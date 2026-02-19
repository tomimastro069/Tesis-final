import os
import json
from app.scanners.ffuf import run_ffuf
from app.scanners.zap import (
    iniciar_spider, 
    esperar_spider, 
    iniciar_escaneo_activo, 
    esperar_escaneo_activo, 
    obtener_reporte_json
)
from app.parsers.ffuf_parser import parsear_ffuf
from app.parsers.zap_parser import parsear_spider, parsear_zap

# Configuración
WORDLIST_PATH = "./wordlist.txt"
OUTPUT_DIR = "./output/raw"
FINAL_REPORT_FILE = "resultado.json"

def run_security_pipeline(target_url):
    """
    Función principal que coordina todo el escaneo.
    """
    print(f"--- Iniciando Orquestador para: {target_url} ---")
    
    # Asegurar que el directorio de salida exista
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # --- 1. ZAP SPIDER ---
    print("\n[1/3] Ejecutando ZAP Spider...")
    spider_id = iniciar_spider(target_url)
    esperar_spider(spider_id)
    
    # --- 2. ZAP ACTIVE SCAN ---
    print("\n[2/3] Ejecutando ZAP Active Scan...")
    ascan_id = iniciar_escaneo_activo(target_url)
    esperar_escaneo_activo(ascan_id)
    
    # Obtener reporte crudo de ZAP (se mantiene en memoria para el reporte final)
    reporte_zap_crudo = obtener_reporte_json()
        
    # --- 3. FFUF ---
    print("\n[3/3] Ejecutando FFUF...")
    
    # Crear wordlist dummy si no existe (para evitar errores)
    if not os.path.exists(WORDLIST_PATH):
        with open(WORDLIST_PATH, "w") as f:
            f.write("admin\nlogin\nbackup\nconfig\n.env\n")
    
    # Ejecutar FFUF
    # Nota: Esto creará un archivo JSON con datos crudos de FFUF en OUTPUT_DIR
    ffuf_raw = run_ffuf(target_url, WORDLIST_PATH, OUTPUT_DIR)
    
    # Leer los datos crudos de FFUF para incluirlos en el reporte final
    # (run_ffuf guarda el archivo y aquí lo leemos para consolidarlo)
    ffuf_data = {}
    if os.path.exists(ffuf_raw["output_file"]):
        with open(ffuf_raw["output_file"], "r") as f:
            try:
                ffuf_data = json.load(f)
            except json.JSONDecodeError:
                print("Advertencia: No se pudo leer el JSON crudo de FFUF.")
    
    # --- 4. CONSOLIDACIÓN Y REPORTE FINAL ---
    print("\nGenerando paquete de datos crudos...")
    
    hallazgos_finales = {
        "target": target_url,
        "zap_raw": reporte_zap_crudo,  # Datos crudos de ZAP
        "ffuf_raw": ffuf_data          # Datos crudos de FFUF
    }
    
    # Guardar el reporte final en resultado.json
    ruta_final = os.path.join(OUTPUT_DIR, FINAL_REPORT_FILE)
    with open(ruta_final, "w") as f:
        json.dump(hallazgos_finales, f, indent=4)
    
    print(f"--- Ejecución finalizada. Datos crudos guardados en: {ruta_final} ---")
    return hallazgos_finales


    def run_parser_pipeline(hallazgos_zap_ffuf):
        pass