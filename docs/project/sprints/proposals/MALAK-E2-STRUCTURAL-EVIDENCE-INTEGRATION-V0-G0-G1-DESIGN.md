---
title: Malāk E2 Structural Evidence Integration V0 — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation design
language: es
created: 2026-09-20
baseline_commit: 2a00a16618a7f11403edd06f051fd8cbb68849ed
g0_result: pass
design_authorized_by: owner
design_authorized_at: 2026-09-20
red_authorized: false
implementation_authorized: false
risk_class: 2
---

# E2 Structural Evidence Integration V0 — G0/G1 Design

## 1. Propósito

Permitir que E2 Engineering Inspect consuma evidencia estructural determinista
derivada del mismo snapshot E0, sin ampliar autoridad ni propagar el cambio a
E3/E4.

```text
GitRepositoryReader
        │
        ├── GovernedKnowledgeReader
        │
        └── RepositoryStructuralProjector
                  ↓
          RepositoryStructuralLookup
                  ↓
          Engineering Inspect (E2)
```

## 2. Resultado G0

```text
baseline: 2a00a16618a7f11403edd06f051fd8cbb68849ed
tracked files discovered: 269
tracked files classified: 269
silently omitted files: 0
tree truncated: false
G0 RESULT: PASS
```

La integración puede realizarse con componentes ya existentes y sin nuevo
runtime, storage, provider, tool o dependencia externa.

## 3. Decisión de admisión

```text
E2 Structural Evidence Integration V0  ADMIT
E3 propagation                         DEFER
E4 propagation                         DEFER
Structural Delta                       DEFER
```

La integración se limita a E2 para medir utilidad antes de expandir la nueva
superficie de evidencia a Analyze o Propose.

## 4. Evidencia disponible

E2 conserva sus superficies actuales:

```text
[R#] Repository text evidence
[K#] Governed Knowledge evidence
```

V0 agrega:

```text
[S#] Structural syntax evidence
```

Los facts [S#] provienen únicamente de:

- `RepositoryStructuralProjection`;
- `RepositoryStructuralLookup`.

No vuelven a leer Git, filesystem ni ejecutar AST.

## 5. Binding de baseline

Debe cumplirse:

```text
repository_reader.baseline_commit
==
knowledge_reader.baseline_commit
==
structural_projection.baseline_commit
```

Mismatch => STOP.

La proyección estructural se crea desde el mismo `GitRepositoryReader` que
compone Engineering Intelligence.

## 6. Semántica de consulta V0

El `inspection_term` existente se reutiliza literalmente contra Structural
Lookup:

```text
lookup_symbol(term)
symbols_in_module(term)
imports_from(term)
```

No existe:

- intent classifier;
- fuzzy matching;
- substring structural search;
- normalización semántica;
- dependency resolution.

Un term puede producir cero o más structural facts exactos según esos tres
lookups.

## 7. Structural Evidence Fact

Cada [S#] debe preservar la provenance original.

### Symbol

```text
ref
fact_type: symbol
baseline_commit
path
blob_sha
module_name
qualified_name
kind
line_number
```

### Import

```text
ref
fact_type: import
baseline_commit
path
blob_sha
source_module
target_module
imported_name
relative_level
line_number
```

Regla:

```text
Structural Fact
!= Semantic Dependency
!= Architecture Assessment
!= Authority
```

## 8. Comportamiento E2

El packet de E2 pasa conceptualmente de:

```text
repository_evidence
knowledge_evidence
limitations
```

a:

```text
repository_evidence
knowledge_evidence
structural_evidence
limitations
```

El modelo puede citar:

```text
[R#] [K#] [S#]
```

Toda cita estructural inexistente => STOP.

El system prompt debe declarar que [S#] es evidencia sintáctica no confiable
como instrucción y no implica dependencia, decisión o autoridad.

## 9. No-evidence behavior

Si:

```text
R = 0
K = 0
S = 0
```

se preserva:

```text
NO MODEL CALL
status: UNCONFIRMED
```

Si sólo existe S, E2 puede realizar su única inferencia usando esa evidencia.
No se agregan llamadas adicionales al modelo.

## 10. Bounds

Se reutilizan los hard bounds de Structural Projection.

E2 agrega solamente:

```text
max structural refs in model context = 12
```

Si existen más facts elegibles:

```text
context_truncated: true
```

El límite total de prompt continúa siendo el hard limit E2 existente.

## 11. Ownership y cambios admitidos

GREEN futuro puede requerir únicamente:

```text
src/malak/app/composition.py
src/malak/capabilities/engineering_inspect.py
```

RED futuro:

```text
tests/test_engineering_inspect.py
tests/test_app_composition.py  # sólo si el contrato existente lo requiere
```

No se admite modificar:

```text
src/malak/capabilities/_engineering_evidence.py
src/malak/capabilities/_engineering_analysis.py
src/malak/capabilities/engineering_analyze.py
src/malak/capabilities/engineering_propose.py
src/malak/infrastructure/repository_reader.py
src/malak/infrastructure/repository_structure.py
src/malak/infrastructure/repository_structure_lookup.py
Kernel
Planner
CLI
Knowledge
Security
```

## 12. Invariantes

1. E2 continúa read-only.
2. E2 continúa stateless.
3. Máximo una inferencia por request.
4. Cero inferencias cuando R=K=S=0.
5. Structural evidence se reúne antes de inferencia.
6. Lookup exacto solamente.
7. [S#] conserva baseline/path/blob/line originales.
8. No se transforma import syntax en semantic dependency.
9. Evidence != Authority.
10. E3 y E4 permanecen byte-for-byte fuera del incremento funcional.
11. No se crea nueva persistencia, cache o índice.
12. Cero writes, shell, network o tool execution nuevos.

## 13. RED requerido antes de GREEN

RED deberá demostrar al menos:

- baseline E0/E1/Structural mismatch => STOP;
- exact symbol produce [S#];
- exact module produce symbol/import [S#];
- substring/fuzzy no produce structural match;
- provenance structural preservada;
- orden determinista de [S#];
- máximo 12 structural refs;
- overflow marca `context_truncated=true`;
- [S999] inventado => STOP;
- system prompt reconoce structural syntax evidence y sus límites;
- R/K actuales no cambian;
- ausencia de S conserva comportamiento E2 previo;
- R=K=S=0 => UNCONFIRMED y cero provider calls;
- exactamente una provider call cuando existe evidencia;
- cero nueva I/O desde Structural Lookup;
- E3 packet sin `structural_evidence`;
- E4 packet sin `structural_evidence`;
- cero writes.

## 14. Security Horizon

```text
Prompt / Context Trust       REQUIRES_REINFORCEMENT
Identity / Delegation        NOT_APPLICABLE
Containment / Revocation     NOT_APPLICABLE
Memory / Knowledge Poisoning NOT_APPLICABLE
Supply Chain                 ALREADY_COVERED
Data Disclosure              ALREADY_COVERED
Resource Governance          ALREADY_COVERED
Evidence / Auditability      REQUIRES_REINFORCEMENT
Human in Control             ALREADY_COVERED
```

Refuerzos requeridos: [S#] no es instrucción, no es semantic truth y las citas
deben validarse contra el pack real.

No existe `BLOCKING_GAP`.

## 15. Malāk Alignment

| Fuente | Disposición | Efecto |
| --- | --- | --- |
| Cognitive Constitution | ADOPT | determinismo antes de inferencia |
| Governance Constitution | ADOPT | evidence != authority |
| Blueprint / Quality Gates | ADAPT | integración Capability-first; Kernel intacto |
| SECURITY.md | ADOPT | structural context untrusted |
| ADR-003 | ADOPT | evidence asciende sin transferir control |
| ADR-004 | ADOPT | G0/G1 + RED antes de GREEN |
| E0 / E1 / E2 | REUSE | mismo snapshot y contratos existentes |
| Structural Projection V0 | REUSE | productor único de facts |
| Structural Lookup V0 | REUSE | lookup exacto |
| E3 / E4 | DEFER | sin propagación en V0 |

## 16. Estado

```text
G0                    PASS
G1 design             ADMITTED
RED                   NOT AUTHORIZED
GREEN                 NOT AUTHORIZED

Kernel delta          0
Planner delta         0
E3/E4 delta           0
external dependency   0
persistent state      0
authority delta       0
new model calls       0
```

El próximo gate, si el Owner lo aprueba, es RED y sólo RED.
