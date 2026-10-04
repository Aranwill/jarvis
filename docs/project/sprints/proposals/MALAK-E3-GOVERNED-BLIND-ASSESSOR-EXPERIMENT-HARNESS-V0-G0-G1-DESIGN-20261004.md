---
title: Malāk E3 Governed Blind Assessor Experiment Harness V0 — G0/G1 Design
status: design_candidate
authority: non_normative
language: es
as_of_date: 2026-10-04
baseline_commit: 7f92a499fda4eb17961a69bf939d719c1d15d260
branch_role: PR-A Design / Documentation
risk_class: 3
critical_contract: true
runtime_delta: 0
implementation_authorized: false
red_authorized: false
green_authorized: false
model_provider_experiment_authorized: false
network_authorized: false
support_sufficient_wiring_authorized: false
rdd_stage_2_authorized: false
authority_effect: none
---

# Malāk E3 Governed Blind Assessor Experiment Harness V0 — G0/G1 Design

## 1. Propósito

Congelar el diseño mínimo para cerrar el hueco real entre el case-set de
qualification ya integrado y el artifact que consume el Assessor Qualification
Pack V0.1.

~~~text
case-set V0.1 + ground truth revisado
        ↓
blind candidate-visible material
        ↓
[HUECO ACTUAL: no existe producer gobernado del experiment artifact]
        ↓
MALAK-E3-SUPPORT-ASSESSOR-RESULTS/v0.1
        ↓
Assessor Qualification Pack V0.1
        ↓
PASS | FAIL | INCONCLUSIVE
~~~

Esta unidad no selecciona ni ejecuta un model/provider real. Diseña únicamente un
harness de evaluation tooling capaz de componer primitives ya integradas, ejecutar
un assessor callable bounded y producir el artifact V0.1 que el Qualification Pack
ya valida.

Invariantes:

~~~text
assessor output != semantic truth
qualification PASS != production authorization
qualification PASS != support_sufficient
experiment Evidence != Authority
more cognition != more authority
~~~

### 1.1 Bounded Design Correction — independent review round 1

El independent pre-RED Design Review del candidate
`889a9df1db482fe56253f1c01b0dd4e20fadc74c` terminó:

~~~text
INDEPENDENT PRE-RED DESIGN REVIEW = FAIL
F253-PRED-01  MATERIAL
F253-PRED-02  MATERIAL
F253-PRED-03  MINOR
~~~

El FAIL histórico se preserva y no se reinterpreta como PASS.

~~~text
design correction round = 1 / 2
RED                     = NOT AUTHORIZED
GREEN                   = NOT AUTHORIZED
authority_effect        = none
~~~

Esta corrección bounded:
1. separa observation/case-set binding del expected-profile binding;
2. congela el schema del experiment profile y sus tres recetas de digest;
3. congela 19 inputs / 19 observations / 13 candidate invocations elegibles;
4. endurece R02/R16/R26/R28-R30/R35;
5. conserva el future three-file scope.

## 2. Corrección del working name post-PR #252

PR #252 registró provisionalmente:

~~~text
E3 Blind Assessor Experiment Boundary V0
~~~

El relevamiento repository-first del baseline actual demuestra que la blind
projection primitive ya existe:

~~~text
src/malak/capabilities/_engineering_analysis.py
→ project_blind_support_assessor_input_v0(...)
~~~

y posee tests que verifican:

- exclusión de expected_outcome y expected_reason_codes;
- exclusión de case_class y critical_properties;
- rechazo de ground truth anidado;
- bounds;
- detached-copy behavior;
- candidate artifact antes de hidden comparison.

Por tanto:

~~~text
crear otra blind projection
→ duplicación
→ REJECT
~~~

La responsabilidad faltante es un harness que componga esa projection con el
support-assessment envelope y produzca el artifact de qualification existente.

Working name corregido:

~~~text
E3 Governed Blind Assessor Experiment Harness V0
~~~

## 3. Construction Preflight

### P0 — Identidad exacta

~~~text
repository                 Aranwill/jarvis
baseline                   7f92a499fda4eb17961a69bf939d719c1d15d260
entry ref                  main
work unit                  E3 Governed Blind Assessor Experiment Harness V0
work type                  PR-A / G0-G1 Design
current material candidate none before this Design PR
last stable checkpoint     PR #252 merge / main@7f92a499fda4eb17961a69bf939d719c1d15d260
~~~

P0 = PASS.

### P1 — Fuentes reconciliadas

Lectura/revisión aplicable:

- AGENTS.md;
- Cognitive Constitution;
- Governance Constitution;
- Blueprint;
- Kernel Specification;
- Architecture Quality Gates;
- SECURITY.md;
- ADR-002, ADR-003 y ADR-004;
- Engineering Method;
- Construction Protocol;
- Construction Preflight;
- Development Checklist;
- Evidence Manifest;
- README CURRENT_STATE;
- implementation_roadmap.md;
- project_context.md;
- documents/projects/jarvis/ideas.md;
- docs/project/concepts/**;
- MALAK_RESEARCH_HORIZON_MAP.md mediante lectura explícita;
- E3 Support Assessment;
- Assessor Qualification Pack V0.1;
- Governed Support Evidence Routing;
- Positive Qualification Consumption Trust Boundary;
- código, tests y evaluation tooling actuales.

Inventario conceptual explícito:

~~~text
GOVERNED_EPHEMERAL_AGENT_EXECUTION_EVIDENCE_REFERENCE.md
GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md
GOVERNED_SWARM_LONG_HORIZON_REFERENCE.md
MALAK_COGNITIVE_DATASET_FOUNDATION.md
MALAK_EVIDENCE_BOUND_COGNITION_FOUNDATION.md
MALAK_RESEARCH_HORIZON_MAP.md
README.md
~~~

Las fuentes conceptuales informan; no autorizan.

P1 = PASS.

### P2 — Arquitectura

~~~text
Kernel First                 preserved
Capability First             preserved
Runtime Independence         preserved
Model Agnostic               preserved
Human in Control             preserved
Zero Trust                   preserved
production runtime delta     0
Kernel / Planner delta       0
new Capability               0
new Service / Manager        0
~~~

P2 = PASS.

### P3 — Directional Communication / Authority

~~~text
trusted evaluation harness
        ↓
bounded candidate callable
        ↓
candidate result data
        ↓
trusted artifact construction
        ↓
Qualification Pack
        ↓
Evidence
        ↓
human / later governed admission
~~~

El candidate devuelve datos. No controla al harness, no modifica policy y no
adquiere Authority.

P3 = PASS.

### P4 — Component / Logic Reuse Review

| Elemento | Disposición | Razón |
| --- | --- | --- |
| project_blind_support_assessor_input_v0 | REUSE | ya existe y bloquea ground-truth leakage por la API |
| assess_governed_evidence_support_v0 | COMPOSE | envelope bounded ya normaliza output/error del assessor |
| case-set V0.1 C01–C18 / 19 inputs | REUSE | corpus y ground truth existentes |
| MALAK-E3-SUPPORT-ASSESSOR-RESULTS/v0.1 | REUSE | schema ya consumido por Qualification Pack |
| evaluate_e3_governed_evidence_support_assessor.py | REUSE AS CONSUMER | consumer independiente del artifact |
| input/semantic digest semantics | ADAPT WITH REGRESSION EQUIVALENCE | producer debe calcular lo mismo que consumer recomputa |
| model/provider runtime | DEFER | no requerido para este harness |
| new Capability | REJECT | no justificada |
| Manager / Registry / Service | REJECT | complejidad preventiva |

Resultado:

~~~text
REUSE + COMPOSE + bounded ADAPT
NEW architectural component = NOT JUSTIFIED
~~~

### P5 — Necessity & Complexity / Risk

Necesidad:

~~~text
Qualification Pack starts at assessor-result artifact
+
current tests synthesize that artifact
+
blind projection already exists
+
no governed experiment-side producer exists
=
bounded harness gap
~~~

Clasificación:

~~~text
risk_class                 3
critical_contract          YES
Design 4R                  REQUIRED
Candidate FULL 4R          REQUIRED after GREEN
RDD Stage 1                REQUIRED
independent pre-RED review REQUIRED
E2E-equivalent             REQUIRED after GREEN
~~~

P5 = PASS.

### P6 — Scope freeze

Esta PR-A modifica solamente:

- este Design record;
- su File Coverage ledger.

Future PR-B, sólo tras merge humano de PR-A y autorización posterior:

~~~text
ALLOW
evaluations/e3_governed_evidence_support_assessor_v0/experiment_profile.json
scripts/run_e3_governed_blind_assessor_experiment.py
tests/test_e3_governed_blind_assessor_experiment.py

DENY WITHOUT STOP → scope review
src/malak/**
evaluations/e3_governed_evidence_support_assessor_v0/cases.json
scripts/evaluate_e3_governed_evidence_support_assessor.py
scripts/evaluate_e3_deterministic_oracle_qualification.py
Kernel
Planner
Security contracts / PDP / PEP
Conversation
runtime/provider/model implementation
dependencies
support_sufficient
Protected Finalization
RDD Stage 2
~~~

Candidate identity:

~~~text
Design candidate = exact PR-A HEAD SHA
RED candidate    = exact SHA in future single Implementation PR
GREEN candidate  = descendant exact SHA in that same PR
candidate change → affected Evidence invalidated/revalidated
~~~

P6 = PASS.

### P7 — Preflight terminal

~~~text
reuse_disposition           REUSE / COMPOSE / ADAPT
necessity_disposition       PASS
risk_class                  3
critical_contract           YES
scope_status                FROZEN
candidate_identity_strategy DEFINED
blocking_findings           0
result                      PASS
authority_effect            none
~~~

Construction Preflight PASS no equivale a review independiente, RED, GREEN,
Ready ni Merge.

## 4. G0 — Problema exacto

El baseline dispone de:

1. case-set V0.1 con 18 casos / 19 inputs y ground truth;
2. blind projection primitive integrada;
3. support-assessment envelope bounded;
4. Qualification Pack offline que recibe assessor-result artifact;
5. positive qualification consumption boundary.

No dispone de un producer gobernado que demuestre la cadena:

~~~text
exact case-set
→ no ground-truth leakage through candidate arguments
→ bounded candidate invocation
→ exact observations
→ exact artifact V0.1
→ existing Qualification Pack
~~~

Los tests actuales construyen artifacts sintéticos. Eso prueba el consumer, pero
no el producer de un experimento separado.

Finding de admisión:

~~~text
GBAEH-G0-01
type: EVALUATION_CHAIN_GAP
severity: material
blocking for real assessor experiment: YES
blocking for current production runtime: NO
authority_effect: none
~~~

## 5. Claim permitido

Un future GREEN podría sostener únicamente:

> El harness V0 produjo un MALAK-E3-SUPPORT-ASSESSOR-RESULTS/v0.1 ligado al
> case-set exacto, usando candidate-visible material derivado de primitives
> existentes, bajo una harness identity explícita, sin pasar ground truth al
> callable a través de su API.

No podrá sostener:

~~~text
candidate cannot access repository ambiently
candidate is semantically correct
candidate is trustworthy
candidate is production-authorized
identity declaration proves independence
model/provider is safe
qualification PASS == truth
support_sufficient == true
~~~

Frontera crítica:

~~~text
argument-level blind boundary
!= OS/process sandbox
!= filesystem isolation
!= network isolation of arbitrary injected code
~~~

## 6. G1 — Diseño mínimo

### 6.1 Trusted side / candidate side

~~~text
TRUSTED EVALUATION SIDE
full case-set
hidden ground truth
binding_prior
expected values
experiment profile
        ↓
existing project_blind_support_assessor_input_v0()
        ↓
trusted structural checks
        ↓
existing assess_governed_evidence_support_v0()
        ↓
CANDIDATE CALLABLE
        ↓
outcome + reason_codes
        ↓
trusted observation construction
        ↓
sealed result artifact V0.1
        ↓
existing Qualification Pack
        ↓
hidden comparison
~~~

### 6.2 Candidate callable

Conceptual contract:

~~~text
assessor(material)
→ {
    outcome: SUPPORTED | INSUFFICIENT | INCONCLUSIVE,
    reason_codes: [...]
  }
~~~

El candidate callable recibe exclusivamente el material que hoy entrega
assess_governed_evidence_support_v0.

No recibe:

~~~text
input_id
case_id
case_class
critical_properties
expected_outcome
expected_reason_codes
binding_prior
fault mode
case-set path
full case-set
ground-truth reviewer identity
qualification result / metrics
prior candidate answers
~~~

Esto evita convertir input_id/case_id en un lookup side-channel.

### 6.3 Structural checks antes de cognition

El harness resuelve deterministicamente, antes del callable:

- role/self-certification conflict;
- subject binding expectation drift;
- evidence-material binding expectation drift;
- material incompleto/incoherente;
- explicit V0 fault mode.

Cuando una condición estructural ya determina una salida:

~~~text
candidate invocation count = 0
~~~

Counters exactos para el corpus V0.1:

~~~text
inputs processed                  19
observations produced             19
structural zero-call inputs       4  (C10, C11, C12, C17)
fault-injection zero-call inputs  2  (C14, C15)
candidate-eligible inputs         13
real candidate invocations        exactly 13 when all eligible calls return
~~~

`attempt`, `envelope invocation` y `real candidate invocation` son
contadores distintos. Un input elegible no puede omitirse silenciosamente.

### 6.4 Binding expectation

SUBJECT:

~~~text
recompute current subject fingerprint
→ mismatch against expected prior fingerprint
→ INCONCLUSIVE / SUBJECT_BINDING_MISMATCH
→ candidate not invoked
~~~

EVIDENCE_MATERIAL:

~~~text
recompute current evidence-material digest
→ mismatch against expected prior digest
→ INCONCLUSIVE / SUBJECT_BINDING_MISMATCH
→ candidate not invoked
~~~

binding_prior permanece trusted-side y nunca llega al callable.

### 6.5 Self-certification

~~~text
assessor_subject_id == finding_producer_subject_id
→ INCONCLUSIVE / SUBJECT_BINDING_MISMATCH
→ candidate invocation count = 0
~~~

Los role IDs tampoco se entregan al callable.

### 6.6 Fault scenarios V0

El future experiment_profile.json debe modelar control de ejecución sin contener
la respuesta esperada:

~~~text
NORMAL
FORCE_UNAVAILABLE
FORCE_MALFORMED_OUTPUT
~~~

Mapping V0:

~~~text
C14.I01 → FORCE_UNAVAILABLE
C15.I01 → FORCE_MALFORMED_OUTPUT
all other inputs → NORMAL
~~~

FORCE_UNAVAILABLE:

~~~text
real candidate invocation count = 0
existing envelope receives assessor=None
→ INCONCLUSIVE / ASSESSOR_UNAVAILABLE
~~~

FORCE_MALFORMED_OUTPUT:

~~~text
real candidate invocation count = 0
trusted local malformed-output fault stub
→ existing envelope
→ INCONCLUSIVE / ASSESSOR_OUTPUT_INVALID
~~~

El profile no incluye expected_outcome, expected_reason_codes,
critical_properties ni qualification thresholds.

### 6.7 No ambient-isolation overclaim

V0 garantiza únicamente que el harness no pasa ground truth al callable mediante
su API.

No garantiza que código Python arbitrario no pueda consultar filesystem,
environment, network, repository o process state si ya posee esas capacidades.

Cualquier experimento real con model/provider requiere gate separado con Security
Horizon Check, disclosure, supply-chain, execution-context y resource controls.

### 6.8 Artifact contract

Output exacto:

~~~text
MALAK-E3-SUPPORT-ASSESSOR-RESULTS/v0.1
~~~

Top-level:

~~~text
schema_version
case_set_digest
assessor_mechanism
harness
case_results
~~~

Cada observation:

~~~text
input_id
input_instance_digest
semantic_input_digest
subject_fingerprint
outcome
reason_codes
~~~

No se crea schema paralelo.

### 6.9 Digest semantics y límites del consumer existente

El producer debe ser regression-equivalent al Qualification Pack para:

- `case_set_digest`;
- `input_instance_digest`;
- `semantic_input_digest`;
- `subject_fingerprint`.

El producer calcula estos valores desde material trusted-side y el Qualification
Pack los recomputa de forma independiente.

~~~text
producer observation digest != trusted assertion
consumer recomputation mismatch → no PASS
~~~

Límite explícito del consumer actual:

El Qualification Pack valida la **forma** SHA-256 de
`assessor_mechanism.config_digest`,
`harness_policy_digest`, `budget_manifest_digest` y
`attempt_policy_digest`, pero no conoce el expected experiment profile ni
recomputa esos bindings contra un profile externo.

~~~text
Qualification Pack observation/case-set binding
!= expected-profile binding
~~~

El governed experiment path V0 agrega antes del consumer un seam harness-side:

~~~text
exact experiment profile
+ expected mechanism descriptor
+ candidate artifact
        ↓
verify_expected_experiment_binding_v0(...)
        ↓
MATCH    → eligible for Qualification Pack
MISMATCH → fail closed / no profile-bound qualification claim
~~~

Invocar directamente al Qualification Pack sin ese seam puede conservar sus
garantías propias, pero no permite reclamar `profile-bound governed experiment`.

### 6.10 Experiment profile V0 — schema cerrado

Top-level exacto:

~~~text
schema_version
harness_policy_version
expected_case_set_schema_version
expected_case_set_digest
execution_order
max_attempts_per_input
expected_input_count
expected_observation_count
expected_candidate_invocations
artifact_max_bytes
candidate_argument_policy
expected_mechanism
fault_modes
~~~

Valores V0:

~~~text
schema_version                   = "MALAK-E3-BLIND-ASSESSOR-EXPERIMENT-PROFILE/v0"
harness_policy_version           = "e3-governed-blind-assessor-experiment-harness/v0"
expected_case_set_schema_version = "MALAK-E3-SUPPORT-ASSESSOR-CASESET/v0.1"
execution_order                  = "CASESET_INPUT_ORDER_SEQUENTIAL"
max_attempts_per_input           = 1
expected_input_count             = 19
expected_observation_count       = 19
expected_candidate_invocations   = 13
artifact_max_bytes               = 524288
candidate_argument_policy        = "EXISTING_SUPPORT_ASSESSMENT_MATERIAL_ONLY"
~~~

`expected_case_set_digest` debe ser SHA-256 lowercase de los **bytes exactos**
del `cases.json` leído. Mismatch antes de procesar inputs → fail closed.

`expected_mechanism` usa exactamente el schema `assessor_mechanism` de
RESULTS/v0.1:

~~~text
mechanism_id
mechanism_version
mechanism_kind
config_digest
producer_subject_id
assessor_subject_id
model_provenance
~~~

El artifact debe contener igualdad estructural exacta:

~~~text
artifact.assessor_mechanism == profile.expected_mechanism
~~~

Metadata formalmente válida pero diferente del mechanism/config esperado:
`expected experiment binding FAIL`.

Esto es binding declarativo, no autenticación ni trust.

`fault_modes` es un array exacto de 19 entries, en el mismo orden del traversal.
Cada entry posee exactamente:

~~~text
input_id
mode
~~~

`input_id`: uno-a-uno con los 19 inputs; sin faltantes, extras ni duplicados.

`mode` enum:

~~~text
NORMAL
FORCE_UNAVAILABLE
FORCE_MALFORMED_OUTPUT
~~~

Mapping V0:

~~~text
C14.I01 → FORCE_UNAVAILABLE
C15.I01 → FORCE_MALFORMED_OUTPUT
remaining 17 entries → NORMAL
~~~

NORMAL no obliga candidate call si un structural precheck cerró el input; por eso
17 NORMAL entries producen 13 candidate-eligible invocations.

Validación del profile:

- UTF-8 válido;
- top-level object;
- exact keys;
- duplicate JSON object keys rechazadas;
- tipos exactos; integers no aceptan booleans;
- strings non-empty y trimmed;
- unknown schema/version/enum rechazado;
- counts y bounds deben coincidir exactamente con V0;
- fault map incompleto, extra, duplicado, reordenado o desplazado falla cerrado.

### 6.10.1 Canonical JSON común

~~~text
json.dumps(
    value,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
~~~

Todos los digests: SHA-256 lowercase hex.

### 6.10.2 harness_policy_digest

~~~text
harness_policy_digest =
SHA256(canonical_json(ENTIRE_VALIDATED_PROFILE_OBJECT))
~~~

Cualquier cambio semántico válido del profile cambia este digest.

### 6.10.3 budget_manifest_digest

Material exacto:

~~~json
{
  "artifact_max_bytes": 524288,
  "expected_candidate_invocations": 13,
  "expected_input_count": 19,
  "expected_observation_count": 19
}
~~~

~~~text
budget_manifest_digest = SHA256(canonical_json(exact_budget_object))
~~~

### 6.10.4 attempt_policy_digest

Material exacto:

~~~json
{
  "execution_order": "CASESET_INPUT_ORDER_SEQUENTIAL",
  "max_attempts_per_input": 1
}
~~~

~~~text
attempt_policy_digest = SHA256(canonical_json(exact_attempt_object))
~~~

Los tres digests:

- son derivados por el harness, no supplied-as-authority por el caller;
- se copian a RESULTS/v0.1;
- se recomputan en `verify_expected_experiment_binding_v0`;
- un SHA-256 formalmente válido pero diferente falla cerrado.

### 6.11 Mechanism identity y expected binding

Para `DETERMINISTIC` o `HUMAN_REVIEWED`:
`model_provenance = null`.

Para `MODEL_BASED`, el provenance schema existente debe ser completo, pero:

~~~text
MODEL_BASED descriptor valid != authorization to execute model/provider
~~~

PR-A y future PR-B de infraestructura no autorizan una ejecución MODEL_BASED real.

El expected-binding seam exige:

~~~text
artifact.assessor_mechanism == profile.expected_mechanism
~~~

por igualdad estructural exacta después de validar schemas.

`config_digest` continúa siendo binding declarativo; el harness no afirma
autenticidad, origen ni trust del mechanism.

### 6.12 Side effects

Future harness:

~~~text
network calls by harness       0
tool calls by harness          0
repo writes                    0
Memory/Knowledge writes        0
Kernel/Planner interactions    0
support_sufficient writes      0
model/provider selection       0
automatic retry                0
parallel execution             0
~~~

## 7. Security Horizon Check

Prompt & Context Trust Boundary: APPLICABLE / PASS BY DESIGN.

- ground truth trusted-side;
- candidate input bounded;
- forbidden fields no cruzan la API;
- candidate output sigue siendo untrusted.

AI Supply-Chain Trust:

~~~text
current Design        NOT ACTIVATED
real model experiment DEFERRED / BLOCKING BEFORE EXECUTION
~~~

Data disclosure: no remote disclosure en esta unidad.

Resource Governance V0:

- 19 inputs;
- una attempt por input;
- ejecución secuencial;
- no retry automático;
- artifact <= 512 KiB.

Identity:

~~~text
declared identity != authenticated identity
~~~

Human in Control permanece intacto.

## 8. Malāk Alignment Matrix

| Fuente | Clase | Intención | Disposición | Efecto |
| --- | --- | --- | --- | --- |
| Cognitive Constitution | normativa | evidence, proportionality, Generation != Finalization | ADOPT | deterministic envelope before cognition |
| Governance Constitution | normativa | HIC, no self-elevation | ADOPT | result never grants authority |
| Blueprint | normativa | Kernel First, Capability First, Model Agnostic | ADOPT | evaluation tooling only |
| Kernel Specification | normativa subordinada | no authority drift, minimum complexity | ADOPT | Kernel delta 0 |
| ADR-002 | accepted ADR | authority/enforcement separation | OBSERVE / N/A | no protected runtime operation added |
| ADR-003 | accepted ADR | result != authority/control | ADOPT | candidate returns data only |
| ADR-004 | accepted ADR | Specification & Verification First | ADOPT | exact RED obligations |
| SECURITY.md | protected policy | Zero Trust, prompt/context, HIC | ADOPT | no GT disclosure; real model deferred |
| Assessor Qualification Pack V0.1 | current contract | exact schemas and safety floor | REUSE | artifact directly consumable |
| Support Evidence Routing V0 | current implementation | blind projection + envelope | REUSE / COMPOSE | no duplicate projection |
| Positive Qualification Consumption V0 | current implementation | governed qualification required | OBSERVE | Evidence still needs later qualification/admission |
| Cognitive Dataset Foundation | concept | hidden evaluation separate | ADAPT | reinforces non-disclosure |
| Evidence-Bound Cognition | concept | confidence/agreement != truth | ADAPT | output remains Evidence |
| Ephemeral Agent Evidence Reference | concept | bounded evaluation/resources | OBSERVE | no agent/sandbox implementation |
| Research Horizon Map | concept | research informs, not authorizes | OBSERVE | no model promotion |
| ideas.md | non-normative | evaluation/model/resource governance | OBSERVE | no framework expansion |
| roadmap/project_context | derived | next candidate | ADAPT | working name refined from current code evidence |

## 9. Critical Contract Hardening

H01 Ground-truth laundering: blocked by existing projection + narrower callable.

H02 input/case ID lookup: IDs remain harness-side; absent from callable.

H03 nested ground truth: existing projection rejects forbidden keys recursively.

H04 forged digests:

- observation/case-set digests: producer calcula y Qualification Pack recomputa;
- profile/harness digests: producer calcula y
  `verify_expected_experiment_binding_v0` recomputa contra el profile esperado;
- el Qualification Pack no se presenta como verifier de profile.

H05 self-certification: role collision cannot become positive.

H06 skip/subset gaming:

~~~text
18 cases
19 inputs
0 skip
0 xfail semantics
0 best-effort subset
~~~

H07 retry/best-of-N gaming:

~~~text
max_attempts_per_input = 1
automatic retry = 0
best-of-N = 0
~~~

H08 parallel nondeterminism: execution_order = SEQUENTIAL.

H09 fault controls: trusted-side only; not candidate-visible.

H10 candidate exception: non-positive, no retry.

H11 malformed candidate output: ASSESSOR_OUTPUT_INVALID.

H12 ambient capabilities: explicitly outside V0 claim; blocks real provider execution
without separate gate.

H13 harness profile drift:

~~~text
validated profile change → harness_policy_digest changes
budget subset change     → budget_manifest_digest changes
attempt subset change    → attempt_policy_digest changes
artifact/profile mismatch
→ verify_expected_experiment_binding_v0 FAIL
→ no profile-bound qualification claim
~~~

Esta responsabilidad no se atribuye al Qualification Pack.

H14 case-set drift: changes digest; stale artifact rejected.

H15 consumer-contract drift: modification required → STOP → scope review.

H16 Authority laundering:

~~~text
experiment PASS
!= qualification PASS
!= admission READY
!= DETERMINISTIC route
!= support_sufficient
!= Ready/Merge
~~~

## 10. Cuatro preguntas de ley

Blueprint: PASS.
Cognitive Constitution: PASS.
Governance Constitution: PASS.
Kernel complexity: PASS / NO DELTA.

## 11. Design 4R — bounded correction writer revalidation

### Risk — PASS para re-review independiente

F253-PRED-01 se corrige separando garantías: el Qualification Pack recomputa
case-set/observation bindings; el nuevo expected-binding seam recomputa profile
digests y compara mechanism exacto.

F253-PRED-02 se corrige congelando schema/version, exact keys, fault map,
canonical JSON y las tres recetas de digest.

Persisten como límites explícitos: argument blindness no es sandboxing; identidad
declarada no es autenticación; real model/provider requiere gate separado.

### Readability — PASS para re-review independiente

~~~text
case-set / hidden ground truth
!= blind projection
!= experiment profile
!= experiment harness producer
!= expected-profile/mechanism verifier
!= candidate assessor
!= result artifact
!= Qualification Pack
!= runtime admission
!= authority
~~~

### Reliability — PASS para re-review independiente

~~~text
18 cases
19 inputs processed
19 observations
13 exact candidate invocations when eligible fixture execution completes
6 zero-call inputs:
  C10/C11/C12/C17 structural
  C14/C15 fault injection
one attempt per input
sequential traversal
exact profile schema
exact digest recipes
exact expected mechanism binding
~~~

Missing eligible invocation es failure.

### Resilience — PASS para re-review independiente

Fail-closed ante malformed/unknown profile, duplicate/missing/extra keys,
fault-map drift, case-set digest mismatch, mechanism mismatch, valid-looking but
wrong harness digests, structural drift, self-certification, unavailable/malformed
assessor, exception, missing/duplicate observations, oversize y consumer mismatch.

Terminal Writer after bounded correction:

~~~text
DESIGN 4R — CORRECTED WRITER CANDIDATE = PASS FOR RE-REVIEW
prior independent review               FAIL preserved
design correction round                1 / 2
claimed corrected                      F253-PRED-01 / F253-PRED-02 / F253-PRED-03
independent re-review                   REQUIRED
authority_effect                        none
~~~

## 12. RDD Stage 1 Design Check

~~~text
baseline exact                         PASS
future candidate identity strategy     PASS
scope/spec binding                     PASS
Evidence provenance strategy           PASS
Writer/Reviewer/Validator/Authority     SEPARATED
PASS|FAIL|INCONCLUSIVE discipline       PASS
candidate/profile change invalidation  PASS
failure Evidence preserved             PASS
Bounded Correction defined             PASS
independent validation required        PASS
authority_effect                       none
RDD Stage 2                            NOT AUTHORIZED
overall                                PASS
~~~

Este Writer Design Check no sustituye independent pre-RED review. El FAIL del
candidate anterior permanece histórico y este candidate corregido requiere
re-review independiente de las superficies afectadas.

## 13. Future RED requirements

Sólo después de review/merge humano de PR-A y autorización separada de RED:

~~~text
GBAEH-R01 exact case-set V0.1 bytes/schema required
GBAEH-R02 exact profile schema/version/keys/types; duplicates/extras/missing/unknown values rejected
GBAEH-R03 exactly 18 cases / 19 inputs processed / 19 observations / zero skip
GBAEH-R04 reuse existing blind projection; no duplicate algorithm
GBAEH-R05 nested forbidden ground truth never reaches candidate
GBAEH-R06 candidate never receives input_id/case_id
GBAEH-R07 candidate never receives expected outcome/reasons
GBAEH-R08 candidate never receives case_class/critical_properties
GBAEH-R09 candidate never receives binding_prior
GBAEH-R10 candidate never receives full case-set/path/profile
GBAEH-R11 SUBJECT drift closes before candidate invocation
GBAEH-R12 EVIDENCE_MATERIAL drift closes before candidate invocation
GBAEH-R13 role self-certification closes before candidate invocation
GBAEH-R14 FORCE_UNAVAILABLE: real candidate zero calls; governed non-positive result
GBAEH-R15 FORCE_MALFORMED_OUTPUT: real candidate zero calls; governed non-positive result
GBAEH-R16 exactly 13 eligible real candidate invocations; no unexpected omission; never >1/input
GBAEH-R17 candidate exception: no retry, non-positive
GBAEH-R18 malformed output rejected; candidate mutation cannot alter trusted source material
GBAEH-R19 output obeys existing support-assessment result/reason contract
GBAEH-R20 case_set_digest equals exact case-set bytes and expected profile binding
GBAEH-R21 input_instance_digest regression-equivalent to consumer
GBAEH-R22 semantic_input_digest regression-equivalent to consumer
GBAEH-R23 subject_fingerprint regression-equivalent to consumer
GBAEH-R24 observation digests producer-computed, never caller-supplied
GBAEH-R25 exact MALAK-E3-SUPPORT-ASSESSOR-RESULTS/v0.1 schema
GBAEH-R26 artifact mechanism metadata exactly equals profile.expected_mechanism; valid-but-different rejected
GBAEH-R27 incomplete MODEL_BASED provenance rejected; valid descriptor grants no execution authority
GBAEH-R28 harness_policy_digest equals SHA256 canonical entire validated profile; valid-but-wrong digest rejected by expected-binding seam
GBAEH-R29 budget_manifest_digest equals exact frozen budget object digest; valid-but-wrong rejected
GBAEH-R30 attempt_policy_digest equals exact frozen attempt object digest; valid-but-wrong rejected
GBAEH-R31 execution order CASESET_INPUT_ORDER_SEQUENTIAL
GBAEH-R32 max_attempts_per_input=1; automatic retry=0; attempt != candidate invocation
GBAEH-R33 emitted artifact <= 524288 bytes
GBAEH-R34 existing Qualification Pack accepts structurally valid generated artifact under its own contract
GBAEH-R35 mutation disposition is split: consumer-contract mutations rejected by Qualification Pack; profile/mechanism-valid-looking mutations rejected by verify_expected_experiment_binding_v0 before consumer
GBAEH-R36 harness performs no network/tool/repo/Memory/Knowledge side effects; no claim about arbitrary callable ambient effects
GBAEH-R37 Kernel/Planner/Conversation/runtime/provider code delta = 0
GBAEH-R38 support_sufficient / Protected Finalization wiring = 0
GBAEH-R39 RDD Stage 2 delta = 0
GBAEH-R40 authority_effect = none
~~~

Additional causal negatives embedded in R02/R16/R26/R28-R30/R35:

- fault map missing/extra/duplicate/reordered/shifted;
- profile valid but different from expected;
- harness digests replaced by other valid SHA-256 values;
- mechanism metadata valid but different from expected identity/config;
- candidate mutates received material;
- candidate invocation omitted for an eligible input.

Causal RED debe provenir de ausencia del harness/profile/expected-binding behavior,
no de romper tests ya verdes.

## 14. Future E2E-equivalent

~~~text
exact case-set
→ exact closed experiment profile
→ recompute expected case-set binding
→ existing blind projection
→ structural checks
→ existing support-assessment envelope
→ bounded deterministic test assessor
→ exactly 13 eligible real candidate calls
→ 19 bound observations
→ exact V0.1 result artifact
→ verify_expected_experiment_binding_v0
→ existing Qualification Pack
→ deterministic terminal qualification
~~~

El deterministic test assessor valida infraestructura, no desempeño productivo.

Negativos obligatorios:

- ground-truth/ID leakage;
- profile unknown/missing/extra/duplicate/type drift;
- fault-map missing/extra/duplicate/reordered/shifted;
- role collision;
- SUBJECT/EVIDENCE_MATERIAL drift;
- unavailable/malformed/exception;
- missing eligible candidate invocation;
- candidate mutation of received material;
- case-set drift;
- mechanism valid-but-different from expected;
- harness/budget/attempt digest replaced by other valid SHA-256;
- observation/case-set mutation;
- missing/duplicate observation;
- oversize artifact.

El E2E debe distinguir:

~~~text
expected-binding verifier rejection
!= Qualification Pack rejection
~~~

y registrar cuál frontera produjo el fail-closed.

## 15. Correction Budget

~~~text
max correction rounds: 2
~~~

Permitido en future PR-B: sólo los tres archivos congelados y ajustes
directamente ligados dentro de ese scope.

Cualquier necesidad de src/malak/**, case-set/consumer changes, dependencies,
network, provider selection, Kernel/Planner/Security/support_sufficient o Stage 2:

~~~text
STOP → scope review
~~~

## 16. Candidate invalidation

Invalidan Evidence afectada:

- Git candidate;
- case-set bytes/schema;
- any validated experiment profile semantic field;
- expected mechanism descriptor/config;
- harness/attempt/budget policy;
- blind projection semantics;
- support-assessment envelope;
- artifact schema;
- digest recipes/canonicalization;
- candidate mechanism/config identity.

Un profile change puede conservar algunos subset digests si el subset no cambia,
pero siempre cambia `harness_policy_digest` porque éste cubre el profile validado
completo.

No se reutiliza PASS stale.

## 17. File Coverage

Ledger asociado:

docs/project/sprints/proposals/MALAK-E3-GOVERNED-BLIND-ASSESSOR-EXPERIMENT-HARNESS-V0-G0-G1-FILE-COVERAGE-20261004.tsv

Baseline:

~~~text
tracked files discovered = 367
recursive tree truncated = false
concept files explicitly inventoried = 7
~~~

## 18. Gate state — PR-A

~~~text
Construction Preflight                 WRITER CANDIDATE PASS
G0 / admission                         WRITER CANDIDATE PASS
Component / Logic Reuse Review         REUSE / COMPOSE / ADAPT
Necessity & Complexity Review          WRITER CANDIDATE PASS
Security Horizon Check                 WRITER CANDIDATE PASS
G1 design                              CORRECTED WRITER CANDIDATE PASS
Malāk Alignment Matrix                 COMPLETE
Critical Contract Hardening            CORRECTED WRITER CANDIDATE PASS
Four Questions                         PASS / PASS / PASS / PASS
Design 4R                              CORRECTED WRITER PASS FOR RE-REVIEW
RDD Stage 1 Design Check               CORRECTED WRITER PASS FOR RE-REVIEW
prior independent pre-RED review       FAIL — preserved
bounded design correction              ROUND 1 / 2
independent pre-RED re-review           PENDING
RED                                    NOT AUTHORIZED
GREEN                                  NOT AUTHORIZED
Implementation PR                      NOT CREATED
model/provider experiment              NOT AUTHORIZED
Ready / Merge                          OWNER ONLY
RDD Stage 2                            NOT AUTHORIZED
authority_effect                       none
~~~

## 19. Next lawful transition


~~~text
independent pre-RED Design Review on exact PR-A candidate
→ PASS | FAIL | INCONCLUSIVE
~~~

PASS no autoriza RED automáticamente. Después corresponde human review y las
decisiones exclusivas del Owner sobre Ready/Merge. Sólo con Design integrado en
main puede crearse la future Implementation PR desde ese baseline.
