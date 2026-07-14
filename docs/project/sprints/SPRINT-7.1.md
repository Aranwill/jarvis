---
title: Sprint 7.1 — CLI con OllamaRuntime
status: borrador preliminar
authority: no normativa
as_of_commit: 71d13fc0ee431b9574fcfb5dbc52baf8cb6e4c4c
language: es
---

# Sprint 7.1 — CLI con `OllamaRuntime`

## Autoridad y dependencia

Documento derivado y no normativo. No autoriza implementación. Requiere el cierre aprobado del Sprint 7.0 y una ruta de composición arquitectónica validada.

## Objetivo preliminar

Conectar la CLI ya validada con `OllamaRuntime` para realizar conversaciones locales reales sin acoplar el Kernel a Ollama.

## Alcance preliminar

- Seleccionar un modelo local pequeño mediante configuración externa al Kernel.
- Componer el runtime concreto en la frontera de aplicación aprobada.
- Gestionar conexión rechazada, timeout, modelo inexistente, respuesta inválida y cancelación controlada.
- Validar respuestas reales sin registrar prompts o datos sensibles innecesarios.
- Añadir pruebas deterministas para errores; las pruebas con Ollama real deberán estar claramente separadas.

## Fuera de alcance

- Cambiar automáticamente modelos, timeout o TTL.
- Modificar el Kernel o contratos centrales sin autorización específica.
- Añadir proveedores externos, navegación, herramientas o memoria.
- Adelantar la calibración del Sprint 7.2.

## Criterios preliminares de aceptación

- La ausencia de Ollama falla de forma clara y controlada.
- La selección del runtime permanece fuera del Kernel.
- Los tests no dependen obligatoriamente de un servicio local activo.
- La prueba manual real está documentada y es reproducible.
- Suite completa en verde y diff revisado.

## Riesgo y rollback

Riesgo: medio por dependencia ambiental local. El rollback debe retirar únicamente la composición y documentación añadidas en la rama del sprint.
