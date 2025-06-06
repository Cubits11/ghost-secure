# BACKEND/memory/tone_tracker.py (Final Lightborn Edition)

import os
import json

# 🔐 Use project root-safe absolute path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TONE_TRACKER_PATH = os.path.join(PROJECT_ROOT, "BACKEND", "memory", "tone_tracker.json")

def load_tone_tracker():
    if not os.path.exists(TONE_TRACKER_PATH):
        return {
            "last_entry_time": None,
            "last_tone": "ghost",
            "tag_history": [],
            "echo_pressure": 0
        }
    try:
        with open(TONE_TRACKER_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {
            "last_entry_time": None,
            "last_tone": "ghost",
            "tag_history": [],
            "echo_pressure": 0
        }

def save_tone_tracker(data):
    with open(TONE_TRACKER_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)