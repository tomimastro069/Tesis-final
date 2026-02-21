import json
#Funcion que junta todos los resultados parseados en una sola estructura
def consolidar_resultados(dict_spider, dict_zap, dict_ffuf, dict_sqlmap):
    #Extraer las listas internas de cada herramienta
    urls_spider = dict_spider.get("urls", [])
    alertas_zap = dict_zap.get("alertas", [])
    rutas_ffuf = dict_ffuf.get("rutas", [])
    vulns_sqlmap = dict_sqlmap.get("vulnerabilidades", [])

    #Juntar todas las URLs unicas encontradas por cualquier herramienta
    todas_las_urls = set()

    for item in urls_spider:
        todas_las_urls.add(item["url"])

    for item in alertas_zap:
        todas_las_urls.add(item["url"])

    for item in rutas_ffuf:
        todas_las_urls.add(item["url"])
    
    # Agregar URLs de sqlmap al set
    for item in vulns_sqlmap:
        todas_las_urls.add(item["url"])

    #Devolver estructura consolidada con los 3 resultados y un resumen
    return {
        "resumen": {
            "total_urls_unicas": len(todas_las_urls),
            "urls_spider": dict_spider.get("total_urls", 0),
            "alertas_zap": dict_zap.get("total_alertas", 0),
            "rutas_ffuf": dict_ffuf.get("total_rutas", 0),
            "vulnerabilidades_sqlmap": len(vulns_sqlmap)
        },
        "spider": dict_spider,
        "zap": dict_zap,
        "ffuf": dict_ffuf,
        "sqlmap": dict_sqlmap
    }

#Crea un archivo en output para mostrar el arhcivo final unificado json.
def resultados_prueba_json(resultados):
    import os
    output_dir = "./output/raw"
    os.makedirs(output_dir, exist_ok=True)

    ruta_archivo = os.path.join(output_dir, "resultado_unificado.json")

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    print(f"\n--- Resultado unificado guardado en: {ruta_archivo} ---")
    print(json.dumps(resultados.get("resumen", {}), indent=4, ensure_ascii=False))
