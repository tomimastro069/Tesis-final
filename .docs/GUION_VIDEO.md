# 🎬 Guion para Video de Progreso — Orquestador de Seguridad

> **Presentación:** Orquestador de Seguridad — Fuzzing Automatizado de Aplicaciones Web  
> **Duración total estimada:** ~3 minutos (180 segundos)  
> **Destinatario:** Video de progreso para el profesor

---

## 🖼️ Diapositiva 1 — Portada

**⏱️ Duración: 8 segundos**

> _"Bienvenidos. Este video muestra el progreso de nuestro proyecto final: un orquestador de seguridad para fuzzing automatizado de aplicaciones web, desarrollado por Cristian Krahulik, Tomas Mastropietro y Juan Segura."_

---

## 🖼️ Diapositiva 2 — ¿Qué es este proyecto?

**⏱️ Duración: 15 segundos**

> _"El proyecto recibe una URL objetivo y ejecuta múltiples pruebas de seguridad sobre ella de forma completamente automática. No inventamos herramientas nuevas: orquestamos herramientas existentes mediante un pipeline en Python que coordina todo el flujo y genera un reporte unificado al final."_

---

## 🖼️ Diapositiva 3 — ¿Qué es el Fuzzing?

**⏱️ Duración: 15 segundos**

> _"El fuzzing consiste en enviar datos inesperados a una aplicación para descubrir fallos ocultos. Nosotros utilizamos tres tipos: fuzzing de directorios para encontrar rutas escondidas, fuzzing de parámetros para probar entradas inusuales, y escaneo activo para detectar vulnerabilidades del OWASP Top 10."_

---

## 🖼️ Diapositiva 4 — Herramientas utilizadas

**⏱️ Duración: 15 segundos**

> _"Las herramientas principales son: OWASP ZAP para el escaneo y descubrimiento de vulnerabilidades, ffuf para el fuzzing de directorios, Docker para correr todo el entorno de forma aislada, DVWA como aplicación vulnerable de prueba, y Python como el lenguaje del orquestador."_

---

## 🖼️ Diapositiva 5 — Arquitectura del Sistema

**⏱️ Duración: 15 segundos**

> _"El sistema corre en tres contenedores Docker que se comunican entre sí: el contenedor de DVWA como objetivo, el contenedor de OWASP ZAP exponiendo su API REST, y el contenedor Python que actúa como orquestador. Todo corre en una red interna aislada."_

---

## 🖼️ Diapositiva 6 — Estructura Modular

**⏱️ Duración: 18 segundos**

> _"El código está dividido en módulos con responsabilidad única. Los Runners ejecutan comandos del sistema con manejo de errores y timeouts. Los Scanners interactúan con ZAP y ffuf para obtener los datos crudos. Los Parsers los transforman en un formato estandarizado. El Pipeline coordina el orden de todo. Y los Utils manejan funciones auxiliares como la consolidación."_

---

## 🖼️ Diapositiva 7 — El Pipeline: Flujo de Ejecución

**⏱️ Duración: 18 segundos**

> _"El pipeline ejecuta cuatro pasos en orden. Primero, ZAP Spider mapea todas las URLs de la aplicación. Segundo, ZAP Active Scan analiza cada URL buscando inyecciones SQL, XSS, CSRF y más. Tercero, ffuf hace fuzzing de directorios para encontrar rutas que el spider no detectó. Cuarto, se consolidan todos los resultados crudos en un paquete unificado."_

---

## 🖼️ Diapositiva 8 — Fase de Parseo

**⏱️ Duración: 18 segundos**

> _"Con los datos crudos listos, entra en acción el pipeline de parseo. El Parser de Spider extrae y deduplica las URLs. El Parser de ZAP aplana las alertas de seguridad eliminando duplicados y extrayendo severidad y solución recomendada. El Parser de ffuf filtra las rutas por código HTTP. Al final, los tres resultados se consolidan en una sola estructura de datos."_

---

## 🖼️ Diapositiva 9 — Resultado Final

**⏱️ Duración: 15 segundos**

> _"El output final es un archivo JSON unificado que incluye: un resumen con totales, la sección de Spider con todas las URLs mapeadas, la sección de ZAP con las vulnerabilidades y su severidad, y la sección de ffuf con las rutas descubiertas. Un solo archivo, listo para análisis."_

---

## 🖼️ Diapositiva 10 — Cómo se ejecuta

**⏱️ Duración: 15 segundos**

> _"La ejecución es simple: con un solo comando de Docker Compose se levanta todo el entorno. Luego se corre el script Python principal. Desde ese momento, el pipeline se encarga solo: spider, escaneo, fuzzing, parseo y consolidación. El usuario solo necesita indicar la URL objetivo."_

---

## 🖼️ Diapositiva 11 — Trabajo en Equipo

**⏱️ Duración: 15 segundos**

> _"El trabajo se dividió por perfiles: Tomas se encargó de la infraestructura Docker, los Runners y los Scanners. Cristian desarrolló los Parsers, el Pipeline y la lógica de consolidación. Juan gestionó la configuración global, el generador de reportes y el punto de entrada del sistema."_

---

## 🖼️ Diapositiva 12 — Conclusiones y Próximos Pasos

**⏱️ Duración: 13 segundos**

> _"Logramos un pipeline funcional de extremo a extremo, con arquitectura modular y entorno completamente dockerizado. Como próximos pasos, planeamos integrar SQLMap para detección de inyecciones SQL, generar reportes en PDF, y agregar clasificación de severidad CVSS."_

---

## 📊 Resumen de tiempos

| Diapositiva | Título               | Segundos          |
| ----------- | -------------------- | ----------------- |
| 1           | Portada              | 8s                |
| 2           | ¿Qué es el proyecto? | 15s               |
| 3           | ¿Qué es el Fuzzing?  | 15s               |
| 4           | Herramientas         | 15s               |
| 5           | Arquitectura         | 15s               |
| 6           | Estructura Modular   | 18s               |
| 7           | Pipeline             | 18s               |
| 8           | Parseo               | 18s               |
| 9           | Resultado Final      | 15s               |
| 10          | Cómo se ejecuta      | 15s               |
| 11          | Trabajo en Equipo    | 15s               |
| 12          | Conclusiones         | 13s               |
| **Total**   |                      | **~180s (3 min)** |

---

## 💡 Tips para la grabación

### Herramienta de voz IA

Recomendadas para generar la voz a partir del guion:

- **[ElevenLabs](https://elevenlabs.io)** — Alta calidad, voces muy naturales (tiene plan gratuito limitado).
- **[Murf.ai](https://murf.ai)** — Buena opción con editor integrado de video/audio.
- **[NotebookLM Audio Overview](https://notebooklm.google.com)** — Gratuito de Google, genera audios de explicación muy naturales.

> **Flujo sugerido:** Pegá el texto de cada diapositiva en la herramienta, generá el audio por separado para cada una y exportalos como archivos `.mp3`.

### Grabación de pantalla

- **OBS Studio** — Gratuito, grabación de pantalla nativa en Linux.
- **Grabación nativa de GNOME** — `Ctrl + Shift + Alt + R` para grabaciones rápidas.

### Edición y sincronización

- **[DaVinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve)** — Gratuito y muy potente.
- **[Kdenlive](https://kdenlive.org)** — Editor open source nativo de Linux.

> Importá los audios y la grabación de pantalla, y ajustá la duración de cada diapositiva para que coincida con el audio correspondiente.

### Velocidad de habla

Configurá la velocidad de la voz IA al **100% o ligeramente más rápido** para que encaje bien dentro de los tiempos indicados en el resumen.
