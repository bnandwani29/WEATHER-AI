# weather.py
import os
import requests
from datetime import datetime, timedelta

def _get_key():
    key = os.getenv("OPENWEATHER_KEY")
    if not key:
        # raise only when a weather function actually needs the key
        raise RuntimeError("OPENWEATHER_KEY not set. Add it to .env or export it in your environment.")
    return key

def get_current_weather(city: str):
    key = _get_key()
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&units=metric&appid={key}"
    )
    r = requests.get(url, timeout=10)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    data = r.json()
    return {
        "city": data.get("name"),
        "temp": round(data["main"]["temp"]),
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
    }

def get_forecast(city: str, day="tomorrow"):
    key = _get_key()
    # geocoding
    geo_url = (
        f"http://api.openweathermap.org/geo/1.0/direct"
        f"?q={city}&limit=1&appid={key}"
    )
    geo_res = requests.get(geo_url, timeout=10)
    geo_res.raise_for_status()
    geo_data = geo_res.json()
    if not geo_data:
        raise ValueError("City not found")
    lat = geo_data[0]["lat"]
    lon = geo_data[0]["lon"]

    forecast_url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?lat={lat}&lon={lon}&units=metric&appid={key}"
    )
    res = requests.get(forecast_url, timeout=10)
    res.raise_for_status()
    forecast_data = res.json()

    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)

    tomorrow_list = [
        entry for entry in forecast_data.get("list", [])
        if datetime.utcfromtimestamp(entry["dt"]).date() == tomorrow
    ]
    if not tomorrow_list:
        raise ValueError("No forecast available for tomorrow")

    temps = [round(i["main"]["temp"]) for i in tomorrow_list]
    descriptions = [i["weather"][0]["description"] for i in tomorrow_list]
    rain_probs = [i.get("pop", 0) * 100 for i in tomorrow_list]

    avg_temp = round(sum(temps) / len(temps))
    rain_chance = round(sum(rain_probs) / len(rain_probs))
    dominant_description = max(set(descriptions), key=descriptions.count)

    return {
        "city": city.title(),
        "temp": avg_temp,
        "description": dominant_description,
        "chance_of_rain": rain_chance,
    }
