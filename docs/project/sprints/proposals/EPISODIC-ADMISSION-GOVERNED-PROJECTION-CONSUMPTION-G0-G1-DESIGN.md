---
title: Episodic Admission Governed Projection Consumption Boundary — G0/G1 Design Record
status: g1_design_review
authority: owner-approved design record
as_of_date: 2026-09-10
unit: Episodic Admission Governed Projection Consumption Boundary
gate: G1
source_baseline: 8638015a3ec8750901a1762ad51f60e7fb4a0240
risk_class: 3
vault_reconciliation_status_at_start: pending_after_pr_89
vault_head_at_start: d7d4e2d7b60982c999017b0a6cfd5b9ee0619be5
vault_last_observed_malak_head: 2e8c5d7318678caeb67c8906c951935832760003
sync_agent_head_at_start: 71b21e0a192017353075954e06e2b55f5f8e2255
sdd_required: true
tdd_required_for_future_implementation: true
full_4r_required: true
rdd_stage_1: adopted
rdd_stage_2_authorized: false
implementation_authorized: false
admission_consumption_implementation_authorized: false
episodic_admission_modification_authorized: false
governed_input_projection_modification_authorized: false
runtime_wiring_authorized: false
persistent_memory_authorized: false
retrieval_authorized: false
knowledge_implementation_authorized: false
sprint_7_12_authorized: false
vault_reconciliation_required_before_g2: true
language: es
---

# Episodic Admission Governed Projection Consumption Boundary — G0/G1 Design Record

## 1. Estado de autoridad

El Owner autorizó avanzar con **G0/G1 exclusivamente para análisis de necesidad y diseño** de la siguiente frontera mínima posterior a `Governed Input Projection`.

La unidad candidata se denomina:

```text
Episodic Admission Governed Projection Consumption Boundary
```

Su responsabilidad propuesta es responder únicamente:

> ¿cómo puede una `GovernedAdmissionInputProjection` válida ser consumida por la policy existente de Episodic Admission sin reabrir ninguna vía lateral desde `candidate.control`, sin duplicar la policy y sin convertir estados de projection en decisiones de admisión?

Esta autorización no permite todavía:

- código productivo;
- tests de implementación;
- modificar `episodic_admission.py`;
- modificar `governed_input_projection.py`;
- modificar Assessment Provenance o Producer Authorization;
- modificar Kernel, Planner, SecurityContext, PDP o PEP;
- conectar Conversation o runtime;
- persistir Memory;
- retrieval;
- Knowledge;
- agentes, tools o red;
- identidad o integridad criptográfica nueva;
- Sprint 7.12;
- RDD Stage 2;
- merge sin revisión humana.

```text
Design != Implementation
Projection READY != Admission ELIGIBLE
Admission Decision != Persistence Authorization
Evidence != Authority
```

---

## 2. Baseline exacto y estado cross-repository

Baseline fuente congelado para G0/G1:

```text
Aranwill/jarvis
main
8638015a3ec8750901a1762ad51f60e7fb4a0240
```

Ese commit corresponde al merge de PR #89, corrective packet documental post-PR #88.

Estado observado al iniciar G1:

```text
Malāk main:
8638015a3ec8750901a1762ad51f60e7fb4a0240

Project Vault main:
d7d4e2d7b60982c999017b0a6cfd5b9ee0619be5

último HEAD de Malāk reflejado por Vault:
2e8c5d7318678caeb67c8906c951935832760003

Vault Sync Agent main:
71b21e0a192017353075954e06e2b55f5f8e2255
```

PR #89 modificó exclusivamente documentación derivada/no normativa. El código productivo de Memory observado por este G0/G1 continúa siendo el integrado por PR #88.

Por tanto:

```text
PRODUCT CODE DRIFT SINCE PR #88 = 0
DOCUMENTARY VAULT RECONCILIATION AFTER PR #89 = PENDING
```

La diferencia documental del Vault no altera el análisis técnico de G0/G1, pero **debe resolverse antes de G2 o de cualquier implementación posterior**.

```text
G2 PRECONDITION:
Vault reconciliation == PASS
```

---

## 3. Resultado formal G0 — necesidad real

El baseline dispone de dos piezas deliberadamente separadas.

Primero:

```text
governed evidence
        ↓
Governed Input Projection
READY | HOLD | DENIED
```

Cuando el resultado es `READY`, la projection materializa:

```text
effective_context: EpisodicAdmissionContext
effective_signals: EpisodicAdmissionSignals
```

Segundo:

```text
EpisodicMemoryCandidate
+
EpisodicAdmissionSignals
        ↓
evaluate_episodic_candidate(...)
        ↓
REJECT | HOLD | ELIGIBLE
```

La separación fue intencional. PR #88 no ejecuta Admission.

El problema real aparece al intentar unirlas de la forma aparentemente más simple:

```python
evaluate_episodic_candidate(
    candidate,
    projection.effective_signals,
    evaluated_at,
)
```

Esa llamada es **incorrecta** para una cadena gobernada.

La implementación vigente de `evaluate_episodic_candidate(...)` hace:

```python
control = candidate.control
```

Y desde ese `control` decide, entre otras cosas:

```text
valid_until
source_authority_classification
confidence_classification
sensitivity_classification
valid_from
```

Esos son precisamente campos trust-sensitive que `Governed Input Projection` reconstruye en un **nuevo** `effective_context` porque la mera presencia de valores en `candidate.control` no constituye evidencia gobernada.

Por tanto, el direct wiring produciría esta vía lateral:

```text
projection.effective_signals
        +
original candidate.control
        ↓
Admission
```

En lugar de:

```text
projection.effective_context
        +
projection.effective_signals
        ↓
Admission
```

Consecuencia:

```text
DIRECT CALL WITH ORIGINAL CANDIDATE: REJECTED BY G0
```

Sin una frontera explícita, cualquier futura conexión hacia persistencia tendría dos alternativas incorrectas:

1. ignorar parte de la projection y volver a confiar en `candidate.control`;
2. duplicar o reimplementar la policy de Admission fuera de `episodic_admission.py`.

Ambas violan la arquitectura ya construida.

La necesidad de una frontera de consumo está demostrada porque cierra el último hueco interno entre evidencia gobernada y la policy existente **antes** de considerar persistencia.

Disposición G0:

```text
G0 RESULT: PASS
candidate disposition: ADAPT
risk class: 3 — HIGH
blocking findings: 0
implementation authorized: false
```

`ADAPT` significa que la solución debe adaptar inputs gobernados al evaluator existente, no reemplazar ni duplicar la policy de Admission.

---

## 4. Alternativas evaluadas en G0

### 4.1. Alternativa A — direct call con candidate original

```text
candidate original
+
projection.effective_signals
        ↓
evaluate_episodic_candidate(...)
```

Disposición:

```text
REJECT
```

Motivo:

- descarta `projection.effective_context`;
- reabre trust desde `candidate.control`;
- rompe el objetivo principal de PR #88.

### 4.2. Alternativa B — modificar la API de `episodic_admission.py`

Ejemplo conceptual:

```text
candidate_id
+
effective_context
+
effective_signals
        ↓
new admission API
```

Disposición:

```text
DEFER
```

No existe necesidad actual de modificar el contrato ya integrado de Admission si un adapter externo puede preservar exactamente su semántica.

Modificar el evaluator existente ampliaría:

- file budget;
- surface de regresión;
- compatibilidad pública;
- correction budget.

### 4.3. Alternativa C — reimplementar Admission en una nueva frontera

Disposición:

```text
REJECT
```

Motivo:

```text
Two Admission policies
= semantic drift risk
= precedence duplication
= security ambiguity
```

### 4.4. Alternativa D — adapter con vista efectiva efímera

Flujo conceptual:

```text
original candidate
        +
READY projection
        ↓
validate consumption bindings
        ↓
construct ephemeral effective candidate view
        │
        ├── candidate_id   = original
        ├── origin         = original
        ├── experience     = original
        ├── created_at     = original
        └── control        = projection.effective_context
        ↓
evaluate_episodic_candidate(
    effective candidate view,
    projection.effective_signals,
    current evaluated_at,
)
        ↓
existing EpisodicAdmissionDecision
```

Disposición:

```text
SELECTED FOR G1 DESIGN
```

Ventajas:

- no modifica la policy existente;
- no muta el candidate original;
- obliga a usar `effective_context` y `effective_signals` juntos;
- mantiene la semántica temporal en Admission;
- permite file budget aditivo y reversible;
- mantiene Kernel y Security sin cambios.

---

## 5. Problema exacto de G1

G1 debe diseñar una frontera que cumpla simultáneamente:

```text
1. non-READY projection -> no Admission call
2. READY projection -> exact binding checks
3. effective context -> used by Admission
4. effective signals -> used by Admission
5. original trust-sensitive control -> cannot influence decision
6. Admission precedence -> remains owned by existing evaluator
7. current evaluation time -> remains meaningful
8. no persistence
9. no runtime wiring
10. no new authority
```

La frontera no debe responder:

```text
¿cómo se producen assessments?
¿cómo se calcula provenance?
¿cómo se autoriza al productor?
¿cómo se proyectan inputs?
¿debe persistirse una decisión ELIGIBLE?
¿cómo se recupera Memory?
¿cómo se promueve a Knowledge?
```

---

## 6. Separaciones obligatorias

```text
CONTENT
!= ASSESSMENT
!= STRUCTURAL PROVENANCE
!= PRODUCER AUTHORIZATION
!= GOVERNED TEMPORAL CONTROL
!= GOVERNED INPUT PROJECTION
!= PROJECTION CONSUMPTION
!= ADMISSION DECISION
!= PERSISTENCE AUTHORIZATION
!= STORED MEMORY
!= AUTHORITY
```

También:

```text
Projection READY != Admission ELIGIBLE
Projection HOLD != Admission HOLD
Projection DENIED != Admission REJECT
Admission ELIGIBLE != Stored
Admission Decision != Persistence Authorization
candidate_id binding != cryptographic content integrity
```

---

## 7. Decisión G1-D1 — la frontera consume; no vuelve a proyectar

La frontera futura recibe una projection ya materializada.

No debe:

- recibir assessments individuales;
- revalidar Assessment Provenance;
- reejecutar Producer Authorization;
- volver a producir temporal evidence;
- llamar `project_governed_admission_inputs(...)` internamente;
- tener acceso a PDP/PEP;
- reconstruir evidence upstream.

Responsabilidad:

```text
validate consumption contract
        ↓
consume READY projection
        ↓
invoke existing Admission policy exactly once
```

Esto mantiene cada frontera con una sola responsabilidad.

---

## 8. Decisión G1-D2 — `HOLD` y `DENIED` nunca se reinterpretan como Admission

Una projection que no sea `READY` **no debe llamar** `evaluate_episodic_candidate(...)`.

Regla:

```text
Projection HOLD
    -> consumption BLOCKED
    -> no EpisodicAdmissionDecision

Projection DENIED
    -> consumption BLOCKED
    -> no EpisodicAdmissionDecision
```

Está prohibido:

```text
Projection HOLD   -> Admission HOLD
Projection DENIED -> Admission REJECT
```

porque los dos planos responden preguntas distintas.

El resultado de consumo deberá preservar suficiente razón para distinguir por qué no hubo evaluación, sin inventar una decisión de Admission.

---

## 9. Decisión G1-D3 — bindings mínimos antes de consumir READY

Una projection `READY` solo puede llegar al evaluator si el consumer valida como mínimo:

```text
projection is a GovernedAdmissionInputProjection
candidate is an EpisodicMemoryCandidate
projection.candidate_id == candidate.candidate_id
projection.outcome == READY
projection.reason_code == READY
projection.effective_context is present
projection.effective_signals is present
projection.policy_version == supported projection policy version
```

Aunque el constructor de `GovernedAdmissionInputProjection` ya impone varios invariantes, la frontera de consumo no debe depender de coerción ni de objetos duck-typed.

### 9.1. Metadata contextual neutral

La projection actual copia desde el candidate original:

```text
subject_scope
domain
purpose
```

Estos campos no son authority ni assessments, pero ayudan a detectar pairing accidental entre una projection y un candidate distinto con el mismo identificador lógico.

G1 requiere antes del consumo:

```text
projection.effective_context.subject_scope == candidate.control.subject_scope
projection.effective_context.domain        == candidate.control.domain
projection.effective_context.purpose       == candidate.control.purpose
```

Si hay mismatch:

```text
BLOCKED
no Admission call
```

Importante:

```text
metadata equality != trust grant
```

La applicability sigue siendo propiedad de `projection.effective_signals.scope_applicable`.

---

## 10. Decisión G1-D4 — policy-version binding explícito

Una projection `READY` no debe consumirse solo porque su shape coincide.

El consumer debe aceptar únicamente la versión de projection que conoce explícitamente.

Regla conceptual:

```text
projection.policy_version
== supported Governed Input Projection POLICY_VERSION
```

Si no coincide:

```text
BLOCKED
no Admission call
```

Esto evita que una projection obsoleta, experimental o producida bajo otra semántica sea tratada silenciosamente como equivalente.

No se permite:

```text
prefix matching
major-only matching
best effort compatibility
unknown version fallback
```

Una migración futura requerirá policy explícita.

---

## 11. Decisión G1-D5 — la policy de Admission debe consumir el contexto proyectado

El `EpisodicMemoryCandidate` original es inmutable y no debe modificarse.

La frontera futura deberá crear exclusivamente una **vista efectiva efímera de evaluación** con los mismos campos estructurales del candidate original salvo:

```text
control = projection.effective_context
```

Conceptualmente:

```text
effective_candidate_view = replace(
    original_candidate,
    control=projection.effective_context,
)
```

La forma exacta de implementación pertenece a G2/G3; G1 congela la semántica, no obliga a usar una función concreta.

La vista efectiva:

- existe solo en memoria durante la evaluación;
- no representa una nueva Memory;
- no recibe un nuevo `candidate_id`;
- no muta el candidate original;
- no debe retornarse como artefacto persistible;
- no debe exponerse a Conversation/runtime;
- no debe convertirse en fuente de truth;
- no debe sobrevivir al consumo salvo como detalle local de ejecución.

Así el evaluator existente observa:

```text
candidate_id     -> original logical identity
control          -> governed effective context
signals          -> governed effective signals
```

Y no puede volver a leer los valores trust-sensitive originales.

---

## 12. Decisión G1-D6 — Admission conserva toda la precedencia semántica

El consumer no debe inspeccionar `effective_signals` para decidir por sí mismo:

```text
REJECT
HOLD
ELIGIBLE
```

Tampoco debe duplicar checks de:

```text
policy_violation
scope_applicable
valid_until
TAINTED
REVOKED
missing classifications
valid_from
UNASSESSED
SUSPECT
sensitive review
contradiction review
```

Esas reglas permanecen exclusivamente en:

```python
evaluate_episodic_candidate(...)
```

El consumer solo crea el input efectivo correcto y delega la semántica al dueño actual de la policy.

```text
Consumption validates the bridge
Admission evaluates the policy
```

---

## 13. Decisión G1-D7 — tiempo de consumo fresco; no time travel

`GovernedAdmissionInputProjection.evaluated_at` indica cuándo la projection validó su evidence y materializó inputs efectivos.

No debe convertirse automáticamente en el tiempo de la decisión futura de Admission.

La frontera de consumo deberá recibir un `evaluated_at` actual, UTC-aware, para la evaluación de Admission.

Regla:

```text
consumption evaluated_at >= projection.evaluated_at
```

Si:

```text
consumption evaluated_at < projection.evaluated_at
```

entonces:

```text
BLOCKED
no Admission call
```

Esto evita evaluación temporal hacia atrás.

La igualdad es válida:

```text
consumption evaluated_at == projection.evaluated_at
```

Y una evaluación posterior también es válida siempre que Admission determine su resultado con el `effective_context` proyectado.

Ejemplo:

```text
projection READY at T1
valid_until = T2
consume at T3 where T3 >= T2
        ↓
Admission decides TEMPORAL_EXPIRED
```

Esto preserva la decisión G2 anterior:

```text
Temporal governance != Temporal admission semantics
```

### 13.1. No inventar TTL de projection

G1 no introduce un máximo arbitrario de edad para una projection.

```text
projection age alone != invalidity
```

Si en el futuro se necesita freshness adicional, revocation o supersession de projections, deberá existir policy explícita. No se inventará un TTL implícito en este adapter.

---

## 14. Decisión G1-D8 — resultado de consumo separado de Admission

La frontera necesita expresar dos estados conceptuales:

```text
EVALUATED
BLOCKED
```

Semántica:

```text
EVALUATED
= se validó el contrato de consumo y se ejecutó exactamente una vez la policy existente de Admission
= contiene EpisodicAdmissionDecision

BLOCKED
= la projection no era consumible o el binding de consumo falló
= no contiene EpisodicAdmissionDecision
```

G1 no congela todavía nombres Python ni reason codes definitivos. G2 deberá definirlos.

Razones conceptuales mínimas que G2 debe representar:

```text
projection_hold
projection_denied
candidate_binding_mismatch
context_binding_mismatch
unsupported_projection_policy
consumption_time_precedes_projection
evaluated
```

El resultado de consumo no debe producir un tercer motor de policy.

Su reason code explica **si pudo ejecutarse Admission**, no cuál fue la decisión de Admission.

---

## 15. Decisión G1-D9 — una evaluación exitosa devuelve la decisión original de Admission

Cuando el bridge sea consumible:

```text
READY projection
+ exact bindings
+ supported policy version
+ valid temporal ordering
        ↓
effective candidate view
        ↓
evaluate_episodic_candidate(...)
        ↓
EpisodicAdmissionDecision
```

La decisión contenida debe ser exactamente la producida por el evaluator existente.

El consumer no debe:

- copiar y modificar el outcome;
- cambiar el reason code;
- reescribir `evaluated_at` después de la llamada;
- alterar `policy_version` de Admission;
- convertir `ELIGIBLE` en autorización de storage.

---

## 16. Decisión G1-D10 — exactly-once local call, sin side effects

Para cada invocación consumible, la policy de Admission se llama exactamente una vez.

```text
0 calls when BLOCKED
1 call when EVALUATED
>1 calls prohibited
```

La frontera permanece:

- pura respecto de I/O;
- sin network;
- sin filesystem;
- sin database;
- sin logging obligatorio;
- sin metrics obligatorias;
- sin PDP/PEP;
- sin LLM;
- sin retries;
- sin background tasks.

Determinismo esperado:

```text
same candidate
+ same projection
+ same evaluated_at
= same consumption result
```

---

## 17. Decisión G1-D11 — candidate identity continúa siendo estructural v1

El baseline liga assessments, provenance, authorization y projection mediante identificadores lógicos como:

```text
assessment_id
candidate_id
request_id
```

`GovernedAdmissionInputProjection` no contiene actualmente un fingerprint del payload completo de `EpisodicMemoryCandidate`.

Por tanto, esta frontera puede comprobar:

```text
candidate_id equality
+
neutral context equality
```

pero no puede demostrar criptográficamente:

```text
origin integrity
experience payload integrity
content hash identity
external producer identity
```

Residual explícito:

```text
structural candidate binding
!= cryptographic candidate content integrity
```

G1 no introduce ahora un hash/fingerprint porque:

- el evaluator de Admission no consume `origin` ni `experience` para su policy;
- esta unidad no persiste, transmite ni ejecuta acciones externas;
- cambiar el contrato de projection ampliaría el scope de una unidad cuya necesidad puede resolverse sin ello.

Sin embargo, este residual **deberá reevaluarse antes de Persistence Authorization o de cualquier serialización/transporte externo de estas decisiones**.

No podrá asumirse que `candidate_id` por sí solo es suficiente para autorizar storage futuro.

---

## 18. Decisión G1-D12 — no revalidación retroactiva de authorization

La projection `READY` demuestra que, en su `evaluated_at`, los inputs necesarios pudieron ser materializados bajo la policy/version de projection vigente.

El consumer no volverá a consultar Security para preguntar si los productores continúan teniendo una sesión activa.

Esto evita confundir:

```text
authorized production at T1
```

con:

```text
producer must retain live authorization forever
```

La futura revocación sistémica de trust, taint propagation o invalidación de state derivado pertenece a una frontera posterior todavía no implementada.

Si esa capability aparece, podrá invalidar o quarantine state mediante policy propia. Este adapter no debe inventarla.

---

## 19. Decisión G1-D13 — file budget candidato para G2

Si G2 no encuentra un blocker nuevo, la implementación futura debería poder mantenerse en un delta aditivo mínimo equivalente a:

```text
NEW
src/malak/memory/governed_projection_consumption.py

NEW
tests/test_governed_projection_consumption.py

MODIFY existing production files = 0
```

En particular, G1 espera cero modificaciones en:

```text
src/malak/memory/episodic_admission.py
src/malak/memory/governed_input_projection.py
src/malak/memory/assessment_provenance.py
src/malak/memory/assessment_producer_authorization.py
src/malak/security/**
src/malak/kernel/**
Conversation/runtime
```

G2 debe verificar y congelar el file budget exacto.

Si la especificación descubre que no puede preservarse:

```text
STOP → ESCALATE → Owner decision
```

---

## 20. Output conceptual mínimo

G2 podrá definir un contrato equivalente a:

```text
GovernedAdmissionConsumptionResult
├── candidate_id
├── outcome: EVALUATED | BLOCKED
├── reason_code
├── evaluated_at
├── admission_decision: EpisodicAdmissionDecision | None
└── policy_version
```

Propiedades:

- inmutable;
- deterministic;
- `admission_decision` presente solo en `EVALUATED`;
- `BLOCKED` nunca contiene una decisión sintética;
- sin persistencia;
- sin authority;
- sin transport semantics.

G1 no congela nombres Python exactos.

---

## 21. Flujo objetivo después de una implementación futura

```text
EpisodicMemoryCandidate
        ↓
AdmissionAssessment
        ↓
Assessment Provenance
        ↓
Producer Authorization
        ↓
Governed Temporal Control
        ↓
Governed Input Projection
READY | HOLD | DENIED
        ↓
Governed Projection Consumption
        │
        ├── non-READY -> BLOCKED -> STOP
        │
        └── READY
              ↓
        effective candidate view
              ↓
        existing Episodic Admission
        REJECT | HOLD | ELIGIBLE
              ↓
              STOP
```

Incluso después de materializar esta unidad:

```text
ELIGIBLE
!= Persistence Authorization
!= Stored Memory
!= Retrieval Eligibility
!= Knowledge
!= Authority
```

---

## 22. Negative scenarios obligatorios para G2/TDD futuro

G2 deberá congelar tests negativos y positivos al menos para:

- **GC-A1 — Projection HOLD never calls Admission:** `HOLD` produce consumo bloqueado y cero `EpisodicAdmissionDecision`.
- **GC-A2 — Projection DENIED never calls Admission:** `DENIED` produce consumo bloqueado y no se convierte en `REJECT`.
- **GC-A3 — Candidate id mismatch:** projection y candidate con ids distintos bloquean antes del evaluator.
- **GC-A4 — Neutral scope mismatch:** `subject_scope` distinto bloquea.
- **GC-A5 — Neutral domain mismatch:** `domain` distinto bloquea.
- **GC-A6 — Neutral purpose mismatch:** `purpose` distinto bloquea.
- **GC-A7 — Unsupported projection policy:** version desconocida bloquea sin fallback.
- **GC-A8 — Evaluation time reversal:** `evaluated_at < projection.evaluated_at` bloquea.
- **GC-A9 — Equal evaluation time allowed:** igualdad temporal puede evaluar.
- **GC-A10 — Later evaluation allowed:** tiempo posterior puede evaluar sin TTL inventado.
- **GC-A11 — Original authority cannot leak:** un `candidate.control.source_authority_classification` conflictivo no debe ganar sobre `projection.effective_context`.
- **GC-A12 — Original confidence cannot leak:** confidence original no influye.
- **GC-A13 — Original sensitivity cannot leak:** sensitivity original no influye.
- **GC-A14 — Original valid_until cannot leak:** la expiración efectiva debe provenir de `projection.effective_context.valid_until`.
- **GC-A15 — Original valid_from cannot leak:** la validez inicial efectiva debe provenir de projection.
- **GC-A16 — Effective policy violation remains Admission-owned:** produce el mismo `POLICY_VIOLATION` del evaluator existente.
- **GC-A17 — Effective out-of-scope remains Admission-owned:** produce el mismo `OUT_OF_SCOPE`.
- **GC-A18 — Effective expired remains Admission-owned:** produce `TEMPORAL_EXPIRED` usando el contexto proyectado y el tiempo fresco.
- **GC-A19 — Effective future window remains Admission-owned:** produce `TEMPORAL_NOT_YET_VALID` cuando corresponde.
- **GC-A20 — TAINTED remains Admission-owned:** no se reimplementa precedencia.
- **GC-A21 — REVOKED remains Admission-owned:** no se reimplementa precedencia.
- **GC-A22 — SUSPECT remains Admission-owned:** produce el mismo `HOLD` del evaluator.
- **GC-A23 — Sensitive review remains Admission-owned:** no se interpreta en consumer.
- **GC-A24 — Contradiction review remains Admission-owned:** no se interpreta en consumer.
- **GC-A25 — ELIGIBLE remains only Admission eligibility:** el consumer no crea storage ni autorización.
- **GC-A26 — Candidate immutability:** el candidate original queda bit-for-bit semánticamente intacto.
- **GC-A27 — Effective candidate view does not escape:** no forma parte del output público.
- **GC-A28 — Exactly one evaluator call:** una invocación `EVALUATED` llama Admission una vez.
- **GC-A29 — Blocked means zero evaluator calls:** todos los blockers terminan antes de Admission.
- **GC-A30 — Determinism:** mismos inputs y tiempo producen mismo resultado.
- **GC-A31 — No I/O:** consumo no accede a red, disco, DB ni servicios.
- **GC-A32 — No PDP/PEP:** no se vuelve a decidir producer authorization.
- **GC-A33 — No projection recomputation:** el consumer no recibe ni evalúa upstream bundles.
- **GC-A34 — Admission decision preserved exactly:** outcome, reason, candidate id, evaluated_at y admission policy version no se reescriben.
- **GC-A35 — No persistence side effect:** incluso `ELIGIBLE` termina en STOP.

G2 puede ampliar esta matriz si descubre nuevos edges; no puede reducir los escenarios críticos sin justificación explícita.

---

## 23. Riesgos evaluados

### 23.1. Trust side-door desde `candidate.control`

Riesgo:

```text
HIGH
```

Mitigación de diseño:

```text
effective candidate view uses projection.effective_context
```

### 23.2. Semántica duplicada de Admission

Riesgo:

```text
HIGH
```

Mitigación:

```text
consumer never decides REJECT/HOLD/ELIGIBLE
```

### 23.3. Projection status reinterpretation

Riesgo:

```text
MEDIUM/HIGH
```

Mitigación:

```text
non-READY -> BLOCKED only
```

### 23.4. Stale/unknown projection semantics

Mitigación:

```text
exact projection policy-version binding
```

### 23.5. Time-of-check / time-of-use temporal semantics

Mitigación:

```text
fresh Admission evaluated_at
+
no time reversal
+
Admission re-evaluates valid_from/valid_until
```

### 23.6. Candidate logical-id collision or substitution

Residual:

```text
candidate_id + neutral metadata binding
!= cryptographic content integrity
```

Aceptable únicamente para esta frontera aislada sin persistencia ni transporte externo. Reevaluación obligatoria antes de Persistence Authorization.

---

## 24. FULL 4R — G1

### Risk — PASS

G1 identifica y bloquea:

- bypass de `effective_context`;
- conversión de Projection `HOLD/DENIED` en Admission outcomes;
- unknown projection version fallback;
- pairing candidate/projection incorrecto;
- time travel;
- duplicación de policy;
- persistencia implícita;
- authority expansion.

Residual principal:

```text
structural candidate binding != cryptographic content integrity
```

Ese residual no concede side effects en esta unidad y queda explícitamente bloqueante para reevaluación antes de persistencia/transporte externo.

### Readability — PASS

Responsabilidad única:

```text
READY governed projection
-> safe adapter
-> existing Admission evaluator
```

No se crea un `MemoryManager`, `TrustManager`, segundo Admission engine ni universal workflow.

### Reliability — PASS

La propuesta conserva:

- exact candidate binding;
- neutral context consistency;
- exact policy version;
- monotonic evaluation time;
- immutable original candidate;
- one-call semantics;
- existing Admission precedence;
- deterministic result.

### Resilience — PASS

Invalid, mismatched, unknown-version o time-reversed inputs degradan a `BLOCKED` antes de alcanzar Admission.

No existe fallback a valores menos gobernados.

---

## 25. Cuatro preguntas obligatorias

```text
1. ¿Respeta Blueprint?               PASS
2. ¿Respeta Cognitive Constitution? PASS
3. ¿Respeta Governance?             PASS
4. ¿Kernel permanece simple?        PASS
```

Razones:

- responsabilidad localizada en Memory Layer;
- no introduce autoridad cognitiva nueva;
- no modifica permisos;
- Human in Control intacto;
- Zero Trust reforzado al cerrar un side-door;
- Kernel delta = 0;
- Security Control Plane delta = 0;
- Admission sigue siendo dueño único de `REJECT | HOLD | ELIGIBLE`.

---

## 26. Preguntas que G2 debe congelar

Antes de cualquier código, G2 deberá definir de forma exacta:

1. nombre del módulo y API pública candidata;
2. contrato exacto del resultado `EVALUATED | BLOCKED`;
3. reason codes exactos y precedencia de blockers;
4. policy version propia de la frontera de consumo;
5. binding exacto a la versión de Governed Input Projection;
6. reglas de tipo y error de argumentos programáticamente inválidos;
7. si el effective candidate view se crea mediante `dataclasses.replace(...)` o construcción explícita equivalente;
8. garantía de que esa vista no escapa del módulo;
9. comparación exacta de `subject_scope/domain/purpose`;
10. semántica UTC y `consumption evaluated_at >= projection.evaluated_at`;
11. comportamiento exacto de `HOLD` y `DENIED` sin sintetizar Admission decisions;
12. invariantes de exactly-one Admission call;
13. file budget final;
14. matriz TDD completa;
15. bounded correction budget;
16. FULL 4R e independent validation;
17. residual de candidate content integrity y condición de reevaluación antes de persistencia;
18. evidencia candidate-bound / RDD Stage 1 requerida.

---

## 27. STOP conditions

Detener y volver al Owner si G2 o una implementación futura requiere:

- modificar Kernel;
- modificar Blueprint o Constituciones;
- modificar Governance Constitution;
- modificar `SecurityContext`, PDP o PEP;
- modificar permisos o scopes de seguridad;
- modificar `episodic_admission.py`;
- modificar `governed_input_projection.py`;
- reimplementar reglas de `REJECT | HOLD | ELIGIBLE`;
- confiar en `candidate.control` trust-sensitive;
- mapear Projection `HOLD/DENIED` a Admission outcomes;
- persistencia;
- retrieval;
- Knowledge;
- Conversation/runtime wiring;
- network, agents o tools;
- dependencia externa;
- identidad criptográfica ficticia;
- TTL de projection inventada sin policy;
- universal trust manager;
- Sprint 7.12;
- RDD Stage 2;
- implementación antes de reconciliar Project Vault.

---

## 28. Resultado G1

G1 concluye que existe una solución mínima compatible con el baseline:

```text
Governed Input Projection
        ↓
validate consumption bindings
        ↓
READY?
 ┌──────┴──────┐
 no            sí
 ↓             ↓
BLOCKED   effective candidate view
               ↓
       existing Admission policy
               ↓
        REJECT | HOLD | ELIGIBLE
               ↓
              STOP
```

Disposición:

```text
G1 RESULT: PASS
selected design: minimal additive adapter
risk class: 3 — HIGH
Kernel delta: 0
Security authority delta: 0
Admission policy duplication: 0
implementation authorized: false
G2 authorized by this document: false
```

El siguiente gate, si el Owner lo autoriza después de revisar e integrar este design record y reconciliar el Vault, es:

```text
G2 — Implementation Candidate Specification
for
Episodic Admission Governed Projection Consumption Boundary
```

G2 deberá seguir siendo specification-only.

---

## 29. Principio de cierre

```text
Governed Projection proves usable effective inputs.
Consumption proves those inputs reach the existing Admission policy without bypass.
Admission decides eligibility.
None of them authorizes persistence.
```

En forma compacta:

```text
READY
!= ELIGIBLE
!= STORED
!= RETRIEVABLE
!= KNOWLEDGE
!= AUTHORITY
```
