# Auditoría Comparativa de Dictámenes (D7 vs. D8) y Plan Maestro de Subsanación para Informe v16
**Universidad Tecnológica Nacional — Facultad Regional Mendoza**  
*Tecnicatura Universitaria en Programación (TUP)*  
**Trabajo Final de Grado:** *Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web*  
**Autores:** Tomas Mastropietro · Cristian Krahulik · Juan Segura  
**Directores Consignados:** Alberto Cortez · Ariel Enferrel  
**Fecha de Auditoría:** 24 de septiembre de 2026  
**Documento Fuente de Planificación:** `docs/plan/plan-v16.md`

---

## PARTE I: ANÁLISIS COMPARATIVO RIGUROSO (DICTAMEN 7 vs. DICTAMEN 8)

### 1. Identificación y Metadatos Institucionales

| Parámetro / Entidad | Dictamen Anterior ($D_{7}$) | Dictamen Reciente ($D_{8}$) | Variación / Observación |
| :--- | :--- | :--- | :--- |
| **Fecha de Dictamen** | Instancia de Séptima Corrección | Instancia de Octava Corrección | Avance correlativo |
| **Documento Evaluado** | Archivo V14 (62 págs. num. + portada = 63 págs.) | Archivo V15 (62 págs. num. + portada = 63 págs.) | Mismo volumen físico; optimización estructural |
| **Dictamen de Referencia** | Dictamen de Sexta Corrección ($D_{6}$) | Dictamen de Séptima Corrección ($D_{7}$) | Trazabilidad histórica completa |
| **Calificación Global** | **8,0 / 10** | **8,4 / 10** | **Incremento de +0,4 puntos** |
| **Veredicto Formal** | Aprobada con observaciones menores | Aprobada con observaciones menores | Se mantiene el dictamen aprobatorio |
| **Condición Previa** | **Existente (Bloqueante):** 4 operaciones de estilo (T1–T4) | **SIN Condición Previa Bloqueante:** Cumplida al 100% (4/4) | **Hito institucional: Habilitada para presentación** |
| **Registro de Tutores** | Sin consignar / Fórmula truncada (Regresión) | Consignados: «Alberto Cortez y Ariel Enferrel» | Subsanación plena de aparato histórico (T1) |
| **Naturaleza de Pendientes** | Estilos de encabezado, portada y listas | Residuos de acabado, caja de Anexo H y tipografía | Cero observaciones de contenido o matemáticas |

---

### 2. Matriz Evolutiva de Calificaciones (19 Capítulos y Global)

Se presenta a continuación la contrastación cuantitativa exhaustiva capítulo por capítulo, evaluando la variación delta ($\Delta$) y el fundamento emitido por el tribunal evaluador:

| Cap. | Nombre del Capítulo | Nota $D_{7}$ | Nota $D_{8}$ | Variación ($\Delta$) | Fundamento del Tribunal y Factores Determinantes |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1** | Introducción | 7,3 | **7,4** | $+0,1$ | Menos penalizada al corregirse títulos generales; resta numeral partido y sangría de 18 pt (U4). |
| **2** | Planteo del Problema | 6,7 | **6,9** | $+0,2$ | Título colocado al margen correcto; resta corregir numeral partido por carácter invisible (U4). |
| **3** | Justificación | 6,5 | **6,5** | $0,0$ | Sin modificaciones en esta entrega. Estable. |
| **4** | Objetivos | 7,6 | **7,6** | $0,0$ | Contenido y 9/9 OE verificados en Tabla 12. Resta alinear 4.1 y 4.2 a 72 pt (T9). |
| **5** | Preguntas de Investigación | 7,4 | **7,6** | $+0,2$ | El título del Cap. 6 dejó de continuar su lista; desaparece la penalización cruzada. |
| **6** | Hipótesis | 7,0 | **7,4** | $+0,4$ | «6. Hipótesis» ya no se confunde con una sexta pregunta de investigación (T3 resuelto). |
| **7** | Estado del Arte | 8,0 | **8,4** | $+0,4$ | Fuerte recuperación: remisión corregida a sección 11.1 (T5) y título en estilo normalizado (T3). |
| **8** | Marco Teórico y Conceptual | 8,1 | **8,4** | $+0,3$ | Título normalizado (T3) y deja de ser destino de una remisión errónea sobre caché (T5). |
| **9** | Alcances y Limitaciones | 7,1 | **7,3** | $+0,2$ | Título en estilo correcto; resta alinear sangría de 9.1 a 72 pt (T9). |
| **10** | Metodología | 7,9 | **8,1** | $+0,2$ | «10. Metodología» dejó de componer el numeral en familia y cuerpo dispares (T3). |
| **11** | Arquitectura | 8,2 | **8,5** | $+0,3$ | Ciclo de vida en 11.4 numerado de 1 a 8 (T2 resuelto), respaldando el cumplimiento del OE1. |
| **12** | Implementación Técnica | 8,4 | **8,4** | $0,0$ | Máximo histórico sostenido: hilos coinciden con 14.4, volumen cierra y SQLMap es ejecutable. |
| **13** | Resultados Obtenidos | 8,4 | **8,4** | $0,0$ | Sin cambios. Las seis tablas cierran con exactitud matemática y trazabilidad física. |
| **14** | Discusión | 8,6 | **8,6** | $0,0$ | Capítulo mejor calificado del documento. Coherencia plena entre timeouts y capítulo 17. |
| **15** | Conclusiones y Trabajos Futuros | 7,9 | **8,1** | $+0,2$ | «Verificación por objetivo específico» jerarquizada como subsección 15.1.1 en índice (T9). |
| **16** | Consideraciones Éticas | 8,2 | **8,2** | $0,0$ | Sin cambios. Sólido anclaje en legislación nacional y código deontológico ACM. |
| **17** | Desarrollo Experimental | 8,3 | **8,6** | $+0,3$ | Jerarquía de niveles restituida, 17.3 desanidada (T4) y cursiva eliminada en Tabla 13 (T9). |
| **18** | Referencias Bibliográficas | 8,5 | **8,8** | $+0,3$ | Sangría francesa APA 7.ª restituida en las 26 entradas y cita Faraday unificada (T8). |
| **19** | Anexos Técnicos | 8,3 | **8,5** | $+0,2$ | Estilos unificados, Dockerfile con mayúscula y Figura 4 ampliada legible (T6/T7). |
| **PROM.** | **Promedio Simple (19 Caps.)** | **7,81** | **7,99** | **$+0,18$** | **Avance sostenido hacia la banda de excelencia.** |
| **GLOBAL**| **Calificación Ponderada UTN** | **8,0** | **8,4** | **$+0,40$** | **Condición previa levantada; documento apto para defensa.** |

---

### 3. Auditoría de Transición de Condiciones Previas

En el Dictamen 7 se impuso una condición previa bloqueante compuesta por 4 operaciones específicas. Su estado en el Dictamen 8 es el siguiente:

* **Operación T1 — Fórmula del tutor y línea institucional en portada:**
  * *Exigencia D7:* Restituir la fórmula truncada («A designar... antes») y unificar el bloque institucional en negrita.
  * *Estado D8:* **CUMPLIDA AL 100%**. La portada consigna formalmente a «Alberto Cortez y Ariel Enferrel» y la línea «Tecnicatura Universitaria en Programación» quedó unificada sin desdoblamientos tipográficos. Se cerró una observación abierta desde la primera instancia.
* **Operación T2 — Numeración correlativa en Sección 11.4:**
  * *Exigencia D7:* Reiniciar en 1 la lista de pasos del ciclo de vida del análisis (estaba numerada de 5 a 12).
  * *Estado D8:* **CUMPLIDA AL 100%**. Los 8 pasos se numeran correlativamente de 1 a 8, respaldando la evidencia formal del Objetivo Específico 1.
* **Operación T3 — Desvinculación de títulos de capítulos de listas automáticas:**
  * *Exigencia D7:* Sacar Capítulos 6, 7, 8 y 9 de listas automáticas y normalizar Capítulos 1, 2 y 10.
  * *Estado D8:* **CUMPLIDA**. Los números están en el texto a margen regular (72 pt) en Calibri Bold 14. «6. Hipótesis» y «7. Estado del Arte» ya no se confunden con ítems de preguntas de investigación.
* **Operación T4 — Jerarquía de encabezados del Capítulo 17 e índice:**
  * *Exigencia D7:* Corregir tamaño de 17.2.1–17.2.5 (estaban en cuerpo 14) y desanidar 17.3 en el índice general.
  * *Estado D8:* **CUMPLIDA**. 17.2.1 a 17.2.5 pasaron a cuerpo 11 (nivel 3); 17.1 a 17.3 a cuerpo 12 (nivel 2). La subsección 17.3 ya no aparece indentada bajo 17.2 en el índice.

---

### 4. Auditoría de Correcciones Recomendadas

Evaluación del estado de las recomendaciones técnicas complementarias formuladas en $D_{7}$:

| Código | Descripción de la Recomendación | Estado en $D_{8}$ | Evidencia Verificada en Informe V15 |
| :---: | :--- | :---: | :--- |
| **T5** | Corrección de remisión errónea en Cap. 7 (apuntaba a 8.5 en vez de 11.1). | **Subsanada** | El texto remite formalmente a la sección 11.1 para el mecanismo de caché incremental. |
| **T6** | Escala de diagramas del Anexo H (Figuras 2 y 4 ampliadas, devolver Fig. 1 a caja). | **Parcial** | Fig. 4 ampliada ahora mide 592x604 pt y es legible (UML legible). Fig. 1 ampliada sigue fuera de caja y se corta inferiormente (pasa a U3). |
| **T7** | Unificación de estilos en Anexos (A.1–A.3, rótulo Anexo H, notas y epígrafes). | **Subsanada** | A.1–A.3 pasaron a Calibri Bold; Anexo H a cuerpo 13; notas a Calibri cursiva 10 pt; epígrafes en cursiva. |
| **T8** | Unificación cita/entrada Faraday y restitución de sangría francesa APA. | **Subsanada** | Cita unificada como «(Faraday Security, 2025)»; 26 referencias con sangría francesa estricta (1.ª línea 72 pt, siguientes 108 pt). |
| **T9** | Subsanación de residuos de acabado tipográfico y de índices. | **Parcial (Mayoría Subsanada)** | Subsanados: cursiva de Tabla 13, niveles de índice preliminar, subsección 15.1.1, Dockerfile en A.1 y caja de Fig. 4. Persisten: títulos a 66 pt, cuerpo menor de Tabla 6 en índice y cierre tipográfico de Tabla 13. |
| **DOC**| Unificación mayúscula Dockerfile en árbol del Anexo A.1. | **Subsanada** | Consignado como «Dockerfile», coincidente con el comando de build en A.2 y A.3. |
| **APA**| Consignación de nombres de directores de tesina en carátula. | **Subsanada** | Incorporados los dos profesionales en portada. |

---

### 5. Ciclo de Vida y Transición de Hallazgos Técnicos

#### A. Hallazgos Cerrados Satisfactoriamente
* **T1, T2, T3, T4:** Todo el bloque de condiciones previas resuelto.
* **T5:** Remisión interna reparada sin cabos sueltos.
* **T7, T8:** Unificación editorial y conformidad plena con normas APA 7.ª edición.
* **R7 / T9 (Cursiva Tabla 13):** Cerrado definitivamente un residuo arrastrado desde la 5.ª corrección.

#### B. Nuevos Hallazgos de Octava Corrección (Serie U — Residuos de Acabado para v16)
El tribunal tipificó 4 hallazgos menores de severidad baja, originados en corrimientos de maquetación:

1. **U1 · Desfase de página en entrada de Tabla 13 en el Índice de Tablas [Severidad: Baja]:**
   * *Diagnóstico:* El índice de tablas envía la Tabla 13 a la página 49. Sin embargo, la tabla y su rótulo físico se encuentran en la página 50 (la pág. 49 concluye con el texto de 17.2.5). Es la única discrepancia entre las 108 entradas de los índices.
   * *Acción correctiva:* Forzar salto de página limpio o actualizar la referencia dinámica del índice.
2. **U2 · Ausencia de espacio tras el punto en el título del Capítulo 17 [Severidad: Baja]:**
   * *Diagnóstico:* El título quedó tipografiado como «17.Desarrollo Experimental y Validación de Hallazgos» (sin espacio tras el punto).
   * *Acción correctiva:* Insertar el espacio tipográfico reglamentario («17. Desarrollo...»).
3. **U3 · Figura 1 ampliada del Anexo H fuera de caja y truncada por el borde inferior [Severidad: Baja - Prioritaria]:**
   * *Diagnóstico:* La imagen ocupa de 24 a 588 pt de ancho, desbordando los márgenes de la caja de texto (72 a 540 pt) y extendiéndose verticalmente más allá del pie de página, cortando la zona inferior del diagrama. Las Figuras 2 y 4 ampliadas también rozan los límites físicos de la hoja.
   * *Acción correctiva:* Escalar la Figura 1 ampliada ajustándola al ancho útil (máximo 100% de la caja de texto o ~468 pt) y centrarla verticalmente en su página exclusiva; contener Figuras 2 y 4 dentro del mismo límite.
4. **U4 · Numeral partido y sangría residual en títulos de Capítulos 1 y 2 [Severidad: Baja]:**
   * *Diagnóstico:* En «1. Introducción» y «2. Planteo del Problema», persiste un separador invisible heredado de listas previas, y el Capítulo 1 arranca a 90 pt (sangrado 18 pt hacia adentro respecto al margen general de 72 pt).
   * *Acción correctiva:* Reemplazar ambos encabezados por texto plano uniforme alineado estrictamente a 72 pt, idéntico a los Capítulos 3 al 19.

#### C. Residuos Menores Persistentes de T9
* **Alineación de subtítulos:** Los títulos 4.1, 4.2, 8.1 a 8.6 y 9.1 arrancan a 66 pt (6 pt a la izquierda del margen estándar de 72 pt). Deben alinearse a 72 pt.
* **Tipografía del Índice de Tablas:** La segunda mitad del título de la Tabla 6 aparece en cuerpo 11 pt en el índice sobre un cuerpo general de 12 pt.
* **Cierre de la Tabla 13:** La celda de total mezcla fuentes: «125 minutos (~2 horas» en Arial Bold y el cierre «)» en Calibri Bold. Debe unificarse al 100% en Calibri.
* **Numerales de listas:** Homogeneizar los numerales de listas automáticas (en 11.4 y otras) a la familia tipográfica principal (Calibri), eliminando fuentes residuales en Arial o Times New Roman.

---

### 6. Balance Cuantitativo de Subsanación Consolidado

| Categoría de Observación | Cantidad en $D_{7}$ | Subsanados en $D_{8}$ | Parciales | No Subsanados | Tasa de Éxito Pleno (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Condición Previa Bloqueante (T1–T4)** | 4 | **4** | 0 | 0 | **100,0 %** |
| **Correcciones Recomendadas (T5–T9, DOC, APA)**| 7 | **6** | 1 | 0 | **85,7 %** |
| **TOTAL GENERAL CONSOLIDADO** | **11** | **10** | **1** | **0** | **90,9 % (91 %)** |

> **Lectura Metodológica del Balance:**  
> Por primera vez en las 8 instancias de auditoría, se alcanza una tasa de cierre pleno superior al 90% con **cero observaciones de contenido técnico, metodológico o aritmético**. El 9,1% restante corresponde exclusivamente al escalado dimensional de una figura complementaria de anexo (Figura 1 en Anexo H).

---

### 7. Diagnóstico de Tendencia y Pronóstico Académico

* **Evolución Histórica de la Calificación:**  
  * Instancia 6: **7,9 / 10** (Condicionada por coherencia numérica intercapítulos).  
  * Instancia 7: **8,0 / 10** (Condicionada por maquetación de portada y listas automáticas).  
  * Instancia 8: **8,4 / 10** (Aprobada sin condiciones; documento formalmente presentable).  
  * **Proyección para Informe v16:** Con la subsanación de los hallazgos U1 a U4 y la lista de acabado fino, la calificación proyectada por el tribunal evaluador se sitúa en **8,7 a 8,8 / 10**, posicionando el informe en el umbral inmediato para aspirar a una calificación de **Sobresaliente (9,0 a 10,0)** en la instancia de defensa oral.
* **Camino Crítico hacia la Excelencia en la Defensa Oral:**  
  El documento técnico ya posee solidez empírica inobjetable (13 tablas cerradas, 26 referencias APA, pipelines reproducibles y métricas reales). El objetivo de la Versión 16 es alcanzar la **perfección editorial absoluta (defecto cero)** para que el tribunal evaluador no encuentre ninguna distracción visual y se concentre exclusivamente en el valor de la ingeniería presentada.

---

## PARTE II: PLAN MAESTRO DE ACCIÓN OPERATIVO PARA INFORME V16

Este plan traduce los hallazgos y recomendaciones del Dictamen 8 en tareas modulares, organizadas bajo la metodología paso a paso y mapeadas con precisión a los archivos fuente en Typst.

```
docs/informe/
├── informe-v16.typ                             <-- Archivo maestro v16 (índices, carátula, directivas)
└── capitulos/
    ├── 01-introduccion.typ                     <-- Tarea Fase 3 (U4: numeral y sangría)
    ├── 02-planteo-problema.typ                 <-- Tarea Fase 3 (U4: numeral sin span invisible)
    ├── 04-objetivos.typ                        <-- Tarea Fase 3 (T9: sangría subtítulos 4.1-4.2)
    ├── 08-marco-teorico.typ                    <-- Tarea Fase 3 (T9: sangría subtítulos 8.1-8.6)
    ├── 09-alcances-limitaciones.typ            <-- Tarea Fase 3 (T9: sangría subtítulo 9.1)
    ├── 11-arquitectura.typ                     <-- Tarea Fase 3 (Tipografía numerales lista 11.4)
    ├── 17-desarrollo-experimental.typ          <-- Tarea Fase 2 (U2: espacio título; T9: tipografía Tabla 13)
    └── 19-anexos.typ                           <-- Tarea Fase 1 (U3: dimensiones Figuras Anexo H)
```

---

### FASE 1: Subsanación Prioritaria en Anexo H (U3 — Redimensión de Figuras) [Hecho]
* **Objetivo:** Resolver el único defecto de legibilidad visual señalado en el Dictamen 8.
* **Archivo afectado:** `docs/informe/capitulos/19-anexos.typ`.
* **Diagnóstico Técnico Actual:**
  * En la línea 443, la Figura 1 ampliada se incluye como `#image("../media/media/image2.png", width: 100%)`. En Typst, esto ocupa todo el ancho de página o invade los márgenes laterales si está en bloque desalineado, desbordando verticalmente y cortándose por el pie.
  * Las Figuras 2 y 4 ampliadas (`image1.jpg` e `image3.png`) también rozan los bordes de la página.
* **Acciones Concretas:**
  1. Restringir el ancho de la Figura 1 ampliada a un tamaño contenido en la caja de texto (ancho sugerido: `88%` o `90%`, con límite vertical para que quepa holgadamente con su epígrafe dentro de los márgenes estándar).
  2. Aplicar alineación vertical centrada en la página de la Figura 1 ampliada para evitar el desbalance espacial superior/inferior.
  3. Ajustar el escalado de las Figuras 2 y 4 ampliadas (ancho sugerido: `90%` a `92%`), garantizando márgenes de seguridad respecto al borde físico del papel.
* **Criterio de Validación:** Inspeccionar visualmente la página renderizada en el PDF: ninguna imagen ni epígrafe debe sobrepasar la caja de texto útil (márgenes laterales de 72 pt a 540 pt) ni invadir el área de pie de página.

---

### FASE 2: Ajuste del Capítulo 17 y Verificación de la Tabla 13 (U1, U2 y T9) [Hecho]
* **Objetivo:** Garantizar la sincronía del índice de tablas, corregir el espaciado del título y unificar la tipografía de la tabla de auditoría manual.
* **Archivos afectados:**
  * `docs/informe/capitulos/17-desarrollo-experimental.typ`
  * `docs/informe/informe-v16.typ`
* **Diagnóstico Técnico Actual:**
  * El título en la versión evaluada se presentó como «17.Desarrollo...» sin espacio entre el punto y el texto (U2).
  * La celda de cierre de la Tabla 13 en el documento evaluado mezclaba fuentes tipográficas entre Arial Bold y Calibri Bold (T9).
  * En el documento compilado final evaluado por el tribunal, la Tabla 13 cayó en la página 50 pero el índice la referenciaba a la 49 (U1).
* **Acciones Concretas:**
  1. Verificar que el título del archivo `17-desarrollo-experimental.typ` mantenga de forma indeleble el espacio reglamentario: `= 17. Desarrollo Experimental y Validación de Hallazgos`.
  2. Inspeccionar la fila de cierre de la Tabla 13 y asegurar que todo el texto `125 minutos (~2 horas)` esté tipografiado en la fuente unificada `Calibri` (peso bold), eliminando cualquier fragmento en Arial.
  3. En `informe-v16.typ`, confirmar que la macro `#let pagina(etiqueta) = context { ... }` obtenga la ubicación real de `<tabla-13>` dinámicamente o añadir un `#pagebreak()` previo si la tabla quedaba partida entre dos páginas.
* **Criterio de Validación:** El índice de tablas debe imprimir exactamente el mismo número de página en el que aparece la cabecera física de la Tabla 13.

---

### FASE 3: Normalización de Encabezados y Tipografía Residual (U4 y T9) [Hecho]
* **Objetivo:** Eliminar cualquier resto de caracteres invisibles, discrepancias de sangría y disparidades de fuente en listas.
* **Archivos afectados:**
  * `docs/informe/capitulos/01-introduccion.typ`
  * `docs/informe/capitulos/02-planteo-problema.typ`
  * `docs/informe/capitulos/04-objetivos.typ`
  * `docs/informe/capitulos/08-marco-teorico.typ`
  * `docs/informe/capitulos/09-alcances-limitaciones.typ`
  * `docs/informe/capitulos/11-arquitectura.typ`
* **Diagnóstico Técnico y Verificación Empírica Realizada:**
  * Los 19 títulos de capítulo (`level 1`) fueron auditados en sus bytes UTF-8: todos inician con `= N. Título` limpio, con espacio simple y cero caracteres invisibles o tabuladores. En el PDF inician en el margen estándar de 72 pt ($x_0 = 70,87\text{ pt}$).
  * Todos los subtítulos de segundo nivel (4.1, 4.2, 8.1–8.6, 9.1) inician exactamente en el margen estándar ($x_0 = 70,87\text{ pt}$). El desfasaje a 66 pt de Google Docs ha desaparecido.
  * Censo tipográfico completo sobre las 63 páginas: el 100% del documento se compone en `Calibri` (y `Consolas` para bloques de código). Cero apariciones de Arial o Times New Roman.
* **Criterio de Validación:** Cumplido al 100%. U4 y los residuos de T9 quedan técnicamente subsanados.

---

### FASE 4: Actualización Estructural del Documento Maestro (`informe-v16.typ`)
* **Objetivo:** Crear la nueva versión oficial del documento compilado con metadatos actualizados.
* **Archivo afectado:** `docs/informe/informe-v16.typ`.
* **Acciones Concretas:**
  1. Generar `informe-v16.typ` tomando como base `informe-v15.typ`.
  2. Mantener explícitamente en la portada la designación formal de directores:  
     `#strong[Directores:] Alberto Cortez y Ariel Enferrel.`
  3. Asegurar que las referencias dinámicas a figuras y tablas utilicen el motor de contexto de Typst (`#context`) para calcular la paginación con precisión matemática en las 108 entradas.
  4. Revisar la entrada de la Tabla 6 en el Índice de Tablas para que todo el texto mantenga un tamaño tipográfico uniforme (12 pt), eliminando el fragmento en 11 pt detectado en T9.
* **Criterio de Validación:** Compilación limpia mediante el compilador Typst sin advertencias (*warnings*) de etiquetas duplicadas ni desbordamiento de páginas.

---

### FASE 5: Gestión Institucional y Preparación de la Defensa
* **Objetivo:** Cumplimentar los aspectos administrativos y preparar las respuestas del tribunal oral.
* **Acciones Concretas:**
  1. **Trámite de Coordinación Académica:** Confirmar con la Secretaría/Coordinación de la TUP la resolución formal de designación de los directores Alberto Cortez y Ariel Enferrel.
  2. **Banco de Preguntas Previsibles para la Defensa Oral:**
     * *Pregunta 1:* «¿Por qué el escaneo activo en la sesión manual insumió 40 minutos mientras que en la discusión se establece un techo de 10 minutos?»  
       *Respuesta preparada:* Se fundamenta en la nota de trazabilidad del Capítulo 17: dicha sesión corrió con la configuración preliminar previa a la optimización de timeouts y concurrencia (2 hilos y sin límite por regla), lo que motivó justamente la formulación e implementación de las mejoras descritas en la sección 14.4.
     * *Pregunta 2:* «¿Con cuántos hilos y qué parámetros opera el motor de SQLMap?»  
       *Respuesta preparada:* Opera con `--threads=10`, `--smart` y `--batch`, conforme a la arquitectura validada en 12.6 y corroborada en 14.4.
     * *Pregunta 3:* «¿Es reproducible el entorno con el Anexo A?»  
       *Respuesta preparada:* Sí, el archivo `docker-compose.yml` unificado en A.2 levanta la totalidad de los 5 servicios desacoplados, cerrando contra las rutas relativas del árbol documentado en A.1 con el archivo `Dockerfile` debidamente tipografiado.
     * *Pregunta 4:* «¿Cómo se concilia el timeout de SQLMap de 300 segundos en 12.3 con los 20 minutos asignados en la Tabla 13?»  
       *Respuesta preparada:* Los 300 segundos corresponden al límite individual por endpoint evaluado; los 20 minutos de la Tabla 13 representan el tiempo acumulado de la sesión completa ejecutada en background contra múltiples rutas candidatas.

---

## PARTE III: MATRIZ DE VERIFICACIÓN DE LOS 5 CRITERIOS INQUEBRANTABLES

Antes de dar por concluida la entrega de la Versión 16, se aplicará el checklist estricto de tolerancia cero:

| Criterio Inquebrantable | Verificación Operativa para Informe v16 | Estado |
| :--- | :--- | :---: |
| **1. Recálculo Aritmético Independiente** | Las 13 tablas cuantitativas deben recalcularse íntegramente. Ninguna suma ni porcentaje puede discrepar (Tablas 3, 4, 9, 10, 11 y 13 con tolerancia cero de redondeo). | `[A VALIDAR EN COMPILACIÓN]` |
| **2. Verificación Cruzada de Remisiones** | Toda remisión interna («sección 11.1», «Tabla 12», «Anexo H») debe resolver contra el destino que efectivamente describe el concepto invocado. | `[A VALIDAR EN COMPILACIÓN]` |
| **3. Consistencia de Parámetros** | Parámetros `--threads=10`, `--smart`, timeouts de ZAP (10 min), volúmenes `.:/app` y nombres de contenedores deben coincidir entre Cap. 11, 12, 14, 17 y Anexos. | `[A VALIDAR EN COMPILACIÓN]` |
| **4. Trazabilidad Empírica a Archivos Reales** | Cada hallazgo, métrica y volcado SQL debe provenir de archivos físicos del repositorio (`resultado_unificado.json`, `sqlmap_bg.log`, etc.). Queda prohibido inventar o simular métricas. | `[CONFORME - HEREDADO V15]` |
| **5. Detección Obligatoria de Regresiones** | La corrección de las figuras del Anexo H y los títulos no debe desfasar la paginación de las 108 entradas del índice general ni alterar las sangrías francesas de las 26 referencias bibliográficas. | `[A VALIDAR EN COMPILACIÓN]` |

---

## RESUMEN DE COMPROMISOS OPERATIVOS PARA INFORME V16

* **Meta de Calificación:** Escalar de **8,4** a **8,7+ / 10** en la versión escrita final.
* **Enfoque de Trabajo:** Cero cambios de contenido ni de datos; 100% de esfuerzo enfocado en **pulido editorial, calibración visual de diagramas y exactitud tipográfica**.
* **Modo de Ejecución:** Modular, paso a paso, aislando cada archivo en `docs/informe/capitulos/` y verificando la compilación en Typst antes de avanzar al siguiente archivo.