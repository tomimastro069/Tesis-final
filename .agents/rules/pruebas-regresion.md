---
trigger: always_on
---

# Regla 8: Ejecución Obligatoria de Pruebas de Regresión

Para evitar que cambios en los módulos de escaneo, bases de datos o parsers introduzcan bugs en el pipeline del orquestador, se debe verificar el correcto funcionamiento mediante los scripts de testing del proyecto.

## Directivas de Pruebas:
1. **Validación tras Cambios en Backend:** Si se realizan modificaciones en archivos dentro de `app/scanners/`, `app/parsers/`, `app/db/` o `app/workflow/`, Antigravity debe proponer o invocar de forma proactiva la ejecución de las pruebas unitarias relacionadas:
   - Modificaciones en parsers -> sugerir ejecutar `test_parsers.py`.
   - Modificaciones en base de datos o lógica de FFUF -> sugerir ejecutar `test_speed.py`.
   - Modificaciones en SQLMap -> sugerir ejecutar `test_sqlmap.py`.
   - Modificaciones en ZAP -> sugerir ejecutar `test_zap.py`.
2. **Chequeo de Reportes:** Se debe asegurar que las modificaciones en el formato JSON consolidado no rompan la generación de los reportes unificados ni la lectura por parte de la API y el frontend.
