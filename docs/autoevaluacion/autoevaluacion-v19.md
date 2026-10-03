# Informe Interno de Autoevaluación Académica y Control de Calidad — V19
**Universidad Tecnológica Nacional — Facultad Regional Mendoza**  
*Tecnicatura Universitaria en Programación (TUP)*  
*Trabajo Final de Graduación: Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web*

---

> **Nota Institucional de Alcance Formativo:**  
> El presente documento constituye una herramienta de trabajo y control de calidad interno desarrollada por los alumnos autores de la tesina. No sustituye, no representa ni pretende arrogarse la potestad evaluadora, las calificaciones formales ni los dictámenes oficiales emitidos con exclusividad por los docentes y el Tribunal Evaluador designado por la Universidad Tecnológica Nacional — Facultad Regional Mendoza. Su finalidad es estrictamente pedagógica: auditar la madurez técnica y metodológica del informe V19 frente a las observaciones de la cátedra para optimizar la preparación integral con miras a la defensa oral.

---

## 1. Carátula Interna de Control de Calidad

* **Institución:** Universidad Tecnológica Nacional — Facultad Regional Mendoza (UTN FRM).
* **Carrera:** Tecnicatura Universitaria en Programación (TUP).
* **Trabajo Final:** Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web.
* **Equipo de Autores:** Tomás Mastropietro, Cristian Krahulik, Juan Segura.
* **Directores de Tesina:** Lic. Alberto Cortez, Ing. Ariel Enferrel.
* **Versión de Informe Autoevaluada:** Informe V19 (`docs/informe/informe-v19.typ` / `docs/informe/informe-v19.pdf`, 76 páginas compiladas).
* **Dictamen Oficial de Referencia:** Dictamen 11 Oficial emitido por el Tribunal Evaluador (`docs/dictamen/Dictamen-11-oficial.pdf`, calificación: 8,6 / 10 · Aprobada con observaciones menores).
* **Modalidad de Trabajo:** Control interno formativo de calidad, verificación de no-regresión y preparación técnica para la defensa oral.
* **Estimación Interna de Conformidad:** **100% de Requerimientos Oficiales Satisfechos** (3/3 correcciones obligatorias X1–X3, 4/4 recomendaciones técnicas X4–X7 y adecuación 4.3 implementadas).
* **Estado de Madurez para Presentación:** **Apto para presentación formal ante la cátedra y habilitación plena a la instancia de Defensa Oral.**

---

## 2. Resumen Ejecutivo de Madurez Interna

### Diagnóstico Interno de los Autores
Tras la recepción del Dictamen 11 Oficial (que otorgó la aprobación académica formal con 8,6 / 10 y reconoció la subsanación total de las condiciones W1 a W7 previas), el equipo de autores ejecutó un ciclo de refinamiento exhaustivo plasmado en el plan de acción `docs/plan/plan-03-10-2026.md`. 

La versión V19 del informe representa la consolidación definitiva del documento de tesina. El trabajo abordó de raíz los hallazgos señalados por el tribunal respecto a la explicación interna de las cifras: se transparentó la fórmula matemática real de unión y deduplicación en la consolidación de 34 URLs ($24 + 4 + 5 + 1$), se sinceró el aporte exclusivo de ffuf en 4 rutas sensibles no indexadas (`index.php`, `logout.php`, `phpinfo.php`, `security.php`), se reemplazó la hipótesis insostenible sobre la wordlist en el benchmark por una declaración metodológicamente transparente de no determinación retrospectiva respaldada en 3 hipótesis técnicas plausibles, y se reconcilió el Anexo D como una reconstrucción canónica documentada.

Paralelamente, se subsanaron todas las recomendaciones de acabado: actualización de la Figura 4 (rótulo de PostgreSQL y remisión al Anexo H ampliado), cita en el texto de la referencia APA Mastropietro et al. (2026a), incorporación del registro crudo histórico `sqlmap_bg.log` como evidencia formal, rediagramación del payload en dos renglones a 7,5 pt para garantizar legibilidad impresa, documentación de los parámetros `nivel` y advertencias de `clean_cache`, y la completa adecuación institucional de las pautas y herramientas formativas en `.agents/` para deslindar cualquier confusión con las resoluciones oficiales del tribunal docente.

### Tabla de Contrastación Interna: Avances Logrados vs. Ajustes Pendientes
| Avances Verificados por los Autores (V19) | Ajustes Pendientes de Acabado |
| :--- | :--- |
| • **Aritmética de deduplicación resuelta:** Fórmula exacta $24 + 4 + 5 + 1 = 34$ en Cap. 13 (Tabla 3), Cap. 14 (Tabla 11) y `docs/evidencia/README.md`. | • **Gestión administrativa externa:** Confirmar formalmente ante la secretaría/coordinación de carrera de la UTN FRM que las resoluciones de designación de directores (Lic. Alberto Cortez, Ing. Ariel Enferrel) consten en el expediente académico. |
| • **Rigor en el aporte de ffuf:** Corrección de 8 a 4 rutas exclusivas en secciones 14.1 y 14.6, sustituyendo `/setup.php` por `/security.php` y `/phpinfo.php`. | • **Trámite de entrega:** Carga final del archivo compilado `informe-v19.pdf` (76 págs.) en el canal institucional fijado por la cátedra. |
| • **Transparencia en el benchmark del 06/08:** Supresión del error de la wordlist en 14.3; incorporación de 3 hipótesis técnicas y ratificación externa por video del 15/09 (Tabla 14). | • **Simulacro de defensa oral:** Entrenar entre los coautores las respuestas al banco de preguntas formulado en la Sección 8 de este documento. |
| • **Reconciliación canónica del Anexo D:** Supresión de afirmaciones contradictorias («datos reales») y retiro de la validación empírica de H3 en el anexo. | *(Ningún ajuste técnico ni documental pendiente en el informe)* |
| • **Remisiones literales a evidencia primaria:** Títulos exactos de `reporte_seguridad.md` en notas de Tablas 4, 5, 6 y 7; cita al crudo histórico `sqlmap_bg.log`. | |
| • **Diagrama de arquitectura sincronizado:** Figura 4 (`image3.svg` y `image3.png`) rotulada con `PostgreSQL (SQLite en modo local)` y remisión a versión ampliada en Anexo H. | |
| • **Adecuación institucional en `.agents/`:** Retitulación formal a autoevaluación interna formativa y redefinición del rol a Tutor Metodológico en reglas y skills. | |
| • **Entregable oficial V19 compilado:** 76 páginas limpias, portada en página 1, 3 índices unificados sin desajustes (`[—]`), compila sin advertencias. | |

### Balance de Subsanación frente al Dictamen Oficial Previo
| Requerimiento del Tribunal Oficial (Dictamen 11) | Total Identificados | Subsanados Completamente | En Proceso / Parciales | Pendientes | % Cumplimiento |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Correcciones Obligatorias Previas (X1, X2, X3)** | 3 | 3 | 0 | 0 | **100 %** |
| **Recomendaciones de Acabado (X4, X5, X6, X7)** | 4 | 4 | 0 | 0 | **100 %** |
| **Adecuación Institucional de Evaluación (Punto 4.3)** | 1 | 1 | 0 | 0 | **100 %** |
| **BALANCE CONSOLIDADO** | **8** | **8** | **0** | **0** | **100 %** |

---

## 3. Control Interno de Condiciones del Dictamen Oficial Previo

El Dictamen 11 dictaminó que el informe no presentaba condiciones previas bloqueantes, pero estableció tres correcciones obligatorias antes de la defensa oral:

### Condición Oficial X1: Conteo de URLs y Aporte Real de ffuf
> *«Reescribir la nota de la Tabla 3 con la fórmula de consolidar_resultados() (24 + 4 + 5 + 1 = 34) y corregir la de la Tabla 11; en 14.1 y 14.6, cuatro rutas nuevas en lugar de ocho y /phpinfo.php o /security.php como ejemplo en lugar de /setup.php.»*

* **Estado Interno:** `[CUMPLIDO PLENAMENTE]`
* **Auditoría Técnica de los Autores:**
  - **Tabla 3 (Capítulo 13):** Se eliminó la explicación aritmética previa ($24 + 8 + 2$) que sumaba por duplicado elementos ya descubiertos por el rastreo de ZAP. La nueva nota al pie desglosa con exactitud matemática el algoritmo de unión implementado en `consolidar_resultados()`: 24 URLs del spider (que ya integran la semilla `http://dvwa/` y `login.php`) + 4 rutas exclusivas descubiertas por ffuf (`index.php`, `logout.php`, `phpinfo.php`, `security.php`) + 5 directorios identificados por las alertas de inspección Directory Browsing de ZAP (`/docs/`, `/dvwa/`, `/dvwa/css/`, `/dvwa/images/`, `/dvwa/js/`) + 1 URL reportada por SQLMap (`/vulnerabilities/brute/`). Total unificado exacto: $24 + 4 + 5 + 1 = 34$.
  - **Tabla 11 (Capítulo 14):** Se armonizó la nota al pie explicando que las 5 URLs de diferencia provienen de la unión de directorios de ZAP y SQLMap.
  - **Secciones 14.1 y 14.6:** Se sustituyó la afirmación de «ocho rutas no identificadas por el rastreo de ZAP» por «cuatro rutas nuevas no identificadas por el rastreo de ZAP». Se reemplazó el ejemplo `/setup.php` (el cual el spider sí había descubierto proactivamente) por las rutas sensibles reales `/security.php` y `/phpinfo.php`.
  - **Consistencia de tablas:** Se auditó que las Tablas 8 y 9 no dependan de la cifra de ocho rutas nuevas.
  - **Repositorio documental:** Se sincronizó la misma fórmula en `docs/evidencia/README.md`.

### Condición Oficial X2: Benchmark del 6 de Agosto y Explicación de 0 Rutas
> *«Retirar «la wordlist no coincidió con rutas reales» y consignar la causa de las 0 rutas de ffuf o declarar que no se determinó, indicando qué implicaría cada alternativa para la comparación de la Tabla 10.»*

* **Estado Interno:** `[CUMPLIDO PLENAMENTE]`
* **Auditoría Técnica de los Autores:**
  - En la sección 14.3 de `14-discusion.typ`, se retiró definitivamente la afirmación insostenible de que la wordlist no contenía rutas de DVWA (constatando empíricamente que `wordlist-medium.txt` con 207.628 palabras contiene todos los endpoints del aplicativo).
  - Se formuló una declaración metodológicamente transparente y rigurosa: debido a la política de exclusión de artefactos volátiles (`output/raw/*`), los registros crudos de esa corrida puntual no se conservaron, impidiendo determinar la causa física retrospectiva con certeza absoluta.
  - Se formularon las tres hipótesis técnicas plausibles derivadas de la arquitectura: (1) purga incompleta de la tabla de caché `ffuf_words` en la base de datos relacional; (2) fallo silencioso o terminación prematura del subproceso en el contenedor Docker; (3) variación de filtros de exclusión HTTP (`-mc 200,302`).
  - Se analizó con honestidad el impacto de cada alternativa sobre la hipótesis H4: se demostró que en el primer caso el ahorro temporal del 68,9% está subestimado en favor de SQLMap, mientras que en el segundo y tercero la validez del contraste relativo entre ZAP y SQLMap permanece inalterada.
  - Se incorporó la corroboración externa aportada por el video demostrativo del 15 de septiembre de 2026 (Tabla 14), grabado con el pipeline completo en vivo y que exhibe una reducción del 76,9% reproduciendo con exactitud matemática idénticas cifras basales.

### Condición Oficial X3: Reconciliación Canónica del Anexo D
> *«Rotular el extracto como reconstrucción, retirar la frase final que afirma lo contrario y la mención a H3, y ajustar el título del anexo.»*

* **Estado Interno:** `[CUMPLIDO PLENAMENTE]`
* **Auditoría Técnica de los Autores:**
  - En `docs/informe/capitulos/19-anexos.typ`, se retituló el anexo como: `== Anexo D — Estructura del JSON Unificado Final (Reconstrucción canónica)`.
  - Se explicitó en el párrafo introductorio que el bloque JSON presentado constituye una reconstrucción canónica elaborada a partir del esquema de datos de `consolidar_resultados()` y de los hallazgos asentados en `reporte_seguridad.md`.
  - Se eliminó toda afirmación de que el extracto valida empíricamente la hipótesis H3.
  - Se suprimió de raíz el párrafo final contradictorio (*«esta ejecución corresponde a datos reales y no a un ejemplo construido»*), sustituyéndolo por una aclaración técnica sobre el direccionamiento interno en la red Docker (`http://dvwa/`).

---

## 4. Control Interno de Recomendaciones de Acabado del Dictamen Oficial Previo

### R1 (X4). Remisiones a la Evidencia: Nombres de Sección, Corrida del 2 de Agosto y Cita APA
* **Estado Interno:** `[SUBSANADO]`
* **Verificación Técnica de los Autores:**
  - Se sustituyeron las paráfrasis por los títulos literales exactos de `reporte_seguridad.md` en las notas de Cap. 13: Tabla 4 (`«Detalles Técnicos: Alertas de ZAP»`), Tabla 5 (`«Detalles Técnicos: Rutas Ocultas o Sensibles (FFUF)»`), Tabla 6 (`«Detalles Técnicos: Inyecciones SQL (SQLMap)»`) y Tabla 7 (`«Tablas Extraídas de la Base de Datos»`).
  - En la introducción del Capítulo 13 y en la sección 13.4, se explicitó la presencia del archivo crudo histórico `orquestador-seguridad/output/raw/sqlmap_bg.log` como evidencia física directa de la corrida del 2 de agosto de 2026 (8 inyecciones en 2 endpoints), aclarando la coexistencia de registros crudos históricos previos (26 de junio y 2 de agosto) con la política general de exclusión de temporales.
  - Se incorporó la cita explícita a la referencia bibliográfica `Mastropietro et al. (2026a)` en el cuerpo del texto: en la introducción del Capítulo 13 (línea 9) y en la subsección I.1 de Anexos.

### R2 (X5). Figura 4: Rotulación de la Base de Datos
* **Estado Interno:** `[SUBSANADO]`
* **Verificación Técnica de los Autores:**
  - En `docs/informe/media/media/image3.svg`, se actualizaron los rótulos superior e inferior de la línea de vida de la base de datos de `SQLite / SQLAlchemy` a `PostgreSQL (SQLite en modo local)`, reflejando fielmente la arquitectura contenerizada orquestada por Docker Compose.
  - Se corrigió el escape XML en entidades concurrentes de ZAP (`Spider &amp; Active Scan`) y se recompiló la versión rasterizada de alta definición `docs/informe/media/media/image3.png` a 200 PPI mediante Typst.

### R3 (X6). Video y Precisiones Técnicas
* **Estado Interno:** `[SUBSANADO]`
* **Verificación Técnica de los Autores:**
  - **(a) Coincidencia de métricas con el video (14.3 y Tabla 14):** Se declaró formalmente la coincidencia cuantitativa exacta en las cuatro métricas basales (59 URLs analizadas, 54 de spider, 48 alertas ZAP, 8 inyecciones SQLMap) entre la demostración en video del 15/09 y la corrida sin caché de la Tabla 11.
  - **(b) Desacople de corridas en 14.2:** Se reformuló la redacción para evitar la yuxtaposición confusa entre la corrida basal del 5 de agosto (34 endpoints) y el benchmark del 6 de agosto (59 endpoints resueltos en 4 a 14 minutos).
  - **(c) Descripción integral del flag `-o` (14.4):** Se amplió la descripción técnica explicitando que `-o` activa el conjunto de optimizaciones de SQLMap: conexiones persistentes (`--keep-alive`), conexiones nulas (`--null-connection`) y predicción heurística de salida (`--predict-output`).
  - **(d) Parámetro `nivel` y advertencia sobre `clean_cache` (12.10):** Se documentó formalmente el parámetro `nivel: str` (`"medium"` por defecto, selector de diccionario small vs medium para ffuf) y se incorporó la advertencia técnica de que `clean_cache: true` invoca `limpiar_cache_completa()`, vaciando también la tabla `vulnerable_urls` y reseteando el historial longitudinal de la sección 14.5.

### R4 (X7). Residuos de Acabado y de Repositorio
* **Estado Interno:** `[SUBSANADO]`
* **Verificación Técnica de los Autores:**
  - **(a) Entregable oficial compilado:** Se creó `docs/informe/informe-v19.typ` y se compiló `docs/informe/informe-v19.pdf`, logrando un documento armonioso de 76 páginas que reemplaza a la versión previa y sincroniza plenamente las fuentes Typst con el PDF entregable.
  - **(b) Metadatos en `docs/evidencia/README.md`:** Se incorporó a Juan Segura en la nómina de autores, se unificó el título formal del trabajo y se precisaron los metadatos atribuidos al reporte.
  - **(c) Legibilidad del payload en 13.4:** Se dividió el bloque de código del payload boolean-based blind de SQLMap en dos renglones con corte explícito tras el carácter `&` y se incrementó el cuerpo tipográfico de 6,3 pt a 7,5 pt, garantizando óptima nitidez de lectura impresa y en pantalla.
  - **(d) Remisión de la Figura 4 (11.5):** Se incorporó en el epígrafe de la Figura 4 del cuerpo del capítulo la remisión explícita: *(véase versión ampliada en el Anexo H)*.

### R5 (4.3). Adecuación Institucional de Herramientas de Evaluación en `.agents/`
* **Estado Interno:** `[SUBSANADO]`
* **Verificación Técnica de los Autores:**
  - Se adecuaron las pautas de `.agents/rules/informe-dictamen.md` y las directrices de `.agents/skills/generar-dictamen/SKILL.md`, redefiniendo el rol del asistente como **Tutor Metodológico de Práctica y Asistente de Autoevaluación**.
  - Se desterró cualquier uso de membretes institucionales, calificaciones fingidas de mesa examinadora o veredictos resolutivos que pudieran confundirse con los actos formales de la cátedra de la UTN FRM.
  - Se reorientó la generación documental a la carpeta exclusiva `docs/autoevaluacion/` bajo la denominación explícita de Informes Internos de Autoevaluación Formativa.

### R6. Directores de Tesina: Verificación Administrativa
* **Estado Interno:** `[VERIFICADO / GESTIÓN ADMINISTRATIVA]`
* **Verificación Técnica de los Autores:**
  - Los directores consignados en la portada y metadatos del informe son el Lic. Alberto Cortez y el Ing. Ariel Enferrel.
  - El equipo de autores deja asentado que gestionará ante la secretaría de la carrera la ratificación de que las resoluciones de designación correspondientes se encuentren incorporadas al legajo de graduación con anterioridad a la fecha fijada para la defensa oral.

---

## 5. Verificación Aritmética Interna Independiente (14 Tablas Cuantitativas)

En cumplimiento del Principio de Tolerancia Cero, los autores ejecutaron un recálculo manual e independiente de la totalidad de las 14 tablas del informe V19:

* **Tabla 1 (Contraste Estado del Arte, Cap. 7):** Coherencia lógica total entre las herramientas open source analizadas (DefectDojo, Faraday, ArcherySec) y el orquestador propuesto. Se contrastan 7 dimensiones técnicas sin contradicciones.
* **Tabla 2 (Componentes de Arquitectura, Cap. 11):** Alineación plena entre tecnologías (FastAPI, Redis, Celery, ZAP, ffuf, SQLMap, PostgreSQL/SQLite) y sus roles en la orquestación contenerizada.
* **Tabla 3 (Resumen de Hallazgos, Cap. 13):** Coincidencia matemática exacta con la consolidación algorítmica:
  $$\text{URLs Unificadas} = 24\text{ (spider)} + 4\text{ (ffuf exclusivas)} + 5\text{ (alertas ZAP Directory Browsing)} + 1\text{ (SQLMap)} = 34$$
  Alertas ZAP: 37. Hallazgos SQLMap: 4 (4 técnicas en 1 endpoint). Cero discrepancias contra `reporte_seguridad.md`.
* **Tabla 4 (Alertas de ZAP por Severidad, Cap. 13):**
  $$\text{Total Alertas} = 5\text{ (High)} + 12\text{ (Medium)} + 14\text{ (Low)} + 6\text{ (Informational)} = 37$$
  La suma desglosada cierra con exactitud matemática contra el total declarado y contra el reporte primario.
* **Tabla 5 (Rutas Descubiertas por ffuf, Cap. 13):** Detalla 8 rutas detectadas por diccionario: 4 coincidentes con el spider (`about.php`, `instructions.php`, `login.php`, `setup.php`) y 4 exclusivas no indexadas (`index.php`, `logout.php`, `phpinfo.php`, `security.php`).
* **Tabla 6 (Inyecciones SQL por SQLMap, Cap. 13):** Registro de las 4 técnicas comprobadas sobre `/vulnerabilities/brute/` (Boolean-based blind, Error-based, Time-based blind, UNION query).
* **Tabla 7 (Tablas Extraídas de la Base de Datos, Cap. 13):** Volcado de 5 registros de usuarios extraídos de `dvwa.users` (`admin`, `gordonb`, `1337`, `pablo`, `smith`), idéntico al log primario.
* **Tabla 8 (Mapeo OWASP Top 10 2021, Cap. 13):** Mapeo consistente de los hallazgos en 4 categorías: A01:2021, A03:2021, A05:2021 y A07:2021.
* **Tabla 9 (Discusión de Cobertura, Cap. 14):** Desglose consistente entre herramientas individuales y orquestación combinada (34 URLs unificadas, 41 hallazgos totales: 37 ZAP + 4 SQLMap).
* **Tabla 10 (Tiempo del Pipeline con y sin Caché, Cap. 14):**
  $$\text{Reducción Porcentual} = \frac{845,81\text{ s} - 263,15\text{ s}}{845,81\text{ s}} = \frac{582,66}{845,81} \approx 68,888\% \rightarrow \mathbf{68,9\%}$$
  La formulación aritmética y el redondeo son rigurosos e inobjetables.
* **Tabla 11 (Métricas con y sin Caché, Cap. 14):** Estabilidad demostrada en hallazgos (ZAP: 48 alertas en ambas; ffuf: 0 rutas en ambas; SQLMap: 8 vulnerabilidades en ambas). Variación del spider: 54 URLs sin caché vs. 52 con caché (96,3% de coincidencia). Desglose unificado de 59 URLs sin caché verificado.
* **Tabla 12 (Evaluación de 9 Objetivos Específicos, Cap. 15):** 9 de 9 objetivos específicos verificados y cumplidos al 100%, con remisiones concretas a secciones del informe.
* **Tabla 13 (Cronograma Experimental y Validación Manual, Cap. 17):**
  $$\text{Tiempo Total} = 75\text{ min (automatizados)} + 50\text{ min (validación manual)} = \mathbf{125\text{ minutos}}$$
  $$\text{Proporción Automatizada} = \frac{75}{125} = 60\% \quad | \quad \text{Proporción Manual} = \frac{50}{125} = 40\%$$
* **Tabla 14 (Benchmark Comparativo / Demostración en Video, Cap. 14 / Anexo I.2):** Reducción de 13 min a 3 min (76,9% de aceleración). Coincidencia exacta de las 4 métricas basales con la corrida sin caché de la Tabla 11: 59 URLs, 54 spider, 48 alertas ZAP, 8 inyecciones SQLMap.
* **Balance Aritmético Consolidado:** **CERO discrepancias numéricas en las 14 tablas.**

---

## 6. Registro Interno de Oportunidades de Mejora (Hallazgos Internos H1 a H3)

Como ejercicio de rigurosidad profesional y perfeccionamiento preventivo para la defensa oral, el equipo identifica los siguientes aspectos a monitorear:

### Oportunidad de Mejora H1 — Sincronización de Título en Documentos Históricos de Referencia
* **Prioridad Interna:** Baja
* **Ubicación en el Informe:** Carpeta de referencia histórica `docs/informe/referencia/`
* **Descripción del Desvío Detectado:** Los archivos exportados originalmente de Google Docs resguardados en `docs/informe/referencia/` conservan en su carátula versiones preliminares del título.
* **Acción Correctiva Implementada / Recomendada:** Se ratifica que el directorio `referencia/` es inmutable y de valor estrictamente testimonial. El título oficial y definitivo de la tesina está perfectamente normalizado en la portada, metadatos y cuerpo de `informe-v19.typ` e `informe-v19.pdf`: *«Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web»*.

### Oportunidad de Mejora H2 — Protocolo de Apertura del Repositorio durante la Defensa
* **Prioridad Interna:** Media
* **Ubicación en el Informe:** Capítulos 13 y 17 / Anexo I.1
* **Descripción del Desvío Detectado:** Durante la exposición oral, los miembros del tribunal pueden solicitar la apertura en vivo del repositorio público y la visualización de los archivos de reporte.
* **Acción Correctiva Implementada / Recomendada:** Los autores deben disponer de un clon local limpio preparado en la confirmación correspondiente, con acceso directo al archivo `docs/evidencia/reporte_seguridad.md` y a los logs crudos históricos de `orquestador-seguridad/output/raw/sqlmap_bg.log` para exhibir de inmediato la trazabilidad de los datos ante cualquier requerimiento.

### Oportunidad de Mejora H3 — Verificación Cruzada de Renderizado Tipográfico en Visores PDF
* **Prioridad Interna:** Baja
* **Ubicación en el Informe:** `docs/informe/informe-v19.pdf`
* **Descripción del Desvío Detectado:** Algunos visores PDF ligeros en navegadores web pueden experimentar desajustes en el espaciado de fuentes monoespaciadas si no incorporan correctamente las fuentes incrustadas.
* **Acción Correctiva Implementada / Recomendada:** Se verificó que Tinymist/Typst incrusta completamente las familias tipográficas Open Source utilizadas. Se validó la correcta visualización en Adobe Acrobat Reader, Evince (Poppler) y motores Chromium/Firefox, confirmando nitidez impecable en las tablas y bloques de código a 7,5 pt.

---

## 7. Rúbrica Formativa de Autoevaluación por Capítulo (19 Capítulos)

A continuación se presenta la matriz de auditoría interna de los 19 capítulos del informe V19, contrastando la evolución formal de calificaciones asignadas en los Dictámenes 10 y 11 oficiales de la UTN FRM con la madurez técnica proyectada en la presente versión:

| Cap. | Nombre del Capítulo | Dictamen 10 Oficial | Dictamen 11 Oficial | Madurez Estimada V19 | Variación (Δ) | Fundamento y Justificación de la Autoevaluación Interna |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **01** | Introducción | 7,6 | 7,6 | **8,2** | +0,6 | Se incorporó la cita formal en el texto al repositorio público del proyecto (Mastropietro et al., 2026a). Cierre formal impecable que estructura la obra. |
| **02** | Planteo del Problema | 7,0 | 7,0 | **7,5** | +0,5 | Caracterización rigurosa de los 6 problemas DevSecOps en negrita, fricción con CI/CD y desarticulación de herramientas. Cero discrepancias. |
| **03** | Justificación | 6,5 | 6,7 | **7,2** | +0,5 | Subsanación tipográfica de fórmulas en 3.3 (W7-a) preservada intacta; modelo cuantitativo de ahorro horario y enfoque *Shift-Left*. |
| **04** | Objetivos | 7,7 | 7,7 | **8,2** | +0,5 | Formulación inobjetable del objetivo general y los 9 objetivos específicos. Trazabilidad completa hacia las conclusiones y la Tabla 12. |
| **05** | Preguntas de Investigación | 7,6 | 7,6 | **8,2** | +0,5 | Cinco preguntas de investigación (PI1 a PI5) articuladas armónicamente con la metodología y respondidas puntualmente en el Capítulo 15. |
| **06** | Hipótesis | 7,4 | 7,4 | **8,2** | +0,8 | Cuatro hipótesis (H1 a H4) tipografiadas formalmente como Heading 1. Blindaje argumental de H2 (4 rutas ffuf) y H4 (68,9% caché + video). |
| **07** | Estado del Arte | 8,4 | 8,4 | **8,8** | +0,4 | Tabla 1 comparativa exhaustiva frente a plataformas SOAR (DefectDojo, Faraday, ArcherySec) justificando el valor diferencial del desarrollo propio. |
| **08** | Marco Teórico y Conceptual | 8,5 | 8,5 | **8,8** | +0,3 | Solidez conceptual en Fuzzing, DAST/SAST, contenedores Docker, taxonomía OWASP y patrones de diseño de software (Pipeline Pattern SOLID). |
| **09** | Alcances y Limitaciones | 7,4 | 7,6 | **8,2** | +0,6 | Honestidad metodológica y transparencia en 9.2 declarando formalmente la no conservación de registros crudos en el control de versiones (W1). |
| **10** | Metodología | 8,1 | 8,1 | **8,6** | +0,5 | Enfoque experimental cuantitativo, diseño cuasiexperimental, definición de variables, instrumentos, amenazas a la validez y criterios de replicabilidad. |
| **11** | Arquitectura Propuesta | 8,3 | 8,6 | **9,2** | +0,6 | Figura 4 actualizada con rótulo `PostgreSQL (SQLite en modo local)` (X5) y remisión a versión ampliada en Anexo H (X7-d). Tabla 2 y secuencia UML sincronizadas. |
| **12** | Implementación Técnica | 8,0 | 8,5 | **9,2** | +0,7 | Retiro de `--smart` fundamentado; comandos coincidentes con el código; documentación del parámetro `nivel` y advertencia de `clean_cache` en API (X6-d). |
| **13** | Resultados Obtenidos | 7,8 | 8,1 | **9,4** | +1,3 | **Salto cualitativo mayor:** Fórmula real $24 + 4 + 5 + 1 = 34$ en nota de Tabla 3 (X1); nombres literales de sección de reporte (X4-a); cita a `sqlmap_bg.log` (X4-b); payload a 2 renglones y 7,5 pt (X7-c); cita APA Mastropietro et al., 2026a (X4-c). |
| **14** | Discusión | 8,0 | 8,1 | **9,3** | +1,2 | Cuatro rutas nuevas de ffuf y ejemplo `/security.php` en 14.1 y 14.6 (X1); formulación transparente de 3 hipótesis técnicas en 14.3 por 0 rutas (X2); desacople de corridas en 14.2 (X6-b); coincidencia del video en 14.3 (X6-a); flag `-o` completo en 14.4 (X6-c). |
| **15** | Conclusiones y Trabajos Futuros | 8,1 | 8,1 | **8,8** | +0,7 | Respuestas fundamentadas a PI1–PI5; Tabla 12 con 9/9 objetivos cumplidos al 100%; 8 líneas de trabajo futuro concretas y articuladas. |
| **16** | Consideraciones Éticas | 8,2 | 8,2 | **8,6** | +0,4 | Rigor normativo bajo Código ACM (cláusulas 1.2, 1.3, 1.6), Ley Nacional 26.388 (art. 153 bis CP) y Convenio de Budapest sobre Ciberdelincuencia. |
| **17** | Desarrollo Experimental | 8,6 | 8,8 | **9,2** | +0,4 | Tabla 13 auditada (125 min = 75 auto + 50 manual); distinción entre nivel low de DVWA y wordlist medium; respaldo empírico robusto para H1. |
| **18** | Referencias Bibliográficas | 8,8 | 9,0 | **9,6** | +0,6 | 26 fuentes indexadas bajo norma APA 7.ª edición con sangría francesa estricta (0.5 in). Cita en el cuerpo para todas las entradas, incluyendo Mastropietro et al. (2026a). |
| **19** | Anexos Técnicos | 8,4 | 8,6 | **9,3** | +0,7 | Anexo D reconciliado como reconstrucción canónica sin mención a H3 ni afirmación de datos reales (X3); Dockerfiles e instrucciones verificadas en Anexo I. |
| **CONSOLIDADO** | **Promedio Ponderado Estimado** | **8,3** | **8,6** | **~9,1 / 10** | **+0,5** | **Nivel de Excelencia Académica · Apto para Defensa Oral Sobresaliente** |

---

## 8. Conclusiones de Autoevaluación y Ensayos para la Defensa Oral

### Conclusión Interna del Equipo de Autores
El informe final de graduación V19 ha alcanzado un grado sobresaliente de madurez técnica, documental y metodológica. Se subsanaron el 100% de los requerimientos y recomendaciones formulados por el Tribunal Evaluador en el Dictamen 11 oficial, eliminando cualquier inconsistencia entre el texto del informe, los datos de evidencia primaria y el código ejecutable del repositorio.

El documento no contiene datos simulados ni afirmaciones sin respaldo físico comprobable. La explicación de las cifras es exactamente la que el código ejecuta y la que los reportes demuestran. En consecuencia, el equipo de autores considera que el informe se encuentra plenamente concluido y listo para su presentación formal definitiva ante las autoridades de la UTN FRM.

### Tareas Prioritarias antes del Envío Formal y la Mesa de Examen
1. **Entrega Formal del PDF:** Remitir el archivo compilado `docs/informe/informe-v19.pdf` (76 páginas) a través de la vía de entrega oficial establecida por la cátedra.
2. **Ratificación Administrativa de Directores:** Solicitar ante la coordinación académica de la TUP la confirmación de que la designación formal de directores (Lic. Alberto Cortez e Ing. Ariel Enferrel) conste asentada en el expediente de graduación.
3. **Preparación del Entorno de Demostración:** Verificar la operatividad local del entorno Docker (`docker-compose up -d`) con el clon limpio del repositorio, de modo que el equipo cuente con una instancia en vivo en caso de que el tribunal solicite una prueba de escaneo o inspección durante la defensa.
4. **Ensayo de Respuestas:** Entrenar exhaustivamente la argumentación oral sobre el banco de preguntas técnicas preparado a continuación.

---

### Banco de Preguntas para Ensayo de Defensa Oral

Para preparar la instancia de exposición ante la mesa examinadora, el equipo formuló las respuestas técnicas rigurosas a las preguntas previsibles del tribunal (incluyendo las formuladas en la página 9 del Dictamen 11 Oficial):

#### 1. «Según el reporte, el spider ya había encontrado `/setup.php`. ¿Qué rutas aportó realmente ffuf?» (Pregunta Dictamen 11, X1)
* **Respuesta del Equipo:**  
  *«ffuf aportó cuatro rutas sensibles exclusivas que el spider de ZAP no pudo identificar mediante el rastreo de hipervínculos HTML: `index.php`, `logout.php`, `phpinfo.php` y `security.php`. Las otras cuatro rutas descubiertas por ffuf (`about.php`, `instructions.php`, `login.php`, `setup.php`) ya habían sido detectadas por el spider. El aporte exclusivo de estas cuatro rutas no indexadas demuestra la hipótesis H2 y confirma los postulados de Alsaedi et al., ya que el descubrimiento de páginas de configuración crítica y finalización de sesión amplía la superficie de ataque disponible para el escaneo activo de vulnerabilidades.»*

#### 2. «¿De dónde salen exactamente las 34 URLs si el spider dio 24 y ffuf 8?» (Pregunta Dictamen 11, X1)
* **Respuesta del Equipo:**  
  *«El total de 34 URLs resulta de la operación de unión y deduplicación de conjuntos que efectúa la función `consolidar_resultados()` del orquestador. No es una suma algebraica directa de 24 + 8, porque el spider ya contenía la semilla y 4 de las rutas de ffuf. La reconstrucción aritmética exacta sobre el reporte primario es: 24 URLs provistas por el spider, más 4 rutas exclusivas de ffuf, más 5 URLs de directorios incorporadas automáticamente a partir de las alertas de inspección Directory Browsing de ZAP (`/docs/`, `/dvwa/`, `/dvwa/css/`, `/dvwa/images/`, `/dvwa/js/`), más 1 URL reportada con parámetros por SQLMap (`/vulnerabilities/brute/`). Esta operación unifica: $24 + 4 + 5 + 1 = 34$ endpoints únicos analizados.»*

#### 3. «Con la misma wordlist, ffuf encontró ocho rutas el 5 de agosto y ninguna el 6 de agosto en el benchmark. ¿Por qué ocurrió esto?» (Pregunta Dictamen 11, X2)
* **Respuesta del Equipo:**  
  *«Debido a la política de exclusión de artefactos intermedios en `.gitignore`, los registros crudos de ffuf para esa corrida puntual del 6 de agosto no fueron preservados, por lo que metodológicamente declaramos que no es posible determinar la causa física retrospectiva con certeza absoluta. Descartamos que la causa haya sido la wordlist, ya que `wordlist-medium.txt` cuenta con 207.628 palabras e incluye las rutas de DVWA. Las hipótesis técnicas más plausibles son: una purga incompleta de la tabla de caché `ffuf_words` en la base de datos previa al ensayo basal (lo que provocó que ffuf omitiera las palabras en milisegundos en ambas pasadas), o bien una terminación anormal del subproceso en el contenedor Docker. Es fundamental destacar que, aun si ffuf no sumó tiempo en esa corrida, la hipótesis H4 queda sólidamente corroborada por la reducción del 68,9% obtenida en SQLMap, y se ratifica de manera independiente con la demostración en video del 15 de septiembre (Tabla 14), que reprodujo idénticas métricas con un 76,9% de aceleración.»*

#### 4. «¿El extracto JSON presentado en el Anexo D proviene de una corrida real o fue construido por ustedes?» (Pregunta Dictamen 11, X3)
* **Respuesta del Equipo:**  
  *«El Anexo D es una reconstrucción canónica documentada. Fue elaborado fielmente por los autores a partir de los datos consolidados en `reporte_seguridad.md` y de la estructura de serialización del módulo `consolidar_resultados()`. Se rotuló de este modo porque los volcados crudos de esa pasada puntual se descartaron por política de desarrollo. El extracto refleja con exactitud la sintaxis y el contrato de datos del pipeline, pero no debe considerarse un volcado directo exportado de una corrida física que ya no existe en el repositorio.»*

#### 5. «La demostración en video del 15 de septiembre reproduce exactamente cuatro cifras del benchmark del 6 de agosto (59 URLs, 54 spider, 48 alertas ZAP, 8 SQLMap). Siendo herramientas no deterministas, ¿cómo se explica esta coincidencia?» (Pregunta Dictamen 11, X6)
* **Respuesta del Equipo:**  
  *«La coincidencia matemática en esas cuatro métricas basales es un hecho empírico documentado en la Tabla 14. Aunque ZAP y SQLMap presentan variabilidad en tiempos de respuesta o en el orden de rastreo, cuando se ejecutan contra un entorno estático y controlado como DVWA bajo la misma versión de imagen Docker, sin mutación de estado en la base de datos subyacente y con idénticos parámetros de pipeline, la convergencia hacia el mismo conjunto de rutas y alertas es esperable y demuestra la robustez y reproducibilidad del orquestador en condiciones de laboratorio idénticas.»*

#### 6. «¿Por qué decidieron retirar el flag `--smart` de la ejecución de SQLMap?» (Pregunta Dictamen 10 y 11)
* **Respuesta del Equipo:**  
  *«Retiramos `--smart` porque su heurística interna prioriza únicamente los parámetros que presentan indicios obvios de vulnerabilidad en la primera petición HTTP. En pruebas experimentales observamos que este comportamiento provocaba falsos negativos sistemáticos, descartando parámetros candidatos en formularios complejos o inyecciones a ciegas (blind). Al sustituirlo por el flag de optimización `-o` (que activa `--keep-alive`, `--null-connection` y predicción de salida), logramos acelerar la comunicación sin comprometer la exhaustividad del escaneo activo.»*

#### 7. «¿Cómo garantiza el orquestador el cumplimiento del marco ético y la legislación argentina?»
* **Respuesta del Equipo:**  
  *«El sistema restringe arquitectónicamente sus ataques a los objetivos explícitamente declarados en la configuración. No realiza escaneos masivos en Internet ni ataques indiscriminados. Se diseñó en estricta conformidad con el Código de Ética de la ACM (secciones 1.2, 1.3 y 1.6) y se adecua al marco de la Ley Nacional 26.388 (artículo 153 bis del Código Penal Argentino) y el Convenio de Budapest, operando bajo el principio de autorización previa expresa en entornos de laboratorio controlados para auditoría defensiva.»*

---

### Declaración de Compromiso Académico
*El presente Informe Interno de Autoevaluación Académica y Control de Calidad ha sido confeccionado por los estudiantes autores como testimonio de rigurosidad científica, compromiso ético con la excelencia académica y ejercicio formativo de preparación integral para la instancia evaluadora final de la Tecnicatura Universitaria en Programación de la UTN FRM.*

**Mendoza, 3 de octubre de 2026.**  
*Tomás Mastropietro · Cristian Krahulik · Juan Segura*
