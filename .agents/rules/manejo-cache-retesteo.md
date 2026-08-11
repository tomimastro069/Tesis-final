---
trigger: always_on
---

# Regla 2: Manejo de Caché y Re-testeo (Cross-Pollination)

El orquestador de seguridad implementa una capa de persistencia mediante SQLite (o PostgreSQL) para evitar repetir escaneos innecesarios en rutas no vulnerables, lo que reduce drásticamente los tiempos entre corridas sucesivas sobre un mismo objetivo (caché incremental).

## Reglas sobre el Manejo de Datos:
1. **Respeto a la Caché Incremental:** Todo desarrollo nuevo o modificación en los módulos de ejecución (ZAP, ffuf, SQLMap) debe integrar o respetar la lectura de la base de datos previa (`sqlmap_history`, base de datos de ZAP). No se debe sugerir lógica que omita este chequeo previo.
2. **Re-testeo Obligatorio:** Las URLs que fueron confirmadas como **vulnerables** en corridas previas **NUNCA** se cachean como "seguras" para ser ignoradas. Siempre deben ser puestas en la cola y re-testeadas para comprobar si la vulnerabilidad sigue activa o si el equipo de desarrollo ya la mitigó.
3. **Flujo de Inyección Cruzada:** El resultado del descubrimiento de rutas (ffuf) debe inyectarse siempre en el árbol de ZAP antes del escaneo activo. La IA tiene estrictamente prohibido proponer código que rompa o independice esta retroalimentación cruzada entre herramientas.
