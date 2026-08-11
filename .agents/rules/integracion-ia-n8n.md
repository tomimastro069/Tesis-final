---
trigger: always_on
---

# Regla 6: Integración con IA y n8n

El proyecto utiliza un flujo de n8n para proveer sugerencias de mitigación asistidas por Inteligencia Artificial. Esta es la única participación directa de la IA en el flujo de seguridad, según la arquitectura y el alcance definido en la tesis.

## Restricciones sobre el Uso de IA:
1. **Solo Sugerencias de Mitigación:** La IA (vía n8n) se usa exclusivamente para explicar vulnerabilidades detectadas y ofrecer pasos de mitigación al usuario final desde el panel web.
2. **Resultados Intocables:** La IA NO DEBE alterar, filtrar, ni recalificar la severidad de los hallazgos técnicos "duros" generados por ZAP, ffuf y SQLMap. Los escáneres son la única fuente de verdad técnica sobre la que se construye el reporte.
3. **No Comercialización:** Como estipula explícitamente la tesis, no se debe sugerir un modelo de priorización de riesgo basado en IA con formato de suscripción paga u orientado a terceros. Toda funcionalidad de IA debe mantenerse contenida dentro del alcance ético del entorno de laboratorio gratuito para investigación.
