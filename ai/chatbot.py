#!/usr/bin/env python3
"""
Terminal Chatbot - Skills: API calling, prompts, responses, JSON handling
"""

import json
import os
from datetime import datetime
from pathlib import Path
import requests
from transformers import pipeline

# Initialize sentiment analysis
classifier = pipeline(
    "sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english"
)


class Chatbot:
    def __init__(self, chat_file="chat_history.json"):
        self.chat_file = chat_file
        self.conversations = self.load_conversations()
        self.current_session = []

    def load_conversations(self):
        """Load chat history from JSON file"""
        if os.path.exists(self.chat_file):
            with open(self.chat_file, "r") as f:
                return json.load(f)
        return []

    def save_conversations(self):
        """Save chat history to JSON file"""
        with open(self.chat_file, "w") as f:
            json.dump(self.conversations, f, indent=2)

    def get_sentiment(self, text):
        """Get sentiment analysis using transformers"""
        result = classifier(text)
        return result[0]

    def create_message(self, role, content, sentiment=None):
        """Create a message object"""
        message = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
        }
        if sentiment:
            message["sentiment"] = sentiment
        return message

    def call_openai_api(self, prompt):
        """Optional: Call OpenAI API (requires API key)"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 150,
        }

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=10,
            )
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"API Error: {e}")

        return None

    def generate_response(self, user_input):
        """Generate response using sentiment or API"""
        # Method 1: Simple sentiment-based response (local)
        sentiment_result = self.get_sentiment(user_input)
        sentiment = sentiment_result["label"]
        confidence = round(sentiment_result["score"], 3)

        if sentiment == "POSITIVE":
            response = "That's great! 😊 I'm glad you're happy!"
        elif sentiment == "NEGATIVE":
            response = "I understand your concern. 😔 How can I help?"
        else:
            response = "That's interesting! Tell me more. 🤔"

        return response, {"sentiment": sentiment, "confidence": confidence}

    def chat(self):
        """Main chat loop"""
        print("\n" + "=" * 50)
        print("🤖 TERMINAL CHATBOT")
        print("=" * 50)
        print("Commands: 'quit' to exit, 'save' to save history, 'history' to view")
        print("=" * 50 + "\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                # Commands
                if user_input.lower() == "quit":
                    self.save_conversations()
                    print("\n✅ Chat history saved. Goodbye!")
                    break

                if user_input.lower() == "save":
                    self.save_conversations()
                    print("✅ Conversation saved to JSON!")
                    continue

                if user_input.lower() == "history":
                    self.show_history()
                    continue

                # Generate response
                response, metadata = self.generate_response(user_input)

                # Create and store messages
                user_msg = self.create_message("user", user_input, metadata)
                bot_msg = self.create_message("bot", response)

                self.current_session.append(user_msg)
                self.current_session.append(bot_msg)

                # Show response with sentiment
                print(f"\nBot: {response}")
                print(
                    f"     [Sentiment: {metadata['sentiment']} ({metadata['confidence']})]"
                )
                print()

            except KeyboardInterrupt:
                print("\n\n✅ Exiting...")
                self.save_conversations()
                break

    def show_history(self):
        """Display conversation history"""
        if not self.current_session:
            print("No conversation yet.\n")
            return

        print("\n" + "=" * 50)
        print("CONVERSATION HISTORY (JSON)")
        print("=" * 50)
        for msg in self.current_session:
            print(json.dumps(msg, indent=2))
        print("=" * 50 + "\n")

    def export_json(self, filename="export.json"):
        """Export current session to JSON"""
        with open(filename, "w") as f:
            json.dump(self.current_session, f, indent=2)
        print(f"✅ Exported to {filename}")


def main():
    bot = Chatbot()
    bot.chat()


if __name__ == "__main__":
    main()
