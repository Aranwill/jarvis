---
title: Malāk E3 Governed Evidence Support Assessment V0 — G0/G1 Admission
status: admission_candidate
authority: design_evidence_only
language: es
as_of_date: 2026-09-30
source_baseline: 65a5d9cc43869ea361b39651579f503b7d3c12d4
risk_class: 3_HIGH
critical_contract: true
implementation_authorized: false
red_authorized: false
rdd_stage_2_authorized: false
authority_effect: none
trigger_finding: E008-SG-02
---

# Malāk E3 Governed Evidence Support Assessment V0 — G0/G1 Admission

## 1. Estado y límite de autoridad

Este artefacto registra únicamente la admisión G0/G1 del siguiente problema acotado:

```text
¿cómo evaluar de forma gobernada y auditable si la evidencia explícitamente ligada
a un finding E3 aporta soporte material a su claim?
```

No autoriza implementación, RED, runtime wiring, cambios normativos ni promoción de
`semantic_assurance`.

```text
admission_candidate
!= implementation authorization
!= RED authorization
!= semantic truth
!= support_sufficient authorization
!= finalization decision
```

## 2. Baseline exacto y necesidad comprobada

Baseline revisado:

```text
Aranwill/jarvis
main@65a5d9cc43869ea361b39651579f503b7d3c12d4
```

Estado relevante:

- PR #212 estableció identidad de relación gobernada;
- PR #215 integró consumo de relación gobernada;
- PR #218 integró coverage + uniqueness;
- PR #222 integró structured evidence role binding;
- PR #223 reconcilió CURRENT_STATE;
- `semantic_assurance: NOT_VERIFIED`;
- `E008-SG-02` permanece OPEN;
- `E008-SG-03` conserva el assurance boundary.

La cadena E3 ya puede demostrar estructuralmente qué refs se presentan como soporte,
counterevidence o fundamento de incertidumbre. No puede demostrar todavía que esos refs
aporten soporte material al claim.

Al mismo tiempo, Cognitive Assurance ya contiene la señal:

```text
support_sufficient
```

y Assurance Signal Boundary valida identidad/autorización/binding del producer, pero su
contrato prohíbe decidir verdad, materialidad o suficiencia.

Por tanto existe un gap real entre:

```text
structured evidence role binding
        ↓
[missing governed support assessment]
        ↓
support_sufficient observation
```

Este gate no presupone que V0 deba cerrar toda la cadena.

## 3. Pregunta de admisión

```text
¿Cuál es el contrato mínimo, auditable y sin autoridad que permite evaluar si la
evidencia explícitamente ligada a un finding E3 aporta soporte material a ese claim,
preservando INCONCLUSIVE cuando Malāk no puede justificar soporte suficiente?
```

## 4. Invariantes obligatorios

```text
evidence ref exists != evidence supports claim
structural grounding != semantic support
semantic support != semantic truth
support assessment != support_sufficient authorization
producer permission != signal truth
support_sufficient != finalization decision
finalization decision != authority
Evidence != Authority
Analysis != Decision
Finding != Authorization
INCONCLUSIVE != PASS
missing evaluator != sufficient support
absence of counterevidence != positive support
same producer self-certification != independent assurance
```

Ningún resultado de este assessment puede modificar código, habilitar tools, aprobar
candidates, otorgar permisos, persistir estado o sustituir revisión humana.

## 5. Sujeto exacto candidato

El assessment debe operar sobre material explícito y acotado, no sobre búsquedas implícitas:

```text
claim / finding statement
governed relation_id
supporting_repository_refs
supporting_knowledge_refs
limiting_or_counterevidence_refs
uncertainty_basis
exact evidence packet material reachable by those refs
```

Un ID, path o label por sí solo no constituye soporte semántico.

V0 congela el sujeto de assessment mediante el binding que E3 ya demuestra:

```text
baseline_commit
+ focus_id
+ evidence_set_digest
+ relation_id
+ finding classification
+ exact statement
+ exact rationale
+ ordered/canonical evidence-role ref sets
+ exact packet material resolved by those refs
```

`evidence_set_digest` identifica el Evidence Focus capturado; no se reutiliza la identidad
episódica de otro dominio y no se reclama identidad criptográfica adicional. El assessment
solo es válido para esa combinación exacta.

```text
change in baseline_commit
OR focus_id
OR evidence_set_digest
OR finding material
OR role refs
OR resolved evidence material
-> prior assessment INVALIDATED
-> reevaluation required
```

Un label/ref lógico sin el material del packet correspondiente no satisface el binding.
V0 no reclama durable provenance, remote authenticity ni identidad fuera del snapshot E3.

## 6. Outcome semántico V0

V0 congela tres disposiciones de assessment:

```text
SUPPORTED
INSUFFICIENT
INCONCLUSIVE
```

Semántica:

```text
SUPPORTED
-> el claim material exacto queda directamente respaldado por el conjunto explícito
   de supporting refs dentro del scope gobernado
-> no existe counterevidence material no reconciliada dentro del packet

INSUFFICIENT
-> los supporting refs explícitos no aportan soporte material suficiente al claim
   exacto, o el soporte requerido está ausente

INCONCLUSIVE
-> existe ambigüedad material, claim compuesto no evaluable como una única proposición,
   counterevidence material no reconciliable, evidencia incompleta, assessor no disponible,
   o el assessment no puede justificar SUPPORTED/INSUFFICIENT sin ampliar scope
```

```text
SUPPORTED != TRUE
SUPPORTED != VERIFIED_FACT
SUPPORTED != architectural correctness
SUPPORTED != authority
INSUFFICIENT != claim proven false
INCONCLUSIVE != INSUFFICIENT
```

V0 **no introduce `PARTIALLY_SUPPORTED`**. `PARTIAL` ya es una clasificación E3 de la
relación observada y no debe reutilizarse como medida de cobertura semántica del statement.

Regla de claim scope:

```text
assessment subject = exact finding.statement as one material proposition
```

Si el statement contiene varias proposiciones materiales independientes y el soporte no
cubre todas:

```text
compound material claim -> INCONCLUSIVE
```

La corrección futura debe dividir el finding upstream o producir un claim atómico en una
nueva ejecución autorizada; el assessor V0 no reescribe ni fragmenta findings.

## 7. Qué puede ser determinista

El baseline permite controles deterministas sobre:

- existencia de refs en el evidence packet exacto;
- pertenencia de cada ref al rol declarado;
- relation_id gobernada;
- cardinalidad, duplicados e incompatibilidades estructurales;
- presencia explícita de counterevidence y uncertainty basis;
- binding estructural ya exigido por E3;
- schema/version/policy cerrados que una futura spec autorice.

Estos controles son precondiciones de assessment. No prueban por sí mismos soporte
semántico.

## 8. Qué no puede declararse determinísticamente en general

G0/G1 rechaza como garantía general:

```text
lexical overlap -> support
keyword match -> entailment
citation existence -> support
model confidence -> truth
source popularity -> truth
absence of contradiction -> support
deterministic general semantic entailment
```

Una regla local puede evaluar relaciones semánticas específicas únicamente si una futura
spec demuestra que la relación y su semántica están suficientemente cerradas. No se
generaliza esa propiedad a claims arbitrarios.

## 9. Separación producer / assessor / signal / authority

La arquitectura debe preservar:

```text
E3 finding producer
!= support assessor role
!= Assurance Signal producer authorization
!= Protected Finalization evaluator
!= human authority
```

La misma implementación física o modelo no puede considerarse independencia suficiente
solo por ejecutar un segundo prompt o una segunda llamada.

Si una futura implementación usa un modelo como assessor:

```text
model output = untrusted assessment evidence
model output != authority
model confidence != support_sufficient
```

La suficiencia de independencia, si es requerida, debe demostrarse por contrato y
provenance, no inferirse.

## 10. Alternativas G0/G1

### A — Prompt-only / same-producer self-certification

**REJECT**

No crea una assurance boundary real y permite que el producer interesado declare
suficiente su propio soporte.

### B — General deterministic semantic entailment

**REJECT**

No existe evidencia en el baseline de un algoritmo local general capaz de demostrar
entailment semántico para claims arbitrarios sin introducir falsas garantías.

### C — Mandatory second model / NLI / embeddings / RAG / GraphRAG

**OBSERVE**

Pueden ser técnicas futuras de evaluación o recuperación, pero el baseline no demuestra
que sean necesarias para V0 ni que su salida deba convertirse en autoridad. Introducirlas
ahora ampliaría dependencias, superficie de confianza y evaluación.

### D — Governed bounded support-assessment contract sobre evidencia explícita

**ADAPT — candidate direction**

Conservar la infraestructura existente de E3 y Cognitive Assurance y diseñar únicamente
la frontera faltante de assessment. V0 debe comenzar por un contrato acotado, fail-closed,
auditable y sin side effects.

### E — Human-only semantic review como única implementación

**OBSERVE / fallback válido**

La revisión humana sigue siendo autoridad final y puede ser necesaria cuando la máquina no
pueda justificar soporte. No resuelve por sí sola la necesidad de representar de forma
estructurada el resultado machine-assisted futuro.

## 11. Malāk Alignment Matrix

| Fuente | Clase | Invariante/intención aplicable | Evidencia baseline | Disposición | Efecto candidato |
|---|---|---|---|---|---|
| Cognitive Constitution | normativa | evidence-bound cognition; incertidumbre explícita; no authority implícita | E3 expone evidence roles y NOT_VERIFIED | ADOPT | preservar fail-closed y separación evidencia/autoridad |
| Governance Constitution | normativa | Human in Control; autorización separada | authority_effect none | ADOPT | assessment no autoriza acciones |
| Blueprint | arquitectura | Kernel First / Capability First / Runtime Independence | E3 vive fuera del Kernel | ADOPT | Kernel delta 0 |
| SECURITY.md | seguridad | Zero Trust, provenance, no trust implícito | refs/producer/model no se presumen confiables | ADOPT | inputs/resultados tratados como no autoridad |
| Architecture Quality Gates | arquitectura | cambio mínimo, boundaries explícitos | gap localizado entre E3 y assurance signal | ADOPT | no nueva layer/manager/service |
| ADR-005 | decisión aceptada | evidence-bound final response; assurance progresiva | support_sufficient ya forma parte del contrato downstream | ADAPT | reutilizar vocabulario sin wiring en V0 |
| ADR-006 | decisión aceptada | missing evaluator != PASS; no self-attestation de suficiencia | gap de evaluator sigue abierto | ADOPT | INCONCLUSIVE/fail-closed |
| implementation roadmap | derivada/plan | E008-SG-02 OPEN; semantic assurance NOT_VERIFIED | PR #222/#223 | ADOPT | atacar el gap sin declarar entailment |
| ideas.md | incubación | evidencia/inspección trazable | intención compatible | OBSERVE | no crea scope adicional |
| Research Horizon Map | investigación | evaluación/assurance progresiva; evitar authority inflation | no prerequisite nuevo demostrado | ADAPT | guía de investigación, no autoridad |
| Evidence-Bound Cognition Foundation | concepto | claims ligados a evidencia y counterevidence | E3 ya materializa roles | ADAPT | conservar intención sin crear subsistema |
| E3 code/tests | baseline ejecutable | relation + explicit evidence roles + NOT_VERIFIED | PR #222 | ADOPT | sujeto primario del assessment |
| Assurance Signal Boundary | baseline ejecutable | projection valida producer/binding, no suficiencia | support_sufficient existe sin resolver semántica | ADOPT | futuro consumidor; wiring fuera de V0 |

```text
ADOPT/ADAPT != implementation authorization
OBSERVE != prerequisite
concept != baseline
roadmap != authorization
```

## 12. Security Horizon Check

| Área | Resultado | Razón |
|---|---|---|
| Prompt & Context Trust Boundary | REQUIRES_REINFORCEMENT | un assessor model-based recibiría material no confiable |
| identidad/delegación | ALREADY_COVERED downstream / NOT YET BOUND here | Signal Boundary autoriza producers; assessment todavía no tiene producer contract |
| compromise containment / trust revocation | NOT_APPLICABLE para G0/G1 documental | no runtime/side effects |
| Memory / Knowledge poisoning | REQUIRES_REINFORCEMENT si knowledge refs entran al evaluator | source role no equivale a trust |
| AI supply-chain trust | DEFERRED | solo aplica si se selecciona modelo/provider |
| data classification / disclosure | DEFERRED | solo aplica al ejecutar evaluación con datos externos |
| Resource Governance | DEFERRED | no ejecución en G0/G1 |
| observabilidad/evidencia/recovery | REQUIRES_REINFORCEMENT | futuro assessment debe ser reconstructible |
| Human in Control | ALREADY_COVERED | authority_effect none; revisión humana preservada |

No existe BLOCKING_GAP para continuar diseño. Sí existen condiciones que impedirían RED si
la futura spec selecciona un evaluator externo/model-based sin cerrar trust/provenance.

## 13. Critical Contract Hardening — hallazgos G0/G1

### Ambigüedad material A — “support” sin scope

**CLOSED FOR V0**

El sujeto es el `finding.statement` exacto. `SUPPORTED` exige soporte material del claim
completo dentro de la relación gobernada. Un statement con proposiciones materiales
independientes cuyo soporte no sea completo produce `INCONCLUSIVE`; V0 no lo reescribe.

### Ambigüedad material B — partial support

**CLOSED FOR V0**

No existe `PARTIALLY_SUPPORTED` en V0. Soporte parcial de un claim compuesto no puede
elevarse a `SUPPORTED` ni degradarse automáticamente a `INSUFFICIENT`; produce
`INCONCLUSIVE`. La clasificación E3 `PARTIAL` permanece ortogonal.

### Ambigüedad material C — source authority vs semantic support

**CLOSED conceptualmente**

Una fuente puede soportar semánticamente una afirmación sin tener autoridad normativa sobre
Malāk. El assessment debe mantener dimensiones separadas.

### Ambigüedad material D — counterevidence

**CLOSED FOR V0**

Todo `limiting_or_counterevidence_ref` debe formar parte del assessment material. La
evaluación es invariante al orden de refs.

```text
material counterevidence absent
-> SUPPORTED remains possible

material counterevidence present and demonstrably compatible/limiting without
negating the exact claim
-> SUPPORTED remains possible only if the limitation is represented by the exact
   claim/rationale and no material proposition overreaches it

material counterevidence conflicts with the exact claim and cannot be reconciled
inside the bounded packet
-> INCONCLUSIVE

supporting refs irrelevant/insufficient regardless of counterevidence
-> INSUFFICIENT
```

El assessor no elimina, rankea por autoridad ni selecciona silenciosamente evidencia
conflictiva. Precedencia documental se aplica cuando la relación evaluada depende de
autoridad normativa; no convierte por sí sola una fuente en soporte semántico.

### Ambigüedad material E — self-assessment

**CLOSED**

Same-producer self-certification no cuenta como assurance independiente.

### Ambigüedad material F — missing capability

**CLOSED**

```text
missing evaluation capability -> INCONCLUSIVE / no positive support claim
```

### Ambigüedad material G — mapping a support_sufficient

**OPEN / OUT OF V0 IMPLEMENTATION UNTIL SEPARATE FREEZE**

El assessment no debe escribir directamente `support_sufficient=True` por inferencia.
Un adapter/policy futuro deberá definir el mapping y producer authorization aplicable.

Resultado del hardening:

```text
known material ambiguities remain
-> RED NOT ADMISSIBLE
```

## 14. Métricas candidatas

Las métricas deben evaluar el assessment, no fabricar un truth score:

```text
claim_support_coverage
unsupported_claim_escape_rate
false_support_acceptance_rate
false_inconclusive_rate
contradiction_handling_recall
assessment_stability_on_equivalent_inputs
```

Antes de GREEN deberá existir corpus/fixture etiquetado independientemente suficiente para
medir, como mínimo, escapes de claims sin soporte y falsas aceptaciones.

No se autoriza un porcentaje de “verdad”.

## 15. Casos adversariales mínimos para futura spec

1. ref real pero material irrelevante al claim;
2. evidencia que soporta solo una cláusula de un claim compuesto;
3. support refs correctos + counterevidence material;
4. dos refs duplicados con roles incompatibles;
5. source con autoridad baja pero contenido semánticamente pertinente;
6. source normativa con alta autoridad pero irrelevante al claim concreto;
7. rationale que afirma más de lo que permiten los refs;
8. uncertainty_basis ausente cuando existe incertidumbre material;
9. assessor que recibe evidencia incompleta;
10. mismo producer intentando autocertificar soporte;
11. inputs equivalentes permutados;
12. evidence material cambiado manteniendo el mismo label/ref lógico;
13. evaluator/model unavailable;
14. output de modelo con alta confianza pero soporte insuficiente;
15. contradicción no resoluble dentro del scope V0.

## 16. Design 4R — G0/G1

### Risk — PASS para continuar diseño

Riesgo alto por interpretar evidence/assurance, mitigado en G0/G1 por runtime delta 0,
authority_effect none y RED bloqueado hasta cerrar ambigüedades.

### Readability — PASS

El boundary propuesto mantiene conceptos distintos: finding, evidence role, assessment,
signal authorization y finalization.

### Reliability — PASS para pre-RED specification

Claim scope, claims compuestos, partial support, counterevidence e invalidación por drift
quedan cerrados para V0. El corpus/fixture y los thresholds de aceptación permanecen como
obligación de la spec pre-RED, no como ambigüedad semántica del contrato.

### Resilience — PASS para pre-RED specification

Failure semantics mínimas quedan congeladas:

```text
evaluator unavailable -> INCONCLUSIVE
malformed assessment -> INCONCLUSIVE / no positive support
material binding mismatch -> assessment invalid / reevaluation required
unresolved material counterevidence -> INCONCLUSIVE
missing exact packet material -> INCONCLUSIVE
```

Ninguna falla puede producir `SUPPORTED` por default.

```text
Design 4R overall for G0/G1 -> PASS
PASS authorizes only progression to Pre-RED Contract Specification.
RED remains NOT AUTHORIZED.
```

## 17. Cuatro preguntas de ley

```text
1. ¿Respeta Blueprint?                  PASS
2. ¿Respeta Cognitive Constitution?    PASS
3. ¿Respeta Governance Constitution?   PASS
4. ¿Mantiene/reduce complejidad Kernel? PASS — Kernel delta 0
```

Estas respuestas admiten continuar diseño; no sustituyen Design 4R ni autorizan RED.

## 18. RDD Stage 1 Design Check — estado G0/G1

- candidate identity strategy: PASS — baseline + focus + evidence digest + exact finding material;
- baseline/candidate binding: PASS para este artefacto;
- evidence provenance: PASS dentro del bounded E3 snapshot; no durable/remote claim;
- Writer / Reviewer / Validator / Authority separation: PASS como diseño; roles no colapsables;
- PASS/FAIL/INCONCLUSIVE semantics: PASS para el gate; assessment usa SUPPORTED/INSUFFICIENT/INCONCLUSIVE sin equivaler a gate PASS;
- INCONCLUSIVE != PASS: PASS;
- candidate/material change invalidates affected evidence: PASS por regla de invalidación;
- bounded correction: PASS como requisito obligatorio de implementación futura;
- independent fix validation: PASS como requisito cuando aplique;
- authority_effect none: PASS;
- RDD Stage 2 NOT AUTHORIZED: PASS.

Resultado:

```text
RDD Stage 1 Design Check = PASS
```

Este PASS admite únicamente avanzar a una **Pre-RED Contract Specification**. No autoriza
RED, tests productivos ni implementación.

## 19. Scope freeze G0/G1

### Permitido en esta unidad

```text
design/admission documentation
baseline analysis
contract alternatives
threat/adversarial analysis
metrics design
fixture/corpus design
producer/assessor separation design
exact-material binding design
```

### Prohibido

```text
src/** changes
tests/** changes
Kernel changes
Planner changes
Registry changes
runtime wiring
Assurance Signal Boundary changes
Protected Finalization changes
support_sufficient producer implementation
model/provider selection
Ollama execution
/self-review
NLI / embeddings / RAG / GraphRAG implementation
agents / swarm
Memory / Knowledge persistence
Cognitive Receipt
RDD Stage 2
authority expansion
normative Constitution/Blueprint/Governance changes
```

## 20. File Coverage Ledger — cobertura de admisión

La revisión integral que originó este gate partió del inventario recursivo del baseline:

```text
tracked files discovered = 335
tracked files classified = 335
silently omitted files   = 0
```

La clasificación se realizó proporcionalmente por rol y path, no como permiso de edición:

| Clase de paths | review_relevance | review_depth | disposition | change_scope |
|---|---|---|---|---|
| constituciones, Blueprint, SECURITY, quality gates | autoridad/alineación | FULL_READ/TARGETED_READ según fuente | FULL_READ/TARGETED_READ | forbidden |
| Construction Protocol, engineering method/checklist | proceso obligatorio | FULL_READ/TARGETED_READ | FULL_READ/TARGETED_READ | forbidden |
| roadmap, project context, CHANGELOG | baseline/estado | TARGETED_READ | TARGETED_READ | forbidden |
| Research Horizon Map, concepts README y concepts relevantes | incubación/intención | TARGETED_READ + structural inventory | TARGETED_READ/STRUCTURAL_INSPECTION | forbidden |
| proposals activas relacionadas E3/Cognitive Assurance | restricciones/candidates/findings | FULL_READ/TARGETED_READ | FULL_READ/TARGETED_READ | forbidden |
| `src/malak/capabilities/**` relevante a E3 | baseline ejecutable | TARGETED_READ + structural inventory | TARGETED_READ/STRUCTURAL_INSPECTION | forbidden en G0/G1 |
| `src/malak/core/**` assurance/finalization relevante | downstream boundary | TARGETED_READ + structural inventory | TARGETED_READ/STRUCTURAL_INSPECTION | forbidden |
| tests E3/assurance relevantes | garantías actuales | TARGETED_READ + structural inventory | TARGETED_READ/STRUCTURAL_INSPECTION | forbidden |
| resto de código/tests/config/workflows | detección de dependencia lateral | STRUCTURAL_INSPECTION | STRUCTURAL_INSPECTION/NOT_APPLICABLE_WITH_REASON | forbidden |
| historical/derived evidence | trazabilidad cuando aplicable | STRUCTURAL_INSPECTION/HISTORICAL_REFERENCE | HISTORICAL_REFERENCE/GENERATED_OR_DERIVED | forbidden |
| manifiesto expresamente rechazado | prohibido por regla vigente | no leído | REJECTED_DO_NOT_READ | forbidden |

El inventario completo no implica `FULL_READ` de 335 archivos. La profundidad fue
proporcional y ningún archivo fue convertido en scope de cambio por su relevancia de review.

## 21. Gate result

```text
G0 problem admission: PASS
G1 direction admission: PASS
Critical Contract Hardening: PASS for G0/G1
Design 4R: PASS for G0/G1
RDD Stage 1 Design Check: PASS for G0/G1
implementation_authorized: false
red_authorized: false
authority_effect: none
```

### Próximo gate permitido

Únicamente después de revisión humana de este artefacto:

```text
E3 Governed Evidence Support Assessment V0
Pre-RED Contract Specification / Hardening
```

Ese gate deberá especificar y endurecer, sin reabrir silenciosamente lo ya cerrado:

1. representación/schema exacta del assessment;
2. assessor/producer independence y provenance operativa;
3. reason codes y precedencia determinista;
4. fixture/corpus adversarial y métricas de aceptación;
5. límites de input/output y resource bounds;
6. validation/evidence manifest y candidate binding;
7. mapping hacia `support_sufficient` explícitamente fuera de scope salvo nueva autorización;
8. allowed files/components exactos para un eventual RED.

Hasta entonces:

```text
RED NOT ADMISSIBLE
IMPLEMENTATION NOT AUTHORIZED
```
