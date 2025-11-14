from core.agents.base import Agent
from core.services.llm_service import LLMService

class LLMAgent(Agent):
    def __init__(self, name="LLMAgent"):
        super().__init__(name)
        self.llm_service = LLMService()
        self.register_skill("reason", self.reason)

    def reason(self, prompt: str):
        """
        Uses the LLM to reason about a given prompt.
        """
        print(f"'{self.name}' is reasoning about the prompt: {prompt}")
        return self.llm_service.execute_prompt(prompt)
