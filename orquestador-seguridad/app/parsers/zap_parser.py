import json

def zap_parser(ruta_archivo):
    #Intentamos ejecutar el parseo
    try:
        #Abrir el archivo JSON con los datos que trae OWASP ZAP
        with open(ruta_archivo,"r") as zap:
            #Cargas la info del zap en la variable data
            data = json.load(zap)

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

        #Si no encontramos el archivo o JSON nos da un error, retornamos una lista vacia
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error al parsear el archivo zap: {e}")
        return []


#Funcion que parsea el resultado que trae ZAP SPIDER - URLS de la pagina
def spider_parser(ruta_archivo):
    try:
        #Abro el archivo JSON de ZAP SPIDER
        with open(ruta_archivo, "r") as f:
            #Cargo los datos del diccionario en data
            data = json.load(f)
        
        #Igualo data a url sin parsear para mejor entendimiento
        urls_sin_parsear = data

        #Creo una lista con las urls encontradas
        urls = [entrada["url"] for entrada in urls_sin_parsear["urlsInScope"]]

        #Retorno todas las urls que encontro SPIDER
        return urls

        #Si no encontramos el archivo o JSON nos da un error, retornamos una lista vacia
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error al parsear el archivo zap: {e}")
        return []