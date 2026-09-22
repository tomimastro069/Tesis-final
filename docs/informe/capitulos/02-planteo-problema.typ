= 2. Planteo del Problema
<planteo-del-problema>
Pese a la amplia oferta de utilidades destinadas al diagnóstico de
seguridad en plataformas web, la mayoría de las entidades tropieza con
serias trabas operativas al momento de establecer un monitoreo
sistemático y continuo. Como se argumentó previamente, los ataques
directos contra vectores web representaron el 12% de los incidentes de
seguridad registrados durante 2025 \(Verizon, 2025), lo que evidencia la
urgencia de abordar este problema mediante métricas y datos
verificables.

Dentro del paradigma contemporáneo de desarrollo de software,
caracterizado por metodologías ágiles e integración continua \(CI/CD),
la evaluación de riesgos suele quedar desplazada. Esto obedece a que los
escáneres dinámicos \(DAST) tradicionales fueron concebidos para
ejecutarse de forma aislada, desarticulada y manual. Cada herramienta
genera salidas heterogéneas y demanda parámetros independientes,
originando complejas limitaciones metodológicas y arquitectónicas:

1. #strong[Silos de información e ineficiencia de integración:] Los
componentes operan en entornos estancos y producen reportes disímiles
\(estructuras JSON incompatibles, salidas en texto plano o esquemas
XML). Esta dispersión imposibilita la correlación automatizada e impide
que los descubrimientos de superficie obtenidos por un fuzzer alimenten
dinámicamente el análisis activo de otros escáneres.

2. #strong[Carga operativa por tareas repetitivas:] Los auditores deben
iniciar manualmente cada utilidad de manera secuencial, monitorear su
progreso de forma independiente y consolidar los hallazgos
artesanalmente, insumiendo valiosas horas de trabajo especializado en
labores administrativas de bajo impacto.

3. #strong[Extensión de los tiempos de análisis y fricción con CI/CD:]
La ejecución sin coordinación de múltiples herramientas insume ventanas
temporales incompatibles con la frecuencia de los despliegues modernos,
escenario agravado por la carencia de mecanismos de caché que eviten
evaluar reiteradamente endpoints sin cambios.

4. #strong[Deficiencias en la reproducibilidad del entorno:] La
inconsistencia en las versiones, variables y configuraciones de
ejecución dificulta contrastar los resultados de diferentes corridas,
obstaculizando la verificación efectiva del proceso de remediación de
hallazgos.

5. #strong[Brecha en la comunicación ejecutiva del riesgo:] Los reportes
nativos se enfocan exclusivamente en detalles técnicos complejos,
omitiendo síntesis de nivel directivo con clasificaciones globales de
riesgo que orienten la toma de decisiones estratégicas.

6. #strong[Fatiga de alertas y saturación cognitiva:] La acumulación de
logs desarticulados obliga a revisar extensos registros heterogéneos,
incrementando la probabilidad de omitir vulnerabilidades críticas
desestimadas entre un alto volumen de advertencias secundarias \(Zhang
et al., 2023).

Por lo tanto, se vuelve indispensable diseñar una solución de software
que automatice la coordinación de herramientas de auditoría web,
normalizando sus métricas bajo un esquema homogéneo. Dicho sistema debe
constituir un orquestador liviano que impulse el enriquecimiento cruzado
entre componentes, reduzca los tiempos de ejecución mediante
persistencia incremental y elabore informes consolidados —técnicos y
ejecutivos— evitando la complejidad estructural y los elevados costos de
suscripción de las soluciones comerciales.
