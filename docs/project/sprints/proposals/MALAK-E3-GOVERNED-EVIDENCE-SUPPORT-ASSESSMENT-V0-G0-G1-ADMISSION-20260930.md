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

La unidad deberá resolver en diseño cómo ligar el assessment al material exacto evaluado.
No puede reclamar content integrity, cryptographic identity ni durable provenance que el
baseline no demuestre.

## 6. Outcome semántico candidato — no congelado

La admisión necesita distinguir al menos:

```text
positive material support
insufficient / absent material support
material uncertainty
```

Nombres candidatos:

```text
SUPPORTED
INSUFFICIENT
INCONCLUSIVE
```

No quedan congelados por G0/G1. En particular:

```text
SUPPORTED != TRUE
SUPPORTED != VERIFIED_FACT
SUPPORTED != authority
```

Si la evidencia favorece parcialmente un claim pero deja una parte material sin soporte,
V0 debe decidir antes de RED si necesita un estado explícito adicional o si corresponde
`INCONCLUSIVE`. No se permite esconder esa ambigüedad.

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

**OPEN / BLOCKS RED**

Debe definirse qué parte del claim debe quedar soportada y cómo tratar claims compuestos.

### Ambigüedad material B — partial support

**OPEN / BLOCKS RED**

Debe decidirse si V0 representa `PARTIALLY_SUPPORTED` o degrada a `INCONCLUSIVE`.

### Ambigüedad material C — source authority vs semantic support

**CLOSED conceptualmente**

Una fuente puede soportar semánticamente una afirmación sin tener autoridad normativa sobre
Malāk. El assessment debe mantener dimensiones separadas.

### Ambigüedad material D — counterevidence

**OPEN / BLOCKS RED**

La presencia de counterevidence no puede ignorarse ni resolverse por orden de entrada.
Debe existir semántica determinista de conflicto/abstención alrededor del assessment.

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

### Reliability — INCONCLUSIVE para RED

No existe aún contrato cerrado de partial support, claims compuestos, counterevidence ni
evaluation corpus. Debe resolverse en la spec pre-RED.

### Resilience — INCONCLUSIVE para RED

Fail-closed está definido conceptualmente, pero faltan failure semantics completas para
evaluator unavailable, malformed assessment y material drift.

```text
Design 4R overall for implementation/RED: INCONCLUSIVE
Design exploration may continue.
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

- candidate identity strategy: PARTIAL — debe congelarse material binding;
- baseline/candidate binding: PASS para este artefacto;
- evidence provenance: PARTIAL — exact material binding pendiente;
- Writer / Reviewer / Validator / Authority separation: PARTIAL;
- PASS/FAIL/INCONCLUSIVE semantics: PARTIAL;
- INCONCLUSIVE != PASS: PASS;
- candidate change invalidates affected evidence: REQUIRED, mecanismo pendiente;
- bounded correction: REQUIRED para implementación futura;
- independent fix validation: REQUIRED cuando aplique;
- authority_effect none: PASS;
- RDD Stage 2 NOT AUTHORIZED: PASS.

Resultado:

```text
RDD Stage 1 Design Check = INCONCLUSIVE
RED NOT ADMISSIBLE
```

No es un failure del G0/G1; identifica exactamente lo que la futura spec debe cerrar antes
de RED.

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
Critical Contract Hardening: INCONCLUSIVE for RED
Design 4R: INCONCLUSIVE for RED
RDD Stage 1 Design Check: INCONCLUSIVE
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

Ese gate deberá cerrar, como mínimo:

1. semántica exacta de claim scope y claims compuestos;
2. partial support;
3. counterevidence/conflict;
4. exact-material binding e invalidación;
5. assessor/producer independence;
6. failure semantics;
7. fixture/corpus y métricas;
8. mapping explícitamente fuera o dentro de scope hacia `support_sufficient`.

Hasta entonces:

```text
RED NOT ADMISSIBLE
IMPLEMENTATION NOT AUTHORIZED
```
