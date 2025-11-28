import os
from fastapi import FastAPI
from pydantic import BaseModel

from app.services.tone_engine import ToneRouter      # NEW
from app.services.safety_engine import SafetyEngine
from app.services.groq_response_builder import GroqResponseBuilder
from app.classifiers.emotion_classifier import EmotionClassifier
from app.classifiers.tone_classifier import ToneClassifier

app = FastAPI(title="SAVIO Backend (Groq Integrated)")

# Core modules
safety_engine = SafetyEngine()
router = ToneRouter()                                # NEW

# Groq response builder
response_builder = GroqResponseBuilder(api_key=os.getenv("GROQ_API_KEY"))

# Classifiers
emotion_clf = EmotionClassifier()
tone_clf = ToneClassifier()


# ---------- Request / Response Schemas ----------
class ChatRequest(BaseModel):
    user_id: str = "anon"
    message: str
    slider: float = 0.5
    context: dict = {}


class ChatResponse(BaseModel):
    tone: str
    text: str
    safety_flags: dict


# ---------- Health Check ----------
@app.get('/health')
def health():
    return {'status': 'ok'}


# ---------- Chat Endpoint ----------
@app.post('/chat', response_model=ChatResponse)
def chat(req: ChatRequest):

    # 1) Safety Pre-check
    safety_flags = safety_engine.quick_check(req.message)
    if safety_flags.get('hard_block'):
        return ChatResponse(
            tone="refusal",
            text="I can't help with that. If you're upset, I can support you in a safer way.",
            safety_flags=safety_flags
        )

    # 2) Emotion Classification
    emotion = emotion_clf.predict(req.message)

    # 3) Tone Classification (OLD classifier, still useful)
    classifier_tone = tone_clf.predict(req.message)

    # 4) NEW ROUTER — determines final tone
    chosen_tone = router.compute(
        classifier_tone=classifier_tone,
        slider=req.slider,
        emotion=emotion,
        message=req.message
    )

    # 5) Generate final response via Groq
    text, tone_used = response_builder.build(
        user_message=req.message,
        emotion=emotion,
        slider=req.slider,
        tone_override=chosen_tone,     # NEW
        file_url=None
    )

    # 6) Return final structured output
    return ChatResponse(
        tone=tone_used,
        text=text,
        safety_flags=safety_flags
    )
