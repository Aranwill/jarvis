---
title: Malāk Sixth U01 Admission Review — 2026-09-26
status: proposed
authority: non_normative
document_role: admission_review
language: es
created: 2026-09-26
reviewed_code_baseline: 0794d5617eec354a66c41e271e7bf413d454b1a6
execution_baseline_rule: current_main_with_admission_doc_only_delta
admission_result: conditional_pass
risk_class: high_bounded_local_runtime
runtime_execution_authorized: false
sixth_u01_authorized: false
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
  - docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md
  - docs/project/sprints/proposals/MALAK-FIFTH-U01-ADMISSION-REVIEW-20260926.md
  - docs/project/sprints/proposals/MALAK-ENGINEERING-RUNTIME-GENERATION-CONTRACT-V0-G0-G1-DESIGN.md
---

# Malāk Sixth U01 Admission Review — 2026-09-26

## 1. Propósito

Determinar si puede prepararse una sexta ejecución gobernada de:

```text
U01 — Core Kernel
```

después de que Fifth U01 terminara de forma íntegra pero `INCONCLUSIVE` por
insuficiencia explícita del contexto solicitado.

Este documento:

```text
NO ejecuta Self-Review
NO autoriza runtime
NO autoriza self-modification
NO cambia el contrato productivo
NO cambia Evidence Focus
NO cambia Kernel
NO cambia Planner
NO concede autoridad al modelo
```

Su efecto es exclusivamente preparar una nueva política de recursos
request-scoped para revisión humana.

## 2. Baseline revisado

```text
repository:
Aranwill/jarvis

branch:
main

reviewed_code_baseline:
0794d5617eec354a66c41e271e7bf413d454b1a6

open PRs observed before branch:
0

main vs reviewed baseline:
IDENTICAL
```

El baseline ya contiene:

```text
PR #197 — Runtime Generation Contract V0
PR #198 — Fifth U01 Admission
```

## 3. Binding de ejecución

Después de integrar este admission:

```text
execution_baseline
= exact current main HEAD at local preflight
```

Único delta permitido desde el baseline revisado:

```text
docs/project/sprints/proposals/
MALAK-SIXTH-U01-ADMISSION-REVIEW-20260926.md
```

Cualquier otro cambio:

```text
-> admission invalidated
-> STOP
-> new review required
```

## 4. Fifth U01 — estado preservado

Ejecución autorizada previamente:

```text
run_id:
bootstrap-u01-20260926-005

baseline:
0794d5617eec354a66c41e271e7bf413d454b1a6

scope:
U01 — Core Kernel

runtime:
OllamaRuntime

model:
qwen3.5:9b
```

Resultado observado por el harness:

```text
Evidence Packet              OK
Engineering Inspect          component_error
Engineering Analyze          SKIPPED / precondition_not_met
Engineering Propose          SKIPPED / precondition_not_met
terminal_disposition         INCONCLUSIVE
live_replay_equivalence      true
tracked_tree_clean           true
acceptance                   PASS
authority_effect             none
```

Interpretación:

```text
acceptance PASS
!=
U01 PASS
```

`acceptance PASS` demuestra integridad del experimento, artifacts válidos,
replay equivalente y árbol trackeado limpio.

## 5. Evidencia local del root cause

La evidencia de runtime local fue inspeccionada por el Owner después del run.

Safe diagnostic persistido:

```text
component           engineering_inspect
reason_code         component_error
exception_type      RuntimeError
cause_chain_types   RuntimeError, HTTPError
origin_scope        repository
repo_relative_file  src/malak/runtime/ollama_runtime.py
function            generate
authority_effect    none
```

El log local de Ollama observado por el Owner registró:

```text
n_ctx = 8192
request = 20041 tokens
available context = 8192 tokens
HTTP POST /api/chat = 400
```

Mensaje material observado:

```text
request (20041 tokens) exceeds the available context size
(8192 tokens), try increasing it
```

Clasificación de esta evidencia:

```text
source:
local operator runtime evidence

repository-native evidence:
NO

authority:
none
```

No se utiliza como sustituto de candidate-bound CI ni como autoridad de cambio.
Sí constituye evidencia causal suficiente para preparar un nuevo admission
request-scoped.

## 6. Hipótesis descartadas por Fifth U01

La evidencia disponible no respalda atribuir el resultado a:

```text
parser de Engineering Inspect
Evidence Focus incompleto
respuesta vacía del modelo
done_reason=length
metadata de tokens ausente
thinking oculto
truncamiento silencioso
shift silencioso
```

La inferencia no produjo respuesta de modelo utilizable porque Ollama rechazó la
request antes de completarla.

## 7. Qué demostró el Runtime Generation Contract

Fifth U01 verificó en ejecución local que la request preservó:

```text
context_window_tokens = 8192
max_output_tokens     = 2048
thinking_enabled      = false
truncate              = false
shift                 = false
```

Runtime provenance observado:

```text
runtime_class             OllamaRuntime
runtime_version           0.33.3
requested_model           qwen3.5:9b
resolved_model            qwen3.5:9b
model_identity_strength   TAG_DIGEST_BOUND
declared_context_window   262144
context_window_source     ollama:model_info
provenance_status         READY
authority_effect          none
```

El rechazo por contexto insuficiente demuestra la propiedad deseada:

```text
insufficient requested context
+ truncate=false
+ shift=false
-> explicit failure
!= silent evidence loss
```

## 8. Candidate Generation Contract — Sixth U01

Nuevo candidato:

```text
context_window_tokens = 32768
max_output_tokens     = 2048
thinking_enabled      = false
truncate              = false
shift                 = false
```

No cambia el contrato productivo. Cambia únicamente la instancia request-scoped
seleccionada para este experimento.

## 9. Justificación cuantitativa

Fifth U01 observó:

```text
prompt/request tokens ≈ 20041
```

Reserva de output:

```text
2048
```

Mínimo aritmético observado:

```text
20041 + 2048 = 22089
```

Un candidato de `24576` dejaría aproximadamente:

```text
24576 - 20041 - 2048 = 2487 tokens
```

de margen, considerado demasiado estrecho para pequeñas variaciones del
Evidence Packet o del rendering.

Con `32768`:

```text
32768 - 20041 - 2048 = 10679 tokens
```

de margen aproximado respecto del run observado.

Además:

```text
32768 < declared_context_window 262144
```

por un margen amplio.

## 10. Por qué no se modifica el prompt todavía

El Fifth U01 aisló una restricción de recursos, no un defecto demostrado del
Evidence Focus.

Por tanto:

```text
no prompt compression
no evidence selector reduction
no evidence loss
no U01 scope reduction
no parser relaxation
```

se considera la corrección más pequeña que preserva la semántica del
experimento.

Si `32768` también resultara insuficiente:

```text
STOP
!= automatic context escalation
```

Cualquier nuevo budget requerirá nuevo admission humano.

## 11. Construction Flow aplicable

Este admission:

```text
does not change a critical contract
does not change production code
does not change architecture
does not change Kernel
does not change Planner
```

Por tanto:

```text
G1 new product design               N/A_WITH_REASON
Critical Contract Hardening         N/A_WITH_REASON
RED / GREEN product implementation  N/A_WITH_REASON
```

Sí aplican:

```text
G0 / admission
four questions of law
execution-profile 4R
Security Horizon check
RDD Stage 1 execution identity
candidate-bound CI
human review
Owner Ready / Merge
separate local preflight
separate explicit runtime authorization
```

## 12. Cuatro preguntas de ley

### 12.1 Blueprint

```text
PASS
```

- Kernel First permanece intacto.
- Capability First permanece intacto.
- runtime y modelo no reciben autoridad.
- Model Agnostic no cambia.
- Human in Control permanece obligatorio.

### 12.2 Constitución Cognitiva

```text
PASS
```

- evidencia observada conduce al nuevo candidate;
- no se inventa una causa alternativa;
- no se trunca evidencia para forzar success;
- el esfuerzo computacional sigue explícito y acotado;
- Generation != Acceptance permanece intacto.

### 12.3 Gobernanza

```text
PASS
```

- el Owner conserva autorización;
- este documento no autoriza ejecución;
- no existe auto-retry;
- no existe auto-escalamiento de recursos;
- merge continúa bajo autoridad humana.

### 12.4 Kernel

```text
UNCHANGED / PASS

Kernel delta = 0
```

## 13. Security Horizon Check

Sixth U01 continúa siendo:

```text
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
```

El incremento de contexto:

```text
changes resource budget
!= changes authority
```

## 14. Evidence Focus

U01 permanece exactamente:

```text
focus_id       U01
focus_label    U01 Core Kernel
subject        Kernel
```

No se modifican selectors.

Repository required selectors:

```text
PATH_PREFIX  src/malak/kernel/
EXACT_PATH   src/malak/services/planner.py
EXACT_PATH   src/malak/contracts/capability.py
EXACT_PATH   src/malak/app/composition.py
EXACT_PATH   tests/test_kernel.py
```

Knowledge required selectors permanecen los seis paths gobernados ya definidos
por el baseline.

Runtime deberá volver a demostrar:

```text
focus_complete == true
```

y continuidad de `evidence_set_digest` entre componentes que lleguen a
ejecutarse.

## 15. Runtime / model identity expectations

Expectativa basada en el preflight de Fifth U01:

```text
runtime_class             OllamaRuntime
runtime_version           0.33.3
model                     qwen3.5:9b
model_identity_strength   TAG_DIGEST_BOUND
declared_context_window   262144
context_window_source     ollama:model_info
provenance_status         READY
```

El digest exacto debe recapturarse localmente antes de Sixth U01.

No se reutiliza ciegamente el valor observado anteriormente.

Cualquier drift:

```text
STOP
-> review required
```

## 16. External configuration freeze

Candidate:

```powershell
$env:MALAK_RUNTIME = "ollama"
$env:MALAK_OLLAMA_MODEL = "qwen3.5:9b"
$env:MALAK_REPOSITORY_ROOT = "D:\Ollama\jarvis"
$env:MALAK_OLLAMA_CONTEXT_WINDOW_TOKENS = "32768"
$env:MALAK_OLLAMA_MAX_OUTPUT_TOKENS = "2048"
$env:MALAK_OLLAMA_THINKING = "disabled"
```

Base URL esperada:

```text
http://localhost:11434
```

## 17. Run identity propuesta

```text
run_id:
bootstrap-u01-20260926-006

task_id:
governed-self-review-bootstrap-v0

focus_id:
U01

focus_label:
U01 Core Kernel

engineering_subject:
Kernel
```

El run_id debe estar libre en preflight.

## 18. Validation refs propuestas

Mínimo:

```text
Validation#597
Validation#600
PR#197
PR#198
run@bootstrap-u01-20260926-005
reviewed-code@0794d5617eec354a66c41e271e7bf413d454b1a6
admission@<merged-sixth-admission-main-sha>
```

La referencia final del admission se completa después del merge humano.

## 19. Preflight local obligatorio

Antes de cualquier autorización de Sixth U01:

```text
branch == main
tracked tree == clean
HEAD == exact execution baseline
origin/main == HEAD
run_id unused

Python == official project environment
Ollama reachable locally
runtime version == expected reviewed version
qwen3.5:9b resolves
exact model digest captured
TAG_DIGEST_BOUND
declared_context_window >= 32768

generation contract:
context = 32768
output  = 2048
thinking = disabled
truncate = false
shift = false

provenance generation_options
==
requested generation contract
```

Cualquier mismatch:

```text
STOP
runtime execution remains NOT AUTHORIZED
```

## 20. Outcomes válidos

```text
NO_CHANGE_RECOMMENDED
HARDENING_PROPOSAL
RESEARCH_REQUIRED
DEFER
INCONCLUSIVE
```

También sigue siendo válido un component failure controlado.

Reglas:

```text
gap != authorization
proposal != implementation
acceptance PASS != cognitive PASS
INCONCLUSIVE != hidden success
model output != authority
```

## 21. Execution-profile 4R

### Risk — PASS WITH EXPLICIT PRECONDITIONS

Nuevo riesgo relativo:

```text
larger local context budget
-> higher resource consumption
```

Mitigación:

```text
fixed budget
single run
no retry
no auto-scaling
local only
Owner authorization
```

### Readability — PASS

El cambio es explícito:

```text
8192 -> 32768 context only
output remains 2048
thinking remains disabled
truncate remains false
shift remains false
```

### Reliability — PASS WITH LOCAL PREFLIGHT PENDING

La causa del Fifth U01 fue observada en runtime local y no se infiere desde
silencio.

Pendiente necesariamente del host:

```text
exact digest
runtime availability
current runtime version
current declared model context
exact main SHA
run_id availability
```

### Resilience — PASS

Ante:

```text
OOM
context exhaustion
HTTP failure
metadata failure
identity mismatch
baseline mismatch
dirty tree
focus incomplete
```

se requiere:

```text
fail closed
-> INCONCLUSIVE / STOP
-> no automatic retry
-> no automatic budget increase
-> no authority expansion
```

## 22. RDD Stage 1 execution identity

```text
reviewed baseline          explicit
future execution baseline  bound
run_id                     explicit
model                      explicit
generation contract        explicit
validation refs            explicit
resource delta             explicit
authority                  unchanged
```

Disposition:

```text
PASS FOR ADMISSION DESIGN
```

No autoriza runtime.

## 23. Deferred observability finding

Fifth U01 reveló que el safe diagnostic preservó:

```text
RuntimeError
HTTPError
component_error
```

pero no preservó el status HTTP `400`, aunque el runtime wrapper lo conocía.

Disposición:

```text
DEFERRED
out of Sixth U01 scope
```

Motivo:

```text
useful observability hardening
!= blocker for bounded resource admission
```

Debe evaluarse en un gate separado bajo el Construction Flow aplicable.

No se modifica producción desde este admission.

## 24. Admission Coverage Ledger

| Grupo | Artefactos / evidencia | Disposición |
|---|---|---|
| Repo baseline | main@0794d561... | CURRENT_STATE_REVALIDATED |
| Fifth admission | MALAK-FIFTH-U01-ADMISSION-REVIEW-20260926.md | HISTORICAL_REFERENCE |
| Fifth runtime result | bootstrap-u01-20260926-005 | OWNER_LOCAL_RUNTIME_EVIDENCE |
| Runtime contract | PR #197 / Validation #597 | CURRENT_STATE_REFERENCE |
| Fifth admission validation | PR #198 / Validation #600 | CURRENT_STATE_REFERENCE |
| Governance / security | baseline normative documents | CURRENT_STATE_REVALIDATED_BY_INHERITED_FLOW |
| U01 Evidence Focus | unchanged | CURRENT_STATE_PRESERVED |
| Observability finding | HTTP status not retained in safe diagnostic | DEFERRED |

Este review es incremental y acotado. No declara auditoría integral de Malāk.

## 25. Admission disposition

Antes de candidate-bound CI:

```text
Fifth U01 integrity                 PASS
Fifth U01 cognitive result         INCONCLUSIVE
root cause isolated                PASS
8192 budget                        REJECTED FOR U01
32768 candidate                    PREPARED
output 2048                        PRESERVED
thinking disabled                  PRESERVED
truncate=false                     PRESERVED
shift=false                        PRESERVED
Kernel delta                       0
Planner delta                      0
Evidence Focus delta               0
runtime contract delta             0
authority_effect                   none

admission candidate CI             PASS — Validation #602
local preflight                    NOT EXECUTED
runtime execution                  NOT AUTHORIZED
Sixth U01                          NOT AUTHORIZED
self-modification                  NOT AUTHORIZED
```

Admission result:

```text
CONDITIONAL PASS
```

Evidencia candidate-bound:

```text
candidate:
1233acc1b2751ed845374a6fe11dcefd9f3e0949

Validation #602:
Ubuntu   1578 passed
Windows  1578 passed
compile  PASS
diff     PASS
```

La corrección documental que registra este cierre cambia la identidad del
candidate y requiere una última Validation candidate-bound antes del merge.

## 26. Current authority state

```text
admission review       PREPARED
runtime execution      NOT AUTHORIZED
Sixth U01              NOT AUTHORIZED
self-modification      NOT AUTHORIZED
Ready                   OWNER ONLY
merge                   OWNER ONLY
authority_effect        none
```
