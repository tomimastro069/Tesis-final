#Funcion que junta todos los resultados parseados en una sola estructura
def consolidar_resultados(dict_spider, dict_zap, dict_ffuf):
    #Extraer las listas internas de cada herramienta
    urls_spider = dict_spider.get("urls", [])
    alertas_zap = dict_zap.get("alertas", [])
    rutas_ffuf = dict_ffuf.get("rutas", [])

    #Juntar todas las URLs unicas encontradas por cualquier herramienta
    todas_las_urls = set()

    for item in urls_spider:
        todas_las_urls.add(item["url"])

    for item in alertas_zap:
        todas_las_urls.add(item["url"])

    for item in rutas_ffuf:
        todas_las_urls.add(item["url"])

    #Devolver estructura consolidada con los 3 resultados y un resumen
    return {
        "resumen": {
            "total_urls_unicas": len(todas_las_urls),
            "urls_spider": dict_spider.get("total_urls", 0),
            "alertas_zap": dict_zap.get("total_alertas", 0),
            "rutas_ffuf": dict_ffuf.get("total_rutas", 0)
        },
        "spider": dict_spider,
        "zap": dict_zap,
        "ffuf": dict_ffuf
    }