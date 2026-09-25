# PPT_CONTENT.md — Vyapar Sarthi
## Paytm Build for India AI Hackathon — Mumbai Edition
### Team: Kairos | Track 3: Autonomous AI Teammates

> 9 slides. All required sections covered. Paste into Canva. Export as PDF (max 10MB).

---

## SLIDE 1 — Title Slide

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

## SLIDE 2 — Problem Statement

**Headline:**
Raju has run the same failed discount 3 times.
Nobody told him.

**Body:**
India has 13 million Paytm merchants collecting payments digitally.
But they make decisions the same way their fathers did —
on instinct, with zero memory of what worked or failed before.

**Three pain points:**

📉 **No decision memory**
Merchants repeat failed strategies because nothing records outcomes.
70% of small merchants retry a promotion even after it failed.

🔇 **No proactive advisor**
Current tools only respond when asked. Nobody watches out for the merchant.

🌐 **Language barrier**
Analytics dashboards are English, data-heavy, and require literacy to read.

**The gap:**
> They have transaction data. They have zero decision intelligence.

---

## SLIDE 3 — Proposed Solution

**Headline:**
Meet Vyapar Sarthi —
the AI teammate that remembers, learns, and speaks up.

**Three capabilities:**

🛑 **Failure Guard**
Detects when a merchant is about to repeat a past mistake.
Warns them in Hindi before they act — automatically, every week.

✅ **Personal Best Replay**
Finds the merchant's own high-performing decisions.
Suggests recreating what actually worked for them specifically.

🌐 **Network Wisdom**
Surfaces what similar Paytm merchants did in the same season — and what paid off.

**How it's delivered:**
No dashboard. No typing. A proactive voice note in Hindi/Marathi —
triggered every Monday morning before the merchant's week begins.

**One line:**
> Vyapar Sarthi nahin kehta "kya hua" — kehta hai "ab kya karo."
> *(It doesn't say what happened — it says what to do now.)*

---

## SLIDE 4 — How It Works

**Headline:**
Built for real. Demo-ready on Day 1.

**Demo scenario (left panel):**

Raju. Kirana store. Dharavi, Mumbai.

📉 3 weeks ago: ran 20% discount → revenue dropped 35%
Cognee logs: `discount_20pct → negative → -35%`

📈 6 weeks ago: opened at 7am instead of 9am → revenue up 25%
Cognee logs: `early_open → positive → +25%`

🔔 This Monday: n8n triggers agent automatically.
Raju hears in Hindi — before his week starts:
*"Namaste Raju bhai. Pichhli baar 20% discount se kamai 35% kum hui.
Is baar subah 7 baje kholne ki koshish karein — chhe hafte pehle
isse 25% zyada kamai hui thi."*

**Architecture flow (right panel):**

```
Paytm Transaction Data
        ↓
Cognee Knowledge Graph
(causal memory: decision → outcome)
        ↓
LangGraph Agent
(pattern_node → suggestion_node)
        ↓
Gemini 3.5 Flash
(generates Hindi voice_script)
        ↓
Sarvam Bulbul v3
(natural Hindi/Marathi audio)
        ↓
n8n Scheduler
(triggers every Monday — no prompt needed)
```

---

## SLIDE 5 — Technology / Tech Stack Used

**Headline:**
Every tool chosen for India. Every version production-ready.

**Table:**

| Layer | Tool | Purpose |
|---|---|---|
| Agent Orchestration | LangGraph 1.2.1 | 3-node StateGraph: ingest → pattern → suggest |
| LLM | Gemini 3.5 Flash | Hindi suggestion + voice script generation |
| Merchant Memory | Cognee (latest) | Graph-native causal memory: decision → outcome |
| Voice Output | Sarvam Bulbul v3 | Natural TTS in 11 Indian languages |
| Workflow Trigger | n8n (cloud) | Autonomous weekly proactive trigger |
| Backend | FastAPI 0.115 | REST API + LangGraph runtime |
| Frontend | Next.js 14 | Merchant dashboard (secondary to voice) |

**Sponsor callout:**
Built with — Cognee · Sarvam · n8n

**Why this stack:**
- Sarvam is the only voice AI trained natively on 22 Indian languages
- Cognee's knowledge graph stores causal relationships — not just chat history
- LangGraph enables stateful, multi-step agent reasoning — not a single prompt

---

## SLIDE 6 — USP (Unique Selling Proposition)

**Headline:**
Every other agent responds.
Vyapar Sarthi remembers.

**Comparison table:**

| Feature | Generic Merchant AI | Vyapar Sarthi |
|---|---|---|
| Memory of past decisions | ❌ | ✅ Cognee causal graph |
| Learns from merchant's failures | ❌ | ✅ Failure Guard node |
| Proactive — no prompt needed | ❌ | ✅ n8n weekly trigger |
| Personalised to this merchant | ❌ | ✅ Per-merchant memory |
| Indian language voice delivery | ❌ | ✅ Sarvam, 11 languages |
| Network intelligence | ❌ | ✅ Similar merchant patterns |

**The compounding moat:**
> The longer a merchant uses Vyapar Sarthi,
> the smarter it gets about them specifically.
> It doesn't stay a product — it becomes a business partner.

---

## SLIDE 7 — Impact & Benefits

**Headline:**
13 million merchants. Zero business advisors.
Until now.

**Merchant impact (3 points):**

📉 **Break the failure loop**
Average small merchant repeats a failed strategy 2.3x before stopping.
Failure Guard breaks this after the first time — saving weeks of lost revenue.

🗣️ **Zero literacy barrier**
No reading. No dashboard. No English.
A voice note in their language — the way business advice has always worked in India.

📈 **Compounding personalisation**
Every decision logged. Every outcome recorded.
Month 3 advice is smarter than Month 1. The merchant grows with the agent.

**Paytm platform impact:**

🔒 **Merchant retention**
An agent that gets smarter over time creates switching cost. Merchants stay on Paytm.

💳 **Loan & insurance upsell signal**
When Vyapar Sarthi detects consistent positive patterns, it surfaces relevant Paytm financial products at the right moment — not cold.

📊 **Aggregate merchant intelligence**
Network Wisdom turns Paytm's 13M merchant dataset into a collective intelligence layer — a moat no competitor can replicate.

---

## SLIDE 8 — Business Model

**Headline:**
Three revenue levers. All native to Paytm's existing ecosystem.

**Model 1 — Freemium SaaS**
Free tier: weekly voice summary (1 suggestion/week)
Paid tier (₹99/month): all 3 capabilities + daily check-ins + WhatsApp delivery
Target: top 10% of Paytm merchants = ~1.3M potential subscribers

**Model 2 — Financial Product Trigger**
Vyapar Sarthi detects a merchant is consistently growing.
It surfaces a Paytm Business Loan or Insurance product at peak trust moment.
Revenue: referral fee / conversion commission to Paytm's lending arm.
This is Track 2 (Financial Journeys) embedded inside Track 3.

**Model 3 — Paytm Platform Intelligence**
Aggregate anonymised decision-outcome data across all merchants.
Sell as a B2B intelligence API to FMCG brands, distributors, and lenders
("What are kirana stores in Pune buying more of this week?")
Revenue: enterprise API licensing.

**Unit economics (rough):**
- Cost per merchant/month: ~₹8 (Gemini + Sarvam + Cognee API calls, weekly cadence)
- Revenue at ₹99/month paid tier: ~₹91 gross margin per merchant
- Break-even: 100K paid merchants

---

## SLIDE 9 — Team Kairos

**Headline:**
We've built agents. We've shipped them.

**Devesh Dolas**
3rd Year B.Tech Computer Engineering, AISSMS IOIT Pune
- Built **Nexus** — LangGraph 9-node adaptive learning platform with multi-model routing and personalization-correction feedback loop
- Built **CrossCheck** — AI agent verification tool with Docker sandboxing and on-chain reputation (ERC-8004)
- Focus: Agent orchestration, LangGraph, RAG, Cognee, FastAPI

**[Teammate Name] — [Institution]**
[Their strongest shipped project — one line]
Focus: [Their skills]

**Why Kairos:**
We're not designing an agent architecture for the first time.
We're applying a battle-tested system to a problem that affects 13 million Indians —
and we can build it in 8 hours because we've built the harder version already.

**The ask:**
Select us to build on Oct 3.
Architecture locked. Split ready. We ship.

---

## CANVA INSTRUCTIONS
- Template: Dark startup pitch (search "pitch deck dark" in Canva)
- Font: Poppins or Inter throughout
- Hindi text: copy-paste directly — Devanagari renders correctly in Canva
- Slide 4: Use a two-column layout — demo story left, architecture flow right
- Slide 6: Use Canva's table element for the comparison table
- Color code: red accent for Failure Guard, green for Personal Best, blue for Network Wisdom
- Export: File → Download → PDF Standard → confirm under 10MB before submitting
