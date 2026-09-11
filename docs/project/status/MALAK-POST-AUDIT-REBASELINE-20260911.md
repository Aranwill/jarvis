---
title: Malāk Post-Audit Rebaseline — 2026-09-11
status: derived_current_state
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
implementation_authorized: false
sprint_7_12_authorized: false
rdd_stage_2_authorized: false
---

# Malāk Post-Audit Rebaseline — 2026-09-11

## 1. Propósito

Este documento registra el estado derivado observado inmediatamente después del cierre de los fixes asociados a la auditoría `ASTRA-AUDIT-BASELINE-20260910-A1`.

Su función es eliminar ambigüedad entre el baseline documental previo y el estado efectivo de los tres repositorios después de integrar los fixes y completar la reconciliación del Vault.

Este documento es informativo y no normativo.

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

El cierre operativo observado conserva los tres repositorios en `main`, sin PR abiertos en `Aranwill/jarvis` al momento de esta reconciliación.

---

## 3. Disposición del drift documental previo

Documentos derivados como:

```text
docs/project/project_context.md
docs/project/implementation_roadmap.md
```

conservan metadata y narrativa fechadas antes de la integración final de los fixes de auditoría.

En particular, referencias que todavía indiquen que el Vault representa únicamente el estado post-PR #92 o que los cambios desde PR #93 permanecen pendientes de reconciliación downstream deben considerarse **históricas/stale respecto del estado operativo actual**.

El estado observado post-auditoría es:

```text
Malāk main@5865da6a5e502fe71e35e2e38bc4cceaab9b3600
        ↓
Vault reconciliado en
main@34f0416a8d312f4f27b9b36c3733cc2703772364
        ↓
Sync Agent estable en
main@f6eb42715dd7771f3bcf7909a99f7e4e7db465c1
```

Por tanto:

```text
post-PR #92 vault state
!=
current vault state
```

Este documento no reescribe snapshots históricos ni concede autoridad al Vault sobre el repositorio oficial.

---

## 4. Estado funcional preservado

El último sprint numerado integrado continúa siendo:

```text
Sprint 7.11 — Reproducible Validation Pipeline Foundation
```

La última ruta conversacional/runtime integrada continúa siendo:

```text
Sprint 7.10 — Conversation Session Isolation Foundation
```

La cadena episódica aislada materializada continúa alcanzando:

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

Las propiedades de separación permanecen:

```text
Projection READY != Admission ELIGIBLE
Admission ELIGIBLE != Persistence Authorization
Consumption EVALUATED != Stored
Evidence != Authority
Generation != Finalization
```

---

## 5. Estado de autoridad

Este rebaseline NO autoriza:

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

## 6. Próximo gate recomendado

Con el baseline técnico y documental post-auditoría estabilizado, la siguiente frontera candidata puede analizarse de forma independiente.

La dirección recomendada es:

```text
Progressive Cognitive Assurance runtime
```

pero únicamente después de congelar un alcance explícito, revisar dependencias e invariantes y obtener aprobación inequívoca del Owner.

Candidate Content Identity G2 permanece como frontera posterior independiente y no queda subsumida por este trabajo.

---

## 7. Deuda de gobernanza de infraestructura observada

Los repositorios observados no presentan branch protection activa sobre `main` en la evidencia GitHub consultada.

Esto no invalida las integraciones existentes, que se realizaron mediante PR + CI, pero deja una diferencia entre:

```text
procedural discipline
!=
platform-enforced branch governance
```

La activación de reglas de protección/rulesets debe tratarse como una mejora de gobernanza de infraestructura independiente, sin confundirse con una capability o un cambio cognitivo de Malāk.

---

## 8. Cierre

El baseline post-auditoría queda descrito como:

```text
three repositories stable
main heads identified
CI/Validation successful
Vault reconciled to current Malāk HEAD
no Sprint 7.12 authorized
no runtime assurance implementation authorized
ready for next explicit gate
```

Este documento debe utilizarse como referencia derivada de estado hasta que `project_context.md` e `implementation_roadmap.md` sean reconciliados de forma integral contra un baseline posterior.
