---
title: Malāk E3 — Deterministic Oracle Qualification Evidence V0 — G0/G1 Design
status: design_candidate
authority: non_normative
language: es
as_of_date: 2026-10-01
repository: Aranwill/jarvis
baseline_commit: cc03e3a2db19c38fd0d3643d0fb56ff1cfadb8d8
branch: design/e3-deterministic-oracle-qualification-evidence-v0
trigger_pr: 235
trigger_candidate: 313657dd407da9ef4b404e0f520c98ee9b3fabb1
trigger_finding: F235-B01
risk_class: 3_HIGH
critical_contract: true
g0: PASS
g1: PASS
critical_contract_hardening: design_candidate
four_law_questions: candidate_pass
design_4r: pending_independent_review
rdd_stage_1_design_check: pending_independent_review
red_authorized: false
green_authorized: false
implementation_authorized: false
runtime_execution_authorized: false
routing_consumption_authorized: false
rdd_stage_2_authorized: false
authority_effect: none
---

# Malāk E3 — Deterministic Oracle Qualification Evidence V0

## 1. Propósito

Definir el contrato mínimo de **evidencia de qualification independiente** que
permita demostrar que un deterministic oracle candidato cubre de forma total una
pregunta gobernada exacta antes de que una futura unidad pueda considerarlo
elegible para la ruta `DETERMINISTIC`.

Esta unidad nace exclusivamente del finding bloqueante `F235-B01` detectado en
PR #235.

El problema demostrado es:

```text
oracle declaration
+
qualification declaration
+
matching digests
+
different subject-id strings
!=
independent qualification
!=
FULL coverage evidence
```

La unidad no implementa todavía el consumo del artefacto por el routing. Su
objetivo es definir **qué evidencia debe existir** antes de considerar esa
integración.

## 2. Baseline y aislamiento respecto de PR #235

Baseline de diseño:

```text
repository  Aranwill/jarvis
main        cc03e3a2db19c38fd0d3643d0fb56ff1cfadb8d8
```

Trigger externo a este baseline:

```text
PR #235                       Draft / open
trigger FULL 4R candidate     aa031722c9fe4fe2cc9896795b5ca33a8b3a7c68
corrected candidate           313657dd407da9ef4b404e0f520c98ee9b3fabb1
Fix Validator                 FAIL
F235-B01                      OPEN
F235-B02                      CLOSED
F235-B03                      CLOSED
F235-B04                      CLOSED
```

Esta rama de diseño parte de `main` y no modifica ni reescribe el candidate de
PR #235.

```text
PR #235 candidate change from this unit = NO
```

## 3. G0 — necesidad demostrada

### 3.1 Finding material

`F235-B01` demostró que un caller podía construir un oracle y una qualification
internamente coherentes, declarar `coverage_claim = FULL`, usar dos
`subject_id` distintos y obtener elegibilidad determinista sin que existiera
evidencia externa de qualification.

Esto viola el hardening previo:

```text
oracle self-declaration
!= qualification
!= full coverage
```

### 3.2 Disposición

```text
need                         DEMONSTRATED
disposition                  ADOPT
reuse existing patterns      YES
new architecture             NO
new runtime component        NO
new manager/registry         NO
new model/provider           NO
new authority                NO
RDD Stage 2                  NO
```

La necesidad es de **evidencia de dominio**, no de nueva autoridad ni de un
sistema de registración.

## 4. Reutilización antes de crear componentes

### 4.1 E3 Support Assessor Qualification Pack V0.1

Se reutiliza su patrón:

```text
independently reviewed material
+
exact mechanism identity
+
artifact digests
+
deterministic qualification runner
+
PASS | FAIL | INCONCLUSIVE
+
authority_effect = none
```

No se reutiliza su semántica.

Su claim vigente es:

> un support assessor candidate cumplió el safety floor observado bajo una
> identidad, case-set y harness concretos.

Eso no demuestra:

```text
oracle X
fully covers
evaluation question Y
```

### 4.2 Governed Relation Coverage & Uniqueness V0

Se reutiliza el principio de:

```text
exact set coverage
+
uniqueness
+
no omissions
+
no duplicate winner
```

Pero esa unidad declara explícitamente:

```text
relation coverage
!= semantic entailment
!= evidence support
```

Por tanto no puede actuar como qualification FULL del oracle.

### 4.3 RDD-M1 Stage 1

Se reutiliza como capa horizontal de construcción:

```text
candidate identity
evidence provenance
finding lineage
correction round
validator provenance
PASS | FAIL | INCONCLUSIVE
authority_effect = none
```

El nuevo artefacto será **domain evidence referenciable por RDD**, no un
`MALAK-EVIDENCE-MANIFEST/v1` alternativo.

## 5. Separaciones semánticas obligatorias

```text
Oracle Qualification Evidence
!= RDD Evidence Manifest
!= RDD Stage 2 Receipt
!= Runtime authorization
!= support_sufficient
!= semantic truth
!= Owner approval
!= Ready
!= Merge
```

Se evita deliberadamente el término `receipt` para no colisionar con una futura
semántica de RDD Stage 2, que permanece no autorizada.

## 6. G1 — claim exacto de V0

Un `PASS` de esta unidad puede sostener únicamente:

> Bajo el candidate, oracle identity, relation, evaluation question, input/output
> contracts, catálogo de obligaciones y evidencia de qualification registrados,
> un reviewer/validator independiente encontró cobertura completa y sin
> ambigüedades materiales conocidas para la pregunta gobernada exacta.

No puede sostener:

```text
oracle is universally correct
oracle proves truth
oracle is authorized for runtime
oracle may execute
routing may automatically trust it
PASS == support_sufficient
PASS == authority
PASS == merge
```

## 7. Contrato candidato

Nombre lógico:

```text
GovernedDeterministicOracleQualificationEvidenceV0
```

Schema conceptual:

```text
MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-EVIDENCE/v0
```

Campos mínimos:

```text
schema_version
repository
evaluated_candidate_commit

oracle_id
oracle_version
oracle_content_digest
oracle_producer_subject_id

relation_id
evaluation_question_identity
input_contract_identity
output_contract_identity

obligation_catalog_digest
obligation_count
coverage_entries[]

qualification_method
qualification_material_digest
qualification_runner_version
qualification_runner_digest
qualification_reviewer_id
qualification_validator_id

qualification_result
qualification_reasons[]
authority_effect
```

`authority_effect` sólo admite:

```text
none
```

## 8. Identidad de qualification

La evidencia queda ligada exactamente a:

```text
repository
evaluated_candidate_commit
oracle_id
oracle_version
oracle_content_digest
relation_id
evaluation_question_identity
input_contract_identity
output_contract_identity
obligation_catalog_digest
qualification_method
qualification_runner_version
qualification_runner_digest
qualification_material_digest
```

Cualquier cambio material:

```text
→ prior qualification evidence becomes stale
→ no positive deterministic eligibility may be inferred
→ affected evidence must be requalified/revalidated
```

El cambio de candidate conserva además la regla superior de RDD Stage 1:

```text
candidate changes
→ prior candidate-bound evidence does not certify the new candidate
```

## 9. Full coverage no es un input declarativo

V0 elimina la idea de que un caller pueda probar cobertura mediante:

```text
coverage_claim = FULL
```

Regla candidata:

```text
FULL coverage
= derived property of qualification PASS
```

No existe una ruta:

```text
caller says FULL
→ router trusts FULL
```

Un future consumer sólo podrá considerar cobertura total cuando exista evidencia
de qualification con resultado `PASS` bajo la identidad exacta aplicable.

## 10. Evaluation Question Obligation Catalog

Una pregunta sólo puede calificarse mediante este V0 si puede descomponerse de
forma bounded en un catálogo cerrado de obligaciones verificables.

Cada obligación candidata posee:

```text
obligation_id
obligation_statement
obligation_identity
```

`obligation_identity`:

```text
SHA-256(
  canonical(
    relation_id,
    evaluation_question_identity,
    obligation_id,
    obligation_statement
  )
)
```

Propiedades:

- IDs no vacíos y únicos;
- statement bounded;
- identity recomputable;
- catálogo bounded;
- orden canónico;
- no obligación implícita;
- no wildcard;
- no `other`;
- no catch-all semántico no revisado.

Si la pregunta no puede descomponerse sin ambigüedad material:

```text
qualification = INCONCLUSIVE
```

No se fuerza una ruta determinista.

## 11. Coverage entries

Cada `coverage_entry` liga exactamente una obligación a un deterministic check
del oracle:

```text
obligation_id
obligation_identity
oracle_check_id
oracle_check_identity
oracle_check_contract_digest
verification_evidence_refs[]
entry_result
entry_reasons[]
```

`entry_result`:

```text
PASS
FAIL
INCONCLUSIVE
```

Reglas:

```text
every obligation exactly once
unknown obligation       → INCONCLUSIVE
missing obligation       → INCONCLUSIVE
duplicate obligation     → INCONCLUSIVE
duplicate arbitrary win  → forbidden
unbound check            → INCONCLUSIVE
check identity drift     → INCONCLUSIVE
```

Una suite de tests puede aportar evidencia, pero:

```text
tests green
!= semantic full coverage proof
```

La cobertura exige que el reviewer independiente justifique el mapping entre la
obligación exacta y el check determinista exacto.

## 12. Qualification method V0

V0 congela una única dirección:

```text
INDEPENDENT_REVIEWED_DETERMINISTIC_COVERAGE
```

Flujo:

```text
exact evaluation question
        ↓
reviewed bounded obligation catalog
        ↓
exact deterministic oracle checks
        ↓
coverage mapping
        ↓
supporting verification evidence
        ↓
independent reviewer
        ↓
deterministic structural validator
        ↓
PASS | FAIL | INCONCLUSIVE
```

No se introduce LLM-as-a-judge, segundo modelo, voting, score o confidence.

## 13. Independencia y provenance

Roles mínimos:

```text
oracle producer
qualification material author
qualification reviewer
qualification validator
Owner / Authority
```

Regla fundamental:

```text
Writer != Reviewer != Validator != Authority
```

Restricciones V0:

- `oracle_producer_subject_id != qualification_reviewer_id`;
- `oracle_producer_subject_id != qualification_validator_id`;
- reviewer y validator deben tener provenance externa verificable por el proceso;
- dos strings diferentes dentro del artifact **no prueban independencia**;
- la independencia real debe quedar respaldada por evidencia externa y
  candidate-bound, compatible con RDD Stage 1.

Si sólo existen IDs declarados sin evidencia externa suficiente:

```text
qualification_result = INCONCLUSIVE
```

V0 no inventa firma, PKI ni authenticated identity.

## 14. Qualification result

Enum terminal:

```text
PASS
FAIL
INCONCLUSIVE
```

### PASS

Sólo cuando:

1. schema y bounds son válidos;
2. candidate/oracle/relation/question/contracts están ligados exactamente;
3. obligation catalog es válido, cerrado y revisado;
4. cada obligación aparece exactamente una vez;
5. cada obligation mapping posee deterministic check exacto;
6. toda evidencia requerida está presente;
7. ningún `entry_result` es FAIL o INCONCLUSIVE;
8. no existe ambigüedad material conocida;
9. provenance de reviewer/validator es suficiente para demostrar separación según
   el proceso de construcción;
10. `authority_effect = none`.

### FAIL

Cuando la evidencia válida demuestra materialmente que el oracle no cubre al
menos una obligación o contradice su contrato.

### INCONCLUSIVE

Cuando no puede demostrarse PASS ni FAIL por:

- identity/binding inválido;
- obligation catalog incompleto o ambiguo;
- provenance insuficiente;
- evidence refs faltantes;
- check no materializable;
- evaluator/validator unavailable;
- scope expansion necesaria;
- recurso fuera de bounds;
- evidencia no reproducible.

```text
INCONCLUSIVE != PASS
```

## 15. Agregación

Sin score y sin mayoría:

```text
any entry FAIL
→ qualification FAIL

no FAIL + any entry INCONCLUSIVE
→ qualification INCONCLUSIVE

all entries PASS
+ all global preconditions PASS
→ qualification PASS
```

No existe:

```text
confidence threshold
weighted vote
best effort
majority coverage
partial promoted to FULL
```

## 16. Fail-closed / no-fallback matrix

| Condición | Resultado |
|---|---|
| schema desconocido | INCONCLUSIVE |
| candidate mismatch | INCONCLUSIVE |
| oracle digest mismatch | INCONCLUSIVE |
| relation mismatch | INCONCLUSIVE |
| evaluation question mismatch | INCONCLUSIVE |
| input/output contract mismatch | INCONCLUSIVE |
| obligation catalog digest mismatch | INCONCLUSIVE |
| obligación faltante | INCONCLUSIVE |
| obligación duplicada | INCONCLUSIVE |
| check identity inválida | INCONCLUSIVE |
| verification evidence ausente | INCONCLUSIVE |
| reviewer/validator provenance insuficiente | INCONCLUSIVE |
| entry materialmente no cubierta | FAIL |
| qualification PASS exacta | PASS |

Ningún error estructural puede producir PASS.

## 17. Bounds V0 candidatos

Los bounds se congelan como safety ceiling de diseño, no como objetivo de uso:

```text
max obligations/question          32
max obligation statement          4 KiB UTF-8
max verification refs/obligation  16
max qualification artifact        512 KiB
network calls                     0
model calls                       0
tool calls                        0
repo writes during validation     0
runtime side effects              0
```

Si 32 obligaciones no alcanzan para expresar una pregunta sin degradarla:

```text
STOP
→ scope/question decomposition review
→ no automatic bound increase
```

## 18. Blindness y self-certification

La qualification no puede usar como prueba:

- `coverage_claim = FULL` del oracle;
- un label `PASS` emitido por el oracle;
- un score/confidence del mismo mecanismo;
- el mismo producer con un alias diferente;
- un segundo prompt del mismo modelo como independencia;
- expected labels ocultos entregados al oracle como input;
- tests escritos únicamente para reflejar la implementación sin revisar el
  contrato de pregunta.

Si se utilizan fixtures/cases como verification evidence, el oracle candidate no
debe recibir expected disposition ni hidden reviewer annotations antes de producir
su output.

## 19. Relación con RDD Stage 1

Esta unidad produce **evidencia de dominio**.

RDD Stage 1 conserva la responsabilidad horizontal de demostrar:

```text
baseline exact
candidate exact
scope/spec exact
validation exact
finding lineage
correction round
producer provenance
validator provenance
4R evidence
terminal aggregation
authority_effect = none
```

La relación es:

```text
Deterministic Oracle Qualification Evidence
        ↓
evidence_reference
        ↓
MALAK-EVIDENCE-MANIFEST/v1
        ↓
RDD Stage 1 Candidate Conformance
```

No se embebe un segundo RDD dentro de E3.

## 20. Relación con PR #235

Esta unidad **no cierra F235-B01 por existencia documental**.

```text
design exists
!= qualification artifact exists
!= routing consumer validated
!= F235-B01 CLOSED
```

Para cerrar B01 en un candidate futuro deberán demostrarse, como mínimo:

1. qualification evidence real bajo este contrato o su versión aprobada;
2. validación independiente;
3. un consumo gobernado que no permita reemplazarla por self-declaration;
4. candidate-bound validation;
5. Fix Validator sobre el finding original.

El mecanismo exacto de consumo por routing queda fuera de esta G0/G1.

## 21. Security Horizon Check

### Prompt / Context Trust

No hay contenido externo ni prompt ejecutable. Si verification evidence contiene
texto, se trata como datos.

### Identity

V0 conserva provenance declarativa + evidencia externa. No inventa identidad
criptográfica.

### Resource Governance

Hard bounds, offline, sin red/model/tools.

### AI Supply Chain

No se selecciona modelo/provider ni artefacto AI ejecutable.

### Human in Control

PASS de qualification no concede ejecución ni integración.

### Resultado candidato

```text
blocking security gap for design    none
new sensitive surface               no
new authority surface               no
```

## 22. Cuatro preguntas de ley — evaluación candidata del Writer

### Blueprint

La unidad se limita a evidence tooling/documentación y no modifica
Kernel/Planner/Registry.

```text
CANDIDATE PASS
```

### Constitución Cognitiva

Refuerza:

- CC-003 Evidence over speculation;
- CC-005 Proportionality;
- CC-006 Cognitive minimization;
- CC-007 Traceability;
- CC-011 Generation != Finalization;
- CC-012 Evidence-bound finalization.

```text
CANDIDATE PASS
```

### Gobernanza

Preserva Human in Control, least privilege, separación de responsabilidades y
no self-escalation.

```text
CANDIDATE PASS
```

### Kernel complexity

```text
Kernel delta = 0
CANDIDATE PASS
```

Estas disposiciones del Writer no sustituyen revisión independiente.

## 23. Design 4R — candidato para revisión independiente

### Risk

Riesgo principal:

```text
false FULL qualification
→ false DETERMINISTIC eligibility
```

Mitigaciones:

- FULL derivado, nunca declarado;
- exact identity binding;
- obligation completeness/uniqueness;
- independent reviewer/validator provenance;
- PASS/FAIL/INCONCLUSIVE;
- no authority effect.

Writer disposition:

```text
CANDIDATE PASS
```

### Readability

Responsabilidad única: demostrar cobertura total del deterministic oracle sobre
una pregunta exacta.

No manager/registry/service.

Writer disposition:

```text
CANDIDATE PASS
```

### Reliability

Exact identities, exact aggregation y invalidation explícita.

Writer disposition:

```text
CANDIDATE PASS
```

### Resilience

Input inválido, material faltante, ambiguity o provenance insuficiente producen
INCONCLUSIVE, nunca PASS.

Writer disposition:

```text
CANDIDATE PASS
```

Resultado terminal del Design 4R:

```text
PENDING INDEPENDENT REVIEW
```

## 24. RDD Stage 1 Design Check — candidato

Debe revisar independientemente:

```text
candidate identity strategy
baseline/candidate binding
domain evidence provenance
Writer / Reviewer / Validator / Authority separation
PASS | FAIL | INCONCLUSIVE only
candidate change invalidates affected evidence
bounded correction semantics
authority_effect = none
Stage 2 fields/effects absent
```

Writer precheck:

```text
candidate identity strategy        candidate PASS
baseline/candidate binding         candidate PASS
evidence provenance                candidate PASS
role separation                    candidate PASS
terminal enum discipline           candidate PASS
invalidation                       candidate PASS
bounded correction compatibility  candidate PASS
authority_effect                   none
RDD Stage 2 effects                none
```

Resultado terminal:

```text
PENDING INDEPENDENT REVIEW
```

No constituye Candidate Conformance.

## 25. Future RED — NO AUTORIZADO

Si una revisión independiente pre-RED convierte los gates pendientes en PASS y el
Owner autoriza RED separadamente, la causal matrix mínima debería demostrar:

```text
R01 self-declared FULL never qualifies
R02 malformed oracle/question/contract identity → INCONCLUSIVE
R03 stale candidate/oracle digest → INCONCLUSIVE
R04 missing obligation → INCONCLUSIVE
R05 duplicate obligation → INCONCLUSIVE
R06 unknown obligation → INCONCLUSIVE
R07 partial coverage → FAIL
R08 unresolved coverage mapping → INCONCLUSIVE
R09 exact complete mapping can qualify PASS
R10 oracle producer == qualification reviewer cannot PASS
R11 insufficient independence evidence cannot PASS
R12 qualification result aggregation is deterministic
R13 authority_effect != none rejected
R14 artifact/resource bounds enforced
R15 no model/provider/network/tool calls
R16 RDD Stage 2 fields absent
R17 qualification PASS does not authorize routing/runtime
R18 PR #235 candidate remains untouched by this unit
```

Compatibility guards no deben presentarse como causal RED.

## 26. Future implementation surface — NO AUTORIZADA

Dirección candidata, no autorización:

```text
evaluations/e3_deterministic_oracle_qualification_v0/**
scripts/evaluate_e3_deterministic_oracle_qualification.py
tests/test_e3_deterministic_oracle_qualification.py
```

No se autoriza modificar:

```text
src/malak/**
Kernel
Planner
CapabilityRegistry
E4
support_sufficient
Protected Finalization
runtime/provider
Memory/Knowledge
security authority
RDD Stage 2
PR #235 candidate
```

El consumo productivo por routing requiere un gate separado o una ampliación
explícitamente aprobada posterior.

## 27. Correction Budget candidato para future implementation

```text
max correction rounds       2
new dependencies            0
runtime components          0
Kernel delta                0
authority effects           0
scope expansion             prohibited
model/provider requirement  STOP
registry/manager need       STOP
runtime consumption need    STOP → separate gate
normative change need       STOP
```

## 28. File Coverage

El inventario recursivo del baseline exacto reportó:

```text
tracked files discovered = 353
tree truncated            = false
```

El ledger de esta unidad se preserva en:

```text
docs/project/sprints/proposals/
MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-EVIDENCE-V0-FILE-COVERAGE.tsv
```

El documento prohibido:

```text
PROJECT - MANIFIESTO MALAK (1).docx
```

no aparece entre los blobs trackeados del baseline y no fue leído.

## 29. Estado de gate

```text
Owner design authorization              YES
G0 admission                             PASS
G1 design                                PASS
Critical Contract Hardening              DESIGN CANDIDATE
Four Questions                           WRITER CANDIDATE PASS
Design 4R                                PENDING INDEPENDENT REVIEW
RDD Stage 1 Design Check                 PENDING INDEPENDENT REVIEW

RED                                      NOT AUTHORIZED
GREEN                                    NOT AUTHORIZED
implementation                           NOT AUTHORIZED
runtime execution                        NOT AUTHORIZED
routing consumption                      NOT AUTHORIZED
RDD Stage 2                              NOT AUTHORIZED
Ready / Merge                            OWNER ONLY
authority_effect                         none
```

## 30. Siguiente transición lícita

```text
independent pre-RED review
        ↓
Critical Contract Hardening disposition
        ↓
Design 4R
        ↓
RDD Stage 1 Design Check
        ↓
if all PASS:
Owner may separately authorize RED
```

No debe modificarse el candidate de PR #235 durante esta revisión.
