import base64
import os
import logging
from typing import Any, Dict, List, Union
import httpx

try:
    from backend.config import settings
    from backend.models import Suggestion
except ImportError:
    from config import settings
    from models import Suggestion



logger = logging.getLogger(__name__)

# Fallback minimal 0.5s silent/gentle WAV for demo resilience if API key is absent or network fails
FALLBACK_WAV_BASE64 = (
    "UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAAAP8A/w=="
)


def generate_tts_audio(voice_script: str, language_code: str = "hi-IN") -> str:
    """
    Calls Sarvam Bulbul v3 TTS API to generate audio for a given voice script.
    Returns a browser-playable base64 audio data URI.
    """
    api_key = settings.SARVAM_API_KEY.strip() if settings.SARVAM_API_KEY else ""

    if not api_key or api_key == "your_sarvam_api_key_here":
        logger.warning(
            "SARVAM_API_KEY not configured. Using fallback audio representation."
        )
        return f"data:audio/wav;base64,{FALLBACK_WAV_BASE64}"

    try:
        url = "https://api.sarvam.ai/text-to-speech"
        headers = {
            "API-Subscription-Key": api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "inputs": [voice_script],
            "target_language_code": language_code,
            "speaker": "shreya",
            "model": "bulbul:v3",
            "enable_preprocessing": True,
        }

        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            audios = data.get("audios", [])
            if audios and audios[0]:
                audio_b64 = audios[0]
                # Return playable data URI
                return f"data:audio/wav;base64,{audio_b64}"

    except Exception as e:
        logger.error(f"Error calling Sarvam TTS API: {e}")
        # Fallback for hackathon demo stability
        return f"data:audio/wav;base64,{FALLBACK_WAV_BASE64}"

    return f"data:audio/wav;base64,{FALLBACK_WAV_BASE64}"


def voice_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LangGraph node: processes suggestions in state and populates `audio_url`
    for each suggestion by calling Sarvam Bulbul v3 TTS API.
    """
    suggestions_raw = state.get("suggestions", [])
    merchant_lang = state.get("language", "hi")
    target_lang = "mr-IN" if merchant_lang == "mr" else ("en-IN" if merchant_lang == "en" else "hi-IN")

    updated_suggestions: List[Union[Suggestion, Dict[str, Any]]] = []

    for item in suggestions_raw:
        if isinstance(item, Suggestion):
            voice_script = item.voice_script
            audio_url = generate_tts_audio(voice_script, target_lang)
            # Update suggestion object
            item.audio_url = audio_url
            updated_suggestions.append(item)
        elif isinstance(item, dict):
            voice_script = item.get("voice_script", "")
            audio_url = generate_tts_audio(voice_script, target_lang)
            item["audio_url"] = audio_url
            updated_suggestions.append(item)
        else:
            updated_suggestions.append(item)

    return {"suggestions": updated_suggestions}
