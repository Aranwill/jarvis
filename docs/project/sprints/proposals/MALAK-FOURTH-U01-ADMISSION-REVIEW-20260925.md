---
title: Malāk Fourth U01 Admission Review — 2026-09-25
status: proposed
authority: non_normative
document_role: admission_review
language: es
created: 2026-09-25
reviewed_code_baseline: 3122106b1d2c151e1085ef3ada1771bb8ea7ea96
execution_baseline_rule: current_main_with_admission_doc_only_delta
admission_result: conditional_pass
runtime_execution_authorized: false
fourth_u01_authorized: false
authority_effect: none
related:
  - docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md
  - docs/project/sprints/proposals/MALAK-THIRD-U01-ADMISSION-REVIEW-20260925.md
  - docs/project/sprints/proposals/MALAK-ANALYZE-STRUCTURED-OUTPUT-CONTRACT-V0-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-GOVERNED-ENGINEERING-EVIDENCE-FOCUS-V0-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-INTERNAL-INTERACTION-OBSERVABILITY-DIAGNOSTICS-MODEL-PROVENANCE-V0-G0-G1-DESIGN.md
  - src/malak/capabilities/_engineering_analysis.py
  - src/malak/capabilities/engineering_analyze.py
  - src/malak/runtime/ollama_runtime.py
  - src/malak/core/conversation.py
---

# Malāk Fourth U01 Admission Review — 2026-09-25

## 1. Propósito

Determinar si el baseline actual de Malāk está preparado para una cuarta
ejecución real y gobernada de:

```text
U01 — Core Kernel
```

sin ejecutar todavía el Self-Review.

Este gate responde únicamente:

```text
¿la causa material que volvió INCONCLUSIVE el Third U01
está cerrada con suficiente evidencia como para pedir
una nueva autorización de runtime?
```

No autoriza ejecución.

## 2. Baseline revisado

Baseline de código/runtime revisado:

```text
repository: Aranwill/jarvis
branch: main
reviewed_code_baseline:
3122106b1d2c151e1085ef3ada1771bb8ea7ea96

PR #194:
MERGED

open PRs observed at admission:
0

remote branches observed at admission:
main only
```

El merge integrado corresponde a:

```text
feat: endurecer structured output de Engineering Analyze
```

## 3. Binding correcto de ejecución

Este admission review no exige que el futuro runtime ejecute exactamente sobre
su commit padre después de integrar el propio documento.

Contrato:

```text
reviewed_code_baseline
= 3122106b1d2c151e1085ef3ada1771bb8ea7ea96

execution_baseline
= exact current main HEAD at local preflight
```

Después de integrar este admission review, la diferencia permitida entre
`reviewed_code_baseline` y `execution_baseline` es únicamente:

```text
docs/project/sprints/proposals/
MALAK-FOURTH-U01-ADMISSION-REVIEW-20260925.md
```

Cualquier otro path modificado:

```text
-> admission invalidated
-> STOP
-> new admission review required
```

## 4. Resultado del Third U01

Run:

```text
bootstrap-u01-20260925-003
```

Baseline:

```text
0ad053e83867aac54142f070150bf11d09cdcee8
```

Resultado material:

```text
Evidence Packet             READY
Inspect                     GROUNDED
focus_id                    U01
focus_complete              true
Analyze                     FAILED component_error
Propose                     SKIPPED precondition_not_met
terminal_disposition        INCONCLUSIVE
live_replay_equivalence     true
tracked_tree_clean          true
acceptance                  PASS
authority_effect            none
```

Runtime/model observado:

```text
runtime_class               OllamaRuntime
requested_model             qwen3.5:9b
resolved_model              qwen3.5:9b
model_identity_strength     TAG_DIGEST_BOUND
provenance_status           READY
```

## 5. Causa material aislada

Safe diagnostics del Third U01:

```text
component:           engineering_analyze
reason_code:         component_error
exception_type:      RuntimeError
cause_chain_types:   RuntimeError, JSONDecodeError
origin_scope:        repository
repo_relative_file:  src/malak/capabilities/_engineering_analysis.py
function:            parse_engineering_analysis
authority_effect:    none
```

Interpretación:

```text
evidence collection
-> succeeded

Inspect
-> succeeded

model invocation
-> occurred

Analyze parser
-> received model content
-> strict JSON parse failed
```

Por tanto, el gap no era:

```text
Evidence Focus
baseline binding
model presence
Ollama reachability
timeout
authority
```

El gap estaba en:

```text
machine-readable output contract
between Engineering Analyze and the LLM runtime
```

## 6. Structured Output V0 integrado

PR #194 integra un contrato provider-neutral:

```text
ConversationRequest.response_json_schema
```

Propiedades:

```text
optional
canonical JSON string
strict JSON object
duplicate keys rejected
non-finite constants rejected
64 KiB hard bound
immutable through frozen dataclass
authority_effect none
```

### OllamaRuntime

Si hay schema:

```text
response_json_schema
-> parse object
-> /api/chat payload["format"] = schema object
```

Si no hay schema:

```text
no format field
-> previous generic behavior preserved
```

### MockLLMRuntime

```text
schema requested
-> FAIL CLOSED
```

No ignora silenciosamente el contrato.

## 7. Ownership de policy

Durante FULL 4R se detectó un scope leak real.

Primer GREEN candidate:

```text
run_engineering_analysis()
-> hardcoded schema
```

Como ese helper es compartido por E3 y E4, el efecto habría sido:

```text
E3 Analyze
-> structured output

E4 internal analysis
-> structured output también
```

Eso violaba el scope congelado.

Corrección integrada:

```text
shared run_engineering_analysis()
-> response_json_schema: str | None = None
-> policy neutral

EngineeringAnalyzeCapability
-> explicit ANALYZE_RESPONSE_JSON_SCHEMA

EngineeringProposeCapability
-> internal analysis schema = None
-> proposal schema = None
```

Regla arquitectónica resultante:

```text
shared utility
!= policy owner

Capability requiring structured output
-> must declare it explicitly
```

## 8. Parser semántico preservado

Structured Output no sustituye la validación de Malāk.

Se preserva:

```text
json.loads strict parsing
duplicate-key rejection
non-finite rejection
exact top-level keys
exact finding keys
classification allow-list
actual evidence ref validation
R + K requirement
duplicate evidence ref rejection
hard finding bounds
hard evidence ref bounds
hard uncertainty bounds
UTF-8 byte bounds
reserved-token protections
```

Por tanto:

```text
provider-native schema accepted
!=
analysis accepted by Malāk
```

La respuesta real debe seguir pasando todos los validadores semánticos.

## 9. Prohibiciones preservadas

No se agregó:

```text
markdown fence stripping
regex JSON extraction
automatic retry
"repair your JSON" retry
silent fallback to unconstrained generation
raw model response persistence
temperature change
sampling change
model change
authority expansion
```

## 10. RED evidence

Validation #550:

```text
candidate:
6d113047f3413c0d56f00116b3a529d2d3b32c35

Ubuntu:
5 failed / 1537 passed

Windows:
5 failed / 1537 passed
```

Fallas esperadas:

```text
S01 ConversationRequest lacked response_json_schema
S02 OllamaRuntime lacked format mapping
S03 Analyze did not attach response schema
S06 provider/runtime path did not surface unsupported schema
S07 MockLLMRuntime did not fail closed
```

Controles verdes:

```text
S04 malformed model JSON still failed strict parser
S05 ordinary Ollama request still had no format
```

No se observaron fallas no relacionadas.

## 11. GREEN validations

Validation #559:

```text
candidate:
dd2dabf124f4bd11ff45cab6f4b894a536fa8143

Ubuntu:  1553 passed
Windows: 1553 passed
```

FULL 4R posterior detectó el scope leak E4 descrito arriba.

Validation #563 sobre la corrección:

```text
candidate:
83a9e8cd2e2ab5d680132181dab940db2580280f

Ubuntu:  1553 passed
Windows: 1553 passed
```

Validation #565, candidate final:

```text
candidate:
0ae883176a17fac8b9b39ed10b2a4ca786efbbcc

Ubuntu:  1554 passed
Windows: 1554 passed
```

Merge integrado:

```text
3122106b1d2c151e1085ef3ada1771bb8ea7ea96
```

## 12. E2E / conformance

El candidate final incluye un E2E determinista que recorre:

```text
EngineeringAnalyzeCapability
-> ConversationService
-> RuntimeConversationProvider
-> OllamaRuntime
-> /api/chat format=<schema>
-> JSON model response
-> existing strict semantic parser
-> GROUNDED envelope
```

También prueba:

```text
schema bounds
-> tied to real E3 constants

generic conversation
-> no format

E4
-> no structured output in this slice
```

## 13. Anti-relaxation review

Comparación contra el baseline previo:

```text
prior test assertions removed       0
prior pytest.raises removed         0
strict parser relaxed               NO
JSON repair added                   NO
automatic retry added               NO
raw response persistence added      NO
sampling changed                    NO
Kernel delta                        0
Planner delta                       0
authority expansion                 0
```

Disposition:

```text
PASS
```

## 14. U01 Evidence Focus impact

PR #194 no modificó los paths requeridos por los selectores U01 revisados en el
Third U01 admission.

El delta de producción se limitó a:

```text
src/malak/capabilities/_engineering_analysis.py
src/malak/capabilities/engineering_analyze.py
src/malak/core/conversation.py
src/malak/runtime/mock_llm_runtime.py
src/malak/runtime/ollama_runtime.py
```

Ninguno pertenece a los required selector paths U01 previamente admitidos:

```text
src/malak/kernel/
src/malak/services/planner.py
src/malak/contracts/capability.py
src/malak/app/composition.py
tests/test_kernel.py
docs/architecture/blueprint.md
docs/architecture/architecture_quality_gates.md
docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md
MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1-BATCH-D.md
```

Por tanto:

```text
prior static selector review
-> no selector path invalidated by PR #194
```

Importante:

```text
static path review
!= runtime focus_complete proof
```

La prueba definitiva sigue siendo el run.

## 15. Runtime evidence requirements

Fourth U01 debe mantener:

```text
SelfReviewEvidencePacket READY
AND
U01 focus_complete == true
AND
Inspect evidence_set_digest
==
Analyze evidence_set_digest
==
Propose evidence_set_digest, if Propose runs
```

No se exige igualdad del digest con el Third U01.

Se exige continuidad interna del Fourth U01.

Cualquier incumplimiento:

```text
-> INCONCLUSIVE
-> STOP
```

## 16. Runtime/model preconditions

Antes de ejecutar:

```text
branch == main
tracked working tree == clean

diff reviewed_code_baseline..HEAD
-> only this admission-review document

current HEAD
-> exact execution_baseline

MALAK_RUNTIME == ollama
MALAK_OLLAMA_MODEL == qwen3.5:9b
MALAK_REPOSITORY_ROOT -> exact repository
local Ollama reachable
qwen3.5:9b resolves locally
model_identity_strength == TAG_DIGEST_BOUND
run_id unused
```

El uso de `qwen3.5:9b` preserva comparabilidad causal con el Third U01.

Si cualquiera falla:

```text
STOP
```

## 17. Model provenance limitation

Se mantiene:

```text
TAG_DIGEST_BOUND
= local requested/resolved tag
+ local digest observed at provenance capture
```

No significa:

```text
served-response cryptographic attestation
```

Sigue siendo aceptable únicamente para este experimento:

```text
local
single-host
read-only
no side-effect tools
no delegation
no PDW
no authority derived from model
Owner-end review
authority_effect none
```

No resuelve RR-03.

## 18. Run identity propuesta

Si el Owner autoriza runtime después de integrar este admission review:

```text
run_id:
bootstrap-u01-20260925-004

task_id:
governed-self-review-bootstrap-v0

focus_id:
U01

focus_label:
U01 Core Kernel

engineering_subject:
Kernel
```

Validation refs:

```text
Validation#550
Validation#559
Validation#563
Validation#565
PR#194
reviewed-code@3122106b1d2c151e1085ef3ada1771bb8ea7ea96
```

## 19. Valid outcomes

Fourth U01 no necesita producir una mejora.

Outcomes válidos:

```text
NO_CHANGE_RECOMMENDED
HARDENING_PROPOSAL
RESEARCH_REQUIRED
DEFER
INCONCLUSIVE
```

Reglas:

```text
GAP != authorization
proposal != implementation
INCONCLUSIVE != hidden failure
NO_CHANGE_RECOMMENDED != weak result
```

## 20. Bootstrap boundary

Fourth U01 sigue ejecutando únicamente:

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
Fourth U01 success
!= bootstrap complete
```

## 21. Security / authority

No cambia:

```text
Kernel authority
Planner authority
SecurityContext
Memory
Knowledge admission
Trace schema
Protected Durable Write
merge authority
```

Permitido durante un futuro Fourth U01 autorizado:

```text
read exact Git baseline
read governed Knowledge
read-only Ollama provenance introspection
local Ollama inference
runtime/internal_interaction/<run_id> artifacts
LIVE projection
REPLAY
```

Prohibido:

```text
tracked production edits
git add / commit / push
branch creation
PR creation
network research
model pull/update/delete
agent creation
scheduler
Memory mutation
Knowledge mutation
self-approval
self-merge
```

## 22. Admission 4R

### Risk — PASS WITH BOUNDED LIMITATION

La causa material del Third U01 tiene ahora enforcement estructural en runtime y
validación semántica independiente en Malāk.

Limitación residual:

```text
TAG_DIGEST_BOUND
!= served-response cryptographic attestation
```

### Readability — PASS

La frontera queda separada:

```text
Capability declares response contract
Runtime maps provider mechanism
Parser validates semantic contract
Owner retains authority
```

### Reliability — PASS

Se dispone de:

```text
exact baseline guard
clean-tree guard
Evidence Focus completeness
evidence digest continuity
structured output request
strict semantic validation
safe diagnostics
runtime provenance
LIVE / REPLAY equivalence
terminal disposition
```

### Resilience — PASS

Ante incapacidad del runtime o output inválido:

```text
fail closed
-> diagnostic / INCONCLUSIVE
-> no repair
-> no fallback
-> no authority
```

## 23. Admission disposition

```text
Third U01 cause isolated              PASS
Structured Output V0 integrated       PASS
RED evidence                          PASS
GREEN candidate-bound CI              PASS
FULL 4R                               PASS
anti-relaxation                       PASS
scope leak                            CLOSED
E2E/conformance                       PASS
U01 selector paths unaffected         PASS
authority expansion                   0
runtime execution                     NOT AUTHORIZED

ADMISSION RESULT:
CONDITIONAL PASS
```

Condición restante:

```text
Owner must review and merge this admission document
then explicitly authorize Fourth U01 runtime
then local preflight must PASS
```

## 24. Current authority state

```text
admission review             PREPARED
runtime execution            NOT AUTHORIZED
Fourth U01                   NOT AUTHORIZED
self-modification            NOT AUTHORIZED
merge                        OWNER ONLY
authority_effect             none
```
