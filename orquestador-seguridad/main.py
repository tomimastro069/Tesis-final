from app.workflow.pipeline import run_security_pipeline

if __name__ == "__main__":
    # Puedes cambiar el target por http://testphp.vulnweb.com/ para ver más acción
    target = "http://dvwa" 
    
    print(f"Iniciando escaneo contra: {target}")
    resultado = run_security_pipeline(target)
    
    print("\nEjecución finalizada. Revisa la carpeta /output/raw")
