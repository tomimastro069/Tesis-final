from app.workflow.pipeline import run_security_pipeline, run_parser_pipeline

if __name__ == "__main__":
    # Puedes cambiar el target por http://testphp.vulnweb.com/ para ver más acción
    target = "http://dvwa" 
    
    print(f"Iniciando escaneo contra: {target}")
    resultado_escaneo = run_security_pipeline(target)
    
    print(f"Iniciando parseo de ZAP, SPIDER y FFUF:")
    resultado_parseo = run_parser_pipeline(resultado_escaneo)

    print("\nEjecución finalizada. Revisa la carpeta /output/raw")
