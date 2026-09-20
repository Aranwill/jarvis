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

Crear una evaluación reproducible y acotada para medir qué cambia en
`Engineering Inspect (E2)` cuando la misma solicitud recibe o no evidencia
estructural `[S#]`.

V0 evalúa comportamiento observable del sistema. No evalúa razonamiento general
del modelo ni autoriza cambios de arquitectura.

## 2. G0

```text
baseline: 5c942d27ea610873182ded77b85d0364bfbe15a0
tracked files discovered: 271
tracked files classified: 271
silently omitted files: 0
tree truncated: false
G0 RESULT: PASS
```

No existe hoy un harness específico para `engineering_inspect`. Sí existe una
fundación conceptual que exige evaluación antes de entrenamiento o expansión de
complejidad.

## 3. Decisión de admisión

```text
E2 Structural Evidence Evaluation Pack V0  ADMIT
new runtime capability                    REJECT
new model abstraction                     REJECT
persistent telemetry                      REJECT
training dataset                           NOT THIS V0
model-quality benchmark                    DEFER
E3/E4 propagation                          DEFER
Structural Delta                           DEFER
```

## 4. Diseño A/B

Cada caso se ejecuta sobre el mismo snapshot y el mismo subject.

```text
A
repository_reader
knowledge_reader
structural_projection = None
→ R + K

B
same repository_reader baseline
same knowledge baseline
structural_projection = projection(same baseline)
→ R + K + S
```

Invariantes:

1. mismo commit;
2. mismo fixture;
3. mismo subject;
4. misma política del provider de evaluación;
5. misma configuración E2;
6. única diferencia material permitida: disponibilidad de S.

Si A y B no comparten baseline exacto:

```text
STOP / INVALID CASE
```

## 5. Ground truth

El expected outcome se define antes de ejecutar el sistema bajo prueba.

No se permite derivar el expected desde el output observado de B.

Cada caso deberá declarar al menos:

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

Los structural facts esperados se describen mediante identidad semántica de
sintaxis, por ejemplo:

```text
fact_type
module_name / source_module
qualified_name / target_module
imported_name
kind
relative_level
```

`blob_sha` y `baseline_commit` se validan como binding del snapshot, no como
oráculo manual.

## 6. Casos mínimos V0

### C1 — exact symbol, structural-only

```text
subject: malak.component.NeedleComponent1
A: UNCONFIRMED
B: GROUNDED
expected S: exact symbol
```

### C2 — exact module, symbols + imports

```text
subject: malak.component
A: UNCONFIRMED
B: GROUNDED
expected S: module symbols + imports
```

### C3 — substring does not activate structural lookup

```text
subject: NeedleComponent
expected S: 0
A/B: non-structural behavior must remain compatible
```

### C4 — textual/knowledge evidence without structural match

```text
subject: needle
expected S: 0
A/B: status and R/K evidence behavior must remain compatible
```

### C5 — absent subject

```text
subject: absent-evaluation-token
A: UNCONFIRMED
B: UNCONFIRMED
expected S: 0
```

### C6 — structural truncation

```text
fixture: >12 structural facts in one module
B structural_evidence_count: 12
B context_truncated: true
A remains without S
```

V0 puede añadir casos sólo si representan una clase nueva de comportamiento, no
variaciones cosméticas.

## 7. Métricas V0

No se crea score compuesto.

### Structural coverage gain count

Número de casos donde:

```text
ground truth expects structural evidence
AND
A == UNCONFIRMED
AND
B == GROUNDED
```

Esto mide cobertura del sistema, no calidad de respuesta.

### Unexpected structural activation count

Número de casos donde ground truth espera `S=0` y B produce `S>0`.

Objetivo contractual:

```text
0
```

### Structural fact mismatch count

Número de casos donde los structural facts observados en B no coinciden con el
expected manual.

Objetivo contractual:

```text
0
```

### Non-structural regression count

En casos con `expected S=0`, diferencias inesperadas A/B en:

```text
status
repository_evidence_count
knowledge_evidence_count
context_truncated
```

Objetivo contractual:

```text
0
```

### Invalid paired baseline count

A/B con baseline distinto.

Objetivo contractual:

```text
0
```

## 8. Lo que V0 no puede afirmar

Incluso si:

```text
A: UNCONFIRMED
B: GROUNDED
```

no se puede concluir:

```text
B is correct
B reasoned better
S improves answer quality
S should propagate to E3/E4
```

`GROUNDED` sólo indica que hubo evidencia admisible suficiente para ejecutar el
path grounded de E2.

## 9. Anti-autoengaño

1. expected definido antes de la ejecución;
2. expected no derivado del projector/lookup bajo prueba;
3. resultados por caso siempre visibles;
4. no ocultar fallos detrás de un promedio;
5. no convertir coverage en quality;
6. no usar citation count como correctness;
7. no seleccionar sólo casos favorables a S;
8. incluir casos negativos y sin match;
9. mismo baseline A/B;
10. evaluación no concede autoridad.

## 10. Provider de evaluación

V0 no evalúa un LLM real.

El futuro harness deberá usar un provider determinista de test con una política
fija y reproducible. Su función será permitir recorrer E2 y observar contracts,
no simular inteligencia.

Por lo tanto:

```text
provider output
!= model benchmark
!= answer quality evidence
```

Un benchmark con modelos reales será un gate separado.

## 11. Estructura candidata futura

Sin implementación autorizada, G1 admite como forma mínima:

```text
evaluations/
  e2_structural_evidence_v0/
    cases.json

scripts/
  evaluate_e2_structural_evidence.py

tests/
  test_e2_structural_evidence_evaluation.py
```

Preferencias:

- JSON para casos: stdlib, sin dependencia nueva;
- runner read-only;
- output a stdout;
- no DB;
- no cache;
- no red;
- no persistencia por defecto.

## 12. Output candidato del runner

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

`conclusion` puede ser `pass` sólo por conformance del pack. No constituye
aprobación arquitectónica.

## 13. Scope futuro admitido

RED futuro:

```text
tests/test_e2_structural_evidence_evaluation.py
```

GREEN futuro, si se autoriza:

```text
evaluations/e2_structural_evidence_v0/cases.json
scripts/evaluate_e2_structural_evidence.py
```

No se modifica:

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

## 14. Relación con Observability V0

```text
Observability V0
→ expone qué ocurrió en una ejecución

Evaluation Pack V0
→ compara ejecuciones emparejadas contra ground truth
```

El pack reutiliza:

```text
R/K/S evidence counts
R/K/S citation counts
model_inference_count
context_truncated
```

sin añadir señales al runtime.

## 15. Relación con Cognitive Dataset Foundation

Este incremento adopta:

```text
evaluation before training
benchmark before adaptation
identify real weaknesses before adding complexity
```

Pero este pack no es todavía:

- dataset cognitivo de entrenamiento;
- hidden evaluation global;
- benchmark de modelos candidatos;
- mecanismo de continual learning.

## 16. Governance / Security

```text
runtime authority          0
new capability             0
persistent state           0
new model calls in runtime 0
Kernel delta               0
Planner delta              0
E3/E4 delta                0
Human in Control           unchanged
```

Evaluation evidence carries zero authority.

## 17. Gate de salida de V0

Un resultado futuro del pack sólo podrá habilitar una nueva discusión si:

```text
paired baseline integrity      PASS
unexpected S activation        0
structural fact mismatches     0
non-structural regressions     0
case-level evidence            preserved
```

Aun cumpliéndose, la propagación a E3/E4 seguirá requiriendo un gate separado.

## 18. Estado

```text
G0                    PASS
G1 design             ADMITTED
RED                   NOT AUTHORIZED
GREEN                 NOT AUTHORIZED

runtime delta         0
authority delta       0
dataset created       0
harness created       0
model benchmark       0
```

El próximo gate, si el Owner lo autoriza, es RED y sólo RED.
