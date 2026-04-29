def parsear_ffuf(dato_dict_crudo):
    try:
        data = dato_dict_crudo

        #Limpiar lista segun los resultados (200 y 302), sin duplicados por URL
        urls_vistas = set()
        lista_limpia = []

        for item in data.get("results", []):
            if isinstance(item, dict) and item.get("status") in [200, 302] and item.get("url") not in urls_vistas:
                urls_vistas.add(item["url"])
                lista_limpia.append({
                    "url": item.get("url", ""),
                    "input": item.get("input", ""),
                    "status": item.get("status", 0)
                })

        #Devolver dict con datos unicos arriba y rutas parseadas adentro
        return {
            "herramienta": "ffuf",
            "comando": data.get("commandline", ""),
            "fecha": data.get("time", ""),
            "total_rutas": len(lista_limpia),
            "rutas": lista_limpia
        }

    except (KeyError, TypeError) as e:
        print(f"Error al parsear los datos de ffuf: {e}")
        return {}