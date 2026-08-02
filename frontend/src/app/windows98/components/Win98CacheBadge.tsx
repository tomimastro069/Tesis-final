import React from "react";

export interface SqlmapCacheInfo {
  totalCandidatas: number;
  totalTesteadas: number;
  omitidasPorCache: string[];
  retesteadasPorVulnerablePrevia: string[];
  sqlmapEnCurso: boolean;
}

export interface FfufCacheInfo {
  totalCandidatas: number;
  totalTesteadas: number;
  omitidasPorCache: number;
}

/**
 * Badge grande y difícil de ignorar que muestra si un análisis usó caché.
 * La caché NO es algo exclusivo de SQLMap: FFUF también cachea palabras ya
 * probadas por wordlist. ZAP (Spider + Active Scan) no usa caché, siempre corre
 * completo. Este badge resume el estado GENERAL del análisis, con el detalle de
 * cada herramienta abajo. Se usa tanto en el reporte individual como en el
 * comparador (WinDiff).
 */
export function Win98CacheBadge({
  sqlmapCacheInfo,
  ffufCacheInfo,
  label
}: {
  sqlmapCacheInfo: SqlmapCacheInfo | null;
  ffufCacheInfo: FfufCacheInfo | null;
  label?: string;
}) {
  if (!sqlmapCacheInfo && !ffufCacheInfo) return null;

  const sqlmapOmitidoPorCompleto = !!sqlmapCacheInfo?.sqlmapEnCurso;
  const sqlmapUsoCache = !!sqlmapCacheInfo && (sqlmapCacheInfo.sqlmapEnCurso || sqlmapCacheInfo.omitidasPorCache.length > 0);
  const ffufUsoCache = !!ffufCacheInfo && ffufCacheInfo.omitidasPorCache > 0;
  const usoCache = sqlmapUsoCache || ffufUsoCache;

  const bg = sqlmapOmitidoPorCompleto ? "bg-[#ff0000] text-white" : usoCache ? "bg-[#ffcc00] text-black" : "bg-[#00a000] text-white";
  const icon = sqlmapOmitidoPorCompleto ? "🚫" : usoCache ? "⚠️" : "✅";
  const headline = sqlmapOmitidoPorCompleto
    ? "SQLMAP NO CORRIÓ (OMITIDO POR COMPLETO)"
    : usoCache
    ? "SE USÓ CACHÉ EN ESTE ANÁLISIS"
    : "SIN CACHÉ — TODO SE TESTEÓ DE NUEVO";

  return (
    <div className={`win98-border-deep px-2 py-1.5 flex items-center gap-2 ${bg}`}>
      <span className="text-2xl leading-none flex-shrink-0">{icon}</span>
      <div className="flex flex-col min-w-0 gap-0.5">
        <span className="font-bold text-sm uppercase tracking-wide">
          {label ? `${label}: ` : ""}
          {headline}
        </span>

        {ffufCacheInfo && (
          <span className="text-[11px] font-bold">
            FFUF: {ffufCacheInfo.totalTesteadas} de {ffufCacheInfo.totalCandidatas} palabra(s) probadas
            {ffufCacheInfo.omitidasPorCache > 0 ? ` — ${ffufCacheInfo.omitidasPorCache} omitida(s) por caché` : " — sin caché"}
          </span>
        )}

        {sqlmapCacheInfo && (
          <span className="text-[11px] font-bold">
            SQLMap: {sqlmapCacheInfo.totalTesteadas} de {sqlmapCacheInfo.totalCandidatas} URL(s) re-testeadas
            {sqlmapCacheInfo.omitidasPorCache.length > 0 ? ` — ${sqlmapCacheInfo.omitidasPorCache.length} omitida(s) por caché` : ""}
            {sqlmapCacheInfo.retesteadasPorVulnerablePrevia.length > 0
              ? ` — ${sqlmapCacheInfo.retesteadasPorVulnerablePrevia.length} re-testeada(s) por ser vulnerable(s) antes`
              : ""}
            {sqlmapOmitidoPorCompleto ? " — otro análisis lo estaba usando al mismo tiempo" : ""}
            {!sqlmapUsoCache ? " — sin caché" : ""}
          </span>
        )}

        <span className="text-[10px] font-normal opacity-80">ZAP (Spider + Active Scan) no usa caché: siempre corre completo.</span>
      </div>
    </div>
  );
}
