import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { fetchAllScans, fetchScanProgress, fetchScanResults, launchScan, deleteScan } from '../../../services/api';
import type { Domain, ScanRequest } from '../../../services/api';
import { parseSecurityResults } from '../../../utils/parser';

interface ScanContextType {
  domains: Domain[];
  activeScan: Domain | null;
  terminalLogs: string[];
  isLoading: boolean;
  loadDomains: () => Promise<void>;
  startScan: (params: ScanRequest) => Promise<string>;
  deleteDomain: (domain: Domain) => Promise<boolean>;
  cancelActiveScan: () => Promise<void>;
  clearTerminalLogs: () => void;
  addLogLine: (line: string) => void;
}

const ScanContext = createContext<ScanContextType | undefined>(undefined);

export function ScanProvider({ children }: { children: React.ReactNode }) {
  const [domains, setDomains] = useState<Domain[]>([]);
  const [activeScan, setActiveScan] = useState<Domain | null>(null);
  const [terminalLogs, setTerminalLogs] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const addLogLine = useCallback((line: string) => {
    const time = new Date().toLocaleTimeString();
    setTerminalLogs(prev => [...prev, `[${time}] ${line}`]);
  }, []);

  const loadDomains = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await fetchAllScans();
      const processed = data.map((d: Domain) => {
        if (d.status === 'completed' && d.rawResults) {
          const parsed = parseSecurityResults(d.rawResults);
          if (parsed) {
            return { ...d, score: parsed.score, riskLevel: parsed.riskLevel };
          }
        }
        return d;
      });
      setDomains(processed);

      // Si hay un escaneo en progreso en el backend, marcarlo como activo
      const scanning = processed.find((d: Domain) => d.status === 'scanning');
      if (scanning && !activeScan) {
        setActiveScan(scanning);
        setTerminalLogs([
          `C:\\> Remoto: Detectado escaneo activo en progreso para ${scanning.target}...`,
          `[${new Date().toLocaleTimeString()}] Retomando logs de ejecución...`
        ]);
      }
    } catch (error) {
      console.error("Error cargando dominios:", error);
    } finally {
      setIsLoading(false);
    }
  }, [activeScan]);

  useEffect(() => {
    loadDomains();
  }, []);

  // Polling para el escaneo activo
  useEffect(() => {
    let interval: number;

    if (activeScan && activeScan.scanId) {
      const scanId = activeScan.scanId;
      let lastMessage = "";

      interval = window.setInterval(async () => {
        try {
          // Obtener progreso
          const progressInfo = await fetchScanProgress(scanId);
          if (progressInfo) {
            const currentMsg = `${progressInfo.message} (${progressInfo.percentage}%)`;
            
            // Actualizar estado del escaneo activo
            setActiveScan((prev: Domain | null) => {
              if (prev && prev.scanId === scanId) {
                return { 
                  ...prev, 
                  progress: progressInfo.percentage, 
                  progressMessage: progressInfo.message 
                };
              }
              return prev;
            });

            // Si el mensaje cambió, agregarlo a los logs de la terminal
            if (progressInfo.message !== lastMessage) {
              lastMessage = progressInfo.message;
              addLogLine(currentMsg);
            }
          }

          // Consultar si ya completó o falló
          const results = await fetchScanResults(scanId);
          if (results) {
            if (results.status === 'completed') {
              addLogLine("Pipeline completado exitosamente.");
              addLogLine("Generando reportes...");
              
              const parsed = parseSecurityResults(results.results);
              const score = parsed?.score ?? null;
              const riskLevel = parsed?.riskLevel ?? null;

              // Actualizar dominios
              setDomains((prev: Domain[]) => 
                prev.map((pd: Domain) => 
                  pd.scanId === scanId 
                    ? { ...pd, status: 'completed' as const, score, riskLevel, rawResults: results.results } 
                    : pd
                )
              );

              addLogLine("C:\\> Escaneo completado. Archivos guardados.");
              setActiveScan(null); // Desbloquear
              clearInterval(interval);
              loadDomains(); // Recargar todo
            } else if (results.status === 'failed') {
              addLogLine("[-] ERROR: El pipeline falló en el backend.");
              setDomains((prev: Domain[]) => 
                prev.map((pd: Domain) => 
                  pd.scanId === scanId ? { ...pd, status: 'error' as const } : pd
                )
              );
              setActiveScan(null); // Desbloquear
              clearInterval(interval);
              loadDomains();
            }
          }
        } catch (error) {
          console.error("Error en polling de ScanContext:", error);
        }
      }, 3000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [activeScan, addLogLine, loadDomains]);

  const startScan = useCallback(async (params: ScanRequest) => {
    if (activeScan) {
      throw new Error("Ya hay un escaneo en progreso. Por favor espera a que termine.");
    }

    setTerminalLogs([
      "C:\\> orquestador-seguridad.exe --target http://dvwa",
      `[${new Date().toLocaleTimeString()}] Iniciando conexión con el orquestador...`,
      `[${new Date().toLocaleTimeString()}] Parámetros: Nivel=${params.nivel}, SQLMap=${params.sqlmap_level}`
    ]);

    try {
      const res = await launchScan(params);
      const newDomain: Domain = {
        id: Date.now().toString(),
        target: params.target,
        scanId: res.scan_id,
        lastScan: new Date().toISOString(),
        score: null,
        riskLevel: null,
        status: "scanning"
      };

      // Agregar a la lista local
      setDomains((prev: Domain[]) => [newDomain, ...prev]);
      // Setear como escaneo activo
      setActiveScan(newDomain);
      
      addLogLine(`Escaneo lanzado con ID: ${res.scan_id}`);
      return res.scan_id;
    } catch (err: any) {
      addLogLine(`[-] ERROR al lanzar escaneo: ${err.message || 'Error desconocido'}`);
      throw err;
    }
  }, [activeScan, addLogLine]);

  const deleteDomain = useCallback(async (domain: Domain) => {
    if (!domain.scanId) {
      setDomains((prev: Domain[]) => prev.filter((d: Domain) => d.id !== domain.id));
      return true;
    }

    try {
      await deleteScan(domain.scanId);
      setDomains((prev: Domain[]) => prev.filter((d: Domain) => d.id !== domain.id));
      return true;
    } catch (err) {
      console.error("Error al borrar dominio:", err);
      return false;
    }
  }, []);

  // Cancela/descarta el escaneo activo desde el frontend. Útil cuando el backend se
  // reinició o se colgó mientras un escaneo estaba en curso: el registro queda con
  // status 'scanning' en la base de datos para siempre y bloquea nuevos escaneos
  // ("Ya hay un escaneo en progreso"). Esto lo saca de la lista activa para desbloquear
  // la app, aunque el proceso de SQLMap en el servidor pueda seguir corriendo solo.
  const cancelActiveScan = useCallback(async () => {
    if (!activeScan) return;

    addLogLine("C:\\> Cancelando análisis por el usuario...");

    try {
      if (activeScan.scanId) {
        await deleteScan(activeScan.scanId);
      }
    } catch (err) {
      console.error("Error al cancelar el escaneo activo:", err);
      addLogLine("[-] No se pudo notificar la cancelación al backend, se descarta igual localmente.");
    } finally {
      setDomains((prev: Domain[]) => prev.filter((d: Domain) => d.scanId !== activeScan.scanId));
      setActiveScan(null);
      addLogLine("C:\\> Análisis cancelado. Ya podés iniciar uno nuevo.");
    }
  }, [activeScan, addLogLine]);

  const clearTerminalLogs = useCallback(() => {
    setTerminalLogs([]);
  }, []);

  return (
    <ScanContext.Provider value={{
      domains,
      activeScan,
      terminalLogs,
      isLoading,
      loadDomains,
      startScan,
      deleteDomain,
      cancelActiveScan,
      clearTerminalLogs,
      addLogLine
    }}>
      {children}
    </ScanContext.Provider>
  );
}

export function useScan() {
  const context = useContext(ScanContext);
  if (!context) {
    throw new Error('useScan must be used within a ScanProvider');
  }
  return context;
}
