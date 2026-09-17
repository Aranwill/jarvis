---
id: MALAK-G2P-B-PERSISTENCE-AUTHORIZATION-COMPOSITION-DESIGN
title: "G2P-B — Composición de solicitud de autorización para persistencia episódica"
status: g2p_b_design_candidate
authority: non_normative_candidate
date: 2026-09-17
source_baseline: ed1b648c03acb40197d5eb7282a5f9babecd4073
risk_class: 3
implementation_authorized: false
security_control_plane_change_authorized: false
persistence_authorization_granted: false
protected_durable_write: false
persistent_memory: false
durable_reliance: false
rdd_stage_2_authorized: false
sprint_7_12_authorized: false
related:
  - docs/architecture/adr/ADR-002-policy-enforcement-boundary.md
  - docs/architecture/adr/ADR-006-protected-durable-reliance-preconditions.md
  - docs/governance/governance_constitution.md
  - docs/development/engineering_method.md
  - docs/project/sprints/proposals/MALAK-ADR-002-PERMISSION-OPERATION-BINDING-HARDENING-G2P-A.md
  - src/malak/memory/episodic_persistence_readiness.py
  - src/malak/security/contracts.py
  - src/malak/security/pdp.py
---

# G2P-B — Composición de solicitud de autorización para persistencia episódica

## 1. Estado y autoridad

Este documento es un **candidate de diseño no normativo**.

No modifica ADR-002 ni ADR-006, no cambia runtime y no autoriza implementación.

```text
Design candidate
!= normative acceptance
!= implementation authorization
!= Persistence Authorization grant
!= PDP ALLOW
!= Protected Durable Write
!= Persistent Memory
!= Durable Reliance
```

La autoridad efectiva permanece en las fuentes normativas aceptadas y en los gates humanos aplicables.

---

## 2. Baseline exacto

Este análisis queda ligado a:

```text
repository: Aranwill/jarvis
branch: main
baseline: ed1b648c03acb40197d5eb7282a5f9babecd4073
```

En este baseline:

- G2A ya liga request, decision y operación al mismo `AuthorizationOperationBinding` cuando la operación es bound;
- G2B ya produce `EpisodicPersistenceReadinessResult.READY` con un binding exacto y determinista del sujeto de persistencia;
- G2P-A ya exige igualdad exacta entre `AuthorizationRequest.permission` y `ProtectedOperation.required_permission` antes del PDP;
- `AuthorizationRequest` ya transporta `SecurityContext`, `PermissionScope`, `created_at` y `operation_binding`;
- el PDP conserva ownership sobre la decisión operacional;
- no existe todavía protected durable write ni Persistent Memory.

---

## 3. Necesidad demostrada

G2B responde:

```text
"¿Este candidato está listo para solicitar persistencia bajo las invariantes actuales?"
```

G2P-A responde:

```text
"¿La permission solicitada coincide con la permission requerida por la operación protegida?"
```

Falta todavía una composición explícita y gobernada que responda:

```text
"¿Cómo se construye la AuthorizationRequest exacta para solicitar permission de persistencia
 a partir de un readiness READY, sin convertir readiness en autorización?"
```

Hoy esa composición podría quedar dispersa entre callers y permitir variaciones de permission, binding o temporalidad.

---

## 4. Threat model

### T1 — Readiness laundering

Interpretar `READY` como si fuera autorización concedida.

```text
READY != authorization
```

### T2 — Permission selection by caller

Permitir que un caller elija una `PermissionScope` distinta de la capacidad de persistencia episódica.

```text
caller-selected permission
+ valid readiness binding
!= valid persistence authorization request
```

### T3 — Binding substitution

Construir una request con un binding distinto del binding emitido por el readiness exacto.

```text
readiness.binding X
request.binding Y
-> invalid composition
```

### T4 — Temporal laundering

Construir una request con `created_at` fuera de la ventana temporal declarada por el `SecurityContext`.

### T5 — Domain leakage into Security

Mover semántica de Memory, `purpose`, `domain`, `subject_scope` o lifecycle al PDP/PEP.

### T6 — Authorization laundering into durable effect

Interpretar una request bien compuesta, o incluso un futuro PDP `ALLOW`, como autorización para escribir durablemente sin pasar por un gate operativo posterior.

### T7 — Reliance laundering

Interpretar permission de persistencia como permission de reutilización o durable reliance posterior.

```text
permission to persist != permission to rely
```

---

## 5. Invariantes de G2P-B

```text
G2PB-I1  readiness READY
          != authorization

G2PB-I2  composed AuthorizationRequest
          != PDP decision

G2PB-I3  PDP ALLOW
          != Protected Durable Write

G2PB-I4  permission to persist
          != permission to rely

G2PB-I5  request.permission
          == PermissionScope("memory.episodic", "persist")

G2PB-I6  request.operation_binding
          == readiness.authorization_operation_binding

G2PB-I7  request.context
          == exact SecurityContext supplied to composition

G2PB-I8  context.issued_at
          <= request.created_at
          < context.expires_at

G2PB-I9  non-READY readiness
          -> no AuthorizationRequest

G2PB-I10 composition
           -> no side effect

G2PB-I11 Memory composer
           != upstream authorization initiation

G2PB-I12 successful composition or PDP ALLOW
           != durable freshness proof
```

---

## 6. Decisión candidata D1 — composición sin side effects

Se propone una única función de composición de dominio Memory, sin side effects observables:

```python
compose_episodic_persistence_authorization_request(
    readiness: EpisodicPersistenceReadinessResult,
    security_context: SecurityContext,
    created_at: datetime,
) -> AuthorizationRequest
```

La función solo compone contratos existentes.

No:

```text
calls PDP
calls PEP
persists data
opens files
writes storage
retries
creates sessions
mutates readiness
mutates SecurityContext
```

La construcción puede utilizar el `request_id` generado por el contrato vigente de `AuthorizationRequest`.

Ese identificador:

```text
request_id
!= idempotency key
!= anti-replay token
!= proof of authorization
```

G2P-B no introduce un generador propio de IDs ni permite al caller seleccionar `request_id` como mecanismo de autoridad.

---

## 7. Decisión candidata D2 — permission fija y no inyectable

La permission de G2P-B queda fijada por la specification:

```python
PermissionScope(
    resource="memory.episodic",
    action="persist",
)
```

El caller no puede aportar ni sobrescribir esa permission.

No se agregan a `PermissionScope`:

```text
candidate_id
domain
subject_scope
purpose
content digest
retention
storage target
policy version
```

Esos elementos pertenecen al exact operation subject o a lifecycle/policies futuras.

---

## 8. Decisión candidata D3 — readiness debe ser READY y bound

La composición solo es válida cuando:

```text
readiness.outcome == READY
AND readiness.reason_code == READY
AND readiness.authorization_operation_binding != None
```

Aunque el contrato actual de `EpisodicPersistenceReadinessResult` ya impide construir un `READY` sin binding válido, la función de composición no debe depender de coerciones ni reinterpretaciones informales.

Un readiness `HOLD` o `DENIED` falla cerrado y no produce request.

---

## 9. Decisión candidata D4 — binding exacto preservado

La request resultante debe transportar exactamente:

```text
readiness.authorization_operation_binding
```

como:

```text
AuthorizationRequest.operation_binding
```

La función no recalcula, transforma, re-hashea ni sustituye el binding.

```text
composition preserves exact binding
!= composition redefines binding semantics
```

La specification de dominio que origina el binding sigue perteneciendo a G2B/Memory.

---

## 10. Decisión candidata D5 — temporalidad de composición

`created_at` debe ser explícito, timezone-aware y temporalmente coherente con el contexto:

```text
security_context.issued_at
<= created_at
< security_context.expires_at
```

Esta comprobación demuestra **coherencia temporal de la request respecto del contexto declarado**.

No demuestra freshness operacional respecto de un reloj confiable en el momento posterior de decisión.

```text
request-time coherence
!= current PDP-time freshness
```

El PDP conserva la validación de vigencia real del `SecurityContext` mediante su `SecurityContextValidator`.

G2P-B no introduce `Clock`, TTL propio, nonce ni anti-replay durable.

Además:

```text
successful G2P-B composition
!= proof that G2B readiness remains fresh for durable execution

PDP ALLOW
!= proof that G2B readiness remains fresh for durable write
```

La freshness necesaria para un futuro efecto durable, su revalidación y cualquier protección de replay permanecen fuera de G2P-B y detrás del gate G2C.

---

## 11. Decisión candidata D6 — ownership preservado

La separación de responsabilidades queda:

```text
Memory
-> decide cómo representar el exact persistence subject
-> produce readiness y binding
-> compone la solicitud de capability exacta

Governance / authorization policy
-> decide si la capability solicitada está permitida

Security / PDP / PEP
-> valida constraints, decide/enforces según contratos vigentes

future protected durable write
-> side effect separado y todavía no autorizado
```

La composición solo puede ocurrir como retorno a una invocación autorizada proveniente de un caller/upstream competente.

```text
authorized upstream caller
-> invokes Memory composer
-> receives AuthorizationRequest as data

Memory composer
!= initiates authorization upstream
!= calls Governance
!= uses events as authorization commands
!= transfers authority
```

La composición de una request no concede autoridad a Memory ni crea control ascendente.

---

## 12. Decisión candidata D7 — ningún cambio al PDP ni a contratos Security

El baseline ya contiene contratos suficientes para G2P-B.

No se propone cambiar:

```text
PermissionScope
SecurityContext
AuthorizationRequest
AuthorizationDecision
AuthorizationOperationBinding
StaticPolicyDecisionPoint
StrictPolicyEnforcementPoint
```

STOP si durante TDD se demuestra que uno de esos contratos necesita cambiar para satisfacer una invariante de G2P-B.

Ese caso requerirá nueva revisión de alcance y autorización humana.

---

## 13. Decisión candidata D8 — ubicación de dominio

La función candidata pertenece a `malak.memory` porque fija la capability concreta de persistencia episódica y consume un resultado de readiness de Memory.

Security permanece genérico y no aprende semántica de:

```text
episodic memory
purpose
domain
subject_scope
retention
storage provider
```

Nombre de módulo candidato:

```text
src/malak/memory/episodic_persistence_authorization.py
```

Esto es una propuesta de diseño; el nombre final deberá validarse en el gate de implementación.

---

## 14. Decisión candidata D9 — no nuevo componente arquitectónico

G2P-B no justifica crear:

```text
PersistenceAuthorizationManager
AuthorizationService
MemoryAuthorizationLayer
PersistenceOrchestrator
PersistenceGateway
```

Una propiedad de composición no crea automáticamente un layer/service/manager.

---

## 15. Relación con ADR-002

G2P-B reutiliza los contratos y garantías ya aceptados por ADR-002:

```text
AuthorizationRequest.permission
AuthorizationRequest.operation_binding
SecurityContext
PDP decision
PEP enforcement
```

No cambia la frontera PDP–PEP.

No convierte `AuthorizationRequest` en autoridad.

---

## 16. Relación con ADR-006

ADR-006 preserva:

```text
Governance -> operational authorization ownership
Security   -> constraints + enforcement
Memory     -> lifecycle semantics
```

G2P-B no resuelve ni autoriza:

```text
retention
disclosure
consent
taint lifecycle
revocation lifecycle
quarantine lifecycle
durable anti-replay
idempotency
partial failure
commit acknowledgement
recovery
Persistent Memory
Durable Reliance
```

En particular:

```text
Persistence Authorization request
!= Persistent Memory readiness

permission to persist
!= permission to rely
```

---

## 17. Secuencia de construcción preservada

```text
G2A    exact operation-subject binding          INTEGRATED
G2B    episodic persistence readiness            INTEGRATED
G2P-A  permission-to-operation binding           INTEGRATED
G2P-B  persistence authorization composition     THIS CANDIDATE
G2C    protected durable write                   STOP
```

`G2P-B` continúa siendo working label de construcción, no taxonomía normativa nueva.

---

## 18. Alcance futuro de implementación candidato

Si un gate humano posterior autoriza TDD/implementación, el presupuesto inicial candidato será:

```text
ADD src/malak/memory/episodic_persistence_authorization.py
MOD src/malak/memory/__init__.py            # solo export si se demuestra necesario
ADD tests/test_episodic_persistence_authorization.py
```

Quedan fuera de alcance sin STOP + nueva aprobación:

```text
src/malak/security/**
src/malak/kernel/**
src/malak/conversation/**
src/malak/knowledge/**
storage providers
database/filesystem writes
PDP rules
PEP behavior
Persistent Memory
Protected Durable Write
RDD Stage 2
Sprint 7.12
```

No se presupone que `__init__.py` deba cambiar; la necesidad deberá demostrarse.

---

## 19. Matriz TDD futura — composición

Si se autoriza implementación, RED deberá demostrar como mínimo:

```text
C1  READY válido + SecurityContext coherente
    -> produce AuthorizationRequest

C2  permission exacta
    -> resource == "memory.episodic"
    -> action == "persist"

C3  caller no puede seleccionar permission alternativa

C4  request.operation_binding
    == readiness.authorization_operation_binding

C5  request.context
    == SecurityContext exacto suministrado

C6  HOLD
    -> BLOCK / no request

C7  DENIED
    -> BLOCK / no request

C8  readiness de tipo inválido
    -> fail closed

C9  SecurityContext de tipo inválido
    -> fail closed

C10 created_at naive
    -> fail closed

C11 created_at < context.issued_at
    -> fail closed

C12 created_at >= context.expires_at
    -> fail closed

C13 READY binding se preserva sin recomputación

C14 composición no consulta PDP

C15 composición no ejecuta PEP

C16 composición no produce side effects de persistencia
```

---

## 20. Tests de frontera / regresión futuros

La implementación deberá demostrar además que:

```text
R1  no cambia contratos Security públicos
R2  no cambia comportamiento del PDP
R3  no cambia comportamiento del PEP
R4  no cambia G2B readiness/binding
R5  no introduce Clock/TTL/nonce/replay semantics nuevas
R6  no crea durable write
R7  no crea persistence storage
```

---

## 21. Full 4R requerido

Risk class: **3 — HIGH**.

Por tratar autorización y persistencia sensible, cualquier candidate runtime deberá recibir FULL 4R:

```text
Risk
Readability
Reliability
Resilience
```

El review debe ser candidate-bound y posterior al GREEN.

---

## 22. Las cuatro preguntas obligatorias

### 1. ¿Respeta el Blueprint?

**PASS preliminar.**

No requiere nuevo layer/service/manager ni altera Kernel.

### 2. ¿Respeta la Constitución Cognitiva?

**PASS preliminar.**

Readiness no se convierte en trust, persistence no se convierte en reliance y el material no adquiere autoridad por ser retenible.

### 3. ¿Respeta la Constitución de Gobernanza?

**PASS preliminar.**

La función candidata compone una solicitud; no decide ni ejecuta. El Owner/Governance y la policy de autorización conservan autoridad.

### 4. ¿Mantiene/preserva/reduce la complejidad del Kernel?

**PASS preliminar.**

Delta Kernel esperado: `0`.

---

## 23. Criterios de aceptación del candidate de diseño

- [ ] La composición permanece diferenciada de autorización y ejecución.
- [ ] `READY` nunca se interpreta como `ALLOW`.
- [ ] La permission queda fija en `memory.episodic/persist`.
- [ ] El binding de G2B se preserva exactamente.
- [ ] `SecurityContext` se preserva exactamente.
- [ ] La temporalidad de request se valida sin duplicar freshness operacional del PDP.
- [ ] No se modifican contratos Security ni PDP/PEP.
- [ ] No existe side effect durable.
- [ ] `permission to persist != permission to rely` permanece explícito.
- [ ] G2C continúa en STOP.
- [ ] Memory no inicia autorización ni control ascendente; solo devuelve la request como dato a un caller autorizado.
- [ ] `request_id` no se interpreta como idempotency key, anti-replay token ni autoridad.
- [ ] Composición exitosa o futuro PDP `ALLOW` no prueban freshness suficiente para durable write.
- [ ] La futura implementación queda sujeta a TDD RED/GREEN y FULL 4R.
- [ ] Se requiere aprobación humana explícita antes de crear tests o runtime.

---

## 24. Rollback conceptual

Mientras este documento permanezca como candidate no normativo, rollback significa:

```text
close/reject candidate
+ no implementation
+ baseline runtime unchanged
```

No existe rollback de datos ni de estado durable porque G2P-B todavía no introduce side effects.

---

## 25. Disposición

```text
G2P-B design candidate: CREATED
implementation: NOT AUTHORIZED
tests: NOT STARTED
runtime: UNCHANGED
G2C: STOP
Protected Durable Write: NOT AUTHORIZED
Persistent Memory: NOT AUTHORIZED
Durable Reliance: NOT AUTHORIZED
```
