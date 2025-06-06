# TESTS/test_pulse_affinity.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from BACKEND.core import pulse_affinity

class TestPulseAffinity(unittest.TestCase):

    def test_emotionally_similar_true(self):
        self.assertTrue(pulse_affinity.emotionally_similar("THROBBING", "FRACTURED"))
        self.assertTrue(pulse_affinity.emotionally_similar("FRACTURED", "THROBBING"))

    def test_emotionally_similar_false(self):
        self.assertFalse(pulse_affinity.emotionally_similar("ABSURD", "PRESSED"))
        self.assertFalse(pulse_affinity.emotionally_similar("THROBBING", "ABSURD"))

    def test_get_closest_related_default_threshold(self):
        related = pulse_affinity.get_closest_related("FRACTURED")
        self.assertIn("THROBBING", related)
        self.assertIn("PRESSED", related)
        self.assertNotIn("ABSURD", related)

    def test_get_closest_related_custom_threshold(self):
        related = pulse_affinity.get_closest_related("PRESSED", threshold=0.75)
        self.assertIn("THROBBING", related)
        self.assertNotIn("FRACTURED", related)

    def test_merge_affinities_top_related(self):
        merged = pulse_affinity.merge_affinities(["THROBBING", "FRACTURED"])
        top_targets = [x[0] for x in merged]
        self.assertIn("PRESSED", top_targets)
        self.assertIn("ECHOING", top_targets)
        self.assertNotIn("THROBBING", top_targets)
        self.assertNotIn("FRACTURED", top_targets)

if __name__ == "__main__":
    print("🧪 Running Pulse Affinity Tests...")
    unittest.main()