from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


class Merchant(BaseModel):
    merchant_id: str
    name: str
    language: Literal["hi", "mr", "en"]  # Hindi, Marathi, English
    category: str  # e.g. "kirana", "pharmacy", "restaurant"


class DecisionEvent(BaseModel):
    event_id: str
    merchant_id: str
    timestamp: datetime
    decision_type: Literal["discount", "inventory", "hours", "promo", "staffing"]
    description: str  # what the merchant did
    outcome: Literal["positive", "negative", "neutral"]
    revenue_delta: float  # change in revenue vs prior week (%)
    context: str  # season, festival, local event if known


class Suggestion(BaseModel):
    suggestion_id: str
    merchant_id: str
    type: Literal["failure_guard", "personal_best", "network_wisdom"]
    title: str  # short Hindi label
    body: str  # full Hindi explanation
    confidence: float  # 0.0 to 1.0
    action: str  # what the merchant should do
    voice_script: str  # exact text to pass to Sarvam TTS
    audio_url: Optional[str] = None  # populated by voice_node
