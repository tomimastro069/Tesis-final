import { useState, useMemo } from "react";
import type { Vulnerability } from "../app/components/VulnerabilityTable";

export function useVulnerabilitiesFilter(vulnerabilities: Vulnerability[]) {
  const [filterSeverity, setFilterSeverity] = useState<string>("All");
  const [filterType, setFilterType] = useState<string>("All");
  const [filterStatus, setFilterStatus] = useState<string>("All");

  const types = useMemo(() => {
    return Array.from(new Set(vulnerabilities.map(v => v.type)));
  }, [vulnerabilities]);

  const filteredVulnerabilities = useMemo(() => {
    return vulnerabilities.filter(v => {
      if (filterSeverity !== "All" && v.severity !== filterSeverity) return false;
      if (filterType !== "All" && v.type !== filterType) return false;
      if (filterStatus !== "All" && v.status !== filterStatus) return false;
      return true;
    });
  }, [vulnerabilities, filterSeverity, filterType, filterStatus]);

  return {
    filterSeverity,
    setFilterSeverity,
    filterType,
    setFilterType,
    filterStatus,
    setFilterStatus,
    types,
    filteredVulnerabilities
  };
}
