# Evidencia Primaria de Pruebas Experimentales
**Universidad Tecnológica Nacional — Facultad Regional Mendoza**  
*Tecnicatura Universitaria en Programación (TUP)*  
**Trabajo Final de Graduación:** *Desarrollo de un Orquestador de Seguridad Web Automatizado mediante la Integración de Herramientas DAST de Código Abierto (OWASP ZAP, ffuf, SQLMap)*  
**Autores:** Tomás Mastropietro, Cristian Krahulik  
**Directores:** Lic. Alberto Cortez, Ing. Ariel Enferrel  

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

En el entorno de desarrollo del orquestador, el archivo `.gitignore` contiene la regla `output/raw/*` para evitar la sobrecarga del repositorio Git con archivos temporales y volcados volátiles generados dinámicamente durante las pruebas de integración continua.

Como consecuencia de dicha política:
1. **Volcados crudos del 5 de agosto:** Los archivos intermedios de texto plano (`sqlmap_bg.log` crudo y el archivo temporal `resultado_unificado.json` en `output/raw/`) no fueron versionados en Git en esa pasada, quedando consolidados de manera definitiva y reproducible en el informe `reporte_seguridad.md`.
2. **Archivos de benchmark de caché del 6 de agosto:** Los volcados intermedios `resultado_sin_cache.json` y `resultado_con_cache.json` generados durante los ensayos de evaluación del impacto del caché incremental (Tablas 10 y 11 del Capítulo 14) no se conservaron en el repositorio. Conforme a lo declarado en las secciones 14.3 y 9.2 del informe, la contrastación de la Hipótesis 4 se sustenta en los registros cronometrados documentados por los autores en el informe escrito.
