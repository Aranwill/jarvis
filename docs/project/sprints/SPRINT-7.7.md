---
title: Sprint 7.7 — Validación de baseline y release interna
status: activo
authority: documentación operativa derivada
as_of_date: 2026-08-16
as_of_commit: 089255e23bd2b686436140ca569edf09c08819a7
branch: sprint/7.7-baseline-certification
language: es
---

# Sprint 7.7 — Validación de baseline y release interna

## Estado

```text
ACTIVO
```

El Sprint 7.7 fue aprobado explícitamente por el propietario el 2026-08-16.

Su activación no certifica una release ni autoriza automáticamente la promoción
de un nuevo baseline. Cada paquete deberá completarse, validarse y aceptarse
antes del cierre integral.

## Baseline inicial

El sprint comienza desde:

```text
089255e23bd2b686436140ca569edf09c08819a7
```

Rama permanente de origen:

```text
main
```

Rama temporal de trabajo:

```text
sprint/7.7-baseline-certification
```

Estado técnico inicial reproducido localmente:

```text
339 passed
compileall: PASS
git diff --check: PASS
working tree: clean
HEAD == origin/main antes de crear la rama temporal
Python 3.12.10
```

## Objetivo

Verificar de forma integral el código, arquitectura, seguridad, documentación,
trazabilidad y capacidad de rollback del bloque 7.x antes de proponer un nuevo
baseline interno de Malāk.

El producto principal de este sprint no es una nueva feature, sino evidencia
suficiente para determinar si el estado actual puede ser aceptado como un
baseline estable, coherente, reproducible y gobernado.

## Alcance

- Ejecutar la suite completa y las validaciones adicionales aplicables.
- Revisar el Development Checklist y los Architecture Quality Gates.
- Comprobar sincronización entre implementación, Blueprint, ADR, AKS, roadmap
  y documentación operativa.
- Clasificar divergencias como normativas, históricas, derivadas, técnicas o
  de seguridad.
- Revisar seguridad, datos sensibles, autorización, lifecycle y comportamiento
  fail-closed.
- Verificar trazabilidad entre requisitos, contratos, código, tests y
  documentación.
- Preparar evidencia explícita de rollback.
- Revisar versión, changelog y metadatos.
- Determinar mediante revisión final si existe evidencia suficiente para
  proponer un nuevo baseline interno.

## Implementation Packets

### 7.7-A — Baseline Inventory & Evidence Freeze

Objetivo:

- fijar exactamente el estado que será evaluado;
- inventariar código, documentación, configuración, dependencias y evidencia
  relevante;
- evitar que el objeto de certificación cambie silenciosamente durante la
  revisión.

### 7.7-B — Technical Validation

Objetivo:

- reproducir la suite completa;
- validar compilación;
- validar integridad básica del árbol;
- ejecutar checks técnicos aplicables;
- registrar resultados reproducibles asociados al commit evaluado.

### 7.7-C — Architecture & Documentation Reconciliation

Objetivo:

- contrastar la implementación real contra las fuentes arquitectónicas y de
  gobernanza aplicables;
- identificar divergencias;
- comprobar separación de responsabilidades, Runtime Independence, Kernel
  First, Capability First y trazabilidad documental.

### 7.7-D — Security Assurance Review

Objetivo:

- revisar el Security Control Plane y Secure Context Lifecycle implementados;
- comprobar comportamiento fail-closed;
- verificar fronteras entre autenticación, lifecycle, autorización,
  enforcement, auditoría y operación protegida;
- registrar riesgos residuales sin incorporar nuevas capacidades de seguridad
  dentro de este sprint.

### 7.7-E — Release Readiness & Rollback Evidence

Objetivo:

- revisar versión, changelog, metadatos y evidencia de rollback;
- determinar qué commit podría proponerse como baseline;
- comprobar que una eventual promoción sea reversible y trazable.

### 7.7-F — Final Certification Review

Objetivo:

- revisar conjuntamente toda la evidencia de los paquetes anteriores;
- clasificar cualquier divergencia restante;
- determinar si existen blockers;
- producir una recomendación final de certificación o rechazo;
- requerir aprobación humana explícita antes de cualquier promoción.

## Regla de tratamiento de hallazgos

Durante la certificación no se corregirá ninguna divergencia silenciosamente.

Todo hallazgo deberá clasificarse antes de modificar el repositorio.

Clasificaciones mínimas:

```text
BLOCKING
CORRECTIVE_PACKET_REQUIRED
DOCUMENTATION_DIVERGENCE
HISTORICAL_DIVERGENCE
ACCEPTED_RESIDUAL_RISK
NOT_APPLICABLE
```

Una corrección funcional o arquitectónica descubierta durante este sprint
deberá tratarse mediante una unidad de cambio explícita y aprobada antes de
considerar certificable el baseline.

## Fuera de alcance

- Incorporar features nuevas durante la estabilización.
- Introducir agentes, navegación o herramientas externas.
- Implementar nonce, replay protection, PKI o identidad criptográfica.
- Implementar Secure Message Bus o IPC seguro.
- Implementar sandbox.
- Implementar GraphRAG.
- Corregir silenciosamente snapshots históricos.
- Modificar documentos de ley sin una decisión explícita independiente.
- Crear tag, mergear, promover una release o modificar `main` sin autorización
  expresa del propietario.

## Criterios de aceptación

- Alcance de certificación explícito y trazable.
- Todos los paquetes 7.7-A a 7.7-F completados.
- Todas las pruebas y gates aplicables aprobados.
- Documentación coherente con la implementación real.
- Divergencias restantes clasificadas y documentadas.
- Riesgos residuales explícitos.
- Procedimiento de rollback probado o suficientemente demostrado.
- Evidencia asociada al commit evaluado.
- Revisión final completada.
- Aprobación humana explícita antes de cualquier promoción.

## Principios obligatorios

El sprint deberá preservar:

- Blueprint Compliance;
- Cognitive Constitution Compliance;
- Governance Constitution Compliance;
- Kernel First;
- Capability First;
- Runtime Independence;
- Human in Control;
- Zero Trust;
- Defense in Depth;
- denegación por defecto;
- fail-closed;
- trazabilidad;
- reversibilidad;
- sprints y paquetes pequeños, revisables y auditables.

## Riesgo

```text
Level 3 — High
```

El riesgo deriva del carácter de certificación: un falso positivo podría
promover como confiable un estado arquitectónico, documental o técnicamente
inconsistente.

Una suite en verde no sustituye la coherencia arquitectónica, documental y de
seguridad.

## Cierre

El cierre del Sprint 7.7 requerirá una decisión humana explícita.

Completar las validaciones no implica automáticamente:

- certificar el baseline;
- modificar la versión;
- crear un tag;
- actualizar `main`;
- iniciar el siguiente sprint.
