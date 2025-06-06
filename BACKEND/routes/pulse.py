# BACKEND/routes/pulse.py (Final Ghostbound Edition)

from flask import Blueprint, request, jsonify
from BACKEND.core.ghostscript_engine import generate_ghost_response
from BACKEND.memory.echo_memory import export_archive

pulse_bp = Blueprint("pulse_bp", __name__)

@pulse_bp.route("/pulse", methods=["POST"])
def pulse_entry():
    data = request.get_json()
    entry = data.get("entry", "").strip()
    mode = data.get("mode", "ghost")
    allow_echo = data.get("echo", True)

    # 🚨 Validation
    if not entry:
        return jsonify({"error": "Empty entry. Please write something."}), 400

    # 🧠 Generate Ghost Response
    result = generate_ghost_response(entry, mode, allow_echo)

    return jsonify({
        "ghost_response": result["ghost_response"],
        "pulse": result["pulse"],
        "tag": result["tag"],
        "strategy": result["strategy"],
        "tone_origin": result["tone_origin"],
        "function": result["function"],  # 🧠 System-level logic like 'ECHO_ARCHIVE'
        "template": result["template"],
        "signals": result["signals"],
        "sentiment": result["sentiment"],
        "subjectivity": result["subjectivity"]
    })

# 📖 Echo Drawer route – returns all echoed memory
@pulse_bp.route("/pulse_feed", methods=["GET"])
def pulse_feed():
    try:
        echo_data = export_archive()
        return jsonify(echo_data)
    except Exception as e:
        return jsonify({"error": "Echo memory is unavailable."}), 500

# 🧪 (Optional) Dev Test Route – Safe to remove in production
"""
@pulse_bp.route("/debug/echo_test", methods=["GET"])
def echo_test():
    return jsonify({
        "ghost_response": "This is a test of Ghost's voice.",
        "pulse": "test_pulse",# BACKEND/routes/pulse.py (Final Ghostbound Edition)

from flask import Blueprint, request, jsonify
from BACKEND.core.ghostscript_engine import generate_ghost_response
from BACKEND.memory.echo_memory import export_archive

pulse_bp = Blueprint("pulse_bp", __name__)

@pulse_bp.route("/pulse", methods=["POST"])
def pulse_entry():
    data = request.get_json()
    entry = data.get("entry", "").strip()
    mode = data.get("mode", "ghost")
    allow_echo = data.get("echo", True)

    # 🚨 Validation
    if not entry:
        return jsonify({"error": "Empty entry. Please write something."}), 400

    # 🧠 Generate Ghost Response
    result = generate_ghost_response(entry, mode, allow_echo)

    return jsonify({
        "ghost_response": result["ghost_response"],
        "pulse": result["pulse"],
        "tag": result["tag"],
        "strategy": result["strategy"],
        "tone_origin": result["tone_origin"],
        "function": result["function"],  # 🧠 System-level logic like 'ECHO_ARCHIVE'
        "template": result["template"],
        "signals": result["signals"],
        "sentiment": result["sentiment"],
        "subjectivity": result["subjectivity"]
    })

# 📖 Echo Drawer route – returns all echoed memory
@pulse_bp.route("/pulse_feed", methods=["GET"])
def pulse_feed():
    try:
        echo_data = export_archive()
        return jsonify(echo_data)
    except Exception as e:
        return jsonify({"error": "Echo memory is unavailable."}), 500

# 🧪 (Optional) Dev Test Route – Safe to remove in production
"""
@pulse_bp.route("/debug/echo_test", methods=["GET"])
def echo_test():
    return jsonify({
        "ghost_response": "This is a test of Ghost's voice.",
        "pulse": "test_pulse",
        "tag": "test_tag",
        "strategy": ["validate", "mirror"],
        "tone_origin": "ghost",
        "function": "TEST",
        "template": "dev-mode",
        "signals": {},
        "sentiment": 0.1,
        "subjectivity": 0.5
    })
"""
        "tag": "test_tag",
        "strategy": ["validate", "mirror"],
        "tone_origin": "ghost",
        "function": "TEST",
        "template": "dev-mode",
        "signals": {},
        "sentiment": 0.1,
        "subjectivity": 0.5
    })
"""