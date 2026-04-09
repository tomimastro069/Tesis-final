def parsear_zap(dato_dict_crudo):
    #Intentamos ejecutar el parseo
    try:
        data = dato_dict_crudo

        # Alertas que trae OWASP ZAP: Iterar por todos los sitios porque ZAP separa el HTTP y HTTPS (puerto 80 y 443)
        vistas = set()
        alertas_parseadas = []
        
        for sitio in data.get("site", []):
            alertas_sin_parsear = sitio.get("alerts", [])
            for alerta in alertas_sin_parsear:
                for instancia in alerta.get("instances", []):
                    url = instancia.get("uri", "")
                    clave = (url, alerta.get("alert", ""))

                    if clave not in vistas:
                        vistas.add(clave)
                        alertas_parseadas.append({
                            "url": url,
                            "vulnerabilidad": alerta.get("alert", "Vulnerabilidad sin nombre"),
                            "severidad": alerta.get("riskdesc", "No clasificado"),
                            "solucion": alerta.get("solution", "No hay solución disponible")
                        })
        
        # Extraer info base del primer sitio (si existe)
        primer_sitio = data["site"][0] if data.get("site") else {}

        # Devolver dict con datos unicos arriba y alertas parseadas adentro
        return {
            "herramienta": "ZAP",
            "fecha": data.get("@generated", "Fecha desconocida"),
            "host": primer_sitio.get("@host", "Desconocido"),
            "puerto": primer_sitio.get("@port", "Desconocido"),
            "ssl": primer_sitio.get("@ssl", "false"),
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