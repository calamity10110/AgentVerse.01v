from core.agents.base import Agent
from core.services.memory_service import MemoryService
from core.services.agent_manager import AgentManager

class SelfImprovementAgent(Agent):
    def __init__(self, agent_manager: AgentManager, name="SelfImprovementAgent"):
        super().__init__(name)
        self.agent_manager = agent_manager
        self.memory_service = MemoryService()
        self.register_skill("review_memories_and_create_skills", self.review_memories_and_create_skills)

    def review_memories_and_create_skills(self):
        """
        Reviews past task memories, identifies patterns, and creates new skills.
        """
        print(f"'{self.name}' is reviewing memories for potential new skills...")

        llm_agent = self._find_agent_by_class("LLMAgent")
        if not llm_agent:
            print("Error: LLMAgent not found.")
            return

        # Get all memories
        memories = self.memory_service.search(lambda x: True)
        if not memories:
            print("No memories to review.")
            return

        # Create a prompt for the LLM to analyze the memories and create a new skill
        prompt = self._create_skill_creation_prompt(memories)

        # Get the new skill code from the LLM
        new_skill_code = llm_agent.execute_task("reason", prompt)
        if new_skill_code:
            self._save_new_skill(new_skill_code)
        else:
            print("Could not get a new skill from the LLMAgent.")

    def _create_skill_creation_prompt(self, memories) -> str:
        """
        Creates a prompt for the LLM to analyze past memories and create a new skill.
        """
        prompt = f"""
        You are a self-improvement agent. Your job is to analyze the memories of past tasks and create a new skill to automate a common sequence of tasks.
        The memories are in the following format:
        {{
            "command": "The original natural language command",
            "plan": "The JSON plan that was executed",
            "results": "The results of each step in the plan"
        }}

        Here are the recent memories:
        {memories}

        Please analyze these memories and identify a sequence of tasks that could be automated into a single skill.
        Then, write the Python code for a new skill that automates this sequence.
        The skill should be a single function, with a descriptive name and a docstring that explains what it does.
        The function should take any necessary arguments and return a result.

        For example, if you see that the OS is frequently studying files and then fetching their contents, you could create a new skill called `study_and_fetch_file`.
        The output should be only the Python code for the new skill, like this:

        ```python
        def study_and_fetch_file(filepath: str):
            \"\"\"
            Studies a file to identify its functions and then fetches its contents.
            \"\"\"
            # NOTE: This is a simplified example. The actual code would need to
            # interact with the appropriate agents to perform these tasks.
            print(f"Studying and fetching file: {{filepath}}")
            # ... implementation ...
            return "..."
        ```
        """
        return prompt

    def _save_new_skill(self, skill_code: str):
        """
        Saves the new skill code to a file in the core/skills directory.
        """
        # Extract the function name from the code
        try:
            # A simple way to extract the function name
            skill_name = skill_code.split("def ")[1].split("(")[0]
            skill_filename = f"core/skills/{skill_name}.py"
            with open(skill_filename, "w") as f:
                f.write(skill_code)
            print(f"New skill '{skill_name}' saved to '{skill_filename}'")
        except Exception as e:
            print(f"Error saving new skill: {e}")

    def _find_agent_by_class(self, class_name: str) -> Agent:
        """
        Finds an agent in the agent manager by its class name.
        """
        for agent in self.agent_manager.agents.values():
            if agent.__class__.__name__ == class_name:
                return agent
        return None
