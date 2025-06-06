# BACKEND/core/tone_flow_engine.py (Final Lightborn Edition)

import os
import json
from datetime import datetime
from BACKEND.memory.tone_tracker import load_tone_tracker, save_tone_tracker

# Resolve safe path for tone log
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOG_PATH = os.path.join(PROJECT_ROOT, "LOGS", "tone_flow.log")

# --------------------------
# 🔁 Tone Flow Decision Logic
# --------------------------
def decide_next_tone(current_tone, tag, echo_count, entry_time=None):
    now = datetime.now()
    tracker = load_tone_tracker()
    last_time = tracker.get("last_entry_time")
    tag_history = tracker.get("tag_history", [])

    # Time delta
    days_since = 0
    if last_time:
        try:
            last_time_dt = datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S")
            days_since = (now - last_time_dt).days
        except:
            days_since = 0

    # Update tag history
    tag_history.append(tag)
    if len(tag_history) > 5:
        tag_history = tag_history[-5:]

    # Tone transition logic (Phase 0.2 Matrix)
    new_tone = current_tone

    if current_tone == "ghost":
        if days_since > 7:
            new_tone = "monk"
        elif tag_history.count(tag) >= 3:
            new_tone = "monk"

    elif current_tone == "monk":
        if echo_count >= 3:
            new_tone = "absurd"
        elif days_since > 7:
            new_tone = "ghost"

    elif current_tone == "absurd":
        if "grief" in tag:
            new_tone = "ghost"
        elif echo_count >= 2:
            new_tone = "monk"

    # Update tracker state
    tracker.update({
        "last_entry_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "last_tone": new_tone,
        "tag_history": tag_history,
        "echo_pressure": echo_count
    })
    save_tone_tracker(tracker)

    return new_tone

# --------------------------
# 📜 Tone Transition Logger
# --------------------------
def log_tone_transition(entry_num, prev_tone, new_tone, tag, echo_count, reason):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = (
        f"[Entry #{entry_num}] Timestamp: {timestamp}\n"
        f"Previous Tone: {prev_tone}\n"
        f"Current Tone: {new_tone}\n"
        f"Tag Detected: {tag}\n"
        f"Echo Count: {echo_count}\n"
        f"Reason: {reason}\n"
        f"---\n"
    )
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(log_line)

# --------------------------
# 🧪 Manual Test
# --------------------------
if __name__ == "__main__":
    print(decide_next_tone("ghost", "grief", 2))
    print(decide_next_tone("monk", "fear", 3))
    print(decide_next_tone("absurd", "grief", 1))