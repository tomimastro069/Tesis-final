# Guía de Uso y Configuración de n8n

Esta carpeta contiene la configuración del workflow (flujo de trabajo) en n8n encargado de procesar y enriquecer las vulnerabilidades utilizando Inteligencia Artificial.

> [!IMPORTANT]
> **Aprovisionamiento Autónomo:**
> La inicialización de n8n, la importación del flujo de trabajo (`flujo.json`), la configuración de las credenciales de la API y su activación se realizan de forma **100% automática** al iniciar los servicios (`docker compose up -d`). Solo necesitas crear el archivo `.env` en la carpeta del orquestador con tu clave `IA_API_KEY`.
>
> Las instrucciones de esta guía sirven como referencia si deseas modificar, depurar o volver a exportar el flujo manualmente.

---

## 🛠️ Cómo Iniciar y Configurar n8n

### 1. Iniciar el contenedor
n8n está integrado en el entorno de Docker Compose del proyecto. Si los contenedores ya están corriendo, n8n ya estará activo. 

Si necesitas iniciarlo desde cero, navega a la carpeta del orquestador y ejecuta:
```bash
docker compose up -d
```
El contenedor se levantará con el nombre `security-n8n`.

### 2. Acceder a la interfaz web
Abre tu navegador web e ingresa a:
* **URL:** [http://localhost:5678](http://localhost:5678)

*(Nota: Si es la primera vez que entras, n8n te pedirá crear una cuenta de usuario administrador local).*

### 3. Importar el Flujo de Trabajo (Workflow)
Existen dos formas muy sencillas de importar el archivo `flujo.json` en n8n:

#### Método A: Arrastrar y Soltar o Importar (Recomendado)
1. En n8n, ve a la sección **Workflows** y haz clic en **Add Workflow** (o abre uno nuevo vacío).
2. Haz clic en el botón de los tres puntos `...` en la esquina superior derecha.
3. Selecciona **Import from File**.
4. Sube el archivo [flujo.json](file:///home/cristian/repos_utn/Tesis-final/n8n/flujo.json).

#### Método B: Copiar y Pegar Directo
1. Abre el archivo [flujo.json](file:///home/cristian/repos_utn/Tesis-final/n8n/flujo.json) en tu editor y copia todo su contenido de texto (`Ctrl + A` y luego `Ctrl + C`).
2. Ve al lienzo/canvas de tu nuevo workflow en n8n.
3. Haz clic en cualquier parte vacía del lienzo y presiona **`Ctrl + V`** (Pegar). Los nodos se importarán y organizarán automáticamente de forma mágica.

### 4. Configurar las Credenciales de Groq
El flujo utiliza el modelo **Llama 3.3 70B** a través de **Groq**. Para configurar tus credenciales:
1. Regístrate u obtén tu API Key desde la consola oficial de Groq: [https://console.groq.com/keys](https://console.groq.com/keys).
2. En n8n, haz doble clic en el nodo **Groq Chat Model**.
3. En la sección **Credential para Groq API**, selecciona **Create New Credential** (o edita la existente).
4. Pega tu API Key de Groq y guarda los cambios.

### 5. Activar y Probar el Workflow
* **Para pruebas temporales:** Haz clic en el botón **Listen for test event** (Escuchar evento de prueba) en el nodo Webhook o en **Execute Workflow** en la barra inferior para capturar la petición entrante del orquestador.
* **Para producción:** Activa el interruptor **Active** (en la esquina superior derecha) para que el flujo quede permanentemente en escucha de los análisis lanzados desde la aplicación.

---

## 📤 Cómo Exportar tu Flujo desde n8n a JSON

Si haces modificaciones en el lienzo de n8n y quieres guardarlas en este repositorio para actualizar el archivo `flujo.json`, puedes exportarlo de dos formas:

### Método 1: Exportar desde el menú (Formato de archivo completo)
1. Con tu flujo abierto en n8n, haz clic en el botón de los tres puntos `...` en la parte superior derecha.
2. Selecciona **Export**.
3. Elige la opción **To File**. 
4. Guarda el archivo descargado reemplazando el contenido de [flujo.json](file:///home/cristian/repos_utn/Tesis-final/n8n/flujo.json).

### Método 2: Copiar nodos al portapapeles (Rápido)
1. Dentro del lienzo de n8n, presiona **`Ctrl + A`** para seleccionar todos los nodos del flujo.
2. Presiona **`Ctrl + C`** para copiarlos.
3. Ve a tu editor de código, abre el archivo [flujo.json](file:///home/cristian/repos_utn/Tesis-final/n8n/flujo.json), selecciona todo y pégalo. n8n almacena automáticamente la estructura JSON completa en tu portapapeles al copiar los nodos.
