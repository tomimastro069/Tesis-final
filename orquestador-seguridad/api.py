import logging
import os
import requests
import uuid
import json
from typing import Optional
from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Configurar logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("security_api")

from app.workflow.pipeline import run_security_pipeline, run_parser_pipeline
from app.reports.generator import generar_reporte
from app.db.database import create_scan, update_scan_status, save_scan_results, get_scan_by_id, init_db, soft_delete_scan, get_all_scans

# Inicializar BD
init_db()

# Almacén en memoria para el progreso de escaneos activos
# Estructura: { scan_id: {"percentage": int, "message": str} }
scan_progress_store = {}

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

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Excepción global no manejada: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor", "message": str(exc)},
    )

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

def ejecutar_pipeline_segundo_plano(scan_id: str, target: str, nivel: str, cookies: Optional[str], callback_url: Optional[str], clean_cache: bool = False, sqlmap_level: str = "basic"):
    logger.info(f"Iniciando escaneo de seguridad en segundo plano para: {target} (ID: {scan_id})")
    try:
        if clean_cache:
            logger.info("[*] Limpiando la caché de la base de datos antes de iniciar...")
            from app.db.database import limpiar_cache_completa
            limpiar_cache_completa()

        if cookies and (cookies.strip() == "" or cookies.strip().lower() == "none"):
            logger.info("[*] Cookies vacías o con valor 'none'. Se usará inicio de sesión automático.")
            cookies = None

        scan_progress_store[scan_id] = {"percentage": 0, "message": "Iniciando escaneo..."}

        def update_progress(percentage: int, message: str):
            scan_progress_store[scan_id] = {"percentage": percentage, "message": message}
            logger.info(f"Progreso [{scan_id}]: {percentage}% - {message}")

        resultado_escaneo = run_security_pipeline(target, nivel, cookies, sqlmap_level=sqlmap_level, progress_callback=update_progress, scan_id=scan_id)
        if not resultado_escaneo:
            raise Exception("El pipeline de escaneo no retornó ningún resultado.")

        resultado_parseo = run_parser_pipeline(resultado_escaneo)

        reporte_tecnico_path, reporte_cliente_path = generar_reporte(resultado_parseo)

        logger.info("[+] Escaneo finalizado y reportes generados con éxito.")
        
        # Guardar en DB
        save_scan_results(scan_id, json.dumps(resultado_parseo))

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
            "scan_id": scan_id,
            "target": target,
            "message": "Escaneo completado exitosamente y reportes generados.",
            "reporte_tecnico": reporte_tecnico_content,
            "reporte_cliente": reporte_cliente_content
        }

        # Limpiar progreso en memoria tras finalizar exitosamente
        if scan_id in scan_progress_store:
            del scan_progress_store[scan_id]

    except Exception as e:
        logger.error(f"[-] Error durante la ejecución del pipeline: {e}", exc_info=True)
        
        try:
            from app.scanners.zap import abortar_escaneos_zap
            abortar_escaneos_zap()
        except Exception as zap_err:
            logger.error(f"[-] Error intentando abortar ZAP tras fallo: {zap_err}")
            
        update_scan_status(scan_id, 'failed')
        payload = {
            "status": "failed",
            "scan_id": scan_id,
            "target": target,
            "message": f"Error en el pipeline de seguridad: {str(e)}",
            "reporte_tecnico": None,
            "reporte_cliente": None
        }

        # Limpiar progreso en memoria si hubo error
        if scan_id in scan_progress_store:
            del scan_progress_store[scan_id]

    if callback_url:
        logger.info(f"Enviando callback a: {callback_url}")
        try:
            r = requests.post(callback_url, json=payload, timeout=15)
            logger.info(f"Callback enviado. Respuesta: {r.status_code}")
        except Exception as cb_err:
            logger.error(f"[-] Falló el envío del callback a {callback_url}: {cb_err}")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Orquestador de Seguridad listo. Accedé a /docs para la documentación interactiva."
    }

@app.get("/scans")
def get_scans():
    scans = get_all_scans()
    for s in scans:
        if s["results_raw"]:
            try:
                s["results"] = json.loads(s["results_raw"])
            except:
                s["results"] = None
            del s["results_raw"]
    return scans

@app.get("/scan/{scan_id}/progress")
def get_scan_progress(scan_id: str):
    # Consultar la memoria
    if scan_id in scan_progress_store:
        return scan_progress_store[scan_id]
    
    # Si no está en memoria, podría haber finalizado o fallado. Consultamos la BD.
    scan_data = get_scan_by_id(scan_id)
    if not scan_data:
        raise HTTPException(status_code=404, detail="Scan no encontrado")
        
    if scan_data["status"] == "completed":
        return {"percentage": 100, "message": "Análisis Completado"}
    elif scan_data["status"] == "failed":
        return {"percentage": 100, "message": "Análisis Fallido"}
        
    # Si está 'scanning' pero no está en memoria (quizás se reinició el backend)
    return {"percentage": 0, "message": "Iniciando o retomando análisis..."}

@app.get("/scan/{scan_id}")
def get_scan(scan_id: str):
    scan_data = get_scan_by_id(scan_id)
    if not scan_data:
        raise HTTPException(status_code=404, detail="Scan no encontrado")
    
    if scan_data["results_raw"]:
        try:
            scan_data["results"] = json.loads(scan_data["results_raw"])
        except:
            scan_data["results"] = None
        del scan_data["results_raw"]
    
    return scan_data

@app.delete("/scan/{scan_id}")
def delete_scan(scan_id: str):
    scan_data = get_scan_by_id(scan_id)
    if not scan_data:
        raise HTTPException(status_code=404, detail="Scan no encontrado")
    
    try:
        from app.scanners.zap import abortar_escaneos_zap
        abortar_escaneos_zap()
    except Exception as zap_err:
        logger.error(f"[-] Error abortando ZAP al eliminar/cancelar scan: {zap_err}")

    try:
        from app.config import settings
        lock_path = os.path.join(settings.OUTPUT_DIR, "sqlmap_bg.lock")
        if os.path.exists(lock_path):
            with open(lock_path, "r", encoding="utf-8") as f:
                pid = int(f.read().strip())
            logger.info(f"[*] Matando proceso de SQLMap con PID {pid} por cancelación...")
            import signal
            os.kill(pid, signal.SIGTERM)
            if os.path.exists(lock_path):
                os.remove(lock_path)
    except Exception as sqlmap_err:
        logger.error(f"[-] Error matando proceso SQLMap por cancelación (puede que no esté corriendo): {sqlmap_err}")
    
    from app.db.database import soft_delete_scan
    soft_delete_scan(scan_id)
    return {"message": "Dominio eliminado exitosamente", "scan_id": scan_id}

@app.post("/scan", status_code=202)
def iniciar_escaneo(request: ScanRequest, background_tasks: BackgroundTasks):
    if request.nivel not in ["small", "medium"]:
        raise HTTPException(status_code=400, detail="El nivel debe ser 'small' o 'medium'.")

    scan_id = str(uuid.uuid4())
    create_scan(scan_id, request.target)

    background_tasks.add_task(
        ejecutar_pipeline_segundo_plano,
        scan_id=scan_id,
        target=request.target,
        nivel=request.nivel,
        cookies=request.cookies,
        callback_url=request.callback_url,
        clean_cache=request.clean_cache,
        sqlmap_level=request.sqlmap_level
    )

    return {
        "message": "Escaneo lanzado! Vas a recibir una notificacion cuando termine.",
        "scan_id": scan_id,
        "target": request.target,
        "nivel": request.nivel,
        "sqlmap_level": request.sqlmap_level
    }
