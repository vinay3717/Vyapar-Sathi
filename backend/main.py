import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import settings
from models import Merchant, Suggestion
from agent.nodes.voice_node import voice_node, generate_tts_audio


# Request/Response schemas
class VoiceRequest(BaseModel):
    suggestion_id: str


class VoiceResponse(BaseModel):
    audio_url: str
    duration_seconds: float


class IngestRequest(BaseModel):
    merchant_id: str
    csv_data: str


class TriggerRequest(BaseModel):
    merchant_id: str
    trigger: str = "weekly_check"


class SuggestionsResponse(BaseModel):
    suggestions: List[Suggestion]
    generated_at: datetime


# Demo seed suggestions for Raju Kirana (merchant_001) as detailed in INTEGRATION.md
DEMO_SUGGESTIONS: List[Suggestion] = [
    Suggestion(
        suggestion_id="sugg_001",
        merchant_id="merchant_001",
        type="failure_guard",
        title="⚠️ सावधान: 20% छूट न दें",
        body="तीन हफ्ते पहले 20% छूट देने पर आपकी कमाई 35% घट गई थी। इस हफ्ते भी छूट देने से बचें।",
        confidence=0.91,
        action="इस हफ्ते सामान सामान्य दर पर ही बेचें।",
        voice_script="नमस्ते राजू भाई। पिछली बार आपने 20% डिस्काउंट दिया था — उस हफ्ते कमाई 35% कम हो गई थी। इस बार डिस्काउंट मत दीजिए।",
    ),
    Suggestion(
        suggestion_id="sugg_002",
        merchant_id="merchant_001",
        type="personal_best",
        title="✅ आपकी सफलता: सुबह 7 बजे खोलें",
        body="छह हफ्ते पहले सुबह 7 बजे दुकान खोलने पर आपकी कमाई 25% बढ़ गई थी। इसे फिर दोहराएं।",
        confidence=0.88,
        action="दुकान सुबह 7:00 बजे खोलें।",
        voice_script="नमस्ते राजू भाई। छह हफ्ते पहले जब आपने सुबह 7 बजे दुकान खोली थी, उस हफ्ते कमाई 25% बढ़ गई थी। अगले हफ्ते फिर से जल्दी खोलने की कोशिश करें।",
    ),
    Suggestion(
        suggestion_id="sugg_003",
        merchant_id="merchant_001",
        type="network_wisdom",
        title="🌐 आसपास के व्यापारी: दूध व नाश्ता कॉम्बो",
        body="मुंबई के 1,800 किराना व्यापारियों ने सुबह के समय ब्रेड-दूध कॉम्बो से 18% ज्यादा बिक्री की है।",
        confidence=0.85,
        action="सुबह के समय ब्रेड और दूध का कॉम्बो पैक काउंटर पर रखें।",
        voice_script="नमस्ते राजू भाई। मुंबई के आसपास के किराना व्यापारियों ने सुबह दूध और ब्रेड का कॉम्बो रखकर बिक्री 18% बढ़ाई है। आप भी इसे आज़माएं।",
    ),
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager:
    Initializes state, pre-generates/caches audio for demo suggestions.
    """
    app.state.cached_suggestions: Dict[str, Suggestion] = {}

    # Pre-populate demo suggestions with voice_node audio
    state = {
        "merchant_id": settings.DEMO_MERCHANT_ID,
        "suggestions": [s.model_copy() for s in DEMO_SUGGESTIONS],
    }
    processed = voice_node(state)
    for sugg in processed.get("suggestions", []):
        app.state.cached_suggestions[sugg.suggestion_id] = sugg

    yield


app = FastAPI(
    title="Vyapar Sarthi API",
    description="Autonomous AI Teammate for Paytm Merchants",
    version="0.1.0",
    lifespan=lifespan,
)

# Enable CORS for Next.js frontend (default port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def healthz():
    """Health check endpoint as defined in BUILD_devesh.md Task 1 GATE."""
    return {"status": "ok"}


# ==============================================================================
# Teammate Scope: Task 2 Route
# ==============================================================================
@app.post("/api/merchant/{merchant_id}/voice", response_model=VoiceResponse)
async def get_merchant_voice(merchant_id: str, request: VoiceRequest):
    """
    Finds suggestion by ID in cached/graph results and returns audio_url.
    Matches contract: POST /api/merchant/{merchant_id}/voice
    Body: { suggestion_id: str }
    Response: { audio_url: str, duration_seconds: float }
    """
    cached = getattr(app.state, "cached_suggestions", {})
    suggestion = cached.get(request.suggestion_id)

    if not suggestion:
        # Check if suggestion exists in DEMO_SUGGESTIONS
        found = next((s for s in DEMO_SUGGESTIONS if s.suggestion_id == request.suggestion_id), None)
        if found:
            audio = generate_tts_audio(found.voice_script)
            cached[found.suggestion_id] = found.model_copy(update={"audio_url": audio})
            suggestion = cached[found.suggestion_id]
        else:
            raise HTTPException(status_code=404, detail=f"Suggestion {request.suggestion_id} not found")

    audio_url = suggestion.audio_url or generate_tts_audio(suggestion.voice_script)

    return VoiceResponse(
        audio_url=audio_url,
        duration_seconds=5.0,  # approximate duration for demo snippet
    )


# ==============================================================================
# Suggestions & Webhook Endpoints (Honoring BUILD.md Contracts)
# ==============================================================================
@app.get("/api/merchant/{merchant_id}/suggestions", response_model=SuggestionsResponse)
async def get_suggestions(merchant_id: str):
    """
    Returns suggestions for given merchant.
    Matches contract: GET /api/merchant/{merchant_id}/suggestions
    Response: { suggestions: Suggestion[], generated_at: datetime }
    """
    cached = getattr(app.state, "cached_suggestions", {})
    merchant_suggestions = [
        s for s in cached.values() if s.merchant_id == merchant_id
    ]

    if not merchant_suggestions:
        merchant_suggestions = DEMO_SUGGESTIONS

    return SuggestionsResponse(
        suggestions=merchant_suggestions,
        generated_at=datetime.now(timezone.utc),
    )


@app.post("/api/merchant/ingest")
async def ingest_merchant_csv(payload: IngestRequest):
    """Ingest CSV endpoint stub for frontend/integration readiness."""
    return {"status": "ok", "events_loaded": 12}


@app.post("/api/webhook/n8n/trigger")
async def n8n_trigger(payload: TriggerRequest):
    """Webhook triggered by n8n workflow."""
    return {"status": "triggered"}
