"use client";

import React, { useEffect, useState, useCallback } from "react";
import { MerchantHeader } from "./components/MerchantHeader";
import { SuggestionCard } from "./components/SuggestionCard";
import { Suggestion } from "./types";
import { RefreshCw, Sparkles, AlertCircle, Radio, Clock, ShieldCheck } from "lucide-react";

export default function MerchantDashboard() {
  const merchantId = "merchant_001";
  const [language, setLanguage] = useState<"hi" | "mr" | "en">("hi");
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [refreshing, setRefreshing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [activePlayingId, setActivePlayingId] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string>("");

  const pageText = {
    hi: {
      heading: "आज के मुख्य व्यापार सुझाव",
      subheading: "आपके स्टोर के ऐतिहासिक डेटा और आसपास के सफल किराना रुझानों से तैयार किए गए",
      lastUpdatedPrefix: "अंतिम अपडेट:",
      refreshBtn: "ताज़ा करें (Refresh)",
      playingAudioTitle: "आवाज़ में सुझाव चल रहा है (Sarvam AI Bulbul v3)",
      closeBtn: "बंद करें ✕",
      errorMsg: "सुझाव लोड करने में समस्या आई। कृपया पुनः प्रयास करें।",
    },
    mr: {
      heading: "आजच्या प्रमुख व्यावसायिक शिफारसी",
      subheading: "तुमच्या दुकानाचा मागील डेटा आणि परिसरातील यशस्वी किराणा ट्रेंड्सवरून तयार केलेल्या",
      lastUpdatedPrefix: "शेवटचे अपडेट:",
      refreshBtn: "ताजे करा (Refresh)",
      playingAudioTitle: "आवाजात शिफारस सुरू आहे (Sarvam AI Bulbul v3)",
      closeBtn: "बंद करा ✕",
      errorMsg: "शिफारसी लोड करण्यात अडचण आली. कृपया पुन्हा प्रयत्न करा.",
    },
    en: {
      heading: "Today's Key Business Recommendations",
      subheading: "Synthesized from your store's historical patterns and local market trends",
      lastUpdatedPrefix: "Last updated:",
      refreshBtn: "Refresh",
      playingAudioTitle: "Playing Voice Recommendation (Sarvam AI Bulbul v3)",
      closeBtn: "Close ✕",
      errorMsg: "Failed to load recommendations. Please try again.",
    },
  }[language];

  const fetchSuggestions = useCallback(
    async (targetLang = language, isManualRefresh = false) => {
      if (isManualRefresh) setRefreshing(true);
      else setLoading(true);
      setError(null);

      try {
        const res = await fetch(`/api/suggestions?merchant_id=${merchantId}&language=${targetLang}`);
        if (!res.ok) {
          throw new Error(`Failed to fetch: ${res.statusText}`);
        }
        const data = await res.json();
        if (data.suggestions && Array.isArray(data.suggestions)) {
          setSuggestions(data.suggestions);
          const localeCode = targetLang === "mr" ? "mr-IN" : targetLang === "en" ? "en-IN" : "hi-IN";
          setLastUpdated(new Date().toLocaleTimeString(localeCode, { hour: "2-digit", minute: "2-digit" }));
        }
      } catch (err: unknown) {
        console.error("Error loading suggestions:", err);
        setError(pageText.errorMsg);
      } finally {
        setLoading(false);
        setRefreshing(false);
      }
    },
    [merchantId, language, pageText.errorMsg]
  );

  useEffect(() => {
    fetchSuggestions(language, false);
  }, [language, fetchSuggestions]);

  const handleLanguageChange = (newLang: "hi" | "mr" | "en") => {
    if (newLang === language) return;
    setLanguage(newLang);
    setActivePlayingId(null);
  };

  const handlePlayVoice = async (suggestionId: string) => {
    const current = suggestions.find((s) => s.suggestion_id === suggestionId);

    if (current && current.audio_url) {
      setActivePlayingId(suggestionId);
      return;
    }

    try {
      const res = await fetch("/api/voice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          suggestion_id: suggestionId,
          merchant_id: merchantId,
          language: language,
        }),
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
    <main className="min-h-screen lg:h-screen lg:overflow-hidden bg-slate-950 text-slate-100 py-3 sm:py-4 px-4 sm:px-6 lg:px-8 flex flex-col justify-between">
      <div className="max-w-6xl mx-auto w-full flex-1 flex flex-col justify-between">
        <div>
          {/* Top Header with interactive Language Switcher */}
          <MerchantHeader
            name="राजू किराना"
            category="किराना स्टोर"
            language={language}
            location="दादर, मुंबई"
            onLanguageChange={handleLanguageChange}
          />

          {/* Section title & controls */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
            <div>
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-amber-400" />
                <h2 className="text-lg md:text-xl font-bold tracking-tight text-white">
                  {pageText.heading}
                </h2>
              </div>
              <p className="text-slate-400 text-[11px] sm:text-xs mt-0.5">
                {pageText.subheading}
              </p>
            </div>

            <div className="flex items-center gap-3">
              {lastUpdated && (
                <span className="text-xs text-slate-400 flex items-center gap-1">
                  <Clock className="w-3.5 h-3.5" />
                  {pageText.lastUpdatedPrefix} {lastUpdated}
                </span>
              )}
              <button
                onClick={() => fetchSuggestions(language, true)}
                disabled={refreshing || loading}
                className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all disabled:opacity-50"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${refreshing ? "animate-spin text-amber-400" : ""}`} />
                <span>{pageText.refreshBtn}</span>
              </button>
            </div>
          </div>

          {/* Loading state */}
          {loading && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 my-6">
              {[1, 2, 3].map((i) => (
                <div
                  key={i}
                  className="h-72 rounded-2xl bg-slate-900/60 border border-slate-800 animate-pulse p-5 flex flex-col justify-between"
                >
                  <div className="space-y-3">
                    <div className="h-5 w-28 bg-slate-800 rounded-full"></div>
                    <div className="h-5 w-3/4 bg-slate-800 rounded"></div>
                    <div className="h-14 w-full bg-slate-800/60 rounded-xl"></div>
                  </div>
                  <div className="h-8 w-24 bg-slate-800 rounded-xl"></div>
                </div>
              ))}
            </div>
          )}

          {/* Error message */}
          {error && !loading && (
            <div className="p-3 rounded-xl bg-red-950/40 border border-red-800 text-red-300 flex items-center gap-3 my-3">
              <AlertCircle className="w-4 h-4 text-red-400 shrink-0" />
              <span className="text-xs">{error}</span>
            </div>
          )}

          {/* Suggestions Grid (3 Cards: Failure Guard, Personal Best, Network Wisdom) */}
          {!loading && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {suggestions.map((suggestion) => (
                <SuggestionCard
                  key={suggestion.suggestion_id}
                  suggestion={suggestion}
                  language={language}
                  isPlaying={activePlayingId === suggestion.suggestion_id}
                  onPlay={handlePlayVoice}
                />
              ))}
            </div>
          )}

          {/* Live Audio Status Bar */}
          {activePlayingId && (
            <div className="mt-3 p-3 rounded-xl bg-slate-900/90 border border-indigo-500/40 flex items-center justify-between gap-4 shadow-lg backdrop-blur-sm animate-fade-in">
              <div className="flex items-center gap-3">
                <Radio className="w-4 h-4 text-amber-400 animate-pulse" />
                <div>
                  <div className="text-xs font-bold text-white">
                    {pageText.playingAudioTitle}
                  </div>
                  <div className="text-[11px] text-slate-400">
                    {suggestions.find((s) => s.suggestion_id === activePlayingId)?.title}
                  </div>
                </div>
              </div>
              <button
                onClick={() => setActivePlayingId(null)}
                className="px-2.5 py-1 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700"
              >
                {pageText.closeBtn}
              </button>
            </div>
          )}
        </div>

        {/* Footer info banner */}
        <footer className="mt-3 pt-2.5 border-t border-slate-900 text-center text-xs text-slate-500 flex flex-col sm:flex-row items-center justify-between gap-2">
          <div className="flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" />
            <span>व्यापार साथी • Paytm Build for India AI Hackathon (Team Cutie&apos;s)</span>
          </div>
          <div className="text-slate-600 text-[11px]">
            Powered by LangGraph • Cognee • Sarvam AI TTS • Gemini Flash
          </div>
        </footer>
      </div>
    </main>
  );
}
