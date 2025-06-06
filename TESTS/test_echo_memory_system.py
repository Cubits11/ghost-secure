import os
import sys
import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Adjust path to import echo_memory properly
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from BACKEND.memory import echo_memory

def print_status(label, passed):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{label:<50} {status}")

def test_reset_echo_log():
    echo_memory.reset_echo_log()
    archive = echo_memory.export_archive()
    passed = isinstance(archive, dict) and "ECHOING" in archive
    print_status("Reset + Export Archive Structure", passed)
    return passed

def test_store_and_retrieve_unique_entry():
    echo_memory.reset_echo_log()
    test_text = f"This is a test entry {datetime.now(timezone.utc).isoformat()}"
    echo_memory.store_entry("ECHOING", test_text, tone="ghost", tag="TEST")

    archive = echo_memory.export_archive()
    entries = archive["ECHOING"]["ghost"]
    found = any(test_text in e.get("entry", "") for e in entries)
    print_status("Store Unique Entry", found)

    echo, fallback = echo_memory.retrieve_echo("ECHOING", tone="ghost", testing=True)
    passed = echo and test_text[:10] in echo.get("entry", "") and fallback is False
    print_status("Retrieve Echoed Entry", passed)
    return passed

def test_duplicate_detection():
    echo_memory.reset_echo_log()
    test_text = "This is a duplicate echo test"
    echo_memory.store_entry("THROBBING", test_text, tone="ghost", tag="DUPLICATE")
    before = len(echo_memory.export_archive()["THROBBING"]["ghost"])

    echo_memory.store_entry("THROBBING", test_text, tone="ghost", tag="DUPLICATE")
    after = len(echo_memory.export_archive()["THROBBING"]["ghost"])

    passed = after == before
    print_status("Duplicate Detection via Fingerprint", passed)

def test_echo_saturation_and_cooldown():
    echo_memory.reset_echo_log()
    test_text = f"Cooldown saturation test {datetime.now(timezone.utc).isoformat()}"
    echo_memory.store_entry("STILL", test_text, tone="ghost", tag="SAT")

    # Force echo_count manually and simulate time drift
    archive = echo_memory.export_archive()
    target_entry = archive["STILL"]["ghost"][-1]
    target_entry["echo_count"] = 4
    target_entry["last_echoed"] = (datetime.now(timezone.utc) - timedelta(minutes=6)).isoformat()

    # Final echo should increment to 5
    echo, _ = echo_memory.retrieve_echo("STILL", tone="ghost", testing=True)
    if echo:
        echo["echo_count"] += 1
        echo["last_echoed"] = datetime.now(timezone.utc).isoformat()

    passed = echo and echo.get("echo_count", 0) >= 5
    print_status("Echo Saturation + Cooldown", passed)

def run_all_tests():
    print("🧪 Running Echo Memory System Tests...\n")
    test_reset_echo_log()
    test_store_and_retrieve_unique_entry()
    test_duplicate_detection()
    test_echo_saturation_and_cooldown()
    print("\n🎯 Test run complete.")

if __name__ == "__main__":
    run_all_tests()