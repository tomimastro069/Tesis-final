# app/scanners/sqlmap.py

from app.runners.exec import run_command
from app.db.database import is_url_tested_in_sqlmap, save_tested_sqlmap_url, get_vulnerable_urls

from app.config import settings

# Ruta donde se clonó sqlmap dentro del contenedor
SQLMAP_PATH = settings.SQLMAP_PATH


def filtrar_urls_con_parametros(urls: list) -> list:
    """
    Filtra una lista de URLs y devuelve solo las que tienen
    parámetros GET (contienen '?').

    SQLMap necesita parámetros para inyectar SQL.
    Sin '?' no tiene dónde probar.

    Ejemplo:
        Entrada: [
            "http://dvwa/login.php",
            "http://dvwa/vulnerabilities/sqli/?id=1",
            "http://dvwa/about.php"
        ]
        Salida: [
            "http://dvwa/vulnerabilities/sqli/?id=1"
        ]
    """
    return [url for url in urls if "?" in url]


def run_sqlmap(url: str, timeout: int = settings.SQLMAP_TIMEOUT, cookies: str = None) -> dict:
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
    # --smart        → [OPTIMIZACIÓN] Heurística previa: solo ataca parámetros que cambian el comportamiento del sitio (ahorra un 80% de tiempo).
    # --threads=10   → [OPTIMIZACIÓN] Dispara 10 hilos concurrentes en vez de 1 (límite máximo de sqlmap).
    # -o             → [OPTIMIZACIÓN] Activa Keep-Alive, Null connection y otros aceleradores HTTP internos.
    # --technique=BEUQ → [OPTIMIZACIÓN RADICAL] Prohíbe inyecciones basadas en tiempo ('T'). Evita que el servidor se quede "durmiendo" a propósito.
    cmd = [
        "python3", SQLMAP_PATH,
        "-u", url,
        "--batch",
        "--random-agent",
        "--level=2",
        "--risk=2",
        "--smart",
        "--threads=10",
        "-o",
        "--technique=BEUQ"
    ]
    
    if cookies:
        cmd.extend(["--cookie", cookies])

    result = run_command(cmd, timeout=timeout)

    return {
        "url": url,
        "stdout": result.get("stdout", ""),
        "stderr": result.get("stderr", ""),
        "success": result.get("success", False),
        "timeout": result.get("timeout", False)
    }


def run_sqlmap_batch(urls: list, timeout: int = settings.SQLMAP_TIMEOUT, cookies: str = None) -> list:
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
        print(f"    [{i}/{len(urls_a_escanear)}] Testeando: {url}")
        resultado = run_sqlmap(url, timeout=timeout, cookies=cookies)
        resultados.append(resultado)
        
        # Solo guardar en caché si no es una URL vulnerable (las vulnerables siempre se re-testean)
        if url not in vulnerable_conocidas:
            save_tested_sqlmap_url(url)

    return resultados