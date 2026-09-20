---
title: Malāk Repository Structural Lookup V0 — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation design
language: es
created: 2026-09-20
baseline_commit: a1028f626cdca2da9979002a21d70645ed848e3e
g0_result: pass
design_authorized_by: owner
design_authorized_at: 2026-09-20
red_authorized: true
red_authorized_by: owner
red_authorized_at: 2026-09-20
red_baseline: 4ac80a4d9d0d575096a25ef43dd67ef9900c247a
implementation_authorized: true
implementation_authorized_by: owner
implementation_authorized_at: 2026-09-20
risk_class: 1
---

# Repository Structural Lookup V0 — G0/G1 Design

## 1. Propósito

Exponer consultas estructurales exactas sobre la proyección ya integrada de
Malāk, sin volver a parsear el repositorio ni introducir inferencia semántica.

```text
GitRepositoryReader
        ↓
RepositoryStructuralProjector
        ↓
RepositoryStructuralProjection
        ↓
Repository Structural Lookup V0
```

## 2. Resultado G0

Baseline revisado:

```text
main@a1028f626cdca2da9979002a21d70645ed848e3e

tracked files discovered = 266
tracked files classified = 266
silently omitted files   = 0
G0 RESULT                 = PASS
```

La revisión confirmó que Symbol Search fue deliberadamente diferido en E0–E4 y
que la primitive estructural necesaria para habilitarlo ya existe en
`repository_structure.py`.

## 3. Necesidad demostrada

V0 ya produce facts exactos, pero hoy el consumidor debe recorrer manualmente:

- `projection.symbols`;
- `projection.imports`;
- `projection.modules`.

La siguiente necesidad mínima es poder responder mecánicamente:

```text
¿existe este símbolo exacto?
¿dónde está definido?
¿qué símbolos declara este módulo?
¿qué imports declara este módulo?
```

No se necesita LLM, fuzzy search, ranking ni índice persistente para resolverlas.

## 4. Decisión de admisión

```text
Repository Structural Lookup V0   ADMIT

Structural Delta                  DEFER
```

Structural Delta sigue siendo útil, pero E0 captura un único HEAD exacto por
reader. No existe todavía una fuente gobernada para obtener dos snapshots
arbitrarios `before/after` sin ampliar responsabilidad. Implementar el
comparador ahora crearía una primitive sin productor natural de ambos inputs.

Lookup V0, en cambio, consume inmediatamente la proyección integrada.

## 5. Ownership

La responsabilidad permanece en Infrastructure porque sólo consulta facts
sintácticos ya derivados.

Ruta candidata para GREEN futuro:

```text
src/malak/infrastructure/repository_structure_lookup.py
```

No modifica `GitRepositoryReader` ni `RepositoryStructuralProjector`.

## 6. Contrato V0

La primitive recibe una `RepositoryStructuralProjection` inmutable.

API candidata equivalente:

```text
RepositoryStructuralLookup(projection)

lookup_symbol(qualified_name)
  -> SymbolFact | None

symbols_in_module(module_name)
  -> tuple[SymbolFact, ...]

imports_from(module_name)
  -> tuple[ImportFact, ...]
```

Semántica:

- `lookup_symbol` usa coincidencia exacta de `qualified_name`;
- cero resultados => `None`;
- más de un resultado exacto => fallo explícito, no selección arbitraria;
- `symbols_in_module` filtra por `module_name`;
- `imports_from` filtra por `source_module`;
- el orden devuelto conserva orden determinista de la proyección.

## 7. Invariantes

1. Lookup no vuelve a leer Git ni filesystem.
2. Lookup no vuelve a ejecutar AST.
3. Projection identity permanece intacta.
4. Un resultado conserva baseline/path/blob/line del fact original.
5. Lookup exacto no normaliza, corrige ni expande nombres.
6. No existe fuzzy matching, score, ranking ni semantic resolution.
7. Un import sigue siendo sintaxis observada, no dependencia arquitectónica.
8. Resultado vacío no se convierte en inferencia.
9. Cero writes, network, provider o LLM.
10. Lookup no asigna authority, severity, decision o permission.

```text
Lookup result
!= architecture assessment
!= authority
```

## 8. Resource Governance

La primitive reutiliza los hard bounds de la proyección y no crea estructuras
persistentes adicionales.

Puede construir mappings efímeros únicamente si RED demuestra una necesidad
material. V0 no autoriza cache global ni índice persistente.

## 9. Malāk Alignment Matrix

| Fuente | Disposición | Efecto |
| --- | --- | --- |
| Cognitive Constitution | ADOPT | regla determinista antes de inferencia probabilística |
| Governance Constitution | ADOPT | read-only; authority delta 0 |
| Blueprint / Quality Gates | ADAPT | Infrastructure primitive; Kernel delta 0 |
| SECURITY.md | ADOPT | evidence != authority; sin nueva superficie sensible |
| E0 Repository Read | REUSE | snapshot owner sin cambios |
| Structural Projection V0 | REUSE | único productor de facts |
| IDEA-013 | ADAPT | consulta mínima sobre proyección reconstruible |
| E2/E3/E4 designs | OBSERVE | Symbol Search diferido allí; no integrar todavía |
| Structural Delta | OBSERVE | útil, pero sin dual-snapshot producer gobernado |

## 10. Security Horizon

```text
Prompt / Context Trust       NOT_APPLICABLE
Identity / Delegation        NOT_APPLICABLE
Containment / Revocation     NOT_APPLICABLE
Memory / Knowledge Poisoning NOT_APPLICABLE
Supply Chain                 ALREADY_COVERED
Data Disclosure              NOT_APPLICABLE
Resource Governance          ALREADY_COVERED
Evidence / Auditability      ALREADY_COVERED
Human in Control             ALREADY_COVERED
```

No existe `BLOCKING_GAP`.

## 11. RED requerido antes de GREEN

RED deberá demostrar al menos:

- exact qualified symbol encontrado;
- símbolo inexistente devuelve `None`;
- colisión exacta produce fallo explícito;
- symbols por módulo sólo devuelve facts de ese módulo;
- imports por módulo sólo devuelve facts de ese source_module;
- resultados preservan identidad y provenance originales;
- orden determinista;
- query vacía o inválida rechazada;
- no se modifica la proyección;
- cero Git/filesystem reads adicionales;
- cero writes;
- cero provider/LLM calls;
- ausencia de fuzzy/substring matching.

RED candidato:

```text
tests/test_repository_structure_lookup.py
```

## 12. Fuera de alcance

```text
Structural Delta
dual-snapshot repository read
fuzzy search
substring search
ranking / scoring
semantic search
dependency graph
call graph
control-flow graph
architecture assessment
test mapping
contract mapping
persistent index / DB / cache
E2/E3/E4 integration
CLI integration
Kernel / Planner changes
agents / tools / sandbox
RDD Stage 2
```

## 13. Estado

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

RED y GREEN fueron autorizados por el Owner el 2026-09-20. La aceptación final y el merge permanecen bajo decisión exclusiva del Owner.
