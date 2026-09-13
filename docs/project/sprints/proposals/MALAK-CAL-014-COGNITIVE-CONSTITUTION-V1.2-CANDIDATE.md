---
title: Malāk CAL-014 — Cognitive Constitution v1.2 Candidate Patch
status: gate_candidate
authority: non_normative_patch_candidate
language: es
as_of_date: 2026-09-13
source_baseline: b61c2764b708bf96ca3829e5a9959a0c5e53ad2c
target_path: docs/governance/cognitive_constitution.md
target_blob: 34ecc6685dd686f9e7143b3547b61ec0d91c7c41
normative_activation_authorized: false
law_materialization_authorized: false
owner_local_materialization_required: true
implementation_authorized: false
related:
  - docs/project/sprints/proposals/MALAK-CAL-014-NORMATIVE-PROMOTION-SCOPE-FREEZE.md
  - docs/governance/cognitive_constitution.md
  - docs/architecture/blueprint.md
  - docs/architecture/adr/ADR-005-evidence-bound-final-response-transition.md
---

# Malāk CAL-014 — Cognitive Constitution v1.2 Candidate Patch

## 1. Propósito

Preservar el patch exacto candidato para una eventual activación humana de
`CC-013 — Reliance Durable Protegido` sin modificar remotamente la Constitución
Cognitiva activa.

```text
candidate patch != law
candidate patch != activation
technical validation != normative authority
```

## 2. Precondición exacta

El patch solo puede aplicarse si el target local continúa siendo exactamente:

```text
path: docs/governance/cognitive_constitution.md
blob: 34ecc6685dd686f9e7143b3547b61ec0d91c7c41
body version: 1.1.0
```

Si el blob difiere:

```text
STOP
→ refresh baseline
→ re-evaluate hunks
→ revalidate scope freeze
```

## 3. Hunks permitidos

Solo quedan permitidas estas transformaciones:

### CC-M1 — related.adr

Después de `ADR-005`, añadir:

```yaml
    - ADR-006
```

### CC-M2 — fecha de activación

Reemplazar:

```yaml
date: 2026-09-10
```

por:

```yaml
date: <activation-date>
```

### CC-M3 — history.updated

Reemplazar:

```yaml
  updated: 2026-09-10
```

por:

```yaml
  updated: <activation-date>
```

### CC-M4 — versión visible

Reemplazar:

```text
**Versión:** 1.1.0
```

por:

```text
**Versión:** 1.2.0
```

### CC-N1 — único principio nuevo

Añadir exactamente después de `CC-012 — Finalización Vinculada a Evidencia` y
antes de `# 1.4 Gestión de la Incertidumbre`:

```markdown
## CC-013 — Reliance Durable Protegido

Antes de que Memory, Knowledge, evidencia externa o artefactos derivados sean
utilizados como fundamento material de una transición durable, o de una decisión
de alto impacto cuya corrección dependa materialmente de ese contenido, Malāk
deberá satisfacer, proporcionalmente al riesgo y en el momento del reliance,
garantías aplicables y suficientes ligadas al material exacto y a su derivación
relevante sobre identidad de origen o productor cuando corresponda, integridad
del contenido y provenance. La suficiencia será determinada por las reglas y
policies gobernadas aplicables, no por autoafirmación del material, de su productor
ni del componente que lo presenta.

Estas garantías no son transitivas ni reutilizables por default entre artefactos,
versiones, derivaciones, contextos, propósitos o momentos distintos. Un
identificador lógico, la igualdad de fuente declarada, la mera presencia o
recuperación del material, su admisión o almacenamiento previo, el consenso, la
repetición, la ausencia de contradicciones detectadas o la confianza declarada no
sustituyen una garantía material aplicable. `content integrity != semantic truth`,
`provenance != trust` y `source identity != authority`.

Cuando una garantía material requerida no pueda establecerse, no sea aplicable al
material exacto, haya quedado obsoleta para la transición o no pueda revalidarse
cuando corresponda, no podrá considerarse implícitamente satisfecha. Malāk deberá
limitar, retener o poner en cuarentena para revisión, negar o abstenerse según las
políticas aplicables. La retención o cuarentena de revisión no autoriza reliance
posterior sin una nueva evaluación aplicable.

Esta regla no convierte identidad, integridad, provenance, receipts,
almacenamiento ni evidencia en trust o autoridad; no impide retención forense o
cuarentena gobernada de material no confiable; y no prescribe un mecanismo
criptográfico, tecnología de almacenamiento o implementación concreta.

---
```

## 4. Invariantes de activación

La activación debe preservar simultáneamente:

```text
CC-001..CC-012 = semánticamente intactos
frontmatter.version = 0.6.0-alpha
Governance Constitution = sin delta
Security ownership = sin delta
Memory lifecycle = no autorizado por este patch
Persistence Authorization = no autorizado
Persistent Memory = no autorizado
```

## 5. Prohibiciones

Este candidate patch no puede utilizarse para inferir:

```text
stored -> trusted
identity -> trust
integrity -> semantic truth
provenance -> trust
retention permission -> reliance permission
CAL-014 active law -> Persistence Authorization
```

No autoriza modificación remota del target. El Owner deberá aplicar cada hunk
localmente y validar el resultado candidate-bound antes de cualquier commit o PR
normativa.
