---
title: Hoja de ruta de implementación de Malāk
status: activo
authority: no normativa
document_role: canonical_derived_implementation_roadmap
as_of_date: 2026-09-04
as_of_commit: 270e39b599a7bb3e7e6611e34dd644d0b7004d88
branch: main
baseline: v0.6.0-alpha
certification_branch: null
candidate_commit: 0735223
certification_status: sprint_7_10_completed
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
- Commit de integración de Sprint 7.10:

```text
270e39b599a7bb3e7e6611e34dd644d0b7004d88
```

- Baseline nominal:

```text
v0.6.0-alpha
```

- Último sprint integrado:

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

- Candidato funcional histórico de Sprint 7.10:

```text
0735223
```

- Evidencia post-merge:

```text
372 passed
compileall: PASS
git diff --check: PASS
working tree: clean
```

- `main` continúa siendo la única rama permanente.
- Sprint 7.10 está completado e integrado.
- Ningún Sprint 7.11 está autorizado.
- La sincronización del Vault es una operación derivada downstream y no
  constituye autorización de nuevas unidades.

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

La implementación permanece efímera y no introduce persistencia, Memory,
RAG, agentes, Sandbox ni ampliación de autoridad.

La finalización de este pipeline no autoriza nuevas capabilities ni ampliación
de autoridad.

---

# 7. Estado del baseline actual

Estado verificado después de integrar Sprint 7.10:

```text
commit de integración Sprint 7.10:
270e39b599a7bb3e7e6611e34dd644d0b7004d88

rama permanente:
main

Sprint 7.10:
completado e integrado

sprint activo autorizado:
ninguno

candidato funcional histórico:
0735223

suite post-merge:
372 passed

compileall:
PASS

git diff --check:
PASS

working tree post-merge:
clean
```

`main` continúa siendo la única rama permanente.

La implementación de Sprint 7.10 no autoriza automáticamente ninguna unidad
posterior, Memory persistente, agentes, tools, Sandbox o ampliación de autoridad.

La reconciliación del Malāk Project Vault representa este baseline de forma
derivada y no altera la autoridad del repositorio oficial.
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

---

# 9. Estado de autorización de nuevos sprints

```text
SPRINT 7.10 COMPLETADO E INTEGRADO
NINGÚN SPRINT POSTERIOR AUTORIZADO
```

Sprint 7.10 — `Conversation Session Isolation Foundation` completó:

```text
inspección
→ justificación
→ definición
→ debate
→ aprobación explícita del propietario
→ implementación
→ validación funcional
→ documentación de cierre
→ PR #58
→ revisión humana
→ merge a main
→ validación post-merge
```

Evidencia de integración:

```text
merge commit:
270e39b599a7bb3e7e6611e34dd644d0b7004d88

candidate:
0735223

pytest:
372 passed

compileall:
PASS

git diff --check:
PASS
```

No está autorizado:

- Sprint 7.11;
- ninguna unidad posterior;
- Memory persistente;
- nuevas capabilities;
- agentes;
- tools;
- Sandbox;
- navegación;
- ampliación de autoridad.

La sincronización del Vault puede continuar como reconciliación derivada del
baseline integrado, pero no constituye un nuevo sprint ni una autorización.

Cualquier unidad posterior deberá atravesar nuevamente el proceso completo
de admisión y aprobación.
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
| Memory Layer | `preservado` | Capacidad futura separada de Knowledge. |
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
| Unidad posterior a Sprint 7.10 | No aprobada | Debe definirse después de evaluar la evidencia y el baseline resultante de Sprint 7.10 |
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
MATERIAL BASELINE REFERENCE
270e39b599a7bb3e7e6611e34dd644d0b7004d88

PERMANENT BRANCH
main

ACTIVE SPRINT BRANCH
NONE

NOMINAL VERSION
v0.6.0-alpha

LAST COMPLETED SPRINT
Sprint 7.10 — Conversation Session Isolation Foundation

ACTIVE SPRINT
NONE

SPRINT AFTER 7.10
NONE AUTHORIZED

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
