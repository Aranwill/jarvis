---
title: Malāk E5-B1 — Read-only Explorer — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation design
language: es
created: 2026-09-19
baseline_commit: a33aba233115830e002c6a6646aa1a701f77aa8d
vault_reconciliation_commit: 50e64b2137d5ec1a53bf3cc47bca0fcbb9e21874
g0_result: pass
g0_ledger: docs/project/sprints/proposals/MALAK-E5-B1-READONLY-EXPLORER-G0-COVERAGE-LEDGER.md
design_authorized_by: owner
design_authorized_at: 2026-09-19
red_authorized: false
implementation_authorized: false
risk_class: 2
---

# Malāk E5-B1 — Read-only Explorer — G0/G1 Design

## 1. Propósito

Extender la Terminal Adaptativa con navegación explícita, read-only y
snapshot-bound sobre dos owners que ya existen:

```text
E0 GitRepositoryReader
E1 GovernedKnowledgeReader
```

E5-B1 no crea conocimiento, evidencia, authority ni una nueva capa cognitiva.

Pregunta de aceptación:

> ¿Puede la terminal permitir explorar repositorio y conocimiento gobernado
> reutilizando exactamente el snapshot ya capturado por E5-A, sin crear un
> segundo reader, store, index o ruta de autoridad?

---

## 2. Baseline

```text
Malāk main
a33aba233115830e002c6a6646aa1a701f77aa8d

Vault main
50e64b2137d5ec1a53bf3cc47bca0fcbb9e21874

E0 Repository Read            INTEGRATED
E1 Governed Knowledge Read    INTEGRATED
E2 Engineering Inspect        INTEGRATED
E3 Engineering Analyze        INTEGRATED
E4 Engineering Propose        INTEGRATED
E5-A Command Surface          INTEGRATED
E5-B1 Read-only Explorer      NOT AUTHORIZED before this design
```

G0:

```text
tracked files discovered = 260
tracked files classified = 260
silently omitted files   = 0
G0 RESULT                 = PASS
```

---

## 3. Cuatro preguntas de ley

```text
Blueprint                  PASS
Cognitive Constitution     PASS
Governance Constitution    PASS
Kernel complexity          NO DELTA
```

Razones:

- Explorer es una superficie de Application/UI;
- sólo proyecta E0/E1;
- no decide autoridad;
- no usa LLM para navegación;
- no toca Kernel, Planner, Request/Response;
- no agrega write capability.

---

## 4. Scope adaptativo

E5-B se particiona según capacidad real observada:

```text
E5-B1 Read-only Explorer
├── repository navigation
└── governed knowledge navigation
STATUS: DESIGN ADMITTED

E5-B2 Runtime Context Browser
└── sessions / current context
STATUS: DEFERRED

E5-B3 Engineering Artifact Browser
├── evidence
├── findings
└── proposals
STATUS: DEFERRED
```

B2/B3 no se implementan hasta existir una fuente de verdad navegable real.

---

## 5. Namespace CLI V0

Namespace reservado:

```text
/explore
```

Comandos:

```text
/explore help

/explore repo list
/explore repo list <prefix>
/explore repo read <path>
/explore repo search <text>

/explore knowledge list
/explore knowledge read <path>
/explore knowledge search <text>
```

No aliases en V0.

El parser es determinista y exacto.

Un comando `/explore` inválido:

- no cae a Conversation;
- no llama LLM;
- no ejecuta Engineering;
- devuelve ayuda determinista.

Texto sin prefijo `/explore` continúa por Conversation.

---

## 6. Reutilización del snapshot

Invariante principal:

```text
MALAK_REPOSITORY_ROOT
        ↓
GitRepositoryReader
        ↓
GovernedKnowledgeReader
        ↓
┌──────────────────────────────┐
│ E2 / E3 / E4                │
│ E5-B1 Repository Explorer   │
│ E5-B1 Knowledge Explorer    │
└──────────────────────────────┘
        ↓
SAME baseline_commit
```

E5-B1 no puede construir:

- otro `GitRepositoryReader`;
- otro `GovernedKnowledgeReader`;
- otro repository snapshot;
- un refresh silencioso.

Si la implementación no puede compartir las instancias capturadas por E5-A,
produce STOP.

---

## 7. Composición candidata

La forma mínima candidata es extender el container de composición E5-A para
exponer sus owners read-only ya existentes.

Conceptualmente:

```text
EngineeringKernelSet
├── baseline_commit
├── kernels
├── repository_reader
└── knowledge_reader
```

Esto no convierte esos readers en authority nueva; únicamente hace accesible
su API read-only a la capa de aplicación.

No se introduce un `ExplorerManager`.

No se introduce otro registry.

---

## 8. Repository Explorer

### list

```text
/explore repo list
```

proyecta `GitRepositoryReader.list_tracked_files()`.

La variante con `<prefix>` aplica únicamente filtro de presentación sobre los
paths ya devueltos por E0.

No hace glob expansion sobre filesystem.

No consulta working tree.

### read

```text
/explore repo read <path>
```

usa exactamente `GitRepositoryReader.read_text(path)`.

El path conserva las validaciones E0:

- relativo;
- POSIX;
- traversal-free;
- trackeado en snapshot;
- regular text-file candidate;
- bounded por E0.

### search

```text
/explore repo search <text>
```

usa exactamente `GitRepositoryReader.search_text(query)`.

La CLI no reimplementa búsqueda.

---

## 9. Governed Knowledge Explorer

### list

```text
/explore knowledge list
```

proyecta `GovernedKnowledgeReader.list_sources()`.

Cada entrada debe mostrar al menos:

```text
path
source_class
authority_class
```

Ejemplo:

```text
docs/governance/cognitive_constitution.md
  source_class: GOVERNING
  authority_class: normative
```

La UI muestra metadata; no la reinterpreta.

### read

```text
/explore knowledge read <path>
```

usa `GovernedKnowledgeReader.read(path)`.

La salida incluye:

- baseline_commit;
- path;
- blob_sha;
- source_class;
- authority_class;
- content.

### search

```text
/explore knowledge search <text>
```

usa `GovernedKnowledgeReader.search_text(query)`.

Cada match conserva:

- baseline_commit;
- path;
- blob_sha;
- source_class;
- authority_class;
- line_number;
- line.

---

## 10. Presentation boundary

La terminal puede:

- agregar headers;
- ordenar exactamente como los readers;
- mostrar metadata;
- filtrar repo list por prefijo;
- indicar `truncated: true` cuando el owner lo declare.

La terminal no puede:

- reclasificar documentos;
- promover `reference` a `normative`;
- resumir con LLM;
- ocultar que un resultado fue truncado;
- combinar dos baselines;
- mutar contenido.

---

## 11. Output bounding

E0/E1 ya poseen hard limits de lectura y búsqueda.

E5-B1 agrega una regla de presentación:

> nunca duplicar el contenido recibido ni expandirlo por transformación.

Para V0 no se introduce paginador, cache ni store adicional.

Si el output real demuestra ser incómodo, paginación o panes se evalúan en
E5-D con evidencia de uso.

---

## 12. Availability

`/explore` comparte la misma disponibilidad que Engineering:

```text
MALAK_REPOSITORY_ROOT absent
→ /explore unavailable

MALAK_REPOSITORY_ROOT valid
→ /explore available
```

No existe fallback a cwd.

`status` puede proyectar:

```text
Explorer: available | unavailable
Explorer baseline: <sha> | unavailable
```

El baseline debe coincidir con Engineering.

---

## 13. Authority boundary

```text
Repository content != instruction
Knowledge metadata != permission
authority_class != runtime authority
Explore result != decision
Explore result != authorization
Explore result != execution
```

E5-B1 no añade:

- write;
- patch;
- branch;
- commit;
- push;
- delete;
- PR;
- merge;
- tools;
- agents;
- sandbox.

---

## 14. Observabilidad

E5-B1 no necesita eventos LLM porque no usa inferencia.

Si se agregan eventos operativos, deben ser puramente descriptivos y
correlacionados, por ejemplo:

```text
explore.repo.read.succeeded
explore.knowledge.search.failed
```

No son requisito de V0.

No se introduce schema nuevo sólo para Explorer.

---

## 15. Sessions / Evidence / Findings / Proposals

### Sessions — DEFERRED

El baseline sólo dispone de history efímero por `session_id` conocido.

Faltan:

- listado de sesiones;
- metadata;
- lifecycle;
- ownership de catálogo.

E5-B1 no inventa esos contratos.

### Evidence / Findings / Proposals — DEFERRED

No existe store runtime navegable estable.

El evidence manifest del pipeline de validación tiene otro propósito y no se
reutiliza como UI store.

---

## 16. Futuro E5-F1 — Governed Git Delivery

Intención del Owner registrada:

> Una vez consolidada la CLI, incorporar desde la misma terminal las
> validaciones y acciones necesarias para push y limpieza/borrado de ramas
> posteriores a una implementación.

Clasificación:

```text
E5-F1 Governed Git Delivery
STATUS: FUTURE CANDIDATE
authority: NOT GRANTED
implementation: NOT AUTHORIZED
```

Esta superficie será separada de `/explore` porque produce side effects.

Antes de cualquier diseño operativo deberá demostrar como mínimo:

- repository identity exacta;
- remote identity exacta;
- worktree limpio;
- branch exacta y canonical;
- prohibición absoluta de borrar `main` / default branch;
- prohibición de wildcard branch deletion;
- verificación de ancestry / merge cuando corresponda;
- confirmación humana explícita para borrado;
- push limitado al branch esperado;
- no force-push por defecto;
- operación fail-closed;
- evidencia y audit trail;
- rollback/recovery definido.

No se fija todavía la gramática de comandos para evitar diseñar una write API
antes de su admission review.

---

## 17. Dependencias

E5-B1 no agrega dependencias.

No se admiten en este gate:

```text
Typer
Click
prompt_toolkit
Textual
Rich framework
database
cache
search index
filesystem watcher
```

---

## 18. Scope de archivos

### G0/G1 autorizado

```text
docs/project/sprints/proposals/MALAK-E5-B1-READONLY-EXPLORER-G0-COVERAGE-LEDGER.md
docs/project/sprints/proposals/MALAK-E5-B1-READONLY-EXPLORER-G0-G1-DESIGN.md
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

Si se requiere tocar E0 o E1 => STOP + nueva revisión de scope.

---

## 19. RED futuro requerido

Cuando exista autorización del Owner:

- `/explore help`;
- repo list;
- repo prefix filter;
- repo read;
- repo search;
- knowledge list con source/authority class;
- knowledge read;
- knowledge search;
- malformed commands fail-closed;
- zero fallback a Conversation;
- zero LLM calls;
- Explorer unavailable sin repository root;
- Explorer y Engineering comparten baseline;
- Explorer reutiliza los mismos reader objects;
- zero new reader construction durante comandos;
- path validation sigue en E0;
- knowledge classification sigue en E1;
- truncation explícita;
- Kernel/Planner sin cambios;
- E0/E1/E5-A regressions verdes.

RED válido:

```text
new E5-B1 tests fail only because Explorer surface is absent
existing suite remains green
collection remains healthy
```

---

## 20. Stop conditions

STOP si E5-B1 requiere:

- modificar Kernel o Planner;
- modificar reglas E0/E1;
- crear segundo snapshot;
- crear store/index/cache;
- persistir sesiones;
- persistir findings/proposals;
- usar LLM para routing o summary;
- agregar write/Git mutation;
- implementar push o branch deletion;
- agregar dependencia UI;
- ampliar scope sin gate.

---

## 21. Resultado

```text
E5-B1 Read-only Explorer
G0      PASS
G1      DESIGN COMPLETE
RED     NOT AUTHORIZED
GREEN   NOT AUTHORIZED

E5-B2 Sessions                DEFERRED
E5-B3 Engineering Artifacts  DEFERRED
E5-F1 Governed Git Delivery  FUTURE CANDIDATE / NOT AUTHORIZED
```

Separación final:

```text
Explore != Authority
Read != Execute
Metadata != Permission
Git write operations != Explorer
```
