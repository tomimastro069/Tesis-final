# Registro de Mejoras Técnicas: Orquestador de Seguridad

Este documento resume las optimizaciones implementadas para transformar el orquestador básico en una herramienta de grado profesional, garantizando la precisión de los datos y maximizando la superficie de ataque.

---

## 1. FFUF: Aislamiento y Precisión
*   **Limpieza Proactiva:** Se implementó el borrado automático de `ffuf_raw.json` antes de cada ejecución. Esto evita que el orquestador lea resultados "fantasmas" de escaneos anteriores si una nueva ejecución falla.
*   **Prevención de Contaminación:** Al asegurar que cada ejecución de FFUF parta de un archivo vacío, se garantiza que las rutas inyectadas en ZAP correspondan exclusivamente al target actual.

## 2. ZAP Parser: Inteligencia Multisitio
*   **Arquitectura Multisite:** El parser fue rediseñado para iterar sobre todos los sitios (`site`) detectados por ZAP. 
    *   *Problema resuelto:* ZAP a veces separa un mismo host en varios nodos (ej: `http://dvwa` y `http://dvwa/`). El código viejo solo miraba el primero, reportando a veces "0 alertas" erróneamente.
    *   *Resultado:* Consolidación total de alertas de todos los nodos en un único reporte veraz.
*   **Mapeo de Campos Extendido:** Se agregaron campos de descripción, solución y método HTTP para enriquecer los reportes técnicos.

## 3. SQLMap: Modo "Tiger" (Agresividad Máxima)
*   **Soporte para Formularios (`--forms`):** SQLMap ahora no solo busca parámetros en la URL (GET), sino que analiza y ataca formularios POST (Login, búsquedas, etc.).
*   **Niveles de Ataque:** Se incrementó a `level 3` y `risk 3`, permitiendo detectar vulnerabilidades más profundas como inyecciones basadas en tiempo (Time-based Blind).
*   **Optimización de Rendimiento:** 
    *   `--threads=5`: Ejecución en paralelo para reducir tiempos de espera.
    *   `--dbms=MySQL`: Pre-configuración para el motor de DVWA, evitando fases de detección innecesarias.
*   **Filtro de URLs Inteligente:** Se amplió el filtro para que SQLMap reciba todos los archivos dinámicos (`.php`, etc.) encontrados por el Spider, permitiéndole buscar formularios ocultos.

## 4. Pipeline: Orquestación Robusta
*   **Limpieza de Sesión ZAP:** Se integró `limpiar_sesion_zap()` al inicio de cada pipeline, invocando `newSession` en la API de ZAP. Esto elimina alertas y Site Trees de escaneos previos.
*   **Cebado de Sesión (Priming):** Implementamos una visita forzada a la URL principal con cookies **antes** de lanzar el Spider. 
    *   *Por qué:* Esto asegura que ZAP vea la aplicación logueada desde el primer segundo, permitiendo que el Spider descubra todo el menú interno que antes quedaba oculto tras el login.
*   **Manejo de Cookies Global:** Inyección centralizada de cookies en todas las herramientas del flujo para mantener la persistencia de la sesión en todo el ciclo de vida del ataque.

---
**Resultado Final:** Un pipeline determinista, agresivo y capaz de penetrar aplicaciones autenticadas con precisión quirúrgica.
