---
title: Malāk U007-F04/F06 — E3 Epistemic Calibration — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation_design
language: es
created: 2026-09-27
baseline_commit: 0b0b1914c6414c003ff6e34f53b8881b8874b0e9
source_run_id: bootstrap-u01-20260926-007
findings:
  - U007-F04
  - U007-F06
risk_class: 3
critical_contract: true
implementation_authorized: false
red_authorized: false
green_authorized: false
runtime_execution_authorized: false
eighth_u01_authorized: false
self_modification_authorized: false
authority_effect: none
related:
  - docs/project/status/MALAK-SEVENTH-U01-UNRESOLVED-CLASSIFICATION-AUDIT-20260927.md
  - docs/project/sprints/proposals/MALAK-U007-F05-KERNEL-INSTANCE-ARCHITECTURE-CLARIFICATION-G0-G1-DESIGN.md
  - docs/architecture/kernel.md
  - docs/project/sprints/proposals/MALAK-E3-ENGINEERING-ANALYZE-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-E4-ENGINEERING-PROPOSE-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-ANALYZE-STRUCTURED-OUTPUT-CONTRACT-V0-G0-G1-DESIGN.md
  - src/malak/capabilities/_engineering_analysis.py
  - src/malak/capabilities/engineering_analyze.py
  - src/malak/capabilities/engineering_propose.py
---

# Malāk U007-F04/F06 — E3 Epistemic Calibration — G0/G1 Design

## 1. Propósito

Diseñar una calibración epistemológica mínima para los findings del Seventh U01:

~~~text
U007-F04
-> D — over-conservative / out-of-scope inference

U007-F06
-> C — historical limitation already accepted
   + over-conservative rationale
~~~

sin cambiar todavía código ni ejecutar otro U01.

Este gate responde:

~~~text
¿Cuándo puede Engineering Analyze usar UNRESOLVED
para bloquear una conclusión sobre el snapshot actual?
~~~

No responde:

~~~text
¿cómo corregir Evidence Focus?
¿cómo reclasificar Knowledge sources?
¿cómo forzar ALIGNED?
¿cómo hacer que el modelo sea determinista?
~~~

## 2. Baseline

~~~text
repository:
Aranwill/jarvis

branch:
main

baseline:
0b0b1914c6414c003ff6e34f53b8881b8874b0e9
~~~

Estado relevante:

~~~text
PR #203
-> Seventh U01 unresolved classification integrated

PR #204
-> U007-F05 architecture clarification design integrated

PR #205
-> Kernel Specification promotion integrated

Kernel Specification
-> KIC-01..KIC-07 active
~~~

## 3. Evidencia causal

### U007-F04

Seventh U01 produjo una inferencia equivalente a:

~~~text
current capability composition
cannot be declared fully resolved
because future architectural drift may occur
~~~

El problema:

~~~text
future possibility
!= uncertainty about current captured snapshot
~~~

La revisión U007 clasificó ese finding como:

~~~text
D — over-conservative / out-of-scope inference
~~~

### U007-F06

Seventh U01 produjo una inferencia equivalente a:

~~~text
CURRENT_STATE_REVALIDATED
is not enough to classify current Kernel as aligned
without a normative Accepted authority closing historical divergence
~~~

El problema:

~~~text
historical process incompleteness
!= current implementation uncertainty
~~~

cuando el claim actual puede evaluarse independientemente con:

~~~text
current implementation evidence
+
current applicable governing/specification evidence
~~~

La revisión U007 clasificó ese finding como:

~~~text
C — historical limitation already accepted
~~~

## 4. Contrato actual de E3

El prompt actual exige:

~~~text
Compare observed implementation evidence
against applicable governed knowledge.

Use only supplied evidence for claims
about captured repository snapshot.

Expose uncertainty and unresolved precedence
instead of inventing a conclusion.

If required precedence is not explicitly established
-> UNRESOLVED
~~~

Clases actuales:

~~~text
ALIGNED
PARTIAL
GAP
CONTRADICTION
UNRESOLVED
~~~

Parser actual:

~~~text
strict JSON
exact keys
classification allow-list
real evidence refs
R+K required for relational classes
UNRESOLVED requires real grounded refs
~~~

E4:

~~~text
UNRESOLVED
-> NO proposal call
-> owner resolution / INCONCLUSIVE path
~~~

Por tanto una clasificación demasiado conservadora puede bloquear Propose aunque
el sistema técnico funcione correctamente.

## 5. Root cause

No se observa un fallo de:

~~~text
JSON schema
parser
reference validation
evidence identity
runtime
provider
structured output
~~~

El root cause candidato es:

~~~text
the epistemic instructions do not explicitly separate:

current-state uncertainty
historical-process limitation
prospective risk
~~~

La instrucción actual:

~~~text
Expose uncertainty...
~~~

es correcta pero demasiado amplia para impedir que el modelo convierta riesgo
futuro o incompletitud histórica en un blocker del snapshot actual.

## 6. Decisión G1

La calibración V0 será prompt-contract only.

Future GREEN scope candidato:

~~~text
src/malak/capabilities/_engineering_analysis.py
tests/test_engineering_analyze.py
tests/test_engineering_propose.py
~~~

No se cambia:

~~~text
ANALYZE_RESPONSE_JSON_SCHEMA
parse_engineering_analysis(...)
parse_engineering_finding(...)
classification enum
evidence ref contract
E4 eligibility rules
InternalInteraction terminal rules
Evidence Focus
Knowledge Reader
runtime/provider
generation contract
~~~

Razón:

~~~text
smallest causal correction first
~~~

No existe evidencia que justifique introducir nuevos campos estructurados o un
segundo clasificador determinista.

## 7. Contrato epistemológico candidato

El prompt compartido de Analyze deberá establecer explícitamente:

### EC-01 — Current snapshot scope

~~~text
Findings classify relationships about the captured repository snapshot only.
~~~

No debe exigir garantías sobre snapshots futuros.

### EC-02 — Prospective risk

~~~text
A possible future drift, future regression or future architectural violation
is not by itself grounds for a current UNRESOLVED finding.
~~~

Un riesgo futuro material puede aparecer en:

~~~text
uncertainties[]
~~~

pero no debe bloquear una relación actual demostrable.

### EC-03 — Historical process limitation

~~~text
Historical process incompleteness does not by itself make the current
implementation relationship UNRESOLVED.
~~~

Debe preservarse como incertidumbre/contexto cuando sea relevante.

### EC-04 — Independent current-state evaluation

Si evidencia histórica o derivada carece de autoridad normativa:

~~~text
do not promote it to authority
~~~

pero también:

~~~text
do not require that derived/historical record
to possess normative authority
when the current relation can be evaluated
from current implementation + applicable higher-authority evidence
~~~

### EC-05 — UNRESOLVED boundary

UNRESOLVED queda reservado para:

~~~text
material ambiguity in the current captured snapshot
OR
insufficient supplied evidence needed for the current relation
OR
current applicable precedence that cannot be resolved
~~~

No para:

~~~text
future possibility alone
historical receipt incompleteness alone
absence of retrospective proof alone
~~~

### EC-06 — No forced optimism

La calibración no ordena:

~~~text
prefer ALIGNED
minimize findings
avoid UNRESOLVED
~~~

Si el snapshot actual realmente carece de evidencia suficiente:

~~~text
UNRESOLVED remains required
~~~

## 8. Por qué no cambiar schema/parser

Agregar campos como:

~~~text
temporal_scope
uncertainty_kind
historical_status
~~~

aumentaría:

~~~text
public/observable analysis contract
E3 parser surface
E4 analysis dependency
structured-output schema
tests
migration burden
~~~

sin evidencia de que el problema actual requiera esa complejidad.

V0 aplica:

~~~text
prompt semantic hardening
+
RED contract tests
+
runtime follow-up only after merge and separate authorization
~~~

Si V0 vuelve a producir el mismo error bajo evidencia correcta:

~~~text
then a structured epistemic field may be justified
in a separate gate
~~~

## 9. Shared E3/E4 analysis boundary

ANALYZE_SYSTEM_PROMPT es compartido por:

~~~text
EngineeringAnalyzeCapability
EngineeringProposeCapability internal analysis
~~~

Por tanto la calibración debe ser única.

No se permite:

~~~text
E3 prompt A
E4 internal-analysis prompt B
~~~

RED deberá demostrar que ambos paths usan el mismo contrato calibrado.

## 10. Existing parser semantics preserved

Las reglas actuales permanecen:

~~~text
ALIGNED/PARTIAL/GAP/CONTRADICTION
-> at least one R ref + one K ref

UNRESOLVED
-> at least one real supplied ref

unknown ref
-> reject

duplicate ref
-> reject
~~~

La calibración no relaja grounding.

## 11. E4 eligibility preserved

No cambia:

~~~text
UNRESOLVED
-> NO_PROPOSAL

CONTRADICTION
-> NO_PROPOSAL

all ALIGNED
-> NO_PROPOSAL / no change need

GAP or PARTIAL
and no UNRESOLVED/CONTRADICTION
-> proposal inference eligible
~~~

Este gate busca mejorar cuándo el modelo elige UNRESOLVED, no reducir el valor
protector de esa clase.

## 12. RED requirements futuros

RED deberá fallar contra el baseline previo a GREEN demostrando al menos:

~~~text
R01 prompt explicitly scopes findings to current captured snapshot

R02 prompt states prospective risk alone
    is not current UNRESOLVED

R03 prompt states historical process incompleteness alone
    is not current UNRESOLVED

R04 prompt requires independent evaluation of current relation
    from current implementation + applicable governed/spec evidence

R05 prompt preserves genuine current ambiguity as UNRESOLVED

R06 prompt places prospective/historical residuals in uncertainties
    when relevant

R07 E3 uses the calibrated shared ANALYZE_SYSTEM_PROMPT

R08 E4 internal analysis uses the same calibrated prompt

R09 classification enum unchanged

R10 parser semantics unchanged

R11 evidence ref semantics unchanged

R12 E4 eligibility unchanged
~~~

RED no debe depender de una inferencia real de Ollama.

Debe probar el contrato observable/determinista.

## 13. GREEN budget futuro

GREEN podrá modificar solamente:

~~~text
src/malak/capabilities/_engineering_analysis.py
tests/test_engineering_analyze.py
tests/test_engineering_propose.py
~~~

Expected production delta:

~~~text
ANALYZE_SYSTEM_PROMPT wording only
~~~

Forbidden:

~~~text
parser changes
schema changes
new dataclass fields
new classifications
Evidence Focus changes
Knowledge Reader changes
runtime changes
provider changes
retry
repair
new model call
Kernel
Planner
~~~

Correction budget:

~~~text
max bounded correction rounds: 2
~~~

## 14. Material prerequisite discovered during G0

G0 encontró una inconsistencia separada:

~~~text
AGENTS.md hierarchy:
approved specifications, including Kernel Specification
-> authority rank below Blueprint and above Accepted ADRs

but E1 currently classifies:
docs/architecture/kernel.md
-> ARCHITECTURE_REFERENCE / reference
~~~

Además U01 Evidence Focus no exige docs/architecture/kernel.md como selector
required.

Puede llegar sólo por supplemental search:

~~~text
bounded
potentially truncated
not required for focus_complete
~~~

Esto significa:

~~~text
U007-F05 normative resolution exists
!=
future U01 is guaranteed to receive it
with correct documentary role
~~~

### Disposición

Este hallazgo queda fuera del scope F04/F06.

Se registra como:

~~~text
PREREQUISITE-KAF-01
Knowledge Authority / U01 Focus fidelity
~~~

No autoriza cambio aquí.

## 15. Runtime sequencing consequence

La implementación futura de EC-01..EC-06 puede avanzar de forma independiente.

Pero:

~~~text
Eighth U01
NOT ADMISSIBLE
until PREREQUISITE-KAF-01 has an explicit disposition
~~~

Razón:

~~~text
do not evaluate calibration quality
against a known incomplete/misclassified governing evidence path
~~~

## 16. Malāk Alignment Matrix

| Fuente | Autoridad | Invariante | Baseline | Disposición | Efecto |
|---|---|---|---|---|---|
| Cognitive Constitution | normativa | incertidumbre visible; Evidence != Authority | preserved | ADOPT | no optimism bias |
| Governance Constitution | normativa | Human in Control | preserved | ADOPT | no authorization |
| Blueprint | architecture master | Kernel/Capability First | current snapshot | ADOPT | findings bounded to current state |
| Kernel Specification | approved specification | KIC-01..KIC-07 | promoted | OBSERVE in this gate | no E3 evidence fix here |
| E3 design | implementation design | compare implementation vs governed knowledge | integrated | ADAPT | temporal calibration |
| E4 design | implementation design | unresolved blocks proposal | integrated | ADOPT | eligibility unchanged |
| Analyze structured output | critical contract | strict schema/parser | integrated | ADOPT | zero schema/parser delta |
| PR #203 audit | derived | F04=D, F06=C | current evidence | INPUT ONLY | causal trigger |
| E1 Knowledge Reader | implementation | source role classification | KAF-01 found | DEFER TO SEPARATE GATE | runtime prerequisite |
| U01 Evidence Focus | implementation | required vs supplemental evidence | KAF-01 found | DEFER TO SEPARATE GATE | runtime prerequisite |

## 17. Four Questions of Law

### Blueprint

~~~text
PASS
~~~

No cambia arquitectura; limita Analyze al snapshot que ya declara analizar.

### Cognitive Constitution

~~~text
PASS
~~~

Preserva incertidumbre real y evita fabricar incertidumbre material desde
riesgo prospectivo o historia incompleta.

### Governance Constitution

~~~text
PASS
~~~

No cambia autoridad; finding sigue sin ser decisión.

### Kernel complexity

~~~text
PASS
Kernel delta 0
Planner delta 0
~~~

## 18. Critical Contract Hardening

Aplica porque Analyze classification controla downstream Propose eligibility.

Interpretaciones cerradas:

~~~text
current claim != future guarantee

historical process limitation
!= current architecture defect

derived evidence
!= normative authority

lack of authority in derived evidence
!= automatic current UNRESOLVED

uncertainty visibility
!= blocking finding requirement

UNRESOLVED remains valid
for current material ambiguity

calibration
!= optimism bias

prompt hardening
!= parser relaxation
~~~

Known material ambiguity after hardening:

~~~text
0 within F04/F06 scope
~~~

Separate prerequisite:

~~~text
KAF-01
not resolved here
~~~

## 19. Design 4R

### Risk — PASS

Main risk:

~~~text
over-correction toward ALIGNED
~~~

Control:

~~~text
EC-06 preserves genuine UNRESOLVED
no parser relaxation
no E4 eligibility change
~~~

Second risk:

~~~text
prompt-only correction may remain probabilistic
~~~

Control:

~~~text
smallest causal correction first
separate runtime benchmark later
structured-field redesign only if evidence justifies it
~~~

### Readability — PASS

Three uncertainty domains are explicit:

~~~text
current
historical
prospective
~~~

### Reliability — PASS

One shared prompt controls E3 and E4 internal Analyze.

No duplicated policy.

### Resilience — PASS

If ambiguity is material to current snapshot:

~~~text
UNRESOLVED
-> remains blocker
~~~

If model still miscalibrates after hardening:

~~~text
runtime result remains visible
-> no retry
-> no repair
-> no authority
-> separate follow-up gate
~~~

## 20. RDD Stage 1 Design Check

~~~text
baseline identity strategy                PASS
future candidate identity strategy        PASS
evidence provenance                       PASS
Writer / Reviewer / Validator separation  PASS
Authority separation                      PASS
PASS / FAIL / INCONCLUSIVE discipline     PASS
candidate change invalidation             PASS
bounded correction                        PASS
authority_effect                           none
RDD Stage 2                                NOT AUTHORIZED
~~~

Result:

~~~text
PASS
~~~

## 21. Security / authority horizon

No cambia:

~~~text
trust boundary
prompt-as-data protection
tool access
network access
Memory
Knowledge writes
runtime authority
self-modification
~~~

Security Horizon:

~~~text
Prompt & Context Trust        ALREADY_COVERED
Identity & Delegation         NOT_APPLICABLE
Compromise Containment        NOT_APPLICABLE
Memory/Knowledge Poisoning    UNCHANGED
AI Supply Chain               UNCHANGED
Resource Governance           UNCHANGED
Observability                 ALREADY_COVERED
Human in Control              PASS
~~~

## 22. Scope summary

Current design candidate:

~~~text
1 design document only
production delta 0
test delta 0
runtime delta 0
Kernel delta 0
Planner delta 0
Evidence Focus delta 0
Knowledge Reader delta 0
authority_effect none
~~~

Future EC implementation candidate:

~~~text
prompt wording + RED/GREEN tests only
~~~

Separate KAF-01 candidate:

~~~text
NOT DESIGNED HERE
NOT AUTHORIZED HERE
~~~

## 23. Authorization boundary

~~~text
G0/G1 design                 PREPARED
Critical Contract Hardening  PASS
Four Questions               PASS
Design 4R                    PASS
RDD Stage 1 Design Check     PASS

RED                           NOT AUTHORIZED
GREEN                         NOT AUTHORIZED
KAF-01 implementation        NOT AUTHORIZED
runtime execution             NOT AUTHORIZED
Eighth U01                    NOT AUTHORIZED
self-modification             NOT AUTHORIZED
authority_effect              none
~~~

## 24. Next lawful transitions

After candidate-bound validation and Owner merge of this design:

~~~text
A. separate KAF-01 G0/G1
   for Knowledge Authority / U01 Focus fidelity

B. explicit Owner authorization for E3 Calibration RED
   may follow independently

C. Eighth U01 remains blocked
   until both lines reach explicit safe disposition
~~~
