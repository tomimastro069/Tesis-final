# Orquestador de Seguridad Automatizado

Bienvenido al **Orquestador de Seguridad**, una herramienta diseñada para integrar y ejecutar de manera secuencial e inteligente múltiples motores de análisis de vulnerabilidades (OWASP ZAP, SQLMap y FFUF) centralizando los resultados en un único reporte legible.

## 🚀 Características Principales

- **Pipeline Unificado**: Controla y orquesta la ejecución de diversas herramientas de escaneo desde un único punto.
- **Soporte de Autenticación**: Capacidad para inyectar cookies de sesión y escanear áreas protegidas (Behind Login).
- **Procesamiento Inteligente**: Toma los hallazgos de una herramienta (Ej: URLs descubiertas por el Spider de ZAP) y alimenta otra (Ej: SQLMap) para realizar comprobaciones profundas y destructivas.
- **Generación de Reportes**: Parsea los resultados y genera automáticamente `reporte_seguridad.md` incluyendo todos los hallazgos conjuntos.
- **Dockerizado**: Entorno limpio, replicable y fácil de levantar con Docker Compose (incluye el target local DVWA).

---

## 🛠️ Requisitos e Instalación

### Opción A: Despliegue con Docker Compose (Recomendado)

El proyecto cuenta con un entorno Docker listo para usar que levanta la instancia de DVWA (aplicación web intencionalmente vulnerable), ZAP controlable por API, y el entorno de nuestro orquestador con todas las herramientas preinstaladas (SQLMap, FFUF, Python).

1. **Clonar y levantar servicios:**

   ```bash
   docker-compose up -d
   ```

2. **Acceder al contenedor de la aplicación:**

   ```bash
   docker exec -it security-app bash
   ```

3. **Ejecutar el pipeline:**

   ```bash
   python main.py
   ```

### Opción B: Entorno Local / Manual

Si prefieres no usar el contenedor de la app, deberás asegurarte de tener en tu sistema:

1. Python 3.11 o superior.
2. [OWASP ZAP](https://www.zaproxy.org/download/) ejecutándose como daemon (o GUI) en el puerto local.
3. Herramientas instaladas globalmente en tu path: [SQLMap](https://sqlmap.org/) y [FFUF](https://github.com/ffuf/ffuf).
4. **Instalar las dependencias de Python**:

   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Uso General

Puedes lanzar el orquestador llamando al script principal. El flujo de ejecución es interactivo y te pedirá configuraciones clave de escaneo.

```bash
python main.py
```

Flujo de la tubería de escaneo:

1. **ZAP Spider**: Analiza el terreno e indexa las URI activas.
2. **ZAP Active Scan**: Busca vulnerabilidades expuestas activamente.
3. **FFUF**: Fuerza bruta y escaneo en búsqueda de directorios ocultos u olvidados.
4. **SQLMap**: Realiza inyecciones destructivas a los parámetros e inputs interactivos encontrados.
5. **Generador de Reportes**: Genera el informe consolidado final dentro del directorio `/output/reports`.

---

# PASO A PASO (para dvwa)

## 1. Obtención de una Sesión Genuina (Cookies)

1. Abre tu navegador web y navega hacia la URL (Ej: `http://dvwa/login.php`).
2. Inicia sesión normalmente usando las credenciales válidas (para DVWA por defecto suele ser `admin` / `password`).
3. Una vez logueado exitosamente, presiona **F12** para abrir las **Herramientas de Desarrollador**.
4. Dirígete a la pestaña **Application** (o **Almacenamiento**).
5. En la barra lateral, expande la categoría **Cookies** y selecciona el dominio al que estás conectado.
6. Localiza la cookie identificativa general de sesión, por ejemplo la que suele llamarse `PHPSESSID`, y fíjate también si hay otras cookies activas como `security=low`. Copia el texto o armalo tú mismo siguiendo la estructura: `clave1=valor1; clave2=valor2`.
   - **Ejemplo resultante:** `PHPSESSID=b41dbfcc529ea4; security=medium`

## 2. Ejecutar el orquestador

Dirígete a tu terminal

```bash
python main.py
```

## 3. Pasar la sesión al sistema

Durante la ejecución interactiva, el script ahora nos hará una nueva pregunta donde volcaremos nuestra cadena mágica.

1. **Nivel de escaneo**: Presiona enter (usará 'medium' como predeterminado).
2. **Cookie de sesión**: Pega la estructura que armaste en el paso 1.

```text
Nivel de escaneo (small/medium) [default: medium]: medium
Cookie de sesion (opcional, ej. PHPSESSID=123..; security=low) [default: none]: PHPSESSID=b41dbfcc529ea4; security=low
```

## 4. Analizar los Resultados Finales

Cuando las 4 fases de escaneos (Spider, ZAP Active, SQLMap, FFUF) terminen su ejecución, deberás abrir tu archivo generado: `output/reports/reporte_seguridad.md`.

> [!TIP]
> **Explosión del Spider (Nuevas Rutas)**
> ZAP ya no se tropezará iterativamente con el `302 Redirect` enviándolo de regreso a `/login.php`. Ahora el escáner navegara por las páginas ocultas como `/vulnerabilities/brute/`, `/vulnerabilities/exec/`, `/vulnerabilities/sqli/`, etc. Podrás verificar docenas de URL nuevas en la sección final de "Mapa del Sitio (Spider)".

> [!WARNING]

> **SQLMap Destructivo**
> El filtro de `sqlmap.py` que se queda únicamente con las URLs que contienen parámetros GET (`?`) va a capturar finalmente todos esos Endpoints de la base del Spider que son **verdaderos inputs interactivos** (Ej: `http://dvwa/vulnerabilities/sqli/?id=1&Submit=Submit`). Ahora SQLMap se tomará su tiempo (recuerda que el flag `--level=2` puede demorar unos minutos) y debería registrar hallazgos reales.

> [!NOTE]
> **FFUF Extendido**
> Durante la recolección, a pesar de usar una _wordlist_ reducida o de mayor nivel, pasará el `StatusCode 200` y podrá identificar exitosamente los repositorios protegidos.

Si encuentras estas alertas de nivel _Medium_ a _High_ o encuentras un abanico extenso de sitios documentados, entonces **la inyección de la cookie ha funcionado a la perfección**.

**Nota Operativa**: Para reiniciar manualmente DVWA hay que entrar a: `http://localhost:8080/setup.php`, hacer click en **Create / Reset Database** y volver al formulario de login.
