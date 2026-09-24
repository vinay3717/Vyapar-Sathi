"use client";

import React, { useEffect, useRef, useState } from "react";
import { Play, Pause, CheckCircle2, AlertCircle } from "lucide-react";

interface VoicePlayerProps {
  audioUrl?: string | null;
  autoPlay?: boolean;
  onEnded?: () => void;
  className?: string;
}

export const VoicePlayer: React.FC<VoicePlayerProps> = ({
  audioUrl,
  autoPlay = true,
  onEnded,
  className = "",
}) => {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [hasFinished, setHasFinished] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!audioUrl) return;

    setHasFinished(false);
    setError(null);

    const audio = new Audio(audioUrl);
    audioRef.current = audio;

    const handlePlay = () => setIsPlaying(true);
    const handlePause = () => setIsPlaying(false);
    const handleEnded = () => {
      setIsPlaying(false);
      setHasFinished(true);
      if (onEnded) onEnded();
    };
    const handleError = () => {
      setIsPlaying(false);
      setError("ऑडियो प्ले करने में समस्या आई");
    };

    audio.addEventListener("play", handlePlay);
    audio.addEventListener("pause", handlePause);
    audio.addEventListener("ended", handleEnded);
    audio.addEventListener("error", handleError);

    if (autoPlay) {
      audio.play().catch((err) => {
        console.warn("Autoplay blocked by browser policy, user interaction required:", err);
        setIsPlaying(false);
      });
    }

    return () => {
      audio.pause();
      audio.removeEventListener("play", handlePlay);
      audio.removeEventListener("pause", handlePause);
      audio.removeEventListener("ended", handleEnded);
      audio.removeEventListener("error", handleError);
    };
  }, [audioUrl, autoPlay, onEnded]);

  const togglePlay = () => {
    if (!audioRef.current) return;

    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play().catch((err) => {
        console.error("Playback failed:", err);
      });
    }
  };

  if (!audioUrl) {
    return null;
  }

  return (
    <div
      className={`inline-flex items-center gap-3 px-3.5 py-1.5 rounded-full text-xs font-medium transition-all duration-200 border ${
        isPlaying
          ? "bg-amber-500/10 text-amber-900 border-amber-400 dark:bg-amber-400/20 dark:text-amber-200"
          : hasFinished
          ? "bg-emerald-50 text-emerald-800 border-emerald-300 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-700/50"
          : "bg-slate-100 text-slate-800 border-slate-300 dark:bg-slate-800 dark:text-slate-200"
      } ${className}`}
    >
      <button
        onClick={togglePlay}
        type="button"
        aria-label={isPlaying ? "रोकें" : "सुनें"}
        className="flex items-center gap-1.5 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-indigo-500 rounded-full"
      >
        {isPlaying ? (
          <>
            <Pause className="w-3.5 h-3.5 animate-pulse text-amber-600 dark:text-amber-400" />
            <span className="font-semibold text-amber-700 dark:text-amber-300">▶ बज रहा है...</span>
            <span className="flex items-center gap-0.5 ml-1">
              <span className="w-1 h-3 bg-amber-500 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
              <span className="w-1 h-4 bg-amber-500 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
              <span className="w-1 h-2 bg-amber-500 rounded-full animate-bounce"></span>
            </span>
          </>
        ) : hasFinished ? (
          <>
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            <span className="font-medium text-emerald-700 dark:text-emerald-300">✓ सुना (दोबारा सुनें ↻)</span>
          </>
        ) : (
          <>
            <Play className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400 fill-current" />
            <span>सुझाव सुनें</span>
          </>
        )}
      </button>

      {error && (
        <span className="flex items-center gap-1 text-[11px] text-red-600">
          <AlertCircle className="w-3 h-3" />
          {error}
        </span>
      )}
    </div>
  );
};

export default VoicePlayer;
