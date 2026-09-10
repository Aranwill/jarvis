---
title: Malāk Blueprint v0.6.2-alpha — Evidence-Bound Finalization Candidate
status: gate_candidate
authority: blueprint_amendment_candidate
language: es
as_of_date: 2026-09-10
source_baseline: 9aaa57fc831e9329e2154b233c8716062958dcb6
target_document: docs/architecture/blueprint.md
target_current_version: 0.6.1-alpha
target_candidate_version: 0.6.2-alpha
activation_authorized: false
implementation_authorized: false
related:
  - docs/architecture/adr/ADR-005-evidence-bound-final-response-transition.md
  - docs/project/sprints/proposals/MALAK-COGNITIVE-ASSURANCE-NORMATIVE-PROMOTION-SCOPE-FREEZE.md
  - docs/project/sprints/proposals/MALAK-COGNITIVE-ASSURANCE-CONSTITUTIONAL-IMPACT-G0-G1.md
---

# Malāk Blueprint v0.6.2-alpha — Evidence-Bound Finalization Candidate

## 1. Estado

Este documento define el patch normativo candidato exacto para una futura versión
`Blueprint v0.6.2-alpha`.

No modifica `docs/architecture/blueprint.md` y no constituye activación normativa.

```text
candidate patch != active Blueprint != implementation != authority
```

## 2. Baseline objetivo

```text
repository: Aranwill/jarvis
baseline commit: 9aaa57fc831e9329e2154b233c8716062958dcb6
target file: docs/architecture/blueprint.md
current Blueprint version: 0.6.1-alpha
project version: v0.6.0-alpha
```

## 3. Operaciones permitidas exactas

Una futura activación solo podrá aplicar estas siete operaciones sobre el target:

### BP-C1 — frontmatter version

```diff
-version: 0.6.1-alpha
+version: 0.6.2-alpha
```

### BP-C2 — relation to ADR-005

Dentro de `related.adr`, después de `ADR-003`:

```diff
     - ADR-001
     - ADR-003
+    - ADR-005
```

No se elimina ni reemplaza ninguna relación existente.

### BP-C3 — history timestamp

```diff
-history:
-  updated: 2026-08-19
+history:
+  updated: 2026-09-10
```

`history.created` permanece sin cambios.

### BP-C4 — visible Blueprint version

```diff
-**Blueprint Versión:** 0.6.1-alpha
+**Blueprint Versión:** 0.6.2-alpha
```

La línea siguiente permanece exactamente:

```text
**Project Version:** v0.6.0-alpha
```

### BP-C5 — fecha visible de última revisión arquitectónica

```diff
-**Última revisión arquitectónica:** 2026-08-19
+**Última revisión arquitectónica:** 2026-09-10
```

El campo frontmatter `date: 2026-07-05` permanece sin cambios, consistente con el patrón de versionado ya aplicado al Blueprint; la revisión vigente se expresa mediante `history.updated` y esta fecha visible de última revisión.

### BP-C6 — versión visible en Estado del Blueprint

Dentro de `# 13. Estado del Blueprint`:

```diff
-**Blueprint v0.6.1-alpha**
+**Blueprint v0.6.2-alpha**
```

Esta operación evita que un mismo Blueprint activo declare dos versiones vigentes distintas.

### BP-C7 — nueva regla única R-022

Insertar inmediatamente después de `R-021 — Prohibición de bypass y ciclos de control`
y antes de `# 10. Componentes Estratégicos`:

```markdown
## R-022 — Transición protegida hacia Final Response

Los outputs producidos o recuperados por modelos, providers, agentes, tools,
Memory, Knowledge, retrieval u otras capacidades cognitivas constituyen
información, evidencia, observaciones o candidatos según su naturaleza y no se
convierten por sí mismos en una Final Response.

Toda transición de una Candidate Response que contenga afirmaciones materiales
hacia una Final Response deberá atravesar las validaciones cognitivas aplicables
definidas por la Constitución Cognitiva y las policies/specifications vigentes.

Ningún modelo, provider, agente, tool o componente downstream podrá omitir una
validación aplicable y presentar directamente su output como Final Response.

Esta regla define una propiedad arquitectónica y no prescribe por sí misma una
nueva layer, service, manager, provider ni implementación concreta.
```

## 4. Semántica de R-022

R-022 expresa solamente:

```text
source output
→ information/evidence/candidate according to nature
→ NOT automatically Final Response

material Candidate Response
→ applicable cognitive assurance
→ protected finalization transition
→ Final Response
```

Su objetivo es extender al plano de finalización de respuesta propiedades ya
existentes en el Blueprint:

```text
R-019 evidence/results may return upstream
R-020 evidence/results do not transfer authority
R-021 authority/validation bypass is prohibited
```

R-022 no crea una nueva teoría de autoridad.

## 5. Elementos deliberadamente no modificados

El candidate exige que permanezcan sin cambio:

- principios `P-001..P-012`;
- diagrama de Arquitectura General;
- lista de capas;
- ownership de Interface, Context, Governance, Kernel, Planning, Reasoning,
  Memory, Knowledge y Execution;
- flujo general existente;
- reglas `R-001..R-021`;
- Componentes Estratégicos;
- restricciones existentes;
- Project Version `v0.6.0-alpha`;
- Kernel Specification;
- Governance Constitution.

## 6. Lo que R-022 NO determina

No congela:

```text
ResponseAssuranceService
ResponseAssuranceLayer
CognitiveAssuranceEngine
ownership runtime exacto
A0/A1/A2/A3
outcomes runtime exactos
ranking algorithm
thresholds
budgets
provider/model concreto
RAG implementation
Memory implementation
receipt schema
```

La regla debe poder ser satisfecha por la arquitectura mínima que una futura
specification demuestre necesaria.

## 7. Compatibilidad con adaptabilidad de Malāk

R-022 debe conservar:

```text
Model Agnostic
Runtime Independence
Language/technology independence
Human in Control
Zero Trust
Everything is Observable
Everything is Auditable
```

Los recursos disponibles pueden cambiar la ruta con la que se intenta satisfacer
el assurance requerido; no pueden convertir un gate no satisfecho en un PASS
implícito.

## 8. Condiciones de activación

El patch no podrá aplicarse al Blueprint activo hasta que:

- ADR-005 haya sido aprobada explícitamente por el Owner;
- el amendment de Cognitive Constitution correspondiente haya sido aprobado;
- exista un candidate exacto de activación sobre el HEAD vigente;
- el diff de activación contenga únicamente los hunks definidos aquí más los
  cambios de aceptación/indexación requeridos;
- CI candidate-bound resulte PASS;
- Ready/merge permanezcan humanos.

## 9. Stop conditions

Detener y abrir nueva evaluación si la activación requiere:

- cambiar el diagrama general;
- añadir una nueva capa o componente;
- cambiar ownership existente;
- modificar Kernel o Security;
- definir algoritmos de assurance;
- activar RDD Stage 2;
- activar Candidate Content Identity G2;
- autorizar Persistence Authorization;
- abrir Sprint 7.12.
