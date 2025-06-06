import pytest
import os
import json
from datetime import datetime

from BACKEND.core.app import app as flask_app
from BACKEND.security.lockdown_manager import unlock_system

LOG_DIR = os.path.join("BACKEND", "LOGS")
FAILURE_LOG_PATH = os.path.join(LOG_DIR, "test_failures.log")

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def ensure_clean_lock_state():
    unlock_system()
    yield
    # Leave post-test lockdown state up to individual test if needed

def log_failure(name: str, reason: str):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(FAILURE_LOG_PATH, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] ❌ {name}: {reason}\n")