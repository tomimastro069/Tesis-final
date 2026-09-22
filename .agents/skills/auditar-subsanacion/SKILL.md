---
name: auditar-subsanacion
description: >-
  Trigger: '/auditar-subsanacion', 'auditar subsanacion', 'verificar correcciones'. Cruza un informe nuevo (docs/informe/) contra el dictamen anterior (docs/dictamen/) para validar la resolución de observaciones, detectar incumplimientos y alertar sobre regresiones.
---

# Procedimiento de Auditoría de Subsanación y Control de Regresiones (`auditar-subsanacion`)
**Universidad Tecnológica Nacional — Facultad Regional Mendoza**  
*Tecnicatura Universitaria en Programación (TUP)*

Este procedimiento operativo guía al asistente en la contrastación minuciosa de una nueva versión del informe de tesina (`docs/informe/informe-v{N}.*`) frente al dictamen previo inmediato (`docs/dictamen/dictamen-{N-1}.md`), verificando la resolución efectiva de observaciones y garantizando la ausencia de regresiones.

---

## 1. Identificación del Par Documental

1. **Definir el documento evaluador de referencia:**
   * Dictamen anterior: `docs/dictamen/dictamen-{N-1}.md` (o `.pdf`).
2. **Definir el informe bajo evaluación:**
   * Nueva entrega: `docs/informe/informe-v{N}.*` (ej. `informe-v15.pdf`).
3. **Verificar correlación:**
   * Confirmar que el informe bajo análisis sea la versión sucesora directa de la auditada en el dictamen previo.

---

## 2. Inventario de Exigencias Previas del Tribunal

Antes de inspeccionar el nuevo informe, extraer y estructurar todas las observaciones formuladas en el dictamen anterior en tres niveles:

1. **Condición(es) Previa(s) Bloqueante(s):** Requisitos obligatorios cuyo incumplimiento impide la aprobación.
2. **Correcciones Recomendadas:** Mejoras técnicas, metodológicas o formales de carácter no excluyente pero incidentes en la nota.
3. **Hallazgos Tipificados:** Defectos específicos codificados (ej. serie $T_1$ a $T_9$, o la letra de instancia correspondiente) clasificados por severidad (*Alta*, *Media*, *Baja*).

---

## 3. Protocolo de Inspección y Clasificación en el Nuevo Informe

Para cada ítem del inventario previo, localizar la sección correspondiente en el nuevo informe y verificar la evidencia real. Clasificar el estado con una de las tres etiquetas estrictas:

* `[TOTALMENTE SUBSANADO]`:
  * El cambio implementado por los autores resuelve de manera integral, precisa e incontrovertible lo requerido por el tribunal.
  * No introduce contradicciones en otras secciones ni debilita la fundamentación académica.
* `[PARCIALMENTE SUBSANADO]`:
  * Los autores realizaron modificaciones en la dirección correcta, pero persiste omisión de datos clave, explicaciones incompletas o falta de contrastación empírica.
* `[NO SUBSANADO / OMITIDO]`:
  * El texto permanece idéntico a la versión anterior, el cambio fue cosmético sin abordar la raíz del problema, o se ignoró la observación del tribunal.

---

## 4. Vigilancia Activa de Regresiones (Criterio 5 de Tolerancia Cero)

El asistente debe auditar que las modificaciones no hayan introducido nuevos problemas colaterales:

1. **Regresiones Aritméticas:**
   * ¿La modificación de un dato en una tabla descuadró las sumas totales o los porcentajes de esa tabla u otras relacionadas?
2. **Regresiones de Remisión:**
   * ¿El agregado o eliminación de párrafos alteró la numeración de títulos, figuras o tablas referenciadas en el texto?
3. **Regresiones de Consistencia Técnica:**
   * ¿Se modificó un parámetro (ej. timeout de 30 s a 60 s, o hilos de 10 a 20) en un capítulo pero se mantuvo el valor viejo en la arquitectura o en la experimentación?
4. **Regresiones de Formato y Maquetación:**
   * Verificar que la portada institucional no haya duplicado información.
   * Verificar que las 26 referencias bibliográficas conserven sangría francesa APA 7.
   * Comprobar que no existan tablas desbordadas o títulos huérfanos al pie de página.

---

## 5. Tabla Consolidada de Balance de Subsanación

Generar una tabla resumen con el estado global de la entrega:

| Categoría de Observación | Total Evaluadas | Subsanadas Plenas | Parciales | No Subsanadas | % Cumplimiento |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Condiciones Previas | - | - | - | - | - % |
| Correcciones Recomendadas | - | - | - | - | - % |
| Hallazgos Tipificados ($T/U$) | - | - | - | - | - % |
| **BALANCE GLOBAL** | **-** | **-** | **-** | **-** | **- %** |

---

## 6. Metodología de Corrección Paso a Paso (Anti-Abrumación)

Para todos aquellos puntos catalogados como `[PARCIALMENTE SUBSANADO]` o `[NO SUBSANADO]`, el asistente **no debe volcar una lista interminable de textos para editar**. Debe ejecutar el protocolo paso a paso:

1. **Seleccionar un único punto crítico a la vez** (priorizando condiciones previas y hallazgos de severidad alta).
2. **Explicar el problema pedagógicamente:** Por qué el tribunal lo señaló y qué falta para cerrarlo con rigor UTN.
3. **Sección y ubicación exacta:** Indicar capítulo, sección, página o tabla involucrada.
4. **Qué quitar:** Mostrar el bloque textual exacto que el usuario debe borrar en su procesador de texto.
5. **Qué poner:** Entregar el bloque de reemplazo listo para copiar y pegar, redactado con estilo formal, académico e impecable.
6. **Pausar y esperar:** Solicitar confirmación o captura al usuario antes de avanzar al siguiente punto de la lista.
