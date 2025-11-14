from core.agents.base import Agent

class AgentManager:
    def __init__(self):
        self.agents = {}

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
