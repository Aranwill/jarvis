---
title: Malāk Assurance Signal Authority Boundary — G0/G1 Design
status: g1_design_candidate
authority: owner_authorized_analysis
language: es
as_of_date: 2026-09-11
source_baseline: 7cae3dcb854207175b716b66c9c569a335f81516
depends_on_pr: 110
g2_implementation_authorized: false
g2b_conversation_integration_authorized: false
sprint_7_12_authorized: false
rdd_stage_2_authorized: false
candidate_content_identity_g2_authorized: false
persistence_authorization_authorized: false
related:
  - docs/architecture/adr/ADR-005-evidence-bound-final-response-transition.md
  - docs/project/sprints/proposals/MALAK-COGNITIVE-ASSURANCE-G1-PROGRESSIVE-DESIGN.md
  - docs/project/sprints/proposals/MALAK-PROGRESSIVE-COGNITIVE-ASSURANCE-RUNTIME-G0-INSPECTION.md
  - docs/project/sprints/proposals/MALAK-PROGRESSIVE-COGNITIVE-ASSURANCE-RUNTIME-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-PROGRESSIVE-COGNITIVE-ASSURANCE-RUNTIME-G2A-IMPLEMENTATION-CANDIDATE-SPEC.md
---

# Malāk Assurance Signal Authority Boundary — G0/G1 Design

## 1. Estado de autoridad

El Owner autorizó continuar el análisis después de materializar y validar en aislamiento:

```text
G2A — Protected Finalization Foundation
```

Esta unidad cubre únicamente G0/G1 del problema siguiente:

> ¿de dónde nacen, cómo se ligan y quién puede afirmar legítimamente los signals que alimentan Protected Finalization sin convertir outputs probabilísticos, metadata del provider o decisiones de otro dominio en autoridad cognitiva implícita?

Esta unidad NO autoriza implementación runtime ni G2B.

```text
G0/G1 design
!=
Signal Producer implementation
!=
Conversation wiring
!=
Final Response enforcement
```

---

## 2. Baseline inspeccionado

Baseline dependiente:

```text
Aranwill/jarvis
PR #110 HEAD
7cae3dcb854207175b716b66c9c569a335f81516
```

G2A expone, en aislamiento, un input explícito equivalente a:

```text
applicability
evidence_required
support_sufficient
contradiction_unresolved
policy_violation
```

Y produce:

```text
ACCEPT | ABSTAIN | BLOCK
```

G2A no decide de dónde provienen esos signals.

---

## 3. G0 — evidencia observada

### 3.1 Request no transporta contexto cognitivo suficiente

`Request` contiene:

```text
content
session_id
request_id
created_at
```

No transporta:

```text
materiality
risk class
claim type
evidence refs
source dispositions
contradiction state
cognitive policy disposition
assurance applicability
```

### 3.2 ConversationRequest tampoco transporta evidencia

`ConversationRequest` contiene:

```text
prompt
model
system_prompt
history
```

No existe claim/evidence binding ni evidence provenance.

### 3.3 ConversationResponse no puede afirmar support sufficiency

`ConversationResponse` contiene únicamente:

```text
content
model
provider
```

Por tanto:

```text
provider/model metadata
!=
evidence
!=
support sufficiency
!=
authority
```

### 3.4 ConversationService finaliza demasiado pronto para G2B

La ruta actual:

```text
provider.generate(...)
        ↓
ConversationResponse
        ↓
record_exchange(... response.content ...)
        ↓
return response
```

El assistant history recibe el output bruto del provider antes de cualquier futura finalización protegida.

Esto sigue siendo un blocker independiente para G2B.

### 3.5 Security PDP no es un productor cognitivo genérico

El Security Control Plane decide permisos para operaciones protegidas mediante:

```text
ALLOW
DENY
REQUIRE_HUMAN_CONFIRMATION
```

Una decisión de autorización no demuestra por sí misma:

```text
claim truth
support sufficiency
contradiction resolution
materiality
```

Y tampoco todo `DENY` debe convertirse en:

```text
policy_violation=True
```

sobre una Candidate Response.

Solo una policy explícita de finalización podría establecer una traducción concreta y acotada.

### 3.6 No existe productor runtime autorizado para los cinco signals

No se observó en el baseline un componente runtime que produzca con semántica suficiente:

```text
AssuranceApplicability
EvidenceRequirement
SupportSufficiency
ContradictionDisposition
FinalizationPolicyDisposition
```

Conclusión:

```text
G0 RESULT: PASS / GAP CONFIRMED
```

El gap es real y no puede cerrarse honestamente mediante wiring directo de Conversation → G2A.

---

## 4. Antipatrones rechazados por G0

### A. Dejar que el LLM se autoasigne assurance

```text
model says "I am confident"
→ support_sufficient=True
```

REJECT.

Model confidence puede ser señal auxiliar futura, nunca sustituto de evidencia.

### B. Usar provider/model como autoridad

```text
provider == trusted_provider
→ support_sufficient=True
```

REJECT.

Provenance técnica no equivale a autoridad epistémica.

### C. Tratar ausencia de señal como estado favorable

```text
no contradiction marker
→ contradiction_unresolved=False
```

REJECT.

```text
missing signal != favorable signal
```

### D. Mapear Security DENY directamente a policy_violation

REJECT como regla general.

Security authorization y cognitive finalization son dominios diferentes.

### E. Inferir materialidad con heurísticas textuales ad hoc

Ejemplos rechazados:

```text
contains "medical" → high risk
contains "write" → not applicable
```

sin specification, coverage y policy versionada.

### F. Permitir que el caller declare NOT_APPLICABLE libremente

REJECT.

Un caller no confiable no puede autoeximirse de assurance.

---

## 5. G1 — decisión arquitectónica

```text
G1 RESULT: PASS / SPLIT
```

No se selecciona un único `AssuranceSignalProducer` monolítico.

Se selecciona una separación conceptual entre:

```text
DOMAIN-SPECIFIC OBSERVATIONS
        ↓
AUTHORIZED SIGNAL PRODUCTION
        ↓
DETERMINISTIC SIGNAL PROJECTION
        ↓
ProtectedFinalizationInput
        ↓
G2A evaluator
```

Razón:

Cada signal tiene una semántica y una fuente de autoridad diferentes. Un productor único tendería a mezclar clasificación, evidencia, policy y seguridad en una autoridad opaca.

---

## 6. Ownership por signal

### 6.1 Applicability

Debe provenir de una **cognitive assurance policy versionada** aplicada a contexto explícito y autorizado.

No puede provenir de:

- output del provider;
- model confidence;
- texto libre del candidate;
- preferencia del caller.

Si el contexto requerido para determinar applicability falta:

```text
→ UNRESOLVED
```

nunca `NOT_APPLICABLE` por defecto.

### 6.2 evidence_required

Debe derivarse de la misma policy o de una policy compatible que determine si las afirmaciones materiales requieren soporte verificable.

No puede inferirse de:

```text
provider identity
model size
model confidence
response length
```

### 6.3 support_sufficient

Solo puede afirmarse a partir de una evaluación explícita de evidencia aplicable.

Debe poder distinguir:

```text
no evidence
insufficient evidence
sufficient evidence
unknown/unassessed
```

G2A actualmente consume booleano; por tanto una futura projection deberá fallar seguro cuando el dominio upstream no pueda demostrar suficiencia.

Regla:

```text
unassessed support
!=
sufficient support
```

### 6.4 contradiction_unresolved

Debe provenir de una evaluación explícita de contradicción o de evidencia que establezca el estado.

No observar contradicción no basta para demostrar resolución cuando el check aplicable no ocurrió.

Una futura policy puede declarar que determinados casos A0 no requieren este check; eso pertenece a applicability, no a falsificar el signal.

### 6.5 policy_violation

Debe representar una violación aplicable a la finalización de esa Candidate Response.

Puede integrar evidencia de Security o Governance solo mediante un adapter/policy explícito y acotado.

```text
Security decision
!=
Cognitive policy violation
```

pero:

```text
explicit finalization policy rule
may consume a security disposition
```

si dicha relación está especificada y versionada.

---

## 7. Boundary de autoridad seleccionado

G1 selecciona el patrón:

```text
observation
!=
producer authorization
!=
projected signal
!=
finalization decision
!=
authority
```

Una futura implementación deberá poder demostrar, conceptualmente:

```text
who produced the observation?
what signal scope may that producer assert?
which request/candidate is it bound to?
which policy version interpreted it?
was every required signal accounted for?
```

No se requiere todavía un registry global ni PKI.

---

## 8. Binding permitido en esta etapa

Candidate Content Identity G2 sigue NO autorizado y pertenece al dominio episódico actualmente diseñado.

Por tanto esta unidad no introduce identidad criptográfica de Response.

El máximo binding admisible para una primera foundation es:

```text
same-process
request-bound
session-bound
candidate-object/content passed directly
no durable receipt
no replay claim
```

Si una futura implementación requiere persistir, transportar o rehidratar signals fuera del proceso:

```text
STOP
→ abrir diseño de content identity / integrity binding específico
```

No reutilizar silenciosamente la identidad episódica.

---

## 9. Projection determinista

El objetivo de una futura projection no es decidir verdad.

Debe solamente convertir observations autorizadas y completas en el contrato que G2A ya entiende.

Conceptualmente:

```text
Authorized Signal Set
        ↓
completeness / scope / binding checks
        ↓
ProtectedFinalizationInput
```

Si falta cualquier signal requerido para la policy aplicable:

```text
projection must fail safe
```

Nunca completar faltantes con defaults favorables.

---

## 10. Qué sí puede ser determinista primero

Siguiendo Progressive Cognitive Assurance G1:

```text
policy applicability
schema validity
producer scope
request binding
policy version compatibility
explicit security disposition mapping
known contradiction markers
known evidence disposition
```

pueden verificarse determinísticamente cuando exista input suficiente.

Lo que no debe inventarse:

```text
materiality from vague heuristics
evidence truth from model confidence
contradiction resolution from silence
policy compliance from provider reputation
```

---

## 11. Consecuencia para G2B

G2B sigue bloqueado.

Para admitir Conversation Finalization Integration deberán existir, como mínimo:

```text
1. signal authority/projection boundary implementada y validada;
2. una forma autorizada de determinar applicability para la ruta conversacional;
3. una forma explícita de representar evidence-required vs not-required;
4. fail-safe semantics para support/contradiction no evaluados;
5. resolución del history timing:
   provider output must not be recorded as assistant history before finalization.
```

Además, una respuesta factual que requiere evidencia no puede obtener `support_sufficient=True` mientras no exista evidencia real evaluable.

---

## 12. Resultado de dependencia

La secuencia segura queda:

```text
G2A Protected Finalization Foundation
        ↓
Assurance Signal Authority Boundary G0/G1   ← this unit
        ↓
future Signal Boundary G2                   ← NOT AUTHORIZED
        ↓
legitimate applicability/evidence producers
        ↓
Conversation history/finalization integration design
        ↓
G2B                                          ← NOT AUTHORIZED
```

No se autoriza saltar desde este G1 directamente a G2B.

---

## 13. Candidato de implementación futura

G1 recomienda que, si el Owner autoriza una siguiente implementation unit, esta sea **solo una foundation de autoridad/projection**, sin clasificadores y sin Conversation wiring.

Objetivo candidato:

```text
accept explicit authorized observations
validate producer scope + binding + completeness
project fail-safe ProtectedFinalizationInput
```

No deberá:

- leer prompts;
- clasificar texto;
- llamar LLMs;
- llamar providers;
- acceder a red;
- mutar history;
- persistir signals;
- crear receipts durables;
- tocar Kernel;
- integrar Conversation;
- activar Memory/Knowledge/retrieval;
- autorizar Candidate Content Identity G2;
- autorizar Sprint 7.12;
- autorizar RDD Stage 2.

---

## 14. Stop conditions para futuro G2

Detener si la implementación requiere:

- inferencia probabilística para decidir producer authority;
- autoasignación de trust por el producer;
- defaults favorables para signals faltantes;
- mapping implícito de Security a Cognitive policy;
- durable binding sin content identity suficiente;
- cambio de Kernel;
- Conversation wiring;
- nueva persistencia;
- nuevas dependencias externas;
- expansión de autoridad.

---

## 15. Estado final de esta unidad

```text
Assurance Signal Authority problem:
CONFIRMED

Architecture:
SPLIT BY SIGNAL DOMAIN

Signal Authority / Projection design:
READY FOR OWNER REVIEW

Signal Boundary G2 implementation:
NOT AUTHORIZED

Conversation G2B:
BLOCKED
```
