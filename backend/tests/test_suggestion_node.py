import pytest
from backend.agent.nodes.ingest_node import ingest_node
from backend.agent.nodes.pattern_node import pattern_node
from backend.agent.nodes.suggestion_node import suggestion_node


@pytest.mark.asyncio
async def test_suggestion_node_generates_three_hindi_suggestions():
    # Ingest and extract patterns
    await ingest_node({"merchant_id": "merchant_001"})
    patterns = await pattern_node({"merchant_id": "merchant_001"})

    state = {
        "merchant_id": "merchant_001",
        "failure_patterns": patterns["failure_patterns"],
        "personal_bests": patterns["personal_bests"],
        "network_wisdom": patterns["network_wisdom"],
    }

    result = await suggestion_node(state)
    assert "suggestions" in result
    suggestions = result["suggestions"]
    assert len(suggestions) == 3

    types = {s.type for s in suggestions}
    assert "failure_guard" in types
    assert "personal_best" in types
    assert "network_wisdom" in types

    for s in suggestions:
        assert s.merchant_id == "merchant_001"
        assert len(s.title) > 0
        assert len(s.body) > 0
        assert 0.0 <= s.confidence <= 1.0
        assert len(s.action) > 0
        assert len(s.voice_script) > 0
        # Voice script should start with Namaste / नमस्ते or contain greeting
        assert any(greeting in s.voice_script.lower() or greeting in s.voice_script for greeting in ["namaste", "नमस्ते"])
        assert s.audio_url is None  # Waiting for voice_node
