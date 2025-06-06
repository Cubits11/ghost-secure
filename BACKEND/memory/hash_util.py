# BACKEND/memory/hash_util.py

import hashlib
import json

def compute_hash(entry):
    """
    Compute a SHA-256 hash of the JSON entry (excluding the hash field).
    This ensures tamper-detection by comparing known hashes.
    """
    json_str = json.dumps(entry, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(json_str.encode('utf-8')).hexdigest()