import subprocess
from core.agents.base import Agent

class ApplicationAgent(Agent):
    def __init__(self, name="ApplicationAgent"):
        super().__init__(name)
        self.register_skill("run_shell_command", self.run_shell_command)

    def run_shell_command(self, command: str):
        """
        Runs a shell command and returns the output.
        """
        print(f"'{self.name}' is running shell command: {command}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"
