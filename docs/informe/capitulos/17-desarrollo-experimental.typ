= 17. Desarrollo Experimental y Validación de Hallazgos
<desarrollo-experimental-y-validación-de-hallazgos>
#emph[#strong[Nota de trazabilidad del capítulo.] Esta sección documenta
una sesión de auditoría manual sobre DVWA en su nivel de seguridad bajo
\(Low), realizada el 4 de agosto de 2026 mediante exploración e
interacción directa con el navegador, y por lo tanto distinta de la
corrida automatizada y documentada del 5 de agosto de 2026 que se
reporta en el capítulo 13 \(nivel de seguridad medium, sin intervención
manual). Al tratarse de un alcance más amplio —incluye rutas y vectores
confirmados manualmente en el navegador, no solo los reportados por las
herramientas automatizadas— los hallazgos de severidad alta descritos
aquí \(ejecución remota de comandos, XSS reflejado e inclusión local de
archivos) corresponden a esta sesión manual y no a la corrida
documentada en la Tabla 4 y en la sección 13.2; de igual modo, la ruta
/config/config.inc.php mencionada en el punto 17.2.1 fue localizada por
inspección manual del navegador durante esta sesión y no por ffuf, por
lo que no figura entre las ocho rutas de la Tabla 5. Los tiempos
registrados en este capítulo miden esta sesión de validación manual de
hallazgos —no un proceso de descubrimiento independiente ni la medición
cronometrada de un proceso manual equivalente al pipeline automatizado
que exige H1 \(véase la aclaración en 14.2)—. Cabe aclarar además que
esta sesión del 4 de agosto de 2026 se ejecutó con la configuración de
herramientas previa al ajuste de rendimiento y timeouts descripto en la
sección 14.4 \(ZAP con 2 hilos concurrentes y sin límite de tiempo por
regla ni por escaneo); por eso el Active Scan de esta sesión insumió 40
minutos, cifra que no es comparable con el techo de 10 minutos ni con
los 14 minutos del pipeline completo medidos en la Tabla 10 bajo la
configuración ya optimizada.]

== 17.1 Cronograma y Distribución Temporal del Proceso de Auditoría
<cronograma-y-distribución-temporal-del-proceso-de-auditoría>
La evaluación de seguridad realizada sobre la plataforma #emph[Damn
Vulnerable Web Application] \(DVWA) en su nivel de seguridad bajo
\(#emph[Low];) se estructuró a través de un enfoque mixto que combinó el
análisis dinámico automatizado con la posterior validación artesanal.
Este proceso experimental demandó un tiempo acumulado de #strong[125
minutos \(poco más de 2 horas)];.

La eficiencia temporal observada se atribuye de manera directa a la
ausencia de mecanismos defensivos en la aplicación bajo prueba, tales
como sistemas de prevención de intrusos \(IPS), cortafuegos de
aplicaciones web \(WAF) o directivas de limitación de tasa \(#emph[Rate
Limiting];). Lo anterior permitió que las herramientas de escaneo
operaran bajo parámetros nominales ideales, optimizando los tiempos de
respuesta del servidor local.

== 17.2 Procedimientos de Descubrimiento y Validación Manual por Vector de Ataque
<procedimientos-de-descubrimiento-y-validación-manual-por-vector-de-ataque>
=== 17.2.1 Fase de Reconocimiento y Mapeo de Superficie \(ZAP Spider y ffuf)
<fase-de-reconocimiento-y-mapeo-de-superficie-zap-spider-y-ffuf>
La fase preliminar de identificación y relevamiento de superficie
demandó un tiempo acumulado de #strong[30 minutos];, distribuidos entre
el análisis manual de sesión, el rastreo pasivo y el #emph[fuzzing] de
rutas. Inicialmente, se emplearon #strong[10 minutos] en una inspección
artesanal a través de las herramientas de desarrollo \(#emph[DevTools];)
del navegador, con el fin de auditar las cookies y los identificadores
de sesión requeridos para la validación de identidad inicial.

Posteriormente, el reconocimiento mediante procesos automatizados
insumió #strong[15 minutos];: el componente #emph[OWASP ZAP Spider]
destinó #strong[5 minutos] a la indexación de hipervínculos y a la
reconstrucción del árbol del sitio, mientras que la utilidad #emph[ffuf]
realizó una búsqueda basada en diccionarios durante #strong[10 minutos];,
logrando localizar endpoints que devolvieron códigos de estado 200 y
302.

Finalmente, la validación y el triaje de los hallazgos del #emph[fuzzer]
requirieron #strong[5 minutos] adicionales de exploración directa. El
auditor verificó la consistencia de las rutas reportadas \(Tabla 5) y
detectó, mediante navegación proactiva, recursos críticos como
/config/config.inc.php, lo que permitió confirmar la exposición de
parámetros de configuración y la accesibilidad de archivos internos del
servidor.

=== 17.2.2 Inyección de Comandos del Sistema Operativo \(ZAP Active Scan)
<inyección-de-comandos-del-sistema-operativo-zap-active-scan>
El módulo de escaneo dinámico #emph[ZAP Active Scan] dedicó una fracción
de sus #strong[40 minutos] de ejecución total a interactuar con los
parámetros del formulario de diagnóstico de red de la aplicación. El
motor automatizado determinó de manera rápida que las entradas de dicho
módulo se concatenaban de forma directa a funciones de ejecución del
sistema operativo anfitrión.

Para la validación manual de este hallazgo, la cual se extendió por
#strong[10 minutos];, se prescindió del uso de herramientas
automatizadas y se procedió a interactuar directamente con la interfaz
gráfica del módulo #emph[Command Injection];. En el campo de texto
diseñado para recibir una dirección IP, se inyectó una dirección
sintácticamente válida seguida de operadores lógicos de concatenación
propios de entornos UNIX/Linux y Windows, estructurando el payload:
127.0.0.1; whoami; id; uname -a.

Al presionar el botón de envío \(#emph[Submit];), el servidor web
procesó exitosamente el comando arbitrario y devolvió en texto plano la
identidad del usuario del sistema \(identificado como www-data), junto
con las especificaciones del kernel del sistema operativo. Esto
corroboró de manera inequívoca la existencia de una vulnerabilidad de
ejecución remota de comandos de criticidad alta.

=== 17.2.3 Vulnerabilidad de Inyección SQL \(sqlmap)
<vulnerabilidad-de-inyección-sql-sqlmap>
La identificación y explotación inicial del parámetro vulnerable a
Inyección SQL fue delegada a la herramienta #emph[sqlmap];, cuyo
análisis automatizado consumió un tiempo de #strong[20 minutos];. Debido
al nulo filtrado de caracteres especiales implementado en el backend, la
herramienta dedujo el motor de base de datos relacional y las técnicas
de explotación viables en un lapso inferior a los dos minutos iniciales,
dedicando el tiempo restante al volcado \(#emph[dump];) automatizado de
las tablas de usuarios y credenciales.

La replicación y comprobación manual de este vector de ataque tomó un
tiempo estimado de #strong[10 minutos];. En primera instancia, se
introdujo un carácter de comilla simple \(\') en el parámetro de
consulta id, con el fin de alterar intencionalmente la sintaxis de la
sentencia SQL original del backend. La visualización de un mensaje de
error nativo emitido por el manejador de base de datos confirmó la falta
de sanitización de la entrada.

En segunda instancia, se procedió a estructurar manualmente un ataque
basado en operadores de unión a través del payload: 1\' UNION SELECT
null, user\() \#. Al enviar dicha petición HTTP, la aplicación web
procesó la unión de tablas espuria y renderizó en la interfaz del
navegador el usuario administrativo actual del sistema gestor de bases
de datos \(root\@localhost). De este modo se validó el hallazgo de
#emph[sqlmap] y se demostró la viabilidad de una extracción de datos no
autorizada.

=== 17.2.4 Cross-Site Scripting Reflejado \(ZAP Active Scan)
<cross-site-scripting-reflejado-zap-active-scan>
Durante el análisis dinámico de #emph[OWASP ZAP];, el escáner identificó
múltiples parámetros susceptibles a la inyección de código de cliente.
El motor inyectó firmas genéricas en los campos de entrada de texto y
detectó que los caracteres especiales eran devueltos directamente en el
cuerpo de la respuesta HTTP sin codificación previa.

El proceso de verificación manual de este hallazgo demandó un tiempo de
#strong[5 minutos];. El auditor accedió al formulario de la sección
#emph[XSS \(Reflected)] e introdujo un fragmento de código estructurado
en lenguaje JavaScript:
\<script\>alert\(\'Vulnerable\_XSS\')\</script\>. Al procesarse la
solicitud, el navegador web del cliente interpretó la cadena de texto no
como un dato plano, sino como una instrucción ejecutable, disparando de
forma inmediata una ventana emergente \(#emph[pop-up];) en el entorno
local. Este comportamiento validó el hallazgo y evidenció el riesgo
latente de secuestro de sesiones o redirecciones maliciosas.

=== 17.2.5 Inclusión Local de Archivos \(ZAP Active Scan)
<inclusión-local-de-archivos-zap-active-scan>
Finalmente, las pruebas de seguridad dinámicas alertaron sobre una
anomalía en el manejo de variables del sistema en el módulo de
navegación de páginas, sugiriendo una vulnerabilidad de Inclusión de
Archivos \(#emph[File Inclusion];).

La fase de validación manual tomó un tiempo aproximado de #strong[10
minutos] y se centró en la manipulación directa de los parámetros
contenidos en la URL mediante el navegador web. Al observar que la
variable page apuntaba de forma explícita a un archivo con extensión
interna \(ej. page\=include.php), el auditor alteró manualmente el
parámetro empleando secuencias de escape y saltos de directorio de la
forma: ?page\=../../../../../../etc/passwd.

Tras efectuar la petición modificada, el servidor web interpretó los
caracteres de retroceso y cargó en la pantalla del usuario el archivo de
configuración interna /etc/passwd. La lectura en texto plano de las
cuentas de usuarios del sistema operativo subyacente sirvió como
evidencia empírica irrefutable para validar de forma manual la
existencia de un fallo crítico de Inclusión Local de Archivos \(LFI).

== 17.3 Conclusiones sobre la Metodología de Validación
<conclusiones-sobre-la-metodología-de-validación>
Como cierre metodológico, es posible determinar que el uso de
herramientas automatizadas aporta un valor fundamental en la reducción
del tiempo de descubrimiento de vectores potenciales. Sin embargo, la
posterior fase de validación manual —que acumuló un estimado de
#strong[50 minutos] del tiempo total del experimento— se erige como el
componente de mayor valor técnico y metodológico en la auditoría. Este
procedimiento no solo reduce la presencia de falsos positivos
intrínsecos a los escaneos automatizados por firmas, sino que documenta
con evidencia concreta el impacto real, la reproducibilidad y el alcance
de las vulnerabilidades dentro de una infraestructura informática.

#strong[Tabla 13. Distribución temporal de la sesión de auditoría manual
del capítulo 17]

#figure(
align(center)[#table(
  columns: 6,
  align: (col, row) => (auto,auto,auto,auto,auto,auto,).at(col),
  inset: 6pt,
  [Fase de la Auditoría], [Herramienta Utilizada], [Técnica / Modalidad
  Operativa], [Tiempo Automatizado \(Descubrimiento)], [Tiempo Manual
  \(Validación / Triaje)], [Tiempo Total por Herramienta],
  [1. Reconocimiento de Sesión],
  [Navegador Web \(DevTools)],
  [Inspección de Cookies e Identificadores de Sesión],
  [#emph[N/A \(Operación Manual)];],
  [10 minutos],
  [#strong[10 minutos];],
  [2. Mapeo de Estructura],
  [OWASP ZAP Spider],
  [Rastreo Pasivo y Web Crawling de Enlaces Visibles],
  [05 minutos],
  [#emph[N/A \(Fase de Reconocimiento)];],
  [#strong[5 minutos];],
  [3. Descubrimiento Oculto],
  [ffuf \(Fuzzing)],
  [Fuerza Bruta de Directorios mediante Diccionarios],
  [10 minutos],
  [05 minutos],
  [#strong[15 minutos];],
  [4. Análisis Dinámico \(DAST)],
  [OWASP ZAP Active Scan],
  [Inyección de Vectores y Firmas de Ataque Genéricas],
  [40 minutos],
  [15 minutos \(Command Injection + XSS)],
  [#strong[55 minutos];],
  [5. Explotación de Datos],
  [sqlmap],
  [Inyección SQL Automatizada y Volcado de Tablas],
  [20 minutos],
  [10 minutos #emph[\(Validación de Sintaxis y UNION)];],
  [#strong[30 minutos];],
  [6. Inclusión de Archivos],
  [OWASP ZAP / Manipulación URL],
  [Inyección de Secuencias de Escape Dinámicas \(LFI)],
  [#emph[Incluido en ZAP Active Scan];],
  [10 minutos],
  [#strong[10 minutos];],
  [Cómputo Global del Experimento],
  [#strong[Enfoque Mixto];],
  [#strong[Ciclo de Auditoría y Validación Técnica Completa];],
  [#strong[75 minutos];],
  [#strong[50 minutos];],
  [#strong[125 minutos \(\~2 horas)];],
)]
)

#text(size: 10pt)[#emph[Nota. Elaboración de los autores a partir de los datos
recolectados durante la sesión de auditoría manual del 4 de agosto de
2026 descrita en este apartado.]]

La Tabla 13 ilustra cómo se distribuyó el esfuerzo temporal a lo largo
de las distintas etapas de la auditoría informática. Se puede observar
una correlación directa entre el uso de herramientas automatizadas para
el descubrimiento masivo de endpoints y el posterior empleo del factor
humano para la validación de vulnerabilidades complejas. El balance
temporal demuestra que el 60% del tiempo total del experimento \(75 de
125 minutos) se delegó a procesos automatizados de recolección de datos,
mientras que el 40% restante \(50 de 125 minutos) se invirtió en la
comprobación manual y artesanal de los vectores de explotación, lo que
reduce la presencia de falsos positivos en el reporte final, sin
eliminarla por completo: la validación manual cubrió cinco vectores
puntuales de esta sesión \(reconocimiento de rutas, inyección de
comandos, inyección SQL, XSS reflejado e inclusión local de archivos).
