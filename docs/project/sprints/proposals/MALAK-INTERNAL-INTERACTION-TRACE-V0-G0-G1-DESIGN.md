---
title: Malāk Internal Interaction Trace V0 — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation_design
language: es
created: 2026-09-23
baseline_commit: 1442463ec397c052e16d21378bfb11c3e0c48662
g0_result: pass
design_authorized_by: owner
design_authorized_at: 2026-09-23
critical_contract: true
risk_class: 3
red_authorized: true
red_authorized_by: owner
red_authorized_at: 2026-09-23
green_authorized: true
green_authorized_by: owner
green_authorized_at: 2026-09-23
implementation_authorized: true
execution_authorized: false
runtime_delta: 0
authority_effect: none
rdd_stage_2_authorized: false
related:
  - docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md
  - docs/development/malak_construction_protocol.md
  - docs/development/evidence_manifest.md
  - docs/project/status/MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1-FINAL.md
  - docs/project/sprints/proposals/MALAK-E2-STRUCTURAL-EVIDENCE-EVALUATION-PACK-V0-G0-G1-DESIGN.md
---

# Malāk Internal Interaction Trace V0 — G0/G1 Design

## 1. Propósito

Definir el mínimo contrato y wiring necesarios para ejecutar el primer test
interno read-only de Malāk de forma:

- observable;
- reconstruible;
- baseline-bound;
- evidence-bound;
- fail-closed;
- sin autoridad de modificación;
- sin agentes dinámicos;
- sin Library externa adicional;
- sin autoaprobación;
- sin autoimplementación.

V0 no pretende medir todavía cuánto “sabe” Malāk. Pretende comprobar que una
tarea pueda recorrer componentes reales de Malāk y que ese recorrido pueda
observarse y reconstruirse con evidencia verificable.

Principio rector:

```text
correct answer without trace
!= successful V0 interaction

successful V0 interaction
= bounded result + reconstructible component flow + evidence provenance
```

## 2. Baseline G0

Baseline exacto observado al admitir este diseño:

```text
repository: Aranwill/jarvis
branch: main
baseline: 1442463ec397c052e16d21378bfb11c3e0c48662
active work branch before admission: none
open PRs before admission: none
permanent branch: main
```

Estado CURRENT relevante ya integrado:

```text
E0 Repository Read                         INTEGRATED
E1 Governed Knowledge Read                 INTEGRATED
E2 Engineering Inspect                     INTEGRATED
E3 Engineering Analyze                     INTEGRATED
E4 Engineering Propose                     INTEGRATED
E5-A Command Surface                       INTEGRATED
E5-B1 Read-only Explorer                   INTEGRATED

Repository Structural Projection V0        INTEGRATED
Repository Structural Lookup V0            INTEGRATED
E2 Structural Evidence Integration V0      INTEGRATED
E2 Structural Evidence Observability V0    INTEGRATED
E2 Structural Evidence Evaluation Pack V0  INTEGRATED / TOOLING

OperationalEvent                           INTEGRATED
InMemoryOperationalEventStore              INTEGRATED
JsonlOperationalEventStore                 INTEGRATED

Governed Self-Review Bootstrap             CONCEPT INTEGRATED
execution                                  NOT AUTHORIZED
```

Último baseline funcional/evaluado previo a la reconciliación documental:

```text
e29d3dc79445506aa9bb4e59a8383524d627db68
Validation #428
1278 passed Ubuntu + Windows
compileall PASS
diff validation PASS
```

G0 conclusion:

```text
new cognitive capability required    NO
new agent required                   NO
new library required                 NO
new database required                NO
Kernel redesign required             NO
Planner redesign required            NO
read-only orchestration gap          YES
execution trace contract gap         YES
runtime run-artifact contract gap    YES
live/replay projection gap           YES

G0 RESULT: PASS
```

## 3. Hechos del wiring actual

La implementación existente no constituye hoy una única pipeline material
`E2 -> E3 -> E4`.

`build_engineering_kernel_set()` crea kernels separados para:

```text
inspect
analyze
propose
```

Cada comando se resuelve mediante su propio Kernel fijo.

Estado real de evidencia:

```text
E2 Inspect
  -> Repository evidence [R#]
  -> Governed Knowledge [K#]
  -> Structural Evidence [S#]

E3 Analyze
  -> Repository evidence [R#]
  -> Governed Knowledge [K#]
  -> no [S#] propagation

E4 Propose
  -> executes grounded analysis internally
  -> Repository evidence [R#]
  -> Governed Knowledge [K#]
  -> no [S#] propagation
```

Regla V0:

```text
visualization must represent actual runtime flow
!= invent E2 -> E3 -> E4 data propagation
```

Structural Evidence permanece limitada a E2. Propagación hacia E3/E4 continúa
DEFERRED y requiere gate separado.

## 4. Gap material

Las capacidades necesarias para la primera autoinspección existen
individualmente, pero falta una unidad capaz de:

1. congelar task/scope/baseline;
2. reunir el packet mínimo exigido por Self-Review;
3. invocar etapas read-only existentes bajo un run común;
4. correlacionar eventos de cada componente;
5. registrar inputs/outputs/evidence refs;
6. obtener un resultado terminal cerrado;
7. materializar un artefacto de ejecución local;
8. proyectar ese artefacto como árbol/grafo vivo;
9. reproducir posteriormente el mismo recorrido;
10. terminar en STOP sin modificar el baseline.

Este gap es de integración/observabilidad, no evidencia de fallo de E0-E5.

## 5. Boundary de reasoning

V0 NO captura ni exige private chain-of-thought, token reasoning ni scratchpad
interno del modelo.

La traza consultable debe contener razonamiento operacional estructurado:

```text
observation
evidence refs
finding/classification
uncertainty
contract/gate result
disposition
rationale bounded to evidence
component transition
```

Regla:

```text
operational rationale != private chain-of-thought
```

El objetivo es permitir preguntas posteriores como:

```text
why did run X end in DEFER?
which evidence supported finding A2?
which components were traversed?
where did uncertainty appear?
which gate stopped the run?
```

sin persistir razonamiento privado del LLM.

## 6. Arquitectura V0 propuesta

No se modifica Kernel ni Planner.

La coordinación se incorpora en application/service boundary como una unidad
read-only que reutiliza kernels/capabilities existentes.

```text
Task
  ↓
Internal Interaction Runner
  ↓
Scope + exact baseline freeze
  ↓
Self-Review Evidence Packet
  ↓
Existing Malāk surfaces
  ├── E0 Repository Read
  ├── E1 Governed Knowledge
  ├── Structural Projection / Lookup
  ├── E2 Inspect
  ├── E3 Analyze when required by fixed V0 workflow
  └── E4 Propose only when admissible
  ↓
Terminal Disposition
  ↓
Run Artifact
  ↓
STOP
```

El Runner:

```text
is orchestration
!= Planner replacement
!= Kernel authority
!= autonomous agent
!= scheduler
!= self-modification engine
```

Las invocaciones Engineering deben seguir atravesando los kernels/capabilities
existentes donde corresponda.

## 7. Self-Review Evidence Packet V0

El collector Engineering actual recupera evidencia por coincidencia con
`subject`. Eso no garantiza por sí solo los inputs mínimos definidos por
`GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md`.

V0 necesita un packet explícito que verifique presencia y provenance de al
menos:

```text
exact current baseline
AGENTS.md
Cognitive Constitution
Governance Constitution
Blueprint
Architecture Quality Gates
SECURITY.md
accepted ADRs applicable to target
Malāk Construction Protocol
Development Checklist
implementation roadmap
ideas.md
MALAK_RESEARCH_HORIZON_MAP.md
relevant concepts
current source code
current tests
current CI/evidence reference
latest applicable audit/reconciliation
```

No se exige insertar todo el contenido crudo en un único prompt.

Para V0, la cobertura mínima se vuelve determinista:

```text
core required exact paths:
  AGENTS.md
  SECURITY.md
  docs/governance/cognitive_constitution.md
  docs/governance/governance_constitution.md
  docs/architecture/blueprint.md
  docs/architecture/architecture_quality_gates.md
  docs/development/malak_construction_protocol.md
  docs/development/development_checklist.md
  docs/project/implementation_roadmap.md
  documents/projects/jarvis/ideas.md
  docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md
  docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md
  docs/project/status/MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1-FINAL.md

ADR coverage:
  catalog ALL tracked docs/architecture/adr/ADR-*.md
  include every ADR whose frontmatter status is exactly accepted
  target-specific selection may narrow prompt evidence later
  catalog coverage itself may not silently omit an accepted ADR

concept coverage:
  catalog docs/project/concepts/**
  required minimum paths above must be present
  relevance selection is recorded separately from catalog coverage

current source/tests:
  catalog tracked src/malak/** and tests/**
  selected evidence may be bounded, catalog coverage must remain explicit

current CI/evidence:
  supplied as explicit external_validation_refs by the caller/Owner boundary
  refs are metadata/evidence only, never authority
  missing required current validation reference -> packet INCONCLUSIVE
```

V0 no intenta inferir desde Git local un resultado de GitHub Actions inexistente
en el snapshot.

El packet debe distinguir:

```text
source catalog
required-source presence
selected evidence
content identity / blob SHA
baseline binding
source class
authority class
truncation / unreadable state
```

Regla fail-closed:

```text
required source missing or unreadable
-> packet INCONCLUSIVE
-> self-review cannot claim complete required input coverage
```

## 8. Run identity

Cada ejecución V0 debe poseer identidad propia.

Campos mínimos:

```text
schema
run_id
task_id
created_at
baseline_commit
workflow_version
runtime_name
model
scope
authority_effect
```

`run_id` identifica la ejecución; no concede autoridad.

`baseline_commit` debe coincidir con el snapshot usado por E0/E1/Structural
Projection y por toda etapa del run.

Regla:

```text
component baseline mismatch
-> FAIL / INCONCLUSIVE according to cause
-> STOP
```

No se permite continuar silenciosamente con evidence de commits distintos.

## 9. Execution Trace Event V0

Los eventos existentes `OperationalEvent` se preservan. No se reinterpretan
como audit, validation ni authority.

V0 podrá extender observabilidad mediante un contrato especializado de trace,
sin convertir telemetría en decisión.

Campos mínimos candidatos:

```text
schema
run_id
sequence
occurred_at
baseline_commit
task_id
phase
component
event_type
input_refs
output_refs
evidence_refs
outcome
reason_code
authority_effect
```

`sequence` debe ser monotónica dentro del run.

Eventos cerrados V0:

```text
RUN_STARTED
SCOPE_FROZEN
EVIDENCE_PACKET_STARTED
EVIDENCE_PACKET_READY
COMPONENT_STARTED
COMPONENT_COMPLETED
COMPONENT_SKIPPED
COMPONENT_FAILED
GATE_EVALUATED
TERMINAL_DISPOSITION
ARTIFACT_FINALIZED
RUN_STOPPED
```

No se agregan payloads arbitrarios de modelo al event stream.

### 9.1 Outcome V0 cerrado

`ExecutionTraceEvent.outcome` utiliza únicamente:

```text
STARTED
SUCCEEDED
FAILED
INCONCLUSIVE
SKIPPED
```

Reglas:

```text
COMPONENT_SKIPPED -> outcome = SKIPPED
FAILED            -> reason_code required
INCONCLUSIVE      -> reason_code required
SKIPPED           -> reason_code required
STARTED/SUCCEEDED -> reason_code absent
```

Reason codes V0 permitidos:

```text
validation_failed
baseline_mismatch
required_evidence_missing
unknown_reference
component_error
dependency_unavailable
trace_write_failed
artifact_validation_failed
not_required_by_workflow
precondition_not_met
unresolved_contradiction
policy_stop
```

No se aceptan reason codes desconocidos ni mensajes de excepción crudos.

### 9.2 Ciclo de referencias del trace

Los IDs de `input_refs`, `output_refs` y `evidence_refs` son referencias
opacas run-local; no son authority ni punteros a objetos mutables.

Para cada run existe un catálogo de referencias conocido por el trace:

```text
input_refs / evidence_refs
-> MUST already exist in run reference catalog

output_refs
-> declare new refs after successful event append
-> MUST NOT duplicate an existing ref
-> MUST NOT self-reference through input/evidence in the same event
```

Un ref desconocido, duplicado o perteneciente a otro run:

```text
-> event rejected
-> trace remains unchanged
```

Esto permite reconstruir flujo de información sin persistir payload cognitivo
arbitrario dentro del event stream.

## 10. Component observation contract

Cada componente observado debe poder responder, cuando aplique:

```text
component_id
status
started_at
completed_at
duration
input_refs
output_refs
evidence_consumed
evidence_produced
baseline_commit
outcome
reason_code
authority_effect
```

Estados visuales V0:

```text
WAITING
RUNNING
COMPLETED
SKIPPED_WITH_REASON
FAILED
INCONCLUSIVE
```

`SKIPPED_WITH_REASON` no equivale a PASS.

## 11. Terminal disposition V0

El resultado global del Self-Review debe usar únicamente:

```text
NO_CHANGE_RECOMMENDED
HARDENING_PROPOSAL
RESEARCH_REQUIRED
DEFER
INCONCLUSIVE
```

Mapping inicial:

```text
complete grounded review + no material gap
-> NO_CHANGE_RECOMMENDED

grounded actionable GAP/PARTIAL + valid bounded proposal
-> HARDENING_PROPOSAL

material uncertainty that requires additional external/curated knowledge
-> RESEARCH_REQUIRED

known dependency or scope deliberately postponed
-> DEFER

missing required evidence / contradiction unresolved / invalid run state
-> INCONCLUSIVE
```

No se introduce `APPROVED`, `AUTHORIZED`, `READY`, `MERGED` ni equivalente.

## 12. Artifacts y ruta local

V0 propone como raíz runtime local:

```text
runtime/internal_interaction/<run_id>/
```

`/runtime/` ya está fuera de Git mediante `.gitignore`.

Artefactos candidatos:

```text
manifest.json
trace.jsonl
evidence.json
assessment.json
outcome.json
attestation.json
```

Semántica:

```text
manifest.json
-> identidad y scope del run

trace.jsonl
-> secuencia de eventos reconstruible

evidence.json
-> source catalog + evidencia seleccionada + provenance

assessment.json
-> findings, incertidumbres y rationale operacional estructurado

outcome.json
-> disposición terminal cerrada

attestation.json
-> digests del artifact set + baseline binding
```

Attestation V0 usa SHA-256 sobre los bytes exactos de:

```text
manifest.json
trace.jsonl
evidence.json
assessment.json
outcome.json
```

`attestation.json` no se auto-incluye en su propio digest set.

La lista de archivos atestados debe ser exacta y ordenada canónicamente. Cualquier
archivo faltante, extra dentro del set declarado o digest distinto:

```text
-> artifact validation FAIL
-> run cannot close successfully
```

El contrato `MALAK-EVIDENCE-MANIFEST/v1` NO se reutiliza como runtime manifest.
Ese schema pertenece a RDD Stage 1 / candidate construction evidence.

Puede reutilizarse su disciplina conceptual:

```text
exact identity
closed schema
evidence binding
fail-closed validation
authority_effect = none
```

pero no su semántica ni schema.

## 13. Persistencia V0

La persistencia propuesta es local, filesystem-bound y limitada al directorio
runtime ignorado por Git.

No constituye:

```text
Persistent Memory
Protected Durable Write
knowledge promotion
candidate construction evidence
database
audit authority
```

La escritura sólo materializa el artefacto observacional del run.

No puede modificar:

```text
src/
tests/
docs/
AGENTS.md
SECURITY.md
Git index
Git refs
branches
commits
PRs
```

Una implementación runtime de esta persistencia sigue requiriendo RED/GREEN y
validación antes de autorizar ejecución.

## 14. Live Graph / Replay Projection V0

La visualización debe derivarse exclusivamente del trace.

```text
runtime event
-> trace store
-> projection
-> CLI/TUI graph
```

Nunca:

```text
UI assumption
-> invented component state
```

La misma proyección debe poder operar sobre:

```text
LIVE stream
or
completed trace.jsonl
```

Así un run histórico puede reproducirse visualmente sin reejecutar el LLM.

Vista mínima:

```text
Task
  ↓
Scope
  ↓
Evidence Packet
  ├── E0
  ├── E1
  └── Structural
  ↓
Engineering stage(s)
  ↓
Terminal disposition
  ↓
Artifact
  ↓
STOP
```

Cada nodo debe ser inspeccionable y mostrar sólo metadata/evidence permitida.

## 15. V0 no incluye

Fuera de alcance explícito:

```text
Library expansion
external research automation
Agent Factory
ephemeral agent creation
multi-agent execution
agent delegation
Structural Evidence propagation to E3/E4
Structural Delta
Planner autonomy
dynamic workflow synthesis
tool side effects
Git delivery
self-edit
self-commit
self-PR
self-merge
Persistent Memory
RDD Stage 2
```

Esas superficies sólo podrán abrirse mediante gates posteriores si V0 aporta
evidencia de necesidad.

## 16. First Interaction Test V0

La primera prueba deberá ser deliberadamente resoluble con capacidades locales
actuales.

Objetivo:

```text
prove internal flow
not maximize task difficulty
```

Condiciones:

```text
one exact baseline
one bounded target
Ollama/local LLM allowed
no agents
no external Library expansion
no network research
read-only repository interaction
run artifact enabled
live projection enabled
Owner receives terminal result
STOP before any repository modification
```

Success criteria:

```text
S1 all required run identity fields valid
S2 baseline remains consistent across components
S3 mandatory source packet coverage is explicit
S4 every traversed component emits reconstructible trace
S5 skipped component has explicit reason
S6 evidence refs remain traceable to source identity
S7 terminal disposition belongs to closed enum
S8 authority_effect remains none
S9 repository/Git state is unchanged by the run
S10 completed trace can be replayed into the same component path
```

A correct textual answer does not compensate for S1-S10 failure.

## 17. Failure semantics

V0 debe fallar cerrado frente a:

```text
baseline mismatch
missing required source
invalid event schema
duplicate/non-monotonic sequence
unknown terminal enum
unknown evidence ref
trace write failure when trace is required
artifact digest mismatch
component exception
unexpected side-effect attempt
authority_effect != none
```

La disposición exacta FAIL/INCONCLUSIVE se fijará en RED tests según si el caso
representa incumplimiento determinista o imposibilidad de concluir.

Nunca se normaliza silenciosamente un evento inválido.

## 18. Reutilización vs delta

REUSE:

```text
GitRepositoryReader
GovernedKnowledgeReader
RepositoryStructuralProjector
RepositoryStructuralLookup
EngineeringInspectCapability
EngineeringAnalyzeCapability
EngineeringProposeCapability
Kernel
OperationalEvent concepts
existing event stores where contract-compatible
OllamaRuntime / ConversationService
E5 command boundary
```

NEW candidate units, si RED futuro las demuestra necesarias:

```text
InternalInteractionRun contract
SelfReviewEvidencePacket contract/builder
ExecutionTraceEvent V0
ExecutionTraceStore/projection adapter
InternalInteractionRunner read-only orchestration
terminal disposition mapper
artifact writer/validator
CLI/TUI live + replay projection
```

El número y nombre exacto de módulos de producción no queda autorizado por G1.
GREEN debe elegir el mínimo delta que satisfaga RED.

## 19. Critical Contract Hardening

Interpretaciones materiales cerradas:

1. Trace no es chain-of-thought.
2. Trace no es audit authority.
3. Evidence packet no es knowledge promotion.
4. Artifact persistence no es Persistent Memory.
5. Runner no es agente.
6. Runner no reemplaza Planner.
7. Runner no concede autoridad a capabilities.
8. Visual graph no inventa estados.
9. E2/E3/E4 no se declaran pipeline si runtime no lo demuestra.
10. E3/E4 no reciben [S#] por este gate.
11. Missing evidence no se convierte en GAP.
12. Proposal no se convierte en autorización.
13. Successful run no autoriza self-modification.
14. Owner conserva review/Ready/merge.
15. V0 no requiere Library ni agentes.
16. Existing OperationalEvent telemetry no se eleva silenciosamente a evidence of correctness.
17. Runtime artifact no sustituye MALAK-EVIDENCE-MANIFEST/v1.
18. Failure to persist required trace blocks successful V0 closure.

Bounded correction post-merge PR #179:

```text
BC-TRACE-001
issue:
  SKIPPED_WITH_REASON existed as a visual/component state but the event enum
  had no event capable of recording an explicit skipped component.

correction:
  add COMPONENT_SKIPPED
  close trace outcome enum
  require reason_code for FAILED / INCONCLUSIVE / SKIPPED

BC-TRACE-002
issue:
  unknown-ref rejection was required without defining reference lifecycle.

correction:
  define run-local reference catalog and append semantics.

BC-PACKET-001
issue:
  "accepted ADRs applicable to target", "relevant concepts" and current CI
  evidence could depend on hidden inference.

correction:
  catalog all accepted ADRs, catalog concepts/src/tests explicitly, and receive
  current validation refs as explicit external evidence metadata.

BC-ARTIFACT-001
issue:
  attestation digest semantics did not state whether it hashed itself.

correction:
  SHA-256 exact-byte digest set excludes attestation.json itself.
```

Known material ambiguity unresolved after bounded correction:

```text
0
```

## 20. Cuatro preguntas de ley

### 1. Blueprint

PASS.

El diseño mantiene Kernel First / Capability First y no añade lógica de
self-review al Kernel.

### 2. Cognitive Constitution

PASS.

El recorrido se liga a evidencia, hace incertidumbre visible y permite
NO_CHANGE/INCONCLUSIVE.

### 3. Governance Constitution

PASS.

No existe self-approval ni authority escalation. Owner recibe el resultado.

### 4. Kernel complexity

PASS.

```text
Kernel delta planned: 0
Planner delta planned: 0
```

## 21. Design 4R

### Risk — PASS

Riesgos principales:

- trace laundering hacia authority;
- persistencia reinterpretada como Memory;
- UI inventando estados;
- self-review interpretado como self-modification;
- baseline/evidence drift;
- captura excesiva de contenido del modelo;
- convertir E2/E3/E4 en pipeline por documentación y no por runtime.

Controles: schemas cerrados, baseline binding, authority_effect none,
operational-rationale boundary, read-only artifact path y STOP terminal.

### Readability — PASS

Run, trace, evidence, assessment, outcome y attestation quedan separados por
responsabilidad.

### Reliability — PASS

Identidad exacta, sequence monotónica, evidence refs y replay permiten
reconstrucción determinista del recorrido observable.

### Resilience — PASS

Missing/invalid evidence, fallos de componente y trace incompleto terminan
fail-closed en lugar de producir éxito aparente.

## 22. RDD Stage 1 Design Check

```text
baseline identity strategy                 PASS
future candidate identity strategy         PASS
evidence provenance                        PASS
Writer/Reviewer/Validator/Authority split  PASS
PASS|FAIL|INCONCLUSIVE discipline          PASS
candidate change invalidates evidence      PASS
bounded correction semantics               PASS
authority_effect                           none
RDD Stage 2                                NOT AUTHORIZED
```

El futuro candidate de implementación deberá producir Candidate Conformance
después de GREEN, targeted validation, Candidate FULL 4R, E2E/CI y demás
precondiciones aplicables.

## 23. RED futuro

RED debe demostrar al menos:

```text
invalid/missing run identity rejected
baseline mismatch rejected
required evidence source absence visible
unknown/duplicate trace event rejected
non-monotonic sequence rejected
unknown refs rejected
authority_effect other than none rejected
invalid terminal disposition rejected
trace persistence failure blocks successful close
component failure represented in trace
skipped component requires reason
artifact digests detect tampering
read-only run cannot mutate protected repository surfaces
replay reconstructs observed component sequence
```

No se autoriza aún crear esos tests.

## 24. GREEN futuro

GREEN podrá implementar únicamente el mínimo necesario para satisfacer RED y el
primer Interaction Test V0.

Prohibición explícita:

```text
no opportunistic E3/E4 structural propagation
no agent framework
no generic workflow engine
no database
no message bus
no distributed tracing platform
no web dashboard
no self-modification
```

## 25. E2E futuro

El E2E debe demostrar:

```text
bounded task
-> run identity
-> scope freeze
-> required source packet
-> actual Malāk component traversal
-> local LLM where applicable
-> terminal disposition
-> artifact finalization
-> STOP
```

Y paralelamente:

```text
same runtime events
-> live graph
-> trace.jsonl
-> replay graph
```

La secuencia observada LIVE y REPLAY debe coincidir en identidad de componentes
y orden material.

## 26. Disposición G0/G1

```text
G0                                  PASS
G1                                  PASS
Critical Contract Hardening         PASS
Four law questions                  PASS
Design 4R                           PASS
RDD Stage 1 Design Check            PASS

RED authorization                   GRANTED BY OWNER POST-PR #179
GREEN authorization                 GRANTED BY OWNER AFTER RED #433
implementation authorization        GRANTED FOR V0 MINIMUM GREEN
execution authorization             NOT GRANTED
runtime delta                        0
authority delta                      0
```

Post-merge admission:

```text
PR #179 merged by Owner
main after merge: eb5a48fad12b8888192139e2b8a552bf50ce4870
Owner continued the work
RED candidate: AUTHORIZED
RED evidence: Validation #433 / 61 failed + 1278 passed on Ubuntu and Windows
GREEN / implementation: AUTHORIZED FOR V0 MINIMUM
execution: NOT AUTHORIZED
```

Siguiente paso permitido:

```text
minimum GREEN implementation only
-> targeted validation
-> Candidate FULL 4R
-> E2E / CI
-> RDD Stage 1 Candidate Conformance
-> human review
```

La autorización GREEN no autoriza el primer runtime self-review real. La
ejecución V0 sobre Malāk permanece separada y requiere cierre técnico y decisión
humana posterior.
