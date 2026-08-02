import React, { useMemo, useState } from "react";
import { useScanReport } from "../../../hooks/useScanReport";
import type { Domain } from "../../../services/api";

interface Props {
  /** Análisis más antiguo (línea base, equivalente a "a/" en un diff de git) */
  domainA: Domain;
  /** Análisis más reciente (equivalente a "b/" en un diff de git) */
  domainB: Domain;
}

type LineStatus = "added" | "removed" | "context";

interface DiffLine {
  key: string;
  status: LineStatus;
  vuln: any;
  count: number;
  /** true si esta línea "removed" corresponde a una URL que SQLMap NO volvió a
   * testear en B por caché (ya estaba marcada como no vulnerable antes). En ese
   * caso no se puede asegurar que la vulnerabilidad haya sido corregida. */
  cacheAmbiguous?: boolean;
}

interface TableDiffLine {
  key: string;
  status: LineStatus;
  table: { database: string; table: string; columns: string[]; rows: string[][] };
  rowCount: number;
  rowsDelta: number;
}

function keyOf(v: any) {
  return `${v.type}||${v.name}||${v.location}`;
}

function keyOfTable(t: any) {
  return `${t.database}::${t.table}`;
}

function shortTarget(domain: Domain) {
  return domain.target.replace(/^https?:\/\//, "");
}

function fileNameFor(domain: Domain) {
  return `Analisis_${shortTarget(domain)}_${domain.id.slice(0, 5)}.doc`;
}

function formatDate(dateStr: string | null) {
  if (!dateStr) return "Desconocida";
  const hasTz = /Z|[+-]\d{2}:\d{2}$/.test(dateStr);
  const d = new Date(hasTz ? dateStr : dateStr + "Z");
  return d.toLocaleString();
}

export function Win98DiffViewer({ domainA, domainB }: Props) {
  const { loading: loadingA, data: dataA } = useScanReport(domainA);
  const { loading: loadingB, data: dataB } = useScanReport(domainB);
  const [filter, setFilter] = useState<"all" | "added" | "removed" | "cached">("all");

  const loading = loadingA || loadingB;

  const diff = useMemo(() => {
    if (!dataA || !dataB) return null;

    const countMap = (list: any[]) => {
      const map = new Map<string, { count: number; sample: any }>();
      (list || []).forEach((v: any) => {
        const k = keyOf(v);
        const existing = map.get(k);
        if (existing) existing.count++;
        else map.set(k, { count: 1, sample: v });
      });
      return map;
    };

    const mapA = countMap(dataA.allVulnerabilities);
    const mapB = countMap(dataB.allVulnerabilities);
    const allKeys = new Set<string>([...mapA.keys(), ...mapB.keys()]);

    // URLs que SQLMap NO volvió a testear en el análisis B por estar cacheadas
    // (ya evaluadas antes como no vulnerables). Si una vulnerabilidad de SQLMap
    // "desaparece" en B pero su URL está acá, no sabemos si se corrigió o
    // simplemente no se volvió a probar.
    const omitidasEnB = new Set<string>(dataB.sqlmapCacheInfo?.omitidasPorCache || []);
    // Si SQLMap se omitió por completo en B (otro análisis lo estaba usando al mismo
    // tiempo), TODAS las vulnerabilidades de SQLMap de A quedan sin confirmar en B,
    // no solo las que estaban en la lista de omitidas.
    const sqlmapNoCorrioEnB = !!dataB.sqlmapCacheInfo?.sqlmapEnCurso;

    const lines: DiffLine[] = [];

    allKeys.forEach((k) => {
      const inA = mapA.get(k);
      const inB = mapB.get(k);
      const countA = inA?.count || 0;
      const countB = inB?.count || 0;
      const sample = (inB || inA)!.sample;
      const esCacheAmbigua = sample.type === "Injection" && (sqlmapNoCorrioEnB || omitidasEnB.has(sample.location));

      if (countA > 0 && countB > 0) {
        lines.push({ key: `${k}::ctx`, status: "context", vuln: sample, count: Math.min(countA, countB) });
        if (countB > countA) {
          lines.push({ key: `${k}::add`, status: "added", vuln: sample, count: countB - countA });
        } else if (countA > countB) {
          lines.push({ key: `${k}::rem`, status: "removed", vuln: sample, count: countA - countB, cacheAmbiguous: esCacheAmbigua });
        }
      } else if (countB > 0) {
        lines.push({ key: `${k}::add`, status: "added", vuln: sample, count: countB });
      } else if (countA > 0) {
        lines.push({ key: `${k}::rem`, status: "removed", vuln: sample, count: countA, cacheAmbiguous: esCacheAmbigua });
      }
    });

    const order: Record<LineStatus, number> = { removed: 0, added: 1, context: 2 };
    lines.sort((a, b) => order[a.status] - order[b.status] || a.vuln.name.localeCompare(b.vuln.name));

    const added = lines.filter((l) => l.status === "added").reduce((s, l) => s + l.count, 0);
    const removed = lines.filter((l) => l.status === "removed" && !l.cacheAmbiguous).reduce((s, l) => s + l.count, 0);
    const unchanged = lines.filter((l) => l.status === "context").reduce((s, l) => s + l.count, 0);
    const cacheAmbiguousCount = lines
      .filter((l) => l.status === "removed" && l.cacheAmbiguous)
      .reduce((s, l) => s + l.count, 0);

    // Diff de tablas de base de datos volcadas por SQLMap
    const tablesA = new Map<string, any>((dataA.sqlmapTables || []).map((t: any) => [keyOfTable(t), t]));
    const tablesB = new Map<string, any>((dataB.sqlmapTables || []).map((t: any) => [keyOfTable(t), t]));
    const tableKeys = new Set<string>([...tablesA.keys(), ...tablesB.keys()]);

    const tableLines: TableDiffLine[] = [];
    tableKeys.forEach((k) => {
      const a = tablesA.get(k);
      const b = tablesB.get(k);
      if (a && b) {
        tableLines.push({
          key: k,
          status: "context",
          table: b,
          rowCount: b.rows.length,
          rowsDelta: b.rows.length - a.rows.length
        });
      } else if (b) {
        tableLines.push({ key: k, status: "added", table: b, rowCount: b.rows.length, rowsDelta: b.rows.length });
      } else if (a) {
        tableLines.push({ key: k, status: "removed", table: a, rowCount: a.rows.length, rowsDelta: -a.rows.length });
      }
    });
    tableLines.sort(
      (a, b) => order[a.status] - order[b.status] || `${a.table.database}.${a.table.table}`.localeCompare(`${b.table.database}.${b.table.table}`)
    );

    return {
      lines,
      added,
      removed,
      unchanged,
      cacheAmbiguousCount,
      scoreDelta: (dataB.score ?? 0) - (dataA.score ?? 0),
      tableLines
    };
  }, [dataA, dataB]);

  if (loading) {
    return (
      <div className="bg-[#c0c0c0] h-full p-4 font-win98 text-black flex items-center justify-center text-xs">
        Comparando análisis de {shortTarget(domainA)} y {shortTarget(domainB)}...
      </div>
    );
  }

  if (!dataA || !dataB || !diff) {
    return (
      <div className="bg-[#c0c0c0] h-full p-4 font-win98 text-black flex items-center justify-center text-xs">
        Error al cargar uno de los dos análisis para comparar.
      </div>
    );
  }

  const visibleLines = diff.lines.filter((l) => {
    if (filter === "all") return true;
    if (filter === "cached") return l.status === "removed" && l.cacheAmbiguous;
    if (filter === "removed") return l.status === "removed" && !l.cacheAmbiguous;
    return l.status === filter;
  });

  const severityRows = ["Critical", "High", "Medium", "Low"].map((name) => {
    const a = dataA.severityData.find((s: any) => s.name === name)?.count ?? 0;
    const b = dataB.severityData.find((s: any) => s.name === name)?.count ?? 0;
    return { name, a, b, delta: b - a };
  });

  return (
    <div className="bg-[#c0c0c0] h-full font-win98 text-black p-2 select-none flex flex-col gap-2 overflow-hidden">
      {/* Cabecera estilo "WinDiff" con los dos archivos comparados */}
      <div className="win98-border bg-[#c0c0c0] p-2 flex flex-col gap-1 flex-shrink-0 text-xs">
        <div className="flex items-center gap-2">
          <img src="https://win98icons.alexmeub.com/icons/png/notepad-1.png" className="w-4 h-4" alt="A" />
          <span className="font-bold">Base (A):</span>
          <span>{fileNameFor(domainA)}</span>
          <span className="text-gray-600">— {formatDate(domainA.lastScan)}</span>
        </div>
        <div className="flex items-center gap-2">
          <img src="https://win98icons.alexmeub.com/icons/png/notepad-1.png" className="w-4 h-4" alt="B" />
          <span className="font-bold">Comparado (B):</span>
          <span>{fileNameFor(domainB)}</span>
          <span className="text-gray-600">— {formatDate(domainB.lastScan)}</span>
        </div>

        <div className="w-full h-[1px] border-t border-gray-500 border-b border-white my-1"></div>

        <div className="flex items-center gap-4 flex-wrap">
          <span>
            Puntaje: <span className="font-bold">{dataA.score}</span> → <span className="font-bold">{dataB.score}</span>{" "}
            <span className={diff.scoreDelta > 0 ? "text-[#006400] font-bold" : diff.scoreDelta < 0 ? "text-[#800000] font-bold" : ""}>
              ({diff.scoreDelta > 0 ? "+" : ""}{diff.scoreDelta})
            </span>
          </span>
          <span className="text-[#006400] font-bold">+{diff.added} nuevas</span>
          <span className="text-[#800000] font-bold">-{diff.removed} corregidas</span>
          <span className="text-gray-600">{diff.unchanged} sin cambios</span>
          {diff.cacheAmbiguousCount > 0 && (
            <span className="text-[#806000] font-bold">⚠ {diff.cacheAmbiguousCount} sin confirmar (caché)</span>
          )}
        </div>

        {dataB.sqlmapCacheInfo?.sqlmapEnCurso && (
          <div className="mt-1 bg-[#ffd6d6] win98-border-deep px-2 py-1 text-[11px] text-[#800000] font-bold">
            ⚠ SQLMap no corrió en el análisis B: había otro análisis usándolo al mismo tiempo, así que se omitió por
            completo. Ningún hallazgo de SQLMap de B es real — relanzá ese análisis antes de confiar en esta comparación.
          </div>
        )}

        {!dataB.sqlmapCacheInfo?.sqlmapEnCurso && diff.cacheAmbiguousCount > 0 && (
          <div className="mt-1 bg-[#ffffc0] win98-border-deep px-2 py-1 text-[11px]">
            ⚠ {diff.cacheAmbiguousCount} hallazgo(s) de SQLMap no aparecen en B, pero su URL no fue re-testeada
            en este análisis (SQLMap la había marcado antes como no vulnerable y la omitió por caché). No asumas
            que están corregidos: mirá la pestaña "⚠ Sin confirmar" o relanzá el escaneo con "Limpiar caché" para confirmarlo.
          </div>
        )}
      </div>

      {/* Filtros tipo pestañas */}
      <div className="flex gap-1 flex-shrink-0">
        {[
          { id: "all", label: "Todo" },
          { id: "added", label: "+ Nuevas" },
          { id: "removed", label: "- Corregidas" },
          ...(diff.cacheAmbiguousCount > 0 ? [{ id: "cached", label: "⚠ Sin confirmar" }] : [])
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setFilter(tab.id as any)}
            className={`px-3 py-0.5 text-xs win98-border ${
              filter === tab.id ? "win98-border-inset bg-white" : "bg-[#c0c0c0]"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Listado de URLs/vulnerabilidades, mismo estilo que el reporte individual, con las diferencias marcadas */}
      <div className="flex-1 bg-white m-[2px] border-2 border-l-[#808080] border-t-[#808080] border-r-white border-b-white overflow-auto block text-xs">
        <table className="w-full text-left border-collapse whitespace-nowrap">
          <thead className="sticky top-0 bg-[#c0c0c0] z-10">
            <tr className="text-black">
              <th className="font-normal py-1 px-2 border-r border-[#808080] win98-border w-14 text-center">Estado</th>
              <th className="font-normal py-1 px-2 border-r border-[#808080] win98-border">Name</th>
              <th className="font-normal py-1 px-2 border-r border-[#808080] win98-border">Severity</th>
              <th className="font-normal py-1 px-2 border-r border-[#808080] win98-border">Type</th>
              <th className="font-normal py-1 px-2 win98-border">Location</th>
            </tr>
          </thead>
          <tbody>
            {visibleLines.map((line) => {
              const isAdded = line.status === "added";
              const isCached = !!line.cacheAmbiguous;
              const isRemoved = line.status === "removed" && !isCached;
              const rowBg = isCached
                ? "bg-[#ffffc0] text-[#806000]"
                : isAdded
                ? "bg-[#d6ffd6] text-[#004d00]"
                : isRemoved
                ? "bg-[#ffd6d6] text-[#800000]"
                : "bg-white text-gray-700";
              const badge = isCached ? "⚠" : isAdded ? "+" : isRemoved ? "-" : "=";
              const badgeTitle = isCached
                ? "Sin confirmar: no se volvió a testear por caché"
                : isAdded
                ? "Nueva en B"
                : isRemoved
                ? "Corregida (ya no aparece en B)"
                : "Sin cambios entre A y B";

              return (
                <tr key={line.key} className={`${rowBg} hover:bg-[#000080] hover:text-white`}>
                  <td className="py-1 px-2 border-r border-dotted border-gray-300 text-center font-bold" title={badgeTitle}>
                    {badge}
                  </td>
                  <td className="py-1 px-2 border-r border-dotted border-gray-300">
                    <div className="flex items-center gap-1 overflow-hidden text-ellipsis max-w-[220px]">
                      <img src="https://win98icons.alexmeub.com/icons/png/msg_warning-0.png" className="w-4 h-4 flex-shrink-0" alt="icon" />
                      <span>
                        {line.vuln.name}
                        {line.count > 1 ? ` (x${line.count})` : ""}
                      </span>
                    </div>
                  </td>
                  <td className="py-1 px-2 border-r border-dotted border-gray-300">{line.vuln.severity}</td>
                  <td className="py-1 px-2 border-r border-dotted border-gray-300 truncate max-w-[140px]">{line.vuln.type}</td>
                  <td className="py-1 px-2 font-bold truncate max-w-[260px]" title={line.vuln.location}>
                    {line.vuln.location}
                    {isCached && <span className="ml-1 font-normal italic whitespace-normal">(no re-testeada en B — caché)</span>}
                  </td>
                </tr>
              );
            })}
            {visibleLines.length === 0 && (
              <tr>
                <td colSpan={5} className="py-4 text-center text-gray-500 hover:bg-transparent hover:text-gray-500">
                  No hay diferencias que mostrar para este filtro.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Diff de tablas de base de datos volcadas por SQLMap */}
      {diff.tableLines.length > 0 && (
        <div className="win98-border-deep bg-white flex-shrink-0 max-h-40 overflow-auto font-mono text-[11px] leading-tight">
          <div className="bg-[#000080] text-white px-2 py-1 sticky top-0 font-sans font-bold">
            Tablas de Base de Datos (SQLMap --dump)
          </div>
          {diff.tableLines.map((tl) => {
            const prefix = tl.status === "added" ? "+" : tl.status === "removed" ? "-" : " ";
            const bg =
              tl.status === "added"
                ? "bg-[#d6ffd6] text-[#004d00]"
                : tl.status === "removed"
                ? "bg-[#ffd6d6] text-[#800000]"
                : "bg-white text-gray-700";
            const deltaLabel =
              tl.status === "context"
                ? tl.rowsDelta === 0
                  ? "(sin cambios en filas)"
                  : `(${tl.rowsDelta > 0 ? "+" : ""}${tl.rowsDelta} fila(s))`
                : "";
            return (
              <div key={tl.key} className={`px-2 py-[1px] whitespace-nowrap ${bg}`}>
                <span className="select-none mr-2 font-bold">{prefix}</span>
                <span>
                  [<span className="font-bold underline decoration-dotted">{tl.table.database}.{tl.table.table}</span>]{" "}
                  {tl.table.columns.length} columna(s), {tl.rowCount} fila(s) {deltaLabel}
                </span>
              </div>
            );
          })}
        </div>
      )}

      {/* Info de caché de SQLMap del análisis B: qué URLs no se volvieron a testear */}
      {dataB.sqlmapCacheInfo && dataB.sqlmapCacheInfo.omitidasPorCache.length > 0 && (
        <div className="win98-border-deep bg-white flex-shrink-0 max-h-32 overflow-auto font-mono text-[11px] leading-tight">
          <div className="bg-[#806000] text-white px-2 py-1 sticky top-0 font-sans font-bold">
            ⚠ URLs omitidas por caché en B ({dataB.sqlmapCacheInfo.omitidasPorCache.length} de {dataB.sqlmapCacheInfo.totalCandidatas} candidatas — no se re-testearon con SQLMap)
          </div>
          {dataB.sqlmapCacheInfo.omitidasPorCache.map((url: string) => (
            <div key={url} className="px-2 py-[1px] whitespace-nowrap bg-[#ffffc0] text-[#806000]">
              <span className="select-none mr-2 font-bold">?</span>
              <span className="font-bold underline decoration-dotted">{url}</span>
            </div>
          ))}
        </div>
      )}

      {/* Tabla resumen de severidades, estilo diffstat */}
      <div className="win98-border bg-[#c0c0c0] p-2 flex-shrink-0 text-xs">
        <p className="font-bold mb-1">Resumen de severidad (A → B)</p>
        <div className="grid grid-cols-4 gap-2">
          {severityRows.map((row) => (
            <div key={row.name} className="bg-white win98-border-deep px-2 py-1 flex flex-col items-center">
              <span className="text-gray-600">{row.name}</span>
              <span>
                {row.a} → {row.b}{" "}
                <span
                  className={
                    row.delta > 0
                      ? "text-[#800000] font-bold"
                      : row.delta < 0
                      ? "text-[#006400] font-bold"
                      : "text-gray-500"
                  }
                >
                  ({row.delta > 0 ? "+" : ""}{row.delta})
                </span>
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
