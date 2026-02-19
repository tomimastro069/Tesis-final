"""
Script de prueba local para verificar que los parsers y la consolidación
funcionan correctamente usando los archivos de ejemplo en app/samples/.

Ejecutar desde la raiz del proyecto:
    python test_parsers.py
"""
import json

from app.parsers.ffuf_parser import parsear_ffuf
from app.parsers.zap_parser import parsear_zap, parsear_spider
from app.utils.results import consolidar_resultados


def cargar_sample(ruta):
    with open(ruta, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    print("=" * 60)
    print("TEST DE PARSERS Y CONSOLIDACIÓN")
    print("=" * 60)

    # --- Cargar datos de ejemplo ---
    zap_crudo = cargar_sample("app/samples/zap_sample.json")
    spider_crudo = cargar_sample("app/samples/spider_sample.json")
    ffuf_crudo = cargar_sample("app/samples/ffuf_sample.json")

    # --- 1. Probar parsear_spider ---
    print("\n[1/3] Probando parsear_spider...")
    spider_parseado = parsear_spider(spider_crudo)
    print(f"  Herramienta: {spider_parseado.get('herramienta')}")
    print(f"  Total URLs: {spider_parseado.get('total_urls')}")
    print(f"  Primeras 3 URLs:")
    for url in spider_parseado.get("urls", [])[:3]:
        print(f"    - {url['url']}")

    # --- 2. Probar parsear_zap ---
    print("\n[2/3] Probando parsear_zap...")
    zap_parseado = parsear_zap(zap_crudo)
    print(f"  Herramienta: {zap_parseado.get('herramienta')}")
    print(f"  Fecha: {zap_parseado.get('fecha')}")
    print(f"  Host: {zap_parseado.get('host')}")
    print(f"  Total alertas: {zap_parseado.get('total_alertas')}")
    print(f"  Alertas encontradas:")
    for alerta in zap_parseado.get("alertas", []):
        print(f"    - [{alerta['severidad']}] {alerta['vulnerabilidad']} → {alerta['url']}")

    # --- 3. Probar parsear_ffuf ---
    print("\n[3/3] Probando parsear_ffuf...")
    ffuf_parseado = parsear_ffuf(ffuf_crudo)
    print(f"  Herramienta: {ffuf_parseado.get('herramienta')}")
    print(f"  Comando: {ffuf_parseado.get('comando')}")
    print(f"  Total rutas: {ffuf_parseado.get('total_rutas')}")
    print(f"  Rutas encontradas:")
    for ruta in ffuf_parseado.get("rutas", []):
        print(f"    - [{ruta['status']}] {ruta['url']}")

    # --- 4. Probar consolidación ---
    print("\n" + "=" * 60)
    print("CONSOLIDACIÓN")
    print("=" * 60)
    resultado_final = consolidar_resultados(spider_parseado, zap_parseado, ffuf_parseado)

    print(f"\n  URLs únicas totales: {resultado_final['resumen']['total_urls_unicas']}")
    print(f"  URLs del spider: {resultado_final['resumen']['urls_spider']}")
    print(f"  Alertas de ZAP: {resultado_final['resumen']['alertas_zap']}")
    print(f"  Rutas de ffuf: {resultado_final['resumen']['rutas_ffuf']}")

    # --- 5. Guardar resultado final para inspección ---
    ruta_salida = "output/raw/test_resultado_final.json"
    with open(ruta_salida, "w") as f:
        json.dump(resultado_final, f, indent=4, ensure_ascii=False)

    print(f"\n  Resultado completo guardado en: {ruta_salida}")
    print("\n" + "=" * 60)
    print("TEST FINALIZADO")
    print("=" * 60)
