---
title: Governed Swarm and Long-Horizon Reference
status: concept
authority: non_normative
document_role: conceptual_reference
language: es
created: 2026-08-14
related:
  - documents/projects/jarvis/ideas.md
  - IDEA-024
purpose: >
  Preservar la evaluación y el mapeo conceptual del anexo sobre enjambre
  gobernado, continuidad de tareas y trabajo de horizonte largo sin crear
  una segunda fuente de autoridad ni autorizar implementación inmediata.
---

# Governed Swarm and Long-Horizon Reference

## 1. Propósito

Este documento registra la incorporación conceptual del material estudiado bajo
el tema:

> **Enjambre Gobernado y Trabajo de Horizonte Largo**

Su función es preservar las conclusiones de diseño que resultaron compatibles
con la arquitectura de Malāk sin duplicar íntegramente el documento de trabajo
original.

Este documento:

- no modifica el baseline;
- no autoriza un sprint;
- no autoriza agentes;
- no crea Mission Controller;
- no crea Execution Graph;
- no introduce Task State;
- no implementa Cognitive Core;
- no modifica Gobernanza;
- no reemplaza `ideas.md`;
- no reemplaza IDEA-024.

La fuente oficial para las iniciativas conceptuales continúa siendo la
documentación vigente del repositorio.

---

## 2. Relación con IDEA-024

La mayor parte del diseño de agentes especializados y orquestación gobernada
queda representada actualmente por:

```text
IDEA-024
Governed Agent Composition & Mission Orchestration Foundation
```

IDEA-024 ya preserva, entre otros conceptos:

- agentes temporales y especializados;
- separación entre competencia y autoridad;
- composición gobernada;
- Mission Orchestration;
- contratos de tarea, output y completion;
- comunicación estructurada;
- deliberación limitada;
- Builder / Reviewer Separation;
- Artifact Workspace;
- repair loops acotados;
- Security Control Plane como autoridad externa;
- Resource Governance;
- Human in Control;
- prohibición de autoelevación;
- prohibición de modificación autónoma de políticas;
- restricción explícita contra sobreingeniería.

Por lo tanto, este documento no crea una iniciativa paralela de Agent Swarm.

---

## 3. Principio central de orquestación

Se preserva el principio:

> **Malāk dirige el enjambre; el enjambre no gobierna Malāk.**

Los agentes futuros deberán ser:

- temporales por defecto;
- especializados;
- limitados por scope;
- gobernados mediante identidad y políticas;
- observables;
- auditables;
- reemplazables;
- incapaces de concederse autoridad.

La existencia de una competencia, profesión, skill o modelo no constituye
permiso operacional.

---

## 4. Preferencia por simplicidad

Antes de recurrir a múltiples agentes deberá evaluarse:

```text
deterministic procedure
        >
single capability
        >
single specialized agent
        >
multi-agent composition
```

cuando las opciones anteriores produzcan calidad equivalente.

La coordinación multiagente solo deberá aparecer cuando exista necesidad real
demostrada por una tarea.

No deberá existir una flota permanente únicamente porque la infraestructura
pueda soportarla.

---

## 5. Dynamic Execution Graph

Se preserva como concepto futuro la posibilidad de representar misiones
complejas mediante un grafo de ejecución.

Un futuro Execution Graph podría modelar:

- tareas;
- dependencias;
- estados;
- agentes asignados;
- artefactos;
- validaciones;
- bloqueos;
- criterios de finalización.

Sin embargo:

```text
Execution Graph
!=
current implementation requirement
```

No deberá crearse hasta que tareas reales demuestren que una secuencia lineal
o un workflow simple resultan insuficientes.

---

## 6. Completion Contracts

Se considera especialmente valioso preservar el concepto de
**Completion Contract**.

Principio:

> **Una tarea no termina porque un agente diga que terminó. Termina cuando los
> criterios de finalización pueden demostrarse mediante evidencia.**

Un futuro contrato podrá expresar:

```text
objective
scope
required_outputs
acceptance_criteria
required_evidence
allowed_tools
resource_limits
failure_conditions
stop_conditions
```

Los Completion Contracts deberán apoyarse en mecanismos de evidencia y
validación existentes, evitando crear una autoridad paralela.

---

## 7. Agent Leases

El concepto de permisos temporales para agentes deberá integrarse, si llega a
ser necesario, con la futura evolución de:

```text
Secure Context Manager
+
Identity & Trust Framework
+
Security Control Plane
```

No se recomienda crear actualmente un sistema separado denominado
`Agent Lease Manager`.

La necesidad deberá resolverse mediante los mecanismos generales de contexto,
identidad, TTL, capability scopes y autorización.

---

## 8. Long-Horizon Task State

Las tareas de horizonte largo necesitarán eventualmente persistencia externa al
contexto del modelo.

Principio:

> **La continuidad pertenece al sistema, no a la ventana de contexto de un
> modelo.**

Un futuro Persistent Task State podrá conservar, según necesidad:

- task identity;
- objetivo;
- estado;
- dependencias;
- checkpoints;
- outputs;
- evidencia;
- side effects;
- blockers;
- siguiente acción segura;
- owner decisions pendientes.

El contexto LLM no deberá convertirse en la fuente primaria de estado de una
misión larga.

---

## 9. Checkpoints y recuperación

Las tareas largas deberán poder:

```text
start
  ↓
execute
  ↓
checkpoint
  ↓
interrupt
  ↓
recover
  ↓
validate
  ↓
resume
```

Antes de repetir una operación después de una interrupción deberá verificarse
si existieron side effects.

Cuando sea viable, las operaciones deberán diseñarse para ser:

- idempotentes;
- recuperables;
- verificables;
- acotadas.

---

## 10. Execution Ledger

Se conserva como concepto futuro un registro estructurado de ejecución cuando
Malāk posea misiones suficientemente complejas.

Su propósito podría ser reconstruir:

- qué ocurrió;
- en qué orden;
- quién produjo cada resultado;
- qué evidencia se generó;
- qué decisiones fueron tomadas;
- qué errores aparecieron;
- qué operaciones tuvieron side effects.

No deberá utilizarse como un nuevo envelope universal de observabilidad.

Deberá mantenerse separado de:

```text
Runtime Metrics
Operational Events
Security Audit
```

salvo relaciones explícitas mediante identificadores.

---

## 11. Shared Task Board

El concepto de Shared Task Board se considera potencialmente útil como
**proyección o interfaz de Task State**, no necesariamente como un subsistema
independiente.

No deberá introducirse una nueva fuente de verdad si el futuro Persistent Task
State puede ofrecer la información requerida.

Principio:

> **Preferir vistas derivadas antes que duplicar estado.**

---

## 12. Graph Health Monitor

Un monitor específico del Execution Graph se considera prematuro.

Antes de implementarlo deberá existir:

- un Execution Graph real;
- fallos observados;
- métricas suficientes;
- necesidad operacional demostrada.

Las funciones útiles deberán extraerse solo cuando la evidencia justifique una
responsabilidad independiente.

---

## 13. Cognitive Core

El concepto de Cognitive Core se considera compatible con la visión futura de
Malāk como identidad cognitiva persistente.

El Cognitive Core podría llegar a actuar como:

- interlocutor principal;
- integrador de especialistas;
- mantenedor de coherencia cognitiva;
- consumidor de Memory, Self Model y Knowledge;
- sintetizador de resultados.

Sin embargo:

```text
Cognitive Core
!=
authority
```

La seguridad, autorización, gobernanza y políticas deberán permanecer fuera de
él y ser deterministas.

No se autoriza su implementación por este documento.

---

## 14. Architecture & Knowledge Steward

Se considera una evolución coherente de:

```text
Project Vault
+
AKS
+
Architecture Auditor
+
Knowledge Governance
```

No se recomienda implementar múltiples subsistemas nuevos para cubrir
responsabilidades ya existentes.

El futuro Steward podrá:

- detectar contradicciones;
- localizar conocimiento obsoleto;
- relacionar decisiones;
- identificar gaps documentales;
- preparar propuestas;
- ayudar a mantener provenance.

No podrá modificar automáticamente fuentes de autoridad.

---

## 15. Engineering Intelligence

Engineering Intelligence deberá emerger de capacidades existentes y futuras,
en lugar de implementarse como un mega-componente.

Podrá combinar:

```text
Cognitive Core
Project Vault
AKS
Telemetry
Sandbox
Independent Validation
Specialist capabilities
```

para:

- autoobservar el sistema;
- detectar oportunidades;
- investigar alternativas;
- producir propuestas;
- construir experimentos aislados;
- evaluar resultados.

Nunca podrá:

- aprobar su propia evolución;
- mergear cambios;
- desplegar;
- modificar el baseline por autoridad propia.

Principio:

> **La autoobservación produce conocimiento; el conocimiento produce
> propuestas; solo la gobernanza produce cambios.**

---

## 16. Digital Twin

La idea de un Digital Twin completo de Malāk se conserva únicamente como:

```text
OBSERVE
```

Existe alto riesgo de sobreingeniería si se intenta construir como plataforma
separada.

Antes de crear un Digital Twin deberán evaluarse primero proyecciones derivadas
de:

```text
Repository
+
AKS
+
Vault
+
Runtime evidence
```

Si esas proyecciones resultan suficientes, no deberá existir un subsistema
adicional.

---

## 17. Cognitive Reference Library

Una biblioteca cognitiva o de ingeniería puede ser útil como conjunto de
Knowledge Artifacts reutilizables.

Deberá vivir en el plano de conocimiento, no como runtime obligatorio.

Podrá incluir:

- patrones;
- anti-patterns;
- decisiones comentadas;
- failure cases;
- architecture cases;
- security cases;
- engineering recipes;
- ejemplos de reasoning esperado.

Su evolución deberá mantenerse compatible con AKS y futura recuperación
estructurada.

---

## 18. Separaciones obligatorias

Se preserva explícitamente:

```text
Context
!=
Task State
!=
Memory
!=
Knowledge
!=
Evidence
```

Cada concepto responde a una responsabilidad distinta.

No deberán fusionarse únicamente por conveniencia de implementación.

---

## 19. Límites contra sobreingeniería

No se autoriza por este documento:

- Agent Swarm;
- Mission Controller;
- Agent Factory;
- agentes permanentes;
- Execution Graph;
- Graph Health Monitor;
- Task Board independiente;
- Execution Ledger universal;
- Cognitive Core;
- Digital Twin;
- Engineering Intelligence runtime;
- recursión ilimitada;
- deliberación multiagente por defecto;
- Context como estado primario;
- retries infinitos;
- creación libre de agentes;
- modificación de políticas;
- modificación de documentos fundacionales;
- GraphRAG;
- acceso libre a Internet.

Todo componente futuro deberá demostrar necesidad operacional.

---

## 20. Dependencias antes de agentic orchestration

Antes de implementar composición multiagente deberán existir suficiente madurez
y evidencia en:

```text
Security Control Plane
Secure Context / Identity
Sandbox
Evidence
Resource Governance
Model Governance
AKS / Knowledge Governance
Independent Validation
Operational Metrics
basic capability contracts
execution contracts
```

El orden exacto deberá determinarse a partir del baseline vigente cuando llegue
el momento.

---

## 21. Relación con el futuro E2E

El primer objetivo operacional continúa siendo construir y medir un vertical
slice E2E simple.

La secuencia preferida es:

```text
single governed E2E
        ↓
real evidence
        ↓
measurement
        ↓
identify limitations
        ↓
introduce only necessary complexity
```

No:

```text
design full swarm
        ↓
build infrastructure
        ↓
look for problems to justify it
```

---

## 22. Estado

```text
Documento: referencia conceptual
Autoridad: no normativa
Implementación: no iniciada
Sprint autorizado: ninguno
Baseline modificado: no
```

Este documento deberá volver a evaluarse contra el repositorio, Blueprint,
Constitución Cognitiva y Gobernanza antes de derivar de él cualquier diseño
operativo.
