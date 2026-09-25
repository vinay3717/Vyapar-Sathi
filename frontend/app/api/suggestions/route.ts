import { NextRequest, NextResponse } from "next/server";
import { Suggestion } from "@/app/types";

const FALLBACK_SUGGESTIONS_MAP: Record<string, Suggestion[]> = {
  hi: [
    {
      suggestion_id: "sugg_001_hi",
      merchant_id: "merchant_001",
      type: "failure_guard",
      title: "⚠️ 20% छूट न दें",
      body: "तीन हफ्ते पहले 20% छूट देने पर आपकी कमाई 35% घट गई थी। इस हफ्ते भी छूट देने से बचें।",
      confidence: 0.96,
      action: "इस हफ्ते सामान सामान्य दर पर ही बेचें।",
      voice_script:
        "नमस्ते राजू भाई। पिछली बार आपने 20% डिस्काउंट दिया था — उस हफ्ते कमाई 35% कम हो गई थी। इस बार डिस्काउंट मत दीजिए।",
      audio_url: "data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAAAP8A/w==",
    },
    {
      suggestion_id: "sugg_002_hi",
      merchant_id: "merchant_001",
      type: "personal_best",
      title: "✅ सुबह 7 बजे खोलें",
      body: "छह हफ्ते पहले सुबह 7 बजे दुकान खोलने पर आपकी कमाई 25% बढ़ गई थी। इसे फिर दोहराएं।",
      confidence: 0.94,
      action: "दुकान सुबह 7:00 बजे खोलें।",
      voice_script:
        "नमस्ते राजू भाई। छह हफ्ते पहले जब आपने सुबह 7 बजे दुकान खोली थी, उस हफ्ते कमाई 25% बढ़ गई थी। अगले हफ्ते फिर से जल्दी खोलने की कोशिश करें।",
      audio_url: "data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAAAP8A/w==",
    },
    {
      suggestion_id: "sugg_003_hi",
      merchant_id: "merchant_001",
      type: "network_wisdom",
      title: "🌐 दूध व नाश्ता कॉम्बो",
      body: "मुंबई के 1,800 किराना व्यापारियों ने सुबह के समय ब्रेड-दूध कॉम्बो से 18% ज्यादा बिक्री की है।",
      confidence: 0.91,
      action: "सुबह के समय ब्रेड और दूध का कॉम्बो पैक काउंटर पर रखें।",
      voice_script:
        "नमस्ते राजू भाई। मुंबई के आसपास के किराना व्यापारियों ने सुबह दूध और ब्रेड का कॉम्बो रखकर बिक्री 18% बढ़ाई है। आप भी इसे आज़माएं।",
      audio_url: "data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAAAP8A/w==",
    },
  ],
  mr: [
    {
      suggestion_id: "sugg_001_mr",
      merchant_id: "merchant_001",
      type: "failure_guard",
      title: "⚠️ २०% सवलत देणे टाळा",
      body: "तीन आठवड्यांपूर्वी २०% डिस्काउंट दिल्याने तुमची कमाई ३५% कमी झाली होती. या आठवड्यात सवलत देणे टाळा.",
      confidence: 0.96,
      action: "या आठवड्यात वस्तू नेहमीच्या दरानेच विका.",
      voice_script:
        "नमस्कार राजू भाऊ. मागच्या वेळी आपण २०% डिस्काउंट दिला होता — त्या आठवड्यात कमाई ३५% कमी झाली होती. या वेळी डिस्काउंट देऊ नका.",
      audio_url: "data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAAAP8A/w==",
    },
    {
      suggestion_id: "sugg_002_mr",
      merchant_id: "merchant_001",
      type: "personal_best",
      title: "✅ सकाळी ७ वाजता दुकान उघडा",
      body: "सहा आठवड्यांपूर्वी सकाळी ७ वाजता दुकान उघडल्यामुळे तुमची कमाई २५% वाढली होती. हे पुन्हा करा.",
      confidence: 0.94,
      action: "दुकान सकाळी ठीक ७:०० वाजता उघडा.",
      voice_script:
        "नमस्कार राजू भाऊ. सहा आठवड्यांपूर्वी जेव्हा आपण सकाळी ७ वाजता दुकान उघडले होते, त्या आठवड्यात कमाई २५% वाढली होती. पुढील आठवड्यात पुन्हा लवकर उघडण्याचा प्रयत्न करा.",
      audio_url: "data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAAAP8A/w==",
    },
    {
      suggestion_id: "sugg_003_mr",
      merchant_id: "merchant_001",
      type: "network_wisdom",
      title: "🌐 परिसरातील व्यापारी: दूध व नाश्ता",
      body: "मुंबईतील १,८०० किराना व्यापाऱ्यांनी सकाळी ब्रेड आणि दुधाचा कॉम्बो ठेवून १८% जास्त विक्री केली आहे.",
      confidence: 0.91,
      action: "सकाळी ब्रेड आणि दुधाचा कॉम्बो पॅक काउंटरवर ठेवा.",
      voice_script:
        "नमस्कार राजू भाऊ. मुंबईतील किराणा व्यापाऱ्यांनी सकाळी दूध आणि ब्रेडचा कॉम्बो ठेवून विक्री १८% वाढवली आहे. आपणही हे करून पहा.",
      audio_url: "data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAAAP8A/w==",
    },
  ],
  en: [
    {
      suggestion_id: "sugg_001_en",
      merchant_id: "merchant_001",
      type: "failure_guard",
      title: "⚠️ Avoid 20% Discount",
      body: "Three weeks ago, running a 20% discount dropped your weekly revenue by 35%. Avoid giving discounts this week.",
      confidence: 0.96,
      action: "Sell products at standard prices without flat discounts.",
      voice_script:
        "Hello Raju bhai. Last time you offered a 20% discount, your revenue dropped by 35%. Please avoid giving discounts this week.",
      audio_url: "data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAAAP8A/w==",
    },
    {
      suggestion_id: "sugg_002_en",
      merchant_id: "merchant_001",
      type: "personal_best",
      title: "✅ Open Shop Early at 7 AM",
      body: "Six weeks ago, opening your shop at 7 AM increased your weekly revenue by 25%. Repeat this winning strategy.",
      confidence: 0.94,
      action: "Open your shop at 7:00 AM sharp with breakfast goods ready.",
      voice_script:
        "Hello Raju bhai. Six weeks ago when you opened your shop at 7 AM, your weekly earnings rose by 25%. Try opening early again this week.",
      audio_url: "data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAAAP8A/w==",
    },
    {
      suggestion_id: "sugg_003_en",
      merchant_id: "merchant_001",
      type: "network_wisdom",
      title: "🌐 Network: Milk & Bread Combos",
      body: "Over 1,800 kirana merchants across Mumbai increased morning sales by 18% with breakfast combo packs.",
      confidence: 0.91,
      action: "Place milk and fresh bread combo packs prominently on the counter.",
      voice_script:
        "Hello Raju bhai. Over 1,800 nearby kirana merchants in Mumbai boosted revenue by 18% with morning milk and bread combos. Consider trying this.",
      audio_url: "data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAAAP8A/w==",
    },
  ],
};

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const merchantId = searchParams.get("merchant_id") || "merchant_001";
  const language = searchParams.get("language") || "hi";
  const fastApiUrl = process.env.FASTAPI_BACKEND_URL || "http://localhost:8000";

  try {
    const res = await fetch(`${fastApiUrl}/api/merchant/${merchantId}/suggestions?language=${language}`, {
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

  const fallbackList = FALLBACK_SUGGESTIONS_MAP[language] || FALLBACK_SUGGESTIONS_MAP.hi;

  return NextResponse.json({
    suggestions: fallbackList,
    generated_at: new Date().toISOString(),
    is_fallback: true,
  });
}
