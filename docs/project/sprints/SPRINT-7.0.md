---
title: Sprint 7.0 — CLI mínima con MockLLMRuntime
status: borrador condicionado
authority: no normativa
as_of_commit: 71d13fc0ee431b9574fcfb5dbc52baf8cb6e4c4c
language: es
---

# Sprint 7.0 — CLI mínima con `MockLLMRuntime`

## Autoridad

Esta ficha es un borrador derivado. No autoriza implementación ni modifica el Blueprint, el Kernel o los contratos centrales.

## Objetivo preliminar

Validar una interacción mínima por terminal con entrada, salida y cierre controlado, utilizando `MockLLMRuntime` y los contratos existentes.

## Puerta arquitectónica obligatoria

Antes de implementar se debe aprobar una decisión de diseño que establezca la ruta entre la Interface Layer, `Kernel.receive` y `ConversationService`.

En el estado inspeccionado existen dos rutas separadas:

```text
Interface Layer → Kernel → Planner → Capability Registry → Capability → Response
ConversationService → Provider Registry → Provider → LLMRuntime
```

La ficha no elige ni presenta como definitiva una conexión entre ambas. Si se aprueba un harness directo sobre `ConversationService`, deberá identificarse como infraestructura limitada de validación y no como el pipeline completo de Malāk.

## Alcance preliminar incluido

- Punto de entrada de consola en la Interface Layer.
- Lectura de texto ingresado por el usuario.
- Salida controlada mediante `exit` o `quit`.
- Tratamiento determinista de entradas vacías.
- Construcción de `ConversationRequest` cuando corresponda a la ruta aprobada.
- Presentación de `ConversationResponse` sin exponer detalles internos innecesarios.
- Composición de `ConversationService`, provider y `MockLLMRuntime` fuera del Kernel.
- Pruebas unitarias del bucle y pruebas de integración proporcionales.
- Documentación de uso y límites.

## Fuera de alcance

- Integrar `OllamaRuntime` o realizar llamadas de red.
- Modificar el Kernel o sus responsabilidades.
- Cambiar contratos centrales sin autorización específica.
- Implementar nuevas Capabilities, memoria, herramientas o agentes.
- Incorporar trabajo de los Sprints 7.1 o posteriores.
- Presentar un harness como arquitectura definitiva.

## Archivos previsiblemente afectados

La lista definitiva depende de la decisión de diseño. Como máximo preliminar:

- `src/app/main.py` o un módulo de Interface Layer explícito.
- Nuevas pruebas bajo `tests/`.
- Documentación operativa de la CLI.

## Restricciones

- Preservar Kernel First, Capability First y Runtime Independence.
- No introducir dependencias directas entre Kernel y runtime/provider concreto.
- Mantener la selección y composición del runtime fuera del Kernel.
- Evitar rutas hardcodeadas y dependencias nuevas.
- Mantener cambios pequeños, reversibles y auditables.

## Estrategia de validación

- Entrada normal produce una respuesta determinista.
- Entrada vacía se gestiona sin invocar trabajo innecesario.
- `exit` y `quit` finalizan sin error.
- Errores controlados no dejan el proceso en estado inconsistente.
- Suite completa: `.\.venv\Scripts\python.exe -m pytest`.
- Revisión de `git diff --check`, diff completo y estado de Git.

## Criterios de aceptación

- La decisión de diseño previa está aprobada y referenciada.
- La CLI respeta la ruta aprobada y sus límites documentados.
- No se modifican áreas protegidas sin autorización expresa.
- Todas las pruebas aplicables están en verde.
- La documentación distingue claramente harness, Interface Layer y pipeline completo.

## Riesgos y rollback

Riesgo: medio, por la frontera arquitectónica no resuelta. El rollback debe limitarse a los archivos creados o modificados por la rama del sprint, sin descartar trabajo ajeno.

## Definición de terminado

Decisión aprobada, alcance implementado sin adelantamientos, validaciones completas, documentación sincronizada, revisión humana, Pull Request y punto de rollback claro.
