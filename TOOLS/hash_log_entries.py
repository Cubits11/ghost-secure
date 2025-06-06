# TOOLS/hash_log_entries.py

import hashlib
import json
import os

INPUT_PATH = "LOGS/secure_echo_log_fixed.jsonl"
OUTPUT_PATH = "LOGS/secure_echo_log_verified.jsonl"

def calculate_hash(entry):
    relevant = {
        "timestamp": entry["timestamp"],
        "entry": entry["entry"],
        "tone": entry["tone"],
        "tag": entry["tag"],
        "fingerprint": entry["fingerprint"]
    }
    raw = json.dumps(relevant, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

with open(INPUT_PATH, "r", encoding="utf-8") as infile, open(OUTPUT_PATH, "w", encoding="utf-8") as outfile:
    for line in infile:
        try:
            entry = json.loads(line)
            entry["hash"] = calculate_hash(entry)
            outfile.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"⚠️ Failed to process line: {e}")