import os
from datetime import datetime

# 📁 Resolve absolute path to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ARCHIVE_PATH = os.path.join(PROJECT_ROOT, "LOGS", "journal_archive.txt")

# 🛠️ Ensure LOGS/ directory exists at the root
os.makedirs(os.path.dirname(ARCHIVE_PATH), exist_ok=True)

# 🧾 Initialize file if missing
if not os.path.exists(ARCHIVE_PATH):
    with open(ARCHIVE_PATH, "w", encoding="utf-8") as f:
        f.write("GHOST JOURNAL ARCHIVE\n" + "="*60 + "\n\n")

# ✍️ Write formatted journal entry to archive
def log_journal_entry(entry, pulse, tone=None, tag=None, strategy=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = (
        f"[{timestamp}] [Pulse: {pulse}] [Tone: {tone}] [Tag: {tag}] [Strategy: {strategy}]\n"
        f"{entry.strip()}\n\n"
    )
    try:
        with open(ARCHIVE_PATH, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception as e:
        print(f"[JOURNAL LOGGER ERROR] Failed to write: {e}")