import uuid

class Agent:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.skills = {}
        self.is_running = False

    def register_skill(self, skill_name, skill_function):
        self.skills[skill_name] = skill_function

    def start(self):
        self.is_running = True
        print(f"Agent {self.name} ({self.id}) is starting.")

    def stop(self):
        self.is_running = False
        print(f"Agent {self.name} ({self.id}) is stopping.")

    def execute_task(self, task_name, *args, **kwargs):
        if not self.is_running:
            print(f"Agent {self.name} is not running.")
            return

        if task_name in self.skills:
            return self.skills[task_name](*args, **kwargs)
        else:
            print(f"Skill '{task_name}' not found for agent {self.name}.")
            return None
