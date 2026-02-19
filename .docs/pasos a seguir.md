## **FASE 0 — Preparación mental (10 minutos)**

**Objetivo**: saber *qué estás construyendo*.

✔️ Estás construyendo **un sistema** que:

* recibe una URL

* ejecuta pruebas automáticas de seguridad

* junta resultados

* genera un reporte

Nada más.  
 No es una “app”, no es un “scanner nuevo”, es **una orquestación**.

---

## **FASE 1 — Entorno mínimo (1–2 horas) TOMAS**

### **Paso 1.1 — Levantar el objetivo**

* Levantá **DVWA con Docker**

* Confirmá que:

  * abre en el navegador

  * responde a `/login.php`, `/vulnerabilities/`, etc.

---

### **Paso 1.2 — Levantar ZAP en modo daemon**  **🎯 Si ves JSON → ZAP está funcionando.**

### 

* Iniciá ZAP con API

* Confirmá:

  * responde en `http://localhost:8090`

  * podés pegar en el navegador una URL tipo `/JSON/core/view/version/`

✔️ Si no responde la API, no sigas.

IMPORTANTE HACER,  PARA LEVANTAR DVWA Y ZAP:

CD orquestador-seguridad  
docker compose up \--build \-d

(esto abre el contenedor de docker e instala y abre dependencias)

---

## **FASE 2 — Entender las herramientas por separado (clave) TOMAS**

### **Paso 2.1 — ZAP Spider SOLO**

* Ejecutá **un spider manual** contra DVWA

* Verificá:

  * cuántas URLs descubre

  * qué tipo de endpoints aparecen

🎯 Resultado esperado:  
 Una lista de URLs, nada más.

---

### **Paso 2.2 — ffuf SOLO**

* Ejecutá ffuf contra DVWA

* Usá una wordlist chica

* Observá:

  * códigos HTTP

  * rutas encontradas

  * JSON de salida

🎯 Resultado esperado:  
 Un archivo `ffuf_results.json`.

La función hace esto:

`Intento ejecutar comando`

    `↓`

`¿terminó en 0?`

    `↓`

`Devuelvo resultado estructurado`

    `↓`

`Si timeout → marco timeout`

    `↓`

`Si error raro → marco system_error`

`comando para analizar rutas desde ffuf a dvwa en modelo json`

`Ejecutá:`

`ffuf -u http://dvwa/FUZZ -w wordlist.txt -of json -o resultado.json`

`y luego:`  
`cat resultado.json`

`log mas completo sin zap:`

`docker exec -it security-app /bin/bash`

`python test_ffuf.py desde dentro del contenedor ffuf`

---

⛔ **Si no entendés qué devuelve cada herramienta, no sigas.**

---

## **FASE 3 — Primer flujo AUTOMATIZADO (el verdadero inicio)**

### **Paso 3.1 — Crear workflow mínimo en n8n**

Creá un workflow con:

`Manual Trigger`  
   `↓`  
`Exec Node (ffuf o curl simple)`  
   `↓`  
`Function Node (mostrar salida)`

✔️ Nada de ZAP todavía  
 ✔️ Nada de DB  
 ✔️ Nada de SQLMap

🎯 Objetivo:  
 **Demostrar que n8n puede ejecutar una herramienta externa.**

---

### **Paso 3.2 — Parsear una salida**

* En el Function Node:

  * leé el JSON de ffuf

  * contá resultados

  * mostralos en consola

🎯 Resultado:  
 Un objeto JSON limpio.

---

## **FASE 4 — Integrar ZAP al flujo**

### **Paso 4.1 — ZAP Spider desde n8n**

* Agregá un HTTP Request Node:

  * dispara el spider

  * espera resultado

  * recupera URLs

🎯 Resultado:  
 Una lista de URLs dentro del workflow.

---

### **Paso 4.2 — Usar esa salida**

* Pasá esas URLs a:

  * ffuf

  * o simplemente guardalas

🎯 Resultado:  
 Flujo encadenado.

---

## **FASE 5 — Consolidación básica**

### **Paso 5.1 — Unificar resultados**

* En un Function Node:

  * juntá resultados de ZAP \+ ffuf

  * eliminá duplicados

  * marcá tipo de hallazgo

🎯 Resultado:  
 Una lista única de “hallazgos”.

---

## **FASE 6 — Reporte SIMPLE**

### **Paso 6.1 — Generar reporte básico**

* Texto plano o Markdown

* Incluye:

  * fecha

  * URL objetivo

  * cantidad de hallazgos

  * listado

🎯 Resultado:  
 Un archivo generado automáticamente.

---

## **FASE 7 — (Opcional) Escalar**

Solo si todo lo anterior anda:

* SQLMap solo a URLs con `?`

* Severidad simple

* Guardar en DB

* CI/CD

---

# **QUÉ ENTREGÁS (aunque no esté perfecto)**

✔️ DVWA funcionando  
 ✔️ Workflow n8n funcional  
 ✔️ ZAP \+ ffuf integrados  
 ✔️ Reporte automático  
 ✔️ Capacidad de explicar el flujo

Eso **aprueba**.

---

## **ERRORES A EVITAR (importantes)**

❌ Empezar por SQLMap  
 ❌ Hacer workflows enormes de una  
 ❌ Meter código sin probar afuera  
 ❌ Pensar que “más herramientas \= mejor nota”

# **📁 ESTRUCTURA DEL PROYECTO (PYTHON)**

**Orquestador de pruebas de seguridad**

`security-orchestrator/`

`│`

`├── app/`

`│   ├── __init__.py`

`│   │`

`│   ├── main.py              # Entry point (lo ejecutás)`

`│   │`

`│   ├── config/`

`│   │   ├── __init__.py`

`│   │   └── settings.py      # URLs, puertos, paths, timeouts`

`│   │`

`│   ├── scanners/`

`│   │   ├── __init__.py`

`│   │   ├── zap.py           # Todo lo relacionado a ZAP`

`│   │   └── ffuf.py          # Todo lo relacionado a ffuf`

`│   │`

`│   ├── runners/`

`│   │   ├── __init__.py`

`│   │   └── exec.py          # Ejecutar comandos externos`

`│   │`

`│   ├── parsers/`

`│   │   ├── __init__.py`

`│   │   ├── zap_parser.py    # Parsear resultados ZAP`

`│   │   └── ffuf_parser.py   # Parsear JSON de ffuf`

`│   │`

`│   ├── workflow/`

`│   │   ├── __init__.py`

`│   │   └── pipeline.py      # Orquestación paso a paso`

`│   │`

`│   ├── reports/`

`│   │   ├── __init__.py`

`│   │   └── generator.py     # Generar reporte final`

`│   │`

`│   └── utils/`

`│       ├── __init__.py`

`│       └── time.py`

`│`

`├── output/`

`│   ├── raw/                 # salidas crudas (json, txt)`

`│   └── reports/             # reportes finales`

`│`

`├── wordlists/`

`│   └── small.txt`

`│`

`├── requirements.txt`

`├── README.md`

`└── .gitignore`

---

## **🧠 CÓMO PENSAR ESTA ESTRUCTURA (clave)**

### **🔹 `main.py`**

No hace lógica.  
 Solo llama al **pipeline**.

`main → pipeline → scanners → parsers → report`

---

### **🔹 `scanners/`**

**No parsean nada**  
 Solo:

* llaman a ZAP

* llaman a ffuf

* devuelven output crudo

---

### **🔹 `runners/exec.py`**

Un solo lugar para:

* `subprocess.run`

* manejar stdout / stderr

* timeouts

👉 esto evita repetir código

---

### **🔹 `parsers/`**

Transforman:

* JSON feo

* texto crudo

en:

`[`

  `{`

    `"tool": "ffuf",`

    `"url": "...",`

    `"status": 200`

  `}`

`]`

---

### **🔹 `workflow/pipeline.py`**

**EL CEREBRO**

Ahí decidís:

1. correr ZAP spider

2. obtener URLs

3. correr ffuf

4. juntar resultados

5. mandar a reporte

---

### **🔹 `reports/`**

Nada de magia.

* texto plano

* markdown

* después PDF si querés

---

## **🟢 ORDEN REAL PARA EMPEZAR A PROGRAMAR**

No todo junto. En este orden:

1️⃣ `runners/exec.py`  
 2️⃣ `scanners/ffuf.py`  
 3️⃣ `parsers/ffuf_parser.py`  
 4️⃣ `workflow/pipeline.py` (solo ffuf)  
 5️⃣ recién después ZAP

---

## **🚫 LO QUE NO VA (por ahora)**

* DB

* SQLMap

* UI

* frameworks web

* “scanner propio”

---

## **📌 VEREDICTO**

Esto **sí** corresponde a:  
 ✔️ tu checklist  
 ✔️ tu idea  
 ✔️ desarrollo en Python  
 ✔️ empezar desde cero

PROYECTO: ORQUESTADOR DE SEGURIDAD (FUZZING AUTOMATIZADO) \- REPARTO DE TAREAS

ESTRUCTURA GENERAL DEL PROYECTO

El sistema se basará en una arquitectura modular en Python para asegurar que cada componente sea independiente y fácil de probar\[cite: 517, 563\].

\--------------------------------------------------------------------------------

🛠️ PERFIL 1: EL INGENIERO DE EJECUCIÓN (TOMAS)

Responsabilidad: Asegurar que las herramientas externas funcionen, se ejecuten correctamente y entreguen datos crudos al sistema\[cite: 572, 610\].

Tareas Principales:

\* Infraestructura de Laboratorio: Configurar y levantar DVWA (objetivo) y OWASP ZAP (modo daemon) mediante Docker\[cite: 76, 81, 401, 407, 409\].

\* Módulo runners/exec.py: Crear la función centralizada que utiliza 'subprocess.run' para ejecutar comandos del sistema, manejando stdout, stderr y límites de tiempo (timeouts)\[cite: 534, 576, 579, 581, 610\].

\* Módulo scanners/ffuf.py: Implementar la lógica para armar el comando de ffuf, ejecutarlo a través del runner y devolver el archivo JSON crudo generado\[cite: 530, 573, 575, 611\].

\* Módulo scanners/zap.py: Implementar la comunicación con la API de ZAP para iniciar el Spider y el escaneo, devolviendo los resultados sin procesar\[cite: 528, 573, 614\].

\--------------------------------------------------------------------------------

🧠 PERFIL 2: EL ARQUITECTO DE LÓGICA (CRISTIAN)

Responsabilidad: Diseñar el flujo de trabajo y transformar los datos técnicos crudos en información estructurada y útil para el reporte\[cite: 584, 596\].

Tareas Principales:

\* Módulo parsers/ffuf\_parser.py: Desarrollar el traductor que toma el JSON "feo" de ffuf y lo convierte en una lista de Python estandarizada (objetos con URL, estado y tipo de hallazgo)\[cite: 540, 583, 588, 612\].

\* Módulo parsers/zap\_parser.py: Desarrollar el traductor para los resultados de la API de ZAP, normalizando los datos para que coincidan con el formato de ffuf\[cite: 538, 584\].

\* Módulo workflow/pipeline.py: Programar el "cerebro" del sistema que coordina el orden de ejecución: primero ZAP Spider, luego obtener URLs y finalmente ejecutar ffuf sobre los objetivos detectados\[cite: 544, 595, 596, 613\].

\* Lógica de Consolidación: Implementar la función de unificación que junta los resultados de todas las herramientas, elimina duplicados y organiza los hallazgos\[cite: 40, 473, 475, 477, 601\].

\--------------------------------------------------------------------------------

📝 PERFIL 3: EL ESPECIALISTA EN CONFIGURACIÓN Y ENTREGA (JUAN)

Responsabilidad: Gestionar la configuración global, la generación del reporte final y asegurar que el proyecto sea ejecutable por terceros\[cite: 525, 549\].

Tareas Principales:

\* Módulo config/settings.py: Definir todas las variables constantes, como la URL del objetivo (DVWA), llaves de API, puertos, rutas a diccionarios (wordlists) y timeouts\[cite: 524, 525\].

\* Módulo reports/generator.py: Desarrollar el motor que toma la lista de hallazgos limpia y genera un archivo final en formato Markdown o texto plano con estadísticas y detalles técnicos\[cite: 548, 549, 603, 606\].

\* Punto de Entrada (main.py): Crear el script principal que importa y arranca el pipeline, sirviendo como la interfaz única de ejecución para el usuario o profesor\[cite: 520, 521, 564, 566\].

\* Gestión de Dependencias: Crear el archivo 'requirements.txt' con todas las librerías necesarias (como 'requests') para que el entorno sea reproducible\[cite: 298, 560\].

\--------------------------------------------------------------------------------

📅 PLAN DE INTEGRACIÓN (EL "MERGE")

Para evitar conflictos técnicos al unir las partes, el equipo seguirá este protocolo:

1\. Sincronización de Datos: Se establece que todos los parsers deben devolver una lista de diccionarios con el formato: {"tool": str, "url": str, "status": int}\[cite: 588, 592\].

2\. Verificación de Entregables: El proyecto se considera funcional si entrega DVWA funcionando, el workflow de n8n/Python integrado y el reporte automático generado\[cite: 267, 501, 506\].

3\. Validación Final: Cada integrante debe ser capaz de explicar el flujo completo del sistema, ya que es el criterio principal de evaluación académica\[cite: 273, 507, 113\].

