import os
import requests
from dotenv import load_dotenv

load_dotenv()


class LLMHandler:
    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4o-mini",
        name: str = "PyPal",
        role: str = "helpful AI assistant",
    ) -> None:
        self.provider = provider.lower()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.provider == "openai" and not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required for OpenAI")
        self.history = []
        self.model = model
        self.system_prompt = (
            f"Your name is {name}, and you are a {role}. "
            "Always respond accordingly to this role."
        )
        self.name = name
        self.role = role

    def add_to_history(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})

    def show_history(self) -> None:
        for entry in self.history:
            print(f"{entry['role'].capitalize()}: {entry['content']}")

    def generate(self, prompt: str) -> str:
        if self.provider == "openai":
            return self._chat_with_openai(prompt)
        elif self.provider == "ollama":
            return self._chat_with_ollama(prompt)
        else:
            return "Unknown provider"

    def _chat_with_openai(self, prompt: str) -> str:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Build context from last 3 messages + current prompt
        recent = self.history[-3:] if len(self.history) >= 3 else self.history[:]
        messages = []

        system_message = {"role": "system", "content": self.system_prompt}
        messages.append(system_message)

        # Add conversation history
        messages += recent

        # Add current user message
        user_message = {"role": "user", "content": prompt}
        messages.append(user_message)

        data = {"model": self.model, "messages": messages}

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        reply = result["choices"][0]["message"]["content"]

        self.add_to_history("user", prompt)
        self.add_to_history("assistant", reply)
        return reply

    def _chat_with_ollama(self, prompt: str) -> str:
        url = "http://localhost:11434/api/chat"

        # Build messages array for Ollama chat API
        recent = self.history[-3:] if len(self.history) >= 3 else self.history[:]
        messages = []

        system_message = {"role": "system", "content": self.system_prompt}
        messages.append(system_message)

        # Add conversation history
        messages += recent

        # Add current user message
        user_message = {"role": "user", "content": prompt}
        messages.append(user_message)

        data = {"model": self.model, "messages": messages, "stream": False}

        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        reply = result.get("message", {}).get("content", "No reply")

        self.add_to_history("user", prompt)
        self.add_to_history("assistant", reply)
        return reply
