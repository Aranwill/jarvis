---
title: Malāk E2 Structural Evidence Evaluation Pack V0 — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation design
language: es
created: 2026-09-20
baseline_commit: 5c942d27ea610873182ded77b85d0364bfbe15a0
g0_result: pass
design_authorized_by: owner
design_authorized_at: 2026-09-20
red_authorized: false
implementation_authorized: false
risk_class: 2
---

# E2 Structural Evidence Evaluation Pack V0 — G0/G1 Design

## 1. Propósito

Medir de forma reproducible qué cambia en `Engineering Inspect (E2)` cuando la
misma solicitud recibe o no evidencia estructural `[S#]`.

V0 evalúa comportamiento observable del sistema. No evalúa calidad general del
modelo ni autoriza cambios arquitectónicos.

## 2. G0

```text
baseline: 5c942d27ea610873182ded77b85d0364bfbe15a0
tracked files: 271/271 classified
silently omitted: 0
tree truncated: false
G0 RESULT: PASS
```

No existe harness específico para E2. La Cognitive Dataset Foundation ya exige
evaluación antes de entrenamiento o expansión de complejidad.

```text
Evaluation Pack V0       ADMIT
new runtime capability   REJECT
persistent telemetry     REJECT
model-quality benchmark  DEFER
E3/E4 propagation        DEFER
Structural Delta         DEFER
```

## 3. Contrato A/B

Cada caso usa el mismo commit, fixture, subject, provider policy y configuración.

```text
A: structural_projection = None
   → R + K

B: structural_projection = projection(same baseline)
   → R + K + S
```

Única diferencia material permitida: disponibilidad de S.

```text
A baseline != B baseline
→ case_result = INVALID
→ pair is not executed
→ conformance_result = FAIL
```

## 4. Evaluation identity y schema cerrado

Cada ejecución debe quedar ligada a:

```text
malak_baseline_sha
case_set_schema_version
case_set_digest
runner_version
runner_digest
provider_policy_version
provider_policy_digest
```

Regla de invalidación:

```text
case-set changes
OR runner changes
OR provider-policy changes
→ evaluation identity changes
→ prior evaluation does not certify the new identity
```

Los digests V0 son SHA-256 sobre los bytes exactos del artefacto evaluado.
No se permite normalización implícita previa al hash.

El case-set V0 usa schema cerrado y fail-closed:

```text
unknown field       → STOP
missing field       → STOP
wrong type          → STOP
unknown enum        → STOP
duplicate case_id   → STOP
empty subject       → STOP
unsupported fixture → STOP
```

El dataset no puede contener código ejecutable, comandos, URLs, rutas arbitrarias
fuera del fixture contract ni instrucciones para ampliar permisos/scope.

Los enums admitidos deben ser cerrados por la implementación V0; ningún valor
desconocido se normaliza, ignora o interpreta por heurística.
## 5. Ground truth

El expected se define antes de ejecutar y no puede derivarse del output B.

Campos mínimos:

```text
case_id
subject
fixture_profile
comparison_class
expected_a_status
expected_b_status
expected_structural_facts
expected_total_structural_count
expected_emitted_structural_count
expected_context_truncated
ground_truth_source
ground_truth_review_status
```

Los facts esperados usan identidad sintáctica explícita:

```text
fact_type
module_name / source_module
qualified_name / target_module
imported_name
kind
relative_level
```

`baseline_commit` y `blob_sha` validan binding; no son oráculo manual.

El ground truth debe tener provenance explícita y revisión separada de la
implementación del runner. Si fue generado por un agente/modelo, no puede
auto-validarse.

```text
ground truth no revisado
OR ground truth reviewer == runner implementation actor
→ INCONCLUSIVE
→ evaluation NOT EXECUTABLE
```

La revisión de ground truth produce evidencia; no concede autoridad sobre Malāk.

Para structural facts, la comparación V0 es una secuencia ordenada exacta.
Orden, multiplicidad y campos materiales deben coincidir; set-equivalence no es
suficiente. En truncation deben distinguirse explícitamente total descubierto y
total emitido.

## 6. Casos V0

| Caso | Subject / fixture | A | B | Expected S |
| --- | --- | --- | --- | --- |
| C1 exact symbol | `malak.component.NeedleComponent1` | UNCONFIRMED | GROUNDED | exact symbol |
| C2 exact module | `malak.component` | UNCONFIRMED | GROUNDED | symbols + imports |
| C3 substring | `NeedleComponent` | exact observed non-S fields | same exact non-S fields | 0 |
| C4 textual/knowledge | `needle` | exact R/K observed fields | same exact R/K fields | 0 |
| C5 absent | `absent-evaluation-token` | UNCONFIRMED | UNCONFIRMED | 0 |
| C6 truncation | >12 structural facts | structural count 0 | GROUNDED | exact total >12; emitted=12; truncated=true |

Sólo se añaden casos si representan una clase nueva de comportamiento.

## 7. Métricas

No existe score compuesto.

| Métrica | Semántica | Objetivo |
| --- | --- | --- |
| `structural_coverage_gain_count` | ground truth espera S, A=UNCONFIRMED, B=GROUNDED | observar |
| `unexpected_structural_activation_count` | expected S=0 pero B produce S>0 | 0 |
| `structural_fact_mismatch_count` | facts B != expected manual | 0 |
| `non_structural_regression_count` | expected S=0 y A/B difieren inesperadamente | 0 |
| `invalid_paired_baseline_count` | baseline A/B distinto | 0 |

Para `non_structural_regression_count` se comparan:

```text
status
repository_evidence_count
knowledge_evidence_count
context_truncated
```

`structural_coverage_gain_count` mide cobertura, no calidad.

## 8. Límites

```text
A: UNCONFIRMED
B: GROUNDED
```

no implica:

```text
B is correct
B reasoned better
S improves answer quality
S should propagate to E3/E4
```

`GROUNDED` sólo indica que E2 recorrió su path grounded con evidencia admisible.

## 9. Anti-autoengaño

1. expected definido antes de ejecutar;
2. expected no derivado del projector/lookup bajo prueba;
3. resultados visibles por caso;
4. no esconder fallos en promedios;
5. coverage != quality;
6. citation count != correctness;
7. incluir casos positivos y negativos;
8. mismo baseline A/B;
9. no seleccionar sólo casos favorables a S;
10. evaluation evidence carries zero authority;
11. todos los casos declarados son obligatorios;
12. skip / xfail / filtering / case selection están prohibidos en V0;
13. un fallo individual permanece visible aunque los agregados parezcan favorables.

## 10. Provider de evaluación

V0 usa un provider determinista de test con política fija para recorrer E2 de
forma reproducible.

```text
provider output
!= model benchmark
!= answer quality evidence
```

Un benchmark con modelos reales requiere gate separado.

## 11. Estructura futura admitida

```text
evaluations/e2_structural_evidence_v0/cases.json
scripts/evaluate_e2_structural_evidence.py
tests/test_e2_structural_evidence_evaluation.py
```

Reglas:

- JSON / stdlib;
- runner read-only respecto del working tree y repos oficiales;
- fixtures sólo en directorio temporal aislado;
- output a stdout;
- sin network;
- sin DB/cache;
- sin commits/branches/PRs;
- sin modificación de repos oficiales;
- sin persistencia por defecto;
- no skip / xfail / filtering de casos.

## 12. Output candidato

```text
baseline_commit
case_count
case_results[]
structural_coverage_gain_count
unexpected_structural_activation_count
structural_fact_mismatch_count
non_structural_regression_count
invalid_paired_baseline_count
conformance_result
utility_observation
```

`conformance_result: PASS` significa únicamente conformance del pack.

`utility_observation` reporta observaciones como coverage gain y nunca participa
en PASS/FAIL. Un pack puede ser conforme y demostrar utilidad nula.

```text
conformance PASS != usefulness
usefulness observed != architecture approval
```

Cada `case_results[]` debe exponer al menos:

```text
case_id
case_result: PASS | FAIL | INVALID
expected
observed_a
observed_b
mismatches[]
```

Un caso `INVALID` no puede convertirse en PASS por agregación.

## 13. Scope futuro

RED futuro:

```text
tests/test_e2_structural_evidence_evaluation.py
```

GREEN futuro:

```text
evaluations/e2_structural_evidence_v0/cases.json
scripts/evaluate_e2_structural_evidence.py
```

Fuera de alcance:

```text
src/malak/**
EngineeringInspectCapability
composition.py
E3/E4
Kernel
Planner
Knowledge
Security
provider registry
```

## 14. Relación con trabajo actual

```text
Observability V0
→ qué ocurrió

Evaluation Pack V0
→ qué diferencia reproducible produjo S contra ground truth
```

Reutiliza counts R/K/S, citation counts, `model_inference_count` y
`context_truncated`, sin añadir señales al runtime.

Cognitive Dataset Foundation aporta:

```text
evaluation before training
benchmark before adaptation
identify real weaknesses before adding complexity
```

Este pack no es training dataset, hidden eval global ni benchmark de modelos.

## 15. Governance

```text
runtime delta           0
authority delta         0
new capability          0
persistent state        0
Kernel delta            0
Planner delta           0
E3/E4 delta             0
dataset created         0
harness created         0
model benchmark         0
Human in Control        unchanged
```

## 16. Gate de salida

El futuro pack sólo puede considerarse conforme si:

```text
paired baseline integrity      PASS
unexpected S activation        0
structural fact mismatches     0
non-structural regressions     0
case-level evidence            preserved
```

Incluso entonces, E3/E4 requieren gate separado.

## 17. Hardening G1 y controles separados

El contrato fue endurecido antes de RED contra:

```text
alternate material interpretation
adversarial interpretation
fail-open behavior
schema ambiguity
identity drift
silent skip/bypass
authority confusion
side-effect expansion
metric/utility conflation
```

Cuatro preguntas de ley:

```text
Blueprint                         PASS
Cognitive Constitution           PASS
Governance Constitution          PASS
Kernel complexity delta          0 / PASS
```

FULL 4R debe ejecutarse y registrarse por separado sobre el candidato material.
Las preguntas de ley no sustituyen FULL 4R.

## 18. Estado

```text
G0        PASS
G1        ADMITTED
RED       NOT AUTHORIZED
GREEN     NOT AUTHORIZED
```

El próximo gate, si el Owner lo autoriza, es RED y sólo RED.
