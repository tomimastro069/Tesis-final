import { useState, useEffect, useCallback } from "react";
import { analyzeVulnerability } from "../services/api";
import type { Vulnerability } from "../app/components/VulnerabilityTable";

export function useAiAnalysis(targetUrl?: string) {
  const [aiSuggestions, setAiSuggestions] = useState<Record<string, string>>({});
  const [seenIds, setSeenIds] = useState<Set<string | number>>(new Set());
  const [analyzingIds, setAnalyzingIds] = useState<Set<string | number>>(new Set());

  useEffect(() => {
    if (targetUrl) {
      const saved = localStorage.getItem(`ai_analysis_${targetUrl}`);
      if (saved) {
        try {
          setAiSuggestions(JSON.parse(saved));
        } catch (e) {}
      }
    }
  }, [targetUrl]);

  const saveSuggestion = useCallback((id: string | number, text: string) => {
    setAiSuggestions(prev => {
      const next = { ...prev, [id]: text };
      if (targetUrl) {
        localStorage.setItem(`ai_analysis_${targetUrl}`, JSON.stringify(next));
      }
      return next;
    });
  }, [targetUrl]);

  const analyze = useCallback(async (vuln: Vulnerability) => {
    setAnalyzingIds(prev => new Set(prev).add(vuln.id));
    try {
      const suggestion = await analyzeVulnerability({
        id: vuln.id,
        name: vuln.name,
        type: vuln.type,
        severity: vuln.severity,
        description: vuln.description,
        location: vuln.location
      });
      saveSuggestion(vuln.id, suggestion);
      return suggestion;
    } catch (error) {
      console.error(error);
      const errText = "Ocurrió un error al contactar con la IA.";
      saveSuggestion(vuln.id, errText);
      return errText;
    } finally {
      setAnalyzingIds(prev => {
        const next = new Set(prev);
        next.delete(vuln.id);
        return next;
      });
    }
  }, [saveSuggestion]);

  const markAsSeen = useCallback((id: string | number) => {
    setSeenIds(prev => new Set(prev).add(id));
  }, []);

  return {
    aiSuggestions,
    seenIds,
    analyzingIds,
    analyze,
    markAsSeen,
    saveSuggestion
  };
}
