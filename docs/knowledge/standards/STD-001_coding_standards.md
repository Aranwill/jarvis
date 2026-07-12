---
id: STD-001
title: Coding Standards

artifact_type: Standard

status: Published
version: 1.0.0

domain: Development

technologies:
  - Python

tags:
  - Coding
  - Standards
  - Development

related:
  - DOC-AKS-002
  - DOC-AKS-003

author: Hector Rodriguez
reviewed_by:

created_at: 2026-07-09
updated_at: 2026-07-09
---

# Overview

## Purpose

Define the minimum coding standards that every contribution to Malāk must follow.

---

## Scope

These standards apply to all source code incorporated into the project.

---

# Content

## General Principles

- Prioritize readability over cleverness.
- Prefer explicit code over implicit behavior.
- Keep functions focused on a single responsibility.
- Avoid duplicated logic.
- Use meaningful names.
- Favor composition over unnecessary inheritance.
- Write code that is easy to test.

## Documentation

- Public modules should include documentation.
- Complex decisions should be documented in the AKS.
- Every architectural change must be traceable.

## Testing

- New functionality should include corresponding tests.
- Existing tests must continue passing.
- Regressions should be fixed before merging.

---

# Design Considerations

These standards define the minimum engineering quality expected across the project.

Additional standards may be added in future revisions.

---

# Related Artifacts

- DOC-AKS-002
- DOC-AKS-003

---

# References

- Clean Code — Robert C. Martin
- The Pragmatic Programmer

---

# Revision History

| Version | Date | Description |
|----------|------------|----------------|
| 1.0.0 | 2026-07-09 | Initial version |