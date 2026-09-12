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

El Owner autorizó avanzar únicamente con el gate de especificación de la siguiente
unidad candidata posterior a G2A:

```text
G2 — Assurance Signal Authority & Projection Foundation
```

Esta autorización congela un diseño candidato y sus límites.

No autoriza todavía implementación de código.

```text
G2-SPEC authorized
!=
G2 implementation authorized
!=
G2B authorized
!=
Sprint 7.12 authorized
!=
RDD Stage 2 authorized
```

Este documento no modifica Blueprint, Cognitive Constitution, Governance
Constitution, ADR-005, Security Control Plane ni contratos públicos existentes.

---

## 2. Baseline y necesidad comprobada

Baseline exacto:

```text
Aranwill/jarvis
main@c979f481e2e5353c8953e41e56e9218c7b1d4c6f
```

G2A ya materializa una foundation aislada:

```text
ProtectedResponseCandidate
        +
ProtectedFinalizationInput
        ↓
evaluate_protected_finalization(...)
        ↓
ACCEPT | ABSTAIN | BLOCK
```

pero consume directamente cinco signals ya resueltos:

```text
applicability
evidence_required
support_sufficient
contradiction_unresolved
policy_violation
```

El baseline no posee un boundary runtime autorizado que pueda demostrar:

```text
who produced each signal?
what exact signal/value may that producer assert?
which request/session/candidate is the observation bound to?
is the producer authorization still valid?
are all required signals present exactly once?
are the observations compatible with the projection policy?
```

Por tanto:

```text
G2A evaluator exists
+
no authorized signal projection boundary
=
G2B remains blocked
```

La necesidad está demostrada y no requiere introducir Conversation wiring para
ser materializada.

---

## 3. Resultado de admisión

Disposición de la línea candidata:

```text
Assurance Signal Boundary G2: ADOPT
```

Razones:

- implementa una necesidad explícita de R-022 / CC-011 / CC-012;
- completa una dependencia reconocida por G2A y por Signal Authority G0/G1;
- reutiliza Security Control Plane para demostrar producer permission sin
  convertir Security en autoridad cognitiva;
- puede implementarse de forma pura, determinista, aislada y reversible;
- no requiere Kernel, Conversation, provider/runtime, Memory, Knowledge,
  persistencia ni dependencias externas.

La clasificación `ADOPT` no equivale a autorización de implementación.

---

## 4. Objetivo verificable

Materializar, en una futura implementación separadamente autorizada, una
foundation que acepte observations explícitas y pueda producir un
`ProtectedFinalizationInput` únicamente cuando la autoridad, binding,
completitud y compatibilidad de esas observations puedan demostrarse.

Flujo objetivo:

```text
ProtectedResponseCandidate
        +
Explicit Signal Observations
        +
Producer Authorization Evidence
        ↓
producer scope validation
        ↓
request/session/candidate binding
        ↓
signal/value compatibility
        ↓
policy-version compatibility
        ↓
exact completeness
        ↓
READY | HOLD | DENIED
        ↓
ProtectedFinalizationInput only when READY
```

La projection no decide verdad, materialidad ni suficiencia por sí misma.

Solo valida si observations explícitas pueden ser legítimamente proyectadas al
contrato que G2A ya consume.

---

## 5. Invariantes obligatorios

La unidad deberá preservar:

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
!= cryptographic integrity
!= replay protection
```

Y:

```text
G2 READY
!= G2A ACCEPT
```

`READY` significa únicamente que el set de signals puede ser proyectado de forma
válida al input de G2A. La decisión de finalización sigue perteneciendo a G2A.

---

## 6. Boundary seleccionado

La unidad futura debe ser una foundation interna y aislada.

Ubicación candidata congelada:

```text
src/malak/core/assurance_signal_projection.py
```

Archivo de tests candidato:

```text
tests/test_assurance_signal_projection.py
```

No se crea una nueva layer arquitectónica, manager global, registry global,
service runtime ni authority domain.

No se modifica `src/malak/core/protected_finalization.py` para implementar G2.

---

## 7. Signal kinds cerrados

G2 admite exactamente cinco kinds:

```text
APPLICABILITY
EVIDENCE_REQUIRED
SUPPORT_SUFFICIENT
CONTRADICTION_UNRESOLVED
POLICY_VIOLATION
```

No se admiten extensions silenciosas.

Agregar un sexto signal requiere nuevo gate de diseño porque cambia completitud,
semántica y policy compatibility.

---

## 8. Valores permitidos

### 8.1 Applicability

Valores:

```text
NOT_APPLICABLE
REQUIRED
UNRESOLVED
```

Debe mapear exactamente a `AssuranceApplicability` de G2A.

### 8.2 Signals booleanos

Los cuatro signals restantes requieren `bool` real:

```text
evidence_required
support_sufficient
contradiction_unresolved
policy_violation
```

No se permiten:

```text
0 / 1
strings
None
truthy objects
implicit coercion
```

---

## 9. Observation contract candidato

Una observation mínima deberá representar conceptualmente:

```text
AssuranceSignalObservation
├── signal_kind
├── value
├── request_id
├── session_id
├── producer_subject_id
└── signal_policy_version
```

Propiedades:

- inmutable;
- sin defaults favorables;
- `request_id`, `session_id` y `producer_subject_id` canónicos y no vacíos;
- `signal_kind` mediante enum cerrado;
- `value` validado estrictamente según kind;
- `signal_policy_version` explícito y canónico.

La observation no contiene permiso implícito.

```text
observation exists
!= producer authorized
```

---

## 10. Binding permitido

Candidate Content Identity G2 permanece no autorizado.

Por tanto G2 utiliza únicamente el máximo binding permitido por Signal Authority
G0/G1:

```text
same-process
request-bound
session-bound
direct candidate object passed to projection
no durable receipt
no replay claim
no cryptographic content identity claim
```

La projection recibe directamente el `ProtectedResponseCandidate` que será
consumido por G2A y exige para cada observation:

```text
observation.request_id == candidate.request_id
observation.session_id == candidate.session_id
```

La identidad del objeto/call boundary solo posee significado dentro de la
invocación actual.

No se persiste ni serializa como prueba durable de identidad de contenido.

### Stop condition

Si una implementación necesita transportar, persistir, rehidratar o reutilizar
observations fuera de este mismo boundary de proceso:

```text
STOP
→ no ampliar G2
→ abrir gate independiente de identity/integrity binding
```

No reutilizar silenciosamente Candidate Content Identity episódica.

---

## 11. Producer authorization evidence

G2 reutiliza los contratos existentes del Security Control Plane únicamente para
demostrar producer permission:

```text
SecurityContext
AuthorizationRequest
AuthorizationDecision
PermissionScope
```

No se modifican esos contratos en esta unidad.

Evidence conceptual mínima:

```text
AssuranceSignalProducerAuthorizationEvidence
├── signal_kind
├── canonical_value
├── producer_subject_id
├── authorization_request
└── authorization_decision
```

La evidencia debe demostrar que el subject estaba autorizado para producir ese
**kind + value** concreto.

No basta autorizar genéricamente al subject como "assurance producer".

---

## 12. Permission scope sensible al valor

El permission requerido se deriva determinísticamente del signal y de su valor.

Forma congelada:

```text
resource = cognition.assurance_signal.<signal_kind>
action   = produce.<canonical_value>
```

Ejemplos:

```text
APPLICABILITY = NOT_APPLICABLE
→ cognition.assurance_signal.applicability
→ produce.not_applicable

APPLICABILITY = REQUIRED
→ cognition.assurance_signal.applicability
→ produce.required

EVIDENCE_REQUIRED = false
→ cognition.assurance_signal.evidence_required
→ produce.false

SUPPORT_SUFFICIENT = true
→ cognition.assurance_signal.support_sufficient
→ produce.true

CONTRADICTION_UNRESOLVED = false
→ cognition.assurance_signal.contradiction_unresolved
→ produce.false

POLICY_VIOLATION = true
→ cognition.assurance_signal.policy_violation
→ produce.true
```

Razón:

Una autorización por kind solamente sería demasiado amplia.

Afirmar:

```text
support_sufficient=True
policy_violation=False
evidence_required=False
applicability=NOT_APPLICABLE
contradiction_unresolved=False
```

puede remover blockers cognitivos y, por tanto, no debe compartir necesariamente
el mismo permission scope que el valor opuesto.

La diferenciación de permisos no convierte un valor autorizado en verdadero.

```text
permission to assert X
!= proof that X is true
```

---

## 13. Validaciones obligatorias de producer authorization

Para cada observation deben verificarse, como mínimo:

```text
1. evidence type válido
2. evidence.signal_kind == observation.signal_kind
3. evidence.canonical_value == observation canonical value
4. evidence.producer_subject_id == observation.producer_subject_id
5. producer_subject_id == authorization_request.context.subject_id
6. authorization_request.context.session_id == candidate.session_id
7. authorization_request.permission == required permission for kind + value
8. authorization_decision.request_id == authorization_request.request_id
9. evaluated_at >= context.issued_at
10. evaluated_at < context.expires_at
11. authorization_decision.allowed is True
```

Una `AuthorizationDecision` permitida solo demuestra producer permission dentro
de su scope.

Nunca se traduce automáticamente a:

```text
policy_violation=False
support_sufficient=True
```

---

## 14. Separación Security / Cognitive Policy

Queda explícitamente prohibido implementar una regla general del tipo:

```text
Security DENY
→ policy_violation=True
```

También está prohibido:

```text
Security ALLOW
→ policy_violation=False
```

Security responde:

> ¿puede este subject producir esta clase exacta de observation?

El contenido cognitivo responde una pregunta distinta.

Solo una futura policy de finalización explícita, versionada y separadamente
autorizada podría consumir una security disposition como input cognitivo.

Esta unidad no crea ese adapter.

---

## 15. Policy versioning

Versión candidata del boundary:

```text
assurance-signal-projection/v1
```

Versión de signal semantics aceptada:

```text
assurance-signal-authority/v1
```

Target de G2A compatible:

```text
protected-finalization/v1
```

Todas las observations de un set proyectable deben declarar exactamente la
versión de signal semantics aceptada por esta projection.

Una versión desconocida o incompatible no puede producir `READY`.

La projection no modifica ni reinterpreta la policy de G2A.

---

## 16. Exact completeness

Un set proyectable exige exactamente una observation autorizada para cada kind:

```text
APPLICABILITY                  exactly 1
EVIDENCE_REQUIRED              exactly 1
SUPPORT_SUFFICIENT              exactly 1
CONTRADICTION_UNRESOLVED        exactly 1
POLICY_VIOLATION                exactly 1
```

Reglas:

```text
missing observation
→ HOLD

extra unknown observation
→ invalid contract / no READY

duplicate kind
→ DENIED

conflicting duplicate values
→ DENIED

identical duplicate values
→ DENIED
```

No se aplica last-write-wins.

No se elige arbitrariamente una observation entre duplicados.

---

## 17. Projection outcome contract

Outcomes candidatos:

```text
READY
HOLD
DENIED
```

### READY

Authority, binding, version, cardinalidad y tipos son válidos y completos.

Solo `READY` puede incluir un `ProtectedFinalizationInput`.

### HOLD

Falta información necesaria pero no existe evidencia suficiente de una
violación estructural o de autorización definitiva.

Ejemplos:

```text
missing signal
missing authorization evidence
```

`HOLD` no puede incluir un `ProtectedFinalizationInput` parcial.

### DENIED

Existe evidencia de misbinding, duplicidad, incompatibilidad, producer scope
incorrecto, autorización denegada/expirada u otra violación cerrada.

`DENIED` no se convierte automáticamente en `BLOCK` de G2A porque son dominios
diferentes.

```text
G2 DENIED
!= G2A BLOCK
```

---

## 18. Reason codes mínimos

La implementación futura deberá incluir reason codes cerrados equivalentes a:

```text
MISSING_SIGNAL
MISSING_AUTHORIZATION_EVIDENCE
DUPLICATE_SIGNAL
REQUEST_ID_MISMATCH
SESSION_ID_MISMATCH
SIGNAL_KIND_MISMATCH
SIGNAL_VALUE_MISMATCH
SIGNAL_VALUE_INVALID
PRODUCER_SUBJECT_MISMATCH
PERMISSION_SCOPE_MISMATCH
DECISION_REQUEST_MISMATCH
CONTEXT_NOT_YET_VALID
CONTEXT_EXPIRED
AUTHORIZATION_DENIED
SIGNAL_POLICY_VERSION_MISMATCH
READY
```

Los nombres Python exactos podrán ajustarse si preservan la semántica congelada.

No se permite un reason genérico que oculte cuál invariante falló.

---

## 19. Deterministic projection

Cuando y solo cuando el outcome sea `READY`, la projection construye:

```text
ProtectedFinalizationInput(
    applicability=<exact projected applicability>,
    evidence_required=<exact projected bool>,
    support_sufficient=<exact projected bool>,
    contradiction_unresolved=<exact projected bool>,
    policy_violation=<exact projected bool>,
)
```

No transforma semánticamente los valores.

No infiere.

No clasifica.

No corrige.

No completa faltantes.

No decide si la combination será finalmente aceptada por G2A.

Inconsistencias cognitivas que G2A ya maneja, por ejemplo:

```text
NOT_APPLICABLE + evidence_required=True
```

pueden proyectarse si ambas observations son legítimas y completas; G2A conserva
la responsabilidad de aplicar su precedencia y producir `ABSTAIN`.

Esto preserva ownership:

```text
G2 validates authority/projection
G2A evaluates finalization policy
```

---

## 20. evaluated_at

Toda evaluación de G2 debe recibir `evaluated_at` explícito.

Requisitos:

```text
datetime
timezone-aware
UTC
```

La projection no consulta reloj global.

El mismo `evaluated_at` se utiliza para validar temporalmente todos los
`SecurityContext` del set.

---

## 21. E2E aislado obligatorio

La futura implementación debe demostrar un E2E real de la cadena afectada sin
conectar Conversation:

```text
ProtectedResponseCandidate
        +
5 explicit observations
        +
5 valid producer authorization evidence objects
        ↓
G2 Signal Authority / Projection
        ↓
READY + ProtectedFinalizationInput
        ↓
existing G2A evaluator
        ↓
ACCEPT | ABSTAIN | BLOCK
```

Escenarios E2E mínimos:

```text
A. complete valid set + NOT_APPLICABLE/evidence_required=False
   → G2 READY
   → G2A ACCEPT

B. complete valid set + REQUIRED/support_sufficient=False
   → G2 READY
   → G2A ABSTAIN

C. complete valid set + policy_violation=True
   → G2 READY
   → G2A BLOCK

D. missing signal
   → G2 HOLD
   → G2A must not be invoked with a projected input

E. unauthorized trust-increasing value
   → G2 DENIED
   → G2A must not be invoked with a projected input
```

Este E2E no permite afirmar live Conversation assurance.

---

## 22. Tests negativos obligatorios

La implementación futura debe cubrir, como mínimo:

```text
wrong candidate type                       → fail safe
wrong observation type                     → fail safe
wrong authorization evidence type          → fail safe
non-UTC evaluated_at                       → fail safe
missing one of five signals                → HOLD
missing auth evidence                      → HOLD
duplicate signal                           → DENIED
request mismatch                           → DENIED
session mismatch                           → DENIED
kind mismatch                              → DENIED
value mismatch                             → DENIED
producer subject mismatch                  → DENIED
permission scope mismatch                  → DENIED
decision/request mismatch                  → DENIED
context not yet valid                      → DENIED
context expired                            → DENIED
authorization denied                       → DENIED
unknown signal policy version              → DENIED
all five valid + authorized                → READY
READY contains exact projected input       → PASS
same material inputs                       → same projection semantics
```

También debe demostrarse que no existen defaults favorables.

---

## 23. Side effects prohibidos

G2 no puede:

- leer prompts;
- clasificar texto;
- determinar materiality mediante heurísticas;
- llamar LLMs;
- llamar providers;
- llamar runtimes;
- acceder a red;
- acceder a filesystem operacional;
- leer o escribir Memory;
- leer o escribir Knowledge;
- persistir observations;
- persistir decisiones;
- crear receipts durables;
- emitir eventos obligatorios;
- modificar conversation history;
- modificar Kernel;
- modificar ConversationService;
- modificar ConversationCapability;
- modificar CLI;
- modificar `Response` público;
- introducir nuevas dependencias externas.

---

## 24. Archivos autorizables para una futura implementación

Si el Owner autoriza posteriormente G2-IMPLEMENTATION, el scope máximo inicial
será:

```text
NEW
src/malak/core/assurance_signal_projection.py

tests/test_assurance_signal_projection.py
```

Este documento podrá actualizarse únicamente para registrar candidate identity y
evidencia de implementación.

No se autoriza modificar otros archivos productivos sin nuevo gate.

---

## 25. Componentes expresamente prohibidos

Fuera de alcance:

```text
src/malak/kernel/**
src/malak/capabilities/conversation.py
src/malak/services/conversation_service.py
src/malak/core/conversation.py
providers / runtimes
CLI
Memory
Knowledge
persistence
retrieval
SECURITY.md
Blueprint
Cognitive Constitution
Governance Constitution
ADR
public Response contract
Candidate Content Identity G2
Persistence Authorization
Conversation G2B
Sprint 7.12
RDD Stage 2
```

No se autoriza ampliar el scope para "preparar" G2B.

---

## 26. Correction Budget candidato

Guardrails de una futura implementación:

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
test_delta_loc_guardrail: 700
```

Los límites LOC son guardrails de complejidad, no una medida de autoridad.

Si la solución razonable supera materialmente este budget:

```text
STOP
→ no expandir silenciosamente
→ volver a admission/design review
```

---

## 27. Risk class y validation envelope

Clasificación candidata:

```text
Risk Class 3 — High
```

Razón:

La unidad valida producer authority para signals que influyen en una frontera de
finalización cognitiva, aunque permanezca aislada y sin efectos operacionales.

Una futura implementación requiere:

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

## 28. Cuatro preguntas obligatorias

### Blueprint

```text
PASS
```

Materializa una frontera determinista para R-022 sin agregar lógica al Kernel.

### Cognitive Constitution

```text
PASS
```

Refuerza CC-011/CC-012, no asumir, evidencia sobre especulación y fail-safe ante
información insuficiente.

### Governance Constitution

```text
PASS
```

Reutiliza autorización explícita, mínimo privilegio y separación de
responsabilidades sin trasladar authority al productor cognitivo.

### Kernel simplicity

```text
PASS
kernel delta = 0
```

---

## 29. Security Horizon Check

Resultado:

```text
Prompt & Context Trust Boundary          NOT_APPLICABLE
Identity / delegation                    ALREADY_COVERED for this same-process scope
Compromise containment                   DEFERRED / no new operational surface
Memory / Knowledge poisoning             NOT_APPLICABLE
AI supply-chain trust                     NOT_APPLICABLE
Data classification / disclosure          NOT_APPLICABLE
Resource Governance                       ALREADY_COVERED by bounded pure execution
Observability / evidence                  REQUIRES candidate-bound engineering evidence only
Human in Control                          ALREADY_COVERED
```

No se habilita una nueva superficie externa o persistente.

---

## 30. Stop conditions

Detener la implementación si requiere cualquiera de los siguientes:

- inferencia probabilística para producer authority;
- autoasignación de trust por el producer;
- defaults favorables;
- autorización por signal kind ignorando el valor cuando el valor cambia el
  efecto cognitivo;
- mapping general Security ALLOW/DENY → cognitive policy signal;
- durable binding sin identity/integrity suficiente;
- transporte o persistencia de observations;
- modificación de G2A para esconder un gap de projection;
- modificación de Kernel;
- Conversation wiring;
- history changes;
- Memory/Knowledge;
- persistencia;
- nuevas dependencias externas;
- ampliación de autoridad;
- necesidad de un registry/manager global no demostrado.

Ante una stop condition:

```text
STOP
→ preserve evidence
→ report blocker
→ new design/admission gate
```

---

## 31. Condiciones para abrir G2B posteriormente

Incluso después de una futura implementación exitosa de G2, Conversation G2B no
queda automáticamente autorizado.

Antes de G2B todavía deberán existir, como mínimo:

```text
1. G2 Signal Authority / Projection integrado y validado;
2. productores legítimos de observations para el scope conversacional elegido;
3. una forma autorizada de determinar applicability;
4. una forma explícita de producir evidence-required/support/contradiction;
5. policy mapping explícito para cualquier security disposition consumida;
6. diseño y autorización del cambio de history timing:
   raw provider output must not enter assistant history before finalization;
7. G2B scope freeze independiente;
8. aprobación explícita del Owner.
```

Por tanto:

```text
G2 implemented
!= legitimate conversation signal producers exist
!= G2B authorized
```

---

## 32. Rollback

Mientras G2 permanezca aislado y sin consumers runtime:

```text
rollback = remove isolated G2 module + tests + candidate spec updates
```

No existe migration, persistence, schema externo, state repair ni data rollback.

La reversibilidad es alta.

---

## 33. Resultado del scope freeze

```text
G2 problem                         CONFIRMED
G2 necessity                       PASS
architecture fit                   PASS
reuse existing authority contracts PASS
value-sensitive producer scopes    FROZEN
same-process binding               FROZEN
exact completeness                 FROZEN
fail-closed projection             FROZEN
G2 → G2A isolated E2E              REQUIRED
Kernel change                      PROHIBITED
Conversation change                PROHIBITED
Memory / Knowledge                 PROHIBITED
persistence                        PROHIBITED
external dependencies              PROHIBITED
G2 implementation                  NOT AUTHORIZED
G2B                                BLOCKED / NOT AUTHORIZED
Sprint 7.12                        NOT AUTHORIZED
RDD Stage 2                        NOT AUTHORIZED
```

Este documento queda listo para revisión humana del Owner.

Una aprobación posterior e inequívoca de **G2-IMPLEMENTATION** será necesaria
antes de crear `assurance_signal_projection.py` o cualquier test de producción
asociado.