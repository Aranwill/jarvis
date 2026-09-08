---
title: Sprint 7.11 — G0 File Coverage Ledger
status: gate_pass
authority: evidencia operativa de admisión
as_of_date: 2026-09-08
unit_id: SPRINT-7.11
gate: G0
source_baseline: deb759ee9855737a24b169e03bde2028c7db7f33
vault_baseline: a36c9e8b4ee1a98f1c25a86ebe8e8035cbf8fc32
sync_agent_baseline: e77e276b6bb913f0814b990be9ff5ec1c9542693
language: es
---

# Sprint 7.11 — G0 File Coverage Ledger

## Resultado

```text
G0 RESULT: PASS
blocking findings: 0
tracked files discovered: 170
tracked files classified: 170
silently omitted files: 0
implementation code touched: 0
```

El inventario exhaustivo obligatorio de esta admisión cubre el repositorio
oficial `Aranwill/jarvis` en el baseline exacto:

```text
deb759ee9855737a24b169e03bde2028c7db7f33
```

El Project Vault y el Vault Sync Agent se consultaron como contexto downstream
de reconciliación y cobertura. No forman parte del scope de implementación de
Sprint 7.11 y no reciben cambios por esta admisión.

---

## Inventario por familia

Los árboles recursivos Git utilizados declararon `truncated: false` en las
familias inspeccionadas.

```text
root files                         8
.github/**                         1
configs/**                         1
docs/**                           52
documents/**                      10
examples/**                        1
scripts/**                         8
src/**                            55
tests/**                          34
------------------------------------
tracked blobs                    170
classified blobs                 170
silently omitted                  0
```

Cada blob queda cubierto por una disposición explícita o por un catch-all de
familia. La profundidad de lectura es proporcional a autoridad y relevancia.

---

## Disposiciones utilizadas

```text
FULL_READ
TARGETED_READ
STRUCTURAL_INSPECTION
HISTORICAL_REFERENCE
GENERATED_OR_DERIVED
NOT_APPLICABLE_WITH_REASON
```

No se identificaron archivos trackeados que exigieran `PROTECTED` o
`REJECTED_DO_NOT_READ`.

---

# Malāk — source of truth

## FULL_READ

```text
AGENTS.md
docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
docs/architecture/architecture_quality_gates.md
docs/development/development_checklist.md
docs/development/development_environment.md
docs/development/engineering_method.md
docs/development/evidence_manifest.md
docs/development/malak_construction_protocol.md
docs/project/sprints/SPRINT-7.10.md
```

Razón: fuentes de ley, método, entorno reproducible, RDD Stage 1 y último sprint
funcional completado.

## TARGETED_READ

```text
docs/architecture/blueprint.md
docs/architecture/kernel.md
docs/architecture/adr/ADR-003-directional-communication-and-authority-flow.md
docs/architecture/adr/ADR-004-specification-and-verification-first.md
docs/architecture/decisions/decision-index.md
docs/project/implementation_roadmap.md
docs/project/project_context.md
docs/project/roadmap.md
documents/projects/jarvis/ideas.md
docs/project/concepts/README.md
docs/project/concepts/GOVERNED_EPHEMERAL_AGENT_EXECUTION_EVIDENCE_REFERENCE.md
docs/project/concepts/GOVERNED_SWARM_LONG_HORIZON_REFERENCE.md
docs/project/concepts/MALAK_COGNITIVE_DATASET_FOUNDATION.md
pyproject.toml
scripts/test.ps1
scripts/malak_evidence.py
tests/test_malak_evidence.py
.github/PULL_REQUEST_TEMPLATE.md
```

Razón: planificación, autoridad direccional, tooling actual, candidate-bound
evidence y referencias conceptuales aplicables.

## STRUCTURAL_INSPECTION

```text
remaining docs/architecture/**
remaining docs/development/**
remaining docs/governance/**
docs/knowledge/**
docs/operations/**
remaining docs/project/**
remaining documents/projects/jarvis/** excluding archive/releases historical
remaining scripts/**
src/app/**
src/malak/**
tests/** excluding test_malak_evidence.py
root project files not listed above
```

Resultado estructural relevante:

```text
src/malak/** current implementation exists
Sprint 7.11 requires no runtime reuse
Kernel/runtime/security implementation remains forbidden
```

## HISTORICAL_REFERENCE

```text
docs/project/sprints/SPRINT-7.0.md ... SPRINT-7.9.md
docs/project/sprints/proposals/RDD-M1-*.md
docs/project/sprints/proposals/SPRINT-7.3-SECOND-CAPABILITY-DRAFT.md
documents/projects/jarvis/archive/**
documents/projects/jarvis/releases/**
```

Sirven para precedentes y trazabilidad; no definen el estado actual por encima
del baseline vigente.

## GENERATED_OR_DERIVED

```text
docs/project/implementation_roadmap.md
docs/project/project_context.md
docs/project/roadmap.md
ROADMAP.md
```

Cuando además figuran como TARGETED_READ, prevalece la profundidad de lectura
indicada; esta disposición registra su clase de autoridad derivada.

## NOT_APPLICABLE_WITH_REASON

```text
configs/**
examples/**
```

No participan en la necesidad de una pipeline de validación y no justifican
modificación.

---

# Revisión de necesidad

## Evidencia existente

Malāk ya posee los checks deterministas locales necesarios:

```text
python -m pytest -q
python -m compileall src tests
git diff --check
```

El proyecto oficial usa Python 3.12 y `pyproject.toml` declara `dependencies = []`.

La carpeta `.github/` del baseline solo contiene:

```text
PULL_REQUEST_TEMPLATE.md
```

No existe workflow CI en `Aranwill/jarvis`.

RDD-M1 demostró que la ausencia de una ejecución reproducible externa al writer
crea fricción al congelar un candidate SHA y buscar validación independiente.

Conclusión:

```text
need = demonstrated
new runtime capability = not needed
new application component = not needed
```

---

# Necessity & Complexity Review

## Alternativa A — No hacer nada

```text
OBSERVE / not preferred
```

Ventaja: cero delta.

Costo: conserva el cuello de botella demostrado de validación reproducible e
independiente.

## Alternativa B — Development Tooling Foundation completa

```text
REJECT for this sprint
```

Ruff, mypy, dev dependency model, matrices amplias, coverage gates y tooling
adicional no son necesarios para resolver el problema actual.

## Alternativa C — Pipeline mínima reutilizando checks actuales

```text
ADAPT / SELECTED
```

Resuelve la necesidad sin alterar producto ni crear subsistemas.

## Alternativa D — CI + RDD Stage 2 / receipts

```text
REJECT
```

Stage 2 no está autorizado y no es necesario para obtener validación
reproducible.

---

# Referencias futuras revalidadas

## IDEA-009 — Development Tooling Foundation

```text
ADAPT
```

Se adopta únicamente la intención de tooling reproducible. Las herramientas
concretas continúan sujetas a necesidad separada.

## IDEA-011 — Malāk Validation & Delivery Protocol

```text
ADOPT parcialmente
```

Se reutiliza evidencia compacta, paquetes pequeños y reversibilidad.
Delivery no concede autoridad y merge permanece humano.

## IDEA-003 — Resource Governance Foundation

```text
OBSERVE
```

No existe motivo para mezclar recursos de runtime con esta unidad de tooling.

## Concepts agentic / Cognitive Dataset

```text
OBSERVE
```

Aportan principios de evidencia, Least Context y separación de autoridad, pero
no justifican agentes, sandbox, dataset ni nuevas capacidades en este sprint.

---

# Downstream review

## Project Vault

El Vault reconciliado observa:

```text
official HEAD = deb759ee9855737a24b169e03bde2028c7db7f33
```

No se detecta baseline drift bloqueante para iniciar esta admisión.

## Vault Sync Agent

La regla vigente:

```text
operational-tooling-change
source_patterns:
  - .github/**
  - .gitignore
  - configs/**
  - docs/development/**
  - examples/**
  - scripts/**
```

ya cubre un eventual `.github/workflows/**`.

Resultado:

```text
new source family = 0
Sync Agent mapping delta = 0
Sync Agent code delta = 0
```

El CI existente del Sync Agent se utiliza solo como referencia comprobada de
que GitHub Actions funciona en el ecosistema Malāk. No se copiará su matriz
Ubuntu/Windows, cache ni `.[dev]` por defecto porque Malāk no ha demostrado esa
necesidad.

---

# Findings G0

## G0-F001 — `git diff --check` no puede ser un no-op

Estado:

```text
RESOLVED AS G1 REQUIREMENT
```

En un checkout limpio, ejecutar `git diff --check` sin especificar el rango que
se pretende validar puede producir un PASS sin inspeccionar el delta del
candidato.

G1 deberá definir semántica exacta y reproducible, candidate-bound, por ejemplo
sobre el commit o rango explícitamente seleccionado. No se aprueba aquí un
comando definitivo.

## G0-F002 — no copiar CI downstream por conveniencia

Estado:

```text
RESOLVED BY SCOPE
```

El Sync Agent posee CI con matriz Ubuntu/Windows, cache pip y extra `.[dev]`.
Sprint 7.11 no hereda esos elementos sin evidencia propia.

## G0-F003 — infraestructura externa sin autoridad

Estado:

```text
RESOLVED AS HARD INVARIANT
```

GitHub Actions podrá producir evidencia técnica. Nunca decisión, approval,
authorization, merge, deploy o release.

---

# Cuatro preguntas de ley — G0

```text
1. Blueprint                 PASS
2. Cognitive Constitution    PASS
3. Governance                PASS
4. Kernel simplicity         PASS
```

Evidencia estructural:

```text
planned src/malak delta      0
planned Kernel delta         0
planned runtime delta        0
planned authority delta      0
planned external Python deps 0
```

---

# Riesgo y review

```text
risk_class = LEVEL 3 / HIGH
FULL 4R required at closure
```

Razón: la pipeline ejecutará código en infraestructura externa y su resultado se
usará como evidencia de validación, aunque no tenga autoridad.

---

# Scope admitido para diseño

G0 admite diseñar, no implementar todavía:

```text
1 minimal GitHub Actions workflow
Python 3.12
existing pytest suite
compileall
candidate-bound whitespace/diff validation
minimum/read-only permissions
RDD Stage 1 evidence reuse
```

Fuera de alcance permanece todo lo enumerado en la ficha de admisión,
especialmente:

```text
src/malak/**
new Python dependencies
Ruff / mypy
broad matrices
RDD Stage 2
auto-fix / auto-approval / auto-merge / auto-deploy
```

---

# Decisión G0

No se detectó conflicto normativo, componente existente que deba reutilizarse en
runtime, drift downstream bloqueante ni necesidad de ampliar el scope.

```text
G0 = PASS
next = G1 design
implementation_authorization = PENDING HUMAN AUTHORITY
merge = HUMAN-ONLY
RDD Stage 2 = NOT AUTHORIZED
```
