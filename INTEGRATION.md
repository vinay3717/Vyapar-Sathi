# INTEGRATION.md — Merge Rules & Interface Contracts

> This document defines how the pieces come together. Read this before merging any branch.

---

## Integration Order

1. **Devesh: Task 1** — Bootstrap (config, models, FastAPI lifespan). GATE: `/healthz` returns 200. Nothing else starts until this passes.
2. **Devesh: Task 2** — Mock CSV + Cognee ingest. GATE: Cognee has DecisionEvent nodes for merchant_001.
3. **Devesh: Task 3** — AgentState + LangGraph graph. GATE: `graph.invoke({"merchant_id": "merchant_001"})` runs without error (even if nodes are stubs).
4. **Devesh: Tasks 4+5** — pattern_node + suggestion_node. GATE: `/api/merchant/merchant_001/suggestions` returns 3 Suggestion objects with `voice_script` populated and `audio_url: null`.
5. **Teammate: Task 1** — voice_node.py. Devesh adds it to the graph after handoff. GATE: Suggestions now have `audio_url` populated.
6. **Teammate: Tasks 2-6** — Frontend + n8n. Can run in parallel with steps 3-4. GATE: Dashboard loads, cards render, Play button works.
7. **Full integration test** — n8n trigger → backend → Cognee → Gemini → Sarvam → frontend plays audio. Run this 2x from reset before demo.

---

## Interface Contracts

### Contract 1: suggestion_node → voice_node
- suggestion_node writes `state["suggestions"]` as `List[Suggestion]`
- Each Suggestion has `voice_script: str` (Hindi, non-empty)
- Each Suggestion has `audio_url: None` (voice_node fills this)
- voice_node reads `state["suggestions"]`, populates `audio_url`, writes back

### Contract 2: FastAPI /suggestions → Next.js frontend
- FastAPI returns: `{ "suggestions": [...], "generated_at": "ISO datetime" }`
- Each suggestion object matches the Suggestion Pydantic model exactly
- Next.js `/api/suggestions/route.ts` proxies without transformation
- Frontend SuggestionCard receives `suggestion: Suggestion` prop directly

### Contract 3: n8n → FastAPI webhook
- n8n POSTs to `POST /api/webhook/n8n/trigger`
- Body: `{ "merchant_id": "merchant_001", "trigger": "weekly_check" }`
- FastAPI returns: `{ "status": "triggered" }`
- FastAPI then invokes graph async — n8n does not wait for completion

---

## Branch Naming

```
main
├── devesh/bootstrap
├── devesh/ingest
├── devesh/graph
├── devesh/patterns
├── devesh/suggestions
├── teammate/voice-node
├── teammate/frontend
└── teammate/n8n
```

Merge order follows Integration Order above. Devesh merges his branches. Teammate merges theirs. No cross-merges.

---

## What to Test Before Merging

**Devesh before each merge:**
- [ ] `uv run pytest` passes (write one smoke test per task)
- [ ] FastAPI routes return correct response shape (curl test)
- [ ] No imports from banned packages (cognee (Cognee replaces this — no langchain_community), @app.on_event)

**Teammate before each merge:**
- [ ] voice_node returns non-empty audio_url for a Hindi voice_script
- [ ] Dashboard loads without console errors
- [ ] SuggestionCard renders for all 3 types
- [ ] VoicePlayer plays audio without errors

---

## What Each Agent Must NOT Touch

| File/Module | Owner | Others must not modify |
|---|---|---|
| `models.py` | Devesh | Frozen after Task 1 — nobody changes it |
| `cognee_client.py` | Devesh | Teammate does not touch |
| `graph.py` | Devesh | Teammate does not touch (Devesh adds voice_node to graph after handoff) |
| `pattern_node.py` | Devesh | Teammate does not touch |
| `suggestion_node.py` | Devesh | Teammate does not touch |
| `voice_node.py` | Teammate | Devesh does not touch (only adds reference in graph.py) |
| `frontend/` (all) | Teammate | Devesh does not touch |
| `n8n/workflow.json` | Teammate | Devesh does not touch |

---

## Demo Path (step by step)

> Every step here maps to someone's code. Know whose before the demo.

1. **[Teammate's frontend]** Judge opens dashboard — `page.tsx` loads, `MerchantHeader` shows "Raju Kirana, Mumbai"
2. **[Devesh's FastAPI + graph]** Page auto-fetches `/api/suggestions` → LangGraph runs: ingest → pattern → suggestion
3. **[Devesh's suggestion_node + Teammate's voice_node]** 3 Suggestion cards appear — one red (⚠️ सावधान), one green (✅ आपकी सफलता), one blue (🌐 आसपास के व्यापारी)
4. **[Demo narration]** "Three weeks ago, Raju ran a 20% discount. Revenue dropped 35%. The agent remembers."
5. **[Teammate's SuggestionCard]** Judge clicks "Suniye 🔊" on the red card (Failure Guard)
6. **[Teammate's voice_node + Sarvam API]** VoicePlayer plays Hindi audio: *"Namaste Raju bhai. Pichhli baar aapne 20% discount diya tha — us hafte kamai 35% kum ho gayi thi. Is baar discount mat dijiye."*
7. **[Demo narration]** "The agent doesn't just warn — it also knows what worked."
8. **[Teammate's SuggestionCard]** Click "Suniye 🔊" on green card (Personal Best Replay)
9. **[Voice plays]** *"Namaste Raju bhai. Chhe hafte pehle jab aapne subah 7 baje dukaan kholi thi, us hafte kamai 25% badh gayi thi. Agli hafte phir se jaldi kholne ki koshish karein."*
10. **[Demo narration]** "And it learns from the network — 1,800 similar Paytm merchants."
11. **[Click blue card]** Network Wisdom voice plays
12. **[n8n demo — optional]** Show n8n dashboard with "Weekly Check" workflow — "This runs every Monday morning, automatically."

---

## Known Integration Risks

| Risk | Mitigation |
|---|---|
| Sarvam TTS rate limit during demo | Cache audio_url responses — don't regenerate live during presentation |
| Cognee graph query returns empty | Ensure ingest runs once at startup via lifespan event |
| Gemini Hindi output quality | Test voice_scripts in advance; have fallback hardcoded Hindi strings ready |
| n8n cloud vs local | Use n8n cloud for reliability; test webhook URL before demo day |
| Frontend fetch fails during demo | Hardcode fallback mock suggestions in page.tsx behind `DEMO_FALLBACK=true` env flag |

---

## Reset Instructions (before each demo run)

1. `curl -X POST localhost:8000/api/merchant/ingest` — reload fresh merchant data
2. Hard-refresh frontend (Ctrl+Shift+R)
3. Confirm 3 cards appear within 5 seconds
4. Test audio on red card — confirm Hindi plays through speakers
5. You're ready
