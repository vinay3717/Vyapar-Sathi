"use client";

import React from "react";
import { Store, Globe, ShieldCheck } from "lucide-react";

interface MerchantHeaderProps {
  name?: string;
  category?: string;
  language?: "hi" | "mr" | "en";
  location?: string;
  onLanguageChange?: (lang: "hi" | "mr" | "en") => void;
}

export const MerchantHeader: React.FC<MerchantHeaderProps> = ({
  name = "राजू किराना",
  category = "किराना स्टोर",
  language = "hi",
  location = "दादर, मुंबई",
  onLanguageChange,
}) => {
  const content = {
    hi: {
      salutation: "नमस्ते,",
      subtext: "आपके व्यवसाय के पिछले अनुभव और नेटवर्क की समझ पर आधारित सुझाव",
      activeBadge: "AI व्यापार साथी सक्रिय",
      partnerBadge: "Paytm पार्टनर",
      categoryLabel: "दुकान श्रेणी",
      languageLabel: "भाषा चुनें",
      categoryName: category,
      locationName: location,
    },
    mr: {
      salutation: "नमस्कार,",
      subtext: "तुमच्या व्यवसायाच्या मागील अनुभव आणि नेटवर्कच्या ज्ञानावर आधारित शिफारसी",
      activeBadge: "AI व्यापार साथी सक्रिय",
      partnerBadge: "Paytm पार्टनर",
      categoryLabel: "दुकान श्रेणी",
      languageLabel: "भाषा निवडा",
      categoryName: "किराणा स्टोअर",
      locationName: "दादर, मुंबई",
    },
    en: {
      salutation: "Welcome,",
      subtext: "Proactive recommendations powered by your past decisions & merchant network",
      activeBadge: "AI Merchant Teammate Active",
      partnerBadge: "Paytm Partner",
      categoryLabel: "STORE CATEGORY",
      languageLabel: "SELECT LANGUAGE",
      categoryName: "Kirana Store",
      locationName: "Dadar, Mumbai",
    },
  }[language] || {
    salutation: "नमस्ते,",
    subtext: "आपके व्यवसाय के पिछले अनुभव और नेटवर्क की समझ पर आधारित सुझाव",
    activeBadge: "AI व्यापार साथी सक्रिय",
    partnerBadge: "Paytm पार्टनर",
    categoryLabel: "दुकान श्रेणी",
    languageLabel: "भाषा चुनें",
    categoryName: category,
    locationName: location,
  };

  const languages: Array<{ code: "hi" | "mr" | "en"; label: string }> = [
    { code: "hi", label: "हिन्दी" },
    { code: "mr", label: "मराठी" },
    { code: "en", label: "English" },
  ];

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
              {content.activeBadge}
            </span>
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-white/10 text-indigo-200 border border-white/10">
              <ShieldCheck className="w-3.5 h-3.5 text-blue-400" />
              {content.partnerBadge}
            </span>
          </div>

          <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight text-white flex items-center gap-2">
            {content.salutation}{" "}
            <span className="bg-gradient-to-r from-amber-200 to-amber-400 bg-clip-text text-transparent">
              {language === "en" ? "Raju Kirana" : name}
            </span>
          </h1>
          <p className="text-slate-300 text-sm mt-1 flex items-center gap-3">
            <span>{content.subtext}</span>
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* Store Category pill */}
          <div className="flex items-center gap-2 bg-slate-800/80 px-3.5 py-2 rounded-xl border border-slate-700/60 shadow-sm">
            <Store className="w-4 h-4 text-indigo-400" />
            <div className="text-xs">
              <div className="text-slate-400 text-[10px] uppercase font-bold tracking-wider">
                {content.categoryLabel}
              </div>
              <div className="font-semibold text-white">
                {content.categoryName} • {content.locationName}
              </div>
            </div>
          </div>

          {/* Interactive Language Switcher */}
          <div className="flex items-center gap-1.5 bg-slate-800/90 p-1.5 rounded-xl border border-slate-700/70 shadow-sm">
            <div className="flex items-center gap-1 pl-2 pr-1 text-slate-400 text-xs">
              <Globe className="w-3.5 h-3.5 text-emerald-400" />
              <span className="hidden sm:inline text-[10px] font-bold uppercase tracking-wider text-slate-400 mr-1">
                {content.languageLabel}
              </span>
            </div>
            <div className="flex items-center gap-1">
              {languages.map((l) => {
                const isActive = language === l.code;
                return (
                  <button
                    key={l.code}
                    id={`lang-btn-${l.code}`}
                    onClick={() => onLanguageChange && onLanguageChange(l.code)}
                    className={`px-3 py-1 text-xs font-semibold rounded-lg transition-all ${
                      isActive
                        ? "bg-gradient-to-r from-indigo-500 to-blue-600 text-white shadow-md shadow-indigo-500/20"
                        : "text-slate-300 hover:text-white hover:bg-slate-700/60"
                    }`}
                  >
                    {l.label}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default MerchantHeader;
