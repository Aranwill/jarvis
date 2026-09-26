---
title: Malāk Engineering Runtime Generation Contract V0 — G0/G1 Design
status: proposed
authority: non_normative
document_role: design
language: es
created: 2026-09-26
baseline_commit: 7ab94f7bfd15a3fbf5f23a09db0d84a95a47b032
implementation_authorized: false
red_authorized: true
red_authorized_by: owner
red_authorized_at: 2026-09-26
green_authorized: false
runtime_execution_authorized: false
authority_effect: none
related:
  - docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md
  - docs/project/sprints/proposals/MALAK-FOURTH-U01-ADMISSION-REVIEW-20260925.md
  - docs/project/sprints/proposals/MALAK-ANALYZE-STRUCTURED-OUTPUT-CONTRACT-V0-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-INTERNAL-INTERACTION-OBSERVABILITY-DIAGNOSTICS-MODEL-PROVENANCE-V0-G0-G1-DESIGN.md
  - src/malak/core/conversation.py
  - src/malak/runtime/ollama_runtime.py
  - src/malak/runtime/runtime_provenance.py
  - src/malak/app/internal_interaction_test_v0.py
---

# Malāk Engineering Runtime Generation Contract V0 — G0/G1 Design

## 1. Propósito

Diseñar, sin implementar todavía, un contrato explícito y gobernado para las opciones materiales de generación utilizadas por el runtime local durante Engineering / Internal Interaction Test V0.

El diseño nace de `bootstrap-u01-20260925-004` y busca cerrar ambigüedades de contexto efectivo, presupuesto de salida, política de thinking y provenance sin relajar validadores existentes ni convertir defaults del provider en política implícita de Malāk.

Este documento NO autoriza RED, GREEN ni una nueva ejecución U01.

## 2. Evidencia de origen — Fourth U01

```text
run_id                     bootstrap-u01-20260925-004
execution_baseline         7ab94f7bfd15a3fbf5f23a09db0d84a95a47b032
Evidence Packet            READY
Inspect                    component_error
Analyze                    SKIPPED / precondition_not_met
Propose                    SKIPPED / precondition_not_met
terminal_disposition       INCONCLUSIVE
live_replay_equivalence    true
tracked_tree_clean         true
acceptance                 PASS
authority_effect           none
```

Safe diagnostic:

```text
component              engineering_inspect
reason_code            component_error
exception_type         RuntimeError
cause_chain_types      RuntimeError
repo_relative_file     src/malak/capabilities/engineering_inspect.py
function               execute
line                   206
```

La línea correspondiente rechaza contenido final vacío o whitespace. Ese fail-closed funcionó correctamente y no debe relajarse.

## 3. Evidencia runtime observada

Durante la ejecución real de Ollama se observó aproximadamente:

```text
runner context          4096
prompt tokens           2050
generated tokens        2046
sum                     4096
runner                  truncated = 1
HTTP                    200
```

El mismo run persistió:

```text
runtime_class              OllamaRuntime
requested_model            qwen3.5:9b
resolved_model             qwen3.5:9b
model_identity_strength    TAG_DIGEST_BOUND
declared_context_window    262144
context_window_source      ollama:model_info
generation_options         {}
provenance_status          READY
authority_effect           none
```

`/api/show` confirmó `qwen35.context_length = 262144`. Por tanto, la capacidad declarada del modelo y el contexto efectivo usado por una request son conceptos distintos.

## 4. Evidencia upstream exacta — Ollama v0.33.3

Se revisó el tag `v0.33.3`, que coincide con la versión local observada.

### 4.1 Context selection

Los tests upstream de `server/routes_options_test.go` establecen prioridad material:

```text
request num_ctx
> model num_ctx
> environment / runtime default
```

Si Malāk omite `num_ctx`, la request queda sujeta a un default externo.

### 4.2 Qwen 3.5 thinking

En `model/renderers/renderer.go` de v0.33.3, Qwen 3.5 se instancia con thinking habilitado. En `model/parsers/qwen35.go`, cuando `thinkValue == nil`, `thinkingEnabled = true`.

Por tanto, para esta versión exacta:

```text
think omitted
-> Qwen 3.5 thinking enabled
```

La ausencia de metadata top-level `thinking` en `/api/show` no equivale a thinking deshabilitado.

### 4.3 API controls

`api/types.go` de v0.33.3 expone en ChatRequest:

```text
options
think
truncate
shift
```

y separa `message.thinking` de `message.content`.

## 5. Gaps formalizados

### RTCTX-01 — Request Context Binding

```text
declared context known
+ request num_ctx absent
= effective context delegated to provider defaults
```

Malāk no puede afirmar que el contexto declarado por el modelo sea el utilizado por una request específica.

### THINK-01 — Explicit Thinking Policy

```text
think omitted
-> provider/model behavior decides
```

Una decisión cognitiva material queda fuera del contrato explícito de Malāk.

### RTMETA-01 — Generation Contract Provenance

```text
runtime_provenance.generation_options == {}
```

El artifact no conserva las opciones materiales que gobernaron la generación.

### BUDGET-01 — Explicit Output Budget

`num_predict` no está fijado por Malāk para Self-Review gobernado.

### TERM-01 — Budget Exhaustion Classification

Un HTTP 200 con contenido vacío termina degradando en un `component_error`; Malāk todavía no usa metadatos seguros del provider para distinguir agotamiento de presupuesto de otros errores.

### INPUT-01 — Silent Input Mutation

`truncate` y `shift` no están gobernados explícitamente para Self-Review. Un provider no debe poder adaptar silenciosamente input/history para caber en contexto.

## 6. Principios de diseño

```text
provider default != governed policy
declared capability != request execution contract
HTTP success != valid generation
hidden reasoning != evidence
implicit repair/retry == forbidden
critical runtime config must be explicit
```

No se permite resolver el problema aceptando contenido vacío, promoviendo `message.thinking` a respuesta final, reintentando automáticamente ni aumentando contexto después de un fallo.

## 7. Alternativas consideradas

### A — Cambiar sólo OLLAMA_CONTEXT_LENGTH

Rechazada como solución arquitectónica: movería el default externo pero no cerraría el contrato.

### B — Hardcodear num_ctx dentro de OllamaRuntime

Rechazada: mezcla mecanismo del adapter con política local/hardware.

### C — Política distinta por Capability

Defer: todavía no hay evidencia suficiente para justificar perfiles separados de Inspect / Analyze / Propose.

### D — Contrato explícito, request-scoped, inyectado por composición Engineering

Seleccionada para V0. El contrato viaja en `ConversationRequest`, la composición Engineering aplica el mismo objeto a E2/E3/E4 y el runtime sólo lo mapea. Así el chat genérico puede seguir usando el mismo runtime sin heredar política de Self-Review.

## 8. RuntimeGenerationContract V0

Se propone un value object inmutable y provider-neutral:

```python
@dataclass(frozen=True, slots=True)
class RuntimeGenerationContract:
    context_window_tokens: int
    max_output_tokens: int
    thinking_enabled: bool
```

V0 no admite un modo `auto/default/provider` ni mapas arbitrarios de opciones.

## 9. Invariantes

```text
context_window_tokens -> int exact, > 0, bool forbidden
max_output_tokens     -> int exact, > 0, bool forbidden
thinking_enabled      -> bool exact
max_output_tokens < context_window_tokens
```

Durante admission/preflight, si existe `declared_context_window`:

```text
context_window_tokens <= declared_context_window
```

Si el provider/runtime no puede aplicar el contrato requerido, el run gobernado debe fallar cerrado.

## 10. Mapping a Ollama

Con contrato explícito:

```text
context_window_tokens -> options.num_ctx
max_output_tokens     -> options.num_predict
thinking_enabled      -> think
input truncation      -> truncate=false
history shifting      -> shift=false
```

Los valores numéricos exactos NO se aprueban en este diseño; se congelarán en un admission posterior.

## 11. Binding y ownership

V0 corrige una ambigüedad importante del diseño inicial: el contrato NO debe quedar como estado global de `OllamaRuntime`, porque el CLI comparte el mismo runtime entre conversación ordinaria y Engineering.

Binding seleccionado:

```text
CLI configuration
-> RuntimeGenerationContract
-> build_engineering_kernel_set(..., generation_contract=contract)
-> same immutable contract supplied to E2 / E3 / E4
-> ConversationRequest.generation_contract
-> RuntimeConversationProvider passthrough
-> OllamaRuntime mapping
```

Ownership:

```text
CLI / app boundary  -> construye y valida política externa
Composition         -> distribuye un único contrato a Engineering
Capability          -> adjunta el contrato recibido; no inventa valores
ConversationService -> passthrough; no selecciona policy
RuntimeProvider     -> passthrough; no selecciona policy
OllamaRuntime       -> mapea mecanismo; no inventa defaults
Self-Review Harness -> exige contract presente antes de Engineering
Kernel / Planner    -> sin cambios
```

Regla:

```text
request-scoped contract
!= runtime-global mutable policy
```

Esto evita que una política destinada a Engineering altere silenciosamente el chat genérico.

## 12. Compatibilidad con conversación genérica

`ConversationRequest` incorpora:

```text
generation_contract: RuntimeGenerationContract | None = None
```

Semántica:

```text
generic conversation request
-> generation_contract=None
-> payload existente preservado

Engineering request con contract configurado
-> explicit generation contract

Internal Interaction Test V0 + Engineering contract absent
-> unavailable / fail closed before Engineering
```

`dataclasses.replace()` de `ConversationService` debe preservar el campo automáticamente al enriquecer history. Un test contractual debe demostrarlo.

No se autoriza un default global en `OllamaRuntime` para resolver este slice.

## 13. Configuración externa propuesta

```text
MALAK_OLLAMA_CONTEXT_WINDOW_TOKENS
MALAK_OLLAMA_MAX_OUTPUT_TOKENS
MALAK_OLLAMA_THINKING
```

`MALAK_OLLAMA_THINKING` acepta únicamente `enabled` o `disabled` para Self-Review gobernado.

## 14. Thinking policy

V0 exige `thinking_enabled` explícito, pero no codifica todavía una política permanente para todo Engineering.

Para el próximo admission, `thinking_enabled=false` es un candidato a evaluar porque el Fourth U01 demostró que el comportamiento implícito del provider puede consumir el presupuesto antes de producir contenido final observable. No es todavía una constante aprobada de producción.

## 15. Safe provenance

`RuntimeModelProvenance.generation_options` ya existe. V0 propone persistir allí el contrato solicitado:

```json
{
  "context_window_tokens": 8192,
  "max_output_tokens": 2048,
  "thinking_enabled": false,
  "input_truncation_allowed": false,
  "history_shift_allowed": false
}
```

Los números son ilustrativos. Se preserva la distinción:

```text
declared_context_window
-> capacidad declarada del modelo

generation_options.context_window_tokens
-> contrato solicitado para el run
```

Esto no es attestation criptográfica de ejecución exacta.

## 16. Response validation

Bajo contrato explícito, OllamaRuntime debe usar sólo metadata segura del response.

Se propone validar:

```text
done == true para non-streaming gobernado
done_reason == length -> generation_budget_exhausted / fail closed
prompt_eval_count >= 0 si está presente
eval_count >= 0 si está presente
eval_count <= max_output_tokens si está presente
prompt_eval_count + eval_count <= context_window_tokens si ambos están presentes
```

También puede observarse `bool(message.thinking)`, pero nunca persistir su contenido.

Si `thinking_enabled=false` y `message.thinking` es no vacío:

```text
generation_contract_violation
-> fail closed
```

`message.thinking` nunca se usa como `message.content`.

## 17. Input truncation y shift

Para Self-Review V0:

```text
truncate=false
shift=false
```

son invariantes. Input demasiado grande debe producir error y STOP, no una mutación silenciosa del evidence packet.

## 18. Relación con Evidence Focus

Generation Contract no cambia selectores, completeness, `evidence_set_digest` ni continuidad Inspect -> Analyze -> Propose.

```text
generation resources != evidence identity
```

## 19. Relación con Structured Output

```text
response_json_schema       -> output shape contract
RuntimeGenerationContract  -> resource / thinking contract
strict parser              -> semantic acceptance
```

Los tres son capas distintas y complementarias.

## 20. No raw reasoning persistence

Prohibido agregar a artifacts:

```text
message.thinking text
raw response
chain-of-thought
provider hidden reasoning
```

Permitido si es necesario:

```text
thinking_requested: true|false
thinking_present: true|false
done
done_reason
token counts
requested budgets
```

## 21. Scope esperado de implementación

Producción probable:

```text
src/malak/runtime/runtime_generation_contract.py   NEW
src/malak/core/conversation.py
src/malak/runtime/ollama_runtime.py
src/malak/runtime/mock_llm_runtime.py
src/malak/runtime/runtime_provenance.py
src/malak/app/cli.py
src/malak/app/composition.py
src/malak/app/internal_interaction_test_v0.py
src/malak/capabilities/engineering_inspect.py
src/malak/capabilities/engineering_analyze.py
src/malak/capabilities/engineering_propose.py
src/malak/capabilities/_engineering_analysis.py
```

Los cambios en Capability/composition quedan limitados a transportar el mismo contrato inmutable; no autorizan policy distinta por E2/E3/E4 ni cambios de parser.

Tests probables:

```text
tests/test_conversation_contract.py
tests/test_conversation_service.py
tests/test_llm_runtime.py
tests/test_ollama_runtime.py
tests/test_runtime_provenance.py
tests/test_composition.py
tests/test_engineering_inspect.py
tests/test_engineering_analyze.py
tests/test_engineering_propose.py
tests/test_cli_self_review_v0.py
tests/test_internal_interaction_test_v0_harness.py
```

Guardrails:

```text
Kernel delta             0
Planner delta            0
Request routing delta    0
Evidence Focus delta     0
Engineering parser logic 0
Structured Output logic  0
Capability policy split  0
```

Si alguno necesita cambiar, STOP y nueva revisión de scope.

## 22. Fuera de alcance

```text
per-Capability context profiles
named thinking levels
adaptive context sizing
automatic VRAM tuning
automatic retry
retry with think=false
retry with larger context
prompt/evidence compression
raw response storage
raw thinking storage
model replacement
model pull/update
provider feature-negotiation framework
streaming
tool calls
Kernel changes
Planner changes
U04 execution
RR-03 execution
self-modification
```

## 23. RED scenarios propuestos

RED requiere autorización separada.

```text
R01 invalid / zero / bool token budgets -> reject
R02 max_output_tokens >= context_window_tokens -> reject
R03 request-scoped contract -> num_ctx, num_predict, think, truncate=false, shift=false
R04 generic request without contract -> existing payload unchanged
R05 ConversationService history enrichment preserves generation_contract
R06 Mock runtime + explicit generation_contract -> fail closed
R07 provenance -> exact canonical generation_options
R08 Self-Review without Engineering contract -> STOP before Engineering
R09 done_reason=length -> fail closed
R10 done=false -> fail closed
R11 thinking_enabled=false + thinking present -> fail closed
R12 Analyze keeps format=<schema> together with generation contract
R13 E2/E3/E4 receive the exact same immutable contract identity/value
R14 Inspect empty final content rejection remains unchanged
```

## 24. GREEN acceptance

GREEN futuro sólo puede aceptarse si todos los RED pasan y además:

```text
existing suite remains green
no previous assert weakened
no fail-closed path removed
no automatic retry introduced
generic Ollama behavior unchanged without contract
Structured Output preserved
Evidence Focus preserved
Kernel / Planner delta 0
authority_effect none
```

## 25. FULL 4R requerido

Este cambio toca ejecución externa gobernada y se clasifica como riesgo alto.

### Risk

Sin fallback oculto, sin input mutation silenciosa, sin reasoning persistido, sin escalamiento automático de recursos.

### Readability

Un contrato, un owner de mapping, sin mapa arbitrario de provider options y nombres explícitos para declared vs requested context.

### Reliability

Tests candidate-bound, mapping exacto, provenance exacta, agotamiento detectable y validadores semánticos existentes intactos.

### Resilience

Unsupported option, contexto insuficiente o budget exhaustion deben terminar fail-closed, sin retries ni self-healing.

## 26. Anti-relaxation

Debe demostrarse:

```text
engineering_inspect empty validator        unchanged
analysis strict JSON parser                unchanged
analysis semantic validators               unchanged
evidence completeness                      unchanged
evidence_set_digest                        unchanged
raw exception persistence                  none
raw response persistence                   none
raw thinking persistence                   none
automatic retry                            none
automatic context increase                 none
automatic thinking switch                  none
authority expansion                        0
```

## 27. Próximo admission

Después de implementación y merge, una nueva ejecución U01 requerirá admission independiente que congele:

```text
model tag
model digest
runtime version
declared context
requested context_window_tokens
requested max_output_tokens
thinking_enabled
truncate=false
shift=false
exact execution baseline
run_id
```

Los valores numéricos permanecen `UNCONFIRMED` hasta ese admission/local resource review.

## 28. RDD flow

```text
G0/G1 design
-> Owner review
-> merge design
-> explicit RED authorization
-> RED exact candidate
-> candidate-bound validation
-> explicit GREEN authorization
-> GREEN exact candidate
-> candidate-bound CI
-> FULL 4R
-> anti-relaxation
-> deterministic E2E/conformance
-> Owner review / merge
-> separate runtime admission
-> explicit next-U01 authorization
-> local preflight
-> run
-> STOP
```

## 29. G0/G1 disposition

```text
Fourth U01 failure isolated                 PASS
RTCTX-01 identified                         PASS
THINK-01 identified                         PASS
RTMETA-01 identified                        PASS
BUDGET-01 identified                        PASS
TERM-01 identified                          PASS
INPUT-01 identified                         PASS

request-scoped Engineering contract selected PASS
provider mapping specified                  PASS
safe provenance specified                   PASS
anti-relaxation specified                   PASS
RED scenarios frozen                        PASS

implementation                              NOT AUTHORIZED
RED                                         NOT AUTHORIZED
GREEN                                       NOT AUTHORIZED
next U01                                    NOT AUTHORIZED
authority_effect                            none

G0/G1 RESULT:
READY FOR OWNER REVIEW
```


## 30. RED authorization checkpoint — 2026-09-26

El Owner autorizó explícitamente avanzar con RED después del merge de G0/G1.

Baseline congelado:

```text
main@b183d8921a34f778e204a8a65330890a4e5c3d67
```

Scope autorizado:

```text
tests only
+
documentación de evidencia RED
```

No autorizado:

```text
production implementation
GREEN
runtime execution
next U01
self-modification
authority expansion
```

### 30.1 Interface freeze para RED

Los tests RED fijan estas fronteras del diseño sin implementar producción:

```text
RuntimeGenerationContract
-> provider-neutral immutable value object

ConversationRequest
-> generation_contract: RuntimeGenerationContract | None

OllamaRuntime.capture_provenance(
    model,
    generation_contract=...
)

build_engineering_kernel_set(
    ...,
    generation_contract=...
)

EngineeringKernelSet.generation_contract
-> same immutable object retained across with_evidence_focus()
```

Esto resuelve la única ambigüedad de interfaz pendiente entre request-scoped
generation policy y provenance del run, sin convertir el contrato en estado
global mutable del runtime.

### 30.2 Expected RED matrix

```text
R01 FAIL  invalid / zero / bool token budgets are not contract-rejected yet
R02 FAIL  budget relation is not contract-rejected yet
R03 FAIL  Ollama request mapping is absent
R04 PASS  generic Ollama request remains unchanged
R05 FAIL  ConversationService cannot preserve a missing generation_contract field
R06 FAIL  Mock runtime does not fail closed on generation contract
R07 FAIL  provenance does not bind requested generation options
R08 FAIL  Self-Review harness does not require Engineering generation contract
R09 FAIL  done_reason=length is not classified fail-closed
R10 FAIL  done=false is not classified fail-closed
R11 FAIL  disabled-thinking contract is not enforced against returned thinking
R12 FAIL  Structured Output + generation contract coexistence is absent
R13 FAIL  composition does not bind one contract through E2/E3/E4/focused rebuild
R14 PASS  Inspect empty final content remains fail-closed
```

Resultado RED esperado:

```text
12 failing scenarios
2 control scenarios passing
0 unrelated failures
```

El candidate RED deberá mantener:

```text
src/malak/** delta = 0
Kernel delta       = 0
Planner delta      = 0
authority_effect   = none
```
