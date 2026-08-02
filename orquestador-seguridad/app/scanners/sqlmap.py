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


def _sqlmap_bg_en_curso(lock_path: str) -> bool:
    """
    Revisa si ya hay una corrida de SQLMap en segundo plano activa (lockfile con un
    PID que sigue vivo). run_sqlmap_bg.sh y sqlmap_bg.log son archivos únicos y
    globales (no separados por scan_id): si dos escaneos se solapan, el segundo
    pisaría el log/script del primero a mitad de camino y corromperia los
    resultados de AMBOS análisis. Evitamos eso acá en vez de arriesgar datos falsos.
    """
    import os

    if not os.path.exists(lock_path):
        return False

    try:
        with open(lock_path, "r", encoding="utf-8") as f:
            pid = int(f.read().strip())
        os.kill(pid, 0)  # No mata al proceso, solo chequea si existe
        return True
    except ProcessLookupError:
        # El PID ya no existe: lockfile viejo/huérfano de una corrida anterior que
        # no se limpió (por ejemplo, si el contenedor se reinició a mitad de camino).
        return False
    except (ValueError, OSError):
        # Lockfile corrupto o sin permisos para verificar: por las dudas, no
        # asumimos que está libre.
        return True


def run_sqlmap_batch(urls: list, timeout: int = settings.SQLMAP_TIMEOUT, cookies: str = None, proxy: str = None, sqlmap_level: str = "basic", scan_id: str = None) -> list:
    """
    Ejecuta SQLMap en SEGUNDO PLANO contra TODAS las URLs que tengan parámetros.
    Genera un script bash y lo lanza como proceso asíncrono para no bloquear el pipeline.
    """
    import os
    import stat
    import subprocess

    lock_path = os.path.join(settings.OUTPUT_DIR, "sqlmap_bg.lock")

    # Paso 1: Filtrar solo URLs con parámetros
    urls_con_params = filtrar_urls_con_parametros(urls)

    if not urls_con_params:
        print("    No se encontraron URLs con parámetros para SQLMap.")
        return []

    # Si ya hay otra corrida de SQLMap en segundo plano activa, no lanzamos una
    # segunda: compartirían el mismo log/script y se corromperían entre sí. Mejor
    # devolver explícitamente "no se testeó nada" que arriesgar datos mezclados.
    if _sqlmap_bg_en_curso(lock_path):
        print("    [!] Ya hay una corrida de SQLMap en segundo plano activa (de otro análisis). Se omite esta corrida para no corromper los resultados de ambas.")
        cache_info = {
            "total_candidatas": len(urls_con_params),
            "total_testeadas": 0,
            "omitidas_por_cache": [],
            "retesteadas_por_vulnerable_previa": [],
            "sqlmap_en_curso": True
        }
        return [{
            "url": "BACKGROUND_EXECUTION",
            "stdout": "Se omitió SQLMap: ya había otro análisis corriendo SQLMap en segundo plano al mismo tiempo. Ningún resultado de SQLMap de este análisis es real; esperá a que termine el otro análisis y volvé a escanear si necesitás confirmar SQL Injection.",
            "stderr": "",
            "success": True,
            "timeout": False,
            "cache_info": cache_info
        }]

    print(f"    Se encontraron {len(urls_con_params)} URLs con parámetros.")

    # Paso 2: Separar URLs en: a re-testear (vulnerables conocidas) y nuevas vs cacheadas
    urls_a_escanear = []
    urls_omitidas_por_cache = []
    urls_retesteadas_por_vulnerable = []
    vulnerable_conocidas = get_vulnerable_urls()

    for url in urls_con_params:
        if url in vulnerable_conocidas:
            print(f"    [⚠ RETEST] {url} fue vulnerable antes → re-testeando siempre")
            urls_a_escanear.append(url)
            urls_retesteadas_por_vulnerable.append(url)
        elif is_url_tested_in_sqlmap(url):
            print(f"    [CACHE] Omitiendo {url} (ya analizada y sin vulnerabilidades previas)")
            urls_omitidas_por_cache.append(url)
        else:
            urls_a_escanear.append(url)

    # Info de caché: se calcula siempre, se necesita para que el frontend sepa qué URLs
    # no se volvieron a probar en este análisis (aunque el escaneo termine vacío o completo).
    cache_info = {
        "total_candidatas": len(urls_con_params),
        "total_testeadas": len(urls_a_escanear),
        "omitidas_por_cache": urls_omitidas_por_cache,
        "retesteadas_por_vulnerable_previa": urls_retesteadas_por_vulnerable
    }

    if not urls_a_escanear:
        print("    [SQLMAP] Escaneo omitido: todas las URLs ya fueron analizadas.")
        return [{
            "url": "BACKGROUND_EXECUTION",
            "stdout": "Todas las URLs candidatas ya habían sido analizadas antes (caché) y no eran vulnerables. No se relanzó SQLMap.",
            "stderr": "",
            "success": True,
            "timeout": False,
            "cache_info": cache_info
        }]

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
        scan_id_arg = f' "{scan_id}"' if scan_id else ""
        f.write(f"python3 -m app.workflow.consolidate_sqlmap{scan_id_arg} >> {log_path} 2>&1\n")
        # Liberar el lock siempre al final, incluso si algo de arriba falló.
        f.write(f"rm -f {lock_path}\n")

    # Dar permisos de ejecución al script
    st = os.stat(script_path)
    os.chmod(script_path, st.st_mode | stat.S_IEXEC)

    # Ejecutar en segundo plano (detached) y guardar su PID en el lockfile para que
    # ningún otro análisis lo pise mientras esté corriendo.
    proc = subprocess.Popen(["bash", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    with open(lock_path, "w", encoding="utf-8") as f:
        f.write(str(proc.pid))

    print(f"    [+] SQLMap lanzado en segundo plano.")
    print(f"    [+] Para ver el progreso en vivo, abrí otra consola y ejecutá:")
    print(f"        docker exec -it security-app tail -f /app/output/raw/sqlmap_bg.log")

    # Retornamos un resultado simulado para que el pipeline no falle, incluyendo
    # la info de caché (qué URLs no se volvieron a probar y cuáles se re-testearon
    # por haber sido vulnerables antes), para que el comparador de análisis pueda
    # advertir al usuario en vez de mostrar "corregida" cuando en realidad no se probó.
    return [{
        "url": "BACKGROUND_EXECUTION",
        "stdout": "SQLMap ejecutándose en segundo plano. Revisar output/raw/sqlmap_bg.log",
        "stderr": "",
        "success": True,
        "timeout": False,
        "cache_info": cache_info
    }]

    #docker exec -it security-app 
    #     tail -f /app/output/raw/sqlmap_bg.log
