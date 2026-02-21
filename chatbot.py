import os
import json
from groq import Groq
import tiktoken


class ConversationManager:
    def __init__(
        self,
        api_key=None,
        default_model="llama-3.1-8b-instant",
        default_temperature=0.7,
        default_max_tokens=5000,
        system_message="You are a helpful assistant.",
        token_budget=10000,
        history_file="chat_history.json"
    ):
        if api_key is None:
            api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found. Please set it as environment variable.")

        self.client = Groq(api_key=api_key)

        self.default_model = default_model
        self.default_temperature = default_temperature
        self.default_max_tokens = default_max_tokens
        self.token_budget = token_budget

        self.system_messages = {
            "helpful": "You are a helpful, polite assistant.",
            "sassy": "You are a sassy assistant who is fed up with answering questions.",
            "teacher": "You are a patient teacher who explains things step by step.",
            "custom": system_message
        }

        self.current_persona = "helpful"
        self.history_file = history_file
        self.encoder = tiktoken.get_encoding("cl100k_base")

        self.load_conversation_history()

    def load_conversation_history(self):
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                self.conversation_history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.conversation_history = [
                {"role": "system", "content": self.system_messages[self.current_persona]}
            ]

    def save_conversation_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.conversation_history, f, indent=2)

    def clear_history(self):
        self.conversation_history = [
            {"role": "system", "content": self.system_messages[self.current_persona]}
        ]
        self.save_conversation_history()

    def count_tokens(self, text):
        return len(self.encoder.encode(text))

    def total_tokens_used(self):
        return sum(self.count_tokens(m["content"]) for m in self.conversation_history)

    def enforce_token_budget(self):
        while self.total_tokens_used() > self.token_budget and len(self.conversation_history) > 1:
            self.conversation_history.pop(1)

    def set_persona(self, persona_name):
        if persona_name not in self.system_messages:
            return

        self.current_persona = persona_name
        self.conversation_history[0] = {
            "role": "system",
            "content": self.system_messages[persona_name]
        }
        self.save_conversation_history()

    def chat_completion(self, user_prompt):
        self.conversation_history.append(
            {"role": "user", "content": user_prompt}
        )

        self.enforce_token_budget()

        response = self.client.chat.completions.create(
            model=self.default_model,
            messages=self.conversation_history,
            temperature=self.default_temperature,
            max_tokens=self.default_max_tokens
        )

        assistant_reply = response.choices[0].message.content

        self.conversation_history.append(
            {"role": "assistant", "content": assistant_reply}
        )

        self.save_conversation_history()

        return assistant_reply