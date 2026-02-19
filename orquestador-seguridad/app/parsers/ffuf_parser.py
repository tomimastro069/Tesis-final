import json

ruta_archivo_ejemplo = "orquestador-seguridad/app/samples/ffuf_sample.json"

def parsear_ffuf(dato_dict_crudo):
    try:
        #Abro el archivo JSON 
        data = dato_dict_crudo

        #Limpiar lista segun los resultados (200 y 302)
        lista_limpia = [
            {
                "herramienta":"ffuf",
                "input":item["input"],
                "url":item["url"],
                "host":item["host"],
                "status":item["status"]
            }
            for item in data["results"] 
            if item["status"] in [200, 302]
        ]

        #Retornar la lista limpia
        return lista_limpia

    except (KeyError, TypeError) as e:
        print(f"Error al parsear el archivo ffuf: {e}")
        return []