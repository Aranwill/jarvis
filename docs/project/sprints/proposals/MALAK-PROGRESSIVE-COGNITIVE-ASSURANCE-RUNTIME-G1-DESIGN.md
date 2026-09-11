---
title: Malāk Progressive Cognitive Assurance Runtime — G1 Design
status: gate_candidate
authority: design_evidence
language: es
as_of_date: 2026-09-11
source_baseline: 5865da6a5e502fe71e35e2e38bc4cceaab9b3600
g0_source: docs/project/sprints/proposals/MALAK-PROGRESSIVE-COGNITIVE-ASSURANCE-RUNTIME-G0-INSPECTION.md
implementation_authorized: false
sprint_7_12_authorized: false
rdd_stage_2_authorized: false
related:
  - docs/architecture/adr/ADR-005-evidence-bound-final-response-transition.md
  - docs/architecture/blueprint.md
  - docs/governance/cognitive_constitution.md
  - docs/project/sprints/proposals/MALAK-COGNITIVE-ASSURANCE-G1-PROGRESSIVE-DESIGN.md
  - docs/project/sprints/proposals/MALAK-PROGRESSIVE-COGNITIVE-ASSURANCE-RUNTIME-SCOPE-FREEZE-CANDIDATE.md
---

# Malāk Progressive Cognitive Assurance Runtime — G1 Design

## 1. Estado de autoridad

Este documento transforma la inspección G0 en un diseño mínimo candidato.

No autoriza implementación.

No crea Sprint 7.12.

No modifica el Blueprint, la Cognitive Constitution ni ADR-005.

```text
G1 Design != G2 Authorization
Design != Runtime Capability
Evidence != Authority
```

---

## 2. Resultado G1

```text
G1 RESULT: PASS / SPLIT
```

### PASS

La arquitectura actual permite definir una frontera protegida sin introducir lógica cognitiva en Kernel, provider o runtime.

### SPLIT

La inspección demuestra que deben separarse dos incrementos distintos:

```text
G2A — Protected Finalization Foundation
     contracts + deterministic evaluator
     isolated / no live conversation enforcement

G2B — Conversation Finalization Integration
     only after applicability/evidence inputs have an authorized producer
```

No se debe fingir que G2A constituye assurance operativo end-to-end.

---

## 3. Decisión de ownership

### 3.1 Orquestación de finalización

Para el primer slice conversacional, el ownership de la transición protegida queda candidato en la frontera de `ConversationCapability`.

Razones:

- está después de `ConversationService.generate()`;
- está antes del retorno al Kernel;
- ya adapta el resultado conversacional al contrato genérico de Capability;
- evita acoplar provider/runtime a governance;
- evita introducir business logic en Kernel;
- permite inyectar una policy/evaluator sin convertirlo en autoridad autónoma.

Dirección:

```text
ConversationCapability
  owns orchestration of:
  generated candidate
      ↓
  assurance evaluation
      ↓
  finalization decision
      ↓
  returned final content
```

`ConversationCapability` no debe decidir verdad por sí misma. Solo debe orquestar un evaluator determinista autorizado.

---

## 4. Ownership preservado de otros componentes

### `ConversationService`

Conserva ownership de:

- provider resolution;
- history snapshot;
- provider delegation;
- conversation history storage.

No recibe ownership de Cognitive Assurance policy.

### `ConversationProvider` / `LLMRuntime`

Conservan generación.

```text
provider/runtime = candidate producer
provider/runtime != finalizer
```

### Kernel

Conserva coordinación genérica.

```text
Kernel.execute capability result
→ wrap Response
```

No evalúa materialidad, evidencia ni assurance.

### CLI

Conserva presentación.

No evalúa assurance.

---

## 5. Cambio conceptual obligatorio en historial

La semántica del historial queda congelada así:

```text
assistant history
=
content actually finalized/presented by Malāk
```

Nunca:

```text
assistant history
=
raw provider candidate that was later withheld/replaced
```

Por tanto el comportamiento futuro deberá separar:

```text
generate candidate
        ↓
finalize candidate
        ↓
record finalized exchange
```

La generación no debe registrar por sí sola el mensaje `assistant` cuando exista una frontera protegida activa.

---

## 6. Estrategia de historial seleccionada

Se compararon tres opciones.

### Opción A — assurance dentro de `ConversationService`

Rechazada como dirección base.

Motivo: mezcla provider delegation/history con governance policy y contradice la responsabilidad declarada actual del service.

### Opción B — `ConversationCapability` accede directamente a `InMemoryConversationContext`

Rechazada.

Motivo: duplica ownership y rompe encapsulación del service.

### Opción C — split generación / commit de intercambio finalizado

Seleccionada.

Semántica:

```text
ConversationService.generate(...)
→ generated ConversationResponse
→ NO assistant history commit yet

ConversationCapability
→ assurance/finalization

ConversationService commit finalized exchange
→ exact user content
→ exact finalized assistant content
```

G1 congela la semántica, no los nombres de métodos ni firmas Python exactas.

---

## 7. Candidate contract mínimo

El primer candidate de respuesta debe ser efímero y request-bound.

Información mínima:

```text
request_id
session_id
content
provider
model
```

Reglas:

- `request_id` es correlación de request existente;
- `session_id` preserva aislamiento conversacional;
- `provider` y `model` conservan provenance técnica ya disponible;
- `content` es candidate generado;
- ninguno de estos campos constituye identidad criptográfica de contenido.

No se introduce:

```text
candidate content hash as trust root
PKI
signature
nonce
Content Identity G2
```

### Invariante

```text
request correlation != content identity
```

---

## 8. Finalization evaluator contract conceptual

G1 selecciona una dependencia determinista e inyectable.

Semántica conceptual:

```text
evaluate(candidate, assurance_input)
→ FinalizationDecision
```

No se congela nombre de clase, módulo ni package.

Propiedades obligatorias:

- pura o efectivamente side-effect free;
- determinista para los mismos inputs;
- sin llamadas de red;
- sin LLM interno;
- sin retries;
- sin persistencia;
- sin acceso directo a Memory/Knowledge;
- policy version identificable;
- malformed/unknown state no puede producir aceptación silenciosa.

---

## 9. Assurance applicability contract

G0 demostró que el runtime no puede determinar materialidad de forma fiable hoy.

Por tanto el evaluator **no debe inventarla**.

G1 congela un input explícito de applicability con tres estados conceptuales:

```text
NOT_APPLICABLE
REQUIRED
UNRESOLVED
```

Semántica:

### `NOT_APPLICABLE`

Existe evidencia upstream determinista suficiente de que el candidate no requiere evidence-bound assurance adicional para ese scope.

### `REQUIRED`

La respuesta requiere assurance según policy/materialidad/riesgo ya evaluados upstream.

### `UNRESOLVED`

No existe información suficiente para afirmar de forma segura si el assurance requerido aplica.

Regla fail-safe:

```text
UNRESOLVED
cannot silently become
NOT_APPLICABLE
```

---

## 10. Evidence input semantics

El evaluator solo puede utilizar evidence state explícitamente suministrado por un productor autorizado.

G1 define categorías conceptuales mínimas, no schemas finales:

```text
evidence_required
support_sufficient
contradiction_unresolved
policy_violation
```

Reglas:

```text
missing signal != favorable signal
model confidence != support_sufficient
provider identity != source authority
absence of contradiction signal != contradiction resolved
```

### Estado actual

No existe hoy un productor runtime general de estos inputs en la ruta conversacional.

Por eso G2B permanece bloqueado hasta que exista una fuente autorizada y verificable de applicability/evidence signals.

---

## 11. Outcome semantics

Los cuatro outcomes del diseño conceptual se preservan semánticamente:

```text
ACCEPT
QUALIFY
ABSTAIN
BLOCK
```

pero G1 evita convertirlos automáticamente en enum/API de G2A.

### `ACCEPT`

El candidate puede convertirse en Final Response sin transformación material adicional.

### `QUALIFY`

Solo puede emitirse si existe **contenido final cualificado explícito**.

```text
QUALIFY
!=
return raw candidate + metadata hidden somewhere
```

Si no existe mecanismo autorizado para producir `qualified_content`, el evaluator no puede inventarlo.

### `ABSTAIN`

Se produce una respuesta determinista de abstención/insuficiencia, no el candidate bruto.

### `BLOCK`

Policy/security/authority impide la finalización solicitada.

No equivale a incertidumbre ordinaria.

---

## 12. Precedencia candidata de decisión

Cuando existan inputs válidos, la policy deberá aplicar precedencia explícita.

Dirección G1:

```text
1. malformed / invalid binding
   → no ACCEPT

2. policy/security violation
   → BLOCK

3. applicability UNRESOLVED
   → ABSTAIN or HOLD-equivalent internal disposition

4. applicability NOT_APPLICABLE
   → ACCEPT

5. applicability REQUIRED + unresolved contradiction
   → QUALIFY only with authorized qualified_content
      otherwise ABSTAIN

6. applicability REQUIRED + required evidence insufficient
   → QUALIFY only with authorized qualified_content
      otherwise ABSTAIN

7. applicability REQUIRED + checks satisfied
   → ACCEPT
```

No majority vote.

No magic score.

---

## 13. Qualified content rule

G1 identifica una restricción importante:

La policy de assurance no debe convertirse en generador lingüístico.

Por tanto:

```text
assurance evaluator
may choose disposition
but must not improvise arbitrary rewritten factual content
```

Una futura ruta `QUALIFY` necesita uno de:

- contenido cualificado determinista;
- candidate revision gobernada y acotada;
- producer específico autorizado.

Eso no forma parte de G2A.

---

## 14. G2A — Protected Finalization Foundation

G2A es el incremento implementable más pequeño identificado por G1.

### Objetivo

Materializar en aislamiento:

- candidate contract mínimo;
- assurance input contract explícito;
- finalization decision contract;
- deterministic evaluator;
- policy version;
- negative tests;
- no side effects.

### G2A NO incluye

- wiring a CLI;
- modificación de ConversationService;
- historial;
- provider/runtime changes;
- live materiality classification;
- evidence retrieval;
- Memory/Knowledge;
- second model;
- QUALIFY content generation.

### Valor

Permite probar:

```text
candidate != decision
invalid/unknown != accepted
policy violation != uncertainty
missing evidence != sufficient evidence
```

sin mentir sobre integración end-to-end.

---

## 15. G2B — Conversation Finalization Integration

G2B solo puede abrirse cuando exista un productor autorizado de:

```text
assurance applicability
and
required evidence/policy signals for the selected scope
```

Entonces podrá integrar:

```text
ConversationResponse candidate
        ↓
assurance input
        ↓
deterministic evaluator
        ↓
finalized content
        ↓
record finalized exchange
        ↓
Kernel Response
        ↓
CLI
```

### Gate condition

```text
no signal producer
→ no live assurance claim
→ no G2B
```

---

## 16. Por qué no usar defaults permisivos

Rechazado:

```text
if missing evidence inputs:
    ACCEPT
```

Eso convertiría ausencia de información en permiso de finalización y violaría el espíritu de R-022/CC-012.

También rechazado:

```text
all LLM output is automatically NOT_APPLICABLE
```

porque una respuesta conversacional arbitraria puede contener afirmaciones materiales.

---

## 17. Por qué no bloquear toda conversación ahora

También se rechaza:

```text
all LLM output = REQUIRED
missing evidence = ABSTAIN
```

como activación inmediata de producto.

Aunque es conservador, degradaría la conversación completa sin una policy de materialidad/assurance suficientemente expresiva y no demostraría utilidad cognitiva proporcional.

La secuencia correcta es:

```text
foundation
→ explicit signals
→ controlled integration
→ measured behavior
```

---

## 18. Kernel invariants

G1 congela:

```text
Kernel.receive()
remains unaware of:
- provider/model
- candidate semantics
- evidence sufficiency
- assurance outcomes
- materiality
```

El Kernel seguirá recibiendo un resultado ya finalizado desde la Capability integrada.

Modificar esta regla requiere evidencia de blocker + gate separado.

---

## 19. Provider/runtime invariants

G1 congela:

```text
LLMRuntime.generate()
→ generated candidate
```

No:

```text
LLMRuntime.generate()
→ authoritative final response
```

Provider/runtime no recibe imports de assurance policy en el primer diseño.

---

## 20. Response contract público

`malak.core.response.Response` puede permanecer inicialmente:

```text
content
source
```

No es obligatorio exponer assurance metadata al Kernel/CLI para demostrar la primera foundation.

Si G2B requiere metadata pública para transparencia/auditoría, deberá justificarse de forma separada antes de ampliar `Response`.

---

## 21. Auditability

G2A puede conservar una decisión in-memory/return value con:

```text
outcome/disposition
reason_code
policy_version
request_id correlation
evaluated_at
```

No se autoriza persistencia nueva.

No se autoriza Cognitive Receipt durable.

```text
decision metadata != receipt authority
```

---

## 22. Tests obligatorios de G2A

Como mínimo:

```text
malformed candidate
→ fail safe

malformed assurance input
→ fail safe

policy violation
→ not ACCEPT

UNRESOLVED applicability
→ not ACCEPT

REQUIRED + missing support
→ not ACCEPT

REQUIRED + unresolved contradiction
→ not ACCEPT unless explicit safe qualified content contract exists

NOT_APPLICABLE valid case
→ ACCEPT

REQUIRED + sufficient explicit support + no blockers
→ ACCEPT

same inputs
→ same decision semantics
```

Además:

```text
no network
no provider calls
no Memory
no Knowledge
no persistence
no Kernel modification
```

---

## 23. Tests obligatorios futuros de G2B

Cuando G2B sea admisible:

```text
raw provider candidate never reaches user-visible response without evaluation
raw rejected candidate never enters assistant history
ACCEPT records exactly finalized accepted content
ABSTAIN/BLOCK records only the actual user-visible final message if history policy requires it
provider/runtime remain assurance-agnostic
Kernel remains assurance-agnostic
CLI presents only finalized response
```

---

## 24. Dependencia pendiente identificada

G1 identifica una dependencia real que no debe ocultarse:

```text
Assurance Applicability / Evidence Signal Production
```

Esta dependencia no equivale automáticamente a:

- Memory;
- Knowledge;
- RAG;
- Content Identity G2;
- second model;
- external provider.

Puede comenzar como una boundary determinista separada, pero necesita su propio G0/G1 antes de G2B.

---

## 25. Decisión de implementación candidata

G1 recomienda que una futura solicitud de implementación autorice, como máximo y de forma separada:

```text
G2A only
Protected Finalization Foundation
```

No recomienda todavía autorizar G2B.

Razón:

```text
we can build the law-preserving decision boundary now
without pretending we already possess the evidence producers needed for live enforcement
```

---

## 26. Stop conditions

Detener G2A si requiere:

- cambios de Kernel;
- cambios de provider/runtime;
- persistencia;
- Content Identity G2;
- Memory/Knowledge wiring;
- nuevas dependencias externas;
- clasificación probabilística always-on;
- ampliación del contrato público `Response` sin necesidad demostrada;
- generación lingüística dentro de evaluator.

Detener G2B si no existe productor explícito y autorizado de applicability/evidence signals.

---

## 27. Resultado final G1

```text
G1 design:
COMPLETE

selected ownership:
ConversationCapability finalization orchestration

selected history semantics:
record Final Response, never raw unaccepted candidate

selected implementation sequence:
G2A foundation first
G2B live integration later

G2A implementation:
NOT AUTHORIZED YET

G2B implementation:
BLOCKED BY SIGNAL-PRODUCER GAP

Sprint 7.12:
NOT AUTHORIZED

Candidate Content Identity G2:
NOT AUTHORIZED

Persistence Authorization:
NOT AUTHORIZED

RDD Stage 2:
NOT AUTHORIZED
```

El siguiente gate válido es una decisión explícita del Owner sobre si autoriza o no **G2A — Protected Finalization Foundation** como unidad aislada y candidate-bound.