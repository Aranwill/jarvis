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

Exponer señales deterministas y efímeras de `Engineering Inspect (E2)` para
observar qué evidencia estuvo disponible y qué refs válidas aparecen
explícitamente en su respuesta.

V0 no mide calidad, verdad, causalidad ni mejora cognitiva.

## 2. G0

```text
baseline: 79319eef23cdd1490531d01de914712811135d9d
tracked files discovered: 270
tracked files classified: 270
silently omitted files: 0
tree truncated: false
G0 RESULT: PASS
```

La responsabilidad cabe en E2. No se justifica componente adicional.

```text
Observability V0        ADMIT
new metrics component   REJECT
persistent telemetry    REJECT
E3/E4 propagation       DEFER
Structural Delta        DEFER
```

## 3. Fuente

Las señales se derivan únicamente de datos que E2 ya posee:

```text
repository_evidence
knowledge_evidence
structural_evidence
validated model response
context_truncated
provider call path
```

No se permite nueva lectura Git/filesystem, nueva consulta estructural, nueva
llamada al modelo, network telemetry ni persistencia.

## 4. Señales V0

### Evidencia disponible

```text
repository_evidence_count
knowledge_evidence_count
structural_evidence_count
```

Significan sólo cuántos elementos de cada clase estuvieron en el packet E2.

### Citas explícitas

```text
repository_citation_count
knowledge_citation_count
structural_citation_count
```

Cada count = número de refs únicas válidas de su clase presentes explícitamente
en la respuesta.

```text
citation
!= semantic use
!= causal contribution
!= correctness
!= quality
```

### Ejecución

```text
model_inference_count ∈ {0,1}
context_truncated
```

`0`: camino sin evidencia, `UNCONFIRMED`.
`1`: una llamada al provider.

Latencia, tokens y coste quedan fuera de V0.

## 5. Output candidato

GROUNDED:

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

UNCONFIRMED:

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

## 6. Derivación

```text
evidence_count = len(evidence collection)
citation_count = count(unique validated refs of class in model output)
model_inference_count = 0 or 1 according to existing E2 path
```

Las refs desconocidas siguen produciendo STOP antes del render grounded.

## 7. Invariantes

1. Evidence availability != usefulness.
2. Citation != semantic use.
3. Citation frequency != confidence/correctness.
4. Structural citation != semantic dependency.
5. Zero citations != irrelevance.
6. Observability != evaluation.
7. Observability != authority.
8. Counts cannot authorize E3/E4 propagation.
9. Counts cannot prove quality improvement.

## 8. Scope

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
Kernel / Planner / CLI / Knowledge / Security
database / cache / event bus
telemetry exporter / metrics registry / receipt store
```

## 9. Compatibilidad

V0 no cambia:

- selección de evidencia;
- packet enviado al modelo;
- system prompt;
- número máximo de inferencias;
- validación de refs;
- límites de contexto;
- autoridad;
- E3/E4.

Sólo amplía la salida observable de E2.

## 10. RED requerido

RED deberá demostrar:

- counts R/K/S exactos;
- citation counts por refs únicas válidas;
- refs repetidas cuentan una vez;
- clases R/K/S permanecen separadas;
- ref desconocida continúa => STOP;
- GROUNDED => `model_inference_count: 1`;
- R=K=S=0 => `model_inference_count: 0`;
- UNCONFIRMED => citation counts en cero;
- truncation existente se preserva;
- packet/model prompt no incorpora estas señales;
- cero provider calls adicionales;
- cero I/O adicional;
- E3/E4 sin cambios.

## 11. Interpretación permitida

V0 permite observar:

```text
S available / S cited
S available / S not cited
structural-only grounded request
mixed evidence request
UNCONFIRMED request
```

No permite concluir:

```text
"Structural Evidence improved the answer"
"The answer is more correct"
"The model reasoned better"
"E3/E4 should receive S"
```

Eso requiere evaluación comparativa separada.

## 12. Cognitive Assurance

Se reutilizan dos propiedades ya documentadas:

```text
measure before expanding complexity
assurance evidence carries zero authority
```

`claim_support_coverage`, `unsupported_claim_escape_rate`, latencia, tokens,
coste y agregación histórica quedan fuera de V0.

## 13. Governance / Security

```text
new authority            0
new component            0
persistent state         0
new model calls          0
new I/O                  0
Kernel delta             0
Planner delta            0
E3/E4 delta              0
Evidence/Auditability    reinforced
Human in Control         unchanged
```

No existe `BLOCKING_GAP`.

## 14. Alignment

| Fuente | Disposición | Efecto |
| --- | --- | --- |
| Cognitive Constitution | ADOPT | hechos antes que interpretación |
| Governance Constitution | ADOPT | metrics != authority |
| Blueprint | ADAPT | usar frontera existente |
| Cognitive Assurance G0/G1 | ADOPT | medir sin manager/store |
| E2 Structural Evidence V0 | REUSE | R/K/S ya disponibles |
| E3/E4 | DEFER | sin propagation |
| Structural Delta | DEFER | necesidad no demostrada |

## 15. Estado

```text
G0        PASS
G1        ADMITTED
RED       NOT AUTHORIZED
GREEN     NOT AUTHORIZED
```

El próximo gate, si el Owner lo autoriza, es RED y sólo RED.
