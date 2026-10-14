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

Estado: `UNCONFIRMED / NOT_EXECUTABLE UNTIL DEMONSTRATED`.

No afirmar que `/self-review test-v0` es un runner universal: actualmente fija su propio TASK_ID/FOCUS/SCOPE.

Si el caso exige cambiar production code sólo para hacerlo ejecutable, mantener `NOT_EXECUTABLE` y STOP salvo nueva admisión independiente.

## G1-F — Semántica de E3/E4

E4 no consume directamente el finding producido por la llamada previa de E3. `engineering_propose.py` ejecuta un nuevo `run_engineering_analysis` antes de generar propuesta.

Por lo tanto, el piloto debe registrar y puntuar por separado:

1. finding/análisis E3;
2. análisis interno ejecutado por E4;
3. propuesta E4;
4. concordancia E3↔E4;
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

Stage 1 Design Check: requerido antes de admitir G2 y debe validar necesidad, reuse, executable mapping, oracle/blindness y métricas.

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

## Decisión G1

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

Siguiente gate permitido: nueva revisión independiente del diseño corregido y, si el reviewer puede demostrarlo sin modificar runtime, propuesta concreta de mapping ejecutable/fixtures visibles+oracle separado. Esa ayuda no constituye por sí sola admisión de G2.

authority_effect=none.
