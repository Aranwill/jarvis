---
id: ADR-003
title: Directional Communication and Authority Flow
status: accepted
date: 2026-08-15
author: Hector Rodriguez
reviewed_by:
  - ChatGPT
version: 0.6.0-alpha

tags:
  - architecture
  - communication
  - authority
  - dependency
  - event-model
  - zero-trust

related:
  - DOC-ARQ-BLUEPRINT
  - ADR-002
  - DOC-ADR-INDEX-001

affects:
  - Architecture
  - Kernel
  - Event Bus
  - Capabilities
  - Agents
  - Governance
  - Security
  - Infrastructure

depends_on:
  - Cognitive Constitution
  - Governance Constitution
  - Blueprint

supersedes: null
superseded_by: null

graph:
  node_type: ArchitectureDecision
  priority: High
---

# ADR-003 — Directional Communication and Authority Flow

## Estado

Accepted

---

## Contexto

El Blueprint de Malāk ya define un flujo general descendente desde el usuario, pasando por las capas de identidad, contexto, gobernanza, validación constitucional y Kernel, hasta las capas cognitivas, de conocimiento y ejecución.

También establece que:

- las dependencias circulares están prohibidas;
- toda comunicación entre módulos se realiza mediante contratos públicos;
- las capas superiores pueden solicitar servicios a capas inferiores mediante contratos;
- los eventos constituyen el mecanismo oficial de comunicación desacoplada.

Sin embargo, algunas secciones históricas del Blueprint utilizan la expresión **Dependencias permitidas** para describir relaciones entre componentes, incluyendo relaciones donde una capa inferior puede necesitar políticas, validación, infraestructura o información administrada por otra capa.

Además, el flujo maestro representa el retorno `Execution Layer → Kernel → Interface Layer`.

Sin una regla explícita, estas relaciones podrían interpretarse erróneamente como autorización para:

- iniciar control desde una capa inferior hacia una superior;
- crear dependencias de control ascendentes;
- usar eventos de retorno como órdenes;
- confundir el retorno de resultados con transferencia de autoridad.

Esta ADR formaliza la semántica direccional sin eliminar la capacidad de devolver resultados, eventos, errores, métricas o evidencia.

---

## Decisión

Malāk adopta las siguientes reglas obligatorias de comunicación interna.

### Términos operativos

**Upstream:** componente que posee u origina control o autoridad para una interacción determinada.

**Downstream:** componente que recibe trabajo delegado dentro de esa interacción.

Estos términos describen la relación de autoridad para una interacción concreta y no necesariamente una posición física fija dentro de la arquitectura.

Un mismo componente puede ser downstream respecto de un orquestador y upstream respecto de un worker o subagente, sin alterar las reglas de autoridad.

### 1. Control y autoridad descendentes

El flujo de:

- control;
- autoridad;
- solicitudes operativas;
- delegación de trabajo;
- permisos;
- políticas aplicables;

se origina en componentes con autoridad upstream y se dirige hacia componentes downstream mediante contratos públicos, requests o comandos tipados, brokers u otros mecanismos de orquestación autorizados.

### 2. Prohibición de control ascendente

Un componente downstream no puede iniciar una invocación de control hacia un componente upstream con el propósito de:

- ordenarle trabajo;
- modificar su estado de autoridad;
- concederse permisos;
- elevar privilegios;
- modificar políticas;
- alterar Gobernanza;
- modificar Constitución;
- modificar Kernel;
- ampliar el alcance de una operación.

### 3. Resultados y evidencia pueden regresar hacia arriba

Los componentes downstream pueden devolver o emitir:

- resultados;
- errores;
- estados;
- health status;
- métricas;
- findings;
- eventos;
- evidencia;
- receipts cuando existan;

hacia el componente que originó el trabajo o hacia consumidores autorizados.

Este retorno constituye **información**, no autoridad.

### 4. El receptor superior decide

Cuando un componente upstream recibe un resultado, evento o evidencia desde un componente downstream, corresponde al componente upstream decidir qué acción posterior realizar dentro de su propia autoridad.

El componente downstream no controla esa decisión.

### 5. Eventos no equivalen a órdenes ascendentes

Los eventos representan hechos ocurridos.

Un evento ascendente puede informar:

```text
ExecutionCompleted
ValidationFailed
HealthCheckFailed
FindingDetected
```

pero no puede utilizarse como una orden encubierta equivalente a:

```text
KernelDoThis
GovernanceGrantPermission
ConstitutionApproveMe
OwnerAuthorizeThis
```

### 6. Las "Dependencias permitidas" no invierten el control

Las listas históricas de **Dependencias permitidas** del Blueprint deben interpretarse como relaciones contractuales o servicios autorizados.

No constituyen autorización para invertir el flujo de control.

Cuando un componente downstream requiera información o validación administrada por un componente upstream, debe utilizar el mecanismo arquitectónico previsto —contrato, request o comando tipado, broker, policy service u orquestación— sin adquirir autoridad sobre ese componente.

Los eventos pueden propagar hechos, resultados o evidencia derivados de esa interacción, pero no constituyen por sí mismos una solicitud de control ni una transferencia de autoridad.

### 7. Prohibición de ciclos

Se prohíben:

- ciclos de control;
- ciclos de autoridad;
- ciclos de autorización;
- dependencias operativas circulares;
- bypass de capas.

La existencia de un canal de retorno de resultados no constituye por sí misma una dependencia circular.

---

## Modelo resumido

```text
CONTROL / AUTHORITY / REQUESTS

Upstream
   │
   ▼
Downstream


RESULTS / EVENTS / EVIDENCE

Upstream
   ▲
   │
Downstream
```

La flecha ascendente representa retorno de información.

No representa autoridad inversa.

---

## Alternativas consideradas

### Alternativa A — Prohibir toda comunicación ascendente

Rechazada.

Impediría devolver resultados, errores, métricas, evidencia y eventos necesarios para la orquestación y observabilidad.

### Alternativa B — Permitir comunicación bidireccional sin distinguir semántica

Rechazada.

Facilitaría acoplamiento, ciclos de dependencia, bypass de autoridad y ambigüedad sobre quién controla el flujo.

### Alternativa C — Control descendente y evidencia ascendente

Aceptada.

Mantiene la jerarquía arquitectónica y de autoridad sin impedir resultados, observabilidad, auditoría ni Event Bus.

---

## Consecuencias

### Positivas

- preserva la jerarquía arquitectónica;
- evita que componentes downstream controlen componentes upstream;
- reduce dependencias circulares;
- mejora Zero Trust interno;
- fortalece separación de responsabilidades;
- permite resultados y evidencia ascendentes sin transferir autoridad;
- clarifica la semántica del Event Bus;
- facilita futuros agentes y subagentes gobernados;
- reduce riesgo de bypass del Security Control Plane;
- hace más verificables las revisiones SDD/TDD/4R y futuros receipts.

### Negativas

- algunos flujos futuros requerirán brokers, contratos o eventos en lugar de llamadas directas;
- puede requerir refactor si se detectan implementaciones históricas con invocación ascendente directa;
- exige distinguir explícitamente entre command/request y result/event.

### Riesgos

- interpretar "dependencia permitida" como permiso de invocación directa;
- diseñar eventos que contengan órdenes encubiertas;
- introducir callbacks con autoridad implícita;
- confundir observabilidad con capacidad de control.

Estos riesgos deben mitigarse mediante contratos públicos, Architecture Quality Gates, revisión 4R y tests de arquitectura cuando corresponda.

---

## Impacto arquitectónico

La decisión afecta la interpretación y evolución de:

- Blueprint;
- Kernel;
- Event Bus;
- Capability Manager;
- Planning Engine;
- Reasoning Engine;
- Memory Layer;
- Knowledge Layer;
- Execution Layer;
- Infrastructure Layer;
- agentes y subagentes futuros;
- Security Control Plane;
- contratos públicos.

Esta ADR no modifica responsabilidades del Kernel ni introduce lógica de negocio.

No requiere modificación inmediata de código mientras la implementación vigente respete la regla.

---

## Relación con Gobernanza

La decisión refuerza:

- Human in Control;
- Zero Trust;
- mínimo privilegio;
- separación de responsabilidades;
- trazabilidad;
- ausencia de accesos privilegiados ocultos;
- prohibición de autoelevación de agentes.

La regla puede resumirse como:

> La autoridad fluye de upstream hacia downstream; los resultados y la evidencia pueden propagarse de downstream hacia upstream.

Un componente downstream nunca puede transformar evidencia en autoridad por cuenta propia.

---

## Compatibilidad con AKS / GraphRAG

La ADR puede representarse como un nodo `ArchitectureDecision` relacionado con:

- Blueprint;
- Kernel;
- Event Model;
- Governance;
- Security;
- Capabilities;
- Agents.

Relaciones sugeridas:

```text
ADR-003
  affects -> Kernel
  affects -> Event Bus
  affects -> Capabilities
  affects -> Agents
  constrains -> Internal Communication
  reinforces -> Zero Trust
  reinforces -> Separation of Responsibilities
  depends_on -> Blueprint
  depends_on -> Governance Constitution
  depends_on -> Cognitive Constitution
```

---

## Criterio de aceptación

- [x] Decisión documentada.
- [x] Metadatos completos.
- [x] Relaciones explícitas.
- [x] Impacto identificado.
- [x] Compatible con Knowledge Model.
- [x] Control y autoridad descendentes definidos.
- [x] Términos upstream/downstream definidos.
- [x] Retorno ascendente de resultados y evidencia definido.
- [x] Invocación ascendente de control prohibida.
- [x] Semántica de eventos ascendentes aclarada.
- [x] Dependencias históricas interpretadas sin inversión de autoridad.
- [x] No introduce cambios en Kernel ni runtime.
