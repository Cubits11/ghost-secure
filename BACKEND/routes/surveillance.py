# BACKEND/routes/surveillance.py

from flask import Blueprint, jsonify
import os, json
from BACKEND.memory.fingerprint_engine import diff_fingerprints, compute_emotional_drift, fingerprint_checksum

surveillance_bp = Blueprint("surveillance_bp", __name__)

SURVEILLANCE_LOG = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "LOGS", "echo_surveillance.jsonl"
))

@surveillance_bp.route("/surveillance", methods=["GET"])
def get_surveillance_log():
    entries = []
    try:
        if not os.path.exists(SURVEILLANCE_LOG):
            print("[SURVEILLANCE] Log file not found.")
            return jsonify({"entries": [], "status": "ok"})

        with open(SURVEILLANCE_LOG, "r") as f:
            for i, line in enumerate(f):
                try:
                    obj = json.loads(line)
                    old_fp = obj.get("old_fp") or obj.get("old_fingerprint")
                    new_fp = obj.get("new_fp") or obj.get("new_fingerprint")

                    if not old_fp or not new_fp:
                        print(f"[SKIP] Line {i}: missing fingerprints.")
                        continue

                    diff = diff_fingerprints(old_fp, new_fp)
                    drift = compute_emotional_drift(old_fp, new_fp)
                    old_checksum = fingerprint_checksum(old_fp)
                    new_checksum = fingerprint_checksum(new_fp)

                    entry = {
                        "uid": obj.get("uid", f"entry_{i}"),
                        "timestamp": obj.get("timestamp", "unknown"),
                        "diff": diff,
                        "drift": drift,
                        "old_checksum": old_checksum,
                        "new_checksum": new_checksum
                    }
                    entries.append(entry)

                except Exception as parse_error:
                    print(f"[ERROR] Failed to parse line {i}: {parse_error}")
                    continue

        entries.sort(key=lambda x: x["timestamp"], reverse=True)
        print(f"[SURVEILLANCE] Returning {len(entries)} entries.")
        return jsonify({"entries": entries[:50], "status": "ok"})

    except Exception as e:
        print(f"[SURVEILLANCE ROUTE ERROR] {e}")
        return jsonify({"error": f"Failed to load surveillance log: {str(e)}"}), 500

@surveillance_bp.route("/surveillance/raw", methods=["GET"])
def get_surveillance_raw():
    """Return raw surveillance intelligence (for dashboards and anomaly detection)."""
    dummy_output = {
        "top_anomalies": [],
        "cue_mismatches": [],
        "timeline": [],
        "tampered_entries": [],
        "status": "success"
    }

    if not os.path.exists(SURVEILLANCE_LOG):
        print("[SURVEILLANCE] Log file not found.")
        return jsonify(dummy_output)

    try:
        top_anomalies = []
        cue_mismatches = []
        timeline = []
        tampered_entries = []

        with open(SURVEILLANCE_LOG, "r") as f:
            for line in f:
                try:
                    obj = json.loads(line)

                    # General metadata
                    timeline.append({
                        "uid": obj.get("uid", "unknown"),
                        "timestamp": obj.get("timestamp", "unknown")
                    })

                    # Placeholder analysis logic
                    if obj.get("is_tampered"):
                        tampered_entries.append(obj)

                    if obj.get("cue_mismatch"):
                        cue_mismatches.append(obj)

                    if obj.get("drift_score", 0) > 0.7:
                        top_anomalies.append(obj)

                except Exception as inner:
                    continue

        return jsonify({
            "top_anomalies": top_anomalies[-20:],  # Limit for UI
            "cue_mismatches": cue_mismatches[-20:],
            "timeline": timeline[-100:],  # Recent 100 UIDs
            "tampered_entries": tampered_entries[-20:],
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": f"Raw surveillance read failed: {str(e)}"}), 500
