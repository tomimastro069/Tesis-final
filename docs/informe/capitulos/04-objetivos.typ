= 4. Objetivos
<objetivos>

== 4.1 Objetivo General
<objetivo-general>

Diseñar e implementar un sistema automatizado que permita orquestar
múltiples herramientas de análisis de seguridad web para detectar
vulnerabilidades en aplicaciones web, consolidar los resultados en
reportes unificados y exponer el sistema como un servicio reutilizable.

El propósito central persigue resolver la fragmentación operativa y el
elevado costo temporal que impone la ejecución artesanal de auditorías
dinámicas de seguridad web. Al integrar herramientas heterogéneas bajo un
flujo coordinado y desatendido, la investigación busca desplazar los
análisis hacia etapas tempranas del ciclo de vida del software \(paradigma
#emph[Shift-Left]\), dotando a los equipos de desarrollo y aseguramiento de
la calidad de un artefacto de software extensible y reproducible que unifique
el descubrimiento de superficie, la explotación controlada y el reporte
estructurado de hallazgos.

== 4.2 Objetivos Específicos
<objetivos-específicos>

Para alcanzar el objetivo general, la investigación tecnológica aplicada se
descompone en nueve objetivos específicos que abarcan el ciclo integral de
ingeniería y validación experimental. Estos objetivos se articulan en torno
a tres ejes metodológicos y funcionales complementarios:

- #strong[Eje de Integración y Detección Dinámica \(OE1, OE3, OE6):]
  orientado a coordinar la triada de escaneo dinámico \(OWASP ZAP, ffuf y
  SQLMap) mediante mecanismos de enriquecimiento cruzado, parseo canónico
  de salidas heterogéneas y autenticación programática de sesiones, operando
  directamente sobre las variables dependientes de cobertura de análisis y
  número de vulnerabilidades detectadas \(sección 10.3).

- #strong[Eje de Arquitectura de Software, Contenerización y Servicios \(OE2, OE4, OE7):]
  enfocado en concebir una estructura modular desacoplada basada en
  principios SOLID, aislar y aprovisionar los componentes en contenedores
  Docker Compose sobre una red dedicada, y exponer el pipeline como una
  API REST asíncrona con persistencia de historial, garantizando la
  manipulación controlada de la variable independiente de automatización y el
  rigor de las variables de control \(sección 10.3).

- #strong[Eje de Validación Experimental, Comunicación y Usabilidad \(OE5, OE8, OE9):]
  destinado a someter el artefacto a evaluación empírica en un entorno de
  laboratorio controlado \(DVWA) bajo los criterios de validación formales
  de la sección 10.6, sintetizar los resultados en reportes diferenciados
  con estimación de riesgo, y proveer una interfaz web interactiva que
  democratice la operación del sistema para usuarios no especialistas.

#pagebreak()

A continuación se detallan los nueve objetivos específicos formulados para
el proyecto:

+ Integrar herramientas de análisis de seguridad web \(OWASP ZAP, ffuf y
  SQLMap) en un flujo de ejecución automatizado, enriqueciendo el
  análisis de cada herramienta con los hallazgos de las demás.

+ Diseñar una arquitectura modular que permita extender el sistema
  fácilmente mediante la incorporación de nuevas herramientas o módulos
  de análisis.

+ Implementar parsers especializados que normalicen los resultados
  generados por cada herramienta en un formato homogéneo.

+ Desplegar el sistema en un entorno contenerizado utilizando Docker,
  garantizando la reproducibilidad del entorno de ejecución.

+ Evaluar el funcionamiento del sistema en un entorno de pruebas
  controlado \(DVWA), verificando el cumplimiento de los criterios de
  validación definidos en la sección 10.6 \(funcionalidad,
  reproducibilidad, cobertura mínima de tres categorías OWASP Top 10 y
  consolidación completa de hallazgos).

+ Implementar un mecanismo de autenticación automática que permita al
  orquestador acceder a secciones protegidas de la aplicación objetivo
  durante el escaneo.

+ Exponer el orquestador como un servicio mediante una API REST que
  ejecute los análisis de forma asíncrona, persista el historial de
  escaneos y permita su consulta posterior.

+ Generar automáticamente dos variantes de reporte —técnico y ejecutivo—
  con clasificación de riesgo global, orientadas a audiencias técnicas y
  no técnicas respectivamente.

+ Desarrollar una interfaz web que consuma la API del orquestador y
  permita lanzar escaneos, visualizar su progreso y consultar los
  hallazgos sin requerir acceso a la línea de comandos.

#emph[Nota de verificación metodológica:] El grado de cumplimiento, la
trazabilidad documental y la contrastación empírica de cada uno de estos
nueve objetivos específicos se auditan de forma exhaustiva y positiva en la
#strong[Tabla 12] de la subsección 15.1.1.
