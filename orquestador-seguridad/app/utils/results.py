def consolidar_resultados(lista_ffuf, lista_zap):
    # Juntamos ambas listas
    total = lista_ffuf + lista_zap
    
    # Usamos un diccionario temporal para filtrar por URL
    vistas = {}
    for item in total:
        # Si la URL ya existe, podrías elegir quedarte con la que tenga más info
        vistas[item["url"]] = item
        
    return list(vistas.values())