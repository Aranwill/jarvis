---
title: Hoja de ruta de implementación de Malāk
status: activo
authority: no normativa
document_role: canonical_derived_implementation_roadmap
as_of_date: 2026-09-11
as_of_commit: e45a3e3c0ebf657a513596aa74452413479c05d1
branch: main
baseline: v0.6.0-alpha
certification_branch: null
candidate_commit: null
certification_status: current_main_validated
legacy_planning_source:
  - docs/project/roadmap.md
language: es
---

# Hoja de ruta de implementación de Malāk

## Propósito

Este documento constituye la fuente derivada canónica para consultar la
planificación de implementación vigente de Malāk.

Centraliza:

- estado de referencia del baseline;
- sprints completados;
- estado de autorización de nuevas unidades;
- iniciativas incorporadas a planificación futura;
- propuestas pendientes;
- disposición de planificación legacy;
- relaciones entre ideas, planificación y fichas de sprint.

Este documento es deliberadamente **derivado y no normativo**.

No reemplaza ni modifica ninguna fuente de ley, arquitectura, seguridad,
gobernanza o contrato aprobado.

---

# 1. Clasificación y autoridad

Este documento:

- no aprueba arquitectura;
- no modifica arquitectura;
- no autoriza cambios;
- no reemplaza fuentes normativas;
- no establece automáticamente el próximo sprint;
- no convierte una recomendación en obligación;
- no concede autoridad a ningún componente;
- no puede ser utilizado para modificar documentos protegidos;
- no puede ser interpretado como permiso de implementación.

Ante cualquier conflicto prevalecen las fuentes de mayor autoridad definidas por
Malāk.

La planificación se subordina siempre a esas fuentes.

---

# 2. Regla de acceso y autoridad

La existencia de información de planificación no altera el modelo de autoridad
de Malāk.

La planificación puede describir o proponer trabajo downstream.

No puede conceder autoridad upstream.

Ningún componente, capability, runtime, modelo, agente, worker, tool o mecanismo
de automatización puede utilizar este roadmap para:

- modificar Constitución Cognitiva;
- modificar Constitución de Gobernanza;
- modificar Blueprint;
- modificar Kernel;
- modificar políticas;
- elevar privilegios;
- concederse permisos;
- ampliar su propio alcance;
- reinterpretar una propuesta como autorización.

Los resultados y evidencia producidos durante una implementación pueden regresar
hacia componentes upstream para evaluación.

Ese retorno constituye información.

No constituye autoridad.

---

# 3. Regla de admisión de sprints

La existencia, numeración, posición, título o ficha de un sprint no constituye
autorización para implementarlo.

Cada propuesta debe someterse, como mínimo, a:

1. inspección completa del baseline vigente;
2. revisión del código, pruebas y documentación aplicables;
3. identificación de una necesidad real y comprobada de Malāk;
4. justificación de su utilidad cognitiva, arquitectónica, operativa o de gobernanza;
5. definición explícita del alcance y fuera de alcance;
6. evaluación de riesgos, dependencias, impacto y rollback;
7. validación mediante las cuatro preguntas obligatorias;
8. presentación y debate del plan de ejecución;
9. aprobación explícita e inequívoca del propietario.

Sin esa aprobación no se debe iniciar una implementación.

La aprobación de un sprint anterior no autoriza automáticamente el siguiente.

El propietario puede:

- aprobar;
- redefinir;
- diferir;
- reemplazar;
- rechazar;
- archivar

cualquier propuesta.

---

# 4. Modelo documental del roadmap

Para reducir duplicación y drift, la planificación deberá seguir esta estructura:

```text
ROADMAP.md
   │
   │ punto de entrada
   ▼
docs/project/implementation_roadmap.md
   │
   │ fuente derivada canónica de planificación
   │
   ├── references → ideas.md
   ├── references → concepts/
   └── references → sprints/
```

## 4.1 `ROADMAP.md`

Función:

```text
entry point
```

Debe permanecer pequeño.

No debe replicar estado detallado.

Debe dirigir a este documento.

## 4.2 `implementation_roadmap.md`

Función:

```text
planning source
```

Es la ubicación normal para consultar:

- baseline de planificación;
- estado de sprints;
- iniciativas futuras aceptadas para planificación;
- propuestas pendientes;
- disposición legacy.

## 4.3 `ideas.md`

Función:

```text
idea registry
```

Debe conservar ideas, visión e iniciativas antes o después de su promoción.

Una idea no se convierte automáticamente en roadmap.

Cuando una idea sea promovida, deberá referenciarse desde este documento sin
duplicar innecesariamente todo su contenido.

## 4.4 `concepts/`

Función:

```text
conceptual references
```

Los conceptos pueden proporcionar diseño preliminar, análisis o contexto.

No constituyen planificación autorizada.

Se consultan únicamente cuando una entrada de roadmap o una evaluación concreta
los haga relevantes.

## 4.5 `sprints/`

Función:

```text
execution evidence
```

Las fichas de sprint documentan:

- alcance aprobado;
- ejecución;
- validaciones;
- evidencia;
- cierre.

No deben actuar como segundo roadmap.

---

# 5. Estado de referencia

- Repositorio: `Aranwill/jarvis`.
- Rama permanente: `main`.
- Commit de integración de Sprint 7.11:

```text
3413e8ccb348440aea757d1feccde25c65be011f
```

- HEAD integrado observado post-PR #111:

```text
e45a3e3c0ebf657a513596aa74452413479c05d1
```

- HEAD de producto de la cadena episódica:

```text
9438c66e315faa2b4c8c3f0a99d4e1e9619992c3
```

- Baseline nominal:

```text
v0.6.0-alpha
```

- Último sprint integrado:

```text
Sprint 7.11 — Reproducible Validation Pipeline Foundation
```

- Última unidad de código de producto integrada:

```text
G2A — Protected Finalization Foundation
```

- Último diseño cognitivo integrado:

```text
Assurance Signal Authority Boundary — G0/G1
```

- Cadena episódica aislada integrada después de Sprint 7.11:

```text
Episodic Memory Admission Boundary
        ↓
Assessment Provenance Boundary
        ↓
Assessment Producer Authorization Boundary
        ↓
Governed Input Projection Boundary
        ↓
Governed Projection Consumption Boundary
```

- Última ruta conversacional/runtime integrada:

```text
Sprint 7.10 — Conversation Session Isolation Foundation
```

- Sprint autorizado actualmente:

```text
ninguno
```

- Rama de implementación activa:

```text
ninguna
```

- Candidato final de Sprint 7.11:

```text
59f592e2e36d11bbd14f7d9d93b1dac4f442c108
```

- Evidencia del candidato final:

```text
388 passed
compileall: PASS
git diff --check: PASS
FULL 4R: PASS
independent validation: PASS
```

- Validación post-merge de Sprint 7.11 sobre `main`: `success`.
- `main` continúa siendo la única rama permanente.
- Sprint 7.11 permanece completado e integrado como último sprint numerado.
- Las fronteras de Memory posteriores fueron autorizadas e integradas como
  unidades separadas y no constituyen Sprint 7.12.
- PR #82 integró Assessment Provenance.
- PR #85 integró Assessment Producer Authorization.
- PR #88 integró Governed Input Projection.
- PR #92 integró Governed Projection Consumption; su candidate
  `5139d95aaa2c30971b3979ca7c3917067856a428` pasó Validation candidate-bound en
  Ubuntu, Windows y macOS; Ubuntu reportó `645 passed`.
- `Projection READY != Admission ELIGIBLE`; el adapter de consumo integrado
  bloquea projections no consumibles y delega una vez a Admission cuando aplica,
  sin wiring conversacional/runtime, persistencia ni side effects.
- PR #93 integró únicamente G0/G1 de Candidate Content Identity; G2,
  implementación y propagación no están autorizados.
- PR #97–#99 preservaron y diseñaron Evidence-Bound Cognition / Progressive
  Cognitive Assurance a nivel conceptual/G0/G1; la promoción normativa posterior
  quedó reflejada mediante ADR-005, Blueprint v0.6.2-alpha y Cognitive
  Constitution v1.1.0.
- PR #110 integró G2A — Protected Finalization Foundation de forma aislada,
  determinista y sin wiring a Conversation/Kernel/provider/runtime.
- PR #111 integró G0/G1 de Assurance Signal Authority Boundary; Signal Boundary
  G2 y Conversation Finalization G2B permanecen no autorizados.
- Ningún Sprint 7.12 ni implementación posterior a G2A está autorizado.
- RDD Stage 1 está adoptado; RDD Stage 2 no está autorizado.
- La última reconciliación aceptada del Vault refleja Malāk
  `5865da6a5e502fe71e35e2e38bc4cceaab9b3600` mediante Vault PR #98; los cambios
  posteriores deben reconciliarse downstream antes del siguiente gate que
  requiera drift cero.

Como referencia histórica, Sprint 7.9 cerró con candidato funcional:

```text
d58b8ec98d48f5e2eac115d1d54b193e1df617fd
```

y validación final:

```text
365 passed
compileall: PASS
git diff --check: PASS
runtime real: PASS
revisión final 4R: PASS
```
---

# 6. Arquitectura implementada relevante para planificación

El Kernel permanece desacoplado de:

- runtimes concretos;
- providers concretos;
- modelos concretos;
- configuración externa de runtime.

Sprint 7.8 estableció la primera ruta cognitiva conversacional integrada:

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
Response
```

`ConversationCapability` actúa como frontera entre el pipeline cognitivo y el
subsistema conversacional.

La construcción de:

```text
providers
runtimes
services
configuration
```

permanece fuera del Kernel.

Sprint 7.9 añadió continuidad conversacional efímera mediante historial
estructurado, `InMemoryConversationContext` y limpieza explícita con `new`,
sin introducir estado conversacional en el Kernel ni en `SecurityContext`.

Sprint 7.10 añade aislamiento conversacional por `session_id`.
La frontera `Capability.execute(...)` preserva el `Request` existente,
`ConversationService` selecciona historial por sesión y la CLI rota la
identidad de sesión mediante `new`.

La implementación conversacional permanece efímera y no introduce
persistencia, RAG, agentes, Sandbox ni ampliación de autoridad.

Después de Sprint 7.11 se materializó incrementalmente una cadena episódica
aislada bajo `src/malak/memory/`:

```text
EpisodicMemoryCandidate
        ↓
AdmissionAssessment
        ↓
Assessment Provenance
VALID | HOLD | INVALID
        ↓
Assessment Producer Authorization
AUTHORIZED | HOLD | DENIED
        ↓
Governed Input Projection
READY | HOLD | DENIED
        ↓
Governed Projection Consumption
BLOCKED | EVALUATED
        ↓
Episodic Admission
REJECT | HOLD | ELIGIBLE
        ↓
STOP
```

La proyección gobernada reconstruye source authority, confidence, sensitivity,
source security status y señales de admisión desde assessments candidate-bound
con provenance y autorización verificadas; temporal validity requiere evidencia
dedicada autorizada. No confía en campos trust-sensitive de `candidate.control`
por mera presencia y no aplica last-write-wins.

La frontera de consumo valida el binding y policy-version de la projection,
construye una vista efímera con el `effective_context` gobernado y llama
exactamente una vez a `evaluate_episodic_candidate(...)` solo cuando la
projection es consumible. No persiste Memory ni crea side effects.

La cadena no introduce Conversation/runtime wiring, persistencia, retrieval,
Knowledge, cambios al Kernel ni ampliación de autoridad.

PR #110 añadió, de forma separada, G2A — Protected Finalization Foundation bajo
`src/malak/core/protected_finalization.py`. La foundation materializa la
separación `Generated Candidate != Final Response` mediante evaluación
`ACCEPT | ABSTAIN | BLOCK`, permanece pura/determinista y no está conectada a la
ruta conversacional. PR #111 documentó G0/G1 del ownership de las señales que
G2A necesitaría para una integración posterior.

La finalización de estas unidades no autoriza nuevas capabilities ni ampliación
de autoridad. Signal Boundary G2 y Conversation Finalization G2B requieren gates
y aprobación separados.

---

# 7. Estado del baseline actual

Estado verificado después de integrar PR #111:

```text
commit de integración Sprint 7.11:
3413e8ccb348440aea757d1feccde25c65be011f

HEAD integrado actual:
e45a3e3c0ebf657a513596aa74452413479c05d1

HEAD de producto de la cadena episódica:
9438c66e315faa2b4c8c3f0a99d4e1e9619992c3

rama permanente:
main

Sprint 7.11:
completado e integrado

última unidad de código de producto integrada:
G2A — Protected Finalization Foundation

último diseño cognitivo integrado:
Assurance Signal Authority Boundary — G0/G1

última ruta conversacional/runtime integrada:
Sprint 7.10 — Conversation Session Isolation Foundation

sprint activo autorizado:
ninguno

candidato final Sprint 7.11:
59f592e2e36d11bbd14f7d9d93b1dac4f442c108

suite del candidato Sprint 7.11:
388 passed

compileall:
PASS

git diff --check:
PASS

PR #92 candidate validation:
success on ubuntu-latest / windows-latest / macos-latest
645 passed on Ubuntu

current main validation:
success on e45a3e3c0ebf657a513596aa74452413479c05d1
```

`main` continúa siendo la única rama permanente.

El G3 original de Episodic Memory Admission fue integrado mediante PR #76 con
candidate `e3e3c2aa6031d4a6a9ad8f3a3c529a9453cbbe9b` y merge
`2d5fe87c304927baeab29e5649f2383030e1a1fd`. Posteriormente se integraron de
forma separada Assessment Provenance (PR #82), Assessment Producer Authorization
(PR #85), Governed Input Projection (PR #88) y Governed Projection Consumption
(PR #92), alcanzando el HEAD de producto
`9438c66e315faa2b4c8c3f0a99d4e1e9619992c3`.

La integración de cada unidad requirió autorización separada y no promovió un
Sprint 7.12. Del mismo modo, PR #92 no autoriza automáticamente Candidate Content
Identity G2, Persistence Authorization, Memory persistente, agentes, tools,
Sandbox, RDD Stage 2 o ampliación de autoridad.

PR #93 añadió únicamente el G0/G1 de Candidate Content Identity. PR #97–#99
preservaron y diseñaron Evidence-Bound Cognition / Progressive Cognitive
Assurance; su promoción normativa posterior quedó registrada mediante ADR-005,
Blueprint v0.6.2-alpha y Cognitive Constitution v1.1.0. PR #110 materializó G2A
en aislamiento y PR #111 integró G0/G1 de Assurance Signal Authority Boundary.

La última reconciliación aceptada del Malāk Project Vault representa Malāk
`main@5865da6a5e502fe71e35e2e38bc4cceaab9b3600` mediante Vault PR #98. Los
cambios posteriores deben sincronizarse antes del siguiente gate que requiera
drift cero y no alteran la autoridad del repositorio oficial.
---

# 8. Estado de sprints del bloque 7.x

| Sprint | Estado | Resultado |
|---|---|---|
| 7.0 | Cerrado | CLI mínima con `MockLLMRuntime` |
| 7.1 | Cerrado | Composición de CLI con `OllamaRuntime` mediante configuración externa |
| 7.2 | Cerrado | Contrato estructural `RuntimeMetricSink` de solo escritura |
| 7.3 | Cerrado | Estabilización de la frontera de `ConversationProvider` |
| 7.4 | Cerrado | Consolidación de logs, métricas y auditoría; sincronización gobernada del Vault |
| 7.5 | Cerrado | Security Control Plane Foundation; autorización, PDP, PEP y auditoría |
| 7.6 | Cerrado | Secure Context Lifecycle Foundation |
| 7.7 | Cerrado | Validación integral y certificación interna del baseline |
| 7.8 | Completado | Primera ruta cognitiva conversacional integrada |
| 7.9 | Completado | Conversation Continuity Foundation; integrado en `main` |
| 7.10 | Completado | Conversation Session Isolation Foundation; integrado y validado post-merge |
| 7.11 | Completado | Reproducible Validation Pipeline Foundation; integrado y validado post-merge |

Las unidades episódicas posteriores a Sprint 7.11 fueron autorizadas e integradas
por separado. No constituyen Sprint 7.12 y no modifican la numeración histórica
del bloque 7.x.

---

# 9. Estado de autorización de nuevos sprints

```text
SPRINT 7.11 COMPLETADO E INTEGRADO
EPISODIC MEMORY ADMISSION BOUNDARY INTEGRADO
ASSESSMENT PROVENANCE BOUNDARY INTEGRADO
ASSESSMENT PRODUCER AUTHORIZATION BOUNDARY INTEGRADO
GOVERNED INPUT PROJECTION BOUNDARY INTEGRADO
GOVERNED PROJECTION CONSUMPTION BOUNDARY INTEGRADO
CANDIDATE CONTENT IDENTITY G0/G1 INTEGRADO — G2 NO AUTORIZADO
PROGRESSIVE COGNITIVE ASSURANCE G0/G1 INTEGRADO
G2A — PROTECTED FINALIZATION FOUNDATION INTEGRADO
ASSURANCE SIGNAL AUTHORITY G0/G1 INTEGRADO
SIGNAL BOUNDARY G2 NO AUTORIZADO
CONVERSATION FINALIZATION G2B NO AUTORIZADO
SPRINT 7.12 NO AUTORIZADO
NINGUNA IMPLEMENTACIÓN POSTERIOR A G2A AUTORIZADA
RDD STAGE 2 NO AUTORIZADO
```

Sprint 7.11 — `Reproducible Validation Pipeline Foundation` completó:

```text
inspección
→ justificación
→ definición
→ debate
→ aprobación explícita del propietario
→ implementación
→ validación candidate-bound
→ FULL 4R
→ validación independiente
→ PR #65
→ revisión humana
→ merge a main
→ validación post-merge
```

Evidencia de integración:

```text
merge commit:
3413e8ccb348440aea757d1feccde25c65be011f

candidate:
59f592e2e36d11bbd14f7d9d93b1dac4f442c108

pytest:
388 passed

compileall:
PASS

git diff --check:
PASS

post-merge Validation:
success
```

La secuencia episódica integrada después de Sprint 7.11 es:

- PR #76 — `Episodic Memory Admission Boundary`;
- PR #82 — `Episodic Admission Assessment Provenance Boundary`;
- PR #85 — `Episodic Admission Assessment Producer Authorization Boundary`;
- PR #88 — `Episodic Admission Governed Input Projection Boundary`;
- PR #92 — `Episodic Admission Governed Projection Consumption Boundary`.

PR #92 cerró la última unidad de producto de esta cadena en
`main@9438c66e315faa2b4c8c3f0a99d4e1e9619992c3`. Su candidate
`5139d95aaa2c30971b3979ca7c3917067856a428` pasó Validation candidate-bound en
los tres hosted runners principales y Ubuntu reportó `645 passed`.

No está autorizado:

- Sprint 7.12;
- Candidate Content Identity G2 o su implementación/propagación;
- Persistence Authorization;
- Signal Boundary G2;
- Conversation Finalization G2B;
- RDD Stage 2;
- Memory persistente;
- nuevas capabilities;
- agentes;
- tools;
- Sandbox;
- navegación;
- ampliación de autoridad.

La sincronización del Vault puede continuar como reconciliación derivada del
baseline integrado, pero no constituye un nuevo sprint ni una autorización.

Cualquier unidad posterior deberá atravesar nuevamente el proceso completo de
admisión y aprobación.
---

# 10. Secure Context Lifecycle Foundation — estado preservado

Sprint 7.6 estableció:

- contrato ampliado de `SecurityContext`;
- frontera temporal `Clock`;
- `SecurityContextValidator`;
- `SecurityContextIssuer`;
- `SecurityContextRenewer`;
- enforcement del lifecycle en el Policy Decision Point;
- semántica temporal `issued_at <= now < expires_at`;
- propagación mediante `SecurityContextEnvelope`;
- denegación por defecto;
- comportamiento fail-closed.

La evidencia de cierre registró:

```text
339 pruebas aprobadas
compileall: PASS
git diff --check: PASS
```

Ese valor es histórico del Sprint 7.6 y no sustituye la evidencia posterior del
Sprint 7.8.

Permanecen fuera de alcance y requieren diseño y aprobación independientes:

- nonce y replay protection;
- identidad criptográfica;
- MFA;
- Secure Context Manager criptográfico completo;
- Secure Message Bus;
- IPC seguro;
- receipts / RDD;
- agentes;
- navegación;
- rutas operativas reales de alto riesgo.

---

# 11. Registro histórico del Sprint 7.5

El Incremento 1 incorporó:

- `PermissionScope`;
- `SecurityContext`;
- `AuthorizationRequest`;
- `AuthorizationDecision`.

La PR #15 fue integrada mediante:

```text
c0a4283b100609daeb4b3422dd28634df9d851b6
```

La validación confirmó:

```text
45 pruebas específicas
166 pruebas totales
compileall: PASS
git diff --check: PASS
```

El Incremento 2 — Activación y reconciliación documental — fue completado
mediante PR #16 y merge:

```text
4afeed440a3bf2096035d0d458d2ef75c71689fd
```

El Incremento 3 implementó un Policy Decision Point mínimo:

- determinista;
- sin LLM;
- denegación por defecto;
- evidencia inmutable de confirmación humana;
- frontera inyectable de verificación.

La validación registró:

```text
104 pruebas específicas
225 pruebas totales
```

El Incremento 4 incorporó un Policy Enforcement Point inicial:

- determinista;
- fail-closed;
- consulta directa al PDP;
- asociación mediante `request_id`;
- ejecución única ante decisión válida.

La validación registró:

```text
19 pruebas específicas
244 pruebas totales
```

La ADR-002 formalizó esta frontera.

Fue integrada mediante PR #19:

```text
af64b062aa1395ba7f7bdd59e5c1099ded68b683
```

El Incremento 5 incorporó evidencia de auditoría mediante:

```text
PR #22
418358cc5b543c59cf4b113f42e762f6c78eec59

PR #23
38b0917c5b8dba5c5a4ef4db157e78ac428ab4bc
```

El Incremento 6 completó la revisión integral y cierre.

Este registro se conserva exclusivamente por trazabilidad.

---

# 12. Cierre verificado del Sprint 7.4

Sprint 7.4 fue integrado en `main` mediante:

```text
7cd7fcc
```

Su sincronización gobernada posterior quedó registrada como:

```text
VSYNC-20260726-005
```

con resultado:

```text
completed/pass
```

La evidencia técnica registró:

```text
94 pruebas específicas
121 pruebas totales
compileall: PASS
git diff --check: PASS
```

La separación arquitectónica establecida permanece válida:

- métricas miden rendimiento cuantificable;
- eventos operativos reconstruyen ejecuciones;
- auditoría evidencia decisiones y acciones sensibles;
- métricas, eventos y auditoría permanecen separados;
- no existe un envelope universal de observabilidad;
- la evidencia no concede autoridad.

Durante Sprint 7.4, Kernel y `ConversationService` permanecieron fuera del
alcance específico de ese sprint.

Esta afirmación es histórica y no describe el estado posterior a Sprint 7.8.

---

# 13. Iniciativas incorporadas a planificación futura

Las siguientes iniciativas se encuentran reconocidas para planificación futura.

Su presencia aquí:

```text
NO autoriza diseño detallado
NO autoriza implementación
NO asigna sprint
```

## 13.1 Sandbox Containment & Evaluation Evidence Foundation

Propósito:

- aislamiento;
- entornos descartables;
- control de red;
- control de archivos;
- control de procesos;
- límites de CPU/RAM/VRAM/disco/tiempo;
- telemetría externa al agente;
- evidencia reproducible;
- snapshots y hashes;
- kill switch;
- timeout;
- cuarentena;
- pruebas de contención;
- revisión humana.

Estado:

```text
Planificación futura reconocida.
Diseño detallado no aprobado.
Implementación no aprobada.
Sin número de sprint.
```

## 13.2 Segmented Domain Governance Foundation

Propósito:

- preservar a Malāk como control plane horizontal;
- permitir Domain Packs subordinados;
- definir precedencia de políticas;
- impedir ampliación de autoridad desde capas inferiores;
- impedir contaminación del Kernel con lógica sectorial.

Estado:

```text
Planificación futura reconocida.
Diseño detallado no aprobado.
Implementación no aprobada.
Sin número de sprint.
```

## 13.3 Knowledge Intake & External Evidence Governance

Propósito:

- gobernar fuentes externas;
- conservar originales y procedencia;
- registrar autoridad, licencia y vigencia;
- tratar índices y grafos como proyecciones reconstruibles;
- incorporar saneamiento y validación;
- prevenir autocontaminación.

Estado:

```text
Planificación futura reconocida.
Diseño detallado no aprobado.
Implementación no aprobada.
Sin número de sprint.
```

## 13.4 Security Learning, Adversarial Evaluation & Deception

Propósito:

- laboratorios locales;
- CTF autorizados;
- aprendizaje defensivo;
- evaluación externa de agentes;
- deception defensiva aislada;
- transformación de evidencia en propuestas defensivas.

Estado:

```text
Planificación futura reconocida.
Diseño detallado no aprobado.
Implementación no aprobada.
Sin número de sprint.
```

Estas iniciativas no habilitan:

- agentes autónomos;
- navegación;
- malware;
- Tor;
- honeypots públicos;
- pentesting no autorizado;
- respuesta ofensiva.

---

# 14. Legacy Planning & Disposition Registry

## 14.1 Propósito

El archivo:

```text
docs/project/roadmap.md
```

contiene planificación temprana que precede a la arquitectura documental actual.

Ese documento conserva valor histórico y varias intenciones de largo plazo.

Por ese motivo:

```text
legacy != vigente
```

pero también:

```text
legacy != descartado
```

Ningún elemento contenido allí debe considerarse eliminado únicamente porque la
planificación haya evolucionado.

Esta sección centraliza su disposición actual para evitar que sea necesario
consultar ambos roadmaps durante decisiones ordinarias.

---

## 14.2 Estados de disposición

| Estado | Significado |
|---|---|
| `materializado` | La intención posee una implementación o equivalente verificable. |
| `parcialmente_materializado` | Parte de la intención existe, pero el alcance original era mayor. |
| `preservado` | Continúa siendo una intención futura válida. |
| `evolucionado` | Fue reformulada mediante una arquitectura o concepto posterior. |
| `candidato_tecnologico` | Tecnología candidata sin compromiso arquitectónico. |
| `requiere_revision` | No existe evidencia suficiente para clasificarla definitivamente. |
| `hito_historico` | Pertenece principalmente a una etapa anterior y se preserva por trazabilidad. |

Los estados anteriores son informativos.

No constituyen autorización.

---

## 14.3 Disposición de elementos legacy

| Elemento legacy | Disposición | Interpretación actual |
|---|---|---|
| Ollama | `materializado` | Existe `OllamaRuntime`; permanece detrás de `LLMRuntime`. |
| Open WebUI | `candidato_tecnologico`, `hito_historico` | Tecnología utilizada en etapas iniciales; no componente obligatorio. |
| Qwen2.5 | `candidato_tecnologico` | Modelo histórico/candidato; Malāk permanece Model Agnostic. |
| DeepSeek | `candidato_tecnologico` | Modelo histórico/candidato; no dependencia permanente. |
| Validación RAG | `preservado` | RAG continúa como capacidad futura. |
| Optimización embeddings | `preservado` | Relevante para futuras capacidades de recuperación. |
| Base documental | `evolucionado` | Evolucionó hacia Knowledge, AKS y futuras capacidades de retrieval. |
| n8n | `candidato_tecnologico` | Automatización permanece; n8n no es requisito arquitectónico. |
| Automatizaciones | `preservado` | Capacidad futura gobernada. |
| ChromaDB | `hito_historico`, `candidato_tecnologico` | Validación temprana; una base vectorial futura debe permanecer sustituible. |
| Memoria Documental | `evolucionado` | Evolucionó hacia separación Memory / Knowledge / AKS. |
| Seguridad IA | `evolucionado` | Evolucionó hacia las fundaciones de seguridad actuales. |
| OWASP LLM Top 10 | `preservado` | Referencia futura de seguridad. |
| Prompt Injection | `preservado` | Amenaza relevante para contenido externo, tools y evidence acquisition. |
| SSRF | `preservado` | Amenaza relevante para futuras capacidades de red. |
| Auditoría documental | `evolucionado` | Relacionada actualmente con AKS, trazabilidad y gobernanza documental. |
| Voice | `preservado` | Capacidad futura. |
| Whisper | `candidato_tecnologico` | Posible tecnología futura de Voice. |
| Piper | `candidato_tecnologico` | Posible tecnología futura de Voice. |
| Agentes | `preservado` | Capacidad futura sujeta a seguridad y gobernanza. |
| Module Registry | `requiere_revision` | Responsabilidad legacy todavía no clasificada definitivamente. |
| Event Bus | `preservado` | Concepto arquitectónico vigente sujeto a verificación del baseline. |
| Lifecycle Manager | `requiere_revision` | Existen mecanismos posteriores de lifecycle, pero no se asume equivalencia exacta. |
| Health Manager | `preservado`, `requiere_revision` | Health sigue siendo preocupación válida; responsabilidad exacta pendiente de revisión. |
| HelloCapability | `hito_historico` | Hito mínimo posteriormente reemplazado por capabilities funcionales reales. |
| Procesamiento de Request | `materializado` | Existe flujo de Request mediante Kernel. |
| Tests del Kernel | `materializado` | Existe validación automatizada del Kernel. |
| Baseline Kernel v1.0 | `hito_historico` | Nomenclatura histórica; no representa la versión nominal actual. |
| Memory Layer | `parcialmente_materializado` | Admission, Assessment Provenance, Producer Authorization, Governed Input Projection y Governed Projection Consumption están materializados de forma aislada; Candidate Content Identity G2, Persistence Authorization, persistencia, retrieval y Memory operativa permanecen futuras. |
| Knowledge Layer | `preservado` | Capacidad futura relacionada con AKS y retrieval. |
| RAG | `preservado` | Capacidad futura. |
| Vector DB | `candidato_tecnologico` | Infraestructura futura sustituible y reconstruible. |
| Planning Engine | `parcialmente_materializado` | Existe Planner mínimo; planificación avanzada requiere diseño independiente. |
| Reasoning Engine | `preservado`, `requiere_revision` | Intención cognitiva futura; arquitectura no definida por el roadmap legacy. |
| Capabilities reales | `parcialmente_materializado` | Ya existen capabilities funcionales; futuras siguen Capability First. |
| FastAPI | `candidato_tecnologico` | Tecnología candidata, no compromiso arquitectónico. |
| IoT | `preservado` | Capacidad futura. |
| Vision | `preservado` | Capacidad futura. |
| OSINT | `evolucionado` | Parte de su intención evolucionó hacia Evidence Acquisition Foundation. |
| Workflows | `preservado` | Capacidad futura relacionada con automatización y orquestación. |
| Malāk Platform v1.0 | `preservado` | Visión de largo plazo; no release plan aprobado. |

---

# 15. Regla de promoción de planificación legacy

Un elemento legacy puede evolucionar mediante:

```text
legacy
  ↓
idea
  ↓
evaluación
  ↓
roadmap
  ↓
specification
  ↓
ADR cuando corresponda
  ↓
sprint aprobado
  ↓
implementation
  ↓
evidence
  ↓
baseline
```

No todos los elementos necesitan recorrer todos los estados.

También pueden evolucionar explícitamente a:

```text
legacy
→ rechazada
```

o:

```text
legacy
→ superseded
```

pero esa transición debe quedar registrada.

Reglas:

```text
ausencia de implementación != rechazo

antigüedad != descarte

idea != roadmap

roadmap != aprobación

aprobación != ejecución

evidencia != autoridad
```

---

# 16. Tecnologías legacy

Las tecnologías nombradas históricamente representan contexto o candidatos:

```text
Ollama
Open WebUI
Qwen2.5
DeepSeek
n8n
ChromaDB
Whisper
Piper
FastAPI
```

Su aparición en documentación legacy no las convierte en dependencias.

Toda selección futura deberá justificarse contra:

- requisitos;
- arquitectura vigente;
- Runtime Independence;
- Vendor Independence;
- seguridad;
- mantenibilidad;
- recursos;
- evidencia técnica.

---

# 17. Propuestas pendientes de revisión y aprobación

| Propuesta | Estado | Observación |
|---|---|---|
| Preparación del AKS para GraphRAG | No aprobada | No implica implementar GraphRAG |
| Candidate Content Identity G2 | No aprobada | G0/G1 integrado por PR #93; debe congelar canonicalización/identity semantics antes de implementación y no autoriza Persistence Authorization |
| Cognitive Assurance — Protected Finalization | Parcialmente materializada | Promoción normativa aceptada; G2A integrado por PR #110 y Signal Authority G0/G1 integrado por PR #111. Signal Boundary G2 y Conversation Finalization G2B permanecen no autorizados |
| Module Registry legacy | Requiere revisión | Determinar si la responsabilidad continúa siendo necesaria o fue absorbida por otra abstracción |
| Lifecycle Manager legacy | Requiere revisión | Comparar intención original contra lifecycle actual |
| Health Manager legacy | Requiere revisión | Definir responsabilidad mínima antes de cualquier propuesta |

La tabla no establece secuencia obligatoria.

---

# 18. Regla de admisión de Capabilities

Una Capability solo podrá incorporarse cuando añada una funcionalidad:

```text
real
necesaria
permanente
```

para Malāk.

No deben crearse Capabilities exclusivamente para:

- validar routing;
- demostrar múltiples entradas;
- probar Registry;
- aumentar cobertura artificialmente;
- completar una secuencia histórica;
- incorporar ejemplos sin utilidad funcional.

La infraestructura interna debe validarse mediante:

- tests;
- doubles;
- fixtures;
- contratos;
- integración controlada.

---

# 19. Restricción estructural

Antes de introducir:

- agentes;
- herramientas externas;
- automatización del sistema operativo;
- navegación;
- mensajería externa;
- memoria sensible;
- Capabilities de alto riesgo;

deben existir las fundaciones requeridas de seguridad y gobernanza.

Ninguna propuesta futura puede:

- ampliar el Kernel con lógica de negocio;
- acoplar el Kernel a un runtime;
- acoplar el Kernel a un proveedor;
- acoplar el Kernel a un modelo;
- introducir dependencias no aprobadas;
- modificar contratos centrales sin revisión;
- asumir que el hardware actual define la arquitectura permanente.

---

# 20. Fichas relacionadas

Evidencia detallada de ejecución:

```text
docs/project/sprints/SPRINT-7.0.md
docs/project/sprints/SPRINT-7.1.md
docs/project/sprints/SPRINT-7.2.md
docs/project/sprints/SPRINT-7.3.md
docs/project/sprints/SPRINT-7.4.md
docs/project/sprints/SPRINT-7.5.md
docs/project/sprints/SPRINT-7.6.md
docs/project/sprints/SPRINT-7.7.md
docs/project/sprints/SPRINT-7.8.md
docs/project/sprints/SPRINT-7.9.md
docs/project/sprints/SPRINT-7.10.md
docs/project/sprints/SPRINT-7.11.md
```

Interpretación:

```text
Sprint file
= evidencia detallada de una unidad concreta

Sprint file
!= autorización de un sprint posterior

Sprint file
!= roadmap general
```

---

# 21. Relación con ideas

Registro de ideas:

```text
documents/projects/jarvis/ideas.md
```

Una idea registrada allí:

```text
no aprueba arquitectura
no autoriza implementación
no establece sprint
```

Cuando una idea sea aceptada para planificación deberá incorporarse a este
roadmap mediante una referencia identificable.

No debe duplicarse innecesariamente todo su análisis.

---

# 22. Relación con Concepts

Referencias conceptuales:

```text
docs/project/concepts/
```

Los Concepts:

- preservan análisis;
- preservan alternativas;
- preservan referencias;
- pueden alimentar evaluación futura;
- no autorizan implementación;
- no forman parte del roadmap hasta promoción explícita.

Este roadmap deberá referenciar el Concept aplicable cuando sea necesario.

---

# 23. Disposición de `docs/project/roadmap.md`

El archivo:

```text
docs/project/roadmap.md
```

se conserva como fuente de planificación legacy original.

Debe identificarse explícitamente como documentación legacy y dirigir hacia:

```text
docs/project/implementation_roadmap.md
```

como fuente derivada canónica de planificación vigente.

Los estados, fases, numeraciones y tecnologías preservados en el roadmap legacy
pertenecen a su contexto histórico y no deben reinterpretarse como estado
operativo, baseline vigente ni autorización de implementación.

El corrective packet documental actual no elimina ni archiva ese archivo.
Su contenido histórico se preserva y únicamente se clarifica su clasificación.

Cualquier propuesta futura para archivarlo, sustituirlo por un stub o eliminarlo
requerirá una evaluación independiente que confirme que no existe información
histórica o de planificación única que deba conservarse.

---

# 24. Regla de no duplicación

A partir de esta consolidación:

`project_context.md` no debería mantener una copia extensa del roadmap.

`README.md` no debería mantener más que un resumen operativo mínimo.

`ROADMAP.md` raíz no debería duplicar planificación.

`ideas.md` no debería duplicar planes detallados.

`concepts/` no debería mantener estados operativos de sprint.

`sprints/` no deberían convertirse en roadmap.

La regla objetivo es:

```text
un concepto → una ubicación responsable
```

con referencias entre artefactos.

---

# 25. Regla de actualización

Este documento debe revalidarse cuando ocurra cualquiera de estos eventos:

- cambio material del baseline o de `HEAD` que afecte la planificación descrita;
- cierre de un sprint;
- apertura formal de un nuevo sprint;
- modificación material de contratos públicos;
- aceptación de una decisión arquitectónica que afecte planificación;
- cambio de rama permanente;
- certificación de un nuevo baseline;
- promoción de una idea al roadmap;
- rechazo o supersedencia de una iniciativa;
- cambio material de las reglas de gobernanza o ejecución.

Los commits puramente documentales, mecánicos o de sincronización que no alteren
la planificación descrita no obligan por sí solos a reemplazar `as_of_commit` ni
el commit material de referencia.

Los registros históricos no deben reescribirse silenciosamente para coincidir
con el presente.

Las diferencias históricas deben conservar contexto temporal.

---

# 26. Estado actual de planificación

```text
CURRENT INTEGRATED HEAD
e45a3e3c0ebf657a513596aa74452413479c05d1

CURRENT PRODUCT HEAD
ecb1315946f47534135bbdc73d94ccf88df0d8d6

SPRINT 7.11 INTEGRATION REFERENCE
3413e8ccb348440aea757d1feccde25c65be011f

PERMANENT BRANCH
main

ACTIVE SPRINT BRANCH
NONE

NOMINAL VERSION
v0.6.0-alpha

LAST COMPLETED NUMBERED SPRINT
Sprint 7.11 — Reproducible Validation Pipeline Foundation

LATEST PRODUCT UNIT
G2A — Protected Finalization Foundation

LATEST MEMORY DESIGN UNIT
Episodic Candidate Content Identity — G0/G1 ONLY

LATEST COGNITIVE ASSURANCE DESIGN
Assurance Signal Authority Boundary — G0/G1

LAST CONVERSATIONAL/RUNTIME SPRINT
Sprint 7.10 — Conversation Session Isolation Foundation

ACTIVE SPRINT
NONE

SPRINT 7.12
NONE AUTHORIZED

IMPLEMENTATION AFTER G2A
NONE AUTHORIZED

SIGNAL BOUNDARY G2
NOT AUTHORIZED

CONVERSATION FINALIZATION G2B
NOT AUTHORIZED

CANDIDATE CONTENT IDENTITY G2
NOT AUTHORIZED

RDD STAGE 2
NOT AUTHORIZED

LEGACY ROADMAP
DISPOSITION REGISTERED

LAW DOCUMENTS
OUT OF SCOPE

AUTHORITY EXPANSION
NONE
```

---

# 27. Principio de cierre

La planificación de Malāk debe permanecer:

```text
trazable
→ gobernada
→ incremental
→ reversible
→ subordinada a autoridad superior
```

El roadmap organiza intención.

No crea autoridad.

La evidencia puede producir una propuesta.

La propuesta puede producir una decisión humana.

Solo una decisión autorizada puede producir implementación.