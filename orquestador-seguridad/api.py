import logging
import os
import requests
from typing import Optional
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel

# Configurar logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("security_api")

from app.workflow.pipeline import run_security_pipeline, run_parser_pipeline
from app.reports.generator import generar_reporte

app = FastAPI(
    title="Orquestador de Seguridad API",
    description="API para orquestar y automatizar escaneos de seguridad con ZAP, FFUF y SQLMap, integrados con n8n.",
    version="1.0.0"
)

from fastapi.middleware.cors import CORSMiddleware

# Permitir CORS desde tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # O especificar exactamente ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers.n8n_router import router as n8n_router
app.include_router(n8n_router)

class ScanRequest(BaseModel):
    target: str
    nivel: Optional[str] = "medium"
    cookies: Optional[str] = None
    callback_url: Optional[str] = None
    clean_cache: Optional[bool] = False
    sqlmap_level: Optional[str] = "basic"

    model_config = {
        "json_schema_extra": {
            "example": {
                "target": "http://dvwa",
                "nivel": "small",
                "cookies": "PHPSESSID=your_session_id; security=low",
                "callback_url": "http://security-n8n:5678/webhook/scan-completado",
                "clean_cache": False,
                "sqlmap_level": "basic"
            }
        }
    }

def ejecutar_pipeline_segundo_plano(target: str, nivel: str, cookies: Optional[str], callback_url: Optional[str], clean_cache: bool = False, sqlmap_level: str = "basic"):
    logger.info(f"Iniciando escaneo de seguridad en segundo plano para: {target} (Nivel: {nivel})")
    try:
        # [MEJORA] Borrado opcional de caché
        if clean_cache:
            logger.info("[*] Limpiando la caché de la base de datos antes de iniciar...")
            from app.db.database import limpiar_cache_completa
            limpiar_cache_completa()

        # [MEJORA] Normalizar cookies para habilitar inicio de sesión automático si se envía vacío o "none"
        if cookies and (cookies.strip() == "" or cookies.strip().lower() == "none"):
            logger.info("[*] Cookies vacías o con valor 'none'. Se usará inicio de sesión automático.")
            cookies = None

        # 1. Ejecutar el pipeline de escaneo
        resultado_escaneo = run_security_pipeline(target, nivel, cookies, sqlmap_level=sqlmap_level)
        if not resultado_escaneo:
            raise Exception("El pipeline de escaneo no retornó ningún resultado.")

        # 2. Parsear los resultados unificados
        resultado_parseo = run_parser_pipeline(resultado_escaneo)

        # 3. Generar los reportes en Markdown
        reporte_tecnico_path, reporte_cliente_path = generar_reporte(resultado_parseo)

        logger.info("[+] Escaneo finalizado y reportes generados con éxito.")

        # Leer el contenido de los reportes para enviarlos por el callback
        reporte_tecnico_content = "No se pudo leer el reporte técnico."
        reporte_cliente_content = "No se pudo leer el reporte del cliente."

        if os.path.exists(reporte_tecnico_path):
            with open(reporte_tecnico_path, "r", encoding="utf-8") as f:
                reporte_tecnico_content = f.read()

        if os.path.exists(reporte_cliente_path):
            with open(reporte_cliente_path, "r", encoding="utf-8") as f:
                reporte_cliente_content = f.read()

        payload = {
            "status": "completed",
            "target": target,
            "message": "Escaneo completado exitosamente y reportes generados.",
            "reporte_tecnico": reporte_tecnico_content,
            "reporte_cliente": reporte_cliente_content
        }

    except Exception as e:
        logger.error(f"[-] Error durante la ejecución del pipeline: {e}", exc_info=True)
        payload = {
            "status": "failed",
            "target": target,
            "message": f"Error en el pipeline de seguridad: {str(e)}",
            "reporte_tecnico": None,
            "reporte_cliente": None
        }

    # Enviar callback si se especificó la URL
    if callback_url:
        logger.info(f"Enviando callback a: {callback_url}")
        try:
            r = requests.post(callback_url, json=payload, timeout=15)
            logger.info(f"Callback enviado. Respuesta: {r.status_code}")
        except Exception as cb_err:
            logger.error(f"[-] Falló el envío del callback a {callback_url}: {cb_err}")
    else:
        logger.info("No se especificó callback_url. Resultados listos localmente en /output/reports.")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Orquestador de Seguridad listo. Accedé a /docs para la documentación interactiva."
    }

@app.post("/scan", status_code=202)
def iniciar_escaneo(request: ScanRequest, background_tasks: BackgroundTasks):
    """
    Inicia la tubería de escaneo de seguridad en segundo plano.
    Retorna inmediatamente confirmando que el escaneo fue encolado.
    """
    if request.nivel not in ["small", "medium"]:
        raise HTTPException(status_code=400, detail="El nivel debe ser 'small' o 'medium'.")

    # Encolar la tarea en segundo plano
    background_tasks.add_task(
        ejecutar_pipeline_segundo_plano,
        target=request.target,
        nivel=request.nivel,
        cookies=request.cookies,
        callback_url=request.callback_url,
        clean_cache=request.clean_cache,
        sqlmap_level=request.sqlmap_level
    )

    return {
        "message": "Escaneo lanzado! Vas a recibir una notificacion cuando termine.",
        "target": request.target,
        "nivel": request.nivel,
        "sqlmap_level": request.sqlmap_level
    }
