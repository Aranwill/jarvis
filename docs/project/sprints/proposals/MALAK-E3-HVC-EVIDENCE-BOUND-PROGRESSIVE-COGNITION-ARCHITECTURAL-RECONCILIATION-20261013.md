---
title: Malāk E3/HVC — Evidence-Bound Progressive Cognition — Architectural Reconciliation
status: architectural_reconciliation_candidate
authority: non_normative
language: es
date: 2026-10-13
baseline_commit: 95eba75dc12b5ec27fa9eaab33f499d9440108b0
baseline_tree: 8d729fc17e5382f15343b702c48d0acdc8195c4b
trigger_issue: 313
parent_issue: 311
risk_class: 3_HIGH
critical_contract: true
authority_effect: none
implementation_authorized: false
red_authorized: false
green_authorized: false
kernel_delta: 0
planner_delta: 0
---

# Malāk E3/HVC — Evidence-Bound Progressive Cognition — Architectural Reconciliation

## 1. Propósito

Esta unidad reconcilia el diseño híbrido E3/HVC con la lógica fundacional de Malāk después de la campaña experimental HVC-B.

No corrige el proyecto por intuición. Incorpora una lección empírica:

> exigir determinismo fuerte al residuo semántico probabilístico produjo complejidad creciente sin demostrar valor proporcional.

La corrección propuesta no debilita gobernanza. Reubica el determinismo donde Malāk ya lo necesita de forma material:

- identidad y binding;
- policy;
- permisos;
- admisión;
- transiciones de estado;
- authorization;
- settlement cuando sea policy-owned;
- Protected Finalization;
- durable reliance cuando aplique.

La cognición puede permanecer probabilística, falible y reemplazable siempre que no adquiera authority por sí misma y que las afirmaciones materiales estén vinculadas a evidencia proporcional al riesgo.

```text
probabilistic cognition != authority
evidence != authority
generation != finalization
learning != self-authorization
```

## 2. Baseline exacto

```text
repository          Aranwill/jarvis
main                95eba75dc12b5ec27fa9eaab33f499d9440108b0
main_tree           8d729fc17e5382f15343b702c48d0acdc8195c4b
tracked_blobs       398
tree_truncated      false
HVC parent          integrated
HVC-A               integrated
HVC-B G0/G1         integrated
#310                CLOSED / NO_SELECTION
#311 / PR #312      design candidate under reconsideration
runtime_delta       0
authority_effect    none
```

## 3. Construction Preflight

```text
work_unit                    issue #313
work_type                    ARCHITECTURAL_RECONCILIATION
last_stable_checkpoint       main@95eba75dc12b5ec27fa9eaab33f499d9440108b0
P0 repository/baseline       PASS
P1 sources/hierarchy         PASS
P2 invariants                PASS
P3 authority direction       PASS
P4 reuse/necessity           PASS / REUSE + ADAPT
P5 risk                      3_HIGH
critical_contract            YES
Design 4R                    REQUIRED
RDD Stage 1 Design Check     REQUIRED
P6 scope                     DOCS ONLY / FROZEN
candidate identity strategy  Git commit/tree
P7 result                    PASS
authority_effect             none
```

Preflight PASS autoriza únicamente esta reconciliación documental.

## 4. Fuentes rectoras reconciliadas

### Normativas / arquitectónicas

- Cognitive Constitution;
- Governance Constitution;
- Blueprint;
- ADR-003;
- ADR-004;
- ADR-005;
- SECURITY.md;
- Architecture Quality Gates.

### Método

- AGENTS.md;
- Engineering Method;
- Construction Preflight;
- Construction Protocol;
- Development Checklist.

### Conceptos y dirección futura

- Evidence-Bound Cognition Foundation;
- Cognitive Dataset Foundation;
- Governed Self-Review Bootstrap;
- Governed Ephemeral Agent Execution reference;
- Research Horizon Map;
- ideas.md.

Estas referencias conceptuales no adquieren authority.

### Evidencia HVC

- Governed Hybrid Verification Composition V0;
- HVC-A SemanticObservationV0;
- HVC-B Specialized Semantic Verifier Experiment;
- #310 local due diligence / NO_SELECTION;
- #311 / PR #312 primitive composition candidate;
- código y tests E3/assurance/finalization existentes.

## 5. Hallazgo principal

El diseño original HVC ya separaba:

```text
deterministic envelope
        +
inferential residual
```

La deriva apareció al tratar de hacer que el residuo inferencial reprodujera con exactitud determinista cuatro dimensiones semánticas y al responder a cada fallo agregando más estructura.

Secuencia observada:

```text
monolithic verifier fails
→ split semantic dimensions
→ specialized model search
→ multiple primitives
→ deterministic composition
→ escalation design
```

Cada paso era localmente defendible. El conjunto comenzó a competir con:

- CC-005 Proporcionalidad;
- CC-006 Minimización Cognitiva;
- anti-overengineering del Construction Protocol;
- Model Agnostic;
- necesidad real demostrada.

Disposición:

```text
problem = ARCHITECTURAL DRIFT OF COMPLEXITY
not = SECURITY FAILURE
not = GOVERNANCE FAILURE
not = NEED TO RELAX MALĀK
```

## 6. Interpretación corregida del determinismo

### 6.1 Determinismo requerido

Debe permanecer fuerte cuando la responsabilidad es de control o transición protegida:

| Superficie | Disposición |
|---|---|
| exact subject/evidence identity | deterministic |
| schema/binding validation | deterministic |
| policy applicability | deterministic cuando policy lo permita |
| permission / authorization | deterministic |
| invalid/malformed handling | deterministic fail-safe |
| authority flow | deterministic contract |
| Protected Finalization decision | deterministic sobre inputs gobernados |
| durable reliance safeguards | deterministic/policy-governed cuando aplique |
| audit identity / provenance | deterministic representation |

### 6.2 Cognición no obligatoriamente determinista

Puede permanecer probabilística:

- interpretación semántica;
- hipótesis;
- síntesis;
- clasificación lingüística;
- planificación no ejecutiva;
- propuesta de alternativas;
- detección de posibles contradicciones;
- búsqueda de explicaciones;
- candidate response generation.

Requisitos:

```text
bounded
observable
replaceable
evidence-aware
uncertainty-capable
authority_effect = none
```

## 7. Modelo híbrido reconciliado

El modelo híbrido pasa a entenderse como:

```text
Probabilistic Cognition
        +
Evidence-Bound Evaluation
        +
Deterministic Governance
        +
Controlled Learning
```

No es una nueva layer ni un nuevo servicio.

### 7.1 Flujo conceptual

```text
user / task
    ↓
governed context + applicable policy
    ↓
minimum sufficient cognition
    ↓
candidate / hypothesis / observation
    ↓
evidence acquisition or reuse when materially required
    ↓
evidence-bound evaluation
    ↓
uncertainty / contradiction / support state
    ↓
applicable assurance
    ↓
Protected Finalization when required
    ↓
response
```

Regla:

```text
deficit determines additional cognition
not
fixed cognition ladder
```

## 8. Progressive Cognition reinterpretada

Orden de preferencia:

```text
simple sufficient rule
before
available governed knowledge/evidence
before
single bounded probabilistic mechanism
before
additional tools/retrieval/review
before
multi-model / agentic escalation
before
human escalation when authority/risk requires it
```

Esto no prescribe una secuencia fija. Cada paso adicional necesita un déficit material identificable.

## 9. Evidencia y probabilidad

Malāk puede usar probabilidades internamente para generar candidatos.

Pero:

```text
probability != evidence
confidence != truth
consensus != evidence sufficiency
retrieval != trust
```

La calidad final debe tender a la respuesta mejor respaldada disponible bajo:

- evidencia válida;
- provenance aplicable;
- temporalidad;
- scope;
- contradiction handling;
- uncertainty;
- policy;
- security.

## 10. Aprendizaje y automejora

CC-010 y los principios de aprendizaje ya exigen que el aprendizaje sea:

```text
incremental
verifiable
reversible
audited
versioned
governed
```

La automejora se interpreta como:

```text
experience
    ↓
observable outcome
    ↓
evaluation
    ↓
pattern / lesson
    ↓
proposal
    ↓
Owner review
    ↓
authorized change
    ↓
comparative reevaluation
```

Malāk puede:

- detectar patrones;
- comparar estrategias;
- medir errores;
- medir abstención;
- identificar regresiones;
- proponer cambios;
- recomendar NO_CHANGE.

Malāk no puede:

- autoaprobar una propuesta;
- modificar permanentemente el baseline por decisión propia;
- convertir una mejora estadística en authority;
- aprender de forma irreversible;
- usar self-report como única evidencia.

## 11. Métricas de mejora práctica

La evaluación futura no debe optimizar sólo por PASS ni por mínima tasa de falsos positivos.

Debe observar un conjunto balanceado:

```text
supported-claim quality
false favorable rate
unnecessary abstention rate
task resolution rate
contradiction handling quality
calibration / uncertainty quality
regression rate
resource cost
latency
reproducibility where materially required
```

Una mejora es evidencia comparativa, no verdad universal.

## 12. Disposición HVC-A

`SemanticObservationV0` conserva valor como:

- vocabulario explícito;
- benchmark de boundaries;
- artefacto de investigación;
- posible contrato especializado si un consumer futuro demuestra necesidad.

Pero este gate rechaza asumir que sus cuatro dimensiones deban ser obligatoriamente emitidas por todo runtime semántico normal.

Disposición:

```text
HVC-A contract value             PRESERVE
HVC-A as universal runtime role  NOT DEMONSTRATED
four-dimension mandatory worker  RECONSIDER
ground-truth corpus              PRESERVE
historical validation evidence   PRESERVE
```

No se reescribe historia ni ground truth.

## 13. Disposición HVC-B / #311

La arquitectura de múltiples semantic primitives más deterministic composition es técnicamente coherente pero su necesidad productiva no está demostrada.

Por CC-005/006:

```text
multiple primitives always-on        REJECT
semantic verifier manager            REJECT
persistent model registry            REJECT
ensemble voting                      REJECT
fixed escalation ladder              REJECT
implicit decomposition               REJECT

single bounded semantic mechanism    ADMIT when needed
additional primitive                 ONLY on demonstrated deficit
large model escalation               OPTIONAL / policy-governed
UNKNOWN                              VALID
```

PR #312 debe permanecer Draft hasta resolución de #313.

## 14. Qué se conserva de los experimentos

Los experimentos #310 conservan valor de evidencia:

- ningún mecanismo probado debe tratarse como árbitro semántico perfecto;
- modelos pequeños pueden aportar señales útiles;
- modelos grandes tampoco eliminan boundaries difíciles;
- structured output no equivale a semantic correctness;
- false favorable y overcommit importan;
- local resource evidence ayuda a decidir mecanismos;
- UNKNOWN/abstention es necesaria;
- supply-chain/provenance siguen siendo relevantes cuando un mecanismo se seleccione.

No se deriva de ellos que Malāk necesite múltiples verificadores permanentes.

## 15. Component / Logic Reuse Review

| Superficie | Disposición |
|---|---|
| existing deterministic routing | REUSE |
| exact evidence bindings | REUSE |
| qualification/evaluation harness patterns | REUSE / ADAPT |
| Assurance Signal | REUSE |
| Protected Finalization | REUSE |
| Self-Review evidence packet | REUSE |
| Engineering Inspect/Analyze/Propose | REUSE |
| Cognitive Dataset concept | ADAPT as evaluation corpus direction |
| SemanticObservationV0 | PRESERVE / OPTIONAL REUSE |
| primitive composition | OBSERVE / not default |
| new cognitive manager/service | REJECT |
| Kernel/Planner change | REJECT |

```text
reuse_disposition = REUSE + ADAPT
new_component_fit = NOT_DEMONSTRATED
```

## 16. Necessity & Complexity Review

Necesario:

- distinguir cognition de authority;
- mantener evidence-bound finalization;
- medir mejora práctica;
- preservar aprendizaje gobernado;
- usar reglas deterministas cuando sean suficientes;
- hacer cognition adicional sólo por déficit material.

No demostrado:

- verifier universal;
- cuatro dimensiones semánticas obligatorias en runtime;
- multiple primitives permanentes;
- ensemble;
- fixed ladder;
- nuevo manager;
- nueva layer;
- nuevo registry;
- nueva authority.

Resultado:

```text
complexity reduction = REQUIRED
governance relaxation = NO
security relaxation = NO
```

## 17. Malāk Alignment Matrix

| Fuente | Invariante / intención | Disposición | Efecto |
|---|---|---|---|
| CC-002 | no inventar | ADOPT | uncertainty y partial response válidos |
| CC-003 | evidencia > especulación | ADOPT | probabilidad no sustituye soporte |
| CC-005 | proporcionalidad | ADOPT | deterministic cuando suficiente; no stack innecesario |
| CC-006 | minimización | ADOPT | cognition extra requiere déficit |
| CC-010 | aprendizaje controlado | ADOPT | experiencia → propuesta, no auto-cambio |
| CC-011 | Generation != Finalization | ADOPT | LLM sigue sin authority |
| CC-012 | evidence-bound finalization | ADOPT | assurance proporcional |
| Governance | Human in Control | ADOPT | Owner aprueba cambios |
| Blueprint | Model Agnostic | ADOPT | no acoplar arquitectura a verifier |
| ADR-003 | result != authority | ADOPT | observaciones suben sin control |
| ADR-004 | spec & verification first | ADOPT | cambios medidos antes de baseline |
| ADR-005 | progressive assurance | ADOPT | no fixed pipeline |
| Evidence-Bound Cognition | best-supported over most probable | ADOPT | núcleo del modelo reconciliado |
| Cognitive Dataset | comportamiento evaluable | ADAPT | medir aprendizaje y calidad |
| Self-Review | proposal without authority | ADOPT | loop de mejora gobernada |
| HVC-A | semantic boundaries | OBSERVE / PRESERVE | benchmark/optional contract |
| #311 primitive composition | safe but complex | OBSERVE / REJECT as default | no integrar aún |

## 18. Security Horizon Check

No se introducen nuevas superficies de:

- network;
- tools;
- persistent Memory;
- persistent Knowledge;
- external execution;
- secrets;
- delegation;
- authority propagation.

Resultado:

```text
Prompt/Context Trust        unchanged
Model supply-chain         deferred until mechanism selection
Memory poisoning           not activated
agent containment          not activated
authority elevation        none
Human in Control           preserved
security relaxation        none
```

## 19. Design 4R

### Risk — PASS

La simplificación no elimina controls authority-bearing. El principal riesgo sería interpretar "menos determinismo" como "menos validación". Se cierra explícitamente:

```text
less cognitive determinism
!=
less governance
!=
less evidence
!=
less security
```

### Readability — PASS

Responsabilidades quedan más claras:

```text
cognition proposes/interprets
evidence grounds
governance decides protected transitions
Owner authorizes durable change
```

### Reliability — PASS

Se conserva fail-safe en invalid/missing protected inputs. La fiabilidad cognitiva pasa a medirse empíricamente en vez de presumirse por arquitectura.

### Resilience — PASS

Un modelo puede fallar, cambiar o ser reemplazado sin transferir authority. UNKNOWN y partial response siguen disponibles.

```text
DESIGN_4R = PASS
```

## 20. RDD Stage 1 Design Check

```text
baseline exact                           PASS
candidate identity strategy              PASS
evidence provenance                      PASS
Writer / Reviewer / Validator / Authority separated
PASS | FAIL | INCONCLUSIVE discipline    PASS
candidate change invalidates evidence    PASS
bounded correction future                REQUIRED if candidate changes materially
independent validation future            REQUIRED before normative/runtime promotion
authority_effect                         none
```

`RDD_STAGE_1_DESIGN_CHECK = PASS`.

## 21. Qué NO autoriza

```text
runtime implementation         NO
RED                            NO
GREEN                          NO
new model selection            NO
HVC-C implementation           NO
support_sufficient wiring      NO
Protected Finalization change  NO
Constitution change            NO
Blueprint change               NO
Kernel / Planner change        NO
automatic learning persistence NO
self-modification              NO
Ready / Merge                  OWNER ONLY
```

## 22. Disposición propuesta para #311 / PR #312

```text
#311 purpose             useful experiment-driven design
#312 implementation      none
#312 state               KEEP DRAFT
primitive architecture  not promoted
reason                   complexity not demonstrated as necessary
supersession             pending Owner acceptance of #313 candidate
```

No cerrar #311 hasta que esta reconciliación sea validada e integrada o rechazada.

## 23. Próximo paso después de esta reconciliación

Si este diseño se integra, el próximo gate no debe ser "más verifier".

Debe definir el mínimo **Evidence-Bound Practical Evaluation Loop** que permita demostrar:

```text
candidate strategy A
vs
candidate strategy B

using fresh evidence/outcomes
→ did Malāk actually improve?
```

Ese gate debe reutilizar los mecanismos existentes de evaluation, observability y Self-Review antes de justificar cualquier componente nuevo.

## 24. Resultado terminal

```text
architectural reconciliation     PASS CANDIDATE
hybrid model                     REDEFINED / SIMPLIFIED
cognitive determinism            NOT UNIVERSAL REQUIREMENT
governance determinism           PRESERVED WHERE APPLICABLE
evidence-bound cognition         PRESERVED / CENTRAL
controlled learning              PRESERVED / CENTRAL
HVC-A                            PRESERVE / OPTIONAL ROLE
HVC-B primitive composition      NOT DEFAULT / NEED NOT DEMONSTRATED
#312                             KEEP DRAFT
new components                   NONE
Kernel / Planner delta           0 / 0
runtime delta                    0
authority_effect                 none
implementation                   NOT AUTHORIZED
RED / GREEN                      NOT AUTHORIZED
Owner authority                  preserved
```
