= 19. Anexos Técnicos
<anexos-técnicos>
== Anexo A — Estructura del Proyecto y configuración de docker compose
<anexo-a-estructura-del-proyecto-y-configuración-de-docker-compose>
=== A.1 Estructura del proyecto
<a.1-estructura-del-proyecto>
orquestador-seguridad/ \
├── main.py \# Punto de entrada CLI \(interactivo) \
├── api.py \# API REST \(FastAPI) - punto de entrada como servicio \
├── docker-compose.yml \# Servicios: dvwa, zap, app, db, n8n \(5
servicios) \
├── Dockerfile \
├── requirements.txt \
├── test\_parsers.py / test\_speed.py / test\_zap.py / test\_sqlmap.py \
├── OPTIMIZACION\_ZAP.md \# Documentación de optimización de timeouts y
caché \
├── app/ \
│ ├── config/settings.py \
│ ├── runners/exec.py \
│ ├── scanners/{zap.py, ffuf.py, sqlmap.py} \
│ ├── parsers/{zap\_parser.py, ffuf\_parser.py, sqlmap\_parser.py} \
│ ├── workflow/{pipeline.py, consolidate\_sqlmap.py} \
│ ├── db/database.py \
│ ├── routers/n8n\_router.py \
│ ├── reports/generator.py \
│ └── utils/{results.py, time.py} \
└── output/{raw/{benchmarks/}, reports/} \
n8n/

├── data/

├── flujo.json

└── init-n8n.sh \
frontend/ \
└── src/{app/components/, app/windows98/, hooks/,
services/#link("http://api.ts")[#underline[api.ts];];}
=== A.2 Archivo docker-compose.yml
<a.2-archivo-docker-compose.yml>
version: \"3.8\"

services:

db:

image: postgres:16-alpine

container\_name: security-db

environment:

POSTGRES\_DB: security\_history

POSTGRES\_USER: security\_user

POSTGRES\_PASSWORD: security\_pass

volumes:

- postgres\_data:/var/lib/postgresql/data

ports:

- \"5433:5432\"

healthcheck:

test: \[\"CMD-SHELL\", \"pg\_isready -U security\_user -d
security\_history\"\]

interval: 5s

timeout: 5s

retries: 10

dvwa:

image: vulnerables/web-dvwa

container\_name: dvwa

ports:

- \"8080:80\"

zap:

image: ghcr.io/zaproxy/zaproxy:stable

container\_name: zap

environment:

- ZAP\_PORT\=8090

command: \>

zap.sh -daemon

-host 0.0.0.0

-port 8090

-config api.key\=12345

-config api.addrs.addr.name\=.\*

-config api.addrs.addr.regex\=true

ports:

- \"8090:8090\"

app:

build: .

container\_name: security-app

depends\_on:

db:

condition: service\_healthy

zap:

condition: service\_started

dvwa:

condition: service\_started

environment:

DB\_ENGINE: postgres

DB\_HOST: db

DB\_PORT: 5432

DB\_NAME: security\_history

DB\_USER: security\_user

DB\_PASSWORD: security\_pass

N8N\_WEBHOOK\_URL: http:\/\/security-n8n:5678/webhook/analyze-vuln

volumes:

- .:/app

ports:

- \"8000:8000\"

n8n:

image: n8nio/n8n:latest

container\_name: security-n8n

ports:

- \"5678:5678\"

environment:

- N8N\_HOST\=localhost

- N8N\_PORT\=5678

- N8N\_PROTOCOL\=http

- NODE\_ENV\=production

- IA\_API\_KEY\=\${IA\_API\_KEY:-}

- GEMINI\_API\_KEY\=\${GEMINI\_API\_KEY:-}

- groq\_key\=\${groq\_key:-}

volumes:

- ../n8n/data:/home/node/.n8n

- ../n8n/flujo.json:/etc/n8n/flujo.json:ro

- ../n8n/init-n8n.sh:/etc/n8n/init-n8n.sh:ro

entrypoint: \[\"tini\", \"--\", \"/bin/sh\", \"/etc/n8n/init-n8n.sh\"\]

depends\_on:

- app

volumes:

postgres\_data:

#emph[Nota sobre seguridad de la configuración. La definición de
  credenciales estáticas y tokens en texto plano
  \(POSTGRES\_PASSWORD\=security\_pass y api.key\=12345) constituye una
  decisión técnica orientada a facilitar el despliegue del laboratorio
  controlado, en concordancia con los alcances definidos en el capítulo 9.
  Por el contrario, las claves de servicios de inteligencia artificial
  \(IA\_API\_KEY, GEMINI\_API\_KEY, groq\_key) se gestionan mediante
  interpolación de variables de entorno del host \(\${VAR:-}),
  garantizando la protección de secretos de producción fuera del entorno
  local.]

=== A.3 Archivo Dockerfile
<a.3-archivo-dockerfile>
\# Imagen base oficial de Python

FROM python:3.11-slim

\# Evita archivos .pyc y buffers raros

ENV PYTHONDONTWRITEBYTECODE\=1

ENV PYTHONUNBUFFERED\=1

\# Instalamos dependencias del sistema necesarias

RUN apt update && apt install -y \\

wget \\

ca-certificates \\

&& rm -rf /var/lib/apt/lists/\*

ARG FFUF\_VERSION\=2.2.1

RUN wget
https:\/\/github.com/ffuf/ffuf/releases/download/v\${FFUF\_VERSION}/ffuf\_\${FFUF\_VERSION}\_linux\_amd64.tar.gz
\\

&& tar -xzf ffuf\_\${FFUF\_VERSION}\_linux\_amd64.tar.gz \\

&& mv ffuf /usr/local/bin/ffuf \\

&& chmod +x /usr/local/bin/ffuf \\

&& rm ffuf\_\${FFUF\_VERSION}\_linux\_amd64.tar.gz

\# Instalamos SQLMap \(clonamos el repo oficial)

RUN apt update && apt install -y git \\

&& git clone --depth 1 https:\/\/github.com/sqlmapproject/sqlmap.git
/opt/sqlmap \\

&& rm -rf /var/lib/apt/lists/\*

\# Directorio de trabajo dentro del contenedor

WORKDIR /app

\# Copiamos requirements primero \(optimiza cache)

COPY requirements.txt .

\# Instalamos dependencias Python

RUN pip install --no-cache-dir -r requirements.txt

\# Copiamos el resto del proyecto

COPY . .

\# Comando por defecto

CMD \[\"uvicorn\", \"api:app\", \"--host\", \"0.0.0.0\", \"--port\",
\"8000\"\]

== Anexo B — Fragmento Representativo: Pipeline de Ejecución
<anexo-b-fragmento-representativo-pipeline-de-ejecución>
def run\_security\_pipeline\(target\_url, nivel\=\"medium\",
cookies\=None, \
sqlmap\_level\=\"basic\", progress\_callback\=None): \
init\_db\() \
... \
if not cookies: \
cookies \= establecer\_sesion\_automatica\(target\_url) \
limpiar\_sesion\_zap\() \
if cookies: \
configurar\_autenticacion\(cookies) \
\
\# --- 1. ZAP SPIDER --- \
spider\_id \= iniciar\_spider\(target\_url) \
esperar\_spider\(spider\_id, progress\_callback\=cb\_spider) \
spider\_urls \= obtener\_urls\(spider\_id) \
\
\# --- 2. FFUF \(antes del Active Scan) --- \
ffuf\_raw \= run\_ffuf\(target\_url, WORDLIST\_PATH, OUTPUT\_DIR,
cookies\=cookies) \
ffuf\_data \= {} if ffuf\_raw.get\(\"skipped\") else
json.load\(open\(ffuf\_raw\[\"output\_file\"\])) \
rutas\_ffuf\_nuevas \= ffuf\_data.get\(\"results\", \[\]) \
\
\# --- 3. INYECTAR RUTAS DE FFUF EN ZAP --- \
if rutas\_ffuf\_nuevas: \
agregar\_urls\_a\_zap\(rutas\_ffuf\_nuevas) \
\
\# --- 4. ZAP ACTIVE SCAN --- \
ascan\_id \= iniciar\_escaneo\_activo\(target\_url) \
esperar\_escaneo\_activo\(ascan\_id, progress\_callback\=cb\_ascan) \
reporte\_zap\_crudo \= obtener\_reporte\_json\() \
\
\# --- 5. SQLMAP \(sesion refrescada, URLs combinadas) --- \
lista\_urls\_total \= list\(set\(spider\_urls.get\(\"results\", \[\]) +
\
\[r.get\(\"url\", \"\") for r in rutas\_ffuf\_nuevas\])) \
sqlmap\_raw \= run\_sqlmap\_batch\(lista\_urls\_total, cookies\=cookies,
\
sqlmap\_level\=sqlmap\_level) \
\
return {\"target\": target\_url, \"spider\_raw\": spider\_urls, \
\"zap\_raw\": reporte\_zap\_crudo, \"sqlmap\_raw\": sqlmap\_raw, \
\"ffuf\_raw\": ffuf\_data}
== Anexo C — Fragmento Representativo: Parser de ZAP
<anexo-c-fragmento-representativo-parser-de-zap>
def parsear\_zap\(dato\_dict\_crudo): \
try: \
data \= dato\_dict\_crudo \
vistas \= set\() \
alertas\_parseadas \= \[\] \
for sitio in data.get\(\"site\", \[\]): \
for alerta in sitio.get\(\"alerts\", \[\]): \
for instancia in alerta.get\(\"instances\", \[\]): \
url \= instancia.get\(\"uri\", \"\") \
clave \= \(url, alerta.get\(\"alert\", \"\")) \
if clave not in vistas: \
vistas.add\(clave) \
alertas\_parseadas.append\({ \
\"url\": url, \
\"vulnerabilidad\": alerta.get\(\"alert\", \"Vulnerabilidad sin
nombre\"), \
\"severidad\": alerta.get\(\"riskdesc\", \"No clasificado\"), \
\"metodo\": instancia.get\(\"method\", \"N/A\"), \
\"solucion\": alerta.get\(\"solution\", \"No hay solucion disponible\")
\
}) \
return {\"herramienta\": \"ZAP\", \"total\_alertas\":
len\(alertas\_parseadas), \
\"alertas\": alertas\_parseadas} \
except \(KeyError, TypeError) as e: \
print\(f\"Error al parsear los datos de ZAP: {e}\") \
return {}

== Anexo D — Ejemplo del JSON Unificado Final \(corrida del 5 de agosto de 2026)
<anexo-d-ejemplo-del-json-unificado-final-corrida-del-5-de-agosto-de-2026>
El siguiente extracto reproduce el campo resumen del archivo
resultado\_unificado.json de la ejecución documentada en el capítulo 13,
verificable directamente en el repositorio del proyecto.

{ \
\"resumen\": { \
\"total\_urls\_unicas\": 34, \
\"urls\_spider\": 24, \
\"alertas\_zap\": 37, \
\"rutas\_ffuf\": 8, \
\"vulnerabilidades\_sqlmap\": 4 \
}, \
\"zap\": { \
\"herramienta\": \"ZAP\", \
\"host\": \"dvwa\", \
\"total\_alertas\": 37, \
\"alertas\": \[ \
{ \"url\": \"http:\/\/dvwa/about.php\", \
\"vulnerabilidad\": \"Content Security Policy \(CSP) Header Not Set\", \
\"severidad\": \"Medium \(High)\" } \
\] \
}, \
\"ffuf\": { \"herramienta\": \"ffuf\", \"total\_rutas\": 8, \
\"rutas\": \[ { \"url\": \"http:\/\/dvwa/setup.php\", \"status\": 200 }
\] }, \
\"sqlmap\": { \"herramienta\": \"SQLMAP\", \
\"vulnerabilidades\": \[ \
{ \"url\":
\"http:\/\/dvwa/vulnerabilities/brute/?Login\=Login&password\=ZAP&username\=ZAP\",
\
\"salida\": \"... Type: boolean-based blind ... parameter \'username\'
is vulnerable\" } \
\] \
} \
}

Todas las rutas reportadas usan http:\/\/dvwa/, el hostname real de la
red interna de Docker, en lugar del hostname ilustrativo target.com que
figuraba en versiones anteriores del documento; esta ejecución
corresponde a datos reales y no a un ejemplo construido.

== Anexo E — Fragmento Representativo: Autenticación Automática
<anexo-e-fragmento-representativo-autenticación-automática>
def establecer\_sesion\_automatica\(target\_url): \
\"\"\"Login automatico en DVWA; reintenta inicializando la BD si
falla.\"\"\" \
session \= requests.Session\() \
def intentar\_login\(): \
r \= session.get\(login\_url, timeout\=10) \
token \= re.search\(r\"user\_token\[\'\\\"\]
value\=\[\'\\\"\]\(\[^\'\\\"\]\*)\", r.text) \
session.post\(login\_url, data\={\"username\": \"admin\", \"password\":
\"password\", \
\"Login\": \"Login\", \"user\_token\": token.group\(1) if token else
\"\"}) \
r\_sec \= session.post\(security\_url, data\={\"security\": \"low\",
\"seclev\_submit\": \"Submit\"}) \
return \"logout\" in r\_sec.text.lower\() \
\
if intentar\_login\(): \
return \"; \".join\(f\"{k}\={v}\" for k, v in
session.cookies.get\_dict\().items\()) \
\
\# Login fallo: inicializar la base de datos de DVWA y reintentar \
session.post\(setup\_url, data\={\"create\_db\": \"Create / Reset
Database\"}) \
time.sleep\(3); session.cookies.clear\() \
if intentar\_login\(): \
return \"; \".join\(f\"{k}\={v}\" for k, v in
session.cookies.get\_dict\().items\()) \
return None
== Anexo F — Fragmento Representativo: API REST
<anexo-f-fragmento-representativo-api-rest>
app \= FastAPI\(title\=\"Orquestador de Seguridad API\",
version\=\"1.0.0\") \
\
class ScanRequest\(BaseModel): \
target: str \
nivel: Optional\[str\] \= \"medium\" \
cookies: Optional\[str\] \= None \
callback\_url: Optional\[str\] \= None \
sqlmap\_level: Optional\[str\] \= \"basic\" \
\
\@app.post\(\"/scan\", status\_code\=202) \
def iniciar\_escaneo\(request: ScanRequest, background\_tasks:
BackgroundTasks): \
scan\_id \= str\(uuid.uuid4\()) \
create\_scan\(scan\_id, request.target) \
background\_tasks.add\_task\(ejecutar\_pipeline\_segundo\_plano,
scan\_id\=scan\_id, \
target\=request.target, nivel\=request.nivel, \
cookies\=request.cookies, sqlmap\_level\=request.sqlmap\_level) \
return {\"message\": \"Escaneo lanzado\", \"scan\_id\": scan\_id} \
\
\@app.get\(\"/scan/{scan\_id}/progress\") \
def get\_scan\_progress\(scan\_id: str): \
if scan\_id in scan\_progress\_store: \
return scan\_progress\_store\[scan\_id\] \
scan\_data \= get\_scan\_by\_id\(scan\_id) \
if not scan\_data: \
raise HTTPException\(status\_code\=404, detail\=\"Scan no encontrado\")
\
return {\"percentage\": 100, \"message\": \"Analisis Completado\"} if
scan\_data\[\"status\"\] \=\= \"completed\" \\ \
else {\"percentage\": 0, \"message\": \"Iniciando o retomando
analisis...\"}

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

== Anexo H — Diagramas en Tamaño Ampliado
<anexo-h-diagramas-en-tamaño-ampliado>
Este anexo reproduce a mayor tamaño, para su mejor observación, las
Figuras 1 a 4 ya presentadas y comentadas en las secciones 11.1, 11.4 y
11.5: Figura 1 \(Diagrama de Arquitectura de Servicio), Figura 2
\(Diagrama Orquestador-Seguridad), Figura 3 \(Diagrama de Pipeline de
ejecución) y Figura 4 \(Diagrama de secuencia — ciclo de vida de POST
/scan).

#box(width: 7.828125546806649in, image("../media/media/image2.png"))
#text(size: 10pt)[#emph[Figura 1 \(ampliada). Diagrama de Arquitectura de Servicio.
  Elaboración propia.]]

#box(width: 7.432292213473316in, image("../media/media/image1.jpg"))

#text(size: 10pt)[#emph[Figura 2 \(ampliada). Diagrama Orquestador-Seguridad. Elaboración
  propia.]]

#quote(block: true)[
  #box(width: 6.246719160104987in, image("../media/media/image4.jpg"))
]

#text(size: 10pt)[#emph[Figura 3 \(ampliada). Diagrama del Pipeline de Ejecución.
  Elaboración propia.]]

#box(width: 8.229166666666666in, image("../media/media/image3.png"))

#text(size: 10pt)[#emph[Figura 4 \(ampliada). Diagrama de secuencia UML. Elaboración
  propia.]]
