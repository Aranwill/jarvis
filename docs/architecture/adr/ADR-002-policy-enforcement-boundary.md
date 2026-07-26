---
id: ADR-002
title: "Frontera de enforcement entre PDP y operación protegida"
status: accepted
date: 2026-07-26
author: Hector Rodriguez
reviewed_by:
  - ChatGPT
version: 1.0.0
tags:
  - security
  - authorization
  - enforcement
  - governance
related:
  blueprint: DOC-ARQ-BLUEPRINT
  sprint: SPRINT-7.5
  knowledge_model: DOC-ARQ-KNOWLEDGE-MODEL
graph:
  type: architecture_decision
  domain: security
  affects:
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

## Alternativas consideradas

### Aceptar una decisión aportada por el llamador

Rechazada porque permitiría fabricar una decisión permitida fuera del
PDP y puentear la frontera de autoridad.

### Integrar el enforcement directamente en el Kernel

Rechazada porque agregaría responsabilidad de seguridad operativa al
Kernel y mezclaría coordinación con decisión y ejecución.

### Incorporar ahora sesiones, firmas, TTL o prevención de replay

Rechazada para este incremento. Estas propiedades requieren contratos y
fundamentos adicionales del futuro Secure Context Manager.

## Consecuencias

### Positivas

- La decisión y su aplicación permanecen separadas.
- El llamador no puede aportar una decisión fabricada a la API del PEP.
- La asociación entre solicitud y decisión es explícita.
- Los fallos del PDP bloquean la ejecución.
- El Kernel permanece intacto.

### Negativas y límites

- La confianza en el PDP depende de la composición que lo inyecta.
- El incremento no impide replay persistente.
- No existe todavía integración con operaciones reales.
- La auditoría de autorización permanece pendiente.

### Riesgos

- Una composición futura podría inyectar un PDP no confiable.
- Una operación no idempotente puede fallar después de iniciarse; el PEP
  no debe reintentarla automáticamente.
- Integrar rutas operativas antes de la auditoría y de una revisión
  independiente ampliaría prematuramente la superficie de riesgo.

## Impacto arquitectónico

La decisión incorpora una frontera nueva en `malak.security` mediante:

- `PolicyEnforcementPoint`;
- `StrictPolicyEnforcementPoint`;
- `ProtectedOperation`;
- `AuthorizationDeniedError`;
- `AuthorizationEnforcementError`.

No modifica contratos de autorización existentes, PDP, Kernel, Planner,
CLI, runtimes ni Capability Registry.

## Relación con Gobernanza

- Blueprint: verifica autorización antes de ejecutar y conserva el
  Kernel sin lógica de negocio.
- Constitución Cognitiva: el enforcement es determinista y no depende
  de LLM.
- Constitución de Gobernanza: aplica seguridad por defecto, mínimo
  privilegio, separación de responsabilidades y control humano.
- Kernel First: no agrega responsabilidades al Kernel.

## Compatibilidad con AKS / GraphRAG

La ADR conserva un identificador permanente, dominio `security`,
relaciones explícitas y una lista acotada de componentes afectados. No
incorpora GraphRAG ni cambia las reglas del AKS.

## Criterios de aceptación

- [x] La decisión no puede ser aportada por el llamador.
- [x] El PEP consulta directamente al PDP inyectado.
- [x] Las decisiones denegadas o incongruentes bloquean la operación.
- [x] Los fallos del PDP producen comportamiento fail-closed.
- [x] La operación se ejecuta una sola vez ante autorización válida.
- [x] No existen reintentos automáticos.
- [x] Kernel, Planner, CLI y runtimes permanecen intactos.

## Rollback

Revertir el commit del Incremento 4 elimina la frontera, sus pruebas y
esta ADR sin afectar el PDP ni los contratos existentes. No existe
estado persistente ni integración operativa que deba migrarse.

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 2026-07-26 | Decisión inicial para la frontera PDP–PEP. |
