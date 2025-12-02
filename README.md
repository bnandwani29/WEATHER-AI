Voice Weather Assistant — Python
<a href="#"> <img src="./.github/assets/weather-icon.png" alt="Weather Assistant Logo" width="100" height="100"> </a>

A complete starter project for building a voice-controlled weather assistant using FastAPI, JavaScript Voice APIs, and OpenWeatherMap.

This project demonstrates:

A fully functional voice-first weather assistant

Real-time speech-to-text and text-to-speech using browser APIs

Weather data fetched from the OpenWeatherMap API

A clean and modern UI with glassmorphism styling

Natural-language understanding for extracting:

❓ Intent (current vs tomorrow forecast)

🏙️ City name

Easy frontend interaction powered by fetch

A backend built with FastAPI, ready for extension, deployment, and hosting

This weather voice assistant is compatible with ANY custom web frontend and deployable on any hosting environment (Render, Vercel, Netlify, Railway, etc.).

🎯 Project Overview

This project includes:

🎙️ Voice Weather Assistant with speech input + spoken output

🌦️ Real-time weather using the OpenWeatherMap API

🧠 Lightweight NLU system (nlu.py)

⚡ FastAPI backend (server/api.py)

🎨 Beautiful modern UI (client/index.html + CSS + JS)

🧪 Clean modular code structure

🚀 Simple to run locally or deploy

📁 Project Structure
project/
│
├── client/
│   ├── index.html
│   ├── app.js
│   ├── style.css
│
├── server/
│   └── api.py
│
├── src/
│   ├── agent.py
│   ├── test_agent.py
│
├── weather.py
├── nlu.py
├── local_agent.py
├── .env.example
└── README.md

🧩 How It Works
🔹 Voice Input

Uses SpeechRecognition API to capture user speech, convert it to text, and send it to the FastAPI backend.

🔹 Natural Language Understanding (NLU)

nlu.py extracts:

The city

Whether the user asked for current weather or tomorrow’s forecast

🔹 Weather API

weather.py fetches:

Temperature

Weather condition

Forecast

🔹 Voice Output

Uses SpeechSynthesis API to speak the assistant’s response.

🛠️ Installation & Setup
1️⃣ Clone the repo
git clone https://github.com/your-username/WEATHER-AI.git
cd WEATHER-AI

2️⃣ Create a virtual environment
Windows
python -m venv venv
.\venv\Scripts\activate

macOS / Linux
python3 -m venv venv
source venv/bin/activate

3️⃣ Install Python dependencies
pip install -r requirements.txt

4️⃣ Add your API key

Create .env file:

OPENWEATHER_KEY=YOUR_KEY_HERE

🚀 Running the Project
Start the FastAPI backend
python -m uvicorn server.api:app --reload --host 127.0.0.1 --port 8000


Backend health check:
➡️ http://127.0.0.1:8000/health

Start the frontend

Open a new terminal:

cd client
python -m http.server 8080


Frontend available at:
➡️ http://127.0.0.1:8080

📡 API Endpoints
POST /agent/query

Request:

{ "text": "What's the weather in Mumbai?" }


Response:

{ "reply": "In Mumbai, it's 27°C and smoke." }

🧪 Example Voice Queries

Try speaking:

“What’s the weather in Delhi?”

“Will it rain tomorrow in Pune?”

“Weather in Jaipur right now?”

“Tell me tomorrow’s weather for Chennai.”

🔐 Environment & Security

This project includes:

✔ .env.example (safe to commit)
❌ .env is ignored automatically
✔ OpenWeather API key stored securely

Never commit real API keys.

🚀 Deployment

You can deploy using:

Render

Railway

Docker

Vercel (frontend) + Render (backend)

Netlify + FastAPI backend

Dockerfile support can be added easily.

🏆 Future Enhancements

Add AI LLM-based conversational agent

Add background weather animations

Multi-day forecasts

Full mobile UI

Wake-word detection (“Hey Weather”)

👩‍💻 Author

Bhavya Nandwani
B.Tech CSE-AI
AI • Python • Full-Stack • Voice Interaction Systems
