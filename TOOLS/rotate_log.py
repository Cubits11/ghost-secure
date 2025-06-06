# TOOLS/rotate_log.py

import os
import shutil
from datetime import datetime

LOG_DIR = os.path.join("LOGS")
CURRENT_LOG = os.path.join(LOG_DIR, "secure_echo_log.jsonl")

def rotate_log():
    if not os.path.exists(CURRENT_LOG):
        print("❌ No secure log found to rotate.")
        return

    timestamp = datetime.now().isoformat(timespec="seconds").replace(":", "-")
    archive_name = f"secure_echo_log_{timestamp}.jsonl"
    archive_path = os.path.join(LOG_DIR, archive_name)

    shutil.copy2(CURRENT_LOG, archive_path)
    open(CURRENT_LOG, "w", encoding="utf-8").close()

    print(f"\n🔄 Secure Log Rotated")
    print(f"📦 Archived as: {archive_name}")
    print(f"🆕 New empty log created: secure_echo_log.jsonl")

if __name__ == "__main__":
    rotate_log()