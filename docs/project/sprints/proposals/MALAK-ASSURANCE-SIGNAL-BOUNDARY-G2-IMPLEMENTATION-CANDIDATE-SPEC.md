---
title: Malāk Assurance Signal Boundary — G2 Implementation Candidate Spec
status: scope_frozen_candidate
authority: owner_authorized_specification_gate
language: es
as_of_date: 2026-09-11
source_baseline: c979f481e2e5353c8953e41e56e9218c7b1d4c6f
spec_gate_authorized: true
implementation_authorized: false
g2_signal_boundary_authorized: false
g2b_conversation_integration_authorized: false
sprint_7_12_authorized: false
rdd_stage_2_authorized: false
candidate_content_identity_g2_authorized: false
persistence_authorization_authorized: false
related:
  - docs/architecture/adr/ADR-005-evidence-bound-final-response-transition.md
  - docs/architecture/blueprint.md
  - docs/governance/cognitive_constitution.md
  - docs/governance/governance_constitution.md
  - docs/development/engineering_method.md
  - docs/development/construction_protocol.md
  - docs/project/sprints/proposals/MALAK-PROGRESSIVE-COGNITIVE-ASSURANCE-RUNTIME-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-PROGRESSIVE-COGNITIVE-ASSURANCE-RUNTIME-G2A-IMPLEMENTATION-CANDIDATE-SPEC.md
  - docs/project/sprints/proposals/MALAK-ASSURANCE-SIGNAL-AUTHORITY-G0-G1-DESIGN.md
---

# Malāk Assurance Signal Boundary — G2 Implementation Candidate Spec

## 1. Estado de autoridad

El Owner autorizó únicamente el gate de especificación de:

```text
G2 — Assurance Signal Authority & Projection Foundation
```

Esta autorización congela diseño, invariantes, alcance y criterios de validación.
No autoriza código productivo ni tests de implementación.

```text
G2-SPEC authorized
!= G2 implementation authorized
!= G2B authorized
!= Sprint 7.12 authorized
!= RDD Stage 2 authorized
```

Este documento no modifica Blueprint, Cognitive Constitution, Governance Constitution,
ADR-005, Security Control Plane ni contratos públicos existentes.

---

## 2. Baseline y necesidad comprobada

Baseline exacto:

```text
Aranwill/jarvis
main@c979f481e2e5353c8953e41e56e9218c7b1d4c6f
```

G2A ya materializa:

```text
ProtectedResponseCandidate
        +
ProtectedFinalizationInput
        ↓
evaluate_protected_finalization(...)
        ↓
ACCEPT | ABSTAIN | BLOCK
```

pero consume cinco signals ya resueltos:

```text
applicability
evidence_required
support_sufficient
contradiction_unresolved
policy_violation
```

El baseline todavía no demuestra de forma gobernada:

```text
who produced each signal?
what exact signal/value may that producer assert?
which request/session/candidate is it bound to?
is producer authorization valid for that scope and time?
are all required signals present exactly once?
are signal semantics compatible with the projection policy?
```

Por tanto:

```text
G2A exists
+
no authorized signal projection boundary
=
G2B remains blocked
```

Resultado de admisión:

```text
Assurance Signal Boundary G2: ADOPT
risk class: 3 — HIGH
implementation authorized: false
```

---

## 3. Objetivo verificable

Una futura implementación separadamente autorizada deberá aceptar observations explícitas
y producir un `ProtectedFinalizationInput` únicamente cuando authority evidence, binding,
cardinalidad, temporalidad y policy compatibility puedan validarse determinísticamente.

```text
ProtectedResponseCandidate
        +
Explicit Signal Observations
        +
Producer Authorization Evidence
        ↓
bounded materialized input validation
        ↓
request/session/candidate binding
        ↓
signal/value compatibility
        ↓
producer authorization binding
        ↓
temporal coherence
        ↓
policy compatibility
        ↓
canonical cross-signal coherence
        ↓
exact completeness
        ↓
READY | HOLD | DENIED
        ↓
ProtectedFinalizationInput only when READY
```

La projection no decide verdad, materialidad ni suficiencia. Solo valida si observations
explícitas pueden alimentar legítimamente el contrato que G2A ya entiende.

---

## 4. Invariantes obligatorios

```text
observation != authority
producer permission != signal truth
signal truth != finalization decision
Security authorization != Cognitive policy disposition
Evidence != Authority
Generation != Finalization
Candidate != Accepted Response
missing signal != favorable signal
```

También:

```text
same-process binding
!= durable content identity
!= cryptographic identity
!= cryptographic integrity
!= replay protection
```

Y:

```text
G2 READY != G2A ACCEPT
G2 DENIED != G2A BLOCK
```

`READY` significa únicamente que el set puede proyectarse válidamente a G2A.

---

## 5. Boundary y archivos candidatos

Ubicación productiva candidata:

```text
src/malak/core/assurance_signal_projection.py
```

Tests candidatos:

```text
tests/test_assurance_signal_projection.py
```

No se crea nueva layer, manager, registry global, service runtime ni authority domain.

No se modifica `src/malak/core/protected_finalization.py` para implementar G2.

---

## 6. Signal kinds y valores cerrados

Kinds permitidos:

```text
APPLICABILITY
EVIDENCE_REQUIRED
SUPPORT_SUFFICIENT
CONTRADICTION_UNRESOLVED
POLICY_VIOLATION
```

Values:

```text
APPLICABILITY
→ NOT_APPLICABLE | REQUIRED | UNRESOLVED

remaining signals
→ bool real only
```

No se admiten `0/1`, strings, `None`, truthy objects ni coerción implícita.

Agregar un sexto signal exige nuevo gate de diseño.

---

## 7. Observation contract candidato

```text
AssuranceSignalObservation
├── signal_kind
├── value
├── request_id
├── session_id
├── producer_subject_id
└── signal_policy_version
```

Reglas:

- inmutable;
- sin defaults favorables;
- IDs canónicos y no vacíos;
- kind mediante enum cerrado;
- value estrictamente compatible con kind;
- signal policy version explícita.

```text
observation exists
!= producer authorized
```

---

## 8. Binding permitido

Candidate Content Identity G2 sigue no autorizado.

El máximo binding permitido para esta foundation es:

```text
same-process
request-bound
session-bound
direct ProtectedResponseCandidate passed to projection
no durable receipt
no replay claim
no cryptographic content identity claim
```

Toda observation debe cumplir:

```text
observation.request_id == candidate.request_id
observation.session_id == candidate.session_id
```

El significado del binding termina con la invocación actual.

Si la solución necesita transportar, persistir, rehidratar o reutilizar observations fuera
de este boundary same-process:

```text
STOP
→ abrir gate independiente de identity/integrity binding
```

No reutilizar silenciosamente Candidate Content Identity episódica.

---

## 9. Producer authorization evidence

G2 reutiliza contratos existentes del Security Control Plane:

```text
SecurityContext
PermissionScope
AuthorizationRequest
AuthorizationDecision
```

No se modifican en esta unidad.

Evidence conceptual:

```text
AssuranceSignalProducerAuthorizationEvidence
├── signal_kind
├── canonical_value
├── request_id
├── session_id
├── producer_subject_id
├── authorization_request
└── authorization_decision
```

Debe demostrar autorización interna para ese **kind + value** concreto y quedar ligada a
la misma request/session de la observation y del candidate.

```text
evidence.request_id == observation.request_id == candidate.request_id
evidence.session_id == observation.session_id == candidate.session_id
```

No basta una autorización genérica como `assurance producer`.

---

## 10. Límite de identidad y provenance de autorización

El Security Control Plane vigente no posee todavía una raíz criptográfica fuerte de
identidad/provenance.

Por tanto esta foundation solo puede afirmar:

```text
governed internal authorization
under the current same-process Security Control Plane
```

No puede afirmar:

```text
cryptographically proven external identity
signed authorization receipt
tamper-proof decision provenance
remote producer authenticity
replay protection
```

La implementación debe exigir:

```text
authorization_request.context.authenticated is True
```

pero incluso eso significa identidad interna autenticada según el baseline actual.

### 10.1 Residual explícito: origen de AuthorizationDecision

`AuthorizationDecision` es un contrato estructural ordinario. Un objeto con:

```text
allowed=True
request_id=<matching id>
```

no constituye por sí solo prueba de que el PDP real haya producido esa decisión.

Por tanto G2 v1 no puede afirmar:

```text
"PDP origin cryptographically proven"
```

ni tratar `AuthorizationDecision.reason` como attestation de origen.

La garantía máxima de G2 v1 es:

```text
structurally valid authorization evidence
supplied inside trusted same-process orchestration
```

Si un uso futuro necesita demostrar origen de la decisión y no solo su binding estructural:

```text
STOP
→ abrir Authorization Decision Provenance gate
```

Ese gate futuro podrá evaluar, de forma separada, obtención directa desde PDP, attestation,
firmas u otro mecanismo gobernado. No se incorpora implícitamente a G2.

### 10.2 Stop condition de trust boundary

Si G2 necesitara aceptar observations o authorization evidence desde:

```text
remote producers
external agents
external tools
untrusted process boundaries
serialized/replayed evidence
```

entonces:

```text
STOP
→ reevaluar identity, signatures, nonce/replay protection and secure messaging
```

---

## 11. Permission scope sensible al valor

El permission requerido se deriva determinísticamente del kind y del valor:

```text
resource = cognition.assurance_signal.<signal_kind>
action   = produce.<canonical_value>
```

Ejemplos:

```text
applicability / NOT_APPLICABLE
→ cognition.assurance_signal.applicability
→ produce.not_applicable

support_sufficient / true
→ cognition.assurance_signal.support_sufficient
→ produce.true

policy_violation / false
→ cognition.assurance_signal.policy_violation
→ produce.false
```

Razón: valores como `support_sufficient=True`, `policy_violation=False`,
`evidence_required=False`, `applicability=NOT_APPLICABLE` o
`contradiction_unresolved=False` pueden remover blockers cognitivos.

```text
permission to assert X
!= proof that X is true
```

---

## 12. Input collection contract y límites

La futura API de G2 debe aceptar únicamente colecciones materializadas y finitas.

Dirección preferida:

```text
tuple[AssuranceSignalObservation, ...]
tuple[AssuranceSignalProducerAuthorizationEvidence, ...]
```

Prohibido aceptar como contrato público de esta foundation:

```text
arbitrary generator
unbounded iterator
lazy stream
network-backed iterable
```

Guardrails:

```text
max observations = 5
max authorization evidence objects = 5
```

Un set incompleto puede producir `HOLD`.

Un set por encima del máximo o con duplicados explícitos produce `DENIED`; G2 no consume
inputs ilimitados antes de verificar cardinalidad.

Cada `authorization_request.request_id` debe ser único dentro del set completo.

```text
same AuthorizationRequest reused for two signals
→ DENIED
```

Esto evita reutilización accidental de una decisión para scopes distintos.

---

## 13. Validaciones obligatorias de producer authorization

Por cada observation/evidence pair deben validarse, como mínimo:

```text
1. evidence type válido
2. evidence.signal_kind == observation.signal_kind
3. evidence.canonical_value == observation canonical value
4. evidence.request_id == observation.request_id == candidate.request_id
5. evidence.session_id == observation.session_id == candidate.session_id
6. evidence.producer_subject_id == observation.producer_subject_id
7. producer_subject_id == authorization_request.context.subject_id
8. authorization_request.context.authenticated is True
9. authorization_request.context.session_id == candidate.session_id
10. authorization_request.permission == required permission for kind + value
11. authorization_decision.request_id == authorization_request.request_id
12. authorization_request.request_id unique inside the set
13. temporal coherence valid
14. authorization_decision.allowed is True
```

Una decision permitida demuestra producer permission dentro del scope estructural
same-process; no demuestra verdad del signal ni prueba criptográfica de origen PDP.

---

## 14. Temporal coherence

Toda evaluación recibe `evaluated_at` explícito y todos los timestamps usados por G2 deben
ser timezone-aware UTC.

G2 exige:

```text
context.issued_at
    <= authorization_request.created_at
    <= evaluated_at
    < context.expires_at
```

Además:

```text
context.issued_at      = UTC
context.expires_at     = UTC
authorization_request.created_at = UTC
evaluated_at           = UTC
```

No se consulta reloj global.

El mismo `evaluated_at` valida todo el set.

Resultados:

```text
created_at before context.issued_at → DENIED
created_at after evaluated_at       → DENIED
evaluated_at before issued_at       → DENIED
evaluated_at >= expires_at          → DENIED
non-UTC temporal input              → fail safe / no READY
```

`AuthorizationDecision` no posee timestamp en el baseline actual; G2 no inventa uno.

---

## 15. Separación Security / Cognitive Policy

Prohibido:

```text
Security DENY  → policy_violation=True
Security ALLOW → policy_violation=False
```

Security responde si un subject puede producir una observation concreta.

El valor cognitivo responde una pregunta diferente.

Solo una futura policy de finalización explícita y separadamente autorizada podría consumir
una security disposition como input cognitivo.

Esta unidad no crea ese adapter.

---

## 16. Policy versioning

Boundary version:

```text
assurance-signal-projection/v1
```

Signal semantics version:

```text
assurance-signal-authority/v1
```

Compatible G2A target:

```text
protected-finalization/v1
```

Todas las observations de un set proyectable deben declarar exactamente la signal semantics
version aceptada.

Versión desconocida o incompatible no puede producir `READY`.

---

## 17. Exact completeness

Debe existir exactamente una observation autorizada por kind:

```text
APPLICABILITY                  1
EVIDENCE_REQUIRED              1
SUPPORT_SUFFICIENT             1
CONTRADICTION_UNRESOLVED       1
POLICY_VIOLATION               1
```

Y exactamente una authorization evidence object correspondiente a cada observation.

Semántica:

```text
missing signal                 → HOLD
missing auth evidence          → HOLD
duplicate signal               → DENIED
duplicate auth evidence        → DENIED
duplicate authorization req id → DENIED
unknown kind                   → invalid contract / no READY
```

Duplicados idénticos también son `DENIED`.

No hay last-write-wins ni selección arbitraria.

---

## 18. Canonical cross-signal coherence

G2 no decide verdad ni suficiencia, pero sí debe impedir representaciones internas
contradictorias que hagan ambiguo el input de G2A.

Para:

```text
APPLICABILITY = NOT_APPLICABLE
```

la única representación canónica proyectable es:

```text
evidence_required        = False
support_sufficient       = False
contradiction_unresolved = False
```

`policy_violation` permanece independiente y puede ser `True` o `False`, porque G2A le da
precedencia propia.

Por tanto:

```text
NOT_APPLICABLE + evidence_required=True
→ DENIED / SIGNAL_SET_INCOHERENT

NOT_APPLICABLE + contradiction_unresolved=True
→ DENIED / SIGNAL_SET_INCOHERENT

NOT_APPLICABLE + support_sufficient=True
→ DENIED / SIGNAL_SET_INCOHERENT
```

Razón:

```text
not applicable
!= evidence required
!= unresolved contradiction
!= positive support claim
```

Esto no desplaza policy de finalización hacia G2. G2 solo canonicaliza el shape semántico
que entrega; G2A conserva ownership de `ACCEPT | ABSTAIN | BLOCK`.

`REQUIRED` y `UNRESOLVED` no reciben reglas adicionales en G2 v1 más allá de contracts,
authority, binding y types ya congelados.

---

## 19. Projection outcome contract

```text
READY
HOLD
DENIED
```

### READY

Authority evidence, binding, temporalidad, versions, cardinalidad, types y cross-signal
coherence son válidos y completos.

Solo `READY` puede contener `ProtectedFinalizationInput`.

### HOLD

Falta evidencia necesaria sin prueba suficiente de una violación definitiva.

`HOLD` no contiene input parcial.

### DENIED

Existe misbinding, duplicidad, incoherencia, scope incorrecto, contexto inválido, producer no
autenticado, temporalidad inválida o authorization denial.

```text
G2 DENIED != G2A BLOCK
```

---

## 20. Reason codes mínimos

```text
MISSING_SIGNAL
MISSING_AUTHORIZATION_EVIDENCE
DUPLICATE_SIGNAL
DUPLICATE_AUTHORIZATION_EVIDENCE
DUPLICATE_AUTHORIZATION_REQUEST_ID
INPUT_CARDINALITY_EXCEEDED
REQUEST_ID_MISMATCH
SESSION_ID_MISMATCH
SIGNAL_KIND_MISMATCH
SIGNAL_VALUE_MISMATCH
SIGNAL_VALUE_INVALID
SIGNAL_SET_INCOHERENT
PRODUCER_SUBJECT_MISMATCH
PRODUCER_NOT_AUTHENTICATED
PERMISSION_SCOPE_MISMATCH
DECISION_REQUEST_MISMATCH
AUTHORIZATION_REQUEST_TIME_INVALID
CONTEXT_NOT_YET_VALID
CONTEXT_EXPIRED
AUTHORIZATION_DENIED
SIGNAL_POLICY_VERSION_MISMATCH
READY
```

Los nombres Python exactos pueden variar si preservan esta semántica cerrada.

---

## 21. Precedencia determinista e invariancia ante orden

Para inputs materialmente equivalentes, outcome y reason code no pueden depender del orden de
observations/evidence.

Precedencia congelada:

```text
0. invalid top-level contract/type/time representation
   → fail safe / no READY

1. input count above maximum
   → DENIED

2. duplicate signal / duplicate evidence / duplicate auth request id
   → DENIED

3. missing signal or missing matching evidence
   → HOLD

4. request/session/candidate binding mismatch
   → DENIED

5. kind/value/type incompatibility
   → DENIED

6. producer subject / authenticated binding failure
   → DENIED

7. permission scope mismatch
   → DENIED

8. temporal coherence failure
   → DENIED

9. authorization decision binding or allowed=False
   → DENIED

10. signal policy version mismatch
    → DENIED

11. cross-signal incoherence
    → DENIED

12. complete valid set
    → READY
```

Dentro de una misma clase de precedencia, la selección de reason code debe ser canónica y no
depender del primer elemento encontrado.

Test obligatorio:

```text
permutation(observations, evidence)
→ same outcome
→ same reason code
→ same projected input when READY
```

---

## 22. Deterministic projection

Solo en `READY`:

```text
ProtectedFinalizationInput(
    applicability=<exact projected applicability>,
    evidence_required=<exact bool>,
    support_sufficient=<exact bool>,
    contradiction_unresolved=<exact bool>,
    policy_violation=<exact bool>,
)
```

La projection no infiere, clasifica, corrige ni completa faltantes.

```text
G2 validates authority/projection
G2A evaluates finalization policy
```

---

## 23. E2E aislado obligatorio

La implementación futura debe demostrar:

```text
ProtectedResponseCandidate
        +
5 explicit observations
        +
5 bound authorization evidence objects
        ↓
G2 Signal Authority / Projection
        ↓
READY + ProtectedFinalizationInput
        ↓
existing G2A evaluator
        ↓
ACCEPT | ABSTAIN | BLOCK
```

Escenarios mínimos:

```text
A. complete canonical NOT_APPLICABLE set
   → G2 READY → G2A ACCEPT

B. complete valid REQUIRED set + support_sufficient=False
   → G2 READY → G2A ABSTAIN

C. complete valid set + policy_violation=True
   → G2 READY → G2A BLOCK

D. missing signal
   → G2 HOLD → G2A not invoked with projected input

E. unauthorized trust-clearing value
   → G2 DENIED → G2A not invoked

F. unauthenticated producer context even with allowed=True object
   → G2 DENIED

G. authorization evidence from another request in same session
   → G2 DENIED

H. authorization_request.created_at after evaluated_at
   → G2 DENIED

I. NOT_APPLICABLE + contradiction_unresolved=True
   → G2 DENIED

J. duplicated authorization_request.request_id across two signals
   → G2 DENIED

K. all permutations of the same valid set
   → same READY semantics and exact projected input
```

Este E2E no permite afirmar live Conversation assurance.

---

## 24. Tests negativos obligatorios

Como mínimo:

```text
wrong candidate type                    → fail safe
wrong observation collection type       → fail safe
wrong auth evidence collection type     → fail safe
generator/iterator input                → fail safe
non-UTC evaluated_at                    → fail safe
non-UTC auth request created_at         → fail safe
input cardinality above max             → DENIED
missing signal                          → HOLD
missing auth evidence                   → HOLD
duplicate signal                        → DENIED
duplicate auth evidence                 → DENIED
duplicate authorization request id      → DENIED
observation request mismatch            → DENIED
evidence request mismatch               → DENIED
observation session mismatch            → DENIED
evidence session mismatch               → DENIED
kind/value mismatch                     → DENIED
producer subject mismatch               → DENIED
producer not authenticated              → DENIED
permission scope mismatch               → DENIED
decision/request mismatch               → DENIED
auth request created before context     → DENIED
auth request created after evaluation   → DENIED
context not yet valid                   → DENIED
context expired                         → DENIED
authorization denied                    → DENIED
unknown signal policy version           → DENIED
NOT_APPLICABLE + evidence_required      → DENIED
NOT_APPLICABLE + support_sufficient     → DENIED
NOT_APPLICABLE + contradiction unresolved → DENIED
all five valid + authorized             → READY
READY contains exact projected input    → PASS
same material inputs                    → same projection semantics
all input permutations                  → same outcome/reason
```

Debe demostrarse que no existen defaults favorables.

---

## 25. Side effects prohibidos

G2 no puede:

- leer prompts;
- clasificar texto/materiality;
- llamar LLMs, providers o runtimes;
- acceder a red;
- aceptar producers remotos/no confiables;
- leer/escribir Memory o Knowledge;
- persistir observations o decisions;
- crear receipts durables;
- modificar history;
- modificar Kernel;
- modificar ConversationService o ConversationCapability;
- modificar CLI;
- modificar `Response` público;
- introducir dependencias externas.

---

## 26. Scope máximo de futura implementación

Si el Owner autoriza G2-IMPLEMENTATION:

```text
NEW
src/malak/core/assurance_signal_projection.py
tests/test_assurance_signal_projection.py
```

Este documento podrá actualizarse solo para candidate identity y evidencia de implementación.

No se autoriza modificar otros archivos productivos sin nuevo gate.

Expresamente fuera de alcance:

```text
Kernel
ConversationCapability
ConversationService
Conversation contracts
providers / runtimes
CLI
Memory / Knowledge
persistence / retrieval
SECURITY.md
Blueprint
Constitutions
ADR
public Response contract
Candidate Content Identity G2
Persistence Authorization
Conversation G2B
Sprint 7.12
RDD Stage 2
```

---

## 27. Correction Budget candidato

```yaml
production_files_new: 1
test_files_new: 1
existing_production_files_modified: 0
external_dependencies_added: 0
public_contract_changes: 0
kernel_delta: 0
conversation_delta: 0
memory_delta: 0
knowledge_delta: 0
persistence_delta: 0
max_fix_rounds_before_escalation: 1
production_delta_loc_guardrail: 350
test_delta_loc_guardrail: 800
```

Si una solución razonable supera materialmente este budget:

```text
STOP
→ new admission/design review
```

---

## 28. Validation envelope

Risk Class 3 exige:

```text
TDD estricto
candidate identity
RDD Stage 1 evidence
focused tests
full suite
compileall
git diff --check
FULL 4R
bounded correction if required
independent validation
isolated G2 → G2A E2E
candidate-bound CI
human review
human merge
post-merge validation
```

RDD Stage 2 permanece no autorizado.

---

## 29. Security Horizon Check

```text
Prompt & Context Trust Boundary   NOT_APPLICABLE
Identity / delegation             PARTIALLY_COVERED — same-process only
Decision origin attestation       BLOCKING_IF_REQUIRED_FOR_LIVE_USE
Strong cryptographic identity     DEFERRED / explicitly not claimed
Compromise containment            DEFERRED / no new operational surface
Memory / Knowledge poisoning      NOT_APPLICABLE
AI supply-chain trust             NOT_APPLICABLE
Data classification / disclosure  NOT_APPLICABLE
Resource Governance               ALREADY_COVERED by bounded pure execution
Observability / evidence           RDD Stage 1 candidate-bound engineering evidence only
Human in Control                  ALREADY_COVERED
```

No se habilita superficie externa ni persistente.

---

## 30. Stop conditions

Detener si la implementación requiere:

- inferencia probabilística para producer authority;
- autoasignación de trust;
- defaults favorables;
- autorización por kind ignorando value;
- aceptar `authenticated=False` como producer válido;
- aceptar evidence desde boundary remoto/no confiable;
- afirmar cryptographic identity/provenance no existente;
- afirmar PDP-origin a partir de un `AuthorizationDecision` estructural solamente;
- resolver proof-of-origin sin gate independiente;
- mapping general Security ALLOW/DENY → cognitive signal;
- durable binding sin identity/integrity suficiente;
- transporte/persistencia/replay de observations;
- colecciones lazy/unbounded;
- modificar G2A para esconder gaps de projection;
- Kernel o Conversation wiring;
- Memory/Knowledge/persistence;
- dependencias externas;
- registry/manager global no demostrado;
- expansión de autoridad.

```text
STOP
→ preserve evidence
→ report blocker
→ new design/admission gate
```

---

## 31. Condiciones para abrir G2B posteriormente

Una futura implementación exitosa de G2 no autoriza G2B.

Antes de G2B deberán existir, como mínimo:

```text
1. G2 integrado y validado;
2. producers legítimos para el scope conversacional elegido;
3. producer/runtime wiring diseñado sin confiar en callers arbitrarios;
4. decisión explícita sobre cómo se obtiene/verifica el origen de AuthorizationDecision
   para el scope live elegido;
5. applicability production autorizada;
6. evidence/support/contradiction production explícita;
7. cualquier Security→Cognitive mapping especificado y versionado;
8. history timing corregido:
   raw provider output must not enter assistant history before finalization;
9. G2B scope freeze independiente;
10. aprobación explícita del Owner.
```

```text
G2 implemented
!= legitimate conversation producers exist
!= PDP decision provenance solved for live use
!= G2B authorized
```

---

## 32. Rollback

Mientras G2 permanezca aislado:

```text
rollback = remove isolated G2 module + tests + candidate evidence updates
```

No existe migration, persistence, schema externo ni data repair.

---

## 33. Resultado del hardening de scope freeze

```text
G2 problem                              CONFIRMED
G2 necessity                            PASS
architecture fit                        PASS
current Security contracts reused       PASS, same-process only
cryptographic identity claimed          NO
PDP-origin cryptographically claimed    NO
authorization evidence request-bound    FROZEN
authorization evidence session-bound    FROZEN
value-sensitive producer scopes         FROZEN
temporal coherence                      FROZEN
bounded materialized collections        FROZEN
unique authorization request ids        FROZEN
exact completeness                      FROZEN
canonical NOT_APPLICABLE representation FROZEN
validation precedence                   FROZEN
permutation invariance                  REQUIRED
fail-closed projection                  FROZEN
G2 → G2A isolated E2E                   REQUIRED
Kernel change                           PROHIBITED
Conversation change                     PROHIBITED
Memory / Knowledge                      PROHIBITED
persistence                             PROHIBITED
external dependencies                   PROHIBITED
G2 implementation                       NOT AUTHORIZED
G2B                                     BLOCKED / NOT AUTHORIZED
Sprint 7.12                             NOT AUTHORIZED
RDD Stage 2                             NOT AUTHORIZED
```

Este documento queda listo para revisión humana del Owner.

Una aprobación posterior e inequívoca de **G2-IMPLEMENTATION** será necesaria antes de crear
`assurance_signal_projection.py` o cualquier test de implementación.
