---
title: Sprint 7.6 — Preparación del AKS para GraphRAG
status: borrador preliminar
authority: no normativa
as_of_commit: 71d13fc0ee431b9574fcfb5dbc52baf8cb6e4c4c
language: es
---

# Sprint 7.6 — Preparación del AKS para GraphRAG

## Autoridad y dependencia

Documento derivado y no normativo. No autoriza implementación. Todo cambio al Architecture Knowledge System debe respetar su gobernanza y actualizar sus artefactos mediante el proceso aprobado.

## Objetivo preliminar

Preparar taxonomía, relaciones, metadatos e índices del AKS para una futura representación como grafo, sin implementar GraphRAG.

## Alcance preliminar

- Revisar y consolidar la taxonomía de artefactos.
- Explicitar relaciones entre documentos, decisiones, componentes y versiones.
- Validar metadatos obligatorios y referencias rotas.
- Definir índices estructurados y reglas de consistencia.
- Crear validaciones deterministas y reportes reproducibles.
- Documentar migración y compatibilidad con los artefactos actuales.

## Fuera de alcance

- Implementar GraphRAG, embeddings o una base de grafos.
- Indexar el documento expresamente rechazado.
- Alterar silenciosamente documentos históricos.
- Introducir recuperación autónoma de fuentes externas.
- Convertir documentos derivados en autoridad normativa.

## Criterios preliminares de aceptación

- Taxonomía y relaciones cuentan con propietario y definición inequívoca.
- Los metadatos pueden validarse de forma automatizada y determinista.
- Los errores se informan sin reescribir fuentes automáticamente.
- La trazabilidad histórica se conserva.
- Suite de validación y documentación del AKS actualizadas.

## Riesgo

Riesgo: medio por posibles cambios masivos de metadatos o pérdida de trazabilidad documental.
