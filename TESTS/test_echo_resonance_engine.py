# TESTS/test_echo_resonance_engine.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from datetime import datetime, timedelta

from BACKEND.memory.echo_resonance_engine import (
    transform_echo,
    should_silence,
    get_silence_line,
    echo_emotion_profile,
    resonant_echo
)

class TestEchoResonanceEngine(unittest.TestCase):

    def setUp(self):
        self.base_entry = {
            "entry": "I feel like I disappeared.",
            "timestamp": (datetime.now() - timedelta(minutes=90)).strftime("%Y-%m-%d %H:%M:%S"),
            "length": 6,
            "echo_count": 1,
            "first_words": ["I", "feel", "like", "I", "disappeared"],
            "fingerprint": {"symbolic": "DRIFT", "tone": "ghost"}
        }

    def test_transform_echo_cues(self):
        cues = {
            "DRIFT": "vanishing",
            "SPIKE": "cut deep",
            "MASK": "hiding something",
            "VOID": "into the void",
            "LOOP": "again and again",
            "ECHO": "still lingers",
            "NONE": "“I...”"
        }
        for cue, expected_phrase in cues.items():
            entry = self.base_entry.copy()
            entry["fingerprint"]["symbolic"] = cue
            result = transform_echo(entry, mode="ghost")
            self.assertIn(expected_phrase, result)

    def test_should_silence_conditions(self):
        # High echo_count
        entry = self.base_entry.copy()
        entry["echo_count"] = 5
        self.assertTrue(should_silence(entry))

        # Symbolic VOID
        entry["echo_count"] = 1
        entry["fingerprint"]["symbolic"] = "VOID"
        self.assertTrue(should_silence(entry))

        # Symbolic LOOP and echo_count 3
        entry["fingerprint"]["symbolic"] = "LOOP"
        entry["echo_count"] = 3
        self.assertTrue(should_silence(entry))

        # Recent timestamp
        entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertTrue(should_silence(entry))

    def test_get_silence_line_by_tone(self):
        ghost_line = get_silence_line("VOID", tone="ghost")
        monk_line = get_silence_line("VOID", tone="monk")
        absurd_line = get_silence_line("VOID", tone="absurd")
        self.assertIn("Ghost", ghost_line)
        self.assertIn("clarity", monk_line)
        self.assertIn("Void", absurd_line)

    def test_resonant_echo_paths(self):
        # Case 1: silence
        entry = self.base_entry.copy()
        entry["echo_count"] = 5
        result = resonant_echo(entry, mode="ghost")
        self.assertIn("Ghost listens", result)

        # Case 2: no symbolic
        entry["echo_count"] = 1
        entry["fingerprint"]["symbolic"] = "NONE"
        result = resonant_echo(entry, mode="ghost")
        self.assertIn("I", result)

        # Case 3: transformed
        entry["fingerprint"]["symbolic"] = "DRIFT"
        result = resonant_echo(entry, mode="ghost")
        self.assertIn("vanishing", result)

if __name__ == "__main__":
    print("🧪 Running Echo Resonance Engine Tests...")
    unittest.main()
