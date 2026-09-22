# BUILD_teammate.md — Teammate (Frontend + Infra)
> ⚠️ AGENT INSTRUCTIONS: You are building ONLY the items in this file. Nothing else. Build exactly as specified.

---

## Your Scope

- Next.js 14 merchant dashboard (page.tsx + 3 components)
- voice_node.py — calls Sarvam Bulbul v3 TTS API
- POST /api/merchant/{merchant_id}/voice FastAPI route
- n8n webhook workflow (workflow.json)
- SARVAM_API_KEY and N8N_WEBHOOK_URL env vars

---

## Your Files

| File | Purpose |
|---|---|
| `backend/agent/nodes/voice_node.py` | Calls Sarvam TTS with voice_script, returns audio_url |
| `frontend/app/page.tsx` | Main merchant dashboard — fetches and displays suggestions |
| `frontend/app/components/SuggestionCard.tsx` | Renders one Suggestion with type badge, title, body, action, Play Voice button |
| `frontend/app/components/VoicePlayer.tsx` | Plays audio_url from Sarvam; shows waveform or simple play/pause |
| `frontend/app/components/MerchantHeader.tsx` | Shows merchant name, category, language badge |
| `frontend/app/api/suggestions/route.ts` | Next.js route that proxies GET to FastAPI /api/merchant/{id}/suggestions |
| `n8n/workflow.json` | n8n workflow: manual trigger → HTTP request to POST /api/webhook/n8n/trigger |

---

## Your Tasks (ordered by priority)

### Task 1: voice_node.py
- What to build: A LangGraph node that receives `state["suggestions"]` (list of Suggestion objects from Devesh's suggestion_node). For EACH suggestion, calls Sarvam Bulbul v3 TTS API with the `voice_script` field. Stores the returned audio URL back into the suggestion object as `audio_url`. Updates `state["suggestions"]` with audio_url populated.
- File: `backend/agent/nodes/voice_node.py`
- Inputs: `state["suggestions"]` — list of Suggestion objects; each has `voice_script` in Hindi
- Sarvam TTS API call:
  ```python
  import httpx
  response = httpx.post(
      "https://api.sarvam.ai/text-to-speech",
      headers={"API-Subscription-Key": settings.SARVAM_API_KEY},
      json={
          "inputs": [suggestion.voice_script],
          "target_language_code": "hi-IN",  # or "mr-IN" for Marathi
          "speaker": "meera",
          "model": "bulbul:v3",
          "enable_preprocessing": True
      }
  )
  # response.json()["audios"][0] is base64 encoded WAV
  # Save to /tmp/{suggestion_id}.wav and return local path or base64 string
  ```
- Outputs: `state["suggestions"]` with `audio_url` field populated on each suggestion (base64 data URI or file path)
- Acceptance criteria: Calling voice_node with a suggestion containing a Hindi voice_script returns an audio file that plays in browser

### Task 2: /api/merchant/{merchant_id}/voice route
- What to build: Add to `backend/main.py` (coordinate with Devesh — he owns main.py, you give him the route to paste in):
  ```
  POST /api/merchant/{merchant_id}/voice
  Body: { suggestion_id: str }
  Response: { audio_url: str, duration_seconds: float }
  ```
  This route finds the suggestion by ID in the last graph run result and returns its audio_url.
- Acceptance criteria: POST with valid suggestion_id returns 200 with audio_url

### Task 3: Next.js dashboard
- What to build: Single-page merchant dashboard. On load, fetches `/api/suggestions?merchant_id=merchant_001` (proxied to FastAPI). Shows MerchantHeader at top. Below: three SuggestionCards (one per suggestion type). Each card has a "Suniye 🔊" (Listen) button that calls /api/merchant/{id}/voice and plays the audio.
- Files: `frontend/app/page.tsx`, `frontend/app/api/suggestions/route.ts`
- Design: Clean, mobile-friendly. Use Tailwind. Color code cards by type: failure_guard = red-50 border, personal_best = green-50 border, network_wisdom = blue-50 border.
- Language: All UI labels in Hindi. "नमस्ते, [Merchant Name]" as header. Card type labels: "⚠️ सावधान", "✅ आपकी सफलता", "🌐 आसपास के व्यापारी"
- Acceptance criteria: Page loads, shows 3 suggestion cards, Play button triggers audio

### Task 4: SuggestionCard component
- What to build: Card component that receives a Suggestion prop. Displays: type badge (color-coded), title (bold, Hindi), body (Hindi, 2 sentences), action (highlighted box, Hindi imperative), confidence as a simple % bar, "Suniye 🔊" button.
- File: `frontend/app/components/SuggestionCard.tsx`
- Props: `suggestion: Suggestion, onPlay: (suggestionId: string) => void`
- Acceptance criteria: Renders correctly for all 3 suggestion types

### Task 5: VoicePlayer component
- What to build: Receives `audioUrl: string` (base64 data URI). Creates an HTML Audio element, plays on mount or on button press. Shows "▶ बज रहा है..." while playing, "✓ सुना" when done.
- File: `frontend/app/components/VoicePlayer.tsx`
- Acceptance criteria: Audio plays without user needing to interact with browser audio settings

### Task 6: n8n workflow
- What to build: Simple n8n workflow JSON. Trigger: Manual trigger (for demo) OR schedule trigger (every Monday 9am IST). Action: HTTP Request node → POST to `${N8N_WEBHOOK_URL}/api/webhook/n8n/trigger` with body `{"merchant_id": "merchant_001", "trigger": "weekly_check"}`. Export as `n8n/workflow.json`.
- Acceptance criteria: Importing workflow.json into n8n and clicking Execute triggers the backend

---

## Contracts You Must Honor

- `voice_node.py` must be added to LangGraph graph by Devesh after you hand it off — coordinate with him on timing
- The Suggestion type shape from `models.py` is frozen — read it, do not change it
- `/api/suggestions/route.ts` must proxy to exactly `GET /api/merchant/{merchant_id}/suggestions` — do not change the FastAPI route path
- `audio_url` on Suggestion is added by your voice_node — Devesh's suggestion_node leaves it empty, you fill it

---

## DO NOT
- Do not modify `models.py`, `graph.py`, `state.py`, or any node files except `voice_node.py`
- Do not change `/api/merchant/ingest` or `/api/merchant/{id}/suggestions` route behavior
- Do not add a database
- Do not add authentication
- Do not install packages not listed in BUILD.md without updating it first
- Do not build the Cognee client — that is Devesh's file
