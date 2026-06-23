from app.workflow.pipeline import run_security_pipeline, run_parser_pipeline
from app.utils.results import resultados_prueba_json
from app.config import settings
from app.reports.generator import generar_reporte
from app.db.database import limpiar_cache_completa

if __name__ == "__main__":
    # Puedes cambiar el target por http://testphp.vulnweb.com/ para ver más acción
    target = settings.TARGET_URL
    
    # Pedir nivel de escaneo al usuario
    nivel = input("Nivel de escaneo (small/medium) [default: medium]: ").lower().strip() or "medium"
    
    # Pedir la cookie de sesion
    cookies = input("Cookie de sesion (opcional, ej. PHPSESSID=123..; security=low) [default: none]: ").strip() or None
    
    # [NUEVO] Opción de limpiar caché
    limpiar = input("¿Deseas limpiar la caché antes de empezar? (s/n) [default: n]: ").lower().strip() == "s"
    if limpiar:
        limpiar_cache_completa()
    
    # [NUEVO] Nivel de SQLMap
    print("\n--- Nivel de Explotación SQLMap ---")
    print("[1] Básico: Solo detecta vulnerabilidad (Recomendado)")
    print("[2] Evidencia Rápida: Extrae bases de datos y usuario actual")
    print("[3] Extracción Completa: Extrae todos los datos (Puede tardar HORAS)")
    
    sqlmap_opcion = input("Selecciona el nivel (1, 2 o 3) [default: 1]: ").strip()
    
    if sqlmap_opcion == "2":
        sqlmap_level = "fast_evidence"
    elif sqlmap_opcion == "3":
        sqlmap_level = "full_dump"
        print("⚠️ ADVERTENCIA: Has seleccionado Extracción Completa. El escaneo puede tardar mucho tiempo.")
    else:
        sqlmap_level = "basic"
    
    print(f"\nIniciando escaneo contra: {target}")
    print(f"Nivel seleccionado: {nivel}")
    print(f"Nivel SQLMap: {sqlmap_level}")
    if cookies:
        print(f"Cookies inyectadas: {cookies}")
        
    resultado_escaneo = run_security_pipeline(target, nivel, cookies, sqlmap_level=sqlmap_level)
    
    print(f"Iniciando parseo de ZAP, SPIDER y FFUF:")
    resultado_parseo = run_parser_pipeline(resultado_escaneo)

    #Funcion de prueba para ver el json unificado y final
    resultados_prueba_json(resultado_parseo)
    
    # Generar el reporte en markdown
    generar_reporte(resultado_parseo)

    print("\nEjecución finalizada. Revisa la carpeta /output/raw y /output/reports")
