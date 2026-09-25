= 9. Alcances y Limitaciones
<alcances-y-limitaciones>
== 9.1 Alcances
<alcances>

El presente trabajo final de graduación abarca el diseño, la implementación, el despliegue y la validación experimental de un sistema de orquestación de seguridad informática concebido para coordinar herramientas dinámicas heterogéneas en entornos controlados de laboratorio. A partir de una arquitectura desacoplada y orientada a servicios, el alcance funcional del artefacto desarrollado comprende tres bloques operativos plenamente verificados:

#strong[a) Núcleo de Detección Dinámica y Enriquecimiento Cruzado:]

- Coordinación automatizada y secuencial de la triada DAST de código abierto: OWASP ZAP para escaneo pasivo y activo de vulnerabilidades generales, ffuf para el descubrimiento de superficie oculta mediante _fuzzing_ de directorios con diccionarios parametrizables, y SQLMap para la detección profunda y verificación de inyecciones SQL.

- Mecanismo de enriquecimiento cruzado inter-herramienta: realimentación automatizada del árbol de URLs de OWASP ZAP a partir de las rutas y parámetros descubiertos durante la fase de fuzzing con ffuf, e interoperabilidad hacia SQLMap para transferir selectivamente endpoints parametrizados sospechosos.

- Módulo de autenticación automatizada y gestión de sesiones HTTP: inicio de sesión programático mediante solicitudes POST y renovación heurística de cookies de sesión para sostener el análisis en secciones restringidas durante escaneos prolongados.

- Filtrado heurístico y ejecución asíncrona de SQLMap: discriminación previa de URLs candidatas basada en la existencia de parámetros manipulables y ejecución desacoplada en segundo plano para evitar bloqueos del flujo principal.

#strong[b) Capa de Persistencia, Caché y API de Servicio:]

- Ingesta, parseo sintáctico y normalización de salidas dispares: transformación de las respuestas heterogéneas \(XML/JSON de ZAP, JSON estructurado de ffuf y registros de texto plano de SQLMap) hacia un esquema canónico consolidado en formato JSON \(#emph[resultado_unificado.json]\).

- Motor de caché incremental y re-evaluación dirigida: indexación de hallazgos por identificador de endpoint y vector de ataque, permitiendo re-verificar con celeridad vulnerabilidades previamente confirmadas sin reiterar la ejecución exhaustiva del pipeline completo.

- Exposición de capacidades mediante arquitectura de servicio REST \(FastAPI): despacho asíncrono de tareas de análisis mediante subprocesos en segundo plano \(#emph[BackgroundTasks]\), monitoreo del ciclo de vida del escaneo en tiempo real y consulta histórica de auditorías.

- Capa de persistencia relacional híbrida: compatibilidad nativa tanto con SQLite para ejecuciones portátiles y pruebas locales, como con PostgreSQL para entornos de servicio multiusuario centralizados.

#strong[c) Interfaz de Usuario y Automatización Operativa:]

- Interfaz web interactiva \(Single Page Application desarrollada en React): panel de control para la parametrización de objetivos, visualización gráfica y tabular de vulnerabilidades consolidadas y consulta histórica de análisis.

- Generación automatizada de reportes técnico y ejecutivo: consolidación de resúmenes estructurados en formatos Markdown y JSON con matriz de riesgo global orientativa para audiencias técnicas y gerenciales.

- Asistencia en remediación mediante modelos de lenguaje: canal de consulta contextual a proveedores de inteligencia artificial \(Groq/Gemini) para sugerir directrices de mitigación técnica específicas frente a los hallazgos confirmados.

- Aprovisionamiento reproducible multicontenedor: despliegue integral del orquestador, la aplicación objetivo de prueba y los motores de análisis mediante Docker Compose sobre una red puente aislada \(#emph[sec-net]\).

== 9.2 Limitaciones
<limitaciones>

La declaración explícita de limitaciones constituye una salvaguarda metodológica indispensable en la ingeniería de seguridad de la información. Este ejercicio permite delimitar con precisión las condiciones bajo las cuales los resultados del orquestador son técnicamente reproducibles y válidos, evitando interpretaciones extrapoladas o falsas expectativas de cobertura en entornos productivos. Las restricciones identificadas se estructuran en tres dimensiones formales:

#strong[a) Delimitación del Entorno de Pruebas y Seguridad de la Infraestructura:]

- Validación circunscrita al entorno de laboratorio controlado: las pruebas empíricas se ejecutaron exclusivamente sobre la aplicación deliberadamente vulnerable DVWA \(Damn Vulnerable Web Application); no se realizaron auditorías sobre aplicaciones en producción reales ni contra infraestructuras protegidas por cortafuegos de aplicaciones web \(WAF), balanceadores de carga o mecanismos anti-escaneo adaptativos \(tales como desafíos CAPTCHA o bloqueo por frecuencia de peticiones), por lo que la extrapolación de los resultados a plataformas corporativas vivas no está empíricamente demostrada.

- Política de seguridad permisiva en la API REST de laboratorio: el prototipo implementado no incorpora autenticación de usuarios mediante tokens JWT u OAuth2, y opera con control de acceso cruzado abierto \(CORS configurado para aceptar cualquier origen), decisión adoptada deliberadamente para simplificar la interacción en el laboratorio local pero que inhabilita su exposición directa en redes públicas no confiables.

- Carácter estrictamente orientativo del componente de IA: las directrices de mitigación emitidas por los modelos de lenguaje no fueron contrastadas sistemáticamente contra un panel de expertos ni validadas mediante pruebas de regresión en código real; deben tratarse como sugerencias preliminares de apoyo y nunca como instrucciones definitivas de remediación.

#strong[b) Restricciones de Comparabilidad Metodológica y Rigor Estadístico:]

- Ausencia de experimento con grupo de control independiente para la medición de tiempos \(H1): el ahorro de esfuerzo se evaluó mediante el contraste analítico entre la duración del pipeline automatizado \(14 minutos) y los tiempos documentados en una sesión de validación y triaje sobre hallazgos ya detectados \(50 minutos manuales sobre 125 minutos totales; véanse el Capítulo 17 y la Tabla 13), pero sin un experimento ciego en el que auditores humanos realicen descubrimiento desde cero, lo que condiciona la verificación empírica formal de la Hipótesis 1 \(como se discute en la sección 14.2).

- Evaluación de cobertura basada en una corrida experimental única \(H2): el análisis comparativo de cobertura individual frente a la combinación de herramientas \(Tabla 9) se sustenta en una ejecución documentada y representativa, y no en un muestreo estadístico de múltiples repeticiones que permita calcular intervalos de confianza o varianzas, acotando el alcance demostrativo de la Hipótesis 2.

- Variabilidad intrínseca del escaneo dinámico y latencias de red: conforme a la amenaza a la confiabilidad descrita en la sección 10.5, factores como la latencia de la pila de red en Docker, la concurrencia de hilos y los tiempos de respuesta del servidor web pueden introducir variaciones marginales en el número de solicitudes procesadas entre corridas sucesivas.

- Modelo heurístico simplificado de clasificación de riesgo: el reporte ejecutivo categoriza el riesgo global mediante una regla booleana simple \(presencia de inyecciones SQL o alertas de severidad _High_\), prescindiendo de esquemas cuantitativos normalizados de la industria como el estándar CVSS \(Common Vulnerability Scoring System).

#strong[c) Vulnerabilidades Fuera de Alcance por Diseño Arquitectónico (Scope Boundaries):]

- Concentración en vectores analizables mediante firmas sintácticas: el orquestador focaliza su capacidad en fallas dinámicas detectables por patrones de inyección y análisis de anomalías en respuestas HTTP \(inyecciones SQL, vectores reflejados de Cross-Site Scripting, inclusión local de archivos, omisión de cabeceras de seguridad y exposición de rutas no enlazadas).

- Exclusión explícita de vulnerabilidades de lógica de negocio \(#emph[Business Logic Flaws]\): aquellas fallas que vulneran los flujos transaccionales legítimos de una aplicación \(como omisión de etapas en pasarelas de pago, manipulación de estados de cuenta o inconsistencias en flujos de compra) escapan al modelo de análisis por firmas del escaneo dinámico y exigen necesariamente modelado funcional y auditoría manual.

- Exclusión de condiciones de carrera \(#emph[Race Conditions]\) y control de acceso horizontal complejo: vectores basados en concurrencia temporal distribuida a nivel de microsegundos o violaciones complejas de control de acceso horizontal entre usuarios con idéntico nivel de privilegios demandan una orquestación semántica de permisos y sincronización que excede el diseño modular del pipeline desarrollado.
