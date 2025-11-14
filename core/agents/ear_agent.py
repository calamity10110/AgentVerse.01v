from core.agents.base import Agent
from core.services.speech_to_text_service import SpeechToTextService

class EarAgent(Agent):
    def __init__(self, name="EarAgent"):
        super().__init__(name)
        self.stt_service = SpeechToTextService()
        self.register_skill("listen_for_command", self.listen_for_command)

    def listen_for_command(self):
        """
        Listens for a spoken command and returns the transcribed text.
        """
        return self.stt_service.listen()
