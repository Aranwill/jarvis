---
id: GOV-AKS-001
title: Knowledge Governance

artifact_type: Governance

status: Published
version: 1.0.0

domain: Knowledge

technologies: []

tags:
  - AKS
  - Governance
  - Knowledge

related:
  - DOC-AKS-002
  - DOC-AKS-003
  - STD-001

author: Hector Rodriguez
reviewed_by:

created_at: 2026-07-09
updated_at: 2026-07-09
---

# Knowledge Governance

## Purpose

Define the minimum governance rules for the Engineering Knowledge Library.

This document establishes what can enter the AKS, what must remain outside, how artifact status is interpreted, and who decides whether knowledge becomes part of the official project baseline.

---

# What Enters the AKS

The AKS may store curated engineering knowledge such as:

- Architecture documents
- Standards
- Patterns
- Recipes
- Examples
- Technology baselines
- Learning packs
- Glossary entries
- Trusted references
- Governance documents

Knowledge must be useful, reusable, structured, and relevant to the evolution of Malāk.

---

# What Does Not Enter the AKS

The AKS must not store:

- Runtime state
- Raw conversations
- Temporary notes
- Logs
- Secrets
- Credentials
- Generated embeddings
- Vector indexes
- Graph databases
- Unverified external content
- Implementation noise without long-term value

---

# Who Decides

The project owner acts as the final authority for accepting, rejecting, deferring, or archiving AKS artifacts.

Future governance mechanisms may introduce reviewers, automated validation, or approval workflows.

For now, acceptance is manual and explicit.

---

# Trusted Sources

A trusted source is a source that is reliable enough to support engineering decisions.

Examples include:

- Official documentation
- Project source code
- Accepted architecture documents
- Published standards
- Reviewed internal artifacts
- Recognized technical books
- Stable external references

External content must not be treated as trusted by default.

---

# Artifact Status

## Draft

Draft means the artifact is still being evaluated.

A Draft artifact may contain incomplete knowledge, pending review, or early design proposals.

Draft artifacts should not be considered official project baseline.

## Published

Published means the artifact has been accepted as part of the official AKS baseline.

A Published artifact can be used as a reference for implementation, validation, planning, and future retrieval.

---

# Minimum Requirements

Every AKS artifact must:

- Have YAML metadata.
- Have a stable ID.
- Declare its artifact type.
- Declare its status.
- Declare relationships when applicable.
- Follow the official artifact template.
- Be stored in the correct AKS category.

---

# Revision History

| Version | Date | Description |
|----------|------------|----------------|
| 1.0.0 | 2026-07-09 | Initial version |