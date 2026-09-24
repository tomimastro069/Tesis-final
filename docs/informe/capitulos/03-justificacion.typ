= 3. Justificación
<justificación>

La fundamentación de esta investigación se estructura sobre cuatro dimensiones
complementarias que articulan las competencias formativas de la carrera, las
demandas técnicas de la ingeniería de software moderna, la viabilidad económica
y la transferencia hacia el medio socio-productivo.

== 3.1 Justificación Académica e Integración Formativa en la TUP
<justificación-académica>

Desde la perspectiva académica e institucional, el desarrollo del presente
Trabajo Final de Grado materializa la convergencia interdisciplinaria de las
principales áreas de conocimiento que configuran el plan de estudios de la
Tecnicatura Universitaria en Programación \(TUP) de la Universidad Tecnológica
Nacional — Facultad Regional Mendoza. Lejos de constituir una aplicación
aislada de conceptos, el orquestador requirió articular de manera transversal:

1. *Programación Orientada a Objetos y Buenas Prácticas:* Implementación
  robusta en Python 3.11, aplicando principios de diseño orientado a objetos,
  modularización, tipado estático auxiliar y gestión estructurada de
  excepciones en la capa del orquestador central \(Python Software Foundation, 2024).
2. *Diseño y Arquitectura de Software:* Adopción rigurosa del patrón de diseño
  Pipeline y de los principios SOLID —en particular, el principio de
  responsabilidad única y el de abierto/cerrado— para desacoplar el ciclo de
  vida de la ejecución respecto de los módulos de parsing y persistencia
  \(Buschmann et al., 1996; Martin, 2003).
3. *Bases de Datos y Persistencia Estructurada:* Modelado y gestión de
  persistencia de sesiones, metadatos, historial de escaneos y caché
  incremental mediante bases de datos relacionales con soporte SQLite y
  proyección hacia PostgreSQL, asegurando integridad transaccional.
4. *Redes, Protocolos y Comunicaciones:* Manipulación analítica del protocolo
  HTTP/HTTPS, inspección de cabeceras, gestión de códigos de respuesta, manejo
  de cookies de sesión y autenticación contextual requerida para la
  evaluación profunda de endpoints.
5. *Infraestructura y Contenedores:* Aislamiento de dependencias y entornos de
  ejecución heterogéneos mediante la tecnología de contenedores Docker y
  orquestación liviana con Docker Compose \(Docker Inc., 2024).
6. *Servicios Web e Interfaz de Usuario:* Extensión del núcleo analítico hacia
  una arquitectura de servicios orientada a la web, implementando una API REST
  asíncrona mediante FastAPI y una interfaz gráfica interactiva en React.

Asimismo, el proyecto aporta un caso de estudio reproducible para la enseñanza
de la ciberseguridad ofensiva y las pruebas de software en el ámbito
universitario, permitiendo a los estudiantes contrastar empíricamente cómo
interactúan los vectores de vulnerabilidad en entornos de laboratorio controlados.
#pagebreak()
== 3.2 Justificación Técnica: Paradigma Shift-Left y Enriquecimiento Cruzado
<justificación-técnica>

Desde la perspectiva técnica y metodológica, la integración continua y la
entrega continua \(CI/CD) han acelerado radicalmente el ciclo de vida del
desarrollo de software. No obstante, las evaluaciones de seguridad dinámicas
\(DAST) tradicionales suelen introducir una severa fricción operativa:
requieren configuraciones manuales complejas, generan salidas incompatibles y
demandan lapsos temporales incompatibles con la agilidad requerida en los
despliegues modernos.

El orquestador desarrollado resuelve esta problemática mediante dos
contribuciones arquitectónicas clave:

1. *Adopción del Paradigma Shift-Left:* Permite trasladar el análisis de
  seguridad dinámico hacia las etapas tempranas del desarrollo. Al condensar
  el escaneo en una rutina automatizada que insume entre 4 y 14 minutos
  —según la activación o no de la caché incremental documentada en la
  Tabla 10—, los equipos de desarrollo pueden ejecutar auditorías periódicas
  sin obstaculizar el flujo de entregas.
2. *Enriquecimiento Cruzado de Herramientas \(Cross-Tool Feeding):* A
  diferencia de la ejecución en silos aislados, el pipeline implementa un flujo
  coordinado donde los hallazgos de una fase nutren la ejecución de la siguiente.
  El fuzzer de alto rendimiento \(ffuf) descubre directorios y rutas ocultas
  que escapan al rastreo estándar; dicha superficie de ataque descubierta es
  transferida de forma inmediata al escáner dinámico \(OWASP ZAP) para su
  evaluación activa, y aquellos endpoints sospechosos de procesar parámetros
  dinámicos vulnerables son analizados en profundidad por el motor
  especializado en inyecciones \(SQLMap).

Este enfoque reduce drásticamente la tasa de omisión derivada de herramientas
desarticuladas y minimiza el error humano intrínseco a la configuración manual
de múltiples utilidades de consola.

== 3.3 Justificación Económica y Modelo Cuantitativo de Retorno de Inversión (ROI)
<justificación-económica>

Desde el punto de vista económico, las evaluaciones de seguridad tradicionales
representan una barrera financiera significativa. Una auditoría de seguridad
web externa o prueba de penetración manual profesional requiere
habitualmente entre 20 y 40 horas de labor técnica cualificada, con
honorarios que oscilan entre 50 y 150 USD por hora en el mercado especializado
\(SANS Institute, 2024).

Bajo un escenario estándar representativo de 30 horas profesionales a una
tarifa media conservadora de 100 USD por hora:

$ C_"auditoría" = 30 " horas" times 100 "USD" / "hora" = 3.000 " USD" $

Para una organización que implemente un esquema básico de revisiones
trimestrales, el costo operativo anual directo asciende a:

$ C_"anual" = 3.000 " USD" times 4 " revisiones" = 12.000 " USD/año" $

Este volumen de erogación resulta económicamente inviable para pequeñas y
medianas empresas \(PyMEs), centros académicos o proyectos emergentes,
induciendo a prescindir de controles de seguridad dinámicos antes del paso a
producción. Por otra parte, las plataformas comerciales de orquestación y
gestión de vulnerabilidades reservan sus capacidades avanzadas de
automatización para suscripciones corporativas de costo prohibitivo
\(DefectDojo, 2025; Faraday Security, 2025).

Frente a este escenario, la solución implementada demuestra un balance de
retorno de inversión \(ROI) altamente favorable:

- *Costo Directo de Licenciamiento:* 0 USD, al basarse íntegramente en
  tecnologías de código abierto de grado industrial \(OWASP ZAP, ffuf, SQLMap,
  Docker, FastAPI, React).
- *Optimización Temporal del Recurso Humano:* El pipeline automatizado
  ejecuta las tareas rutinarias de reconocimiento, fuzzing masivo y escaneo
  activo en un intervalo acotado de 4 a 14 minutos, permitiendo que el
  profesional concentre su tiempo exclusivamente en el triaje y validación
  final de hallazgos críticos.
- *Mitigación Preventiva de Costos por Incidentes:* Según el informe global
  de IBM \(2025), el costo promedio de una filtración de datos asciende a
  4,44 millones de dólares. Detectar fallas críticas como inyecciones SQL
  o credenciales expuestas en fases tempranas previene impactos financieros
  y legales de orden catastrófico para la organización.


== 3.4 Transferencia Tecnológica y Replicabilidad en PyMEs y Ámbito Educativo
<transferencia-tecnológica>

Finalmente, el proyecto posee una clara vocación de transferencia tecnológica.
La arquitectura no se restringe a un script de uso personal, sino que se
formaliza como un prototipo desacoplado, modular y reproducible:

1. *Democratización para el Ecosistema PyME:* Brinda a organizaciones sin
  departamentos formales de ciberseguridad una herramienta accesible,
  desplegable en minutos mediante un único comando de orquestación
  \(`docker compose up`), capaz de entregar un reporte consolidado en JSON y
  Markdown sin costos recurrentes.
2. *Valor Pedagógico y Transferencia Académica:* Funciona como un entorno de
  laboratorio para que cátedras de desarrollo de software y seguridad puedan
  experimentar con la automatización DAST y el paradigma Shift-Left sobre
  blancos controlados como DVWA.
3. *Extensibilidad Arquitectónica:* La separación limpia entre la capa de
  ejecución, la API REST asíncrona y la interfaz web asegura que otros equipos
  puedan extender el sistema integrando nuevas herramientas de escaneo
  \(ej. análisis de contenedores o escaneo SSL) mediante el patrón de diseño
  establecido.
