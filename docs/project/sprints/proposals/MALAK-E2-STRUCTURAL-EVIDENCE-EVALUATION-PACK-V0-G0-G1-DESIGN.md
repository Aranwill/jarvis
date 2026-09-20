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
→ STOP / INVALID CASE
```

## 4. Ground truth

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
expected_structural_count
expected_context_truncated
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

## 5. Casos V0

| Caso | Subject / fixture | A | B | Expected S |
| --- | --- | --- | --- | --- |
| C1 exact symbol | `malak.component.NeedleComponent1` | UNCONFIRMED | GROUNDED | exact symbol |
| C2 exact module | `malak.component` | UNCONFIRMED | GROUNDED | symbols + imports |
| C3 substring | `NeedleComponent` | compatible non-S | compatible non-S | 0 |
| C4 textual/knowledge | `needle` | compatible R/K | compatible R/K | 0 |
| C5 absent | `absent-evaluation-token` | UNCONFIRMED | UNCONFIRMED | 0 |
| C6 truncation | >12 structural facts | no S | GROUNDED | 12 + truncated |

Sólo se añaden casos si representan una clase nueva de comportamiento.

## 6. Métricas

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

## 7. Límites

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

## 8. Anti-autoengaño

1. expected definido antes de ejecutar;
2. expected no derivado del projector/lookup bajo prueba;
3. resultados visibles por caso;
4. no esconder fallos en promedios;
5. coverage != quality;
6. citation count != correctness;
7. incluir casos positivos y negativos;
8. mismo baseline A/B;
9. no seleccionar sólo casos favorables a S;
10. evaluation evidence carries zero authority.

## 9. Provider de evaluación

V0 usa un provider determinista de test con política fija para recorrer E2 de
forma reproducible.

```text
provider output
!= model benchmark
!= answer quality evidence
```

Un benchmark con modelos reales requiere gate separado.

## 10. Estructura futura admitida

```text
evaluations/e2_structural_evidence_v0/cases.json
scripts/evaluate_e2_structural_evidence.py
tests/test_e2_structural_evidence_evaluation.py
```

Reglas:

- JSON / stdlib;
- runner read-only;
- output a stdout;
- sin DB/cache/red;
- sin persistencia por defecto.

## 11. Output candidato

```text
baseline_commit
case_count
case_results[]
structural_coverage_gain_count
unexpected_structural_activation_count
structural_fact_mismatch_count
non_structural_regression_count
invalid_paired_baseline_count
conclusion
```

`conclusion: pass` significa conformance del pack, no aprobación arquitectónica.

## 12. Scope futuro

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

## 13. Relación con trabajo actual

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

## 14. Governance

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

## 15. Gate de salida

El futuro pack sólo puede considerarse conforme si:

```text
paired baseline integrity      PASS
unexpected S activation        0
structural fact mismatches     0
non-structural regressions     0
case-level evidence            preserved
```

Incluso entonces, E3/E4 requieren gate separado.

## 16. Estado

```text
G0        PASS
G1        ADMITTED
RED       NOT AUTHORIZED
GREEN     NOT AUTHORIZED
```

El próximo gate, si el Owner lo autoriza, es RED y sólo RED.
