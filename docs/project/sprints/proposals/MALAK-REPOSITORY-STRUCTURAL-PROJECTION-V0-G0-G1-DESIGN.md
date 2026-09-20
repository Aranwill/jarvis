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
red_authorized: false
implementation_authorized: false
risk_class: 2
---

# Malāk Repository Structural Projection V0 — G0/G1 Design

## 1. Propósito

Definir una primitive determinista, read-only y snapshot-bound que derive hechos
sintácticos verificables del código Python ya capturado por E0.

Pregunta de aceptación:

> ¿Puede Malāk conocer símbolos e imports de su propio código mediante hechos AST
> ligados al mismo commit/blob de E0, sin LLM, writes, store persistente ni nueva
> autoridad?

---

## 2. Baseline

```text
repository: Aranwill/jarvis
branch: main
baseline: e14787431f864f74226706ad8655a348ee102d77

E0 Repository Read          INTEGRATED
E1 Knowledge Read           INTEGRATED
E2 Engineering Inspect      INTEGRATED
E3 Engineering Analyze      INTEGRATED
E4 Engineering Propose      INTEGRATED
E5-A Command Surface        INTEGRATED
E5-B1 Read-only Explorer    INTEGRATED
```

G0:

```text
tracked files discovered = 262
tracked files classified = 262
silently omitted files   = 0
G0 RESULT                 = PASS
```

---

## 3. Necesidad demostrada

E0 ya puede leer y buscar texto del snapshot exacto, pero no puede responder
mecánicamente:

```text
¿qué símbolos define este módulo?
¿dónde está definido este símbolo?
¿qué imports declara este archivo?
```

Responderlas hoy requiere buscar texto y luego interpretar.

V0 reduce esa inferencia transformando sintaxis Python en evidencia estructurada.

---

## 4. Ownership arquitectónico

La primitive pertenece a Infrastructure porque:

- consume blobs read-only de E0;
- deriva hechos técnicos;
- no decide qué significan arquitectónicamente;
- no autoriza ni ejecuta acciones.

Ruta candidata para GREEN futuro:

```text
src/malak/infrastructure/repository_structure.py
```

No se crea Manager, Service, Registry, DB, cache ni index persistente.

---

## 5. Invariantes V0

1. E0 continúa siendo único owner del snapshot y del blob identity.
2. V0 sólo procesa contenido devuelto por `GitRepositoryReader`.
3. Working tree, staged y untracked continúan invisibles.
4. Sólo se procesan tracked paths `.py`.
5. Se usa `ast` de Python 3.12 standard library.
6. Cada fact conserva `baseline_commit`, `path`, `blob_sha` y línea fuente.
7. El orden de módulos, símbolos e imports es determinista.
8. La proyección completa posee digest determinista.
9. Un parse error no produce facts parciales silenciosos.
10. Superar cualquier hard bound produce fallo explícito o truncation explícita
    según lo que congele RED; nunca crecimiento implícito.
11. La proyección no asigna autoridad, severidad ni meaning arquitectónico.
12. No existe write, shell, Git write, network, provider ni LLM call.

Principio:

```text
Syntax Fact
!= Semantic Dependency
!= Architecture Assessment
!= Authority
```

---

## 6. Contratos candidatos

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

`kind` queda cerrado a:

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

V0 registra lo que el AST demuestra. No resuelve dinámicamente imports ni
convierte automáticamente `from x import y` en una afirmación de que
`x.y` es un módulo.

---

## 7. API mínima candidata

El comportamiento verificable esperado es equivalente a:

```text
RepositoryStructuralProjector(repository_reader)

baseline_commit

project()
  -> modules
  -> symbols
  -> imports
  -> projection_digest
```

El nombre exacto del tipo/API puede ajustarse durante RED si existe una razón
demostrada. No se autoriza ampliar responsabilidad.

---

## 8. Resource Governance V0

G1 exige hard bounds explícitos para:

- cantidad máxima de Python blobs procesados;
- bytes Python agregados procesados;
- symbols emitidos;
- imports emitidos;
- bytes máximos de salida serializable;
- tiempo máximo de proyección cuando aplique.

Los valores exactos deberán elegirse desde el baseline real y congelarse antes
de GREEN.

Los límites configurables, si se admiten, sólo podrán reducir hard ceilings.

---

## 9. Projection Identity

La identidad debe derivarse de representación canónica de facts ya ordenados y
del baseline exacto.

Conceptualmente:

```text
baseline_commit
+
canonical ordered facts
        ↓
SHA-256
        ↓
projection_digest
```

El digest identifica la proyección; no la convierte en fuente autoritativa.

---

## 10. RED requerido antes de GREEN

Debe demostrar al menos:

- mismo snapshot => misma proyección y digest;
- cambio de working tree invisible;
- staged change invisible;
- untracked `.py` invisible;
- avance posterior de HEAD no muta una instancia ya capturada;
- non-Python ignorado;
- parse error explícito;
- class detectada correctamente;
- function y async function detectadas;
- method y async method detectados;
- qualified names deterministas para nesting soportado;
- import absoluto detectado;
- import relativo detectado;
- alias preservado cuando sea material al fact;
- cada fact conserva baseline/path/blob/line;
- ordering determinista;
- hard bounds fail-closed/truncated según contrato;
- digest cambia cuando cambia un fact material;
- cero filesystem writes;
- cero Git writes;
- cero provider/LLM calls.

RED autorizado: `false`.

---

## 11. Scope futuro de RED/GREEN

RED candidato:

```text
tests/test_repository_structure.py
```

GREEN candidato:

```text
src/malak/infrastructure/repository_structure.py
```

Ningún archivo funcional adicional está admitido en V0 sin volver a G1.

---

## 12. Fuera de alcance

```text
Kernel changes
Planner changes
CapabilityRegistry changes
Conversation changes
Knowledge changes
Security PDP/PEP changes
Engineering Inspect integration
Engineering Analyze integration
Engineering Propose integration
CLI integration
RepositoryReader mutation
persistent index
database
cache
embeddings
RAG / GraphRAG
Repository Knowledge Map completo
Call Graph
Control Flow Graph
semantic dependency inference
architecture violation detection
test-to-component mapping
contract-to-implementation mapping
structural scoring
baseline structural delta
agents
tools
sandbox
Git/filesystem writes
RDD Stage 2
```

---

## 13. Resultado G1

```text
Repository Structural Projection V0

G0                         PASS
G1 design                  ADMITTED
RED                        NOT AUTHORIZED
GREEN                      NOT AUTHORIZED

Kernel delta               0
Planner delta              0
external dependencies      0
persistent state           0
authority delta            0
```

El próximo gate, si el Owner lo aprueba, es RED y sólo RED.
