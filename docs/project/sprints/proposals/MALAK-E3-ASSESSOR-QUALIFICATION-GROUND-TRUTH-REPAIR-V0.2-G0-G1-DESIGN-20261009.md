---
title: Malāk E3 Assessor Qualification Ground-Truth Repair V0.2 — G0/G1 Design
status: design_candidate
authority: non_normative
language: es
as_of_date: 2026-10-09
baseline_commit: 0ae7886072b58c292f099b4c764ffd3386489d7b
baseline_tree: 4f6ac23c2d852615253df4d2b71f3835abdeac49
work_unit: E3 Assessor Qualification Ground-Truth Repair V0.2
risk_class: 3
critical_contract: true
runtime_delta: 0
kernel_delta: 0
authority_effect: none
rdd_stage_2_authorized: false
---

# E3 Assessor Qualification Ground-Truth Repair V0.2 — G0/G1 Design

## 1. Trigger y disposición inmediata

Esta unidad nace por una falla del **ground truth**, no por una falla demostrada del assessor.

El corpus vigente está ligado a los bytes exactos de:

`evaluations/e3_governed_evidence_support_assessor_v0/cases.json`

con digest:

`23e045b5e5aede8341323c486e77893d7161899f0c20870703efff28789f3f83`.

Una revisión independiente externa, declarada como:

`E3-ASSQ-GROUND-TRUTH-REVIEWER-A-20261009`

revisó exactamente ese digest, mantuvo separación respecto de `assessor_results.json`, y terminó:

```text
ground-truth review = FAIL
authority_effect     = none
```

El finding material principal es que existen labels/expected outcomes cuya evidencia visible no materializa suficientemente el escenario o el soporte que afirman representar. C13 es el ejemplo crítico: equivalencia por permutación está materializada, pero los textos genéricos A/B no demuestran por sí solos soporte material para la afirmación evaluada.

Por lo tanto:

```text
ground truth FAIL
→ Qualification Pack execution BLOCKED para ese corpus
→ assessor semantic qualification UNKNOWN
→ no score ni PASS/FAIL del assessor puede derivarse de ese oracle
```

La ejecución live previa permanece evidencia histórica de ejecución y publicación, no evidencia válida de qualification contra un corpus reparado.

## 2. Construction Preflight

### P0 — Identidad exacta

```text
repository             Aranwill/jarvis
baseline               0ae7886072b58c292f099b4c764ffd3386489d7b
baseline tree          4f6ac23c2d852615253df4d2b71f3835abdeac49
branch permanente      main
work unit              E3 Assessor Qualification Ground-Truth Repair V0.2
work type              PR-A / G0-G1 Design
owner instruction      avanzar reparación del ground truth
last stable checkpoint main@0ae7886072b58c292f099b4c764ffd3386489d7b
```

P0 = PASS.

### P1 — Fuentes reconciliadas

Fuentes normativas/protegidas y de proceso aplicables:

- `AGENTS.md`;
- `docs/governance/cognitive_constitution.md`;
- `docs/governance/governance_constitution.md`;
- `docs/architecture/blueprint.md`;
- `docs/architecture/kernel.md`;
- `docs/architecture/architecture_quality_gates.md`;
- `SECURITY.md`;
- ADR-003 y ADR-004;
- `docs/development/engineering_method.md`;
- `docs/development/malak_construction_protocol.md`;
- `docs/development/malak_construction_preflight.md`;
- `docs/development/development_checklist.md`;
- `docs/development/evidence_manifest.md`.

Fuentes CURRENT y contractuales directas:

- `docs/project/project_context.md`;
- `docs/project/implementation_roadmap.md`;
- Assessor Qualification Pack G0/G1 Admission;
- Pre-RED Contract Hardening;
- Bounded Contract Correction V0.1;
- Blind Assessor Experiment Harness Design;
- Case-set Byte Stability Design Amendment;
- Governed Local Ollama Assessor Experiment Design;
- `cases.json`;
- `experiment_profile.json`;
- qualification runner y tests afectados.

La cobertura recursiva del baseline detectó:

```text
tracked blobs discovered = 379
tracked blobs classified = 379
silently omitted files   = 0
recursive tree truncated = false
```

El detalle vive en el File Coverage Ledger de esta PR-A.

P1 = PASS.

### P2 — Invariantes

```text
Human in Control                         PASS
Kernel First                             PASS / Kernel delta 0
Capability First                         N/A / no Capability nueva
Runtime Independence                     PASS / runtime delta 0
separation of responsibilities           PASS
Zero Trust                               PASS
result/evidence != authority             PASS
semantic label != semantic proof         PASS
no hidden authority elevation            PASS
```

P2 = PASS.

### P3 — Dirección de autoridad

```text
Owner
  ↓
approved construction scope
  ↓
ground-truth repair candidate
  ↓
independent blind ground-truth review
  ↑
Evidence / findings only
  ↑
candidate
```

Verificaciones:

```text
upward control path              NONE
authority self-elevation         NONE
assessor result as oracle input  FORBIDDEN
ground-truth reviewer authority  NONE
support_sufficient write         NONE
RDD Stage 2                      NOT AUTHORIZED
```

P3 = PASS.

### P4 — Reuse / necesidad / complejidad

Disposición:

```text
existing Qualification Pack       REUSE
existing case-set schema v0.1     ADAPT CONTENT
existing blind harness            REUSE
existing byte-binding semantics   REUSE
existing Qualification runner     REUSE unless a new material defect proves otherwise
new scorer/framework              REJECT
new runtime/provider              REJECT
new Capability/service/manager    REJECT
```

No existe necesidad de un subsistema nuevo. El gap está en la calidad semántica del corpus de evaluación.

P4 = PASS.

### P5 — Riesgo

```text
risk_class                    3
risk_rationale                ground truth controls qualification semantics;
                              false oracle can generate false PASS/FAIL
critical_contract             YES
Design 4R                     REQUIRED
Candidate FULL 4R             REQUIRED for future PR-B
RDD Stage 1                   REQUIRED
independent design review     REQUIRED
independent ground-truth review REQUIRED before qualification
```

P5 = PASS.

### P6 — Scope freeze

Esta PR-A modifica únicamente:

```text
docs/project/sprints/proposals/MALAK-E3-ASSESSOR-QUALIFICATION-GROUND-TRUTH-REPAIR-V0.2-G0-G1-DESIGN-20261009.md
docs/project/sprints/proposals/MALAK-E3-ASSESSOR-QUALIFICATION-GROUND-TRUTH-REPAIR-V0.2-G0-G1-FILE-COVERAGE-20261009.tsv
```

Hard-zero PR-A:

```text
evaluations/**
scripts/**
tests/**
src/malak/**
configs/**
.gitattributes
.github/**
Constitutions
Blueprint
Kernel
accepted ADRs
SECURITY.md
CURRENT_STATE docs
```

P6 = PASS.

### P7 — Resultado

```text
Construction Preflight = PASS
implementation          = NOT AUTHORIZED BY THIS PR-A
authority_effect        = none
```

## 3. Principios no negociables del repair

```text
scenario label        != scenario evidence
expected outcome      != proof of expected outcome
contract validity     != semantic validity
equivalence           != material support
digest equality       != semantic correctness
model agreement       != ground-truth correctness
Qualification PASS    != production authorization
Evidence              != Authority
```

El repair no puede modificar el corpus para hacerlo coincidir con respuestas previas de un modelo.

## 4. Blindness y anti-contaminación

Durante el repair y su revisión:

- no leer `assessor_results.json` de ejecuciones live previas;
- no leer outputs por caso de `qwen3.5:9b` ni de otro assessor candidate;
- no usar métricas/resultados previos para decidir labels;
- no seleccionar evidence material con el objetivo de convertir un resultado previo en PASS;
- sí se puede conservar como hecho histórico que una ejecución completó el harness, sin exponer sus disposiciones semánticas.

```text
repair ground truth
must be independent of
candidate answers
```

Si un actor de repair accede a las respuestas del assessor bajo evaluación:

```text
ground-truth independence compromised
→ STOP
→ fresh repair/review actor required
```

## 5. Obligaciones semánticas por caso

El futuro corpus conserva 18 cases / 19 inputs salvo que un nuevo finding de Design obligue a re-admisión.

### C01 — EXACT_SUPPORT

Debe materializar soporte directo, explícito y suficiente para la afirmación visible.

### C02 — IRRELEVANT_SUPPORT

Debe incluir evidence material real y visible que sea genuinamente irrelevante para la afirmación; la irrelevancia no puede existir sólo en el nombre del case.

### C03 — INSUFFICIENT_SUPPORT

Debe materializar soporte parcial o insuficiente de manera observable. La insuficiencia debe derivarse del packet, no del label.

### C04 — COMPOUND_PARTIAL_SUPPORT

La afirmación debe contener más de una cláusula material y el packet debe soportar sólo una parte, de modo que el expected non-positive outcome sea defendible.

### C05 — COMPATIBLE_LIMITING_EVIDENCE

Debe existir limiting evidence visible y compatible con la afirmación, sin convertirlo artificialmente en contradicción.

### C06 — UNRESOLVED_COUNTEREVIDENCE

Debe materializar counterevidence concreto y material que permanezca no resuelto dentro del bounded packet.

### C07 — AUTHORITY_SEMANTIC_MISMATCH

Debe existir una fuente de autoridad/normativa cuyo contenido sea realmente semánticamente irrelevante para la afirmación evaluada.

### C08 — LOW_AUTHORITY_RELEVANT_SUPPORT

Debe existir material contextual de menor autoridad pero semánticamente relevante que soporte de manera defendible la afirmación acotada.

### C09 — RATIONALE_OVERCLAIM

El exceso del rationale debe ser visible y concreto respecto del material suministrado. No basta declarar que “overclaims”.

### C10 — MISSING_EVIDENCE_MATERIAL

Debe preservar de forma explícita la ausencia de material y la excepción contractual correspondiente, sin que el runner rellene el faltante.

### C11 — STATEMENT_BINDING_DRIFT

Prior/current subject deben ser distintos de forma material y el binding previo debe ser recomputable desde el corpus bajo la canonicalización vigente.

### C12 — EVIDENCE_MATERIAL_BINDING_DRIFT

Prior/current evidence material deben diferir materialmente y el digest previo debe ser recomputable de forma determinista desde el corpus.

### C13 — EQUIVALENT_INPUT_PERMUTATION

Debe mantener exactamente dos inputs con:

```text
input_instance_digest I01 != I02
semantic_input_digest I01 == I02
```

La única diferencia admitida es la permutación no semántica. Además, el evidence material de ambos inputs debe **soportar realmente** la afirmación visible. La equivalencia entre inputs no sustituye esta obligación.

### C14 — ASSESSOR_UNAVAILABLE

El scenario fault debe estar materializado por el execution profile/harness de manera reproducible. El input semántico no debe pretender demostrar por sí solo la indisponibilidad.

### C15 — MALFORMED_ASSESSOR_OUTPUT

El fault injection debe producir de manera reproducible un output inválido bajo el contrato, sin usar un label como sustituto de la falla.

### C16 — HIGH_CONFIDENCE_UNSUPPORTED

La afirmación/rationale y el packet deben hacer observable que confianza declarada no sustituye soporte material. El expected negative outcome debe derivarse del material, no de una etiqueta invisible.

### C17 — SELF_CERTIFICATION

La identidad de producer/assessor y su conflicto deben estar explícitamente materializados y ser suficientes para justificar el resultado no positivo según el contrato vigente.

### C18 — SCOPE_EXPANSION_REQUIRED

El bounded packet debe hacer observable que la afirmación requiere evidencia específica fuera del scope y que esa evidencia no está disponible dentro del packet. La mera frase “scope expansion required” no basta.

## 6. Future PR-B — scope candidato

Sólo después de:

1. CI candidate-bound de esta PR-A;
2. Independent Design Review PASS;
3. revisión humana;
4. Owner Ready/Merge;
5. post-merge reconciliation;
6. instrucción separada del Owner para PR-B.

ALLOW candidato inicial:

```text
evaluations/e3_governed_evidence_support_assessor_v0/cases.json
evaluations/e3_governed_evidence_support_assessor_v0/experiment_profile.json
tests/test_e3_governed_blind_assessor_experiment.py
tests/test_e3_governed_blind_assessor_ollama_experiment.py
```

Hard-zero inicial:

```text
src/malak/**
scripts/evaluate_e3_governed_evidence_support_assessor.py
scripts/run_e3_governed_blind_assessor_experiment.py
scripts/run_e3_governed_blind_assessor_ollama_experiment.py
dependencies
Kernel
Planner
Capabilities
Security PDP/PEP
Conversation
support_sufficient
Protected Finalization
RDD Stage 2
```

Si el repair demuestra que el qualification runner o el harness requieren un cambio material:

```text
STOP
→ record finding
→ separate admission/scope review
→ no implicit expansion
```

## 7. Identity e invalidación

El corpus reparado tendrá bytes nuevos y, por tanto, un digest nuevo.

Debe actualizarse de forma exacta y consistente:

```text
cases.json raw bytes
→ SHA-256 lowercase
→ experiment_profile.expected_case_set_digest
→ harness tests
→ Ollama adapter tests
→ future assessor artifact.case_set_digest
→ Qualification Pack recomputation
```

El path-specific `.gitattributes` `text eol=lf` permanece sin cambios.

Todo artefacto ligado al digest viejo queda históricamente válido para su identidad original, pero **no comparable** con el nuevo corpus.

```text
old Run #3 result artifact
!= evidence for repaired corpus
```

## 8. RED causal futuro — requisitos mínimos

La futura PR-B debe materializar RED causal que demuestre, como mínimo:

```text
GTR-R01 old expected case-set digest rejected after corpus change
GTR-R02 new raw-byte digest bound exactly through profile/tests
GTR-R03 C02 materializes actual irrelevant evidence
GTR-R04 C03 materializes actual partial/insufficient evidence
GTR-R05 C04 materializes compound partial support
GTR-R06 C05 limiting evidence is visible and compatible
GTR-R07 C06 counterevidence is concrete and unresolved
GTR-R08 C07 authoritative material is semantically irrelevant
GTR-R09 C08 low-authority contextual material is semantically relevant
GTR-R10 C09 rationale overclaim is concretely observable
GTR-R11 C10 missing-material exception remains explicit
GTR-R12 C11 prior/current subject binding is recomputable
GTR-R13 C12 prior/current evidence-material binding is recomputable
GTR-R14 C13 has two distinct instances with one semantic identity
GTR-R15 C13 evidence materially supports the visible statement
GTR-R16 C14 fault injection is reproducible and candidate-hidden
GTR-R17 C15 malformed-output injection is reproducible
GTR-R18 C16 confidence-substitution claim lacks material support
GTR-R19 C17 self-certification identity conflict is explicit
GTR-R20 C18 missing out-of-scope dependency is concretely observable
GTR-R21 18 cases / 19 inputs remain exact
GTR-R22 ground-truth fields remain absent from blind assessor input
GTR-R23 repair tests do not inspect prior assessor_results
GTR-R24 Qualification Pack consumer remains unchanged
GTR-R25 authority_effect remains none
```

## 9. Independent ground-truth review obligatorio

Antes de permitir qualification sobre cualquier nuevo assessor result, un actor independiente debe revisar el nuevo `cases.json` exacto y su contrato aplicable.

Requisitos:

- reviewer distinto del repair writer cuando la independencia sea requerida por el gate;
- reviewer no accede a `assessor_results.json`;
- digest revisado = SHA-256 de bytes exactos;
- review semántica, no sólo schema;
- cada finding recibe disposición;
- terminal `PASS | FAIL | INCONCLUSIVE`;
- `authority_effect = none`.

Sólo `PASS` habilita el uso del nuevo ground truth por el Qualification Pack.

## 10. Correction Budget

Future PR-B:

```text
max bounded correction rounds = 2
```

Correcciones admisibles dentro del budget:

- case-set fixture;
- profile digest binding;
- tests directamente ligados al repair;
- documentación del candidate cuando sea necesaria para trazabilidad.

STOP inmediato si aparece necesidad de:

- cambiar `src/malak/**`;
- cambiar runtime/provider;
- añadir dependencia;
- cambiar autoridad;
- modificar law docs;
- introducir network;
- modificar qualification semantics fuera del repair admitido.

## 11. Security Horizon

```text
network                           0 en PR-A
model execution                   0 en PR-A
provider selection                0
secret handling                   N/A
ground-truth leakage to candidate FORBIDDEN
prior candidate answer leakage    FORBIDDEN
repo writes runtime               0
authority_effect                  none
```

La amenaza principal de esta unidad es **evaluation poisoning / circular oracle construction**. El control principal es separación estricta entre ground-truth repair y respuestas del assessor candidate.

## 12. Cuatro preguntas de ley

### Blueprint

PASS — evaluation tooling permanece fuera del Kernel y no introduce nuevo runtime.

### Cognitive Constitution

PASS — CC-002/003/011/012 exigen no convertir labels, outputs o confianza en evidencia suficiente o verdad.

### Governance Constitution

PASS — Evidence/Validation permanecen separadas de Decision/Authority; Owner conserva Ready/Merge.

### Kernel simplicity

PASS — Kernel delta = 0.

## 13. Design 4R — writer candidate

### Risk — PASS candidate

El diseño elimina el riesgo de evaluar un assessor contra un oracle semánticamente dudoso y prohíbe contaminación por respuestas previas.

### Readability — PASS candidate

Se separan explícitamente: scenario, evidence material, expected disposition, binding, fault injection, qualification y authority.

### Reliability — PASS candidate

La identidad sigue raw-byte bound; cualquier cambio de corpus invalida artifacts viejos y exige digest nuevo.

### Resilience — PASS candidate

FAIL/INCONCLUSIVE del ground-truth review bloquea qualification. No existe fallback por majority, label o modelo.

```text
Design 4R = WRITER PASS CANDIDATE
```

Requiere Independent Design Review antes de revisión humana.

## 14. RDD Stage 1 Design Check — writer candidate

```text
baseline exact                         PASS
scope frozen                           PASS
spec/trigger binding                   PASS
candidate identity strategy            PASS
risk class 3                           PASS
critical contract                      PASS
case-set identity invalidation         PASS
blindness / anti-contamination         PASS
future RED causal matrix               PASS
correction budget                      PASS
independent validation requirement     PASS
authority_effect                       none
overall                                WRITER PASS CANDIDATE
```

`RDD Stage 2 = NOT AUTHORIZED`.

## 15. Rollback

PR-A es docs-only.

Rollback:

```text
revert candidate commit
→ no runtime/code/case-set state affected
```

Future PR-B rollback deberá preservar el corpus viejo sólo como historial Git; no deberá reutilizar su qualification evidence como current.

## 16. Next lawful transition

```text
PR-A candidate-bound CI
→ Independent Design Review
→ Design 4R / RDD Stage 1 Design Check independent disposition
→ human review
→ Owner Ready / Merge
→ post-merge reconciliation
→ separate Owner authorization for PR-B
→ RED
→ GREEN
→ Candidate FULL 4R
→ independent ground-truth review on NEW digest
→ independent candidate validation
→ RDD Stage 1 Candidate Conformance
→ human review
→ Owner Ready / Merge
→ post-merge reconciliation
→ separately authorized new live model experiment
→ Qualification Pack
→ PASS | FAIL | INCONCLUSIVE
```

Nada en esta PR-A autoriza model promotion, `support_sufficient`, Protected Finalization, production admission o RDD Stage 2.
