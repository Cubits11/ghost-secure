import os
import json
import ast

input_path = "LOGS/secure_echo_log.jsonl"
output_path = "LOGS/secure_echo_log_fixed.jsonl"

fixed = 0
skipped = 0

with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
    for idx, line in enumerate(infile, 1):
        line = line.strip()
        if not line:
            skipped += 1
            continue
        try:
            # Try to convert Python-style dict string to actual dict
            parsed = ast.literal_eval(line)
            # Dump back to valid JSON
            json_line = json.dumps(parsed)
            outfile.write(json_line + "\n")
            fixed += 1
        except Exception as e:
            print(f"⚠️  Skipping line {idx}: {e}")
            skipped += 1

print("\n✅ Fix Attempt Complete")
print(f"✔️  Converted Entries: {fixed}")
print(f"❌ Skipped Corrupted Lines: {skipped}")
print(f"📄 New file written to: {output_path}")