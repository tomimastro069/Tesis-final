= 12. Implementación Técnica
<implementación-técnica>
== 12.1 Infraestructura Docker
<infraestructura-docker>
El sistema se define en un archivo docker-compose.yml \(Docker Inc.,
2024) que especifica los servicios dvwa \(la aplicación objetivo, basada
en la imagen vulnerables/web-dvwa, DVWA Project, 2024), zap \(el escáner
OWASP ZAP, ejecutado en modo daemon con su API REST habilitada en el
puerto 8090), db \(base de datos PostgreSQL para historial y caché) y
app \(el orquestador Python, que se construye a partir del Dockerfile
del proyecto y expone además la API REST en el puerto 8000), además del
servicio n8n utilizado para las sugerencias de mitigación asistidas por
IA. La configuración de dependencias mediante la directiva depends\_on
asegura que ZAP, DVWA y la base de datos se encuentren disponibles antes
de que el orquestador inicie su ejecución. El frontend se desarrolla
como un proyecto npm independiente, fuera de esta definición de Docker
Compose, y se conecta a la API mediante HTTP. El contenido íntegro del
archivo se transcribe en el Anexo A.

El contenedor del orquestador monta el directorio del proyecto como un
volumen \(.:/app), lo que permite que los archivos de salida generados
durante la ejecución del pipeline sean accesibles directamente desde el
sistema de archivos del host.

== 12.2 Pipeline de Ejecución
<pipeline-de-ejecución>
El pipeline de ejecución se implementa en el módulo
app/workflow/pipeline.py, que expone dos funciones principales:
run\_security\_pipeline\() y run\_parser\_pipeline\(). La primera
constituye el punto de entrada del proceso de escaneo: gestiona la
autenticación, ejecuta en orden spider de ZAP, ffuf, inyección de rutas
descubiertas, escaneo activo de ZAP y SQLMap en segundo plano,
devolviendo un diccionario con los datos crudos de las cuatro fuentes.
La segunda función invoca los parsers especializados y consolida los
resultados normalizados.

== 12.3 Módulo Runner
<módulo-runner>
El módulo app/runners/exec.py implementa la función run\_command\(), que
actúa como capa de abstracción para la ejecución de comandos del sistema
operativo mediante subprocess.run\(). El parámetro timeout tiene un
valor por defecto de 60 segundos a nivel del runner genérico, pero cada
scanner puede sobrescribirlo: SQLMap recibe explícitamente el valor
SQLMAP\_TIMEOUT centralizado en settings.py \(300 segundos), por lo que
la diferencia entre ambos valores es una configuración deliberada por
herramienta y no una inconsistencia entre secciones.

== 12.4 Módulo de Escaneo ZAP
<módulo-de-escaneo-zap>
El módulo app/scanners/zap.py encapsula toda la comunicación con la API
REST de OWASP ZAP \(OWASP Foundation, 2024): iniciar\_spider\(),
esperar\_spider\() y obtener\_urls\() controlan el crawling inicial;
iniciar\_escaneo\_activo\() y esperar\_escaneo\_activo\() configuran
intensidad y umbral de alertas; obtener\_reporte\_json\() descarga el
reporte completo; configurar\_autenticacion\() registra la cookie de
sesión para escaneos autenticados; agregar\_urls\_a\_zap\() inyecta en
el árbol de sitios de ZAP las rutas descubiertas por ffuf; y
limpiar\_sesion\_zap\() reinicia la sesión de ZAP al comienzo de cada
ejecución.

== 12.5 Módulo de Escaneo ffuf
<módulo-de-escaneo-ffuf>
El módulo app/scanners/ffuf.py implementa la función run\_ffuf\() \(ffuf
Project, 2024). Antes de ejecutar el fuzzer, consulta la base de datos
por las palabras de la wordlist ya testeadas contra el objetivo, genera
una wordlist temporal solo con las palabras nuevas, y marca la ejecución
como skipped si no hay palabras nuevas para probar. El comando se
configura con -u, -w, -mc 200,302 y -of json/-o. Al finalizar, las
palabras efectivamente probadas se persisten en la base de datos.

== 12.6 Módulo de Escaneo SQLMap
<módulo-de-escaneo-sqlmap>
El módulo app/scanners/sqlmap.py implementa la detección de inyecciones
SQL \(SQLMap Project, 2024). La función
filtrar\_urls\_con\_parametros\() prioriza las URLs con parámetros GET y
rutas .php de formularios interactivos conocidos, excluyendo rutas
estáticas o de configuración. El comando de SQLMap se ejecuta con
--batch, --flush-session, --forms, --dbms\=MySQL, --level\=1, --risk\=3,
--threads\=10, --smart, --technique\=BEUST y -o. La función
run\_sqlmap\_batch\() separa las URLs candidatas en tres grupos según el
historial en base de datos: las marcadas como vulnerables se re-testean
siempre; las ya analizadas sin hallazgos se omiten; las nuevas se
encolan. El escaneo se ejecuta en segundo plano mediante un script bash
generado dinámicamente.

== 12.7 Sistema de Parseo
<sistema-de-parseo>
El sistema de parseo se implementa en el paquete app/parsers/ y consta
de tres módulos especializados. zap\_parser.py normaliza los resultados
del spider y aplana las alertas del reporte de ZAP eliminando duplicados
por clave \(url, alerta). ffuf\_parser.py filtra las rutas con códigos
HTTP 200 y 302 y elimina duplicados por URL.

El parser de SQLMap, sqlmap\_parser.py, funciona mediante la búsqueda de
un conjunto de patrones de texto dentro de la salida estándar \(stdout)
capturada de cada ejecución. La función parsear\_sqlmap\() recorre la
lista de resultados y considera una URL como vulnerable cuando su stdout
contiene, en minúsculas, al menos una de las siguientes cadenas: “is
vulnerable”, “is injectable”, “appears to be”, “vulnerability:”, “sql
injection”, “payload:”, “type:”, “database names are:”, “current user
is:”, “fetched data logged to text files” y “available databases”. Es,
en consecuencia, un parser de coincidencia de texto sobre salida en
lenguaje natural, no un parser que se apoye en el código de retorno del
proceso ni en una salida estructurada \(por ejemplo,
--output-format\=json). Esto lo hace dependiente del formato exacto de
los mensajes que SQLMap imprime por consola, un formato que no está
garantizado entre versiones de la herramienta: un cambio de redacción en
una futura versión de SQLMap podría hacer que una URL efectivamente
vulnerable no sea reconocida como tal \(falso negativo), sin que el
pipeline reporte ningún error, ya que el parser no distingue entre “no
se encontraron estos patrones porque no hay vulnerabilidad” y “no se
encontraron estos patrones porque el mensaje cambió de forma”. Elia et
al. \(2010) documentan precisamente este tipo de riesgo al comparar
herramientas de detección de inyección SQL basadas en distintos
mecanismos de análisis de salida \(Elia et al., 2010). Una alternativa
más robusta, no implementada en esta versión, sería inspeccionar el
código de retorno del proceso junto con la salida en formato JSON que
SQLMap puede producir de forma nativa, evitando así la dependencia de
cadenas de texto en lenguaje natural.

Los tres parsers comparten un patrón de diseño consistente: reciben un
diccionario o lista cruda, aplican transformaciones y filtrado, eliminan
duplicados e incluyen manejo de excepciones \(KeyError, TypeError) que
devuelven estructuras vacías en caso de error, evitando que un fallo en
el parseo de una herramienta interrumpa el pipeline completo.

== 12.8 Consolidación de Resultados
<consolidación-de-resultados>
El módulo app/utils/results.py implementa la función
consolidar\_resultados\(), que recibe los diccionarios normalizados de
spider, ZAP, ffuf y SQLMap y genera una estructura unificada con un
bloque de resumen \(conteos agregados) y los resultados completos de
cada herramienta. La función resultados\_prueba\_json\() persiste el
resultado consolidado en un archivo JSON en output/raw/.

== 12.9 Autenticación Automática
<autenticación-automática>
El sistema implementa un flujo de login programático contra DVWA
\(establecer\_sesion\_automatica\()): obtiene el token CSRF del
formulario de login, envía las credenciales, fija el nivel de seguridad
de la aplicación y verifica el éxito del login. Si el login falla, el
sistema intenta inicializar automáticamente la base de datos de la
aplicación objetivo mediante setup.php antes de reintentar. La cookie de
sesión obtenida se reutiliza para autenticar a ZAP, ffuf y SQLMap, y se
renueva antes de ejecutar SQLMap para evitar que expire durante el
escaneo activo de ZAP.

== 12.10 API REST y Frontend
<api-rest-y-frontend>
El módulo api.py \(FastAPI) expone el pipeline como servicio: POST /scan
lanza un escaneo en segundo plano; GET /scan/{id}/progress permite
consultar el porcentaje de avance; GET /scans lista el historial
persistido; GET /scan/{id} devuelve el detalle de un escaneo puntual;
DELETE /scan/{id} realiza un borrado lógico. Al finalizar un escaneo, la
API notifica su finalización mediante un webhook HTTP a un flujo de n8n.
El frontend, desarrollado en React, consume estos endpoints para ofrecer
un panel de dominios escaneados, un formulario de lanzamiento de
escaneos, una tabla de vulnerabilidades y un componente de sugerencias
de mitigación que consulta un endpoint adicional de análisis asistido
por IA expuesto a través del router de n8n.

#strong[Nota sobre pruebas.] Los scripts test\_parsers.py,
test\_speed.py, test\_zap.py y test\_sqlmap.py son scripts de
verificación manual \(ejecutan una función y muestran el resultado por
consola), no una suite de pruebas unitarias automatizadas con
aserciones.
