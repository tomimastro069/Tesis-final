import time
import os
import sys

from app.scanners.ffuf import run_ffuf
from app.db.database import init_db

def main():
    # Inicializar la base de datos por si acaso
    init_db()
    
    # URL y directorios de prueba
    target_url = "http://benchmark-speed.local"
    output_dir = "output/test_ffuf_speed"
    wordlist_path = "test_wordlist.txt"
    
    # Crear un diccionario de 100 palabras de prueba
    print("Preparando entorno de prueba...")
    with open(wordlist_path, "w") as f:
        for i in range(100):
            f.write(f"palabra_secreta_{i}\n")
            
    print("\n--- PRUEBA 1: Primera ejecución (sin caché) ---")
    start1 = time.time()
    res1 = run_ffuf(target_url, wordlist_path, output_dir)
    end1 = time.time()
    tiempo1 = end1 - start1
    print(f"Skipped: {res1.get('skipped')}")
    print(f"Tiempo total: {tiempo1:.4f} segundos")
    
    print("\n--- PRUEBA 2: Segunda ejecución (mismas palabras, con caché) ---")
    start2 = time.time()
    res2 = run_ffuf(target_url, wordlist_path, output_dir)
    end2 = time.time()
    tiempo2 = end2 - start2
    print(f"Skipped: {res2.get('skipped')}")
    print(f"Tiempo total: {tiempo2:.4f} segundos")
    
    # Añadimos 5 palabras nuevas al diccionario
    with open(wordlist_path, "a") as f:
        for i in range(100, 105):
            f.write(f"palabra_nueva_{i}\n")
            
    print("\n--- PRUEBA 3: Tercera ejecución (5 palabras nuevas añadidas) ---")
    start3 = time.time()
    res3 = run_ffuf(target_url, wordlist_path, output_dir)
    end3 = time.time()
    tiempo3 = end3 - start3
    print(f"Skipped: {res3.get('skipped')}")
    print(f"Tiempo total: {tiempo3:.4f} segundos")
    
    print("\n--- RESUMEN ---")
    print(f"Mejora entre la 1ra y 2da pasada: {(tiempo1/tiempo2):.2f}x más rápido")
    
    # Limpieza
    try:
        os.remove(wordlist_path)
    except:
        pass

if __name__ == "__main__":
    main()
