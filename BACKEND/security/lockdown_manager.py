import json
import os
from datetime import datetime

# ✅ Correct lockdown file path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOCKDOWN_FILE = os.path.join(PROJECT_ROOT, "BACKEND", "memory", "lockdown_status.json")

def read_lock_file():
    if not os.path.exists(LOCKDOWN_FILE):
        return {"locked": False}
    try:
        with open(LOCKDOWN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Lockdown Error] Failed to read file: {e}")
        return {"locked": False}

def is_locked():
    return read_lock_file().get("locked", False)

def lock_system(reason="Unknown Security Trigger"):
    status = {
        "locked": True,
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    try:
        print(f"[DEBUG] Writing lockdown file at {LOCKDOWN_FILE}")
        with open(LOCKDOWN_FILE, "w", encoding="utf-8") as f:
            json.dump(status, f, indent=2)
        print(f"[Lockdown] System locked. Reason: {reason}")
    except Exception as e:
        print(f"[Lockdown Error] Could not write lock file: {e}")

def unlock_system():
    if os.path.exists(LOCKDOWN_FILE):
        try:
            os.remove(LOCKDOWN_FILE)
            print("[Lockdown] Lockdown lifted.")
        except Exception as e:
            print(f"[Unlock Error] Could not remove lock file: {e}")
    else:
        print("[Lockdown] No active lockdown.")

def toggle_lockdown():
    if is_locked():
        unlock_system()
        return False
    else:
        lock_system("Manual toggle via API")
        return True

def get_lock_info():
    return read_lock_file()