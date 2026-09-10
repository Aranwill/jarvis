---
title: Malāk Cognitive Assurance — G0 Research and Cost Evidence
status: gate_candidate
authority: research_admission_evidence
language: es
as_of_date: 2026-09-10
source_baseline: 1a2e31e1b7dfb9a692f0f198b32bd33714a62ff2
risk_class_if_promoted: 3
implementation_authorized: false
constitutional_change_authorized: false
rdd_stage_2_authorized: false
related:
  - docs/project/concepts/MALAK_EVIDENCE_BOUND_COGNITION_FOUNDATION.md
  - docs/governance/cognitive_constitution.md
  - docs/governance/governance_constitution.md
  - docs/architecture/blueprint.md
  - documents/projects/jarvis/ideas.md
  - AGENTS.md
---

# Malāk Cognitive Assurance — G0 Research and Cost Evidence

## 1. Propósito

Evaluar, antes de diseñar o implementar una nueva frontera cognitiva, qué precedentes externos y qué propiedades internas justifican una metodología propia de assurance para Malāk.

La pregunta de G0 no es:

> ¿Cómo hacemos más complejo a Malāk para comprobar cada respuesta?

La pregunta es:

> ¿Cuál es el mínimo mecanismo proporcional, adaptable y verificable que reduce la probabilidad de que información no soportada alcance una respuesta final como hecho aceptado?

Este documento es evidencia de investigación y admisión. No crea una capability, contrato, servicio, política runtime, ADR ni ley constitucional.

---

## 2. Norte arquitectónico preservado

Malāk debe permanecer:

- Human in Control;
- Kernel First;
- Runtime Independent;
- Language Agnostic;
- Model Agnostic;
- Provider Agnostic;
- auditable;
- observable;
- proporcional en uso de recursos;
- cognitivamente minimalista;
- capaz de degradar de forma explícita y segura.

La finalidad de Cognitive Assurance es aumentar la determinación de la **aceptación y finalización** de respuestas, no eliminar por fuerza bruta la naturaleza probabilística de los modelos.

```text
probabilistic generation
        ↓
minimum sufficient assurance
        ↓
increasingly deterministic acceptance
        ↓
governed final response
```

Principio operativo candidato:

> **Maximum justified confidence with minimum necessary complexity.**

---

## 3. Restricciones ya existentes dentro de Malāk

La Cognitive Constitution ya exige proporcionalidad y minimización cognitiva: no utilizar procesos complejos cuando una regla simple produzca un resultado equivalente y evitar pasos innecesarios.

El Blueprint ya declara al LLM como proveedor reemplazable y separa la arquitectura de cualquier runtime o proveedor concreto.

`IDEA-003 — Resource Governance Foundation` ya preserva propiedades compatibles con esta evaluación:

- activar solo capacidades necesarias;
- lazy loading de modelos, índices, servicios y herramientas;
- descargar recursos tras inactividad;
- mantener por defecto un solo modelo generativo pesado en VRAM;
- preferir ejecución secuencial antes que paralela salvo evidencia telemétrica;
- limitar top-k y reranking;
- degradar capacidades de forma controlada cuando falten recursos.

Por tanto una propuesta que obligue a múltiples modelos pesados o múltiples rondas para toda respuesta sería incompatible con el baseline conceptual actual salvo nueva evidencia y autorización.

---

## 4. Evidencia externa revisada

### 4.1 OpenAI — incertidumbre y abstención

Referencia:

`https://openai.com/index/why-language-models-hallucinate/`

Hallazgo relevante:

- los sistemas de evaluación que premian solamente exactitud pueden incentivar guessing;
- un error confiado puede ser peor que una abstención;
- reconocer incertidumbre es una conducta deseable cuando no existe soporte suficiente.

Disposición Malāk:

```text
ADOPT PROPERTY
```

Propiedad adoptable:

```text
unsupported guess < qualified uncertainty / abstention
```

No se adopta ninguna implementación o API específica de proveedor.

### 4.2 Anthropic — eval-driven development y graders proporcionales

Referencia:

`https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents`

Hallazgos relevantes:

- definir éxito mediante evals antes de escalar una capacidad reduce ambigüedad;
- se combinan graders deterministas, modelos y revisión humana según la propiedad evaluada;
- deben medirse también latencia, tokens, coste por tarea y error rate;
- comenzar con suites pequeñas puede aportar valor antes de construir infraestructura masiva.

Disposición Malāk:

```text
ADAPT
```

Adaptación:

- preferir evaluadores deterministas para invariantes objetivas;
- usar evaluadores probabilísticos solo para propiedades que no puedan cerrarse mecánicamente;
- medir calidad y coste conjuntamente.

### 4.3 Google — claim grounding y contexto suficiente

Referencias:

`https://cloud.google.com/generative-ai-app-builder/docs/check-grounding`

`https://research.google/blog/deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context/`

Hallazgos relevantes:

- grounding útil requiere soporte a nivel de claims;
- context suficiente y context recuperado no son equivalentes;
- incluso modelos fuertes pueden responder incorrectamente cuando el contexto es insuficiente;
- RAG no debe interpretarse como garantía de verdad.

Disposición Malāk:

```text
ADAPT
```

Propiedad candidata:

```text
retrieved != sufficient != trusted != true
```

### 4.4 Google — Astute RAG y conflictos de conocimiento

Referencia:

`https://research.google/pubs/astute-rag-overcoming-imperfect-retrieval-augmentation-and-knowledge-conflicts-for-large-language-models/`

Hallazgos relevantes:

- retrieval imperfecto puede introducir información irrelevante, engañosa o maliciosa;
- los conflictos entre conocimiento paramétrico y evidencia externa son una frontera real;
- la consolidación source-aware y la finalización según confiabilidad pueden mejorar robustez.

Disposición Malāk:

```text
ADAPT / FUTURE RAG
```

No autoriza RAG actual.

### 4.5 Google — metacognición e incertidumbre fiel

Referencia:

`https://research.google/pubs/position-hallucinations-undermine-trust-metacognition-is-a-way-forward/`

Hallazgo relevante:

- ampliar conocimiento no resuelve por sí mismo la capacidad de reconocer límites;
- para sistemas agentic, incertidumbre puede actuar como señal de control para decidir cuándo buscar y qué confiar.

Disposición Malāk:

```text
ADAPT
```

Malāk debe tratar incertidumbre como señal gobernada, no como autoridad del modelo.

### 4.6 Microsoft — groundedness != correctness

Referencia:

`https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-llm-evaluation-phase`

Hallazgos relevantes:

- groundedness, completeness, utilization, relevancy y correctness son dimensiones diferentes;
- una respuesta puede estar grounded en una fuente y aun ser incorrecta;
- las evaluaciones con LLM son no deterministas y requieren rangos/calibración;
- deben documentarse parámetros y resultados de evaluación.

Disposición Malāk:

```text
ADOPT SEPARATION / ADAPT IMPLEMENTATION
```

Regla:

```text
one score != complete assurance
```

### 4.7 AWS Bedrock — grounding/relevance thresholds

Referencia:

`https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html`

Hallazgos relevantes:

- grounding y relevance pueden evaluarse como dimensiones separadas;
- thresholds pueden decidir filtrado;
- el mecanismo posee restricciones de casos de uso y comportamiento de streaming que impiden asumir cobertura universal.

Disposición Malāk:

```text
ADAPT CONCEPT / REJECT PROVIDER COUPLING
```

### 4.8 NVIDIA NeMo Guardrails — output rails y coste observable

Referencias:

`https://docs.nvidia.com/nemo/guardrails/configure-guardrails/guardrail-catalog/fact-checking`

`https://docs.nvidia.com/nemo/guardrails/evaluation/evaluate-configuration`

Hallazgos relevantes:

- fact-checking puede ubicarse como output rail;
- self-check depende fuertemente de la capacidad del modelo y no constituye prueba determinista;
- evaluaciones de guardrails deben medir compliance, número de LLM calls/tokens y latency impact;
- algunos fallos de self-check pueden configurarse fail-closed.

Disposición Malāk:

```text
ADAPT
```

Malāk debe preferir una frontera obligatoria cuando aplique, pero no una segunda inferencia obligatoria para toda respuesta.

### 4.9 NIST AI 600-1 — confabulation como riesgo de sistema

Referencia:

`https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf`

Hallazgo relevante:

- confabulation surge naturalmente de la naturaleza estadística de modelos generativos;
- el control debe tratarse como gestión de riesgo del sistema, no como promesa de modelo perfecto.

Disposición Malāk:

```text
ADOPT FRAMING
```

### 4.10 CoVe — Chain-of-Verification

Referencia:

`https://aclanthology.org/2024.findings-acl.212/`

Hallazgo relevante:

- draft → preguntas de verificación → respuestas independientes → respuesta final puede reducir hallucination en tareas evaluadas.

Coste estructural:

- múltiples etapas de inferencia;
- mayor latencia y tokens;
- riesgo de errores correlacionados si se usa el mismo modelo.

Disposición Malāk:

```text
OBSERVE / ADAPT FOR A2-A3 ONLY
```

No default para respuestas triviales.

### 4.11 RARR — attribution and revision

Referencia:

`https://aclanthology.org/2023.acl-long.910/`

Hallazgo relevante:

- búsqueda de atribución y revisión posterior puede mejorar soporte externo preservando el output original.

Coste estructural:

- búsqueda adicional;
- análisis/revisión adicional;
- depende de adquisición externa de evidencia.

Disposición Malāk:

```text
OBSERVE / FUTURE EVIDENCE ACQUISITION
```

### 4.12 CRAG — Corrective RAG

Referencia:

`https://arxiv.org/abs/2401.15884`

Hallazgo relevante:

- un evaluador ligero de retrieval puede decidir si la evidencia recuperada merece uso o corrección adicional.

Disposición Malāk:

```text
ADAPT FOR FUTURE RAG
```

Propiedad valiosa:

```text
retrieval itself is evaluated before material reliance
```

### 4.13 Self-RAG

Referencia:

`https://proceedings.iclr.cc/paper_files/paper/2024/hash/25f7be9694d7b32d5cc670927b8091e1-Abstract-Conference.html`

Hallazgo relevante:

- retrieval on-demand y crítica adaptativa pueden superar retrieval indiscriminado.

Coste/limitación:

- requiere comportamiento/modelado especializado;
- no justifica acoplar la arquitectura de Malāk a reflection tokens o un modelo concreto.

Disposición Malāk:

```text
ADOPT ADAPTIVITY PRINCIPLE / REJECT MODEL COUPLING
```

### 4.14 Semantic Entropy

Referencia:

`https://www.nature.com/articles/s41586-024-07421-0`

Hallazgo relevante:

- la incertidumbre semántica puede ayudar a detectar determinadas respuestas no confiables y habilitar selective answering.

Coste potencial:

- suele requerir muestreo múltiple o inferencias adicionales;
- no constituye un detector universal de falsedad.

Disposición Malāk:

```text
OBSERVE AS OPTIONAL HIGHER-ASSURANCE SIGNAL
```

---

## 5. Evaluación de costes

No se asignan multiplicadores universales porque dependen del modelo, hardware, batching, contexto, proveedor y red. G0 clasifica costos relativos.

| Mecanismo | Compute | Latencia | Memoria/VRAM | Complejidad | Disposición |
|---|---|---|---|---|---|
| schema/policy/precedence checks | muy bajo | muy baja | mínima | baja | ADOPT |
| provenance/evidence binding | bajo | baja | baja | moderada | ADOPT |
| temporal/scope validation | muy bajo | muy baja | mínima | baja | ADOPT |
| retrieval simple cuando es necesario | bajo-moderado | baja-moderada | índice | moderada | ADAPT |
| reranking selectivo | moderado | moderada | opcional | moderada | ADAPT |
| un verifier LLM selectivo | alto relativo | alta | modelo/API | media-alta | ADAPT A2/A3 |
| CoVe / revisión multi-pass | alto | alta | reutilizable/API | alta | OBSERVE A2/A3 |
| multi-model voting always-on | muy alto | muy alta | alta | alta | REJECT AS DEFAULT |
| agent debate/swarm always-on | extremo/no acotado | extrema | alta | muy alta | REJECT AS DEFAULT |

---

## 6. Hallazgo G0 principal — progressive assurance

La evidencia no justifica un pipeline fijo de máxima verificación.

Se selecciona para diseño posterior la propiedad:

```text
minimum sufficient assurance
proportional to risk, uncertainty and available resources
```

Modelo conceptual candidato, sin contratos aprobados:

```text
A0 — FAST / DETERMINISTIC
simple response or deterministic result
cheap structural checks
no extra verifier by default

A1 — GROUNDED
evidence-dependent answer
provenance + scope + temporal validity + evidence binding
one generation by default

A2 — VERIFIED
meaningful contradiction / uncertainty / complex factual synthesis
selective verifier or bounded reconsideration

A3 — HIGH ASSURANCE
high-impact / sensitive / persistent / externally consequential
independent checks and human governance when applicable
```

Los nombres `A0..A3` son placeholders conceptuales y no constituyen contratos públicos.

---

## 7. Propiedades seleccionadas

### MCA-G0-P1 — Deterministic checks first

Toda propiedad objetivamente verificable debe preferir reglas deterministas a inferencia adicional.

### MCA-G0-P2 — One heavy generator by default

No cargar múltiples modelos generativos pesados por defecto.

### MCA-G0-P3 — Expensive verification is conditional

Una segunda inferencia, retrieval adicional o evaluador independiente requiere señal material de riesgo, insuficiencia o contradicción.

### MCA-G0-P4 — Retrieval is not automatically trusted

RAG futuro debe evaluar suficiencia, provenance, vigencia, scope y conflicto antes de material reliance.

### MCA-G0-P5 — Uncertainty is a control signal

Incertidumbre suficiente puede provocar `QUALIFY`, búsqueda adicional acotada o `ABSTAIN`; nunca concede autoridad.

### MCA-G0-P6 — Same material state should converge

Con evidencia material, policy, estado y tiempo equivalentes, la **decisión de assurance** debe tender a ser estable aunque la superficie lingüística pueda variar.

### MCA-G0-P7 — Bounded cognition

Reconsideration, retrieval y verification deben tener presupuestos finitos. No se permiten loops abiertos de “seguir pensando hasta sentirse seguro”.

### MCA-G0-P8 — Explicit degradation

Si la infraestructura no puede satisfacer el assurance requerido, Malāk debe degradar de forma visible (`QUALIFY`/`ABSTAIN`/`BLOCK` según caso), no reducir silenciosamente garantías.

### MCA-G0-P9 — Infrastructure changes strategy, not law

CPU-only, GPU local, servicios remotos o frontier providers pueden cambiar la estrategia de ejecución, pero no las leyes cognitivas aplicables.

### MCA-G0-P10 — Assurance evidence carries zero authority

Scores, verifier outputs, consensus y receipts son evidencia. No autorizan acciones ni cambian Human in Control.

---

## 8. Métricas candidatas

No usar únicamente `hallucination rate` del modelo.

Medir al menos conceptualmente:

```text
unsupported_claim_generation_rate
unsupported_claim_escape_rate
abstention_precision
abstention_recall
claim_support_coverage
contradiction_detection_rate
assurance_decision_stability
latency_delta
llm_calls_per_response
tokens_per_response
retrieval_rounds_per_response
peak_ram
peak_vram
external_cost_per_response
```

Métrica estratégica candidata:

```text
unsupported claim generated internally
        !=
unsupported claim escaped as accepted final fact
```

El segundo evento es el fallo sistémico prioritario.

---

## 9. Budgeting conceptual

G1 deberá evaluar si cada operación cognitiva necesita un presupuesto explícito de recursos.

Posibles dimensiones, sin schema aprobado:

```text
max_generation_passes
max_verifier_passes
max_retrieval_rounds
max_sources
max_context
max_latency
max_external_cost
allowed_provider_classes
```

Los valores concretos no pertenecen a G0.

---

## 10. Alternativas rechazadas en G0

### Un LLM judge obligatorio para toda respuesta

```text
REJECT AS DEFAULT
```

Motivo: duplica costo de inferencia y mantiene evaluación probabilística incluso donde una regla objetiva es suficiente.

### Majority voting como verdad

```text
REJECT
```

Motivo: consensus != truth y errores pueden estar correlacionados.

### Multi-agent debate always-on

```text
REJECT AS DEFAULT
```

Motivo: costo y superficie arquitectónica no justificados para la necesidad actual.

### Frontier provider obligatorio

```text
REJECT
```

Motivo: viola independencia de proveedor y degradación local.

### GraphRAG obligatorio

```text
REJECT
```

Motivo: no existe necesidad actual demostrada y añade infraestructura antes de disponer de RAG básico.

### Cognitive receipt exhaustivo para toda interacción

```text
REJECT AS DEFAULT
```

Motivo: trazabilidad debe ser proporcional; no se justifica conservar grandes traces para operaciones triviales.

---

## 11. Complejidad arquitectónica permitida

Regla de admission para cualquier diseño posterior:

> **No crear un componente si una responsabilidad real puede expresarse limpiamente mediante una frontera existente.**

Toda nueva pieza deberá responder:

1. ¿qué fallo concreto evita?
2. ¿puede resolverlo una regla determinista?
3. ¿requiere realmente otro modelo?
4. ¿cuál es su coste máximo o presupuesto?
5. ¿qué ocurre en hardware limitado?
6. ¿cómo degrada explícitamente?
7. ¿qué evidencia demuestra mejora?
8. ¿puede eliminarse o sustituirse sin romper arquitectura?

Si estas preguntas no tienen respuesta suficiente:

```text
STOP / DO NOT ADD COMPONENT
```

---

## 12. Relación con RDD

Gentle AI RDD continúa siendo una referencia valiosa para:

- candidate identity/binding;
- frozen candidate;
- bounded review/correction;
- lineage;
- evidence/receipt separation from delivery authority.

La evaluación G0 concluye que RDD **no debe convertirse en una metodología cognitiva monolítica**.

Disposición:

```text
RDD for Malāk Engineering Assurance     ADAPT / CONTINUE
RDD properties for Cognitive Assurance  ADAPT SELECTIVELY
RDD as complete Cognitive Method        REJECT
RDD Stage 2                             NOT AUTHORIZED
```

Malāk debe madurar su propio método integrando propiedades demostradas de distintas líneas de investigación bajo su Constitución, Resource Governance y Human in Control.

---

## 13. Resultado G0

```text
G0 RESULT: PASS / ADAPT

selected direction:
Malāk-native progressive cognitive assurance

core property:
maximum justified confidence
with minimum necessary complexity

architecture style:
small deterministic/governed control plane
+ replaceable probabilistic workers

always-on multi-model verification:
REJECT

risk/resource-adaptive escalation:
SELECT

implementation:
NOT AUTHORIZED

constitutional promotion:
NOT AUTHORIZED

RDD Stage 2:
NOT AUTHORIZED
```

---

## 14. Gate siguiente permitido

Solo con autorización separada del Owner, G1 podrá **diseñar** el mínimo modelo conceptual de progressive assurance y sus invariantes verificables.

G1 deberá congelar:

- responsabilidad exacta de la futura frontera;
- qué puede resolverse sin LLM;
- señales mínimas de escalación;
- semántica de degradación;
- budget model conceptual;
- outputs cerrados candidatos;
- límites de observabilidad/receipt;
- relación con Constitutional Assurance existente;
- stop conditions contra sobreingeniería.

G1 no deberá implementar runtime, RAG, Memory, Knowledge, agents, tools ni cambios constitucionales.

---

## 15. Fuera de alcance

```text
Cognitive Constitution modification
Governance Constitution modification
Blueprint modification
ADR creation/acceptance
runtime implementation
Response Assurance service
RAG implementation
persistent Memory
Knowledge implementation
agent/swarm implementation
model loading policy implementation
Resource Governance implementation
new external dependencies
new provider integration
RDD Stage 2
Candidate Content Identity G2
Persistence Authorization
Sprint 7.12 authorization
authority expansion
```

---

## 16. Conclusión

La evidencia revisada favorece construir una metodología cognitiva propia de Malāk, inspirada en precedentes externos pero subordinada a sus leyes.

El valor no proviene de añadir más razonamiento por defecto. Proviene de mover la confiabilidad hacia fronteras explícitas y auditables:

```text
cheap deterministic evidence first
        ↓
additional cognition only when necessary
        ↓
bounded and observable escalation
        ↓
explicit uncertainty/degradation
        ↓
best-supported final response
```

G0 no encuentra justificación para hacer a Malāk más pesado o más acoplado. Encuentra justificación para hacerlo **más selectivo, verificable y determinista en sus decisiones**.
