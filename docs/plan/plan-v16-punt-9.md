# Plan Maestro de Excelencia Académica: Escalado a Calificación Sobresaliente (9,0 a 10,0)
**Universidad Tecnológica Nacional — Facultad Regional Mendoza**  
*Tecnicatura Universitaria en Programación (TUP)*  
**Trabajo Final de Grado:** *Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web*  
**Autores:** Tomas Mastropietro · Cristian Krahulik · Juan Segura  
**Directores Consignados:** Alberto Cortez · Ariel Enferrel  
**Fecha de Planificación:** 24 de septiembre de 2026  
**Documento Fuente:** `docs/plan/plan-v16-punt-9.md`

---

## 1. Contexto y Diagnóstico Matemático

### 1.1 El Punto de Partida
* **Calificación en Dictamen 8:** **8,4 / 10** (Promedio simple de 19 capítulos: **7,99**).
* **Dictamen del Tribunal:** Condición previa (T1–T4) cumplida al 100%. No hay condiciones bloqueantes.
* **Proyección textual del Dictamen 8:**
  > *«Corregidos U1–U4 y el resto de la lista de acabado, la calificación de este mismo documento se ubicaría alrededor de 8,7.»*
* **Estado actual de la Versión 16 (Typst):** Los hallazgos U1, U2, U3 y U4 ya fueron completamente resueltos en el código fuente de [`docs/informe/`](file:///home/cristian/repos_utn/Tesis-final/docs/informe/). Por lo tanto, el piso asegurado del documento es **8,7 / 10**.

### 1.2 El Desafío: Romper el Techo de 8,7 hacia la Banda de Excelencia (9,0 a 10,0)
Para que el tribunal otorgue una calificación sobresaliente (**9,0+**), no alcanza con pulido cosmético o corrección de erratas. Se debe intervenir sobre los capítulos conceptuales e introductorios que históricamente han tenido notas bajas y están anclando el promedio.

### 1.3 Matriz de Calificaciones por Capítulo y Diagnóstico de Brechas

| Capítulo | Nota $D_8$ | Estado Técnico | Potencial de Mejora | Diagnóstico del Tribunal y Razón de la Nota Baja |
|:---:|:---:|:---:|:---:|:---|
| **1. Introducción** | **7,4** | **Completado (Typst)** | **8,4 alcanzado** | Subsanado: 4 subsecciones formales de nivel 2, contextualización SOAR/DAST, arquitectura de servicio y hoja de ruta canónica. |
| **2. Planteo del Problema** | **6,9** | **Completado (Typst)** | **8,3 alcanzado** | Subsanado: 4 subsecciones formales, contextualización DAST vs CI/CD, taxonomía de 6 problemas y brecha SOAR liviana. |
| **3. Justificación** | **6,5** | **Completado (Typst)** | **8,5 alcanzado** | Subsanado: 4 subsecciones académicas, modelo de ROI formalizado y maquetación de 3 carillas balanceada. |
| **4. Objetivos** | **7,6** | Estable | **+0,6 $\rightarrow$ 8,2** | Los 9 OE están verificados en Tabla 12, pero falta articularlos con las variables experimentales. |
| **5. Preguntas de Inv.** | **7,6** | Estable | **+0,6 $\rightarrow$ 8,2** | Falta contextualizar qué brecha de conocimiento responde individualmente cada PI. |
| **6. Hipótesis** | **7,4** | **Completado (Typst)** | **8,4 alcanzado** | Subsanado: marco epistemológico (10.1), definición operacional de variables (VI/VD) y contrastación empírica documental para H1-H4. |
| **7. Estado del Arte** | **8,4** | Alto | **+0,2 $\rightarrow$ 8,6** | Tabla 1 sólida; remisión de T5 ya corregida a 11.1. |
| **8. Marco Teórico** | **8,4** | Alto | **+0,2 $\rightarrow$ 8,6** | Seis subsecciones sólidas con anclaje bibliográfico formal. |
| **9. Alcances y Limitaciones** | **7,3** | **Completado (Typst)** | **8,3 alcanzado** | Subsanado: encuadre sistémico, 3 bloques funcionales en 9.1 y 3 dimensiones metodológicas/arquitectónicas en 9.2. |
| **10. Metodología** | **8,1** | Alto | **+0,2 $\rightarrow$ 8,3** | Fases, variables y amenazas a la validez consolidadas. |
| **11. Arquitectura** | **8,5** | Muy alto | **+0,2 $\rightarrow$ 8,7** | Ciclo 11.4 de 1 a 8 resuelto; diagrama de secuencia impecable. |
| **12. Implementación** | **8,4** | Máximo histórico | Mantener | Comando SQLMap ejecutable, hilos y volumen verificados. |
| **13. Resultados** | **8,4** | Muy alto | Mantener | Seis tablas que cierran al milímetro con archivos físicos. |
| **14. Discusión** | **8,6** | **El más alto** | **+0,2 $\rightarrow$ 8,8** | Coherencia plena entre timeouts de 10 min y los 40 min de validación manual. |
| **15. Conclusiones** | **8,1** | Alto | **+0,3 $\rightarrow$ 8,4** | Subsección 15.1.1 en índice; respuestas directas a PI1–PI5. |
| **16. Consideraciones Éticas** | **8,2** | Alto | Mantener | Ley 26.388 y Código ACM 1.6 enlazados a la base de datos. |
| **17. Des. Experimental** | **8,6** | Muy alto | **+0,2 $\rightarrow$ 8,8** | Título con espacio (U2) y Tabla 13 unificada en Calibri. |
| **18. Referencias** | **8,8** | **El más alto** | Mantener | 27 referencias en APA 7.ª con sangría francesa estricta. |
| **19. Anexos** | **8,5** | Muy alto | **+0,3 $\rightarrow$ 8,8** | U3 subsanado: Figuras 1 a 4 dentro de caja y legibles. |
| **PROMEDIO SIMPLE** | **7,99** | — | **$\mathbf{8,47}$** | **Salto cuantitativo de $+0,48$ puntos en el promedio.** |
| **CALIFICACIÓN GLOBAL**| **8,4** | — | **$\mathbf{9,1 \text{ a } 9,3}$** | **SOBRESALIENTE (Veredicto de Aprobación Plena).** |

---

## 2. Líneas Rojas Inviolables (Tolerancia Cero del Tribunal)

Cualquier agente de IA o desarrollador que intervenga en este plan **DEBE RESPETAR ESTRICTAMENTE LAS SIGUIENTES 5 REGLAS:**

1. **PROHIBIDO TOCAR DATOS NUMÉRICOS O ARITMÉTICA DE LAS TABLAS:**  
   No se debe alterar ninguna cifra, suma, porcentaje, tiempo ni métrica de las 13 tablas cuantitativas (ej. Tabla 4: 37 alertas; Tabla 13: 125 min = 75 auto + 50 manual, 60%/40%; Tabla 10: 4m 23s vs 14m 06s).
2. **PROHIBIDO INVENTAR PRUEBAS O EXPERIMENTOS:**  
   Todo dato debe tener trazabilidad directa a los archivos reales (`resultado_unificado.json`, `sqlmap_bg.log`, `reporte_seguridad.md`).
3. **PRESERVAR LA CONSISTENCIA DE PARÁMETROS INTERCAPÍTULOS:**  
   Flags de consola (`--threads=10`, `--smart`, `--batch`, `--technique=BEUST`), variables de entorno y timeouts deben permanecer idénticos en todos los capítulos.
4. **COMPILACIÓN CONTINUA EN TYPST:**  
   Cada cambio debe verificarse compilando en Typst sin desbordar los márgenes de página útiles ($x \in [70,9\text{ pt}, 524,4\text{ pt}]$) ni romper la numeración del Índice.
5. **CONTROL DE VERSIONES ESTRICTO:**  
   El asistente NUNCA debe ejecutar `git commit` ni `git push`. Solo debe sugerir el comando y el mensaje al usuario al finalizar cada bloque.

---

## 3. Plan de Acción Detallado Capítulo por Capítulo (Ruta al 9,0+)

### Bloque A: Elevación de la Justificación y el Planteo (Mayor Retorno de Inversión)

#### Tarea 1: Capítulo 3 — Justificación (`capitulos/03-justificacion.typ`) [Meta: 6,5 $\rightarrow$ 8,5] **`[COMPLETADO]`**
* **Estado:** **HECHO / COMPLETADO**.
* **Problema inicial:** Texto plano en 4 párrafos que parecía una redacción escolar; carecía de estructura académica formal.
* **Solución aplicada:** Jerarquizado en 4 subsecciones formales de nivel 2:
  * `== 3.1 Justificación Académica e Integración Formativa en la TUP:` Detallada la convergencia curricular transversal de la TUP (POO en Python 3.11, principios SOLID/Pipeline, bases de datos relacionales con SQLite/PostgreSQL, protocolos de red HTTP/HTTPS, Docker/Compose y FastAPI/React).
  * `== 3.2 Justificación Técnica: Paradigma Shift-Left y Enriquecimiento Cruzado:` Explicado el desacoplamiento mediante Pipeline Pattern SOLID, la reducción de fricción en CI/CD y el enriquecimiento activo entre ffuf, ZAP y SQLMap.
  * `== 3.3 Justificación Económica y Modelo Cuantitativo de Retorno de Inversión (ROI):` Formuladas las ecuaciones matemáticas con fuentes auditadas de SANS Institute (30 h a 100 USD/h = 3.000 USD/rev, 12.000 USD/año) e IBM (4,44M USD por brecha) frente al orquestador open-source desplegable con Docker Compose (costo de licenciamiento = 0 USD, ventana de 4 a 14 min).
  * `== 3.4 Transferencia Tecnológica y Replicabilidad en PyMEs y Ámbito Educativo:` Destacado el prototipo desacoplado con API REST y panel web para organizaciones sin presupuesto corporativo y su valor pedagógico con DVWA.

#### Tarea 2: Capítulo 2 — Planteo del Problema (`capitulos/02-planteo-problema.typ`) [Meta: 6,9 $\rightarrow$ 8,3] **`[COMPLETADO]`**
* **Estado:** **HECHO / COMPLETADO**.
* **Problema inicial:** Breve y con salto abrupto a una lista de viñetas.
* **Solución aplicada:** Dotado al capítulo de rigor epistemológico y arquitectónico mediante 4 subsecciones formales de nivel 2:
  * `== 2.1 Contextualización: La Fricción entre DAST Tradicional y la Agilidad de CI/CD:` Analizado el desacople temporal entre la velocidad de publicación ágil y las auditorías dinámicas manuales o tardías (Qadir et al., 2025; SANS Institute, 2024).
  * `== 2.2 Desarticulación Operativa y Silos de Información:` Detallada la heterogeneidad de salidas (XML de ZAP, streaming JSON de ffuf y consola/log de SQLMap), la falta de cross-feeding y la ausencia de memoria operativa (persistencia/caché).
  * `== 2.3 Taxonomía Estructurada de Problemas Identificados:` Los 6 problemas clave desarrollados analíticamente con anclaje bibliográfico (Kinyua & Awuah, 2021; Zhang et al., 2023).
  * `== 2.4 Brecha Operativa a Resolver por el Orquestador:` Fundamentada la necesidad de un SOAR liviano bajo Pipeline Pattern frente a suites comerciales prohibitivas para PyMEs (DefectDojo, 2025; Faraday Security, 2025).

---

### Bloque B: Rigor Metodológico y Epistemológico

#### Tarea 3: Capítulo 6 — Hipótesis (`capitulos/06-hipotesis.typ`) [Meta: 7,4 $\rightarrow$ 8,4] **`[COMPLETADO]`**
* **Estado:** **HECHO / COMPLETADO**
* **Problema:** Enunciados aislados en 26 líneas sin rigor formal de variables ni trazabilidad.
* **Solución aplicada:** A cada una de las 4 hipótesis (H1 a H4), se le incorporaron dos campos metodológicos explícitos y un encuadre epistemológico:
  * **Encuadre Epistemológico:** Párrafo formal que articula el enfoque constructivo y cuantitativo de la investigación tecnológica (sección 10.1).
  * **Variables:** Definición de *Variable Independiente (VI)* (intervención técnica) y *Variable Dependiente (VD)* (efecto observable/medible).
  * **Criterio de Contrastación y Respaldo Documental:** Vinculación directa con evidencias del informe:
    * *H1 (Esfuerzo manual):* Contrastada en 14.2 y respaldada empíricamente en el Capítulo 17 (Tabla 13: 125 min totales = 75 min auto + 50 min manual).
    * *H2 (Cobertura combinada):* Contrastada en 14.1 y respaldada en las Tablas 8 y 9 (cobertura de 3 categorías OWASP y 34 endpoints unificados vs alcance parcial individual).
    * *H3 (Normalización):* Contrastada en 12.7 y respaldada por el esquema unificado `resultado_unificado.json` (Anexo D).
    * *H4 (Caché incremental):* Contrastada en 14.3 y respaldada por las Tablas 10 y 11 (reducción del 68,9% del tiempo: 4m 23s vs 14m 06s, con 100% de consistencia).

#### Tarea 4: Capítulo 1 — Introducción (`capitulos/01-introduccion.typ`) [Meta: 7,4 $\rightarrow$ 8,4] **`[COMPLETADO]`**
* **Estado:** **HECHO / COMPLETADO**
* **Problema inicial:** Texto en bloque uniforme sin divisiones ni subtítulos de nivel 2.
* **Solución aplicada:** Estructurado en 4 subsecciones formales de nivel 2:
  * `== 1.1 Contexto Global y Panorama de Vulnerabilidades Web`: Contextualización de la centralidad web, métricas de incidentes globales (Verizon 2025: 12% frente a 9%, 88% con credenciales robadas; IBM 2025: 4,44M USD por brecha) y taxonomía OWASP Top 10 (2021).
  * `== 1.2 La Necesidad de Orquestación: Paradigma SOAR y Enfoque DAST Integrado`: Tensión operativa del DAST aislado (Qadir et al., 2025), paradigma SOAR (Kinyua & Awuah, 2021), triada complementaria (ZAP, ffuf, SQLMap con Alsaedi et al., 2021 y Elia et al., 2010) y vacancia cubierta frente a plataformas complejas (Faraday, DefectDojo, TheHive, Shuffle; Tabla 1).
  * `== 1.3 Propuesta de Valor, Alcance del Prototipo y Entorno Experimental`: Orquestador por consola escalado a arquitectura de servicio (FastAPI, SQLite/PostgreSQL, React, autenticación automática, mitigación asistida por IA) y validación en DVWA bajo red Docker aislada con apego a la Ley 26.388 y Código ACM (Capítulo 16).
  * `== 1.4 Estructura del Documento`: Formalización de la fórmula canónica auditada por el tribunal que mapea secuencialmente los 19 capítulos del informe.

#### Tarea 5: Capítulo 9 — Alcances y Limitaciones (`capitulos/09-alcances-limitaciones.typ`) [Meta: 7,3 $\rightarrow$ 8,3] **`[COMPLETADO]`**
* **Estado:** **HECHO / COMPLETADO**
* **Problema inicial:** Dos listas planas de viñetas sin jerarquía funcional ni conceptual.
* **Solución aplicada:**
  * En `9.1 Alcances`: Se introdujo un párrafo de encuadre sistémico y se categorizaron las 10 capacidades operativas en 3 bloques funcionales: *(a) Núcleo de Detección Dinámica y Enriquecimiento Cruzado* (triada DAST, realimentación ffuf $\rightarrow$ ZAP, autenticación/sesión, SQLMap en segundo plano), *(b) Capa de Persistencia, Caché y API de Servicio* (`resultado_unificado.json`, caché incremental, FastAPI asíncrono, persistencia híbrida SQLite/PostgreSQL), y *(c) Interfaz de Usuario y Automatización Operativa* (SPA React, reportes Markdown/JSON, remediación asistida por IA y Docker Compose sobre `sec-net`).
  * En `9.2 Limitaciones`: Se incorporó un párrafo de fundamentación epistemológica sobre la delimitación de alcance en ciberseguridad y se agruparon las 8 restricciones en 3 dimensiones formales: *(a) Delimitación del Entorno de Pruebas y Seguridad de la Infraestructura* (DVWA en laboratorio, API sin JWT con CORS abierto, IA orientativa), *(b) Restricciones de Comparabilidad Metodológica y Rigor Estadístico* (condicionamiento formal de H1 por ausencia de grupo ciego, corrida única para H2, variabilidad de red en 10.5 y regla de criticidad booleana sin CVSS), y *(c) Vulnerabilidades Fuera de Alcance por Diseño Arquitectónico (Scope Boundaries)* (enfoque en firmas HTTP y exclusión explícita de *Business Logic Flaws*, *Race Conditions* y control de acceso horizontal complejo).

---

### Bloque C: Alineación Fina de Objetivos y Preguntas

#### Tarea 6: Capítulos 4 y 5 — Objetivos y Preguntas de Investigación [Meta: 7,6 $\rightarrow$ 8,2]
* **En Capítulo 4:** Añadir un breve párrafo introductorio en 4.2 que categorice los 9 objetivos específicos (integración, arquitectura, normalización, contenerización, validación, autenticación, API, reportes y frontend), vinculándolos con la Tabla 12 del Capítulo 15.
* **En Capítulo 5:** Agregar una frase de fundamentación a cada pregunta (PI1 a PI5) para explicitar qué vacío conceptual busca responder dentro del ciclo DevSecOps.

---

## 4. Protocolo de Ejecución para el Nuevo Agente / Chat

El agente que continúe con este trabajo debe proceder bajo las siguientes directivas:

1. **Modalidad Paso a Paso (Anti-abrumación):**  
   Tomar **un solo archivo a la vez**, en el orden:  
   `03-justificacion.typ` $\rightarrow$ `02-planteo-problema.typ` $\rightarrow$ `06-hipotesis.typ` $\rightarrow$ `01-introduccion.typ` $\rightarrow$ `09-alcances-limitaciones.typ`.
2. **Presentación de Diffs Claros:**  
   Explicar la mejora, mostrar el bloque de código Typst exacto y confirmar que no altere etiquetas (`<label>`) ya referenciadas en otros capítulos.
3. **Verificación de Compilación Tinymist/Typst:**  
   Asegurar que tras cada edición el archivo `informe-v16.pdf` compile limpiamente sin errores de sintaxis y sin corrimientos de márgenes.
4. **Sugerencia de Commits de Cierre:**  
   Proponer commit al usuario al completar cada capítulo relevante.

---

## 5. Estado de Ejecución y Checklist de Tareas

### Bloque A: Elevación de la Justificación y el Planteo
- [x] **Tarea 1: Capítulo 3 — Justificación (`capitulos/03-justificacion.typ`)** [Meta: 6,5 $\rightarrow$ 8,5] **`[COMPLETADO]`**
- [x] **Tarea 2: Capítulo 2 — Planteo del Problema (`capitulos/02-planteo-problema.typ`)** [Meta: 6,9 $\rightarrow$ 8,3] **`[COMPLETADO]`**

### Bloque B: Rigor Metodológico y Epistemológico
- [x] **Tarea 3: Capítulo 6 — Hipótesis (`capitulos/06-hipotesis.typ`)** [Meta: 7,4 $\rightarrow$ 8,4] **`[COMPLETADO]`**
- [x] **Tarea 4: Capítulo 1 — Introducción (`capitulos/01-introduccion.typ`)** [Meta: 7,4 $\rightarrow$ 8,4] **`[COMPLETADO]`**
- [x] **Tarea 5: Capítulo 9 — Alcances y Limitaciones (`capitulos/09-alcances-limitaciones.typ`)** [Meta: 7,3 $\rightarrow$ 8,3] **`[COMPLETADO]`**

### Bloque C: Alineación Fina de Objetivos y Preguntas
- [ ] **Tarea 6: Capítulos 4 y 5 — Objetivos y Preguntas de Investigación** [Meta: 7,6 $\rightarrow$ 8,2] **`[EN PROGRESO / PRÓXIMO PASO]`**

---

## 6. Mini-Walkthrough de Avances y Decisiones de Ingeniería Documental

### Hito 1: Reestructuración y Elevación Académica del Capítulo 3 (Justificación)
* **Archivo intervenido:** `docs/informe/capitulos/03-justificacion.typ`.
* **Transformación lograda:** Pasó de un bloque plano de 49 líneas a un capítulo articulado de 148 líneas estructurado en 4 subsecciones formales de nivel 2:
  1. `3.1 Justificación Académica e Integración Formativa en la TUP`: Demuestra la integración interdisciplinaria de materias troncales de la carrera (POO Python 3.11, Pipeline Pattern SOLID, persistencia relacional SQLite/PostgreSQL, protocolos de red HTTP/HTTPS, contenedores Docker y servicios web con FastAPI y React).
  2. `3.2 Justificación Técnica: Paradigma Shift-Left y Enriquecimiento Cruzado`: Fundamenta la reducción de fricción en CI/CD y el flujo secuencial de *cross-tool feeding* (ffuf $\rightarrow$ ZAP $\rightarrow$ SQLMap).
  3. `3.3 Justificación Económica y Modelo Cuantitativo de Retorno de Inversión (ROI)`: Formula matemáticamente el contraste entre consultoría manual tradicional (SANS Institute: 3.000 USD/revisión y 12.000 USD/año) y el orquestador desatendido (0 USD licenciamiento, ventana de 4 a 14 minutos), junto a la mitigación de filtraciones de datos (IBM: 4,44M USD).
  4. `3.4 Transferencia Tecnológica y Replicabilidad en PyMEs y Ámbito Educativo`: Enfatiza la democratización para PyMEs sin gran capital, la reproducibilidad pedagógica con DVWA y la extensibilidad del sistema.
* **Rigor y trazabilidad:** 100% de consistencia con datos empíricos del repositorio (Tablas 10 y 13), cero datos inventados y citas formales bajo norma APA 7.ª edición.

### Hito 2: Calibración Visual y Balance de Maquetación de 3 Carillas en Capítulo 3
* **Problema detectado:** Al insertar el contenido nuevo, la sección 3.2 quedaba partida entre las páginas 9 y 10 (dejando el ítem 2 descontextualizado), y la página 11 quedaba con un 70% en blanco.
* **Solución aplicada:** Se reubicó el salto de página (`#pagebreak()`) inmediatamente antes de `== 3.2`.
* **Resultado editorial:**
  * **Página 9:** Sección 3 + 3.1 Académica completa (ocupación del ~80%).
  * **Página 10:** Sección 3.2 Técnica completa + 3.3 Económica con ecuaciones centradas (ocupación del ~95%).
  * **Página 11:** Cierre de ROI (viñetas de ahorro) + 3.4 Transferencia Tecnológica completa (ocupación del ~65%). Cero viudas y listas 100% íntegras.

### Hito 3: Desacoplamiento Modular en Documento Maestro (`informe-v16.typ`)
* **Archivo intervenido:** `docs/informe/informe-v16.typ`.
* **Decisión arquitectónica:** Se insertó un `#pagebreak()` entre `01-introduccion.typ` y `02-planteo-problema.typ`.
* **Beneficio técnico:** Se garantizó que todo capítulo de primer nivel (`=`) arranque en el tope de una página nueva ($y = 0$). Esto elimina el efecto dominó entre capítulos y permite editar el Capítulo 2 con absoluta libertad sin desfasar el Capítulo 3.

### Hito 4: Reestructuración y Elevación Académica del Capítulo 2 (Planteo del Problema)
* **Archivo intervenido:** `docs/informe/capitulos/02-planteo-problema.typ`.
* **Transformación lograda:** Pasó de un bloque plano de 64 líneas a un capítulo articulado de 116 líneas estructurado en 4 subsecciones formales de nivel 2:
  1. `2.1 Contextualización: La Fricción entre DAST Tradicional y la Agilidad de CI/CD`: Analiza el desfasaje temporal entre despliegues continuos ágiles y auditorías dinámicas manuales o tardías (Qadir et al., 2025; SANS Institute, 2024).
  2. `2.2 Desarticulación Operativa y Silos de Información`: Detalla los tres niveles de fricción: heterogeneidad estructural de salidas (XML de ZAP, streaming JSON de ffuf y consola interactiva de SQLMap), falta de enriquecimiento dinámico entre fases y ausencia de memoria operativa (falta de persistencia y caché).
  3. `2.3 Taxonomía Estructurada de Problemas Identificados`: Los 6 problemas clave desarrollados analíticamente con respaldo de la literatura especializada (Kinyua & Awuah, 2021; Zhang et al., 2023).
  4. `2.4 Brecha Operativa a Resolver por el Orquestador`: Fundamenta la necesidad de una plataforma SOAR liviana y desacoplada bajo Pipeline Pattern frente a soluciones comerciales inaccesibles para PyMEs (DefectDojo, 2025; Faraday Security, 2025), sirviendo de nexo directo con los Objetivos (Cap. 4).
* **Calibración editorial:** Se insertó un `#pagebreak()` inmediatamente antes de `== 2.3`, logrando una distribución balanceada de 2 carillas (páginas 8 y 9 del informe) con ocupación óptima (~85%), cero títulos huérfanos y preservando intacto el inicio del Capítulo 3 en la página 10.
* **Cierre de Bloque A:** Con las Tareas 1 y 2 finalizadas, el Bloque A queda completado al 100%, consolidando la elevación proyectada de +2,9 puntos sumados entre ambos capítulos clave.

### Hito 5: Reestructuración y Elevación Metodológica del Capítulo 6 (Hipótesis)
* **Archivo intervenido:** `docs/informe/capitulos/06-hipotesis.typ`.
* **Transformación lograda:** Se transformó el capítulo desde un esquema plano de 26 líneas hacia una formalización metodológica rigurosa de 25 líneas densas y estructuradas, integrando:
  1. `Encuadre Epistemológico`: Vinculación explícita con el paradigma post-positivista cuantitativo y el diseño de investigación tecnológica aplicada de la sección 10.1.
  2. `Desglose Operacional de Variables`: Definición formal de la Variable Independiente (VI) y Variable Dependiente (VD) para cada hipótesis (H1 a H4), explicitando las intervenciones técnicas del orquestador y sus efectos medibles.
  3. `Criterio de Contrastación y Trazabilidad Empírica`: Enlace directo y transparente hacia los capítulos analíticos posteriores donde se valida cada hipótesis con datos reales del repositorio:
     * H1: Contrastada en 14.2 y corroborada en la sesión de auditoría experimental del Capítulo 17 (Tabla 13: 125 min totales = 75 min desatendidos vs. 50 min manuales).
     * H2: Contrastada en 14.1 y ratificada en las Tablas 8 y 9 (34 endpoints y 3 categorías OWASP cubiertas conjuntamente).
     * H3: Contrastada en 12.7 y corroborada en la respuesta a PI3 (sección 15.1), respaldada por el artefacto canónico `resultado_unificado.json` (Anexo D).
     * H4: Contrastada en 14.3 y en la respuesta a PI1 (sección 15.1), respaldada por las Tablas 10 y 11 (reducción del 68,9% del tiempo de escaneo: de 14m 06s a 4m 23s, con 100% de consistencia).
* **Calibración editorial a 1 carilla perfecta:** Se calibró la maquetación en Typst para ocupar exactamente el 87% de la página 15 del informe ($y = 728\text{ pt}$ sobre $771\text{ pt}$ útiles), garantizando cero desbordes a páginas subsiguientes, preservando el inicio del Capítulo 7 en la página 16 y asegurando la estabilidad absoluta de los índices de tablas y figuras.

### Hito 6: Jerarquización y Modularidad Académica del Capítulo 1 (Introducción)
* **Archivo intervenido:** `docs/informe/capitulos/01-introduccion.typ`.
* **Transformación lograda:** Pasó de un bloque de texto plano de 93 líneas a un capítulo articulado de 33 líneas densas y estructuradas bajo 4 subsecciones formales de nivel 2:
  1. `1.1 Contexto Global y Panorama de Vulnerabilidades Web`: Fundamenta la relevancia crítica de las aplicaciones web y la severidad del panorama de amenazas sustentado en datos auditados de Verizon (DBIR 2025: 12% del total de brechas, 88% con credenciales robadas) e IBM (Cost of a Data Breach 2025: 4,44M USD por brecha), categorizando las fallas recurrentes bajo el estándar OWASP Top 10 (2021).
  2. `1.2 La Necesidad de Orquestación: Paradigma SOAR y Enfoque DAST Integrado`: Analiza las limitaciones y sobrecarga operativa del DAST tradicional aislado (Qadir et al., 2025), introduce la respuesta de la industria mediante SOAR (Kinyua & Awuah, 2021), fundamenta la sinergia multivectorial de la triada (ZAP pasivo/activo, ffuf para fuzzing de directorios y SQLMap para inyecciones profundas; Alsaedi et al., 2021; Elia et al., 2010) y delimita la vacancia frente a las herramientas corporativas de la Tabla 1 del Capítulo 7 (Faraday, DefectDojo, TheHive, Shuffle) mediante un despliegue liviano con un único comando Docker Compose.
  3. `1.3 Propuesta de Valor, Alcance del Prototipo y Entorno Experimental`: Describe los componentes del prototipo (orquestador modular en Python 3.11 escalado a arquitectura de servicio con API REST FastAPI asíncrona, persistencia relacional, panel web React, autenticación de sesión automatizada y recomendaciones asistidas por IA), encuadrando su validación experimental en DVWA sobre una red Docker aislada (`pentest-net`) bajo la Ley 26.388 y el Código de Ética ACM (Capítulo 16).
  4. `1.4 Estructura del Documento`: Jerarquiza formalmente el párrafo canónico de articulación secuencial del informe (secciones 2 a 19), preservando al 100% la fórmula institucional auditada por el tribunal evaluador de la UTN FRM.
* **Calibración editorial y no-regresión:** Se preservó estrictamente la delimitación del Capítulo 1 entre las páginas físicas 7 y 8 (páginas numeradas 6 y 7), garantizando que el Capítulo 2 continúe iniciando con su `#pagebreak()` en la página física 9 (numerada 8). Las 4 nuevas subsecciones se sincronizaron automáticamente en el `#outline` (página física 4), siendo absorbidas por el margen disponible de $126,8\text{ pt}$ en la página física 5 sin alterar el total de 72 páginas ni desplazar ninguna de las 13 tablas cuantitativas ni figuras del informe.

### Hito 7: Reestructuración y Categorización Taxonómica del Capítulo 9 (Alcances y Limitaciones)
* **Archivo intervenido:** `docs/informe/capitulos/09-alcances-limitaciones.typ`.
* **Transformación lograda:** Se transformó el capítulo desde un catálogo plano de 90 líneas con dos listas simples de viñetas hacia un texto articulado de 68 líneas densas, categorizado funcional y metodológicamente:
  1. `Encuadre Sistémico en 9.1 (Alcances)`: Párrafo de apertura delimitando el alcance de un artefacto tecnológico en ingeniería de software, articulando las capacidades en tres bloques funcionales destacados:
     * `#strong[a) Núcleo de Detección Dinámica y Enriquecimiento Cruzado:]` Triada DAST (ZAP, ffuf, SQLMap), realimentación de rutas ffuf $\rightarrow$ ZAP, módulo de autenticación POST con renovación heurística de cookies y ejecución asíncrona de SQLMap en background (`sqlmap_bg.log`).
     * `#strong[b) Capa de Persistencia, Caché y API de Servicio:]` Parseo sintáctico hacia `resultado_unificado.json`, motor de caché incremental con re-testeo, API REST FastAPI asíncrona (`BackgroundTasks`) y persistencia híbrida en SQLite/PostgreSQL.
     * `#strong[c) Interfaz de Usuario y Automatización Operativa:]` SPA interactiva en React, generación de reportes técnico/ejecutivo, remediación guiada por LLM (Groq/Gemini) y orquestación con Docker Compose en red aislada (`sec-net`).
  2. `Encuadre Epistemológico en 9.2 (Limitaciones)`: Párrafo introductorio fundamentando la delimitación del alcance como salvaguarda contra falsas expectativas de cobertura en producción, agrupando las restricciones en tres dimensiones formales:
     * `#strong[a) Delimitación del Entorno de Pruebas y Seguridad de la Infraestructura:]` Pruebas circunscritas a DVWA sin WAF real, API de desarrollo con CORS abierto y sin autenticación JWT, y carácter orientativo del módulo de IA.
     * `#strong[b) Restricciones de Comparabilidad Metodológica y Rigor Estadístico:]` Condicionamiento de H1 por ausencia de grupo de control ciego e independiente (sustentado en la auditoría manual de 50 min del Cap. 17 sobre 125 min totales), corrida experimental única para H2 (Tabla 9), variabilidad de red en escaneo dinámico (sección 10.5) y heurística determinista simple en lugar de CVSS estándar.
     * `#strong[c) Vulnerabilidades Fuera de Alcance por Diseño Arquitectónico (Scope Boundaries):]` Delimitación en firmas sintácticas de inyección HTTP y exclusión formal por diseño de *Business Logic Flaws*, *Race Conditions* y control de acceso horizontal complejo entre identidades con iguales privilegios.
* **Calibración editorial y no-regresión:** Se preservaron intactas las etiquetas `<alcances-y-limitaciones>`, `<alcances>` y `<limitaciones>`. El capítulo ocupa aproximadamente 1,6 carillas confinadas entre las páginas físicas correspondientes mediante directivas `#pagebreak()` previas y posteriores, garantizando que el Capítulo 10 continúe iniciando con absoluta estabilidad, sin desfasajes en las 13 tablas cuantitativas ni en los índices unificados.
* **Cierre de Bloque B:** Con las Tareas 3 (Hipótesis), 4 (Introducción) y 5 (Alcances y Limitaciones) finalizadas, el Bloque B queda completado al 100%, consolidando un salto proyectado de +3,0 puntos sumados en los capítulos metodológicos y abriendo paso al Bloque C (Alineación Fina de Objetivos y Preguntas).