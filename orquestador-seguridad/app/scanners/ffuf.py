# app/scanners/ffuf.py

import os
from ..runners.exec import run_command


def run_ffuf(target_url: str, wordlist_path: str, output_dir: str, cookies: str = None) -> dict:
    """
    Ejecuta ffuf contra un target y guarda el resultado en JSON.
    
    Args:
        target_url (str): URL objetivo con FUZZ.
        wordlist_path (str): Path al archivo de palabras.
        output_dir (str): Carpeta donde se guardará el JSON.
        cookies (str): Opcional. String de cookies.

    Returns:
        dict: {
            'output_file': str,   # path al JSON
            'stdout': str,        # salida cruda de ffuf
            'stderr': str         # errores crudos de ffuf
        }
    """
    # Asegurarse de que la carpeta de salida exista
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "ffuf_raw.json")
    
    # Asegurar que no haya doble slash al concatenar (ej: http://sitio.com/ + /FUZZ)
    base_url = target_url.rstrip("/")
    
    # Comando ffuf
    cmd = [
        "ffuf",
        "-u", f"{base_url}/FUZZ",
        "-w", wordlist_path,
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
    
    return {
        "output_file": output_file,
        "stdout": result.get("stdout"),
        "stderr": result.get("stderr")
    }
