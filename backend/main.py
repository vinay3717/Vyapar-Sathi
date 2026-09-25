import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Dict, List, Optional

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.config import settings
from backend.models import Suggestion
from backend.agent.graph import build_graph
from backend.agent.nodes.ingest_node import ingest_node
from backend.agent.nodes.voice_node import voice_node, generate_tts_audio
from backend.memory.cognee_client import cognee_client


# ==============================================================================
# Shared Request / Response Schemas strictly honoring BUILD.md
# ==============================================================================
class IngestRequest(BaseModel):
    merchant_id: str = "merchant_001"
    csv_data: Optional[str] = None


class IngestResponse(BaseModel):
    status: str = "ok"
    events_loaded: int


class SuggestionsResponse(BaseModel):
    suggestions: List[Suggestion]
    generated_at: datetime


class VoiceRequest(BaseModel):
    suggestion_id: str


class VoiceResponse(BaseModel):
    audio_url: str
    duration_seconds: float = 5.0


class N8nTriggerRequest(BaseModel):
    merchant_id: str = "merchant_001"
    trigger: str = "weekly_check"


class N8nTriggerResponse(BaseModel):
    status: str = "triggered"


# Demo suggestions seed for Raju Kirana (merchant_001) per INTEGRATION.md
DEMO_SUGGESTIONS: List[Suggestion] = [
    Suggestion(
        suggestion_id="sugg_001",
        merchant_id="merchant_001",
        type="failure_guard",
        title="⚠️ 20% छूट न दें",
        body="तीन हफ्ते पहले 20% छूट देने पर आपकी कमाई 35% घट गई थी। इस हफ्ते भी छूट देने से बचें।",
        confidence=0.91,
        action="इस हफ्ते सामान सामान्य दर पर ही बेचें।",
        voice_script="नमस्ते राजू भाई। पिछली बार आपने 20% डिस्काउंट दिया था — उस हफ्ते कमाई 35% कम हो गई थी। इस बार डिस्काउंट मत दीजिए।",
    ),
    Suggestion(
        suggestion_id="sugg_002",
        merchant_id="merchant_001",
        type="personal_best",
        title="✅ सुबह 7 बजे खोलें",
        body="छह हफ्ते पहले सुबह 7 बजे दुकान खोलने पर आपकी कमाई 25% बढ़ गई थी। इसे फिर दोहराएं।",
        confidence=0.88,
        action="दुकान सुबह 7:00 बजे खोलें।",
        voice_script="नमस्ते राजू भाई। छह हफ्ते पहले जब आपने सुबह 7 बजे दुकान खोली थी, उस हफ्ते कमाई 25% बढ़ गई थी। अगले हफ्ते फिर से जल्दी खोलने की कोशिश करें।",
    ),
    Suggestion(
        suggestion_id="sugg_003",
        merchant_id="merchant_001",
        type="network_wisdom",
        title="🌐 दूध व नाश्ता कॉम्बो",
        body="मुंबई के 1,800 किराना व्यापारियों ने सुबह के समय ब्रेड-दूध कॉम्बो से 18% ज्यादा बिक्री की है।",
        confidence=0.85,
        action="सुबह के समय ब्रेड और दूध का कॉम्बो पैक काउंटर पर रखें।",
        voice_script="नमस्ते राजू भाई। मुंबई के आसपास के किराना व्यापारियों ने सुबह दूध और ब्रेड का कॉम्बो रखकर बिक्री 18% बढ़ाई है। आप भी इसे आज़माएं।",
    ),
]


# ==============================================================================
# Lifespan Management
# ==============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan manager:
    Initializes Cognee local storage, compiles 4-node LangGraph, and pre-seeds demo data.
    """
    print(f"Starting Vyapar Sarthi backend in {settings.ENVIRONMENT} mode...")
    await cognee_client.initialize()
    app.state.graph = build_graph()
    app.state.latest_suggestions: Dict[str, List[Suggestion]] = {}
    app.state.cached_suggestions: Dict[str, Suggestion] = {}

    # Initialize cache with demo suggestions and their audio
    demo_state = {
        "merchant_id": settings.DEMO_MERCHANT_ID,
        "suggestions": [s.model_copy() for s in DEMO_SUGGESTIONS],
    }
    try:
        processed = voice_node(demo_state)
        demo_list = processed.get("suggestions", [])
        app.state.latest_suggestions[settings.DEMO_MERCHANT_ID] = demo_list
        for s in demo_list:
            if isinstance(s, Suggestion):
                app.state.cached_suggestions[s.suggestion_id] = s
    except Exception as e:
        print(f"Notice: pre-processing demo audio in lifespan: {e}")

    # Pre-seed demo merchant CSV data into Cognee
    try:
        await ingest_node({"merchant_id": settings.DEMO_MERCHANT_ID})
        print(f"Pre-loaded demo merchant data for {settings.DEMO_MERCHANT_ID}")
    except Exception as e:
        print(f"Notice: pre-seeding startup data: {e}")

    yield

    print("Shutting down Vyapar Sarthi backend...")


app = FastAPI(
    title="Vyapar Sarthi API",
    description="Autonomous AI Teammate for Paytm Merchants",
    version="1.0.0",
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


# ==============================================================================
# Endpoints
# ==============================================================================
@app.get("/healthz")
async def healthz():
    """Liveness probe returning 200 ok."""
    return {"status": "ok"}


@app.post("/api/merchant/ingest", response_model=IngestResponse)
async def ingest_merchant(req: Optional[IngestRequest] = None):
    """
    POST /api/merchant/ingest
    Runs ingest_node standalone, stores DecisionEvents in Cognee graph, and returns count.
    """
    merchant_id = req.merchant_id if req else settings.DEMO_MERCHANT_ID
    csv_data = req.csv_data if req else None

    result = await ingest_node({"merchant_id": merchant_id, "csv_data": csv_data})
    events_loaded = result.get("events_stored", 0)
    return IngestResponse(status="ok", events_loaded=events_loaded)


@app.get("/api/merchant/{merchant_id}/suggestions", response_model=SuggestionsResponse)
async def get_merchant_suggestions(merchant_id: str):
    """
    GET /api/merchant/{merchant_id}/suggestions
    Invokes the full LangGraph pipeline (ingest -> pattern -> suggestion -> voice)
    and returns exactly 3 suggestions (failure_guard, personal_best, network_wisdom).
    """
    if not hasattr(app.state, "graph") or app.state.graph is None:
        app.state.graph = build_graph()

    try:
        result = await app.state.graph.ainvoke({"merchant_id": merchant_id})
        suggestions = result.get("suggestions", [])
    except Exception as e:
        print(f"Notice: Error invoking graph for {merchant_id}, using fallback: {e}")
        suggestions = getattr(app.state, "latest_suggestions", {}).get(merchant_id, DEMO_SUGGESTIONS)

    if not suggestions:
        suggestions = DEMO_SUGGESTIONS

    # Update cache
    if not hasattr(app.state, "latest_suggestions"):
        app.state.latest_suggestions = {}
    if not hasattr(app.state, "cached_suggestions"):
        app.state.cached_suggestions = {}

    app.state.latest_suggestions[merchant_id] = suggestions
    for s in suggestions:
        if isinstance(s, Suggestion):
            app.state.cached_suggestions[s.suggestion_id] = s

    return SuggestionsResponse(
        suggestions=suggestions,
        generated_at=datetime.now(timezone.utc),
    )


@app.post("/api/merchant/{merchant_id}/voice", response_model=VoiceResponse)
async def get_merchant_voice(merchant_id: str, req: VoiceRequest):
    """
    POST /api/merchant/{merchant_id}/voice
    Finds suggestion by ID in cached/graph results and returns audio_url.
    Body: { suggestion_id: str }
    Response: { audio_url: str, duration_seconds: float }
    """
    cached = getattr(app.state, "cached_suggestions", {})
    suggestion = cached.get(req.suggestion_id)

    if not suggestion:
        # Check in latest_suggestions for this merchant
        merchant_suggestions = getattr(app.state, "latest_suggestions", {}).get(merchant_id, [])
        suggestion = next((s for s in merchant_suggestions if s.suggestion_id == req.suggestion_id), None)

    if not suggestion:
        # Check DEMO_SUGGESTIONS
        found = next((s for s in DEMO_SUGGESTIONS if s.suggestion_id == req.suggestion_id), None)
        if found:
            audio = generate_tts_audio(found.voice_script)
            suggestion = found.model_copy(update={"audio_url": audio})
            cached[found.suggestion_id] = suggestion
        else:
            raise HTTPException(status_code=404, detail=f"Suggestion {req.suggestion_id} not found")

    audio_url = suggestion.audio_url or generate_tts_audio(suggestion.voice_script)

    return VoiceResponse(
        audio_url=audio_url,
        duration_seconds=5.0,
    )


@app.post("/api/webhook/n8n/trigger", response_model=N8nTriggerResponse)
async def n8n_webhook_trigger(req: N8nTriggerRequest, background_tasks: BackgroundTasks):
    """
    POST /api/webhook/n8n/trigger
    Accepts n8n weekly trigger, immediately returns status='triggered',
    and invokes full LangGraph pipeline asynchronously in background.
    """
    async def async_graph_runner(m_id: str):
        if hasattr(app.state, "graph") and app.state.graph is not None:
            try:
                await app.state.graph.ainvoke({"merchant_id": m_id})
            except Exception as e:
                print(f"Error in background async_graph_runner: {e}")

    background_tasks.add_task(async_graph_runner, req.merchant_id)
    return N8nTriggerResponse(status="triggered")
