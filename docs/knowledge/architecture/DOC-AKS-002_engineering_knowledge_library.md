---
id: DOC-AKS-002
title: Engineering Knowledge Library
artifact_type: Architecture Document
status: Published
version: 1.0.1
author: Hector Rodriguez
reviewed_by:
created_at: 2026-07-09
updated_at: 2026-10-03
language: es

tags:
  - AKS
  - Knowledge
  - Engineering
  - Architecture

related:
  - DOC-ARQ-001
  - GOV-001
---

# Engineering Knowledge Library

## Propósito

La Engineering Knowledge Library extiende el Architecture Knowledge System
(AKS) mediante un repositorio estructurado de conocimiento de ingeniería
reutilizable.

Su objetivo es preservar el conocimiento técnico generado durante la evolución
de Malāk de forma estandarizada, reutilizable y auditable.

La biblioteca está destinada tanto a personas como a futuras capabilities
automatizadas de Retrieval, Validation, GraphRAG y Knowledge Management.

---

# Objetivos

La biblioteca busca:

- centralizar conocimiento de ingeniería;
- promover reutilización en lugar de duplicación;
- preservar decisiones arquitectónicas;
- estandarizar documentación;
- mejorar el onboarding;
- soportar futuros mecanismos de recuperación inteligente;
- servir como `canonical engineering knowledge repository`.

---

# Categorías de artefactos

La biblioteca se organiza en distintas categorías de artefactos de ingeniería.

Ejemplos:

- Standards;
- Patterns;
- Recipes;
- Examples;
- Technologies;
- Learning Packs;
- References;
- Glossary.

Cada artefacto pertenece a una categoría y sigue una estructura común de
metadata.

---

# Estrategia de crecimiento

La Engineering Knowledge Library evolucionará de forma incremental.

Pueden incorporarse nuevos tipos de artefactos sin afectar los documentos
existentes.

Capabilities futuras pueden incluir:

- Semantic search;
- Retrieval;
- Validation;
- GraphRAG;
- Knowledge Manager;
- Relationship discovery;
- Automated indexing.

Estas capabilities permanecen intencionalmente fuera del alcance de este
documento.

---

# Qué NO almacena la biblioteca

La Engineering Knowledge Library no está destinada a almacenar:

- Runtime state;
- User conversations;
- Memory;
- Logs;
- Configuration files;
- Generated embeddings;
- Vector indexes;
- Graph databases;
- Temporary implementation notes.

Sólo pertenece a la biblioteca conocimiento de ingeniería curado.

---

# Relación con futuro GraphRAG

La Engineering Knowledge Library es la `authoritative source of engineering knowledge`.

Futuras capabilities de GraphRAG, Retrieval y Knowledge Manager consumirán
esta biblioteca como su entrada principal sin cambiar su estructura.

Los documentos permanecen legibles por humanos y, al mismo tiempo, utilizables
como artefactos de conocimiento procesables por máquinas.

---

# Principios de diseño

- Human first;
- Machine readable;
- Stable identifiers;
- Incremental evolution;
- Version controlled;
- Explicit relationships;
- Reusable knowledge;
- Architecture before automation.

---

# Historial de revisiones

| Versión | Fecha | Descripción |
|---|---|---|
| 1.0.0 | 2026-07-09 | Versión inicial. |
| 1.0.1 | 2026-10-03 | Normalización del contenido explicativo al español, preservando términos técnicos canónicos en su idioma original. |
