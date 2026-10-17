---
title: "Malāk — E2 Output Contract Alignment después de C01 Attempt 1"
status: bounded_correction_pending_independent_fix_validation
authority: non_normative_proposal
language: es
date: 2026-10-16
repository: Aranwill/jarvis
baseline_commit: 8c401b2bed1c114efadba3777c7662f45e56e8c6
baseline_tree: 573c9b3e5cc49052863d9fb30b69d4e4d2322bfd
issues: [319, 327, 330]
critical_contract: true
risk_class: 3
implementation_status: NOT_IMPLEMENTED
model_execution_authorized: false
authority_effect: none
---

# E2 Output Contract Alignment — G0/G1

## 1. Resultado y frontera

Esta unidad nace de evidencia runtime real del piloto gobernado de self-review.
C01 Attempt 1 quedó consumido y E2 terminó en rechazo fail-closed:

```text
E2=FAILED
E3=NOT_ATTEMPTED
E4=NOT_ATTEMPTED
retry=FORBIDDEN

exception_type=RuntimeError
exception_message=assertion text contains reserved evidence or analysis ref token
```

El finding no es que Malāk haya aceptado output inválido. El parser lo rechazó
correctamente. El finding es que el contrato que guía/constriñe la generación no
hace visible con suficiente fuerza una regla que el parser exige después:

```text
generation-facing contract
!=
full deterministic acceptance contract
```

Esta PR-A será sólo Design / Documentation. No autoriza RED, GREEN, reintento de
C01, C02/C03, model calls, Ready o Merge.

## 2. Candidate Identity y evidencia del incidente

```text
repository=Aranwill/jarvis
baseline_commit=8c401b2bed1c114efadba3777c7662f45e56e8c6
baseline_tree=573c9b3e5cc49052863d9fb30b69d4e4d2322bfd

C01_ATTEMPT=CONSUMED
failure.json.sha256=08CAACA9B7565B51C0C9975455F3DB297F1AD7E40D234F32F2CC9AD57564EEDB
preflight.json.sha256=1713C9B50BC4423838F26589C440D240D054CD1EBC883EA5A337D88ED6FEB165
```

Registro gobernado:
- #327 contiene Owner G2 y el incident record.
- #330 contiene la unidad de corrección.
- C01 no se reejecuta bajo el G2 consumido.
- C02 y C03 permanecen HOLD.

El JSON bruto rechazado de C01 no fue persistido por el path vigente y no se
reconstruye ni se inventa. Sólo es evidencia soportada que algún
`assertion.text` contenía un token reservado según el parser.

### 2.1 Bounded correction record

El candidate documental anterior:

```text
candidate_sha=c1bf6d90835d6673a75ba157e6e170e0ae1acaef
candidate_tree=63b18fcb23ffd0309b1771c1b85c4fe1bce8bd98
```

recibió:

```text
FAIL_DESIGN_CONTRACT_VALIDATION
RED_READY_FOR_OWNER_DECISION=NO
BLOCKING_FINDINGS=F01,F02
NON_BLOCKING_FINDINGS=N01,N02
authority_effect=none
```

Informe independiente suministrado por el Owner:

```text
MALAK-PR331-INDEPENDENT-CRITICAL-CONTRACT-DESIGN-VALIDATION.md
sha256=9be4c25ce4157ff8cd7f4fc896c9743f9c3346e74fb4b5558616c9750ab2b540
```

Esta corrección está limitada documentalmente a:

- F01: cerrar el origen de rejection metadata;
- F02: incorporar Malāk Alignment Matrix;
- N01: corregir el diagnóstico causal;
- N02: usar `REJECTED_DO_NOT_READ`.

No se agrega implementación ni se modifica el resultado histórico de C01.

## 3. Construction Preflight

El baseline remoto `main` fue revalidado antes de abrir esta unidad y sigue en
`8c401b2bed1c114efadba3777c7662f45e56e8c6` / tree `573c9b3e5cc49052863d9fb30b69d4e4d2322bfd`.

Inventario recursivo: 399 blobs trackeados del baseline, clasificados en el File
Coverage Ledger adjunto; el ledger agrega además los dos documentos de esta PR-A
para 401 filas totales. Inventario no equivale a lectura completa.

| Checkpoint | Disposición |
|---|---|
| P0 | PASS — repository, baseline, incident y work type exactos |
| P1 | PASS — fuentes obligatorias identificadas; profundidad en ledger |
| P2 | PASS — Human in Control, Capability First, Runtime Independence, fail-closed y authority none preservados |
| P3 | PASS — evidence/result asciende como información; no authority/control upstream |
| P4 | ADAPT — reutilizar E2/schema/parser existentes; no nuevo subsistema |
| P5 | risk 3 / critical contract por interpretar output usado como evidence |
| P6 | change scope documental congelado en esta PR-A |
| P7 | PASS sólo para diseño; implementation/RED/GREEN siguen no autorizados |

Fuentes rectoras reconciliadas: `AGENTS.md`, Cognitive Constitution,
Governance Constitution, Blueprint, Architecture Quality Gates, ADR-003,
ADR-004, `SECURITY.md`, Engineering Method, Construction Protocol, Construction
Preflight, Development Checklist, implementation roadmap, ideas y
`docs/project/concepts/**`. La evidencia externa no adquiere autoridad.

## 4. Estado técnico verificado

E2 V1 ya posee:

- `malak.e2.assertions.v1`;
- schema JSON explícito enviado en `ConversationRequest.response_json_schema`;
- enums de refs efectivamente disponibles;
- `history=()`;
- una sola inferencia;
- parser estricto posterior;
- rechazo de duplicate keys, non-finite JSON, unknown refs, duplicate refs,
  namespaces incorrectos, byte limits y reserved ref tokens;
- renderer determinista que inserta las citas desde `evidence_refs`.

La regla relevante del system prompt ya dice que las refs no deben aparecer en
texto libre. Sin embargo, el schema de `summary`, `assertion.text` y
`uncertainties[]` sólo expresa string + límites de longitud. El parser aplica
además la regla de token reservado.

La obligación ya era visible a nivel de system prompt, pero no estaba reflejada en la
metadata del schema ni reforzada por el contrato focused completo. El incidente C01
demuestra que esa exposición parcial no fue suficiente para evitar el rechazo en la
ruta real; no permite atribuir causalidad a un token concreto ni afirmar una mejora
futura sin nueva evidencia.

## 5. Investigación externa — Ollama 0.34.4 / Structured Outputs

Fuentes informativas, sin autoridad sobre Malāk:

- https://docs.ollama.com/capabilities/structured-outputs
- https://docs.ollama.com/api/chat
- https://github.com/ollama/ollama/releases/tag/v0.34.4
- https://github.com/ollama/ollama/issues/8325
- https://github.com/ollama/ollama/issues/12726

Hallazgos:

1. Ollama documenta `format=<JSON Schema>` en `/api/chat`.
2. La documentación recomienda además incluir el schema en el prompt para
   groundear la respuesta.
3. Ollama recomienda temperatura baja como tip de reliability, pero este gate no
   cambia sampling porque mezclaría variables causales.
4. La release 0.34.4 modificó internamente Structured Outputs y actualizó
   llama.cpp/MLX/XGrammar.
5. La documentación pública no congela para Malāk un subset contractual de todos
   los keywords JSON Schema.
6. Existen reportes históricos y posteriores donde `pattern` produjo
   `invalid JSON schema in format` o comportamiento incompatible.

Disposición:

```text
JSON Schema pattern as correctness boundary = REJECT for this slice
```

No porque regex sea intrínsecamente inválida, sino porque Malāk no posee evidencia
candidate-bound suficiente para tratar ese keyword provider-specific como una
garantía estable en el runtime congelado.

## 6. G0 — necesidad y alternativas

Necesidad demostrada: sí. Existe un rechazo runtime real, preservado y
reproducible en la frontera determinista.

Alternativas:

| Alternativa | Disposición |
|---|---|
| No cambiar | REJECT para reliability: conservaría exactamente el gap observado |
| Relajar parser | REJECT: degrada fail-closed |
| Strip/repair de refs en texto | REJECT: transforma output inválido |
| Retry automático | REJECT: viola single-attempt semantics |
| Cambiar modelo | DEFER: no corrige el contrato |
| temperature=0 | DEFER: variable de sampling separada |
| JSON Schema `pattern` como enforcement principal | REJECT en este slice: soporte no suficientemente estable/portable |
| Nuevo validator/service/manager | REJECT: responsabilidad existente ya pertenece a E2 |
| Espejar el contrato exacto en prompt + schema metadata y conservar parser | ADAPT — solución mínima candidata |

```yaml
G0_RESULT: PASS
NECESSITY: DEMONSTRATED
NEW_SUBSYSTEM: NO
AUTHORITY_EXPANSION: NO
MODEL_EXECUTION: NOT_AUTHORIZED
authority_effect: none
```

### 6.1 Malāk Alignment Matrix — bounded correction F02

La matriz aplica `docs/development/malak_construction_protocol.md §4.6`. No crea
autoridad nueva ni autorización de implementación.

| source | source_authority_class | applicable_invariant_or_intent | baseline_evidence | alignment_disposition | implementation_effect | deferred_or_rejected_effect | rationale | traceability_reference |
|---|---|---|---|---|---|---|---|---|
| Cognitive Constitution | normativa | generated output remains candidate; evidence/uncertainty explicit; no self-authority | E2 output is parsed/validated deterministically after generation | ADOPT | preserve strict parser as final acceptance boundary | auto-accept/repair/retry REJECTED | closes gap without delegating truth to model/provider | `docs/governance/cognitive_constitution.md`; §7 |
| Governance Constitution | normativa | Human in Control; no authority escalation; side effects explicit | current E2 inspection has `authority_effect=none` and no write authority | ADOPT | keep correction authority-free; future execution separately gated | Ready/Merge/G2/model execution from this design REJECTED | design evidence is information, not permission | `docs/governance/governance_constitution.md`; §§8–13 |
| Blueprint | normative architecture | Capability First; Runtime Independence; bounded responsibility | E2 semantics live in Capability; Runtime transports generic schema | ADAPT | expected PR-B delta remains inside `engineering_inspect.py` + tests | Runtime/Kernel/Planner/E3/E4 delta REJECTED absent new evidence | smallest boundary already owns the contract | `docs/architecture/blueprint.md`; §7.6 |
| SECURITY.md | protected security policy | model/evidence content is untrusted DATA; disclosure bounded | parser receives untrusted generated strings; baseline exceptions may interpolate unknown refs | ADAPT | expose only fixed local rejection metadata + exact digest/byte count | raw response, excerpts, values, keys, refs, repr, dynamic exception text REJECTED | closes F01 and prevents rejected content becoming registrable metadata | `SECURITY.md`; §7.5 |
| Architecture Quality Gates | accepted architecture | minimality, explicit failure modes, testability, no hidden coupling | one production file expected; no new service/store/module | ADOPT | fail pre-model on mismatch/overflow; fail post-model on invalid output | new subsystem/provider-specific correctness boundary REJECTED | preserves bounded architecture | `docs/architecture/architecture_quality_gates.md`; §§7–14 |
| ADR-003 | accepted decision | information may flow upward; authority/control may not | rejection result is informational, `authority_effect=none` | ADOPT | return bounded local diagnostic only | error-derived authority or upstream command REJECTED | preserves directional authority flow | `docs/architecture/adr/ADR-003-directional-communication-and-authority-flow.md` |
| ADR-004 | accepted decision | specification/verification before implementation | PR-A precedes RED/GREEN | ADOPT | freeze design first, then independent fix validation | implementation-before-spec REJECTED | candidate remains documentation-only | `docs/architecture/adr/ADR-004-specification-and-verification-first.md` |
| Construction Protocol §4.6 | operational process | material G0/G1 requires explicit alignment traceability | previous candidate omitted equivalent matrix (F02) | ADOPT | this matrix becomes the traceable admission record | implicit inheritance from #329 REJECTED | new `response_contract`/rejection metadata need own alignment | `docs/development/malak_construction_protocol.md §4.6` |
| implementation roadmap | operational/derived | E2 remains governed engineering capability; progressive evidence path | E2 capability and strict parser already exist | OBSERVE | no direct implementation authority | broader roadmap work DEFERRED | confirms scope direction only | `docs/project/implementation_roadmap.md` |
| ideas.md | conceptual non-normative | determinism/evidence-bound improvement without bypassing governance | current incident is concrete evidence; concept snapshot is not baseline | OBSERVE | none | unrelated/historical ideas DEFERRED | concept informs horizon, not candidate authority | `documents/projects/jarvis/ideas.md` |
| MALAK_RESEARCH_HORIZON_MAP | conceptual non-normative | investigate reliability/determinism with evidence | no normative permission derived from horizon | OBSERVE | none | research-only paths DEFERRED | preserves separation research != implementation | `docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md` |
| relevant `concepts/**` | conceptual non-normative | evidence-bound self-review, governed execution, no silent authority gain | #319/#327 flow already binds execution to freeze + Owner decision | ADAPT | preserve new-freeze/new-G2 requirement after model-visible change | autonomous reuse of prior freeze/G2 REJECTED | reuse intent only where compatible with higher sources | `docs/project/concepts/**`; §§12–13 |
| baseline E2 code/tests | implementation evidence | actual schema/parser/renderer behavior is the implementation truth for this unit | schema metadata omits reserved-ref rule; parser enforces it; unknown-ref error may include model values | ADAPT | mirror canonical schema in focused prompt; fixed local reject metadata; add RED/regression tests later | parser relaxation, raw-output logging, retry REJECTED | directly addresses demonstrated contract/disclosure gaps | `src/malak/capabilities/engineering_inspect.py`; `src/malak/capabilities/_engineering_analysis.py`; E2 tests |
| C01 incident + independent PR #331 validation | derived evidence, no authority | preserve historical attempt; findings remain candidate-bound | C01 consumed; F01/F02 blocking, N01/N02 non-blocking on prior candidate | ADAPT | bounded documentation correction only | C01 replay, C02/C03 execution, inferred raw output REJECTED | evidence narrows correction; does not authorize execution | #327 incident record; #330; independent report SHA-256 above |

```text
TO_IMPLEMENT (future PR-B, only after later authorization):
- focused E2 response-contract exposure from the canonical schema;
- fixed local-only rejection metadata;
- regression tests proving no rejected-content disclosure.

NOT_IMPLEMENTED:
- all production behavior described above.

DEFERRED:
- sampling/model changes;
- provider-specific schema keyword hardening;
- broader observability/reliability work.

REJECTED:
- parser relaxation;
- retries/repair/fallback;
- raw rejected-output persistence;
- dynamic exception text as registrable validator detail;
- Runtime/Kernel/Planner/E3/E4 scope expansion without new evidence.

WHY:
- close the demonstrated contract/disclosure gap with the smallest existing Capability boundary.
```

## 7. G1 — diseño candidato

### 7.1 Regla central

```text
provider structured constraint
!=
semantic acceptance

model-visible contract
+
provider structured constraint
+
deterministic parser
```

El parser actual sigue siendo el enforcement final. No se elimina ni relaja.

### 7.2 Cambio E2 focused mínimo

Sólo para la ruta E2 con `GovernedEngineeringEvidenceFocus`:

1. construir primero el mismo `response_json_schema` canónico;
2. agregar `description` explícita en los campos de free text:
   `summary`, `assertions[].text`, `uncertainties[]`;
3. la descripción debe reflejar exactamente la política vigente:
   no incluir tokens reservados standalone R/K/S/A + dígitos en free text;
   las citas van únicamente en `assertions[].evidence_refs`;
4. incluir el schema canónico como material local `response_contract` dentro
   del prompt focused;
5. distinguir explícitamente `response_contract` de `evidence_packet`:
   el primero es contrato local; el segundo sigue siendo DATA no confiable;
6. medir el prompt final completo contra el límite vigente antes del model call;
7. overflow => error pre-model, cero inferencias, sin truncation/fallback.

La ruta E2 no-focused no duplica el schema en el prompt en este slice. Esto evita
cambiar disponibilidad de inspecciones genéricas sin evidencia de necesidad.
La regla del parser permanece común y estricta.

### 7.3 Forma model-visible candidata

Conceptualmente:

```json
{
  "response_contract": {
    "...": "the exact canonical E2 JSON schema for this evidence catalog"
  },
  "evidence_packet": {
    "baseline_commit": "...",
    "inspection_term": "...",
    "repository_evidence": [],
    "knowledge_evidence": [],
    "structural_evidence": [],
    "limitations": {},
    "focus": {}
  }
}
```

No se agrega un schema paralelo ni un segundo contrato manual. El objeto incluido
en el prompt se deriva del mismo string canónico enviado a
`response_json_schema`.

Invariante:

```text
json.dumps(prompt.response_contract, canonical)
==
ConversationRequest.response_json_schema
```

Un mismatch interno debe fallar antes de generar.

### 7.4 Reserved refs

Se conserva el patrón parser vigente:

```text
(?<![A-Za-z0-9_])[RKSA][0-9]+(?![A-Za-z0-9_])
```

No se mueve esta garantía al provider. Se refleja semánticamente en la
`description` model-visible con ejemplos claros (`R1`, `[R1]`, `K2`,
`S3`, `A1`), pero la aceptación final continúa siendo determinista.

Esto cierra:

```text
hidden parser-only obligation
→ explicit model-visible obligation + same deterministic guard
```

sin afirmar equivalencia entre constrained decoding y validación Malāk.

### 7.5 Evidencia segura de output rechazado — bounded correction F01

No persistir raw model output ni fragmentos derivados de él.

Cuando una respuesta no vacía fue generada pero el parser/validator E2 la rechaza,
la superficie **registrable** de la capability debe contener exclusivamente
metadata local, fija y acotada:

```text
reason_code=E2_OUTPUT_CONTRACT_REJECTED
validator_code=DETERMINISTIC_VALIDATION_REJECTED
validator_detail=E2 output rejected by deterministic contract validation.
output_sha256=<sha256 of exact UTF-8 response>
output_bytes=<integer>
authority_effect=none
```

En este slice no se necesita distinguir públicamente el subtipo exacto de rechazo.
El detalle fijo es deliberadamente menos expresivo para impedir que valores no
confiables se conviertan en metadata registrable.

Reglas obligatorias:

- `reason_code`, `validator_code` y `validator_detail` provienen sólo de
  constantes locales del código;
- ninguno puede derivarse de valores, keys, refs, excerpts, `repr`,
  `Exception.args` o mensajes dinámicos controlados por el output;
- el error registrable no serializa `__cause__`, `__context__`, traceback ni
  una excepción subyacente cuyo mensaje pueda contener contenido rechazado;
- si se captura internamente una excepción de parser, la traducción pública usa
  un error local fijo y suprime chaining observable (`raise ... from None` o
  mecanismo equivalente probado);
- `output_sha256` se calcula sobre los bytes UTF-8 exactos de
  `response.content`, sin normalización;
- `output_bytes` es la longitud de esos mismos bytes UTF-8;
- el digest y el byte count identifican el intento, no certifican verdad,
  evidencia semántica ni autoridad;
- nunca incluir raw response, substring, offending token/ref/key/value o
  chain-of-thought;
- nunca reinyectar el output;
- no retry, repair ni fallback;
- el error sigue siendo error y STOP.

No se crea módulo, store, service o nueva persistencia. Un harness puede registrar
el error público fijo y los campos seguros anteriores. Cualquier diagnóstico más
detallado que requiera contenido rechazado queda fuera de este slice y requiere
nuevo diseño/gate.

Criterios de no exposición para RED futuro:

1. unknown ref con marcador arbitrario y salto de línea;
2. value largo y multibyte;
3. reserved ref en free text;
4. JSON inválido;
5. duplicate key;
6. cualquier rejection path existente que construya hoy mensajes dinámicos.

En todos los casos, el contenido sintético rechazado debe estar ausente de:
mensaje público, metadata serializable, args públicos, cause/context observable y
cualquier artefacto registrable. Sólo digest/bytes pueden depender del response
exacto.

### 7.6 Change scope futuro esperado

PR-B candidata, después de admisión de este diseño:

```text
src/malak/capabilities/engineering_inspect.py
tests/test_engineering_inspect.py
tests/test_e2_e3_contract_reliability_v1.py
```

Sólo si RED demuestra necesidad podrá agregarse otro archivo, con revisión de
scope previa. En particular:

```text
src/malak/runtime/ollama_runtime.py          delta esperado 0
src/malak/core/conversation.py              delta esperado 0
src/malak/services/conversation_service.py  delta esperado 0
src/malak/capabilities/engineering_analyze.py delta esperado 0
Kernel / Planner                            delta 0
```

## 8. Critical Contract Hardening

Ambigüedades materiales cerradas en diseño:

- schema no sustituye parser;
- descripción no se presenta como enforcement criptográfico/gramatical;
- provider support no se asume más allá del transporte JSON Schema ya integrado;
- no `pattern` provider-dependent;
- no repair/retry;
- no raw-output persistence;
- rejection metadata deriva sólo de constantes locales y nunca de contenido rechazado;
- no broaden E3/E4;
- no model/sampling change;
- no reejecución histórica de C01;
- model-visible context change invalida el freeze anterior;
- cualquier nueva ejecución requiere nuevo freeze + Owner G2.

Unknown/missing/duplicate handling permanece en el parser vigente.

```yaml
KNOWN_MATERIAL_AMBIGUITY_UNRESOLVED: 0  # producer claim after bounded correction; independent fix validation pending
RED_ADMISSIBLE_FROM_DESIGN_ALONE: NO
```

RED requiere revisión/promoción humana de PR-A y RDD Design Check sobre el
candidate documental exacto.

## 9. Cuatro preguntas de ley

### Blueprint

PASS como diseño del productor. La lógica permanece en Capability; Runtime,
Kernel y Planner no adquieren semántica E2.

### Cognitive Constitution

PASS. La generación continúa siendo candidata; parser/validation finalizan.
No se inventa evidencia y el rechazo sigue explícito.

### Governance Constitution

PASS del productor después de bounded correction. No hay permission, side effect,
learning, persistence, self-modification, Ready o Merge automático. La metadata de
rechazo registrable queda limitada a constantes locales + digest/bytes y no puede
transportar contenido rechazado.

### Kernel complexity

PASS. Delta esperado del Kernel = 0.

Estas disposiciones no certifican una implementación inexistente.

## 10. Design 4R

| Lente | Disposición del productor |
|---|---|
| Risk | PASS — no relaxation/retry/raw persistence; rejection metadata no deriva de output; freeze previo se invalida ante prompt/schema change |
| Readability | PASS — un schema canónico, no segundo DSL; contract/evidence separados |
| Reliability | PASS — la obligación ya visible en prompt se refleja/refuerza en schema metadata + focused contract; enforcement final queda igual |
| Resilience | PASS — overflow/output inválido terminan en STOP; error registrable usa sólo metadata local fija + digest/bytes; sin fallback |

Riesgo residual: un LLM aún puede producir output rechazable aunque el contrato
sea más explícito. Esta unidad busca reducir contract rejection; no garantiza
compliance probabilística.

## 11. RDD Stage 1 Design Check — productor

```text
baseline binding                 PASS
future candidate identity        commit/tree bound
evidence provenance              PASS
Writer/Reviewer/Validator split  preserved
PASS/FAIL/INCONCLUSIVE only      preserved
candidate change invalidation    required
bounded correction               required on blocking finding
authority_effect                 none
risk_class                       3
RDD Stage 2 on PR-B              REQUIRED
```

```yaml
RDD_STAGE1_DESIGN_CHECK_PRODUCER: PASS
PREVIOUS_INDEPENDENT_DESIGN_VALIDATION: FAIL_ON_c1bf6d90835d6673a75ba157e6e170e0ae1acaef
BOUNDED_CORRECTION_F01_F02_N01_N02: APPLIED_PRODUCER
INDEPENDENT_FIX_VALIDATION: PENDING
RED_AUTHORIZED: NO
GREEN_AUTHORIZED: NO
```

## 12. RED mínimo futuro

Después de merge humano del design y nueva autorización explícita:

1. focused E2 prompt contiene `response_contract`;
2. `response_contract` reproduce byte/canonicalmente el schema pedido;
3. free-text descriptions reflejan reserved-ref policy;
4. output con reserved ref en free text sigue rechazado;
5. output válido con refs sólo en `evidence_refs` sigue aceptado;
6. unknown refs siguen rechazadas;
7. duplicate refs/keys siguen rechazadas;
8. no-focused E2 no recibe duplicación de schema en prompt;
9. provider calls = 1 para output rechazado; no retry;
10. rechazo posterior a generación expone sólo códigos/detail locales fijos + digest/bytes; tests adversariales prueban que refs/values/keys/excerpts, saltos de línea, multibyte, JSON inválido y duplicate keys no aparecen en mensaje/args/cause/context/metadata registrable;

11. E3/E4/runtime/conversation permanecen sin delta;
12. overflow del prompt combinado falla antes de provider call.

RED no ejecuta Ollama real.

## 13. Validación futura de PR-B

Orden obligatorio:

```text
PR-A design review / Owner merge
→ RED exact candidate
→ Owner GREEN authorization
→ GREEN minimum
→ targeted tests
→ Candidate FULL 4R
→ Bounded Correction / Fix Validator if needed
→ E2E/integration
→ CI candidate-bound
→ independent validation
→ RDD Stage 1 Candidate Conformance
→ RDD Stage 2 receipt (risk 3)
→ human Ready / Merge
→ post-merge validation
→ NEW PRE-MODEL FREEZE
→ NEW OWNER G2
→ only then any new model execution
```

C01 Attempt 1 permanece histórico y consumido. C02/C03 no se gastan para validar
una implementación no cerrada.

## 14. COMPLEXITY_DELTA

PR-A actual:

```text
production code delta    0
runtime delta            0
Kernel delta             0
dependencies             0
new services/managers    0
documents                2
```

PR-B propuesta:

```text
new modules              0
new classes              0 expected
new persistence          0
additional model calls   0
retries                  0
provider-specific logic  0
production files         1 expected
```

## 15. Disposición terminal

```yaml
G0: PASS
G1_DESIGN: PASS_PRODUCER
CRITICAL_CONTRACT_HARDENING: PASS_PRODUCER
LAW_QUESTIONS: PASS_PRODUCER
DESIGN_4R: PASS_PRODUCER
RDD_STAGE1_DESIGN_CHECK: PASS_PRODUCER
INDEPENDENT_DESIGN_VALIDATION: PENDING
SOLUTION_IMPLEMENTED: NO
C01_RETRY: FORBIDDEN
C02: HOLD
C03: HOLD
RED_AUTHORIZED: NO
GREEN_AUTHORIZED: NO
MODEL_EXECUTION_AUTHORIZED: NO
RED_READY_FOR_OWNER_DECISION: NO
READY_FOR_OWNER_REVIEW: NO
MERGE_AUTHORIZED: NO
authority_effect: none
```
