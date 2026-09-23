= 1. Introducción
<introducción>
Las aplicaciones web constituyen actualmente uno de los componentes más
importantes de la infraestructura digital moderna. Empresas,
instituciones educativas, organismos gubernamentales y plataformas
comerciales dependen cada vez más de sistemas accesibles a través de
internet para brindar servicios a usuarios finales.

Esta dependencia creciente tiene un correlato directo en el panorama de
amenazas: según el Data Breach Investigations Report 2025 de Verizon,
los ataques básicos a aplicaciones web \(Basic Web Application Attacks)
representaron el 12% de las brechas de seguridad analizadas en 2025,
frente al 9% del año anterior, y el 88% de esos ataques involucró
credenciales robadas \(Verizon, 2025). El Cost of a Data Breach Report
2025 de IBM sitúa el costo global promedio de una brecha de seguridad en
4,44 millones de dólares \(IBM, 2025). Estas cifras contextualizan, con
datos verificables, la afirmación de que las aplicaciones web son un
vector de riesgo relevante y creciente.

Entre las vulnerabilidades más comunes en este tipo de aplicaciones se
encuentran las inyecciones SQL, el Cross Site Scripting \(XSS), las
configuraciones de seguridad incorrectas, la autenticación débil y la
exposición de endpoints internos. Estas categorías están ampliamente
documentadas por la comunidad de seguridad informática, particularmente
a través del proyecto OWASP Top 10, que identifica las categorías de
riesgo más críticas para aplicaciones web.

Tradicionalmente, la detección de estas vulnerabilidades se realiza
mediante auditorías de seguridad manuales o mediante herramientas
especializadas de escaneo dinámico \(DAST, Dynamic Application Security
Testing), que analizan la aplicación en ejecución sin acceso a su código
fuente \(Qadir et al., 2025). El uso individual de estas herramientas
requiere conocimientos técnicos avanzados y un proceso manual de
correlación de resultados entre herramientas heterogéneas. Frente a esta
problemática surge la necesidad de soluciones que integren múltiples
herramientas dentro de un flujo coordinado, un enfoque que en la
industria se enmarca dentro de lo que se conoce como SOAR \(Security
Orchestration, Automation and Response): la orquestación de herramientas
de seguridad, la automatización de tareas repetitivas y la
centralización de la respuesta ante hallazgos \(Kinyua & Awuah, 2021).

Este trabajo integra tres herramientas que, en conjunto, cubren vectores
de ataque complementarios: OWASP ZAP realiza escaneo dinámico general
\(pasivo y activo) sobre la aplicación en ejecución; ffuf se especializa
en el descubrimiento de rutas, directorios y endpoints no enlazados
mediante fuzzing de directorios \(Alsaedi et al., 2021); y SQLMap se
enfoca específicamente en la detección y explotación de inyecciones SQL,
un tipo de vulnerabilidad que los escáneres generales suelen identificar
con menor profundidad que una herramienta dedicada \(Elia et al., 2010).
La combinación de una herramienta de propósito general, una de
descubrimiento de superficie de ataque y una especializada en un vector
crítico busca maximizar la cobertura sin incurrir en la complejidad de
plataformas comerciales de mayor escala.

Trabajos previos sobre orquestación de seguridad se discuten en detalle
en el Capítulo 7 \(Estado del Arte), donde se contrastan plataformas de
código abierto orientadas a la gestión y orquestación de resultados de
seguridad —Faraday, DefectDojo, TheHive y Shuffle— con la propuesta de
este trabajo \(ver Tabla 1). La brecha específica que este proyecto
busca cubrir es la ausencia, entre esas alternativas, de una opción
liviana que no requiera infraestructura compleja de despliegue,
orientada puntualmente al escaneo web interactivo mediante fuzzing y
escaneo activo, y desplegable en su totalidad con un único comando de
Docker Compose.

En este contexto se desarrolla el presente proyecto, cuyo objetivo es
diseñar e implementar un orquestador automatizado de herramientas de
seguridad web capaz de ejecutar distintos tipos de análisis, normalizar
los resultados heterogéneos producidos por cada herramienta y generar
reportes unificados de vulnerabilidades detectadas. A partir de esta
base, el sistema se extendió hacia una arquitectura de servicio: una API
REST que ejecuta los análisis de forma asíncrona, persiste el historial
de escaneos y expone los resultados a un panel web, con soporte de
autenticación automática para escanear secciones protegidas y de
sugerencias de mitigación asistidas por inteligencia artificial. El
sistema fue probado en un entorno de laboratorio controlado utilizando
DVWA como aplicación objetivo, garantizando un marco ético y
reproducible para la investigación.

#strong[Estructura del documento:] El presente trabajo se encuentra
articulado de la siguiente manera: las secciones 2 a 6 definen la
problemática, justificación, metas, interrogantes e hipótesis
orientadoras. Las bases teóricas y el estado del arte se examinan en las
secciones 7 y 8, dando paso a la delimitación y metodología en los
apartados 9 y 10. La arquitectura del sistema, el modelo de servicio y
la implementación técnica del pipeline se detallan en los capítulos 11 y
12. La presentación de hallazgos y su debate técnico se abordan en las
secciones 13 y 14, condensando las conclusiones y líneas de
investigación futuras en el capítulo 15. Por último, la sección 16
aborda las consideraciones éticas y normativas, el capítulo 17
profundiza el desarrollo experimental y los apartados 18 y 19 reúnen las
fuentes bibliográficas y anexos técnicos.
