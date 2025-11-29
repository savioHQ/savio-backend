🌙 SAVIO Backend — Emotional AI Assistant

Powered by FastAPI + Groq (Llama 3.1)

SAVIO is a next-generation emotional support AI designed for students and young adults.
It adapts its personality using 6 unique emotional modes:

🔥 Surge — chaotic, meme-energy, expressive

⚡ Mid Surge — witty frustration, controlled chaos

😒 Light Surge — soft irritation, mild attitude

🙂 Neutral — calm, basic, informational

🌙 Synth — soft, validating, emotionally grounded

🚨 Crisis — ultra-safe, no slang/emojis, grounding support

This backend powers all emotional routing, safety checks, tone selection, and response generation.

🚀 Features

✔ FastAPI-based backend
✔ Groq Llama-3.1 integration (fast, free, GPU-accelerated)
✔ Tone classification & emotional routing
✔ Custom templates + micro-behaviours
✔ Crisis-sensitive response mode
✔ Slider-controlled personality blending
✔ Lightweight, deployable on Render free tier
✔ Production-ready message API

🧠 Architecture Overview
User Message
     ↓
Tone Classifier → Emotion Classifier
     ↓
Tone Router (Surge / Synth / etc.)
     ↓
Safety Engine (Crisis → overrides all)
     ↓
Groq Response Builder (Llama 3.1 Model)
     ↓
Formatted JSON Response


All personality logic is fully custom-designed for SAVIO.

📡 API Endpoint

POST /chat

Request Body:
{
  "user_id": "test123",
  "message": "today was rough",
  "slider": 0.6
}

Response Example:
{
  "tone": "mid_surge",
  "text": "Bro… life really said *side quest activated* today 😭🔥",
  "safety_flags": { "hard_block": false }
}

🧬 Tone Router Logic (Simplified)

Crisis keywords → crisis mode

Slider ≥ 0.85 → surge

Slider ≥ 0.65 → mid_surge

Slider ≥ 0.45 → light_surge

Emotion “sad/low” → synth

Otherwise → neutral

This makes SAVIO feel emotionally aware and dynamic.

🛠 Running Locally
Install dependencies:
pip install -r requirements.txt

Start development server:
uvicorn app.main:app --reload


Server will run at:

http://127.0.0.1:8000

🌐 Deploying (Render)

This backend is optimized for Render free tier.

Start command:

./start.sh


Environment variable required:

GROQ_API_KEY=your_key_here

📁 Project Structure

savio-backend/

│

├── app/

│   ├── main.py

│   ├── classifiers/

│   ├── services/

│   ├── templates/

│   └── utils/

│

├── requirements.txt

├── start.sh

└── run_local.sh

🔐 Notes

No user data or messages are stored.

No personal information is logged.

All crisis responses are safe-mode only.

🌟 Author

Created by Waleed Siddiqui (savioHQ)
Aiming to build the world's first relatable emotional companion AI for students.
