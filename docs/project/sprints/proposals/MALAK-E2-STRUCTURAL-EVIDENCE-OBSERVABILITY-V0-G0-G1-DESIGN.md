---
title: Malāk E2 Structural Evidence Observability V0 — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation design
language: es
created: 2026-09-20
baseline_commit: 79319eef23cdd1490531d01de914712811135d9d
g0_result: pass
design_authorized_by: owner
design_authorized_at: 2026-09-20
red_authorized: false
implementation_authorized: false
risk_class: 2
---

# E2 Structural Evidence Observability V0 — G0/G1 Design

## 1. Propósito

Exponer señales deterministas y efímeras sobre la evidencia utilizada por
`Engineering Inspect (E2)`, sin crear telemetry runtime, storage, métricas
persistentes ni autoridad nueva.

La pregunta de V0 es limitada:

> ¿Qué evidencia estuvo disponible y qué referencias explícitas aparecen en la
> respuesta de E2?

V0 no intenta medir calidad, verdad, causalidad ni mejora cognitiva.

## 2. G0

```text
baseline: 79319eef23cdd1490531d01de914712811135d9d
tracked files discovered: 270
tracked files classified: 270
silently omitted files: 0
tree truncated: false
G0 RESULT: PASS
```

La responsabilidad puede vivir en la frontera existente de E2. No se justifica
un componente adicional.

## 3. Decisión de admisión

```text
E2 Structural Evidence Observability V0  ADMIT
new metrics component                    REJECT
persistent telemetry                     REJECT
E3 propagation                           DEFER
E4 propagation                           DEFER
Structural Delta                         DEFER
```

## 4. Fuente de las señales

E2 ya conoce durante una ejecución:

```text
repository_evidence
knowledge_evidence
structural_evidence
validated model response
context_truncated
whether inference occurred
```

Las nuevas señales deben derivarse únicamente de esos datos ya disponibles.

No se permite:

- nueva lectura de Git;
- nueva lectura de filesystem;
- nueva consulta a Structural Lookup;
- nueva llamada al modelo;
- network telemetry;
- persistencia.

## 5. Señales V0

### Evidencia disponible

```text
repository_evidence_count
knowledge_evidence_count
structural_evidence_count
```

`count > 0` significa sólo que esa clase de evidencia fue incluida en el
packet E2. No significa que el modelo la haya usado correctamente.

### Referencias explícitas observadas

Después de validar la respuesta del modelo:

```text
repository_citation_count
knowledge_citation_count
structural_citation_count
```

Cada count representa refs únicos válidos presentes explícitamente como
`[R#]`, `[K#]` o `[S#]`.

```text
citation
!= semantic use
!= causal contribution
!= correctness
!= quality
```

### Ejecución

```text
model_inference_count
context_truncated
```

En E2 V0:

```text
model_inference_count ∈ {0, 1}
```

`0` corresponde al camino sin evidencia que termina `UNCONFIRMED`.
`1` corresponde a una ejecución que invocó el provider una vez.

No se mide latencia en V0.

## 6. Output candidato

Las señales se exponen en el resultado textual existente de E2.

Ejemplo GROUNDED:

```text
repository_evidence_count: 2
knowledge_evidence_count: 1
structural_evidence_count: 3
repository_citation_count: 1
knowledge_citation_count: 0
structural_citation_count: 2
model_inference_count: 1
context_truncated: false
```

Ejemplo UNCONFIRMED:

```text
repository_evidence_count: 0
knowledge_evidence_count: 0
structural_evidence_count: 0
repository_citation_count: 0
knowledge_citation_count: 0
structural_citation_count: 0
model_inference_count: 0
context_truncated: false
```

No se crea schema persistente ni API nueva.

## 7. Derivación

```text
evidence_count
=
len(evidence collection)

citation_count
=
count(unique validated refs of class present in model output)

model_inference_count
=
0 before/no provider call
1 after exactly one provider call
```

Las citas desconocidas continúan produciendo STOP antes de renderizar un
resultado grounded.

## 8. Invariantes semánticos

1. Evidence availability != evidence usefulness.
2. Citation != semantic use.
3. Citation frequency != confidence.
4. Citation frequency != correctness.
5. Structural citation != semantic dependency.
6. Zero citations != evidence irrelevance.
7. Observability != evaluation.
8. Observability != authority.
9. Metrics cannot authorize propagation to E3/E4.
10. Metrics cannot prove quality improvement by themselves.

## 9. Scope admitido

GREEN futuro puede modificar únicamente:

```text
src/malak/capabilities/engineering_inspect.py
```

RED futuro:

```text
tests/test_engineering_inspect.py
```

Fuera de alcance:

```text
composition.py
_engineering_evidence.py
_engineering_analysis.py
engineering_analyze.py
engineering_propose.py
repository_reader.py
repository_structure.py
repository_structure_lookup.py
Kernel
Planner
CLI
Knowledge
Security
database
cache
event bus
telemetry exporter
metrics registry
receipt store
```

## 10. Compatibilidad

La integración no cambia:

- selección de evidencia;
- packet enviado al modelo;
- system prompt;
- número máximo de inferencias;
- validación de refs;
- límites de contexto;
- autoridad;
- comportamiento de E3/E4.

Sólo amplía la salida observable de E2 con hechos derivados de la ejecución
actual.

## 11. RED requerido

RED deberá demostrar:

- counts R/K/S reflejan exactamente el packet real;
- citation counts cuentan refs únicos válidos;
- refs repetidos cuentan una sola vez;
- refs de clases distintas permanecen separados;
- `[S999]` continúa => STOP;
- GROUNDED => `model_inference_count: 1`;
- R=K=S=0 => `model_inference_count: 0`;
- UNCONFIRMED muestra todos los citation counts en cero;
- truncation existente se preserva;
- packet enviado al modelo permanece sin nuevas señales;
- no hay provider call adicional;
- no hay I/O adicional;
- E3/E4 permanecen sin cambios.

## 12. Qué V0 sí permite observar

Después de múltiples ejecuciones externas se podrá distinguir, sin inferir causa:

```text
S available / S cited
S available / S not cited
structural-only grounded request
mixed evidence request
UNCONFIRMED request
```

La agregación histórica de esos eventos NO pertenece a V0.

## 13. Qué V0 no demuestra

Un resultado como:

```text
structural_evidence_count: 4
structural_citation_count: 3
```

no permite concluir:

```text
"Structural Evidence improved the answer"
"The answer is more correct"
"The model reasoned better"
"E3/E4 should now receive S"
```

Esas conclusiones requieren evaluación separada y evidencia comparativa.

## 14. Relación con Cognitive Assurance

V0 adopta dos propiedades ya documentadas:

```text
measure before expanding complexity
assurance evidence carries zero authority
```

Métricas más amplias como `claim_support_coverage`,
`unsupported_claim_escape_rate`, `latency_delta`,
`tokens_per_response` y `external_cost_per_response` siguen fuera de V0.

## 15. Security / Governance

```text
Prompt / Context Trust       unchanged
Identity / Delegation        unchanged
Containment / Revocation     unchanged
Memory / Knowledge           unchanged
Supply Chain                 unchanged
Data Disclosure              unchanged
Resource Governance          unchanged
Evidence / Auditability      reinforced
Human in Control             unchanged
```

No existe `BLOCKING_GAP`.

```text
observability counts carry zero authority
```

## 16. Alignment

| Fuente | Disposición | Efecto |
| --- | --- | --- |
| Cognitive Constitution | ADOPT | hechos antes que interpretación |
| Governance Constitution | ADOPT | evidence/metrics != authority |
| Blueprint | ADAPT | usar frontera existente |
| Cognitive Assurance G0/G1 | ADOPT | medir sin nuevo manager/store |
| E2 Structural Evidence V0 | REUSE | R/K/S ya disponibles |
| E3 / E4 | DEFER | no propagation |
| Structural Delta | DEFER | necesidad aún no demostrada |

## 17. Estado

```text
G0                    PASS
G1 design             ADMITTED
RED                   NOT AUTHORIZED
GREEN                 NOT AUTHORIZED

new component         0
persistent state      0
new model calls       0
new I/O               0
Kernel delta          0
Planner delta         0
E3/E4 delta           0
authority delta       0
```

El próximo gate, si el Owner lo autoriza, es RED y sólo RED.
