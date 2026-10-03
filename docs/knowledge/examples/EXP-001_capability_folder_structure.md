---
id: EXP-001
title: Capability Folder Structure

artifact_type: Example

status: Published
version: 1.0.1

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
updated_at: 2026-10-03
language: es
---

# Descripción general

## Propósito

Proporcionar una estructura de carpetas de referencia para implementar nuevas
capabilities en Malāk.

---

## Alcance

Este ejemplo ilustra la organización recomendada para el package de una
capability.

---

# Contenido

Ejemplo:

```text
capabilities/
└── my_capability/
    ├── __init__.py
    ├── capability.py
    ├── contracts.py
    ├── exceptions.py
    └── tests/
```

La estructura puede evolucionar con el tiempo, pero debería preservar la separación
de responsabilidades y mantener consistencia entre capabilities.

---

# Consideraciones de diseño

El objetivo es la consistencia, no la rigidez. Pueden incorporarse archivos
adicionales cuando la complejidad de la capability lo justifique.

---

# Artefactos relacionados

- STD-001
- REC-001

---

# Referencias

- Project Blueprint
- Development Checklist

---

# Historial de revisiones

| Versión | Fecha | Descripción |
|---|---|---|
| 1.0.0 | 2026-07-09 | Versión inicial. |
| 1.0.1 | 2026-10-03 | Normalización del contenido explicativo al español, preservando términos técnicos canónicos en su idioma original. |
