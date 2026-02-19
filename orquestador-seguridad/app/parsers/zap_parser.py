def parsear_zap(dato_dict_crudo):
    #Intentamos ejecutar el parseo
    try:
        data = dato_dict_crudo

        #Alertas que trae OWASP ZAP
        alertas_sin_parsear = data["site"][0]["alerts"]

        #Aplanar alertas: una entrada por cada URL afectada, sin duplicados
        vistas = set()
        alertas_parseadas = []

        for alerta in alertas_sin_parsear:
            for instancia in alerta["instances"]:
                url = instancia["uri"]
                clave = (url, alerta["alert"])

                if clave not in vistas:
                    vistas.add(clave)
                    alertas_parseadas.append({
                        "url": url,
                        "vulnerabilidad": alerta["alert"],
                        "severidad": alerta["riskdesc"],
                        "solucion": alerta["solution"]
                    })

        #Devolver dict con datos unicos arriba y alertas parseadas adentro
        return {
            "herramienta": "ZAP",
            "fecha": data["@generated"],
            "host": data["site"][0]["@host"],
            "puerto": data["site"][0]["@port"],
            "ssl": data["site"][0]["@ssl"],
            "total_alertas": len(alertas_parseadas),
            "alertas": alertas_parseadas
        }

    #Si hay un error de clave o tipo en el diccionario, retornamos un dict vacio
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