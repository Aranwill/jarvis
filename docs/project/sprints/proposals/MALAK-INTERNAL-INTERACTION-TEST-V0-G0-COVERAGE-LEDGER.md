---
title: Malāk Internal Interaction Test V0 — G0 File Coverage Ledger
status: gate_pass
authority: evidence_only
document_role: admission_coverage_ledger
language: es
created: 2026-09-23
source_baseline: 424febae61d6ab6f1f312efdb4bcad03f0cf79fd
unit_id: MALAK-INTERNAL-INTERACTION-TEST-V0
gate: G0
runtime_delta: 0
authority_effect: none
---

# Malāk Internal Interaction Test V0 — G0 Coverage Ledger

## 1. Resultado

```text
repository                    Aranwill/jarvis
branch                        main
baseline                      424febae61d6ab6f1f312efdb4bcad03f0cf79fd
recursive Git tree            complete
tree truncated                false
tracked blobs discovered      299
tracked blobs classified      299
silently omitted              0
runtime delta                 0
authority delta               0

G0 RESULT                     PASS
blocking findings             0
```

Este ledger admite únicamente el diseño del harness gobernado para el primer
Internal Interaction Test V0 real. No autoriza todavía su ejecución.

## 2. Inventario recursivo

```text
.github/**          2
root files          8
configs/**          1
docs/**           127
documents/**       10
evaluations/**      1
examples/**         1
scripts/**          9
src/**             81
tests/**           59
---------------------
total              299
```

## 3. FULL_READ — material directo

```text
AGENTS.md
SECURITY.md

docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
docs/architecture/blueprint.md
docs/architecture/architecture_quality_gates.md
docs/development/malak_construction_protocol.md
docs/development/development_checklist.md

docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md
docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md
docs/project/status/MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1-FINAL.md
docs/project/sprints/proposals/MALAK-INTERNAL-INTERACTION-TRACE-V0-G0-G1-DESIGN.md
docs/project/sprints/proposals/MALAK-LIVE-REPLAY-VISUAL-PROJECTION-V0-G0-G1-DESIGN.md

src/malak/app/internal_interaction.py
src/malak/app/trace_view.py
src/malak/app/cli.py
src/malak/app/composition.py
src/malak/infrastructure/repository_reader.py
src/malak/services/self_review_evidence.py

tests/test_internal_interaction_v0.py
tests/test_execution_trace_projection_v0.py
tests/test_trace_view_v0.py
tests/test_cli_trace_v0.py
tests/test_cli.py
```

## 4. TARGETED_READ

```text
src/malak/capabilities/engineering_inspect.py
src/malak/capabilities/engineering_analyze.py
src/malak/capabilities/engineering_propose.py
src/malak/runtime/ollama_runtime.py
src/malak/services/conversation_service.py
src/malak/knowledge/knowledge_reader.py
docs/architecture/adr/**
docs/project/concepts/**
documents/projects/jarvis/**
.github/workflows/validation.yml
pyproject.toml
```

## 5. STRUCTURAL_INSPECTION

El resto del baseline fue inspeccionado para detectar superficies duplicadas,
side effects, agentes, schedulers, event buses o mecanismos de ejecución que
deban reutilizarse antes de crear uno nuevo.

Resultado:

```text
second interaction runner       NOT FOUND
second trace store              NOT FOUND
self-review execution command   NOT FOUND
agent requirement               NOT FOUND
scheduler requirement           NOT FOUND
new dependency requirement      NOT FOUND
```

## 6. Hallazgos G0

### FCL-IIT-001 — la lógica cognitiva del test ya existe

```text
status: OBSERVED
blocking: no
```

El baseline ya contiene:

```text
InternalInteractionRunner
SelfReviewEvidencePacket
Engineering Inspect
Engineering Analyze
Engineering Propose
TerminalDisposition
runtime artifacts
attestation
LIVE event sink
trace replay
visual projection
```

No debe crearse otra orquestación cognitiva.

### FCL-IIT-002 — falta un entrypoint gobernado de ejecución

```text
status: OBSERVED
blocking: no
```

La CLI sólo expone superficies read-only:

```text
/trace help
/trace replay
/trace inspect
```

No existe una ruta de Owner explícita para iniciar el bootstrap self-review V0.

### FCL-IIT-003 — el primer task ya está definido

```text
status: OBSERVED
blocking: no
```

`GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md` define como primer foco:

```text
U01 Core Kernel
U04 Observability
RR-03 Strong SecurityContext Provenance
```

y admite `NO_CHANGE_RECOMMENDED` como resultado correcto.

### FCL-IIT-004 — no se necesita agente

```text
status: OBSERVED
blocking: no
```

La referencia conceptual indica explícitamente que no se exige un agente
autónomo si las capacidades existentes son suficientes.

Disposición:

```text
agents      REJECT for V0
library     REJECT for V0
scheduler   REJECT for V0
existing Engineering kernels  REUSE
```

### FCL-IIT-005 — baseline snapshot ya es commit-bound

```text
status: OBSERVED
blocking: no
```

`GitRepositoryReader` captura `HEAD` y su árbol al inicializarse y lee blobs
por identidad Git. Working tree, index y cambios posteriores quedan fuera de la
vista capturada.

Para el primer test, aun así, debe existir un preflight humano/técnico que evite
confundir un working tree local sucio con el baseline que Malāk realmente vio.

### FCL-IIT-006 — Ollama debe ser runtime real del bootstrap

```text
status: OBSERVED
blocking: no
```

El harness de primera ejecución debe rechazar `MockLLMRuntime`.

El objetivo es comprobar la interacción real de Engineering con el modelo local,
no volver a ejecutar mocks de CI.

### FCL-IIT-007 — evidencia CI debe entrar explícitamente

```text
status: OBSERVED
blocking: no
```

`SelfReviewEvidencePacket` requiere referencias externas explícitas.

El harness no debe consultar GitHub ni inferir CI desde internet. Las referencias
se entregan en el borde Owner/CLI.

### FCL-IIT-008 — visual LIVE y replay ya comparten contrato

```text
status: OBSERVED
blocking: no
```

El test puede conectar `LiveTraceTextView` al `event_sink` existente y
comparar al finalizar contra el replay de `trace.jsonl`.

No hace falta una segunda visualización.

## 7. Security Horizon Check

| Línea | Resultado |
| --- | --- |
| Prompt / Context Trust Boundary | ALREADY_COVERED — Engineering trata evidencia como datos no confiables. |
| Identity / Delegation | NOT_APPLICABLE — no agents/tools delegados. |
| Compromise Containment | ALREADY_COVERED — read-only Engineering y artifact boundary. |
| Memory / Knowledge Poisoning | ALREADY_COVERED — no durable knowledge write. |
| AI Supply Chain | ALREADY_COVERED — runtime local existente; no dependencia nueva. |
| Data Classification | REQUIRES_REINFORCEMENT — live view no debe imprimir prompts/CoT. |
| Resource Governance | REQUIRES_REINFORCEMENT — una sola ejecución, sin loop/scheduler. |
| Human in Control | REQUIRES_REINFORCEMENT — el comando debe ser explícito y terminar en Owner/STOP. |

No se detecta `BLOCKING_GAP`.

## 8. G0 disposition

```text
existing cognitive path            YES
existing evidence path             YES
existing artifact path             YES
existing live/replay path          YES
execution entrypoint               NO
agent required                     NO
new dependency required            NO
Kernel delta required              NO
Planner delta required             NO
authority delta required           NO

G0 RESULT                          PASS
```

Siguiente paso permitido: G1 design únicamente.
