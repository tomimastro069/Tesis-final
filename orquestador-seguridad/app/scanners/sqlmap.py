# app/scanners/sqlmap.py

from app.runners.exec import run_command


from app.config import settings

# Ruta donde se clonó sqlmap dentro del contenedor
SQLMAP_PATH = settings.SQLMAP_PATH


def filtrar_urls_con_parametros(urls: list) -> list:
    """
    Filtra una lista de URLs para SQLMap.
    Ahora incluimos:
    1. URLs con parámetros GET ('?')
    2. Archivos dinámicos (.php) para que SQLMap busque formularios (--forms)
    """
    extensiones_interesantes = [".php", ".php7", ".asp", ".aspx", ".jsp"]
    return [
        url for url in urls 
        if "?" in url or any(ext in url.lower() for ext in extensiones_interesantes)
    ]


def run_sqlmap(url: str, timeout: int = settings.SQLMAP_TIMEOUT, cookies: str = None, proxy: str = None) -> dict:
    """
    Ejecuta SQLMap contra UNA URL que tenga parámetros GET.

    SQLMap va a probar si los parámetros de esa URL son vulnerables
    a inyección SQL. Por ejemplo, si la URL es:
        http://dvwa/vulnerabilities/sqli/?id=1
    SQLMap prueba cosas como:
        ?id=1' OR '1'='1
        ?id=1 UNION SELECT ...
    Y después te dice si el parámetro 'id' es vulnerable o no.

    Args:
        url (str): URL con parámetros (debe tener '?').
        timeout (int): Tiempo máximo en segundos (default 5 minutos,
                       porque SQLMap puede tardar bastante).

    Returns:
        dict: {
            'url': str,          # la URL que se testeó
            'stdout': str,       # salida cruda de sqlmap (texto)
            'stderr': str,       # errores si hubo
            'success': bool,     # si el comando terminó bien
            'timeout': bool      # si se pasó del tiempo límite
        }
    """
    # Comando SQLMap optimizado para velocidad
    # --batch        → modo automático
    # --random-agent → evita bloqueos por User-Agent
    # --forms        → busca formularios POST
    # --level=2      → nivel intermedio (suficiente para la mayoría)
    # --risk=1       → riesgo bajo (evita payloads pesados/destructivos)
    # --smart        → ¡CLAVE! Solo testea a fondo si hay indicios de vulnerabilidad
    # --threads=5     → velocidad en paralelo
    # --dbms=MySQL   → directo al motor de DVWA
    cmd = [
        "python3", SQLMAP_PATH,
        "-u", url,
        "--batch",
        "--proxy", proxy if proxy else "",
        "--random-agent", # Ya no importa tanto porque ZAP lo va a reemplazar, pero por si acaso
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "--level=3",
        "--risk=2",
        "--threads=5",
        "--dbms=MySQL",
        "--flush-session",
        "--drop-set-cookie",   # Mantenemos esto para que no nos pisen la sesión
        # Cabeceras para mimetizar un navegador al 100%
        "--header=Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "--header=Connection: keep-alive",
        "--header=Upgrade-Insecure-Requests: 1",
        f"--referer={url.split('?')[0]}", 
    ]
    
    if cookies:
        # Asegurar espacio después de ; para compatibilidad con PHP
        cookies_clean = cookies.replace(";", "; ").replace("  ", " ")
        cmd.extend(["--cookie", cookies_clean])

    # Ejecutar usando el mismo runner que ffuf
    result = run_command(cmd, timeout=timeout)

    return {
        "url": url,
        "stdout": result.get("stdout", ""),
        "stderr": result.get("stderr", ""),
        "success": result.get("success", False),
        "timeout": result.get("timeout", False)
    }


def run_sqlmap_batch(urls: list, timeout: int = settings.SQLMAP_TIMEOUT, cookies: str = None, proxy: str = None) -> list:
    """
    Ejecuta SQLMap contra TODAS las URLs que tengan parámetros.

    Esta función:
    1. Recibe la lista completa de URLs (del spider)
    2. Filtra solo las que tienen '?'
    3. Ejecuta SQLMap en cada una
    4. Devuelve una lista con todos los resultados

    Args:
        urls (list): Lista de URLs (pueden tener o no parámetros).
        timeout (int): Timeout por cada URL individual.

    Returns:
        list: Lista de dicts, uno por cada URL testeada.
              Si no hay URLs con parámetros, devuelve lista vacía.
    """
    # Paso 1: Filtrar solo URLs con parámetros
    urls_con_params = filtrar_urls_con_parametros(urls)

    if not urls_con_params:
        print("    No se encontraron URLs con parámetros para SQLMap.")
        return []

    print(f"    Se encontraron {len(urls_con_params)} URLs con parámetros.")

    # Paso 2: Ejecutar SQLMap en cada URL
    resultados = []
    for i, url in enumerate(urls_con_params, 1):
        print(f"    [{i}/{len(urls_con_params)}] Testeando: {url}")
        resultado = run_sqlmap(url, timeout=timeout, cookies=cookies, proxy=proxy)
        resultados.append(resultado)

    return resultados