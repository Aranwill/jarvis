---
title: Malāk Live / Replay Visual Projection V0 — G0 File Coverage Ledger
status: gate_pass
authority: evidence_only
document_role: admission_coverage_ledger
language: es
created: 2026-09-23
source_baseline: 0424cfeca7ca16fa59649b9bdfbe45f739030c25
unit_id: MALAK-LIVE-REPLAY-VISUAL-PROJECTION-V0
gate: G0
runtime_delta: 0
authority_effect: none
---

# Malāk Live / Replay Visual Projection V0 — G0 Coverage Ledger

## 1. Resultado

```text
repository                    Aranwill/jarvis
branch                        main
baseline                      0424cfeca7ca16fa59649b9bdfbe45f739030c25
recursive Git tree            complete
tree truncated                false
tracked blobs discovered      292
tracked blobs classified      292
silently omitted              0
runtime delta                 0
authority delta               0

G0 RESULT                     PASS
blocking findings             0
```

Este ledger admite únicamente el diseño de una proyección visual read-only de la
traza interna ya integrada. No autoriza ejecución real del Self-Review ni
implementación.

## 2. Inventario recursivo por familia

El árbol Git exacto del baseline fue inventariado recursivamente.

```text
.github/**                     2
root files                     8
configs/**                     1
docs/architecture/**          14
docs/development/**            5
docs/governance/**             2
docs/knowledge/**             10
docs/operations/**             1
docs/project/concepts/**       7
docs/project/sprints/**       71
docs/project/status/**        11
docs/project/** other          4
documents/**                  10
evaluations/**                 1
examples/**                    1
scripts/**                     9
src/malak/**                  78
src/** other                   1
tests/**                      56
--------------------------------
total                         292
```

Cada familia recibe una disposición explícita en este ledger. No se usaron
búsquedas textuales como sustituto del inventario.

## 3. FULL_READ — fuentes directamente materiales

```text
AGENTS.md
SECURITY.md
docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
docs/architecture/blueprint.md
docs/architecture/architecture_quality_gates.md
docs/development/malak_construction_protocol.md
docs/development/development_checklist.md
docs/project/implementation_roadmap.md
docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md
documents/projects/jarvis/ideas.md

docs/project/sprints/proposals/MALAK-E5-ENGINEERING-CLI-G0-G1-DESIGN.md
docs/project/sprints/proposals/MALAK-E5-G0-COVERAGE-LEDGER.md
docs/project/sprints/proposals/MALAK-INTERNAL-INTERACTION-TRACE-V0-G0-G1-DESIGN.md

src/malak/app/cli.py
src/malak/app/composition.py
src/malak/app/internal_interaction.py
src/malak/observability/execution_trace.py
src/malak/observability/operational_event.py
src/malak/observability/operational_event_sink.py

tests/test_cli.py
tests/test_internal_interaction_v0.py
tests/test_execution_trace_v0.py
tests/test_app_composition.py
```

Razón: son la fuente de autoridad, método, interfaz, trace runtime y pruebas
directamente afectadas por la futura proyección.

## 4. TARGETED_READ — fuentes relacionadas

```text
docs/architecture/adr/**
docs/architecture/kernel.md
docs/architecture/documentation_architecture.md
docs/development/engineering_method.md
docs/development/evidence_manifest.md
docs/project/concepts/**
docs/project/status/**
documents/projects/jarvis/**
pyproject.toml
.github/workflows/validation.yml
```

Razón: pueden imponer límites de autoridad, evidencia, dependencias, delivery o
presentación, pero no son dueños directos de la proyección visual.

## 5. STRUCTURAL_INSPECTION — resto del baseline

```text
.github/** restante
configs/**
docs/knowledge/**
docs/operations/**
docs/project/sprints/** no directamente aplicables
evaluations/**
examples/**
scripts/**
src/malak/** restante
src/** restante
tests/** restante
root technical/history files
```

Razón: verificar que no exista una segunda TUI, renderer, dashboard, event bus,
trace viewer o dependencia ya implementada que deba reutilizarse.

## 6. PROTECTED

```text
SECURITY.md
```

Leído por exigencia de admission review. No se modifica.

## 7. Hallazgos G0

### FCL-VIS-001 — fuente runtime de verdad ya existe

```text
status: OBSERVED
blocking: no
```

El baseline ya contiene:

```text
ExecutionTraceEvent
ExecutionTrace
event_sink live
trace.jsonl
read_execution_trace_jsonl
project_component_path
InternalInteractionRunner
```

Por tanto la visualización no necesita crear un segundo sistema de eventos ni
una segunda fuente de estado.

### FCL-VIS-002 — falta proyección visual humana

```text
status: OBSERVED
blocking: no
```

La traza puede reconstruirse y compararse LIVE/REPLAY, pero no existe todavía
un árbol legible que represente fases, componentes, estado, razón y referencias.

### FCL-VIS-003 — la CLI vigente es suficiente como primera superficie

```text
status: OBSERVED
blocking: no
```

La CLI actual es dependency-free, determinista y ya representa el borde humano
de Malāk. No existe necesidad demostrada de abrir una segunda aplicación para V0.

### FCL-VIS-004 — no existe framework TUI integrado

```text
status: OBSERVED
blocking: no
```

`pyproject.toml` mantiene:

```text
dependencies = []
```

No existe adopción material de Textual, Rich, Typer, Click o prompt_toolkit que
deba reutilizarse.

### FCL-VIS-005 — E5-D Rich TUI continúa diferido

```text
status: OBSERVED
blocking: no
```

El diseño E5 preserva:

```text
E5-D Rich TUI
panes / overlays / split views / shortcuts / multi-window
DEFERRED
```

La necesidad actual es menor: visualizar el recorrido real del primer test.
Promover toda E5-D sería scope expansion.

### FCL-VIS-006 — intención histórica reutilizable, stack externo rechazado

```text
status: OBSERVED
blocking: no
```

`ideas.md` preserva:

```text
Terminal/TUI as Operational Surface, Not Core Dependency
```

y el Research Horizon Map preserva `EXT-22` como input de propiedades mientras
rechaza copiar arquitectura CLI/TUI, defaults o authority model externos.

Disposición:

```text
operational visual surface      ADOPT
presence / flow projection      ADAPT
external TUI architecture       REJECT
external authority model        REJECT
full multi-window TUI now       OBSERVE / DEFER
```

### FCL-VIS-007 — visualización no debe transformarse en autoridad

```text
status: OBSERVED
blocking: no
```

La futura proyección sólo puede representar trace existente.

```text
visual state != runtime authority
rendered PASS != validation PASS
UI label != evidence
projection != decision
```

## 8. Security Horizon Check

| Línea | Resultado V0 |
| --- | --- |
| Prompt & Context Trust Boundary | ALREADY_COVERED — el renderer no consume texto libre para decidir flujo. |
| Identity & Delegation | NOT_APPLICABLE — no hay agents/tools/delegación. |
| Compromise Containment | NOT_APPLICABLE — no hay ejecución externa nueva. |
| Memory / Knowledge Poisoning | NOT_APPLICABLE — no se promueve conocimiento. |
| AI Supply-Chain Trust | ALREADY_COVERED — cero dependencia externa nueva propuesta. |
| Data Classification / Disclosure | REQUIRES_REINFORCEMENT — la vista debe mostrar metadata/referencias permitidas, no volcar outputs arbitrarios por defecto. |
| Resource Governance | ALREADY_COVERED — sin workers, polling loops o concurrencia. |
| Observabilidad / Human in Control | REQUIRES_REINFORCEMENT — la UI debe reflejar eventos reales y distinguir NOT_OBSERVED de estados ejecutados. |

No se detecta `BLOCKING_GAP`.

## 9. G0 disposition

```text
need demonstrated                  YES
existing source of truth           YES
duplicate event system required    NO
new dependency required            NO
full Rich TUI required             NO
Kernel delta required              NO
Planner delta required             NO
authority delta required           NO
visual projection gap              YES

G0 RESULT                          PASS
```

Siguiente paso permitido: G1 design únicamente.
