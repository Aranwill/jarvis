---
title: Malāk CAL-014 — Decision Index ADR-006 Candidate Patch
status: gate_candidate
authority: non_normative_patch_candidate
language: es
as_of_date: 2026-09-13
source_baseline: b61c2764b708bf96ca3829e5a9959a0c5e53ad2c
target_path: docs/architecture/decisions/decision-index.md
target_blob: 9d3c12a80adfbbca5bb9cdb6c90c933dab19c427
adr_acceptance_authorized: false
normative_activation_authorized: false
law_materialization_authorized: false
owner_local_materialization_required: true
related:
  - docs/project/sprints/proposals/MALAK-CAL-014-NORMATIVE-PROMOTION-SCOPE-FREEZE.md
  - docs/project/sprints/proposals/MALAK-CAL-014-ADR-006-CANDIDATE.md
  - docs/architecture/decisions/decision-index.md
---

# Malāk CAL-014 — Decision Index ADR-006 Candidate Patch

## 1. Propósito

Preservar el delta exacto del Decision Index que solo podrá aplicarse después de
una aceptación humana explícita de ADR-006.

```text
ADR candidate != Accepted ADR
Accepted ADR required before index mutation
index entry != authority
```

## 2. Precondición exacta

El patch solo puede aplicarse si:

```text
target blob = 9d3c12a80adfbbca5bb9cdb6c90c933dab19c427
Total ADRs = 5
Accepted = 5
ADR-006 has been explicitly accepted by Owner
```

Si ADR-006 permanece `Proposed`, este patch NO se aplica.

## 3. Hunks permitidos

### DI-N1 — primera tabla

Después de:

```text
| ADR-005 | Accepted | 2026-09-10 | Evidence-Bound Final Response Transition | Architecture / Cognition |
```

añadir:

```text
| ADR-006 | Accepted | <activation-date> | Protected Durable Reliance Preconditions | Architecture / Cognition / Memory |
```

### DI-N2 — segunda tabla

Después de:

```text
| ADR-005 | Evidence-Bound Final Response Transition | Accepted | 2026-09-10 | Architecture |
```

añadir:

```text
| ADR-006 | Protected Durable Reliance Preconditions | Accepted | <activation-date> | Architecture |
```

### DI-M1 — Total ADRs

Reemplazar:

```text
Total ADRs: 5
```

por:

```text
Total ADRs: 6
```

### DI-M2 — Accepted

Reemplazar:

```text
Accepted: 5
```

por:

```text
Accepted: 6
```

## 4. Invariantes

Deben permanecer sin cambios:

```text
ADR-001..ADR-005 rows
Superseded: 0
Deprecated: 0
Draft: 0
all previous dates/titles/domains
```

## 5. Stop conditions

Detener si:

- ADR-006 no fue aceptada humanamente;
- el target blob cambió;
- ADR-006 ya aparece en cualquiera de las tablas;
- otra ADR ocupó el identificador ADR-006;
- se requiere modificar una ADR previa o cualquier otra estadística;
- se intenta usar el índice como sustituto de la decisión arquitectónica.

No autoriza modificación remota del Decision Index. El Owner deberá aplicar los
hunks localmente después de aceptar ADR-006 y validar el candidate completo.
