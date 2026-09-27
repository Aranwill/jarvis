---
title: Malāk Seventh U01 Admission Review — 2026-09-26
status: proposed
authority: non_normative
document_role: admission_review
language: es
created: 2026-09-26
reviewed_code_baseline: 4833b50d76cf139c3466c7b8acd68bc4168ce708
execution_baseline_rule: current_main_with_admission_doc_only_delta
admission_result: conditional_pass_pending_final_validation
risk_class: high_bounded_local_runtime
runtime_execution_authorized: false
seventh_u01_authorized: false
self_modification_authorized: false
authority_effect: none
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
  - docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md
  - docs/project/sprints/proposals/MALAK-SIXTH-U01-ADMISSION-REVIEW-20260926.md
  - docs/project/sprints/proposals/MALAK-E4-REFERENCE-BOUNDED-STRUCTURED-OUTPUT-V0-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-ENGINEERING-RUNTIME-GENERATION-CONTRACT-V0-G0-G1-DESIGN.md
---

# Malāk Seventh U01 Admission Review — 2026-09-26

## 1. Propósito

Determinar si puede prepararse una séptima ejecución gobernada de:

~~~text
U01 — Core Kernel
~~~

después de que Sixth U01 demostrara:

~~~text
Evidence Packet       PASS
Engineering Inspect   PASS
Engineering Analyze   PASS / GROUNDED
Engineering Propose   component_error
terminal              INCONCLUSIVE
acceptance            PASS
authority_effect      none
~~~

y de que el blocker observado en E4 fuera corregido mediante un contrato
reference-bound de Structured Output.

Este documento:

~~~text
NO ejecuta Self-Review
NO autoriza runtime
NO autoriza Seventh U01
NO autoriza self-modification
NO cambia Kernel
NO cambia Planner
NO cambia Evidence Focus
NO cambia generation contract
NO concede autoridad al modelo
~~~

## 2. Baseline revisado

~~~text
repository:
Aranwill/jarvis

branch:
main

reviewed_code_baseline:
4833b50d76cf139c3466c7b8acd68bc4168ce708

main vs merge commit:
IDENTICAL

open PRs observed:
0
~~~

Este baseline contiene:

~~~text
PR #197 — Runtime Generation Contract V0
PR #199 — Sixth U01 Admission
PR #200 — E4 Reference-Bounded Structured Output V0 design
PR #201 — E4 Reference-Bounded Structured Output V0 implementation
~~~

## 3. Binding de ejecución

Después de integrar este admission:

~~~text
execution_baseline
= exact current main HEAD at local preflight
~~~

Único delta permitido desde el baseline revisado:

~~~text
docs/project/sprints/proposals/
MALAK-SEVENTH-U01-ADMISSION-REVIEW-20260926.md
~~~

Cualquier otro cambio:

~~~text
-> admission invalidated
-> STOP
-> new review required
~~~

## 4. Sixth U01 — evidencia preservada

Run:

~~~text
run_id:
bootstrap-u01-20260926-006

baseline:
74d7e3374c342c51bec12cc303d7b9658a634db9

scope:
U01 — Core Kernel

runtime:
OllamaRuntime

model:
qwen3.5:9b
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

Assessment material:

~~~text
analysis_status   GROUNDED
focus_id          U01
focus_complete    true
finding_count     4
classifications   ALIGNED, ALIGNED, ALIGNED, PARTIAL
~~~

## 5. Root cause de Sixth U01

Safe diagnostic:

~~~text
component             engineering_propose
reason_code           component_error
exception_type        RuntimeError
origin_scope          repository
repo_relative_file    src/malak/capabilities/_engineering_analysis.py
function              _parse_engineering_finding
authority_effect      none
~~~

La validación material rechazó:

~~~text
finding cites unknown evidence refs
~~~

Interpretación:

~~~text
E4 internal analysis inference
-> model output received
-> output reached semantic parser
-> at least one R#/K# ref was outside the exact evidence set
-> parser rejected
-> fail closed
-> INCONCLUSIVE
~~~

El parser actuó correctamente.

El problema aislado fue:

~~~text
E4 LLM output contract
was weaker than
E4 semantic reference contract
~~~

## 6. Remediation integrada

### 6.1 Diseño

PR #200:

~~~text
E4 Reference-Bounded Structured Output V0
~~~

Candidate-bound design closure:

~~~text
Validation #606
Ubuntu   1578 passed
Windows  1578 passed
compile  PASS
diff     PASS
~~~

Diseño seleccionado:

~~~text
E4 internal analysis
-> response_json_schema
-> exact R#/K# enum from same evidence packet

E4 proposal
-> response_json_schema
-> exact A# enum
-> exact R#/K# enum from same proposal packet

existing parsers
-> remain authoritative
~~~

### 6.2 RED / GREEN implementation

PR #201:

~~~text
RED — Validation #608
1577 passed
6 expected failures

GREEN — Validation #611
1583 passed
0 failures
~~~

Candidate final:

~~~text
ec1695968800145469537ddc8439a0433f6257b6
~~~

Merge baseline:

~~~text
4833b50d76cf139c3466c7b8acd68bc4168ce708
~~~

Post-GREEN closure:

~~~text
FULL 4R                     PASS
E2E / integration           PASS
independent validation      PASS
RDD Stage 1 Candidate       PASS
blocking findings           0
~~~

## 7. Qué cambió desde Sixth U01

Cambio material:

~~~text
E4 internal analysis
before:
response_json_schema = None

after:
response_json_schema = exact evidence-bound schema
~~~

y:

~~~text
E4 proposal
before:
response_json_schema = None

after:
response_json_schema =
exact A# + exact R#/K# reference-bound schema
~~~

No cambió:

~~~text
E3 observable behavior
semantic parser acceptance
Evidence Focus
generation contract
OllamaRuntime
Kernel
Planner
authority
~~~

## 8. Por qué Seventh U01 es un nuevo run

Sixth U01 queda preservado como evidencia histórica:

~~~text
bootstrap-u01-20260926-006
-> INCONCLUSIVE
~~~

No se borra ni reutiliza.

Seventh U01 debe usar:

~~~text
bootstrap-u01-20260926-007
~~~

porque:

~~~text
new code baseline
new behavior under evaluation
new artifact identity required
~~~

## 9. Generation Contract candidato

Se conserva exactamente el contract ya admitido para Sixth U01:

~~~text
context_window_tokens = 32768
max_output_tokens     = 2048
thinking_enabled      = false
truncate              = false
shift                 = false
~~~

No existe evidencia actual que justifique otro cambio de recursos.

## 10. Por qué 32768 se conserva

Fifth U01 demostró:

~~~text
8192 context
< approximately 20041 request tokens
-> HTTP 400
~~~

Sixth U01 con 32768 logró:

~~~text
Evidence Packet   PASS
Inspect           PASS
Analyze           PASS
~~~

Por tanto:

~~~text
32768 solved the observed context blocker
through E3
~~~

El nuevo blocker fue independiente del contexto:

~~~text
E4 unknown evidence ref
~~~

Como ese blocker fue tratado mediante Structured Output reference-bound:

~~~text
no evidence supports
raising context again
~~~

Regla:

~~~text
no auto-scaling
no speculative resource change
~~~

## 11. Runtime / model expectations

Preflight esperado:

~~~text
runtime_class             OllamaRuntime
runtime_version           0.33.3
requested_model           qwen3.5:9b
resolved_model            qwen3.5:9b
model_identity_strength   TAG_DIGEST_BOUND
declared_context_window   262144
context_window_source     ollama:model_info
provenance_status         READY
authority_effect          none
~~~

El digest exacto debe recapturarse localmente.

No se reutiliza ciegamente el digest de Sixth U01.

Cualquier drift:

~~~text
STOP
-> review required
~~~

## 12. External configuration freeze

Candidate:

~~~powershell
$env:MALAK_RUNTIME = "ollama"
$env:MALAK_OLLAMA_MODEL = "qwen3.5:9b"
$env:MALAK_REPOSITORY_ROOT = "D:\Ollama\jarvis"
$env:MALAK_OLLAMA_CONTEXT_WINDOW_TOKENS = "32768"
$env:MALAK_OLLAMA_MAX_OUTPUT_TOKENS = "2048"
$env:MALAK_OLLAMA_THINKING = "disabled"
~~~

Expected base URL:

~~~text
http://localhost:11434
~~~

## 13. Run identity propuesta

~~~text
run_id:
bootstrap-u01-20260926-007

task_id:
governed-self-review-bootstrap-v0

focus_id:
U01

focus_label:
U01 Core Kernel

engineering_subject:
Kernel
~~~

El run_id debe estar libre en local preflight.

## 14. Validation lineage propuesta

Minimum lineage:

~~~text
Validation#597
PR#197

Validation#603
PR#199

Validation#606
PR#200

Validation#608
Validation#611
PR#201

run@bootstrap-u01-20260926-006

reviewed-code@4833b50d76cf139c3466c7b8acd68bc4168ce708
admission@<merged-seventh-admission-main-sha>
~~~

Interpretación:

~~~text
Validation #597
-> Runtime Generation Contract

Validation #603
-> Sixth U01 resource admission

Validation #606
-> E4 reference-bound design

Validation #608
-> causal RED evidence

Validation #611
-> GREEN candidate + regression closure
~~~

## 15. Evidence Focus

U01 permanece:

~~~text
focus_id       U01
focus_label    U01 Core Kernel
subject        Kernel
~~~

No se modifican selectors.

Required repository selectors:

~~~text
PATH_PREFIX  src/malak/kernel/
EXACT_PATH   src/malak/services/planner.py
EXACT_PATH   src/malak/contracts/capability.py
EXACT_PATH   src/malak/app/composition.py
EXACT_PATH   tests/test_kernel.py
~~~

Required knowledge selectors permanecen los seis gobernados por el baseline.

Runtime debe volver a demostrar:

~~~text
focus_complete == true
~~~

y continuidad de:

~~~text
evidence_set_digest
~~~

entre componentes aplicables.

## 16. E4 reference-bound expectations

Seventh U01 debe ejercer el nuevo contrato real de E4.

### Internal analysis

Expected:

~~~text
same evidence packet
-> exact R#/K# refs
-> response_json_schema enum
-> provider structured output
-> same exact parser allowed_refs
~~~

### Proposal

Si E4 recibe análisis accionable:

~~~text
same analysis packet
-> exact A# refs
same evidence packet
-> exact R#/K# refs
-> proposal response_json_schema
-> existing proposal semantic parser
~~~

Structured Output:

~~~text
does not replace parser
does not grant authority
does not imply proposal acceptance
~~~

## 17. Outcomes válidos

~~~text
NO_CHANGE_RECOMMENDED
HARDENING_PROPOSAL
RESEARCH_REQUIRED
DEFER
INCONCLUSIVE
~~~

También continúa siendo válido:

~~~text
controlled component failure
~~~

Reglas:

~~~text
schema compliance != semantic acceptance
proposal != decision
proposal != implementation
model output != authority
acceptance PASS != cognitive PASS
INCONCLUSIVE != hidden success
~~~

## 18. Construction Flow aplicable

Este admission:

~~~text
does not change product design
does not change production code
does not change architecture
does not change critical contracts
~~~

Los cambios de critical contract ya fueron cerrados en PR #200 / #201.

Por tanto este gate aplica:

~~~text
G0 / admission review
four questions of law
execution-profile 4R
Security Horizon check
RDD Stage 1 execution identity
candidate-bound CI
human review
Owner Ready / Merge
separate local sync
separate local preflight
separate explicit runtime authorization
~~~

No aplica nuevamente:

~~~text
RED / GREEN implementation
Critical Contract Hardening
~~~

porque no se está modificando el contrato en este admission.

## 19. Cuatro preguntas de ley

### Blueprint

~~~text
PASS
~~~

- Kernel First intacto.
- Capability First intacto.
- Runtime Independence intacto.
- Human in Control intacto.
- Model Agnostic intacto.

### Cognitive Constitution

~~~text
PASS
~~~

- la evidencia conduce la decisión de reintento;
- Sixth U01 permanece INCONCLUSIVE;
- no se inventa un PASS retrospectivo;
- Generation != Acceptance intacto;
- Evidence != Authority intacto.

### Governance Constitution

~~~text
PASS
~~~

- Owner conserva autorización;
- admission != execution permission;
- no auto-retry;
- no auto-merge;
- no self-modification.

### Kernel

~~~text
UNCHANGED / PASS
Kernel delta = 0
Planner delta = 0
~~~

## 20. Security Horizon Check

Seventh U01 candidate remains:

~~~text
local
single-host
read-only over tracked baseline
local Ollama inference
no tools
no agents
no external research
no model mutation
no Memory mutation
no Knowledge mutation
no tracked production edit
no self-modification
authority_effect none
~~~

E4 Structured Output adds:

~~~text
provider-side output constraint
+
existing semantic parser
~~~

No new authority surface is introduced.

## 21. Execution-profile 4R

### Risk

~~~text
PASS WITH PREFLIGHT
~~~

Primary residual risks:

- host drift;
- model/runtime drift;
- run_id reuse;
- schema provider incompatibility;
- new model output failure;
- resource pressure.

Mitigation:

~~~text
exact preflight
single run
no retry
no auto-scaling
fail closed
Owner authorization
~~~

### Readability

~~~text
PASS
~~~

Run identity, baseline, resource contract, lineage and authority are explicit.

### Reliability

~~~text
PASS WITH LOCAL PREFLIGHT PENDING
~~~

Repository candidate is validated.

Still host-dependent:

~~~text
exact local HEAD
origin/main equality
Ollama reachability
runtime version
model digest
declared context
generation options
run_id availability
~~~

### Resilience

~~~text
PASS
~~~

Any:

~~~text
baseline mismatch
dirty tree
run_id collision
identity mismatch
schema/provider failure
context failure
component error
~~~

must yield:

~~~text
STOP / INCONCLUSIVE
no retry
no budget increase
no authority expansion
~~~

## 22. RDD Stage 1 execution identity

~~~text
reviewed baseline          explicit
future execution baseline  bound
run_id                     explicit
model                      explicit
generation contract        explicit
validation refs            explicit
E4 remediation lineage     explicit
authority                  unchanged
~~~

Disposition:

~~~text
PASS FOR ADMISSION DESIGN
~~~

No runtime execution is authorized.

## 23. Preflight local obligatorio

Before any Seventh U01 authorization:

~~~text
branch == main
tracked tree == clean
HEAD == exact merged admission baseline
origin/main == HEAD
run_id unused

Python == official project environment
Ollama reachable
runtime version == expected reviewed version
qwen3.5:9b resolves
exact model digest captured
TAG_DIGEST_BOUND
declared_context_window >= 32768

generation contract:
context  = 32768
output   = 2048
thinking = disabled
truncate = false
shift    = false

provenance generation_options
==
requested generation contract
~~~

Any mismatch:

~~~text
STOP
runtime execution remains NOT AUTHORIZED
~~~

## 24. Deferred findings remain separate

### D01 — HTTP status in Safe Diagnostic

~~~text
DEFERRED
separate observability gate
~~~

### D02 — reuse prior E3 live analysis in E4

~~~text
DEFERRED
separate orchestration / architecture gate
~~~

Neither is a blocker for Seventh U01 admission.

## 25. Admission Coverage Ledger

| Group | Evidence | Disposition |
|---|---|---|
| Repo baseline | main@4833b50d... | CURRENT_STATE_REVALIDATED |
| Runtime contract | PR #197 / Validation #597 | CURRENT_STATE_REFERENCE |
| Sixth admission | PR #199 / Validation #603 | HISTORICAL_RESOURCE_REFERENCE |
| Sixth runtime | bootstrap-u01-20260926-006 | OWNER_LOCAL_RUNTIME_EVIDENCE |
| E4 design | PR #200 / Validation #606 | CURRENT_STATE_REFERENCE |
| E4 RED | Validation #608 | HISTORICAL_CAUSAL_EVIDENCE |
| E4 GREEN | PR #201 / Validation #611 | CURRENT_STATE_REVALIDATED |
| U01 Evidence Focus | unchanged | CURRENT_STATE_PRESERVED |
| Governance / security | baseline normative documents | CURRENT_STATE_REVALIDATED_BY_INHERITED_FLOW |
| Deferred observability | HTTP status retention | DEFERRED |
| Deferred orchestration | E3 output reuse | DEFERRED |

This review is incremental and bounded.

It does not claim a full Malāk audit.

## 26. Admission disposition

Before candidate-bound CI:

~~~text
Sixth U01 integrity              PASS
Sixth U01 cognitive result      INCONCLUSIVE
Sixth blocker isolated          PASS
E4 reference-bound design       PASS
E4 RED                          PASS AS RED
E4 GREEN                        PASS
E4 FULL 4R                      PASS
E4 E2E                          PASS
E4 candidate conformance        PASS

context 32768                    PRESERVED
output 2048                      PRESERVED
thinking disabled                PRESERVED
truncate=false                   PRESERVED
shift=false                      PRESERVED

Kernel delta                     0
Planner delta                    0
Evidence Focus delta             0
runtime contract delta           0
authority_effect                 none

admission candidate CI           PASS — Validation #613
final admission validation       PENDING
local preflight                  NOT EXECUTED
runtime execution                NOT AUTHORIZED
Seventh U01                      NOT AUTHORIZED
self-modification                NOT AUTHORIZED
~~~

Admission result:

~~~text
CONDITIONAL PASS
pending final candidate-bound validation
after recording Validation #613
~~~

## 27. Candidate-bound admission validation

Validation #613 executed against:

~~~text
candidate:
b598172abc905ba2d6afba4245bcf3ca966cdf71
~~~

Result:

~~~text
Ubuntu                       1583 passed
Windows                      1583 passed
compileall                   PASS
candidate identity           PASS
candidate diff               PASS
review threads               0
~~~

Validated scope:

~~~text
1 admission document
0 production code
Kernel delta 0
Planner delta 0
Evidence Focus delta 0
runtime contract delta 0
authority_effect none
~~~

Interpretation:

~~~text
candidate-bound admission validation PASS
!= local preflight
!= runtime authorization
!= Seventh U01 authorization
~~~

Recording this evidence changes the candidate identity.

Therefore one final candidate-bound Validation is required before Owner review /
merge.

## 28. Current authority state

~~~text
admission review       PREPARED
runtime execution      NOT AUTHORIZED
Seventh U01            NOT AUTHORIZED
self-modification      NOT AUTHORIZED
Ready                  OWNER ONLY
merge                  OWNER ONLY
authority_effect       none
~~~
