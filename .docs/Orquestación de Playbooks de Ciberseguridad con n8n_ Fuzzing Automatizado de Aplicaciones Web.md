# **Orquestación de Playbooks de Ciberseguridad con n8n: Fuzzing Automatizado de Aplicaciones Web**

**Autores y afiliaciones**

 Cristian Krahulik — (Materia: Seguridad Ofensiva / Universidad / Equipo)

 Tomas Mastropietro –(Materia: Seguridad Ofensiva / Universidad  / Equipo)

 Juan Segura –(Materia: Seguridad Ofensiva / Universidad / Equipo)  
 Autor corresponsal: (krahulikcristian@gmail.com)

---

## **Resumen**

Este trabajo presenta el diseño e implementación de un laboratorio de *fuzzing automatizado* para aplicaciones web, integrando herramientas de escaneo y detección de vulnerabilidades (OWASP ZAP, ffuf, wfuzz, SQLMap, Burp Suite) con un orquestador *low-code* (n8n). La propuesta combina automatización de pruebas (fuzzing de rutas y parámetros, detección de inyecciones, escaneo activo/pasivo) con consolidación de resultados en base de datos y generación de reportes automáticos.  
 El objetivo es demostrar cómo integrar fuzzing y seguridad web en pipelines CI/CD y entornos educativos, permitiendo la detección temprana de vulnerabilidades OWASP Top 10\.

**Palabras clave:** n8n, fuzzing, OWASP ZAP, SQLMap, wfuzz, ffuf, automatización, seguridad web, CI/CD

---

## **1\. Introducción**

Las aplicaciones web continúan siendo un vector principal de ataques debido a errores de validación, configuraciones inseguras y endpoints expuestos. El *fuzzing* —ya sea de contenido, parámetros o directorios— permite identificar estos puntos débiles de manera automatizada.  
 Este trabajo propone una orquestación reproducible con **n8n** para combinar herramientas *open source* de fuzzing y escaneo, consolidando resultados en **PostgreSQL** y generando reportes automáticos.

**Contribuciones:**

* Arquitectura replicable con n8n, OWASP ZAP, ffuf/wfuzz y SQLMap.

* Playbooks orquestados para discovery → fuzzing → análisis → reporte.

* Base de datos estructurada para almacenamiento de hallazgos.

* Guía de ejercicios prácticos y criterios de evaluación académica.

---

## **2\. Trabajos relacionados / Marco teórico**

La propuesta se apoya en las guías **OWASP Testing Guide** y **OWASP Top 10**, que establecen las categorías más comunes de vulnerabilidades web.  
 Se complementa con el uso de **ZAP** y **Burp Suite** para escaneo pasivo/activo, **ffuf/wfuzz** para fuzzing rápido, y **SQLMap** para detección de inyecciones SQL automatizadas.  
 El enfoque *low-code* mediante **n8n** permite integrar múltiples herramientas sin programación compleja, facilitando el uso educativo y de laboratorio.

---

## **3\. Metodología**

### **Diseño experimental**

* Entorno controlado con una aplicación vulnerable (**DVWA**) desplegada en contenedor Docker.

* Orquestación completa a través de **n8n**, que ejecuta workflows secuenciales.

* Almacenamiento de resultados y estadísticas en **PostgreSQL**.

### **Variables y métricas sugeridas**

* **Endpoints descubiertos:** cantidad de URLs detectadas por ZAP Spider.

* **Paths descubiertos:** rutas encontradas por ffuf/wfuzz.

* **Vulnerabilidades confirmadas:** hallazgos validados por SQLMap o evidencia directa.

* **Tasa de falsos positivos:** proporción de resultados no reproducibles.

* **Duración promedio del escaneo.**

### **Procedimiento general (pipeline)**

1. **Trigger n8n:** inicio manual o programado.

2. **Descubrimiento:** OWASP ZAP (spider/crawl).

3. **Fuzzing de rutas:** ffuf o wfuzz sobre URL base.

4. **Pruebas de parámetros:** fuzzing y SQLMap sobre endpoints con parámetros.

5. **Consolidación:** normalización y deduplicación de resultados.

6. **Clasificación:** asignación de severidad (CVSS-like).

7. **Reporte:** generación automática en Markdown \+ envío por email/Slack.

---

## **4\. Arquitectura propuesta**

`┌────────────────────────────────────────────────────┐`  
`│         Entorno de Fuzzing Automatizado                     │`  
`│                                                    │`  
`│  ┌──────────────┐         ┌──────────────┐       │`  
`│  │     N8N      │────────▶│ Burp Suite   │       │`  
`│  │ Orchestrator │         │     API      │       │`  
`│  └──────┬───────┘         └──────┬───────┘       │`  
`│         │                        │               │`  
`│         ▼                        ▼               │`  
`│  ┌──────────────┐         ┌──────────────┐       │`  
`│  │  OWASP ZAP   │────────▶│    DVWA      │       │`  
`│  │     API      │         │ (Target App) │       │`  
`│  └──────────────┘         └──────────────┘       │`  
`│         │                                         │`  
`│         ▼                                         │`  
`│  ┌──────────────┐                                │`  
`│  │  PostgreSQL  │                                │`  
`│  │ (Results DB) │                                │`  
`│  └──────────────┘                                │`  
`└────────────────────────────────────────────────────┘`

**Seguridad operativa:** credenciales cifradas en n8n, límites de tasa en herramientas, y entorno aislado (sandbox) para evitar daños.

---

## **5\. Playbooks (casos de uso n8n)**

### **PB-1 — Discovery \+ Directory Fuzzing**

**Input:** URL base del objetivo  
 **Pasos:**

1. Webhook → iniciar workflow manual.

2. ZAP Spider → descubrir endpoints.

3. ffuf (Exec Node) → fuzzing de directorios (`ffuf -u TARGET/FUZZ -w common.txt`).

4. Parsear resultados JSON y registrar hallazgos.

5. Guardar en DB (Postgres Node).

6. Enviar reporte o alerta (Email/Slack).

---

### **PB-2 — Parameter Fuzzing \+ SQLMap**

**Input:** URLs con parámetros (ej. `?id=1`).  
 **Pasos:**

1. Filtrar endpoints con parámetros.

2. Ejecutar wfuzz/ffuf con payloads de inyección.

3. Lanzar SQLMap (`--batch --random-agent --level=2 --risk=2`).

4. Parsear resultados JSON → marcar vulnerables.

5. Consolidar y priorizar según severidad.

---

### **PB-3 — Continuous Fuzzing (CI/CD)**

**Input:** Pipeline de staging o preproducción.  
 **Pasos:**

1. Trigger desde CI (GitHub Actions/GitLab).

2. Ejecutar ffuf reducido \+ ZAP passive scan.

3. Generar reporte y bloquear merge si hay vulnerabilidades críticas.

---

## **6\. Configuración del laboratorio**

### **Instalación DVWA**

`docker pull vulnerables/web-dvwa`  
`docker run -d -p 8080:80 --name dvwa vulnerables/web-dvwa`  
`# Acceder: http://localhost:8080 (user: admin / pass: password)`

### **Instalación OWASP ZAP**

`sudo snap install zaproxy --classic`  
`zap.sh -daemon -host 0.0.0.0 -port 8090 -config api.key=YOUR_API_KEY`

### **Instalación herramientas de fuzzing**

`pip3 install wfuzz`  
`go install github.com/ffuf/ffuf/v2@latest`  
`git clone https://github.com/sqlmapproject/sqlmap.git`

---

## **7\. Esquema de Base de Datos (PostgreSQL)**

`CREATE DATABASE fuzzing_results;`  
`\c fuzzing_results;`

`CREATE TABLE scans (`  
    `id SERIAL PRIMARY KEY,`  
    `target_url VARCHAR(500),`  
    `scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,`  
    `total_vulnerabilities INTEGER,`  
    `critical_count INTEGER,`  
    `high_count INTEGER,`  
    `medium_count INTEGER,`  
    `low_count INTEGER,`  
    `report_path VARCHAR(500)`  
`);`

`CREATE TABLE vulnerabilities (`  
    `id SERIAL PRIMARY KEY,`  
    `scan_id INTEGER REFERENCES scans(id),`  
    `source VARCHAR(50),`  
    `type VARCHAR(200),`  
    `severity VARCHAR(20),`  
    `url TEXT,`  
    `description TEXT,`  
    `solution TEXT,`  
    `cweid INTEGER,`  
    `evidence TEXT`  
`);`

---

## **8\. Resultados esperados y evaluación**

**Indicadores (estimados):**

| Métrica | Valor esperado |
| ----- | ----- |
| Endpoints descubiertos | 100–200 |
| Paths encontrados (ffuf) | 300–400 |
| Vulnerabilidades confirmadas | 5–10 |
| Tasa de falsos positivos | \<15% |
| Duración promedio de escaneo | 40–60 min |

**Criterios de evaluación académica:**

| Criterio | Puntos |
| ----- | ----- |
| Configuración de herramientas | 20 |
| Identificación de vulnerabilidades | 30 |
| Workflow n8n funcional | 25 |
| Reporte y análisis | 15 |
| Plan de remediación | 10 |

---

## **9\. Discusión**

El uso de **n8n** permite integrar distintas herramientas de fuzzing en un entorno reproducible y transparente, reduciendo la carga manual.  
 Sin embargo, la automatización debe equilibrarse con revisión humana para evitar falsos positivos o daños no intencionados.  
 Las limitaciones incluyen dependencias de wordlists y variabilidad de entornos web.

---

## **10\. Amenazas a la validez**

* **Interna:** entorno controlado (DVWA) puede no reflejar producción.

* **Externa:** resultados no extrapolables a apps con WAF o autenticación.

* **Constructo:** métricas sensibles al tamaño y calidad de listas de fuzzing.

---

## **11\. Conclusiones y trabajo futuro**

El proyecto demuestra que la orquestación con **n8n** mejora la eficiencia del fuzzing automatizado, integrando varias herramientas en un flujo único.  
 **Futuro:** incorporar aprendizaje activo (payloads adaptativos), integración con ticketing (GLPI/Jira) y pruebas autenticadas.

---

## **12\. Consideraciones éticas**

Ejecutar únicamente en entornos autorizados.  
 Anonimizar resultados y limitar impacto (timeouts, rate limits).

---

## **13\. Agradecimientos**

A los docentes y equipos que colaboraron en la validación del laboratorio, y a las comunidades de proyectos open source (ZAP, ffuf, wfuzz, SQLMap).

---

## **Apéndice A — Fragmentos técnicos (n8n / scripts)**

**Ejemplo: ZAP Spider (nodo Function)**

`const axios = require('axios');`  
`const ZAP_URL = 'http://localhost:8090';`  
`const API_KEY = process.env.ZAP_API_KEY;`  
`const TARGET_URL = 'http://localhost:8080';`  
``const spiderResponse = await axios.get(`${ZAP_URL}/JSON/spider/action/scan/`, {``  
  `params: { apikey: API_KEY, url: TARGET_URL, recurse: true }`  
`});`

**Ejemplo: ffuf (Exec Node)**

`ffuf -u http://localhost:8080/FUZZ -w /path/to/common.txt -mc 200,301,302,401,403 -of json -o /tmp/ffuf_results.json -t 50 -timeout 10`

**Ejemplo: SQLMap wrapper**

`python3 /path/to/sqlmap/sqlmap.py -u "http://localhost:8080/vuln.php?id=1" --batch --random-agent --level=2 --risk=2`

