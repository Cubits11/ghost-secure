# TESTS/test_surveillance_endpoint.py

import os
import json
import pytest
from datetime import datetime
from BACKEND.core.app import app

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "LOGS")
FAILURE_LOG = os.path.join(LOG_DIR, "test_failures.log")

REQUIRED_KEYS = {"uid", "timestamp", "diff", "drift", "old_checksum", "new_checksum"}

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def log_failure(test_name, message):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(FAILURE_LOG, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] ❌ {test_name}: {message}\n")

def test_surveillance_response(client):
    res = client.get("/surveillance")
    assert res.status_code == 200, "Expected 200 OK"

    data = res.get_json()
    assert "entries" in data and isinstance(data["entries"], list), "Missing or invalid 'entries' key"

    for i, entry in enumerate(data["entries"][:5]):
        missing_keys = REQUIRED_KEYS - entry.keys()
        if missing_keys:
            log_failure("test_surveillance_response", f"Entry {i} missing keys: {missing_keys}")
            assert False, f"Entry {i} missing keys: {missing_keys}"

        if not isinstance(entry["diff"], dict) or not isinstance(entry["drift"], dict):
            log_failure("test_surveillance_response", f"Entry {i} 'diff' or 'drift' is not a dict")
            assert False