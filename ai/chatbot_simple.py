#!/usr/bin/env python3
"""
Simple Terminal Chatbot - Minimal Version
"""

import json
import requests
from datetime import datetime


class SimpleChatbot:
    def __init__(self):
        self.history = []

    def api_call(
        self, prompt: str, api_url: str = "http://localhost:8000/workflow/analyze"
    ) -> dict:
        """
        API Call to your FastAPI backend
        Returns: JSON response
        """
        payload = {"text": prompt}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=5)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def save_json(self, filename: str = "history.json"):
        """Save conversation to JSON"""
        with open(filename, "w") as f:
            json.dump(self.history, f, indent=2)

    def add_message(self, role: str, content: str, metadata: dict = None):
        """Add message to history"""
        msg = {
            "time": datetime.now().isoformat(),
            "role": role,
            "content": content,
            "meta": metadata or {},
        }
        self.history.append(msg)
        return msg

    def run(self):
        """Main loop"""
        print("💬 Chatbot (type 'quit' to exit, 'save' to save)")

        while True:
            user_text = input("\nYou: ").strip()

            if user_text.lower() == "quit":
                self.save_json()
                break
            elif user_text.lower() == "save":
                self.save_json()
                print("✅ Saved!")
                continue
            elif not user_text:
                continue

            # API call
            api_response = self.api_call(user_text)

            # Add to history
            self.add_message("user", user_text)
            self.add_message("bot", str(api_response), api_response)

            # Display response
            if "label" in api_response:
                label = api_response["label"]
                confidence = api_response["confidence"]
                print(f"\nBot: {label} (confidence: {confidence})")
            else:
                print(f"\nBot: {api_response}")


if __name__ == "__main__":
    bot = SimpleChatbot()
    bot.run()
