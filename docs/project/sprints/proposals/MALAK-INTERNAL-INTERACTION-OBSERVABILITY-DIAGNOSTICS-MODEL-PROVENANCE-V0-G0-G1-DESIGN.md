---
title: Malāk Internal Interaction Observability, Diagnostics & Model Provenance V0 — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation_design
language: es
created: 2026-09-24
baseline_commit: 2fed4a8e3009ac890d0aff287640d12fb645a32b
g0_result: pass
design_authorized_by: owner
design_authorized_at: 2026-09-24
risk_class: 3
critical_contract: true
red_authorized: false
implementation_authorized: false
runtime_execution_authorized: false
third_u01_execution_authorized: false
runtime_delta: 0
authority_effect: none
rdd_stage_2_authorized: false
related:
  - docs/project/sprints/proposals/MALAK-INTERNAL-INTERACTION-TRACE-V0-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-LIVE-REPLAY-VISUAL-PROJECTION-V0-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-INTERNAL-INTERACTION-TEST-V0-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-GOVERNED-ENGINEERING-EVIDENCE-FOCUS-V0-G0-G1-DESIGN.md
  - docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md
  - docs/development/malak_construction_protocol.md
  - src/malak/app/internal_interaction.py
  - src/malak/observability/execution_trace.py
  - src/malak/observability/execution_trace_projection.py
  - src/malak/app/trace_view.py
  - src/malak/runtime/ollama_runtime.py
---

# Malāk Internal Interaction Observability, Diagnostics & Model Provenance V0 — G0/G1 Design

## 1. Propósito

Cerrar tres observaciones abiertas del primer Self-Review real sin mezclar
responsabilidades ni debilitar la trazabilidad existente:

```text
OBS-01
-> durante una llamada larga al LLM el Owner no puede saber si Malāk sigue activo

OBS-02
-> component_error preserva la clase categórica del fallo
-> pero descarta la causa técnica útil para diagnóstico

MODEL-TRACE
-> el run identifica runtime/model por nombre
-> pero no congela una identidad suficiente para comparar capacidad del modelo
   de forma independiente del retrieval / evidence set
```

Objetivo general:

```text
live liveness
+ safe technical diagnosis
+ reproducible model identity
!= authority
!= private chain-of-thought
!= autonomous recovery
```

Este documento diseña el contrato completo, pero la implementación futura deberá
dividirse en slices separados para preservar causalidad.

## 2. Baseline G0

Baseline exacto:

```text
repository: Aranwill/jarvis
branch: main
baseline: 2fed4a8e3009ac890d0aff287640d12fb645a32b
open PRs observed before admission: none
permanent remote branch observed: main
```

Estado integrado relevante:

```text
Internal Interaction Trace V0                 INTEGRATED
Live / Replay Visual Projection V0            INTEGRATED
Internal Interaction Test V0                  INTEGRATED
Governed Engineering Evidence Focus V0        INTEGRATED
EVID-01 / EVID-02                             CLOSED AT IMPLEMENTATION LEVEL

OBS-01 heartbeat / elapsed                    OPEN
OBS-02 component_error diagnostic cause       OPEN
Model provenance beyond model string          OPEN

third real U01                                BLOCKED
```

G0 no reabre la auditoría integral ni el diseño de Evidence Focus.

## 3. Hechos del baseline

### 3.1 Trace

`ExecutionTraceEvent` conserva hoy:

```text
schema
run_id
sequence
occurred_at
baseline_commit
task_id
phase
component
event_type
input_refs
output_refs
evidence_refs
outcome
reason_code
authority_effect
```

`reason_code=component_error` clasifica correctamente el fallo, pero no explica
su causa técnica.

El contrato actual ya prohíbe mensajes de excepción crudos como reason codes.

### 3.2 Projection

La proyección ya calcula:

```text
started_at
completed_at
duration_ms
status
reason_code
```

Por tanto el problema OBS-01 no es falta de timestamps.

El problema es que `LiveTraceTextView` sólo vuelve a renderizar cuando llega un
nuevo evento. Durante una llamada síncrona larga al LLM no llega ningún evento
intermedio.

### 3.3 Component exceptions

`InternalInteractionRunner` usa actualmente caminos equivalentes a:

```python
try:
    ...
except Exception:
    reason_code = "component_error"
```

La excepción se descarta.

En cambio, errores de envelope controlados ya conservan un reason code específico.

### 3.4 Runtime/model

El run conserva hoy:

```text
runtime_name
model
```

`OllamaRuntime` conserva además métricas de la última respuesta exitosa:

```text
model
total duration
load duration
prompt eval count/duration
eval count/duration
tokens per second derivable
```

Pero el run no congela:

```text
model digest
runtime/Ollama version
declared context metadata
runtime configuration
per-run provenance status
```

Por eso:

```text
same model tag
!= proven same model artifact
```

## 4. Decisión de arquitectura

No se crea un Observability Manager, Agent, Scheduler, Memory, DB ni Event Bus.

Se adoptan tres contratos acotados:

```text
A. Live Elapsed Overlay
B. Safe Diagnostic Envelope
C. Runtime / Model Provenance Snapshot
```

Integración conceptual:

```text
ExecutionTrace
      │
      ├── material state ───────────────> LIVE projection
      │                                  REPLAY projection
      │
      ├── RUNNING node ────────────────> live-only elapsed refresh
      │                                  no new trace event
      │
      ├── COMPONENT_FAILED ────────────> safe diagnostic summary
      │                                  + diagnostic artifact
      │
      └── run identity ────────────────> runtime/model provenance artifact
```

## 5. Regla central: material trace vs live liveness

OBS-01 NO debe introducir eventos falsos sólo para refrescar la pantalla.

Se preserva:

```text
material execution fact
-> persisted trace event

mere passage of time while RUNNING
-> live visual refresh only
-> no authority
-> no new execution fact
```

Por tanto:

```text
heartbeat tick
!= progress
heartbeat tick
!= model token progress
heartbeat tick
!= evidence progress
heartbeat tick
!= new trace event
```

## 6. Slice A — Live Elapsed Overlay / OBS-01

### 6.1 Objetivo

Mientras un nodo material esté `RUNNING`, mostrar que el proceso sigue activo y
cuánto tiempo observable ha transcurrido.

Ejemplo:

```text
[>>] Inspect   RUNNING   elapsed=18.4s
```

Sin:

```text
42%
ETA 15s
tokens 800/2000
"almost done"
```

salvo que una futura fuente real entregue esos datos y exista otro gate.

### 6.2 Fuente de verdad

El overlay utiliza únicamente:

```text
projection node.status == RUNNING
projection node.started_at
monotonic local clock for display elapsed
```

No modifica:

```text
ExecutionTraceEvent
trace.jsonl
sequence
component outcome
terminal disposition
```

### 6.3 LIVE == REPLAY

Se preserva materialmente:

```text
LIVE final material projection
==
REPLAY projection from trace.jsonl
```

No se exige:

```text
every transient terminal redraw during LIVE
==
historical replay frame stream
```

El elapsed vivo es un overlay efímero.

Al completar/fallar el nodo:

```text
live elapsed overlay stops
final duration_ms
-> comes from persisted start/end events
-> remains replayable
```

### 6.4 Concurrencia

La llamada Engineering/LLM no debe moverse a otro thread sólo para habilitar
heartbeat.

Diseño preferido:

```text
main execution thread
-> remains unchanged

small live-view ticker
-> read-only projection snapshot
-> periodic render only
-> no trace mutation
-> no capability invocation
-> no repository access
```

El ticker debe:

- poder detenerse determinísticamente;
- no sobrevivir al run;
- no bloquear STOP;
- no escribir artefactos;
- no ocultar excepciones;
- no convertirse en scheduler general;
- serializar output para evitar frames corruptos.

## 7. Slice B — Safe Diagnostic Envelope / OBS-02

### 7.1 Principio

Se conserva:

```text
reason_code = stable categorical contract
```

y se agrega una capa distinta:

```text
diagnostic = bounded technical observation
```

Nunca:

```text
reason_code = raw str(exception)
```

### 7.2 Contrato conceptual

```text
SafeDiagnosticEnvelope
├─ schema
├─ diagnostic_id
├─ diagnostic_fingerprint
├─ run_id
├─ baseline_commit
├─ task_id
├─ phase
├─ component
├─ reason_code
├─ exception_type
├─ cause_chain_types
├─ safe_summary
├─ origin_scope
├─ repo_relative_file
├─ function
├─ line
└─ authority_effect = none
```

### 7.3 diagnostic_id

Debe ser run-local, path-safe y no semántico.

Ejemplo conceptual:

```text
D0001
D0002
```

No contiene secretos, mensajes del modelo ni paths locales.

### 7.4 diagnostic_fingerprint

Objetivo:

```text
"¿es materialmente el mismo tipo de fallo técnico?"
```

Se deriva de representación canónica de campos seguros, por ejemplo:

```text
component
reason_code
exception_type
cause_chain_types
origin_scope
repo_relative_file
function
```

No incluye:

```text
raw exception message
absolute local path
prompt
response
secret
URL
timestamp
diagnostic_id
```

### 7.5 Origen

Si el traceback contiene un frame dentro del repository root:

```text
origin_scope = repository
repo_relative_file = src/malak/...
function = ...
line = positive integer
```

Si la causa material sólo puede ubicarse fuera del repo:

```text
origin_scope = external
repo_relative_file = null
function = null or safe library function name
line = null
```

Nunca se persiste una ruta absoluta local.

### 7.6 safe_summary

No usa `str(exc)` por defecto.

Se deriva de una clasificación cerrada y sanitizada.

Ejemplos:

```text
TimeoutError
-> operation timed out

HTTP/network cause
-> runtime dependency request failed

ValueError
-> component rejected invalid value

unknown
-> component raised an unexpected exception
```

Una causa específica sólo puede mostrarse si proviene de un contrato de mensaje
seguro explícitamente marcado como tal.

### 7.7 Cause chain

Puede conservar nombres de tipos:

```text
RuntimeError <- TimeoutError
```

No conserva:

- traceback textual;
- locals;
- argumentos de excepción;
- request body;
- prompt;
- model output;
- headers;
- tokens/secrets;
- variables de entorno.

### 7.8 Persistencia

Se agrega un artefacto exacto:

```text
diagnostics.jsonl
```

Siempre existe, aunque esté vacío.

Cada `COMPONENT_FAILED` por excepción debe producir:

```text
reason_code = component_error
diagnostic artifact entry
diagnostic ref visible from failure path
```

El artifact debe entrar en el set atestado del run.

### 7.9 Trace compatibility

Diseño preferido V0:

```text
preserve ExecutionTraceEvent schema if possible
use output_refs to declare diagnostic:<id>
```

Ejemplo:

```text
COMPONENT_FAILED
output_refs = ("diagnostic:D0001",)
reason_code = component_error
```

Así:

- el trace sigue siendo materialmente reconstruible;
- el failure puede producir evidencia diagnóstica;
- no se agregan payloads arbitrarios al event stream.

Si RED demuestra que esto no permite una UX suficientemente segura y
replayable, cualquier cambio de schema del trace requiere STOP y nuevo gate.

### 7.10 Visual mínima

El árbol principal puede mostrar:

```text
[!!] Analyze (component_error) diagnostic=D0001
```

La inspección detallada debe poder mostrar sólo metadata sanitizada:

```text
diagnostic_id: D0001
type: TimeoutError
summary: operation timed out
origin: src/malak/runtime/ollama_runtime.py:<line>
function: generate
fingerprint: <sha256>
authority_effect: none
```

No se imprime traceback crudo.

## 8. Slice C — Runtime / Model Provenance Snapshot

### 8.1 Objetivo

Separar cuatro causas que hoy pueden confundirse:

```text
intent interpretation problem
!= evidence retrieval/completeness problem
!= model reasoning/capability problem
!= governance stop
```

### 8.2 Contrato conceptual

```text
RuntimeModelProvenance
├─ schema
├─ captured_at
├─ runtime_class
├─ provider
├─ requested_model
├─ resolved_model
├─ model_digest
├─ model_identity_strength
├─ runtime_version
├─ declared_context_window
├─ context_window_source
├─ generation_options
├─ timeout_seconds
├─ keep_alive
├─ max_request_bytes
├─ max_response_bytes
├─ provenance_status
└─ authority_effect = none
```

### 8.3 Identidad de modelo

Estados mínimos:

```text
DIGEST_BOUND
TAG_ONLY
UNAVAILABLE
```

Reglas:

```text
requested tag only
!= exact reproducible model identity

digest known
-> DIGEST_BOUND

tag known but digest unavailable
-> TAG_ONLY

model cannot be resolved locally
-> UNAVAILABLE
```

No se infiere digest desde el nombre.

### 8.4 Runtime introspection

La captura puede realizar consultas read-only al runtime local antes del run.

No constituye:

```text
external research
internet access
model execution
tool authority
model update
model pull
model deletion
```

Quedan prohibidos en este gate:

```text
pull model
update model
delete model
change model
change Modelfile
change runtime config automatically
```

### 8.5 Context window

Se registra como metadata declarada, no como uso real garantizado.

```text
declared_context_window
!= actual prompt tokens consumed
!= available free context
```

Si el runtime no permite resolverla de forma no ambigua:

```text
declared_context_window = null
context_window_source = unavailable
```

No se inventa ni estima.

### 8.6 Generation parameters

Se registra únicamente lo que Malāk fija explícitamente.

Si no se fijan temperature/top_p/seed/num_ctx u otros options:

```text
generation_options = {}
```

Eso significa:

```text
Malāk did not explicitly set generation options
```

y no:

```text
server/model defaults are proven identical
```

### 8.7 Runtime metrics

Las métricas ya disponibles pueden preservarse por llamada cuando sea viable:

```text
resolved response model
total_duration
load_duration
prompt_eval_count
prompt_eval_duration
eval_count
eval_duration
tokens_per_second derived
```

Estas métricas son telemetría.

```text
metrics != evaluation
metrics != benchmark verdict
metrics != authority
```

La incorporación de métricas per-call podrá vivir en el mismo artifact de
provenance o en un JSONL separado si RED demuestra que el cardinality contract lo
requiere.

### 8.8 Evidence binding

El run ya conserva `evidence_set_digest` para el focus gobernado.

El benchmark futuro debe poder correlacionar:

```text
baseline_commit
focus_id
evidence_set_digest
runtime/model provenance
terminal outcome
runtime metrics
```

Así:

```text
same evidence set + same model digest
-> comparable execution conditions

different evidence set
-> not a clean model-capability comparison

different model digest
-> not the same model artifact
```

## 9. Artifact set propuesto

V0 del nuevo contrato propone:

```text
manifest.json
trace.jsonl
evidence.json
assessment.json
outcome.json
diagnostics.jsonl
runtime_provenance.json
attestation.json
```

`diagnostics.jsonl` y `runtime_provenance.json` deben incluirse en la
attestation.

No son:

```text
Memory
Knowledge
audit authority
candidate construction evidence
persistent learning
```

Son artefactos observacionales del run.

## 10. Third U01 admission

El tercer U01 permanece bloqueado durante diseño/RED/GREEN.

Antes de autorizarlo deben estar cerrados al menos:

```text
OBS-01 LIVE elapsed available
OBS-02 safe diagnostic preservation available
runtime/model provenance captured
Evidence Focus already integrated
candidate validation green
FULL 4R green
E2E green
RDD Stage 1 Candidate Conformance PASS
Owner explicit runtime authorization
```

Se recomienda para el tercer U01 exigir:

```text
model_identity_strength = DIGEST_BOUND
```

Si el runtime local no puede resolver digest:

```text
STOP
-> do not silently downgrade a benchmark-grade run to TAG_ONLY
```

Esto sólo aplica al Self-Review experimental que busca comparar capacidad con
trazabilidad fuerte; no redefine toda conversación genérica de Malāk.

## 11. Secuencia de implementación

El diseño es conjunto para congelar interfaces, pero los candidates deben
separarse:

```text
Slice A — OBS-01 Live Elapsed
    ↓ human merge
Slice B — OBS-02 Safe Diagnostics
    ↓ human merge
Slice C — Runtime / Model Provenance
    ↓ human merge
Third U01 admission review
```

Motivo:

```text
one failure
-> one causal surface

avoid changing liveness + errors + model identity in one GREEN
```

El Owner puede cambiar este orden explícitamente.

## 12. Candidate surface budgets

### Slice A candidate files

```text
src/malak/app/trace_view.py
src/malak/app/internal_interaction_test_v0.py
tests/test_trace_view.py
tests/test_internal_interaction_test_v0_harness.py
```

STOP si requiere cambiar Kernel, Planner, ExecutionTrace schema o ejecutar
Engineering en worker threads.

### Slice B candidate files

```text
src/malak/app/internal_interaction.py
src/malak/observability/execution_trace.py       only if RED proves refs insufficient
src/malak/app/trace_view.py
new bounded diagnostics contract/helper if RED proves needed
tests/test_internal_interaction_v0.py
tests/test_execution_trace.py
tests/test_trace_view.py
```

Preferred path mantiene trace schema V0.

### Slice C candidate files

```text
src/malak/runtime/ollama_runtime.py
src/malak/app/internal_interaction.py
src/malak/app/internal_interaction_test_v0.py
bounded runtime provenance contract/helper if RED proves needed
tests/test_ollama_runtime.py
tests/test_internal_interaction_v0.py
tests/test_internal_interaction_test_v0_harness.py
```

No se modifica ConversationRequest para meter metadata de provenance.

## 13. Critical Contract Hardening

Interpretaciones materiales cerradas:

1. heartbeat no es progreso;
2. elapsed vivo no es trace event;
3. live overlay no altera material LIVE==REPLAY;
4. diagnostics no son chain-of-thought;
5. reason_code mantiene su semántica categórica;
6. raw exception text no entra por defecto a trace/artifacts;
7. absolute local paths no se persisten;
8. traceback textual no se persiste;
9. diagnostic origin no determina root cause arquitectónica;
10. exception type no equivale a finding;
11. diagnostic fingerprint no equivale a issue identity perfecta;
12. model tag no equivale a model digest;
13. declared context window no equivale a tokens usados;
14. metrics no equivalen a evaluación;
15. provenance no concede autoridad;
16. runtime introspection local no puede mutar Ollama/modelos;
17. missing model digest no se inventa;
18. third U01 no se autoautoriza al quedar GREEN.

Adversarial / fail-open:

```text
raw secret in exception             -> must not persist
absolute path                       -> strip / reject
traceback with prompt/local vars    -> never serialize
diagnostic unknown field            -> reject
unknown diagnostic schema           -> reject
duplicate diagnostic_id             -> reject
diagnostic run/baseline mismatch     -> reject
model digest malformed              -> provenance incomplete
runtime introspection mutation path -> forbidden
ticker cannot stop                  -> fail test / no admission
ticker modifies trace               -> reject
fake percentage/ETA                 -> reject
```

Known material ambiguity unresolved:

```text
0
```

## 14. Malāk Alignment Matrix

| Fuente | Clase | Intención/invariante | Baseline | Disposición | Efecto |
| --- | --- | --- | --- | --- | --- |
| Cognitive Constitution | normativa | evidencia e incertidumbre explícitas | trace/evidence existentes | ADOPT | diagnóstico y provenance verificables |
| Governance Constitution | normativa | usuario conserva control | authority_effect none | ADOPT | no auto-recovery ni auto-update |
| Blueprint | arquitectura | Kernel First / Capability First | Kernel desacoplado | ADOPT | Kernel delta 0 |
| SECURITY.md | protegida | minimizar disclosure / trust fuerte | raw exception no preservada | ADOPT | sanitización fail-closed |
| Internal Interaction Trace V0 | contrato integrado | reconstructible, no CoT | trace V0 activo | ADAPT | refs diagnósticos, schema preferentemente intacto |
| Live/Replay Projection V0 | contrato integrado | UI deriva de facts | final projection equality | ADAPT | overlay live separado |
| Internal Interaction Test V0 | contrato integrado | local/read-only/STOP | harness real | ADAPT | admission más observable |
| Runtime Metrics | implementación | telemetría no authority | Ollama metrics existentes | ADOPT | reutilizar métricas disponibles |
| current component catch paths | implementación | fail-safe | exception discarded | ADAPT | diagnostic envelope seguro |
| prior real run evidence | observacional | OBS-01/OBS-02 | runs 001/002 | ADOPT | causal input del gate |

Separación:

```text
observability != evaluation
diagnostic != root-cause finding
provenance != authority
telemetry != benchmark verdict
design PASS != RED authorization
```

## 15. Cuatro preguntas de ley

### Blueprint

PASS.

No se requiere Kernel ni Planner change.

### Cognitive Constitution

PASS.

Se preserva incertidumbre y se mejora provenance sin inventar causalidad.

### Governance Constitution

PASS.

No se habilita recuperación automática, cambio de modelo ni self-modification.

### Kernel complexity

PASS.

```text
Kernel planned delta  0
Planner planned delta 0
```

## 16. Design 4R

### Risk — PASS

Riesgos:

- disclosure desde exceptions;
- falsa sensación de progreso;
- races en live output;
- confundir telemetry con evaluación;
- model tag mutable;
- provenance parcial presentada como exacta.

Controles:

- diagnostic schema cerrado;
- no raw exception text;
- live-only elapsed;
- output serialization;
- identity strength explícita;
- fail-closed para benchmark-grade run.

### Readability — PASS

Tres contratos separados, con responsabilidad única:

```text
liveness
diagnostics
provenance
```

No se crea una capa general de observability orchestration.

### Reliability — PASS

- final duration proviene del trace;
- diagnostics quedan run/baseline-bound;
- model identity expone su strength;
- artifacts se atestan;
- unknown/missing no se normaliza.

### Resilience — PASS

- una excepción produce INCONCLUSIVE + diagnóstico seguro;
- una falla de provenance no cambia de modelo;
- ticker no participa en execution authority;
- STOP sigue siendo posible aunque una capability falle.

## 17. Security Horizon Check

Resultado:

```text
Prompt & Context Trust Boundary        ALREADY_COVERED + REINFORCED
data disclosure                        REQUIRES REINFORCEMENT -> diagnostic sanitizer
resource governance                    ALREADY_COVERED
external network                       NOT APPLICABLE
identity/delegation                    NOT APPLICABLE
Memory/Knowledge poisoning             NOT APPLICABLE
Protected Durable Write                NOT APPLICABLE
```

La nueva persistencia sigue limitada a runtime artifact local ignorado por Git.

## 18. RDD Stage 1 Design Check

```text
baseline identity strategy                 PASS
candidate identity strategy                PASS
evidence provenance                        PASS
Writer/Reviewer/Validator/Authority split  PASS
PASS|FAIL|INCONCLUSIVE discipline          PASS
candidate change invalidates evidence      PASS
bounded correction semantics               PASS
authority_effect                           none
RDD Stage 2                                NOT AUTHORIZED
```

Cada slice tendrá RED/GREEN y candidate identity propios.

## 19. RED requirements por slice

### Slice A / OBS-01

RED deberá demostrar:

```text
A01 RUNNING node can expose live elapsed without new trace event
A02 no percentage or ETA is rendered
A03 elapsed uses monotonic display clock
A04 ticker stops on completed/failed/skipped
A05 ticker cannot outlive run teardown
A06 final duration remains trace-derived
A07 LIVE final material projection == REPLAY
A08 trace event count unchanged by elapsed refresh
A09 no Kernel/Planner delta
A10 authority_effect none
```

### Slice B / OBS-02

RED deberá demostrar:

```text
B01 component exception creates safe diagnostic
B02 reason_code remains component_error
B03 raw str(exc) not persisted by default
B04 raw traceback not persisted
B05 absolute paths not persisted
B06 repo-relative origin preserved when available
B07 external origin does not leak local path
B08 cause chain preserves types only
B09 diagnostic_id unique in run
B10 diagnostic fingerprint deterministic for same safe inputs
B11 diagnostics artifact run/baseline bound
B12 diagnostics artifact included in attestation
B13 failed component visibly exposes diagnostic ref
B14 malformed diagnostic fails closed
B15 no prompts/responses/secrets in diagnostic schema
B16 authority_effect none
```

### Slice C / Model Provenance

RED deberá demostrar:

```text
C01 requested model recorded
C02 resolved local model recorded
C03 valid digest -> DIGEST_BOUND
C04 missing digest -> TAG_ONLY/UNAVAILABLE, never fabricated
C05 runtime version recorded when available
C06 context metadata explicit as declared, not actual-use claim
C07 no implicit generation options invented
C08 timeout/keep_alive/byte limits recorded from runtime config
C09 runtime introspection is read-only
C10 provenance artifact run/baseline bound
C11 provenance artifact included in attestation
C12 same evidence_set_digest remains independently visible
C13 metrics remain telemetry only
C14 no model update/pull/delete path
C15 benchmark-grade self-review rejects non-DIGEST_BOUND identity
C16 authority_effect none
```

## 20. E2E futuro

Después de GREEN de los tres slices:

```text
real local Ollama
exact baseline
exact focus evidence digest
DIGEST_BOUND model identity
LIVE elapsed visible during long call
controlled synthetic component failure path test
safe diagnostic replay/inspection
artifacts + attestation
LIVE final projection == REPLAY
tracked tree clean
STOP
```

No se usa un fallo real destructivo para probar diagnostics; el E2E de error debe
ser controlado/determinista.

## 21. Stop conditions

STOP si:

- se necesita mover Engineering a worker threads para heartbeat;
- se necesita capturar raw traceback;
- se necesita persistir prompt/model output para diagnosticar;
- se necesita modificar Kernel/Planner;
- se necesita cambiar ConversationRequest para este gate;
- se necesita introducir scheduler/event bus;
- se necesita red externa;
- se propone cambiar/actualizar el modelo durante provenance capture;
- no puede distinguirse model tag de digest;
- un overlay live modifica trace material;
- diagnostics adquieren semántica de authority;
- se intenta ejecutar third U01 antes de runtime admission.

## 22. Rollback

Cada slice debe poder revertirse independientemente.

```text
Slice A rollback
-> current event-driven live view

Slice B rollback
-> generic component_error fail-safe semantics

Slice C rollback
-> current runtime_name + model identity fields
```

La reversión no puede alterar evidencia histórica de runs anteriores.

## 23. G0/G1 disposition

```text
G0                                  PASS
G1                                  PASS
Critical Contract Hardening         PASS
Four law questions                  PASS
Design 4R                           PASS
Security Horizon Check              PASS
RDD Stage 1 Design Check            PASS
known material ambiguity            0

RED Slice A                         NOT GRANTED
RED Slice B                         NOT GRANTED
RED Slice C                         NOT GRANTED
implementation authorization        NOT GRANTED
runtime execution authorization     NOT GRANTED
third real U01 execution            BLOCKED
authority_effect                    none
runtime delta                       0
```

Siguiente gate permitido tras revisión/merge humano de este diseño:

```text
Owner explicit RED authorization for Slice A / OBS-01
-> RED tests only
-> candidate-bound evidence
-> STOP
```
