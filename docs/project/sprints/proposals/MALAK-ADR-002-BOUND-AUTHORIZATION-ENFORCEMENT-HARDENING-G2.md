---
title: Malāk ADR-002 — Bound Authorization Enforcement Hardening G2 Candidate
status: g2_hardening_candidate
authority: non_normative_candidate
language: es
as_of_date: 2026-09-15
unit: Bound Authorization Enforcement Foundation
gate: G2
source_baseline: 46dde74592ffc336104f4309cdd8a966b518fc53
risk_class: 3
sdd_required: true
tdd_required_for_future_implementation: true
full_4r_required: true
rdd_stage_1: adopted
rdd_stage_2_authorized: false
adr_002_amendment_authorized: false
implementation_authorized: false
security_control_plane_change_authorized: false
persistence_authorization_authorized: false
persistent_memory_authorized: false
protected_durable_write_authorized: false
durable_reliance_runtime_authorized: false
conversation_g2b_authorized: false
sprint_7_12_authorized: false
related:
  - docs/architecture/adr/ADR-002-policy-enforcement-boundary.md
  - docs/architecture/adr/ADR-006-protected-durable-reliance-preconditions.md
  - docs/governance/governance_constitution.md
  - docs/architecture/blueprint.md
  - docs/architecture/architecture_quality_gates.md
  - SECURITY.md
  - docs/development/malak_construction_protocol.md
  - src/malak/security/contracts.py
  - src/malak/security/pdp.py
  - src/malak/security/pep.py
  - src/malak/security/audit.py
---

# Malāk ADR-002 — Bound Authorization Enforcement Hardening G2 Candidate

## 1. Estado de autoridad

Esta unidad congela exclusivamente un candidato G2 de endurecimiento para la frontera
PDP → PEP definida por ADR-002.

No modifica todavía ADR-002 ni autoriza implementación.

```text
candidate wording
!= ADR amendment
!= accepted architecture
!= implementation authorization
!= Persistence Authorization
!= Persistent Memory
```

El objetivo es eliminar ambigüedades antes de introducir cualquier side effect durable,
sin cambiar la forma arquitectónica vigente:

```text
caller
  ↓ AuthorizationRequest
PEP
  ↓ trusted PDP
AuthorizationDecision
  ↓ validation / enforcement
ProtectedOperation
```

Se preservan:

```text
caller cannot supply AuthorizationDecision to PEP
PDP decides
PEP enforces
Decision != Execution
Security != Memory lifecycle ownership
Kernel remains outside business/security execution logic
```

---

## 2. Baseline exacto

Fuente autoritativa de esta revisión:

```text
Aranwill/jarvis
main@46dde74592ffc336104f4309cdd8a966b518fc53
```

Baseline observado:

```text
AuthorizationRequest
  context
  permission
  request_id
  created_at

AuthorizationDecision
  request_id
  allowed
  reason

HumanConfirmationEvidence
  confirmation_id
  original_request_id
  new_request_id
  subject_id
  permission
  confirmed_by
  confirmed_at

ProtectedOperation
  execute()

StrictPolicyEnforcementPoint
  request -> PDP -> decision -> audit -> execute
```

ADR-002 ya impide que una decisión aportada por el caller sea tratada como autoridad.
También conserva fail-closed ante fallo del PDP, decisión inválida, request mismatch o
denegación.

---

## 3. Problema exacto

La asociación vigente demuestra:

```text
AuthorizationDecision.request_id
==
AuthorizationRequest.request_id
```

pero no demuestra de forma genérica:

```text
AuthorizationRequest
is bound to
THIS exact protected operation subject
```

Por tanto:

```text
permission class match
!= exact operation subject binding

request_id match
!= material subject binding

allowed=True
!= bearer token for arbitrary object of the same permission class
```

Este residual fue aceptable mientras las operaciones reales protegidas no incluían
un durable write materialmente sensible. Deja de ser aceptable como base para una
futura Persistence Authorization / Protected Durable Write.

---

## 4. Threat model mínimo

Este hardening debe impedir, como mínimo:

```text
T1  authorize operation subject A -> execute subject B
T2  authorize intent A -> execute intent B
T3  present a decision with same request_id but different/missing subject binding
T4  confirm operation A -> reuse confirmation for bound operation B
T5  audit only permission class while losing exact operation subject identity
T6  treat equality of an opaque binding as trust/authenticity
T7  treat an allowed decision as a reusable permission token
T8  claim replay protection where only in-process request correlation exists
T9  allow domain caller to inject an arbitrary binding unrelated to operation payload
```

No intenta resolver todavía:

```text
durable anti-replay across crashes
idempotent durable storage
partial-failure recovery
retention/disclosure/consent policy
Persistent Memory lifecycle
Durable Reliance runtime
```

---

## 5. Decisión candidata D1 — operation binding genérico y opaco

Se propone un contrato Security-domain mínimo equivalente a:

```python
@dataclass(frozen=True, slots=True)
class AuthorizationOperationBinding:
    namespace: str
    binding_version: str
    digest_algorithm: str
    digest_hex: str
```

Semántica:

```text
AuthorizationOperationBinding
!= permission
!= trust
!= authenticity
!= provenance
!= semantic truth
!= authority
```

`namespace` identifica el dominio/tipo de sujeto protegido.

`binding_version` identifica la especificación que determinó qué material entra en el
binding.

`digest_algorithm` y `digest_hex` identifican de forma determinista el sujeto material
según esa specification.

Security trata el binding como opaco. No interpreta Memory candidates, Persistence
Intent, Conversation, Knowledge ni ningún tipo de dominio.

---

## 6. Reglas de canonicalidad del binding

El contrato deberá exigir:

```text
namespace        canonical non-empty text
binding_version  canonical non-empty text
digest_algorithm canonical non-empty text
digest_hex       non-empty lowercase hexadecimal
```

G2 no congela un algoritmo universal para todo Malāk.

```text
algorithm identifier
!= algorithm policy
```

Cada dominio protegido deberá definir de forma independiente:

```text
what exact material is bound
canonicalization/version rules
allowed digest algorithm
how the protected operation derives/recomputes its binding
```

Una futura operación episódica puede utilizar una derivación compatible con sus
contratos de Content Identity, pero Security no depende de esos tipos.

---

## 7. Decisión candidata D2 — AuthorizationRequest bound

`AuthorizationRequest` podrá transportar:

```python
operation_binding: AuthorizationOperationBinding | None = None
```

Interpretación:

```text
None
= legacy/unbound operation semantics only

binding present
= authorization request refers to one exact protected-operation subject
```

El binding forma parte material de la request sobre la que decide el PDP.

No puede agregarse después de la decisión ni vivir solamente en un wrapper de Memory.

```text
Memory wrapper around an unbound AuthorizationRequest
!= bound operational authorization
```

---

## 8. Decisión candidata D3 — AuthorizationDecision conserva binding

Para una request bound, la decisión candidata deberá conservar el mismo binding:

```python
AuthorizationDecision
    request_id
    allowed
    reason
    operation_binding: AuthorizationOperationBinding | None
```

Regla:

```text
decision.operation_binding
==
request.operation_binding
```

Esto no convierte `AuthorizationDecision` en un bearer token.

El PEP sigue consultando directamente al PDP sobre la request concreta y nunca acepta
una decisión aportada por el caller.

Propósito del campo:

- hacer explícita la materia exacta sobre la que el PDP decidió;
- detectar PDP defectuoso/incongruente;
- conservar evidencia auditable;
- impedir que `request_id` sea la única asociación material.

---

## 9. Decisión candidata D4 — PDP copia, no fabrica, el binding

El PDP no calcula ni interpreta el operation binding.

Cuando emite una `AuthorizationDecision`, debe copiar exactamente:

```text
request.operation_binding
→ decision.operation_binding
```

Para toda salida:

```text
ALLOW
DENY
REQUIRE_HUMAN_CONFIRMATION resolved as allow/deny
```

el binding de la decision debe corresponder a la request evaluada.

```text
PDP policy may decide permission class
but must preserve exact request subject binding
```

La policy vigente puede continuar siendo:

```text
subject_id + PermissionScope -> effect
```

Este hardening no obliga a que cada `PolicyRule` enumere cada objeto concreto.

---

## 10. Decisión candidata D5 — protected operation owns its binding

Una operación protegida bound debe exponer su binding desde el propio objeto que
contiene/posee el material a ejecutar.

Conceptualmente:

```python
class BoundProtectedOperation(Protocol[ResultT]):
    @property
    def authorization_binding(self) -> AuthorizationOperationBinding:
        ...

    def execute(self) -> ResultT:
        ...
```

Regla crítica:

```text
caller-supplied binding beside the operation
!= sufficient
```

El operation binding deberá ser derivado del estado material inmutable que la
operación realmente utilizará o recomputado desde él según la specification del
dominio.

No es válido:

```text
operation(payload=B, binding_for=A)
```

solo porque el caller suministre ambos valores.

La specification de cada operación bound deberá definir cómo se demuestra:

```text
operation.authorization_binding
corresponds to
operation exact material
```

---

## 11. Decisión candidata D6 — PEP exact binding enforcement

Antes de ejecutar una operación bound, el PEP deberá preservar esta matriz:

```text
request binding | operation binding | result
----------------+-------------------+-----------------------------
None            | None              | legacy path may continue
present         | None              | BLOCK
None            | present           | BLOCK
A               | B, A != B         | BLOCK
A               | A                 | continue to PDP/decision gate
```

Después de consultar al PDP:

```text
decision.request_id != request.request_id
→ BLOCK

decision.operation_binding != request.operation_binding
→ BLOCK

decision.allowed is False
→ BLOCK

all bindings coherent + allowed
→ execute exactly once for that PEP invocation
```

El check request↔operation debe ocurrir antes de cualquier side effect.

El check request↔decision debe ocurrir después de obtener la decisión del PDP y antes
del side effect.

---

## 12. Decisión candidata D7 — HumanConfirmationEvidence bound

Una confirmación humana para una operación bound no puede quedar ligada solamente a:

```text
subject + permission + request IDs
```

Debe conservar además:

```python
operation_binding: AuthorizationOperationBinding | None
```

La validación PDP deberá exigir:

```text
confirmation.operation_binding
==
request.operation_binding
```

Interpretaciones prohibidas:

```text
same subject
+ same permission
+ matching new_request_id
!= permission to substitute another bound object
```

La confirmación sigue siendo evidencia:

```text
HumanConfirmationEvidence
!= AuthorizationDecision
!= permanent permission
!= reusable consent token
```

El verifier externo/humano continúa siendo responsable de la autenticidad de la
confirmación. Este hardening congela únicamente el binding estructural necesario para
que una confirmación válida no pueda aplicarse a otro operation subject.

---

## 13. Decisión candidata D8 — temporal coherence de AuthorizationRequest

G2 congela la propiedad:

```text
context.issued_at
<= request.created_at
< context.expires_at
```

Una request que declara haber sido creada fuera del lifecycle del contexto que usa es
incoherente y no debe poder convertirse en autoridad válida.

La implementación exacta de esta comprobación puede ubicarse en constructor/PDP según
la revisión de compatibilidad de G3, pero la propiedad es obligatoria.

Separación:

```text
request temporal coherence
!= durable anti-replay
```

El PDP continuará validando además que el `SecurityContext` esté vigente al momento de
la decisión.

---

## 14. Decisión candidata D9 — audit exacto del binding

`AuthorizationAuditRecord` deberá poder preservar:

```python
operation_binding: AuthorizationOperationBinding | None
```

Para un fallo de coherencia bound, el audit deberá registrar el binding de la request
y, cuando resulte seguro y posible sin romper el contrato de auditoría, evidencia
suficiente del binding presentado por la operación.

No se exige duplicar payload ni contenido sensible dentro del audit.

```text
exact binding metadata
!= copy of protected payload
```

Reason codes mínimos candidatos:

```text
request_operation_binding_presence_mismatch
request_operation_binding_mismatch
decision_operation_binding_mismatch
```

El outcome puede reutilizar `ENFORCEMENT_FAILED` si no se demuestra necesidad de una
nueva taxonomía de outcomes.

---

## 15. Replay — semántica congelada y límite explícito

ADR-002 ya establece que el PEP consulta al PDP dentro de cada invocación y no acepta
una decision externa.

Este hardening congela:

```text
AuthorizationDecision.allowed
!= reusable permission token
```

Y para futuras operaciones durables:

```text
same authorization request
must not be treated as sufficient proof
for unlimited repeated durable side effects
```

Pero G2A no fingirá durable anti-replay mediante un cache en RAM.

```text
in-memory seen-request set
!= crash-safe anti-replay

request_id uniqueness assumption
!= replay protection
```

El cierre durable de replay deberá coordinarse posteriormente con:

```text
idempotency key / write identity
partial-failure semantics
commit acknowledgement semantics
recovery after crash/restart
```

Por tanto:

```text
G2A exact binding hardening
!= G2C durable replay closure
```

---

## 16. Relación con Persistence Readiness

Una futura `EpisodicPersistenceReadinessBoundary` podrá producir únicamente evidencia
de dominio:

```text
READY | HOLD | DENIED
```

Nunca `AUTHORIZED`.

Cuando `READY`, una futura composición podrá construir un `AuthorizationRequest`
bound al exact persistence subject/intent.

```text
Memory READY
→ may request Governance/Security authorization

Memory READY
!= operational permission
```

La futura operación de write deberá exponer exactamente el mismo operation binding
que la request/decision autorizadas.

---

## 17. Relación con Persisted Payload Identity

Este candidate no afirma:

```text
candidate content identity
== persisted payload identity
```

La futura operación durable deberá definir la relación exacta entre:

```text
authorized semantic subject/intent
        ↓ governed deterministic transformation
actual durable payload
```

Ese binding permanece bloqueante antes de Protected Durable Write.

---

## 18. Quarantine y forensic retention

No se incorporan a esta unidad.

```text
normal episodic persistence
!= forensic retention
!= quarantine retention
```

Un flujo futuro de quarantine puede usar la misma infraestructura genérica de exact
operation binding, pero requerirá otro `PermissionScope`, purpose y policy.

```text
retention/quarantine authorization
!= later reliance permission
```

---

## 19. Compatibilidad con ADR-002

Forma preservada:

```text
PEP asks trusted PDP
caller cannot supply decision
request/decision validated before execution
fail closed on decision failure/incoherence
operation executes once per successful PEP invocation
Kernel remains unchanged
```

Hardening candidato:

```text
request_id binding
+
exact operation subject binding
+
human confirmation exact subject binding
+
audit binding
```

Por tanto, la disposición G2 es:

```text
preferred normative path:
AMEND ADR-002

new ADR:
NOT REQUIRED unless review demonstrates a materially new architecture
```

La enmienda deberá preservar explícitamente que replay durable e idempotency siguen
fuera de ADR-002 hasta el gate operativo correspondiente.

---

## 20. Candidate API surface

Si un gate posterior autoriza implementación, la API candidata puede requerir:

```text
malak.security.contracts.AuthorizationOperationBinding
AuthorizationRequest.operation_binding
AuthorizationDecision.operation_binding
HumanConfirmationEvidence.operation_binding

malak.security.pep.BoundProtectedOperation

AuthorizationAuditRecord.operation_binding
```

La forma exacta entre `ProtectedOperation` y `BoundProtectedOperation` deberá elegirse
en G3/TDD de manera que preserve compatibilidad y no introduzca duck-typing ambiguo.

No se congela todavía una implementación basada en `getattr(...)`.

---

## 21. Precedencia de enforcement candidata

Orden requerido para una futura implementación:

```text
1. validate AuthorizationRequest type
2. validate request/operation binding presence symmetry
3. validate request/operation binding equality
4. call trusted PDP with exact request
5. validate AuthorizationDecision type
6. validate decision.request_id == request.request_id
7. validate decision.operation_binding == request.operation_binding
8. block denied decision
9. write ALLOWED audit bound to exact operation subject
10. execute protected operation exactly once for this invocation
11. on operation failure, preserve OPERATION_FAILED audit semantics
```

Ante binding mismatch:

```text
no PDP-derived allow may bypass it
no protected operation executes
security audit is attempted
fail closed if required audit cannot be written
```

---

## 22. Escenarios TDD obligatorios futuros

### Contratos

```text
C1  canonical bound contract accepted
C2  empty namespace/version/algorithm/digest rejected
C3  non-hex / uppercase digest rejected if lowercase canonical form is frozen
C4  unbound legacy request remains constructible
C5  bound request preserves exact immutable binding
C6  decision preserves copied binding
C7  confirmation preserves exact binding
C8  request.created_at before context.issued_at rejected/denied
C9  request.created_at at/after context.expires_at rejected/denied
```

### PDP

```text
P1  ALLOW decision copies request binding exactly
P2  DENY decision copies request binding exactly
P3  human-confirmed ALLOW copies exact request binding
P4  confirmation binding mismatch -> DENY
P5  bound confirmation cannot authorize different operation subject
```

### PEP

```text
E1  bound request + same bound operation + allowed decision -> execute once
E2  bound request + unbound operation -> block, zero operation calls
E3  unbound request + bound operation -> block, zero operation calls
E4  A request + B operation -> block, zero operation calls
E5  A request + PDP decision B -> block, zero operation calls
E6  same request_id + mismatched binding -> block
E7  caller still cannot supply AuthorizationDecision
E8  PDP failure -> block
E9  denied decision -> block
E10 audit failure before operation -> block
E11 operation failure -> no automatic retry
E12 legacy unbound path preserves existing semantics
```

### Audit

```text
A1  allowed bound operation records exact binding
A2  denied bound operation records exact binding
A3  binding mismatch records enforcement failure without payload disclosure
A4  operation failure preserves exact binding evidence
```

---

## 23. File budget futuro candidato

Este documento no autoriza implementación.

Si un gate humano posterior la autoriza, el file budget inicial queda limitado a:

```text
MOD  src/malak/security/contracts.py
MOD  src/malak/security/pdp.py
MOD  src/malak/security/pep.py
MOD  src/malak/security/audit.py
MOD  src/malak/security/__init__.py

MOD  tests/test_authorization_contracts.py
MOD  tests/test_policy_decision_point.py
MOD  tests/test_policy_enforcement_point.py
MOD  tests/test_authorization_audit.py
```

Fuera de scope:

```text
src/malak/kernel/**
Conversation
Planner
CLI
runtime/model adapters
src/malak/memory/**
storage/database/filesystem
external derived record
external reconciliation process
Persistent Memory
Durable Reliance runtime
```

Si la comprobación temporal de request causa cambios transversales fuera de este
budget, debe producir STOP y dividirse en un gate separado en lugar de ampliar el
scope silenciosamente.

---

## 24. STOP conditions

Detener antes de implementación si aparece cualquiera de estas condiciones:

```text
S1  exact binding exige acoplar Security a tipos de Memory
S2  caller puede proporcionar una AuthorizationDecision al PEP
S3  operation binding puede suministrarse separadamente del protected operation
S4  confirmation puede aplicarse a otro bound operation subject
S5  legacy compatibility requiere bypass silencioso para bound operations
S6  replay durable se declara resuelto solo con estado en memoria
S7  audit exige copiar payload sensible
S8  Kernel adquiere authorization/enforcement responsibility
S9  file budget crece materialmente sin nuevo gate
S10 current baseline cambia materialmente antes de candidate implementation
```

---

## 25. Malāk Alignment Matrix

| Source | Authority class | Invariant / intent | Disposition | Candidate effect | Deferred / rejected effect |
| --- | --- | --- | --- | --- | --- |
| Governance Constitution | constitutional | seguridad por defecto, mínimo privilegio, separación, auditabilidad | ADOPT | exact bound authorization remains governed | no Memory authority |
| Blueprint | architecture master | Governance First, Security by Design, Kernel minimal | ADOPT | generic Security boundary only | no Kernel delta |
| ADR-002 | accepted ADR | PDP decides, PEP enforces, caller cannot supply decision | ADAPT | strengthen request/decision/operation association | no architecture replacement |
| ADR-006 | accepted ADR | exact persistence subject binding before durable write | ADOPT | G2A becomes prerequisite for future persistence | no durable write authorization |
| SECURITY.md | protected requirements | access != persist/reuse permission; contextual identity/lifecycle | ADOPT | exact operation subject + temporal coherence | no Persistent Memory |
| Existing Security contracts | implemented baseline | request/decision/context/confirmation public contracts | ADAPT | additive optional binding | no parallel authorization system |
| Existing PDP | implemented baseline | policy decision over exact request | ADAPT | preserve/copy binding, confirmation binding | no object-specific policy explosion |
| Existing PEP | implemented baseline | direct PDP consultation + fail-closed enforcement | ADAPT | exact operation binding enforcement | no caller decision input |
| Existing audit | implemented baseline | important authorization actions auditable | ADAPT | preserve exact binding metadata | no payload duplication |
| Memory episodic chain | implemented domain baseline | content identity/readiness are evidence, not authority | OBSERVE | future consumer of generic bound auth | no Memory changes in G2A |

```text
alignment evidence != authority
candidate wording != implementation authorization
```

---

## 26. FULL 4R — specification review

### Risk

```text
status: PASS
```

Reviewed:

- operation substitution;
- decision/request subject mismatch;
- human-confirmation subject substitution;
- authorization laundering through wrapper evidence;
- replay overclaim;
- sensitive payload leakage into audit;
- Security↔Memory coupling.

Residual:

- durable anti-replay remains intentionally deferred;
- operation-domain binding derivation must be specified per bound operation.

### Readability

```text
status: PASS
```

Vocabulary frozen:

```text
PermissionScope        = operation class
OperationBinding       = exact protected subject identity
AuthorizationRequest   = request over permission + optional exact subject
AuthorizationDecision  = PDP decision over that exact request
ConfirmationEvidence   = human evidence bound to same request subject
PEP                    = enforcement
ProtectedOperation     = executable effect
```

### Reliability

```text
status: PASS WITH FUTURE TDD
```

Required negative scenarios are frozen in §22.

No implicit fallback from bound to unbound semantics is allowed.

### Resilience

```text
status: PASS AT SPEC LEVEL
```

Binding mismatch blocks before side effect.
PDP failure remains fail-closed.
Audit failure remains fail-closed before operation when applicable.
Operation failure remains non-retrying.
Durable crash/replay semantics remain an explicit later gate.

---

## 27. G2 result

```text
G2 SPEC RESULT: PASS

candidate:
Bound Authorization Enforcement Foundation

blocking specification findings:
0

normative prerequisite:
ADR-002 amendment candidate review + explicit human acceptance

implementation authorization:
false
```

Carry-forward gates:

```text
G2A implementation
  BLOCKED pending ADR-002 hardening acceptance + owner authorization

G2B Episodic Persistence Readiness
  HOLD until G2A integration and revalidation

G2C Protected Durable Write
  STOP

Persistent Memory
  NOT AUTHORIZED

Durable Reliance runtime
  NOT AUTHORIZED
```

---

## 28. Non-negotiable separations

```text
PermissionScope
!= exact operation subject

OperationBinding
!= trust
!= authenticity
!= authority

request_id match
!= material binding

AuthorizationDecision.allowed
!= bearer token
!= durable replay permission

HumanConfirmationEvidence
!= AuthorizationDecision
!= permanent consent

Memory READY
!= operational authorization

Security authorization
!= Memory lifecycle semantics

exact operation authorization
!= durable write success

Stored
!= trusted
!= Durable Reliance
```
