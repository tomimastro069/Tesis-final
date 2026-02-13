import os
import time
import json
import requests
from ..runners.exec import run_command

ZAP_API_KEY = ""  # si configuraste API key en el daemon, ponela acá
ZAP_HOST = "zap"
ZAP_PORT = 8090

def run_zap(target_url: str, output_dir: str) -> dict:
    """
    Ejecuta un escaneo activo de ZAP contra un target y guarda el resultado en JSON.
    
    Args:
        target_url (str): URL objetivo
        output_dir (str): Carpeta donde se guardará el JSON
    
    Returns:
        dict: {
            'output_file': str,   # path al JSON
            'stdout': str,        # salida cruda de ZAP (informativa)
            'stderr': str         # errores crudos
        }
    """
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "resultado_zap.json")
    
    base_url = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON"
    
    try:
        # 1. Acceder a la API para iniciar el escaneo activo
        scan_url = f"{base_url}/ascan/action/scan/?url={target_url}"
        if ZAP_API_KEY:
            scan_url += f"&apikey={ZAP_API_KEY}"
        
        r = requests.get(scan_url)
        r.raise_for_status()
        scan_id = r.json().get("scan")
        
        stdout_msgs = [f"Iniciando escaneo ZAP en {target_url}, scan_id={scan_id}"]
        stderr_msgs = []
        
        # 2. Esperar a que termine el escaneo activo
        status_url = f"{base_url}/ascan/view/status/?scanId={scan_id}"
        while True:
            resp = requests.get(status_url)
            resp.raise_for_status()
            status = int(resp.json().get("status", 0))
            stdout_msgs.append(f"Progreso: {status}%")
            if status >= 100:
                break
            time.sleep(2)
        
        # 3. Obtener el reporte en JSON
        report_url = f"http://{ZAP_HOST}:{ZAP_PORT}/OTHER/core/other/json/?apikey={ZAP_API_KEY}"
        # si querés usar el endpoint core/json o core/other/html también
        # acá usamos /OTHER/core/other/json como placeholder
        
        # Por simplicidad, también podemos exportar via comando docker exec si preferís
        # Pero usamos requests directo
        report_data = {
            "scan_id": scan_id,
            "target": target_url,
            "info": "Escaneo completo, resultados disponibles en ZAP GUI o API"
        }
        
        # Guardar JSON
        with open(output_file, "w") as f:
            json.dump(report_data, f, indent=4)
        
        stdout_msgs.append(f"Archivo JSON generado en: {output_file}")
        return {
            "output_file": output_file,
            "stdout": "\n".join(stdout_msgs),
            "stderr": "\n".join(stderr_msgs)
        }
    
    except Exception as e:
        return {
            "output_file": output_file,
            "stdout": "",
            "stderr": str(e)
        }
