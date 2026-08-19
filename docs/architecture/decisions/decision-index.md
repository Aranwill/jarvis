# Architecture Decision Index

Versión: 0.6.0-alpha

Estado: Activo

ID: DOC-ADR-INDEX-001

---

# Objetivo

Este documento constituye el índice oficial de todas las Architecture Decision Records (ADR) del proyecto Malāk.

Su objetivo es proporcionar una vista centralizada de las decisiones arquitectónicas aprobadas, su estado, impacto y relaciones con el resto del conocimiento del proyecto.

No reemplaza a las ADR individuales.

Actúa como punto de entrada para la exploración de la arquitectura.

---

# Convenciones

Todas las ADR deberán:

- poseer un identificador único;
- incluir metadatos YAML;
- mantener trazabilidad histórica;
- declarar relaciones explícitas;
- respetar el Knowledge Model (DOC-ARQ-001).

---

# Estados posibles

- Proposed
- Accepted
- Superseded
- Deprecated
- Rejected

---

# Índice

| ADR | Estado | Fecha | Título | Impacto |
|------|--------|--------|--------|---------|
| ADR-003 | Accepted | 2026-08-15 | Directional Communication and Authority Flow | Architecture / Communication |
| ADR-004 | Accepted | 2026-08-19 | Specification and Verification First | Architecture / Engineering Method |


---

# Relaciones

Este documento mantiene relación directa con:

- DOC-ARQ-001 — Knowledge Model
- Blueprint
- Governance Constitution
- Cognitive Constitution
- Development Checklist

---

# Evolución

Toda nueva ADR aceptada deberá registrarse en este índice.

Ninguna ADR podrá eliminarse.

Las decisiones reemplazadas conservarán su historial mediante los campos:

- supersedes
- superseded_by

La historia arquitectónica del proyecto constituye conocimiento permanente.

# Architecture Decision Index

Este documento mantiene el registro oficial de todas las decisiones arquitectónicas del proyecto Malāk.

Toda ADR aceptada deberá registrarse aquí.

---

| ID | Title | Status | Date | Domain |
|----|-------|--------|------------|------------|
| ADR-001 | Identity Migration: Jarvis → Malāk | Accepted | 2026-07-05 | Identity |
| ADR-002 | Frontera de enforcement entre PDP y operación protegida | Accepted | 2026-07-26 | Security |
| ADR-003 | Directional Communication and Authority Flow | Accepted | 2026-08-15 | Architecture |
| ADR-004 | Specification and Verification First | Accepted | 2026-08-19 | Architecture |


---

## Statistics

Total ADRs: 4

Accepted: 4

Superseded: 0

Deprecated: 0

Draft: 0

---

## Domains

- Architecture
- Identity
- Kernel
- Runtime
- Capability
- Governance
- Memory
- Knowledge
- Security
- Infrastructure
- AI Models

---

## Rules

Every architecture decision must:

- Have a permanent ID.
- Be stored under `docs/architecture/adr`.
- Follow the ADR template.
- Respect the Blueprint.
- Respect the Cognitive Constitution.
- Respect the Governance Constitution.
- Be referenced by future ADRs whenever applicable.
