= 2. Planteo del Problema
<planteo-del-problema>

Pese a la amplia oferta de utilidades especializadas destinadas al diagnóstico
de seguridad en plataformas web, la mayoría de las organizaciones tropieza con
severas trabas operativas al momento de establecer un esquema de evaluación
sistemático, continuo y reproducible. Los vectores de ataque dirigidos contra
aplicaciones web representaron el 12% del total de incidentes de seguridad
confirmados durante 2025, de los cuales el 88% estuvo vinculado al compromiso de
credenciales \(Verizon, 2025). Sumado a ello, el costo financiero global de una
brecha de datos promedia los 4,44 millones de dólares \(IBM, 2025), lo que torna
crítico abordar esta problemática desde una perspectiva metodológica e ingenieril
sustentada en métricas empíricas.

== 2.1 Contextualización: La Fricción entre DAST Tradicional y la Agilidad de CI/CD
<contextualización-fricción-dast>

En el paradigma contemporáneo de ingeniería de software, caracterizado por la
adopción generalizada de metodologías ágiles y canalizaciones de integración y
despliegue continuos \(CI/CD), la frecuencia de publicación de nuevas versiones
ha pasado de ciclos mensuales o trimestrales a cadencias diarias o semanales. No
obstante, las evaluaciones de seguridad dinámicas \(DAST) tradicionales fueron
concebidas originalmente para auditorías puntuales, periódicas y de ejecución
manual al final del ciclo de vida \(Qadir et al., 2025).

Esta divergencia genera un desacople estructural: mientras el equipo de
desarrollo demanda respuestas en cuestión de minutos para validar un despliegue,
un análisis de seguridad dinámico exhaustivo que opere de manera aislada insume
múltiples horas de configuración y ejecución. Como resultado, las auditorías
dinámicas son omitidas o relegadas a fases tardías, incrementando el riesgo de
promover vulnerabilidades críticas a entornos de producción \(SANS Institute, 2024).

== 2.2 Desarticulación Operativa y Silos de Información
<desarticulación-silos-información>

El panorama operativo de las herramientas de código abierto disponibles se
encuentra fragmentado. Cada analizador resuelve con alta eficacia un vector
específico —el descubrimiento de rutas ocultas mediante fuzzing, el análisis
heurístico de vulnerabilidades web o la confirmación de inyecciones en bases de
datos—, pero lo hace de forma completamente desacoplada y estanca \(Abdulghaffar et
al., 2023).

Esta desarticulación se manifiesta principalmente en tres niveles:

1. *Incompatibilidad en los Modelos de Datos de Salida:* OWASP ZAP genera alertas
   en esquemas XML jerárquicos o JSON complejos con anidamientos profundos; ffuf
   produce un flujo de objetos JSON línea a línea con métricas de palabras y
   códigos de estado HTTP; mientras que SQLMap emite volcados interactivos por
   consola en texto plano y registros de sesión no normalizados. La ausencia de un
   modelo canónico impide la agregación directa de resultados.
2. *Carencia de Enriquecimiento Dinámico entre Fases:* Los descubrimientos de
   superficie expuesta realizados por un fuzzer no son comunicados automáticamente
   al escáner dinámico para guiar su rastreo activo, ni las alertas de parámetros
   sospechosos son transferidas al motor de explotación especializada para
   verificar su impacto real.
3. *Ausencia de Memoria Operativa:* Las ejecuciones tradicionales carecen de
   mecanismos de persistencia que almacenen el estado de corridas previas. Cada
   nueva auditoría evalúa desde cero todos los endpoints, consumiendo ancho de
   banda y tiempo de procesamiento de forma redundante sobre componentes que no
   han sufrido modificaciones en su código fuente.

#pagebreak()
== 2.3 Taxonomía Estructurada de Problemas Identificados
<taxonomía-problemas-identificados>

A partir del análisis operativo y de la literatura especializada en automatización
de seguridad \(Kinyua & Awuah, 2021; Zhang et al., 2023), se identifican seis
problemas críticos que obstaculizan la efectividad de las pruebas DAST en entornos
productivos:

1. *Silos de información e ineficiencia en la correlación cruzada:* Las
   herramientas operan en entornos estancos y producen reportes disímiles,
   imposibilitando la correlación automatizada de vectores e impidiendo que los
   hallazgos de superficie alimenten dinámicamente el análisis activo.
2. *Sobrecarga operativa por tareas manuales repetitivas:* Los profesionales de
   seguridad deben intervenir manualmente para lanzar cada utilidad de forma
   secuencial, configurar credenciales de sesión en consolas heterogéneas y
   consolidar los resultados artesanalmente, consumiendo tiempo valioso en labores
   administrativas de bajo impacto técnico.
3. *Fricción temporal e incompatibilidad con la cadencia de CI/CD:* La ejecución
   secuencial no coordinada demanda lapsos incompatibles con los despliegues
   ágiles. La ausencia de mecanismos de caché incremental agrava este escenario,
   forzando escaneos completos redundantes ante cambios mínimos.
4. *Deficiencias en la reproducibilidad del entorno de ejecución:* La variabilidad
   en las dependencias del sistema operativo, las versiones de los intérpretes y
   las configuraciones locales dificulta contrastar resultados obtenidos en
   distintos momentos, obstaculizando la validación fiable de los procesos de
   remediación.
5. *Brecha en la comunicación ejecutiva y dispersión de métricas:* Los reportes
   nativos de cada herramienta priorizan detalles técnicos atomizados sin
   proporcionar resúmenes consolidados de nivel directivo ni clasificaciones de
   severidad global que faciliten la toma de decisiones basada en riesgo.
6. *Fatiga de alertas y saturación cognitiva del equipo auditor:* La dispersión
   de logs no normalizados genera un volumen masivo de avisos secundarios y
   posibles falsos positivos, elevando la probabilidad de que vulnerabilidades de
   severidad crítica pasen inadvertidas por sobrecarga informativa \(Zhang et al., 2023).

== 2.4 Brecha Operativa a Resolver por el Orquestador
<brecha-operativa-orquestador>

Las plataformas comerciales de orquestación y gestión de vulnerabilidades que
abordan estos problemas suelen exigir despliegues de infraestructura pesados,
configuraciones complejas y modelos de suscripción de elevado costo financiero
\(DefectDojo, 2025; Faraday Security, 2025), lo que las torna inaccesibles para
organizaciones medianas o proyectos con recursos acotados.

Surge así una brecha operacional concreta: la necesidad de una solución de
software liviana, estructurada bajo estándares abiertos y desplegable en
contenedores aislados, que automatice la coordinación secuencial de herramientas
DAST complementarias. Dicho sistema debe normalizar los hallazgos en un esquema
unificado, habilitar el enriquecimiento cruzado entre etapas, optimizar las ventanas
de ejecución mediante persistencia y caché incremental, y ofrecer visibilidad tanto
técnica como ejecutiva, sentando las bases para los objetivos formulados en el
Capítulo 4.

