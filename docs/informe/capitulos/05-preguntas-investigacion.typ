= 5. Preguntas de Investigación
<preguntas-de-investigación>

En concordancia con el paradigma de investigación tecnológica aplicada de
tipo constructivo adoptado \(sección 10.1), las preguntas de investigación
actúan como directrices epistémicas que delimitan los problemas técnicos,
metodológicos y operativos abordados durante la creación y validación del
artefacto de software. Cada interrogante examina una tensión crítica del
ciclo DevSecOps: la fricción temporal en la integración continua, el
aislamiento de las herramientas especializadas, la heterogeneidad de
esquemas de datos, la complejidad de reproducción del entorno y la
transición desde utilitarios de consola hacia plataformas de servicio.

A continuación se presentan las cinco preguntas de investigación que guían el
desarrollo y la evaluación del proyecto, explicitando para cada una su
fundamentación teórica y su articulación metodológica:

+ #strong[\(PI1)] ¿En qué medida un sistema de orquestación desarrollado
  en Python mejora, en términos cualitativos y de tiempo de
  re-ejecución, la coordinación de múltiples herramientas de seguridad
  web frente a su ejecución manual e independiente?
  - #strong[Fundamentación y brecha conceptual:] Aborda la fricción operativa
    y los cuellos de botella generados por la ejecución interactiva,
    secuencial y fragmentada de pruebas de seguridad por parte de auditores
    humanos \(Planteo del Problema, Capítulo 2). Indaga si la coordinación
    desatendida del flujo y la incorporación de mecanismos de caché
    incremental permiten mitigar sustancialmente los tiempos de respuesta sin
    degradar la exhaustividad ni la consistencia de los hallazgos.
  - #strong[Articulación metodológica:] Vinculada operativamente con los
    objetivos específicos OE1 y OE5, y con las hipótesis H1 \(reducción del
    esfuerzo manual) y H4 \(optimización temporal por caché). Su respuesta
    empírica se desarrolla en la sección 15.1, sustentada por las
    mediciones de las Tablas 10 y 11 \(reducción temporal del 68,9% por
    caché) y la contrastación del esfuerzo manual documentada en la sección
    14.2 y la Tabla 13 \(Capítulo 17).

+ #strong[\(PI2)] ¿La integración de herramientas open source en un
  pipeline unificado —donde los hallazgos de una herramienta enriquecen
  el análisis de otra— permite ampliar la cobertura de detección
  respecto al uso individual de cada herramienta?
  - #strong[Fundamentación y brecha conceptual:] Examina el problema de los
    silos de información característico de las herramientas DAST tradicionales,
    las cuales operan de forma estanca y sin retroalimentación contextual.
    Cuestiona si el encadenamiento secuencial con inyección cruzada
    \(_cross-tool feeding_: transferencia de rutas descubiertas por ffuf al
    árbol de ZAP y selección heurística de URLs candidatas hacia SQLMap)
    logra descubrir vectores que permanecen invisibles ante el análisis
    individual y aislado de cada motor.
  - #strong[Articulación metodológica:] Vinculada con los objetivos
    específicos OE1 y OE5, y con la hipótesis H2 \(cobertura multidimensional
    por enriquecimiento cruzado). Su contrastación empírica se documenta en
    la sección 14.1 y en la respuesta de la sección 15.1, respaldada por la
    Tabla 8 y la Tabla 9, donde el pipeline unificado cubrió tres
    categorías del OWASP Top 10 frente a una única categoría por herramienta
    en solitario.

#pagebreak()
#set enum(start: 3)

+ #strong[\(PI3)] ¿Es posible generar un formato unificado de resultados
  a partir de herramientas que producen salidas en formatos
  heterogéneos?
  - #strong[Fundamentación y brecha conceptual:] Responde a la fragmentación
    sintáctica y semántica derivada de coordinar motores de diversa índole
    \(árbol jerárquico XML/JSON de ZAP, flujo continuo en JSON de ffuf y
    registros de texto plano de SQLMap). Indaga la factibilidad de transformar
    dicha diversidad hacia un modelo de datos homogéneo y normalizado, capaz
    de preservar los atributos esenciales de cada vulnerabilidad y posibilitar
    su ingesta automática por herramientas de gestión o interfaces web.
  - #strong[Articulación metodológica:] Vinculada con los objetivos
    específicos OE3 y OE8, y con la hipótesis H3 \(normalización estructurada).
    Se fundamenta en la arquitectura de parsers desacoplados \(sección 12.7)
    y en la consolidación del esquema canónico #emph[resultado_unificado.json]
    \(Anexo D), validada positivamente en la sección 15.1.

+ #strong[\(PI4)] ¿Qué ventajas ofrece una arquitectura modular y
  contenerizada para sistemas de análisis de seguridad automatizados en
  términos de extensibilidad y reproducibilidad?
  - #strong[Fundamentación y brecha conceptual:] Indaga en el dilema de la
    portabilidad y la resolución de dependencias antagónicas propio del
    software de ciberseguridad. Examina en qué medida la adhesión a patrones
    de diseño desacoplados \(SOLID) y la infraestructura inmutable basada en
    contenedores Docker mitigan el riesgo de regresiones y garantizan la
    reproducibilidad exacta del banco de pruebas, permitiendo incorporar
    nuevos módulos de escaneo sin alterar el núcleo del sistema.
  - #strong[Articulación metodológica:] Vinculada con los objetivos
    específicos OE2 y OE4. Su resolución se sustenta en la arquitectura de
    paquetes \(sección 11.2), el despliegue multicontenedor sobre la red
    #emph[sec-net] \(sección 12.1) y la verificación del criterio de
    reproducibilidad \(100% en hallazgos de ZAP y SQLMap, Tabla 11),
    ratificada en la sección 15.1.

+ #strong[\(PI5)] ¿Puede un sistema de este tipo extenderse, sin
  modificar su lógica de escaneo central, hacia un servicio persistente
  con interfaz web y capacidades de seguimiento histórico de
  vulnerabilidades?
  - #strong[Fundamentación y brecha conceptual:] Explora la superación de la
    brecha entre utilitarios de línea de comandos de uso exclusivo para
    especialistas y plataformas centralizadas integrables en la cultura
    DevSecOps. Evalúa si el desacoplamiento arquitectónico del orquestador
    permite añadir asincronía, persistencia relacional híbrida
    \(SQLite/PostgreSQL) y una interfaz de usuario intuitiva sin requerir
    modificaciones sobre el flujo de escaneo subyacente.
  - #strong[Articulación metodológica:] Vinculada con los objetivos
    específicos OE6, OE7 y OE9. Se sustenta en el desarrollo de la Fase 7
    \(sección 10.2), la API REST en FastAPI, la persistencia en base de datos
    y la SPA en React \(sección 12.10, Anexos F y G), corroborada en las
    conclusiones de la sección 15.1.
