---
name: tarea-hecha
description: >-
  Trigger: '/tarea-hecha', '/tarea-echa'. Cierra formalmente una tarea completada en docs/plan/plan-03-10-2026.md, actualiza el checklist de ejecución, registra el hito en el mini-walkthrough y sugiere el commit en dos partes. Solo se ejecuta ante invocación explícita con comando o barra '/'.
---

# Procedimiento de Cierre de Tarea y Registro de Avance (`/tarea-hecha`, `/tarea-echa`)
**Universidad Tecnológica Nacional — Facultad Regional Mendoza**  
*Tecnicatura Universitaria en Programación (TUP)*  
**Documento Fuente:** `docs/plan/plan-03-10-2026.md`

Este procedimiento operativo guía al asistente en su rol de **Tutor Académico y Miembro del Tribunal Evaluador** para cerrar formalmente una tarea completada del plan de subsanación atómica, actualizar la matriz y el checklist de `docs/plan/plan-03-10-2026.md`, documentar el hito en el mini-walkthrough y sugerir el commit reglamentario.

---

## 1. Condición Estricta de Disparo

* **Regla de Invocación Exclusiva:** Esta skill **SOLO** debe ejecutarse cuando el usuario la active de manera explícita en el chat utilizando el comando con barra diagonal:
  * `/tarea-hecha [N]`
  * `/tarea-echa [N]`
  * `/tarea-hecha`
  * `/tarea-echa`
* Si el usuario no utiliza el comando explícito o el símbolo `/`, no se debe ejecutar este procedimiento.

---

## 2. Identificación de la Tarea a Cerrar

1. **Parámetro Explícito:**  
   Si el usuario envía un número (ejemplo: `/tarea-hecha 1` o `/tarea-echa 1`), se selecciona directamente la **Tarea N** indicada.
2. **Parámetro Implícito (Detección Automática):**  
   Si el usuario no envía un número (solo `/tarea-hecha`), el asistente debe inspeccionar la **Sección 5 (Checklist de Tareas)** de `docs/plan/plan-03-10-2026.md` y seleccionar:
   * La tarea marcada como `[ ] [EN PROGRESO / PRÓXIMO PASO]`.
   * En su defecto, la primera tarea que figure pendiente `[ ]`.

---

## 3. Verificaciones de Calidad Previas al Cierre

Antes de marcar la tarea como completada en el plan, verificar:
1. **Compilación Limpia:** Que los archivos capitulares modificados (`docs/informe/capitulos/{NN}-{nombre}.typ`) no presenten errores de sintaxis en Typst ni advertencias de delimitadores no cerrados.
2. **Cero Invención de Datos:** Que no se hayan incorporado métricas ni herramientas ficticias fuera del repositorio.
3. **Cero Regresiones de Maquetación y Sintaxis:** Que las fórmulas y recálculos aritméticos cierren de forma exacta, que los epígrafes y tablas mantengan consistencia intercapítulos y que no existan desbordes de caja.

---

## 4. Actualización Obligatoria en `docs/plan/plan-03-10-2026.md`

El asistente debe aplicar las siguientes 4 modificaciones sincronizadas en `docs/plan/plan-03-10-2026.md`:

1. **En la Sección 5 (Checklist de Tareas):**
   * Cambiar la casilla de la tarea a completada:
     `- [x] **Tarea N: ...** [Meta: ...] **[COMPLETADO]**`
   * Si existe una tarea siguiente inmediata, marcarla como:
     `- [ ] **Tarea N+1: ...** [Meta: ...] **[EN PROGRESO / PRÓXIMO PASO]**`
2. **En la Sección 4 (Plan de Acción Detallado):**
   * Actualizar el título de la Tarea N agregando `**[COMPLETADO]**`.
   * Registrar: `* **Estado:** **HECHO / COMPLETADO**` junto al resumen de las correcciones aplicadas.
3. **En la Sección 3 (Matriz de Calificaciones por Capítulo):**
   * Actualizar la fila del capítulo afectado:
     * *Meta Subsanada:* Registrar la nota proyectada alcanzada.
     * *Acción Correctiva:* Indicar la subsanación realizada.
4. **En la Sección 6 (Mini-Walkthrough de Avances y Decisiones de Ingeniería Documental):**
   * Añadir el nuevo hito correlativo:
     `### Hito X: [Nombre de la Tarea / Capítulo]`
     * Detallar los archivos intervenidos (`docs/informe/capitulos/{NN}-{nombre}.typ`).
     * Describir la transformación técnica y tipográfica lograda.
     * Explicar el impacto en la no-regresión y en la satisfacción de los hallazgos del Dictamen 11 oficial (X1 a X7).

---

## 5. Generación de la Sugerencia de Commit Profesional

Conforme a la regla institucional `user_global_workflow` (prohibición estricta de ejecutar `git commit` automático), el asistente debe sugerir el commit al usuario estructurado en dos partes:

```markdown
### Sugerencia de Commit

#### Parte 1: Comando
git commit -m "docs(informe): [descripción concisa de la tarea completada]"

#### Parte 2: Mensaje
docs(informe): [descripción concisa de la tarea completada]

- [Detalle de los cambios principales aplicados]
- [Mención de la subsanación de hallazgos del Dictamen 11 oficial (X1 a X7)]
- [Registro de la actualización en plan-03-10-2026.md y checklist]
```

---

## 6. Transición a la Siguiente Tarea

Concluir informando al usuario cuál es la siguiente tarea disponible en la hoja de ruta y recomendarle el comando exacto para iniciarla (ejemplo: *«Para continuar con la siguiente tarea, escribe `/tarea 2`»*).
