UNIVERSIDAD TECNOLÓGICA NACIONAL — FACULTAD REGIONAL MENDOZA · TECNICATURA UNIVERSITARIA EN PROGRAMACIÓN

# Dictamen de Séptima Corrección

Auditoría de subsanación sobre la condición previa de coherencia numérica, las siete correcciones recomendadas y los once hallazgos abiertos (S1–S11) · calificación actualizada Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web

Autores Tomas Mastropietro · Cristian Krahulik · Juan Segura

Tutor Sin consignar (séptima instancia consecutiva). La portada conserva la fórmula institucional, pero esta vez truncada: «A designar por la coordinación académica antes». Véase T1.

Documento evaluado Archivo V14 · Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web, 62 páginas numeradas más portada (63 en la paginación del archivo). La numeración del archivo salta de V11 a V14: se evalúa únicamente la entrega recibida.

Dictamen de referencia Dictamen de Sexta Corrección — «Aprobada con observaciones menores · una única condición previa de coherencia numérica» · 7,9 / 10

Modalidad Verificación de los tres componentes de la condición previa, de las siete correcciones recomendadas y de los once hallazgos S1–S11; recálculo independiente de la aritmética de las trece tablas; cotejo entrada por entrada de los tres índices contra la paginación real; inventario y resolución de todas las remisiones internas; cotejo de las veintiséis entradas bibliográficas contra el cuerpo; cotejo cruzado de los parámetros de configuración de los capítulos 12, 14 y 17; verificación del docker-compose.yml del Anexo A contra la estructura del Anexo A.1; y — por primera vez en la serie— auditoría de estilos de encabezado y de numeración automática en el cuerpo, y medición de las cajas de las figuras del Anexo H contra la caja de texto de la página.

## APROBADA CON OBSERVACIONES MENORES

Calificación global: 8,0 / 10 · La condición previa de coherencia numérica, cumplida en sus tres componentes · Una condición previa nueva, exclusivamente de numeración y portada: cuatro operaciones de estilo, sin escribir contenido ni tocar una sola cifra.

La condición previa se cumplió entera y se cumplió bien. Las tres cifras que el dictamen anterior señaló como incompatibles entre capítulos hoy dicen lo mismo en todas las páginas donde aparecen: la nota de trazabilidad del capítulo 17 declara que la sesión del 4 de agosto corrió con la configuración previa al ajuste de timeouts de 14.4 y que por eso sus cuarenta minutos de Active Scan no son comparables con el techo de diez ni con los catorce de la Tabla 10; la sección 12.6 transcribe hoy --threads=10 y --smart, coincidentes con 14.4; y el denominador de treinta y siete alertas desapareció de 17.3, reemplazado por la enumeración de los cinco vectores de la propia sesión. Con ellas se resolvieron además dos de las correcciones recomendadas que tocaban el mismo núcleo: el volumen del servicio app es hoy.:/app en el Anexo A.2, coincidente con 12.1, y la estructura del Anexo A.1 ubica n8n/ y frontend/ fuera de la raíz del proyecto, con lo cual los tres montajes../n8n/… cierran contra el árbol documentado; y las banderas de línea de comandos figuran hoy con doble guion, de modo que el único comando que el documento transcribe es ejecutable tal como está impreso.

El índice volvió a verificarse íntegro y vuelve a estar bien: ciento ocho entradas cotejadas una por una contra la paginación real — ochenta y siete del índice general, ocho del de figuras y trece del de tablas— sin una sola discrepancia de página, y sin negrita, sin versales y sin puntos finales espurios. Las trece tablas cierran aritméticamente por tercera instancia consecutiva. Ninguna remisión interna del documento cuelga.

Lo que impide dar el documento por terminado es, otra vez, de otra naturaleza que lo anterior, y conviene decirlo con precisión. No son cifras: no queda un solo número del trabajo que este tribunal haya podido poner en contradicción con otro. Es la maquinaria de numeración y de estilos de título del procesador de texto, que esta instancia audita por primera vez en el cuerpo del documento y que arrastra cuatro defectos visibles: la fórmula del tutor quedó cortada a mitad de frase en la portada, la lista de pasos de la sección 11.4 arranca en «5», los títulos de cuatro capítulos están construidos como ítems de una lista automática —de modo que «6. Hipótesis» se lee como la sexta pregunta de investigación— y el capítulo 17 tiene su jerarquía de encabezados invertida. Son cuatro operaciones de estilo. No tocan una cifra, una tabla ni una oración.

### 1. Resumen ejecutivo

De los veintiún puntos que el dictamen anterior dejó abiertos —tres componentes de la condición previa, siete correcciones recomendadas y once hallazgos S1–S11—, trece quedan cerrados, seis parcialmente y dos sin cerrar. Los tres que bloqueaban la presentación están entre los cerrados, y ninguno de los puntos que restan es de contenido: todos, sin excepción, son de acabado.

Avances verificados Lo que queda pendiente

La condición previa, cumplida en sus tres componentes. La nota de trazabilidad del capítulo 17 declara hoy la configuración con que corrió la sesión del 4 de agosto y explica los cuarenta minutos; 12.6 y 14.4 coinciden en --threads=10 y en --smart; el denominador ajeno de 17.3 fue suprimido.

La fórmula del tutor quedó truncada en la portada. Lee «A designar por la coordinación académica antes», sin «de la presentación». Es la primera línea que el tribunal ve y hoy está a mitad de frase. Es una regresión de esta entrega.

El comando de SQLMap es ejecutable. Las nueve banderas de 12.6 y

14. 4 figuran con doble guion. El desajuste de hilos desapareció y --smart

está incorporada al comando transcripto.

La lista de pasos de 11.4 está numerada de 5 a 12. Continúa la numeración de la lista de cuatro capas de 11.1 en lugar de reiniciar. Son los ocho pasos del ciclo de vida de un análisis, en la sección que la Tabla 12 invoca como evidencia del OE1.

El entorno cierra contra su propia documentación..:/app en el Anexo A.2 coincide con 12.1, y el árbol del Anexo A.1 ubica n8n/ y Cuatro títulos de capítulo son ítems de una lista automática. Los capítulos 6, 7, 8 y 9 no llevan su número en el texto: lo reciben de un campo

Dictamen de Séptima Corrección · Orquestador de Seguridad · UTN FRM Página 1 de 8

frontend/ fuera de la raíz, de modo que los montajes../n8n/… resuelven. Se incorporaron además OPTIMIZACION_ZAP.md y output/raw/benchmarks/, que el cuerpo invocaba sin listarlos.

de lista y aparecen sangrados 36 pt. Los capítulos 6 y 7 continúan la numeración de la lista de preguntas de investigación, con lo que «6. Hipótesis» se lee en la página 11 como una sexta pregunta.

Los tres índices, correctos en las ciento ocho entradas. Verificadas una por una contra la paginación real. El índice general está íntegro en Times New Roman regular de 11 pt: desapareció la negrita de los capítulos 5, 11, 13 y 17, las versales del 17 y los puntos finales de sus subsecciones.

El capítulo 17 tiene la jerarquía de encabezados invertida. Sus subsecciones de tercer nivel (17.2.1 a 17.2.5) están en cuerpo 14, mayor que el de sus secciones madre (12) e igual al de los títulos de capítulo; y

17. 3, que es de segundo nivel, arrastra ese mismo estilo, por lo que el

índice la anida bajo 17.2.

Las trece tablas cierran por tercera vez consecutiva en el recálculo independiente, incluidas las dos verificaciones cruzadas que el dictamen anterior incorporó: 10 + 15 + 5 = 30 de 17.2.1 contra las tres primeras filas de la Tabla 13, y 75 / 50 / 125 con sus porcentajes de 60 y 40.

Una remisión apunta a una sección que no dice lo que la remisión afirma. El capítulo 7 atribuye a la sección 8.5 la descripción del mecanismo de caché incremental; 8.5 trata del Pipeline Pattern y del principio de responsabilidad única, y no menciona el caché.

Los residuos tipográficos señalados se corrigieron en su mayoría. Desaparecieron los dos puntos huérfanos (cierre de 9.1 y del Anexo G), el Resumen cierra con punto, el epígrafe de la Figura 3 ampliada está anclado a su figura y las figuras del Anexo H ya no se cortan en el margen.

Residuos de acabado. El párrafo de comentario de la Tabla 13 sigue íntegro en cursiva; los títulos A.1–A.3 y el del Anexo H conservan estilos ajenos al resto de los anexos; la Figura 4 ampliada tiene exactamente el tamaño de la del cuerpo; ninguna de las veintiséis referencias lleva sangría francesa; y la cita «(Faraday, 2025)» no coincide con su entrada «Faraday Security».

Balance de subsanación

Origen del punto pendiente Total Subsanados Parciales No subsanados

Condición previa a la presentación (tres componentes) 3 3 — —

Correcciones recomendadas antes de la defensa 7 3 3 1

Hallazgos abiertos de la instancia anterior (S1–S11) 11 7 3 1

Total 21 13 (62 %) 6 (29 %) 2 (9 %)

Sobre la lectura de este balance. Las correcciones recomendadas 2, 4 y 5 y los hallazgos S6, S8 y S9 describen el mismo conjunto de residuos de acabado desde los dos registros que el dictamen anterior usó, de modo que los seis «parciales» corresponden en rigor a tres conjuntos de residuos, no a seis problemas distintos. El porcentaje de cierre pleno es el más bajo de las dos últimas instancias, y sin embargo la distancia real al documento terminado es la más corta de la serie: lo que quedó parcial son residuos tipográficos, y los tres puntos que bloqueaban la presentación están cerrados.

Lo que corresponde reconocer. El dictamen anterior dijo que lo que faltaba era «una frase, un número y un recorte», y que corregidos S1, S2 y S3 el documento se ubicaría alrededor de 8,2. Los autores hicieron esas tres operaciones y además resolvieron S4, S5, S7 y S10, que eran las que el dictamen dejaba para después de la defensa. La reparación de S1 merece un párrafo propio: en lugar de retocar los cuarenta minutos para que encajaran con el techo de diez —que era la salida fácil y la falsa—, agregaron a la nota de trazabilidad la declaración de la configuración con que esa sesión efectivamente corrió. Es exactamente la operación correcta: no cambia un dato, explica por qué el dato es el que es, y de paso convierte una contradicción aparente en una nota metodológica defendible.

Por qué, aun así, queda una corrección previa. Porque un tribunal que abra el documento encuentra en la portada una frase cortada a mitad, en la página 11 un capítulo que se lee como la sexta pregunta de investigación, y en la página 24 una lista de ocho pasos que empieza en el número cinco. Ninguno de los tres es un error de contenido y los tres se arreglan en menos de un cuarto de hora, pero los tres se ven antes de que nadie lea una tabla. Este tribunal deja constancia expresa de que T2, T3 y T4 no son defectos introducidos en esta entrega: estaban en el documento y no fueron detectados antes porque ninguna instancia de la serie había auditado los estilos de encabezado y la numeración automática dentro del cuerpo. T1, en cambio, sí es una regresión de esta entrega.

### 2. Verificación de la condición previa

Componente Estado Verificación en la entrega

Agregar a la nota de trazabilidad del capítulo 17 una oración que declare con qué configuración corrió la sesión del 4 de agosto, de modo que sus 40 minutos de Active Scan dejen de contradecir el techo de 10 minutos de

14. 4 y los 14 minutos de la Tabla 10.

Cumplida La nota declara hoy que la sesión «se ejecutó con la configuración de herramientas previa al ajuste de rendimiento y timeouts descripto en la sección 14.4 (ZAP con 2 hilos concurrentes y sin límite de tiempo por regla ni por escaneo)» y que «por eso el Active Scan de esta sesión insumió 40 minutos, cifra que no es comparable con el techo de 10 minutos ni con los 14 minutos del pipeline completo medidos en la Tabla 10». Es la reparación pedida, con la cifra y la sección nombradas. La declaración es además coherente con 14.4, que atribuye a la configuración conservadora dos hilos y ausencia de límite por regla.

Unificar el valor de --threads de SQLMap entre 12.6 y 14.4, e incorporar --smart al comando de

12. 6 si efectivamente se usa.

Cumplida La sección 12.6 transcribe hoy: --batch, --flush-session, --forms, --dbms=MySQL, -level=1, --risk=3, --threads=10, --smart, --technique=BEUST y -o. La sección 14.4 declara --threads=10 y --smart. Coinciden en el número y en la bandera. Se optó por el valor 10, que es el que 14.4 justificaba como parte del ajuste de rendimiento: la elección es la coherente.

Suprimir de 17.3 el denominador de «treinta y siete alertas», que pertenece a una corrida que el propio capítulo declara ajena, o reemplazarlo por el de su propia sesión.

Cumplida El párrafo de cierre lee hoy: «la validación manual cubrió cinco vectores puntuales de esta sesión (reconocimiento de rutas, inyección de comandos, inyección SQL, XSS reflejado e inclusión local de archivos)». El denominador ajeno desapareció y los cinco vectores quedan enumerados y verificables contra 17.2.1 a 17.2.5. El capítulo 17 ya no se contradice consigo mismo.

Nota. Con estas tres reparaciones cierra el último residuo de la contradicción Q2 de la cuarta instancia, que atravesó cuatro dictámenes. No queda hoy, en el cuerpo del documento, una sola cifra que este tribunal haya podido poner en contradicción con otra cifra del mismo documento.

### 3. Verificación de las correcciones recomendadas

Dictamen de Séptima Corrección · Orquestador de Seguridad · UTN FRM Página 2 de 8

Corrección recomendada Estado Verificación en la entrega

Reproducibilidad. Reescribir con doble guion las banderas de

12. 6 y 14.4, y resolver el

volumen del servicio app.

Subsanada Las dos. Las nueve banderas figuran con doble guion en ambas secciones, verificado sobre los spans del archivo y no sobre la apariencia: el comando es hoy copiable y ejecutable. El volumen se resolvió a favor de 12.1 (.:/app) y —lo que el dictamen anterior pedía como alternativa— el árbol del Anexo A.1 se ajustó en consecuencia: n8n/ y frontend/ figuran hoy fuera de orquestador-seguridad/, de modo que los tres montajes../n8n/data,../n8n/flujo.json y../n8n/init-n8n.sh resuelven contra directorios que el árbol declara. El archivo levanta y su documentación lo acompaña.

Anexo H. Reducir la escala de las Figuras 2 y 4 ampliadas, anclar el epígrafe de la Figura 3 y unificar el título del Anexo H y de A.1 a A.3 con el estilo de los demás anexos.

Parcial Dos de tres. Las Figuras 2 y 4 ampliadas ya no se cortan: el bloque DVWA y la columna N8N están hoy completos dentro de la página. El epígrafe de la Figura 3 ampliada está en la misma página que su figura. Los títulos no se unificaron: A.1, A.2 y A.3 siguen en Times New Roman Bold de 14 pt subrayado frente a los Calibri Bold de 13 pt de los Anexos A a G, y el rótulo del Anexo H sigue en cuerpo 20. Aparecen además dos efectos nuevos de la reescala (véase T6).

Índice. Quitar la negrita a los capítulos 5, 11, 13 y 17, pasar el título del 17 a caja normal, quitar el punto final a sus subsecciones y actualizar el campo.

Subsanada Las cuatro operaciones. Las ochenta y siete entradas del índice general están hoy en Times New Roman regular de 11 pt sin excepción; el título del capítulo 17 figura en caja normal en el índice y en el cuerpo; y sus subsecciones se numeran sin punto final, como el resto del documento. El campo se actualizó: las ciento ocho entradas de los tres índices coinciden con la paginación real.

Residuos. Los dos puntos huérfanos, el punto final del Resumen, la tipografía del párrafo de comentario de la Tabla 13 y el cuerpo menor en dos entradas del índice de tablas.

Parcial Tres de cinco. No queda un solo punto huérfano en las sesenta y tres páginas del archivo: los de 9.1 y del Anexo G desaparecieron. El Resumen cierra con punto, como su Abstract. La entrada de la Tabla 3 en el índice de tablas quedó a cuerpo uniforme. Persisten: el párrafo que comenta la Tabla 13, que sigue íntegro en Calibri cursiva de 11 pt frente al Calibri redonda del resto del cuerpo —es el residuo de R7, abierto desde la quinta instancia—, y la entrada de la Tabla 6, que conserva la segunda mitad de su título en cuerpo 11 sobre un índice a cuerpo 12.

Referencias. Unificar «TheHive Project» / «StrangeBee», restituir la sangría francesa de Alsaedi et al. y emparejar el interlineado de la lista.

Parcial Dos de tres, con un efecto lateral. La entrada lee hoy «TheHive Project. (2025). TheHive documentation», alfabetizada bajo la T y coincidente con la cita de la nota de la Tabla 1: el desajuste se resolvió. El interlineado quedó uniforme: 13,4 pt dentro de cada entrada y 22,4 pt entre entradas, sin excepciones. La sangría francesa, en cambio, no se restituyó en Alsaedi sino que se eliminó del resto: las veintiséis entradas arrancan hoy todas sus líneas en el mismo punto (108 pt), de modo que la lista es uniforme pero ya no cumple la sangría francesa que exige APA. Aparece además el desajuste Faraday (véase T8).

Trazabilidad. Incorporar al árbol del Anexo A.1 el OPTIMIZACION_ZAP.md y el directorio output/raw/benchmarks/.

Subsanada Los dos. El árbol lista hoy OPTIMIZACION_ZAP.md con su comentario y output/{raw/{benchmarks/}, reports/}. Todo archivo que el cuerpo invoca como evidencia —14.2 para la documentación de optimización, 14.3 para los benchmarks— figura en la estructura documentada.

Aparato. Consignar el nombre del tutor. No subsanada Séptima instancia consecutiva. La fórmula institucional no solo sigue sin resolverse: en esta entrega quedó truncada. Véase T1.

### 4. Verificación de los hallazgos abiertos de la instancia anterior

Hallazgo Sev. Estado Verificación

S1 · El capítulo 17 asigna 40 minutos al escaneo activo que 14.4 acotó en 10 Alto Subsanada La nota de trazabilidad declara la configuración previa al ajuste y nombra las tres cifras. La contradicción se explica sin modificar ningún dato.

S2 · 12.6 y 14.4 declaran distinta cantidad de hilos para SQLMap Medio Subsanada --threads=10 en ambas, y --smart incorporada al comando de 12.6.

S3 · La cobertura manual de 17.3 se calcula sobre el total de alertas de otra corrida Medio Subsanada El denominador de treinta y siete alertas fue suprimido y reemplazado por la enumeración de los cinco vectores de la propia sesión.

S4 · El volumen del servicio app no coincide entre el Anexo A.2 y 12.1 Medio Subsanada.:/app en A.2, coincidente con 12.1, y el árbol de A.1 reubica n8n/ y frontend/ fuera de la raíz, con lo que los montajes../n8n/… resuelven. El conjunto es hoy internamente coherente.

S5 · Las banderas de línea de comandos figuran con guion largo Medio Subsanada Las nueve banderas con doble guion en 12.6 y 14.4, verificado sobre los caracteres del archivo.

S6 · Figuras del Anexo H cortadas en el margen y epígrafe separado de su figura Bajo Parcial Los cortes desaparecieron y el epígrafe de la Figura 3 está anclado; el epígrafe de la Figura 1 ampliada coincide hoy con el índice de figuras. Quedan dos efectos de la reescala: la Figura 1 ampliada ocupa el ancho completo de la hoja, invadiendo ambos márgenes, y la Figura 4 ampliada tiene exactamente las mismas dimensiones que la del cuerpo. Se consigna en T6.

S7 · Cuatro entradas del índice general en negrita, versales y puntos finales del capítulo 17

Bajo Subsanada Índice íntegro en Times New Roman regular de 11 pt; el título del 17 en caja normal; sus subsecciones sin punto final.

S8 · Residuos tipográficos aislados Bajo Parcial Tres de cinco. Cerrados: los dos puntos huérfanos y el punto final del Resumen. Abiertos: la cursiva del párrafo de la Tabla 13 y el cuerpo menor de la entrada de la Tabla 6 en el índice de tablas; los estilos de A.1–A.3 y del Anexo H se consignan en T7.

S9 · Una cita no coincide con su entrada bibliográfica Bajo Parcial El caso señalado quedó resuelto y el interlineado es uniforme. La sangría francesa se eliminó en lugar de restituirse, y aparece un segundo desajuste cita-entrada del mismo tipo (T8).

Dictamen de Séptima Corrección · Orquestador de Seguridad · UTN FRM Página 3 de 8

S10 · Dos archivos citados en el cuerpo no figuran en la estructura del Anexo A.1 Bajo Subsanada Los dos incorporados al árbol, con comentario en el caso de OPTIMIZACION_ZAP.md.

S11 · El nombre del tutor sigue sin consignarse Bajo No subsanada Séptima instancia consecutiva, y esta vez con la fórmula truncada. Véase T1.

4. 1 Verificación aritmética independiente

Este tribunal recalculó las trece tablas cuantitativas. Las trece cierran. Es la tercera instancia consecutiva en que ocurre, y la primera en que ninguna de ellas contradice además a ninguna otra sección del documento.

Tabla Verificación Resultado

Tablas 1 y 2 Cualitativas: cuatro plataformas contrastadas y cinco componentes, coincidentes con los cinco servicios del Anexo A.2 ( db, dvwa, zap, app, n8n) y con el comentario del árbol de A.1. Cierra

Tabla 3 (resumen) 24 spider + 8 ffuf + 2 declaradas en la nota = 34 URLs únicas. Coincide con el campo resumen del Anexo D. Cierra

Tabla 4 (alertas ZAP) Ocurrencias: 5+5+5+5+5+5+2+2+1+1+1 = 37. Severidad: Medium 16, Low 14, Informational 7 = 37. Porcentajes 43,2 / 37,8 / 18,9 correctos a una decimal. Cierra

Tabla 5 (rutas ffuf) Ocho rutas, coincidentes con el indicador de la Tabla 3 y con ffuf.rutas del Anexo D. Cierra

Tablas 6 y 7 (SQLMap) Un endpoint confirmado por cuatro técnicas = 4 hallazgos individuales; cinco usuarios volcados. Cierra

Tabla 8 (OWASP) Tres categorías —A01, A03, A05—, coincidentes con la fila combinada de la Tabla 9 y con el cierre de 13.5. Cierra

Tabla 9 (cobertura) 37 alertas de ZAP + 4 hallazgos de SQLMap = 41 combinados; 34 URLs unificadas. Cierra

Tabla 10 (caché) (845,81 − 263,15) / 845,81 = 68,89 %, coincidente con el 68,9 % informado. Los redondeos a «14 min 06 s» y «4 min 23 s» de 15.1 son correctos. El panel de caché cierra: 3 + 5 = 8 URLs. Cierra

Tabla 11 (estabilidad) 57/59 = 96,6 %; 52/54 = 96,3 %. Composición: 59 − 54 = 5 y 57 − 52 = 5, declaradas en la nota. Cierra

Tabla 12 (objetivos) Nueve objetivos específicos, ocho cumplidos y uno parcial, coincidente con el listado de 4.2, que enumera efectivamente nueve. Cierra

Tabla 13 (cap. 17) Filas: 10+5+15+55+30+10 = 125. Columnas: automatizado 5+10+40+20 = 75; manual 10+5+15+10+10 = 50. 75 + 50 = 125; 75/125 = 60 %, 50/125 = 40 %. El desglose de 17.2.1 (10 + 15 + 5 = 30) cierra contra las tres primeras filas, y los tiempos manuales de 17.2.2 a 17.2.5 (10 + 5 + 10 + 10) cierran contra las filas 4 a 6.

Cierra

Levantamiento de la advertencia sobre la Tabla 13. El dictamen anterior consignó que la tabla cerraba consigo misma pero no contra el capítulo

14. Con la nota de trazabilidad incorporada en esta entrega, los cuarenta minutos de la fila del Active Scan tienen una explicación declarada en el

propio documento y dejan de contradecir el techo de 14.4 y los catorce minutos de la Tabla 10. La advertencia queda levantada.

4. 2 Verificación del índice y de las remisiones

Se cotejaron las ciento ocho entradas de los tres índices contra la paginación impresa del propio archivo —no contra el índice— y todas coinciden: las cinco entradas preliminares, las diecinueve de capítulo, las cincuenta y cinco de subsección y las ocho de anexo del índice general, las ocho del índice de figuras y las trece del índice de tablas. Se comprobó, entre otras, que el capítulo 13 abre en la página 32, el 17 en la 47, las Referencias en la 50, los Anexos en la 52 y el Anexo H en la 58, y que las cuatro figuras del cuerpo están en las páginas 22, 23, 25 y 26 que el índice de figuras anuncia.

Se inventariaron además todas las remisiones internas del cuerpo —a capítulos, secciones, tablas, figuras y anexos— y se resolvieron una por una contra los títulos y rótulos a los que apuntan. Ninguna cuelga. La única defectuosa no es una remisión rota sino una remisión equivocada: la del capítulo 7 a la sección 8.5, que se consigna en T5.

### 5. Hallazgos de la presente instancia

T1 · La fórmula del tutor quedó truncada en la portada Medio La portada lee «Tutor: A designar por la coordinación académica antes». Falta el complemento «de la presentación», con lo que la línea termina en una preposición y la frase queda sin cerrar. Este tribunal admitió en instancias anteriores la fórmula institucional completa como salida válida frente a la ausencia del nombre; una fórmula cortada a mitad no es esa salida: es un error de tipeo en la primera página del trabajo, y es lo primero que el tribunal de defensa va a leer. Es una regresión de esta entrega: la versión evaluada en la sexta instancia llevaba la fórmula completa. La reparación son tres palabras. Conviene además aprovechar la misma pasada para un detalle contiguo: en la línea institucional, «Tecnicatura» está en negrita y «Universitaria en Programación» no, herencia del mismo rótulo en negrita que encabeza cada campo de la portada.

T2 · La lista de pasos de la sección 11.4 está numerada de 5 a 12 Medio La sección 11.4 «Flujo de Datos Detallado» presenta el ciclo de vida completo de un análisis en ocho pasos. Esos ocho pasos aparecen numerados 5, 6, 7, 8, 9, 10, 11 y 12: la lista continúa la numeración de la enumeración de cuatro capas de la sección

11. 1 en lugar de reiniciar en uno. El efecto en la página 24 es que el lector encuentra un procedimiento que empieza en el paso

cinco sin que existan los pasos uno a cuatro.

El defecto es doblemente inoportuno porque 11.4 es la sección que la Tabla 12 declara como evidencia del cumplimiento del objetivo específico 1, y la que el Anexo H y la propia Figura 1 invocan por su número. La reparación es marcar la lista y elegir «reiniciar numeración en 1». Conviene revisar en la misma pasada que los numerales de la lista están en Times New Roman mientras el texto de los ítems está en Calibri, desajuste que se repite en otras listas del documento.

Dictamen de Séptima Corrección · Orquestador de Seguridad · UTN FRM Página 4 de 8

T3 · Cuatro títulos de capítulo están construidos como ítems de una lista automática Medio Los títulos de los capítulos 6 (Hipótesis), 7 (Estado del Arte), 8 (Marco Teórico y Conceptual) y 9 (Alcances y Limitaciones) no llevan su número en el texto: lo reciben de un campo de numeración automática, y su texto arranca a 108 pt del borde, es decir, sangrado 36 pt respecto del margen en el que están todos los demás títulos de capítulo. El numeral se compone además en un cuerpo y una tipografía distintos de los del título.

La consecuencia visible está en la página 11: la lista numerada de preguntas de investigación termina en el ítem 5 «(PI5) ¿Puede un sistema de este tipo extenderse…?» y a continuación, con la misma sangría y el mismo formato de numeral, aparece «6. Hipótesis». Un lector desprevenido lee ahí una sexta pregunta de investigación. Lo mismo ocurre dos páginas después con «7. Estado del Arte».

El mismo mecanismo produce dos variantes menores en el resto del documento: los capítulos 1 y 2 llevan su numeral en un span separado con un carácter invisible intercalado —y el capítulo 1 queda además sangrado 18 pt respecto de los demás—, y el capítulo 10 compone su «10.» en Times New Roman de 12 pt mientras el texto «Metodología» va en Calibri Bold de 14 pt. En total, cinco tratamientos distintos para un mismo nivel de encabezado. La reparación es seleccionar los siete títulos afectados y aplicarles el mismo estilo que ya tienen los capítulos 3, 4, 5, 11 a 19, con el número escrito en el texto. El índice, que hoy los muestra correctamente porque toma el número del campo, seguirá mostrándolos bien.

T4 · El capítulo 17 tiene la jerarquía de encabezados invertida y el índice anida 17.3 bajo 17.2 Medio En todo el documento, las secciones de segundo nivel se componen en cuerpo 12: así están 4.1, 8.1 a 8.6, 10.1 a 10.6, 11.1 a 11.5,

12. 1 a 12.10, 13.1 a 13.5, 14.1 a 14.6 y 15.1 a 15.2, y así están también 17.1 y 17.2. Las subsecciones de tercer nivel del capítulo 17

—17.2.1 a 17.2.5— están, en cambio, en cuerpo 14: más grandes que sus propias secciones madre e iguales a los títulos de capítulo. La jerarquía se lee al revés de como está.

De ese mismo estilo se deriva un efecto en el índice. La sección 17.3 «Conclusiones sobre la Metodología de Validación», que es de segundo nivel y cierra el capítulo, arrastra el estilo de tercer nivel de las 17.2.x, de modo que el índice la lista con la sangría de 108 pt de las subsecciones y la anida visualmente bajo 17.2. Quien lea el índice entenderá que las conclusiones metodológicas del capítulo son una subsección de los procedimientos por vector de ataque, cuando son su cierre. Es el último resto del bloque de estilos que el capítulo 17 arrastra desde su incorporación. La reparación son dos operaciones: aplicar a 17.2.1–17.2.5 el estilo de tercer nivel correcto y a 17.3 el mismo estilo de segundo nivel que tienen 17.1 y 17.2, y actualizar el campo.

T5 · Una remisión atribuye a la sección 8.5 un contenido que esa sección no tiene Medio El capítulo 7 (Estado del Arte), al comentar a Zhang et al. (2023), afirma que el problema de eficiencia que esos autores abordan es «análogo al que este proyecto aborda mediante el mecanismo de caché incremental descripto en la sección 8.5». La sección 8.5 es «Pipeline de Datos y Arquitectura Modular» y trata del Pipeline Pattern de Buschmann et al. y del principio de responsabilidad única de Martin: no menciona el caché incremental en ninguna línea.

No es una remisión rota —8.5 existe— sino una remisión equivocada, que es más difícil de detectar y más incómoda de encontrar en la defensa. El mecanismo de caché incremental se describe en 11.1 (capa de persistencia), se implementa en 12.5 y 12.6 y se mide en 14.3. La reparación es reemplazar «8.5» por la sección que corresponda; si la intención era remitir al lugar donde el caché se mide, «14.3» es la remisión correcta, y si era al lugar donde se describe, «11.1».

T6 · El Anexo H no amplía la Figura 4 y la Figura 1 ampliada invade ambos márgenes Bajo El Anexo H existe, según su propio párrafo de apertura, «para su mejor observación» de las Figuras 1 a 4. Medidas las cajas de imagen contra las del cuerpo, el resultado es desparejo. La Figura 1 pasa de 414 × 369 pt a 612 × 575, la Figura 2 de 420 × 296 a 487 × 362 y la Figura 3 de 416 × 583 a 450 × 630. La Figura 4 ampliada mide 487 × 397 pt, exactamente lo mismo que la Figura 4 del cuerpo: no está ampliada. Como es el diagrama de secuencia UML —el de rótulos más pequeños y el que el tribunal más va a necesitar leer—, es precisamente la figura para la que el anexo se creó.

En sentido contrario, la Figura 1 ampliada ocupa los 612 pt de ancho de la hoja, es decir que se extiende hasta los dos bordes físicos de la página e invade por completo ambos márgenes, mientras el resto del documento respeta una caja de texto de 72 a 540 pt. Las Figuras 2 y 4 ampliadas, por su parte, dejan libre cerca del cuarenta por ciento de la altura de su página. La reparación es escalar las Figuras 2 y 4 para que aprovechen el alto disponible y devolver la Figura 1 a la caja de texto.

T7 · Estilos del capítulo de anexos sin unificar Bajo Conviven en el capítulo 19 cinco criterios distintos para elementos del mismo rango. Los rótulos «Anexo A» a «Anexo G» van en Calibri Bold de 13 pt; el del Anexo H, en Calibri Bold de 20 pt y subrayado. Los apartados A.1, A.2 y A.3 van en Times New Roman Bold de 14 pt subrayado, única aparición de esa familia tipográfica en un título del documento. La nota de seguridad del Anexo A.2 va en Times New Roman de 11 pt, mientras las restantes notas de tabla y de figura del documento van en Calibri cursiva de 10 pt. Los epígrafes de las cuatro figuras del Anexo H van en Calibri redonda, mientras los de las mismas figuras en el cuerpo van en Calibri cursiva. Y el título «19. Anexos Técnicos» usa un azul (#366091) distinto del que comparten los otros dieciocho títulos de capítulo (#4E80BC).

Ninguno de los cinco afecta al contenido y los cinco se resuelven aplicando a cada elemento el estilo que su equivalente ya tiene en el resto del documento.

T8 · Referencias: un segundo desajuste cita-entrada y la sangría francesa eliminada Bajo La nota de la Tabla 1 cita «(Faraday, 2025)» y la entrada correspondiente del capítulo 18 es «Faraday Security. (2025)». Es exactamente el mismo desajuste que la instancia anterior señaló para TheHive y que los autores corrigieron: el elemento inicial de la entrada debe coincidir con el que la cita nombra, porque es el que permite localizarla. Se resuelve unificando en una de las dos formas, preferentemente en la de la entrada.

Por separado, la lista quedó con un interlineado impecablemente uniforme —13,4 pt dentro de cada entrada, 22,4 pt entre entradas — pero sin sangría francesa en ninguna de las veintiséis: todas las líneas, primeras y sucesivas, arrancan en 108 pt. El dictamen anterior pedía restituir la sangría perdida en una entrada; la operación resolvió la disparidad eliminándola en todas. La reparación es aplicar a la lista un estilo de párrafo con sangría francesa de 0,5 pulgada, que corrige las veintiséis de una sola vez.

Dictamen de Séptima Corrección · Orquestador de Seguridad · UTN FRM Página 5 de 8

T9 · Residuos de aparato y de acabado Bajo

El párrafo que comenta la Tabla 13 sigue íntegro en Calibri cursiva de 11 pt, frente al Calibri redonda del cuerpo. Es el residuo de R7, abierto desde la quinta instancia, y hoy el único párrafo del documento en esa situación.

En el índice general, «Índice», «Índice de Figuras» e «Índice de Tablas» figuran como entradas de segundo nivel (sangría de 90 pt), es decir, anidadas bajo «Abstract», como si fueran subsecciones suyas.

En el índice de tablas, la entrada de la Tabla 6 conserva la segunda mitad de su título en cuerpo 11 sobre una lista compuesta a cuerpo 12. El rótulo en el cuerpo, en cambio, es uniforme: el desajuste está solo en el campo.

En la sección 15.1, «Verificación por objetivo específico» está construido como una viñeta de lista y no como un título, de modo que no figura en el índice pese a introducir la Tabla 12 y a funcionar como un apartado.

Los títulos 4.1, 4.2, 8.1 a 8.6 y 9.1 arrancan a 66 pt, seis puntos a la izquierda del margen de 72 pt en el que están todos los demás títulos de sección.

En la fila de cierre de la Tabla 13, «125 minutos (~2 horas» se compone en Arial Bold y el paréntesis de cierre en Calibri Bold, único lugar de la tabla donde aparece esa familia.

El árbol del Anexo A.1 lista el archivo como « dockerfile » en minúscula, mientras el Anexo A.3 lo titula «Archivo Dockerfile» y el servicio app del Anexo A.2 usa build:., que en un sistema de archivos sensible a mayúsculas busca Dockerfile. Es una letra, en el único punto del árbol donde la diferencia impide construir la imagen.

El índice de figuras lista la Figura 4 ampliada como «Diagrama de secuencia UML» y su epígrafe la rotula «Diagrama de Secuencia UML»: discrepancia de caja entre el campo y el rótulo.

### 6. Calificación por capítulo

Capítulo Anterior Actual Fundamento

Introducción 7,4 7,3 Contenido sin cambios y sin residuos. Penalizada levemente porque su título es un ítem de lista automática sangrado 18 pt respecto del resto (T3).

Planteo del problema 6,8 6,7 Sin cambios de contenido. Misma penalización de título que la Introducción.

Justificación 6,5 6,5 Sin cambios.

Objetivos 7,6 7,6 Sin cambios. Los nueve objetivos específicos siguen verificados uno por uno en la Tabla 12.

Preguntas de investigación 7,0 7,4 Recuperación. El capítulo etiqueta hoy explícitamente PI1 a PI5, con lo que la sigla «PI4» que el capítulo 14 usa tiene definición en el documento: cae la penalización que este tribunal venía aplicando. Penalizado aún porque el título del capítulo siguiente continúa su numeración de lista (T3).

Hipótesis 7,2 7,0 H1 a H4 sin cambios y coherentes con 14.2, 14.3 y el capítulo 17. Penalizado porque su título se lee como la sexta pregunta de investigación del capítulo anterior (T3).

Estado del arte 8,2 8,0 La Tabla 1 y las cuatro plataformas contrastadas se mantienen. Penalizado por la remisión equivocada a la sección 8.5 (T5) y por el formato de su título (T3).

Marco teórico 8,2 8,1 Las seis subsecciones con anclaje bibliográfico, sin cambios. Penalizado por el formato de su título (T3) y por ser el destino de la remisión de T5.

Alcances y limitaciones 6,9 7,1 Desapareció el punto huérfano del cierre de 9.1 que lo penalizaba. El inventario de limitaciones sigue siendo honesto y completo, e incluye las dos comparaciones que el trabajo no pudo resolver.

Metodología 8,0 7,9 Numeración correlativa y criterios de 10.6 estables. Penalizado por el numeral «10.» del título, compuesto en otra familia y otro cuerpo que el resto (T3).

Arquitectura 8,6 8,2 Único retroceso. El contenido no cambió y las subsecciones 11.2 a 11.5 conservan lo que recuperaron en la instancia anterior, pero la auditoría de numeración de esta instancia detecta que los ocho pasos de 11.4 están numerados de 5 a 12 (T2), en la sección que la Tabla 12 invoca como evidencia del OE1. Sigue siendo, en contenido, uno de los mejores capítulos del trabajo.

Implementación técnica 7,6 8,4 Mayor recuperación de la instancia y máximo histórico del capítulo. Los tres defectos que lo hicieron retroceder en la sexta instancia están resueltos: los hilos coinciden con 14.4, el volumen del servicio app cierra contra el Anexo A y el comando de SQLMap es ejecutable tal como está impreso. La sección del parser de SQLMap sigue siendo la mejor pieza técnica del trabajo.

Resultados 8,4 8,4 Sin cambios. Las seis tablas cierran, la nota metodológica sobre variabilidad entre corridas se mantiene y la trazabilidad a archivos concretos no perdió nada.

Discusión 8,4 8,6 Deja de ser el otro extremo de S1 y S2: 14.4 coincide hoy con 12.6 y el techo de diez minutos convive con los cuarenta del capítulo 17 sin contradecirlos. Es el capítulo mejor calificado del documento.

Conclusiones 8,0 7,9 El contenido no cambió y ninguna remisión cuelga. Penalizado porque «Verificación por objetivo específico» es una viñeta usada como título y no figura en el índice (T9).

Consideraciones éticas 8,2 8,2 Sin cambios. La norma argentina y el código ACM con cita autor-año, y el principio 1.6 invocado desde la nota de la Tabla 7.

Desarrollo experimental (cap. 17) 7,6 8,3 Segunda mayor recuperación. La nota de trazabilidad explica hoy los cuarenta minutos del Active Scan declarando la configuración de la sesión, el denominador ajeno de 17.3 fue suprimido y la aritmética interna cierra contra el texto y contra la Tabla 13. Penalizado por la jerarquía invertida de sus encabezados y por 17.3 anidada en el índice (T4), y por la cursiva del párrafo de comentario de la Tabla 13 (T9).

Referencias 8,6 8,5 El desajuste TheHive / StrangeBee resuelto y el interlineado uniforme en las veintiséis entradas.

Dictamen de Séptima Corrección · Orquestador de Seguridad · UTN FRM Página 6 de 8

Penalizado porque la sangría francesa se eliminó en lugar de restituirse y porque persiste un desajuste cita-entrada del mismo tipo en Faraday (T8).

Anexos 8,4 8,3 El árbol de A.1 incorpora los dos archivos que el cuerpo invocaba y reubica n8n/ y frontend/, con lo que el docker-compose.yml cierra contra su propia documentación. Penalizado por los estilos sin unificar de A.1–A.3 y del Anexo H (T7) y porque la Figura 4 ampliada no amplía (T6).

El promedio simple de las diecinueve notas por capítulo es 7,81. La calificación global se establece en 8,0 / 10, frente al 7,9 del dictamen anterior. El dictamen de sexta corrección proyectó 8,2 para la corrección de S1, S2 y S3; los autores hicieron esas tres y cuatro más, lo que justificaría esa cifra, pero de la proyección se descuentan dos décimas por los defectos de numeración y estilo de encabezado que esta instancia detecta y por la regresión de la portada. Corregidos T1 a T4 —que son tres palabras, un reinicio de lista, siete títulos y dos estilos—, la calificación de este mismo documento se ubicaría alrededor de 8,4.

7. Dictamen final

### APROBADA CON OBSERVACIONES MENORES

8,0 / 10 · La condición previa anterior, cumplida en sus tres componentes · Una condición previa nueva, exclusivamente de numeración y portada, sin escribir contenido

Fundamentación

Esta es la instancia en que las cifras del documento dejaron de ser un problema. No queda un número del trabajo que este tribunal haya podido poner en contradicción con otro: las trece tablas cierran por tercera vez consecutiva, la aritmética interna del capítulo 17 coincide con su texto y con su tabla, el capítulo 14 y el 17 pueden leerse uno después del otro sin que el mismo escaneo dure dos cosas distintas, y el único comando que el documento transcribe se puede copiar y ejecutar. El archivo de despliegue cierra contra la estructura que el propio anexo documenta. Los tres índices son exactos en sus ciento ocho entradas. Ninguna remisión cuelga.

Lo que queda es de una sola naturaleza, y conviene ser franco sobre su origen igual que lo fue el dictamen anterior. Tres de los cuatro puntos de la condición previa —la numeración de la lista de 11.4, los títulos de capítulo construidos como ítems de lista y la jerarquía invertida del capítulo 17— no los introdujeron los autores en esta entrega: estaban en el documento y aparecen ahora porque esta es la primera instancia de la serie que audita los estilos de encabezado y la numeración automática dentro del cuerpo, y no solo su reflejo en el índice. El cuarto, la fórmula del tutor cortada a mitad de frase, sí es una regresión de esta entrega, y es la razón por la que el punto que atraviesa las siete instancias sin cerrarse está hoy peor que en la sexta.

Conviene decir dónde está este trabajo. Siete dictámenes atrás tenía resultados con URLs ficticias, ninguna bibliografía académica, ninguna figura y conclusiones que contradecían a la discusión. Hoy tiene tres corridas datadas y trazables a archivos nombrados, veintiséis fuentes citadas y verificadas una por una contra el cuerpo, un marco teórico anclado subsección por subsección, ocho figuras con anexo propio, trece tablas que cierran, un archivo de despliegue que levanta con un comando y que coincide con su documentación, un capítulo de ética que aplica el código ACM al caso concreto de los datos que su propio sistema persiste, un capítulo de validación manual con payloads y evidencia que ningún dictamen pidió, y un inventario de limitaciones que declara con nombre y apellido las dos comparaciones que el trabajo no logró resolver en lugar de disimularlas. Está en condiciones de defenderse. Le falta que el procesador de texto numere las cosas como el documento las ordena.

Condición previa a la presentación (una: cuatro operaciones de numeración y portada)

Ninguna de las cuatro exige escribir contenido, medir nada ni tocar una cifra o una tabla. En conjunto son menos de un cuarto de hora de trabajo.

Portada. Restituir la fórmula completa: «A designar por la coordinación académica antes de la presentación». Son tres palabras, y es la primera línea que el tribunal lee.

Sección 11.4. Reiniciar la numeración de la lista de pasos en 1, de modo que el ciclo de vida del análisis se enumere de 1 a 8 y no de 5 a 12.

Títulos de capítulo. Sacar los títulos de los capítulos 6, 7, 8 y 9 de la lista automática que los numera y sangra, y aplicarles — junto con los de los capítulos 1, 2 y 10— el mismo estilo que ya tienen los capítulos 3, 4, 5 y 11 a 19, con el número escrito en el texto. El objetivo mínimo es que «6. Hipótesis» y «7. Estado del Arte» dejen de leerse como ítems de la lista de preguntas de investigación.

Capítulo 17. Aplicar a 17.2.1–17.2.5 un estilo de tercer nivel de cuerpo menor que el de sus secciones madre, y a 17.3 el mismo estilo de segundo nivel que tienen 17.1 y 17.2, de modo que el índice deje de anidarla bajo 17.2. Actualizar el campo del índice después de las cuatro operaciones.

Correcciones recomendadas antes de la defensa

Remisión. Corregir en el capítulo 7 la remisión a la «sección 8.5» por la sección donde el caché incremental efectivamente se describe (11.1) o se mide (14.3).

Anexo H. Escalar las Figuras 2 y 4 ampliadas para que aprovechen el alto disponible de su página —la Figura 4 hoy no está ampliada en absoluto— y devolver la Figura 1 ampliada a la caja de texto, de la que hoy sale por ambos márgenes.

Estilos de anexos. Unificar los títulos A.1 a A.3 y el rótulo del Anexo H con el estilo de los Anexos A a G; llevar la nota del Anexo A.2 al estilo de nota del resto del documento; poner en cursiva los epígrafes de las figuras del Anexo H, como los del cuerpo; y unificar el color del título del capítulo 19 con el de los otros dieciocho.

Referencias. Unificar «Faraday» / «Faraday Security» entre la cita de la nota de la Tabla 1 y la entrada bibliográfica, y aplicar a la lista completa un estilo con sangría francesa.

Residuos. Quitar la cursiva al párrafo de comentario de la Tabla 13; convertir «Verificación por objetivo específico» en título de sección; llevar «Índice», «Índice de Figuras» e «Índice de Tablas» al primer nivel del índice; corregir el cuerpo menor de la

Dictamen de Séptima Corrección · Orquestador de Seguridad · UTN FRM Página 7 de 8

entrada de la Tabla 6; alinear a 72 pt los títulos 4.1, 4.2, 8.1–8.6 y 9.1; unificar la tipografía de la fila de cierre de la Tabla 13.

Reproducibilidad. Escribir «Dockerfile» con mayúscula inicial en el árbol del Anexo A.1, para que coincida con el build:. del Anexo A.2 y con el título del Anexo A.3.

Aparato. Consignar el nombre del tutor, séptima instancia consecutiva en que la portada no lo responde y primera en que además no cierra la frase.

Preguntas previsibles del tribunal

«El escaneo activo, ¿tarda cuarenta minutos o diez?» — Tiene respuesta y está escrita. La nota de trazabilidad del capítulo 17 lo explica en una oración. Es la pregunta que dejó de ser un problema en esta entrega.

«¿SQLMap corre con cinco hilos o con diez?» — Con diez, en las dos secciones que lo declaran, y con --smart.

«Los cinco vectores validados a mano, ¿sobre qué total se calculan?» — Sobre los cinco de la propia sesión, enumerados.

«¿Podemos levantar el entorno con el archivo del Anexo A?» — Sí. El YAML está en un único bloque, los cinco servicios son los que la Tabla 2 declara y los volúmenes cierran contra el árbol de A.1. El único obstáculo residual es la minúscula de dockerfile en el árbol.

«La sección 11.4, ¿por qué empieza en el paso cinco?» — Es la primera pregunta de forma si la condición previa no se ejecuta, y no tiene una buena respuesta que no sea «es un error de la lista».

«¿Hipótesis es el capítulo 6 o la pregunta de investigación 6?» — Es el capítulo 6. El documento, tal como está compuesto, no lo deja claro en la página 11.

«El timeout de SQLMap es de 300 segundos según 12.3, pero la Tabla 13 le asigna veinte minutos. ¿Cómo se concilia?» — Se concilia: 300 segundos es el tope por invocación y la sesión atacó varias URLs candidatas en segundo plano. No es una contradicción, pero conviene tener la respuesta preparada porque las dos cifras conviven en el documento sin una frase que las relacione.

Cierre

La instancia anterior cerró diciendo que faltaba «una frase, un número y un recorte». Se hicieron las tres, y se hicieron bien: la que más valor tiene es la primera, porque los autores eligieron explicar por qué un dato era el que era en lugar de retocarlo para que encajara, que es la diferencia entre un informe técnico y un informe complaciente. Lo que queda ahora ya no es coherencia sino numeración: cuatro operaciones de estilo en un documento cuyo contenido, cifras, tablas, referencias y remisiones este tribunal da por verificados. Es la distancia más corta de las seis instancias anteriores, y por primera vez en la serie no hay nada pendiente que exija volver a medir, volver a correr, volver a redactar ni volver a pensar: solo hay que hacer que el índice automático y las listas numeradas digan lo que el documento ya dice.

Nota de alcance. Esta evaluación se basa en el cotejo entre el archivo V14 entregado y el Dictamen de Sexta Corrección, complementado con: recálculo independiente de la aritmética de las trece tablas; verificación entrada por entrada de los tres índices contra la paginación real del archivo; inventario y resolución de todas las remisiones internas contra los títulos y rótulos del cuerpo; cotejo de las veintiséis entradas bibliográficas contra el cuerpo del texto; cotejo cruzado de los parámetros de configuración declarados en 12.1, 12.3, 12.6, 14.4 y en el capítulo 17; verificación del dockercompose.yml del Anexo A contra la estructura declarada en el Anexo A.1; auditoría de estilos de encabezado, familias tipográficas, cuerpos y numeración automática dentro del cuerpo del documento; y medición de las cajas de las ocho figuras contra la caja de texto de la página. Corresponde una aclaración sobre los hallazgos T2, T3, T4, T5 y parte de T7 y T9: se refieren a defectos preexistentes que las instancias anteriores no detectaron, no a regresiones introducidas en esta entrega; se consignan ahora porque esta es la primera verificación de la serie que audita los estilos y la numeración en el cuerpo y no solo su reflejo en el índice. T1 sí es una regresión de esta entrega. No incluye la ejecución ni la auditoría del código del repositorio, ni la reproducción del entorno de laboratorio, ni la comprobación de que los archivos resultado_unificado.json, resultado_sin_cache.json, resultado_con_cache.json, reporte_seguridad.md y sqlmap_bg.log contengan efectivamente los datos citados, ni la verificación de que la sesión manual del 4 de agosto de 2026 se haya realizado en las condiciones que su nota de trazabilidad declara. Las referencias verificadas en instancias anteriores no se reverificaron en su contenido editorial. Los estados de subsanación consignan lo que el texto entregado permite verificar. Las calificaciones numéricas reflejan un juicio experto orientado a asistir a los autores y no constituyen una nota oficial de la institución.

Dictamen de Séptima Corrección · Orquestador de Seguridad · UTN FRM Página 8 de 8