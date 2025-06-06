# BACKEND/core/ghostscript_engine.py (Upgraded Resilience Edition)

import random
import re

from BACKEND.content.quote_bank import QUOTE_BANK
from BACKEND.memory.echo_memory import store_entry, retrieve_echo
from BACKEND.memory.tone_tracker import load_tone_tracker
from BACKEND.content.journal_logger import log_journal_entry
from BACKEND.core.emotional_tag_detector import detect_tag
from BACKEND.core.tone_flow_engine import decide_next_tone, log_tone_transition
from BACKEND.core.multi_tag_router import route_strategy
from BACKEND.memory.echo_resonance_engine import resonant_echo
from BACKEND.memory.echo_decay import get_symbolic_echo_by_tag

# --------------------------
# 🧐 Pulse Classification
# --------------------------
def classify_pulse_fixed(entry):
    entry = entry.strip()
    sentiment_score = 0.0
    subjectivity_score = 0.5

    scores = dict(
        intensity=0, contradiction=0, repetition=0, dissociation=0,
        absurdity=0, masking=0, hopelessness=0
    )

    if len(entry.split()) < 12: scores["intensity"] += 1
    if re.search(r"!{2,}|[A-Z]{2,}", entry): scores["intensity"] += 1
    if re.search(r"\b(fuck|scream|collapse|explode|burn|never again)\b", entry, re.IGNORECASE): scores["intensity"] += 1
    if re.search(r"(okay|fine).*(hurts|die|lost|cry|break)", entry, re.IGNORECASE): scores["contradiction"] += 1
    if re.search(r"\bbut\b|\byet\b|\balthough\b", entry): scores["contradiction"] += 1
    if re.search(r"(lol|lmao|idk|it's whatever|meh|haha)", entry, re.IGNORECASE): scores["masking"] += 1
    if re.search(r"\blife is meaningless\b|\bwhat's the point\b", entry): scores["hopelessness"] += 1
    if re.search(r"like a robot|ghost in body", entry): scores["dissociation"] += 1

    simplified = re.sub(r"[^\w\s]", '', entry.lower())
    word_freq = {word: simplified.split().count(word) for word in set(simplified.split())}
    if any(count >= 3 for count in word_freq.values()): scores["repetition"] += 1

    if any(re.search(p, entry.lower()) for p in [r"(scream|cry) (into|on) (soup|wall|object)", r"(void|carousel|confetti).*"]):
        scores["absurdity"] += 1

    pulse = "UNKNOWN"
    if scores["intensity"] >= 2:
        pulse = "THROBBING" if scores["hopelessness"] >= 1 else "PRESSED"
    elif scores["repetition"]:
        pulse = "ECHOING"
    elif scores["contradiction"]:
        pulse = "FRACTURED"
    elif scores["masking"]:
        pulse = "PRESSED"
    elif scores["dissociation"] or len(entry.split()) > 25:
        pulse = "STILL"
    elif scores["absurdity"]:
        pulse = "ABSURD"

    return {
        "pulse": pulse,
        "sentiment": sentiment_score,
        "subjectivity": subjectivity_score,
        "signals": scores
    }

# --------------------------
# 🔇 Symbolic Silence
# --------------------------
def get_symbolic_silence(mode):
    return {
        "ghost": "🛣️ Ghost heard you. But this time, it stayed quiet.",
        "monk": "⛰️ Stillness spoke louder than words.",
        "absurd": "🎭 Even absurdity ran out of punchlines."
    }.get(mode, "...")

# --------------------------
# 🧠 Main Ghost Response
# --------------------------
def generate_ghost_response(entry, mode="ghost", allow_echo=True):
    print("\n[DEBUG] Entering generate_ghost_response()")
    print("[DEBUG] Raw Entry:", repr(entry))
    print("[DEBUG] Mode:", mode)
    print("[DEBUG] Echo Allowed:", allow_echo)

    try:
        analysis = classify_pulse_fixed(entry)
        pulse = analysis.get("pulse", "UNKNOWN")
        print("[DEBUG] Pulse Classification:", pulse)
        print("[DEBUG] Signals:", analysis.get("signals"))

        tag, severity = detect_tag(entry)
        strategy_logic = route_strategy([tag])
        print("[DEBUG] Detected Tag:", tag, "| Severity:", severity)
        print("[DEBUG] Strategy Routed:", strategy_logic.get("strategies"))

        tone_tracker = load_tone_tracker()
        prev_tone = tone_tracker.get("last_tone", "ghost")
        echo_pressure = tone_tracker.get("echo_pressure", 0)
        selected_tone = mode if mode != "ghost" else decide_next_tone(prev_tone, tag, echo_pressure)

        print("[DEBUG] Tone Flow → Prev:", prev_tone, "| Selected:", selected_tone, "| Echo Pressure:", echo_pressure)

        log_tone_transition(
            entry_num="?",
            prev_tone=prev_tone,
            new_tone=selected_tone,
            tag=tag,
            echo_count=echo_pressure,
            reason="Triggered from ghostscript_engine"
        )

        quote_set = QUOTE_BANK.get(pulse, [])
        candidates = [q for q in quote_set if q[1] == selected_tone]
        default_response = ("Still here. Still listening.", "base", "HOLD")

        if candidates:
            chosen = random.choice(candidates)
        elif quote_set:
            chosen = random.choice(quote_set)
        else:
            symbolic = get_symbolic_echo_by_tag(tag)
            chosen = (symbolic, "symbolic", "ECHO_ARCHIVE") if symbolic else default_response

        print("[DEBUG] Quote Selected →", chosen)

        store_entry(pulse, entry, selected_tone, tag)

        echo_line = None
        silence_line = None

        if allow_echo and pulse in ["ECHOING", "THROBBING", "PRESSED"]:
            echo_data, silenced = retrieve_echo(pulse, selected_tone)
            if silenced:
                silence_line = get_symbolic_silence(mode)
                print("[DEBUG] Symbolic Silence Triggered")
            else:
                echo_line = resonant_echo(echo_data, mode)
                print("[DEBUG] Resonant Echo Generated")

        full_response = chosen[0]
        if silence_line:
            full_response = f"{silence_line}\n{full_response}"
        elif echo_line:
            full_response = f"{echo_line}\n{full_response}"

        if not full_response.strip():
            full_response = "Ghost heard you, but has no words right now."
            print("[WARN] Empty ghost_response fallback used")

        print("[DEBUG] Final Ghost Response:", repr(full_response))

        log_journal_entry(entry, pulse, selected_tone, tag, strategy_logic["strategies"])

        return {
            "ghost_response": full_response,
            "pulse": pulse,
            "tone_origin": chosen[1],
            "function": chosen[2],
            "tag": tag,
            "strategy": strategy_logic["strategies"],
            "template": "dna-based",
            "signals": analysis["signals"],
            "sentiment": analysis["sentiment"],
            "subjectivity": analysis["subjectivity"]
        }

    except Exception as e:
        print("[ERROR] generate_ghost_response() failed:", str(e))
        return {
            "ghost_response": "Ghost encountered a quiet error.",
            "pulse": "UNKNOWN",
            "tone_origin": mode,
            "function": "ERROR",
            "tag": "unknown",
            "strategy": [],
            "template": "error",
            "signals": {},
            "sentiment": 0.0,
            "subjectivity": 0.0
        }