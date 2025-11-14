from core.agents.base import Agent

class TextAgent(Agent):
    def __init__(self, name="TextAgent"):
        super().__init__(name)
        self.register_skill("get_user_input", self.get_user_input)

    def get_user_input(self, prompt: str):
        """
        Gets input from the user's keyboard.
        """
        return input(prompt)
