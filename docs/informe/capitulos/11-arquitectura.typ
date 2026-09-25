= 11. Arquitectura Propuesta e Implementada
<arquitectura-propuesta-e-implementada>
== 11.1 Descripción General
<descripción-general>
La arquitectura del sistema se organiza en cuatro capas, ilustradas en
la Figura 1:

#block[
  #set enum(numbering: "1.", start: 1)
  + Orquestador Python: coordina la ejecución del pipeline \(spider → ffuf
    → inyección de rutas en ZAP → escaneo activo → SQLMap), gestiona
    autenticación y sesión, y consolida resultados.

  + Herramientas de escaneo: OWASP ZAP \(spider y escaneo activo), ffuf
    \(fuzzing de directorios) y SQLMap \(inyección SQL), cada una
    encapsulada en su propio módulo \(ver Figura 2).

  + Capa de persistencia: base de datos SQLite o PostgreSQL que almacena
    historial de escaneos, caché incremental de ffuf y SQLMap, y URLs
    marcadas para re-testeo automático.

  + Capa de servicio: una API REST \(FastAPI) que expone el pipeline de
    forma asíncrona con seguimiento de progreso, y un frontend web que
    consume esa API para lanzar escaneos y visualizar resultados,
    incluyendo sugerencias de mitigación obtenidas mediante un flujo de
    n8n.
]

#align(center)[
  #image("../media/media/image2.png", width: 78%)
]

#text(size: 10pt)[#emph[Figura 1. Diagrama de Arquitectura de Servicio. Elaboración propia
  \(véase versión ampliada en el Anexo H).]] <fig-1>

#pagebreak()

== 11.2 Componentes y Sus Roles
<componentes-y-sus-roles>
#strong[Tabla 2. Componentes del sistema y su función en el pipeline] <tabla-2>

#figure(
  align(center)[#table(
    columns: 3,
    align: (col, row) => (auto, auto, auto).at(col),
    inset: 6pt,
    [Componente], [Contenedor], [Función en el pipeline],
    [DVWA], [dvwa], [Aplicación objetivo de las pruebas],
    [OWASP ZAP], [zap], [Spider, escaneo activo y generación de reportes vía API REST],
    [Orquestador Python],
    [security-app],
    [Coordinación del pipeline, autenticación automática, ejecución de
      ffuf y SQLMap, parseo y consolidación],

    [API REST],
    [security-app],
    [Expone el pipeline como servicio asíncrono \(/scan, /scans,
      /scan/{id}, /scan/{id}/progress)],

    [Base de datos],
    [db \(SQLite embebida o PostgreSQL)],
    [Persistencia de historial de escaneos, caché incremental de
      ffuf/SQLMap y URLs marcadas para re-testeo],
  )],
)

#text(size: 10pt)[#emph[Nota. Elaboración propia.]]

La Figura 2 detalla cómo el orquestador coordina específicamente a las
tres herramientas de escaneo y el enriquecimiento cruzado entre ellas.

#align(center)[
  #image("../media/media/image5.jpg", width: 62%)
]

#text(size: 10pt)[#emph[Figura 2. Diagrama Orquestador-Seguridad: coordinación y
  enriquecimiento cruzado entre ZAP, ffuf y SQLMap. Elaboración propia
  \(véase versión ampliada en el Anexo H).]] <fig-2>

== 11.3 Red Docker y Aislamiento
<red-docker-y-aislamiento>
Todos los servicios se ejecutan dentro de una red virtual Docker
gestionada por Docker Compose. Esta configuración garantiza el
aislamiento del tráfico interno entre contenedores y permite la
resolución de nombres de servicio: los contenedores se comunican entre
sí por nombre \(por ejemplo, el orquestador se conecta a ZAP mediante el
hostname zap y a DVWA mediante el hostname dvwa). Los puertos se exponen
al host únicamente para los servicios que requieren acceso externo
durante el desarrollo. La API habilita CORS para permitir que el
frontend, ejecutado fuera de la red interna de Docker, consuma sus
endpoints durante el desarrollo.

== 11.4 Flujo de Datos Detallado
<flujo-de-datos-detallado>
El ciclo de vida completo de un análisis de seguridad en el sistema
sigue la secuencia representada en la Figura 3:

#block[
  #set enum(numbering: "1.", start: 1)
  + El orquestador establece sesión autenticada contra la aplicación
    objetivo \(login automático y configuración del nivel de seguridad) y
    limpia la sesión previa de ZAP.

  + Ejecuta el spider de ZAP contra la URL objetivo, que recorre la
    aplicación web descubriendo las URLs accesibles.

  + Ejecuta ffuf contra la URL base, consultando primero el historial en
    base de datos para descartar palabras de wordlist ya testeadas contra
    ese objetivo.

  + Las rutas descubiertas por ffuf se inyectan en la sesión de ZAP antes
    del paso siguiente.

  + Se ejecuta el escaneo activo de ZAP, que ataca tanto las URLs
    descubiertas por su propio spider como las rutas aportadas por ffuf.

  + Se combinan las URLs del spider y de ffuf, se filtran las candidatas
    con parámetros o rutas interactivas, se descartan las que ya están
    cacheadas sin hallazgos previos y se conserva siempre el re-testeo de
    las marcadas como vulnerables en ejecuciones anteriores; SQLMap se
    ejecuta en segundo plano sobre esa lista final, con la sesión de
    autenticación renovada para evitar su expiración.

  + Los resultados crudos de cada herramienta son procesados por parsers
    especializados que normalizan las estructuras de datos y eliminan
    duplicados.

  + El módulo de consolidación unifica los resultados de todos los parsers
    en un único archivo JSON estructurado, que alimenta tanto el reporte
    técnico como el reporte ejecutivo.
]

#align(center)[
  #image("../media/media/image4.jpg", width: 65%)
]

#text(size: 10pt)[#emph[Figura 3. Diagrama de Pipeline de ejecución. Elaboración propia
  \(véase versión ampliada en el Anexo H).]] <fig-3>

== 11.5 Diagrama de Secuencia — Ciclo de Vida de POST /scan
<diagrama-de-secuencia-ciclo-de-vida-de-post-scan>
Las Figuras 1 a 3 documentan la arquitectura estática del sistema y el
flujo interno del pipeline de escaneo, pero no el comportamiento
asíncrono de la API frente al cliente. La Figura 4 completa esa
descripción con un diagrama de secuencia UML del ciclo de vida completo
de una petición POST /scan, desde que el frontend la dispara hasta que
la API notifica su finalización a n8n.

El diagrama distingue explícitamente entre la respuesta inmediata de la
API \(202 Accepted con el scan\_id, antes de que el pipeline haya
siquiera comenzado a ejecutarse) y el trabajo en segundo plano que
realiza ejecutar\_pipeline\_segundo\_plano\(): mientras este último
coordina secuencialmente a ZAP, ffuf y SQLMap y lee/escribe en la base
de datos, el frontend consulta el progreso mediante polling periódico a
GET /scan/{id}/progress, sin bloquear ni depender de que la conexión
HTTP original permanezca abierta. Esta separación entre la respuesta
síncrona y la ejecución asíncrona es la que permite que el pipeline
—cuya duración se documenta en la sección 14.3 entre 4 y 14 minutos
según el estado del caché— no comprometa la responsividad de la API ni
del frontend.

#align(center)[
  #image("../media/media/image3.png", width: 78%)
]

#text(size: 10pt)[#emph[Figura 4. Diagrama de secuencia — ciclo de vida de POST /scan.
  Elaboración propia \(véase versión ampliada en el Anexo H).]] <fig-4>

=== 11.5.1 Detalle de la Secuencia de Interacción
<detalle-de-la-secuencia-de-interacción>

El ciclo asíncrono representado en el diagrama comprende las siguientes etapas:

+ #strong[Frontend → API \(POST /scan):] el usuario inicia un escaneo desde el frontend enviando una petición HTTP `POST /scan` a FastAPI, incluyendo la URL objetivo y los parámetros de análisis.

+ #strong[API → Base de datos \(crear scan\_id):] la API genera un identificador único \(`scan_id`) y registra el escaneo en la base de datos junto con el objetivo, garantizando persistencia y trazabilidad.

+ #strong[API → Pipeline \(ejecutar en segundo plano):] la API despacha `ejecutar_pipeline_segundo_plano()` como tarea en segundo plano. La API no espera la conclusión del escaneo para responder, desacoplando el tiempo de escaneo del ciclo de vida HTTP.

+ #strong[API → Frontend \(202 Accepted + scan\_id):] la API responde inmediatamente con código HTTP `202 Accepted` y el `scan_id`. El escaneo continúa ejecutándose de forma asíncrona; el cliente solo recibe el identificador para consultar el estado.

+ #strong[Pipeline → ZAP \(ZAP Spider):] el pipeline inicia el spidering de OWASP ZAP para rastrear la aplicación web y recolectar las URLs accesibles del objetivo.

+ #strong[Pipeline → ffuf \(ffuf):] tras el spider, ffuf ejecuta un análisis de fuerza bruta mediante wordlists para descubrir rutas y directorios no vinculados directamente.

+ #strong[Pipeline → ZAP \(inyectar rutas descubiertas):] las nuevas rutas halladas por ffuf son incorporadas al árbol de sitios de ZAP, ampliando la superficie de ataque.

+ #strong[Pipeline → ZAP \(ZAP Active Scan):] con las rutas consolidadas, ZAP ejecuta el escaneo activo atacando tanto las rutas del spider como las aportadas por ffuf para identificar vulnerabilidades.

+ #strong[Pipeline → SQLMap:] concluido el Active Scan, el pipeline extrae las URLs candidatas y despacha SQLMap en segundo plano para corroborar vulnerabilidades de inyección SQL.

+ #strong[Pipeline → Base de datos \(guardar resultados):] durante la ejecución, el sistema persiste de forma incremental el estado y los hallazgos en la base de datos para mantener el historial.

+ #strong[Frontend → API \(GET /scan/{id}/progress):] de forma desacoplada, el frontend consulta periódicamente el estado del escaneo enviando peticiones de polling a `GET /scan/{id}/progress` con el `scan_id` correspondiente.

+ #strong[API → Frontend \(porcentaje de progreso):] la API responde con el avance relativo del pipeline \(`percentage: 100` y `"Analisis Completado"` al finalizar). El término "porcentaje" refleja estrictamente el avance secuencial de etapas del orquestador, no una métrica de cobertura ni de vulnerabilidades detectadas.

+ #strong[Ciclo de Polling Periódico:] las consultas y respuestas de progreso se reiteran a intervalos regulares sin mantener abierta la conexión original de `POST /scan`.

+ #strong[Pipeline → API \(escaneo finalizado):] al concluir todas las herramientas integradas \(ZAP Spider, ffuf, ZAP Active Scan y SQLMap), el pipeline notifica a la API la finalización del trabajo.

+ #strong[API → n8n \(webhook HTTP):] finalmente, la API dispara una notificación vía webhook HTTP a n8n para informar la culminación del escaneo e iniciar los flujos automatizados de sugerencias de mitigación.
