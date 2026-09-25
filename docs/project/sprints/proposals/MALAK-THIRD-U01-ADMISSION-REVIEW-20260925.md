---
title: Malāk Third U01 Admission Review — 2026-09-25
status: proposed
authority: non_normative
document_role: admission_review
language: es
created: 2026-09-25
baseline_commit: 07e667d669352d8cb0974dbbbcb017fa4ea7d979
reviewed_code_baseline: 07e667d669352d8cb0974dbbbcb017fa4ea7d979
admission_merge_observed: 32ad7e49513c5c96d7f66b1084544feb4531d667
execution_baseline_rule: current_main_with_admission_doc_only_delta
admission_result: conditional_pass
runtime_execution_authorized: false
third_u01_authorized: false
authority_effect: none
related:
  - docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md
  - docs/project/sprints/proposals/MALAK-INTERNAL-INTERACTION-TEST-V0-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-GOVERNED-ENGINEERING-EVIDENCE-FOCUS-V0-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-INTERNAL-INTERACTION-OBSERVABILITY-DIAGNOSTICS-MODEL-PROVENANCE-V0-G0-G1-DESIGN.md
  - src/malak/app/internal_interaction_test_v0.py
  - src/malak/capabilities/_engineering_evidence.py
  - src/malak/runtime/ollama_runtime.py
  - src/malak/runtime/runtime_provenance.py
---

# Malāk Third U01 Admission Review — 2026-09-25

## 1. Propósito

Determinar si el baseline actual de Malāk está preparado para una tercera
ejecución real y gobernada del slice:

```text
U01 — Core Kernel
```

sin ejecutar todavía el Self-Review.

Este gate no autoriza runtime. Su función es responder:

```text
¿las causas que bloquearon los dos runs anteriores están cerradas
con suficiente evidencia como para pedir autorización de ejecución?
```

## 2. Baseline revisado y binding de ejecución

El baseline de código/runtime evaluado por este admission review es:

```text
repository: Aranwill/jarvis
branch: main
reviewed_code_baseline:
07e667d669352d8cb0974dbbbcb017fa4ea7d979

open PRs observed at admission: 0
remote branches observed at admission: main only
```

La integración de este mismo admission review produjo después:

```text
admission_merge_observed:
32ad7e49513c5c96d7f66b1084544feb4531d667
```

Entre `reviewed_code_baseline` y ese merge se observó únicamente:

```text
docs/project/sprints/proposals/
MALAK-THIRD-U01-ADMISSION-REVIEW-20260925.md
```

sin cambios de código, tests, configuración ni runtime.

Esto cierra una propiedad auto-referencial del gate: un documento trackeado no
puede exigir que `HEAD` siga siendo su commit padre después de ser mergeado.

Por tanto, el contrato correcto es:

```text
reviewed_code_baseline
-> congela el código/runtime admitido

execution_baseline
-> exact current main HEAD at local preflight
-> captured by Engineering / artifacts
-> may differ from reviewed_code_baseline only through this admission-review
   document
```

Cualquier otro path modificado desde `reviewed_code_baseline`:

```text
-> admission invalidated
-> STOP
-> new admission review required
```

Integraciones previas relevantes:

```text
Governed Engineering Evidence Focus V0    INTEGRATED
OBS-01 Live Elapsed                       INTEGRATED
OBS-02 Safe Diagnostics                   INTEGRATED
Runtime / Model Provenance V0             INTEGRATED
Validation #541                           1535 PASS Ubuntu / Windows
```

## 3. Historial causal

### Run 1

```text
bootstrap-u01-20260923-001

Inspect
-> COMPONENT_FAILED
-> generic component_error
-> causa técnica perdida
-> terminal INCONCLUSIVE
```

Gap asociado:

```text
OBS-02
```

Estado actual:

```text
CLOSED
-> diagnostic ref
-> diagnostics.jsonl
-> safe cause
-> repo-relative origin when demonstrable
-> attestation
```

### Run 2

```text
bootstrap-u01-20260923-002

Inspect
-> GROUNDED

evidence
-> repository 12
-> knowledge 12
-> context_truncated=true

Analyze
-> UNCONFIRMED
-> complete evidence required

Propose
-> NOT EXECUTED

terminal
-> INCONCLUSIVE
```

Gaps asociados:

```text
EVID-01
EVID-02
```

Estado actual:

```text
CLOSED AT IMPLEMENTATION LEVEL
-> governed U01 evidence focus
-> deterministic required selectors
-> explicit completeness
-> evidence_set_digest
-> same evidence identity across Inspect / Analyze / Propose
-> required truncation => incomplete / fail closed
```

## 4. U01 exact-current-baseline selector review

Se revisaron los selectores requeridos de U01 contra el
`reviewed_code_baseline@07e667d...`.

La integración posterior del admission review no modificó ninguno de esos
selectores ni sus fuentes requeridas.

Resultado estático de admisión:

| Selector | Matches observados | Budget | Estado |
| --- | ---: | ---: | --- |
| `src/malak/kernel/` | 20 | 64 | RESOLVED |
| `src/malak/services/planner.py` | 6 | 32 | RESOLVED |
| `src/malak/contracts/capability.py` | 1 | 32 | RESOLVED |
| `src/malak/app/composition.py` | 26 | 64 | RESOLVED |
| `tests/test_kernel.py` | 15 | 64 | RESOLVED |
| `docs/architecture/blueprint.md` | 6 | 16 | RESOLVED |
| `docs/architecture/architecture_quality_gates.md` | 5 | 64 | RESOLVED |
| `docs/governance/cognitive_constitution.md` | 18 | 64 | RESOLVED |
| `docs/governance/governance_constitution.md` | 6 | 32 | RESOLVED |
| `GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md` | 12 | 64 | RESOLVED |
| `MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1-BATCH-D.md` | 30 | 64 | RESOLVED |

Máxima longitud observada de una línea seleccionable:

```text
136 bytes
```

Budget por línea:

```text
2048 bytes
```

Por tanto, la revisión estática no observa hoy:

```text
required selector missing
required selector budget overflow
required line truncation
```

Importante:

```text
static admission review
!= runtime focus_complete proof
```

La prueba material definitiva sigue ocurriendo durante el run mediante los
lectores Git/Knowledge ligados al baseline exacto.

## 5. Evidencia y completitud

Para la tercera ejecución, U01 debe mantener:

```text
SelfReviewEvidencePacket READY
AND
U01 focus complete
AND
Inspect evidence_set_digest
==
Analyze evidence_set_digest
==
Propose evidence_set_digest, if Propose runs
```

Cualquier incumplimiento:

```text
-> INCONCLUSIVE
-> STOP
-> no reinterpretation as GAP
```

La evidencia suplementaria puede truncarse de forma visible, pero no puede
convertir un required selector incompleto en completo.

## 6. Observabilidad y diagnóstico

Los dos gaps operacionales observados en los runs previos tienen ahora caminos
explícitos.

### OBS-01

Durante llamadas largas:

```text
RUNNING
-> live elapsed overlay
-> no fake %
-> no fake ETA
-> no new trace event
```

La duración final sigue derivando del trace material.

### OBS-02

Ante excepción de componente:

```text
COMPONENT_FAILED
-> reason_code = component_error
-> diagnostic:Dxxxx
-> safe diagnostic artifact
```

No se persiste por defecto:

```text
raw str(exc)
raw traceback
locals
absolute local paths
prompt
response
secrets
```

## 7. Runtime / Model Provenance

El Harness exige antes de Engineering:

```text
capture_provenance(model)
-> model_identity_strength == TAG_DIGEST_BOUND
```

`TAG_DIGEST_BOUND` significa:

```text
configured local tag
+
resolved local tag
+
digest observed from local Ollama model catalog
```

No significa:

```text
cryptographic attestation of the exact model artifact
that served every /api/chat response
```

### 7.1 Disposición de fuerza de identidad

Para esta tercera ejecución U01, `TAG_DIGEST_BOUND` se considera
**suficiente como precondición mínima**, únicamente porque el experimento es:

- local;
- single-host;
- read-only sobre producción;
- sin tools con side effects;
- sin delegación;
- sin Protected Durable Write;
- sin autoridad derivada del modelo;
- con resultado que termina en Owner;
- con `authority_effect=none`.

Por tanto:

```text
TAG_DIGEST_BOUND
-> ACCEPTABLE FOR THIS BOUNDED U01 RUN

TAG_DIGEST_BOUND
-> NOT SUFFICIENT FOR
   cryptographic served-response attestation
   cross-host trust
   delegated authority
   Protected Durable Write
   security-sensitive model identity claims
```

Esto no modifica RR-03 ni lo declara resuelto.

## 8. Runtime preconditions obligatorias

La ejecución futura sólo puede iniciarse si, en local:

```text
branch == main
tracked working tree == clean

diff reviewed_code_baseline..HEAD
-> only:
   docs/project/sprints/proposals/
   MALAK-THIRD-U01-ADMISSION-REVIEW-20260925.md

current HEAD
-> becomes exact execution baseline
-> Engineering baseline must equal that HEAD

MALAK_RUNTIME == ollama
MALAK_OLLAMA_MODEL configured
MALAK_REPOSITORY_ROOT points to exact repository
local Ollama reachable
configured model resolves locally
model identity == TAG_DIGEST_BOUND
run_id does not already exist
```

El Harness ya falla cerrado ante branch/head/tree mismatch y ante identidad
inferior a `TAG_DIGEST_BOUND`.

El control adicional `reviewed_code_baseline..HEAD` pertenece al preflight de
admisión y debe ejecutarse antes de invocar el Harness.

## 9. Run identity propuesto

Si el Owner autoriza runtime después de integrar este admission review:

```text
run_id:
bootstrap-u01-20260925-003

validation refs:
Validation#541
Validation#543
PR#190
PR#191
reviewed-code@07e667d669352d8cb0974dbbbcb017fa4ea7d979

exact execution baseline:
captured from current main HEAD at preflight and persisted by the run artifacts
```

El task/focus/scope siguen congelados por Test V0:

```text
task_id   governed-self-review-bootstrap-v0
focus_id  U01
subject   Kernel
mode      read-only
```

No se permite input arbitrario de task/focus/subject.

## 10. Expected valid outcomes

La tercera ejecución no necesita producir una mejora.

Resultados válidos:

```text
NO_CHANGE_RECOMMENDED
HARDENING_PROPOSAL
RESEARCH_REQUIRED
DEFER
INCONCLUSIVE
```

Reglas:

```text
INCONCLUSIVE != failure to hide
NO_CHANGE_RECOMMENDED != weak result
GAP != authorization
proposal != implementation
```

## 11. Bootstrap completion boundary

La tercera ejecución sigue siendo sólo:

```text
U01
```

Incluso si U01 termina `COMPLETE`:

```text
U04   NOT EXECUTED
RR-03 NOT EXECUTED
```

Por tanto:

```text
third U01 PASS
!= bootstrap complete
```

No se puede agregar un resultado global que esconda slices no ejecutados.

## 12. Security / authority review

No cambia:

```text
Kernel authority
Planner authority
SecurityContext
Memory
Knowledge admission
Trace schema
Protected Durable Write
agent authority
merge authority
```

Permitido durante el run:

```text
read exact Git baseline
read governed Knowledge
local read-only Ollama provenance introspection
local Ollama inference
runtime/internal_interaction/<run_id> artifacts
terminal LIVE view
REPLAY
```

Prohibido:

```text
edit tracked production
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

## 13. Admission 4R

### Risk — PASS WITH BOUNDED LIMITATION

La principal limitación residual es:

```text
TAG_DIGEST_BOUND
!= served-response digest attestation
```

Es aceptable para este experimento read-only y sin autoridad, pero no se eleva a
una garantía de identidad criptográfica.

### Readability — PASS

Las causas previas están separadas:

```text
evidence problem
!= component failure
!= liveness problem
!= model identity limitation
!= governance stop
```

### Reliability — PASS

El run tiene:

- exact baseline guard;
- clean-tree guard;
- focus completeness;
- evidence digest;
- diagnostic artifacts;
- runtime provenance artifact;
- attestation;
- LIVE/REPLAY equivalence;
- terminal disposition cerrada.

### Resilience — PASS

Cualquier precondición material insuficiente produce STOP / INCONCLUSIVE antes
de convertir incertidumbre en finding o autoridad.

## 14. RDD / Candidate Conformance

Este admission review no implementa runtime.

```text
reviewed code baseline exact     PASS
execution baseline rule           PASS
prior candidate validations      PASS
causal gaps closed separately    PASS
runtime preconditions explicit   PASS
rollback                         not applicable
authority_effect                 none
```

No se autoriza RDD Stage 2 ni ninguna modificación basada en el eventual output
de U01.

## 15. Admission disposition

```text
Third U01 Admission Review

baseline readiness              PASS
baseline binding semantics       PASS
EVID-01 / EVID-02               CLOSED
OBS-01                          CLOSED
OBS-02                          CLOSED
Model Provenance                CLOSED FOR BOUNDED RUN
TAG_DIGEST_BOUND                ACCEPTED WITH LIMITATION
U01 selector static review      PASS
authority expansion             0
production write authority      0

ADMISSION RESULT:
CONDITIONAL PASS
```

Condición restante:

```text
Owner must explicitly authorize the real runtime execution
after this admission review is reviewed and merged.
```

## 16. Current authority state

```text
third U01 runtime execution     NOT AUTHORIZED
self-modification               NOT AUTHORIZED
implementation from findings    NOT AUTHORIZED
Ready / merge of this review    OWNER ONLY
authority_effect                none
```

Siguiente gate, sólo después de revisión/merge humano:

```text
Owner explicit runtime authorization
-> local preflight
-> third U01 real run
-> artifacts
-> LIVE / REPLAY
-> disposition
-> Owner
-> STOP
```


## 17. Post-merge baseline binding correction

Después de mergear este admission review se verificó una inconsistencia
documental material:

```text
document required:
HEAD == reviewed_code_baseline

but merging the document itself changed HEAD
```

Eso no representa drift de código, pero sí hacía imposible cumplir literalmente
la precondición después del merge.

La corrección no relaja el baseline. Lo separa en dos identidades:

```text
reviewed_code_baseline
= 07e667d669352d8cb0974dbbbcb017fa4ea7d979

execution_baseline
= exact current main HEAD at preflight
```

Admission sigue válido únicamente si:

```text
git diff --name-only reviewed_code_baseline..HEAD
==
docs/project/sprints/proposals/
MALAK-THIRD-U01-ADMISSION-REVIEW-20260925.md
```

Si aparece cualquier otro path:

```text
STOP
-> current admission no longer covers execution baseline
-> new admission review required
```

Este ajuste:

```text
runtime authority expansion     0
code/runtime delta              0
self-review execution           NOT AUTHORIZED
authority_effect                none
```
