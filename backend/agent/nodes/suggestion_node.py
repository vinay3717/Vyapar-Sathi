import json
import re
import uuid
from typing import Dict, Any, List
from google import genai
from backend.agent.state import AgentState
from backend.config import settings
from backend.models import Suggestion


def clean_json_string(text: str) -> str:
    """Strips markdown code fences and whitespace from LLM output."""
    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def get_fallback_suggestions(merchant_id: str) -> List[Suggestion]:
    """Reliable fallback suggestions matching demo specifications."""
    return [
        Suggestion(
            suggestion_id=f"sug_{merchant_id}_fg_{uuid.uuid4().hex[:6]}",
            merchant_id=merchant_id,
            type="failure_guard",
            title="⚠️ डिस्काउंट देने से बचें",
            body="पिछली बार 20% डिस्काउंट देने पर आपकी साप्ताहिक कमाई 30% घट गई थी। इससे आपके मुनाफे पर बुरा असर पड़ा था।",
            confidence=0.96,
            action="इस हफ्ते किसी भी सामान पर फ्लैट डिस्काउंट न दें।",
            voice_script="नमस्ते राजू भाई। पिछली बार आपने 20% डिस्काउंट दिया था — उस हफ्ते कमाई 30% कम हो गई थी। इस बार डिस्काउंट मत दीजिए।",
            audio_url=None,
        ),
        Suggestion(
            suggestion_id=f"sug_{merchant_id}_pb_{uuid.uuid4().hex[:6]}",
            merchant_id=merchant_id,
            type="personal_best",
            title="✅ सुबह जल्दी दुकान खोलें",
            body="छह हफ्ते पहले सुबह 7 बजे दुकान खोलने पर नाश्ते के ग्राहकों से कमाई 25% बढ़ी थी। यह आपका सबसे सफल फैसला रहा है।",
            confidence=0.94,
            action="दुकान को सुबह ठीक 7:00 बजे खोलें और ताज़ा सामान रखें।",
            voice_script="नमस्ते राजू भाई। छह हफ्ते पहले जब आपने सुबह 7 बजे दुकान खोली थी, उस हफ्ते कमाई 25% बढ़ गई थी। अगले हफ्ते फिर से जल्दी खोलने की कोशिश करें।",
            audio_url=None,
        ),
        Suggestion(
            suggestion_id=f"sug_{merchant_id}_nw_{uuid.uuid4().hex[:6]}",
            merchant_id=merchant_id,
            type="network_wisdom",
            title="🌐 आसपास के व्यापारियों की सीख",
            body="मुंबई के 1,800 किराना व्यापारी सुबह 7 बजे ताज़ा दूध और ब्रेड रखकर 25% अधिक कमाई कर रहे हैं।",
            confidence=0.91,
            action="सुबह के समय दूध, ब्रेड और नाश्ते का स्टॉक काउंटर पर सजाएं।",
            voice_script="नमस्ते राजू भाई। मुंबई के 1,800 किराना व्यापारी सुबह 7 बजे ताज़ा दूध और नाश्ते का सामान रखकर 25% ज़्यादा कमाई कर रहे हैं। आप भी इसे आज़माएं।",
            audio_url=None,
        ),
    ]


async def suggestion_node(state: AgentState) -> Dict[str, Any]:
    """
    LangGraph node: calls Gemini to generate 3 structured Suggestion objects
    (failure_guard, personal_best, network_wisdom) with natural Hindi voice scripts.
    """
    merchant_id = state.get("merchant_id", "merchant_001")
    failure_patterns = state.get("failure_patterns", [])
    personal_bests = state.get("personal_bests", [])
    network_wisdom = state.get("network_wisdom", [])

    # Format patterns for Gemini prompt
    patterns_summary = {
        "merchant_id": merchant_id,
        "failure_patterns": [
            {
                "decision": p.decision_type if hasattr(p, "decision_type") else p.get("decision_type"),
                "description": p.description if hasattr(p, "description") else p.get("description"),
                "revenue_delta": f"{p.revenue_delta}%" if hasattr(p, "revenue_delta") else f"{p.get('revenue_delta')}%",
                "outcome": "negative",
            }
            for p in failure_patterns
        ],
        "personal_bests": [
            {
                "decision": p.decision_type if hasattr(p, "decision_type") else p.get("decision_type"),
                "description": p.description if hasattr(p, "description") else p.get("description"),
                "revenue_delta": f"+{p.revenue_delta}%" if hasattr(p, "revenue_delta") else f"+{p.get('revenue_delta')}%",
                "outcome": "positive",
            }
            for p in personal_bests
        ],
        "network_wisdom": network_wisdom,
    }

    prompt = f"""You are an AI business advisor for Indian kirana merchants.
Given these patterns, generate exactly 3 suggestions in JSON.
One suggestion for type "failure_guard", one for type "personal_best", and one for type "network_wisdom".

Each must have:
- type: exactly one of "failure_guard", "personal_best", "network_wisdom"
- title: Hindi label in Devanagari script (5 words max, e.g. "सावधान: डिस्काउंट न दें")
- body: Hindi explanation in Devanagari script (exactly 2 sentences)
- confidence: number between 0.0 and 1.0
- action: Hindi imperative sentence in Devanagari script telling what to do
- voice_script: Hindi speech text in Devanagari script (2-3 sentences, addressed respectfully to merchant as 'Aap', and must start with 'Namaste Raju bhai' or 'Namaste').

Return ONLY a valid JSON array of 3 objects. No markdown formatting.
Patterns:
{json.dumps(patterns_summary, indent=2, ensure_ascii=False)}
"""

    suggestions: List[Suggestion] = []

    if settings.GEMINI_API_KEY:
        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            # Try gemini-flash-latest first as confirmed by model list
            response_text = ""
            for model_name in ["gemini-flash-latest", "models/gemini-flash-latest", "gemini-2.5-flash"]:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )
                    if response and response.text:
                        response_text = response.text
                        break
                except Exception as ex:
                    print(f"Model {model_name} attempt: {ex}")
                    continue

            if response_text:
                cleaned = clean_json_string(response_text)
                raw_suggestions = json.loads(cleaned)

                if isinstance(raw_suggestions, list) and len(raw_suggestions) >= 3:
                    for item in raw_suggestions[:3]:
                        s_type = item.get("type", "failure_guard")
                        if s_type not in ["failure_guard", "personal_best", "network_wisdom"]:
                            s_type = "failure_guard"
                        
                        sug = Suggestion(
                            suggestion_id=f"sug_{merchant_id}_{s_type}_{uuid.uuid4().hex[:6]}",
                            merchant_id=merchant_id,
                            type=s_type,
                            title=item.get("title", "व्यापार सुझाव"),
                            body=item.get("body", "आपके व्यापार के विश्लेषण के आधार पर सुझाव।"),
                            confidence=float(item.get("confidence", 0.9)),
                            action=item.get("action", "सुझाव का पालन करें।"),
                            voice_script=item.get("voice_script", "नमस्ते राजू भाई। व्यापार में प्रगति के लिए यह कदम उठाएं।"),
                            audio_url=None,
                        )
                        suggestions.append(sug)
        except Exception as e:
            print(f"Gemini suggestion generation notice: {e}, using demo fallback")

    # Fallback if Gemini did not produce 3 valid objects
    if len(suggestions) < 3:
        suggestions = get_fallback_suggestions(merchant_id)

    return {"suggestions": suggestions}
