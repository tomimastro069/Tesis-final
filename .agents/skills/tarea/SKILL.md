---
name: tarea
description: >-
  Trigger: '/tarea', '/plan-capitulo', 'tarea', 'plan-capitulo'. Planifica e implementa tareas individuales del plan de subsanación y defensa en docs/plan/plan-03-10-2026.md, auditando el texto plano, garantizando cero invención de datos bajo normas APA 7.ª y reglas institucionales UTN FRM.
---

# Procedimiento de Planificación e Implementación de Tarea (`/tarea`, `/plan-capitulo`)
**Universidad Tecnológica Nacional — Facultad Regional Mendoza**  
*Tecnicatura Universitaria en Programación (TUP)*  
**Documento Fuente:** `docs/plan/plan-03-10-2026.md`

Este procedimiento operativo guía al asistente en su rol de **Tutor Académico y Miembro del Tribunal Evaluador** para tomar una tarea individual del plan de subsanación atómica hacia la calificación sobresaliente (**9,0+ / defensa oral**), auditar el código Typst existente, diseñar la solución rigurosa y generar el plan de implementación previo a la edición.

---

## 1. Entrada y Detección de la Tarea

1. **Parseo del Comando:**
   * El usuario invoca `/tarea [N]` o `/plan-capitulo [N]` (ejemplos: `/tarea 1`, `/tarea 2`, `/plan-capitulo 1`).
   * Si el usuario **no especifica número** (solo escribe `/tarea`), el asistente debe inspeccionar la **Sección 5 (Checklist de Tareas)** de `docs/plan/plan-03-10-2026.md` e identificar la primera tarea marcada como `[ ] [EN PROGRESO / PRÓXIMO PASO]` o `[ ] [PENDIENTE]`.
2. **Localización de los Metadatos en el Plan:**
   * Abrir y leer `docs/plan/plan-03-10-2026.md` en la sección correspondiente:
     * **Tarea 1:** Subsanación de X1 (Conteo de 34 URLs en Tabla 3 y 11; aporte real de 4 rutas de ffuf y ejemplo `/security.php` en Cap. 14).
     * **Tarea 2:** Subsanación de X2 y X3 (Benchmark de 6 de agosto en 14.3 y Reconciliación de Anexo D como reconstrucción).
     * **Tarea 3:** Subsanación de X4 y X5 (Títulos de reporte en Tablas 4, 5 y 7; trazabilidad con `sqlmap_bg.log`; APA 2026a; rótulo PostgreSQL en Figura 4).
     * **Tarea 4:** Subsanación de X6 y X7 (Parámetro `nivel` y `clean_cache` en API; payload legible a 2 renglones en 13.4; coincidencia de video; remisión Anexo H en Figura 4; README de evidencia).
     * **Tarea 5:** Adecuación Institucional del Punto 4.3 (Herramienta de autoevaluación académica en `.agents/`).
     * **Tarea 6:** Creación del Entregable V19, Sincronización Operativa de Skills y Verificación Final.
   * Identificar:
     * Archivos físicos afectados (`docs/informe/capitulos/{NN}-{nombre}.typ`, `media/`, etc.).
     * Meta de calificación y recuperación técnica.
     * Diagnóstico del problema identificado por el tribunal evaluador en el Dictamen 11 oficial.
     * Esquema de solución requerida (bloques de código Typst, fórmulas, tablas, etc.).

---

## 2. Las 5 Líneas Rojas Inviolables (Tolerancia Cero)

Antes de cualquier propuesta o análisis, el asistente debe aplicar estrictamente los siguientes límites:

1. **PROHIBIDO TOCAR DATOS NUMÉRICOS O ARITMÉTICA DE LAS TABLAS:** No modificar sumas, tiempos, porcentajes ni cifras de las 13 tablas cuantitativas del informe.
2. **PROHIBIDO INVENTAR PRUEBAS O EXPERIMENTOS:** Toda métrica o afirmación técnica debe tener trazabilidad directa a archivos físicos reales (`resultado_unificado.json`, `sqlmap_bg.log`, benchmarks de caché).
3. **PRESERVAR LA CONSISTENCIA DE PARÁMETROS INTERCAPÍTULOS:** Flags (`--threads=10`, `--smart`, `--batch`, `--technique=BEUST`), variables de entorno, nombres de contenedores y timeouts deben ser idénticos a los definidos en los Capítulos 11, 12, 14, 17 y 19.
4. **COMPILACIÓN CONTINUA Y CAJA TIPOGRÁFICA EN TYPST:** Respetar el ancho de caja útil ($x \in [70,9\text{ pt}, 524,4\text{ pt}]$), sangría estándar (72 pt / $70,87\text{ pt}$), viñetas con guion (`- ` y nunca `* `) y etiquetas únicas (`<label>`).
5. **CONTROL DE VERSIONES ESTRICTO:** Prohibición absoluta de ejecutar `git commit` o `git push`. Solo sugerir commit en 2 partes al finalizar.

---

## 3. Protocolo de Auditoría y Diseño Paso a Paso

El asistente debe ejecutar las siguientes fases metodológicas:

### Fase 1: Auditoría del Texto Plano Actual
* Leer íntegramente el archivo capitular objetivo en `docs/informe/capitulos/{NN}-{nombre}.typ`.
* Contar líneas y párrafos actuales.
* Analizar debilidades: ¿carece de subtítulos de nivel 2?, ¿es un salto abrupto a viñetas?, ¿carece de fundamentos epistemológicos o arquitectónicos?, ¿hay oraciones huérfanas?

### Fase 2: Matriz de Trazabilidad Empírica y Cero Invención
* Listar cada afirmación conceptual y técnica que se incorporará y verificar su respaldo en:
  * El stack tecnológico real: Python 3.11, OWASP ZAP, ffuf, SQLMap, Docker Compose, FastAPI, React, SQLite/PostgreSQL.
  * Los tiempos reales: ventana de 4 a 14 minutos (Tabla 10).
  * Los datos de ciberseguridad documentados: OWASP Top 10 (2021), IBM (2025: 4,44M USD), Verizon (2025), SANS Institute (2024: 3.000 y 12.000 USD).
  * La articulación formativa real: Asignaturas de la Tecnicatura Universitaria en Programación (TUP - UTN FRM).
  * Citas en APA 7.ª edición: Contrastadas contra las entradas existentes en `docs/informe/capitulos/18-referencias.typ`.

### Fase 3: Elaboración del Artefacto de Plan de Implementación
* Crear obligatoriamente un artefacto markdown con la herramienta `write_to_file`:
  * Ruta: `/home/cristian/.gemini/antigravity-ide/brain/<conversation-id>/plan_implementacion_capitulo_{NN}.md`.
  * Contenido estructurado:
    1. **Identificación Institucional:** Carrera, título de tesina, autores, directores, archivo afectado y meta de calificación.
    2. **Auditoría del Texto Plano Actual:** Transcripción del estado actual y diagnóstico crítico del tribunal.
    3. **Matriz de Trazabilidad:** Tabla de contrastación empírica demostrando cero datos inventados.
    4. **Estructura Académica Formal Propuesta:** Jerarquía de subsecciones (`== X.Y`) y desglose conceptual.
    5. **Propuesta Textual Completa en Sintaxis Typst:** Bloque de código Typst nativo listo para sustitución, con escapes correctos de paréntesis `\(`, guiones para listas `- ` y etiquetas `<...>`.
    6. **Protocolo de Validación y No-Regresión:** Control de páginas, sincronía del outline, aislamiento con `#pagebreak()` y ausencia de impacto en tablas/figuras.

### Fase 4: Presentación al Usuario (Anti-Abrumación)
* Responder al usuario de forma concisa:
  * Enlazar directamente al artefacto generado.
  * Resumir en 3 o 4 viñetas las decisiones clave tomadas.
  * **DETENERSE Y PEDIR CONFIRMACIÓN:** Nunca modificar el archivo `.typ` antes de que el usuario revise y apruebe el plan.
