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

### 6.9 Digest semantics

El producer debe ser regression-equivalent al Qualification Pack para:

- case_set_digest;
- input_instance_digest;
- semantic_input_digest;
- subject_fingerprint.

El producer calcula. El consumer recomputa.

~~~text
producer digest
!= trusted assertion

consumer recomputation mismatch
→ no PASS
~~~

### 6.10 Harness identity

El artifact existente exige:

~~~text
harness_policy_version
harness_policy_digest
budget_manifest_digest
attempt_policy_digest
~~~

Esos digests deben derivarse del exact experiment profile o de subsets
versionados del mismo; no pueden ser opacos supplied-by-caller.

Perfil mínimo:

~~~text
schema_version
harness_policy_version
execution_order
max_attempts_per_input
max_candidate_invocations
fault_modes
artifact_max_bytes
candidate_argument_policy
~~~

Valores V0:

~~~text
execution_order           SEQUENTIAL
max_attempts_per_input    1
max_candidate_invocations <= 17 NORMAL inputs
artifact_max_bytes        512 KiB
candidate_argument_policy EXISTING_SUPPORT_ASSESSMENT_MATERIAL_ONLY
~~~

No se congela token budget, temperatura ni provider retry policy de un modelo
real.

### 6.11 Mechanism identity

Metadata:

~~~text
mechanism_id
mechanism_version
mechanism_kind
config_digest
producer_subject_id
assessor_subject_id
model_provenance
~~~

El harness no decide trust.

MODEL_BASED metadata completa tampoco autoriza ejecutar un modelo en esta unidad.

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

H04 forged digests: producer recomputes; consumer independently recomputes.

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

H13 harness profile drift: changes identity/digests and invalidates Evidence.

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

## 11. Design 4R

### Risk — PASS

Revisados: leakage, lookup side channels, nested leakage, forged digests,
self-certification, skip/retry gaming, malformed outputs, identity drift, ambient
capabilities y Authority laundering.

Residual risk explícito: V0 no es OS/process sandbox. No bloquea el harness
evaluation-side; sí impide overclaim y ejecución real de provider sin gate propio.

### Readability — PASS

~~~text
case-set / ground truth
!= blind projection
!= experiment harness
!= candidate assessor
!= result artifact
!= qualification runner
!= runtime admission
!= authority
~~~

### Reliability — PASS

Schemas existentes, 19/19 inputs, attempts=1, sequential, producer/consumer
binding independiente y candidate/profile invalidation explícita.

### Resilience — PASS

Invalid input, binding drift, self-certification, unavailable/malformed assessor,
exceptions, incomplete artifact, oversize y consumer mismatch son fail-closed.

Terminal Writer:

~~~text
DESIGN 4R — WRITER CANDIDATE = PASS
blocking design findings = 0
independent pre-RED review = PENDING
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

Este Writer Design Check no sustituye independent pre-RED review.

## 13. Future RED requirements

Sólo después de review/merge humano de PR-A y autorización separada de RED:

~~~text
GBAEH-R01 exact case-set V0.1 required
GBAEH-R02 exact experiment-profile schema/version required
GBAEH-R03 18 cases / 19 inputs / zero skip
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
GBAEH-R14 FORCE_UNAVAILABLE calls real candidate zero times
GBAEH-R15 FORCE_MALFORMED_OUTPUT calls real candidate zero times
GBAEH-R16 NORMAL input calls candidate at most once
GBAEH-R17 candidate exception has no retry and remains non-positive
GBAEH-R18 malformed candidate record remains non-positive
GBAEH-R19 output obeys existing support-assessment result contract
GBAEH-R20 case_set_digest exact
GBAEH-R21 input_instance_digest regression-equivalent to consumer
GBAEH-R22 semantic_input_digest regression-equivalent to consumer
GBAEH-R23 subject_fingerprint regression-equivalent to consumer
GBAEH-R24 observation digests producer-computed, not caller-supplied
GBAEH-R25 exact RESULTS/v0.1 schema
GBAEH-R26 exact mechanism metadata schema
GBAEH-R27 incomplete MODEL_BASED metadata rejected
GBAEH-R28 harness_policy_digest derived from exact profile
GBAEH-R29 budget_manifest_digest derived
GBAEH-R30 attempt_policy_digest derived
GBAEH-R31 execution order SEQUENTIAL
GBAEH-R32 one attempt / no automatic retry
GBAEH-R33 generated artifact <= 512 KiB
GBAEH-R34 existing Qualification Pack accepts valid generated artifact
GBAEH-R35 artifact mutation rejected by existing Qualification Pack
GBAEH-R36 no network/tool/repo/Memory/Knowledge side effects by harness
GBAEH-R37 Kernel/Planner/Conversation/runtime/provider code delta = 0
GBAEH-R38 support_sufficient / Protected Finalization wiring = 0
GBAEH-R39 RDD Stage 2 delta = 0
GBAEH-R40 authority_effect = none
~~~

Causal RED debe provenir de ausencia del harness/profile, no de romper tests ya
verdes.

## 14. Future E2E-equivalent

~~~text
exact case-set
→ exact experiment profile
→ existing blind projection
→ structural checks
→ existing support-assessment envelope
→ bounded deterministic test assessor
→ 19 bound observations
→ exact V0.1 result artifact
→ existing Assessor Qualification Pack
→ deterministic terminal qualification
~~~

Un deterministic test assessor basta para validar infraestructura. Su PASS no es
evidencia de un assessor productivo.

Negativos: leakage, role collision, binding drift, unavailable, malformed,
exception, artifact mutation, profile/case drift, missing/duplicate observation y
oversize.

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
- case-set bytes;
- experiment profile;
- harness/attempt/budget policy;
- blind projection semantics;
- support-assessment envelope;
- artifact schema;
- digest semantics;
- mechanism/config identity.

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
G1 design                              WRITER CANDIDATE PASS
Malāk Alignment Matrix                 COMPLETE
Critical Contract Hardening            WRITER CANDIDATE PASS
Four Questions                         PASS / PASS / PASS / PASS
Design 4R                              WRITER CANDIDATE PASS
RDD Stage 1 Design Check               WRITER CANDIDATE PASS
independent pre-RED review              PENDING
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
