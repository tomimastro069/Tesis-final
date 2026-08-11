---
trigger: always_on
---

# Regla 4: Estética y Componentes del Frontend

El frontend del orquestador posee una identidad visual muy específica que debe respetarse de manera estricta durante el desarrollo y modificación de componentes.

## Convenciones de Diseño:
1. **Identidad Retro / Glassmorphism:** El proyecto posee una estética dual consciente: un panel de control con estética moderna (Glassmorphism) y una interfaz retro que recrea el escritorio de Windows 98. Se debe respetar el estilo seleccionado para cada componente sin mezclar conceptos contradictorios.
2. **Terminal MS-DOS:** La visualización del progreso del análisis se hace mediante una terminal simulada estilo "MS-DOS Prompt". La IA NO debe sugerir componentes de progreso genéricos (barras de progreso convencionales o modales genéricos) que reemplacen o eliminen esta experiencia de la terminal.
3. **Consistencia Visual:** Al proponer componentes nuevos de React o modificar los existentes, se deben utilizar las clases y estructuras de CSS ya definidas en el proyecto. No reescribir la interfaz con TailwindCSS u otros frameworks de utilidad si esto rompe la coherencia con el diseño temático definido por los autores de la tesis.
