---
trigger: always_on
---

# Regla 7: Prevención de Commits con Ajustes Temporales de Rendimiento

El rendimiento del orquestador (hilos y consumo) es la base comparativa de la tesis. Las optimizaciones que reduzcan los recursos locales para cuidar la PC del desarrollador son temporales y no deben subirse al repositorio.

## Directivas de Control:
1. **Advertencia de Commit:** Al realizar o proponer cambios en archivos de configuración críticos (`docker-compose.yml`, `zap.py`, `sqlmap.py`) que rebajen los hilos o limiten recursos por debajo del estándar de la tesis, Antigravity debe emitir una advertencia visible en su respuesta indicando que esos cambios **no deben ser commiteados**.
2. **Preservar Documentación de Tesis:** Bajo ninguna circunstancia se debe sugerir la modificación de archivos markdown de documentación de la tesis (ej. `OPTIMIZACION_ZAP.md` o el documento principal de la tesis) para adaptarlos a las métricas del entorno local temporal. La documentación de la tesis debe reflejar siempre el rendimiento optimizado máximo.
