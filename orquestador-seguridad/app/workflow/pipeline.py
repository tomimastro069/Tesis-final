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
    obtener_reporte_json,
    configurar_autenticacion
)
from app.parsers.ffuf_parser import parsear_ffuf
from app.parsers.zap_parser import parsear_spider, parsear_zap
from app.parsers.sqlmap_parser import parsear_sqlmap
from app.utils.results import consolidar_resultados 
from app.db.database import init_db, save_vulnerable_url

from app.config import settings

# Configuración de Wordlists
# Se usan rutas dinámicas basadas en WORDLISTS_DIR de settings
WORDLISTS = {
    "small": os.path.join(settings.WORDLISTS_DIR, "Discovery", "Web-content", "wordlist-small.txt"),
    "medium": os.path.join(settings.WORDLISTS_DIR, "Discovery", "Web-content", "wordlist-medium.txt")
}
OUTPUT_DIR = "./output/raw"
FINAL_REPORT_FILE = "resultado.json"

def run_security_pipeline(target_url, nivel="medium", cookies=None):
    """
    Función principal que coordina todo el escaneo.
    
    Args:
        target_url: URL objetivo a escanear
        nivel: Nivel de wordlist a usar ("small" o "medium"). Default: "medium"
        cookies: String opcional con cookies (ej: "PHPSESSID=123")
    
    Returns:
        dict: Datos crudos consolidados de todos los escaneos
    """
    # Inicializar la base de datos de historial
    init_db()
    
    # Validar nivel y obtener ruta de wordlist
    if nivel not in WORDLISTS:
        print(f"Error: Nivel '{nivel}' inválido. Use 'small' o 'medium'")
        return None
    
    WORDLIST_PATH = WORDLISTS[nivel]
    
    print(f"--- Iniciando Orquestador para: {target_url} ---")
    print(f"Nivel de wordlist: {nivel}")
    if cookies:
        print(f"Autenticando con cookies en ZAP, FFUF y SQLMap...")
    
    # Asegurar que el directorio de salida exista
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # --- Configuración Autenticación Global (ZAP) ---
    if cookies:
        configurar_autenticacion(cookies)
    
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
    sqlmap_raw = run_sqlmap_batch(lista_urls, cookies=cookies)

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
    ffuf_raw = run_ffuf(target_url, WORDLIST_PATH, OUTPUT_DIR, cookies=cookies)
    
    # Manejar caso de escaneo omitido (todas las palabras ya fueron probadas)
    if ffuf_raw.get("skipped"):
        print(f"  [FFUF] Escaneo omitido: todas las palabras ya fueron probadas anteriormente.")
        ffuf_data = {}
    else:
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

    # --- Marcar URLs vulnerables para re-testeo automático ---
    # ZAP: guardar cada alerta encontrada
    for alerta in zap_parseado.get("alertas", []):
        save_vulnerable_url(
            url=alerta["url"],
            tool="ZAP",
            vulnerabilidad=alerta["vulnerabilidad"],
            severidad=alerta["severidad"]
        )
    
    # SQLMap: guardar cada vulnerabilidad encontrada
    for vuln in sqlmap_parseado.get("vulnerabilidades", []):
        save_vulnerable_url(
            url=vuln["url"],
            tool="SQLMap",
            vulnerabilidad=vuln.get("tipo", "SQL Injection"),
            severidad="High"
        )
    
    total_marcadas = len(zap_parseado.get("alertas", [])) + len(sqlmap_parseado.get("vulnerabilidades", []))
    if total_marcadas > 0:
        print(f"\n[⚠] {total_marcadas} URL(s) marcadas para re-testeo automático en el próximo escaneo.")

    return resultados_unificados



    #docker exec -it security-app sh