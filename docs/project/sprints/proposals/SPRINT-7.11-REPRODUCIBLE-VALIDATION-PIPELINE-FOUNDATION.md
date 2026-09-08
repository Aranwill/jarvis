---
title: Sprint 7.11 — Reproducible Validation Pipeline Foundation
status: g0_pass_awaiting_implementation_authorization
authority: documentación operativa de admisión
as_of_date: 2026-09-08
baseline_commit: deb759ee9855737a24b169e03bde2028c7db7f33
branch: feat/sprint-7.11-reproducible-validation-pipeline
unit_id: SPRINT-7.11
risk_class: 3
g0_result: PASS
implementation_authorized: false
rdd_stage_1: adopted
rdd_stage_2_authorized: false
merge_authority: human_only
language: es
---

# Sprint 7.11 — Reproducible Validation Pipeline Foundation

## Estado de autoridad

El propietario autorizó la admisión formal de Sprint 7.11 sobre:

```text
deb759ee9855737a24b169e03bde2028c7db7f33
```

G0 cerró `PASS`. La implementación funcional sigue sin autorización hasta que el
propietario revise y apruebe el contrato mínimo resultante de la admisión.

Separaciones permanentes:

```text
admission
!= implementation
!= validation
!= approval
!= merge
```

```text
merge decision + merge execution = HUMAN-ONLY
```

RDD Stage 2 permanece no autorizado.

---

## Baseline

```text
repository: Aranwill/jarvis
branch: main
baseline_commit: deb759ee9855737a24b169e03bde2028c7db7f33
baseline_tree: 061ce062dba149f9e455137a54ffbeedf777566d
nominal_version: v0.6.0-alpha
latest_completed_functional_sprint: Sprint 7.10
RDD Stage 1: integrated
```

El Project Vault reconciliado observa el mismo HEAD oficial y el Sync Agent local
fue reconciliado mediante `accept-proposal` después del merge humano de la PR
#60.

---

## Necesidad comprobada

RDD-M1 demostró un cuello de botella real:

```text
candidate frozen
→ deterministic validation required
→ no CI existed in Aranwill/jarvis
→ independent execution required manual/external coordination
```

Malāk ya posee los checks locales:

```text
python -m pytest -q
python -m compileall src tests
git diff --check
```

pero `.github/` solo contiene el template de PR.

La necesidad es ejecutar esos controles de manera reproducible y ligada al
candidate exacto. No es incorporar tooling por moda.

---

## Disposición de iniciativas

```text
IDEA-009 Development Tooling Foundation       ADAPT
IDEA-011 Validation & Delivery Protocol        ADOPT parcialmente
IDEA-003 Resource Governance Foundation        OBSERVE
Memory / agents / Sandbox / cognitive dataset OBSERVE
RDD Stage 2                                    REJECT for this sprint
```

Se reutiliza únicamente lo necesario para validación reproducible y evidencia.

---

## G0 — resultado

File Coverage Ledger:

```text
docs/project/sprints/proposals/SPRINT-7.11-G0-COVERAGE-LEDGER.md
```

Resultado:

```text
tracked files discovered = 170
tracked files classified = 170
silently omitted files   = 0
blocking findings         = 0
G0                        = PASS
```

Hallazgos principales:

1. `git diff --check` sin rango explícito puede ser un no-op en checkout limpio;
2. no debe copiarse la matriz Ubuntu/Windows ni cache del Sync Agent sin necesidad;
3. `.github/**` ya está mapeado downstream por `operational-tooling-change`;
4. GitHub Actions debe producir evidencia, nunca autoridad.

---

# Contrato mínimo propuesto para implementación

## Objetivo

```text
pull request / main integration
        ↓
read-only GitHub Actions validation
        ↓
exact candidate identity
        ↓
pytest + compileall + candidate diff check
        ↓
technical evidence
        ↓
human review / human merge
```

## Archivos funcionales máximos esperados

```text
.github/workflows/validation.yml
docs/development/development_environment.md
pyproject.toml
```

No se crea nuevo script ni test module salvo que un fallo reproducible demuestre
que es necesario.

La documentación/evidencia del sprint permanece en la ficha y ledger existentes.

---

## G1 — Validation Contract & Threat Boundary

Diseño propuesto:

### Triggers

```text
pull_request
push: main
```

`pull_request_target` queda prohibido.

### Candidate identity

Para PR:

```text
candidate = github.event.pull_request.head.sha
```

El checkout debe usar explícitamente ese SHA, no confiar en el merge ref
sintético como identidad del candidato.

Para `push` a `main`:

```text
candidate = github.sha
```

Cada ejecución debe registrar el SHA evaluado y comprobar:

```text
git rev-parse HEAD == expected candidate
```

Un nuevo commit produce una nueva ejecución; evidencia anterior no certifica el
nuevo candidate.

### Permissions

```yaml
permissions:
  contents: read
```

Checkout:

```text
persist-credentials: false
fetch-depth: 0
```

Prohibido:

```text
secrets
write permissions
PR comments automáticos
branch mutation
auto-fix
auto-approval
auto-merge
auto-deploy
release
```

### Runner

Una única plataforma inicial:

```text
windows-latest
Python 3.12
```

Justificación: coincide con el entorno oficial actual de desarrollo y evita una
matriz multi-OS prematura.

### Bootstrap CI

Dependencias externas de workflow mínimas y explícitas:

```text
actions/checkout@v4
actions/setup-python@v5
```

Son bootstrap de GitHub Actions, no dependencias de runtime ni autoridad.
No se incorporan acciones de terceros adicionales.

### Pytest reproducible

`pytest` ya es una herramienta oficial del entorno de Malāk, pero actualmente no
está declarado como dependencia instalable en `pyproject.toml`.

Propuesta mínima:

```toml
[project.optional-dependencies]
dev = ["pytest>=9,<10"]
```

Esto no modifica:

```text
[project].dependencies = []
```

por lo que el runtime continúa sin dependencias Python externas.

El workflow podrá instalar:

```text
python -m pip install -e ".[dev]"
```

No se añaden Ruff, mypy, coverage ni lockfile en este sprint.

### Checks

```text
python -m pytest -q
python -m compileall -q src tests scripts
```

Whitespace/diff validation debe inspeccionar un rango real.

Para PR:

```text
git diff --check <base_sha>...<candidate_sha>
```

Para push a `main`:

```text
git diff --check <before_sha>..<candidate_sha>
```

Los SHA deben provenir del evento y quedar visibles en la ejecución.

### Semántica de resultado

```text
validation command fails      → FAIL evidence
setup / runner / timeout issue → INCONCLUSIVE for Stage 1 evidence
all required checks pass       → PASS evidence
```

El estado nativo de GitHub Actions no reemplaza el enum del Evidence Manifest;
la interpretación Stage 1 permanece externa y ligada al candidate exacto.

### Independencia

La ejecución en runner externo aporta validación determinista independiente del
entorno del Writer.

No sustituye:

```text
Reviewer
FULL 4R
human Authority
```

---

## Gates de implementación propuestos

```text
G1 — Validation Contract & Threat Boundary
     cierre documental del contrato anterior

G2 — Reproducible Dev Bootstrap
     declarar pytest dev extra + reconciliar development_environment

G3 — Minimal Read-Only Workflow
     un workflow, un runner, permisos read-only, exact candidate checkout

G4 — Candidate-Bound / Negative Validation
     verificar identity mismatch, diff real, permisos y failure behavior

G5 — Dogfood
     ejecutar la propia pipeline sobre el candidate exacto de Sprint 7.11
     emitir MALAK-EVIDENCE-MANIFEST/v1 activo fuera del candidate

G6 — Closure
     FULL 4R independiente + utility/overhead review + human governance
```

No se avanza con `FAIL` o `INCONCLUSIVE` bloqueante.

---

## Métricas de cierre

```text
changed functional files
test count / result
compileall result
diff-check result
candidate identity match
workflow permissions
runtime dependencies added
Kernel delta
runtime delta
authority delta
workflow duration
findings
correction rounds
RDD evidence overhead
```

Objetivos:

```text
runtime dependencies added = 0
Kernel delta               = 0
runtime delta              = 0
authority delta            = 0
new third-party actions    = 0
```

---

## Cuatro preguntas de ley

```text
Blueprint                 PASS
Cognitive Constitution    PASS
Governance                PASS
Kernel simplicity         PASS
```

Condición de conservación:

```text
src/malak/** delta = 0
Kernel delta       = 0
runtime delta      = 0
authority delta    = 0
```

---

## Riesgo

```text
LEVEL 3 / HIGH
FULL 4R required at closure
```

La pipeline ejecuta código del candidato en infraestructura externa. Por eso:

- no recibe secretos;
- no recibe write permissions;
- no usa `pull_request_target`;
- no persiste credenciales de checkout;
- el resultado es evidencia, no autoridad.

---

## STOP conditions

```text
requires src/malak/** change
requires Kernel/runtime/security authority change
requires secret exposure
requires write permission
requires pull_request_target
requires third-party action beyond approved bootstrap
requires new runtime dependency
requires Ruff/mypy/coverage/multi-OS expansion
requires branch protection/delivery enforcement
requires RDD Stage 2
requires auto-fix/approval/merge/deploy/release
cannot prove candidate identity
cannot prove diff actually inspected candidate delta
scope exceeds admitted files
```

Ante STOP:

```text
stop → preserve evidence → request human authority
```

---

## Rollback

Rollback absoluto:

```text
deb759ee9855737a24b169e03bde2028c7db7f33
```

El workflow y dev metadata son aditivos y pueden revertirse sin migración de
datos, Kernel, runtime o Security Control Plane.

---

## Estado actual

```text
admission authorization       YES
baseline frozen                YES
G0                             PASS
implementation authorization   PENDING
implementation code            NOT STARTED
PR                             Draft
RDD Stage 1                    ADOPTED
RDD Stage 2                    NOT AUTHORIZED
merge                          HUMAN-ONLY
```
