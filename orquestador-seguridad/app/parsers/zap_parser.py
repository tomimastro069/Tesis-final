def parsear_zap(dato_dict_crudo):
    #Intentamos ejecutar el parseo
    try:
        #Acceder directamente al diccionario con los datos crudos de OWASP ZAP
        data = dato_dict_crudo

        #Alertas que trae OWASP ZAP
        alertas_sin_parsear = data["site"][0]["alerts"]

        #Datos Principales de OWASP ZAP
        datos_site = {
            "herramienta":"ZAP",
            "fecha_de_generacion": data["@generated"],
            "url_atacada": data["site"][0]["@name"],
            "host": data["site"][0]["@host"],
            "puerto": data["site"][0]["@port"],
            "ssl": data["site"][0]["@ssl"]
        }
        #Limpiar la informacion irrelevante del diccionario "data"
        alertas_parseado = [
            {
                "vulnerabilidad": alerta["alert"],
                "url": [instancia["uri"] for instancia in alerta["instances"]],
                "severidad": alerta["riskdesc"],
                "solucion": alerta["solution"]
            }
            for alerta in alertas_sin_parsear
        ]

        #Agregar la lista de datos parseados a los datos del site
        datos_site["alertas"] = alertas_parseado

        #Retornar los datos limpios
        return datos_site

        #Si hay un error de clave o tipo en el diccionario, retornamos una lista vacia
    except (KeyError, TypeError) as e:
        print(f"Error al parsear los datos de ZAP: {e}")
        return []


#Funcion que parsea el resultado que trae ZAP SPIDER - URLS de la pagina
def parsear_spider(dato_dict_crudo):
    try:
        #Acceder directamente al diccionario con los datos crudos de ZAP SPIDER
        data = dato_dict_crudo

        #Creo una lista con las urls encontradas
        urls = [entrada["url"] for entrada in data["urlsInScope"]]

        #Retorno todas las urls que encontro SPIDER
        return urls

        #Si hay un error de clave o tipo en el diccionario, retornamos una lista vacia
    except (KeyError, TypeError) as e:
        print(f"Error al parsear los datos de ZAP Spider: {e}")
        return []