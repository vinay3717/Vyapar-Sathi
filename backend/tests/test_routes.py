import pytest
from fastapi.testclient import TestClient
from backend.main import app, lifespan


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_healthz_route(client):
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_ingest_route(client):
    res = client.post("/api/merchant/ingest", json={"merchant_id": "merchant_001"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["events_loaded"] >= 3


def test_suggestions_route(client):
    res = client.get("/api/merchant/merchant_001/suggestions")
    assert res.status_code == 200
    data = res.json()
    assert "suggestions" in data
    assert "generated_at" in data
    
    suggestions = data["suggestions"]
    assert len(suggestions) == 3
    
    types = {s["type"] for s in suggestions}
    assert types == {"failure_guard", "personal_best", "network_wisdom"}

    for s in suggestions:
        assert s["merchant_id"] == "merchant_001"
        assert len(s["title"]) > 0
        assert len(s["body"]) > 0
        assert len(s["action"]) > 0
        assert len(s["voice_script"]) > 0
        assert s["audio_url"] is None


def test_voice_route(client):
    # First call suggestions to populate cache
    sug_res = client.get("/api/merchant/merchant_001/suggestions")
    sug_id = sug_res.json()["suggestions"][0]["suggestion_id"]

    # Now call voice route
    voice_res = client.post(
        "/api/merchant/merchant_001/voice",
        json={"suggestion_id": sug_id}
    )
    assert voice_res.status_code == 200
    data = voice_res.json()
    assert "audio_url" in data
    assert "duration_seconds" in data


def test_n8n_webhook_trigger_route(client):
    res = client.post(
        "/api/webhook/n8n/trigger",
        json={"merchant_id": "merchant_001", "trigger": "weekly_check"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data == {"status": "triggered"}
