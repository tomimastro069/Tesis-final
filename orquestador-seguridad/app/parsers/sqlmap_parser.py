def parsear_sqlmap(dato_dict_crudo):
    try:
        #data Contiene una lista de dicts
        data = dato_dict_crudo

        lista_sql = list()

        for url_analizada in data:
            stdout = url_analizada.get("stdout", "")
            # Buscamos múltiples patrones que indican éxito en SQLMap
            patrones_exito = [
                "is vulnerable",
                "is injectable",
                "appears to be",
                "vulnerability:",
                "SQL injection",
                "Payload:",
                "Type:",
                "database names are:",
                "current user is:",
                "fetched data logged to text files",
                "available databases"
            ]
            
            if any(p.lower() in stdout.lower() for p in patrones_exito):
                url_filtrada = {
                    "url": url_analizada["url"],
                    "salida": stdout
                }
                lista_sql.append(url_filtrada)

        return {
            "herramienta": "SQLMAP",
            "vulnerabilidades": lista_sql
        }
    except (KeyError, TypeError) as e:
        print(f"Error al parsear los datos de SQLMap: {e}")
        return {"herramienta": "SQLMAP", "vulnerabilidades": []}