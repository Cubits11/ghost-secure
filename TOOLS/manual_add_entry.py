import os
import sys

# 👇 Add your project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from BACKEND.memory.echo_memory import store_entry

# 🔹 Add test entry here
store_entry("FRACTURED", "i still remember the night i fell silent", tone="ghost", tag="ISOLATION")
print("✅ Entry stored and logged.")