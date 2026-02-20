# Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web

## Diapositiva 1 — Portada

**Título:** Orquestador de Seguridad — Fuzzing Automatizado de Aplicaciones Web

**Autores:** Cristian Krahulik, Tomas Mastropietro, Juan Segura

**Materia:** Seguridad Ofensiva

---

## Diapositiva 2 — ¿Qué es este proyecto?

Un sistema automatizado que recibe una URL objetivo, ejecuta múltiples pruebas de seguridad sobre ella, recopila todos los hallazgos y genera un reporte unificado.

No es un scanner nuevo, sino una **orquestación inteligente** de herramientas de seguridad ya existentes, coordinadas por un pipeline en Python.

**Objetivo:** Detectar vulnerabilidades web de forma automatizada y reproducible.

---

## Diapositiva 3 — ¿Qué es el Fuzzing?

El fuzzing es una técnica de seguridad que consiste en enviar datos inesperados o aleatorios a una aplicación para descubrir fallos, rutas ocultas o vulnerabilidades.

Tipos de fuzzing utilizados:

- **Fuzzing de directorios:** buscar rutas y archivos ocultos en un servidor web.
- **Fuzzing de parámetros:** probar valores inusuales en formularios y URLs.
- **Escaneo activo/pasivo:** analizar respuestas del servidor para detectar vulnerabilidades conocidas (OWASP Top 10).

---

## Diapositiva 4 — Herramientas utilizadas

- **OWASP ZAP:** Escáner de seguridad web open source. Realiza el descubrimiento de rutas (Spider) y análisis de vulnerabilidades (Active Scan).
- **ffuf:** Fuzzer web ultrarrápido. Descubre directorios y archivos ocultos usando diccionarios de palabras.
- **Docker:** Plataforma de contenedores para levantar el entorno completo de laboratorio de manera reproducible.
- **DVWA:** Aplicación web intencionalmente vulnerable, usada como objetivo de pruebas.
- **Python:** Lenguaje del orquestador que coordina todo el flujo.

---

## Diapositiva 5 — Arquitectura del Sistema

El sistema corre completamente dentro de contenedores Docker:

1. **Contenedor DVWA** — La aplicación vulnerable objetivo.
2. **Contenedor OWASP ZAP** — El scanner de seguridad en modo daemon (API REST).
3. **Contenedor App (Python)** — El orquestador que coordina todo.

Los tres servicios se comunican entre sí por la red interna de Docker, garantizando un entorno aislado y seguro.

---

## Diapositiva 6 — Estructura Modular del Proyecto

El orquestador sigue una arquitectura modular donde cada componente tiene una responsabilidad única:

- **Runners:** Ejecutan comandos del sistema de forma segura, manejando errores y timeouts.
- **Scanners:** Interactúan con las herramientas externas (ZAP y ffuf) y obtienen los datos crudos.
- **Parsers:** Transforman los datos crudos de cada herramienta en un formato limpio y estandarizado.
- **Pipeline:** El "cerebro" del sistema que coordina el orden de ejecución de todo el flujo.
- **Utils:** Funciones auxiliares, como la consolidación de resultados de múltiples herramientas.

---

## Diapositiva 7 — El Pipeline: Flujo de Ejecución

El pipeline ejecuta los pasos en orden secuencial:

**Paso 1 — ZAP Spider:** Descubre todas las URLs y endpoints de la aplicación objetivo recorriendo su estructura.

**Paso 2 — ZAP Active Scan:** Analiza cada URL encontrada buscando vulnerabilidades conocidas (inyecciones SQL, XSS, CSRF, etc.).

**Paso 3 — ffuf:** Ejecuta fuzzing de directorios para descubrir rutas ocultas que el spider no pudo encontrar.

**Paso 4 — Consolidación:** Recopila todos los datos crudos y los guarda como paquete unificado.

---

## Diapositiva 8 — Fase de Parseo

Una vez obtenidos los datos crudos, el sistema ejecuta un segundo pipeline de parseo:

- **Parser de Spider:** Extrae y deduplica las URLs descubiertas.
- **Parser de ZAP:** Aplana las alertas de seguridad, eliminando duplicados y extrayendo URL, vulnerabilidad, severidad y solución recomendada.
- **Parser de ffuf:** Filtra las rutas encontradas por código de estado HTTP y elimina duplicados.

Finalmente, los tres resultados parseados se consolidan en una estructura unificada con un resumen general.

---

## Diapositiva 9 — Resultado Final

El sistema genera un archivo JSON unificado que contiene:

- **Resumen:** Total de URLs únicas encontradas, cantidad de alertas de ZAP, y rutas descubiertas por ffuf.
- **Sección Spider:** Listado completo de URLs mapeadas de la aplicación.
- **Sección ZAP:** Vulnerabilidades detectadas con su severidad y solución.
- **Sección ffuf:** Rutas y directorios descubiertos con su estado HTTP.

Todo en un solo archivo, listo para análisis o generación de reportes.

---

## Diapositiva 10 — Cómo se ejecuta

1. Se levanta el entorno completo con un solo comando de Docker Compose.
2. Se ejecuta el script principal de Python.
3. El pipeline se encarga automáticamente de: ejecutar el spider, lanzar el escaneo activo, correr ffuf, parsear todo y consolidar.
4. Los resultados finales quedan en la carpeta de salida del proyecto.

Todo es automático: el usuario solo necesita indicar la URL objetivo.

---

## Diapositiva 11 — Trabajo en Equipo

El proyecto se dividió en tres perfiles:

- **Ingeniero de Ejecución (Tomas):** Infraestructura Docker, módulo Runner y módulos Scanners (ZAP y ffuf).
- **Arquitecto de Lógica (Cristian):** Módulos Parsers, Pipeline de ejecución y lógica de consolidación.
- **Especialista en Configuración y Entrega (Juan):** Configuración global, generador de reportes y punto de entrada del sistema.

---

## Diapositiva 12 — Conclusiones y Próximos Pasos

**Logros:**

- Pipeline funcional que ejecuta pruebas de seguridad automatizadas de extremo a extremo.
- Arquitectura modular, limpia y extensible.
- Entorno completamente dockerizado y reproducible.

**Próximos pasos:**

- Integrar SQLMap para detección automática de inyecciones SQL.
- Implementar generación de reportes en Markdown/PDF.
- Agregar clasificación de severidad (CVSS) a los hallazgos.
- Posible integración con pipelines CI/CD.
