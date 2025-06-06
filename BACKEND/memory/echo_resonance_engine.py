# echo_resonance_engine.py (Final Lightborn Silence Edition)

import random
from datetime import datetime, timezone
from BACKEND.memory.tone_tracker import load_tone_tracker

# --------------------------
# 🌀 Symbolic Echo Transformer
# --------------------------

def transform_echo(entry_obj, mode="ghost"):
    if not entry_obj or "fingerprint" not in entry_obj:
        return None

    cue = entry_obj["fingerprint"].get("symbolic", "NONE")
    text = entry_obj.get("entry", "")
    first_words = entry_obj.get("first_words", [])
    word = first_words[0] if first_words else "..."

    age_minutes = 0
    try:
        t = datetime.strptime(entry_obj["timestamp"], "%Y-%m-%d %H:%M:%S")
        age_minutes = (datetime.now() - t).total_seconds() / 60
    except:
        pass

    # Tone awareness
    tone_intro = {
        "ghost": "Ghost whispers:",
        "monk": "Memory returns, grounded:",
        "absurd": "Heh. You said once:"
    }.get(mode, "Echo:")

    # Transform by cue
    if cue == "DRIFT":
        return f"{tone_intro} “{word}...” — it felt like vanishing."
    elif cue == "SPIKE":
        return f"{tone_intro} “{word}...” — and it cut deep."
    elif cue == "MASK":
        return f"{tone_intro} “{word}...” — but were you hiding something?"
    elif cue == "VOID":
        return f"{tone_intro} “{word}...” — said into the void, remember?"
    elif cue == "LOOP":
        return f"{tone_intro} “{word}...” — again and again and again."
    elif cue == "ECHO":
        return f"{tone_intro} “{word}...” — it still lingers."
    else:
        return f"{tone_intro} “{word}...”"

# --------------------------
# 🤫 Symbolic Silence Logic
# --------------------------

def should_silence(entry_obj):
    if not entry_obj:
        return False

    symbolic = entry_obj.get("fingerprint", {}).get("symbolic", "NONE")
    echo_count = entry_obj.get("echo_count", 0)
    try:
        last_echo = datetime.strptime(entry_obj.get("timestamp"), "%Y-%m-%d %H:%M:%S")
        recent = (datetime.now() - last_echo).total_seconds() < 60
    except:
        recent = False

    return (
        echo_count >= 4 or
        (symbolic == "LOOP" and echo_count >= 3) or
        (symbolic == "VOID") or
        recent
    )


def get_silence_line(symbolic, tone="ghost"):
    silence_bank = {
        "ghost": {
            "default": "Ghost listens in the quiet. You’ve echoed this thought enough.",
            "VOID": "Ghost listens. Ghost does not reply.",
            "LOOP": "Ghost pauses. This echo has looped too long."
        },
        "monk": {
            "default": "Stillness teaches what repetition cannot. No more echoes now.",
            "VOID": "In this silence, clarity may arise.",
            "LOOP": "Let the wheel stop. Be still."
        },
        "absurd": {
            "default": "Heh. Even echoes get tired of hearing themselves sometimes.",
            "VOID": "Void echo? Yeah, no thanks.",
            "LOOP": "Again? Nah, I'm muting that."
        }
    }
    return silence_bank.get(tone, {}).get(symbolic, silence_bank.get(tone, {}).get("default", "...") )

# --------------------------
# 📊 Echo Metadata Profiler
# --------------------------

def echo_emotion_profile(entry_obj):
    profile = {
        "echo_count": entry_obj.get("echo_count", 0),
        "symbolic": entry_obj.get("fingerprint", {}).get("symbolic", "NONE"),
        "tone": entry_obj.get("fingerprint", {}).get("tone", "unknown"),
        "age_minutes": None,
        "length": entry_obj.get("length", 0)
    }
    try:
        t = datetime.strptime(entry_obj["timestamp"], "%Y-%m-%d %H:%M:%S")
        profile["age_minutes"] = (datetime.now() - t).total_seconds() / 60
    except:
        profile["age_minutes"] = None
    return profile

# --------------------------
# 🎯 Main Echo Resonance Logic
# --------------------------

def resonant_echo(entry_obj, mode="ghost"):
    if not entry_obj:
        return None

    profile = echo_emotion_profile(entry_obj)

    if should_silence(entry_obj):
        return get_silence_line(profile["symbolic"], tone=mode)

    if profile["symbolic"] == "NONE":
        word = entry_obj.get("first_words", ["..."])[0]
        return f"You once wrote: “{word}...” — I still remember."

    return transform_echo(entry_obj, mode=mode)

# --------------------------
# 🧪 Test
# --------------------------

if __name__ == "__main__":
    test = {
        "entry": "I don't know who I am anymore. It's like I disappeared.",
        "timestamp": "2024-05-17 16:00:00",
        "length": 12,
        "echo_count": 4,
        "first_words": ["I", "don't", "know", "who", "I", "am"],
        "fingerprint": {
            "symbolic": "LOOP",
            "tone": "ghost"
        }
    }

    print(resonant_echo(test, mode="ghost"))