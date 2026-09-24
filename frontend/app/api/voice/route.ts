import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { suggestion_id, merchant_id = "merchant_001" } = body;
    const fastApiUrl = process.env.FASTAPI_BACKEND_URL || "http://localhost:8000";

    const res = await fetch(`${fastApiUrl}/api/merchant/${merchant_id}/voice`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ suggestion_id }),
    });

    if (res.ok) {
      const data = await res.json();
      return NextResponse.json(data);
    }
  } catch (err) {
    console.warn("Could not reach FastAPI voice endpoint:", err);
  }

  // Fallback audio
  return NextResponse.json({
    audio_url:
      "data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAAAP8A/w==",
    duration_seconds: 5.0,
  });
}
