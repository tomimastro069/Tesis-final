def parsear_sqlmap(dato_dict_crudo):
    try:
        #data Contiene una lista de dicts
        data = dato_dict_crudo

        lista_sql = list()

        for url_analizada in data:
            stdout = url_analizada.get("stdout", "").lower()
            # Buscamos indicios claros de éxito:
            if any(term in stdout for term in ["vulnerable", "back-end dbms", "payload:"]):
                url_filtrada = {
                    "url": url_analizada["url"],
                    "salida": url_analizada["stdout"]
                }
                lista_sql.append(url_filtrada)

        return {
            "herramienta": "SQLMAP",
            "vulnerabilidades": lista_sql
        }
    except (KeyError, TypeError) as e:
        print(f"Error al parsear los datos de SQLMap: {e}")
        return {"herramienta": "SQLMAP", "vulnerabilidades": []}