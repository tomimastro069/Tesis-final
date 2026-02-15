# app/scanners/zap.py

import time
import requests

ZAP_HOST = "zap"
ZAP_PORT = 8090
API_KEY = "12345"


def iniciar_spider(target_url: str) -> str:
    """
    Inicia el spider en ZAP.
    Devuelve el scan_id.
    """
    url = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/spider/action/scan/"
    params = {
        "apikey": API_KEY,
        "url": target_url
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json().get("scan")


def esperar_spider(scan_id: str) -> None:
    """
    Espera hasta que el spider llegue a 100%.
    No interpreta resultados.
    """
    url = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/spider/view/status/"

    while True:
        response = requests.get(url, params={
            "apikey": API_KEY,
            "scanId": scan_id
        })

        response.raise_for_status()

        status = int(response.json().get("status", 0))

        if status >= 100:
            break

        time.sleep(2)


def obtener_urls(scan_id: str) -> dict:
    """
    Obtiene las URLs encontradas por el spider.
    Devuelve el JSON crudo.
    """
    url = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/spider/view/results/"

    response = requests.get(url, params={
        "apikey": API_KEY,
        "scanId": scan_id
    })

    response.raise_for_status()

    return response.json()


def iniciar_escaneo_activo(target_url: str) -> str:
    """
    Inicia el escaneo activo (Active Scan) en ZAP.
    Devuelve el scan_id.
    """
    # --- OPTIMIZACIÓN ---
    # Configuramos la intensidad a LOW (Baja). Reduce drásticamente el tiempo y CPU.
    # Realiza menos pruebas por parámetro, pero mantiene las categorías principales.
    base_opt = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/ascan/action"
    requests.get(f"{base_opt}/setOptionAttackStrength/", params={"apikey": API_KEY, "strength": "LOW"})
    requests.get(f"{base_opt}/setOptionAlertThreshold/", params={"apikey": API_KEY, "threshold": "MEDIUM"})

    url = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/ascan/action/scan/"
    params = {
        "apikey": API_KEY,
        "url": target_url,
        "recurse": "true"  # Escanea recursivamente lo encontrado por el spider
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json().get("scan")


def esperar_escaneo_activo(scan_id: str) -> None:
    """
    Espera hasta que el escaneo activo llegue a 100%.
    """
    url = f"http://{ZAP_HOST}:{ZAP_PORT}/JSON/ascan/view/status/"

    while True:
        response = requests.get(url, params={"apikey": API_KEY, "scanId": scan_id})
        response.raise_for_status()
        status = int(response.json().get("status", 0))
        print(f"Progreso escaneo activo: {status}%")

        if status >= 100:
            break
        time.sleep(5)  # El escaneo activo es más lento, esperamos 5s


def obtener_reporte_json() -> dict:
    """
    Obtiene el reporte completo en formato JSON.
    Este endpoint (/OTHER/core/other/jsonreport/) devuelve la estructura
    completa (site, alerts) que tu parser espera.
    """
    url = f"http://{ZAP_HOST}:{ZAP_PORT}/OTHER/core/other/jsonreport/"

    response = requests.get(url, params={"apikey": API_KEY})
    response.raise_for_status()

    return response.json()
