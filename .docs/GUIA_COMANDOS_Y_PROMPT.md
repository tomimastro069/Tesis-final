# Guía de Comandos Docker y Prompt para IA

## Requisitos previos

- **WSL Debian** con Docker instalado
- Archivo `C:\Users\windows\.wslconfig` con:
```ini
[wsl2]
memory=8GB
swap=8GB
processors=4
```
- Si se modifica `.wslconfig`, reiniciar WSL con: `wsl --shutdown` (desde CMD/PowerShell de Windows)

---

## Comandos Docker (ejecutar desde WSL Debian)

### 1. Navegar al proyecto
```bash
cd ~/proyectos/Tesis-final/orquestador-seguridad
```

### 2. Levantar los contenedores
```bash
docker compose up --build -d
```

**Respuesta esperada:**
```
[+] Building ...
[+] Running 3/3
 ✔ Container dvwa          Started
 ✔ Container zap           Started
 ✔ Container security-app  Started
```

### 3. Ejecutar el orquestador de seguridad
```bash
docker exec -it security-app python main.py
```

**Respuesta esperada:**
```
Iniciando escaneo contra: http://dvwa
--- Iniciando Orquestador para: http://dvwa ---

[1/3] Ejecutando ZAP Spider...

[2/3] Ejecutando ZAP Active Scan...
Progreso escaneo activo: 0%
Progreso escaneo activo: 35%
Progreso escaneo activo: 35%
...
Progreso escaneo activo: 100%

[3/3] Ejecutando FFUF...

Generando paquete de datos crudos...
--- Ejecución finalizada. Datos crudos guardados en: ./output/raw/resultado.json ---
Iniciando parseo de ZAP, SPIDER y FFUF:

--- Resultado unificado guardado en: ./output/raw/resultado_unificado.json ---
{
    "total_urls_unicas": X,
    "urls_spider": X,
    "alertas_zap": X,
    "rutas_ffuf": X
}

Ejecución finalizada. Revisa la carpeta /output/raw
```

> ⚠️ El escaneo activo puede tardar varios minutos. Es normal que se quede en 35% un rato.

### 4. Monitorear recursos (en otra terminal WSL)
```bash
docker stats --format "table {{.Name}}\t{{.MemUsage}}\t{{.CPUPerc}}"
```

**Respuesta esperada (durante escaneo activo):**
```
NAME           MEM USAGE / LIMIT     CPU %
security-app   ~22MiB / 7.7GiB       0%
zap            ~2-3.5GiB / 7.7GiB    ~200-400%
dvwa           ~130MiB / 7.7GiB      ~0.5%
```

### 5. Ver los archivos de salida
```bash
# Datos crudos consolidados
docker exec -it security-app cat output/raw/resultado.json | head -50

# Resultado unificado y parseado
docker exec -it security-app cat output/raw/resultado_unificado.json
```

### 6. Detener los contenedores
```bash
docker compose down
```

### 7. Ver logs de un contenedor específico
```bash
docker logs zap
docker logs security-app
docker logs dvwa
```

---

## Archivos de salida

| Archivo | Contenido |
|---------|-----------|
| `output/raw/resultado.json` | Datos CRUDOS de las 3 herramientas (spider_raw, zap_raw, ffuf_raw) |
| `output/raw/ffuf_raw.json` | Salida cruda de FFUF solamente |
| `output/raw/resultado_unificado.json` | Datos PARSEADOS y unificados de las 3 herramientas con resumen |

---

## Prompt para copiar y pegar en otro chat de IA

```
Estoy trabajando en mi tesis de la UTN. El proyecto es un "Orquestador de Seguridad" que ejecuta 3 herramientas de escaneo de vulnerabilidades web (ZAP Spider, ZAP Active Scan, FFUF) contra un target (DVWA) dentro de Docker, y luego parsea y unifica los resultados en un JSON final.

## Entorno
- Windows con WSL Debian
- Docker Compose con 3 contenedores: `dvwa` (target vulnerable), `zap` (OWASP ZAP escáner), `security-app` (mi app Python)
- Se necesita un archivo C:\Users\windows\.wslconfig con memory=8GB y swap=8GB para evitar que WSL crashee por el consumo de ZAP

## Estructura del proyecto (orquestador-seguridad/)
```
main.py                          → Punto de entrada, ejecuta pipeline + parseo + genera JSON unificado
docker-compose.yml               → 3 servicios: dvwa (puerto 8080), zap (puerto 8090), app
dockerfile                       → Python 3.11-slim + ffuf binario
requirements.txt                 → requests
wordlist.txt                     → Palabras para FFUF
app/
  workflow/
    pipeline.py                  → Orquesta los 3 escaneos (run_security_pipeline) + parseo (run_parser_pipeline)
  scanners/
    zap.py                       → Funciones: iniciar_spider, esperar_spider, obtener_urls, iniciar_escaneo_activo, esperar_escaneo_activo, obtener_reporte_json
    ffuf.py                      → Función run_ffuf que ejecuta el binario ffuf
  parsers/
    zap_parser.py                → parsear_zap (alertas) y parsear_spider (URLs)
    ffuf_parser.py               → parsear_ffuf (rutas encontradas con status 200/302)
  utils/
    results.py                   → consolidar_resultados (unifica sin duplicados) + resultados_prueba_json (guarda JSON final)
output/raw/
  resultado.json                 → Datos crudos de las 3 herramientas
  ffuf_raw.json                  → Salida cruda de FFUF
  resultado_unificado.json       → JSON final parseado y unificado
```

## Flujo de ejecución
1. `run_security_pipeline(target)` ejecuta secuencialmente:
   - ZAP Spider → descubre URLs del target
   - ZAP Active Scan → busca vulnerabilidades (la parte más pesada, ~2-3.5GB RAM)
   - FFUF → fuzzing de directorios/archivos
   - Guarda todo crudo en `resultado.json`
2. `run_parser_pipeline(resultado)` toma los datos crudos y:
   - Parsea spider → extrae URLs únicas con formato {url}
   - Parsea ZAP → extrae alertas con formato {url, vulnerabilidad, severidad, solucion}
   - Parsea FFUF → extrae rutas con formato {url, input, status}
   - Consolida los 3 en un dict con resumen (total_urls_unicas, urls_spider, alertas_zap, rutas_ffuf)
3. `resultados_prueba_json()` guarda el JSON unificado en `resultado_unificado.json`

## Comandos para ejecutar
```bash
cd ~/proyectos/Tesis-final/orquestador-seguridad
docker compose up --build -d
docker exec -it security-app python main.py
```

## Estado actual
- Todos los escaneos funcionan correctamente
- Los parsers funcionan y generan el JSON unificado
- El target es DVWA (Damn Vulnerable Web Application) en http://dvwa dentro de la red Docker

Necesito ayuda con: [DESCRIBÍ ACÁ LO QUE NECESITÁS]
```

---

*Última actualización: 19 de febrero de 2026*

Para ver un listado limpio de qué bases de datos y qué tablas se han extraído (sin ver todo el JSON gigante de las filas y columnas), podés ejecutar este comando que filtra los duplicados:

bash
docker exec -it security-db psql -U security_user -d security_history -c "SELECT DISTINCT db_name, table_name FROM sqlmap_tables_history;"

para ver la tabla completa de usuarios: 
docker exec -it security-db psql -U security_user -d security_history -c "
SELECT 
  fila->>0 AS user_id,
  fila->>1 AS username,
  fila->>2 AS avatar,
  fila->>3 AS password,
  fila->>4 AS last_name,
  fila->>5 AS first_name,
  fila->>6 AS last_login,
  fila->>7 AS failed_login
FROM (
  SELECT json_array_elements(rows_data::json) AS fila 
  FROM (
    SELECT rows_data 
    FROM sqlmap_tables_history 
    WHERE table_name = 'users' 
    ORDER BY timestamp DESC 
    LIMIT 1
  ) latest
) sub;"

para ver la tabla completa guestbook:

docker exec -it security-db psql -U security_user -d security_history -c "
SELECT 
  fila->>0 AS comment_id,
  fila->>1 AS name,
  fila->>2 AS comment
FROM (
  SELECT json_array_elements(rows_data::json) AS fila 
  FROM (
    SELECT rows_data 
    FROM sqlmap_tables_history 
    WHERE table_name = 'guestbook' 
    ORDER BY timestamp DESC 
    LIMIT 1
  ) latest
) sub;"
