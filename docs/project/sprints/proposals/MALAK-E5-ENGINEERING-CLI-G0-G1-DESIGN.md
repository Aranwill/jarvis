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
TUI, tasks, agents, tools o ejecución inexistente.

Pregunta de aceptación:

> ¿Puede Malāk exponer Conversation + Engineering Intelligence mediante una
> superficie CLI determinista, simple y trazable, conservando Kernel mínimo,
> Human in Control y exactamente las fronteras read-only de E2/E3/E4?

E5-A sólo debe demostrar:

```text
human input
   ↓
deterministic CLI parsing
   ↓
pre-composed Kernel boundary
   ↓
existing Capability
   ↓
existing output
   ↓
human
```

`CLI != Authority`.

---

## 2. Baseline

```text
Aranwill/jarvis main
5b6660eba9e5617a59c17d7380dd6822e8c193a4

E0 Repository Read            INTEGRATED
E1 Governed Knowledge Read    INTEGRATED
E2 Engineering Inspect        INTEGRATED
E3 Engineering Analyze        INTEGRATED
E4 Engineering Propose        INTEGRATED
D1 E4 state reconciliation    CLOSED
E5 Engineering CLI            NOT AUTHORIZED before this design
```

Downstream observado:

```text
Vault PR #126 merged
Vault main c1d61e264113ec396760b39dc5e027252eefe2f7
```

G0 exhaustivo:

```text
tracked files discovered = 258
tracked files classified = 258
silently omitted files   = 0
G0 RESULT                 = PASS
```

Ledger:

`docs/project/sprints/proposals/MALAK-E5-G0-COVERAGE-LEDGER.md`

---

## 3. Cuatro preguntas de ley

```text
Blueprint                  PASS
Cognitive Constitution     PASS
Governance Constitution    PASS
Kernel complexity          NO DELTA
```

Razones:

- E5-A vive en `app/composition`, no en cognición.
- routing de comandos es determinista, no probabilístico;
- E5-A no inventa evidencia ni altera E2/E3/E4;
- el Owner conserva toda autoridad;
- Kernel, Planner y contratos core permanecen intactos.

Si E5-A requiere ampliar responsabilidad del Kernel, el design produce STOP.

---

## 4. Necesidad demostrada

La CLI actual ya ofrece:

```text
help
status
new
exit / quit / salir
conversation prompt
```

y ya preserva runtime selection, session/request IDs, routing conversacional por
Kernel, history efímero, observabilidad y errores controlados.

El baseline también contiene E2, E3 y E4 integrados.

Gap real:

```text
existing CLI
+
integrated Engineering capabilities
↓
missing human command surface
```

No existe necesidad demostrada de una TUI completa para resolver este gap.

---

## 5. Terminal Adaptativa — roadmap preservado

```text
E5-A Command Surface
     Conversation + Inspect + Analyze + Propose
     DESIGN ADMITTED

E5-B Navigation / Context
     sessions / evidence / findings / proposals / knowledge
     DEFERRED

E5-C Profiles
     presentation filters / relevant views / relevant actions
     DEFERRED

E5-D Rich TUI
     panes / overlays / split views / shortcuts / multi-window
     DEFERRED

E5-E Task Surface
     lifecycle / queue / progress / watchdog / bounded concurrency
     BLOCKED until real task/execution lifecycle exists

E5-F Operational Control
     agents / tools / sandbox / approvals / execution
     BLOCKED until separately implemented and governed
```

Regla adaptativa:

```text
capability exists
→ mature + governed
→ real human utility
→ security horizon clear
→ four questions PASS
→ terminal projection may be admitted
```

La terminal crece con Malāk; no se adelanta a Malāk.

---

## 6. Profiles futuros

E5-C podrá cambiar:

- qué información se muestra;
- qué vistas son prioritarias;
- qué navegación resulta cómoda.

Nunca podrá cambiar:

- permisos;
- authority;
- policy;
- scope;
- enforcement.

```text
Profile = presentation filter
Profile != authority
```

E5-A no implementa profiles.

---

## 7. Referencia EXT-22 / gentle-pi

El Research Horizon Map preserva `gentle-pi` como input de propiedades, no
como arquitectura a copiar.

Disposición E5:

```text
typed task lifecycle      OBSERVE for E5-E
bounded concurrency       OBSERVE for E5-E
presence projection       OBSERVE for E5-D/E5-E
candidate lineage         REUSE where Malāk already implements it
candidate-bound evidence  REUSE RDD Stage 1
CLI/TUI architecture      REJECT direct adoption
authority model           REJECT direct adoption
framework/defaults        REJECT direct adoption
```

Clasificación: `ADAPT properties; do not copy architecture`.

---

## 8. Scope exacto de E5-A

E5-A agrega una sola responsabilidad:

> Reconocer comandos Engineering explícitos y dirigirlos determinísticamente a
> kernels precompuestos que contienen exactamente una capability integrada.

Capacidades:

```text
engineering_inspect
engineering_analyze
engineering_propose
```

Conversation permanece intacta.

E5-A no crea una capability nueva: su responsabilidad es de Application /
Interface Composition.

---

## 9. Gramática CLI V0

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

Sin aliases en V0.

El prefijo `/` evita que una frase conversacional normal sea interpretada
accidentalmente como control de CLI.

Ejemplo conversacional que sigue siendo Conversation:

```text
Explícame cómo funciona Engineering Propose.
```

---

## 10. Parser determinista

El parser:

- no usa LLM;
- no usa embeddings;
- no usa intent classifier;
- no usa fuzzy matching;
- no consulta Memory/Knowledge;
- no autocorrige subcomandos.

Ruta:

```text
input
 ↓
/engineering namespace?
 ├─ no  → existing Conversation path
 └─ yes → exact deterministic parser
```

El namespace/action puede normalizarse a lowercase.

El `subject` conserva case y contenido interno; sólo elimina whitespace
exterior y después queda sujeto a las validaciones existentes de E2/E3/E4.

Comando inválido o incompleto:

- devuelve error determinista;
- no cae a Conversation;
- no genera model call;
- no ejecuta capability.

---

## 11. Routing y Kernel

E5-A no modifica:

```text
Kernel
Planner
Request
Response
CapabilityRegistry
```

Reutiliza el patrón vigente:

```text
Capability
 + CapabilityRegistry(exactly one)
 + Planner(capability_name=exact capability)
 ↓
Kernel
```

Entonces:

```text
/engineering inspect  → Kernel[engineering_inspect]
/engineering analyze  → Kernel[engineering_analyze]
/engineering propose  → Kernel[engineering_propose]
```

La CLI selecciona una superficie por token explícito; no selecciona autoridad.

Regla obligatoria:

```text
CLI command routing != capability execution bypass
```

Toda capability continúa atravesando `Kernel.receive(...)`.

---

## 12. Composición V0

Composición candidata futura:

```text
explicit repository_root
        ↓
GitRepositoryReader
        ↓
GovernedKnowledgeReader
        ↓
shared ConversationService
        ↓
E2 / E3 / E4
        ↓
one fixed Kernel per capability
```

Los tres kernels comparten:

- un único `GitRepositoryReader`;
- un único baseline capturado;
- un único `GovernedKnowledgeReader`;
- provider/runtime/model config común.

No se construyen snapshots separados.

---

## 13. Repository root y snapshot

Variable candidata:

```text
MALAK_REPOSITORY_ROOT
```

Reglas:

- explícita;
- opcional para no romper Conversation;
- sin fallback implícito a current working directory;
- sin auto-discovery;
- validada por `GitRepositoryReader`.

Si falta:

```text
Conversation available
Engineering unavailable with deterministic explanation
```

El baseline Engineering se captura una vez al inicio.

No hay en E5-A:

- refresh;
- fetch;
- pull;
- cambio silencioso de HEAD.

Para otro baseline se reinicia la CLI.

---

## 14. Help, status y output

`help` conserva el comportamiento actual y puede anunciar el namespace
Engineering.

`/engineering help` muestra sólo:

```text
inspect
analyze
propose
```

`status` puede agregar:

```text
engineering: available | unavailable
engineering baseline: <sha> | unavailable
```

La CLI no reinterpreta semánticamente los outputs de E2/E3/E4.

Permitido:

```text
Malāk [engineering/analyze]
<capability output unchanged>
```

No permitido:

```text
capability output
→ CLI invents new status / authority
```

---

## 15. Observabilidad y sesión

Engineering usa `request_id` correlacionado.

Eventos candidatos:

```text
engineering.inspect.started/succeeded/failed
engineering.analyze.started/succeeded/failed
engineering.propose.started/succeeded/failed
```

`component = cli`.

La falla del evento `started` bloquea la ejecución, igual que en Conversation.

Una falla del evento final no convierte una respuesta válida en una segunda
ejecución.

Conversation conserva history efímero.

Engineering permanece stateless respecto de history.

`session_id != Memory != SecurityContext != Authority`.

---

## 16. Authority boundary

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

`/engineering propose X` sólo produce E4.

No produce patch, write, branch, commit, PR, tool, sandbox, agent, execution o
merge.

---

## 17. Security Horizon Check

| Línea | Resultado E5-A |
| --- | --- |
| Prompt & Context Trust | ALREADY_COVERED |
| Identity & Delegation | NOT_APPLICABLE |
| Compromise Containment | NOT_APPLICABLE |
| Memory / Knowledge Poisoning | ALREADY_COVERED |
| AI Supply-Chain Trust | ALREADY_COVERED — cero dependencia nueva |
| Data Classification | NOT_APPLICABLE |
| Resource Governance | ALREADY_COVERED — sin workers/concurrency |
| Observability / Human in Control | REQUIRES_REINFORCEMENT |

No existe `BLOCKING_GAP` para E5-A.

---

## 18. Dependencias y riqueza visual

E5-A prohíbe agregar framework UI.

No E5-A:

```text
Typer
Click
prompt_toolkit
Textual
curses abstraction
web UI
desktop UI
```

No es rechazo permanente.

E5-D evaluará framework sólo si una interfaz rica demuestra valor que la CLI
simple ya no puede entregar.

Principio:

```text
Terminal richness follows system maturity
```

---

## 19. E5-D/E5-E/E5-F preservados

E5-D podrá evaluar en el futuro:

- panes;
- overlays;
- split views;
- command palette;
- shortcuts;
- multi-session;
- multi-window;
- evidence/detail views.

Regla:

```text
TUI projects real system state
TUI does not invent system state
```

E5-E podrá evaluar task lifecycle, queue, progress, watchdogs y bounded
concurrency sólo cuando esos contratos existan realmente.

E5-F queda bloqueado hasta existir y gobernarse agents/tools/sandbox/execution.

---

## 20. Malāk Alignment Matrix

| Fuente | Invariante / intención | Disposición | Efecto E5 |
| --- | --- | --- | --- |
| Cognitive Constitution | proporcionalidad, evidencia, trazabilidad | ADOPT | parser determinista |
| Governance Constitution | Human in Control, mínimo privilegio | ADOPT | CLI no concede autoridad |
| Blueprint | Kernel pequeño, Capability First | ADOPT | app/composition only |
| Architecture Quality Gates | Kernel estable | ADOPT | kernel delta = 0 |
| SECURITY.md | Zero Trust, fail-closed | ADOPT | invalid command no cae a LLM |
| Construction Protocol | G0, gates, adaptive incubation | ADOPT | coverage + scope mínimo |
| Current CLI | conversation + commands + events | REUSE | preservar |
| Kernel / Planner | entry point + deterministic fixed routing | REUSE | kernels precompuestos |
| E2/E3/E4 | read-only grounded capabilities | REUSE | exponer sin modificar |
| EXT-22 | lifecycle/concurrency/presence properties | OBSERVE | futuro E5-D/E |
| gentle-pi CLI/TUI | arquitectura externa | REJECT direct adoption | no copy |

---

## 21. Scope de archivos

### G0/G1 autorizado

```text
docs/project/sprints/proposals/MALAK-E5-G0-COVERAGE-LEDGER.md
docs/project/sprints/proposals/MALAK-E5-ENGINEERING-CLI-G0-G1-DESIGN.md
```

### RED futuro — NO autorizado aún

Scope candidato:

```text
tests/test_cli.py
tests/test_app_composition.py
```

### GREEN futuro — NO autorizado aún

Scope candidato mínimo:

```text
src/malak/app/cli.py
src/malak/app/composition.py
```

Cualquier archivo adicional => STOP + revisión de scope.

---

## 22. TDD RED requerido antes de GREEN

Cuando el Owner autorice RED, cubrir al menos:

- namespace exacto `/engineering`;
- help Engineering;
- routes inspect/analyze/propose;
- subject preservado;
- invalid/missing command fail-closed;
- zero fallback a Conversation para command inválido;
- zero LLM intent classification;
- non-command input conserva Conversation;
- `help/status/new/exit` permanecen verdes;
- Engineering unavailable sin `MALAK_REPOSITORY_ROOT`;
- zero implicit cwd fallback;
- un snapshot compartido por E2/E3/E4;
- baseline idéntico;
- todas las routes pasan `Kernel.receive`;
- nunca `Capability.execute` directo;
- outputs E2/E3/E4 preservados;
- history vacío en Engineering;
- events correlacionados;
- no nueva dependencia;
- Kernel/Planner sin cambios;
- regressions E2/E3/E4 verdes.

RED válido:

```text
new E5 tests fail only because E5-A does not exist
existing baseline tests remain green
collection remains healthy
```

Otro patrón => STOP.

---

## 23. GREEN futuro y métricas

Sólo tras autorización separada:

1. targeted E5;
2. CLI regression;
3. E2/E3/E4 regression;
4. Kernel/Planner regression;
5. full pytest;
6. compileall;
7. diff check;
8. candidate identity;
9. evidence manifest;
10. FULL 4R;
11. Ubuntu + Windows;
12. E2E `CLI → Kernel → E2/E3/E4 → output → Owner`;
13. independent validation;
14. human review.

Objetivos:

```text
dependencies_added = 0
kernel_delta = 0
planner_delta = 0
E2_behavior_delta = 0
E3_behavior_delta = 0
E4_behavior_delta = 0
```

---

## 24. Stop conditions

STOP si E5-A requiere:

- Kernel/Planner/core contract changes;
- E0/E1 changes;
- behavior changes E2/E3/E4;
- LLM intent routing;
- fuzzy routing;
- semantic parsing de outputs E2/E3/E4;
- implicit cwd repository discovery;
- auto-fetch/auto-pull;
- silent baseline refresh;
- nueva dependencia;
- rich TUI adelantada;
- workers/concurrency/task store/watchdog;
- agents/tools/sandbox;
- writes/Git mutation/execution;
- profiles con efecto de autoridad;
- proposal → action;
- scope expansion sin nuevo gate.

---

## 25. Resultado

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

Este documento autoriza únicamente G0/G1 documental.

No autoriza tests RED, implementación GREEN, merge ni fases posteriores.

Separación final:

```text
Terminal != Authority
Command != Permission
Presentation != Decision
Proposal != Implementation
Evidence != Authority
```
