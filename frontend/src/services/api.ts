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
  lastScan: string | null;
  score: number | null;
  riskLevel: string | null;
  status: 'idle' | 'scanning' | 'completed' | 'error';
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

export async function fetchScanResults() {
  try {
    const response = await fetch('/output/raw/resultado.json?t=' + Date.now());
    if (!response.ok) {
      return null;
    }
    return response.json();
  } catch (error) {
    console.error("No se pudo cargar el resultado.json", error);
    return null;
  }
}
