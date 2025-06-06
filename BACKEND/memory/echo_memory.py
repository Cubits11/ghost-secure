# 📁 FILE: BACKEND/memory/echo_memory.py

from datetime import datetime, timedelta, timezone
from uuid import uuid4
import hashlib
import json
import os
import getpass
import socket

from BACKEND.memory.fingerprint_engine import (
    diff_fingerprints,
    compute_emotional_drift,
    fingerprint_checksum
)
from BACKEND.security.security_layer import encrypt_entry, decrypt_entry

# ---------------------------
# 📍 Constants and Globals
# ---------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FIXTURE_PATH = os.path.join(PROJECT_ROOT, "LOGS", "echo_log_fixture.json")
LOG_PATH = os.path.join(PROJECT_ROOT, "LOGS", "secure_echo_log.jsonl")
AUDIT_LOG_PATH = os.path.join(PROJECT_ROOT, "LOGS", "audit_log.jsonl")
SURVEILLANCE_LOG_PATH = os.path.join(PROJECT_ROOT, "LOGS", "echo_surveillance.jsonl")

PULSES = ["THROBBING", "ECHOING", "FRACTURED", "PRESSED", "STILL", "ABSURD", "UNKNOWN"]
TONES = ["ghost", "monk", "absurd"]

echo_log = {pulse: {tone: [] for tone in TONES} for pulse in PULSES}

MAX_ECHO_COUNT = 5
ECHO_COOLDOWN_MINUTES = 5

# ---------------------------
# 🔐 Fingerprint + Fallbacks
# ---------------------------
def generate_fingerprint(entry_text, tone, tag):
    try:
        from BACKEND.memory.fingerprint_engine import generate_fingerprint as _gen
        return _gen(entry_text, tone, tag)
    except ImportError:
        return {"warning": "fingerprint engine unavailable"}

def get_closest_related(pulse):
    try:
        from BACKEND.core.pulse_affinity import get_closest_related as _get
        return _get(pulse)
    except ImportError:
        return ["UNKNOWN"]

# ---------------------------
# ✍️ Store Echo Entry
# ---------------------------
def store_entry(pulse, entry_text, tone="ghost", tag="UNKNOWN"):
    timestamp = datetime.now(timezone.utc).isoformat()
    uid = str(uuid4())
    fingerprint_data = generate_fingerprint(entry_text, tone, tag)
    new_fp = fingerprint_data.get("fingerprint")
    if not new_fp:
        print("[Store Entry] Missing fingerprint, skipping entry.")
        return

    echo_log.setdefault(pulse, {t: [] for t in TONES})
    echo_log[pulse].setdefault(tone, [])
    bank = echo_log[pulse][tone]

    for existing in bank:
        if existing.get("fingerprint", {}).get("fingerprint") == new_fp:
            log_surveillance(existing.get("uid", uid), existing["fingerprint"], fingerprint_data)
            existing.update({
                "echo_count": existing.get("echo_count", 0) + 1,
                "last_echoed": timestamp,
                "timestamp": timestamp,
                "fingerprint": fingerprint_data
            })
            existing["fingerprint"]["seen_again"] = True
            log_echo_entry({**existing, "entry": entry_text.strip(), "tone": tone, "tag": tag}, enable_audit_trail=True)
            return

    entry = {
        "uid": uid,
        "version": "1.0",
        "timestamp": timestamp,
        "entry": entry_text.strip(),
        "length": len(entry_text.strip().split()),
        "first_words": entry_text.strip().split()[:6],
        "echoed": False,
        "echo_count": 0,
        "fingerprint": fingerprint_data
    }
    bank.append(entry)
    log_echo_entry({**entry, "tone": tone, "tag": tag}, enable_audit_trail=True)

# ---------------------------
# 🔍 Echo Eligibility + Scoring
# ---------------------------
def should_echo(entry, testing=False):
    if not entry or entry.get("echoed", False): return False
    if entry.get("echo_count", 0) >= MAX_ECHO_COUNT: return False
    if not testing and entry.get("last_echoed"):
        try:
            last = datetime.fromisoformat(entry["last_echoed"].replace("Z", "+00:00"))
            if datetime.now(timezone.utc) - last < timedelta(minutes=ECHO_COOLDOWN_MINUTES): return False
        except: return False
    return 3 <= entry.get("length", 0) <= 50

def score_echo(entry):
    l = entry["length"]
    return 0.9 if l < 25 else 0.5 if l < 50 else 0.2

# ---------------------------
# 🧠 Retrieve Resonant Echo
# ---------------------------
def retrieve_echo(pulse, tone="ghost", testing=False):
    best, score = None, 0

    def search(pulses):
        nonlocal best, score
        for p in pulses:
            bank = echo_log.get(p, {}).get(tone, [])
            entries_to_scan = bank if testing else bank[:-1] if len(bank) > 1 else bank
            for e in reversed(entries_to_scan):
                if should_echo(e, testing=testing):
                    s = score_echo(e)
                    if s > score:
                        best, score = e, s

    search([pulse])
    if not best:
        search(get_closest_related(pulse))

    if best:
        if not testing:
            best.update({
                "echoed": True,
                "echo_count": best.get("echo_count", 0) + 1,
                "last_echoed": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            })
        return best, False
    return None, True

# ---------------------------
# 🎭 Echo Formatting
# ---------------------------
def format_echo_memory(e):
    if not e: return None
    fw = e.get("first_words", ["..."])
    try:
        ago = (datetime.now(timezone.utc) - datetime.fromisoformat(e["timestamp"])).total_seconds() / 60
    except: ago = 0

    if e.get("echo_count", 0) >= 4:
        return "Ghost paused. You’ve said this often—let’s hold the silence together this time."
    if ago < 3:
        return f"You just wrote: \u201c{' '.join(fw)}...\u201d Are you listening to yourself?"
    if ago < 10:
        return f"You once wrote: \u201c{' '.join(fw)}...\u201d It still hums underneath."
    if ago < 60:
        return f"You whispered this an hour ago: \u201c{fw[0]}...\u201d"
    return f"You once wrote: \u201c{' '.join(fw)}...\u201d Time didn’t erase it."

# ---------------------------
# 📤 Archive Echo Log
# ---------------------------
def export_archive():
    return echo_log

# ---------------------------
# 🔄 Reset & Load from Disk
# ---------------------------
def reset_echo_log():
    global echo_log
    try:
        with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
            echo_log.clear()
            echo_log.update(json.load(f))
    except Exception:
        echo_log = {pulse: {tone: [] for tone in TONES} for pulse in PULSES}
    load_from_log()

def load_from_log(path=LOG_PATH):
    print(f"[Echo Load] Reading from: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    e = json.loads(line.strip())
                    if "entry" in e:
                        try:
                            e["entry"] = decrypt_entry(e["entry"])
                        except Exception:
                            e["entry"] = "[Error: Decryption failed]"

                    tone = e.get("tone", "ghost")
                    pulse = e.get("pulse", "UNKNOWN")
                    e["tamper_status"] = verify_integrity(e)

                    echo_log.setdefault(pulse, {t: [] for t in TONES})
                    echo_log[pulse].setdefault(tone, []).append(e)

                    if "[Error" not in e["entry"]:
                        print(f"[🧩] Loaded echo ({pulse}, {tone}) →", e["entry"][:60])
                except json.JSONDecodeError:
                    print("[⚠️] Skipping corrupt JSON line")
                except Exception as err:
                    print(f"[⚠️] Failed to load one line: {err}")
    except FileNotFoundError:
        print(f"[🚫] Echo log file not found at {path}")
    except Exception as err:
        print(f"[Log Load Error] {err}")

# ---------------------------
# 🧾 Integrity + Audit Trail
# ---------------------------
def compute_secure_hash(e):
    return hashlib.sha256(json.dumps({k: v for k, v in e.items() if k != "hash"}, sort_keys=True).encode()).hexdigest()

def verify_integrity(e):
    expected = e.get("hash")
    actual = compute_secure_hash(e)
    return "intact" if expected == actual else "tampered"

def log_echo_entry(e, enable_audit_trail=False):
    try:
        if "entry" in e:
            e["entry"] = encrypt_entry(e["entry"])
        e["hash"] = compute_secure_hash(e)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(e) + "\n")
        if enable_audit_trail:
            log = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "uid": e.get("uid"),
                "tag": e.get("tag"),
                "tone": e.get("tone"),
                "operation": "log_echo_entry",
                "user": getpass.getuser(),
                "host": socket.gethostname()
            }
            with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as af:
                af.write(json.dumps(log) + "\n")
    except Exception as err:
        print(f"[Log Error] {err}")

# ---------------------------
# 🔍 Surveillance Logging
# ---------------------------
def log_surveillance(uid, old_fp, new_fp):
    try:
        log = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uid": uid,
            "diff": diff_fingerprints(old_fp, new_fp),
            "drift": compute_emotional_drift(old_fp, new_fp),
            "old_checksum": fingerprint_checksum(old_fp),
            "new_checksum": fingerprint_checksum(new_fp)
        }
        with open(SURVEILLANCE_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(log) + "\n")
    except Exception as err:
        print(f"[Surveillance Error] {err}")