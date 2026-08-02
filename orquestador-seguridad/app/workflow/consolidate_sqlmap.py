import os
import re
import sys
import json
import traceback
from datetime import datetime

from app.config import settings
from app.db.database import save_vulnerable_url, init_db, save_sqlmap_tables, get_scan_by_id, save_scan_results
from app.reports.generator import generar_reporte
from app.parsers.sqlmap_parser import parsear_tablas_log_sqlmap

def parse_sqlmap_log_content(content: str) -> list:
    """
    Parsea el contenido de sqlmap_bg.log y extrae las vulnerabilidades encontradas.
    Retorna una lista de diccionarios con formato compatible con el pipeline.
    """
    # Expresión regular para separar el log por URL testeada: [i/N] Testeando: <url>
    matches = list(re.finditer(r"\[\d+/\d+\] Testeando:\s+(https?://\S+)", content))
    
    vulnerabilidades = []
    
    for i in range(len(matches)):
        url = matches[i].group(1)
        start = matches[i].end()
        end = matches[i+1].start() if i + 1 < len(matches) else len(content)
        section_text = content[start:end]
        
        # 1. Buscar parámetros vulnerables
        # Los parámetros vulnerables se delimitan por "Parameter: <nombre> (<método>)"
        param_matches = list(re.finditer(r"Parameter:\s+(\w+)\s+\((GET|POST|Cookie|Header)\)", section_text))
        
        url_vulns = []
        
        for j in range(len(param_matches)):
            param_name = param_matches[j].group(1)
            method = param_matches[j].group(2)
            p_start = param_matches[j].end()
            p_end = param_matches[j+1].start() if j + 1 < len(param_matches) else len(section_text)
            param_text = section_text[p_start:p_end]
            
            # Buscar inyecciones (Type, Title, Payload) dentro del texto del parámetro
            injects = re.findall(
                r"Type:\s*(.*?)\n\s*Title:\s*(.*?)\n\s*Payload:\s*(.*?)(?:\n|$)", 
                param_text, 
                re.DOTALL
            )
            
            for injection_type, title, payload in injects:
                url_vulns.append({
                    "url": url,
                    "parametro": param_name,
                    "tipo": injection_type.strip(),
                    "titulo": title.strip(),
                    "payload": payload.strip(),
                    "metodo": method.strip()
                })
        
        # 2. Buscar volcados de datos (databases, tables, user hashes, etc.)
        extra_info_parts = []
        
        # Detectar base de datos y tabla
        db_table = re.search(r"Database:\s*(\S+)\nTable:\s*(\S+)\n\[(\d+)\s+entries\]", section_text)
        if db_table:
            db_name = db_table.group(1)
            table_name = db_table.group(2)
            entries_count = db_table.group(3)
            extra_info_parts.append(f"Volcado de Tabla: {db_name}.{table_name} ({entries_count} registros)")
        
        # Detectar tablas ASCII-art de forma robusta sin truncar las filas
        # Permite líneas con '|' y separadores '+' dentro de la misma tabla
        tables = re.findall(r"(\+[-+]+\+\n(?:\|.*?\|\n|\+[-+]+\+\n)+\+[-+]+\+)", section_text)
        for t in tables:
            extra_info_parts.append(t)
            
        # Detectar bases de datos disponibles
        dbs_match = re.search(r"available databases \[\d+\]:\n(.*?)(?:\n\n|\Z)", section_text, re.DOTALL)
        if dbs_match:
            dbs = [d.strip() for d in dbs_match.group(1).split("\n") if d.strip()]
            extra_info_parts.append(f"Bases de datos disponibles: {', '.join(dbs)}")
            
        # Detectar usuario actual
        user_match = re.search(r"current user:\s*'(.*?)'", section_text)
        if user_match:
            extra_info_parts.append(f"Usuario actual: {user_match.group(1)}")
            
        # Detectar base de datos actual
        current_db_match = re.search(r"current database:\s*'(.*?)'", section_text)
        if current_db_match:
            extra_info_parts.append(f"Base de datos actual: {current_db_match.group(1)}")
            
        # Si encontramos inyecciones para esta URL, les agregamos la información extra solo a la primera
        if url_vulns:
            extra_info_str = "\n\n".join(extra_info_parts) if extra_info_parts else ""
            for idx, v in enumerate(url_vulns):
                if idx == 0 and extra_info_str:
                    v["extra_info"] = extra_info_str
                vulnerabilidades.append(v)
                
    return vulnerabilidades

def main():
    print("=" * 60)
    print("INICIANDO CONSOLIDACIÓN ASÍNCRONA DE SQLMAP")
    print("=" * 60)

    # scan_id del escaneo al que pertenece este SQLMap en segundo plano (si se pasó como argumento)
    scan_id = sys.argv[1] if len(sys.argv) > 1 else None
    if scan_id:
        print(f"[*] scan_id recibido: {scan_id}")
    else:
        print("[!] No se recibió scan_id: solo se actualizarán los archivos en disco, no la base de datos del escaneo.")

    init_db()
    
    log_path = os.path.join(settings.OUTPUT_DIR, "sqlmap_bg.log")
    unificado_path = os.path.join(settings.OUTPUT_DIR, "resultado_unificado.json")
    
    if not os.path.exists(log_path):
        print(f"[-] ERROR: No se encontró el archivo de log en {log_path}")
        return
        
    print(f"[*] Leyendo log de SQLMap: {log_path}")
    with open(log_path, "r", encoding="utf-8") as f:
        log_content = f.read()
        
    vulnerabilidades = parse_sqlmap_log_content(log_content)
    print(f"[+] Se parsearon {len(vulnerabilidades)} vulnerabilidades de SQLMap.")

    # 1. Guardar hallazgos en la Base de Datos
    for v in vulnerabilidades:
        print(f"    - Guardando vuln: SQL Injection en {v['url']} (param: {v['parametro']})")
        save_vulnerable_url(
            url=v["url"],
            tool="SQLMap",
            vulnerabilidad=f"SQL Injection ({v['titulo']})",
            severidad="High"
        )

    # Formatear al formato que espera el consolidado
    sqlmap_parsed = {
        "herramienta": "SQLMAP",
        "vulnerabilidades": vulnerabilidades
    }

    # Integrar tablas extraídas (Parser de tablas estructuradas)
    try:
        tablas_extraidas = parsear_tablas_log_sqlmap(log_path)
        if tablas_extraidas:
            sqlmap_parsed["tablas_extraidas"] = tablas_extraidas
            target_url = "URL_DESCONOCIDA"
            if vulnerabilidades:
                target_url = vulnerabilidades[0]["url"]
            save_sqlmap_tables(target_url, tablas_extraidas)
    except Exception as e:
        print(f"[!] Error al parsear o guardar tablas en consolidación: {e}")

    # 2. Actualizar la base de datos del escaneo (lo que realmente lee el frontend).
    # Sin esto, los hallazgos y tablas de SQLMap quedan solo en el disco y nunca
    # llegan a la app, porque SQLMap corre en segundo plano y el escaneo ya se
    # había guardado como "completado" antes de que terminara.
    db_results = None
    if scan_id:
        try:
            scan_row = get_scan_by_id(scan_id)
            if scan_row and scan_row.get("results_raw"):
                db_results = json.loads(scan_row["results_raw"])
            else:
                print(f"[!] No se encontraron resultados previos en la base de datos para scan_id={scan_id}.")
                db_results = {"resumen": {}}

            # db_results["cache_info"] (general: FFUF + SQLMap) ya se guardó al inicio
            # del escaneo y no hace falta tocarlo acá — este script solo actualiza los
            # hallazgos/tablas de SQLMap, no recalcula la caché.
            db_results["sqlmap"] = sqlmap_parsed

            # Recalcular el conteo de vulnerabilidades de SQLMap en el resumen
            resumen = db_results.get("resumen", {}) or {}
            resumen["vulnerabilidades_sqlmap"] = len(vulnerabilidades)
            db_results["resumen"] = resumen

            save_scan_results(scan_id, json.dumps(db_results, ensure_ascii=False))
            print(f"[✓] Base de datos actualizada para scan_id={scan_id} con hallazgos y tablas de SQLMap.")
        except Exception as e:
            print(f"[!] Error al actualizar la base de datos para scan_id={scan_id}: {e}")
            traceback.print_exc()
    else:
        print("[!] No se recibió scan_id: se omite la actualización de la base de datos.")

    # 3. Actualizar resultado_unificado.json (archivo de referencia en disco, opcional)
    if os.path.exists(unificado_path):
        print(f"[*] Actualizando reporte consolidado: {unificado_path}")
        try:
            with open(unificado_path, "r", encoding="utf-8") as f:
                reporte = json.load(f)

            reporte["sqlmap"] = sqlmap_parsed

            # Recalcular el resumen
            todas_las_urls = set()

            # URLs del spider
            for item in reporte.get("spider", {}).get("urls", []):
                todas_las_urls.add(item["url"])
            # URLs de ZAP
            for item in reporte.get("zap", {}).get("alertas", []):
                todas_las_urls.add(item["url"])
            # URLs de FFUF
            for item in reporte.get("ffuf", {}).get("rutas", []):
                todas_las_urls.add(item["url"])
            # URLs de SQLMap reales
            for item in vulnerabilidades:
                todas_las_urls.add(item["url"])

            reporte["resumen"]["total_urls_unicas"] = len(todas_las_urls)
            reporte["resumen"]["vulnerabilidades_sqlmap"] = len(vulnerabilidades)

            # Escribir de vuelta el archivo consolidado
            with open(unificado_path, "w", encoding="utf-8") as f:
                json.dump(reporte, f, indent=4, ensure_ascii=False)

            print("[✓] resultado_unificado.json actualizado con éxito.")

            # 4. Regenerar reportes MD y TXT
            print("[*] Regenerando reportes en formato Markdown y Texto...")
            generar_reporte(reporte)
            print("[✓] Reportes de seguridad regenerados.")

        except Exception as e:
            print(f"[-] ERROR al actualizar reportes: {e}")
            traceback.print_exc()
    else:
        print(f"[!] No se encontró el archivo {unificado_path}. Se omite la actualización de ese archivo de referencia (no afecta a la app).")
        # Aun sin el archivo de referencia, regeneramos los reportes MD/TXT con lo que
        # tengamos disponible (los resultados recién guardados en la base de datos).
        if db_results:
            try:
                print("[*] Regenerando reportes en formato Markdown y Texto a partir de la base de datos...")
                generar_reporte(db_results)
                print("[✓] Reportes de seguridad regenerados.")
            except Exception as e:
                print(f"[-] ERROR al regenerar reportes desde la base de datos: {e}")
                traceback.print_exc()

if __name__ == "__main__":
    main()
