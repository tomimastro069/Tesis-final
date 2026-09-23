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
  \(véase versión ampliada en el Anexo H).]]

#pagebreak()

== 11.2 Componentes y Sus Roles
<componentes-y-sus-roles>
#strong[Tabla 2. Componentes del sistema y su función en el pipeline]

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

#box(width: 5.832357830271216in, image("../media/media/image5.jpg"))

#text(size: 10pt)[#emph[Figura 2. Diagrama Orquestador-Seguridad: coordinación y
  enriquecimiento cruzado entre ZAP, ffuf y SQLMap. Elaboración propia
  \(véase versión ampliada en el Anexo H).]]

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

#box(width: 5.78614501312336in, image("../media/media/image4.jpg"))

#text(size: 10pt)[#emph[Figura 3. Diagrama de Pipeline de ejecución. Elaboración propia
  \(véase versión ampliada en el Anexo H).]]

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

#box(width: 6.75in, image("../media/media/image3.png"))

#text(size: 10pt)[#emph[Figura 4. Diagrama de secuencia — ciclo de vida de POST /scan.
  Elaboración propia \(véase versión ampliada en el Anexo H).]]

#pagebreak()

#strong[EXPLICACIÓN GENERAL DEL DIAGRAMA:]

1. Frontend → API: POST /scan

El usuario inicia un escaneo desde el frontend. El frontend envía una
petición HTTP POST /scan a la API de FastAPI, incluyendo el objetivo y
los parámetros configurados para el análisis.

2. API → Base de datos: crear scan\_id

La API genera un identificador único \(scan\_id) para ese escaneo y
registra el nuevo análisis en la base de datos junto con el objetivo.
Esto permite identificar y consultar posteriormente ese escaneo.

3. API → Pipeline: ejecutar en segundo plano

La API programa ejecutar\_pipeline\_segundo\_plano\() como una tarea en
segundo plano.

Esto significa que #strong[la API no espera a que termine el escaneo
  para responderle al frontend];. El pipeline continúa ejecutándose
independientemente de la petición HTTP original.

4. API → Frontend: 202 Accepted + scan\_id

La API responde inmediatamente:

202 Accepted

scan\_id

El código 202 Accepted indica que la solicitud fue aceptada y que el
procesamiento continuará de forma asíncrona.

#strong[El escaneo todavía no terminó en este punto.] El frontend
solamente recibe el identificador con el que podrá consultar su estado.

5. Pipeline → ZAP: ZAP Spider

El pipeline inicia el Spider de OWASP ZAP.

Su función dentro del flujo es recorrer el objetivo y obtener las URLs
descubiertas. El pipeline espera a que termine y recupera esas URLs para
continuar con las siguientes etapas.

6. Pipeline → ffuf: ffuf

Una vez finalizado el Spider, se ejecuta ffuf.

ffuf utiliza una wordlist para buscar rutas adicionales en el objetivo.
Las rutas nuevas encontradas se incorporan posteriormente al análisis de
ZAP.

7. Pipeline → ZAP: inyectar rutas descubiertas

Las rutas nuevas encontradas por ffuf se agregan al árbol de sitios de
ZAP.

Esto permite que las rutas descubiertas mediante fuzzing también sean
consideradas durante el Active Scan.

8. Pipeline → ZAP: ZAP Active Scan

Después de incorporar las rutas nuevas, se inicia el Active Scan de ZAP.

Esta etapa realiza el análisis activo del objetivo y genera el reporte
de vulnerabilidades detectadas.

9. Pipeline → SQLMap

Finalizado el Active Scan, el pipeline combina las URLs obtenidas
mediante el Spider y ffuf y las utiliza como entrada para SQLMap.

SQLMap analiza las URLs candidatas para detectar posibles
vulnerabilidades de inyección SQL.

10. Pipeline → Base de datos: guardar resultados

Durante la ejecución, el sistema actualiza el estado y los resultados
del escaneo en la base de datos.

Esto permite conservar el historial del análisis y consultar
posteriormente su información.

11. Frontend → API: GET /scan/{id}/progress

Mientras el pipeline continúa trabajando, el frontend realiza
periódicamente una petición:

GET /scan/{id}/progress

El {id} corresponde al scan\_id recibido anteriormente.

Esto se denomina #strong[polling];: el frontend pregunta periódicamente
a la API cuál es el estado actual del escaneo.

12. API → Frontend: porcentaje de progreso

La API responde indicando el progreso del escaneo.

Cuando todavía existe información de progreso en memoria, devuelve el
porcentaje correspondiente. Si el escaneo ya está registrado como
completado en la base de datos, devuelve:

percentage: 100

message: \"Analisis Completado\"

Por eso, en el diagrama #strong[\"porcentaje\" significa el porcentaje
  de avance del pipeline];, no un porcentaje de vulnerabilidades
encontradas ni un porcentaje de cobertura.

13. Polling periódico

Las flechas:

Frontend → API

GET /scan/{id}/progress

API → Frontend

porcentaje

se repiten mientras el escaneo está ejecutándose.

El frontend #strong[no mantiene abierta la petición POST /scan]
esperando varios minutos. Consulta separadamente el progreso mediante
estas peticiones periódicas.

14. Pipeline → API: escaneo finalizado

Cuando todas las etapas del pipeline terminan —ZAP Spider, ffuf, ZAP
Active Scan y SQLMap— el pipeline informa a la API que el análisis
finalizó.

15. API → n8n: webhook HTTP

Finalmente, la API envía una notificación mediante un #strong[webhook
  HTTP a n8n] para informar que el escaneo terminó.

Esto permite que n8n continúe con los procesos asociados a la
finalización del análisis, como las funcionalidades de sugerencias de
mitigación.
