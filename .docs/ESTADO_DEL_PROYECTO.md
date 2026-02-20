# 📊 Estado del Proyecto — Orquestador de Seguridad (Fuzzing Automatizado)

**Fecha de análisis:** 20 de febrero de 2026

---

## 🟢 LO QUE YA ESTÁ HECHO (Funcional)

### ✅ Fase 1 — Entorno de Laboratorio

| Componente               | Estado   | Detalles                                                   |
| ------------------------ | -------- | ---------------------------------------------------------- |
| DVWA (target vulnerable) | ✅ Hecho | Contenedor Docker configurado en `docker-compose.yml`      |
| OWASP ZAP (daemon)       | ✅ Hecho | Contenedor Docker, API en puerto 8090, API key configurada |
| Docker Compose           | ✅ Hecho | 3 servicios: `dvwa`, `zap`, `security-app`                 |
| Dockerfile               | ✅ Hecho | Python 3.11-slim + binario ffuf                            |
| `.wslconfig` documentado | ✅ Hecho | Guía en `GUIA_COMANDOS_Y_PROMPT.md`                        |

### ✅ Fase 2 — Módulos Core (Perfil 1: Tomas - Ingeniero de Ejecución)

| Módulo             | Estado   | Detalles                                                                                                                                    |
| ------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `runners/exec.py`  | ✅ Hecho | `run_command()` con subprocess, manejo de timeout y errores                                                                                 |
| `scanners/zap.py`  | ✅ Hecho | 6 funciones: `iniciar_spider`, `esperar_spider`, `obtener_urls`, `iniciar_escaneo_activo`, `esperar_escaneo_activo`, `obtener_reporte_json` |
| `scanners/ffuf.py` | ✅ Hecho | `run_ffuf()` que ejecuta ffuf vía `run_command()` y guarda JSON                                                                             |

### ✅ Fase 3-4 — Módulos Lógica (Perfil 2: Cristian - Arquitecto de Lógica)

| Módulo                   | Estado   | Detalles                                                                       |
| ------------------------ | -------- | ------------------------------------------------------------------------------ |
| `parsers/zap_parser.py`  | ✅ Hecho | `parsear_zap()` (alertas) y `parsear_spider()` (URLs), con deduplicación       |
| `parsers/ffuf_parser.py` | ✅ Hecho | `parsear_ffuf()` filtra status 200/302, sin duplicados                         |
| `workflow/pipeline.py`   | ✅ Hecho | `run_security_pipeline()` (orquestación) + `run_parser_pipeline()` (parseo)    |
| `utils/results.py`       | ✅ Hecho | `consolidar_resultados()` (unifica) + `resultados_prueba_json()` (guarda JSON) |

### ✅ Punto de Entrada

| Módulo    | Estado   | Detalles                                          |
| --------- | -------- | ------------------------------------------------- |
| `main.py` | ✅ Hecho | Ejecuta pipeline → parseo → guarda JSON unificado |

### ✅ Archivos de Salida Generados

- `output/raw/resultado.json` — Datos crudos de las 3 herramientas
- `output/raw/ffuf_raw.json` — Salida cruda de FFUF
- `output/raw/resultado_unificado.json` — JSON parseado y unificado

---

## 🔴 LO QUE FALTA PARA COMPLETAR EL PROYECTO

### ❌ 1. `config/settings.py` — VACÍO

**Prioridad:** 🟡 Media  
**Responsable según docs:** Juan (Perfil 3)  
**Qué debería tener:**

- Variables de configuración centralizadas (ahora están hardcodeadas):
  - `ZAP_HOST`, `ZAP_PORT`, `API_KEY` (actualmente hardcodeadas en `scanners/zap.py`)
  - `TARGET_URL` (hardcodeada en `main.py`)
  - `WORDLIST_PATH`, `OUTPUT_DIR` (hardcodeadas en `pipeline.py`)
  - Timeouts configurables
- Esto evitaría tener valores mágicos repartidos en el código

### ❌ 2. `reports/generator.py` — VACÍO

**Prioridad:** 🔴 Alta (es requisito de evaluación: 15 puntos)  
**Responsable según docs:** Juan (Perfil 3)  
**Qué debería tener:**

- Función que tome el `resultado_unificado.json` y genere un **reporte legible** en Markdown
- El reporte debe incluir:
  - Fecha del escaneo
  - URL objetivo
  - Resumen ejecutivo (tabla de severidades)
  - Lista de vulnerabilidades críticas/altas con descripción y solución
  - Lista de rutas descubiertas por ffuf
  - URLs del spider
  - Plan de remediación
- Guardar reporte en `output/reports/`

### ❌ 3. `readme.md` — VACÍO

**Prioridad:** 🟡 Media  
**Responsable según docs:** Juan (Perfil 3)  
**Qué debería tener:**

- Descripción del proyecto
- Requisitos previos
- Instrucciones de instalación y ejecución
- Estructura del proyecto
- Ejemplo de salida

### ❌ 4. Carpeta `output/reports/` — NO EXISTE

**Prioridad:** 🔴 Alta (ligada al generador de reportes)  
**Qué debería contener:**

- Reportes finales generados automáticamente (Markdown/texto plano)
- Se menciona en la estructura del proyecto en los docs pero no se creó

### ❌ 5. Integración de `settings.py` en el código existente

**Prioridad:** 🟡 Media  
**Detalle:**

- Una vez creado `settings.py`, hay que importar las constantes en:
  - `scanners/zap.py` (reemplazar `ZAP_HOST`, `ZAP_PORT`, `API_KEY`)
  - `workflow/pipeline.py` (reemplazar `WORDLIST_PATH`, `OUTPUT_DIR`)
  - `main.py` (reemplazar target hardcodeado)

### ❌ 6. `requirements.txt` — INCOMPLETO

**Prioridad:** 🟢 Baja  
**Estado actual:** Solo tiene `requests`  
**Posible mejora:** Agregar versiones pinned (`requests==2.x.x`) para reproducibilidad

---

## 🟡 COSAS OPCIONALES (Fase 7 del plan)

Estas tareas **NO son obligatorias para aprobar** pero suman nota:

| Tarea Opcional                    | Estado                      | Notas                                                                         |
| --------------------------------- | --------------------------- | ----------------------------------------------------------------------------- |
| Integración con SQLMap            | ❌ No implementado          | Solo para URLs con `?` parámetros. No es prioritario                          |
| Clasificación de Severidad (CVSS) | ⚠️ Parcial                  | ZAP ya devuelve `riskdesc`, pero no hay clasificación formal en consolidación |
| Base de datos PostgreSQL          | ❌ No implementado          | Esquema SQL está documentado pero no implementado                             |
| Integración CI/CD                 | ❌ No implementado          | Mencionado como PB-3 en docs                                                  |
| Envío de reportes por Email/Slack | ❌ No implementado          | Mencionado en docs                                                            |
| Integración con n8n               | ❌ No implementado como tal | El proyecto usa Python puro en vez de n8n (decisión válida)                   |

---

## 📋 RESUMEN: CHECKLIST PARA APROBAR

Según la documentación de "pasos a seguir", los **entregables mínimos** para aprobar son:

| Entregable                        | Estado                                       | ¿Listo? |
| --------------------------------- | -------------------------------------------- | ------- |
| ✔️ DVWA funcionando               | Contenedor Docker operativo                  | ✅      |
| ✔️ Workflow funcional             | Pipeline Python completo (security + parser) | ✅      |
| ✔️ ZAP + ffuf integrados          | Ambos scanners implementados y parseados     | ✅      |
| ✔️ Reporte automático             | **`generator.py` VACÍO — NO GENERA REPORTE** | ❌      |
| ✔️ Capacidad de explicar el flujo | Depende de cada integrante                   | ⚠️      |

---

## 🎯 PLAN DE ACCIÓN — Orden de prioridad

### 1️⃣ **URGENTE: Implementar `reports/generator.py`**

- Es el único entregable obligatorio que falta
- Debe tomar `resultado_unificado.json` y generar un `.md` legible
- Crear carpeta `output/reports/`

### 2️⃣ **IMPORTANTE: Completar `config/settings.py`**

- Centralizar las variables de configuración
- Importarlas en los módulos correspondientes

### 3️⃣ **RECOMENDADO: Escribir `readme.md`**

- Documentación básica del proyecto

### 4️⃣ **OPCIONAL: Integrar el reporte en `main.py`**

- Que `main.py` llame a `generator.py` después del parseo
- Flujo completo: escaneo → parseo → consolidación → **reporte**

---

_Análisis generado el 20/02/2026 comparando la documentación del proyecto con el código fuente actual._
