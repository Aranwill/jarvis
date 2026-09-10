---
title: Malāk Cognitive Assurance — Constitutional Impact Review G0/G1
status: gate_candidate
authority: constitutional_impact_review
language: es
as_of_date: 2026-09-10
source_baseline: c16c23e14cbd2e34c3abdba085a113dd0a37e0f5
vault_drift_zero_observed: true
implementation_authorized: false
constitutional_change_authorized: false
blueprint_change_authorized: false
adr_creation_authorized: false
rdd_stage_2_authorized: false
candidate_content_identity_g2_authorized: false
sprint_7_12_authorized: false
related:
  - docs/project/concepts/MALAK_EVIDENCE_BOUND_COGNITION_FOUNDATION.md
  - docs/project/sprints/proposals/MALAK-COGNITIVE-ASSURANCE-G0-RESEARCH-EVIDENCE.md
  - docs/project/sprints/proposals/MALAK-COGNITIVE-ASSURANCE-G1-PROGRESSIVE-DESIGN.md
  - docs/governance/cognitive_constitution.md
  - docs/governance/governance_constitution.md
  - docs/architecture/blueprint.md
  - docs/project/sprints/proposals/CONSTITUTIONAL-ASSURANCE-G1-DESIGN.md
  - AGENTS.md
---

# Malāk Cognitive Assurance — Constitutional Impact Review G0/G1

## 1. Estado de autoridad

El Owner autorizó exclusivamente el Constitutional Impact Review G0/G1 de la
dirección Evidence-Bound / Progressive Cognitive Assurance.

Esta unidad puede:

- comparar principios candidatos contra la Cognitive Constitution vigente;
- detectar duplicación, gaps y conflictos;
- clasificar impacto constitucional;
- proponer el delta normativo mínimo que una futura unidad podría evaluar;
- delimitar qué pertenece a Constitución, Blueprint, ADR, specification o policy;
- definir stop conditions para evitar sobreingeniería.

Esta unidad NO puede:

- modificar Cognitive Constitution;
- modificar Governance Constitution;
- modificar Blueprint;
- crear, aceptar o numerar definitivamente un ADR;
- crear contratos, APIs, clases o enums;
- implementar Response Assurance;
- modificar `src/` o `tests/`;
- autorizar Candidate Content Identity G2;
- autorizar Persistence Authorization;
- autorizar RDD Stage 2;
- abrir Sprint 7.12;
- ampliar autoridad.

```text
Review != Amendment != Specification != Implementation != Authority
```

---

## 2. Baseline congelado

Repositorio oficial:

```text
Aranwill/jarvis
main
c16c23e14cbd2e34c3abdba085a113dd0a37e0f5
```

Estado downstream observado antes de esta unidad:

```text
Project Vault reconciled to Malāk c16c23e1...
final sync run: base == head
changed_files = 0
document_candidates = 0
validation_findings = 0
conclusion = pass
proposal_created = false
```

La reconciliación del Vault no concede autoridad normativa; únicamente elimina
drift downstream antes del review.

---

## 3. Pregunta G0

```text
¿La dirección Cognitive Assurance requiere realmente nuevas leyes
constitucionales, o puede derivarse de principios ya vigentes?
```

Resultado:

```text
G0 RESULT: PASS

finding:
la mayor parte de la intención ya existe de forma parcial o implícita;
no se justifica promover las 15 CAL como 15 leyes nuevas.

required action:
minimal normative delta only
```

---

## 4. Cobertura constitucional ya existente

La Cognitive Constitution vigente ya contiene soporte material para gran parte
de Evidence-Bound Cognition:

```text
CC-002  No asumir
CC-003  Evidencia sobre especulación
CC-004  Transparencia Cognitiva
CC-005  Proporcionalidad
CC-006  Minimización Cognitiva
CC-007  Trazabilidad
CC-008  Coherencia
CC-009  Consistencia Temporal
```

También establece:

- gestión explícita de incertidumbre;
- evaluación de evidencia y confianza en decisiones;
- aprendizaje verificable/auditable/versionado;
- provenance/origen y confianza para Knowledge;
- prohibición de modificación autónoma de la Constitución;
- precedencia normativa.

Por tanto, Cognitive Assurance debe reforzar esta Constitución, no crear una
segunda constitución epistemológica paralela.

---

## 5. Cobertura arquitectónica ya existente

El Blueprint vigente ya protege propiedades relevantes:

```text
P-005 Human in Control
P-006 Zero Trust
P-007 Model Agnostic
P-009 Everything is Observable
P-010 Everything is Auditable
P-011 Runtime Independence
P-012 Specification & Verification First
```

Además:

```text
R-019 resultados/evidencia pueden retornar upstream sin transferir control
R-020 retorno de evidencia no concede autoridad
R-021 prohibición de bypass de capas de autoridad/validación
```

Esto significa que una futura Response Assurance no necesita inventar una nueva
teoría de autoridad ni un nuevo principio de no-bypass desde cero.

---

## 6. Clasificación G0 de las leyes candidatas CAL-001..015

La clasificación usada es cerrada para este review:

```text
EXISTING
CLARIFY
NEW_CONSTITUTIONAL
POLICY_ONLY
DEFER
```

### CAL-001 — Generation is not Answer

```text
DISPOSITION: NEW_CONSTITUTIONAL
```

Motivo:

La Constitución actual gobierna decisiones y evidencia, pero no expresa de forma
inequívoca que una salida de modelo/provider/tool/agente sea solamente un
candidate y no pueda auto-promoverse a Final Response.

Principio mínimo candidato:

```text
Generation != Finalization
```

No congela pipeline ni componente.

### CAL-002 — Best Supported over Most Probable

```text
DISPOSITION: CLARIFY
OWNER: CC-003
```

`CC-003 — Evidencia sobre especulación` ya contiene la dirección normativa.

Una futura enmienda puede aclarar que probabilidad, persuasión o confidence del
modelo no sustituyen soporte material.

No se justifica una ley independiente.

### CAL-003 — Evidence Binding before Material Reliance

```text
DISPOSITION: NEW_CONSTITUTIONAL
```

La Constitución exige evidencia, pero no exige hoy que afirmaciones materiales
que dependan de evidencia puedan ser ligadas a su soporte antes de finalización.

La obligación debe ser proporcional al riesgo y materialidad.

No implica provenance por token ni citation obligatoria para toda frase.

### CAL-004 — Retrieved does not mean Trusted

```text
DISPOSITION: CLARIFY
OWNER: CC-003 + CC-008 + Zero Trust
```

Principio a preservar:

```text
retrieved != trusted
memory != truth
knowledge != immutable truth
model output != authority
```

La taxonomía concreta de trust, poisoning, quarantine y source disposition
pertenece a specifications/policies futuras.

### CAL-005 — Validation before Finalization

```text
DISPOSITION: NEW_CONSTITUTIONAL
```

Existe validación constitucional de operaciones y existe Specification &
Verification First para ingeniería, pero falta una obligación explícita de que
una respuesta material atraviese las validaciones cognitivas aplicables antes de
convertirse en Final Response.

Debe formularse de manera proporcional para no convertir preguntas triviales en
workflows pesados.

### CAL-006 — Contradictions must be Resolved or Exposed

```text
DISPOSITION: CLARIFY
OWNER: CC-004 + CC-008 + CC-009
```

Coherencia, consistencia temporal y transparencia ya cubren la intención.

Una futura aclaración debe impedir que una síntesis lingüística oculte un
conflicto material no resuelto.

No requiere una ley nueva.

### CAL-007 — Consensus is not Truth

```text
DISPOSITION: CLARIFY
OWNER: CC-003
```

La evidencia debe prevalecer sobre especulación. El acuerdo de modelos/agentes es
una señal posible, no autoridad ni prueba suficiente por conteo.

La política de ensembles o judges queda fuera de la Constitución.

### CAL-008 — Deterministic Acceptance and Ranking

```text
DISPOSITION: POLICY_ONLY
```

Como objetivo de ingeniería es valioso:

```text
same material evidence
+ same applicable policy
+ same relevant state
+ same evaluation time
→ stable material assurance decision
```

Pero congelar exactitud de ranking como ley constitucional puede impedir futuras
técnicas legítimas y crear falsa precisión sobre evaluación semántica.

La Constitución puede favorecer reglas objetivas y explícitas cuando existan;
el algoritmo exacto de ranking/precedencia pertenece a specification/policy
versionada.

### CAL-009 — Uncertainty over Fabrication

```text
DISPOSITION: EXISTING
OWNER: CC-002 + uncertainty management
```

La Constitución ya prohíbe inventar información ante dudas razonables y ordena
indicar incertidumbre, limitar alcance o solicitar aclaración.

No crear duplicado.

### CAL-010 — Explainable Selection without Private Chain-of-Thought Dependence

```text
DISPOSITION: CLARIFY
OWNER: CC-004 + CC-007
```

Transparencia y trazabilidad ya justifican un rationale verificable.

Debe aclararse que auditabilidad no exige almacenar ni exponer chain-of-thought
privado.

El formato concreto del rationale/receipt es policy/specification.

### CAL-011 — More Cognition does not Mean More Authority

```text
DISPOSITION: EXISTING
OWNER: Blueprint / Governance authority model
```

El Blueprint ya establece que resultados y evidencia no transfieren autoridad y
prohíbe bypass/ascenso de control.

No duplicar esta regla dentro de Cognitive Constitution salvo referencia
explicativa estrictamente necesaria.

### CAL-012 — Applicable Assurance Gates are Non-Bypassable

```text
DISPOSITION: CLARIFY
OWNER: future constitutional finalization rule + Blueprint R-021
```

El no-bypass ya existe arquitectónicamente.

Lo que falta es declarar que la transición a Final Response también es una
transición protegida cuando existan assurance gates aplicables.

No requiere una nueva capa por sí mismo.

### CAL-013 — Evidence Freshness and Scope Matter

```text
DISPOSITION: CLARIFY
OWNER: CC-008 + CC-009
```

Temporalidad ya está regulada y contexto/scope forman parte de coherencia.

Debe preservarse que:

```text
newer != automatically superior
out-of-scope authoritative source != applicable truth
```

Los algoritmos de precedencia permanecen en policy/specification.

### CAL-014 — Source Identity and Content Integrity before Durable Reliance

```text
DISPOSITION: DEFER
```

La dirección es compatible con Zero Trust y Knowledge provenance, pero la
arquitectura aún no posee Candidate Content Identity G2, propagación end-to-end,
Persistence Authorization ni durable Memory/Knowledge reliance.

Promover ahora una formulación demasiado concreta correría delante de las
fronteras materializadas.

Revisar nuevamente después de Candidate Content Identity + binding suficiente.

### CAL-015 — Reconsideration must be Bounded

```text
DISPOSITION: CLARIFY
OWNER: CC-005 + CC-006
```

Proporcionalidad y minimización ya cubren la dirección.

La futura aclaración puede exigir que la reevaluación converja y no sea ilimitada.

Budgets concretos permanecen policy/configuration.

---

## 7. Resultado de cobertura

```text
EXISTING:              CAL-009, CAL-011
CLARIFY:               CAL-002, CAL-004, CAL-006, CAL-007,
                       CAL-010, CAL-012, CAL-013, CAL-015
NEW_CONSTITUTIONAL:    CAL-001, CAL-003, CAL-005
POLICY_ONLY:           CAL-008
DEFER:                 CAL-014
```

Conclusión:

```text
15 candidate laws
→ 3 true constitutional gaps
→ 8 clarifications
→ 2 already covered
→ 1 policy-level mechanism
→ 1 deferred dependency
```

Esta reducción es deliberada y aplica Complexity Budget al plano normativo.

---

## 8. G1 — Diseño del delta normativo mínimo

```text
G1 RESULT: PASS / MINIMAL PROMOTION PATH
```

No se recomienda crear tres leyes nuevas independientes si pueden expresarse con
menor superficie normativa.

G1 propone consolidar `CAL-003 + CAL-005 + CAL-012` como una única obligación de
**Evidence-Bound Finalization**, manteniendo `CAL-001` como separación conceptual
independiente.

Por tanto, el delta constitucional futuro recomendado es como máximo:

```text
NEW PRINCIPLE A
Generation does not finalize authority

NEW PRINCIPLE B
Material final responses require applicable evidence-bound assurance
before finalization and cannot bypass that assurance
```

Más aclaraciones acotadas sobre principios existentes cuando sean estrictamente
necesarias.

Objetivo:

```text
minimum new law
maximum semantic coverage
```

---

## 9. Candidate constitutional semantics — NO amendment yet

### 9.1 Candidate A — Generation / Finalization Separation

Semántica mínima candidata:

> Outputs de modelos, providers, agents, tools, retrieval, Memory o Knowledge son
> información/candidatos según su naturaleza y no adquieren por sí mismos estado
> de Final Response, verdad o autoridad.

Propiedades:

```text
model output != final answer
retrieval result != final answer
tool result != final answer
candidate != accepted response
```

No exige múltiples candidatos ni múltiples modelos.

### 9.2 Candidate B — Evidence-Bound Finalization

Semántica mínima candidata:

> Toda respuesta material deberá satisfacer las validaciones cognitivas
> aplicables a su riesgo, evidencia e incertidumbre antes de ser finalizada. Las
> afirmaciones que dependan de evidencia deberán poder justificar su soporte con
> granularidad proporcional. Una validación aplicable no podrá ser omitida por un
> componente downstream.

Propiedades:

```text
material claim
→ applicable assurance
→ supported / qualified / abstained / blocked
→ final response
```

No congela nombres de outcomes, levels, algorithms o providers.

---

## 10. Clarificaciones recomendadas sobre leyes existentes

Estas son candidatas de redacción futura, no edits autorizados.

### CC-002

Preservar explícitamente:

```text
uncertainty > fabrication
supported partial answer > unsupported complete answer
```

### CC-003

Aclarar:

```text
best supported > most probable
confidence != truth
consensus != evidence sufficiency
retrieved != trusted by retrieval alone
```

### CC-004 / CC-007

Aclarar que una decisión material debe ser justificable mediante evidencia,
restricciones, incertidumbre y disposición final, sin requerir private
chain-of-thought.

### CC-005 / CC-006

Aclarar:

```text
deterministic checks first when sufficient
additional cognition only when it addresses a material deficit
reconsideration must remain bounded
```

Sin congelar budgets universales.

### CC-008 / CC-009

Aclarar que contradicciones materiales deben resolverse o exponerse y que scope,
temporalidad y autoridad de evidencia participan en la resolución.

---

## 11. Lo que debe permanecer fuera de la Constitución

La Constitución NO debe contener:

```text
A0 / A1 / A2 / A3 exact IDs
ACCEPT / QUALIFY / ABSTAIN / BLOCK exact enums
number of model calls
number of sources
number of verifier passes
specific providers
specific LLMs
specific RAG implementation
GraphRAG requirement
confidence thresholds
ranking weights
magic composite score
receipt JSON schema
receipt retention period
latency targets
token budgets
VRAM/CPU budgets
provider fallback order
majority-vote algorithm
```

Estas decisiones son evolutivas y deben vivir en specifications, policies o
configuration según corresponda.

```text
Constitution = durable cognitive law
Policy        = versioned operational decision
Configuration = environment/runtime choice
```

---

## 12. Impacto candidato sobre Blueprint

La futura promoción constitucional obligará a revisar Blueprint, pero G1 NO
recomienda crear hoy una nueva capa `Response Assurance Layer`.

El delta arquitectónico mínimo a evaluar es declarar la transición:

```text
Candidate Response
      ↓
Applicable Assurance Decision
      ↓
Final Response
```

como **protected finalization transition**.

Propiedad candidata:

```text
no model/provider/tool/agent/retrieval component
may publish a material candidate directly as Final Response
when applicable assurance is unmet
```

Esto puede implementarse más adelante mediante un contrato/boundary existente o
uno nuevo si una responsabilidad real lo demuestra.

G1 deliberadamente NO selecciona owner runtime.

---

## 13. No crear un componente por anticipación

Stop rule:

```text
constitutional requirement
!= automatic new service
!= automatic new layer
!= automatic new manager
```

Antes de crear `ResponseAssuranceService`, `CognitiveAssuranceEngine` o nombre
equivalente deberá demostrarse que:

- existe una responsabilidad única;
- no cabe limpiamente en una frontera existente;
- tiene consumidores reales;
- el no-bypass puede garantizarse;
- puede probarse de manera objetiva;
- no duplica Constitutional Engine, Reasoning Engine o Governance;
- el costo de arquitectura está justificado.

Si no se demuestra:

```text
DO NOT CREATE COMPONENT
```

---

## 14. Relación con Constitutional Assurance existente

`CONSTITUTIONAL-ASSURANCE-G1-DESIGN.md` establece un precedente importante:

- mecanizar solamente invariantes objetivas;
- no interpretar lenguaje constitucional completo en runtime;
- usar evidencia determinista cuando sea posible;
- declarar falsos negativos y alcance explícitamente;
- evitar servicios universales prematuros.

La futura Cognitive Assurance debe reutilizar esa disciplina.

Una vez exista una finalization boundary material, Constitutional Assurance podrá
evaluar invariantes estructurales objetivas de no-bypass.

No se diseñan esos tests en esta unidad porque la frontera runtime todavía no
existe.

---

## 15. Relación con RDD

RDD Stage 1 continúa como fuente metodológica de propiedades:

```text
candidate identity
bound evidence
bounded review
receipt/evidence != authority
human delivery authority
```

Cognitive Assurance adapta esas propiedades al dominio de respuestas, pero:

```text
RDD != Cognitive Constitution
RDD != truth mechanism
RDD != authority
RDD Stage 2 remains not authorized
```

La promoción constitucional deberá ser Malāk-native y seguir siendo válida aun
si GentleAI/RDD cambia o desaparece.

---

## 16. Resource flexibility y assurance floor

G1 constitucional NO debe convertir recursos en ley tecnológica.

Se preserva la dirección:

```text
required assurance floor
is driven by risk/materiality/evidence need

available resources
select the authorized route
```

Pero los hard limits siguen siendo reales.

Si el assurance requerido no puede alcanzarse:

```text
explicit limitation / qualification / abstention / block
```

Nunca degradación silenciosa.

Los budgets y fallback routes pertenecen a futura Resource/Model Governance y
Cognitive Assurance policy.

---

## 17. Métrica constitucional vs métricas operativas

La Constitución no debe congelar métricas de benchmark concretas.

Puede preservar la obligación general de no presentar como plenamente soportada
una afirmación que no haya alcanzado el assurance aplicable.

Métricas como:

```text
unsupported_claim_escape_rate
false_abstention_rate
supported_answer_rate
assurance decision stability
model calls
latency
resource use
```

pertenecen a validation/evaluation specifications.

---

## 18. Secuencia de promoción recomendada

Este review NO autoriza ejecutar la secuencia.

Si el Owner aprueba promoción después de merge de este record:

```text
1. ADR candidate
   - problema
   - opciones
   - decisión normativa mínima
   - owner arquitectónico todavía evaluado

2. Blueprint version candidate
   - protected finalization transition
   - no-bypass architecture requirement
   - no provider/model coupling

3. Cognitive Constitution amendment candidate
   - Generation/Finalization separation
   - Evidence-Bound Finalization
   - bounded clarifications only

4. independent review of normative consistency

5. human approval/merge

6. separate Response Assurance specification gate

7. only then possible implementation G2/G3 path
```

La numeración del ADR y la versión exacta del Blueprint no se congelan aquí.

---

## 19. Stop conditions

Detener y abrir una unidad separada si aparece necesidad de:

- crear un runtime service;
- modificar Constitutional Engine;
- modificar Reasoning Engine;
- modificar Interface Layer;
- crear API pública;
- introducir un new response type;
- implementar ranking;
- implementar RAG/Memory/Knowledge;
- introducir provider/model routing;
- crear receipt schema;
- modificar Security behavior;
- implementar resource scheduling;
- diseñar Candidate Content Identity propagation;
- activar RDD Stage 2.

Ninguna de esas necesidades puede entrar silenciosamente en el paquete normativo.

---

## 20. Resultado final G0/G1

```text
CONSTITUTIONAL IMPACT REVIEW
G0: PASS
G1: PASS / MINIMAL PROMOTION PATH
```

Finding principal:

```text
Malāk already has most of the cognitive law required.
The correct evolution is reinforcement, not constitutional duplication.
```

Delta normativo mínimo candidato:

```text
A. Generation != Finalization
B. Material Finalization requires applicable evidence-bound assurance
```

Con clarificaciones acotadas de leyes existentes, no proliferación de leyes.

Principios operativos conservados fuera de Constitución:

```text
progressive assurance
resource-adaptive execution
deterministic ranking mechanics
A0..A3 placeholders
bounded budgets
provider selection
verification routes
receipts
metrics
```

Dependencia diferida:

```text
CAL-014 / durable content identity and integrity
→ revisit after Candidate Content Identity + end-to-end binding
```

---

## 21. Estado de autorización al cerrar este record

```text
Cognitive Assurance G0 research                    integrated previously
Cognitive Assurance G1 progressive design          integrated previously
Constitutional Impact Review G0/G1                 candidate in this unit

Cognitive Constitution modification                NOT AUTHORIZED
Blueprint modification                             NOT AUTHORIZED
ADR creation/acceptance                            NOT AUTHORIZED
Response Assurance specification                   NOT AUTHORIZED
Response Assurance implementation                  NOT AUTHORIZED
Candidate Content Identity G2                      NOT AUTHORIZED
Persistence Authorization                          NOT AUTHORIZED
RDD Stage 2                                        NOT AUTHORIZED
Sprint 7.12                                        NOT AUTHORIZED
```

La próxima decisión pertenece exclusivamente al Owner después de revisar este
candidate.
