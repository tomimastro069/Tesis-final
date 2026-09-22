= 6. Hipótesis
<hipótesis>
#quote(block: true)[
Se plantean las siguientes hipótesis de investigación:

#strong[H1:] La automatización del proceso de análisis de seguridad
mediante un sistema de orquestación reduce el esfuerzo manual necesario
para detectar vulnerabilidades en aplicaciones web, al eliminar la
necesidad de ejecutar cada herramienta de forma independiente y
consolidar manualmente los resultados.

#strong[H2:] La integración de múltiples herramientas de análisis
\(escaneo activo, fuzzing de directorios e inyección SQL), donde los
hallazgos de una herramienta se utilizan para enriquecer el análisis de
las demás, permite obtener una cobertura de detección mayor que el uso
individual de cada herramienta.

#strong[H3:] La normalización de resultados mediante parsers
especializados facilita la interpretación de los hallazgos y mejora la
utilidad de los reportes generados, al presentar información de fuentes
heterogéneas en una estructura unificada y coherente.

#strong[H4:] Un mecanismo de caché incremental respaldado en base de
datos reduce el tiempo de las ejecuciones repetidas del pipeline sobre
un mismo objetivo, al evitar repetir pruebas ya realizadas sobre
elementos previamente analizados y sin hallazgos.
]
