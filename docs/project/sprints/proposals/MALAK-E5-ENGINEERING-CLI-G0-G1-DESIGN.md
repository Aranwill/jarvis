---
title: Malāk E5 — Engineering CLI / Adaptive Terminal Foundation — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation design
language: es
created: 2026-09-19
baseline_commit: 5b6660eba9e5617a59c17d7380dd6822e8c193a4
vault_reconciliation_commit: c1d61e264113ec396760b39dc5e027252eefe2f7
g0_result: pass
g0_ledger: docs/project/sprints/proposals/MALAK-E5-G0-COVERAGE-LEDGER.md
design_authorized_by: owner
design_authorized_at: 2026-09-19
red_authorized: false
implementation_authorized: false
risk_class: 2
---

# Malāk E5 — Engineering CLI / Adaptive Terminal Foundation — G0/G1 Design

## 1. Propósito

Introducir la primera etapa gobernada de la Terminal Adaptativa de Malāk sin
crear una segunda arquitectura cognitiva, sin ampliar autoridad y sin adelantar
TUI, tasks, agents, tools o ejecución que todavía no existen en el baseline.

E5 no nace para reemplazar la CLI actual. Nace para convertirla en una superficie
humana coherente sobre capacidades que Malāk ya integró.

Pregunta de aceptación:

> ¿Puede Malāk exponer Conversation + Engineering Intelligence mediante una
> superficie CLI determinista, simple y trazable, conservando Kernel mínimo,
> Human in Control y exactamente las fronteras read-only de E2/E3/E4?

E5-A debe demostrar únicamente:

```text
human input
   ↓
deterministic CLI command parsing
   ↓
pre-composed Kernel boundary
   ↓
existing integrated Capability
   ↓
existing deterministic / grounded output
   ↓
human
```

Nunca:

```text
CLI
 ↓
new authority
 ↓
implicit execution
```

---

## 2. Baseline de admisión

```text
repository: Aranwill/jarvis
branch: main
baseline: 5b6660eba9e5617a59c17d7380dd6822e8c193a4

E0 — Repository Read            INTEGRATED
E1 — Governed Knowledge Read    INTEGRATED
E2 — Engineering Inspect        INTEGRATED
E3 — Engineering Analyze        INTEGRATED
E4 — Engineering Propose        INTEGRATED
D1 — E4 Current-State Reconciliation CLOSED

E5 — Engineering CLI            NOT AUTHORIZED before this design
```

Downstream reconciliado observado:

```text
Vault PR #126 — merged
Vault main:
c1d61e264113ec396760b39dc5e027252eefe2f7
```

No existían PR abiertas en `Aranwill/jarvis` al iniciar esta G0/G1.

El G0 exhaustivo correspondiente quedó registrado en:

```text
docs/project/sprints/proposals/MALAK-E5-G0-COVERAGE-LEDGER.md
```

Resultado:

```text
tracked files discovered = 258
tracked files classified = 258
silently omitted files   = 0
G0 RESULT                 = PASS
```

---

## 3. Cuatro preguntas de ley

### 3.1 ¿Respeta Blueprint?

Sí.

E5-A permanece en el borde de aplicación. Reutiliza Capabilities ya integradas y
no convierte UI, parser o CLI en componente cognitivo ni de autoridad.

### 3.2 ¿Respeta Constitución Cognitiva?

Sí.

El routing del comando es determinista, no probabilístico. E5-A no inventa
evidencia, no sustituye grounding y no altera los envelopes ni las reglas de
E2/E3/E4.

### 3.3 ¿Respeta Gobernanza?

Sí.

La terminal presenta intención y resultados. No concede permisos ni convierte
`proposal` en decisión, autorización o implementación.

### 3.4 ¿Hace al Kernel más simple o más complejo?

No modifica el Kernel.

E5-A debe reutilizar el patrón vigente de Kernel + Registry + Planner fijo en
composición. Si la implementación requiere aumentar responsabilidad del Kernel,
la admisión deja de ser válida y debe producir STOP.

Resultado:

```text
Blueprint              PASS
Cognitive Constitution PASS
Governance              PASS
Kernel complexity       NO DELTA
```

---

## 4. Necesidad demostrada

El baseline actual contiene una CLI funcional en:

```text
src/malak/app/cli.py
```

La superficie vigente ofrece:

```text
help
status
new
exit / quit / salir
conversation prompt
```

También contiene:

- selección de runtime `mock` / `ollama`;
- `session_id` por conversación;
- `request_id` por request;
- continuidad conversacional;
- routing conversacional a través de Kernel;
- eventos operativos correlacionados para conversation;
- manejo controlado de errores.

Sin embargo E2, E3 y E4 ya están integrados y no existe una superficie humana
coherente para invocarlos desde la CLI.

La necesidad de E5-A es por tanto concreta:

```text
integrated Engineering capabilities
                +
existing CLI
                ↓
missing human command surface
```

No se necesita una TUI completa para resolver este gap.

---

## 5. Posición en Engineering Intelligence

```text
E0 Repository Read
        +
E1 Governed Knowledge Read
        ↓
shared bounded evidence
        ↓
E2 Engineering Inspect
        ↓
E3 Engineering Analyze
        ↓
E4 Engineering Propose
        ↓
Owner

E5-A Adaptive Terminal Command Surface
        ↓
makes E2/E3/E4 reachable by explicit human command
        ↓
does not change E2/E3/E4 authority or semantics
```

E5-A es una superficie de interacción.

No es:

- Reasoning Engine;
- Planning Engine nuevo;
- Capability Manager nuevo;
- orchestration layer;
- execution engine;
- task manager;
- agent manager;
- permission system;
- source of truth;
- authority boundary nueva.

---

## 6. Terminal Adaptativa — roadmap preservado

La visión de terminal no se limita a tres comandos. E5 se preserva como una
fundación adaptativa que sólo crece cuando el baseline demuestra una capacidad y
una necesidad reales.

```text
E5-A — Command Surface
        Conversation + Inspect + Analyze + Propose
        DESIGN ADMITTED

E5-B — Navigation / Context Surface
        sessions / evidence / findings / proposals / knowledge
        DEFERRED

E5-C — Profiles
        presentation filters / relevant views / relevant actions
        DEFERRED

E5-D — Rich TUI
        panes / overlays / split views / shortcuts / multi-window experience
        DEFERRED

E5-E — Task Surface
        lifecycle / queue / progress / watchdog / bounded concurrency
        BLOCKED until real task/execution lifecycle exists

E5-F — Operational Control
        agents / tools / sandbox / approvals / executions
        BLOCKED until those capabilities exist and are separately governed
```

Este roadmap es adaptativo:

```text
capability exists
      ↓
mature + governed?
      ↓
human utility demonstrated?
      ↓
security horizon clear?
      ↓
four questions PASS?
      ↓
admit terminal projection
```

No se construyen ventanas vacías para capacidades inexistentes.

---

## 7. Regla de profiles futura

E5-C podrá introducir perfiles únicamente como filtros de presentación.

Principio:

```text
profile
  ↓
what is shown
what is emphasized
what navigation is convenient
```

Nunca:

```text
profile
  ↓
new authority
permission escalation
hidden bypass
```

Un perfil no podrá conceder una Capability, operación o permiso que el sistema no
haya autorizado independientemente.

E5-A no implementa profiles.

---

## 8. Referencia externa preservada — EXT-22 / gentle-pi

El Research Horizon Map registra `gentle-pi` como `EXT-22`.

Disposición E5:

```text
typed task lifecycle                  OBSERVE for E5-E
bounded concurrency                   OBSERVE for E5-E
presence projection                   OBSERVE for E5-D/E5-E
candidate lineage                     REUSE where already applicable through RDD
candidate-bound evidence              REUSE existing Malāk discipline
CLI/TUI architecture                  REJECT as direct adoption
authority model                       REJECT as direct adoption
framework/defaults                    REJECT as direct adoption
```

Clasificación global:

```text
EXT-22 → ADAPT properties, do not copy architecture
```

Malāk toma propiedades demostradas y las revalida contra su propia lógica.

---

## 9. Scope exacto de E5-A

E5-A V0 agrega una única responsabilidad:

> Reconocer comandos Engineering explícitos y dirigirlos determinísticamente a
> kernels precompuestos que contienen exactamente una capability integrada.

Capacidades expuestas:

```text
engineering_inspect
engineering_analyze
engineering_propose
```

Conversation continúa intacta.

E5-A no crea una capability nueva porque el valor no es cognitivo. La
responsabilidad es de Application / Interface Composition.

---

## 10. Gramática CLI V0

Namespace reservado:

```text
/engineering
```

Comandos:

```text
/engineering help
/engineering inspect <subject>
/engineering analyze <subject>
/engineering propose <subject>
```

No existen aliases en V0.

La elección de un namespace explícito con `/` evita que una frase conversacional
normal sea reinterpretada accidentalmente como control de CLI.

Ejemplos:

```text
/engineering inspect Memory
/engineering analyze Memory
/engineering propose Memory
```

Entrada conversacional normal:

```text
Explícame cómo funciona Engineering Propose.
```

continúa por Conversation.

---

## 11. Parser determinista

El parser de E5-A:

- no usa LLM;
- no usa embeddings;
- no usa classifier;
- no consulta Memory;
- no consulta Knowledge;
- no consulta Planner para inferir intención;
- no ejecuta fuzzy matching;
- no autocorrige subcomandos.

Reglas:

```text
strip outer whitespace
        ↓
exact /engineering namespace?
   ┌────┴────┐
   no       yes
   ↓         ↓
existing    deterministic E5 parser
conversation
```

El namespace y action pueden normalizarse en lowercase.

El `subject`:

- conserva case;
- conserva contenido interno;
- elimina únicamente whitespace exterior;
- se delega a la validación ya existente de E2/E3/E4;
- no se reescribe semánticamente.

Comando inválido:

```text
/engineering unknown X
```

produce error determinista y ayuda.

Nunca cae a Conversation.

Comando incompleto:

```text
/engineering inspect
```

produce error determinista.

Nunca provoca model call.

---

## 12. Routing: Kernel permanece como entry point

E5-A no modifica `Kernel`, `Planner`, `Request` ni
`CapabilityRegistry`.

La composición futura autorizable debe reutilizar el patrón existente:

```text
Capability
    ↓
CapabilityRegistry(exactly that capability)
    +
Planner(capability_name=exact capability)
    ↓
Kernel
```

Para Engineering:

```text
/engineering inspect
        ↓
Kernel[engineering_inspect]

/engineering analyze
        ↓
Kernel[engineering_analyze]

/engineering propose
        ↓
Kernel[engineering_propose]
```

La CLI selecciona una superficie precompuesta por un token de comando explícito.

No selecciona autoridad.

No llama `.execute()` directamente.

Regla:

```text
CLI command routing != capability execution bypass
```

Toda capability continúa atravesando `Kernel.receive(...)`.

---

## 13. Composición Engineering V0

Cuando E5-A tenga GREEN autorizado, la composición mínima candidata será:

```text
explicit repository_root
        ↓
GitRepositoryReader
        ↓
GovernedKnowledgeReader
        ↓
shared ConversationService
        ↓
EngineeringInspectCapability
EngineeringAnalyzeCapability
EngineeringProposeCapability
        ↓
one fixed Kernel per capability
```

Los tres kernels deben compartir:

- el mismo `GitRepositoryReader`;
- el mismo baseline capturado;
- el mismo `GovernedKnowledgeReader`;
- el mismo provider/runtime;
- el mismo model config aplicable.

Esto evita baseline mismatch interno y evita construir tres snapshots diferentes.

---

## 14. Configuración del repositorio

Variable candidata:

```text
MALAK_REPOSITORY_ROOT
```

Reglas:

- explícita;
- opcional para preservar CLI conversacional existente;
- sin fallback implícito a current working directory;
- sin búsqueda ascendente automática;
- sin discovery probabilístico.

Si está ausente:

```text
Conversation → disponible
Engineering CLI → unavailable / deterministic explanation
```

Si está presente:

```text
GitRepositoryReader validates exact Git top-level
        ↓
captured HEAD becomes Engineering baseline
```

E5-A no agrega una validación Git paralela que compita con E0.

---

## 15. Snapshot lifetime

El baseline Engineering se captura una sola vez durante composición.

Durante una sesión CLI:

```text
startup
  ↓
capture repository baseline
  ↓
inspect / analyze / propose
  ↓
same baseline
```

No existe `refresh` en E5-A.

No existe auto-fetch.

No existe auto-pull.

No existe cambio silencioso de HEAD.

Para capturar otro baseline, V0 requiere reiniciar la CLI.

Esto preserva reproducibilidad y evita mezclar outputs de distintos snapshots en
una misma sesión operacional.

---

## 16. Help y status

`help` conserva comandos actuales y puede anunciar el namespace Engineering.

`/engineering help` expone únicamente:

```text
inspect
analyze
propose
```

`status` podrá mostrar, sin crear autoridad:

```text
runtime
provider
engineering: available | unavailable
engineering baseline: <sha> | unavailable
```

No muestra estado inventado de capabilities.

No interpreta PASS/GROUNDED como autorización.

---

## 17. Output boundary

E5-A no parsea nuevamente los envelopes producidos por E2/E3/E4.

Regla:

```text
Capability output
        ↓
CLI presentation
```

No:

```text
Capability output
        ↓
CLI semantic reinterpretation
        ↓
new status / authority
```

La CLI puede agregar únicamente un encabezado determinista de presentación, por
ejemplo:

```text
Malāk [engineering/inspect]
<capability output unchanged>
```

El payload de la capability debe permanecer intacto.

---

## 18. Observabilidad

Los comandos Engineering exitosamente parseados deben conservar correlación por
`request_id`.

Eventos candidatos sin crear schema nuevo:

```text
engineering.inspect.started
engineering.inspect.succeeded
engineering.inspect.failed

engineering.analyze.started
engineering.analyze.succeeded
engineering.analyze.failed

engineering.propose.started
engineering.propose.succeeded
engineering.propose.failed
```

Todos:

```text
component = cli
request_id = request exacto
authority_effect = none implicitly by event semantics
```

Un fallo al registrar el evento `started` debe conservar el comportamiento
fail-closed ya aplicado por la CLI conversacional: no se ejecuta la capability.

Un fallo del evento final no debe convertir una respuesta válida en ejecución
fallida ni generar un segundo efecto semántico.

Comandos inválidos o help/status no generan eventos Engineering.

---

## 19. Session boundary

Conversation conserva su `session_id` e historial efímero.

Engineering E2/E3/E4 continúa siendo stateless respecto de history.

E5-A no añade conversation history a las inferencias Engineering.

El `session_id` de la CLI puede utilizarse únicamente como correlación de
request donde el contrato `Request` lo requiera.

Nunca como:

- Memory;
- authority;
- SecurityContext;
- evidence;
- baseline identity.

---

## 20. Authority boundary

E5-A preserva:

```text
CLI input != Authorization
CLI selection != Permission
CLI presentation != Authority

Evidence != Authority
Analysis != Decision
Finding != Authorization
Proposal != Decision
Proposal != Authorization
Proposal != Implementation
Proposal != Execution
```

En particular:

```text
/engineering propose X
```

produce únicamente E4.

No habilita:

- patch;
- write;
- branch;
- commit;
- PR;
- tool;
- sandbox;
- agent;
- execution;
- merge.

---

## 21. Security Horizon Check

### Prompt & Context Trust

`ALREADY_COVERED`.

E5-A no transforma contenido recuperado en comandos. El namespace se reconoce
antes de llegar a E2/E3/E4 y el subject continúa como data.

### Identity & Delegation

`NOT_APPLICABLE`.

No existen agents ni delegation.

### Compromise Containment

`NOT_APPLICABLE`.

No se agrega operación externa.

### Memory / Knowledge poisoning

`ALREADY_COVERED`.

E5-A reutiliza E1 y no persiste nuevo estado.

### AI Supply-Chain Trust

`ALREADY_COVERED`.

E5-A requiere cero dependencia externa nueva.

### Data classification

`NOT_APPLICABLE`.

No persiste ni exporta datos.

### Resource Governance

`ALREADY_COVERED`.

Sin background jobs, concurrency, workers ni loops.

### Observability / Human in Control

`REQUIRES_REINFORCEMENT`.

E5-A debe preservar correlación y mostrar claramente que Propose vuelve al Owner.

No existe blocker de seguridad para E5-A.

---

## 22. Complejidad y dependencias

E5-A V0 prohíbe nuevas dependencias de UI.

Fuera de scope:

```text
Typer
Click
prompt_toolkit
Textual
Rich-as-framework
curses abstraction
web UI
desktop UI
```

Esto no constituye un rechazo permanente.

Significa:

> una dependencia de terminal rica sólo se evalúa cuando E5-D demuestre necesidad
> real que la CLI simple ya no pueda resolver.

E5-A debe poder implementarse con la biblioteca estándar y componentes actuales.

---

## 23. E5-D — experiencia rica futura

La visión futura preserva:

- panel de navegación;
- panel de tareas cuando existan tareas reales;
- detalle seleccionado;
- logs/evidence visibles;
- overlays;
- command palette;
- atajos;
- multi-session view;
- split views;
- presencia / estado observable;
- perfiles de información.

Pero E5-D permanece `DEFERRED`.

No se selecciona framework TUI en E5-A.

No se crea layout vacío.

No se crea estado UI paralelo al estado real de Malāk.

Regla futura:

```text
TUI projects system state
TUI does not invent system state
```

---

## 24. E5-E — Task Surface futura

Las propiedades preservadas de task lifecycle sólo se promueven cuando exista un
dueño runtime real.

E5-E podrá considerar:

```text
QUEUED
RUNNING
WAITING
PAUSED
SUCCEEDED
FAILED
CANCELLED
```

únicamente si esos estados son contratos reales del sistema.

La terminal no podrá inventar lifecycle por conveniencia visual.

También quedan diferidos:

- queue;
- bounded concurrency;
- watchdogs;
- cancellation;
- retry;
- resume;
- checkpoints;
- task store;
- presence projection.

---

## 25. E5-F — Operational Control futura

Bloqueado hasta diseño separado de las superficies subyacentes.

No autorizado por E5:

```text
agents
tools
sandbox
network
external API execution
writes
Git mutation
self-modification
automatic remediation
automatic merge
```

Cuando esas capabilities existan, la terminal será únicamente uno de sus
consumidores.

---

## 26. Malāk Alignment Matrix

| Fuente | Clase | Invariante / intención | Disposición E5 | Efecto |
| --- | --- | --- | --- | --- |
| Cognitive Constitution | normativa | proporcionalidad, minimización, evidencia, trazabilidad | ADOPT | parser determinista; no nueva inferencia |
| Governance Constitution | normativa | Human in Control, separación, mínimo privilegio | ADOPT | CLI no concede autoridad |
| Blueprint | normativa | Kernel pequeño, Capability First, incrementalidad | ADOPT | E5 queda en app/composition |
| Architecture Quality Gates | arquitectura | no aumentar Kernel sin justificación | ADOPT | Kernel delta = 0 |
| SECURITY.md | política protegida | Zero Trust, fail-closed, Human in Control | ADOPT | malformed command no cae a LLM |
| Construction Protocol | método | G0 exhaustivo, gates, adaptive incubation | ADOPT | coverage ledger + scope mínimo |
| Current CLI | baseline | conversation + basic commands + events | REUSE | preservar comportamiento |
| Kernel / Planner | baseline | Kernel entry point + planner fijo | REUSE | kernels precompuestos por capability |
| E2 | baseline | grounded read-only inspection | REUSE | command surface only |
| E3 | baseline | grounded analysis | REUSE | command surface only |
| E4 | baseline | bounded proposal → Owner | REUSE | command surface only |
| Research Horizon EXT-22 | no normativa | lifecycle tipado / bounded concurrency / presence | OBSERVE | reservado para E5-D/E5-E |
| gentle-pi CLI/TUI | externa | arquitectura propia del proyecto externo | REJECT direct adoption | no copiar framework/modelo |
| Profiles conversacionales preservados | intención de producto | interfaz relevante por rol | ADAPT | E5-C futuro; presentation only |

---

## 27. Cuadro de implementación adaptativa

| Unidad | Necesidad actual | Implementación E5-A | Estado |
| --- | --- | --- | --- |
| Conversation | sí | preservar | CURRENT |
| Inspect | sí | exponer | CANDIDATE |
| Analyze | sí | exponer | CANDIDATE |
| Propose | sí | exponer | CANDIDATE |
| Evidence browser | todavía no demostrada | no | DEFERRED |
| Findings browser | todavía no demostrada | no | DEFERRED |
| Profiles | intención válida, no blocker | no | DEFERRED |
| Rich panes | no necesaria para V0 | no | DEFERRED |
| Task list | runtime inexistente | no | BLOCKED |
| Concurrency view | runtime inexistente | no | BLOCKED |
| Agents/tools control | capabilities no autorizadas | no | BLOCKED |
| Execution approvals | execution no autorizada | no | BLOCKED |

---

## 28. Scope de archivos

### G0/G1 autorizado por el Owner

```text
docs/project/sprints/proposals/MALAK-E5-G0-COVERAGE-LEDGER.md
docs/project/sprints/proposals/MALAK-E5-ENGINEERING-CLI-G0-G1-DESIGN.md
```

### RED futuro — NO autorizado por este documento

Scope candidato si el Owner autoriza RED:

```text
tests/test_cli.py
tests/test_app_composition.py
```

No se autoriza todavía.

### GREEN futuro — NO autorizado por este documento

Scope candidato mínimo si RED demuestra necesidad y el Owner autoriza GREEN:

```text
src/malak/app/cli.py
src/malak/app/composition.py
```

Cualquier archivo adicional requiere stop + revisión de scope.

---

## 29. TDD RED requerido antes de GREEN

Cuando exista autorización explícita de RED, debe demostrar al menos:

- namespace exacto `/engineering`;
- `/engineering help` determinista;
- inspect route exacta;
- analyze route exacta;
- propose route exacta;
- subject case/content preservado;
- command prefix normalizado sin mutar subject;
- invalid action => deterministic error;
- missing subject => deterministic error;
- invalid Engineering command => zero conversation calls;
- invalid Engineering command => zero engineering capability calls;
- no LLM intent classification;
- non-command text preserves existing Conversation path;
- current `help/status/new/exit` behavior remains green;
- Engineering unavailable when `MALAK_REPOSITORY_ROOT` is absent;
- no implicit cwd fallback;
- one repository snapshot shared by E2/E3/E4 composition;
- identical baseline for the three capabilities;
- all Engineering requests traverse `Kernel.receive`;
- CLI never calls Capability.execute directly;
- E2 output preserved;
- E3 output preserved;
- E4 output preserved;
- `proposal != implementation` visible in behavior;
- engineering request IDs correlate started/succeeded/failed events;
- started-event failure prevents capability execution;
- final event failure does not invent a second capability failure;
- no session history injected into Engineering;
- no new external dependency;
- Kernel source unchanged;
- Planner source unchanged;
- E2/E3/E4 regression suites remain green.

RED válido:

```text
new E5 tests fail because E5-A command/composition surface does not exist
existing baseline tests remain green
collection remains healthy
```

Cualquier fallo preexistente o no relacionado => STOP.

---

## 30. Validación GREEN futura

Sólo tras autorización GREEN separada:

1. targeted E5 tests;
2. E2/E3/E4 regression;
3. existing CLI regression;
4. Kernel/Planner regression;
5. full pytest;
6. compileall;
7. git diff --check;
8. candidate identity;
9. candidate-bound evidence manifest;
10. FULL 4R;
11. Windows + Ubuntu;
12. E2E real:
    `CLI command → Kernel → E2/E3/E4 → output → Owner`;
13. independent validation;
14. human review;
15. Ready y merge humanos.

---

## 31. Métricas del gate futuro

Registrar:

```text
baseline_sha
candidate_sha
risk_class
changed_files
production_delta
test_delta
dependencies_added
kernel_delta
planner_delta
public_contract_changes
targeted_tests
full_tests
correction_rounds
risk_status
readability_status
reliability_status
resilience_status
final_status
```

Objetivos E5-A:

```text
dependencies_added = 0
kernel_delta = 0
planner_delta = 0
E2 behavior delta = 0
E3 behavior delta = 0
E4 behavior delta = 0
```

---

## 32. Stop conditions

STOP si E5-A requiere:

- modificar Kernel;
- modificar Planner;
- modificar Request/Response core;
- modificar E0/E1;
- cambiar comportamiento observable E2/E3/E4;
- introducir LLM intent routing;
- introducir fuzzy command matching;
- parsear semánticamente outputs E2/E3/E4;
- usar current working directory implícito como repo root;
- auto-fetch o auto-pull;
- refrescar baseline silenciosamente;
- nueva dependencia externa;
- Typer/Click/Textual/prompt_toolkit por adelantado;
- background worker;
- concurrency;
- task store;
- watchdog;
- agent;
- tool;
- sandbox;
- write;
- Git mutation;
- ejecución;
- profiles con efecto de autoridad;
- convertir proposal en acción;
- ampliar scope sin nuevo gate.

---

## 33. Evaluación de sobreingeniería

E5-A pasa el Complexity Budget porque:

```text
existing CLI
+
existing integrated capabilities
+
deterministic parser
+
minimal composition
=
immediate human utility
```

E5-D/E/F no pasan todavía ese mismo test porque introducirían infraestructura
sin consumidor runtime real.

Regla:

> Terminal richness follows system maturity; it does not precede it.

---

## 34. Resultado de admisión

```text
E5-A Command Surface
G0      PASS
G1      DESIGN COMPLETE
RED     NOT AUTHORIZED
GREEN   NOT AUTHORIZED

E5-B    DEFERRED
E5-C    DEFERRED
E5-D    DEFERRED
E5-E    BLOCKED
E5-F    BLOCKED
```

El design deja preparada una expansión futura sin comprometer el baseline actual.

---

## 35. Autoridad

Este documento registra diseño no normativo.

La autorización del Owner en esta etapa cubre únicamente:

```text
G0 coverage
+
G1 design
```

No autoriza:

```text
RED tests
GREEN implementation
runtime changes
new dependencies
rich TUI
profiles
tasks
agents
tools
sandbox
writes
execution
merge
```

Separación final:

```text
Terminal != Authority
Command != Permission
Presentation != Decision
Proposal != Implementation
Evidence != Authority
```
