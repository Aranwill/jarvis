---
title: Episodic Admission Governed Input Projection Boundary — G0/G1 Design Record
status: g1_design_review
authority: owner-approved design record
as_of_date: 2026-09-09
unit: Episodic Admission Governed Input Projection Boundary
gate: G1
source_baseline: b96e1802c47e447699f06f4a019241d119f747ef
risk_class: 3
vault_reconciliation_status_at_start: resolved
vault_head_at_start: 4bf73bd1ef1bfb6929f0562ee851cfebd2cdef6e
sync_agent_head_at_start: 71b21e0a192017353075954e06e2b55f5f8e2255
sdd_required: true
tdd_required_for_future_implementation: true
full_4r_required: true
rdd_stage_1: adopted
rdd_stage_2_authorized: false
implementation_authorized: false
admission_wiring_authorized: false
persistent_memory_authorized: false
retrieval_authorized: false
knowledge_implementation_authorized: false
sprint_7_12_authorized: false
vault_reconciliation_required_before_implementation: true
language: es
---

# Episodic Admission Governed Input Projection Boundary — G0/G1 Design Record

## 1. Estado de autoridad

El Owner autorizó **G1 exclusivamente para diseño** de la unidad mínima:

```text
Episodic Admission Governed Input Projection Boundary
```

Esta autorización permite registrar el resultado formal de G0 y definir cómo una futura frontera podrá proyectar inputs efectivos de admisión a partir de assessments con provenance y autorización de productor gobernadas, sin ejecutar todavía la policy de admisión.

No autoriza:

- código productivo;
- tests de implementación;
- cambios a `episodic_admission.py`;
- cambios a `assessment_provenance.py`;
- cambios a `assessment_producer_authorization.py`;
- cambios a Kernel, SecurityContext, PDP o PEP;
- wiring con Conversation o runtime;
- persistencia, retrieval o Knowledge;
- agentes, tools o red;
- identidad criptográfica nueva;
- Sprint 7.12;
- RDD Stage 2;
- merge sin revisión humana.

```text
Design != Implementation
Projection READY != Admission ELIGIBLE
Admission != Persistence Authorization
Evidence != Authority
```

---

## 2. Baseline y estado cross-repository

Baseline fuente congelado para G0/G1:

```text
Aranwill/jarvis
main
b96e1802c47e447699f06f4a019241d119f747ef
```

Estado verificado al iniciar G1:

```text
Malāk main:
b96e1802c47e447699f06f4a019241d119f747ef

Project Vault main:
4bf73bd1ef1bfb6929f0562ee851cfebd2cdef6e

Vault Sync Agent main:
71b21e0a192017353075954e06e2b55f5f8e2255

post-reconciliation dry-run:
base_commit == head_commit == b96e1802...
changed_files = 0
document_candidates = 0
validation_findings = 0
conclusion = pass
proposal_created = false
```

Por tanto:

```text
BASELINE_DRIFT = 0
PROJECTION_DRIFT = 0
STATE_DRIFT = 0
```

Si este design record se integra, el Vault deberá reconciliarse otra vez antes de cualquier implementación posterior.

---

## 3. Resultado formal G0

La unidad inicialmente considerada era:

```text
Assessment Provenance
+
Producer Authorization
        ↓
direct Episodic Admission wiring
```

Resultado:

```text
DIRECT WIRING: NOT YET
```

Motivo: el baseline ya gobierna ocho dimensiones mediante `AdmissionAssessment`, provenance estructural y producer authorization, pero `episodic_admission.py` todavía consume adicionalmente metadata de control y temporal validity mediante `EpisodicAdmissionContext`.

En particular:

```text
valid_from
valid_until
```

pueden cambiar directamente `HOLD` / `REJECT` y no forman parte de las ocho assessments gobernadas actuales.

Un adapter directo dejaría una vía lateral no demostrada:

```text
8 governed assessments
        +
unproven temporal control
        ↓
Admission
```

Eso no satisface Zero Trust ni la separación histórica:

```text
source authority
!= confidence
!= source security status
!= temporal validity
```

G0 selecciona por tanto:

```text
Episodic Admission Governed Input Projection Boundary
```

Disposición:

```text
G0 RESULT: PASS
candidate disposition: ADAPT
risk class: 3 — HIGH
blocking findings: 0
implementation authorized: false
```

---

## 4. Problema exacto

El baseline dispone ahora de tres fronteras independientes:

```text
AdmissionAssessment
        ↓
Assessment Provenance
VALID | HOLD | INVALID
        ↓
Producer Authorization
AUTHORIZED | HOLD | DENIED
```

Y por separado:

```text
EpisodicMemoryCandidate
+
EpisodicAdmissionSignals
        ↓
Episodic Admission
REJECT | HOLD | ELIGIBLE
```

Falta una frontera que responda únicamente:

> ¿pueden estas evidencias gobernadas materializar un conjunto completo, coherente y candidate-bound de inputs efectivos para la policy de admisión?

No debe responder todavía:

```text
¿es el candidate ELIGIBLE?
¿debe persistirse?
¿debe recuperarse?
¿debe promoverse a Knowledge?
```

---

## 5. Separaciones obligatorias

```text
CONTENT
!= ASSESSMENT
!= STRUCTURAL PROVENANCE
!= PRODUCER AUTHORIZATION
!= GOVERNED TEMPORAL CONTROL
!= EFFECTIVE ADMISSION INPUT
!= ADMISSION DECISION
!= PERSISTENCE AUTHORIZATION
!= AUTHORITY
```

También:

```text
AUTHORIZED assessment != trusted truth
Projection READY != ELIGIBLE
Projection HOLD != admission HOLD automatically
Projection DENIED != candidate REJECT automatically
candidate.control field present != field authorized for effective admission
```

---

## 6. Decisión G1-D1 — Projection no ejecuta Admission

La frontera futura deberá terminar después de construir inputs efectivos y nunca llamar por sí misma:

```python
evaluate_episodic_candidate(...)
```

Flujo objetivo:

```text
governed evidence
        ↓
projection validation
        ↓
READY | HOLD | DENIED
        ↓
STOP
```

Un wiring posterior, autorizado separadamente, podrá decidir cómo consumir una proyección `READY`.

---

## 7. Decisión G1-D2 — los valores efectivos se reconstruyen, no se heredan por confianza implícita

`EpisodicMemoryCandidate.control` puede contener estructuralmente:

```text
subject_scope
domain
purpose
source_authority_classification
confidence_classification
sensitivity_classification
valid_from
valid_until
```

Pero la futura proyección no debe considerar automáticamente autoritativos los campos que influyen trust/admission solo porque ya estén presentes en el candidate.

Regla:

```text
candidate.control value present
!= governed effective admission value
```

Para las dimensiones cubiertas por `AdmissionAssessment`, el valor efectivo deberá provenir del assessment correcto con:

```text
provenance = VALID
producer authorization = AUTHORIZED
candidate binding = exact
kind binding = exact
```

La proyección deberá construir un nuevo conjunto efectivo de inputs. No debe mutar el candidate original.

---

## 8. Decisión G1-D3 — metadata contextual neutral permanece separada

Los campos:

```text
subject_scope
domain
purpose
```

se conservan como metadata contextual del candidate, no como assessments de trust.

G1 permite que una futura proyección los copie desde el `EpisodicAdmissionContext` inmutable original siempre que el candidate binding sea el esperado.

Pero:

```text
subject_scope/domain/purpose
cannot by themselves create READY
cannot replace SCOPE_APPLICABLE
cannot grant producer authority
cannot create ELIGIBLE
```

La applicability efectiva sigue dependiendo del assessment gobernado `SCOPE_APPLICABLE`.

---

## 9. Decisión G1-D4 — mapping cerrado de assessments a inputs efectivos

La proyección futura deberá usar un mapping explícito y cerrado:

| AssessmentKind | Effective target |
|---|---|
| `SOURCE_AUTHORITY` | `control.source_authority_classification` |
| `CONFIDENCE` | `control.confidence_classification` |
| `SENSITIVITY` | `control.sensitivity_classification` |
| `SOURCE_SECURITY_STATUS` | `signals.source_security_status` |
| `SCOPE_APPLICABLE` | `signals.scope_applicable` |
| `POLICY_VIOLATION` | `signals.policy_violation` |
| `SENSITIVE_REVIEW_REQUIRED` | `signals.sensitive_review_required` |
| `CONTRADICTION_REQUIRES_REVIEW` | `signals.contradiction_requires_review` |

No se permiten:

```text
string-based dynamic field names
implicit fallback to candidate.control
last-write-wins
LLM-selected mapping
unknown assessment kinds
```

---

## 10. Decisión G1-D5 — cardinalidad exacta; no "último gana"

Para cada dimensión requerida por la projection v1 debe existir exactamente un assessment utilizable.

```text
0 usable assessments for required kind -> HOLD
1 usable assessment                  -> continue
>1 usable assessments                -> HOLD
```

G1 prohíbe elegir por:

```text
list order
timestamp order
latest wins
highest confidence
producer role priority
lexicographic order
```

sin una policy de resolución de conflictos aprobada.

Incluso dos assessments autorizadas con el mismo valor representan ambigüedad de cardinalidad y no deben colapsarse silenciosamente en v1.

```text
multiple usable inputs -> HOLD
```

Una futura unidad podrá introducir supersession/conflict-resolution gobernada si aparece una necesidad real.

---

## 11. Decisión G1-D6 — resultado previo de provenance/autorización debe ser exacto

Un assessment solo puede proyectarse si sus decisiones previas están completas y ligadas al mismo objeto:

```text
assessment.assessment_id
== provenance_decision.assessment_id
== producer_authorization_decision.assessment_id

assessment.candidate_id
== provenance_decision.candidate_id
== producer_authorization_decision.candidate_id
== expected candidate_id

assessment.kind
== provenance_decision.kind
== producer_authorization_decision.kind
```

Y además:

```text
provenance outcome = VALID
producer authorization outcome = AUTHORIZED
```

Cualquier mismatch estructural debe fallar cerrado.

`HOLD`, `INVALID` o `DENIED` previos no se reinterpretan como valores de admisión.

---

## 12. Decisión G1-D7 — type semantics permanecen cerradas

La proyección deberá validar el tipo esperado de cada dimensión antes de materializar inputs efectivos:

```text
SOURCE_AUTHORITY            -> canonical str
CONFIDENCE                  -> canonical str
SENSITIVITY                 -> canonical str
SOURCE_SECURITY_STATUS      -> closed SourceSecurityStatus value
SCOPE_APPLICABLE            -> bool
POLICY_VIOLATION            -> bool
SENSITIVE_REVIEW_REQUIRED   -> bool
CONTRADICTION_REQUIRES_REVIEW -> bool
```

Un valor estructuralmente permitido por `AdmissionAssessment` pero semánticamente inválido para su target no se coerciona.

Ejemplos prohibidos:

```text
"false" -> False
"acceptable " -> ACCEPTABLE
1 -> True
unknown security string -> UNASSESSED
```

La ausencia o incompatibilidad debe degradar a `HOLD` o `DENIED` según el tipo de finding que G2 congele.

---

## 13. Decisión G1-D8 — temporal validity es un control gobernado separado

`valid_from` y `valid_until` afectan directamente la policy de admisión y por tanto no pueden considerarse confiables por mera presencia en `candidate.control`.

Regla:

```text
candidate.control.valid_from / valid_until
!= governed temporal validity by themselves
```

G1 preserva temporal validity como dimensión separada de authority/confidence/security status.

La futura projection v1 solo podrá alcanzar `READY` si dispone de **evidencia temporal gobernada** ligada al mismo candidate y a una policy/regla identificable.

G1 no inventa todavía una falsa autoridad temporal. G2 deberá escoger una única forma mínima y verificable entre opciones compatibles con la arquitectura, por ejemplo:

```text
A) deterministic policy-derived temporal envelope
   with explicit policy/version binding

or

B) dedicated governed temporal assessment/evidence
   with producer authorization
```

No se permitirá fallback dual silencioso.

Hasta que G2 congele el contrato:

```text
missing governed temporal control -> HOLD
```

Y siempre:

```text
valid_until absent != valid forever
```

---

## 14. Decisión G1-D9 — la projection no reimplementa la precedencia de admission

La precedencia de:

```text
policy violation
out of scope
expired
TAINTED / REVOKED
missing assessments
review conditions
ELIGIBLE
```

permanece propiedad de `evaluate_episodic_candidate(...)`.

La projection no debe decidir cuál de dos inputs de admisión "gana" semánticamente. Solo demuestra que cada input efectivo está completo, gobernado, ligado y representable.

```text
Projection validates inputs
Admission evaluates policy
```

---

## 15. Resultado conceptual de projection

G1 adopta conceptualmente tres resultados para G2:

```text
READY
HOLD
DENIED
```

Semántica:

```text
READY
= existe un conjunto completo y coherente de inputs efectivos gobernados
!= ELIGIBLE

HOLD
= falta evidencia, temporal control, cardinalidad única o clasificación verificable
!= admission HOLD automatically

DENIED
= existe mismatch/tampering/incompatibilidad estructural que no debe reutilizarse
!= candidate REJECT automatically
```

G2 decidirá nombres y reason codes exactos.

---

## 16. Output conceptual mínimo

Una futura implementation candidate podrá representar algo equivalente a:

```text
GovernedAdmissionInputProjection
├── candidate_id
├── outcome: READY | HOLD | DENIED
├── reason_code
├── effective_context: EpisodicAdmissionContext | None
├── effective_signals: EpisodicAdmissionSignals | None
├── evaluated_at
└── policy_version
```

Propiedades:

- inmutable;
- deterministic;
- sin I/O;
- sin persistence;
- sin network;
- sin LLM;
- sin PDP/PEP calls;
- sin mutación del candidate;
- `effective_context/signals` presentes solo cuando la semántica de G2 lo permita.

Este contrato es conceptual en G1; nombres exactos pertenecen a G2.

---

## 17. Negative scenarios obligatorios para G2/TDD futuro

- **GP-A1 — Candidate control cannot bypass assessment governance:** un valor preexistente de source authority/confidence/sensitivity no sustituye assessment autorizada.
- **GP-A2 — Temporal side-door blocked:** `valid_until` presente en candidate no basta para READY.
- **GP-A3 — Missing required assessment:** ausencia de una dimensión requerida produce HOLD.
- **GP-A4 — Duplicate same-kind assessment:** dos inputs utilizables del mismo kind producen HOLD; no last-write-wins.
- **GP-A5 — Conflicting same-kind assessment:** `ACCEPTABLE` + `SUSPECT` no se resuelve por orden.
- **GP-A6 — Provenance HOLD cannot project:** no genera control efectivo.
- **GP-A7 — Provenance INVALID cannot project:** no genera control efectivo.
- **GP-A8 — Authorization HOLD cannot project:** no genera control efectivo.
- **GP-A9 — Authorization DENIED cannot project:** no genera control efectivo ni hard reject downstream automático.
- **GP-A10 — Assessment id mismatch:** falla cerrado.
- **GP-A11 — Candidate id mismatch:** falla cerrado.
- **GP-A12 — Kind mismatch:** falla cerrado.
- **GP-A13 — Wrong bool type:** string `"false"` no se coerciona a bool.
- **GP-A14 — Unknown security status:** no se convierte en `UNASSESSED` por defecto.
- **GP-A15 — Neutral metadata cannot authorize:** subject_scope/domain/purpose no crean READY por sí mismos.
- **GP-A16 — SCOPE_APPLICABLE remains governed:** scope label no sustituye assessment de applicability.
- **GP-A17 — Missing temporal evidence:** HOLD.
- **GP-A18 — Temporal candidate mismatch:** falla cerrado.
- **GP-A19 — Unbounded temporal validity:** no implica validez eterna.
- **GP-A20 — Projection READY does not call Admission:** cero side effect y cero `EpisodicAdmissionDecision`.
- **GP-A21 — Projection READY does not persist:** cero storage/retrieval.
- **GP-A22 — Determinism:** mismos inputs producen mismo resultado.

---

## 18. FULL 4R — G1

### Risk — PASS

Se evaluaron bypass mediante `candidate.control`, temporal trust side-door, duplicate/last-write-wins, conflicting assessments, authorization confusion, unauthorized negative-value DoS, type coercion, authority inversion y acoplamiento prematuro a Admission.

Riesgo residual principal:

```text
temporal governance contract not yet frozen
```

Ese residual es deliberadamente bloqueante para `READY` y deberá resolverse en G2 antes de implementación.

### Readability — PASS

Una sola responsabilidad:

```text
governed evidence
-> effective admission input projection
```

No se crea `MemoryManager`, `TrustManager`, policy engine universal ni segundo admission engine.

### Reliability — PASS

G2 deberá conservar cardinalidad exacta, mapping cerrado, candidate/kind/assessment binding, tipos estrictos, inputs inmutables, determinismo y fail-closed.

### Resilience — PASS

Missing, duplicate, ambiguous, mismatched o temporally ungoverned inputs degradan a `HOLD`/`DENIED`, nunca a mayor trust o a `READY` por defecto.

---

## 19. Cuatro preguntas obligatorias

```text
1. ¿Respeta Blueprint?               PASS
2. ¿Respeta Cognitive Constitution? PASS
3. ¿Respeta Governance?             PASS
4. ¿Kernel permanece simple?        PASS
```

Razones:

- responsabilidad dentro de Memory Layer;
- cognition/evidence no se convierten en authority;
- no se amplían permisos;
- Human in Control intacto;
- Kernel delta = 0;
- Security Control Plane sin cambios;
- Admission policy sigue siendo una frontera separada.

---

## 20. STOP conditions

Detener y volver al Owner si G2 o una implementación futura requiere:

- modificar Kernel;
- modificar Constituciones o Blueprint;
- modificar SecurityContext, PDP o PEP;
- ejecutar PDP/PEP desde esta frontera;
- modificar `episodic_admission.py` sin autorización separada;
- mutar el candidate original;
- introducir fallback a campos no gobernados;
- resolver conflicts por orden implícito;
- persistencia, retrieval o Knowledge;
- runtime/Conversation wiring;
- LLM como productor de autoridad;
- red, agents o tools;
- dependencia externa;
- identidad criptográfica ficticia;
- taxonomía global de trust;
- Sprint 7.12;
- RDD Stage 2.

---

## 21. Preguntas que G2 debe congelar

1. contrato exacto de `GovernedAdmissionInputProjection`;
2. reason codes y precedencia de `READY | HOLD | DENIED`;
3. representación exacta del bundle assessment + provenance + authorization;
4. cardinalidad y colección de inputs;
5. comportamiento exacto ante provenance/authorization HOLD versus DENIED/INVALID;
6. parsing explícito de `SourceSecurityStatus` sin coerción;
7. forma mínima y única de **governed temporal control**;
8. binding de temporal evidence a candidate + policy/version;
9. si `effective_context/signals` solo existen en READY;
10. file budget del candidate de implementación;
11. escenarios TDD y bounded correction budget;
12. cómo un futuro wiring consume READY sin modificar semántica de Admission.

G2 no deberá resolver persistencia ni retrieval.

---

## 22. Resultado G1

```text
G1 RESULT: PASS
unit: Episodic Admission Governed Input Projection Boundary
risk class: 3 — HIGH
design accepted: true
blocking findings: 0
implementation authorized: false
admission wiring authorized: false
persistent memory authorized: false
retrieval authorized: false
knowledge authorized: false
sprint 7.12 authorized: false
rdd stage 2 authorized: false
vault reconciliation required before implementation: true
```

Próximo paso permitido únicamente mediante nueva autorización del Owner:

```text
G2 — Implementation Candidate Specification
```
