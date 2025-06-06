# TOOLS/debug_missing_hashes.py

import json
from pathlib import Path

log_path = Path("LOGS") / "secure_echo_log_2025-06-03T11-45-12.jsonl"

with open(log_path, "r") as f:
    entries = [json.loads(line) for line in f]

no_hash = [e for e in entries if "hash" not in e]
print(f"🧪 Entries missing 'hash': {len(no_hash)} / {len(entries)}")

if no_hash:
    print("⚠️ These entries were never hashed. Consider rebuilding them.")
else:
    print("✅ All entries have hashes — likely tampering or hash mismatch issue.")