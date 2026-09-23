= 13. Resultados Obtenidos
<resultados-obtenidos>
#quote(block: true)[
Los resultados de este capítulo corresponden a la ejecución del pipeline
completo contra DVWA \(DVWA Project, 2024) registrada el 5 de agosto de
2026 a las 19:53 \(hora local del entorno), y son verificables
directamente contra los archivos resultado\_unificado.json,
reporte\_seguridad.md y sqlmap\_bg.log del repositorio del proyecto.

#strong[Nota metodológica sobre la fuente de estos datos.] Una versión
preliminar de este capítulo citaba cifras \(61 URLs, 55 del spider, 56
alertas de ZAP) extraídas de un archivo test\_resultado\_final.json que
no se conserva en el repositorio del proyecto, por lo que no pudieron
verificarse contra ninguna corrida real disponible. Esta versión
reemplaza esas cifras por los datos de la ejecución más reciente y
verificable del pipeline \(5 de agosto de 2026), trazable directamente a
resultado\_unificado.json, reporte\_seguridad.md y sqlmap\_bg.log. Cabe
aclarar que ZAP y SQLMap son herramientas de escaneo dinámico cuyo
comportamiento no es estrictamente determinístico entre corridas —el
orden de exploración del spider, los tiempos de respuesta del servidor y
el estado de la caché incremental pueden variar el número exacto de URLs
y alertas detectadas de una ejecución a otra sobre el mismo objetivo—,
tal como se declara en la amenaza a la validez de Confiabilidad
\(sección 10.5). En consecuencia, las cifras de este capítulo deben
leerse como el resultado de una ejecución puntual, documentada y
trazable, y no como una constante reproducible con exactitud aritmética
entre corridas.

Evidencia adicional de esta variabilidad: esta misma corrida del 5 de
agosto ofrece un ejemplo concreto del fenómeno descripto arriba. Una
ejecución previa registrada el 2 de agosto de 2026 había confirmado
inyección SQL tanto en el parámetro id de /vulnerabilities/sqli/ como en
el parámetro username de /vulnerabilities/brute/ \(8 hallazgos
individuales, 4 técnicas × 2 endpoints). En la corrida del 5 de agosto
documentada en este capítulo, SQLMap solo confirmó el segundo punto
\(/vulnerabilities/brute/, parámetro username, 4 hallazgos
individuales); el endpoint /vulnerabilities/sqli/ no volvió a reportarse
como vulnerable en esta pasada, pese a no haberse modificado el objetivo
entre ambas corridas. Spider, ZAP y ffuf se mantuvieron estables entre
ambas ejecuciones. Este contraste entre dos corridas reales —no
hipotético— es la evidencia más directa disponible en este informe de
que los resultados de SQLMap pueden variar entre ejecuciones sobre el
mismo objetivo sin cambios de por medio, y es retomado con un tercer
punto de datos en la sección 14.3.
]

== 13.1 Resumen de Hallazgos
<resumen-de-hallazgos>
#strong[Tabla 3. Resumen de hallazgos — ejecución sobre DVWA del 5 de
agosto de 2026]

#figure(
align(center)[#table(
  columns: 2,
  align: (col, row) => (auto,auto,).at(col),
  inset: 6pt,
  [Indicador], [Valor],
  [Total de URLs únicas descubiertas y analizadas],
  [34],
  [URLs descubiertas por el Spider],
  [24],
  [Alertas de seguridad reportadas por ZAP],
  [37],
  [Rutas descubiertas por ffuf],
  [8],
  [Hallazgos individuales reportados por SQLMap],
  [4 \(4 técnicas × 1 endpoint vulnerable)],
)]
)

#text(size: 10pt)[#emph[Nota. Datos extraídos de resultado\_unificado.json \(campo
resumen). El total de 34 URLs únicas no es la simple suma de spider
\(24) y ffuf \(8): las 2 URLs restantes corresponden a la URL semilla
del objetivo \(#link("http://dvwa/");) y a una URL derivada del proceso
de autenticación automática \(#link("http://dvwa/login.php") con
parámetros de sesión), incorporadas al conjunto unificado antes de la
deduplicación por el módulo consolidar\_resultados\() y no
contabilizadas en los campos spider.resultados ni ffuf.rutas del JSON
crudo.]]

== 13.2 Vulnerabilidades Detectadas por OWASP ZAP
<vulnerabilidades-detectadas-por-owasp-zap>
#quote(block: true)[
El escaneo activo de OWASP ZAP reportó un total de 37 alertas de
seguridad. La Tabla 4 sintetiza los tipos de alerta detectados y su
cantidad de ocurrencias.

#strong[Cómo leer la columna Severidad.] Cada valor sigue el formato
Riesgo \(Confianza) que expone el campo riskdesc de la API de ZAP: el
primer término \(High, Medium, Low o Informational) es el nivel de
riesgo de la vulnerabilidad, y el término entre paréntesis es el nivel
de confianza — qué tan seguro está ZAP de que el hallazgo es real y no
un falso positivo— \(también High, Medium, Low, o Confirmed). Son dos
escalas independientes: un hallazgo “Low \(High)”, como Server Leaks
Version Information en la tabla siguiente, es de bajo riesgo pero con
alta confianza de que el hallazgo es correcto; en cambio un “Medium
\(Medium)” es de riesgo medio con una confianza también media, es decir,
con mayor probabilidad relativa de ser un falso positivo. La confianza
no debe confundirse con la severidad: un hallazgo de alto riesgo pero
baja confianza amerita revisión manual antes de tratarse como
confirmado, mientras que uno de bajo riesgo y alta confianza puede
priorizarse con más certeza aunque su impacto sea menor.
]

#strong[Tabla 4. Vulnerabilidades detectadas por OWASP ZAP, por tipo]

#figure(
align(center)[#table(
  columns: 4,
  align: (col, row) => (auto,auto,auto,auto,).at(col),
  inset: 6pt,
  [Vulnerabilidad], [Severidad], [Ocurrencias], [URL de ejemplo],
  [Content Security Policy \(CSP) Header Not Set],
  [Medium \(High)],
  [5],
  [http:\/\/dvwa/about.php],
  [Directory Browsing],
  [Medium \(Medium)],
  [5],
  [http:\/\/dvwa/docs/],
  [Missing Anti-clickjacking Header],
  [Medium \(Medium)],
  [5],
  [http:\/\/dvwa/about.php],
  [Server Leaks Version Information \(\"Server\" header)],
  [Low \(High)],
  [5],
  [http:\/\/dvwa],
  [X-Content-Type-Options Header Missing],
  [Low \(Medium)],
  [5],
  [http:\/\/dvwa/dvwa/css/login.css],
  [User Agent Fuzzer],
  [Informational \(Medium)],
  [5],
  [http:\/\/dvwa/about.php],
  [In Page Banner Information Leak],
  [Low \(High)],
  [2],
  [http:\/\/dvwa/sitemap.xml],
  [Information Disclosure - Debug Error Messages],
  [Low \(Medium)],
  [2],
  [http:\/\/dvwa/instructions.php],
  [HTTP Only Site],
  [Medium \(Medium)],
  [1],
  [http:\/\/dvwa/],
  [Authentication Request Identified],
  [Informational \(High)],
  [1],
  [http:\/\/dvwa/login.php],
  [Information Disclosure - Suspicious Comments],
  [Informational \(Medium)],
  [1],
  [http:\/\/dvwa/setup.php],
)]
)

#quote(block: true)[
#text(size: 10pt)[#emph[Nota. Datos extraídos de resultado\_unificado.json /
reporte\_seguridad.md. La severidad reproduce el campo riskdesc de ZAP
en formato «Nivel de Riesgo \(Nivel de Confianza)».]]

La distribución de las 37 alertas por nivel de severidad base es la
siguiente: Medium 16 \(43,2%), Low 14 \(37,8%) e Informational 7
\(18,9%). No se registraron alertas de severidad High en esta ejecución
del escaneo pasivo/activo de ZAP; los hallazgos de severidad alta de
esta entrega provienen de SQLMap \(sección 13.4).
]

== 13.3 Rutas Descubiertas por ffuf
<rutas-descubiertas-por-ffuf>
#strong[Tabla 5. Rutas descubiertas por fuzzing de directorios \(ffuf)]

#figure(
align(center)[#table(
  columns: 3,
  align: (col, row) => (auto,auto,auto,).at(col),
  inset: 6pt,
  [Ruta Descubierta], [Input \(Wordlist)], [Código HTTP],
  [http:\/\/dvwa/about.php],
  [about.php],
  [200],
  [http:\/\/dvwa/index.php],
  [index.php],
  [302],
  [http:\/\/dvwa/instructions.php],
  [instructions.php],
  [200],
  [http:\/\/dvwa/login.php],
  [login.php],
  [200],
  [http:\/\/dvwa/logout.php],
  [logout.php],
  [302],
  [http:\/\/dvwa/phpinfo.php],
  [phpinfo.php],
  [302],
  [http:\/\/dvwa/security.php],
  [security.php],
  [302],
  [http:\/\/dvwa/setup.php],
  [setup.php],
  [200],
)]
)

#text(size: 10pt)[#emph[Nota. Datos extraídos de resultado\_unificado.json, campo
ffuf.rutas.]]

== 13.4 Análisis Automatizado con SQLMap
<análisis-automatizado-con-sqlmap>
#quote(block: true)[
SQLMap se ejecutó sobre las URLs con parámetros descubiertas por el
spider y por ffuf. En esta corrida se confirmó como vulnerable el
parámetro username del formulario de fuerza bruta
\(/vulnerabilities/brute/), mediante las cuatro técnicas configuradas
\(--technique\=BEUST), lo que totaliza los 4 hallazgos individuales del
resumen consolidado. El payload real registrado para la técnica
boolean-based blind fue: username\=SCVZ\' RLIKE \(SELECT \(CASE WHEN
\(4201\=4201) THEN 0x5343565a ELSE 0x28 END))--

RmAL&password\=Fqvd&Login\=Login.
]

#strong[Tabla 6. Endpoints confirmados como vulnerables por SQLMap —
corrida del 5 de agosto de 2026]

#figure(
align(center)[#table(
  columns: 3,
  align: (col, row) => (auto,auto,auto,).at(col),
  inset: 6pt,
  [Endpoint], [Parámetro], [Técnicas que confirmaron la inyección],
  [/vulnerabilities/brute/],
  [username],
  [Boolean-based blind \(RLIKE), Error-based \(EXTRACTVALUE), Time-based
  blind \(SLEEP), UNION query \(8 columnas)],
)]
)

#text(size: 10pt)[#emph[Nota. Datos extraídos de sqlmap\_bg.log y
resultado\_unificado.json.]]

#strong[Tabla 7. Datos extraídos a través de Sql Injection – corrida del
5 de agosto del 2026]

#figure(
align(center)[#table(
  columns: 5,
  align: (col, row) => (auto,auto,auto,auto,auto,).at(col),
  inset: 6pt,
  [User\_id], [User], [Password], [last\_name], [first\_name],
  [1],
  [admin],
  [903a98d709fa4683aaaa036b84c125a6],
  [admin],
  [admin],
  [2],
  [gordonb],
  [e99a18c428cb38d5f260853678922e03],
  [Brown],
  [Gordon],
  [3],
  [1337],
  [8d3533d75ae2c3966d7e0d4fcc69216b],
  [Me],
  [Hack],
  [4],
  [pablo],
  [0d107d09f5bbe40cade3de5c71e9e9b7],
  [Picasso],
  [Pablo],
  [5],
  [smithy],
  [5f4dcc3b5aa765d61d8327deb882cf99],
  [Smith],
  [Bob],
)]
)

#text(size: 10pt)[#emph[Nota. Datos extraídos de sqlmap\_bg.log y
resultado\_unificado.json. Además, se evitaron columnas como «avatar»,
«last\_login» o «failed\_login» debido a que no aportan información
relevante para el análisis presentado en este informe. Los valores
mostrados son las credenciales por defecto de DVWA, una aplicación
deliberadamente vulnerable; el criterio de manejo responsable de datos
extraídos descrito en el capítulo 16 \(principio 1.6 del código ACM)
rige para cualquier uso de esta técnica sobre un objetivo real.]]

A partir de la explotación exitosa, SQLMap identificó el motor de base
de datos como MySQL/MariaDB, enumeró la base de datos activa \(dvwa) y
extrajo el contenido de las tablas users \(5 registros) y guestbook \(1
registro), replicando el conjunto de datos por defecto de DVWA. Los
timestamps last\_login de la tabla users \(2026-08-05 19:50:13)
coinciden con el horario de esta corrida, confirmando que el volcado
corresponde a una extracción en vivo y no a datos de ejemplo
reutilizados. El volcado completo está disponible en
reporte\_seguridad.md y sqlmap\_bg.log.

#quote(block: true)[
Sobre el endpoint /vulnerabilities/sqli/ \(parámetro id): en la corrida
del 2 de agosto de 2026 este endpoint también se había confirmado como
vulnerable, con las mismas cuatro técnicas. En la corrida del 5 de
agosto no fue reportado por SQLMap. No se modificó el código de la
aplicación objetivo entre ambas fechas; la explicación más plausible es
que, en esta pasada puntual, el conjunto de URLs con parámetros que el
spider y ffuf le entregaron a SQLMap no incluyó una variante de
/vulnerabilities/sqli/ con un parámetro id explícito en la forma que
SQLMap necesita para reconocerlo como candidato, o bien el mecanismo de
re-testeo priorizó otro orden de ataque dentro del tiempo disponible.
Esta explicación se retoma y refuerza con un tercer punto de datos en la
sección 14.3.
]

== 13.5 Análisis por Categoría OWASP Top 10
<análisis-por-categoría-owasp-top-10>
#strong[Tabla 8. Hallazgos clasificados por categoría OWASP Top 10]

#figure(
align(center)[#table(
  columns: 3,
  align: (col, row) => (auto,auto,auto,).at(col),
  inset: 6pt,
  [Categoría OWASP], [Vulnerabilidades detectadas], [Herramienta],
  [A01:2021 – Broken Access Control],
  [Directory Browsing \(5 instancias); rutas administrativas
  \(/setup.php, /security.php) descubiertas por ffuf],
  [ZAP, ffuf],
  [A03:2021 – Injection],
  [SQL Injection confirmada en /vulnerabilities/brute/ \(username);
  confirmada también en /vulnerabilities/sqli/ \(id) en la corrida
  previa del 2 de agosto de 2026],
  [SQLMap],
  [A05:2021 – Security Misconfiguration],
  [CSP Header Not Set, Missing Anti-clickjacking Header,
  X-Content-Type-Options Missing, Server Leaks Version Information, HTTP
  Only Site],
  [ZAP],
)]
)

#text(size: 10pt)[#emph[Nota. Elaboración propia.]]

El sistema detectó vulnerabilidades pertenecientes a tres categorías
distintas del OWASP Top 10 en esta ejecución, cumpliendo el criterio de
cobertura mínima definido en la sección 10.6.
