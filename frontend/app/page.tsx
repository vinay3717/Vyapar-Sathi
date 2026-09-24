"use client";

import React, { useEffect, useState, useCallback } from "react";
import { MerchantHeader } from "./components/MerchantHeader";
import { SuggestionCard } from "./components/SuggestionCard";
import { Suggestion } from "./types";
import { RefreshCw, Sparkles, AlertCircle, Radio, Clock, ShieldCheck } from "lucide-react";

export default function MerchantDashboard() {
  const merchantId = "merchant_001";
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [refreshing, setRefreshing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [activePlayingId, setActivePlayingId] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string>("");

  const fetchSuggestions = useCallback(async (isManualRefresh = false) => {
    if (isManualRefresh) setRefreshing(true);
    else setLoading(true);
    setError(null);

    try {
      const res = await fetch(`/api/suggestions?merchant_id=${merchantId}`);
      if (!res.ok) {
        throw new Error(`Failed to fetch: ${res.statusText}`);
      }
      const data = await res.json();
      if (data.suggestions && Array.isArray(data.suggestions)) {
        setSuggestions(data.suggestions);
        setLastUpdated(new Date().toLocaleTimeString("hi-IN", { hour: "2-digit", minute: "2-digit" }));
      }
    } catch (err: unknown) {
      console.error("Error loading suggestions:", err);
      setError("सुझाव लोड करने में समस्या आई। कृपया पुनः प्रयास करें।");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [merchantId]);

  useEffect(() => {
    fetchSuggestions();
  }, [fetchSuggestions]);

  const handlePlayVoice = async (suggestionId: string) => {
    // If the suggestion already has an audio_url, activate it
    const current = suggestions.find((s) => s.suggestion_id === suggestionId);

    if (current && current.audio_url) {
      setActivePlayingId(suggestionId);
      return;
    }

    try {
      // Call voice endpoint to get audio_url
      const res = await fetch("/api/voice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ suggestion_id: suggestionId, merchant_id: merchantId }),
      });

      if (res.ok) {
        const data = await res.json();
        if (data.audio_url) {
          setSuggestions((prev) =>
            prev.map((s) =>
              s.suggestion_id === suggestionId ? { ...s, audio_url: data.audio_url } : s
            )
          );
          setActivePlayingId(suggestionId);
        }
      }
    } catch (err) {
      console.error("Error fetching audio:", err);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        {/* Top Header */}
        <MerchantHeader
          name="राजू किराना"
          category="किराना स्टोर"
          language="hi"
          location="दादर, मुंबई"
        />

        {/* Section title & controls */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div>
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-amber-400" />
              <h2 className="text-xl md:text-2xl font-bold tracking-tight text-white">
                आज के मुख्य व्यापार सुझाव
              </h2>
            </div>
            <p className="text-slate-400 text-xs sm:text-sm mt-1">
              आपके स्टोर के ऐतिहासिक डेटा और आसपास के सफल किराना रुझानों से तैयार किए गए
            </p>
          </div>

          <div className="flex items-center gap-3">
            {lastUpdated && (
              <span className="text-xs text-slate-400 flex items-center gap-1">
                <Clock className="w-3.5 h-3.5" />
                अंतिम अपडेट: {lastUpdated}
              </span>
            )}
            <button
              onClick={() => fetchSuggestions(true)}
              disabled={refreshing || loading}
              className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all disabled:opacity-50"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${refreshing ? "animate-spin text-amber-400" : ""}`} />
              <span>ताज़ा करें (Refresh)</span>
            </button>
          </div>
        </div>

        {/* Loading state */}
        {loading && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 my-12">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="h-80 rounded-2xl bg-slate-900/60 border border-slate-800 animate-pulse p-6 flex flex-col justify-between"
              >
                <div className="space-y-4">
                  <div className="h-6 w-32 bg-slate-800 rounded-full"></div>
                  <div className="h-6 w-3/4 bg-slate-800 rounded"></div>
                  <div className="h-16 w-full bg-slate-800/60 rounded-xl"></div>
                </div>
                <div className="h-10 w-28 bg-slate-800 rounded-xl"></div>
              </div>
            ))}
          </div>
        )}

        {/* Error message */}
        {error && !loading && (
          <div className="p-4 rounded-xl bg-red-950/40 border border-red-800 text-red-300 flex items-center gap-3 my-6">
            <AlertCircle className="w-5 h-5 text-red-400 shrink-0" />
            <span className="text-sm">{error}</span>
          </div>
        )}

        {/* Suggestions Grid (3 Cards: Failure Guard, Personal Best, Network Wisdom) */}
        {!loading && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {suggestions.map((suggestion) => (
              <SuggestionCard
                key={suggestion.suggestion_id}
                suggestion={suggestion}
                isPlaying={activePlayingId === suggestion.suggestion_id}
                onPlay={handlePlayVoice}
              />
            ))}
          </div>
        )}

        {/* Live Audio Status Bar */}
        {activePlayingId && (
          <div className="mt-8 p-4 rounded-xl bg-slate-900/90 border border-indigo-500/40 flex items-center justify-between gap-4 shadow-lg backdrop-blur-sm animate-fade-in">
            <div className="flex items-center gap-3">
              <Radio className="w-5 h-5 text-amber-400 animate-pulse" />
              <div>
                <div className="text-xs font-bold text-white">
                  आवाज़ में सुझाव चल रहा है (Sarvam AI Bulbul v3)
                </div>
                <div className="text-[11px] text-slate-400">
                  {suggestions.find((s) => s.suggestion_id === activePlayingId)?.title}
                </div>
              </div>
            </div>
            <button
              onClick={() => setActivePlayingId(null)}
              className="px-3 py-1 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700"
            >
              बंद करें ✕
            </button>
          </div>
        )}

        {/* Footer info banner */}
        <footer className="mt-14 pt-6 border-t border-slate-900 text-center text-xs text-slate-500 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-indigo-400" />
            <span>व्यापार साथी • Paytm Build for India AI Hackathon (Team Kairos)</span>
          </div>
          <div className="text-slate-600">
            Powered by LangGraph • Cognee • Sarvam AI TTS • Gemini Flash
          </div>
        </footer>
      </div>
    </main>
  );
}
