---
title: Malāk Fifth U01 Admission Review — 2026-09-26
status: proposed
authority: non_normative
document_role: admission_review
language: es
created: 2026-09-26
reviewed_code_baseline: c67485cee7b19571426f05747a8620c374da7f5b
execution_baseline_rule: current_main_with_admission_doc_only_delta
admission_result: conditional_pass
risk_class: high_bounded_local_runtime
runtime_execution_authorized: false
fifth_u01_authorized: false
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
  - docs/project/sprints/proposals/MALAK-FOURTH-U01-ADMISSION-REVIEW-20260925.md
  - docs/project/sprints/proposals/MALAK-ENGINEERING-RUNTIME-GENERATION-CONTRACT-V0-G0-G1-DESIGN.md
  - src/malak/app/internal_interaction_test_v0.py
  - src/malak/runtime/runtime_generation_contract.py
  - src/malak/runtime/ollama_runtime.py
  - src/malak/capabilities/_engineering_evidence.py
---

# Malāk Fifth U01 Admission Review — 2026-09-26

## 1. Propósito

Determinar si el baseline actual de Malāk está preparado para solicitar una quinta
ejecución real, local y gobernada de:

```text
U01 — Core Kernel
```

después de integrar **Engineering Runtime Generation Contract V0**.

Este documento:

```text
NO ejecuta Self-Review
NO autoriza runtime
NO autoriza self-modification
NO autoriza cambios productivos
NO concede autoridad al modelo
NO autoriza merge automático
```

Su único efecto es preparar un admission reproducible y auditable para revisión
humana.

## 2. Baseline revisado

Baseline material revisado:

```text
repository: Aranwill/jarvis
branch: main
reviewed_code_baseline:
c67485cee7b19571426f05747a8620c374da7f5b

PR #197:
MERGED

open PRs observed before admission branch:
0

main compared with merge commit:
IDENTICAL
```

El merge integrado corresponde a:

```text
feat: implementar contrato de generación gobernada
```

## 3. Binding de ejecución

La ejecución futura no debe reutilizar ciegamente el baseline revisado si el
propio documento de admission fue integrado después.

Regla:

```text
reviewed_code_baseline
= c67485cee7b19571426f05747a8620c374da7f5b

execution_baseline
= exact current main HEAD at local preflight
```

Después de integrar este admission review, el único delta permitido entre
`reviewed_code_baseline` y `execution_baseline` es:

```text
docs/project/sprints/proposals/
MALAK-FIFTH-U01-ADMISSION-REVIEW-20260926.md
```

Cualquier otro path modificado:

```text
-> admission invalidated
-> STOP
-> new admission review required
```

## 4. Evidencia de origen — Fourth U01

Run anterior:

```text
run_id                     bootstrap-u01-20260925-004
execution_baseline         7ab94f7bfd15a3fbf5f23a09db0d84a95a47b032
Evidence Packet            READY
Inspect                    component_error
Analyze                    SKIPPED / precondition_not_met
Propose                    SKIPPED / precondition_not_met
terminal_disposition       INCONCLUSIVE
live_replay_equivalence    true
tracked_tree_clean         true
acceptance                 PASS
authority_effect           none
```

Safe diagnostic:

```text
component              engineering_inspect
reason_code            component_error
exception_type         RuntimeError
repo_relative_file     src/malak/capabilities/engineering_inspect.py
function               execute
```

La validación fail-closed de contenido final vacío funcionó correctamente y fue
preservada.

## 5. Causa material aislada del Fourth U01

Durante el run se observó aproximadamente:

```text
runner context          4096
prompt tokens           2050
generated tokens        2046
sum                     4096
runner truncated        1
HTTP                    200
```

La provenance del mismo run declaraba:

```text
runtime_class              OllamaRuntime
requested_model            qwen3.5:9b
resolved_model             qwen3.5:9b
model_identity_strength    TAG_DIGEST_BOUND
declared_context_window    262144
context_window_source      ollama:model_info
generation_options         {}
provenance_status          READY
authority_effect           none
```

Interpretación admitida:

```text
declared model capacity
!=
effective request context
```

La request delegaba contexto, output budget y thinking policy a defaults externos.

## 6. Cierre material integrado por PR #197

El baseline actual contiene:

```text
RuntimeGenerationContract
-> immutable / provider-neutral

ConversationRequest
-> request-scoped generation_contract

Engineering composition
-> same contract through E2 / E3 / E4
-> same identity preserved through focused rebuild

OllamaRuntime
-> options.num_ctx
-> options.num_predict
-> think
-> truncate=false
-> shift=false

runtime provenance
-> exact requested generation_options

Self-Review harness
-> generation contract required
-> provenance contract match required
```

Fail-closed integrado:

```text
done != true                    -> reject
done_reason=length              -> reject
missing prompt_eval_count       -> reject
missing eval_count              -> reject
invalid token counts            -> reject
eval_count > output budget      -> reject
total tokens > context budget   -> reject
thinking-disabled violation     -> reject
```

No se agregó:

```text
automatic retry
automatic context increase
automatic thinking switch
raw response persistence
raw thinking persistence
authority expansion
```

## 7. Evidencia de validación del contrato

Final candidate de PR #197:

```text
d8cd8fcbdba7d1d104a35716621a25677423b308
Validation #597
```

Resultado:

```text
Ubuntu:  1578 passed
Windows: 1578 passed

compile Python sources: PASS
candidate identity:      PASS
candidate diff:          PASS
review threads:          0
```

Hardening adicional validado:

```text
G15 requested context > declared model context -> reject
G16 invalid / excess provider token counts     -> reject
G17 missing completion token metadata          -> reject
```

E2E determinista validado:

```text
EngineeringAnalyzeCapability
-> ConversationService
-> RuntimeConversationProvider
-> OllamaRuntime
-> Structured Output
-> RuntimeGenerationContract
-> completion metadata validation
-> existing strict parser
-> GROUNDED
```

## 8. Construction Flow aplicable

Este admission no crea ni modifica un contrato crítico.

El contrato material fue diseñado, endurecido, probado, revisado y mergeado en
el gate anterior.

Disposición para este admission:

```text
G0 / admission                    THIS DOCUMENT
G1 new design                     N/A_WITH_REASON
Critical Contract Hardening       N/A_WITH_REASON
RED / GREEN product change        N/A_WITH_REASON
```

Razón:

```text
no product contract delta
no architecture delta
no Kernel delta
no Planner delta
execution reuses merged RuntimeGenerationContract V0
```

Sí aplican:

```text
cuatro preguntas de ley
execution-profile 4R
Security Horizon check
RDD Stage 1 execution identity check
candidate-bound validation of this admission document
human review
Owner Ready / Merge
separate explicit runtime authorization
local preflight
```

Tests verdes del gate anterior no constituyen por sí solos autorización de
runtime.

## 9. Cuatro preguntas de ley

### 9.1 ¿Respeta el Blueprint?

```text
PASS
```

Motivo:

- preserva Kernel First;
- preserva Capability First;
- el runtime no se convierte en autoridad;
- mantiene Human in Control;
- no introduce acoplamiento del Kernel con Ollama;
- la política de recursos queda fuera del Kernel y request-scoped.

### 9.2 ¿Respeta la Constitución Cognitiva?

```text
PASS
```

Motivo:

- evidencia verificable prevalece sobre inferencia;
- output de modelo no equivale a aceptación ni autoridad;
- presupuesto computacional queda explícito y acotado;
- failure / missing metadata termina fail-closed;
- no se completa evidencia ausente mediante invención.

### 9.3 ¿Respeta la Gobernanza?

```text
PASS
```

Motivo:

- Owner conserva autorización operativa;
- ejecución sensible requiere aprobación separada;
- no hay auto-promoción ni auto-merge;
- autoridad del modelo permanece en cero;
- run y artifacts quedan trazables.

### 9.4 ¿Hace al Kernel más simple o más complejo?

```text
UNCHANGED / PASS
```

Este admission no modifica el Kernel.

```text
Kernel delta = 0
```

## 10. Security Horizon Check

El próximo run continúa limitado a un experimento:

```text
local
single-host
read-only over tracked baseline
local Ollama inference
no tools
no agents
no network research
no model pull/update/delete
no Memory mutation
no Knowledge mutation
no tracked production edit
no self-modification
authority_effect none
```

Compatibilidad con SECURITY.md:

```text
Model != System
Intelligence != Authority
Execution != Evidence
Evidence != Authority
```

Compatibilidad con Research Horizon:

```text
Resource Governance             ALIGNED
Governed Self-Improvement       ALIGNED
Autonomous self-modification    FORBIDDEN / unchanged
new interoperability surface    none
new agent surface               none
new tool surface                none
```

## 11. U01 Evidence Focus re-review

El selector U01 vigente fue revisado nuevamente porque PR #197 modificó
`src/malak/app/composition.py`, que pertenece al evidence set requerido.

Focus vigente:

```text
focus_id       U01
focus_label    U01 Core Kernel
subject        Kernel
```

Repository required selectors:

```text
PATH_PREFIX  src/malak/kernel/
EXACT_PATH   src/malak/services/planner.py
EXACT_PATH   src/malak/contracts/capability.py
EXACT_PATH   src/malak/app/composition.py
EXACT_PATH   tests/test_kernel.py
```

Knowledge required selectors:

```text
docs/architecture/blueprint.md
docs/architecture/architecture_quality_gates.md
docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md
docs/project/status/MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1-BATCH-D.md
```

Estado estático observado en `main@c67485c...`:

```text
kernel prefix exists                       PASS
all repository EXACT_PATH exist            PASS
all knowledge EXACT_PATH exist             PASS
composition selector remains addressable   PASS
```

Esto no sustituye la prueba runtime:

```text
focus_complete == true
```

ni la continuidad:

```text
Inspect evidence_set_digest
==
Analyze evidence_set_digest
==
Propose evidence_set_digest, if Propose runs
```

## 12. Candidate Generation Contract para Fifth U01

Se selecciona como candidato de ejecución:

```text
context_window_tokens = 8192
max_output_tokens     = 2048
thinking_enabled      = false
truncate              = false
shift                 = false
```

### 12.1 Justificación de contexto

Fourth U01 agotó aproximadamente:

```text
2050 prompt
+ 2046 generated
= 4096
```

Con el candidato:

```text
8192 total context
- 2048 max output
= 6144 tokens disponibles para input / prompt / history
```

Esto:

- duplica el contexto efectivo que falló;
- conserva un output budget acotado;
- evita adaptar silenciosamente la request;
- no implementa escalamiento automático;
- no establece una política universal para todo Malāk.

Si el input real no cabe bajo el contrato:

```text
STOP
!= retry with larger context
```

### 12.2 Justificación de thinking disabled

La evidencia upstream revisada para Ollama v0.33.3 mostró que Qwen 3.5 puede
habilitar thinking cuando `think` se omite.

Para este run:

```text
thinking_enabled=false
```

reduce ambigüedad material sobre consumo del budget y exige contenido final
observable.

Esto no crea una ley global:

```text
Fifth U01 experiment policy
!= universal Engineering thinking policy
```

## 13. Runtime / model identity preconditions

Valores esperados por continuidad causal con Fourth U01:

```text
MALAK_RUNTIME                 ollama
MALAK_OLLAMA_MODEL            qwen3.5:9b
runtime_class                 OllamaRuntime
runtime_version               0.33.3
declared_context_window       262144
model_identity_strength       TAG_DIGEST_BOUND
provenance_status             READY
```

El digest exacto del modelo no se inventa en este documento porque no está
persistido como valor recuperable en el baseline oficial revisado.

Por tanto, antes de autorizar la ejecución:

```text
local preflight
-> capture exact model digest
-> confirm qwen3.5:9b resolves
-> confirm TAG_DIGEST_BOUND
-> confirm runtime_version == 0.33.3
-> confirm declared_context_window == 262144
-> Owner reviews exact preflight identity
-> only then runtime may be explicitly authorized
```

Si runtime version, model digest binding o declared context no coinciden con la
expectativa:

```text
STOP
-> admission identity changed
-> review required
```

## 14. External configuration freeze

Para Fifth U01:

```powershell
$env:MALAK_RUNTIME = "ollama"
$env:MALAK_OLLAMA_MODEL = "qwen3.5:9b"
$env:MALAK_REPOSITORY_ROOT = "D:\Ollama\jarvis"
$env:MALAK_OLLAMA_CONTEXT_WINDOW_TOKENS = "8192"
$env:MALAK_OLLAMA_MAX_OUTPUT_TOKENS = "2048"
$env:MALAK_OLLAMA_THINKING = "disabled"
```

`MALAK_OLLAMA_BASE_URL` puede permanecer en el default local:

```text
http://localhost:11434
```

si el preflight demuestra que corresponde al runtime local esperado.

No se admite configuración parcial del generation contract.

## 15. Run identity propuesta

Después de merge humano del admission, autorización explícita de runtime y
preflight PASS:

```text
run_id:
bootstrap-u01-20260926-005

task_id:
governed-self-review-bootstrap-v0

focus_id:
U01

focus_label:
U01 Core Kernel

engineering_subject:
Kernel
```

El `run_id` debe estar libre antes de ejecutar.

## 16. Validation refs propuestas

El comando futuro debe incluir referencias externas no vacías y trazables.

Mínimo:

```text
Validation#597
PR#197
reviewed-code@c67485cee7b19571426f05747a8620c374da7f5b
admission@<merged-admission-main-sha>
```

El SHA final del admission sólo puede completarse después del merge humano.

## 17. Preflight local obligatorio

Antes de ejecutar:

```text
branch == main
tracked working tree == clean
HEAD == exact execution_baseline
diff reviewed_code_baseline..HEAD
-> only admission document

Python == official project environment
Ollama reachable locally
runtime version == 0.33.3
qwen3.5:9b resolves locally
exact model digest captured
model_identity_strength == TAG_DIGEST_BOUND
declared_context_window == 262144

RuntimeGenerationContract:
context = 8192
output  = 2048
thinking = disabled
truncate = false
shift = false

run_id unused
```

Cualquier fallo:

```text
STOP
runtime execution remains NOT AUTHORIZED
```

## 18. Ejecución futura — comando reproducible

Después de autorización explícita del Owner, iniciar la CLI desde la raíz oficial:

```powershell
.\.venv\Scripts\python.exe -m malak.app.cli
```

Dentro de la CLI:

```text
/self-review test-v0 bootstrap-u01-20260926-005 Validation#597 PR#197 reviewed-code@c67485cee7b19571426f05747a8620c374da7f5b admission@<merged-admission-main-sha>
```

Este documento no autoriza ejecutar ese comando todavía.

## 19. Runtime acceptance invariants

La ejecución debe preservar:

```text
SelfReviewEvidencePacket READY
U01 focus_complete == true
same execution baseline through run
same generation contract through E2/E3/E4
runtime provenance generation_options == requested contract
TAG_DIGEST_BOUND model identity
completion token metadata present
completion token counts inside requested budgets
LIVE final material projection == REPLAY
tracked tree clean
authority_effect == none
```

Si Propose no corre por una precondición legítima, el resultado puede continuar
siendo `INCONCLUSIVE`; no debe fabricarse success.

## 20. Outcomes válidos

```text
NO_CHANGE_RECOMMENDED
HARDENING_PROPOSAL
RESEARCH_REQUIRED
DEFER
INCONCLUSIVE
```

Reglas:

```text
gap != authorization
proposal != implementation
INCONCLUSIVE != hidden failure
NO_CHANGE_RECOMMENDED != weak result
model output != accepted truth
```

## 21. Bootstrap boundary

Fifth U01 ejecuta únicamente:

```text
U01
```

Aunque termine satisfactoriamente:

```text
U04   NOT EXECUTED
RR-03 NOT EXECUTED
```

Por tanto:

```text
Fifth U01 success
!= bootstrap complete
```

## 22. Execution-profile 4R

### Risk — PASS WITH EXPLICIT PRECONDITIONS

Riesgo principal:

- runtime LLM real;
- model identity local, no served-response cryptographic attestation;
- consumo de recursos local;
- output probabilístico.

Mitigaciones:

- no tools ni side effects externos;
- generation contract explícito;
- fail-closed;
- Evidence Focus gobernado;
- owner authorization separada;
- authority zero.

Limitación residual:

```text
TAG_DIGEST_BOUND
!= served-response cryptographic attestation
```

### Readability — PASS

La frontera permanece explícita:

```text
Owner
-> authorizes run

CLI
-> external policy values

Engineering composition
-> one immutable generation contract

Capability
-> declares request policy

OllamaRuntime
-> maps provider mechanism

Harness
-> validates provenance and run invariants

Model
-> produces candidate output only
```

### Reliability — PASS WITH LOCAL PREFLIGHT PENDING

Disponible:

- exact reviewed baseline;
- U01 static selector re-review;
- Validation #597;
- deterministic E2E;
- G15/G16/G17;
- clean-tree guard;
- evidence digest continuity;
- provenance capture.

Pendiente necesariamente del host local:

- exact digest;
- runtime reachability;
- exact runtime version;
- declared model context;
- execution HEAD.

### Resilience — PASS

Ante cualquier incapacidad:

```text
missing metadata
budget exhaustion
context overrun
thinking violation
identity weakness
focus incomplete
component error
baseline mismatch
dirty tree
```

la disposición requerida es:

```text
fail closed
-> INCONCLUSIVE / STOP
-> no retry
-> no self-healing
-> no authority expansion
```

## 23. RDD Stage 1 execution identity check

```text
candidate identity              explicit
reviewed baseline               explicit
future execution baseline       bound by rule
generation contract             explicit
run_id                          explicit
validation refs                 explicit
runtime/model expectations      explicit
evidence != authority           preserved
human authority                 preserved
```

Disposition:

```text
PASS FOR ADMISSION DESIGN
```

No constituye runtime authorization.

## 24. Admission Coverage Ledger

Alcance revisado deliberadamente:

| Grupo | Artefactos | Profundidad | Disposición |
|---|---|---|---|
| Reglas de repo | `AGENTS.md` | targeted/full applicable rules | CURRENT_STATE_REVALIDATED |
| Método | Construction Protocol, Development Checklist, Engineering Method | targeted | CURRENT_STATE_REVALIDATED |
| Normativo | Blueprint, Cognitive Constitution, Governance Constitution, Architecture Quality Gates, SECURITY.md | targeted | CURRENT_STATE_REVALIDATED |
| Horizon | Research Horizon Map, concepts README, Governed Self-Review Bootstrap Task | targeted | CONCEPTUAL / NON_NORMATIVE |
| Evidencia histórica | Fourth U01 Admission, Runtime Generation Contract design | targeted | HISTORICAL_REFERENCE |
| Runtime contract | conversation, runtime generation contract, Ollama runtime, provenance, CLI, composition | targeted/code | CURRENT_STATE_REVALIDATED |
| Self-Review | InternalInteractionTestV0Harness + CLI binding | targeted/code | CURRENT_STATE_REVALIDATED |
| Evidence Focus | `_engineering_evidence.py` U01 selector catalog | targeted/code | CURRENT_STATE_REVALIDATED |
| U01 repository selectors | kernel prefix, planner, capability contract, composition, test_kernel | structural/targeted | RESOLVED |
| U01 knowledge selectors | six exact governed paths | structural/targeted | RESOLVED |
| PR #197 validation | Validation #597 / 1578 tests both runners | evidence | CURRENT_STATE_REVALIDATED |

Este es un review incremental del runtime admission; no se declara auditoría
integral/transversal de todo Malāk.

## 25. Admission disposition

Estado antes de validar este candidate documental:

```text
Fourth U01 cause isolated                 PASS
Runtime Generation Contract V0 merged     PASS
G15 / G16 / G17                           PASS
candidate-bound CI #597                   PASS
deterministic E2E                         PASS
U01 selector static re-review             PASS
four questions of law                     PASS
Security Horizon check                    PASS
execution-profile 4R                      PASS
RDD Stage 1 execution identity check      PASS

admission document candidate CI           PASS — Validation #599
local runtime preflight                    NOT EXECUTED
runtime execution                          NOT AUTHORIZED
Fifth U01                                  NOT AUTHORIZED
self-modification                          NOT AUTHORIZED
authority_effect                           none
```

Admission result:

```text
CONDITIONAL PASS
```

Evidencia candidate-bound:

```text
candidate:
d6af5131b39b31839f0aca421d2fd79049617694

Validation #599:
Ubuntu   1578 passed
Windows  1578 passed
compile  PASS
diff     PASS
```

La corrección documental que registra este cierre cambia la identidad del
candidate y requiere una última Validation candidate-bound antes del merge.

Condiciones restantes:

```text
Owner reviews and merges admission
-> exact main baseline confirmed
-> local preflight PASS
-> Owner reviews exact local runtime/model identity
-> Owner explicitly authorizes Fifth U01
-> run
-> STOP after result for human review
```

## 26. Current authority state

```text
admission review             PREPARED
runtime execution            NOT AUTHORIZED
Fifth U01                    NOT AUTHORIZED
self-modification            NOT AUTHORIZED
Ready                        OWNER ONLY
merge                        OWNER ONLY
authority_effect             none
```
