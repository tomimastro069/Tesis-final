# app/scanners/sqlmap.py

from app.runners.exec import run_command
from app.db.database import is_url_tested_in_sqlmap, save_tested_sqlmap_url, get_vulnerable_urls

from app.config import settings

# Ruta donde se clonó sqlmap dentro del contenedor
SQLMAP_PATH = settings.SQLMAP_PATH


def filtrar_urls_con_parametros(urls: list) -> list:
    """
    Filtra y prioriza URLs para SQLMap.

    Orden de prioridad:
    1. URLs con parámetros GET ('?') — las más probables de ser vulnerables
       (excluye paths de configuración/estáticos que no son SQLi targets)
    2. Páginas .php de input interactivo sin params (para --forms)
       Solo incluye paths que sugieran formularios de usuario: login, sqli, brute, upload, etc.
       Excluye páginas estáticas: instructions, about, setup, phpinfo, etc.
    """
    PATHS_INTERACTIVOS = ["sqli", "login", "brute", "upload", "csrf", "xss_r", "xss_s", "exec"]
    PATHS_EXCLUIDOS = [
        "instructions", "about", "setup", "phpinfo", "logout",
        "config", "ids_log", "security.php", "phpids","login.php"
    ]

    def no_excluida(url: str) -> bool:
        return not any(p in url.lower() for p in PATHS_EXCLUIDOS)

    con_params = [u for u in urls if "?" in u and no_excluida(u)]

    sin_params_interactivos = [
        u for u in urls
        if "?" not in u
        and any(ext in u.lower() for ext in [".php", ".php7", ".asp", ".aspx", ".jsp"])
        and any(p in u.lower() for p in PATHS_INTERACTIVOS)
        and no_excluida(u)
    ]

    # Primero las que tienen params, luego las interactivas sin params
    return con_params + sin_params_interactivos


def run_sqlmap(url: str, timeout: int = settings.SQLMAP_TIMEOUT, cookies: str = None, proxy: str = None, sqlmap_level: str = "basic") -> dict:
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
    # Comando SQLMap Optimizado
    # --batch        → modo automático, no pide confirmaciones al usuario
    # --random-agent → usa un User-Agent aleatorio (para no ser detectado)
    # --level=2      → nivel de profundidad de pruebas (1-5, 2 es moderado)
    # --risk=2       → nivel de riesgo de los payloads (1-3, 2 es moderado)
    # NOTA: --smart fue removido intencionalmente. En DVWA las responses básicas son
    # idénticas ante cualquier input → la heurística previa descarta el param silenciosamente.
    # --threads=5    → 5 hilos paralelos
    # -o             → Activa Keep-Alive, Null connection y otros aceleradores HTTP internos.
    # --technique=BEUST → Todas las técnicas: Boolean, Error, Union, Stacked, Time
    # Construcción base del comando
    cmd = [
        "python3", SQLMAP_PATH,
        "-u", url,
        "--batch",
        "--flush-session",   # Evitar que SQLMap recicle escaneos anteriores en su propia caché
        "--forms",           # Ataca formularios POST también
        "--dbms=MySQL",      # Optimizado para DVWA
        "--level=3",         # Nivel de profundidad 3
        "--risk=3",          # Riesgo máximo
        "--threads=5",       # 5 hilos paralelos
        "--technique=BEUST", # Todas las técnicas: Boolean, Error, Union, Stacked, Time
        "-o"
    ]
    
    # Agregar banderas de enumeración según el nivel solicitado
    if sqlmap_level == "fast_evidence":
        cmd.extend(["--dbs", "--current-user"])
    elif sqlmap_level == "full_dump":
        cmd.append("--dump")
    
    # Agregar Proxy solo si se define
    if proxy:
        cmd.extend(["--proxy", proxy])
    
    # Agregar Cookies si existen
    if cookies:
        cmd.extend(["--cookie", cookies])
    
    # Usar un User-Agent fijo y real para no romper la sesión de DVWA
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    cmd.extend(["--user-agent", ua])

    result = run_command(cmd, timeout=timeout)

    return {
        "url": url,
        "stdout": result.get("stdout", ""),
        "stderr": result.get("stderr", ""),
        "success": result.get("success", False),
        "timeout": result.get("timeout", False)
    }


def run_sqlmap_batch(urls: list, timeout: int = settings.SQLMAP_TIMEOUT, cookies: str = None, proxy: str = None, sqlmap_level: str = "basic", progress_callback=None) -> list:
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

    # Paso 2: Separar URLs en: a re-testear (vulnerables conocidas) y nuevas vs cacheadas
    resultados = []
    urls_a_escanear = []
    vulnerable_conocidas = get_vulnerable_urls()
    
    for url in urls_con_params:
        if url in vulnerable_conocidas:
            print(f"    [⚠ RETEST] {url} fue vulnerable antes → re-testeando siempre")
            urls_a_escanear.append(url)
        elif is_url_tested_in_sqlmap(url):
            print(f"    [CACHE] Omitiendo {url} (ya analizada y sin vulnerabilidades previas)")
        else:
            urls_a_escanear.append(url)

    if not urls_a_escanear:
        print("    [SQLMAP] Escaneo omitido: todas las URLs ya fueron analizadas.")
        return []

    print(f"    Iniciando escaneo real en {len(urls_a_escanear)} URLs...")

    for i, url in enumerate(urls_a_escanear, 1):
        if progress_callback: progress_callback((i - 1) / len(urls_a_escanear) * 100, f"Testeando: {url}")
        print(f"    [{i}/{len(urls_a_escanear)}] Testeando: {url}")
        resultado = run_sqlmap(url, timeout=timeout, cookies=cookies, proxy=proxy, sqlmap_level=sqlmap_level)
        resultados.append(resultado)
        
        # Solo guardar en caché si no es una URL vulnerable (las vulnerables siempre se re-testean)
        if url not in vulnerable_conocidas:
            save_tested_sqlmap_url(url)

    if progress_callback: progress_callback(100, "SQLMap finalizado.")
    return resultados