= 4. Objetivos
<objetivos>
== 4.1 Objetivo General
<objetivo-general>
Diseñar e implementar un sistema automatizado que permita orquestar
múltiples herramientas de análisis de seguridad web para detectar
vulnerabilidades en aplicaciones web, consolidar los resultados en
reportes unificados y exponer el sistema como un servicio reutilizable.

== 4.2 Objetivos Específicos
<objetivos-específicos>
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
