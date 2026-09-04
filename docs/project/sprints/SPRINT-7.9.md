---
title: Sprint 7.9 — Conversation Continuity Foundation
status: en_ejecucion
authority: documentación operativa derivada
as_of_date: 2026-09-03
as_of_commit: d58b8ec98d48f5e2eac115d1d54b193e1df617fd
branch: sprint/7.9-conversation-continuity
language: es
---

# Sprint 7.9 — Conversation Continuity Foundation

## Estado

```text
EN EJECUCIÓN
```

El Sprint 7.9 fue debatido y aprobado explícitamente por el propietario
el 2026-09-03.

Su activación autoriza únicamente el trabajo definido dentro de este sprint.

No autoriza automáticamente:

- nuevos sprints;
- Memory persistente;
- agentes;
- tools;
- navegación;
- Internet;
- Sandbox;
- RAG o GraphRAG;
- cambios de autoridad;
- cambios del Kernel;
- cambios generales del contrato Capability;
- cambios de SecurityContext;
- incorporación de capacidades futuras registradas como ideas o conceptos.

Cada paquete deberá implementarse, probarse, revisarse y aceptarse antes de
avanzar al siguiente.

Ante una desviación arquitectónica o una necesidad no prevista:

```text
STOP GATE
→ no commit
→ revisar diseño
→ rollback al último gate aceptado
```

---

## Baseline inicial

El sprint comienza desde:

```text
2864435401353e5abcfcb51fc276361a0225c2b7
```

Rama permanente de origen:

```text
main
```

Rama temporal de trabajo:

```text
sprint/7.9-conversation-continuity
```

Estado técnico reproducido localmente antes de crear la rama:

```text
Python 3.12.10
virtual environment: .venv
pytest: 348 passed
compileall: PASS
git diff --check: PASS
working tree: clean
HEAD == origin/main
```

Este commit constituye el punto de rollback absoluto del Sprint 7.9.

---

## Necesidad comprobada

Sprint 7.8 estableció la primera ruta cognitiva conversacional end-to-end:

```text
CLI
→ Kernel
→ Planner
→ CapabilityRegistry
→ ConversationCapability
→ ConversationService
→ ConversationProviderRegistry
→ RuntimeConversationProvider
→ LLMRuntime
→ Response
```

La ruta es funcional pero permanece esencialmente stateless entre turnos.

Actualmente una nueva solicitud conversacional no recibe de forma estructurada
los intercambios anteriores de la conversación activa.

Antes de introducir Memory persistente, Knowledge, RAG o mecanismos de
recuperación de largo plazo, Malāk necesita evidencia operativa sobre una
capacidad más pequeña:

```text
mantener continuidad dentro de una conversación activa
```

Sprint 7.9 implementará esa capacidad de forma efímera, limitada, explícita y
reversible.

---

## Objetivo

Permitir que una única conversación activa conserve contexto entre varios
turnos mientras vive el proceso de aplicación, sin introducir persistencia.

La continuidad deberá:

- existir fuera del LLM;
- existir fuera del Kernel;
- mantenerse únicamente en memoria;
- utilizar mensajes estructurados;
- conservar intercambios completos;
- aplicar un límite explícito;
- permitir limpieza explícita;
- no sobrevivir al proceso;
- no conceder autoridad;
- no convertirse en Memory persistente.

Principio operativo:

```text
Malāk puede mantener una conversación
sin afirmar todavía que Malāk recuerda.
```

---

## Fuentes consultadas

La implementación se evalúa contra el corpus vigente de Malāk.

Fuentes normativas y arquitectónicas aplicables:

- Blueprint vigente;
- Constitución Cognitiva;
- Constitución de Gobernanza;
- arquitectura del Kernel;
- contratos vigentes;
- Security Control Plane;
- Secure Context Lifecycle;
- decisiones cerradas de los Sprints 7.0 a 7.8.

Fuentes operativas y derivadas:

- `docs/project/project_context.md`;
- `docs/project/implementation_roadmap.md`;
- `docs/project/sprints/SPRINT-7.8.md`;
- documentación de desarrollo y entorno.

Referencias conceptuales y de ideas:

- `documents/projects/jarvis/ideas.md`;
- patrón candidato `Context Continuity Outside the LLM`;
- `docs/project/concepts/`;
- referencias futuras relacionadas con Memory, Resource Governance,
  Sandbox, Evidence, agentes y trabajo de horizonte largo.

Regla de uso:

```text
consultar todo
→ implementar solo lo autorizado
```

Ideas, conceptos y roadmap derivado proporcionan información y restricciones
de diseño.

No conceden autoridad de implementación por sí mismos.

---

## Decisión arquitectónica principal

La continuidad conversacional deberá permanecer fuera del Kernel.

No se utilizará `SecurityContext` como contenedor de historial conversacional.

Seguridad y conversación representan dominios distintos.

Conceptualmente:

```text
SecurityContext
→ identidad, autenticación, lifecycle y autoridad de seguridad

Conversation Continuity
→ mensajes temporales de una conversación activa
```

Aunque puedan correlacionarse en una evolución posterior, no deberán
conflarse.

---

## Restricción sobre Request y Capability

El contrato actual del Kernel recibe un `Request` que contiene `session_id`.

Sin embargo, la frontera actual ejecuta la capability mediante el contenido
conversacional existente.

Sprint 7.9 no utilizará esta necesidad aislada para generalizar prematuramente
el contrato Capability.

No se incorporarán en este sprint contratos universales como:

```text
CapabilityExecutionRequest
CapabilityExecutionResult
```

La decisión de Sprint 7.8 permanece vigente:

```text
una abstracción general solo deberá introducirse
cuando múltiples capabilities reales demuestren una necesidad común
```

---

## Arquitectura objetivo

Dirección mínima:

```text
CLI
  ↓
Kernel.receive()
  ↓
Planner
  ↓
CapabilityRegistry
  ↓
ConversationCapability
  ↓
ConversationService
  │
  ├── read conversation snapshot
  │
  ↓
ConversationProviderRegistry
  ↓
RuntimeConversationProvider
  ↓
LLMRuntime
  ↓
ConversationResponse
  │
  ↓
ConversationService
  │
  └── record successful exchange
```

La continuidad deberá ser proporcionada mediante una dependencia externa y
acotada, conceptualmente equivalente a:

```text
InMemoryConversationContext
```

Responsabilidades mínimas:

```text
snapshot()
record_exchange()
clear()
bounded history
```

No deberá conocer:

```text
Kernel
Planner
Ollama
SecurityContext
Vault
filesystem
database
Memory
RAG
agents
tools
```

---

## Modelo conversacional mínimo

Se incorporará un mensaje estructurado equivalente a:

```text
ConversationMessage
├── role
└── content
```

Roles iniciales admitidos para historial:

```text
user
assistant
```

El `system_prompt` continuará siendo responsabilidad separada del historial
ordinario.

`ConversationRequest` deberá preservar sus campos existentes y evolucionar de
forma aditiva.

Dirección conceptual:

```text
ConversationRequest
├── prompt
├── model
├── system_prompt
└── history
```

No se eliminarán contratos existentes únicamente para introducir continuidad.

---

## Política de ventana inicial

El contexto utilizará inicialmente una ventana limitada a:

```text
6 intercambios completos
```

Un intercambio está compuesto por:

```text
user
assistant
```

Cuando se exceda el límite se descartará el intercambio completo más antiguo.

No se descartará únicamente uno de los dos mensajes de un intercambio.

El valor inicial constituye una política conservadora para validar el
mecanismo.

No representa una política definitiva de Resource Governance.

Sprint 7.9 no implementará todavía:

- token budgeting avanzado;
- compresión automática;
- summarization;
- priorización semántica;
- selección dinámica de recuerdos.

---

## Regla de integridad del contexto

El contexto solo deberá modificarse después de una generación exitosa.

Secuencia obligatoria:

```text
snapshot
→ generate
→ successful response
→ record_exchange
```

Ante error:

```text
snapshot
→ generate
→ failure
→ context unchanged
```

No se admitirá dejar el historial en estado parcial como:

```text
user almacenado
assistant inexistente
```

---

## Runtime Independence

La continuidad deberá expresarse mediante contratos conversacionales.

No deberá almacenar conocimiento específico de Ollama dentro del contexto.

Para runtimes capaces de conversación estructurada se preferirá una
representación estructurada de mensajes en lugar de concatenar manualmente
historial dentro de un prompt plano.

La adaptación concreta hacia Ollama pertenece exclusivamente a
`OllamaRuntime`.

Antes de cerrar el paquete correspondiente deberá verificarse la API oficial
vigente del runtime.

---

## Compatibilidad obligatoria

La evolución deberá ser aditiva.

Una construcción sin contexto conversacional deberá continuar siendo válida.

Conceptualmente:

```text
ConversationService(registry)
```

deberá conservar comportamiento compatible con Sprint 7.8.

Y:

```text
ConversationService(
    registry,
    context=...
)
```

habilitará continuidad explícita.

No se deberá convertir la continuidad en una dependencia obligatoria de todas
las ejecuciones conversacionales.

---

## Invariantes protegidos

Durante Sprint 7.9 no se espera modificar:

```text
src/malak/kernel/kernel.py
src/malak/services/planner.py
src/malak/contracts/capability.py
src/malak/capabilities/conversation.py
src/malak/security/*
```

Especialmente:

```text
Kernel: no debe incorporar estado conversacional
Planner: no debe incorporar estado conversacional
Capability contract: no debe generalizarse
SecurityContext: no debe almacenar historial
```

Si la implementación exige modificar alguno de estos límites para hacer
funcionar el sprint:

```text
STOP GATE
```

La necesidad deberá debatirse antes de continuar.

---

## Paquetes previstos

### 7.9-A — Sprint Activation & Architecture Freeze

Objetivo:

- certificar baseline;
- registrar aprobación;
- fijar alcance;
- documentar invariantes;
- registrar fuentes consultadas;
- definir gates;
- definir rollback.

Resultado:

```text
documentación activa
código sin cambios
baseline reproducido
```

---

### 7.9-B — Conversation Contract Extension

Objetivo:

Introducir de forma aditiva:

```text
ConversationMessage
ConversationRequest.history
```

sin integrar todavía almacenamiento de contexto.

Condiciones:

- compatibilidad con contratos existentes;
- tests focalizados;
- full suite verde;
- Kernel sin cambios;
- Capability contract sin cambios.

Rollback:

```text
volver al commit de 7.9-A
```

---

### 7.9-C — Bounded In-Memory Conversation Context

Objetivo:

Crear un componente efímero responsable únicamente de:

```text
snapshot
record_exchange
clear
bounded history
```

Condiciones:

- almacenamiento exclusivamente en RAM;
- límite inicial de 6 intercambios;
- snapshots sin mutación externa;
- eliminación por intercambio completo;
- ningún consumidor integrado todavía.

Rollback:

```text
volver al commit de 7.9-B
```

---

### 7.9-D — ConversationService Integration

Objetivo:

Integrar el contexto de forma opcional en `ConversationService`.

Secuencia:

```text
read snapshot
→ generate
→ successful response
→ record exchange
```

Condiciones:

- sin contexto: comportamiento compatible con 7.8;
- con contexto: historial disponible al provider;
- fallo de generación: contexto intacto;
- limpieza explícita disponible;
- ninguna dependencia del Kernel.

Rollback:

```text
volver al commit de 7.9-C
```

---

### 7.9-E — Structured Runtime Conversation Adapter

Objetivo:

Adaptar `OllamaRuntime` para transportar conversación estructurada mediante la
API conversacional oficial vigente del runtime.

Dirección prevista:

```text
system message?
→ history
→ current user message
```

Condiciones:

- orden preservado;
- prompt actual siempre último;
- keep_alive preservado;
- timeout preservado;
- métricas preservadas;
- errores controlados;
- tests deterministas sin dependencia obligatoria de un servicio Ollama activo.

Si la API real vigente requiere una modificación arquitectónica no prevista:

```text
STOP GATE
```

Rollback:

```text
volver al commit de 7.9-D
```

---

### 7.9-F — CLI Conversation Continuity

Objetivo:

Mantener una conversación efímera durante una ejecución de CLI.

Incorporar un comando explícito:

```text
new
```

que deberá limpiar únicamente el contexto conversacional activo.

No deberá:

- reiniciar el Kernel;
- modificar seguridad;
- alterar configuración;
- persistir datos;
- borrar recursos externos.

Rollback:

```text
volver al commit de 7.9-E
```

---

### 7.9-G — Cognitive End-to-End Validation

Objetivo:

Validar:

```text
CLI
→ Kernel
→ Planner
→ ConversationCapability
→ ConversationService
→ Conversation Context
→ Provider
→ Runtime
→ Response
```

Comprobar especialmente:

- continuidad entre turnos;
- orden de mensajes;
- límite de ventana;
- reset;
- fallo sin mutación parcial;
- compatibilidad de Sprint 7.8;
- Kernel sin cambios;
- Planner sin cambios;
- Capability contract sin cambios;
- Security sin cambios.

Rollback:

```text
volver al commit de 7.9-F
```

---

### 7.9-H — Real Runtime Validation & Final Review

Objetivo:

Validar manualmente el comportamiento real con el runtime local aprobado para
la prueba.

Escenario mínimo:

```text
turno 1:
establecer un dato temporal de conversación

turno 2:
comprobar que el modelo recibe continuidad

new

turno 3:
comprobar que el contexto anterior ya no se entrega
```

La evaluación validará transporte de contexto, no una respuesta textual exacta
del modelo.

Después:

- full pytest;
- compileall;
- git diff --check;
- revisión arquitectónica;
- documentación de cierre;
- PR;
- revisión;
- merge a main;
- reconciliación posterior mediante Vault Sync Agent.

---

## Fuera de alcance

Sprint 7.9 no implementará:

- Memory persistente;
- memoria episódica;
- memoria semántica;
- almacenamiento en disco;
- SQLite;
- JSONL persistente;
- vector databases;
- embeddings;
- Knowledge;
- RAG;
- GraphRAG;
- AKS runtime integration;
- recuperación de conversaciones;
- múltiples conversaciones persistentes;
- historial entre reinicios;
- summarization automática;
- compresión de contexto;
- token budgeting avanzado;
- Resource Governance completa;
- Model Router avanzado;
- tools;
- agentes;
- navegación;
- Internet;
- Browser Worker;
- Sandbox;
- Evidence Acquisition;
- automatización del sistema operativo;
- ejecución autónoma;
- nonce;
- replay protection;
- PKI;
- MFA;
- Secure Message Bus;
- Secure Context Manager criptográfico completo;
- nuevos privilegios;
- nuevas operaciones protegidas;
- cambios generales del contrato Capability.

---

## Seguridad

Sprint 7.9 no amplía autoridad operativa.

El historial conversacional:

```text
es información
≠ autoridad
```

Una entrada anterior del usuario o una respuesta anterior del modelo no deberá:

- conceder permisos;
- modificar políticas;
- elevar privilegios;
- sustituir confirmación humana;
- actuar como decisión de autorización;
- modificar SecurityContext.

Se preserva:

```text
La cognición puede proponer.
La autoridad decide.
```

El riesgo residual:

```text
7.7-D-001 — Strong SecurityContext Provenance
```

permanece aceptado y fuera de alcance.

La continuidad efímera local no deberá aumentar materialmente la exposición
asociada a ese riesgo.

---

## Privacidad y persistencia

Sprint 7.9 adoptará:

```text
ephemeral by default
```

El historial:

- vive únicamente en memoria;
- desaparece al finalizar el proceso;
- puede limpiarse explícitamente;
- no deberá escribirse automáticamente en logs;
- no deberá enviarse al Vault;
- no deberá persistirse como evidencia;
- no deberá convertirse en dataset.

Cualquier futura retención requerirá una decisión separada.

---

## Observabilidad

Los límites actuales entre:

```text
metrics
operational events
security audit
```

deberán preservarse.

Sprint 7.9 no introducirá un envelope universal.

El contenido del historial no deberá incorporarse incidentalmente a métricas,
eventos o auditoría.

Si surge una necesidad de observabilidad del contexto, deberá evaluarse
explícitamente antes de implementarse.

---

## Cuatro preguntas obligatorias

### 1. ¿Respeta el Blueprint?

Sí, condicionado a mantener la continuidad fuera del Kernel y preservar las
fronteras existentes.

### 2. ¿Respeta la Constitución Cognitiva?

Sí. El cambio es pequeño, proporcional, reversible y mejora la continuidad
cognitiva sin introducir autoridad ni autonomía.

### 3. ¿Respeta la Constitución de Gobernanza?

Sí. La evidencia y el historial siguen siendo información. Ningún dato
conversacional adquiere autoridad.

### 4. ¿Preserva la simplicidad estructural del Kernel?

Sí, condicionado a no modificar el Kernel para almacenar, transportar o
gestionar historial conversacional.

Un incumplimiento de cualquiera de estas condiciones provoca:

```text
STOP GATE
```

---

## Estrategia de gates

Cada paquete aceptado deberá terminar en un commit independiente.

Secuencia:

```text
baseline 28644354
  ↓
7.9-A
  ↓
7.9-B
  ↓
7.9-C
  ↓
7.9-D
  ↓
7.9-E
  ↓
7.9-F
  ↓
7.9-G
  ↓
7.9-H
```

Antes del merge a `main`, un rollback podrá utilizar el commit estable del gate
anterior.

Después del merge a `main`, cualquier rollback deberá realizarse mediante
`git revert` y no reescribiendo el historial de la rama permanente.

---

## Validación mínima por gate

Cada gate funcional deberá ejecutar como mínimo:

```powershell
python -m pytest -q
python -m compileall src tests
git diff --check
```

Además deberá ejecutar los tests focalizados correspondientes antes de la suite
completa.

Un gate no se acepta únicamente porque el código compile.

Debe existir evidencia de:

```text
tests
arquitectura
compatibilidad
scope
rollback
```

---

## Reconciliación con Project Vault

No se realizará sincronización manual del Vault durante los gates internos.

Secuencia esperada:

```text
Sprint branch
→ gates
→ final review
→ PR
→ merge a main
→ Vault Sync Agent
→ proposal
→ human review
→ Vault merge
```

El Project Vault continúa siendo una proyección derivada.

No sustituye la autoridad del repositorio oficial.

---

## Evidencia de implementación y validación

### Candidato final evaluado

```text
commit: d58b8ec98d48f5e2eac115d1d54b193e1df617fd
branch: sprint/7.9-conversation-continuity
```

El candidato final fue validado con working tree limpio.

### Gates implementados

```text
7.9-A — Sprint Activation & Architecture Freeze              PASS
7.9-B — Conversation Contract Extension                     PASS
7.9-C — Bounded In-Memory Conversation Context              PASS
7.9-D — ConversationService Integration                     PASS
7.9-E — Structured Runtime Conversation Adapter             PASS
7.9-F — CLI Conversation Continuity                         PASS
7.9-G — Cognitive End-to-End Validation                     PASS
7.9-H — Real Runtime Validation & Final Review              PASS
```

### Findings de revisión

Durante la validación se identificaron dos findings acotados.

#### G-R01 — Supported history roles

Finding:

```text
ConversationMessage permitía roles fuera del conjunto
inicial autorizado para historial:
user | assistant
```

Corrección:

```text
ConversationMessage rechaza roles no soportados.
```

Resultado:

```text
Correction Budget: PASS
Fix rounds: 1/1
Validation: PASS
```

Commit:

```text
3ed0d09af5e4a64ba87742116c6c2ff4b033cf6
```

#### H-R01 — CLI help consistency

Finding:

```text
el comando `new` estaba implementado y probado,
pero no aparecía en HELP_MESSAGE.
```

Corrección:

```text
HELP_MESSAGE documenta el comando `new`
sin modificar su comportamiento.
```

Resultado:

```text
Correction Budget: PASS
Fix rounds: 1/1
Validation: PASS
```

Commit:

```text
d58b8ec98d48f5e2eac115d1d54b193e1df617fd
```

### Validación automatizada final

Sobre el candidato final:

```text
python -m pytest -q
365 passed

python -m compileall src tests
PASS

git diff --check baseline..candidate
PASS

working tree
clean
```

### Invariantes arquitectónicos

Comparados contra el baseline inicial del Sprint 7.9:

```text
Kernel: unchanged
Planner: unchanged
Capability contract: unchanged
ConversationCapability: unchanged
Security: unchanged
```

No se introdujo:

```text
Memory persistente
persistencia en disco
Knowledge
RAG
GraphRAG
agentes
tools
Sandbox
navegación
Internet
nueva autoridad
estado conversacional en Kernel
historial en SecurityContext
```

### Validación con runtime real

Runtime utilizado:

```text
OllamaRuntime
model: qwen3.5:9b
base URL: http://localhost:11434
```

Se ejecutó el escenario manual definido para Sprint 7.9-H.

Resultado:

```text
continuidad entre turnos: PASS
uso del contexto en un turno posterior: PASS
comando `new`: PASS
eliminación del contexto anterior tras `new`: PASS
```

La evaluación validó transporte y eliminación del contexto,
no una formulación textual exacta del modelo.

No se persistió el contenido conversacional utilizado durante la prueba.

```text
Real Runtime Validation: PASS
```

### Revisión final 4R

```text
Risk:         PASS
Readability:  PASS
Reliability:  PASS
Resilience:   PASS

Overall:      PASS
```

No quedaron findings técnicos abiertos derivados de la revisión final.

### Estado previo al cierre

```text
implementación: completa
validación automatizada: completa
validación runtime real: completa
revisión arquitectónica: completa
revisión 4R: PASS
documentación de cierre: en preparación
aprobación final del propietario: pendiente
```

El candidato está técnicamente preparado para cierre, PR y revisión.

Este estado no constituye por sí mismo autorización para iniciar Sprint 7.10
ni ninguna otra unidad posterior.

---

## Criterio de cierre

Sprint 7.9 solo podrá declararse completado cuando:

- todos los paquetes aprobados estén cerrados;
- todos los tests estén verdes;
- `compileall` sea PASS;
- `git diff --check` sea PASS;
- la prueba manual con runtime real sea satisfactoria;
- Kernel permanezca simple;
- Capability contract no haya sido generalizado incidentalmente;
- SecurityContext permanezca separado del historial conversacional;
- no exista persistencia introducida;
- documentación y evidencia sean consistentes;
- exista una ruta de rollback clara;
- el propietario apruebe el cierre.

El cierre de Sprint 7.9 no autoriza automáticamente Sprint 7.10 ni ninguna otra
unidad posterior.
