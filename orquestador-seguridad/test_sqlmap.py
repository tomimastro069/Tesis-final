"""
Script de prueba local para verificar que SQLMap y su parser funcionan correctamente.
Busca explotar de forma dirigida el endpoint vulnerable de SQL Injection en DVWA.

Ejecutar desde el contenedor de la aplicación:
    python test_sqlmap.py
"""
import sys
import json
from app.config import settings
from app.workflow.pipeline import establecer_sesion_automatica
from app.scanners.sqlmap import run_sqlmap
from app.parsers.sqlmap_parser import parsear_sqlmap
from app.db.database import init_db, limpiar_cache_completa

def main():
    print("=" * 60)
    print("TEST DE FUNCIONALIDAD SQLMAP EN DVWA")
    print("=" * 60)

    # 1. Inicializar la base de datos
    print("[1/5] Inicializando base de datos...")
    init_db()

    # Limpiar caché para asegurar que no se omita por ejecuciones previas
    print("[*] Limpiando caché previa para este test...")
    limpiar_cache_completa()

    print("\n--- Nivel de Explotación SQLMap ---")
    print("[1] Básico: Solo detecta vulnerabilidad")
    print("[2] Evidencia Rápida: Extrae bases de datos y usuario actual")
    print("[3] Extracción Completa: Extrae todos los datos (LENTO)")
    
    sqlmap_opcion = input("Selecciona el nivel (1, 2 o 3) [default: 1]: ").strip()
    if sqlmap_opcion == "2":
        sqlmap_level = "fast_evidence"
    elif sqlmap_opcion == "3":
        sqlmap_level = "full_dump"
    else:
        sqlmap_level = "basic"

    target_url = settings.TARGET_URL
    print(f"[*] Target URL configurado: {target_url}")

    # 2. Iniciar sesión automática en DVWA para obtener las cookies de sesión (security=low)
    print("\n[2/5] Obteniendo sesión autenticada en DVWA...")
    cookies = establecer_sesion_automatica(target_url)
    if not cookies:
        print("[-] ERROR: No se pudo obtener la sesión en DVWA.")
        print("    Asegúrate de que los contenedores de Docker estén corriendo:")
        print("    docker compose up -d --build")
        print("    Y que DVWA esté inicializado (http://localhost:8080/setup.php)")
        sys.exit(1)

    # 3. Definir la URL de inyección SQL de DVWA
    # Nota: Este endpoint en DVWA tiene una inyección SQL clásica en el parámetro 'id'
    sqli_url = f"{target_url.rstrip('/')}/vulnerabilities/sqli/?id=1&Submit=Submit"
    print(f"\n[3/5] Lanzando SQLMap contra endpoint vulnerable:")
    print(f"      URL: {sqli_url}")
    print(f"      Cookies: {cookies}")
    print("[*] Ejecutando SQLMap en segundo plano (esto puede demorar entre 30 y 60 segundos)...")

    # 4. Ejecutar SQLMap
    resultado_raw = run_sqlmap(sqli_url, cookies=cookies, sqlmap_level=sqlmap_level)
    
    # Guardar salida cruda temporalmente
    salida_raw_path = "output/raw/test_sqlmap_raw.json"
    with open(salida_raw_path, "w") as f:
        json.dump(resultado_raw, f, indent=4)
    print(f"[+] Ejecución de comando finalizada. Salida guardada en {salida_raw_path}")

    # 5. Parsear el resultado con sqlmap_parser
    print("\n[4/5] Parseando los resultados de SQLMap...")
    resultado_parseado = parsear_sqlmap([resultado_raw])

    print("\n[5/5] Resumen del Test:")
    print("-" * 40)
    print(f"Herramienta: {resultado_parseado.get('herramienta')}")
    vulnerabilidades = resultado_parseado.get("vulnerabilidades", [])
    print(f"Vulnerabilidades encontradas: {len(vulnerabilidades)}")

    if vulnerabilidades:
        print("\n[✓] ¡ÉXITO! SQLMap detectó la inyección SQL:")
        for vuln in vulnerabilidades:
            print(f"    - URL Vulnerable: {vuln['url']}")
            # Mostrar un pedazo del stdout donde detectó la vulnerabilidad
            print("    - Fragmento del reporte de SQLMap:")
            stdout_lines = vuln["salida"].split("\n")
            for line in stdout_lines:
                if any(p in line for p in ["is vulnerable", "is injectable", "Type:", "Title:", "Payload:"]):
                    print(f"        {line.strip()}")
    else:
        print("\n[✗] FALLÓ: SQLMap no reportó vulnerabilidad alguna.")
        print("    Revisa la salida de error/consola en output/raw/test_sqlmap_raw.json")
        if resultado_raw.get("stderr"):
            print("    Errores detectados:")
            print(f"    {resultado_raw['stderr']}")
    print("=" * 60)

if __name__ == "__main__":
    main()
