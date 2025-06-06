# BACKEND/core/tag_logic_engine.py (Final Lightborn Edition)

def determine_response_logic(tag, severity):
    logic_map = {
        ("relapse", 3): {
            "tone": "Truth Blade",
            "strategy": "Confrontation",
            "prompt_template": "Direct truth, bold and steady",
            "memory_action": "Suppress echo"
        },
        ("relapse", 2): {
            "tone": "Mirror",
            "strategy": "Reverse Mirror",
            "prompt_template": "Reflect quiet progress",
            "memory_action": "Record return"
        },
        ("disconnection", 2): {
            "tone": "Ghost",
            "strategy": "Poetic Reflection",
            "prompt_template": "Metaphor and imagery",
            "memory_action": "Allow recurrence"
        },
        ("shame", 2): {
            "tone": "Mirror",
            "strategy": "Gentle Contradiction",
            "prompt_template": "Challenge false narrative softly",
            "memory_action": "Flag for reentry"
        },
        ("identity", 2): {
            "tone": "Ghost",
            "strategy": "Echo Response",
            "prompt_template": "Repeat pattern symbolically",
            "memory_action": "Link to past tag"
        },
        ("suppression", 1): {
            "tone": "Monk",
            "strategy": "Containment",
            "prompt_template": "Quiet affirmation",
            "memory_action": "Silent archive"
        },
        ("healing-fear", 2): {
            "tone": "Mirror",
            "strategy": "Reframing Identity",
            "prompt_template": "Transform anxiety into becoming",
            "memory_action": "Encourage self-trust"
        }
    }

    key = (tag, severity)
    if key in logic_map:
        return logic_map[key]

    for s in range(severity - 1, 0, -1):
        fallback_key = (tag, s)
        if fallback_key in logic_map:
            return logic_map[fallback_key]

    return {
        "tone": "Monk",
        "strategy": "Minimal Reassurance",
        "prompt_template": "Anchor presence gently",
        "memory_action": "No action"
    }