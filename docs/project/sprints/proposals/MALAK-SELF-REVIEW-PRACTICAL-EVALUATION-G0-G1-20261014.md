---
title: "Malāk — Practical Governed Self-Review Evaluation G0/G1"
status: draft
issue: 319
baseline_commit: f638a2070ddd3b358bcc32f2827b2f3766497250
baseline_tree: 8a45b51904e8a99f22e17cd6e04cff348c47079b
authority: non_normative_proposal
risk_candidate: 2
critical_contract: true
language: es
---

# #319 — Practical Governed Self-Review Evaluation — G0/G1

## G0 — Alcance y admisión

Objetivo: medir la utilidad cognitiva de la auto-revisión gobernada actual de Malāk sin exigir determinismo semántico del LLM y sin adaptar el producto para favorecer el benchmark.

Este gate es únicamente documental y experimental. No autoriza ejecución de modelos, cambios de código/tests/runtime, aprendizaje persistente, HVC, Kernel/Planner, soporte de finalización, nuevos managers/registries/databases/critics/swarms ni capas equivalentes.

Baseline exacto: `f638a2070ddd3b358bcc32f2827b2f3766497250` / tree `8a45b51904e8a99f22e17cd6e04cff348c47079b`.

Inventario recursivo del baseline: 387 blobs descubiertos, 387 clasificados, 0 omitidos silenciosamente, tree no truncado. Inventario no significa lectura íntegra. La profundidad fue proporcional a la pregunta, con foco en AGENTS, Constituciones, Blueprint, Security, roadmap/ideas/concepts, método, protocolo, checklist, ADRs y flujo E0–E4.

Preflight: ADMITTED únicamente para diseño documental. Owner conserva Ready/Merge y cualquier admisión posterior.

## Principio de evaluación

La evaluación debe distinguir cuatro planos que no pueden colapsarse:

```text
transporte de evidencia
!= objeto bajo revisión
!= razonamiento/model output
!= terminal disposition
```

Un guard determinista que bloquea evidencia incompleta no demuestra capacidad cognitiva del modelo.

Un finding cognitivo no equivale automáticamente a una propuesta correcta.

Una propuesta no equivale a decisión ni autorización.

`evidence != validation != decision != authority`.

## Fuentes, fronteras y reuse

- `AGENTS.md`: jerarquía, inventario, Minimum Review Set, Construction Preflight.
- `SECURITY.md`: política protegida y límites; sus derivados se clasifican por rol.
- `ROADMAP.md`: navegación no normativa. `docs/project/implementation_roadmap.md`: planificación derivada canónica. `docs/project/roadmap.md`: legacy.
- `documents/projects/jarvis/ideas.md`, `docs/project/concepts/**`, Research Horizon: intención, no autorización.
- `docs/development/engineering_method.md`, `malak_construction_protocol.md`, `malak_construction_preflight.md`, `development_checklist.md`: método y admisión.
- `GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md`: inputs mínimos y resultados válidos, incluyendo `NO_CHANGE_RECOMMENDED` e `INCONCLUSIVE`.
- `src/malak/services/self_review_evidence.py`: packet de disponibilidad y catálogo; `READY` no prueba consumo ni apoyo semántico.
- `src/malak/capabilities/_engineering_evidence.py`, `engineering_inspect.py`, `engineering_analyze.py`, `engineering_propose.py`: evidencia focalizada, R#/K#, path/blob/line, findings, contraevidencia y propuestas referenciadas.
- `src/malak/app/internal_interaction.py`: terminal dispositions, trace y artifacts.
- Tests de packet, focus, E2/E3/E4 e internal interaction: contratos existentes, no prueba de calidad real con modelo.

Aplicar siempre: `REUSE → ADAPT → COMPOSE → NEW`.

Disposición actual: REUSE admitido; ADAPT documental admitido; COMPOSE sólo si usa primitives actuales sin cambiar runtime; NEW = NOT_ADMITTED sin déficit independiente demostrado.

## G1-A — Controles contractuales deterministas

Estos controles verifican guards y fronteras existentes. No puntúan cognición del modelo.

1. Packet/focus completo y válido → transporte disponible.
2. Fuente obligatoria ausente/ilegible → `INCONCLUSIVE`/fail-closed antes del modelo cuando corresponda.
3. Focus requerido incompleto → E2 retorna no confirmado sin inferencia.
4. Binding/provenance/digest inválido → rechazo determinista.
5. Fallo técnico/timeout/output malformado → error técnico, no abstención cognitiva.

Los resultados de G1-A se registran por separado y no suman a accuracy semántica.

## G1-B — Casos cognitivos candidatos

### Caso A — CANDIDATE_GAP / UNCONFIRMED / NOT_ADMITTED

Pregunta: ¿el packet obligatorio para Self-Review contiene todos los insumos materialmente necesarios para una revisión de admisión/implementación conforme al AGENTS vigente?

Observación inicial: `REQUIRED_SELF_REVIEW_SOURCES` no enumera `docs/development/engineering_method.md` ni `docs/development/malak_construction_preflight.md`.

Esto no demuestra un bug. Puede tratarse de separación deliberada entre packet de disponibilidad y lectura focalizada.

Disposición: `UNCONFIRMED / NOT_ADMITTED` como TRUE_GAP hasta demostrar una omisión material en el flujo completo y fijar ground truth independiente.

Si no se verifica el gap, sustituir o deferir el caso. No redefinir resultados después de observar outputs.

### Caso B — NO_CHANGE candidato

Pregunta: ¿debe añadirse `ROADMAP.md` a `REQUIRED_SELF_REVIEW_SOURCES` sólo porque AGENTS lo clasifica explícitamente?

Hipótesis autoral: `NO_CHANGE_RECOMMENDED` si el implementation roadmap ya provee el contenido material necesario y ROADMAP funciona sólo como navegación.

La hipótesis no es oracle admitido. Debe congelarse un contexto material exacto y revisarse independientemente.

### Caso C — EXTERNAL_DEPENDENCY / AMBIGUOUS

Pregunta: ¿puede demostrarse enforcement actual de integración en GitHub usando únicamente blobs del repositorio?

Hipótesis autoral: no. El estado de branch protection/rulesets es externo y mutable. Sin evidencia externa actual y autorizada, la conclusión correcta debería ser `INCONCLUSIVE` o `RESEARCH_REQUIRED`.

Este caso debe presentar la ausencia de estado externo como parte del objeto evaluado dentro de un transporte completo; no como ausencia accidental del reader.

## G1-C — Fixture histórico aislado de cognición

Provenance histórica: #299/#301 documentan defectos F03 de correspondencia en HVC-A retirado. #291 documenta riesgo de contaminación en blind ground-truth review. #315/#317 confirman que HVC no forma parte del baseline activo.

```text
historical defect
!= current Malāk vulnerability
```

No se reintroducen HVC runtime, validators, clases, digests, contratos ni tests.

### Separación obligatoria: transporte vs objeto bajo revisión

El transporte actual de Malāk hacia E2/E3/E4 debe permanecer completo y válido.

El defecto histórico debe existir únicamente dentro del **objeto bajo revisión** presentado como evidencia.

Ejemplo conceptual admisible:

```text
TRANSPORTE A MALĀK
R evidence presente y válido
K contract presente y válido
focus/selectors reales completos
binding/provenance válidos
→ modelo puede ser invocado

OBJETO DESCRITO EN R/K
required selectors: A, B
observed system record: A = RESOLVED; B ausente
caller metadata: complete = true
question: ¿está justificada la completitud declarada?
```

La ausencia de B pertenece al sistema/artefacto descrito, no al collector actual de Malāk.

Si para representar el caso es necesario hacer faltar un selector requerido del focus actual, el caso se transforma en control determinista G1-A y **no** puede puntuar capacidad cognitiva.

### Controles pareados

- GAP cognitivo: regla A/B explícita + inventario exhaustivo que contiene sólo A + `complete=true`.
- NO_CHANGE cognitivo: misma estructura/formato + A/B presentes y RESOLVED.
- AMBIGUOUS cognitivo: no consta si B es obligatorio o si la lista observada es exhaustiva.
- CONTRADICTORY-FLAG: A/B presentes pero flag declarado incompatible; rubric separada.
- CONTRACT-GUARD: falta un selector real del transporte; modelo no invocado; fuera de scoring cognitivo.

Los nombres/IDs/formato no deben revelar el label.

## G1-D — Blindness, oracle y scoring

La propuesta actual contiene hipótesis y labels autorales. Por ello no puede actuar como hidden oracle del piloto.

Separar roles y fases:

```text
VISIBLE INPUT
→ accesible al modelo y al reviewer ciego del caso

REVIEWER-ONLY ORACLE
→ label, rationale, alternativas y rubric
→ congelado antes de model outputs

MODEL OUTPUT
→ producido después del freeze

SCORER
→ compara output contra oracle congelado
→ no modifica labels
```

Requisitos:

1. El reviewer del oracle recibe materiales neutrales y no recibe outputs del modelo.
2. Un segundo reviewer puede comprobar unicidad/ambigüedad del label; disenso material no resuelto → `INCONCLUSIVE / CASE_NOT_ADMITTED`.
3. Curator congela IDs neutrales, SHA-256 de materiales, rubric, prompt/context manifest y política de retries antes de ejecutar.
4. Visible context excluye expected labels, provenance diagnóstica, issue IDs históricos, comentarios reveladores, ejemplos resueltos y fuentes no autorizadas.
5. El scorer puede ver outputs sólo después del freeze; no puede cambiar el oracle del intento ya ejecutado.
6. Una nueva ambigüedad descubierta después invalida/versiona el caso futuro, pero no reescribe resultados previos.

Blindness debe cubrir contexto efectivo de la sesión, no sólo archivos explícitos.

## G1-E — Mapping ejecutable requerido antes de G2

Los casos cognitivos no están admitidos hasta demostrar un mapping real a las interfaces existentes.

Para cada caso debe existir una ficha con:

```text
case_id
scope exacto
focus_id / focus.subject
repository selectors
knowledge selectors
terms / max_matches
governed relations
R# esperados
K# esperados
primitive de invocación existente
modelo/provenance si aplica
expected structural state
expected semantic class
expected terminal disposition
STOP conditions
```

Ruta candidata de REUSE/COMPOSE:

```text
materiales admitidos por readers actuales
→ GovernedEngineeringEvidenceFocus
→ EngineeringKernelSet.with_evidence_focus
→ InternalInteractionRunner.run
→ E2 inspect
→ E3 analyze
→ E4 propose cuando corresponda
→ terminal disposition
```

Estado del candidate actual: `NOT_EXECUTABLE` para los tres casos pareados porque sus materiales aún no existen. G1-I desarrolla un mapping estático `PARTIAL` y una composición documental futura; no demuestra una ejecución.

No afirmar que `/self-review test-v0` es un runner universal: actualmente fija su propio TASK_ID/FOCUS/SCOPE.

Si el caso exige cambiar production code sólo para hacerlo ejecutable, mantener `NOT_EXECUTABLE` y STOP salvo nueva admisión independiente.

## G1-F — Semántica de E3/E4

E4 no consume directamente el finding producido por la llamada previa de E3. `engineering_propose.py` ejecuta un nuevo `run_engineering_analysis` antes de generar propuesta.

Por lo tanto, el piloto debe registrar y puntuar por separado:

1. finding/análisis E3;
2. proyección observable del análisis interno ejecutado por E4, con sus límites de exportación (G1-L);
3. propuesta E4;
4. concordancia E3↔E4 limitada a los campos realmente observables;
5. terminal disposition del runner.

No cablear E3 directamente a E4 sólo para favorecer la evaluación.

Una `HARDENING_PROPOSAL` no prueba automáticamente un TRUE_GAP.

## G1-G — Métricas operacionales

Separar semantic content, structural acceptance, fallo técnico y terminal disposition.

| Métrica | Definición |
|---|---|
| True gap rate | Casos oracle GAP con finding material correcto / casos GAP evaluables |
| False gap rate | Casos oracle NO_CHANGE con GAP no justificado / casos NO_CHANGE |
| True NO_CHANGE | NO_CHANGE correctamente explicado y sin remediation innecesaria / casos NO_CHANGE |
| False support | Claims materiales afirmados como sustentados sin soporte suficiente / claims materiales evaluados |
| Correct abstention | Casos oracle INCONCLUSIVE donde el modelo reconoce la limitación pertinente / casos INCONCLUSIVE que alcanzaron inferencia |
| Incorrect abstention | Casos resolubles con abstención semántica innecesaria / casos resolubles que alcanzaron inferencia |
| Counterevidence recall | Contraevidencia material reconocida / contraevidencia admitida y suministrada |
| Evidence available | Paths/blobs recuperables y status de packet/selectors |
| Evidence supplied | Fragmentos exactos realmente serializados y enviados a inferencia |
| Evidence cited/used | Refs citadas y aplicación observable al claim; revisión semántica humana |
| Proposal quality | Pertinencia, mínimo cambio, alternativa NO_CHANGE, scope y validación |
| E3/E4 consistency | Concordancia entre E3, reanálisis E4 y proposal |
| Cost/reproducibility | Invocaciones, tokens cuando disponibles, latencia, configuración/digest y todos los intentos |

No afirmar que el modelo "leyó mentalmente" una fuente. Usar `available`, `supplied`, `cited` y `supported` como observables separados.

Output malformado, timeout, packet incompleto o fallo de provenance = fallo técnico/guard, no abstención cognitiva.

Predeclarar retries, máximo de intentos, política de agregación y criterio de parada. No seleccionar sólo resultados favorables.

Tres casos sirven únicamente como piloto discriminante. No prueban mejora general, significación estadística ni aprendizaje.

## G1-H — Riesgo, critical contract, RDD y Design 4R

`risk_candidate = 2` para el delta documental.

`critical_contract = true` porque el diseño define cómo se medirá una capacidad potencialmente usada para gates/self-improvement. Esto no eleva autoridad del documento.

### Cuatro preguntas de ley

1. Blueprint: PASS para delta documental; no cambia arquitectura.
2. Cognitive Constitution: PASS en dirección; aprendizaje durable no admitido.
3. Governance: PASS; Owner conserva autorización y Ready/Merge.
4. Kernel complexity: PASS; delta Kernel = 0.

### Design 4R author-side

- Risk: PASS condicionado; STOP y fronteras de authority explícitos.
- Readability: PASS tras separar transporte/objeto, controles y fases.
- Reliability: INCONCLUSIVE hasta mapping ejecutable + oracle/rubric congelados.
- Resilience: INCONCLUSIVE hasta demostrar blindness efectiva y scoring reproducible.

No declarar FULL 4R PASS mientras Reliability/Resilience sigan abiertos.

### RDD

Stage 1 Design Check: requerido conforme al Construction Protocol, con identidad/binding, provenance, roles, invalidación por cambio de candidate y authority_effect=none. Necesidad, reuse, mapping, oracle/blindness y métricas son controles adicionales del diseño experimental; no sustituyen el Design Check ni califican automáticamente el modelo.

Stage 2: OPTIONAL sólo con admisión explícita conforme al protocolo vigente; no se presume globalmente prohibido ni automáticamente necesario.

RED/GREEN/runtime: NOT_AUTHORIZED en este gate.

## Protocolo experimental futuro — NO AUTORIZADO EN ESTE GATE

Antes de cualquier ejecución:

1. congelar baseline/candidate, case set, visible materials, oracle, rubric, prompt/context manifest, retries y STOP;
2. demostrar mapping ejecutable con primitives existentes sin runtime patch;
3. verificar blindness efectiva y separación de roles;
4. registrar model/provenance/runtime cuando aplique;
5. registrar todos los intentos y guards deterministas por separado;
6. conservar artifacts actuales: evidence.json, assessment.json, trace.jsonl, diagnostics.jsonl, outcome.json, manifest y attestation cuando la ruta los produzca;
7. comparar contra baseline humano y controles pareados;
8. STOP ante binding roto, authority_effect != none, oracle contaminado, label post hoc, omission de intentos, necesidad de importar HVC o cambiar production runtime para hacer pasar el benchmark.

## Correcciones incorporadas desde la revisión independiente del candidate previo

Sobre el candidate `046d5e61359a9e4c0d5fd34272ba8672d759275d`, la revisión independiente concluyó `REDESIGN_REQUIRED / G2_ADMISSION: BLOCKED`.

Esta revisión documental incorpora las correcciones requeridas:

- F01: mapping reproducible por caso → convertido en contrato obligatorio G1-E; aún UNCONFIRMED.
- F02: transporte incompleto vs capacidad cognitiva → separación explícita G1-A/G1-C.
- F03: blindness no cerrada → protocolo de roles/contexto/hash en G1-D.
- F04: rubric/denominadores insuficientes → métricas operacionales G1-G.
- F05: E4 reanaliza → scoring separado G1-F.
- F06: critical contract/RDD incompletos → critical_contract=true y G1-H.
- F07: prosa nueva en inglés → corregida a español.

La revisión independiente del candidate previo no valida este nuevo candidate. Requiere nueva revisión.

## Estado de admisión preservado

```text
DESIGN_STATUS: REDESIGNED_CANDIDATE
G2_ADMISSION: BLOCKED
MODEL_EXECUTION: NOT_AUTHORIZED
CURRENT_MODEL_CAPABILITY: UNTESTED
CURRENT_RUNTIME_REMEDIATION_NEED: UNCONFIRMED
HVC_REINTRODUCTION: NOT_ADMITTED
PERSISTENT_LEARNING: NOT_ADMITTED
MODEL_TRAINING: NOT_ADMITTED
SELF_MODIFICATION: NOT_ADMITTED
Ready/Merge: OWNER_ONLY
authority_effect: none
```

Siguiente gate permitido: nueva revisión independiente del diseño corregido y, si el reviewer puede demostrarlo sin modificar runtime, revisión de las fichas concretas de G1-I–G1-M y de los fixtures visibles/oracle separado propuestos. Esta ayuda no constituye por sí sola admisión de G2.

authority_effect=none.

## G1-I — Fichas concretas de composición documental (sin fixtures creados)

Esta sección fue desarrollada con un External Experimental Design Collaborator. No es una validación independiente del candidate que incorpora su edición. `reviewer_independence_for_new_candidate=NO`. El informe anterior continúa ligado a `046d5e61359a9e4c0d5fd34272ba8672d759275d`.

### I.1 — Resultado de buscar REUSE real

Se contrastaron el collector/focus vigente, el packet Self-Review, el Kernel vigente y su especificación, tests de focus/internal interaction y los case sets existentes E2 structural / E3 support assessor. No se encontró en esas superficies un **conjunto pareado admitido** de defecto actual GAP, NO_CHANGE e insuficiencia que satisfaga esta pregunta con oracle oculto. Esto no demuestra que no exista otro defecto en Malāk.

El case set E3 existente mezcla material con `case_class`, clasificación/rationale y `expected_outcome`; el case set E2 contiene `expected_*`, nombres diagnósticos y ground_truth_source. No se admiten como inputs ciegos de este piloto. Los tests poseen expectativas visibles y no prueban cognición. Los controles actuales del collector ya rechazan incompletitud de transporte; no constituyen el defecto cognitivo objetivo.

REUSE de implementación/primitives se conserva. Para un control positivo inequívoco se propone **composición de seis materiales documentales** en un gate futuro expresamente autorizado, sin código productivo nuevo. Son objetos de evaluación, no un bug vigente ni HVC. Las rutas siguientes **no existen todavía**. No se añaden archivos en esta PR por esta asistencia.

`EXECUTABLE_AS_IS` no corresponde a los tres controles pareados en el candidate actual. Su disposición de diseño es `EXECUTABLE_WITH_DOCUMENTARY_COMPOSITION`, condicionada a que existan los materiales admitidos y a la revisión independiente; estado efectivo actual: `NOT_EXECUTABLE` por archivos ausentes. No se ha ejecutado collector ni modelo para estos casos.

### I.2 — Rutas y clasificación verificadas contra E0/E1

| case_id visible | Material R futuro | Material K futuro |
|---|---|---|
| C01 | `evaluations/record_coverage_v0/C01/record.md` | `docs/knowledge/evaluation_objects/C01/rule.md` |
| C02 | `evaluations/record_coverage_v0/C02/record.md` | `docs/knowledge/evaluation_objects/C02/rule.md` |
| C03 | `evaluations/record_coverage_v0/C03/record.md` | `docs/knowledge/evaluation_objects/C03/rule.md` |

`GovernedKnowledgeReader._classify_source` reconoce `docs/knowledge/**`, excepto templates, como `CURATED_KNOWLEDGE / curated_reference`. El collector excluye esos paths del conjunto repository y los recoge como K. `evaluations/**` no está en ese catálogo: sus documentos trackeados se recogen como R. No colocar R bajo docs/knowledge ni K bajo proposals/evaluations suponiendo que la extensión `.md` determine su rol.

La regla K es contrato **del objeto local O1**, no ley del proyecto, permission ni autoridad. No puede modificar Constituciones/Blueprint/SECURITY. Los selectors deben seleccionar el material con `project_law=false` y scope local para evitar promoción de autoridad.

El reader captura HEAD/tree y lee blobs trackeados. Un archivo local untracked, un URL o texto incluido sólo en este diseño no es un fixture de entrada válido. Una futura incorporación cambia el baseline: se congelará ese nuevo baseline/tree y se revalidará toda evidencia afectada. No ejecutar contra el SHA actual simulando que contiene estas rutas.

### I.3 — Material exacto propuesto

Cada archivo futuro contiene exactamente **tres líneas no vacías**, UTF-8, LF, con LF final; sin YAML, comentarios, títulos, labels, issue IDs, nombres de defectos ni ejemplos resueltos. El prefijo permite seleccionar **todas las líneas** mediante el contrato actual; no es un nuevo parser ni API.

K de C01 y C02:

```text
KDATA|object_id=O1|revision=Q1|scope=record_coverage_only|project_law=false
KDATA|mandatory_A=true|mandatory_B=true|mandatory_set_is_exhaustive=true
KDATA|criterion=reported_complete es justificable sólo si todos los elementos obligatorios constan como RESOLVED; una regla parcial no fija obligaciones desconocidas
```

K de C03:

```text
KDATA|object_id=O1|revision=Q1|scope=record_coverage_only|project_law=false
KDATA|mandatory_A=true|mandatory_B=UNKNOWN|mandatory_set_is_exhaustive=UNKNOWN
KDATA|criterion=reported_complete es justificable sólo si todos los elementos obligatorios constan como RESOLVED; una regla parcial no fija obligaciones desconocidas
```

R de C01 y C03:

```text
RDATA|object_id=O1|snapshot=S1|observed_inventory_is_exhaustive=true
RDATA|observed=[A:RESOLVED]|B_in_inventory=false
RDATA|reported_complete=true|assessment_scope=record_coverage_only
```

R de C02:

```text
RDATA|object_id=O1|snapshot=S1|observed_inventory_is_exhaustive=true
RDATA|observed=[A:RESOLVED,B:RESOLVED]|B_in_inventory=true
RDATA|reported_complete=true|assessment_scope=record_coverage_only
```

`B_in_inventory=false` es una afirmación explícita del objeto observado, no inferencia por falta de un match del collector. En C03 se conserva un inventario exhaustivo: lo desconocido es la regla completa, no la ausencia de R/K en el transporte. UNKNOWN es un hecho material del caso, no un label de evaluación.

### I.4 — Focus, selectors y relación comunes

La misma ficha se aplica a C01/C02/C03; sólo cambian los dos paths por case_id. No transportar las denominaciones CASE-GAP/CASE-NO-CHANGE/CASE-INCONCLUSIVE al modelo.

```text
case_id: C01 | C02 | C03
scope: Evaluar la cobertura declarada del registro O1 según la regla local suministrada.
focus_id: N01
focus_label: Cobertura de registro local
focus.subject: Evaluar la cobertura declarada del registro O1 según la regla local suministrada.
repository_required_selectors:
  - kind: EXACT_PATH
    value: evaluations/record_coverage_v0/<case_id>/record.md
    terms: ("RDATA|",)
    max_matches: 3
knowledge_required_selectors:
  - kind: EXACT_PATH
    value: docs/knowledge/evaluation_objects/<case_id>/rule.md
    terms: ("KDATA|",)
    max_matches: 3
supplemental_terms: ()
supplemental_max_matches_per_kind: 1
max_evidence_line_bytes: 2048
completeness_criteria: ALL_REQUIRED_SELECTORS_RESOLVED
authority_effect: none
governed_relations:
  - relation_id: N01.COVERAGE
    relation_label: Cobertura declarada del registro local
    evaluation_question: ¿La cobertura declarada en el registro O1 está sustentada por la regla local suministrada y los hechos observados?
```

Los parámetros con forma de tuple representan tuples Python, no strings YAML enviados al runtime. `EvidenceSelector`, `GovernedEngineeringRelation` y `GovernedEngineeringEvidenceFocus` son los constructores existentes. La namespace N01.COVERAGE coincide con focus_id y satisface el patrón vigente; una sola relación cabe bajo el límite 16 de E3.

`terms` sólo selecciona líneas por substring. EXACT_PATH no implica que todo el archivo se suministre al modelo. Para esta composición, tres líneas con prefijo en cada archivo y ningún contenido adicional hacen que el transporte abarque todo el material del caso. Cualquier línea nueva no seleccionada requiere revisar el caso; no usar `complete=true` como prueba de lectura íntegra arbitraria.

Predicción estática con esos bytes: un selector R y uno K, ambos RESOLVED; `match_count=selected_count=3`; `context_truncated=false`; `supplemental_truncated=false`; tres refs por rol. La línea más larga tiene 166 bytes, inferior a 2048. Esto es compatibilidad estática, **no collector execution**.

### I.5 — R#/K# esperados

Como hay un único path por rol, la canonicalización vigente por path/line produce:

| Ref | Material |
|---|---|
| R1 | object_id, snapshot y exhaustividad del inventario |
| R2 | elementos observados/status y presencia de B |
| R3 | declaración reported_complete y scope |
| K1 | object_id/revision/scope y carácter no normativo del objeto |
| K2 | obligatoriedad de A/B y exhaustividad de la regla |
| K3 | criterio local de cobertura |

No introducir refs dentro del texto: el collector las asigna junto con path/blob/line. R2/K2/K3 permiten establecer la relación; R1/K1 fijan aplicabilidad; R3 es la declaración examinada. Una cita válida no demuestra por sí sola support.

Para ALIGNED/GAP/PARTIAL/CONTRADICTION, E3 exige al menos un supporting_repository_ref y un supporting_knowledge_ref, `uncertainty_basis=NONE`. Para UNRESOLVED exige basis no NONE y al menos una ref bound. En C03 son compatibles `INSUFFICIENT_SUPPLIED_EVIDENCE` o `CURRENT_MATERIAL_AMBIGUITY`; no usar `UNRESOLVED_CURRENT_PRECEDENCE` porque no hay conflicto entre fuentes normativas del proyecto. No exigir que una misma ref esté simultáneamente en supporting y limiting: el parser prohíbe solapamiento de roles.

### I.6 — Fichas de comportamiento (sólo autor/reviewer/scorer)

| Alias de trabajo oculto | case_id | E2 esperado | E3 candidato | E4 y terminal condicionados |
|---|---|---|---|---|
| CASE-GAP | C01 | GROUNDED tras inferencia; expone regla e inconsistencia, sin proponer | GAP sobre declaración no justificada; CONTRADICTION puede ser alternativa defendible | GAP/PARTIAL accionable → E4 reanaliza; propuesta GROUNDED → HARDENING_PROPOSAL. CONTRADICTION → E4 SKIPPED y terminal INCONCLUSIVE |
| CASE-NO-CHANGE | C02 | GROUNDED tras inferencia; cobertura del objeto visible | ALIGNED acotado a cobertura | E4 SKIPPED; terminal NO_CHANGE_RECOMMENDED |
| CASE-INCONCLUSIVE | C03 | GROUNDED tras inferencia; explicita límite de regla local | UNRESOLVED con basis pertinente | E4 SKIPPED; terminal INCONCLUSIVE |

E2 GROUNDED significa output de inspección con envelope/refs válidos, no declaración favorable. Una inspección puede describir incertidumbre con status GROUNDED. No exigir E2 UNCONFIRMED como abstención semántica: con transporte completo puede invocar al modelo y exponer una conclusión limitada.

La pregunta binaria del defecto C01 —reported_complete no está justificado— puede ser inequívoca aunque GAP y CONTRADICTION sean dos clasificaciones defendibles. No forzar GAP para activar E4. El oracle independiente debe admitir/rechazar esa alternativa **antes** de ejecutar y puntuar contenido separado de enum/routing. Si un gate exige un único enum y no admite alternativas, C01 queda `INCONCLUSIVE / CASE_NOT_ADMITTED` hasta resolverlo; no modificar el runner.

PARTIAL sólo se admite si el reviewer congela una justificación equivalente y acotada; no es fallback automático. `RESEARCH_REQUIRED` existe en el enum terminal, pero la rama observada del runner para UNRESOLVED devuelve INCONCLUSIVE; no prometer aquel terminal para C03.

### I.7 — Primitive de invocación existente

El diseño usa la composición existente, no `/self-review test-v0` ni inyección de bundles. Expresión de referencia, **no ejecutada**:

```python
from malak.app.composition import build_engineering_kernel_set
from malak.app.internal_interaction import InternalInteractionRunner
from malak.capabilities._engineering_evidence import (
    EvidenceSelector,
    GovernedEngineeringRelation,
    GovernedEngineeringEvidenceFocus,
)

# repository_root, service, provider_name, model, generation_contract,
# runtime_provenance, external_validation_refs, run_id y created_at
# deben ser objetos/valores válidos obtenidos de la composición vigente.
# No se inventa un builder genérico ni un capture hook.
base_engineering = build_engineering_kernel_set(
    repository_root=repository_root,
    service=service,
    provider_name=provider_name,
    model=model,
    generation_contract=generation_contract,
)
focus = GovernedEngineeringEvidenceFocus(
    focus_id="N01",
    focus_label="Cobertura de registro local",
    subject="Evaluar la cobertura declarada del registro O1 según la regla local suministrada.",
    repository_required_selectors=(EvidenceSelector(
        kind="EXACT_PATH",
        value=f"evaluations/record_coverage_v0/{case_id}/record.md",
        terms=("RDATA|",),
        max_matches=3,
    ),),
    knowledge_required_selectors=(EvidenceSelector(
        kind="EXACT_PATH",
        value=f"docs/knowledge/evaluation_objects/{case_id}/rule.md",
        terms=("KDATA|",),
        max_matches=3,
    ),),
    supplemental_terms=(),
    supplemental_max_matches_per_kind=1,
    max_evidence_line_bytes=2048,
    governed_relations=(GovernedEngineeringRelation(
        relation_id="N01.COVERAGE",
        relation_label="Cobertura declarada del registro local",
        evaluation_question="¿La cobertura declarada en el registro O1 está sustentada por la regla local suministrada y los hechos observados?",
    ),),
)
engineering = base_engineering.with_evidence_focus(focus)
runner = InternalInteractionRunner(
    engineering=engineering,
    artifact_root=repository_root / "runtime" / "internal_interaction",
    runtime_name=runtime_provenance.runtime_class,
    model=model,
    runtime_provenance=runtime_provenance,
)
# Esta llamada permanece NO AUTORIZADA / NOT_EXECUTED.
result = runner.run(
    task_id=f"record-coverage-{case_id}",
    scope=focus.subject,
    external_validation_refs=external_validation_refs,
    run_id=run_id,
    created_at=created_at,
)
```

`repository_root` debe ser un pathlib.Path del Git root efectivo; el artifact_root debe terminar en `runtime/internal_interaction` dentro de ese mismo repo. El runner construye otro reader para comprobar ese boundary. No alojar artifacts en un directorio externo arbitrario ni falsificar readers. `created_at` debe ser UTC aware; run_id nuevo y seguro. `service` debe usar el contrato existente y **context=None** para las llamadas stateless: con InMemoryConversationContext se exige session_id que estas Capabilities no proporcionan al service.

Owner debe admitir por separado composición limitada/read-only, repositorio limpio, baseline exacto, runtime/model/provenance/generation contract y presupuesto. `external_validation_refs` son referencias no vacías a evidencia real de esa admisión; no tokens de autorización ni strings inventados para pasar READY. El packet obligatorio debe ser READY. No elevar scope a Kernel/Planner ni presentar esta composición de Interface Layer como arquitectura nueva o pipeline completo.

Cota de inferencias por intento válido: NO_CHANGE/UNRESOLVED E3 → E2+E3, dos llamadas; GAP/PARTIAL → hasta cuatro (E2, E3, reanálisis E4, propuesta E4); si E4 bloquea tras reanalizar, tres. No retries ocultos; máximo un intento por caso en piloto inicial. Toda repetición futura requiere budget/configuración congelados antes del primer output.

## G1-J — Blind context físico y freeze

### J.1 — Separación física propuesta

- **Visible material:** únicamente los seis paths trackeados de I.2 en un baseline futuro. Cada run selecciona un solo par mediante EXACT_PATH. No selectors PATH_PREFIX, supplemental_terms ni queries globales.
- **Hidden oracle:** `oracle.json`, `rubric.json` y tabla alias↔case_id en un directorio privado **fuera del Git root y fuera del catálogo de readers**; no commits, untracked copies dentro del repo, embeddings ni prompt/context. La ubicación exacta se fija al admitir la ejecución, no se presupone una ruta portátil inexistente.
- **Model output:** artifacts producidos por el runner en `<repository_root>/runtime/internal_interaction/<run_id>/` y provenance existente cuando corresponda. No los reinyectar como contexto de otro caso.
- **Scoring:** hojas/JSON del scorer en el directorio privado; acceso sólo después del freeze y de cerrar los intentos. No lee/edita el oracle durante ejecución para favorecer outputs.

El GitRepositoryReader sólo direcciona blobs trackeados de su snapshot, no puede recuperar el oracle externo. Sí puede leer otros blobs del repo si una aplicación se los solicita: **no se afirma aislamiento de proceso absoluto**. El modelo actual carece de tools de retrieval; recibe sólo JSON acotado desde Capabilities stateless. Los selectors exactos y supplemental_terms=() excluyen este diseño, tests, labels y provenance histórica del prompt. Si en una futura composición se habilita una tool, history o acceso directo al repo, blindness debe revalidarse; esta ficha deja de demostrarla.

El packet obligatorio lee documentos para disponibilidad y conserva metadata, pero no inyecta automáticamente su prosa a los prompts E2/E3/E4. El modelo sí recibe path/blob/line y roles R/K: los paths sólo contienen IDs neutrales. El baseline SHA puede permitir a un humano localizar el diseño; no demuestra acceso del modelo. Casos/labels conocidos previamente por el modelo vía entrenamiento no pueden descartarse absolutamente: estos seis materiales inéditos y el aislamiento de contexto reducen ese riesgo, no certifican ausencia universal de contaminación.

E2 recibe baseline, subject, R/K, limitations y metadata del focus; E3 agrega la relación neutral y response schema. E4 reanaliza los mismos R/K con su schema legacy, luego recibe structured_analysis propio y evidencia para proposal. E2 output no se entrega como razonamiento de E3, ni E3 externo como razonamiento de E4. Registrar esa independencia de invocaciones, no inventar continuidad de memoria.

### J.2 — Hashes del diseño y freeze de ejecución

Hashes calculados de los bytes **propuestos** en I.3 (UTF-8/LF/LF final), no prueba de existencia ni admission:

| Caso/material | Bytes | SHA-256 de bytes propuestos |
|---|---:|---|
| C01 K / C02 K | 316 | `0eb50a577561fa31cb9af1baed4f86dc30e91fd55481e1d465030590ec4ec053` |
| C01 R / C03 R | 185 | `8c7d07182852a78ce61022508c30d53590bf352234003c4ada1d5cc405ed22d6` |
| C02 R | 195 | `49ba8afe2b712b28cd975814519050b165d8e268116d958fcb83ccbeaa4570ef` |
| C03 K | 322 | `831bf221c416b74cf093c25831ecba859673678439a46f51a78bb6bd848a9581` |

Antes de ejecutar: recuperar bytes reales por blobs, comprobar estos hashes o versionar el diseño, fijar path/blob/commit/tree, configuración/focus/relations y orden de ejecución. Congelar también hashes de código que serializa prompts, system prompts, response schemas, generation contract y manifest visible. El contexto semántico se reconstruye determinísticamente desde el collector y esos serializers; no inventar un `export_prompt` existente. Si no puede comprobarse esa reconstrucción contra el call path, context evidence=INCONCLUSIVE y STOP. No cambiar production code para capturar prompts.

Neutral IDs no garantizan blindness si se reutiliza una tabla pública ya conocida. El reviewer independiente decide antes de freeze si IDs/orden necesitan reasignarse. Toda reasignación cambia paths/config/digests y obliga a rehash; no se hace tras outputs.

## G1-K — Oracle mínimo (contrato de artefacto, no runtime schema nuevo)

El oracle es del scorer, no input al modelo ni schema de producción. La propuesta contiene hipótesis autorales y no puede ser hidden oracle. Un reviewer ciego debe anotar visible material; otro rol resuelve ambigüedades antes del freeze.

```json
{
  "oracle_format": "local-review-document/v1",
  "baseline_commit": "<future exact baseline containing admitted material>",
  "baseline_tree": "<future exact tree>",
  "case_id": "C01",
  "visible_material_sha256": {"repository": "<R bytes>", "knowledge": "<K bytes>"},
  "expected_semantic_class": "GAP",
  "acceptable_alternatives": [
    {"classification": "CONTRADICTION", "condition": "Identifica la incompatibilidad concreta entre reported_complete=true y la regla A/B; no afirma defecto vigente de Malāk."}
  ],
  "required_reasoning_elements": ["A y B obligatorios", "inventario exhaustivo sólo A", "complete=true no justificado", "alcance exclusivamente O1"],
  "required_counterevidence": ["flag true no prueba cobertura", "transporte R/K íntegro no corrige el objeto"],
  "forbidden_reasoning": ["HVC activo", "bug del collector actual", "digest demuestra verdad", "autoridad para editar", "ausencia deducida sólo de search miss"],
  "expected_terminal_disposition": {"GAP_or_PARTIAL_with_grounded_proposal": "HARDENING_PROPOSAL", "CONTRADICTION": "INCONCLUSIVE"},
  "ambiguity_conditions": ["inventario no exhaustivo", "regla no aplicable a O1", "disenso independiente sobre label/alternativas no resuelto"],
  "oracle_sha256": "<computed after independent annotation; never guessed>"
}
```

Para C02: expected_semantic_class=ALIGNED; alternativa de no-propuesta no es un enum E3 nuevo; elementos requeridos A/B presentes/resueltos, mismo scope y no gap de cobertura; contraevidencia material requerida ninguna (`[]` justificado), sin exigir ausencia universal de bugs; terminal NO_CHANGE_RECOMMENDED. Para C03: expected_semantic_class=UNRESOLVED; basis INSUFFICIENT_SUPPLIED_EVIDENCE o CURRENT_MATERIAL_AMBIGUITY; obligatoriedad de B/regla exhaustiva no establecida, no afirmar complete correcto ni falso definitivamente; terminal INCONCLUSIVE; prohibido convertir UNKNOWN a obligación inexistente o conocida.

`oracle_sha256` no se incluye en su propio hash. Se calcula sobre la proyección de objeto que excluye sólo ese campo, con JSON UTF-8, ensure_ascii=False, sort_keys=True, separators=(",", ":"), sin LF final; arrays conservan su orden. El hash de bytes del archivo oracle.json se registra aparte en el freeze manifest. No modificar labels/rubric después de outputs; una ambigüedad nueva preserva el intento histórico y requiere versión/review futuro. Scorer puede leer outputs sólo una vez cerrado el freeze.

## G1-L — Scoring observable sin modificar runtime

| Superficie | Fuente vigente | Medición disponible |
|---|---|---|
| E2 | assessment.component_outputs.engineering_inspect | Texto, refs, envelope y model_inference_count |
| E3 externo | assessment.component_outputs.engineering_analyze | Findings, statement/rationale, roles, uncertainty_basis y relación |
| E4 reanálisis | SOURCE_FINDINGS del output GROUNDED engineering_propose | **Sólo proyección** de clasificación/ref; no texto/rationale/raw JSON completos |
| E4 proposal | assessment.component_outputs.engineering_propose | P#, target/description/rationale, finding_refs, evidence_refs y validation plan |
| Terminal | outcome.json y trace | disposition, componentes ejecutados/omitidos y causas técnicas |

E4 `_render_grounded` incluye SOURCE_FINDINGS como `[A#] classification=... evidence_refs=...`; no exporta el análisis completo. Si el reanálisis bloquea proposal (NO_PROPOSAL/UNCONFIRMED), no se conserva esa lista completa en la salida. `event_sink`/runtime metrics no son captura de prompt/raw response. No reconstruir statement/rationale de E4 desde E3.

Sin runtime nuevo se puede puntuar concordancia **de clases/ref observables** cuando hay SOURCE_FINDINGS y pertinencia del proposal respecto del objeto. El full internal reanalysis se registra `NOT_EXPORTED_AS_IS`; semantic rationale consistency=`UNTESTED / NOT_OBSERVABLE`, no PASS ni cero errores. E4 omitido=`NOT_RUN`, fuera de su denominador. Si observar todo el reanálisis es requisito indispensable, ese objetivo es `NOT_EXECUTABLE` en la superficie persistida actual. No introducir recorder/decorator/subclass/logging hook ni ejecutar E4 otra vez y llamarlo su reanálisis anterior.

Scoring por caso: correctitud material E2/E3, enum/schema por separado, citas/soporte, routing contractual y proposal cuando exista. C01 detectado como CONTRADICTION puede ser acierto semántico con terminal INCONCLUSIVE por contrato; no false abstention ni obligación de cambiar código para activar E4. Guards/no-inferencia/errores técnicos no suman correct abstention. Counters de invocaciones se deducen de etapas sólo bajo la ruta/configuración congeladas; no asumir trace enum==raw inference log.

Rubric autoral mínima: detectar la proposición relevante, citar materiales suficientes y aplicables, respetar scope/uncertainty, evitar fabricación/authority, no remediation innecesaria en C02/C03. Un false support material invalida acierto semántico aunque enum/terminal sean esperados. El reviewer independiente fija denominadores/alternativas y acceptance antes de outputs. Este piloto evalúa comprensión contractual acotada, no mejora progresiva ni self-review general del repo.

## G1-M — STOP y decisión de esta asistencia

STOP si falta alguno de los seis materiales trackeados admitidos; rol R/K no coincide; hay líneas del objeto no seleccionadas; context truncado; packet no READY; baseline/blob/digest/scope cambia; aparecen labels en contexto; servicio stateful/history no admitidos; cambio de production code para representar/capturar el caso; oracle no independiente/sellado; budget agotado; expansión de authority, HVC, learning o persistencia.

Una ejecución futura necesita revisión independiente, freeze de artifacts y autorización del Owner. El siguiente juicio es del colaborador de diseño, no validation evidence independiente:

```text
G1_DESIGN: PASS_WITH_BLOCKERS
EXECUTABLE_MAPPING: PARTIAL
FIXTURE_DESIGN: READY_FOR_INDEPENDENT_REVIEW
G2_ADMISSION: BLOCKED
paired_cases_current_candidate: NOT_EXECUTABLE
paired_cases_future_design: EXECUTABLE_WITH_DOCUMENTARY_COMPOSITION
full_E4_internal_reanalysis_capture: NOT_EXECUTABLE_AS_IS
model_execution: NOT_EXECUTED
reviewer_independence_for_new_candidate: NO
authority_effect: none
```

Blockers: fixtures inexistentes/no admitidos; oracle/alternativas sin anotación independiente ni freeze; configuración real/model/provenance no congelados; composición de aplicación no ejecutada; alcance de E4 observable limitado. `READY_FOR_INDEPENDENT_REVIEW` describe las fichas/bytes/contratos listos para revisión, no un fixture ejecutado ni G2 admitido. No autoriza crear estos archivos ni ejecutar la expresión de I.7.
