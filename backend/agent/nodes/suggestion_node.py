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


def get_fallback_suggestions(merchant_id: str, language: str = "hi") -> List[Suggestion]:
    """Reliable fallback suggestions matching demo specifications across Hindi, Marathi, and English."""
    if language == "mr":
        return [
            Suggestion(
                suggestion_id=f"sug_{merchant_id}_fg_{uuid.uuid4().hex[:6]}",
                merchant_id=merchant_id,
                type="failure_guard",
                title="⚠️ २०% सवलत देणे टाळा",
                body="तीन आठवड्यांपूर्वी २०% डिस्काउंट दिल्याने तुमची साप्ताहिक कमाई ३०% कमी झाली होती. या आठवड्यात सवलत देणे टाळा.",
                confidence=0.96,
                action="या आठवड्यात वस्तू नेहमीच्या दरानेच विका.",
                voice_script="नमस्कार राजू भाऊ. मागच्या वेळी आपण २०% डिस्काउंट दिला होता — त्या आठवड्यात कमाई ३०% कमी झाली होती. या वेळी डिस्काउंट देऊ नका.",
                audio_url=None,
            ),
            Suggestion(
                suggestion_id=f"sug_{merchant_id}_pb_{uuid.uuid4().hex[:6]}",
                merchant_id=merchant_id,
                type="personal_best",
                title="✅ सकाळी लवकर दुकान उघडा",
                body="सहा आठवड्यांपूर्वी सकाळी ७ वाजता दुकान उघडल्यामुळे सकाळच्या ग्राहकांमुळे कमाई २५% वाढली होती. हा तुमचा सर्वोत्तम निर्णय ठरला.",
                confidence=0.94,
                action="दुकान सकाळी ठीक ७:०० वाजता उघडा आणि ताजे सामान ठेवा.",
                voice_script="नमस्कार राजू भाऊ. सहा आठवड्यांपूर्वी जेव्हा आपण सकाळी ७ वाजता दुकान उघडले होते, त्या आठवड्यात कमाई २५% वाढली होती. पुढील आठवड्यात पुन्हा लवकर उघडण्याचा प्रयत्न करा.",
                audio_url=None,
            ),
            Suggestion(
                suggestion_id=f"sug_{merchant_id}_nw_{uuid.uuid4().hex[:6]}",
                merchant_id=merchant_id,
                type="network_wisdom",
                title="🌐 परिसरातील व्यापाऱ्यांची युक्ती",
                body="मुंबईतील १,८०० किराणा व्यापारी सकाळी ७ वाजता ताजे दूध आणि ब्रेड ठेवून २५% अधिक कमाई करत आहेत.",
                confidence=0.91,
                action="सकाळी दूध, ब्रेड आणि नाश्त्याचा साठा काउंटरवर ठेवा.",
                voice_script="नमस्कार राजू भाऊ. मुंबईतील १,८०० किराणा व्यापारी सकाळी ७ वाजता ताजे दूध आणि नाश्त्याचे सामान ठेवून २५% जास्त कमाई करत आहेत. आपणही हे करून पहा.",
                audio_url=None,
            ),
        ]
    elif language == "en":
        return [
            Suggestion(
                suggestion_id=f"sug_{merchant_id}_fg_{uuid.uuid4().hex[:6]}",
                merchant_id=merchant_id,
                type="failure_guard",
                title="⚠️ Avoid 20% Discount",
                body="Three weeks ago, running a 20% discount dropped your weekly revenue by 30%. Avoid giving discounts this week.",
                confidence=0.96,
                action="Keep standard pricing across all inventory this week.",
                voice_script="Hello Raju bhai. Last time you offered a 20% discount, revenue dropped by 30%. Please avoid giving flat discounts this week.",
                audio_url=None,
            ),
            Suggestion(
                suggestion_id=f"sug_{merchant_id}_pb_{uuid.uuid4().hex[:6]}",
                merchant_id=merchant_id,
                type="personal_best",
                title="✅ Open Shop Early at 7 AM",
                body="Six weeks ago, opening at 7 AM boosted your revenue by 25% from morning breakfast shoppers. Repeat this winning habit.",
                confidence=0.94,
                action="Open your store at 7:00 AM sharp with fresh stock ready.",
                voice_script="Hello Raju bhai. Six weeks ago when you opened shop at 7 AM, your weekly revenue rose by 25%. Try opening early again next week.",
                audio_url=None,
            ),
            Suggestion(
                suggestion_id=f"sug_{merchant_id}_nw_{uuid.uuid4().hex[:6]}",
                merchant_id=merchant_id,
                type="network_wisdom",
                title="🌐 Network Wisdom: Morning Combos",
                body="Over 1,800 kirana stores across Mumbai made 25% higher profit by pairing fresh bread and milk at 7 AM.",
                confidence=0.91,
                action="Place bread and fresh milk combo packs front and center on your counter.",
                voice_script="Hello Raju bhai. 1,800 Mumbai kirana merchants earned 25% more by stocking fresh milk and breakfast combos by 7 AM. You should try this too.",
                audio_url=None,
            ),
        ]
    else:  # Hindi default
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
    (failure_guard, personal_best, network_wisdom) with natural voice scripts in target language.
    """
    merchant_id = state.get("merchant_id", "merchant_001")
    language = state.get("language", "hi")
    failure_patterns = state.get("failure_patterns", [])
    personal_bests = state.get("personal_bests", [])
    network_wisdom = state.get("network_wisdom", [])

    # Format patterns for Gemini prompt
    patterns_summary = {
        "merchant_id": merchant_id,
        "language": language,
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

    lang_instructions = {
        "mr": {
            "lang_name": "Marathi (मराठी in Devanagari script)",
            "salutation": "'Namaskar Raju bhau' or 'Namaskar'",
            "address": "respectfully as 'Aap' or 'Tumhi'",
        },
        "en": {
            "lang_name": "English",
            "salutation": "'Hello Raju bhai' or 'Hello'",
            "address": "respectfully as 'you'",
        },
        "hi": {
            "lang_name": "Hindi (हिन्दी in Devanagari script)",
            "salutation": "'Namaste Raju bhai' or 'Namaste'",
            "address": "respectfully as 'Aap'",
        },
    }.get(language, {
        "lang_name": "Hindi (हिन्दी in Devanagari script)",
        "salutation": "'Namaste Raju bhai' or 'Namaste'",
        "address": "respectfully as 'Aap'",
    })

    prompt = f"""You are an AI business advisor for Indian kirana merchants.
Target Language: {lang_instructions['lang_name']}.
Given these patterns, generate exactly 3 suggestions in JSON in {lang_instructions['lang_name']}.
One suggestion for type "failure_guard", one for type "personal_best", and one for type "network_wisdom".

Each must have:
- type: exactly one of "failure_guard", "personal_best", "network_wisdom"
- title: short label in {lang_instructions['lang_name']} (5 words max)
- body: clear explanation in {lang_instructions['lang_name']} (exactly 2 sentences)
- confidence: number between 0.0 and 1.0
- action: imperative sentence in {lang_instructions['lang_name']} telling what action to take
- voice_script: spoken text in {lang_instructions['lang_name']} (2-3 sentences, addressed {lang_instructions['address']}, and must start with {lang_instructions['salutation']}).

Return ONLY a valid JSON array of 3 objects. No markdown formatting.
Patterns:
{json.dumps(patterns_summary, indent=2, ensure_ascii=False)}
"""

    suggestions: List[Suggestion] = []

    if settings.GEMINI_API_KEY:
        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            response_text = ""
            for model_name in ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-flash-latest"]:
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
                            body=item.get("body", "व्यवसायाच्या विश्लेषणावर आधारित शिफारस."),
                            confidence=float(item.get("confidence", 0.9)),
                            action=item.get("action", "सुझाव का पालन करें."),
                            voice_script=item.get("voice_script", "नमस्ते राजू भाई. व्यापार में प्रगति के लिए यह कदम उठाएं."),
                            audio_url=None,
                        )
                        suggestions.append(sug)
        except Exception as e:
            print(f"Gemini suggestion generation notice: {e}, using fallback")

    # Fallback if Gemini did not produce 3 valid objects
    if len(suggestions) < 3:
        suggestions = get_fallback_suggestions(merchant_id, language)

    return {"suggestions": suggestions}
