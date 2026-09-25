= 15. Conclusiones y Trabajos Futuros
<conclusiones-y-trabajos-futuros>
== 15.1 Conclusiones
<conclusiones>
Primero, el sistema evolucionó de un pipeline secuencial simple a un
servicio completo: una API REST que ejecuta el escaneo en segundo plano,
reporta progreso, persiste resultados e historial, y se integra con n8n
mediante webhooks. Esto confirma que la arquitectura modular original
\(runners, scanners, parsers, workflow) es lo suficientemente flexible
como para sostener una capa de servicio y una interfaz web sin
reescribir la lógica de escaneo.

Segundo, la integración entre herramientas dejó de ser una simple
consolidación posterior y pasó a ser un enriquecimiento activo: las
rutas descubiertas por ffuf se inyectan en ZAP antes del escaneo activo,
ampliando su superficie de ataque real. Esto sostiene H2 de forma más
directa que en la versión original del sistema. Una primera
descomposición de esa mejora, por herramienta, se presenta en la Tabla 9
del capítulo 14: el orquestador combinado cubrió tres categorías del
OWASP Top 10 frente a una sola categoría por herramienta operando en
solitario. Esa descomposición proviene de una única ejecución y no de un
experimento con corridas aisladas y controladas para cada herramienta,
por lo que la cuantificación formal de H2 —con ejecuciones realmente
independientes de cada herramienta— sigue pendiente, tal como se declara
en la Tabla 9 y en 9.2.

Tercero, se implementó un mecanismo de caché incremental
\(SQLite/PostgreSQL) que evita repetir ataques de ffuf y SQLMap contra
objetivos ya analizados, y un sistema de re-testeo automático que sí
vuelve a atacar, en cada corrida, las URLs previamente confirmadas como
vulnerables. H4 cuenta con evidencia propia y medida sobre el pipeline
completo: una ejecución con caché activo tardó 4 min 23 s frente a 14
min 06 s sin caché \(68,9% menos tiempo), con hallazgos prácticamente
estables entre ambas corridas \(Tablas 10 y 11, sección 14.3). La
comparación contra el tiempo de un proceso manual equivalente —H1 en su
formulación original— es un tipo de dato distinto y sigue sin contar con
una medición propia; se retiró del capítulo 14 en lugar de sostenerse
con cifras sin respaldo.

Cuarto, la generación automática de dos reportes —uno técnico y uno
ejecutivo, este último con clasificación automática de riesgo global—
responde a la limitación señalada sobre la comunicación de resultados a
audiencias no técnicas.

Quinto, el desarrollo de un frontend funcional \(dashboard de dominios,
formulario de escaneo, tabla de vulnerabilidades, sugerencias de
mitigación asistidas por IA) transformó el proyecto de una herramienta
de línea de comandos a una plataforma con interfaz web operable por
usuarios no técnicos, cumpliendo el objetivo planteado originalmente
como idea complementaria y hoy documentado en el Anexo G como decisión
de diseño.

Sexto, las dos comparaciones cuantitativas más exigentes que este
trabajo se propuso resolver —cobertura individual frente a combinada, y tiempo del pipeline
automatizado frente a un proceso manual equivalente— fueron abordadas en
el capítulo 14, pero con resultados distintos entre sí: la primera
cuenta con una descomposición basada en datos reales de una ejecución
\(Tabla 9), aunque no en un experimento de corridas aisladas; la segunda
no pudo sostenerse con ningún dato propio verificable y se retiró del
informe en lugar de mantenerse con cifras sin base. Ambas limitaciones
se declaran explícitamente como trabajo pendiente en 15.2, y no como
comparaciones ya resueltas.
#pagebreak()
En relación directa con las preguntas de investigación formuladas en el
capítulo 5, el proyecto arriba a las siguientes conclusiones
específicas:

- #strong[Respuesta a PI1 \(Eficiencia y re-ejecución):] La orquestación
  coordinada permitió ejecutar el pipeline de tres herramientas de
  manera automatizada y desatendida. Con el soporte de la base de datos
  y el mecanismo de caché incremental, el tiempo de re-análisis se
  redujo en un 68,9% \(de 14 min 06 s a 4 min 23 s, Tabla 10),
  confirmando empíricamente la hipótesis H4.

- #strong[Respuesta a PI2 \(Cobertura combinada y retroalimentación):]
  La inyección cruzada de rutas de ffuf hacia ZAP y la priorización de
  parámetros para SQLMap permitieron consolidar 41 alertas sobre 34
  endpoints unificados \(Tabla 9), alcanzando una cobertura de tres
  categorías del OWASP Top 10 que ninguna de las tres herramientas logró
  de forma aislada en el entorno de pruebas, lo que valida la hipótesis
  H2.

- #strong[Respuesta a PI3 \(Normalización de datos heterogéneos):]
  Mediante el desarrollo de parsers especializados e independientes, se
  logró transformar las salidas dispares de ZAP \(JSON jerárquico), ffuf
  \(JSON plano) y SQLMap \(texto plano y volcados de BD) en un único
  esquema estructurado \(resultado\_unificado.json), validando la
  hipótesis H3.

- #strong[Respuesta a PI4 \(Extensibilidad y reproducibilidad):] La
  arquitectura contenerizada mediante Docker Compose garantizó la
  reproducibilidad del laboratorio con un único comando y demostró su
  extensibilidad al permitir incorporar una base de datos PostgreSQL, un
  motor de flujos n8n y un frontend en React sin modificar la lógica
  interna del pipeline de escaneo.

- #strong[Respuesta a PI5 \(Evolución hacia arquitectura de servicio):]
  La implementación de la API REST asíncrona en FastAPI y el mecanismo
  de autenticación automática demostraron la viabilidad de transformar
  un orquestador de línea de comandos en una plataforma persistente,
  capaz de reportar progreso en tiempo real y ser operada por usuarios
  no técnicos.

#pagebreak()
=== 15.1.1 Verificación por objetivo específico
<verificación-por-objetivo-específico>
La siguiente tabla verifica, de forma sintética, el cumplimiento de cada
uno de los nueve objetivos específicos definidos en la sección 4.2.

#strong[Tabla 12. Verificación de cumplimiento por objetivo específico] <tabla-12>

#figure(
  align(center)[#table(
    columns: 4,
    align: (col, row) => (auto, auto, auto, auto).at(col),
    inset: 6pt,
    [OE], [Objetivo], [Estado], [Evidencia],
    [OE1],
    [Integrar ZAP, ffuf y SQLMap en un flujo automatizado con
      enriquecimiento cruzado],
    [Cumplido],
    [Sección 11.4 y Figura 2; Tabla 9 \(cap. 14)],

    [OE2],
    [Arquitectura modular extensible],
    [Cumplido],
    [Sección 12 completa; paquetes runners/scanners/parsers/workflow],

    [OE3], [Parsers especializados que normalicen resultados heterogéneos], [Cumplido], [Sección 12.7],
    [OE4],
    [Despliegue contenerizado y reproducible con Docker],
    [Cumplido],
    [Sección 12.1; docker-compose.yml \(5 servicios)],

    [OE5],
    [Evaluar el sistema contra los criterios de validación de 10.6],
    [Cumplido],
    [Criterios de 10.6 verificados: cap. 13 \(funcionalidad y
      consolidación), Tabla 8 \(cobertura) y Tabla 11 \(reproducibilidad del
      96,3%–100%).],

    [OE6], [Autenticación automática contra secciones protegidas], [Cumplido], [Sección 12.9; Anexo E],
    [OE7], [Exponer el orquestador como API REST asíncrona con historial], [Cumplido], [Sección 12.10; Anexo F],
    [OE8],
    [Generar reportes técnico y ejecutivo con clasificación de riesgo],
    [Cumplido],
    [reporte\_seguridad.md, reporte\_cliente.md],

    [OE9], [Interfaz web para lanzar y consultar escaneos sin línea de comandos], [Cumplido], [Anexo G; frontend React],
  )],
)

#text(size: 10pt)[#emph[Nota. Elaboración propia.]]

== 15.2 Trabajos Futuros
<trabajos-futuros>
Dado que autenticación automática, reportes en Markdown, configuración
centralizada, base de datos de historial, panel web y sugerencias de IA
ya están implementados, el trabajo futuro se concentra en lo que
efectivamente falta:

+ #strong[Comparación cuantitativa individual vs. combinada con corridas
    aisladas reales:] instrumentar el pipeline para ejecutar cada
  herramienta de forma verdaderamente aislada \(sin las demás activas)
  además de en conjunto, y registrar la diferencia de cobertura, para
  validar H2 con evidencia numérica propia de un experimento controlado.

+ #strong[Medición de tiempo manual equivalente:] instrumentar el
  pipeline con timestamps de inicio/fin por etapa y cronometrar una
  sesión real de análisis manual con las mismas herramientas, para
  contrastar H1 contra una línea de base real en lugar de una estimación
  sin sustento.

+ #strong[Seguridad de la API:] actualmente api.py habilita CORS para
  cualquier origen \(allow\_origins\=\[“\*”\]) y no requiere
  autenticación para lanzar o consultar escaneos; se recomienda
  restringir el origen y agregar un mecanismo de autenticación antes de
  exponer la API fuera de un entorno de laboratorio.

+ #strong[Validación de las sugerencias de IA:] contrastar
  sistemáticamente las recomendaciones generadas por el modelo de
  lenguaje contra criterio experto, para medir su tasa de acierto antes
  de recomendarlas como apoyo confiable.

+ #strong[Scoring de riesgo formal:] reemplazar la heurística actual de
  clasificación de riesgo \(ALTO/MEDIO/BAJO) por un criterio estándar
  como CVSS, que permita comparar resultados entre organizaciones.

+ #strong[Evaluación de reproducibilidad longitudinal a gran escala:] si
  bien la estabilidad del núcleo de detección quedó demostrada con un
  96,3%–100% de coincidencia \(Tabla 11), se propone como línea de
  trabajo futuro extender las mediciones de reproducibilidad a lo largo
  de campañas prolongadas de escaneo periódico sobre diversas
  aplicaciones web, evaluando la deriva temporal \(#emph[drift];) de los
  escáneres y la resiliencia del pipeline ante fluctuaciones en la
  latencia de red.

+ #strong[Integración con pipelines de CI/CD] \(GitHub Actions, GitLab
  CI), aprovechando que la API ya soporta ejecución asíncrona con
  callback.

+ #strong[Incorporación de herramientas adicionales:] Nikto, Nuclei o
  Nmap, para ampliar la cobertura del análisis.
