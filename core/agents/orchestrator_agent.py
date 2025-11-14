from core.agents.base import Agent
from core.services.agent_manager import AgentManager

class OrchestratorAgent(Agent):
    def __init__(self, agent_manager: AgentManager, name="OrchestratorAgent"):
        super().__init__(name)
        self.agent_manager = agent_manager
        self.register_skill("delegate_task", self.delegate_task)

    def delegate_task(self, task_type: str, *args, **kwargs):
        """
        Delegates a task to the appropriate agent based on the task type.
        """
        print(f"'{self.name}' received task: {task_type}")

        target_agent = self._find_agent_for_task(task_type)

        if target_agent:
            print(f"Delegating task '{task_type}' to agent '{target_agent.name}'")
            return target_agent.execute_task(task_type, *args, **kwargs)
        else:
            print(f"No suitable agent found for task type '{task_type}'")
            return None

    def _find_agent_for_task(self, task_type: str) -> Agent:
        """
        Finds an agent in the agent manager that can handle the given task type.
        """
        for agent in self.agent_manager.agents.values():
            if task_type in agent.skills:
                return agent
        return None
