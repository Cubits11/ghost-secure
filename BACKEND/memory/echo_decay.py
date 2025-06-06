# BACKEND/memory/echo_decay.py (Final Lightborn Edition)
# Unified Decay System — Tag-Based, Symbolic, Integrates with Ghost

import time
import json
import os

# 🌌 Tag-based emotional echo archive
# This archive represents Ghost's long-term symbolic memory
echo_memory = {
    "relapse": [
        {
            "text": "You didn’t fail. You paused.",
            "timestamp": time.time() - 86400 * 2,
            "weight": 1.0
        },
        {
            "text": "Still showing up. Even if it's slow.",
            "timestamp": time.time() - 86400 * 7,
            "weight": 1.0
        }
    ],
    "shame": [
        {
            "text": "You deserve quiet that doesn't judge you.",
            "timestamp": time.time() - 86400 * 1,
            "weight": 1.0
        }
    ],
    "shame_loop": []
}

# 🔗 Safe path for memory persistence
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DECAY_MEMORY_PATH = os.path.join(PROJECT_ROOT, "LOGS", "decayed_echo_memory.json")

# ⚙️ Decay algorithm: exponential fading by age
def apply_decay(echo, days_passed, decay_rate=0.1):
    return max(0, echo["weight"] * (1 - decay_rate) ** days_passed)

# 🔍 Viable echoes above threshold, ordered by weight
def get_viable_echoes(tag, threshold=0.3):
    now = time.time()
    viable = []
    if tag in echo_memory:
        for echo in echo_memory[tag]:
            days_old = (now - echo["timestamp"]) / 86400
            decayed_weight = apply_decay(echo, days_old)
            echo["weight"] = decayed_weight
            if decayed_weight >= threshold:
                viable.append((echo["text"], decayed_weight, days_old))
    return sorted(viable, key=lambda x: -x[1])

# 🎭 Rewording based on age and emotional distance
def symbolically_reword(text, age):
    if age > 7:
        return f"You once whispered: '{text}' — remember who you were back then."
    if age > 3:
        return f"You echoed before: '{text}' — still relevant."
    return text

# 🔁 Unified function: get best symbolic echo for a tag
def get_symbolic_echo_by_tag(tag):
    viable = get_viable_echoes(tag)
    if not viable:
        return None
    best_text, _, age = viable[0]
    return symbolically_reword(best_text, age)

# 📊 Echo decay state snapshot (for tracker/pressure overlays)
def decay_status_report():
    report = {}
    now = time.time()
    for tag, entries in echo_memory.items():
        active = 0
        faded = 0
        for e in entries:
            days_old = (now - e["timestamp"]) / 86400
            weight = apply_decay(e, days_old)
            if weight >= 0.3:
                active += 1
            else:
                faded += 1
        report[tag] = {"active": active, "faded": faded, "total": active + faded}
    return report

# 💾 Save/Load echo memory to disk
def save_memory(filepath=DECAY_MEMORY_PATH):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(echo_memory, f, indent=2)

def load_memory(filepath=DECAY_MEMORY_PATH):
    global echo_memory
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            echo_memory = json.load(f)

# 🧪 Dev testing block
if __name__ == "__main__":
    tags = ["relapse", "shame", "shame_loop"]
    for tag in tags:
        viable = get_viable_echoes(tag)
        if viable:
            age = viable[0][2]
            echo_line = symbolically_reword(viable[0][0], age)
            print(f"[{tag.upper()}] Echo: \"{echo_line}\" (weight {viable[0][1]:.2f})")
        else:
            print(f"[{tag.upper()}] No viable echoes. Silence holds.")
    print("\n-- Decay Report --")
    print(json.dumps(decay_status_report(), indent=2))
    save_memory()
