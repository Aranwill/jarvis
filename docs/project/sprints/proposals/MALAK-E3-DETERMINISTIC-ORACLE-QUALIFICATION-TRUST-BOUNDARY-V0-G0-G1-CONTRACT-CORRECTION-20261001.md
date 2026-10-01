---
title: Malāk E3 — Deterministic Oracle Qualification Trust Boundary V0 — G0/G1 Contract Correction
status: design_candidate
authority: non_normative
language: es
as_of_date: 2026-10-01
repository: Aranwill/jarvis
baseline_commit: c86a9bc3e716046bd8c803e5893fc36289c1d485
branch: design/e3-oracle-qualification-trust-boundary-v0
trigger_pr: 237
trigger_candidate: b288c915c080fe26a261f90a442bd6016f3e314d
trigger_review: MALAK-PR237-CANDIDATE-FULL-4R-B288C9-20261001.md
trigger_result: FAIL
risk_class: 3_HIGH
critical_contract: true
contract_correction: true
g0: PASS
g1: PASS
critical_contract_hardening: design_candidate
four_law_questions: candidate_pass
design_4r: pending_independent_review
rdd_stage_1_design_check: pending_independent_review
implementation_authorized: false
red_authorized: false
green_authorized: false
runtime_execution_authorized: false
routing_consumption_authorized: false
rdd_stage_2_authorized: false
authority_effect: none
---

# Malāk E3 — Deterministic Oracle Qualification Trust Boundary V0

## 1. Propósito

Corregir el contrato de E3 Deterministic Oracle Qualification Evidence V0 después
de que Candidate FULL 4R de PR #237 demostrara rutas materiales de false-PASS.

La corrección separa explícitamente:

~~~text
structural/content validation
!=
independent qualification
!=
RDD Candidate Conformance
!=
human authority
~~~

El objetivo no es añadir más hashes ni otra capa de self-certification.

El objetivo es impedir que un evaluator offline afirme que una evidencia es
independiente, completa o gobernada cuando sólo puede observar bytes y campos
suministrados por el caller.

## 2. Baseline y aislamiento

Baseline integrado:

~~~text
repository  Aranwill/jarvis
main        c86a9bc3e716046bd8c803e5893fc36289c1d485
~~~

Trigger externo:

~~~text
PR #237
candidate                  b288c915c080fe26a261f90a442bd6016f3e314d
Candidate FULL 4R          FAIL

F237-F4R-01                BLOCKING
F237-F4R-02                BLOCKING
F237-F4R-03                BLOCKING
F237-F4R-04                BLOCKING
F237-F4R-05                BLOCKING
F237-F4R-06                BLOCKING
F237-F4R-07                BLOCKING
~~~

PR #237 permanece congelada. Esta unidad no modifica su branch, runner ni tests.

## 3. G0 — necesidad demostrada

Las reproducciones independientes de PR #237 demostraron que podía obtenerse
PASS con:

~~~text
fabricated independence digests
incomplete obligation catalog
arbitrary catalog digest
arbitrary qualification material digest
arbitrary runner digest
fake verification refs
caller-controlled expected_binding
~~~

La causa raíz se resume en:

~~~text
internally coherent declarations
!=
externally grounded qualification
~~~

Disposición:

~~~text
need                         DEMONSTRATED
disposition                  ADAPT / CONTRACT CORRECTION
new runtime component        NO
new manager/registry         NO
new store/database           NO
new PKI/signatures           NO
new provider/model           NO
RDD Stage 2                  NO
authority delta              0
~~~

## 4. Evidencia interna reutilizable

### 4.1 RDD-M1 Evidence Manifest

RDD-M1 ya establece:

~~~text
producer / validator strings = provenance
!= proof of real independence
~~~

La independencia real debe demostrarse por evidencia externa y Engineering
Method.

El active manifest puede permanecer fuera del candidate worktree, ligado al SHA
exacto, sin convertirse en authority ni Stage 2 receipt.

Esta unidad reutiliza esa separación.

### 4.2 E2 Structural Evidence Evaluation Pack

El runner existente de E2 conserva explícitamente:

~~~text
identity_independence_verified = False
requires_external_validation   = True
~~~

y declara que la independencia real debe validarse fuera del runner.

Esta unidad adopta el mismo principio, no su implementación ni su semántica de
dominio.

### 4.3 MALAK-EVIDENCE-VALIDATOR/v1

Malāk ya separa:

~~~text
validator_result
!=
manifest_result
~~~

Un validator puede decir que un artefacto es estructuralmente válido sin
convertirse en productor de su claim.

Esta separación se reutiliza para E3 Qualification.

## 5. Corrección fundamental

El diseño anterior permitía interpretar:

~~~text
evaluate_qualification_evidence_v0(...)
→ qualification PASS
~~~

La corrección V0 establece:

~~~text
offline structural validator
→ structural validation result only

independent reviewer / validator process
→ qualification review evidence

structural PASS
+
independent qualification review PASS
+
exact binding
→ qualification may be considered evidenced
~~~

Ninguno de estos resultados concede autoridad.

## 6. Tres dominios separados

### A. Qualification Material

Material de dominio que describe:

- pregunta exacta;
- oracle exacto;
- obligation catalog;
- coverage entries;
- verification evidence;
- qualification material;
- runner identity material.

### B. Structural Validation

Valida de forma determinista:

- schema;
- bounds;
- canonicalization;
- content digests;
- exact bindings;
- set coverage;
- uniqueness;
- stale material;
- resolved evidence references.

No valida identidad humana real.

### C. Independent Qualification Review Evidence

Evidence externa al candidate activo que declara el resultado de una revisión
independiente sobre material exacto y candidate exacto.

La revisión externa conserva:

~~~text
PASS | FAIL | INCONCLUSIVE
authority_effect = none
~~~

## 7. Separaciones obligatorias

~~~text
structural_validator_result
!= qualification_review_result

qualification_review_result
!= RDD manifest result

RDD manifest result
!= RDD Candidate Conformance

RDD Candidate Conformance
!= Owner approval

evidence
!= authority
~~~

También:

~~~text
digest-shaped
!= content-bound

content-bound
!= provenance-authenticated

distinct role strings
!= independent actors

external reference string
!= resolved evidence

exact coverage of supplied catalog
!= proof catalog is semantically complete
~~~

## 8. Revised offline validator contract

Nombre candidato:

~~~text
DeterministicOracleQualificationStructuralValidatorV0
~~~

Output mínimo:

~~~text
validator_schema
validator_result
validator_reasons[]
candidate_commit
qualification_bundle_digest
executing_runner_version
executing_runner_digest
requires_external_validation
identity_independence_verified
authority_effect
~~~

Valores obligatorios:

~~~text
validator_result:
PASS | FAIL | INCONCLUSIVE

requires_external_validation:
true

identity_independence_verified:
false

authority_effect:
none
~~~

El runner offline nunca podrá emitir:

~~~text
identity_independence_verified = true
~~~

en V0.

## 9. Qualification Bundle

Schema conceptual:

~~~text
MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-BUNDLE/v0
~~~

Contenido mínimo:

~~~text
repository
evaluated_candidate_commit

oracle_identity
  oracle_id
  oracle_version
  oracle_content_digest
  oracle_producer_subject_id

governed_question_material
  relation_id
  evaluation_question_identity
  input_contract_identity
  output_contract_identity

obligation_catalog[]
obligation_catalog_digest

coverage_entries[]

verification_evidence[]
verification_evidence_digest

qualification_material
qualification_material_digest
~~~

El bundle no contiene un trusted boolean ni un self-declared FULL.

## 10. Content binding obligatorio

### 10.1 Obligation catalog

El validator debe computar:

~~~text
obligation_catalog_digest
=
SHA-256(canonical(obligation_catalog))
~~~

No acepta un digest sólo por coincidir en dos objetos caller-controlled.

### 10.2 Qualification material

Debe existir material bounded explícito.

~~~text
qualification_material_digest
=
SHA-256(canonical(qualification_material))
~~~

Si el material no está presente o no puede recomputarse:

~~~text
validator_result = INCONCLUSIVE
~~~

### 10.3 Verification evidence

Cada coverage entry referencia una identidad presente en
verification_evidence[].

Cada evidence item mínimo:

~~~text
evidence_id
evidence_kind
content_digest
content_or_bounded_material
candidate_binding
~~~

El validator debe resolver cada ref localmente dentro del bundle.

~~~text
unresolved ref
→ INCONCLUSIVE
~~~

No existe:

~~~text
"evidence:fake"
→ accepted by string presence
~~~

### 10.4 Bundle digest

El validator computa:

~~~text
qualification_bundle_digest
=
SHA-256(canonical(all material fields excluding derived output))
~~~

Ese digest es la identidad material usada por la revisión externa.

## 11. Runner identity

El runner no acepta su identidad como verdad declarada por el caller.

Debe derivar:

~~~text
executing_runner_version
executing_runner_digest
~~~

desde el propio artefacto ejecutado o desde una identidad deterministicamente
recomputable de sus bytes/version.

El expected runner identity, si existe, pertenece al material revisado
externamente.

Mismatch:

~~~text
→ INCONCLUSIVE
~~~

La estrategia exacta de self-digest debe revisarse en pre-RED para evitar
recursión o identidad circular.

## 12. Governed reference no es caller authority

Se elimina la semántica implícita:

~~~text
expected_binding object
= trusted source
~~~

V0 usa:

~~~text
governed_question_material
~~~

como material content-bound.

El structural validator puede demostrar:

~~~text
artifact matches this material
~~~

pero no puede demostrar:

~~~text
this material was legitimately governed
~~~

sin evidencia externa.

Por tanto:

~~~text
structural PASS
!= governed provenance verified
~~~

## 13. Completeness del Obligation Catalog

Este es un límite epistémico explícito.

El structural validator puede demostrar:

~~~text
coverage entries exactly cover supplied catalog
~~~

No puede demostrar por sintaxis:

~~~text
supplied catalog contains every material obligation
for the governed evaluation question
~~~

Por tanto la completitud semántica del catálogo requiere una revisión externa
ligada exactamente a:

~~~text
relation_id
evaluation_question_identity
obligation_catalog_digest
qualification_bundle_digest
evaluated_candidate_commit
~~~

Si no existe esa revisión:

~~~text
qualification_review_result = INCONCLUSIVE
~~~

Un catálogo O01-only nunca puede transformarse en qualification PASS sólo porque
su coverage sea exacta.

## 14. Independent Qualification Review Evidence

Nombre candidato:

~~~text
GovernedDeterministicOracleQualificationReviewEvidenceV0
~~~

Schema conceptual:

~~~text
schema_version
repository
evaluated_candidate_commit
qualification_bundle_digest

reviewed_relation_id
reviewed_evaluation_question_identity
reviewed_obligation_catalog_digest

implementation_actor_id
qualification_reviewer_id
qualification_validator_id

structural_validator_result
structural_validator_evidence_reference

catalog_completeness_result
independence_review_result
verification_material_review_result

qualification_review_result
finding_refs[]
evidence_references[]
authority_effect
~~~

Terminal enum:

~~~text
PASS | FAIL | INCONCLUSIVE
~~~

Este artefacto es evidencia de proceso/dominio; no es authority ni Stage 2
receipt.

## 15. Qué puede validar automáticamente el Review Evidence validator

Un futuro validator de Review Evidence podría comprobar:

- schema exacto;
- candidate exacto;
- bundle digest exacto;
- structural validator result;
- terminal aggregation;
- campos y refs no vacíos;
- no self-contradiction;
- absence of authority fields.

No puede comprobar automáticamente en V0:

- identidad humana autenticada;
- que GitHub account X corresponda materialmente a una persona;
- que dos IDs distintos sean dos actores reales;
- que el reviewer haya actuado independientemente sólo por declararlo.

Por tanto cualquier helper conserva:

~~~text
identity_independence_verified = false
requires_external_validation   = true
~~~

La independencia real sigue siendo una propiedad del proceso revisada
externamente.

## 16. Persistencia externa y anti-recursión

Durante la validación del candidate activo:

~~~text
active Qualification Review Evidence
→ external to candidate worktree
~~~

Soportes candidatos ya compatibles con Malāk:

- conversación de la PR ligada al SHA;
- artefacto de validator;
- informe independiente externo ligado al SHA.

Una copia histórica posterior dentro del repo:

~~~text
describes prior candidate
!= certifies commit containing the copy
~~~

No se crea store, registry ni database.

## 17. Relación con RDD Stage 1

Flujo:

~~~text
Qualification Bundle
        ↓
Structural Validator
        ↓
validator_result

Independent Qualification Review
        ↓
Qualification Review Evidence
        ↓
domain evidence reference

RDD Evidence Manifest
        ↓
candidate-bound construction evidence

RDD Candidate Conformance
        ↓
process conformance only

Human review / Owner
        ↓
authority remains human
~~~

RDD Stage 1 no autentica mágicamente reviewer identity.

## 18. Terminal qualification semantics

V0 congela:

~~~text
structural validator FAIL
→ qualification cannot PASS

structural validator INCONCLUSIVE
→ qualification cannot PASS

structural validator PASS
+ catalog completeness FAIL
→ qualification FAIL

structural validator PASS
+ any external review dimension INCONCLUSIVE
→ qualification INCONCLUSIVE

all required external review dimensions PASS
+ exact candidate/bundle binding
→ qualification_review_result PASS
~~~

El PASS es una disposición de revisión independiente sobre evidencia, no una
decisión de runtime.

## 19. Original artifact declared result

El nuevo schema del Qualification Bundle V0 **NO admite**:

~~~text
qualification_result
qualification_reasons
~~~

como campos de input.

Regla congelada:

~~~text
caller supplies qualification_result and/or qualification_reasons
→ schema mismatch
→ validator_result = INCONCLUSIVE
→ qualification cannot PASS
~~~

No existe compatibilidad legacy dentro del Bundle V0 para estos campos.
El resultado terminal sólo puede derivarse de Structural Validation +
Independent Qualification Review Evidence bajo los bindings exactos aplicables.

## 20. Mapping de findings F237-F4R

### F237-F4R-01 — self-declared independence

Corrección de contrato:

~~~text
offline validator cannot certify independence
external process review required
~~~

### F237-F4R-02 — omission-based PASS

Corrección:

~~~text
exact supplied-catalog coverage
!= catalog completeness
catalog completeness is explicit external review dimension
~~~

### F237-F4R-03 — catalog digest

Corrección:

~~~text
recompute from canonical catalog bytes
~~~

### F237-F4R-04 — qualification material digest

Corrección:

~~~text
material must be present and digest recomputable
~~~

### F237-F4R-05 — runner identity

Corrección:

~~~text
runner identity derived from executing artifact, not caller declaration
~~~

### F237-F4R-06 — verification refs

Corrección:

~~~text
every ref resolves to supplied bounded evidence material
~~~

### F237-F4R-07 — expected_binding as authority

Corrección:

~~~text
reference material can be content-bound
but its governed provenance remains an external review claim
~~~

## 21. Security Horizon Check

### Zero Trust

No caller-controlled field adquiere trust por presencia o coherencia interna.

### Prompt/context trust

Textual review material remains DATA, not instruction or authority.

### Identity

V0 no inventa authenticated identity. Declarative IDs remain provenance only.

### Supply chain

Runner content identity becomes explicit and recomputable.

### Resources

All material remains bounded and offline.

### Human in Control

No review evidence authorizes runtime, routing, Ready or Merge.

### Resultado candidato

~~~text
new external service        0
new network dependency      0
new secret/credential       0
new authority surface       0
~~~

## 22. Cuatro preguntas de ley — Writer candidate

### Blueprint

No cambia Kernel, Planner, Registry, runtime ni Capability boundary.

~~~text
CANDIDATE PASS
~~~

### Cognitive Constitution

Refuerza evidence over speculation, traceability, uncertainty y
evidence-bound reliance.

~~~text
CANDIDATE PASS
~~~

### Governance Constitution

Impide self-certification y conserva separación Writer / Reviewer / Validator /
Authority.

~~~text
CANDIDATE PASS
~~~

### Kernel complexity

~~~text
Kernel delta = 0
CANDIDATE PASS
~~~

Estas disposiciones no sustituyen revisión independiente.

## 23. Design 4R — candidate

### Risk

El riesgo dominante es false-PASS por confundir material content-bound con
provenance independiente.

La corrección lo separa explícitamente.

Writer disposition:

~~~text
CANDIDATE PASS
~~~

### Readability

Dos responsabilidades distintas:

~~~text
structural validation
external qualification review
~~~

No manager/registry/framework.

Writer disposition:

~~~text
CANDIDATE PASS
~~~

### Reliability

Content digests recomputables + bundle digest + exact candidate binding.

Writer disposition:

~~~text
CANDIDATE PASS
~~~

### Resilience

Unresolved material/provenance/completeness:

~~~text
INCONCLUSIVE
~~~

Nunca positive PASS.

Writer disposition:

~~~text
CANDIDATE PASS
~~~

Terminal:

~~~text
PENDING INDEPENDENT REVIEW
~~~

## 24. RDD Stage 1 Design Check — candidate

Debe confirmar:

- candidate-bound evidence separation;
- active evidence external to candidate;
- no Stage 2 receipt;
- domain review result distinct from manifest validator result;
- Writer / Reviewer / Validator / Authority separation;
- PASS / FAIL / INCONCLUSIVE only;
- authority_effect none;
- candidate change invalidates affected evidence.

Writer precheck:

~~~text
CANDIDATE PASS
~~~

Terminal:

~~~text
PENDING INDEPENDENT REVIEW
~~~

## 25. Future RED — NOT AUTHORIZED

Un future RED deberá probar como mínimo:

~~~text
TB-R01 structural PASS cannot claim independence verified
TB-R02 no external review evidence → qualification INCONCLUSIVE
TB-R03 caller fabricates all role IDs/digests → no qualification PASS
TB-R04 obligation catalog digest recomputed from catalog
TB-R05 qualification material digest recomputed from material
TB-R06 verification refs must resolve to evidence material
TB-R07 fake/unresolved ref → INCONCLUSIVE
TB-R08 runner identity derived from actual runner
TB-R09 stale runner → INCONCLUSIVE
TB-R10 supplied O01-only catalog can be structurally exact but cannot become qualification PASS without completeness review
TB-R11 external review bound to wrong catalog digest → INCONCLUSIVE
TB-R12 external review bound to wrong bundle digest → INCONCLUSIVE
TB-R13 external review bound to wrong candidate → INCONCLUSIVE
TB-R14 structural FAIL prevents qualification PASS
TB-R15 structural INCONCLUSIVE prevents qualification PASS
TB-R16 external review FAIL propagates FAIL
TB-R17 external review INCONCLUSIVE propagates INCONCLUSIVE
TB-R18 all exact dimensions PASS can support qualification review PASS
TB-R19 authority_effect remains none
TB-R20 no Stage 2 / runtime / routing wiring
TB-R21 caller-declared qualification_result/reasons → schema mismatch → structural INCONCLUSIVE → no qualification PASS
~~~

## 26. Future implementation surface — NOT AUTHORIZED

Possible direction only:

~~~text
scripts/evaluate_e3_deterministic_oracle_qualification.py
tests/test_e3_deterministic_oracle_qualification.py
~~~

A second helper is not authorized by this design.

If a second validator/helper becomes necessary:

~~~text
STOP
→ scope review
~~~

Forbidden without separate authorization:

~~~text
src/malak/**
Kernel
Planner
Registry
runtime/provider
support_sufficient
routing consumer
evaluations/**
database/store
PKI/signatures
RDD Stage 2
PR #235
~~~

## 27. Disposición de PR #237

PR #237 permanece evidencia de un candidate GREEN que falló FULL 4R.

Esta contract correction no convierte:

~~~text
PR #237 FULL 4R FAIL
→ PASS
~~~

Después de integrar este diseño y superar sus gates, el Owner deberá decidir
separadamente si:

~~~text
A) PR #237 recibe una correction contract-aware
or
B) PR #237 se conserva/cierra como failed candidate y nace una nueva implementation unit
~~~

No se toma esa decisión dentro de este gate.

## 28. Correction Budget futuro

Si posteriormente se autoriza corregir la implementación:

~~~text
allowed production files    1
allowed test files          1
new dependencies            0
src/malak delta             0
runtime delta               0
architecture delta          0
authority delta             0
max fix rounds              2
~~~

STOP si aparece necesidad de:

- store/registry/database;
- PKI/signature;
- network verification;
- runtime/routing integration;
- Stage 2;
- contract reinterpretation adicional;
- third implementation file.

## 29. File Coverage

El baseline exacto fue inventariado recursivamente:

~~~text
tracked files discovered = 355
tracked files classified = 355
silently omitted files   = 0
tree truncated           = false
~~~

Ledger:

~~~text
docs/project/sprints/proposals/
MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-TRUST-BOUNDARY-V0-FILE-COVERAGE.tsv
~~~

El archivo prohibido:

~~~text
PROJECT - MANIFIESTO MALAK (1).docx
~~~

no aparece entre los blobs trackeados y no fue leído.

## 30. Estado de gate

~~~text
Owner contract-correction design authorization   YES
G0                                                PASS
G1                                                PASS
Critical Contract Hardening                       DESIGN CANDIDATE
Four Questions                                    WRITER CANDIDATE PASS
Design 4R                                         PENDING INDEPENDENT REVIEW
RDD Stage 1 Design Check                          PENDING INDEPENDENT REVIEW

PR #237                                            FROZEN / FULL 4R FAIL
RED                                                NOT AUTHORIZED
GREEN                                              NOT AUTHORIZED
implementation                                     NOT AUTHORIZED
runtime/routing                                    NOT AUTHORIZED
RDD Stage 2                                        NOT AUTHORIZED
authority_effect                                   none
~~~

## 31. Siguiente transición lícita

~~~text
independent pre-RED review
        ↓
Critical Contract Hardening
        ↓
Design 4R
        ↓
RDD Stage 1 Design Check
        ↓
Owner decision
~~~

No se modifica PR #237 durante esta revisión.
