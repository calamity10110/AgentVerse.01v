import yaml
from core.services.agent_manager import AgentManager

class Kernel:
    def __init__(self, config_path):
        self.agent_manager = AgentManager()
        self.config = self._load_config(config_path)

    def _load_config(self, config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def bootstrap(self):
        print("Kernel bootstrapping...")
        self.agent_manager.discover_and_load_agents()
        self._load_agents_from_config()
        self.agent_manager.discover_and_load_skills()
        self._start_agents()
        print("Kernel bootstrap complete.")

    def _load_agents_from_config(self):
        for agent_name in self.config.get('agents', []):
            if agent_name in ["OrchestratorAgent", "SelfImprovementAgent"]:
                # These agents require the agent_manager
                self.agent_manager.create_agent_instance(agent_name, agent_manager=self.agent_manager)
            else:
                self.agent_manager.create_agent_instance(agent_name)

    def _start_agents(self):
        for agent_id in self.agent_manager.agents:
            self.agent_manager.activate_agent(agent_id)

    def run_interaction_loop(self):
        """
        Runs the main interaction loop of the OS.
        """
        text_agent = self._find_agent_by_class("TextAgent")
        ear_agent = self._find_agent_by_class("EarAgent")
        speak_agent = self._find_agent_by_class("SpeakAgent")

        if not text_agent or not ear_agent or not speak_agent:
            print("Error: Missing one or more required agents for the interaction loop.")
            return

        speak_agent.execute_task("speak", "Hello! I am your agent-based OS. How can I help you today?")

        while True:
            # For this PoC, we'll let the user choose the input method.
            input_method = text_agent.execute_task("get_user_input", "Choose your input method (text/speech): ")

            if input_method.lower() == "text":
                command = text_agent.execute_task("get_user_input", "Please enter your command: ")
            elif input_method.lower() == "speech":
                command = ear_agent.execute_task("listen_for_command")
            else:
                speak_agent.execute_task("speak", "Invalid input method. Please try again.")
                continue

            if command:
                if command.lower() == "exit":
                    speak_agent.execute_task("speak", "Goodbye!")
                    break
                elif command.lower() == "run self-improvement":
                    self.run_self_improvement()
                else:
                    self.run_task(command)
            else:
                speak_agent.execute_task("speak", "I'm sorry, I didn't catch that. Please try again.")

    def run_task(self, command: str):
        """
        Runs a natural language command through the OrchestratorAgent.
        """
        orchestrator = self._find_agent_by_class("OrchestratorAgent")
        if orchestrator:
            orchestrator.execute_task("process_natural_language_command", command)
        else:
            print("Error: OrchestratorAgent not found.")

    def run_self_improvement(self):
        """
        Runs the self-improvement process.
        """
        self_improvement_agent = self._find_agent_by_class("SelfImprovementAgent")
        if self_improvement_agent:
            self_improvement_agent.execute_task("review_memories_and_create_skills")
        else:
            print("Error: SelfImprovementAgent not found.")

    def _find_agent_by_class(self, class_name: str):
        for agent in self.agent_manager.agents.values():
            if agent.__class__.__name__ == class_name:
                return agent
        return None

    def shutdown(self):
        print("Kernel shutting down...")
        for agent_id in self.agent_manager.agents:
            self.agent_manager.deactivate_agent(agent_id)
        print("Kernel shutdown complete.")

if __name__ == "__main__":
    kernel = Kernel('config.yaml')
    kernel.bootstrap()

    kernel.run_interaction_loop()

    kernel.shutdown()
