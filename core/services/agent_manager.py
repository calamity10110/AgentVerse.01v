import os
import importlib
from core.agents.base import Agent

class AgentManager:
    def __init__(self):
        self.agents = {}
        self.agent_classes = {}

    def discover_and_load_agents(self, agent_directory="core/agents"):
        """
        Dynamically discovers and loads agent classes from the specified directory.
        """
        print(f"Discovering agents in '{agent_directory}'...")
        for filename in os.listdir(agent_directory):
            if filename.endswith(".py") and filename != "base.py" and filename != "__init__.py":
                module_name = f"{agent_directory.replace('/', '.')}.{filename[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type) and issubclass(attr, Agent) and attr is not Agent:
                            self.agent_classes[attr.__name__] = attr
                            print(f"Discovered agent class: {attr.__name__}")
                except Exception as e:
                    print(f"Error loading module {module_name}: {e}")

    def discover_and_load_skills(self, skill_directory="core/skills"):
        """
        Dynamically discovers and loads skills from the specified directory,
        and attaches them to the appropriate agents.
        """
        print(f"Discovering skills in '{skill_directory}'...")
        if not os.path.exists(skill_directory):
            return

        for filename in os.listdir(skill_directory):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = f"{skill_directory.replace('/', '.')}.{filename[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if callable(attr) and not attr_name.startswith("__"):
                            # For simplicity, we'll attach the new skill to the OrchestratorAgent
                            # In a more advanced implementation, the LLM could decide which agent gets the skill.
                            orchestrator = self._find_agent_by_class("OrchestratorAgent")
                            if orchestrator:
                                orchestrator.register_skill(attr_name, attr)
                                print(f"Loaded skill '{attr_name}' and attached it to the OrchestratorAgent.")
                except Exception as e:
                    print(f"Error loading module {module_name}: {e}")

    def create_agent_instance(self, class_name, **kwargs):
        """
        Creates an instance of an agent class.
        """
        if class_name in self.agent_classes:
            agent_class = self.agent_classes[class_name]
            try:
                # Pass kwargs to the agent's constructor
                instance = agent_class(**kwargs)
                self.load_agent(instance)
                return instance
            except Exception as e:
                print(f"Error creating instance of {class_name}: {e}")
                return None
        else:
            print(f"Agent class '{class_name}' not found.")
            return None

    def load_agent(self, agent: Agent):
        self.agents[agent.id] = agent
        print(f"Agent '{agent.name}' ({agent.id}) loaded.")

    def activate_agent(self, agent_id: str):
        if agent_id in self.agents:
            self.agents[agent_id].start()
        else:
            print(f"Agent with ID '{agent_id}' not found.")

    def deactivate_agent(self, agent_id: str):
        if agent_id in self.agents:
            self.agents[agent_id].stop()
        else:
            print(f"Agent with ID '{agent_id}' not found.")

    def get_agent(self, agent_id: str) -> Agent:
        return self.agents.get(agent_id)

    def _find_agent_by_class(self, class_name: str) -> Agent:
        """
        Finds an agent in the agent manager by its class name.
        """
        for agent in self.agents.values():
            if agent.__class__.__name__ == class_name:
                return agent
        return None
