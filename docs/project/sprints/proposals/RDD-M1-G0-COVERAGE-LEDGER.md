---
title: RDD-M1 — G0 File Coverage Ledger
status: gate_pass
authority: evidencia operativa de admisión
as_of_date: 2026-09-08
unit_id: RDD-M1
gate: G0
source_baseline: e8c1e5c14ee1b844fa23ca5cb342237f7aaaa8f0
vault_baseline: 4024d4fad5570ba20e835bfaf3937a89c5a2e963
sync_agent_baseline: e77e276b6bb913f0814b990be9ff5ec1c9542693
language: es
---

# RDD-M1 — G0 File Coverage Ledger

## Resultado

```text
G0 RESULT: PASS
blocking findings: 0
silently omitted files: 0
next: G1
```

Se inventariaron los árboles Git recursivos completos de los tres repositorios.
Las tres respuestas declararon `truncated: false`.

```text
Aranwill/jarvis
  e8c1e5c14ee1b844fa23ca5cb342237f7aaaa8f0

Aranwill/malak-project-vault
  4024d4fad5570ba20e835bfaf3937a89c5a2e963

Aranwill/malak-vault-sync-agent
  e77e276b6bb913f0814b990be9ff5ec1c9542693
```

Cobertura conceptual por repositorio:

```text
tracked files discovered = |recursive Git tree blobs|
tracked files classified = |recursive Git tree blobs|
silently omitted files   = 0
```

Todos los blobs quedan cubiertos por una regla explícita o catch-all; la
profundidad de lectura es proporcional a su relevancia.

---

## Disposiciones

```text
FULL_READ
TARGETED_READ
STRUCTURAL_INSPECTION
HISTORICAL_REFERENCE
GENERATED_OR_DERIVED
NOT_APPLICABLE_WITH_REASON
PROTECTED
REJECTED_DO_NOT_READ
```

No se identificaron archivos trackeados que exigieran abrir secretos o material
prohibido.

---

## Malāk — source of truth

### FULL_READ

```text
AGENTS.md
docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
docs/architecture/architecture_quality_gates.md
docs/architecture/adr/ADR-003-directional-communication-and-authority-flow.md
docs/architecture/adr/ADR-004-specification-and-verification-first.md
docs/development/engineering_method.md
docs/development/malak_construction_protocol.md
docs/development/development_checklist.md
src/malak/security/audit.py
```

### TARGETED_READ

```text
docs/architecture/blueprint.md
docs/architecture/kernel.md
docs/development/development_environment.md
docs/project/implementation_roadmap.md
docs/project/project_context.md
docs/project/sprints/SPRINT-7.10.md
documents/projects/jarvis/ideas.md
docs/project/concepts/**
src/malak/observability/**
pyproject.toml
```

### STRUCTURAL_INSPECTION

```text
remaining docs/architecture/**
remaining docs/project/**
remaining documents/projects/jarvis/**
src/malak/** excluding targeted files
src/app/**
tests/**
scripts/**
.github/**
root project files
```

### HISTORICAL_REFERENCE / NOT_APPLICABLE

```text
historical sprint/archive material → HISTORICAL_REFERENCE
configs/**                        → NOT_APPLICABLE_WITH_REASON
examples/**                       → NOT_APPLICABLE_WITH_REASON
```

### Finding J-001 — runtime audit is not construction evidence

`src/malak/security/audit.py` and `src/malak/observability/**` belong to product
runtime concerns. Reusing them for RDD-M1 would mix domains.

```text
REJECT runtime reuse
RDD-M1 remains development tooling outside src/malak
```

---

## Project Vault — derived projection

### TARGETED / GENERATED_OR_DERIVED

```text
AGENTS.md
00-governance/**
01-architecture/CURRENT_COMPONENTS_MAP.md
02-current-baseline/CURRENT_BASELINE.md
03-roadmap/IMPLEMENTATION_ROADMAP.md
05-decisions/PENDING_DECISIONS.md
08-session-context/MALAK_SESSION_CONTEXT.md
10-knowledge-index/**
```

### HISTORICAL / STRUCTURAL

```text
04-sprints/**
07-audits/**
09-repository-snapshots/**
06-security/**
06-strategy/**
templates/**
remaining root files
```

Finding V-001:

```text
Vault observed official HEAD = e8c1e5c14ee1b844fa23ca5cb342237f7aaaa8f0
blocking baseline drift = none detected
```

El Vault permanece derivado y no autoriza RDD-M1.

---

## Vault Sync Agent — downstream reconciliation

### FULL / TARGETED

```text
AGENTS.md
config/vault-sync.example.yaml
src/malak_vault_sync/candidate_resolver.py
src/malak_vault_sync/evidence.py
src/malak_vault_sync/git_inspector.py
```

### STRUCTURAL_INSPECTION

```text
remaining src/malak_vault_sync/**
tests/**
docs/**
.github/**
scripts/**
pyproject.toml
remaining root files
```

### Finding S-001 — adapt patterns, do not import components

El Sync Agent ya tiene candidate/evidence/git tooling, pero su relación es:

```text
Malāk source of truth
        ↓
Sync Agent
        ↓
Project Vault
```

Por tanto:

```text
ADAPT deterministic patterns
DO NOT create upstream dependency on Sync Agent
```

### Finding S-002 — no nueva familia documental

Una ruta source nueva puede producir `COVERAGE_DRIFT`. Stage 1 usa familias ya
mapeadas:

```text
docs/development/**
scripts/**
tests/**
docs/project/sprints/**
```

Resultado:

```text
new source families = 0
Sync Agent mapping changes = 0
Sync Agent code delta = 0
```

---

## Cuatro preguntas — G0

```text
Blueprint                 PASS
Cognitive Constitution    PASS
Governance                PASS
Kernel simplicity         PASS (Kernel delta = 0)
```

---

## Proporcionalidad

G0 autoriza únicamente:

```text
1 development contract
1 read-only deterministic helper
1 focused test module
1 pilot manifest
```

No se justifican componentes arquitectónicos, runtime components, stores,
dependencias externas ni cambios al Sync Agent.

---

## Decisión

No se detectó conflicto normativo, solución existente suficiente, drift
bloqueante ni necesidad de ampliar scope.

```text
G0 = PASS
G1 authorized
Stage 2 remains unauthorized
```
