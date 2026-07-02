import { useState, useEffect, useCallback } from "react";
import { fetchAllScans, fetchScanProgress, fetchScanResults, deleteScan } from "../services/api";
import type { Domain } from "../services/api";
import { parseSecurityResults } from "../utils/parser";

export function useDomains() {
  const [domains, setDomains] = useState<Domain[]>([]);

  const loadDomains = useCallback(async () => {
    const data = await fetchAllScans();
    const processed = data.map(d => {
      if (d.status === 'completed' && d.rawResults) {
        const parsed = parseSecurityResults(d.rawResults);
        if (parsed) {
          return { ...d, score: parsed.score, riskLevel: parsed.riskLevel };
        }
      }
      return d;
    });
    setDomains(processed);
  }, []);

  useEffect(() => {
    loadDomains();
  }, [loadDomains]);

  // Polling para dominios en estado 'scanning'
  useEffect(() => {
    let interval: number;
    const hasScanning = domains.some(d => d.status === 'scanning');
    
    if (hasScanning) {
      interval = window.setInterval(async () => {
        try {
          const scanningDomains = domains.filter(d => d.status === 'scanning' && d.scanId);
          for (const d of scanningDomains) {
            const progressInfo = await fetchScanProgress(d.scanId!);
            if (progressInfo) {
              setDomains(prev => prev.map(pd => pd.id === d.id ? { ...pd, progress: progressInfo.percentage, progressMessage: progressInfo.message } : pd));
            }

            const results = await fetchScanResults(d.scanId!);
            if (results && results.status === 'completed' && results.results) {
              const parsed = parseSecurityResults(results.results);
              if (parsed) {
                setDomains(prev => {
                  const updated = prev.map(pd => pd.id === d.id ? { ...pd, status: 'completed' as const, score: parsed.score, riskLevel: parsed.riskLevel } : pd);
                  return updated;
                });
              }
            } else if (results && results.status === 'failed') {
              setDomains(prev => {
                const updated = prev.map(pd => pd.id === d.id ? { ...pd, status: 'error' as const } : pd);
                return updated;
              });
            }
          }
        } catch (error) {
          console.error("Error durante el polling:", error);
        }
      }, 3000);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [domains]);

  const handleAddDomain = useCallback((domain: Domain) => {
    setDomains(prev => [domain, ...prev]);
  }, []);

  const handleDeleteDomain = useCallback(async (domain: Domain) => {
    if (!domain.scanId) {
      setDomains(prev => prev.filter(d => d.id !== domain.id));
      return true;
    }
    
    if (window.confirm("¿Estás seguro de que quieres eliminar este dominio del panel?")) {
      try {
        await deleteScan(domain.scanId);
        setDomains(prev => prev.filter(d => d.id !== domain.id));
        return true;
      } catch (err) {
        alert("Error al eliminar el dominio");
        return false;
      }
    }
    return false;
  }, []);

  return {
    domains,
    loadDomains,
    handleAddDomain,
    handleDeleteDomain
  };
}
