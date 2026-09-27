---
title: Malāk E3 — Semantic Grounding Hardening — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation_design
language: es
created: 2026-09-27
baseline_commit: 2a2e0407a8472186775fa1ecd17f94f37721636a
source_run_id: bootstrap-u01-20260927-008
source_findings:
  - E008-SG-01
  - E008-SG-02
  - E008-SG-03
risk_class: 3
critical_contract: true
implementation_authorized: true
red_authorized: true
green_authorized: true
runtime_execution_authorized: false
self_modification_authorized: false
authority_effect: none
related:
  - docs/project/status/MALAK-EIGHTH-U01-SEMANTIC-GROUNDING-AUDIT-20260927.md
  - docs/project/sprints/proposals/MALAK-E3-ENGINEERING-ANALYZE-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-U007-F04-F06-E3-EPISTEMIC-CALIBRATION-G0-G1-DESIGN.md
  - docs/project/concepts/MALAK_EVIDENCE_BOUND_COGNITION_FOUNDATION.md
  - src/malak/capabilities/_engineering_analysis.py
  - src/malak/capabilities/engineering_analyze.py
  - src/malak/capabilities/engineering_propose.py
---

# Malāk E3 — Semantic Grounding Hardening — G0/G1 Design

## 1. Propósito

Diseñar el siguiente gate mínimo para el límite de assurance expuesto por el
Octavo U01:

~~~text
real evidence refs
but
materially incorrect claim-to-evidence bindings
+ unreconciled A4/A6 conclusions
~~~

La pregunta de admisión es:

> ¿Qué control mínimo puede impedir que un análisis estructuralmente válido sea
> consumido como semánticamente coherente cuando sus propios bindings o findings
> materiales no lo demuestran?

Este documento no implementa la respuesta.

## 2. Baseline y trigger

~~~text
baseline:
2a2e0407a8472186775fa1ecd17f94f37721636a

source run:
bootstrap-u01-20260927-008

source disposition:
INCONCLUSIVE

artifact integrity:
PASS

semantic audit:
GAP_REQUIRES_HARDENING
~~~

El diseño previo de calibración E3 declaró:

~~~text
if V0 repeats the error under correct evidence
-> a structured epistemic field may be justified in a separate gate
~~~

El Octavo U01 activa ese trigger porque:

- `focus_complete == true`;
- la fuente normativa `kernel.md` estaba presente;
- KIC-02 y KIC-05 resolvían la relación A6;
- el output aun produjo un `UNRESOLVED` contradictorio con A4;
- múltiples rationale atribuyeron contenido a refs que no lo contenían.

## 3. Clasificación de riesgo

~~~text
risk_class: 3 / high
critical_contract: true
~~~

E3 produce e interpreta evidence usada por:

- clasificación de findings;
- elegibilidad de E4;
- disposición terminal del internal interaction runner;
- revisión humana posterior.

El cambio no posee autoridad, pero puede alterar qué caminos informativos se
ejecutan o se bloquean. Por ello requiere hardening pre-RED, Design 4R, RDD Stage
1 Design Check y Candidate FULL 4R si se autoriza implementación.

## 4. Problema exacto

El contrato actual demuestra:

~~~text
JSON shape valid
evidence IDs exist
R/K surfaces present
baseline/focus bound
authority_effect none
~~~

No demuestra:

~~~text
each cited line supports the material claim
all described source identities are correct
materially equivalent findings are mutually coherent
UNRESOLVED considered supplied higher-authority resolution evidence
~~~

La corrección no debe prometer una validación semántica determinista general que
la implementación no pueda realizar.

## 5. Invariantes obligatorios

~~~text
SGH-01  evidence identity remains exact and candidate-bound
SGH-02  model output remains untrusted data
SGH-03  claim support must be explicit and auditable
SGH-04  structural grounding != semantic assurance
SGH-05  unresolved material conflict remains fail-closed
SGH-06  no second hidden authority or auto-approval
SGH-07  E3/E4 shared analysis contract remains single-source
SGH-08  no Kernel, Planner or runtime responsibility moves into this gate
SGH-09  existing artifacts remain historical and immutable
SGH-10  authority_effect remains none
~~~

## 6. Opciones evaluadas

### Opción A — segundo prompt-only patch

~~~text
disposition: REJECT AS SOLE CONTROL
~~~

Ventaja:

- delta mínimo.

Problema:

- la calibración anterior ya añadió reglas explícitas;
- el Octavo U01 volvió a omitir evidencia resolutiva;
- no crea una garantía verificable nueva;
- no mejora la auditabilidad de cada binding.

Un ajuste de prompt puede complementar el gate, pero no constituye por sí solo
la remediation suficiente.

### Opción B — semantic entailment determinista general

~~~text
disposition: REJECT
~~~

No existe un algoritmo local simple que pueda demostrar entailment semántico
general entre cualquier claim y líneas arbitrarias sin introducir otro sistema
cognitivo, nueva autoridad implícita o una falsa garantía.

### Opción C — segundo modelo validador obligatorio

~~~text
disposition: OBSERVE
~~~

Podría aportar revisión independiente, pero introduce:

- otra llamada de modelo;
- nueva configuración y costo;
- nuevas condiciones de fallo;
- una segunda superficie probabilística;
- dudas de independencia real si usa el mismo provider/modelo.

No es el cambio mínimo demostrado por este incidente.

### Opción D — binding estructurado y assurance explícito

~~~text
disposition: ADAPT / CANDIDATE FOR HARDENING
~~~

El output debe hacer explícita la función de cada ref y el límite de assurance,
sin afirmar que la estructura prueba entailment.

## 7. Contrato candidato

La forma exacta debe cerrarse durante Critical Contract Hardening antes de RED.
El candidato mínimo deberá representar por finding, de manera equivalente:

~~~text
classification
statement
rationale
supporting_repository_refs
supporting_knowledge_refs
limiting_or_counterevidence_refs
uncertainty_basis
~~~

`uncertainty_basis` sólo aplica a `UNRESOLVED` y debe pertenecer a:

~~~text
CURRENT_MATERIAL_AMBIGUITY
INSUFFICIENT_SUPPLIED_EVIDENCE
UNRESOLVED_CURRENT_PRECEDENCE
~~~

Reglas candidatas:

1. una clase relacional requiere soporte R y K separado;
2. `UNRESOLVED` debe identificar exactamente qué condición actual lo bloquea;
3. una incertidumbre de arquitectura debe citar al menos una fuente normativa o
   especificación aprobada aplicable, no sólo una fuente conceptual o derivada;
4. counterevidence material conocido no puede omitirse silenciosamente;
5. dos findings sobre la misma relación no pueden terminar en disposiciones
   incompatibles sin un conflicto explícito;
6. el renderer debe mantener visibles path, line y authority class de cada ref;
7. el envelope debe declarar qué assurance fue realmente ejecutado.

Estado candidato de assurance:

~~~text
STRUCTURALLY_GROUNDED
SEMANTIC_REVIEW_REQUIRED
SEMANTICALLY_REVIEWED
~~~

Estos nombres son provisionales. El hardening debe evitar migraciones ambiguas
desde `GROUNDED` y demostrar compatibilidad o una transición explícita.

## 8. Qué puede validarse determinísticamente

El candidate podrá validar sin interpretación semántica general:

- que cada ref exista en el packet exacto;
- que repository refs y knowledge refs estén en sus campos correctos;
- que no existan duplicados entre roles incompatibles;
- que `uncertainty_basis` sea obligatorio sólo para `UNRESOLVED`;
- que una incertidumbre normativa cite conocimiento con authority class
  suficiente;
- que campos, tamaños, caracteres y enums respeten límites;
- que el output permanezca ligado al baseline y Evidence Focus;
- que la ausencia de assurance requerida falle de forma cerrada.

No puede declarar determinísticamente, sin otro mecanismo:

- verdad general del statement;
- entailment semántico completo;
- exhaustividad conceptual absoluta;
- corrección arquitectónica final.

Esa frontera debe quedar visible en código, tests y documentación.

## 9. Consistencia entre findings

### 9.1 Resultado de inspección del mecanismo `relation_key`

El hardening inspeccionó el contrato vigente de
`GovernedEngineeringEvidenceFocus`.

Actualmente el focus contiene:

~~~text
focus_id
focus_label
inspection_term
repository_required_selectors
knowledge_required_selectors
supplemental_terms
supplemental_max_matches_per_kind
~~~

No contiene una taxonomía gobernada de relaciones o invariantes evaluables.

Por tanto un `relation_key` libre producido únicamente por el modelo tendría la
misma debilidad que el statement actual:

~~~text
model-generated relation_key
!= deterministic relation identity
~~~

El modelo podría asignar keys distintas a A4 y A6 y evitar accidentalmente el
control de conflicto. Una comparación textual o por similitud tampoco constituye
una garantía arquitectónica estable.

Disposición:

~~~text
free-form relation_key                    REJECT
lexical/similarity conflict detector      REJECT
focus-governed relation catalog           ADAPT / SEPARATE SCOPE REQUIRED
~~~

Un catálogo gobernado exigiría ampliar `GovernedEngineeringEvidenceFocus`, sus
schemas, tests y binding. Esa superficie estaba expresamente fuera del scope
admitido para este gate y no puede incorporarse por corrección lateral.

### 9.2 Consistency review separado

La alternativa de un consistency review separado conserva dos variantes:

~~~text
human semantic review
OR
independent machine-assisted semantic review
~~~

La revisión humana es el único mecanismo actualmente disponible cuya autoridad y
limitaciones están definidas. No provee continuidad automática E3 -> E4.

Un reviewer asistido por modelo requeriría diseño propio de:

~~~text
independence
evidence packet binding
failure semantics
provider/model diversity or justified equivalence
resource budget
terminal aggregation
authority_effect none
~~~

No se autoriza introducirlo dentro de este gate.

### 9.3 Decisión de hardening

El mecanismo de consistencia no puede cerrarse dentro del scope actual sin una
de estas ampliaciones materiales:

~~~text
A. governed relation catalog in Evidence Focus
B. separately designed semantic reviewer
~~~

Ambas requieren admisión y autorización explícitas.

Hasta resolver esta decisión:

~~~text
Critical Contract Hardening  INCONCLUSIVE
RED                            NOT ADMISSIBLE
~~~

Esta conclusión no invalida el valor del binding estructurado candidato. Impide
presentarlo falsamente como cierre suficiente del finding E008-SG-01.

### 9.4 Ruta seleccionada por el Owner

El Owner autorizó ampliar G0/G1 y RED contractual para la ruta A:

~~~text
minimal governed relation catalog in Evidence Focus
~~~

Contrato exacto candidato:

~~~text
GovernedEngineeringRelation
├── relation_id
├── relation_label
└── evaluation_question

GovernedEngineeringEvidenceFocus
└── governed_relations: tuple[GovernedEngineeringRelation, ...]
~~~

Reglas:

1. `relation_id` es estable, namespaced por `focus_id` y no lo genera el modelo;
2. formato V0: `<FOCUS_ID>.<UPPER_SNAKE_RELATION>`;
3. IDs, labels y questions son no vacíos, acotados e inmutables;
4. no se permiten IDs duplicados dentro de un focus;
5. el catálogo forma parte de `evidence_set_digest`;
6. modificar el catálogo invalida evidencia focus-bound anterior;
7. sólo U01 recibe catálogo en este candidate;
8. U04 y RR-03 permanecen sin relaciones hasta gates propios;
9. catálogo y clasificación no crean autoridad;
10. el catálogo identifica una relación evaluable, no predetermina su resultado.

Catálogo U01 V0:

~~~text
U01.KERNEL_RESPONSIBILITY
U01.KERNEL_INSTANCE_CARDINALITY
U01.CAPABILITY_ROUTING
U01.RUNTIME_INDEPENDENCE
U01.MINIMAL_COMPLEXITY
~~~

La relación causal del Octavo U01 queda representada por:

~~~text
U01.KERNEL_INSTANCE_CARDINALITY

evaluation_question:
Do concrete Kernel instances preserve one architectural Core Kernel?
~~~

Esta selección cierra únicamente identidad de relación dentro del Focus U01.
No autoriza cambiar el schema E3, consumir `relation_id` downstream ni afirmar
semantic entailment. El Owner autorizó después un GREEN separado y limitado a la
fundación del catálogo en `_engineering_evidence.py`.

### 9.5 Critical Contract Hardening — relation catalog foundation

El hardening pre-RED del catálogo base cierra:

~~~text
contract owner          GovernedEngineeringEvidenceFocus
relation type           GovernedEngineeringRelation
relation fields         relation_id, relation_label, evaluation_question
relation id format      <FOCUS_ID>.<UPPER_SNAKE_RELATION>
relation id max         128 UTF-8 bytes
relation label max      256 UTF-8 bytes
evaluation question max 1024 UTF-8 bytes
unknown fields          rejected by constructor
missing fields          rejected by constructor
empty/whitespace text   rejected
control/format text     rejected
duplicate relation ids  rejected per focus
namespace mismatch      rejected per focus
catalog order           declared tuple order, stable
catalog digest binding  mandatory
authority_effect        none
~~~

Semántica de catálogo vacío:

~~~text
generic/ad-hoc focus  -> allowed
U04 / RR-03 current  -> preserved empty in this candidate
U01 bootstrap focus  -> exact non-empty V0 catalog required
~~~

La pregunta describe qué relación evaluar. No incluye expected classification,
expected answer ni una cita que obligue al modelo a producir `ALIGNED`.

Casos adversariales revisados:

- key inventada por el modelo: no puede entrar al catálogo;
- key duplicada con label distinta: rechazo por ID;
- namespace de otro focus: rechazo;
- cambio de catálogo sin invalidación: impedido por digest binding;
- catálogo conceptual usado como autoridad: prohibido por `authority_effect`;
- catálogo U01 propagado silenciosamente a U04/RR-03: test negativo;
- label/question con formato invisible o control: rechazo;
- reorder silencioso: cambia la identidad ligada al digest.

Resultado focalizado:

~~~text
Critical Contract Hardening — relation catalog foundation: PASS
downstream E3 relation consumption: NOT IN SCOPE / NOT AUTHORIZED
~~~

## 10. Impacto E3/E4/internal interaction

El análisis es compartido por:

~~~text
EngineeringAnalyzeCapability
EngineeringProposeCapability internal analysis
~~~

Todo cambio deberá mantener un único contrato fuente.

El hardening deberá especificar explícitamente:

- cómo E4 consume el nuevo output;
- qué estados permiten o bloquean Propose;
- qué estado terminal corresponde a falta de semantic assurance;
- cómo se preserva `INCONCLUSIVE != PASS`;
- cómo se evita reinterpretar artifacts históricos.

No se cambiará el terminal mapper por inferencia lateral.

## 11. Scope candidato por gates

### Gate G0/G1 — este documento

Objetivo:

- cerrar causa, opciones, límites y decisión de admisión.

Archivos:

~~~text
docs/project/status/MALAK-EIGHTH-U01-SEMANTIC-GROUNDING-AUDIT-20260927.md
docs/project/sprints/proposals/MALAK-E3-SEMANTIC-GROUNDING-HARDENING-G0-G1-DESIGN.md
~~~

Resultado esperado:

~~~text
audit preserved
candidate direction bounded
RED not yet authorized
~~~

### Gate hardening pre-RED futuro

Archivos candidatos:

~~~text
docs/project/sprints/proposals/MALAK-E3-SEMANTIC-GROUNDING-HARDENING-G0-G1-DESIGN.md
src/malak/capabilities/_engineering_analysis.py  # contract inspection only
src/malak/capabilities/engineering_analyze.py   # parser inspection only
src/malak/capabilities/engineering_propose.py   # shared consumer inspection only
src/malak/app/internal_interaction.py            # terminal consumer inspection only
tests/test_engineering_analyze.py                # RED design only
tests/test_engineering_propose.py                # RED design only
tests/test_internal_interaction_v0.py            # RED design only
~~~

El listado no autoriza modificaciones.

La inspección posterior de hardening determinó que este listado tampoco contiene
superficie suficiente para implementar un `relation_key` determinista. Cualquier
alternativa basada en un catálogo gobernado requeriría admitir explícitamente:

~~~text
src/malak/capabilities/_engineering_evidence.py
tests/test_governed_engineering_evidence_focus_v0.py
~~~

Esos archivos continúan fuera de alcance en el candidate actual.

El Owner autorizó posteriormente la ampliación G0/G1 y RED contractual a esos
dos archivos, y luego autorizó por separado el GREEN limitado a
`_engineering_evidence.py`. La autorización no incluye schema ni consumo E3/E4.

### RED futuro

Requiere autorización separada y deberá fallar causalmente, como mínimo, para:

1. ref existente pero ubicada en el rol equivocado;
2. `UNRESOLVED` sin `uncertainty_basis`;
3. incertidumbre arquitectónica sustentada sólo por fuente no normativa;
4. misma relación clasificada simultáneamente `ALIGNED` y `UNRESOLVED` sin
   conflicto explícito;
5. assurance ausente o sobredeclarado;
6. divergence del prompt/contract compartido E3/E4;
7. authority effect distinto de `none`.

### GREEN ejecutado — relation catalog foundation

El GREEN autorizado quedó limitado a:

~~~text
src/malak/capabilities/_engineering_evidence.py
tests/test_governed_engineering_evidence_focus_v0.py  # validación/corrección acotada
~~~

No incluye cambios de schema o consumo E3/E4. Kernel, Planner, runtime,
CapabilityRegistry y provider permanecen sin cambios.

## 12. Fuera de alcance

~~~text
Kernel
Planner
CapabilityRegistry
app composition
runtime/provider implementation
Ollama configuration
new model selection
downstream Evidence Focus/E3 schema expansion
Knowledge Reader
semantic retrieval
embeddings / RAG / GraphRAG
agents
tools
writes from model output
self-modification
RDD Stage 2
Ready / merge automation
~~~

## 13. Malāk Alignment Matrix

| Fuente | Clase | Invariante / intención | Disposición | Efecto candidato |
| --- | --- | --- | --- | --- |
| Cognitive Constitution | normativa | evidencia, contradicción y límites de confianza | ADOPT | findings no se aceptan por fluidez narrativa |
| Governance Constitution | normativa | Human in Control; output no es autoridad | ADOPT | `authority_effect = none` |
| Blueprint | normativa | Capability First; Kernel pequeño | ADOPT | cambio permanece en Engineering Capability |
| `SECURITY.md` | protegida/subordinada | model output no confiable; fail-closed | ADOPT | parsing y consumo no elevan confianza implícita |
| Architecture Quality Gates | referencia arquitectónica | limitar drift y complejidad | ADOPT | gate acotado y reversible |
| E3 accepted design | histórico/aceptado | findings R/K, strict schema, bounded output | ADAPT | binding más explícito sin autoridad nueva |
| E3 epistemic calibration | design histórico | current-state scope y trigger de estructura futura | ADOPT | el trigger del Octavo U01 se preserva |
| Eighth U01 audit | evidencia derivada | A4/A6 y misbinding | ADOPT | causal evidence del gate |
| Evidence-Bound Cognition Foundation | conceptual/no normativa | binding, contradiction handling, assurance | ADAPT | guía; no autoridad ni subsistema nuevo |
| Research Horizon / concepts | conceptual/no normativa | evidence != authority | OBSERVE | no adelantar Cognitive Receipt ni RDD Stage 2 |
| Roadmap | derivada | crecimiento incremental | OBSERVE | no convierte el hardening en sprint autorizado |
| Ideas | no normativa | validación y receipts futuros | OBSERVE | no crear registry/evaluator genérico |

## 14. Security Horizon Check

| Superficie | Resultado | Razón |
| --- | --- | --- |
| Model output trust | REQUIRES_REINFORCEMENT | el output estructuralmente válido contiene claims no respaldados |
| Authority expansion | ALREADY_COVERED | permanece `none` |
| Prompt/context trust | ALREADY_COVERED | evidence JSON continúa como datos no confiables |
| Persistent state | NOT_APPLICABLE | no se incorpora persistencia nueva |
| External execution | NOT_APPLICABLE | no se agregan side effects |
| AI supply chain | NOT_APPLICABLE | no cambia modelo/provider |
| Observability/evidence | REQUIRES_REINFORCEMENT | binding y assurance deben quedar explícitos |
| Human in Control | ALREADY_COVERED | revisión y merge permanecen humanos |

## 15. Cuatro preguntas de ley

### Blueprint

~~~text
PASS
~~~

La responsabilidad permanece en Engineering Capability. Kernel delta `0`.

### Cognitive Constitution

~~~text
PASS
~~~

El candidate busca impedir que presencia de evidencia sea confundida con soporte
semántico y exige exponer contradicciones materiales.

### Governance Constitution

~~~text
PASS
~~~

Ningún output autoriza cambios, ejecución o promoción.

### Kernel complexity

~~~text
PASS
~~~

Kernel, Planner y CapabilityRegistry quedan fuera de alcance.

## 16. Design 4R

### Risk — PASS

Riesgos principales:

- falsa seguridad por nombre de estado;
- contrato estructurado demasiado complejo;
- romper compatibilidad E3/E4;
- convertir validación en autoridad;
- introducir un segundo evaluador sin independencia real.

Mitigación:

- hardening antes de RED;
- una sola representación compartida;
- límites y enums cerrados;
- fail-closed;
- scope y correction budget explícitos.

El catálogo no ejecuta modelos, no decide clasificaciones y no produce efectos.

### Readability — PASS

Tipo, ID namespaced, label y pregunta evaluable separan identidad técnica de texto
humano. El catálogo U01 queda declarado en un único lugar.

### Reliability — PASS

El diseño rechaza IDs libres, duplicados, namespaces ajenos y catálogo no ligado
al digest. Las rutas genéricas existentes conservan catálogo vacío y el cambio
downstream E3 queda separado.

### Resilience — PASS

Entradas ausentes, inválidas, duplicadas, fuera de namespace, sobredimensionadas
o con caracteres invisibles fallan antes de recolectar evidencia o llamar modelos.

Resultado:

~~~text
Design 4R — relation catalog foundation: PASS
Design 4R — downstream E3 consumption: NOT EXECUTED / NOT AUTHORIZED
~~~

## 17. RDD Stage 1 Design Check

~~~text
candidate identity strategy        PASS
baseline/evidence binding          PASS
Writer/Reviewer/Validator split    PASS
PASS|FAIL|INCONCLUSIVE discipline  PASS
candidate change invalidation      PASS
bounded correction                 PASS
authority_effect                   none
RDD Stage 2                        NOT AUTHORIZED
overall                            PASS
~~~

Estrategia de identidad:

~~~text
baseline commit
+ exact allowed files
+ test candidate diff hash captured before execution
+ pytest command and result
~~~

Separación preservada:

~~~text
Writer     -> future GREEN actor within approved files
Reviewer   -> Candidate FULL 4R after GREEN
Validator  -> focused tests + independent validation when required
Authority  -> Owner only
~~~

El futuro semantic reviewer downstream continúa fuera de alcance. No se asume
independencia por usar otro prompt o llamada.

Resultado:

~~~text
RDD Stage 1 Design Check — relation catalog foundation: PASS
RDD Stage 1 Candidate Conformance: PASS — relation catalog foundation
~~~

## 18. STOP conditions

Detener antes de RED si:

- no se cierra el mecanismo de consistencia;
- el schema afirma semantic assurance que no puede demostrar;
- el diseño requiere cambiar Kernel o runtime;
- E3 y E4 divergen;
- un nuevo evaluator adquiere autoridad implícita;
- el cambio exige ampliar Evidence Focus sin gate separado;
- aparece una alternativa más simple que preserve las mismas garantías;
- baseline cambia materialmente.

## 19. Validation plan candidato

Cuando RED/GREEN sea autorizado:

1. tests focalizados del contrato y parser;
2. tests compartidos E3/E4;
3. tests del internal interaction mapper;
4. UTF-8 y `git diff --check`;
5. Candidate FULL 4R;
6. bounded correction si existen findings;
7. Fix Validator independiente cuando aplique;
8. E2E focalizado con provider determinista;
9. suite completa Windows/Ubuntu cuando corresponda;
10. RDD Stage 1 Candidate Conformance;
11. runtime follow-up sólo con autorización humana separada.

Un test de prompt por substring no demostrará por sí solo el cierre.

### 19.1 Registro de corrida RED no admisible

Una primera corrida focalizada fue ejecutada antes de cerrar formalmente Design
4R y RDD Stage 1 Design Check en este documento.

~~~text
command:
.\.venv\Scripts\python.exe -m pytest \
  tests/test_governed_engineering_evidence_focus_v0.py -k sgh -q

observed:
12 failed, 27 deselected

direct cause:
GovernedEngineeringRelation missing
GovernedEngineeringEvidenceFocus.governed_relations missing

candidate test diff hash:
d10aa95aa9a8ef8eaf9142c244e58316c9b9210c
~~~

Disposición:

~~~text
technical causal failure  OBSERVED
sequence compliance       FAIL
RED evidence              INVALID_SEQUENCE / NOT_ADMISSIBLE
authority_effect          none
~~~

Esta corrida no se reutiliza como RED válido y no se reconstruye retroactivamente
como PASS. Después de los checkpoints pre-RED debe existir un nuevo candidate RED
material, una identidad nueva y una nueva ejecución focalizada.

### 19.2 Nuevo candidate RED admisible

Después de cerrar los checkpoints pre-RED se agregaron casos materiales para:

- duplicate relation ID con texto distinto;
- namespace de relación distinto del `focus_id`;
- límites UTF-8 de label/question;
- caracteres de formato invisibles.

Identidad previa a ejecución:

~~~text
baseline:
2a2e0407a8472186775fa1ecd17f94f37721636a

allowed RED file:
tests/test_governed_engineering_evidence_focus_v0.py

test candidate diff hash:
e35787a04a3163155279981e9e19317ec08806ea

production delta:
0
~~~

La ejecución deberá usar el mismo comando focalizado. Cualquier cambio posterior
al test candidate invalida esta identidad y exige recaptura antes de ejecutar.

Resultado observado:

~~~text
candidate hash verified  PASS
tests selected           18
tests failed             18
tests deselected         27
production delta         0

direct causes:
- GovernedEngineeringRelation missing
- GovernedEngineeringEvidenceFocus.governed_relations missing
~~~

Disposición:

~~~text
causal RED failure       PASS
scope fidelity           PASS
candidate identity       PASS
relation catalog RED     PASS
authority_effect         none
~~~

Este PASS significa que RED falló por la ausencia exacta del contrato candidato.
No significa GREEN, corrección implementada ni aceptación del diseño downstream.

### 19.3 GREEN autorizado y resultado focalizado

El Owner autorizó GREEN únicamente para la fundación del catálogo gobernado en
`_engineering_evidence.py`. La implementación agregó:

- `GovernedEngineeringRelation` inmutable;
- validación de formato namespaced, texto, categorías invisibles y límites UTF-8;
- `governed_relations` como tuple ordenada en Evidence Focus;
- rechazo de tipos, duplicados y namespace ajeno;
- binding del catálogo no vacío a `evidence_set_digest`;
- catálogo V0 de U01;
- preservación exacta del catálogo vacío para U04, RR-03 y focos ad hoc.

Resultado focalizado inicial:

~~~text
command:
.\.venv\Scripts\python.exe -m pytest \
  tests/test_governed_engineering_evidence_focus_v0.py -k sgh -q

result:
18 passed, 27 deselected
~~~

La ejecución completa del archivo focal obtuvo:

~~~text
45 passed
~~~

### 19.4 Candidate FULL 4R y bounded correction

Candidate FULL 4R no encontró findings bloqueantes:

~~~text
Risk         PASS — fail-closed, sin autoridad ni side effects
Readability  PASS — identidad, label y pregunta permanecen separados
Reliability  PASS — catálogo ligado al digest; vacíos preservados fuera de U01
Resilience   PASS — entradas inválidas se rechazan antes de recolectar evidencia
~~~

La revisión identificó tres coberturas negativas faltantes, corregidas dentro del
budget aprobado sin ampliar producción:

- contenedor no tuple;
- elemento de catálogo con tipo desconocido;
- límite UTF-8 de `relation_id`.

Identidad del candidate fuente + tests después de la corrección:

~~~text
candidate diff hash:
747c3b1afbe98f2d8ee710cc8b79efdcf5832954
~~~

Revalidación:

~~~text
focused SGH       21 passed, 27 deselected
full focus file   48 passed
~~~

### 19.5 Validación de integración y suite completa

La validación focalizada de consumidores existentes cubrió:

~~~text
tests/test_engineering_inspect.py
tests/test_engineering_analyze.py
tests/test_engineering_propose.py
tests/test_internal_interaction_v0.py
tests/test_internal_interaction_test_v0_harness.py

result: 276 passed in 274.61s
~~~

La suite completa local Windows obtuvo:

~~~text
command:
.\.venv\Scripts\python.exe -m pytest -q

result:
1620 passed in 405.28s (0:06:45)
~~~

No se llamó a Ollama, no se generaron artifacts runtime y no se ejecutó
`/self-review`. La validación independiente por otro agente no fue ejecutada y no
se presenta como evidencia disponible.

## 20. Rollback

En este gate documental:

~~~text
rollback
-> retirar únicamente los dos documentos nuevos antes de commit
~~~

En un GREEN futuro, el rollback deberá limitarse al contrato E3/E4 y sus tests
autorizados. No se utilizarán operaciones destructivas de Git.

## 21. Estado de autoridad

~~~text
G0/G1 design              PREPARED
Critical Contract Hardening PASS — relation catalog foundation
Four Questions of Law      PASS
Design 4R                  PASS — relation catalog foundation
RDD Stage 1 Design Check   PASS — relation catalog foundation
first RED run              INVALID_SEQUENCE / NOT_ADMISSIBLE
RED relation catalog       PASS — 18 causal failures / candidate e35787a...
RED E3 consumption         NOT AUTHORIZED
GREEN relation catalog     PASS — candidate 747c3b1...
Candidate FULL 4R          PASS — no blocking findings
bounded correction         PASS — negative coverage only
focused validation         PASS — 21 selected / 48 file total
integration validation     PASS — 276 passed
full local suite           PASS — 1620 passed
independent validation     NOT EXECUTED
runtime execution          NOT AUTHORIZED
self-modification          NOT AUTHORIZED
Ready                      OWNER ONLY
merge                      OWNER ONLY
authority_effect           none
~~~

Siguiente transición lícita:

~~~text
owner reviews candidate and validation evidence
-> independent validation if explicitly authorized/required
-> owner decides whether to authorize commit/push or further downstream design
~~~
