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
        "--level=1",         # Nivel de profundidad 1 (suficiente para parámetros GET/POST y evita testear cookies)
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


def run_sqlmap_batch(urls: list, timeout: int = settings.SQLMAP_TIMEOUT, cookies: str = None, proxy: str = None, sqlmap_level: str = "basic") -> list:
    """
    Ejecuta SQLMap en SEGUNDO PLANO contra TODAS las URLs que tengan parámetros.
    Genera un script bash y lo lanza como proceso asíncrono para no bloquear el pipeline.
    """
    import os
    import stat
    import subprocess
    
    # Paso 1: Filtrar solo URLs con parámetros
    urls_con_params = filtrar_urls_con_parametros(urls)

    if not urls_con_params:
        print("    No se encontraron URLs con parámetros para SQLMap.")
        return []

    print(f"    Se encontraron {len(urls_con_params)} URLs con parámetros.")

    # Paso 2: Separar URLs en: a re-testear (vulnerables conocidas) y nuevas vs cacheadas
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

    print(f"    Generando script para escaneo en segundo plano de {len(urls_a_escanear)} URLs...")

    script_path = os.path.join(settings.OUTPUT_DIR, "run_sqlmap_bg.sh")
    log_path = os.path.join(settings.OUTPUT_DIR, "sqlmap_bg.log")
    
    with open(script_path, "w", encoding="utf-8") as f:
        f.write("#!/bin/bash\n\n")
        f.write(f"echo '--- Iniciando SQLMap en segundo plano ---' > {log_path}\n")
        
        for i, url in enumerate(urls_a_escanear, 1):
            cmd = [
                "python3", SQLMAP_PATH,
                "-u", f'"{url}"',
                "--batch",
                "--flush-session",
                "--forms",
                "--dbms=MySQL",
                "--level=1",
                "--risk=3",
                "--threads=5",
                "--technique=BEUST",
                "-o"
            ]
            if sqlmap_level == "fast_evidence":
                cmd.extend(["--dbs", "--current-user"])
            elif sqlmap_level == "full_dump":
                cmd.append("--dump")
            
            if proxy:
                cmd.extend(["--proxy", proxy])
            
            if cookies:
                cmd.extend(["--cookie", f'"{cookies}"'])
            
            ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            cmd.extend(["--user-agent", f'"{ua}"'])
            
            cmd_str = " ".join(cmd)
            f.write(f"echo '[{i}/{len(urls_a_escanear)}] Testeando: {url}' >> {log_path}\n")
            f.write(f"{cmd_str} >> {log_path} 2>&1\n")
            
            # Guardamos en caché para que no se repitan en futuras corridas
            if url not in vulnerable_conocidas:
                save_tested_sqlmap_url(url)
                
        f.write(f"echo '--- Escaneo finalizado ---' >> {log_path}\n")
        f.write(f"python3 -m app.workflow.consolidate_sqlmap >> {log_path} 2>&1\n")

    # Dar permisos de ejecución al script
    st = os.stat(script_path)
    os.chmod(script_path, st.st_mode | stat.S_IEXEC)
    
    # Ejecutar en segundo plano (detached)
    subprocess.Popen(["bash", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    
    print(f"    [+] SQLMap lanzado en segundo plano.")
    print(f"    [+] Para ver el progreso en vivo, abrí otra consola y ejecutá:")
    print(f"        docker exec -it security-app tail -f /app/output/raw/sqlmap_bg.log")

    # Retornamos un resultado simulado para que el pipeline no falle
    return [{
        "url": "BACKGROUND_EXECUTION",
        "stdout": "SQLMap ejecutándose en segundo plano. Revisar output/raw/sqlmap_bg.log",
        "stderr": "",
        "success": True,
        "timeout": False
    }]

    #docker exec -it security-app 
    #     tail -f /app/output/raw/sqlmap_bg.log
