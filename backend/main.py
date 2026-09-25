from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.config import settings
from backend.models import Suggestion
from backend.agent.graph import build_graph
from backend.agent.nodes.ingest_node import ingest_node
from backend.memory.cognee_client import cognee_client


# Request and Response schemas strictly conforming to BUILD.md contracts
class IngestRequest(BaseModel):
    merchant_id: str = "merchant_001"
    csv_data: Optional[str] = None


class IngestResponse(BaseModel):
    status: str = "ok"
    events_loaded: int


class SuggestionsResponse(BaseModel):
    suggestions: List[Suggestion]
    generated_at: datetime


class N8nTriggerRequest(BaseModel):
    merchant_id: str = "merchant_001"
    trigger: str = "weekly_check"


class N8nTriggerResponse(BaseModel):
    status: str = "triggered"


class VoiceRequest(BaseModel):
    suggestion_id: str


class VoiceResponse(BaseModel):
    audio_url: str
    duration_seconds: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan manager.
    Pre-initializes Cognee local storage and compiles the LangGraph instance once at startup.
    """
    print(f"Starting Vyapar Sarthi backend in {settings.ENVIRONMENT} mode...")
    await cognee_client.initialize()
    app.state.graph = build_graph()
    app.state.latest_suggestions = {}
    
    # Pre-seed demo merchant data at startup per INTEGRATION.md
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

# CORS middleware for Next.js frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    Invokes the full LangGraph pipeline (ingest -> pattern -> suggestion)
    and returns exactly 3 suggestions (failure_guard, personal_best, network_wisdom).
    """
    if not hasattr(app.state, "graph") or app.state.graph is None:
        app.state.graph = build_graph()

    result = await app.state.graph.ainvoke({"merchant_id": merchant_id})
    suggestions = result.get("suggestions", [])

    # Cache latest suggestions for voice route
    if not hasattr(app.state, "latest_suggestions"):
        app.state.latest_suggestions = {}
    app.state.latest_suggestions[merchant_id] = suggestions

    return SuggestionsResponse(
        suggestions=suggestions,
        generated_at=datetime.utcnow(),
    )


@app.post("/api/merchant/{merchant_id}/voice", response_model=VoiceResponse)
async def get_merchant_voice(merchant_id: str, req: VoiceRequest):
    """
    POST /api/merchant/{merchant_id}/voice
    Returns audio_url for a given suggestion_id.
    """
    latest = getattr(app.state, "latest_suggestions", {}).get(merchant_id, [])
    audio_url = ""
    for s in latest:
        if s.suggestion_id == req.suggestion_id:
            audio_url = s.audio_url or ""
            break

    return VoiceResponse(audio_url=audio_url, duration_seconds=5.0)


@app.post("/api/webhook/n8n/trigger", response_model=N8nTriggerResponse)
async def n8n_webhook_trigger(req: N8nTriggerRequest, background_tasks: BackgroundTasks):
    """
    POST /api/webhook/n8n/trigger
    Accepts n8n weekly trigger, immediately returns status='triggered',
    and invokes full LangGraph pipeline asynchronously in background.
    """
    async def async_graph_runner(m_id: str):
        if hasattr(app.state, "graph") and app.state.graph is not None:
            await app.state.graph.ainvoke({"merchant_id": m_id})

    background_tasks.add_task(async_graph_runner, req.merchant_id)
    return N8nTriggerResponse(status="triggered")
