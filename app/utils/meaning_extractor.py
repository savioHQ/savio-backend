import re

class MeaningExtractor:
    def __init__(self):
        # keyword groups
        self.shock_words = ["what happened", "wtf", "bro what", "how did", "no way", "omg"]
        self.anger_words = ["annoying", "pissed", "angry", "irritating", "hate"]
        self.sad_words = ["sad", "upset", "down", "hopeless"]
        self.stress_words = ["stress", "tired", "exhausted", "overwhelmed"]
        self.surprise_words = ["wait", "hold up", "no shot", "seriously"]

    def extract(self, text: str):
        t = text.lower()

        emotion = "neutral"
        topic = None

        if any(w in t for w in self.shock_words):
            emotion = "shock"
        elif any(w in t for w in self.anger_words):
            emotion = "anger"
        elif any(w in t for w in self.sad_words):
            emotion = "sad"
        elif any(w in t for w in self.stress_words):
            emotion = "stress"
        elif any(w in t for w in self.surprise_words):
            emotion = "surprise"

        # extract rough keyword/topic
        words = re.findall(r"[a-zA-Z]+", t)
        keywords = [w for w in words if len(w) > 3]
        topic = keywords[-1] if keywords else None

        return {
            "emotion": emotion,
            "topic": topic
        }
