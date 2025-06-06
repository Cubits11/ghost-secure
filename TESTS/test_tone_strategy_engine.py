# TESTS/test_tone_strategy_engine.py

import unittest
import os
import sys
import json
import time
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from BACKEND.core import tone_strategy_engine as tse

class TestToneStrategyEngine(unittest.TestCase):
    def setUp(self):
        self.user_id = "test_user"
        self.pulse = "FRACTURED"
        self.test_dna = [
            {
                "question": "How do you feel today?",
                "emotional_tags": ["identity", "solitude"],
                "default_tone": "ghost",
                "strategies": ["mirror", "anchor"]
            }
        ]
        self.old_dna = tse.DNA[:]
        tse.DNA.clear()
        tse.DNA.extend(self.test_dna)

    def tearDown(self):
        tse.DNA.clear()
        tse.DNA.extend(self.old_dna)

    def test_prioritize_tags(self):
        tags = ["hope", "shame", "identity"]
        prioritized = tse.prioritize_tags(tags)
        self.assertEqual(prioritized, ["shame", "hope", "identity"])

    def test_find_dna_match(self):
        match = tse.find_dna_match("identity")
        self.assertIsNotNone(match)
        self.assertEqual(match["default_tone"], "ghost")

    def test_resolve_tone_flow(self):
        tone, strategies = tse.resolve_tone_flow(
            user_id=self.user_id, tags=["identity"], pulse=self.pulse, echo_count=0
        )
        self.assertEqual(tone, "ghost")
        self.assertIn("anchor", strategies)

    def test_get_strategy_routing(self):
        routing = tse.get_strategy_routing(
            tags=["identity", "solitude"], echo_count=1,
            user_id=self.user_id, pulse=self.pulse
        )
        self.assertEqual(routing["tone"], "ghost")
        self.assertIn("mirror", routing["strategies"])

if __name__ == "__main__":
    print("🧪 Running Tone Strategy Engine Tests...")
    unittest.main()