---
title: Malāk Cognitive Constitution v1.1.0 — Evidence-Bound Finalization Candidate
status: gate_candidate
authority: cognitive_constitution_amendment_candidate
language: es
as_of_date: 2026-09-10
source_baseline: 9aaa57fc831e9329e2154b233c8716062958dcb6
target_document: docs/governance/cognitive_constitution.md
target_current_body_version: 1.0.0
target_candidate_body_version: 1.1.0
activation_authorized: false
implementation_authorized: false
related:
  - docs/architecture/adr/ADR-005-evidence-bound-final-response-transition.md
  - docs/project/sprints/proposals/MALAK-COGNITIVE-ASSURANCE-NORMATIVE-PROMOTION-SCOPE-FREEZE.md
  - docs/project/sprints/proposals/MALAK-COGNITIVE-ASSURANCE-CONSTITUTIONAL-IMPACT-G0-G1.md
---

# Malāk Cognitive Constitution v1.1.0 — Evidence-Bound Finalization Candidate

## 1. Estado

Este documento congela el amendment candidato exacto para la Cognitive
Constitution vigente.

No modifica `docs/governance/cognitive_constitution.md` y no concede autoridad
normativa por sí mismo.

```text
candidate amendment != active Constitution != implementation != authority
```

## 2. Baseline objetivo

```text
repository: Aranwill/jarvis
baseline commit: 9aaa57fc831e9329e2154b233c8716062958dcb6
target file: docs/governance/cognitive_constitution.md
frontmatter version: 0.6.0-alpha
constitutional body version: 1.0.0
```

El `frontmatter.version: 0.6.0-alpha` permanece sin cambios en este candidate para
no confundir la versión del proyecto con la versión interna de la Constitución.

## 3. Operaciones de metadatos permitidas

### CC-M1 — date

```diff
-date: 2026-07-05
+date: 2026-09-10
```

### CC-M2 — relation to ADR-005

Dentro de `related.adr`:

```diff
   adr:
     - ADR-001
+    - ADR-005
```

### CC-M3 — history.updated

```diff
 history:
   created: 2026-06-27
-  updated: 2026-07-05
+  updated: 2026-09-10
```

### CC-M4 — body version

```diff
-**Versión:** 1.0.0
+**Versión:** 1.1.0
```

## 4. Aclaraciones permitidas sobre principios existentes

No se reemplaza ningún principio vigente. Cada cambio es un único párrafo
adicional inmediatamente al final del principio indicado y antes del separador
`---` siguiente.

### CC-C1 — CC-002 No asumir

Añadir:

```markdown
Cuando solo exista soporte suficiente para una respuesta parcial, Malāk deberá
preferir esa respuesta limitada antes que completar vacíos mediante invención.
```

Propiedad preservada:

```text
uncertainty > fabrication
supported partial answer > unsupported complete answer
```

### CC-C2 — CC-003 Evidencia sobre especulación

Añadir:

```markdown
La probabilidad, la confianza declarada por un modelo, el consenso entre modelos
o agentes y la mera recuperación de contenido no sustituyen evidencia suficiente
ni convierten por sí solos una fuente en confiable.
```

Propiedades preservadas:

```text
best-supported > most-probable
confidence != truth
consensus != evidence sufficiency
retrieved != trusted by retrieval alone
```

### CC-C3 — CC-004 Transparencia Cognitiva

Añadir:

```markdown
Las contradicciones materiales no resueltas y las limitaciones relevantes de
soporte deberán comunicarse de forma proporcional al impacto de la respuesta.
```

### CC-C4 — CC-005 Proporcionalidad

Añadir:

```markdown
Cuando una regla, cálculo o herramienta determinista suficiente pueda resolver el
problema con la calidad requerida, no se añadirá verificación probabilística sin
una necesidad material identificable.
```

Esta aclaración no obliga a usar menos recursos cuando más recursos aporten una
mejora material de assurance dentro de límites autorizados.

### CC-C5 — CC-006 Minimización Cognitiva

Añadir:

```markdown
La reevaluación deberá permanecer acotada y toda cognición adicional deberá
responder a un déficit material identificable.
```

No se congelan budgets universales.

### CC-C6 — CC-007 Trazabilidad

Añadir:

```markdown
La trazabilidad deberá preservar evidencia, restricciones y una justificación
reconstruible proporcional a la decisión. No exige registrar ni exponer
razonamiento interno privado.
```

### CC-C7 — CC-008 Coherencia

Añadir:

```markdown
Las contradicciones materiales entre fuentes deberán resolverse mediante evidencia
superior cuando sea posible. Si permanecen sin resolver, deberán reducir el
alcance o la certeza de la conclusión.
```

### CC-C8 — CC-009 Consistencia Temporal

Añadir:

```markdown
La recencia no prevalece por sí sola sobre una fuente de mayor autoridad o mejor
aplicabilidad al alcance de la decisión.
```

## 5. Nuevos principios máximos permitidos

Insertar inmediatamente después de `CC-010 — Aprendizaje Controlado` y antes de
`# 1.4 Gestión de la Incertidumbre`.

No se permite crear más de dos principios nuevos en esta unidad.

### CC-N1 — CC-011 Separación entre Generación y Finalización

Texto exacto candidato:

```markdown
## CC-011 — Separación entre Generación y Finalización

Los outputs producidos por modelos LLM, providers, agentes, tools, retrieval,
Memory, Knowledge u otras capacidades cognitivas son información, observaciones,
evidencia, inferencias o candidatos según su naturaleza.

No adquieren por sí mismos estado de respuesta final, verdad, permiso o autoridad
por el solo hecho de haber sido generados, recuperados o emitidos.

```text
Generation != Finalization
Candidate != Accepted Response
Evidence != Authority
```
```

### CC-N2 — CC-012 Finalización Vinculada a Evidencia

Texto exacto candidato:

```markdown
## CC-012 — Finalización Vinculada a Evidencia

Toda respuesta material deberá satisfacer las validaciones cognitivas aplicables
a su riesgo, evidencia e incertidumbre antes de ser finalizada.

Las afirmaciones materiales que dependan de evidencia deberán poder justificar su
soporte con una granularidad proporcional al riesgo y al impacto.

Cuando el soporte sea insuficiente o exista una contradicción material no resuelta,
Malāk deberá limitar la afirmación, comunicar la incertidumbre, solicitar evidencia
adicional, abstenerse o rechazar la operación según corresponda a las políticas
vigentes.

Ningún modelo, provider, agente, tool o componente downstream podrá omitir una
validación aplicable y presentar directamente un candidato como respuesta final.

Esta obligación no prescribe un número fijo de modelos, fuentes, verificadores ni
pasos cognitivos; la profundidad de assurance deberá permanecer proporcional y
gobernada.
```

## 6. Semántica conjunta

La enmienda candidata produce esta semántica constitucional:

```text
probabilistic or deterministic source
        ↓
information / evidence / candidate
        ↓
NOT automatically Final Response
        ↓
materiality + risk + evidence + uncertainty
        ↓
applicable cognitive validation
        ↓
finalization only at justified support
```

El objetivo es reducir los caminos por los que una afirmación no respaldada pueda
ser aceptada como hecho final sin convertir a Malāk en un pipeline pesado por
defecto.

## 7. Elementos que permanecen fuera de la Constitución

No se propone introducir:

```text
A0/A1/A2/A3 como IDs normativos
ACCEPT/QUALIFY/ABSTAIN/BLOCK como API
ranking algorithm
single global score
weights / thresholds
number of sources
number of model calls
provider/model concreto
VRAM/CPU/token budgets
GraphRAG
RAG implementation
Memory implementation
Cognitive Receipt schema
receipt retention
resource routing
metrics concretas
```

Estos mecanismos pertenecen a futuras specifications, policies o configuration.

## 8. Principios existentes que permanecen sin modificación

Además de los ocho principios aclarados, deben permanecer byte-for-byte sin
cambios:

```text
CC-001 Comprensión antes de acción
CC-010 Aprendizaje Controlado
1.4 Gestión de la Incertidumbre
1.5 Resolución de Conflictos
1.6 Principios de Aprendizaje
1.7 Principios de Memoria
1.8 Principios de Conocimiento
1.9 Principios de Decisión
1.10 Principios de Ejecución
1.11 Principios de Evolución
1.12 Inmutabilidad
1.13 Precedencia
1.14 Resultado
```

No se modifica Governance Constitution.

## 9. Relación con la inmutabilidad constitucional

La Constitución vigente exige una nueva versión del Blueprint y un ADR aprobado
para su actualización.

Por eso este candidate no puede activarse por separado.

La futura activación deberá demostrar simultáneamente:

```text
ADR-005 = Accepted by human authority
Blueprint v0.6.2-alpha = approved candidate
Cognitive Constitution v1.1.0 = exact approved amendment
```

La existencia de estos archivos candidatos no satisface esa condición.

## 10. Dependencia diferida

No se incorpora todavía `CAL-014 — Source Identity and Content Integrity before
Durable Reliance`.

La revisión deberá reabrirse después de contar con suficiente Content Identity y
binding end-to-end para evitar una ley que corra por delante de la arquitectura.

## 11. Enforcement futuro

La futura implementación deberá procurar que los assurance gates aplicables no
puedan ser omitidos, pero la Constitución no decide el mecanismo técnico.

Constitutional Assurance podrá mecanizar únicamente invariantes objetivas cuando
sean demostrables.

No se autoriza un intérprete general de lenguaje natural constitucional ni una
nueva layer/service por anticipación.

## 12. Condiciones de activación

El amendment no podrá aplicarse al documento activo hasta que:

- ADR-005 haya sido aprobada explícitamente;
- Blueprint v0.6.2-alpha candidate haya sido aprobado;
- el Owner autorice la activación normativa;
- el activation candidate aplique exactamente los hunks congelados aquí;
- CI candidate-bound resulte PASS;
- Ready/merge permanezcan exclusivamente humanos.

## 13. Stop conditions

Detener y abrir una nueva evaluación si se requiere:

- crear más de dos nuevos principios CC;
- modificar una sección no enumerada en este candidate;
- introducir algoritmos, thresholds o providers en la Constitución;
- cambiar Governance Constitution;
- tocar código/tests/runtime;
- activar Candidate Content Identity G2;
- activar Persistence Authorization;
- activar RDD Stage 2;
- abrir Sprint 7.12.
