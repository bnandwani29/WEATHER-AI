# server/api.py
# Minimal, robust FastAPI server for the weather agent.
from dotenv import load_dotenv
load_dotenv()  # must run before functions that read env

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

# Import local modules after load_dotenv
# weather.py must implement get_current_weather(city) and get_forecast(city, day)
from weather import get_current_weather, get_forecast
import nlu

app = FastAPI(title="Vaiu Weather API")

# Dev CORS: allow local browser client on 8080 (and anything else while developing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # safe for local development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/weather")
def weather_endpoint(city: str = Query(..., min_length=1)):
    try:
        data = get_current_weather(city)
    except RuntimeError as e:
        # missing key or configuration
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        raise HTTPException(status_code=502, detail="Weather API error")

    if data is None:
        raise HTTPException(status_code=404, detail="City not found")
    return {"ok": True, "data": data}

@app.get("/forecast")
def forecast_endpoint(city: str = Query(..., min_length=1), day: str = Query("tomorrow")):
    try:
        data = get_forecast(city, day)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        raise HTTPException(status_code=502, detail="Weather API error")
    return {"ok": True, "data": data}

@app.post("/agent/query")
async def agent_query(request: Request):
    """
    Handle a text query from the client:
      - parse the text (NLU)
      - call the local weather functions directly (no internal HTTP)
      - return a short reply in {"reply": "..."}
    """
    payload = await request.json()
    text = payload.get("text", "").strip()
    if not text:
        return {"reply": "Please provide a question in the 'text' field."}

    parsed = nlu.parse(text)
    city = parsed.get("city")
    when = parsed.get("when", "now")

    if not city:
        return {"reply": "Which city did you mean?"}

    # CALL WEATHER FUNCTIONS DIRECTLY (avoid calling our own HTTP endpoints)
    try:
        if when == "now":
            data = get_current_weather(city)
        else:
            data = get_forecast(city, when)
    except RuntimeError as e:
        # configuration problem (e.g. missing key)
        return {"reply": f"Server configuration error: {str(e)}"}
    except Exception as e:
        # catch-all
        return {"reply": "Weather service returned an error. Please try again later."}

    if not data:
        return {"reply": f"I couldn't find weather for {city}. Could you check the city name?"}

    # Format a friendly reply
    if when == "now":
        reply = f"In {data.get('city','that city')}, it's {data.get('temp')}°C and {data.get('description')}."
    else:
        # forecast may include chance_of_rain or similar fields
        if 'chance_of_rain' in data:
            reply = (f"Tomorrow in {data.get('city','that city')}, expect {data.get('description')} "
                     f"with around {data.get('temp')}°C. Chance of rain is about {data.get('chance_of_rain')}%.")
        else:
            reply = f"Tomorrow in {data.get('city','that city')}, expect {data.get('temp')}°C with {data.get('description')}."

    return {"reply": reply}
