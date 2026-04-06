import os
import datetime
from app.config import settings

def generar_reporte(resultados, formato="markdown", output_dir=settings.REPORTS_DIR):
    """
    Genera reportes finales en formato Markdown o texto plano basados en los resultados consolidados.
    Se genera un reporte técnico detallado y un reporte amigable para el cliente.
    
    :param resultados: Diccionario con la estructura consolidada de hallazgos.
    :param formato: 'markdown' o 'txt'
    :param output_dir: Directorio donde se guardará el reporte.
    :return: Tupla con la ruta del archivo técnico y la ruta del cliente.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    extension = "md" if formato == "markdown" else "txt"
    ruta_archivo_tecnico = os.path.join(output_dir, f"reporte_seguridad.{extension}")
    ruta_archivo_cliente = os.path.join(output_dir, f"reporte_cliente.{extension}")
    
    if formato == "markdown":
        contenido_tecnico = _generar_contenido_markdown(resultados)
        contenido_cliente = _generar_contenido_cliente_markdown(resultados)
    else:
        contenido_tecnico = _generar_contenido_texto(resultados)
        contenido_cliente = _generar_contenido_cliente_texto(resultados)
        
    with open(ruta_archivo_tecnico, "w", encoding="utf-8") as f:
        f.write(contenido_tecnico)
        
    with open(ruta_archivo_cliente, "w", encoding="utf-8") as f:
        f.write(contenido_cliente)
        
    print(f"[+] Reporte técnico generado exitosamente en: {ruta_archivo_tecnico}")
    print(f"[+] Reporte para cliente generado exitosamente en: {ruta_archivo_cliente}")
    return ruta_archivo_tecnico, ruta_archivo_cliente

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

def _evaluar_riesgo_global(resultados):
    # Logica simple para definir si el riesgo es critico, alto, medio o bajo
    sqlmap_data = resultados.get("sqlmap", {})
    zap_data = resultados.get("zap", {})
    
    hay_sql = len(sqlmap_data.get("vulnerabilidades", [])) > 0
    alerta_alta = any(a.get("severidad", "").lower() == "high" for a in zap_data.get("alertas", []))
    alerta_media = any(a.get("severidad", "").lower() == "medium" for a in zap_data.get("alertas", []))
    
    if hay_sql or alerta_alta:
        return "ALTO", "Se detectaron vulnerabilidades críticas que podrían comprometer toda la aplicación o base de datos."
    elif alerta_media:
        return "MEDIO", "Se encontraron riesgos moderados que podrían ser aprovechados bajo ciertas condiciones."
    else:
        return "BAJO", "La superficie de ataque presenta riesgos menores o solo de carácter informativo."

def _generar_contenido_cliente_markdown(resultados):
    resumen = resultados.get("resumen", {})
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nivel_riesgo, descripcion_riesgo = _evaluar_riesgo_global(resultados)
    
    md = [
        "# Reporte de Seguridad para el Cliente",
        f"**Fecha de evaluación:** {fecha_actual}\n",
        "## Resumen",
        f"Este reporte presenta una visión no técnica de los resultados de seguridad de la aplicación. Su objetivo es ayudar en la toma de decisiones para proteger los activos de la empresa.\n",
        f"### Nivel de Riesgo Global: **{nivel_riesgo}**",
        f"{descripcion_riesgo}\n",
        "## Visión General de la Evaluación"
    ]
    
    total_hallazgos = resumen.get('alertas_zap', 0) + resumen.get('vulnerabilidades_sqlmap', 0)
    rutas_descubiertas = resumen.get('rutas_ffuf', 0)
    
    md.append(f"- **Puntos de acceso analizados (URLs):** {resumen.get('total_urls_unicas', 0)}")
    md.append(f"- **Áreas descubiertas no enlazadas directamente:** {rutas_descubiertas}")
    md.append(f"- **Vulnerabilidades y debilidades de seguridad encontradas:** {total_hallazgos}\n")
    
    md.append("## Principales Riesgos Identificados")
    
    # Riesgos Altos (SQL o ZAP High)
    sql_vulns = resultados.get("sqlmap", {}).get("vulnerabilidades", [])
    if sql_vulns:
        md.append("### Falla Crítica de Acceso a Datos (Inyección SQL)")
        md.append("Se identificó al menos un punto donde un atacante podría manipular la base de datos de la empresa, lo cual puede derivar en un compromiso del área de base de datos.")
    
    zap_alertas = resultados.get("zap", {}).get("alertas", [])
    categorias_vistas = set()
    for alerta in zap_alertas:
        sev = alerta.get("severidad", "N/A")
        vuln = alerta.get("vulnerabilidad", "Varias")
        if (sev.lower() in ["high", "medium"]) and vuln not in categorias_vistas:
            md.append(f"### {vuln}")
            if sev.lower() == "high":
                md.append("Representa un riesgo elevado para la integridad o confidencialidad de la aplicación.")
            else:
                md.append("Representa un riesgo moderado que podría permitir ataques secundarios o revelación de información.")
            categorias_vistas.add(vuln)
            
    if not sql_vulns and not categorias_vistas:
        md.append("No se detectaron riesgos de severidad alta o media en esta evaluación automatizada.")
        
    md.append("\n## Recomendaciones a Nivel de Negocio")
    md.append("1. **Asignación de Prioridad:** Derive este reporte junto con el 'Reporte Técnico' al equipo de desarrollo para la pronta revisión y corrección de las vulnerabilidades halladas.")
    if sql_vulns or any(a.get("severidad", "").lower() == "high" for a in zap_alertas):
        md.append("2. **Acción Inmediata Requerida:** Debido a la presencia de riesgos ALTOS, se sugiere no avanzar a producción o poner en pausa las funciones afectadas hasta solventarlas.")
    md.append("3. **Política de Revisiones:** Se aconseja incorporar escaneos de seguridad periódicos en el ciclo de vida del desarrollo de forma continua.")
    
    return "\n".join(md)

def _generar_contenido_cliente_texto(resultados):
    resumen = resultados.get("resumen", {})
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nivel_riesgo, descripcion_riesgo = _evaluar_riesgo_global(resultados)
    
    txt = [
        "==================================================",
        "       REPORTE DE SEGURIDAD PARA EL CLIENTE       ",
        "==================================================",
        f"Fecha de evaluación: {fecha_actual}\n",
        "[ RESUMEN ]",
        "Este reporte presenta una visión no técnica de los resultados de seguridad.",
        "Su objetivo es orientar sobre el estado de la aplicación.\n",
        f"Nivel de Riesgo Global: {nivel_riesgo}",
        f"{descripcion_riesgo}\n",
        "[ VISIÓN GENERAL DE LA EVALUACIÓN ]"
    ]
    
    total_hallazgos = resumen.get('alertas_zap', 0) + resumen.get('vulnerabilidades_sqlmap', 0)
    txt.append(f"- Puntos de acceso analizados: {resumen.get('total_urls_unicas', 0)}")
    txt.append(f"- Áreas descubiertas ocultas: {resumen.get('rutas_ffuf', 0)}")
    txt.append(f"- Vulnerabilidades de seguridad encontradas: {total_hallazgos}\n")
    
    txt.append("[ PRINCIPALES RIESGOS IDENTIFICADOS ]")
    sql_vulns = resultados.get("sqlmap", {}).get("vulnerabilidades", [])
    if sql_vulns:
        txt.append("\n>> Falla Crítica de Acceso a Datos (Inyección SQL)")
        txt.append("   Riesgo de compromiso de la base de datos.")
        
    zap_alertas = resultados.get("zap", {}).get("alertas", [])
    categorias_vistas = set()
    for alerta in zap_alertas:
        sev = alerta.get("severidad", "N/A")
        vuln = alerta.get("vulnerabilidad", "Varias")
        if (sev.lower() in ["high", "medium"]) and vuln not in categorias_vistas:
            txt.append(f"\n>> {vuln} (Riesgo evaluado: {sev})")
            if sev.lower() == "high":
                txt.append("   Riesgo elevado para la integridad de la aplicación.")
            else:
                txt.append("   Riesgo moderado a tener en cuenta.")
            categorias_vistas.add(vuln)
            
    if not sql_vulns and not categorias_vistas:
        txt.append("No se detectaron riesgos de severidad alta o media.")
        
    txt.append("\n[ RECOMENDACIONES A NIVEL DE NEGOCIO ]")
    txt.append("1. Compartir este informe y el reporte técnico detallado al equipo de desarrollo.")
    if sql_vulns or any(a.get("severidad", "").lower() == "high" for a in zap_alertas):
        txt.append("2. ACCIÓN RECOMENDADA: Priorizar la remediación de debilidades de nivel ALTO.")
    txt.append("3. Evaluar la aplicación periódicamente.")
    
    return "\n".join(txt)
