# PPT_CONTENT.md — Vyapar Sarthi
## Paytm Build for India AI Hackathon — Mumbai Edition
### Team: Kairos | Track 3: Autonomous AI Teammates

> 8 slides. Paste each into Canva. Export as PDF (max 10MB).

---

## SLIDE 1 — Cover

**Headline (large):**
व्यापार सारथी
Vyapar Sarthi

**Subheadline:**
The AI teammate that learns from your mistakes — so you don't repeat them.

**Bottom tag:**
Track 3: Autonomous AI Teammates | Team Kairos | Paytm Build for India

**Visual direction:**
Dark background. Kirana store at night, warm glow, subtle AI interface overlay.

---

## SLIDE 2 — The Problem

**Headline:**
Raju has run the same failed discount 3 times.
Nobody told him.

**Body:**
India's 13 million Paytm merchants collect payments digitally.
But they make decisions the same way their fathers did —
on instinct, with no memory of what worked or failed before.

**The gap in one line:**
> They have transaction data. They have zero decision memory.

**Visual direction:**
Left: merchant staring at paper ledger. Right: Paytm QR code. Gap between = the problem.

---

## SLIDE 3 — Our Solution

**Headline:**
Meet Vyapar Sarthi —
the AI teammate that remembers, learns, and speaks up.

**Three capabilities:**

🛑 **Failure Guard**
Detects when a merchant is about to repeat a past mistake.
Warns them — in Hindi — before they act.

✅ **Personal Best Replay**
Finds the merchant's own high-performing patterns.
Suggests recreating what actually worked for them specifically.

🌐 **Network Wisdom**
Surfaces what similar Paytm merchants did in the same situation — and what paid off.

**Key line:**
No dashboard. No typing. A proactive voice note — in their language, before they ask.

---

## SLIDE 4 — Demo Scenario

**Headline:**
Raju. Kirana store. Dharavi, Mumbai.

**Three panels:**

📉 **3 weeks ago**
Raju ran a 20% discount.
Revenue dropped 35%.
Cognee logs it: `discount_20pct → negative → -35%`

📈 **6 weeks ago**
Raju opened at 7am instead of 9am.
Revenue rose 25%.
Cognee logs it: `early_open → positive → +25%`

🔔 **This Monday morning**
n8n triggers the agent automatically.
LangGraph runs. Sarvam speaks.
Raju hears — in Hindi — what to do differently this week.
He didn't open an app. He didn't type a question.

---

## SLIDE 5 — How It Works

**Headline:**
Built on real infrastructure. Not a prototype.

**Flow (left to right, 5 steps):**

```
Paytm Transaction Data
        ↓
Cognee Knowledge Graph
(causal memory: decision → outcome)
        ↓
LangGraph Agent
pattern_node → suggestion_node
        ↓
Gemini 3.5 Flash
generates Hindi voice_script
        ↓
Sarvam Bulbul v3
delivers natural Hindi/Marathi audio
        ↓
n8n Scheduler
triggers every Monday — no prompt needed
```

**Sponsor row (logos or text):**
Cognee · Sarvam · n8n

---

## SLIDE 6 — Why This Wins

**Headline:**
Every other agent responds.
Vyapar Sarthi remembers.

**Table:**

| | Generic Merchant AI | Vyapar Sarthi |
|---|---|---|
| Memory of past decisions | ❌ | ✅ Cognee causal graph |
| Learns from failures | ❌ | ✅ Failure Guard |
| Proactive — no prompt needed | ❌ | ✅ n8n weekly trigger |
| Personalised to this merchant | ❌ | ✅ Per-merchant graph |
| Indian language voice | ❌ | ✅ Sarvam, 11 languages |

**The moat:**
The longer a merchant uses it, the smarter it gets about them specifically.
It becomes a business partner — not a product.

---

## SLIDE 7 — Tech Stack & Feasibility

**Headline:**
8 hours. Two people. One locked architecture.

**Stack:**

| Layer | Tool | Version |
|---|---|---|
| Agent orchestration | LangGraph | 1.2.1 |
| LLM | Gemini 3.5 Flash | gemini-3.5-flash |
| Merchant memory | Cognee | latest |
| Voice output | Sarvam Bulbul v3 | bulbul:v3 |
| Workflow trigger | n8n | cloud |
| Backend | FastAPI | 0.115.x |
| Frontend | Next.js | 14 |

**Why it's buildable:**
- No real Paytm API needed — mock CSV for demo; Paytm already has this data
- Cognee handles graph complexity — we write queries, not the engine
- LangGraph is our home ground — we've shipped 9-node production graphs (Nexus)
- Sarvam TTS = one HTTP call

---

## SLIDE 8 — Team & Ask

**Headline:**
We've built agents. We've shipped them.

**Devesh Dolas**
3rd year B.Tech, AISSMS IOIT Pune
Built Nexus (LangGraph 9-node adaptive platform) + CrossCheck (AI agent verification, Docker + on-chain reputation)
Owns: Agent architecture, Cognee, LangGraph, FastAPI

**[Teammate Name] — [Institution]**
[Their strongest project in one line]
Owns: Sarvam voice layer, n8n, Next.js dashboard

---

**The ask:**
Select us to build this on Oct 3.
The architecture is locked. The split is ready. We ship.

---

*Vyapar Sarthi nahin kehta "kya hua" — kehta hai "ab kya karo."*
*(It doesn't say what happened — it says what to do now.)*

---

## CANVA INSTRUCTIONS
- Template: Dark startup pitch (search "pitch deck dark" in Canva)
- Font: Poppins or Inter
- Hindi text: copy-paste from above — renders correctly in Canva
- Slide 5 flow: use Canva's arrow/connector shapes
- Slide 6 table: use Canva's table element
- Export: File → Download → PDF Standard → check under 10MB
