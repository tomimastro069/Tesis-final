# app/scanners/ffuf.py

import os
from ..runners.exec import run_command
from ..db.database import get_tested_words, save_tested_words


def run_ffuf(target_url: str, wordlist_path: str, output_dir: str, cookies: str = None) -> dict:
    """
    Ejecuta ffuf contra un target y guarda el resultado en JSON.
    
    Si existen palabras ya probadas para el target, crea una wordlist temporal
    con únicamente las palabras no probadas.
    
    Args:
        target_url (str): URL objetivo con FUZZ.
        wordlist_path (str): Path al archivo de palabras.
        output_dir (str): Carpeta donde se guardará el JSON.
        cookies (str): Opcional. String de cookies.

    Returns:
        dict: {
            'output_file': str,   # path al JSON
            'stdout': str,        # salida cruda de ffuf
            'stderr': str,        # errores crudos de ffuf
            'skipped': bool       # True si se omitió el escaneo
        }
    """
    # Normalizar URL
    target_url = target_url.rstrip("/")
    
    # Extraer el nombre de la wordlist (sin extensión) como clave de caché.
    # Así 'small' y 'medium' son cachés totalmente independientes.
    # Ej: "/wordlists/common-small.txt" -> "common-small"
    wordlist_name = os.path.splitext(os.path.basename(wordlist_path))[0]
    
    # Leer wordlist original
    if not os.path.exists(wordlist_path):
        raise FileNotFoundError(f"Wordlist no encontrada: {wordlist_path}")
    
    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
        all_words = set(line.strip() for line in f if line.strip() and not line.startswith("#"))
    
    # Obtener palabras ya probadas para este target CON ESTA WORDLIST específica
    tested_words = get_tested_words(target_url, wordlist_name)

    # Filtrar palabras no probadas
    untested_words = all_words - tested_words
    omitidas_por_cache = all_words - untested_words

    # Info de caché: se calcula siempre, para que el frontend sepa cuánto de la
    # wordlist realmente se probó en este análisis vs. cuánto vino de caché.
    cache_info = {
        "total_candidatas": len(all_words),
        "total_testeadas": len(untested_words),
        "omitidas_por_cache": len(omitidas_por_cache)
    }

    # Si no hay palabras nuevas, omitir escaneo
    if not untested_words:
        return {
            "output_file": None,
            "stdout": "",
            "stderr": "Todas las palabras ya fueron probadas",
            "skipped": True,
            "cache_info": cache_info
        }
    
    # Crear wordlist temporal con palabras no probadas
    temp_wordlist_path = os.path.join(output_dir, "temp_wordlist.txt")
    os.makedirs(output_dir, exist_ok=True)
    
    with open(temp_wordlist_path, "w", encoding="utf-8") as f:
        for word in sorted(untested_words):
            f.write(word + "\n")
    
    # Usar la wordlist temporal en lugar de la original
    wordlist_to_use = temp_wordlist_path
    
    # Asegurarse de que la carpeta de salida exista
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "ffuf_raw.json")
    
    # Asegurar que no haya doble slash al concatenar (ej: http://sitio.com/ + /FUZZ)
    base_url = target_url
    
    # Comando ffuf usando la wordlist temporal
    cmd = [
        "ffuf",
        "-u", f"{base_url}/FUZZ",
        "-w", wordlist_to_use,
        "-e", ".php",
        "-mc", "200,302",
        "-ic", # ignore wordlist comments
        "-of", "json",
        "-o", output_file
    ]
    
    if cookies:
        cmd.extend(["-b", cookies])
    
    # Ejecutar comando usando exec.py
    result = run_command(cmd)
    
    # Guardar las palabras probadas en la base de datos (vinculadas a esta wordlist)
    if untested_words:
        save_tested_words(target_url, untested_words, wordlist_name)
    
    return {
        "output_file": output_file,
        "stdout": result.get("stdout"),
        "stderr": result.get("stderr"),
        "skipped": False,
        "cache_info": cache_info
    }
