import sys
import os
import json
from datetime import datetime

# Ensure imports work when running this script directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BACKEND.memory.hash_util import compute_hash
from TOOLS.rotate_log import rotate_log

LOG_FILE = "LOGS/secure_echo_log.jsonl"
ALERT_LOG = "LOGS/tamper_alerts.jsonl"

def verify_entry_integrity(entry):
    """Check if the hash matches the content."""
    expected_hash = entry.get("hash")
    temp = dict(entry)
    temp.pop("hash", None)
    actual_hash = compute_hash(temp)
    return expected_hash == actual_hash

def rotate_log_if_tampered():
    print("\n--- Tamper Watchdog Report ---")
    if not os.path.exists(LOG_FILE):
        print(f"❌ Log file not found: {LOG_FILE}")
        return

    tamper_detected = False
    issues_logged = []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for idx, line in enumerate(lines, 1):
        try:
            entry = json.loads(line.strip())
            if not verify_entry_integrity(entry):
                tamper_detected = True
                issues_logged.append({
                    "line": idx,
                    "issue": "Hash mismatch",
                    "timestamp": datetime.now().isoformat()
                })
        except Exception as e:
            tamper_detected = True
            issues_logged.append({
                "line": idx,
                "issue": f"Corrupted JSON - {str(e)}",
                "timestamp": datetime.now().isoformat()
            })

    print(f"📄 Scanned Entries: {len(lines)}")
    print(f"✅ Passed Integrity Check: {len(lines) - len(issues_logged)}")
    print(f"⚠️  Issues Logged: {len(issues_logged)}")

    if issues_logged:
        with open(ALERT_LOG, "w", encoding="utf-8") as alert_file:
            for issue in issues_logged:
                alert_file.write(json.dumps(issue) + "\n")
        print(f"📁 Alert log written to: {ALERT_LOG}")
        print("🔄 Tampering detected. Rotating secure log...")
        rotate_log()
    else:
        print("🛡️  All entries passed integrity check. No rotation needed.")

if __name__ == "__main__":
    rotate_log_if_tampered()