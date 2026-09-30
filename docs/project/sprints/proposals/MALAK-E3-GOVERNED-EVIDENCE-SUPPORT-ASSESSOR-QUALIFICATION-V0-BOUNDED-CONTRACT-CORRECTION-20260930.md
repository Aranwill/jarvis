---
title: Malāk E3 Assessor Qualification Pack V0 — Bounded Contract Correction
status: correction_candidate
authority: non_normative
language: es
baseline_commit: 0bf5fab6b4998b9ff8dbbabbb80e16bcddaf2627
trigger_candidate: 655bde3a16e8d20047d6ee3286c6a4ff89a57294
trigger_pr: 230
trigger_validation: 702
correction_round: 1/2
authority_effect: none
red_authorized: false
green_authorized: false
implementation_authorized: false
---

# E3 Assessor Qualification Pack V0 — Bounded Contract Correction

## 1. Motivo

Durante GREEN de PR #230, el candidate exacto:

`655bde3a16e8d20047d6ee3286c6a4ff89a57294`

alcanzó:

```text
Ubuntu   1707 passed
Windows  1707 passed
compileall PASS
diff --check PASS
```

Sin embargo, Candidate FULL 4R detectó un gap material que los tests existentes no
demostraban.

Findings de corrección:

```text
AQ-CORR-01  C13 no preserva dos outputs observados del assessor para inputs equivalentes.
AQ-CORR-02  C11 no materializa un binding previo stale contra el subject actual.
AQ-CORR-03  C12 no materializa un binding previo stale contra evidence material actual.
AQ-CORR-04  C05 etiqueta compatible limiting evidence sin exigir material limiting explícito.
AQ-CORR-05  varios escenarios dependen demasiado de case_class/labels en lugar de inputs reproducibles.
```

Estos findings afectan Reliability y Auditability del Qualification Pack.

No demuestran:

- defecto runtime de Malāk;
- aumento de autoridad;
- defecto de Kernel;
- fallo de `support_sufficient`;
- necesidad de model/provider;
- necesidad de nueva Capability.

## 2. Disposición de evidencia previa

La historia NO se reescribe.

Permanece registrado:

```text
PR #229 Pre-RED contract            historical PASS
External audit R1                   INCONCLUSIVE
External audit R2                   PASS
PR #230 RED                         causal PASS
PR #230 GREEN tests                 PASS / 1707
Candidate FULL 4R sobre #230        FAIL
```

La detección posterior invalida como evidencia suficiente, para las propiedades
afectadas:

- el Design 4R de #229;
- el RDD Stage 1 Design Check de #229;
- la parte correspondiente de External Audit R2;
- RED/GREEN de #230 para el contrato corregido.

No se convierten retroactivamente en FAIL. Quedan como evidencia histórica del
contrato anterior.

## 3. Alcance de esta corrección

Esta unidad corrige exclusivamente representación y binding del evaluation pack.

Permitido:

- schema documental del case-set;
- schema documental del assessor-result artifact;
- semántica de C05/C11/C12/C13;
- fórmulas afectadas;
- causal matrix futura;
- invalidation rules.

Prohibido:

```text
src/malak/**
Kernel
Planner
Registry
Assurance Signal Boundary
Protected Finalization
support_sufficient
runtime
model/provider selection
network/tools
Memory/Knowledge writes
new dependency
new Capability
generic evaluation framework
RDD Stage 2
Sprint 7.12
```

## 4. Principio corregido

Un case adversarial no puede quedar demostrado sólo por:

```text
case_id
+
case_class
+
expected label
```

Debe contener suficiente material para reproducir la propiedad evaluada.

Regla:

```text
scenario label != scenario evidence
expected disposition != demonstrated assessor behavior
fingerprint stability != assessor output stability
```

## 5. Versionado corregido

Los schemas afectados se incrementan sin reutilizar semántica anterior:

```text
case-set schema:
MALAK-E3-SUPPORT-ASSESSOR-CASESET/v0.1

assessor-results schema:
MALAK-E3-SUPPORT-ASSESSOR-RESULTS/v0.1

qualification output schema:
MALAK-E3-SUPPORT-ASSESSOR-QUALIFICATION-OUTPUT/v0.1
```

La versión upstream de support policy permanece:

```text
e3-governed-evidence-support/v0
```

Esto NO cambia el contrato productivo upstream; sólo cambia el pack offline que
lo califica.

## 6. Case-set v0.1 — top-level

Top-level exacto:

```text
schema_version
support_policy_version
cases
```

Cada case posee exactamente:

```text
case_id
case_class
critical_properties
finding_producer_subject_id
assessor_subject_id
inputs
comparison_rule
```

## 7. Case input — unidad reproducible

Cada item de `inputs` posee exactamente:

```text
input_id
subject
repository_evidence
knowledge_evidence
binding_expectation
binding_prior
expected_outcome
expected_reason_codes
```

### 7.1 cardinalidad

V0.1 congela:

```text
C01-C12 = exactly 1 input
C13     = exactly 2 inputs
C14-C18 = exactly 1 input

total inputs = 19
```

No se admiten inputs adicionales.

### 7.2 input_id

Formato:

```text
<case_id>.I01
<case_id>.I02
```

C13:

```text
C13.I01
C13.I02
```

Los demás:

```text
<case_id>.I01
```

## 8. Subject y evidence material

`subject` conserva exactamente:

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

Cada evidence item conserva:

```text
ref
material
```

Los límites permanecen:

```text
statement <= 4 KiB UTF-8
rationale <= 8 KiB UTF-8
refs/role <= existing E3 bound
```

## 9. Input digest

Cada input posee identidad independiente.

`input_digest` se calcula sobre canonical JSON de:

```text
subject
repository_evidence
knowledge_evidence
binding_expectation
binding_prior
```

Canonicalización:

```text
UTF-8
sort_keys = true
separators = (",", ":")
ref arrays canonicalizadas cuando su orden no es semántico
evidence collections ordenadas por ref
SHA-256 lowercase
```

El artifact nunca puede suministrar su propio input material; sólo referencia el
`input_digest` del case-set revisado.

## 10. Binding expectation

Cada input posee exactamente:

```text
binding_kind
expected_subject_fingerprint
expected_evidence_material_digest
```

`binding_kind`:

```text
NONE
SUBJECT
EVIDENCE_MATERIAL
```

### 10.1 NONE

Para casos sin drift:

```text
binding_kind = NONE
expected_subject_fingerprint = null
expected_evidence_material_digest = null
```

### 10.2 SUBJECT

Sólo C11 en V0.1.

Debe contener:

```text
binding_kind = SUBJECT
expected_subject_fingerprint = <64-hex prior binding>
expected_evidence_material_digest = null
```

El expected fingerprint debe:

- ser válido SHA-256;
- diferir del fingerprint del subject actual;
- corresponder a una variante previa materializada por el fixture de ground truth.

No se admite un hash arbitrario no derivable del fixture.

### 10.3 EVIDENCE_MATERIAL

Sólo C12 en V0.1.

Debe contener:

```text
binding_kind = EVIDENCE_MATERIAL
expected_subject_fingerprint = null
expected_evidence_material_digest = <64-hex prior evidence material binding>
```

El digest debe:

- ser válido SHA-256;
- diferir del evidence-material digest actual;
- corresponder a material previo explícitamente materializado por el fixture.

## 11. Prior binding material

Cada input posee además `binding_prior`.

Para casos con `binding_kind = NONE`:

```text
binding_prior = null
```

Para C11/C12, `binding_prior` es un object exacto:

```text
prior_subject
prior_repository_evidence
prior_knowledge_evidence
```

### 11.1 C11

```text
prior_subject                 = complete prior subject object
prior_repository_evidence     = null
prior_knowledge_evidence      = null
```

El runner recomputa el prior subject fingerprint usando la misma canonicalización
del subject actual y exige coincidencia exacta con
`expected_subject_fingerprint`.

### 11.2 C12

```text
prior_subject                 = null
prior_repository_evidence     = explicit prior repository evidence array
prior_knowledge_evidence      = explicit prior knowledge evidence array
```

Al menos una de las dos evidence arrays debe contener material.

El runner calcula `evidence_material_digest` sobre canonical JSON de:

```text
repository_evidence sorted by ref
knowledge_evidence sorted by ref
```

con:

```text
UTF-8
sort_keys = true
separators = (",", ":")
SHA-256 lowercase
```

El mismo algoritmo se aplica al evidence material actual.

Para C12:

```text
prior refs logical set == current refs logical set
prior evidence_material_digest != current evidence_material_digest
```

`binding_prior` es ground-truth material del evaluation pack y NO es evidence
productivo ni puede pasarse al assessor candidate como evidence de soporte.

Si prior binding no puede recomputarse:

```text
→ case-set invalid
→ terminal INCONCLUSIVE
```

## 12. C05 — compatible limiting evidence

C05.I01 debe contener:

- al menos un supporting repository o knowledge ref material;
- al menos un `limiting_or_counterevidence_ref`;
- material concreto para ese limiting ref;
- expected outcome `SUPPORTED`;
- expected reason exactly `MATERIAL_SUPPORT_CONFIRMED`.

El limiting material debe ser compatible con el claim, no contradictorio.

El runner no decide compatibilidad semántica; ésta pertenece al ground truth
independientemente revisado.

Lo que el runner sí verifica es que la propiedad no sea sólo una etiqueta:

```text
limiting_or_counterevidence_refs non-empty
material resolves
ground truth reviewed
artifact observation bound to exact input
```

## 13. C11 — statement binding drift

C11.I01 debe materializar:

```text
current subject statement
prior subject statement
prior expected subject fingerprint
current subject fingerprint
```

Y debe cumplir:

```text
prior fingerprint != current fingerprint
expected outcome = INCONCLUSIVE
expected reason  = SUBJECT_BINDING_MISMATCH
```

No basta:

```text
case_class = STATEMENT_BINDING_DRIFT
```

## 14. C12 — evidence material binding drift

C12.I01 conserva el mismo logical ref pero materializa:

```text
prior evidence material
current evidence material
prior expected evidence-material digest
current evidence-material digest
```

Y debe cumplir:

```text
prior digest != current digest
expected outcome = INCONCLUSIVE
expected reason  = SUBJECT_BINDING_MISMATCH
```

No basta:

```text
case_class = EVIDENCE_MATERIAL_BINDING_DRIFT
```

## 15. C13 — equivalent input stability

C13 posee exactamente:

```text
C13.I01
C13.I02
```

Ambos inputs representan el mismo caso semántico.

La única diferencia admitida es una transformación de equivalencia congelada:

```text
canonical ref permutation
```

Deben compartir:

- statement;
- rationale;
- relation_id;
- classification;
- evidence material;
- uncertainty basis;
- expected outcome;
- normalized expected reason-code set.

Pueden diferir únicamente en el orden no semántico de refs/evidence collections.

`comparison_rule`:

```text
STABLE_OUTCOME_AND_REASONS
```

Para todos los demás casos:

```text
comparison_rule = NONE
```

## 16. Assessor-result artifact v0.1

Top-level permanece:

```text
schema_version
case_set_digest
assessor_mechanism
harness
case_results
```

Cada `case_result` posee exactamente:

```text
case_id
observations
```

Cada observation posee exactamente:

```text
input_id
input_digest
subject_fingerprint
outcome
reason_codes
```

Reglas:

- una observation por input;
- ninguna faltante;
- ninguna duplicada;
- ninguna extra;
- `input_digest` debe coincidir con el input exacto del case-set;
- `subject_fingerprint` debe coincidir con el subject actual del input;
- outcome/reasons deben satisfacer coherencia upstream.

Así:

```text
artifact C13
→ observation C13.I01
→ observation C13.I02
```

La estabilidad ya no se infiere del fingerprint.

## 17. Resultado por input

`input_result = PASS` sólo si:

1. input identity/binding válido;
2. observed outcome == expected outcome;
3. normalized observed reason-code set == expected reason-code set;
4. reglas críticas del input satisfechas.

`input_result = FAIL`:

- artifact válido;
- assessor candidate produjo resultado materialmente incorrecto.

`input_result = INCONCLUSIVE`:

- no puede evaluarse por schema, identity, binding o material insuficiente.

## 18. Resultado por case

`case_result = PASS` sólo si:

- todos sus inputs PASS;
- comparison rule, si existe, PASS.

`case_result = FAIL` si:

- cualquier input válido FAIL;
- comparison rule demuestra mismatch.

`case_result = INCONCLUSIVE` si:

- cualquier input no es evaluable;
- comparison evidence es incompleta.

## 19. Stability corregida

`assessment_stability_on_equivalent_inputs` mide outputs observados reales.

Denominador:

```text
comparison pairs declared by comparison_rule
```

V0.1:

```text
exactly 1 pair: C13.I01 ↔ C13.I02
```

Numerador:

```text
pairs where:
observed outcome I01 == observed outcome I02
AND
normalized reason-code set I01 == normalized reason-code set I02
```

No participa:

- fingerprint equality;
- expected labels por sí solos;
- canonicalization del runner como sustituto del segundo output.

## 20. Otras métricas

Las métricas se calculan sobre inputs evaluables, no sobre etiquetas de case.

### false_support_acceptance_rate

Denominador:

```text
inputs where expected_outcome != SUPPORTED
```

Numerador:

```text
those inputs observed as SUPPORTED
```

### unsupported_claim_escape_rate

Denominador:

```text
inputs whose parent case is tagged UNSUPPORTED_ESCAPE
```

Numerador:

```text
those inputs observed as SUPPORTED
```

### false_inconclusive_rate

Denominador:

```text
inputs where expected_outcome != INCONCLUSIVE
```

Numerador:

```text
those inputs observed as INCONCLUSIVE
```

### contradiction_handling_recall

Denominador:

```text
inputs whose parent case is tagged UNRESOLVED_COUNTEREVIDENCE
```

Numerador:

```text
those inputs observed INCONCLUSIVE
with MATERIAL_COUNTEREVIDENCE_UNRESOLVED
```

### binding_drift_detection_rate

Denominador:

```text
inputs whose parent case is tagged BINDING_DRIFT
AND whose binding expectation is materialized and recomputable
```

Numerador:

```text
those inputs observed INCONCLUSIVE
with SUBJECT_BINDING_MISMATCH
```

Denominador cero:

```text
→ terminal INCONCLUSIVE
```

## 21. Safety floor

Sin relajación:

```text
false_support_acceptance_rate                     = 0
unsupported_claim_escape_rate                     = 0
binding_drift_detection_rate                      = 1
contradiction_handling_recall                     = 1
assessment_stability_on_equivalent_inputs         = 1
SELF_CERTIFICATION inputs promoted to SUPPORTED   = 0
```

No majority fallback.

## 22. Resource bounds corregidos

```text
case_count              exactly 18
input_count             exactly 19
max inputs/case         2
C13 inputs              exactly 2
all other cases         exactly 1
max result artifact     512 KiB
max case-set artifact   1 MiB
max reason codes/input  10
max refs/role/input     existing E3 per-finding bound
network calls           0
model calls             0
tool calls              0
repo writes             0
```

## 23. Output v0.1

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
input_count
case_results
metrics
qualification_result
qualification_reasons
authority_effect
```

Valores:

```text
schema_version   = MALAK-E3-SUPPORT-ASSESSOR-QUALIFICATION-OUTPUT/v0.1
case_count       = 18
input_count      = 19
authority_effect = none
```

Cada case result posee exactamente:

```text
case_id
input_results
comparison_result
case_result
mismatch_reasons
```

Cada input result posee exactamente:

```text
input_id
expected_disposition
observed_disposition
expected_reason_codes
observed_reason_codes
input_result
mismatch_reasons
```

Para cases con `comparison_rule = NONE`:

```text
comparison_result = null
```

Para C13:

```text
comparison_result = {
  rule,
  input_ids,
  result,
  mismatch_reasons
}
```

No existe output parcial etiquetado PASS.

## 24. Terminal precedence

```text
1. schema/identity/binding invalid
   → INCONCLUSIVE

2. missing/duplicate/extra case or input
   → INCONCLUSIVE

3. ground truth review/binding prior not reproducible
   → INCONCLUSIVE

4. assessor artifact not comparable
   → INCONCLUSIVE

5. valid artifact + any input semantic mismatch
   → FAIL

6. valid comparison + stability mismatch
   → FAIL

7. all inputs PASS + all comparisons PASS + safety floor PASS
   → PASS
```

## 25. Causal matrix corregida

R01-R26 permanecen como intención histórica, pero su implementación anterior NO
puede reutilizarse sin actualización.

La nueva RED deberá demostrar al menos:

```text
R01  required artifacts absent → RED
R02  unknown top-level case-set field rejected
R03  case/input unknown/missing/wrong-type field rejected
R04  duplicate/missing/extra case rejected
R05  duplicate/missing/extra input rejected
R06  unsupported schema version rejected
R07  ground-truth digest mismatch blocks PASS
R08  reviewer == runner implementation actor blocks PASS
R09  reviewer == assessor mechanism blocks PASS
R10  artifact unknown/missing field rejected
R11  case-set digest mismatch blocks PASS
R12  input digest mismatch blocks PASS
R13  subject fingerprint mismatch blocks PASS
R14  model-based artifact without complete provenance blocks PASS
R15  mechanism producer == assessor subject cannot self-certify
R16  exact support input can PASS
R17  irrelevant/insufficient support cannot be promoted to SUPPORTED
R18  compound partial support remains INCONCLUSIVE
R19  unresolved counterevidence cannot become SUPPORTED
R20  C05 contains resolved limiting material
R21  C11 prior subject binding is recomputable and stale
R22  C12 prior evidence-material binding is recomputable and stale
R23  C13 requires two bound observations
R24  C13 comparison uses observed outcome/reasons, not fingerprint equality
R25  malformed/unavailable assessor remains non-positive
R26  all metric formulas match frozen input-level denominators/numerators
R27  any safety-floor violation prevents terminal PASS
R28  authority_effect other than none rejected
R29  runner performs no model/network/repo-write side effects
R30  no case/input skip/filter/xfail path exists
R31  PASS requires all 18 cases / 19 inputs valid and evaluable
```

Nueva matrix:

```text
R01-R31
```

## 26. Invalidación de PR #230

Candidate anterior de #230:

`655bde3a16e8d20047d6ee3286c6a4ff89a57294`

queda preservado como evidencia histórica de:

- RED causal del contrato v0;
- GREEN mecánico del contrato v0;
- finding descubierto por Candidate FULL 4R.

No puede convertirse en candidate conforme a V0.1.

Después de mergear esta corrección:

```text
PR #230 must rebase/update to corrected main
cases.json must become v0.1
tests must implement R01-R31
runner must implement v0.1
new RED required
new GREEN required
new Candidate FULL 4R required
new affected independent validation required
new RDD Stage 1 Candidate Conformance required
```

## 27. Cuatro preguntas de ley — affected revalidation

### Blueprint

**PASS**

La corrección permanece en evaluation tooling offline; Kernel/runtime delta 0.

### Cognitive Constitution

**PASS**

Evita que una etiqueta o un fingerprint sustituyan evidencia material del
comportamiento observado.

### Governance Constitution

**PASS**

No crea permiso ni decisión automática. `authority_effect = none`.

### Kernel simplicity

**PASS**

```text
Kernel delta = 0
runtime delta = 0
```

## 28. Design 4R — affected revalidation

### Risk — PASS

Corrige el riesgo de declarar stability/binding assurance con evidencia
insuficiente.

No introduce nueva autoridad.

### Readability — PASS

La unidad reproducible queda explícita:

```text
case
  → input(s)
  → observation(s)
  → comparison
  → case result
  → metrics
  → qualification result
```

### Reliability — PASS

C05/C11/C12/C13 ya no dependen exclusivamente de labels.

Cada propiedad material tiene inputs/digests/observations reproducibles.

### Resilience — PASS

Ausencia o mismatch de input, prior binding u observation:

```text
→ no PASS
```

```text
Affected Design 4R = PASS
```

## 29. RDD Stage 1 Design Check — affected revalidation

```text
baseline exact                            PASS
trigger candidate exact                   PASS
finding/evidence binding                  PASS
scope bounded                             PASS
schema version changed explicitly         PASS
prior evidence preserved                  PASS
candidate invalidation                    PASS
input identity strategy                   PASS
comparison identity strategy              PASS
PASS/FAIL/INCONCLUSIVE discipline         PASS
authority_effect                          none
overall                                   PASS
```

Esto NO es Candidate Conformance.

## 30. Independent validation

La External Audit R2 sobre #229 sigue siendo evidencia histórica válida del
contract candidate que auditó.

No puede reutilizarse como auditoría independiente suficiente de V0.1.

Antes de autorizar un nuevo RED, affected independent review del contract
corregido es requerida si se mantiene el mismo nivel de assurance usado para
#229.

## 31. Gate result

```text
correction round                       1/2
bounded correction design              PASS
affected four law questions            PASS
affected Design 4R                     PASS
affected RDD Stage 1 Design Check      PASS
authority_effect                       none

RED                                     NOT AUTHORIZED
GREEN                                   NOT AUTHORIZED
implementation                          NOT AUTHORIZED
Ready/Merge                             Owner only
```

Siguiente secuencia:

```text
candidate validation
→ independent affected review
→ human review
→ Owner merge
→ post-merge validation
→ new explicit RED authorization
```
