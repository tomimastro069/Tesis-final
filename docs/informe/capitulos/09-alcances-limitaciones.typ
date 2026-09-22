= 9. Alcances y Limitaciones
<alcances-y-limitaciones>
== 9.1 Alcances
<alcances>
#quote(block: true)[
El proyecto cubre el diseño, la implementación y la validación de un
orquestador de seguridad funcional en un entorno de laboratorio
controlado, con las siguientes capacidades implementadas y verificadas:
]

- Ejecución automatizada de tres herramientas de análisis de seguridad
  \(OWASP ZAP, ffuf y SQLMap), con enriquecimiento cruzado entre ffuf y
  ZAP.

- Autenticación automática contra la aplicación objetivo, incluyendo
  renovación de sesión durante ejecuciones prolongadas.

- Descubrimiento de URLs mediante el spider de ZAP y fuzzing de
  directorios mediante ffuf con wordlists configurables.

- Detección de inyecciones SQL mediante SQLMap, con filtrado priorizado
  de URLs candidatas y ejecución en segundo plano.

- Parseo, normalización y consolidación de resultados en un archivo JSON
  unificado.

- Caché incremental de resultados y re-testeo automático de URLs
  previamente confirmadas como vulnerables.

- Generación automática de reportes técnico y ejecutivo, con
  clasificación de riesgo global.

- Exposición del orquestador mediante una API REST con ejecución
  asíncrona, seguimiento de progreso y persistencia de historial de
  escaneos.

- Interfaz web para lanzar escaneos, visualizar resultados y consultar
  sugerencias de mitigación asistidas por IA.

- Despliegue del entorno completo mediante Docker Compose.

== 9.2 Limitaciones
<limitaciones>
- El sistema fue probado únicamente sobre DVWA en un entorno de
  laboratorio; no se realizaron pruebas sobre aplicaciones en
  producción, por lo que la generalización de los resultados a otros
  contextos no está garantizada.

- La API no implementa autenticación ni restricción de origen \(CORS
  abierto a cualquier dominio), por lo que su uso actual está limitado a
  entornos de laboratorio y no a un despliegue expuesto públicamente.

- Las sugerencias de mitigación generadas por el componente de IA no
  fueron validadas sistemáticamente contra un criterio experto; deben
  tratarse como apoyo complementario, no como fuente única de
  remediación.

- La clasificación de riesgo global del reporte ejecutivo utiliza una
  heurística simple \(presencia de hallazgos High/SQL Injection), no un
  criterio estándar de la industria como CVSS.

- Debe señalarse la ausencia de una comparación empírica de alcance
  equivalente entre la ejecución del pipeline automatizado y un proceso
  de descubrimiento manual independiente; los registros del capítulo 17
  corresponden a una sesión de validación y triaje sobre hallazgos ya
  detectados en nivel #emph[Low];, lo que imposibilita la verificación
  controlada que exige H1 \(véanse la sección 6 y el análisis
  metodológico en 14.2).

- No se cuantificó formalmente, mediante ejecuciones controladas de cada
  herramienta en aislamiento, la cobertura individual frente a la
  cobertura combinada; el capítulo 14 aporta evidencia sobre una única
  ejecución, no un experimento repetido, lo que limita el alcance de la
  validación empírica de H2.

- Los resultados de herramientas de escaneo dinámico como ZAP y SQLMap
  pueden variar entre ejecuciones sucesivas contra el mismo objetivo
  \(ver 10.5, amenaza a la validez de Confiabilidad); las cifras
  reportadas en el capítulo 13 corresponden a una ejecución puntual y
  documentada, no a un promedio de múltiples corridas.

- El orquestador concentra su capacidad de detección dinámica en fallas
  identificables mediante inyección de firmas y análisis de respuestas
  HTTP \(inyecciones SQL, vectores reflejados de XSS, omisión de
  cabeceras de seguridad y descubrimiento de rutas ocultas). Quedan
  explícitamente excluidas del alcance automatizado las vulnerabilidades
  de lógica de negocio \(Business Logic Flaws), las fallas de control de
  acceso horizontal complejo entre múltiples perfiles de usuario y las
  condiciones de carrera \(Race Conditions), vectores que por su
  naturaleza contextual y semántica exigen necesariamente una auditoría
  manual experta.
