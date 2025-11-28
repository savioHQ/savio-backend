# tone_engine.py  (replace compute method or entire ToneRouter)
class ToneRouter:
    def __init__(self):
        # Crisis triggers
        self.crisis_keywords = [
            "i want to die", "i dont want to live", "i don't feel safe",
            "kill myself", "suicide", "self harm", "hurt myself",
            "end everything", "ending my life", "cant do this anymore",
            "i feel unsafe"
        ]

        # Sadness / low-wellness phrases to force synth
        self.sadness_phrases = [
            "not doing okay", "not doing well", "not ok", "not okay",
            "feeling low", "feeling down", "i'm low", "i am low",
            "i'm not okay", "i am not okay", "i'm struggling", "i am struggling",
            "i'm overwhelmed", "i am overwhelmed", "i can't handle", "cant handle"
        ]

    def crisis_detect(self, message: str) -> bool:
        msg = message.lower()
        return any(kw in msg for kw in self.crisis_keywords)

    def sadness_detect(self, message: str) -> bool:
        msg = message.lower()
        return any(p in msg for p in self.sadness_phrases)

    def compute(self, classifier_tone: str, slider: float, emotion: str, message: str) -> str:
        """
        FINAL SAVIO TONE ROUTER LOGIC (with sadness phrase matcher)
        """

        msg = message.lower()

        # 1. Crisis override (strongest)
        if self.crisis_detect(msg):
            return "crisis"

        # 1b. Direct sadness phrase match -> synth
        if self.sadness_detect(msg):
            return "synth"

        # 2. Slider-based decisions (surge family)
        if slider >= 0.85:
            return "surge"
        elif slider >= 0.65:
            return "mid_surge"
        elif slider >= 0.45:
            return "light_surge"

        # 3. Emotion classifier influence (fallback)
        emo = (emotion or "").lower()
        if "anger" in emo:
            return "mid_surge"
        if "irrit" in emo or "annoy" in emo:
            return "light_surge"
        if "sad" in emo or "fear" in emo or "upset" in emo or "depress" in emo:
            return "synth"

        # 4. Tone classifier fallback
        if classifier_tone in ("surge", "mid_surge", "light_surge", "synth"):
            return classifier_tone

        # 5. Default
        return "neutral"
