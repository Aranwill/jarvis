---
title: Malāk CAL-014 — Cognitive Constitution v1.2 Candidate Patch
status: gate_candidate
authority: non_normative_patch_candidate
language: es
as_of_date: 2026-09-13
source_baseline: 876fa62819ec511d4f0d2e7ad6e759aa3f275cf9
target_path: docs/governance/cognitive_constitution.md
target_blob: 34ecc6685dd686f9e7143b3547b61ec0d91c7c41
controlling_hardening: docs/project/sprints/proposals/MALAK-CAL-014-NORMATIVE-SCOPE-INTERPRETIVE-HARDENING.md
refreshes_candidate_from_pr: 130
normative_activation_authorized: false
law_materialization_authorized: false
owner_local_materialization_required: true
implementation_authorized: false
related:
  - docs/project/sprints/proposals/MALAK-CAL-014-NORMATIVE-PROMOTION-SCOPE-FREEZE.md
  - docs/project/sprints/proposals/MALAK-CAL-014-NORMATIVE-SCOPE-INTERPRETIVE-HARDENING.md
  - docs/governance/cognitive_constitution.md
  - docs/architecture/blueprint.md
  - docs/architecture/adr/ADR-005-evidence-bound-final-response-transition.md
---

# Malāk CAL-014 — Cognitive Constitution v1.2 Candidate Patch

## 1. Propósito

Preservar el patch exacto candidato, refrescado contra el Interpretive Hardening,
para una eventual activación humana de `CC-013 — Reliance Durable Protegido` sin
modificar remotamente la Constitución Cognitiva activa.

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
→ revalidate Scope Freeze + Interpretive Hardening
```

## 3. Hunks permitidos

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
utilizados como fundamento material de una transición durable, o de una decisión de
alto impacto cuya clasificación deba determinarse mediante reglas gobernadas,
auditables y fail-closed y cuya corrección dependa materialmente de ese contenido,
Malāk deberá satisfacer, proporcionalmente al riesgo y en el momento del reliance,
garantías aplicables y suficientes ligadas al material exacto y a su derivación
relevante sobre identidad de origen o productor cuando dicha identidad sea material
para la corrección, provenance, trust, authority, admissibility o riesgo de la
transición, integridad del contenido y provenance.

La aplicabilidad y suficiencia podrán ser refinadas por rules/policies gobernadas,
pero ninguna policy inferior podrá omitir, rebajar, declarar satisfecha por default
o convertir en opcional una obligación constitucional materialmente aplicable. La
no-aplicabilidad material que elimine una garantía deberá estar gobernada,
justificada y ser reconstructible/auditable bajo criterios superiores aplicables; no
podrá fabricarse por conveniencia, costo, latencia, ausencia de evaluator ni interés
del productor/presentador. La suficiencia no podrá surgir de autoafirmación del
material, de su productor ni del componente que lo presenta. Cuando una obligación
constitucional material sea aplicable y no exista una policy o mecanismo autorizado
capaz de evaluarla, la transición deberá fallar de forma cerrada.

La ausencia o incertidumbre material de clasificación de impacto no podrá
interpretarse como bajo impacto. Cuando dicha incertidumbre pueda alterar la
aplicabilidad de estas garantías, Malāk deberá aplicar las protecciones de alto
impacto o bloquear/escalar la transición según las policies gobernadas aplicables;
nunca degradarla por default.

Estas garantías no son transitivas ni reutilizables por default entre artefactos,
versiones, derivaciones, contextos, propósitos o momentos distintos. Un identificador
lógico, la igualdad de fuente declarada, la mera presencia o recuperación del
material, su admisión o almacenamiento previo, el consenso, la repetición, la
ausencia de contradicciones detectadas o la confianza declarada no sustituyen una
garantía material aplicable. `content integrity != semantic truth`, `provenance !=
trust` y `source identity != authority`.

Cuando una garantía material requerida no pueda establecerse, haya quedado obsoleta
para la transición, no pueda revalidarse cuando corresponda o una no-aplicabilidad
material no pueda justificarse bajo criterios gobernados, no podrá considerarse
implícitamente satisfecha. Malāk deberá impedir la transición, limitar su alcance,
negar o abstenerse según las policies aplicables.

Cualquier retención o quarantine de revisión es un efecto operativo separado y solo
podrá ocurrir cuando exista autorización independiente bajo Governance/policy de
autorización aplicable, sujeta a los controles de Security y a las semantics de
lifecycle de Memory que correspondan. Dicha autorización no concede reliance
posterior sin una nueva evaluación aplicable.

Esta regla no convierte identidad, integridad, provenance, receipts, almacenamiento
ni evidencia en trust o autoridad; no impide retención forense o quarantine
gobernada de material no confiable cuando exista autorización independiente
aplicable; y no prescribe un mecanismo criptográfico, tecnología de almacenamiento
o implementación concreta.
```

No se permite modificar CC-001..CC-012 para materializar CAL-014.

## 4. Invariantes de activación

La activación debe preservar simultáneamente:

```text
CC-001..CC-012 = semánticamente intactos
frontmatter.version = 0.6.0-alpha
Governance Constitution = sin delta
Security constraint/enforcement != operational authority
Memory lifecycle semantics != operational authority
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
policy refinement -> constitutional waiver
conditional applicability -> manufactured non-applicability
unclassified -> low impact
CAL-014 active law -> Persistence Authorization
```

No autoriza modificación remota del target. El Owner deberá aplicar cada hunk
localmente y validar el resultado candidate-bound antes de cualquier commit o PR
normativa.
