---
title: Malāk Cognitive Assurance — G1 Progressive Assurance Design
status: gate_candidate
authority: conceptual_design_evidence
language: es
as_of_date: 2026-09-10
source_baseline: d835934c3cd80aac63f5f06f2e2c555c7f817350
g0_source: docs/project/sprints/proposals/MALAK-COGNITIVE-ASSURANCE-G0-RESEARCH-EVIDENCE.md
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

# Malāk Cognitive Assurance — G1 Progressive Assurance Design

## 1. Estado de autoridad

El Owner autorizó continuar después de integrar G0.

Esta unidad diseña solamente la forma mínima de **Progressive Cognitive Assurance** derivada de G0.

No autoriza:

- implementación runtime;
- cambios en `src/` o `tests/`;
- modificación de Cognitive Constitution;
- modificación de Governance Constitution;
- modificación de Blueprint;
- creación o aceptación de ADR;
- RAG;
- Memory persistente;
- Knowledge operativo;
- agentes o tools;
- Resource Governance implementation;
- provider/model integration;
- RDD Stage 2;
- Candidate Content Identity G2;
- Persistence Authorization;
- Sprint 7.12;
- expansión de autoridad.

```text
Design != Specification != Validation != Decision != Authority
```

---

## 2. Resultado G1

```text
G1 RESULT: PASS / ADAPT

selected design:
progressive, evidence-bound, resource-aware cognitive assurance

primary objective:
best-supported safe response
at or above the required assurance floor

secondary objective:
use the least unnecessary cost/complexity

resource scarcity:
may change execution strategy
must not silently lower the assurance floor
```

La corrección introducida respecto de una lectura demasiado rígida de G0 es deliberada:

```text
minimum necessary complexity
!=
minimum resource use at any cost
```

La optimización de recursos es subordinada a la calidad requerida por la decisión cognitiva.

---

## 3. Norte del diseño

Malāk debe tender a que:

```text
probabilistic workers
        ↓
produce candidates / evidence / estimates
        ↓
deterministic + governed assurance rules
        ↓
select, qualify, abstain or block
        ↓
final response
```

El sistema no intenta hacer determinista la generación lingüística completa.

El objetivo es hacer cada vez más determinista la decisión sobre **qué afirmaciones pueden atravesar la frontera de respuesta final y con qué nivel de certeza declarado**.

---

## 4. Regla de precedencia calidad–recursos

La Cognitive Constitution ya ordena, ante conflictos, considerar seguridad, cumplimiento constitucional, riesgo, evidencia, reversibilidad, costo y eficiencia.

G1 deriva una regla compatible:

```text
1. constitutional / governance / security constraints
2. required assurance floor
3. evidence sufficiency and contradiction status
4. explicit hard resource/authority limits
5. quality-improving escalation when justified
6. latency / compute / token / cost optimization
```

Por tanto:

```text
cost optimization
NEVER overrides
an unmet assurance requirement
```

Si alcanzar el assurance requerido consume más recursos pero permanece dentro de límites autorizados, Malāk puede emplearlos.

Si no puede alcanzar el assurance requerido dentro de límites duros, no debe fingir equivalencia de calidad.

---

## 5. Hard limits vs flexible preferences

G1 distingue dos categorías conceptuales.

### 5.1 Hard limits

No pueden sobrepasarse por mejorar una respuesta.

Ejemplos conceptuales:

- permisos y autoridad;
- política de privacidad;
- prohibición de un provider o red;
- límites de seguridad;
- límites económicos explícitos del Owner;
- indisponibilidad física de memoria/VRAM/CPU;
- deadlines duros cuando hayan sido definidos;
- políticas de datos o residencia;
- rate limits externos.

### 5.2 Flexible preferences

Pueden sacrificarse cuando hacerlo aporta valor material y sigue dentro de hard limits.

Ejemplos conceptuales:

- objetivo de baja latencia;
- preferencia por una sola inferencia;
- preferencia por ejecución local cuando la política permita una alternativa externa;
- target de tokens reducido;
- preferencia por no cargar un segundo modelo;
- target de consumo energético o tiempo de cómputo no vinculante.

La política concreta de qué límite es duro o flexible pertenece a futura Resource/Model Governance, no a este documento.

---

## 6. Principio Quality Floor First

Cada solicitud material deberá tener un **required assurance floor** proporcional al riesgo, impacto, incertidumbre y tipo de afirmación.

Ese floor se decide antes de considerar si la máquina actual es rápida o lenta.

```text
required assurance
!=
available resources
```

Los recursos disponibles determinan **cómo intentar alcanzar** el floor, no **qué floor merece** la pregunta.

Ejemplo conceptual:

```text
high-impact factual decision
requires high assurance

weak local resources
DO NOT convert it into low-assurance truth
```

Ante insuficiencia de recursos:

```text
use authorized alternative
OR
qualify
OR
abstain
OR
block
```

según el riesgo y la capacidad residual.

Nunca:

```text
quietly downgrade
→ present as fully supported
```

---

## 7. Niveles conceptuales de assurance

G1 conserva cuatro niveles como **design placeholders**, no contratos públicos.

### A0 — Direct / Deterministic

Uso candidato:

- transformaciones de texto;
- cálculo/regla determinista;
- contenido no factual generado por pedido;
- respuestas donde no existe una afirmación material que requiera evidencia externa.

Propiedades:

- checks estructurales aplicables;
- sin verifier adicional por defecto;
- sin retrieval por defecto.

### A1 — Grounded

Uso candidato:

- afirmaciones dependientes de documentos;
- futuras respuestas con RAG/Knowledge/Memory;
- estado de sistema verificable;
- información cuya fuente concreta importa.

Propiedades:

- evidence provenance;
- scope/temporal validity;
- source/security disposition;
- claim/evidence binding proporcional;
- una generación pesada por defecto cuando sea suficiente.

### A2 — Verified

Uso candidato:

- contradicciones materiales;
- síntesis factual compleja;
- incertidumbre relevante;
- evidencia insuficiente que podría resolverse mediante una verificación adicional;
- decisiones donde una segunda perspectiva aporta valor demostrado.

Propiedades:

- una escalación acotada;
- verifier o retrieval adicional selectivo;
- reevaluación posterior;
- no majority vote automático.

### A3 — High Assurance

Uso candidato:

- decisiones de alto impacto;
- acciones persistentes o externamente consecuentes;
- seguridad;
- afirmaciones donde un error pueda causar daño material;
- contextos que requieran gobernanza humana.

Propiedades:

- evidencia más fuerte o independiente;
- checks deterministas máximos aplicables;
- verificación adicional autorizada cuando aporte valor;
- Human in Control cuando corresponda.

Los IDs `A0..A3` no quedan congelados como API.

---

## 8. Inputs conceptuales mínimos

Una futura frontera de assurance solo necesita conocer conceptualmente:

```text
request / objective context
candidate response
material claims or decision payload
evidence references and dispositions
applicable policy / constitution version
risk / impact class
uncertainty and contradiction signals
available authorized capabilities
resource envelope
evaluation time
```

G1 NO define clases Python, JSON schemas ni APIs.

No se exige que todos esos datos existan para A0.

---

## 9. Deterministic checks first

Antes de invocar otra inferencia, deben agotarse los controles deterministas aplicables.

Ejemplos conceptuales:

```text
schema validity
policy allow/deny
source status
candidate/evidence identity
scope applicability
temporal validity
required fields
known contradiction markers
explicit authority boundaries
exact arithmetic / deterministic tool result
```

Regla:

```text
if deterministic evidence can settle the question
→ do not add probabilistic verification
```

Esto reduce costo sin degradar assurance.

---

## 10. Evidence sufficiency before model confidence

La confidence producida por un modelo es una señal auxiliar.

No sustituye:

- evidencia suficiente;
- provenance;
- vigencia;
- scope;
- autoridad de fuente;
- ausencia/resolución de contradicción.

```text
high model confidence + weak evidence
!=
high assurance
```

Y también:

```text
lower model confidence + authoritative evidence
may still support a qualified factual answer
```

La futura policy deberá valorar primero el estado de evidencia material.

---

## 11. Ranking sin score mágico

G1 rechaza como diseño base un único score opaco que mezcle verdad, costo, confianza y autoridad.

En su lugar se selecciona un **orden de precedencia explícito**.

Antes de rankear por utilidad o estilo, un candidato debe superar/admitir:

```text
policy / constitutional admissibility
security constraints
evidence support floor
temporal/scope applicability
contradiction disposition
uncertainty requirements
```

Solo entre candidatos admisibles puede considerarse luego:

```text
completeness
relevance
clarity
resource cost
latency
```

Coste/eficiencia actúan como optimización secundaria o desempate, no como sustituto de verdad o soporte.

```text
cheaper candidate
!=
better-supported candidate
```

---

## 12. Escalation-by-deficit

Una escalación cara debe responder a un déficit concreto.

No se admite:

```text
"think harder"
→ generic second pass
```

sin identificar qué falta.

Ejemplos conceptuales:

```text
missing evidence
→ targeted retrieval

source conflict
→ source/temporal/authority resolution

uncertain factual synthesis
→ selective verifier

insufficient independent support for A3
→ authorized independent check / human review
```

Esto mantiene la complejidad causalmente ligada al problema.

---

## 13. Bounded cognition

Toda escalación debe tener un presupuesto finito.

G1 no congela números universales.

El diseño futuro deberá poder expresar límites como:

```text
max verification rounds
max retrieval rounds
max model calls
max candidate revisions
max wall-clock budget
max token/API budget
max concurrent heavy models
```

Propiedad obligatoria:

```text
no unbounded cognitive loop
```

Al agotarse el presupuesto sin alcanzar el floor:

```text
QUALIFY | ABSTAIN | BLOCK
```

según la clase de riesgo.

---

## 14. Resultados conceptuales cerrados

G1 selecciona cuatro outcomes como semántica candidata:

### ACCEPT

La respuesta alcanza el required assurance floor para las afirmaciones materiales que contiene.

### QUALIFY

Existe soporte suficiente para una respuesta limitada, pero no para una afirmación más fuerte.

La salida debe exponer la limitación material.

### ABSTAIN

No existe soporte suficiente para responder responsablemente, pero no es necesario bloquear toda interacción.

### BLOCK

Una policy, seguridad, autoridad o riesgo aplicable impide producir la respuesta/acción solicitada en esa forma.

Importante:

```text
ABSTAIN != failure
QUALIFY != hidden downgrade
BLOCK != model uncertainty
```

No se autoriza todavía ningún enum runtime.

---

## 15. Regla de degradación explícita

Cuando infraestructura o providers no permitan alcanzar el nivel previsto:

```text
required floor remains unchanged
achieved floor is reported internally
response outcome reflects the gap
```

Ejemplo conceptual:

```text
A2 required
local verifier unavailable
external provider disallowed
        ↓
if current evidence supports only A1
        ↓
QUALIFY or ABSTAIN
```

Nunca:

```text
A2 required
resources unavailable
        ↓
pretend A2 passed
```

---

## 16. Resource adaptation without provider coupling

La policy cognitiva debe expresar **capacidades requeridas**, no marcas o runtimes concretos.

Ejemplo conceptual:

```text
need: independent factual verification
```

Puede satisfacerse, según infraestructura y autorización, mediante:

- modelo local especializado;
- segundo modelo local;
- frontier model conectado;
- retrieval/evidence service;
- regla/sistema simbólico;
- herramienta determinista;
- revisión humana.

La arquitectura no debe codificar:

```text
if assurance == A2:
    call VendorX
```

La selección concreta pertenecerá a futuras Model/Capability/Resource Governance.

---

## 17. Preferencia por un heavy generator, no prohibición absoluta

G0 propuso un solo modelo generativo pesado por defecto.

G1 aclara:

```text
one heavy generator by default
!=
never use a second model
```

Si:

- existe un déficit concreto;
- una segunda inferencia puede reducirlo materialmente;
- la operación está autorizada;
- recursos/presupuesto lo permiten;
- el required assurance floor lo justifica;

entonces un segundo modelo o verifier puede ser correcto.

La prohibición es contra el **always-on redundancy without demonstrated need**, no contra gastar recursos con propósito.

---

## 18. No majority vote as truth mechanism

Múltiples modelos pueden aportar evidencia independiente o diversidad de hipótesis.

Pero:

```text
3 votes > 2 votes
!=
truth
```

Una respuesta con mejor evidencia puede prevalecer sobre una mayoría de outputs sin soporte equivalente.

El ranking debe considerar calidad/autoridad/provenance de evidencia, no solo conteo de modelos.

---

## 19. Contradiction handling

Una contradicción material activa una decisión explícita.

Orden conceptual:

```text
1. detect conflict
2. compare source validity / authority / time / scope
3. resolve if one side has superior admissible evidence
4. otherwise reduce achievable assurance
5. expose or abstain when unresolved
```

La síntesis lingüística no puede ocultar contradicciones pendientes.

---

## 20. Auditability proportional to materiality

No se requiere un artefacto persistente enorme para toda respuesta.

La trazabilidad futura deberá ser proporcional.

Para decisiones materiales, un receipt/record compacto podría preservar:

```text
candidate identity
policy version
required assurance
achieved assurance
material evidence refs
source dispositions
contradiction disposition
verification steps used
resource class / budget disposition
final assurance outcome
evaluation time
```

No debe incluir chain-of-thought privado como requisito de auditabilidad.

No se aprueba ningún schema en G1.

---

## 21. Métricas candidatas para demostrar valor

Una futura implementación no deberá justificarse solo por intuición.

Métricas candidatas:

```text
unsupported_claim_escape_rate
supported_answer_rate
appropriate_abstention_rate
false_abstention_rate
contradiction_exposure_rate
source-attribution correctness
assurance-decision stability
average model calls per request
p95 latency
resource use by assurance level
external provider usage
cost per successfully assured response
```

Métrica prioritaria:

```text
unsupported_claim_escape_rate
```

Pero deberá observarse junto a `false_abstention_rate` para evitar un sistema que parezca seguro simplemente porque nunca responde.

---

## 22. Determinismo esperado

G1 no exige que dos generaciones tengan palabras idénticas.

Sí exige como objetivo de diseño:

```text
same material claims/evidence
+ same policy
+ same relevant state
+ same effective evaluation time
        ↓
same assurance classification
same contradiction disposition
same support floor
same ACCEPT/QUALIFY/ABSTAIN/BLOCK outcome
```

La superficie lingüística puede variar siempre que conserve las mismas afirmaciones materiales y límites de assurance.

---

## 23. Complejidad arquitectónica permitida

G1 no justifica crear ahora:

- `CognitiveAssuranceManager`;
- `ResponseAssuranceService`;
- nuevo microservicio;
- nuevo registry;
- nueva base de datos;
- nuevo event bus;
- nuevo graph engine;
- multi-agent orchestrator;
- nuevo Constitutional Engine runtime;
- provider abstraction adicional;
- persistent receipt store.

Primero debe demostrarse qué responsabilidad concreta no puede vivir en fronteras existentes.

Regla:

```text
new responsibility proved
→ evaluate component

new component imagined
→ NOT sufficient
```

---

## 24. Relación con RDD

RDD continúa siendo útil para Engineering Assurance por propiedades como:

```text
candidate binding
frozen scope
bounded review
lineage / evidence
review != delivery authority
```

G1 adapta solamente esas propiedades generales al plano cognitivo:

```text
candidate response
→ evidence-bound evaluation
→ bounded correction/verification
→ separately governed finalization
```

No se importa la máquina de estados de GentleAI ni se activa RDD Stage 2.

```text
RDD inspiration != Cognitive Authority
```

---

## 25. Relación con Evidence-Bound Cognition

El concepto `MALAK_EVIDENCE_BOUND_COGNITION_FOUNDATION.md` preserva las leyes candidatas.

Este G1 responde a una pregunta distinta:

> ¿Cuál es el mecanismo conceptual mínimo que permitiría aplicar esas leyes de forma proporcional y adaptable?

Separación:

```text
Evidence-Bound Cognition
→ intended cognitive laws

Progressive Cognitive Assurance G1
→ candidate decision mechanism
```

No existe todavía promoción constitucional.

---

## 26. Cuatro preguntas obligatorias

### 1. ¿Respeta Blueprint?

```text
PASS
```

- no acopla a modelo/provider/runtime;
- no toca Kernel;
- conserva separación de responsabilidades;
- no crea nuevos componentes todavía.

### 2. ¿Respeta Cognitive Constitution?

```text
PASS
```

- evidencia sobre especulación;
- incertidumbre explícita;
- proporcionalidad;
- minimización compatible con calidad esperada;
- trazabilidad;
- costo subordinado correctamente dentro de la resolución de conflictos existente.

### 3. ¿Respeta Governance?

```text
PASS
```

- evaluaciones no conceden autoridad;
- providers/verifiers no se autoautorizan;
- BLOCK por policy permanece separado de incertidumbre.

### 4. ¿Preserva/reduce complejidad del Kernel?

```text
PASS
Kernel delta = 0
```

---

## 27. Riesgo

Si esta dirección se promueve a enforcement runtime:

```text
risk_class = LEVEL 3 / HIGH
```

Motivo:

- afectaría qué información puede convertirse en respuesta final;
- tocaría semántica de confianza, evidencia y abstención;
- cualquier bypass podría permitir unsupported claims;
- cualquier exceso de bloqueo podría degradar utilidad.

Por tanto una implementación futura requerirá especificación cerrada, TDD, FULL 4R, bounded correction e independent validation.

---

## 28. Stop conditions para el siguiente gate

STOP / ESCALATE si el próximo diseño requiere:

- bajar el assurance floor por falta de recursos;
- un único score opaco como verdad;
- majority voting como autoridad;
- multi-agent/multi-model always-on;
- vendor/provider obligatorio;
- Kernel changes;
- Security authority changes;
- RAG o Memory persistente como prerequisito actual;
- persistent receipt store;
- interpretación constitucional libre por un LLM como única barrera;
- loops de verification/retrieval no acotados;
- RDD Stage 2;
- Sprint 7.12 automático;
- implementación antes de promoción normativa aplicable.

---

## 29. Gate posterior recomendado

G1 no autoriza implementación.

Antes de convertir esta dirección en runtime debe decidirse su relación normativa con la Cognitive Constitution.

Ruta recomendada:

```text
G1 design integrated
        ↓
Vault reconciliation / drift 0
        ↓
separate Constitutional Impact Review
        ↓
ADR / Blueprint / Cognitive Constitution path
only if approved
        ↓
closed enforcement specification
        ↓
implementation candidate
```

La promoción constitucional deberá respetar la regla de inmutabilidad vigente de la Cognitive Constitution.

---

## 30. Decisión G1

```text
G1 RESULT: PASS / ADAPT

SELECT:
- required assurance floor independent from resource availability
- deterministic checks first
- progressive assurance
- escalation-by-deficit
- bounded cognition
- explicit degradation
- provider/model/language agnostic capability selection
- ordered admissibility/ranking instead of opaque truth score
- ACCEPT / QUALIFY / ABSTAIN / BLOCK as candidate semantics
- auditability proportional to materiality

PRESERVE:
- Human in Control
- evidence != authority
- confidence != truth
- consensus != truth
- RDD Stage 1 only

REJECT AS DEFAULT:
- cheapest-path-first when it lowers assurance
- multi-model voting
- always-on verifier
- agent debate/swarm
- provider coupling
- silent quality downgrade

IMPLEMENTATION AUTHORIZED: NO
CONSTITUTIONAL CHANGE AUTHORIZED: NO
RDD STAGE 2 AUTHORIZED: NO
```
