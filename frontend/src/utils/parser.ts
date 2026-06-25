export function parseSecurityResults(rawData: any) {
  if (!rawData) return null;

  const alerts: any[] = [];
  if (rawData.zap && rawData.zap.alertas) {
    alerts.push(...rawData.zap.alertas);
  } else if (rawData.zap_raw && rawData.zap_raw.site) {
    // Fallback in case of old raw data format
    rawData.zap_raw.site.forEach((s: any) => {
      if (s.alerts) alerts.push(...s.alerts);
    });
  }

  const sqlVulns: any[] = [];
  if (rawData.sqlmap && rawData.sqlmap.vulnerabilidades) {
    sqlVulns.push(...rawData.sqlmap.vulnerabilidades);
  } else if (Array.isArray(rawData.sqlmap_raw)) {
    sqlVulns.push(...rawData.sqlmap_raw);
  } else if (rawData.sqlmap_raw && rawData.sqlmap_raw.vulnerabilidades) {
    sqlVulns.push(...rawData.sqlmap_raw.vulnerabilidades);
  }

  let critical = 0;
  let high = 0;
  let medium = 0;
  let low = 0;

  const vulnTypes: Record<string, number> = {};

  alerts.forEach(a => {
    // Parse severity from new format "Medium (High)" or old format riskcode
    let risk = "Low";
    if (a.severidad) {
      const sevString = a.severidad.toLowerCase();
      if (sevString.includes("high") || sevString.includes("alta")) {
        high++; risk = "High";
      } else if (sevString.includes("medium") || sevString.includes("media")) {
        medium++; risk = "Medium";
      } else if (sevString.includes("low") || sevString.includes("baja")) {
        low++; risk = "Low";
      } else {
        low++; // Default
      }
    } else {
      // Old format fallback
      const rcode = parseInt(a.riskcode || "0", 10);
      if (rcode === 3) { high++; risk = "High"; }
      else if (rcode === 2) { medium++; risk = "Medium"; }
      else { low++; risk = "Low"; }
    }
    
    a._parsedSeverity = risk;
    const name = a.vulnerabilidad || a.name || "Unknown";
    vulnTypes[name] = (vulnTypes[name] || 0) + 1;
  });

  sqlVulns.forEach((v: any) => {
    critical++;
    const name = "SQL Injection";
    vulnTypes[name] = (vulnTypes[name] || 0) + 1;
  });

  const total = critical + high + medium + low;
  const score = Math.max(0, 100 - (critical * 20 + high * 10 + medium * 5 + low * 1));
  const riskLevel = critical > 0 || high > 0 ? "ALTO" : medium > 0 ? "MEDIO" : "BAJO";

  const severityData = [
    { name: "Critical", count: critical, color: "#dc2626" },
    { name: "High", count: high, color: "#ea580c" },
    { name: "Medium", count: medium, color: "#d97706" },
    { name: "Low", count: low, color: "#3b82f6" },
  ];

  const typesData = Object.entries(vulnTypes)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([name, value], i) => {
      const colors = ["#ea580c", "#dc2626", "#d97706", "#3b82f6", "#10b981"];
      return { name, value, color: colors[i % colors.length] };
    });

  const allVulnerabilities = [
    ...sqlVulns.map((v: any) => ({
      id: Math.random().toString(),
      name: `SQL Injection in ${v.parametro || 'unknown'}`,
      severity: "Critical",
      location: v.url,
      type: "Injection",
      status: "Open",
      description: "SQL Injection found by SQLMap",
      recommendation: "Use parameterized queries or prepared statements."
    })),
    ...alerts.map((a: any) => ({
      id: Math.random().toString(),
      name: a.vulnerabilidad || a.name,
      severity: a._parsedSeverity,
      location: a.url || a.instances?.[0]?.uri || "Various",
      type: "Configuration",
      status: "Open",
      description: (a.descripcion || a.desc || "").replace(/<[^>]+>/g, ''),
      recommendation: (a.solucion || a.solution || "").replace(/<[^>]+>/g, '')
    }))
  ];

  return {
    total,
    score,
    riskLevel,
    severityData,
    typesData,
    allVulnerabilities
  };
}
