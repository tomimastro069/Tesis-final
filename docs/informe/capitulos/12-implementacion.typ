= 12. Implementación Técnica
<implementación-técnica>
== 12.1 Infraestructura Docker
<infraestructura-docker>
El sistema se define en un archivo `docker-compose.yml` \(Docker Inc.,
2024) que especifica los servicios `dvwa` \(la aplicación objetivo, basada
en la imagen `vulnerables/web-dvwa`, DVWA Project, 2024), `zap` \(el escáner
OWASP ZAP, ejecutado en modo daemon con su API REST habilitada en el
puerto 8090), `db` \(base de datos PostgreSQL para historial y caché) y
`app` \(el orquestador Python, que se construye a partir del `Dockerfile`
del proyecto y expone además la API REST en el puerto 8000), además del
servicio `n8n` utilizado para las sugerencias de mitigación asistidas por
IA. La configuración de dependencias mediante la directiva `depends_on`
asegura que ZAP, DVWA y la base de datos se encuentren disponibles antes
de que el orquestador inicie su ejecución. El frontend se desarrolla
como un proyecto npm independiente, fuera de esta definición de Docker
Compose, y se conecta a la API mediante HTTP. El contenido íntegro del
archivo se transcribe en el Anexo A.

El contenedor del orquestador monta el directorio del proyecto como un
volumen \(`.:/app`), lo que permite que los archivos de salida generados
durante la ejecución del pipeline sean accesibles directamente desde el
sistema de archivos del host.

== 12.2 Pipeline de Ejecución
<pipeline-de-ejecución>
El pipeline de ejecución se implementa en el módulo
`app/workflow/pipeline.py`, que expone dos funciones principales:
`run_security_pipeline()` y `run_parser_pipeline()`. La primera
constituye el punto de entrada del proceso de escaneo: gestiona la
autenticación, ejecuta en orden spider de ZAP, ffuf, inyección de rutas
descubiertas, escaneo activo de ZAP y SQLMap en segundo plano,
devolviendo un diccionario con los datos crudos de las cuatro fuentes.
La segunda función invoca los parsers especializados y consolida los
resultados normalizados.

== 12.3 Módulo Runner
<módulo-runner>
El módulo `app/runners/exec.py` implementa la función `run_command()`, que
actúa como capa de abstracción para la ejecución de comandos del sistema
operativo mediante `subprocess.run()`. El parámetro `timeout` tiene un
valor por defecto de 60 segundos a nivel del runner genérico, pero cada
scanner puede sobrescribirlo: SQLMap recibe explícitamente el valor
`SQLMAP_TIMEOUT` centralizado en `settings.py` \(300 segundos), por lo que
la diferencia entre ambos valores es una configuración deliberada por
herramienta y no una inconsistencia entre secciones.

== 12.4 Módulo de Escaneo ZAP
<módulo-de-escaneo-zap>
El módulo `app/scanners/zap.py` encapsula toda la comunicación con la API
REST de OWASP ZAP \(OWASP Foundation, 2024): `iniciar_spider()`,
`esperar_spider()` y `obtener_urls()` controlan el crawling inicial;
`iniciar_escaneo_activo()` y `esperar_escaneo_activo()` configuran
intensidad y umbral de alertas; `obtener_reporte_json()` descarga el
reporte completo; `configurar_autenticacion()` registra la cookie de
sesión para escaneos autenticados; `agregar_urls_a_zap()` inyecta en
el árbol de sitios de ZAP las rutas descubiertas por ffuf; y
`limpiar_sesion_zap()` reinicia la sesión de ZAP al comienzo de cada
ejecución.

== 12.5 Módulo de Escaneo ffuf
<módulo-de-escaneo-ffuf>
El módulo `app/scanners/ffuf.py` implementa la función `run_ffuf()` \(ffuf
Project, 2024). Antes de ejecutar el fuzzer, consulta la base de datos
por las palabras de la wordlist ya testeadas contra el objetivo, genera
una wordlist temporal solo con las palabras nuevas, y marca la ejecución
como `skipped` si no hay palabras nuevas para probar. El comando se
configura con `-u`, `-w`, `-mc 200,302` y `-of json` / `-o`. Al finalizar, las
palabras efectivamente probadas se persisten en la base de datos.

#pagebreak()
== 12.6 Módulo de Escaneo SQLMap
<módulo-de-escaneo-sqlmap>
El módulo `app/scanners/sqlmap.py` implementa la detección de inyecciones
SQL \(SQLMap Project, 2024). La función
`filtrar_urls_con_parametros()` prioriza las URLs con parámetros GET y
rutas `.php` de formularios interactivos conocidos, excluyendo rutas
estáticas o de configuración. El comando de SQLMap se ejecuta con
`--batch`, `--flush-session`, `--forms`, `--dbms=MySQL`, `--level=1`, `--risk=3`,
`--threads=5`, `--technique=BEUST` y `-o`. La bandera `--smart` fue
retirada intencionalmente del pipeline debido a que, en aplicaciones como
DVWA, las respuestas base homogéneas ante cualquier parámetro provocaban
que la heurística de descarte rápido omitiera en silencio endpoints
vulnerables. La función `run_sqlmap_batch()` separa las URLs candidatas en
tres grupos según el historial en base de datos: las marcadas como
vulnerables se re-testean siempre; las ya analizadas sin hallazgos se omiten;
las nuevas se encolan. El escaneo se ejecuta en segundo plano mediante un
script bash generado dinámicamente. Asimismo, la función `run_sqlmap()` admite
el parámetro `sqlmap_level`, el cual modula el alcance de explotación en tres
modalidades: `basic` \(detección y confirmación con el comando base),
`fast_evidence` \(incorpora `--dbs`, `--tables` y `--current-user` para recabar
evidencia del esquema sin volcar datos) y `full_dump` \(añade `--dump` para
extraer íntegramente las tablas vulnerables confirmadas).

== 12.7 Sistema de Parseo
<sistema-de-parseo>
El sistema de parseo se implementa en el paquete `app/parsers/` y consta
de tres módulos especializados. `zap_parser.py` normaliza los resultados
del spider y aplana las alertas del reporte de ZAP eliminando duplicados
por clave \(`url, alerta`). `ffuf_parser.py` filtra las rutas con códigos
HTTP 200 y 302 y elimina duplicados por URL.

El parser de SQLMap, `sqlmap_parser.py`, funciona mediante la búsqueda de
un conjunto de patrones de texto dentro de la salida estándar \(`stdout`)
capturada de cada ejecución. La función `parsear_sqlmap()` recorre la
lista de resultados y considera una URL como vulnerable cuando su stdout
contiene, en minúsculas, al menos una de las siguientes cadenas: “is
vulnerable”, “is injectable”, “appears to be”, “vulnerability:”, “sql
injection”, “payload:”, “type:”, “database names are:”, “current user
is:”, “fetched data logged to text files” y “available databases”. Es,
en consecuencia, un parser de coincidencia de texto sobre salida en
lenguaje natural, no un parser que se apoye en el código de retorno del
proceso ni en una salida estructurada en formato JSON \(como la que expone
la API REST oficial de SQLMap a través de `sqlmapapi.py`). Esto lo hace
dependiente del formato exacto de los mensajes que SQLMap imprime por
consola, un formato que no está garantizado entre versiones de la
herramienta: un cambio de redacción en una futura versión de SQLMap
podría hacer que una URL efectivamente vulnerable no sea reconocida como
tal \(falso negativo), sin que el pipeline reporte ningún error, ya que el
parser no distingue entre “no se encontraron estos patrones porque no hay
vulnerabilidad” y “no se encontraron estos patrones porque el mensaje
cambió de forma”. Elia et al. \(2010) documentan precisamente este tipo de
riesgo al comparar herramientas de detección de inyección SQL basadas en
distintos mecanismos de análisis de salida. Una alternativa más robusta,
no implementada en esta versión, sería inspeccionar el código de retorno
del proceso e interactuar directamente con la API REST \(`sqlmapapi.py`),
la cual genera respuestas nativas en formato JSON estructurado, evitando
así la dependencia de cadenas de texto en lenguaje natural impresas en
la consola.

Los tres parsers comparten un patrón de diseño consistente: reciben un
diccionario o lista cruda, aplican transformaciones y filtrado, eliminan
duplicados e incluyen manejo de excepciones \(`KeyError`, `TypeError`) que
devuelven estructuras vacías en caso de error, evitando que un fallo en
el parseo de una herramienta interrumpa el pipeline completo.

== 12.8 Consolidación de Resultados
<consolidación-de-resultados>
El módulo `app/utils/results.py` implementa la función
`consolidar_resultados()`, que recibe los diccionarios normalizados de
spider, ZAP, ffuf y SQLMap y genera una estructura unificada con un
bloque de resumen \(conteos agregados) y los resultados completos de
cada herramienta. La función `resultados_prueba_json()` persiste el
resultado consolidado en un archivo JSON en `output/raw/`.

#pagebreak()
== 12.9 Autenticación Automática
<autenticación-automática>
El sistema implementa un flujo de login programático contra DVWA
\(`establecer_sesion_automatica()`): obtiene el token CSRF del
formulario de login, envía las credenciales, fija el nivel de seguridad
de la aplicación y verifica el éxito del login. Si el login falla, el
sistema intenta inicializar automáticamente la base de datos de la
aplicación objetivo mediante `setup.php` antes de reintentar. La cookie de
sesión obtenida se reutiliza para autenticar a ZAP, ffuf y SQLMap, y se
renueva antes de ejecutar SQLMap para evitar que expire durante el
escaneo activo de ZAP.

== 12.10 API REST y Frontend
<api-rest-y-frontend>
El módulo `api.py` \(FastAPI) expone el pipeline como servicio: `POST /scan`
lanza un escaneo en segundo plano, admitiendo los parámetros opcionales
`sqlmap_level: str` \(`basic`, `fast_evidence` o `full_dump`) y `clean_cache: bool`
\(el cual purga el historial en base de datos para forzar una ejecución limpia sin
reutilización de caché); `GET /scan/{id}/progress` permite consultar el porcentaje
de avance; `GET /scans` lista el historial persistido; `GET /scan/{id}` devuelve el
detalle de un escaneo puntual; `DELETE /scan/{id}` realiza un borrado lógico. Al
finalizar un escaneo, la API notifica su finalización mediante un webhook HTTP a un
flujo de n8n.
El frontend, desarrollado en React, consume estos endpoints para ofrecer
un panel de dominios escaneados, un formulario de lanzamiento de
escaneos, una tabla de vulnerabilidades y un componente de sugerencias
de mitigación que consulta un endpoint adicional de análisis asistido
por IA expuesto a través del router de n8n. El código fuente integral de estos componentes y el registro audiovisual de demostración en tiempo real se encuentran documentados para su verificación en el Anexo I.

#strong[Nota sobre pruebas.] Los scripts `test_parsers.py`,
`test_speed.py`, `test_zap.py` y `test_sqlmap.py` son scripts de
verificación manual \(ejecutan una función y muestran el resultado por
consola), no una suite de pruebas unitarias automatizadas con
aserciones.
