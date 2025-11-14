import requests
from core.agents.base import Agent

class CommunicatorAgent(Agent):
    def __init__(self, name="CommunicatorAgent"):
        super().__init__(name)
        self.register_skill("fetch_url", self.fetch_url)

    def fetch_url(self, url: str):
        print(f"'{self.name}' is fetching URL: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the URL: {e}")
            return None
