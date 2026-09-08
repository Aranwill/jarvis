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

## 1. Resultado

```text
G0 — ADMISSION & BASELINE REVIEW
RESULT: PASS
BLOCKING FINDINGS: 0
SILENTLY OMITTED FILES: 0
NEXT GATE: G1 — MALAK-EVIDENCE-MANIFEST/v1
```

Este ledger documenta la cobertura transversal exigida por
`docs/development/malak_construction_protocol.md` para admitir RDD-M1.

La cobertura se ejecutó sobre snapshots Git exactos y completos de los tres
repositorios relacionados. Las tres respuestas recursivas de Git declararon
`truncated: false`.

```text
Aranwill/jarvis
  baseline = e8c1e5c14ee1b844fa23ca5cb342237f7aaaa8f0

Aranwill/malak-project-vault
  baseline = 4024d4fad5570ba20e835bfaf3937a89c5a2e963

Aranwill/malak-vault-sync-agent
  baseline = e77e276b6bb913f0814b990be9ff5ec1c9542693
```

Para cada repositorio se aplica la siguiente identidad de cobertura:

```text
tracked files discovered = |recursive Git tree blobs|
tracked files classified = |recursive Git tree blobs|
silently omitted files   = 0
```

La clasificación es exhaustiva mediante reglas de path con catch-all. La
profundidad de lectura es proporcional a la relevancia del artefacto.

---

# 2. Disposiciones utilizadas

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

No se identificó ningún archivo trackeado que requiriera abrir secretos o
material expresamente prohibido. Cualquier artefacto futuro que coincida con una
restricción de protección deberá inventariarse sin ser leído.

---

# 3. Ledger — Aranwill/jarvis

## 3.1 Fuentes de ley y arquitectura

| Path / familia | Tipo | Autoridad | Profundidad | Disposición | Razón |
|---|---|---:|---|---|---|
| `AGENTS.md` | reglas operativas | alta operativa | full | FULL_READ | gobierna revisión integral, gates y cobertura |
| `docs/governance/cognitive_constitution.md` | Constitución | máxima | full | FULL_READ | proporcionalidad, minimización y trazabilidad |
| `docs/governance/governance_constitution.md` | Constitución | máxima | full | FULL_READ | mínimo privilegio, separación, auditoría y no autoescalamiento |
| `docs/architecture/blueprint.md` | Blueprint | alta | targeted | TARGETED_READ | P-012 y límites arquitectónicos aplicables |
| `docs/architecture/architecture_quality_gates.md` | quality gates | alta | full | FULL_READ | Kernel First, Human in Control, Traceability |
| `docs/architecture/kernel.md` | especificación Kernel | alta | structural | STRUCTURAL_INSPECTION | confirmar `Kernel delta = 0` |
| `docs/architecture/adr/ADR-003-directional-communication-and-authority-flow.md` | ADR accepted | alta | full | FULL_READ | autoridad downstream, evidencia upstream sin autoridad |
| `docs/architecture/adr/ADR-004-specification-and-verification-first.md` | ADR accepted | alta | full | FULL_READ | specification + evidence, sin autoridad implícita |
| restantes `docs/architecture/**` | arquitectura | alta/media | structural | STRUCTURAL_INSPECTION | no presentan dependencia RDD-M1 que exija modificación |

## 3.2 Método, planificación e ideas

| Path / familia | Tipo | Profundidad | Disposición | Razón |
|---|---|---|---|---|
| `docs/development/engineering_method.md` | método | full | FULL_READ | Candidate Identity, 4R, bounded correction, validation |
| `docs/development/malak_construction_protocol.md` | protocolo | full | FULL_READ | Stage 0→1, gates, evidence manifest y cobertura |
| `docs/development/development_checklist.md` | checklist | full | FULL_READ | reglas de RDD progresivo y cierre |
| `docs/development/development_environment.md` | entorno | targeted | TARGETED_READ | herramientas externas no forman baseline automáticamente |
| `docs/project/implementation_roadmap.md` | roadmap derivado | targeted | TARGETED_READ | necesidad y autorización no automática |
| `docs/project/project_context.md` | contexto | targeted | TARGETED_READ | autoridad direccional y baseline |
| `documents/projects/jarvis/ideas.md` | registro de ideas | targeted | TARGETED_READ | Content-Bound Evidence Receipts + anti-overengineering |
| `docs/project/concepts/**` | referencias conceptuales | recursive targeted | TARGETED_READ | lectura recursiva completada; evidencia externa relevante |
| `docs/project/sprints/SPRINT-7.10.md` | último sprint | targeted | TARGETED_READ | último baseline funcional cerrado |
| restantes `docs/project/sprints/**` | histórico de ejecución | structural/history | HISTORICAL_REFERENCE | patrón de gates/cierre; no autoridad nueva |
| `documents/projects/jarvis/archive/**` | legacy | structural | HISTORICAL_REFERENCE | no usar como baseline actual |
| restantes `documents/projects/jarvis/**` | proyecto/legacy | structural | STRUCTURAL_INSPECTION | sin mecanismo existente que sustituya Stage 1 |

## 3.3 Código y tests

| Path / familia | Tipo | Profundidad | Disposición | Razón |
|---|---|---|---|---|
| `src/malak/security/audit.py` | runtime security audit | full | FULL_READ | evaluado para posible reutilización; rechazado para RDD-M1 por dominio |
| `src/malak/observability/**` | observabilidad runtime | targeted | TARGETED_READ | evaluado para reutilización; no corresponde a evidencia de construcción |
| `src/malak/kernel/**` | Kernel | structural | STRUCTURAL_INSPECTION | debe permanecer intacto |
| restante `src/malak/**` | runtime/product code | structural | STRUCTURAL_INSPECTION | no existe tooling Stage 1 reutilizable dentro del runtime |
| `src/app/**` | launcher/app | structural | NOT_APPLICABLE_WITH_REASON | fuera del dominio de construcción RDD-M1 |
| `tests/**` | tests | structural | STRUCTURAL_INSPECTION | base de regresión; se añadirá test focalizado sin modificar tests runtime |
| `scripts/**` | development tooling | structural | STRUCTURAL_INSPECTION | ubicación existente adecuada para helper mínimo |
| `.github/**` | workflow/review | structural | STRUCTURAL_INSPECTION | no requiere nuevo workflow para RDD-M1 |
| `configs/**` | runtime config | structural | NOT_APPLICABLE_WITH_REASON | no corresponde al contrato de evidencia |
| `examples/**` | ejemplos | structural | NOT_APPLICABLE_WITH_REASON | no participa en Stage 1 |
| `pyproject.toml` | proyecto Python | targeted | TARGETED_READ | no se justifican dependencias nuevas |
| restantes archivos root | proyecto | structural | STRUCTURAL_INSPECTION | sin conflicto o solución Stage 1 existente |

### Finding J-001 — No reutilizar auditoría runtime

`src/malak/security/audit.py` representa auditoría de autorización operacional y
`src/malak/observability/**` representa eventos operativos del producto.

Usarlos para evidencia de construcción mezclaría dominios y responsabilidades.

```text
disposition: REJECT reuse as RDD-M1 dependency
reason: separation of responsibilities
```

RDD-M1 permanecerá en development tooling, fuera de `src/malak`.

---

# 4. Ledger — Aranwill/malak-project-vault

El Vault es derivado y no puede definir arquitectura o autoridad de RDD-M1.

| Path / familia | Profundidad | Disposición | Razón |
|---|---|---|---|
| `AGENTS.md` | targeted | TARGETED_READ | autoridad y reglas de proyección |
| `00-governance/**` | targeted | TARGETED_READ | confirmar subordinación del Vault |
| `01-architecture/CURRENT_COMPONENTS_MAP.md` | targeted | GENERATED_OR_DERIVED | verificar que no exista componente RDD ya implementado |
| `02-current-baseline/CURRENT_BASELINE.md` | full/targeted | GENERATED_OR_DERIVED | confirma HEAD oficial observado `e8c1e5c1...` |
| `03-roadmap/IMPLEMENTATION_ROADMAP.md` | targeted | GENERATED_OR_DERIVED | planificación derivada |
| `05-decisions/PENDING_DECISIONS.md` | targeted | GENERATED_OR_DERIVED | detectar conflicto o decisión pendiente relevante |
| `08-session-context/MALAK_SESSION_CONTEXT.md` | targeted | GENERATED_OR_DERIVED | contexto operacional |
| `10-knowledge-index/**` | targeted | GENERATED_OR_DERIVED | referencias conceptuales derivadas |
| `07-audits/**` | structural/history | HISTORICAL_REFERENCE | evidencia histórica del Sync Agent |
| `09-repository-snapshots/**` | structural/history | HISTORICAL_REFERENCE | snapshots no sustituyen fuente oficial |
| `04-sprints/**` | structural/history | HISTORICAL_REFERENCE | cierres derivados |
| `06-security/**`, `06-strategy/**` | structural | STRUCTURAL_INSPECTION | sin bloqueo específico RDD-M1 |
| `templates/**`, root restante | structural | STRUCTURAL_INSPECTION | sin contrato Stage 1 reutilizable |

### Finding V-001 — Baseline reconciliado

El Vault observa exactamente el baseline oficial usado por RDD-M1:

```text
e8c1e5c14ee1b844fa23ca5cb342237f7aaaa8f0
```

No se detectó drift de baseline que bloquee G0.

---

# 5. Ledger — Aranwill/malak-vault-sync-agent

El Sync Agent es downstream respecto de `Aranwill/jarvis/main`.

| Path / familia | Profundidad | Disposición | Razón |
|---|---|---|---|
| `AGENTS.md` | full | FULL_READ | autoridad, cobertura y reglas de nuevas rutas |
| `config/vault-sync.example.yaml` | full | FULL_READ | operación determinista y límites |
| `src/malak_vault_sync/candidate_resolver.py` | full | FULL_READ | mappings existentes para rutas propuestas |
| `src/malak_vault_sync/evidence.py` | full | FULL_READ | patrones reutilizables conceptualmente |
| `src/malak_vault_sync/git_inspector.py` | targeted | TARGETED_READ | inspección Git downstream |
| `src/malak_vault_sync/audit.py` | structural | STRUCTURAL_INSPECTION | dominio propio del Sync Agent |
| restantes `src/malak_vault_sync/**` | structural | STRUCTURAL_INSPECTION | no deben convertirse en dependencia upstream |
| `tests/**` | structural | STRUCTURAL_INSPECTION | demuestra madurez del agente, no contrato Malāk |
| `docs/**` | structural/targeted | STRUCTURAL_INSPECTION | operación y cierres del agente |
| `.github/**`, `scripts/**`, `pyproject.toml`, root restante | structural | STRUCTURAL_INSPECTION | sin bloqueo RDD-M1 |

### Finding S-001 — Existe tooling similar, pero no es reutilizable como dependencia

El Sync Agent ya posee:

```text
candidate_resolver
evidence
git_inspector
audit
```

pero su relación autorizada es:

```text
Malāk source of truth
        ↓
Sync Agent
        ↓
Project Vault
```

Convertir `Aranwill/jarvis` en consumidor del Sync Agent introduciría una
inversión de dependencia y mezclaría autoridad upstream/downstream.

```text
disposition: ADAPT PATTERNS, DO NOT IMPORT COMPONENTS
```

Patrones admitidos como referencia:

- stdlib antes que dependencias nuevas;
- JSON determinista;
- validación estricta de SHA Git;
- fail-closed ante evidencia inválida;
- provenance explícita.

### Finding S-002 — No crear `docs/project/evidence/**` en Stage 1

El Sync Agent considera una ruta fuente nueva como evento de cobertura y puede
producir `COVERAGE_DRIFT` cuando no existe mapping.

RDD-M1 no necesita una nueva familia documental.

Ubicaciones seleccionadas:

```text
contract:
  docs/development/evidence_manifest.md

helper:
  scripts/malak_evidence.py

tests:
  tests/test_malak_evidence.py

pilot manifest:
  docs/project/sprints/proposals/RDD-M1-EVIDENCE-MANIFEST.json
```

Las cuatro familias ya están observadas por mappings existentes.

Resultado:

```text
new Sync Agent mapping = 0
Sync Agent code delta   = 0
new source family       = 0
```

---

# 6. Cuatro preguntas obligatorias — cierre G0

## ¿Respeta el Blueprint?

PASS. El cambio permanece en tooling de desarrollo, no introduce dependencia
runtime y preserva la dirección de autoridad.

## ¿Respeta la Constitución Cognitiva?

PASS. Refuerza evidencia y trazabilidad aplicando proporcionalidad y
minimización. No participa en cognición.

## ¿Respeta la Constitución de Gobernanza?

PASS. Preserva mínimo privilegio, separación de responsabilidades,
no-autoescalamiento y Human in Control.

## ¿Mantiene simple el Kernel?

PASS condicionado permanentemente a:

```text
Kernel delta = 0
```

---

# 7. Evaluación de sobreingeniería

```text
new runtime components = 0
new architectural components = 0
new external dependencies = 0
new database/store = 0
new source path families = 0
Sync Agent changes = 0
Kernel changes = 0
Security authority changes = 0
```

Se justifica únicamente:

```text
1 development contract
1 deterministic helper
1 focused test module
1 pilot evidence artifact
```

Cada elemento cubre directamente el gap aprobado de Stage 1.

---

# 8. Riesgo y rollback

Riesgo inicial de la unidad:

```text
LEVEL 3 / HIGH
```

por tratarse de tooling que soportará evidencia de aceptación, aunque no posea
autoridad.

Rollback:

- retirar contrato;
- retirar helper;
- retirar tests específicos;
- retirar evidencia piloto si corresponde;
- revertir documentación de la unidad.

No existe migración de datos ni impacto en runtime.

---

# 9. Decisión G0

No se detectó:

- conflicto con Constitución, Blueprint o ADR;
- solución existente dentro de Malāk que vuelva innecesario Stage 1;
- necesidad de nueva Capability;
- necesidad de tocar Kernel;
- necesidad de tocar Security Control Plane;
- necesidad de modificar Sync Agent;
- dependencia externa justificada;
- drift bloqueante.

```text
G0 RESULT = PASS
AUTHORIZED NEXT = G1 — Evidence Contract v1
```

G0 no autoriza Stage 2 ni amplía el alcance G0–G6 previamente aprobado.
