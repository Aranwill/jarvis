---
title: Malāk E5 — G0 File Coverage Ledger
status: gate_pass
authority: evidencia operativa de admisión
as_of_date: 2026-09-19
unit_id: MALAK-E5
gate: G0
source_baseline: 5b6660eba9e5617a59c17d7380dd6822e8c193a4
vault_baseline: c1d61e264113ec396760b39dc5e027252eefe2f7
language: es
---

# Malāk E5 — G0 File Coverage Ledger

## Resultado

```text
G0 RESULT: PASS
blocking findings: 0
tracked files discovered: 258
tracked files classified: 258
silently omitted files: 0
implementation code touched: 0
```

El inventario exhaustivo obligatorio para la admisión de E5 cubre el repositorio
oficial `Aranwill/jarvis` en el baseline exacto:

```text
5b6660eba9e5617a59c17d7380dd6822e8c193a4
```

El árbol Git recursivo utilizado declaró `truncated: false`. Ningún blob
trackeado quedó fuera del inventario por no coincidir con una búsqueda textual.

El Project Vault fue utilizado únicamente como contexto downstream reconciliado.
La proyección vigente observada corresponde a Vault
`c1d61e264113ec396760b39dc5e027252eefe2f7`, integrado mediante PR #126.

---

## Inventario por familia

```text
.github/**                         2
arquitectura                     14
desarrollo                        5
gobernanza                        2
conceptos                         6
project state                     6
sprints / proposals              60
ideas / históricos               10
src/malak/**                     73
tests/**                         50
otros                            30
-----------------------------------
tracked blobs                   258
classified blobs                258
silently omitted                  0
```

Cada blob queda cubierto por una disposición explícita o por un catch-all de
familia. La profundidad de lectura es proporcional a autoridad, riesgo y
relevancia para la Terminal Adaptativa.

No se detectó en este baseline el archivo expresamente rechazado
`PROJECT - MANIFIESTO MALAK (1).docx`. Si apareciera en un baseline futuro,
deberá clasificarse `REJECTED_DO_NOT_READ` y no abrirse.

---

## Disposiciones utilizadas

```text
FULL_READ
TARGETED_READ
STRUCTURAL_INSPECTION
HISTORICAL_REFERENCE
GENERATED_OR_DERIVED
NOT_APPLICABLE_WITH_REASON
PROTECTED
```

---

# Malāk — source of truth

## FULL_READ

```text
AGENTS.md
SECURITY.md
docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
docs/architecture/blueprint.md
docs/architecture/architecture_quality_gates.md
docs/development/engineering_method.md
docs/development/malak_construction_protocol.md
docs/project/implementation_roadmap.md
docs/project/project_context.md
docs/project/concepts/README.md
docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md
docs/project/sprints/proposals/MALAK-E2-ENGINEERING-INSPECT-G0-G1-DESIGN.md
docs/project/sprints/proposals/MALAK-E3-ENGINEERING-ANALYZE-G0-G1-DESIGN.md
docs/project/sprints/proposals/MALAK-E4-ENGINEERING-PROPOSE-G0-G1-DESIGN.md
src/malak/app/cli.py
src/malak/app/composition.py
src/malak/kernel/kernel.py
src/malak/kernel/registry.py
src/malak/kernel/bootstrap.py
src/malak/services/planner.py
src/malak/infrastructure/repository_reader.py
src/malak/knowledge/knowledge_reader.py
src/malak/capabilities/engineering_inspect.py
src/malak/capabilities/engineering_analyze.py
src/malak/capabilities/engineering_propose.py
tests/test_cli.py
tests/test_app_composition.py
tests/test_kernel.py
tests/test_planner.py
tests/test_engineering_inspect.py
tests/test_engineering_analyze.py
tests/test_engineering_propose.py
```

Razón: fuentes de ley, seguridad, método, baseline vigente y código/tests que
forman o delimitan directamente la superficie E5.

## TARGETED_READ

```text
docs/architecture/kernel.md
docs/architecture/adr/**
docs/architecture/decisions/**
documents/projects/jarvis/ideas.md
docs/project/concepts/GOVERNED_SWARM_LONG_HORIZON_REFERENCE.md
docs/project/concepts/GOVERNED_EPHEMERAL_AGENT_EXECUTION_EVIDENCE_REFERENCE.md
docs/project/concepts/MALAK_EVIDENCE_BOUND_COGNITION_FOUNDATION.md
docs/knowledge/**
pyproject.toml
.github/**
```

Razón: contratos, antecedentes y referencias que pueden restringir routing,
autoridad, observabilidad, lifecycle futuro o dependencias.

La búsqueda dirigida en `ideas.md` no produjo una iniciativa de CLI/terminal
que deba promoverse automáticamente. La intención material relevante se encuentra
en el baseline actual, en E0–E4 y en la referencia externa preservada `EXT-22`
del Research Horizon Map.

## STRUCTURAL_INSPECTION

```text
src/malak/** restante
tests/** restante
configs/**
examples/**
scripts/**
root files técnicos
```

Razón: verificar que E5 no duplique responsabilidades, no introduzca una segunda
ruta cognitiva, no dependa de un framework TUI existente y no active una
superficie operacional no observada.

## HISTORICAL_REFERENCE

```text
docs/project/sprints/** no activos
documents/projects/jarvis/** históricos no aplicables
snapshots / registros históricos cuando correspondan
```

Razón: trazabilidad y detección de intención previa sin sustituir el baseline.

## GENERATED_OR_DERIVED

```text
docs/project/implementation_roadmap.md
docs/project/project_context.md
```

Estos documentos fueron además leídos en profundidad por contener el estado
CURRENT reconciliado. Su clasificación derivada no aumenta su autoridad.

## PROTECTED

```text
SECURITY.md
```

La política fue leída por exigencia de admission review. E5-A no la modifica.

---

# Findings de cobertura

## FCL-E5-01 — No existe una Terminal Engineering integrada

```text
status: OBSERVED
blocking: no
```

El baseline contiene una CLI conversacional funcional y E2/E3/E4 integrados,
pero no una superficie humana que exponga esas capabilities desde la CLI.

## FCL-E5-02 — El Planner vigente es deliberadamente mínimo

```text
status: OBSERVED
blocking: no
```

`Planner` resuelve un único `capability_name` configurado. E5 no necesita
convertirlo en router universal ni introducir intent classification.

## FCL-E5-03 — La composición actual está limitada a Conversation

```text
status: OBSERVED
blocking: no
```

`build_conversation_kernel(...)` registra únicamente
`ConversationCapability`. La futura E5-A debe ampliar composición en el borde
de aplicación sin cambiar Kernel, Planner o contratos core.

## FCL-E5-04 — No existe dependencia TUI que deba reutilizarse

```text
status: OBSERVED
blocking: no
```

No se encontró adopción material de Typer, Click, prompt_toolkit o Textual para
la CLI vigente. Introducir una dependencia TUI en E5-A no está justificado.

## FCL-E5-05 — EXT-22 es input de propiedades, no arquitectura

```text
status: OBSERVED
blocking: no
```

El Research Horizon Map preserva `gentle-pi` como
`IMPLEMENTATION_INPUT + WATCH_SIGNAL` para propiedades como lifecycle tipado,
concurrencia acotada y projection de presencia, y prohíbe inferir de ello la
adopción de su CLI/TUI, defaults o modelo de autoridad.

---

# Security Horizon Check

| Línea | Resultado E5-A |
| --- | --- |
| Prompt & Context Trust Boundary | ALREADY_COVERED — E5-A no cambia los límites E2–E4 ni convierte output en instrucciones. |
| Identity & Delegation | NOT_APPLICABLE — no hay agentes, tools ni delegación. |
| Compromise Containment | NOT_APPLICABLE — no se introduce ejecución externa. |
| Memory / Knowledge Poisoning | ALREADY_COVERED — E5-A reutiliza E1/E2/E3/E4 sin persistencia nueva. |
| AI Supply-Chain Trust | ALREADY_COVERED — cero dependencia externa nueva en E5-A. |
| Data Classification / Disclosure | NOT_APPLICABLE — no se agrega persistencia, exportación ni egress. |
| Resource Governance | ALREADY_COVERED — E5-A no añade concurrencia, workers ni loops. |
| Observabilidad / Human in Control | REQUIRES_REINFORCEMENT — comandos Engineering deben conservar correlación y no adquirir autoridad. |

No existe `BLOCKING_GAP` para diseñar E5-A.

---

# Cierre G0

```text
tracked files discovered = 258
tracked files classified = 258
silently omitted files   = 0

baseline drift blocking admission = none observed
new external dependency required  = no
Kernel modification required      = no
Planner modification required     = no
E2/E3/E4 behavior change required = no

G0 RESULT = PASS
```

Este PASS permite diseñar E5-A. No autoriza RED, GREEN, merge ni ninguna fase
posterior de la Terminal Adaptativa.
