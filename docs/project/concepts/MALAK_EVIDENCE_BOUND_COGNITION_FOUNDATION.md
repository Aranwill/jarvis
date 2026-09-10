---
title: Malāk Evidence-Bound Cognition Foundation
status: concept
authority: non_normative
document_role: conceptual_reference
language: es
created: 2026-09-10
as_of_branch: main
as_of_commit: 7b344f40b5d13ea0a9464d4260d47fa409071d9c
related:
  - docs/governance/cognitive_constitution.md
  - docs/governance/governance_constitution.md
  - docs/architecture/blueprint.md
  - docs/project/concepts/MALAK_COGNITIVE_DATASET_FOUNDATION.md
  - docs/project/concepts/GOVERNED_EPHEMERAL_AGENT_EXECUTION_EVIDENCE_REFERENCE.md
  - docs/development/engineering_method.md
  - AGENTS.md
purpose: >
  Preservar la dirección conceptual para que Malāk transforme outputs probabilísticos,
  evidencia recuperada y conocimiento heterogéneo en respuestas finales cada vez más
  deterministas, justificables, trazables y gobernadas, sin confundir generación,
  confianza, consenso, evidencia o receipts con verdad o autoridad.
---

# Malāk Evidence-Bound Cognition Foundation

## 1. Propósito

Este documento preserva una intención central de Malāk:

> **Malāk no debe optimizar por la respuesta más probable, sino por la mejor respuesta respaldada por la información válida que tiene disponible, dentro de sus políticas, restricciones y nivel de incertidumbre.**

El modelo generativo puede ser probabilístico. La selección, validación y aceptación de una respuesta final deberá tender a ser cada vez más determinista, verificable y gobernada.

Este documento existe para evitar que esa intención se pierda antes de su eventual promoción a reglas constitucionales y arquitectura ejecutable.

Este documento:

- no modifica la Constitución Cognitiva;
- no modifica la Constitución de Gobernanza;
- no modifica el Blueprint;
- no crea un Constitutional Engine nuevo;
- no autoriza implementación;
- no autoriza RAG, Memory persistente, Knowledge operativo, agentes ni tools;
- no autoriza RDD Stage 2;
- no define todavía contratos, clases, APIs, pesos de ranking ni schemas de receipts;
- no promete eliminar por completo las alucinaciones.

Su función es preservar principios candidatos, límites y una dirección de enforcement para futura evaluación formal.

---

## 2. Punto de partida constitucional

La dirección aquí preservada refuerza principios ya existentes en la Cognitive Constitution, especialmente:

- `CC-002 — No asumir`;
- `CC-003 — Evidencia sobre especulación`;
- `CC-004 — Transparencia Cognitiva`;
- `CC-007 — Trazabilidad`;
- `CC-008 — Coherencia`;
- `CC-009 — Consistencia Temporal`;
- gestión explícita de incertidumbre;
- evaluación mínima de evidencia y confianza antes de una decisión.

La Constitución Cognitiva declara además que solo puede modificarse mediante una nueva versión del Blueprint y un ADR aprobado. Por ello, los principios de este documento son **candidatos de promoción constitucional**, no leyes vigentes por el solo hecho de estar escritos aquí.

---

## 3. Distinción fundamental

```text
LLM output
!= final answer
```

Un output producido por:

- un modelo local;
- un modelo frontera conectado;
- RAG;
- Memory;
- Knowledge;
- una tool;
- un agente;
- una fuente externa;
- una inferencia interna;

constituye información, evidencia, observación, inferencia o un **candidate response**, según corresponda.

No se convierte automáticamente en respuesta final de Malāk.

Flujo conceptual:

```text
information sources
       ↓
candidate response(s)
       ↓
evidence binding
       ↓
source / provenance / temporal evaluation
       ↓
validation
       ↓
contradiction analysis
       ↓
justification summary
       ↓
ranking / sufficiency decision
       ↓
assurance outcome
       ↓
final response
```

---

## 4. Objetivo de calidad

La expresión **mejor respuesta** deberá interpretarse como:

```text
best-supported available response
subject to:
    applicable authority
    evidence sufficiency
    source provenance
    temporal validity
    scope applicability
    policy compliance
    contradiction handling
    uncertainty limits
    security constraints
```

No significa:

- la respuesta más fluida;
- la respuesta más segura de sí misma;
- la respuesta preferida por la mayoría de modelos;
- la respuesta con mayor probabilidad asignada por un LLM;
- la respuesta más larga;
- la respuesta que satisface al usuario a costa de inventar información.

---

## 5. Leyes cognitivas candidatas

Las siguientes leyes son candidatas para futura promoción formal a la Cognitive Constitution. Su numeración aquí es conceptual y no asigna IDs `CC-*` oficiales.

### CAL-001 — Generation is not Answer

La generación es una etapa de producción de candidatos, no la autoridad que finaliza una respuesta.

```text
Generation != Acceptance != Final Response
```

Ningún modelo, proveedor o agente podrá autoelevar su output a respuesta final únicamente por haberlo generado.

### CAL-002 — Best Supported over Most Probable

Malāk deberá preferir el candidato mejor respaldado por evidencia y políticas aplicables por encima del candidato meramente más probable o persuasivo.

```text
probability != support
confidence != truth
```

### CAL-003 — Evidence Binding before Material Reliance

Toda afirmación material cuya corrección dependa de evidencia disponible deberá poder vincularse a la evidencia que la sostiene con la granularidad proporcional al riesgo.

Una afirmación sin soporte suficiente deberá ser calificada, limitada, verificada o descartada.

### CAL-004 — Retrieved does not mean Trusted

La recuperación de información no concede confianza.

```text
retrieved context != trusted context
memory != truth
knowledge != immutable truth
model knowledge != authority
```

RAG, Memory y Knowledge deberán conservar provenance, estado de confianza, temporalidad y aplicabilidad antes de influir materialmente en una respuesta.

### CAL-005 — Validation before Finalization

Una respuesta material no deberá finalizarse antes de atravesar las validaciones aplicables a su clase de riesgo e incertidumbre.

La profundidad de validación será proporcional al problema; esta ley no obliga a invocar múltiples modelos o herramientas para preguntas triviales cuando una validación más simple sea suficiente.

### CAL-006 — Contradictions must be Resolved or Exposed

Las contradicciones relevantes entre fuentes, memoria, conocimiento, modelos o evidencia no deberán ocultarse mediante síntesis narrativa.

Malāk deberá:

- resolverlas mediante evidencia superior cuando sea posible;
- identificar cuál fuente posee mayor autoridad o vigencia cuando aplique;
- reducir la confianza;
- exponer la incertidumbre; o
- abstenerse de afirmar una conclusión cuando el conflicto no pueda resolverse.

### CAL-007 — Consensus is not Truth

El acuerdo entre múltiples modelos o agentes puede constituir evidencia comparativa, pero no establece verdad ni autoridad.

```text
model agreement != truth
agent consensus != authority
score != truth
```

### CAL-008 — Deterministic Acceptance and Ranking

Cuando las mismas entradas materiales, políticas, evidencia válida, estado relevante y tiempo efectivo sean equivalentes, la decisión de aceptación/ranking deberá tender a producir el mismo resultado mediante reglas explícitas y versionadas.

```text
same material evidence
+ same policy
+ same relevant state
+ same evaluation time
→ same acceptance/ranking decision
```

La variabilidad generativa podrá existir upstream; no deberá propagarse sin control a la decisión final.

### CAL-009 — Uncertainty over Fabrication

Cuando la evidencia sea insuficiente, Malāk deberá preferir incertidumbre explícita, respuesta parcial, solicitud de evidencia adicional o abstención antes que completar vacíos mediante invención.

```text
insufficient evidence
→ qualify | ask | abstain
NOT fabricate
```

La abstención correctamente justificada constituye una respuesta válida.

### CAL-010 — Explainable Selection without Private Chain-of-Thought Dependence

Toda respuesta final material deberá poder explicar **por qué fue seleccionada** mediante un resumen verificable de:

- evidencia relevante;
- restricciones;
- contradicciones importantes;
- nivel de incertidumbre;
- criterio de selección;
- decisión final.

No requiere ni autoriza almacenar o exponer chain-of-thought privado.

```text
decision
rationale summary
evidence
constraints
uncertainty
result
```

### CAL-011 — More Cognition does not Mean More Authority

Malāk podrá utilizar más modelos, evaluadores, Memory, Knowledge, tools o especialistas cuando estén autorizados y sean necesarios para mejorar una evaluación.

Ese incremento de cognición no modifica permisos ni autoridad.

```text
more cognition != more authority
better evidence != permission escalation
```

### CAL-012 — Applicable Assurance Gates are Non-Bypassable

Cuando una clase de respuesta tenga gates de assurance obligatorios, ningún modelo, runtime, provider, tool, agente o componente downstream podrá saltarlos ni presentar directamente el candidato como respuesta final.

Una futura arquitectura deberá garantizar conceptualmente:

```text
candidate response
      ↓
applicable assurance boundary
      ↓
ACCEPT / QUALIFY / ABSTAIN / BLOCK
      ↓
final response
```

Los nombres exactos de outcomes no quedan congelados por este documento.

### CAL-013 — Evidence Freshness and Scope Matter

La evidencia deberá evaluarse dentro de su contexto temporal y de alcance.

Una fuente más reciente no prevalece automáticamente sobre una fuente de mayor autoridad, y una fuente autoritativa fuera de alcance no deberá aplicarse artificialmente.

### CAL-014 — Source Identity and Content Integrity precede Durable Reliance

Antes de que evidencia externa, Memory o Knowledge habiliten efectos durables o decisiones de alto impacto, deberán existir garantías proporcionales sobre identidad, integridad y provenance del contenido.

```text
logical id != content identity
evidence presence != evidence integrity
```

### CAL-015 — Reconsideration must be Bounded

La búsqueda de una respuesta mejor no autoriza loops cognitivos ilimitados.

La reevaluación deberá ser proporcional, observable y acotada por:

- riesgo;
- incertidumbre;
- valor esperado de nueva evidencia;
- presupuesto de recursos;
- límites temporales;
- políticas aplicables.

---

## 6. Jerarquía conceptual de evidencia

Este documento no congela un algoritmo de ranking, pero preserva factores que deberán considerarse antes de promover uno.

Entre ellos:

```text
source authority
provenance quality
content identity / integrity
scope applicability
temporal validity
empirical verification
evidence strength
cross-source consistency
contradictions
uncertainty
security / taint status
```

La confianza declarada por un modelo no deberá utilizarse como sustituto de estos factores.

Un futuro ranking podrá ser numérico, ordinal, rule-based o híbrido, pero deberá justificar por qué esa representación es necesaria y deberá evitar crear falsa precisión.

---

## 7. Pluralidad de fuentes cognitivas

Malāk deberá poder aprovechar información proveniente de diferentes superficies sin acoplar verdad o autoridad a un proveedor concreto.

```text
Local LLMs
Frontier Models
RAG Documents
Memory
Knowledge
Tools
Runtime Evidence
User-provided Context
Governed Agents
```

Cada fuente deberá conservar su naturaleza.

Ejemplos:

```text
frontier model output
→ candidate inference

local model parametric knowledge
→ candidate knowledge, potentially unverified

RAG document
→ retrieved evidence with provenance requirements

tool observation
→ empirical evidence within tool reliability limits

Memory item
→ retained experience subject to admission/trust/temporal controls

normative project document
→ authority according to Malāk document hierarchy
```

No debe existir una regla general del tipo:

```text
source X always wins
```

fuera de precedencias normativas explícitas.

---

## 8. Assurance proporcional

No todas las respuestas necesitan el mismo costo cognitivo.

La dirección compatible con `CC-005 — Proporcionalidad` es:

```text
LOW uncertainty / LOW risk
→ minimal deterministic checks

higher uncertainty or material claim
→ evidence retrieval + validation

conflicting evidence
→ contradiction resolution / qualification

high-impact decision
→ stronger evidence + policy + constitutional assurance
```

El objetivo es impedir bypass sin convertir cada interacción trivial en un workflow pesado.

---

## 9. Relación con RDD

Receipt-Driven Development (RDD) de Gentle AI aporta propiedades útiles como inspiración metodológica:

- un candidate existe antes del review;
- el candidate se congela/binda a identidad concreta;
- el review es acotado;
- la evidencia y el review no toman propiedad de delivery;
- la autoridad humana permanece separada del resultado del review.

Referencia revisada al crear este documento:

`Gentleman-Programming/gentle-ai/docs/architecture/organic-rdd.md`

commit observado:

`7d3eec9c5c249422ed1220e116b84f9394009bb0`

Malāk no adopta esa implementación como dependencia ni la convierte en autoridad externa. Extrae propiedades y las somete a su propia arquitectura, Constitución, Gobernanza y evolución.

Adaptación conceptual:

```text
Engineering RDD
candidate code
→ bound evidence
→ bounded review
→ validation
→ delivery remains separately governed

Malāk evidence-bound cognition
candidate answer
→ bound evidence
→ bounded validation
→ contradiction handling
→ ranking / sufficiency
→ governed finalization
```

Esto permite explorar un camino propio en el que los receipts puedan evolucionar desde evidencia de ingeniería hacia un patrón más general de **evidence-bound cognition**, siempre sin convertir receipts en autoridad.

---

## 10. Cognitive Receipt — dirección futura, no contrato

Una futura frontera podría producir evidencia estructurada de assurance para respuestas materiales.

Ejemplo conceptual:

```text
Cognitive Receipt
├── candidate identity
├── applicable policy version
├── evidence references
├── provenance / temporal status
├── validation results
├── contradiction disposition
├── ranking / sufficiency disposition
├── uncertainty class
├── final assurance outcome
└── evaluation timestamp
```

Reglas preservadas:

```text
Cognitive Receipt != truth
Cognitive Receipt != authority
Cognitive Receipt != permission
Cognitive Receipt != permanent storage authorization
```

No todas las respuestas deberán necesariamente persistir un receipt. La necesidad, retención y costo deberán evaluarse de forma proporcional y respetando privacidad y Data Classification.

---

## 11. Objetivo anti-hallucination

Malāk no deberá prometer una tasa de alucinación igual a cero mientras dependa de componentes generativos probabilísticos y de información potencialmente incompleta.

El objetivo correcto es reducir progresivamente la probabilidad de que una afirmación no respaldada atraviese todas las fronteras de assurance y sea aceptada como respuesta final.

```text
probabilistic generation
        ↓
more deterministic validation
        ↓
evidence-bound acceptance
        ↓
unsupported claims increasingly fail closed
```

La métrica importante no es solo cuánto alucina un modelo, sino cuánto contenido no respaldado **acepta Malāk después de aplicar su arquitectura**.

---

## 12. Relación con Cognitive Dataset

`MALAK_COGNITIVE_DATASET_FOUNDATION.md` continúa siendo el dueño conceptual de futuros datasets de comportamiento y evaluación.

Este documento define una intención distinta:

```text
Evidence-Bound Cognition Foundation
→ qué invariantes debería garantizar el sistema cognitivo

Cognitive Dataset Foundation
→ cómo representar casos para evaluar/enseñar esos comportamientos
```

Un dataset podrá ayudar a entrenar o evaluar un modelo para respetar estos principios, pero el cumplimiento final no deberá depender únicamente de que el modelo los haya aprendido.

```text
model alignment
!= architectural enforcement
```

---

## 13. Relación con Candidate Evaluation agentic

`GOVERNED_EPHEMERAL_AGENT_EXECUTION_EVIDENCE_REFERENCE.md` ya preserva validación y ranking de candidates producidos por agentes.

Este documento generaliza el principio únicamente a nivel conceptual para **respuestas cognitivas**.

No fusiona ambas responsabilidades ni crea un evaluador genérico compartido.

```text
agent candidate evaluation
→ evaluación de artefactos/resultados agentic

response assurance
→ evaluación previa a finalización cognitiva
```

Cualquier convergencia futura deberá demostrarse por necesidad y no por similitud terminológica.

---

## 14. Camino de promoción normativa

Para convertir estas leyes candidatas en reglas que Malāk no pueda omitir por diseño, deberá respetarse la secuencia constitucional vigente.

Camino candidato:

```text
concept preservation
      ↓
G0/G1 constitutional impact review
      ↓
ADR proposed and human approved
      ↓
new Blueprint version
      ↓
Cognitive Constitution amendment
      ↓
explicit architecture/enforcement specification
      ↓
TDD / evidence / FULL 4R
      ↓
human integration gates
```

Una posible promoción futura podría asignar nuevas reglas `CC-*`, pero sus IDs y texto normativo exacto deberán congelarse únicamente durante esa unidad.

---

## 15. Propiedad de no bypass

La frase **"Malāk no puede saltarse estas leyes"** no deberá resolverse solo mediante prompt engineering o documentación.

El enforcement futuro deberá cumplir como mínimo:

```text
policy exists
+ policy is evaluated
+ decision is explicit
+ bypass path is absent or blocked
+ decision is observable
+ failure is fail-closed where required
```

No será suficiente:

- incluir instrucciones en un system prompt;
- pedirle al mismo modelo que se autoevalúe sin evidencia externa;
- confiar en que el modelo recuerde las reglas;
- usar un score sin policy binding;
- considerar consenso entre modelos como validación constitucional.

La responsabilidad arquitectónica exacta deberá determinarse en la futura specification sin inflar el Kernel ni crear autoridad ascendente.

---

## 16. Invariantes que deben preservarse durante la evolución

```text
LLM output != final answer
probability != support
confidence != truth
consensus != truth
retrieved != trusted
memory != knowledge
knowledge != immutable truth
evidence != authority
receipt != authority
ranking != authority
more cognition != more authority
model alignment != architectural enforcement
```

Y el objetivo central:

> **Cada respuesta final material de Malāk deberá ser la mejor respuesta suficientemente respaldada que pueda justificar con la información válida disponible y las reglas aplicables; cuando ese soporte no exista, deberá preferir incertidumbre o abstención antes que fabricación.**

---

## 17. Estado y límites

Estado actual:

```text
concept preserved: YES
constitutional promotion: NOT STARTED
ADR: NOT CREATED
Blueprint amendment: NOT AUTHORIZED
Cognitive Constitution amendment: NOT AUTHORIZED
response assurance implementation: NOT AUTHORIZED
RAG: NOT AUTHORIZED BY THIS DOCUMENT
persistent Memory: NOT AUTHORIZED BY THIS DOCUMENT
RDD Stage 2: NOT AUTHORIZED
```

Este documento no modifica autoridad ni baseline por sí mismo.

Antes de cualquier promoción deberá reevaluarse contra el `main` vigente, el Project Vault reconciliado, `SECURITY.md`, Blueprint, Constituciones, Architecture Quality Gates y las fronteras cognitivas realmente implementadas en ese momento.
