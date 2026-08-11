# app/scanners/zap.py

import time
import requests

from app.config import settings

ZAP_HOST = settings.ZAP_HOST
ZAP_PORT = settings.ZAP_PORT
API_KEY = settings.ZAP_API_KEY


def _zap_get(url: str, params: dict = None, timeout: int = 15) -> requests.Response:
    """Realiza peticiones GET a ZAP con lógica de reintentos para fallos transitorios."""
    max_retries = 3
    retry_delay = 1.0
    for i in range(max_retries):
        try:
            return requests.get(url, params=params, timeout=timeout)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if i < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
                continue
            raise e


def configurar_autenticacion(cookies: str) -> None:
    """
    Agrega reglas en el Replacer de ZAP para inyectar 
    las cookies de sesión en todas las peticiones (Spider y Active Scan).
    """
    # Remover las reglas si ya existen de un escaneo previo
    url_remove = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/replacer/action/removeRule/"
    try:
        _zap_get(url_remove, params={"apikey": API_KEY, "description": "OrquestadorGlobalCookie"})
        _zap_get(url_remove, params={"apikey": API_KEY, "description": "OrquestadorGlobalCookieAdd"})
    except requests.exceptions.RequestException:
        pass

    # Regla 1: Reemplazar el header Cookie si ya existe en la petición
    url_add = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/replacer/action/addRule/"
    params_replace = {
        "apikey": API_KEY,
        "description": "OrquestadorGlobalCookie",
        "enabled": "true",
        "matchType": "REQ_HEADER",
        "matchRegex": "false",
        "matchString": "Cookie",
        "replacement": cookies
    }
    try:
        _zap_get(url_add, params=params_replace).raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"    [ZAP] Error configurando regla de reemplazo: {e}")

    # Regla 2: Agregar el header Cookie si NO existe en la petición (ej: primera petición del Spider)
    params_add = {
        "apikey": API_KEY,
        "description": "OrquestadorGlobalCookieAdd",
        "enabled": "true",
        "matchType": "REQ_HEADER_ADD",
        "matchRegex": "false",
        "matchString": "Cookie",
        "replacement": cookies
    }
    try:
        _zap_get(url_add, params=params_add).raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"    [ZAP] Error configurando regla de adición: {e}")


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

    response = _zap_get(url, params=params)
    response.raise_for_status()

    return response.json().get("scan")


def esperar_spider(scan_id: str, progress_callback=None) -> None:
    """
    Espera hasta que el spider llegue a 100%.
    No interpreta resultados.
    """
    url = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/spider/view/status/"

    while True:
        response = _zap_get(url, params={
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

    response = _zap_get(url, params={
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
    _zap_get(f"{base_opt}/setOptionAttackStrength/", params={"apikey": API_KEY, "strength": "LOW"})
    _zap_get(f"{base_opt}/setOptionAlertThreshold/", params={"apikey": API_KEY, "threshold": "MEDIUM"})

    # Optimización 2: Aumentar la cantidad de hilos/peticiones concurrentes (por defecto 2, lo subimos a 20)
    _zap_get(f"{base_opt}/setOptionThreadPerHost/", params={"apikey": API_KEY, "Integer": 20})
    
    # Optimización 3: Limitar a 1 minuto máximo el tiempo que ZAP se queda intentando validar UNA variante
    _zap_get(f"{base_opt}/setOptionMaxRuleDurationInMins/", params={"apikey": API_KEY, "Integer": 1})
    
    # Optimización 4: Limitar a 10 minutos máximo el ACTIVE SCAN completo para evitar que quede colgado
    _zap_get(f"{base_opt}/setOptionMaxScanDurationInMins/", params={"apikey": API_KEY, "Integer": 10})

    # Optimización 5: Desactivar la validación y busqueda agresiva de tokens CSRF (ahorra mucho tiempo)
    _zap_get(f"{base_opt}/setOptionHandleAntiCSRFTokens/", params={"apikey": API_KEY, "Boolean": "false"})

    url = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/ascan/action/scan/"
    params = {
        "apikey": API_KEY,
        "url": target_url,
        "recurse": "true"  # Escanea recursivamente lo encontrado por el spider
    }

    response = _zap_get(url, params=params)
    response.raise_for_status()

    return response.json().get("scan")


def esperar_escaneo_activo(scan_id: str, progress_callback=None) -> None:
    """
    Espera hasta que el escaneo activo llegue a 100%.
    """
    url = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/ascan/view/status/"

    while True:
        response = _zap_get(url, params={"apikey": API_KEY, "scanId": scan_id})
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

    response = _zap_get(url, params={"apikey": API_KEY})
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
            _zap_get(url_access, params={
                "apikey": API_KEY,
                "url": ruta,
                "followRedirects": "true"
            }, timeout=5)
        except requests.exceptions.RequestException:
            # Si una URL falla (timeout, 404, etc.) simplemente se ignora
            pass

    print(f"    [ZAP] Rutas inyectadas. El Active Scan las incluirá en su ataque.")


def abortar_escaneos_zap() -> None:
    """
    Detiene de manera forzada todas las arañas y escaneos activos en ZAP.
    """
    print("    [ZAP] Deteniendo escaneos/arañas activos para liberar recursos...")
    
    # 1. Detener Active Scan
    url_stop_ascan = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/ascan/action/stopAllScans/"
    try:
        _zap_get(url_stop_ascan, params={"apikey": API_KEY}, timeout=5)
    except Exception:
        pass

    # 2. Detener Spider
    url_stop_spider = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/spider/action/stopAllScans/"
    try:
        _zap_get(url_stop_spider, params={"apikey": API_KEY}, timeout=5)
    except Exception:
        pass


def limpiar_sesion_zap() -> None:
    """
    Inicia una nueva sesión en ZAP, borrando todo el historial, 
    árbol de sitios y alertas previas.
    """
    abortar_escaneos_zap()
    
    url = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/core/action/newSession/"
    try:
        _zap_get(url, params={"apikey": API_KEY, "overwrite": "true"})
    except requests.exceptions.RequestException as e:
        print(f"    [ZAP] Error limpiando sesión: {e}")
