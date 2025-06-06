def test_status(client):
    """Ensure lockdown status endpoint is reachable and returns a boolean."""
    res = client.get("/core_status")
    assert res.status_code == 200
    json_data = res.get_json()
    assert "lockdown" in json_data
    assert isinstance(json_data["lockdown"], bool)