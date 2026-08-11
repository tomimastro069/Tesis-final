---
trigger: always_on
---

# Regla 5: Procesamiento de Datos (Parsers y Consolidación)

El orquestador produce un único archivo estructurado (`resultado_unificado.json`) a partir de las salidas heterogéneas de las herramientas, siguiendo el principio de responsabilidad única.

## Convenciones de Procesamiento:
1. **Parsers Independientes:** Cada herramienta (ZAP, ffuf, SQLMap) debe tener su propio script de parseo en el directorio `parsers/`. No se deben mezclar lógicas de parseo de distintas herramientas en un solo archivo.
2. **Estructura del JSON Unificado:** Cualquier modificación en los datos recolectados debe concluir en el archivo JSON consolidado final. La estructura de este JSON (separando el bloque "resumen" de los bloques individuales por herramienta) no debe alterarse de manera que rompa la lectura que hace el Frontend y la Base de Datos.
3. **Separación de Salidas:** Mantener estrictamente la separación de directorios entre los resultados en bruto generados por las herramientas (`output/raw/`) y los resultados procesados y consolidados (`output/reports/`).
