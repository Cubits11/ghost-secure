import pytest, time, os, json
from BACKEND.security.lockdown_manager import lock_system, unlock_system, is_locked, LOCKDOWN_FILE

def read_lock_file():
    if os.path.exists(LOCKDOWN_FILE):
        with open(LOCKDOWN_FILE, "r") as f:
            return json.load(f)
    return {"locked": False}

@pytest.fixture(autouse=True)
def ensure_unlocked_before_and_after():
    """Ensure we start and end every test unlocked."""
    unlock_system()
    yield
    unlock_system()

def test_toggle_lockdown(client):
    """Toggle lockdown and verify response format."""
    response = client.post("/toggle_lockdown")
    assert response.status_code == 200
    data = response.get_json()
    assert "enabled" in data
    assert isinstance(data["enabled"], bool)

def test_lockdown_blocks_journal(client):
    """Ensure /journal is blocked while in lockdown."""
    lock_system("Test initiated")
    time.sleep(0.2)  # give time to write file

    print("\n🔒 is_locked():", is_locked())
    print("🔒 lock file contents:", read_lock_file())

    response = client.post("/journal", json={"entry": "test entry", "mode": "ghost"})
    print("📡 response code:", response.status_code)
    print("📡 response data:", response.get_json())

    assert response.status_code == 403
    assert "error" in response.get_json()

def test_unlock_allows_journal(client):
    """Ensure journal entry is accepted when unlocked."""
    unlock_system()
    time.sleep(0.1)

    response = client.post("/journal", json={"entry": "hello again", "mode": "ghost"})
    assert response.status_code == 200
    assert "ghost_response" in response.get_json()

def test_reset_denied_when_locked(client):
    """Ensure /reset is blocked during lockdown."""
    lock_system("Test initiated")
    time.sleep(0.2)

    print("\n🔒 is_locked():", is_locked())
    print("🔒 lock file contents:", read_lock_file())

    response = client.get("/reset")
    print("📡 response code:", response.status_code)
    print("📡 response data:", response.get_json())

    assert response.status_code == 403
    assert "error" in response.get_json()

def test_reset_works_when_unlocked(client):
    """Ensure /reset works when unlocked."""
    unlock_system()
    time.sleep(0.1)

    response = client.get("/reset")
    assert response.status_code == 200
    assert "message" in response.get_json()