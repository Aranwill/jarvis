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
red_authorized: true
red_authorized_by: owner
red_authorized_at: 2026-09-20
red_baseline: e7ce1bfab8b73690c8e3c5b032c6baf0ee63b2c0
implementation_authorized: false
risk_class: 2
---

# E2 Structural Evidence Integration V0 — G0/G1 Design

## 1. Propósito

Integrar en E2 evidencia estructural determinista derivada del mismo snapshot E0,
sin ampliar autoridad ni propagar el cambio a E3/E4.

```text
GitRepositoryReader
   ├─ GovernedKnowledgeReader
   └─ RepositoryStructuralProjector
          ↓
      RepositoryStructuralLookup
          ↓
  Engineering Inspect (E2)
```

## 2. G0

```text
baseline: 2a00a16618a7f11403edd06f051fd8cbb68849ed
tracked files discovered: 269
tracked files classified: 269
silently omitted files: 0
tree truncated: false
G0 RESULT: PASS
```

La integración reutiliza componentes existentes y no requiere nuevo runtime,
storage, provider, tool o dependencia externa.

## 3. Decisión de admisión

```text
E2 Structural Evidence Integration V0  ADMIT
E3 propagation                         DEFER
E4 propagation                         DEFER
Structural Delta                       DEFER
```

V0 se limita a E2 para obtener evidencia de uso real antes de ampliar Analyze o
Propose.

## 4. Superficies de evidencia

E2 conserva:

```text
[R#] repository text evidence
[K#] governed knowledge evidence
```

y agrega:

```text
[S#] structural syntax evidence
```

[S#] proviene únicamente de `RepositoryStructuralProjection` y
`RepositoryStructuralLookup`. Lookup no vuelve a leer Git/filesystem ni ejecuta
AST.

## 5. Baseline binding

Debe cumplirse:

```text
repository_reader.baseline_commit
==
knowledge_reader.baseline_commit
==
structural_projection.baseline_commit
```

Mismatch => STOP.

La proyección debe construirse desde el mismo `GitRepositoryReader` compartido
por Engineering Intelligence.

## 6. Consulta V0

El `inspection_term` existente se usa literalmente:

```text
lookup_symbol(term)
symbols_in_module(term)
imports_from(term)
```

No hay intent classifier, fuzzy matching, substring structural search,
normalización semántica ni dependency resolution.

## 7. Formato [S#]

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

```text
Structural Fact
!= Semantic Dependency
!= Architecture Assessment
!= Authority
```

## 8. Comportamiento E2

El packet incorpora:

```text
repository_evidence
knowledge_evidence
structural_evidence
limitations
```

El modelo puede citar `[R#]`, `[K#]` y `[S#]`. Una cita estructural no
existente => STOP.

El system prompt debe declarar [S#] como evidencia sintáctica no confiable como
instrucción y no equivalente a dependency, decision o authority.

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

Si sólo existe S, E2 mantiene como máximo una inferencia. V0 no agrega llamadas
al modelo.

## 9. Bounds

Se reutilizan los hard bounds de Structural Projection.

E2 agrega:

```text
max structural refs in model context = 12
```

Más facts elegibles => `context_truncated=true`.

El hard limit total del prompt E2 permanece sin cambios.

## 10. Scope admitido

GREEN futuro puede modificar únicamente:

```text
src/malak/app/composition.py
src/malak/capabilities/engineering_inspect.py
```

RED futuro:

```text
tests/test_engineering_inspect.py
tests/test_app_composition.py  # sólo si el contrato existente lo exige
```

Fuera de alcance:

```text
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
Structural Delta
persistent index/cache/DB
new tools/agents
```

## 11. Invariantes

1. E2 sigue read-only y stateless.
2. Máximo una inferencia por request.
3. Cero inferencias cuando R=K=S=0.
4. Structural evidence se reúne antes de inferencia.
5. Lookup exacto solamente.
6. [S#] preserva baseline/path/blob/line originales.
7. Import syntax no se convierte en semantic dependency.
8. Evidence != Authority.
9. E3/E4 quedan funcionalmente intactos.
10. No hay nueva persistencia, cache, write, shell, network o tool execution.

## 12. RED requerido

RED deberá demostrar:

- baseline E0/E1/Structural mismatch => STOP;
- exact symbol produce [S#];
- exact module produce symbol/import [S#];
- substring/fuzzy no produce structural match;
- provenance y orden estructural preservados;
- máximo 12 [S#];
- overflow => `context_truncated=true`;
- [S999] inventado => STOP;
- system prompt reconoce límites de structural syntax evidence;
- R/K actuales no cambian;
- ausencia de S conserva comportamiento previo;
- R=K=S=0 => UNCONFIRMED y cero provider calls;
- exactamente una provider call cuando existe evidencia;
- cero nueva I/O desde Structural Lookup;
- E3/E4 packets no incorporan `structural_evidence`;
- cero writes.

## 13. Security Horizon

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

Refuerzos: [S#] no es instrucción ni semantic truth; toda cita se valida contra
el pack real. No existe `BLOCKING_GAP`.

## 14. Alignment

| Fuente | Disposición | Efecto |
| --- | --- | --- |
| Cognitive Constitution | ADOPT | determinismo antes de inferencia |
| Governance Constitution | ADOPT | evidence != authority |
| Blueprint / Quality Gates | ADAPT | Capability-first; Kernel intacto |
| SECURITY.md | ADOPT | structural context untrusted |
| ADR-003 | ADOPT | evidence sin transferencia de control |
| ADR-004 | ADOPT | RED antes de GREEN |
| E0 / E1 / E2 | REUSE | mismo snapshot |
| Structural Projection V0 | REUSE | productor de facts |
| Structural Lookup V0 | REUSE | lookup exacto |
| E3 / E4 | DEFER | sin propagación V0 |

## 15. Estado

```text
G0                    PASS
G1 design             ADMITTED
RED                   AUTHORIZED
GREEN                 NOT AUTHORIZED

Kernel delta          0
Planner delta         0
E3/E4 delta           0
external dependency   0
persistent state      0
authority delta       0
new model calls       0
```

RED fue autorizado por el Owner el 2026-09-20. Este documento no autoriza GREEN.
