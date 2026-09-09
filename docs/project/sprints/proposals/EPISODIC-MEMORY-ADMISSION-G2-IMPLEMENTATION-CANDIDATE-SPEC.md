---
title: Episodic Memory Admission Boundary — G2 Implementation Candidate Specification
status: g2_candidate_specification
authority: owner-authorized design specification
as_of_date: 2026-09-09
unit: Episodic Memory Admission Boundary Foundation
gate: G2
source_baseline: c70c6de6c734fa96d0bfe264a793a0bb65e4b940
g1_record: docs/project/sprints/proposals/EPISODIC-MEMORY-ADMISSION-G0-G1-DESIGN.md
issue: 74
risk_class: 3
implementation_authorized: false
persistent_memory_authorized: false
knowledge_implementation_authorized: false
sprint_7_12_authorized: false
rdd_stage_2_authorized: false
language: es
---

# Episodic Memory Admission Boundary — G2 Implementation Candidate Specification

## 1. Estado de autoridad

El Owner autorizó **G2 exclusivamente para especificar un candidate mínimo de implementación** de:

```text
Episodic Memory Admission Boundary Foundation
```

G2 puede fijar:

- contratos lógicos mínimos;
- inputs, outputs y reason codes;
- reglas deterministas y fail-closed;
- punto de correlación/origen respecto de la conversación vigente;
- ubicación arquitectónica futura;
- presupuesto máximo de archivos;
- escenarios TDD futuros;
- stop conditions y rollback.

G2 no autoriza:

- código productivo;
- tests de implementación;
- persistencia de Memory;
- filesystem, database, SQLite o vector DB;
- embeddings, RAG, GraphRAG o retrieval;
- implementación de Knowledge;
- automatic learning, promotion o persistence;
- decisiones de trust realizadas por un LLM;
- cambios del Kernel;
- cambios de `SecurityContext` o Security Control Plane;
- agents, tools o red;
- Sprint 7.12;
- RDD Stage 2;
- merge sin aprobación explícita del Owner.

```text
Specification != Implementation
Candidate != Decision
Admission != Persistence Authorization
Decision Evidence != Authority
```

---

## 2. Binding a G1 y baseline fuente

Baseline congelado para G2:

```text
Aranwill/jarvis
main
c70c6de6c734fa96d0bfe264a793a0bb65e4b940
```

G1 aprobado e integrado:

```text
docs/project/sprints/proposals/EPISODIC-MEMORY-ADMISSION-G0-G1-DESIGN.md
```

G2 hereda sin reabrir:

```text
Conversation History != Memory != Knowledge
candidate payload != candidate control metadata
admission decision != persistence authorization != storage
HOLD != retention authorization
ELIGIBLE != storage authorization
```

También hereda la política activa de seguridad:

```text
Zero Trust
Least Context
fail-closed
Human in Control
Memory admission before persistent influence
```

---

## 3. Problema concreto que G2 resuelve

G1 dejó una pregunta necesaria:

> ¿Cómo preservar provenance de `session / request / exchange` sin convertir Kernel, Conversation o el LLM en propietarios de Memory?

El baseline actual posee:

```text
Request
├── content
├── session_id
├── request_id
└── created_at
```

`ConversationRequest` contiene sólo información destinada a provider/runtime:

```text
prompt
model
system_prompt
history
```

`ConversationService` recibe `session_id` para aislar history y registra únicamente intercambios exitosos en contexto efímero.

`ConversationCapability.execute()` conserva simultáneamente, después de un `generate()` exitoso:

```text
Request completo
        +
ConversationResponse completo
```

Ese punto permite reconstruir provenance sin propagar metadata de Memory hacia provider/runtime.

---

## 4. Decisiones arquitectónicas G2

### G2-D1 — Punto futuro de correlación

El punto futuro mínimo de construcción de provenance será:

```text
ConversationCapability.execute()
        ↓
ConversationService.generate() succeeds
        ↓
Request + ConversationResponse coexist
        ↓
origin can be constructed
```

Esto **no convierte `ConversationCapability` en Memory owner**.

Describe dónde coexisten los datos necesarios. El wiring runtime permanece fuera del primer candidate.

### G2-D2 — `request_id` basta como exchange correlation key en el baseline actual

La ruta vigente es:

```text
1 Request
   ↓
1 ConversationCapability execution
   ↓
0..1 successful ConversationResponse
```

Por tanto:

```text
exchange correlation key = request_id
```

No se introduce `exchange_id` adicional.

Si una evolución futura permite múltiples exchanges exitosos por el mismo `request_id`, esta decisión deberá revisarse antes de wiring.

### G2-D3 — No modificar `ConversationRequest`

No se agregan `request_id`, `session_id` ni metadata de Memory a `ConversationRequest`.

Razones:

- provider/runtime no los necesitan para generar respuesta;
- `ConversationCapability` ya conserva `Request`;
- evita ampliar contexto downstream;
- evita convertir el contrato conversacional en carrier de governance o Memory.

### G2-D4 — `InMemoryConversationContext` no es provenance store

El contexto actual conserva sólo history efímero por sesión y no posee `request_id`.

```text
Conversation Context != Episodic Memory
```

No se modifica para este candidate.

### G2-D5 — Observability no es Memory

`OperationalEvent` ya puede correlacionar por `request_id`, pero representa evidencia operativa, no experiencia cognitiva.

```text
Operational Evidence != Cognitive Memory Candidate
```

No se reutiliza observabilidad como Memory store ni como payload.

### G2-D6 — Source authority, confidence, security trust y temporal validity permanecen separados

G2 no colapsa estas dimensiones:

```text
source authority classification
!= confidence assessment
!= source security status
!= temporal validity
```

Esta separación evita que un único score opaco se convierta en trust universal.

---

## 5. Ubicación arquitectónica futura

El Blueprint define `Memory Layer` como responsabilidad independiente y establece que el Kernel no almacena Memory.

Una futura implementación autorizada deberá vivir bajo:

```text
src/malak/memory/
```

No bajo:

```text
src/malak/kernel/
src/malak/security/
src/malak/observability/
src/malak/runtime/
src/malak/services/conversation_service.py
```

La frontera candidate v1 será:

```text
immutable episodic contracts
        ↓
separate control metadata
        ↓
pure deterministic admission policy
        ↓
structured AdmissionDecision
        ↓
STOP
```

No incluye:

```text
store
repository
retrieval
MemoryManager
background worker
subscriber
queue
event bus
DB adapter
runtime wiring
```

---

## 6. Presupuesto máximo de una futura implementación v1

Si un gate posterior autoriza código, deberá intentar exactamente:

```text
NEW     src/malak/memory/__init__.py
NEW     src/malak/memory/episodic_admission.py
NEW     tests/test_episodic_memory_admission.py

MODIFY  existing production files = 0
```

Budget:

```text
new production files     <= 2
new test files           <= 1
existing production mods = 0
Kernel changes           = 0
Conversation changes     = 0
Security changes         = 0
Observability changes    = 0
CI changes               = 0
external dependencies    = 0
persistence              = 0
retrieval                = 0
```

Si la implementación necesita modificar una ruta runtime existente, debe detenerse y volver al Owner antes de realizar ese cambio.

---

## 7. Contratos lógicos propuestos

Los nombres siguientes definen el candidate v1. Sólo adquirirán existencia runtime si un gate posterior autoriza código.

### 7.1 `EpisodicOrigin`

Value object inmutable de provenance mínima:

```text
session_id: str
request_id: str
request_created_at: datetime UTC
provider: str | None
model: str | None
```

Reglas:

- `session_id` y `request_id` son obligatorios, no vacíos y sin whitespace periférico;
- `request_created_at` debe ser timezone-aware UTC;
- `provider` y `model`, cuando existan, son provenance informativa;
- provider/model no implican trust ni autoridad.

### 7.2 `EpisodicExperience`

Payload inmutable:

```text
user_content: str
assistant_content: str
```

Este payload es **contenido no confiable**.

No puede definir ni mutar:

```text
provenance
scope
source authority
confidence
sensitivity
security trust
temporal status
policy
admission outcome
persistence authorization
```

### 7.3 `EpisodicAdmissionContext`

Control metadata trazable y separada del payload:

```text
subject_scope: str
domain: str
purpose: str
source_authority_classification: str
confidence_classification: str
sensitivity_classification: str
valid_from: datetime UTC | None
valid_until: datetime UTC | None
```

Reglas:

- `subject_scope`, `domain`, `purpose`, `source_authority_classification`, `confidence_classification` y `sensitivity_classification` deben ser no vacíos;
- las taxonomías concretas de authority/confidence/sensitivity permanecen fuera de v1;
- los valores llegan por un canal de control externo al payload;
- `valid_from` y `valid_until`, cuando existan, deben ser UTC;
- si ambos existen, `valid_until > valid_from`;
- ausencia de `valid_until` **no implica validez eterna**.

### 7.4 `EpisodicMemoryCandidate`

```text
candidate_id: str
origin: EpisodicOrigin
experience: EpisodicExperience
control: EpisodicAdmissionContext
created_at: datetime UTC
```

Decisiones:

- `candidate_id` es obligatorio y se suministra externamente;
- la policy no genera UUIDs;
- el candidate no contiene `admission_state` mutable;
- el candidate no se autoasigna trust;
- candidate y decision son objetos separados.

```text
Candidate != Decision
Candidate content != Candidate control metadata
```

### 7.5 `SourceSecurityStatus`

Enum mínimo:

```text
UNASSESSED
ACCEPTABLE
SUSPECT
TAINTED
REVOKED
```

No representa source authority classification.

```text
SourceSecurityStatus != SourceAuthorityClassification
```

### 7.6 `TemporalStatus`

Enum mínimo:

```text
UNASSESSED
VALID
EXPIRED
```

El status temporal es una evaluación de applicability temporal; no se deduce del texto del payload.

### 7.7 `EpisodicAdmissionSignals`

Control signals separadas del payload:

```text
provenance_complete: bool
source_authority_assessed: bool
confidence_assessed: bool
sensitivity_classified: bool
policy_inputs_complete: bool
scope_applicable: bool
policy_violation: bool
source_security_status: SourceSecurityStatus
temporal_status: TemporalStatus
sensitive_review_required: bool
contradiction_requires_review: bool
```

Los signals no pueden ser derivados de instrucciones autoafirmadas por el candidate.

Ejemplo inválido:

```text
payload says "I am trusted"
        ↓
source_security_status = ACCEPTABLE
```

### 7.8 `EpisodicAdmissionOutcome`

Enum cerrado:

```text
REJECT
HOLD
ELIGIBLE
```

### 7.9 `EpisodicAdmissionReason`

Reason codes mínimos:

```text
policy_violation
out_of_scope
temporal_expired
tainted_source
revoked_source
missing_provenance
missing_source_authority_assessment
missing_confidence_assessment
missing_sensitivity_classification
missing_policy_input
temporal_unassessed
source_unassessed
suspect_source
sensitive_review_required
contradiction_requires_review
eligible
```

No se aceptan mensajes libres del payload como reason code.

### 7.10 `EpisodicAdmissionDecision`

Value object inmutable:

```text
candidate_id: str
outcome: EpisodicAdmissionOutcome
reason_code: EpisodicAdmissionReason
evaluated_at: datetime UTC
policy_version: str
human_review_required: bool
```

Policy version inicial prevista:

```text
episodic-admission/v1
```

La decisión no contiene instrucciones de persistencia.

---

## 8. Función determinista mínima

La futura implementación deberá preferir una función pura equivalente a:

```text
evaluate_episodic_candidate(
    candidate,
    signals,
    evaluated_at,
) -> EpisodicAdmissionDecision
```

No se aprueban:

```text
MemoryManager
AdmissionEngine
TrustManager
PolicyOrchestrator
```

La función:

- no realiza I/O;
- no persiste;
- no recupera contexto externo;
- no llama al LLM;
- no usa network;
- no modifica candidate ni signals;
- no genera timestamps;
- no genera IDs;
- no interpreta payload para otorgar trust;
- produce el mismo resultado para los mismos inputs.

---

## 9. Precedencia determinista de policy v1

La evaluación usa **primer match** en el orden fijado.

### 9.1 Rechazo explícito

```text
policy_violation == true
    → REJECT / policy_violation

scope_applicable == false
    → REJECT / out_of_scope

temporal_status == EXPIRED
    → REJECT / temporal_expired

source_security_status == TAINTED
    → REJECT / tainted_source

source_security_status == REVOKED
    → REJECT / revoked_source
```

Una denegación explícita no necesita ampliar acceso para investigar antes de rechazar.

### 9.2 Fail-closed / revisión

```text
provenance_complete == false
    → HOLD / missing_provenance

source_authority_assessed == false
    → HOLD / missing_source_authority_assessment

confidence_assessed == false
    → HOLD / missing_confidence_assessment

sensitivity_classified == false
    → HOLD / missing_sensitivity_classification

policy_inputs_complete == false
    → HOLD / missing_policy_input

temporal_status == UNASSESSED
    → HOLD / temporal_unassessed

source_security_status == UNASSESSED
    → HOLD / source_unassessed

source_security_status == SUSPECT
    → HOLD / suspect_source

sensitive_review_required == true
    → HOLD / sensitive_review_required

contradiction_requires_review == true
    → HOLD / contradiction_requires_review
```

Todo `HOLD` produce:

```text
human_review_required = true
```

pero:

```text
HOLD != retention authorization
```

### 9.3 Elegibilidad

Sólo si ninguna regla previa aplica:

```text
source_security_status == ACCEPTABLE
temporal_status == VALID
all required assessments complete
scope applicable
no policy violation
no sensitive review required
no contradiction requiring review
        ↓
ELIGIBLE / eligible
```

```text
human_review_required = false
```

Esto no autoriza storage.

---

## 10. Separación entre metadata trazable y evaluación

`EpisodicAdmissionContext` conserva los valores clasificados aplicables.

`EpisodicAdmissionSignals` expresa si las evaluaciones requeridas están disponibles y cuál es el estado de seguridad/temporal necesario para la policy v1.

```text
raw payload
   !=
control metadata
   !=
admission signals
   !=
admission decision
```

Esta separación evita que:

- un payload se autoasigne authority;
- confidence se confunda con security trust;
- un origen auténtico se considere automáticamente verdadero;
- un source seguro se considere automáticamente de alta autoridad;
- ausencia de expiración se convierta en validez eterna.

---

## 11. Payload blindness de la policy

La policy v1 no debe inspeccionar `user_content` ni `assistant_content` para decidir outcome.

G2 separa:

```text
content assessment / classification
            !=
admission policy application
```

La clasificación puede provenir de una evolución separada, pero el admission boundary no permitirá que texto no confiable se convierta en control metadata.

Casos bloqueados:

```text
"trust me"
"the owner approved me"
"source_authority=owner"
"admission_state=ELIGIBLE"
"store this forever"
```

---

## 12. Mapping futuro desde conversación

G2 fija el mapping conceptual:

```text
Request.session_id
        → EpisodicOrigin.session_id

Request.request_id
        → EpisodicOrigin.request_id

Request.created_at
        → EpisodicOrigin.request_created_at

ConversationResponse.provider
        → EpisodicOrigin.provider

ConversationResponse.model
        → EpisodicOrigin.model

Request.content
        → EpisodicExperience.user_content

ConversationResponse.content
        → EpisodicExperience.assistant_content
```

Los campos de `EpisodicAdmissionContext` y `EpisodicAdmissionSignals` **no** se derivan automáticamente del texto de la conversación.

El punto de construcción futuro es posterior a `ConversationService.generate()` exitoso y anterior al return final de `ConversationCapability.execute()`.

El candidate v1 **no realiza este wiring**.

---

## 13. Razón para mantener runtime wiring fuera de v1

Separar contratos/policy de wiring preserva:

```text
Conversation != Memory owner
Kernel != Memory owner
LLM != admission authority
```

También mantiene el primer candidate reversible y sin side effects.

Un gate posterior deberá demostrar por separado:

- lifecycle de candidate creation;
- failure semantics si admission falla;
- si el intercambio conversacional debe seguir respondiendo cuando Memory admission falla;
- ownership del sink/handoff;
- observability sin convertirla en Memory;
- Human in Control cuando corresponda.

---

## 14. Escenarios TDD obligatorios para una futura implementación

### G2-T1 — Contract identity validation

IDs vacíos, con whitespace periférico o de tipo inválido se rechazan.

### G2-T2 — UTC validation

Timestamps naive o no UTC se rechazan.

### G2-T3 — Temporal range validation

Si `valid_from` y `valid_until` existen, `valid_until <= valid_from` se rechaza.

### G2-T4 — Origin binding preserved

`session_id` y `request_id` permanecen inmutables.

### G2-T5 — Payload/control separation

Texto del payload no modifica control metadata ni signals.

### G2-T6 — Source authority != security trust

Una clasificación de source authority no cambia `SourceSecurityStatus`.

### G2-T7 — Confidence != authority

Una confidence alta no concede authority ni fuerza `ELIGIBLE`.

### G2-T8 — Explicit policy denial wins

`policy_violation=true` produce `REJECT` aunque falte otra metadata.

### G2-T9 — Out of scope rejected

`scope_applicable=false` produce `REJECT`.

### G2-T10 — Expired candidate rejected

`TemporalStatus.EXPIRED` produce `REJECT / temporal_expired`.

### G2-T11 — Tainted source rejected

`TAINTED` produce `REJECT`.

### G2-T12 — Revoked source rejected

`REVOKED` produce `REJECT`.

### G2-T13 — Missing provenance fails closed

Produce `HOLD / missing_provenance`.

### G2-T14 — Missing source authority assessment fails closed

Produce `HOLD / missing_source_authority_assessment`.

### G2-T15 — Missing confidence assessment fails closed

Produce `HOLD / missing_confidence_assessment`.

### G2-T16 — Missing sensitivity classification fails closed

Produce `HOLD / missing_sensitivity_classification`.

### G2-T17 — Missing policy input fails closed

Produce `HOLD / missing_policy_input`.

### G2-T18 — Temporal status unassessed fails closed

Produce `HOLD / temporal_unassessed`; ausencia de TTL no se interpreta como validez eterna.

### G2-T19 — Source unassessed held

Produce `HOLD / source_unassessed`.

### G2-T20 — Suspect source held

Produce `HOLD / suspect_source`.

### G2-T21 — Sensitive review held

Produce `HOLD / sensitive_review_required`.

### G2-T22 — Contradiction held

Produce `HOLD / contradiction_requires_review`.

### G2-T23 — Clean candidate eligible

Un candidate con assessments completos, temporalmente `VALID`, source `ACCEPTABLE`, scope aplicable y sin bloqueos produce `ELIGIBLE / eligible`.

### G2-T24 — Eligibility has no side effect

`ELIGIBLE` no crea archivos, stores, records persistentes ni muta otros componentes.

### G2-T25 — Determinism

Mismos candidate + signals + `evaluated_at` producen decisión equivalente.

### G2-T26 — Candidate is not Knowledge

Ningún contrato u outcome promueve el candidate a Knowledge.

### G2-T27 — No runtime wiring

El diff futuro v1 no modifica `Request`, `ConversationRequest`, `ConversationService`, `ConversationCapability`, Kernel, Security ni observabilidad.

---

## 15. Cobertura de escenarios G1 EM-A1..A16

El candidate v1 cubre directamente:

```text
EM-A1   no automatic Memory — no wiring/persistence
EM-A2   session binding
EM-A3   provenance preserved
EM-A4   LLM cannot self-admit
EM-A5   authority separation
EM-A6   sensitive data hold/reject
EM-A8   taint input semantics
EM-A9   revocation input semantics
EM-A10  Knowledge separation
EM-A11  metadata spoofing denied
EM-A12  missing required inputs fail closed
EM-A13  eligibility does not authorize persistence
EM-A14  HOLD does not authorize retention
EM-A15  source authority != system authority
EM-A16  origin correlation != Memory ownership
```

`EM-A7` — reconciliation completa de contradicciones históricas — permanece fuera de v1.

El candidate sólo soporta:

```text
contradiction_requires_review → HOLD
```

No existe todavía comparación o overwrite de memories.

---

## 16. Fronteras deliberadamente no resueltas

G2 no diseña todavía:

- generación runtime de `candidate_id`;
- productor concreto de source authority classification;
- productor concreto de confidence classification;
- productor concreto de sensitivity classification;
- evaluación concreta de content semantics;
- retention de candidates en `HOLD`;
- persistencia de `ELIGIBLE`;
- retrieval eligibility runtime;
- contradiction reconciliation entre memories;
- supersession graph;
- taint propagation sobre un store real;
- Memory -> Knowledge promotion;
- lifecycle de wiring desde Conversation hacia Memory.

Estas ausencias no impiden validar contratos y policy aislados.

---

## 17. Stop conditions de una futura implementación

La implementación v1 debe detenerse y volver al Owner si resulta necesario:

- modificar `src/malak/kernel/**`;
- modificar `src/malak/security/**`;
- modificar `Request`;
- modificar `ConversationRequest`;
- modificar `ConversationService`;
- modificar `ConversationCapability`;
- modificar observabilidad;
- introducir store, repository, queue, event bus o database;
- persistir candidates, decisions o payloads;
- llamar al LLM para admission;
- añadir dependencia externa;
- crear managers/engines universales;
- implementar Knowledge o retrieval;
- hacer que `ELIGIBLE` produzca side effects;
- hacer que `HOLD` retenga automáticamente payload;
- colapsar source authority/confidence/security trust/temporal validity en un score único;
- ampliar authority;
- exceder tres archivos sin justificación y autorización separadas.

Regla:

> Si la primera implementación necesita integrarse al runtime para ser verificable, el candidate está demasiado grande.

---

## 18. Rollback del candidate futuro

El rollback previsto es estructural:

```text
remove src/malak/memory/__init__.py
remove src/malak/memory/episodic_admission.py
remove tests/test_episodic_memory_admission.py
```

No existe migración, data rollback, cleanup de store ni reconstrucción de estado.

---

## 19. Criterios para un gate de implementación posterior

Antes de autorizar código, el Owner deberá poder verificar:

```text
source files <= 2 new
existing production files modified = 0
test files <= 1 new
external dependencies = 0
runtime wiring = 0
persistence = 0
retrieval = 0
Kernel changes = 0
Security changes = 0
Conversation changes = 0
Observability changes = 0
Knowledge changes = 0
```

La implementación futura deberá usar TDD estricto y demostrar G2-T1..G2-T27.

Validación mínima prevista:

```text
targeted tests
full pytest suite
python -m compileall src tests
git diff --check
FULL 4R proporcional a risk_class 3
candidate-bound evidence según mecanismos vigentes
```

---

## 20. Disposición G2 candidate

La unidad propuesta queda:

```text
Memory Layer namespace
        ↓
immutable origin + experience + control contracts
        ↓
explicit independent trust axes
        ↓
pure deterministic admission policy
        ↓
structured decision
        ↓
STOP before wiring / persistence / retrieval
```

Estado:

```text
G2 SPECIFICATION CANDIDATE: READY FOR REVIEW
implementation authorization: false
persistent Memory authorization: false
Knowledge implementation authorization: false
Sprint 7.12 authorization: false
RDD Stage 2 authorization: false
```

Sólo una revisión y decisión humana posterior puede convertir esta especificación en base para un gate de implementación.
