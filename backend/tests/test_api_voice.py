from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_post_voice_endpoint():
    with TestClient(app) as test_client:
        response = test_client.post(
            "/api/merchant/merchant_001/voice",
            json={"suggestion_id": "sugg_001"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "audio_url" in data
        assert "duration_seconds" in data
        assert data["audio_url"].startswith("data:audio/wav;base64,")


def test_get_suggestions_endpoint():
    with TestClient(app) as test_client:
        response = test_client.get("/api/merchant/merchant_001/suggestions")
        assert response.status_code == 200
        data = response.json()
        assert "suggestions" in data
        assert len(data["suggestions"]) >= 3
