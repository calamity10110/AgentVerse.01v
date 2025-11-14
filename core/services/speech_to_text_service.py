import speech_recognition as sr

class SpeechToTextService:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        """
        Listens for a spoken command and transcribes it.
        """
        with sr.Microphone() as source:
            print("Listening for a command...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            command = self.recognizer.recognize_sphinx(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Recognition error: {e}")
            return None
