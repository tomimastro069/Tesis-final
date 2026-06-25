# app/scanners/zap.py

import time
import requests

from app.config import settings

ZAP_HOST = settings.ZAP_HOST
ZAP_PORT = settings.ZAP_PORT
API_KEY = settings.ZAP_API_KEY


def configurar_autenticacion(cookies: str) -> None:
    """
    Agrega una regla en el Replacer de ZAP para inyectar 
    las cookies de sesión en todas las peticiones (Spider y Active Scan).
    """
    # Remover la regla si ya existe de un escaneo previo
    url_remove = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/replacer/action/removeRule/"
    try:
        requests.get(url_remove, params={"apikey": API_KEY, "description": "OrquestadorGlobalCookie"})
    except requests.exceptions.RequestException:
        pass

    url = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/replacer/action/addRule/"
    params = {
        "apikey": API_KEY,
        "description": "OrquestadorGlobalCookie",
        "enabled": "true",
        "matchType": "REQ_HEADER",
        "matchRegex": "false",
        "matchString": "Cookie",
        "replacement": cookies
    }
    response = requests.get(url, params=params)
    response.raise_for_status()


def iniciar_spider(target_url: str) -> str:
    """
    Inicia el spider en ZAP.
    Devuelve el scan_id.
    """
    url = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/spider/action/scan/"
    params = {
        "apikey": API_KEY,
        "url": target_url
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json().get("scan")


def esperar_spider(scan_id: str, progress_callback=None) -> None:
    """
    Espera hasta que el spider llegue a 100%.
    No interpreta resultados.
    """
    url = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/spider/view/status/"

    while True:
        response = requests.get(url, params={
            "apikey": API_KEY,
            "scanId": scan_id
        })

        response.raise_for_status()

        status = int(response.json().get("status", 0))
        if progress_callback:
            progress_callback(status)

        if status >= 100:
            break

        time.sleep(2)


def obtener_urls(scan_id: str) -> dict:
    """
    Obtiene las URLs encontradas por el spider.
    Devuelve el JSON crudo.
    """
    url = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/spider/view/results/"

    response = requests.get(url, params={
        "apikey": API_KEY,
        "scanId": scan_id
    })

    response.raise_for_status()

    return response.json()


def iniciar_escaneo_activo(target_url: str) -> str:
    """
    Inicia el escaneo activo (Active Scan) en ZAP.
    Devuelve el scan_id.
    """
    # Si la URL es raiz (ej: http://dvwa), agregamos / al final
    # para asegurar que coincida con el nodo en el arbol de ZAP.
    if target_url.count("/") == 2 and "?" not in target_url:
        target_url += "/"

    base_opt = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/ascan/action"
    # Optimización 1: Reducir fuerza y umbral para menor carga
    requests.get(f"{base_opt}/setOptionAttackStrength/", params={"apikey": API_KEY, "strength": "LOW"})
    requests.get(f"{base_opt}/setOptionAlertThreshold/", params={"apikey": API_KEY, "threshold": "MEDIUM"})

    # Optimización 2: Aumentar la cantidad de hilos/peticiones concurrentes (por defecto 2, lo subimos a 20)
    requests.get(f"{base_opt}/setOptionThreadPerHost/", params={"apikey": API_KEY, "Integer": 20})
    
    # Optimización 3: Limitar a 1 minuto máximo el tiempo que ZAP se queda intentando validar UNA variante
    requests.get(f"{base_opt}/setOptionMaxRuleDurationInMins/", params={"apikey": API_KEY, "Integer": 1})
    
    # Optimización 4: Limitar a 10 minutos máximo el ACTIVE SCAN completo para evitar que quede colgado
    requests.get(f"{base_opt}/setOptionMaxScanDurationInMins/", params={"apikey": API_KEY, "Integer": 10})

    # Optimización 5: Desactivar la validación y busqueda agresiva de tokens CSRF (ahorra mucho tiempo)
    requests.get(f"{base_opt}/setOptionHandleAntiCSRFTokens/", params={"apikey": API_KEY, "Boolean": "false"})

    url = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/ascan/action/scan/"
    params = {
        "apikey": API_KEY,
        "url": target_url,
        "recurse": "true"  # Escanea recursivamente lo encontrado por el spider
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json().get("scan")


def esperar_escaneo_activo(scan_id: str, progress_callback=None) -> None:
    """
    Espera hasta que el escaneo activo llegue a 100%.
    """
    url = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/ascan/view/status/"

    while True:
        response = requests.get(url, params={"apikey": API_KEY, "scanId": scan_id})
        response.raise_for_status()
        status = int(response.json().get("status", 0))
        print(f"Progreso escaneo activo: {status}%")
        if progress_callback:
            progress_callback(status)

        if status >= 100:
            break
        time.sleep(5)  # El escaneo activo es más lento, esperamos 5s


def obtener_reporte_json() -> dict:
    """
    Obtiene el reporte completo en formato JSON.
    Este endpoint (/OTHER/core/other/jsonreport/) devuelve la estructura
    completa (site, alerts) que tu parser espera.
    """
    url = f"http://{ZAP_HOST}:{ZAP_PORT}/OTHER/core/other/jsonreport/"

    response = requests.get(url, params={"apikey": API_KEY})
    response.raise_for_status()

    return response.json()


def agregar_urls_a_zap(rutas_ffuf: list) -> None:
    """
    Inyecta en el árbol interno de ZAP las URLs descubiertas por FFUF
    para que el Active Scan posterior también las ataque.

    FFUF descubre rutas que el Spider de ZAP no puede encontrar (fuerza bruta
    de diccionario vs. crawling de links). Sin esta función, el Active Scan
    solo ataca lo que el Spider vio. Con ella, todas las rutas nuevas de FFUF
    quedan registradas en el contexto de ZAP antes del ataque.

    Args:
        rutas_ffuf (list): Lista de dicts con clave 'url', tal como devuelve
                           el parser de FFUF. Ej: [{"url": "http://dvwa/admin/"}]
    """
    url_access = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/core/action/accessUrl/"

    total = len(rutas_ffuf)
    if total == 0:
        return

    print(f"    [ZAP] Inyectando {total} rutas de FFUF en el árbol de ZAP...")

    for item in rutas_ffuf:
        ruta = item.get("url", "")
        if not ruta:
            continue
        try:
            requests.get(url_access, params={
                "apikey": API_KEY,
                "url": ruta,
                "followRedirects": "true"
            }, timeout=5)
        except requests.exceptions.RequestException:
            # Si una URL falla (timeout, 404, etc.) simplemente se ignora
            pass

    print(f"    [ZAP] Rutas inyectadas. El Active Scan las incluirá en su ataque.")


def limpiar_sesion_zap() -> None:
    """
    Inicia una nueva sesión en ZAP, borrando todo el historial, 
    árbol de sitios y alertas previas.
    """
    url = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/core/action/newSession/"
    try:
        requests.get(url, params={"apikey": API_KEY, "overwrite": "true"})
    except requests.exceptions.RequestException as e:
        print(f"    [ZAP] Error limpiando sesión: {e}")
