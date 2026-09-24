import { NextRequest, NextResponse } from "next/server";
import { Suggestion } from "@/app/types";

const FALLBACK_SUGGESTIONS: Suggestion[] = [
  {
    suggestion_id: "sugg_001",
    merchant_id: "merchant_001",
    type: "failure_guard",
    title: "⚠️ सावधान: 20% छूट न दें",
    body: "तीन हफ्ते पहले 20% छूट देने पर आपकी कमाई 35% घट गई थी। इस हफ्ते भी छूट देने से बचें।",
    confidence: 0.91,
    action: "इस हफ्ते सामान सामान्य दर पर ही बेचें।",
    voice_script:
      "नमस्ते राजू भाई। पिछली बार आपने 20% डिस्काउंट दिया था — उस हफ्ते कमाई 35% कम हो गई थी। इस बार डिस्काउंट मत दीजिए।",
    audio_url: "data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAAAP8A/w==",
  },
  {
    suggestion_id: "sugg_002",
    merchant_id: "merchant_001",
    type: "personal_best",
    title: "✅ आपकी सफलता: सुबह 7 बजे खोलें",
    body: "छह हफ्ते पहले सुबह 7 बजे दुकान खोलने पर आपकी कमाई 25% बढ़ गई थी। इसे फिर दोहराएं।",
    confidence: 0.88,
    action: "दुकान सुबह 7:00 बजे खोलें।",
    voice_script:
      "नमस्ते राजू भाई। छह हफ्ते पहले जब आपने सुबह 7 बजे दुकान खोली थी, उस हफ्ते कमाई 25% बढ़ गई थी। अगले हफ्ते फिर से जल्दी खोलने की कोशिश करें।",
    audio_url: "data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAAAP8A/w==",
  },
  {
    suggestion_id: "sugg_003",
    merchant_id: "merchant_001",
    type: "network_wisdom",
    title: "🌐 आसपास के व्यापारी: दूध व नाश्ता कॉम्बो",
    body: "मुंबई के 1,800 किराना व्यापारियों ने सुबह के समय ब्रेड-दूध कॉम्बो से 18% ज्यादा बिक्री की है।",
    confidence: 0.85,
    action: "सुबह के समय ब्रेड और दूध का कॉम्बो पैक काउंटर पर रखें।",
    voice_script:
      "नमस्ते राजू भाई। मुंबई के आसपास के किराना व्यापारियों ने सुबह दूध और ब्रेड का कॉम्बो रखकर बिक्री 18% बढ़ाई है। आप भी इसे आज़माएं।",
    audio_url: "data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAAAP8A/w==",
  },
];

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const merchantId = searchParams.get("merchant_id") || "merchant_001";
  const fastApiUrl = process.env.FASTAPI_BACKEND_URL || "http://localhost:8000";

  try {
    const res = await fetch(`${fastApiUrl}/api/merchant/${merchantId}/suggestions`, {
      headers: { "Content-Type": "application/json" },
      cache: "no-store",
    });

    if (res.ok) {
      const data = await res.json();
      return NextResponse.json(data);
    }

    console.warn(`FastAPI returned status ${res.status}. Using fallback suggestions.`);
  } catch (error) {
    console.warn("Could not reach FastAPI backend. Serving resilient fallback suggestions:", error);
  }

  return NextResponse.json({
    suggestions: FALLBACK_SUGGESTIONS,
    generated_at: new Date().toISOString(),
    is_fallback: true,
  });
}
