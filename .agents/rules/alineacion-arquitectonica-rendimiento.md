---
trigger: always_on
---

# Regla 1: Alineación Arquitectónica y Rendimiento

Al contribuir o sugerir cambios en el orquestador de seguridad, se debe respetar estrictamente la arquitectura estipulada en la tesis del proyecto, priorizando la **velocidad, el bajo consumo y la automatización incremental**.

## Convenciones Estrictas:
1. **Pipeline Pattern (Pipes and Filters):** Respetar y no alterar el flujo lógico básico: `spider` -> `ffuf` -> `inyección de rutas en ZAP` -> `active scan` -> `SQLMap`. Las herramientas se ejecutan en este orden para que los resultados de descubrimiento de una enriquezcan el ataque de las siguientes (cross-pollination).
2. **Minimalismo en Dependencias y Despliegue:** El orquestador es un sistema liviano diseñado para levantarse con un único comando (`docker compose up`). Queda estrictamente prohibido sugerir la incorporación de brokers de mensajería (Kafka, RabbitMQ) o bases de datos excesivamente pesadas que rompan la simplicidad del orquestador, a menos que el usuario lo demande explícitamente.
3. **Núcleo de Escáneres:** La combinación de contenedores de ZAP, ffuf y SQLMap es el núcleo inamovible de evaluación. No sugerir reemplazar este stack ni delegar sus análisis a plataformas comerciales de terceros. Todas las mejoras de rendimiento deben apuntar a optimizar las banderas de ejecución de estos tres escáneres o el manejo de caché.
