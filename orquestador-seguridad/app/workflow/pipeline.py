import os
import json
from app.scanners.ffuf import run_ffuf
from app.scanners.sqlmap import run_sqlmap_batch
from app.scanners.zap import (
    iniciar_spider, 
    esperar_spider, 
    obtener_urls,
    iniciar_escaneo_activo, 
    esperar_escaneo_activo, 
    obtener_reporte_json
)
from app.parsers.ffuf_parser import parsear_ffuf
from app.parsers.zap_parser import parsear_spider, parsear_zap
from app.parsers.sqlmap_parser import parsear_sqlmap
from app.utils.results import consolidar_resultados 

# Configuración
# Nota: el directorio real se llama "worldlists" (con una 'l' extra),
# por lo que la ruta anterior provocaba un FileNotFoundError al crear
# el archivo. También nos aseguramos de que la carpeta existe antes de
# intentar escribir la wordlist.
WORDLISTS = {
    "small": "app/wordlists/Discovery/Web-content/wordlist-small.txt",
    "medium": "app/wordlists/Discovery/Web-content/wordlist-medium.txt"
}
nivel = input("Nivel de escaneo: (small/medium): ").lower()
WORDLIST_PATH = WORDLISTS.get(nivel)
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
    print("\n[1/4] Ejecutando ZAP Spider...")
    spider_id = iniciar_spider(target_url)
    esperar_spider(spider_id)
    spider_urls = obtener_urls(spider_id)

    # --- 2. ZAP ACTIVE SCAN ---
    print("\n[2/4] Ejecutando ZAP Active Scan...")
    ascan_id = iniciar_escaneo_activo(target_url)
    esperar_escaneo_activo(ascan_id)
    
    # Obtener reporte crudo de ZAP (se mantiene en memoria para el reporte final)
    reporte_zap_crudo = obtener_reporte_json()

    # --- 3. SQLMAP ---
    print("\n[3/4] Ejecutando SQLMAP...")
    # Sacamos la lista de URLs del resultado del spider
    # spider_urls es un dict tipo {"results": ["http://...", ...]}
    lista_urls = spider_urls.get("results", [])
    sqlmap_raw = run_sqlmap_batch(lista_urls)

    # --- 4. FFUF ---
    print("\n[4/4] Ejecutando FFUF...")
    
    # Crear wordlist dummy si no existe (para evitar errores)
    # Asegurarse de que la carpeta padre exista antes de abrir el archivo.
    wordlist_dir = os.path.dirname(WORDLIST_PATH)
    if wordlist_dir and not os.path.exists(wordlist_dir):
        os.makedirs(wordlist_dir, exist_ok=True)

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
        "spider_raw": spider_urls,
        "zap_raw": reporte_zap_crudo,  # Datos crudos de ZAP
        "sqlmap_raw": sqlmap_raw,      # Datos crudos de SQLMap
        "ffuf_raw": ffuf_data          # Datos crudos de FFUF
    }
    
    # Guardar el reporte final en resultado.json
    ruta_final = os.path.join(OUTPUT_DIR, FINAL_REPORT_FILE)
    with open(ruta_final, "w") as f:
        json.dump(hallazgos_finales, f, indent=4)
    
    print(f"--- Ejecución finalizada. Datos crudos guardados en: {ruta_final} ---")
    return hallazgos_finales


def run_parser_pipeline(resultado_escaneo):

    #Dividimos los datos crudos del escaneo
    spider_crudo = resultado_escaneo["spider_raw"]
    zap_crudo = resultado_escaneo["zap_raw"]
    ffuf_crudo = resultado_escaneo["ffuf_raw"]
    sqlmap_crudo = resultado_escaneo["sqlmap_raw"]

    #Parsear el spider
    spider_parseado = parsear_spider(spider_crudo)

    #Parsear el zap
    zap_parseado = parsear_zap(zap_crudo)

    #Parsear el ffuf
    ffuf_parseado = parsear_ffuf(ffuf_crudo)

    sqlmap_parseado = parsear_sqlmap(sqlmap_crudo)

    #Consolidar los 3 resultados en una sola lista sin duplicados
    resultados_unificados = consolidar_resultados(spider_parseado, zap_parseado, ffuf_parseado, sqlmap_parseado)

    return resultados_unificados