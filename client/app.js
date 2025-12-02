const out = document.getElementById('out');
const btn = document.getElementById('rec');

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

const rec = new SpeechRecognition();
rec.lang = 'en-IN';
rec.interimResults = false;

rec.onresult = async (e) => {
  const text = e.results[0][0].transcript;
  out.textContent = "You: " + text + "\n";

  // Send to backend
  const res = await fetch("http://127.0.0.1:8000/agent/query", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ text }),
  });

  const json = await res.json();
  out.textContent += "Agent: " + json.reply;

  // Speak the answer
  speechSynthesis.speak(new SpeechSynthesisUtterance(json.reply));
};

btn.onclick = () => rec.start();
