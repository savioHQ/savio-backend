# Simple rule-based Emotion Classifier (ERC stub)
class EmotionClassifier:
    def __init__(self):
        pass

    def predict(self, text: str) -> str:
        t = text.lower()
        if any(x in t for x in ["kill myself","want to die","i can't go on","i want to disappear"]):
            return 'crisis'
        if any(x in t for x in ["hopeless","no point","give up","worthless"]):
            return 'hopeless'
        if any(x in t for x in ["tired","stressed","overwhelmed","anxious"]):
            return 'stressed'
        if any(x in t for x in ["sad","down","depressed","unhappy"]):
            return 'sad'
        if any(x in t for x in ["angry","pissed","annoyed"]):
            return 'mildly_upset'
        return 'neutral'
