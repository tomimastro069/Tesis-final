# 🛡️ Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web
> **Sistema de orquestación para análisis automatizado de vulnerabilidades web mediante fuzzing y escaneo activo**

[![Universidad](https://img.shields.io/badge/UTN-FRM-003366?style=for-the-badge&logo=institution&logoColor=white)](https://www.frm.utn.edu.ar/)
[![Carrera](https://img.shields.io/badge/TUP-Tecnicatura_Universitaria_en_Programación-005BA1?style=for-the-badge)](https://www.frm.utn.edu.ar/)
[![Trabajo Final](https://img.shields.io/badge/Modalidad-Trabajo_Final_de_Graduación-2E7D32?style=for-the-badge)](#-ficha-institucional-del-trabajo-final)
[![Estado](https://img.shields.io/badge/Estado-Aprobada_para_Defensa_Oral-1B5E20?style=for-the-badge)](#-ficha-institucional-del-trabajo-final)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose_v2-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![React](https://img.shields.io/badge/React-18.3-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-F57C00?style=for-the-badge)](LICENSE)

---

## 📋 Ficha Institucional del Trabajo Final

* **Institución:** Universidad Tecnológica Nacional — Facultad Regional Mendoza (UTN FRM).
* **Carrera:** Tecnicatura Universitaria en Programación (TUP).
* **Modalidad Académica:** Trabajo Final de Graduación.
* **Título:** *Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web*.
* **Subtítulo:** *Sistema de orquestación para análisis automatizado de vulnerabilidades web mediante fuzzing y escaneo activo*.
* **Línea de Investigación:** Seguridad informática · Ciberseguridad ofensiva · Automatización de pruebas · Ingeniería de software.
* **Autores:** Tomas Mastropietro · Cristian Krahulik · Juan Segura.
* **Directores del Trabajo Final:** Alberto Cortez · Ariel Enferrel.
* **Año Académico:** 2026.
* **Documentación Oficial:** [informe-v17.pdf](docs/informe/informe-v17.pdf) (76 páginas numeradas + portada, compuesto en Typst).
* **Estado Académico:** Aprobada para Defensa Oral con recomendación de calificación sobresaliente.

---

## 📖 1. Descripción del Proyecto y Planteo del Problema

En el ciclo de vida del desarrollo seguro (*DevSecOps*), las pruebas dinámicas de seguridad para aplicaciones web (*DAST*) y las técnicas de *fuzzing* suelen enfrentarse a dos limitaciones críticas:
1. **Desarticulación operativa y silos de información:** El uso aislado de escáneres web (como OWASP ZAP), fuzzers de directorios (como ffuf) y herramientas de inyección (como SQLMap) genera datos fragmentados, formatos dispares y redundancia analítica.
2. **Fricción con la agilidad de entrega (CI/CD):** Los escaneos dinámicos exhaustivos demandan ventanas prolongadas de tiempo (decenas de minutos u horas) y un alto consumo de cómputo sobre superficies que no han variado.

### Propuesta de Valor
Este **Trabajo Final de Graduación** diseña, implementa y valida experimentalmente una plataforma liviana de orquestación (bajo el paradigma SOAR — *Security Orchestration, Automation, and Response*) que:
* **Coordina de forma secuencial y automatizada** a OWASP ZAP, ffuf y SQLMap en entornos contenerizados e independientes.
* **Alimenta dinámicamente** los hallazgos de una fase a la siguiente (las rutas descubiertas por ffuf se inyectan al Spider de ZAP y los parámetros candidatos a SQLMap).
* **Optimiza tiempos de escaneo mediante un motor de caché incremental** persistente en SQLite/PostgreSQL, reduciendo las ventanas de análisis repetitivo en más de un 68 % sin comprometer la cobertura.
* **Consolida los resultados** en un reporte unificado en formato JSON y Markdown con clasificación de riesgos bajo el estándar OWASP Top 10.
* **Provee una API REST asíncrona (FastAPI)**, asistencia de remediación potenciada por Inteligencia Artificial (Google Gemini vía n8n) y un panel interactivo web con estética retro (estilo Windows 98) en React.

---

## 🏗️ 2. Arquitectura del Sistema

La arquitectura está construida bajo un modelo modular desacoplado en cuatro capas funcionales:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      CAPA DE CLIENTE E INTERACCIÓN                     │
│   Frontend Retro (React 18 + Vite)     │   Asistente IA (n8n + Gemini) │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP REST / WebSocket Polling
┌───────────────────────────────────▼────────────────────────────────────┐
│                        CAPA DE SERVICIO ASÍNCRONO                      │
│   FastAPI (api.py)  ──►  Worker en Segundo Plano (pipeline.py)         │
│   Persistencia e Historial: PostgreSQL / SQLite (history.db)           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ CLI / REST API Calls
┌───────────────────────────────────▼────────────────────────────────────┐
│                       CAPA DE MOTORES DE SEGURIDAD                     │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐  │
│  │    OWASP ZAP     │───►│       ffuf       │───►│      SQLMap      │  │
│  │ (Spider/Activo)  │    │ (Fuzzing Rutas)  │    │  (Inyección SQL) │  │
│  └──────────────────┘    └──────────────────┘    └──────────────────┘  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Tráfico HTTP / Red Aislada
┌───────────────────────────────────▼────────────────────────────────────┐
│                      CAPA DE INFRAESTRUCTURA Y TARGET                  │
│       Contenedores Docker Compose  ──►  DVWA (Laboratorio Objetivo)    │
└────────────────────────────────────────────────────────────────────────┘
```

### Componentes y Contenedores del Stack (`docker-compose.yml`)

| Contenedor | Imagen Base | Puerto Local | Función en el Sistema |
| :--- | :--- | :---: | :--- |
| `security-app` | `python:3.11-slim` | `8000:8000` | Orquestador central, parsers sintácticos, motor de caché y API REST FastAPI. |
| `dvwa` | `vulnerables/web-dvwa` | `8080:80` | Aplicación web intencionalmente vulnerable empleada como banco de pruebas. |
| `zap` | `ghcr.io/zaproxy/zaproxy:stable` | `8090:8090` | Daemon de OWASP ZAP para spidering y escaneo activo controlado por API REST. |
| `security-db` | `postgres:16-alpine` | `5433:5432` | Base de datos relacional para persistencia de escaneos y trazabilidad. |
| `security-n8n` | `n8nio/n8n:latest` | `5678:5678` | Motor de automatización para enriquecimiento de hallazgos con IA (Gemini). |

### Flujo de Ejecución Secuencial del Pipeline
1. **Autenticación Automatizada:** Obtención de cookie de sesión (`PHPSESSID`) con perfil de seguridad configurado en DVWA.
2. **Reconocimiento con ZAP Spider:** Rastreo de hipervínculos, formularios y componentes web expuestos.
3. **Fuzzing de Directorios con ffuf:** Descubrimiento por fuerza bruta de rutas ocultas (`/vulnerabilities/`, backups, archivos sensibles), consultando la base de datos de historial para omitir palabras ya probadas.
4. **Escaneo Activo con OWASP ZAP:** Análisis heurístico profundo inyectando las rutas descubiertas por ffuf.
5. **Comprobación y Explotación con SQLMap:** Verificación de inyección SQL sobre endpoints candidatos empleando los flags ejecutables (`--batch`, `--flush-session`, `--forms`, `--dbms=MySQL`, `--level=1`, `--risk=3`, `--threads=5`, `--technique=BEUST` y `-o`, habiéndose desestimado `--smart` para garantizar cobertura analítica completa sobre DVWA) e interactuando mediante `sqlmapapi.py`.
6. **Consolidación de Hallazgos:** Los parsers especializados (`zap_parser.py`, `ffuf_parser.py`, `sqlmap_parser.py`) normalizan las salidas y generan `resultado_unificado.json` y `reporte_seguridad.md`.

---

## 🚀 3. Puesta en Marcha y Reproducibilidad Rápida (Quickstart)

Siguiendo las pautas de reproducibilidad científica del **Anexo I** del informe, el entorno completo se despliega en pocos pasos mediante Docker Compose:

### Requisitos Previos
* [Docker Engine](https://docs.docker.com/engine/install/) 24.0+ y [Docker Compose](https://docs.docker.com/compose/) v2.0+.
* [Node.js](https://nodejs.org/) 20+ y [pnpm](https://pnpm.io/) (únicamente si se ejecuta el frontend fuera de contenedor).
* Clave de API de Google Gemini (opcional, requerida para el módulo de asistencia con IA).

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/tomimastro069/Tesis-final.git
cd Tesis-final
```

### Paso 2: Configurar Variables de Entorno (Opcional para IA)
```bash
cd orquestador-seguridad
cp .env.example .env
```
*Edite el archivo `.env` para asignar su clave `IA_API_KEY=tu_api_key_de_gemini`.*

### Paso 3: Desplegar la Infraestructura Multicontenedor
```bash
docker compose up -d --build
```

Una vez que los servicios completen el aprovisionamiento, las interfaces quedarán disponibles en:
* **API REST y Documentación Swagger:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Laboratorio Vulnerable (DVWA):** [http://localhost:8080](http://localhost:8080) (Credenciales por defecto: `admin` / `password`)
* **OWASP ZAP API Daemon:** [http://localhost:8090](http://localhost:8090)
* **Consola de Flujos n8n:** [http://localhost:5678](http://localhost:5678)

### Paso 4: Iniciar el Frontend Retro (React)
En una terminal separada:
```bash
cd frontend
pnpm install
pnpm dev
```
Acceda a la interfaz gráfica retro en [http://localhost:5173](http://localhost:5173).

---

## 🎬 4. Validación Empírica y Registro Audiovisual

Para asegurar la transparencia experimental y dar cumplimiento a los requerimientos de la UTN FRM, el trabajo cuenta con un **video demostrativo formal de 09:00 minutos exactos en resolución 1080p Full HD**, documentado en el **Anexo I.2** y la **Tabla 14** del informe escrito:

📺 **Registro Audiovisual Oficial en YouTube:** [https://www.youtube.com/watch?v=UA0rolg9ZKI](https://www.youtube.com/watch?v=UA0rolg9ZKI)

```
00:00        00:50              02:20                   04:50            06:40           08:20     09:00
┌──────────────┬──────────────────┬───────────────────────┬────────────────┬───────────────┬─────────┐
│  Bloque 1    │    Bloque 2      │       Bloque 3        │    Bloque 4    │   Bloque 5    │Bloque 6 │
│ Presentación │ Escaneo Inicial  │ Auditoría de Reportes │ Contraste con  │ Escaneo con   │ Cierre  │
│ e Interfaz   │ Sin Caché (13m)  │ y Análisis con IA     │ WinDiff        │ Caché (3 min) │ UTN FRM │
└──────────────┴──────────────────┴───────────────────────┴────────────────┴───────────────┴─────────┘
```

### Resultados Experimentales Clave (Ejecución sobre DVWA)
* **Superficie de Ataque Identificada:** 34 URLs exploradas ($24\text{ vía Spider} + 8\text{ vía ffuf} + 2\text{ derivadas}$).
* **Hallazgos de Seguridad Consolidados:** 41 vulnerabilidades confirmadas ($37\text{ por ZAP} + 4\text{ por SQLMap}$), abarcando inyecciones SQL (A03), configuraciones inseguras (A05) y fallos de autenticación (A07).
* **Impacto del Motor de Caché Incremental (Hipótesis H4):**
  * **Sin caché:** $14\text{ min } 05,81\text{ s}$ ($845,81\text{ s}$).
  * **Con caché incremental activo:** $4\text{ min } 23,15\text{ s}$ ($263,15\text{ s}$).
  * **Optimización empírica:** **68,9 % de reducción del tiempo total** con 0 % de pérdida en detección de hallazgos críticos.

---

## 📁 5. Estructura del Repositorio

```text
Tesis-final/
├── docs/                               # Documentación académica e institucional
│   ├── informe/                        # Trabajo Final modular en Typst y PDF compilado
│   │   ├── informe-v17.typ             # Documento maestro (metadatos, índices, includes)
│   │   ├── informe-v17.pdf             # Entregable oficial compilado (76 páginas + portada)
│   │   └── capitulos/                  # Los 19 capítulos desacoplados (01 a 19)
│   ├── evidencia/                      # Evidencia física canónica (reporte_seguridad.md y README)
│   ├── dictamen/                       # Dictámenes docentes (excluidos de Git por privacidad)
│   ├── plan/                           # Planes de acción internos (en .gitignore)
│   └── audit/                          # Minutas de auditoría algorítmica (en .gitignore)
├── orquestador-seguridad/              # Backend Python y orquestador central
│   ├── app/                            # Módulos del orquestador (scanners, parsers, workflow, db)
│   ├── api.py                          # Servicio web FastAPI asíncrono
│   ├── main.py                         # Punto de entrada interactivo por consola
│   ├── docker-compose.yml              # Configuración multicontenedor (5 servicios)
│   └── Dockerfile                      # Imagen contenerizada del orquestador
├── frontend/                           # Panel web retro interactivo (React 18 + Vite)
├── n8n/                                # Flujos automatizados y puente con Gemini AI
├── LICENSE                             # Licencia de código abierto MIT
└── README.md                           # Ficha técnica y guía principal del repositorio
```

---

## ⚖️ 6. Consideraciones Éticas y Cumplimiento Legal

Este sistema fue desarrollado con propósitos estrictamente **académicos, defensivos y de investigación científica**:
* **Legislación Nacional:** Se ajusta al marco de la **Ley 26.388 de Delitos Informáticos** (incorporada al art. 153 bis del Código Penal de la República Argentina).
* **Marco Internacional:** Se rige por los lineamientos del **Convenio de Budapest sobre Ciberdelincuencia**.
* **Código de Conducta Profesional:** Cumple con los principios 1.2 (*Evitar el daño*), 1.3 (*Ser justo y tomar medidas para no discriminar*) y 1.6 (*Respetar la privacidad*) del **Código de Ética de la ACM** (*Association for Computing Machinery*).
* **Restricción de Alcance:** El uso del software sobre objetivos no autorizados expresamente es ilegal. Los autores y la institución no se responsabilizan por el uso indebido del prototipo.

---

## 📚 7. Cómo Citar este Trabajo Final

Si utiliza este código fuente, los datos experimentales o la metodología en investigaciones académicas, cite el trabajo formalmente conforme a las normas **APA 7.ª edición**:

### Formato APA (7.ª edición)
```text
Mastropietro, T., Krahulik, C., & Segura, J. (2026). Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web [Trabajo final de graduación, Universidad Tecnológica Nacional — Facultad Regional Mendoza]. Repositorio oficial en GitHub. https://github.com/tomimastro069/Tesis-final
```

### Entrada BibTeX
```bibtex
@mastersthesis{mastropietro2026orquestador,
  title        = {Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web},
  author       = {Mastropietro, Tomas and Krahulik, Cristian and Segura, Juan},
  year         = {2026},
  school       = {Universidad Tecnol{\'o}gica Nacional --- Facultad Regional Mendoza},
  type         = {Trabajo final de graduaci{\'o}n},
  note         = {Tecnicatura Universitaria en Programaci{\'o}n (TUP)},
  url          = {https://github.com/tomimastro069/Tesis-final}
}
```

---

## 📄 8. Licencia

Este proyecto se distribuye bajo los términos de la [Licencia MIT](LICENSE). Es software libre y abierto para fines de estudio, docencia e investigación.
