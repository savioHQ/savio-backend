# Placeholder ToneClassifier wrapper
class ToneClassifier:
    def __init__(self):
        pass

    def predict(self, text: str) -> str:
        t = text.lower()
        if any(x in t for x in ['bro','lol','ngl','wtf']):
            return 'surge'
        if any(x in t for x in ['annoy','irritat','ugh','tired']):
            return 'light_surge'
        return 'neutral'
