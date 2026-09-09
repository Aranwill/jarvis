---
title: Episodic Admission Governed Input Projection Boundary — G2 Implementation Candidate Specification
status: g2_implementation_candidate_spec_review
authority: owner-approved specification record
as_of_date: 2026-09-09
unit: Episodic Admission Governed Input Projection Boundary
gate: G2
source_baseline: 84a7bc2f785751d478d8a1341f993d861cb2f208
risk_class: 3
vault_reconciliation_status_at_start: resolved
vault_head_at_start: cbd5f74070176e5c20d300b811153e73d95f9d3f
sdd_required: true
tdd_required: true
full_4r_required: true
rdd_stage_1: adopted
rdd_stage_2_authorized: false
implementation_authorized: false
admission_wiring_authorized: false
security_control_plane_change_authorized: false
persistent_memory_authorized: false
retrieval_authorized: false
knowledge_implementation_authorized: false
sprint_7_12_authorized: false
vault_reconciliation_required_before_implementation: true
language: es
---

# Episodic Admission Governed Input Projection Boundary — G2 Implementation Candidate Specification

## 1. Estado de autoridad

El Owner autorizó exclusivamente la materialización de G2 como especificación del candidato de implementación para:

```text
Episodic Admission Governed Input Projection Boundary
```

G2 congela contratos, temporal governance, cardinalidad, mapping, precedencia, escenarios TDD, FULL 4R, bounded correction, file budget y STOP conditions.

G2 no autoriza todavía:

- código productivo;
- tests de implementación;
- cambios a `episodic_admission.py`;
- cambios a `assessment_provenance.py`;
- cambios a `assessment_producer_authorization.py`;
- cambios a `SecurityContext`, PDP o PEP;
- wiring hacia Admission, Conversation o runtime;
- persistencia, retrieval o Knowledge;
- agentes, tools o red;
- identidad criptográfica, PKI, firmas, nonce o replay protection;
- Sprint 7.12;
- RDD Stage 2;
- merge sin decisión humana.

```text
Specification != Implementation
Projection READY != Admission ELIGIBLE
Evidence != Authority
```

---

## 2. Baseline exacto y precondiciones

Baseline fuente congelado:

```text
Aranwill/jarvis
main
84a7bc2f785751d478d8a1341f993d861cb2f208
```

Estado cross-repository al iniciar G2:

```text
Malāk main:
84a7bc2f785751d478d8a1341f993d861cb2f208

Project Vault main:
cbd5f74070176e5c20d300b811153e73d95f9d3f

post-reconciliation dry-run:
base_commit == head_commit == 84a7bc2f...
changed_files = 0
document_candidates = 0
validation_findings = 0
conclusion = pass
proposal_created = false
```

Precondiciones:

```text
G0 PASS / ADAPT
G1 PASS + integrated
Assessment Provenance G3 integrated
Assessment Producer Authorization G3 integrated
Vault reconciliation PASS
drift = 0
```

---

## 3. Método de construcción obligatorio

La unidad conserva el método vigente de Malāk:

```text
SDD
  ↓
G2 specification
  ↓
TDD: RED → GREEN → REFACTOR when justified
  ↓
FULL 4R
  ↓
Bounded Correction if findings exist
  ↓
Independent Validation
  ↓
Candidate-Bound Evidence / RDD Stage 1
  ↓
Human Governance
  ↓
Vault reconciliation
```

Invariantes:

```text
Writer != Reviewer != Validator != Authority
Evidence != Receipt != Validation != Decision != Authority
candidate changes -> prior candidate-bound evidence must be revalidated
```

---

## 4. Problema exacto

El baseline dispone de fronteras separadas:

```text
AdmissionAssessment
        ↓
Assessment Provenance
VALID | HOLD | INVALID
        ↓
Producer Authorization
AUTHORIZED | HOLD | DENIED
```

Y por separado:

```text
EpisodicMemoryCandidate
+
EpisodicAdmissionSignals
        ↓
Episodic Admission
REJECT | HOLD | ELIGIBLE
```

La proyección futura debe responder solo:

> ¿existe un conjunto completo, coherente, candidate-bound y gobernado de inputs efectivos que pueda ser entregado posteriormente a la policy de admisión?

No debe responder:

```text
¿es el candidate ELIGIBLE?
¿debe persistirse?
¿debe recuperarse?
¿debe promoverse a Knowledge?
```

---

## 5. Separaciones obligatorias

```text
CONTENT
!= ASSESSMENT
!= STRUCTURAL PROVENANCE
!= PRODUCER AUTHORIZATION
!= GOVERNED TEMPORAL CONTROL
!= EFFECTIVE ADMISSION INPUT
!= ADMISSION DECISION
!= PERSISTENCE AUTHORIZATION
!= AUTHORITY
```

También:

```text
AUTHORIZED assessment != trusted truth
Projection READY != ELIGIBLE
Projection HOLD != admission HOLD automatically
Projection DENIED != candidate REJECT automatically
candidate.control value present != governed effective admission value
```

---

## 6. Decisión G2-D1 — file budget del candidato futuro

El candidato G3 futuro queda limitado a:

```text
NEW
src/malak/memory/governed_input_projection.py

NEW
tests/test_governed_input_projection.py

MODIFY existing production files = 0
```

Cambios explícitamente no permitidos en G3 bajo esta especificación:

```text
src/malak/memory/episodic_admission.py                 0
src/malak/memory/assessment_provenance.py             0
src/malak/memory/assessment_producer_authorization.py 0
src/malak/security/**                                 0
src/malak/kernel/**                                   0
Conversation/runtime                                  0
```

Si la implementación exige modificar alguno de esos límites:

```text
STOP → ESCALATE → new Owner decision
```

---

## 7. Decisión G2-D2 — projection no ejecuta Admission

La API candidata termina en:

```text
READY | HOLD | DENIED
```

y no llama:

```python
evaluate_episodic_candidate(...)
```

La projection valida governance y representabilidad.
Admission conserva la semántica de policy.

```text
Projection validates inputs
Admission evaluates policy
```

---

## 8. Decisión G2-D3 — temporal governance v1 usa evidencia dedicada

G1 dejó dos alternativas para temporal validity. G2 selecciona una sola:

```text
Dedicated Governed Temporal Control Evidence
```

Se descarta para v1 una TTL inventada o derivada implícitamente porque el baseline no contiene una TTL canónica aprobada.

No existe fallback dual.

```text
candidate.control.valid_from / valid_until
!= governed temporal control
```

La temporal governance v1 reutiliza los contratos existentes de Security sin crear otro PDP.

PermissionScope exacto:

```text
resource = "memory.episodic_admission.temporal_control"
action   = "produce.validity_window"
```

No wildcards.
No prefix matching.
No implicit inheritance.

---

## 9. Contrato exacto — `GovernedTemporalControlEvidence`

El módulo candidato debe definir:

```python
@dataclass(frozen=True, slots=True)
class GovernedTemporalControlEvidence:
    candidate_id: str
    valid_from: datetime
    valid_until: datetime
    policy_or_rule_reference: str
    producer_subject_id: str
    request: AuthorizationRequest
    decision: AuthorizationDecision
```

Validaciones constructoras:

- `candidate_id`, `policy_or_rule_reference` y `producer_subject_id` canónicos, no vacíos y sin whitespace periférico;
- `valid_from` y `valid_until` deben ser `datetime` UTC aware;
- `valid_until > valid_from`;
- `request` debe ser `AuthorizationRequest`;
- `decision` debe ser `AuthorizationDecision`.

Semántica:

```text
Temporal evidence
!= persistence TTL
!= retention policy
!= authorization token
!= cryptographic proof
!= admission decision
```

G2 no impone relación semántica entre `candidate.created_at` y el intervalo. Esa relación, si alguna vez se necesita, requiere policy explícita.

---

## 10. Decisión G2-D4 — validación temporal al momento de proyección

La temporal evidence es utilizable solo si:

```text
evidence.candidate_id == candidate.candidate_id
producer_subject_id == request.context.subject_id
request.permission == exact temporal PermissionScope
decision.request_id == request.request_id
evaluated_at >= context.issued_at
evaluated_at < context.expires_at
decision.allowed is True
```

El momento `evaluated_at` debe ser UTC.

Importante:

```text
valid_from > evaluated_at
```

no es finding de projection.

Y:

```text
valid_until <= evaluated_at
```

no es finding de projection.

Si la evidencia temporal está gobernada y estructuralmente válida, la projection puede ser `READY`; posteriormente Admission decide `TEMPORAL_NOT_YET_VALID` o `TEMPORAL_EXPIRED` según corresponda.

Esto preserva:

```text
Temporal governance != Temporal admission semantics
```

---

## 11. Decisión G2-D5 — bundle exacto por assessment

El candidato debe definir:

```python
@dataclass(frozen=True, slots=True)
class GovernedAssessmentProjectionInput:
    assessment: AdmissionAssessment
    provenance_decision: AssessmentProvenanceDecision
    producer_authorization_evidence: AssessmentProducerAuthorizationEvidence
    producer_authorization_decision: AssessmentProducerAuthorizationDecision
```

El bundle es evidence plumbing; no concede autoridad.

Validaciones constructoras:

- tipos exactos de los cuatro contratos;
- no coerción;
- no I/O;
- no mutación de objetos existentes.

La projection no debe tratar el outcome de una decisión como un booleano libre. Debe verificar bindings exactos contra el assessment actual y contra la evidencia subyacente.

Residual explícito:

```text
structural binding
!= cryptographic content integrity
!= authenticated external producer identity
```

---

## 12. Decisión G2-D6 — bindings exactos por assessment

Para que un bundle sea utilizable deben cumplirse, como mínimo:

```text
assessment.assessment_id
== provenance_decision.assessment_id
== producer_authorization_evidence.assessment_id
== producer_authorization_decision.assessment_id

assessment.candidate_id
== provenance_decision.candidate_id
== producer_authorization_evidence.candidate_id
== producer_authorization_decision.candidate_id
== candidate.candidate_id

assessment.kind
== provenance_decision.kind
== producer_authorization_evidence.kind
== producer_authorization_decision.kind
```

Además:

```text
provenance_decision.outcome == VALID
producer_authorization_decision.outcome == AUTHORIZED
```

La evidence de producer authorization debe permanecer consistente con:

```text
assessment value -> deterministic influence class
required PermissionScope
producer subject
request_id
SecurityContext lifecycle
AuthorizationDecision.allowed
```

La implementación puede reutilizar funciones puras ya existentes para verificar esos invariantes; no debe reimplementar PDP/PEP ni inventar autoridad propia.

---

## 13. Decisión G2-D7 — cardinalidad exacta y orden independiente

Los ocho `AssessmentKind` vigentes son requeridos:

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

Para cada kind:

```text
0 input bundles -> HOLD
1 input bundle  -> validate and continue
>1 bundles      -> HOLD
```

Incluso si dos bundles duplicados expresan el mismo valor:

```text
>1 == ambiguous cardinality -> HOLD
```

Prohibido resolver por:

```text
input order
last-write-wins
latest timestamp
highest confidence
producer role priority
lexicographic ordering
```

La colección de entrada puede llegar en cualquier orden y el resultado debe ser idéntico.

---

## 14. Decisión G2-D8 — mapping cerrado a inputs efectivos

Mapping exacto:

| AssessmentKind | Effective target |
|---|---|
| `SOURCE_AUTHORITY` | `context.source_authority_classification` |
| `CONFIDENCE` | `context.confidence_classification` |
| `SENSITIVITY` | `context.sensitivity_classification` |
| `SOURCE_SECURITY_STATUS` | `signals.source_security_status` |
| `SCOPE_APPLICABLE` | `signals.scope_applicable` |
| `POLICY_VIOLATION` | `signals.policy_violation` |
| `SENSITIVE_REVIEW_REQUIRED` | `signals.sensitive_review_required` |
| `CONTRADICTION_REQUIRES_REVIEW` | `signals.contradiction_requires_review` |

Temporal evidence proyecta:

```text
context.valid_from
context.valid_until
```

Metadata contextual neutral se copia del candidate original:

```text
context.subject_scope
context.domain
context.purpose
```

Esa metadata:

```text
cannot create READY by itself
cannot replace SCOPE_APPLICABLE
cannot grant authority
cannot create ELIGIBLE
```

---

## 15. Decisión G2-D9 — no fallback a trust-sensitive `candidate.control`

Para construir el `EpisodicAdmissionContext` efectivo, la projection debe ignorar como autoridad los valores preexistentes de:

```text
candidate.control.source_authority_classification
candidate.control.confidence_classification
candidate.control.sensitivity_classification
candidate.control.valid_from
candidate.control.valid_until
```

Aunque esos campos estén completos, no sustituyen evidencia gobernada.

La projection crea un **nuevo** `EpisodicAdmissionContext`.

El candidate original no se muta.

---

## 16. Decisión G2-D10 — type semantics exactas

Tipos efectivos:

```text
SOURCE_AUTHORITY              -> canonical str
CONFIDENCE                    -> canonical str
SENSITIVITY                   -> canonical str
SOURCE_SECURITY_STATUS        -> SourceSecurityStatus
SCOPE_APPLICABLE              -> bool exacto
POLICY_VIOLATION              -> bool exacto
SENSITIVE_REVIEW_REQUIRED     -> bool exacto
CONTRADICTION_REQUIRES_REVIEW -> bool exacto
```

No coerción:

```text
"false" != False
1 != True
"acceptable " != ACCEPTABLE
unknown security string != UNASSESSED
```

Para `SOURCE_SECURITY_STATUS`, la conversión solo puede usar un valor canónico exacto reconocido por `SourceSecurityStatus`.

---

## 17. Contratos exactos de resultado

### 17.1 `GovernedAdmissionProjectionOutcome`

```python
class GovernedAdmissionProjectionOutcome(StrEnum):
    READY = "ready"
    HOLD = "hold"
    DENIED = "denied"
```

### 17.2 `GovernedAdmissionProjectionReason`

G2 congela estos reason codes:

```text
ASSESSMENT_BINDING_MISMATCH
ASSESSMENT_PROVENANCE_HOLD
ASSESSMENT_PROVENANCE_INVALID
ASSESSMENT_AUTHORIZATION_HOLD
ASSESSMENT_AUTHORIZATION_DENIED
MISSING_REQUIRED_ASSESSMENT
DUPLICATE_REQUIRED_ASSESSMENT
INVALID_EFFECTIVE_ASSESSMENT_VALUE
MISSING_TEMPORAL_CONTROL
TEMPORAL_CANDIDATE_MISMATCH
TEMPORAL_PRODUCER_SUBJECT_MISMATCH
TEMPORAL_PERMISSION_SCOPE_MISMATCH
TEMPORAL_DECISION_REQUEST_MISMATCH
TEMPORAL_CONTEXT_NOT_YET_VALID
TEMPORAL_CONTEXT_EXPIRED
TEMPORAL_AUTHORIZATION_DENIED
READY
```

### 17.3 `GovernedAdmissionInputProjection`

```python
@dataclass(frozen=True, slots=True)
class GovernedAdmissionInputProjection:
    candidate_id: str
    outcome: GovernedAdmissionProjectionOutcome
    reason_code: GovernedAdmissionProjectionReason
    evaluated_at: datetime
    effective_context: EpisodicAdmissionContext | None = None
    effective_signals: EpisodicAdmissionSignals | None = None
    finding_kind: AssessmentKind | None = None
    policy_version: str = POLICY_VERSION
```

Reglas:

```text
READY  -> effective_context and effective_signals required
HOLD   -> both None
DENIED -> both None
```

`finding_kind` se usa solo cuando el finding corresponde a una assessment concreta; para temporal findings permanece `None`.

---

## 18. API pública candidata

El módulo candidato debe exponer únicamente lo necesario:

```python
POLICY_VERSION
GovernedTemporalControlEvidence
GovernedAssessmentProjectionInput
GovernedAdmissionProjectionOutcome
GovernedAdmissionProjectionReason
GovernedAdmissionInputProjection
project_governed_admission_inputs(...)
```

Firma principal:

```python
def project_governed_admission_inputs(
    candidate: EpisodicMemoryCandidate,
    assessment_inputs: tuple[GovernedAssessmentProjectionInput, ...],
    temporal_control: GovernedTemporalControlEvidence | None,
    evaluated_at: datetime,
) -> GovernedAdmissionInputProjection:
    ...
```

La función:

- no recibe LLM;
- no recibe PDP o PEP;
- no persiste;
- no hace network;
- no genera `AuthorizationRequest`;
- no llama Admission;
- no muta inputs.

---

## 19. Precedencia determinista global

La projection debe ser independiente del orden de entrada.

Clases de findings:

```text
DENIED findings > HOLD findings > READY
```

Dentro de `DENIED`, prioridad:

```text
1. assessment binding mismatch
2. provenance INVALID
3. producer authorization DENIED
4. invalid effective assessment value when it represents structural incompatibility
5. temporal candidate mismatch
6. temporal producer subject mismatch
7. temporal permission mismatch
8. temporal request/decision mismatch
9. temporal context not yet valid / expired
10. temporal authorization denied
```

Dentro de `HOLD`, prioridad:

```text
1. provenance HOLD
2. producer authorization HOLD
3. duplicate required assessment
4. missing required assessment
5. invalid/unsupported effective assessment value that cannot be classified safely
6. missing temporal control
```

Cuando múltiples assessment kinds tienen el mismo nivel de finding, el desempate usa el orden canónico de §13, nunca el orden de entrada.

La razón de esta precedencia es trazabilidad determinista, no policy de Admission.

---

## 20. Construcción efectiva en READY

Solo después de validar 8/8 dimensiones y temporal governance, construir:

```python
EpisodicAdmissionContext(
    subject_scope=candidate.control.subject_scope,
    domain=candidate.control.domain,
    purpose=candidate.control.purpose,
    source_authority_classification=<SOURCE_AUTHORITY value>,
    confidence_classification=<CONFIDENCE value>,
    sensitivity_classification=<SENSITIVITY value>,
    valid_from=temporal_control.valid_from,
    valid_until=temporal_control.valid_until,
)
```

Y:

```python
EpisodicAdmissionSignals(
    scope_applicable=<SCOPE_APPLICABLE>,
    policy_violation=<POLICY_VIOLATION>,
    source_security_status=<SOURCE_SECURITY_STATUS>,
    sensitive_review_required=<SENSITIVE_REVIEW_REQUIRED>,
    contradiction_requires_review=<CONTRADICTION_REQUIRES_REVIEW>,
)
```

Ningún valor trust-sensitive se toma como fallback del `candidate.control` original.

---

## 21. Escenarios TDD obligatorios para G3

### Contratos y tipos

- **GP2-T01** — projection inputs y output son inmutables.
- **GP2-T02** — `evaluated_at` naive falla en construcción/llamada.
- **GP2-T03** — `evaluated_at` aware no UTC falla.
- **GP2-T04** — temporal `valid_from`/`valid_until` exigen UTC.
- **GP2-T05** — temporal `valid_until <= valid_from` falla.

### Side-door / no fallback

- **GP2-T06** — candidate con authority/confidence/sensitivity completos pero sin assessment gobernada -> HOLD.
- **GP2-T07** — candidate con valid_from/valid_until completos pero sin temporal evidence -> HOLD.
- **GP2-T08** — valores trust-sensitive del candidate no sobrescriben assessments gobernadas.
- **GP2-T09** — candidate original no se muta.

### Cardinalidad

- **GP2-T10** — falta SOURCE_AUTHORITY -> HOLD.
- **GP2-T11** — falta cualquiera de los ocho kinds -> HOLD.
- **GP2-T12** — dos bundles del mismo kind y mismo valor -> HOLD.
- **GP2-T13** — dos bundles del mismo kind con valores distintos -> HOLD.
- **GP2-T14** — reordenar la colección no cambia outcome/reason.

### Provenance y authorization

- **GP2-T15** — provenance HOLD -> HOLD.
- **GP2-T16** — provenance INVALID -> DENIED.
- **GP2-T17** — authorization HOLD -> HOLD.
- **GP2-T18** — authorization DENIED -> DENIED.
- **GP2-T19** — assessment_id mismatch -> DENIED.
- **GP2-T20** — candidate_id mismatch -> DENIED.
- **GP2-T21** — kind mismatch -> DENIED.
- **GP2-T22** — evidence/request permission incompatible con assessment actual -> DENIED.
- **GP2-T23** — producer subject mismatch -> DENIED.
- **GP2-T24** — request/decision mismatch -> DENIED.

### Effective value semantics

- **GP2-T25** — boolean string `"false"` no se coerciona a bool.
- **GP2-T26** — integer `1` no se coerciona a bool.
- **GP2-T27** — source security desconocido no se convierte a UNASSESSED.
- **GP2-T28** — `"acceptable "` no se normaliza silenciosamente.

### Temporal governance

- **GP2-T29** — temporal control missing -> HOLD.
- **GP2-T30** — temporal candidate mismatch -> DENIED.
- **GP2-T31** — temporal producer subject mismatch -> DENIED.
- **GP2-T32** — temporal permission mismatch -> DENIED.
- **GP2-T33** — temporal decision/request mismatch -> DENIED.
- **GP2-T34** — SecurityContext temporal not-yet-valid -> DENIED.
- **GP2-T35** — SecurityContext temporal expired -> DENIED.
- **GP2-T36** — temporal AuthorizationDecision denied -> DENIED.
- **GP2-T37** — governed window todavía no iniciado puede producir READY.
- **GP2-T38** — governed window ya expirado puede producir READY; Admission semantics queda fuera de esta frontera.

### READY

- **GP2-T39** — exactamente 8/8 assessments válidas/autorizadas + temporal evidence válida -> READY.
- **GP2-T40** — READY contiene nuevo `EpisodicAdmissionContext` y `EpisodicAdmissionSignals` con mapping exacto.
- **GP2-T41** — READY no llama `evaluate_episodic_candidate(...)`.
- **GP2-T42** — mismos inputs producen exactamente la misma projection.
- **GP2-T43** — no se crean archivos, red, persistencia ni side effects.

### Precedencia

- **GP2-T44** — DENIED domina missing assessment HOLD independientemente del orden.
- **GP2-T45** — provenance INVALID domina duplicate HOLD.
- **GP2-T46** — temporal DENIED domina missing assessment HOLD.
- **GP2-T47** — múltiples findings del mismo nivel usan kind order canónico, no list order.

G3 puede añadir tests constructores razonables, pero no puede reducir estos escenarios sin nueva autorización.

---

## 22. FULL 4R obligatorio

### Risk

Debe demostrar:

- ausencia de fallback trust-sensitive desde `candidate.control`;
- ausencia de last-write-wins;
- ausencia de authority expansion;
- temporal evidence gobernada y exact permission binding;
- `READY != ELIGIBLE`;
- residual de identidad/integridad criptográfica explícito.

### Readability

Debe demostrar:

- una única responsabilidad: proyectar inputs gobernados;
- mapping cerrado y visible;
- sin `Manager`, universal registry u orchestrator general;
- reason codes legibles.

### Reliability

Debe demostrar:

- deterministic ordering;
- exact cardinality;
- exact type semantics;
- UTC estricto;
- mismos inputs -> misma projection;
- candidate no mutado.

### Resilience

Debe demostrar:

- missing evidence -> HOLD;
- tampering/binding mismatch -> DENIED;
- ambiguity -> HOLD;
- no default permissivo;
- no side effects.

---

## 23. Bounded Correction

Si G3 presenta findings, el correction budget queda limitado a:

```text
src/malak/memory/governed_input_projection.py
tests/test_governed_input_projection.py
```

Máximo recomendado:

```text
2 bounded correction rounds
```

Si un finding exige cambiar contracts anteriores, Security, Kernel o Admission:

```text
STOP → ESCALATE
```

Cada candidate nuevo invalida la evidencia candidate-bound anterior y exige revalidación completa.

---

## 24. Validación independiente requerida

Candidate final G3 deberá pasar:

```text
full pytest suite
compileall
git diff --check
exact candidate identity
exact file budget
Ubuntu
Windows
macOS
FULL 4R
```

No basta con una ejecución local.

---

## 25. STOP conditions

Detener G3 inmediatamente si aparece necesidad de:

- modificar cualquier archivo existente;
- modificar `episodic_admission.py`;
- modificar provenance o producer authorization;
- modificar SecurityContext/PDP/PEP;
- generar nuevas PolicyRule runtime;
- llamar `evaluate_episodic_candidate(...)`;
- persistir Memory;
- retrieval;
- Knowledge;
- runtime/Conversation wiring;
- network;
- LLM;
- agents/tools;
- resolver conflictos por latest/highest/priority sin policy aprobada;
- inventar TTL;
- introducir criptografía o afirmar identidad criptográfica inexistente;
- ampliar autoridad;
- tocar Kernel.

---

## 26. Residuales explícitos

G2 no resuelve:

```text
strong cryptographic producer identity
signed assessment content
nonce/replay protection
supersession/conflict resolution
retention policy
persistence
retrieval eligibility
Knowledge promotion
```

En particular:

```text
structurally valid evidence
!= cryptographically signed evidence

READY
!= trusted truth
!= ELIGIBLE
!= persistence authorization
!= authority
```

Estos residuales no bloquean la frontera aislada porque no existe wiring runtime, persistencia ni ejecución externa en este candidate.

---

## 27. Cuatro preguntas obligatorias

```text
1. Blueprint?               PASS
2. Cognitive Constitution?  PASS
3. Governance?              PASS
4. Kernel remains simple?   PASS
```

Razones:

- la responsabilidad permanece en Memory;
- cognition/evidence no crea autoridad;
- Human in Control permanece intacto;
- no hay self-authorization;
- `Kernel delta = 0`.

---

## 28. Rollback

G2 es documental.

Rollback del candidate G3 futuro:

```text
close PR without merge
+ delete implementation branch
```

Como el presupuesto G3 no modifica archivos existentes, el rollback vuelve exactamente al baseline anterior sin migraciones ni cleanup persistente.

---

## 29. Resultado G2

```text
Unit:
Episodic Admission Governed Input Projection Boundary

G2 RESULT:
PASS

Risk:
3 — HIGH

Implementation candidate:
SPECIFIED

Future file budget:
2 NEW files
0 existing files modified

Temporal governance:
DEDICATED AUTHORIZED EVIDENCE

Admission execution:
NOT AUTHORIZED

Persistent Memory:
NOT AUTHORIZED

Sprint 7.12:
NOT AUTHORIZED

RDD Stage 2:
NOT AUTHORIZED
```

La siguiente transición posible, después de merge humano y reconciliación del Vault, es una autorización separada para:

```text
G3 — isolated TDD implementation candidate
```

Nada en este documento autoriza esa transición automáticamente.
