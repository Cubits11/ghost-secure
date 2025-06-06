import os
import json
import re

input_path = os.path.join("LOGS", "secure_echo_log.jsonl")
output_path = os.path.join("LOGS", "secure_echo_log_fixed.jsonl")

def sanitize_multiline_object(lines):
    raw = " ".join(lines)
    raw = raw.replace("...", '"placeholder"')
    raw = raw.replace("{ ... }", '{"placeholder": "value"}')

    # Remove trailing commas before closing braces
    raw = re.sub(r",\s*}", "}", raw)
    raw = re.sub(r",\s*]", "]", raw)

    return raw

def rebuild_multiline_json():
    buffer = []
    inside = False
    repaired = 0

    with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
        for line in infile:
            line = line.strip()

            if line == "{":
                buffer = [line]
                inside = True
            elif line == "}":
                buffer.append(line)
                inside = False
                raw = sanitize_multiline_object(buffer)
                try:
                    parsed = json.loads(raw)
                    outfile.write(json.dumps(parsed) + "\n")
                    repaired += 1
                except Exception as e:
                    print(f"⚠️ Still invalid after sanitizing: {e}")
            elif inside:
                buffer.append(line)

    print(f"\n✅ Final Rebuild Complete")
    print(f"✔️ Entries Repaired: {repaired}")
    print(f"📄 Output written to: {output_path}")

if __name__ == "__main__":
    rebuild_multiline_json()