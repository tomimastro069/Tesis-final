from app.workflow.pipeline import run_security_pipeline, run_parser_pipeline
from app.utils.results import resultados_prueba_json
from app.config import settings

if __name__ == "__main__":
    # Puedes cambiar el target por http://testphp.vulnweb.com/ para ver más acción
    target = settings.TARGET_URL
    
    # Pedir nivel de escaneo al usuario
    nivel = input("Nivel de escaneo (small/medium) [default: medium]: ").lower().strip() or "medium"
    
    print(f"Iniciando escaneo contra: {target}")
    print(f"Nivel seleccionado: {nivel}")
    resultado_escaneo = run_security_pipeline(target, nivel)
    
    print(f"Iniciando parseo de ZAP, SPIDER y FFUF:")
    resultado_parseo = run_parser_pipeline(resultado_escaneo)

    #Funcion de prueba para ver el json unificado y final
    resultados_prueba_json(resultado_parseo)
    print("\nEjecución finalizada. Revisa la carpeta /output/raw")
