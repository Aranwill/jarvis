---
id: ADR-001
title: "Identity Migration: Jarvis to Malāk"
status: accepted
date: 2026-07-05
author: Hector Rodriguez
reviewed_by: []
version: 1.0.0
tags:
  - identity
  - migration
  - governance
  - architecture
  - aks
related:
  blueprint: DOC-ARQ-BLUEPRINT
  kernel: DOC-ARQ-KERNEL
  knowledge_model: DOC-ARQ-KNOWLEDGE-MODEL
graph:
  type: architecture_decision
  domain: identity
  affects:
    - project_identity
    - namespace
    - documentation
    - governance
  depends_on:
    - Blueprint
    - Cognitive Constitution
    - Governance Constitution
---

# ADR-001 — Identity Migration: Jarvis → Malāk

## Status

Accepted.

## Context

The project was originally developed under the name Jarvis. During the evolution of the architecture, the project identity was formally changed to Malāk.

This change is not cosmetic only. The project identity must be reflected consistently across the runtime, documentation, governance artifacts, release metadata, and future Architecture Knowledge System.

The migration already started at runtime level by moving the Python namespace from `src/jarvis` to `src/malak`.

## Decision

The project identity is officially migrated from Jarvis to Malāk.

From this ADR onward, all new architecture, governance, development, release, and knowledge artifacts must use Malāk as the canonical project identity.

Legacy references to Jarvis may remain only when they are historically necessary, but they must not be used as the current project identity.

## Rationale

This decision establishes a stable identity for the project before continuing with deeper architectural evolution.

It also prevents fragmentation between runtime names, documentation names, release names, and future knowledge graph entities.

The migration supports the Architecture Knowledge System by creating a clear identity boundary between historical references and the current canonical system.

## Consequences

### Positive

- Establishes Malāk as the canonical project name.
- Aligns runtime namespace, documentation, governance, and release metadata.
- Reduces ambiguity in future ADRs and architecture documents.
- Creates the first formal architectural decision in the AKS.
- Supports future RAG, GraphRAG, and graph database integration.

### Negative / Trade-offs

- Some legacy references to Jarvis may still exist temporarily.
- Documentation cleanup must be progressive and governed.
- Future scripts, tests, and release metadata must be checked for naming consistency.

## Validation Checklist

- Does this decision respect the Blueprint? Yes.
- Does this decision respect the Cognitive Constitution? Yes.
- Does this decision respect the Governance Constitution? Yes.
- Does this decision make the Kernel simpler or more complex? It keeps the Kernel simple.
- Does this decision preserve Runtime Independence? Yes.
- Does this decision preserve Capability First? Yes.
- Does this decision preserve Human in Control? Yes.

## Implementation Notes

The runtime migration from `src/jarvis` to `src/malak` was completed during Sprint 5.1.

The test suite was validated during Sprint 5.2.

This ADR formalizes the architectural and governance decision behind that migration.

## Related Documents

- `docs/architecture/blueprint.md`
- `docs/architecture/kernel.md`
- `docs/architecture/knowledge_model.md`
- `docs/architecture/adr/ADR-TEMPLATE.md`
- `docs/architecture/decisions/decision-index.md`

## History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-05 | Initial ADR created to formalize the identity migration from Jarvis to Malāk. |