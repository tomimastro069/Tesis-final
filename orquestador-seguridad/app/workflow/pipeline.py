import os
import json
import requests
from app.scanners.ffuf import run_ffuf
from app.scanners.sqlmap import run_sqlmap_batch
from app.scanners.zap import (
    iniciar_spider, 
    esperar_spider, 
    obtener_urls,
    iniciar_escaneo_activo, 
    esperar_escaneo_activo, 
    obtener_reporte_json,
    configurar_autenticacion,
    agregar_urls_a_zap,
    limpiar_sesion_zap,
    configurar_user_agent_zap
)
from app.parsers.ffuf_parser import parsear_ffuf
from app.parsers.zap_parser import parsear_spider, parsear_zap
from app.parsers.sqlmap_parser import parsear_sqlmap
from app.utils.results import consolidar_resultados 

from app.config import settings

# Configuración de Wordlists
WORDLISTS = {
    "small": os.path.join(settings.WORDLISTS_DIR, "Discovery", "Web-content", "wordlist-small.txt"),
    "medium": os.path.join(settings.WORDLISTS_DIR, "Discovery", "Web-content", "wordlist-medium.txt")
}
OUTPUT_DIR = "./output/raw"
FINAL_REPORT_FILE = "resultado.json"

def run_security_pipeline(target_url, nivel="medium", cookies=None):
    if nivel not in WORDLISTS:
        print(f"Error: Nivel '{nivel}' inválido. Use 'small' o 'medium'")
        return None
    
    WORDLIST_PATH = WORDLISTS[nivel]
    
    print(f"--- Iniciando Orquestador para: {target_url} ---")
    print(f"Nivel de wordlist: {nivel}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # --- 0. LOGIN AUTOMÁTICO ---
    print(f"[*] Iniciando sesión automática en {target_url}...")
    session = requests.Session()
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    session.headers.update({'User-Agent': ua})
    
    try:
        login_url = f"{target_url.rstrip('/')}/login.php"
        r = session.get(login_url)
        import re
        token_match = re.search(r"name='user_token' value='(.*?)'", r.text)
        user_token = token_match.group(1) if token_match else ""
        
        data = {"username": "admin", "password": "password", "Login": "Login", "user_token": user_token}
        session.post(login_url, data=data)
        
        security_url = f"{target_url.rstrip('/')}/security.php"
        r = session.get(security_url)
        token_match = re.search(r"name='user_token' value='(.*?)'", r.text)
        sec_token = token_match.group(1) if token_match else ""
        
        session.post(security_url, data={"security": "low", "seclev_submit": "Submit", "user_token": sec_token})
        
        cookies_dict = session.cookies.get_dict()
        cookies = "; ".join([f"{k}={v}" for k, v in cookies_dict.items()])
        if "security" not in cookies:
            cookies += "; security=low"
        print(f" [+] Sesión establecida automáticamente. Cookie: {cookies}")
    except Exception as e:
        print(f" [!] Error en login automático: {e}")

    # --- CONFIGURAR ZAP ---
    limpiar_sesion_zap()
    configurar_user_agent_zap(ua)
    if cookies:
        configurar_autenticacion(cookies)
    
    # --- VALIDACIÓN (LA QUE ANDABA) ---
    print(f"[*] Validando acceso a rutas protegidas en {target_url}...")
    try:
        test_url = f"{target_url.rstrip('/')}/vulnerabilities/sqli/"
        headers = {
            'Cookie': cookies,
            'User-Agent': ua,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        r = requests.get(test_url, headers=headers, allow_redirects=True, timeout=10)
        if "login.php" in r.url or "Login" in r.text:
            print(f" [!] ALERTA: La sesión es INVÁLIDA (pero seguimos adelante).")
        else:
            print(" [+] Sesión VALIDADA exitosamente para rutas protegidas.")
    except:
        print(" [!] No se pudo validar la sesión.")

    # [1/4] FFUF
    print("\n[1/4] Ejecutando FFUF...")
    ffuf_raw = run_ffuf(target_url, WORDLIST_PATH, OUTPUT_DIR, cookies=cookies)
    
    ffuf_data = {}
    rutas_ffuf_nuevas = []
    if os.path.exists(ffuf_raw["output_file"]):
        with open(ffuf_raw["output_file"], "r") as f:
            try:
                ffuf_data = json.load(f)
                rutas_ffuf_nuevas = ffuf_data.get("results", [])
            except: pass

    if rutas_ffuf_nuevas:
        agregar_urls_a_zap(rutas_ffuf_nuevas)

    # [2/4] ZAP Spider
    print("\n[2/4] Ejecutando ZAP Spider...")
    s_id = iniciar_spider(target_url)
    esperar_spider(s_id)
    spider_urls = obtener_urls(s_id)

    # [3/4] ZAP Active Scan
    print("\n[3/4] Ejecutando ZAP Active Scan...")
    ascan_id = iniciar_escaneo_activo(target_url)
    esperar_escaneo_activo(ascan_id)
    reporte_zap_crudo = obtener_reporte_json()

    # [4/4] SQLMap
    print("\n[4/4] Ejecutando SQLMap...")
    lista_urls_spider = spider_urls.get("results", [])
    rutas_semilla = [
        f"{target_url}/vulnerabilities/sqli/?id=1&Submit=Submit",
        f"{target_url}/vulnerabilities/sqli_blind/?id=1&Submit=Submit",
    ]
    lista_urls_total = list(set(lista_urls_spider + rutas_semilla))
    
    # Enrutamos por ZAP para que no nos patee el 302
    proxy_zap = "http://zap:8090"
    sqlmap_raw = run_sqlmap_batch(lista_urls_total, cookies=cookies, proxy=proxy_zap)

    # Consolidación final
    hallazgos_finales = {
        "target": target_url,
        "spider_raw": spider_urls,
        "zap_raw": reporte_zap_crudo,
        "sqlmap_raw": sqlmap_raw,
        "ffuf_raw": ffuf_data
    }

    output_path = os.path.join(OUTPUT_DIR, FINAL_REPORT_FILE)
    with open(output_path, "w") as f:
        json.dump(hallazgos_finales, f, indent=4)
    
    return hallazgos_finales

def run_parser_pipeline(resultado_escaneo):
    if not resultado_escaneo: return None
    
    print("Iniciando parseo de ZAP, SPIDER y FFUF:")
    spider_crudo = resultado_escaneo.get("spider_raw", {})
    zap_crudo = resultado_escaneo.get("zap_raw", {})
    sqlmap_crudo = resultado_escaneo.get("sqlmap_raw", [])
    ffuf_crudo = resultado_escaneo.get("ffuf_raw", {})

    vuls_spider = parsear_spider(spider_crudo)
    vuls_zap = parsear_zap(zap_crudo)
    vuls_sqlmap = parsear_sqlmap(sqlmap_crudo)
    vuls_ffuf = parsear_ffuf(ffuf_crudo)

    resultado_unificado = consolidar_resultados(vuls_spider, vuls_zap, vuls_sqlmap, vuls_ffuf)
    
    unificado_path = os.path.join(OUTPUT_DIR, "resultado_unificado.json")
    with open(unificado_path, "w") as f:
        json.dump(resultado_unificado, f, indent=4)
        
    return resultado_unificado