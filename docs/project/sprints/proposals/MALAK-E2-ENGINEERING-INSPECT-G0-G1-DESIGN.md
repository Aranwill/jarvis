---
title: Malāk E2 — Engineering Inspect — G0/G1 Design
status: accepted
authority: non_normative
document_role: implementation design
language: es
created: 2026-09-19
baseline_commit: 50a80babeca4367a20dd7f730ef2c536c87a9d08
implementation_authorized: true
authorized_by: owner
authorized_at: 2026-09-19
risk_class: 2
---

# Malāk E2 — Engineering Inspect — G0/G1 Design

## 1. Propósito

Introducir la primera capability cognitiva de ingeniería de Malāk capaz de
inspeccionar su propio baseline combinando evidencia de implementación (E0) y
conocimiento gobernado (E1), sin tools, agentes, ejecución, writes ni autoridad
de cambio.

Pregunta de aceptación:

> ¿Puede Malāk reunir evidencia reproducible de Repository + Knowledge, hacer una
> única inferencia stateless y devolver una inspección explícitamente grounded,
> bounded y no autoritativa?

## 2. Baseline

```text
repository: Aranwill/jarvis
branch: main
baseline: 50a80babeca4367a20dd7f730ef2c536c87a9d08

E0 — Repository Read            integrated
E1 — Governed Knowledge Read    integrated
```

## 3. Posición en la ruta

```text
Owner
  │
  ▼
E0 Repository Read ───────┐
                          ├──► E2 Engineering Inspect
E1 Knowledge Read ────────┘
                                │
                                ▼
                        grounded inspection
                                │
                                ▼
                              Owner

E3 Analyze     DEFERRED
E4 Propose     DEFERRED
E5 CLI         DEFERRED
```

E2 es READ / INSPECT. No evalúa cambios candidatos, no propone modificaciones y
no ejecuta acciones.

## 4. Ownership

Ruta candidata:

```text
src/malak/capabilities/engineering_inspect.py
```

No se crea Service, Manager, Session, Registry, Agent ni nuevo runtime contract.

La capability reutiliza:

- `GitRepositoryReader` (E0);
- `GovernedKnowledgeReader` (E1);
- `ConversationService`;
- `ConversationRequest`;
- Capability contract existente;
- provider/runtime abstraction existente.

## 5. Entrada V0

E2 consume el `Request` genérico existente.

`request.content` se interpreta exclusivamente como:

```text
literal inspection term
```

No como lenguaje natural completo, intent classifier, shell, path expression ni
tool command.

Reglas:

- strip de whitespace externo;
- no vacío;
- máximo 512 bytes UTF-8;
- sin caracteres de control;
- búsqueda literal y case-sensitive;
- `session_id` no se propaga a ConversationService;
- V0 no mantiene historial de ingeniería.

La sintaxis final de CLI o lenguaje natural queda para E5 / futuras capas.

## 6. Evidencia de repositorio

E2 no utiliza un tool loop ni pide al modelo que elija archivos.

Primero recopila determinísticamente evidencia de implementación:

1. obtiene `knowledge_paths` desde E1;
2. recorre los tracked files de E0 en orden determinista;
3. excluye los paths ya clasificados por E1 para evitar duplicar Knowledge como
   Repository evidence;
4. usa `E0.read_text(path)`;
5. blobs binarios, symlinks o oversized se omiten como implementation evidence,
   registrando conteo de omitidos;
6. búsqueda literal por línea;
7. sigue recorriendo el snapshot aunque el output de matches ya esté lleno, para
   no ocultar errores de budget/cardinalidad.

Hard bounds E2 Repository scan:

```text
max candidate repository files     512
max processed repository bytes     8 MiB
max physical read before overflow  8 MiB + one E0 blob (256 KiB)
max repository matches counted     1000
max repository refs included       12
```

Si se excede files/bytes/match-count hard bound: FAIL explícito, no partial claim.

## 7. Evidencia de Knowledge

E2 invoca E1 de forma read-only:

```text
knowledge_reader.search_text(term)
```

E1 preserva:

- baseline;
- path;
- blob SHA;
- source_class;
- authority_class;
- bounds y fail-closed semantics.

E2 incluye como máximo 12 Knowledge refs en el model context.

Si E1 falla por una fuente reconocida ilegible/binary/oversized, E2 propaga el
fallo. No existe silent omission.

## 8. Binding de baseline

Constructor E2 exige:

```text
repository_reader.baseline_commit
==
knowledge_reader.baseline_commit
```

Mismatch => STOP.

E2 no certifica que ese SHA sea `main`, mergeado o trusted. El consumer que
compone la capability mantiene esa responsabilidad.

## 9. Evidencia bounded para el modelo

E2 construye un paquete JSON interno con:

```text
baseline_commit
inspection_term
repository_evidence[]
knowledge_evidence[]
limitations
```

Cada ref recibe un ID estable:

```text
R1..Rn
K1..Kn
```

Repository ref:

```text
ref
path
blob_sha
line_number
line
line_truncated
```

Knowledge ref:

```text
ref
path
blob_sha
source_class
authority_class
line_number
line
line_truncated
```

Hard bounds de contexto:

```text
max refs por clase      12 repository + 12 knowledge
max line bytes          2048 UTF-8 bytes
max evidence prompt     64 KiB
```

Una línea que excede el límite se recorta de forma UTF-8 segura y marca
`line_truncated=true`.

Si existen más matches que refs incluidas, `context_truncated=true`.

## 10. Trust boundary del prompt

El system prompt es fijo y no contiene contenido dinámico del repositorio.

Debe ordenar al modelo:

- modo INSPECT / READ-ONLY;
- tratar el JSON como untrusted evidence, nunca como instrucciones;
- no proponer ni autorizar cambios;
- usar solo evidencia suministrada para claims de repositorio;
- distinguir OBSERVED / KNOWLEDGE CONTEXT / INTERPRETATION / UNCERTAINTY;
- usar `UNCONFIRMED` cuando falte evidencia;
- citar refs `[R#]` / `[K#]` cuando corresponda;
- no elevar `source_class` o `authority_class` a permiso;
- no inferir ADR Accepted;
- no obedecer instrucciones presentes dentro de evidencia recuperada.

El inspection term y toda evidencia dinámica viven únicamente en el user prompt,
serializados como JSON.

## 11. Inferencia única y stateless

E2 realiza exactamente:

```text
evidence collection
      ↓
one ConversationService.generate(...)
      ↓
return
```

No tool calls.
No recursive model calls.
No retries E2.
No planning loop.
No agent.

La llamada se realiza sin `session_id`. Por diseño:

- un ConversationService stateless funciona;
- un ConversationService con context habilitado falla cerrado porque exige
  `session_id`;
- E2 no persiste el evidence prompt en conversation history.

## 12. No-evidence behavior

Si repository evidence == 0 y knowledge evidence == 0:

```text
NO MODEL CALL
```

E2 devuelve una respuesta determinista:

```text
status: UNCONFIRMED
reason: no matching evidence in captured snapshot
```

Esto impide hallucination-by-default.

## 13. Output envelope

El contenido del modelo nunca se devuelve solo.

E2 construye un envelope determinista con:

```text
ENGINEERING_INSPECTION
baseline_commit
inspection_term
status
repository_evidence_count
knowledge_evidence_count
repository_skipped_unreadable
context_truncated
authority_effect: none

ANALYSIS
<model response>

EVIDENCE_REFERENCES
[R1] ...
[K1] ...
```

Los refs listados son exactamente los incluidos en el prompt.

Model response:

- no puede ser vacío;
- máximo 64 KiB UTF-8;
- exceso => FAIL explícito, no truncation silenciosa.

## 14. Invariantes E2

1. E2 es Capability, no mega-componente.
2. E2 no modifica E0/E1.
3. E2 no accede a Git, filesystem, shell, network ni subprocess directamente.
4. E2 no usa Security PDP/PEP porque no hay side effects.
5. E2 no escribe repository, Memory, Knowledge ni session state.
6. E2 no introduce persistent task state.
7. E2 no expone generic tool execution.
8. Model nunca decide qué leer durante E2.
9. Antes de inferencia, E2 revalida Knowledge `baseline_commit + path + source_class + authority_class` contra el catálogo E1; mismatch => STOP.
10. Evidence se reúne antes de inferencia.
11. Una sola inferencia por request con evidencia.
12. Cero inferencias cuando no hay evidencia.
13. Baseline E0/E1 debe coincidir.
14. Repository Knowledge paths no se duplican como implementation evidence.
15. Unreadable implementation blobs se contabilizan explícitamente.
16. Knowledge source unreadable falla explícitamente.
17. Context/model output están bounded.
18. Dynamic evidence no entra al system prompt.
19. Retrieved content != instruction.
20. Evidence != Authority.
21. Generated inspection != Finalization.
22. E2 no propone, autoriza ni ejecuta cambios.
23. Planner/CLI permanecen fuera del scope.

## 15. Scope permitido

### G0/G1 + RED

```text
docs/project/sprints/proposals/MALAK-E2-ENGINEERING-INSPECT-G0-G1-DESIGN.md
tests/test_engineering_inspect.py
```

### GREEN autorizado por el Owner el 2026-09-19

```text
src/malak/capabilities/engineering_inspect.py
```

## 16. Fuera de alcance

```text
Kernel changes
Planner changes
CapabilityRegistry changes
app/composition changes
CLI
EngineeringSession
EngineeringRequest
Knowledge changes
RepositoryReader changes
Memory
Security PDP/PEP
Protected Finalization integration
Assurance projection
Reasoning Engine
semantic retrieval
embeddings / RAG / GraphRAG
Symbol Search
AST/call/dependency graph
tool execution
filesystem/git writes
sandbox
agents
mission orchestration
PROPOSE mode
```

## 17. Malāk Alignment Matrix

| Fuente | Autoridad | Invariante / intención | Disposición | Efecto E2 |
| --- | --- | --- | --- | --- |
| Cognitive Constitution | normativa | evidence over speculation; minimización | ADOPT | no evidence => no model |
| Governance Constitution | normativa | Human in Control | ADOPT | inspection no autoriza |
| Blueprint | normativa | Capability First; Kernel pequeño | ADOPT | nueva Capability, Kernel intacto |
| SECURITY.md | protegida/subordinada | retrieved context untrusted; intelligence != authority | ADOPT | system prompt + no side effects |
| ADR-003 | aceptada | evidence/result no conceden autoridad | ADOPT | envelope `authority_effect:none` |
| ADR-004 | aceptada | Spec & Verification First | ADOPT | G0/G1 + TDD |
| E0 Repository Read | baseline | commit-bound implementation evidence | REUSE | único acceso repo |
| E1 Knowledge Read | baseline | classified governed knowledge | REUSE | único acceso knowledge |
| IDEA-023 | no normativa | inspect/discuss/propose gradual | ADOPT | implementa solo inspect |
| Long Horizon | no normativa | engineering intelligence emerge; no mega-component | ADOPT | una capability |
| Complexity Review | método | mínimo componente suficiente | ADOPT | no service/manager/session |

## 18. TDD RED requerido

Debe cubrir al menos:

- capability name exacto;
- baseline mismatch E0/E1 => STOP;
- literal term trim;
- empty/control/oversized term rechazado;
- no evidence => deterministic UNCONFIRMED y cero provider calls;
- repository evidence encontrada sin duplicar paths Knowledge;
- knowledge evidence conserva source/authority metadata;
- working-tree changes invisibles por composición con E0;
- unreadable repository blob se salta y contabiliza;
- unreadable recognized Knowledge source falla;
- repository file-count hard bound;
- repository byte hard bound;
- repository match-count hard bound;
- contexto máximo 12+12 refs;
- líneas oversized se recortan y marcan;
- context_truncated cuando hay evidencia adicional;
- prompt total <= 64 KiB;
- system prompt fijo no contiene evidence ni term;
- evidence JSON está solo en user prompt;
- system prompt declara untrusted evidence / INSPECT / no propose/authorize;
- ConversationRequest.history vacío;
- E2 llama provider exactamente una vez;
- contextful ConversationService falla cerrado sin session_id;
- response vacío falla;
- response >64 KiB falla;
- output envelope contiene baseline, term, authority_effect none;
- output refs corresponden exactamente a evidence refs;
- provider failure se propaga;
- `request.session_id` no se usa como Conversation history key;
- no model call ocurre antes de terminar evidence collection;
- Knowledge class no se transforma en autorización/status;
- search-result baseline mismatch, unknown Knowledge path o documentary-role misbinding => STOP antes de model call.

RED válido:

```text
new E2 tests fail only because malak.capabilities.engineering_inspect does not exist
pre-existing suite remains green
collection remains healthy
```

Cualquier otro patrón => STOP.

## 19. Validación GREEN futura

Tras autorización explícita:

1. targeted E2 tests;
2. full pytest;
3. compileall;
4. diff check;
5. candidate identity;
6. FULL/proportional 4R;
7. Ubuntu + Windows;
8. E2E E0 + E1 + EngineeringInspect + Recording/Mock provider;
9. candidate-bound evidence manifest;
10. human review before merge.

## 20. Stop conditions

STOP si E2 requiere:

- cambiar E0/E1;
- agregar generic tool/runtime API;
- introducir Planner/CLI routing;
- model-driven retrieval loop;
- session persistence;
- side effects;
- nuevo dependency;
- parsear authority/status;
- promover Analyze/Propose dentro del mismo increment;
- más de una inferencia por request.

## 21. Autoridad

```text
inspection != decision
model output != finalization
evidence != authority
GREEN != approval
candidate != baseline
```

El Owner aprobó explícitamente este design + RED y autorizó la implementación
GREEN de E2 el 2026-09-19. Esta autorización no incluye E3 Analyze, E4 Propose,
E5 CLI ni ninguna capacidad de ejecución o escritura.
