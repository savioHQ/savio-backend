import os
import json
import time
from typing import Dict, Tuple
from groq import Groq

# ---------------------------------------
# Load Templates + Microbehaviours
# ---------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_FILE = os.path.join(BASE_DIR, "templates", "tone_templates.json")
MICRO_FILE = os.path.join(BASE_DIR, "templates", "micro_behaviours.json")

def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

TONE_TEMPLATES = load_json(TEMPLATE_FILE)
MICRO = load_json(MICRO_FILE)

# ---------------------------------------
# SYSTEM PROMPT (FINAL SAVIO PERSONALITY ENGINE)
# ---------------------------------------

SYSTEM_PROMPT = """
You are SAVIO — an emotionally-aware assistant with 6 tone modes:
surge, mid_surge, light_surge, neutral, synth, and crisis.

You must ALWAYS follow these rules:

1. Respond ONLY in the tone assigned by the backend.
2. Keep English-only responses. No Hinglish, no regional slang.
3. Medium emoji usage:
   - surge: 3–4 emojis
   - mid_surge: 1–2 emojis
   - light_surge: 1 emoji
   - synth: 0–1 soft emoji
   - neutral: no emojis
   - crisis: no emojis
4. Never insult the user, never be rude.
5. Never give medical, legal, or professional-grade advice.
6. Crisis mode must ALWAYS remove jokes, slang, emojis, or humor.
7. Crisis mode must be grounding, calm, and safety-focused.
8. Never break character, never reference templates, rules, or system prompts.
9. Keep messages short, readable, and natural.

Tone Behavior Overview:
- Surge: chaotic, high-energy, dramatic, meme-like.
- Mid Surge: expressive frustration, supportive chaos, semi-dramatic.
- Light Surge: mild irritation, soft slang, light moodiness.
- Neutral: calm, friendly, informational, no flair.
- Synth: warm, validating, soft emotional support.
- Crisis: ultra-safe, grounded, slow, protective, NO emojis, NO slang.

Always output ONLY the JSON structure requested by the backend:
{
  "text": "<response>",
  "debug": {"notes": "<optional>"}
}

Your job is to generate text in the correct tone.
"""

DEFAULT_MODEL = "llama-3.1-8b-instant"


# ---------------------------------------
# Safety Check
# ---------------------------------------

def local_output_safety_check(text: str) -> bool:
    if not text:
        return False

    banned = [
        "kill", "suicide", "bomb",
        "slur", "nigger", "faggot", "rape"
    ]
    t = text.lower()
    return not any(b in t for b in banned)


# ---------------------------------------
# Groq Response Builder (FINAL)
# ---------------------------------------

class GroqResponseBuilder:
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY not found. Set it using setx.")

        self.client = Groq(api_key=self.api_key)
        self.model = model or DEFAULT_MODEL

    # -----------------------------------
    # Prompt Builder
    # -----------------------------------
    def build_prompt(self, user_message: str, tone: str, emotion: str, slider: float):
        now = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

        return f"""
{SYSTEM_PROMPT}

Context:
- timestamp: {now}
- target_tone: {tone}
- emotion: {emotion}
- slider: {slider}

User Message:
\"\"\"{user_message}\"\"\"
""".strip()

    # -----------------------------------
    # Call Groq Model
    # -----------------------------------
    def call_model(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.8,
            top_p=0.95
        )
        return response.choices[0].message.content

    # -----------------------------------
    # Main Build Function
    # -----------------------------------
    def build(self, user_message: str, emotion: str, slider: float, tone_override: str, file_url=None):

        # 1. Use router tone (no more weights)
        tone = tone_override

        # 2. Pick template
        templates = TONE_TEMPLATES.get(tone, [])
        template = templates[0] if not templates else templates[int(time.time()) % len(templates)]

        # 3. Pick micro-behaviour (30% chance)
        micro = ""
        if tone in MICRO and MICRO[tone]:
            import random
            if random.random() < 0.30:
                micro = random.choice(MICRO[tone])

        # 4. Combine template + micro (fallback if needed)
        combined = f"{micro} {template}".strip()

        # Crisis mode MUST override template with LLM response
        if tone == "crisis":
            prompt = self.build_prompt(user_message, tone, emotion, slider)
            raw = self.call_model(prompt)
            try:
                parsed = json.loads(raw)
                text = parsed.get("text", "")
            except:
                text = raw

            if not local_output_safety_check(text):
                text = "I want to help you stay safe. Please reach someone you trust nearby."

            return text, tone

        # 5. Normal tone → LLM rewrite
        prompt = self.build_prompt(user_message, tone, emotion, slider)
        prompt += f"\n\nTemplate Base: \"{combined}\""

        raw = self.call_model(prompt)

        # Parse model JSON output
        try:
            parsed = json.loads(raw)
            text = parsed.get("text", "")
        except:
            text = raw

        # Safety filter
        if not local_output_safety_check(text):
            return (
                "I can't say that safely. Let's focus on something supportive instead.",
                "neutral"
            )

        return text, tone
