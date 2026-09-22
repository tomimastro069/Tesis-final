= 10. Metodología
<metodología>
== 10.1 Diseño de la Investigación
<diseño-de-la-investigación>
#quote(block: true)[
Se adopta un paradigma post-positivista con enfoque predominantemente
cuantitativo en la medición de variables del sistema \(cantidad de
hallazgos, severidad, cobertura), combinado con un diseño de
investigación tecnológica aplicada de tipo constructivo: el objetivo
central no es contrastar una hipótesis mediante un experimento
controlado con grupo de comparación, sino diseñar, construir y validar
un artefacto de software contra criterios de aceptación predefinidos. El
método de trabajo es iterativo e incremental: cada componente del
pipeline se implementa, prueba y valida de forma independiente antes de
ser integrado al sistema completo. Las pruebas de funcionamiento se
realizan mediante la ejecución del pipeline contra DVWA, una aplicación
web intencionalmente vulnerable utilizada como entorno de prueba
\(testbed), y los resultados se evalúan contra los criterios de
validación definidos en la sección 10.6.
]

== 10.2 Fases del Proyecto
<fases-del-proyecto>
#quote(block: true)[
El proyecto se desarrolló en seis fases secuenciales. La primera fase
consistió en la investigación de herramientas de seguridad web, donde se
evaluaron las capacidades, formatos de salida y posibilidades de
integración de diversas herramientas open source. La segunda fase abordó
el diseño de la arquitectura del sistema, definiendo la estructura
modular de paquetes, los flujos de datos y las interfaces entre
componentes. La tercera fase fue la implementación del orquestador en
Python, incluyendo los módulos de ejecución, escaneo, parseo y
consolidación. La cuarta fase comprendió la integración con contenedores
Docker, configurando el archivo docker-compose.yml para desplegar DVWA,
ZAP y la aplicación orquestadora. La quinta fase se dedicó al desarrollo
de parsers de resultados, implementando la normalización de las salidas
heterogéneas de cada herramienta. La sexta fase consistió en las pruebas
en entorno de laboratorio, ejecutando el pipeline completo contra DVWA y
documentando los resultados obtenidos.

Una séptima fase, posterior a la planificación original, extendió el
sistema hacia un servicio persistente: incorporó autenticación
automática contra la aplicación objetivo, una capa de base de datos
\(SQLite/PostgreSQL) para historial de escaneos y caché incremental, una
API REST \(FastAPI) para ejecución asíncrona del pipeline, y un frontend
web que consume dicha API para lanzar escaneos y visualizar resultados.
]

== 10.3 Variables
<variables>
#quote(block: true)[
La variable independiente de la investigación es la automatización del
proceso de análisis de seguridad mediante el orquestador. Se define
operacionalmente como la ejecución coordinada de las herramientas OWASP
ZAP \(spider y escaneo activo), ffuf y SQLMap a través del pipeline
implementado en Python, en contraposición a la ejecución manual e
independiente de cada herramienta por parte de un analista.

Las variables dependientes son las siguientes:
]

+ Número de vulnerabilidades detectadas: cantidad total de hallazgos de
  seguridad identificados por el sistema durante una ejecución completa
  del pipeline, medida a partir del archivo JSON unificado generado por
  el módulo de consolidación.

+ Severidad de los hallazgos: clasificación de las vulnerabilidades
  detectadas según su nivel de riesgo \(High, Medium, Low,
  Informational), tal como es reportada por las herramientas integradas,
  particularmente por OWASP ZAP.

+ Cobertura de análisis: cantidad de URLs únicas descubiertas y
  analizadas por el conjunto de herramientas, incluyendo las
  identificadas por el spider, las verificadas por el escaneo activo,
  las descubiertas por el fuzzing de directorios y las incorporadas como
  URL semilla o por el módulo de autenticación \(ver nota de composición
  en la sección 13.1).

+ Tiempo de ejecución del pipeline: duración de cada etapa y del proceso
  completo, medible mediante instrumentación de timestamps al inicio y
  fin de cada etapa. Actualmente esta medición es parcial: cubre el
  mecanismo de caché de ffuf mediante test\_speed.py y el pipeline
  completo mediante la comparación con/sin caché de la sección 14.3, y
  está pendiente de extenderse a una medición equivalente del proceso
  manual \(ver 14.2).

#quote(block: true)[
Las variables de control comprenden el entorno objetivo \(DVWA en su
configuración por defecto), las versiones específicas de las
herramientas utilizadas \(imágenes Docker), las wordlists empleadas por
ffuf, y los niveles de profundidad y riesgo configurados en SQLMap.
]

== 10.4 Instrumentos
<instrumentos>
#quote(block: true)[
Los instrumentos utilizados en la investigación son los propios
componentes del sistema desarrollado. Los contenedores Docker
constituyen la infraestructura de ejecución que garantiza la
reproducibilidad del entorno. El pipeline Python \(Python Software
Foundation, 2024) actúa como el instrumento principal de recolección de
datos, coordinando la ejecución de cada herramienta y registrando sus
salidas crudas. Los parsers especializados funcionan como instrumentos
de transformación, normalizando los datos heterogéneos en un formato
homogéneo. El módulo de consolidación actúa como instrumento de
síntesis, unificando los resultados en un único archivo JSON
estructurado que constituye la fuente de datos para el análisis. El
script test\_speed.py funciona como instrumento de medición de tiempo,
comparando la duración de una primera ejecución de ffuf sin caché contra
ejecuciones posteriores con caché activa sobre el mismo objetivo.
]

== 10.5 Amenazas a la Validez
<amenazas-a-la-validez>
- #strong[Validez interna:] DVWA es un entorno diseñado deliberadamente
  para ser vulnerable, lo que puede facilitar artificialmente la
  detección de hallazgos respecto a una aplicación real con controles de
  seguridad activos.

- #strong[Validez externa:] los resultados obtenidos sobre DVWA no son
  necesariamente generalizables a aplicaciones en producción con
  arquitecturas, frameworks o controles de seguridad distintos.

- #strong[Confiabilidad:] no se verificó formalmente si ZAP y SQLMap
  producen resultados idénticos entre ejecuciones repetidas sobre el
  mismo objetivo sin cambios; el mecanismo de caché asume, pero no
  confirma explícitamente, esta estabilidad. Esta amenaza dejó de ser
  hipotética en esta entrega: al comparar la corrida documentada en el
  capítulo 13 con corridas previas del mismo pipeline sobre el mismo
  objetivo, se observaron diferencias en el número total de URLs y
  alertas detectadas entre ejecuciones \(ver nota metodológica del
  capítulo 13), lo cual confirma empíricamente que la reproducibilidad
  exacta no está garantizada y refuerza la necesidad de declarar, en
  cada reporte de resultados, la fecha y las condiciones puntuales de la
  corrida que se está documentando.

== 10.6 Criterios de Validación
<criterios-de-validación>
#quote(block: true)[
Un componente del sistema se considera validado cuando cumple
simultáneamente los siguientes criterios:
]

- #strong[Funcionalidad:] la herramienta se ejecuta correctamente dentro
  del pipeline y produce una salida procesable por el parser
  correspondiente.

- #strong[Reproducibilidad:] una ejecución posterior del pipeline sobre
  el mismo objetivo produce resultados equivalentes en estructura y tipo
  de hallazgos. Se considera reproducible si dos ejecuciones sucesivas,
  sin cambios en la aplicación objetivo, coinciden en al menos el 90% de
  los hallazgos detectados. Este criterio fue verificado empíricamente
  en el benchmark de ejecuciones sucesivas documentado en la sección
  14.3 \(Tabla 11), donde la coincidencia de alertas de seguridad de
  OWASP ZAP y de vulnerabilidades de SQLMap alcanzó el 100%, y la
  estabilidad en la superficie de URLs analizadas fue del 96,3%,
  superando holgadamente el umbral de aceptación del 90%. La leve
  variación en el número de URLs del spider responde a la naturaleza
  dinámica del rastreo web analizada en la sección 10.5, mientras que el
  núcleo de detección crítica de vulnerabilidades demostró una
  estabilidad absoluta.

- #strong[Cobertura:] el sistema detecta vulnerabilidades pertenecientes
  a al menos tres categorías distintas del OWASP Top 10.

- #strong[Consolidación:] todos los hallazgos de las herramientas
  individuales se integran correctamente en el archivo JSON unificado
  final.
