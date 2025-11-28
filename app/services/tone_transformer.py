class ToneTransformer:
    def to_surge(self, meaning):
        emotion = meaning["emotion"]
        topic = meaning["topic"]

        if emotion == "shock":
            return f"BROOO— WHAT WAS THAT CHAOTIC PLOT TWIST 💀😭🔥"
        if emotion == "stress":
            return f"BROOO— life really said *hold this L* today 😭🔥"
        if emotion == "anger":
            return f"NAH THAT'S WILD— who even does that 💀🔥"
        return "BROOO— this whole situation is actually insane 💀🔥"

    def to_mid_surge(self, meaning):
        emotion = meaning["emotion"]

        if emotion == "shock":
            return "Okay wait—how did it escalate THAT fast?? 😭"
        if emotion == "stress":
            return "Hold up—this is messy but we can fix it."
        if emotion == "anger":
            return "Yeah that’s definitely annoying. Let’s break it down."
        return "Alright, something is off here. Let me check."

    def to_light_surge(self, meaning):
        return "Yeah that’s kinda wild ngl, but we’ll handle it."

    def to_neutral(self, meaning):
        return "Alright, let’s go through what happened calmly."

    def to_synth(self, meaning):
        emotion = meaning["emotion"]

        if emotion == "stress":
            return "Hey… slow down for a sec. That sounded like a lot to handle."
        if emotion == "sad":
            return "I’m really sorry you’re feeling that way. I’m here with you."
        return "Let’s take a slow moment and look at what’s going on."

    def to_crisis(self, meaning):
        return "I’m here with you. You’re not alone right now."
