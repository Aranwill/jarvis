---
id: DOC-ARQ-QUALITY-GATES
title: Architecture Quality Gates
status: active
version: 0.6.0-alpha
date: 2026-07-05
author: Hector Rodriguez
reviewed_by: []

tags:
  - architecture
  - governance
  - quality
  - validation
  - aks

related:
  blueprint: DOC-ARQ-BLUEPRINT
  kernel: DOC-ARQ-KERNEL
  knowledge_model: DOC-ARQ-KNOWLEDGE-MODEL
  adr:
    - ADR-001

graph:
  type: architecture_document
  domain: governance

history:
  created: 2026-07-05
  updated: 2026-07-05
---

# Architecture Quality Gates

## Purpose

This document defines the minimum architectural quality requirements that every significant change in Malāk must satisfy before being accepted.

Architecture is considered part of the product and therefore follows the same quality standards as source code.

---

# Gate 1 — Blueprint Compliance

Every architectural change must remain consistent with the current Blueprint.

---

# Gate 2 — Cognitive Constitution Compliance

Changes shall preserve the principles defined in the Cognitive Constitution.

---

# Gate 3 — Governance Constitution Compliance

Changes shall comply with the Governance Constitution.

---

# Gate 4 — Kernel First

The Kernel should remain as small, stable and deterministic as possible.

Any increase in Kernel responsibility requires explicit architectural justification.

---

# Gate 5 — Capability First

New functionality should evolve as a Capability unless a justified exception exists.

---

# Gate 6 — Runtime Independence

Architecture must avoid unnecessary coupling to programming languages, runtimes or specific AI models.

---

# Gate 7 — Human in Control

Critical decisions must always remain auditable and reversible by a human operator.

---

# Gate 8 — Architecture Knowledge System

Every architectural decision that changes the system design must update the AKS.

When applicable:

- ADR
- Decision Index
- Blueprint
- Kernel
- Knowledge Model

must be updated.

---

# Gate 9 — Traceability

Every architectural change should be traceable through:

- Git Commit
- ADR
- Documentation
- Release

---

# Gate 10 — Release Readiness

No release shall be published if the architecture documentation is inconsistent with the implemented system.

---

# Validation Checklist

Before approving an architectural change verify:

- Blueprint updated when necessary.
- Kernel updated when necessary.
- ADR created or updated.
- Decision Index updated.
- Documentation version updated.
- Git history is traceable.
- Architecture remains compatible with the AKS.

