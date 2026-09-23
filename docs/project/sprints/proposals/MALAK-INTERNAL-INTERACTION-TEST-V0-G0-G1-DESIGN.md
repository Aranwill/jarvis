---
title: Malāk Internal Interaction Test V0 — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation_design
language: es
created: 2026-09-23
baseline_commit: 424febae61d6ab6f1f312efdb4bcad03f0cf79fd
g0_result: pass
g0_ledger: docs/project/sprints/proposals/MALAK-INTERNAL-INTERACTION-TEST-V0-G0-COVERAGE-LEDGER.md
risk_class: 3
critical_contract: true
design_authorized_by: owner
design_authorized_at: 2026-09-23
red_authorized: true
red_authorized_by: owner
red_authorized_at: 2026-09-23
implementation_authorized: false
execution_authorized: false
runtime_delta: 0
authority_effect: none
related:
  - docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md
  - docs/project/sprints/proposals/MALAK-INTERNAL-INTERACTION-TRACE-V0-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-LIVE-REPLAY-VISUAL-PROJECTION-V0-G0-G1-DESIGN.md
  - docs/development/malak_construction_protocol.md
---

# Malāk Internal Interaction Test V0 — G0/G1 Design

## 1. Propósito

Diseñar el harness mínimo y gobernado que permita ejecutar por primera vez el
Self-Review Bootstrap real de Malāk con:

```text
current exact Git baseline
+ Ollama local
+ existing Engineering Inspect / Analyze / Propose
+ mandatory Self-Review Evidence Packet
+ LIVE visual projection
+ persisted trace/artifacts
+ REPLAY verification
+ Owner boundary
+ STOP
```

Este gate no autoriza todavía la ejecución real.

## 2. Pregunta de aceptación

> ¿Puede Malāk ejecutar una revisión gobernada y read-only de su propio baseline,
> usando un LLM local, recorrer sus componentes reales, mostrar el recorrido LIVE,
> persistir evidencia y reconstruir después el mismo recorrido por REPLAY, sin
> crear agentes, autoautorizarse ni modificar producción?

## 3. Baseline G0

```text
repository                     Aranwill/jarvis
branch                         main
baseline                       424febae61d6ab6f1f312efdb4bcad03f0cf79fd
tracked blobs discovered       299
tracked blobs classified       299
silently omitted               0
G0                             PASS
blocking findings              0
```

Capacidades ya integradas:

```text
InternalInteractionRunner      YES
SelfReviewEvidencePacket       YES
Engineering Inspect            YES
Engineering Analyze            YES
Engineering Propose            YES
TerminalDisposition            YES
runtime artifact set           YES
attestation                    YES
LIVE event sink                YES
trace JSONL                    YES
REPLAY projection              YES
/trace replay                  YES
/trace inspect                 YES
```

Gap real:

```text
governed execution entrypoint  NO
real first-run preflight       NO
LIVE ↔ REPLAY final assertion  NO
```

## 4. Decisión G1

Se admite un único entrypoint de bootstrap:

```text
/self-review test-v0 <run_id> <validation_ref> [<validation_ref> ...]
```

No se admite un comando genérico:

```text
/self-review run <free-form-task>     REJECT
/interaction run <arbitrary-scope>    REJECT
/agent run                            REJECT
```

Razón: V0 debe ejecutar un task fijo, acotado y ya gobernado. No debe abrir una
superficie arbitraria de autoinspección.

## 5. Task identity V0

Constantes propuestas:

```text
task_id:
  governed-self-review-bootstrap-v0

workflow:
  internal-interaction-test-v0
```

El usuario no puede modificar `task_id` desde CLI.

## 6. Scope freeze V0

El scope debe ser constante de aplicación y no texto libre.

Scope canónico:

```text
Governed self-review bootstrap V0: inspect the current exact baseline for
material gaps in U01 Core Kernel and U04 Observability; reassess RR-03 Strong
SecurityContext Provenance only against current surfaces; distinguish historical
evidence limitations from current defects; no-change is a valid outcome;
authority_effect=none.
```

Propiedades:

- cabe dentro de los límites E2/E3/E4;
- cubre el bootstrap task existente;
- no presupone un defecto;
- no pide implementación;
- no pide investigación externa por defecto;
- no permite alterar scope desde input humano.

## 7. Runtime admission

El test real V0 sólo puede ejecutarse si:

```text
runtime_name == OllamaRuntime
model != null
repository_root configured
engineering kernel set available
external_validation_refs non-empty
run_id safe
artifact target does not already exist
```

`MockLLMRuntime`:

```text
allowed in automated tests
REJECTED for real bootstrap execution
```

## 8. Repository preflight

El harness debe exponer y verificar antes de comenzar:

```text
repository_root
captured baseline_commit
current branch
tracked working-tree cleanliness
artifact destination
runtime
model
validation refs
```

Para V0 real:

```text
current branch == main
tracked working tree == clean
```

No se requiere comparar automáticamente contra `origin/main` ni hacer network
fetch desde Malāk.

La sincronización con GitHub se verifica fuera del runtime antes de autorizar la
ejecución.

### 8.1 Por qué exigir clean tracked tree

`GitRepositoryReader` ya ignora working tree/index y queda ligado a HEAD.

El preflight de limpieza existe para evitar una discrepancia humana:

```text
what user sees locally
!=
what Malāk captured from HEAD
```

Untracked runtime artifacts bajo `runtime/` no cuentan como drift de baseline.

## 9. CI / external evidence

Las referencias de validación entran desde el borde Owner:

```text
/self-review test-v0 run-001 Validation#<N> [Validation#<M> ...]
```

Reglas:

- al menos una ref;
- texto no vacío y sin whitespace periférico;
- no se consulta GitHub desde runtime;
- ref != authority;
- ref != pass claim;
- ref es metadata/evidence externa para el packet.

El Owner debe entregar referencias correspondientes al baseline/candidate que
se pretende revisar.

## 10. Flujo real V0

```text
Owner command
  ↓
preflight
  ↓
exact baseline capture
  ↓
Self-Review Evidence Packet
  ↓
LIVE view attached to event_sink
  ↓
Engineering Inspect
  ↓
Engineering Analyze
  ↓
Engineering Propose only if GAP/PARTIAL
  ↓
TerminalDisposition
  ↓
artifacts + attestation
  ↓
REPLAY load
  ↓
LIVE == REPLAY material assertion
  ↓
summary to Owner
  ↓
STOP
```

## 11. Visual behavior

Durante el run se reutiliza:

`LiveTraceTextView`.

Cada evento válido actualiza la misma proyección ya integrada.

No se agrega:

- segunda UI;
- dashboard;
- TUI multiventana;
- event bus;
- polling loop.

Al finalizar se imprime un replay final derivado de `trace.jsonl`.

## 12. LIVE / REPLAY final assertion

Después de persistir y validar artifacts:

```text
live_projection
==
load_trace_projection(repository_root, run_id)
```

Comparación material mínima:

- run_id;
- baseline;
- task_id;
- node ids;
- statuses;
- timestamps;
- duration_ms;
- reason codes;
- refs;
- last sequence;
- stopped state.

Mismatch:

```text
test disposition: INCONCLUSIVE
claim of successful visual bootstrap: FORBIDDEN
artifacts remain available for diagnosis
authority_effect: none
```

El mismatch no modifica el `TerminalDisposition` ya emitido por Engineering;
es un fallo del test harness/observabilidad, no una reinterpretación cognitiva.

## 13. Result summary V0

Al finalizar, la CLI debe mostrar como mínimo:

```text
run_id
baseline_commit
runtime
model
terminal_disposition
component_path
artifact_dir
live_replay_equivalence
authority_effect
```

No muestra por defecto:

- prompts;
- raw model requests;
- private chain-of-thought;
- secrets;
- full component outputs.

Los outputs operacionales completos permanecen en `assessment.json`.

## 14. Failure semantics

### Preflight failure

```text
no InternalInteractionRunner.run()
no artifact directory created by harness
no LLM call
controlled error
```

### Model/component failure

Se usa la semántica existente:

```text
COMPONENT_FAILED
-> reason_code
-> INCONCLUSIVE where applicable
-> artifacts if runner reaches terminal persistence
```

### LIVE renderer failure

Para el primer test V0:

```text
fail closed for test acceptance
do not claim LIVE success
do not synthesize missing visual state
```

No se concede autoridad por continuar ni por abortar.

### Replay failure

```text
controlled failure
test acceptance = INCONCLUSIVE
runtime result remains evidence-only
```

## 15. Idempotencia operacional

Un `run_id` no puede sobrescribir un run existente.

```text
runtime/internal_interaction/<run_id> exists
-> reject before model execution
```

No existe `--force`.

## 16. Side-effect boundary

Permitido:

```text
read exact Git snapshot
call local Ollama
write runtime/internal_interaction/<run_id>/**
print terminal output
```

Prohibido:

```text
tracked source write
Git add/commit/push
branch creation
PR creation
network research
agent creation
scheduler creation
Library mutation
Memory mutation
self-approval
self-merge
```

## 17. Git cleanliness postcondition

El harness captura tracked status antes y después.

Criterio:

```text
tracked status before == clean
tracked status after  == clean
```

Si aparece tracked drift:

```text
test acceptance = INCONCLUSIVE
STOP
```

Esto no elimina artefactos del run.

## 18. CLI namespace

Se propone:

```text
/self-review help
/self-review test-v0 <run_id> <validation_ref> [<validation_ref> ...]
```

Help debe declarar explícitamente:

```text
read-only baseline review
local Ollama required
no self-modification
Owner retains authority
```

No se expone un scope editable.

## 19. Runtime composition

La CLI ya crea:

```text
runtime
conversation service
engineering kernel set
repository_root
model
```

El harness reutiliza exactamente esos objetos.

No debe reconstruir un segundo EngineeringKernelSet.

Candidate unit posible:

```text
InternalInteractionTestV0Harness
```

Responsabilidad:

- preflight;
- conectar live sink;
- ejecutar runner;
- verificar artifacts;
- replay;
- comparar;
- resumir.

No contiene lógica de Inspect/Analyze/Propose.

## 20. Authority model

En todo momento:

```text
finding != authorization
proposal != authorization
terminal disposition != authorization
NO_CHANGE != approval
HARDENING_PROPOSAL != sprint
RESEARCH_REQUIRED != network permission
test PASS != merge permission
```

El final siempre es:

```text
Owner
-> review artifacts
-> decide next action
```

## 21. Critical Contract Hardening

Se clasifica:

```text
risk_class: 3
critical_contract: true
```

porque abre por primera vez una superficie real de self-review con LLM.

Interpretaciones cerradas:

1. `test-v0` no significa self-improvement.
2. El command owner-triggered no transfiere authority.
3. Ollama produce propuestas/evaluaciones, no decisiones.
4. El task y scope son fijos.
5. External validation refs son evidence metadata.
6. No existe auto-remediation.
7. No existe research web en V0.
8. No existe agent factory.
9. No existe retry loop autónomo.
10. Un resultado NO_CHANGE es éxito válido.
11. Un resultado INCONCLUSIVE es éxito de seguridad, no fallo a ocultar.
12. El test debe poder terminar sin generar propuesta.

Known material ambiguity:

```text
0
```

## 22. Cuatro preguntas de ley

### Blueprint

PASS.

Reutiliza Capability First y mantiene Kernel delta 0.

### Cognitive Constitution

PASS.

Evidencia e incertidumbre son explícitas; no se exige encontrar un gap.

### Governance Constitution

PASS.

Owner inicia el test y conserva toda decisión posterior.

### Kernel complexity

PASS.

```text
Kernel planned delta  0
Planner planned delta 0
```

## 23. Design 4R

### Risk — PASS

Controles principales: task fijo, scope fijo, Ollama-only, clean-tree preflight,
run-id sin overwrite, artifacts confinados, authority none, no side effects de
producción.

### Readability — PASS

```text
CLI
-> Test Harness
-> Existing InternalInteractionRunner
-> Existing Engineering
```

Sin duplicar cognición.

### Reliability — PASS

Baseline exacto, validation refs explícitas, attestation existente y equivalencia
LIVE/REPLAY al final.

### Resilience — PASS

Preflight falla antes de modelo; component failures son visibles; replay mismatch
no se normaliza; tracked drift fuerza INCONCLUSIVE.

## 24. RDD Stage 1 Design Check

```text
baseline identity strategy                 PASS
candidate identity strategy                PASS
evidence provenance                        PASS
Writer/Reviewer/Validator/Authority split  PASS
PASS|FAIL|INCONCLUSIVE discipline          PASS
candidate change invalidates evidence      PASS
bounded correction semantics               PASS
authority_effect                           none
RDD Stage 2                                NOT AUTHORIZED
```

## 25. RED futuro

RED deberá cubrir al menos:

```text
fixed task_id
fixed scope
Mock runtime rejected
missing model rejected
missing repository_root rejected
engineering unavailable rejected
empty validation refs rejected
unsafe run_id rejected
existing artifact run rejected before LLM
non-main branch rejected for V0
dirty tracked working tree rejected before LLM
live sink receives actual events
runner uses existing EngineeringKernelSet
result authority_effect none
artifact set validated
LIVE projection == REPLAY projection
replay mismatch yields test INCONCLUSIVE
tracked tree remains clean
CLI invalid command never falls back to Conversation
no arbitrary scope accepted
no agent created
no network research path
```

RED no está autorizado todavía.

## 26. GREEN futuro

GREEN debe implementar únicamente el harness y wiring CLI necesarios para cerrar
RED.

Prohibido:

```text
Kernel changes
Planner changes
new LLM abstraction
new Engineering composition
agents
Library
scheduler
network research
self-modification
generic self-review task input
```

## 27. Ejecución real futura

La ejecución real será un gate separado incluso después de GREEN.

Secuencia:

```text
G0/G1 merged
-> RED
-> GREEN
-> candidate-bound CI
-> FULL 4R
-> E2E
-> Owner merge
-> local sync + exact-main verification
-> explicit Owner runtime execution authorization
-> first real test
```

El merge del harness:

```text
!= runtime execution authorization
```

## 28. Disposición

```text
G0                                  PASS
G1                                  PASS
Critical Contract Hardening         PASS
Four law questions                  PASS
Design 4R                           PASS
RDD Stage 1 Design Check            PASS
known material ambiguity            0

RED authorization                   GRANTED BY OWNER POST-PR #183
implementation authorization        NOT GRANTED
runtime execution authorization     NOT GRANTED
authority_effect                    none
runtime delta                       0
```

Post-merge admission:

```text
PR #183 merged by Owner
main after merge: bd308d5f6bc221dd2582021de9abe00be3152191
RED candidate: AUTHORIZED
GREEN / implementation: NOT AUTHORIZED
runtime execution: NOT AUTHORIZED
```

Siguiente paso permitido:

```text
RED tests only
-> observe expected candidate-bound failure
-> explicit GREEN authorization separately
```
