---
title: Malāk Progressive Cognitive Assurance Runtime — G0 Inspection
status: gate_evidence
authority: inspection_evidence
language: es
as_of_date: 2026-09-11
source_baseline: 5865da6a5e502fe71e35e2e38bc4cceaab9b3600
implementation_authorized: false
sprint_7_12_authorized: false
rdd_stage_2_authorized: false
related:
  - docs/architecture/adr/ADR-005-evidence-bound-final-response-transition.md
  - docs/architecture/blueprint.md
  - docs/governance/cognitive_constitution.md
  - docs/project/sprints/proposals/MALAK-PROGRESSIVE-COGNITIVE-ASSURANCE-RUNTIME-SCOPE-FREEZE-CANDIDATE.md
---

# Malāk Progressive Cognitive Assurance Runtime — G0 Inspection

## 1. Estado de autoridad

Este documento registra una inspección G0 del baseline vigente para localizar la transición real entre generación conversacional y respuesta final.

No autoriza implementación.

No congela contratos runtime.

No crea Sprint 7.12.

```text
Inspection != Specification
Specification != Implementation Authorization
Evidence != Authority
```

---

## 2. Pregunta G0

La inspección responde:

> ¿Dónde ocurre hoy la transición efectiva desde un output de provider/runtime hasta una respuesta presentada al usuario, qué componentes poseen cada responsabilidad y qué gaps impiden materializar correctamente R-022 / CC-011 / CC-012?

---

## 3. Fuentes de código inspeccionadas

Baseline:

```text
Aranwill/jarvis
main@5865da6a5e502fe71e35e2e38bc4cceaab9b3600
```

Ruta principal inspeccionada:

```text
src/malak/app/cli.py
src/malak/app/composition.py
src/malak/kernel/kernel.py
src/malak/contracts/capability.py
src/malak/capabilities/conversation.py
src/malak/services/conversation_service.py
src/malak/services/conversation_context.py
src/malak/providers/runtime_provider.py
src/malak/core/conversation.py
src/malak/core/response.py
```

Cobertura auxiliar revisada:

```text
tests/test_conversation_execution_path.py
tests/test_conversation_capability.py
tests/test_conversation_service.py
```

Fuentes normativas relevantes:

```text
docs/architecture/blueprint.md
docs/architecture/adr/ADR-005-evidence-bound-final-response-transition.md
docs/governance/cognitive_constitution.md
```

---

## 4. Ruta runtime real observada

La ruta conversacional vigente es:

```text
CLI
  ↓
Request
  ↓
Kernel.receive()
  ↓
Planner.resolve()
  ↓
CapabilityRegistry.get()
  ↓
ConversationCapability.execute()
  ↓
ConversationService.generate()
  ↓
ConversationProviderRegistry.get()
  ↓
RuntimeConversationProvider.generate()
  ↓
LLMRuntime.generate()
  ↓
ConversationResponse
  ↓
ConversationService
  ↓
ConversationCapability returns response.content
  ↓
Kernel wraps content in Response
  ↓
CLI prints response.content
```

No se observó una frontera explícita de assurance/finalization entre `ConversationResponse` y la presentación al usuario.

---

## 5. Punto exacto de elevación actual

`ConversationCapability.execute()` recibe un `ConversationResponse` desde `ConversationService.generate()` y devuelve directamente:

```text
response.content
```

Ese `str` es recibido por `Kernel.receive()`, que lo envuelve inmediatamente como:

```text
Response(
    content=result,
    source=capability.name,
)
```

Por tanto, para la ruta conversacional actual:

```text
provider/runtime output
→ ConversationResponse.content
→ capability result
→ Response.content
→ user-visible output
```

No existe un estado intermedio formal equivalente a `Candidate Response` ni evidencia de una validación aplicable antes de crear la respuesta presentada.

### Hallazgo G0-01

```text
CURRENT STATE:
Generation ≈ Finalization in the conversation path
```

Esto no significa que provider y Kernel sean conceptualmente equivalentes. Significa que el código actual no materializa todavía la transición protegida exigida por R-022.

---

## 6. Ownership observado

### `RuntimeConversationProvider`

Responsabilidad observada:

```text
ConversationRequest
→ LLMRuntime.generate()
→ ConversationResponse
```

Es un adapter de infraestructura/runtime.

No debe poseer finalización cognitiva.

### `ConversationService`

Responsabilidad declarada y observada:

- resolver provider;
- enriquecer request con historial;
- delegar generación;
- registrar intercambios exitosos cuando existe contexto.

Su docstring excluye explícitamente governance policies.

Por tanto no aparece, en el baseline actual, como propietario natural de Cognitive Assurance policy.

### `ConversationCapability`

Responsabilidad observada:

- adaptar `Request` genérico a `ConversationRequest`;
- invocar `ConversationService`;
- convertir `ConversationResponse` en el valor devuelto a Kernel.

Es la frontera existente inmediatamente posterior a generación y anterior a la respuesta genérica del Kernel.

### `Kernel`

Responsabilidad observada:

- guard de request vacío;
- resolver capability;
- ejecutar capability;
- envolver resultado en `Response`.

El Blueprint prohíbe incorporar lógica de negocio al Kernel y ADR-005 no autoriza cambios de Kernel por sí misma.

### `CLI`

Responsabilidad observada:

- componer y ejecutar la interacción;
- imprimir `response.content`.

No debe poseer policy cognitiva; es Interface Layer.

---

## 7. Seam candidato observado

El seam mínimo ya existente para estudiar en G1 es:

```text
ConversationService.generate()
        ↓
ConversationResponse
        ↓
[ protected finalization seam ]
        ↓
ConversationCapability result
        ↓
Kernel Response
```

Esto favorece, como hipótesis G1 y NO como decisión congelada, mantener el primer slice fuera del Kernel y fuera del provider/runtime.

```text
preferred inspection direction:
ConversationCapability boundary
or a dependency injected into that boundary
```

La inspección no demuestra todavía que sea necesario crear un nuevo service/layer/manager.

Esto es consistente con ADR-005:

```text
architectural property
!= automatic new component
```

---

## 8. Hallazgo crítico de historial conversacional

Cuando `ConversationService` opera con `InMemoryConversationContext`, actualmente ejecuta:

```text
provider.generate(...)
        ↓
response
        ↓
context.record_exchange(
    user_content=request.prompt,
    assistant_content=response.content,
)
        ↓
return response
```

Esto ocurre **antes** de cualquier futura frontera de assurance situada después de `ConversationService.generate()`.

Por tanto, si un candidate fuera posteriormente:

```text
QUALIFY
ABSTAIN
BLOCK
```

o transformado antes de Final Response, el contexto actual ya habría almacenado el contenido bruto del provider como mensaje `assistant`.

### Hallazgo G0-02

```text
raw generated candidate
may enter conversational history
before protected finalization
```

Eso sería incompatible con una semántica fuerte de:

```text
Generation != Finalization
```

si el historial de conversación representa lo que Malāk efectivamente dijo al usuario.

### Consecuencia para G1

G1 deberá definir explícitamente la semántica del historial.

La dirección más segura a evaluar es:

```text
history records Final Response
not unaccepted raw Candidate Response
```

No se autoriza aún modificar `ConversationService` ni `InMemoryConversationContext`.

---

## 9. Ausencia de evidence-bearing inputs en la ruta actual

`ConversationResponse` contiene únicamente:

```text
content
model
provider
```

No transporta:

- evidence references;
- provenance;
- contradiction state;
- source authority;
- temporal applicability;
- material claim set;
- required assurance floor;
- achieved assurance;
- policy version;
- security disposition.

`Response` contiene únicamente:

```text
content
source
```

### Hallazgo G0-03

La ruta vigente ofrece un lugar físico para insertar una frontera, pero **no ofrece todavía información suficiente para ejecutar una policy evidence-bound general**.

```text
seam exists
!=
assurance inputs exist
```

Por tanto sería incorrecto introducir una implementación que aparente evaluar evidencia cuando el runtime no la transporta.

---

## 10. Materialidad no representada

R-022 protege específicamente la transición de Candidate Response con afirmaciones materiales.

El runtime actual no contiene un contrato explícito para distinguir:

```text
non-material / deterministic response
vs
material factual response
```

Tampoco existe un clasificador autorizado de materialidad en la ruta conversacional.

### Hallazgo G0-04

G1 no puede asumir automáticamente que:

```text
all conversation == material
```

ni que:

```text
LLM confidence == materiality/evidence state
```

La materialidad y el assurance applicability deberán quedar definidos mediante inputs/policy explícitos o una regla conservadora demostrable antes de implementar.

---

## 11. Capability genérica y scope inicial

El contrato base `Capability.execute(Request)` no tipa el resultado y el Kernel envuelve el resultado de cualquier capability como `Response.content`.

El baseline posee además `EchoCapability`, que devuelve determinísticamente `request.content`.

Esto implica:

```text
Kernel response construction
is generic
```

pero no demuestra que el primer slice de assurance deba modificar el contrato `Capability` completo.

### Hallazgo G0-05

Generalizar de inmediato assurance a todas las capabilities ampliaría el scope sin necesidad demostrada.

La ruta probabilística real actualmente relevante es `ConversationCapability`.

Dirección G1 recomendada:

```text
prove protected finalization on conversation first
without changing generic Capability contract
unless a hard invariant cannot otherwise be satisfied
```

---

## 12. Bypass map observado

### Bypass B1 — Provider output → capability return

Actual:

```text
ConversationResponse.content
→ return directly
```

Estado:

```text
OPEN
```

### Bypass B2 — Candidate enters history before finalization

Actual:

```text
provider response
→ context.record_exchange()
→ later capability return
```

Estado:

```text
OPEN
```

### Bypass B3 — Kernel wraps arbitrary capability result

Actual:

```text
Capability.execute()
→ Kernel Response
```

Estado:

```text
GENERIC BY DESIGN
```

No debe tratarse como defecto global sin distinguir capabilities deterministas de outputs cognitivos materiales.

### Bypass B4 — CLI presentation

La CLI solo presenta el `Response` recibido desde Kernel.

Estado:

```text
NO independent cognition bypass observed
```

### Bypass B5 — Direct src caller of ConversationService

La inspección de código encontró la ruta de producto mediante `ConversationCapability`; no se observó otra ruta de producto en `src/` que llame a `_service.generate()` y presente directamente su resultado al usuario.

Los usos directos adicionales observados pertenecen a tests/fixtures.

Estado:

```text
NO second product presentation path observed
```

---

## 13. Restricciones derivadas de R-022 / ADR-005

La evidencia normativa obliga a preservar:

```text
provider output != Final Response
candidate validation cannot be bypassed when applicable
Kernel is not automatically the assurance owner
no automatic new layer/service/manager
progressive / proportional assurance
no mandatory multi-model verification
Evidence != Authority
```

Por tanto G1 no debe:

- introducir assurance en `LLMRuntime`;
- introducir assurance en `RuntimeConversationProvider`;
- colocar policy cognitiva en CLI;
- convertir Kernel en reasoning/assurance engine;
- crear un servicio nuevo solo por nomenclatura;
- inventar evidence fields sin producer/semantics definidos;
- registrar raw candidate como respuesta histórica aceptada si el outcome no lo finaliza.

---

## 14. Resultado G0

```text
G0 RESULT: PASS / ADAPT
```

### PASS

Existe un gap real y observable entre generación y finalización.

Existe un seam concreto inmediatamente después de la generación conversacional y antes del retorno final de `ConversationCapability`.

No se observó una segunda ruta de producto que obligue a modificar Kernel para cerrar el primer slice conversacional.

### ADAPT

El scope freeze inicial debe adaptarse a dos hechos del baseline:

1. `ConversationService` persiste en historial efímero el candidate bruto antes del seam candidato;
2. la ruta actual no transporta evidencia/materialidad suficiente para ejecutar una policy evidence-bound general.

Por tanto:

```text
G0 PASS
!=
ready to implement ACCEPT/QUALIFY/ABSTAIN/BLOCK semantics immediately
```

---

## 15. Requisitos obligatorios para G1

Antes de solicitar autorización de implementación, G1 deberá congelar como mínimo:

### G1-R1 — Ownership exacto

Definir qué frontera existente posee:

```text
Candidate Response
→ assurance evaluation
→ Final Response
```

sin modificar Kernel salvo blocker demostrado.

### G1-R2 — Semántica del historial

Definir cuándo se registra un intercambio y garantizar que un candidate no aceptado no se convierta en historial `assistant` como si hubiera sido Final Response.

### G1-R3 — Minimal Candidate contract

Definir el mínimo dato necesario para preservar:

```text
content
provider/model provenance already available
request binding if required
```

sin implementar Content Identity G2 incidentalmente.

### G1-R4 — Assurance applicability/materiality

Definir de dónde proviene la decisión de que un check aplica.

No se permite inferirla mediante confianza del modelo.

### G1-R5 — Evidence input semantics

Definir qué evidencia real existe en el primer slice.

Si no existe evidence-bearing input suficiente, reducir el primer slice a propiedades demostrables de no-bypass/finalization en vez de fingir evidence sufficiency.

### G1-R6 — Outcome semantics

Determinar si el primer slice necesita realmente cuatro outcomes runtime o una semántica mínima menor.

Los placeholders G1 previos no deben convertirse automáticamente en API.

### G1-R7 — Failure behavior

Estado desconocido, malformed input o evaluator failure debe ser fail-safe y no elevar candidate a Final Response.

### G1-R8 — Tests de no-bypass

Como mínimo deberán demostrar:

```text
provider candidate cannot reach user-visible Response through the integrated path without crossing the boundary
non-finalized candidate is not recorded as accepted assistant history
finalized content is the content recorded/presented
Kernel remains free of new cognitive business logic
provider/runtime remain unaware of assurance implementation
```

---

## 16. Stop conditions confirmadas por G0

Detener o separar gate si G1 demuestra que el primer slice exige:

- Content Identity G2;
- Persistence Authorization;
- Memory/Knowledge/retrieval wiring;
- nuevo Security authority;
- modificación sustancial del Kernel;
- cambio global del contrato `Capability` sin necesidad demostrada;
- classifier probabilístico adicional obligatorio;
- evidencia inexistente presentada como verificada;
- persistencia nueva;
- dependencias externas nuevas.

---

## 17. Hipótesis G1 recomendada

La hipótesis más pequeña compatible con la evidencia actual es:

```text
ConversationProvider / Runtime
        ↓
ConversationResponse (generated candidate)
        ↓
ConversationCapability-owned finalization seam
        ↓
minimal deterministic assurance/finalization contract
        ↓
accepted/qualified/abstained/blocked final content
        ↓
record only finalized conversational exchange
        ↓
Kernel receives ordinary capability result
        ↓
Response
```

La frase `ConversationCapability-owned` es una hipótesis de diseño para G1, no una decisión normativa ni autorización de implementación.

Una alternativa mejor puede elegirse si preserva ownership claro con menor cambio.

---

## 18. Decisión de avance

```text
G0 inspection:
COMPLETE

runtime implementation:
NOT AUTHORIZED

exact contracts:
NOT FROZEN

recommended next gate:
G1 — exact ownership + contracts + history semantics + applicability/evidence semantics

Sprint 7.12:
NOT AUTHORIZED

Candidate Content Identity G2:
NOT AUTHORIZED

Persistence Authorization:
NOT AUTHORIZED

RDD Stage 2:
NOT AUTHORIZED
```

La evidencia actual justifica continuar a G1 de diseño, pero no justifica todavía modificar `src/` o `tests/`.