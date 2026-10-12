---
title: Malāk E3 Governed Hybrid Verification Composition V0 — G0/G1 Design
status: g0_g1_candidate
authority: non_normative
language: es
date: 2026-10-12
baseline_commit: a2b9122719866258182bfef883ca0dd3737f38f0
baseline_tree: a6e04894e2d63422833fb39553fea95f7656c4e7
trigger_issue: 280
research_issue: 278
supporting_research_pr: 279
risk_class: 3_HIGH
critical_contract: true
authority_effect: none
implementation_authorized: false
red_authorized: false
green_authorized: false
support_sufficient_wiring_authorized: false
protected_finalization_wiring_authorized: false
u08_authorized: false
kernel_delta: 0
planner_delta: 0
---

# Malāk E3 Governed Hybrid Verification Composition V0 — G0/G1 Design

## 1. Estado y propósito

Esta unidad formaliza G0/G1 de la dirección seleccionada para investigar la
evolución de E3 después de la campaña G-01 V0.4.

La pregunta no es:

> ¿qué modelo debemos instalar para que reemplace a Malāk como árbitro semántico?

La pregunta es:

> ¿cómo puede Malāk conservar toda authority y settlement mientras utiliza
> workers semánticos reemplazables únicamente para el residuo que no puede
> resolverse de forma determinista?

Esta unidad es exclusivamente Design / Documentation.

No implementa runtime, no selecciona modelo/provider, no modifica el corpus V0.4,
no produce support_sufficient, no conecta Protected Finalization y no desbloquea
U08.

~~~text
Design != Implementation
Observation != Decision
Evidence != Authority
Qualification PASS != Production Authorization
~~~

## 2. Baseline exacto

~~~text
repository                 Aranwill/jarvis
main                       a2b9122719866258182bfef883ca0dd3737f38f0
tree                       a6e04894e2d63422833fb39553fea95f7656c4e7
tracked baseline blobs     387
recursive tree truncated   false
~~~

El archivo expresamente rechazado por AGENTS.md:

~~~text
PROJECT - MANIFIESTO MALAK (1).docx
~~~

no está presente en el baseline y no fue leído, resumido ni procesado.

El File Coverage Ledger de esta unidad clasifica los 387 blobs del baseline y
registra separadamente los dos candidate additions de PR-A.

## 3. Construction Preflight

~~~text
preflight_version            0.1.0
repository                   Aranwill/jarvis
baseline                     a2b9122719866258182bfef883ca0dd3737f38f0
work_unit                    issue #280
work_type                    MATERIAL_G0_G1_DESIGN
owner_instruction            avanzar después del law-compatibility review de Option C
current_candidate            none antes de PR-A
last_stable_checkpoint       main@a2b9122719866258182bfef883ca0dd3737f38f0

P0 repository/baseline       PASS
P1 sources/hierarchy         PASS
P2 invariants                PASS
P3 authority direction       PASS
P4 reuse/necessity           PASS / COMPOSE
P5 risk                      3_HIGH
critical_contract            YES
Design 4R                    REQUIRED
Candidate FULL 4R            future implementation only
RDD Stage 1 Design Check     REQUIRED
RDD Stage 2                  REQUIRED only for future risk-3/4 implementation candidate
P6 scope                     FROZEN
candidate identity strategy  Git commit/tree for PR-A; future PR-B separately bound
result                       PASS
authority_effect             none
~~~

Construction Preflight PASS sólo permite entrar a G0/G1. No constituye
aprobación del design ni autorización de implementación.

## 4. Fuentes reconciliadas

### 4.1 Autoridad superior / método

Reconciliadas contra el baseline exacto:

- AGENTS.md;
- Cognitive Constitution;
- Governance Constitution;
- Blueprint;
- Kernel specification;
- Architecture Quality Gates;
- SECURITY.md;
- ADR-002, ADR-003, ADR-004, ADR-005 y ADR-006;
- Engineering Method;
- Construction Protocol;
- Construction Preflight;
- Development Checklist.

### 4.2 CURRENT / planificación / conceptos

Reconciliados:

- implementation roadmap;
- ideas.md;
- concepts/README.md;
- Research Horizon Map;
- Evidence-Bound Cognition Foundation;
- Cognitive Dataset Foundation;
- Governed Self-Review Bootstrap;
- Governed Ephemeral Agent Execution reference;
- Governed Swarm / Long-Horizon reference.

Los conceptos y research permanecen no normativos.

### 4.3 Baseline técnico E3 / assurance

Reconciliados:

- E3 Structured Evidence Role Binding V0;
- E3 Governed Evidence Support Assessment V0;
- E3 Governed Support Evidence Routing V0;
- deterministic oracle qualification;
- Positive Qualification Consumption Trust Boundary V0;
- blind assessor / qualification machinery;
- ground-truth repair V0.4;
- src/malak/capabilities/_engineering_analysis.py;
- src/malak/capabilities/_engineering_qualification_consumption.py;
- src/malak/core/assurance_signal_projection.py;
- src/malak/core/protected_finalization.py;
- src/malak/app/composition.py;
- tests focalizados correspondientes;
- V0.4 cases/profile.

### 4.4 Investigación externa

Issue #278 y Draft PR #279 contienen evidencia comparativa externa.

Disposición:

~~~text
external research = CORROBORATION / IMPLEMENTATION_INPUT candidate
external research != authority
external pattern != Malāk architecture
~~~

PR #279 no es prerequisite normativo de este G0/G1.

## 5. Invariantes superiores

La composición debe preservar como mínimo:

~~~text
CC-003 evidence > speculation
CC-005 deterministic sufficient rule before unnecessary probabilistic verification
CC-006 additional cognition only for a material deficit
CC-011 Generation != Finalization
CC-012 material finalization requires applicable assurance
CC-013 missing required assurance -> fail closed

GOV-001 Human/User retains operational authority
GOV-004 least privilege
GOV-005 separation of responsibilities

Blueprint:
Kernel First
Capability First
Human in Control
Model Agnostic
R-017..R-020 directional authority/evidence
R-022 protected finalization

SECURITY:
Model != System
Intelligence != Authority
Evidence != Authority
unknown/invalid/unverifiable != permission
~~~

## 6. G0 — problema real

### HVC-01 — El role monolítico G-01 no ha sido calificado

La evidencia V0.4 permanece intacta.

~~~text
gemma4:12b              NOT_QUALIFIED_FOR_G01
qwen3.5:9b              NOT_QUALIFIED_FOR_G01
granite4.2:8b           NOT_QUALIFIED_FOR_G01
deepseek-coder-v2:16b   NOT_QUALIFIED_FOR_G01 / SAFETY_FLOOR_VIOLATION
gpt-oss:20b             MODEL_CONTRACT_INCOMPATIBLE
~~~

Disposición:

~~~text
PRESERVE
DO NOT weaken V0.4
DO NOT tune ground truth from model output
~~~

### HVC-02 — E3 ya separa deterministic envelope de inferential residual

El baseline no es model-first.

route_governed_support_evidence_v0 ya distingue:

~~~text
DETERMINISTIC
INFERENTIAL
INSUFFICIENT
~~~

y el positive qualification consumption boundary sólo eleva a DETERMINISTIC una
qualification exacta, admitida, binding-correct y temporalmente válida.

Disposición:

~~~text
REUSE
~~~

### HVC-03 — Seis clases del corpus ya no dependen del assessor

V0.4 conserva:

~~~text
18 cases
19 observed inputs
13 candidate invocations
~~~

Las clases C10/C11/C12/C14/C15/C17 poseen resolución nativa dentro del envelope
vigente.

Disposición:

~~~text
PRESERVE native ownership
never return these responsibilities to a semantic worker
~~~

### HVC-04 — El gap material es el residuo semántico, no ausencia de inteligencia general

El residuo incluye, según caso:

- material bearing;
- relevant-but-insufficient support;
- compound partial support;
- compatible limiting evidence;
- unresolved counterevidence;
- authority/relevance separation;
- rationale overclaim;
- unsupported high-confidence claim;
- scope dependency.

Estas propiedades no deben colapsarse automáticamente en una única confianza
de modelo.

### HVC-05 — El downstream de assurance ya existe y no debe ser duplicado

El baseline contiene:

~~~text
Assurance Signal Authority / Projection G2
        ↓
ProtectedFinalizationInput
        ↓
Protected Finalization G2A
        ↓
ACCEPT | ABSTAIN | BLOCK
~~~

E3 no debe crear un segundo finalizer.

### HVC-06 — support_sufficient continúa siendo una frontera protegida

~~~text
E3 assessment SUPPORTED
!= semantic truth
!= support_sufficient
!= Final Response
!= authority
~~~

Esta unidad no cambia esa separación.

## 7. Component / Logic Reuse Review

| Superficie | Disposición | Uso permitido en esta dirección |
|---|---|---|
| Governed Evidence Support Assessment V0 | REUSE / ADAPT | envelope exacto de subject/evidence + output bounded |
| Governed Support Evidence Routing V0 | REUSE | deterministic-first + inferential residual |
| Deterministic Oracle Qualification | REUSE | full covered deterministic questions |
| Positive Qualification Consumption Boundary V0 | REUSE | positive deterministic reliance sólo con admission exacta |
| Blind Assessor Experiment + Qualification Pack | REUSE / ADAPT | patrón de blind qualification para futuros mechanisms |
| V0.4 corpus | REUSE as benchmark | preservar monolithic benchmark; no tuning |
| Assurance Signal Authority / Projection G2 | REUSE downstream | no semantic truth; sólo projection autorizada |
| Protected Finalization G2A | REUSE unchanged | finalization remains separate |
| Security PDP/PEP | REUSE for permission | authorization != semantic truth |
| Kernel | NO_CHANGE | 0 lógica E3/verification |
| Planner | NO_CHANGE | no new semantic authority |
| SemanticEngine / VerificationGovernor | REJECT | nueva autoridad/subsystem no justificada |
| ResponseAssuranceLayer | REJECT | ADR-005 ya rechazó crearla por anticipación |
| HybridVerificationManager | REJECT | responsabilidad puede expresarse por composición |

Resultado:

~~~text
reuse_disposition = COMPOSE
new_component_fit = NOT_DEMONSTRATED
NEW component      = NOT_ADMISSIBLE
~~~

## 8. Necessity & Complexity Review

Necesidad demostrada:

~~~text
YES:
bounded semantic residual remains after deterministic routing
current general-model role is not qualified

NO:
new governance layer
new Kernel responsibility
always-on ensemble
global semantic score
new persistent state
new model registry
new manager/service
~~~

La respuesta mínima no es implementar toda la research ladder.

La respuesta mínima es definir cómo se inserta una futura observación semántica
sin cambiar authority ni finalization.

## 9. G1 — diseño seleccionado

Nombre de trabajo:

~~~text
E3 Governed Hybrid Verification Composition V0
~~~

No es una nueva layer.

Es una composición conceptual de fronteras existentes más un residuo semántico
acotado.

~~~text
exact governed E3 subject + evidence
        ↓
existing structural/binding validation
        ↓
existing deterministic routing
        ├─ fully covered oracle
        │      ↓
        │  DETERMINISTIC
        │
        └─ inferential residual
               ↓
      future bounded semantic mechanism
               ↓
      semantic observation(s)
      authority_effect = none
               ↓
      deterministic native settlement
               ↓
SUPPORTED | INSUFFICIENT | INCONCLUSIVE
               ↓
STOP in this design
~~~

El STOP es deliberado.

Esta unidad no conecta el resultado con support_sufficient ni Protected
Finalization.

## 10. Separación de responsabilidades

### 10.1 Malāk / upstream governed policy

Posee:

- qué pregunta se evalúa;
- qué evidence packet exacto aplica;
- si existe oracle determinista;
- qué assurance depth está permitida/requerida;
- si corresponde invocar cognición adicional;
- budgets y límites;
- autorización de tools/network cuando una unidad futura los requiera;
- escalación;
- finalization downstream.

### 10.2 Semantic worker / verifier

Puede:

- evaluar únicamente el material entregado por contrato;
- producir observaciones semánticas acotadas;
- declarar UNKNOWN;
- devolver evidence deficit;
- devolver su mechanism identity/provenance cuando el contrato lo exija.

No puede:

- decidir policy;
- elegir su propio assurance floor;
- ampliar scope;
- solicitar privilegios por efecto automático;
- iniciar tools/network;
- mutar Memory/Knowledge;
- persistir authority-bearing state;
- producir support_sufficient;
- llamar Protected Finalization;
- autorizar operación;
- ordenar upstream work;
- auto-promoverse.

### 10.3 Native settlement

Posee una policy determinista versionada sobre observaciones ya admitidas.

No decide que una observación probabilística sea verdad.

Decide cómo se trata conservadoramente un conjunto explícito de observaciones
bajo el contrato vigente.

## 11. Dirección de comunicación y authority

Compatible con ADR-003:

~~~text
CONTROL / REQUEST / POLICY / PERMISSION
Malāk upstream
        ↓
semantic worker downstream

RESULT / FINDING / OBSERVATION / EVIDENCE DEFICIT
Malāk upstream
        ↑
semantic worker downstream

upward authority_effect = none
~~~

Prohibido:

~~~text
verifier -> run search
verifier -> call tool
verifier -> change policy
verifier -> choose new model
verifier -> request more privilege
verifier -> support_sufficient
verifier -> final ACCEPT
~~~

Si el verifier detecta evidencia ausente:

~~~text
semantic result:
EVIDENCE_DEFICIT / EXTERNAL_DEPENDENCY / UNKNOWN
        ↑
Malāk upstream policy decides:
abstain | acquire evidence | escalate | stop
~~~

## 12. Claim decomposition

La investigación externa sugiere beneficio de claim-level verification, pero
claim decomposition es también una transformación semántica y no se convierte
por ello en truth.

Reglas de diseño:

1. el original claim permanece exacto y bound;
2. ningún claim part puede sustituir silenciosamente al original;
3. coverage entre original y parts debe ser explícita;
4. partial coverage nunca se agrega como full support;
5. omitted material clause produce UNKNOWN/INCONCLUSIVE;
6. una decomposición probabilística conserva authority_effect=none;
7. un decomposer requiere qualification propia;
8. cuando upstream ya dispone de claim parts estructurados no debe invocarse un
   decomposer probabilístico innecesario;
9. keyword splitting no constituye semantic decomposition válida.

Disposición:

~~~text
claim decomposition = ADMIT as optional child gate
always-on decomposition = REJECT
implementation in this unit = NO
~~~

## 13. Specialized semantic verifier

Un MiniCheck/AlignScore/NLI-style mechanism o un frontier model puede ser
evaluado en el futuro como implementation candidate del mismo bounded role.

La arquitectura no se acopla a un tipo concreto.

Requisitos mínimos futuros:

~~~text
replaceable mechanism
exact input binding
no hidden ground truth
bounded structured output
no side effects
no policy authority
no self-certification
fail closed on malformed/unavailable output
qualification bound to exact mechanism/config/schema/corpus
authority_effect = none
~~~

Disposición:

~~~text
specialized verifier experiment = ADMIT as future child gate
specific verifier/model          = NOT SELECTED
~~~

## 14. Semantic observation — mínima responsabilidad candidata

El diseño no congela todavía un schema productivo, pero congela las dimensiones
que una futura child unit puede evaluar sin mezclarlas con authority:

~~~text
subject binding
claim / claim-part identity when applicable
material bearing:
    MATERIAL | NON_MATERIAL | UNKNOWN
semantic stance:
    SUPPORTS | LIMITS | CONTRADICTS | UNKNOWN
scope dependency:
    NONE | EXTERNAL_REQUIRED | UNKNOWN
coverage:
    FULL | PARTIAL | UNKNOWN
mechanism identity/provenance
authority_effect = none
~~~

Estas dimensiones son candidate design material.

Los nombres exactos, cardinalidad y schema deben endurecerse en el child gate
antes de RED.

## 15. Deterministic native settlement

La futura settlement policy debe ser conservadora.

Invariantes mínimas:

~~~text
UNKNOWN never becomes positive by default
PARTIAL never becomes FULL
missing required observation never becomes favorable
unresolved contradiction prevents positive settlement
external dependency unresolved prevents positive settlement
binding drift -> INCONCLUSIVE
malformed/unavailable verifier -> INCONCLUSIVE
self-certification -> INCONCLUSIVE
~~~

Un outcome E3 SUPPORTED sigue siendo un domain assessment:

~~~text
E3 SUPPORTED
!= support_sufficient
!= finalization ACCEPT
!= semantic truth
!= authority
~~~

Por tanto, un futuro verifier qualified puede contribuir a un E3 SUPPORTED sin
obtener por ello authority sobre Final Response.

## 16. Refutation / multiple models

No son parte obligatoria del camino normal.

Pueden ser invocados en una child unit futura únicamente cuando una upstream
policy gobernada determine que el riesgo/materialidad justifica cognition
adicional.

~~~text
reviewer != authority
refuter != authority
agreement != truth
vote != authority
~~~

ADR-005 rechaza multiple judges always-on como default.

Disposición:

~~~text
selective escalation = ADMIT
always-on ensemble    = REJECT
~~~

## 17. Calibrated abstention

La investigación de conformal/selective prediction se conserva como
IMPLEMENTATION_INPUT de investigación.

No se promueven thresholds en este G1.

Regla compatible:

~~~text
uncertainty / out-of-calibration
→ UNKNOWN / abstain / escalate
never favorable default
~~~

Una guarantee estadística futura sólo puede reclamarse bajo los supuestos
explicitados por su propio gate y dataset.

## 18. Relación con Assurance Signal / Protected Finalization

Esta composición termina antes de Assurance Signal production.

~~~text
E3 semantic settlement
        ↓
NO DIRECT WIRING IN THIS UNIT
        X
support_sufficient
        ↓
Assurance Signal Projection
        ↓
Protected Finalization
~~~

Una futura integración requerirá una unidad separada que demuestre quién puede
producir SUPPORT_SUFFICIENT y bajo qué evidence/qualification/authorization.

Esta G1 no presupone que E3 SUPPORTED sea condición suficiente.

## 19. Preservación G-01 V0.4

G-01 V0.4 conserva su significado:

~~~text
MONOLITHIC ASSESSOR CAPABILITY BENCHMARK
~~~

No se cambia:

- case-set;
- prompt;
- expected outcomes;
- reason taxonomy;
- safety floor;
- historical FAIL evidence.

Su utilidad futura:

- benchmark de modelos generalistas;
- control experimental;
- comparación contra una arquitectura descompuesta;
- señal de regresión.

No será usado para forzar el design nuevo a imitar exactamente un role que
eventualmente deje de ser productivo.

## 20. Qualification futura

La arquitectura requiere separar component qualification de system qualification.

### 20.1 Mechanism qualification

Futuro child gate.

Debe medir el role exacto del semantic mechanism, no un role mayor.

Hard properties candidatas:

~~~text
blind ground truth
exact binding
output schema integrity
self-certification blocked
malformed/unavailable fail closed
no authority effect
no side effects
UNKNOWN preserved
false positive behavior measured
~~~

### 20.2 Settlement qualification

Debe probar que la deterministic policy no convierte:

~~~text
partial -> full
unknown -> supported
contradiction -> supported
scope deficit -> supported
binding drift -> supported
~~~

### 20.3 System qualification

Debe medir la salida E3 completa después de envelope + mechanism + settlement.

La propiedad prioritaria es:

~~~text
probabilistic error
must not silently cross
a protected positive-reliance boundary
~~~

La eventual producción de support_sufficient requiere qualification separada.

## 21. Secuencia de child gates

Este G1 no autoriza implementación.

Si el Owner integra PR-A, la secuencia candidata es:

~~~text
HVC-A — Semantic Observation / Ground-Truth Contract
        no model; schema + blind ground truth + discriminability

HVC-B — Specialized Semantic Verifier Experiment
        exact candidate mechanism; offline/isolated

HVC-C — Deterministic Settlement
        native policy over admitted observations

HVC-D — E3 System Qualification
        envelope + mechanism + settlement

HVC-E — Assurance Signal bridge
        OPTIONAL / separate admission
        only if HVC-D demonstrates sufficient need
~~~

Claim decomposition puede abrirse entre HVC-A y HVC-B como subunidad separada
si el observation contract demuestra que compound claims no pueden evaluarse de
forma suficiente sin ella.

No se implementa todo el ladder en una sola PR.

## 22. First next unit recomendado

Después del eventual merge humano de este design:

~~~text
HVC-A — Semantic Observation / Ground-Truth Contract
~~~

Razón:

- define qué información debe producir un verifier;
- permite review ciego independiente antes de escoger modelos;
- evita benchmark fitting;
- permite saber si claim decomposition es realmente necesaria;
- no requiere runtime/network/provider;
- reduce riesgo antes de cualquier dependencia externa.

## 23. Malāk Alignment Matrix

| Source | Authority class | Invariant / intent | Baseline evidence | Disposition | Effect |
|---|---|---|---|---|---|
| Cognitive Constitution | constitutional | evidence, proportionality, minimization, Generation != Finalization | CC-003/005/006/011/012/013 | ADOPT | deterministic-first, bounded semantic residual |
| Governance Constitution | constitutional | Human in Control, least privilege, responsibility separation | GOV-001/004/005 | ADOPT | verifier has no authority |
| Blueprint | architecture | Kernel/Capability/Model Agnostic + directional authority | current layered architecture | ADOPT | Kernel/Planner delta 0 |
| Kernel specification | approved specification | orchestration only, no business logic | current Kernel | ADOPT | no HVC logic in Kernel |
| Architecture Quality Gates | architecture quality | Kernel stable; Capability First; Human in Control | current gates | ADOPT | composition, not new layer |
| SECURITY.md | protected policy | Zero Trust; Intelligence/Evidence != Authority | current PDP/PEP | ADOPT | no implicit trust or side effects |
| ADR-002 | accepted ADR | authorization decision/enforcement boundary | PDP/PEP | REUSE | authorization remains separate |
| ADR-003 | accepted ADR | downward control, upward evidence | current contracts | ADOPT | verifier returns evidence only |
| ADR-004 | accepted ADR | Specification & Verification First | this G0/G1 before RED | ADOPT | no implementation-first |
| ADR-005 | accepted ADR | evidence-bound progressive finalization | Protected Finalization G2A | ADOPT | no Response Assurance Layer |
| ADR-006 | accepted ADR | reliance guarantees non-transitive; fail closed | protected reliance policy | OBSERVE | no durable reliance in this unit |
| Progressive Cognitive Assurance | design lineage | probabilistic workers + deterministic governed rules | existing design | ADOPT | direct architectural ancestor |
| Assurance Signal Boundary | current implementation | authorized observation projection | G2 | REUSE downstream | no direct HVC wiring |
| E3 Routing | current implementation | deterministic/inferential/insufficient | current code/tests | REUSE | entry point before semantics |
| E3 Support Assessment | current implementation | bounded semantic assessment | current code/tests | ADAPT | future mechanism behind envelope |
| E3 Positive Qualification Consumption | current implementation | exact positive deterministic trust boundary | current code/tests | REUSE | no caller-controlled trust |
| V0.4 G-01 | evaluation evidence | monolithic role not qualified | current corpus + U06 evidence | PRESERVE | benchmark only |
| Evidence-Bound Cognition concept | non-normative | candidate -> evidence -> validation -> finalization | concept | ADAPT | research alignment only |
| Cognitive Dataset concept | non-normative | define behavior/benchmarks before training | concept | ADAPT | ground truth before model |
| Research Horizon | non-normative | research != authority | concept | ADOPT | external work remains input only |
| #278/#279 external research | research evidence | decomposition/verifiers/control patterns | issue/PR | OBSERVE / ADAPT | no copied architecture |

## 24. Security Horizon Check

### Prompt / Context Trust

Status:

~~~text
REQUIRES_REINFORCEMENT in future model-based child gate
~~~

No model execution is authorized here.

Future semantic mechanisms must receive only bounded, explicit evidence material
and must not interpret evidence text as privileged instruction.

### AI supply chain

Status:

~~~text
DEFERRED until exact external/model artifact selected
~~~

A future model/verifier requires provenance, integrity, license and compatibility
review proportional to its deployment.

### Network / tools

~~~text
NOT ACTIVATED
~~~

No child worker may initiate network/tools unless a separate gate authorizes it.

### Memory / Knowledge

~~~text
NOT ACTIVATED
~~~

No persistence, retrieval promotion or Knowledge admission follows from semantic
verification.

### Human in Control

~~~text
PASS
~~~

Owner remains Ready/Merge authority and any future sensitive promotion remains
separately governed.

## 25. Critical Contract Hardening

Known material ambiguities and dispositions:

### A1 — Does verifier output equal semantic truth?

~~~text
NO
verifier output = bounded observation
~~~

### A2 — Does E3 SUPPORTED equal support_sufficient?

~~~text
NO
explicitly prohibited
~~~

### A3 — Can verifier initiate evidence acquisition?

~~~text
NO
it may report deficit; upstream Malāk decides
~~~

### A4 — Can multiple models create truth by consensus?

~~~text
NO
agreement is evidence at most
~~~

### A5 — Can claim decomposition replace original claim?

~~~text
NO
original remains bound; coverage required
~~~

### A6 — Is claim decomposition mandatory?

~~~text
NO
deficit-driven only
~~~

### A7 — Does the design create a new layer/service/manager?

~~~text
NO
composition of existing boundaries
~~~

### A8 — Does missing verifier capability lower the assurance floor?

~~~text
NO
UNKNOWN / INCONCLUSIVE / abstain
~~~

### A9 — Can a specific specialized verifier become architectural dependency?

~~~text
NO
mechanism must remain replaceable
~~~

### A10 — Does this design unblock U08?

~~~text
NO
U08 remains BLOCKED
~~~

Hardening result:

~~~text
known material ambiguity unresolved = 0
fail-open path admitted             = 0
authority expansion                 = 0
~~~

## 26. Cuatro preguntas de ley

### 1. ¿Respeta Blueprint?

PASS.

- Kernel delta 0;
- Planner delta 0;
- Model Agnostic;
- Capability/contract composition;
- no new architecture layer;
- directional authority preserved.

### 2. ¿Respeta Cognitive Constitution?

PASS.

- deterministic first;
- uncertainty explicit;
- Generation != Finalization;
- evidence remains separate from authority;
- additional cognition is deficit-driven.

### 3. ¿Respeta Governance Constitution?

PASS.

- Human in Control;
- least privilege;
- no self-elevation;
- verifier cannot authorize itself or anything upstream.

### 4. ¿Mantiene o reduce complejidad del Kernel?

PASS.

~~~text
Kernel delta = 0
~~~

## 27. Design 4R

### Risk — PASS

Evaluado:

- false positive semantic support;
- authority laundering;
- direct support_sufficient promotion;
- hidden upward control;
- model/provider coupling;
- always-on cognitive cost;
- claim decomposition omission;
- majority-vote truth laundering;
- missing-signal favorable default;
- security/prompt boundary in future model gate.

Mitigación:

- authority_effect none;
- exact bindings;
- fail closed;
- native deterministic settlement;
- independent qualification;
- child gates;
- no support_sufficient wiring;
- no side effects.

Residual risk:

~~~text
semantic verifier error remains possible
~~~

Ese riesgo es justamente la razón para separar observation, settlement y
finalization.

### Readability — PASS

Responsabilidades separadas:

~~~text
routing
semantic observation
settlement
assurance signal production
projection
finalization
authority
~~~

No se introducen nombres que oculten ownership detrás de un manager universal.

### Reliability — PASS

Diseño exige:

- closed enums / bounded output en futuras specs;
- exact identity/binding;
- no favorable defaults;
- deterministic aggregation;
- candidate-bound qualification;
- invalidation on mechanism/schema/corpus change.

### Resilience — PASS

Fallos esperados:

~~~text
verifier unavailable  -> INCONCLUSIVE
malformed output       -> INCONCLUSIVE
coverage unknown       -> INCONCLUSIVE
scope dependency       -> INCONCLUSIVE / escalate
contradiction unresolved -> INCONCLUSIVE
resource/model unavailable -> no assurance downgrade
~~~

## 28. RDD Stage 1 Design Check

~~~text
candidate identity strategy                PASS
baseline/candidate binding                 PASS
evidence provenance                       PASS
Writer / Reviewer / Validator / Authority PASS
PASS | FAIL | INCONCLUSIVE discipline     PASS
INCONCLUSIVE != PASS                      PASS
candidate change invalidates evidence     PASS
bounded correction defined                PASS
independent fix validation future         PASS
authority_effect                          none
RDD Stage 2 applicability                 future risk-3/4 implementation: REQUIRED
~~~

Resultado:

~~~text
RDD_STAGE_1_DESIGN_CHECK = PASS
~~~

Este PASS no es Candidate Conformance y no autoriza RED.

## 29. Scope freeze de PR-A

Allowed candidate additions:

~~~text
docs/project/sprints/proposals/MALAK-E3-GOVERNED-HYBRID-VERIFICATION-COMPOSITION-V0-G0-G1-DESIGN-20261012.md
docs/project/sprints/proposals/MALAK-E3-GOVERNED-HYBRID-VERIFICATION-COMPOSITION-V0-G0-G1-FILE-COVERAGE-20261012.tsv
~~~

Fuera de scope / forbidden:

~~~text
src/**
tests/**
scripts/**
evaluations/**
configs/**
AGENTS.md
SECURITY.md
docs/governance/**
docs/architecture/blueprint.md
docs/architecture/kernel.md
accepted ADRs
runtime/model/provider
network/tools
Memory/Knowledge
support_sufficient
Protected Finalization wiring
U08
~~~

Si el design requiere cambiar una fuente superior:

~~~text
STOP
→ reopen G0/G1
~~~

## 30. Candidate Identity y correction budget

PR-A candidate identity:

~~~text
Git commit SHA + tree SHA
base = a2b9122719866258182bfef883ca0dd3737f38f0
~~~

Design correction budget:

~~~text
allowed_files          2 candidate docs
production_delta       0
test_delta             0
architecture_law_delta 0
max_fix_rounds         2
Kernel_delta           0
Planner_delta          0
authority_delta        0
~~~

Un finding que requiera salir de ese budget produce ESCALATE, no scope expansion.

## 31. Criterios de aceptación de PR-A

- Construction Preflight PASS.
- 387/387 baseline blobs classified; silently omitted = 0.
- Malāk Alignment Matrix completa.
- Component/Logic Reuse Review = COMPOSE.
- NEW component = NOT_ADMISSIBLE.
- Security Horizon Check dispuesto.
- Critical Contract Hardening PASS.
- cuatro preguntas de ley PASS.
- Design 4R PASS.
- RDD Stage 1 Design Check PASS.
- G-01 V0.4 preservado sin cambios.
- U08 permanece BLOCKED.
- no runtime/code/test delta.
- authority_effect none.
- Ready/Merge sólo Owner.

## 32. Terminal G0/G1 result

~~~text
G0 result                         PASS
G1 result                         PASS / ADAPT
selected direction                GOVERNED_HYBRID_VERIFICATION_COMPOSITION
architecture mode                 REUSE + ADAPT + COMPOSE
new governance layer              REJECTED
new component                     NOT_ADMISSIBLE
first child gate                  HVC-A semantic observation / ground-truth contract
specific verifier                 NOT_SELECTED
claim decomposition               OPTIONAL / separate child admission
support_sufficient                NOT WIRED / NOT AUTHORIZED
Protected Finalization integration NOT AUTHORIZED
G-01 V0.4                         PRESERVED
U08                               BLOCKED
Kernel delta                      0
Planner delta                     0
authority_effect                  none
implementation                    NOT AUTHORIZED
RED                               NOT AUTHORIZED
GREEN                             NOT AUTHORIZED
Ready / Merge                     OWNER ONLY
~~~

La dirección seleccionada no coloca un verifier por encima de Malāk.

Malāk conserva policy, routing, settlement, finalization y authority. Los
mecanismos probabilísticos permanecen workers acotados y reemplazables.
