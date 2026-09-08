---
title: Sprint 7.11 — Reproducible Validation Pipeline Foundation
status: implementation_in_progress
authority: documentación operativa de admisión y ejecución
as_of_date: 2026-09-08
baseline_commit: deb759ee9855737a24b169e03bde2028c7db7f33
branch: feat/sprint-7.11-reproducible-validation-pipeline
unit_id: SPRINT-7.11
risk_class: 3
g0_result: PASS
g1_result: PASS
g2_result: PASS
g3_result: PASS
implementation_authorized: true
rdd_stage_1: adopted
rdd_stage_2_authorized: false
merge_authority: human_only
language: es
---

# Sprint 7.11 — Reproducible Validation Pipeline Foundation

## Autoridad

El propietario autorizó explícitamente G1–G6 después de G0.

```text
baseline                     deb759ee9855737a24b169e03bde2028c7db7f33
implementation               AUTHORIZED
RDD Stage 2                  NOT AUTHORIZED
merge decision + execution   HUMAN-ONLY
```

La pipeline produce evidencia. Nunca aprobación, autorización, merge, deploy o
release.

```text
Evidence != Receipt != Validation != Decision != Authority
```

---

## Necesidad

RDD-M1 demostró que Malāk no tenía una ejecución CI reutilizable para validar un
candidato congelado fuera del entorno del Writer.

Sprint 7.11 automatiza únicamente controles que ya existían localmente:

```text
pytest
compileall
git diff --check
```

No incorpora una tooling foundation completa.

G0 File Coverage Ledger:

```text
docs/project/sprints/proposals/SPRINT-7.11-G0-COVERAGE-LEDGER.md
170 discovered / 170 classified / 0 omitted / 0 blockers
```

---

## Scope autorizado

```text
.github/workflows/validation.yml
docs/development/development_environment.md
pyproject.toml
esta ficha + evidencia PR
```

Guardrails:

```text
src/malak/** delta = 0
Kernel delta       = 0
runtime delta      = 0
authority delta    = 0
runtime deps added = 0
```

Fuera de alcance:

```text
Ruff / mypy / coverage
multi-OS matrix
secrets
pull_request_target
write permissions
branch protection enforcement
RDD Stage 2
auto-fix / auto-approval / auto-merge / auto-deploy / release
```

---

## G1 — Validation Contract & Threat Boundary — PASS

Triggers:

```text
pull_request
push: main
```

Candidate identity:

```text
PR   → github.event.pull_request.head.sha
push → github.sha
```

El checkout debe usar ese SHA exacto y comprobar:

```text
git rev-parse HEAD == expected candidate
```

Permisos:

```yaml
permissions:
  contents: read
```

Checkout:

```text
fetch-depth: 0
persist-credentials: false
```

Bootstrap oficial autorizado después de F001:

```text
actions/checkout@v6
actions/setup-python@v6
```

No se admiten acciones de terceros adicionales.

Runner:

```text
windows-latest
Python 3.12
```

Checks:

```text
python -m pytest -q
python -m compileall -q src tests scripts
PR   → git diff --check <base>...<candidate>
push → git diff --check <before>..<candidate>
```

Un `git diff --check` sin rango sobre checkout limpio no es evidencia suficiente.

---

## G2 — Reproducible Dev Bootstrap — PASS

`pytest` quedó declarado únicamente como extra de desarrollo:

```toml
[project.optional-dependencies]
dev = ["pytest>=9,<10"]
```

Se preserva:

```text
[project].dependencies = []
```

`docs/development/development_environment.md` documenta instalación `.[dev]`,
pipeline, candidate identity y frontera de autoridad.

---

## G3 — Minimal Read-Only Workflow — PASS

El workflow implementa:

```text
one workflow
one Windows runner
Python 3.12
exact candidate checkout
contents: read
no persisted credentials
pytest
compileall
explicit candidate diff range
```

No genera artifacts, comments, fixes ni mutaciones de branch.

---

## G4 — Candidate-Bound / Negative Validation

### Primer dogfood — candidato histórico

```text
candidate: e64f5d62f2067fda9bbd5e0304ef24d30db7fa4e
GitHub Actions run: 34276063172
result: PASS with non-blocking bootstrap warning discovered by review
pytest: 388 passed in 8.75s
compileall: PASS
diff-check: PASS
candidate identity: PASS
permissions: contents read + metadata read only
```

El candidate queda preservado como evidencia histórica y no certifica commits
posteriores.

### F001 — deprecated Node20 action runtime

FULL 4R / log review detectó que:

```text
actions/checkout@v4
actions/setup-python@v5
```

apuntaban a Node 20 deprecado y GitHub los forzaba a Node 24.

Estado:

```text
F001 = BOUNDED CORRECTION APPLIED
```

Correction Budget:

```text
objective: remove active Node20 deprecation from new pipeline
allowed files:
  .github/workflows/validation.yml
  this sprint record
max_fix_rounds: 1
new actions: 0
new Python deps: 0
runtime/Kernel/authority delta: 0
```

Corrección:

```text
checkout v4 → v6
setup-python v5 → v6
```

Son las mismas acciones oficiales, ahora Node24-compatible. La corrección requiere
revalidación completa sobre el nuevo candidate SHA.

---

## G5 — Dogfood

Estado:

```text
PENDING REVALIDATION AFTER F001
```

El candidate final deberá producir una nueva ejecución exitosa. El manifest Stage
1 activo permanecerá fuera del candidate tree y estará ligado al SHA exacto.

---

## G6 — Closure

Requiere:

```text
FULL 4R
independent validation
candidate-bound Stage 1 evidence
utility / overhead review
human governance
```

El merge permanece fuera de autoridad de cualquier workflow o assistant.

---

## STOP conditions

```text
src/malak/** change
Kernel/runtime/security authority change
secret exposure
write permission
pull_request_target
unapproved third-party action
runtime dependency
Ruff/mypy/coverage/multi-OS expansion
branch protection/delivery enforcement
RDD Stage 2
auto-fix/approval/merge/deploy/release
candidate identity cannot be proven
candidate diff cannot be proven
scope expansion
```

Ante STOP:

```text
STOP → preserve evidence → human authority
```

---

## Rollback

```text
deb759ee9855737a24b169e03bde2028c7db7f33
```

El cambio es exterior al runtime y reversible sin migración de datos.
