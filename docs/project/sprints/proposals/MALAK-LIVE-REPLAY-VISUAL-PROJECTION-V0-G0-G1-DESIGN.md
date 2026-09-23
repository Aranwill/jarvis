---
title: Malāk Live / Replay Visual Projection V0 — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation_design
language: es
created: 2026-09-23
baseline_commit: 0424cfeca7ca16fa59649b9bdfbe45f739030c25
g0_result: pass
g0_ledger: docs/project/sprints/proposals/MALAK-LIVE-REPLAY-VISUAL-PROJECTION-V0-G0-COVERAGE-LEDGER.md
design_authorized_by: owner
design_authorized_at: 2026-09-23
risk_class: 2
critical_contract: false
red_authorized: true
red_authorized_by: owner
red_authorized_at: 2026-09-23
implementation_authorized: false
execution_authorized: false
runtime_delta: 0
authority_effect: none
related:
  - docs/project/sprints/proposals/MALAK-INTERNAL-INTERACTION-TRACE-V0-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-E5-ENGINEERING-CLI-G0-G1-DESIGN.md
  - docs/development/malak_construction_protocol.md
---

# Malāk Live / Replay Visual Projection V0 — G0/G1 Design

## 1. Propósito

Agregar la mínima superficie visual necesaria para observar el recorrido interno
real de Malāk durante el primer Interaction Test V0 y reproducir posteriormente
el mismo recorrido desde `trace.jsonl`.

Pregunta de aceptación:

> ¿Puede una persona observar y reconstruir visualmente el flujo real de un run
> sin introducir una segunda fuente de estado, autoridad, razonamiento o
> arquitectura TUI?

V0 debe probar:

```text
same real trace
  ├─ LIVE projection
  └─ REPLAY projection

same material path
same node semantics
same evidence/reference metadata
no invented runtime state
```

## 2. Baseline G0

```text
repository                     Aranwill/jarvis
branch                         main
baseline                       0424cfeca7ca16fa59649b9bdfbe45f739030c25
tracked blobs discovered       292
tracked blobs classified       292
silently omitted               0
G0 RESULT                      PASS
```

Integrated baseline directly reused:

```text
ExecutionTraceEvent            INTEGRATED
ExecutionTrace                 INTEGRATED
LIVE event_sink                INTEGRATED
trace.jsonl persistence        INTEGRATED
trace replay                   INTEGRATED
component-path projection      INTEGRATED
InternalInteractionRunner      INTEGRATED
Self-Review Evidence Packet    INTEGRATED
CLI                            INTEGRATED
```

Gap:

```text
machine-observable trace       YES
human visual tree              NO
human replay view              NO
node inspection projection     NO
```

## 3. G0 decision

No se admite una TUI completa en este gate.

```text
dependency-free tree projection     ADMIT
existing CLI as first surface       ADMIT
LIVE event-driven updates           ADMIT
REPLAY from exact runtime artifact  ADMIT
node metadata inspection            ADMIT

Textual/Rich/prompt_toolkit         REJECT for V0
panes / overlays / multi-window     DEFER to E5-D
mouse / interactive widgets         DEFER
full-screen terminal control        DEFER
new event bus                       REJECT
new runtime state store             REJECT
```

Razón:

la necesidad inmediata es verificar visualmente el recorrido del flujo del
primer test, no construir todavía la Terminal Adaptativa completa.

## 4. Critical-contract classification

V0 se clasifica:

```text
risk_class: 2
critical_contract: false
```

Justificación:

- no produce evidence;
- no valida evidence;
- no concede permission;
- no decide terminal disposition;
- no modifica candidate identity;
- no ejecuta side effects;
- sólo proyecta trace ya validado.

La proyección dejará de ser no-crítica si en el futuro una decisión automática,
gate o autorización depende de sus estados renderizados.

Aunque no sea critical contract, se aplica hardening explícito porque una vista
incorrecta podría inducir a error humano.

## 5. Fuente única de verdad

Regla obligatoria:

```text
ExecutionTraceEvent
      ↓
Trace Projection
      ↓
Renderer
      ↓
Human

never:

Renderer
  ↓
invented state
  ↓
runtime claim
```

La UI no consulta directamente:

- LLM outputs para inferir estados;
- repository state para inferir etapas;
- logs arbitrarios;
- Memory;
- Knowledge;
- agent state futuro;
- heurísticas textuales.

Sólo consume el contrato `ExecutionTraceEvent` ya integrado.

## 6. Projection Model V0

La proyección materializa un view model inmutable y derivado.

Campos mínimos por nodo:

```text
node_id
label
phase
component
status
started_at
completed_at
duration_ms
outcome
reason_code
input_refs
output_refs
evidence_refs
last_sequence
authority_effect
```

Estados visuales cerrados:

```text
NOT_OBSERVED
RUNNING
COMPLETED
SKIPPED
FAILED
INCONCLUSIVE
```

Regla importante:

```text
NOT_OBSERVED != WAITING
```

V0 no afirma que un componente esté esperando si no existe evento que lo
demuestre.

## 7. Canonical V0 tree

La proyección podrá presentar una estructura canónica para facilitar lectura:

```text
RUN
├─ Scope
├─ Evidence Packet
├─ Engineering
│  ├─ Inspect
│  ├─ Analyze
│  └─ Propose
├─ Terminal Disposition
├─ Artifact
└─ STOP
```

Los nodos canónicos pueden existir como slots de presentación, pero su estado
inicial debe ser exclusivamente:

```text
NOT_OBSERVED
```

Sólo un evento real puede mover un nodo a otro estado.

La existencia visual del slot:

```text
!= component executed
!= component required
!= component available
```

## 8. Event-to-node mapping

Mapping cerrado V0:

```text
RUN_STARTED
  -> run / RUNNING

SCOPE_FROZEN
  -> scope / COMPLETED

EVIDENCE_PACKET_STARTED
  -> evidence / RUNNING

EVIDENCE_PACKET_READY + SUCCEEDED
  -> evidence / COMPLETED

EVIDENCE_PACKET_READY + INCONCLUSIVE
  -> evidence / INCONCLUSIVE

COMPONENT_STARTED
  -> exact component / RUNNING

COMPONENT_COMPLETED
  -> exact component / COMPLETED

COMPONENT_SKIPPED
  -> exact component / SKIPPED

COMPONENT_FAILED
  -> exact component / FAILED

TERMINAL_DISPOSITION
  -> decision / COMPLETED

ARTIFACT_FINALIZED
  -> artifact / COMPLETED

RUN_STOPPED
  -> stop / COMPLETED
  -> run / COMPLETED
```

Unknown event type:

```text
impossible after valid ExecutionTraceEvent construction
but projection must still fail closed if fed non-contract input
```

## 9. Transition hardening

Un nodo no puede retroceder silenciosamente.

Ejemplos inválidos:

```text
COMPLETED -> RUNNING
FAILED    -> COMPLETED
SKIPPED   -> RUNNING
sequence N -> sequence <= N
component event after RUN_STOPPED
```

Resultado:

```text
projection update rejected
previous valid projection preserved
```

La proyección no corrige ni normaliza una traza inválida.

## 10. Duration semantics

Duración se deriva únicamente cuando existen timestamps observados suficientes.

```text
COMPONENT_STARTED at T1
COMPONENT_COMPLETED/FAILED at T2
-> duration_ms = T2 - T1
```

Si falta inicio:

```text
duration_ms = null
```

No se inventa cero ni duración aproximada.

`SKIPPED` no tiene duración salvo que una futura versión contractual la
demuestre.

## 11. Metadata visible

La vista resumen muestra sólo:

```text
node label
status
duration when known
outcome
reason_code when applicable
```

La inspección detallada puede mostrar:

```text
run_id
baseline_commit
task_id
phase
component
event sequence
timestamps
input_refs
output_refs
evidence_refs
authority_effect
```

V0 NO muestra por defecto:

- prompts;
- respuestas LLM completas;
- component outputs completos;
- secrets;
- stack traces;
- private chain-of-thought.

Los outputs operacionales consultables permanecen en los artefactos existentes,
no se duplican dentro del renderer.

## 12. Text renderer V0

V0 usa texto plano determinista y portable.

Ejemplo:

```text
MALAK INTERNAL INTERACTION — run-001
baseline 0424cfe...

[OK] RUN
 |-- [OK] Scope
 |-- [OK] Evidence Packet
 |-- Engineering
 |    |-- [OK] Inspect       142 ms
 |    |-- [>>] Analyze
 |    `-- [..] Propose      NOT_OBSERVED
 |-- [..] Terminal Disposition
 |-- [..] Artifact
 `-- [..] STOP
```

Tokens visuales V0:

```text
[..] NOT_OBSERVED
[>>] RUNNING
[OK] COMPLETED
[--] SKIPPED
[!!] FAILED
[??] INCONCLUSIVE
```

Se eligen tokens ASCII para máxima compatibilidad Windows/Linux.

Color ANSI:

```text
not required
not authoritative
may be deferred
```

## 13. LIVE projection

El `InternalInteractionRunner` ya acepta `event_sink`.

V0 reutiliza esa frontera:

```text
ExecutionTraceEvent
      ↓
ProjectionSink
      ↓
Projection state
      ↓
TextRenderer
      ↓
output_fn
```

El live sink:

- no bloquea ni modifica el runner;
- no modifica el evento;
- no devuelve autoridad;
- no puede cambiar terminal disposition;
- falla de forma controlada.

Política V0 ante renderer failure durante una ejecución futura:

```text
runtime trace remains source of truth
visual failure is reported
visual success must not be claimed
runner authority remains unchanged
```

La política exacta fail/continue del futuro wiring CLI se fijará en RED; este
gate no autoriza runtime self-review.

## 14. REPLAY projection

Replay usa exclusivamente:

```text
runtime/internal_interaction/<safe_run_id>/trace.jsonl
```

y la lectura contractual existente:

`read_execution_trace_jsonl()`.

No se permite path arbitrario desde input CLI.

```text
run_id
-> validated safe run id
-> fixed runtime root
-> trace.jsonl
```

La visualización replay no reejecuta LLM, Engineering ni Self-Review.

## 15. CLI surface V0

Namespace candidato:

```text
/trace
```

Comandos de lectura candidatos:

```text
/trace help
/trace replay <run_id>
/trace inspect <run_id> <node_id>
```

No se agrega en este gate:

```text
/trace run
/self-review run
/interaction run
```

porque eso autorizaría o expondría ejecución real, que sigue separada.

Cuando el primer Interaction Test V0 sea autorizado, el live renderer podrá
conectarse al `event_sink` ya diseñado sin cambiar el projection contract.

## 16. Node inspection

`inspect` no lee outputs cognitivos arbitrarios.

Devuelve el estado proyectado del nodo:

```text
node_id
status
phase
component
timestamps
duration
outcome
reason
input refs
output refs
evidence refs
sequence
authority_effect
```

Unknown node:

```text
controlled not-found result
!= fabricate NOT_OBSERVED node
```

Sólo los slots canónicos V0 pueden existir como `NOT_OBSERVED`.

## 17. LIVE / REPLAY equivalence

Para una misma secuencia válida de eventos:

```text
fold(live events)
==
fold(read(trace.jsonl))
```

en las siguientes propiedades materiales:

```text
node ids
node statuses
component path
terminal node states
reason codes
reference sets
last sequence
```

Los timestamps y duración deben coincidir cuando la fuente replay preserva los
mismos eventos exactos.

Renderer whitespace o encabezados no constituyen equivalencia material.

## 18. No segunda persistencia

La proyección puede vivir sólo en memoria durante LIVE.

No crea:

- DB;
- JSON projection cache;
- Memory;
- knowledge artifact;
- duplicate ledger.

Replay reconstruye la vista desde `trace.jsonl`.

```text
trace.jsonl = durable source
projection = disposable derived state
```

## 19. Application boundary

El candidato futuro debe ubicarse fuera de Kernel y Planner.

Responsabilidades:

```text
observability layer
  -> projection semantics

application/CLI layer
  -> rendering + human commands
```

Prohibido:

```text
Kernel imports renderer
Planner imports projection
capability imports CLI
trace contract imports UI
```

## 20. Malāk Alignment Matrix

| Fuente | Clase | Invariante/intención | Baseline | Disposición | Efecto |
| --- | --- | --- | --- | --- | --- |
| Cognitive Constitution | normativa | evidencia y límites explícitos; no falsa certeza | trace ya estructurado | ADOPT | distinguir NOT_OBSERVED de ejecutado |
| Governance Constitution | normativa | Human in Control; evidencia != autoridad | authority_effect none | ADOPT | renderer sin authority |
| Blueprint | arquitectura | capas y Kernel mínimo | UI/app boundary existente | ADOPT | cero Kernel/Planner delta |
| SECURITY.md | protegida | no secretos/CoT; observabilidad segura | trace usa reason codes | ADAPT | metadata segura por defecto |
| Architecture Quality Gates | arquitectura | evitar duplicación/overengineering | trace y CLI ya existen | ADOPT | reutilizar, no framework nuevo |
| Internal Interaction Trace V0 | design integrado | live/replay desde eventos reales | main@0424cfe | ADOPT | fuente única |
| E5 Engineering CLI | design integrado | terminal adaptativa progresiva | CLI actual | ADAPT | visual tree mínimo; E5-D diferido |
| ideas.md patrón terminal | no normativa | TUI como operational surface | intención preservada | ADAPT | superficie visual, no core dependency |
| Research Horizon EXT-22 | research input | presence projection útil; no copiar stack | preservado | ADAPT | propiedad sí, arquitectura no |
| pyproject.toml | baseline técnico | dependencies vacías | dependencies=[] | ADOPT | V0 dependency-free |
| current code/tests | implementado | event_sink + replay + CLI | disponible | ADOPT | mínima capa derivada |

Elementos diferidos/rechazados:

```text
Rich multi-window TUI        OBSERVE / DEFER
external TUI framework       REJECT V0
event bus nuevo              REJECT
dashboard web                REJECT
runtime execution command    DEFER
agent/task panels            DEFER
```

## 21. Cuatro preguntas de ley

### Blueprint

PASS.

La proyección vive en observability/application boundary.

### Cognitive Constitution

PASS.

No crea certeza a partir de ausencia de eventos y hace visibles estados
INCONCLUSIVE/FAILED/SKIPPED.

### Governance Constitution

PASS.

No concede ni representa authority distinta de `none`.

### Kernel complexity

PASS.

```text
Kernel planned delta  0
Planner planned delta 0
```

## 22. Design 4R

### Risk — PASS

Riesgos:

- estado visual inventado;
- renderer confundido con validación;
- exposición excesiva de outputs;
- path traversal en replay;
- divergencia LIVE/REPLAY;
- dependencia TUI innecesaria.

Controles: mapping cerrado, NOT_OBSERVED, safe run_id, fixed runtime root,
metadata mínima, equivalence test y cero dependencia.

### Readability — PASS

Separación:

```text
trace event
projection
renderer
CLI
```

sin managers ni framework.

### Reliability — PASS

Fold determinista sobre eventos ordenados y equivalencia LIVE/REPLAY.

### Resilience — PASS

Invalid transitions, invalid refs/path, corrupt replay o renderer error deben
ser visibles y fail-closed respecto de claims visuales.

## 23. RDD Stage 1 Design Check

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

## 24. RED candidate futuro

RED deberá cubrir como mínimo:

```text
canonical nodes start NOT_OBSERVED
real event advances exact node only
unknown/non-contract event rejected
invalid state regression rejected
post-STOP event rejected
duration derived only from observed start/end
SKIPPED has explicit reason
FAILED has explicit reason
INCONCLUSIVE visible
node inspect returns only projection metadata
unknown node does not fabricate state
ASCII render deterministic
LIVE fold == REPLAY fold
safe run_id enforced
replay cannot escape runtime root
corrupt trace fails closed
no dependency added
Kernel/Planner unchanged
CLI replay does not invoke LLM/runtime
```

No RED está autorizado aún.

## 25. GREEN futuro

GREEN debe implementar el mínimo necesario.

Candidate units posibles:

```text
ExecutionTraceProjection
ExecutionTraceProjectionNode
LiveTraceProjectionSink
PlainTextTraceRenderer
CLI /trace replay + inspect wiring
```

Los nombres exactos no son autoridad; RED determina el mínimo delta.

Prohibido en GREEN:

```text
Textual
Rich
prompt_toolkit
Typer
Click
full-screen terminal manager
multi-window layout
new event bus
database/cache
self-review execution command
Kernel/Planner changes
```

## 26. E2E futuro

Cadena replay:

```text
valid runtime artifact
-> trace.jsonl
-> contract reader
-> projection
-> renderer
-> human text tree
```

Cadena live equivalente:

```text
same ExecutionTraceEvents
-> live sink
-> projection
-> renderer
-> same material final tree
```

Debe demostrarse que ninguna ruta invoca modelos ni modifica el repositorio.

## 27. Stop conditions

STOP si:

- se requiere modificar Kernel o Planner;
- el renderer necesita inferir estado desde texto libre;
- hace falta una segunda persistencia;
- se intenta añadir ejecución real del Self-Review;
- una dependencia externa se vuelve necesaria sin admission separado;
- LIVE y REPLAY no pueden compartir exactamente el mismo projection contract;
- una visual failure puede alterar la decisión runtime.

## 28. G0/G1 disposition

```text
G0                                  PASS
G1                                  PASS
Four law questions                  PASS
Design 4R                           PASS
RDD Stage 1 Design Check            PASS
known material ambiguity            0

RED authorization                   GRANTED BY OWNER POST-PR #181
implementation authorization        NOT GRANTED
runtime self-review execution       NOT GRANTED
authority_effect                    none
runtime delta                       0
```

Post-merge admission:

```text
PR #181 merged by Owner
main after merge: 675121c3c3180c8436a6e436997247307b19207b
Owner continued the work
RED candidate: AUTHORIZED
GREEN / implementation: NOT AUTHORIZED
runtime self-review execution: NOT AUTHORIZED
```

Siguiente paso permitido:

```text
RED tests only
-> observe expected candidate-bound failure
-> Owner review / explicit GREEN authorization separately
```
