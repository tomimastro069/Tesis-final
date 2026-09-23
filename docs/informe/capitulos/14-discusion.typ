= 14. Discusión
<discusión>
Los resultados obtenidos confirman que es técnicamente viable
implementar un sistema de orquestación de herramientas de seguridad web
utilizando exclusivamente tecnologías open source y un desarrollo propio
en Python. El pipeline automatizado logró detectar vulnerabilidades en
múltiples categorías del OWASP Top 10, y el reporte técnico generado el
5 de agosto de 2026 \(output/reports/reporte\_seguridad.md) constituye
evidencia de una ejecución real contra el entorno DVWA, con hostnames
reales del entorno Docker en lugar de datos de ejemplo.

El sistema evolucionó considerablemente respecto al diseño original de
tres módulos independientes \(ZAP, ffuf, SQLMap) hacia una arquitectura
de servicio: una API REST \(api.py, FastAPI) que ejecuta el pipeline en
segundo plano, expone el progreso del escaneo en tiempo real, persiste
el historial de análisis en base de datos y notifica su finalización
mediante webhooks a un flujo de n8n. Sobre esta API se construyó además
un frontend que consume estos endpoints. Esta extensión responde
directamente a PI4 \(extensibilidad y reproducibilidad): la separación
entre orquestador, API y frontend permitió incorporar estas capas sin
modificar la lógica interna del pipeline.

== 14.1 Contraste de cobertura: uso individual frente a combinado \(H2)
<contraste-de-cobertura-uso-individual-frente-a-combinado-h2>
El pipeline actual no solo integra los hallazgos de las tres
herramientas al final del proceso, sino que los cruza durante la
ejecución: las rutas descubiertas por ffuf se inyectan en la sesión de
ZAP antes de iniciar el escaneo activo, de modo que ZAP ataca tanto las
URLs descubiertas por su propio spider como las descubiertas por ffuf; y
SQLMap solo recibe URLs candidatas porque el spider y ffuf las aportaron
previamente. La Tabla 9 descompone, a partir de esta misma ejecución,
qué detecta cada herramienta por separado frente al resultado del
pipeline combinado.

#pagebreak()

#strong[Tabla 9. Cobertura por herramienta en solitario frente al
  pipeline combinado \(misma ejecución del 5 de agosto de 2026)] <tabla-9>

#figure(
  align(center)[#table(
    columns: 5,
    align: (col, row) => (auto, auto, auto, auto, auto).at(col),
    inset: 6pt,
    [Herramienta / Método],
    [URLs analizadas],
    [Hallazgos],
    [Cobertura
      OWASP Top 10],
    [Limitación de operar en solitario],

    [ZAP \(spider + active scan)],
    [24 \(su propio spider)],
    [37 alertas],
    [A05:2021],
    [No descubre rutas no enlazadas de forma proactiva; no profundiza en
      inyección SQL],

    [ffuf],
    [8 \(wordlist)],
    [0 \(solo identifica códigos HTTP, no clasifica vulnerabilidades)],
    [A01:2021 \(indirecta)],
    [No evalúa el contenido de las respuestas ni ejecuta lógica de
      detección],

    [SQLMap en aislamiento total],
    [0 \(requiere URLs de entrada)],
    [0],
    [—],
    [No tiene capacidad de crawling propia; depende arquitectónicamente de
      que otra herramienta le entregue URLs parametrizadas],

    [Orquestador \(combinado)],
    [34 \(unificadas)],
    [41 \(37 ZAP + 4 SQLMap)],
    [A01, A03, A05 \(tres categorías)],
    [Pipeline secuencial; no se ejecutó, además de esta corrida, una
      segunda ejecución de control con las herramientas verdaderamente
      aisladas entre sí],
  )],
)

#text(size: 10pt)[#emph[Nota. Elaboración propia a partir de resultado\_unificado.json.
  Las filas «ZAP» y «ffuf» reflejan lo que cada herramienta aporta dentro
  de la corrida combinada, no una ejecución separada de cada una contra el
  objetivo; SQLMap en aislamiento total es una limitación arquitectónica
  documentada, no medida por separado.]]

#strong[Nota metodológica.] Esta tabla no proviene de tres ejecuciones
independientes y controladas de cada herramienta contra DVWA, sino de la
descomposición de una única corrida combinada. Falta aún una comparación
cuantitativa formal, con ejecuciones aisladas reales, entre la cobertura
individual y la combinada; esta limitación se declara explícitamente en
las conclusiones del capítulo 15 y como línea de trabajo futuro en 15.2,
en lugar de darse por resuelta.

Bajo este esquema, ZAP en solitario no descubre por sí mismo las rutas
administrativas que ffuf sí encuentra \(por ejemplo, /setup.php o
/security.php), y SQLMap no puede operar sin que otra herramienta le
aporte URLs parametrizadas. La orquestación combinada amplía por
construcción la superficie cubierta: no es solo que se sumen los
hallazgos de cada herramienta, sino que los hallazgos de una habilitan
el trabajo de la siguiente.

== 14.2 Reducción de esfuerzo manual \(H1)
<reducción-de-esfuerzo-manual-h1>
El sistema incorpora un mecanismo de caché incremental respaldado en
SQLite/PostgreSQL \(app/db/database.py) que registra qué palabras de
wordlist y qué URLs con parámetros ya fueron analizadas contra un
objetivo determinado. Según la documentación de optimización del
proyecto \(OPTIMIZACION\_ZAP.md) y las pruebas de test\_speed.py, una
segunda ejecución de ffuf sobre un mismo objetivo sin palabras nuevas se
resuelve en milisegundos, y SQLMap omite en menos de un segundo las URLs
ya analizadas sin hallazgos. La sección 14.3 amplía esta evidencia con
una medición del pipeline completo \(no solo de ffuf en aislamiento):
esa medición cuantifica el efecto del caché sobre el propio sistema
automatizado, pero —al igual que test\_speed.py— no constituye una
comparación contra un proceso manual, que es específicamente lo que
exige H1 en su formulación original.

Con el fin de contrastar la hipótesis H1 —que postula la disminución de
la labor técnica artesanal en la identificación de fallas de seguridad—,
la investigación dispone del ensayo experimental registrado y
estructurado en el capítulo 17 \(véase Tabla 13). La referida sesión
registró una carga temporal acumulada de 125 minutos, dentro de la cual
el 60% del período \(75 minutos) fue ejecutado por procesos automáticos
de escaneo y recolección de datos, restringiendo la intervención humana
a 50 minutos \(40%) enfocados únicamente en la validación de cinco
vectores críticos.

A pesar de que este registro no representa una prueba a ciegas de
exploración manual independiente sobre toda la superficie —limitación
expresamente declarada en la sección 9.2—, las métricas presentadas en
el capítulo 17 aportan respaldo empírico a H1: efectuar de forma
artesanal el mapeo de 34 endpoints, el fuzzing de más de 200.000
palabras y la evaluación de entradas insumiría numerosas horas de labor
especializada \(SANS Institute, 2024). En contraposición, el pipeline
automatizado efectúa la fase integral de reconocimiento y ataque en un
intervalo de entre 4 y 14 minutos \(Tabla 10), circunscribiendo la tarea
del auditor a una revisión final de hallazgos y sustituyendo múltiples
ejecuciones desarticuladas por un único comando desatendido.

Los datos, tablas y el detalle completo de esta sesión de validación
manual se desarrollan en el capítulo 17 \(Desarrollo experimental y
validación de hallazgos).

== 14.3 Verificación de H4: impacto del caché incremental
<verificación-de-h4-impacto-del-caché-incremental>
A diferencia de H1, la hipótesis H4 —que el caché incremental reduce el
tiempo de ejecuciones repetidas del pipeline sobre un mismo objetivo— sí
cuenta con una medición propia del pipeline completo \(ZAP + ffuf +
SQLMap), obtenida ejecutando dos corridas consecutivas contra DVWA: una
con el caché deshabilitado \(análisis completo desde cero) y otra con el
caché incremental activo. Ambas corridas se realizaron el 6 de agosto de
2026, entre las 09:14 y las 09:41 \(hora local del entorno), y son
verificables contra los archivos resultado\_sin\_cache.json y
resultado\_con\_cache.json del directorio output/raw/benchmarks/ del
repositorio del proyecto.

#strong[Tabla 10. Tiempo total del pipeline con y sin caché incremental] <tabla-10>

#figure(
  align(center)[#table(
    columns: 3,
    align: (col, row) => (auto, auto, auto).at(col),
    inset: 6pt,
    [Condición], [Tiempo total del pipeline], [Reducción],
    [Sin caché \(análisis completo desde cero)], [14 min 05,81 s \(845,81 s)], [—],
    [Con caché incremental activo], [4 min 23,15 s \(263,15 s)], [68,9% menos tiempo],
  )],
)

#text(size: 10pt)[#emph[Nota. Medición propia sobre una ejecución real del pipeline
  completo contra DVWA, reportada por los autores, corridas del 6 de
  agosto de 2026 \(ver referencia de archivos arriba). El panel de caché
  de la corrida con caché activo registró: ffuf 0 de 207.628 palabras
  probadas \(207.628 omitidas por caché); SQLMap 3 de 8 URLs re-testeadas
  \(5 omitidas por caché, 3 re-testeadas por haber sido vulnerables en una
  corrida anterior); ZAP no participa del mecanismo de caché y ejecuta
  spider y escaneo activo completos en ambas corridas.]]

Esta es, a diferencia de la comparación retirada de H1, una medición
real de tiempo del pipeline end-to-end, con la salvedad de que compara
dos configuraciones del propio sistema automatizado \(con y sin caché) y
no al sistema automatizado contra un proceso manual —que sigue siendo la
comparación pendiente en H1.

La misma comparación aporta además evidencia relevante para el criterio
de reproducibilidad de la sección 10.6. Los hallazgos de ambas corridas
resultaron prácticamente estables: 48 alertas de ZAP en ambos casos, 0
rutas de ffuf en ambos casos \(la wordlist utilizada en esta prueba
puntual no coincidió con rutas reales de DVWA) y 8 vulnerabilidades de
SQLMap en ambos casos; la única variación se dio en el conteo del spider
de ZAP —que no participa del caché y por lo tanto no debería verse
afectado por él— con 54 URLs sin caché frente a 52 con caché, una
diferencia de apenas dos URLs \(96,3% de coincidencia) atribuible a la
variabilidad propia del rastreo dinámico ya señalada en 10.5, no a un
efecto del caché.

Sobre las 8 vulnerabilidades de SQLMap reportadas en ambas corridas de
este benchmark, frente a las 4 de la corrida de referencia del capítulo
13: la diferencia es consistente con lo señalado en la sección 13.4.
Ambas corridas de este benchmark confirmaron inyección tanto en
/vulnerabilities/brute/ \(username) como en /vulnerabilities/sqli/
\(id), de forma coincidente con la corrida del 2 de agosto documentada
en 13.4, mientras que la corrida de referencia del 5 de agosto del
capítulo 13 solo confirmó el primer endpoint. Este tercer punto de datos
refuerza la lectura de que la no detección de /vulnerabilities/sqli/ en la
corrida del capítulo 13 fue un evento puntual de esa pasada —probablemente
ligado al conjunto de URLs parametrizadas que el spider y ffuf le
entregaron a SQLMap en ese momento— y no un cambio estructural del
comportamiento del sistema.

#strong[Tabla 11. Estabilidad de hallazgos entre la corrida sin caché y
  con caché] <tabla-11>

#figure(
  align(center)[#table(
    columns: 4,
    align: (col, row) => (auto, auto, auto, auto).at(col),
    inset: 6pt,
    [Indicador], [Sin caché], [Con caché], [Coincidencia],
    [Total de URLs únicas], [59], [57], [96,6%],
    [URLs descubiertas por el Spider], [54], [52], [96,3%],
    [Alertas de ZAP], [48], [48], [100%],
    [Rutas descubiertas por ffuf], [0], [0], [100%],
    [Vulnerabilidades de SQLMap], [8], [8], [100%],
  )],
)

#text(size: 10pt)[#emph[Nota. Medición propia reportada por los autores. Los campos se
  interpretan según la estructura del bloque «resumen» de
  resultado\_unificado.json, consistente con las Tablas 3 a 8. Al igual
  que en la Tabla 3, el total de URLs únicas de cada corrida \(59 y 57)
  excede la suma de spider y ffuf \(54+0 y 52+0): la diferencia de 5 URLs
  en cada caso corresponde a la URL semilla y a las URLs derivadas del
  proceso de autenticación y de re-testeo automático de los dos endpoints
  marcados como vulnerables \(/vulnerabilities/brute/ y
  /vulnerabilities/sqli/), incorporadas al conjunto unificado de la misma
  forma señalada en la nota de la Tabla 3.]]

Estos resultados proveen respaldo empírico directo para corroborar la
hipótesis H4 y el parámetro de reproducibilidad detallado en el apartado
10.6. En lugar de restar validez a los ensayos, la constancia absoluta
en la identificación de fallas \(48 alertas reportadas por ZAP y 8
inyecciones confirmadas mediante SQLMap) al modificar la configuración
de la caché ratifica la solidez del flujo de trabajo: el esquema de
optimización temporal disminuye la duración del análisis en un 68,9%
preservando intactas la exhaustividad del escaneo y la precisión de los
descubrimientos.

== 14.4 Rendimiento y ajuste de timeouts
<rendimiento-y-ajuste-de-timeouts>
El rendimiento del pipeline fue un problema identificado y resuelto
durante el desarrollo. Por defecto, el Active Scan de ZAP podía superar
las 4 horas por objetivo debido a su configuración conservadora \(2
hilos concurrentes, sin límite de tiempo por regla ni por escaneo,
verificación de tokens anti-CSRF). Esto se corrigió aumentando a 20
hilos concurrentes, fijando un límite de 1 minuto por regla y un techo
de 10 minutos para el escaneo activo completo, y desactivando la
verificación de tokens CSRF. De forma análoga, SQLMap se configuró con
--threads\=10 y la bandera --smart, que descarta parámetros no
inyectables en segundos en lugar de forzarlos. El pipeline sigue siendo
secuencial por diseño —ffuf debe completarse antes del escaneo activo de
ZAP para poder inyectarle las rutas descubiertas, y SQLMap necesita las
URLs combinadas de spider y ffuf además de una sesión recién
refrescada—, pero el cuello de botella real \(la duración del escaneo de
ZAP) fue acotado explícitamente en lugar de dejarse sin control.

== 14.5 Seguimiento longitudinal y sugerencias de mitigación por IA
<seguimiento-longitudinal-y-sugerencias-de-mitigación-por-ia>
El sistema de re-testeo automático de URLs vulnerables agrega una
dimensión no contemplada en las hipótesis originales: las URLs donde se
confirmó una vulnerabilidad se excluyen deliberadamente del caché y se
vuelven a atacar en cada ejecución, registrando primera\_vez y
última\_vez de detección. Esto permite usar el sistema como herramienta
de seguimiento longitudinal —si un equipo de desarrollo corrige una
falla, el campo última\_vez deja de actualizarse—, una capacidad más
cercana a una plataforma de gestión de vulnerabilidades que a un escáner
de una sola pasada.

La incorporación de un componente de sugerencias de mitigación asistidas
por IA \(expuesto en el frontend mediante useAiAnalysis, que consulta un
endpoint de n8n) constituye una extensión funcional relevante, pero debe
presentarse con cautela: las sugerencias generadas por el modelo no
fueron validadas sistemáticamente contra un criterio experto, por lo que
se recomiendan como apoyo complementario y no como fuente única de
remediación.

== 14.6 Comparación con el panorama de la industria
<comparación-con-el-panorama-de-la-industria>
Al contrastar el sistema propuesto con el panorama actual de la
industria \(ver también Tabla 1), se identifican paralelismos y
divergencias operativas:

- #strong[Plataformas de Gestión de Vulnerabilidades \(Faraday,
    DefectDojo):] se especializan en la centralización y el triaje de
  hallazgos heterogéneos, permitiendo una visión estática del riesgo,
  pero carecen de mecanismos para coordinar activamente la ejecución
  secuencial en tiempo real o facilitar el enriquecimiento dinámico de
  datos entre escáneres. El orquestador desarrollado automatiza
  íntegramente el flujo del pipeline, algo que estas plataformas no
  hacen por sí mismas.

- #strong[Plataformas SOAR \(Shuffle, TheHive):] representan ecosistemas
  de respuesta ante incidentes de alta robustez, pero cuya
  implementación exige una infraestructura compleja y costos de
  licenciamiento elevados en sus variantes comerciales. El sistema aquí
  presentado se distingue por su arquitectura ligera, orientada
  específicamente al escaneo web interactivo y la portabilidad mediante
  Docker Compose.

Contraste de hallazgos con el estado del arte: Aunque la fase
experimental se acotó a un laboratorio controlado utilizando DVWA como
objetivo, las métricas recolectadas respaldan de manera directa las
observaciones reportadas en la literatura reciente de ciberseguridad
ofensiva:

1. #strong[Sinergia y complementariedad de scanners \(Qadir et al.,
    2025):] Al evaluar múltiples herramientas de DAST sobre docenas de
  objetivos web, se observa que ningún motor aislado logra abarcar por
  completo la totalidad del OWASP Top 10. Esta premisa se comprueba en la
  Tabla 9, donde el pipeline unificado expandió la detección desde una
  sola categoría \(A05 en ZAP) hasta tres categorías críticas \(A01, A03 y
  A05).

2. #strong[Ampliación de la superficie de ataque mediante fuzzing
    \(Alsaedi et al., 2021):] El descubrimiento de ocho rutas no
  identificadas por el rastreo de ZAP —incluyendo endpoints de
  administración clave como /setup.php y /security.php— confirma
  empíricamente que el fuzzing de directorios resulta indispensable para
  complementar el escaneo activo.

3. #strong[Especialización en la detección de inyecciones \(Althunayyan
    et al., 2022; Elia et al., 2010):] La confirmación de vectores SQL
  mediante técnicas avanzadas por parte de SQLMap en secciones no
  catalogadas como vulnerables por ZAP demuestra la disparidad entre
  escáneres generales y módulos dedicados, fundamentando la inclusión de
  este componente en la arquitectura.

Como línea de trabajo futuro \(sección 15.2), se plantea la evaluación
comparativa de esta plataforma frente a soluciones comerciales en
entornos vulnerables adicionales \(como WebGoat o OWASP Juice Shop),
analizando la tasa de falsos positivos y el impacto en la red.
