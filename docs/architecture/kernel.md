---
id: DOC-ARQ-KERNEL
title: Kernel

status: active

version: 0.6.0-alpha

date: 2026-07-05

author: Hector Rodriguez

reviewed_by: []

tags:
  - architecture
  - kernel
  - runtime
  - governance
  - cognition

related:
  blueprint: DOC-ARQ-BLUEPRINT
  knowledge_model: DOC-ARQ-KNOWLEDGE-MODEL
  adr:
    - ADR-001

graph:
  type: kernel_document

  domain: kernel

  depends_on:
    - Blueprint
    - Cognitive Constitution
    - Governance Constitution

  affects:
    - Runtime
    - Capabilities
    - Memory
    - Knowledge
    - Planner
    - Orchestrator

history:
  created: 2026-06-27
  updated: 2026-07-05
---

# Malāk Kernel

> [!NOTE]
> **Migración de identidad del proyecto**
>
> Este documento fue creado originalmente cuando el proyecto se llamaba **Jarvis**.
>
> A partir de la versión **v0.6.0-alpha**, el nombre oficial del proyecto es **Malāk**.
>
> Este cambio afecta únicamente la identidad del proyecto. La arquitectura, los principios y las decisiones técnicas permanecen sin modificaciones.

## Estado

Documento: kernel.md
Sprint: Sprint 6.5 — Conversation Runtime
ID de arquitectura: ARQ-003
Estado: Implementado y validado
Versión objetivo: Malāk v0.6.0-alpha
Última revisión arquitectónica: 2026-07-05

---

## Objetivo

El Malāk Kernel es el núcleo de orquestación del sistema.

Su función principal es coordinar los módulos de Malāk sin depender directamente de un modelo LLM, proveedor externo, interfaz o herramienta específica.

Malāk no debe estar centrado en Ollama, OpenAI, Claude, Gemini ni ningún modelo particular.

El centro del sistema debe ser el Kernel.

---

## Principio central

El LLM es un servicio intercambiable.

El Kernel es quien decide:

* qué módulo participa;
* qué modelo se utiliza;
* si debe consultarse memoria;
* si debe consultarse RAG;
* si se requiere validación de seguridad;
* si debe registrarse un evento;
* si debe medirse una acción;
* si debe solicitarse confirmación humana.

---

## Capas del Kernel

El Kernel se divide en tres capas principales:

```text
Malāk Kernel
│
├── Control Layer
├── Intelligence Layer
└── Infrastructure Layer
```

---

## 1. Control Layer

La Control Layer define el flujo de trabajo del sistema.

### Componentes

* Decision Engine
* Event Bus
* Scheduler

### Responsabilidad

Decidir qué ocurre, cuándo ocurre y en qué orden.

### No debe hacer

* Ejecutar modelos directamente.
* Guardar memoria directamente.
* Ejecutar herramientas directamente.
* Escribir logs manualmente fuera del sistema de logging.

---

## 2. Intelligence Layer

La Intelligence Layer contiene los módulos relacionados con razonamiento, memoria, modelos y agentes.

### Componentes

* Model Router
* Memory Manager
* Agent Manager
* RAG Manager

### Responsabilidad

Resolver qué capacidades inteligentes necesita Malāk para responder o ejecutar una tarea.

### No debe hacer

* Tomar decisiones de seguridad final.
* Ejecutar comandos del sistema operativo directamente.
* Modificar configuración global.
* Saltarse el Event Bus.

---

## 3. Infrastructure Layer

La Infrastructure Layer sostiene los servicios transversales del sistema.

### Componentes

* Config Manager
* Security Manager
* Logging Manager
* Metrics Manager
* Tool Manager

### Responsabilidad

Proveer configuración, seguridad, observabilidad, métricas y acceso controlado a herramientas.

### No debe hacer

* Decidir la estrategia cognitiva de una respuesta.
* Elegir agentes por sí misma.
* Modificar memoria salvo que el Kernel lo indique.

---

## Componentes del Kernel

### Config Manager

Responsabilidad:

* Leer configuración.
* Validar configuración.
* Exponer configuración al resto del sistema.

No hace:

* Ejecutar modelos.
* Guardar memoria.
* Cargar documentos.
* Ejecutar herramientas.

---

### Event Bus

Responsabilidad:

* Publicar eventos.
* Distribuir eventos.
* Permitir comunicación desacoplada entre módulos.

Ejemplos de eventos:

```text
user.message.received
decision.started
decision.completed
rag.search.started
rag.search.completed
memory.lookup.started
memory.lookup.completed
model.selected
model.response.generated
tool.execution.requested
tool.execution.completed
security.confirmation.required
security.blocked
metrics.recorded
```

No hace:

* Decidir respuestas.
* Ejecutar herramientas.
* Validar seguridad.
* Guardar memoria por sí mismo.

---

### Decision Engine

Responsabilidad:

* Analizar la intención de la consulta.
* Definir el flujo de procesamiento.
* Decidir si se requiere RAG.
* Decidir si se requiere memoria.
* Decidir si se requiere una herramienta.
* Solicitar selección de modelo al Model Router.
* Solicitar validación al Security Manager cuando corresponda.

No hace:

* Responder directamente al usuario.
* Ejecutar comandos.
* Elegir modelos hardcodeados.
* Saltarse validaciones de seguridad.

---

### Model Router

Responsabilidad:

* Seleccionar el modelo adecuado según la tarea.
* Aplicar reglas de fallback.
* Considerar recursos disponibles.
* Separar modelos por rol: razonamiento, código, resumen, embeddings, visión.

No hace:

* Interpretar intención del usuario.
* Guardar memoria.
* Ejecutar herramientas.
* Decidir políticas de seguridad.

---

### Memory Manager

Responsabilidad:

* Gestionar memoria de sesión.
* Gestionar memoria de largo plazo.
* Integrar ChromaDB.
* Administrar embeddings.
* Consolidar resúmenes útiles.

No hace:

* Decidir qué modelo usar.
* Ejecutar herramientas.
* Responder directamente.
* Guardar información sensible sin política definida.

---

### RAG Manager

Responsabilidad:

* Buscar conocimiento en documentos locales.
* Recuperar fragmentos relevantes.
* Preparar contexto para el modelo.
* Registrar fuentes utilizadas.

No hace:

* Decidir por sí mismo cuándo debe ejecutarse.
* Modificar documentos originales.
* Reemplazar memoria de largo plazo.
* Ejecutar acciones externas.

---

### Agent Manager

Responsabilidad:

* Registrar agentes disponibles.
* Seleccionar agentes especializados cuando el Decision Engine lo indique.
* Coordinar agentes.
* Controlar resultados parciales.

No hace:

* Ejecutar agentes sin autorización del Kernel.
* Saltarse seguridad.
* Usar herramientas directamente sin pasar por Tool Manager.

---

### Scheduler

Responsabilidad:

* Programar tareas internas.
* Ejecutar rutinas periódicas.
* Coordinar backups, limpieza, indexación y chequeos de salud.

No hace:

* Crear tareas críticas sin confirmación.
* Ejecutar acciones externas sin pasar por Security Manager.

---

### Logging Manager

Responsabilidad:

* Registrar eventos importantes.
* Separar logs por categoría.
* Mantener trazabilidad del sistema.

Categorías sugeridas:

```text
logs/chat/
logs/kernel/
logs/agents/
logs/rag/
logs/memory/
logs/security/
logs/errors/
logs/performance/
```

No hace:

* Tomar decisiones.
* Modificar configuración.
* Ejecutar herramientas.

---

### Metrics Manager

Responsabilidad:

* Medir tiempos.
* Medir uso de recursos.
* Medir llamadas a modelos.
* Medir recuperación RAG.
* Medir errores.
* Medir rendimiento de agentes.

Métricas iniciales:

```text
request_id
timestamp
intent
selected_model
response_time_ms
rag_used
memory_used
tool_used
security_level
error_count
```

No hace:

* Registrar contenido sensible completo.
* Tomar decisiones.
* Ejecutar acciones.

---

### Security Manager

Responsabilidad:

* Clasificar riesgo de acciones.
* Bloquear acciones peligrosas.
* Solicitar confirmación humana.
* Definir políticas de ejecución.
* Validar comandos antes de ejecución.

Niveles de riesgo propuestos:

```text
LOW
MEDIUM
HIGH
BLOCKED
```

Acciones que requieren confirmación:

* Borrar archivos.
* Modificar archivos fuera del proyecto.
* Ejecutar comandos del sistema.
* Enviar mensajes externos.
* Usar APIs con costo.
* Modificar configuraciones críticas.
* Acceder a datos sensibles.

No hace:

* Ejecutar herramientas.
* Responder preguntas.
* Elegir modelos.
* Guardar memoria.

---

### Tool Manager

Responsabilidad:

* Registrar herramientas disponibles.
* Ejecutar herramientas permitidas.
* Pasar siempre por validación de seguridad.
* Registrar resultados.

Ejemplos futuros:

* PowerShell.
* Docker.
* Git.
* Navegador.
* APIs.
* Telegram.
* Automatizaciones.

No hace:

* Decidir cuándo se usa una herramienta.
* Saltarse seguridad.
* Ejecutar acciones destructivas sin confirmación.

---

## Thinking Pipeline

El flujo general de procesamiento será:

```text
Usuario
  ↓
Interface Layer
  ↓
Kernel
  ↓
Intent Analyzer
  ↓
Context Builder
  ↓
Memory Lookup
  ↓
RAG Retrieval
  ↓
Model Selection
  ↓
Reasoning
  ↓
Validation
  ↓
Response Builder
  ↓
Usuario
```

---

## Regla de comunicación

Los módulos no deben llamarse libremente entre sí.

La comunicación debe pasar por:

* Kernel
* Event Bus
* contratos definidos en core/contracts

Esto reduce acoplamiento y permite reemplazar módulos sin romper el sistema.

---

## Decisión inicial para v0.5.0-alpha

El Decision Engine comenzará basado en reglas simples.

No se implementará todavía un Mini LLM Router.

Motivo:

* menor consumo de recursos;
* más fácil depuración;
* comportamiento determinista;
* mejor para validar arquitectura inicial.

La opción de usar un modelo pequeño como router queda reservada para una versión futura.

---

## Estado objetivo al final del Sprint 1

Al finalizar Sprint 1, Malāk deberá tener:

* Kernel documentado.
* Estructura core creada.
* Contratos iniciales definidos.
* Configuración centralizada.
* Logging base diseñado.
* Métricas base diseñadas.
* Security Manager diseñado.
* Decision Engine especificado, aunque no completamente implementado.

---

---

## Estado actual (v0.6.0-alpha)

La arquitectura definida en este documento continúa siendo la referencia oficial para el Kernel de Malāk.

Durante los Sprints 5 y 6 se implementó la primera versión funcional del núcleo respetando las responsabilidades aquí establecidas, sin introducir cambios en sus principios arquitectónicos.

Actualmente se encuentran implementados y validados:

- Bootstrap del Kernel.
- Planner MVP.
- Capability Registry.
- Capability Contract.
- Conversation Contract.
- Conversation Service.
- Conversation Provider Registry.
- LLM Runtime (abstracción).
- Mock LLM Runtime.

Todos estos componentes permanecen desacoplados mediante contratos e interfaces, preservando los principios de:

- Kernel First.
- Capability First.
- Runtime Independence.
- Human in Control.
- Model Agnostic.

La integración con proveedores externos de inferencia (por ejemplo, Ollama) deberá realizarse exclusivamente mediante implementaciones de `LLMRuntime`, sin modificar las responsabilidades del Kernel definidas en este documento.

## Decisiones relacionadas

* ARQ-001: Crear carpeta core.
* ARQ-002: Crear capa contracts.
* ARQ-003: Diseñar Malāk Kernel.


---

# ARQ-006

## KERNEL MÍNIMO GOBERNANTE

El Malāk Kernel deberá ser pequeño en implementación, pero fuerte en autoridad operativa.

El Kernel no deberá contener la lógica interna de memoria, modelos, herramientas, agentes, RAG, voz o identidad.

Su responsabilidad será coordinar, gobernar y controlar la ejecución del sistema mediante componentes centrales.

## Componentes internos del Kernel

El Kernel estará compuesto por:

- Decision Engine
- Policy Engine
- Execution Controller
- Malāk Service Bus
- Service Registry

## Responsabilidades del Kernel

El Kernel deberá:

- recibir solicitudes desde las interfaces;
- iniciar el proceso cognitivo;
- consultar políticas activas;
- coordinar servicios registrados;
- controlar la ejecución;
- permitir pausa, cancelación y reanudación;
- aplicar reglas de gobernanza;
- bloquear acciones no permitidas;
- registrar decisiones relevantes;
- entregar respuestas a la capa de identidad o interfaz correspondiente.

## Responsabilidades que NO pertenecen al Kernel

El Kernel no deberá:

- almacenar memoria directamente;
- ejecutar modelos directamente;
- procesar documentos directamente;
- ejecutar herramientas directamente;
- generar voz directamente;
- contener personalidad;
- decidir políticas por fuera de la gobernanza.

## Principio de autoridad

Todo servicio de Malāk deberá obedecer las decisiones del Kernel y las políticas de gobernanza activas.

Ninguna capacidad cognitiva, modelo, agente, herramienta o proceso podrá ejecutar una acción que contradiga las políticas de gobernanza activas.