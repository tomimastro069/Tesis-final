= 19. Anexos Técnicos
<anexos-técnicos>
== Anexo A — Estructura del Proyecto y configuración de docker compose
<anexo-a-estructura-del-proyecto-y-configuración-de-docker-compose>
=== A.1 Estructura del proyecto
<a.1-estructura-del-proyecto>

```text
orquestador-seguridad/
├── main.py                 # Punto de entrada CLI (interactivo)
├── api.py                  # API REST (FastAPI) - punto de entrada como servicio
├── docker-compose.yml      # Servicios: dvwa, zap, app, db, n8n (5 servicios)
├── Dockerfile
├── requirements.txt
├── test_parsers.py / test_speed.py / test_zap.py / test_sqlmap.py
├── OPTIMIZACION_ZAP.md     # Documentación de optimización de timeouts y caché
├── app/
│   ├── config/settings.py
│   ├── runners/exec.py
│   ├── scanners/{zap.py, ffuf.py, sqlmap.py}
│   ├── parsers/{zap_parser.py, ffuf_parser.py, sqlmap_parser.py}
│   ├── workflow/{pipeline.py, consolidate_sqlmap.py}
│   ├── db/database.py
│   ├── routers/n8n_router.py
│   ├── reports/generator.py
│   └── utils/{results.py, time.py}
└── output/{raw/{benchmarks/}, reports/}
n8n/
├── data/
├── flujo.json
└── init-n8n.sh
frontend/
└── src/{app/components/, app/windows98/, hooks/, services/api.ts}
```

#pagebreak()

=== A.2 Archivo docker-compose.yml
<a.2-archivo-docker-compose.yml>

```yaml
version: "3.8"

services:

  db:
    image: postgres:16-alpine
    container_name: security-db
    environment:
      POSTGRES_DB: security_history
      POSTGRES_USER: security_user
      POSTGRES_PASSWORD: security_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5433:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U security_user -d security_history"]
      interval: 5s
      timeout: 5s
      retries: 10

  dvwa:
    image: vulnerables/web-dvwa
    container_name: dvwa
    ports:
      - "8080:80"

  zap:
    image: ghcr.io/zaproxy/zaproxy:stable
    container_name: zap
    environment:
      - ZAP_PORT=8090
    command: >
      zap.sh -daemon
      -host 0.0.0.0
      -port 8090
      -config api.key=12345
      -config api.addrs.addr.name=.*
      -config api.addrs.addr.regex=true
    ports:
      - "8090:8090"

  app:
    build: .
    container_name: security-app
    depends_on:
      db:
        condition: service_healthy
      zap:
        condition: service_started
      dvwa:
        condition: service_started
    environment:
      DB_ENGINE: postgres
      DB_HOST: db
      DB_PORT: 5432
      DB_NAME: security_history
      DB_USER: security_user
      DB_PASSWORD: security_pass
      N8N_WEBHOOK_URL: http://security-n8n:5678/webhook/analyze-vuln
    volumes:
      - .:/app
    ports:
      - "8000:8000"

  n8n:
    image: n8nio/n8n:latest
    container_name: security-n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - NODE_ENV=production
      - IA_API_KEY=${IA_API_KEY:-}
      - GEMINI_API_KEY=${GEMINI_API_KEY:-}
      - groq_key=${groq_key:-}
    volumes:
      - ../n8n/data:/home/node/.n8n
      - ../n8n/flujo.json:/etc/n8n/flujo.json:ro
      - ../n8n/init-n8n.sh:/etc/n8n/init-n8n.sh:ro
    entrypoint: ["tini", "--", "/bin/sh", "/etc/n8n/init-n8n.sh"]
    depends_on:
      - app

volumes:
  postgres_data:
```

#text(
  size: 10pt,
)[#emph[Nota sobre seguridad de la configuración. La definición de credenciales estáticas y tokens en texto plano (POSTGRES_PASSWORD=security_pass y api.key=12345) constituye una decisión técnica orientada a facilitar el despliegue del laboratorio controlado, en concordancia con los alcances definidos en el capítulo 9. Por el contrario, las claves de servicios de inteligencia artificial (IA_API_KEY, GEMINI_API_KEY, groq_key) se gestionan mediante interpolación de variables de entorno del host (\${VAR:-}), garantizando la protección de secretos de producción fuera del entorno local.]]

#pagebreak()
=== A.3 Archivo Dockerfile
<a.3-archivo-dockerfile>

```dockerfile
# Imagen base oficial de Python
FROM python:3.11-slim

# Evita archivos .pyc y buffers raros
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalamos dependencias del sistema necesarias
RUN apt update && apt install -y \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

ARG FFUF_VERSION=2.2.1
ARG FFUF_URL=https://github.com/ffuf/ffuf/releases/download/v${FFUF_VERSION}

RUN wget \
        ${FFUF_URL}/ffuf_${FFUF_VERSION}_linux_amd64.tar.gz \
    && tar -xzf ffuf_${FFUF_VERSION}_linux_amd64.tar.gz \
    && mv ffuf /usr/local/bin/ffuf \
    && chmod +x /usr/local/bin/ffuf \
    && rm ffuf_${FFUF_VERSION}_linux_amd64.tar.gz

# Instalamos SQLMap (clonamos el repo oficial)
RUN apt update && apt install -y git \
    && git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git /opt/sqlmap \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos requirements primero (optimiza cache)
COPY requirements.txt .

# Instalamos dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto
COPY . .

# Comando por defecto
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

#pagebreak()
== Anexo B — Fragmento Representativo: Pipeline de Ejecución
<anexo-b-fragmento-representativo-pipeline-de-ejecución>

```python
def run_security_pipeline(target_url, nivel="medium", cookies=None,
                          sqlmap_level="basic", progress_callback=None):
    init_db()
    ...
    if not cookies:
        cookies = establecer_sesion_automatica(target_url)
    limpiar_sesion_zap()
    if cookies:
        configurar_autenticacion(cookies)

    # --- 1. ZAP SPIDER ---
    spider_id = iniciar_spider(target_url)
    esperar_spider(spider_id, progress_callback=cb_spider)
    spider_urls = obtener_urls(spider_id)

    # --- 2. FFUF (antes del Active Scan) ---
    ffuf_raw = run_ffuf(target_url, WORDLIST_PATH, OUTPUT_DIR, cookies=cookies)
    ffuf_data = {} if ffuf_raw.get("skipped") else json.load(open(ffuf_raw["output_file"]))
    rutas_ffuf_nuevas = ffuf_data.get("results", [])

    # --- 3. INYECTAR RUTAS DE FFUF EN ZAP ---
    if rutas_ffuf_nuevas:
        agregar_urls_a_zap(rutas_ffuf_nuevas)

    # --- 4. ZAP ACTIVE SCAN ---
    ascan_id = iniciar_escaneo_activo(target_url)
    esperar_escaneo_activo(ascan_id, progress_callback=cb_ascan)
    reporte_zap_crudo = obtener_reporte_json()

    # --- 5. SQLMAP (sesión refrescada, URLs combinadas) ---
    lista_urls_total = list(set(spider_urls.get("results", []) +
                                [r.get("url", "") for r in rutas_ffuf_nuevas]))
    sqlmap_raw = run_sqlmap_batch(lista_urls_total, cookies=cookies,
                                  sqlmap_level=sqlmap_level)

    return {"target": target_url, "spider_raw": spider_urls,
            "zap_raw": reporte_zap_crudo, "sqlmap_raw": sqlmap_raw,
            "ffuf_raw": ffuf_data}
```

#pagebreak()
== Anexo C — Fragmento Representativo: Parser de ZAP
<anexo-c-fragmento-representativo-parser-de-zap>

```python
def parsear_zap(dato_dict_crudo):
    try:
        data = dato_dict_crudo
        vistas = set()
        alertas_parseadas = []
        for sitio in data.get("site", []):
            for alerta in sitio.get("alerts", []):
                for instancia in alerta.get("instances", []):
                    url = instancia.get("uri", "")
                    clave = (url, alerta.get("alert", ""))
                    if clave not in vistas:
                        vistas.add(clave)
                        alertas_parseadas.append({
                            "url": url,
                            "vulnerabilidad": alerta.get("alert", "Vulnerabilidad sin nombre"),
                            "severidad": alerta.get("riskdesc", "No clasificado"),
                            "metodo": instancia.get("method", "N/A"),
                            "solucion": alerta.get("solution", "No hay solucion disponible")
                        })
        return {"herramienta": "ZAP", "total_alertas": len(alertas_parseadas),
                "alertas": alertas_parseadas}
    except (KeyError, TypeError) as e:
        print(f"Error al parsear los datos de ZAP: {e}")
        return {}
```

#pagebreak()
== Anexo D — Ejemplo del JSON Unificado Final (corrida del 5 de agosto de 2026)
<anexo-d-ejemplo-del-json-unificado-final-corrida-del-5-de-agosto-de-2026>

El siguiente extracto reproduce la estructura canónica del bloque resumen
del esquema JSON unificado generado por el módulo de consolidación del
pipeline para la ejecución documentada en el capítulo 13 \(corrida del 5 de
agosto de 2026), cuyos valores concuerdan íntegramente con los documentados
en `reporte_seguridad.md`. Se presenta con fines de especificación de la
arquitectura de interoperabilidad homogénea \(validando la hipótesis H3),
dado que los volcados crudos generados en `output/raw/` no se preservaron en el
control de versiones debido a las reglas de exclusión del repositorio.

```json
{
  "resumen": {
    "total_urls_unicas": 34,
    "urls_spider": 24,
    "alertas_zap": 37,
    "rutas_ffuf": 8,
    "vulnerabilidades_sqlmap": 4
  },
  "zap": {
    "herramienta": "ZAP",
    "host": "dvwa",
    "total_alertas": 37,
    "alertas": [
      {
        "url": "http://dvwa/about.php",
        "vulnerabilidad": "Content Security Policy (CSP) Header Not Set",
        "severidad": "Medium (High)"
      }
    ]
  },
  "ffuf": {
    "herramienta": "ffuf",
    "total_rutas": 8,
    "rutas": [
      {
        "url": "http://dvwa/setup.php",
        "status": 200
      }
    ]
  },
  "sqlmap": {
    "herramienta": "SQLMAP",
    "vulnerabilidades": [
      {
        "url": "http://dvwa/vulnerabilities/brute/?Login=Login&password=ZAP&username=ZAP",
        "salida": "... Type: boolean-based blind ... parameter 'username' is vulnerable"
      }
    ]
  }
}
```

Todas las rutas reportadas usan http://dvwa/, el hostname real de la
red interna de Docker, en lugar del hostname ilustrativo target.com que
figuraba en versiones anteriores del documento; esta ejecución
corresponde a datos reales y no a un ejemplo construido.

#pagebreak()
== Anexo E — Fragmento Representativo: Autenticación Automática
<anexo-e-fragmento-representativo-autenticación-automática>

```python
def establecer_sesion_automatica(target_url):
    """Login automatico en DVWA; reintenta inicializando la BD si falla."""
    session = requests.Session()
    def intentar_login():
        r = session.get(login_url, timeout=10)
        token = re.search(r"user_token['\"] value=['\"]([^'\"]*)", r.text)
        session.post(login_url, data={"username": "admin", "password": "password",
                                      "Login": "Login", "user_token": token.group(1) if token else ""})
        r_sec = session.post(security_url, data={"security": "low", "seclev_submit": "Submit"})
        return "logout" in r_sec.text.lower()

    if intentar_login():
        return "; ".join(f"{k}={v}" for k, v in session.cookies.get_dict().items())

    # Login fallo: inicializar la base de datos de DVWA y reintentar
    session.post(setup_url, data={"create_db": "Create / Reset Database"})
    time.sleep(3)
    session.cookies.clear()
    if intentar_login():
        return "; ".join(f"{k}={v}" for k, v in session.cookies.get_dict().items())
    return None
```

#pagebreak()
== Anexo F — Fragmento Representativo: API REST
<anexo-f-fragmento-representativo-api-rest>

```python
app = FastAPI(title="Orquestador de Seguridad API", version="1.0.0")

class ScanRequest(BaseModel):
    target: str
    nivel: Optional[str] = "medium"
    cookies: Optional[str] = None
    callback_url: Optional[str] = None
    sqlmap_level: Optional[str] = "basic"

@app.post("/scan", status_code=202)
def iniciar_escaneo(request: ScanRequest, background_tasks: BackgroundTasks):
    scan_id = str(uuid.uuid4())
    create_scan(scan_id, request.target)
    background_tasks.add_task(ejecutar_pipeline_segundo_plano,
                              scan_id=scan_id,
                              target=request.target, nivel=request.nivel,
                              cookies=request.cookies, sqlmap_level=request.sqlmap_level)
    return {"message": "Escaneo lanzado", "scan_id": scan_id}

@app.get("/scan/{scan_id}/progress")
def get_scan_progress(scan_id: str):
    if scan_id in scan_progress_store:
        return scan_progress_store[scan_id]
    scan_data = get_scan_by_id(scan_id)
    if not scan_data:
        raise HTTPException(status_code=404, detail="Scan no encontrado")

    return {"percentage": 100, "message": "Analisis Completado"} if scan_data["status"] == "completed" \
        else {"percentage": 0, "message": "Iniciando o retomando analisis..."}
```

#pagebreak()


== Anexo G — Frontend: Panel de Control
<anexo-g-frontend-panel-de-control>
El frontend, desarrollado en React y TypeScript, consume la API REST del
orquestador y ofrece dos experiencias de interfaz que coexisten en el
proyecto: un panel de control con estética moderna \(glassmorphism,
gráficos interactivos) y una interfaz alternativa que recrea el
escritorio de Windows 98, con sus propios íconos de escritorio, menú de
inicio y una terminal estilo “MS-DOS Prompt” para seguir el progreso del
análisis.

Motivación de la elección de diseño. La estética retro no es un tema
visual accesorio, sino una decisión de diseño consciente del equipo,
adoptada por tres razones concretas. Primero, una razón de identidad:
distingue al proyecto de la generalidad de dashboards de seguridad con
apariencia corporativa genérica, dándole una impronta propia reconocible
dentro de un trabajo académico. Segundo, una razón de contexto cultural:
el lenguaje visual de fines de los años noventa está asociado, dentro de
la comunidad de seguridad informática, a una estética de herramienta
técnica y de acceso directo a la información, coherente con la
naturaleza ofensiva de las herramientas que el sistema orquesta.
Tercero, una razón de alcance de aprendizaje: construir una interfaz
sobre una paleta y unos patrones de interacción muy distintos a los de
un framework de diseño moderno \(ventanas arrastrables, íconos de
escritorio, una terminal simulada) implicó resolver problemas de UI que
no se presentan en un dashboard convencional, ampliando el trabajo de
frontend del equipo más allá de componentes estándar.

Panel de estado del análisis \(DomainsDashboard). Muestra el objetivo
escaneado como una tarjeta con su nivel de riesgo, la fecha del último
análisis y su estado actual, consultado mediante polling al endpoint
/scan/{id}/progress. Por las razones legales expuestas en el capítulo
16, el formulario de escaneo restringe el campo de URL objetivo,
dejándolo deshabilitado y fijo en http:\/\/dvwa; el diseño multi-dominio
queda como una capacidad arquitectónica disponible para habilitarse en
el futuro, condicionada a un flujo formal de autorización.

Sugerencias de mitigación asistidas por IA \(useAiAnalysis). Desde la
tabla de vulnerabilidades, el usuario puede solicitar una sugerencia de
mitigación para un hallazgo puntual; el frontend envía sus datos al
endpoint /api/n8n/analyze, que delega el análisis a un flujo de n8n.
Esta implementación reemplaza la propuesta original de “Idea
Complementaria”: no existe un motor de priorización de riesgo basado en
pesos configurables ni una versión con suscripción paga orientada a
terceros —esa dimensión comercial se descarta explícitamente—, y el
análisis multi-objetivo que la idea original imaginaba queda limitado,
por diseño y por las restricciones legales del capítulo 16, a un único
entorno de laboratorio autorizado \(DVWA).

#pagebreak()
== Anexo H — Diagramas en Tamaño Ampliado
<anexo-h-diagramas-en-tamaño-ampliado>
Este anexo reproduce a mayor tamaño, para su mejor observación, las
Figuras 1 a 4 ya presentadas y comentadas en las secciones 11.1, 11.2, 11.4 y
11.5: Figura 1 \(Diagrama de Arquitectura de Servicio), Figura 2
\(Diagrama Orquestador-Seguridad), Figura 3 \(Diagrama de Pipeline de
ejecución) y Figura 4 \(Diagrama de secuencia — ciclo de vida de POST
/scan).

#page(flipped: true)[
  #align(center + horizon)[
    #image("../media/media/image2.png", width: 100%, height: 84%, fit: "contain")
    #v(0.6em)
    #text(size: 10pt)[#emph[Figura 1 (ampliada). Diagrama de Arquitectura de Servicio. Elaboración propia.]] <fig-1-ampliada>
  ]
]

#align(center + horizon)[
  #image("../media/media/image1.jpg", width: 92%)
  #v(0.8em)
  #text(size: 10pt)[#emph[Figura 2 (ampliada). Diagrama Orquestador-Seguridad. Elaboración propia.]] <fig-2-ampliada>
]

#pagebreak()

#align(center + horizon)[
  #image("../media/media/image4.jpg", width: 92%)
  #v(0.8em)
  #text(size: 10pt)[#emph[Figura 3 (ampliada). Diagrama de Pipeline de ejecución. Elaboración propia.]] <fig-3-ampliada>
]

#page(flipped: true)[
  #align(center + horizon)[
    #image("../media/media/image3.png", width: 100%, height: 88%, fit: "contain")
    #v(0.6em)
    #text(size: 10pt)[#emph[Figura 4 (ampliada). Diagrama de secuencia — ciclo de vida de POST /scan. Elaboración propia.]] <fig-4-ampliada>
  ]
]

#pagebreak()

== Anexo I — Disponibilidad de Código Fuente y Recursos Audiovisuales
<anexo-i-disponibilidad-de-código-fuente-y-recursos-audiovisuales>

Con el propósito de garantizar la reproducibilidad científica, la transparencia metodológica y la verificabilidad empírica del presente trabajo final de graduación, se ponen a disposición del tribunal evaluador de la UTN Facultad Regional Mendoza y de la comunidad académica los recursos digitales que sustentan el prototipo funcional desarrollado y su correspondiente validación en tiempo real.

=== I.1 Repositorio de Código Fuente y Prototipo Funcional (GitHub)
<i.1-repositorio-de-código-fuente-y-prototipo-funcional>

El código fuente integral del orquestador, los parsers sintácticos de seguridad, las configuraciones de contenerización con Docker Compose, los scripts de automatización y el panel de control web retro se encuentran alojados y versionados en el repositorio público de GitHub:

#align(center)[
  #rect(stroke: 0.5pt + luma(150), inset: (x: 15pt, y: 10pt), radius: 4pt)[
    *Repositorio oficial:* #link("https://github.com/tomimastro069/Tesis-final")[github.com/tomimastro069/Tesis-final] \
    *Rama principal evaluada:* `main` \
    *Licencia de software:* MIT License \
    *Entorno de ejecución:* Docker Engine 24+ y Docker Compose v2+
  ]
]

*Instrucciones de clonación y despliegue rápido del entorno:*
```bash
# Clonación del repositorio oficial
git clone https://github.com/tomimastro069/Tesis-final.git
cd Tesis-final
cd orquestador-seguridad

# Despliegue de la infraestructura multicontenedor (DVWA, ZAP, App, DB, n8n)
docker compose up -d --build
```

=== I.2 Registro Audiovisual de Demostración y Pruebas Empíricas (YouTube)
<i.2-registro-audiovisual-de-demostración-y-pruebas-empíricas>

Aprobado por la Dirección del Trabajo Final, se elaboró un registro audiovisual demostrativo formal con una duración exacta de 9:00 minutos en resolución de alta definición (1080p FHD). El material documenta de manera continua el despliegue del entorno, la ejecución autónoma del pipeline secuencial de escaneo (ZAP, ffuf y SQLMap en modo de extracción completa `full_dump` y nivel de seguridad `low`), la interacción con el asistente de remediación basado en inteligencia artificial y la validación empírica del ahorro temporal provisto por el motor de caché incremental. Dicha demostración refleja una sesión independiente grabada el 15 de septiembre de 2026 (18:33 a 18:46 para la corrida basal y 19:15 a 19:18 para la optimizada) y publicada el 25 de septiembre de 2026, cuya concordancia y diferencias horarias respecto al benchmark formal del 6 de agosto (Tabla 10) se analizan en la sección 14.3.

#align(center)[
  #rect(stroke: 0.5pt + luma(150), inset: (x: 15pt, y: 10pt), radius: 4pt)[
    *Acceso al video demostrativo:* #link("https://www.youtube.com/watch?v=UA0rolg9ZKI")[youtube.com/watch?v=UA0rolg9ZKI] \
    *Título de la producción:* Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web \
    *Duración total:* 09:00 minutos exactos | *Resolución:* 1080p (Full HD) \
    *Institución:* Universidad Tecnológica Nacional — Facultad Regional Mendoza
  ]
]

A continuación, se detalla la estructura narrativa y el desglose visual por bloques cronológicos que componen la demostración audiovisual:

#pagebreak()

#strong[Tabla 14. Estructura narrativa, marcas temporales y desglose visual del video demostrativo] <tabla-14>

#[
  #set text(size: 8.5pt)
  #set par(leading: 0.50em)
  #figure(
    align(center)[#table(
      columns: (0.85fr, 1.45fr, 2.7fr),
      inset: (x: 6pt, y: 3.6pt),
      align: (center + horizon, left + horizon, left + top),
      [Bloque y Tiempo], [Apartado Visual en Pantalla], [Descripción Técnica y Contenido Demostrado],
    
      [Bloque 1\ 00:00 – 00:50\ (50 s)],
      [Pantalla principal de la interfaz de usuario retro (estilo Windows 98) con el asistente interactivo #emph[«Acerca del Proyecto»] desplegado. El cursor recorre sucesivamente las pestañas: #emph[Bienvenida], #emph[El Proyecto], #emph[Cómo Funciona] y #emph[Tecnología].],
      [Presentación formal del proyecto ante la UTN FRM. Planteo de la problemática del pentesting web manual, justificación técnica del orquestador y presentación del stack tecnológico integrando OWASP ZAP, ffuf y SQLMap en contenedores Docker coordinados por Python.],

      [Bloque 2\ 00:50 – 02:20\ (1 min 30 s)],
      [Apertura de la ventana #emph[«Analizador de Seguridad»]. Selección de la opción #emph[«Limpiar caché»], nivel de análisis #emph[«Profundo»] y SQLMap en #emph[«3 - Extracción Completa»]. Al accionar #emph[«Comenzar Análisis»], emerge la consola #emph[MS-DOS Prompt] mostrando el flujo de registros de escaneo acelerado a $16 times$.],
      [Ejecución del primer escaneo completo sin caché (13 minutos de duración real: 18:33 a 18:46). Demostración del flujo: autenticación automatizada en DVWA con obtención de cookie de sesión, rastreo con Spider de ZAP, fuzzing de directorios con ffuf e inyección dinámica de rutas hacia ZAP activo y SQLMap.],

      [Bloque 3\ 02:20 – 04:50\ (2 min 30 s)],
      [02:20: #emph[Explorador de Reportes] y ventana #emph[System Properties] con tarjeta verde de estado. \
      03:00: Pestaña #emph[Device Manager] con el listado exhaustivo de vulnerabilidades por severidad. \
      03:45: Inspección de vulnerabilidad, selección de pestaña #emph[AI Analysis] y activación del botón #emph[«Analyze with AI»]. \
      04:10: Pestaña #emph[Performance] con gráficos de barras. \
      04:30: Pestaña #emph[ODBC Data Sources] con las tablas `dvwa.users` y `dvwa.guestbook`.],
      [Consolidación y auditoría de resultados: resumen métrico de 59 URLs analizadas (54 descubiertas por Spider, 48 alertas de ZAP y 8 hallazgos de SQLMap). Clasificación de criticidad en Device Manager, generación interactiva de guías de remediación con fragmentos de código mediante IA y comprobación de la extracción efectiva de datos relacionales con hashes MD5.],

      [Bloque 4\ 04:50 – 06:40\ (1 min 50 s)],
      [Apertura de la utilidad de contraste #emph[WinDiff - dvwa vs dvwa]. Visualización comparativa a doble panel: panel izquierdo (amarillo) correspondiente a la ejecución #emph[«Con Caché»] y panel derecho (verde) al análisis basal #emph[«Sin Caché»].],
      [Evaluación analítica del impacto del motor de caché: demostración de más de 207.000 palabras omitidas por ffuf al no detectar alteraciones en la superficie y descarte inteligente en SQLMap de URLs sin hallazgos previos re-testeando únicamente endpoints vulnerables, manteniendo 100% de coincidencia en vulnerabilidades críticas.],

      [Bloque 5\ 06:40 – 08:20\ (1 min 40 s)],
      [06:40: Configuración de nuevo escaneo con la casilla de limpiar caché desmarcada. \
      07:00: Ejecución en consola acelerada ($16 times$) con rótulo temporal: #emph[«Análisis con caché: 19:15 - 19:18»]. \
      07:40: Apertura de reportes con la tarjeta amarilla distintiva de análisis optimizado por caché.],
      [Demostración empírica de reducción de tiempos en vivo: conclusión del pipeline completo en 3 minutos frente a los 13 minutos iniciales de la sesión grabada el 15 de septiembre de 2026, evidenciando una reducción temporal aproximada del 77% (10 minutos economizados) sin degradación de cobertura ni alteración de hallazgos, en consonancia cualitativa con el 68,9% documentado formalmente en la Tabla 10.],

      [Bloque 6\ 08:20 – 09:00\ (40 s)],
      [Pantalla de cierre formal del proyecto con el logotipo oficial de la Universidad Tecnológica Nacional (UTN) y los datos institucionales del trabajo final.],
      [Conclusiones finales sobre la viabilidad del orquestador SOAR liviano, balance costo-beneficio de la caché incremental y agradecimientos protocolares a los directores del trabajo final y al tribunal evaluador de la UTN FRM.]
    )],
  )
]

#v(0.3em)
#text(size: 9.5pt)[#emph[Nota. Elaboración propia a partir del guion técnico y registro audiovisual del proyecto (Mastropietro et al., 2026b).]]


