# BACKEND/core/secure_writer.py

import os
import json
import hashlib
from datetime import datetime

# 🔐 Set secure log file path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SECURE_LOG_PATH = os.path.join(PROJECT_ROOT, "LOGS", "secure_echo_log.jsonl")

# 📌 Append-only secure logger
def append_secure_log(entry_data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry_data["timestamp"] = timestamp

    # 🔑 Create SHA-256 hash of the entire record
    json_str = json.dumps(entry_data, sort_keys=True)
    entry_hash = hashlib.sha256(json_str.encode("utf-8")).hexdigest()
    entry_data["signature"] = entry_hash

    # ✍️ Append to log file (one JSON object per line)
    with open(SECURE_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry_data) + "\n")

    return entry_hash

# 🧪 Quick test entry (can be removed later)
if __name__ == "__main__":
    test_entry = {
        "entry": "I feel like I'm disappearing again.",
        "pulse": "FRACTURED",
        "tone": "ghost",
        "tag": "dissociation",
        "fingerprint": {
            "symbolic": "DRIFT",
            "fingerprint": "feel_disappear_again_TAG:dissociation_TONE:ghost_CUE:DRIFT"
        }
    }
    sig = append_secure_log(test_entry)
    print("🔏 Entry written with signature:", sig)
