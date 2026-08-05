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

import re

def parsear_tablas_log_sqlmap(log_path):
    """
    Parsea un archivo de log de sqlmap y extrae las bases de datos, 
    tablas, columnas y filas (entradas) dumpeadas.
    """
    with open(log_path, 'r', encoding='utf-8') as f:
        log_content = f.read()

    databases = {}
    current_db = None
    current_table = None
    state = "SEARCHING"
    
    for line in log_content.splitlines():
        line = line.strip()
        
        if line.startswith("Database: "):
            current_db = line.split("Database: ")[1].strip()
            if current_db not in databases:
                databases[current_db] = {}
            state = "SEARCHING"
            continue
            
        if line.startswith("Table: "):
            current_table = line.split("Table: ")[1].strip()
            if current_db:
                databases[current_db][current_table] = {"columns": [], "rows": []}
            state = "EXPECTING_HEADER_SEPARATOR"
            continue

        # "[N tables]" precede al listado de nombres de tabla cuando SQLMap corrió
        # con --tables pero sin --dump (nivel "fast_evidence"): no hay columnas ni
        # filas, cada renglón de la caja ASCII es directamente un nombre de tabla.
        if re.match(r"^\[\d+ tables?\]$", line) and current_db:
            state = "EXPECTING_TABLE_NAMES_SEPARATOR"
            continue

        if state == "EXPECTING_TABLE_NAMES_SEPARATOR" and line.startswith("+"):
            state = "EXPECTING_TABLE_NAMES"
            continue

        if state == "EXPECTING_TABLE_NAMES":
            if line.startswith("|"):
                nombre_tabla = line.strip("|").strip()
                if current_db and nombre_tabla and nombre_tabla not in databases[current_db]:
                    databases[current_db][nombre_tabla] = {"columns": [], "rows": []}
            elif line.startswith("+"):
                state = "SEARCHING"
            continue

        if state == "EXPECTING_HEADER_SEPARATOR" and line.startswith("+"):
            state = "EXPECTING_HEADERS"
            continue
            
        if state == "EXPECTING_HEADERS" and line.startswith("|"):
            columns = [c.strip() for c in line.split("|")[1:-1]]
            if current_db and current_table:
                databases[current_db][current_table]["columns"] = columns
            state = "EXPECTING_DATA_SEPARATOR"
            continue
            
        if state == "EXPECTING_DATA_SEPARATOR" and line.startswith("+"):
            state = "EXPECTING_DATA_ROWS"
            continue
            
        if state == "EXPECTING_DATA_ROWS":
            if line.startswith("|"):
                row = [c.strip() for c in line.split("|")[1:-1]]
                if current_db and current_table:
                    databases[current_db][current_table]["rows"].append(row)
            elif line.startswith("+"):
                # Fin de la tabla
                state = "SEARCHING"
                current_table = None
            continue
            
    return databases