---
id: DOC-AKS-003
title: Engineering Knowledge Artifact Types
artifact_type: Architecture Document
status: Published
version: 1.0.1
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
updated_at: 2026-10-03
language: es
---

# Engineering Knowledge Artifact Types

## Propósito

Este documento define la taxonomía de artefactos utilizada por la Engineering
Knowledge Library.

Cada tipo de artefacto tiene un propósito específico y debería utilizarse de forma
consistente en todo el proyecto.

El objetivo es asegurar que el conocimiento de ingeniería permanezca
estructurado, reutilizable, buscable y fácil de mantener.

---

# Tipos de artefactos

## STD — Standard

### Propósito

Define reglas obligatorias de ingeniería que deben cumplirse.

### Contenido típico

- estándares de código;
- convenciones de nombres;
- reglas de documentación;
- reglas de seguridad;
- restricciones arquitectónicas.

### Usar cuando

La información describe requisitos que toda contribución debe cumplir.

---

## PAT — Pattern

### Propósito

Documenta soluciones reutilizables de arquitectura o diseño.

### Contenido típico

- patrones de diseño;
- patrones de integración;
- patrones arquitectónicos;
- patrones de comunicación.

### Usar cuando

Se espera reutilizar la misma solución en múltiples componentes.

---

## REC — Recipe

### Propósito

Proporciona guías de implementación paso a paso.

### Contenido típico

- documentos how-to;
- procedimientos de deployment;
- guías de configuración;
- flujos de desarrollo.

### Usar cuando

Un proceso repetible necesita ejecutarse de forma consistente.

---

## EXP — Example

### Propósito

Proporciona ejemplos concretos de implementación.

### Contenido típico

- estructuras de carpetas;
- snippets de código;
- ejemplos de API;
- ejemplos de configuración.

### Usar cuando

Mostrar una referencia práctica resulta más efectivo que describirla.

---

## TECH — Technology

### Propósito

Documenta tecnologías adoptadas por el proyecto.

### Contenido típico

- baselines de frameworks;
- evaluaciones de librerías;
- políticas de versiones;
- razones de adopción.

### Usar cuando

El documento explica cómo se utiliza una tecnología dentro de Malāk.

---

## LPK — Learning Pack

### Propósito

Captura material de aprendizaje curado sobre temas de ingeniería.

### Contenido típico

- buenas prácticas;
- resúmenes de libros;
- notas internas de aprendizaje;
- referencias de formación.

### Usar cuando

El objetivo es preservar conocimiento de ingeniería y no definir reglas
obligatorias del proyecto.

---

## REF — Reference

### Propósito

Almacena referencias externas confiables.

### Contenido típico

- RFC;
- documentación oficial;
- estándares;
- papers académicos;
- artículos técnicos.

### Usar cuando

El conocimiento proviene de una fuente externa autoritativa.

---

## GLO — Glossary

### Propósito

Define terminología utilizada en el proyecto.

### Contenido típico

- acrónimos;
- conceptos arquitectónicos;
- terminología de dominio;
- vocabulario interno.

### Usar cuando

Un concepto requiere una definición canónica.

---

# Principios de diseño

Todo artefacto debería:

- tener un identificador estable;
- seguir el template común de metadata;
- declarar relaciones explícitas;
- estar bajo control de versiones;
- poder comprenderse de forma independiente;
- ser reutilizable;
- evitar conocimiento duplicado.

---

# Evolución futura

Podrán incorporarse tipos adicionales a medida que evolucione la Engineering
Knowledge Library.

Los nuevos tipos deben preservar compatibilidad hacia atrás y seguir el mismo
modelo de metadata.

---

# Historial de revisiones

| Versión | Fecha | Descripción |
|---|---|---|
| 1.0.0 | 2026-07-09 | Versión inicial. |
| 1.0.1 | 2026-10-03 | Normalización del contenido explicativo al español, preservando términos técnicos canónicos en su idioma original. |
