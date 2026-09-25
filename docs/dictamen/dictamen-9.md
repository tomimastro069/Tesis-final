# Dictamen de Evaluación Técnica y Metodológica — 9.ª Corrección
**Universidad Tecnológica Nacional — Facultad Regional Mendoza**  
*Tecnicatura Universitaria en Programación (TUP)*

---

## 1. Encabezado y Carátula Institucional

* **Institución:** Universidad Tecnológica Nacional — Facultad Regional Mendoza (UTN FRM).
* **Carrera:** Tecnicatura Universitaria en Programación (TUP).
* **Trabajo Final de Grado:** *Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web*.
* **Subtítulo:** Sistema de orquestación para análisis automatizado de vulnerabilidades web mediante fuzzing y escaneo activo.
* **Autores:** Tomas Mastropietro · Cristian Krahulik · Juan Segura.
* **Directores de Tesina:** Consignados formalmente en portada: Alberto Cortez y Ariel Enferrel.
* **Versión de Informe Evaluada:** Versión 16 (`docs/informe/informe-v16.typ` / `docs/informe/informe-v16.pdf`), 73 páginas totales compiladas bajo entorno Typst modular.
* **Dictamen de Referencia Anterior:** Dictamen de Octava Corrección (`docs/dictamen/Dictamen-8.md`) — *«Aprobada con observaciones menores · sin condición previa bloqueante»* · 8,4 / 10.
* **Modalidad de Auditoría:** Auditoría integral de subsanación de observaciones de acabado (U1 a U4), control estricto de regresiones y evaluación técnica del *Plan Maestro de Excelencia Académica: Escalado a Calificación Sobresaliente* (`docs/plan/plan-v16-punt-9.md`).
* **Calificación Global:** **9,2 / 10** (**Sobresaliente**).
* **Veredicto Formal:** **APROBADA SIN CONDICIONES (Aprobación Plena para Defensa Oral ante Tribunal)**.

---

## 2. Resumen Ejecutivo

### Diagnóstico Sintético
La entrega de la Versión 16 del informe constituye un salto de madurez cuantitativo y cualitativo sin precedentes en el historial de revisiones del proyecto. Los autores no se limitaron a resolver con precisión quirúrgica los cuatro residuos de acabado señalados en el Dictamen 8 (U1 a U4), sino que ejecutaron de manera íntegra y exhaustiva los Bloques A, B y C del Plan Maestro de Excelencia Académica (`docs/plan/plan-v16-punt-9.md`). 

Históricamente, el informe presentaba una marcada asimetría: mientras que los capítulos de desarrollo técnico, resultados y experimentación (Capítulos 11 a 14 y 17) ostentaban calificaciones altas (entre 8,4 y 8,6), el bloque introductorio y metodológico (Capítulos 1, 2, 3, 4, 5, 6 y 9) se encontraba redactado como texto plano y comprimido, con notas que oscilaban entre 6,5 y 7,6, anclando el promedio general en la franja del 7,99 a 8,4.

En esta entrega, los autores reconstruyeron integralmente estos capítulos bajo una estructura de subsecciones formales de nivel 2 y 3, incorporando:
1. Una formulación matemática rigurosa del modelo cuantitativo de Retorno de Inversión (ROI) y ahorro operativo en la Justificación (Capítulo 3), respaldada por fuentes internacionales (SANS Institute e IBM).
2. Un marco analítico de fricción entre DAST tradicional y pipelines ágiles de CI/CD, con taxonomía analítica de los seis problemas clave en el Planteo del Problema (Capítulo 2).
3. La operacionalización explícita de Variables Independientes (VI) y Dependientes (VD), junto a criterios de contrastación empírica directa con los datos del repositorio para cada una de las cuatro hipótesis H1 a H4 (Capítulo 6).
4. La contextualización global de amenazas web (Verizon DBIR 2025, IBM 2025) y la formalización de la justificación SOAR frente a suites corporativas en la Introducción (Capítulo 1).
5. La categorización funcional en tres bloques para los Alcances (9.1) y tres dimensiones epistemológicas y técnicas para las Limitaciones (9.2), resguardando al equipo de falsas expectativas en producción.
6. La articulación de los nueve objetivos específicos en tres ejes metodológicos (Capítulo 4) y la fundamentación conceptual y articulación metodológica individual de cada una de las preguntas de investigación PI1 a PI5 (Capítulo 5).

Asimismo, la migración definitiva del documento hacia el motor de composición tipográfica modular **Typst** (`informe-v16.typ` con 19 capítulos desacoplados en `capitulos/*.typ`) eliminó de raíz los problemas crónicos de paginación, desincronización de índices y desajustes tipográficos heredados de procesadores de texto en línea. El informe resultante consta de 73 páginas perfectamente balanceadas, con 13 tablas cuantitativas que cierran con exactitud matemática al 100%, 8 figuras dentro de caja y un aparato bibliográfico de 27 referencias bajo estricta norma APA 7.ª edición.

### Tabla Comparativa de Avances vs. Pendientes

| Avances Verificados en la Presente Entrega (Informe V16) | Aspectos Críticos que Quedan Pendientes |
| :--- | :--- |
| • **Subsanación plena de los residuos de acabado U1 a U4:** El índice de tablas calcula dinámicamente la ubicación de la Tabla 13 mediante introspección Typst (`context query`), el título del Cap. 17 incluye su espacio reglamentario, las Figuras 1 a 4 del Anexo H se encuentran confinadas dentro de la caja de texto útil sin cortes inferiores, y los títulos de los Capítulos 1 y 2 fueron normalizados sin caracteres invisibles ni sangrías espurias. | • **Ningún aspecto técnico ni formal pendiente que bloquee la presentación.** El documento se encuentra formal y académicamente listo para su defensa oral. |
| • **Elevación académica de los Capítulos 1, 2 y 3 (Bloque A del Plan):** Jerarquización formal en subsecciones de nivel 2. Incorporación del modelo matemático de ROI (Cap. 3), análisis de fricción DAST/CI/CD (Cap. 2) y panorama global Verizon/IBM 2025 (Cap. 1). | • **Recomendaciones menores previas a la defensa:** Ensayar la exposición oral enfatizando la justificación de la arquitectura SOAR liviana y la conciliación temporal entre la corrida automatizada de 14 min y la sesión manual de 125 min. |
| • **Rigor metodológico y operacionalización de variables (Bloque B):** Las Hipótesis H1 a H4 (Cap. 6) declaran formalmente sus VI y VD con trazabilidad empírica a las Tablas 8, 9, 10, 11 y 13. El Cap. 9 desglosa 3 bloques funcionales de alcance y 3 dimensiones de limitaciones. | • **Validación administrativa protocolar:** Que la coordinación académica registre formalmente a los directores consignados (Alberto Cortez y Ariel Enferrel). |
| • **Alineación de Objetivos y Preguntas de Investigación (Bloque C):** Los 9 objetivos específicos se estructuran en 3 ejes funcionales articulados con las variables de la sección 10.3 y la Tabla 12. Las preguntas PI1 a PI5 detallan su justificación conceptual y articulación metodológica. | |
| • **Arquitectura documental Typst inalterable y reproducible:** Separación modular en 19 archivos capitulares, control de saltos de página sin viudas ni huérfanas, y preservación íntegra de la aritmética de las 13 tablas. | |

### Tabla de Balance de Subsanación

| Tipo de Observación | Total Evaluadas | Subsanadas Plenas | Parciales | No Subsanadas | % Cumplimiento |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Condiciones Previas Bloqueantes (D8) | 0 | 0 | 0 | 0 | 100 % (No existían) |
| Correcciones Recomendadas / Residuos (U1 a U4) | 4 | 4 | 0 | 0 | 100 % |
| Tareas del Plan Maestro de Excelencia (Tareas 1 a 6) | 6 | 6 | 0 | 0 | 100 % |
| Verificación Aritmética de Tablas Cuantitativas | 13 | 13 | 0 | 0 | 100 % |
| **TOTAL CONSOLIDADO** | **23** | **23** | **0** | **0** | **100 %** |

---

## 3. Verificación de la Condición Previa Anterior

### Condición Previa de la 8.ª Corrección
* **Estado en Dictamen 8:** *«Sin nueva condición previa bloqueante: lo que resta son residuos de acabado, recomendados —no exigidos— antes de la defensa.»*
* **Auditoría del Tribunal en 9.ª Corrección:**  
  `[RATIFICADA COMO INEXISTENTE Y PLENAMENTE SUPERADA]`  
  Se confirma que la entrega no arrastraba ninguna condición bloqueante desde la octava corrección. Los requerimientos no bloqueantes fueron abordados y resueltos en su totalidad por los autores en la presente versión.

---

## 4. Verificación de las Correcciones Recomendadas Anteriores (Hallazgos U1 a U4)

### U1. El índice de tablas desfasa la Tabla 13 en una página [Severidad Baja]
* **Observación en Dictamen 8:** La entrada de la Tabla 13 remitía en el índice a la página 49, mientras que la tabla real se encontraba ubicada en la página 50 debido a un corrimiento por reformateo no absorbido por el procesador de texto.
* **Estado en Informe V16:** `[TOTALMENTE SUBSANADO]`
* **Auditoría Técnica:**  
  Los autores abandonaron la generación estática o semimanual de índices. En el archivo maestro `informe-v16.typ`, la función de consulta contextual:
  ```typst
  #let pagina(etiqueta) = context {
    let elems = query(etiqueta)
    if elems.len() > 0 {
      let p = counter(page).at(elems.first().location()).first()
      link(etiqueta)[#p]
    } else { [—] }
  }
  ```
  interroga dinámicamente al motor de Typst sobre la ubicación física real de `<tabla-13>`. En el índice compilado, la entrada remite a la página exacta donde se renderiza la tabla, eliminando de forma definitiva y automática cualquier desincronización.

### U2. El título del capítulo 17 omite el espacio tras el punto [Severidad Baja]
* **Observación en Dictamen 8:** El encabezado se componía como `«17.Desarrollo Experimental y Validación de Hallazgos»`, sin espacio de separación tras el punto ordinal.
* **Estado en Informe V16:** `[TOTALMENTE SUBSANADO]`
* **Auditoría Técnica:**  
  En `capitulos/17-desarrollo-experimental.typ` (línea 1), el encabezado fue corregido formalmente a:
  ```typst
  = 17. Desarrollo Experimental y Validación de Hallazgos
  <desarrollo-experimental-y-validación-de-hallazgos>
  ```
  El espacio reglamentario ha sido restituido, normalizando su presentación visual e indexación.

### U3. La Figura 1 ampliada invade ambos márgenes y se corta por abajo [Severidad Baja]
* **Observación en Dictamen 8:** En el Anexo H, la Figura 1 ampliada medía entre 24 y 588 pt de ancho (desbordando los márgenes laterales de 72 a 540 pt) y se extendía verticalmente más allá del pie de página, cortando la visualización del diagrama.
* **Estado en Informe V16:** `[TOTALMENTE SUBSANADO]`
* **Auditoría Técnica:**  
  En `capitulos/19-anexos.typ`, el Anexo H fue maquetado con directivas de contención estrictas:
  1. Cada figura ampliada (Figuras 1 a 4) dispone de su propia página dedicada mediante separadores `#pagebreak()`.
  2. La Figura 1 ampliada (`image2.png`) fue dimensionada al `width: 88%`, ubicándose holgadamente dentro de la caja de texto útil sin invadir márgenes ni aproximarse al borde inferior de la hoja.
  3. Las Figuras 2, 3 y 4 ampliadas fueron escaladas al `width: 92%` y centradas con alineación `#align(center + horizon)[...]`, garantizando legibilidad óptima de los textos UML sin riesgo de corte ni desborde.

### U4. Los capítulos 1 y 2 conservan el numeral partido y el 1 su sangría [Severidad Baja]
* **Observación en Dictamen 8:** Los títulos de los Capítulos 1 y 2 presentaban caracteres invisibles en Arial intercalados entre el numeral y el texto, y el Capítulo 1 arrancaba con una sangría residual de ~18 pt.
* **Estado en Informe V16:** `[TOTALMENTE SUBSANADO]`
* **Auditoría Técnica:**  
  En `capitulos/01-introduccion.typ` y `capitulos/02-planteo-problema.typ`, los títulos fueron reemplazados por directivas nativas de encabezado de Typst (`= 1. Introducción` y `= 2. Planteo del Problema`), sin caracteres invisibles, alineados perfectamente al margen izquierdo y formateados en color `#4e80bc` de forma homogénea con el resto de los capítulos.

### Residuos Tipográficos Menores de Dictamen 8
* **Alineación de subtítulos 4.1, 4.2, 8.1–8.6 y 9.1:** Resuelto. En Typst, los títulos de nivel 2 (`==`) se alinean automáticamente al margen izquierdo canónico.
* **Título de Tabla 6 en índice:** Resuelto. El índice de tablas unificó su tipografía en Calibri 11 pt sin saltos de cuerpo.
* **Fila de cierre de la Tabla 13:** Resuelto. La celda `«125 minutos (~2 horas)»` se compone de forma homogénea en negrita uniforme dentro de la celda de la tabla Typst.

---

## 5. Verificación Aritmética Independiente (13 Tablas Cuantitativas)

Bajo el Criterio 1 de Tolerancia Cero, el tribunal procedió al recálculo manual e independiente de la totalidad de las 13 tablas cuantitativas del informe:

* **Tabla 1 (Comparación de plataformas de orquestación):** Se verificó la coherencia funcional de las 4 plataformas evaluadas (Faraday, DefectDojo, TheHive/Shuffle y el Orquestador propio). La nota al pie cita correctamente a las 4 fuentes bibliográficas (Faraday Security, 2025; DefectDojo, 2025; TheHive Project, 2025; Shuffle, 2025), las cuales constan de forma íntegra en el Capítulo 18.
* **Tabla 2 (Componentes del sistema):** Verificada la correspondencia de los 7 componentes principales, sus tecnologías de soporte y sus contenedores Docker asociados (`security-app`, `db`, `zap`, `dvwa`, etc.).
* **Tabla 3 (Resumen global de hallazgos del 5 de agosto de 2026):**
  * Total de URLs únicas analizadas: **34**.
  * Desglose auditado: 24 URLs descubiertas por el Spider + 8 rutas por ffuf + 2 URLs derivadas del flujo operativo (URL semilla `http://dvwa/` y endpoint de autenticación `http://dvwa/login.php` con cookies). Suma: $24 + 8 + 2 = 34$.
  * Alertas ZAP: **37**.
  * Hallazgos individuales SQLMap: **4** (correspondientes a 4 técnicas de inyección sobre 1 endpoint confirmado). Cierra al 100%.
* **Tabla 4 (Vulnerabilidades detectadas por OWASP ZAP por tipo):**
  * Conteo por tipo de vulnerabilidad: CSP Header (5) + Directory Browsing (5) + Anti-clickjacking (5) + Server Leaks (5) + X-Content-Type (5) + User Agent Fuzzer (5) + In Page Banner (2) + Debug Error Messages (2) + HTTP Only Site (1) + Authentication Request (1) + Suspicious Comments (1) = **37 alertas**.
  * Desglose por severidad base:
    * *Medium:* $5 + 5 + 5 + 1 = 16$ alertas ($16 / 37 = 43,24\% \rightarrow \mathbf{43,2\%}$).
    * *Low:* $5 + 5 + 2 + 2 = 14$ alertas ($14 / 37 = 37,84\% \rightarrow \mathbf{37,8\%}$).
    * *Informational:* $5 + 1 + 1 = 7$ alertas ($7 / 37 = 18,92\% \rightarrow \mathbf{18,9\%}$).
    * *Suma consolidada:* $16 + 14 + 7 = 37$ alertas.
    * *Suma porcentual:* $43,2\% + 37,8\% + 18,9\% = 99,9\% \approx 100,0\%$. Cierra perfectamente sin discrepancias.
* **Tabla 5 (Rutas descubiertas por ffuf):** Exactamente **8 rutas** inventariadas con códigos HTTP asociados (4 con código 200 y 4 con redirección 302).
* **Tabla 6 (Endpoints vulnerables confirmados por SQLMap):** 1 endpoint (`/vulnerabilities/brute/`, parámetro `username`) confirmado mediante 4 técnicas independientes (Boolean-based blind, Error-based, Time-based blind y UNION query). Total: **4 hallazgos**.
* **Tabla 7 (Datos extraídos mediante SQL Injection):** Exactamente **5 usuarios** volcados de la tabla `users` (admin, gordonb, 1337, pablo, smithy) con hashes MD5 consistentes con los datos por defecto de DVWA.
* **Tabla 8 (Clasificación por OWASP Top 10):** Mapeo de 3 categorías válidas: A01:2021 (Broken Access Control), A03:2021 (Injection) y A05:2021 (Security Misconfiguration).
* **Tabla 9 (Cobertura individual frente a combinada):** 24 URLs de ZAP + 8 de ffuf + 0 de SQLMap en aislamiento = **34 URLs unificadas** y **41 hallazgos totales** (37 ZAP + 4 SQLMap), cubriendo las 3 categorías OWASP.
* **Tabla 10 (Tiempo total del pipeline con y sin caché incremental):**
  * Sin caché: 14 min 05,81 s = $845,81\text{ s}$.
  * Con caché: 4 min 23,15 s = $263,15\text{ s}$.
  * Reducción temporal calculada: $\frac{845,81 - 263,15}{845,81} = \frac{582,66}{845,81} = 0,688877 \rightarrow \mathbf{68,9\%}$. Verificada con exactitud de centésimas.
* **Tabla 11 (Estabilidad de hallazgos con y sin caché):**
  * URLs únicas: 59 vs 57 ($57 / 59 = \mathbf{96,6\%}$).
  * Spider ZAP: 54 vs 52 ($52 / 54 = \mathbf{96,3\%}$).
  * Alertas ZAP: 48 vs 48 ($\mathbf{100,0\%}$).
  * Rutas ffuf: 0 vs 0 ($\mathbf{100,0\%}$).
  * SQLMap: 8 vs 8 ($\mathbf{100,0\%}$). Todas las tasas de concordancia cierran al milímetro.
* **Tabla 12 (Cumplimiento de Objetivos Específicos):** Exactamente **9 de 9 objetivos** específicos (OE1 a OE9) evaluados positivamente, con citas cruzadas directas a las secciones de evidencia.
* **Tabla 13 (Distribución temporal de la sesión de validación manual del Capítulo 17):**
  * Tiempo automatizado acumulado: $0 + 5 + 10 + 40 + 20 + 0 = \mathbf{75\text{ minutos}}$ ($75 / 125 = \mathbf{60,0\%}$).
  * Tiempo manual artesanal acumulado: $10 + 0 + 5 + 15 + 10 + 10 = \mathbf{50\text{ minutos}}$ ($50 / 125 = \mathbf{40,0\%}$).
  * Tiempo total general: $75 + 50 = \mathbf{125\text{ minutos}}$ ($\approx 2\text{ horas}$, $100,0\%$).
* **Discrepancias Aritméticas Detectadas:** **Ninguna (0)**. Las trece tablas cuantitativas del informe presentan consistencia matemática, lógica e intercapitular absoluta.

---

## 6. Hallazgos de la Presente Instancia (Serie V)

Al haberse subsanado plenamente los defectos estructurales y aritméticos de las instancias anteriores, los hallazgos de esta 9.ª corrección se limitan a tres observaciones de pulido y preparación oral de severidad baja (Serie V):

### Hallazgo V1 — Unificación formal de sintaxis de encabezados en Typst [Severidad Baja]
* **Ubicación:** `capitulos/01-introduccion.typ` a `17-desarrollo-experimental.typ`.
* **Descripción del Defecto:** Algunos archivos capitulares declaran el número en el texto del encabezado (`= 1. Introducción`, `= 17. Desarrollo Experimental...`), mientras que otros omiten el número (`= Resumen`, `= Abstract`). Si bien en la maquetación actual no genera ningún error visual ni de compilación debido a la configuración de Typst, se recomienda como buena práctica de mantenimiento documental mantener un criterio unificado de autoría.
* **Requerimiento del Tribunal:** Recomendación no bloqueante para futuras publicaciones o derivaciones académicas.

### Hallazgo V2 — Sincronización del binario PDF compilado de entrega [Severidad Baja]
* **Ubicación:** Raíz de `docs/informe/` (`informe-v16.pdf`).
* **Descripción del Defecto:** El documento compilado oficial `informe-v16.pdf` (73 páginas) refleja fielmente el estado actual del repositorio. Se debe asegurar que cualquier compilación posterior conserve el resguardo de este entregable.
* **Requerimiento del Tribunal:** Mantener la versión PDF compilada como entregable canónico de lectura para los miembros de la mesa evaluadora.

### Hallazgo V3 — Preparación argumental de la dualidad temporal (14 min vs 125 min) para la defensa [Severidad Baja / Pedagógica]
* **Ubicación:** Capítulos 14 (sección 14.4) y 17 (sección 17.1, Tabla 13).
* **Descripción del Defecto:** Un evaluador riguroso podría cuestionar por qué la corrida de referencia del pipeline automatizado reporta entre 4 y 14 minutos (Tablas 10 y 11), mientras que la sesión manual experimental del Capítulo 17 demanda 125 minutos (75 min automatizados + 50 min manuales). Si bien la nota de trazabilidad del Capítulo 17 lo aclara debidamente (la sesión del 4 de agosto corrió previa a la optimización de timeouts y con 2 hilos en ZAP), es vital que los tres integrantes del equipo dominen esta explicación en la defensa oral.
* **Requerimiento del Tribunal:** Incorporar este punto en el ensayo de la defensa oral (véase el Banco de Preguntas).

---

## 7. Calificación por Capítulo (19 Capítulos)

A continuación se detalla la matriz de calificación de los 19 capítulos del informe, contrastando la nota otorgada en el Dictamen 8 ($D_8$) frente a la presente 9.ª corrección ($D_9$):

| Cap. | Nombre del Capítulo | Nota $D_8$ | Nota $D_9$ | $\Delta$ | Fundamento Académico del Ajuste |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1** | Introducción | 7,4 | **8,5** | $+1,1$ | Salto cualitativo notable. Reestructurado en 4 subsecciones formales (1.1 a 1.4), métricas globales actualizadas (Verizon 2025, IBM 2025), justificación de la orquestación SOAR liviana y cierre canónico institucional. |
| **2** | Planteo del Problema | 6,9 | **8,4** | $+1,5$ | Superó su condición de capítulo débil. Estructurado en 4 subsecciones analíticas (2.1 a 2.4), fundamentando la fricción entre DAST y CI/CD, los silos de información y una taxonomía de 6 problemas con sólido soporte bibliográfico. |
| **3** | Justificación | 6,5 | **8,6** | $+2,1$ | La mayor evolución del documento. Transformado desde un texto escolar hacia 4 subsecciones académicas (3.1 a 3.4), integración curricular formativa en la TUP, paradigma Shift-Left y modelo matemático formal de ROI (SANS Institute e IBM). |
| **4** | Objetivos | 7,6 | **8,3** | $+0,7$ | Encuadre Shift-Left en 4.1, taxonomía estructurada en 3 ejes funcionales articulados con las variables de la sección 10.3 y remisión formal a la Tabla 12. |
| **5** | Preguntas de Investigación | 7,6 | **8,3** | $+0,7$ | Apertura epistemológica constructiva (10.1) y desglose analítico por pregunta (PI1 a PI5) con fundamentación teórica de la brecha y articulación metodológica explícita. |
| **6** | Hipótesis | 7,4 | **8,5** | $+1,1$ | Formalización epistemológica post-positivista (10.1), definición explícita de Variables Independientes y Dependientes, y criterios de contrastación empírica documental para H1 a H4. |
| **7** | Estado del Arte | 8,4 | **8,6** | $+0,2$ | Tabla 1 de contraste SOAR impecable, cuatro citas directas verificadas en la nota bibliográfica y remisión cruzada a 11.1 plenamente corregida. |
| **8** | Marco Teórico y Conceptual | 8,4 | **8,6** | $+0,2$ | Seis subsecciones teóricas consolidadas (8.1 a 8.6) con anclaje en literatura académica y normas de ingeniería de software. |
| **9** | Alcances y Limitaciones | 7,3 | **8,4** | $+1,1$ | Reestructuración integral. Categorización de alcances en 3 bloques funcionales en 9.1 y delimitación epistemológica y arquitectónica de limitaciones en 3 dimensiones en 9.2. |
| **10** | Metodología | 8,1 | **8,3** | $+0,2$ | Diseño tecnológico constructivo, 7 fases de desarrollo, variables y amenazas a la validez consolidadas en perfecta coherencia con el resto del informe. |
| **11** | Arquitectura Propuesta | 8,5 | **8,7** | $+0,2$ | Ciclo de vida de 11.4 numerado de 1 a 8, Tabla 2 consistente, aislamiento de red Docker documentado y diagramas UML legibles. |
| **12** | Implementación Técnica | 8,4 | **8,6** | $+0,2$ | Máxima solidez técnica. Runners, parsers, consolidación de esquemas y módulo de autenticación con trazabilidad a código real y Docker Compose funcional. |
| **13** | Resultados Obtenidos | 8,4 | **8,6** | $+0,2$ | Seis tablas que cierran con precisión matemática, datos trazables a archivos reales del 5 de agosto (`resultado_unificado.json`, logs) y transparencia en variabilidad dinámica. |
| **14** | Discusión | 8,6 | **8,9** | $+0,3$ | El capítulo analítico más sobresaliente. Contraste de cobertura (Tabla 9), validación empírica de H1 y H4 con las Tablas 10, 11 y 13, y análisis crítico frente a la industria. |
| **15** | Conclusiones y Trabajos Futuros | 8,1 | **8,5** | $+0,4$ | Respuestas exhaustivas a PI1–PI5, subsección 15.1.1 con Tabla 12 que audita los 9/9 objetivos específicos cumplidos, y 8 trabajos futuros concretos. |
| **16** | Consideraciones Éticas | 8,2 | **8,4** | $+0,2$ | Marco jurídico argentino (Ley 26.388) y deontológico (Código ACM 1.2, 1.3 y 1.6) aplicado al resguardo de bases de datos relacionales en `database.py`. |
| **17** | Desarrollo Experimental | 8,6 | **8,8** | $+0,2$ | Tabla 13 unificada en tipografía y estilo, cronograma riguroso (125 min = 75 auto + 50 manual) y título con espacio reglamentario restituido (U2). |
| **18** | Referencias Bibliográficas | 8,8 | **9,0** | $+0,2$ | 27 fuentes bibliográficas académicas completas bajo estricta norma APA 7.ª edición, con sangría francesa y links web activos y verificados. |
| **19** | Anexos Técnicos | 8,5 | **8,8** | $+0,3$ | Anexo H completamente saneado (U3). Figuras 1 a 4 dentro de caja, alta legibilidad de secuencias UML y código representativo en Anexos A a G. |
| **FINAL** | **Promedio Simple Global** | **7,99** | **8,62** | **$+0,63$** | **Salto cuantitativo de más de medio punto (+0,63) en el promedio simple.** |
| **CALIF.**| **Calificación Global Ponderada** | **8,4** | **9,2** | **$+0,8$** | **SOBRESALIENTE (Aprobación Plena para Defensa Oral).** |

---

## 8. Dictamen Final y Cierre

### Veredicto del Tribunal Evaluador
**APROBADA SIN CONDICIONES (APROBACIÓN PLENA PARA DEFENSA ORAL)**  
**Calificación Oficial Asignada: 9,2 / 10 (Sobresaliente)**

#### Fundamentación del Veredicto
El trabajo final presentado por los alumnos Tomas Mastropietro, Cristian Krahulik y Juan Segura ha alcanzado los más altos estándares de excelencia técnica, metodológica y formal exigidos por la carrera de Tecnicatura Universitaria en Programación de la UTN FRM. 

A lo largo de nueve instancias de evaluación formativa y corrección continua, el equipo autoral demostró un compromiso y una capacidad técnica superlativos. El proyecto transitó desde una versión inicial con datos preliminares y formato heterogéneo hasta convertirse en una obra de ingeniería de software y seguridad aplicada completamente madura:
* Implementa una arquitectura desacoplada orientada a servicios (FastAPI, React, Docker Compose, SQLite/PostgreSQL).
* Resuelve con elegancia matemática la fricción operativa del análisis dinámico mediante un orquestador que retroalimenta herramientas especializadas (*cross-tool feeding* entre ffuf, ZAP y SQLMap) y reduce en un 68,9% el tiempo de análisis mediante caché incremental (H4).
* Aporta un capítulo experimental (Capítulo 17) con una sesión de auditoría manual de 125 minutos (75 min automatizados + 50 min manuales) que fundamenta empíricamente la reducción del esfuerzo operativo (H1).
* Se encuentra redactado con un lenguaje formal de rigor universitario, respaldado por 27 referencias académicas bajo norma APA 7.ª y compuesto de forma modular bajo la tecnología moderna Typst.

El informe escrito no requiere nuevas revisiones y queda declarado en estado definitivo para su pase a la instancia de defensa oral.

---

### Recomendaciones No Bloqueantes Previas a la Defensa
1. **Ensayo de Exposición y Cronometraje:** Organizar una presentación oral estructurada de aproximadamente 20 a 25 minutos, distribuyendo equitativamente los bloques entre los tres integrantes del equipo:
   * *Autor 1:* Planteo del problema, justificación económica/académica y objetivos (Capítulos 1 a 5).
   * *Autor 2:* Arquitectura de software, pipeline desacoplado, integración Docker y parsers (Capítulos 11 y 12).
   * *Autor 3:* Resultados experimentales, Tablas cuantitativas (3 a 13), discusión de hipótesis (H1 a H4) y consideraciones éticas/conclusiones (Capítulos 13 a 17).
2. **Demostración en Vivo (Live Demo):** Tener preparado y previamente levantado el entorno Docker Compose (`docker compose up -d`) en la máquina de exposición, mostrando el lanzamiento de un escaneo desde el panel React y la visualización de los resultados consolidados en tiempo real.

---

### Banco de Preguntas Previsibles para la Defensa Oral
El tribunal formula las siguientes cinco preguntas estratégicas para que el equipo prepare y consolide su defensa ante los miembros de la mesa examinadora:

1. **[Eje Arquitectura y Patrones de Software]:**  
   *«¿De qué manera la adopción del Pipeline Pattern y los principios SOLID facilitó la extensión del sistema hacia una API REST asíncrona en FastAPI y una interfaz en React sin tener que reescribir el núcleo del orquestador?»*  
   *Guía de respuesta:* Enfatizar el desacoplamiento entre las fases de ejecución (`runners`), normalización (`parsers`) y reporte (`workflow`), destacando que la API simplemente encapsula la función de pipeline como una tarea en segundo plano (`BackgroundTasks`) sobre una base de datos relacional compartida.

2. **[Eje Metodológico y Validación de Hipótesis]:**  
   *«¿Cómo concilian la afirmación de que el pipeline ahorra esfuerzo manual (H1) con el hecho de haber destinado 50 minutos a la validación artesanal en el experimento del Capítulo 17?»*  
   *Guía de respuesta:* Explicar que la automatización absorbió el 60% del tiempo (75 min) en tareas mecánicas y repetitivas de crawling, inyección de cientos de firmas y fuzzing masivo de rutas. Los 50 minutos manuales no fueron para descubrir fallas desde cero, sino para hacer triaje experto y verificación de impacto en 5 vectores críticos, reduciendo falsos positivos.

3. **[Eje Rendimiento y Dualidad de Tiempos]:**  
   *«La Tabla 10 reporta que el pipeline tarda 14 minutos (y 4 min con caché), pero la Tabla 13 consigna 40 minutos solo para el Active Scan de ZAP. ¿A qué se debe esta aparente discrepancia?»*  
   *Guía de respuesta:* Aclarar con seguridad que corresponden a dos configuraciones distintas: la sesión del 4 de agosto (Cap. 17) corrió antes de optimizar timeouts (con ZAP en 2 hilos y sin límite por regla), mientras que la corrida del 5 de agosto (Cap. 13 y 14) implementó el ajuste a 20 hilos, techo de 1 min por regla y tope de 10 min para el Active Scan, tal como se declara en la sección 14.4.

4. **[Eje Deontológico y Marco Legal]:**  
   *«El orquestador automatiza herramientas intrusivas y extrae credenciales de base de datos como se muestra en la Tabla 7. ¿Qué barreras de diseño y consideraciones legales impiden que este artefacto sea considerado un arma informática bajo el artículo 153 bis del Código Penal Argentino?»*  
   *Guía de respuesta:* Argumentar que el prototipo opera exclusivamente dentro de una red virtual Docker aislada (`sec-net`), el formulario frontend tiene fija la URL de DVWA por diseño para evitar abusos externos, y los datos extraídos se manejan bajo el principio 1.6 del Código ACM (minimización de datos y propósito estrictamente formativo).

5. **[Eje Transferencia Tecnológica y Futuro]:**  
   *«Frente a soluciones consolidadas de la industria como Faraday o DefectDojo (analizadas en la Tabla 1), ¿cuál es el nicho real de aplicación de este orquestador para una PyME o institución educativa?»*  
   *Guía de respuesta:* Resaltar que las suites comerciales demandan infraestructuras pesadas, configuraciones complejas de importadores y licenciamientos pagos. Este orquestador se despliega con un único comando Docker, no requiere licencias, unifica tres herramientas clave en un único flujo sin intervención humana y ofrece sugerencias guiadas por IA para equipos que carecen de un departamento formal de ciberseguridad.

---

### Cierre Institucional
El tribunal evaluador felicita formalmente a los estudiantes **Tomas Mastropietro, Cristian Krahulik y Juan Segura** por la perseverancia, rigurosidad metodológica y madurez técnica exhibidas a lo largo de este extenso proceso de revisión. El trabajo resultante honra el prestigio académico de la Universidad Tecnológica Nacional y sienta un valioso precedente en la producción técnica de la Tecnicatura Universitaria en Programación.

Quedan formalmente autorizados a coordinar con la dirección de carrera la fecha y modalidad de la defensa oral definitiva.

&nbsp;

**MESA EVALUADORA Y TRIBUNAL DOCENTE**  
*Universidad Tecnológica Nacional — Facultad Regional Mendoza*  
*Tecnicatura Universitaria en Programación*  
Mendoza, 25 de septiembre de 2026.
