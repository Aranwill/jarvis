---

title: Sprint 7.8 — Cognitive Conversation Execution Path Foundation
status: activo
authority: documentación operativa derivada
as_of_date: 2026-08-16
as_of_commit: 6c179730e6d4220bbba22a8282f978a7a1aa9155
branch: main
language: es
------------

# Sprint 7.8 — Cognitive Conversation Execution Path Foundation

## Estado

```text
COMPLETADO
```

El Sprint 7.8 fue aprobado explícitamente por el propietario el 2026-08-16.

Su activación autoriza únicamente el trabajo definido dentro de este sprint.

No autoriza automáticamente:

* cambios posteriores fuera de alcance;
* nuevos sprints;
* promoción de release;
* creación o movimiento de tags;
* ampliación de autoridad;
* incorporación de capacidades no definidas en este documento.

Cada paquete deberá implementarse, probarse, revisarse y aceptarse antes de avanzar al siguiente cuando exista una decisión arquitectónica pendiente.

---

## Baseline inicial

El sprint comienza desde:

```text
6c179730e6d4220bbba22a8282f978a7a1aa9155
```

Rama permanente de origen:

```text
main
```

Rama temporal de trabajo:

```text
sprint/7.8-cognitive-conversation-execution-path
```

Estado técnico inicial reproducido localmente antes de crear la rama temporal:

```text
339 passed
compileall: PASS
git diff --check: PASS
working tree: clean
HEAD == origin/main
Python 3.12.10
```

El commit anterior constituye el baseline inicial del Sprint 7.8.

Cualquier cambio de este sprint deberá ser trazable respecto de ese punto y mantener una ruta clara de rollback.

---

## Objetivo

Establecer la primera ruta cognitiva conversacional end-to-end de Malāk.

El sprint conectará el flujo:

```text
Kernel
→ Planner
→ Capability
```

con el subsistema conversacional existente:

```text
ConversationService
→ ConversationProvider
→ LLMRuntime
```

sin acoplar el Kernel a:

* servicios concretos;
* providers;
* runtimes;
* modelos;
* implementaciones específicas de infraestructura.

El resultado esperado es que una solicitud pueda entrar por la frontera oficial de Malāk y recorrer una capability conversacional hasta obtener una respuesta mediante un runtime intercambiable.

Este sprint convierte componentes ya existentes en una primera ruta cognitiva integrada, preservando las fronteras arquitectónicas establecidas.

---

## Estado arquitectónico inicial

Antes de Sprint 7.8 existen dos rutas funcionales separadas.

### Pipeline cognitivo mínimo

```text
Request
  ↓
Kernel.receive()
  ↓
Planner.resolve()
  ↓
CapabilityRegistry.get()
  ↓
Capability.execute()
  ↓
Response
```

El Planner actual resuelve únicamente la capability:

```text
echo
```

El Capability Registry contiene actualmente:

```text
EchoCapability
```

El Kernel no conoce:

* ConversationService;
* ConversationProvider;
* LLMRuntime;
* OllamaRuntime;
* MockLLMRuntime.

Esta independencia deberá preservarse.

### Pipeline conversacional actual

```text
ConversationRequest
  ↓
ConversationService.generate()
  ↓
ConversationProviderRegistry
  ↓
RuntimeConversationProvider
  ↓
LLMRuntime
  ↓
ConversationResponse
```

Actualmente la CLI utiliza esta ruta directamente.

La CLI no utiliza `Kernel.receive()` para sus solicitudes conversacionales.

Por tanto, el pipeline cognitivo y el pipeline conversacional existen, pero todavía no forman una única ruta de ejecución.

---

## Arquitectura objetivo

La arquitectura objetivo mínima del sprint es:

```text
Request
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
  ↓
ConversationProviderRegistry
  ↓
RuntimeConversationProvider
  ↓
LLMRuntime
  ↓
ConversationResponse
  ↓
Response
```

La frontera:

```text
Kernel → Capability
```

debe permanecer como límite entre el núcleo cognitivo y las implementaciones concretas de capacidades.

Conversation deberá incorporarse detrás de la abstracción `Capability`.

---

## Decisión arquitectónica inicial

Sprint 7.8 adopta como dirección inicial:

```text
ConversationCapability
```

como adapter entre:

```text
Capability.execute(...)
```

y:

```text
ConversationService.generate(...)
```

La capability deberá adaptar la entrada proveniente del pipeline cognitivo al contrato estructurado:

```text
ConversationRequest
```

y convertir:

```text
ConversationResponse
```

en el resultado esperado por la frontera actual de Capability.

No se modificará inicialmente el contrato general:

```text
Capability.execute(request)
```

para introducir una abstracción universal de ejecución.

Una evolución futura hacia contratos como:

```text
CapabilityExecutionRequest
CapabilityExecutionResult
```

solo deberá considerarse cuando exista evidencia suficiente de múltiples capabilities reales que compartan necesidades estructuradas comunes.

No se generalizará prematuramente el contrato actual.

---

## Principios de diseño

### Kernel First

El Kernel debe permanecer pequeño, estable y orientado a coordinación.

No deberá incorporar lógica conversacional.

### Capability First

Conversation deberá integrarse como capability.

El Kernel no deberá introducir condiciones especiales como:

```text
if capability == conversation
```

ni rutas equivalentes que conozcan servicios concretos.

### Runtime Independence

`LLMRuntime` seguirá siendo la única frontera entre el dominio conversacional y motores concretos de inferencia.

Ollama no deberá aparecer como dependencia del Kernel ni de los contratos cognitivos.

### Composition at the Boundary

La construcción de:

* runtimes;
* providers;
* registries;
* services;
* capabilities;
* Kernel;

deberá ocurrir desde una frontera externa apropiada de composición.

La composición concreta no deberá desplazarse dentro del Kernel.

### Incremental Integration

Cada nueva conexión deberá introducirse mediante cambios pequeños, probados y reversibles.

No se realizará una migración completa de la CLI, Planner, Kernel y Conversation en un único cambio.

---

## Restricción arquitectónica principal

No se aceptará una solución que introduzca dependencias directas desde el Kernel hacia:

```text
ConversationService
ConversationProvider
ConversationProviderRegistry
LLMRuntime
OllamaRuntime
MockLLMRuntime
```

Tampoco se aceptará una solución donde:

```text
kernel.bootstrap
```

se convierta en responsable de seleccionar runtimes, modelos o configuración operativa externa.

La composición de esas dependencias deberá permanecer fuera del núcleo cognitivo.

---

## Compatibilidad obligatoria

El comportamiento histórico deberá preservarse durante los primeros incrementos mientras no exista una decisión explícita que lo modifique.

En particular:

```text
Kernel()
```

deberá continuar siendo una construcción válida.

La ruta existente:

```text
Kernel()
→ Planner()
→ EchoCapability
```

no deberá romperse al introducir capacidad de composición externa.

El objetivo inicial es permitir una evolución aditiva, por ejemplo mediante una frontera de inyección controlada de dependencias, sin eliminar inmediatamente los defaults actuales.

---

## Paquetes previstos

### 7.8-A — Sprint Activation & Architecture Freeze

Objetivo:

* formalizar la aprobación del sprint;
* fijar baseline;
* documentar alcance;
* congelar invariantes;
* registrar arquitectura objetivo;
* evitar cambios funcionales antes de contar con una dirección explícita.

Resultado esperado:

```text
documentación del sprint activa
baseline trazable
arquitectura inicial registrada
código sin cambios
```

---

### 7.8-B — Kernel Composition Seam

Objetivo:

Introducir una frontera mínima de composición que permita construir el Kernel con dependencias proporcionadas externamente.

Dirección prevista:

```text
Kernel(
    planner=...,
    registry=...,
)
```

preservando:

```text
Kernel()
```

como comportamiento compatible.

Este paquete no incorporará Conversation.

Este paquete no modificará el Planner para enrutar conversación.

Este paquete no modificará la CLI.

El objetivo es únicamente desacoplar la construcción interna rígida del Kernel sin alterar su lógica de ejecución.

EVIDENCE:
- kernel tests: 4 passed
- full suite: 340 passed
- compileall: PASS
- git diff --check: PASS
- Kernel() backwards compatibility preserved
- injected Planner and CapabilityRegistry validated
- no Conversation, provider, runtime or CLI dependency introduced into Kernel

---

### 7.8-C — Conversation Capability Adapter

Objetivo:

Crear una capability conversacional que implemente el contrato existente:

```text
Capability
```

y adapte:

```text
request content
```

hacia:

```text
ConversationRequest
```

delegando la ejecución a:

```text
ConversationService
```

y devolviendo el contenido de:

```text
ConversationResponse
```

La capability no seleccionará runtimes concretos.

La capability no construirá providers.

La capability no conocerá Ollama.

---

### 7.8-D — Conversation Routing

Objetivo:

Evolucionar el Planner de forma mínima y determinista para permitir el routing hacia:

```text
conversation
```

cuando corresponda.

Este paquete deberá evitar:

* selección de modelos;
* selección de runtime;
* navegación;
* herramientas;
* memoria;
* decisiones de seguridad;
* lógica de infraestructura.

El Planner deberá continuar resolviendo capacidades, no ejecutándolas.

---

### 7.8-E — Kernel-driven Application Composition

Objetivo:

Crear una composición externa de aplicación que conecte:

```text
Runtime
→ RuntimeConversationProvider
→ ConversationProviderRegistry
→ ConversationService
→ ConversationCapability
→ CapabilityRegistry
→ Planner
→ Kernel
```

sin introducir esas dependencias dentro del Kernel.

Esta composición deberá permitir tanto:

```text
MockLLMRuntime
```

como:

```text
OllamaRuntime
```

sin cambiar el Kernel.

---

### 7.8-F — CLI Migration

Objetivo:

Migrar la ruta conversacional de la CLI para utilizar:

```text
Kernel.receive()
```

como frontera cognitiva.

Actualmente la CLI invoca directamente:

```text
ConversationService.generate()
```

Después de este paquete, una solicitud conversacional ordinaria deberá atravesar el pipeline cognitivo.

Los comandos propios de la CLI como:

```text
help
status
exit
```

podrán permanecer en la frontera de aplicación y no deberán convertirse artificialmente en capabilities salvo necesidad posterior demostrada.

---

### 7.8-G — End-to-End Validation

Objetivo:

Validar la ruta completa con un runtime determinista.

La validación deberá cubrir al menos:

```text
Request
→ Kernel
→ Planner
→ ConversationCapability
→ ConversationService
→ Provider
→ MockLLMRuntime
→ Response
```

También deberá comprobar:

* errores controlados;
* source correcto de respuesta;
* comportamiento ante capability inexistente;
* compatibilidad del Kernel histórico;
* ausencia de dependencias concretas dentro del Kernel;
* preservación de tests existentes.

---

### 7.8-H — Real Runtime Validation & Final Review

Objetivo:

Validar la composición final mediante:

```text
OllamaRuntime
```

y realizar la revisión integral del sprint.

La validación manual deberá comprobar al menos:

```text
CLI
→ Kernel
→ Planner
→ ConversationCapability
→ ConversationService
→ RuntimeConversationProvider
→ OllamaRuntime
→ modelo local
```

La validación real no deberá modificar la arquitectura para acomodar Ollama.

La misma ruta deberá funcionar mediante la abstracción `LLMRuntime`.

---

## Fuera de alcance

Sprint 7.8 no implementará:

* Memory persistente;
* memoria episódica;
* Knowledge;
* RAG;
* GraphRAG;
* AKS runtime integration;
* tools;
* agentes;
* navegación;
* Internet;
* Evidence Acquisition Foundation;
* Browser Worker;
* Sandbox;
* automatización del sistema operativo;
* ejecución autónoma;
* Model Router avanzado;
* selección dinámica compleja de modelos;
* Resource Governance avanzada;
* optimización de RAM;
* optimización de VRAM;
* lazy loading;
* descarga automática de modelos;
* nonce;
* replay protection;
* PKI;
* identidad criptográfica;
* Secure Message Bus;
* MFA;
* Secure Context Manager criptográfico completo;
* nuevos privilegios;
* nuevas operaciones protegidas;
* evolución general del contrato `Capability` sin necesidad demostrada.

---

## Seguridad

Sprint 7.8 no amplía autoridad operativa.

La integración cognitiva no deberá:

* conceder permisos;
* modificar policies;
* crear rutas privilegiadas;
* saltarse el Security Control Plane;
* interpretar una respuesta LLM como autorización;
* convertir la conversación en una fuente de autoridad.

Se preserva el principio:

```text
La cognición puede proponer.
La autoridad decide.
```

El riesgo residual existente:

```text
7.7-D-001 — Provenance fuerte del SecurityContext
```

permanece aceptado y fuera de alcance de este sprint.

Sprint 7.8 no deberá aumentar materialmente la exposición asociada a ese riesgo.

---

## Observabilidad

Los mecanismos existentes de:

* métricas;
* eventos operativos;
* auditoría;

deberán conservar sus fronteras actuales.

No se creará un envelope universal de observabilidad.

La integración del pipeline cognitivo deberá permitir posteriormente mantener correlación end-to-end sin mezclar:

```text
metrics
operational events
security audit
```

en un único subsistema.

Cualquier cambio de observabilidad necesario durante el sprint deberá tratarse explícitamente y no incorporarse incidentalmente.

---

## Kernel Composition Rule

La composición de dependencias deberá respetar esta separación:

```text
Application Boundary
        ↓
Composition
        ↓
Kernel
```

y no:

```text
Kernel
        ↓
construct runtime
        ↓
construct providers
        ↓
read environment
```

El Kernel no deberá leer configuración externa de runtime.

El Kernel no deberá conocer variables como:

```text
MALAK_RUNTIME
MALAK_OLLAMA_MODEL
MALAK_OLLAMA_BASE_URL
```

Esas variables pertenecen a la frontera de aplicación.

---

## Dependency Direction

La dirección deseada es:

```text
Kernel
  ↓
Capability abstraction
  ↓
ConversationCapability
  ↓
ConversationService
  ↓
ConversationProvider abstraction
  ↓
LLMRuntime abstraction
  ↓
Concrete runtime
```

Las dependencias concretas no deberán fluir en sentido contrario.

En particular:

```text
OllamaRuntime
```

no deberá ser importado por:

* Kernel;
* Planner;
* Capability contract;
* Conversation contract.

---

## Reglas para el Planner

El Planner continuará siendo un componente de resolución.

Su responsabilidad será:

```text
Request → capability name
```

No deberá:

* ejecutar capabilities;
* construir capabilities;
* seleccionar providers;
* seleccionar runtimes;
* realizar llamadas LLM;
* administrar memoria;
* conceder autoridad;
* ejecutar políticas de seguridad.

Cualquier evolución futura del Planner hacia clasificación más sofisticada deberá realizarse en un sprint independiente o en una unidad explícitamente aprobada.

---

## Reglas para ConversationCapability

La capability conversacional deberá:

* implementar `Capability`;
* exponer un nombre estable;
* recibir la entrada desde el pipeline cognitivo;
* construir el contrato conversacional mínimo necesario;
* delegar a `ConversationService`;
* devolver el resultado al Kernel.

No deberá:

* construir el runtime;
* seleccionar Ollama;
* leer variables de entorno;
* administrar providers globales;
* modificar el Kernel;
* acceder directamente a Memory;
* acceder directamente a RAG;
* acceder directamente a Internet;
* conceder permisos.

---

## Reglas para ConversationService

`ConversationService` conservará su responsabilidad vigente.

Debe continuar siendo responsable únicamente de:

```text
resolver provider solicitado
delegar ConversationRequest
retornar ConversationResponse
```

No deberá absorber responsabilidades del Kernel ni del Planner.

No deberá convertirse en un orchestrator cognitivo general.

---

## Reglas para LLMRuntime

`LLMRuntime` continuará siendo la frontera exclusiva hacia motores de inferencia.

Las capabilities y el Kernel no deberán depender de métodos específicos de Ollama.

La integración deberá continuar permitiendo sustituir:

```text
MockLLMRuntime
OllamaRuntime
```

sin modificar los contratos cognitivos.

---

## Estrategia de pruebas

Cada paquete funcional deberá incluir tests antes de considerarse completo.

Se priorizarán:

* unit tests;
* tests deterministas;
* negative tests;
* integración controlada;
* tests de compatibilidad.

La validación con Ollama real se realizará únicamente después de que la ruta determinista esté estable.

No se utilizará un servicio externo real como requisito para ejecutar la suite estándar.

---

## Criterios generales de aceptación

Sprint 7.8 podrá considerarse candidato a cierre únicamente si:

* existe una ruta conversacional completa a través del Kernel;
* el Kernel continúa independiente de servicios concretos;
* el Kernel continúa independiente de providers;
* el Kernel continúa independiente de runtimes;
* Conversation se encuentra detrás de Capability;
* la composición ocurre fuera del Kernel;
* Planner continúa limitado a resolución;
* ConversationService conserva su responsabilidad;
* LLMRuntime conserva Runtime Independence;
* la CLI puede recorrer la ruta cognitiva;
* MockLLMRuntime permite validación determinista;
* OllamaRuntime puede utilizar la misma arquitectura;
* los tests históricos permanecen válidos o cualquier cambio contractual ha sido explícitamente aprobado;
* no se introducen capacidades fuera de alcance;
* no aparecen blockers arquitectónicos;
* no aparecen blockers de seguridad;
* la suite completa permanece en verde;
* `compileall` permanece correcto;
* `pip check` permanece correcto;
* `git diff --check` permanece correcto;
* existe evidencia clara de rollback;
* la revisión final es aprobada explícitamente por el propietario.

---

## Validaciones obligatorias por cambio

Antes de cualquier modificación importante se deberá comprobar:

1. ¿Respeta el Blueprint?
2. ¿Respeta la Constitución Cognitiva?
3. ¿Respeta la Gobernanza?
4. ¿Hace al Kernel más simple o al menos preserva su simplicidad estructural?

Si alguna respuesta es negativa o dudosa:

```text
STOP
```

La implementación deberá detenerse y rediseñarse antes de continuar.

---

## Riesgos iniciales

### R1 — Acoplamiento del Kernel

Riesgo:

Introducir lógica específica de Conversation dentro del Kernel.

Mitigación:

```text
Conversation detrás de Capability.
```

### R2 — Composition leakage

Riesgo:

Hacer que Kernel o bootstrap seleccionen runtimes, providers o configuración externa.

Mitigación:

```text
composition root externo.
```

### R3 — Generalización prematura

Riesgo:

Crear contratos universales de ejecución antes de contar con evidencia suficiente.

Mitigación:

```text
preservar Capability actual durante los primeros incrementos.
```

### R4 — Big-bang CLI migration

Riesgo:

Modificar simultáneamente Kernel, Planner, capability, composición y CLI.

Mitigación:

```text
paquetes secuenciales y validación entre incrementos.
```

### R5 — Regresión del baseline histórico

Riesgo:

Romper `Kernel()` o Echo antes de estabilizar la nueva ruta.

Mitigación:

```text
compatibilidad aditiva inicial y tests de regresión.
```

---

## Rollback

El punto de rollback inicial del sprint es:

```text
6c179730e6d4220bbba22a8282f978a7a1aa9155
```

La rama del sprint deberá conservar una secuencia de commits pequeños y reversibles.

Ningún incremento deberá requerir revertir múltiples cambios no relacionados para restaurar el baseline anterior.

Cada paquete deberá poder identificarse mediante commits trazables.

---

## Human in Control

La aprobación de Sprint 7.8 autoriza su ejecución dentro del alcance definido.

No autoriza automáticamente:

* cambiar documentos de ley;
* modificar Blueprint;
* ampliar autoridad;
* introducir nuevas capacidades sensibles;
* promover una release;
* cambiar la versión;
* crear tags;
* iniciar otro sprint.

Las decisiones arquitectónicas relevantes que aparezcan durante el sprint deberán ser presentadas al propietario antes de introducir cambios que alteren contratos o fronteras estables.

---

## Regla de ejecución

La secuencia inicial aprobada es:

```text
7.8-A
↓
7.8-B
↓
7.8-C
↓
7.8-D
↓
7.8-E
↓
7.8-F
↓
7.8-G
↓
7.8-H
```

Cada paquete deberá:

1. tener alcance explícito;
2. introducir una unidad coherente de cambio;
3. incorporar o actualizar tests;
4. ejecutar validaciones aplicables;
5. revisar impacto arquitectónico;
6. revisar impacto de seguridad;
7. revisar documentación;
8. producir un commit pequeño y reversible;
9. quedar aceptado antes del siguiente cambio significativo.

No se acumularán múltiples paquetes funcionales sin validación intermedia.

---

## Estado inicial de paquetes

```text
7.8-A — Sprint Activation & Architecture Freeze
STATUS: COMPLETED

7.8-B — Kernel Composition Seam
STATUS: COMPLETED

7.8-C — Conversation Capability Adapter
STATUS: COMPLETED
EVIDENCE:
- conversation capability tests: 2 passed
- full suite: 342 passed
- compileall: PASS
- git diff --check: PASS
- stable capability name: conversation
- ConversationRequest adaptation validated
- configured provider, model and system prompt propagation validated
- ConversationResponse content returned through Capability boundary
- no Kernel, Planner, runtime, provider construction or CLI changes introduced

7.8-D — Conversation Routing
STATUS: COMPLETED
EVIDENCE:
- planner tests: 2 passed
- full suite: 343 passed
- compileall: PASS
- git diff --check: PASS
- Planner() default routing to echo preserved
- explicit deterministic routing to conversation validated
- Request contract unchanged
- no prompt heuristics or LLM-based routing introduced
- no Kernel, runtime, provider or CLI changes introduced

7.8-E — Kernel-driven Application Composition
STATUS: COMPLETED
EVIDENCE:
- application composition tests: 2 passed
- full suite: 345 passed
- compileall: PASS
- git diff --check: PASS
- build_conversation_kernel() returns Kernel
- conversation path through Kernel validated with MockLLMRuntime
- composition root located under malak.app
- Kernel remains independent from runtime selection and environment
- no CLI migration introduced in this package

7.8-F — CLI Migration
STATUS: COMPLETED
EVIDENCE:
- kernel-routing CLI test: 1 passed
- full CLI suite: 24 passed
- full suite: 346 passed
- compileall: PASS
- git diff --check: PASS
- ordinary prompts routed through Kernel.receive()
- Kernel Request preserves CLI-generated request_id
- help, status, exit and empty-input handling remain at CLI boundary
- operational event behavior preserved
- injected ConversationService compatibility preserved
- no Kernel, Planner, ConversationCapability or runtime contract changes introduced

7.8-G — End-to-End Validation
STATUS: COMPLETED
EVIDENCE:
- end-to-end conversation path tests: 2 passed
- full suite: 348 passed
- compileall: PASS
- git diff --check: PASS
- Request -> Kernel -> Planner -> ConversationCapability -> ConversationService -> RuntimeConversationProvider -> MockLLMRuntime validated
- response source preserved as conversation
- empty-request Kernel guard preserved
- no production code changes required in this package

7.8-H — Real Runtime Validation & Final Review
STATUS: COMPLETED
EVIDENCE:
- real runtime: OllamaRuntime
- real model: qwen3.5:9b
- Ollama endpoint: http://localhost:11434
- CLI import validation: PASS
- real end-to-end inference: PASS
- expected probe: MALAK-7.8-OK
- observed response: MALAK-7.8-OK
- CLI remained operational after inference
- clean working tree preserved after runtime validation
- no production code changes required in this package
```


---

## Certificación final de Sprint 7.8

### Resultado

```text
COMPLETADO
```

## Cierre

El cierre de Sprint 7.8 requerirá:

* finalización de los paquetes aprobados;
* revisión integral;
* evidencia técnica;
* evidencia arquitectónica;
* revisión de seguridad;
* trazabilidad;
* rollback verificable;
* aprobación humana explícita.

Completar los tests no implica automáticamente cerrar el sprint.

Cerrar el sprint no implica automáticamente:

* iniciar otro;
* modificar versión;
* crear un tag;
* publicar una release;
* ampliar autoridad;
* habilitar agentes;
* habilitar tools;
* habilitar navegación.

Sprint 7.8 deberá terminar con una primera ruta cognitiva conversacional integrada, pero todavía gobernada, limitada y arquitectónicamente desacoplada.
