import random, json, os

from app.utils.meaning_extractor import MeaningExtractor
from app.services.tone_transformer import ToneTransformer

BASE = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_PATH = os.path.join(BASE, 'templates', 'tone_templates.json')
MICRO_PATH = os.path.join(BASE, 'templates', 'micro_behaviours.json')

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

TEMPLATES = load_json(TEMPLATES_PATH)
MICROS = load_json(MICRO_PATH)


class ResponseBuilder:
    def __init__(self):
        self.extractor = MeaningExtractor()
        self.transform = ToneTransformer()

    def pick_tone_from_weights(self, weights):
        sorted_tones = sorted(weights.items(), key=lambda kv: kv[1], reverse=True)
        return sorted_tones[0][0]

    def build(self, user_text: str, weights: dict, emotion: str):
        # 1. Pick tone based on weights
        tone = self.pick_tone_from_weights(weights)

        # 2. Extract meaning from the user message
        meaning = self.extractor.extract(user_text)

        # 3. Generate tone-styled rewrite based on meaning
        if tone == "surge":
            core = self.transform.to_surge(meaning)
        elif tone == "mid_surge":
            core = self.transform.to_mid_surge(meaning)
        elif tone == "light_surge":
            core = self.transform.to_light_surge(meaning)
        elif tone == "neutral":
            core = self.transform.to_neutral(meaning)
        elif tone == "synth":
            core = self.transform.to_synth(meaning)
        elif tone == "crisis":
            core = self.transform.to_crisis(meaning)
        else:
            core = "Let's take a look at that."

        # 4. Optional micro-behaviour
        micro = ""
        if tone in ("surge", "mid_surge", "light_surge"):
            if random.random() < 0.35:
                micro = random.choice(MICROS.get(tone, []))

        # 5. Final response assembly
        final = f"{micro} {core}".strip()
        return final, tone

    def refuse(self, user_text: str, mode='hard_block'):
        if mode == 'hard_block':
            return "I can't help with that. If you're upset, I can help in a safer way."
        return "I can't respond to that."


