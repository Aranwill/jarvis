---
id: MALAK-ADR-002-PERMISSION-OPERATION-BINDING-HARDENING-G2P-A
title: ADR-002 Permission-to-Protected-Operation Binding Hardening — G2P-A
status: g2p_a_hardening_candidate
authority: non_normative_candidate
date: 2026-09-15
source_baseline: 869ce248f1b0bb9eafaae74ac6d82452590ad30d
risk_class: 3
implementation_authorized: false
security_control_plane_change_authorized: false
persistence_authorization: false
persistent_memory: false
protected_durable_write: false
durable_reliance: false
conversation_g2b: false
rdd_stage_2_authorized: false
sprint_7_12_authorized: false
related:
  - docs/architecture/adr/ADR-002-policy-enforcement-boundary.md
  - docs/architecture/adr/ADR-006-protected-durable-reliance-preconditions.md
  - docs/governance/governance_constitution.md
  - SECURITY.md
  - src/malak/security/contracts.py
  - src/malak/security/pdp.py
  - src/malak/security/pep.py
  - src/malak/security/audit.py
  - src/malak/memory/episodic_persistence_readiness.py
---

# ADR-002 Permission-to-Protected-Operation Binding Hardening — G2P-A

## 1. Estado y autoridad

Este documento es un **candidate de diseño no normativo**.

No modifica ADR-002, no cambia runtime y no autoriza implementación.

```text
Design candidate
!= ADR amendment
!= implementation authorization
!= Persistence Authorization
!= Protected Durable Write
!= Persistent Memory
!= Durable Reliance
```

La autoridad efectiva continúa en las fuentes normativas aceptadas y en los gates
humanos aplicables.

---

## 2. Baseline exacto

Este análisis queda ligado a:

```text
repository: Aranwill/jarvis
branch: main
baseline: 869ce248f1b0bb9eafaae74ac6d82452590ad30d
```

Baseline material relevante:

- ADR-002 v1.2.0 ya exige exact `operation_binding` entre request, decision y
  protected operation para operaciones bound.
- `AuthorizationRequest` conserva `PermissionScope` y
  `AuthorizationOperationBinding` como dimensiones distintas.
- `StaticPolicyDecisionPoint` decide con `(subject_id, PermissionScope)` y preserva
  el operation binding sin interpretar semántica de dominio.
- `StrictPolicyEnforcementPoint` valida exact operation binding, request identity,
  decisión, temporalidad y auditoría antes de ejecutar.
- G2B produce `EpisodicPersistenceReadinessResult.READY` con un
  `AuthorizationOperationBinding` exacto, pero no concede autorización.

---

## 3. Hallazgo

El hardening G2A resolvió la pregunta:

```text
"¿La autorización corresponde exactamente al sujeto material X?"
```

pero la frontera actual todavía no puede demostrar de forma estructural:

```text
"¿La PermissionScope usada para autorizar X es exactamente la PermissionScope
 que la operación protegida X requiere?"
```

Hoy existen dos dimensiones:

```text
AuthorizationRequest.permission
AuthorizationRequest.operation_binding
```

El PDP decide la permission solicitada y conserva el binding opaco.

El PEP demuestra:

```text
request.operation_binding
== decision.operation_binding
== protected_operation.authorization_binding
```

pero `ProtectedOperation` no declara actualmente una permission requerida contra la
cual el PEP pueda comparar `request.permission`.

Por tanto, el siguiente caso no está estructuralmente excluido por la frontera:

```text
protected operation actual:
    persist exact subject X

protected operation binding:
    X

AuthorizationRequest.operation_binding:
    X                  # exacto

AuthorizationRequest.permission:
    Y                  # permission distinta

PDP policy:
    subject S may Y    # ALLOW
```

En ese escenario, subject binding es correcto pero la clase de permiso puede ser
incorrecta para la operación ejecutada.

---

## 4. Threat model

### T1 — Permission laundering

Un caller usa una permission permitida distinta de la que la operación sensible
realmente requiere, conservando el binding correcto del sujeto material.

```text
correct subject binding
+ wrong permission
!= valid authorization
```

### T2 — Confused deputy

Un componente privilegiado ejecuta una operación protegida bajo una permission que
no representa la capacidad real que está ejerciendo.

### T3 — Audit ambiguity

Si la auditoría conserva únicamente la permission solicitada por la request, un
mismatch puede no dejar evidencia reconstructible de la permission que la operación
real declaraba requerir.

### T4 — Persistence-specific laundering

Un futuro protected durable write podría recibir el exact G2B operation binding pero
ser autorizado mediante una permission distinta de `memory.episodic/persist`.

### T5 — Domain leakage into Security

Una corrección incorrecta podría intentar hacer que Security interprete `purpose`,
`domain`, `subject_scope` o tipos de Memory. Eso queda prohibido por este candidate.

---

## 5. Invariantes

Este candidate congela conceptualmente las siguientes separaciones:

```text
PermissionScope
!= exact operation subject

operation binding
!= permission

permission equality
!= subject equality

subject equality
!= permission equality

Memory readiness
!= permission

PDP ALLOW
!= execution unless PEP proves exact permission + exact subject
```

Para una operación protegida que declare ambos contratos:

```text
AuthorizationRequest.permission
== ProtectedOperation.required_permission
```

Y, cuando sea bound:

```text
AuthorizationRequest.operation_binding
== AuthorizationDecision.operation_binding
== ProtectedOperation.authorization_binding
```

Ambas familias de invariantes son necesarias y no se sustituyen entre sí.

---

## 6. Decisión candidata D1 — required permission opaca para Security

Una futura operación protegida podrá exponer:

```python
required_permission: PermissionScope | None
```

Security tratará este valor de forma opaca respecto de la semántica de dominio.

El PEP solo necesita conocer:

```text
exact PermissionScope equality
```

No necesita interpretar:

```text
Memory purpose
Memory domain
subject_scope
retention policy
consent semantics
storage provider
payload schema
```

---

## 7. Decisión candidata D2 — exact request/operation permission equality

Cuando `ProtectedOperation.required_permission` exista:

```text
request.permission == operation.required_permission
```

es condición previa obligatoria para consultar al PDP y ejecutar la operación.

Mismatch:

```text
request.permission != operation.required_permission
-> BLOCK
```

No debe existir coerción, wildcard implícito, jerarquía inferida ni equivalencia
semántica informal.

```text
same-looking string
!= PermissionScope equality
```

La comparación usa el contrato normalizado `PermissionScope` existente.

---

## 8. Decisión candidata D3 — bound operation no puede omitir required permission

Para preservar compatibilidad legacy sin dejar hueco en nuevas operaciones bound:

```text
operation.authorization_binding is not None
AND operation.required_permission is None
-> BLOCK
```

La razón es directa:

```text
exact subject binding
without exact required permission
is incomplete authorization binding
```

Compatibilidad:

```text
legacy unbound operation
+ no required_permission
-> legacy semantics may continue
```

Esto no convierte legacy en referencia para nuevas operaciones sensibles.

Un futuro protected durable write deberá declarar obligatoriamente:

```text
required_permission != None
authorization_binding != None
```

---

## 9. Decisión candidata D4 — fail-closed al leer required permission

Si acceder a `protected_operation.required_permission`:

- lanza una excepción;
- devuelve un tipo distinto de `PermissionScope | None`;
- o produce estado incoherente con una operación bound;

el PEP debe fallar cerrado y la operación no se ejecuta.

Reason codes candidatos:

```text
protected_operation_permission_unavailable
invalid_protected_operation_permission
bound_operation_permission_missing
request_operation_permission_mismatch
```

---

## 10. Decisión candidata D5 — precedencia antes del PDP

La permission real requerida por la operación debe comprobarse antes de pedir una
decisión operacional al PDP.

Orden candidato:

```text
1. validate AuthorizationRequest type
2. read protected-operation required_permission
3. read protected-operation authorization_binding
4. validate required_permission type/coherence
5. validate request.permission == required_permission when declared
6. validate bound operation cannot omit required_permission
7. validate request/operation binding presence/equality
8. validate request temporal coherence
9. call trusted PDP with exact AuthorizationRequest
10. validate AuthorizationDecision type
11. validate decision.request_id == request.request_id
12. validate decision.operation_binding == request.operation_binding
13. block denied decision
14. write ALLOWED audit
15. execute protected operation once for this invocation
```

La comprobación previa evita que un ALLOW del PDP pueda convertirse después en una
señal confusa para una operación cuya permission requerida no coincide.

---

## 11. Decisión candidata D6 — audit conserva requested vs required permission

Para un mismatch, la auditoría debe poder reconstruir:

```text
requested permission
actual protected-operation required permission
exact operation binding when applicable
outcome / reason
```

La API candidata puede extender `AuthorizationAuditRecord` con un campo append-only:

```python
protected_operation_permission: PermissionScope | None = None
```

El append-only placement es importante para preservar compatibilidad posicional de
los campos públicos históricos.

La auditoría no duplica semántica de dominio ni concede autoridad.

```text
audit evidence != authorization
```

---

## 12. Decisión candidata D7 — PDP permanece genérico

No se propone cambiar la semántica del PDP.

El PDP continúa decidiendo sobre:

```text
subject_id + PermissionScope
```

y preservando el exact operation binding recibido.

Este candidate no requiere que el PDP entienda qué significa una permission para
Memory, Conversation o cualquier otro dominio.

```text
PDP generic authorization policy
!= domain lifecycle policy
```

---

## 13. Decisión candidata D8 — AuthorizationDecision no necesita duplicar permission

No se demuestra necesidad de agregar `permission` a `AuthorizationDecision` en este
gate.

Razón:

- el PEP construye la autoridad únicamente consultando directamente al PDP confiable;
- el request exacto ya contiene la permission;
- el PEP comprueba `request.permission == operation.required_permission` antes del
  PDP;
- `decision.request_id == request.request_id` preserva la correlación con la request
  consultada;
- el caller no puede inyectar una `AuthorizationDecision` al PEP.

Agregar permission a la decisión duplicaría contrato sin cerrar un threat adicional
demostrado en este incremento.

STOP si una revisión posterior demuestra que un PDP intercambiable puede producir una
decisión permission-confused pese a la consulta directa.

---

## 14. Decisión candidata D9 — no PermissionScope explosion

La futura persistence permission inicial candidata sigue siendo una clase estable:

```python
PermissionScope(
    resource="memory.episodic",
    action="persist",
)
```

No se incorporan dentro de `PermissionScope`:

```text
candidate_id
domain
subject_scope
purpose
content digest
readiness timestamp
retention duration
storage location
```

Esos elementos pertenecen al exact operation subject binding o a policies de dominio
posteriores.

```text
PermissionScope classifies the capability
operation binding identifies the exact subject
```

---

## 15. Decisión candidata D10 — composición de Persistence Authorization queda después

Una futura función de composición podrá, en un gate separado, transformar:

```text
EpisodicPersistenceReadiness READY
+ fresh SecurityContext
```

en:

```text
AuthorizationRequest(
    permission=PermissionScope("memory.episodic", "persist"),
    operation_binding=readiness.authorization_operation_binding,
    ...
)
```

Pero este candidate **no autoriza ni implementa esa composición**.

La secuencia obligatoria queda:

```text
G2A exact operation-subject binding        INTEGRATED
G2B episodic persistence readiness          INTEGRATED
G2P-A permission-to-operation binding       THIS CANDIDATE
G2P-B persistence authorization composition FUTURE GATE
G2C protected durable write                 STOP
```

`G2P-A` y `G2P-B` son working labels de construcción, no nueva taxonomía normativa.

---

## 16. Relación con Governance

La Constitución de Gobernanza conserva:

```text
user as highest operational authority
security by default
least privilege
separation of responsibilities
traceability
```

Este hardening refuerza mínimo privilegio al demostrar que la permission evaluada es
la permission exacta declarada por la operación protegida.

No transfiere autoridad a la operación protegida:

```text
operation declares required permission
!= operation grants itself permission
```

La operación solo declara el contrato que el PEP debe comparar contra la request.
El PDP sigue siendo quien decide sobre esa request.

---

## 17. Relación con ADR-006

ADR-006 conserva:

```text
Governance -> operational authorization ownership
Security   -> constraints + enforcement
Memory     -> lifecycle semantics
```

Este hardening pertenece a Security porque prueba coherencia entre:

```text
requested permission
actual protected operation
```

No resuelve ni autoriza:

```text
retention / disclosure / consent
payload identity
replay / authorization freshness
idempotency
partial failure
quarantine lifecycle
Persistent Memory
Durable Reliance
```

---

## 18. Normative path

La revisión concluye:

```text
new ADR: NOT REQUIRED
ADR-002 amendment: REQUIRED BEFORE RUNTIME IMPLEMENTATION
preferred version: 1.3.0
```

Justificación:

- el gap pertenece a la misma frontera PDP–PEP de ADR-002;
- extiende exact authorization enforcement, no crea nueva arquitectura;
- no agrega ownership al Kernel, Memory o Governance;
- no requiere nuevo layer/service/manager;
- preserva la semántica de ADR-002 v1.2 y agrega una dimensión de coherencia que hoy
  falta.

La futura enmienda v1.3 deberá ser mínima y declarar expresamente:

```text
required permission binding
!= operation subject binding

valid bound execution requires both
```

---

## 19. TDD matrix futura — PEP

Si un gate humano posterior autoriza implementación, RED deberá demostrar como mínimo:

```text
P1  legacy unbound operation without required_permission preserves legacy semantics
P2  operation required_permission exact request match -> continue
P3  request permission A + operation required permission B -> BLOCK
P4  permission mismatch -> PDP not called
P5  permission mismatch -> protected operation not executed
P6  permission property access failure -> BLOCK
P7  invalid permission property type -> BLOCK
P8  bound operation + missing required_permission -> BLOCK
P9  bound operation + exact required_permission + exact binding -> may continue
P10 exact permission + binding mismatch -> BLOCK
P11 permission mismatch + audit failure -> fail closed
P12 denied PDP decision still blocks after permission match
P13 operation failure still receives no automatic retry
P14 caller still cannot provide AuthorizationDecision
```

---

## 20. TDD matrix futura — audit

```text
A1 allowed operation records requested permission
A2 allowed operation records protected_operation_permission when declared
A3 permission mismatch records ENFORCEMENT_FAILED
A4 mismatch audit preserves requested + required permission
A5 bound operation missing required permission is auditable
A6 permission access failure is auditable without executing operation
A7 legacy positional construction remains compatible
A8 binding audit semantics from G2A remain unchanged
```

---

## 21. File budget futuro candidato

Este documento no autoriza implementación.

Si ADR-002 v1.3 es aceptada y un gate humano posterior autoriza runtime, el budget
inicial queda congelado en:

```text
MOD  src/malak/security/pep.py
MOD  src/malak/security/audit.py
MOD  tests/test_policy_enforcement_point.py
MOD  tests/test_authorization_audit.py
```

No se demuestra necesidad actual de modificar:

```text
src/malak/security/contracts.py
src/malak/security/pdp.py
src/malak/security/__init__.py
src/malak/memory/**
src/malak/app/**
Kernel
Planner
CLI
Conversation
storage
```

STOP y volver al Owner si RED demuestra que el cierre requiere ampliar ese budget a
PDP/contracts o cualquier dominio fuera de Security/tests.

---

## 22. Compatibility contract

La implementación futura deberá preservar:

```text
legacy unbound PEP behavior
existing AuthorizationRequest API
existing AuthorizationDecision API
existing HumanConfirmationEvidence semantics
existing exact operation-binding enforcement
existing audit positional compatibility
no automatic retries
caller cannot supply decisions
```

Ningún test se "arreglará" relajando fail-closed o debilitando G2A.

---

## 23. Explicitly rejected alternatives

### A. Encode required permission inside operation binding digest

Rechazada.

```text
permission
!= exact operation subject
```

Mezclarlas oscurece responsabilidades y obligaría a Security a inferir semántica desde
un digest opaco.

### B. Make PDP interpret Memory intent

Rechazada por acoplamiento inverso y violation de domain opacity.

### C. Let Memory return AUTHORIZED

Rechazada por authority laundering.

```text
Memory readiness != operational authority
```

### D. Add a PersistenceAuthorizationManager now

Rechazada: no se demuestra necesidad de nuevo layer/service/manager.

### E. Trust caller-selected PermissionScope

Rechazada por el threat central de permission laundering.

### F. Require permission only in application composition

Rechazada como garantía suficiente. Una composición correcta puede ser bypassed por
otro caller si el PEP no valida la permission contra la operación real.

---

## 24. Residuals explicitly outside G2P-A

```text
semantic Persistence Authorization policy
retention/disclosure/consent
volatile assessment max-age
actual persisted-payload identity/binding
durable anti-replay
authorization freshness beyond SecurityContext lifecycle
idempotency key / write identity
partial-failure / commit acknowledgement / recovery
quarantine/forensic retention
Persistent Memory lifecycle
Durable Reliance runtime
```

Nada de lo anterior puede interpretarse como resuelto por exact permission binding.

---

## 25. Gate disposition

```text
G2P-A architecture analysis                PASS
permission-laundering threat               CONFIRMED
new architecture component required        NO
new ADR required                           NO
ADR-002 v1.3 amendment required            YES
runtime implementation authorized          NO
Persistence Authorization authorized       NO
Protected Durable Write authorized         NO
Persistent Memory authorized               NO
Durable Reliance authorized                NO
```

---

## 26. Acceptance criteria for this design candidate

- [x] exact baseline recorded;
- [x] threat separated from G2A operation-subject binding;
- [x] Security remains domain-opaque;
- [x] Memory gains no authority;
- [x] Governance ownership preserved;
- [x] Kernel remains unchanged;
- [x] no new layer/service/manager introduced;
- [x] legacy compatibility strategy defined;
- [x] audit requirements defined;
- [x] TDD matrix frozen;
- [x] future runtime file budget frozen;
- [x] ADR path determined;
- [x] G2C remains STOP.

Human review is still required before normative amendment or implementation.
