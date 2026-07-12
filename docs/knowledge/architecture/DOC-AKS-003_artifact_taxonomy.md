---
id: DOC-AKS-003
title: Engineering Knowledge Artifact Types
artifact_type: Architecture Document
status: Published
version: 1.0.0
domain: Knowledge
technology: AKS
tags:
  - AKS
  - Artifact Types
  - Knowledge
related:
  - DOC-AKS-002
author: Hector Rodriguez
reviewed_by:
created_at: 2026-07-09
updated_at: 2026-07-09
---

# Engineering Knowledge Artifact Types

## Purpose

This document defines the artifact taxonomy used by the Engineering Knowledge Library.

Each artifact type has a specific purpose and should be used consistently throughout the project.

The goal is to ensure that engineering knowledge remains structured, reusable, searchable and easy to maintain.

---

# Artifact Types

## STD — Standard

Purpose

Defines mandatory engineering rules that must be followed.

Typical contents

- Coding standards
- Naming conventions
- Documentation rules
- Security rules
- Architectural constraints

Use when

The information describes requirements that every contributor must follow.

---

## PAT — Pattern

Purpose

Documents reusable architectural or design solutions.

Typical contents

- Design patterns
- Integration patterns
- Architectural patterns
- Communication patterns

Use when

The same solution is expected to be reused across multiple components.

---

## REC — Recipe

Purpose

Provides step-by-step implementation guides.

Typical contents

- How-to documents
- Deployment procedures
- Configuration guides
- Development workflows

Use when

A repeatable process needs to be executed consistently.

---

## EXP — Example

Purpose

Provides concrete implementation examples.

Typical contents

- Folder structures
- Code snippets
- API examples
- Configuration examples

Use when

Showing a practical reference is more effective than describing it.

---

## TECH — Technology

Purpose

Documents technologies adopted by the project.

Typical contents

- Framework baselines
- Library evaluations
- Version policies
- Adoption rationale

Use when

The document explains how a technology is used within Malāk.

---

## LPK — Learning Pack

Purpose

Captures curated learning material for engineering topics.

Typical contents

- Best practices
- Book summaries
- Internal learning notes
- Training references

Use when

The objective is to preserve engineering knowledge rather than define project rules.

---

## REF — Reference

Purpose

Stores trusted external references.

Typical contents

- RFCs
- Official documentation
- Standards
- Academic papers
- Technical articles

Use when

The knowledge originates from an external authoritative source.

---

## GLO — Glossary

Purpose

Defines terminology used across the project.

Typical contents

- Acronyms
- Architectural concepts
- Domain terminology
- Internal vocabulary

Use when

A concept requires a canonical definition.

---

# Design Principles

Every artifact should:

- Have a stable identifier.
- Follow the common metadata template.
- Declare explicit relationships.
- Be version controlled.
- Be independently understandable.
- Be reusable.
- Avoid duplicated knowledge.

---

# Future Evolution

Additional artifact types may be introduced as the Engineering Knowledge Library evolves.

New types must preserve backward compatibility and follow the same metadata model.