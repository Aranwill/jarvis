---
id: ADR-002
title: "Frontera de enforcement entre PDP y operación protegida"
status: accepted
date: 2026-07-26
updated: 2026-09-15
author: Hector Rodriguez
reviewed_by:
  - ChatGPT
version: 1.2.0
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
requested exact subject binding
actual protected-operation binding
outcome / reason
```

Un mismatch de binding nunca debe degradarse a un audit de autorización
permitida.

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

Rechazada para el incremento original. El hardening v1.2.0 tampoco declara
resuelto replay durable: liga autorización y ejecución al mismo sujeto material,
pero freshness/replay durable continúa requiriendo contratos y fundamentos
adicionales coordinados con la operación concreta.

### Resolver el binding únicamente en un wrapper de dominio

Rechazada. Un wrapper Memory-local alrededor de una `AuthorizationRequest`
unbound no demuestra que el PDP haya decidido sobre el sujeto material exacto.
El binding debe formar parte de la request evaluada y ser verificado por la
frontera de enforcement.

### Hacer que Security interprete tipos de Memory

Rechazada. Introduciría acoplamiento inverso y transferiría semántica de dominio
a Security. El binding debe permanecer opaco y versionado; cada dominio es
responsable de derivarlo/recomputarlo desde el material real que protege.

## Consecuencias

### Positivas

- La decisión y su aplicación permanecen separadas.
- El llamador no puede aportar una decisión fabricada a la API del PEP.
- La asociación entre solicitud y decisión es explícita.
- Las operaciones bound agregan asociación explícita con el sujeto material
  exacto que será ejecutado.
- La confirmación humana no puede interpretarse como permiso para otro sujeto
  bound de la misma clase.
- La auditoría puede conservar qué sujeto exacto fue autorizado sin copiar el
  payload.
- Los fallos del PDP, las decisiones incongruentes y los binding mismatches
  bloquean la ejecución.
- El Kernel permanece intacto.

### Negativas y límites

- La confianza en el PDP depende de la composición que lo inyecta.
- El binding requiere una specification de dominio que defina material exacto,
  canonicalización, versión y algoritmo aceptado.
- Equality de bindings no demuestra trust, autenticidad ni verdad semántica.
- El hardening no impide replay durable por sí mismo.
- Un durable write futuro deberá resolver además idempotencia y fallos parciales.
- No existe todavía integración con Persistent Memory ni protected durable write.

Nota de evolución: la limitación de auditoría del ADR original describía
correctamente el estado al aprobar ADR-002. Posteriormente, el Sprint 7.5
incorporó contratos de auditoría mediante la PR #22 y su integración fail-closed
con el PEP mediante la PR #23. v1.2.0 extiende la propiedad arquitectónica para
que una futura operación bound preserve también la identidad exacta del sujeto
en esa evidencia.

### Riesgos

- Una composición futura podría inyectar un PDP no confiable.
- Una operation implementation defectuosa podría declarar un binding que no
  corresponda al payload real; cada dominio sensible debe definir cómo deriva o
  recomputa el binding desde el estado realmente ejecutado.
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

Esta aceptación arquitectónica no constituye por sí misma autorización de
implementación. No autoriza Persistence Authorization, Persistent Memory,
Protected Durable Write, Durable Reliance runtime, Conversation G2B, RDD Stage 2
o Sprint 7.12.

No se agrega responsabilidad al Kernel, Planner, CLI, runtimes ni Capability
Registry.

## Relación con Gobernanza

- Blueprint: verifica autorización antes de ejecutar y conserva el
  Kernel sin lógica de negocio.
- Constitución Cognitiva: el enforcement es determinista y no depende
  de LLM.
- Constitución de Gobernanza: aplica seguridad por defecto, mínimo
  privilegio, separación de responsabilidades, trazabilidad y control humano.
- ADR-006: el hardening satisface la precondición arquitectónica de exact
  operation-subject binding, pero no declara satisfechas freshness/replay,
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

Estos checks expresan aceptación de la **decisión arquitectónica**; no afirman
que el runtime v1.2.0 ya esté implementado.

## Rollback

Para el incremento original, revertir su commit elimina la frontera, sus pruebas
y esta ADR sin afectar el PDP.

Para el hardening v1.2.0, antes de cualquier implementación el rollback consiste
en revertir exclusivamente la enmienda documental. Si posteriormente existiera
una implementación bound, su rollback deberá revertir primero el runtime y sus
contratos de forma compatible antes de retirar esta obligación arquitectónica.

No existe en este momento estado persistente ni integración durable que deba
migrarse por esta enmienda.

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 2026-07-26 | Decisión inicial para la frontera PDP–PEP. |
| 1.1.0 | 2026-08-09 | Reconciliación histórica: auditoría incorporada posteriormente por PR #22 y PR #23 sin cambiar la frontera PDP–PEP. |
| 1.2.0 | 2026-09-15 | Hardening normativo: exact operation binding, propagación request/decision/confirmation, enforcement fail-closed, audit bound y coherencia temporal; durable replay/idempotencia permanecen fuera de scope. |
