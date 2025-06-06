# TOOLS/print_broken_log.py

input_path = "LOGS/secure_echo_log.jsonl"

with open(input_path, "r", encoding="utf-8") as infile:
    for idx, line in enumerate(infile, 1):
        print(f"\n--- Line {idx} ---")
        print(line.strip())