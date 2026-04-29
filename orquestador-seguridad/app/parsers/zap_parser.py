def parsear_zap(dato_dict_crudo):
    # Intentamos ejecutar el parseo
    try:
        data = dato_dict_crudo
        alertas_parseadas = []
        vistas = set()

        # ZAP organiza las alertas por "site". Iteramos por todos los sitios registrados
        # para no perder alertas si ZAP separó el target en varios nodos (ej: con y sin barra).
        sitios = data.get("site", [])
        for sitio in sitios:
            alertas_sin_parsear = sitio.get("alerts", [])

            for alerta in alertas_sin_parsear:
                for instancia in alerta.get("instances", []):
                    url = instancia.get("uri")
                    clave = (url, alerta.get("alert"))

                    if clave not in vistas:
                        vistas.add(clave)
                        alertas_parseadas.append({
                            "url": url,
                            "vulnerabilidad": alerta.get("alert"),
                            "severidad": alerta.get("riskdesc"),
                            "solucion": alerta.get("solution"),
                            "metodo": instancia.get("method", "N/A"),
                            "descripcion": alerta.get("description", "N/A")
                        })

        # Devolver dict con datos consolidados de todos los sitios
        return {
            "herramienta": "ZAP",
            "total_alertas": len(alertas_parseadas),
            "alertas": alertas_parseadas
        }

    # Si hay un error de clave o tipo en el diccionario, retornamos un dict vacio
    except (KeyError, TypeError) as e:
        print(f"Error al parsear los datos de ZAP: {e}")
        return {}


#Funcion que parsea el resultado que trae ZAP SPIDER - URLS de la pagina
# El endpoint /JSON/spider/view/results/ devuelve: {"results": ["url1", "url2", ...]}
def parsear_spider(dato_dict_crudo):
    try:
        data = dato_dict_crudo

        #Crear lista de URLs sin duplicados
        urls_vistas = set()
        urls_parseadas = []

        for url in data["results"]:
            if url not in urls_vistas:
                urls_vistas.add(url)
                urls_parseadas.append({"url": url})

        #Devolver dict con datos unicos arriba y urls adentro
        return {
            "herramienta": "ZAP Spider",
            "total_urls": len(urls_parseadas),
            "urls": urls_parseadas
        }

    #Si hay un error de clave o tipo en el diccionario, retornamos un dict vacio
    except (KeyError, TypeError) as e:
        print(f"Error al parsear los datos de ZAP Spider: {e}")
        return {}