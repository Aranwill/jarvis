---
title: Malāk Repository Structural Projection V0 — G0 File Coverage Ledger
status: gate_pass
authority: operational admission evidence
as_of_date: 2026-09-20
unit_id: MALAK-REPOSITORY-STRUCTURAL-PROJECTION-V0
gate: G0
source_baseline: e14787431f864f74226706ad8655a348ee102d77
language: es
---

# Repository Structural Projection V0 — G0 Coverage

## Resultado

```text
G0 RESULT: PASS
blocking findings: 0
tracked files discovered: 262
tracked files classified: 262
silently omitted files: 0
implementation code touched: 0
```

El árbol Git recursivo del baseline declaró `truncated: false`.
El archivo rechazado `PROJECT - MANIFIESTO MALAK (1).docx` no estaba presente;
si reaparece debe clasificarse `REJECTED_DO_NOT_READ`.

## Cobertura

```text
.github/**          2
root/config        18
docs/**           108
documents/**       10
src/**             74
tests/**           50
---------------------
tracked blobs     262
```

```text
FULL_READ                    19
TARGETED_READ                21
STRUCTURAL_INSPECTION       126
HISTORICAL_REFERENCE         58
NOT_APPLICABLE_WITH_REASON   38
```

Lectura profunda aplicada a ley, arquitectura, seguridad, método, roadmap,
IDEA-013, Research Horizon, E0, composición, evidence collection,
`test_architecture_invariants.py` y `pyproject.toml`. El resto fue cubierto
por inspección estructural o referencia histórica proporcional.

## Findings

### RSPV0-G0-01 — E0 es el owner del snapshot

`GitRepositoryReader` ya fija commit, tracked files, blob identity y lectura
snapshot-bound.

**Disposition:** `REUSE`; no modificar E0.

### RSPV0-G0-02 — Existe un gap estructural real

E0 puede buscar texto, pero no expone hechos sobre módulos, símbolos e imports.
Ese gap obliga hoy a interpretar texto para preguntas que pueden resolverse
mecánicamente.

### RSPV0-G0-03 — AST ya está admitido en el baseline

`tests/test_architecture_invariants.py` ya usa `ast` de Python para verificar
imports y fronteras. No se introduce parser externo.

### RSPV0-G0-04 — IDEA-013 respalda una proyección mínima

IDEA-013 exige proyecciones `GENERATED / NON-AUTHORITATIVE / REBUILDABLE /
HASHED / VERSIONED / SOURCE-LINKED` y evita implementar mapa, retrieval, cache
y memoria en una sola unidad.

V0 implementaría sólo la primera primitive estructural.

### RSPV0-G0-05 — Ownership

La primitive pertenece a Infrastructure: deriva hechos técnicos de blobs E0.
No evalúa arquitectura, policy, autoridad ni estrategia cognitiva.

## Security Horizon

| Línea | Resultado |
| --- | --- |
| Prompt / Context Trust | NOT_APPLICABLE |
| Identity / Delegation | NOT_APPLICABLE |
| Memory / Knowledge Poisoning | NOT_APPLICABLE |
| AI Supply Chain | ALREADY_COVERED — stdlib |
| Data Disclosure | NOT_APPLICABLE |
| Resource Governance | REQUIRES_REINFORCEMENT — hard bounds |
| Evidence / Auditability | ALREADY_COVERED |
| Human in Control | ALREADY_COVERED |

No existe `BLOCKING_GAP`.

## Alignment

| Fuente | Disposición | Efecto |
| --- | --- | --- |
| Cognitive Constitution | ADOPT | determinismo antes de inferencia cuando sea suficiente |
| Governance Constitution | ADOPT | read-only, authority delta 0 |
| Blueprint / Quality Gates | ADAPT | Infrastructure primitive; Kernel delta 0 |
| SECURITY.md | ADOPT | Zero Trust; evidence != authority; bounded |
| ADR-003 | ADOPT | evidencia asciende sin transferir control |
| ADR-004 | ADOPT | RED antes de GREEN |
| E0 Repository Read | REUSE | único owner del snapshot |
| IDEA-013 | ADAPT | proyección mínima, no Knowledge Map completo |
| Research Horizon | ADOPT | instrumentos verificables antes de cognición adicional |

## Cierre

```text
G0 = PASS
external dependency   = 0
persistent store      = 0
Kernel delta          = 0
Planner delta         = 0
authority delta       = 0
writes                = 0
LLM/provider          = 0
hard resource bounds  = REQUIRED
```

Este PASS autoriza únicamente G1 documental.
