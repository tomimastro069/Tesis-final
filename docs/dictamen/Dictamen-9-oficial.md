**UNIVERSIDAD TECNOLÓGICA NACIONAL — FACULTAD REGIONAL MENDOZA**

Tecnicatura Universitaria en Programación

**Dictamen de Novena Corrección**

*Auditoría de subsanación sobre la lista de acabado del dictamen anterior (U1–U4 y residuos) y de los defectos introducidos por la recomposición del documento en Typst · calificación actualizada*

**Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web**

**Autores**  Tomas Mastropietro · Cristian Krahulik · Juan Segura

**Directores**  La portada consigna «Alberto Cortez y Ariel Enferrel», sin cambios respecto de la instancia anterior. Su confirmación sigue a cargo de la coordinación académica.

**Documento evaluado**  Archivo V16 · Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web, 71 páginas numeradas más portada (72 en la paginación del archivo). A diferencia de las entregas anteriores, el documento fue recompuesto íntegramente en Typst 0.15.1; se evalúa únicamente la entrega recibida.

**Dictamen de referencia**  Dictamen de Octava Corrección — «Aprobada con observaciones menores · sin nueva condición previa bloqueante» · 8,4 / 10

**Modalidad**  Verificación de los siete puntos de la lista de acabado del dictamen anterior; recálculo independiente de la aritmética de las trece tablas; cotejo entrada por entrada de los tres índices (121 entradas) contra la paginación real; inventario y resolución de las 59 remisiones internas a secciones; reconstrucción por coordenadas y análisis sintáctico del docker-compose del Anexo A.2; medición de las cajas de las ocho figuras contra la caja de texto; inventario de familias tipográficas, cuerpos, márgenes y colores de encabezado; y cotejo carácter por carácter de los comandos, flags y payloads transcriptos en el cuerpo.

**APROBADA CON OBSERVACIONES MENORES**

**Calificación global: 8,5 / 10**  ·  La lista de acabado anterior, cerrada en las seis operaciones a cargo de los autores.  ·  Sin condición previa bloqueante; una corrección obligatoria antes de la defensa (V1).

La lista de acabado se ejecutó completa y por una vía que no se esperaba: en lugar de corregir uno a uno los residuos, los autores recompusieron el documento entero en Typst. El resultado es el documento tipográficamente más consistente de toda la serie. Los diecinueve capítulos, sus secciones y sus subsecciones arrancan al mismo margen; no queda un solo carácter en Arial; los numerales de las listas, las tablas y los títulos comparten familia, cuerpo y color; los bloques de código de los anexos llevan hoy recuadro y resaltado de sintaxis; y las ciento veintiuna entradas de los tres índices coinciden con la paginación real, sin excepción.

La misma recomposición introdujo, sin embargo, un defecto que no existía en la V15. Typst convierte el doble guion en raya tipográfica cuando el texto no está marcado como código, y eso alteró precisamente los pasajes que el documento transcribe de forma literal: los flags de SQLMap de las secciones 12.6, 12.7, 13.4 y 14.4 aparecen hoy como «–batch», «–threads=10» o «–technique=BEUST», y el payload que la sección 13.4 presenta como «real registrado» perdió el comentario SQL y quedó partido en dos párrafos. El comando que el dictamen anterior calificó de ejecutable ya no lo es tal como está impreso.

Ninguna cifra, tabla ni conclusión se vio afectada, y la reparación es mecánica —marcar esos pasajes como código en línea, como el propio documento ya hace en la sección 11.5.1—. Por eso no se la trata como condición previa, pero sí como corrección obligatoria antes de la defensa: es el único punto de esta instancia que un integrante del tribunal con experiencia en la herramienta advertiría como error técnico.

# **1\. Resumen ejecutivo**

De los siete puntos de la lista de acabado del dictamen anterior, las seis operaciones a cargo de los autores quedaron subsanadas; la séptima —la confirmación de los directores— no depende de ellos. Lo nuevo de esta instancia proviene en su totalidad del cambio de herramienta de composición.

| Avances verificados | Lo que queda pendiente |
| :---- | :---- |
| **Lista de acabado cerrada.** Figura 1 ampliada dentro de la caja y sin cortes (U3); Tabla 13 remitida a la página correcta (U1); espacio restituido en el título del capítulo 17 (U2); capítulos 1 y 2 sin numeral partido ni sangría (U4). | **Flags y payload alterados por la conversión de guiones (V1).** Trece flags de SQLMap impresos con raya en lugar de doble guion, el payload de 13.4 sin su comentario SQL y partido en dos párrafos, y comillas tipográficas en allow\_origins (15.2). Corrección obligatoria antes de la defensa. |
| **Tipografía uniforme en todo el documento.** Calibri en cuerpo, tablas, listas y títulos; Consolas en el código; cero apariciones de Arial. Todos los títulos a 70,9 pt y en el mismo azul (\#4E80BC), incluido el matiz disperso de los rótulos de los anexos. | **Las ampliadas del Anexo H casi no amplían (V2).** Contenidas en la caja, la Figura 1 ampliada mide 1,13 veces la del cuerpo y la Figura 4, 1,18 veces; los rótulos del diagrama de secuencia vuelven a ser ilegibles. |
| **Índices exactos y remisiones sanas.** Las 121 entradas de los tres índices coinciden con la paginación real; las 59 remisiones a secciones resuelven; la aritmética de las trece tablas cierra. | **Dos imprecisiones de remisión y epígrafe en el Anexo H (V3).** El anexo ubica la Figura 2 en secciones donde no se presenta, y el epígrafe de la Figura 3 ampliada difiere del del cuerpo. |
| **Anexos técnicos mejor presentados.** Bloques de código recuadrados y con resaltado; el docker-compose del Anexo A.2 se reconstruye y parsea sin error, con sus cinco servicios. | **Residuos de acabado (V4).** Fórmula de 3.3 en otra familia tipográfica; rótulo y encabezados de la Tabla 7; nota de la Tabla 10 partida entre páginas; URL del Dockerfile cortada a mitad de línea. |

**Balance de subsanación**

| Origen del punto pendiente | Total | Subsanados | Parciales | No subsanados |
| :---- | :---- | :---- | :---- | :---- |
| Lista de acabado — operaciones a cargo de los autores (U1–U4, residuos tipográficos, numerales de lista) | 6 | **6** | — | — |
| Confirmación de los directores (a cargo de la coordinación académica) | 1 | — | — | No verificable |
| **TOTAL a cargo de los autores** | **6** | **6 (100 %)** | **0** | **0** |

***Lectura del balance.** Es la primera instancia de la serie en que todo lo que el dictamen anterior dejó a cargo de los autores quedó cerrado por completo. Los cuatro hallazgos que se consignan más abajo no son arrastres: son defectos nuevos, y tres de ellos (V1, V2 y parte de V4) tienen la misma causa —el cambio de herramienta de composición—.*

# **2\. Verificación de la lista de acabado**

| Punto de la lista | Estado | Verificación en la entrega |
| :---- | :---- | :---- |
| U3 · Anexo H. Reducir la Figura 1 ampliada a la caja de texto, centrarla y contener también las Figuras 2 y 4\. | **Subsanada** | Las cuatro ampliadas están hoy dentro de la caja de texto (89–506 pt de ancho, sobre una caja de 70,9–524,4 pt) y ninguna excede el borde inferior: la Figura 1 ampliada ocupa 154–514 pt de alto en una hoja de 842\. Lo pedido se cumplió. Como efecto colateral, las figuras de rótulos más pequeños dejaron de ampliar de forma útil; se consigna como hallazgo nuevo (V2). |
| U1 · Índice de tablas. Remitir la Tabla 13 a su página real. | **Subsanada** | La entrada remite a la página 55, donde están el rótulo y la tabla. Tras el corrimiento general de paginación que produjo la recomposición, las 121 entradas de los tres índices coinciden con la página real (véase sección 3). |
| U2 · Capítulo 17\. Insertar el espacio tras el numeral. | **Subsanada** | El título se compone «17. Desarrollo Experimental y Validación de Hallazgos», como los otros dieciocho. |
| U4 · Capítulos 1 y 2\. Quitar el carácter invisible del numeral y alinear el capítulo 1 al margen. | **Subsanada** | Los títulos «1. Introducción» y «2. Planteo del Problema» se componen con dígito, punto y espacio, sin carácter intercalado, y arrancan en x \= 70,9 pt, el mismo margen de los capítulos 3 a 19\. |
| Residuos tipográficos. Títulos 4.1, 4.2, 8.1–8.6 y 9.1; Tabla 6 en el índice; fila de cierre de la Tabla 13\. | **Subsanada** | Todos los títulos de segundo y tercer nivel del documento arrancan en 70,9 pt. La entrada de la Tabla 6 ocupa una sola línea en Calibri 11\. La fila «Cómputo Global del Experimento» de la Tabla 13 está íntegramente en Calibri Bold. |
| Numerales de lista. Componerlos en la familia del texto. | **Subsanada** | El inventario tipográfico del archivo no registra ninguna aparición de Arial: los numerales de 11.4, 11.5.1 y del resto de las listas están en Calibri, igual que el texto de sus ítems. |
| Directores. Confirmación por la coordinación académica. | **No verificable** | La portada no cambió. El tribunal no puede validar la identidad ni la designación de los directores consignados; el punto sigue a cargo de la coordinación. |

# **3\. Verificación aritmética, índices y remisiones**

Se recalcularon de forma independiente las trece tablas. Las trece cierran por quinta instancia consecutiva y su contenido no cambió respecto de la V15. En particular: la Tabla 3 compone 34 URLs como 24 del spider, 8 de ffuf y 2 derivadas, tal como declara su nota; la Tabla 4 suma 37 ocurrencias y se distribuye en Medium 16, Low 14 e Informational 7; la Tabla 9 totaliza 41 hallazgos (37 \+ 4); la Tabla 10 convierte correctamente 845,81 s y 263,15 s y su reducción es del 68,9 %; la Tabla 11 arroja 96,6 % y 96,3 % y su nota justifica las 5 URLs de diferencia en cada corrida; y la Tabla 13 cierra por columnas (75 \+ 50 \= 125 minutos) y por filas (10 \+ 5 \+ 15 \+ 55 \+ 30 \+ 10 \= 125).

Se cotejaron las 121 entradas de los tres índices —100 del índice general, 8 de figuras y 13 de tablas— contra la paginación impresa. La recomposición corrió prácticamente todo el documento (las Referencias pasaron de la página 51 a la 56; la Tabla 13, de la 50 a la 55), y el índice lo absorbió entero: no hay ninguna discrepancia. Se inventariaron además las 59 remisiones a secciones y subsecciones del cuerpo, más las remisiones a capítulos, tablas, figuras y anexos: todas resuelven contra un destino existente. La única imprecisión está en el texto introductorio del Anexo H y se consigna en V3.

Por último, el docker-compose del Anexo A.2 se reconstruyó a partir de las coordenadas de cada carácter y se sometió a análisis sintáctico YAML: parsea sin error y declara los cinco servicios (db, dvwa, zap, app, n8n), coincidentes con el árbol del Anexo A.1, con la sección 12.1 y con la Tabla 12 (OE4). Los bloques de código de los anexos, compuestos como bloques literales, no sufrieron la conversión de guiones que afecta al cuerpo: el «--» del entrypoint de n8n y los flags del Dockerfile están intactos.

# **4\. Hallazgos de la presente instancia**

**V1 · La conversión de guiones alteró los flags de SQLMap y el payload transcripto  \[Medio\]**

Typst trata el doble guion como raya tipográfica cuando el texto no está marcado como código. Todos los pasajes del cuerpo que transcriben la línea de comandos de SQLMap quedaron afectados, y todos están compuestos en Calibri, no en monoespaciada. El dictamen anterior calificó de ejecutable el comando de 12.6; tal como se imprime hoy, no lo es.

| Ubicación | Página | Texto impreso | Debe decir |
| :---- | :---- | :---- | :---- |
| Sección 12.6 | 34 | –batch, –flush-session, –forms, –dbms=MySQL, –level=1, –risk=3, –\[salto de línea\]threads=10, –smart, –technique=BEUST | \--batch, \--flush-session, \--forms, \--dbms=MySQL, \--level=1, \--risk=3, \--threads=10, \--smart, \--technique=BEUST |
| Sección 12.7 | 34 | –output-\[salto de línea\]format=json | La opción, en monoespaciada y sin partir (véase además la pregunta previsible sobre este flag) |
| Sección 13.4 | 39 | (–technique=BEUST) | (--technique=BEUST) |
| Sección 13.4 (payload «real registrado») | 39 | … 0x28 END))–  \[párrafo nuevo\]  RmAL\&password=Fqvd\&Login=Login | El payload completo, con su comentario SQL de doble guion, en un solo bloque de código |
| Sección 14.4 | 45 | –threads=10 y la bandera –smart | \--threads=10 y la bandera \--smart |
| Sección 15.2 | 49 | allow\_origins=\[“\*”\] (comillas tipográficas) | allow\_origins=\["\*"\] |

El caso más delicado es el payload: el texto lo presenta como la evidencia literal registrada en sqlmap\_bg.log, y hoy no coincide con ella ni carácter por carácter ni en su continuidad. La reparación es la misma para las seis ubicaciones: marcar comandos, flags, payloads y fragmentos de código como código en línea (entre comillas invertidas), que en Typst suprime la conversión y compone en monoespaciada, tal como el documento ya hace con POST /scan, scan\_id y ejecutar\_pipeline\_segundo\_plano() en la sección 11.5.1. Conviene aplicar el mismo criterio a los nombres de módulos, funciones y rutas de los capítulos 12 a 14, hoy en Calibri.

**V2 · Las ampliadas del Anexo H quedaron dentro de la caja, pero casi no amplían  \[Bajo\]**

Al contenerlas en la caja de texto —que es lo que pidió el dictamen anterior—, las Figuras 1 y 4 ampliadas quedaron apenas mayores que sus versiones del cuerpo: la Figura 1 mide 399 pt de ancho frente a 354 (1,13 veces) y la Figura 4, 417 × 340 pt frente a 354 × 289 (1,18 veces). En la V15, la Figura 4 ampliada medía 592 × 604 pt y el dictamen anterior la consideró legible; hoy es un 30 % más angosta y los rótulos del diagrama de secuencia UML —los más pequeños del documento— vuelven a no poder leerse a tamaño de impresión. Las Figuras 2 y 3 sí amplían de forma apreciable (1,48 y 1,41 veces).

La contradicción entre «ampliar» y «no salir de la caja» se resuelve girando la hoja: compuestas en páginas apaisadas (en Typst, page(flipped: true)) y al ancho completo de la caja, las Figuras 1 y 4 pueden superar el doble del tamaño del cuerpo sin invadir ningún margen. Se consigna como bajo porque las cuatro figuras están completas en el cuerpo y ningún contenido se pierde.

**V3 · Remisión imprecisa y epígrafe dispar en el Anexo H  \[Bajo\]**

La introducción del anexo afirma que las Figuras 1 a 4 fueron «presentadas y comentadas en las secciones 11.1, 11.4 y 11.5»; la Figura 2 se presenta y comenta en la sección 11.2 (página 28), que la enumeración omite. Además, la Figura 3 ampliada se rotula «Diagrama del Pipeline de Ejecución», mientras que en el cuerpo, en el índice de figuras y en la propia introducción del anexo figura como «Diagrama de Pipeline de ejecución». Basta con agregar 11.2 a la enumeración y unificar el epígrafe.

**V4 · Residuos de acabado  \[Bajo\]**

Ninguno afecta el contenido. (a) Las dos fórmulas de la sección 3.3 (página 11\) están compuestas en la fuente matemática por defecto (New Computer Modern), incluidas las palabras «horas», «USD» y «revisiones», lo que las aparta visualmente del resto del documento en Calibri; conviene fijar la fuente matemática o escribir las unidades como texto. (b) La Tabla 7 (página 39\) se rotula «Datos extraídos a través de Sql Injection – corrida del 5 de agosto del 2026», mientras la Tabla 6 usa «SQL» y «de 2026»; sus encabezados mezclan «User\_id», «User», «Password», «last\_name» y «first\_name»; y la columna «Password» contiene hashes MD5, no contraseñas, por lo que convendría rotularla «Password (hash MD5)». (c) La nota de la Tabla 10 empieza en la página 43 y termina en la 44\. (d) En el Dockerfile del Anexo A.3 (página 61), la URL del wget se corta a mitad de línea y la continuación arranca sin sangría, lo que puede leerse como una línea independiente; conviene partir la orden con una barra invertida o acortarla con una variable.

# **5\. Calificación por capítulo**

| Capítulo | Anterior | Actual | Fundamento |
| :---- | ----- | ----- | :---- |
| Introducción | 7,4 | **7,6** | Numeral sin carácter invisible y título al margen (U4). Contenido sin cambios. |
| Planteo del problema | 6,9 | **7,0** | Numeral restituido (U4); cae la última penalización de forma. |
| Justificación | 6,5 | **6,5** | Sin cambios de contenido. Las fórmulas de 3.3 en otra familia tipográfica (V4) no alteran la nota. |
| Objetivos | 7,6 | **7,7** | 4.1 y 4.2 alineados al margen. |
| Preguntas de investigación | 7,6 | **7,6** | Sin cambios. |
| Hipótesis | 7,4 | **7,4** | Sin cambios. |
| Estado del arte | 8,4 | **8,4** | Sin cambios. La Tabla 1 gana legibilidad con la nueva composición. |
| Marco teórico | 8,4 | **8,5** | 8.1 a 8.6 alineados al margen. |
| Alcances y limitaciones | 7,3 | **7,4** | 9.1 alineado al margen. |
| Metodología | 8,1 | **8,1** | Sin cambios. |
| Arquitectura | 8,5 | **8,6** | Numerales en Calibri; 11.5.1 compone el código en línea en monoespaciada, el criterio que V1 pide extender. |
| Implementación técnica | 8,4 | **7,9** | Retroceso. El comando de SQLMap de 12.6 y el flag de 12.7 están impresos con raya en lugar de doble guion y en fuente de texto; el comando ya no es ejecutable tal como se lee (V1). |
| Resultados | 8,4 | **8,1** | Retroceso. El payload «real registrado» de 13.4 perdió su comentario SQL y quedó partido en dos párrafos (V1); rótulo y encabezados de la Tabla 7 (V4). Las seis tablas cierran. |
| Discusión | 8,6 | **8,5** | Flags de 14.4 alterados (V1). Sigue entre los capítulos mejor calificados. |
| Conclusiones | 8,1 | **8,0** | Comillas tipográficas en allow\_origins (15.2, V1). |
| Consideraciones éticas | 8,2 | **8,2** | Sin cambios. |
| Desarrollo experimental (cap. 17\) | 8,6 | **8,8** | Título con espacio (U2), Tabla 13 bien indexada (U1) y con fila de cierre uniforme. |
| Referencias | 8,8 | **8,9** | Sangría francesa conservada y composición uniforme en las veintiséis entradas. |
| Anexos | 8,5 | **8,5** | Mejoran: código recuadrado y resaltado, docker-compose que parsea, ampliadas dentro de la caja (U3). Compensan: las Figuras 1 y 4 ampliadas apenas amplían (V2) y la remisión y el epígrafe del Anexo H (V3). |

El promedio simple de las diecinueve notas por capítulo es 7,98, prácticamente igual al de la instancia anterior (7,99): las mejoras de forma en nueve capítulos quedan compensadas por el retroceso de los tres capítulos técnicos que transcriben comandos. La calificación global se establece en 8,5 / 10, frente al 8,4 anterior, porque la recomposición aporta una uniformidad que atraviesa todo el documento y que la nota por capítulo no alcanza a reflejar: por primera vez no queda un solo residuo de estilo, margen, familia o índice. No alcanza el 8,7 que proyectaba el dictamen anterior porque la misma recomposición introdujo V1 y V2. Corregidos V1 a V4, la calificación de este mismo documento se ubicaría alrededor de 8,8.

# **6\. Dictamen final**

**APROBADA CON OBSERVACIONES MENORES**

8,5 / 10 · La lista de acabado anterior, cerrada en las seis operaciones a cargo de los autores · Sin condición previa bloqueante · Una corrección obligatoria antes de la defensa (V1)

**Fundamentación**

Esta es la instancia en que la forma del documento dejó de ser un tema. Todo lo que el dictamen anterior dejó pendiente —una figura fuera de caja, una entrada del índice desfasada, un título sin espacio, dos numerales partidos, un puñado de títulos corridos seis puntos y una familia tipográfica sobrante— quedó resuelto, y quedó resuelto de raíz: al recomponer el documento en un sistema que aplica los estilos por regla y no por párrafo, los autores eliminaron la causa de los desajustes que se arrastraban desde la quinta instancia.

Esa misma decisión trajo un costo que conviene nombrar con precisión. Un sistema de composición tipográfica «mejora» automáticamente los guiones y las comillas del texto corrido, y en un trabajo de seguridad informática el texto corrido incluye líneas de comando y payloads que deben leerse carácter por carácter. Hoy, el comando de SQLMap, cuatro flags repartidos entre los capítulos 12 y 14 y el payload que el capítulo 13 presenta como evidencia literal no dicen lo que la herramienta ejecutó. No hay allí ninguna cifra alterada ni ninguna conclusión comprometida, y la reparación lleva minutos; pero es precisamente el tipo de detalle que un tribunal con experiencia en la herramienta detecta en la primera lectura, y por eso se exige corregirlo antes de la defensa.

Lo demás es de acabado. El Anexo H cumple hoy lo que se le pidió —sus figuras están dentro de la caja— y la manera de que además amplíe es girar la hoja. El resto de la lista son remisiones, rótulos y cortes de línea que no obligan a volver a medir, correr ni redactar. El trabajo sigue en condiciones de defenderse.

**Corrección obligatoria antes de la defensa**

* **V1 · Comandos, flags y payloads.** Componer como código en línea (entre comillas invertidas) el comando de SQLMap de 12.6, el flag de 12.7, los flags de 13.4 y 14.4, el payload de 13.4 —completo, con su comentario SQL y sin partir— y el allow\_origins de 15.2. Verificar después, en el PDF, que cada doble guion se imprime como tal.

**Lista de acabado recomendada (no bloqueante)**

* **Anexo H (V2).** Componer las Figuras 1 y 4 ampliadas en páginas apaisadas y al ancho completo de la caja, para que efectivamente amplíen.

* **Anexo H (V3).** Agregar la sección 11.2 a la enumeración de la introducción y unificar el epígrafe de la Figura 3 ampliada con el del cuerpo.

* **Código en línea.** Extender la monoespaciada a los nombres de módulos, funciones y rutas de los capítulos 12 a 14, como ya ocurre en 11.5.1.

* **Tabla 7\.** Rotularla «SQL Injection» y «de 2026», unificar los encabezados y aclarar que la columna de contraseñas contiene hashes MD5.

* **Residuos (V4).** Fijar la fuente de las fórmulas de 3.3; evitar el corte de la nota de la Tabla 10 entre páginas; partir con barra invertida la orden wget del Dockerfile.

* **Directores.** Que la coordinación académica confirme que los directores consignados son los asignados al trabajo.

**Preguntas previsibles del tribunal**

***«¿SQLMap tiene un flag \--output-format=json?»*** — No como opción de la línea de comandos: la salida estructurada en JSON se obtiene a través de su API REST (sqlmapapi.py). Conviene reformular la frase de 12.7 en ese sentido antes de la defensa.

***«La columna Password de la Tabla 7, ¿son contraseñas?»*** — Son hashes MD5 de las contraseñas por defecto de DVWA; por ejemplo, 5f4dcc3b5aa765d61d8327deb882cf99 corresponde a «password». Conviene decirlo en el rótulo.

***«El escaneo activo, ¿tarda cuarenta minutos o diez?»*** — Sigue teniendo respuesta escrita: la nota de trazabilidad del capítulo 17 declara que esa sesión corrió con la configuración previa al ajuste de timeouts de 14.4.

***«¿Podemos levantar el entorno con el archivo del Anexo A?»*** — Sí: el docker-compose parsea, declara los cinco servicios y coincide con el árbol de A.1 y con 12.1.

***«El timeout de SQLMap es de 300 s según 12.3, pero la Tabla 13 le asigna veinte minutos, ¿cómo se concilia?»*** — 300 s es el tope por invocación; la sesión atacó varias URLs candidatas en segundo plano.

**Cierre**

La instancia anterior dejó una lista de acabado y proyectó 8,7 si se cumplía. Se cumplió entera, y por una vía que además previene su reaparición; la calificación se establece en 8,5 porque el cambio de herramienta trajo consigo un defecto nuevo en los pasajes más literales del trabajo. Lo pendiente es corto y concreto: que los comandos se lean como se ejecutan, y que el anexo de diagramas amplíe. Nada de ello exige volver a medir, correr ni redactar.

***Nota de alcance.** Esta evaluación se basa en el cotejo entre el archivo V16 entregado y el Dictamen de Octava Corrección, complementado con: recálculo independiente de la aritmética de las trece tablas; verificación entrada por entrada de los tres índices contra la paginación real; inventario y resolución de las remisiones internas; reconstrucción por coordenadas y análisis sintáctico del docker-compose del Anexo A.2; medición de las cajas de las ocho figuras; inventario de familias tipográficas, cuerpos, márgenes y colores; y cotejo carácter por carácter de los comandos, flags y payloads del cuerpo. No incluye la ejecución ni la auditoría del código del repositorio, ni la reproducción del entorno de laboratorio, ni la verificación de que las corridas y la sesión manual se hayan realizado en las condiciones que el documento declara, ni la validación de la identidad o designación de los directores. Los estados de subsanación consignan lo que el texto entregado permite verificar. Las calificaciones numéricas reflejan un juicio experto orientado a asistir a los autores y no constituyen una nota oficial de la institución.*