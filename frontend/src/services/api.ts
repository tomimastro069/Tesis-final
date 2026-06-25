export interface ScanRequest {
  target: string;
  nivel: string;
  cookies?: string;
  clean_cache?: boolean;
  sqlmap_level?: string;
  callback_url?: string;
}

export interface Domain {
  id: string;
  target: string;
  scanId?: string;
  lastScan: string | null;
  score: number | null;
  riskLevel: string | null;
  status: 'idle' | 'scanning' | 'completed' | 'error';
  progress?: number;
  progressMessage?: string;
  rawResults?: any;
}

const API_URL = 'http://localhost:8000';

export async function launchScan(params: ScanRequest) {
  const response = await fetch(`${API_URL}/scan`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      ...params,
      callback_url: "http://security-n8n:5678/webhook/scan-completado"
    }),
  });

  if (!response.ok) {
    throw new Error('Error al lanzar escaneo');
  }
  return response.json();
}

export async function fetchScanResults(scanId: string) {
  try {
    const response = await fetch(`${API_URL}/scan/${scanId}`);
    if (!response.ok) {
      return null;
    }
    return response.json();
  } catch (error) {
    console.error("No se pudo cargar el resultado de scanId", scanId, error);
    return null;
  }
}

export async function fetchScanProgress(scanId: string) {
  try {
    const response = await fetch(`${API_URL}/scan/${scanId}/progress`);
    if (!response.ok) {
      return null;
    }
    return response.json();
  } catch (error) {
    console.error("No se pudo obtener el progreso de scanId", scanId, error);
    return null;
  }
}

export async function deleteScan(scanId: string) {
  try {
    const response = await fetch(`${API_URL}/scan/${scanId}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error("No se pudo eliminar el dominio.");
    }
    return true;
  } catch (error) {
    console.error("Error eliminando scanId", scanId, error);
    throw error;
  }
}

export async function fetchAllScans(): Promise<Domain[]> {
  try {
    const response = await fetch(`${API_URL}/scans`);
    if (!response.ok) {
      throw new Error("No se pudieron cargar los dominios");
    }
    const scans = await response.json();
    
    // Mapear al modelo Domain del frontend
    return scans.map((scan: any) => {
      let riskLevel = null;
      let score = null;

      if (scan.results) {
        // Asumiendo que usamos la misma lógica de parseSecurityResults en el frontend,
        // o si los resultados crudos ya tienen el cálculo, podemos extraerlo.
        // Pero parseSecurityResults hace ese cálculo. Vamos a devolver un Dominio básico y luego el frontend puede llamar parseSecurityResults si es necesario, 
        // pero parseSecurityResults toma results.results que sería el JSON crudo o parseado.
        const parsed = scan.results.zap ? scan.results : null; // Simplificación temporal si lo hace el Dashboard.
      }

      return {
        id: scan.scan_id,
        target: scan.target_url,
        scanId: scan.scan_id,
        lastScan: scan.created_at,
        score: null,
        riskLevel: null,
        status: scan.status,
        rawResults: scan.results // Lo guardamos para poder parsearlo luego
      };
    });
  } catch (error) {
    console.error("Error obteniendo los escaneos", error);
    return [];
  }
}
