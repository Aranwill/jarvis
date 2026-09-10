---
title: Episodic Admission Governed Projection Consumption Boundary — G2 Implementation Candidate Specification
status: g2_implementation_candidate_spec_review
authority: owner-approved specification record
as_of_date: 2026-09-10
unit: Episodic Admission Governed Projection Consumption Boundary
gate: G2
source_baseline: aaabae65fcd989ed698704fa1bc735c3896c3903
risk_class: 3
vault_reconciliation_status_at_start: resolved
vault_head_at_start: 4b504f258d110b646fe062e846abe6893e0749a1
vault_reflects_malak_head: aaabae65fcd989ed698704fa1bc735c3896c3903
sync_agent_head_at_start: 71b21e0a192017353075954e06e2b55f5f8e2255
sdd_required: true
tdd_required: true
full_4r_required: true
rdd_stage_1: adopted
rdd_stage_2_authorized: false
implementation_authorized: false
admission_consumption_implementation_authorized: false
episodic_admission_modification_authorized: false
governed_input_projection_modification_authorized: false
security_control_plane_change_authorized: false
runtime_wiring_authorized: false
persistent_memory_authorized: false
retrieval_authorized: false
knowledge_implementation_authorized: false
sprint_7_12_authorized: false
vault_reconciliation_required_before_implementation: true
language: es
---

# Episodic Admission Governed Projection Consumption Boundary — G2 Implementation Candidate Specification

## 1. Estado de autoridad

El Owner autorizó avanzar con **G2 exclusivamente como Specification-Driven Development** para la unidad:

```text
Episodic Admission Governed Projection Consumption Boundary
```

G2 congela el contrato exacto de consumo, resultados, reason codes, precedencia, binding, tiempo, adapter efímero, matriz TDD, file budget, FULL 4R, bounded correction y evidencia candidate-bound requerida para una futura implementación.

G2 **no autoriza todavía implementación**.

No autoriza:

- código productivo;
- tests de implementación;
- modificar `episodic_admission.py`;
- modificar `governed_input_projection.py`;
- modificar Assessment Provenance o Producer Authorization;
- modificar SecurityContext, PDP, PEP o permisos;
- modificar Kernel;
- wiring con Conversation/runtime;
- persistencia de Memory;
- retrieval;
- Knowledge;
- agentes, tools o red;
- dependencias nuevas;
- identidad o integridad criptográfica nueva;
- Sprint 7.12;
- RDD Stage 2;
- promoción a Ready o merge sin decisión humana.

```text
Specification != Implementation
Projection READY != Admission ELIGIBLE
Admission ELIGIBLE != Persistence Authorization
Evidence != Authority
```

---

## 2. Baseline exacto y precondiciones

Baseline fuente congelado:

```text
Aranwill/jarvis
main
aaabae65fcd989ed698704fa1bc735c3896c3903
```

Ese commit integra PR #90 — G0/G1 de esta misma unidad.

Estado cross-repository verificado al iniciar G2:

```text
Malāk main:
aaabae65fcd989ed698704fa1bc735c3896c3903

Project Vault main:
4b504f258d110b646fe062e846abe6893e0749a1

Vault refleja Malāk HEAD:
aaabae65fcd989ed698704fa1bc735c3896c3903

Vault Sync Agent main:
71b21e0a192017353075954e06e2b55f5f8e2255
```

La reconciliación fue aceptada explícitamente por el Owner y el dry-run posterior reportó:

```text
base_commit == head_commit == aaabae65fcd989ed698704fa1bc735c3896c3903
changed_files = 0
document_candidates = 0
validation_findings = 0
conclusion = pass
proposal_created = false
```

Precondiciones:

```text
G0 PASS / ADAPT
G1 PASS + integrated
Vault reconciliation PASS
BASELINE_DRIFT = 0
PROJECTION_DRIFT = 0
STATE_DRIFT = 0
```

Si este G2 se integra, el Vault deberá reconciliarse nuevamente antes de una futura implementación G3.

---

## 3. Método de construcción obligatorio

La unidad conserva la disciplina vigente:

```text
G0 need analysis
  ↓
G1 design
  ↓
G2 exact specification
  ↓
Owner authorization for implementation
  ↓
TDD RED
  ↓
minimal GREEN
  ↓
REFACTOR only when justified
  ↓
FULL 4R
  ↓
Bounded Correction
  ↓
Independent Validation
  ↓
Candidate-Bound Evidence / RDD Stage 1
  ↓
Draft PR
  ↓
Human review / Ready / merge
  ↓
Vault reconciliation
```

Invariantes:

```text
Writer != Reviewer != Validator != Authority
Evidence != Receipt != Validation != Decision != Authority
candidate changes -> prior candidate-bound evidence becomes stale
```

---

## 4. Problema exacto

El baseline dispone de:

```text
Governed Input Projection
READY | HOLD | DENIED
```

Una projection `READY` contiene:

```text
effective_context: EpisodicAdmissionContext
effective_signals: EpisodicAdmissionSignals
```

Y por separado existe la policy:

```text
EpisodicMemoryCandidate
+
EpisodicAdmissionSignals
        ↓
evaluate_episodic_candidate(...)
        ↓
REJECT | HOLD | ELIGIBLE
```

El evaluator vigente lee:

```python
control = candidate.control
```

Por ello, pasar el candidate original junto con `projection.effective_signals` reabriría trust-sensitive metadata desde `candidate.control` y descartaría el `effective_context` gobernado.

La unidad debe resolver únicamente:

> entregar conjuntamente el contexto y las señales gobernadas a la policy existente de Admission, sin mutar el candidate original, sin duplicar Admission y sin reinterpretar `HOLD/DENIED` de Projection.

---

## 5. Separaciones obligatorias

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
!= RETRIEVAL ELIGIBILITY
!= KNOWLEDGE
!= AUTHORITY
```

Y explícitamente:

```text
Projection READY != Admission ELIGIBLE
Projection HOLD != Admission HOLD
Projection DENIED != Admission REJECT
Admission ELIGIBLE != Stored
candidate_id binding != cryptographic candidate content integrity
```

---

## 6. Decisión G2-D1 — file budget exacto del candidato G3

La futura implementación queda limitada a exactamente dos archivos nuevos:

```text
NEW
src/malak/memory/governed_projection_consumption.py

NEW
tests/test_governed_projection_consumption.py

MODIFY existing production files = 0
```

No se modifica:

```text
src/malak/memory/__init__.py
src/malak/memory/episodic_admission.py
src/malak/memory/governed_input_projection.py
src/malak/memory/assessment_provenance.py
src/malak/memory/assessment_producer_authorization.py
src/malak/security/**
src/malak/kernel/**
Conversation/runtime
```

La API candidata será importable desde su módulo explícito; G2 no exige re-export en `malak.memory`.

Si G3 necesita ampliar este budget:

```text
STOP → ESCALATE → Owner decision
```

---

## 7. Decisión G2-D2 — módulo y policy version exactos

Módulo candidato:

```text
malak.memory.governed_projection_consumption
```

Policy version propia:

```python
POLICY_VERSION = "episodic-admission-governed-projection-consumption/v1"
```

La versión soportada de upstream projection es exactamente el `POLICY_VERSION` integrado por:

```text
malak.memory.governed_input_projection
```

Actualmente:

```text
episodic-admission-governed-input-projection/v1
```

No se permite:

```text
prefix matching
major-only matching
semantic best effort
unknown-version fallback
silent migration
```

---

## 8. Decisión G2-D3 — API principal exacta

El módulo candidato expondrá:

```python
POLICY_VERSION
GovernedAdmissionConsumptionOutcome
GovernedAdmissionConsumptionReason
GovernedAdmissionConsumptionResult
consume_governed_admission_projection(...)
```

Firma exacta candidata:

```python
def consume_governed_admission_projection(
    candidate: EpisodicMemoryCandidate,
    projection: GovernedAdmissionInputProjection,
    evaluated_at: datetime,
) -> GovernedAdmissionConsumptionResult:
    ...
```

No recibe:

- assessments;
- provenance decisions;
- producer authorization evidence;
- temporal evidence;
- PDP/PEP;
- SecurityContext;
- DB;
- filesystem;
- network;
- LLM;
- tool context;
- persistence handle.

---

## 9. Decisión G2-D4 — resultado exacto `EVALUATED | BLOCKED`

```python
class GovernedAdmissionConsumptionOutcome(StrEnum):
    EVALUATED = "evaluated"
    BLOCKED = "blocked"
```

Semántica:

```text
EVALUATED
= el bridge de consumo fue validado
= Admission fue ejecutado exactamente una vez
= contiene la EpisodicAdmissionDecision original

BLOCKED
= el bridge no es consumible bajo esta policy
= Admission no fue ejecutado
= no contiene EpisodicAdmissionDecision
```

`BLOCKED` nunca sintetiza `REJECT`, `HOLD` o `ELIGIBLE`.

---

## 10. Decisión G2-D5 — reason codes exactos

```python
class GovernedAdmissionConsumptionReason(StrEnum):
    CANDIDATE_BINDING_MISMATCH = "candidate_binding_mismatch"
    UNSUPPORTED_PROJECTION_POLICY = "unsupported_projection_policy"
    CONSUMPTION_TIME_PRECEDES_PROJECTION = "consumption_time_precedes_projection"
    PROJECTION_DENIED = "projection_denied"
    PROJECTION_HOLD = "projection_hold"
    CONTEXT_BINDING_MISMATCH = "context_binding_mismatch"
    EVALUATED = "evaluated"
```

Estos reason codes explican exclusivamente si Admission pudo ser invocado.

No expresan ni sustituyen:

```text
EpisodicAdmissionReason
GovernedAdmissionProjectionReason
Persistence Authorization
```

---

## 11. Decisión G2-D6 — contrato exacto de output

```python
@dataclass(frozen=True, slots=True)
class GovernedAdmissionConsumptionResult:
    candidate_id: str
    outcome: GovernedAdmissionConsumptionOutcome
    reason_code: GovernedAdmissionConsumptionReason
    evaluated_at: datetime
    admission_decision: EpisodicAdmissionDecision | None = None
    policy_version: str = POLICY_VERSION
```

Invariantes constructoras:

- `candidate_id` canonical, no vacío y sin whitespace periférico;
- `outcome` debe ser `GovernedAdmissionConsumptionOutcome`;
- `reason_code` debe ser `GovernedAdmissionConsumptionReason`;
- `evaluated_at` debe ser `datetime` UTC-aware exacto;
- `policy_version` canonical, no vacío y sin whitespace periférico;
- `EVALUATED` exige `reason_code == EVALUATED`;
- `EVALUATED` exige `admission_decision is not None`;
- `BLOCKED` prohíbe `reason_code == EVALUATED`;
- `BLOCKED` exige `admission_decision is None`;
- cuando existe `admission_decision`, su `candidate_id` debe coincidir con `candidate_id`;
- cuando existe `admission_decision`, su `evaluated_at` debe coincidir exactamente con `evaluated_at`.

El output no incluye ni expone el effective candidate view.

---

## 12. Decisión G2-D7 — argumentos programáticamente inválidos

Antes de semántica de consumo:

```text
candidate wrong type  -> TypeError
projection wrong type -> TypeError
evaluated_at wrong type -> TypeError
naive evaluated_at -> ValueError
aware non-UTC evaluated_at -> ValueError
```

No se coerciona:

```text
string timestamp -> datetime
substitute dict -> dataclass
string enum -> enum
```

Errores de programación no se convierten en `BLOCKED`.

`BLOCKED` está reservado a entradas bien tipadas cuya relación gobernada no puede consumirse.

---

## 13. Decisión G2-D8 — precedencia determinista de blockers

Después de type/UTC validation, el consumer aplica exactamente esta precedencia:

```text
1. CANDIDATE_BINDING_MISMATCH
2. UNSUPPORTED_PROJECTION_POLICY
3. CONSUMPTION_TIME_PRECEDES_PROJECTION
4. PROJECTION_DENIED
5. PROJECTION_HOLD
6. CONTEXT_BINDING_MISMATCH
7. EVALUATED
```

Racional:

- identity pairing se valida antes de interpretar semántica del objeto;
- unknown policy nunca se consume por shape;
- time reversal bloquea antes de ejecutar policy;
- `DENIED` se conserva como non-consumable sin convertirlo en Admission `REJECT`;
- `HOLD` se conserva como non-consumable sin convertirlo en Admission `HOLD`;
- neutral-context binding solo puede verificarse en `READY`, porque solo `READY` porta `effective_context`;
- únicamente después de esos checks se invoca Admission.

La precedencia es de bridge validation, no de Admission policy.

---

## 14. Decisión G2-D9 — candidate binding exacto

Primer binding semántico:

```text
projection.candidate_id == candidate.candidate_id
```

Mismatch:

```text
BLOCKED
CANDIDATE_BINDING_MISMATCH
Admission calls = 0
```

No se acepta:

- alias;
- case folding;
- whitespace normalization;
- substring;
- external lookup.

Residual:

```text
candidate_id equality != cryptographic payload integrity
```

---

## 15. Decisión G2-D10 — binding exacto de projection policy

Debe cumplirse:

```text
projection.policy_version
== governed_input_projection.POLICY_VERSION
```

Mismatch:

```text
BLOCKED
UNSUPPORTED_PROJECTION_POLICY
Admission calls = 0
```

La comparación es exacta.

---

## 16. Decisión G2-D11 — orden temporal exacto

El `evaluated_at` del consumer representa el tiempo actual de Admission.

Debe cumplirse:

```text
consumption evaluated_at >= projection.evaluated_at
```

Si:

```text
consumption evaluated_at < projection.evaluated_at
```

resultado:

```text
BLOCKED
CONSUMPTION_TIME_PRECEDES_PROJECTION
Admission calls = 0
```

Se permite igualdad.

Se permite tiempo posterior sin TTL inventado.

```text
projection age alone != invalidity
```

Admission reevaluará `valid_from` y `valid_until` usando ese tiempo fresco.

---

## 17. Decisión G2-D12 — `HOLD` y `DENIED` no se reinterpretan

```text
projection.outcome == DENIED
-> BLOCKED / PROJECTION_DENIED
-> zero Admission calls

projection.outcome == HOLD
-> BLOCKED / PROJECTION_HOLD
-> zero Admission calls
```

Prohibido:

```text
DENIED -> Admission REJECT
HOLD   -> Admission HOLD
```

El `reason_code` original de Projection permanece upstream y no se convierte en `EpisodicAdmissionReason`.

---

## 18. Decisión G2-D13 — READY requiere el contrato integrado, no duck typing

El consumer acepta únicamente una instancia real de:

```text
GovernedAdmissionInputProjection
```

El contrato integrado de projection ya garantiza para `READY`:

```text
reason_code == READY
effective_context is not None
effective_signals is not None
finding_kind is None
```

G3 no reconstruirá una segunda validator de invariantes internos de esa dataclass.

La frontera sí exige exact type validation, policy-version binding y sus propios bindings de consumo.

---

## 19. Decisión G2-D14 — neutral context binding exacto

Para una projection `READY`, antes de Admission:

```text
projection.effective_context.subject_scope == candidate.control.subject_scope
projection.effective_context.domain        == candidate.control.domain
projection.effective_context.purpose       == candidate.control.purpose
```

Si cualquiera difiere:

```text
BLOCKED
CONTEXT_BINDING_MISMATCH
Admission calls = 0
```

La comparación es exacta y conjunta.

No se añade un reason code por cada campo: la responsabilidad es el binding del contexto neutral completo.

```text
context equality != trust grant
```

Applicability sigue viniendo de `projection.effective_signals.scope_applicable`.

---

## 20. Decisión G2-D15 — effective candidate view exacta

Después de todos los blockers y solo para `READY`, G3 construirá una vista efímera equivalente a:

```python
effective_candidate = dataclasses.replace(
    candidate,
    control=projection.effective_context,
)
```

G2 selecciona **`dataclasses.replace(...)`** como forma preferida y exacta porque:

- conserva `candidate_id`;
- conserva `origin`;
- conserva `experience`;
- conserva `created_at`;
- reemplaza únicamente `control`;
- reutiliza el constructor/invariantes de `EpisodicMemoryCandidate`;
- no muta el original;
- evita construcción manual repetitiva.

Si G3 demuestra incompatibilidad técnica real con `replace`, debe STOP y escalar; no cambia silenciosamente la estrategia.

La vista:

```text
local only
not returned
not persisted
not serialized
not logged as new Memory
not exposed to runtime
not authority
```

---

## 21. Decisión G2-D16 — llamada exacta a Admission

Una vez construida la vista:

```python
admission_decision = evaluate_episodic_candidate(
    effective_candidate,
    projection.effective_signals,
    evaluated_at,
)
```

La función se invoca:

```text
exactly 1 time when EVALUATED
exactly 0 times when BLOCKED
```

No hay retries.

No hay segunda evaluación de confirmación.

No hay pre-evaluación parcial.

---

## 22. Decisión G2-D17 — Admission conserva toda la semántica

El consumer no inspecciona `effective_signals` o `effective_context` para decidir:

```text
POLICY_VIOLATION
OUT_OF_SCOPE
TEMPORAL_EXPIRED
TAINTED_SOURCE
REVOKED_SOURCE
missing classifications
TEMPORAL_NOT_YET_VALID
SOURCE_UNASSESSED
SUSPECT_SOURCE
SENSITIVE_REVIEW_REQUIRED
CONTRADICTION_REQUIRES_REVIEW
ELIGIBLE
```

Todo eso sigue perteneciendo a:

```python
evaluate_episodic_candidate(...)
```

El consumer no reimplementa precedencia de Admission.

```text
Consumption validates bridge semantics.
Admission owns eligibility semantics.
```

---

## 23. Decisión G2-D18 — decisión de Admission preservada exactamente

Cuando outcome de consumo es `EVALUATED`, el resultado porta el mismo objeto lógico producido por Admission.

No se altera:

```text
candidate_id
outcome
reason_code
evaluated_at
policy_version
human_review_required
```

El consumer no convierte `ELIGIBLE` en ninguna capability nueva.

```text
EVALUATED + Admission ELIGIBLE
-> STOP
```

---

## 24. Decisión G2-D19 — pureza y ausencia de side effects

La implementación candidata debe ser determinista y side-effect free respecto de infraestructura.

Prohibido:

- filesystem;
- DB;
- cache persistente;
- network;
- logging obligatorio;
- metrics obligatorias;
- background execution;
- retries;
- event bus;
- PDP/PEP;
- Security reauthorization;
- LLM;
- tool invocation;
- persistence.

Determinismo:

```text
same candidate
+ same projection
+ same evaluated_at
= same consumption result
```

---

## 25. Matriz TDD obligatoria para G3

G3 no puede reducir esta matriz sin autorización nueva.

### 25.1. Contratos y tipos

- **GC2-T01** — output/result es inmutable.
- **GC2-T02** — wrong candidate type -> `TypeError`.
- **GC2-T03** — wrong projection type -> `TypeError`.
- **GC2-T04** — wrong evaluated_at type -> `TypeError`.
- **GC2-T05** — naive evaluated_at -> `ValueError`.
- **GC2-T06** — aware non-UTC evaluated_at -> `ValueError`.
- **GC2-T07** — `EVALUATED` sin decision falla construcción.
- **GC2-T08** — `BLOCKED` con decision falla construcción.
- **GC2-T09** — outcome/reason incompatible falla construcción.
- **GC2-T10** — decision candidate_id distinto del result falla construcción.
- **GC2-T11** — decision evaluated_at distinto del result falla construcción.

### 25.2. Precedencia y blockers

- **GC2-T12** — candidate id mismatch -> `BLOCKED / CANDIDATE_BINDING_MISMATCH` y 0 calls.
- **GC2-T13** — unknown projection policy -> `BLOCKED / UNSUPPORTED_PROJECTION_POLICY` y 0 calls.
- **GC2-T14** — time reversal -> `BLOCKED / CONSUMPTION_TIME_PRECEDES_PROJECTION` y 0 calls.
- **GC2-T15** — projection DENIED -> `BLOCKED / PROJECTION_DENIED` y 0 calls.
- **GC2-T16** — projection HOLD -> `BLOCKED / PROJECTION_HOLD` y 0 calls.
- **GC2-T17** — READY subject_scope mismatch -> `BLOCKED / CONTEXT_BINDING_MISMATCH`.
- **GC2-T18** — READY domain mismatch -> `BLOCKED / CONTEXT_BINDING_MISMATCH`.
- **GC2-T19** — READY purpose mismatch -> `BLOCKED / CONTEXT_BINDING_MISMATCH`.
- **GC2-T20** — múltiples blockers respetan precedencia exacta de §13.

### 25.3. Temporal consumption

- **GC2-T21** — `evaluated_at == projection.evaluated_at` puede evaluar.
- **GC2-T22** — `evaluated_at > projection.evaluated_at` puede evaluar.
- **GC2-T23** — projection antigua no se bloquea solo por edad.
- **GC2-T24** — effective `valid_until` expirado al tiempo fresco produce Admission `TEMPORAL_EXPIRED`.
- **GC2-T25** — effective `valid_from` futuro produce Admission `TEMPORAL_NOT_YET_VALID`.

### 25.4. No trust-sensitive fallback

- **GC2-T26** — source authority original conflictiva no influye frente a effective_context.
- **GC2-T27** — confidence original conflictiva no influye.
- **GC2-T28** — sensitivity original conflictiva no influye.
- **GC2-T29** — original valid_until no influye.
- **GC2-T30** — original valid_from no influye.
- **GC2-T31** — candidate original permanece sin mutación después de EVALUATED.
- **GC2-T32** — effective candidate view no aparece en output público.

### 25.5. Admission-owned semantics

- **GC2-T33** — policy violation produce exactamente Admission `REJECT / POLICY_VIOLATION`.
- **GC2-T34** — out-of-scope produce exactamente Admission `REJECT / OUT_OF_SCOPE`.
- **GC2-T35** — TAINTED produce exactamente Admission `REJECT / TAINTED_SOURCE`.
- **GC2-T36** — REVOKED produce exactamente Admission `REJECT / REVOKED_SOURCE`.
- **GC2-T37** — UNASSESSED produce exactamente Admission HOLD correspondiente.
- **GC2-T38** — SUSPECT produce exactamente Admission HOLD correspondiente.
- **GC2-T39** — sensitive review produce exactamente Admission HOLD correspondiente.
- **GC2-T40** — contradiction review produce exactamente Admission HOLD correspondiente.
- **GC2-T41** — fully admissible effective inputs producen Admission `ELIGIBLE` sin storage side effect.

### 25.6. Exactly-once, preservation y determinismo

- **GC2-T42** — EVALUATED llama evaluator exactamente una vez.
- **GC2-T43** — todos los BLOCKED llaman evaluator cero veces.
- **GC2-T44** — admission decision queda preservada exactamente en result.
- **GC2-T45** — same inputs + same evaluated_at -> same result.
- **GC2-T46** — no projection recomputation ni upstream bundle handling.
- **GC2-T47** — no PDP/PEP ni producer reauthorization.
- **GC2-T48** — no filesystem/network/DB/persistence side effects.
- **GC2-T49** — `ELIGIBLE` termina en STOP y no crea persistence authorization.

Total mínimo congelado:

```text
49 escenarios TDD
```

G3 puede añadir tests constructores o regression tests locales, pero no eliminar los anteriores sin Owner decision.

---

## 26. Estrategia TDD exacta

Primera fase G3 futura:

```text
RED commit
= tests/test_governed_projection_consumption.py only
```

El RED debe demostrar fallo por ausencia del módulo/API productiva, no por tests corruptos.

Luego:

```text
GREEN commit
= add src/malak/memory/governed_projection_consumption.py
```

La implementación GREEN debe ser mínima para satisfacer el contrato congelado.

No se permite introducir funcionalidad no requerida para “preparar el futuro”.

---

## 27. FULL 4R obligatorio

### Risk

Debe demostrar:

- original trust-sensitive `candidate.control` no puede llegar a Admission;
- `HOLD/DENIED` no se convierten en Admission outcomes;
- unknown projection version falla cerrado;
- mismatched candidate/context falla cerrado;
- time reversal falla cerrado;
- Admission policy no se duplica;
- `ELIGIBLE` no produce persistence;
- no authority expansion.

Residual explícito:

```text
candidate_id + neutral context binding
!= cryptographic candidate content integrity
```

### Readability

Debe demostrar:

- responsabilidad única de bridge/adapter;
- enums y reason codes cerrados;
- flow corto y visible;
- no `Manager`, orchestrator universal o registry general;
- `dataclasses.replace` usado solo para la vista local.

### Reliability

Debe demostrar:

- UTC estricto;
- exact policy-version binding;
- deterministic blocker precedence;
- exact neutral-context equality;
- exactly-one evaluator call;
- immutable original candidate;
- same inputs -> same result.

### Resilience

Debe demostrar:

- cualquier blocker termina antes de Admission;
- no fallback a datos menos gobernados;
- no retries ni side effects;
- no reauthorization retroactiva;
- no silent compatibility.

---

## 28. Bounded Correction

Correction budget de una futura G3:

```text
src/malak/memory/governed_projection_consumption.py
tests/test_governed_projection_consumption.py
```

Máximo recomendado:

```text
2 bounded correction rounds
```

Cada cambio del candidate invalida evidencia candidate-bound previa y exige revalidación completa.

Si un finding exige tocar cualquier archivo fuera del budget:

```text
STOP → ESCALATE
```

---

## 29. Independent Validation obligatoria

Candidate G3 final deberá demostrar:

```text
full pytest suite
compileall src tests
git diff --check
exact candidate identity
exact 2-file budget
Ubuntu PASS
Windows PASS
macOS PASS
FULL 4R PASS
49+ required scenarios represented
```

La validación debe estar ligada al SHA exacto del candidate final.

No basta:

- resultado local aislado;
- resultado de candidate anterior;
- CI parcial;
- “tests passed” sin identidad exacta.

---

## 30. Candidate-Bound Evidence / RDD Stage 1

El paquete de evidencia debe registrar como mínimo:

```text
base SHA
candidate SHA
changed files exactos
RED evidence
GREEN evidence
full test count/result
compileall result
diff-check result
Ubuntu job identity/result
Windows job identity/result
macOS job identity/result
FULL 4R disposition
bounded correction rounds used
independent validation disposition
```

Separaciones:

```text
Evidence != Receipt
Receipt != Validation
Validation != Decision
Decision != Authority
```

RDD Stage 2 continúa no autorizado.

---

## 31. Residuales explícitos

Esta unidad no resuelve:

```text
cryptographic candidate content identity
signed projection content
nonce/replay protection
projection revocation propagation
supersession of projections
persistence authorization
retention policy
stored Memory
retrieval eligibility
Knowledge promotion
Conversation/runtime wiring
```

Especialmente:

```text
structural binding
!= cryptographic integrity
```

Este residual es aceptable solo porque la unidad:

- no persiste;
- no transmite externamente;
- no ejecuta tools;
- no concede autoridad;
- termina después de Admission decision.

Antes de Persistence Authorization, el residual deberá reevaluarse explícitamente y no puede heredarse por silencio.

---

## 32. STOP conditions de G3

Detener inmediatamente si la implementación requiere:

- modificar cualquier archivo existente;
- modificar `episodic_admission.py`;
- modificar `governed_input_projection.py`;
- modificar provenance o producer authorization;
- modificar SecurityContext/PDP/PEP;
- modificar permissions/scopes;
- modificar Kernel;
- reimplementar `REJECT | HOLD | ELIGIBLE`;
- confiar en trust-sensitive `candidate.control` original;
- convertir Projection HOLD/DENIED en Admission outcome;
- inventar TTL de projection;
- llamar Admission más de una vez;
- persistencia;
- retrieval;
- Knowledge;
- Conversation/runtime wiring;
- network;
- LLM;
- agents/tools;
- nuevas dependencies;
- criptografía ficticia;
- universal trust manager;
- Sprint 7.12;
- RDD Stage 2;
- implementación antes de reconciliar nuevamente el Project Vault tras integrar G2.

---

## 33. Cuatro preguntas obligatorias

```text
1. ¿Respeta Blueprint?               PASS
2. ¿Respeta Cognitive Constitution? PASS
3. ¿Respeta Governance?             PASS
4. ¿Kernel permanece simple?        PASS
```

Razones:

- responsabilidad permanece localizada en Memory Layer;
- no crea cognición ni autoridad nueva;
- no modifica Security permissions;
- Human in Control intacto;
- Zero Trust reforzado;
- Kernel delta = 0;
- Admission sigue siendo dueño único de eligibility semantics;
- persistence permanece fuera de scope.

---

## 34. Resultado G2

G2 congela una implementación futura mínima equivalente a:

```text
EpisodicMemoryCandidate
+
GovernedAdmissionInputProjection
+
fresh evaluated_at
        ↓
validate candidate binding
        ↓
validate exact projection policy
        ↓
validate time ordering
        ↓
READY?
 ┌──────┴────────┐
 no              yes
 ↓               ↓
BLOCKED     validate neutral context
                 ↓
          dataclasses.replace(
            candidate,
            control=effective_context
          )
                 ↓
          evaluate_episodic_candidate(
            effective candidate,
            effective_signals,
            evaluated_at
          )
                 ↓
             EVALUATED
                 ↓
       REJECT | HOLD | ELIGIBLE
                 ↓
                STOP
```

Disposición:

```text
G2 RESULT: PASS
candidate specification: FROZEN
risk class: 3 — HIGH
future G3 file budget: 2 NEW files
existing production modifications: 0
required TDD scenarios: 49
Kernel delta: 0
Security authority delta: 0
Persistence delta: 0
implementation authorized: false
Sprint 7.12 authorized: false
RDD Stage 2 authorized: false
```

---

## 35. Próximo gate permitido

Después de revisión humana, integración de este G2 y nueva reconciliación del Vault, el siguiente gate posible será únicamente:

```text
G3 — TDD Implementation Candidate
for
Episodic Admission Governed Projection Consumption Boundary
```

Ese G3 requiere autorización humana separada.

No queda autorizado automáticamente por este documento.

---

## 36. Principio de cierre

```text
Projection proves governed effective inputs.
Consumption proves those inputs reach the existing Admission policy without bypass.
Admission decides REJECT | HOLD | ELIGIBLE.
None of them authorizes persistence.
```

Forma compacta:

```text
READY
!= EVALUATED
!= ELIGIBLE
!= PERSISTENCE AUTHORIZED
!= STORED
!= RETRIEVABLE
!= KNOWLEDGE
!= AUTHORITY
```
