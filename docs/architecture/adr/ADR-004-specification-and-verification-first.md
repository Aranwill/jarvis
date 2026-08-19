---
id: ADR-004
title: Specification and Verification First
status: accepted
date: 2026-08-19
author: Hector Rodriguez
reviewed_by:
  - ChatGPT
version: 0.6.0-alpha

tags:
  - architecture
  - engineering
  - specification
  - verification
  - testing

related:
  - DOC-ARQ-BLUEPRINT
  - DOC-ADR-INDEX-001

affects:
  - Architecture
  - Engineering Method

depends_on:
  - Cognitive Constitution
  - Governance Constitution
  - Blueprint

supersedes: null
superseded_by: null

graph:
  node_type: ArchitectureDecision
  priority: High
---

# ADR-004 — Specification and Verification First

## Estado

Accepted

---

## Contexto

Malāk ya dispone de un método de ingeniería que incorpora Specification-Driven Development, Test-Driven Development, revisión proporcional al riesgo, corrección acotada y validación independiente.

También existen criterios de desarrollo que exigen comportamiento esperado, criterios de aceptación verificables, trazabilidad y evidencia antes de considerar terminado un cambio.

Sin embargo, estos mecanismos permanecen definidos principalmente en documentación de desarrollo.

El Blueprint todavía no expresa como principio arquitectónico que una modificación significativa debe definir qué comportamiento se espera y cómo podrá verificarse antes de ser aceptada en el baseline.

Esta decisión incorpora ese principio sin trasladar al Blueprint los detalles operativos de SDD, TDD o del proceso de revisión.

---

## Decisión

Malāk adopta el principio arquitectónico:

**Specification & Verification First**

Toda modificación significativa de Malāk deberá definir su comportamiento esperado y criterios de aceptación verificables antes de ser aceptada en el baseline.

La implementación deberá respaldarse mediante pruebas y evidencia objetiva proporcionales al riesgo.

Las reglas metodológicas detalladas permanecerán en:

`docs/development/engineering_method.md`

La especificación, las pruebas y la evidencia no conceden autoridad ni pueden modificar por sí mismas arquitectura, gobernanza o documentos de ley.

El Blueprint incorporará este principio como `P-012`.

---

## Alternativas consideradas

### Alternativa A — Mantener el principio únicamente en documentación de desarrollo

Rechazada.

Mantendría SDD y TDD como metodología de implementación sin establecer explícitamente su relación con la aceptación arquitectónica del baseline.

### Alternativa B — Incorporar el proceso completo de SDD y TDD dentro del Blueprint

Rechazada.

Introduciría detalle metodológico innecesario dentro del documento maestro de arquitectura y duplicaría responsabilidades ya definidas en el Malāk Engineering Method.

### Alternativa C — Incorporar únicamente el principio arquitectónico y mantener el método separado

Aceptada.

El Blueprint establece la obligación arquitectónica y la documentación de desarrollo conserva el procedimiento detallado.

---

## Consecuencias

### Positivas

- establece comportamiento esperado antes de aceptar cambios significativos;
- exige criterios verificables;
- fortalece la relación entre especificación, implementación, tests y evidencia;
- reduce aceptación de cambios basada únicamente en afirmaciones;
- preserva la separación entre arquitectura y metodología de desarrollo;
- mantiene Human in Control.

### Negativas

- los cambios significativos requieren especificación y evidencia explícitas antes de cierre;
- puede aumentar ligeramente el trabajo documental en cambios de mayor riesgo.

### Riesgos

- sobredocumentar cambios triviales;
- confundir pruebas aprobadas con autoridad para modificar arquitectura;
- trasladar detalles metodológicos al Blueprint.

Estos riesgos se mitigan aplicando controles proporcionales al riesgo y manteniendo el método detallado fuera del Blueprint.

---

## Impacto arquitectónico

La decisión afecta únicamente:

- los principios arquitectónicos del Blueprint;
- la interpretación de aceptación de cambios significativos en el baseline.

No modifica:

- responsabilidades del Kernel;
- flujo de autoridad;
- contratos públicos;
- runtimes;
- providers;
- capabilities;
- Security Control Plane.

---

## Relación con Gobernanza

Esta decisión no concede nueva autoridad.

La especificación, los tests, los resultados de validación y la evidencia pueden informar una decisión de aceptación.

No pueden autorizarse a sí mismos ni modificar documentos de mayor autoridad.

La aprobación final continúa perteneciendo a la autoridad humana correspondiente.

---

## Compatibilidad con AKS / GraphRAG

La decisión puede representarse como un nodo `ArchitectureDecision` relacionado con:

- Blueprint;
- Engineering Method;
- arquitectura;
- validación;
- testing.

Relaciones sugeridas:

```text
ADR-004
  affects -> Blueprint
  affects -> Engineering Method
  establishes -> Specification & Verification First
  reinforces -> Human in Control
  reinforces -> Traceability
