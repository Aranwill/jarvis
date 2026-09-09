---
title: Episodic Admission Assessment Producer Authorization Boundary — G2 Implementation Candidate Specification
status: g2_implementation_candidate_spec_review
authority: owner-approved specification record
as_of_date: 2026-09-09
unit: Episodic Admission Assessment Producer Authorization Boundary
gate: G2
source_baseline: 4953532addef9a5e4c0dd8e9e03531ab7c77ce51
risk_class: 3
vault_reconciliation_status_at_start: resolved
vault_head_at_start: adf60ff908db41ecf80bde7980a590134f68ab10
sync_agent_head_at_start: 71b21e0a192017353075954e06e2b55f5f8e2255
sdd_required: true
tdd_required: true
full_4r_required: true
rdd_stage_1: adopted
rdd_stage_2_authorized: false
implementation_authorized: false
security_control_plane_change_authorized: false
admission_wiring_authorized: false
persistent_memory_authorized: false
retrieval_authorized: false
knowledge_implementation_authorized: false
sprint_7_12_authorized: false
vault_reconciliation_required_before_implementation: true
language: es
---

# Episodic Admission Assessment Producer Authorization Boundary — G2 Implementation Candidate Specification

## 1. Estado de autoridad

El Owner autorizó exclusivamente la materialización de G2 como especificación del candidato de implementación para:

```text
Episodic Admission Assessment Producer Authorization Boundary
```

G2 congela contratos, semántica, bindings, permission scopes, precedencia, escenarios TDD, file budget, FULL 4R y STOP conditions.

G2 no autoriza todavía:

- código productivo;
- tests de implementación;
- cambios a `SecurityContext`;
- cambios a PDP o PEP;
- nuevas `PolicyRule` runtime;
- wiring hacia `episodic_admission.py`;
- Conversation o runtime wiring;
- persistencia, retrieval o Knowledge;
- agentes, tools o red;
- identidad criptográfica, PKI, firmas, nonce o replay protection;
- Sprint 7.12;
- RDD Stage 2;
- merge sin decisión humana.

```text
Specification != Implementation
Authorization evidence != Authority
AUTHORIZED != Admission
```

---

## 2. Baseline exacto y precondiciones

Baseline fuente congelado:

```text
Aranwill/jarvis
main
4953532addef9a5e4c0dd8e9e03531ab7c77ce51
```

Estado cross-repository al iniciar G2:

```text
Malāk main:
4953532addef9a5e4c0dd8e9e03531ab7c77ce51

Project Vault main:
adf60ff908db41ecf80bde7980a590134f68ab10

Vault Sync Agent main:
71b21e0a192017353075954e06e2b55f5f8e2255

post-reconciliation dry-run:
base_commit == head_commit == 4953532a...
changed_files = 0
document_candidates = 0
validation_findings = 0
conclusion = pass
proposal_created = false
```

Precondiciones G2:

```text
G0 PASS
G1 PASS + integrated
Vault reconciliation PASS
Security Control Plane available
Assessment Provenance G3 integrated
```

---

## 3. Método de construcción obligatorio

Esta unidad conserva el método vigente de Malāk:

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

Invariantes metodológicas:

```text
Writer != Reviewer != Validator != Authority
Evidence != Receipt != Validation != Decision != Authority
candidate changes -> prior candidate-bound evidence must be revalidated
```

---

## 4. Problema exacto que resuelve G2

El baseline ya puede demostrar:

```text
AdmissionAssessment
        ↓
validate_assessment_provenance(...)
        ↓
VALID | HOLD | INVALID
```

Pero `VALID` solo demuestra provenance estructural. No demuestra que un principal gobernado tenga permiso para producir una assessment de ese `AssessmentKind` con ese efecto downstream.

G2 congela el candidato mínimo para responder:

```text
¿la assessment structurally valid
puede ser considerada como input gobernado
según una autorización emitida por el Security Control Plane?
```

No responde todavía:

```text
¿debe la assessment modificar EpisodicAdmissionContext/Signals?
¿debe el candidate ser ELIGIBLE?
¿debe persistirse algo?
```

---

## 5. Separaciones obligatorias

```text
ASSESSMENT VALUE
!= STRUCTURAL PROVENANCE
!= PRODUCER REFERENCE
!= PRODUCER SUBJECT
!= SECURITY CONTEXT
!= PERMISSION SCOPE
!= AUTHORIZATION REQUEST
!= AUTHORIZATION DECISION
!= PRODUCER AUTHORIZATION RESULT
!= ADMISSION INPUT
!= ADMISSION DECISION
!= PERSISTENCE AUTHORIZATION
!= AUTHORITY
```

También:

```text
producer_reference != producer_subject_id
SecurityContext.authenticated != cryptographically proven identity
AuthorizationDecision.allowed != trusted assessment truth
AUTHORIZED != ELIGIBLE
```

---

## 6. Decisión G2-D1 — reutilizar contratos existentes de Security

La implementación candidata debe reutilizar directamente:

```text
malak.security.contracts.PermissionScope
malak.security.contracts.AuthorizationRequest
malak.security.contracts.AuthorizationDecision
malak.security.contracts.SecurityContext
```

No debe crear duplicados memory-local equivalentes a esos contratos.

La autoridad sigue perteneciendo al Security Control Plane.

Memory únicamente:

1. deriva el permission scope esperado;
2. recibe evidencia de autorización ya producida;
3. verifica bindings estructurales y temporales;
4. devuelve `AUTHORIZED | HOLD | DENIED`;
5. termina.

```text
Memory validates authorization evidence
Memory does not grant authorization
```

---

## 7. Decisión G2-D2 — wrapper memory-local sin autoridad propia

La implementación candidata puede introducir un bundle inmutable local únicamente para ligar la evidencia de Security al assessment concreto:

```python
@dataclass(frozen=True, slots=True)
class AssessmentProducerAuthorizationEvidence:
    assessment_id: str
    candidate_id: str
    kind: AssessmentKind
    influence_class: AssessmentInfluenceClass
    producer_subject_id: str
    request: AuthorizationRequest
    decision: AuthorizationDecision
```

Semántica:

```text
Evidence bundle
!= permission token
!= cryptographic proof
!= PDP
!= authority
```

El bundle no puede autoautorizar nada. Su contenido debe ser revalidado contra el assessment, la provenance, el permission scope esperado, la request, el SecurityContext y la decision.

`producer_reference` de `AdmissionAssessment` permanece opaca y no se compara ni se reinterpreta como `producer_subject_id`.

---

## 8. Decisión G2-D3 — clases locales de influencia

G2 congela el enum local:

```python
class AssessmentInfluenceClass(StrEnum):
    TRUST_INCREASING = "trust_increasing"
    TRUST_REDUCING = "trust_reducing"
    REVIEW_FORCING = "review_forcing"
    HARD_REJECT = "hard_reject"
    UNCLASSIFIED = "unclassified"
```

Este enum es local a `assessment_producer_authorization.py`.

No constituye una taxonomía universal de trust para todo Malāk.

---

## 9. Decisión G2-D4 — clasificación determinista de influence

La implementación debe derivar la influence class desde `AssessmentKind + value`; nunca debe aceptar una influence class libre como autoridad suficiente.

Matriz cerrada:

| AssessmentKind | Value | Influence |
| --- | --- | --- |
| `SOURCE_SECURITY_STATUS` | `"acceptable"` | `TRUST_INCREASING` |
| `SOURCE_SECURITY_STATUS` | `"unassessed"` | `REVIEW_FORCING` |
| `SOURCE_SECURITY_STATUS` | `"suspect"` | `TRUST_REDUCING` |
| `SOURCE_SECURITY_STATUS` | `"tainted"` | `HARD_REJECT` |
| `SOURCE_SECURITY_STATUS` | `"revoked"` | `HARD_REJECT` |
| `SCOPE_APPLICABLE` | `True` | `TRUST_INCREASING` |
| `SCOPE_APPLICABLE` | `False` | `HARD_REJECT` |
| `POLICY_VIOLATION` | `False` | `TRUST_INCREASING` |
| `POLICY_VIOLATION` | `True` | `HARD_REJECT` |
| `SENSITIVE_REVIEW_REQUIRED` | `False` | `TRUST_INCREASING` |
| `SENSITIVE_REVIEW_REQUIRED` | `True` | `REVIEW_FORCING` |
| `CONTRADICTION_REQUIRES_REVIEW` | `False` | `TRUST_INCREASING` |
| `CONTRADICTION_REQUIRES_REVIEW` | `True` | `REVIEW_FORCING` |
| `SOURCE_AUTHORITY` | canonical string | `UNCLASSIFIED` |
| `CONFIDENCE` | canonical string | `UNCLASSIFIED` |
| `SENSITIVITY` | canonical string | `UNCLASSIFIED` |

Para dimensiones de semántica cerrada, un tipo o valor no reconocido no debe inferirse:

```text
unsupported closed value -> HOLD
```

Para `SOURCE_AUTHORITY`, `CONFIDENCE` y `SENSITIVITY`, G2 conserva `UNCLASSIFIED`: una autorización puede permitir producir esa dimensión, pero no le asigna dirección de trust.

---

## 10. Decisión G2-D5 — PermissionScope canónico

El permission scope esperado debe derivarse de forma determinista:

```text
resource = "memory.episodic_assessment.<assessment_kind>"
action   = "produce.<influence_class>"
```

Ejemplos:

```text
PermissionScope(
    resource="memory.episodic_assessment.source_security_status",
    action="produce.trust_reducing",
)

PermissionScope(
    resource="memory.episodic_assessment.confidence",
    action="produce.unclassified",
)
```

No wildcards.
No prefix matching.
No implicit inheritance.
No role-to-permission inference inside Memory.

La autorización es scoped por:

```text
subject_id + AssessmentKind + influence class
```

El PDP existente continúa siendo quien determina si existe policy aplicable.

---

## 11. Decisión G2-D6 — autorización scoped, binding local por assessment

G2 no exige una `PolicyRule` nueva por `assessment_id` o `candidate_id`.

La autorización de Security puede reutilizarse dentro del scope exacto autorizado mientras el `SecurityContext` siga válido.

El consumo memory-local sí debe ligarse al assessment concreto mediante el bundle:

```text
assessment_id
candidate_id
kind
influence_class
producer_subject_id
request_id
```

Esto permite:

```text
Security authorization scope != per-assessment policy explosion
```

sin perder binding estructural al momento de consumo.

G2 no añade TTL propio. La validez temporal depende del `SecurityContext` y del momento de consumo.

---

## 12. Decisión G2-D7 — validez temporal al momento de consumo

Aunque el PDP haya permitido la request, Memory debe fallar cerrado si al momento de consumo:

```text
evaluated_at < context.issued_at
or
evaluated_at >= context.expires_at
```

Esta verificación no crea una nueva policy de autoridad; replica el lifecycle invariant ya materializado por `SecurityContext` para impedir reutilización de una decision después de expirar el contexto.

No se introduce nonce ni replay protection ficticio.

Residual explícito:

```text
context lifecycle check != cryptographic anti-replay
```

---

## 13. Contratos exactos del candidato

### 13.1 `AssessmentInfluenceClass`

Enum definido en §8.

### 13.2 `AssessmentProducerAuthorizationEvidence`

Contrato definido en §7.

Validaciones constructoras:

- IDs y `producer_subject_id` canónicos, no vacíos y sin whitespace periférico;
- `kind` debe ser `AssessmentKind`;
- `influence_class` debe ser `AssessmentInfluenceClass`;
- `request` debe ser `AuthorizationRequest`;
- `decision` debe ser `AuthorizationDecision`.

### 13.3 `AssessmentProducerAuthorizationOutcome`

```python
class AssessmentProducerAuthorizationOutcome(StrEnum):
    AUTHORIZED = "authorized"
    HOLD = "hold"
    DENIED = "denied"
```

### 13.4 `AssessmentProducerAuthorizationReason`

G2 congela los reason codes:

```text
MISSING_PROVENANCE_DECISION
PROVENANCE_HOLD
PROVENANCE_INVALID
MISSING_AUTHORIZATION_EVIDENCE
ASSESSMENT_ID_MISMATCH
CANDIDATE_ID_MISMATCH
KIND_MISMATCH
UNSUPPORTED_ASSESSMENT_VALUE
INFLUENCE_CLASS_MISMATCH
PRODUCER_SUBJECT_MISMATCH
PERMISSION_SCOPE_MISMATCH
DECISION_REQUEST_MISMATCH
CONTEXT_NOT_YET_VALID
CONTEXT_EXPIRED
AUTHORIZATION_DENIED
AUTHORIZED
```

### 13.5 `AssessmentProducerAuthorizationDecision`

```python
@dataclass(frozen=True, slots=True)
class AssessmentProducerAuthorizationDecision:
    assessment_id: str
    candidate_id: str
    kind: AssessmentKind
    outcome: AssessmentProducerAuthorizationOutcome
    reason_code: AssessmentProducerAuthorizationReason
    evaluated_at: datetime
    influence_class: AssessmentInfluenceClass | None = None
    producer_subject_id: str | None = None
    authorization_request_id: str | None = None
    policy_version: str = POLICY_VERSION
```

El decision object es evidencia local de validación; no es una `AuthorizationDecision` de Security y no concede autoridad fuera de esta frontera.

---

## 14. API pública candidata

El módulo candidato debe exponer únicamente lo necesario:

```python
POLICY_VERSION
AssessmentInfluenceClass
AssessmentProducerAuthorizationEvidence
AssessmentProducerAuthorizationOutcome
AssessmentProducerAuthorizationReason
AssessmentProducerAuthorizationDecision
required_permission_for_assessment(...)
validate_assessment_producer_authorization(...)
```

Firma conceptual principal:

```python
def validate_assessment_producer_authorization(
    assessment: AdmissionAssessment,
    provenance_decision: AssessmentProvenanceDecision | None,
    evidence: AssessmentProducerAuthorizationEvidence | None,
    evaluated_at: datetime,
) -> AssessmentProducerAuthorizationDecision:
    ...
```

No recibe PDP.
No recibe PEP.
No genera `AuthorizationRequest`.
No ejecuta policy.
No escribe audit de Security.

Recibe evidencia ya producida y valida su binding.

---

## 15. `required_permission_for_assessment(...)`

La función debe:

1. validar el tipo de assessment;
2. derivar influence class de forma determinista;
3. si el valor cerrado no es reconocido, devolver ausencia de permiso clasificable de forma explícita para que la función principal produzca `HOLD`;
4. construir `PermissionScope` exacto con la convención §10.

No debe consultar registries, archivos, red, LLM ni configuración externa.

---

## 16. Precedencia determinista

La función principal debe evaluar en este orden:

```text
1. provenance decision missing
   -> HOLD / MISSING_PROVENANCE_DECISION

2. provenance outcome HOLD
   -> HOLD / PROVENANCE_HOLD

3. provenance outcome INVALID
   -> DENIED / PROVENANCE_INVALID

4. provenance assessment/candidate/kind mismatch
   -> DENIED / corresponding mismatch

5. closed assessment value unsupported
   -> HOLD / UNSUPPORTED_ASSESSMENT_VALUE

6. authorization evidence missing
   -> HOLD / MISSING_AUTHORIZATION_EVIDENCE

7. evidence assessment/candidate/kind mismatch
   -> DENIED / corresponding mismatch

8. evidence influence != derived influence
   -> DENIED / INFLUENCE_CLASS_MISMATCH

9. evidence producer_subject_id != request.context.subject_id
   -> DENIED / PRODUCER_SUBJECT_MISMATCH

10. request.permission != expected PermissionScope
    -> DENIED / PERMISSION_SCOPE_MISMATCH

11. decision.request_id != request.request_id
    -> DENIED / DECISION_REQUEST_MISMATCH

12. evaluated_at < context.issued_at
    -> DENIED / CONTEXT_NOT_YET_VALID

13. evaluated_at >= context.expires_at
    -> DENIED / CONTEXT_EXPIRED

14. decision.allowed is False
    -> DENIED / AUTHORIZATION_DENIED

15. all checks pass
    -> AUTHORIZED / AUTHORIZED
```

No reason code posterior puede elevar un resultado previamente fail-closed.

---

## 17. Semántica de resultados

```text
AUTHORIZED
= la assessment structurally valid tiene evidencia interna de autorización
  correctamente bound al scope esperado bajo el Security Control Plane actual
```

Pero:

```text
AUTHORIZED
!= authenticated external identity
!= cryptographic producer proof
!= trusted truth
!= admission eligibility
!= admission execution
!= persistence authorization
!= Knowledge promotion
!= authority expansion
```

`HOLD` significa evidencia insuficiente o semántica no clasificable de forma segura.

`DENIED` significa que existe un mismatch, invalidez o una decision Security explícitamente no permitida.

```text
DENIED != EpisodicAdmissionOutcome.REJECT automatically
HOLD != EpisodicAdmissionOutcome.HOLD automatically
```

El wiring posterior sigue fuera de scope.

---

## 18. Asimetría de permisos preservada

Los scopes separados por influence class deben hacer imposible reutilizar una autorización restrictiva para un efecto permisivo.

```text
produce.trust_reducing
!= produce.trust_increasing

produce.review_forcing
!= produce.trust_increasing

produce.hard_reject
!= produce.trust_increasing
```

Ejemplos que deben fallar:

```text
permission for SUSPECT
used for ACCEPTABLE
-> DENIED

permission for review_required=true
used for review_required=false
-> DENIED

permission for policy_violation=true
used for policy_violation=false
-> DENIED
```

---

## 19. Seguridad frente a self-assertion y DoS

G2 preserva simultáneamente:

```text
una fuente no autorizada no puede aumentar trust
```

y:

```text
una fuente no autorizada tampoco puede imponer hard-reject/review efectivo
```

Por tanto:

```text
producer_role="security_trust_state"
value="revoked"
structural provenance VALID
but no valid authorization evidence
-> HOLD or DENIED at producer authorization boundary
-> no direct REJECT downstream
```

Esto evita convertir fail-closed en un vector trivial de DoS.

---

## 20. Human confirmation

G2 no implementa ni revalida `HumanConfirmationEvidence` dentro de Memory.

Si una policy Security requiere confirmación humana, el PDP debe resolverla antes de producir una `AuthorizationDecision(allowed=True, ...)`.

Memory solo valida:

```text
request binding
decision binding
permission scope
subject binding
context lifetime
allowed flag
```

No duplica el `HumanConfirmationVerifier`.

---

## 21. Límite de identidad

La implementación candidata es válida únicamente como frontera interna bajo el Security Control Plane actual.

```text
SecurityContext.subject_id
+ authenticated=True
+ allowed AuthorizationDecision
```

no constituye por sí solo identidad criptográfica fuerte.

La unidad no puede presentarse como suficiente para:

- producers externos;
- agentes remotos;
- tools externas no confiables;
- mensajes de red hostiles;
- escenarios que requieran anti-replay criptográfico.

Eso requerirá gates futuros de identidad/provenance fuerte.

---

## 22. File/change budget del G3 futuro

Si el Owner autoriza posteriormente G3, el presupuesto máximo inicial será:

```text
NEW
src/malak/memory/assessment_producer_authorization.py

tests/test_assessment_producer_authorization.py

MODIFY existing production files = 0
MODIFY existing test files       = 0
Kernel changes                   = 0
SecurityContext changes          = 0
PDP changes                      = 0
PEP changes                      = 0
Admission wiring                 = 0
Persistence                      = 0
Retrieval                        = 0
Knowledge                        = 0
External dependencies            = 0
```

Si TDD demuestra que ese presupuesto es insuficiente:

```text
STOP -> Owner review
```

No ampliar scope silenciosamente.

---

## 23. Escenarios TDD obligatorios para G3 futuro

G2 congela como mínimo los siguientes escenarios:

1. provenance missing -> `HOLD`;
2. provenance `HOLD` -> authorization `HOLD`;
3. provenance `INVALID` -> authorization `DENIED`;
4. provenance para otro assessment -> `DENIED`;
5. provenance para otro candidate -> `DENIED`;
6. provenance para otro kind -> `DENIED`;
7. closed value desconocido -> `HOLD`;
8. open string kind -> `UNCLASSIFIED` determinista;
9. evidence missing -> `HOLD`;
10. evidence para otro assessment -> `DENIED`;
11. evidence para otro candidate -> `DENIED`;
12. evidence para otro kind -> `DENIED`;
13. caller-supplied influence mismatch -> `DENIED`;
14. `producer_subject_id` distinto de `request.context.subject_id` -> `DENIED`;
15. wrong `PermissionScope.resource` -> `DENIED`;
16. wrong `PermissionScope.action` -> `DENIED`;
17. `AuthorizationDecision.request_id` mismatch -> `DENIED`;
18. context not yet valid -> `DENIED`;
19. context expired exactly at `evaluated_at` -> `DENIED`;
20. `allowed=False` remains `DENIED` regardless of reason text;
21. exact allowed scope + valid bindings -> `AUTHORIZED`;
22. permission `trust_reducing` cannot authorize `trust_increasing`;
23. permission `hard_reject` cannot authorize clearing/permissive value;
24. una assessment no autorizada `REVOKED` no produce admission reject;
25. `producer_reference` is never interpreted as subject id;
26. same inputs -> same result;
27. inputs remain immutable;
28. no filesystem writes;
29. no network calls;
30. no LLM calls;
31. no PDP/PEP call from the validator;
32. `AUTHORIZED` object cannot self-promote to `ELIGIBLE`, persistence or Knowledge.

TDD debe materializar primero tests que fallen por ausencia del módulo/contrato y después la implementación mínima necesaria.

---

## 24. FULL 4R plan para G3 futuro

### Risk

Revisar obligatoriamente:

- self-asserted producer authority;
- permission scope confusion;
- subject/request/decision mismatch;
- stale SecurityContext reuse;
- restrictive-to-permissive privilege escalation;
- hard-reject DoS por input no autorizado;
- falsa equivalencia entre auth interna e identidad criptográfica;
- replay semántico más allá del scope admitido;
- bypass de provenance;
- authority inversion Memory -> Security.

### Readability

La implementación debe conservar una sola responsabilidad:

```text
validate whether Security authorization evidence
is correctly bound to one structurally valid assessment
```

No `Manager`, no registry global, no orchestrator.

### Reliability

Exigir:

- dataclasses inmutables;
- enums cerrados;
- UTC estricto para `evaluated_at`;
- permission derivation determinista;
- precedence estable;
- exact equality en IDs, kind, subject, request y permission;
- fail-closed por ausencia o mismatch.

### Resilience

Exigir:

- denied nunca reinterpretado;
- scope ambiguo nunca autorizado;
- context expirado nunca autorizado;
- unsupported value nunca inferido;
- no side effects;
- no authority expansion ante error.

---

## 25. Bounded Correction

Si G3 produce findings, cada correction round deberá declarar:

```text
finding
allowed files
forbidden files
change budget
validation to rerun
candidate SHA after correction
```

Budget inicial:

```text
allowed:
- src/malak/memory/assessment_producer_authorization.py
- tests/test_assessment_producer_authorization.py

forbidden:
- Kernel
- SecurityContext
- PDP/PEP
- episodic_admission.py
- runtime/Conversation
- persistence/retrieval/Knowledge
```

Si el finding no puede resolverse dentro de ese budget:

```text
STOP -> ESCALATE TO OWNER
```

---

## 26. Independent Validation y candidate-bound evidence

La evidencia de G3 futuro deberá identificar exactamente:

```text
baseline SHA
candidate SHA
changed file set
TDD RED evidence
TDD GREEN evidence
full test suite result
compileall result
git diff --check result
Ubuntu result
Windows result
macOS result
FULL 4R result
```

Si el candidate SHA cambia después de la validación:

```text
previous evidence != evidence for new candidate
```

Se deberá revalidar proporcionalmente.

---

## 27. STOP conditions

Detener y volver al Owner si G3 requiere:

- modificar Kernel;
- modificar Blueprint, Constitutions o AQG;
- modificar `SecurityContext`;
- modificar PDP o PEP;
- añadir `PolicyRule` productiva;
- crear un segundo authority engine dentro de Memory;
- reinterpretar `producer_reference` como identidad;
- asumir identidad criptográfica inexistente;
- wiring directo a `episodic_admission.py`;
- persistencia, retrieval o Knowledge;
- agents/tools/red;
- dependency externa;
- registry persistente;
- wildcard permissions;
- taxonomía universal de trust;
- nonce/replay protection ficticio;
- Sprint 7.12;
- RDD Stage 2.

---

## 28. Rollback del candidato futuro

Como G3 futuro solo puede añadir dos archivos nuevos y no modificar contratos existentes, rollback conceptual:

```text
remove candidate branch / close PR without merge
```

Si se integrara y luego requiriera reversión humana:

```text
revert isolated merge commit
```

No debe existir migración de datos, schema, state externo ni side effect que dificulte rollback.

---

## 29. No wiring en esta unidad

Incluso después de una futura implementación G3 exitosa:

```text
AssessmentProducerAuthorizationOutcome.AUTHORIZED
```

no autoriza automáticamente:

```text
EpisodicAdmissionContext mutation
EpisodicAdmissionSignals mutation
evaluate_episodic_candidate(...)
ELIGIBLE
storage
retrieval
Knowledge promotion
```

La conexión:

```text
Assessment Provenance
        ↓
Producer Authorization
        ↓
Episodic Admission
```

seguirá requiriendo un gate SDD posterior separado.

---

## 30. Compatibilidad con arquitectura y gobernanza

```text
Blueprint compliance: PASS
Cognitive Constitution: PASS
Governance Constitution: PASS
Kernel simplicity: PASS
Human in Control: PASS
Zero Trust: PASS
Defense in Depth: PASS
Runtime Independence: PASS
```

Dirección de autoridad preservada:

```text
Security Control Plane
        ↓
AuthorizationRequest / AuthorizationDecision
        ↓
Memory binding validation
        ↓
possible later governed consumption
```

Nunca:

```text
Memory assessment
        ↑
creates or overrides Security authority
```

---

## 31. Resultado G2

```text
G2 RESULT: PASS
unit: Episodic Admission Assessment Producer Authorization Boundary
risk class: 3 — HIGH
candidate specification: frozen for human review
future implementation budget: 2 new files
existing production modifications: 0
security modifications: 0
kernel modifications: 0
admission wiring: 0
persistent memory: 0
retrieval: 0
knowledge: 0
implementation authorized: false
sprint 7.12 authorized: false
rdd stage 2 authorized: false
vault reconciliation required before implementation: true
```

Próximo paso permitido únicamente mediante nueva autorización explícita del Owner:

```text
G3 — Assessment Producer Authorization isolated TDD implementation candidate
```
