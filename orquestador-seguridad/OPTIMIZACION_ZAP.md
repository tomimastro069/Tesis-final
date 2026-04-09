# 🚀 Optimización de Rendimiento Global: ZAP, FFUF & SQLMap

Este documento detalla las configuraciones de rendimiento específicas aplicadas a los motores de escaneo (OWASP ZAP, FFUF y SQLMap) para lograr reducir los tiempos de escaneo en el orquestador general de horas a minutos.

## El Problema: ¿Por qué ZAP tardaba tanto?
Por defecto, el *Active Scan* de ZAP está configurado para la extrema precaución. Su diseño original es testear sitios sin llegar a "tumbarlos" (denegación de servicio accidental) e intentar leer cada respuesta de forma clínica. 

Como ZAP explora múltiples problemas a la vez (XSS, inyecciones OS, SQLi, Fugas), genera un efecto de **crecimiento exponencial**. Si prueba 50 ataques distintos en cada parámetro, y una página web tiene 10 parámetros, procesará 500 envíos... solamente en una página. Sumado a que por defecto dispara los ataques lentamente, un escaneo rutinario puede superar fácilmente las 4 horas bloqueando el orquestador entero.

---

## Configuración Implementada (Antes vs Ahora)

### 1. Multiplicación de Hilos Concurrentes (`ThreadPerHost`)
* **Cómo funcionaba antes:** ZAP utiliza siempre **2 hilos por defecto**. Lanzando solo 2 inyecciones a la vez.
* **Cómo está ahora:** Aumentado forzadamente a **20 hilos**.
* **Por qué se hizo:** Obligamos a ZAP a abusar del ancho de banda y paralelizar el proceso enviando múltiples solicitudes simultáneas HTTP de ida y vuelta. La velocidad aumenta en un factor de 10x asumiendo que el servidor objetivo puede soportar esa carga (stress) sin caerse.

### 2. Límite de Asedio por Regla (`MaxRuleDurationInMins`)
* **Cómo funcionaba antes:** Ilimitado (valor 0). En la comprobación de ataques silenciosos (como *Blind Time-Based SQL Injection*), ZAP inyecta matemáticas que generan retrasos. Esos procesos pueden hacer que la herramienta se quede congelada atacando **un único botón** de tu página web durante 20 minutos.
* **Cómo está ahora:** Límite fijado en **1 minuto**.
* **Por qué se hizo:** Si a los 60 segundos de reloj físico, ese ataque en particular no obtuvo certeza o sigue colgado, aborta la operación de forma inmediata sin considerarlo vulneable, empujando la cola y forzando a ZAP a saltar al siguiente de la lista (ej: probar con XSS). Destraba los peores embotellamientos lógicos.

### 3. Exhaustión de Tiempo Global (`MaxScanDurationInMins`)
* **Cómo funcionaba antes:** Ilimitado (valor 0). Si un objetivo de caja negra tenía miles de rutas detectables en el Spider, ZAP no pararía hasta agotar el 100% de los elementos el día siguiente.
* **Cómo está ahora:** Límite máximo de duración seteado en **10 minutos**.
* **Por qué se hizo:** Otorga predictibilidad al backend. Al obligarlo a morir a los 10 minutos, aseguramos que el Pipeline principal de Python (`main.py`) continúe siempre su flujo lógico, recopile los resultados generados hasta esa "fecha de caducidad" y libere el hilo operativo para iniciar el turno de SQLMap/FFUF sin pausas infinitas.

### 4. Análisis profundo de DOM y Tokens (`HandleAntiCSRFTokens`)
* **Cómo funcionaba antes:** Activado (`true`). Los servidores usan "Tokens dinámicos" Anti-CSRF (letras aleatorias ocultas) en los formularios. Para hackear un formulario así, ZAP debe renderizar el HTML tras cada ataque, usar CPU para buscar la nueva llave, guardarla y adjuntarla en el siguiente Payload inyectado.
* **Cómo está ahora:** Apagado por la fuerza (`false`).
* **Por qué se hizo:** Procesar cadenas HTML y leer el DOM para una extracción dinámica consume un volumen infernal de recursos de CPU locales. Al indicarle a ZAP que no se interese por este control, aceleramos el análisis directo de parámetros web y sub-rutas sin detenernos a descifrar bloqueos CSRF que pueden ser irrelevantes.

---

## ⚡ Implementación de Caché SQLite para FFUF

FFUF es extremadamente rápido, pero sufre de redundancia: al realizar auditorías periódicas a un mismo target, volverá a someter miles de peticiones de red por cada elemento en el diccionario (*wordlist*), malgastando tiempo y ancho de banda probando repetidamente rutas que ya conocemos.

Para mitigar esto, hemos implementado un sistema de **Memoria Transaccional** apoyado en una base de datos SQLite (`app/db/database.py`).

### Filtro Incremental (Diferencia de Conjuntos)
* **Cómo funcionaba antes:** Si la *wordlist* contenía 50,000 palabras, FFUF lanzaba siempre 50,000 peticiones HTTP por target, en cada iteración del orquestador.
* **Cómo está ahora:**
    1. Antes del ataque, el orquestador lee la base de datos usando la URL objetivo y obtiene todas las palabras previamente inyectadas en sesiones anteriores.
    2. Aplica una resta lógica matemática (`untested = all_words - tested_words`) y genera una *Wordlist Temporal* en la carpeta `/output` con **solo** las palabras "vírgenes" no testeadas.
    3. Si la resta da 0 (todas las palabras ya constan en base de datos para ese sitio), FFUF establece la bandera inteligente `skipped = True` omitiendo al 100% el estrés al servidor destino.

### Impacto en la Velocidad
Esto transforma al módulo FFUF en algo puramente **Incremental**. Las pasadas posteriores se evalúan en menos de 10 milisegundos a menos que manualmente agregues nuevo vocabulario al `.txt` del directorio de `wordlists`, logrando una re-usabilidad perfecta en flujos de Integración Continua.

---

## 💉 Maximización de Velocidad en SQLMap

El uso estándar de SQLMap realiza un ataque ciego comprobando combinaciones de falso/verdadero y calculando tiempos de latencia del servidor, lo que hace que cada evaluación tome minutos interminables, incluso en parámetros web que claramente no están conectados a una base de datos.

Para erradicar esta pérdida de tiempo, forzamos la inyección de **banderas agresivas** en el subproceso manejado por `app/scanners/sqlmap.py`:

### Configuración de Ataque 

* **Multi-Threading (`--threads=10`):** 
  Por defecto, SQLMap escanea pidiendo datos en estricta fila india (1 hilo). Lo hemos forzado al máximo límite técnico permitido por el framework (10 hilos). Multiplica exponencialmente la capacidad de validar vulnerabilidades basadas en booleanos o *Blind Timed*.
* **Escaneo de Inteligencia Heurística (`--smart`):**
  Sin esta bandera, SQLMap probaría fuerza bruta de inyecciones en *absolutamente todos* los parámetros (`?id=`, `?lang=`, `?page=`). Al aplicar `--smart`, el scanner hace un chequeo relámpago con una simple comilla. Si el comportamiento de la página no muta ni devuelve errores lógicos, SQLMap descartará ese parámetro al instante y pasará a otra ruta, ahorrando cerca de un 80% del tiempo neto de escaneo.
* **Prohibición de latencias (`--technique=BEUQ`):**
  A pesar de todo lo anterior, SQLMap solía ser lento porque tiene una técnica letal llamada *Time-Based Blind SQLi* (Técnica T). Esta técnica se dedica a inyectarle comandos al servidor diciendo "Si entiendes este comando, quédate congelado por 5 segundos". El gran problema es que testear matemáticas obliga al orquestador a esperar físicamente esos tiempos muertos una y otra vez. Al pasarle `BEUQ`, le indicamos que es libre de usar Lógica Booleana, Errores, Unión y Queries, pero le prohíbe terminantemente usar tiempo. Esto aniquila el retraso residual.
* **Optimizaciones Generales Inter-Servidor (`-o`):**
  Activa de golpe todos los interruptores de aceleración interna de red: habilitando soporte de conexiones persistentes (*Keep-Alive*), evitando descargar gráficas o cuerpos HTML muy pesados si la petición solo busca evaluar los headers de error (*Null connection*), y agilizando las respuestas ciegas.
