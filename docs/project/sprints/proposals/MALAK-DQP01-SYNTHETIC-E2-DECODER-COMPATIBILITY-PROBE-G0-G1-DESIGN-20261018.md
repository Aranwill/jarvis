---
title: Malāk DQP01 — Synthetic E2 Decoder Compatibility Probe — G0/G1 Design
status: design_candidate
authority: non_normative
language: es
as_of_date: 2026-10-18
baseline_commit: b054f7cb10a0cbc5818ffc5ae5ca7503efc2d209
baseline_tree: 0cb2f1c2f097c7a6abd2535011129211e9d6b4bb
branch_role: PR-A Design / Documentation
risk_class: 3
critical_contract: true
implementation_authorized: false
red_authorized: false
green_authorized: false
model_execution_authorized: false
c03_authorized: false
rdd_stage_2_pr_a_required: true
rdd_stage_2_required_for_future_executor: true
authority_effect: none
---

# Malāk DQP01 — Synthetic E2 Decoder Compatibility Probe — G0/G1 Design

## 1. Propósito

Congelar el diseño mínimo de DQP01 para observar, con una única generación
sintética, si el stack exacto de E2 puede producir una salida aceptada por el
parser E2 vigente usando el schema focused completo con cuatro variantes.

DQP01 reduce una incertidumbre acotada del contexto PRE-MODEL posterior a #336:

~~~text
F336-C03-01
REAL_DECODER_ANYOF_UNQUALIFIED
~~~

No mide cognición del piloto, no ejecuta C03, no reabre C01/C02 y no convierte
una muestra positiva en calificación universal del decoder.

~~~text
OBSERVED_COMPATIBILITY
!= ALL_CONSTRAINTS_ENFORCED
!= ANYOF_CAUSAL_ENFORCEMENT
!= FUTURE_C03_SUCCESS
!= PASS_EXECUTION_CONTEXT_FREEZE
!= G2
!= C03_AUTHORIZATION
~~~

Esta PR-A no ejecuta modelos ni llama /api/chat.

## 2. Identidad congelada

~~~text
repository                 Aranwill/jarvis
baseline_commit            b054f7cb10a0cbc5818ffc5ae5ca7503efc2d209
baseline_tree              0cb2f1c2f097c7a6abd2535011129211e9d6b4bb
baseline_blobs             405
schema_sha256              4e264b311badcbce771f4f74ef35690703571dc0585869a77373aba252b7109e
request_sha256             e6c833f775d7e87e50d7c9434c763007d0ece0700d7fc1a920d6c459b012d754
system_prompt_sha256       c2d382f0a1dba803fcab4ec6d7fafac04d231c02f4b916d9c22536658785b7cd
prompt_sha256              f2829621a5f15f77ec8eed7c3577e1280a9e1a1c6265c776390951c4620b8ef8
synthetic_request_bytes    14544
authority_effect           none
~~~

La fuente externa de diseño recibió PASS independiente antes de esta PR-A.
Ese PASS no certifica este candidate Git; este candidate requiere revisión
independiente candidate-bound.

## 3. Construction Preflight

### P0 — identidad repository-first

PASS candidate. Main coincide exactamente con el baseline declarado.

### P1 — fuentes reconciliadas

Fuentes aplicables:
- AGENTS.md;
- Cognitive Constitution;
- Governance Constitution;
- Blueprint;
- Kernel Specification;
- Architecture Quality Gates;
- SECURITY.md;
- Engineering Method;
- Construction Protocol;
- Construction Preflight;
- Development Checklist;
- Evidence Manifest;
- RDD Stage 2 Validation Receipt;
- CURRENT README.md y implementation_roadmap.md;
- implementación y tests E2, Conversation y Ollama relevantes.

El File Coverage Ledger de esta PR-A clasifica el baseline completo.

### P2 — invariantes

~~~text
Human in Control             preserved
Kernel First                 preserved
Capability First             N/A — no Capability nueva
Runtime Independence         preserved
Zero Trust                   preserved
Least Context                preserved
product delta                0
Kernel delta                 0
Governance delta             0
new dependency               0
model calls in PR-A          0
authority expansion          0
~~~

### P3 — autoridad

~~~text
Owner
  ↓
governed experimental scope
  ↓
future bounded executor
  ↓
local runtime/model
  ↓
synthetic result
  ↑
Evidence only
  ↑
independent validation
  ↑
human decision
~~~

No existe upward control path ni auto-promoción. authority_effect=none.

### P4 — Reuse / Complexity

~~~text
OllamaRuntime                         REUSE
ConversationRequest                   REUSE
RuntimeGenerationContract             REUSE
E2 schema / strict parser             REUSE
synthetic probe fixture               NEW TEST/EVALUATION ARTIFACT ONLY
new runtime/provider/service          REJECT
new Capability/manager/registry       REJECT
new benchmark subsystem               REJECT
~~~

Mocks y validación estática no observan el decoder real. Un probe sintético
único es la intervención mínima para observar compatibilidad sin consumir C03.

### P5 — riesgo

~~~text
risk_class                     3
risk_rationale                 model execution + loopback transport + Evidence used by freeze reasoning
critical_contract              YES
Design 4R                      REQUIRED
Candidate FULL 4R              REQUIRED for future executor
RDD Stage 1                    REQUIRED
RDD Stage 2 PR-A               REQUIRED
RDD Stage 2 future executor     REQUIRED
independent validation         REQUIRED
~~~

### P6 — scope

Esta PR-A permite sólo este Design, su Identity y su File Coverage Ledger.

Hard-zero PR-A:

~~~text
src/malak/**
scripts/**
tests/**
evaluations/**
configs/**
.github/**
law docs
CURRENT_STATE docs
runtime/product code
~~~

### P7 — resultado

~~~text
Construction Preflight writer candidate = PASS
implementation                         = NOT AUTHORIZED BY THIS PR-A
model execution                        = NOT AUTHORIZED
authority_effect                       = none
~~~

## 4. G0 — problema exacto

Estado CURRENT preservado:

~~~text
C01_ATTEMPT                 CONSUMED
C01_RETRY                   FORBIDDEN
C02_ATTEMPT                 CONSUMED
C02_RETRY                   FORBIDDEN
C03_ATTEMPT                 NOT_STARTED
C03                         HOLD
MODEL_EXECUTION_AUTHORIZED  NO
PROCESS_CONFORMANCE_HISTORICAL FAIL
~~~

La recuperación técnica de E2 cerró parser/schema contract local y CI, pero no
observó empíricamente la combinación exacta del decoder real para el schema
focused anyOf.

Pregunta DQP01:

> ¿Puede el stack exacto producir al menos una salida E2 válida con el schema
> exacto, usando datos exclusivamente sintéticos y sin consumir C03?

G0 writer candidate = PASS.

## 5. G1 — diseño mínimo

### 5.1 Presupuesto

~~~text
budget_global_DQP01       1 POST /api/chat
hidden_retries            0
repair                    0
fallback                  0
normalization             0
partial_acceptance        0
prompt adaptation         0
pilot calls               0
parallelism               1
~~~

Timeout, crash o desconexión después de reservar el intento no autorizan retry.

### 5.2 Runtime futuro

Sólo después de todos los gates y una autorización humana separada:

~~~text
endpoint                  http://localhost:11434
runtime                   existing OllamaRuntime
model                     qwen3.5:9b
context_window_tokens     32768
max_output_tokens         2048
thinking_enabled          false
input_truncation_allowed  false
history_shift_allowed     false
history                   empty
timeout_seconds           600
keep_alive                0
~~~

Version, model digest y provenance deben coincidir con el freeze aplicable.
Drift produce STOP.

### 5.3 Material sintético

~~~text
repository refs  R1 R2 R3
knowledge refs   K1 K2 K3
structural refs  NONE
pilot fixtures   FORBIDDEN
oracle/rubric    FORBIDDEN
expected labels  FORBIDDEN
C01/C02/C03 data FORBIDDEN
~~~

El request pide exactamente:
1. OBSERVED con R1;
2. KNOWLEDGE_CONTEXT con K1;
3. INTERPRETATION con R2 y K2;
4. UNCERTAINTY sin refs.

El ejemplo válido sintético es sólo control offline. Nunca es runtime output ni
oracle.

### 5.4 Schema y system prompt

El schema focused debe ser byte-identical al capturado en E2:

~~~text
4e264b311badcbce771f4f74ef35690703571dc0585869a77373aba252b7109e
~~~

El system prompt E2 exacto conserva:

~~~text
c2d382f0a1dba803fcab4ec6d7fafac04d231c02f4b916d9c22536658785b7cd
~~~

Cualquier drift bloquea transporte.

### 5.5 Attempt reservation

El único intento se reserva antes del transporte mediante creación exclusiva
de un claim externo al repo.

~~~text
claim exists
→ duplicate/concurrent invocation rejected
→ no POST
~~~

Después de reservar:

~~~text
timeout / disconnect / crash / uncertain transport
→ attempt consumed or uncertain
→ NO RETRY
~~~

### 5.6 Evidencia y contención

Fuera del candidate se conservan:
- request exacto y digest;
- schema/system/prompt digests;
- Git state before/after;
- runtime provenance before/after;
- attempt claim;
- HTTP/result metadata;
- raw sintético sólo si llega y está bounded;
- raw digest/bytes;
- parser result y four-kind coverage.

No raw en excepciones públicas.

### 5.7 Parser

La salida se valida con el parser E2 vigente y strict JSON.

Parser rejection significa output observado rechazado. No implica por sí solo
decoder anyOf unsupported.

## 6. Semántica terminal

### PASS_DQP01

Demuestra sólo:

~~~text
OBSERVED_COMPATIBILITY = SUPPORTED
~~~

No demuestra universal enforcement.

### FAIL_DQP01

- respuesta recibida y parser/cobertura rechazada: FAIL del probe, subcausa
  decoder no demostrada;
- rechazo HTTP/schema explícito: FAIL del request exacto; atribución a anyOf
  requiere evidencia causal suficiente.

### INCONCLUSIVE_DQP01

Timeout, crash, ausencia/incompletitud de respuesta, provenance drift o
incertidumbre sobre transporte. INCONCLUSIVE != PASS. No retry.

## 7. Incertidumbre que debe sobrevivir

~~~yaml
anyof_decoder_causal_enforcement: INCONCLUSIVE
all_constraints_universal_enforcement: INCONCLUSIVE
success_rate: UNKNOWN
repeatability_across_calls: UNKNOWN
transfer_to_real_C03: UNKNOWN
semantic_correctness_C03: NOT_TESTED
historical_C02_causality: INCONCLUSIVE
~~~

Una muestra positiva no cierra automáticamente F336-C03-01.

## 8. Critical Contract Hardening

~~~text
alternate material interpretations   CLOSED for bounded claim
adversarial overclaim                CLOSED by explicit inequality rules
fail-open paths                      NONE admitted
authority boundaries                 CLOSED
schema/input drift                    STOP
candidate/evidence binding           REQUIRED
unknown transport after reservation  INCONCLUSIVE / NO RETRY
tooling-outside-Git bypass            FORBIDDEN
known material ambiguity unresolved  0
~~~

Hardening writer candidate = PASS.

## 9. Cuatro preguntas de ley

1. Blueprint: PASS candidate — tooling de evaluación aislado; Kernel delta 0.
2. Cognitive Constitution: PASS candidate — CC-003/005/006.
3. Governance Constitution: PASS candidate — GOV-001/004 y Human in Control.
4. Kernel simplicity: PASS candidate — Kernel delta 0.

## 10. Design 4R

Risk — PASS candidate. Una llamada, synthetic-only, reservation-before-transport,
no retry y autoridad humana separada.

Readability — PASS candidate. Design, executor, probe result, freeze, G2 y C03
son estados distintos.

Reliability — PASS candidate. SHA/digests exactos, parser strict, provenance
before/after y drift STOP.

Resilience — PASS candidate. Crash/timeout no generan repetición; no fallback ni
repair.

Design 4R writer candidate = PASS.

## 11. RDD Stage 1 Design Check

~~~text
baseline exact                          PASS
candidate identity strategy             PASS
baseline/candidate binding              PASS
evidence provenance                     PASS
Writer/Reviewer/Validator/Authority     SEPARATED
PASS|FAIL|INCONCLUSIVE only             PASS
INCONCLUSIVE != PASS                    PASS
candidate drift invalidates evidence    PASS
bounded correction                      REQUIRED if findings
Fix Validator                           REQUIRED when applicable
authority_effect                        none
RDD Stage 2 PR-A                        REQUIRED
RDD Stage 2 future executor             REQUIRED
~~~

RDD Stage 1 Design Check writer candidate = PASS.

## 12. Future PR-B — executor candidate

Sólo después de:
1. CI candidate-bound de PR-A;
2. Independent Design Review PASS del candidate exacto;
3. RDD Stage 1 Candidate Conformance + RDD Stage 2 Receipt REQUIRED para esta PR-A risk-3;
4. revisión humana;
5. Owner Ready/Merge;
6. post-merge reconciliation;
7. autorización separada para PR-B.

La PR-B debe materializar un executor Git candidate-bound. Un script material
únicamente fuera de Git no satisface la identidad requerida.

Scope inicial a readmitir y congelar para PR-B:

~~~text
scripts/run_dqp01_synthetic_e2_decoder_probe.py
tests/test_dqp01_synthetic_e2_decoder_probe.py
evaluations/dqp01_synthetic_e2_decoder_probe/**
~~~

PR-B requiere RED causal, Owner GREEN authorization, GREEN mínimo, targeted
tests, Candidate FULL 4R, Bounded Correction/Fix Validator cuando aplique,
E2E con transporte simulado, CI candidate-bound, independent validation,
RDD Stage 1 Candidate Conformance y RDD Stage 2 Receipt.

Nada de esto autoriza la llamada live. La única llamada requiere autorización
humana posterior para candidate/request/runtime/model exactos.

## 13. Revisión externa previa

La revisión independiente PRE-MODEL del paquete externo concluyó PASS de diseño
y dejó:

~~~text
CAN_ADVANCE_TO_GOVERNED_IMPLEMENTATION_PATH = YES
DIRECT_UNTRACKED_EXECUTOR_IMPLEMENTATION = NO
DIRECT_INFERENCE = NO
REQUIRES_CANDIDATE_BOUND_EXECUTOR = YES
REQUIRES_FULL_4R_FOR_EXECUTOR = YES
REQUIRES_CI_CANDIDATE_BOUND = YES
REQUIRES_RDD_STAGE_1_CANDIDATE_CONFORMANCE = YES
REQUIRES_RDD_STAGE_2_RECEIPT = YES
~~~

Finding que debe permanecer abierto:

~~~text
DQP01-F01
SINGLE_SAMPLE_DOES_NOT_PROVE_ANYOF_ENFORCEMENT
OPEN / MUST_BE_PRESERVED
~~~

Finding de proceso incorporado:

~~~text
DQP01-F02
EXECUTOR_MUST_BE_CANDIDATE_BOUND
DISPOSITION DEFINED
~~~

La revisión externa es input de diseño, no certificación de este candidate.

## 14. Malāk Alignment Matrix

| source | authority class | invariant / intent | disposition | effect |
|---|---|---|---|---|
| Cognitive Constitution | normative | evidence over speculation; proportionality; minimization | ADOPT | bounded probe and residual |
| Governance Constitution | normative | user control; least privilege | ADOPT | separate execution authority |
| Blueprint | normative architecture | Human in Control; Runtime Independence; Verification First | ADOPT | no Kernel/product coupling |
| SECURITY.md | protected | Zero Trust; Least Context; Evidence != Authority | ADOPT | synthetic-only and fail-closed |
| Architecture Quality Gates | protected | architecture/governance compliance | ADOPT | pre-RED review |
| Construction Protocol | operative | critical sequence; PR-A/PR-B; RDD | ADOPT | two-phase construction |
| Evidence Manifest / Receipt | operative contract | candidate binding / Stage 2 | ADOPT | future executor candidate-bound |
| CURRENT roadmap/README | derived current state | C03 HOLD; new freeze/G2 | ADOPT | no inference now |
| E2 runtime/parser/tests | implementation | strict contract | REUSE | no new product component |
| concepts / ideas | conceptual | evidence-bound learning | OBSERVE | no subsystem |
| external DQP01 review | independent evidence | single sample useful but non-universal | ADAPT | preserve residual |

## 15. Bounded Design Correction — Round 1

Trigger independiente: la revisión de PR #337 sobre el candidate
`ab9a842ea5532a2ab345854f5867c6028154b391` devolvió `INCONCLUSIVE` sin defecto técnico bloqueante del
experimento y abrió F337-ID01, F337-COV01 y F337-RDD01.

Esta corrección está estrictamente limitada a:

~~~text
F337-ID01
candidate tree independently re-read from Git object
actual = expected = 6adc78489dc2a94860b3d576ca03ae563bf7ae63
writer-side status = EVIDENCE AVAILABLE FOR FIX VALIDATOR

F337-COV01
baseline recursive Git tree = non-truncated
Git blobs = 405
ledger baseline rows = 405
missing = 0
extra = 0
duplicated = 0
writer-side status = EVIDENCE AVAILABLE FOR FIX VALIDATOR

F337-RDD01
RDD Stage 2 PR-A = REQUIRED
RDD Stage 2 future PR-B = REQUIRED
writer-side status = TEXT CORRECTED / EVIDENCE STILL REQUIRED BEFORE READY

CI #969
tests = PASS
compileall = PASS
git diff --check = FAIL
cause = empty final related_findings field encoded as trailing tab on 405 baseline TSV rows
correction = encode explicit NONE in those 405 cells
~~~

No finding se auto-cierra por declaración del writer. El nuevo candidate invalida
la disposición terminal sobre el SHA anterior y requiere affected independent
Fix/Design Validation.

Preservación epistemológica obligatoria:

~~~text
DQP01-F01 — SINGLE_SAMPLE_DOES_NOT_PROVE_ANYOF_ENFORCEMENT
OPEN / MUST_BE_PRESERVED
~~~

No se modifica budget, schema, request, runtime contract, C03 HOLD, autoridad ni
scope de producto.

## 16. File Coverage

~~~text
baseline tracked blobs discovered = 405
baseline tracked blobs classified = 405
baseline silently omitted files   = 0
candidate-only PR-A artifacts     = 3
~~~

## 17. Rollback

PR-A es docs-only.

~~~text
revert candidate commit
→ no runtime/model/product state affected
→ C03 remains HOLD
→ no DQP01 attempt consumed
~~~

## 18. Next lawful transition

~~~text
PR-A candidate-bound CI
→ Independent Design Review on exact candidate
→ affected Design 4R / RDD Design disposition
→ RDD Stage 1 Candidate Conformance + RDD Stage 2 Receipt REQUIRED para PR-A
→ human review
→ Owner Ready / Merge
→ post-merge reconciliation
→ separate Owner authorization for PR-B
→ RED / GREEN / FULL 4R / E2E / CI / independent validation
→ RDD Stage 1 Candidate Conformance
→ RDD Stage 2 Receipt
→ human review / Owner Ready / Merge
→ separate explicit authorization for ONE live DQP01 call
→ independent DQP01 result validation
→ complementary F336-C03-01 disposition
→ NEW PRE-MODEL freeze remains separate
→ NEW Owner G2 remains separate
~~~

authority_effect=none
