# 🛡️ Orquestador de Seguridad Automatizado

Bienvenido al Orquestador de Seguridad, una herramienta diseñada para integrar y ejecutar de manera secuencial e inteligente múltiples motores de análisis de vulnerabilidades (OWASP ZAP, SQLMap y FFUF) centralizando los resultados en un único reporte legible y profesional.

## 🚀 Características Principales

- **Pipeline Unificado:** Controla y orquesta la ejecución de diversas herramientas de escaneo desde un único punto de entrada.
- **Soporte de Autenticación:** Capacidad para inyectar cookies de sesión y escanear áreas protegidas (Behind Login).
- **Procesamiento Inteligente:** Toma los hallazgos de una herramienta (Ej: URLs descubiertas por el Spider de ZAP) y alimenta otra (Ej: SQLMap) para realizar comprobaciones profundas y destructivas.
- **Generación de Reportes:** Parsea los resultados y genera automáticamente `reporte_seguridad.md` incluyendo todos los hallazgos conjuntos.
- **Dockerizado:** Entorno limpio, replicable y fácil de levantar con Docker Compose (incluye el target local DVWA).

## 🛠️ Requisitos e Instalación

### Opción A: Despliegue con Docker Compose (Recomendado)

El proyecto cuenta con un entorno Docker listo para usar que levanta la instancia de DVWA (aplicación web intencionalmente vulnerable), ZAP controlable por API, n8n con aprovisionamiento autónomo, y el entorno de nuestro orquestador con todas las herramientas preinstaladas (SQLMap, FFUF, Python).

1. **Configurar las Variables de Entorno (Requerido para la IA):**
   Antes de levantar los contenedores por primera vez, debes crear el archivo `.env` en la carpeta `orquestador-seguridad/` copiando la plantilla `.env.example` y configurando tu clave de API de Gemini (generada en Google AI Studio):
   
   ```bash
   cp .env.example .env
   ```
   
   Abre el archivo `.env` y define tu clave de API:
   ```env
   IA_API_KEY=tu_api_key_de_gemini
   ```

2. **Levantar los servicios:**
   Ejecuta el siguiente comando para iniciar todo el stack. En el primer arranque, n8n importará y activará automáticamente el flujo de análisis con IA y tus credenciales:

   ```bash
   docker compose up -d
   ```

   > [!NOTE]
   > **¿Qué pasa si levantaste los contenedores antes de configurar el `.env`?**
   > Si iniciaste los servicios sin configurar la API key y n8n ya se inicializó, puedes borrar el marcador de inicio y forzar una reconfiguración ejecutando:
   > ```bash
   > rm -f ../n8n/data/init_done && docker compose down && docker compose up -d
   > ```

2. **Acceder al contenedor de la aplicación:**

   ```bash
   docker exec -it security-app bash
   ```

3. **Ejecutar el pipeline:**

   ```bash
   python main.py
   ```

### Opción B: Entorno Local / Manual

Si prefieres no usar el contenedor de la app, asegúrate de contar con:

- Python 3.11 o superior.
- OWASP ZAP ejecutándose como daemon (o GUI) en el puerto local.
- Herramientas instaladas globalmente en tu PATH: SQLMap y FFUF.

**Instalación de dependencias:**

```bash
pip install -r requirements.txt
```

## 💻 Uso General

Puedes lanzar el orquestador llamando al script principal. El flujo de ejecución es interactivo y solicitará las configuraciones clave.

```bash
python main.py
```

**Flujo de la tubería de escaneo:**

| Fase | Herramienta | Acción |
| ---- | ----------- | ------ |
| 1 | ZAP Spider | Analiza el terreno e indexa las URI activas. |
| 2 | ZAP Active Scan | Busca vulnerabilidades expuestas activamente. |
| 3 | FFUF | Fuerza bruta para hallar directorios ocultos u olvidados. |
| 4 | SQLMap | Inyecciones destructivas a los parámetros e inputs encontrados. |
| 5 | Reporte | Generación del informe consolidado en `/output/reports`. |

---

## 📖 Paso a Paso (Caso Práctico: DVWA)

### 1. Obtención de una Sesión Genuina (Cookies)

1. Abre el navegador y navega a la URL (Ej: `http://dvwa/login.php`).
2. Inicia sesión con credenciales válidas (por defecto `admin` / `password`).
3. Presiona **F12** para abrir las Herramientas de Desarrollador.
4. Dirígete a la pestaña **Application** (o Almacenamiento) > **Cookies**.
5. Localiza la cookie `PHPSESSID` y `security=low`. Copia la estructura:
   - **Ejemplo:** `PHPSESSID=b41dbfcc529ea4; security=low`

### 2. Ejecutar el orquestador

Dirígete a tu terminal y ejecuta:

```bash
python main.py
```

### 3. Configuración de la sesión

Durante la ejecución, el script solicitará los parámetros:

- **Nivel de escaneo**: Presiona Enter (default: `medium`).
- **Cookie de sesión**: Pega la cadena obtenida en el paso 1.

```text
Nivel de escaneo (small/medium) [default: medium]: medium
Cookie de sesion (opcional) [default: none]: PHPSESSID=b41dbfcc529ea4; security=low
```

### 4. Analizar los Resultados Finales

Al finalizar, abre el archivo: `output/reports/reporte_seguridad.md`.

> [!TIP]
> **Explosión del Spider (Nuevas Rutas)**
> ZAP ya no se detendrá ante el `302 Redirect`. Ahora navegará por rutas ocultas como `/vulnerabilities/brute/` o `/vulnerabilities/sqli/`.

> [!WARNING]
> **SQLMap Destructivo**
> El filtro capturará los Endpoints que son verdaderos inputs interactivos. SQLMap se tomará su tiempo (flag `--level=2`) para registrar hallazgos reales.

> [!NOTE]
> **FFUF Extendido**
> Al pasar el `StatusCode 200`, FFUF identificará exitosamente los repositorios protegidos que antes eran inaccesibles.

> [!INFO]
> **Nota Operativa:** Para reiniciar manualmente DVWA, > > > acceda a `http://localhost:8080/setup.php` y haga clic en "Create / Reset Database".
