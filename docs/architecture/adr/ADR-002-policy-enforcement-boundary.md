---
id: ADR-002
title: "Frontera de enforcement entre PDP y operación protegida"
status: accepted
date: 2026-07-26
updated: 2026-09-15
author: Hector Rodriguez
version: 1.3.0
tags:
  - security
  - authorization
  - enforcement
  - governance
related:
  blueprint: DOC-ARQ-BLUEPRINT
  sprint: SPRINT-7.5
  knowledge_model: DOC-ARQ-KNOWLEDGE-MODEL
  adr: ADR-006
graph:
  type: architecture_decision
  domain: security
  affects:
    - authorization_contracts
    - authorization_audit
    - policy_enforcement_point
    - policy_decision_point
    - protected_operations
  depends_on:
    - Blueprint
    - Cognitive Constitution
    - Governance Constitution
    - Authorization Contracts
    - Policy Decision Point
supersedes: null
superseded_by: null
---

# ADR-002 — Frontera de enforcement entre PDP y operación protegida

## Estado

Accepted.

## Contexto

El Sprint 7.5 incorporó contratos mínimos de autorización y un Policy
Decision Point determinista. Una `AuthorizationDecision` puede
construirse como cualquier otro contrato público, por lo que una frontera
de enforcement que aceptara decisiones aportadas por el llamador
permitiría presentar una decisión fabricada como autoridad válida.

La aplicación de una decisión debe permanecer separada de la decisión y
de la lógica de negocio. También debe bloquear de forma segura cualquier
fallo, tipo de respuesta inválido o asociación incongruente.

La evolución posterior de Malāk incorporó operaciones gobernadas donde ya no
alcanza con demostrar que una `AuthorizationDecision` corresponde a un
`request_id`: para side effects materialmente sensibles debe poder demostrarse
además que la request, la decisión y la operación protegida refieren al mismo
sujeto material exacto.

```text
permission class match
!= exact protected-operation subject binding

request_id match
!= material subject binding

allowed=True
!= reusable permission token
```

El hardening posterior también demuestra que exact subject binding no alcanza si
la `PermissionScope` evaluada no coincide con la permission que la operación
protegida declara requerir realmente.

```text
exact protected-operation subject binding
+ wrong permission
!= valid authorization
```

Esta ampliación endurece la misma frontera PDP–PEP. No transfiere autoridad a
Memory, al caller ni a la operación protegida.

## Decisión

El Policy Enforcement Point obtiene siempre la decisión consultando
directamente a un `PolicyDecisionPoint` confiable e inyectado. Su API no
acepta una `AuthorizationDecision` aportada por el llamador.

Antes de ejecutar una operación protegida, el PEP:

1. valida que la entrada sea una `AuthorizationRequest`;
2. solicita la decisión al PDP;
3. valida que el resultado sea una `AuthorizationDecision`;
4. verifica que `decision.request_id` coincida exactamente con la
   solicitud;
5. bloquea toda decisión denegada;
6. ejecuta la operación exactamente una vez solo ante una decisión
   válida y permitida.

Los fallos del PDP y las respuestas inválidas producen un error de
enforcement y nunca ejecutan la operación. Los errores de la operación
se propagan sin reintento automático.

### Hardening v1.2.0 — autorización ligada al sujeto exacto de operación

Para operaciones que declaren semántica bound, la autorización debe quedar
ligada explícitamente al sujeto material exacto de la operación protegida
mediante un binding Security-domain opaco y determinista.

La propiedad normativa es:

```text
AuthorizationRequest.operation_binding
== AuthorizationDecision.operation_binding
== ProtectedOperation.authorization_binding
```

cuando la operación protegida requiera binding.

El binding:

- identifica de forma determinista el sujeto material exacto según una
  specification de dominio versionada;
- es transportado por la request sobre la que decide el PDP;
- es preservado por la `AuthorizationDecision`;
- es expuesto por la operación protegida para enforcement;
- puede ser auditado sin copiar el payload sensible;
- permanece opaco para Security respecto de la semántica de Memory,
  Conversation, Knowledge u otros dominios.

Quedan prohibidas estas interpretaciones:

```text
operation binding
!= PermissionScope
!= trust
!= authenticity
!= provenance
!= semantic truth
!= authority

same permission
!= same protected subject

same request_id
!= same protected subject
```

El PDP no calcula ni reinterpreta el binding de dominio. Decide sobre la
`AuthorizationRequest` recibida y, para una request bound, la decisión debe
preservar exactamente ese mismo binding. Un PDP que devuelva un binding
faltante o diferente produce una decisión incongruente y el PEP debe bloquear.

### Asimetría bound/unbound

El PEP debe fallar cerrado si request y operación protegida no coinciden en su
semántica de binding:

```text
request bound + operation unbound  -> BLOCK
request unbound + operation bound  -> BLOCK
request bound + operation bound + mismatch -> BLOCK
request bound + operation bound + exact match -> continue
both unbound -> legacy semantics only
```

La compatibilidad unbound existe exclusivamente para operaciones legacy cuya
specification no exija binding. Una futura operación sensible puede declarar
que `None` es inválido; un protected durable write deberá hacerlo antes de ser
admitido.

### Hardening v1.3.0 — permission requerida ligada a la operación protegida

`PermissionScope` y `operation_binding` representan dimensiones distintas de la
autorización:

```text
PermissionScope
-> qué clase de capacidad se solicita

operation binding
-> sobre qué sujeto material exacto
```

Para una operación protegida que declare una permission requerida, el PEP debe
demostrar:

```text
AuthorizationRequest.permission
== ProtectedOperation.required_permission
```

La operación protegida declara la permission que requiere; no se concede a sí
misma esa permission. La autoridad continúa siendo decidida por el PDP sobre la
`AuthorizationRequest` exacta.

Quedan prohibidas estas interpretaciones:

```text
required permission declaration
!= authorization

permission equality
!= exact subject equality

exact subject equality
!= permission equality

operation binding
!= permission
```

Para una operación bound, omitir la permission requerida deja incompleta la
asociación de autorización:

```text
ProtectedOperation.authorization_binding != None
AND ProtectedOperation.required_permission == None
-> BLOCK
```

La compatibilidad legacy permanece limitada a operaciones unbound que no
declaren `required_permission`.

Security trata `required_permission` como un `PermissionScope` opaco respecto de
la semántica de dominio. No interpreta `purpose`, `domain`, `subject_scope`,
retention, consent, storage ni tipos de Memory.

El PDP permanece genérico y continúa decidiendo sobre:

```text
subject_id + PermissionScope
```

No necesita conocer la semántica interna de la operación protegida.

El PEP debe fallar cerrado cuando:

```text
required_permission no puede leerse
required_permission tiene tipo inválido
request.permission != required_permission
bound operation no declara required_permission
```

La comparación de permission requerida debe realizarse antes de solicitar una
decisión al PDP. Esta obligación no requiere alterar la comprobación temporal ya
existente: la coherencia temporal puede seguir validándose antes de la permission
si la implementación preserva fail-closed y ninguna decisión del PDP ocurre antes
de demostrar la permission correcta.

La auditoría debe permitir reconstruir, cuando aplique:

```text
requested permission
actual protected-operation required permission
requested exact subject binding
actual protected-operation binding
outcome / reason
```

La igualdad estructural tampoco demuestra que una implementación defectuosa haya
declarado la permission semánticamente correcta para su comportamiento real. Cada
operación sensible deberá fijar `required_permission` mediante su specification y
pruebas correspondientes.

```text
request.permission == operation.required_permission
!= proof that operation declared the semantically correct permission
```

### Human confirmation ligada al mismo sujeto

Cuando una policy requiera confirmación humana para una request bound, la
evidencia de confirmación debe quedar ligada al mismo operation binding de la
request nueva que será reevaluada por el PDP.

```text
same subject_id
+ same PermissionScope
+ matching request ids
!= confirmation for another bound operation subject
```

La confirmación humana sigue siendo evidencia para una reevaluación; no es una
`AuthorizationDecision`, no crea permiso permanente y no puede reutilizarse
como bearer token para otro sujeto material.

### Coherencia temporal de AuthorizationRequest

Una `AuthorizationRequest` debe ser temporalmente coherente con el
`SecurityContext` que declara usar:

```text
context.issued_at
<= request.created_at
< context.expires_at
```

Una request creada antes de la emisión del contexto o en/después de su
expiración es inválida.

Esta regla no introduce un TTL de autorización adicional y no constituye
protección durable contra replay.

### Auditoría bound

Para una operación bound, la auditoría de autorización debe preservar el
operation binding suficiente para identificar el sujeto exacto que fue
autorizado/enforced, sin requerir copiar el payload protegido.

La evidencia auditable debe permitir distinguir al menos:

```text
permission class
requested required permission
actual protected-operation required permission
requested exact subject binding
actual protected-operation binding
outcome / reason
```

Un mismatch de permission o binding nunca debe degradarse a un audit de
autorización permitida.

### Replay e idempotencia

`AuthorizationDecision.allowed=True` no constituye un permiso reutilizable
indefinidamente.

Esta ADR no afirma que el binding, `request_id` o `SecurityContext` actuales
resuelvan anti-replay durable.

```text
request correlation
!= durable anti-replay

operation binding
!= idempotency key

single in-process PEP execution
!= exactly-once durable effect
```

Para futuros side effects durables, freshness/replay, idempotencia,
partial-failure, commit acknowledgement y recovery deberán resolverse de forma
coordinada antes de autorizar el write. ADR-006 conserva esas precondiciones.

## Alternativas consideradas

### Aceptar una decisión aportada por el llamador

Rechazada porque permitiría fabricar una decisión permitida fuera del
PDP y puentear la frontera de autoridad.

### Integrar el enforcement directamente en el Kernel

Rechazada porque agregaría responsabilidad de seguridad operativa al
Kernel y mezclaría coordinación con decisión y ejecución.

### Incorporar ahora sesiones, firmas, TTL o prevención de replay

Rechazada para el incremento original. Los hardenings v1.2.0 y v1.3.0 tampoco
declaran resuelto replay durable: ligan autorización y ejecución al mismo sujeto
material y a la permission requerida, pero freshness/replay durable continúa
requiriendo contratos y fundamentos adicionales coordinados con la operación
concreta.

### Resolver el binding únicamente en un wrapper de dominio

Rechazada. Un wrapper Memory-local alrededor de una `AuthorizationRequest`
unbound no demuestra que el PDP haya decidido sobre el sujeto material exacto.
El binding debe formar parte de la request evaluada y ser verificado por la
frontera de enforcement.

### Hacer que Security interprete tipos de Memory

Rechazada. Introduciría acoplamiento inverso y transferiría semántica de dominio
a Security. El binding debe permanecer opaco y versionado; cada dominio es
responsable de derivarlo/recomputarlo desde el material real que protege.

### Confiar en la PermissionScope seleccionada por el caller

Rechazada. Permitiría permission laundering: un caller podría conservar el exact
operation binding pero solicitar una permission distinta que el PDP sí permita.
La permission debe contrastarse con la operación protegida real en el PEP.

### Codificar la permission dentro del operation binding

Rechazada. `PermissionScope` y exact operation subject representan propiedades
diferentes. Mezclarlas dentro de un digest opaco perdería claridad de
responsabilidades y no reemplaza la comparación estructural de permission.

## Consecuencias

### Positivas

- La decisión y su aplicación permanecen separadas.
- El llamador no puede aportar una decisión fabricada a la API del PEP.
- La asociación entre solicitud y decisión es explícita.
- Las operaciones bound agregan asociación explícita con el sujeto material
  exacto que será ejecutado.
- La permission evaluada puede quedar ligada a la permission que la operación
  protegida declara requerir.
- La confirmación humana no puede interpretarse como permiso para otro sujeto
  bound de la misma clase.
- La auditoría puede conservar qué permission y qué sujeto exactos fueron
  autorizados sin copiar el payload.
- Los fallos del PDP, las decisiones incongruentes, permission mismatches y
  binding mismatches bloquean la ejecución.
- El Kernel permanece intacto.

### Negativas y límites

- La confianza en el PDP depende de la composición que lo inyecta.
- El binding requiere una specification de dominio que defina material exacto,
  canonicalización, versión y algoritmo aceptado.
- Cada operación sensible deberá declarar correctamente su `required_permission`;
  igualdad estructural no demuestra corrección semántica de esa declaración.
- Equality de bindings no demuestra trust, autenticidad ni verdad semántica.
- El hardening no impide replay durable por sí mismo.
- Un durable write futuro deberá resolver además idempotencia y fallos parciales.
- No existe todavía integración con Persistent Memory ni protected durable write.

Nota de evolución: la limitación de auditoría del ADR original describía
correctamente el estado al aprobar ADR-002. Posteriormente, el Sprint 7.5
incorporó contratos de auditoría mediante la PR #22 y su integración fail-closed
con el PEP mediante la PR #23. v1.2.0 extiende la propiedad arquitectónica para
que una futura operación bound preserve también la identidad exacta del sujeto
en esa evidencia. v1.3.0 extiende la misma frontera para preservar también la
coherencia entre la permission solicitada y la permission requerida por la
operación protegida.

### Riesgos

- Una composición futura podría inyectar un PDP no confiable.
- Una operation implementation defectuosa podría declarar un binding que no
  corresponda al payload real; cada dominio sensible debe definir cómo deriva o
  recomputa el binding desde el estado realmente ejecutado.
- Una operation implementation defectuosa podría declarar una
  `required_permission` que no represente su semántica real; la specification y
  los tests de la operación deben cerrar esa brecha.
- Una operación no idempotente puede fallar después de iniciarse; el PEP no debe
  reintentarla automáticamente.
- Confundir operation binding con replay protection produciría una garantía
  falsa.
- Integrar rutas operativas durables antes de resolver lifecycle, replay,
  idempotencia y partial-failure ampliaría prematuramente la superficie de riesgo.

## Impacto arquitectónico

La decisión conserva la frontera existente en `malak.security` mediante:

- `PolicyEnforcementPoint`;
- `StrictPolicyEnforcementPoint`;
- `ProtectedOperation`;
- `AuthorizationDeniedError`;
- `AuthorizationEnforcementError`.

v1.2.0 autoriza como dirección arquitectónica una evolución compatible de los
contratos Security para representar y propagar un operation binding opaco en:

- `AuthorizationRequest`;
- `AuthorizationDecision`;
- `HumanConfirmationEvidence` cuando aplique;
- `ProtectedOperation` / enforcement;
- `AuthorizationAuditRecord` para operaciones bound.

v1.3.0 autoriza como dirección arquitectónica una evolución compatible de la
misma frontera para:

- exponer `ProtectedOperation.required_permission` cuando aplique;
- comparar en el PEP la permission solicitada contra la requerida por la
  operación protegida;
- exigir `required_permission` en nuevas operaciones bound;
- preservar requested vs protected-operation permission en auditoría cuando
  aplique.

No se demuestra necesidad de cambiar la semántica del PDP ni de agregar
`permission` a `AuthorizationDecision` en este incremento.

Esta aceptación arquitectónica no constituye por sí misma autorización de
implementación. No autoriza Persistence Authorization, Persistent Memory,
Protected Durable Write, Durable Reliance runtime, Conversation G2B, RDD Stage 2
o Sprint 7.12.

No se agrega responsabilidad al Kernel, Planner, CLI, runtimes ni Capability
Registry, ni se crea un nuevo layer/service/manager.

## Relación con Gobernanza

- Blueprint: verifica autorización antes de ejecutar y conserva el
  Kernel sin lógica de negocio.
- Constitución Cognitiva: el enforcement es determinista y no depende
  de LLM.
- Constitución de Gobernanza: aplica seguridad por defecto, mínimo
  privilegio, separación de responsabilidades, trazabilidad y control humano.
- ADR-006: los hardenings satisfacen precondiciones arquitectónicas de exact
  operation-subject binding y de coherencia entre permission solicitada y
  operación protegida, pero no declaran satisfechas freshness/replay,
  retention/disclosure/consent, idempotencia o partial-failure de un futuro
  durable write.
- Kernel First: no agrega responsabilidades al Kernel.

## Compatibilidad con AKS / GraphRAG

La ADR conserva un identificador permanente, dominio `security`, relaciones
explícitas y una lista acotada de componentes afectados. No incorpora GraphRAG
ni cambia las reglas del AKS.

El Decision Index no requiere una nueva entrada porque ADR-002 mantiene título,
identidad y estado `Accepted`; esta modificación es una evolución versionada de
la misma decisión.

## Criterios de aceptación

Criterios ya materializados por el incremento original:

- [x] La decisión no puede ser aportada por el llamador.
- [x] El PEP consulta directamente al PDP inyectado.
- [x] Las decisiones denegadas o incongruentes bloquean la operación.
- [x] Los fallos del PDP producen comportamiento fail-closed.
- [x] La operación se ejecuta una sola vez por invocación del PEP ante
  autorización válida.
- [x] No existen reintentos automáticos.
- [x] Kernel, Planner, CLI y runtimes permanecen intactos.

Requisitos arquitectónicos aceptados por v1.2.0 para una futura implementación
bound:

- [x] Request, decision y operación protegida deben referir al mismo operation
  binding exacto.
- [x] El binding es opaco para Security y no transfiere trust/authority.
- [x] Bound/unbound mismatch debe fallar cerrado.
- [x] Human confirmation debe conservar exact binding cuando aplique.
- [x] AuthorizationRequest debe ser temporalmente coherente con su
  SecurityContext.
- [x] Audit debe poder registrar el sujeto exacto de una operación bound.
- [x] Replay durable e idempotencia permanecen explícitamente fuera de la
  garantía provista por el binding.

Requisitos arquitectónicos aceptados por v1.3.0 para una futura implementación
de required-permission binding:

- [x] La permission solicitada debe coincidir exactamente con la permission
  requerida por la operación protegida cuando ésta la declare.
- [x] Una operación bound no puede omitir `required_permission`.
- [x] La lectura inválida o no disponible de `required_permission` debe fallar
  cerrado.
- [x] El mismatch de permission debe bloquear antes de consultar al PDP.
- [x] El PDP permanece genérico y no interpreta semántica de dominio.
- [x] Audit debe poder distinguir permission solicitada y permission requerida.
- [x] Legacy unbound sin `required_permission` puede conservar semántica
  compatible.
- [x] Permission equality no se confunde con exact subject binding ni con prueba
  de corrección semántica de la permission declarada.

Estos checks expresan aceptación de la **decisión arquitectónica**; no afirman
que el runtime v1.2.0 o v1.3.0 ya esté implementado.

## Rollback

Para el incremento original, revertir su commit elimina la frontera, sus pruebas
y esta ADR sin afectar el PDP.

Para los hardenings v1.2.0 y v1.3.0, antes de cualquier implementación el
rollback consiste en revertir exclusivamente la enmienda documental
correspondiente. Si posteriormente existiera una implementación bound, su
rollback deberá revertir primero el runtime y sus contratos de forma compatible
antes de retirar la obligación arquitectónica aplicable.

No existe en este momento estado persistente ni integración durable que deba
migrarse por esta enmienda.

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 2026-07-26 | Decisión inicial para la frontera PDP–PEP. |
| 1.1.0 | 2026-08-09 | Reconciliación histórica: auditoría incorporada posteriormente por PR #22 y PR #23 sin cambiar la frontera PDP–PEP. |
| 1.2.0 | 2026-09-15 | Hardening normativo: exact operation binding, propagación request/decision/confirmation, enforcement fail-closed, audit bound y coherencia temporal; durable replay/idempotencia permanecen fuera de scope. |
| 1.3.0 | 2026-09-15 | Hardening normativo: exact required-permission binding entre request y operación protegida, fail-closed ante mismatch/ausencia en operaciones bound y auditoría requested-vs-required; runtime y Persistence Authorization permanecen no autorizados. |