# BACKEND/core/multi_tag_router.py (Final Lightborn Edition)

# This module routes tone and strategy when multiple emotional tags are detected in a single entry.
# It integrates:
#   - tag priority
#   - echo memory references
#   - dna_bank.json alignment
#   - strategy blending

import os
import json

# 🔗 Resolve DNA path safely
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DNA_BANK_PATH = os.path.join(PROJECT_ROOT, "content", "dna_bank.json")

# --------------------------
# 📥 Load DNA Bank
# --------------------------
def load_dna_bank():
    try:
        with open(DNA_BANK_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load DNA bank: {e}")
        return []

# --------------------------
# 🧠 Prioritize Tags
# --------------------------
def prioritize_tags(tags, echo_history=None):
    echo_weight = {tag: echo_history.get(tag, 0) for tag in tags} if echo_history else {tag: 0 for tag in tags}
    return sorted(tags, key=lambda t: -echo_weight[t])

# --------------------------
# 🎯 Select Tone + Strategy
# --------------------------
def route_strategy(tags, echo_history=None):
    dna = load_dna_bank()
    tag_priority = prioritize_tags(tags, echo_history)

    if not tag_priority:
        return {
            "tone": "monk",
            "strategies": ["anchor"],
            "qID": None,
            "source": "default"
        }

    dominant_tag = tag_priority[0]
    matched_q = None

    for q in dna:
        if dominant_tag in q.get("emotional_tags", []):
            matched_q = q
            break

    if not matched_q:
        return {
            "tone": "monk",
            "strategies": ["anchor"],
            "qID": None,
            "source": "default"
        }

    strategies = matched_q.get("strategies", [])
    secondary = tag_priority[1:] if len(tag_priority) > 1 else []

    for sec in secondary:
        for q in dna:
            if sec in q.get("emotional_tags", []):
                for s in q.get("strategies", []):
                    if s not in strategies:
                        strategies.append(s)
                break

    return {
        "tone": matched_q.get("default_tone", "monk"),
        "strategies": strategies,
        "qID": matched_q.get("qID"),
        "source": "dna"
    }

# --------------------------
# 🧪 Test Example
# --------------------------
if __name__ == "__main__":
    test_tags = ["grief", "rage", "hope"]
    echo_mock = {"grief": 2, "rage": 1, "hope": 0}
    decision = route_strategy(test_tags, echo_mock)
    print("Decision:", json.dumps(decision, indent=2))
