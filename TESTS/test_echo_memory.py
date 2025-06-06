print("🧪 Running Echo Memory Tests...")

import unittest
import sys, os, json
from uuid import UUID
from datetime import datetime, timedelta

# Setup import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from BACKEND.memory.echo_memory import (
    store_entry,
    retrieve_echo,
    reset_echo_log,
    export_archive,
    compute_secure_hash,
    verify_integrity,
    LOG_PATH
)
from BACKEND.security.security_layer import decrypt_entry


class TestEchoMemory(unittest.TestCase):

    def setUp(self):
        reset_echo_log()

    # 🧠 Functionality Test 1
    def test_01_store_and_retrieve_basic_echo(self):
        store_entry("THROBBING", "I am so tired of everything.", "ghost", "relapse")
        echo, silenced = retrieve_echo("THROBBING", "ghost")
        self.assertIsNotNone(echo)
        self.assertFalse(silenced)
        self.assertIn("entry", echo)
        self.assertGreater(len(echo["entry"]), 0)

    # 🕳️ Silencing Test
    def test_02_should_be_silenced_when_limit_exceeded(self):
        for _ in range(6):
            store_entry("ECHOING", "Still the same thoughts repeat.", "ghost", "loop")
        for _ in range(5):
            retrieve_echo("ECHOING", "ghost")
        echo, silenced = retrieve_echo("ECHOING", "ghost")
        self.assertTrue(silenced or echo["echo_count"] >= 5)

    # 📦 Archive Structure Test
    def test_03_export_archive_contains_pulses(self):
        archive = export_archive()
        self.assertIn("THROBBING", archive)
        self.assertIn("ghost", archive["THROBBING"])

    # 🔐 Encryption on Disk
    def test_04_entry_is_encrypted_on_disk(self):
        pulse, tone, tag = "FRACTURED", "monk", "collapse"
        text = "Test encrypted echo entry."
        store_entry(pulse, text, tone, tag)

        with open(LOG_PATH, "r", encoding="utf-8") as f:
            last = json.loads(f.readlines()[-1])
        encrypted = last["entry"]

        self.assertNotEqual(encrypted, text)
        self.assertEqual(decrypt_entry(encrypted), text)

    # ✅ Integrity Check
    def test_05_integrity_verification(self):
        pulse = "ABSURD"
        text = "This is an honest entry."
        store_entry(pulse, text, "absurd", "reflection")

        with open(LOG_PATH, "r", encoding="utf-8") as f:
            entry = json.loads(f.readlines()[-1])

        self.assertEqual(verify_integrity(entry), "intact")
        entry["entry"] = "tampered"
        self.assertEqual(verify_integrity(entry), "tampered")

    # 🆔 UID Format
    def test_06_uid_is_valid_uuid(self):
        store_entry("STILL", "Valid UUID test", "ghost", "identity")
        echo, _ = retrieve_echo("STILL", "ghost", testing=True)

        try:
            UUID(echo["uid"])
            valid = True
        except ValueError:
            valid = False

        self.assertTrue(valid)


if __name__ == "__main__":
    unittest.main()