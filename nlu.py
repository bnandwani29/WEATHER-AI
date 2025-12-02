import re

def parse(text: str):
    """
    Simple rule-based parser for weather queries.
    Returns: {"intent": ..., "city": ..., "when": ...}
    """
    if not text:
        return {"intent": None, "city": None, "when": "now"}

    t = text.lower()
    when = "now"

    # Detect if user asks about tomorrow
    if "tomorrow" in t or "will it rain" in t or "rain tomorrow" in t:
        when = "tomorrow"

    # Extract city after "in", "at", "for"
    m = re.search(r'\b(?:in|at|for)\s+([a-z\s]+)', t)
    city = None
    if m:
        city_raw = m.group(1).strip()
        city_raw = re.sub(r'\btomorrow\b', '', city_raw).strip()  # clean trailing words
        city = city_raw.title() if city_raw else None

    intent = "weather_forecast" if when == "tomorrow" else "weather_current"
    return {"intent": intent, "city": city, "when": when}
