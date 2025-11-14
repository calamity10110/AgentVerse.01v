import os
from litellm import completion

class LLMService:
    def __init__(self, api_key=None, model="claude-3-haiku-20240307"):
        """
        Initializes the LLMService.
        Args:
            api_key (str, optional): The API key for the LLM provider. Defaults to the ANTHROPIC_API_KEY environment variable.
            model (str, optional): The name of the model to use. Defaults to "claude-3-haiku-20240307".
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
        os.environ["ANTHROPIC_API_KEY"] = self.api_key

    def execute_prompt(self, prompt: str, max_tokens=1024):
        """
        Executes a prompt against the configured LLM.
        Args:
            prompt (str): The prompt to send to the LLM.
            max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 1024.
        Returns:
            str: The response from the LLM.
        """
        messages = [{"role": "user", "content": prompt}]
        try:
            response = completion(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"An error occurred while communicating with the LLM: {e}")
            return None
