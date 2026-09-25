export type SuggestionType = "failure_guard" | "personal_best" | "network_wisdom";

export interface Suggestion {
  suggestion_id: string;
  merchant_id: string;
  type: SuggestionType;
  title: string;
  body: string;
  confidence: number;
  action: string;
  voice_script: string;
  audio_url?: string | null;
}

export interface Merchant {
  merchant_id: string;
  name: string;
  language: "hi" | "mr" | "en";
  category: string;
}
