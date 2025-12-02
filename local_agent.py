"""
local_agent.py

Simple command-line agent that uses your REST "weather" function.

- Uses nlu.parse(text) to extract city/when.
- Calls the REST API at AGENT_API_BASE (/weather and /forecast).
- Prints a natural reply and (optionally) speaks it using pyttsx3 when available.

Usage:
    # start your server first:
    uvicorn server.api:app --reload --port 8000

    # run agent:
    python local_agent.py

Notes:
- Set AGENT_API_BASE env var if your API is not at http://127.0.0.1:8000
- Install optional TTS: pip install pyttsx3  (works offline)
"""

import os
import sys
import requests

# Try to import the project's NLU parser
try:
    import nlu
except Exception as e:
    # If import fails, provide a minimal fallback parser
    print("Warning: could not import nlu.py. Using a minimal fallback parser.", file=sys.stderr)

    class nlu:
        @staticmethod
        def parse(text: str):
            # Very small fallback: look for 'tomorrow' and city after 'in' or 'for'
            import re
            t = text.lower() if text else ""
            when = "now"
            if "tomorrow" in t or "will it rain" in t:
                when = "tomorrow"
            m = re.search(r'\b(?:in|at|for)\s+([a-z\s]+)', t)
            city = m.group(1).strip().title() if m else None
            intent = "weather_forecast" if when == "tomorrow" else "weather_current"
            return {"intent": intent, "city": city, "when": when}


# Optional TTS using pyttsx3 (offline). If not installed, agent will just print replies.
TTS_AVAILABLE = False
try:
    import pyttsx3

    tts_engine = pyttsx3.init()
    TTS_AVAILABLE = True
except Exception:
    tts_engine = None
    TTS_AVAILABLE = False

API_BASE = os.getenv("AGENT_API_BASE", "http://127.0.0.1:8000")


def format_agent_reply(data: dict, when: str = "now") -> str:
    """Format the weather API response dict into a natural-sounding reply."""
    if not data:
        return "Sorry, I couldn't get weather details."

    if when != "now" and "chance_of_rain" in data:
        # forecast style
        city = data.get("city", "that city")
        temp = data.get("temp")
        desc = data.get("description", "weather")
        rain = data.get("chance_of_rain")
        return f"Tomorrow in {city}, expect {desc} with around {temp}°C. Chance of rain is about {rain}%."
    else:
        # current weather style
        city = data.get("city", "that city")
        temp = data.get("temp")
        desc = data.get("description", "weather")
        return f"The weather in {city} is currently {temp}°C with {desc}."


def call_weather_api(city: str, when: str = "now") -> str:
    """
    Call the weather server endpoints and return a natural language reply string.
    - city: string or None
    - when: 'now' or 'tomorrow' (or other token your NLU sets)
    """
    if not city:
        return "Which city did you mean?"

    try:
        if when == "now":
            url = f"{API_BASE}/weather"
            resp = requests.get(url, params={"city": city}, timeout=8)
        else:
            url = f"{API_BASE}/forecast"
            resp = requests.get(url, params={"city": city, "day": when}, timeout=8)

        # Raise for non-2xx responses (so we can detect errors)
        resp.raise_for_status()

    except requests.exceptions.HTTPError as e:
        # If the API returned 404, city not found.
        try:
            code = resp.status_code
        except Exception:
            code = None
        if code == 404:
            return f"Sorry — I couldn't find weather for \"{city}\". Could you check the city name?"
        return "Sorry, the weather service returned an error. Please try again later."
    except requests.exceptions.RequestException as e:
        return "Sorry, I couldn't reach the weather service. Check your network or server."

    # Extract the API response payload
    payload = {}
    try:
        payload = resp.json().get("data", {})
    except Exception:
        # If JSON parsing fails, return a simple message
        return "Sorry, the weather service returned an invalid response."

    # Format into a natural reply
    reply = format_agent_reply(payload, when=when)
    return reply


def speak_text(text: str):
    """Speak the text using pyttsx3 if available."""
    if not text:
        return
    if TTS_AVAILABLE and tts_engine:
        try:
            tts_engine.say(text)
            tts_engine.runAndWait()
        except Exception:
            # If TTS fails quietly, continue
            pass


def interactive_loop():
    print("=== Vaiu Local Agent (CLI) ===")
    print("Type a weather question (e.g. \"What's the weather in Mumbai?\") or 'quit' to exit.")
    while True:
        try:
            user = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if not user:
            continue
        if user.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        # Parse user input
        parsed = nlu.parse(user)
        city = parsed.get("city")
        when = parsed.get("when", "now")
        intent = parsed.get("intent")

        # Basic validation
        if not city:
            # Ask for clarification
            follow = "Which city did you mean?"
            print("Agent:", follow)
            speak_text(follow)
            continue

        # Call weather API
        reply = call_weather_api(city, when=when)
        print("Agent:", reply)
        speak_text(reply)


if __name__ == "__main__":
    # CLI entrypoint
    # Optionally accept a single question argument: python local_agent.py "What's the weather in Mumbai?"
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:]).strip()
        parsed = nlu.parse(question)
        city = parsed.get("city")
        when = parsed.get("when", "now")
        if not city:
            print("Agent: Which city did you mean?")
            sys.exit(0)
        reply = call_weather_api(city, when=when)
        print("Agent:", reply)
        speak_text(reply)
    else:
        interactive_loop()
