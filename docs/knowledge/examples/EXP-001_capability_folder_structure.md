---
id: EXP-001
title: Capability Folder Structure

artifact_type: Example

status: Published
version: 1.0.0

domain: Development

technologies:
  - Python

tags:
  - Capability
  - Example
  - Project Structure

related:
  - STD-001
  - REC-001

author: Hector Rodriguez
reviewed_by:

created_at: 2026-07-09
updated_at: 2026-07-09
---

# Overview

## Purpose

Provide a reference folder structure for implementing new capabilities in Malāk.

---

## Scope

This example illustrates the recommended organization for a capability package.

---

# Content

Example:

```text
capabilities/
└── my_capability/
    ├── __init__.py
    ├── capability.py
    ├── contracts.py
    ├── exceptions.py
    └── tests/
```

The structure may evolve over time, but should preserve separation of responsibilities and maintain consistency across capabilities.

---

# Design Considerations

The goal is consistency, not rigidity. Additional files may be introduced when justified by the capability's complexity.

---

# Related Artifacts

- STD-001
- REC-001

---

# References

- Project Blueprint
- Development Checklist

---

# Revision History

| Version | Date | Description |
|----------|------------|----------------|
| 1.0.0 | 2026-07-09 | Initial version |