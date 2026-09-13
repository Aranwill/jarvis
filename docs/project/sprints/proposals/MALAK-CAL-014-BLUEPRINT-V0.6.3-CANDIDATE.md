---
title: Malāk CAL-014 — Blueprint v0.6.3 Candidate Patch
status: gate_candidate
authority: non_normative_patch_candidate
language: es
as_of_date: 2026-09-13
source_baseline: b61c2764b708bf96ca3829e5a9959a0c5e53ad2c
target_path: docs/architecture/blueprint.md
target_blob: 9c09b26d040164955e99cc27c362b0e72373dc3f
normative_activation_authorized: false
law_materialization_authorized: false
owner_local_materialization_required: true
implementation_authorized: false
related:
  - docs/project/sprints/proposals/MALAK-CAL-014-NORMATIVE-PROMOTION-SCOPE-FREEZE.md
  - docs/architecture/blueprint.md
  - docs/governance/cognitive_constitution.md
---

# Malāk CAL-014 — Blueprint v0.6.3 Candidate Patch

## 1. Propósito

Preservar el patch exacto candidato para una eventual incorporación de
`R-023 — Transición protegida hacia Reliance Durable` sin modificar remotamente
el Blueprint activo.

```text
candidate patch != architecture activation
candidate patch != implementation authorization
```

## 2. Precondición exacta

El patch solo puede aplicarse si el target local continúa siendo exactamente:

```text
path: docs/architecture/blueprint.md
blob: 9c09b26d040164955e99cc27c362b0e72373dc3f
Blueprint version: 0.6.2-alpha
Project Version: v0.6.0-alpha
```

Si el blob difiere:

```text
STOP
→ refresh baseline
→ re-evaluate hunks
→ revalidate scope freeze
```

## 3. Hunks permitidos

### BP-M1 — frontmatter.version

Reemplazar:

```yaml
version: 0.6.2-alpha
```

por:

```yaml
version: 0.6.3-alpha
```

### BP-M2 — related.adr

Después de `ADR-005`, añadir:

```yaml
    - ADR-006
```

### BP-M3 — history.updated

Reemplazar:

```yaml
  updated: 2026-09-10
```

por:

```yaml
  updated: <activation-date>
```

### BP-M4 — versión visible

Reemplazar:

```text
**Blueprint Versión:** 0.6.2-alpha
```

por:

```text
**Blueprint Versión:** 0.6.3-alpha
```

`**Project Version:** v0.6.0-alpha` permanece sin cambios.

### BP-M5 — última revisión arquitectónica

Reemplazar:

```text
**Última revisión arquitectónica:** 2026-09-10
```

por:

```text
**Última revisión arquitectónica:** <activation-date>
```

### BP-N1 — única regla nueva

Añadir exactamente después de `R-022 — Transición protegida hacia Final Response`
y antes de `# 10. Componentes Estratégicos`:

```markdown
---

## R-023 — Transición protegida hacia Reliance Durable

La retención, almacenamiento, recuperación o admisión previa de material no lo
convierte por sí mismo en fundamento válido para reliance durable.

Toda transición en la que Memory, Knowledge, evidencia externa o un artefacto
derivado pase a ser fundamento material de un efecto durable, o de una decisión
de alto impacto cuya corrección dependa materialmente de ese contenido, deberá
satisfacer las garantías aplicables de identidad, integridad y provenance
definidas por la Constitución Cognitiva y las policies/specifications vigentes.
Las garantías deberán corresponder al material exacto, a la derivación relevante
y al contexto de la transición; no podrán heredarse únicamente por compartir un
identificador lógico, fuente declarada, ubicación de almacenamiento, historial de
admisión o relación de derivación.

Una garantía válida para un artefacto, versión, contexto o momento no se presume
válida para otro. Cuando una garantía material requerida no pueda establecerse o
haya dejado de ser aplicable, la transición deberá fallar de forma cerrada y
limitarse, retenerse o ponerse en cuarentena para revisión, negarse o abstenerse
según la policy aplicable. Retención o cuarentena no equivalen a autorización para
reliance posterior.

Esta regla define una propiedad arquitectónica y no prescribe por sí misma una
nueva layer, service, manager, mecanismo criptográfico, storage technology ni
implementación concreta.
```

### BP-M6 — Estado del Blueprint

En `# 13. Estado del Blueprint`, reemplazar:

```text
**Blueprint v0.6.2-alpha**
```

por:

```text
**Blueprint v0.6.3-alpha**
```

## 4. Invariantes de activación

Deben permanecer sin cambios:

```text
Project Version: v0.6.0-alpha
diagrama general
ownership de capas
Kernel
Memory Layer ownership
Knowledge Layer ownership
R-001..R-022
Governance Constitution
SECURITY.md
```

## 5. Prohibiciones

Este patch no crea ni autoriza:

```text
new layer/service/manager
storage implementation
Persistence Intent
Persistence Authorization
Persistent Memory
retrieval/RAG/Knowledge runtime
RDD Stage 2
Sprint 7.12
```

No autoriza modificación remota del Blueprint. El Owner deberá aplicar cada hunk
localmente y validar el candidate exacto antes de cualquier commit o PR normativa.
