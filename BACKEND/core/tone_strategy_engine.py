# BACKEND/core/tone_strategy_engine.py (Final Lightborn Edition)
# Phase 0.2–0.3: Dynamic Tone Selector + Multi-Tag Strategy Router

import time
import json
import os

# 🔐 Safe path resolution
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DNA_PATH = os.path.join(PROJECT_ROOT, "content", "dna_bank.json")
TONE_TRACKER_PATH = os.path.join(PROJECT_ROOT, "LOGS", "tone_tracker.json")

# Load DNA bank
with open(DNA_PATH, "r", encoding="utf-8") as f:
    DNA = json.load(f)

# Load tone flow memory tracker
if os.path.exists(TONE_TRACKER_PATH):
    with open(TONE_TRACKER_PATH, "r", encoding="utf-8") as f:
        TONE_TRACKER = json.load(f)
else:
    TONE_TRACKER = {}

def save_tone_tracker():
    with open(TONE_TRACKER_PATH, "w", encoding="utf-8") as f:
        json.dump(TONE_TRACKER, f, indent=2)

def prioritize_tags(tags):
    priority_order = {
        "grief": 5, "rage": 4, "shame": 3, "fear": 3,
        "hope": 2, "solitude": 2, "identity": 1, "loner": 1
    }
    return sorted(tags, key=lambda t: -priority_order.get(t, 0))

def find_dna_match(tag):
    for entry in DNA:
        if tag in entry["emotional_tags"]:
            return entry
    return None

def resolve_tone_flow(user_id, tags, pulse, echo_count=0):
    last_state = TONE_TRACKER.get(user_id, {"tone": "ghost", "timestamp": 0})
    last_tone = last_state["tone"]
    last_time = last_state["timestamp"]
    now = time.time()
    delta_days = (now - last_time) / 86400

    top_tag = prioritize_tags(tags)[0]
    match = find_dna_match(top_tag)

    if last_tone == "ghost" and delta_days > 7:
        new_tone = "monk"
    elif last_tone == "absurd" and "grief" in tags:
        new_tone = "ghost"
    elif echo_count > 2:
        new_tone = "monk"
    elif match:
        new_tone = match["default_tone"]
    else:
        new_tone = last_tone

    TONE_TRACKER[user_id] = {
        "tone": new_tone,
        "timestamp": now,
        "pulse": pulse,
        "tags": tags
    }
    save_tone_tracker()

    return new_tone, match["strategies"] if match else ["anchor"]

def get_strategy_routing(tags, echo_count=0, user_id="default", pulse="UNKNOWN"):
    """
    Main interface: returns tone + strategy list for Ghost response logic
    """
    tone, strategy_list = resolve_tone_flow(user_id, tags, pulse, echo_count)
    return {
        "tone": tone,
        "strategies": strategy_list,
        "tag_priority": prioritize_tags(tags)
    }
