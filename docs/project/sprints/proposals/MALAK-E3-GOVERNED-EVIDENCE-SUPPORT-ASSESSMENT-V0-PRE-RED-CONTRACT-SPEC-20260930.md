---
title: Malāk E3 Governed Evidence Support Assessment V0 — Pre-RED Contract Specification
status: pre_red_candidate
authority: design_evidence_only
language: es
as_of_date: 2026-09-30
source_baseline: 65a5d9cc43869ea361b39651579f503b7d3c12d4
design_candidate: 27e401e923b5b22bdd0b6195ecc489d5802c7fab
risk_class: 3_HIGH
critical_contract: true
implementation_authorized: false
red_authorized: false
green_authorized: false
runtime_execution_authorized: false
rdd_stage_2_authorized: false
authority_effect: none
trigger_finding: E008-SG-02
---

# Malāk E3 Governed Evidence Support Assessment V0 — Pre-RED Contract Specification

## 1. Propósito y scope

Congelar el contrato mínimo verificable previo a cualquier RED para evaluar si la evidencia explícitamente ligada a un finding E3 aporta soporte material al `finding.statement` exacto.

Deriva del G0/G1 candidate `27e401e923b5b22bdd0b6195ecc489d5802c7fab`. No autoriza tests, implementación, runtime ni wiring downstream.

V0 se limita al path E3 focalizado que ya posee `baseline_commit`, `focus_id`, `evidence_set_digest`, `governed relation_id`, structured evidence roles y packet R/K exacto.

Fuera de scope: generic E3, E4, `support_sufficient`, Protected Finalization, Kernel/Planner/Registry, nuevos services/managers/layers, selección de model/provider, NLI/embeddings/RAG/GraphRAG, agents, Memory/persistence, Cognitive Receipt y RDD Stage 2.

## 2. Separación de responsabilidades

```text
finding producer
-> finding + explicit evidence roles

support assessor
-> bounded claim/evidence assessment
-> assessment record

signal producer / adapter
-> OUT OF V0

Assurance Signal Boundary
-> unchanged

Protected Finalization
-> unchanged

human authority
-> unchanged
```

El assessor no modifica el finding, no produce autoridad y no escribe `support_sufficient`.

## 3. Assessment subject identity

Cada assessment queda ligado exactamente a:

```text
baseline_commit
focus_id
evidence_set_digest
relation_id
classification
statement
rationale
supporting_repository_refs
supporting_knowledge_refs
limiting_or_counterevidence_refs
uncertainty_basis
resolved material for every bound ref
```

V0 no crea un content-identity subsystem. Cualquier cambio en esos campos o en el material resuelto invalida el assessment y exige reevaluación.

Un assessment sin baseline/focus/evidence-set binding exacto no puede producir `SUPPORTED`.

## 4. Outcome contract

Enum cerrado:

```text
SUPPORTED
INSUFFICIENT
INCONCLUSIVE
```

`SUPPORTED`: el statement material completo está directamente respaldado por las supporting refs explícitas dentro de la relación gobernada y no existe counterevidence material no reconciliada.

`INSUFFICIENT`: las supporting refs explícitas son irrelevantes, ausentes o materialmente insuficientes. No significa que el claim sea falso.

`INCONCLUSIVE`: no puede justificarse de forma bounded SUPPORTED ni INSUFFICIENT; incluye claim compuesto no completamente soportado, counterevidence material no reconciliable, material incompleto, binding inválido, assessor unavailable, malformed output o necesidad de ampliar scope.

No existe `PARTIALLY_SUPPORTED` en V0.

```text
SUPPORTED != TRUE
SUPPORTED != VERIFIED_FACT
SUPPORTED != support_sufficient=True
INSUFFICIENT != FALSE
INCONCLUSIVE != PASS
```

## 5. Contract record candidato

```text
GovernedEvidenceSupportAssessmentV0
├── policy_version
├── baseline_commit
├── focus_id
├── evidence_set_digest
├── relation_id
├── finding_fingerprint
├── outcome
├── reason_codes[]
├── assessed_supporting_repository_refs[]
├── assessed_supporting_knowledge_refs[]
├── assessed_limiting_or_counterevidence_refs[]
└── authority_effect
```

`policy_version = e3-governed-evidence-support/v0`. Unknown version falla cerrado.

`finding_fingerprint` es un digest determinista local de la representación canónica de relation_id, classification, statement, rationale, los tres grupos de refs y uncertainty_basis.

Algoritmo candidato para un eventual RED/GREEN: UTF-8 canonical JSON, object keys ordenadas, arrays de refs en orden canónico del packet, SHA-256 lowercase hex.

Su objetivo es detectar drift del finding; no equivale a global candidate content identity, source authenticity ni authority.

`authority_effect` tiene un único valor válido: `none`.

## 6. Reason codes V0

Enum cerrado:

```text
MATERIAL_SUPPORT_CONFIRMED
SUPPORTING_REFS_IRRELEVANT
SUPPORTING_REFS_INSUFFICIENT
COMPOUND_CLAIM_NOT_FULLY_SUPPORTED
MATERIAL_COUNTEREVIDENCE_UNRESOLVED
SUBJECT_BINDING_MISMATCH
EVIDENCE_MATERIAL_INCOMPLETE
ASSESSOR_UNAVAILABLE
ASSESSOR_OUTPUT_INVALID
ASSESSMENT_SCOPE_EXCEEDED
```

Reglas:

```text
SUPPORTED
-> exactly MATERIAL_SUPPORT_CONFIRMED

INSUFFICIENT
-> SUPPORTING_REFS_IRRELEVANT and/or SUPPORTING_REFS_INSUFFICIENT

INCONCLUSIVE
-> one or more applicable non-positive uncertainty/failure reason codes
-> never MATERIAL_SUPPORT_CONFIRMED
```

El orden de reason codes no altera outcome; una futura representación debe canonicalizarlo.

## 7. Precedencia determinista

Antes de evaluación semántica:

```text
P01 invalid top-level/input bounds
P02 policy version mismatch
P03 baseline/focus/evidence_set mismatch
P04 finding fingerprint mismatch
P05 exact evidence material missing
P06 evidence-role structural invariant violation
P07 assessor unavailable
P08 assessor output malformed/out of enum
P09 bounded semantic disposition
```

P01-P06 no pueden invocar ni confiar en un evaluator semántico. P02-P08 nunca pueden terminar en SUPPORTED.

La futura implementación debe distinguir invalid API/programmer input de un assessment epistemológicamente INCONCLUSIVE; no convertirá excepciones de tipo en resultados cognitivos silenciosos.

## 8. Counterevidence

Todas las `limiting_or_counterevidence_refs` son material obligatorio.

```text
no material counterevidence
-> SUPPORTED remains possible

limitation compatible with exact bounded claim
-> SUPPORTED remains possible

material conflict unresolved in bounded packet
-> INCONCLUSIVE + MATERIAL_COUNTEREVIDENCE_UNRESOLVED

supporting refs insufficient independently
-> INSUFFICIENT
```

Prohibido: first/last-ref wins, majority wins, ref-count wins, model-confidence wins o asumir que mayor autoridad documental implica automáticamente mayor soporte semántico.

## 9. Assessor independence y provenance

```text
finding producer role != support assessor role
```

No demuestra independencia: same model + second prompt, same producer + renamed function, o output que se autodeclara VERIFIED/SUPPORTED.

Una implementación futura debe exponer provenance suficiente para identificar el mecanismo assessor. Si no demuestra la separación requerida: `INCONCLUSIVE`.

Esta spec no exige segundo modelo. Un mecanismo determinista para relaciones cerradas o un evaluator model-assisted bounded requieren sus garantías aplicables; ninguno obtiene autoridad.

## 10. Seguridad si el assessor fuese model-based

Claim, rationale y evidence material son untrusted data. Instrucciones embebidas nunca se ejecutan. No tools, network, writes, Memory/persistence ni authority decisions. Structured output estricto + parser local fail-closed + hard input/output bounds. El output del evaluator no se convierte en evidencia primaria.

Seleccionar model/provider con delta material exige gate separado.

## 11. Resource bounds

Se reutilizan como techo los límites E3 actuales:

```text
max findings                 16
max statement bytes          4 KiB
max rationale bytes          8 KiB
max evidence refs per role   <= existing E3 per-finding bound
assessment unit              one finding
```

No se congela token budget universal. Si se elige evaluator model-based, prompt/output byte budgets deberán medirse y congelarse antes de GREEN.

Exceder bounds falla cerrado; no hay truncado silencioso ni SUPPORTED por fallback.

## 12. Corpus adversarial V0

Mínimo:

```text
C01 exact support
C02 real ref but irrelevant material
C03 insufficient support
C04 compound claim, only one clause supported
C05 compatible limiting evidence
C06 unresolved material counterevidence
C07 normative authority but semantically irrelevant
C08 low-authority context semantically relevant
C09 rationale overclaims refs
C10 missing resolved evidence material
C11 changed statement with stale fingerprint
C12 changed evidence material with same logical ref label
C13 permuted equivalent ref input
C14 assessor unavailable
C15 malformed assessor output
C16 high-confidence evaluator output with insufficient evidence
C17 self-certifying producer/assessor provenance
C18 scope expansion required to decide
```

El ground truth del corpus no puede provenir únicamente del mismo mecanismo evaluado.

## 13. Métricas y safety floor

```text
false_support_acceptance_rate
unsupported_claim_escape_rate
false_inconclusive_rate
contradiction_handling_recall
assessment_stability_on_equivalent_inputs
binding_drift_detection_rate
```

Safety floor pre-GREEN sobre corpus crítico:

```text
false support acceptance                         = 0
binding drift escapes                            = 0
unresolved counterevidence promoted to SUPPORTED = 0
self-certification promoted to SUPPORTED         = 0
```

`false_inconclusive_rate` debe medirse antes de congelar threshold. Optimizar cobertura no puede relajar el safety floor. No existe truth score ni composite confidence score.

## 14. RED causal matrix

RED futuro requiere autorización humana separada:

```text
R01 canonical finding fingerprint stable for identical material
R02 statement/rationale/relation/role-ref drift changes fingerprint
R03 baseline/focus/evidence_set mismatch cannot yield SUPPORTED
R04 missing resolved ref material cannot yield SUPPORTED
R05 exact materially supporting packet can yield SUPPORTED
R06 real but irrelevant supporting refs yield INSUFFICIENT
R07 materially insufficient supporting refs yield INSUFFICIENT
R08 compound partially-supported claim yields INCONCLUSIVE
R09 unresolved material counterevidence yields INCONCLUSIVE
R10 compatible limiting evidence does not force INCONCLUSIVE
R11 reason-code/outcome incoherence fails closed
R12 unknown policy version fails closed
R13 assessor unavailable yields INCONCLUSIVE
R14 malformed assessor output cannot yield SUPPORTED
R15 self-certifying producer/assessor provenance cannot yield SUPPORTED
R16 equivalent input permutations preserve disposition
R17 authority_effect other than none fails closed
R18 assessment does not emit or mutate support_sufficient
R19 generic E3 remains unchanged
R20 E4 remains unchanged
R21 Kernel/Planner/Registry remain untouched
```

Compatibility guards ya verdes no deben etiquetarse falsamente como causal RED.

## 15. Candidate implementation surface — no autorizado

Primera superficie productiva a evaluar si RED fuese autorizado:

```text
src/malak/capabilities/_engineering_analysis.py
src/malak/capabilities/engineering_analyze.py
```

Un archivo interno E3 nuevo sólo podrá admitirse si RED demuestra una responsabilidad cohesiva que no cabe ahí sin degradar legibilidad.

Tests candidatos:

```text
tests/test_e3_governed_evidence_support_assessment_v0.py
tests/test_engineering_analyze.py
tests/test_internal_interaction_test_v0_harness.py
```

Los dos últimos sólo por compatibilidad demostrada.

Prohibido por inferencia lateral:

```text
src/malak/core/assurance_signal_projection.py
src/malak/core/protected_finalization.py
src/malak/capabilities/engineering_propose.py
Kernel
Planner
Registry
governance
Blueprint
```

## 16. Correction budget

```text
max correction rounds: 2
scope expansion: prohibited
new dependency: STOP
new model/provider requirement: STOP
new runtime service/manager: STOP
support_sufficient wiring need: STOP
normative change need: STOP
```

## 17. Validation evidence antes de GREEN

Un eventual candidate debe demostrar:

```text
exact baseline/candidate identity
candidate diff
focused causal tests
full pytest Ubuntu
full pytest Windows
compileall
no forbidden-file delta
no authority expansion
no support_sufficient wiring
no semantic_assurance overclaim
```

Si usa evaluator probabilístico/model-based, además: versioned evaluation corpus, assessor provenance, métricas medidas, stability report y false-support safety floor PASS.

Tests verdes sin estas evidencias no cierran el gate.

## 18. Design 4R — Pre-RED

Risk PASS: positive support queda negado ante binding drift, counterevidence irresuelta, self-certification o evaluator failure.

Readability PASS: outcome, reason, subject identity, provenance y downstream authority permanecen separados.

Reliability PASS: enums, invalidación, precedencia, corpus y safety floor quedan congelados; inputs equivalentes deben conservar disposición.

Resilience PASS: failure paths son fail-closed y nunca producen SUPPORTED por ausencia de capability.

```text
Design 4R Pre-RED = PASS
```

## 19. RDD Stage 1 Design Check — Pre-RED

```text
candidate identity strategy        PASS
baseline exact                     PASS
evidence/material binding          PASS
scope/spec binding                 PASS
Writer/Reviewer/Validator split    PASS at contract level
PASS/FAIL/INCONCLUSIVE discipline  PASS
candidate change invalidation      PASS
bounded correction                 PASS
independent validation requirement PASS
authority_effect                   none
RDD Stage 2 effects                NONE
overall                            PASS
```

No constituye Candidate Conformance.

## 20. Security Horizon — Pre-RED

```text
Prompt/Context Trust Boundary      PASS contractually / runtime not selected
Identity/Delegation                PASS role separation / implementation pending
Compromise containment             N/A no side effects
Memory/Knowledge poisoning         PASS contractually: source role != trust
AI supply-chain                    DEFERRED until model/provider selection
Data disclosure                    DEFERRED until execution mechanism selection
Resource Governance                PASS bounded subject / model budget pending if needed
Observability/evidence             PASS contractually / implementation pending
Human in Control                   PASS
```

No BLOCKING_GAP para diseñar RED. Elegir un mecanismo model-based podría abrir gates adicionales antes de GREEN.

## 21. Cuatro preguntas de ley

```text
Blueprint                         PASS
Cognitive Constitution            PASS
Governance Constitution           PASS
Kernel complexity                 PASS — delta 0
```

## 22. Pre-RED gate result

```text
G0/G1 admission                   PASS
Pre-RED Contract Specification    PASS
Critical Contract Hardening       PASS
Design 4R                         PASS
RDD Stage 1 Design Check          PASS
Security Horizon                  PASS

RED authorized                    false
implementation authorized         false
runtime execution authorized      false
authority_effect                  none
```

Siguiente decisión humana posible: autorizar bounded RED sobre R01-R21 y la superficie explícita de esta spec.

Hasta autorización separada:

```text
NO TEST CHANGES
NO PRODUCTION CHANGES
NO RUNTIME EXECUTION
NO DRAFT PR PROMOTION IMPLIED BY THIS PASS
```
