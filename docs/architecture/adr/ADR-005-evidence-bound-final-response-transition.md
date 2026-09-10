---
id: ADR-005
title: Evidence-Bound Final Response Transition
status: accepted
date: 2026-09-10
author: Hector Rodriguez
reviewed_by: ChatGPT
version: 0.6.0-alpha

tags:
  - architecture
  - decision
  - cognition
  - assurance
  - evidence

related:
  - DOC-ARQ-BLUEPRINT
  - DOC-GOV-COGNITIVE-CONSTITUTION
  - docs/project/sprints/proposals/MALAK-COGNITIVE-ASSURANCE-CONSTITUTIONAL-IMPACT-G0-G1.md
  - docs/project/sprints/proposals/MALAK-COGNITIVE-ASSURANCE-NORMATIVE-PROMOTION-SCOPE-FREEZE.md

affects:
  - Blueprint
  - Cognitive Constitution
  - Final Response transition

depends_on:
  - ADR-003
  - ADR-004
  - Cognitive Constitution
  - Governance Constitution
  - Blueprint

supersedes: null
superseded_by: null

graph:
  node_type: ArchitectureDecision
  priority: High
---

# ADR-005 — Evidence-Bound Final Response Transition

## Estado

Accepted

ADR-005 fue aceptada explícitamente por el Owner el 2026-09-10 mediante
el gate humano de activación normativa. La aceptación de esta decisión no
constituye autorización para implementar runtime.

```text
Proposal != Acceptance != Implementation != Authority
```

---

## Contexto

Malāk ya establece en su Cognitive Constitution principios de no asumir,
evidencia sobre especulación, transparencia, proporcionalidad, minimización,
trazabilidad, coherencia y consistencia temporal.

El Blueprint vigente agrega Human in Control, Zero Trust, Model Agnostic,
observabilidad/auditabilidad, Runtime Independence, retorno de evidencia sin
transferencia de autoridad y prohibición de bypass de capas de validación.

La investigación y el diseño de Cognitive Assurance integrados durante PR #97 a
#101 identificaron un gap más específico: la arquitectura aún no expresa de forma
inequívoca que un output generado o recuperado sea solamente información,
evidencia, observación o candidate según su naturaleza, y que la transición a
Final Response de una respuesta material deba quedar protegida por el assurance
cognitivo aplicable.

El Constitutional Impact Review G0/G1 redujo quince leyes conceptuales a un delta
normativo mínimo de dos principios candidatos:

```text
Generation != Finalization

Material Final Response
requires applicable Evidence-Bound Assurance
before finalization
```

El mismo review rechazó convertir esta necesidad en una obligación de crear una
nueva layer/service/manager y mantuvo algoritmos, budgets, providers, outcomes y
ranking exacto fuera de Constitución.

---

## Decisión

Malāk adopta las siguientes propiedades arquitectónicas
permanentes.

### 1. Generación y recuperación no finalizan una respuesta

Los outputs provenientes de:

- modelos LLM locales;
- modelos frontera conectados;
- providers;
- agents;
- tools;
- retrieval/RAG;
- Memory;
- Knowledge;
- otras capacidades cognitivas autorizadas;

serán tratados según su naturaleza como información, observación, evidencia,
inferencia o candidate.

No adquirirán por sí mismos estado de Final Response, verdad, permiso o autoridad
por el solo hecho de haber sido generados, recuperados o emitidos.

```text
Generation != Finalization
Retrieved != Finalized
Candidate != Accepted Response
Evidence != Authority
```

### 2. La transición Candidate Response → Final Response es protegida

Cuando una respuesta contenga afirmaciones materiales, la transición hacia Final
Response deberá satisfacer las validaciones cognitivas aplicables a su riesgo,
evidencia, incertidumbre y políticas vigentes.

Las afirmaciones materiales que dependan de evidencia deberán poder justificar su
soporte con granularidad proporcional al riesgo.

Si una validación aplicable no puede satisfacerse, la finalización deberá reflejar
el déficit mediante limitación, cualificación, solicitud de evidencia adicional,
abstención o bloqueo según la policy vigente.

Ningún modelo, provider, agent, tool o componente downstream podrá omitir una
validación aplicable y elevar directamente su output a Final Response.

### 3. Assurance progresivo, no pipeline fijo

La decisión no obliga a ejecutar el mismo costo cognitivo para todas las
interacciones.

Las verificaciones deben ser proporcionales al riesgo y materialidad, y deben
preferir controles deterministas cuando estos sean suficientes.

El uso de retrieval adicional, verificadores, múltiples modelos u otras
capacidades queda permitido solamente cuando una policy/specification futura lo
justifique y lo autorice.

### 4. La propiedad no crea un componente por sí misma

```text
constitutional requirement
!= automatic new layer/service/manager
```

ADR-005 no decide todavía si la transición protegida será materializada mediante
un contrato, una policy boundary, una responsabilidad de un componente existente
o un componente dedicado.

Ese ownership deberá definirse únicamente si una specification posterior demuestra
que una responsabilidad real no puede expresarse limpiamente mediante fronteras
existentes.

---

## Alternativas consideradas

### A. No realizar ningún cambio normativo

Rechazada como dirección candidata.

Los principios actuales reducen alucinación y exigen evidencia, pero no expresan
de forma suficientemente inequívoca la separación entre generación y
finalización ni la protección de la transición a Final Response.

### B. Promover las quince CAL como quince nuevas leyes

Rechazada.

Duplicaría obligaciones ya existentes, ampliaría innecesariamente la superficie
constitucional y mezclaría mecanismos de policy con ley permanente.

### C. Crear inmediatamente un `Response Assurance Layer` o servicio dedicado

Rechazada.

La necesidad demostrada es una propiedad arquitectónica, no evidencia suficiente
de que haga falta un nuevo componente.

### D. Ejecutar siempre múltiples modelos/jueces antes de responder

Rechazada como default.

Aumenta costo y latencia sin demostrar que toda interacción requiere ese nivel de
assurance. El diseño seleccionado es progresivo y deficit-driven.

### E. Selección basada en un único score global

Rechazada como requisito arquitectónico.

Un score único puede mezclar autoridad, evidencia, confianza, costo y estilo y
crear falsa precisión. El mecanismo exacto de ranking pertenece a policy o
specification versionada.

---

## Consecuencias

### Positivas

- refuerza la frontera entre workers probabilísticos y decisión final gobernada;
- reduce caminos por los que un output no respaldado puede llegar como hecho
  aceptado;
- mantiene independencia de modelos, providers, lenguajes e infraestructura;
- permite gastar más recursos cuando aporten valor sin volverlos obligatorios en
  todos los casos;
- mantiene el assurance auditable sin convertir evidencia en autoridad;
- preserva la posibilidad de abstención o respuesta limitada cuando el soporte no
  alcanza el floor requerido;
- permite futura mecanización de invariantes objetivas de no-bypass.

### Negativas

- una futura implementación agregará costo de evaluación en respuestas
  materiales;
- algunas respuestas podrán tener mayor latencia cuando requieran escalación;
- el sistema necesitará policies versionadas para determinar assurance suficiente;
- será necesario medir falsos abstentions además de escapes de claims no soportados.

### Riesgos

- sobreingeniería si se interpreta la propiedad como obligación de crear nuevas
  capas o servicios;
- falsa precisión si ranking/confidence se comprimen prematuramente en un score;
- aumento de costo si verification multi-model se vuelve always-on;
- degradación silenciosa si recursos insuficientes rebajan el assurance floor;
- falsa sensación de verdad absoluta si un receipt o verifier se trata como
  autoridad.

Mitigación:

```text
bounded + deterministic change
progressive assurance
explicit degradation
Evidence != Authority
Receipt != Authority
```

---

## Impacto arquitectónico

El impacto normativo mínimo es:

```text
Blueprint
→ nueva regla R-022: Protected Final Response Transition

Cognitive Constitution
→ máximo dos nuevos principios + aclaraciones acotadas

Governance Constitution
→ sin cambios

Kernel
→ sin cambios por ADR-005

Runtime / src / tests
→ sin cambios por este paquete normativo
```

La decisión no altera el flujo de autoridad definido por ADR-003 ni la regla
Specification & Verification First de ADR-004.

---

## Relación con Gobernanza

- Human in Control permanece intacto.
- Evidence, receipts, reviewers y modelos no reciben autoridad adicional.
- El no-bypass de R-021 se extiende conceptualmente a la transición de respuesta
  final cuando exista assurance aplicable.
- La ejecución concreta deberá respetar Zero Trust y políticas de privacidad,
  seguridad y recursos.
- La falta de recursos puede cambiar la estrategia de ejecución, no falsificar que
  un assurance requirement fue satisfecho.

---

## Compatibilidad con AKS / GraphRAG

ADR-005 puede representarse como una decisión arquitectónica relacionada con:

```text
Cognitive Constitution
Blueprint
Evidence-Bound Cognition
Progressive Cognitive Assurance
ADR-003
ADR-004
```

No exige GraphRAG ni AKS operativo. La representación estructurada futura deberá
preservar su status y relaciones sin convertirlas en autoridad ejecutable.

---

## Fuera de alcance

ADR-005 no decide ni autoriza:

```text
A0/A1/A2/A3 como API
ACCEPT/QUALIFY/ABSTAIN/BLOCK como enum runtime
ranking algorithm
weights / thresholds
number of sources
number of model calls
providers concretos
GraphRAG
RAG implementation
persistent Memory
Persistence Authorization
Candidate Content Identity G2
content identity propagation
Cognitive Receipt schema
Resource Governance implementation
RDD Stage 2
Sprint 7.12
```

`CAL-014 — Source Identity and Content Integrity before Durable Reliance` continúa
diferida hasta existir Content Identity y binding end-to-end suficiente.

---

## Estado de activación

ADR-005 fue aceptada explícitamente por el Owner el 2026-09-10 mediante
el gate humano de activación normativa.

La aceptación se realiza conjuntamente con:

- Blueprint v0.6.2-alpha;
- Cognitive Constitution v1.1.0;
- la indexación correspondiente en Decision Index.

Esta aceptación activa únicamente la decisión normativa descrita en este ADR.

No autoriza por sí misma:

- implementación runtime;
- Candidate Content Identity G2;
- Persistence Authorization;
- RDD Stage 2;
- Sprint 7.12.
