---
title: Sprint 7.11 — Reproducible Validation Pipeline Foundation
status: ready_for_independent_validation
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
g4_result: PASS
g5_result: PASS
implementation_authorized: true
rdd_stage_1: adopted
rdd_stage_2_authorized: false
merge_authority: human_only
language: es
---

# Sprint 7.11 — Reproducible Validation Pipeline Foundation

## Estado

```text
G0 admission                         PASS
G1 validation/threat contract        PASS
G2 reproducible dev bootstrap        PASS
G3 minimal read-only workflow        PASS
G4 candidate-bound validation        PASS
G5 dogfood                           PASS
G6 independent validation/governance PENDING
```

Baseline:

```text
deb759ee9855737a24b169e03bde2028c7db7f33
```

RDD Stage 2 permanece no autorizado.

```text
merge decision + merge execution = HUMAN-ONLY
```

---

## Necesidad y solución

RDD-M1 demostró que Malāk carecía de una ejecución CI reutilizable para validar
un candidato congelado fuera del entorno del Writer.

La solución reutiliza únicamente controles ya existentes:

```text
candidate / PR
    ↓
read-only GitHub Actions
    ↓
exact candidate identity
pytest
compileall
candidate-bound diff-check
    ↓
technical evidence
    ↓
human review / human merge
```

No se implementó una Development Tooling Foundation completa.

---

## Scope final

Archivos funcionales:

```text
.github/workflows/validation.yml
docs/development/development_environment.md
pyproject.toml
```

Evidencia/admisión:

```text
docs/project/sprints/proposals/SPRINT-7.11-G0-COVERAGE-LEDGER.md
esta ficha
PR #65 / GitHub Actions runs
```

Guardrails verificados:

```text
src/malak/** delta = 0
Kernel delta       = 0
runtime delta      = 0
authority delta    = 0
runtime deps added = 0
```

---

## Contrato implementado

Triggers:

```text
pull_request
push: main
```

No existe `pull_request_target`.

Candidate identity:

```text
PR   → github.event.pull_request.head.sha
push → github.sha
git rev-parse HEAD must equal expected candidate
```

Permisos:

```yaml
permissions:
  contents: read
```

GitHub agrega `metadata: read` de forma efectiva; no existen permisos de
escritura.

Checkout:

```text
fetch-depth: 0
persist-credentials: false
```

Bootstrap oficial:

```text
actions/checkout@v6
actions/setup-python@v6
```

Runner:

```text
windows-latest
Python 3.12
```

Dev dependency:

```toml
[project.optional-dependencies]
dev = ["pytest>=9,<10"]
```

Se preserva:

```text
[project].dependencies = []
```

Checks:

```text
python -m pytest -q
python -m compileall -q src tests scripts
PR   → git diff --check <base>...<candidate>
push → git diff --check <before>..<candidate>
```

---

## G0 — Admission — PASS

Ledger:

```text
170 tracked files discovered
170 classified
0 silently omitted
0 blocking findings
```

Disposición principal:

```text
IDEA-009 Development Tooling Foundation  ADAPT
IDEA-011 Validation & Delivery Protocol   ADOPT parcialmente
Resource Governance                       OBSERVE
Memory / agents / Sandbox                 OBSERVE
RDD Stage 2                               REJECT for this sprint
```

---

## G4 finding y Bounded Correction

### F001 — deprecated Node20 action runtime

El primer dogfood usó:

```text
actions/checkout@v4
actions/setup-python@v5
```

y el runner informó que ambas actions apuntaban a Node 20 deprecado.

Correction Budget:

```text
allowed files:
  .github/workflows/validation.yml
  sprint record
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

Revalidación posterior: PASS.

---

## G5 — Dogfood — PASS

Primer candidato histórico:

```text
e64f5d62f2067fda9bbd5e0304ef24d30db7fa4e
run 34276063172
388 passed
compileall PASS
diff-check PASS
candidate identity PASS
```

Ese run produjo F001 durante review y quedó superseded para certificación de
candidatos posteriores.

Candidato revalidado después de F001:

```text
aed4374fcb7709e22a10d7f793735044d6b0bdac
run 34276296506
388 passed in 8.69s
compileall PASS
diff-check PASS
candidate identity PASS
Contents read / Metadata read
Node20 deprecation absent
```

Este documento de cierre crea un nuevo candidate SHA. Por RDD Stage 1, el run de
`aed4374f...` permanece evidencia histórica válida pero **no certifica el nuevo
HEAD**. El nuevo HEAD debe recibir una ejecución completa antes de G6.

El manifest Stage 1 activo se conserva fuera del candidate tree, ligado al SHA
exacto validado.

---

## FULL 4R — self-review

### Risk — PASS

- ejecuta código del candidato en infraestructura externa;
- token efectivo read-only;
- sin secrets;
- sin `pull_request_target`;
- sin branch mutation;
- sin delivery authority.

### Readability — PASS

- un workflow;
- un job;
- pasos explícitos;
- no wrappers ni DSL adicional;
- documentación local reconciliada.

### Reliability — PASS

- candidate SHA se verifica contra `HEAD`;
- PR y push usan rangos de diff explícitos;
- suite completa y compileall se ejecutan desde instalación `.[dev]`;
- fallos de comandos producen job failure.

### Resilience — PASS

- `fetch-depth: 0` permite resolver base/candidate;
- base faltante falla cerrado;
- push con `before` nulo usa `git show --check`;
- timeout de job: 15 minutos;
- F001 eliminó la deprecación activa detectada.

Observación no bloqueante:

```text
runner image + pytest range + official action major tags
→ reproducibilidad operacional, no hermeticidad bit-for-bit
```

Cada run conserva las versiones y action SHA resueltas en logs. No se justifica
introducir lockfile, pinning criptográfico o infraestructura adicional en Stage 1.

Self-review no sustituye independent validation.

---

## G6 — pendiente

Para cierre final se requiere sobre el **nuevo HEAD exacto**:

```text
GitHub Actions PASS
candidate identity PASS
FULL 4R independent review / human validation
Stage 1 evidence bound to exact SHA
utility / overhead review
human governance
```

Ningún PASS técnico autoriza merge.

---

## Utility / overhead preliminar

Valor demostrado:

```text
manual external test coordination
→ automatic candidate-bound validation on every PR candidate
```

Costo funcional:

```text
1 workflow
1 dev extra
1 development-environment reconciliation
0 runtime components
0 runtime dependencies
0 Kernel changes
0 authority changes
```

La mayor carga documental pertenece al File Coverage Ledger obligatorio de G0,
no a operación recurrente de la pipeline.

---

## STOP / rollback

Continúan prohibidos:

```text
src/malak/** changes
Kernel/runtime/security authority changes
secrets / write permissions
pull_request_target
third-party actions
runtime dependencies
Ruff/mypy/coverage/multi-OS expansion
branch protection/delivery enforcement
RDD Stage 2
auto-fix/approval/merge/deploy/release
```

Rollback absoluto:

```text
deb759ee9855737a24b169e03bde2028c7db7f33
```

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
