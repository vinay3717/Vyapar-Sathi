# BUILD.md — Vyapar Sarthi
> ⚠️ AGENT INSTRUCTIONS: Build ONLY what is listed here. Do not add features, do not infer requirements, do not improve on the spec. If something is unclear, output a comment `// UNCLEAR: [question]` and stop. Do not proceed past unclear points.

---

## Project Overview

Vyapar Sarthi is an autonomous AI teammate embedded in a Paytm merchant's workflow. It builds a causal memory of every merchant's past decisions — what failed, what worked, what similar merchants did — and proactively surfaces the next best action before the merchant even asks, delivered in their own language via voice.

The system has three capabilities: **Failure Guard** (warns before repeating a past mistake), **Personal Best Replay** (recommends recreating a merchant's own past high-performing patterns), and **Network Wisdom** (shows what similar merchants did in the same situation). All three feed into a single voice note delivered in Hindi/Marathi.

**Track:** Track 3 — Autonomous AI Teammates
**Hackathon:** Paytm Build for India AI Hackathon — Mumbai Edition
**Team:** Kairos
**Event date:** Oct 3, 2026 (8 hours)

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Agent orchestration | LangGraph | 1.2.1 |
| LLM | Gemini 3.5 Flash | latest |
| Memory / knowledge graph | Cognee | latest (pip install cognee) |
| Workflow triggers | n8n | latest (self-hosted or cloud) |
| Voice output | Sarvam Bulbul v3 TTS API | latest |
| Backend | FastAPI | 0.115.x |
| Frontend | Next.js | 14 App Router |
| Data | Mock Paytm transaction CSV | — |
| Language | Python 3.11+ | — |
| Dependency management | uv + pyproject.toml | — |

---

## Shared Contracts (ALL agents must honor these)

### Data Models

```python
# Merchant
class Merchant(BaseModel):
    merchant_id: str
    name: str
    language: Literal["hi", "mr", "en"]  # Hindi, Marathi, English
    category: str  # e.g. "kirana", "pharmacy", "restaurant"

# Decision Event (stored in Cognee graph)
class DecisionEvent(BaseModel):
    event_id: str
    merchant_id: str
    timestamp: datetime
    decision_type: Literal["discount", "inventory", "hours", "promo", "staffing"]
    description: str          # what the merchant did
    outcome: Literal["positive", "negative", "neutral"]
    revenue_delta: float      # change in revenue vs prior week (%)
    context: str              # season, festival, local event if known

# Agent Suggestion
class Suggestion(BaseModel):
    suggestion_id: str
    merchant_id: str
    type: Literal["failure_guard", "personal_best", "network_wisdom"]
    title: str                # short Hindi label
    body: str                 # full Hindi explanation
    confidence: float         # 0.0 to 1.0
    action: str               # what the merchant should do
    voice_script: str         # exact text to pass to Sarvam TTS
```

### API Endpoints

```
POST /api/merchant/ingest
  Body: { merchant_id: str, csv_data: str (base64) }
  Response: { status: "ok", events_loaded: int }
  Auth: None (demo mode)

GET /api/merchant/{merchant_id}/suggestions
  Response: { suggestions: Suggestion[], generated_at: datetime }
  Auth: None (demo mode)

POST /api/merchant/{merchant_id}/voice
  Body: { suggestion_id: str }
  Response: { audio_url: str, duration_seconds: float }
  Auth: None (demo mode)

POST /api/webhook/n8n/trigger
  Body: { merchant_id: str, trigger: "weekly_check" }
  Response: { status: "triggered" }
  Auth: None (demo mode)
```

### Environment Variables

```env
# LLM
GEMINI_API_KEY=                    # owned by: Devesh

# Memory
COGNEE_API_KEY=                    # owned by: Devesh
COGNEE_GRAPH_URL=                  # owned by: Devesh

# Voice
SARVAM_API_KEY=                    # owned by: Teammate

# Workflow
N8N_WEBHOOK_URL=                   # owned by: Teammate

# App
ENVIRONMENT=development            # owned by: both
DEMO_MERCHANT_ID=merchant_001      # owned by: both
```

### File Structure

```
vyapar-sarthi/
├── backend/
│   ├── pyproject.toml
│   ├── main.py                    # FastAPI app + lifespan
│   ├── config.py                  # pydantic-settings config
│   ├── models.py                  # shared Pydantic models
│   ├── agent/
│   │   ├── graph.py               # LangGraph StateGraph (Devesh)
│   │   ├── nodes/
│   │   │   ├── ingest_node.py     # loads CSV into Cognee (Devesh)
│   │   │   ├── pattern_node.py    # detects failure patterns (Devesh)
│   │   │   ├── suggestion_node.py # generates suggestions (Devesh)
│   │   │   └── voice_node.py      # calls Sarvam TTS (Teammate)
│   │   └── state.py               # AgentState TypedDict
│   ├── memory/
│   │   └── cognee_client.py       # Cognee graph operations (Devesh)
│   └── data/
│       └── mock_transactions.csv  # seed data (both)
├── frontend/
│   ├── package.json
│   ├── app/
│   │   ├── page.tsx               # merchant dashboard (Teammate)
│   │   ├── components/
│   │   │   ├── SuggestionCard.tsx # renders one suggestion (Teammate)
│   │   │   ├── VoicePlayer.tsx    # plays audio from Sarvam (Teammate)
│   │   │   └── MerchantHeader.tsx # name + category (Teammate)
│   │   └── api/
│   │       └── suggestions/
│   │           └── route.ts       # proxies to FastAPI (Teammate)
└── n8n/
    └── workflow.json              # n8n webhook trigger (Teammate)
```

---

## Team Overview

| Teammate | Role | Owns | Integrates With |
|---|---|---|---|
| Devesh | Agent / Backend | LangGraph graph, all nodes except voice_node, Cognee client, FastAPI routes for /ingest and /suggestions, mock CSV data | Hands off: Suggestion[] to voice_node; AgentState to frontend via /suggestions endpoint |
| Teammate | Frontend / Infra | Next.js dashboard, SuggestionCard, VoicePlayer, voice_node.py, n8n workflow, Sarvam TTS API calls, /voice endpoint | Receives: Suggestion[] from /suggestions; sends audio_url back to frontend |

---

## DO NOT Section (applies to all agents)

- Do not add any feature not listed in this document
- Do not change shared contract definitions — models.py is frozen once written
- Do not rename files or folders listed in the file structure
- Do not install packages not listed in the tech stack
- Do not use your own judgment to "improve" the code
- Do not add authentication beyond what is specified (none, demo mode)
- Do not add a database — Cognee is the only persistence layer
- Do not use `@app.on_event` — use lifespan only
- Do not import from `cognee (Cognee replaces this — no langchain_community)` for vector store — not needed here
- Do not build real Paytm API integration — mock CSV is sufficient for demo
