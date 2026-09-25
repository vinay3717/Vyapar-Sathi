from datetime import datetime
from fastapi.testclient import TestClient
from backend.config import settings
from backend.models import Merchant, DecisionEvent, Suggestion
from backend.main import app


client = TestClient(app)


def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_config_loaded():
    assert settings.DEMO_MERCHANT_ID == "merchant_001"
    assert settings.ENVIRONMENT == "development"
    assert settings.GEMINI_API_KEY != ""


def test_models():
    merchant = Merchant(
        merchant_id="merchant_001",
        name="Raju Kirana",
        language="hi",
        category="kirana",
    )
    assert merchant.merchant_id == "merchant_001"

    event = DecisionEvent(
        event_id="evt_001",
        merchant_id="merchant_001",
        timestamp=datetime.now(),
        decision_type="discount",
        description="20% flat discount on all items",
        outcome="negative",
        revenue_delta=-30.0,
        context="Week 3 Monsoon",
    )
    assert event.outcome == "negative"
    assert event.revenue_delta == -30.0

    suggestion = Suggestion(
        suggestion_id="sug_001",
        merchant_id="merchant_001",
        type="failure_guard",
        title="डिस्काउंट से बचें",
        body="पिछली बार 20% डिस्काउंट देने पर कमाई 30% कम हो गई थी।",
        confidence=0.95,
        action="इस हफ्ते डिस्काउंट न दें।",
        voice_script="नमस्ते राजू भाई। पिछली बार 20% डिस्काउंट देने पर कमाई 30% कम हो गई थी।",
    )
    assert suggestion.type == "failure_guard"
    assert suggestion.audio_url is None
