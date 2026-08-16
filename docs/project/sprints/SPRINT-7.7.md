---
title: Sprint 7.7 — Validación de baseline y release interna
status: activo
authority: documentación operativa derivada
as_of_date: 2026-08-16
as_of_commit: 089255e23bd2b686436140ca569edf09c08819a7
branch: sprint/7.7-baseline-certification
language: es
---

# Sprint 7.7 — Validación de baseline y release interna

## Estado

```text
ACTIVO
```

El Sprint 7.7 fue aprobado explícitamente por el propietario el 2026-08-16.

Su activación no certifica una release ni autoriza automáticamente la promoción
de un nuevo baseline. Cada paquete deberá completarse, validarse y aceptarse
antes del cierre integral.

## Baseline inicial

El sprint comienza desde:

```text
089255e23bd2b686436140ca569edf09c08819a7
```

Rama permanente de origen:

```text
main
```

Rama temporal de trabajo:

```text
sprint/7.7-baseline-certification
```

Estado técnico inicial reproducido localmente:

```text
339 passed
compileall: PASS
git diff --check: PASS
working tree: clean
HEAD == origin/main antes de crear la rama temporal
Python 3.12.10
```

## Objetivo

Verificar de forma integral el código, arquitectura, seguridad, documentación,
trazabilidad y capacidad de rollback del bloque 7.x antes de proponer un nuevo
baseline interno de Malāk.

El producto principal de este sprint no es una nueva feature, sino evidencia
suficiente para determinar si el estado actual puede ser aceptado como un
baseline estable, coherente, reproducible y gobernado.

## Alcance

- Ejecutar la suite completa y las validaciones adicionales aplicables.
- Revisar el Development Checklist y los Architecture Quality Gates.
- Comprobar sincronización entre implementación, Blueprint, ADR, AKS, roadmap
  y documentación operativa.
- Clasificar divergencias como normativas, históricas, derivadas, técnicas o
  de seguridad.
- Revisar seguridad, datos sensibles, autorización, lifecycle y comportamiento
  fail-closed.
- Verificar trazabilidad entre requisitos, contratos, código, tests y
  documentación.
- Preparar evidencia explícita de rollback.
- Revisar versión, changelog y metadatos.
- Determinar mediante revisión final si existe evidencia suficiente para
  proponer un nuevo baseline interno.

## Implementation Packets

### 7.7-A — Baseline Inventory & Evidence Freeze

Objetivo:

- fijar exactamente el estado que será evaluado;
- inventariar código, documentación, configuración, dependencias y evidencia
  relevante;
- evitar que el objeto de certificación cambie silenciosamente durante la
  revisión.

### 7.7-B — Technical Validation

Objetivo:

- reproducir la suite completa;
- validar compilación;
- validar integridad básica del árbol;
- ejecutar checks técnicos aplicables;
- registrar resultados reproducibles asociados al commit evaluado.

### 7.7-C — Architecture & Documentation Reconciliation

Objetivo:

- contrastar la implementación real contra las fuentes arquitectónicas y de
  gobernanza aplicables;
- identificar divergencias;
- comprobar separación de responsabilidades, Runtime Independence, Kernel
  First, Capability First y trazabilidad documental.

### 7.7-D — Security Assurance Review

Objetivo:

- revisar el Security Control Plane y Secure Context Lifecycle implementados;
- comprobar comportamiento fail-closed;
- verificar fronteras entre autenticación, lifecycle, autorización,
  enforcement, auditoría y operación protegida;
- registrar riesgos residuales sin incorporar nuevas capacidades de seguridad
  dentro de este sprint.

### 7.7-E — Release Readiness & Rollback Evidence

Objetivo:

- revisar versión, changelog, metadatos y evidencia de rollback;
- determinar qué commit podría proponerse como baseline;
- comprobar que una eventual promoción sea reversible y trazable.

### 7.7-F — Final Certification Review

Objetivo:

- revisar conjuntamente toda la evidencia de los paquetes anteriores;
- clasificar cualquier divergencia restante;
- determinar si existen blockers;
- producir una recomendación final de certificación o rechazo;
- requerir aprobación humana explícita antes de cualquier promoción.

## Regla de tratamiento de hallazgos

Durante la certificación no se corregirá ninguna divergencia silenciosamente.

Todo hallazgo deberá clasificarse antes de modificar el repositorio.

Clasificaciones mínimas:

```text
BLOCKING
CORRECTIVE_PACKET_REQUIRED
DOCUMENTATION_DIVERGENCE
HISTORICAL_DIVERGENCE
ACCEPTED_RESIDUAL_RISK
NOT_APPLICABLE
```

Una corrección funcional o arquitectónica descubierta durante este sprint
deberá tratarse mediante una unidad de cambio explícita y aprobada antes de
considerar certificable el baseline.

## Fuera de alcance

- Incorporar features nuevas durante la estabilización.
- Introducir agentes, navegación o herramientas externas.
- Implementar nonce, replay protection, PKI o identidad criptográfica.
- Implementar Secure Message Bus o IPC seguro.
- Implementar sandbox.
- Implementar GraphRAG.
- Corregir silenciosamente snapshots históricos.
- Modificar documentos de ley sin una decisión explícita independiente.
- Crear tag, mergear, promover una release o modificar `main` sin autorización
  expresa del propietario.

## Criterios de aceptación

- Alcance de certificación explícito y trazable.
- Todos los paquetes 7.7-A a 7.7-F completados.
- Todas las pruebas y gates aplicables aprobados.
- Documentación coherente con la implementación real.
- Divergencias restantes clasificadas y documentadas.
- Riesgos residuales explícitos.
- Procedimiento de rollback probado o suficientemente demostrado.
- Evidencia asociada al commit evaluado.
- Revisión final completada.
- Aprobación humana explícita antes de cualquier promoción.

## Principios obligatorios

El sprint deberá preservar:

- Blueprint Compliance;
- Cognitive Constitution Compliance;
- Governance Constitution Compliance;
- Kernel First;
- Capability First;
- Runtime Independence;
- Human in Control;
- Zero Trust;
- Defense in Depth;
- denegación por defecto;
- fail-closed;
- trazabilidad;
- reversibilidad;
- sprints y paquetes pequeños, revisables y auditables.

## Riesgo

```text
Level 3 — High
```

El riesgo deriva del carácter de certificación: un falso positivo podría
promover como confiable un estado arquitectónico, documental o técnicamente
inconsistente.

Una suite en verde no sustituye la coherencia arquitectónica, documental y de
seguridad.

## Cierre

El cierre del Sprint 7.7 requerirá una decisión humana explícita.

Completar las validaciones no implica automáticamente:

- certificar el baseline;
- modificar la versión;
- crear un tag;
- actualizar `main`;
- iniciar el siguiente sprint.

## 7.7-A — Baseline Inventory & Evidence Freeze

### Estado

```text
COMPLETADO
```

### Objeto técnico congelado

La certificación evalúa exclusivamente el estado técnico contenido en:

```text
repository: Aranwill/jarvis
branch: main
commit: 089255e23bd2b686436140ca569edf09c08819a7
date: 2026-08-15
```

El commit documental utilizado para activar Sprint 7.7 no forma parte del
objeto técnico bajo certificación.

### Inventario básico

```text
tracked files: 152
nominal version: v0.6.0-alpha
python requirement: >=3.12
runtime dependencies declared in pyproject.toml: none
tag at certified commit: none
```

Estado técnico reproducido antes de iniciar la certificación:

```text
339 passed
compileall: PASS
git diff --check: PASS
working tree: clean
HEAD == origin/main
Python 3.12.10
```

### Fuentes de autoridad y arquitectura identificadas

- `docs/governance/cognitive_constitution.md`
- `docs/governance/governance_constitution.md`
- `docs/architecture/blueprint.md`
- `docs/architecture/kernel.md`
- `docs/architecture/architecture_quality_gates.md`
- `docs/architecture/adr/ADR-001-identity-migration-jarvis-to-malak.md`
- `docs/architecture/adr/ADR-002-policy-enforcement-boundary.md`
- `docs/architecture/adr/ADR-003-directional-communication-and-authority-flow.md`
- `SECURITY.md`

### Hallazgos

#### 7.7-A-001 — Referencia obsoleta a manifest.yaml

```text
classification: DOCUMENTATION_DIVERGENCE
severity: LOW
blocking: NO
```

Evidencia:

- `manifest.yaml` existió históricamente;
- fue actualizado para Malāk durante la migración de identidad;
- fue eliminado explícitamente el 2026-07-20 mediante el commit
  `99adccef66703ddb147ee7a837c4af9bb4e86d5c`;
- el baseline certificado no contiene `manifest.yaml`;
- `docs/project/project_context.md` todavía lo enumera dentro de la estructura
  relevante del repositorio.

Decisión:

No restaurar `manifest.yaml`.

La referencia documental deberá evaluarse y reconciliarse durante
`7.7-C — Architecture & Documentation Reconciliation`.

#### 7.7-A-002 — Migration Status desactualizado en PROJECT.md

```text
classification: DOCUMENTATION_DIVERGENCE
severity: LOW
blocking: NO
```

Evidencia:

`PROJECT.md` mantiene sin marcar, entre otros:

```text
[ ] Source code updated
[ ] Namespaces migrated
```

Sin embargo, `ADR-001 — Identity Migration: Jarvis to Malāk` está aceptado y
documenta que la migración del runtime desde `src/jarvis` hacia `src/malak`
fue completada durante Sprint 5.1 y validada posteriormente.

Decisión:

No modificar `PROJECT.md` durante 7.7-A.

La semántica y vigencia de la checklist deberán reconciliarse durante
`7.7-C — Architecture & Documentation Reconciliation`.

### Resultado de 7.7-A

El objeto técnico de certificación quedó identificado e inmutable por commit.

No se detectaron blockers que impidan continuar con la validación técnica.

Las divergencias encontradas son documentales, de severidad baja y quedan
registradas para tratamiento explícito posterior.

El cierre de 7.7-A no certifica todavía el baseline.

## 7.7-B — Technical Validation

### Estado

```text
COMPLETADO
```

### Candidate baseline validado

Tras la aplicación del corrective packet `7.7-B-C1 — Packaging Boundary & Build Hygiene`,
la validación técnica final se ejecutó sobre:

```text
commit: 34c711c7ecd73fb4187d675e1be6efbeee8c8b3
branch: sprint/7.7-baseline-certification
```

Este commit incorpora únicamente:

- restricción explícita del package discovery a `malak*`;
- exclusión de `/build/` como artefacto generado.

### Evidencia técnica final

```text
Python: 3.12.10
pytest: 339 passed
compileall: PASS
pip check: PASS
isolated wheel build: PASS
wheel package boundary: PASS
unexpected wheel entries: []
build directory ignored: PASS
git diff --check: PASS
working tree: clean
```

### Packaging

El build aislado mediante PEP 517 completó correctamente y produjo un wheel
`malak-0.6.0a0-py3-none-any.whl`.

La validación del contenido confirmó que el artefacto final contiene únicamente:

- `malak/...`
- metadata `malak-*.dist-info/...`

No se detectaron paquetes top-level inesperados.

### Hallazgos investigados

#### 7.7-B-001 — Normalización de versión

```text
classification: NOT_APPLICABLE
blocking: NO
```

`0.6.0-alpha` es normalizado por la metadata Python como `0.6.0a0`.

No requiere corrección.

#### 7.7-B-002 — Backend setuptools ausente en la venv activa

```text
classification: NOT_APPLICABLE
blocking: NO
```

La ausencia de `setuptools` en la venv activa no impide el flujo de build soportado.

El build aislado PEP 517 aprovisionó correctamente el backend declarado por
`pyproject.toml` y produjo el wheel esperado.

#### 7.7-B-003 — Comportamiento de ayuda de la CLI

```text
classification: NOT_APPLICABLE
blocking: NO
```

La CLI es interactiva por diseño. `help` es un comando interno de la sesión y
no un flag `--help`.

No se detectó contradicción con la documentación operativa vigente.

#### 7.7-B-004 — Package discovery demasiado amplio

```text
classification: CORRECTIVE_PACKET_REQUIRED
severity: MEDIUM
blocking_release: YES
status: RESOLVED
```

Durante el build inicial, setuptools incluía `app/main.py` como package top-level
adicional debido al descubrimiento amplio bajo `src/`.

Corrección aplicada mediante `7.7-B-C1`:

```toml
[tool.setuptools.packages.find]
where = ["src"]
include = ["malak*"]
```

Revalidación:

```text
unexpected wheel entries: []
```

#### 7.7-B-005 — Artefacto build/ no ignorado

```text
classification: CORRECTIVE_PACKET_REQUIRED
severity: LOW
blocking_release: YES
status: RESOLVED
```

El build oficial generaba `/build/` como contenido untracked.

Corrección aplicada mediante `7.7-B-C1`:

```text
/build/
```

Revalidación:

```text
git check-ignore: PASS
working tree after build: clean
```

### Corrective Packet 7.7-B-C1

```text
name: Packaging Boundary & Build Hygiene
status: COMPLETED
commit: 34c711c7ecd73fb4187d675e1be6efbeee8c8b3
files:
  - pyproject.toml
  - .gitignore
```

El corrective packet no modificó:

- Kernel;
- runtime behavior;
- Security Control Plane;
- tests funcionales;
- dependencias runtime;
- `src/app/main.py`.

### Resultado de 7.7-B

La validación técnica se considera completada.

No quedan blockers técnicos conocidos dentro del alcance de 7.7-B.

El candidate baseline `34c711c7ecd73fb4187d675e1be6efbeee8c8b3` queda habilitado para continuar
con `7.7-C — Architecture & Documentation Reconciliation`.

El cierre de 7.7-B no certifica todavía el baseline completo.

## 7.7-C-C1 — Derived Documentation Reconciliation

### Estado

```text
COMPLETADO
```

### Aprobación

El corrective packet fue aprobado explícitamente por el propietario el 2026-08-16.

### Objetivo

Reconciliar documentación derivada y metadata operativa con el estado real
observado durante Sprint 7.7, sin modificar arquitectura normativa ni código.

### Alcance autorizado

Archivos modificables:

- `docs/project/project_context.md`
- `docs/project/implementation_roadmap.md`
- `PROJECT.md`
- `docs/project/sprints/SPRINT-7.7.md`

Fuera de alcance:

- `docs/project/roadmap.md`
- `ROADMAP.md`
- Blueprint
- Kernel
- Constitución Cognitiva
- Constitución de Gobernanza
- ADR aceptados
- `SECURITY.md`
- código
- tests

### Hallazgos tratados

#### 7.7-A-001 — Referencia obsoleta a manifest.yaml

```text
classification: DOCUMENTATION_DIVERGENCE
severity: LOW
target_resolution: 7.7-C-C1
```

Se elimina `manifest.yaml` de la estructura vigente descrita por
`project_context.md`. El archivo histórico no se restaura.

#### 7.7-A-002 — Migration Status desactualizado

```text
classification: DOCUMENTATION_DIVERGENCE
severity: LOW
target_resolution: 7.7-C-C1
```

`PROJECT.md` se reconcilia con ADR-001 únicamente en los estados demostrados:
migración del source code y del namespace hacia Malāk.

No se marca `Repository renamed`, porque el repositorio continúa identificado
como `Aranwill/jarvis`.

#### 7.7-C-001 — project_context.md describe Sprint 7.7 como no autorizado

```text
classification: DOCUMENTATION_DIVERGENCE
severity: MEDIUM
target_resolution: 7.7-C-C1
```

El contexto derivado se actualiza para distinguir:

- baseline integrado previo;
- candidate técnico bajo certificación;
- rama temporal de certificación;
- Sprint 7.7 activo;
- ausencia de promoción final de release.

#### 7.7-C-002 — implementation_roadmap.md anclado al estado previo de Sprint 7.6

```text
classification: DOCUMENTATION_DIVERGENCE
severity: MEDIUM
target_resolution: 7.7-C-C1
```

La hoja de ruta derivada registra el estado actual de certificación sin adquirir
autoridad normativa ni aprobar por sí sola una release.

#### 7.7-C-003 — docs/project/roadmap.md legacy

```text
classification: HISTORICAL_DIVERGENCE
severity: LOW
blocking_release: NO
decision: PRESERVE
```

No se modifica. No posee referencias operativas vigentes y se preserva como
artefacto legacy/histórico.

### Restricción de promoción

La aplicación de este corrective packet no certifica el baseline ni autoriza:

- merge;
- push;
- tag;
- cambio de versión;
- inicio del siguiente sprint.

Primero debe revisarse el diff, ejecutar las validaciones aplicables y cerrar
formalmente 7.7-C-C1.

### Validación de 7.7-C-C1

El corrective packet fue aplicado y revisado sobre el commit:

```text
1c787deba94a13128232a20924642ffb8c0f73e8
```

Resultado:

```text
git diff --check: PASS
git show --check: PASS
working tree: clean
scope: 4 archivos documentales autorizados
```

No se modificaron documentos normativos, contratos, código ni tests.

### Resolución de hallazgos

```text
7.7-A-001: RESOLVED
7.7-A-002: RESOLVED
7.7-C-001: RESOLVED
7.7-C-002: RESOLVED
7.7-C-003: ACCEPTED_HISTORICAL / NO_CHANGE
```

### Resultado de 7.7-C

La reconciliación de arquitectura y documentación se considera completada.

Se revisaron las fuentes normativas y operativas aplicables, incluyendo
Constitución Cognitiva, Constitución de Gobernanza, Blueprint, especificación
del Kernel, Architecture Quality Gates, ADR aceptados, Development Checklist,
PROJECT.md, project_context.md y las hojas de ruta aplicables.

No se detectó una divergencia arquitectónica bloqueante entre la
implementación evaluada y las fuentes normativas revisadas.

La documentación derivada desactualizada fue reconciliada mediante
`7.7-C-C1 — Derived Documentation Reconciliation`.

`docs/project/roadmap.md` se preserva sin cambios como artefacto legacy/histórico
y no se considera fuente operativa vigente.

Permanecieron sin cambios:

- Kernel;
- contratos públicos;
- Constitución Cognitiva;
- Constitución de Gobernanza;
- Blueprint;
- ADR aceptados;
- `SECURITY.md`;
- código;
- tests.

El cierre de 7.7-C no certifica todavía el baseline completo ni autoriza merge,
push, tag, promoción de release o inicio del siguiente sprint.

El candidate queda habilitado para continuar con:

```text
7.7-D — Security Assurance Review
```