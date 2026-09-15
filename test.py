import re
from datetime import datetime


class SimpleAI:
    def __init__(self):
        self.name = "PyBot"
        self.user_name = None
        self.capitals = {
            "france": "Paris",
            "germany": "Berlin",
            "italy": "Rome",
            "spain": "Madrid",
            "united kingdom": "London",
            "uk": "London",
            "japan": "Tokyo",
            "india": "New Delhi",
            "china": "Beijing",
            "usa": "Washington, D.C.",
            "united states": "Washington, D.C.",
            "canada": "Ottawa",
            "brazil": "Brasília",
            "argentina": "Buenos Aires",
            "australia": "Canberra",
            "egypt": "Cairo",
            "south africa": "Pretoria",
            "nigeria": "Abuja",
            "mexico": "Mexico City",
            "russia": "Moscow",
            "turkey": "Ankara",
            "greece": "Athens",
            "sweden": "Stockholm",
            "norway": "Oslo",
            "netherlands": "Amsterdam",
            "switzerland": "Bern",
        }

    def _clean_country_name(self, country_name: str) -> str:
        country_name = country_name.strip().lower()
        country_name = country_name.replace("the ", "")
        country_name = country_name.rstrip("?!.,")
        country_name = re.sub(r"[^a-z\s]", "", country_name)
        return " ".join(country_name.split())

    def _get_capital(self, country_name: str) -> str:
        clean_country = self._clean_country_name(country_name)
        capital = self.capitals.get(clean_country)

        if capital:
            return f"The capital of {clean_country.title()} is {capital}."

        return f"I don’t know the capital of {clean_country.title()} yet."

    def _get_time(self) -> str:
        now = datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}."

    def _do_math(self, text: str) -> str:
        expression = re.sub(r"\s+", "", text)

        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return f"The result is {result}."
        except Exception:
            return "I couldn’t evaluate that expression. Please use a simple math calculation."

    def _remember_name(self, text: str) -> str | None:
        match = re.search(r"(?:my name is|call me)\s+([a-zA-Z]+)", text, re.IGNORECASE)
        if not match:
            return None

        self.user_name = match.group(1).capitalize()
        return f"Nice to meet you, {self.user_name}! I’ll remember your name."

    def _fallback_response(self, lowered: str) -> str:
        if any(phrase in lowered for phrase in ["how are you", "how are you doing"]):
            return "I’m doing well and ready to help. How are you doing?"

        if any(phrase in lowered for phrase in ["i am good", "i'm good", "i am fine", "i'm fine"]):
            return "That’s good to hear! What would you like to talk about?"

        if any(phrase in lowered for phrase in ["i am sad", "i'm sad", "i feel sad"]):
            return "I’m sorry you’re feeling sad. You can talk to me about what happened."

        if "what do you know" in lowered:
            return "I know basic conversation, country capitals, the current date and time, and simple math."

        if "what is my name" in lowered or "do you know my name" in lowered:
            if self.user_name:
                return f"Your name is {self.user_name}."
            return "You haven’t told me your name yet. You can say, ‘my name is Alex’."

        if self.user_name:
            return (
                f"I’m not sure about that, {self.user_name}. I can help with capitals, time, math, "
                "or a simple conversation."
            )

        return (
            "I’m not sure about that yet. I can help with capitals, time, math, and conversation. "
            "Try asking ‘what is the capital of France?’ or ‘how are you?’"
        )

    def respond(self, user_input: str) -> str:
        text = user_input.strip()

        if not text:
            return "I’m here. Ask me anything!"

        lowered = text.lower()

        if any(word in lowered for word in ["hi", "hello", "hey"]):
            return f"Hello! I’m {self.name}, a simple AI assistant. How can I help you today?"

        if any(word in lowered for word in ["bye", "goodbye", "see you"]):
            return "Goodbye! Come back anytime."

        if "your name" in lowered:
            return f"My name is {self.name}."

        remembered_name = self._remember_name(text)
        if remembered_name:
            return remembered_name

        if "help" in lowered:
            return (
                "I can help with simple conversations, basic math, country capitals, and quick information. "
                "Try asking me to calculate, tell the time, or ask for a capital city."
            )

        if "capital" in lowered and "of" in lowered:
            match = re.search(r"capital(?: city)? of\s+(.+)", lowered)
            if match:
                return self._get_capital(match.group(1).strip())

        if "time" in lowered or "date" in lowered:
            return self._get_time()

        if any(word in lowered for word in ["who are you", "what are you", "about you"]):
            return (
                "I’m a lightweight AI assistant built in Python. I can answer simple questions, "
                "chat with you, and do basic calculations."
            )

        if re.search(r"\d+\s*[+\-*/]\s*\d+", lowered):
            return self._do_math(text)

        if "thank" in lowered:
            return "You’re welcome!"

        return self._fallback_response(lowered)


def main() -> None:
    ai = SimpleAI()
    print(f"Welcome! I’m {ai.name}. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.strip().lower() in {"exit", "quit", "bye"}:
            print(f"{ai.name}: Goodbye!")
            break

        print(f"{ai.name}: {ai.respond(user_input)}")


if __name__ == "__main__":
    main()
