---
title: Sprint 7.11 — Reproducible Validation Pipeline Foundation
status: admission_authorized
authority: documentación operativa de admisión
as_of_date: 2026-09-08
baseline_commit: deb759ee9855737a24b169e03bde2028c7db7f33
branch: feat/sprint-7.11-reproducible-validation-pipeline
unit_id: SPRINT-7.11
risk_class: 3
implementation_authorized: false
rdd_stage_1: adopted
rdd_stage_2_authorized: false
merge_authority: human_only
language: es
---

# Sprint 7.11 — Reproducible Validation Pipeline Foundation

## Estado de autoridad

El propietario autorizó iniciar la **admisión formal** de Sprint 7.11 sobre el
baseline exacto `deb759ee9855737a24b169e03bde2028c7db7f33` después de revisar la
comparativa de próximos pasos.

Esta autorización permite:

- congelar baseline;
- crear esta rama temporal de admisión;
- ejecutar G0 en modo read-only;
- materializar el File Coverage Ledger;
- definir necesidad, scope, riesgos y gates;
- preparar un PR Draft como contenedor auditable.

No autoriza todavía implementación funcional. La implementación solo puede
comenzar después de que G0 cierre `PASS` y el alcance resultante continúe dentro
de esta admisión sin activar una condición de STOP.

Separaciones permanentes:

```text
admission authorization
!= implementation evidence
!= validation
!= approval
!= merge
```

```text
merge execution = HUMAN-ONLY
```

Ningún agente, assistant, reviewer, validator, workflow, manifest o mecanismo de
automatización puede ejecutar, auto-habilitar o reinterpretar el merge.

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

El baseline fue re-verificado antes de crear la rama de admisión.

---

## Necesidad comprobada

RDD-M1 demostró una limitación operacional real: ante un candidato congelado,
Malāk carecía de una vía CI reutilizable que pudiera ejecutar validaciones
deterministas sobre el SHA exacto y producir evidencia técnica reproducible.

Estado actual relevante:

```text
.github/
└── PULL_REQUEST_TEMPLATE.md

scripts/test.ps1
→ python -m pytest -v

pyproject.toml
→ pytest configurado
→ Python >= 3.12
→ dependencies = []
```

La necesidad no es incorporar tooling moderno por inercia. Es reducir la fricción
entre:

```text
candidate frozen
→ deterministic validation
→ candidate-bound evidence
→ independent review
→ human governance
```

sin otorgar autoridad a la pipeline.

---

## Disposición de iniciativas preservadas

### IDEA-009 — Development Tooling Foundation

```text
ADAPT
```

Se conserva únicamente la intención de calidad y desarrollo reproducibles.
Ruff, mypy, dependencias de desarrollo separadas, matrices amplias y tooling
adicional quedan diferidos hasta demostrar necesidad propia.

### IDEA-011 — Malāk Validation & Delivery Protocol

```text
ADOPT parcialmente como restricción de proceso
```

Se reutilizan paquetes pequeños, trazables, reversibles y evidencia compacta.
No se adopta ninguna autoridad de delivery, auto-approval ni auto-merge.

### IDEA-003 — Resource Governance Foundation

```text
OBSERVE
```

Su propia admisión futura requiere evidencia telemétrica suficiente. No forma
parte de Sprint 7.11.

### Evolución conversacional / Memory / agentes

```text
OBSERVE
```

No existe necesidad demostrada que justifique mezclarlos con esta unidad.

---

## Objetivo

Establecer una pipeline mínima, reproducible y de solo validación para candidatos
de Malāk, reutilizando los checks ya existentes y sin tocar el runtime.

Flujo objetivo:

```text
candidate / pull request
        ↓
read-only validation pipeline
        ↓
pytest
compileall
git diff --check
        ↓
candidate-bound evidence
        ↓
human review
        ↓
human-only merge decision and execution
```

La pipeline informa. No decide.

---

## Scope candidato

Alcance inicial sujeto a cierre de G0:

```text
.github/workflows/**          candidato a nuevo artefacto
pyproject.toml                solo si una necesidad mínima de config lo exige
scripts/**                    reutilizar antes de crear wrappers nuevos
tests/**                      solo tests del tooling si fueran necesarios
docs/project/sprints/**       evidencia de sprint
```

Objetivo de cambios funcionales esperado:

- una única pipeline;
- Python 3.12;
- `python -m pytest`;
- `python -m compileall -q src tests scripts`;
- `git diff --check` ligado al baseline/candidato aplicable;
- permisos mínimos de GitHub;
- evidencia compatible con `MALAK-EVIDENCE-MANIFEST/v1`.

---

## Fuera de alcance

```text
src/malak/**
Kernel
Planner
Conversation
Memory
Knowledge
Security authority
SecurityContext
PDP / PEP
runtime / providers
new Capabilities
agents
Sandbox
Resource Governance
Model Governance
RDD Stage 2
receipts de Stage 2+
Ruff
mypy
coverage gates nuevos
matrices amplias de Python/OS
bots de review
caches complejas
auto-fix
auto-approval
auto-merge
auto-deploy
release automation
write access innecesario
```

---

## Invariantes de autoridad

### A1 — Authority permanece humana

La pipeline no puede aprobar, autorizar, promover, mergear ni desplegar.

### A2 — Permisos mínimos

El workflow deberá operar con permisos mínimos y no podrá ampliar sus propios
permisos ni reinterpretar evidencia como autorización.

### A3 — Evidencia no es autoridad

```text
Evidence != Receipt != Validation != Decision != Authority
```

### A4 — Merge permanentemente humano

```text
validation PASS
→ evidence only
→ human reviews
→ human decides
→ human executes merge
```

### A5 — Candidate identity

Toda evidencia terminal debe estar ligada al SHA exacto evaluado. Si el candidato
cambia, la evidencia afectada debe revalidarse.

---

## Cuatro preguntas de ley — admisión inicial

### 1. ¿Respeta el Blueprint?

```text
PASS condicionado
```

La propuesta vive fuera de `src/malak/**`, no introduce nuevas responsabilidades
de runtime y preserva Runtime Independence y Human in Control.

### 2. ¿Respeta la Constitución Cognitiva?

```text
PASS condicionado
```

La propuesta refuerza evidencia, proporcionalidad, minimización y trazabilidad sin
modificar razonamiento, Memory, Knowledge ni comportamiento cognitivo.

### 3. ¿Respeta la Constitución de Gobernanza?

```text
PASS condicionado
```

Solo si los permisos son mínimos, la pipeline es informativa, no existe
self-escalation y merge/approval continúan exclusivamente humanos.

### 4. ¿Mantiene el Kernel simple?

```text
PASS condicionado
```

Guardrail obligatorio:

```text
Kernel delta = 0
src/malak/** delta = 0
runtime delta = 0
authority delta = 0
```

---

## Riesgo

Clasificación inicial:

```text
LEVEL 3 — HIGH
```

Motivo: aunque el runtime delta esperado es cero, la pipeline ejecutará código en
infraestructura externa y producirá evidencia utilizada en la cadena de
validación. Corresponde FULL 4R antes del cierre.

El riesgo no autoriza ampliar scope.

---

## G0 — Admission & Baseline Review

Objetivo:

Demostrar que existe necesidad real, que la alternativa propuesta es la mínima y
que todos los archivos trackeados del repositorio oficial fueron descubiertos y
clasificados sin omisiones silenciosas.

Precondiciones:

```text
main == deb759ee9855737a24b169e03bde2028c7db7f33
RDD Stage 1 integrated
Vault downstream reconciled
no Sprint 7.11 implementation started
```

Evidencia requerida:

- File Coverage Ledger completo;
- roadmap + ideas + concepts revisados;
- Engineering Method + Construction Protocol revisados;
- Blueprint + Constituciones + Architecture Quality Gates revisados;
- Sprint 7.10 revisado;
- tooling/tests/config actual inspeccionado;
- alternativas ADOPT/ADAPT/OBSERVE/REJECT;
- scope y STOP conditions cerrados.

Resultado permitido:

```text
PASS | FAIL | INCONCLUSIVE
```

---

## Gates candidatos posteriores a G0

Estos gates son planificación provisional y no se ejecutan hasta que G0 cierre
`PASS`.

```text
G1 — Validation Contract & Threat Boundary
G2 — Minimal Read-Only Workflow
G3 — Candidate-Bound Validation Semantics
G4 — Negative / Permission / Failure Tests
G5 — Dogfood on exact candidate
G6 — FULL 4R + independent validation + utility closure
```

Cada gate deberá tener scope exacto, candidate identity, checks, STOP y rollback.

---

## STOP conditions globales

```text
requires src/malak/** change
requires Kernel/runtime change
requires Security authority change
requires new external dependency without separate justification
requires write permission not strictly necessary
requires auto-approval / auto-merge / auto-deploy
requires RDD Stage 2
requires workflow to become source of authority
cannot bind evidence to exact candidate
cannot determine result safely
scope exceeds admitted boundary
```

Ante cualquiera:

```text
STOP
→ no ampliar automáticamente
→ registrar evidencia
→ escalar a autoridad humana
```

---

## Rollback

La unidad es aditiva y exterior al runtime.

Rollback absoluto:

```text
deb759ee9855737a24b169e03bde2028c7db7f33
```

Un eventual workflow podrá eliminarse sin migración de datos, cambios de Kernel,
cambios de runtime ni alteración del Security Control Plane.

---

## Estado actual

```text
admission authorization    YES
branch                      CREATED
baseline frozen             YES
G0                          IN PROGRESS
implementation code         NOT STARTED
RDD Stage 2                 NOT AUTHORIZED
merge execution             HUMAN-ONLY
```
