---
title: Malāk Repository Structural Projection V0 — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation design
language: es
created: 2026-09-20
baseline_commit: e14787431f864f74226706ad8655a348ee102d77
g0_result: pass
g0_ledger: docs/project/sprints/proposals/MALAK-REPOSITORY-STRUCTURAL-PROJECTION-V0-G0-COVERAGE-LEDGER.md
design_authorized_by: owner
design_authorized_at: 2026-09-20
red_authorized: true
red_authorized_by: owner
red_authorized_at: 2026-09-20
red_baseline: 2e5f97aac41804461ceadd81680762b9e2313d13
implementation_authorized: true
implementation_authorized_by: owner
implementation_authorized_at: 2026-09-20
risk_class: 2
---

# Repository Structural Projection V0 — G0/G1 Design

## 1. Propósito

Derivar hechos sintácticos verificables del código Python ya capturado por E0:

```text
GitRepositoryReader
        ↓
      ast.parse
        ↓
ModuleFact / SymbolFact / ImportFact
```

Sin LLM, writes, store persistente ni nueva autoridad.

## 2. Necesidad

E0 resuelve lectura y búsqueda textual, pero no puede responder
determinísticamente:

```text
¿qué símbolo define este módulo?
¿dónde está definido?
¿qué imports declara este archivo?
```

V0 reduce inferencia sobre texto convirtiendo sintaxis Python en evidencia
estructurada y baseline-bound.

## 3. Ownership

La primitive pertenece a Infrastructure y consume exclusivamente
`GitRepositoryReader`.

Ruta candidata para GREEN futuro:

```text
src/malak/infrastructure/repository_structure.py
```

No se crea Manager, Service, Registry, DB, cache ni índice persistente.

## 4. Invariantes

1. E0 sigue siendo único owner del snapshot y blob identity.
2. Sólo se procesan tracked `.py` devueltos por E0.
3. Working tree, staged y untracked permanecen invisibles.
4. Parser: `ast` Python 3.12 standard library.
5. Cada fact conserva baseline, path, blob SHA y línea.
6. Orden y digest son deterministas.
7. Parse error no produce facts parciales silenciosos.
8. Hard bounds impiden crecimiento implícito.
9. La proyección sólo declara hechos sintácticos.
10. Cero writes, network, provider o LLM calls.

```text
Syntax Fact
!= Semantic Dependency
!= Architecture Assessment
!= Authority
```

## 5. Contrato V0

### ModuleFact

```text
baseline_commit
path
blob_sha
module_name
```

### SymbolFact

```text
baseline_commit
path
blob_sha
module_name
qualified_name
kind
line_number
```

`kind`:

```text
CLASS
FUNCTION
ASYNC_FUNCTION
METHOD
ASYNC_METHOD
```

### ImportFact

```text
baseline_commit
path
blob_sha
source_module
target_module
imported_name
line_number
relative_level
```

V0 registra lo demostrado por AST; no resuelve imports dinámicos ni convierte
`from x import y` en una afirmación semántica no demostrada.

## 6. API candidata

```text
RepositoryStructuralProjector(repository_reader)

project()
  -> modules
  -> symbols
  -> imports
  -> projection_digest
```

El nombre exacto puede cambiar durante RED si existe necesidad demostrada; la
responsabilidad no puede ampliarse.

## 7. Resource Governance

Antes de GREEN deben congelarse hard ceilings basados en el baseline real para:

- Python blobs procesados;
- bytes agregados;
- symbols;
- imports;
- output serializable;
- tiempo de proyección cuando aplique.

Cualquier límite configurable sólo podrá reducir esos ceilings.

## 8. Projection Identity

```text
baseline_commit
+
canonical ordered facts
        ↓ SHA-256
projection_digest
```

El digest identifica la proyección; no concede autoridad.

## 9. RED requerido

RED deberá demostrar al menos:

- mismo snapshot => misma proyección/digest;
- working tree, staged y untracked invisibles;
- HEAD posterior no muta una instancia capturada;
- non-Python ignorado;
- parse error explícito;
- class/function/async/method detectados;
- imports absolutos y relativos detectados;
- baseline/path/blob/line conservados;
- ordering estable;
- bounds fail-closed o truncation explícita según contrato;
- digest cambia ante un fact material distinto;
- cero filesystem/Git writes;
- cero provider/LLM calls.

RED candidato:

```text
tests/test_repository_structure.py
```

RED autorizado: `true`.

## 10. Fuera de alcance

```text
Kernel / Planner / CapabilityRegistry changes
Conversation / Knowledge / Security changes
E2/E3/E4 integration
CLI integration
RepositoryReader mutation
persistent index / DB / cache
RAG / GraphRAG / embeddings
Repository Knowledge Map completo
Call Graph / Control Flow Graph
semantic dependency inference
architecture violation detection
test mapping / contract mapping
structural scoring / structural delta
agents / tools / sandbox
Git/filesystem writes
RDD Stage 2
```

## 11. Estado

```text
G0                    PASS
G1 design             ADMITTED
RED                   AUTHORIZED
GREEN                 AUTHORIZED

Kernel delta          0
Planner delta         0
external dependency   0
persistent state      0
authority delta       0
```

RED y GREEN fueron autorizados por el Owner el 2026-09-20. La aceptación y el merge continúan bajo decisión exclusiva del Owner.
