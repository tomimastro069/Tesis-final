import json

ruta_archivo_ejemplo = "orquestador-seguridad/app/samples/ffuf_sample.json"

def ffuf_parser(ruta_archivo):
    try:
        #Abro el archivo JSON 
        with open(ruta_archivo,"r") as f:
            #Cargo el archivo JSON en la variable data
            data = json.load(f)

        #Limpiar lista segun los resultados que tienen status = 200
        lista_limpia = [
            {
                "herramienta":"ffuf",
                "input":item["input"],
                "url":item["url"],
                "host":item["host"],
                "status":item["status"]
            }
            for item in data["results"] 
            if item["status"] == 200
        ]

        #Retornar la lista limpia
        return lista_limpia

    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error al parsear el archivo ffuf: {e}")
        return []