---
id: DOC-ARQ-BLUEPRINT
title: Blueprint
status: active
version: 0.6.1-alpha
date: 2026-07-05
author: Hector Rodriguez
reviewed_by: []

tags:
  - architecture
  - blueprint
  - kernel
  - governance
  - cognition

related:
  kernel: DOC-ARQ-KERNEL
  knowledge_model: DOC-ARQ-KNOWLEDGE-MODEL
  adr:
    - ADR-001
    - ADR-003

graph:
  type: architecture_document

  domain: architecture

  depends_on:
    - Cognitive Constitution
    - Governance Constitution

  affects:
    - Runtime
    - Kernel
    - Capabilities
    - Memory
    - Knowledge

history:
  created: 2026-06-27
  updated: 2026-08-19
---

# Malāk Blueprint

> [!NOTE]
> **Migración de identidad del proyecto**
>
> Este documento fue creado originalmente cuando el proyecto se llamaba **Jarvis**.
>
> A partir de la versión **v0.6.0-alpha**, el nombre oficial del proyecto es **Malāk**.
>
> Este cambio afecta únicamente la identidad del proyecto. La arquitectura, los principios y las decisiones técnicas permanecen sin modificaciones.

**Blueprint Versión:** 0.6.1-alpha
**Project Version:** v0.6.0-alpha
**Documento:** BP-001
**Estado:** Aprobado y validado
**Sprint:** Sprint 6.5 — Conversation Runtime
**Clasificación:** Documento Maestro de Arquitectura
**Última revisión arquitectónica:** 2026-08-19

---

# 1. Objetivo

El Blueprint constituye el documento maestro de arquitectura de Malāk.

Su propósito es definir la estructura completa de la plataforma, las responsabilidades de cada componente, las reglas arquitectónicas y la organización general del sistema.

Toda decisión técnica, implementación, módulo o capacidad deberá respetar este documento.

---

# 2. Alcance

El Blueprint gobierna:

* arquitectura
* componentes
* capas
* gobernanza
* contratos
* dependencias
* principios
* evolución de la plataforma

No reemplaza documentos específicos como:

* Kernel Specification
* Capability SDK
* Constitution Specification
* ADR
* Domain Model

Estos derivan del Blueprint.

---

# 3. Visión

Malāk es una plataforma cognitiva modular, gobernable y extensible.

No está centrada en un modelo de lenguaje.

El modelo LLM representa únicamente un proveedor intercambiable de capacidades cognitivas.

La plataforma debe poder evolucionar independientemente de cualquier tecnología específica.

---

# 4. Principios Arquitectónicos

## P-001

Kernel First

---

## P-002

Constitution First

---

## P-003

Governance First

---

## P-004

Capability First

---

## P-005

Human in Control

---

## P-006

Zero Trust

---

## P-007

Model Agnostic

---

## P-008

Security by Design

---

## P-009

Everything is Observable

---

## P-010

Everything is Auditable

---
## P-011

Runtime Independence

---

## P-012

Specification & Verification First

Toda modificación significativa de Malāk deberá definir su comportamiento esperado y criterios de aceptación verificables antes de ser aceptada en el baseline.

La implementación deberá respaldarse mediante pruebas y evidencia objetiva proporcionales al riesgo.

Las reglas metodológicas detalladas se definen en `docs/development/engineering_method.md`.

La especificación, las pruebas y la evidencia no conceden autoridad ni pueden modificar por sí mismas arquitectura, gobernanza o documentos de ley.

---

# 5. Arquitectura General

```text
                        Usuario
                           │
                           ▼
                 Interface Layer
                           │
                           ▼
                 Identity Layer
                           │
                           ▼
                  Context Layer
                           │
                           ▼
                Governance Layer
                           │
                           ▼
              Constitutional Engine
                           │
                           ▼
                      Kernel
                           │
       ┌───────────────┼─────────────────┐
       ▼               ▼                 ▼
Capability Manager  Planning Engine  Reasoning Engine
       │               │                 │
       └───────────────┴─────────────────┘
                       │
                       ▼
                Memory Layer
                       │
                       ▼
               Knowledge Layer
                       │
                       ▼
               Execution Layer
                       │
                       ▼
             Infrastructure Layer
```

---

# 6. Capas Arquitectónicas

La plataforma queda dividida en las siguientes capas:

* Interface Layer
* Identity Layer
* Context Layer
* Governance Layer
* Constitutional Engine
* Kernel
* Capability Manager
* Planning Engine
* Reasoning Engine
* Memory Layer
* Knowledge Layer
* Execution Layer
* Infrastructure Layer

Cada capa posee responsabilidades exclusivas.

No pueden existir responsabilidades compartidas.

---

# 7. Responsabilidades Generales

## Interface Layer

Gestiona la interacción con el usuario.

---

## Identity Layer

Gestiona identidad, perfiles y autenticación.

---

## Context Layer

Construye el contexto operativo antes de iniciar el procesamiento.

---

## Governance Layer

Administra políticas generales del sistema.

---

## Constitutional Engine

Valida que toda acción respete la Constitución Cognitiva y la Constitución de Gobernanza.

Puede aprobar o rechazar cualquier operación.

---

## Kernel

Coordina el funcionamiento interno.

No implementa lógica de negocio.

No almacena memoria.

No razona.

No ejecuta herramientas.

---

## Capability Manager

Administra todas las capacidades registradas.

---

## Planning Engine

Convierte objetivos en planes.

---

## Reasoning Engine

Realiza inferencias y evaluación lógica.

---

## Memory Layer

Administra toda la memoria del sistema.

---

## Knowledge Layer

Gestiona documentos, RAG, embeddings y conocimiento estructurado.

---

## Execution Layer

Ejecuta herramientas, agentes, automatizaciones y acciones.

---

## Infrastructure Layer

Proporciona servicios técnicos y recursos de infraestructura.

---

# 8. Flujo General

Toda solicitud seguirá el siguiente recorrido:

```text
Usuario

↓

Interface

↓

Identity

↓

Context

↓

Governance

↓

Constitutional Engine

↓

Kernel

↓

Planning

↓

Reasoning

↓

Memory

↓

Knowledge

↓

Execution

↓

Respuesta
```

---

# 9. Reglas Arquitectónicas

## R-001

El Blueprint constituye la máxima referencia arquitectónica.

---

## R-002

Toda funcionalidad pertenece a una Capability.

---

## R-003

El Kernel no implementa lógica de negocio.

---

## R-004

Toda ejecución debe ser validada por el Constitutional Engine.

---

## R-005

Las dependencias circulares están prohibidas.

---

## R-006

Toda comunicación entre módulos se realiza mediante contratos públicos.

---

## R-007

Todo componente posee un único propietario.

---

## R-008

Todo componente posee versión independiente.

---

## R-009

Todo cambio arquitectónico requiere un ADR.

---

## R-010

Toda decisión importante debe ser auditable.

---

## R-011

La memoria constituye un servicio independiente.

---

## R-012

El conocimiento constituye un servicio independiente.

---

## R-013

La planificación es independiente del razonamiento.

---

## R-014

El modelo LLM es reemplazable.

---

## R-015

Toda implementación debe respetar la Constitución Cognitiva.

---

## R-016

Toda implementación debe respetar la Constitución de Gobernanza.

---

## R-017 — Flujo descendente de control y autoridad

El flujo de control, autoridad y solicitudes operativas es descendente: una capa o componente upstream puede solicitar trabajo a un componente downstream únicamente mediante contratos públicos, requests o comandos tipados, o mecanismos de orquestación autorizados.

Los eventos pueden registrar o propagar que una solicitud, resultado o cambio de estado ocurrió, pero no constituyen por sí mismos una transferencia de autoridad ni una orden de control.

---

## R-018 — Prohibición de control ascendente

Una capa o componente downstream no puede iniciar control, autorización, elevación de privilegios, modificación de política ni establecer una dependencia de control ascendente sobre un componente upstream.

Las consultas, validaciones o servicios autorizados por contrato no transfieren control ni autoridad al componente solicitante.

---

## R-019 — Retorno ascendente de resultados y evidencia

Los resultados, estados, errores, métricas, eventos y evidencia pueden propagarse desde capas inferiores hacia capas superiores únicamente como retorno de una solicitud previa o mediante eventos tipados y contratos definidos.

Este retorno no constituye control ascendente.

---

## R-020 — Autoridad no transferible por retorno

La propagación ascendente de resultados o evidencia no concede autoridad al emisor inferior sobre el receptor superior.

La autoridad permanece en la capa o componente que la posee según Blueprint, Gobernanza y contratos aplicables.

---

## R-021 — Prohibición de bypass y ciclos de control

Queda prohibido:

* iniciar invocaciones directas ascendentes de control;
* utilizar eventos como órdenes encubiertas hacia capas superiores;
* saltar capas de autoridad o validación;
* crear ciclos de dependencia o de control;
* reinterpretar un resultado, evento o receipt como autorización.

---

# 10. Componentes Estratégicos

El Blueprint establece los siguientes componentes principales:

* Constitutional Engine
* Kernel
* Capability Manager
* Planning Engine
* Reasoning Engine
* Memory Layer
* Knowledge Layer
* Execution Layer

Todos los componentes futuros deberán integrarse dentro de esta estructura.

---

# 11. Evolución

Ninguna nueva característica podrá incorporarse sin definir:

* capa
* propietario
* contrato
* dependencias
* versión
* reglas de gobernanza
* En v0.6.0-alpha, la interacción con modelos queda desacoplada mediante `Conversation Service`, `Conversation Provider Registry`, `Conversation Provider` y `LLM Runtime`. Ningún modelo o proveedor externo forma parte del Kernel.

---

# 12. Restricciones

Queda prohibido:

* incorporar lógica fuera de las capas definidas
* crear dependencias cruzadas
* modificar directamente el Kernel para agregar funcionalidades
* acoplar componentes al modelo LLM
* omitir la validación constitucional
* acceder directamente a la memoria desde componentes no autorizados

---

# 13. Estado del Blueprint

Versión del Blueprint:

**Blueprint v0.6.1-alpha**

Estado normativo:

**Documento Maestro de Arquitectura aprobado y validado.**

La cobertura de implementación y el sprint operativo vigente se determinan mediante la documentación `CURRENT_STATE` del proyecto y no forman parte del estado normativo de este Blueprint.

---

# 14. Próximos documentos derivados

A partir de este Blueprint deberán desarrollarse:

* Kernel Specification
* Constitution Specification
* Capability SDK
* Domain Model
* Event Model
* Memory Specification
* Knowledge Specification
* ADR Repository
* API Contracts
* Infrastructure Specification

---

# Fin del Documento

# Malāk BLUEPRINT

**Versión:** 0.5.0-alpha
**Documento:** BP-002
**Título:** Arquitectura Detallada de Capas
**Estado:** Aprobado
**Sprint:** Sprint 1B
**Dependencia:** BP-001

---

# 1. Objetivo

Definir la arquitectura detallada de cada capa de Malāk.

Cada capa deberá tener responsabilidades claras, límites definidos, entradas, salidas, dependencias permitidas y dependencias prohibidas.

---

# 2. Regla General

Ninguna implementación podrá existir fuera de una capa definida.

Toda capa debe respetar:

* Constitución Cognitiva
* Constitución de Gobernanza
* Kernel
* Gobernanza
* Contratos públicos
* Modelo de eventos
* Capability First Architecture

---

# 3. Interface Layer

## Propósito

Gestionar la interacción entre el usuario y Malāk.

## Responsabilidades

* recibir solicitudes
* presentar respuestas
* gestionar canales de interacción
* normalizar entrada del usuario
* enviar eventos iniciales al sistema

## Entradas

* texto
* voz
* archivos
* comandos
* eventos externos autorizados

## Salidas

* respuesta al usuario
* solicitudes normalizadas
* eventos de interacción

## Dependencias permitidas

* Identity Layer
* Context Layer

## Dependencias prohibidas

* Memory Layer
* Knowledge Layer
* Execution Layer
* Infrastructure directa

## Eventos emitidos

* UserInputReceived
* UserCommandReceived
* UserFileSubmitted

## Estado inicial

**Activo**

---

# 4. Identity Layer

## Propósito

Gestionar identidad, perfil, permisos y sesión del usuario.

## Responsabilidades

* identificar usuario
* validar sesión
* cargar perfil operativo
* resolver permisos base
* asociar solicitud a identidad

## Entradas

* solicitud normalizada
* datos de sesión
* metadatos de usuario

## Salidas

* identidad validada
* perfil activo
* permisos iniciales

## Dependencias permitidas

* Governance Layer
* Infrastructure Layer

## Dependencias prohibidas

* Execution Layer
* Reasoning Engine
* Planning Engine

## Eventos emitidos

* IdentityResolved
* SessionValidated
* PermissionProfileLoaded

## Estado inicial

**Activo**

---

# 5. Context Layer

## Propósito

Construir el contexto operativo de cada solicitud.

## Responsabilidades

* crear contexto activo
* definir alcance
* identificar intención
* cargar metadatos relevantes
* preparar el marco de procesamiento

## Entradas

* identidad validada
* solicitud del usuario
* estado de sesión

## Salidas

* contexto activo
* intención preliminar
* restricciones iniciales

## Dependencias permitidas

* Identity Layer
* Governance Layer
* Memory Layer mediante contrato

## Dependencias prohibidas

* Execution Layer directa
* Kernel directo sin validación
* acceso directo a base de datos

## Eventos emitidos

* ContextCreated
* IntentDetected
* ScopeDefined

## Estado inicial

**Activo**

---

# 6. Governance Layer

## Propósito

Administrar las políticas operativas generales del sistema.

## Responsabilidades

* aplicar reglas de gobernanza
* resolver permisos
* definir restricciones
* validar compatibilidad operativa
* preparar políticas para el Constitutional Engine

## Entradas

* contexto activo
* identidad
* solicitud
* política vigente

## Salidas

* restricciones aplicables
* permisos efectivos
* reglas activas

## Dependencias permitidas

* Identity Layer
* Constitutional Engine
* Policy Store

## Dependencias prohibidas

* Execution Layer directa
* modificación directa de memoria
* modificación directa del Kernel

## Eventos emitidos

* GovernancePolicyLoaded
* GovernanceCheckRequested
* EffectivePermissionsResolved

## Estado inicial

**Activo**

---

# 7. Constitutional Engine

## Propósito

Validar que toda operación respete la Constitución Cognitiva y la Constitución de Gobernanza.

## Responsabilidades

* validar acciones
* aprobar operaciones
* rechazar operaciones inválidas
* auditar decisiones críticas
* bloquear ejecuciones riesgosas
* aplicar reglas constitucionales

## Entradas

* contexto
* permisos efectivos
* intención
* plan propuesto
* acción propuesta

## Salidas

* aprobación
* rechazo
* restricciones adicionales
* evento de auditoría

## Dependencias permitidas

* Governance Layer
* Audit System
* Policy Store

## Dependencias prohibidas

* ejecutar herramientas
* modificar memoria
* modificar conocimiento
* razonar por cuenta propia
* planificar tareas

## Eventos emitidos

* ConstitutionalCheckRequested
* ConstitutionalCheckPassed
* ConstitutionalCheckFailed
* OperationRejected

## Estado inicial

**Activo obligatorio**

---

# 8. Kernel

## Propósito

Coordinar el ciclo de vida interno de la plataforma.

## Responsabilidades

* orquestar flujo general
* despachar solicitudes
* coordinar módulos
* mantener estado operativo
* controlar ciclo de procesamiento

## Entradas

* contexto validado
* operación aprobada
* eventos del sistema

## Salidas

* solicitudes a motores internos
* eventos de coordinación
* respuesta procesada

## Dependencias permitidas

* Constitutional Engine
* Capability Manager
* Planning Engine
* Reasoning Engine
* Event Bus

## Dependencias prohibidas

* lógica de negocio
* ejecución directa de herramientas
* modificación directa de memoria
* acceso directo a documentos
* dependencia directa de modelos LLM

## Eventos emitidos

* KernelCycleStarted
* KernelDispatchRequested
* KernelCycleCompleted
* KernelErrorRaised

## Estado inicial

**Activo crítico**

---

# 9. Capability Manager

## Propósito

Administrar todas las capacidades registradas en Malāk.

## Responsabilidades

* registrar capacidades
* cargar capacidades
* descargar capacidades
* validar dependencias
* verificar versiones
* exponer capacidades disponibles
* controlar permisos de capacidades

## Entradas

* solicitud del Kernel
* metadata de Capability
* política de permisos

## Salidas

* Capability habilitada
* Capability rechazada
* catálogo actualizado

## Dependencias permitidas

* Kernel
* Governance Layer
* Capability Registry
* Infrastructure Layer

## Dependencias prohibidas

* ejecución directa sin autorización
* acceso directo a memoria
* modificación directa del Kernel

## Eventos emitidos

* CapabilityRegistered
* CapabilityLoaded
* CapabilityRejected
* CapabilityDisabled

## Estado inicial

**Activo**

---

# 10. Planning Engine

## Propósito

Convertir objetivos en planes ejecutables.

## Responsabilidades

* descomponer objetivos
* generar tareas
* ordenar pasos
* priorizar acciones
* replanificar ante errores
* producir planes validables

## Entradas

* objetivo
* contexto
* capacidades disponibles
* restricciones

## Salidas

* plan
* tareas
* dependencias del plan
* condiciones de éxito

## Dependencias permitidas

* Kernel
* Capability Manager
* Reasoning Engine
* Constitutional Engine para validación

## Dependencias prohibidas

* ejecutar acciones
* modificar memoria
* escribir conocimiento
* acceder directamente a infraestructura

## Eventos emitidos

* PlanRequested
* PlanGenerated
* PlanRejected
* ReplanRequested

## Estado inicial

**Activo**

---

# 11. Reasoning Engine

## Propósito

Realizar inferencia, evaluación lógica y selección de alternativas.

## Responsabilidades

* razonar sobre contexto
* evaluar hipótesis
* comparar alternativas
* validar coherencia
* asistir planificación
* asistir respuesta

## Entradas

* contexto
* problema
* hipótesis
* conocimiento recuperado
* restricciones

## Salidas

* inferencia
* evaluación
* recomendación
* justificación

## Dependencias permitidas

* Kernel
* Knowledge Layer mediante contrato
* Memory Layer mediante contrato
* Model Provider mediante abstracción de Runtime

## Dependencias prohibidas

* ejecución directa
* modificación directa de memoria
* acceso directo a base de datos
* dependencia rígida de un modelo LLM

## Eventos emitidos

* ReasoningRequested
* ReasoningCompleted
* ReasoningFailed
* HypothesisEvaluated

## Estado inicial

**Activo**

---

# 12. Memory Layer

## Propósito

Gestionar la memoria del sistema.

## Responsabilidades

* almacenar memoria autorizada
* recuperar memoria relevante
* consolidar memoria
* comprimir memoria
* archivar memoria
* aplicar olvido controlado

## Submódulos

* Working Memory
* Episodic Memory
* Semantic Memory
* Procedural Memory
* Archive Memory

## Entradas

* solicitudes de lectura
* solicitudes de escritura
* eventos aprobados
* contexto validado

## Salidas

* memoria recuperada
* memoria actualizada
* memoria archivada

## Dependencias permitidas

* Constitutional Engine
* Knowledge Layer
* Infrastructure Layer

## Dependencias prohibidas

* aceptar escrituras sin validación
* ejecutar herramientas
* razonar
* planificar

## Eventos emitidos

* MemoryReadRequested
* MemoryRetrieved
* MemoryUpdateRequested
* MemoryUpdated
* MemoryArchived

## Estado inicial

**Activo controlado**

---

# 13. Knowledge Layer

## Propósito

Gestionar conocimiento documental, estructurado y recuperable.

## Responsabilidades

* indexar documentos
* generar embeddings
* consultar RAG
* mantener Knowledge Graph
* verificar fuentes
* versionar conocimiento

## Componentes

* Document Store
* Embedding Store
* ChromaDB
* Knowledge Graph
* Indexer
* Verifier

## Entradas

* documentos
* consultas
* solicitudes de recuperación
* metadata

## Salidas

* fragmentos recuperados
* fuentes
* evidencia
* relaciones de conocimiento

## Dependencias permitidas

* Memory Layer
* Infrastructure Layer
* Constitutional Engine

## Dependencias prohibidas

* ejecutar acciones
* modificar memoria sin contrato
* decidir por el Kernel
* razonar por cuenta propia

## Eventos emitidos

* KnowledgeIndexed
* KnowledgeRetrieved
* SourceVerified
* DocumentRejected

## Estado inicial

**Activo**

---

# 14. Execution Layer

## Propósito

Ejecutar acciones autorizadas.

## Responsabilidades

* ejecutar tools
* ejecutar agentes
* ejecutar automatizaciones
* llamar APIs
* correr workflows
* devolver resultados

## Entradas

* plan aprobado
* tarea aprobada
* Capability autorizada
* permisos efectivos

## Salidas

* resultado de ejecución
* error de ejecución
* evento de finalización

## Dependencias permitidas

* Kernel
* Capability Manager
* Constitutional Engine
* Infrastructure Layer

## Dependencias prohibidas

* modificar memoria directamente
* modificar Constitución
* modificar Kernel
* ejecutar sin validación previa

## Eventos emitidos

* ExecutionRequested
* ExecutionStarted
* ExecutionCompleted
* ExecutionFailed
* ToolInvoked

## Estado inicial

**Activo restringido**

---

# 15. Infrastructure Layer

## Propósito

Proveer los servicios técnicos necesarios para operar Malāk.

## Responsabilidades

* contenedores
* bases de datos
* almacenamiento
* redes
* APIs internas
* logs técnicos
* colas
* healthchecks
* secretos

## Componentes

* Docker
* Docker Compose
* SQL Server
* ChromaDB
* Open WebUI
* * Ollama, como runtime externo intercambiable mediante contrato
* FastAPI
* File System
* Backup System

## Entradas

* solicitudes técnicas autorizadas
* operaciones internas
* eventos de infraestructura

## Salidas

* servicios disponibles
* logs
* estado de salud
* errores técnicos

## Dependencias permitidas

* todas las capas mediante contrato técnico

## Dependencias prohibidas

* lógica de negocio
* decisiones cognitivas
* razonamiento
* gobernanza

## Eventos emitidos

* ServiceStarted
* ServiceStopped
* HealthCheckPassed
* HealthCheckFailed
* BackupCreated

## Estado inicial

**Activo base**

---

# 16. Reglas Globales de Dependencia

## Interpretación de dependencias

Las secciones históricas denominadas **Dependencias permitidas** describen relaciones contractuales o servicios autorizados entre componentes.

No deben interpretarse como autorización para invertir el flujo de control.

Cuando una capa inferior necesite validación, política, contexto o información perteneciente a una capa superior, no inicia control sobre ella: utiliza el contrato, request o comando tipado, broker u orquestación previstos por la arquitectura.

Los eventos pueden propagar hechos, resultados o evidencia, pero no transfieren control ni autoridad.

La dirección de control y autoridad permanece siempre descendente.

## D-001

Las capas superiores pueden solicitar servicios a capas inferiores solo mediante contratos.

## D-002

Las capas inferiores no deben conocer detalles internos de capas superiores.

## D-003

Ninguna capa puede saltar el Constitutional Engine cuando la operación implique riesgo, memoria, ejecución o permisos.

## D-004

Execution Layer nunca escribe directamente en Memory Layer.

## D-005

Knowledge Layer no decide acciones.

## D-006

Memory Layer no ejecuta acciones.

## D-007

Kernel coordina, pero no implementa lógica funcional.

## D-008

Planning Engine propone planes; no ejecuta.

## D-009

Reasoning Engine evalúa; no ejecuta.

## D-010

Capability Manager registra y habilita; no ejecuta lógica de negocio por sí mismo.

---

## D-011 — Dirección del control

Las solicitudes de control y trabajo fluyen desde componentes superiores hacia componentes inferiores.

---

## D-012 — Dirección de resultados

Los componentes inferiores pueden devolver resultados, errores, estados, métricas y evidencia hacia el componente superior que originó el trabajo o hacia consumidores autorizados mediante contratos o eventos.

---

## D-013 — No invocación ascendente

Un componente inferior no puede invocar directamente a un componente superior para ordenarle trabajo, modificar su estado de autoridad, concederse permisos o alterar su política.

---

## D-014 — Eventos sin autoridad implícita

Un evento emitido desde una capa inferior hacia una superior representa un hecho, resultado o evidencia.

No representa una orden, autorización ni transferencia de autoridad.

---

## D-015 — No circularidad operacional

Quedan prohibidos los ciclos de control, dependencia operacional o autorización entre capas.

La existencia de un canal de retorno no convierte la relación en una dependencia circular.

---

# 17. Estados de Capa

Cada capa deberá reportar uno de los siguientes estados:

* Active
* Inactive
* Degraded
* Failed
* Maintenance
* Disabled
* Unknown

---

# 18. Criterio de Implementación

Una capa se considera implementada cuando posee:

* contrato público
* eventos definidos
* healthcheck
* logs mínimos
* dependencias declaradas
* errores controlados
* documentación técnica
* pruebas básicas

---

# 19. Resultado

BP-002 establece la arquitectura detallada de capas de Malāk y define los límites operativos para cada componente del sistema.

Desde esta versión, cualquier implementación futura deberá mapearse explícitamente a una capa, declarar sus dependencias y respetar las reglas de comunicación, gobernanza y validación constitucional.

---

# Fin del Documento

# 6. Flujo General del Sistema

## 6.1 Objetivo

Definir el ciclo de vida completo de una solicitud dentro de Malāk.

Este flujo es obligatorio para todas las Capabilities, agentes, herramientas, automatizaciones y módulos futuros.

---

## 6.2 Flujo Maestro

```text
Usuario
    │
    ▼
Interface Layer
    │
    ▼
Identity Layer
    │
    ▼
Context Layer
    │
    ▼
Governance Layer
    │
    ▼
Constitutional Engine
    │
    ▼
Kernel
    │
    ▼
Capability Manager
    │
    ▼
Planning Engine
    │
    ▼
Reasoning Engine
    │
    ▼
Memory Layer
    │
    ▼
Knowledge Layer
    │
    ▼
Execution Layer
    │
    ▼
Kernel
    │
    ▼
Interface Layer
    │
    ▼
Usuario
```

> **Regla de interpretación del retorno:** el tramo `Execution Layer → Kernel → Interface Layer` representa propagación ascendente de resultado, estado y evidencia hacia el orquestador y la interfaz. No representa una nueva invocación ascendente de control ni una dependencia operacional inversa.

---

## 6.3 Fases del Procesamiento

### Fase 1 — Recepción

**Responsable:** Interface Layer

**Acciones:**

* recibir solicitud
* validar formato
* generar RequestID
* generar CorrelationID
* emitir evento inicial

**Evento emitido:** `RequestReceived`

---

### Fase 2 — Identificación

**Responsable:** Identity Layer

**Acciones:**

* validar usuario
* cargar perfil operativo
* cargar permisos base
* validar sesión

**Evento emitido:** `IdentityValidated`

---

### Fase 3 — Construcción de Contexto

**Responsable:** Context Layer

**Acciones:**

* identificar intención
* cargar contexto activo
* determinar alcance
* adjuntar metadatos relevantes

**Evento emitido:** `ContextCreated`

---

### Fase 4 — Gobernanza

**Responsable:** Governance Layer

**Acciones:**

* cargar políticas activas
* calcular permisos efectivos
* preparar restricciones operativas

**Evento emitido:** `GovernanceValidated`

---

### Fase 5 — Validación Constitucional

**Responsable:** Constitutional Engine

**Acciones:**

* validar Constitución Cognitiva
* validar Constitución de Gobernanza
* aprobar operación
* rechazar operación
* registrar decisión crítica

**Eventos emitidos:**

* `OperationApproved`
* `OperationRejected`

---

### Fase 6 — Orquestación

**Responsable:** Kernel

**Acciones:**

* seleccionar flujo operativo
* coordinar componentes
* iniciar ciclo de procesamiento
* despachar solicitud a subsistemas

**Evento emitido:** `KernelDispatchStarted`

---

### Fase 7 — Descubrimiento de Capacidades

**Responsable:** Capability Manager

**Acciones:**

* localizar capacidades disponibles
* verificar versión
* verificar permisos
* resolver dependencias
* exponer capacidades habilitadas

**Evento emitido:** `CapabilitiesResolved`

---

### Fase 8 — Planificación

**Responsable:** Planning Engine

**Acciones:**

* dividir objetivo en tareas
* generar plan
* priorizar pasos
* definir condiciones de éxito
* solicitar validación si corresponde

**Evento emitido:** `PlanGenerated`

---

### Fase 9 — Razonamiento

**Responsable:** Reasoning Engine

**Acciones:**

* analizar contexto
* evaluar alternativas
* seleccionar estrategia
* generar justificación
* validar coherencia lógica

**Evento emitido:** `ReasoningCompleted`

---

### Fase 10 — Recuperación de Memoria

**Responsable:** Memory Layer

**Acciones:**

* recuperar memoria relevante
* consolidar contexto histórico
* devolver recuerdos autorizados

**Evento emitido:** `MemoryRetrieved`

---

### Fase 11 — Recuperación de Conocimiento

**Responsable:** Knowledge Layer

**Acciones:**

* consultar RAG
* consultar Knowledge Graph
* recuperar documentos
* validar evidencia
* adjuntar fuentes

**Evento emitido:** `KnowledgeRetrieved`

---

### Fase 12 — Ejecución

**Responsable:** Execution Layer

**Acciones:**

* ejecutar herramientas
* ejecutar agentes
* llamar APIs
* ejecutar workflows
* devolver resultado operativo

**Evento emitido:** `ExecutionCompleted`

---

### Fase 13 — Consolidación

**Responsable:** Kernel

**Acciones:**

* consolidar resultados
* verificar consistencia
* preparar respuesta final
* registrar estado final

**Evento emitido:** `ResponseBuilt`

---

### Fase 14 — Entrega

**Responsable:** Interface Layer

**Acciones:**

* renderizar respuesta
* devolver resultado al usuario
* cerrar solicitud

**Evento emitido:** `ResponseDelivered`

---

## 6.4 Reglas Globales del Flujo

### F-001

Toda solicitud genera un `RequestID` único.

---

### F-002

Toda operación comparte un `CorrelationID` para trazabilidad.

---

### F-003

Cada fase debe registrar inicio y fin.

---

### F-004

Si una fase falla, el Kernel debe decidir entre:

* reintentar
* replanificar
* abortar
* escalar

---

### F-005

Ninguna fase puede omitir al Constitutional Engine cuando la operación implique:

* ejecución
* escritura
* modificación de memoria
* acceso a recursos sensibles
* uso de herramientas
* modificación de conocimiento
* cambio de configuración

---

### F-006

Cada fase debe emitir al menos un evento.

---

### F-007

Las fases son desacopladas.

No pueden invocarse directamente entre sí fuera de contratos definidos.

---

### F-008

Todo resultado debe incluir metadatos mínimos:

* RequestID
* CorrelationID
* Timestamp
* Capability utilizada
* Estado final
* Tiempo de procesamiento

---

## 6.5 Resultado

El Blueprint define un pipeline único, gobernado y trazable.

Toda Capability, agente, herramienta o integración futura deberá insertarse en este flujo sin alterar su estructura base.

# Fin de la sección

# 7. Modelo de Eventos

## 7.1 Objetivo

Definir el mecanismo oficial de comunicación interna entre los componentes de Malāk.

Toda interacción entre capas deberá realizarse mediante eventos tipados, trazables y auditables, salvo en los casos donde exista un contrato síncrono explícitamente definido.

---

# 7.2 Principios

## E-001

Los eventos representan hechos ocurridos.

Nunca representan lógica de negocio.

---

## E-002

Los eventos son inmutables.

Una vez emitidos no pueden modificarse.

---

## E-003

Todo evento posee identidad única.

---

## E-004

Todo evento es auditable.

---

## E-005

Todo evento es trazable de extremo a extremo.

---

## E-006

Los eventos son independientes del modelo LLM utilizado.

---

## E-007

Los eventos nunca contienen lógica de ejecución.

---

# 7.3 Estructura Base

Todo evento deberá implementar el siguiente contrato mínimo:

```yaml
event_id:
event_type:
event_version:

request_id:
correlation_id:
causation_id:

source:
target:

timestamp:

severity:

status:

payload:

metadata:
```

---

# 7.4 Descripción de Campos

| Campo          | Descripción                            |
| -------------- | -------------------------------------- |
| event_id       | Identificador único del evento         |
| event_type     | Tipo de evento                         |
| event_version  | Versión del contrato                   |
| request_id     | Solicitud asociada                     |
| correlation_id | Identificador de la operación completa |
| causation_id   | Evento que originó este evento         |
| source         | Componente emisor                      |
| target         | Destinatario esperado                  |
| timestamp      | Fecha y hora UTC                       |
| severity       | Nivel de criticidad                    |
| status         | Estado del evento                      |
| payload        | Información útil                       |
| metadata       | Información adicional                  |

---

# 7.5 Severidad

Valores permitidos:

```text
TRACE

DEBUG

INFO

NOTICE

WARNING

ERROR

CRITICAL

FATAL
```

---

# 7.6 Estado del Evento

Estados oficiales:

```text
Created

Published

Received

Processing

Completed

Rejected

Cancelled

Expired

Failed

Archived
```

---

# 7.7 Tipos de Eventos

## Eventos de Usuario

```text
RequestReceived

UserAuthenticated

UserDisconnected

UserCancelledRequest
```

---

## Eventos de Contexto

```text
ContextCreated

IntentDetected

ScopeDefined

ContextUpdated
```

---

## Eventos de Gobernanza

```text
GovernanceValidated

GovernanceRejected

PermissionGranted

PermissionDenied

PolicyLoaded
```

---

## Eventos Constitucionales

```text
OperationApproved

OperationRejected

ConstitutionViolation

PolicyViolation

RiskDetected
```

---

## Eventos del Kernel

```text
KernelStarted

KernelDispatchStarted

KernelDispatchCompleted

KernelRecovered

KernelError
```

---

## Eventos de Capacidades

```text
CapabilityRegistered

CapabilityLoaded

CapabilityEnabled

CapabilityDisabled

CapabilityUpdated

CapabilityRemoved
```

---

## Eventos de Planificación

```text
PlanRequested

PlanGenerated

PlanRejected

ReplanRequested

PlanCompleted
```

---

## Eventos de Razonamiento

```text
ReasoningRequested

ReasoningCompleted

ReasoningRejected

HypothesisGenerated

HypothesisValidated
```

---

## Eventos de Memoria

```text
MemoryReadRequested

MemoryRetrieved

MemoryStored

MemoryUpdated

MemoryArchived

MemoryCompacted
```

---

## Eventos de Conocimiento

```text
KnowledgeRetrieved

KnowledgeIndexed

KnowledgeUpdated

KnowledgeValidated

SourceVerified
```

---

## Eventos de Ejecución

```text
ExecutionRequested

ExecutionStarted

ExecutionCompleted

ExecutionCancelled

ExecutionFailed

ToolInvoked

AgentExecuted
```

---

## Eventos de Infraestructura

```text
HealthCheckPassed

HealthCheckFailed

ServiceStarted

ServiceStopped

BackupCreated

BackupRestored
```

---

# 7.8 Flujo de un Evento

```text
Evento Creado
        │
        ▼
Validación del Contrato
        │
        ▼
Publicación
        │
        ▼
Recepción
        │
        ▼
Procesamiento
        │
        ▼
Resultado
        │
        ▼
Archivado
```

---

# 7.9 Reglas de Emisión

## EV-001

Todo evento deberá poseer un EventID único.

---

## EV-002

Todo evento deberá pertenecer a un CorrelationID.

---

## EV-003

Todo evento deberá indicar su componente emisor.

---

## EV-004

Todo evento deberá indicar versión del contrato.

---

## EV-005

Todo evento deberá registrar Timestamp UTC.

---

## EV-006

Todo evento deberá poder auditarse.

---

## EV-007

Los eventos nunca modificarán directamente el estado del sistema.

---

## EV-008 — Eventos ascendentes como evidencia

Un evento emitido desde una capa inferior hacia una capa superior puede transportar resultado, estado, error, métrica o evidencia.

No puede utilizarse para iniciar autoridad, conceder permisos, ordenar trabajo al componente superior ni alterar políticas.

---

## EV-009 — Respeto de jerarquía

El campo `target` de un evento no autoriza bypass de capas, inversión del flujo de control ni invocación ascendente directa.

Toda acción derivada del evento debe ser decidida por el componente que posea la autoridad correspondiente.

---

# 7.10 Reglas de Consumo

## EC-001

Un consumidor nunca debe asumir el orden absoluto de llegada.

---

## EC-002

Los consumidores deberán ser idempotentes.

---

## EC-003

Los consumidores deberán validar la versión del contrato.

---

## EC-004

Los consumidores deberán ignorar eventos desconocidos de forma segura.

---

## EC-005

Un evento procesado no podrá procesarse nuevamente salvo recuperación explícita.

---

# 7.11 Eventos Prohibidos

Queda prohibido emitir eventos que:

* contengan credenciales
* contengan secretos
* contengan tokens de autenticación
* ejecuten código
* contengan lógica de negocio
* modifiquen memoria directamente
* modifiquen conocimiento directamente

---

# 7.12 Auditoría

Todo evento deberá quedar registrado con:

* EventID
* RequestID
* CorrelationID
* Emisor
* Destino
* Fecha
* Resultado
* Duración
* Estado final

---

# 7.13 Versionado

Cada contrato de evento tendrá:

```text
Major.Minor.Patch
```

Ejemplo:

```text
RequestReceived v1.0.0

ExecutionCompleted v2.1.3
```

---

# 7.14 Compatibilidad

Los consumidores deberán soportar, como mínimo:

* misma versión mayor
* versiones menores compatibles

Los cambios incompatibles requerirán incrementar la versión mayor del contrato.

---

# 7.15 Integración con el Kernel

El Kernel actuará como coordinador del flujo de eventos.

No podrá modificar el contenido de un evento publicado.

Solo podrá:

* enrutar
* priorizar
* registrar
* coordinar
* recuperar eventos cuando corresponda

---

# 7.16 Resultado

El Modelo de Eventos establece un mecanismo de comunicación desacoplado, versionado y auditable entre todos los componentes de Malāk.

Este modelo constituye la base para la orquestación interna de la plataforma y será obligatorio para cualquier componente incorporado en futuras versiones.

# Fin de la sección

# 8. Modelo de Dominio

## 8.1 Objetivo

Definir el modelo conceptual oficial de Malāk.

El Modelo de Dominio establece las entidades principales de la plataforma, sus responsabilidades y relaciones.

Toda implementación deberá mapearse sobre este dominio.

---

# 8.2 Principios

## DM-001

Toda entidad posee una única responsabilidad.

---

## DM-002

Toda entidad posee identidad propia.

---

## DM-003

Las entidades se relacionan mediante contratos.

---

## DM-004

Las entidades son independientes de la implementación técnica.

---

## DM-005

El dominio no depende del modelo LLM.

---

# 8.3 Entidades del Dominio

```text
User

Identity

Session

Request

Context

Goal

Plan

Task

Capability

CapabilityVersion

CapabilityRegistry

Agent

Tool

Workflow

Reasoning

Memory

Knowledge

Document

Embedding

KnowledgeGraph

Event

Policy

Constitution

Decision

AuditLog

HealthStatus

InfrastructureService
```

---

# 8.4 User

## Propósito

Representa al propietario o consumidor del sistema.

## Atributos mínimos

```yaml
user_id
display_name
profile
preferences
timezone
status
created_at
updated_at
```

---

# 8.5 Identity

## Propósito

Representa la identidad operativa utilizada por Malāk.

## Atributos

```yaml
identity_id
user_id
roles
permissions
authentication_provider
status
```

---

# 8.6 Session

## Propósito

Representa una sesión activa de interacción.

## Atributos

```yaml
session_id
user_id
started_at
last_activity
state
context_id
```

---

# 8.7 Request

## Propósito

Representa una solicitud realizada al sistema.

## Atributos

```yaml
request_id
session_id
goal_id
request_type
priority
status
created_at
completed_at
```

---

# 8.8 Context

## Propósito

Representa el contexto operativo utilizado durante el procesamiento.

## Atributos

```yaml
context_id
request_id
identity_id
memory_snapshot
knowledge_snapshot
constraints
metadata
```

---

# 8.9 Goal

## Propósito

Representa el objetivo que Malāk debe alcanzar.

## Atributos

```yaml
goal_id
request_id
description
priority
status
success_criteria
```

---

# 8.10 Plan

## Propósito

Representa un plan generado por Planning Engine.

## Atributos

```yaml
plan_id
goal_id
version
status
estimated_cost
estimated_time
```

---

# 8.11 Task

## Propósito

Representa una unidad mínima de trabajo.

## Atributos

```yaml
task_id
plan_id
capability_id
status
priority
order
```

---

# 8.12 Capability

## Propósito

Representa una capacidad registrada dentro de Malāk.

## Atributos

```yaml
capability_id
name
version
owner
permissions
status
category
```

---

# 8.13 CapabilityVersion

## Propósito

Controlar versiones compatibles.

## Atributos

```yaml
version_id
capability_id
semantic_version
compatibility
checksum
release_date
```

---

# 8.14 CapabilityRegistry

## Propósito

Repositorio oficial de capacidades.

## Contiene

* capacidades registradas
* versiones
* dependencias
* estado
* permisos

---

# 8.15 Agent

## Propósito

Representa una entidad autónoma especializada.

## Atributos

```yaml
agent_id
name
role
capabilities
status
owner
```

---

# 8.16 Tool

## Propósito

Representa una herramienta ejecutable.

## Atributos

```yaml
tool_id
name
provider
version
permissions
status
```

---

# 8.17 Workflow

## Propósito

Representa una secuencia reutilizable de ejecución.

## Atributos

```yaml
workflow_id
tasks
version
status
```

---

# 8.18 Reasoning

## Propósito

Representa el resultado del proceso de razonamiento.

## Atributos

```yaml
reasoning_id
strategy
confidence
evidence
result
```

---

# 8.19 Memory

## Propósito

Representa una unidad de memoria.

## Atributos

```yaml
memory_id
memory_type
importance
confidence
source
created_at
expires_at
```

---

# 8.20 Knowledge

## Propósito

Representa conocimiento disponible para consulta.

## Atributos

```yaml
knowledge_id
source
trust_score
version
status
```

---

# 8.21 Document

## Propósito

Representa un documento indexado.

## Atributos

```yaml
document_id
title
type
checksum
owner
created_at
```

---

# 8.22 Embedding

## Propósito

Representa un vector generado.

## Atributos

```yaml
embedding_id
document_id
model
dimensions
version
```

---

# 8.23 KnowledgeGraph

## Propósito

Representa relaciones semánticas.

## Componentes

* Nodes
* Edges
* Relationships
* Labels

---

# 8.24 Event

## Propósito

Representa un evento del sistema.

## Atributos

```yaml
event_id
event_type
request_id
correlation_id
timestamp
payload
status
```

---

# 8.25 Policy

## Propósito

Representa una política de gobernanza.

## Atributos

```yaml
policy_id
name
scope
priority
enabled
```

---

# 8.26 Constitution

## Propósito

Representa las reglas constitucionales activas.

## Componentes

* Cognitive Constitution
* Governance Constitution

---

# 8.27 Decision

## Propósito

Representa una decisión relevante tomada por Malāk.

## Atributos

```yaml
decision_id
reasoning_id
confidence
approved
timestamp
```

---

# 8.28 AuditLog

## Propósito

Registrar toda operación relevante.

## Atributos

```yaml
audit_id
entity
operation
actor
timestamp
result
```

---

# 8.29 HealthStatus

## Propósito

Representar el estado operativo de un componente.

## Valores

```text
Healthy
Warning
Degraded
Failed
Maintenance
Unknown
```

---

# 8.30 InfrastructureService

## Propósito

Representa un servicio de infraestructura.

## Ejemplos

* Ollama
* Open WebUI
* SQL Server
* ChromaDB
* FastAPI
* Docker
* Redis
* MinIO

---

# 8.31 Relaciones Principales

```text
User
 │
 └── Identity
       │
       └── Session
              │
              └── Request
                     │
                     ├── Context
                     ├── Goal
                     │      │
                     │      └── Plan
                     │             │
                     │             └── Task
                     │                    │
                     │                    └── Capability
                     │                           │
                     │                           ├── Tool
                     │                           ├── Workflow
                     │                           └── Agent
                     │
                     ├── Memory
                     ├── Knowledge
                     │      ├── Document
                     │      ├── Embedding
                     │      └── KnowledgeGraph
                     │
                     ├── Event
                     ├── Decision
                     └── AuditLog
```

---

# 8.32 Reglas del Dominio

## DOM-001

Toda Request pertenece a una Session.

---

## DOM-002

Toda Session pertenece a un User.

---

## DOM-003

Todo Plan pertenece a un Goal.

---

## DOM-004

Toda Task pertenece a un Plan.

---

## DOM-005

Toda Task debe ejecutarse mediante una Capability.

---

## DOM-006

Toda Capability puede utilizar cero o más Tools.

---

## DOM-007

Todo Agent posee una o más Capabilities.

---

## DOM-008

Toda modificación relevante genera un Event.

---

## DOM-009

Toda decisión genera un AuditLog.

---

## DOM-010

Toda entidad crítica deberá ser versionable cuando corresponda.

---

# 8.33 Resultado

El Modelo de Dominio define el lenguaje común de Malāk. A partir de este punto, la base de datos, las APIs, el SDK de Capabilities, el sistema de memoria y el motor de conocimiento deberán utilizar estas entidades como referencia oficial.

# Fin de la sección

# 9. Modelo de Datos

## 9.1 Objetivo

Definir el modelo oficial de persistencia de Malāk.

Este documento establece:

* qué información debe persistirse
* dónde debe almacenarse
* quién puede acceder
* quién puede modificarla
* cómo se versiona
* cómo se respalda
* cómo se recupera

El Modelo de Datos es independiente de la implementación tecnológica.

---

# 9.2 Principios

## DATA-001

Cada dato posee un único sistema de verdad (Single Source of Truth).

---

## DATA-002

Los datos nunca deben duplicarse innecesariamente.

---

## DATA-003

Cada tipo de dato deberá almacenarse en el motor más adecuado.

---

## DATA-004

Toda escritura deberá ser autorizada por el Constitutional Engine cuando corresponda.

---

## DATA-005

Toda modificación relevante será auditada.

---

## DATA-006

Todo dato deberá poseer trazabilidad.

---

# 9.3 Arquitectura de Persistencia

```text
                        Malāk
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
 Relational Store     Vector Store     Graph Store
   (SQL Server)        (ChromaDB)      (Graph DB)
        │                  │                  │
        ▼                  ▼                  ▼
 Configuración      Embeddings        Relaciones
 Auditoría          Fragmentos        Conocimiento
 Metadata           Búsquedas         Inferencias
 Estado             RAG               Contexto
```

---

# 9.4 Motores de Persistencia

## SQL Server

Responsabilidad:

Persistencia estructurada.

---

## ChromaDB

Responsabilidad:

Búsqueda semántica.

---

## Knowledge Graph

Responsabilidad:

Relaciones entre entidades.

> **Nota:** Aunque inicialmente no se implemente un motor de grafos, el modelo queda definido para permitir una futura migración sin cambios arquitectónicos.

---

## File Storage

Responsabilidad:

Archivos originales.

Ejemplos:

* PDF
* DOCX
* Markdown
* Audio
* Imágenes
* Video
* Código fuente

---

# 9.5 Distribución de Entidades

## SQL Server

Persistirá:

```text
Users

Identities

Sessions

Requests

Goals

Plans

Tasks

Capabilities

CapabilityVersions

Agents

Tools

Policies

Constitutions

AuditLogs

Events

HealthStatus

Configurations

Backups

Workflows

Metrics
```

---

## ChromaDB

Persistirá:

```text
Embeddings

Chunks

DocumentFragments

SemanticIndexes

RAGCollections
```

---

## Graph Store

Persistirá:

```text
Knowledge Nodes

Entity Relations

Ontology

Semantic Links

Concept Maps

Reasoning Links

Decision Relations
```

---

## File Storage

Persistirá:

```text
PDF

Books

Markdown

Images

Audio

Video

Scripts

Configuration Files

Logs

Backups
```

---

# 9.6 Datos Temporales

No deben persistirse:

* contexto de ejecución
* memoria de trabajo
* buffers
* resultados intermedios
* estados efímeros

Su ciclo de vida finalizará al concluir la solicitud, salvo decisión explícita del sistema.

---

# 9.7 Clasificación de Datos

## Nivel 1

Público

Ejemplos:

* documentación pública
* manuales

---

## Nivel 2

Interno

Ejemplos:

* configuraciones
* métricas

---

## Nivel 3

Restringido

Ejemplos:

* memoria
* perfiles
* preferencias

---

## Nivel 4

Crítico

Ejemplos:

* constituciones
* políticas
* auditoría
* claves de infraestructura
* configuraciones sensibles

---

# 9.8 Versionado

Las siguientes entidades deberán ser versionadas:

```text
Capabilities

Policies

Constitutions

Knowledge

Documents

Workflows

Prompts

Agents

Configurations
```

---

# 9.9 Identificadores

Toda entidad persistente deberá poseer:

```yaml
id:
version:
created_at:
updated_at:
created_by:
updated_by:
status:
checksum:
```

---

# 9.10 Integridad

Toda escritura deberá garantizar:

* integridad referencial
* consistencia
* atomicidad
* recuperación
* trazabilidad

---

# 9.11 Auditoría

Toda modificación deberá registrar:

```yaml
entity

operation

actor

timestamp

old_value

new_value

request_id

correlation_id
```

---

# 9.12 Acceso a Datos

Acceso permitido únicamente mediante:

* Repositories
* Services
* Contracts
* SDK oficial

Queda prohibido el acceso directo desde componentes de negocio.

---

# 9.13 Propietarios

Cada entidad posee un propietario único.

Ejemplo:

| Entidad    | Propietario        |
| ---------- | ------------------ |
| User       | Identity Layer     |
| Session    | Identity Layer     |
| Request    | Kernel             |
| Goal       | Planning Engine    |
| Plan       | Planning Engine    |
| Task       | Planning Engine    |
| Memory     | Memory Layer       |
| Knowledge  | Knowledge Layer    |
| Event      | Event Bus          |
| AuditLog   | Governance Layer   |
| Capability | Capability Manager |

---

# 9.14 Reglas de Escritura

## WRITE-001

Solo el propietario puede modificar una entidad.

---

## WRITE-002

Los demás componentes deberán solicitar modificaciones mediante contratos.

---

## WRITE-003

Toda escritura relevante genera:

* Event
* AuditLog

---

## WRITE-004

La eliminación física queda prohibida para entidades críticas.

Se utilizará borrado lógico (`soft delete`) cuando sea aplicable.

---

# 9.15 Estrategia de Backups

Se deberán respaldar:

* SQL Server
* ChromaDB
* Graph Store
* Configuración
* Constituciones
* Policies
* Capabilities
* Documentos

Los backups deberán ser:

* versionados
* verificables
* restaurables
* auditables

---

# 9.16 Recuperación

Toda restauración deberá:

* validar integridad
* validar versión
* validar compatibilidad
* registrar auditoría
* emitir eventos

---

# 9.17 Evolución

Ningún cambio de motor de persistencia deberá afectar:

* el dominio
* los contratos
* las APIs
* las capacidades

La infraestructura podrá reemplazarse manteniendo el mismo modelo lógico.

---

# 9.18 Resultado

El Modelo de Datos establece una arquitectura de persistencia desacoplada, preparada para evolucionar desde una implementación local (SQL Server + ChromaDB + sistema de archivos) hacia una arquitectura distribuida o híbrida sin modificar el dominio de Malāk.

# Fin de la sección

# 10. Modelo de Capacidades (Capability Model)

## 10.1 Objetivo

Definir la especificación oficial de una **Capability** dentro de Malāk.

Toda funcionalidad incorporada a la plataforma deberá implementarse como una Capability registrada.

No existirán funcionalidades "embebidas" fuera de este modelo.

---

# 10.2 Definición

Una **Capability** es una unidad funcional autocontenida, versionable, gobernable y reemplazable que implementa una responsabilidad específica dentro de Malāk.

Ejemplos:

* Responder preguntas
* Indexar documentos
* Ejecutar código
* Consultar una API
* Administrar memoria
* Generar embeddings
* Enviar un correo
* Ejecutar un Workflow
* Controlar dispositivos IoT

---

# 10.3 Principios

## CAP-001

Una Capability implementa una única responsabilidad.

---

## CAP-002

Debe ser desacoplada.

---

## CAP-003

Debe ser reemplazable.

---

## CAP-004

Debe ser registrable.

---

## CAP-005

Debe ser versionable.

---

## CAP-006

Debe ser auditable.

---

## CAP-007

Debe ser gobernable.

---

## CAP-008

Debe poder habilitarse o deshabilitarse sin modificar el Kernel.

---

# 10.4 Ciclo de Vida

```text
Desarrollada
      │
      ▼
Registrada
      │
      ▼
Validada
      │
      ▼
Habilitada
      │
      ▼
Disponible
      │
      ▼
Ejecutándose
      │
      ▼
Suspendida
      │
      ▼
Actualizada
      │
      ▼
Retirada
```

---

# 10.5 Contrato Obligatorio

Toda Capability deberá implementar:

```yaml
capability_id:
name:
display_name:
description:

owner:

category:

semantic_version:

api_version:

status:

permissions:

dependencies:

configuration:

inputs:

outputs:

events:

healthcheck:

telemetry:

documentation:

tests:

checksum:
```

---

# 10.6 Categorías

```text
Core

Reasoning

Planning

Memory

Knowledge

Execution

Tool

Workflow

Agent

Security

Infrastructure

Integration

Automation

Learning

Monitoring

Developer

Experimental
```

---

# 10.7 Estados

```text
Development

Testing

Validated

Enabled

Disabled

Deprecated

Retired

Failed
```

---

# 10.8 Dependencias

Una Capability podrá depender únicamente de:

* contratos públicos
* otras Capabilities registradas
* SDK oficial
* Event Bus

Queda prohibida la dependencia directa con implementaciones internas.

---

# 10.9 Permisos

Toda Capability deberá declarar:

```yaml
can_read_memory:
can_write_memory:

can_read_knowledge:
can_write_knowledge:

can_execute_tools:

can_call_external_api:

can_modify_configuration:

requires_constitution_validation:
```

---

# 10.10 Entradas

Las entradas deberán estar tipadas.

Ejemplo:

```yaml
Goal

Request

Context

Document

MemoryReference

KnowledgeReference

ToolRequest
```

---

# 10.11 Salidas

Las salidas deberán estar tipadas.

Ejemplo:

```yaml
Plan

ReasoningResult

ExecutionResult

KnowledgeResult

MemoryUpdate

Event

Error
```

---

# 10.12 Eventos

Toda Capability deberá declarar:

## Eventos emitidos

```text
CapabilityStarted

CapabilityCompleted

CapabilityFailed

CapabilityCancelled
```

## Eventos consumidos

Declarados explícitamente.

---

# 10.13 Health Check

Cada Capability implementará:

```yaml
status

version

dependencies

last_execution

error_count

latency

availability
```

---

# 10.14 Telemetría

Métricas mínimas:

* ejecuciones
* tiempo promedio
* errores
* éxito
* consumo de memoria
* consumo de CPU
* uso de GPU (cuando aplique)
* tokens utilizados (LLM)
* costo estimado (si aplica)

---

# 10.15 Configuración

Toda configuración deberá ser externa.

Queda prohibido utilizar constantes embebidas en el código para configuraciones operativas.

---

# 10.16 Seguridad

Toda Capability deberá declarar:

* permisos requeridos
* recursos utilizados
* APIs externas
* secretos requeridos
* nivel de riesgo

---

# 10.17 Versionado

Versionado semántico obligatorio.

```text
Major.Minor.Patch
```

Ejemplo:

```text
2.3.1
```

---

# 10.18 Compatibilidad

Cada Capability deberá declarar:

```yaml
minimum_kernel:

maximum_kernel:

minimum_sdk:

supported_api_versions:
```

---

# 10.19 Registro

El Capability Registry almacenará:

* metadata
* versión
* estado
* dependencias
* permisos
* categoría
* propietario
* firma
* checksum

---

# 10.20 Descubrimiento

El Capability Manager podrá descubrir capacidades mediante:

* registro local
* paquetes firmados
* repositorios autorizados
* Marketplace futuro

---

# 10.21 Firma

Las Capabilities podrán incorporar firma digital para verificar:

* integridad
* origen
* autenticidad

---

# 10.22 Reglas

## C-001

El Kernel nunca conocerá implementaciones concretas.

---

## C-002

El Kernel solo conoce contratos.

---

## C-003

Las Capabilities podrán actualizarse independientemente.

---

## C-004

Las Capabilities podrán reemplazarse sin recompilar el sistema.

---

## C-005

Una Capability nunca modificará directamente otra Capability.

---

## C-006

Toda ejecución será registrada.

---

## C-007

Toda ejecución será gobernada por el Constitutional Engine cuando corresponda.

---

## C-008

Toda Capability deberá pasar una validación antes de ser habilitada.

---

## C-009

Las Capabilities experimentales no podrán ejecutarse en producción sin autorización explícita.

---

## C-010

Las Capabilities deberán ser deterministas siempre que la naturaleza de la tarea lo permita. Cuando intervengan modelos probabilísticos, deberán declarar el nivel esperado de no determinismo y las estrategias de mitigación.

---

# 10.23 Roadmap Evolutivo

**Fase 1**

* Registry local
* Capabilities internas

**Fase 2**

* SDK oficial
* Carga dinámica

**Fase 3**

* Marketplace
* Firma digital
* Distribución de paquetes

**Fase 4**

* Ecosistema de terceros
* Certificación de Capabilities
* Repositorio oficial

---

# 10.24 Resultado

El Modelo de Capacidades convierte a Malāk en una plataforma extensible donde toda funcionalidad es un componente independiente, gobernado, versionado y reemplazable.

A partir de este documento, cualquier nueva característica deberá desarrollarse como una Capability registrada, eliminando el acoplamiento al núcleo y permitiendo la evolución del sistema sin afectar su arquitectura.

# Fin de la sección

# 11. Modelo Cognitivo

## 11.1 Objetivo

Definir el modelo cognitivo oficial de Malāk.

El Modelo Cognitivo establece cómo la plataforma interpreta solicitudes, construye entendimiento, razona, decide, ejecuta y aprende bajo control constitucional y gobernanza.

---

## 11.2 Principio Central

Malāk no responde directamente.

Malāk procesa cognitivamente una solicitud antes de producir una respuesta o ejecutar una acción.

Toda operación deberá atravesar un ciclo cognitivo mínimo.

---

## 11.3 Ciclo Cognitivo General

```text
Entrada del Usuario
        │
        ▼
Percepción
        │
        ▼
Comprensión
        │
        ▼
Contextualización
        │
        ▼
Planificación
        │
        ▼
Razonamiento
        │
        ▼
Decisión
        │
        ▼
Validación Constitucional
        │
        ▼
Ejecución
        │
        ▼
Evaluación
        │
        ▼
Aprendizaje Controlado
        │
        ▼
Respuesta
```

---

## 11.4 Etapas Cognitivas

### 11.4.1 Percepción

Convierte la entrada del usuario en una señal procesable.

Incluye:

* texto
* voz
* archivo
* imagen
* comando
* evento externo autorizado

Resultado esperado:

```text
Input normalizado
```

---

### 11.4.2 Comprensión

Interpreta qué solicita el usuario.

Incluye:

* intención
* objetivo
* restricciones
* urgencia
* ambigüedad
* tipo de tarea

Resultado esperado:

```text
Intent + Goal preliminar
```

---

### 11.4.3 Contextualización

Construye el contexto activo.

Incluye:

* sesión
* identidad
* memoria relevante
* conocimiento disponible
* políticas aplicables
* estado del sistema

Resultado esperado:

```text
Contexto operativo
```

---

### 11.4.4 Planificación

Transforma el objetivo en pasos.

Incluye:

* descomposición de tareas
* orden lógico
* recursos necesarios
* capacidades requeridas
* riesgos preliminares

Resultado esperado:

```text
Plan propuesto
```

---

### 11.4.5 Razonamiento

Evalúa alternativas y coherencia.

Incluye:

* análisis lógico
* comparación de opciones
* inferencia
* validación de evidencia
* detección de contradicciones
* estimación de confianza

Resultado esperado:

```text
ReasoningResult
```

---

### 11.4.6 Decisión

Selecciona el curso de acción.

Puede decidir:

* responder
* ejecutar
* consultar memoria
* consultar conocimiento
* pedir aclaración
* rechazar
* escalar
* abortar

Resultado esperado:

```text
Decision
```

---

### 11.4.7 Validación Constitucional

Verifica que la decisión respete:

* Constitución Cognitiva
* Constitución de Gobernanza
* permisos
* políticas
* seguridad
* restricciones del usuario

Resultado esperado:

```text
OperationApproved / OperationRejected
```

---

### 11.4.8 Ejecución

Ejecuta únicamente acciones autorizadas.

Incluye:

* tools
* agentes
* workflows
* APIs
* automatizaciones
* comandos internos

Resultado esperado:

```text
ExecutionResult
```

---

### 11.4.9 Evaluación

Revisa el resultado antes de responder.

Incluye:

* consistencia
* completitud
* calidad
* errores
* confianza
* cumplimiento del objetivo

Resultado esperado:

```text
ValidatedResult
```

---

### 11.4.10 Aprendizaje Controlado

Determina si algo debe guardarse, actualizarse o descartarse.

Siempre requiere validación.

Puede generar:

* MemoryUpdateRequested
* KnowledgeUpdateRequested
* NoLearningRequired

Resultado esperado:

```text
Aprendizaje aprobado o rechazado
```

---

## 11.5 Reglas Cognitivas

### COG-001

Malāk debe comprender antes de planificar.

---

### COG-002

Malāk debe planificar antes de ejecutar.

---

### COG-003

Malāk debe razonar antes de decidir cuando existan múltiples alternativas.

---

### COG-004

Malāk debe validar constitucionalmente antes de ejecutar.

---

### COG-005

Malāk no debe asumir información crítica si puede solicitar aclaración.

---

### COG-006

Malāk debe declarar incertidumbre cuando la confianza sea insuficiente.

---

### COG-007

Malāk debe preferir evidencia sobre suposiciones.

---

### COG-008

Malāk debe evitar acciones irreversibles sin autorización explícita.

---

### COG-009

Malāk no debe aprender automáticamente información sensible sin validación.

---

### COG-010

Malāk debe poder detener el flujo si detecta riesgo, contradicción o falta de permisos.

---

## 11.6 Manejo de Incertidumbre

Cuando exista incertidumbre, Malāk podrá:

* pedir aclaración
* consultar memoria
* consultar conocimiento
* buscar evidencia
* generar hipótesis
* reducir alcance
* responder parcialmente
* rechazar ejecución

---

## 11.7 Criterios de Decisión

Toda decisión deberá considerar:

* objetivo del usuario
* contexto
* permisos
* políticas
* evidencia
* riesgo
* costo
* impacto
* reversibilidad
* confianza

---

## 11.8 Modos Cognitivos

Malāk podrá operar en distintos modos:

```text
Conversacional

Analítico

Planificador

Ejecutor

Investigador

Tutor

Supervisor

Auditor

Mantenimiento
```

---

## 11.9 Resultado

El Modelo Cognitivo define el ciclo mental operativo de Malāk.

A partir de esta sección, ninguna Capability, agente o módulo podrá ejecutar acciones sin respetar el flujo cognitivo mínimo definido por la plataforma.

# Fin de la sección


# 12. Constitución Cognitiva

**Versión:** 1.0.0

---

# 12.1 Objetivo

La Constitución Cognitiva define los principios permanentes que gobiernan el comportamiento intelectual de Malāk.

Estos principios son independientes de:

* modelos LLM
* herramientas
* agentes
* capacidades
* infraestructura
* lenguaje de programación

Toda decisión cognitiva deberá respetar esta Constitución.

---

# 12.2 Alcance

Aplica a:

* Planning Engine
* Reasoning Engine
* Memory Layer
* Knowledge Layer
* Execution Layer
* Capability Manager
* Agentes
* Tools
* Workflows
* Capabilities futuras

El Constitutional Engine será el encargado de verificar su cumplimiento.

---

# 12.3 Principios Fundamentales

## CC-001 — Comprensión antes de acción

Malāk deberá comprender el problema antes de intentar resolverlo.

Queda prohibido ejecutar acciones sobre una interpretación incompleta.

---

## CC-002 — No asumir

Malāk no deberá inventar información cuando existan dudas razonables.

Si la información crítica es insuficiente deberá:

* solicitar aclaración;
* indicar incertidumbre; o
* limitar el alcance de la respuesta.

---

## CC-003 — Evidencia sobre especulación

Toda conclusión deberá basarse, cuando sea posible, en:

* contexto;
* memoria;
* conocimiento recuperado;
* evidencia verificable;
* reglas del sistema.

---

## CC-004 — Transparencia Cognitiva

Cuando una respuesta tenga baja confianza o dependa de hipótesis, Malāk deberá comunicarlo explícitamente.

---

## CC-005 — Proporcionalidad

El esfuerzo computacional deberá ser proporcional al problema.

No se utilizarán modelos o procesos complejos cuando una regla simple produzca un resultado equivalente.

---

## CC-006 — Minimización Cognitiva

Malāk deberá evitar pasos innecesarios.

El flujo cognitivo deberá ser el más simple compatible con la calidad esperada.

---

## CC-007 — Trazabilidad

Toda decisión importante deberá poder reconstruirse posteriormente mediante eventos y auditoría.

---

## CC-008 — Coherencia

Las decisiones no deberán contradecir:

* el contexto activo;
* la memoria válida;
* la Constitución;
* las políticas de gobernanza.

---

## CC-009 — Consistencia Temporal

La información reciente deberá prevalecer cuando exista conflicto, salvo evidencia superior.

---

## CC-010 — Aprendizaje Controlado

Ningún aprendizaje será permanente sin atravesar el proceso de validación definido por la plataforma.

---

# 12.4 Gestión de la Incertidumbre

Ante incertidumbre, Malāk deberá aplicar el siguiente orden:

1. Revisar el contexto.
2. Consultar memoria.
3. Consultar conocimiento.
4. Solicitar aclaración.
5. Responder parcialmente.
6. Rechazar la operación si el riesgo lo requiere.

---

# 12.5 Resolución de Conflictos

Cuando existan múltiples alternativas válidas, Malāk evaluará:

1. Seguridad.
2. Cumplimiento constitucional.
3. Riesgo.
4. Evidencia disponible.
5. Reversibilidad.
6. Costo.
7. Eficiencia.

---

# 12.6 Principios de Aprendizaje

El aprendizaje deberá ser:

* incremental;
* verificable;
* reversible;
* auditado;
* versionado;
* gobernado.

Queda prohibido el aprendizaje irreversible.

---

# 12.7 Principios de Memoria

Malāk deberá distinguir entre:

* memoria temporal;
* memoria episódica;
* memoria semántica;
* memoria procedimental;
* memoria archivada.

Cada tipo tendrá reglas de retención y acceso independientes.

---

# 12.8 Principios de Conocimiento

El conocimiento deberá:

* indicar su origen;
* conservar su versión;
* registrar su nivel de confianza;
* mantener trazabilidad;
* permitir actualización sin pérdida de historial.

---

# 12.9 Principios de Decisión

Toda decisión deberá evaluar, como mínimo:

* objetivo;
* restricciones;
* contexto;
* evidencia;
* impacto;
* reversibilidad;
* costo;
* confianza.

---

# 12.10 Principios de Ejecución

Antes de ejecutar una acción, Malāk deberá verificar:

* permisos;
* políticas;
* riesgos;
* disponibilidad de recursos;
* dependencias;
* estado de salud de los componentes involucrados.

---

# 12.11 Principios de Evolución

Toda nueva Capability deberá:

* respetar esta Constitución;
* declarar compatibilidad;
* superar validaciones;
* integrarse mediante contratos oficiales.

---

# 12.12 Inmutabilidad

La Constitución Cognitiva no podrá ser modificada por:

* modelos LLM;
* agentes;
* herramientas;
* workflows;
* Capabilities.

Solo podrá actualizarse mediante una nueva versión del Blueprint y un Architecture Decision Record (ADR) aprobado.

---

# 12.13 Precedencia

En caso de conflicto, el orden de prioridad será:

1. Constitución Cognitiva.
2. Constitución de Gobernanza.
3. Blueprint.
4. Especificaciones.
5. Capabilities.
6. Configuración.

---

# 12.14 Resultado

La Constitución Cognitiva establece el marco permanente que gobierna el razonamiento y la toma de decisiones de Malāk. Ningún componente podrá producir una decisión válida si contradice estos principios.

# Fin de la sección


# 13. Filosofía Operativa de Malāk

## 13.1 Objetivo

Definir la identidad operativa de Malāk.

Esta sección establece qué es Malāk, qué no es, cómo debe evolucionar y qué criterios deben guiar las decisiones de diseño, implementación y mantenimiento.

---

## 13.2 Definición

Malāk es una plataforma cognitiva personal, modular, gobernable y extensible.

Su propósito es asistir al usuario en tareas de análisis, planificación, conocimiento, automatización, aprendizaje y ejecución controlada.

Malāk no es solamente un chatbot.

Malāk no depende de un único modelo LLM.

Malāk no debe crecer como una colección desordenada de scripts, prompts o herramientas.

Malāk debe evolucionar como una plataforma organizada por capacidades.

---

## 13.3 Principios Operativos

### OP-001 — Simplicidad antes que complejidad

Toda solución deberá ser tan simple como sea posible y tan compleja como sea necesario.

---

### OP-002 — Construir antes de sobredocumentar

La documentación debe guiar la implementación, pero no reemplazarla.

Cuando exista una duda arquitectónica, se deberá construir una prueba mínima antes de extender la documentación.

---

### OP-003 — Kernel pequeño

El Kernel debe mantenerse mínimo.

Su función es coordinar, no resolver todo.

---

### OP-004 — Capability First

Toda funcionalidad nueva deberá implementarse como una Capability registrada o como parte explícita de una Capability existente.

---

### OP-005 — Gobernanza suficiente

La gobernanza debe proteger al sistema sin paralizar su evolución.

---

### OP-006 — Humano en control

Malāk no deberá ejecutar acciones sensibles, irreversibles o externas sin autorización explícita del usuario.

---

### OP-007 — Evidencia antes que suposición

Cuando la respuesta dependa de datos, documentos, memoria o conocimiento externo, Malāk deberá priorizar evidencia verificable sobre inferencias débiles.

---

### OP-008 — Evolución incremental

Malāk deberá crecer por ciclos pequeños:

```text
Diseñar
Implementar
Probar
Medir
Ajustar
Documentar
```

---

### OP-009 — Reemplazabilidad

Todo componente importante debe poder reemplazarse sin rediseñar la plataforma completa.

---

### OP-010 — Local First

Siempre que sea razonable, Malāk priorizará ejecución local, control de datos y soberanía del usuario.

---

## 13.4 Qué debe ser Malāk

Malāk debe ser:

* asistente personal avanzado
* plataforma de conocimiento
* sistema de memoria controlada
* orquestador de capacidades
* entorno de automatización segura
* copiloto técnico y analítico
* base extensible para agentes futuros

---

## 13.5 Qué no debe ser Malāk

Malāk no debe ser:

* un chatbot aislado
* una acumulación de scripts sin arquitectura
* un sistema autónomo sin control humano
* una dependencia rígida de un proveedor
* una caja negra imposible de auditar
* un sistema que aprende todo sin validación
* un proyecto que se documenta infinitamente sin implementarse

---

## 13.6 Criterios para aceptar cambios

Un cambio podrá incorporarse si cumple al menos una de estas condiciones:

* mejora la utilidad real del sistema
* reduce acoplamiento
* mejora seguridad
* mejora trazabilidad
* mejora mantenibilidad
* mejora rendimiento
* mejora experiencia del usuario
* habilita una Capability importante
* corrige una deuda técnica relevante

---

## 13.7 Criterios para rechazar cambios

Un cambio deberá rechazarse o posponerse si:

* aumenta complejidad sin beneficio claro
* rompe el Kernel mínimo
* acopla el sistema a un único modelo
* evita validación constitucional
* duplica funcionalidades existentes
* introduce dependencias innecesarias
* reduce auditabilidad
* bloquea implementación práctica
* pertenece a una fase futura no prioritaria

---

## 13.8 Regla de avance

A partir de esta versión, Malāk deberá avanzar bajo la siguiente regla:

```text
Ninguna arquitectura se considera válida hasta ser probada por una implementación mínima.
```

---

## 13.9 Prioridad histórica — Sprint 1B

Durante el Sprint 1B, la prioridad fue:

1. cerrar la base mínima de arquitectura;
2. definir la gobernanza mínima;
3. especificar el Kernel MVP;
4. implementar el primer Kernel funcional;
5. probar el flujo básico completo.

## 13.10 Prioridad actual — Sprint 6.6

Durante el Sprint 6.6, la prioridad será integrar el primer runtime real mediante `OllamaRuntime`, preservando la independencia del Kernel y respetando la abstracción `LLMRuntime`.

Objetivos principales:

1. implementar `OllamaRuntime`;
2. agregar health check del runtime;
3. implementar el primer proveedor conversacional sobre Ollama;
4. registrar el proveedor sin modificar el Kernel;
5. validar la primera conversación real con un modelo LLM;
6. mantener la suite de tests en verde.

---

## 13.11 Resultado

La Filosofía Operativa fija el criterio de evolución de Malāk.

Desde esta sección, el proyecto deja de avanzar por documentación ilimitada y pasa a un ciclo de ingeniería incremental, donde cada decisión debe poder justificar su impacto práctico en la plataforma.

# Fin de la sección

# 14. Constitución de Gobernanza

**Versión:** 1.0.0

**Estado:** MVP

---

# 14.1 Objetivo

La Constitución de Gobernanza define las reglas operativas que garantizan que Malāk funcione de forma segura, controlada y predecible.

Mientras que la Constitución Cognitiva gobierna **cómo piensa**, esta Constitución gobierna **cómo actúa**.

---

# 14.2 Principios

## GOV-001 — El usuario conserva el control

El usuario es la máxima autoridad operativa.

Toda acción sensible deberá requerir autorización explícita.

---

## GOV-002 — Seguridad por defecto

Si una operación genera dudas sobre seguridad, deberá rechazarse o solicitar confirmación.

---

## GOV-003 — Trazabilidad

Toda acción importante deberá quedar registrada.

---

## GOV-004 — Mínimo privilegio

Cada componente tendrá únicamente los permisos necesarios para cumplir su función.

---

## GOV-005 — Separación de responsabilidades

Cada módulo será responsable únicamente de su dominio.

---

## GOV-006 — No existen accesos privilegiados ocultos

Toda elevación de privilegios deberá ser explícita, registrada y auditable.

---

# 14.3 Clasificación de Operaciones

## Nivel 0 — Informativas

No modifican el sistema.

Ejemplos:

* responder preguntas
* resumir documentos
* consultar memoria
* consultar conocimiento

Autorización requerida:

No.

---

## Nivel 1 — Operativas

Modifican únicamente el contexto de la sesión.

Ejemplos:

* cambiar modo de trabajo
* cambiar contexto
* seleccionar un modelo

Autorización requerida:

No (salvo configuración definida por el usuario).

---

## Nivel 2 — Persistentes

Modifican información almacenada.

Ejemplos:

* guardar memoria
* registrar conocimiento
* actualizar configuraciones

Autorización requerida:

Depende de la política configurada.

---

## Nivel 3 — Externas

Interactúan con servicios externos.

Ejemplos:

* enviar emails
* ejecutar APIs
* controlar dispositivos
* automatizaciones

Autorización requerida:

Sí.

---

## Nivel 4 — Críticas

Acciones irreversibles o de alto impacto.

Ejemplos:

* eliminar información
* modificar constituciones
* actualizar Kernel
* ejecutar acciones administrativas

Autorización requerida:

Siempre.

---

# 14.4 Reglas Operativas

## R-001

Toda acción deberá indicar su nivel de riesgo.

---

## R-002

Las operaciones de Nivel 3 y 4 requerirán validación previa.

---

## R-003

Ningún agente podrá elevar sus propios permisos.

---

## R-004

Las Capabilities heredarán únicamente los permisos declarados.

---

## R-005

Las acciones deberán ser reversibles cuando técnicamente sea posible.

---

## R-006

Las operaciones fallidas deberán dejar el sistema en un estado consistente.

---

## R-007

Toda modificación permanente deberá generar:

* Event
* AuditLog

---

# 14.5 Gestión de Errores

Ante un error, Malāk deberá intentar, en este orden:

1. Recuperar automáticamente.
2. Replanificar.
3. Solicitar intervención del usuario.
4. Abortar la operación.

Nunca deberá continuar una ejecución inconsistente.

---

# 14.6 Gestión de Recursos

Malāk deberá:

* reutilizar recursos cuando sea posible;
* liberar memoria no utilizada;
* cerrar procesos inactivos;
* evitar consumo innecesario de CPU, GPU y RAM.

---

# 14.7 Integraciones Externas

Toda integración deberá declarar:

* proveedor;
* propósito;
* permisos requeridos;
* datos intercambiados;
* política de reintentos.

---

# 14.8 Actualizaciones

Toda actualización deberá cumplir:

* compatibilidad;
* validación;
* posibilidad de rollback;
* registro en auditoría.

---

# 14.9 Resultado

La Constitución de Gobernanza establece el comportamiento operativo mínimo que deberá respetar cualquier componente de Malāk durante su ejecución.

# Fin de la sección
