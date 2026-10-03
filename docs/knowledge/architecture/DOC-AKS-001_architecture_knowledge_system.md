---
id: DOC-AKS-001
title: Architecture Knowledge System

artifact_type: Architecture Document

status: Published
version: 1.0.1

domain: Knowledge Architecture

technologies: []

tags:
  - AKS
  - Architecture
  - Knowledge
  - Documentation

related:
  - DOC-ARQ-BLUEPRINT
  - DOC-ARQ-001
  - DOC-AKS-002
  - DOC-AKS-003

author: Hector Rodriguez
reviewed_by:

created_at: 2026-07-09
updated_at: 2026-10-03
language: es
---

# Architecture Knowledge System

## Propósito

El Architecture Knowledge System, o AKS, es el subsistema de conocimiento
estructurado de Malāk.

Su propósito es preservar conocimiento de arquitectura, ingeniería y gobernanza
de forma legible para humanos, procesable por máquinas, trazable y apta para
futuras capabilities de Retrieval, Validation y GraphRAG.

---

# Alcance

El AKS es responsable de organizar conocimiento curado del proyecto.

Incluye:

- Architecture knowledge;
- Engineering standards;
- Patterns;
- Recipes;
- Examples;
- Technology baselines;
- Learning Packs;
- Glossary entries;
- Trusted references;
- Knowledge metadata;
- Artifact relationships.

El AKS no incluye:

- Runtime memory;
- User conversations;
- Logs;
- Secrets;
- Vector indexes;
- Graph databases;
- Raw external content;
- Temporary notes;
- Generated cache files.

---

# Rol del sistema

El AKS no es el Kernel.

El AKS no es el Runtime.

El AKS no es el Knowledge Manager.

El AKS es la `authoritative knowledge source` que futuras capabilities pueden consumir.

Componentes futuros como Retrieval, GraphRAG, Validation Sandbox y Knowledge
Manager deben consumir artefactos AKS sin cambiar el significado ni la
estructura de los documentos fuente.

---

# Responsabilidades principales

El AKS es responsable de:

- definir artefactos de conocimiento estables;
- preservar trazabilidad arquitectónica;
- favorecer mantenibilidad a largo plazo;
- hacer reutilizable el conocimiento de ingeniería;
- proveer metadata estructurada;
- habilitar futura recuperación automatizada;
- habilitar futuros flujos de validación;
- soportar futura representación de conocimiento basada en grafos.

---

# Componentes del AKS

## Architecture

Define la estructura, los principios y el modelo interno del AKS.

Ejemplos:

- AKS architecture;
- Engineering library specification;
- Artifact taxonomy;
- Metadata model;
- Relationship model.

## Artifact Library

Almacena conocimiento de ingeniería curado.

Ejemplos:

- Standards;
- Patterns;
- Recipes;
- Examples;
- Technologies;
- Learning Packs;
- Glossary entries;
- References.

## Templates

Define estructuras documentales reutilizables para artefactos AKS.

## Governance Integration

La gobernanza del contenido AKS se define fuera de la biblioteca AKS, bajo la
gobernanza del proyecto.

El AKS sigue las reglas de gobernanza, pero no define la gobernanza general de
Malāk.

---

# Relación con la arquitectura de Malāk

El AKS apoya la arquitectura de Malāk preservando conocimiento sobre:

- decisiones de diseño;
- restricciones arquitectónicas;
- estándares de ingeniería;
- patrones aceptados;
- evolución del sistema;
- fundamentos para futuras implementaciones.

El AKS complementa el Blueprint, los ADR y los documentos de gobernanza.

No los reemplaza.

---

# Relación con futuro GraphRAG

Futuras capabilities GraphRAG pueden utilizar el AKS como su fuente curada principal.

Por ello, el AKS debe preservar:

- IDs estables;
- relaciones explícitas;
- consistencia de metadata;
- límites de confianza de las fuentes;
- historial de versiones.

GraphRAG no forma parte de este alcance.

El AKS debe estar preparado para GraphRAG sin implementarlo prematuramente.

---

# Relación con futuro Knowledge Manager

Un futuro Knowledge Manager podrá indexar, validar, buscar o administrar
artefactos AKS.

El Knowledge Manager será un componente de implementación.

El AKS permanece como capa de conocimiento fuente.

Esta separación evita que la lógica de implementación modifique el significado
del conocimiento curado.

---

# Principios de diseño

El AKS sigue estos principios:

- arquitectura antes que automatización;
- legible por humanos primero;
- procesable por máquinas por diseño;
- identificadores estables;
- relaciones explícitas;
- conocimiento versionado;
- separación entre conocimiento fuente e índices generados;
- sólo conocimiento curado;
- evolución incremental;
- sin contenido hostil crudo por defecto.

---

# Baseline actual

El baseline actual del AKS incluye:

- una estructura de carpetas definida;
- un template general de artefacto;
- categorías iniciales de artefactos;
- artefactos iniciales de conocimiento de ingeniería;
- documentos iniciales de arquitectura.

Este baseline es intencionalmente mínimo.

Prepara a Malāk para futuras capabilities de conocimiento sin implementar
GraphRAG, Retrieval, Knowledge Manager ni Validation Sandbox durante este sprint.

---

# Historial de revisiones

| Versión | Fecha | Descripción |
|---|---|---|
| 1.0.0 | 2026-07-09 | Baseline inicial de arquitectura AKS. |
| 1.0.1 | 2026-10-03 | Normalización del contenido explicativo al español, preservando términos técnicos canónicos en su idioma original. |
