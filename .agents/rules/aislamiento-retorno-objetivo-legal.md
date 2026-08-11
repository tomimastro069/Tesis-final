---
trigger: always_on
---

# Regla 3: Aislamiento y Entorno Objetivo (Consideraciones Legales y Éticas)

El proyecto se enmarca dentro de una tesis de seguridad ofensiva, por lo cual se deben respetar rigurosamente los límites de alcance y las consideraciones éticas documentadas en el Capítulo 16 de la tesis.

## Restricciones de Alcance:
1. **Objetivo Predefinido:** El objetivo de escaneo del orquestador está estrictamente limitado al entorno de laboratorio autorizado. La URL por defecto y objetivo principal SIEMPRE será `http://dvwa`.
2. **Prohibición de Escaneo Externo:** Antigravity (y cualquier otro agente) tiene ESTRICTAMENTE PROHIBIDO sugerir, escribir o habilitar código que permita al sistema realizar ataques masivos, escaneos de vulnerabilidades o fuzzing hacia dominios arbitrarios de internet, redes públicas o sistemas en producción.
3. **Bloqueo del Frontend:** El campo de URL objetivo en el panel de control del frontend debe permanecer deshabilitado y fijado en `http://dvwa`. La funcionalidad multi-dominio es una capacidad arquitectónica que no se debe habilitar por defecto.
