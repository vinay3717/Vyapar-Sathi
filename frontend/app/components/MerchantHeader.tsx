"use client";

import React from "react";
import { Store, Globe, ShieldCheck } from "lucide-react";

interface MerchantHeaderProps {
  name?: string;
  category?: string;
  language?: "hi" | "mr" | "en";
  location?: string;
}

export const MerchantHeader: React.FC<MerchantHeaderProps> = ({
  name = "राजू किराना",
  category = "किराना स्टोर",
  language = "hi",
  location = "दादर, मुंबई",
}) => {
  const languageNames: Record<string, string> = {
    hi: "हिन्दी (Hindi)",
    mr: "मराठी (Marathi)",
    en: "English",
  };

  return (
    <header className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-6 shadow-xl border border-indigo-800/40 mb-8 backdrop-blur-md">
      {/* Decorative ambient background glows */}
      <div className="absolute top-0 right-0 w-80 h-80 bg-indigo-500/10 rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-60 h-60 bg-blue-500/10 rounded-full blur-2xl -ml-20 -mb-20 pointer-events-none" />

      <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-5">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              AI व्यापार साथी सक्रिय
            </span>
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-white/10 text-indigo-200 border border-white/10">
              <ShieldCheck className="w-3.5 h-3.5 text-blue-400" />
              Paytm पार्टनर
            </span>
          </div>

          <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight text-white flex items-center gap-2">
            नमस्ते, <span className="bg-gradient-to-r from-amber-200 to-amber-400 bg-clip-text text-transparent">{name}</span>
          </h1>
          <p className="text-slate-300 text-sm mt-1 flex items-center gap-3">
            <span>आपके व्यवसाय के पिछले अनुभव और नेटवर्क की समझ पर आधारित सुझाव</span>
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <div className="flex items-center gap-2 bg-slate-800/80 px-3.5 py-2 rounded-xl border border-slate-700/60 shadow-sm">
            <Store className="w-4 h-4 text-indigo-400" />
            <div className="text-xs">
              <div className="text-slate-400 text-[10px] uppercase font-bold tracking-wider">दुकान श्रेणी</div>
              <div className="font-semibold text-white">{category} • {location}</div>
            </div>
          </div>

          <div className="flex items-center gap-2 bg-slate-800/80 px-3.5 py-2 rounded-xl border border-slate-700/60 shadow-sm">
            <Globe className="w-4 h-4 text-emerald-400" />
            <div className="text-xs">
              <div className="text-slate-400 text-[10px] uppercase font-bold tracking-wider">भाषा</div>
              <div className="font-semibold text-emerald-300">{languageNames[language] || language}</div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default MerchantHeader;
