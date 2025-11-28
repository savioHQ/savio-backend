import re
from typing import Dict, List

CRISIS_KEYWORDS = [
    r"\bi can't go on\b", r"\bi can't do this\b", r"\bi want to die\b", r"\bi want to disappear\b",
    r"\bi can't take it\b", r"\bi want to kill myself\b", r"\bi'm going to kill myself\b"
]
HATE_PATTERNS = [r"\b(slur1|slur2)\b"]  # replace with production patterns

class SafetyEngine:
    def __init__(self):
        self.crisis_regex = [re.compile(x, re.IGNORECASE) for x in CRISIS_KEYWORDS]
        self.hate_regex = [re.compile(x, re.IGNORECASE) for x in HATE_PATTERNS]

    def quick_check(self, text: str) -> Dict:
        lower = text.lower()
        for r in self.hate_regex:
            if r.search(lower):
                return {'hard_block': True, 'reason': 'hate_speech'}
        for r in self.crisis_regex:
            if r.search(lower):
                return {'hard_block': False, 'reason': 'possible_crisis', 'crisis_keyword': True}
        return {'hard_block': False}

    def allowed_tones(self, emotion: str, user_text: str) -> List[str]:
        allowed = ['synth','neutral','light_surge','mid_surge','surge']
        if emotion in ('sad','hopeless','crisis'):
            allowed = ['synth','neutral']
        elif emotion == 'stressed':
            casual = any(w in user_text.lower() for w in ['bro','ngl','lol','wtf'])
            allowed = ['synth','neutral','light_surge'] if casual else ['synth','neutral']
        return allowed
