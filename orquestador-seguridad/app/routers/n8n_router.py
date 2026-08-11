from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Any, Dict
import requests
import logging
import os

logger = logging.getLogger("security_api.n8n")

router = APIRouter(
    prefix="/api/n8n",
    tags=["n8n"]
)

# N8N Webhook URL - Cargado desde variables de entorno para apuntar a producción por defecto
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://security-n8n:5678/webhook/analyze-vuln")

class VulnerabilityAnalysisRequest(BaseModel):
    id: str | int
    name: str
    type: str
    severity: str
    description: Optional[str] = None
    location: Optional[str] = None

class VulnerabilityAnalysisResponse(BaseModel):
    status: str
    data: Dict[str, Any]

def _send_to_n8n_sync(payload: dict) -> dict:
    """
    Función modular para enviar a n8n.
    Separamos esto para que en el futuro, si se requiere websockets, tareas de fondo,
    o polling asíncrono, podamos modificar/extender esta implementación fácilmente.
    """
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=30)
        response.raise_for_status()
        
        # Intentamos retornar el JSON real de n8n
        try:
            return response.json()
        except ValueError:
            # Si n8n no devuelve JSON, retornamos texto
            return {"raw_text": response.text}
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error comunicándose con n8n: {e}")
        # Retornamos un mock si falla la conexión porque n8n no está corriendo aún en esa URL.
        return {
            "status": "mock",
            "message": "Simulando respuesta de n8n porque el webhook no está disponible.",
            "original_error": str(e),
            "ai_suggestion": f"Análisis simulado para la vulnerabilidad: {payload.get('vulnerability', {}).get('name')}. Aquí iría la respuesta de la IA generada por el pipeline de n8n."
        }

@router.post("/analyze", response_model=VulnerabilityAnalysisResponse)
def analyze_vulnerability(request: VulnerabilityAnalysisRequest):
    """
    Recibe la vulnerabilidad y la envía a n8n para análisis con IA.
    """
    logger.info(f"Recibida solicitud de análisis para la vulnerabilidad: {request.name}")
    
    # Construir el payload para n8n
    n8n_payload = {
        "vulnerability": request.model_dump(),
        "action": "analyze"
    }

    # Llamar al servicio (aislado para facilitar futura refactorización)
    n8n_response = _send_to_n8n_sync(n8n_payload)
    
    return VulnerabilityAnalysisResponse(
        status="success",
        data=n8n_response
    )
