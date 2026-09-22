---
name: analizar-informe
description: >-
  Trigger: '/analizar-informe', 'analizar informe', 'revisar informe', o auditoría exhaustiva de un informe de tesina (PDF/Markdown) en docs/informe/. Evalúa los 19 capítulos bajo los 5 criterios de tolerancia cero de UTN FRM.
---

# Procedimiento de Auditoría Exhaustiva de Informe de Tesina (`analizar-informe`)
**Universidad Tecnológica Nacional — Facultad Regional Mendoza**  
*Tecnicatura Universitaria en Programación (TUP)*

Este procedimiento operativo guía al asistente en su rol de **Tutor y Revisor del Tribunal Evaluador** para auditar en profundidad una versión específica del informe de tesina (`docs/informe/informe-v{N}.*`).

---

## 1. Identificación y Alcance del Documento

1. **Localizar el archivo de informe:**
   * El informe debe ubicarse en `docs/informe/` con formato `informe-v{N}.pdf`, `.docx` o `.md`.
   * Si no se especifica versión, seleccionar la más reciente o consultar al usuario.
2. **Determinar la modalidad:**
   * Auditoría aislada (revisión de coherencia intrínseca sin dictamen previo de referencia).
   * Si existe un dictamen anterior de referencia, se debe activar complementariamente la skill `auditar-subsanacion`.

---

## 2. Verificación Estructural de los 19 Capítulos Obligatorios

Verificar la existencia formal, integridad de contenido y subtítulos obligatorios de cada uno de los 19 capítulos institucionales:

1. **Capítulo 1 — Introducción:** Contexto, motivación y párrafo formal de cierre (*«Estructura del documento»* que anticipa el recorrido capitular).
2. **Capítulo 2 — Planteo del Problema:** Dimensiones DevSecOps, fricción con pipelines CI/CD, silos de información entre desarrollo y seguridad; 6 problemas clave resaltados.
3. **Capítulo 3 — Justificación:** Dimensión Académica, Técnica, Económica (modelo cuantitativo de ROI/ahorro con paradigma *Shift-Left*) y Transferencia tecnológica.
4. **Capítulo 4 — Objetivos:** Objetivo General (4.1) y exactamente 9 Objetivos Específicos (4.2) alineados al alcance técnico.
5. **Capítulo 5 — Preguntas de Investigación:** 5 preguntas formales formuladas con precisión (PI1 a PI5).
6. **Capítulo 6 — Hipótesis:** 4 hipótesis (H1 a H4) tipografiadas formalmente como títulos de primer nivel (Heading 1).
7. **Capítulo 7 — Estado del Arte:** Análisis comparativo de herramientas existentes y presencia de la **Tabla 1** de contraste analítico (soluciones SOAR vs. escáneres aislados).
8. **Capítulo 8 — Marco Teórico y Conceptual:** Subsecciones obligatorias: 8.1 Fuzzing, 8.2 DAST/SAST, 8.3 Docker, 8.4 OWASP Top 10, 8.5 Pipeline Pattern SOLID, 8.6 SOAR.
9. **Capítulo 9 — Alcances y Limitaciones:** 9.1 Alcances del sistema y 9.2 Limitaciones explícitas de la solución.
10. **Capítulo 10 — Metodología:** 10.1 Diseño de investigación, 10.2 Fases del desarrollo, 10.3 Variables independientes y dependientes, 10.4 Instrumentos de recolección, 10.5 Amenazas a la validez, 10.6 Criterios de validación empírica.
11. **Capítulo 11 — Arquitectura Propuesta e Implementada:** 11.1 Arquitectura general, 11.2 Componentes del sistema (**Tabla 2** descriptiva), 11.3 Aislamiento de red Docker, 11.4 Flujo de ejecución detallado (Pasos 1 a 8), 11.5 Diagrama de secuencia formal.
12. **Capítulo 12 — Implementación Técnica:** 12.1 Docker y orquestación, 12.2 Pipeline orquestador, 12.3 Runner de ejecución, 12.4 Motor ZAP, 12.5 Motor ffuf, 12.6 Motor SQLMap, 12.7 Parsers de normalización, 12.8 Consolidación unificada de hallazgos, 12.9 Módulo de autenticación, 12.10 API REST y Frontend Web.
13. **Capítulo 13 — Resultados Obtenidos:** 13.1 Resumen cuantitativo global (**Tabla 3**), 13.2 Resultados ZAP (**Tabla 4**), 13.3 Resultados ffuf (**Tabla 5**), 13.4 Resultados SQLMap (**Tablas 6 y 7**), 13.5 Cobertura y mapeo OWASP Top 10 (**Tabla 8**).
14. **Capítulo 14 — Discusión:** 14.1 Cobertura de vulnerabilidades (**Tabla 9**), 14.2 Reducción de esfuerzo manual en validación de H1 (respaldado con Capítulo 17), 14.3 Impacto de caché en H4 y reproducibilidad (**Tablas 10 y 11**), 14.4 Política y gestión de timeouts, 14.5 Seguimiento y asistencia con IA, 14.6 Comparación con la industria y literatura.
15. **Capítulo 15 — Conclusiones y Trabajos Futuros:** 15.1 Conclusiones y respuestas formales a PI1-PI5, 15.1.1 **Tabla 12** con evaluación explícita de los 9 objetivos específicos cumplidos, 15.2 Trabajos futuros detallados en 8 puntos concretos.
16. **Capítulo 16 — Consideraciones Éticas y Legales:** Marco normativo argentino (Ley 26.388 art. 153 bis Código Penal), Convenio de Budapest y Código Ético ACM (principios 1.2, 1.3 y 1.6) aplicado a la protección de datos en `database.py`.
17. **Capítulo 17 — Desarrollo Experimental y Validación de Hallazgos:** Nota explícita de trazabilidad empírica, 17.1 Cronograma de ejecución, 17.2 Procedimientos detallados por vector de ataque, 17.3 Conclusiones del experimento y **Tabla 13** de tiempos (125 minutos totales = 75 automatizados + 50 manuales).
18. **Capítulo 18 — Referencias Bibliográficas:** 26 entradas bibliográficas académicas completas bajo norma APA 7.ª edición, con sangría francesa estricta y URLs activas/formateadas.
19. **Capítulo 19 — Anexos Técnicos:** Unificación exhaustiva de Anexos A al H, incluyendo diagramas ampliados de arquitectura y flujo en Anexo H.

---

## 3. Protocolo de los 5 Criterios de Tolerancia Cero

El asistente debe ejecutar sin excepción las siguientes verificaciones:

### Criterio 1: Recálculo Aritmético Independiente (13 Tablas)
Recalcular manualmente cada celda de las 13 tablas:
* **Tabla 1:** Total de herramientas y capacidades contrastadas.
* **Tabla 2:** Especificaciones de componentes y coherencia de versiones.
* **Tablas 3 a 8 (Resultados):** Sumas de hallazgos por severidad (Crítica, Alta, Media, Baja, Info), tiempos acumulados y porcentajes de detección. Comprobar que la suma de hallazgos individuales coincida exactamente con el total unificado de la Tabla 3.
* **Tabla 9 (Discusión de Cobertura):** Mapeo de vectores probados vs. detectados.
* **Tablas 10 y 11 (Caché y Tiempos):** Reducción porcentual de tiempo de ejecución con caché y tasas de acierto (*hit rate*).
* **Tabla 12 (Cumplimiento de Objetivos):** 9/9 objetivos marcados con métrica de logro cuantitativo.
* **Tabla 13 (Validación Experimental):** Desglose temporal: exactamente 75 min automatizados + 50 min de verificación manual = 125 min totales de experimentación.

### Criterio 2: Remisiones Cruzadas
* Cotejar cada referencia textual (*«según se expone en 11.2»*, *«véase Tabla 7»*, *«conforme a la Sección 14.3»*) con el destino real. Si una remisión apunta a un número equivocado de capítulo, sección o tabla, registrarla como hallazgo editorial de corrección obligatoria.

### Criterio 3: Consistencia Intercapítulos
* Contrastar los parámetros técnicos entre capítulos:
  * Flags de CLI: `--threads=10`, `--smart`, `--batch`, timeouts configurados.
  * Rutas y volúmenes Docker declarados en Cap. 11, 12, 17 y Anexos.
  * Tiempos de ejecución reportados en Cap. 13 vs. Cap. 14 vs. Cap. 17.

### Criterio 4: Trazabilidad a Archivos Empíricos Reales
* Ningún número o volcado de vulnerabilidad puede ser hipotético:
  * Cotejar contra `resultado_unificado.json`, logs de ejecución y benchmarks existentes en el repositorio.
  * Si se detectan métricas no fundamentadas en pruebas reales, marcar como hallazgo de severidad Alta.

### Criterio 5: Detección de Regresiones y Formato
* Verificar que elementos visuales y normativos no se hayan degradado:
  * Portada institucional limpia, sin texto duplicado ni saltos huérfanos.
  * Sangría francesa en las 26 referencias de APA 7.
  * Tablas completas sin desbordamiento de margen ni corte arbitrario de encabezados.

---

## 4. Tipificación de Hallazgos

Registrar cada defecto detectado asignándole un código y nivel de severidad:
* **Severidad Alta:** Afecta la validez académica, la consistencia aritmética, la trazabilidad empírica o contradice hipótesis/objetivos. Bloquea la aprobación sin condiciones.
* **Severidad Media:** Inconsistencias en parámetros intercapítulos, remisiones cruzadas desactualizadas, tablas con leyendas ambiguas o falta de detalle metodológico.
* **Severidad Baja:** Errores tipográficos menores, espaciados, ajustes de puntuación o sangría que no comprometen la comprensión técnica.

---

## 5. Matriz de Calificación por Capítulo

Asignar a cada uno de los 19 capítulos una calificación cuantitativa en la escala de 1,0 a 10,0, fundamentando detalladamente el puntaje en base al rigor técnico y la subsanación de observaciones. Calcular el promedio ponderado global.

---

## 6. Salida de la Skill

Al concluir la auditoría, estructurar la devolución al usuario con:
1. Resumen ejecutivo de la versión evaluada.
2. Calificación global estimada (x,x / 10).
3. Inventario consolidado de hallazgos por severidad.
4. Si el usuario solicita corregir, activar la **Metodología Paso a Paso** (aislar un único problema, indicar qué quitar y qué poner con texto listo para copiar).
