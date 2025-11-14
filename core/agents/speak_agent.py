import pyttsx3
from core.agents.base import Agent

class SpeakAgent(Agent):
    def __init__(self, name="SpeakAgent"):
        super().__init__(name)
        self.engine = pyttsx3.init()
        self.register_skill("speak", self.speak)

    def speak(self, text: str):
        """
        Speaks the given text using the text-to-speech engine.
        """
        print(f"'{self.name}' is speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
