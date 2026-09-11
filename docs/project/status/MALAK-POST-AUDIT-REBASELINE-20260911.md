---
title: Malāk Post-Audit Rebaseline — 2026-09-11
status: superseded_derived_snapshot
authority: non-normative
language: es
as_of_date: 2026-09-11
source_repository: Aranwill/jarvis
source_branch: main
source_commit: 5865da6a5e502fe71e35e2e38bc4cceaab9b3600
vault_repository: Aranwill/malak-project-vault
vault_commit: 34f0416a8d312f4f27b9b36c3733cc2703772364
sync_agent_repository: Aranwill/malak-vault-sync-agent
sync_agent_commit: f6eb42715dd7771f3bcf7909a99f7e4e7db465c1
superseded_by_commit: e45a3e3c0ebf657a513596aa74452413479c05d1
current_state_documents:
  - docs/project/project_context.md
  - docs/project/implementation_roadmap.md
implementation_authorized: false
sprint_7_12_authorized: false
rdd_stage_2_authorized: false
---

# Malāk Post-Audit Rebaseline — 2026-09-11

> [!IMPORTANT]
> Este documento se conserva como **snapshot derivado histórico** del estado
> observado inmediatamente después del cierre de los fixes de
> `ASTRA-AUDIT-BASELINE-20260910-A1`.
>
> Ya no representa el estado operativo actual de Malāk. Para estado vigente y
> planificación derivada deben consultarse `docs/project/project_context.md` y
> `docs/project/implementation_roadmap.md` reconciliados contra un baseline
> posterior.

## 1. Propósito

Este documento registra el estado derivado observado inmediatamente después del cierre de los fixes asociados a la auditoría `ASTRA-AUDIT-BASELINE-20260910-A1`.

Su función fue eliminar ambigüedad entre el baseline documental previo y el estado efectivo de los tres repositorios después de integrar los fixes y completar la reconciliación del Vault.

Este documento es informativo, no normativo y queda preservado como evidencia histórica point-in-time.

No modifica ni reemplaza:

- Cognitive Constitution;
- Governance Constitution;
- Blueprint;
- Kernel Specification;
- ADR aceptados;
- SECURITY.md;
- contratos públicos;
- fichas de sprint aprobadas;
- historial Git.

Ante conflicto, prevalece siempre la fuente de mayor autoridad y la evidencia Git más reciente aplicable.

---

## 2. Estado observado de los repositorios

### Repositorio oficial de Malāk

```text
repository: Aranwill/jarvis
branch: main
HEAD: 5865da6a5e502fe71e35e2e38bc4cceaab9b3600
latest merge: PR #109
change: fix(runtime): acotar payloads del transporte Ollama
Validation on HEAD: success
```

### Malāk Project Vault

```text
repository: Aranwill/malak-project-vault
branch: main
HEAD: 34f0416a8d312f4f27b9b36c3733cc2703772364
latest merge: PR #98
change: docs(vault): synchronize Malak 5865da6a
Validation on HEAD: success
```

### Vault Sync Agent

```text
repository: Aranwill/malak-vault-sync-agent
branch: main
HEAD: f6eb42715dd7771f3bcf7909a99f7e4e7db465c1
latest merge: PR #28
change: docs(assurance): aclarar límite de contenido en reconciliación
CI on HEAD: success
```

El cierre operativo observado conservaba los tres repositorios en `main`, sin PR abiertos en `Aranwill/jarvis` al momento de esta reconciliación.

---

## 3. Disposición del drift documental previo

Documentos derivados como:

```text
docs/project/project_context.md
docs/project/implementation_roadmap.md
```

conservaban metadata y narrativa fechadas antes de la integración final de los fixes de auditoría.

En particular, referencias que todavía indicaban que el Vault representaba únicamente el estado post-PR #92 o que los cambios desde PR #93 permanecían pendientes de reconciliación downstream debían considerarse **históricas/stale respecto del estado operativo observado en este snapshot**.

El estado observado post-auditoría era:

```text
Malāk main@5865da6a5e502fe71e35e2e38bc4cceaab9b3600
        ↓
Vault reconciliado en
main@34f0416a8d312f4f27b9b36c3733cc2703772364
        ↓
Sync Agent estable en
main@f6eb42715dd7771f3bcf7909a99f7e4e7db465c1
```

Por tanto, en ese punto temporal:

```text
post-PR #92 vault state
!=
post-audit reconciled vault state
```

Este documento no reescribe snapshots históricos ni concede autoridad al Vault sobre el repositorio oficial.

---

## 4. Estado funcional preservado

El último sprint numerado integrado continuaba siendo:

```text
Sprint 7.11 — Reproducible Validation Pipeline Foundation
```

La última ruta conversacional/runtime integrada continuaba siendo:

```text
Sprint 7.10 — Conversation Session Isolation Foundation
```

La cadena episódica aislada materializada alcanzaba:

```text
Episodic Memory Admission
        ↓
Assessment Provenance
        ↓
Assessment Producer Authorization
        ↓
Governed Input Projection
        ↓
Governed Projection Consumption
```

Las propiedades de separación permanecían:

```text
Projection READY != Admission ELIGIBLE
Admission ELIGIBLE != Persistence Authorization
Consumption EVALUATED != Stored
Evidence != Authority
Generation != Finalization
```

---

## 5. Estado de autoridad

Este rebaseline NO autorizó:

- Sprint 7.12;
- Progressive Cognitive Assurance runtime;
- Candidate Content Identity G2;
- Persistence Authorization;
- Memory persistente;
- retrieval;
- Knowledge operativo;
- Conversation/runtime wiring de la cadena episódica;
- agentes;
- tools;
- Sandbox;
- navegación;
- RDD Stage 2;
- ampliación de autoridad.

```text
Reconciliation != Authorization
Current State != Next Scope
Evidence != Authority
```

---

## 6. Próximo gate recomendado en ese snapshot

Con el baseline técnico y documental post-auditoría estabilizado, la siguiente frontera candidata podía analizarse de forma independiente.

La dirección recomendada en ese punto era:

```text
Progressive Cognitive Assurance runtime
```

pero únicamente después de congelar un alcance explícito, revisar dependencias e invariantes y obtener aprobación inequívoca del Owner.

Candidate Content Identity G2 permanecía como frontera posterior independiente y no quedaba subsumida por este trabajo.

Esta sección conserva una recomendación histórica; no describe por sí sola el estado de autorización posterior.

---

## 7. Deuda de gobernanza de infraestructura observada

Los repositorios observados no presentaban branch protection activa sobre `main` en la evidencia GitHub consultada.

Esto no invalidaba las integraciones existentes, realizadas mediante PR + CI, pero dejaba una diferencia entre:

```text
procedural discipline
!=
platform-enforced branch governance
```

La activación de reglas de protección/rulesets debía tratarse como una mejora de gobernanza de infraestructura independiente, sin confundirse con una capability o un cambio cognitivo de Malāk.

---

## 8. Cierre histórico

El baseline post-auditoría quedó descrito en ese momento como:

```text
three repositories stable
main heads identified
CI/Validation successful
Vault reconciled to Malāk main@5865da6a
no Sprint 7.12 authorized
no runtime assurance implementation authorized
ready for next explicit gate
```

Este documento queda preservado como referencia derivada histórica del punto `main@5865da6a` y **no debe utilizarse como alias de current state** después de su supersedencia.
