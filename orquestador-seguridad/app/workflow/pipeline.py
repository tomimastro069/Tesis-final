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
    limpiar_sesion_zap
)
from app.parsers.zap_parser import parsear_spider, parsear_zap
from app.parsers.ffuf_parser import parsear_ffuf
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

def establecer_sesion_automatica(target_url):
    """
    Realiza un login automático en DVWA y devuelve las cookies.
    También establece el nivel de seguridad a 'low'.
    Si el login falla porque la base de datos no está inicializada,
    intenta inicializarla automáticamente haciendo un POST a setup.php.
    """
    print(f"[*] Iniciando sesión automática en {target_url}...")
    from urllib.parse import urlparse
    parsed = urlparse(target_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    
    login_url = f"{base_url}/login.php"
    security_url = f"{base_url}/security.php"
    setup_url = f"{base_url}/setup.php"
    
    session = requests.Session()
    # User-Agent de navegador para evitar bloqueos
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    session.headers.update({'User-Agent': ua})
    
    def intentar_login():
        try:
            import re
            # 1. Obtener el token user_token del formulario de login
            r = session.get(login_url, timeout=10)
            print(f"   [DEBUG] GET login.php status: {r.status_code}, URL final: {r.url}")
            
            # Intentar con comillas simples y dobles (DVWA puede variar)
            token_match = re.search(r"name=['\"]user_token['\"] value=['\"]([^'\"]*)", r.text)
            user_token = token_match.group(1) if token_match else ""
            print(f"   [DEBUG] user_token encontrado: {'SI' if token_match else 'NO'} ({user_token[:10]}...)")
            
            # 2. Hacer el Login
            payload = {
                "username": "admin",
                "password": "password",
                "Login": "Login",
                "user_token": user_token
            }
            r_login = session.post(login_url, data=payload, timeout=10)
            print(f"   [DEBUG] POST login status: {r_login.status_code}, URL final: {r_login.url}")
            print(f"   [DEBUG] Cookies tras login: {dict(session.cookies)}")
            print(f"   [DEBUG] Body login response (300 chars): {r_login.text[:300]}")
            
            # 3. Establecer nivel de seguridad a 'low'
            payload_sec = {
                "security": "low",
                "seclev_submit": "Submit"
            }
            r_sec = session.post(security_url, data=payload_sec, timeout=10)
            print(f"   [DEBUG] POST security status: {r_sec.status_code}, URL final: {r_sec.url}")
            tiene_logout = "logout.php" in r_sec.text.lower() or "logout" in r_sec.text.lower()
            print(f"   [DEBUG] ¿Tiene 'logout' en respuesta security.php?: {tiene_logout}")
            
            # Verificar si realmente estamos logueados
            return tiene_logout
        except Exception as e:
            print(f" [!] Error durante intento de login: {e}")
            return False

    # Primer intento de login
    if intentar_login():
        cookies_dict = session.cookies.get_dict()
        if "PHPSESSID" in cookies_dict:
            cookie_str = "; ".join([f"{k}={v}" for k, v in cookies_dict.items()])
            print(f" [+] Sesión establecida con éxito y VERIFICADA. Cookie: {cookie_str}")
            return cookie_str

    # Si falló, es muy probable que la base de datos no esté inicializada.
    # Intentamos crear/resetear la base de datos automáticamente.
    print(" [!] El login falló. Intentando inicializar la base de datos de DVWA automáticamente...")
    try:
        # Primero acceder a setup.php sin autenticar (GET) para obtener token si lo requiere
        r_setup_get = session.get(setup_url, timeout=10)
        print(f" [*] setup.php GET status: {r_setup_get.status_code}")

        # Enviar petición POST a setup.php para crear la base de datos
        payload_setup = {
            "create_db": "Create / Reset Database"
        }
        r_setup = session.post(setup_url, data=payload_setup, timeout=15)
        print(f" [*] setup.php POST status: {r_setup.status_code}")
        print(f" [*] setup.php respuesta (primeros 300 chars): {r_setup.text[:300]}")

        # Verificación estricta: buscamos el mensaje real de éxito de DVWA
        setup_ok = (
            "database has been created" in r_setup.text.lower()
            or "setup successful" in r_setup.text.lower()
            or "database setup complete" in r_setup.text.lower()
            or r_setup.status_code == 200
        )

        if setup_ok:
            print(" [+] POST a setup.php ejecutado. Esperando 3s para que MySQL inicialice...")
            import time
            time.sleep(3)
            
            # CRÍTICO: limpiar cookies viejas — el PHPSESSID viejo ya no es válido
            # después de resetear la DB. Necesitamos una sesión nueva.
            session.cookies.clear()
            print(" [+] Cookies limpiadas. Reintentando login...")
            
            # Reintentar el login ahora que la base de datos está creada
            if intentar_login():
                cookies_dict = session.cookies.get_dict()
                if "PHPSESSID" in cookies_dict:
                    cookie_str = "; ".join([f"{k}={v}" for k, v in cookies_dict.items()])
                    print(f" [+] Sesión establecida con éxito tras inicializar la BD. Cookie: {cookie_str}")
                    return cookie_str
                else:
                    print(" [!] Login post-setup OK pero no hay PHPSESSID en cookies.")
            else:
                print(" [!] Login sigue fallando después de setup.php.")
        else:
            print(f" [!] setup.php no devolvió respuesta esperada (status {r_setup.status_code}).")
    except Exception as e:
        print(f" [!] Error intentando inicializar la base de datos: {e}")

    print(" [!] Falló el inicio de sesión automático y no se pudo inicializar la base de datos.")
    return None
def run_security_pipeline(target_url, nivel="medium", cookies=None, sqlmap_level="basic", progress_callback=None, scan_id=None):
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
    
    # --- [MEJORA] LOGIN AUTOMÁTICO ---
    if not cookies:
        cookies = establecer_sesion_automatica(target_url)
    
    # --- 0. PREPARACIÓN DE SESIÓN EN ZAP ---
    print("Limpiando sesión previa de ZAP...")
    limpiar_sesion_zap()

    if cookies:
        print(f"[*] Configurando scanners con cookies: {cookies}")
        configurar_autenticacion(cookies)
        
        # [MEJORA 4] Cebado de Sesión (Priming): Visita forzada para que ZAP capture la sesión
        # Apuntamos a una ruta protegida real para confirmar acceso
        test_url = f"{target_url.rstrip('/')}/vulnerabilities/sqli/"
        print(f"[*] Cebando sesión (Priming) en {test_url}...")
        try:
            # Usamos un User-Agent de navegador para que DVWA nos acepte la cookie
            ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            requests.get(test_url, headers={'Cookie': cookies, 'User-Agent': ua}, timeout=10)
        except Exception as e:
            print(f" [!] Advertencia en Priming: {e}")
    
    # --- 1. ZAP SPIDER ---
    print("\n[1/4] Ejecutando ZAP Spider...")
    if progress_callback: progress_callback(0, "Iniciando ZAP Spider...")
    def cb_spider(local_pct, msg=""):
        if progress_callback: progress_callback(int(local_pct * 0.20), msg or "Ejecutando ZAP Spider...")
    
    spider_id = iniciar_spider(target_url)
    esperar_spider(spider_id, progress_callback=cb_spider)
    spider_urls = obtener_urls(spider_id)

    # --- 2. FFUF (antes del Active Scan para enriquecer el contexto de ZAP) ---
    print("\n[2/4] Ejecutando FFUF...")
    
    # [MEJORA 1] Limpieza Proactiva: Borrar resultado anterior para evitar datos fantasmas
    ffuf_output = os.path.join(OUTPUT_DIR, "ffuf_raw.json")
    if os.path.exists(ffuf_output):
        os.remove(ffuf_output)

    wordlist_dir = os.path.dirname(WORDLIST_PATH)
    if wordlist_dir and not os.path.exists(wordlist_dir):
        os.makedirs(wordlist_dir, exist_ok=True)

    if not os.path.exists(WORDLIST_PATH):
        with open(WORDLIST_PATH, "w") as f:
            f.write("admin\nlogin\nbackup\nconfig\n.env\n")

    if progress_callback: progress_callback(20, "Iniciando FFUF (Fuzzing)...")

    ffuf_raw = run_ffuf(target_url, WORDLIST_PATH, OUTPUT_DIR, cookies=cookies)

    if progress_callback: progress_callback(30, "FFUF completado.")

    if ffuf_raw.get("skipped"):
        print(f"  [FFUF] Escaneo omitido: todas las palabras ya fueron probadas anteriormente.")
        ffuf_data = {}
        rutas_ffuf_nuevas = []
    else:
        ffuf_data = {}
        if ffuf_raw.get("output_file") and os.path.exists(ffuf_raw["output_file"]):
            with open(ffuf_raw["output_file"], "r") as f:
                try:
                    ffuf_data = json.load(f)
                except json.JSONDecodeError:
                    print("Advertencia: No se pudo leer el JSON crudo de FFUF.")
        # Extraer rutas encontradas para inyectarlas en ZAP
        rutas_ffuf_nuevas = ffuf_data.get("results", [])
        # Normalizar al formato [{"url": "..."}] si FFUF devuelve otro formato
        if rutas_ffuf_nuevas and isinstance(rutas_ffuf_nuevas[0], dict) and "url" not in rutas_ffuf_nuevas[0]:
            rutas_ffuf_nuevas = [{"url": r.get("url", "")} for r in rutas_ffuf_nuevas]

    # --- 3. INYECTAR RUTAS DE FFUF EN ZAP (enriquecer el contexto antes del Active Scan) ---
    if rutas_ffuf_nuevas:
        print(f"\n[3/4-pre] Inyectando {len(rutas_ffuf_nuevas)} rutas de FFUF en ZAP...")
        agregar_urls_a_zap(rutas_ffuf_nuevas)
    else:
        print("\n[3/4-pre] Sin rutas nuevas de FFUF para inyectar en ZAP.")

    # --- 4. ZAP ACTIVE SCAN (ahora ataca Spider + rutas de FFUF) ---
    print("\n[3/4] Ejecutando ZAP Active Scan...")
    if progress_callback: progress_callback(30, "Iniciando ZAP Active Scan...")
    def cb_ascan(local_pct, msg=""):
        if progress_callback: progress_callback(30 + int(local_pct * 0.50), msg or "Ejecutando ZAP Active Scan...")
        
    ascan_id = iniciar_escaneo_activo(target_url)
    esperar_escaneo_activo(ascan_id, progress_callback=cb_ascan)

    # Obtener reporte crudo de ZAP
    reporte_zap_crudo = obtener_reporte_json()

    # --- 5. SQLMAP (recibe URLs del Spider + FFUF combinadas) ---
    print("\n[4/4] Ejecutando SQLMAP...")
    
    # [MEJORA] Refrescar la cookie de sesión antes de SQLMap
    # porque el escaneo activo de ZAP tarda mucho y la sesión de la víctima pudo haber expirado.
    if cookies is not None:
        print("    [*] Refrescando sesión para SQLMap (evitando caducidad por inactividad)...")
        nuevas_cookies = establecer_sesion_automatica(target_url)
        if nuevas_cookies:
            cookies = nuevas_cookies
            print(f"    [+] Sesión refrescada con éxito. Nueva Cookie: {cookies}")
        else:
            print("    [-] Falló el refresco de sesión. Usando cookie anterior o modo anónimo.")

    lista_urls_spider = spider_urls.get("results", [])
    # Combinar todas las rutas (SQLMap filtrará internamente por ? o .php)
    lista_urls_ffuf   = [r.get("url", "") for r in rutas_ffuf_nuevas]
    lista_urls_total  = list(set(lista_urls_spider + lista_urls_ffuf))  # sin duplicados
    sqlmap_raw = run_sqlmap_batch(lista_urls_total, cookies=cookies, proxy=None, sqlmap_level=sqlmap_level, scan_id=scan_id)
    
    # --- 4. CONSOLIDACIÓN Y REPORTE FINAL ---
    print("\nGenerando paquete de datos crudos...")
    
    hallazgos_finales = {
        "target": target_url,
        "spider_raw": spider_urls,
        "zap_raw": reporte_zap_crudo,  # Datos crudos de ZAP
        "sqlmap_raw": sqlmap_raw,      # Datos crudos de SQLMap
        "ffuf_raw": ffuf_data,         # Datos crudos de FFUF
        "ffuf_cache_info": ffuf_raw.get("cache_info"),  # Info de caché de FFUF (palabras testeadas/omitidas)
        "sqlmap_level": sqlmap_level   # Nivel de SQLMap usado (basic/fast_evidence/full_dump), para saber qué esperar de tablas
    }
    
    print(f"--- Ejecución finalizada. Datos crudos retornados en memoria ---")
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

    # NOTA: acá NO se intenta leer sqlmap_bg.log ni tablas_extraidas. En este punto
    # SQLMap recién se lanzó en segundo plano (run_sqlmap_batch ya volvió) así que el
    # log todavía no tiene resultados reales, o peor, puede tener los de una corrida
    # anterior (es un archivo único, no por scan_id). Los hallazgos y tablas reales de
    # SQLMap se completan después, de forma asíncrona, en consolidate_sqlmap.py cuando
    # el proceso en segundo plano termina, y ese es el que actualiza la base de datos
    # y regenera reporte_seguridad.md con la información correcta de esta corrida.

    #Consolidar los 3 resultados en una sola lista sin duplicados
    resultados_unificados = consolidar_resultados(spider_parseado, zap_parseado, ffuf_parseado, sqlmap_parseado)

    # Caché general del escaneo: NO es algo específico de SQLMap. FFUF también cachea
    # palabras ya probadas por wordlist, y SQLMap cachea URLs ya probadas y no
    # vulnerables. ZAP (Spider + Active Scan) no usa caché: siempre corre completo.
    # Se calcula todo de forma síncrona (antes de lanzar SQLMap en segundo plano), así
    # que ya está disponible acá.
    sqlmap_cache_info = None
    if isinstance(sqlmap_crudo, list) and len(sqlmap_crudo) > 0 and isinstance(sqlmap_crudo[0], dict):
        sqlmap_cache_info = sqlmap_crudo[0].get("cache_info")

    resultados_unificados["cache_info"] = {
        "ffuf": resultado_escaneo.get("ffuf_cache_info"),
        "sqlmap": sqlmap_cache_info
    }

    # Nivel de SQLMap usado en este análisis (basic/fast_evidence/full_dump). El
    # frontend lo necesita para explicar por qué no hay tablas: puede ser que no se
    # haya testeado nada nuevo (caché), o que el nivel elegido directamente no
    # extraiga tablas (solo "full_dump" hace --dump).
    resultados_unificados["sqlmap_level"] = resultado_escaneo.get("sqlmap_level")

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