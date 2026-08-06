import re

# ZAP manda el riesgo y la confianza juntos en "riskdesc", con formato
# "Riesgo (Confianza)" (ej: "Medium (Low)"). Antes guardábamos ese texto
# combinado tal cual en "severidad", lo que rompía cualquier comparación que
# buscara el riesgo real: un hallazgo "Low (High)" contiene la palabra "high"
# aunque su riesgo real sea bajo. Acá los separamos en el origen para que
# nadie más tenga que re-parsear el texto combinado.
_RISKDESC_RE = re.compile(r"^\s*([A-Za-z ]+?)\s*\(([A-Za-z ]+)\)\s*$")


def _separar_riesgo_confianza(riskdesc: str):
    match = _RISKDESC_RE.match(riskdesc or "")
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return riskdesc or "No clasificado", "N/A"


def parsear_zap(dato_dict_crudo):
    #Intentamos ejecutar el parseo
    try:
        data = dato_dict_crudo

        # Alertas que trae OWASP ZAP: Iterar por todos los sitios porque ZAP separa el HTTP y HTTPS (puerto 80 y 443)
        vistas = set()
        alertas_parseadas = []
        
        for sitio in data.get("site", []):
            alertas_sin_parsear = sitio.get("alerts", [])
            for alerta in alertas_sin_parsear:
                for instancia in alerta.get("instances", []):
                    url = instancia.get("uri", "")
                    clave = (url, alerta.get("alert", ""))

                    if clave not in vistas:
                        vistas.add(clave)
                        riesgo, confianza = _separar_riesgo_confianza(alerta.get("riskdesc", ""))
                        alertas_parseadas.append({
                            "url": url,
                            "vulnerabilidad": alerta.get("alert", "Vulnerabilidad sin nombre"),
                            "severidad": riesgo,
                            "confianza": confianza,
                            "metodo": instancia.get("method", "N/A"),
                            "descripcion": alerta.get("desc", "N/A"),
                            "solucion": alerta.get("solution", "No hay solución disponible"),
                            # Prueba real del hallazgo (solo la traen las reglas de Active Scan,
                            # las pasivas como headers faltantes suelen dejarlas vacías):
                            # "param": el parámetro atacado, "attack": el payload exacto que
                            # ZAP inyectó, "evidence": el fragmento de la respuesta que confirma
                            # que el payload funcionó (ej. reflejado tal cual en el HTML).
                            "parametro": instancia.get("param", ""),
                            "payload_ataque": instancia.get("attack", ""),
                            "evidencia": instancia.get("evidence", "")
                        })
        
        # Extraer info base del primer sitio (si existe)
        primer_sitio = data["site"][0] if data.get("site") else {}

        # Devolver dict con datos unicos arriba y alertas parseadas adentro
        return {
            "herramienta": "ZAP",
            "fecha": data.get("@generated", "Fecha desconocida"),
            "host": primer_sitio.get("@host", "Desconocido"),
            "puerto": primer_sitio.get("@port", "Desconocido"),
            "ssl": primer_sitio.get("@ssl", "false"),
            "total_alertas": len(alertas_parseadas),
            "alertas": alertas_parseadas
        }

    #Si hay un error de clave o tipo en el diccionario, retornamos un dict vacio
    except (KeyError, TypeError) as e:
        print(f"Error al parsear los datos de ZAP: {e}")
        return {}


#Funcion que parsea el resultado que trae ZAP SPIDER - URLS de la pagina
# El endpoint /JSON/spider/view/results/ devuelve: {"results": ["url1", "url2", ...]}
def parsear_spider(dato_dict_crudo):
    try:
        data = dato_dict_crudo

        #Crear lista de URLs sin duplicados
        urls_vistas = set()
        urls_parseadas = []

        for url in data["results"]:
            if url not in urls_vistas:
                urls_vistas.add(url)
                urls_parseadas.append({"url": url})

        #Devolver dict con datos unicos arriba y urls adentro
        return {
            "herramienta": "ZAP Spider",
            "total_urls": len(urls_parseadas),
            "urls": urls_parseadas
        }

    #Si hay un error de clave o tipo en el diccionario, retornamos un dict vacio
    except (KeyError, TypeError) as e:
        print(f"Error al parsear los datos de ZAP Spider: {e}")
        return {}