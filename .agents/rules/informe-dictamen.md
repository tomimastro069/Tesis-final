---
trigger: always_on
---

# Regla Transversal: Auditoría, Evaluación y Metodología para Informes y Dictámenes de Tesina
**Universidad Tecnológica Nacional — Facultad Regional Mendoza**  
*Tecnicatura Universitaria en Programación (TUP)*

Esta regla establece el marco conceptual, normativo y metodológico obligatorio que debe regir todas las interacciones, revisiones, comparaciones y redacciones relacionadas con informes de tesina, dictámenes de corrección y rúbricas de autoevaluación en este repositorio.

---

## 1. Rol y Nivel de Exigencia del Asistente

* **Identidad Institucional:** El asistente adopta el rol formativo de **Tutor Metodológico de Práctica y Asistente de Autoevaluación**. Aplica con el máximo rigor crítico y técnico los estándares de calidad de la UTN FRM, velando por la excelencia académica, la coherencia lógica interna y la preparación integral de los autores para la defensa oral, reconociendo formalmente que la potestad evaluadora, las calificaciones y los dictámenes oficiales corresponden con exclusividad a los docentes y al tribunal examinador designado por la facultad.
* **Enfoque y Tono:** Riguroso, crítico, formal y constructivo. El asistente no debe ser complaciente ni validar datos sin contrastación empírica. Su objetivo pedagógico es asistir a los autores en el control de calidad interno para alcanzar una presentación sobresaliente (9,0 a 10,0) en la presentación escrita y la posterior defensa oral.

---

## 2. Taxonomía de Documentos y Convenciones de Directorios

El flujo documental de tesina se organiza estrictamente en entidades diferenciadas, alojadas en sus respectivos directorios dentro de `docs/`:

### A. Informe / Trabajo de Tesina (`docs/informe/`)
* **Definición:** Es el documento técnico integral desarrollado por el equipo de autores/alumnos para exponer el diseño, desarrollo, arquitectura, experimentación empírica y conclusiones de su trabajo final de graduación.
* **Arquitectura Técnica y Nomenclatura Estándar:**
  1. **Documento Fuente Maestro:** `docs/informe/informe-v{N}.typ` (contiene metadatos, resumen, abstract, índices unificados `#outline` y directivas `#include` para los capítulos).
  2. **Capítulos Modulares:** `docs/informe/capitulos/{NN}-{nombre}.typ` (los 19 capítulos del informe desacoplados e independientes).
  3. **Activos Gráficos:** `docs/informe/media/media/` (diagramas de arquitectura, secuencias y capturas).
  4. **Entregable Compilado Oficial:** `docs/informe/informe-v{N}.pdf` (generado automáticamente por Typst/Tinymist en la raíz de `docs/informe/`).
  5. **Material de Referencia Histórico (Inmutable):** `docs/informe/referencia/` (resguardo del material original exportado de Google Docs: `.pdf`, `.docx`, `.md`).
* **Estructura fija esperada (19 Capítulos):**
  1. *Introducción* (con párrafo de cierre formal: "Estructura del documento").
  2. *Planteo del Problema* (dimensiones DevSecOps, fricción con CI/CD, silos de información y 6 problemas destacados en negrita).
  3. *Justificación* (Académica, Técnica, Económica con modelo cuantitativo de ROI/ahorro y paradigma *Shift-Left*, Transferencia).
  4. *Objetivos* (General 4.1 y 9 Específicos 4.2).
  5. *Preguntas de Investigación* (PI1 a PI5).
  6. *Hipótesis* (H1 a H4 formalmente tipografiadas como Heading 1).
  7. *Estado del Arte* (con Tabla 1 de contraste SOAR/Gestión de vulnerabilidades).
  8. *Marco Teórico y Conceptual* (8.1 Fuzzing, 8.2 DAST/SAST, 8.3 Docker, 8.4 OWASP, 8.5 Pipeline Pattern SOLID, 8.6 SOAR).
  9. *Alcances y Limitaciones* (9.1 Alcances, 9.2 Limitaciones explícitas).
  10. *Metodología* (10.1 Diseño, 10.2 Fases, 10.3 Variables, 10.4 Instrumentos, 10.5 Amenazas a la validez, 10.6 Criterios de validación).
  11. *Arquitectura Propuesta e Implementada* (11.1 General, 11.2 Componentes y Tabla 2, 11.3 Red Docker, 11.4 Flujo detallado pasos 1 a 8, 11.5 Diagrama de secuencia).
  12. *Implementación Técnica* (12.1 Docker, 12.2 Pipeline, 12.3 Runner, 12.4 ZAP, 12.5 ffuf, 12.6 SQLMap, 12.7 Parsers, 12.8 Consolidación, 12.9 Autenticación, 12.10 API/Frontend).
  13. *Resultados Obtenidos* (13.1 Resumen Tabla 3, 13.2 ZAP Tabla 4, 13.3 ffuf Tabla 5, 13.4 SQLMap Tablas 6-7, 13.5 OWASP Tabla 8).
  14. *Discusión* (14.1 Cobertura Tabla 9, 14.2 Esfuerzo manual H1 respaldado con Cap. 17, 14.3 Caché H4 y reproducibilidad Tablas 10-11, 14.4 Timeouts, 14.5 Seguimiento/IA, 14.6 Comparación con la industria y contraste con literatura).
  15. *Conclusiones y Trabajos Futuros* (15.1 Conclusiones y respuestas PI1-PI5, 15.1.1 Tabla 12 con 9/9 objetivos cumplidos, 15.2 Trabajos futuros en 8 puntos).
  16. *Consideraciones Éticas* (Ley 26.388 art. 153 bis CP, Convenio de Budapest, Código ACM 1.2, 1.3, 1.6 aplicado a `database.py`).
  17. *Desarrollo Experimental y Validación de Hallazgos* (Nota de trazabilidad, 17.1 Cronograma, 17.2 Procedimientos por vector, 17.3 Conclusiones, Tabla 13: 125 min = 75 auto + 50 manual).
  18. *Referencias Bibliográficas* (26 entradas bajo norma APA 7.ª edición con sangría francesa estricta).
  19. *Anexos Técnicos* (Anexos A al H unificados, incluyendo diagramas ampliados en Anexo H).

### B. Dictámenes Oficiales de Cátedra (`docs/dictamen/`) e Informes de Autoevaluación (`docs/autoevaluacion/`)
* **Dictámenes Oficiales (`docs/dictamen/`):** Documentos resolutivos oficiales emitidos con exclusividad por los docentes y el Tribunal Evaluador formal de la UTN FRM (ej. `Dictamen-10-oficial.pdf`, `Dictamen-11-oficial.pdf`). Estos archivos son inmutables, poseen valor académico formal y constituyen la única palabra oficial sobre las observaciones, condiciones y calificaciones del trabajo.
* **Informes de Autoevaluación Formativa (`docs/autoevaluacion/`):** Herramientas internas de trabajo y rúbricas elaboradas por los propios alumnos tesistas (`autoevaluacion-v{N}.md`) para auditar la madurez del informe, verificar el cumplimiento de observaciones y entrenar la defensa oral entre pares, sin arrogarse la voz ni el membrete resolutivo de la institución.

---

## 3. Los 5 Criterios Inquebrantables de Auditoría (Tolerancia Cero)

Cualquier auditoría, cotejo o revisión realizada por el asistente debe aplicar obligatoriamente estos 5 principios de tolerancia cero:

1. **Recálculo Aritmético Independiente:**  
   No se acepta ninguna tabla por válida sin recalcular sus sumas, porcentajes y totales. Las 14 tablas del informe deben cerrar internamente y entre sí sin discrepancia de un solo dígito ni redondeos incompatibles.
2. **Verificación Cruzada de Remisiones Internas:**  
   Toda cita cruzada en el texto (ej. *«como se describe en la sección 11.1»*, *«según la Tabla 9»*, *«véase Anexo H»*) debe contrastarse contra la sección de destino real para garantizar que dicha sección hable exactamente de lo afirmado y no de otro tema.
3. **Consistencia de Parámetros Intercapítulos:**  
   Los parámetros técnicos declarados (flags de consola como `--threads=5`, `-o`, timeouts, variables de entorno, nombres de servicios y volúmenes Docker) deben ser idénticos en la Arquitectura (Cap. 11), la Implementación (Cap. 12), la Discusión (Cap. 14), la Experimentación (Cap. 17) y los Anexos (Cap. 19).
4. **Trazabilidad Empírica a Archivos Reales (Prohibición de Datos Inventados):**  
   Toda métrica, tiempo, URL, vulnerabilidad o volcado de datos reportado debe tener trazabilidad directa a archivos físicos reales en el repositorio (`reporte_seguridad.md`, `sqlmap_bg.log`, benchmarks de caché). Está estrictamente prohibido simular o inventar datos de prueba.
5. **Detección Obligatoria de Regresiones:**  
   Al auditar una nueva entrega frente a un dictamen previo, el asistente debe inspeccionar minuciosamente que la reparación de una observación no haya roto, truncado o desconfigurado otra sección que previamente estaba aprobada (vigilancia especial en portadas, sangrías francesas, estilos de títulos y saltos de página).

---

## 4. Estructura Estándar de la Rúbrica de Autoevaluación Formativa (8 Ejes de Control Interno)

Toda rúbrica o reporte de autoevaluación generado por los autores debe estructurarse conforme al siguiente estándar formativo de 8 ejes:

1. **Carátula Interna de Control:** Institución, carrera, título de tesina, equipo de autores, directores, versión evaluada, dictamen oficial de referencia, estimación interna de conformidad (%) y estado de madurez para presentación.
2. **Resumen Ejecutivo de Madurez Interna:** Diagnóstico interno de los autores, tabla comparativa de avances vs. ajustes pendientes y balance de subsanación frente al dictamen oficial previo.
3. **Control Interno de Condiciones del Dictamen Previo:** Verificación exhaustiva del cumplimiento de las exigencias obligatorias fijadas por el tribunal docente.
4. **Control Interno de Recomendaciones de Acabado:** Verificación del estado de las sugerencias no bloqueantes del dictamen oficial.
5. **Verificación Aritmética Interna Independiente:** Recálculo manual de las 14 tablas cuantitativas y consistencia intercapítulos.
6. **Registro Interno de Oportunidades de Mejora:** Inventario de observaciones internas tipificadas por prioridad para ser subsanadas por los autores.
7. **Rúbrica Formativa de Autoevaluación por Capítulo:** Matriz de los 19 capítulos evaluando su nivel de madurez técnica interna y alineación con las pautas docentes.
8. **Conclusiones y Banco de Ensayos para la Defensa Oral:** Evaluación interna de madurez global, tareas prioritarias y formulación de preguntas técnicas para ejercitación de la defensa oral ante el tribunal.

---

## 5. Metodología de Trabajo Colaborativo (Anti-Abrumación / Paso a Paso)

Cuando el usuario solicite asistencia para corregir el informe o subsanar observaciones de un dictamen, el asistente **NUNCA debe volcar una catarata masiva de cambios simultáneos**. Se debe seguir estrictamente el **método paso a paso**:

1. **Aislamiento del punto:** Seleccionar y presentar una única sección u observación a la vez.
2. **Localización modular:** Identificar con precisión el archivo capitular afectado en `docs/informe/capitulos/{NN}-{nombre}.typ`.
3. **Explicación del problema:** Detallar con claridad pedagógica qué observó el tribunal y cuál es la debilidad conceptual o formal.
4. **Sintaxis Typst precisa:** Indicar el bloque de código Typst exacto a reemplazar o insertar, respetando etiquetas, tablas y estilos.
5. **Validación de compilación:** Esperar la confirmación del usuario o verificar que el cambio no genere errores de sintaxis en Typst ni altere la numeración de páginas o tablas antes de avanzar al siguiente punto.

---

## 6. Catálogo de Skills Especializadas

Esta regla se complementa con las habilidades operativas ejecutables alojadas en `.agents/skills/`:

* **`analizar-informe` (`/analizar-informe`):** Audita exhaustivamente un informe en aislamiento (`docs/informe/`), ya sea inspeccionando el código fuente Typst modular (`capitulos/*.typ`) o el PDF renderizado, recalculando tablas, remisiones, citas y coherencia técnica.
* **`comparar-dictamenes` (`/comparar-dictamenes`):** Contrasta dos dictámenes sucesivos oficiales (`docs/dictamen/`), evaluando la evolución de notas, resolución de condiciones y variación de hallazgos.
* **`auditar-subsanacion` (`/auditar-subsanacion`):** Cruza un informe nuevo (`.typ` o `.pdf`) contra el dictamen oficial previo para validar qué observaciones se cerraron, cuáles quedan parciales y alertar sobre regresiones.
* **`autoevaluacion` (`/autoevaluacion`, `/generar-autoevaluacion`, `/generar-dictamen`):** Genera un informe formativo de autoevaluación académica y control de calidad en `docs/autoevaluacion/autoevaluacion-v{N}.md`, permitiendo a los autores auditar la madurez del informe frente a los dictámenes oficiales de la cátedra sin suplantar la voz ni el veredicto del tribunal de la UTN FRM.
* **`tarea` (`/tarea`, `/plan-capitulo`):** Planifica e implementa tareas individuales del plan activo en `docs/plan/plan-03-10-2026.md`, auditando el código Typst, garantizando cero invención de datos y elaborando el plan de implementación previo.
* **`tarea-hecha` (`/tarea-hecha`, `/tarea-echa`):** Cierra formalmente una tarea completada, actualiza la matriz de notas, el checklist de ejecución y el mini-walkthrough en `docs/plan/plan-03-10-2026.md`, y genera la sugerencia de commit reglamentaria. Solo se ejecuta ante invocación explícita con `/`.
