---
id: GOV-AKS-001
title: Knowledge Governance

artifact_type: Governance

status: Published
version: 1.0.1

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
updated_at: 2026-10-03
language: es
---

# Knowledge Governance

## Propósito

Definir las reglas mínimas de gobernanza para la Engineering Knowledge Library.

Este documento establece qué puede ingresar al AKS, qué debe permanecer fuera,
cómo se interpreta el estado de un artefacto y quién decide si el conocimiento
pasa a formar parte del baseline oficial del proyecto.

---

# Qué ingresa al AKS

El AKS puede almacenar conocimiento de ingeniería curado, como:

- Architecture documents;
- Standards;
- Patterns;
- Recipes;
- Examples;
- Technology baselines;
- Learning Packs;
- Glossary entries;
- Trusted references;
- Governance documents.

El conocimiento debe ser útil, reutilizable, estructurado y relevante para la
evolución de Malāk.

---

# Qué no ingresa al AKS

El AKS no debe almacenar:

- Runtime state;
- Raw conversations;
- Temporary notes;
- Logs;
- Secrets;
- Credentials;
- Generated embeddings;
- Vector indexes;
- Graph databases;
- Unverified external content;
- Implementation noise without long-term value.

---

# Quién decide

El Owner del proyecto actúa como autoridad final para aceptar, rechazar,
diferir o archivar artefactos AKS.

Futuros mecanismos de gobernanza podrán incorporar reviewers, automated
validation o approval workflows.

Por ahora, la aceptación es manual y explícita.

---

# Fuentes confiables

Una fuente confiable es una fuente suficientemente fiable para respaldar decisiones
de ingeniería.

Ejemplos:

- Official documentation;
- Project source code;
- Accepted architecture documents;
- Published standards;
- Reviewed internal artifacts;
- Recognized technical books;
- Stable external references.

El contenido externo no debe tratarse como confiable por defecto.

---

# Estado de los artefactos

## Draft

`Draft` significa que el artefacto todavía está siendo evaluado.

Un artefacto Draft puede contener conocimiento incompleto, revisión pendiente o
propuestas de diseño tempranas.

Los artefactos Draft no deberían considerarse parte del baseline oficial del
proyecto.

## Published

`Published` significa que el artefacto fue aceptado como parte del baseline
oficial del AKS.

Un artefacto Published puede utilizarse como referencia para implementación,
validación, planificación y futura recuperación.

---

# Requisitos mínimos

Todo artefacto AKS debe:

- tener metadata YAML;
- tener un ID estable;
- declarar su tipo de artefacto;
- declarar su estado;
- declarar relaciones cuando corresponda;
- seguir el template oficial de artefactos;
- almacenarse en la categoría AKS correcta.

---

# Historial de revisiones

| Versión | Fecha | Descripción |
|---|---|---|
| 1.0.0 | 2026-07-09 | Versión inicial. |
| 1.0.1 | 2026-10-03 | Normalización del contenido explicativo al español, preservando términos técnicos canónicos en su idioma original. |
