# BACKEND/core/surveillance_utils.py

import json
from datetime import datetime
import os

SURVEILLANCE_LOG_PATH = os.path.join(
    os.path.dirname(__file__), "..", "LOGS", "echo_surveillance.jsonl"
)

def parse_surveillance_logs(path=SURVEILLANCE_LOG_PATH):
    logs = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    logs.append(entry)
                except json.JSONDecodeError:
                    print("[Surveillance Parser Error] Malformed log line skipped.")
    except Exception as e:
        print(f"[Surveillance Log Load Error] {e}")
    return logs

def generate_surveillance_report(logs, top_n=5):
    if not logs:
        return {
            "top_anomalies": [],
            "cue_mismatches": [],
            "timeline": [],
            "tampered_entries": []
        }

    # Sort by anomaly score
    sorted_by_anomaly = sorted(
        logs, key=lambda x: x.get('diff', {}).get('anomaly_score', 0), reverse=True
    )[:top_n]

    # Cue mismatches
    cue_mismatches = [log for log in logs if not log.get("diff", {}).get("cue_match", True)][:top_n]

    # Drift timeline
    timeline = []
    for log in logs:
        try:
            ts = log["timestamp"]
            drift_score = round(log["drift"]["score"], 2)
            timeline.append({
                "uid": log["uid"],
                "timestamp": ts,
                "drift": drift_score
            })
        except:
            continue

    # Tampered entries
    tampered = [
        log for log in logs if log.get("old_checksum") != log.get("new_checksum")
    ]

    return {
        "top_anomalies": sorted_by_anomaly,
        "cue_mismatches": cue_mismatches,
        "timeline": timeline,
        "tampered_entries": tampered
    }