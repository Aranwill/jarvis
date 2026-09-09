---
title: Episodic Admission Assessment Provenance Boundary — G2 Implementation Candidate Specification
status: g2_candidate_specification
authority: owner-authorized design specification
as_of_date: 2026-09-09
unit: Episodic Admission Assessment Provenance Boundary
gate: G2
source_baseline: 684927a1e429e530da8f9831f374551c22b48d8f
g1_record: docs/project/sprints/proposals/EPISODIC-ADMISSION-ASSESSMENT-PROVENANCE-G0-G1-DESIGN.md
risk_class: 3
vault_reconciliation_status: resolved
vault_head: 155172f1c258fe40c1a25fbf97a537022859064f
sync_agent_head: 71b21e0a192017353075954e06e2b55f5f8e2255
implementation_authorized: false
persistent_memory_authorized: false
retrieval_authorized: false
knowledge_implementation_authorized: false
sprint_7_12_authorized: false
rdd_stage_2_authorized: false
language: es
---

# Episodic Admission Assessment Provenance Boundary — G2 Implementation Candidate Specification

## 1. Estado de autoridad

El Owner autorizó **G2 exclusivamente para especificar un candidate mínimo de implementación** de:

```text
Episodic Admission Assessment Provenance Boundary
```

G2 puede fijar:

- contratos lógicos mínimos;
- inputs, outputs, enums y reason codes;
- binding entre assessment y candidate;
- matriz dimensional de producer roles;
- reglas deterministas y fail-closed;
- límites explícitos de provenance estructural v1;
- presupuesto máximo de archivos;
- escenarios TDD futuros;
- FULL 4R del candidate;
- stop conditions y rollback.

G2 **no autoriza**:

- código productivo;
- tests de implementación;
- modificación de `src/malak/memory/episodic_admission.py`;
- wiring hacia G3, Conversation, Kernel o runtime;
- cambios en `SecurityContext`, PDP o PEP;
- persistencia, storage o repository de Memory;
- retrieval, RAG, GraphRAG o Knowledge;
- agents, tools o red;
- registry persistente de productores;
- identidad criptográfica, PKI, firmas, nonce o replay protection;
- un `TrustManager`, `MemoryManager` o authority service universal;
- Sprint 7.12;
- RDD Stage 2;
- merge sin aprobación explícita del Owner.

```text
Specification != Implementation
Structural provenance != authenticated identity
Assessment provenance != Admission decision
Admission decision != Persistence authorization
Evidence != Authority
```

---

## 2. Binding a G1, baseline y reconciliación cross-repository

Baseline congelado para G2:

```text
Aranwill/jarvis
main
684927a1e429e530da8f9831f374551c22b48d8f
```

G1 aprobado e integrado:

```text
docs/project/sprints/proposals/
EPISODIC-ADMISSION-ASSESSMENT-PROVENANCE-G0-G1-DESIGN.md
```

El drift downstream que G0/G1 aceptaron temporalmente fue posteriormente reconciliado mediante el flujo gobernado del Vault Sync Agent.

Estado verificado antes de abrir G2:

```text
Malāk main:
684927a1e429e530da8f9831f374551c22b48d8f

Project Vault main:
155172f1c258fe40c1a25fbf97a537022859064f

Vault Sync Agent main:
71b21e0a192017353075954e06e2b55f5f8e2255

post-reconciliation dry-run:
base_commit == head_commit == 684927a1...
changed_files = 0
document_candidates = 0
validation_findings = 0
conclusion = pass
proposal_created = false
```

Por tanto:

```text
BASELINE_DRIFT = 0
PROJECTION_DRIFT = 0
STATE_DRIFT = 0
```

La aceptación temporal de drift registrada en G1 permanece como hecho histórico de aquella revisión; ya no constituye riesgo abierto para G2.

---

## 3. Baseline observado que G2 debe respetar

G3 ya materializó una policy episódica aislada bajo:

```text
src/malak/memory/episodic_admission.py
```

Actualmente existen, entre otros:

```text
EpisodicAdmissionContext
EpisodicAdmissionSignals
SourceSecurityStatus
EpisodicAdmissionDecision
evaluate_episodic_candidate(...)
```

La policy consume valores como:

```text
source_authority_classification
confidence_classification
sensitivity_classification
scope_applicable
policy_violation
source_security_status
sensitive_review_required
contradiction_requires_review
```

El baseline ya prueba:

```text
payload cannot set control metadata
missing assessments fail closed
TAINTED / REVOKED cannot be overridden by confidence
policy denial has higher precedence
ELIGIBLE != Stored
no runtime side effects
```

Pero todavía no existe un contrato independiente que vincule cada assessment con:

```text
what dimension was assessed
which candidate it belongs to
which logical producer role emitted it
which declared producer reference emitted it
which policy/rule generated it
when it was assessed
whether that producer role is allowed for that dimension
```

Ese es el único problema que este G2 intenta congelar.

---

## 4. Decisión arquitectónica principal G2

### G2-D1 — La primera implementación será aislada antes del wiring

El candidate v1 **no modifica G3**.

Debe crear una frontera independiente:

```text
Assessment value + structural provenance
        ↓
pure provenance validation
        ↓
VALID | HOLD | INVALID
        ↓
STOP
```

No debe hacer todavía:

```text
VALID provenance
        ↓
automatic mutation of EpisodicAdmissionContext
or EpisodicAdmissionSignals
        ↓
Admission evaluation
```

Ese wiring requerirá un gate posterior y una nueva autorización explícita.

Razones:

- preserva rollback simple;
- evita alterar una policy G3 ya validada;
- permite probar la provenance boundary de forma independiente;
- impide confundir provenance estructural con trust operacional real;
- mantiene `Cognition != Authority` y `Evidence != Authority`.

### G2-D2 — No crear identidad que el baseline no puede demostrar

La v1 puede registrar:

```text
producer_role
producer_reference
policy_or_rule_reference
assessed_at
```

pero:

```text
producer_reference
!=
cryptographically verified producer identity
```

La presencia de una referencia declarada no demuestra autenticación, no concede permisos y no prueba que el caller no esté mintiendo sobre su rol.

Por ello G2 no autoriza wiring operacional que dependa de esa referencia como si fuera una identidad fuerte.

### G2-D3 — Producer role es dimensional, no autoridad universal

Un producer role autorizado para una dimensión no obtiene permiso para otras.

```text
DATA_CLASSIFICATION
may assess sensitivity

DATA_CLASSIFICATION
!= permission to assess source security status
!= permission to assess source authority
!= operational permission
```

### G2-D4 — Provenance se liga al assessment y al candidate

No se acepta provenance separada que pueda reutilizarse libremente para otro valor o candidato.

El assessment será un value object inmutable que contiene simultáneamente:

```text
assessment identity
candidate identity
assessment kind
assessment value
producer provenance
```

La decisión de provenance deberá devolver `assessment_id` y `candidate_id` para preservar binding explícito.

---

## 5. Ubicación arquitectónica futura

Una futura implementación autorizada deberá vivir bajo:

```text
src/malak/memory/
```

Candidate v1 previsto:

```text
NEW  src/malak/memory/assessment_provenance.py
NEW  tests/test_episodic_assessment_provenance.py
```

No debe vivir bajo:

```text
src/malak/kernel/
src/malak/security/
src/malak/observability/
src/malak/runtime/
src/malak/services/
src/malak/capabilities/
```

No modifica:

```text
src/malak/memory/episodic_admission.py
src/malak/memory/__init__.py
```

en el candidate inicial.

---

## 6. Presupuesto máximo de una futura implementación v1

Si un gate posterior autoriza código, deberá intentar exactamente:

```text
NEW     src/malak/memory/assessment_provenance.py
NEW     tests/test_episodic_assessment_provenance.py

MODIFY  existing production files = 0
```

Budget:

```text
new production files     <= 1
new test files           <= 1
existing production mods = 0
Kernel changes           = 0
Conversation changes     = 0
Security changes         = 0
Observability changes    = 0
Runtime changes          = 0
CI changes               = 0
external dependencies    = 0
persistence              = 0
retrieval                = 0
Knowledge                = 0
```

Si la implementación necesita modificar una ruta productiva existente, debe detenerse y volver al Owner antes de hacerlo.

---

## 7. Contratos lógicos propuestos

Los nombres siguientes congelan el candidate v1. Sólo adquirirán existencia runtime si un gate posterior autoriza implementación.

### 7.1 `AssessmentKind`

Enum cerrado:

```text
SOURCE_AUTHORITY
CONFIDENCE
SENSITIVITY
SOURCE_SECURITY_STATUS
SCOPE_APPLICABLE
POLICY_VIOLATION
SENSITIVE_REVIEW_REQUIRED
CONTRADICTION_REQUIRES_REVIEW
```

Semántica:

```text
AssessmentKind
!= trust level
!= producer authority
!= admission outcome
```

Cada kind representa una dimensión que G3 ya consume actualmente.

### 7.2 `AssessmentProducerRole`

Enum lógico mínimo:

```text
SOURCE_GOVERNANCE
EVIDENCE_EVALUATION
DATA_CLASSIFICATION
SECURITY_TRUST_STATE
ADMISSION_POLICY
CONFLICT_EVALUATION
```

Estos valores representan **roles lógicos**, no componentes runtime nuevos.

```text
AssessmentProducerRole
!= component identity
!= SecurityContext role
!= permission token
!= verified principal
```

No se crea un registry global ni una jerarquía universal de authority.

### 7.3 `AdmissionAssessment`

Value object inmutable:

```text
assessment_id: str
candidate_id: str
kind: AssessmentKind
value: str | bool
producer_role: AssessmentProducerRole | None
producer_reference: str | None
policy_or_rule_reference: str | None
assessed_at: datetime UTC | None
```

Reglas:

- `assessment_id` es obligatorio, canónico, no vacío y suministrado externamente;
- `candidate_id` es obligatorio, canónico, no vacío y suministrado externamente;
- la policy no genera IDs;
- `kind` debe ser `AssessmentKind`;
- `value` sólo puede ser `str` o `bool` en v1;
- strings de `value`, cuando se usen, deben ser canónicos y no vacíos;
- `bool` debe ser boolean real, no entero `0/1`;
- `producer_role` puede ser `None` para representar provenance incompleta;
- `producer_reference` puede ser `None` para representar provenance incompleta;
- `policy_or_rule_reference` puede ser `None` para representar provenance incompleta;
- `assessed_at` puede ser `None` para representar provenance incompleta;
- `assessed_at`, cuando exista, debe ser timezone-aware UTC;
- `producer_reference` es una referencia estructural opaca;
- el validator no infiere role desde `producer_reference`;
- el validator no interpreta `value` para conceder authority;
- el payload episódico no participa en la construcción de producer role o provenance.

El uso de `str | bool` es deliberadamente transport-neutral para esta frontera aislada. La conversión futura hacia tipos concretos de G3, como `SourceSecurityStatus`, queda fuera del candidate v1 y requerirá un adapter/wiring autorizado aparte.

### 7.4 `AssessmentProvenanceOutcome`

Enum cerrado:

```text
HOLD
INVALID
VALID
```

Semántica:

```text
VALID
!= trusted truth
!= admission eligible
!= persistence authorization

HOLD
!= retention authorization

INVALID
!= automatic candidate rejection
```

La provenance boundary clasifica la **validez estructural de provenance**, no decide el outcome final de Memory admission.

### 7.5 `AssessmentProvenanceReason`

Reason codes mínimos:

```text
missing_producer_role
missing_producer_reference
missing_policy_or_rule_reference
missing_assessed_at
assessment_from_future
candidate_mismatch
producer_role_not_allowed_for_kind
valid
```

No se aceptan mensajes libres del payload como reason code.

### 7.6 `AssessmentProvenanceDecision`

Value object inmutable:

```text
assessment_id: str
candidate_id: str
kind: AssessmentKind
outcome: AssessmentProvenanceOutcome
reason_code: AssessmentProvenanceReason
evaluated_at: datetime UTC
policy_version: str
```

Policy version inicial:

```text
episodic-assessment-provenance/v1
```

La decisión no contiene:

```text
storage instruction
admission outcome
permission
SecurityContext
producer authentication claim
trust score
```

---

## 8. Matriz dimensional cerrada v1

La primera policy de provenance debe fijar explícitamente:

| Assessment kind | Producer role permitido |
|---|---|
| `SOURCE_AUTHORITY` | `SOURCE_GOVERNANCE` |
| `CONFIDENCE` | `EVIDENCE_EVALUATION` |
| `SENSITIVITY` | `DATA_CLASSIFICATION` |
| `SOURCE_SECURITY_STATUS` | `SECURITY_TRUST_STATE` |
| `SCOPE_APPLICABLE` | `ADMISSION_POLICY` |
| `POLICY_VIOLATION` | `ADMISSION_POLICY`, `SECURITY_TRUST_STATE` |
| `SENSITIVE_REVIEW_REQUIRED` | `ADMISSION_POLICY`, `DATA_CLASSIFICATION` |
| `CONTRADICTION_REQUIRES_REVIEW` | `CONFLICT_EVALUATION` |

Esta matriz representa scope lógico por dimensión.

No significa que un caller pueda ganar ese rol escribiendo su nombre en un campo.

```text
declared role
!= authenticated role
```

La v1 sólo prueba que el **contrato estructural recibido** usa una combinación role/kind permitida.

---

## 9. Función determinista mínima

La futura implementación deberá preferir una función pura equivalente a:

```text
validate_assessment_provenance(
    assessment,
    expected_candidate_id,
    evaluated_at,
) -> AssessmentProvenanceDecision
```

No se aprueban:

```text
ProvenanceManager
TrustManager
ProducerRegistry
AuthorityResolver
PolicyOrchestrator
```

La función:

- no realiza I/O;
- no persiste;
- no usa filesystem;
- no usa network;
- no llama al LLM;
- no consulta SecurityContext;
- no modifica assessment;
- no genera timestamps;
- no genera IDs;
- no interpreta `producer_reference` como identidad verificada;
- no interpreta payload episódico;
- produce el mismo resultado para los mismos inputs.

---

## 10. Precedencia determinista de provenance policy v1

La evaluación usa **primer match** en este orden.

### 10.1 Provenance incompleta → `HOLD`

```text
producer_role is None
    → HOLD / missing_producer_role

producer_reference is None
    → HOLD / missing_producer_reference

policy_or_rule_reference is None
    → HOLD / missing_policy_or_rule_reference

assessed_at is None
    → HOLD / missing_assessed_at
```

Esto representa información insuficiente, no una aprobación parcial.

### 10.2 Binding inválido → `INVALID`

```text
assessment.candidate_id != expected_candidate_id
    → INVALID / candidate_mismatch
```

La provenance de un assessment para candidate A no puede reutilizarse para candidate B.

### 10.3 Tiempo imposible → `HOLD`

```text
assessment.assessed_at > evaluated_at
    → HOLD / assessment_from_future
```

No se intenta resolver clock skew en v1.

### 10.4 Scope dimensional inválido → `INVALID`

```text
producer_role not allowed for assessment.kind
    → INVALID / producer_role_not_allowed_for_kind
```

Un role válido para una dimensión no gana authority sobre las demás.

### 10.5 Provenance estructural válida

Sólo si ninguna regla previa aplica:

```text
VALID / valid
```

Esto significa únicamente:

```text
required structural provenance present
candidate binding matches
assessment timestamp is not in the future
role-kind combination is allowed by policy v1
```

No significa:

```text
producer authenticated
assessment true
source trusted
candidate eligible
storage allowed
```

---

## 11. Regla monotónica preservada en G2

La v1 no modela una jerarquía universal de authority y no puede autenticar el producer real.

Por tanto la garantía monotónica que G2 sí puede imponer es:

```text
HOLD provenance
must never satisfy a positive admission prerequisite

INVALID provenance
must never satisfy a positive admission prerequisite

only VALID provenance
may be considered by a future authorized adapter
```

También:

```text
VALID provenance alone
must never create ELIGIBLE
must never clear REJECT
must never authorize persistence
```

Una futura integración deberá conservar además:

```text
negative / conservative findings
may reduce trust or require review

missing / invalid provenance
must never increase trust
```

La integración concreta permanece fuera de este candidate.

---

## 12. Binding, replay y reutilización

`assessment_id` y `candidate_id` existen para correlación y binding determinista.

La v1 **no** implementa:

- unicidad persistente de `assessment_id`;
- nonce;
- anti-replay criptográfico;
- firma de assessment;
- secure clock;
- registry de producer identities.

Por tanto:

```text
assessment_id
!= globally unique security nonce

candidate_id binding
!= cryptographic anti-replay
```

El candidate evita misbinding accidental dentro del contrato, pero no afirma resolver replay adversarial a nivel de sistema.

---

## 13. Relación futura con G3

El candidate v1 termina antes de G3.

Frontera prevista para un gate posterior:

```text
AdmissionAssessment
        +
AssessmentProvenanceDecision == VALID
        ↓
AUTHORIZED ADAPTER / WIRING GATE
        ↓
translate value into existing G3 control input
        ↓
evaluate_episodic_candidate(...)
```

Ese adapter deberá demostrar, entre otras cosas:

- que `assessment_id` y decision corresponden al mismo assessment;
- que candidate binding coincide;
- que el tipo de `value` se traduce de forma exacta al contrato G3;
- que `HOLD` o `INVALID` nunca se convierten en assessment positivo;
- que el payload no puede insertar provenance;
- que el caller no puede autoasignarse producer role mediante contenido;
- que no se expande authority.

Nada de ese wiring está autorizado por G2.

---

## 14. Escenarios TDD obligatorios para una futura implementación

### AP2-01 — Valid structural provenance

Assessment completo, candidate correcto, timestamp válido y role permitido → `VALID / valid`.

### AP2-02 — Missing producer role

`producer_role=None` → `HOLD / missing_producer_role`.

### AP2-03 — Missing producer reference

`producer_reference=None` → `HOLD / missing_producer_reference`.

### AP2-04 — Missing rule reference

`policy_or_rule_reference=None` → `HOLD / missing_policy_or_rule_reference`.

### AP2-05 — Missing assessed_at

`assessed_at=None` → `HOLD / missing_assessed_at`.

### AP2-06 — Candidate misbinding

Assessment ligado a otro `candidate_id` → `INVALID / candidate_mismatch`.

### AP2-07 — Future assessment

`assessed_at > evaluated_at` → `HOLD / assessment_from_future`.

### AP2-08 — Dimensional producer scope

`DATA_CLASSIFICATION` intentando producir `SOURCE_SECURITY_STATUS` → `INVALID / producer_role_not_allowed_for_kind`.

### AP2-09 — Allowed dual producer role

`POLICY_VIOLATION` puede ser producido por `ADMISSION_POLICY` o `SECURITY_TRUST_STATE`; ambas combinaciones son estructuralmente válidas.

### AP2-10 — Producer reference does not grant role

El validator nunca deriva `producer_role` desde un string como `"security"`, `"owner"` o `"llm"`.

### AP2-11 — Declared identity is not verified identity

Una decision `VALID` no contiene ni expone un flag equivalente a `identity_verified=true`.

### AP2-12 — Value cannot alter producer role

`value="trusted"`, `value="owner"` o cualquier otro contenido no modifica el role ni la matriz permitida.

### AP2-13 — Deterministic precedence

Si faltan producer role y producer reference simultáneamente, aplica el primer reason code definido: `missing_producer_role`.

### AP2-14 — Deterministic resolution

Mismos inputs → misma decision byte-semantically equivalente.

### AP2-15 — Inputs immutable

La función no muta `AdmissionAssessment`.

### AP2-16 — No side effects

La validación no crea archivos, no escribe estado, no llama red, no llama LLM y no persiste.

### AP2-17 — No G3 wiring

El test suite del candidate no necesita construir ni modificar `EpisodicAdmissionContext`, `EpisodicAdmissionSignals` o `EpisodicAdmissionDecision`.

### AP2-18 — VALID does not mean authority

La decision `VALID` no contiene storage flag, admission outcome, permission o authority token.

---

## 15. Tipado y validación de construcción

La implementación futura deberá distinguir errores de contrato de estados gobernables.

Errores de contrato que deben fallar durante construcción o llamada:

```text
assessment_id not str
candidate_id not str
empty / non-canonical required IDs
kind not AssessmentKind
value neither str nor bool
empty / non-canonical string value
producer_role wrong runtime type when non-None
assessed_at non-datetime when non-None
assessed_at non-UTC when non-None
evaluated_at non-UTC
expected_candidate_id invalid
```

Estados incompletos intencionalmente representables y evaluables:

```text
producer_role = None
producer_reference = None
policy_or_rule_reference = None
assessed_at = None
```

Esos estados producen `HOLD`, no excepciones de policy.

---

## 16. FULL 4R — G2 candidate specification

### Risk — PASS

Riesgos evaluados:

- self-asserted trust;
- producer role confusion;
- cross-dimension authority leakage;
- candidate misbinding;
- provenance reutilizable sin binding;
- falsa afirmación de identidad autenticada;
- replay presentado erróneamente como resuelto;
- wiring prematuro con G3;
- creación de registry/manager global;
- contaminación de Kernel o SecurityContext.

Mitigación principal:

```text
isolated structural boundary
+ immutable contracts
+ candidate binding
+ closed dimensional matrix
+ deterministic fail-closed validation
+ no runtime wiring
```

Riesgo residual explícito:

```text
structural producer role/reference
!= authenticated producer identity
```

Este riesgo es aceptable para una foundation aislada precisamente porque G2 prohíbe que la v1 conceda authority o se conecte automáticamente con G3.

### Readability — PASS

Responsabilidad única:

> Validar si un assessment posee provenance estructural suficiente y si el producer role declarado está autorizado para esa dimensión.

No se crea un trust engine universal ni se mezclan admission, persistence o Security.

### Reliability — PASS

La especificación fija:

- enums cerrados;
- matrix cerrada;
- precedencia exacta;
- reason codes cerrados;
- UTC estricto;
- candidate binding;
- determinismo;
- inputs inmutables;
- cero side effects.

### Resilience — PASS

Faltantes, ambigüedad temporal o provenance incompleta degradan a `HOLD`.

Misbinding y producer role fuera de dimensión degradan a `INVALID`.

Ningún estado incompleto o inválido aumenta trust ni autoriza ejecución.

---

## 17. Architecture Quality Gates

```text
Blueprint compliance: PASS
Cognitive Constitution: PASS
Governance Constitution: PASS
Kernel First: PASS
Capability First: N/A — pure Memory Layer contract foundation
Runtime Independence: PASS
Human in Control: PASS
Traceability: PASS
```

### Preguntas obligatorias antes del cambio

1. ¿Respeta Blueprint? → **PASS**
2. ¿Respeta Cognitive Constitution? → **PASS**
3. ¿Respeta Governance? → **PASS**
4. ¿Kernel permanece simple? → **PASS; delta Kernel = 0**

---

## 18. Stop conditions

Detener y volver al Owner si la futura implementación requiere:

- modificar `episodic_admission.py`;
- modificar Kernel;
- modificar `SecurityContext`, PDP o PEP;
- crear permission tokens;
- autenticar cryptographically producer identities;
- registry persistente o global de producers;
- DB, filesystem o storage;
- runtime wiring;
- Conversation wiring;
- Event Bus;
- agents/tools;
- network;
- external dependency;
- background worker;
- persistence/retrieval/Knowledge;
- taxonomía universal de trust;
- más archivos productivos que el budget aprobado.

Cualquiera de esas necesidades constituye nueva evidencia arquitectónica y exige re-admission o autorización separada según corresponda.

---

## 19. Rollback previsto

El candidate de implementación v1, si luego es autorizado, deberá ser reversible eliminando únicamente:

```text
src/malak/memory/assessment_provenance.py
tests/test_episodic_assessment_provenance.py
```

sin migraciones, sin estado persistente, sin tocar G3 y sin modificar Kernel o runtime.

---

## 20. Criterios de aceptación para un gate posterior de implementación

Antes de autorizar código deberán verificarse nuevamente:

```text
exact main baseline unchanged or explicitly re-reviewed
Vault relevant drift = 0
file budget still sufficient
TDD scenarios AP2-01 .. AP2-18 preserved
no new runtime dependency discovered
FULL 4R still PASS
Owner implementation authorization explicit
```

La autorización futura deberá ser candidate-bound a un SHA exacto.

---

## 21. Resultado G2

```text
G2 RESULT: PASS
unit: Episodic Admission Assessment Provenance Boundary
candidate disposition: ADAPT
risk class: 3
candidate architecture: isolated structural provenance validator
new production files planned: 1
new test files planned: 1
existing production modifications planned: 0
Kernel delta: 0
SecurityContext delta: 0
runtime wiring: 0
persistent memory: 0
retrieval: 0
Knowledge: 0
implementation authorized: false
sprint 7.12 authorized: false
rdd stage 2 authorized: false
relevant Vault drift: 0
```

Próximo paso permitido únicamente mediante nueva autorización del Owner:

```text
Assessment Provenance G3 — isolated TDD implementation candidate
```

Incluso después de ese candidate:

```text
provenance implementation
!= G3 admission wiring
!= persistent Memory
!= authority expansion
```
