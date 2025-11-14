from core.agents.base import Agent
import json

class DisplayAgent(Agent):
    def __init__(self, name="DisplayAgent"):
        super().__init__(name)
        self.register_skill("show_message", self.show_message)
        self.register_skill("show_plan", self.show_plan)

    def show_message(self, message: str):
        """
        Displays a message to the user.
        """
        print(f"[DisplayAgent]: {message}")

    def show_plan(self, plan: list):
        """
        Displays a task plan to the user in a readable format.
        """
        print("\n--- Proposed Task Plan ---")
        for i, task in enumerate(plan):
            print(f"Step {i+1}:")
            print(f"  - Task: {task.get('task_type')}")
            print(f"  - Arguments: {task.get('args')}")
            print(f"  - Keyword Arguments: {task.get('kwargs')}")
        print("--------------------------\n")
