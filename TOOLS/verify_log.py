import json
import hashlib
import os
import sys
from termcolor import cprint
from difflib import unified_diff

LOG_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join("LOGS", "secure_echo_log.jsonl")

def compute_hash(entry_dict):
    clean = {k: v for k, v in entry_dict.items() if k != "hash"}
    encoded = json.dumps(clean, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

def diff_entries(original, tampered):
    original_str = json.dumps(original, indent=2, sort_keys=True).splitlines()
    tampered_str = json.dumps(tampered, indent=2, sort_keys=True).splitlines()
    return list(unified_diff(original_str, tampered_str, fromfile="expected", tofile="found", lineterm=""))

def verify_secure_log():
    if not os.path.exists(LOG_PATH):
        cprint(f"❌ Log file not found: {LOG_PATH}", "red")
        return

    total = passed = failed = skipped = 0

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            total += 1
            line = line.strip()
            if not line:
                cprint(f"⚠️  Line {line_num} is empty.", "yellow")
                skipped += 1
                continue

            try:
                entry = json.loads(line)
                if not isinstance(entry, dict):
                    cprint(f"❌ Line {line_num} is not a JSON object.", "red")
                    failed += 1
                    continue

                stored_hash = entry.get("hash")
                if not stored_hash:
                    cprint(f"❌ Line {line_num} missing 'hash'.", "red")
                    failed += 1
                    continue

                expected_hash = compute_hash(entry)
                if stored_hash == expected_hash:
                    cprint(f"✅ Line {line_num} integrity verified.", "green")
                    passed += 1
                else:
                    cprint(f"❌ Line {line_num} hash mismatch.", "red")
                    failed += 1

                    # Show diff breakdown
                    expected_dict = {k: v for k, v in entry.items() if k != "hash"}
                    actual_hash = compute_hash(expected_dict)
                    diff = diff_entries(expected_dict, entry)
                    print("\n🔍 Diff Breakdown:")
                    for line in diff:
                        print(line)

            except Exception as e:
                cprint(f"❌ Line {line_num} malformed: {str(e)}", "red")
                failed += 1

    print("\n--- Log Integrity Report ---")
    cprint(f"Total Entries: {total}", "cyan")
    cprint(f"✅ Passed: {passed}", "green")
    cprint(f"❌ Failed: {failed}", "red")
    cprint(f"⚠️  Skipped: {skipped}", "yellow")

if __name__ == "__main__":
    verify_secure_log()