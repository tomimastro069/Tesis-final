= 6. Hipótesis
<hipótesis>

En concordancia con el diseño de investigación tecnológica aplicada y el enfoque cuantitativo adoptado \(sección 10.1), las hipótesis de trabajo postulan relaciones funcionales entre las decisiones arquitectónicas del orquestador y la optimización de los procesos de auditoría web. Cada hipótesis explicita su formulación, sus variables y su criterio de contrastación empírica:

#strong[H1 — Reducción del Esfuerzo Manual mediante Automatización:]
La automatización del proceso de análisis de seguridad web mediante un pipeline de orquestación desacoplado reduce el esfuerzo manual necesario para detectar y correlacionar vulnerabilidades, al sustituir la ejecución interactiva independiente de cada herramienta y la consolidación artesanal de reportes por un flujo desatendido y centralizado.
- #strong[Variables:] _Variable Independiente \(VI\):_ Modalidad de ejecución \(pipeline en Python vs. consola interactiva manual). _Variable Dependiente \(VD\):_ Esfuerzo operativo \(tiempo de intervención y acciones de correlación).
- #strong[Contrastación empírica:] Contrastada en la sección 14.2 y respaldada en el Capítulo 17 \(Tabla 13: 125 min totales = 75 min desatendidos vs. 50 min manuales).

#strong[H2 — Cobertura Multidimensional por Enriquecimiento Cruzado:]
La integración secuencial de múltiples herramientas dinámicas \(fuzzing con ffuf, escaneo activo con OWASP ZAP y explotación con SQLMap), donde los hallazgos de una fase enriquecen dinámicamente la superficie de las subsecuentes, permite alcanzar una cobertura de detección mayor que el uso individual de cada herramienta.
- #strong[Variables:] _VI:_ Flujo integrado con retroalimentación \(_cross-tool feeding_: ffuf $->$ ZAP $->$ SQLMap). _VD:_ Cobertura de detección \(endpoints analizados y categorías OWASP Top 10 identificadas).
- #strong[Contrastación empírica:] Contrastada en la sección 14.1 y ratificada en las Tablas 8 y 9 \(cobertura combinada de 3 categorías OWASP y 34 endpoints unificados frente a coberturas individuales parciales).

#strong[H3 — Normalización Estructurada e Interoperabilidad de Salidas Heterogéneas:]
La incorporación de una capa de parseo desacoplada y especializada por herramienta transforma las salidas sintácticas y semánticas heterogéneas \(XML/JSON de ZAP, streaming de ffuf y texto de SQLMap) en un esquema canónico homogéneo, facilitando la interpretación integral de los hallazgos y su interoperabilidad con servicios web.
- #strong[Variables:] _VI:_ Arquitectura de parsers independientes basados en interfaces modulares. _VD:_ Uniformidad estructural e interpretabilidad \(esquema canónico consumible por API REST y frontend).
- #strong[Contrastación empírica:] Contrastada en la sección 12.7 y corroborada en la respuesta a PI3 \(sección 15.1), respaldada por el esquema canónico `resultado_unificado.json` \(Anexo D).

#strong[H4 — Optimización Temporal Mediante Caché Incremental:]
Un mecanismo de caché incremental respaldado en base de datos relacional reduce significativamente el tiempo de procesamiento en ejecuciones repetidas del pipeline sobre un mismo objetivo, al omitir pruebas redundantes sobre componentes previamente analizados sin hallazgos, preservando intactas la exhaustividad y reproducibilidad.
- #strong[Variables:] _VI:_ Caché incremental persistente con identificación de estado por hash. _VD:_ Tiempo de ejecución en corridas sucesivas y consistencia de hallazgos sobre el mismo objetivo.
- #strong[Contrastación empírica:] Contrastada en la sección 14.3 y en la respuesta a PI1 \(sección 15.1), respaldada por las Tablas 10 y 11 \(reducción del 68,9% del tiempo: de 14m 06s a 4m 23s, con 100% de consistencia en 48 alertas ZAP y 8 inyecciones SQLMap).
