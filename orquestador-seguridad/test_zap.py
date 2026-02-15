from app.scanners.zap import iniciar_spider, esperar_spider, obtener_urls, iniciar_escaneo_activo, esperar_escaneo_activo, obtener_reporte_json

def main():
    target = "http://dvwa"

    print("Iniciando spider...")
    scan_id = iniciar_spider(target)
    print(f"Scan ID: {scan_id}")

    print("Esperando a que termine...")
    esperar_spider(scan_id)

    print("Obteniendo URLs...")
    urls = obtener_urls(scan_id)
    print(f"URLs encontradas (raw): {len(urls)}")

    print("\nIniciando Active Scan (Búsqueda de vulnerabilidades)...")
    ascan_id = iniciar_escaneo_activo(target)
    print(f"Active Scan ID: {ascan_id}")

    print("Esperando a que termine el escaneo activo...")
    esperar_escaneo_activo(ascan_id)

    print("Obteniendo reporte completo...")
    reporte = obtener_reporte_json()

    print("¡Escaneo finalizado!")
    # Verificamos si hay sitios en el reporte para confirmar que funcionó
    if "site" in reporte:
        print(f"Reporte generado para: {reporte['site'][0]['@name']}")
        print(f"Alertas encontradas: {len(reporte['site'][0]['alerts'])}")
    else:
        print("El reporte está vacío o tiene un formato inesperado.")


if __name__ == "__main__":
    main()
