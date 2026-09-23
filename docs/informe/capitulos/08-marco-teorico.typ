= 8. Marco Teórico y Conceptual
<marco-teórico-y-conceptual>
== 8.1 Fuzzing
<fuzzing>
El fuzzing es una técnica de pruebas de seguridad que consiste en enviar
entradas inesperadas o malformadas a un sistema con el objetivo de
identificar comportamientos anómalos o vulnerabilidades \(Alsaedi et
al., 2021). Se distinguen tres enfoques según el nivel de conocimiento
del sistema bajo prueba: black-box \(sin conocimiento interno, basado
únicamente en la interfaz expuesta), grey-box \(con conocimiento
parcial, por ejemplo instrumentación de cobertura) y white-box \(con
acceso completo al código fuente). La herramienta ffuf utilizada en este
proyecto corresponde a un fuzzing black-box de tipo directory fuzzing:
un subtipo específico de fuzzing web orientado al descubrimiento de
rutas, distinto del fuzzing de parámetros o del fuzzing de protocolos de
red y binarios \(Alsaedi et al., 2021).

== 8.2 Escaneo de Vulnerabilidades
<escaneo-de-vulnerabilidades>
Se distingue entre DAST \(Dynamic Application Security Testing), que
analiza la aplicación en ejecución sin acceso a su código fuente —el
enfoque utilizado por OWASP ZAP en este proyecto—, y SAST \(Static Application Security Testing), que analiza el código
fuente sin ejecutarlo. Qadir et al. \(2025) comparan empíricamente ambos
enfoques sobre setenta y cinco aplicaciones reales y concluyen que son
complementarios antes que sustitutos: las herramientas SAST detectan
mejor vulnerabilidades de severidad alta en etapas tempranas, mientras
que las DAST —como las utilizadas en este proyecto— identifican fallas que solo se
manifiestan en tiempo de ejecución \(Qadir et al., 2025). Dentro del
enfoque DAST se distinguen además el escaneo pasivo \(análisis del
tráfico sin modificar solicitudes) y el escaneo activo \(envío de
payloads para verificar vulnerabilidades).

== 8.3 Contenedores Docker
<contenedores-docker>
Docker permite ejecutar aplicaciones dentro de contenedores aislados que
comparten el kernel del sistema operativo anfitrión, a diferencia de la
virtualización completa, que emula hardware y ejecuta un sistema
operativo independiente por cada máquina virtual. Para este proyecto,
Docker se eligió por su menor sobrecarga de recursos y su tiempo de
arranque casi instantáneo, adecuado para levantar y destruir entornos de
laboratorio repetidamente. Esta elección tiene una implicancia de
seguridad relevante: al compartir kernel, un contenedor mal configurado
representa una superficie de escape potencial hacia el host. Javed y
Toor \(2021), en una evaluación de herramientas de detección de
vulnerabilidades en contenedores \(Clair, Anchore y Microscanner) sobre
imágenes públicas de Docker Hub, encontraron que ninguna de las tres
herramientas detecta de forma confiable vulnerabilidades a nivel de
paquetes de aplicación —solo del sistema operativo base—, lo que
refuerza por qué este proyecto no delega el análisis de seguridad de la
aplicación al propio motor de contenedores, sino a herramientas
dedicadas de DAST y fuzzing que operan sobre el servicio en ejecución
\(Javed & Toor, 2021). Por este motivo, los servicios de este proyecto
se ejecutan sin privilegios extendidos.

== 8.4 OWASP Top 10
<owasp-top-10>
El proyecto OWASP publica periódicamente una lista de las diez
categorías de riesgo más críticas para aplicaciones web \(OWASP
Foundation, 2021). Además de la inyección \(A03:2021) y las fallas de
configuración \(A05:2021), el sistema desarrollado también detecta
hallazgos de la categoría A01:2021 \(Broken Access Control, mediante
rutas administrativas descubiertas por ffuf) y, a través de sus
componentes de autenticación, resulta relevante para A07:2021 \(fallas
de identificación y autenticación).

== 8.5 Pipeline de Datos y Arquitectura Modular
<pipeline-de-datos-y-arquitectura-modular>
El pipeline implementado sigue el patrón arquitectónico conocido como
Pipeline Pattern \(o Pipes and Filters), en el que los datos fluyen a
través de una secuencia de etapas de transformación, cada una con una
responsabilidad única; este patrón fue formalizado por Buschmann,
Meunier, Rohnert, Sommerlad y Stal \(1996) en su catálogo de patrones de
arquitectura de software como una solución recurrente para sistemas que
procesan datos en etapas independientes y reemplazables, propiedad que
en este proyecto se aprovecha para intercalar la inyección de rutas de
ffuf en la sesión de ZAP sin modificar el resto de las etapas del
pipeline \(Buschmann et al., 1996). La separación entre runners,
scanners, parsers y workflow responde adicionalmente al principio de
responsabilidad única \(Single Responsibility Principle), uno de los
cinco principios SOLID de diseño orientado a objetos sistematizados por
Martin \(2003), según el cual un módulo debe tener una única razón para
cambiar; en este proyecto, esa separación es lo que permite sustituir o
extender un scanner o un parser sin afectar al resto del pipeline
\(Martin, 2003).

== 8.6 Orquestación y Automatización de Seguridad \(SOAR)
<orquestación-y-automatización-de-seguridad-soar>
El concepto de SOAR \(Security Orchestration, Automation and Response)
engloba las tecnologías que permiten integrar herramientas de seguridad
dispares, automatizar tareas repetitivas de análisis y estandarizar la
respuesta ante hallazgos \(Kinyua & Awuah, 2021). La extensión de este
proyecto hacia una API con ejecución asíncrona, persistencia de
historial y notificación mediante webhooks a un flujo de n8n lo
posiciona conceptualmente dentro de esta categoría, aunque a una escala
considerablemente más acotada que las plataformas SOAR comerciales o de
código abierto de mayor madurez descriptas en el Estado del Arte. Kinyua
y Awuah \(2021) identifican la incorporación de aprendizaje automático
para la priorización de alertas como una de las principales direcciones
futuras del campo; este proyecto no implementa dicha capacidad, pero sí
incorpora un componente de sugerencias de mitigación asistidas por IA
\(sección 12.10), conceptualmente cercano a esa dirección de trabajo.
