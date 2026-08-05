import React, { useState, useMemo } from "react";
import { useScanReport } from "../../../hooks/useScanReport";
import type { Domain } from "../../../services/api";
import { useWindows } from "../context/WindowsContext";
import { Win98VulnerabilityDetails } from "./Win98VulnerabilityDetails";
import { Win98CacheBadge } from "./Win98CacheBadge";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

export function Win98ScanReport({ domain, windowId }: { domain: Domain; windowId: string }) {
  const { loading, data } = useScanReport(domain);
  const [activeTab, setActiveTab] = useState("general");
  const { openWindow, closeWindow } = useWindows();

  const [filterSeverity, setFilterSeverity] = useState("all");
  const [filterType, setFilterType] = useState("all");

  const filteredVulnerabilities = useMemo(() => {
    if (!data?.allVulnerabilities) return [];
    return data.allVulnerabilities.filter((v: any) => {
      if (filterSeverity !== "all" && v.severity.toLowerCase() !== filterSeverity) return false;
      if (filterType !== "all" && v.type !== filterType) return false;
      return true;
    });
  }, [data?.allVulnerabilities, filterSeverity, filterType]);

  const handleDoubleClick = (vuln: any) => {
    const wId = `vuln-${vuln.id || Math.random()}`;
    openWindow({
      id: wId,
      title: `Vulnerability Properties - ${vuln.name}`,
      icon: "https://win98icons.alexmeub.com/icons/png/msg_warning-0.png",
      component: <Win98VulnerabilityDetails vuln={vuln} targetUrl={domain.target} windowId={wId} />
    });
  };

  if (loading) {
    return (
      <div className="bg-[#c0c0c0] h-full p-4 font-win98 text-black flex items-center justify-center">
        Analizando propiedades del sistema de {domain.target}...
      </div>
    );
  }

  if (!data) {
    return (
      <div className="bg-[#c0c0c0] h-full p-4 font-win98 text-black flex items-center justify-center">
        Error al cargar los datos del reporte.
      </div>
    );
  }

  const GRADE = data.score >= 85 ? "A" : data.score >= 65 ? "B" : data.score >= 45 ? "C" : "D";

  const renderTabs = () => {
    const tabs = [
      { id: "general", label: "General" },
      { id: "vulnerabilities", label: "Device Manager" },
      { id: "performance", label: "Performance" },
      { id: "tools", label: "Hardware Profiles" },
      { id: "database", label: "ODBC Data Sources" }
    ];

    return (
      <div className="flex z-10 relative">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-3 py-1 font-win98 text-xs border ${
                isActive
                  ? "bg-[#c0c0c0] border-t-white border-l-white border-b-[#c0c0c0] border-r-gray-500 shadow-[1px_1px_0_black,-1px_-1px_0_transparent_inset] translate-y-[2px] z-20 pb-2"
                  : "bg-[#c0c0c0] border-t-white border-l-white border-b-gray-500 border-r-gray-500 shadow-[1px_1px_0_black,-1px_-1px_0_transparent_inset] translate-y-[4px] z-0"
              } -mr-[2px] first:ml-0`}
            >
              {tab.label}
            </button>
          );
        })}
      </div>
    );
  };

  return (
    <div className="bg-[#c0c0c0] h-full font-win98 text-black p-3 select-none flex flex-col">
      {renderTabs()}
      
      {/* Contenedor Principal de la Pestaña */}
      <div className="flex-1 border-t-white border-l-white border-b-gray-500 border-r-gray-500 border bg-[#c0c0c0] p-4 shadow-[1px_1px_0_black,-1px_-1px_0_transparent_inset] z-10 flex flex-col overflow-hidden">
        
        {activeTab === "general" && (
          <div className="flex gap-6 h-full overflow-auto">
            <div className="w-32 h-32 flex-shrink-0 flex items-start justify-center">
              <img 
                src="https://win98icons.alexmeub.com/icons/png/computer_explorer-4.png" 
                alt="System" 
                className="w-16 h-16"
              />
            </div>
            <div className="flex-1 flex flex-col gap-4 text-xs">
              <div>
                <p>System:</p>
                <div className="ml-4">
                  <p>Security Analysis Report</p>
                  <p>Target: {domain.target}</p>
                </div>
              </div>

              <div className="w-full h-[1px] border-t border-gray-500 border-b border-white my-1"></div>

              <Win98CacheBadge sqlmapCacheInfo={data.sqlmapCacheInfo} ffufCacheInfo={data.ffufCacheInfo} />

              <div className="w-full h-[1px] border-t border-gray-500 border-b border-white my-1"></div>

              <div>
                <p className="font-bold">Estadísticas Generales:</p>
                <div className="ml-4 win98-border-deep bg-white p-2 mt-1 w-72">
                  <div className="flex justify-between py-0.5">
                    <span>Total de URLs únicas analizadas:</span>
                    <span className="font-bold">{data.generalStats.totalUrlsUnicas}</span>
                  </div>
                  <div className="flex justify-between py-0.5">
                    <span>URLs descubiertas por Spider:</span>
                    <span className="font-bold">{data.generalStats.urlsSpider}</span>
                  </div>
                  <div className="flex justify-between py-0.5">
                    <span>Alertas identificadas por ZAP:</span>
                    <span className="font-bold">{data.generalStats.alertasZap}</span>
                  </div>
                  <div className="flex justify-between py-0.5">
                    <span>Rutas descubiertas por FFUF:</span>
                    <span className="font-bold">{data.generalStats.rutasFfuf}</span>
                  </div>
                  <div className="flex justify-between py-0.5">
                    <span>Vulnerabilidades detectadas por SQLMap:</span>
                    <span className="font-bold">{data.generalStats.vulnerabilidadesSqlmap}</span>
                  </div>
                </div>
              </div>

              <div className="w-full h-[1px] border-t border-gray-500 border-b border-white my-1"></div>

              <div>
                <p>Overall Score:</p>
                <div className="ml-4">
                  <p className="text-sm font-bold">{data.score}/100 (Risk: {GRADE})</p>
                </div>
              </div>

              <div className="w-full h-[1px] border-t border-gray-500 border-b border-white my-1"></div>

              <div>
                <p>Vulnerabilities Found:</p>
                <div className="ml-4 grid grid-cols-2 gap-2 mt-2 w-64">
                  {data.severityData.map((item: any) => (
                    <div key={item.name} className="flex justify-between">
                      <span>{item.name}:</span>
                      <span style={{ color: item.color }} className="font-bold">{item.count}</span>
                    </div>
                  ))}
                  <div className="col-span-2 flex justify-between mt-2 pt-2 border-t border-[#808080] border-b border-b-white">
                    <span>Total:</span>
                    <span className="font-bold">{data.total}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === "vulnerabilities" && (
          <div className="flex flex-col h-full overflow-hidden">
            <div className="flex gap-4 mb-2">
              <div className="flex items-center gap-2 text-xs">
                <label>Severity:</label>
                <select 
                  className="win98-select" 
                  value={filterSeverity} 
                  onChange={(e) => setFilterSeverity(e.target.value)}
                >
                  <option value="all">All</option>
                  <option value="critical">Critical</option>
                  <option value="high">High</option>
                  <option value="medium">Medium</option>
                  <option value="low">Low</option>
                </select>
              </div>
              <div className="flex items-center gap-2 text-xs">
                <label>Type:</label>
                <select 
                  className="win98-select w-40" 
                  value={filterType} 
                  onChange={(e) => setFilterType(e.target.value)}
                >
                  <option value="all">All Types</option>
                  {Array.from(new Set((data?.allVulnerabilities || []).map((v: any) => v.type))).map((type: any) => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>
            </div>
            
            <div className="flex-1 bg-white m-[2px] border-2 border-l-[#808080] border-t-[#808080] border-r-white border-b-white overflow-auto block text-xs">
              <table className="w-full text-left border-collapse whitespace-nowrap">
                <thead className="sticky top-0 bg-[#c0c0c0] z-10">
                  <tr className="text-black">
                    <th className="font-normal py-1 px-2 border-r border-[#808080] win98-border">Name</th>
                    <th className="font-normal py-1 px-2 border-r border-[#808080] win98-border">Severity</th>
                    <th className="font-normal py-1 px-2 border-r border-[#808080] win98-border">Type</th>
                    <th className="font-normal py-1 px-2 win98-border">Location</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredVulnerabilities.map((vuln: any, idx: number) => (
                    <tr 
                      key={vuln.id || idx} 
                      onDoubleClick={() => handleDoubleClick(vuln)}
                      className="hover:bg-[#000080] hover:text-white cursor-pointer"
                    >
                      <td className="py-1 px-2 border-r border-dotted border-gray-300">
                        <div className="flex items-center gap-1 overflow-hidden text-ellipsis max-w-[200px]">
                          <img src="https://win98icons.alexmeub.com/icons/png/msg_warning-0.png" className="w-4 h-4" alt="icon"/>
                          {vuln.name}
                        </div>
                      </td>
                      <td className="py-1 px-2 border-r border-dotted border-gray-300">{vuln.severity}</td>
                      <td className="py-1 px-2 border-r border-dotted border-gray-300 truncate max-w-[150px]">{vuln.type}</td>
                      <td className="py-1 px-2 truncate max-w-[200px]">{vuln.location}</td>
                    </tr>
                  ))}
                  {filteredVulnerabilities.length === 0 && (
                    <tr>
                      <td colSpan={4} className="py-4 text-center text-gray-500">No vulnerabilities match the filters.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
            <p className="text-[10px] text-gray-600 mt-1">Double-click a vulnerability to view details and AI suggestions.</p>
          </div>
        )}

        {activeTab === "performance" && (
          <div className="flex flex-col h-full overflow-hidden">
            <p className="text-xs mb-2 font-bold">Security Performance and Analytics</p>
            <div className="flex-1 flex gap-4 overflow-auto pb-4">
              
              <div className="flex-1 win98-border-deep bg-white p-2 flex flex-col min-h-[250px]">
                <p className="text-xs font-bold text-center mb-2">Vulnerabilities by Type</p>
                <div className="flex-1">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data?.typesData || []} layout="vertical" margin={{ left: 20, right: 10 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#c0c0c0" horizontal={false} />
                      <XAxis type="number" tick={{fontSize: 10}} />
                      <YAxis type="category" dataKey="name" width={100} tick={{fontSize: 10}} />
                      <Tooltip contentStyle={{backgroundColor: "#ffffe1", border: "1px solid black", fontSize: "10px", borderRadius: 0}} />
                      <Bar dataKey="value" fill="#000080" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="flex-1 win98-border-deep bg-white p-2 flex flex-col min-h-[250px]">
                <p className="text-xs font-bold text-center mb-2">Top Vulnerable Endpoints</p>
                <div className="flex-1">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data?.scanMetrics?.topVulnerableUrls || []} margin={{ left: -10, right: 10, bottom: 20 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#c0c0c0" vertical={false} />
                      <XAxis dataKey="url" tick={{fontSize: 9}} angle={-45} textAnchor="end" height={60} />
                      <YAxis type="number" tick={{fontSize: 10}} />
                      <Tooltip contentStyle={{backgroundColor: "#ffffe1", border: "1px solid black", fontSize: "10px", borderRadius: 0}} />
                      <Bar dataKey="count" fill="#800000" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

            </div>
          </div>
        )}

        {activeTab === "tools" && (
          <div className="flex flex-col h-full overflow-hidden">
            <p className="text-xs mb-2 font-bold">Hardware and Analysis Tools Profiles</p>
            <div className="win98-border-deep bg-white w-full flex flex-col p-4 text-xs gap-4 overflow-auto">
              <div>
                <p className="font-bold border-b border-gray-400 mb-2">Scanners Executed</p>
                <div className="flex gap-4">
                  <div className="flex items-center gap-2">
                    <img src="https://win98icons.alexmeub.com/icons/png/gears-0.png" alt="tool" className="w-6 h-6"/>
                    <span>{data.scanMetrics?.scanners || "OWASP ZAP, SQLMap"}</span>
                  </div>
                </div>
              </div>

              <div>
                <p className="font-bold border-b border-gray-400 mb-2">Threat Nature</p>
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-[#c0c0c0] p-2 win98-border">
                    <p>Injection Flaws:</p>
                    <p className="text-lg font-bold text-[#800000]">{data.scanMetrics?.threatNature?.injection || 0}</p>
                  </div>
                  <div className="bg-[#c0c0c0] p-2 win98-border">
                    <p>Configuration Flaws:</p>
                    <p className="text-lg font-bold text-[#000080]">{data.scanMetrics?.threatNature?.configuration || 0}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === "database" && (
          <div className="flex flex-col h-full overflow-hidden">
            <p className="text-xs mb-2 font-bold">Tablas de Base de Datos Volcadas (SQLMap --dump)</p>
            {(!data.sqlmapTables || data.sqlmapTables.length === 0) ? (
              <div className="flex-1 flex flex-col items-center justify-center text-xs text-gray-500 win98-border-deep bg-white text-center px-6">
                <img
                  src="https://win98icons.alexmeub.com/icons/png/directory_open_file_cabinet-2.png"
                  alt="Sin datos"
                  className="w-8 h-8 mb-2 opacity-50 grayscale"
                />
                {data.sqlmapLevel === "basic" ? (
                  <>
                    <span className="font-bold">No hay tablas: el análisis usó el modo BÁSICO de SQLMap.</span>
                    <span className="mt-1">Este modo solo detecta SI un parámetro es inyectable, no extrae nombres ni contenido de bases de datos. Es esperable que no aparezca nada acá.</span>
                  </>
                ) : data.sqlmapLevel === "fast_evidence" ? (
                  <>
                    <span className="font-bold">No hay tablas completas: el análisis usó el modo INTERMEDIO de SQLMap.</span>
                    <span className="mt-1">Este modo solo trae nombres de bases de datos/tablas/usuario (evidencia rápida), no vuelca el contenido de las tablas. Para ver filas y columnas hace falta correr el modo de extracción completa (--dump).</span>
                  </>
                ) : data.sqlmapLevel === "full_dump" ? (
                  <>
                    <span className="font-bold">No se extrajeron tablas en este análisis.</span>
                    <span className="mt-1">Se usó el modo de EXTRACCIÓN COMPLETA (--dump), así que si no aparece nada acá es porque SQLMap no encontró inyecciones explotables para volcar datos, no por una limitación del modo.</span>
                  </>
                ) : (
                  <span>No se extrajeron tablas de bases de datos en este análisis.</span>
                )}
              </div>
            ) : (
              <div className="flex-1 flex flex-col gap-4 overflow-auto pr-1">
                {data.sqlmapTables.map((t: any) => (
                  <div key={`${t.database}.${t.table}`} className="win98-border-deep bg-white flex flex-col">
                    <div className="bg-[#000080] text-white text-xs font-bold px-2 py-1 flex items-center gap-2">
                      <img src="https://win98icons.alexmeub.com/icons/png/briefcase-2.png" className="w-4 h-4" alt="db" />
                      <span>{t.database}.{t.table}</span>
                      <span className="ml-auto font-normal">{t.rows.length} fila(s) · {t.columns.length} columna(s)</span>
                    </div>
                    <div className="overflow-auto max-h-56">
                      <table className="w-full text-[10px] text-left border-collapse whitespace-nowrap">
                        <thead className="sticky top-0 bg-[#c0c0c0]">
                          <tr>
                            {t.columns.map((c: string) => (
                              <th key={c} className="font-bold px-2 py-1 border-r border-b border-[#808080]">{c}</th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {t.rows.map((row: string[], rIdx: number) => (
                            <tr key={rIdx} className="hover:bg-[#000080] hover:text-white">
                              {row.map((cell, cIdx) => (
                                <td key={cIdx} className="px-2 py-0.5 border-r border-dotted border-gray-300">{cell}</td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

      </div>

      <div className="flex justify-end gap-2 mt-4 flex-shrink-0">
        <button onClick={() => closeWindow(windowId)} className="px-6 py-1 win98-border active:win98-border-inset text-xs bg-[#c0c0c0]">Volver</button>
      </div>
    </div>
  );
}
