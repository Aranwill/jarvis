---
title: Episodic Candidate Content Identity Propagation & Binding — G2 Implementation Candidate Specification
status: g2_candidate_specification
authority: owner-authorized scope freeze
as_of_date: 2026-09-12
unit: Episodic Candidate Content Identity Propagation & Binding Boundary
gate: G2-SPEC
source_baseline: d08d4ccb77c704d1831e7e2a1c6dfbc337dbe67e
risk_class: 3
sdd_required: true
tdd_required_for_future_implementation: true
full_4r_required: true
rdd_stage_1: adopted
rdd_stage_2_authorized: false
g2_spec_authorized: true
implementation_authorized: false
persistent_memory_authorized: false
persistence_authorization_authorized: false
retrieval_authorized: false
knowledge_implementation_authorized: false
runtime_wiring_authorized: false
kernel_change_authorized: false
security_control_plane_change_authorized: false
sprint_7_12_authorized: false
compromise_aware_binding_required: true
verification_transitivity_allowed: false
self_attestation_allowed: false
candidate_id_fallback_allowed: false
legacy_compatibility_mode_allowed: false
language: es
---

# Episodic Candidate Content Identity Propagation & Binding — G2 Implementation Candidate Specification

## 1. Estado de autoridad

El Owner autorizó avanzar desde el G0/G1 endurecido de `Episodic Candidate Content
Identity Propagation & Binding Boundary` hacia **G2-SPEC exclusivamente**.

Baseline fuente congelado:

```text
repository: Aranwill/jarvis
branch:     main
commit:     d08d4ccb77c704d1831e7e2a1c6dfbc337dbe67e
```

Ese commit integra PR #124 y congela el modelo `Compromise-Aware Binding`.

Esta especificación:

- congela contratos exactos para una futura implementación candidata;
- no autoriza código productivo;
- no autoriza tests de implementación;
- no autoriza Persistence Authorization;
- no autoriza Persistent Memory;
- no autoriza retrieval / RAG / Knowledge;
- no modifica Kernel, Conversation ni Security Control Plane;
- no autoriza HMAC, firmas, PKI o remote attestation;
- no autoriza RDD Stage 2;
- no autoriza Sprint 7.12;
- no concede merge authority.

Separaciones obligatorias:

```text
candidate_id != candidate content identity
identity carried != identity verified against actual candidate
identity verified != producer/component trusted
component trusted != semantic correctness
content identity != source authenticity
content integrity != source trust
content integrity != truth
content identity binding != producer authorization
producer authorization != signal truth
Projection READY != Admission ELIGIBLE
Admission ELIGIBLE != Persistence Authorization
Persistence Authorization != Stored Memory
Evidence != Authority
```

---

## 2. Objetivo exacto de G2

La futura implementación deberá transformar la cadena episódica desde correlación
principalmente por `candidate_id` hacia una cadena content-bound explícita:

```text
EpisodicMemoryCandidate
        ↓
EpisodicCandidateContentIdentity
        ↓
AdmissionAssessment
        ↓
AssessmentProvenanceDecision
        ↓
AssessmentProducerAuthorizationEvidence / Decision
        ↓
GovernedTemporalControlEvidence
        ↓
GovernedAdmissionInputProjection
        ↓
GovernedAdmissionConsumptionResult
        ↓
STOP
```

Todos los artefactos anteriores deberán quedar ligados al **mismo sidecar completo**
`EpisodicCandidateContentIdentity`, sin introducir un segundo digest, alias o manager.

La unidad debe impedir:

```text
valid evidence for DX
+
same candidate_id but content DY
→ permissive reuse
```

cuando:

```text
DX != DY
```

---

## 3. Scope productivo congelado

La futura implementación candidata puede modificar únicamente:

```text
src/malak/memory/assessment_provenance.py
src/malak/memory/assessment_producer_authorization.py
src/malak/memory/governed_input_projection.py
src/malak/memory/governed_projection_consumption.py
```

Tests correspondientes permitidos:

```text
tests/test_episodic_assessment_provenance.py
tests/test_assessment_producer_authorization.py
tests/test_governed_input_projection.py
tests/test_governed_projection_consumption.py
```

No se crean módulos productivos nuevos.

Fuera de scope:

```text
src/malak/memory/candidate_content_identity.py
src/malak/memory/episodic_admission.py
src/malak/memory/__init__.py
src/malak/security/**
src/malak/core/**
src/malak/services/**
src/malak/capabilities/**
Vault
Sync Agent
```

`candidate_content_identity.py` es dependencia estable y única dueña de la
canonicalización/digest v1.

Cualquier quinto módulo productivo requerido implica:

```text
STOP → demonstrate necessity → Owner review → new scope decision
```

---

## 4. File / dependency / correction budget

```yaml
production_files_new: 0
existing_production_files_modified: 4
test_files_new: 0
existing_test_files_modified: 4
external_dependencies_added: 0
kernel_delta: 0
security_contract_delta: 0
conversation_delta: 0
persistence_delta: 0
retrieval_delta: 0
authority_delta: 0
production_net_new_loc_guardrail: 220
test_net_new_loc_guardrail: 650
max_material_fix_rounds_before_escalation: 2
```

Exceder cualquier guardrail material obliga:

```text
STOP → explain demonstrated need → Owner review
```

---

## 5. Policy version migration

La migración es contractualmente incompatible con los artefactos `candidate_id-only`.
Por tanto, las policy versions de los cuatro módulos cambian de v1 a v2:

```text
assessment_provenance.py
"episodic-assessment-provenance/v2"

assessment_producer_authorization.py
"episodic-assessment-producer-authorization/v2"

governed_input_projection.py
"episodic-admission-governed-input-projection/v2"

governed_projection_consumption.py
"episodic-admission-governed-projection-consumption/v2"
```

No habrá compatibilidad automática con v1 dentro de esta unidad.

Regla:

```text
legacy v1 artifact
!=
content-bound v2 artifact
```

No se introduce decoder, adapter, feature flag ni fallback legacy.

---

## 6. Tipo de binding reutilizado

Tipo obligatorio:

```python
EpisodicCandidateContentIdentity
```

No se introduce:

```text
CandidateBindingId
BindingToken
IntegrityEnvelope
VerifiedIdentity
TrustedIdentity
UniversalIntegrityManager
registry global
```

La igualdad es igualdad completa de dataclass, incluyendo:

```text
candidate_id
digest_algorithm
digest_hex
canonicalization_version
policy_version
```

No se compara `digest_hex` de manera aislada.

---

## 7. Contrato exacto — AdmissionAssessment

`AdmissionAssessment` deberá adquirir un campo obligatorio:

```python
candidate_content_identity: EpisodicCandidateContentIdentity
```

Orden conceptual:

```text
assessment_id
candidate_id
candidate_content_identity
kind
value
...
```

Invariantes de constructor:

```text
candidate_content_identity is EpisodicCandidateContentIdentity
candidate_content_identity.candidate_id == candidate_id
```

Violaciones estructurales:

```text
wrong type      → TypeError
candidate mismatch → ValueError
```

No existe `None` permitido.

El constructor no afirma que la identity haya sido verificada contra el candidate
real. Solo garantiza consistencia interna del artefacto.

```text
identity carried != identity independently verified
```

---

## 8. Contrato exacto — AssessmentProvenanceDecision

`AssessmentProvenanceDecision` deberá adquirir:

```python
candidate_content_identity: EpisodicCandidateContentIdentity
```

Invariantes:

```text
identity.candidate_id == candidate_id
```

Toda decisión producida por provenance debe copiar exactamente la identity del
assessment recibido.

La función cambia de:

```python
validate_assessment_provenance(
    assessment,
    expected_candidate_id,
    evaluated_at,
)
```

hacia:

```python
validate_assessment_provenance(
    assessment: AdmissionAssessment,
    expected_candidate_content_identity: EpisodicCandidateContentIdentity,
    evaluated_at: datetime,
) -> AssessmentProvenanceDecision
```

No se añade un segundo `expected_candidate_id`; el ID lógico ya está contenido en
ambos contratos y se valida explícitamente.

---

## 9. Provenance reason codes y precedencia

Se conserva:

```text
CANDIDATE_MISMATCH
```

para discrepancia de ID lógico.

Se agrega exactamente:

```python
AssessmentProvenanceReason.CONTENT_IDENTITY_MISMATCH = (
    "content_identity_mismatch"
)
```

Orden de evaluación congelado después de type/UTC validation:

```text
1. assessment.candidate_id != expected_identity.candidate_id
   → INVALID / CANDIDATE_MISMATCH

2. assessment.candidate_content_identity != expected_identity
   → INVALID / CONTENT_IDENTITY_MISMATCH

3. missing producer_role
   → HOLD

4. missing producer_reference
   → HOLD

5. missing policy_or_rule_reference
   → HOLD

6. missing assessed_at
   → HOLD

7. assessed_at > evaluated_at
   → HOLD

8. producer_role invalid for kind
   → INVALID

9. otherwise
   → VALID
```

Un content mismatch conocido **precede** HOLD por metadata incompleta. No puede
convertirse en un estado ambiguo/reintentable.

La decisión resultante siempre transporta la identity del assessment presentado,
no la expected identity.

Esto preserva evidencia de qué artefacto fue evaluado.

---

## 10. Contrato exacto — Producer Authorization Evidence

`AssessmentProducerAuthorizationEvidence` deberá adquirir:

```python
candidate_content_identity: EpisodicCandidateContentIdentity
```

Invariantes:

```text
identity.candidate_id == candidate_id
```

El evidence no puede afirmar `verified=True`, `trusted=True` ni equivalente.

Security contracts permanecen sin cambios:

```text
AuthorizationRequest
AuthorizationDecision
PermissionScope
```

---

## 11. Contrato exacto — Producer Authorization Decision

`AssessmentProducerAuthorizationDecision` deberá adquirir:

```python
candidate_content_identity: EpisodicCandidateContentIdentity
```

Toda decisión generada copia la identity del `AdmissionAssessment` evaluado.

Se agrega exactamente:

```python
AssessmentProducerAuthorizationReason.CONTENT_IDENTITY_MISMATCH = (
    "content_identity_mismatch"
)
```

No se cambia el significado de AUTHORIZED/HOLD/DENIED.

---

## 12. Producer Authorization — precedencia exacta relevante

Después de type/UTC validation:

```text
1. provenance_decision is None
   → HOLD / MISSING_PROVENANCE_DECISION

2. provenance assessment_id mismatch
   → DENIED / ASSESSMENT_ID_MISMATCH

3. provenance candidate_id mismatch
   → DENIED / CANDIDATE_ID_MISMATCH

4. provenance candidate_content_identity mismatch
   → DENIED / CONTENT_IDENTITY_MISMATCH

5. provenance kind mismatch
   → DENIED / KIND_MISMATCH

6. provenance HOLD
   → HOLD / PROVENANCE_HOLD

7. provenance INVALID
   → DENIED / PROVENANCE_INVALID
```

La igualdad en 4 es:

```text
provenance.identity == assessment.identity
```

Después se preservan las reglas existentes de influence/permission.

Cuando authorization evidence existe, antes de evaluar permiso/contexto:

```text
evidence.assessment_id == assessment.assessment_id

evidence.candidate_id == assessment.candidate_id

evidence.candidate_content_identity == assessment.candidate_content_identity

evidence.kind is assessment.kind
```

Mismatch de identity:

```text
DENIED / CONTENT_IDENTITY_MISMATCH
```

Un provenance HOLD con identity contradictoria no puede ocultar el mismatch.

---

## 13. Contrato exacto — GovernedTemporalControlEvidence

Se agrega campo obligatorio:

```python
candidate_content_identity: EpisodicCandidateContentIdentity
```

Invariantes de constructor:

```text
identity is correct type
identity.candidate_id == candidate_id
```

El evidence temporal no se exceptúa del binding porque controla `valid_from` /
`valid_until`, campos trust-sensitive para Admission.

No se modifica `AuthorizationRequest` ni `AuthorizationDecision`.

---

## 14. Contrato exacto — GovernedAdmissionInputProjection

Se agrega campo obligatorio para **todos los outcomes**:

```python
candidate_content_identity: EpisodicCandidateContentIdentity
```

Aplica a:

```text
READY
HOLD
DENIED
```

Invariante:

```text
projection.identity.candidate_id == projection.candidate_id
```

Una projection HOLD/DENIED no pierde identidad material por no ser consumible.

Policy version:

```text
episodic-admission-governed-input-projection/v2
```

---

## 15. Projection — verificación local no transitiva

`project_governed_admission_inputs(...)` dispone del `EpisodicMemoryCandidate` real.

Al comienzo de una invocación válida deberá calcular exactamente una vez:

```python
actual_identity = compute_episodic_candidate_content_identity(candidate)
```

Ese `actual_identity` es la referencia material de la invocación.

No se admite:

```text
use upstream "verified" bit
lookup cache by candidate_id
resolve another candidate after verification
trust an identity because previous component said MATCH
```

La función debe seguir operando sobre la misma instancia `candidate` recibida.

```text
verify-and-use same material
```

---

## 16. Projection reason codes nuevos

Se agregan exactamente:

```python
GovernedAdmissionProjectionReason.ASSESSMENT_CONTENT_IDENTITY_MISMATCH = (
    "assessment_content_identity_mismatch"
)
GovernedAdmissionProjectionReason.TEMPORAL_CONTENT_IDENTITY_MISMATCH = (
    "temporal_content_identity_mismatch"
)
```

`ASSESSMENT_BINDING_MISMATCH` se conserva para:

```text
assessment_id mismatch
candidate_id mismatch
kind mismatch
```

No absorbe content identity mismatch.

`TEMPORAL_CANDIDATE_MISMATCH` se conserva para ID lógico.

---

## 17. Projection — bundle binding exacto

Para cada `GovernedAssessmentProjectionInput`:

```text
assessment.assessment_id
== provenance.assessment_id
== producer_evidence.assessment_id
== producer_decision.assessment_id
```

```text
assessment.candidate_id
== provenance.candidate_id
== producer_evidence.candidate_id
== producer_decision.candidate_id
== candidate.candidate_id
```

```text
assessment.kind
is provenance.kind
is producer_evidence.kind
is producer_decision.kind
```

Y además:

```text
assessment.identity
== provenance.identity
== producer_evidence.identity
== producer_decision.identity
== actual_identity
```

Cualquier divergencia de identity:

```text
DENIED / ASSESSMENT_CONTENT_IDENTITY_MISMATCH
```

antes de poder producir READY.

La proyección no debe llamar a canonicalización propia ni comparar solo digest.

---

## 18. Projection — temporal binding exacto

Cuando existe `GovernedTemporalControlEvidence`:

```text
temporal.candidate_id == candidate.candidate_id
```

se evalúa con el reason existente `TEMPORAL_CANDIDATE_MISMATCH`.

Luego:

```text
temporal.candidate_content_identity == actual_identity
```

Mismatch:

```text
DENIED / TEMPORAL_CONTENT_IDENTITY_MISMATCH
```

antes de usar `valid_from` / `valid_until`.

---

## 19. Projection — precedencia de denied findings

Ranking exacto v2:

```text
1  ASSESSMENT_CONTENT_IDENTITY_MISMATCH
2  ASSESSMENT_BINDING_MISMATCH
3  ASSESSMENT_PROVENANCE_INVALID
4  ASSESSMENT_AUTHORIZATION_DENIED
5  INVALID_EFFECTIVE_ASSESSMENT_VALUE
6  TEMPORAL_CANDIDATE_MISMATCH
7  TEMPORAL_CONTENT_IDENTITY_MISMATCH
8  TEMPORAL_PRODUCER_SUBJECT_MISMATCH
9  TEMPORAL_PERMISSION_SCOPE_MISMATCH
10 TEMPORAL_DECISION_REQUEST_MISMATCH
11 TEMPORAL_CONTEXT_NOT_YET_VALID / TEMPORAL_CONTEXT_EXPIRED
12 TEMPORAL_AUTHORIZATION_DENIED
```

HOLD ranking permanece:

```text
1 ASSESSMENT_PROVENANCE_HOLD
2 ASSESSMENT_AUTHORIZATION_HOLD
3 DUPLICATE_REQUIRED_ASSESSMENT
4 MISSING_REQUIRED_ASSESSMENT
5 INVALID_EFFECTIVE_ASSESSMENT_VALUE
6 MISSING_TEMPORAL_CONTROL
```

Known identity mismatch siempre pertenece a DENIED, nunca HOLD.

Todas las projections resultantes llevan:

```text
candidate_content_identity = actual_identity
```

incluso cuando el finding proviene de evidence stale.

El reason code conserva la causa; el campo identity declara el candidate real de
la evaluación de projection.

---

## 20. Contrato exacto — GovernedAdmissionConsumptionResult

El terminal content-bound adquiere dos campos obligatorios:

```python
actual_candidate_content_identity: EpisodicCandidateContentIdentity
presented_projection_content_identity: EpisodicCandidateContentIdentity
```

No se reemplazan por un booleano `verified`.

`actual_candidate_content_identity`:

```text
identity calculada desde el exact candidate pasado a Consumption
```

`presented_projection_content_identity`:

```text
identity transportada por la exact projection presentada a Consumption
```

Invariante siempre:

```text
result.actual_candidate_content_identity.candidate_id == result.candidate_id
```

Para `EVALUATED`:

```text
actual_identity == presented_identity
admission_decision is not None
```

Para BLOCKED por mismatch de ID o identity:

```text
actual_identity may differ from presented_identity
admission_decision is None
```

Para cualquier otro BLOCKED:

```text
actual_identity == presented_identity
```

Esto preserva evidencia del mismatch sin confundir cuál candidate fue realmente
suministrado.

---

## 21. Consumption reason code nuevo

Se agrega exactamente:

```python
GovernedAdmissionConsumptionReason.CONTENT_IDENTITY_BINDING_MISMATCH = (
    "content_identity_binding_mismatch"
)
```

Se conserva:

```text
CANDIDATE_BINDING_MISMATCH
```

para diferencia de `candidate_id`.

---

## 22. Consumption — orden exacto

Después de type/UTC validation:

```text
1. actual_identity = compute(candidate)
2. presented_identity = projection.candidate_content_identity

3. projection.candidate_id != candidate.candidate_id
   → BLOCKED / CANDIDATE_BINDING_MISMATCH

4. verify_episodic_candidate_content_identity(candidate, presented_identity)
   != MATCH
   → BLOCKED / CONTENT_IDENTITY_BINDING_MISMATCH

5. projection.policy_version != projection v2
   → BLOCKED / UNSUPPORTED_PROJECTION_POLICY

6. evaluated_at < projection.evaluated_at
   → BLOCKED / CONSUMPTION_TIME_PRECEDES_PROJECTION

7. projection DENIED
   → BLOCKED / PROJECTION_DENIED

8. projection HOLD
   → BLOCKED / PROJECTION_HOLD

9. effective context mismatch
   → BLOCKED / CONTEXT_BINDING_MISMATCH

10. otherwise call Admission exactly once
    → EVALUATED
```

No se llama `evaluate_episodic_candidate(...)` en steps 3–9.

Consumption no acepta una assertion previa de verification como sustituto del step 4.

---

## 23. Compromise-Aware Binding — reglas congeladas

### 23.1. Verification is local, not transitive

Cuando una frontera tiene el candidate real:

```text
Projection  → computes actual identity locally
Consumption → verifies locally again
```

La segunda verificación no se elimina porque la primera exista.

### 23.2. No self-attestation

Prohibido agregar campos equivalentes a:

```text
verified
trusted
integrity_ok
component_attested
```

como fuente de autoridad dentro de esta unidad.

### 23.3. No verification cache as authority

No global cache, registry, singleton ni memoización por `candidate_id` que permita
omitir una verificación requerida.

### 23.4. No re-resolution

Después de calcular/verificar identity de la instancia recibida, la frontera no
vuelve a resolver candidate por ID, storage, registry, filesystem o network.

### 23.5. Unable-to-verify = fail closed

No existe `best effort`.

Metadata criptográfica incompatible, identity ausente por artefacto inválido o
MISMATCH no puede caer a candidate-id-only.

### 23.6. Component compromise boundary

Una salida semánticamente falsa pero correctamente ligada al candidate no se
convierte en verdadera por content identity.

```text
correct binding
!=
producer correctness
```

Esta unidad tampoco vuelve tamper-proof al runtime Python.

```text
terminal content-bound artifact
!=
tamper-proof artifact
!=
independently trustworthy artifact
```

---

## 24. Admission permanece intacta

No se modifica:

```text
EpisodicMemoryCandidate
EpisodicAdmissionDecision
evaluate_episodic_candidate
Admission precedence
```

La protección queda alrededor:

```text
content-bound projection
        ↓
independent Consumption verify
        ↓
Admission
        ↓
content-bound Consumption result
```

Una `EpisodicAdmissionDecision` aislada continúa sin ser evidencia suficiente para
Persistence Authorization.

---

## 25. No Security authority delta

No se modifican:

```text
AuthorizationRequest
AuthorizationDecision
PermissionScope
PDP
PEP
SecurityContext
```

La content identity no concede permiso.

Producer Authorization continúa respondiendo:

```text
¿este productor estaba autorizado para producir esta clase de assessment?
```

Content binding responde:

```text
¿estos artefactos se refieren al mismo exact candidate content?
```

Son controles ortogonales.

---

## 26. TDD contract congelado

La futura implementación debe empezar por tests y cubrir, como mínimo:

### 26.1. Constructor contracts

- `AdmissionAssessment` exige identity y rechaza wrong type;
- assessment `candidate_id` != identity.candidate_id → ValueError;
- ProvenanceDecision exige identity;
- ProducerAuthorizationEvidence exige identity;
- ProducerAuthorizationDecision exige identity;
- TemporalControlEvidence exige identity;
- Projection exige identity;
- ConsumptionResult exige actual + presented identity.

### 26.2. Provenance

- same candidate ID + different content identity → INVALID / CONTENT_IDENTITY_MISMATCH;
- candidate ID mismatch → INVALID / CANDIDATE_MISMATCH;
- identity mismatch precede missing producer metadata HOLD;
- valid path echoes exact assessment identity;
- expected identity wrong type → TypeError.

### 26.3. Producer authorization

- provenance identity mismatch → DENIED / CONTENT_IDENTITY_MISMATCH;
- evidence identity mismatch → DENIED / CONTENT_IDENTITY_MISMATCH;
- identity mismatch precede PROVENANCE_HOLD cuando el provenance está materialmente ligado a otra identity;
- AUTHORIZED output carries assessment identity;
- permission semantics existentes no cambian.

### 26.4. Temporal evidence

- temporal identity candidate mismatch rejected structurally;
- temporal evidence same ID but stale identity → projection DENIED / TEMPORAL_CONTENT_IDENTITY_MISMATCH.

### 26.5. Projection bundle

- each of assessment/provenance/evidence/decision stale independently → DENIED / ASSESSMENT_CONTENT_IDENTITY_MISMATCH;
- same-ID candidate substitution fails;
- no mismatch can produce READY;
- projection outputs actual computed candidate identity for READY/HOLD/DENIED;
- algorithm/canonicalization/policy metadata mismatch fails closed;
- no digest-only acceptance.

### 26.6. Consumption

- same candidate ID + stale projection identity → BLOCKED / CONTENT_IDENTITY_BINDING_MISMATCH;
- candidate ID mismatch remains CANDIDATE_BINDING_MISMATCH;
- actual and presented identities both preserved on blocked mismatch;
- EVALUATED requires actual == presented;
- unsupported projection policy with matching identity remains blocked by existing reason;
- identity mismatch occurs before policy/outcome/context checks;
- Admission evaluator not invoked on identity mismatch;
- successful path calls Admission exactly once.

### 26.7. No transitive verification

Tests/review evidence must demonstrate que Consumption usa `verify_episodic_candidate_content_identity`
sobre el candidate recibido y no un upstream flag/cache.

No se requiere una abstracción de attestation.

### 26.8. TOCTOU boundary

El same-ID substitution corpus debe demostrar que una identity obtenida de candidate X
no permite evaluar candidate Y con el mismo ID.

No se introduce lookup/resolver para producir el test.

### 26.9. Regression

- full pytest PASS;
- Candidate Content Identity vectors A/B/C permanecen PASS;
- Admission precedence intacta;
- Producer Authorization semantics intactas;
- Projection cardinality/temporal semantics intactas;
- Consumption side-effect isolation intacta.

---

## 27. Forbidden test shortcuts

No se aceptan tests que hagan pasar el candidate mediante:

- cambiar los expected digests de Candidate Content Identity;
- monkeypatch de canonicalización;
- convertir identity en Optional;
- construir artifacts sin identity usando defaults ocultos;
- fixture global de `verified=True`;
- comparar solo `digest_hex`;
- omitir same-ID substitution;
- cambiar Admission expected outcomes para acomodar propagation.

Monkeypatch de `evaluate_episodic_candidate` es aceptable únicamente en un test
acotado para demostrar `not invoked on mismatch` / `exactly once on success`, sin
alterar reglas de Admission.

---

## 28. FULL 4R — criterios exactos

### Risk

PASS requiere demostrar:

```text
identity != trust
binding != authority
binding != producer correctness
binding != Persistence Authorization
```

Y ausencia de fallback legacy.

### Readability

Un reviewer debe poder seguir explícitamente:

```text
candidate identity
→ assessment
→ provenance
→ producer auth
→ temporal evidence
→ projection
→ consumption actual/presented identities
```

sin helper genérico opaco ni estado global.

### Reliability

PASS requiere:

- same-ID substitution matrix;
- cross-artifact stale identity matrix;
- metadata incompatibility;
- Ubuntu candidate-bound PASS;
- Windows candidate-bound PASS;
- full pytest;
- compileall;
- git diff --check.

### Resilience

PASS requiere:

- no Optional identity;
- no candidate-id fallback;
- no digest-only comparison;
- no verification transitivity;
- no self-attestation;
- no re-resolution after verify;
- identity mismatch never reaches Admission.

---

## 29. RDD Stage 1 evidence

La futura implementación deberá emitir `MALAK-EVIDENCE-MANIFEST/v1` ligado al SHA
exacto del candidate de implementación.

Debe declarar al menos:

```text
base_sha
candidate_sha
risk_class
files changed
file budget
correction round
FULL 4R
pytest result
compileall result
diff-check result
Ubuntu observation
Windows observation
blocking findings
```

Se mantiene:

```text
Stage 1 evidence
!=
independent reviewer authority
!=
validator authority
!=
merge authority
```

RDD Stage 2 continúa no autorizado.

---

## 30. Candidate implementation shape

La implementación futura será **un único candidate atómico**.

Las fases TDD lógicas son:

```text
P1  Assessment + Provenance
P2  Producer Authorization
P3  Projection + Temporal binding
P4  Consumption terminal binding
```

Puede haber commits internos separados para preservar TDD y revisión, pero:

```text
NO partial merge of P1/P2/P3/P4 to main
```

Motivo:

una migración parcial exigiría identity opcional o compatibilidad v1/v2 dentro de
la misma cadena, lo cual reabre el bypass que esta unidad intenta cerrar.

---

## 31. STOP conditions

La futura implementación debe detenerse si requiere:

- modificar `EpisodicMemoryCandidate`;
- modificar `candidate_content_identity.py` sin inconsistencia demostrada;
- cambiar canonicalization v1;
- cambiar vectors A/B/C;
- modificar `EpisodicAdmissionDecision`;
- modificar Admission precedence;
- modificar Security contracts / PDP / PEP;
- introducir Persistence Authorization;
- introducir Memory store;
- introducir retrieval / Knowledge;
- introducir Conversation/Kernel wiring;
- introducir HMAC, firma, PKI o attestation;
- introducir dependency externa;
- agregar identity Optional;
- agregar legacy candidate-id-only fallback;
- agregar `verified`/`trusted` self-attestation field;
- agregar verification cache/registry como autoridad;
- re-resolver candidate por ID después de verificar;
- aceptar digest-only matching;
- requerir un quinto módulo productivo;
- exceder 2 material correction rounds;
- exceder file/LOC budget sin nueva decisión del Owner.

---

## 32. Pass criteria de futura implementación

La unidad solo puede considerarse implementation-complete si:

```text
4 production files only                    PASS
4 test files only                          PASS
0 new production files                     PASS
0 external dependencies                    PASS
policy v2 migration                        PASS
mandatory full sidecar propagation         PASS
same-ID substitution                       FAIL-CLOSED
cross-artifact stale identity              FAIL-CLOSED
Projection local compute                   PASS
Consumption independent verify             PASS
actual/presented terminal identities        PASS
no self-attestation                        PASS
no verification transitivity               PASS
no candidate-id fallback                   PASS
Admission isolation                        PASS
full pytest                                PASS
compileall                                 PASS
git diff --check                           PASS
Ubuntu CI                                  PASS
Windows CI                                 PASS
FULL 4R                                    PASS
RDD Stage 1 manifest                       PASS
blocking findings                          0
```

Al completar estos criterios:

```text
STOP
```

No se autoriza automáticamente Persistence Authorization.

---

## 33. Residual explícito después de implementación

Aun con propagation/binding completa permanecerán abiertos:

```text
component authenticity
runtime tamper resistance
producer semantic correctness
independent attestation
authorization replay outside current contracts
Persistence Authorization policy
stored-content integrity
revocation / quarantine
trust-aware retrieval
Knowledge promotion
```

La futura revisión de Persistence Authorization deberá evaluar si el
`GovernedAdmissionConsumptionResult` content-bound es evidencia suficiente y qué
otros controles son necesarios.

No puede asumirlo por defecto.

---

## 34. Resultado G2-SPEC

```text
unit:
Episodic Candidate Content Identity Propagation & Binding Boundary

baseline:
d08d4ccb77c704d1831e7e2a1c6dfbc337dbe67e

G0/G1:
MERGED / HARDENED

G2-SPEC:
AUTHORIZED / FROZEN BY THIS DOCUMENT

future implementation scope:
4 existing production modules
4 existing test modules
0 new production modules
0 external dependencies

contract migration:
v1 candidate-id-primary artifacts
→ v2 mandatory content-bound artifacts

compromise-aware requirements:
local non-transitive verification
no self-attestation
no verified cache authority
no post-check re-resolution
fail closed unable-to-verify
actual + presented identities preserved at terminal

implementation authorized:
false

Persistence Authorization authorized:
false
Persistent Memory authorized:
false
RDD Stage 2 authorized:
false
Sprint 7.12 authorized:
false
```

Disposición:

```text
G2-SPEC RESULT: ADOPT FOR OWNER REVIEW
NEXT GATE: explicit Owner authorization for TDD + implementation only
```

El merge de esta spec no constituye autorización automática de código.
