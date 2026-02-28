# Informe Técnico — Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web

---

## Portada

| Campo           | Detalle                                                            |
| --------------- | ------------------------------------------------------------------ |
| **Título**      | Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web |
| **Autores**     | Cristian Krahulik · Tomas Mastropietro · Juan Segura               |
| **Materia**     | Seguridad Ofensiva                                                 |
| **Fecha**       | Febrero 2026                                                       |
| **Repositorio** | `orquestador-seguridad/`                                           |

---

## Resumen

Este trabajo presenta el diseño e implementación de un sistema de **fuzzing automatizado** para aplicaciones web, desarrollado íntegramente en Python. El sistema recibe una URL objetivo y ejecuta en forma secuencial y coordinada cuatro herramientas de seguridad: OWASP ZAP (spider y escaneo activo), ffuf (fuzzing de directorios) y SQLMap (detección de inyecciones SQL). Cada herramienta actúa de forma independiente dentro de un contenedor Docker; el orquestador Python consume sus APIs y salidas, normaliza los datos crudos mediante parsers especializados y produce un único archivo JSON consolidado con todos los hallazgos. El enfoque adoptado propone una arquitectura modular donde cada componente tiene una responsabilidad única y bien delimitada, facilitando la extensibilidad y el mantenimiento del sistema.

**Palabras clave:** fuzzing, OWASP ZAP, ffuf, SQLMap, Docker, Python, seguridad web, automatización, DVWA, OWASP Top 10.

---

## 1. Introducción

Las aplicaciones web representan uno de los principales vectores de ataque en entornos de producción. Errores de validación de entrada, configuraciones inseguras, rutas expuestas involuntariamente y endpoints sin protección son vulnerabilidades que, a pesar de ser conocidas y documentadas por la comunidad (OWASP Top 10), siguen siendo frecuentes en sistemas reales.

El **fuzzing** es una técnica de prueba de seguridad que consiste en enviar entradas automatizadas, inesperadas o malformadas a una aplicación con el objetivo de descubrir comportamientos anómalos, rutas ocultas o vulnerabilidades explotables. A diferencia de un análisis estático o una revisión manual de código, el fuzzing actúa sobre la aplicación en ejecución y puede detectar problemas que solo se manifiestan en tiempo de corrida.

El presente proyecto construye un **orquestador** —no un nuevo scanner— que coordina herramientas de fuzzing y análisis de seguridad ya existentes y probadas, automizando el flujo completo: descubrimiento de superficie de ataque, análisis de vulnerabilidades, fuzzing de directorios, detección de inyecciones SQL, normalización de resultados y consolidación en un reporte unificado.

### 1.1 Objetivo general

Diseñar e implementar un sistema automatizado en Python que orqueste múltiples herramientas de seguridad sobre una URL objetivo y produzca un reporte consolidado de hallazgos.

### 1.2 Objetivos específicos

1. Integrar OWASP ZAP (spider + active scan), ffuf y SQLMap en un flujo de ejecución secuencial.
2. Diseñar parsers que normalicen las salidas crudas heterogéneas de cada herramienta.
3. Consolidar los resultados eliminando duplicados y organizando la información por herramienta.
4. Orquestar todo el entorno de laboratorio mediante contenedores Docker reproducibles.
5. Mantener una arquitectura modular con responsabilidad única por componente.

### 1.3 Alcance y limitaciones

El sistema fue diseñado y probado sobre un entorno de laboratorio controlado, usando **DVWA** (Damn Vulnerable Web Application) como objetivo. No se realizaron pruebas sobre aplicaciones en producción. El módulo de generación de reportes en formato humano (Markdown/PDF) está planificado pero no implementado en la versión actual.

---

## 2. Marco Teórico

### 2.1 Fuzzing web

El fuzzing web puede clasificarse en tres categorías según su objetivo:

| Tipo                       | Descripción                                                                                | Herramienta utilizada   |
| -------------------------- | ------------------------------------------------------------------------------------------ | ----------------------- |
| **Fuzzing de directorios** | Prueba rutas y archivos mediante listas de palabras para descubrir recursos ocultos        | ffuf                    |
| **Fuzzing de parámetros**  | Inyecta valores anómalos en parámetros GET/POST para encontrar comportamientos inesperados | SQLMap, ZAP Active Scan |
| **Escaneo activo/pasivo**  | Analiza las respuestas HTTP en busca de patrones de vulnerabilidades conocidas             | OWASP ZAP               |

A diferencia del fuzzing de caja negra puro, el enfoque adoptado combina las tres estrategias de forma secuencial y coordinada, usando la salida de un paso como entrada del siguiente (por ejemplo, las URLs descubiertas por el spider de ZAP son utilizadas por SQLMap).

### 2.2 OWASP Top 10

La fundación OWASP (Open Worldwide Application Security Project) publica periódicamente un ranking de las diez categorías de vulnerabilidades web más críticas. El sistema implementado apunta específicamente a detectar vulnerabilidades de las siguientes categorías:

- **A01 — Broken Access Control:** rutas y recursos a los que se accede sin autorización, detectables mediante fuzzing de directorios.
- **A03 — Injection:** inyecciones SQL, XSS y similares, detectadas por ZAP Active Scan y SQLMap.
- **A05 — Security Misconfiguration:** cabeceras de seguridad ausentes, información expuesta en respuestas de error, detectadas por ZAP.
- **A07 — Identification and Authentication Failures:** formularios de login y endpoints de autenticación expuestos, detectables mediante spider y fuzzing.

### 2.3 Herramientas utilizadas

#### 2.3.1 OWASP ZAP (Zed Attack Proxy)

ZAP es un escáner de seguridad web open source mantenido por la fundación OWASP. Ofrece dos modos de análisis:

- **Spider (rastreador):** recorre la aplicación siguiendo enlaces y mapeando todos los endpoints disponibles. Devuelve una lista de URLs descubiertas.
- **Active Scan (escaneo activo):** envía requests activamente modificados a cada URL encontrada, buscando vulnerabilidades como inyecciones, XSS, CSRF y otros patrones del OWASP Top 10. Genera alertas clasificadas por severidad (High, Medium, Low, Informational).

ZAP expone una **API REST** completa que permite iniciar y monitorear ambos modos de forma programática, lo cual fue fundamental para su integración en el pipeline Python.

#### 2.3.2 ffuf (Fast Web Fuzzer)

ffuf es un fuzzer web de alto rendimiento escrito en Go. Su función principal es probar sistemáticamente rutas y directorios en un servidor web usando una lista de palabras (wordlist). Soporta salida en formato JSON estructurado, lo que facilita su integración en pipelines automatizados. Permite filtrar resultados por código de estado HTTP, tamaño de respuesta y tiempo de respuesta.

#### 2.3.3 SQLMap

SQLMap es una herramienta open source de detección y explotación de inyecciones SQL. Recibe una URL con parámetros GET y prueba automáticamente múltiples técnicas de inyección SQL (boolean-based, time-based, union-based, etc.). El flag `--batch` permite ejecutarlo en modo completamente automático sin interacción del usuario.

#### 2.3.4 Docker y Docker Compose

Docker permite contenerizar cada servicio de forma aislada. Docker Compose permite definir y levantar múltiples contenedores con sus dependencias y configuración de red en un solo comando (`docker compose up --build -d`). El uso de contenedores garantiza que el entorno sea **reproducible** independientemente del sistema operativo del host.

#### 2.3.5 DVWA (Damn Vulnerable Web Application)

DVWA es una aplicación web PHP/MySQL intencionalmente vulnerable, diseñada para entornos de práctica y educación en seguridad. Contiene implementaciones vulnerables de formularios de login, consultas SQL, carga de archivos, XSS y más. Se utilizó como objetivo de pruebas por ser un entorno controlado y conocido.

### 2.4 Decisión de arquitectura: Python puro vs. n8n

El plan original del proyecto contemplaba usar **n8n** como orquestador low-code. Tras una evaluación técnica, el equipo decidió implementar el orquestador directamente en **Python puro** por las siguientes razones:

#### Problema de infraestructura con n8n como orquestador único

n8n es una plataforma de automatización de flujos de trabajo que corre como un servidor Node.js dentro de su propio contenedor. Para usar n8n como orquestador **sin un proyecto Python externo**, n8n tendría que ser responsable de ejecutar directamente las herramientas de seguridad (ffuf, ZAP spider, ZAP active scan, SQLMap) mediante nodos de ejecución de comandos.

Esto implicaría instalar todas esas herramientas **dentro del mismo contenedor de n8n**:

```
Contenedor n8n (problema)
├── Servidor n8n (Node.js)
├── ffuf (binario Go ~10 MB)
├── sqlmap (Python + dependencias)
├── zap.sh (Java, ~500 MB)        ← ZAP requiere JVM
└── Base de datos PostgreSQL
```

Este enfoque presenta problemas concretos:

1. **Contaminación del servidor de orquestación:** n8n es una herramienta de automatización genérica. Instalarle herramientas especializadas de pentesting (que son pesadas, requieren runtimes distintos y tienen sus propias dependencias) rompe el principio de responsabilidad única del contenedor.

2. **ZAP requiere Java:** OWASP ZAP es una aplicación Java que necesita una JVM para correr. Instalar una JVM dentro del contenedor de n8n (que es Node.js) lo vuelve innecesariamente pesado y complejo.

3. **Mantenimiento difícil:** al tener múltiples herramientas con runtimes distintos (Node.js para n8n, Go para ffuf, Python para SQLMap, Java para ZAP) en un solo contenedor, las actualizaciones y el debugging se vuelven significativamente más complejos.

4. **Docker ya resuelve esto mejor:** la solución correcta para ejecutar múltiples servicios especializados es tener **un contenedor por responsabilidad** (principio de Docker), no acumular herramientas en un único servidor.

La alternativa adoptada —un contenedor Python dedicado al orquestador— delega ZAP a su propio contenedor oficial (`ghcr.io/zaproxy/zaproxy`) e instala solo ffuf y SQLMap dentro del contenedor Python, que son herramientas ligeras sin JVM.

#### Comparación técnica general

| Criterio                            | n8n como orquestador único          | Python puro + contenedores separados |
| ----------------------------------- | ----------------------------------- | ------------------------------------ |
| Control sobre el flujo              | Limitado a nodos visuales           | Total, programático                  |
| Integración con APIs REST           | Soportada con nodos HTTP            | Nativa con biblioteca `requests`     |
| Manejo de errores y timeouts        | Básico                              | Granular por operación               |
| Pruebas unitarias                   | No nativas                          | Soporte completo (`pytest`)          |
| Dependencias en el mismo contenedor | ffuf + sqlmap + ZAP + JVM + Node.js | Solo ffuf + sqlmap (Python)          |
| ZAP                                 | Instalado en el servidor de n8n     | Contenedor oficial propio            |
| Imagen Docker resultante            | Muy pesada (~1 GB+)                 | Liviana (python:3.11-slim base)      |
| Reproducibilidad                    | Compleja, múltiples runtimes        | Clara, un runtime por contenedor     |

La decisión de usar Python puro permitió mantener cada herramienta en su propio contenedor o espacio de responsabilidad, un control más granular del flujo de ejecución y un manejo de errores más robusto.

---

## 3. Arquitectura del Sistema

### 3.1 Infraestructura: contenedores Docker

El sistema se despliega mediante **Docker Compose** con tres servicios interconectados en una red interna:

```
┌──────────────────────────────────────────────────────────────┐
│                    Red interna Docker                        │
│                                                              │
│  ┌─────────────────┐    ┌──────────────────┐                │
│  │   dvwa           │    │   zap             │               │
│  │  (objetivo)      │◄───│  (API REST :8090) │               │
│  │  :8080           │    │  ghcr.io/zaproxy  │               │
│  └─────────────────┘    └──────────────────┘               │
│           ▲                       ▲                          │
│           │                       │                          │
│  ┌─────────────────────────────────────────┐                │
│  │          security-app (Python)           │                │
│  │          orquestador principal           │                │
│  │          ffuf + sqlmap incluidos         │                │
│  └─────────────────────────────────────────┘                │
└──────────────────────────────────────────────────────────────┘
```

El contenedor `security-app` se construye a partir de una imagen `python:3.11-slim` a la que se le instalan `ffuf` (binario oficial v2.1.0) y `sqlmap` (clonado desde GitHub) directamente en el Dockerfile. ZAP y DVWA corren en sus propios contenedores y se comunican con el orquestador a través de la red interna de Docker.

El archivo `docker-compose.yml` define los tres servicios:

```yaml
services:
  dvwa: # Aplicación vulnerable objetivo (puerto 8080)
  zap: # OWASP ZAP daemon con API REST (puerto 8090)
  app: # Orquestador Python con ffuf y sqlmap integrados
```

### 3.2 Arquitectura modular del orquestador

El código Python sigue una arquitectura modular estricta donde cada paquete tiene una única responsabilidad:

```
orquestador-seguridad/
├── main.py                   # Punto de entrada único
└── app/
    ├── runners/
    │   └── exec.py           # Ejecución de procesos externos
    ├── scanners/
    │   ├── zap.py            # Comunicación con la API REST de ZAP
    │   ├── ffuf.py           # Ejecución y configuración de ffuf
    │   └── sqlmap.py         # Ejecución y filtrado de URLs para SQLMap
    ├── parsers/
    │   ├── zap_parser.py     # Normalización de alertas y URLs de ZAP
    │   ├── ffuf_parser.py    # Filtrado y normalización de rutas de ffuf
    │   └── sqlmap_parser.py  # Procesamiento de resultados de SQLMap
    ├── workflow/
    │   └── pipeline.py       # Orquestación del flujo completo
    ├── utils/
    │   └── results.py        # Consolidación y persistencia de resultados
    └── config/
        └── settings.py       # Variables de configuración centralizadas
```

### 3.3 Diagrama de flujo de datos

```
URL objetivo (input)
        │
        ▼
┌───────────────────┐
│  run_security_    │   ← pipeline.py (orquestador)
│  pipeline()       │
└───────┬───────────┘
        │
        ├─── [1] ZAP Spider ──────────────► spider_urls (JSON crudo)
        │         iniciar_spider()
        │         esperar_spider()
        │         obtener_urls()
        │
        ├─── [2] ZAP Active Scan ─────────► reporte_zap_crudo (JSON)
        │         iniciar_escaneo_activo()
        │         esperar_escaneo_activo()
        │         obtener_reporte_json()
        │
        ├─── [3] SQLMap ──────────────────► sqlmap_raw (lista de dicts)
        │         filtrar_urls_con_parametros()
        │         run_sqlmap_batch()
        │
        └─── [4] ffuf ────────────────────► ffuf_raw.json (archivo)
                  run_ffuf()
                         │
                         ▼
              hallazgos_finales (dict)
              guardado en resultado.json
                         │
                         ▼
        ┌───────────────────────────┐
        │  run_parser_pipeline()    │   ← pipeline.py (fase parseo)
        └───────────┬───────────────┘
                    │
                    ├─── parsear_spider()  ──► dict normalizado (Spider)
                    ├─── parsear_zap()   ───► dict normalizado (ZAP)
                    ├─── parsear_ffuf()  ───► dict normalizado (ffuf)
                    └─── parsear_sqlmap() ──► dict normalizado (SQLMap)
                                   │
                                   ▼
                    consolidar_resultados()
                                   │
                                   ▼
                    resultado_unificado.json (output final)
```

---

## 4. Implementación

### 4.1 Entorno de laboratorio (Docker Compose)

El entorno completo se levanta con un único comando:

```bash
cd orquestador-seguridad
docker compose up --build -d
```

Esto construye la imagen del orquestador (instalando Python 3.11, ffuf y sqlmap) y levanta los tres servicios en paralelo. El servicio `app` depende de `zap` y `dvwa`, por lo que Docker Compose garantiza el orden de arranque.

El Dockerfile del orquestador instala ffuf descargando el binario oficial compilado para Linux AMD64, y clona sqlmap directamente desde su repositorio oficial en `/opt/sqlmap`:

```dockerfile
FROM python:3.11-slim

# Instalar ffuf (binario oficial v2.1.0)
RUN wget https://github.com/ffuf/ffuf/releases/latest/download/ffuf_2.1.0_linux_amd64.tar.gz \
    && tar -xzf ffuf_2.1.0_linux_amd64.tar.gz \
    && mv ffuf /usr/local/bin/ffuf

# Instalar SQLMap (repositorio oficial)
RUN git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git /opt/sqlmap
```

### 4.2 Módulo Runners — `app/runners/exec.py`

El runner es la capa más baja del sistema. Provee una función única `run_command()` que encapsula `subprocess.run` con manejo de errores, timeouts y diferentes tipos de fallo:

```python
def run_command(command, timeout=60) -> dict:
    # Retorna siempre un dict estructurado:
    # {
    #   "success": bool,
    #   "stdout": str,
    #   "stderr": str,
    #   "returncode": int | None,
    #   "timeout": bool,
    #   "error_type": None | "execution_error" | "timeout" | "system_error"
    # }
```

Centralizar la ejecución de subprocesos en un único lugar tiene tres ventajas clave:

1. **Evita código duplicado**: tanto ffuf como sqlmap usan el mismo runner.
2. **Uniformidad de errores**: cualquier problema de ejecución externa retorna siempre el mismo formato de dict.
3. **Timeout configurable**: cada herramienta puede definir su propio límite de tiempo (ffuf usa 60s por defecto, sqlmap usa 300s dado que puede tardar más en análisis complejos).

### 4.3 Módulo Scanners

#### 4.3.1 Scanner ZAP — `app/scanners/zap.py`

El scanner de ZAP implementa 6 funciones que mapean directamente a llamadas a la API REST de ZAP:

| Función                    | Endpoint ZAP                        | Descripción                                       |
| -------------------------- | ----------------------------------- | ------------------------------------------------- |
| `iniciar_spider()`         | `POST /JSON/spider/action/scan/`    | Inicia el rastreo, devuelve `scan_id`             |
| `esperar_spider()`         | `GET /JSON/spider/view/status/`     | Polling cada 2s hasta progreso = 100%             |
| `obtener_urls()`           | `GET /JSON/spider/view/results/`    | Retorna lista de URLs descubiertas                |
| `iniciar_escaneo_activo()` | `POST /JSON/ascan/action/scan/`     | Inicia active scan con fuerza LOW y umbral MEDIUM |
| `esperar_escaneo_activo()` | `GET /JSON/ascan/view/status/`      | Polling cada 5s hasta progreso = 100%             |
| `obtener_reporte_json()`   | `GET /OTHER/core/other/jsonreport/` | Obtiene el reporte completo con alertas           |

El modelo de espera activa (polling loop) fue la estrategia elegida para sincronizar el pipeline Python con los procesos asincrónicos de ZAP, ya que ZAP no provee webhooks ni callbacks.

#### 4.3.2 Scanner ffuf — `app/scanners/ffuf.py`

La función `run_ffuf()` construye el comando de ffuf y lo delega al runner. Los parámetros clave del comando son:

```bash
ffuf -u {target}/FUZZ \
     -w {wordlist} \
     -e .php \          # también prueba rutas con extensión .php
     -mc 200,302 \      # filtra por códigos de éxito y redirección
     -of json \         # salida en formato JSON
     -o ffuf_raw.json
```

La decisión de filtrar solo códigos 200 y 302 reduce el ruido eliminando respuestas de error (404, 403) que no indican recursos accesibles.

#### 4.3.3 Scanner SQLMap — `app/scanners/sqlmap.py`

SQLMap requiere URLs con parámetros GET para inyectar payloads. El módulo implementa tres funciones:

- `filtrar_urls_con_parametros()`: filtra de la lista del spider solo las URLs que contienen `?`, ya que sin parámetros SQLMap no tiene dónde probar.
- `run_sqlmap()`: ejecuta SQLMap contra una URL individual con flags `--batch --random-agent --level=2 --risk=2`.
- `run_sqlmap_batch()`: itera sobre todas las URLs filtradas y ejecuta SQLMap en cada una secuencialmente.

El nivel 2 de profundidad y riesgo 2 representan un balance entre exhaustividad del análisis y tiempo de ejecución.

### 4.4 Módulo Parsers

Los parsers son responsables de transformar los datos crudos y heterogéneos de cada herramienta en estructuras Python uniformes y limpias.

#### 4.4.1 Parser ZAP — `parsear_zap()`

El JSON de ZAP tiene una estructura anidada compleja: `site → alerts → instances`. Cada alerta puede afectar múltiples URLs (instancias). El parser aplana esta estructura en una lista plana de registros únicos por combinación `(url, vulnerabilidad)`, utilizando un `set` para la deduplicación:

```python
# Estructura de salida normalizada:
{
    "herramienta": "ZAP",
    "fecha": "...",
    "host": "dvwa",
    "total_alertas": 12,
    "alertas": [
        {
            "url": "http://dvwa/login.php",
            "vulnerabilidad": "SQL Injection",
            "severidad": "High (Risk=3, Confidence=3)",
            "solucion": "Use parameterized queries..."
        },
        ...
    ]
}
```

#### 4.4.2 Parser Spider — `parsear_spider()`

El endpoint `/JSON/spider/view/results/` devuelve `{"results": ["url1", "url2", ...]}`. El parser elimina duplicados y normaliza cada URL en un diccionario:

```python
{
    "herramienta": "ZAP Spider",
    "total_urls": 45,
    "urls": [{"url": "http://dvwa/login.php"}, ...]
}
```

#### 4.4.3 Parser ffuf — `parsear_ffuf()`

ffuf produce un JSON con array `results`, donde cada elemento tiene `url`, `status`, `length`, `words` y más campos. El parser filtra solo los resultados con código 200 o 302, elimina duplicados por URL y extrae los campos relevantes:

```python
{
    "herramienta": "ffuf",
    "total_rutas": 8,
    "rutas": [
        {"url": "http://dvwa/admin", "input": {"FUZZ": "admin"}, "status": 200},
        ...
    ]
}
```

### 4.5 Módulo Pipeline — `app/workflow/pipeline.py`

El pipeline implementa dos funciones públicas que representan las dos fases del sistema:

**`run_security_pipeline(target_url)`** — Fase de escaneo:

1. Ejecuta ZAP Spider y espera su finalización.
2. Ejecuta ZAP Active Scan y espera su finalización.
3. Ejecuta SQLMap sobre las URLs con parámetros del spider.
4. Ejecuta ffuf sobre el target base.
5. Empaqueta todos los resultados crudos en un dict y los guarda en `output/raw/resultado.json`.

**`run_parser_pipeline(resultado_escaneo)`** — Fase de parseo:

1. Separa los datos crudos por herramienta.
2. Llama al parser correspondiente de cada herramienta.
3. Consolida los cuatro resultados parseados.
4. Retorna la estructura unificada.

### 4.6 Módulo Utils — Consolidación de resultados

La función `consolidar_resultados()` recibe los cuatro dicts normalizados y produce la estructura final:

```python
{
    "resumen": {
        "total_urls_unicas": 52,   # URLs únicas en todo el sistema
        "urls_spider": 45,
        "alertas_zap": 12,
        "rutas_ffuf": 8,
        "vulnerabilidades_sqlmap": 2
    },
    "spider": { ... },   # resultado completo del spider
    "zap":    { ... },   # alertas normalizadas de ZAP
    "ffuf":   { ... },   # rutas descubiertas por ffuf
    "sqlmap": { ... }    # vulnerabilidades SQL encontradas
}
```

El cálculo de `total_urls_unicas` utiliza un `set` de Python que agrega URLs de todas las fuentes, garantizando que una URL descubierta tanto por el spider como por ffuf se cuente solo una vez.

### 4.7 Punto de entrada — `main.py`

El punto de entrada es un script mínimo y sin lógica propia. Su único rol es llamar al pipeline en orden y mostrar confirmación al usuario:

```python
target = "http://dvwa"

resultado_escaneo = run_security_pipeline(target)
resultado_parseo = run_parser_pipeline(resultado_escaneo)
resultados_prueba_json(resultado_parseo)
```

Este diseño es intencional: toda la lógica vive en el pipeline, y `main.py` solo actúa como interfaz de inicio. Esto facilita que el sistema sea invocado desde otros contextos (tests, schedulers, APIs) sin modificar el punto de entrada.

---

## 5. División del trabajo

El proyecto se organizó en tres perfiles con responsabilidades diferenciadas:

| Perfil                                      | Integrante         | Módulos a cargo                                                                               |
| ------------------------------------------- | ------------------ | --------------------------------------------------------------------------------------------- |
| **Ingeniero de Ejecución**                  | Tomas Mastropietro | Infraestructura Docker, `runners/exec.py`, `scanners/zap.py`, `scanners/ffuf.py`              |
| **Arquitecto de Lógica**                    | Cristian Krahulik  | `parsers/zap_parser.py`, `parsers/ffuf_parser.py`, `workflow/pipeline.py`, `utils/results.py` |
| **Especialista en Configuración y Entrega** | Juan Segura        | `config/settings.py`, `reports/generator.py`, `main.py`, `requirements.txt`                   |

El protocolo de integración acordado fue que todos los parsers deben devolver un dict con la clave `"herramienta"` y una lista de hallazgos en clave uniforme, para que `consolidar_resultados()` pueda procesarlos sin conocer el origen específico de cada dato.

---

## 6. Resultados

### 6.1 Estado de implementación

| Componente                        | Estado             | Observaciones                                              |
| --------------------------------- | ------------------ | ---------------------------------------------------------- |
| Entorno Docker (DVWA + ZAP + App) | ✅ Completo        | 3 servicios funcionales en `docker-compose.yml`            |
| `runners/exec.py`                 | ✅ Completo        | Subprocess con timeout y manejo de errores                 |
| `scanners/zap.py`                 | ✅ Completo        | 6 funciones: spider, active scan, reporte JSON             |
| `scanners/ffuf.py`                | ✅ Completo        | Ejecución con filtro 200/302 y salida JSON                 |
| `scanners/sqlmap.py`              | ✅ Completo        | Filtrado de URLs con parámetros + ejecución batch          |
| `parsers/zap_parser.py`           | ✅ Completo        | Aplanamiento y deduplicación de alertas                    |
| `parsers/ffuf_parser.py`          | ✅ Completo        | Filtrado por código HTTP, deduplicación                    |
| `parsers/sqlmap_parser.py`        | ✅ Completo        | Procesamiento de salida de SQLMap                          |
| `workflow/pipeline.py`            | ✅ Completo        | Orquestación completa en 2 fases                           |
| `utils/results.py`                | ✅ Completo        | Consolidación y persistencia JSON                          |
| `main.py`                         | ✅ Completo        | Punto de entrada mínimo                                    |
| `config/settings.py`              | ⚠️ Pendiente       | Variables de configuración aún hardcodeadas en cada módulo |
| `reports/generator.py`            | ❌ No implementado | Generación de reporte legible (Markdown/PDF)               |

### 6.2 Archivos de salida generados

El sistema produce tres archivos en la carpeta `output/raw/`:

| Archivo                    | Contenido                                            |
| -------------------------- | ---------------------------------------------------- |
| `resultado.json`           | Datos crudos de las cuatro herramientas (pre-parseo) |
| `ffuf_raw.json`            | Salida directa de ffuf en formato JSON nativo        |
| `resultado_unificado.json` | Datos normalizados y consolidados (output final)     |

### 6.3 Estructura del output final

El archivo `resultado_unificado.json` tiene la siguiente estructura de alto nivel:

```json
{
    "resumen": {
        "total_urls_unicas": 52,
        "urls_spider": 45,
        "alertas_zap": 12,
        "rutas_ffuf": 8,
        "vulnerabilidades_sqlmap": 2
    },
    "spider": {
        "herramienta": "ZAP Spider",
        "total_urls": 45,
        "urls": [ ... ]
    },
    "zap": {
        "herramienta": "ZAP",
        "total_alertas": 12,
        "alertas": [
            {
                "url": "http://dvwa/vulnerabilities/sqli/",
                "vulnerabilidad": "SQL Injection",
                "severidad": "High (Risk=3, Confidence=3)",
                "solucion": "Do not trust client side input..."
            }
        ]
    },
    "ffuf": {
        "herramienta": "ffuf",
        "total_rutas": 8,
        "rutas": [ ... ]
    },
    "sqlmap": { ... }
}
```

---

## 7. Discusión

### 7.1 Decisiones de diseño y justificación

**Separación de fases (scan vs. parse):** El pipeline se divide en dos fases explícitas. La primera fase ejecuta todas las herramientas y guarda los datos crudos. La segunda fase los parsea y consolida. Esta separación permite reejecutar el parseo sin necesidad de volver a correr las herramientas (que pueden tardar varios minutos), facilitando el debugging y el desarrollo iterativo de los parsers.

**Deduplicación en parsers:** Cada parser implementa su propia lógica de deduplicación usando `set` de Python. Esto evita que una misma URL aparezca múltiples veces en el reporte final, solo porque fue detectada por más de una herramienta o en múltiples instancias de la misma alerta.

**Modelo de polling para ZAP:** La API de ZAP es asíncrona (los escaneos ocurren en background). El sistema implementa loops de polling con `time.sleep()` entre consultas de estado. El spider usa intervalos de 2 segundos y el active scan usa intervalos de 5 segundos, dado que el active scan es significativamente más lento.

### 7.2 Desviaciones respecto al plan original

La implementación final difiere del plan original en los siguientes puntos:

| Aspecto       | Plan original                  | Implementación real                    |
| ------------- | ------------------------------ | -------------------------------------- |
| Orquestador   | n8n (low-code)                 | Python puro                            |
| Base de datos | PostgreSQL para resultados     | Archivos JSON locales                  |
| Reporte       | Markdown + Email/Slack         | JSON estructurado (Markdown pendiente) |
| CI/CD         | Integración con GitHub Actions | No implementado                        |
| Configuración | `settings.py` centralizado     | Variables hardcodeadas en cada módulo  |

La decisión más significativa fue reemplazar n8n por Python puro. Esto simplificó la infraestructura (un contenedor menos) y permitió un control más granular del flujo de ejecución.

### 7.3 Limitaciones actuales

- **Configuración hardcodeada:** los valores de `ZAP_HOST`, `ZAP_PORT`, `API_KEY` y rutas de wordlists están definidos directamente en el código fuente. Sería más robusto centralizarlos en `config/settings.py` o leerlos de variables de entorno.
- **Reporte legible ausente:** el output actual es un JSON técnico. Un integrante del equipo no técnico no puede leer directamente `resultado_unificado.json`. La implementación de `reports/generator.py` es el próximo paso crítico.
- **Entorno de pruebas controlado:** todos los resultados se obtuvieron sobre DVWA, una aplicación diseñada para ser vulnerable. El comportamiento del sistema sobre aplicaciones reales puede variar significativamente (WAFs, autenticación, rate limiting).

---

## 8. Conclusiones

### 8.1 Logros alcanzados

Se implementó exitosamente un orquestador de seguridad que:

1. **Integra cuatro herramientas heterogéneas** (ZAP, ffuf, SQLMap, DVWA) en un pipeline secuencial y automatizado.
2. **Normaliza datos de fuentes diferentes** mediante parsers especializados que producen estructuras uniformes.
3. **Consolida múltiples hallazgos** en un único archivo JSON sin duplicados.
4. **Opera en un entorno completamente contenerizado** y reproducible con un solo comando Docker Compose.
5. **Mantiene una arquitectura modular** donde cada componente puede ser probado, modificado o reemplazado de forma independiente.

El sistema demuestra que es posible construir un pipeline de seguridad funcional combinando herramientas open source existentes, sin necesidad de implementar capacidades de análisis propias. El valor del proyecto reside en la orquestación, normalización y consolidación —no en las herramientas en sí.

### 8.2 Trabajo futuro

| Prioridad | Tarea                                             | Impacto                               |
| --------- | ------------------------------------------------- | ------------------------------------- |
| 🔴 Alta   | Implementar `reports/generator.py` (Markdown/PDF) | Hace el output consumible por humanos |
| 🔴 Alta   | Centralizar configuración en `settings.py`        | Elimina valores hardcodeados          |
| 🟡 Media  | Clasificación de severidad CVSS                   | Permite priorizar remediación         |
| 🟡 Media  | Documentar `README.md`                            | Facilita uso por terceros             |
| 🟢 Baja   | Integración CI/CD (GitHub Actions)                | Automatización continua               |
| 🟢 Baja   | Pruebas autenticadas (login + cookies)            | Mayor cobertura de escaneo            |
| 🟢 Baja   | Almacenamiento en base de datos                   | Historial de escaneos                 |

---

## 9. Referencias

1. OWASP Foundation. _OWASP Top Ten_. https://owasp.org/www-project-top-ten/ (2021).
2. OWASP Foundation. _OWASP Testing Guide v4.2_. https://owasp.org/www-project-web-security-testing-guide/ (2021).
3. OWASP Foundation. _OWASP ZAP Documentation_. https://www.zaproxy.org/docs/ (2024).
4. ffuf Project. _ffuf — Fast Web Fuzzer_. https://github.com/ffuf/ffuf (2024).
5. SQLMap Project. _SQLMap — Automatic SQL Injection Tool_. https://sqlmap.org / https://github.com/sqlmapproject/sqlmap (2024).
6. Docker Inc. _Docker Documentation_. https://docs.docker.com (2024).
7. DVWA Project. _Damn Vulnerable Web Application_. https://github.com/digininja/DVWA (2024).
8. Python Software Foundation. _subprocess — Subprocess management_. https://docs.python.org/3/library/subprocess.html (2024).

---

## Apéndice A — Estructura completa del proyecto

```
orquestador-seguridad/
├── main.py
├── docker-compose.yml
├── dockerfile
├── requirements.txt
├── test_parsers.py
├── test_zap.py
└── app/
    ├── __init__.py
    ├── config/
    │   ├── __init__.py
    │   └── settings.py          (pendiente)
    ├── runners/
    │   ├── __init__.py
    │   └── exec.py              ✅
    ├── scanners/
    │   ├── __init__.py
    │   ├── zap.py               ✅
    │   ├── ffuf.py              ✅
    │   └── sqlmap.py            ✅
    ├── parsers/
    │   ├── __init__.py
    │   ├── zap_parser.py        ✅
    │   ├── ffuf_parser.py       ✅
    │   └── sqlmap_parser.py     ✅
    ├── workflow/
    │   ├── __init__.py
    │   └── pipeline.py          ✅
    ├── reports/
    │   ├── __init__.py
    │   └── generator.py         ❌ (pendiente)
    ├── utils/
    │   ├── __init__.py
    │   └── results.py           ✅
    ├── samples/                 (datos de prueba)
    └── worldlists/
        └── wordlist.txt
```

---

## Apéndice B — Fragmentos de código representativos

### B.1 Runner — manejo de subprocesos (`exec.py`)

```python
def run_command(command, timeout=60) -> dict:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=isinstance(command, str)
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "timeout": False,
            "error_type": None if result.returncode == 0 else "execution_error"
        }
    except subprocess.TimeoutExpired as e:
        return { "success": False, "timeout": True, "error_type": "timeout", ... }
    except Exception as e:
        return { "success": False, "error_type": "system_error", ... }
```

### B.2 Parser ZAP — aplanamiento y deduplicación (`zap_parser.py`)

```python
def parsear_zap(dato_dict_crudo):
    alertas_sin_parsear = data["site"][0]["alerts"]
    vistas = set()
    alertas_parseadas = []

    for alerta in alertas_sin_parsear:
        for instancia in alerta["instances"]:
            url = instancia["uri"]
            clave = (url, alerta["alert"])   # deduplicación por URL + tipo

            if clave not in vistas:
                vistas.add(clave)
                alertas_parseadas.append({
                    "url": url,
                    "vulnerabilidad": alerta["alert"],
                    "severidad": alerta["riskdesc"],
                    "solucion": alerta["solution"]
                })
```

### B.3 Pipeline — orquestación secuencial (`pipeline.py`)

```python
def run_security_pipeline(target_url):
    # [1/4] ZAP Spider
    spider_id = iniciar_spider(target_url)
    esperar_spider(spider_id)
    spider_urls = obtener_urls(spider_id)

    # [2/4] ZAP Active Scan
    ascan_id = iniciar_escaneo_activo(target_url)
    esperar_escaneo_activo(ascan_id)
    reporte_zap_crudo = obtener_reporte_json()

    # [3/4] SQLMap (solo URLs con parámetros)
    lista_urls = spider_urls.get("results", [])
    sqlmap_raw = run_sqlmap_batch(lista_urls)

    # [4/4] ffuf (fuzzing de directorios)
    ffuf_raw = run_ffuf(target_url, WORDLIST_PATH, OUTPUT_DIR)

    return { "target": target_url, "spider_raw": spider_urls,
             "zap_raw": reporte_zap_crudo, "sqlmap_raw": sqlmap_raw,
             "ffuf_raw": ffuf_data }
```

---

## Apéndice C — Ejemplo de estructura JSON de salida

```json
{
  "resumen": {
    "total_urls_unicas": 52,
    "urls_spider": 45,
    "alertas_zap": 12,
    "rutas_ffuf": 8,
    "vulnerabilidades_sqlmap": 2
  },
  "zap": {
    "herramienta": "ZAP",
    "total_alertas": 12,
    "alertas": [
      {
        "url": "http://dvwa/vulnerabilities/sqli/?id=1",
        "vulnerabilidad": "SQL Injection",
        "severidad": "High (Risk=3, Confidence=3)",
        "solucion": "Do not trust client side input. Validate, filter input. Use parameterized queries."
      },
      {
        "url": "http://dvwa/login.php",
        "vulnerabilidad": "Anti-CSRF Tokens Scanner",
        "severidad": "Medium (Risk=2, Confidence=1)",
        "solucion": "Phase: Architecture and Design. Use a vetted library or framework."
      }
    ]
  },
  "ffuf": {
    "herramienta": "ffuf",
    "total_rutas": 8,
    "rutas": [
      {
        "url": "http://dvwa/admin",
        "input": { "FUZZ": "admin" },
        "status": 200
      },
      {
        "url": "http://dvwa/config",
        "input": { "FUZZ": "config" },
        "status": 302
      }
    ]
  }
}
```

---

_Informe generado en base al análisis del código fuente del proyecto — Febrero 2026_
