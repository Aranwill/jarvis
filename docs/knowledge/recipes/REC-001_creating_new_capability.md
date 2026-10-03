---
id: REC-001
title: Creating a New Capability

artifact_type: Recipe

status: Published
version: 1.0.1

domain: Development

technologies:
  - Python

tags:
  - Capability
  - Recipe

related:
  - STD-001

author: Hector Rodriguez
reviewed_by:

created_at: 2026-07-09
updated_at: 2026-10-03
language: es
---

# Descripción general

## Propósito

Proporcionar un proceso repetible para introducir una nueva capability en
Malāk.

---

## Alcance

Aplica siempre que se agregue una nueva capability al sistema.

---

# Contenido

1. Definir la responsabilidad de la capability.
2. Crear el package de implementación.
3. Registrar la capability.
4. Implementar tests unitarios.
5. Actualizar el Architecture Knowledge System si se generó conocimiento
   arquitectónico.
6. Validar la test suite completa.
7. Actualizar la documentación del proyecto cuando corresponda.

---

# Consideraciones de diseño

Las capabilities deberían permanecer independientes y respetar los contratos del
Kernel.

---

# Artefactos relacionados

- STD-001

---

# Referencias

- Blueprint
- Development Checklist

---

# Historial de revisiones

| Versión | Fecha | Descripción |
|---|---|---|
| 1.0.0 | 2026-07-09 | Versión inicial. |
| 1.0.1 | 2026-10-03 | Normalización del contenido explicativo al español, preservando términos técnicos canónicos en su idioma original. |
