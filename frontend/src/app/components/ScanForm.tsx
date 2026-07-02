import React, { useState } from "react";
import { useScan } from "../windows98/context/ScanContext";
import type { ScanRequest } from "../../services/api";

export function ScanForm({ onScanStarted }: { onScanStarted: (scanId: string) => void }) {
  const { startScan, activeScan } = useScan();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<ScanRequest>({
    target: "http://dvwa",
    nivel: "medium",
    sqlmap_level: "basic",
    cookies: "",
    clean_cache: false
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (activeScan) {
      setError("Ya hay un análisis activo.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const scanId = await startScan(formData);
      onScanStarted(scanId);
    } catch (err: any) {
      setError(err.message || "Error al lanzar el análisis");
    } finally {
      setLoading(false);
    }
  };

  const isBlocked = activeScan !== null;

  return (
    <div className="bg-[#c0c0c0] p-4 h-full flex flex-col font-win98 text-black select-none">
      <div className="mb-4">
        <h3 className="text-sm font-bold mb-1">Configuración del Análisis</h3>
        <p className="text-[11px] text-gray-700">Configure los parámetros para el escaneo de seguridad contra el dominio objetivo.</p>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-3 py-2 text-[11px] mb-3 win98-border-inset">
          <strong>Error:</strong> {error}
        </div>
      )}

      {isBlocked ? (
        <div className="flex-1 flex flex-col justify-center items-center bg-[#c0c0c0] p-4 text-center">
          <img 
            src="https://win98icons.alexmeub.com/icons/png/clock-0.png" 
            alt="Reloj" 
            className="w-12 h-12 mb-4 animate-pulse"
          />
          <span className="font-bold text-xs">Análisis en progreso...</span>
          <span className="text-[11px] text-gray-700 mt-1">
            {activeScan.target} ({activeScan.progress ?? 0}%)
          </span>
          <div className="w-48 h-4 bg-white border border-gray-400 mt-2 win98-border-inset relative overflow-hidden">
            <div 
              className="h-full bg-[#000080]" 
              style={{ width: `${activeScan.progress ?? 0}%` }}
            />
          </div>
          <span className="text-[10px] text-gray-600 mt-2">{activeScan.progressMessage}</span>
          
          <p className="text-[10px] text-gray-500 max-w-[250px] mt-4">
            La aplicación de escaneo se encuentra bloqueada mientras se ejecuta el análisis actual. Puede ver los detalles en la terminal de MS-DOS Prompt.
          </p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="flex-1 flex flex-col gap-3">
          {/* Target */}
          <div>
            <label className="block text-xs font-bold mb-1">Dominio Objetivo (URL)</label>
            <input 
              type="url" 
              required 
              className="w-full bg-[#dfdfdf] px-2 py-1 text-xs border border-gray-400 cursor-not-allowed outline-none select-none win98-border-inset"
              value="http://dvwa"
              disabled
            />
          </div>

          {/* Cookies */}
          <div>
            <label className="block text-xs font-bold mb-1">Cookie de Sesión (Opcional)</label>
            <input 
              type="text" 
              placeholder="PHPSESSID=your_session; security=low" 
              className="w-full bg-white px-2 py-1 text-xs border border-gray-400 outline-none win98-border-inset"
              value={formData.cookies}
              onChange={(e) => setFormData({...formData, cookies: e.target.value})}
            />
          </div>

          {/* Clean Cache Checkbox */}
          <div className="flex items-center gap-2 mt-1">
            <input 
              type="checkbox" 
              id="cleanCache"
              checked={formData.clean_cache}
              onChange={(e) => setFormData({...formData, clean_cache: e.target.checked})}
              className="cursor-pointer"
            />
            <label htmlFor="cleanCache" className="text-xs cursor-pointer select-none">
              Limpiar la caché antes de empezar (fuerza re-escaneo)
            </label>
          </div>

          {/* Nivel y Nivel SQLMap */}
          <div className="grid grid-cols-2 gap-3 mt-1">
            <div>
              <label className="block text-xs font-bold mb-1">Nivel de Análisis</label>
              <select 
                value={formData.nivel} 
                onChange={(e) => setFormData({...formData, nivel: e.target.value})}
                className="w-full bg-white px-1 py-[2px] text-xs border border-gray-400 outline-none win98-border-inset"
              >
                <option value="small">Básico (Wordlist chica)</option>
                <option value="medium">Profundo (Wordlist mediana)</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-bold mb-1">Nivel SQLMap</label>
              <select 
                value={formData.sqlmap_level} 
                onChange={(e) => setFormData({...formData, sqlmap_level: e.target.value})}
                className="w-full bg-white px-1 py-[2px] text-xs border border-gray-400 outline-none win98-border-inset"
              >
                <option value="basic">1 - Básico (Recomendado)</option>
                <option value="fast_evidence">2 - Evidencia Rápida</option>
                <option value="full_dump">3 - Extracción Completa (Lento)</option>
              </select>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-end gap-3 mt-auto pt-4 border-t border-[#dfdfdf]">
            <button 
              type="submit" 
              disabled={loading}
              className="bg-[#c0c0c0] px-4 py-1 text-xs font-bold win98-border active:win98-border-inset outline-none cursor-pointer"
            >
              {loading ? 'Iniciando...' : 'Comenzar Análisis'}
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
