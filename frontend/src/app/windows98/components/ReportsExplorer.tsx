import React from "react";
import { useScan } from "../context/ScanContext";
import { useWindows } from "../context/WindowsContext";
import { ScanReport } from "../../components/ScanReport";
import type { Domain } from "../../../services/api";

export function ReportsExplorer() {
  const { domains, deleteDomain } = useScan();
  const { openWindow } = useWindows();

  // Filtrar solo los que están completados
  const completedScans = domains.filter(d => d.status === "completed" || d.status === "error");

  const handleOpenReport = (domain: Domain) => {
    openWindow({
      id: `report-${domain.scanId}`,
      title: `Reporte - ${domain.target.replace(/^https?:\/\//, "")}`,
      icon: "https://win98icons.alexmeub.com/icons/png/notepad-1.png",
      component: <ScanReport domain={domain} />
    });
  };

  const handleDelete = async (e: React.MouseEvent, domain: Domain) => {
    e.stopPropagation();
    if (window.confirm(`¿Estás seguro de que quieres eliminar el reporte de ${domain.target}?`)) {
      await deleteDomain(domain);
    }
  };

  return (
    <div className="bg-[#c0c0c0] h-full flex flex-col font-win98 text-black select-none">
      {/* Barra de Menú Estilo Win98 */}
      <div className="flex gap-4 px-2 py-[2px] border-b border-[#dfdfdf] text-xs">
        <span className="hover:bg-[#000080] hover:text-white px-1 cursor-pointer">Archivo</span>
        <span className="hover:bg-[#000080] hover:text-white px-1 cursor-pointer">Edición</span>
        <span className="hover:bg-[#000080] hover:text-white px-1 cursor-pointer">Ver</span>
        <span className="hover:bg-[#000080] hover:text-white px-1 cursor-pointer">Favoritos</span>
        <span className="hover:bg-[#000080] hover:text-white px-1 cursor-pointer">Ayuda</span>
      </div>

      {/* Barra de Herramientas Estilo Explorer */}
      <div className="flex items-center gap-2 p-[4px] border-b border-[#808080] text-xs bg-[#c0c0c0]">
        <button className="flex items-center gap-1 px-1.5 py-0.5 win98-border active:win98-border-inset">
          <img src="https://win98icons.alexmeub.com/icons/png/arrow_left-0.png" alt="Atrás" className="w-4 h-4" />
          <span>Atrás</span>
        </button>
        <button className="flex items-center gap-1 px-1.5 py-0.5 win98-border active:win98-border-inset">
          <img src="https://win98icons.alexmeub.com/icons/png/arrow_right-0.png" alt="Adelante" className="w-4 h-4" />
          <span>Adelante</span>
        </button>
        <button className="flex items-center gap-1 px-1.5 py-0.5 win98-border active:win98-border-inset">
          <img src="https://win98icons.alexmeub.com/icons/png/arrow_up-0.png" alt="Subir" className="w-4 h-4" />
        </button>
        <div className="w-[1px] h-5 bg-[#808080] mx-1"></div>
        <button className="flex items-center gap-1 px-1.5 py-0.5 win98-border active:win98-border-inset">
          <img src="https://win98icons.alexmeub.com/icons/png/search_file-0.png" alt="Buscar" className="w-4 h-4" />
          <span>Buscar</span>
        </button>
        <button className="flex items-center gap-1 px-1.5 py-0.5 win98-border active:win98-border-inset">
          <img src="https://win98icons.alexmeub.com/icons/png/directory_open-0.png" alt="Carpetas" className="w-4 h-4" />
          <span>Carpetas</span>
        </button>
      </div>

      {/* Barra de Dirección (Address Bar) */}
      <div className="flex items-center gap-2 p-1 border-b border-[#808080] text-xs">
        <span className="text-gray-600">Dirección</span>
        <div className="flex-1 bg-white px-2 py-0.5 border border-gray-400 win98-border-inset text-xs select-text">
          C:\Mis Documentos\Reportes de Seguridad
        </div>
      </div>

      {/* Contenedor Principal (Explorador de Carpetas + Archivos) */}
      <div className="flex-1 flex bg-white m-[2px] win98-border-deep overflow-hidden">
        {/* Panel Izquierdo (Info/Detalle Estilo Windows 98) */}
        <div className="w-[180px] bg-[#c0c0c0] p-4 border-r border-[#808080] flex flex-col justify-between select-none">
          <div>
            <h4 className="text-sm font-bold leading-tight">Reportes de Seguridad</h4>
            <div className="w-full h-[2px] bg-[#808080] my-2"></div>
            <p className="text-[10px] text-gray-700 leading-normal">
              Haga doble clic en un archivo de reporte para abrir la evaluación de vulnerabilidades y ver detalles con la IA.
            </p>
          </div>
          
          <div className="text-[10px] text-gray-600">
            <div>Total: {completedScans.length} reportes</div>
            <div>Carpeta local</div>
          </div>
        </div>

        {/* Panel Derecho (Lista de Archivos de Reportes) */}
        <div className="flex-1 p-4 overflow-y-auto bg-white flex flex-wrap content-start gap-6 select-none">
          {completedScans.map((scan) => {
            const isError = scan.status === "error";
            const scoreLabel = scan.score !== null ? `[Score ${scan.score}]` : "[Error]";
            const fileName = `Reporte_${scan.target.replace(/^https?:\/\//, "")}_${scan.id.slice(0, 5)}.doc`;
            const fileIcon = isError 
              ? "https://win98icons.alexmeub.com/icons/png/msg_error-0.png"
              : "https://win98icons.alexmeub.com/icons/png/notepad-1.png";

            return (
              <div 
                key={scan.id}
                onDoubleClick={() => !isError && handleOpenReport(scan)}
                className="w-[100px] flex flex-col items-center cursor-pointer hover:bg-[#000080]/10 p-1 group border border-transparent hover:border-dotted hover:border-[#808080] rounded"
                title={`${fileName} - Haga doble clic para abrir`}
              >
                <div className="relative">
                  <img 
                    src={fileIcon} 
                    alt="Archivo" 
                    className="w-10 h-10 mb-1 pointer-events-none group-hover:brightness-95"
                  />
                  {scan.score !== null && (
                    <span 
                      className="absolute bottom-1 right-0 text-[9px] font-bold text-white px-0.5 rounded shadow-sm"
                      style={{
                        background: scan.score >= 85 ? "#10b981" : scan.score >= 65 ? "#ea580c" : "#dc2626"
                      }}
                    >
                      {scan.score}
                    </span>
                  )}
                </div>
                <span className="text-[11px] text-center leading-tight break-all text-black px-1">
                  {fileName}
                </span>
                
                {/* Botón de Borrar discreto */}
                <button
                  onClick={(e) => handleDelete(e, scan)}
                  className="mt-1 opacity-0 group-hover:opacity-100 bg-[#dfdfdf] border border-gray-400 px-1 py-0.5 text-[9px] hover:bg-red-100 hover:text-red-700"
                  title="Eliminar este reporte"
                >
                  Eliminar
                </button>
              </div>
            );
          })}

          {completedScans.length === 0 && (
            <div className="flex-1 flex flex-col justify-center items-center text-gray-500 h-full">
              <img src="https://win98icons.alexmeub.com/icons/png/directory_open_file_cabinet-2.png" alt="Vacío" className="w-12 h-12 mb-2 opacity-50" />
              <span className="text-xs">No hay reportes disponibles.</span>
              <span className="text-[10px] text-gray-400 mt-1">Realice un escaneo desde el Analizador para generar uno.</span>
            </div>
          )}
        </div>
      </div>

      {/* Barra de Estado (Status Bar) */}
      <div className="bg-[#c0c0c0] border-t border-[#dfdfdf] px-2 py-[2px] flex justify-between text-[11px] text-gray-700 select-none">
        <span>{completedScans.length} Objeto(s)</span>
        <span>Mi PC</span>
      </div>
    </div>
  );
}
