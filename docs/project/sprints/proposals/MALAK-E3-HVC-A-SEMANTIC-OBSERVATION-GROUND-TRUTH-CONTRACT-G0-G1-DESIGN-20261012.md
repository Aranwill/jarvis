---
title: Malāk E3 HVC-A — Semantic Observation / Ground-Truth Contract — G0/G1 Design
status: g0_g1_candidate
authority: non_normative
language: es
date: 2026-10-12
baseline_commit: 26550b225e316bee6cff5cb0fb47b931e9335186
baseline_tree: 824f42c3262f86bea7e4b3a4973f132d5135e7be
trigger_issue: 282
parent_issue: 280
parent_design_pr: 281
corrective_ledger_issue: 271
risk_class: 3_HIGH
critical_contract: true
authority_effect: none
implementation_authorized: false
red_authorized: false
green_authorized: false
specific_verifier_selected: false
support_sufficient_wiring_authorized: false
protected_finalization_wiring_authorized: false
u08_authorized: false
kernel_delta: 0
planner_delta: 0
---

# Malāk E3 HVC-A — Semantic Observation / Ground-Truth Contract — G0/G1 Design

## 1. Propósito

Esta unidad formaliza el primer child gate del diseño integrado
`E3 Governed Hybrid Verification Composition V0`.

HVC-A responde únicamente:

> ¿Qué observación semántica mínima, explícita y discriminable debe poder producir
> un futuro verifier para que Malāk pueda evaluarla sin cederle policy, settlement,
> finalization ni authority?

Esta unidad es **Design / Documentation only**.

No ejecuta modelos, no selecciona provider, no modifica V0.4, no implementa
settlement, no produce `support_sufficient`, no conecta Protected Finalization y
no desbloquea U08.

```text
Semantic observation != semantic truth
Observation != settlement
Settlement != support_sufficient
Evidence != Authority
```

## 2. Baseline exacto y cobertura

```text
repository                 Aranwill/jarvis
main                       26550b225e316bee6cff5cb0fb47b931e9335186
tree                       824f42c3262f86bea7e4b3a4973f132d5135e7be
tracked baseline blobs     389
recursive tree truncated   false
candidate additions        2
silently omitted           0
```

El archivo expresamente rechazado por `AGENTS.md`,
`PROJECT - MANIFIESTO MALAK (1).docx`, no está presente en este baseline y no
fue leído ni procesado.

El File Coverage Ledger de esta unidad clasifica 389/389
blobs del baseline y registra separadamente los dos candidate additions.

## 3. Construction Preflight

```text
preflight_version            0.1.0
repository                   Aranwill/jarvis
baseline                     26550b225e316bee6cff5cb0fb47b931e9335186
work_unit                    issue #282
work_type                    MATERIAL_G0_G1_DESIGN
owner_instruction            "avanza jarvis"
parent_design                #280 / PR #281 integrated
last_stable_checkpoint       main@26550b225e316bee6cff5cb0fb47b931e9335186

P0 repository/baseline       PASS
P1 sources/hierarchy         PASS
P2 invariants                PASS
P3 authority direction       PASS
P4 reuse/necessity           PASS / REUSE + ADAPT + COMPOSE
P5 risk                      3_HIGH
critical_contract            YES
Design 4R                    REQUIRED
Candidate FULL 4R            future PR-B only
RDD Stage 1 Design Check     REQUIRED
RDD Stage 2                  REQUIRED for future risk-3 candidate
independent validation       REQUIRED for ground-truth discriminability
P6 scope                     FROZEN
candidate identity strategy  Git commit/tree; PR-A docs only
P7 result                    PASS
authority_effect             none
```

Preflight PASS autoriza únicamente continuar con G0/G1 de esta unidad. No
autoriza RED, GREEN ni implementación.

## 4. Fuentes reconciliadas

### 4.1 Autoridad y método

Reconciliadas:

- `AGENTS.md`;
- Cognitive Constitution;
- Governance Constitution;
- Blueprint;
- Kernel specification;
- Architecture Quality Gates;
- `SECURITY.md`;
- ADR-002, ADR-003, ADR-004, ADR-005 y ADR-006;
- Engineering Method;
- Construction Protocol v0.2.7;
- Construction Preflight v0.1.0;
- Development Checklist;
- Evidence Manifest y RDD Validation Receipt.

### 4.2 Estado, planificación y conceptos

Reconciliados:

- `README.md`;
- `docs/project/project_context.md`;
- `docs/project/implementation_roadmap.md`;
- `documents/projects/jarvis/ideas.md`;
- `docs/project/concepts/README.md`;
- `MALAK_RESEARCH_HORIZON_MAP.md`;
- `MALAK_COGNITIVE_DATASET_FOUNDATION.md`;
- `MALAK_EVIDENCE_BOUND_COGNITION_FOUNDATION.md`;
- referencias conceptuales relacionadas.

Estas fuentes conceptuales no adquieren autoridad.

### 4.3 Baseline técnico relevante

Reconciliados:

- `src/malak/capabilities/_engineering_analysis.py`;
- `src/malak/capabilities/_engineering_qualification_consumption.py`;
- E3 Governed Support Evidence Routing;
- positive qualification consumption;
- blind assessor / qualification machinery;
- `evaluations/e3_governed_evidence_support_assessor_v0/**`;
- `src/malak/core/assurance_signal_projection.py`;
- `src/malak/core/protected_finalization.py`;
- tests E3 / assurance / finalization aplicables.

## 5. G0 — problema exacto

### HVC-A-01 — El residuo semántico sigue siendo real

G-01 V0.4 permanece `NOT PASSED` para todos los candidates evaluados. El
resultado no se debilita ni se reetiqueta.

El problema no es ausencia de un modelo suficientemente grande; es que el role
monolítico mezcla varias decisiones semánticas que Malāk necesita observar y
settlear por separado.

### HVC-A-02 — El contrato actual ya ofrece bindings reutilizables

El baseline ya dispone de:

- `baseline_commit`;
- `focus_id`;
- `evidence_set_digest`;
- `relation_id`;
- `finding_fingerprint`;
- refs de evidencia por rol;
- outcomes y reasons actuales;
- blind projection y forbidden ground-truth keys.

Estos bindings deben reutilizarse. HVC-A no crea un sistema paralelo de identity.

### HVC-A-03 — Ground truth debe preceder al mecanismo

El parent design exige:

```text
contract / ground truth
before
specific verifier selection
```

Esto coincide con Specification & Verification First y con Cognitive Dataset:
primero definir comportamiento esperado, después evaluar mecanismo.

### HVC-A-04 — Observación y settlement deben quedar separados

Un future worker puede producir una observación. No puede convertirla en:

```text
SUPPORTED
support_sufficient
Final Response
Authority
```

La futura deterministic settlement pertenece a HVC-C.

### HVC-A-05 — El oracle debe ser ciego y discriminable

La experiencia V0.4 demuestra que las diferencias entre:

- irrelevant vs relevant-but-insufficient;
- compound partial vs generic insufficiency;
- limits vs contradiction;
- explicit external dependency vs ordinary uncertainty;

deben ser visibles y clasificables sin acceder a expected labels.

## 6. Component / Logic Reuse Review

| Superficie | Disposición | HVC-A |
|---|---|---|
| E3 subject/evidence bindings | REUSE | identidad exacta |
| GovernedEvidenceSupportAssessmentV0 | ADAPT | referencia de dominio, no settlement final |
| Governed Support Evidence Routing | REUSE | conserva deterministic-first |
| deterministic oracle qualification | REUSE | patrón de oracle y validación |
| blind assessor projection | REUSE / ADAPT | separación visible/hidden |
| V0.4 corpus | PRESERVE / REFERENCE | benchmark histórico, no modificar |
| qualification machinery | REUSE pattern | futura HVC-B, no ejecutar aquí |
| Assurance Signal | NO_CHANGE | downstream protegido |
| Protected Finalization | NO_CHANGE | fuera de alcance |
| Kernel / Planner | NO_CHANGE | delta 0 |
| new SemanticEngine / VerificationGovernor / Manager | REJECT | no necesidad demostrada |

Resultado:

```text
reuse_disposition = REUSE + ADAPT + COMPOSE
NEW component      = NOT_ADMISSIBLE
```

## 7. Necessity & Complexity Review

Necesario:

```text
YES
- contrato de observación semántica mínimo
- ground truth ciego
- reglas de discriminabilidad
- binding exacto
- comportamiento UNKNOWN/fail-closed
```

No necesario:

```text
NO
- nueva Capability
- nueva layer
- new manager/service/registry
- model/provider
- network/tools
- persistence
- global confidence score
- ensemble always-on
- claim decomposer always-on
```

## 8. G1 — contrato seleccionado

Nombre de artefacto de trabajo:

```text
SemanticObservationV0
```

Es un **contract**, no una Capability ni un servicio.

### 8.1 Binding mínimo

Toda observación futura debe estar ligada a:

```text
policy_version
baseline_commit
focus_id
evidence_set_digest
relation_id
finding_fingerprint
evidence_ref
claim_part_id?          # sólo si upstream ya provee una parte autorizada
authority_effect = none
```

`claim_part_id` no autoriza decomposición. Si upstream no aporta partes
estructuradas, la observación se liga al claim raíz mediante el
`finding_fingerprint`.

### 8.2 Dimensiones semánticas cerradas

```text
material_bearing:
  MATERIAL
  NON_MATERIAL
  UNKNOWN

semantic_stance:
  SUPPORTS
  LIMITS
  CONTRADICTS
  UNKNOWN

scope_dependency:
  NONE
  EXTERNAL_REQUIRED
  UNKNOWN

coverage:
  FULL
  PARTIAL
  UNKNOWN
```

### 8.3 Semántica normativa del contrato candidato

**MATERIAL**

El material visible puede cambiar la evaluación del soporte o suficiencia del
claim.

**NON_MATERIAL**

El material visible no guarda relación material con el claim ni con su
suficiencia evidenciaria. Autoridad documental de la fuente no vuelve relevante
un contenido no relacionado.

**UNKNOWN**

El packet acotado no permite determinar bearing sin asumir material externo.

**SUPPORTS**

El material aporta evidencia afirmativa para al menos una proposición material
del claim.

**LIMITS**

El material restringe, acota o declara no-establishment sin afirmar por sí mismo
una proposición incompatible con el claim.

**CONTRADICTS**

El material afirma una proposición materialmente incompatible con el claim.

**EXTERNAL_REQUIRED**

El packet identifica explícitamente una dependencia de evidencia fuera del
bounded packet que es necesaria para resolver la evaluación.

**FULL**

El soporte visible cubre todas las proposiciones materiales necesarias del claim
al nivel de evaluación aplicable.

**PARTIAL**

Existe soporte visible para al menos una proposición material, pero no para todas.

### 8.4 Combinaciones fail-closed

```text
NON_MATERIAL
→ semantic_stance = UNKNOWN
→ coverage = UNKNOWN

SUPPORTS
→ material_bearing = MATERIAL

FULL | PARTIAL
→ semantic_stance = SUPPORTS
→ material_bearing = MATERIAL

LIMITS | CONTRADICTS
→ coverage = UNKNOWN

scope_dependency = EXTERNAL_REQUIRED
→ positive settlement later is prohibited until resolved

ANY required dimension = UNKNOWN
→ no positive settlement by default
```

Una combinación inválida es contract-invalid. No se corrige por heurística.

### 8.5 Rationale

Un futuro mecanismo puede incluir una explicación breve y bounded para
auditabilidad, pero:

```text
rationale != settlement input authority
rationale confidence != truth
free text != enum override
```

## 9. Ground-Truth Contract

HVC-A separa dos superficies:

```text
VisibleSemanticObservationCaseV0
        ↓
bounded input visible to reviewer/mechanism

HiddenSemanticObservationGroundTruthV0
        ↓
expected dimensions + reviewer rationale
        ↓
qualification only
```

El material hidden nunca forma parte del input visible.

### 9.1 Forbidden leak keys en proyección visible

Como mínimo:

```text
expected_material_bearing
expected_semantic_stance
expected_scope_dependency
expected_coverage
expected_outcome
expected_reason_codes
case_class
reviewer_annotations
qualification_thresholds
ground_truth
oracle_label
```

La implementación futura deberá reutilizar/adaptar el patrón de blind projection
existente y fallar cerrado ante leakage detectado.

## 10. Discriminability matrix mínima

El case-set futuro deberá incluir pares/adversariales que permitan distinguir:

1. material full support vs persuasive overclaim;
2. unrelated authoritative source vs relevant insufficient source;
3. relevant insufficient vs compound partial support;
4. compatible limiting evidence vs contradiction;
5. explicit external dependency vs ordinary insufficiency;
6. missing evidence material vs semantic UNKNOWN;
7. exact binding vs binding drift;
8. root claim vs upstream-authorized claim part;
9. duplicate/conflicting observations vs one valid observation;
10. malformed/unknown enum vs valid abstaining observation.

Cada boundary material debe recibir una Ground-Truth Review independiente sin
acceso a expected labels previos, model outputs ni qualification results.

## 11. Claim decomposition

Disposición:

```text
optional future child gate
NOT REQUIRED by HVC-A
NOT IMPLEMENTED
```

HVC-A debe poder expresar `PARTIAL` sobre el claim raíz. Sólo si Ground-Truth
Review demuestra que eso es insuficiente para clasificar compound claims se
admitirá un gate separado de decomposition.

## 12. Dirección de autoridad — ADR-003

```text
CONTROL / REQUEST / POLICY
Malāk upstream
        ↓
future semantic mechanism downstream

OBSERVATION / FINDING / DEFICIT
Malāk upstream
        ↑
future semantic mechanism downstream

upward authority_effect = none
```

Prohibido:

- worker cambia policy;
- worker elige modelo alternativo;
- worker inicia tool/network;
- worker amplía scope;
- worker produce `support_sufficient`;
- worker llama Protected Finalization;
- worker ordena una acción upstream.

## 13. Security Horizon Check

| Superficie | Disposición |
|---|---|
| Prompt / Context Trust Boundary | REQUIRES_REINFORCEMENT en futura HVC-B |
| model/provider supply chain | DEFERRED hasta seleccionar mecanismo |
| network/tools | NOT_ACTIVATED |
| Memory/Knowledge | NOT_ACTIVATED |
| data persistence | NOT_ACTIVATED |
| Human in Control | PASS |
| least context | ADOPT |
| fail-closed | ADOPT |

Ground-truth text y evidence text se tratan como datos, no como instrucciones
privilegiadas.

## 14. Critical Contract Hardening

### A1 — ¿Una observación es truth?
NO.

### A2 — ¿SUPPORTS equivale a E3 SUPPORTED?
NO.

### A3 — ¿FULL equivale a support_sufficient?
NO.

### A4 — ¿NON_MATERIAL puede tener stance SUPPORTS/LIMITS/CONTRADICTS?
NO. Combinación inválida.

### A5 — ¿LIMITS equivale a CONTRADICTS?
NO. LIMITS acota/no-establishes; CONTRADICTS afirma incompatibilidad material.

### A6 — ¿PARTIAL puede convertirse en FULL por ausencia de otro material?
NO.

### A7 — ¿UNKNOWN puede convertirse en favorable por default?
NO.

### A8 — ¿EXTERNAL_REQUIRED autoriza al worker a buscar?
NO. Sólo informa deficit; upstream decide.

### A9 — ¿claim parts pueden generarse implícitamente?
NO. Sólo pueden consumirse si upstream los aporta bajo contrato autorizado.

### A10 — ¿ground truth puede ajustarse por model outputs?
NO.

### A11 — ¿rationale free-text puede sobreescribir enums?
NO.

### A12 — ¿HVC-A modifica V0.4?
NO.

### A13 — ¿HVC-A desbloquea U08?
NO.

Resultado:

```text
known material ambiguity unresolved = 0 for G1 design
fail-open path admitted             = 0
authority expansion                 = 0
```

## 15. Cuatro preguntas de ley

### Blueprint
PASS — Kernel/Planner delta 0; Model Agnostic; contracts before implementation.

### Cognitive Constitution
PASS — evidence over speculation; uncertainty explicit; Generation != Finalization;
missing assurance fails closed.

### Governance Constitution
PASS — Human in Control; least privilege; no self-elevation.

### Complejidad del Kernel
PASS — `Kernel delta = 0`.

## 16. Design 4R

### Risk — PASS

Riesgos: label leakage, semantic over-support, authority laundering, enum
ambiguity, binding drift, compound-claim omission, hidden scope expansion.

Mitigación: blind ground truth, exact bindings, closed enums, invalid-combination
rejection, UNKNOWN fail-closed, independent Ground-Truth Review.

### Readability — PASS

Se separan explícitamente:

```text
observation
ground truth
qualification
settlement
assurance projection
finalization
authority
```

### Reliability — PASS

Mismas entradas/bindings deben producir artefactos evaluables bajo schema
versionado. Invalid/missing/duplicate material no recibe default favorable.

### Resilience — PASS

```text
unknown enum      -> invalid / no positive reliance
missing dimension -> invalid / no positive reliance
binding drift     -> invalid / INCONCLUSIVE downstream
ground-truth leak -> qualification invalid
review ambiguity  -> INCONCLUSIVE / STOP
```

## 17. RDD Stage 1 Design Check

```text
candidate identity strategy                PASS
baseline/candidate binding                 PASS
evidence provenance                       PASS
Writer / Reviewer / Validator / Authority PASS
PASS | FAIL | INCONCLUSIVE discipline     PASS
INCONCLUSIVE != PASS                      PASS
candidate change invalidates evidence     PASS
bounded correction                        DEFINED
independent fix validation                REQUIRED when findings change candidate
authority_effect                          none
RDD Stage 2 future risk-3 candidate       REQUIRED
```

Resultado:

```text
RDD_STAGE_1_DESIGN_CHECK = PASS
```

## 18. Secuencia crítica aplicable

Para la futura materialización PR-B se aplica sin sustitución:

```text
G0/G1 Design integrated
→ RED
→ Owner GREEN authorization
→ GREEN
→ targeted validation
→ Candidate FULL 4R
→ Bounded Correction / Fix Validator / revalidation if needed
→ E2E / integration-equivalent
→ CI candidate-bound
→ independent validation
→ RDD Stage 1 Candidate Conformance
→ RDD Stage 2 Receipt (risk 3)
→ human review
→ Owner Ready / Merge
→ post-merge validation
```

## 19. Scope freeze de PR-A

Allowed:

```text
docs/project/sprints/proposals/MALAK-E3-HVC-A-SEMANTIC-OBSERVATION-GROUND-TRUTH-CONTRACT-G0-G1-DESIGN-20261012.md
docs/project/sprints/proposals/MALAK-E3-HVC-A-SEMANTIC-OBSERVATION-GROUND-TRUTH-CONTRACT-G0-G1-FILE-COVERAGE-20261012.tsv
```

Forbidden:

```text
all baseline files
src/**
tests/**
scripts/**
evaluations/**
configs/**
AGENTS.md
SECURITY.md
docs/governance/**
Blueprint / Kernel / accepted ADRs
model/provider/runtime
support_sufficient
Protected Finalization wiring
U08
```

Si una corrección del design requiere modificar una fuente superior:

```text
STOP
→ reopen admission / separate scope
```

## 20. Candidate Identity / correction budget

```text
baseline               26550b225e316bee6cff5cb0fb47b931e9335186
PR-A candidate         Git SHA + tree after materialization
allowed files          2 added docs
baseline modifications 0
production delta       0
test/evaluation delta  0
law delta              0
Kernel delta           0
Planner delta          0
max design fix rounds  2
authority_effect       none
```

## 21. Criterios de aceptación de PR-A

- Preflight PASS.
- 389/389 blobs clasificados; omisiones silenciosas 0.
- Alignment Matrix completa.
- REUSE + ADAPT + COMPOSE.
- NEW component NOT_ADMISSIBLE.
- Security Horizon Check dispuesto.
- Critical Contract Hardening PASS.
- cuatro preguntas de ley PASS.
- Design 4R PASS.
- RDD Stage 1 Design Check PASS.
- V0.4 preservado.
- U08 bloqueado.
- runtime/test/evaluation delta 0.
- authority_effect none.
- Ready/Merge Owner-only.

## 22. Malāk Alignment Matrix

| Source | Authority | Invariant / intent | Disposition | Implementation effect |
|---|---|---|---|---|
| Cognitive Constitution | constitutional | evidence, uncertainty, Generation != Finalization | ADOPT | observation remains evidence |
| Governance Constitution | constitutional | Human in Control / least privilege | ADOPT | worker has zero authority |
| Blueprint | architecture | Kernel/Capability/Model Agnostic | ADOPT | Kernel/Planner unchanged |
| Kernel spec | approved specification | orchestration boundary | ADOPT | no HVC-A logic in Kernel |
| Architecture Quality Gates | architecture | spec/verification + traceability | ADOPT | contract before materialization |
| SECURITY.md | protected | Zero Trust / fail closed | ADOPT | UNKNOWN never favorable |
| ADR-002 | accepted ADR | authorization separate from evidence | REUSE | no permission semantics |
| ADR-003 | accepted ADR | downward control/upward evidence | ADOPT | observation returns upward only |
| ADR-004 | accepted ADR | Specification & Verification First | ADOPT | ground truth before verifier |
| ADR-005 | accepted ADR | Evidence-Bound Finalization | ADOPT | no direct finalization |
| ADR-006 | accepted ADR | reliance non-transitive / fail closed | ADOPT | no observation reused as trust |
| parent HVC design | promoted design | deterministic-first + semantic residual | ADOPT | direct child contract |
| E3 bindings/routing | implementation | exact subject/evidence identity | REUSE | no parallel binding system |
| V0.4 corpus | evaluation evidence | known semantic boundaries | PRESERVE | no tuning |
| Cognitive Dataset concept | non-normative | define behavior before training | ADAPT | ground truth first |
| Evidence-Bound Cognition concept | non-normative | evidence before finalization | ADAPT | observation is bounded evidence |
| Research Horizon | non-normative | research != authority / complexity restraint | ADOPT | no new subsystem |

## 23. Terminal G0/G1 result

```text
Construction Preflight            PASS
File Coverage                     389/389; omitted 0
G0                                PASS
G1                                PASS / ADAPT
reuse                             REUSE + ADAPT + COMPOSE
new component                     NOT_ADMISSIBLE
critical contract                 YES
risk                              3_HIGH
Critical Contract Hardening       PASS
law questions                     PASS
Design 4R                         PASS
RDD Stage 1 Design Check          PASS
specific verifier                 NOT_SELECTED
ground-truth implementation       NOT AUTHORIZED
RED / GREEN                       NOT AUTHORIZED
support_sufficient                NOT WIRED / NOT AUTHORIZED
Protected Finalization            NOT WIRED / NOT AUTHORIZED
G-01 V0.4                         PRESERVED / NOT PASSED
U08                               BLOCKED
Kernel / Planner delta            0 / 0
authority_effect                  none
Ready / Merge                     OWNER ONLY
```

La siguiente transición, sólo después de integración humana de PR-A, es una PR-B
que materialice el schema/case-set/validación de HVC-A siguiendo §5.5.
