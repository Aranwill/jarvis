---
title: "Malāk — Practical Governed Self-Review Evaluation G0/G1"
status: draft
issue: 319
baseline_commit: f638a2070ddd3b358bcc32f2827b2f3766497250
baseline_tree: 8a45b51904e8a99f22e17cd6e04cff348c47079b
authority: non_normative_proposal
risk_candidate: 2
language: es
---

# #319 — Practical Governed Self-Review Evaluation — G0/G1

## G0 — Alcance y admission

Objetivo: medir la utilidad de la auto-revisión gobernada actual sin exigir determinismo semántico del LLM. Solo diseño documental. No se autoriza ejecución de modelos, cambios de código/tests/runtime, aprendizaje persistente, HVC, Kernel/Planner, soporte de finalización ni nuevas capas.

Baseline exacto: `f638a2070ddd3b358bcc32f2827b2f3766497250` / tree `8a45b51904e8a99f22e17cd6e04cff348c47079b`.

Inventario recursivo: 387 blobs descubiertos, 387 clasificados, 0 omitidos silenciosamente, tree no truncado. Inventario no significa lectura íntegra. La profundidad fue proporcional a la pregunta, con foco en AGENTS, Constituciones, Blueprint, Security, roadmap/ideas/concepts, método, protocolo, checklist, ADRs y flujo E0–E4.

Preflight: ADMITTED para diseño documental; no es autorización para implementación. Owner conserva Ready/Merge.

## Fuentes, fronteras y reuse

- `AGENTS.md`: jerarquía, inventario, Minimum Review Set, Construction Preflight.
- `SECURITY.md`: política protegida y límites; sus derivados se clasifican por rol.
- `ROADMAP.md`: navegación no normativa. `docs/project/implementation_roadmap.md`: planificación derivada canónica. `docs/project/roadmap.md`: legacy.
- `documents/projects/jarvis/ideas.md`, `docs/project/concepts/**`, Research Horizon: intención, no autorización.
- `docs/development/engineering_method.md`, `malak_construction_protocol.md`, `malak_construction_preflight.md`, `development_checklist.md`: método y admisión.
- `GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md`: inputs mínimos y resultados válidos, incluyendo NO_CHANGE.
- `src/malak/services/self_review_evidence.py`: packet de disponibilidad y catálogo; READY no prueba consumo ni apoyo semántico.
- `src/malak/capabilities/_engineering_evidence.py`, `engineering_inspect.py`, `engineering_analyze.py`, `engineering_propose.py`: evidencia focalizada, R#/K#, path/blob/line, findings, contraevidencia y propuestas referenciadas.
- `src/malak/app/internal_interaction.py`: terminal dispositions, trace y artifacts.
- Tests de packet, focus, E2/E3/E4 e internal interaction: contratos existentes, no prueba de calidad real con modelo.

REUSE de mecanismos actuales. ADAPT/COMPOSE/NEW: NOT_ADMITTED sin déficit demostrado. No añadir `ROADMAP.md` como fuente obligatoria por su mera presencia en AGENTS. No crear otra capa de provenance.

## G1 — Casos de referencia congelados antes de ejecutar

### A — CANDIDATE_GAP (UNCONFIRMED; no es TRUE_GAP admitido)

Pregunta: ¿el packet obligatorio para Self-Review contiene todos los insumos que son materialmente necesarios para una revisión de admisión/implementación conforme al AGENTS vigente?

Observación inicial: `REQUIRED_SELF_REVIEW_SOURCES` no enumera `docs/development/engineering_method.md` ni `docs/development/malak_construction_preflight.md`. No se presume que ello sea un bug: puede tratarse de separación deliberada entre packet de disponibilidad y lectura focalizada. Para calificar GAP, debe demostrarse una omisión material en el flujo completo, no sólo diferencia entre listas.

Expected: **UNCONFIRMED / NOT_ADMITTED como TRUE_GAP** hasta demostrar un defecto material real y fijar ground truth independiente. `GAP` sólo si la ausencia causa una decisión insuficientemente sustentada; `NO_CHANGE` si el flujo existente consume las fuentes por otra vía; `INCONCLUSIVE` si no puede comprobarse. La ausencia en el packet no demuestra por sí sola incumplimiento del Construction Preflight, que tiene obligaciones propias. Si no se verifica el gap, sustituir el caso por uno real antes de ejecutar, mediante revisión independiente y nueva congelación; no redefinir resultados post hoc.

### B — NO_CHANGE

Pregunta: ¿debe añadirse `ROADMAP.md` a `REQUIRED_SELF_REVIEW_SOURCES` sólo porque AGENTS lo clasifica explícitamente?

Expected: NO_CHANGE_RECOMMENDED, si el implementation roadmap ya provee el contenido material y el entrypoint no añade evidencia necesaria. Debe citar roles y no convertir navegación en autoridad.

### C — AMBIGUOUS / EXTERNAL_DEPENDENCY

Pregunta: ¿puede demostrarse enforcement actual de integración en GitHub usando únicamente blobs del repositorio?

Expected: no. El estado de branch protection/rulesets es externo y mutable; una conclusión favorable basada sólo en el árbol es inválida. Admitir evidencia externa actual y autorizada si existe; de otro modo `INCONCLUSIVE` / `RESEARCH_REQUIRED`.

## G1 — Revisión contractual pendiente de admisión

Los tres casos son preguntas de investigación, no automáticamente fixtures ejecutables. Antes de G2, demostrar para cada caso un mapping concreto a la interfaz actual (`scope`, focus/selectors, evidencia R#/K#, expected terminal disposition), y disponibilidad de evidencia reproducible. C requiere un fixture con ausencia controlada de estado externo, sin presentar GitHub API como parte del reader del repositorio. Si no se pueden mapear, `NOT_EXECUTABLE` y rediseño documental antes de admisión. Un evaluador independiente debe fijar y sellar ground truth antes de cualquier output de modelo.

## Protocolo experimental futuro (NO AUTORIZADO EN ESTE GATE)

1. Congelar SHA/tree, pregunta, alcance, fuentes relevantes, counterevidence y ground truth independiente de los outputs.
2. Ejecutar la misma interfaz existente, sin adaptar prompts/criterios a posteriori ni filtrar sólo resultados favorables.
3. Guardar artifacts actuales: evidence.json, assessment.json, trace.jsonl, diagnostics.jsonl, outcome.json, manifest y attestation; registrar runtime/model/provenance cuando aplique.
4. Auditar disponibilidad vs consumo real vs soporte de cada claim. Una referencia válida demuestra identidad/provenance estructural, no verdad semántica.
5. Comparar contra baseline humano, incluyendo resultados de NO_CHANGE y abstención; repetir con variabilidad declarada si se usa un modelo probabilístico.
6. STOP ante baseline distinto, fuente obligatoria ilegible, evidence binding roto, authority_effect != none, ground truth no independiente, resultado que implique self-authorization o expansión no aprobada.

## Métricas y aceptación

Medir por caso: grounded-claim rate, false favorable/support rate, counterevidence recall, detección de contradicción, false GAP, abstención correcta/innecesaria, calidad de propuesta, coste/latencia y reproducibilidad. Registrar denominadores y todos los intentos, no sólo aciertos.

No declarar PASS global a partir de tres casos ilustrativos. Tres casos son piloto discriminante; una afirmación de mejora requiere un conjunto ampliado, criterio de éxito predeclarado y comparación con baseline. Un `NO_CHANGE` correcto cuenta como éxito; UNKNOWN apropiado también.

## RDD / Design 4R / decisión

Risk candidate 2 para diseño de evaluación. RDD Stage 1: diseño sujeto a validación independiente; Stage 2: OPTIONAL sólo con admission explícita futura. RED/GREEN y runtime: NOT_AUTHORIZED.

4R author-side: Risk — controles/STOP definidos; Readability — casos y expectativas separados; Reliability — ground truth previo y SHA exacto; Resilience — abstención y no-change válidos. Independiente: PENDING.

Decisión G1: `DESIGN_ONLY / NOT_EXECUTED / NOT_QUALIFIED`. No se solicita implementación. Siguiente gate posible: validación independiente de este diseño y aprobación Owner para piloto read-only, con controles proporcionales.

authority_effect=none.
