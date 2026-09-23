#set text(font: ("Calibri", "Liberation Sans", "Arial"), size: 11pt)

#show heading.where(level: 1): set text(size: 14pt, fill: rgb("#4e80bc"))
#show heading.where(level: 2): set text(size: 12pt, fill: rgb("#4e80bc"))
#show heading.where(level: 3): set text(size: 11pt, fill: rgb("#4e80bc"))

#set page(header: none)

#text(size: 19pt, weight: "bold", fill: rgb("#4e80bc"))[
  Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web
]

#v(2.5em)

#text(size: 13pt, weight: "bold")[
  UNIVERSIDAD TECNOLÓGICA NACIONAL – FACULTAD REGIONAL MENDOZA
]

#v(0.3em)

#text(size: 12pt, weight: "bold")[
  Tecnicatura Universitaria en Programación
]

#v(2.5em)

#strong[Subtítulo:] Sistema de orquestación para análisis automatizado de vulnerabilidades web mediante fuzzing y escaneo activo

#v(1.8em)

#strong[Autores:] Tomas Mastropietro, Cristian Krahulik, Juan Segura

#v(1.8em)

#strong[Directores:] Alberto Cortez y Ariel Enferrel.

#v(1.8em)

#strong[Línea de Investigación:] Seguridad informática · Ciberseguridad ofensiva · Automatización de pruebas · Ingeniería de software

#v(1.8em)

#strong[Fecha:] 2026

#pagebreak()

#counter(page).update(1)
#set page(header: align(right)[#context counter(page).display("1")])

= Resumen
<resumen>
#quote(block: true)[
El presente trabajo describe el diseño, implementación y validación de
un sistema automatizado de análisis de seguridad para aplicaciones web
basado en técnicas de fuzzing y escaneo activo. El sistema desarrollado,
denominado Orquestador de Seguridad, fue implementado íntegramente en
Python y permite coordinar la ejecución de múltiples herramientas
especializadas de análisis de vulnerabilidades de manera automatizada y
secuencial.

El sistema integra las herramientas OWASP ZAP, ffuf y SQLMap, cada una
ejecutándose en entornos contenerizados mediante Docker. El orquestador
central se encarga de coordinar la ejecución de cada herramienta,
recolectar sus resultados, procesarlos mediante parsers especializados y
consolidarlos en un único informe estructurado en formato JSON. La
arquitectura implementada se basa en un modelo modular donde cada
componente posee una responsabilidad específica: ejecución de
herramientas externas, recolección de datos, procesamiento de resultados
y consolidación final de hallazgos. Sobre esta base, el sistema se
extendió hacia una arquitectura de servicio con API REST asíncrona,
persistencia de historial, caché incremental, integración con n8n y un
frontend en React.

Las pruebas del sistema fueron realizadas sobre DVWA \(Damn Vulnerable
Web Application), una aplicación web intencionalmente vulnerable
utilizada comúnmente para investigación y entrenamiento en seguridad
informática. Durante las pruebas se logró detectar múltiples
vulnerabilidades relacionadas con el OWASP Top 10, incluyendo
inyecciones SQL, configuraciones de seguridad incorrectas y rutas
administrativas expuestas.

Los resultados obtenidos demuestran que la automatización del proceso de
fuzzing y escaneo permite reducir el esfuerzo de análisis manual,
facilitando la identificación temprana de vulnerabilidades en
aplicaciones web. Estas comparaciones se detallan en el capítulo 14,
junto con las limitaciones metodológicas correspondientes.

#strong[Palabras clave:] Fuzzing, Seguridad Web, OWASP ZAP, SQLMap,
Automatización, Docker, Python.
]

#pagebreak()

= Abstract
<abstract>
#quote(block: true)[
This work presents the design, implementation and validation of an
automated security analysis system for web applications based on fuzzing
techniques and active vulnerability scanning. The developed system,
called Security Orchestrator, was implemented entirely in Python and
coordinates the execution of multiple specialized security tools in an
automated and sequential pipeline.

The system integrates OWASP ZAP, ffuf, and SQLMap, each executed in
containerized environments using Docker. The Python orchestrator manages
tool execution, collects raw outputs, processes the results through
specialized parsers, and consolidates all findings into a single
structured JSON report.

The system was tested using DVWA \(Damn Vulnerable Web Application) as a
controlled laboratory target. The tests successfully identified
vulnerabilities associated with the OWASP Top 10, including SQL
injection, insecure configurations, and exposed administrative routes.

The results show that automated fuzzing orchestration improves
vulnerability discovery efficiency and reduces manual testing effort in
web security assessments, with the corresponding measurement caveats
detailed in Chapter 14.

#strong[Keywords:] Fuzzing, Web Security, OWASP ZAP, Automation,
Vulnerability Scanning, Docker, Python.
]

#pagebreak()

= Índice
<índice>
#outline(title: none, indent: auto)

#pagebreak()
= Índice de Figuras
<índice-de-figuras>
Figura 1. Diagrama de Arquitectura de Servicio 22

Figura 2. Diagrama Orquestador-Seguridad 23

Figura 3. Diagrama de Pipeline de ejecución 25

Figura 4. Diagrama de secuencia — ciclo de vida de POST /scan 26

Figura 1 \(ampliada). Diagrama de Arquitectura de Servicio 59

Figura 2 \(ampliada). Diagrama Orquestador-Seguridad 60

Figura 3 \(ampliada). Diagrama del Pipeline de Ejecución 61

Figura 4 \(ampliada). Diagrama de secuencia UML 62

= Índice de Tablas
<índice-de-tablas>
Tabla 1. Comparación de plataformas de orquestación y gestión de
vulnerabilidades 14

Tabla 2. Componentes del sistema y su función en el pipeline 22

Tabla 3. Resumen de hallazgos — ejecución sobre DVWA del 5 de agosto de
2026 33

Tabla 4. Vulnerabilidades detectadas por OWASP ZAP, por tipo 34

Tabla 5. Rutas descubiertas por fuzzing de directorios \(ffuf) 35

Tabla 6. Endpoints confirmados como vulnerables por SQLMap — corrida del
5 de agosto de 2026 35

Tabla 7. Datos extraídos a través de Sql Injection – corrida del 5 de
agosto del 2026 35

Tabla 8. Hallazgos clasificados por categoría OWASP Top 10 36

Tabla 9. Cobertura por herramienta en solitario frente al pipeline
combinado 38

Tabla 10. Tiempo total del pipeline con y sin caché incremental 40

Tabla 11. Estabilidad de hallazgos entre la corrida sin caché y con
caché 40

Tabla 12. Verificación de cumplimiento por objetivo específico 44

Tabla 13. Distribución temporal de la sesión de auditoría manual del
capítulo 17 49

#pagebreak()

#include "capitulos/01-introduccion.typ"

#include "capitulos/02-planteo-problema.typ"

#pagebreak()

#include "capitulos/03-justificacion.typ"

#pagebreak()

#include "capitulos/04-objetivos.typ"

#include "capitulos/05-preguntas-investigacion.typ"

#include "capitulos/06-hipotesis.typ"

#include "capitulos/07-estado-del-arte.typ"

#include "capitulos/08-marco-teorico.typ"

#include "capitulos/09-alcances-limitaciones.typ"

#include "capitulos/10-metodologia.typ"

#include "capitulos/11-arquitectura.typ"

#include "capitulos/12-implementacion.typ"

#include "capitulos/13-resultados.typ"

#include "capitulos/14-discusion.typ"

#include "capitulos/15-conclusiones.typ"

#include "capitulos/16-consideraciones-eticas.typ"

#include "capitulos/17-desarrollo-experimental.typ"

#include "capitulos/18-referencias.typ"

#include "capitulos/19-anexos.typ"
