---
title: Malāk Conceptual References
status: active
authority: non_normative
document_role: index
language: es
created: 2026-08-14
---

# Malāk Conceptual References

## Propósito

Esta carpeta conserva documentos conceptuales y referencias de diseño que
pueden orientar futuras evaluaciones de Malāk.

Los documentos contenidos aquí:

- no modifican el baseline vigente;
- no constituyen decisiones arquitectónicas aprobadas;
- no autorizan implementación;
- no autorizan sprints;
- no reemplazan Blueprint, Constitución Cognitiva ni Gobernanza;
- deben revalidarse contra el estado vigente antes de derivar trabajo operativo.

La autoridad continúa determinada por la jerarquía documental oficial del
proyecto.

## Documentos actuales

### Malāk Cognitive Dataset Foundation

Archivo:

`MALAK_COGNITIVE_DATASET_FOUNDATION.md`

Preserva la propuesta conceptual para definir, evaluar y eventualmente adaptar
el comportamiento cognitivo de Malāk.

Principio central:

> Primero definir qué significa pensar y responder como Malāk; después decidir
> si es necesario entrenar un modelo para conseguirlo.

Estado:

`concept / non_normative / working_reference`

### Malāk Evidence-Bound Cognition Foundation

Archivo:

`MALAK_EVIDENCE_BOUND_COGNITION_FOUNDATION.md`

Preserva la dirección conceptual para que outputs probabilísticos, evidencia
recuperada y conocimiento heterogéneo se transformen en respuestas finales
validadas, justificables, rankeadas y cada vez más deterministas.

Principio central:

> Generation != Acceptance != Final Response.

Define leyes cognitivas candidatas, la relación conceptual con RDD y el camino
de promoción ADR → Blueprint → Cognitive Constitution → enforcement, sin
modificar todavía ninguna fuente normativa ni autorizar implementación.

Estado:

`concept / non_normative / conceptual_reference`

### Governed Swarm and Long-Horizon Reference

Archivo:

`GOVERNED_SWARM_LONG_HORIZON_REFERENCE.md`

Preserva el mapeo y evaluación conceptual del material relacionado con:

- agentes gobernados;
- Mission Orchestration;
- trabajo de horizonte largo;
- Completion Contracts;
- Persistent Task State;
- checkpoints;
- Execution Graph;
- Engineering Intelligence;
- Cognitive Core;
- restricciones contra sobreingeniería.

La implementación agentic continúa gobernada principalmente por IDEA-024 y por
las fundaciones relacionadas existentes.

Estado:

`concept / non_normative / conceptual_reference`

### Malāk Research Horizon Map

Archivo:

`MALAK_RESEARCH_HORIZON_MAP.md`

Preserva la reconciliación entre investigación externa, visión futura y
conceptos ya existentes de Malāk, distinguiendo explícitamente entre:

- líneas ya alineadas;
- responsabilidades existentes que necesitan refuerzo;
- gaps conceptuales candidatos;
- tecnologías que solo deben mantenerse bajo observación;
- direcciones incompatibles con la visión de Malāk.

Incluye el mapeo de seguridad y resiliencia relacionado con Prompt/Context Trust,
Memory/Knowledge poisoning, supply chain de AI, identidad y delegación,
contención sistémica de componentes comprometidos, deception/forensics,
interoperabilidad gobernada y evolución controlada.

Además, mantiene el **registro canónico de evidencia externa validada** usada por
esta capa conceptual. Los demás documentos no normativos deben referenciar ese
mapa en lugar de duplicar catálogos de fuentes, salvo que una especificación o
revisión concreta necesite preservar evidencia propia del candidato evaluado.

La presencia de una fuente externa en el mapa demuestra únicamente que fue
revisada y clasificada por aplicabilidad. No convierte esa fuente en autoridad de
Malāk, no promueve automáticamente un gap y no autoriza implementación.

No crea nuevas capabilities ni autoriza implementación.

Estado:

`concept / non_normative / research_horizon_reconciliation`

## Regla de uso

Antes de utilizar cualquiera de estos documentos para proponer implementación:

1. verificar `main` y HEAD;
2. verificar el baseline vigente;
3. consultar Blueprint;
4. consultar Constitución Cognitiva;
5. consultar Gobernanza;
6. revisar decisiones y roadmap vigentes;
7. identificar partes superseded o ya materializadas;
8. aplicar Necessity & Complexity Review;
9. proponer un alcance pequeño;
10. esperar autorización explícita del Owner.

Cuando una decisión dependa de investigación externa, deberá consultarse primero
el registro de evidencia de `MALAK_RESEARCH_HORIZON_MAP.md` y distinguir:

```text
fuente externa
!= evidencia aplicable
!= disposición ADOPT / ADAPT / OBSERVE / REJECT
!= roadmap
!= autorización
```

### Governed Ephemeral Agent Execution, Evidence and Candidate Evaluation Reference

Archivo:

`GOVERNED_EPHEMERAL_AGENT_EXECUTION_EVIDENCE_REFERENCE.md`

Preserva la referencia conceptual relacionada con:

- ejecución efímera y aislada de agentes;
- `Least Context`;
- observación externa de la ejecución;
- evidencia independiente del agente;
- lifecycle y liberación explícita de recursos;
- validación de candidatos antes del ranking;
- score como mecanismo comparativo sin autoridad;
- separación entre productor, observador, reviewer, validator y autoridad.

Complementa a `GOVERNED_SWARM_LONG_HORIZON_REFERENCE.md` sin reemplazarlo.

Separación principal:

```text
Governed Swarm
→ composición, coordinación y trabajo de horizonte largo

Ephemeral Agent Execution
→ sandbox, contexto, evidencia, lifecycle y evaluación de candidatos.
```

La implementación agentic continúa subordinada a las iniciativas existentes,
principalmente `IDEA-001`, `IDEA-003`, `IDEA-020` e `IDEA-024`.

Estado:

`concept / non_normative / conceptual_reference`

## Relación con el Project Vault

El repositorio oficial conserva estos documentos como referencia conceptual.

El Project Vault podrá mantener índices y proyecciones derivadas para facilitar
navegación, recuperación y continuidad.

Estas proyecciones son derivadas y no alteran la autoridad del repositorio oficial.

El Vault no deberá convertirse en una segunda fuente de autoridad para estos
documentos.
