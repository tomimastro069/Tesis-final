---
trigger: always_on
---

# Regla 9: Tipado Estricto y Manejo de Errores en API y Frontend

Para asegurar la robustez, mantenibilidad y legibilidad del código desarrollado en conjunto con tu equipo, se deben seguir prácticas sólidas de tipado.

## Directivas Técnicas:
1. **Backend (Python / FastAPI):**
   - Todos los endpoints de la API en `api.py` o `main.py` deben usar esquemas estrictos de **Pydantic** para validar los payloads de entrada y las respuestas (`response_model`).
   - Declarar tipos explícitos para todas las funciones auxiliares, retornos y parámetros.
   - Utilizar el framework de excepciones de FastAPI (`HTTPException`) y manejadores globales de errores para garantizar respuestas de error consistentes (evitando caídas del servidor sin formato estructurado).
2. **Frontend (Vite / React / TypeScript):**
   - Evitar estrictamente el uso del tipo `any`. Todo dato proveniente de la API debe estar fuertemente tipado mediante `interfaces` o `types` definidos en `services/api.ts` o componentes del frontend.
   - Usar TypeScript de forma estricta para props de componentes y hooks personalizados.
