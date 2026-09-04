---
title: Sprint 7.10 — Conversation Session Isolation Foundation
status: en_cierre
authority: documentación operativa derivada
as_of_date: 2026-09-04
baseline_commit: 43041f920a1b8063491e6d5cabcb1fd887bdc7a8
branch: feat/sprint-7.10-session-isolation
implementation_head: 0735223
language: es
---

# Sprint 7.10 — Conversation Session Isolation Foundation

## Estado

```text
IMPLEMENTACIÓN FUNCIONAL COMPLETA
CIERRE DOCUMENTAL EN CURSO
```

Sprint 7.10 fue debatido y aprobado explícitamente por el propietario
el 2026-09-04.

La implementación funcional quedó validada antes del cierre documental.

Este sprint no autoriza automáticamente ninguna unidad posterior.

---

## Baseline inicial

El sprint comenzó desde:

```text
43041f920a1b8063491e6d5cabcb1fd887bdc7a8
```

Rama permanente de origen:

```text
main
```

Rama temporal de trabajo:

```text
feat/sprint-7.10-session-isolation
```

Estado inicial reproducido:

```text
HEAD == origin/main
working tree: clean
tests focalizados Kernel/Capability: 7 passed
```

Este commit constituye el punto de rollback absoluto del Sprint 7.10.

---

## Necesidad comprobada

Sprint 7.9 incorporó continuidad conversacional efímera mediante
`InMemoryConversationContext`.

Sin embargo, el contexto era conceptualmente único para toda la instancia
de `ConversationService`.

El contrato `Request` ya contenía:

```text
session_id
```

pero el Kernel reducía prematuramente la ejecución de Capability a:

```text
request.content
```

Por lo tanto, la identidad de sesión no alcanzaba el subsistema
conversacional.

La necesidad comprobada fue:

```text
preservar Request.session_id
→ propagarlo hasta ConversationService
→ aislar el historial por sesión
```

sin introducir persistencia ni Memory.

---

## Objetivo

Garantizar aislamiento determinista del contexto conversacional efímero:

```text
session-A
  └── history-A

session-B
  └── history-B
```

con la invariante:

```text
history-A nunca contiene history-B
history-B nunca contiene history-A
```

El aislamiento debe permanecer:

- exclusivamente en memoria;
- fuera del Kernel;
- fuera de `SecurityContext`;
- independiente de runtimes concretos;
- independiente de providers concretos;
- sin persistencia.

---

## Fuera de alcance

Sprint 7.10 no incorpora:

- persistencia;
- filesystem conversation store;
- database;
- Memory;
- embeddings;
- vector database;
- RAG;
- GraphRAG;
- agentes;
- tools;
- Sandbox;
- navegación;
- red;
- cambios de autorización;
- cambios de `SecurityContext`;
- nonce;
- replay protection;
- identidad criptográfica;
- Resource Governance avanzado.

---

## Decisión arquitectónica

No se creó un nuevo DTO universal de ejecución.

El contrato existente:

```text
Request
├── content
├── session_id
├── request_id
└── created_at
```

ya contenía la metadata necesaria.

La frontera de Capability evolucionó desde:

```text
Capability.execute(request.content)
```

hacia:

```text
Capability.execute(request)
```

Esto preserva metadata existente sin introducir:

```text
CapabilityExecutionRequest
CapabilityExecutionResult
ExecutionEnvelope
```

La necesidad se resolvió utilizando contratos ya presentes.

---

## Arquitectura resultante

```text
Request
  │
  ▼
Kernel.receive()
  │
  ▼
Capability.execute(Request)
  │
  ▼
ConversationCapability
  │
  ├── request.content
  └── request.session_id
          │
          ▼
ConversationService
          │
          ▼
InMemoryConversationContext
          │
          ├── session-A
          │     └── exchanges
          │
          └── session-B
                └── exchanges
```

El Kernel continúa sin almacenar estado conversacional.

---

## Contrato del contexto conversacional

`InMemoryConversationContext` mantiene:

```text
_sessions: session_id → exchanges
```

Operaciones:

```text
snapshot(session_id)
record_exchange(session_id, ...)
clear(session_id)
```

Propiedades:

- `snapshot()` es específico de sesión;
- `snapshot()` de una sesión desconocida devuelve historial vacío;
- una lectura no necesita crear explícitamente una sesión;
- `record_exchange()` crea el contenedor de sesión bajo demanda;
- `clear(session_id)` es idempotente;
- `clear(session_id)` elimina únicamente esa sesión;
- `max_exchanges` se aplica independientemente por sesión;
- eviction de una sesión no afecta ninguna otra.

---

## Integridad ante errores

Se conserva la regla establecida en Sprint 7.9:

```text
snapshot
→ provider.generate
→ success
→ record_exchange
```

Ante fallo:

```text
snapshot
→ provider.generate
→ failure
→ context unchanged
```

Además, el fallo en una sesión no modifica el historial de ninguna otra.

---

## ConversationService

Cuando no existe contexto:

```text
ConversationService(registry)
```

continúa funcionando sin requerir `session_id`.

Cuando existe contexto:

```text
ConversationService(
    registry,
    context=...
)
```

`session_id` es obligatorio.

No existe una sesión global implícita ni un fallback `"default"`.

La ausencia de `session_id` con contexto habilitado produce un error
explícito.

---

## CLI Session Lifecycle

La CLI ya no utiliza:

```text
session_id="cli"
```

como identidad global fija.

Al iniciar la CLI:

```text
crear session_id UUID
```

Los prompts posteriores reutilizan esa sesión.

El comando:

```text
new
```

ejecuta:

```text
clear(session_actual)
→ generar nueva UUID
→ continuar con session_nueva
```

Por lo tanto, `new` representa una frontera real de conversación y no
solamente el vaciado de una lista compartida.

---

## Invariantes protegidos

Sprint 7.10 garantiza:

```text
Request.session_id llega intacto a ConversationCapability
session A nunca observa historial de B
session B nunca observa historial de A
clear(A) no modifica B
eviction(A) no modifica B
provider failure no modifica el contexto
new crea una nueva identidad de sesión
no existe sesión global/default implícita
```

También se preserva:

```text
Planner: sin cambios
SecurityContext: sin cambios
authorization: sin cambios
providers: sin cambios
runtimes: sin cambios
observability: sin cambios
persistence: inexistente
```

---

## Archivos funcionales alcanzados

### Commit 1 — frontera de ejecución

```text
a0209a4
refactor(capability): preserve request metadata across execution boundary
```

Archivos:

```text
src/malak/contracts/capability.py
src/malak/kernel/kernel.py
src/malak/capabilities/echo.py
src/malak/capabilities/conversation.py
tests/test_capability_registry.py
tests/test_kernel.py
tests/test_conversation_capability.py
```

### Commit 2 — aislamiento conversacional

```text
0735223
feat(conversation): isolate in-memory context by session
```

Archivos:

```text
src/malak/app/cli.py
src/malak/capabilities/conversation.py
src/malak/services/conversation_context.py
src/malak/services/conversation_service.py
tests/test_cli.py
tests/test_conversation_context.py
tests/test_conversation_service.py
```

---

## Gates ejecutados

### Gate 0 — baseline

```text
HEAD == origin/main
working tree clean
```

### Gate 1 — Capability / Kernel

Baseline:

```text
7 passed
```

Después de preservar `Request`:

```text
7 passed
```

Validación ampliada:

```text
13 passed
```

### Gate 2 — Conversation Context

Baseline:

```text
14 passed
```

Contexto aislado:

```text
9 passed
```

### Gate 3 — ConversationService

```text
context + service: 20 passed
integration path: 6 passed
```

### Gate 4 — CLI

```text
CLI: 27 passed
conversation accumulated gate: 53 passed
```

### Gate 5 — validación completa

```text
pytest: 372 passed
compileall: PASS
git diff --check: PASS
working tree: clean
```

---

## Resultado

Sprint 7.10 establece una frontera estable de sesión conversacional
sin introducir Memory.

La separación conceptual resultante es:

```text
Conversation History != Memory != Knowledge
```

Conversation History representa únicamente intercambios efímeros asociados
a una sesión activa.

No representa recuerdo persistente, conocimiento recuperable ni autoridad.

---

## Definition of Done

```text
[x] Request.session_id llega intacto a ConversationCapability
[x] session A nunca observa history de session B
[x] session B nunca observa history de session A
[x] max_exchanges opera independientemente por sesión
[x] clear(A) no modifica B
[x] provider failure no modifica contexto
[x] new rota a un session_id nuevo
[x] no existe sesión global/default implícita
[x] no existe persistencia
[x] SecurityContext permanece sin cambios
[x] Planner permanece sin cambios
[x] full pytest PASS
[x] compileall PASS
[x] git diff --check PASS
```

---

## Cierre pendiente

Antes de considerar integrado el sprint:

```text
reconciliar project_context.md
→ reconciliar implementation_roadmap.md
→ ejecutar gates documentales
→ commit de cierre
→ push de rama
→ PR
→ revisión
→ merge a main
→ verificar main
→ reconciliar Vault contra SHA integrado
```

No se autoriza automáticamente ningún Sprint 7.11.

---

## Rollback

Rollback absoluto:

```text
43041f920a1b8063491e6d5cabcb1fd887bdc7a8
```

Rollback de la capa de aislamiento:

```text
a0209a4
```

Rollback del último candidato funcional:

```text
0735223^
```

Cualquier desviación detectada durante el cierre requiere:

```text
STOP
→ no ampliar alcance
→ revisar evidencia
→ corregir únicamente el cierre
```
