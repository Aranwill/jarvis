---
title: Hoja de ruta de implementación 7.x
status: borrador
authority: no normativa
as_of_date: 2026-07-14
as_of_commit: 71d13fc0ee431b9574fcfb5dbc52baf8cb6e4c4c
language: es
---

# Hoja de ruta de implementación 7.x

## Clasificación y autoridad

Este documento es derivado, informativo y no normativo. Ordena el contexto de planificación aportado por el propietario del proyecto, pero no aprueba arquitectura, no autoriza implementaciones y no reemplaza las fuentes normativas de Malāk.

Ante cualquier conflicto prevalecen, en este orden, la Constitución Cognitiva, la Constitución de Gobernanza, el Blueprint, las especificaciones aprobadas, los ADR aceptados y los contratos públicos vigentes.

Cada sprint requiere alcance aprobado, rama dedicada, validación completa, Pull Request y punto de rollback. La existencia de una ficha de sprint no constituye autorización para ejecutarlo.

## Estado de referencia

- Rama inspeccionada: `refactor/rename-malak`.
- Commit de referencia: `71d13fc0ee431b9574fcfb5dbc52baf8cb6e4c4c`.
- Baseline nominal: `v0.6.0-alpha`.
- Suite conocida: 51 pruebas aprobadas.
- El flujo del Kernel y el stack conversacional existen como rutas separadas.
- No hay una integración formal validada entre `Kernel.receive` y `ConversationService`.

## Secuencia prevista

| Sprint | Objetivo preliminar | Dependencia o puerta de entrada |
|---|---|---|
| 7.0 | CLI mínima con `MockLLMRuntime` | Decisión de diseño sobre la ruta de integración |
| 7.1 | CLI con `OllamaRuntime` | Sprint 7.0 cerrado y ruta de composición aprobada |
| 7.2 | Calibración real del runtime | Métricas reales obtenidas mediante 7.1 |
| 7.3 | Segunda Capability controlada | Criterio de selección definido sin ampliar el Kernel |
| 7.4 | Consolidación de logs, métricas y auditoría | Contratos de eventos y política de datos definidos |
| 7.5 | Base del plano de control de seguridad | Diseño y gobernanza aprobados; no usar LLM para autorizar |
| 7.6 | Preparación del AKS para GraphRAG | Taxonomía y metadatos aprobados; sin implementar GraphRAG |
| 7.7 | Validación de baseline y release interna | Sprints anteriores aceptados y documentación sincronizada |

## Restricción estructural

El Sprint 7.5 debe completarse antes de introducir agentes, herramientas externas, automatización del sistema operativo, navegación, mensajería externa, memoria sensible o Capabilities de alto riesgo.

## Fuera de alcance de esta hoja de ruta

- Aprobar la arquitectura de cualquiera de los sprints.
- Modificar el Kernel o contratos centrales.
- Adelantar trabajo de un sprint posterior.
- Certificar releases.
- Reescribir roadmaps o snapshots históricos.
- Autorizar commits, push, merge o Pull Requests.

## Fichas relacionadas

- `docs/project/sprints/SPRINT-7.0.md`
- `docs/project/sprints/SPRINT-7.1.md`
- `docs/project/sprints/SPRINT-7.2.md`
- `docs/project/sprints/SPRINT-7.3.md`
- `docs/project/sprints/SPRINT-7.4.md`
- `docs/project/sprints/SPRINT-7.5.md`
- `docs/project/sprints/SPRINT-7.6.md`
- `docs/project/sprints/SPRINT-7.7.md`

## Regla de actualización

Revalidar este documento cuando cambie materialmente HEAD, se acepte un ADR relacionado, se cierre un sprint, se modifiquen contratos públicos o se certifique un nuevo baseline.
