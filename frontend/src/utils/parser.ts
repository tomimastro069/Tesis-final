import { getVulnKnowledge, interpretConfidence } from "./vulnKnowledgeBase";

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
      if (sevString.includes("informational") || sevString.includes("informativo") || sevString.includes("informacional")) {
        return; // Ignore informational alerts
      } else if (sevString.includes("high") || sevString.includes("alta")) {
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
      else if (rcode === 1) { low++; risk = "Low"; }
      else { return; } // riskcode 0 is informational, ignore
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
    .map(([name, value], i) => {
      // Use golden angle approximation (137.5 degrees) to scatter hues beautifully
      const hue = (i * 137.5) % 360;
      const color = `hsl(${hue.toFixed(1)}, 75%, 55%)`;
      return { name, value, color };
    });

  const allVulnerabilities = [
    ...sqlVulns.map((v: any) => {
      const name = `SQL Injection in ${v.parametro || 'unknown'}`;
      const knowledge = getVulnKnowledge("SQL Injection", "Injection");
      return {
        id: Math.random().toString(),
        name,
        severity: "Critical",
        location: v.url,
        type: "Injection",
        status: "Open",
        description: "SQL Injection found by SQLMap",
        recommendation: "Use parameterized queries or prepared statements.",
        queEs: knowledge.queEs,
        peligroReal: knowledge.peligroReal,
        comoMitigar: knowledge.comoMitigar,
      };
    }),
    ...alerts.filter((a: any) => a._parsedSeverity).map((a: any) => {
      const name = a.vulnerabilidad || a.name;
      const method = a.metodo || a.method;
      const evidence = a.evidencia || a.evidence;
      const knowledge = getVulnKnowledge(name, "Configuration", method, evidence);
      return {
        id: Math.random().toString(),
        name,
        severity: a._parsedSeverity,
        location: a.url || a.instances?.[0]?.uri || "Various",
        type: "Configuration",
        status: "Open",
        method: method && method !== "N/A" ? method : undefined,
        confidence: a.confianza && a.confianza !== "N/A" ? a.confianza : undefined,
        confidenceNote: interpretConfidence(a.confianza),
        description: (a.descripcion || a.desc || "").replace(/<[^>]+>/g, ''),
        recommendation: (a.solucion || a.solution || "").replace(/<[^>]+>/g, ''),
        queEs: knowledge.queEs,
        peligroReal: knowledge.peligroReal,
        comoMitigar: knowledge.comoMitigar,
        // Prueba real capturada por el Active Scan de ZAP (vacío en reglas
        // pasivas, como headers faltantes, que no envían ningún payload).
        attackParam: a.parametro || undefined,
        attackPayload: a.payload_ataque || undefined,
        attackEvidence: a.evidencia || undefined,
      };
    })
  ];

  // Tablas de base de datos volcadas por SQLMap (--dump), si las hubo
  const sqlmapTables: Array<{ database: string; table: string; columns: string[]; rows: string[][] }> = [];
  const tablasExtraidas =
    rawData.sqlmap?.tablas_extraidas ||
    rawData.sqlmap_raw?.tablas_extraidas ||
    null;

  if (tablasExtraidas) {
    Object.entries(tablasExtraidas).forEach(([dbName, tables]: [string, any]) => {
      Object.entries(tables || {}).forEach(([tableName, tableData]: [string, any]) => {
        sqlmapTables.push({
          database: dbName,
          table: tableName,
          columns: tableData?.columns || [],
          rows: tableData?.rows || []
        });
      });
    });
  }

  // Estadísticas generales del escaneo (calculadas por el backend al consolidar los resultados)
  const resumenCrudo = rawData.resumen || {};
  const generalStats = {
    totalUrlsUnicas: resumenCrudo.total_urls_unicas ?? 0,
    urlsSpider: resumenCrudo.urls_spider ?? 0,
    alertasZap: resumenCrudo.alertas_zap ?? 0,
    rutasFfuf: resumenCrudo.rutas_ffuf ?? 0,
    vulnerabilidadesSqlmap: resumenCrudo.vulnerabilidades_sqlmap ?? 0
  };

  // Info de caché GENERAL del escaneo. No es algo exclusivo de SQLMap: FFUF también
  // cachea palabras ya probadas por wordlist, y SQLMap cachea URLs ya probadas y no
  // vulnerables. ZAP (Spider + Active Scan) no usa caché, siempre corre completo.
  //
  // rawData.cache_info es la ubicación nueva (top-level, { ffuf, sqlmap }). Se deja
  // como fallback rawData.sqlmap?.cache_info por si el registro es de un análisis
  // guardado antes de este cambio.
  const cacheInfoGeneral = rawData.cache_info || null;
  const sqlmapCacheCruda = cacheInfoGeneral?.sqlmap || rawData.sqlmap?.cache_info || rawData.sqlmap_raw?.cache_info || null;
  const ffufCacheCruda = cacheInfoGeneral?.ffuf || null;

  const sqlmapCacheInfo = sqlmapCacheCruda
    ? {
        totalCandidatas: sqlmapCacheCruda.total_candidatas ?? 0,
        totalTesteadas: sqlmapCacheCruda.total_testeadas ?? 0,
        omitidasPorCache: sqlmapCacheCruda.omitidas_por_cache || [],
        retesteadasPorVulnerablePrevia: sqlmapCacheCruda.retesteadas_por_vulnerable_previa || [],
        // true si este análisis se omitió por completo porque otro escaneo ya tenía
        // SQLMap corriendo en segundo plano al mismo tiempo (evita datos corruptos
        // por dos corridas pisándose el mismo log/script).
        sqlmapEnCurso: !!sqlmapCacheCruda.sqlmap_en_curso
      }
    : null;

  const ffufCacheInfo = ffufCacheCruda
    ? {
        totalCandidatas: ffufCacheCruda.total_candidatas ?? 0,
        totalTesteadas: ffufCacheCruda.total_testeadas ?? 0,
        omitidasPorCache: ffufCacheCruda.omitidas_por_cache ?? 0
      }
    : null;

  // Nivel de SQLMap usado en este análisis. Determina qué se puede esperar de tablas:
  // "basic" no extrae nada, "fast_evidence" solo trae nombres de BD/tablas/usuario,
  // "full_dump" es el único que trae las tablas completas (columnas + filas).
  const sqlmapLevel: string | null = rawData.sqlmap_level ?? null;

  const scanners = [];
  if (rawData.zap || rawData.zap_raw) scanners.push("OWASP ZAP");
  if (rawData.sqlmap || rawData.sqlmap_raw) scanners.push("SQLMap");

  const urlCounts: Record<string, number> = {};
  allVulnerabilities.forEach(v => {
    const url = v.location || "Unknown";
    urlCounts[url] = (urlCounts[url] || 0) + 1;
  });

  const uniqueEndpoints = Object.keys(urlCounts).filter(u => u !== "Unknown").length;

  const topVulnerableUrls = Object.entries(urlCounts)
    .filter(([url]) => url !== "Unknown" && url !== "Various")
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([url, count]) => ({ url, count }));

  let injectionCount = 0;
  let configCount = 0;
  
  const severityByTypeMap: Record<string, { Critical: number; High: number; Medium: number; Low: number; total: number }> = {};

  allVulnerabilities.forEach(v => {
    if (v.type === "Injection") injectionCount++;
    else if (v.type === "Configuration") configCount++;
    
    if (!severityByTypeMap[v.name]) {
      severityByTypeMap[v.name] = { Critical: 0, High: 0, Medium: 0, Low: 0, total: 0 };
    }
    const sev = v.severity as "Critical" | "High" | "Medium" | "Low";
    if (severityByTypeMap[v.name][sev] !== undefined) {
      severityByTypeMap[v.name][sev]++;
    }
    severityByTypeMap[v.name].total++;
  });

  const stackedSeverityByType = Object.entries(severityByTypeMap)
    .sort((a, b) => b[1].total - a[1].total)
    .map(([name, counts]) => ({
      name,
      Critical: counts.Critical,
      High: counts.High,
      Medium: counts.Medium,
      Low: counts.Low,
    }))
    .slice(0, 8); // Top 8 types for the chart

  return {
    total,
    score,
    riskLevel,
    severityData,
    typesData,
    allVulnerabilities,
    sqlmapTables,
    generalStats,
    sqlmapCacheInfo,
    ffufCacheInfo,
    sqlmapLevel,
    scanMetrics: {
      scanners: scanners.join(", ") || "Desconocido",
      uniqueEndpoints,
      topVulnerableUrls,
      threatNature: {
        injection: injectionCount,
        configuration: configCount
      },
      stackedSeverityByType
    }
  };
}
