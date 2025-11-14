import psutil
from core.agents.base import Agent

class HardwareAgent(Agent):
    def __init__(self, name="HardwareAgent"):
        super().__init__(name)
        self.register_skill("get_cpu_usage", self.get_cpu_usage)
        self.register_skill("get_memory_usage", self.get_memory_usage)
        self.register_skill("get_disk_usage", self.get_disk_usage)

    def get_cpu_usage(self):
        """
        Gets the current CPU usage as a percentage.
        """
        return psutil.cpu_percent(interval=1)

    def get_memory_usage(self):
        """
        Gets the current memory usage as a percentage.
        """
        return psutil.virtual_memory().percent

    def get_disk_usage(self):
        """
        Gets the current disk usage as a percentage.
        """
        return psutil.disk_usage('/').percent
