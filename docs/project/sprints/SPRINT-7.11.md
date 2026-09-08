---
title: Sprint 7.11 — Reproducible Validation Pipeline Foundation
status: completado
authority: documentación operativa derivada
as_of_date: 2026-09-08
baseline_commit: deb759ee9855737a24b169e03bde2028c7db7f33
branch: feat/sprint-7.11-reproducible-validation-pipeline
implementation_head: 59f592e2e36d11bbd14f7d9d93b1dac4f442c108
integrated_commit: 3413e8ccb348440aea757d1feccde25c65be011f
integration_pr: 65
risk_class: 3
rdd_stage_1: adopted
rdd_stage_2_authorized: false
language: es
---

# Sprint 7.11 — Reproducible Validation Pipeline Foundation

## Estado

```text
COMPLETADO
INTEGRADO EN MAIN
G0–G6 PASS
FULL 4R PASS
VALIDACIÓN INDEPENDIENTE PASS
VALIDACIÓN POST-MERGE EN MAIN PASS
```

Sprint 7.11 fue admitido, diseñado, autorizado, implementado, revisado y
validado mediante gates pequeños y evidencia ligada al candidato exacto.

La decisión y ejecución de merge permanecieron bajo autoridad humana.

Commit de integración:

```text
3413e8ccb348440aea757d1feccde25c65be011f
```

PR de integración:

```text
#65 — Sprint 7.11: Reproducible Validation Pipeline Foundation
```

El workflow de validación ejecutado sobre `main` después del merge concluyó con
`success` para el HEAD integrado exacto.

Este sprint no autoriza automáticamente ninguna unidad posterior.

---

## Baseline inicial

El sprint comenzó desde:

```text
deb759ee9855737a24b169e03bde2028c7db7f33
```

Ese baseline ya incluía RDD-M1 — Candidate-Bound Evidence Foundation.

Rollback absoluto del sprint:

```text
deb759ee9855737a24b169e03bde2028c7db7f33
```

---

## Necesidad comprobada

RDD-M1 demostró que Malāk podía producir evidencia ligada a un candidato, pero
carecía de una ejecución CI reutilizable e independiente del entorno del Writer
para validar un candidate SHA congelado.

La necesidad se resolvió sin crear una nueva capability, servicio de runtime ni
subsistema de producto.

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

---

## Scope funcional integrado

Archivos funcionales incorporados o reconciliados por Sprint 7.11:

```text
.github/workflows/validation.yml
pyproject.toml
docs/development/development_environment.md
```

Artefactos de admisión y evidencia:

```text
docs/project/sprints/proposals/SPRINT-7.11-G0-COVERAGE-LEDGER.md
docs/project/sprints/proposals/SPRINT-7.11-REPRODUCIBLE-VALIDATION-PIPELINE-FOUNDATION.md
PR #65
GitHub Actions runs asociados
```

Los documentos de `proposals/` se preservan como evidencia del proceso de
admisión, diseño, ejecución y validación. Esta ficha consolida el estado final
post-merge y evita reinterpretarlos como estado operativo vigente.

Guardrails preservados:

```text
src/malak/** delta = 0
Kernel delta       = 0
runtime delta      = 0
authority delta    = 0
runtime deps added = 0
```

---

## Contrato de validación integrado

Triggers:

```text
pull_request
push: main
```

Candidate identity:

```text
PR   → github.event.pull_request.head.sha
push → github.sha
HEAD debe coincidir con el candidate esperado
```

Permisos:

```text
contents: read
metadata: read efectivo
write permissions: none
```

Checkout y entorno:

```text
actions/checkout@v6
actions/setup-python@v6
fetch-depth: 0
persist-credentials: false
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

Dependencia de desarrollo incorporada:

```toml
[project.optional-dependencies]
dev = ["pytest>=9,<10"]
```

Se preservó:

```text
[project].dependencies = []
```

---

## Evidencia del candidato final

Candidato final antes del merge:

```text
59f592e2e36d11bbd14f7d9d93b1dac4f442c108
```

Evidencia registrada en PR #65:

```text
candidate identity     PASS
pytest                 PASS — 388 passed
compileall             PASS
diff-check             PASS
FULL 4R                PASS
independent validation PASS
G0–G6                   PASS
```

Después del merge, GitHub Actions ejecutó nuevamente `Validation` sobre:

```text
3413e8ccb348440aea757d1feccde25c65be011f
```

con conclusión:

```text
success
```

---

## Bounded Correction registrada

Durante dogfood se detectó:

```text
SPRINT-7.11-F001
Deprecated Node20 action runtime
```

Corrección acotada:

```text
actions/checkout@v4     → @v6
actions/setup-python@v5 → @v6
new actions             = 0
new Python deps         = 0
Kernel/runtime delta    = 0
authority delta         = 0
```

La revalidación posterior fue PASS.

---

## RDD

Sprint 7.11 mantiene:

```text
RDD Stage 1 = ADOPTED
RDD Stage 2 = NOT AUTHORIZED
```

Invariante permanente:

```text
Evidence != Receipt != Validation != Decision != Authority
```

La pipeline produce evidencia técnica. No puede:

- aprobar;
- autorizar;
- mergear;
- desplegar;
- publicar releases;
- ampliar scope;
- modificar gobernanza.

---

## Resultado arquitectónico

Sprint 7.11 no modifica la arquitectura funcional de Malāk.

Su resultado es una fundación de ingeniería reproducible que permite validar
candidatos exactos fuera del entorno del Writer y que puede servir de soporte a
futuras invariantes verificables, siempre mediante autorización independiente.

La última unidad funcional de producto/runtime anterior continúa siendo Sprint
7.10 — Conversation Session Isolation Foundation.

La última unidad de sprint integrada en el baseline pasa a ser Sprint 7.11.

---

## Estado posterior

```text
baseline nominal:             v0.6.0-alpha
main HEAD integrado:          3413e8ccb348440aea757d1feccde25c65be011f
último sprint integrado:      Sprint 7.11
último sprint funcional:      Sprint 7.10
sprint activo autorizado:     ninguno
rama de implementación activa: ninguna
RDD Stage 2:                  no autorizado
merge authority:              HUMAN-ONLY
```

La reconciliación documental y del Project Vault posterior al merge es trabajo
derivado. No reabre Sprint 7.11 ni concede autoridad para la siguiente unidad.
