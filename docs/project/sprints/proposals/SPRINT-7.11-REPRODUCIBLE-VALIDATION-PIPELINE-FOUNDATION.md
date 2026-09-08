---
title: Sprint 7.11 — Reproducible Validation Pipeline Foundation
status: implementation_authorized
authority: documentación operativa de admisión y ejecución
as_of_date: 2026-09-08
baseline_commit: deb759ee9855737a24b169e03bde2028c7db7f33
branch: feat/sprint-7.11-reproducible-validation-pipeline
unit_id: SPRINT-7.11
risk_class: 3
g0_result: PASS
g1_result: PASS
implementation_authorized: true
rdd_stage_1: adopted
rdd_stage_2_authorized: false
merge_authority: human_only
language: es
---

# Sprint 7.11 — Reproducible Validation Pipeline Foundation

## Autoridad y estado

El propietario aprobó explícitamente la implementación después de revisar G0 y
el contrato mínimo resultante.

```text
baseline                       deb759ee9855737a24b169e03bde2028c7db7f33
G0 admission                   PASS
G1 validation/threat contract  PASS
implementation                 AUTHORIZED
RDD Stage 2                    NOT AUTHORIZED
merge decision + execution     HUMAN-ONLY
```

La autorización cubre únicamente G1–G6 dentro del scope de esta ficha. Un STOP
requiere nueva autoridad humana; ningún actor puede ampliar su propio scope.

---

## Necesidad comprobada

RDD-M1 demostró un cuello de botella real:

```text
candidate frozen
→ deterministic validation required
→ no CI in Aranwill/jarvis
→ independent execution required manual/external coordination
```

Malāk ya usa localmente:

```text
python -m pytest -q
python -m compileall src tests
git diff --check
```

Sprint 7.11 automatiza esos controles sobre el candidato exacto. No introduce
nuevos controles de calidad por inercia.

File Coverage Ledger de admisión:

```text
docs/project/sprints/proposals/SPRINT-7.11-G0-COVERAGE-LEDGER.md
170 discovered / 170 classified / 0 silently omitted / 0 blockers
```

---

## Disposición de iniciativas

```text
IDEA-009 Development Tooling Foundation       ADAPT
IDEA-011 Validation & Delivery Protocol        ADOPT parcialmente
IDEA-003 Resource Governance Foundation        OBSERVE
Memory / agents / Sandbox                      OBSERVE
RDD Stage 2                                    REJECT for this sprint
```

---

## Scope autorizado

Máximo funcional:

```text
.github/workflows/validation.yml
docs/development/development_environment.md
pyproject.toml
```

Documentación/evidencia del sprint puede actualizar esta ficha y el PR.

No se crea nuevo script ni test module salvo finding reproducible que lo haga
necesario y permanezca dentro del objetivo aprobado.

Guardrails:

```text
src/malak/** delta = 0
Kernel delta       = 0
runtime delta      = 0
authority delta    = 0
runtime deps added = 0
```

---

## G1 — Validation Contract & Threat Boundary — PASS

### Triggers

```text
pull_request
push: main
```

`pull_request_target` está prohibido.

### Candidate identity

PR:

```text
candidate = github.event.pull_request.head.sha
```

Push a main:

```text
candidate = github.sha
```

El checkout debe usar explícitamente el candidate SHA y verificar:

```text
git rev-parse HEAD == expected candidate
```

Un commit nuevo implica candidato nuevo y nueva validación.

### Permissions / supply boundary

```yaml
permissions:
  contents: read
```

Checkout:

```text
persist-credentials: false
fetch-depth: 0
```

Bootstrap permitido:

```text
actions/checkout@v4
actions/setup-python@v5
```

No se admiten acciones de terceros adicionales, secretos ni permisos de
escritura.

### Runner

```text
windows-latest
Python 3.12
```

Una sola plataforma para evitar matriz prematura.

### Dev bootstrap

`pytest` ya es herramienta oficial de Malāk. Se autoriza declararlo solo como
extra de desarrollo:

```toml
[project.optional-dependencies]
dev = ["pytest>=9,<10"]
```

`[project].dependencies` debe permanecer vacío.

### Checks requeridos

```text
python -m pytest -q
python -m compileall -q src tests scripts
```

El diff check debe inspeccionar un rango real:

```text
PR   → git diff --check <base_sha>...<candidate_sha>
push → git diff --check <before_sha>..<candidate_sha>
```

Nunca se acepta `git diff --check` sin rango como evidencia suficiente sobre un
checkout limpio.

### Resultado

```text
command failure              → FAIL evidence
runner/setup/environment gap → INCONCLUSIVE Stage 1 evidence
all required checks pass     → PASS evidence
```

GitHub Actions produce evidencia técnica. No produce aprobación, autorización ni
merge authority.

---

## Gates autorizados

```text
G2 — Reproducible Dev Bootstrap
     pytest dev extra + development_environment

G3 — Minimal Read-Only Workflow
     exact candidate checkout + read-only permissions + required checks

G4 — Candidate-Bound / Negative Validation
     identity, diff range, permissions, failure semantics

G5 — Dogfood
     ejecutar pipeline sobre candidate exacto
     manifest Stage 1 activo fuera del candidate

G6 — Closure
     FULL 4R + independent validation + utility/overhead review
```

No se avanza ante `FAIL` o `INCONCLUSIVE` bloqueante.

---

## Riesgo y cierre

```text
LEVEL 3 / HIGH
FULL 4R required
Writer != Reviewer != Validator != Authority
```

Métricas mínimas:

```text
candidate identity match
pytest result
compileall result
diff-check result
workflow permissions
workflow duration
changed functional files
runtime dependencies added
Kernel/runtime/authority delta
findings + correction rounds
RDD evidence overhead
```

---

## STOP conditions

```text
requires src/malak/** change
requires Kernel/runtime/security authority change
requires secret exposure
requires write permission
requires pull_request_target
requires unapproved third-party action
requires runtime dependency
requires Ruff/mypy/coverage/multi-OS expansion
requires branch protection/delivery enforcement
requires RDD Stage 2
requires auto-fix/approval/merge/deploy/release
cannot prove candidate identity
cannot prove candidate delta was inspected
scope exceeds admitted files
```

Ante STOP:

```text
STOP → preserve evidence → request human authority
```

---

## Rollback

```text
deb759ee9855737a24b169e03bde2028c7db7f33
```

El cambio es exterior al runtime y reversible sin migración de datos.

---

## Invariante permanente

```text
Evidence != Receipt != Validation != Decision != Authority

validation PASS
→ evidence only
→ human reviews
→ human decides
→ human executes merge
```
