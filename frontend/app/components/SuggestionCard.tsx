"use client";

import React from "react";
import { Suggestion, SuggestionType } from "../types";
import { VoicePlayer } from "./VoicePlayer";
import { Volume2, AlertTriangle, TrendingUp, Users, ArrowRight } from "lucide-react";

interface SuggestionCardProps {
  suggestion: Suggestion;
  isPlaying?: boolean;
  onPlay: (suggestionId: string) => void;
}

interface TypeConfig {
  label: string;
  subLabel: string;
  icon: React.ReactNode;
  containerClass: string;
  badgeClass: string;
  actionBgClass: string;
  confidenceColorClass: string;
  buttonClass: string;
}

export const SuggestionCard: React.FC<SuggestionCardProps> = ({
  suggestion,
  isPlaying = false,
  onPlay,
}) => {
  const typeConfigs: Record<SuggestionType, TypeConfig> = {
    failure_guard: {
      label: "⚠️ सावधान",
      subLabel: "Failure Guard • पिछली गलती से बचाव",
      icon: <AlertTriangle className="w-4 h-4 text-red-600 dark:text-red-400" />,
      containerClass:
        "border-red-200 bg-gradient-to-b from-red-50/70 to-white hover:border-red-400 shadow-sm hover:shadow-md dark:from-red-950/20 dark:to-slate-900 dark:border-red-900/50",
      badgeClass:
        "bg-red-100 text-red-800 border-red-200 dark:bg-red-900/40 dark:text-red-300 dark:border-red-800",
      actionBgClass:
        "bg-red-50 border-red-200 text-red-950 dark:bg-red-950/40 dark:border-red-800/60 dark:text-red-200",
      confidenceColorClass: "bg-red-500",
      buttonClass:
        "bg-red-600 hover:bg-red-700 text-white shadow-red-500/20 focus:ring-red-400",
    },
    personal_best: {
      label: "✅ आपकी सफलता",
      subLabel: "Personal Best • अपने श्रेष्ठ रिकॉर्ड को दोहराएं",
      icon: <TrendingUp className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />,
      containerClass:
        "border-emerald-200 bg-gradient-to-b from-emerald-50/70 to-white hover:border-emerald-400 shadow-sm hover:shadow-md dark:from-emerald-950/20 dark:to-slate-900 dark:border-emerald-900/50",
      badgeClass:
        "bg-emerald-100 text-emerald-800 border-emerald-200 dark:bg-emerald-900/40 dark:text-emerald-300 dark:border-emerald-800",
      actionBgClass:
        "bg-emerald-50 border-emerald-200 text-emerald-950 dark:bg-emerald-950/40 dark:border-emerald-800/60 dark:text-emerald-200",
      confidenceColorClass: "bg-emerald-500",
      buttonClass:
        "bg-emerald-600 hover:bg-emerald-700 text-white shadow-emerald-500/20 focus:ring-emerald-400",
    },
    network_wisdom: {
      label: "🌐 आसपास के व्यापारी",
      subLabel: "Network Wisdom • 1,800+ व्यापारियों का अनुभव",
      icon: <Users className="w-4 h-4 text-blue-600 dark:text-blue-400" />,
      containerClass:
        "border-blue-200 bg-gradient-to-b from-blue-50/70 to-white hover:border-blue-400 shadow-sm hover:shadow-md dark:from-blue-950/20 dark:to-slate-900 dark:border-blue-900/50",
      badgeClass:
        "bg-blue-100 text-blue-800 border-blue-200 dark:bg-blue-900/40 dark:text-blue-300 dark:border-blue-800",
      actionBgClass:
        "bg-blue-50 border-blue-200 text-blue-950 dark:bg-blue-950/40 dark:border-blue-800/60 dark:text-blue-200",
      confidenceColorClass: "bg-blue-500",
      buttonClass:
        "bg-blue-600 hover:bg-blue-700 text-white shadow-blue-500/20 focus:ring-blue-400",
    },
  };

  const config = typeConfigs[suggestion.type] || typeConfigs.network_wisdom;
  const confidencePercent = Math.min(100, Math.max(0, Math.round((suggestion.confidence || 0.8) * 100)));

  return (
    <div
      className={`rounded-2xl border p-6 flex flex-col justify-between transition-all duration-300 relative group overflow-hidden ${config.containerClass}`}
    >
      <div>
        {/* Top bar: Type badge & Confidence */}
        <div className="flex items-start justify-between gap-3 mb-4">
          <div className="flex flex-col gap-1">
            <span
              className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold border tracking-wide w-fit ${config.badgeClass}`}
            >
              {config.icon}
              {config.label}
            </span>
            <span className="text-[11px] text-slate-600 dark:text-slate-400 font-medium ml-1">
              {config.subLabel}
            </span>
          </div>

          {/* Confidence Indicator */}
          <div className="text-right flex flex-col items-end">
            <div className="text-[11px] font-semibold text-slate-500 dark:text-slate-400">
              भरोसा: <span className="font-bold text-slate-700 dark:text-slate-200">{confidencePercent}%</span>
            </div>
            <div className="w-16 h-1.5 bg-slate-200 dark:bg-slate-700 rounded-full mt-1 overflow-hidden">
              <div
                className={`h-full rounded-full transition-all duration-500 ${config.confidenceColorClass}`}
                style={{ width: `${confidencePercent}%` }}
              />
            </div>
          </div>
        </div>

        {/* Title */}
        <h2 className="text-lg font-bold text-slate-900 dark:text-white leading-snug mb-2">
          {suggestion.title}
        </h2>

        {/* Body Explanation */}
        <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed mb-5">
          {suggestion.body}
        </p>

        {/* Action Highlight Box (Imperative) */}
        <div
          className={`p-3.5 rounded-xl border flex items-start gap-2.5 mb-5 ${config.actionBgClass}`}
        >
          <ArrowRight className="w-4 h-4 mt-0.5 shrink-0 opacity-80" />
          <div>
            <div className="text-[10px] uppercase font-bold tracking-wider opacity-70">
              सुझावित कदम (Recommended Action)
            </div>
            <div className="text-sm font-bold leading-snug mt-0.5">
              {suggestion.action}
            </div>
          </div>
        </div>
      </div>

      {/* Footer: Voice Button or Embedded Player */}
      <div className="pt-3 border-t border-slate-200/80 dark:border-slate-800 flex items-center justify-between gap-3">
        {isPlaying && suggestion.audio_url ? (
          <VoicePlayer audioUrl={suggestion.audio_url} autoPlay={true} />
        ) : (
          <button
            onClick={() => onPlay(suggestion.suggestion_id)}
            type="button"
            className={`inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all duration-200 shadow-sm active:scale-95 focus:outline-none focus:ring-2 focus:ring-offset-1 ${config.buttonClass}`}
          >
            <Volume2 className="w-4 h-4 animate-pulse" />
            <span>सुनिए 🔊 (Suniye)</span>
          </button>
        )}

        {suggestion.audio_url && !isPlaying && (
          <span className="text-[11px] text-slate-600 dark:text-slate-400 font-medium">
            ऑडियो तैयार है
          </span>
        )}
      </div>
    </div>
  );
};

export default SuggestionCard;
