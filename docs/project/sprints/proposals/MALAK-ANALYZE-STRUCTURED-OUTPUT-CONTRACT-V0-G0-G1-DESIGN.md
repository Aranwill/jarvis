---
title: Malāk Analyze Structured Output Contract V0 — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation_design
language: es
created: 2026-09-25
baseline_commit: 0ad053e83867aac54142f070150bf11d09cdcee8
g0_result: pass
design_authorized_by: owner
design_authorized_at: 2026-09-25
risk_class: 3
critical_contract: true
implementation_authorized: true
implementation_scope: analyze_structured_output_v0_only
red_authorized: true
red_authorized_by: owner
red_authorized_at: 2026-09-25
green_authorized: true
green_authorized_by: owner
green_authorized_at: 2026-09-25
runtime_execution_authorized: false
fourth_u01_execution_authorized: false
authority_effect: none
rdd_stage_2_authorized: false
related:
  - docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md
  - docs/project/sprints/proposals/MALAK-E3-ENGINEERING-ANALYZE-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-E4-ENGINEERING-PROPOSE-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-GOVERNED-ENGINEERING-EVIDENCE-FOCUS-V0-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-INTERNAL-INTERACTION-OBSERVABILITY-DIAGNOSTICS-MODEL-PROVENANCE-V0-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-THIRD-U01-ADMISSION-REVIEW-20260925.md
  - src/malak/core/conversation.py
  - src/malak/core/llm_runtime.py
  - src/malak/services/conversation_service.py
  - src/malak/runtime/ollama_runtime.py
  - src/malak/capabilities/_engineering_analysis.py
  - src/malak/capabilities/engineering_analyze.py
  - src/malak/capabilities/engineering_propose.py
---

# Malāk Analyze Structured Output Contract V0 — G0/G1 Design

## 1. Propósito

Cerrar el fallo material observado durante el tercer U01 real sin relajar los
validadores fail-closed existentes y sin acoplar Engineering directamente a
Ollama.

El problema observado es:

```text
Engineering Analyze
-> evidencia completa
-> Inspect GROUNDED
-> modelo invocado
-> response.content recibido
-> parse_engineering_analysis()
-> JSONDecodeError
-> RuntimeError
-> component_error
-> Propose SKIPPED
-> terminal INCONCLUSIVE
```

La frontera a endurecer es:

```text
machine-readable output contract
between Engineering and the LLM runtime
```

No es:

```text
evidence retrieval
baseline binding
model provenance
Ollama reachability
timeout
authority
```

## 2. Baseline G0

Baseline exacto:

```text
repository: Aranwill/jarvis
branch: main
baseline: 0ad053e83867aac54142f070150bf11d09cdcee8
```

Estado relevante integrado:

```text
Governed Engineering Evidence Focus V0      INTEGRATED
OBS-01 Live Elapsed                         INTEGRATED
OBS-02 Safe Diagnostics                     INTEGRATED
Runtime / Model Provenance V0               INTEGRATED
Third U01 Admission Review                  INTEGRATED
```

No se reabre ninguno de esos contratos en este gate.

## 3. Evidencia del Third U01 real

Run:

```text
bootstrap-u01-20260925-003
```

Baseline:

```text
0ad053e83867aac54142f070150bf11d09cdcee8
```

Modelo/runtime:

```text
runtime_class:            OllamaRuntime
requested_model:          qwen3.5:9b
resolved_model:           qwen3.5:9b
model_identity_strength:  TAG_DIGEST_BOUND
provenance_status:        READY
authority_effect:         none
```

Evidence / Inspect:

```text
Evidence Packet:          READY
missing_required_sources: none
unreadable_required:      none

Inspect status:           GROUNDED
focus_id:                 U01
focus_complete:           true
evidence_set_digest:
7dea2fce5f206f9fc14e8f091952aacceadd6194533c84a885068b1f03272c76
```

Analyze diagnostic:

```text
diagnostic_id:       D0001
component:           engineering_analyze
reason_code:         component_error
exception_type:      RuntimeError
cause_chain_types:   RuntimeError, JSONDecodeError
origin_scope:        repository
repo_relative_file:  src/malak/capabilities/_engineering_analysis.py
function:            parse_engineering_analysis
line:                269
authority_effect:    none
```

Terminal:

```text
Analyze:                FAILED
Propose:                precondition_not_met
terminal_disposition:   INCONCLUSIVE
live_replay_equivalence true
tracked_tree_clean      true
acceptance              PASS
authority_effect        none
```

Interpretación causal:

```text
Harness acceptance PASS
!=
cognitive completion

Evidence Focus reached Analyze successfully.
Analyze failed while parsing model content as strict JSON.
```

## 4. Contrato actual de E3

E3 ya exige al modelo:

```text
Return strict JSON only
exact top-level fields:
summary, findings, uncertainties
```

El parser actual aplica:

```text
json.loads(...)
duplicate-key rejection
non-finite JSON rejection
exact-key validation
classification allow-list
evidence ref validation
repository + knowledge evidence requirement
hard count / byte bounds
reserved-ref protections
```

Por tanto:

```text
parser strictness
= desired safety property
```

No se relaja.

## 5. Gap arquitectónico

Hoy `ConversationRequest` expresa:

```text
prompt
model
system_prompt
history
```

y `OllamaRuntime.generate()` envía:

```text
model
messages
stream=false
keep_alive
```

No existe un contrato provider-neutral que permita a una Capability declarar:

```text
this response must satisfy this JSON Schema
```

En consecuencia, E3 tiene:

```text
strict parser
+
prompt instruction
-
runtime structured-output enforcement
```

El tercer U01 demostró que esa frontera no es suficientemente robusta.

## 6. Base externa verificada

La API actual de Ollama soporta Structured Outputs en `/api/chat` mediante el
campo:

```text
format
```

que puede contener:

```text
"json"
OR
JSON Schema object
```

Fuentes oficiales consultadas:

```text
https://github.com/ollama/ollama/blob/main/docs/api.md
https://github.com/ollama/ollama/blob/main/docs/capabilities/structured-outputs.mdx
https://github.com/ollama/ollama/blob/main/docs/openapi.yaml
```

La documentación recomienda mantener validación posterior del contenido. Ese
principio coincide con Malāk:

```text
runtime structural constraint
!=
semantic acceptance
```

## 7. Decisión de arquitectura G1

No se introduce un tipo `OllamaFormat` en Engineering.

Se agrega una primitive provider-neutral y mínima en la frontera de
Conversation:

```text
ConversationRequest
    response_json_schema: str | None
```

Propiedades:

```text
optional
immutable string
canonical JSON
root object
byte bounded
no authority
no provider identity
```

Flujo:

```text
Engineering Analyze
-> static ANALYZE_RESPONSE_SCHEMA
-> canonical schema JSON
-> ConversationRequest.response_json_schema
-> ConversationService passthrough
-> registered provider/runtime
-> OllamaRuntime maps schema to /api/chat format
-> model response
-> existing strict parser
-> existing semantic validators
```

## 8. Por qué schema como string canónico

No se usa un `dict` mutable dentro de `ConversationRequest`.

Preferencia:

```text
canonical JSON string
```

sobre:

```text
nested mutable mapping
```

por:

- inmutabilidad natural;
- comparación determinista;
- serialización estable;
- menor superficie de copia defensiva;
- desacople de tipos internos del provider.

El provider que soporte JSON Schema debe:

```text
parse schema string
-> require JSON object
-> forward object in provider-native mechanism
```

## 9. Regla de providers

El contrato de `ConversationRequest` no garantiza que todo provider futuro
soporte Structured Outputs.

Regla:

```text
response_json_schema is None
-> existing behavior

response_json_schema is present
AND provider supports it
-> enforce provider-native structured output

response_json_schema is present
AND provider cannot enforce it
-> FAIL CLOSED
-> do not silently ignore
```

Para V0 se implementan dos comportamientos explícitos:

```text
OllamaRuntime
-> soporta response_json_schema
-> lo mapea a /api/chat format

MockLLMRuntime
-> NO soporta structured output
-> si recibe response_json_schema != None
   FAIL CLOSED
```

Esto evita que un runtime in-tree ignore silenciosamente un contrato solicitado.

No se crea capability negotiation framework ni registry de features en este
slice. La ausencia de soporte se expresa por comportamiento fail-closed del
runtime concreto.

## 10. Analyze response schema

E3 declara un schema estructural estático equivalente a:

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["summary", "findings", "uncertainties"],
  "properties": {
    "summary": {
      "type": "string"
    },
    "findings": {
      "type": "array",
      "minItems": 1,
      "maxItems": 16,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "classification",
          "statement",
          "rationale",
          "evidence_refs"
        ],
        "properties": {
          "classification": {
            "type": "string",
            "enum": [
              "ALIGNED",
              "PARTIAL",
              "GAP",
              "CONTRADICTION",
              "UNRESOLVED"
            ]
          },
          "statement": {
            "type": "string"
          },
          "rationale": {
            "type": "string"
          },
          "evidence_refs": {
            "type": "array",
            "minItems": 1,
            "maxItems": 16,
            "uniqueItems": true,
            "items": {
              "type": "string"
            }
          }
        }
      }
    },
    "uncertainties": {
      "type": "array",
      "maxItems": 16,
      "items": {
        "type": "string"
      }
    }
  }
}
```

El schema NO reemplaza validaciones E3.

## 11. Separación structural vs semantic

Structured Output sólo mejora:

```text
JSON syntax
object/array shape
required fields
basic types
enum
basic item counts
additional properties
```

El parser de Malāk sigue siendo autoridad para:

```text
duplicate-key defense
non-finite values
UTF-8 byte bounds
non-empty / whitespace-only text
control / format characters
reserved ref tokens
actual allowed evidence refs
R + K evidence requirement
cross-finding semantics
uncertainty semantics
all existing E3 invariants
```

Regla:

```text
provider accepted schema
!=
Malāk accepted analysis
```

## 12. No se hace output repair

V0 prohíbe:

```text
strip markdown fences
extract first {...}
regex JSON recovery
automatic retry
"please fix your JSON" retry
silent parser relaxation
persist raw model response
fallback to unconstrained generation
```

Si Structured Output aun produce contenido que falla E3:

```text
component_error
-> safe diagnostic
-> INCONCLUSIVE
-> STOP
```

## 13. No se modifica temperature en este slice

La documentación externa sugiere una temperatura baja para mayor determinismo.

V0 no la cambia.

Motivo:

```text
structured-output enforcement
should be isolated from
sampling-policy change
```

Esto preserva causalidad frente a los U01 previos.

Cualquier futura política de sampling requiere otro gate.

## 14. E4 / Engineering Propose

E4 presenta el mismo patrón general:

```text
prompt says strict JSON
-> strict parser
-> no runtime structured-output contract
```

Pero V0 NO cambia Propose todavía.

Decisión:

```text
build reusable primitive now
apply only to Analyze first
validate in tests + real bounded run
then decide a separate E4 slice
```

Esto evita mezclar dos componentes cognitivos en el mismo experimento.

## 15. Cambios previstos — Slice A solamente

Archivos de implementación esperados:

```text
src/malak/core/conversation.py
src/malak/runtime/ollama_runtime.py
src/malak/runtime/mock_llm_runtime.py
src/malak/capabilities/_engineering_analysis.py
tests/test_conversation*.py or existing core request tests
tests/test_ollama_runtime.py
tests/test_engineering_analyze.py
tests/test_internal_interaction_test_v0_harness.py
```

`ConversationService` debería requerir:

```text
code delta: ideally 0
```

porque `dataclasses.replace()` preserva los demás campos del request.

Kernel / Planner / Request de Malāk:

```text
delta 0
```

## 16. Contrato de ConversationRequest

Propuesta:

```text
response_json_schema: str | None = None
```

Validaciones mínimas en el value boundary:

```text
None
OR
non-empty trimmed UTF-8 string
within explicit hard byte limit
strict JSON parse
root must be object
```

No se implementa un JSON Schema validator completo dentro de Core.

Motivo:

```text
Malāk validates its own static schema by tests
provider validates/uses provider-native schema mechanics
full JSON Schema meta-validation here
= unnecessary scope / dependency
```

## 17. OllamaRuntime mapping

Cuando `response_json_schema` está presente:

```text
schema_object = strict json.loads(response_json_schema)
payload["format"] = schema_object
```

Cuando no está presente:

```text
payload remains backward compatible
format key absent
```

No se usa:

```text
format="json"
```

para E3 porque un schema explícito ofrece una restricción estructural más fuerte.

## 18. Provenance

Este slice no redefine Model Provenance.

El Structured Output contract es parte del código congelado por:

```text
baseline_commit
```

No se agrega en V0:

```text
response_schema artifact
response_schema digest
new provenance strength
served-response attestation
```

Una futura necesidad de comparar schemas independientemente del baseline debe
pasar por otro gate.

## 19. Trace / diagnostics

No cambia Trace schema.

No se persiste respuesta raw.

Si el provider/runtime falla al aplicar schema:

```text
existing component failure path
-> component_error
-> SafeDiagnosticEnvelope
```

Si el modelo entrega JSON estructuralmente aceptable pero semánticamente inválido:

```text
existing E3 parser/validator failure
-> component_error
-> SafeDiagnosticEnvelope
```

## 20. RED candidate esperado

RED debe demostrar al menos:

```text
S01 ConversationRequest has no structured-output contract
S02 Ollama request does not send format schema
S03 Analyze does not attach response schema
S04 unconstrained non-JSON model response reaches parser and fails
S05 generic requests remain unchanged when no schema is present
S06 provider/runtime must not silently ignore an explicitly requested schema
S07 MockLLMRuntime explicitly fails closed when schema is requested
```

El RED no ejecuta el modelo real.

## 21. GREEN acceptance

GREEN Slice A debe probar:

```text
G01 canonical schema contract is immutable
G02 invalid/non-object schema fails closed
G03 schema is byte bounded
G04 ConversationService preserves schema through context replace
G05 Ollama /api/chat receives format object only when requested
G06 generic Ollama request remains byte-for-byte semantically unchanged otherwise
G07 Analyze always requests its static schema
G08 Analyze valid structured JSON still passes existing parser
G09 semantically invalid structured JSON still fails existing parser
G10 no fence stripping / repair / retry introduced
G11 no raw model response persistence introduced
G12 no generation temperature/options change
G13 E4 remains unchanged in this slice
G14 Kernel / Planner / Request delta 0
G15 existing suite PASS Ubuntu + Windows
G16 MockLLMRuntime fails closed instead of pretending structured-output support
```

## 22. E2E / conformance

Candidate-bound E2E debe demostrar:

```text
Analyze
-> ConversationRequest.response_json_schema present
-> OllamaRuntime payload format == parsed schema object
-> response.content
-> existing parse_engineering_analysis
-> normal grounded envelope
```

Y también:

```text
ordinary conversation
-> response_json_schema None
-> no format field
-> behavior unchanged

Mock runtime + schema request
-> explicit failure
-> no silent ignore
```

No se ejecuta Fourth U01 durante implementation validation.

## 23. FULL 4R

### Risk

Objetivo:

```text
reduce malformed-machine-output risk
without relaxing semantic validation
```

Riesgos a vigilar:

- schema accidentally replaces semantic validation;
- provider silently ignores schema;
- mutable schema object;
- unintended sampling changes;
- provider-specific field leaking into Engineering;
- overclaim that schema guarantees correctness.

### Readability

Debe quedar visible:

```text
Capability declares desired response contract
Provider maps it
Parser validates actual semantic contract
```

### Reliability

Debe preservar:

```text
fail closed
strict parser
same baseline binding
same evidence contracts
same authority none
same no-retry policy
```

### Resilience

Si schema support falla:

```text
STOP
!= fallback to unconstrained output
```

## 24. 4 preguntas de ley

### Blueprint

No se introduce lógica de provider en Kernel ni en Engineering.

### Cognitive Constitution

El schema mejora forma de salida, no verdad, evidencia ni autoridad.

### Governance Constitution

No concede escritura, ejecución adicional, auto-retry, auto-fix ni merge.

### Kernel complexity

```text
Kernel delta 0
Planner delta 0
Request routing delta 0
```

## 25. RDD

Orden propuesto:

```text
G0/G1 design
-> Owner review
-> RED authorization
-> RED exact candidate
-> validation
-> GREEN authorization
-> GREEN exact candidate
-> candidate-bound CI
-> FULL 4R
-> E2E/conformance
-> Owner review/merge
-> separate runtime admission
-> Fourth U01 only if explicitly authorized
```

## 26. Alcance congelado

IN:

```text
provider-neutral JSON Schema request contract
Ollama structured-output mapping
Engineering Analyze adoption
tests
docs
```

OUT:

```text
Engineering Propose adoption
temperature policy
automatic retry
output repair
raw response persistence
model change
evidence changes
Kernel changes
Planner changes
Memory changes
Knowledge mutation
self-modification
runtime U01 execution
```

## 27. G0 disposition

```text
Third U01 failure cause isolated          PASS
existing strict parser should remain      PASS
provider-native structured output exists  PASS
provider-neutral insertion point exists   PASS
bounded implementation path exists        PASS
authority expansion                       0
runtime execution                         NOT AUTHORIZED

G0 RESULT:
PASS
```

## 28. Current authority state

```text
design review                    AUTHORIZED
implementation                   NOT AUTHORIZED
RED                              NOT AUTHORIZED
GREEN                            NOT AUTHORIZED
Fourth U01                       NOT AUTHORIZED
self-modification                NOT AUTHORIZED
Ready / merge                    OWNER ONLY
authority_effect                 none
```

Siguiente gate:

```text
Owner review of this design
-> explicit RED authorization
```


## 29. Post-validation design review hardening

Validation #547 sobre el candidate documental inicial:

```text
44c0e5c3768acf5a07fd41a60011cf92b305f087

Ubuntu:  1535 passed
Windows: 1535 passed
```

La revisión posterior detectó una ambigüedad de contrato antes de autorizar RED.

### 29.1 MockLLMRuntime

Malāk posee dos runtimes in-tree:

```text
OllamaRuntime
MockLLMRuntime
```

Agregar `response_json_schema` al request sin modificar Mock podría permitir:

```text
schema requested
-> Mock ignores field
-> response returned anyway
```

Eso contradice:

```text
explicit structured-output request
must not be silently ignored
```

Por tanto el diseño se endurece:

```text
OllamaRuntime
-> enforce via provider-native format

MockLLMRuntime
-> reject explicit schema request
```

No se introduce negotiation framework.

### 29.2 Provider-native constraint is not semantic authority

Incluso cuando Ollama acepta `format=<schema>`, Malāk no debe interpretar eso
como prueba de cumplimiento semántico o como una attestation del output.

Regla preservada:

```text
provider-native structured constraint
-> best-effort structural enforcement at generation boundary

actual response
-> MUST still pass strict Malāk parser + semantic validators
```

Si un backend/model devuelve contenido no conforme pese al schema:

```text
existing parser fails
-> component_error
-> diagnostic
-> INCONCLUSIVE
-> STOP
```

No existe fallback a unconstrained generation.

### 29.3 Scope effect

```text
additional production file in expected scope:
src/malak/runtime/mock_llm_runtime.py

Kernel delta          0
Planner delta         0
Request routing delta 0
authority expansion   0
runtime execution     NOT AUTHORIZED
Fourth U01            NOT AUTHORIZED
```


## 30. RED authorization checkpoint

El Owner autorizó explícitamente RED el 2026-09-25.

Alcance autorizado:

```text
tests only
+
documentation of RED evidence
```

No autorizado:

```text
production implementation
GREEN
Fourth U01
runtime execution
self-modification
```

Baseline RED:

```text
main@d48987b93c46bd192fea10ca4744d96156e53f07
```

RED debe aislar exactamente:

```text
S01 ConversationRequest lacks response_json_schema
S02 OllamaRuntime does not map requested schema to /api/chat format
S03 Engineering Analyze does not attach a response schema
S04 malformed model JSON reaches the existing strict parser and fails closed
S05 ordinary Ollama requests remain without format
S06 RuntimeConversationProvider must not hide unsupported schema behavior
S07 MockLLMRuntime must fail closed when schema is explicitly requested
```

Expected RED properties:

```text
new contract tests fail only where functionality is intentionally absent
existing unrelated suite remains green
no production file changed
Kernel / Planner / Request delta 0
authority_effect none
```


## 31. GREEN authorization checkpoint

Después de Validation #550, RED quedó demostrado sobre:

```text
candidate:
6d113047f3413c0d56f00116b3a529d2d3b32c35

Ubuntu:  5 failed / 1537 passed
Windows: 5 failed / 1537 passed
```

Fallas nuevas exactas:

```text
S01 ConversationRequest lacks response_json_schema
S02 OllamaRuntime lacks format mapping
S03 Analyze lacks response schema
S06 runtime provider path does not surface unsupported schema
S07 MockLLMRuntime does not fail closed
```

Controles:

```text
S04 strict parser malformed JSON rejection   PASS
S05 generic Ollama request has no format     PASS
```

El Owner autorizó GREEN dentro del scope congelado.

Producción autorizada:

```text
src/malak/core/conversation.py
src/malak/runtime/ollama_runtime.py
src/malak/runtime/mock_llm_runtime.py
src/malak/capabilities/_engineering_analysis.py
```

Tests/documentación asociados también están autorizados.

No autorizado:

```text
Engineering Propose structured-output adoption
temperature / sampling changes
retry / repair
raw response persistence
Kernel / Planner changes
Fourth U01
runtime execution
self-modification
```

La implementación debe preservar:

```text
provider-neutral request contract
Ollama format mapping
Mock fail-closed
strict semantic parser
generic request backward compatibility
authority_effect none
```


## 32. FULL 4R / anti-relaxation correction after Validation #559

Validation #559 sobre el candidate previo:

```text
dd2dabf124f4bd11ff45cab6f4b894a536fa8143

Ubuntu:  1553 passed
Windows: 1553 passed
```

La revisión posterior no se limitó a "tests verdes". Se comparó el candidate con
el baseline y se verificó:

```text
prior test assertions removed       0
prior pytest.raises removed         0
strict parser relaxations           0
retry / repair paths added          0
raw response persistence added      0
sampling changes                    0
Kernel / Planner delta              0
authority expansion                 0
```

### 32.1 Ambigüedad encontrada: shared analysis path

`run_engineering_analysis()` es compartido por:

```text
EngineeringAnalyzeCapability (E3)
EngineeringProposeCapability (E4 internal analysis phase)
```

El primer GREEN candidate adjuntaba `ANALYZE_RESPONSE_JSON_SCHEMA`
directamente dentro del helper compartido.

Consecuencia no deseada:

```text
E3 Analyze
-> structured output

E4 internal analysis
-> structured output también
```

Eso contradecía el scope congelado:

```text
apply only to Analyze first
E4 remains unchanged in this slice
```

Aunque todos los tests pasaban, el comportamiento ampliaba silenciosamente el
scope funcional.

### 32.2 Corrección fail-closed de scope

El helper compartido pasa a recibir:

```text
response_json_schema: str | None = None
```

y no decide política por sí mismo.

`EngineeringAnalyzeCapability` declara explícitamente:

```text
response_json_schema=ANALYZE_RESPONSE_JSON_SCHEMA
```

`EngineeringProposeCapability` no solicita schema:

```text
E4 analysis request   response_json_schema=None
E4 proposal request   response_json_schema=None
```

Test contractual:

```text
G13
all E4 requests remain unconstrained in this slice
```

Esto cierra la ambigüedad entre:

```text
shared implementation utility
!=
policy owner
```

La Capability que necesita structured output debe declararlo explícitamente.

### 32.3 Anti-relaxation disposition

```text
semantic parser                  unchanged
E3 invalid JSON rejection        preserved
E3 extra fields rejection        preserved
E3 unknown classification        preserved
E3 unknown refs                  preserved
E3 duplicate refs/keys           preserved
generic Ollama request           unchanged
Mock unsupported schema          fail closed
E4                               unchanged
Kernel / Planner                 delta 0
authority_effect                 none
Fourth U01                       NOT AUTHORIZED
```

El candidate posterior a esta corrección requiere nueva Validation candidate-bound
antes de cerrar FULL 4R / E2E.
