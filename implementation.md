
# Apartir de ahora vamos a empezar el desarrollo de optimizacion

### dejamos dado el proyecto como finalizado, para luego continuar a comparar la nueva version y analizar resultados

---
---
---

# Optimización de FFUF con Base de Datos de Historial

## Descripción

Para optimizar el rendimiento y reducir el tiempo de escaneo con FFUF, se agregará una base de datos local SQLite. Esta base de datos almacenará el historial de las palabras probadas (procedentes de las wordlists) en relación con el target atacado.

De esta forma, en futuras ejecuciones sobre la misma URL:

1. El sistema leerá la wordlist original.
2. Extraerá de la BD las palabras que ya fueron escaneadas contra dicho target.
3. Se generará una wordlist temporal que contenga *únicamente* las palabras no probadas.
4. FFUF ejecutará el escaneo sólo empleando esta wordlist reducida.
5. Una vez finalizado el escaneo, se guardarán esas nuevas palabras en el historial de la BD.

## ✅ User Review Required (COMPLETADO)

1. **Ubicación de la Base de Datos:** ✅ NO rastrear en Git — agregada a `.gitignore` para que el historial sea local de cada máquina.
2. **Dependencias:** ✅ Usamos `sqlite3` nativo de Python — sin nuevos paquetes.

## Proposed Changes

### `app/db` (Nueva Capa) — ✅ COMPLETADO

#### [NEW] `app/db/__init__.py`

#### [NEW] `app/db/database.py`

Se creará un nuevo módulo para manejar SQLite que contará con:

* Función `init_db()`: Para crear la base de datos `history.db` y una tabla `ffuf_history` (target_url, word, timestamp).
* Función `get_tested_words(target_url)`: Para obtener un conjunto (`Set`) de todas las palabras ya probadas en ese target.
* Función `save_tested_words(target_url, words_list)`: Para registrar un nuevo lote de palabras probadas en un target dado.

### `app/scanners` — ✅ COMPLETADO

#### [MODIFY] `app/scanners/ffuf.py`

* Antes de componer el comando de `ffuf`, leeremos de `wordlist_path`.
* Usaremos `get_tested_words(target_url)` para excluir las palabras ya atacadas.
* Crearemos una `temp_wordlist.txt` en `output_dir` (ej: `/output/raw/temp_wordlist.txt`).
* Si `temp_wordlist.txt` queda vacío (se probaron ya todas las palabras), lo indicaremos y devolveremos un resultado con salida "Omitido" (para no afectar los reportes y evitar llamadas innecesarias a FFUF).
* Si se ejecuta y termina exitosamente, invocaremos a `save_tested_words` para guardar el registro de escaneo en ese target.

### `app/workflow` — ✅ COMPLETADO

#### [MODIFY] `app/workflow/pipeline.py`

* En `run_security_pipeline`, importaremos y llamaremos a `init_db()` en las fases iniciales, garantizando que el esquema de la BD exista antes de que intervenga `run_ffuf`.
* Validaremos apropiadamente cuando el resultado crudo regrese vacío debido a un escaneo omitido.

---

## ✅ Estado: IMPLEMENTACIÓN COMPLETA

*Todos los cambios descritos arriba han sido implementados.*

---

## Open Questions

* Si en el futuro cambian las rutas (o publican un release nuevo de la web) en tu local/target específico ¿Deberíamos considerar alguna bandera o comando al ejecutar `main.py` para forzar un "limpiado de base de datos de FFUF" (Forzar escaneo)?

## Verification Plan

### Automated Tests

1. Ejecutar el orquestador contra el target default (`http://dvwa/`).
2. Validar que FFUF corre normal en su primera pasada.
3. Ejecutarlo una segunda vez con el mismo nivel de wordlist.
4. Confirmar en los logs la advertencia de que "todas las palabras ya fueron probadas" y que FFUF se omite (y dura 0 segundos), sin romper el reporte generado en PDF/MD.
