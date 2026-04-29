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
from app.parsers.ffuf_parser import parsear_ffuf
from app.parsers.zap_parser import parsear_spider, parsear_zap
from app.parsers.sqlmap_parser import parsear_sqlmap
from app.utils.results import consolidar_resultados 

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
    
    # Limpiar ZAP de ejecuciones anteriores para que no se filtre basura de otros targets
    # --- 0. LOGIN AUTOMÁTICO (DVWA) ---
    print(f"[*] Iniciando sesión automática en {target_url}...")
    session = requests.Session()
    # Forzar un User-Agent de navegador real
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    })
    
    try:
        # 1. Obtener token de login (user_token)
        login_url = f"{target_url.rstrip('/')}/login.php"
        r = session.get(login_url)
        import re
        token_match = re.search(r"name='user_token' value='(.*?)'", r.text)
        user_token = token_match.group(1) if token_match else ""
        
        # 2. Hacer POST de login
        data = {
            "username": "admin",
            "password": "password",
            "Login": "Login",
            "user_token": user_token
        }
        session.post(login_url, data=data)
        
        # 3. Forzar nivel de seguridad a 'low'
        security_url = f"{target_url.rstrip('/')}/security.php"
        # Obtener nuevo token
        r = session.get(security_url)
        token_match = re.search(r"name='user_token' value='(.*?)'", r.text)
        sec_token = token_match.group(1) if token_match else ""
        
        session.post(security_url, data={
            "security": "low",
            "seclev_submit": "Submit",
            "user_token": sec_token
        })
        
        # Extraer las cookies finales
        cookies_dict = session.cookies.get_dict()
        cookies = "; ".join([f"{k}={v}" for k, v in cookies_dict.items()])
        if "security" not in cookies:
            cookies += "; security=low"
            
        print(f" [+] Sesión establecida automáticamente. Cookie: {cookies}")
        
    except Exception as e:
        print(f" [!] Error en login automático: {e}")
        # Si falla el login automático, seguimos con las cookies manuales si existen

    print("Limpiando sesión previa de ZAP...")
    limpiar_sesion_zap()
    
    # --- Configuración Autenticación Global (ZAP) ---
    if cookies:
        configurar_autenticacion(cookies)
        
        # [VALIDACIÓN] Verificar si la sesión permite entrar a las carpetas vulnerables
        print(f"[*] Validando acceso a rutas protegidas en {target_url}...")
        try:
            test_url = f"{target_url.rstrip('/')}/vulnerabilities/sqli/"
            # Usamos un User-Agent fijo para coincidir con SQLMap
            headers = {
                'Cookie': cookies,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
            }
            r = requests.get(test_url, headers=headers, allow_redirects=True, timeout=10)
            if "login.php" in r.url or "Login" in r.text:
                print(f" [!] ALERTA: La sesión ha EXPIRADO o es INVÁLIDA.")
                print(f" [!] Contenido detectado: {r.text[:100]}...")
                print(" [!] El servidor te redirigió al login. Por favor, obtené una cookie fresca.")
                return # Frenamos el escaneo si la sesión no sirve
            elif r.status_code == 200:
                print(" [+] Sesión VALIDADA exitosamente para rutas protegidas.")
                import re
                title_match = re.search(r'<title>(.*?)</title>', r.text, re.IGNORECASE)
                title = title_match.group(1) if title_match else "Sin título"
                print(f" [+] Título de la página: {title}")
                if "Login" in title:
                    print(" [!] ALERTA: La sesión es válida pero estás en la página de LOGIN.")
                    return
                body_preview = r.text[:150].replace('\n', ' ')
                print(f" [+] Debug Body: {body_preview}...")
            else:
                print(f" [?] Respuesta inesperada en validación: {r.status_code}")
        except Exception as e:
            print(f" [!] Error durante validación de sesión: {e}")
    
    # --- 1. FFUF ---
    print("\n[1/4] Ejecutando FFUF...")
    
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
    
    # Leer los datos crudos de FFUF para incluirlos en el reporte final
    # (run_ffuf guarda el archivo y aquí lo leemos para consolidarlo)
    ffuf_data = {}
    rutas_ffuf_nuevas = []
    if os.path.exists(ffuf_raw["output_file"]):
        with open(ffuf_raw["output_file"], "r") as f:
            try:
                ffuf_data = json.load(f)
                rutas_ffuf_nuevas = ffuf_data.get("results", [])
                if rutas_ffuf_nuevas and isinstance(rutas_ffuf_nuevas[0], dict) and "url" not in rutas_ffuf_nuevas[0]:
                    rutas_ffuf_nuevas = [{"url": r.get("url", "")} for r in rutas_ffuf_nuevas]
            except json.JSONDecodeError:
                print("Advertencia: No se pudo leer el JSON crudo de FFUF.")

    # --- 2. INYECTAR RUTAS DE FFUF EN ZAP (antes del Spider) ---
    if rutas_ffuf_nuevas:
        print(f"\n[1/4-pre] Inyectando {len(rutas_ffuf_nuevas)} rutas de FFUF en ZAP...")
        agregar_urls_a_zap(rutas_ffuf_nuevas)
    else:
        print("\n[1/4-pre] Sin rutas nuevas de FFUF para inyectar en ZAP.")

    # --- 3. ZAP SPIDER ---
    print("\n[2/4] Ejecutando ZAP Spider...")
    
    # Cebamos ZAP con la URL principal para que el Spider empiece logueado
    if cookies:
        print(f"    [ZAP] Cebando sitio con cookies para acceso autenticado...")
        agregar_urls_a_zap([{"url": target_url}])

    # 3.1 Spider en la URL principal
    spider_id = iniciar_spider(target_url)
    esperar_spider(spider_id)
    spider_urls_dict = obtener_urls(spider_id)
    todas_urls_spider = spider_urls_dict.get("results", [])
    
    # 3.2 Spider en las puertas ocultas descubiertas por FFUF
    if rutas_ffuf_nuevas:
        print("    [ZAP] Lanzando Spider en las rutas ocultas para mapeo profundo...")
        for item in rutas_ffuf_nuevas:
            ruta = item.get("url", "")
            # Evitamos spiderar la raiz de nuevo si FFUF la devolvió
            if ruta and ruta.strip("/") != target_url.strip("/"):
                print(f"    [ZAP] Spidering ruta oculta: {ruta}")
                s_id = iniciar_spider(ruta)
                esperar_spider(s_id)
                s_urls = obtener_urls(s_id)
                todas_urls_spider.extend(s_urls.get("results", []))
                
    # Reconstruimos la estructura que espera el resto del código (removiendo duplicados)
    spider_urls = {"results": list(set(todas_urls_spider))}

    # --- 4. ZAP ACTIVE SCAN ---
    print("\n[3/4] Ejecutando ZAP Active Scan...")
    ascan_id = iniciar_escaneo_activo(target_url)
    esperar_escaneo_activo(ascan_id)
    
    # Obtener reporte crudo de ZAP (se mantiene en memoria para el reporte final)
    reporte_zap_crudo = obtener_reporte_json()

    # --- 5. SQLMAP ---
    print("\n[4/4] Ejecutando SQLMAP...")
    lista_urls_spider = spider_urls.get("results", [])
    # Combinar con las rutas de FFUF que tengan parámetros (?
    lista_urls_ffuf   = [r.get("url", "") for r in rutas_ffuf_nuevas if "?" in r.get("url", "")]
    
    # [SEMBRADO] Rutas críticas de DVWA que a veces el spider se salta
    rutas_semilla = [
        f"{target_url}/vulnerabilities/sqli/?id=1&Submit=Submit",
        f"{target_url}/vulnerabilities/sqli_blind/?id=1&Submit=Submit",
        f"{target_url}/vulnerabilities/fi/?page=include.php",
        f"{target_url}/vulnerabilities/exec/"
    ]
    
    lista_urls_total  = list(set(lista_urls_spider + lista_urls_ffuf + rutas_semilla))  # sin duplicados
    sqlmap_raw = run_sqlmap_batch(lista_urls_total, cookies=cookies)
    
    # --- 5. CONSOLIDACIÓN Y REPORTE FINAL ---
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



    #docker exec -it security-app sh