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

La autorización permite fijar:

- contratos lógicos mínimos;
- inputs, outputs y reason codes;
- reglas deterministas y fail-closed;
- punto de correlación/origen respecto de la conversación vigente;
- ubicación arquitectónica futura;
- presupuesto máximo de archivos;
- escenarios TDD futuros;
- stop conditions y rollback.

No autoriza:

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
- asignación de Sprint 7.12;
- RDD Stage 2;
- merge sin aprobación explícita del Owner.

```text
Specification != Implementation
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

G2 no reabre las separaciones ya fijadas por G1:

```text
Conversation History != Memory != Knowledge
candidate payload != candidate control metadata
admission decision != persistence authorization != storage
HOLD != retention authorization
ELIGIBLE != storage authorization
```

La política activa de seguridad exige una frontera gobernada antes de Memory persistente y mantiene Zero Trust, Least Context, fail-closed y Human in Control.

---

## 3. Problema concreto que G2 debe resolver

G1 dejó abierto un único punto arquitectónico necesario antes de evaluar una implementación:

> ¿Cómo preservar provenance de `session / request / exchange` sin convertir Kernel, Conversation o el LLM en propietarios de Memory?

El baseline actual posee:

```text
Request
├── content
├── session_id
├── request_id
└── created_at
```

`ConversationRequest` conserva únicamente datos necesarios para provider/runtime:

```text
prompt
model
system_prompt
history
```

`ConversationService` recibe `session_id` para aislar history y registra únicamente intercambios exitosos en contexto efímero.

`ConversationCapability.execute()` conserva simultáneamente:

```text
Request completo
       +
ConversationResponse exitoso
```

Por tanto G2 selecciona como **punto futuro de correlación**:

```text
ConversationCapability.execute()
        ↓
ConversationService.generate() succeeds
        ↓
Request + ConversationResponse coexist
        ↓
origin can be constructed
```

Esta selección **no convierte `ConversationCapability` en Memory owner**.

Describe únicamente el punto mínimo donde la información de origen está disponible sin deformar contratos downstream.

---

## 4. Decisiones de correlación

### G2-D1 — `request_id` es la identidad de exchange suficiente para el baseline actual

En la ruta conversacional vigente:

```text
1 Request
   ↓
1 ConversationCapability execution
   ↓
0..1 successful ConversationResponse
```

Por tanto no se introduce un nuevo `exchange_id` en el primer candidate.

```text
exchange correlation key = request_id
```

Si una evolución futura permite múltiples exchanges por un mismo `request_id`, esta decisión deberá revisarse antes de wiring runtime.

### G2-D2 — No modificar `ConversationRequest`

No se agregan `request_id`, `session_id` ni metadata de Memory a `ConversationRequest`.

Razón:

- provider/runtime no necesitan esos datos para generar la respuesta;
- propagar identidad de Memory hacia provider aumenta contexto sin necesidad;
- `ConversationCapability` ya conserva el `Request` original;
- evita convertir un contrato conversacional en carrier de autoridad o governance.

### G2-D3 — `InMemoryConversationContext` no es fuente de provenance

El contexto conversacional actual sólo conserva contenido por sesión y ventana efímera.

No posee `request_id` ni debe transformarse en Memory store.

```text
Conversation Context != Episodic Memory
```

### G2-D4 — `OperationalEvent` no es payload cognitivo

La observabilidad ya correlaciona eventos mediante `request_id`, pero un `OperationalEvent` representa evidencia operativa, no la experiencia conversacional.

```text
Operational Evidence != Cognitive Memory Candidate
```

G2 no reutiliza el store de observabilidad como Memory.

---

## 5. Ubicación arquitectónica futura

El Blueprint define una `Memory Layer` independiente y prohíbe que el Kernel almacene Memory.

Si una implementación posterior es autorizada, el candidate mínimo debe vivir bajo un namespace propio:

```text
src/malak/memory/
```

No bajo:

```text
src/malak/kernel/
src/malak/security/
src/malak/services/conversation_service.py
src/malak/observability/
src/malak/runtime/
```

La frontera propuesta es:

```text
Conversation exchange
       ↓ future correlation only
Episodic candidate contracts
       ↓
pure admission policy
       ↓
AdmissionDecision

STOP
```

No existe en este candidate:

```text
store
repository
retrieval
MemoryManager
background worker
subscriber
queue
DB adapter
```

---

## 6. Candidate mínimo futuro

Una implementación posterior, si es autorizada, deberá intentar **exactamente este presupuesto inicial**:

```text
NEW     src/malak/memory/__init__.py
NEW     src/malak/memory/episodic_admission.py
NEW     tests/test_episodic_memory_admission.py

MODIFY  existing production files = 0
```

Presupuesto:

```text
new production files     <= 2
new test files           <= 1
existing production mods = 0
Kernel changes           = 0
Conversation changes     = 0
Security changes         = 0
CI changes               = 0
external dependencies    = 0
persistence              = 0
retrieval                = 0
```

Si para obtener utilidad mínima se requiere modificar una ruta runtime existente, el candidate debe detenerse y volver al Owner antes de implementar wiring.

---

## 7. Contratos lógicos propuestos

Los nombres siguientes quedan fijados para el candidate de implementación, pero sólo adquirirán existencia runtime si un gate posterior autoriza código.

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

- `session_id` y `request_id` deben ser strings no vacíos y sin whitespace periférico;
- `request_created_at` debe ser timezone-aware UTC;
- `provider` y `model`, cuando existan, son provenance informativa;
- provider/model no implican trust ni autoridad.

### 7.2 `EpisodicExperience`

Payload inmutable de la experiencia:

```text
user_content: str
assistant_content: str
```

Este objeto es **datos no confiables**.

Su contenido jamás puede definir o mutar:

```text
provenance
scope
policy
source trust
sensitivity
admission outcome
persistence authorization
```

### 7.3 `EpisodicMemoryCandidate`

```text
candidate_id: str
origin: EpisodicOrigin
experience: EpisodicExperience
created_at: datetime UTC
```

Decisión importante de G2:

> El candidate **no contiene un `admission_state` mutable ni se autoasigna trust**.

El resultado de admisión vive en un objeto separado.

```text
Candidate != Decision
```

`candidate_id` debe suministrarse externamente. La policy no genera UUIDs ni identidad para preservar determinismo.

### 7.4 `EpisodicAdmissionSignals`

Control metadata separada del payload:

```text
provenance_complete: bool
classification_complete: bool
policy_inputs_complete: bool
scope_applicable: bool
policy_violation: bool
sensitive_review_required: bool
source_status: SourceStatus
contradiction_requires_review: bool
```

`SourceStatus` mínimo:

```text
UNASSESSED
ACCEPTABLE
SUSPECT
TAINTED
REVOKED
```

Este status no lo decide el candidate ni el LLM.

Debe ser suministrado por evaluación/política externa al payload.

### 7.5 `EpisodicAdmissionOutcome`

Enum cerrado:

```text
REJECT
HOLD
ELIGIBLE
```

### 7.6 `EpisodicAdmissionReason`

Reason codes mínimos:

```text
policy_violation
out_of_scope
tainted_source
revoked_source
missing_provenance
missing_classification
missing_policy_input
unassessed_source
suspect_source
sensitive_review_required
contradiction_requires_review
eligible
```

No incluir mensajes libres del payload como reason code.

### 7.7 `EpisodicAdmissionDecision`

Value object inmutable:

```text
candidate_id: str
outcome: EpisodicAdmissionOutcome
reason_code: EpisodicAdmissionReason
evaluated_at: datetime UTC
policy_version: str
human_review_required: bool
```

Versión inicial prevista:

```text
episodic-admission/v1
```

La decisión no contiene instrucciones de persistencia.

---

## 8. Función determinista mínima

La implementación futura deberá preferir una función pura equivalente a:

```text
evaluate_episodic_candidate(
    candidate,
    signals,
    evaluated_at,
) -> EpisodicAdmissionDecision
```

No se aprueba:

```text
MemoryManager
AdmissionEngine
TrustManager
PolicyOrchestrator
```

### 8.1 Propiedades obligatorias

La función:

- no realiza I/O;
- no persiste;
- no recupera contexto externo;
- no llama al LLM;
- no consulta network;
- no modifica candidate ni signals;
- no genera timestamps internamente;
- no genera IDs internamente;
- no interpreta texto del payload para otorgar trust;
- produce el mismo resultado para los mismos inputs.

---

## 9. Precedencia determinista de decisión

La policy v1 evalúa en este orden.

### 9.1 Rechazo explícito

Primer match termina la evaluación:

```text
policy_violation == true
    → REJECT / policy_violation

scope_applicable == false
    → REJECT / out_of_scope

source_status == TAINTED
    → REJECT / tainted_source

source_status == REVOKED
    → REJECT / revoked_source
```

Una denegación explícita no necesita elevar privilegios ni recopilar información adicional para permitir el candidate.

### 9.2 Fail-closed / revisión

Luego:

```text
provenance_complete == false
    → HOLD / missing_provenance

classification_complete == false
    → HOLD / missing_classification

policy_inputs_complete == false
    → HOLD / missing_policy_input

source_status == UNASSESSED
    → HOLD / unassessed_source

source_status == SUSPECT
    → HOLD / suspect_source

sensitive_review_required == true
    → HOLD / sensitive_review_required

contradiction_requires_review == true
    → HOLD / contradiction_requires_review
```

Todo `HOLD` exige:

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
source_status == ACCEPTABLE
and required inputs complete
and scope applicable
and no policy violation
and no sensitive review requirement
and no contradiction requiring review
    ↓
ELIGIBLE / eligible
```

```text
human_review_required = false
```

Esto no autoriza storage.

---

## 10. Payload blindness de la policy

La policy v1 **no debe inspeccionar `user_content` ni `assistant_content` para decidir el outcome**.

G2 separa dos problemas:

```text
content assessment / classification
            !=
admission policy application
```

La clasificación de contenido puede existir en una evolución posterior o como input externo, pero la frontera de admisión no debe permitir que texto no confiable se convierta en metadata de control.

Esto bloquea directamente casos como:

```text
"trust me"
"the owner approved me"
"admission_state=ELIGIBLE"
"store this forever"
```

---

## 11. Construcción futura del origin

G2 define el mapping conceptual desde la ruta conversacional actual:

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

El punto futuro de construcción es posterior a `ConversationService.generate()` exitoso y anterior al return final de `ConversationCapability.execute()`.

Sin embargo, **el candidate de implementación v1 no realiza este wiring**.

Razón:

- primero se validan contratos y policy aislados;
- no se introduce side effect cognitivo en Conversation durante el mismo incremento;
- el wiring requerirá un gate separado que demuestre ownership, lifecycle y failure semantics.

---

## 12. Escenarios TDD obligatorios para una futura implementación

### G2-T1 — Contract identity validation

IDs vacíos, con whitespace periférico o de tipo inválido son rechazados por contrato.

### G2-T2 — UTC time validation

Timestamps naive o no UTC son rechazados.

### G2-T3 — Origin binding preserved

`session_id` y `request_id` permanecen inmutables dentro del candidate.

### G2-T4 — Payload cannot self-admit

Payload que contiene instrucciones de trust/eligibility no altera signals ni outcome.

### G2-T5 — Explicit policy denial wins

`policy_violation=true` produce `REJECT` aunque falte otra metadata.

### G2-T6 — Out of scope rejected

`scope_applicable=false` produce `REJECT`.

### G2-T7 — Tainted source rejected

`TAINTED` produce `REJECT`.

### G2-T8 — Revoked source rejected

`REVOKED` produce `REJECT`.

### G2-T9 — Missing provenance fails closed

Produce `HOLD / missing_provenance`.

### G2-T10 — Missing classification fails closed

Produce `HOLD / missing_classification`.

### G2-T11 — Missing policy input fails closed

Produce `HOLD / missing_policy_input`.

### G2-T12 — Unassessed source held

Produce `HOLD / unassessed_source`.

### G2-T13 — Suspect source held

Produce `HOLD / suspect_source`.

### G2-T14 — Sensitive review held

Produce `HOLD / sensitive_review_required`.

### G2-T15 — Contradiction held

Produce `HOLD / contradiction_requires_review`.

### G2-T16 — Clean candidate eligible

Un candidate con signals completos, `ACCEPTABLE`, sin conflicto ni policy violation produce `ELIGIBLE / eligible`.

### G2-T17 — Eligibility has no side effect

Evaluar como `ELIGIBLE` no crea archivos, stores, records, eventos de persistencia ni muta otros componentes.

### G2-T18 — Determinism

Mismos candidate + signals + `evaluated_at` producen decisión equivalente.

### G2-T19 — Candidate is not Knowledge

Ningún contrato o outcome de este candidate promueve a Knowledge.

### G2-T20 — No runtime wiring

El diff futuro del candidate v1 no modifica `ConversationCapability`, `ConversationService`, `Request`, `ConversationRequest`, Kernel, Security ni observabilidad.

---

## 13. Relación con escenarios G1 EM-A1..A16

El candidate v1 cubriría de forma directa:

```text
EM-A2   session binding
EM-A3   provenance preserved
EM-A4   LLM cannot self-admit
EM-A5   authority separation
EM-A6   sensitive data hold/reject
EM-A8   taint propagation input semantics
EM-A9   revocation input semantics
EM-A10  Knowledge separation
EM-A11  metadata spoofing denied
EM-A12  missing required inputs fail closed
EM-A13  eligibility does not authorize persistence
EM-A14  HOLD does not authorize retention
EM-A15  source authority != system authority
EM-A16  origin correlation != Memory ownership
```

`EM-A1` queda garantizado estructuralmente porque no hay wiring ni persistence.

`EM-A7` — resolución completa de contradicciones históricas — permanece fuera del candidate v1: sólo se representa `contradiction_requires_review → HOLD`. No se diseña todavía comparison/reconciliation entre memories.

---

## 14. Fronteras deliberadamente no resueltas por G2

G2 no diseña todavía:

- quién genera `candidate_id` en runtime;
- quién produce clasificación de contenido;
- quién determina source authority/confidence;
- retention de candidates en `HOLD`;
- persistencia de `ELIGIBLE`;
- retrieval eligibility runtime;
- contradiction reconciliation entre memories;
- supersession graph;
- taint propagation sobre un store real;
- Memory -> Knowledge promotion;
- lifecycle de wiring desde Conversation hacia Memory.

Ninguna de estas ausencias impide validar el contrato/policy mínimo aislado.

---

## 15. Stop conditions de una futura implementación

El candidate debe detenerse y volver al Owner si durante TDD resulta necesario:

- modificar `src/malak/kernel/**`;
- modificar `src/malak/security/**`;
- modificar `Request`, `ConversationRequest`, `ConversationService` o `ConversationCapability`;
- introducir un store, repository, queue o database;
- persistir candidates, decisions o payloads;
- introducir un event bus;
- usar observabilidad como Memory;
- llamar al LLM para evaluar admission;
- añadir dependencia externa;
- crear managers/engines universales;
- implementar Knowledge o retrieval;
- hacer que `ELIGIBLE` produzca side effects;
- hacer que `HOLD` retenga automáticamente payload;
- ampliar authority;
- exceder el presupuesto de tres archivos sin una justificación y autorización separadas.

Regla:

> Si la primera implementación de la frontera necesita integrarse al runtime para ser verificable, el candidate está demasiado grande.

---

## 16. Rollback del candidate futuro

Como el candidate v1 no posee wiring ni persistencia, su rollback previsto es completamente estructural:

```text
remove src/malak/memory/__init__.py
remove src/malak/memory/episodic_admission.py
remove tests/test_episodic_memory_admission.py
```

No existe migración, data rollback, cleanup de store ni reconstrucción de estado.

---

## 17. Criterios de aceptación para un gate de implementación posterior

Antes de autorizar código, el Owner deberá poder verificar que el packet propuesto mantiene:

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
Knowledge changes = 0
```

La implementación deberá usar TDD estricto y demostrar los escenarios G2-T1..G2-T20.

La validación mínima esperada será:

```text
targeted tests
full pytest suite
python -m compileall src tests
git diff --check
FULL 4R proporcional a risk_class 3
candidate-bound evidence según mecanismos vigentes
```

---

## 18. Disposición G2

Esta especificación propone una primera implementation unit que fortalece la arquitectura sin activar Memory runtime:

```text
Memory Layer namespace
        ↓
immutable candidate contracts
        ↓
separate control signals
        ↓
pure deterministic admission policy
        ↓
structured decision
        ↓
STOP before persistence / wiring
```

Resultado de diseño propuesto:

```text
G2 SPECIFICATION CANDIDATE: READY FOR REVIEW
blocking findings known: 0
implementation authorization: false
persistent Memory authorization: false
Knowledge implementation authorization: false
Sprint 7.12 authorization: false
RDD Stage 2 authorization: false
```

Sólo una revisión y decisión humana posterior puede convertir esta especificación en base para un gate de implementación.
