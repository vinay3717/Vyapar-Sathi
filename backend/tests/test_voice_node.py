import pytest

try:
    from backend.models import Suggestion
    from backend.agent.nodes.voice_node import voice_node
except ImportError:
    from models import Suggestion
    from agent.nodes.voice_node import voice_node


def test_voice_node_populates_audio_url():
    suggestion = Suggestion(
        suggestion_id="sugg_001",
        merchant_id="merchant_001",
        type="failure_guard",
        title="सावधान: छूट न दें",
        body="पिछली बार 20% छूट देने पर बिक्री घटी थी।",
        confidence=0.88,
        action="इस हफ्ते छूट देने से बचें।",
        voice_script="नमस्ते राजू भाई। पिछली बार आपने बीस प्रतिशत डिस्काउंट दिया था, उससे कमाई घट गई थी।",
        audio_url=None,
    )

    state = {
        "merchant_id": "merchant_001",
        "suggestions": [suggestion],
    }

    result = voice_node(state)

    assert "suggestions" in result
    updated_suggestions = result["suggestions"]
    assert len(updated_suggestions) == 1
    assert updated_suggestions[0].audio_url is not None
    assert updated_suggestions[0].audio_url.startswith("data:audio/wav;base64,")


def test_voice_node_dict_handling():
    raw_dict = {
        "suggestion_id": "sugg_002",
        "merchant_id": "merchant_001",
        "type": "personal_best",
        "title": "सफलता दोहराएं",
        "body": "सुबह 7 बजे दुकान खोलने पर कमाई बढ़ी थी।",
        "confidence=0.92": 0.92,
        "action": "दुकान जल्दी खोलें।",
        "voice_script": "नमस्ते राजू भाई। सुबह जल्दी दुकान खोलने पर अच्छी कमाई हुई थी।",
    }

    state = {
        "merchant_id": "merchant_001",
        "suggestions": [raw_dict],
    }

    result = voice_node(state)
    assert result["suggestions"][0]["audio_url"] is not None
    assert len(result["suggestions"][0]["audio_url"]) > 20
