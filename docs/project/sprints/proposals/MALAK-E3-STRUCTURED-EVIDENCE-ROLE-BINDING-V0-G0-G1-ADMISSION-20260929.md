---
title: Malāk E3 — Structured Evidence Role Binding V0 — G0/G1 Admission
status: design_candidate
authority: non_normative
document_role: admission_design
language: es
created: 2026-09-29
baseline_commit: 87e770b4d7e0e6c01ac24f9cc09bbe22068ea7e0
source_findings:
  - E008-SG-02
  - E008-SG-03
risk_class: 3
critical_contract: true
implementation_authorized: false
red_authorized: false
green_authorized: false
runtime_execution_authorized: false
self_modification_authorized: false
rdd_stage_2_authorized: false
authority_effect: none
related:
  - docs/project/status/MALAK-EIGHTH-U01-SEMANTIC-GROUNDING-AUDIT-20260927.md
  - docs/project/sprints/proposals/MALAK-E3-SEMANTIC-GROUNDING-HARDENING-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-E3-GOVERNED-RELATION-COVERAGE-UNIQUENESS-V0-G0-G1-ADMISSION-20260929.md
  - docs/project/concepts/MALAK_EVIDENCE_BOUND_COGNITION_FOUNDATION.md
  - src/malak/capabilities/_engineering_analysis.py
  - src/malak/capabilities/engineering_analyze.py
  - src/malak/capabilities/engineering_propose.py
---

# Malāk E3 — Structured Evidence Role Binding V0 — G0/G1 Admission

## 1. Propósito

Evaluar y congelar el siguiente hardening mínimo de E3 después de integrar:

~~~text
Governed Engineering Relation Catalog Foundation     PR #212
E3 Governed Relation Consumption V0                  PR #215
E3 Governed Relation Coverage & Uniqueness V0        PR #218
CURRENT_STATE post-PR #218                           PR #219
~~~

El objetivo es reducir el gap material restante de **E008-SG-02** sin afirmar
una garantía semántica que Malāk todavía no ejecuta.

La pregunta exacta de admisión es:

> ¿Puede E3 hacer explícita y verificable la función estructural de cada
> referencia de evidencia dentro de un finding gobernado, manteniendo separado
> ese binding de una futura verificación de entailment semántico?

La respuesta de este gate es **sí**, con alcance focalizado y sin segundo modelo.

Este documento no autoriza RED, GREEN, runtime, Self-Review ni RDD Stage 2.

---

## 2. Baseline exacto

~~~text
repository   Aranwill/jarvis
branch       main
baseline     87e770b4d7e0e6c01ac24f9cc09bbe22068ea7e0
tree         2dbeb7060d0d4940e21624c790ce804b6274264e
~~~

Cierre inmediatamente anterior:

~~~text
PR #218
candidate    b6d3d7d42c69610d1e26fbee2ad1778ee45755d0
merge        70989b1878f1f4f9289c65611c3d7b561d5ae286
Validation #668 post-merge
1633 passed Ubuntu + Windows

PR #219
candidate    b02353b7b6558648bcc849b3afefe87bda811355
merge        87e770b4d7e0e6c01ac24f9cc09bbe22068ea7e0
Validation #670 post-merge
1633 passed Ubuntu + Windows
compileall PASS
candidate identity PASS
candidate diff PASS
~~~

La rama documental de PR #219 fue eliminada después del merge.

---

## 3. Trigger material vigente

La auditoría del Octavo U01 preserva:

~~~text
E008-SG-01  SEMANTIC_GROUNDING_GAP
E008-SG-02  EVIDENCE_BINDING_GAP
E008-SG-03  ASSURANCE_LABEL_BOUNDARY
~~~

Después de PR #212, PR #215 y PR #218:

~~~text
relation identity                  hardened
relation membership                hardened
relation set coverage              hardened
relation uniqueness                hardened
canonical relation order           hardened
catalog capacity preflight         hardened
~~~

Eso reduce de forma determinista la clase de inconsistencia estructural
observada en E008-SG-01.

Permanece abierto:

~~~text
known evidence id
!= semantically supporting evidence
~~~

y permanece explícito:

~~~text
GROUNDED
-> structurally grounded to a real evidence packet
!= semantic entailment verified
~~~

Por tanto:

~~~text
E008-SG-02  OPEN
E008-SG-03  BOUNDARY PRESERVED
~~~

---

## 4. Estado técnico actual

Un finding relation-aware de E3 contiene actualmente:

~~~text
relation_id
classification
statement
rationale
evidence_refs
~~~

El parser valida:

- JSON y claves exactas;
- clasificación permitida;
- IDs conocidos;
- ausencia de duplicados;
- presencia combinada de R + K para clases relacionales;
- relation_id allowlisted;
- cobertura exacta y única del catálogo gobernado.

No puede distinguir estructuralmente:

~~~text
ref usada como soporte de implementación
ref usada como soporte de conocimiento
ref usada como limitación o contraevidencia
base exacta de un UNRESOLVED
~~~

La lista plana:

~~~text
evidence_refs
~~~

preserva identidad, pero no rol epistemológico.

---

## 5. Evidencia histórica ya admitida

El diseño:

~~~text
MALAK-E3-SEMANTIC-GROUNDING-HARDENING-G0-G1-DESIGN.md
~~~

evaluó cuatro opciones.

Disposición preservada:

~~~text
prompt-only patch                        REJECT AS SOLE CONTROL
general deterministic semantic entailment REJECT
mandatory second-model validator          OBSERVE
structured binding + explicit assurance   ADAPT / CANDIDATE FOR HARDENING
~~~

Ese diseño propuso separar, por finding:

~~~text
supporting_repository_refs
supporting_knowledge_refs
limiting_or_counterevidence_refs
uncertainty_basis
~~~

El catálogo gobernado requerido para evitar relation keys libres ya fue
materializado posteriormente mediante PR #212, consumido por PR #215 y
endurecido por PR #218.

No existe razón para reabrir esas decisiones.

---

## 6. Decisión G0

~~~text
unit:
E3 Structured Evidence Role Binding V0

disposition:
ADAPT

scope:
focused E3 with non-empty governed relation catalog only

generic E3:
UNCHANGED

E4:
UNCHANGED

second model:
NO

semantic judge:
NO

relation-specific evidence allowlist:
NOT IN THIS V0

Structural Evidence E2 -> E3/E4:
DEFERRED / NOT IN SCOPE

authority_effect:
none
~~~

Resultado:

~~~text
G0 = PASS
~~~

---

## 7. Contrato candidato G1

Para E3 focalizado con catálogo gobernado no vacío, el output model-facing
de cada finding deberá representar exactamente:

~~~text
relation_id
classification
statement
rationale
supporting_repository_refs
supporting_knowledge_refs
limiting_or_counterevidence_refs
uncertainty_basis
~~~

La lista plana model-facing:

~~~text
evidence_refs
~~~

dejará de formar parte del schema **sólo en este path relation-aware**.

El contrato genérico con catálogo vacío conserva exactamente el formato legacy.

### 7.1 uncertainty_basis

Para evitar optional-field ambiguity y mantener exact-key schemas, V0 utiliza:

~~~text
NONE
CURRENT_MATERIAL_AMBIGUITY
INSUFFICIENT_SUPPLIED_EVIDENCE
UNRESOLVED_CURRENT_PRECEDENCE
~~~

Reglas:

~~~text
classification != UNRESOLVED
-> uncertainty_basis == NONE

classification == UNRESOLVED
-> uncertainty_basis != NONE
~~~

Esto adapta la intención histórica “uncertainty_basis sólo aplica a UNRESOLVED”
sin depender de claves condicionalmente ausentes.

---

## 8. Binding estructural exacto

El schema relation-aware deberá construirse después de recolectar el evidence
packet exacto.

Malāk ya posee una frontera reusable:

~~~text
response_json_schema_builder(
    repository_evidence,
    knowledge_evidence
)
~~~

Por tanto el schema puede exponer enums ligados al packet:

~~~text
supporting_repository_refs
-> enum exacto de refs R presentes

supporting_knowledge_refs
-> enum exacto de refs K presentes

limiting_or_counterevidence_refs
-> enum exacto de R + K presentes
~~~

El parser deberá repetir la validación fail-closed aunque el provider aplique
structured output.

No se confía en el schema remoto como único enforcement.

---

## 9. Reglas deterministas V0

### 9.1 Known-ref binding

Toda ref debe existir en el mismo packet exacto.

### 9.2 Role correctness

~~~text
supporting_repository_refs
-> sólo R refs

supporting_knowledge_refs
-> sólo K refs
~~~

Una K ref en repository support o una R ref en knowledge support falla cerrado.

### 9.3 Duplicate / overlap

No se permiten:

- duplicados dentro de una lista;
- una misma ref simultáneamente como supporting y limiting/counterevidence.

### 9.4 Relational classifications

Para:

~~~text
ALIGNED
PARTIAL
GAP
CONTRADICTION
~~~

se exige:

~~~text
supporting_repository_refs != empty
supporting_knowledge_refs  != empty
uncertainty_basis          == NONE
~~~

### 9.5 UNRESOLVED

Para:

~~~text
UNRESOLVED
~~~

se exige:

~~~text
uncertainty_basis != NONE
total bound refs >= 1
~~~

Se conserva la semántica de E3 Epistemic Calibration:

~~~text
CURRENT_MATERIAL_AMBIGUITY
INSUFFICIENT_SUPPLIED_EVIDENCE
UNRESOLVED_CURRENT_PRECEDENCE
~~~

### 9.6 Current precedence

Cuando:

~~~text
uncertainty_basis == UNRESOLVED_CURRENT_PRECEDENCE
~~~

al menos una K ref ligada debe corresponder a una fuente con rol:

~~~text
GOVERNING / normative
OR
APPROVED_SPECIFICATION / normative_subordinate
~~~

Una explicación de precedence sustentada únicamente por fuente conceptual,
derived o non-normative no es suficiente.

---

## 10. Representación interna y compatibilidad

V0 debe preservar una única representación compartida de analysis.

La dirección candidata mínima es extender el finding interno para conservar:

~~~text
supporting_repository_refs
supporting_knowledge_refs
limiting_or_counterevidence_refs
uncertainty_basis
~~~

sin eliminar la vista canónica agregada:

~~~text
evidence_refs
~~~

La vista agregada se deriva determinísticamente de los roles y existe sólo para
compatibilidad interna donde sea necesario.

No puede utilizarse para borrar nuevamente la distinción de roles en el renderer
relation-aware.

### Orden canónico de la unión

~~~text
supporting_repository_refs
then supporting_knowledge_refs
then limiting_or_counterevidence_refs
~~~

Cada grupo conserva orden estable y no contiene duplicados.

---

## 11. Assurance explícito sin sobredeclaración

El renderer relation-aware deberá mantener visible:

~~~text
status: GROUNDED
semantic_assurance: NOT_VERIFIED
authority_effect: none
~~~

Interpretación:

~~~text
GROUNDED
-> packet structurally valid and bound

semantic_assurance: NOT_VERIFIED
-> this gate did not prove entailment
~~~

No se introducen:

~~~text
SEMANTICALLY_REVIEWED
SEMANTICALLY_VERIFIED
truth score
confidence score
automatic acceptance
~~~

E008-SG-03 permanece una frontera explícita, no un estado resuelto por nombre.

---

## 12. Qué garantiza V0

Puede garantizar determinísticamente:

- identidad exacta de refs;
- separación R/K por rol;
- no duplicación y no overlap incompatible;
- base explícita de UNRESOLVED;
- requirement de autoridad documental mínima para precedence;
- binding al mismo packet, baseline y focus;
- compatibilidad de catálogo;
- fail-closed ante malformed/unknown refs;
- assurance real expuesto como no verificado;
- authority effect cero.

---

## 13. Qué NO garantiza V0

No demuestra:

~~~text
the cited line semantically entails the statement
the classification is true
all material counterevidence was found
all material counterevidence was cited
relation-specific evidence sufficiency
general semantic consistency between different relations
semantic truth
~~~

Por ello:

~~~text
E008-SG-02
-> remains OPEN
-> receives deterministic structural hardening
-> MUST NOT be declared CLOSED by this V0 alone
~~~

Un futuro semantic reviewer, relation-specific evidence scope o mecanismo
equivalente requiere gate separado si la evidencia posterior demuestra necesidad.

---

## 14. E4 y consumers

### E4

Engineering Propose continúa usando su analysis relation-less legacy:

~~~text
allowed_relation_ids == ()
flat evidence_refs
existing eligibility semantics
~~~

No se hace E4 relation-aware.

No cambia:

~~~text
GAP/PARTIAL + finding refs + evidence refs + Owner authorization
UNRESOLVED / CONTRADICTION blocking
all ALIGNED -> no change
~~~

### Internal Interaction

El harness focalizado puede requerir adaptación de fixture para emitir el nuevo
schema relation-aware.

Si ocurre:

~~~text
test-only compatibility correction
!= production scope expansion
~~~

El terminal mapper no cambia por inferencia lateral.

---

## 15. RED causal futuro

RED requiere autorización explícita posterior.

Matriz mínima:

~~~text
R01 relation-aware schema requires exact role-separated fields
    and does not accept flat model-facing evidence_refs

R02 K ref in supporting_repository_refs fails closed

R03 R ref in supporting_knowledge_refs fails closed

R04 unknown, duplicate or supporting/counter overlap fails closed

R05 relational classification missing repository or knowledge support fails closed

R06 UNRESOLVED with NONE/invalid uncertainty_basis fails closed

R07 non-UNRESOLVED with non-NONE uncertainty_basis fails closed

R08 UNRESOLVED_CURRENT_PRECEDENCE backed only by non-normative K refs fails closed

R09 valid role-bound finding is accepted and rendered with
    semantic_assurance: NOT_VERIFIED

R10 empty governed catalog preserves exact generic E3 contract

R11 E4 legacy relation-less analysis remains unchanged
~~~

Expected current behavior:

~~~text
R01-R09 contain causal RED coverage
R10-R11 compatibility guards remain GREEN
~~~

No RED se materializa en este gate.

---

## 16. Candidate GREEN futuro — scope máximo

Sólo si RED es autorizado y demuestra las causas previstas.

Archivos productivos candidatos:

~~~text
src/malak/capabilities/_engineering_analysis.py
src/malak/capabilities/engineering_analyze.py
~~~

Tests candidatos:

~~~text
tests/test_e3_structured_evidence_role_binding_v0.py
tests/test_engineering_analyze.py                   # only if compatibility requires
tests/test_internal_interaction_test_v0_harness.py # only if compatibility requires
tests/test_engineering_propose.py                  # compatibility guard only if required
~~~

No se autoriza modificar:

~~~text
src/malak/capabilities/_engineering_evidence.py
src/malak/capabilities/engineering_propose.py
Kernel
Planner
CapabilityRegistry
Memory
SecurityContext
runtime/provider
Conversation
governance
Blueprint
Structural Evidence
Structural Delta
persistence
~~~

---

## 17. Correction Budget futuro

~~~text
max correction rounds: 2
scope expansion: prohibited
new material requirement: STOP -> separate gate
~~~

Un fixture incompatible puede corregirse sólo si:

- el defecto es estrictamente de compatibilidad con el nuevo schema autorizado;
- no modifica semántica productiva;
- la correction permanece dentro de tests afectados.

---

## 18. Malāk Alignment Matrix

| Fuente | Clase | Invariante | Disposición | Efecto |
| --- | --- | --- | --- | --- |
| Cognitive Constitution | normativa | evidencia > especulación; trazabilidad; soporte proporcional | ADOPT | refs por rol y base explícita |
| Governance Constitution | normativa | Human in Control | ADOPT | ningún binding autoriza |
| Blueprint | normativa | Capability First; Kernel pequeño | ADOPT | cambio limitado a E3 |
| Architecture Quality Gates | arquitectura | mínima complejidad y auditabilidad | ADOPT | no subsistema nuevo |
| SECURITY.md | protected subordinate | model output untrusted | ADOPT | doble enforcement schema + parser |
| Engineering Method | proceso | cambio proporcional | ADOPT | no semantic judge |
| Construction Protocol | proceso | critical-contract sequence | ADOPT | RED separado |
| Eighth U01 Semantic Audit | evidencia derivada | SG-BINDING / SG-ASSURANCE | ADAPT | trigger causal |
| E3 Semantic Grounding Hardening design | histórico de diseño | structured binding candidate | ADAPT | retoma opción D |
| Relation Catalog / Consumption / Coverage | baseline | relación gobernada estable | ADOPT | precondición ya integrada |
| Evidence-Bound Cognition Foundation | concepto no normativo | CAL-003 / CAL-006 | ADAPT | guía, no autoridad |
| Research Horizon Map | concepto no normativo | evidence != authority | OBSERVE | no Stage 2 |
| Other concepts | concepto no normativo | horizontes futuros | OBSERVE | no promoción lateral |
| ideas.md | no normativa | research/assurance horizon | OBSERVE | no registry/reviewer genérico |
| Structural Evidence E2 | baseline | no propagación E3/E4 | OBSERVE | permanece diferido |

---

## 19. Security Horizon Check

| Superficie | Resultado | Razón |
| --- | --- | --- |
| Model output trust | REINFORCE_EXISTING | claims siguen siendo input no confiable |
| Prompt/context trust | ALREADY_COVERED | evidence JSON continúa como data |
| Authority expansion | NO NEW EXPOSURE | authority_effect none |
| Persistent state | NOT_APPLICABLE | sin writes/persistence |
| External execution | NOT_APPLICABLE | una inferencia existente; sin side effects nuevos |
| AI supply chain | NOT_APPLICABLE | no cambia model/provider |
| Agent delegation | NOT_APPLICABLE | no agents |
| Data disclosure | NO NEW EXPOSURE | mismo packet existente |
| Resource governance | ALREADY_COVERED | mismos hard limits; schema bounded |
| Evidence/assurance | REINFORCE_EXISTING | rol explícito y no-overclaim |
| Human in Control | PRESERVED | revisión/Ready/Merge humanos |

Resultado:

~~~text
Security Horizon Check = PASS
~~~

---

## 20. Cuatro preguntas de ley

### Blueprint

~~~text
PASS
~~~

Capability First preservado. Kernel delta cero.

### Cognitive Constitution

~~~text
PASS
~~~

CC-003, CC-004, CC-005, CC-006, CC-007, CC-008, CC-011 y CC-012 favorecen
binding explícito, incertidumbre visible y assurance proporcional sin crear una
verificación probabilística innecesaria.

### Governance Constitution

~~~text
PASS
~~~

El output sigue siendo informativo y no concede autoridad.

### Kernel complexity

~~~text
PASS
~~~

Kernel, Planner y CapabilityRegistry permanecen fuera del candidate.

Resultado:

~~~text
Four Questions of Law = PASS
~~~

---

## 21. Design 4R

### Risk — PASS

Riesgos:

- confundir role binding con semantic support;
- romper generic E3;
- hacer E4 relation-aware accidentalmente;
- overfit del schema a U01;
- introducir autoridad implícita.

Mitigaciones:

- scope sólo relation-aware;
- `semantic_assurance: NOT_VERIFIED`;
- legacy path unchanged;
- E4 negative guard;
- no second model;
- authority_effect none.

### Readability — PASS

Los roles separan explícitamente:

~~~text
implementation support
knowledge support
limitation/counterevidence
uncertainty basis
~~~

sin crear un score opaco.

### Reliability — PASS

Mismos packet refs + misma clasificación + mismo output estructurado producen
las mismas reglas de aceptación.

Schema y parser deben validar los mismos invariantes.

### Resilience — PASS

Unknown refs, role mismatch, overlap, invalid uncertainty basis y precedence sin
fuente normativa aplicable fallan cerrado.

Resultado:

~~~text
Design 4R = PASS
~~~

---

## 22. RDD Stage 1 Design Check

~~~text
candidate identity strategy        PASS
baseline exact                     PASS
baseline/evidence binding          PASS
scope/spec binding                 PASS
Writer/Reviewer/Validator split    PASS
PASS|FAIL|INCONCLUSIVE discipline  PASS
candidate change invalidation      PASS
bounded correction defined         PASS
authority_effect                   none
RDD Stage 2 effects                NONE
overall                            PASS
~~~

Esto no constituye Candidate Conformance.

---

## 23. Cobertura exhaustiva del baseline

Inventario recursivo:

~~~text
tracked files discovered = 332
tracked files classified = 332
silently omitted files   = 0
~~~

Disposiciones:

~~~text
FULL_READ                    28
TARGETED_READ                11
STRUCTURAL_INSPECTION       152
HISTORICAL_REFERENCE         96
NOT_APPLICABLE_WITH_REASON   45
REJECTED_DO_NOT_READ          0
~~~

Ledger:

~~~text
docs/project/sprints/proposals/MALAK-E3-STRUCTURED-EVIDENCE-ROLE-BINDING-V0-FILE-COVERAGE.tsv
~~~

Todos los archivos bajo:

~~~text
docs/project/concepts/**
~~~

fueron descubiertos y revisados de forma recursiva según su rol no normativo.

La fuente rechazada por AGENTS.md:

~~~text
PROJECT - MANIFIESTO MALAK (1).docx
~~~

no está trackeada en este baseline. No fue abierta, indexada ni utilizada.

---

## 24. Ambigüedades materiales

Se evaluaron explícitamente:

~~~text
optional uncertainty field semantics
role-prefix mismatch
duplicate/overlap semantics
legacy flat evidence_refs compatibility
E4 relation-aware leakage
semantic assurance naming
second-model pressure
relation-specific evidence scoping
Structural Evidence propagation
~~~

Disposición:

~~~text
uncertainty field -> always present with NONE sentinel
role mismatch -> fail closed
overlap -> fail closed
legacy generic E3 -> preserved
E4 -> preserved relation-less
semantic assurance -> NOT_VERIFIED metadata only
second model -> not admitted
relation-specific evidence scope -> separate future gate if needed
Structural Evidence -> deferred
~~~

Known material ambiguity unresolved:

~~~text
0
~~~

---

## 25. Estado terminal de admisión

~~~text
baseline post-merge Validation #670      PASS
G0                                      PASS
G1                                      PASS
Critical Contract Hardening             PASS
Four Questions of Law                   PASS
Design 4R                               PASS
Security Horizon Check                  PASS
RDD Stage 1 Design Check                PASS

RED                                     NOT AUTHORIZED
GREEN                                   NOT AUTHORIZED
Candidate FULL 4R                       NOT APPLICABLE YET
Runtime Self-Review                     NOT AUTHORIZED
RDD Stage 2                             NOT AUTHORIZED
Ready / Merge                           OWNER ONLY
authority_effect                        none
~~~

Siguiente transición lícita:

~~~text
Owner review of this admission/design
-> explicit RED authorization
-> materialize causal RED R01-R11 only
~~~

No se autoriza ninguna transición por la sola existencia de este documento.
