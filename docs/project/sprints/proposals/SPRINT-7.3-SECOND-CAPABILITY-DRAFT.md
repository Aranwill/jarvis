---
title: Sprint 7.3 — Segunda Capability controlada
status: borrador preliminar
authority: no normativa
as_of_commit: 71d13fc0ee431b9574fcfb5dbc52baf8cb6e4c4c
language: es
---

# Sprint 7.3 — Segunda Capability controlada

## Autoridad y dependencia

Documento derivado y no normativo. No autoriza implementación. La Capability concreta y el criterio de selección requieren aprobación previa.

## Objetivo preliminar

Validar que el Planner y el Capability Registry seleccionen entre más de una Capability sin ampliar innecesariamente el Kernel.

## Alternativas preliminares

- `HelpCapability`.
- `StatusCapability`.

La selección deberá basarse en alcance mínimo, comportamiento determinista y ausencia de acciones externas.

## Alcance preliminar

- Definir la responsabilidad única de la Capability elegida.
- Usar el contrato público existente.
- Incorporarla al registro mediante la composición aprobada.
- Añadir reglas deterministas de selección al Planner fuera del Kernel cuando corresponda.
- Probar selección correcta, fallback y Capability inexistente.

## Fuera de alcance

- Herramientas externas, agentes, navegación o automatización.
- Lógica de negocio dentro del Kernel.
- Selección mediante LLM.
- Escritura persistente o acceso a información sensible.

## Criterios preliminares de aceptación

- La nueva funcionalidad pertenece a una Capability aislada.
- El Kernel conserva sus responsabilidades actuales.
- La selección es determinista y está cubierta por pruebas.
- No existen dependencias circulares ni acoplamiento a runtimes concretos.
- Suite completa en verde y documentación sincronizada.

## Riesgo

Riesgo: bajo a medio, concentrado en el crecimiento del Planner y en una posible duplicación de responsabilidades.
