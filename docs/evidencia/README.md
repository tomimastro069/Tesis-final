# Evidencia Primaria de Pruebas Experimentales
**Universidad Tecnológica Nacional — Facultad Regional Mendoza**  
*Tecnicatura Universitaria en Programación (TUP)*  
**Trabajo Final de Graduación:** *Orquestador de Seguridad: Fuzzing Automatizado de Aplicaciones Web*  
**Subtítulo:** *Sistema de orquestación para análisis automatizado de vulnerabilidades web mediante fuzzing y escaneo activo*  
**Autores:** Tomás Mastropietro, Cristian Krahulik, Juan Segura  
**Directores de Tesina:** Lic. Alberto Cortez, Ing. Ariel Enferrel  

---

## 1. Propósito de este Directorio

El presente directorio (`docs/evidencia/`) aloja y resguarda los artefactos documentales y registros experimentales primarios que sustentan los capítulos de **Resultados Obtenidos (Capítulo 13)** y **Discusión (Capítulo 14)** del informe de tesina.

Este directorio se encuentra expresamente excluido de las reglas de omisión de `.gitignore`, garantizando la disponibilidad pública, la trazabilidad directa y la auditabilidad externa de la evidencia frente a los tribunales evaluadores y la comunidad académica.

---

## 2. Inventario de Artefactos Disponibles

### `reporte_seguridad.md` (Corrida Maestra del 5 de agosto de 2026)
* **Fecha y hora de generación:** 2026-08-05 19:53:35 (hora local del entorno).
* **Entorno de ejecución:** Red contenerizada Docker (`sec-net`), aplicación objetivo DVWA (*Damn Vulnerable Web Application*, versión 1.3), nivel de seguridad `low`, pipeline automatizado end-to-end (OWASP ZAP 2.17.0, ffuf v2.1.0-dev, SQLMap 1.10.7.253#dev).
* **Métricas cuantitativas consolidadas (Capítulo 13, Tabla 3):**
  - Total de URLs únicas analizadas: **34** (unión consolidada de 24 del Spider de ZAP + 4 rutas exclusivas de ffuf + 5 URLs de directorios de alertas ZAP Directory Browsing + 1 URL vulnerable reportada por SQLMap).
  - URLs descubiertas por el Spider de ZAP: **24**.
  - Alertas de seguridad reportadas por ZAP: **37** (Capítulo 13, Tabla 4).
  - Rutas descubiertas por ffuf: **8** (Capítulo 13, Tabla 5).
  - Vulnerabilidades confirmadas por SQLMap: **4** (Capítulo 13, Tabla 6: Boolean-based blind, Error-based, Time-based blind y UNION query sobre `/vulnerabilities/brute/`, parámetro `username`).
* **Volcado de datos relacionales (Capítulo 13, Tabla 7):**
  - Extracción en vivo de la tabla `dvwa.users` (5 registros).
  - Timestamps de registro: `2026-08-05 19:50:13`.
  - Hash de usuario `admin`: `5f4dcc3b5aa765d61d8327deb882cf99` (hash MD5 de la contraseña por defecto «password»).

---

## 3. Aclaración Metodológica sobre Artefactos Crudos Intermedios

En el ciclo de desarrollo y prueba del orquestador, el directorio `orquestador-seguridad/output/raw/` resguarda registros de pruebas de integración continua y verificación técnica:
1. **Registros de corridas históricas previas:** Los archivos crudos versionados en el repositorio (`sqlmap_bg.log` de fecha 02/08/2026, `resultado_unificado.json`, etc.) documentan ejecuciones de calibración del sistema. Específicamente, `sqlmap_bg.log` es citado en la sección 13.4 del informe como testimonio empírico de la variabilidad natural de SQLMap frente a parametrizaciones dinámicas.
2. **Corrida maestra del 5 de agosto de 2026:** Los archivos volátiles de esa ejecución puntual no requirieron preservación redundante en `output/raw/`, dado que fueron consolidados de forma íntegra, canónica y estructurada en el reporte final `reporte_seguridad.md` alojado en este directorio.
3. **Ensayos de benchmark de caché del 6 de agosto de 2026:** Los volcados intermedios `resultado_sin_cache.json` y `resultado_con_cache.json` generados durante los ensayos de evaluación del motor de caché incremental (Tablas 10 y 11 del Capítulo 14) no se conservaron en el repositorio. Conforme a lo declarado en las secciones 14.3 y 9.2 del informe, la contrastación de la Hipótesis 4 se sustenta en los registros cronometrados reportados por los autores y ratificados de forma independiente por el registro audiovisual del 15 de septiembre de 2026 (Anexo I.2, Tabla 14).
