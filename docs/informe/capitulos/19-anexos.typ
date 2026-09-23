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

RUN wget https://github.com/ffuf/ffuf/releases/download/v${FFUF_VERSION}/ffuf_${FFUF_VERSION}_linux_amd64.tar.gz \
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

El siguiente extracto reproduce el campo resumen del archivo
resultado_unificado.json de la ejecución documentada en el capítulo 13,
verificable directamente en el repositorio del proyecto.

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
Figuras 1 a 4 ya presentadas y comentadas en las secciones 11.1, 11.4 y
11.5: Figura 1 \(Diagrama de Arquitectura de Servicio), Figura 2
\(Diagrama Orquestador-Seguridad), Figura 3 \(Diagrama de Pipeline de
ejecución) y Figura 4 \(Diagrama de secuencia — ciclo de vida de POST
/scan).



#align(center)[
  #image("../media/media/image2.png", width: 100%)
  #v(0.5em)
  #text(size: 10pt)[#emph[Figura 1 (ampliada). Diagrama de Arquitectura de Servicio. Elaboración propia.]] <fig-1-ampliada>
]

#pagebreak()

#align(center)[
  #image("../media/media/image1.jpg", width: 100%)
  #v(0.5em)
  #text(size: 10pt)[#emph[Figura 2 (ampliada). Diagrama Orquestador-Seguridad. Elaboración propia.]] <fig-2-ampliada>
]

#pagebreak()

#align(center)[
  #image("../media/media/image4.jpg", width: 92%)
  #v(0.5em)
  #text(size: 10pt)[#emph[Figura 3 (ampliada). Diagrama del Pipeline de Ejecución. Elaboración propia.]] <fig-3-ampliada>
]

#pagebreak()

#align(center)[
  #image("../media/media/image3.png", width: 100%)
  #v(0.5em)
  #text(size: 10pt)[#emph[Figura 4 (ampliada). Diagrama de secuencia UML. Elaboración propia.]] <fig-4-ampliada>
]


