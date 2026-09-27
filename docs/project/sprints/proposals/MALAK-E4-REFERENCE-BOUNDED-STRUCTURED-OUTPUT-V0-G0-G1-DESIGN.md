---
title: Malāk E4 Reference-Bounded Structured Output V0 — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation_design
language: es
created: 2026-09-26
baseline_commit: 74d7e3374c342c51bec12cc303d7b9658a634db9
g0_result: pass
design_authorized_by: owner
design_authorized_at: 2026-09-26
critical_contract: true
risk_class: 3
implementation_authorized: false
red_authorized: false
green_authorized: false
runtime_execution_authorized: false
seventh_u01_authorized: false
self_modification_authorized: false
authority_effect: none
rdd_stage_1_design_check: pass
design_candidate_validation: pass
design_candidate_validation_ref: Validation#605
rdd_stage_2_authorized: false
related:
  - AGENTS.md
  - SECURITY.md
  - docs/development/malak_construction_protocol.md
  - docs/development/development_checklist.md
  - docs/development/engineering_method.md
  - docs/architecture/blueprint.md
  - docs/architecture/architecture_quality_gates.md
  - docs/governance/cognitive_constitution.md
  - docs/governance/governance_constitution.md
  - docs/project/implementation_roadmap.md
  - documents/projects/jarvis/ideas.md
  - docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md
  - docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md
  - docs/project/sprints/proposals/MALAK-E4-ENGINEERING-PROPOSE-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-ANALYZE-STRUCTURED-OUTPUT-CONTRACT-V0-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-SIXTH-U01-ADMISSION-REVIEW-20260926.md
  - src/malak/core/conversation.py
  - src/malak/capabilities/_engineering_analysis.py
  - src/malak/capabilities/engineering_analyze.py
  - src/malak/capabilities/engineering_propose.py
  - src/malak/runtime/ollama_runtime.py
  - tests/test_engineering_analyze.py
  - tests/test_engineering_propose.py
---

# Malāk E4 Reference-Bounded Structured Output V0 — G0/G1 Design

## 1. Propósito

Diseñar un hardening acotado de Engineering Propose (E4) después de que una
ejecución real y gobernada del Sixth U01 demostrara:

~~~text
Evidence Packet       PASS
Engineering Inspect   PASS
Engineering Analyze   PASS / GROUNDED
Engineering Propose   component_error
terminal              INCONCLUSIVE
acceptance            PASS
authority_effect      none
~~~

El fallo material ocurrió durante la fase de análisis interno de E4, antes de
que E4 llegara a producir una proposal.

Objetivo:

~~~text
reforzar machine-readable output constraints
sin relajar semantic validation
~~~

Este documento:

~~~text
NO implementa código
NO autoriza RED
NO autoriza GREEN
NO autoriza runtime
NO autoriza Seventh U01
NO cambia Kernel
NO cambia Planner
NO modifica Evidence Focus
NO cambia autoridad
~~~

## 2. Evidencia causal — Sixth U01

Run observado por el Owner:

~~~text
run_id       bootstrap-u01-20260926-006
baseline     74d7e3374c342c51bec12cc303d7b9658a634db9
scope        U01 — Core Kernel
runtime      OllamaRuntime
model        qwen3.5:9b
~~~

Resultado:

~~~text
Evidence Packet              OK
Engineering Inspect          OK
Engineering Analyze          OK
Engineering Propose          component_error
terminal_disposition         INCONCLUSIVE
live_replay_equivalence      true
tracked_tree_clean           true
acceptance                   PASS
authority_effect             none
~~~

Assessment:

~~~text
analysis_status  GROUNDED
focus_id         U01
focus_complete   true
finding_count    4
classifications  ALIGNED, ALIGNED, ALIGNED, PARTIAL
~~~

El finding PARTIAL habilitó legítimamente la ruta de propuesta.

## 3. Safe diagnostic exacto

El Safe Diagnostic Envelope persistido registró:

~~~text
component             engineering_propose
reason_code           component_error
exception_type        RuntimeError
origin_scope          repository
repo_relative_file    src/malak/capabilities/_engineering_analysis.py
function              _parse_engineering_finding
line                  465
authority_effect      none
~~~

La línea material del baseline es la validación de referencias desconocidas:

~~~text
unknown_refs = set(refs_raw) - allowed_refs

unknown_refs non-empty
-> RuntimeError
-> finding cites unknown evidence refs
~~~

Interpretación causal:

~~~text
E4 internal analysis inference
-> model content received
-> parser reached finding semantics
-> at least one evidence ref was not in allowed evidence set
-> strict parser rejected output
-> component_error
-> INCONCLUSIVE
~~~

No existe evidencia de que el fallo actual sea:

~~~text
context exhaustion
Ollama reachability
model identity
Evidence Focus incompleteness
E3 parser failure
proposal parser failure
proposal cross-reference failure
~~~

E4 todavía no había llegado a su proposal inference.

## 4. Contexto histórico relevante

Analyze Structured Output Contract V0 creó una primitive provider-neutral:

~~~text
ConversationRequest.response_json_schema
~~~

y la aplicó deliberadamente sólo a E3.

Decisión histórica explícita:

~~~text
build reusable primitive now
apply only to Analyze first
validate in tests + real bounded run
then decide a separate E4 slice
~~~

Scope congelado:

~~~text
E3 Analyze
-> structured output

E4 internal analysis
-> response_json_schema = None

E4 proposal
-> response_json_schema = None
~~~

Sixth U01 no revela una regresión accidental.

Revela:

~~~text
the next intentionally deferred E4 hardening boundary
~~~

## 5. Clasificación

El cambio es contrato crítico porque E4:

~~~text
interpreta findings ligados a evidencia
produce proposal candidates
valida bindings R#/K#/A#
puede informar revisión humana posterior
~~~

Secuencia obligatoria:

~~~text
G0/G1
-> Critical Contract Hardening
-> Four Questions of Law
-> Design 4R
-> RDD Stage 1 Design Check
-> RED
-> GREEN
-> Candidate FULL 4R
-> bounded correction when needed
-> E2E / integration
-> candidate-bound CI
-> independent validation
-> RDD Stage 1 Candidate Conformance
-> human review
-> Ready
-> human merge
~~~

Este documento llega sólo hasta RDD Stage 1 Design Check.

## 6. G0 — necesidad material

E4 exige semánticamente:

~~~text
findings cite only real R#/K#
proposals cite only real A#
proposals cite only real R#/K#
proposal evidence traces through cited findings
~~~

Pero hoy sus dos inferencias dependen de:

~~~text
prompt says strict JSON
+
strict semantic parser
-
runtime structured-output enforcement
~~~

Sixth U01 demostró que el primer LLM call interno de E4 puede emitir una
referencia inexistente y alcanzar el parser.

El parser funcionó correctamente:

~~~text
invalid ref
-> reject
-> fail closed
~~~

La necesidad NO es relajar el parser.

La necesidad es reducir outputs inválidos antes del parser usando la primitive
provider-neutral existente.

Resultado:

~~~text
G0 = PASS
~~~

No se justifica:

~~~text
retry
repair
parser relaxation
model replacement
sampling changes
Evidence Focus reduction
authority changes
~~~

## 7. Objetivo G1

Adoptar Structured Output en E4 con referencia exacta al packet:

~~~text
provider structural constraint
+
exact reference enum constraint
+
existing semantic parser
~~~

Nunca:

~~~text
provider schema replaces semantic validation
~~~

## 8. No-objetivos

Fuera de alcance:

~~~text
E3 observable behavior changes
E2 behavior changes
Evidence Focus changes
new retrieval
prompt repair
output repair
automatic retry
temperature / sampling changes
model changes
context auto-scaling
raw model response persistence
new provenance authority
Kernel changes
Planner changes
CLI changes
tools
agents
network expansion
filesystem writes
Git operations
self-modification
Seventh U01 execution
~~~

## 9. G1 — arquitectura seleccionada

### 9.1 Primitive reutilizada

Se reutiliza:

~~~text
ConversationRequest.response_json_schema: str | None
~~~

Ya posee:

~~~text
strict JSON validation
canonical serialization
root-object requirement
64 KiB hard UTF-8 limit
provider-neutral representation
Ollama format mapping
unsupported-provider fail-closed behavior
~~~

No se crea otra primitive de structured output.

### 9.2 E3 permanece sin cambios

E3 conserva:

~~~text
response_json_schema = ANALYZE_RESPONSE_JSON_SCHEMA
~~~

Su schema estático y parser no cambian.

### 9.3 E4 internal analysis — schema evidence-bound

Flujo:

~~~text
collect exact evidence bundle
        ↓
repository_evidence tuple
knowledge_evidence tuple
        ↓
derive exact refs
R# + K#
        ↓
build canonical Analyze schema
evidence_refs.items.enum = exact refs
        ↓
ConversationRequest.response_json_schema
        ↓
provider structured output
        ↓
existing parse_engineering_analysis
        ↓
existing semantic validation
~~~

La misma evidencia alimenta:

~~~text
prompt
schema enum
parser allowed_refs
evidence_set_digest
~~~

### 9.4 Shared analysis helper

run_engineering_analysis hoy recibe:

~~~text
response_json_schema: str | None
~~~

G1 propone agregar a esa utility privada un builder opcional:

~~~text
response_json_schema_builder:
    Callable[
        [repository_evidence_tuple, knowledge_evidence_tuple],
        canonical_schema_string,
    ] | None
~~~

Reglas:

~~~text
static schema None + builder None
-> current unconstrained behavior

static schema present + builder None
-> current E3 behavior

static schema None + builder present
-> build after exact evidence collection

static schema present + builder present
-> fail closed
~~~

El helper no decide política.

~~~text
shared implementation utility != policy owner
~~~

E3 elige static schema.

E4 elige evidence-bound builder.

### 9.5 Analyze evidence-bound schema

Se reutiliza el shape lógico de ANALYZE_RESPONSE_JSON_SCHEMA.

Cambio:

~~~text
findings[].evidence_refs.items
~~~

de:

~~~json
{"type":"string"}
~~~

a:

~~~json
{
  "type":"string",
  "enum":["R1","...","Rn","K1","...","Km"]
}
~~~

El enum:

- nace del tuple exacto canonicalizado;
- conserva orden determinista;
- no admite duplicados;
- no concede autoridad.

El parser sigue exigiendo:

~~~text
actual membership
no duplicates
valid classification
relational finding requires R + K
reserved ref token protection
all current byte/count bounds
~~~

### 9.6 E4 proposal — schema reference-bound

Luego de aceptar análisis:

~~~text
analysis findings
-> A1 ... An
~~~

y con el mismo evidence set:

~~~text
R1 ... Rn
K1 ... Km
~~~

E4 crea schema de proposal con:

~~~text
proposal.kind
-> current allowed enum

proposal.finding_refs.items
-> exact A# enum

proposal.evidence_refs.items
-> exact R#/K# enum
~~~

El shape actual permanece:

~~~text
summary
proposals
validation_plan
risks
assumptions
~~~

### 9.7 Límite expresivo

JSON Schema NO intenta expresar:

~~~text
proposal evidence_refs
must belong to
union of evidence refs from cited finding_refs
~~~

Esa relación sigue siendo responsabilidad de _parse_proposal_set.

Regla:

~~~text
schema constrains candidate shape
parser decides semantic acceptance
~~~

## 10. Canonicalidad y binding

### 10.1 Refs exactas

Refs permitidas se derivan sólo de objetos exactos del packet.

Prohibido:

~~~text
numeric range inference
external lookup
repository re-enumeration
model-declared allowed refs
closest-ref repair
~~~

### 10.2 Orden determinista

Orden:

~~~text
repository evidence tuple
then knowledge evidence tuple
~~~

A#:

~~~text
analysis findings tuple order
~~~

### 10.3 Same-packet binding

Debe existir una única cadena:

~~~text
evidence tuples
-> prompt
-> schema
-> parser
~~~

Divergencia:

~~~text
STOP
~~~

## 11. Schema-size boundary

ConversationRequest impone:

~~~text
64 KiB hard UTF-8 schema limit
~~~

Regla:

~~~text
dynamic schema > 64 KiB
-> request rejected
-> fail closed
-> no fallback to schema None
~~~

U01 observado:

~~~text
repository evidence ≈ 103
knowledge evidence  ≈ 101
total refs           ≈ 204
~~~

Ese caso cabe con margen.

No se convierte esta observación en garantía universal.

## 12. Provider behavior

OllamaRuntime ya soporta:

~~~text
response_json_schema
-> canonical object
-> /api/chat format
~~~

No se espera cambio de runtime.

Provider sin soporte:

~~~text
schema requested
+
provider unsupported
-> fail closed
~~~

Nunca fallback unconstrained.

## 13. Inference budget preservado

~~~text
analysis inference   <= 1
proposal inference   <= 1
total                <= 2
~~~

Este hardening no agrega:

~~~text
retry
repair
critique call
retrieval loop
~~~

## 14. Eligibility E4 preservada

~~~text
UNCONFIRMED
-> no proposal call

UNRESOLVED
-> no proposal call

CONTRADICTION
-> no proposal call

all ALIGNED
-> no proposal call

GAP or PARTIAL
and no blockers
-> proposal call allowed
~~~

Structured Output no decide eligibility.

## 15. Parsers continúan autoritativos

Internal analysis parser conserva:

~~~text
strict JSON
duplicate-key rejection
non-finite rejection
exact keys
classification allow-list
actual evidence membership
R + K requirement
bounds
reserved-ref protections
~~~

Proposal parser conserva:

~~~text
strict JSON
exact keys
allowed kinds
actual A# membership
actual R#/K# membership
evidence belongs to cited finding union
at least one actionable cited finding
duplicate rejection
bounds
reserved-ref protections
~~~

## 16. Critical Contract Hardening

### H01 — schema no reemplaza parser

~~~text
CLOSED
~~~

### H02 — static schema no resuelve el fallo observado

~~~text
CLOSED
~~~

Un campo string aún permite R999.

E4 requiere enum exacto.

### H03 — enum no se infiere por rango numérico

~~~text
CLOSED
~~~

Se extraen refs concretas presentes.

### H04 — schema y parser no observan evidence distinto

~~~text
CLOSED
~~~

Mismos tuples in-memory.

### H05 — builder nunca falla open

~~~text
CLOSED
~~~

Cualquier:

~~~text
invalid builder output
oversized schema
empty required refs
provider unsupported
schema construction exception
~~~

produce failure.

Nunca fallback sin schema.

### H06 — E3 permanece unchanged

~~~text
CLOSED
~~~

### H07 — cross-reference semántica permanece en parser

~~~text
CLOSED
~~~

### H08 — unknown refs siguen inválidas si provider incumple schema

~~~text
CLOSED
~~~

Parser sigue siendo barrera.

### H09 — no repair loop

~~~text
CLOSED
~~~

Failure:

~~~text
component_error
-> INCONCLUSIVE
-> STOP
~~~

### H10 — authority zero

~~~text
CLOSED
~~~

Schema compliance:

~~~text
!= evidence authority
!= proposal authorization
!= implementation permission
~~~

### H11 — schema overflow

~~~text
CLOSED
~~~

64 KiB sigue siendo hard bound.

### H12 — determinismo

~~~text
CLOSED
~~~

Mismo tuple produce mismo enum y schema canónico.

## 17. Adversarial interpretation review

Rechazado:

1. provider schema permite omitir parser;
2. ref desconocida puede borrarse automáticamente;
3. typo puede mapearse a ref cercana;
4. R104 probablemente significa R103;
5. Structured Output equivale a grounded output;
6. proposal estructuralmente válida equivale a aceptada;
7. modelo decide refs válidas;
8. overflow de schema permite ejecutar sin schema;
9. E4 puede parsear el envelope textual renderizado de E3;
10. hardening autoriza Seventh U01.

Todas:

~~~text
REJECTED
~~~

## 18. Malāk Alignment Matrix

| Source | Authority class | Intent / invariant | Baseline evidence | Disposition | Implementation effect | Deferred / rejected |
|---|---|---|---|---|---|---|
| Blueprint | normative architecture | Capability First, Human in Control, Runtime Independence, Spec & Verification First | E4 capability + provider-neutral schema primitive | ADOPT | hardening en E4/private helper | Kernel/Planner/provider coupling rejected |
| Cognitive Constitution | normative cognition | Generation != Finalization; Evidence != Authority | parser semántico decide acceptance | ADOPT | schema = pre-constraint only | schema/model authority rejected |
| Governance Constitution | normative governance | Owner máxima autoridad | proposals terminan en Owner | ADOPT | authority_effect none | auto-approval rejected |
| SECURITY.md | protected security | Zero Trust, fail-closed | unknown refs ya fallan closed | ADOPT | no unconstrained fallback | silent repair/retry rejected |
| Architecture Quality Gates | architecture reference | runtime independence, traceability, human control | ConversationRequest is provider-neutral | ADOPT | caller declares schema | Ollama-specific capability type rejected |
| E4 G0/G1 historical design | approved design history | max 2 inference, grounded proposal, strict parser | current E4 implements rules | REUSE | request constraint only | eligibility/parser redesign rejected |
| Analyze Structured Output V0 | approved prior contract | reusable primitive; E4 adoption deferred | E3 schema, E4 None by scope | ADAPT | separate E4 adoption slice | E3 changes rejected |
| Implementation Roadmap | derived current state | E0-E4 integrated; Self-Review active candidate | E4 is current baseline | ADOPT | current-state remediation | roadmap != authority |
| ideas.md / IDEA-002 | non-normative | evidence -> proposal -> human | Sixth U01 stopped without self-change | ADOPT | improve proposal reliability | autonomous modification rejected |
| Research Horizon | non-normative | Governed Self-Improvement and Resource Governance aligned | bounded runtime already exists | ADOPT | reliability hardening | new subsystem rejected |
| Governed Self-Review Bootstrap | non-normative reference | proposal ends at Owner | U01 run STOP worked | ADOPT | harden existing E4 | auto-remediation rejected |
| Sixth U01 evidence | operator runtime evidence | unknown ref in E4 internal analysis | diagnostic/assessment/trace reviewed | OBSERVE / IMPLEMENTATION_INPUT | justifies slice | not source of law |
| Current code/tests | baseline implementation | strict parser + schema primitive | main at 74d7e337... | REUSE / ADAPT | private helper + E4 tests | broad refactor rejected |

Separaciones:

~~~text
alignment evidence != authority
ADOPT != implementation authorization
REUSE != runtime authorization
local runtime evidence != source of law
~~~

## 19. Security Horizon Check

Prompt & Context Trust Boundary:

~~~text
REQUIRES_REINFORCEMENT
~~~

Este slice refuerza output no confiable.

Identity / Delegation:

~~~text
NOT_APPLICABLE / unchanged
~~~

Memory / Knowledge admission:

~~~text
ALREADY_COVERED / unchanged
~~~

AI supply chain:

~~~text
NOT_APPLICABLE to this delta
~~~

Resource Governance:

~~~text
ALREADY_COVERED
generation contract unchanged
~~~

Observability:

~~~text
ALREADY_COVERED
component_error remains visible
~~~

HTTP status safe-diagnostic finding permanece:

~~~text
DEFERRED / separate gate
~~~

Human in Control:

~~~text
PASS
~~~

## 20. Cuatro preguntas de ley

### Blueprint

~~~text
PASS
~~~

E4 sigue siendo Capability; Kernel permanece limpio; contrato provider-neutral.

### Cognitive Constitution

~~~text
PASS
~~~

Output de modelo sigue no confiable; parser preserva acceptance; no evidence invention.

### Governance Constitution

~~~text
PASS
~~~

Owner conserva autorización; proposal != permission; no self-change.

### Kernel simplicity

~~~text
UNCHANGED / PASS
Kernel delta = 0
Planner delta = 0
~~~

## 21. Design 4R

### Risk

~~~text
PASS WITH HARD BOUNDARIES
~~~

Riesgos:

- schema sustituyendo parser;
- evidence mismatch;
- schema overflow;
- E3 collateral change;
- unconstrained fallback;
- false belief that schema validates cross-field semantics.

Mitigaciones:

- parser unchanged;
- same tuple binding;
- 64 KiB fail-closed;
- E3 static path unchanged;
- no fallback;
- cross-reference remains semantic.

### Readability

~~~text
PASS
~~~

Ownership:

~~~text
E3 -> static schema policy
E4 -> evidence-bound schema policy
shared helper -> mechanism only
ConversationRequest -> provider-neutral transport
parser -> semantic acceptance
~~~

No new Manager/Registry/framework.

### Reliability

~~~text
PASS FOR DESIGN
~~~

Requiere:

- canonical schema;
- deterministic enum;
- exact refs;
- unchanged parser;
- provider fail-closed;
- max two inferences;
- no retry;
- request contract testable.

### Resilience

~~~text
PASS FOR DESIGN
~~~

Ante:

~~~text
unknown ref
invalid schema
oversized schema
provider unsupported
invalid proposal relation
structured output failure
~~~

respuesta:

~~~text
component_error / fail closed
-> INCONCLUSIVE
-> no repair
-> no retry
-> no authority expansion
~~~

## 22. RDD Stage 1 — Design Check

Design baseline:

~~~text
74d7e3374c342c51bec12cc303d7b9658a634db9
~~~

Design unit:

~~~text
E4 Reference-Bounded Structured Output V0
~~~

Responsibilities:

~~~text
EngineeringProposeCapability
-> policy owner

run_engineering_analysis private helper
-> mechanism

ConversationRequest.response_json_schema
-> provider-neutral transport

existing parsers
-> semantic acceptance
~~~

Dependency direction:

~~~text
E4
-> private analysis helper
-> ConversationService
-> provider/runtime

no reverse dependency
no Kernel dependency
~~~

Expected implementation scope:

~~~text
src/malak/capabilities/_engineering_analysis.py
src/malak/capabilities/engineering_propose.py
tests/test_engineering_propose.py
targeted harness/conformance tests only if RED proves necessary
this design document
~~~

Expected zero delta:

~~~text
src/malak/kernel/**
src/malak/services/planner.py
src/malak/app/composition.py
E3 observable behavior
src/malak/runtime/ollama_runtime.py
src/malak/core/conversation.py
Evidence Focus catalog
~~~

Outside-scope required delta:

~~~text
STOP
-> return to G1
~~~

Design invalidates if:

~~~text
main materially changes E3/E4 structured-output path
response_json_schema contract changes
Evidence Focus ref identity changes
E4 parser semantics change independently
runtime schema support changes
~~~

Disposition:

~~~text
RDD Stage 1 Design Check = PASS
~~~

No implementation candidate exists yet.

## 23. RED requirements

RED is NOT AUTHORIZED by this document.

When separately authorized, demonstrate:

R01:

~~~text
first E4 request response_json_schema is currently None
~~~

R02:

~~~text
second E4 proposal request response_json_schema is currently None
~~~

R03:

~~~text
first E4 schema evidence enum
== exact packet R#/K# refs
~~~

R04:

~~~text
proposal finding enum
== exact A# refs
~~~

R05:

~~~text
proposal evidence enum
== exact R#/K# refs
~~~

R06:

~~~text
E3 request schema remains exactly current static schema
~~~

R07:

~~~text
parser still rejects unknown refs
~~~

R08:

~~~text
parser still rejects proposal evidence outside cited findings
~~~

R09:

~~~text
static schema + builder simultaneously
-> fail closed
~~~

R10:

~~~text
schema oversize
-> fail closed
-> no None fallback
~~~

R11:

~~~text
provider calls remain <= 2
no retry / repair
~~~

R12:

~~~text
malformed builder result rejected
~~~

R13:

~~~text
same evidence tuple
-> same canonical schema
~~~

R14:

~~~text
authority_effect none
owner authorization required
~~~

## 24. GREEN acceptance criteria

If later authorized:

~~~text
targeted RED tests PASS
existing E4 tests PASS
existing E3 tests PASS unchanged
full suite PASS
compileall PASS
diff check PASS
candidate identity PASS
Kernel delta 0
Planner delta 0
no runtime/core change unless re-admitted
no parser relaxation
no retry
no repair
authority_effect none
~~~

## 25. Candidate FULL 4R

Post-GREEN, each lens must run independently.

Blocking finding:

~~~text
-> bounded correction
-> Fix Validator
-> rerun affected evidence
~~~

No direct jump to E2E.

## 26. E2E / integration requirements

Path A:

~~~text
focused evidence
-> exact refs
-> dynamic analysis schema
-> ConversationRequest
-> provider structured output
-> parse_engineering_analysis
-> grounded analysis
~~~

Path B:

~~~text
grounded analysis
-> exact A# refs
-> dynamic proposal schema
-> ConversationRequest
-> provider structured output
-> _parse_proposal_set
-> grounded proposal envelope
~~~

Negative conformance:

~~~text
unknown evidence ref still rejected
unknown finding ref still rejected
cross-finding evidence mismatch still rejected
unsupported schema provider fails closed
no unconstrained fallback
~~~

Runtime U01 is not required for implementation E2E.

## 27. Candidate-bound CI

Required:

~~~text
Ubuntu
Windows
full pytest
compileall
candidate identity
candidate diff
~~~

Tests green alone do not close the contract.

## 28. Independent validation

Verify:

- scope;
- parser semantic behavior unchanged;
- E3 observable behavior unchanged;
- exact enum binding;
- no bypass/fallback;
- no authority expansion.

## 29. RDD Stage 1 Candidate Conformance

Only after:

~~~text
GREEN
FULL 4R
E2E
CI
independent validation
~~~

Compare exact candidate against this design.

## 30. Runtime follow-up

Seventh U01 only after:

~~~text
implementation merged by Owner
main verified
new admission
local sync
runtime/model preflight
generation contract preflight
new run_id
explicit Owner authorization
~~~

No runtime execution is authorized here.

## 31. Deferred findings

### D01 — HTTP status in Safe Diagnostic

~~~text
DEFERRED
separate observability gate
~~~

### D02 — reuse prior E3 live analysis in E4

E4 V0 currently permits:

~~~text
analysis inference <= 1
proposal inference <= 1
~~~

Changing orchestration to consume prior E3 live output would be a separate
architecture change and is not required to close this failure.

~~~text
DEFERRED
~~~

## 32. Scope summary

Expected implementation delta:

~~~text
_engineering_analysis private mechanism
engineering_propose E4 policy
E4 tests / targeted conformance
~~~

Expected zero delta:

~~~text
Kernel
Planner
E2
E3 observable behavior
Evidence Focus
Conversation public contract
OllamaRuntime behavior
generation contract
governance authority
~~~

## 33. Candidate-bound design validation

Validation #605 executed against:

~~~text
candidate:
7a8da22865546117c6f6c8240699bd8cfcf84533
~~~

Result:

~~~text
Ubuntu                       1578 passed
Windows                      1578 passed
compile                      PASS
candidate identity           PASS
candidate diff               PASS
review threads               0
~~~

Validated scope:

~~~text
1 design document
0 production code
Kernel delta 0
Planner delta 0
Evidence Focus delta 0
authority_effect none
~~~

Interpretation:

~~~text
candidate-bound design validation PASS
!= RED authorization
!= implementation authorization
~~~

This documentation-only closure changes the candidate identity and therefore
requires one final candidate-bound Validation before human review / merge.

## 34. Current disposition

~~~text
G0                              PASS
G1                              PASS
Critical Contract Hardening     PASS
Four Questions of Law           PASS
Design 4R                       PASS
RDD Stage 1 Design Check        PASS
Design candidate validation     PASS — Validation #605

implementation                  NOT AUTHORIZED
RED                             NOT AUTHORIZED
GREEN                           NOT AUTHORIZED
runtime execution               NOT AUTHORIZED
Seventh U01                     NOT AUTHORIZED
self-modification               NOT AUTHORIZED
authority_effect                none
~~~

Next lawful transition:

~~~text
Owner reviews G0/G1 design candidate
-> candidate-bound CI
-> human decision whether RED may be authorized
~~~
