# TOOLS/echo_summary.py

import os
import sys
import json
from collections import Counter

# Add project root to system path for import resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Try importing export_archive from echo_memory
try:
    from BACKEND.memory.echo_memory import export_archive
except ImportError as e:
    print("❌ Failed to import echo_memory module.")
    print(f"Error: {e}")
    sys.exit(1)

def summarize_echo_log():
    try:
        archive = export_archive()
    except Exception as e:
        print("❌ Failed to load echo memory archive.")
        print(f"Error: {e}")
        return

    if not archive or not isinstance(archive, dict):
        print("⚠️  Echo archive is empty or malformed.")
        return

    pulse_summary = {}
    cue_counter = Counter()
    total_entries = 0

    for pulse, tone_dict in archive.items():
        pulse_summary[pulse] = {}
        for tone, entries in tone_dict.items():
            if not isinstance(entries, list):
                continue
            count = len(entries)
            pulse_summary[pulse][tone] = count
            total_entries += count
            for e in entries:
                cue = e.get("fingerprint", {}).get("symbolic", "NONE")
                cue_counter[cue] += 1

    print("\n🧠 Echo Memory Summary")
    print("----------------------")
    print(f"Total Entries: {total_entries}\n")

    for pulse, tones in pulse_summary.items():
        print(f"🌀 Pulse: {pulse}")
        for tone, count in tones.items():
            print(f"  🎭 Tone '{tone}': {count} entries")
        print()

    print("🔍 Top Symbolic Cues")
    print("----------------------")
    for cue, count in cue_counter.most_common(5):
        print(f"  {cue}: {count}")

if __name__ == "__main__":
    summarize_echo_log()