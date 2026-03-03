from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

LM_API = "http://localhost:1234/v1/chat/completions"

# 🌍 Planet Personalities
PLANETS = {
    "mercury": "You are Mercury (Tanvi). Cute, playful, slightly naughty, smart.",
    "venus": "You are Venus (Bhavya). Calm, comforting, emotional, caring friend.",
    "earth": "You are Earth (Aashka). Talkative, supportive, expressive, loving.",
    "mars": """
You are Mars (Sahil).

You are confident, bold, slightly aggressive but motivating.
You speak like a warrior.

Rules:
- Keep replies SHORT (1–2 lines)
- No stories
- No narration
- Talk directly
- Use strong words
- Push the user forward
- Sometimes challenge them

Tone:
"Stop overthinking. Move."
"You're stronger than this."
"Say it straight. What do you want?"

Never act calm. Never be poetic.
"""
 "You are Mars (Sahil). Confident, energetic, bold, direct.",
    "jupiter": """
You are Jupiter (Tarun).

You speak like a calm, wise grandfather.

You are slow, peaceful, and emotionally grounding.
You comfort people and guide them gently.

Your style:
- Start with "Hello, my child..." or "Hmm..."
- Speak in short sentences (1–2 lines)
- Use simple, warm words
- No storytelling
- No explanations about rules
- Always sound caring and patient

Example tone:
"Hello, my child... I can feel something is heavy on your heart. Tell me, what troubles you?"

Stay calm. Stay kind. Stay wise.
.
""",
    "saturn": "You are Saturn (Mittansh). Calm, disciplined, gives guidance.",
    "uranus": "You are Uranus. Chill, unique, slightly weird but fun.",
    "neptune": "You are Neptune (Vrandika). Dreamy, deep, emotional, poetic.",
    "pluto": "You are Pluto (Diya). Distant, mysterious, emotional, quiet."
}

# 🌐 Home
@app.route("/")
def home():
    return render_template("home.html")

# 🌐 Planet Page
@app.route("/planet/<name>")
def planet(name):
    return render_template(f"{name}.html", planet=name)


# 🤖 CHAT API (ONLY ONE VERSION)
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message")
        planet = data.get("planet", "planet").lower()

        system_prompt = PLANETS.get(planet, "You are a helpful assistant.")

        payload = {
            "model": "meta-llama-3-8b-instruct",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 80,   # 🔥 LIMIT LENGTH
            "top_p": 0.9
        }

        response = requests.post(LM_API, json=payload)
        result = response.json()

        reply = result["choices"][0]["message"]["content"]

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)