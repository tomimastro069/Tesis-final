import React from "react";
import { useScan } from "../context/ScanContext";
import { useWindows } from "../context/WindowsContext";
import { Win98ScanReport } from "./Win98ScanReport";
import type { Domain } from "../../../services/api";

export function ReportsExplorer() {
  const { domains, deleteDomain } = useScan();
  const { openWindow } = useWindows();

  // Filtrar solo los que están completados o error
  const completedScans = domains.filter(d => d.status === "completed" || d.status === "error");

  const handleOpenReport = (domain: Domain) => {
    openWindow({
      id: `report-${domain.scanId}`,
      title: `System Properties - ${domain.target.replace(/^https?:\/\//, "")}`,
      icon: "https://win98icons.alexmeub.com/icons/png/computer_explorer-4.png",
      component: <Win98ScanReport domain={domain} />
    });
  };

  return (
    <div className="bg-[#c0c0c0] h-full flex flex-col font-win98 text-black select-none">
      {/* Barra de Menú Estilo Win98 */}
      <div className="flex gap-4 px-2 py-[2px] border-b border-[#dfdfdf] text-xs">
        <span className="hover:bg-[#000080] hover:text-white px-1 cursor-pointer">Archivo</span>
        <span className="hover:bg-[#000080] hover:text-white px-1 cursor-pointer">Edición</span>
        <span className="hover:bg-[#000080] hover:text-white px-1 cursor-pointer">Ver</span>
        <span className="hover:bg-[#000080] hover:text-white px-1 cursor-pointer">Favoritos</span>
        <span className="hover:bg-[#000080] hover:text-white px-1 cursor-pointer">Herramientas</span>
        <span className="hover:bg-[#000080] hover:text-white px-1 cursor-pointer">Ayuda</span>
      </div>

      {/* Barra de Herramientas eliminada a petición */}

      {/* Barra de Dirección (Address Bar) */}
      <div className="flex items-center gap-2 p-1 border-b border-[#808080] text-xs">
        <span className="text-black ml-1">Dirección</span>
        <div className="flex flex-1 items-center bg-white border-2 border-l-[#808080] border-t-[#808080] border-r-white border-b-white text-xs select-text">
          <img src="https://win98icons.alexmeub.com/icons/png/briefcase-2.png" className="w-4 h-4 ml-1 mr-1" alt="Icon" />
          <span className="flex-1 py-0.5">Reportes de Seguridad</span>
          <div className="bg-[#dfdfdf] win98-border px-2 py-0.5 cursor-pointer">▼</div>
        </div>
      </div>

      {/* Contenedor Principal (Lista de Detalles) */}
      <div className="flex-1 bg-white m-[2px] border-2 border-l-[#808080] border-t-[#808080] border-r-white border-b-white overflow-auto block">
        <table className="w-full text-xs text-left whitespace-nowrap border-collapse">
          <thead className="sticky top-0 bg-[#c0c0c0] z-10 shadow-[0_1px_0_#000]">
            <tr>
              <th className="font-normal px-2 py-0.5 win98-border active:win98-border-inset cursor-default w-[40%]">Nombre</th>
              <th className="font-normal px-2 py-0.5 win98-border active:win98-border-inset cursor-default w-[20%]">Fecha de escaneo</th>
              <th className="font-normal px-2 py-0.5 win98-border active:win98-border-inset cursor-default w-[15%]">Riesgo</th>
              <th className="font-normal px-2 py-0.5 win98-border active:win98-border-inset cursor-default w-[10%]">Puntos</th>
              <th className="font-normal px-2 py-0.5 win98-border active:win98-border-inset cursor-default w-[15%]">Tipo</th>
            </tr>
          </thead>
          <tbody>
            {completedScans.map((scan) => {
              const isError = scan.status === "error";
              const fileName = `Reporte_${scan.target.replace(/^https?:\/\//, "")}_${scan.id.slice(0, 5)}.doc`;
              const fileIcon = isError 
                ? "https://win98icons.alexmeub.com/icons/png/msg_error-0.png"
                : "https://win98icons.alexmeub.com/icons/png/notepad-1.png";

              // Formato de fecha con manejo de zona horaria
              const parseUTCDate = (dateStr: string | null) => {
                if (!dateStr) return "Desconocida";
                // Si la fecha no tiene indicador de zona horaria (Z o +00:00), asumimos que el backend generó UTC
                const hasTimezone = /Z|[+-]\d{2}:\d{2}$/.test(dateStr);
                const dateObj = new Date(hasTimezone ? dateStr : dateStr + "Z");
                return dateObj.toLocaleString();
              };
              const scanDate = parseUTCDate(scan.lastScan);
              
              // Nivel de riesgo localizado
              const riskTranslations: Record<string, string> = {
                high: "Alto", medium: "Medio", low: "Bajo", info: "Informativo"
              };
              const riskStr = scan.riskLevel ? (riskTranslations[scan.riskLevel] || scan.riskLevel) : (isError ? "Fallido" : "-");

              return (
                <tr 
                  key={scan.id} 
                  onDoubleClick={() => !isError && handleOpenReport(scan)}
                  className="hover:bg-[#000080] hover:text-white cursor-pointer group"
                >
                  <td className="px-1 py-0.5 border-r border-transparent flex items-center gap-2">
                    <img src={fileIcon} alt="Icon" className="w-4 h-4" />
                    <span>{fileName}</span>
                  </td>
                  <td className="px-2 py-0.5 border-r border-transparent">{scanDate}</td>
                  <td className="px-2 py-0.5 border-r border-transparent">{riskStr}</td>
                  <td className="px-2 py-0.5 border-r border-transparent">{scan.score !== null ? scan.score : "-"}</td>
                  <td className="px-2 py-0.5">{isError ? "Error de Escaneo" : "Documento de Auditoría"}</td>
                </tr>
              );
            })}
            
            {completedScans.length === 0 && (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center text-gray-500 hover:bg-transparent hover:text-gray-500">
                  <div className="flex flex-col items-center justify-center">
                    <img src="https://win98icons.alexmeub.com/icons/png/directory_open_file_cabinet-2.png" alt="Vacío" className="w-8 h-8 mb-2 opacity-50 grayscale" />
                    <span>0 archivos encontrados.</span>
                  </div>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Barra de Estado (Status Bar) */}
      <div className="bg-[#c0c0c0] border-t border-[#dfdfdf] px-2 py-[2px] flex justify-between text-[11px] text-gray-700 select-none shadow-[inset_0_1px_0_#fff]">
        <span>{completedScans.length} objeto(s)</span>
        <span>My Computer</span>
      </div>
    </div>
  );
}
