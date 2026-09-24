---
name: tarea-hecha
description: >-
  Trigger: '/tarea-hecha', '/tarea-echa'. Cierra formalmente una tarea completada en docs/plan/plan-v16-punt-9.md, actualiza el checklist de ejecución, registra el hito en el mini-walkthrough y sugiere el commit en dos partes. Solo se ejecuta ante invocación explícita con comando o barra '/'.
---

# Procedimiento de Cierre de Tarea y Registro de Avance (`/tarea-hecha`, `/tarea-echa`)
**Universidad Tecnológica Nacional — Facultad Regional Mendoza**  
*Tecnicatura Universitaria en Programación (TUP)*  
**Documento Fuente:** `docs/plan/plan-v16-punt-9.md`

Este procedimiento operativo guía al asistente en su rol de **Tutor Académico y Miembro del Tribunal Evaluador** para cerrar formalmente una tarea completada del plan de escalado hacia la calificación sobresaliente (**9,0 a 10,0**), actualizar la matriz y el checklist del plan maestro, documentar el hito en el mini-walkthrough y sugerir el commit reglamentario.

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
   Si el usuario envía un número (ejemplo: `/tarea-hecha 2` o `/tarea-echa 2`), se selecciona directamente la **Tarea N** indicada.
2. **Parámetro Implícito (Detección Automática):**  
   Si el usuario no envía un número (solo `/tarea-hecha`), el asistente debe inspeccionar la **Sección 5 (Checklist de Tareas)** de `docs/plan/plan-v16-punt-9.md` y seleccionar:
   * La tarea marcada como `[ ] [EN PROGRESO / PRÓXIMO PASO]`.
   * En su defecto, la primera tarea que figure pendiente `[ ]`.

---

## 3. Verificaciones de Calidad Previas al Cierre

Antes de marcar la tarea como completada en el plan, verificar:
1. **Compilación Limpia:** Que el archivo capitular modificado (`docs/informe/capitulos/{NN}-{nombre}.typ`) no presente errores de sintaxis en Typst ni advertencias de delimitadores no cerrados.
2. **Cero Invención de Datos:** Que no se hayan incorporado métricas ni herramientas ficticias fuera del repositorio.
3. **Cero Regresiones de Maquetación:** Que los saltos de página (`#pagebreak()`) preserven la independencia de capítulos y mantengan un balance visual armónico (sin listas partidas a la mitad ni páginas semivacías).

---

## 4. Actualización Obligatoria en `docs/plan/plan-v16-punt-9.md`

El asistente debe aplicar las siguientes 4 modificaciones sincronizadas en `docs/plan/plan-v16-punt-9.md`:

1. **En la Sección 5 (Checklist de Tareas):**
   * Cambiar la casilla de la tarea a completada:
     `- [x] **Tarea N: ...** [Meta: ...] **[COMPLETADO]**`
   * Si existe una tarea siguiente inmediata, marcarla como:
     `- [ ] **Tarea N+1: ...** [Meta: ...] **[EN PROGRESO / PRÓXIMO PASO]**`
2. **En la Sección 3 (Plan de Acción Detallado):**
   * Actualizar el título de la Tarea N agregando `**[COMPLETADO]**`.
   * Registrar: `* **Estado:** **HECHO / COMPLETADO**` junto al resumen de las subsecciones y mejoras aplicadas.
3. **En la Sección 1.3 (Matriz de Calificaciones por Capítulo):**
   * Actualizar la fila del capítulo afectado:
     * *Estado Técnico:* Cambiar a `Completado (Typst)`.
     * *Potencial de Mejora:* Registrar la nota proyectada alcanzada (ej. `8,3 alcanzado`).
     * *Diagnóstico:* Resumir brevemente la subsanación realizada.
4. **En la Sección 6 (Mini-Walkthrough de Avances y Decisiones de Ingeniería Documental):**
   * Añadir el nuevo hito correlativo:
     `### Hito X: [Nombre de la Tarea / Capítulo]`
     * Detallar el archivo intervenido (`docs/informe/capitulos/{NN}-{nombre}.typ`).
     * Describir la transformación lograda (número de líneas, subsecciones formales, argumentos académicos).
     * Explicar las decisiones de maquetación y balance de carillas aplicadas.

---

## 5. Generación de la Sugerencia de Commit Profesional

Conforme a la regla institucional `user_global_workflow` (prohibición estricta de ejecutar `git commit` automático), el asistente debe sugerir el commit al usuario estructurado en dos partes:

```markdown
### Sugerencia de Commit

#### Parte 1: Comando
git commit -m "docs(informe): [descripción concisa de la tarea completada]"

#### Parte 2: Mensaje
docs(informe): [descripción concisa de la tarea completada]

- [Detalle de los cambios principales aplicados en el capítulo]
- [Mención de la jerarquización y normas APA/UTN respetadas]
- [Registro de la actualización en plan-v16-punt-9.md y checklist]
```

---

## 6. Transición a la Siguiente Tarea

Concluir informando al usuario cuál es la siguiente tarea disponible en la hoja de ruta y recomendarle el comando exacto para iniciarla (ejemplo: *«Para continuar con la siguiente tarea, escribe `/tarea 3`»*).
