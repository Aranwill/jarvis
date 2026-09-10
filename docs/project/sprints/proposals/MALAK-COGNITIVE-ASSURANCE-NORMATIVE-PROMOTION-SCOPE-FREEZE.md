---
title: Malāk Cognitive Assurance — Normative Promotion Scope Freeze
status: gate_candidate
authority: scope_freeze
language: es
as_of_date: 2026-09-10
source_baseline: 9aaa57fc831e9329e2154b233c8716062958dcb6
implementation_authorized: false
normative_activation_authorized: false
adr_acceptance_authorized: false
rdd_stage_2_authorized: false
candidate_content_identity_g2_authorized: false
sprint_7_12_authorized: false
related:
  - docs/project/sprints/proposals/MALAK-COGNITIVE-ASSURANCE-CONSTITUTIONAL-IMPACT-G0-G1.md
  - docs/governance/cognitive_constitution.md
  - docs/architecture/blueprint.md
  - docs/architecture/adr/ADR-TEMPLATE.md
---

# Malāk Cognitive Assurance — Normative Promotion Scope Freeze

## 1. Propósito

Congelar el perímetro exacto del paquete candidato de promoción normativa de
Evidence-Bound / Progressive Cognitive Assurance antes de redactar cualquier
cambio normativo activo.

```text
scope freeze != normative amendment != ADR acceptance != implementation != authority
```

## 2. Baseline exacto

```text
repository: Aranwill/jarvis
branch: main
commit: 9aaa57fc831e9329e2154b233c8716062958dcb6
```

## 3. Archivos permitidos en esta unidad

La unidad queda limitada exactamente a cuatro archivos NUEVOS:

```text
docs/project/sprints/proposals/MALAK-COGNITIVE-ASSURANCE-NORMATIVE-PROMOTION-SCOPE-FREEZE.md
docs/architecture/adr/ADR-005-evidence-bound-final-response-transition.md
docs/project/sprints/proposals/MALAK-BLUEPRINT-V0.6.2-EVIDENCE-BOUND-FINALIZATION-CANDIDATE.md
docs/project/sprints/proposals/MALAK-COGNITIVE-CONSTITUTION-V1.1-EVIDENCE-BOUND-FINALIZATION-CANDIDATE.md
```

Todo otro archivo queda fuera de alcance.

En particular, deben permanecer byte-for-byte sin modificación en esta unidad:

```text
docs/architecture/blueprint.md
docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
docs/architecture/decisions/decision-index.md
src/**
tests/**
SECURITY.md
AGENTS.md
```

El índice ADR no se modifica porque su regla vigente registra ADR aceptadas; ADR-005
permanece Proposed en este paquete.

## 4. Estado de ADR-005 permitido

ADR-005 puede:

- existir como `status: proposed`;
- describir la decisión candidata y sus consecuencias;
- referenciar el Constitutional Impact Review integrado;
- definir que `Generation != Finalization`;
- definir una transición protegida Candidate Response → Final Response para
  respuestas materiales;
- preservar que una validación aplicable no puede ser bypassada;
- rechazar la creación automática de una nueva layer/service/manager;
- diferir el ownership/runtime exacto a specification posterior.

ADR-005 NO puede:

- declararse Accepted;
- conceder autoridad;
- aprobar un componente runtime;
- fijar provider/model concreto;
- autorizar RAG, persistent Memory, Persistence Authorization, Candidate Content
  Identity G2, RDD Stage 2 o Sprint 7.12.

## 5. Delta Blueprint candidato permitido

El archivo candidato de Blueprint solo puede proponer estas operaciones futuras:

1. `Blueprint v0.6.1-alpha` → `Blueprint v0.6.2-alpha`.
2. Añadir `ADR-005` a `related.adr`.
3. Actualizar `history.updated` a `2026-09-10`.
4. Mantener `Project Version: v0.6.0-alpha` sin cambios.
5. Añadir exactamente una regla nueva después de `R-021`:
   `R-022 — Protected Final Response Transition`.

R-022 puede exigir únicamente:

```text
generation/retrieval result != final response
material Candidate Response
→ applicable cognitive assurance
→ protected finalization transition
→ Final Response
no bypass
```

Queda prohibido en este paquete proponer:

- nueva capa;
- nuevo manager;
- nuevo service;
- cambio al diagrama general;
- cambio de ownership de Reasoning/Interface/Kernel;
- algoritmo, threshold, provider, budget o outcome runtime concreto.

## 6. Delta Cognitive Constitution candidato permitido

El archivo candidato de Constitución solo puede proponer:

### Metadatos

- mantener `frontmatter.version: 0.6.0-alpha`;
- actualizar `date`/`history.updated` a `2026-09-10`;
- añadir `ADR-005` a `related.adr`;
- cambiar la versión constitucional del cuerpo `1.0.0` → `1.1.0`.

### Aclaraciones sobre principios existentes

Solo se permiten aclaraciones acotadas en:

```text
CC-002
CC-003
CC-004
CC-005
CC-006
CC-007
CC-008
CC-009
```

Las aclaraciones deben limitarse a los findings ya aprobados por el Constitutional
Impact Review:

- incertidumbre antes que fabricación;
- best-supported sobre most-probable;
- confidence/consensus/retrieval no equivalen a verdad o suficiencia;
- contradicciones materiales se resuelven o exponen;
- deterministic checks first cuando sean suficientes;
- reconsideración acotada y causalmente ligada a un déficit;
- trazabilidad mediante evidencia/rationale verificable sin exigir private CoT;
- temporalidad, scope y autoridad participan en resolución de evidencia.

### Nuevos principios máximos

Solo pueden proponerse dos nuevos principios:

```text
CC-011 — Separación entre Generación y Finalización
CC-012 — Finalización Vinculada a Evidencia
```

No se permite crear CC adicionales en esta unidad.

## 7. Elementos que deben permanecer fuera de la Constitución

```text
A0/A1/A2/A3 exactos
ACCEPT/QUALIFY/ABSTAIN/BLOCK como API
top-k
número de modelos o fuentes
weights/scores/thresholds
budgets universales
providers/runtimes concretos
GraphRAG
receipt schema
retención de receipts
métricas concretas
resource routing
```

Esos elementos permanecen en specification/policy/configuration futura.

## 8. Dependencia diferida

`CAL-014 — Source Identity and Content Integrity before Durable Reliance` queda
fuera de este paquete.

Motivo:

```text
Candidate Content Identity G2 = NOT AUTHORIZED
end-to-end content binding = NOT DESIGNED
Persistence Authorization = NOT AUTHORIZED
persistent Memory/Knowledge reliance = NOT AUTHORIZED
```

## 9. Stop conditions

La unidad debe detenerse si:

- se requiere modificar un archivo fuera de los cuatro permitidos;
- ADR-005 necesita estado Accepted antes del gate humano;
- el Blueprint requiere una nueva capa/componente para expresar la propiedad;
- la Constitución requiere más de dos nuevos principios;
- aparece necesidad de código/tests/runtime;
- se necesita decidir Content Identity G2, Persistence Authorization o RDD Stage 2;
- el candidate diverge del baseline congelado.

## 10. Gate posterior

La integración de este paquete solo preserva y revisa candidatos normativos.

No activa las nuevas reglas en los documentos de ley vigentes.

Una futura activación deberá requerir autorización separada del Owner y aplicar un
patch exacto, candidate-bound, sobre:

```text
ADR-005 status / aceptación
docs/architecture/blueprint.md
docs/governance/cognitive_constitution.md
docs/architecture/decisions/decision-index.md (solo si ADR-005 es aceptada)
```

sin implementación runtime en el mismo candidate.
