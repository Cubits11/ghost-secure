# TESTS/test_surveillance_logs.py

import pytest
import json
from datetime import datetime
import sys, os

# Ensure BACKEND is importable
sys.path.append(os.path.abspath("BACKEND"))

from BACKEND.core.app import app  # ✅ Corrected import path

LOG_DIR = os.path.join("BACKEND", "LOGS")
FAILURE_LOG_PATH = os.path.join(LOG_DIR, "test_failures.log")

EXPECTED_KEYS = {
    "top_anomalies",
    "cue_mismatches",
    "timeline",
    "tampered_entries"
}

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def log_failure(name, reason):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(FAILURE_LOG_PATH, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] ❌ {name}: {reason}\n")

def test_surveillance_response_structure(client):
    """Test /surveillance response structure and content."""
    response = client.get("/surveillance")
    assert response.status_code == 200, "Expected 200 OK from /surveillance"
    data = response.get_json()

    if not isinstance(data, dict):
        log_failure("test_surveillance_response_structure", "Response is not a dict")
        assert False

    missing = EXPECTED_KEYS - data.keys()
    if missing:
        log_failure("test_surveillance_response_structure", f"Missing keys: {missing}")
        assert False

    for key in EXPECTED_KEYS:
        if not isinstance(data[key], list):
            log_failure("test_surveillance_response_structure", f"{key} is not a list")
            assert False

def test_surveillance_raw_route(client):
    """Test /surveillance/raw route availability."""
    response = client.get("/surveillance/raw")
    assert response.status_code == 200, "Expected 200 OK from /surveillance/raw"
    data = response.get_json()
    assert "status" in data and data["status"] == "success"

    expected_keys = ["top_anomalies", "cue_mismatches", "timeline", "tampered_entries"]
    for key in expected_keys:
        assert key in data, f"Missing key: {key}"
        assert isinstance(data[key], list), f"{key} is not a list"