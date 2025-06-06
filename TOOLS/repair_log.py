# TOOLS/repair_log.py

import os
import json
import sys
from datetime import datetime

input_path = os.path.join("LOGS", "secure_echo_log.jsonl")
output_path = os.path.join("LOGS", "secure_echo_log_repaired.jsonl")

def is_valid_json(line):
    try:
        obj = json.loads(line)
        return isinstance(obj, dict)
    except json.JSONDecodeError:
        return False

def try_partial_repair(line):
    try:
        # Attempt to fix Python-style dicts or single quotes
        line = line.replace("'", '"')
        line = line.replace("...", '"placeholder"')
        line = line.replace("{ ... }", '{"placeholder": "value"}')
        obj = json.loads(line)
        obj["repaired"] = True
        obj["repair_reason"] = "Converted malformed quotes or placeholder symbols"
        obj["repair_timestamp"] = datetime.now().isoformat()
        return obj
    except:
        return None

def repair_log():
    if not os.path.exists(input_path):
        print(f"❌ Input file not found: {input_path}")
        return

    repaired = 0
    skipped = 0

    with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
        for idx, line in enumerate(infile, 1):
            line = line.strip()
            if not line:
                print(f"⚠️  Skipping line {idx}: Empty")
                skipped += 1
                continue

            if is_valid_json(line):
                outfile.write(line + "\n")
                repaired += 1
            else:
                fixed = try_partial_repair(line)
                if fixed:
                    outfile.write(json.dumps(fixed) + "\n")
                    repaired += 1
                else:
                    print(f"⚠️  Skipping line {idx}: Unfixable JSON")
                    skipped += 1

    print("\n🛠️  Log Repair Complete")
    print(f"✅ Repaired Entries: {repaired}")
    print(f"❌ Skipped Corrupted Lines: {skipped}")
    print(f"📄 Output written to: {output_path}")

if __name__ == "__main__":
    repair_log()