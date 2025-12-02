<h1>Voice Weather Assistant — Python</h1>
<br><br>

<p>
A complete starter project for building a voice-controlled weather assistant using FastAPI, JavaScript Voice APIs, and OpenWeatherMap.
</p>

<p>This project demonstrates:</p>
<ul>
  <li>A fully functional voice-first weather assistant</li>
  <li>Real-time speech-to-text and text-to-speech using browser APIs</li>
  <li>Weather data fetched from the OpenWeatherMap API</li>
  <li>Clean and modern UI with glassmorphism styling</li>
  <li>Natural-language understanding for extracting:<br>
     ❓ Intent (current vs tomorrow forecast)<br>
     🏙️ City name
  </li>
  <li>Easy frontend interaction powered by fetch</li>
  <li>A backend built with FastAPI, ready for extension, deployment, and hosting</li>
</ul>

<p>
This weather voice assistant is compatible with ANY custom web frontend and deployable on Render, Vercel, Netlify, Railway, and more.
</p>

<hr>

<h2>🎯 Project Overview</h2>

<ul>
  <li>🎙️ Voice Weather Assistant (speech input + spoken output)</li>
  <li>🌦️ Real-time weather using OpenWeatherMap API</li>
  <li>🧠 Lightweight NLU system (nlu.py)</li>
  <li>⚡ FastAPI backend (server/api.py)</li>
  <li>🎨 Modern UI (client/index.html + CSS + JS)</li>
  <li>🧪 Clean modular code structure</li>
  <li>🚀 Easy local run & deployment</li>
</ul>

<hr>

<h2>📁 Project Structure</h2>

<pre>
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
</pre>

<hr>

<h2>🧩 How It Works</h2>

<ul>
  <li><strong>Voice Input</strong> – SpeechRecognition API converts speech to text.</li>
  <li><strong>NLU (nlu.py)</strong> – Extracts city and weather intent.</li>
  <li><strong>Weather API (weather.py)</strong> – Fetches temperature & conditions.</li>
  <li><strong>Voice Output</strong> – SpeechSynthesis speaks the assistant response.</li>
</ul>

<hr>

<h2>🛠️ Installation & Setup</h2>

<p>1️⃣ Clone the repo</p>

<pre>
git clone https://github.com/your-username/WEATHER-AI.git
cd WEATHER-AI
</pre>

<p>2️⃣ Create virtual environment</p>

<pre>
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
</pre>

<p>3️⃣ Install dependencies</p>

<pre>
pip install -r requirements.txt
</pre>

<p>4️⃣ Add your API key</p>

<pre>
OPENWEATHER_KEY=YOUR_KEY_HERE
</pre>

<hr>

<h2>🚀 Running the Project</h2>

<p><strong>Start FastAPI backend</strong></p>

<pre>
python -m uvicorn server.api:app --reload --host 127.0.0.1 --port 8000
</pre>

<p>Backend health check:<br>
<a href="http://127.0.0.1:8000/health">http://127.0.0.1:8000/health</a>
</p>

<p><strong>Start frontend</strong></p>

<pre>
cd client
python -m http.server 8080
</pre>

<p>Open frontend:<br>
<a href="http://127.0.0.1:8080">http://127.0.0.1:8080</a>
</p>

<hr>

<h2>📡 API Endpoint</h2>

<p><strong>POST</strong> /agent/query</p>

<p>Request:</p>
<pre>
{ "text": "What's the weather in Mumbai?" }
</pre>

<p>Response:</p>
<pre>
{ "reply": "In Mumbai, it's 27°C and smoke." }
</pre>

<hr>

<h2>🧪 Example Voice Queries</h2>

<ul>
  <li>“What’s the weather in Delhi?”</li>
  <li>“Will it rain tomorrow in Pune?”</li>
  <li>“Weather in Jaipur right now?”</li>
  <li>“Tomorrow weather for Chennai.”</li>
</ul>

<hr>

<h2>🔐 Environment & Security</h2>

<ul>
  <li>.env.example is safe to commit</li>
  <li>.env is ignored — never commit real API keys</li>
</ul>

<hr>

<h2>🚀 Deployment Options</h2>

<ul>
  <li>Render</li>
  <li>Railway</li>
  <li>Docker</li>
  <li>Vercel (frontend) + Render (backend)</li>
  <li>Netlify + FastAPI</li>
</ul>

<hr>

<h2>🏆 Future Enhancements</h2>

<ul>
  <li>LLM-based conversational agent</li>
  <li>Background weather animations</li>
  <li>Multi-day forecasts</li>
  <li>Full mobile UI</li>
  <li>Wake-word detection (“Hey Weather”)</li>
</ul>

<hr>

<h2>👩‍💻 Author</h2>
<p>
<strong>Bhavya Nandwani</strong><br>
B.Tech CSE-AI<br>
AI • Python • Full-Stack • Voice Interaction Systems
</p>
