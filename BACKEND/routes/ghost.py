# BACKEND/routes/ghost.py (Final Lightborn Route Blueprint — with safe pulse_feed)

from flask import Blueprint, request, jsonify
from datetime import datetime
import json, os

# Core engines and memory tools
from BACKEND.core.ghostscript_engine import generate_ghost_response
from BACKEND.memory.echo_memory import reset_echo_log, export_archive, echo_log
from BACKEND.memory.tone_tracker import load_tone_tracker
from BACKEND.memory.echo_resonance_engine import echo_emotion_profile, resonant_echo

# Blueprint init
ghost_bp = Blueprint("ghost", __name__)

@ghost_bp.route("/journal", methods=["POST"])
def journal_entry():
    data = request.get_json()
    entry = data.get("entry", "")
    mode = data.get("mode", "ghost")
    allow_echo = data.get("echo", True)

    result = generate_ghost_response(entry, mode, allow_echo)

    return jsonify({
        "pulse": result["pulse"],
        "tone": result["tone_origin"],
        "function": result["function"],
        "signals": result["signals"],
        "sentiment": result["sentiment"],
        "subjectivity": result["subjectivity"],
        "ghost_response": result["ghost_response"]
    })

@ghost_bp.route("/reset", methods=["GET"])
def reset():
    reset_echo_log()
    log_path = os.path.join("LOGS", "tone_flow.log")
    with open(log_path, "a") as log:
        log.write(f"[RESET] {datetime.now().isoformat()}\n")
    return jsonify({"message": "Echo memory and journal reset."})

@ghost_bp.route("/pulse_status", methods=["GET"])
def pulse_counts():
    return {pulse: len(echo_log[pulse]) for pulse in echo_log}

@ghost_bp.route("/archive", methods=["GET"])
def journal_archive():
    return jsonify(export_archive())

@ghost_bp.route("/tracker", methods=["GET"])
def tracker():
    return jsonify(load_tone_tracker())

@ghost_bp.route("/echo_profile", methods=["GET"])
def echo_profile():
    recent = None
    latest_time = None
    for tone_dict in echo_log.values():
        for entry_list in tone_dict.values():
            for entry in entry_list:
                try:
                    t = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
                    if not latest_time or t > latest_time:
                        latest_time = t
                        recent = entry
                except:
                    continue
    if not recent:
        return jsonify({"error": "No recent echo entries found."})
    profile = echo_emotion_profile(recent)
    profile["echo_text"] = resonant_echo(recent, recent.get("tone", "ghost"))
    profile["first_words"] = recent.get("first_words", [])
    return jsonify(profile)

@ghost_bp.route("/pulse_feed", methods=["GET"])
def pulse_feed():
    all_entries = []
    for pulse, tone_dict in echo_log.items():
        for tone, entries in tone_dict.items():
            for entry in entries:
                try:
                    t = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
                    entry["_t"] = t
                    entry["pulse"] = pulse
                    entry["tone"] = tone
                    all_entries.append(entry)
                except:
                    continue
    sorted_entries = sorted(all_entries, key=lambda e: e["_t"], reverse=True)
    feed = []
    for entry in sorted_entries[:5]:
        profile = echo_emotion_profile(entry)
        feed.append({
            "timestamp": entry.get("timestamp"),
            "tone": profile["tone"],
            "pulse": entry.get("pulse", ""),
            "symbolic": profile["symbolic"],
            "echo_count": profile["echo_count"],
            "echo_text": resonant_echo(entry, profile["tone"])
        })
    return jsonify(feed)

@ghost_bp.route("/dna_bias_test", methods=["POST"])
def dna_bias_test():
    data = request.get_json()
    pulse = data.get("pulse", "UNKNOWN")
    mode = data.get("mode", "ghost")
    echo_pressure = data.get("echo_pressure", 0)

    from BACKEND.content.quote_bank import QUOTE_BANK
    dna_path = os.path.join("BACKEND", "content", "dna_bank.json")
    with open(dna_path, "r", encoding="utf-8") as f:
        dna_bank = json.load(f)
    from BACKEND.core.ghostscript_engine import get_symbolic_silence

    tone_fallbacks = dna_bank.get(pulse, {}).get("fallback_tones", [])
    selected_tone = mode if mode != "ghost" else (tone_fallbacks[0] if tone_fallbacks else "ghost")

    candidates = [q for q in QUOTE_BANK.get(pulse, []) if q[1] == selected_tone]
    quote = None
    reason = ""

    if candidates:
        quote = candidates[0][0]
        reason = "Tone-matched quote found."
    elif QUOTE_BANK.get(pulse):
        quote = QUOTE_BANK[pulse][0][0]
        reason = "Fallback quote used — no tone match."
    else:
        quote = get_symbolic_silence(mode)
        reason = "No quotes available, using symbolic silence."

    return jsonify({
        "mode": mode,
        "selected_tone": selected_tone,
        "fallback_quote": quote,
        "symbolic_silence": get_symbolic_silence(mode),
        "quote_candidates": [q[0] for q in QUOTE_BANK.get(pulse, [])],
        "reason": reason
    })