import { useState, useEffect } from "react";
import { fetchScanResults } from "../services/api";
import type { Domain } from "../services/api";
import { parseSecurityResults } from "../utils/parser";

export function useScanReport(domain: Domain) {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    async function loadData() {
      if (!domain.scanId) {
        setLoading(false);
        return;
      }
      setLoading(true);
      try {
        const result = await fetchScanResults(domain.scanId);
        if (result && result.results) {
          const parsed = parseSecurityResults(result.results);
          setData(parsed);
        } else {
          setData(null);
        }
      } catch (e) {
        console.error("Failed to load results", e);
        setData(null);
      }
      setLoading(false);
    }
    loadData();
  }, [domain]);

  return { loading, data };
}
