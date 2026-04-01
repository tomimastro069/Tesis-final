import os
import datetime
from app.config import settings

def generar_reporte(resultados, formato="markdown", output_dir=settings.REPORTS_DIR):
    """
    Genera un reporte final en formato Markdown o texto plano basado en los resultados consolidados.
    
    :param resultados: Diccionario con la estructura consolidada de hallazgos (resumen, spider, zap, ffuf, sqlmap).
    :param formato: 'markdown' o 'txt'
    :param output_dir: Directorio donde se guardará el reporte.
    :return: Ruta del archivo generado.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    extension = "md" if formato == "markdown" else "txt"
    ruta_archivo = os.path.join(output_dir, f"reporte_seguridad.{extension}")
    
    if formato == "markdown":
        contenido = _generar_contenido_markdown(resultados)
    else:
        contenido = _generar_contenido_texto(resultados)
        
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(contenido)
        
    print(f"[+] Reporte generado exitosamente en: {ruta_archivo}")
    return ruta_archivo

def _generar_contenido_markdown(resultados):
    resumen = resultados.get("resumen", {})
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    md = [
        "# Reporte Consolidado de Seguridad",
        f"**Fecha de generación:** {fecha_actual}\n",
        "## Estadísticas Generales"
    ]
    
    # Resumen
    md.append(f"- **Total de URLs únicas analizadas:** {resumen.get('total_urls_unicas', 0)}")
    md.append(f"- **URLs descubiertas por Spider:** {resumen.get('urls_spider', 0)}")
    md.append(f"- **Alertas identificadas por ZAP:** {resumen.get('alertas_zap', 0)}")
    md.append(f"- **Rutas descubiertas por FFUF:** {resumen.get('rutas_ffuf', 0)}")
    md.append(f"- **Vulnerabilidades detectadas por SQLMap:** {resumen.get('vulnerabilidades_sqlmap', 0)}\n")
    
    # Detalle ZAP
    zap_data = resultados.get("zap", {})
    if zap_data and zap_data.get("alertas"):
        md.append("## Detalles Técnicos: Alertas de ZAP")
        for alerta in zap_data.get("alertas", []):
            req_method = alerta.get("metodo", "N/A")
            md.append(f"### {alerta.get('vulnerabilidad', 'Vulnerabilidad Desconocida')}")
            md.append(f"- **Severidad:** {alerta.get('severidad', 'N/A')}")
            md.append(f"- **URL:** `{alerta.get('url', 'N/A')}`")
            md.append(f"- **Método:** {req_method}")
            md.append(f"- **Descripción:** {alerta.get('descripcion', 'N/A')}")
            md.append(f"- **Solución:** {alerta.get('solucion', 'N/A')}")
            md.append("\n---")
    
    # Detalle FFUF
    ffuf_data = resultados.get("ffuf", {})
    if ffuf_data and ffuf_data.get("rutas"):
        md.append("## Detalles Técnicos: Rutas Ocultas o Sensibles (FFUF)")
        for ruta in ffuf_data.get("rutas", []):
            md.append(f"### Directorio/Archivo Sensible o Expuesto")
            md.append(f"- **Severidad:** Low (Informational)")
            md.append(f"- **URL:** `{ruta.get('url', 'N/A')}`")
            md.append(f"- **Método:** GET")
            md.append(f"- **Descripción:** Archivo o directorio descubierto (HTTP Status: {ruta.get('status', 'N/A')}, Lines: {ruta.get('lines', 'N/A')}, Words: {ruta.get('words', 'N/A')})")
            md.append(f"- **Solución:** <p>Verifique si este recurso debe ser público. Si contiene información confidencial, configure controles de acceso o retírelo del servidor.</p>")
            md.append("\n---")
    
    # Detalle SQLMap
    sqlmap_data = resultados.get("sqlmap", {})
    if sqlmap_data and sqlmap_data.get("vulnerabilidades"):
        md.append("\n## Detalles Técnicos: Inyecciones SQL (SQLMap)")
        for vuln in sqlmap_data.get("vulnerabilidades", []):
            titulo = vuln.get('titulo', 'N/A')
            md.append(f"### SQL Injection ({titulo})")
            md.append(f"- **Severidad:** High (High)")
            md.append(f"- **URL:** `{vuln.get('url', 'N/A')}`")
            md.append(f"- **Método:** N/A")
            md.append(f"- **Descripción:** Inyección en parámetro `{vuln.get('parametro', 'N/A')}` mediante un payload tipo `{vuln.get('tipo', 'N/A')}`: `{vuln.get('payload', 'N/A')}`")
            md.append(f"- **Solución:** <p>Use parameterized queries (prepared statements) instead of string concatenation for SQL queries. Use stored procedures. Apply least privilege to the database account.</p>")
            md.append("\n---")
            
    # Detalle Spider (Opcional, podría ser muy largo)
    spider_data = resultados.get("spider", {})
    urls_spider = spider_data.get("urls", [])
    if urls_spider:
        md.append("\n## Mapa del Sitio (Spider)")
        md.append("<details><summary>Ver lista completa de URLs descubiertas</summary>\n")
        md.append("<ul>")
        for u in urls_spider:
            md.append(f"<li><code>{u.get('url', 'N/A')}</code></li>")
        md.append("</ul>\n</details>")
        
    return "\n".join(md)

def _generar_contenido_texto(resultados):
    resumen = resultados.get("resumen", {})
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    txt = [
        "==================================================",
        "          REPORTE CONSOLIDADO DE SEGURIDAD        ",
        "==================================================",
        f"Fecha de generación: {fecha_actual}\n",
        "[ ESTADÍSTICAS GENERALES ]",
        f"- Total de URLs únicas analizadas: {resumen.get('total_urls_unicas', 0)}",
        f"- URLs descubiertas por Spider: {resumen.get('urls_spider', 0)}",
        f"- Alertas identificadas por ZAP: {resumen.get('alertas_zap', 0)}",
        f"- Rutas descubiertas por FFUF: {resumen.get('rutas_ffuf', 0)}",
        f"- Vulnerabilidades detectadas por SQLMap: {resumen.get('vulnerabilidades_sqlmap', 0)}\n",
    ]
    
    # Detalle ZAP
    zap_data = resultados.get("zap", {})
    if zap_data and zap_data.get("alertas"):
        txt.append("\n[ DETALLES TÉCNICOS: ZAP ]")
        for alerta in zap_data.get("alertas", []):
            txt.append(f"\n>> {alerta.get('vulnerabilidad', 'Vulnerabilidad Desconocida')}")
            txt.append(f"   Severidad: {alerta.get('severidad', 'N/A')}")
            txt.append(f"   URL: {alerta.get('url', 'N/A')}")
            txt.append(f"   Método: {alerta.get('metodo', 'N/A')}")
            txt.append(f"   Descripción: {alerta.get('descripcion', 'N/A')}")
            txt.append(f"   Solución: {alerta.get('solucion', 'N/A')}")
            txt.append("-" * 50)
            
    # Detalle FFUF
    ffuf_data = resultados.get("ffuf", {})
    if ffuf_data and ffuf_data.get("rutas"):
        txt.append("\n[ DETALLES TÉCNICOS: RUTAS FFUF ]")
        for ruta in ffuf_data.get("rutas", []):
            txt.append(f"- URL: {ruta.get('url', 'N/A')} | Status: {ruta.get('status', 'N/A')} | Words: {ruta.get('words', 'N/A')} | Lines: {ruta.get('lines', 'N/A')}")
            
    # Detalle SQLMap
    sqlmap_data = resultados.get("sqlmap", {})
    if sqlmap_data and sqlmap_data.get("vulnerabilidades"):
        txt.append("\n[ DETALLES TÉCNICOS: SQLMAP ]")
        for vuln in sqlmap_data.get("vulnerabilidades", []):
            txt.append(f"\n>> Inyección en: {vuln.get('parametro', 'N/A')}")
            txt.append(f"   URL: {vuln.get('url', 'N/A')}")
            txt.append(f"   Tipo: {vuln.get('tipo', 'N/A')}")
            txt.append(f"   Título: {vuln.get('titulo', 'N/A')}")
            txt.append(f"   Payload: {vuln.get('payload', 'N/A')}")
            txt.append("-" * 50)
            
    # Spider
    spider_data = resultados.get("spider", {})
    urls_spider = spider_data.get("urls", [])
    if urls_spider:
        txt.append("\n[ MAPA DEL SITIO: SPIDER ]")
        for u in urls_spider[:20]: # Mostramos las primeras 20 para no saturar
            txt.append(f"- {u.get('url', 'N/A')}")
        if len(urls_spider) > 20:
            txt.append(f"... (y {len(urls_spider) - 20} URLs más)")
            
    return "\n".join(txt)
