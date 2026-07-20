---
title: Hoja de ruta de implementación
status: borrador
authority: no normativa
as_of_date: 2026-07-20
as_of_commit: d1425600eb2914b3c5571ebdabcbdd8de66661da0
branch: main
language: es
---

# Hoja de ruta de implementación

## Clasificación y autoridad

Este documento es derivado, informativo y no normativo.

Organiza propuestas preliminares de implementación, pero:

- no aprueba arquitectura;
- no autoriza cambios;
- no reemplaza las fuentes normativas;
- no establece automáticamente el próximo sprint;
- no convierte una recomendación en una obligación.

Ante cualquier conflicto prevalecen, en este orden:

1. Constitución Cognitiva;
2. Constitución de Gobernanza;
3. Blueprint;
4. especificaciones aprobadas;
5. ADR aceptados;
6. contratos públicos vigentes;
7. documentación operativa aprobada.

## Regla de admisión de sprints

La existencia, numeración, posición, título o ficha de un sprint no constituye autorización para implementarlo.

Cada propuesta debe someterse, como mínimo, a:

1. inspección completa del baseline vigente;
2. revisión del código, pruebas y documentación aplicables;
3. identificación de una necesidad real y comprobada de Malāk;
4. justificación de su utilidad cognitiva, arquitectónica, operativa o de gobernanza;
5. definición explícita del alcance y fuera de alcance;
6. evaluación de riesgos, dependencias, impacto y rollback;
7. validación mediante las cuatro preguntas obligatorias;
8. presentación y debate del plan de ejecución;
9. aprobación explícita e inequívoca del propietario.

Sin esa aprobación no se debe crear una rama, modificar archivos ni iniciar una implementación.

La aprobación de un sprint anterior no autoriza automáticamente el siguiente.

El propietario puede aprobar, redefinir, diferir, reemplazar o descartar cualquier propuesta.

## Estado de referencia

- Rama permanente: `main`.
- Commit de referencia: `d1425600eb2914b3c5571ebdabcbdd8de66661da0`.
- Baseline nominal: `v0.6.0-alpha`.
- Suite validada: 69 pruebas aprobadas.
- `compileall` validado sin errores.
- `git diff --check` validado sin errores.
- Sprint 7.2 cerrado: `Runtime Metric Sink Contract`.
- El Kernel permanece desacoplado de runtimes, proveedores y modelos concretos.
- La CLI y el pipeline Kernel–Planner–Capability continúan siendo rutas separadas.
- No existe todavía una integración formal validada entre `Kernel.receive` y `ConversationService`.
- `main` es la única rama permanente del repositorio.

## Sprints cerrados del bloque 7.x

| Sprint | Estado | Resultado |
|---|---|---|
| 7.0 | Cerrado | CLI mínima con `MockLLMRuntime` |
| 7.1 | Cerrado | Composición de CLI con `OllamaRuntime` mediante configuración externa |
| 7.2 | Cerrado | Contrato estructural `RuntimeMetricSink` de solo escritura |

## Propuestas pendientes de revisión y aprobación

| Propuesta | Estado | Observación |
|---|---|---|
| Sprint 7.3 | No aprobado | Requiere redefinición completa; no se asumirá una segunda Capability sin necesidad funcional real |
| Consolidación de logs, métricas y auditoría | No aprobada | Debe justificarse contra la infraestructura actual y los contratos existentes |
| Security Control Plane Foundation | No aprobada | Debe diseñarse y aprobarse antes de capacidades externas o de alto riesgo |
| Preparación del AKS para GraphRAG | No aprobada | No implica implementar GraphRAG |
| Validación de baseline y release interna | No aprobada | Solo corresponde después de cerrar y sincronizar los bloques previos |

La tabla anterior no establece secuencia obligatoria.

El próximo sprint debe seleccionarse únicamente después de una revisión completa del baseline y de la necesidad real de Malāk.

## Regla de admisión de Capabilities

Una Capability solo podrá incorporarse cuando añada una funcionalidad real, necesaria y permanente para Malāk.

No se deben crear Capabilities con el único propósito de:

- validar routing;
- demostrar que el Planner selecciona múltiples entradas;
- comprobar que el Registry admite varias Capabilities;
- aumentar cobertura artificialmente;
- ejercitar infraestructura interna;
- completar una secuencia prevista;
- incorporar ejemplos sin utilidad funcional.

La infraestructura interna debe validarse mediante pruebas, dobles, fixtures, contratos e integración controlada.

## Restricción estructural

Antes de introducir agentes, herramientas externas, automatización del sistema operativo, navegación, mensajería externa, memoria sensible o Capabilities de alto riesgo, deben aprobarse e implementarse los fundamentos de seguridad y gobernanza correspondientes.

Ninguna propuesta futura puede:

- ampliar el Kernel con lógica de negocio;
- acoplar el Kernel a un runtime, proveedor, modelo o infraestructura concreta;
- introducir dependencias no aprobadas;
- modificar contratos centrales sin revisión específica;
- asumir que el hardware actual define la arquitectura permanente de Malāk.

## Fichas relacionadas

- `docs/project/sprints/SPRINT-7.0.md`
- `docs/project/sprints/SPRINT-7.1.md`
- `docs/project/sprints/SPRINT-7.2.md`
- `docs/project/sprints/SPRINT-7.3.md`
- `docs/project/sprints/SPRINT-7.4.md`
- `docs/project/sprints/SPRINT-7.5.md`
- `docs/project/sprints/SPRINT-7.6.md`
- `docs/project/sprints/SPRINT-7.7.md`

Las fichas pendientes son propuestas y no constituyen autorización de implementación.

## Regla de actualización

Este documento debe revalidarse cuando ocurra cualquiera de estos eventos:

- cambio material de `HEAD`;
- cierre de un sprint;
- modificación de contratos públicos;
- aceptación de un ADR relacionado;
- cambio de rama permanente;
- certificación de un nuevo baseline;
- cambio material de las reglas de gobernanza o ejecución.

Los snapshots históricos y releases certificadas no deben reescribirse para coincidir con este documento.
