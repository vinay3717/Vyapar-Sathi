# BUILD_devesh.md — Devesh (Agent + Backend)
> ⚠️ AGENT INSTRUCTIONS: You are building ONLY the items in this file. Nothing else. Build exactly as specified.

---

## Your Scope

- FastAPI app setup (main.py, config.py, lifespan)
- Pydantic models (models.py)
- AgentState TypedDict (agent/state.py)
- LangGraph StateGraph with 3 nodes (agent/graph.py)
- ingest_node.py — loads merchant CSV into Cognee
- pattern_node.py — queries Cognee graph to detect failure and success patterns
- suggestion_node.py — calls Gemini to generate Suggestion objects from patterns
- Cognee client wrapper (memory/cognee_client.py)
- Mock transaction CSV (data/mock_transactions.csv)
- FastAPI routes: POST /api/merchant/ingest, GET /api/merchant/{merchant_id}/suggestions, POST /api/webhook/n8n/trigger

---

## Your Files

| File | Purpose |
|---|---|
| `backend/main.py` | FastAPI app, lifespan startup, route registration |
| `backend/config.py` | Pydantic-settings: GEMINI_API_KEY, COGNEE_API_KEY, COGNEE_GRAPH_URL, ENVIRONMENT, DEMO_MERCHANT_ID |
| `backend/models.py` | Merchant, DecisionEvent, Suggestion — exact shapes from BUILD.md |
| `backend/agent/state.py` | AgentState TypedDict |
| `backend/agent/graph.py` | LangGraph StateGraph builder |
| `backend/agent/nodes/ingest_node.py` | Parses CSV → DecisionEvent list → stores in Cognee |
| `backend/agent/nodes/pattern_node.py` | Queries Cognee → extracts failure patterns + personal bests + network wisdom |
| `backend/agent/nodes/suggestion_node.py` | Sends patterns to Gemini → returns Suggestion list with Hindi voice_script |
| `backend/memory/cognee_client.py` | Cognee SDK wrapper: store_events(), query_patterns(), query_network() |
| `backend/data/mock_transactions.csv` | Seed data for merchant_001 |

---

## Your Tasks (ordered by priority)

### Task 1: Bootstrap — config, models, FastAPI lifespan
- What to build: `config.py` with pydantic-settings, `models.py` with all three models, `main.py` with lifespan that initialises Cognee connection
- Files: `backend/config.py`, `backend/models.py`, `backend/main.py`
- Inputs: ENV vars from .env
- Outputs: Running FastAPI server on port 8000 with `/healthz` returning `{"status": "ok"}`
- Acceptance criteria: `curl localhost:8000/healthz` returns 200

### Task 2: Mock CSV + Cognee ingest
- What to build: A realistic mock CSV with 90 days of transaction data for merchant_001 (a kirana store in Mumbai). Columns: `date, amount, category, notes`. Include clear patterns: a failed 20% discount in week 3 (revenue dropped 30%), a successful early-morning hours extension in week 6 (revenue up 25%), a Diwali overstock in week 9 (waste noted in notes column). Then build `cognee_client.py` and `ingest_node.py` that reads the CSV and stores DecisionEvent objects into Cognee graph.
- Files: `backend/data/mock_transactions.csv`, `backend/memory/cognee_client.py`, `backend/agent/nodes/ingest_node.py`
- Inputs: CSV file path, merchant_id
- Outputs: DecisionEvent objects stored in Cognee; ingest_node returns `{"events_stored": N}`
- Acceptance criteria: After calling ingest_node, Cognee graph has at least 3 DecisionEvent nodes for merchant_001

### Task 3: AgentState + LangGraph graph
- What to build: `AgentState` TypedDict and the 3-node LangGraph `StateGraph`. Nodes in order: `ingest_node` → `pattern_node` → `suggestion_node`. The graph is compiled once at startup and stored on `app.state.graph`.
- Files: `backend/agent/state.py`, `backend/agent/graph.py`
- Inputs: None at build time; graph is invoked with `{"merchant_id": str}` at runtime
- Outputs: Compiled graph on `app.state.graph`
- Acceptance criteria: `app.state.graph.invoke({"merchant_id": "merchant_001"})` runs without error

### Task 4: pattern_node
- What to build: Queries Cognee graph for merchant_id. Returns three buckets: `failure_patterns` (decisions with negative outcome), `personal_bests` (decisions with positive outcome, revenue_delta > 15%), `network_wisdom` (mock — hardcoded list of 2-3 patterns from "similar kirana merchants", flagged as `source: "network"`). Returns these in AgentState.
- File: `backend/agent/nodes/pattern_node.py`
- Inputs: `state["merchant_id"]`, Cognee graph
- Outputs: `state["failure_patterns"]`, `state["personal_bests"]`, `state["network_wisdom"]`
- Acceptance criteria: For merchant_001, returns at least 1 failure_pattern (the week-3 discount) and 1 personal_best (the week-6 hours extension)

### Task 5: suggestion_node
- What to build: Takes the three pattern buckets. Calls Gemini 3.5 Flash with a structured prompt. Returns exactly 3 Suggestion objects — one per type (failure_guard, personal_best, network_wisdom). Each Suggestion must have a `voice_script` field in Hindi (Devanagari script), 2-3 sentences, addressed directly to the merchant as "Aap". Store suggestions in AgentState.
- File: `backend/agent/nodes/suggestion_node.py`
- Inputs: `state["failure_patterns"]`, `state["personal_bests"]`, `state["network_wisdom"]`
- Outputs: `state["suggestions"]` — list of 3 Suggestion objects
- Gemini prompt shape:
  ```
  You are an AI business advisor for Indian kirana merchants.
  Given these patterns, generate exactly 3 suggestions in JSON.
  Each must have: type, title (Hindi, 5 words max), body (Hindi, 2 sentences),
  confidence (0-1), action (Hindi imperative sentence), voice_script (Hindi, 2-3 sentences, start with "Namaste").
  Return only valid JSON array. No markdown.
  Patterns: {patterns}
  ```
- Acceptance criteria: Returns valid JSON array of 3 Suggestion objects; voice_script is in Hindi

### Task 6: FastAPI routes
- What to build: Three routes as specified in BUILD.md shared contracts.
  - `POST /api/merchant/ingest` — runs ingest_node standalone, returns events_loaded count
  - `GET /api/merchant/{merchant_id}/suggestions` — invokes full graph, returns suggestions list
  - `POST /api/webhook/n8n/trigger` — accepts n8n webhook, invokes full graph for given merchant_id, returns triggered status
- File: `backend/main.py` (add routes to existing app)
- Inputs: Request bodies as defined in BUILD.md
- Outputs: Response bodies as defined in BUILD.md
- Acceptance criteria: All three routes return 200 with correct shape; test with curl

---

## Contracts You Must Honor

- `models.py` shapes are frozen — do not change field names or types after Task 1
- `app.state.graph` is the only graph instance — never instantiate per-request
- `voice_script` field in Suggestion must be populated — teammate's voice_node depends on it
- `/api/merchant/{merchant_id}/suggestions` response shape: `{ suggestions: Suggestion[], generated_at: datetime }` — teammate's frontend depends on this exactly

---

## DO NOT
- Do not build voice_node.py — that is teammate's file
- Do not build any frontend files
- Do not build n8n workflow
- Do not call Sarvam API — that is teammate's responsibility
- Do not add auth middleware
- Do not add a PostgreSQL or Redis dependency — Cognee only
- Do not change shared contract definitions once models.py is written
- Do not add packages without updating BUILD.md first
