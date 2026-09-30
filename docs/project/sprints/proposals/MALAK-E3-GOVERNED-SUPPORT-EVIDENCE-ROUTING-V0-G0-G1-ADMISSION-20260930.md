---
title: Malāk E3 Governed Support Evidence Routing V0 — G0/G1 Admission
status: g0_g1_candidate
authority: non_normative
language: es
baseline_commit: 774841d9fe045f048c4d2bcc2275e195fbb7c212
trigger_finding: E008-SG-02
risk_class: HIGH
critical_contract: true
authority_effect: none
implementation_authorized: false
red_authorized: false
green_authorized: false
model_provider_experiment_authorized: false
support_sufficient_wiring_authorized: false
rdd_stage_2_authorized: false
---

# E3 Governed Support Evidence Routing V0 — G0/G1 Admission

## 1. Propósito

Esta unidad determina si el siguiente paso de E3 debe introducir un nuevo
mecanismo cognitivo o si Malāk ya posee primitivas suficientes para resolver una
parte material del support assessment de forma determinista y escalar únicamente
el residuo inferencial.

La pregunta de admisión es:

> Dada una relación gobernada, un finding exacto y evidencia material ligada,
> ¿puede Malāk decidir de forma reproducible si esa pregunta puede resolverse
> mediante una prueba determinista existente, si requiere inferencia adicional o
> si la evidencia es insuficiente, sin ejecutar todavía ningún modelo/verifier y
> sin crear autoridad?

Esta unidad **no implementa** el router, un assessor, un modelo, un provider ni
wiring productivo.

## 2. Baseline exacto

```text
repository  Aranwill/jarvis
baseline    774841d9fe045f048c4d2bcc2275e195fbb7c212
tracked blobs discovered 349
recursive tree truncated false
```

El baseline ya contiene:

- E3 Structured Evidence Role Binding V0;
- E3 Governed Evidence Support Assessment V0;
- E3 Assessor Qualification Pack V0.1;
- reconciliación CURRENT_STATE post-PR #230/#232;
- `E008-SG-02 = OPEN`;
- `semantic_assurance = NOT_VERIFIED`;
- `support_sufficient = NOT WIRED / NOT AUTHORIZED`;
- `authority_effect = none`.

El archivo rechazado por `AGENTS.md` no apareció entre los 349 blobs trackeados
del baseline. Su regla `REJECTED_DO_NOT_READ` continúa vigente; no fue abierto ni
utilizado.

## 3. Finding de arquitectura que motiva esta admisión

### GSR-01 — La hipótesis "assessor = nuevo LLM" no está respaldada por el baseline

**Disposición:** REJECT como default arquitectónico.

Malāk ya posee controles deterministas y contratos que resuelven:

- identidad de baseline y evidence packet;
- relation identity;
- roles de evidence;
- source/authority class;
- material completeness;
- binding/fingerprint drift;
- output schema;
- self-certification;
- fail-closed behavior;
- qualification reproducible.

Introducir un modelo antes de agotar estas garantías violaría el principio
constitucional de proporcionalidad.

### GSR-02 — Falta routing explícito entre evidencia determinista e inferencia

**Disposición:** ADMIT para diseño.

No existe hoy una decisión gobernada que responda:

```text
esta relation/evaluation_question
+
este evidence packet exacto
        ↓
¿existe un oracle determinista gobernado que cubra completamente la pregunta?
```

Sin esa frontera, la ausencia de assessor tiende a verse como ausencia de
"inteligencia", cuando puede ser simplemente ausencia de routing/composición.

### GSR-03 — El Qualification Pack valida artifacts, pero no produce un experimento ciego

**Disposición:** ADMIT como frontera de experiment integrity.

`cases.json` contiene ground truth:

```text
expected_outcome
expected_reason_codes
critical_properties
case_class
```

Esto es correcto para el qualification runner, pero un futuro mecanismo evaluado
no debe recibir esos campos.

El pack actual no es defectuoso por ello: su contrato comienza en un
`assessor-result artifact` ya producido.

La pieza ausente es un futuro **trusted blind experiment projection/harness** que
produzca el input del mecanismo sin exponer ground truth.

### GSR-04 — Tests existentes contienen oráculos útiles, pero tests != runtime

**Disposición:** ADAPT.

Los tests actuales prueban propiedades deterministas reales, pero código
productivo no debe importar `tests/**`.

Una futura reutilización deberá:

- extraer una primitive compartida mínima cuando exista necesidad productiva; o
- mantener el oracle exclusivamente en `evaluations/**` / tooling cuando su
  propósito sea experimental.

No se autoriza mover lógica todavía.

## 4. Inventario de primitivas internas reutilizables

### 4.1 Governed Engineering Evidence Focus

`src/malak/capabilities/_engineering_evidence.py`

Ya materializa:

- baseline exacto;
- focus identity;
- evidence selectors;
- relation catalog;
- completeness;
- evidence-set digest;
- bounded collection.

**Uso potencial:** input identity y evidence scope del routing.

**No prueba:** entailment semántico.

### 4.2 Governed Engineering Relation

Las relaciones U01 existentes poseen identidad y `evaluation_question`
gobernadas.

**Uso potencial:** seleccionar un oracle por una relación exacta, no por keywords
ni por una inferencia libre.

```text
relation identity
!= semantic truth
```

### 4.3 Governed Knowledge Reader

`src/malak/knowledge/knowledge_reader.py`

Ya transporta `source_class` y `authority_class` y permite acotar conocimiento
aplicable.

**Uso potencial:** eliminar/limitar material documental fuera de alcance antes de
cualquier inferencia adicional.

**No prueba:** relevancia o soporte semántico suficiente.

### 4.4 Structured Evidence Role Binding + parser E3

Malāk ya distingue:

- repository support;
- knowledge support;
- limiting/counterevidence;
- uncertainty basis.

Esto reduce la superficie que un assessor debe resolver.

```text
structural role binding
!= semantic entailment
```

### 4.5 Governed Evidence Support Assessment V0

`assess_governed_evidence_support_v0()` ya implementa la envolvente gobernada.

Antes de invocar `assessor(material)` valida:

- policy version;
- expected binding;
- producer/assessor separation;
- presence de evidence material;
- exact evidence refs.

Después valida:

- output shape exacto;
- enum de outcome;
- reason-code coherence;
- fail-closed ante output inválido.

El input real entregado al assessor ya está reducido a:

```text
relation_id
classification
statement
rationale
supporting_repository_evidence
supporting_knowledge_evidence
limiting_or_counterevidence
uncertainty_basis
```

Este shape es una base natural para una futura **blind projection** porque no
contiene `expected_outcome` ni `expected_reason_codes`.

### 4.6 Assessor Qualification Pack V0.1

El pack ya admite:

```text
DETERMINISTIC
MODEL_BASED
HUMAN_REVIEWED
```

Por tanto, la arquitectura actual **no presupone un modelo**.

El pack ya valida:

- exact case/input coverage;
- C05 limiting material;
- C11/C12 prior binding;
- C13 stability sobre dos observations reales;
- malformed/unavailable outputs;
- self-certification;
- metric population integrity;
- `authority_effect = none`.

### 4.7 Architecture invariants y Kernel tests

Existen pruebas deterministas de propiedades que se solapan con relaciones U01.

No se reinterpretan automáticamente como proof de toda la pregunta semántica.

Su valor es demostrar que existen **oracles específicos** posibles.

## 5. Cobertura determinista preliminar por relación U01

Esta tabla es una clasificación G0/G1, no una certificación ni un contrato
congelado.

| relation_id | evidencia/oracle existente | cobertura preliminar | disposición |
|---|---|---|---|
| `U01.RUNTIME_INDEPENDENCE` | AST architecture invariants sobre imports/proveedores/runtime | fuerte para boundaries concretas | candidato determinista |
| `U01.CAPABILITY_ROUTING` | `Kernel.receive → Planner.resolve → Registry.get → Capability.execute` + tests Kernel | fuerte para el routing implementado | candidato determinista |
| `U01.KERNEL_INSTANCE_CARDINALITY` | Kernel spec + composition/tests | parcial; requiere demostrar criterio exacto | ADAPT / investigar |
| `U01.KERNEL_RESPONSIBILITY` | surface/import boundaries + Kernel contract | parcial; "no business logic" no está totalmente formalizado | inferential residual posible |
| `U01.MINIMAL_COMPLEXITY` | principios y shape actual | insuficiente para definir "small enough" sin umbral gobernado | no inventar oracle |

Regla:

```text
partial deterministic coverage
!= deterministic settlement
```

## 6. Investigación externa — Gentle AI / Gentle Shell

La investigación es **targeted comparative research**, no auditoría integral de
los repositorios externos.

Referencias pinneadas:

```text
Gentleman-Programming/gentle-ai
commit b388eb31e9d39f81bea8ab0e439a6c70848d84bc

Gentleman-Programming/gentle-shell
commit 3e2a02f3b9f36331445ad53fbb62412d2db3c23b
```

### 6.1 Gentle: policy nativa antes del reviewer

Fuente:

`gentle-ai/internal/reviewtransaction/risk.go`

Evidencia:

- `RiskAssessment` es determinista y repository-derived;
- código nativo selecciona 0/1/4 lenses;
- model/provider no es input del classifier.

**Disposición Malāk:** ADAPT.

Principio útil:

> la policy determina cuánta cognición hace falta; el modelo no decide su propio
> nivel de scrutiny.

### 6.2 Gentle: evidencia deterministic / inferential / insufficient

Fuente:

`gentle-ai/internal/reviewtransaction/transaction.go`

Gentle materializa explícitamente:

```text
deterministic
inferential
insufficient
```

y rutea:

- deterministic → no necesita refuter;
- inferential → un único refuter batch;
- insufficient → escalación/inconclusive.

**Disposición Malāk:** ADAPT.

No se copian enums ni state machine. Se adopta la separación conceptual porque
coincide con la Constitución Cognitiva y con Progressive Assurance ya existente.

### 6.3 Gentle: modelo sin autoridad

Fuentes:

- `gentle-ai/internal/reviewerprovider/contract.go`;
- `gentle-ai/internal/assets/skills/_shared/review-ledger-contract.md`;
- `gentle-ai/docs/architecture/organic-rdd.md`.

La implementación separa:

```text
provider result
!= native lifecycle authority
!= delivery authority
```

El contrato declara que código nativo aplica el resultado y que commit/push/PR/
release siguen bajo policy externa/humana.

**Disposición Malāk:** ADOPT como evidencia convergente de principios ya vigentes,
no como nueva autoridad.

### 6.4 Gentle Shell: transporta roles; no gobierna review

Fuente:

`gentle-shell/docs/review-integration.md`

Gentle Shell usa su model registry existente para transportar completions
acotadas. No reconstruye bindings, no clasifica resultados y no crea autoridad.

**Disposición Malāk:** OBSERVE para un futuro verifier model-based.

No se autoriza Model Registry, provider integration ni runtime change en esta
unidad.

## 7. Malāk Alignment Matrix

| source | authority class | invariant / intent | baseline evidence | disposition | implementation effect | deferred/rejected effect |
|---|---|---|---|---|---|---|
| Cognitive Constitution CC-003/005/006/011/012 | constitutional | evidence > speculation; deterministic sufficiency; generation != finalization | support assessment + qualification + explicit uncertainty | ADOPT | deterministic-first routing | reject model-first default |
| Governance GOV-001/004/005 | constitutional | human control, least privilege, separation | authority_effect none; Owner lifecycle | ADOPT | router cannot grant authority | no autonomous promotion |
| Blueprint | architecture | model/provider interchangeable; Kernel First; Capability First | Kernel/runtime separation already present | ADOPT | Kernel delta 0 | reject Kernel/model coupling |
| SECURITY.md | security policy | fail-closed, AI supply-chain only when applicable, Human in Control | no model/provider/network in this G0/G1 | ADOPT | no new sensitive surface | model security remains deferred |
| Progressive Assurance | derived design | deterministic checks first; escalation by material deficit | explicit design already present | ADOPT | routing must prefer sufficient deterministic oracle | no probabilistic verifier by default |
| E3 Support Assessment V0 | current contract | assessor is a bounded callable behind deterministic envelope | `assess_governed_evidence_support_v0` | ADOPT | compose before replacing | do not add parallel support subsystem |
| Qualification Pack V0.1 | current evaluation contract | assessor can be deterministic/model/human | V0.1 schemas + runner | ADOPT | first candidate may be deterministic | model not assumed |
| Gentle AI RDD @ b388eb3 | external evidence | native evidence classification and escalation-by-deficit | deterministic/inferential/insufficient routing | ADAPT | use as comparative evidence | reject copying lifecycle/state machine |
| Gentle Shell @ 3e2a02f | external evidence | model runtime as transport, not authority | in-process bounded completions | OBSERVE | future-only if inferential deficit survives | no provider work now |
| Governed Self-Review Bootstrap concept | non-normative | self-review must remain governed | first-task candidate but not automatic next execution | DEFERRED | none | not current unit |

## 8. Candidate routing model — conceptual only

La clasificación exacta **no se congela en G0/G1**.

Modelo conceptual:

```text
validate exact subject/evidence/binding
        ↓
invalid/incomplete?
        └─ yes → fail closed / INCONCLUSIVE

valid
        ↓
does an approved deterministic oracle fully cover relation + question?
        ├─ yes → deterministic route
        │          ↓
        │       bounded oracle result
        │
        └─ no
            ↓
is material evidence sufficient to justify further semantic evaluation?
        ├─ no → insufficient / INCONCLUSIVE
        └─ yes → inferential deficit
                    ↓
               no authorized verifier in V0
                    ↓
               INCONCLUSIVE
```

Reglas candidatas:

1. el router **no decide verdad**;
2. el router **no decide authority**;
3. un oracle sólo puede seleccionarse por relation identity + contract gobernado;
4. keyword matching no basta;
5. cobertura parcial nunca se eleva a cobertura total;
6. ausencia de oracle nunca significa `SUPPORTED`;
7. `INFERENTIAL` no implica automáticamente ejecutar un LLM;
8. si no existe verifier autorizado, la salida permanece `INCONCLUSIVE`;
9. un modelo futuro sería un actor reemplazable detrás de un contrato, no una
   dependencia arquitectónica de Engineering.

## 9. Blind Experiment Boundary — requisito antes de evaluar cualquier assessor

El qualification runner debe conservar acceso a ground truth.

El assessor candidate no.

Una futura proyección deberá separar:

```text
TRUSTED HARNESS
cases.json
   ├─ hidden ground truth
   │    case_class
   │    critical_properties
   │    expected_outcome
   │    expected_reason_codes
   │
   └─ candidate material
        relation_id
        classification
        statement
        rationale
        supporting_repository_evidence
        supporting_knowledge_evidence
        limiting_or_counterevidence
        uncertainty_basis
```

La proyección debe derivarse de la semántica ya utilizada por
`assess_governed_evidence_support_v0()`, no de un schema paralelo inventado.

El candidate assessor no debe recibir ground truth por:

- argumentos;
- environment;
- archivo lateral;
- prompt;
- metadata;
- access incidental al case-set completo.

Esta frontera deberá endurecerse antes de cualquier experimento real de
qualification.

## 10. Lo que este diseño NO autoriza

```text
new LLM                               NO
external LLM/API                      NO
Ollama assessor                       NO
NLI model                             NO
second model / judge                  NO
model voting                          NO
ensemble                              NO
AssessorManager                       NO
AssessorRegistry                      NO
SemanticEngine                        NO
new Capability                        NO
new Service                           NO
Kernel change                         NO
Planner change                        NO
runtime/provider integration           NO
support_sufficient wiring             NO
Protected Finalization wiring         NO
semantic_assurance promotion          NO
RDD Stage 2                           NO
Sprint 7.12                           NO
```

## 11. Posible ubicación futura — no congelada

La evidencia actual favorece reutilizar superficies existentes antes de crear
componentes.

Opciones que deberán decidirse en hardening, no aquí:

1. helper privado mínimo cerca de `_engineering_analysis.py`;
2. oracle exclusivamente evaluation-side para demostrar cobertura antes de
   promover lógica;
3. primitive compartida extraída sólo si runtime y tests necesitan la misma
   lógica.

Se rechaza por ahora crear un manager/registry/service genérico.

## 12. Critical Contract classification

La futura superficie es **critical-contract** porque:

- interpreta evidence;
- condiciona assurance;
- puede decidir si una pregunta se considera resoluble sin inferencia adicional;
- afecta el camino que eventualmente podría alimentar `support_sufficient`.

Por lo tanto, antes de RED deberá existir:

```text
Critical Contract Hardening
→ ambiguity/adversarial review
→ exact route semantics
→ exact oracle qualification rule
→ blind projection contract
→ fail-open/fail-closed behavior
→ candidate/evidence binding
→ skip/bypass analysis
→ correction budget
→ Design 4R
→ RDD Stage 1 Design Check
```

## 13. Security Horizon

### Prompt / Context Trust

**APPLICABLE TO FUTURE BLIND HARNESS**

Ground truth debe permanecer fuera del candidate input.

### AI supply-chain

**DEFERRED**

Sólo se activa si una futura unidad autoriza un modelo real.

### Data disclosure

**NOT ACTIVATED**

No existe ejecución remota ni provider en esta unidad.

### Network / tools

**NOT ACTIVATED**

No se autoriza red ni tools adicionales.

### Model Governance / Resource Governance

**DEFERRED**

No hay modelo.

### Human in Control

**PASS**

Toda promoción posterior requiere gates y decisión humana.

## 14. Cuatro preguntas de ley

### 14.1 ¿Respeta Blueprint?

**PASS**

- Kernel delta 0;
- runtime/model/provider agnostic;
- reutiliza contratos existentes;
- no crea subsystem paralelo.

### 14.2 ¿Respeta Cognitive Constitution?

**PASS**

Especialmente:

```text
CC-003 Evidence over speculation
CC-005 Proportionality
CC-006 Cognitive minimization
CC-011 Generation != Finalization
CC-012 evidence-bound finalization
```

### 14.3 ¿Respeta Governance?

**PASS**

`authority_effect = none`; ningún actor puede promoverse ni otorgar permiso.

### 14.4 ¿Hace al Kernel más simple o más complejo?

**PASS / NO DELTA**

El routing propuesto no pertenece al Kernel.

Cualquier futura necesidad de tocar Kernel:

```text
STOP
→ new admission
```

## 15. Design 4R preliminar de admisión

Esto no sustituye el Design 4R requerido después del Critical Contract
Hardening.

### Risk — PASS para continuar a hardening

Riesgo principal: convertir una prueba parcial en soporte semántico total.

Mitigación de diseño:

- exact relation identity;
- full-coverage oracle requirement;
- no heuristic fallback;
- default INCONCLUSIVE;
- no model/provider;
- no authority.

### Readability — PASS

La responsabilidad queda separada:

```text
evidence collection
!= routing
!= oracle/verifier
!= support assessment envelope
!= qualification
!= authority
```

### Reliability — PASS para continuar a hardening

El diseño reutiliza evidence/binding/qualification existentes en vez de crear
una segunda cadena.

### Resilience — PASS para continuar a hardening

Ausencia de oracle, verifier o evidencia suficiente debe cerrar en
`INCONCLUSIVE`, nunca en `SUPPORTED`.

## 16. File Coverage

Ledger:

`docs/project/sprints/proposals/MALAK-E3-GOVERNED-SUPPORT-EVIDENCE-ROUTING-V0-G0-G1-FILE-COVERAGE.tsv`

Resultado:

```text
tracked files discovered = 349
tracked files classified = 349
silently omitted files   = 0
recursive tree truncated = false
```

La profundidad fue proporcional:

- fuentes normativas/current-state/relevantes: FULL_READ o TARGETED_READ;
- código/tests relacionados: FULL_READ/STRUCTURAL_INSPECTION;
- proposals históricas no activas: HISTORICAL_REFERENCE;
- resto: clasificación estructural explícita.

## 17. Resultado G0/G1

```text
need demonstrated                         YES
existing internal primitives reusable     YES
model-first architecture justified         NO
Gentle RDD conceptual alignment            YES / ADAPT
blind experiment boundary required         YES
critical-contract                          YES
Kernel delta                               0
authority_effect                           none
implementation authorized                  false
RED authorized                             false
GREEN authorized                           false
model/provider experiment authorized       false
support_sufficient wiring authorized       false
RDD Stage 2 authorized                     false
```

### Decisión de admisión

**ADMIT TO PRE-RED CRITICAL CONTRACT HARDENING ONLY.**

La siguiente unidad, si el Owner la autoriza, debe endurecer el contrato de:

1. support evidence routing;
2. deterministic oracle eligibility/full-coverage;
3. blind experiment projection;
4. fail-closed behavior y bypass resistance.

No debe implementar todavía un oracle productivo ni ejecutar un assessor real.

## 18. Secuencia futura propuesta

```text
G0/G1 — THIS UNIT
        ↓
Pre-RED Critical Contract Hardening
        ↓
Four law questions
        ↓
Design 4R
        ↓
RDD Stage 1 Design Check
        ↓
HUMAN RED AUTHORIZATION
        ↓
RED focused on blind projection + routing contract
        ↓
GREEN minimal
        ↓
candidate FULL 4R / validation / RDD conformance
        ↓
human merge
        ↓
first DETERMINISTIC assessor experiment
        ↓
Qualification Pack V0.1
        ↓
measure exact inferential residual
        ↓
ONLY THEN consider human/local-model/model verifier
```

La secuencia no concede autorización automática a ninguna etapa posterior.
