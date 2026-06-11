#!/usr/bin/env python3
"""
Advanced Terminal Chatbot - Async API calls with JSON
"""

import json
import asyncio
import aiohttp
from datetime import datetime
from typing import Optional
import os


class AdvancedChatbot:
    def __init__(self, api_base="https://api.openai.com/v1"):
        self.api_base = api_base
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.messages = []

    async def call_api(self, prompt: str, use_openai: bool = False) -> dict:
        """
        Async API call to OpenAI or local service
        Returns JSON response
        """
        if not use_openai or not self.api_key:
            return self.local_response(prompt)

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_base}/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "status": "success",
                            "response": data["choices"][0]["message"]["content"],
                            "tokens": data["usage"]["total_tokens"],
                        }
                    else:
                        return {
                            "status": "error",
                            "message": f"Status {response.status}",
                        }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def local_response(self, prompt: str) -> dict:
        """Fallback: Local response without API"""
        responses = {
            "hello": "Hi! How are you today?",
            "help": "I'm here to help! Ask me anything.",
            "how are you": "I'm doing great, thanks for asking!",
        }

        for key, value in responses.items():
            if key in prompt.lower():
                return {"status": "success", "response": value, "source": "local"}

        return {
            "status": "success",
            "response": "That's interesting! Tell me more.",
            "source": "local",
        }

    async def add_message(
        self, role: str, content: str, metadata: Optional[dict] = None
    ):
        """Add message to history"""
        msg = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
        }
        if metadata:
            msg.update(metadata)
        self.messages.append(msg)

    async def chat_async(self, use_api: bool = False):
        """Async chat loop"""
        print("\n🤖 ADVANCED TERMINAL CHATBOT (Async)")
        print("Commands: 'quit', 'export', 'clear'\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() == "quit":
                    print("✅ Goodbye!")
                    break

                if user_input.lower() == "export":
                    self.export_json()
                    continue

                if user_input.lower() == "clear":
                    self.messages = []
                    print("✅ History cleared!\n")
                    continue

                # Async API call
                await self.add_message("user", user_input)

                print("\n⏳ Thinking...\n")
                api_response = await self.call_api(user_input, use_api)

                response_text = api_response.get("response", "Error getting response")
                await self.add_message("bot", response_text, api_response)

                print(f"Bot: {response_text}\n")

            except KeyboardInterrupt:
                print("\n✅ Exiting...")
                break

    def export_json(self, filename: str = "chat_export.json"):
        """Export to JSON"""
        with open(filename, "w") as f:
            json.dump(self.messages, f, indent=2)
        print(f"✅ Exported {len(self.messages)} messages to {filename}\n")

    def display_json(self):
        """Display raw JSON"""
        print(json.dumps(self.messages, indent=2))


async def main():
    bot = AdvancedChatbot()
    await bot.chat_async(use_api=False)  # Set True if OpenAI API key available


if __name__ == "__main__":
    asyncio.run(main())
