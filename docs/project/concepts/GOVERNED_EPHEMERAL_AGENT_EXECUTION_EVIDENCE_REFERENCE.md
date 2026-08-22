---
title: Governed Ephemeral Agent Execution, Evidence and Candidate Evaluation Reference
status: concept
authority: non_normative
document_role: conceptual_reference
language: es
created: 2026-08-22
related:
  - documents/projects/jarvis/ideas.md
  - docs/project/concepts/GOVERNED_SWARM_LONG_HORIZON_REFERENCE.md
  - IDEA-001
  - IDEA-003
  - IDEA-020
  - IDEA-024
purpose: >
  Preservar la referencia conceptual para ejecución efímera y aislada de agentes,
  minimización de contexto, observación externa, evidencia verificable,
  liberación de recursos y evaluación gobernada de candidatos sin crear una
  nueva fuente de autoridad ni autorizar implementación.
---

# Governed Ephemeral Agent Execution, Evidence and Candidate Evaluation Reference

## 1. Propósito

Este documento preserva y consolida el diseño conceptual relacionado con la ejecución futura de agentes temporales dentro de entornos aislados y descartables.

Su objetivo es evitar que esta línea de diseño vuelva a quedar distribuida entre conversaciones o resumida de forma que se pierdan sus restricciones esenciales.

Este documento:

- no modifica el baseline;
- no aprueba arquitectura;
- no autoriza un sprint;
- no autoriza agentes;
- no implementa sandbox;
- no implementa scoring;
- no crea un sistema multiagente;
- no modifica Gobernanza;
- no modifica el Security Control Plane;
- no modifica el Kernel;
- no reemplaza `ideas.md`;
- no reemplaza `GOVERNED_SWARM_LONG_HORIZON_REFERENCE.md`.

Su contenido deberá volver a evaluarse contra el baseline y las fuentes de mayor autoridad antes de derivar cualquier implementación.

---

## 2. Relación con las iniciativas existentes

Esta referencia no crea una iniciativa nueva.

Preserva una intersección de responsabilidades ya distribuidas entre:

```text
IDEA-001
Sandbox Containment & Evaluation Evidence Foundation
        ↓
contención, observabilidad y evidencia externa

IDEA-003
Resource Governance Foundation
        ↓
presupuestos, carga y liberación de recursos

IDEA-020
Sovereign Agent Fleet Control & Vertical Scaling
        ↓
visión futura de agentes y escalado gobernado

IDEA-024
Governed Agent Composition & Mission Orchestration Foundation
        ↓
composición y coordinación gobernada de misiones
```

Este documento conserva específicamente:

```text
agent execution
+
containment
+
least context
+
external evidence
+
resource lifecycle
+
candidate validation
+
candidate comparison
```

No absorbe ni sustituye ninguna de las iniciativas anteriores.

---

## 3. Frontera con Governed Swarm

La referencia `GOVERNED_SWARM_LONG_HORIZON_REFERENCE.md` responde principalmente a:

> ¿Cómo puede Malāk coordinar agentes, misiones, artefactos y trabajo de horizonte largo?

Este documento responde principalmente a:

> ¿Cómo debe ejecutarse, limitarse, observarse, finalizarse y evaluarse una ejecución agentic concreta?

Separación conceptual:

```text
Governed Swarm
    ↓
orchestration / missions / long-horizon work

Ephemeral Agent Execution
    ↓
sandbox / context / evidence / lifecycle / candidate evaluation
```

---

## 4. Principios rectores

> **El agente puede producir un resultado, pero no puede ser la única fuente autoritativa de evidencia sobre su propia ejecución.**

> **La evidencia puede justificar una propuesta; no concede autoridad.**

> **Un score puede ayudar a comparar candidatos válidos; no establece verdad, seguridad ni permiso.**

> **Least Privilege debe complementarse con Least Context.**

> **La inteligencia puede proponer. La autoridad decide.**

---

## 5. Arquitectura conceptual

```text
                         TASK / GOAL
                             │
                             ▼
                   Governed Orchestration
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
     Sandbox A          Sandbox B          Sandbox C
     ephemeral          ephemeral          ephemeral
          │                  │                  │
       Agent A            Agent B            Agent C
          │                  │                  │
     Candidate A        Candidate B        Candidate C
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                             ▼
                  External Evidence Plane
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        Architecture      Security       Empirical
         Validation       Validation      Validation
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                    Candidate Validity
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
            VALID         INVALID      INCONCLUSIVE
              │
              ▼
                     Score / Ranking
                             │
                             ▼
                       Proposal
                             │
                             ▼
                    Human Governance
```

Este diagrama es conceptual. No define componentes, contratos, clases, APIs ni procesos aprobados.

---

## 6. Sandbox efímero

Una futura ejecución agentic deberá considerar aislamiento por defecto.

Propiedades candidatas:

- entorno descartable;
- aislamiento del Kernel y del Cognitive Core;
- filesystem limitado;
- red denegada por defecto;
- herramientas allowlisted;
- procesos limitados;
- límites de CPU;
- límites de RAM;
- límites de VRAM;
- límites de almacenamiento;
- timeout;
- kill switch;
- cuarentena;
- snapshots cuando sean necesarios;
- destrucción o cierre seguro al finalizar.

El sandbox no deberá considerarse una frontera de confianza absoluta.

```text
Sandbox != Trust
```

La ejecución seguirá subordinada a Zero Trust y Defense in Depth.

---

## 7. Least Context

Cada agente deberá recibir solamente la información necesaria para la tarea autorizada.

```text
Least Privilege
→ mínimo permiso necesario

Least Context
→ mínimo conocimiento necesario
```

Un agente podría recibir:

```text
task
specification
required files
applicable rules
allowed tools
resource budget
acceptance criteria
temporary security context
```

No deberá recibir por defecto:

```text
complete Memory
complete Project Vault
all conversations
unrestricted filesystem
all tools
all secrets
unrelated credentials
unrestricted Internet
```

Least Context busca reducir:

- exposición de información;
- superficie de ataque;
- consumo de contexto;
- propagación innecesaria de secretos;
- contaminación cognitiva;
- impacto de una ejecución comprometida;
- consumo de RAM y VRAM.

---

## 8. Observación externa

La evidencia canónica de una ejecución no deberá depender exclusivamente del agente que está siendo evaluado.

Una futura frontera de observación externa podrá recopilar, según riesgo y necesidad:

- comandos ejecutados;
- herramientas utilizadas;
- procesos creados;
- accesos a archivos;
- conexiones de red;
- duración;
- errores;
- outputs;
- cambios de filesystem;
- hashes;
- intentos denegados;
- consumo de CPU;
- consumo de RAM;
- consumo de VRAM;
- violaciones de políticas;
- eventos de timeout;
- terminación forzada.

> **Lo que un agente afirma haber hecho no sustituye la evidencia externa de lo que realmente ocurrió.**

---

## 9. Candidate Evidence Package

Cada resultado agentic relevante podrá generar un paquete estructurado de evidencia.

```text
Candidate
├── identity
├── task
├── model/runtime
├── sandbox
├── context manifest
├── allowed tools
├── execution evidence
├── resource evidence
├── tests
├── architecture findings
├── security findings
├── empirical results
├── artifacts
└── final status
```

El paquete deberá permitir reconstruir una ejecución sin depender de una explicación narrativa del propio agente.

No se aprueba en este documento ningún esquema concreto.

---

## 10. Lifecycle efímero

```text
CREATE
  ↓
ASSIGN MINIMUM CONTEXT
  ↓
ISSUE TEMPORARY AUTHORITY
  ↓
LOAD REQUIRED MODEL
  ↓
EXECUTE
  ↓
COLLECT EXTERNAL EVIDENCE
  ↓
VALIDATE
  ↓
REVOKE CONTEXT / TOKENS
  ↓
UNLOAD MODEL
  ↓
RELEASE RESOURCES
  ↓
DESTROY OR QUARANTINE SANDBOX
  ↓
RETAIN AUTHORIZED EVIDENCE
```

La terminación de una tarea deberá producir una liberación explícita y verificable de recursos cuando no exista una razón aprobada para mantenerlos.

La política definitiva de unload deberá pertenecer a Resource Governance y Model Governance, no a este documento.

---

## 11. Generación independiente de candidatos

Cuando exista evidencia de que múltiples alternativas aportan valor, una misión podrá producir candidatos independientes.

```text
Task
 ├── Agent A → Candidate A
 ├── Agent B → Candidate B
 └── Agent C → Candidate C
```

La independencia puede utilizar modelos, estrategias, roles, hipótesis o aproximaciones distintas.

La deliberación multiagente no deberá ser la opción por defecto.

```text
deterministic procedure
        >
single capability
        >
single specialized agent
        >
multi-agent composition
```

---

## 12. Validación antes del ranking

Los candidatos no deberán entrar directamente en un sistema de puntuación.

```text
Candidate
   ↓
Law / Policy Validation
   ↓
Architecture Validation
   ↓
Security Validation
   ↓
Specification Validation
   ↓
Empirical Validation
   ↓
Evidence Sufficiency
   ↓
VALID / INVALID / INCONCLUSIVE
```

Reglas conceptuales:

```text
Hard law violation
→ INVALID

Security FAIL
→ INVALID

Insufficient evidence
→ INCONCLUSIVE

Tests PASS
→ evidence, not absolute proof

High score
→ cannot convert INVALID into VALID
```

Solo candidatos `VALID` podrán ser comparados mediante ranking.

---

## 13. Score y ranking

```text
Score != Truth
Score != Safety
Score != Evidence
Score != Authority
Score != Governance
```

Una evaluación futura podría considerar cumplimiento de specification, resultados empíricos, tests, rendimiento, recursos, mantenibilidad, simplicidad, reversibilidad, findings, arquitectura, seguridad y costo operacional.

No se aprueba ninguna fórmula de puntuación en este documento.

Una violación crítica no podrá compensarse mediante una puntuación numérica.

---

## 14. Counter-evidence y refutación

Según el riesgo, una evaluación podrá intentar:

- encontrar contraejemplos;
- romper invariantes;
- ejecutar casos adversariales;
- localizar contradicciones;
- comparar alternativas;
- detectar supuestos ocultos;
- reproducir findings;
- declarar incertidumbre residual.

```text
Candidate
   ↓
support evidence
+
counter-evidence
+
independent review
   ↓
evaluation
```

---

## 15. Separación de roles

```text
Author
!=
Observer
!=
Reviewer
!=
Validator
!=
Authority
```

El productor de un artefacto no deberá ser su único evaluador cuando el riesgo o impacto justifique separación.

```text
Builder
   ↓
Reviewer
   ↓
Security Review when applicable
   ↓
QA / Test Worker
   ↓
Independent Validation
```

La separación de roles no implica necesariamente modelos diferentes, pero sí deberá evitar que una única perspectiva controle producción, evidencia, validación y autoridad.

---

## 16. Resource Governance

La ejecución agentic deberá respetar proporcionalidad.

Se deberá preferir:

- agentes temporales;
- modelos cargados bajo demanda;
- un modelo generativo pesado en VRAM por defecto cuando sea viable;
- ejecución secuencial antes que paralela salvo evidencia;
- contextos mínimos;
- límites de iteración;
- límites de herramientas;
- presupuestos de ejecución;
- liberación explícita de recursos;
- degradación controlada.

La posibilidad técnica de ejecutar múltiples agentes no constituye por sí misma justificación para hacerlo.

---

## 17. Security Control Plane

```text
Sandbox
→ containment

Security Control Plane
→ authorization
```

Ningún agente podrá:

- ampliar sus propios permisos;
- modificar policies;
- concederse authority;
- omitir el PEP;
- modificar evidencia externa;
- reinterpretar una denegación como permiso.

---

## 18. Relación con Context, Memory y Knowledge

```text
Agent Context
!=
Security Context
!=
Task State
!=
Memory
!=
Knowledge
!=
Evidence
```

El contexto mínimo de una ejecución no deberá convertirse automáticamente en memoria.

La evidencia de una ejecución no deberá convertirse automáticamente en conocimiento canónico.

La promoción entre estas categorías deberá estar gobernada.

---

## 19. Controlled Engineering Improvement

```text
sandbox evidence
      ↓
analysis
      ↓
engineering proposal
      ↓
independent validation
      ↓
human governance
```

Un candidato ganador sigue siendo solamente un candidato.

Un ranking no concede permiso para modificar código, mergear, desplegar, alterar arquitectura, cambiar Gobernanza o modificar el baseline.

---

## 20. Límites contra sobreingeniería

Este documento no autoriza:

- Agent Swarm;
- agentes permanentes;
- Mission Controller;
- Agent Factory;
- múltiples sandboxes por defecto;
- scoring universal;
- votación por mayoría de modelos;
- deliberación ilimitada;
- recursión agentic ilimitada;
- acceso libre a Internet;
- modificación del Kernel;
- auto-merge;
- auto-deploy;
- autoaprobación;
- persistencia indiscriminada;
- almacenamiento de chain-of-thought como evidencia canónica.

Todo mecanismo deberá demostrar necesidad operacional antes de introducir complejidad.

---

## 21. Dependencias conceptuales

Antes de diseñar esta arquitectura como implementación deberán existir suficiente madurez y evidencia en:

```text
Security Control Plane
Secure Context / Identity
Resource Governance
Model Governance
Sandbox Containment
Evidence
Independent Validation
Operational Metrics
Capability Contracts
Execution Contracts
```

---

## 22. Reglas que deben preservarse

```text
Agent output != Evidence

Least Privilege + Least Context

Score != Truth
Score != Safety
Score != Authority

Hard law violation
→ INVALID

Security FAIL
→ INVALID

Insufficient evidence
→ INCONCLUSIVE

Only VALID candidates
→ may be ranked

Agent completion
→ revoke temporary authority
→ unload unnecessary model resources
→ release resources
→ destroy or quarantine sandbox
→ retain authorized evidence
```

---

## 23. Estado

```text
Documento: referencia conceptual
Autoridad: no normativa
Implementación: no iniciada
Sprint autorizado: ninguno
Baseline modificado: no
```

Antes de utilizar este documento para proponer implementación deberán revisarse:

1. baseline vigente;
2. Blueprint;
3. Constitución Cognitiva;
4. Constitución de Gobernanza;
5. Security Control Plane;
6. Resource Governance;
7. Model Governance;
8. estado real del sandbox;
9. estado real de Agent Manager y composición agentic;
10. evidencia operacional disponible.

---
