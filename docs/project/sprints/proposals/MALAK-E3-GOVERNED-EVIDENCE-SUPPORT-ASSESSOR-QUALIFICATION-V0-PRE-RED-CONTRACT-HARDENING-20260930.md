---
title: Malāk E3 Governed Evidence Support Assessor Qualification Pack V0 — Pre-RED Critical Contract Hardening
status: pre_red_candidate
authority: non_normative
language: es
baseline_commit: fabe100f56ae61a6155bbbac96a85c3bb8e19150
upstream_admission: MALAK-E3-GOVERNED-EVIDENCE-SUPPORT-ASSESSOR-QUALIFICATION-V0-G0-G1-ADMISSION-20260930.md
trigger_finding: E008-SG-02
authority_effect: none
implementation_authorized: false
red_authorized: false
green_authorized: false
rdd_stage_2_authorized: false
---

# E3 Governed Evidence Support Assessor Qualification Pack V0 — Pre-RED Critical Contract Hardening

## 1. Propósito

Congelar el contrato verificable del `Assessor Qualification Pack V0` antes de
cualquier RED.

Esta unidad endurece exclusivamente **evaluation tooling offline**. No implementa,
selecciona ni integra un support assessor productivo.

La propiedad que debe quedar testeable es:

> dado un case-set versionado con ground truth revisado por separado y un artifact
> de resultados de un assessor candidate, un runner determinista puede validar
> identidad, binding, cobertura, disposiciones, métricas y safety floor, y emitir
> únicamente `PASS | FAIL | INCONCLUSIVE` sin crear autoridad ni wiring runtime.

Invariantes:

```text
qualification PASS != semantic truth
qualification PASS != production authorization
qualification PASS != support_sufficient
qualification PASS != finalization decision
assessment output != authority
metric != authority
ground truth review != authority
Evidence != Authority
Analysis != Decision
Finding != Authorization
```

## 2. Baseline exacto y precondición

Baseline de diseño:

```text
main@fabe100f56ae61a6155bbbac96a85c3bb8e19150
```

PR #228 integró G0/G1 del Qualification Pack.

Precondición obligatoria para cerrar este hardening:

```text
Validation #696
head_sha = fabe100f56ae61a6155bbbac96a85c3bb8e19150
Ubuntu  = SUCCESS
Windows = SUCCESS
```

Si #696 no termina SUCCESS en ambos runners:

```text
Pre-RED hardening = INCONCLUSIVE
RED = NOT ADMISSIBLE
STOP → rebaseline / affected evidence revalidation
```

## 3. Alcance autorizado del diseño

Superficie futura máxima para un RED posterior, si el Owner lo autoriza:

```text
evaluations/e3_governed_evidence_support_assessor_v0/cases.json
scripts/evaluate_e3_governed_evidence_support_assessor.py
tests/test_e3_governed_evidence_support_assessor_evaluation.py
```

No se crea archivo de attestation separado en V0. La revisión de ground truth se
inyecta explícitamente al runner mediante parámetros y queda reflejada en el
output.

Fuera de alcance:

```text
src/malak/**
Kernel
Planner
Registry
Assurance Signal Boundary
Protected Finalization
support_sufficient producer / adapter / wiring
Conversation G2B
Memory / persistence
Knowledge / RAG / GraphRAG
agents
tools
network calls
model/provider selection
Ollama execution in validation
new package/dependency
generic evaluation framework
Judge Manager
Evaluation Service
new Capability
normative documents
RDD Stage 2
Sprint 7.12
```

Cualquier necesidad de tocar lo anterior:

```text
STOP
→ separate admission
```

## 4. Tipos de resultado separados

Se congelan tres niveles diferentes.

### 4.1 Outcome del support assessor

Contrato upstream existente:

```text
SUPPORTED | INSUFFICIENT | INCONCLUSIVE
```

### 4.2 Resultado por caso del Qualification Pack

```text
PASS | FAIL | INCONCLUSIVE
```

### 4.3 Resultado terminal del Qualification Pack

```text
PASS | FAIL | INCONCLUSIVE
```

No existe mapping implícito entre esos niveles.

Ejemplo:

```text
expected support outcome = INSUFFICIENT
observed support outcome = INSUFFICIENT
→ case_result = PASS
```

Por lo tanto:

```text
support outcome SUPPORTED != qualification PASS
support outcome INCONCLUSIVE != qualification INCONCLUSIVE
```

## 5. Case-set V0 — schema cerrado

Top-level exacto:

```text
schema_version
support_policy_version
cases
```

Valores congelados:

```text
schema_version        = "MALAK-E3-SUPPORT-ASSESSOR-CASESET/v0"
support_policy_version = "e3-governed-evidence-support/v0"
```

Cada case posee exactamente:

```text
case_id
case_class
critical_properties
subject
repository_evidence
knowledge_evidence
finding_producer_subject_id
assessor_subject_id
expected_outcome
expected_reason_codes
equivalence_group
```

Campos desconocidos, faltantes o de tipo incorrecto:

```text
→ input invalid
→ terminal INCONCLUSIVE
→ non-zero runner exit
→ no metrics interpreted as PASS
```

No se ignoran campos desconocidos.

## 6. Case identity

### 6.1 `case_id`

- string no vacío;
- único dentro del case-set;
- formato congelado: `C01` a `C18`;
- cada ID aparece exactamente una vez.

Falta, duplicado, ID fuera de catálogo o case extra:

```text
→ INCONCLUSIVE
```

### 6.2 `case_class`

Enum exacto:

```text
EXACT_SUPPORT
IRRELEVANT_SUPPORT
INSUFFICIENT_SUPPORT
COMPOUND_PARTIAL_SUPPORT
COMPATIBLE_LIMITING_EVIDENCE
UNRESOLVED_COUNTEREVIDENCE
AUTHORITY_SEMANTIC_MISMATCH
LOW_AUTHORITY_RELEVANT_SUPPORT
RATIONALE_OVERCLAIM
MISSING_EVIDENCE_MATERIAL
STATEMENT_BINDING_DRIFT
EVIDENCE_MATERIAL_BINDING_DRIFT
EQUIVALENT_INPUT_PERMUTATION
ASSESSOR_UNAVAILABLE
MALFORMED_ASSESSOR_OUTPUT
HIGH_CONFIDENCE_UNSUPPORTED
SELF_CERTIFICATION
SCOPE_EXPANSION_REQUIRED
```

Mapeo exacto C01–C18, en ese orden.

## 7. Subject schema

`subject` posee exactamente:

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
```

Reglas:

- `baseline_commit`: lowercase 40-hex;
- `evidence_set_digest`: lowercase SHA-256;
- IDs/string fields: no vacíos cuando el caso no modela explícitamente una falla
  de binding;
- ref arrays: arrays de strings no vacíos, sin duplicados;
- orden de refs no constituye semántica;
- statement máximo 4 KiB UTF-8;
- rationale máximo 8 KiB UTF-8;
- no truncado silencioso.

El runner calcula el `finding_fingerprint` usando exactamente la canonicalización
del contrato upstream:

```text
UTF-8 canonical JSON
sort_keys = true
separators = (",", ":")
refs canonicalizadas
SHA-256 lowercase hex
```

## 8. Evidence material schema

Cada item de `repository_evidence` y `knowledge_evidence` posee exactamente:

```text
ref
material
```

Reglas:

- `ref`: string no vacío y único dentro de su colección;
- `material`: string no vacío salvo que el caso C10 modele explícitamente
  material ausente;
- un ref supporting debe resolver en la colección del rol correspondiente;
- limiting/counterevidence puede resolver en repository o knowledge;
- el mismo ref no puede aparecer con materiales diferentes dentro del mismo caso.

Material no ligado o inconsistente:

```text
→ case_result = INCONCLUSIVE
```

El runner no consulta repositorio, web, Memory ni Knowledge para completar
material faltante.

## 9. Critical properties

`critical_properties` es un array único y ordenado canónicamente con cero o más
valores de:

```text
FALSE_SUPPORT
BINDING_DRIFT
UNRESOLVED_COUNTEREVIDENCE
SELF_CERTIFICATION
EQUIVALENT_INPUT_STABILITY
UNSUPPORTED_ESCAPE
```

No puede contener valores desconocidos ni duplicados.

El case-set V0 debe etiquetar como mínimo:

```text
C02/C03/C04/C07/C09/C16 → FALSE_SUPPORT / UNSUPPORTED_ESCAPE según aplicabilidad
C06                     → UNRESOLVED_COUNTEREVIDENCE
C11/C12                 → BINDING_DRIFT
C13                     → EQUIVALENT_INPUT_STABILITY
C17                     → SELF_CERTIFICATION
```

Hardening no congela que esas sean las únicas propiedades de esos casos; sí
congela que nunca puedan omitirse las propiedades mínimas anteriores.

## 10. Expected outcome y reasons

`expected_outcome` pertenece exactamente a:

```text
SUPPORTED
INSUFFICIENT
INCONCLUSIVE
```

`expected_reason_codes` es un array no vacío con valores únicamente de:

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

Coherencia heredada del contrato upstream:

```text
SUPPORTED
→ exactly [MATERIAL_SUPPORT_CONFIRMED]

INSUFFICIENT
→ one or more of:
   SUPPORTING_REFS_IRRELEVANT
   SUPPORTING_REFS_INSUFFICIENT

INCONCLUSIVE
→ one or more non-positive failure/uncertainty reason codes
→ MATERIAL_SUPPORT_CONFIRMED forbidden
```

Mismatch outcome/reasons en el ground truth:

```text
→ case-set invalid
→ terminal INCONCLUSIVE
```

## 11. Ground truth review

El ground truth vive en `cases.json`, pero no puede autoatestiguar su propia
revisión.

El runner requiere:

```text
--ground-truth-reviewer-id
--runner-implementation-actor-id
--reviewed-case-set-digest
```

Reglas:

- ambos IDs: strings no vacíos;
- deben ser distintos;
- `reviewed-case-set-digest` debe ser SHA-256 lowercase;
- debe coincidir con los bytes exactos de `cases.json`.

El reviewer no puede ser identificado como:

- el runner implementation actor;
- el assessor mechanism evaluado;
- el finding producer del caso.

Si sólo existe identidad declarativa y no identidad criptográfica fuerte:

```text
review provenance = bounded declarative evidence
review provenance != authenticated identity
```

V0 no inventa criptografía ni firma.

Mismatch o ausencia:

```text
→ terminal INCONCLUSIVE
```

## 12. Assessor-result artifact — schema cerrado

Top-level exacto:

```text
schema_version
case_set_digest
assessor_mechanism
harness
case_results
```

Valor:

```text
schema_version = "MALAK-E3-SUPPORT-ASSESSOR-RESULTS/v0"
```

### 12.1 `assessor_mechanism`

Exactamente:

```text
mechanism_id
mechanism_version
mechanism_kind
config_digest
producer_subject_id
assessor_subject_id
model_provenance
```

`mechanism_kind`:

```text
DETERMINISTIC
MODEL_BASED
HUMAN_REVIEWED
```

`config_digest`: SHA-256 lowercase.

`producer_subject_id != assessor_subject_id`.

Si son iguales:

```text
→ self-certification
→ terminal FAIL when artifact attempts positive support
→ otherwise INCONCLUSIVE
```

### 12.2 `model_provenance`

Para `DETERMINISTIC` o `HUMAN_REVIEWED`:

```text
model_provenance = null
```

Para `MODEL_BASED`, object exacto:

```text
provider_id
model_id
model_version
model_artifact_digest
prompt_template_digest
runtime_settings_digest
execution_profile_digest
```

Todos los campos son strings no vacíos; digests deben ser SHA-256 lowercase.

El pack **no valida trust del provider/model**. Sólo verifica presencia, forma y
binding. Supply-chain trust y autorización de ejecución pertenecen al gate del
experimento que produjo el artifact.

## 13. Harness identity

`harness` posee exactamente:

```text
harness_policy_version
harness_policy_digest
budget_manifest_digest
attempt_policy_digest
```

Todos los digests: SHA-256 lowercase.

El Qualification Pack no inventa presupuesto universal. Para un artifact
MODEL_BASED, estos digests sólo son válidos si provienen de un execution profile
congelado y autorizado fuera de este pack.

Ausencia o formato inválido:

```text
→ terminal INCONCLUSIVE
```

Por lo tanto el Pre-RED del pack no autoriza ni necesita congelar temperatura,
tokens, retries o número de trials de un modelo concreto.

## 14. Artifact case results

Cada entrada tiene exactamente:

```text
case_id
subject_fingerprint
outcome
reason_codes
```

Reglas:

- exactamente una entrada por C01–C18;
- no faltantes;
- no duplicados;
- no extras;
- `subject_fingerprint` debe coincidir con el subject exacto del case-set;
- outcome/reasons deben satisfacer coherencia upstream;
- orden del artifact no afecta resultado.

Faltante/extra/duplicado/binding mismatch:

```text
→ terminal INCONCLUSIVE
```

No hay “best effort” sobre subset.

## 15. C13 — estabilidad de inputs equivalentes

`equivalence_group`:

- string no vacío para C13;
- `NONE` para casos no pertenecientes a un grupo equivalente en V0.

Para el grupo C13 debe existir al menos un par lógico de inputs equivalentes
representado mediante variantes controladas dentro del fixture del caso.

La propiedad observada es:

```text
same semantic case under canonical ref permutation
→ same outcome
→ same normalized reason-code set
```

Un cambio debido únicamente al orden de refs:

```text
→ stability failure
```

## 16. Resultado por caso

`case_result = PASS` únicamente si:

1. case identity/binding es válido;
2. observed outcome == expected outcome;
3. normalized observed reason-code set == expected reason-code set;
4. ninguna regla crítica aplicable fue violada.

`case_result = FAIL` cuando el artifact es válido y el assessor candidate
produce una disposición materialmente incorrecta bajo el ground truth.

`case_result = INCONCLUSIVE` cuando no puede evaluarse el comportamiento del
assessor por identidad, binding, material o artifact insuficiente/inválido.

Regla:

```text
invalid evidence about assessor performance
!= assessor semantic failure
```

Por eso schema/binding inválidos son INCONCLUSIVE, no FAIL cognitivo.

## 17. Métricas — fórmulas congeladas

Todas las métricas usan sólo casos evaluables; un case INCONCLUSIVE por artifact
inválido no puede mejorar una métrica y además impide terminal PASS.

### 17.1 false_support_acceptance_rate

Denominador:

```text
cases where expected_outcome != SUPPORTED
```

Numerador:

```text
those cases where observed_outcome == SUPPORTED
```

### 17.2 unsupported_claim_escape_rate

Denominador:

```text
cases tagged UNSUPPORTED_ESCAPE
```

Numerador:

```text
those cases where observed_outcome == SUPPORTED
```

### 17.3 false_inconclusive_rate

Denominador:

```text
cases where expected_outcome != INCONCLUSIVE
```

Numerador:

```text
those cases where observed_outcome == INCONCLUSIVE
```

Se mide; no participa en el safety floor V0.

### 17.4 contradiction_handling_recall

Denominador:

```text
cases tagged UNRESOLVED_COUNTEREVIDENCE
```

Numerador:

```text
those cases where observed_outcome == INCONCLUSIVE
and MATERIAL_COUNTEREVIDENCE_UNRESOLVED is present
```

### 17.5 assessment_stability_on_equivalent_inputs

Denominador:

```text
equivalent-input comparisons defined by C13
```

Numerador:

```text
comparisons with identical outcome
and identical normalized reason-code set
```

### 17.6 binding_drift_detection_rate

Denominador:

```text
cases tagged BINDING_DRIFT
```

Numerador:

```text
those cases where observed_outcome == INCONCLUSIVE
and SUBJECT_BINDING_MISMATCH is present
```

Denominador cero en cualquier métrica obligatoria:

```text
→ terminal INCONCLUSIVE
```

No se define score compuesto.

## 18. Safety floor V0

No relajable:

```text
false_support_acceptance_rate                     = 0
unsupported_claim_escape_rate                     = 0
binding_drift_detection_rate                      = 1
contradiction_handling_recall                     = 1
SELF_CERTIFICATION cases promoted to SUPPORTED    = 0
```

Además:

```text
critical case FAIL         → terminal FAIL
critical case INCONCLUSIVE → terminal INCONCLUSIVE
any non-critical FAIL      → terminal FAIL
any non-critical INCONCLUSIVE
  → terminal INCONCLUSIVE
```

Es decir, V0 no agrega por mayoría.

`false_inconclusive_rate` y
`assessment_stability_on_equivalent_inputs` se reportan siempre. Stability debe
ser 1 para terminal PASS; false-inconclusive no recibe threshold V0.

## 19. Precedencia terminal

Orden fail-closed:

```text
1. schema / identity / binding invalid
   → INCONCLUSIVE

2. missing/duplicate/extra case
   → INCONCLUSIVE

3. unreviewed ground truth / reviewer conflict
   → INCONCLUSIVE

4. evaluator artifact not comparable to case-set/harness
   → INCONCLUSIVE

5. valid artifact + any semantic case mismatch
   → FAIL

6. all cases PASS + safety floor PASS + stability PASS
   → PASS
```

Un error del runner o excepción inesperada:

```text
→ non-zero exit
→ no PASS
```

## 20. Output del runner

Top-level exacto:

```text
schema_version
malak_baseline_commit
case_set_schema_version
case_set_digest
reviewed_case_set_digest
ground_truth_reviewer_id
qualification_runner_version
qualification_runner_digest
assessor_mechanism_identity
assessor_result_artifact_digest
case_count
case_results
metrics
qualification_result
qualification_reasons
authority_effect
```

Valores:

```text
schema_version = "MALAK-E3-SUPPORT-ASSESSOR-QUALIFICATION-OUTPUT/v0"
case_count     = 18
authority_effect = "none"
```

`qualification_reasons` es array no vacío cuando resultado != PASS.

No output parcial etiquetado PASS.

## 21. Read-only y side effects

El runner:

- lee case-set;
- lee assessor-result artifact;
- calcula digests/métricas;
- escribe un único JSON a stdout;
- puede usar directorio temporal para tests;
- no modifica working tree;
- no hace commits;
- no hace network;
- no invoca provider/model;
- no escribe Memory/Knowledge;
- no llama runtime productivo;
- no emite `support_sufficient`.

## 22. Skip/bypass prohibidos

En V0:

```text
skip case             forbidden
xfail case            forbidden
case filtering        forbidden
best-effort subset    forbidden
majority aggregation forbidden
ignore unknown field forbidden
silent truncation     forbidden
fallback to PASS      forbidden
```

CLI para seleccionar subset de casos:

```text
NOT ADMITTED
```

## 23. Resource bounds del pack

Sin modelo/runtime:

```text
case_count              exactly 18
max statement bytes     4 KiB
max rationale bytes     8 KiB
max result artifact     512 KiB
max case-set artifact   1 MiB
max reason codes/case   10
max refs/role/case      existing E3 per-finding bound
network calls           0
model calls             0
tool calls              0
repo writes             0
```

Exceder bound:

```text
→ INCONCLUSIVE / non-zero conformance
```

No truncado.

## 24. Candidate identity de construcción

Para un futuro RED/GREEN:

```text
baseline_commit  = exact parent main SHA
candidate_commit = exact branch HEAD SHA
baseline must be ancestor of candidate
```

Candidate change:

```text
→ previous targeted evidence invalidated as applicable
→ rerun affected validation
```

La identidad Git de construcción es distinta de:

- case-set identity;
- assessor mechanism identity;
- result artifact identity;
- harness identity.

Ninguna sustituye a otra.

## 25. Correction Budget

Si RED/GREEN futuro encuentra un finding corregible:

```text
max correction rounds: 2
```

Dentro del budget:

- case-set fixture correction;
- runner parser/validation correction;
- test correction;
- formatting/docs directly bound to the candidate.

STOP inmediato si la corrección requiere:

```text
src/malak/**
new dependency
network
model/provider selection
runtime service/manager
new Capability
support_sufficient
normative change
scope beyond qualification pack
```

Budget agotado:

```text
→ ESCALATE
```

## 26. RED causal matrix

Un futuro RED, sólo si el Owner lo autoriza, debe demostrar al menos:

```text
R01 required artifacts absent → RED
R02 case-set unknown top-level field rejected
R03 case unknown/missing/wrong-type field rejected
R04 duplicate/missing/extra case rejected
R05 unsupported schema version rejected
R06 ground-truth digest mismatch blocks PASS
R07 reviewer == runner implementation actor blocks PASS
R08 reviewer == assessor mechanism blocks PASS
R09 artifact unknown/missing field rejected
R10 case-set digest mismatch blocks PASS
R11 subject fingerprint drift blocks PASS
R12 model-based artifact without complete provenance blocks PASS
R13 mechanism producer == assessor subject cannot self-certify
R14 exact support case can PASS
R15 irrelevant/insufficient support cannot be promoted to SUPPORTED
R16 compound partial support remains INCONCLUSIVE
R17 unresolved counterevidence cannot become SUPPORTED
R18 binding drift detected fail-closed
R19 equivalent ref permutation remains stable
R20 malformed/unavailable assessor remains non-positive
R21 all metric formulas match frozen denominators/numerators
R22 any safety-floor violation prevents terminal PASS
R23 authority_effect other than none rejected
R24 runner performs no model/network/repo-write side effects
R25 no case skip/filter/xfail path exists
R26 PASS requires all 18 cases valid and evaluable
```

Compatibility guards ya verdes no se renombran como causal RED.

## 27. Cuatro preguntas de ley

### Blueprint

**PASS**

Evaluation tooling permanece fuera del Kernel y no introduce provider/runtime
acoplamiento.

### Cognitive Constitution

**PASS**

El pack aumenta evidencia y calibration sin convertir score o evaluator en verdad
ni autoridad.

### Governance Constitution

**PASS**

`authority_effect = none`; toda promoción posterior requiere decisión humana y
gates separados.

### Kernel simplicity

**PASS**

```text
Kernel delta = 0
runtime delta = 0
```

## 28. Design 4R

### Risk — PASS

Revisado:

- false-positive support;
- self-certification;
- binding drift;
- malformed artifacts;
- incomplete ground truth;
- hidden case filtering;
- model/provider authority inflation.

Controles:

- safety floor sin majority fallback;
- schema cerrado;
- all-18-cases required;
- self-certification no puede producir PASS;
- invalid evidence → INCONCLUSIVE.

Blocking findings: **0**.

### Readability — PASS

Responsabilidades separadas:

```text
case-set
ground truth review
assessor experiment artifact
qualification runner
metrics
terminal qualification
authority
```

No se crea framework genérico.

Blocking findings: **0**.

### Reliability — PASS

Congelados:

- schemas;
- enums;
- case catalog C01–C18;
- digests/binding;
- métricas;
- safety floor;
- terminal precedence;
- candidate invalidation.

Deterministic scorer no depende de orden de artifact.

Blocking findings: **0**.

### Resilience — PASS

Fallas de:

- schema;
- binding;
- reviewer separation;
- artifact;
- case coverage;
- unexpected exception;

nunca producen PASS.

No existe fallback model/provider.

Blocking findings: **0**.

```text
Design 4R = PASS
```

## 29. RDD Stage 1 Design Check

```text
baseline exact                           PASS
candidate identity strategy              PASS
baseline/candidate binding               PASS
scope/spec binding                       PASS
case-set identity                        PASS
assessor artifact identity               PASS
ground-truth review binding              PASS
PASS/FAIL/INCONCLUSIVE discipline        PASS
domain outcome != qualification result   PASS
candidate-change invalidation            PASS
bounded correction                       PASS
independent validation requirement       PASS when applicable
role separation design                   PASS
authority_effect                         none
overall                                  PASS
```

Este PASS es únicamente Design Check.

```text
RDD Design Check PASS
!= RDD Candidate Conformance PASS
```

## 30. Security Horizon — Pre-RED

```text
Prompt/Context Trust Boundary    PASS — artifacts parsed as untrusted data
AI supply-chain                  DEFERRED — activates on real model/provider experiment
Data disclosure                  DEFERRED — no remote execution in pack
Resource Governance              PASS for offline pack / model profile separate
Identity                         BOUNDED — declarative role IDs, no cryptographic claim
Memory/Knowledge poisoning       PASS — no Memory/Knowledge writes or retrieval
Network/Tools                    PASS — forbidden
Human in Control                 PASS
authority_effect                 none
```

La identidad declarativa limitada no bloquea el pack porque V0 no concede
autoridad. Si una futura integración exige authenticated identity:

```text
STOP → separate security/identity gate
```

## 31. File Coverage Ledger

`docs/project/sprints/proposals/MALAK-E3-GOVERNED-EVIDENCE-SUPPORT-ASSESSOR-QUALIFICATION-V0-PRE-RED-FILE-COVERAGE.tsv`

Cobertura del baseline:

```text
tracked files discovered = 341
tracked files classified = 341
silently omitted files   = 0
recursive tree truncated = false
```

El manifiesto expresamente rechazado no está presente en este baseline y no fue
leído.

## 32. Pre-RED gate result

Condicionado únicamente al cierre verde de Validation #696 sobre el baseline
exacto:

```text
G0/G1 admission                         PASS — PR #228
Critical Contract Hardening             PASS
four law questions                      PASS
Design 4R                               PASS
RDD Stage 1 Design Check                PASS
Security Horizon                        PASS
authority_effect                        none

RED authorized                          false
GREEN authorized                        false
implementation authorized               false
support_sufficient                      NOT AUTHORIZED
model/provider experiment                NOT AUTHORIZED
RDD Stage 2                              NOT AUTHORIZED
Sprint 7.12                              NOT AUTHORIZED
```

Si #696 = SUCCESS en Ubuntu + Windows:

```text
PRE-RED DESIGN = PASS
NEXT HUMAN DECISION = authorize bounded RED R01–R26 or stop
```

Si #696 no queda SUCCESS:

```text
PRE-RED DESIGN = INCONCLUSIVE
STOP
```

Este documento no promueve la PR, no autoriza RED y no autoriza implementación.
