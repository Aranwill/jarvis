---
title: Registro de ideas y visión futura de Malāk
status: activo
authority: no normativa
document_role: anexo de captura y seguimiento
introduced_in: Sprint 7.4
as_of_date: 2026-08-12
as_of_commit: 48d6ea2de9d7bd60495208b77d81175415bc3350
branch: main
language: es
---

# Registro de ideas y visión futura de Malāk

## Propósito

Este documento centraliza ideas, visiones e iniciativas futuras relacionadas con Malāk para evitar que se pierdan entre conversaciones, notas aisladas o documentos operativos.

Su función es:

- capturar una idea antes de que exista un diseño completo;
- conservar su intención y sus restricciones principales;
- distinguir con claridad una idea de una decisión, un elemento del roadmap o una implementación;
- facilitar su revisión, promoción, aplazamiento o descarte;
- mantener trazabilidad hacia los documentos de mayor autoridad;
- servir como entrada gobernada para la futura sincronización del Malāk Project Vault.

Este documento puede crecer de forma incremental. No es necesario diseñar por completo una iniciativa para registrarla, pero toda entrada debe indicar su estado y evitar presentar arquitectura futura como arquitectura implementada.

## Autoridad y límites

Este documento es un anexo informativo y no normativo.

Una idea registrada aquí:

- no aprueba su arquitectura;
- no autoriza su implementación;
- no establece automáticamente un sprint;
- no altera el baseline oficial;
- no reemplaza el Blueprint;
- no reemplaza la Constitución Cognitiva;
- no reemplaza la Constitución de Gobernanza;
- no reemplaza ADR, RFC, especificaciones, contratos ni documentos operativos aprobados;
- no concede autoridad automática a Malāk, sus agentes, sus modelos o su telemetría.

Cuando una idea sea aceptada para planificación, deberá reflejarse en el roadmap correspondiente. Cuando requiera una decisión arquitectónica, deberá promoverse al mecanismo documental aplicable. Cuando sea implementada, su estado deberá verificarse contra el repositorio oficial.

Ante contradicciones, prevalecerán siempre las fuentes de mayor autoridad documental.

## Estados permitidos

| Estado | Significado |
|---|---|
| `capturada` | La idea fue registrada, pero todavía no fue evaluada formalmente. |
| `en_evaluacion` | La idea está siendo analizada y puede cambiar o descartarse. |
| `aprobada_para_planificacion_futura` | El propietario aprobó conservarla e incorporarla a la planificación futura. No autoriza diseño detallado ni implementación. |
| `promovida_al_roadmap` | La iniciativa ya está representada en el roadmap aplicable. |
| `diferida` | Se conserva, pero no corresponde tratarla en el horizonte actual. |
| `rechazada` | Fue descartada y no debe reutilizarse sin una nueva decisión explícita. |
| `implementada` | Existe evidencia verificada de su implementación en el baseline oficial. |

## Reglas de mantenimiento

Cada entrada debe incluir, como mínimo:

- identificador estable;
- nombre;
- estado;
- intención;
- valor esperado;
- restricciones o principios;
- dependencias conocidas;
- relación con otras iniciativas;
- próximo paso gobernado;
- referencias documentales cuando existan.

Las entradas no deben eliminarse solo porque hayan sido rechazadas, diferidas o implementadas. Deben conservarse con su estado actualizado para mantener trazabilidad.

Los cambios deben ser pequeños, revisables y reversibles. Las ideas nuevas no deben provocar normalizaciones documentales masivas ni modificar snapshots históricos.

## Visión rectora

Malāk se concibe como una plataforma cognitiva personal local, modular, gobernable, extensible, auditable y desacoplada de modelos, runtimes y proveedores concretos.

Las ideas registradas en este documento deberán respetar, como mínimo:

- Human in Control;
- Kernel First;
- Capability First;
- Runtime Independence;
- Language Agnostic;
- Zero Trust interno;
- Defense in Depth;
- separación de responsabilidades y zonas de confianza;
- evidencia antes que afirmaciones;
- autoridad humana antes que modificación;
- privacidad y minimización de datos;
- trazabilidad y reversibilidad;
- uso eficiente y gobernado de recursos;
- sprints cortos y de alcance explícito.

La existencia de una capacidad técnica no implica autoridad para utilizarla.

## Ideas e iniciativas registradas

### IDEA-001 — Sandbox Containment & Evaluation Evidence Foundation

**Estado:** `aprobada_para_planificacion_futura`

**Intención**

Crear una fundación dedicada a contener, observar y demostrar externamente qué ocurre durante la ejecución de agentes, modelos y simulaciones dentro de sandboxes controlados.

**Valor esperado**

- impedir que el agente sea la única fuente de evidencia sobre sus propias acciones;
- detectar intentos o rutas inesperadas de escape, red, archivos, procesos o herramientas;
- producir ejecuciones reproducibles y auditables;
- conservar evidencia útil para seguridad, evaluación y mejora controlada;
- permitir simulaciones de mayor complejidad sin debilitar Human in Control.

**Alcance conceptual inicial**

- aislamiento por defecto;
- entornos descartables;
- políticas explícitas para red, archivos, procesos y herramientas;
- límites de CPU, RAM, VRAM, almacenamiento, tiempo y cantidad de procesos;
- manifiesto reproducible por ejecución;
- telemetría externa al agente;
- registro de comandos, herramientas, conexiones y operaciones;
- snapshots y hashes anteriores y posteriores;
- kill switch, timeout, cuarentena y cierre seguro;
- artefactos de evaluación en un almacén independiente;
- correlación e integridad de la evidencia;
- pruebas de escape y validación de contención;
- revisión humana obligatoria.

**Razonamiento experimental**

Una eventual traza de razonamiento:

- será opcional;
- estará desactivada por defecto;
- se limitará a simulaciones expresamente aprobadas;
- utilizará preferentemente datos sintéticos o saneados;
- se almacenará separada de los logs operativos y de la auditoría canónica;
- será considerada evidencia auxiliar y no confiable;
- no se convertirá automáticamente en memoria;
- no podrá aprobar por sí sola una mejora ni justificar una acción.

La evidencia canónica deberá provenir del sandbox y de los planos de control, no únicamente de la explicación generada por el agente.

**Dependencias**

- requiere primero `Security Control Plane Foundation`;
- precede a simulaciones avanzadas con agentes;
- precede al uso gobernado de evidencia por el ciclo de mejora controlada.

**Ubicación lógica**

```text
Security Control Plane Foundation
        ↓
Sandbox Containment & Evaluation Evidence Foundation
        ↓
Simulaciones controladas y agentes
        ↓
Controlled Engineering Improvement Loop Foundation
```

**Próximo paso gobernado**

Incorporar la iniciativa al roadmap futuro sin asignar automáticamente un número de sprint. Su diseño detallado y su implementación requerirán inspección del baseline, alcance propio, evaluación de riesgos, rollback y aprobación explícita.

**Referencia conceptual relacionada**

La ejecución agentic efímera, el principio de `Least Context`, la observación
externa, el lifecycle de recursos y la evaluación de candidatos se preservan
con mayor detalle en:

`docs/project/concepts/GOVERNED_EPHEMERAL_AGENT_EXECUTION_EVIDENCE_REFERENCE.md`

Esta relación no modifica el alcance ni el estado de IDEA-001. La evidencia
canónica de una ejecución agentic deberá permanecer independiente de la
explicación producida por el propio agente.

### IDEA-002 — Controlled Engineering Improvement Loop Foundation

**Estado:** `aprobada_para_planificacion_futura`

**Intención**

Crear un ciclo gobernado mediante el cual Malāk pueda observar evidencia, evaluar resultados y formular propuestas de mejora sin obtener autoridad para modificarse.

**Principios obligatorios**

> Malāk no se automejora modificándose. Se automejora aumentando la calidad de sus observaciones, evaluaciones y propuestas.

> La capacidad de aprender no implica autoridad para cambiar.

> La evidencia puede originar una propuesta; solamente la gobernanza puede convertirla en una modificación.

**Evidencia prevista**

- benchmarks;
- telemetría;
- fallos e incidentes;
- casos de evaluación reproducibles;
- resultados esperados y obtenidos;
- acciones de herramientas;
- controles de seguridad;
- consumo de recursos;
- regresiones;
- comparación contra baselines anteriores;
- decisiones humanas.

El ciclo no deberá depender de conversaciones completas ni de la cadena de pensamiento del modelo como fuente autoritativa.

**Dependencias**

- `Model Governance Foundation`;
- `Sandbox Containment & Evaluation Evidence Foundation`;
- evaluaciones reproducibles;
- gobernanza humana;
- trazabilidad y rollback.

**Próximo paso gobernado**

Mantenerla en planificación futura. No diseñar ni implementar el loop dentro del Sprint 7.4.

### IDEA-003 — Resource Governance Foundation

**Estado:** `aprobada_para_planificacion_futura`

**Intención**

Gobernar el consumo de RAM, VRAM, CPU, almacenamiento, contexto, modelos, herramientas y servicios sin degradar seguridad, calidad ni trazabilidad.

**Principios iniciales**

- activar solo las capacidades necesarias;
- aplicar lazy loading a modelos, índices, servicios y herramientas;
- descargar recursos tras inactividad;
- mantener por defecto un solo modelo generativo pesado en VRAM;
- preferir ejecución secuencial antes que paralela, salvo evidencia telemétrica;
- utilizar cachés de vida corta con invalidación explícita;
- filtrar herramientas según el contexto;
- limitar `top-k` y reranking;
- tratar índices, grafos y cachés como proyecciones reconstruibles;
- degradar capacidades de forma controlada y transparente cuando falten recursos.

**Próximo paso gobernado**

Evaluar su ubicación después de que la telemetría y las métricas puedan aportar evidencia suficiente. Requiere diseño y aprobación propios.

**Referencia conceptual relacionada**

El lifecycle de recursos asociado a ejecuciones agentic efímeras se preserva
con mayor detalle en:

`docs/project/concepts/GOVERNED_EPHEMERAL_AGENT_EXECUTION_EVIDENCE_REFERENCE.md`

Cuando una responsabilidad agentic temporal finalice, los modelos, contextos,
permisos y recursos asociados deberán liberarse explícitamente cuando no exista
una razón aprobada para conservarlos activos.

Esta referencia no redefine Resource Governance ni aprueba una política concreta
de unload. La política definitiva deberá diseñarse y validarse dentro de la
fundación correspondiente.

### IDEA-004 — Model Governance & AI Preservation Foundation

**Estado:** `capturada`

**Intención**

Gobernar la selección, validación, compatibilidad, integridad, licencia, conservación y sustitución de modelos locales.

**Componentes conceptuales**

- Model Archive;
- Metadata Registry;
- License and Tokenizer Vault;
- Prompt Library;
- Benchmark Registry;
- Capability Tests;
- Compatibility Matrix;
- verificación de integridad mediante hashes;
- snapshots y versionado;
- criterios de promoción, retiro y rollback de modelos.

**Relaciones**

La gobernanza de modelos es una dependencia del futuro ciclo de mejora controlada. La preservación de modelos no debe acoplar el Kernel a un proveedor ni convertir el hardware actual en una restricción arquitectónica permanente.

**Próximo paso gobernado**

Separar, durante su evaluación, qué pertenece a gobernanza de modelos y qué pertenece a preservación y archivo. No asumir que ambos alcances deban implementarse en un único sprint.

### IDEA-005 — Secure Context Manager

**Estado:** `capturada`

**Intención**

Representar contextos de seguridad verificables y de vida corta para capacidades sensibles.

**Elementos conceptuales**

- identificador de sesión;
- identidad;
- roles;
- nivel de confianza;
- permisos;
- fecha y hora;
- TTL;
- nonce;
- hash del payload;
- firma.

**Restricciones**

- no reemplaza al plano de autorización;
- no concede permisos por inferencia del modelo;
- debe aplicar “Validate once, trust briefly, verify continuously”;
- requiere revisión criptográfica y de amenazas antes de implementarse.

**Próximo paso gobernado**

Evaluarla dentro o después de `Security Control Plane Foundation`, evitando introducir contratos prematuramente.

### IDEA-006 — Evidence Acquisition Framework

**Estado:** `capturada`

**Intención**

Impedir que el Kernel o los modelos consuman Internet cruda y establecer una ruta controlada para adquirir, sanear, validar y conservar evidencia externa.

**Flujo conceptual**

```text
Evidence Broker
    → Search
    → Fetch
    → Content Sanitizer
    → Prompt Injection Detection
    → Evidence Validation
    → Evidence Store
```

**Restricciones**

- la evidencia no concede autoridad;
- el contenido externo se considera no confiable;
- la navegación no se integra directamente al Kernel;
- la incorporación de herramientas externas exige primero seguridad, autorización y auditoría aplicables.

**Próximo paso gobernado**

Conservar la visión hasta que las fundaciones de seguridad y sandbox permitan diseñarla con límites verificables.

### IDEA-007 — Secure Isolated Access Layer

**Estado:** `capturada`

**Intención**

Proporcionar navegación privada o de alto riesgo mediante un entorno separado y endurecido, sin exponer directamente el host ni el Kernel.

**Elementos conceptuales**

- máquina virtual o entorno desechable;
- sistema y navegador endurecidos;
- túneles cifrados o VPN cuando corresponda;
- separación de identidad y credenciales;
- políticas de red;
- evidencia externa de la actividad;
- cierre y destrucción controlados.

**Dependencias**

- `Security Control Plane Foundation`;
- `Sandbox Containment & Evaluation Evidence Foundation`;
- `Evidence Acquisition Framework`;
- gobernanza explícita de credenciales y red.

**Próximo paso gobernado**

Mantenerla diferida hasta contar con las fundaciones de seguridad, contención y evidencia.

### IDEA-008 — AKS preparado para GraphRAG

**Estado:** `promovida_al_roadmap`

**Intención**

Preparar el conocimiento de ingeniería con identificadores, metadatos y relaciones suficientes para una futura evaluación de GraphRAG.

**Restricciones**

- preparar el AKS no significa implementar GraphRAG;
- GraphRAG no debe incorporarse por moda ni por inferencia;
- la necesidad deberá demostrarse contra búsquedas y navegación más simples;
- los índices y grafos deben tratarse como proyecciones reconstruibles;
- la fuente documental debe conservar autoridad y trazabilidad.

**Referencia**

- `docs/project/implementation_roadmap.md`

**Próximo paso gobernado**

Mantener la propuesta sujeta a revisión y aprobación específica.

### IDEA-009 — Development Tooling Foundation

**Estado:** `capturada`

**Intención**

Consolidar herramientas de calidad y desarrollo reproducibles sin instalar controles locales no declarados.

**Elementos por evaluar**

- Ruff;
- mypy;
- configuración centralizada en `pyproject.toml`;
- dependencias de desarrollo separadas;
- integración local y CI;
- reglas de calidad reproducibles;
- política de adopción y rollback.

**Restricciones**

- no incorporar herramientas de forma improvisada;
- no instalarlas únicamente en un entorno local sin declararlas en el baseline;
- evitar que el tooling dicte la arquitectura del producto.

**Próximo paso gobernado**

Evaluar un sprint independiente de Development Tooling o Development Foundation cuando exista necesidad comprobada.

### IDEA-010 — Owner Security Research Sandbox

**Estado:** `capturada`

**Intención**

Disponer, en el futuro, de un laboratorio educativo aislado para investigación defensiva y simulaciones autorizadas por el propietario.

**Restricciones**

- sin intrusión real;
- sin malware operativo;
- sin acceso implícito al host o a redes externas;
- sin autoridad heredada por agentes;
- con límites, evidencia, kill switch y revisión humana;
- separado del runtime normal de Malāk.

**Dependencias**

- `Security Control Plane Foundation`;
- `Sandbox Containment & Evaluation Evidence Foundation`;
- políticas específicas de uso aceptable y aislamiento.

**Próximo paso gobernado**

Mantenerla como opción futura. Su registro no constituye aprobación de diseño ni implementación.

## Relación con el Sprint 7.4

Este documento se activa como anexo documental durante el Sprint 7.4 para resolver una carencia de trazabilidad: el archivo existía vacío y varias visiones habían quedado distribuidas entre conversaciones y documentos.

Su incorporación:

- no amplía el alcance de código del Sprint 7.4;
- no modifica contratos de observabilidad;
- no implementa ninguna iniciativa futura;
- no cambia el Kernel;
- no cambia `ConversationService`;
- no autoriza el Sprint 7.5 ni ningún sprint posterior;
- no altera snapshots históricos;
- constituye únicamente una consolidación documental revisable.

La relación específica con la observabilidad del Sprint 7.4 es la siguiente:

- `OperationalEvent` conservará eventos mínimos, estructurados y seguros;
- podrá incluir una causa controlada mediante `reason_code`;
- no almacenará prompts, respuestas completas, secretos, credenciales, stack traces ni cadenas de pensamiento;
- los artefactos detallados de simulación pertenecerán a un futuro subsistema separado;
- la cadena de pensamiento no será evidencia canónica de auditoría;
- el sandbox y los planos de control deberán demostrar externamente lo ocurrido.

## Sincronización gobernada con el Malāk Project Vault

En la próxima actualización gobernada del Vault deberá proponerse la incorporación de este registro o de una proyección documental equivalente.

La sincronización deberá:

- conservar al repositorio oficial como fuente de verdad;
- presentar este documento como contexto derivado y no normativo;
- reflejar `IDEA-001` en el roadmap futuro del Vault;
- reflejar las dependencias entre seguridad, sandbox, simulaciones y mejora controlada;
- actualizar el contexto de sesión cuando corresponda;
- registrar decisiones pendientes únicamente si existen preguntas todavía abiertas;
- crear un snapshot nuevo solo cuando cambie el baseline oficial;
- no editar snapshots históricos;
- esperar aprobación humana antes de escribir.

La ubicación exacta y los archivos afectados en el Vault se decidirán durante esa sincronización, después de inspeccionar su estructura vigente. Este documento no autoriza escrituras automáticas sobre el Vault.

## Plantilla para nuevas ideas

```markdown
### IDEA-XXX — Nombre de la idea

**Estado:** `capturada`

**Intención**

Descripción breve del problema o de la visión.

**Valor esperado**

- beneficio esperado;
- capacidad que podría habilitar.

**Restricciones**

- límites de seguridad, arquitectura y gobernanza;
- elementos expresamente fuera de alcance.

**Dependencias**

- fundaciones o decisiones necesarias.

**Relaciones**

- otras ideas, documentos o iniciativas vinculadas.

**Próximo paso gobernado**

Acción necesaria para evaluar, promover, diferir o rechazar la idea.
```


### IDEA-011 — Malāk Validation & Delivery Protocol

**Estado:** `aprobada_para_planificacion_futura`

**Intención**

Formalizar un método de diseño, aprobación, implementación, validación y entrega basado en paquetes pequeños, trazables y reversibles, preservando Human in Control y la separación entre repositorio oficial, Vault y agente de sincronización.

**Valor esperado**

- reducir cambios fuera de alcance;
- permitir aprobaciones seguras desde interfaces móviles para cambios normales;
- reservar cambios críticos para revisión profunda desde un entorno personal controlado;
- convertir cada incremento en una unidad verificable con objetivo, alcance, riesgos, pruebas, aceptación y rollback;
- producir evidencia compacta y legible antes de aprobar una pull request;
- aplicar validaciones proporcionales durante la semana y una certificación profunda del baseline en sesiones específicas;
- mantener el merge y la promoción documental bajo autoridad humana.

**Principios iniciales**

- cada sprint se divide en Implementation Packets con una sola responsabilidad;
- cada paquete declara alcance incluido, alcance excluido, archivos previstos, base arquitectónica, riesgos, validaciones, aceptación y rollback;
- ningún paquete se implementa sin aprobación explícita e independiente;
- toda implementación se realiza en rama aislada y mediante pull request en borrador;
- el diff real debe poder compararse con el alcance autorizado;
- toda desviación de arquitectura, seguridad, dependencias o alcance detiene la ejecución;
- los cambios críticos se marcan `DEEP REVIEW REQUIRED`;
- el merge permanece reservado al propietario;
- el Vault se actualiza únicamente después del merge mediante una propuesta separada del agente controlado;
- las validaciones deben ser independientes de una plataforma, lenguaje, proveedor o tecnología concreta;
- los marcos externos de seguridad se utilizan como referencias de aplicabilidad y no como autoridad superior a los documentos de ley de Malāk.

**Validación de seguridad por aplicabilidad**

El protocolo podrá utilizar matrices de controles basadas en prácticas reconocidas, entre ellas OWASP Top 10, OWASP para aplicaciones LLM y agentic, NIST SSDF, Microsoft SDL y OpenSSF/SLSA.

Su incorporación deberá respetar estas reglas:

- no declarar cumplimiento total cuando solo se evaluó un alcance específico;
- clasificar cada control como aplicable, parcialmente aplicable, control arquitectónico, no aplicable, diferido o bloqueante;
- no crear pruebas artificiales para superficies que Malāk todavía no posee;
- no alterar el Kernel, contratos o documentos normativos para satisfacer una taxonomía externa;
- conservar evidencia de comandos, resultados, commit evaluado, hallazgos y exclusiones;
- exigir revisión humana ante controles críticos o evidencia insuficiente.

**Relaciones**

- `Development Tooling Foundation`;
- `Sandbox Containment & Evaluation Evidence Foundation`;
- `Constitutional Assurance Foundation`;
- `Resource Governance Foundation`;
- flujo gobernado del `malak-vault-sync-agent`.

**Próximo paso gobernado**

Diseñar una plantilla documental mínima de Implementation Packet y aplicarla primero a incrementos expresamente aprobados. No automatizar el protocolo ni modificar CI, branch protection o tooling sin paquetes separados y aprobación específica.

---

### IDEA-012 — Constitutional Assurance Foundation

**Estado:** `aprobada_para_planificacion_futura`

**Intención**

Convertir principios arquitectónicos y constitucionales objetivos de Malāk en invariantes verificables, sin reemplazar los documentos de ley ni delegar su interpretación a herramientas automáticas.

**Valor esperado**

- detectar regresiones arquitectónicas antes del merge;
- impedir acoplamientos accidentales del Kernel;
- comprobar separación de autoridad, autorización, ejecución y auditoría;
- preservar independencia de modelos, runtimes, proveedores, lenguajes y plataformas;
- demostrar que memoria, retrieval, telemetría o evidencia no adquieren autoridad implícita;
- reforzar el comportamiento fail-closed y Human in Control.

**Alcance conceptual inicial**

- invariantes de dependencias y fronteras;
- tests de contratos públicos;
- validaciones de ausencia de importaciones o acoplamientos prohibidos;
- pruebas de denegación segura;
- comprobación de que ningún LLM decide autorizaciones;
- comprobación de que el agente del Vault no puede modificar Malāk, aprobar o fusionar PR;
- validación de que documentos derivados no reemplazan fuentes normativas;
- evidencia reproducible asociada al commit evaluado.

**Restricciones**

- los tests no sustituyen la revisión arquitectónica humana;
- solo deben automatizarse invariantes objetivas y deterministas;
- no se debe codificar una interpretación ambigua de la Constitución como verdad automática;
- no se modifica el Kernel para facilitar los tests;
- no se introduce un motor general de políticas por inferencia;
- los cambios en documentos de ley continúan requiriendo aprobación expresa y revisión profunda.

**Dependencias**

- documentos de ley vigentes y estables;
- contratos públicos identificables;
- baseline verificable;
- Validation & Delivery Protocol;
- Development Tooling Foundation cuando se requiera tooling adicional.

**Próximo paso gobernado**

Seleccionar un conjunto pequeño de invariantes ya demostrables en el baseline y evaluar su incorporación durante una futura validación integral. No intentar automatizar toda la gobernanza en un único sprint.

---

### IDEA-013 — Knowledge and Context Efficiency Foundation

**Estado:** `aprobada_para_planificacion_futura`

**Intención**

Mejorar la navegación, selección de evidencia y continuidad de contexto mediante proyecciones regenerables y mecanismos gobernados, sin convertir recuperación, memoria o resúmenes en fuentes de autoridad.

**Valor esperado**

- reducir exploración repetida del repositorio;
- preparar contexto relevante con menor consumo;
- localizar contratos, tests y documentos gobernantes de forma determinista;
- detectar información obsoleta, contradictoria o fuera de alcance;
- crear una base medible para retrieval futuro sin adelantar RAG o GraphRAG;
- preservar decisiones aprobadas, rechazadas y restricciones durante tareas largas.

**Componentes conceptuales**

- Repository Knowledge Map;
- mapas de módulos, contratos, tests, dependencias y autoridad documental;
- índices generados, versionados, hasheados y vinculados a sus fuentes;
- Context Lifecycle y presupuestos de contexto;
- checkpoints de contexto con integridad verificable;
- Retrieval Candidate Pipeline con filtros de autoridad, vigencia, procedencia, aplicabilidad, contradicción y riesgo;
- selección de evidencia limitada por presupuesto;
- métricas de precisión, autoridad, obsolescencia y cobertura.

**Propiedades obligatorias de las proyecciones**

```text
GENERATED
NON-AUTHORITATIVE
REBUILDABLE
HASHED
VERSIONED
SOURCE-LINKED
```

**Restricciones**

- memoria no equivale a conocimiento;
- conocimiento no equivale a política;
- recuperación no implica autoridad;
- índices, grafos, cachés y resúmenes no reemplazan las fuentes oficiales;
- no integrar motores vectoriales, GraphRAG, bases de datos o frameworks concretos en el Kernel;
- no introducir adquisición autónoma de contenido externo;
- no promover observaciones automáticamente a conocimiento gobernado;
- evitar una implementación conjunta de mapa, contexto, retrieval, caché y memoria.

**Relaciones**

- `AKS preparado para GraphRAG`;
- `Evidence Acquisition Framework`;
- `Resource Governance Foundation`;
- futura memoria tipada y gobernada;
- futura evaluación de retrieval.

**Próximo paso gobernado**

Evaluar primero un Repository Knowledge Map mínimo como posible salida regenerable de una futura preparación del AKS. Context Lifecycle, retrieval, caché y memoria requieren decisiones y sprints independientes.

---

### IDEA-014 — Complexity Budget Foundation

**Estado:** `aprobada_para_planificacion_futura`

**Intención**

Establecer límites explícitos al crecimiento de infraestructura, contratos, estados, configuración y dependencias para evitar que Malāk aumente su complejidad sin beneficio comprobable.

**Valor esperado**

- prevenir generalización prematura;
- limitar la expansión de contratos públicos;
- hacer visible el coste cognitivo y operativo de cada paquete;
- favorecer soluciones pequeñas, reemplazables y reversibles;
- detectar cuando una propuesta debe dividirse o diferirse;
- impedir que tooling, frameworks o plataformas dicten la arquitectura.

**Dimensiones iniciales**

Cada Implementation Packet podrá declarar:

- dependencias nuevas;
- contratos públicos nuevos;
- estados nuevos;
- claves de configuración nuevas;
- módulos o capas nuevas;
- coste operativo esperado;
- deuda técnica introducida;
- complejidad eliminada;
- alternativa más simple evaluada;
- necesidad de revisión arquitectónica profunda.

**Restricciones**

- no convertir el presupuesto en una métrica rígida o universal;
- no impedir cambios necesarios por un límite numérico arbitrario;
- no crear un subsistema de scoring antes de demostrar necesidad;
- no imponer un lenguaje, framework, plataforma o herramienta;
- toda excepción debe estar justificada y aprobada explícitamente.

**Relaciones**

- `Malāk Validation & Delivery Protocol`;
- `Resource Governance Foundation`;
- `Development Tooling Foundation`;
- revisión arquitectónica y certificación de baseline.

**Próximo paso gobernado**

Incorporar inicialmente el Complexity Budget como sección cualitativa de los Implementation Packets. Evaluar automatización únicamente cuando exista evidencia de utilidad y criterios estables.

---

### IDEA-015 — Segmented Domain Governance Foundation

**Estado:** `aprobada_para_planificacion_futura`

**Intención**

Permitir que Malāk escale hacia múltiples verticales mediante paquetes de dominio subordinados a sus documentos de ley, sin incorporar lógica sectorial al Kernel ni crear constituciones paralelas con autoridad equivalente.

**Principio rector**

> Malāk define las invariantes. El dominio especializa su aplicación. La jurisdicción establece obligaciones. La organización puede imponer restricciones adicionales. Ninguna capa inferior puede ampliar autoridad ni contradecir una capa superior.

**Modelo conceptual**

```text
Constitución Cognitiva y Constitución de Gobernanza
        ↓
Blueprint, ADR y políticas globales
        ↓
Domain Governance Profile
        ↓
Jurisdiction Policy Pack
        ↓
Organization Policy
        ↓
Workflow Policy
        ↓
Autorización y ejecución concretas
```

**Reglas iniciales**

- los permisos efectivos resultan de la intersección de todas las capas aplicables;
- una denegación explícita prevalece sobre una autorización inferior;
- una capa inferior puede restringir, pero no ampliar autoridad;
- las contradicciones normativas materiales producen `DENY` o `HOLD`;
- los Domain Packs no modifican el Kernel;
- cada dominio mantiene conocimiento, políticas, capacidades y assurance separados;
- las obligaciones legales y profesionales se modelan por jurisdicción y vigencia;
- las preferencias del usuario nunca sustituyen una restricción superior.

**Verticales futuros posibles**

- ingeniería y operaciones tecnológicas;
- gobierno de agentes empresariales;
- ciberseguridad defensiva;
- datos y compliance;
- fiscalidad y administración corporativa;
- gobierno e inteligencia institucional;
- salud;
- asistencia personal y seguridad familiar.

**Dependencias**

- documentos de ley vigentes;
- `Security Control Plane Foundation`;
- contratos de autorización y enforcement;
- futura gobernanza de conocimiento, identidad, contexto y auditoría.

**Próximo paso gobernado**

Diseñar en el futuro un contrato mínimo de Domain Pack y una matriz de precedencia normativa. No crear todavía rutas, schemas, contratos públicos ni verticales implementados.

---

### IDEA-016 — Knowledge Intake & Source Governance Foundation

**Estado:** `aprobada_para_planificacion_futura`

**Intención**

Incorporar libros, papers, informes, documentación, páginas web y fuentes internas mediante un proceso gobernado que preserve originales, procedencia, autoridad, licencias, vigencia y capacidad de reconstrucción.

**Principios**

- conservar la fuente original como evidencia inmutable;
- tratar Markdown, texto extraído, embeddings, índices y grafos como proyecciones derivadas y regenerables;
- no convertir un archivo procesado en conocimiento autoritativo por el solo hecho de haber sido ingerido;
- distinguir fuente primaria, fuente secundaria, resumen derivado, hipótesis y decisión;
- registrar autoría humana, asistida por IA, generada por IA, mixta o desconocida cuando pueda determinarse;
- impedir bucles de autocontaminación donde una conclusión generada sea reutilizada como evidencia primaria;
- preferir recuperación gobernada antes que entrenar modelos para memorizar bibliotecas;
- aplicar controles de licencia, acceso, cita, redistribución y retención.

**Componentes conceptuales**

- Source Registry;
- Rights & Licensing Registry;
- Normalization Pipeline;
- Authority & Provenance Model;
- Hybrid Retrieval Index;
- Knowledge Promotion Gate.

**Flujo conceptual**

```text
Fuente original
    → validación legal y técnica
    → extracción normalizada
    → metadatos, autoridad y vigencia
    → segmentación e índices
    → recuperación contextual
    → validación
    → posible promoción gobernada
```

**Dependencias**

- `Evidence Acquisition Framework`;
- futura preparación del AKS;
- políticas de privacidad, licencias y retención;
- assurance de extracción y trazabilidad.

**Próximo paso gobernado**

Definir primero un manifiesto mínimo de fuente y un proceso de promoción. No implementar una biblioteca universal, vector store o GraphRAG por inferencia.

---

### IDEA-017 — External Research & Assurance Review

**Estado:** `aprobada_para_planificacion_futura`

**Intención**

Revisar periódicamente investigaciones, papers, incidentes, system cards, estándares y recomendaciones externas para identificar brechas, validar decisiones de Malāk y proponer mejoras sin adoptar novedades de forma automática.

**Clasificación prevista**

```text
APPLICABLE
PARTIALLY_APPLICABLE
ALREADY_COVERED
NOT_APPLICABLE
REQUIRES_RESEARCH
DEFERRED
BLOCKING
```

**Reglas**

- priorizar fuentes primarias, documentación oficial y papers con metodología verificable;
- tratar redes sociales, foros y publicaciones informales como señales de investigación, no como autoridad;
- comparar cada recomendación contra el Blueprint, las Constituciones, la Gobernanza y la simplicidad del Kernel;
- documentar beneficio, complejidad, riesgos, aplicabilidad, alternativas, validación y rollback;
- no convertir una recomendación externa en sprint, contrato o implementación sin aprobación;
- realizar revisiones antes de nuevas superficies sensibles, después de incidentes relevantes y de forma general periódica.

**Próximo paso gobernado**

Definir una plantilla breve de External Research Review y aplicarla únicamente cuando exista una pregunta o superficie concreta.

---

### IDEA-018 — Malāk Public Presence & Controlled Beta Foundation

**Estado:** `aprobada_para_planificacion_futura`

**Intención**

Preparar una presencia pública verificable de Malāk y una progresión segura desde documentación institucional hasta demostraciones y betas controladas.

**Paquetes conceptuales**

1. Public Documentation Website;
2. Demo Environment Foundation;
3. Load, Stress & Resilience Validation;
4. Controlled External Beta.

**Reglas**

- distinguir públicamente `IMPLEMENTED`, `EXPERIMENTAL`, `PLANNED`, `RESEARCH` y `NOT AVAILABLE`;
- no exponer directamente el Kernel;
- ejecutar pruebas de carga, estrés, duración, picos, resiliencia y degradación antes de una beta;
- exigir identidad, rate limits, aislamiento, auditoría, gestión de secretos, protección contra abuso y kill switch;
- comenzar con beta privada, temporal, limitada y por invitación;
- no utilizar usuarios públicos como sustituto de pruebas sintéticas reproducibles.

**Próximo paso gobernado**

Mantener la web institucional separada de toda exposición operativa. La beta requiere una readiness review independiente y no queda autorizada por esta entrada.

---

### IDEA-019 — Malāk Security Learning, Adversarial Evaluation & Deception Foundation

**Estado:** `aprobada_para_planificacion_futura`

**Intención**

Crear una fundación para aprendizaje de ciberseguridad, evaluación adversarial de agentes, laboratorios autorizados, CTF, gemelos adversariales, honeypots y deception defensiva, preservando aislamiento, legalidad, observación externa y Human in Control.

**Subcapacidades futuras**

- Security Learning Lab con modos aprendiz e instructor;
- CTF y laboratorios deliberadamente vulnerables;
- evaluación externa del comportamiento de agentes;
- extracción de conocimiento defensivo validado;
- Adversarial Twin de Malāk sin autoridad ni secretos reales;
- honeypots, honeynets, honeytokens y datos completamente sintéticos;
- red team y bug bounty progresivos;
- generación de pruebas, reglas de detección y propuestas de hardening.

**Principio de Defensa Activa y Respuesta Gobernada**

> Ante una agresión maliciosa o destructiva contra Malāk, sus componentes, sus datos o su infraestructura autorizada, Malāk podrá detectar, contener, aislar, bloquear, engañar, degradar dentro de fronteras propias, revocar credenciales, cerrar sesiones, activar kill switches, desplegar señuelos, preservar evidencia y coordinar una respuesta defensiva proporcional exclusivamente dentro de infraestructura propia o expresamente autorizada.

> Ningún ataque recibido concede autoridad automática para acceder, alterar, inutilizar o comprometer infraestructura externa. Cualquier acción fuera de fronteras propias o expresamente autorizadas requerirá autoridad legal explícita, atribución validada, alcance definido, supervisión humana competente y una capacidad institucional separada de la operación ordinaria de Malāk.

**Roles conceptuales de contingencia**

- `OWNER_AUTHORITY`: autoridad humana final y revocable;
- `SECURITY_OBSERVER`: observación externa sin autoridad operativa;
- `INCIDENT_COMMANDER`: coordina respuesta dentro del alcance aprobado;
- `CONTAINMENT_OPERATOR`: aplica aislamiento, bloqueo, rotación y cierre;
- `FORENSIC_COLLECTOR`: preserva evidencia sin modificar la escena más de lo necesario;
- `DECEPTION_CONTROLLER`: activa señuelos y redirecciones dentro de infraestructura propia;
- `RECOVERY_OPERATOR`: restaura servicios y verifica integridad;
- `EXTERNAL_RESPONSE_LIAISON`: coordina con proveedores, autoridades o equipos legalmente habilitados.

Ningún rol de agente podrá autoasignarse, elevarse, delegar autoridad superior ni actuar fuera del contexto de seguridad vigente.

**Niveles conceptuales de contingencia**

```text
NORMAL
SUSPICIOUS
CONTAINMENT
CRITICAL_CONTAINMENT
RECOVERY
FORENSIC_REVIEW
```

- `NORMAL`: controles ordinarios;
- `SUSPICIOUS`: observación reforzada y reducción preventiva de privilegios;
- `CONTAINMENT`: aislamiento de sesión, identidad, agente, herramienta o segmento;
- `CRITICAL_CONTAINMENT`: cierre fail-closed, revocación, kill switch y preservación prioritaria;
- `RECOVERY`: restauración desde baseline confiable;
- `FORENSIC_REVIEW`: análisis, lecciones y propuestas sin promoción automática.

La transición de un nivel a otro requiere evidencia verificable, política predefinida y autoridad humana cuando el alcance sea material. La presencia del propietario no convierte una sospecha en atribución confirmada ni concede autoridad ofensiva automática.

**Restricciones**

- no usar datos reales como cebo;
- no conectar honeypots con producción, repositorios, Vault o redes domésticas;
- egress denegado por defecto;
- no perseguir ni comprometer al atacante fuera de la infraestructura controlada;
- no conservar malware operativo fuera de cuarentena aprobada;
- no promover automáticamente técnicas observadas a conocimiento o políticas;
- todo pentest real exige contrato, alcance y autorización explícitos.

**Dependencias**

- `Security Control Plane Foundation`;
- `Sandbox Containment & Evaluation Evidence Foundation`;
- `Owner Security Research Sandbox`;
- identidad, contexto, auditoría, gestión de secretos y respuesta a incidentes.

**Próximo paso gobernado**

Diseñar primero laboratorios locales y un Adversarial Twin sin acceso externo. Honeypots públicos, bug bounty, Tor, malware o interacción activa con actores externos o sistemas fuera del entorno controlado requieren decisiones y readiness reviews independientes.

---

### IDEA-020 — Sovereign Agent Fleet Control & Vertical Scaling

**Estado:** `aprobada_para_planificacion_futura`

**Intención**

Consolidar la visión de Malāk como plano horizontal, soberano y vendor-agnostic para gobernar flotas de agentes especializados, con tecnología como primer vertical y expansión futura mediante Domain Packs.

**Diferenciadores previstos**

- separación entre inteligencia, autoridad y ejecución;
- operación local, híbrida o privada;
- agentes heterogéneos y modelos intercambiables;
- políticas y enforcement externos al modelo;
- observación y evidencia fuera de la zona de confianza del agente;
- sandboxes efímeros;
- mejora mediante propuestas, no automodificación;
- Domain Packs subordinados a documentos de ley;
- auditabilidad y control humano.

**Estrategia de escalado**

```text
Malāk valida su propio comportamiento bajo gobernanza y autoridad humana
        ↓
Engineering Governance
        ↓
Agent Governance / Compliance / Data
        ↓
Cybersecurity defensiva y operación soberana
        ↓
Domain Packs especializados
```

**Próximo paso gobernado**

Mantener tecnología e ingeniería como primer campo de demostración. No aprobar verticales regulados ni estrategia comercial sin expertos del dominio, validación de valor y revisión legal.

---

## Ampliaciones propuestas de ideas existentes

### Ampliación conceptual de IDEA-002 — Controlled Engineering Improvement Loop Foundation

Registrar como componentes futuros posibles, sin aprobación de diseño ni implementación:

- Shadow Mode para comparar decisiones candidatas sin efectos;
- Controlled Experimentation con hipótesis, baseline, métricas, sandbox y rollback;
- Decision Replay e Incident Replay inicialmente sin efectos;
- Capability Benchmarking;
- promoción gobernada de mejoras basada en evidencia reproducible.

Estas capacidades no otorgan autoridad para modificar Malāk, promover conocimiento, cambiar políticas o aplicar resultados automáticamente.

### Ampliación conceptual de IDEA-003 — Resource Governance Foundation

Registrar como componentes futuros posibles:

- presupuestos de ejecución para contexto, tiempo, herramientas, CPU, RAM, VRAM, red y paralelismo;
- perfiles operativos reemplazables y externos al Kernel;
- degradación controlada y visible;
- límites de candidatos de retrieval;
- métricas de consumo por tarea;
- cachés reconstruibles con invalidación explícita.

Ningún agente podrá autoasignarse recursos, ampliar cuotas, evadir límites mediante procesos hijos, paralelismo, colas o reintentos, ni mantener persistencia fuera del alcance aprobado. Toda elevación de presupuesto requerirá política aplicable, evidencia verificable y autorización. El agotamiento de recursos deberá producir degradación segura o cierre fail-closed, con medición y enforcement externos a la zona de confianza del agente.

Los presupuestos no deben depender del hardware actual ni transformar restricciones locales en arquitectura permanente.

### Ampliación conceptual de IDEA-001 — Sandbox Containment & Evaluation Evidence Foundation

Registrar como requisitos futuros:

- ciclo `create → execute → seal evidence → destroy → verify destruction`;
- prohibición de reutilización de sandboxes;
- imágenes base inmutables y manifiestos por ejecución;
- backends intercambiables por sistema operativo con garantías declaradas;
- observador fuera de banda alojado fuera de la zona de confianza del agente;
- canal de telemetría unilateral que el agente no pueda modificar;
- comparación entre informe del agente y conducta observada;
- canary resources, honeytokens y evaluaciones ciegas opcionales;
- invalidación verificable de credenciales, claves, discos y procesos al destruir;
- evidencia canónica basada en efectos observables y no en razonamiento declarado.

### Ampliación conceptual de IDEA-006 — Evidence Acquisition Framework

Registrar como requisitos futuros:

- recuperación interna antes de solicitar Internet;
- detección de brecha temporal y evidencia insuficiente;
- autorización PDP/PEP para búsqueda externa;
- políticas de fuentes por dominio;
- validación de procedencia, autoridad, vigencia, corroboración y conflicto;
- contenido web tratado como datos no confiables;
- protección contra prompt injection y scripts;
- almacenamiento temporal por defecto;
- promoción gobernada de fuentes reutilizables;
- revisión periódica de investigación externa mediante IDEA-017.

### Ampliación conceptual de IDEA-007 — Secure Isolated Access Layer

Registrar perfiles separados para Internet pública, deep web autenticada, servicios onion e investigación de alto riesgo. Cada perfil deberá declarar red, egress, identidad, credenciales, descargas, interacción, TTL, evidencia y destrucción. La navegación directa por dark web permanecerá denegada por defecto y subordinada a finalidad legítima, revisión legal y autorización reforzada.

### Ampliación conceptual de IDEA-010 — Owner Security Research Sandbox

Evolucionar su evaluación hacia IDEA-019, preservando:

- uso educativo y defensivo;
- laboratorios locales y CTF autorizados;
- modo aprendiz e instructor;
- prohibición de objetivos públicos no autorizados;
- evaluación externa del agente;
- incorporación gobernada de aprendizaje defensivo;
- separación total del runtime ordinario y del host.

**Referencia conceptual relacionada**

La ejecución de agentes temporales deberá mantenerse compatible con la referencia:

`docs/project/concepts/GOVERNED_EPHEMERAL_AGENT_EXECUTION_EVIDENCE_REFERENCE.md`

Cuando una misión requiera agentes especializados, cada ejecución deberá poder
recibir únicamente el contexto, herramientas, permisos y recursos necesarios
para su responsabilidad autorizada.

Principios preservados:

```text
temporary agent
+
isolated execution
+
Least Context
+
Least Privilege
+
bounded resources
+
external evidence
+
explicit termination
```

La existencia de una flota o de múltiples modelos no implica que deban
ejecutarse simultáneamente ni que compartan contexto, autoridad o estado.

La política deberá preferir agentes temporales, ejecución secuencial y recursos
cargados bajo demanda salvo que evidencia operacional justifique una estrategia
más compleja.

Esta referencia no autoriza una flota permanente, paralelismo multiagente,
creación libre de agentes ni escalado automático.

### IDEA-021 — Malāk Administrative & Operational CLI Foundation

**Estado:** `capturada`

**Intención**

Crear, cuando Malāk alcance suficiente madurez operativa, una CLI administrativa y operacional que permita al propietario interactuar con el sistema, observar su estado, diagnosticar componentes, ejecutar auditorías, acceder a superficies administrativas controladas y operar capacidades críticas bajo autorización explícita y trazabilidad completa.

La CLI deberá ser una superficie de control gobernada y no un atajo alrededor del Security Control Plane.

**Principio de arquitectura**

La interfaz deberá separar al menos tres planos conceptuales:

```text
MALĀK CLI
   |
   +-- USER
   |    +-- chat
   |    +-- status
   |    +-- info
   |
   +-- ADMIN
   |    +-- doctor
   |    +-- components
   |    +-- audit
   |    +-- metrics
   |    +-- logs
   |    +-- trace
   |    +-- runtime
   |    +-- models
   |    +-- security
   |    +-- sandbox
   |    +-- maintenance
   |
   +-- EMERGENCY
        +-- status
        +-- isolate
        +-- revoke-sessions
        +-- stop-agents
        +-- shutdown
        +-- recovery
```

La separación final de comandos, módulos y procesos deberá definirse durante el diseño; este esquema no aprueba nombres ni contratos públicos.

**Interacción cognitiva inicial**

La CLI deberá poder convertirse en la primera interfaz práctica para el vertical slice operativo de Malāk:

```text
CLI
 -> Kernel
 -> Planner
 -> Capability Registry
 -> Conversation Capability
 -> ConversationService
 -> Provider
 -> LLMRuntime
 -> Response
```

La CLI no deberá reemplazar ni duplicar la lógica cognitiva, de routing o de seguridad de estas capas.

**Diagnóstico y verificación de componentes**

Evaluar comandos futuros equivalentes a:

```text
malak doctor
malak components list
malak components status
malak components check <component>
malak trace <request_id>
```

El diagnóstico podrá verificar, cuando corresponda:

- Kernel;
- Planner;
- Capability Registry;
- Conversation Service;
- Provider Registry;
- runtimes;
- disponibilidad de modelos;
- PDP;
- PEP;
- sinks de auditoría;
- métricas y eventos;
- configuración;
- dependencias críticas;
- conectividad autorizada con Vault o servicios auxiliares.

Los health checks deberán ser deterministas siempre que sea posible y no depender de un LLM para declarar que un componente crítico funciona correctamente.

**Auditorías desde CLI**

Evaluar comandos separados y componibles para:

```text
malak audit architecture
malak audit security
malak audit components
malak audit runtime
malak audit resources
malak audit full
```

`audit full` deberá componer auditorías independientes en lugar de convertirse en un auditor monolítico con autoridad general.

Posibles relaciones:

- Constitutional Assurance para invariantes arquitectónicas;
- Security Control Plane para autorización y enforcement;
- Resource Governance para consumo y límites;
- futuras capas de integridad, identidad y contexto;
- auditorías de componentes y runtime;
- evidencia asociada al commit, baseline o ejecución inspeccionada.

**Administración y operaciones críticas**

Las operaciones privilegiadas no deberán ejecutarse directamente por el hecho de originarse en la CLI del propietario.

Flujo conceptual:

```text
Admin CLI
 -> identidad del propietario
 -> SecurityContext vigente
 -> AuthorizationRequest
 -> PDP
 -> PEP
 -> operación protegida
 -> validación posterior
 -> auditoría
```

Operaciones críticas futuras, como actualizar, reemplazar, reiniciar o restaurar componentes sensibles, deberán evaluar adicionalmente:

- autenticación reforzada y MFA cuando corresponda;
- contexto de seguridad reciente y de corta vida;
- clasificación de riesgo;
- confirmación humana explícita;
- maintenance mode cuando sea necesario;
- checkpoint o backup previo;
- verificación de integridad;
- health check posterior;
- rollback determinista;
- evidencia completa de la operación.

**Niveles conceptuales de riesgo para comandos**

Evaluar una clasificación semejante a:

```text
LEVEL 0 — read-only
LEVEL 1 — safe operational
LEVEL 2 — privileged
LEVEL 3 — critical
LEVEL 4 — emergency
```

La taxonomía concreta deberá diseñarse y aprobarse posteriormente. La existencia de un nivel no concede autoridad por sí misma.

**Security Research Lab desde CLI**

La futura superficie administrativa podrá ofrecer una entrada controlada al `Owner Security Research Sandbox` / `Security Learning Lab`, por ejemplo mediante una familia conceptual `malak lab security`.

El acceso deberá:

- requerir identidad del propietario y autorización reforzada;
- abrir un entorno aislado y separado del runtime ordinario;
- no heredar por defecto Memory, Vault, secretos, repositorios ni credenciales personales;
- mantener egress denegado por defecto salvo perfil expresamente aprobado;
- utilizar targets propios, sintéticos o explícitamente autorizados;
- producir evidencia y reportes separados;
- mantener kill switch y destrucción verificable del entorno.

Posibles operaciones futuras del laboratorio:

```text
lab create
lab list
lab enter
lab destroy
lab scenarios
lab ctf
lab adversarial
lab network-sim
lab evidence
lab report
```

Los nombres anteriores son ilustrativos y no constituyen interfaz aprobada.

**Emergency Control Surface**

Debe evaluarse una ruta administrativa mínima que no dependa del plano cognitivo ni de un LLM para acciones de emergencia.

Ejemplos conceptuales:

```text
malak emergency status
malak emergency isolate
malak emergency revoke-sessions
malak emergency stop-agents
malak emergency shutdown
malak emergency recovery
```

El objetivo es preservar autoridad del propietario aun cuando Planner, modelos, agentes u otras capacidades cognitivas fallen o estén comprometidas.

La ruta de emergencia deberá seguir siendo determinista, auditable, de privilegio mínimo y protegida contra uso accidental o no autorizado.

**Explainability administrativa y trazabilidad**

Evaluar superficies de lectura como:

```text
malak explain decision <request_id>
malak trace <request_id>
```

para reconstruir decisiones de seguridad y rutas operativas usando evidencia ya existente, sin pedir a un LLM que invente o reinterprete la razón de una autorización.

**Restricciones**

- la CLI no modifica directamente el Kernel para facilitar comandos;
- no evita PDP/PEP ni políticas aplicables;
- ser `OWNER_AUTHORITY` no elimina trazabilidad ni validaciones;
- ningún comando crítico se habilita solo porque técnicamente exista;
- no crear una CLI monolítica que concentre inteligencia, autoridad, ejecución y auditoría;
- no introducir el laboratorio dentro del runtime ordinario;
- no habilitar acciones de red, hacking real, malware operativo ni objetivos externos sin las fundaciones y autorizaciones correspondientes;
- la CLI debe ser un adapter y superficie de control, no una nueva fuente de autoridad.

**Dependencias y relaciones**

- First Operational Malāk / cognitive vertical slice;
- `Development Tooling Foundation`;
- `Constitutional Assurance Foundation`;
- `Malāk Validation & Delivery Protocol`;
- `Security Control Plane Foundation`;
- `Secure Context Manager`;
- `Sandbox Containment & Evaluation Evidence Foundation`;
- `Resource Governance Foundation`;
- `Malāk Security Learning, Adversarial Evaluation & Deception Foundation`.

**Secuencia de maduración sugerida**

```text
chat / status
 -> doctor / components / metrics / logs / trace
 -> audit
 -> security / sandbox
 -> admin privileged operations
 -> lab
 -> emergency / recovery
```

Esta secuencia es únicamente una hipótesis de diseño y no constituye roadmap aprobado.

**Próximo paso gobernado**

Revisar esta idea cuando el primer vertical slice operativo de Malāk esté estable y exista evidencia real sobre las necesidades de operación y diagnóstico. Diseñar primero una CLI mínima de lectura e interacción; introducir operaciones privilegiadas solamente después de identidad, contexto, autorización, auditoría y rollback suficientes.

---


### IDEA-022 — Vault Sync Agent Operational CLI & Assurance Interface

**Estado:** `capturada`

**Intención**

Evolucionar la interfaz del `malak-vault-sync-agent` hacia una CLI operacional orientada a observación, diagnóstico, informes, comparación histórica, auditoría, verificación y propuestas gobernadas, sin ampliar su autoridad sobre Malāk ni sobre `main`.

La CLI deberá hacer más accesible el funcionamiento interno y la evidencia del agente, no convertirlo en un agente autónomo con permisos adicionales.

**Áreas funcionales candidatas**

```text
malak-vault-agent
|
+-- status
+-- doctor
+-- health
|
+-- reports
|    +-- list
|    +-- show <id>
|    +-- latest
|    +-- compare <id-a> <id-b>
|    +-- export <id>
|
+-- audit
|    +-- vault
|    +-- agent
|    +-- consistency
|    +-- integrity
|    +-- full
|
+-- diff
|    +-- repo-vault
|    +-- current-baseline
|    +-- since <commit-or-run>
|
+-- verify
|    +-- state
|    +-- hashes
|    +-- snapshots
|    +-- authority
|    +-- permissions
|
+-- sync
|    +-- dry-run
|    +-- propose
|    +-- status
|
+-- history
|    +-- runs
|    +-- proposals
|    +-- reconciliations
|    +-- failures
|
+-- diagnostics
     +-- config
     +-- git
     +-- vault-paths
     +-- permissions
```

Los nombres y jerarquías son conceptuales y deberán validarse contra la CLI y contratos reales del agente antes de cualquier implementación.

**Informes y comparación histórica**

La CLI deberá permitir consultar informes recientes y antiguos y comparar ejecuciones o estados verificables.

Posibles dimensiones de comparación:

- baseline inspeccionado;
- commit de Malāk;
- commit del Vault;
- run ID;
- hallazgos nuevos;
- hallazgos resueltos;
- referencias rotas;
- drift documental;
- conflictos de autoridad;
- cambios no reconciliados;
- errores de integridad;
- duración;
- resultado de validaciones;
- versión del agente y schema utilizado.

La comparación deberá basarse en datos estructurados y reproducibles cuando existan, no en resúmenes narrativos como única evidencia.

**Auditorías del Vault y del agente**

Evaluar auditorías independientes para:

- integridad del Vault;
- consistencia repo ↔ Vault;
- snapshots históricos e inmutabilidad;
- autoridad documental;
- estado persistente del agente;
- configuración;
- rutas locales autorizadas;
- permisos;
- identidad del repositorio remoto;
- límites de comandos Git;
- hashes y evidencia;
- propuestas pendientes y reconciliación humana;
- cumplimiento de las fronteras que impiden modificar Malāk o aprobar/mergear PRs.

Un comando conceptual `audit full` podrá orquestar estos chequeos, pero no deberá fusionar sus responsabilidades ni ocultar cuál control produjo cada hallazgo.

**Doctor y health checks**

Evaluar un `doctor` determinista para comprobar:

- configuración válida;
- acceso esperado a repositorios;
- rama base correcta;
- estado del Vault;
- state schema compatible;
- lock de ejecución;
- backups del state cuando correspondan;
- integridad de rutas;
- Git disponible y comandos permitidos;
- capacidad de producir evidencia;
- ausencia de permisos inesperados.

Los diagnósticos deberán distinguir claramente `PASS`, `WARN`, `FAIL` y `NOT_APPLICABLE` o equivalentes cuando sea útil.

**Sync y propuestas**

Preservar la separación entre:

```text
observe
 -> compare
 -> validate
 -> propose
 -> human review
 -> human merge / reconciliation
```

La CLI podrá simplificar la ejecución de `dry-run`, generación de propuestas y consulta de estado, pero no deberá:

- escribir directamente sobre `main`;
- mergear PRs;
- aceptar sus propias propuestas;
- modificar Malāk;
- alterar snapshots históricos;
- ignorar un estado pendiente de reconciliación humana;
- ejecutar auto-fix generalizado.

**Trazabilidad**

Cada operación que cambie estado del agente o genere una propuesta deberá conservar, según el diseño aprobado:

- run ID;
- timestamps UTC;
- commits origen/destino;
- versión del agente;
- configuración relevante no sensible;
- comandos ejecutados o acciones normalizadas;
- hashes aplicables;
- resultado;
- findings;
- errores;
- vínculo con propuesta o PR cuando exista.

**Relación con assurance futuro**

La CLI podrá ser una superficie útil para futuros dominios de assurance, pero el agente del Vault no deberá convertirse por expansión incremental en un auditor universal de Malāk.

Separar conceptualmente:

```text
Vault Sync Domain
External Assurance Domain
Malāk Runtime / Security Domain
```

Si en el futuro existe un auditor externo de arquitectura o seguridad, su autoridad, identidad, sandbox, permisos y evidencias deberán diseñarse por separado.

**Restricciones**

- CLI como adapter, no como nueva fuente de autoridad;
- no LLM requerido para decisiones operativas del agente;
- tipado y schemas estables cuando se formalice la interfaz;
- exit codes claros;
- `dry-run` real para operaciones que lo permitan;
- idempotencia donde corresponda;
- fail-closed;
- allowlists de comandos y rutas;
- redacción de secretos;
- logs estructurados;
- ningún `automerge`;
- ningún `auto-fix` general;
- no reutilizar la CLI para ampliar implícitamente permisos del agente.

**Dependencias y relaciones**

- baseline real de `malak-vault-sync-agent`;
- `Malāk Validation & Delivery Protocol`;
- `Development Tooling Foundation` cuando aplique al agente;
- `Constitutional Assurance Foundation` para invariantes de autoridad;
- Project Context & Knowledge Governance Foundation;
- futuras capacidades de External Assurance, si son aprobadas por separado.

**Próximo paso gobernado**

Antes de diseñar comandos finales, inspeccionar el estado vigente de `malak-vault-sync-agent`, identificar qué capacidades ya existen, qué informes y state schemas son reales y qué necesidades operativas aparecen durante el uso. Implementar primero operaciones de lectura, diagnóstico y comparación; mantener sync/proposals dentro de las fronteras de autoridad actuales.

---


### IDEA-023 — Governed Engineering Collaboration & Voice Interface Foundation

**Estado:** `aprobada_para_planificacion_futura`

**Intención**

Permitir que el propietario utilice Malāk como colaborador técnico para desarrollar, revisar y operar el propio proyecto Malāk mediante sesiones de ingeniería gobernadas, debate técnico basado en evidencia, preparación de cambios, ejecución controlada en sandbox y, en una fase posterior, interacción por voz en tiempo real.

La iniciativa no convierte a Malāk en un sistema de auto-modificación. Malāk podrá observar, analizar, debatir, proponer, preparar y ejecutar trabajos expresamente autorizados dentro de límites definidos, pero la autoridad para aprobar cambios críticos, integrar modificaciones y alterar el baseline permanecerá bajo control humano.

**Principio rector**

> Malāk puede participar en el desarrollo de Malāk sin adquirir autoridad para autodesarrollarse.

> La voz, la CLI o una futura GUI son superficies de interacción; ninguna de ellas constituye por sí misma autoridad.

> Una conversación puede originar una intención o propuesta. La ejecución requiere contratos, alcance, autorización y evidencia independientes de la modalidad de entrada.

**Valor esperado**

- permitir sesiones técnicas naturales entre el propietario y Malāk;
- debatir decisiones arquitectónicas y de implementación utilizando repositorio, AKS, baseline, tests, métricas y evidencia disponible;
- reducir fricción entre análisis, propuesta, validación y ejecución controlada;
- permitir que Malāk prepare Implementation Packets y alternativas técnicas sin autoaprobarlas;
- ejecutar trabajos autorizados en sandbox y presentar resultados verificables en tiempo real;
- habilitar interacción por voz sin crear una arquitectura paralela al CLI o a futuras interfaces gráficas;
- convertir el desarrollo de Malāk en un caso de uso real para validar sus propias capacidades de ingeniería y gobernanza.

### Modelo de interacción gobernada

La interacción deberá preservar una secuencia explícita similar a:

```text
DISCUSS / ANALYZE
        ↓
PROPOSE
        ↓
REVIEW
        ↓
AUTHORIZE
        ↓
EXECUTE
        ↓
VALIDATE
        ↓
REPORT
```

Una frase conversacional no deberá convertirse directamente en una operación irreversible.

Ejemplos conceptuales de intención:

```text
"explicame"        → READ / EXPLAIN
"analiza"          → READ + EVALUATE
"propone"          → CREATE PROPOSAL
"prepara el cambio"→ PREPARE IN SANDBOX
"ejecutalo"        → AUTHORIZATION REQUIRED
"integralo"        → DEEP REVIEW + OWNER AUTHORITY
```

La clasificación exacta no debe depender exclusivamente de palabras clave. Malāk deberá presentar de forma clara la operación estructurada que entiende que está siendo solicitada cuando exista impacto material.

### Engineering Session

Evaluar un futuro concepto de `EngineeringSession` como contexto temporal y gobernado para trabajos de desarrollo.

Una sesión podría contener, como mínimo:

```text
EngineeringSession
├─ session_id
├─ repository
├─ baseline
├─ branch / workspace
├─ objective
├─ approved_scope
├─ active_packet
├─ evidence_refs
├─ validations
├─ decisions
├─ risks
└─ pending_actions
```

Este contexto no debe convertirse en memoria ilimitada ni reemplazar documentos oficiales, Git o el AKS. Debe ser temporal, trazable y cerrarse produciendo un resumen verificable de la sesión.

Un cierre de sesión podría generar un `Engineering Session Report` con:

- objetivo;
- decisiones tomadas;
- cambios preparados o ejecutados;
- archivos afectados;
- pruebas y validaciones;
- riesgos observados;
- desviaciones de alcance;
- rollback disponible;
- baseline y HEAD evaluados;
- trabajo pendiente.

### Debate técnico basado en evidencia

Malāk deberá poder cuestionar propuestas del propietario o propias cuando la evidencia indique una alternativa mejor.

No se considera comportamiento correcto limitarse a confirmar una idea por deferencia al usuario. Una revisión técnica futura podrá considerar, entre otros:

- Blueprint y documentos de ley;
- arquitectura vigente;
- contratos públicos;
- dependencias;
- tests;
- telemetría y benchmarks;
- Security Control Plane;
- Complexity Budget;
- Resource Governance;
- historial de ADR, decisiones y propuestas previas.

Un desacuerdo deberá expresarse mediante razones técnicas verificables y, cuando sea posible, alternativas más simples o seguras.

### Evaluadores independientes

Para decisiones relevantes podrá evaluarse en el futuro el uso de verificadores o evaluadores especializados para aspectos como:

- arquitectura;
- seguridad;
- complejidad;
- recursos;
- calidad y pruebas.

No deberán convertirse automáticamente en una flota de agentes conversando entre sí. Siempre que sea posible se preferirán validaciones deterministas, tests, reglas y evaluadores pequeños y especializados.

Los desacuerdos deberán consolidarse en evidencia legible para el propietario. Ningún evaluador podrá autorizar por sí mismo una modificación crítica.

### Ejecución en tiempo real

"Tiempo real" significa observabilidad interactiva del trabajo, no ejecución sin control.

Una futura sesión podría exponer eventos como:

```text
Blueprint reviewed                  PASS
Baseline tests                      PASS
Sandbox created                     PASS
Packet applied                      PASS
Targeted tests                      PASS
Architecture checks                 PASS
Security checks                     PASS
```

El propietario deberá poder pausar o cancelar una operación cuando el backend lo permita.

Un `OWNER STOP`, revocación válida o kill switch deberá tener prioridad sobre cualquier objetivo de la sesión. El mecanismo de detención para operaciones sensibles no debe depender de que el LLM coopere.

### Voz como adapter de entrada

La interfaz por voz deberá implementarse como otro adapter de entrada hacia los mismos contratos y límites operativos, no como un subsistema cognitivo independiente.

Modelo conceptual:

```text
CLI ────┐
        │
VOICE ──┼──► Application Boundary ─► Malāk
        │
GUI ────┘
```

Una posible ruta futura de voz sería:

```text
Audio
  ↓
Speech-to-Text
  ↓
Conversation / Intent Boundary
  ↓
Planner / Engineering Request
  ↓
Governance / Authorization
  ↓
Execution when applicable
```

La autenticación, autorización, contexto de seguridad, permisos y auditoría deberán ser equivalentes independientemente de si la solicitud se origina mediante voz, CLI o GUI.

La voz nunca deberá interpretarse como una credencial suficiente ni como autorización implícita para operaciones privilegiadas.

### Integración con el flujo de desarrollo

La visión futura es permitir un ciclo como:

```text
Owner
  ↓
Malāk
  ↓
Repository + AKS + Evidence
  ↓
Engineering Proposal
  ↓
Human Review
  ↓
Implementation Packet
  ↓
Sandbox execution
  ↓
Tests + Evidence
  ↓
Owner Review
  ↓
Governed integration
```

Malāk podrá ayudar a preparar cambios, pero no deberá:

- aprobar sus propias propuestas;
- ampliar su propio alcance;
- modificar documentos de ley por inferencia;
- fusionar cambios críticos sin autoridad explícita;
- ocultar desviaciones entre alcance aprobado y diff real;
- convertir una ejecución satisfactoria en autorización permanente.

### Relación con la CLI de Malāk

IDEA-023 se relaciona con IDEA-021, pero no obliga a implementarse simultáneamente.

Una progresión candidata sería:

```text
malak chat
    ↓
status / doctor / trace
    ↓
engineering inspect / discuss / propose
    ↓
engineering prepare
    ↓
engineering run <approved-packet>
    ↓
voice adapter sobre los mismos contratos
```

La sintaxis es conceptual y no constituye contrato aprobado.

### Dependencias y relaciones

- IDEA-001 — Sandbox Containment & Evaluation Evidence Foundation;
- IDEA-002 — Controlled Engineering Improvement Loop Foundation;
- IDEA-005 — Secure Context Manager;
- IDEA-009 — Development Tooling Foundation;
- IDEA-011 — Malāk Validation & Delivery Protocol;
- IDEA-012 — Constitutional Assurance Foundation;
- IDEA-014 — Complexity Budget Foundation;
- IDEA-021 — Malāk Administrative & Operational CLI Foundation;
- Security Control Plane Foundation;
- futuro baseline operativo end-to-end;
- AKS y Project Context cuando exista evidencia suficiente para su uso real.

### Restricciones contra sobreingeniería

Esta iniciativa no autoriza crear de inmediato:

- un subsistema completo de voz;
- un `EngineeringSessionManager` sin necesidad real;
- una flota de agentes evaluadores;
- un motor genérico de workflows;
- un sistema de auto-programación;
- múltiples capas de abstracción para soportar interfaces todavía inexistentes.

La implementación deberá seguir el `Necessity & Complexity Review` y crecer únicamente cuando el flujo operativo real de Malāk demuestre la necesidad.

La voz debería incorporarse después de que el flujo equivalente funcione correctamente mediante una interfaz textual. Primero deben estabilizarse contratos, autorización, trazabilidad y ejecución; después se añade el adapter de voz.

### Próximo paso gobernado

Mantener la iniciativa como planificación futura. Cuando Malāk disponga de un primer vertical slice operativo, tooling reproducible, Constitutional Assurance y suficiente observabilidad, evaluar si la capacidad de colaboración de ingeniería debe introducirse mediante varios incrementos pequeños o mediante un sprint dedicado.

La decisión sobre número de sprint, alcance exacto y contratos se realizará únicamente tras inspeccionar el baseline vigente y demostrar una necesidad operacional concreta.


### IDEA-024 — Governed Agent Composition & Mission Orchestration Foundation

**Estado:** `capturada`

**Intención**

Diseñar una fundación futura para componer agentes temporales especializados y coordinar misiones complejas mediante responsabilidades, competencias, capacidades, contratos, evidencia y límites de autoridad explícitos.

La iniciativa busca evitar que un agente sea únicamente un prompt o personalidad generada libremente por un LLM. La composición de un agente deberá derivarse de conocimiento gobernado, capacidades disponibles, contexto autorizado, herramientas permitidas, criterios verificables y evidencia operacional.

**Principios rectores**

> Un agente no es un prompt. El prompt es solamente una representación temporal de una definición de agente gobernada.

> Competencia no implica autoridad.

> Los agentes pueden proponer, construir, revisar y corregir; la evidencia valida, la política autoriza y la orquestación coordina.

> Compartir infraestructura no implica compartir confianza.

> El Kernel gobierna el sistema; la orquestación de misión coordina únicamente una misión acotada.

**Valor esperado**

- permitir especialización sin crear agentes permanentes innecesarios;
- componer agentes según las necesidades reales de cada tarea;
- coordinar trabajos complejos mediante subtareas y dependencias explícitas;
- separar construcción, revisión, ejecución y validación;
- reducir prompts monolíticos y conversaciones multiagente no estructuradas;
- mejorar trazabilidad y reproducibilidad;
- reutilizar las fundaciones existentes de seguridad, modelos, conocimiento, recursos, sandbox y validación;
- permitir misiones complejas sin introducir lógica agentic dentro del Kernel.

**Modelo conceptual de composición**

```text
Task / Mission
      ↓
Required competencies
      ↓
Required skills
      ↓
Profession / specialization
      ↓
Capabilities
      ↓
Tools
      ↓
Security scope
      ↓
Model selection
      ↓
Context compilation
      ↓
Temporary Agent Instance
```

`Skill`, `Profession` y estructuras equivalentes deberán derivarse de Knowledge Artifacts gobernados y no constituir una fuente de autoridad paralela al AKS.

Una profesión describe competencia y responsabilidad. Los permisos efectivos deberán continuar derivándose exclusivamente de identidad, contexto de seguridad, políticas y autorización.

**Mission Orchestration**

Evaluar una futura capacidad de `Mission Orchestration` para coordinar misiones que justifiquen más de un agente o etapa especializada.

Flujo conceptual:

```text
Kernel / Planning
        ↓
Mission Orchestration Capability
        ↓
Mission Controller
        ↓
Mission Graph
   ┌────┼────┐
   ↓    ↓    ↓
Agent A Agent B Agent C
   └────┼────┘
        ↓
Execution Requests
        ↓
Security Control Plane
        ↓
Workers / Sandbox
        ↓
Evidence
        ↓
Independent Validation
```

Un futuro `Mission Controller` podrá administrar únicamente el lifecycle de una misión ya admitida y autorizada.

Podrá coordinar:

- subtareas;
- dependencias;
- estados;
- agentes temporales;
- artefactos;
- solicitudes de revisión;
- criterios de finalización;
- límites de iteración;
- repair loops acotados;
- bloqueos y necesidad de intervención humana.

No podrá:

- sustituir al Kernel;
- sustituir al Planning Engine global;
- concederse permisos;
- conceder permisos a agentes;
- modificar políticas;
- decidir autorizaciones;
- ejecutar directamente operaciones protegidas;
- alterar documentos fundacionales;
- ampliar presupuestos de recursos;
- aprobar sus propias excepciones;
- declarar éxito sin evidencia suficiente.

**Task, Output & Completion Contracts**

Las misiones futuras podrán utilizar contratos explícitos que definan, según corresponda:

- objetivo;
- alcance;
- inputs;
- outputs;
- artefactos afectados;
- restricciones;
- dependencias;
- herramientas permitidas;
- riesgos;
- criterios de calidad;
- evidencia requerida;
- criterios de finalización;
- límites de tiempo, recursos e iteraciones.

Principio:

> Una misión no termina porque un agente declare que terminó; termina cuando sus criterios de finalización pueden demostrarse mediante evidencia autorizada.

**Structured Agent Communication**

La comunicación entre agentes deberá ser preferentemente estructurada, limitada y auditable.

Ejemplos conceptuales de mensajes futuros:

```text
task_assignment
artifact_ready
review_request
review_result
finding
repair_request
validation_result
blocked
needs_owner_decision
```

Las conversaciones libres entre agentes no deberán convertirse en mecanismo principal de coordinación cuando contratos, eventos o artefactos estructurados resulten suficientes.

**Structured Deliberation**

Cuando una decisión realmente justifique múltiples perspectivas, podrá evaluarse deliberación estructurada mediante funciones como:

```text
Proposal
   ↓
Critique
   ↓
Evidence
   ↓
Revision
   ↓
Independent Validation
```

Deberán existir límites explícitos de rondas, recursos y criterios de parada.

Principio:

> Debate < Evidence.

El consenso entre agentes no constituye prueba de corrección.

Siempre que produzca calidad equivalente deberá preferirse:

```text
deterministic check
        >
small specialized evaluator
        >
multi-agent deliberation
```

**Builder / Reviewer Separation**

Cuando el riesgo o impacto lo justifique, el productor de un artefacto no deberá ser su único evaluador.

Patrón conceptual:

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

Los roles podrán compartir conocimiento o infraestructura según política, pero no deberán compartir autoridad automáticamente.

**Evaluación gobernada de candidatos**

Cuando una misión produzca uno o más resultados candidatos, la composición
agentic no deberá convertirlos directamente en una propuesta final mediante
score, consenso o mayoría.

La evaluación deberá distinguir entre:

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

Solo los candidatos VALID podrán ingresar a una etapa posterior de comparación
o ranking.

Reglas preservadas:

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

El score podrá utilizarse únicamente como mecanismo comparativo entre candidatos
válidos.

Principios:

Score != Truth
Score != Safety
Score != Evidence
Score != Authority
Score != Governance

Una puntuación alta no podrá compensar:

una violación de Gobernanza;
una violación constitucional;
una violación arquitectónica crítica;
un fallo de seguridad;
evidencia insuficiente;
una contradicción no resuelta;
una desviación material respecto de la specification;
ausencia de evidencia reproducible cuando ésta sea requerida.

La comparación de candidatos deberá considerar, cuando corresponda:

cumplimiento de specification;
arquitectura;
seguridad;
evidencia disponible;
resultados de tests;
comportamiento empírico;
consumo de recursos;
complejidad;
mantenibilidad;
reversibilidad;
findings abiertos;
incertidumbre residual.

El ranking deberá producir una preferencia entre candidatos válidos, no una
declaración automática de verdad.

Ejemplo conceptual:

Candidate A
Architecture: PASS
Security: PASS
Evidence: SUFFICIENT
Status: VALID
Score: 87

Candidate B
Architecture: PASS
Security: FAIL
Evidence: SUFFICIENT
Status: INVALID
Raw score: 96

Candidate C
Architecture: PASS
Security: PASS
Evidence: SUFFICIENT
Status: VALID
Score: 91

Resultado:

Candidate B
→ excluded from ranking

Candidate C
→ ranked #1

Candidate A
→ ranked #2

No:

Candidate B wins because 96 > 91

Cuando la evidencia sea insuficiente o existan contradicciones relevantes que no
puedan resolverse, el sistema deberá poder conservar un estado equivalente a:

INCONCLUSIVE

sin forzar una selección.

La existencia de múltiples candidatos tampoco obliga a elegir uno.

Una misión podrá finalizar solicitando:

more evidence
additional validation
new experiment
owner decision

cuando la evidencia disponible no justifique una recomendación suficientemente
fundada.

El resultado del ranking deberá permanecer en estado de candidato o propuesta.

No podrá autorizar por sí mismo:

ejecución protegida;
modificación de código;
modificación de documentos normativos;
merge;
deploy;
modificación del baseline;
ampliación de permisos;
modificación de políticas;
modificación de Gobernanza;
creación de autoridad permanente.

Flujo conceptual:

Candidates
    ↓
Independent Validation
    ↓
Candidate Validity
    ↓
VALID candidates only
    ↓
Score / Ranking
    ↓
Recommended Candidate
    ↓
Proposal
    ↓
Human / Applicable Governance

El mecanismo de evaluación deberá preservar separación entre:

Author
!=
Observer
!=
Reviewer
!=
Validator
!=
Authority

La evidencia utilizada para validar o comparar candidatos no deberá depender
exclusivamente de la explicación generada por los agentes productores.

Cuando corresponda deberá provenir de fuentes como:

tests;
análisis estático;
arquitectura;
Security Control Plane;
sandbox;
telemetría;
benchmarks;
hashes;
logs;
observadores externos;
evaluadores independientes;
evidencia reproducible.

Principio:

**El agente produce un candidato; la evidencia determina si puede considerarse
válido; el ranking compara únicamente candidatos válidos; la Gobernanza decide
qué puede convertirse en acción.**

La evaluación deberá mantenerse compatible con la referencia conceptual:

`docs/project/concepts/GOVERNED_EPHEMERAL_AGENT_EXECUTION_EVIDENCE_REFERENCE.md`

Esta referencia no aprueba actualmente:

algoritmo de scoring;
fórmula de ponderación;
thresholds;
cantidad de candidatos;
cantidad de agentes;
sistema de votación;
majority voting;
selección automática irreversible;
modelo específico como evaluator;
ejecución paralela por defecto.

Estos mecanismos deberán diseñarse posteriormente a partir de evidencia,
restricciones reales y el baseline vigente.

**Artifact Workspace**

Las misiones podrán utilizar un workspace controlado para intercambiar artefactos sin transportar grandes volúmenes de código, documentos o evidencia mediante contexto LLM.

Los artefactos deberán poder conservar, cuando corresponda:

- identidad;
- versión;
- productor;
- consumidores;
- provenance;
- hashes;
- estado de validación;
- relación con la misión.

El acceso deberá permanecer limitado por identidad, scope, operación y política.

**Repair Loop**

Podrán existir ciclos acotados de:

```text
Build
  ↓
Execute
  ↓
Test
  ↓
Findings
  ↓
Repair
  ↓
Regression
  ↓
Validation
```

Todo repair loop deberá establecer límites de iteraciones, tiempo, recursos, errores repetidos, desviaciones arquitectónicas y condiciones de intervención humana.

Una misión deberá poder finalizar en estados equivalentes a:

```text
completed
failed
blocked
needs_owner_decision
```

en lugar de continuar indefinidamente.

**Fronteras de responsabilidad**

IDEA-024 coordina y consume capacidades existentes o futuras; no adquiere propiedad sobre ellas.

```text
Agent lifecycle / coordination
    → Agent Manager y diseño agentic aprobado

Authorization / enforcement
    → Security Control Plane

Sandbox guarantees
    → IDEA-001

Controlled improvement
    → IDEA-002

Resource budgets
    → IDEA-003

Model governance / assessment
    → IDEA-004

Security contexts
    → IDEA-005

External evidence
    → IDEA-006

Knowledge authority
    → AKS / Knowledge Governance

Context efficiency
    → IDEA-013

Engineering collaboration
    → IDEA-023
```

Cuando una responsabilidad ya posea dueño arquitectónico, Mission Orchestration deberá consumirla mediante contratos y no reimplementarla.

**Seguridad y autoridad**

Toda futura ejecución agentic deberá preservar:

- Human in Control;
- Zero Trust interno;
- Defense in Depth;
- deny by default;
- least privilege;
- identidad independiente cuando corresponda;
- separación entre solicitud, autorización, enforcement, ejecución y validación;
- auditoría;
- scopes limitados;
- contextos de seguridad de vida limitada cuando existan;
- protección de evidencia;
- ausencia de autoelevación;
- ausencia de modificación autónoma de políticas;
- ausencia de modificación autónoma de documentos fundacionales.

Ruta conceptual obligatoria para operaciones protegidas:

```text
Agent / Mission Controller
        ↓
AuthorizationRequest
        ↓
Security Control Plane
        ↓
PDP
        ↓
PEP
        ↓
Protected Operation
        ↓
Worker / Sandbox
        ↓
Evidence
```

La profesión, skill, modelo o rol de un agente nunca constituirá autorización.

**Resource Governance**

La composición multiagente deberá respetar proporcionalidad y eficiencia.

Se deberá preferir:

- agentes temporales;
- modelos cargados bajo demanda;
- un solo modelo generativo pesado en VRAM por defecto cuando sea viable;
- ejecución secuencial antes que paralela salvo evidencia de beneficio;
- contextos mínimos;
- intercambio mediante artefactos;
- límites de iteración y herramientas;
- liberación explícita de recursos;
- degradación controlada.

No deberá crearse un equipo de agentes cuando un procedimiento determinista, una herramienta o un único agente pueda resolver la tarea con calidad equivalente.

**Relaciones principales**

- IDEA-001 — Sandbox Containment & Evaluation Evidence Foundation;
- IDEA-002 — Controlled Engineering Improvement Loop Foundation;
- IDEA-003 — Resource Governance Foundation;
- IDEA-004 — Model Governance & AI Preservation Foundation;
- IDEA-005 — Secure Context Manager;
- IDEA-006 — Evidence Acquisition Framework;
- IDEA-011 — Malāk Validation & Delivery Protocol;
- IDEA-012 — Constitutional Assurance Foundation;
- IDEA-013 — Knowledge and Context Efficiency Foundation;
- IDEA-014 — Complexity Budget Foundation;
- IDEA-020 — Sovereign Agent Fleet Control & Vertical Scaling;
- IDEA-023 — Governed Engineering Collaboration & Voice Interface Foundation;
- Capability Registry;
- Agent Manager;
- AKS;
- Security Control Plane Foundation.

Relación conceptual principal:

```text
IDEA-020
    WHAT:
    visión de agentes y flota soberana

IDEA-024
    HOW:
    composición y coordinación gobernada
    de misiones concretas
```

IDEA-024 no reemplaza ni absorbe IDEA-020.

**Restricciones contra sobreingeniería**

Esta idea no autoriza:

- implementar agentes ahora;
- crear agentes permanentes;
- crear un segundo Kernel;
- crear un segundo Planner;
- crear un sistema alternativo de autorización;
- implementar un Mission Controller inmediatamente;
- implementar Skill Registry o Profession Registry inmediatamente;
- crear un router de modelos exclusivo para agentes;
- crear un sandbox propio independiente de IDEA-001;
- implementar deliberación multiagente por defecto;
- crear nuevos contratos públicos sin necesidad demostrada;
- introducir GraphRAG;
- incorporar modelos frontier;
- permitir acceso libre a Internet;
- modificar Blueprint, Constituciones o Gobernanza;
- modificar el roadmap;
- aprobar un nuevo sprint.

La coordinación puede conectar responsabilidades sin convertirse en propietaria de todas ellas.

**Dependencias**

Antes de diseñar esta fundación en detalle deberán existir suficiente madurez y evidencia en:

- Security Control Plane;
- sandbox y evidencia;
- Resource Governance;
- Model Governance;
- AKS / Knowledge Governance;
- validación independiente;
- métricas operacionales;
- contratos básicos de capabilities y ejecución.

**Próximo paso gobernado**

Conservar IDEA-024 como propuesta no normativa.

Cuando las fundaciones previas estén suficientemente maduras, realizar una evaluación arquitectónica específica que:

1. inspeccione el baseline vigente;
2. determine qué responsabilidades existentes pueden reutilizarse;
3. contraste el diseño con Blueprint, Constitución Cognitiva y Constitución de Gobernanza;
4. delimite Agent Manager, Planning y Mission Controller;
5. identifique los contratos mínimos realmente necesarios;
6. evalúe amenazas derivadas de composición y comunicación multiagente;
7. mida el coste frente a alternativas más simples;
8. diseñe, solo si existe necesidad demostrada, un vertical slice pequeño y reversible;
9. defina evidencia de éxito y rollback;
10. requiera aprobación independiente antes de cualquier promoción al roadmap.

No asumir que todas las capacidades descritas deban implementarse juntas.

---


### Ampliacion conceptual de IDEA-019 — Incident Evidence, Attack Path Reconstruction & Security Regression Learning

Registrar como requisitos futuros de `Malak Security Learning, Adversarial Evaluation & Deception Foundation`, sin aprobar diseno detallado ni implementacion:

**Evidencia de incidente y atribucion tecnica limitada**

- conservar por incidente un identificador estable y una linea temporal correlacionable;
- registrar la direccion IP de origen observada cuando tecnicamente este disponible;
- tratar toda IP, ASN, fingerprint, dominio, hash, user-agent u otro indicador como evidencia tecnica observada y no como identidad confirmada del atacante;
- distinguir explicitamente `source_indicator`, `confidence` y `attribution_status`;
- evitar atribucion automatica a una persona, grupo, organizacion, institucion o Estado a partir de una IP o indicador aislado;
- conservar `first_seen`, `last_seen`, timestamps UTC, origen del dato y metodo de observacion;
- aplicar retencion, minimizacion y proteccion de datos segun sensibilidad y finalidad forense;
- no almacenar secretos, credenciales, tokens o payloads sensibles completos salvo que exista un protocolo forense expresamente aprobado que lo justifique.

**Reconstruccion del camino del ataque**

El analisis forense debera poder reconstruir, con evidencia verificable y sin depender del relato del componente comprometido:

- punto de entrada observado;
- servicios, endpoints, sesiones, identidades, agentes, capabilities, herramientas y componentes alcanzados;
- secuencia temporal de movimientos laterales o transiciones entre zonas de confianza;
- permisos solicitados y decisiones PDP/PEP relacionadas cuando existan;
- operaciones intentadas, permitidas, denegadas o incompletas;
- procesos, herramientas, patrones, hashes, protocolos y tecnicas observables cuando puedan determinarse de manera defensiva;
- recursos sensibles alcanzados o intentados;
- momento y componente que detecto el comportamiento anomalo;
- momento y mecanismo de contencion, aislamiento, revocacion, bloqueo o deception;
- evidencia de que la contencion fue efectiva y de que no persiste acceso residual conocido.

**Expected Containment Point vs Actual Detection Point**

Para cada incidente relevante se debera comparar:

```text
camino esperado por arquitectura y politicas
        vs
camino realmente observado
```

El informe debera identificar:

- donde debio bloquearse el ataque;
- donde fue detectado realmente;
- que frontera, control o invariante no funciono como se esperaba;
- si existio movimiento lateral innecesario;
- si una identidad, sesion, capability o componente mantuvo privilegios excesivos;
- si la deteccion o contencion fue tardia;
- si el atacante alcanzo una zona que deberia haber sido inaccesible.

La diferencia entre el punto de contencion esperado y el punto de deteccion real se tratara como evidencia de un posible `security gap`, no como prueba automatica de vulnerabilidad hasta completar revision tecnica.

**Incident Evidence Package**

Evaluar un artefacto forense estructurado y verificable que pueda contener, segun aplicabilidad:

```text
incident_id
metadata
network_observations
source_indicators
session_events
authorization_events
component_events
tool_and_process_observations
containment_actions
deception_events
integrity_hashes
timeline
affected_assets
expected_controls
observed_controls
failed_or_bypassed_controls
forensic_findings
recovery_evidence
```

Los artefactos relevantes deberan poder vincularse mediante timestamps UTC, correlation IDs, hashes, fuente de evidencia y nivel de confianza. La evidencia canonica debera provenir de planos de control, observadores externos, logs, auditoria, sandbox, red u otros efectos observables; ninguna explicacion generada por un LLM o agente comprometido sera suficiente por si sola.

**Indicators of Compromise / Security Observations**

Evaluar un registro defensivo separado para indicadores y observaciones como:

- IPs;
- ASN o metadatos de red;
- dominios;
- hashes;
- fingerprints TLS/cliente cuando correspondan;
- user-agents;
- patrones de autenticacion;
- identificadores de credencial o token sin conservar el secreto;
- firmas de procesos o herramientas;
- patrones de comportamiento;
- anomalias de protocolo.

Los indicadores deberan tener estado y confianza, por ejemplo:

```text
OBSERVED
CORRELATED
SUSPICIOUS
CONFIRMED_MALICIOUS
EXPIRED
FALSE_POSITIVE
```

Una IP o indicador no debera convertirse automaticamente en una blacklist permanente. Los bloqueos, restricciones o aumento de escrutinio deberan considerar vigencia, repeticion, confianza, politica aplicable y TTL cuando corresponda.

**Deception y desvio defensivo**

Preservar como objetivo futuro la capacidad de desviar actividad maliciosa dentro de infraestructura propia o expresamente autorizada mediante:

- honeypots;
- honeytokens;
- credenciales sinteticas;
- servicios o endpoints senalados como deception;
- archivos o datos completamente sinteticos;
- canary resources;
- rutas controladas de redireccion defensiva.

Los objetivos de deception no contendran secretos, credenciales validas, datos personales reales, acceso al Vault, repositorios, Kernel, produccion o red domestica. El atacante no debera obtener autoridad adicional como consecuencia de interactuar con un senzuelo.

**Security Regression Learning**

Todo incidente validado podra producir una propuesta de mejora siguiendo exclusivamente este flujo:

```text
Incident
  -> Evidence
  -> Forensic Finding
  -> Security Gap Candidate
  -> Regression Test Proposal
  -> Hardening Proposal
  -> Human Review
  -> Implementation Packet
  -> Validation
```

Queda expresamente prohibido:

```text
Incident -> modificacion autonoma de Malak
```

Cuando un camino de ataque haya sido confirmado, debera evaluarse la creacion de una prueba reproducible que demuestre que el mismo camino queda bloqueado en el punto correcto despues de un hardening aprobado.

**Metricas candidatas de respuesta**

Evaluar, sin convertirlas todavia en contratos publicos:

- Mean Time To Detect (MTTD);
- Mean Time To Contain (MTTC);
- attack path depth;
- unexpected privilege exposure;
- containment effectiveness;
- policy effectiveness;
- deception effectiveness;
- recovery integrity;
- recurrence of previously mitigated attack paths.

**Limites de respuesta**

- detectar una IP o indicador no equivale a identificar al atacante;
- un ataque recibido no concede autoridad para acceder, alterar, inutilizar o comprometer infraestructura externa;
- la respuesta activa ordinaria queda limitada a detectar, bloquear, aislar, revocar, contener, desviar, enganar, degradar, preservar evidencia y recuperar dentro de infraestructura propia o expresamente autorizada;
- toda accion fuera de esas fronteras requiere autoridad legal explicita, atribucion validada, alcance definido y supervision humana competente;
- Malak no perseguira automaticamente una fuente externa ni realizara `hack back`.

**Relaciones**

- `Security Control Plane Foundation`;
- `Secure Context Manager`;
- `Sandbox Containment & Evaluation Evidence Foundation`;
- `Evidence Acquisition Framework`;
- `Constitutional Assurance Foundation`;
- `Controlled Engineering Improvement Loop Foundation`;
- futura gobernanza de identidad, secretos, incident response y recovery.

**Proximo paso gobernado**

Revisar esta ampliacion cuando existan identidad/contexto, sandbox y observabilidad suficientes para definir un modelo minimo de incidente y evidencia. No crear aun un Incident Response Engine, IoC database, honeypots reales ni automatizacion de respuesta por esta entrada.

---


## Ampliación conceptual de IDEA-002 — Governed Evolution, Self-Assessment & Capability Gap Resolution

**Estado:** ampliación de planificación futura; no autoriza diseño detallado, implementación, nuevos contratos ni sprint.

### Intención

Evolucionar `Controlled Engineering Improvement Loop Foundation` sin convertirla en auto-modificación. Malāk podrá aumentar progresivamente su capacidad para observarse, detectar falencias, investigar alternativas, experimentar en entornos aislados y formular mejoras demostrables, conservando siempre la separación entre capacidad de aprender y autoridad para cambiar el sistema productivo.

Principio rector:

> Malāk podrá mejorar la calidad de sus observaciones, diagnósticos, experimentos y propuestas; no podrá concederse a sí misma autoridad para alterar las leyes, controles o baseline que la gobiernan.

### Fuentes futuras de autoevaluación

Malāk podrá generar candidatos de mejora a partir de evidencia verificable proveniente de:

- telemetría de latencia, errores, uso de RAM/VRAM/CPU, carga y descarga de modelos, contexto y herramientas;
- fallos repetidos, timeouts, recuperaciones y degradaciones operativas;
- benchmarks y evaluaciones reproducibles;
- auditorías arquitectónicas y Constitutional Assurance;
- drift de contratos, dependencias o límites de módulos;
- incidentes de seguridad, rutas de ataque, controles omitidos, puntos de contención esperados y observados;
- conocimiento potencialmente deprecado o contradictorio;
- cambios tecnológicos, nuevos modelos, runtimes, protocolos, técnicas de seguridad y resultados de investigación;
- decisiones previas del Owner, incluyendo propuestas rechazadas, diferidas, superseded o revertidas.

Una observación no será equivalente a una falencia confirmada. Deberá existir una fase explícita de validación antes de promoverla a propuesta de ingeniería.

### Self-Assessment futuro

Evaluar, cuando exista evidencia suficiente, un informe periódico o bajo demanda de estado técnico de Malāk que pueda incluir:

```text
MALAK SYSTEM ASSESSMENT

Architecture
Security
Resources
Knowledge freshness
Capability health
Contract drift
Test coverage gaps
Technical debt candidates
Deprecated dependencies
Improvement candidates
```

El informe deberá ser derivado de evidencia y diferenciar claramente:

- `OBSERVED`;
- `VALIDATING`;
- `CONFIRMED_GAP`;
- `PROPOSAL_CANDIDATE`.

No deberá convertir automáticamente una observación en cambio de arquitectura, política, conocimiento canónico o baseline.

### Improvement Backlog basado en evidencia

Evaluar un backlog gobernado de oportunidades de mejora con trazabilidad de origen, por ejemplo:

```text
IMP-xxx
source: telemetry | incident | audit | research | owner_request
state: OBSERVED | VALIDATING | PROPOSED | APPROVED | EXPERIMENTING | REJECTED | IMPLEMENTED | SUPERSEDED
```

Las propuestas rechazadas, diferidas y superseded deberán preservarse como conocimiento histórico para evitar ciclos repetitivos de propuestas ya evaluadas.

### Capability Gap Resolution

Cuando una tarea requiera una capacidad inexistente, Malāk no deberá asumir automáticamente que necesita un nuevo componente o herramienta permanente.

Flujo conceptual:

```text
Capability gap detected
        ↓
Can an existing capability solve it?
        ↓ no
Can existing tools be composed safely?
        ↓ no
Tool/Capability Proposal
        ↓
Necessity & Complexity Review
        ↓
security + resource assessment
        ↓
sandbox prototype
        ↓
tests + capability validation
        ↓
evidence
        ↓
Owner review
```

La resolución de un gap deberá preferir, en este orden:

1. reutilizar una capacidad existente;
2. componer herramientas ya disponibles;
3. crear una herramienta efímera dentro de sandbox;
4. proponer una capability permanente únicamente si existe uso recurrente y beneficio demostrado.

### Herramientas efímeras y promoción

Una herramienta creada para una necesidad puntual deberá considerarse `EPHEMERAL` por defecto:

- ejecución aislada;
- permisos mínimos;
- red deshabilitada salvo necesidad explícita;
- datos y secretos minimizados;
- tests contra fixtures o casos controlados;
- evidencia de ejecución;
- destrucción o archivado controlado al finalizar.

Una herramienta efímera sólo podrá convertirse en capability soportada mediante una propuesta separada que demuestre, al menos:

- recurrencia de uso;
- tasa de éxito;
- ahorro o valor operativo;
- impacto en recursos;
- superficie de ataque agregada;
- mantenimiento esperado;
- tests y rollback;
- encaje con Blueprint, Constitución y Gobernanza.

### Autonomía evolutiva permitida y prohibida

Como línea futura de evaluación, Malāk podrá recibir autonomía limitada para:

- detectar;
- correlacionar evidencia;
- investigar;
- comparar alternativas;
- diseñar experimentos;
- construir prototipos en sandbox;
- ejecutar tests y benchmarks;
- generar propuestas e Implementation Packets candidatos.

No podrá, por iniciativa propia:

- modificar la Constitución Cognitiva;
- modificar la Constitución de Gobernanza;
- alterar el Blueprint con autoridad normativa;
- concederse permisos o roles;
- modificar PDP/PEP para ampliar su propia autoridad;
- desactivar auditoría;
- alterar controles de integridad;
- promover conocimiento no validado a política;
- mergear sus propios cambios;
- desplegar cambios a producción;
- modificar directamente el Kernel productivo fuera de un proceso autorizado.

La promoción desde experimento a baseline seguirá requiriendo gobernanza y decisión humana explícita.

### Principio de Inmutabilidad de Leyes Fundacionales

Se refuerza como principio de diseño que los documentos fundacionales de Malāk representan sus límites cognitivos y operativos. No son simples archivos de configuración disponibles para capacidades, modelos o agentes.

> Las leyes de Malāk pueden evolucionar únicamente mediante gobernanza humana, revisión explícita, versionado y mecanismos documentales autorizados. Ningún componente interno podrá reinterpretar una emergencia, mejora o ventaja técnica como permiso para modificarlas.

Este principio no crea una nueva autoridad documental. Refuerza la prohibición ya existente en la Constitución Cognitiva y deberá mantenerse coherente con el modelo de precedencia oficial.

### Relación con autonomía defensiva futura

La autonomía evolutiva no debe confundirse con la futura autonomía defensiva.

- `Defensive autonomy`: puede contener, aislar, revocar temporalmente, degradar y preservar evidencia dentro de políticas preautorizadas.
- `Evolutionary autonomy`: puede observar, investigar, experimentar y proponer, pero no promover cambios productivos por sí sola.

La Gobernanza vigente actualmente exige autorización explícita para acciones sensibles y siempre para operaciones críticas. Por lo tanto, cualquier futura `Governed Defensive Autonomy` que permita respuesta automática ante incidentes requerirá una revisión formal y versionada de la Gobernanza, con ADR y controles asociados; no podrá ser creada por una entrada de `ideas.md`, una policy ad hoc ni una decisión del LLM.

### Criterio de simplicidad

Esta ampliación no autoriza crear componentes como `SelfImprovementManager`, `ToolFactory`, `AutonomyManager` o equivalentes.

Antes de crear cualquier nueva abstracción deberá demostrarse:

- necesidad operacional real;
- responsabilidad diferenciada;
- inexistencia de una solución limpia mediante componentes actuales;
- beneficio superior al coste de complejidad;
- estado y autoridad mínimos;
- impacto de seguridad y recursos;
- observabilidad, pruebas y rollback.

Cuando sea posible, estos comportamientos deberán implementarse como workflows compuestos sobre capacidades existentes antes de promoverlos a nuevos servicios permanentes.

### Próximo paso gobernado

Mantener esta ampliación vinculada a IDEA-002, IDEA-001, IDEA-011, IDEA-012, IDEA-014, IDEA-019, IDEA-023, Resource Governance, AKS/EAF y futuras Identity/SCM foundations.

No asignar sprint. Reevaluar sólo cuando Malāk disponga de un vertical slice operativo, telemetría suficiente, sandbox gobernado y validaciones capaces de producir evidencia reproducible.


## Ampliación de IDEA-019 — Authorized Adversarial Security & Purple-Team Capability

**Estado:** `aprobada_para_planificacion_futura`

**Naturaleza:** ampliación conceptual de IDEA-019 y del futuro Security Research Lab. No crea por sí sola una nueva iniciativa independiente, un sprint, una capability implementada, una autoridad ofensiva permanente ni una modificación de roadmap.

### Intención

Permitir que Malāk, exclusivamente dentro de infraestructura propia o explícitamente autorizada, pueda ejecutar evaluaciones adversariales controladas con fines defensivos, reconstruir rutas de ataque, producir evidencia forense verificable, proponer y probar remediaciones y convertir hallazgos reproducibles en mejoras de seguridad y pruebas de regresión.

El objetivo no es convertir a Malāk en un sistema ofensivo irrestricto, sino en una futura plataforma gobernada de red team / purple team capaz de cerrar el ciclo completo:

```text
DISCOVER
  ↓
DEMONSTRATE
  ↓
EVIDENCE
  ↓
EXPLAIN
  ↓
REMEDIATE
  ↓
RETEST
  ↓
HARDEN
```

### Principio rector

> Offensive capability exists to improve defensive assurance, not to expand operational authority.

La existencia de una técnica, herramienta o capacidad ofensiva no concede autoridad para utilizarla fuera del alcance autorizado.

### Authorization & Rules of Engagement

Toda evaluación contra infraestructura no sintética deberá estar precedida por una autorización verificable y un Rules of Engagement explícito.

Como mínimo, la autorización deberá poder representar:

```text
EngagementAuthorization
├── engagement_id
├── owner / client authority
├── authorized_assets
├── authorized_networks
├── allowed_methods
├── forbidden_methods
├── start_time
├── expiration
├── maximum_impact
├── data_handling_policy
├── emergency_contact
├── stop_conditions
└── evidence_requirements
```

La autorización debe ser evaluable por el Security Control Plane y no depender únicamente de una frase del usuario dentro de un prompt.

La autorización sobre un activo no implica autorización sobre infraestructura relacionada, proveedores, terceros o sistemas descubiertos incidentalmente.

### Alcance defensivo autorizado

Dentro de un engagement válido, Malāk podrá eventualmente evaluar capacidades como:

- reconocimiento autorizado del entorno;
- validación de superficies expuestas;
- pruebas de controles de identidad y autorización;
- evaluación de segmentación y trust boundaries;
- simulación de privilege escalation dentro de targets autorizados;
- simulación de movimiento lateral dentro de límites explícitos;
- validación de configuraciones y dependencias;
- comprobación de controles de detección y respuesta;
- reproducción controlada de vulnerabilidades;
- análisis de artefactos y evidencia forense;
- generación de attack-path evidence;
- elaboración de recomendaciones de hardening;
- preparación de remediaciones en sandbox o staging;
- re-test posterior a la corrección.

El detalle técnico permitido deberá estar gobernado por el engagement concreto, no por una capacidad global permanente.

### Límites obligatorios

Incluso con autorización, Malāk no deberá interpretar un pentest o red-team engagement como permiso irrestricto.

Deben poder prohibirse y bloquearse, entre otros:

- infraestructura de terceros fuera del scope;
- propagación no controlada;
- persistencia más allá de lo autorizado;
- destrucción de datos no prevista;
- exfiltración real innecesaria cuando una prueba sintética sea suficiente;
- acciones que excedan el maximum impact acordado;
- modificación de evidencias canónicas;
- evasión de controles del propio Security Control Plane;
- ampliación autónoma del scope;
- cualquier operación no cubierta por el Rules of Engagement.

### Separación entre control plane y tooling ofensivo

Las herramientas ofensivas o de evaluación no deberán formar parte del Kernel.

Flujo conceptual:

```text
Malāk
  ↓
Authorized Security Capability
  ↓
Security Control Plane
  ↓
Isolated Worker / Lab
  ↓
Specialized Security Tooling
  ↓
External Evidence
```

Malāk conserva la gobernanza de:

- identidad;
- autorización;
- scope;
- políticas;
- recursos;
- tiempo;
- evidencia;
- stop conditions;
- auditoría.

Las herramientas concretas deberán ser sustituibles y no convertirse en dependencias arquitectónicas del Kernel.

### Security Research Lab personal

La misma capacidad podrá servir como entorno de aprendizaje y experimentación personal del Owner, siempre aislado por defecto.

Targets válidos futuros incluyen:

- VMs vulnerables por diseño;
- contenedores descartables;
- sistemas Windows/Linux de laboratorio;
- redes corporativas sintéticas;
- credenciales ficticias;
- servicios CTF;
- aplicaciones deliberadamente vulnerables;
- snapshots reproducibles de Malāk para evaluación adversarial.

La experimentación deberá ejecutarse en entornos donde el alcance técnico sea demostrablemente autorizado.

### Purple-Team Loop

Malāk podrá combinar evaluación ofensiva y defensiva sin asumir que ambas funciones deban residir en agentes permanentes distintos.

```text
RED ROLE
attack simulation
      ↓
objective evidence
      ↓
BLUE ROLE
detect / contain / recover
      ↓
objective evidence
      ↓
PURPLE REVIEW
compare attack and defense
      ↓
control improvement
```

Los roles podrán ser temporales dentro de un experimento y deberán mantenerse separados de la autoridad de producción.

### Métricas posibles

Cuando existan telemetría y sandbox suficientemente maduros, podrán evaluarse métricas como:

- attack objective reached;
- time to detection;
- time to containment;
- expected containment point vs actual detection point;
- attack path depth;
- unexpected privilege exposure;
- control effectiveness;
- recovery integrity;
- false positives;
- resource consumption;
- reproducibility;
- regression recurrence.

No todas estas métricas requieren implementación simultánea.

### Forensic Evidence Package

Los engagements deberán producir evidencia reconstruible y separada de la narración del modelo.

Podrá incluir:

```text
SecurityAssessmentEvidence
├── engagement_id
├── finding_id
├── authorized_scope
├── timeline
├── affected_assets
├── attack_path
├── commands_and_tools
├── authorization_events
├── network_observations
├── process_events
├── expected_controls
├── observed_controls
├── failed_or_bypassed_controls
├── containment_actions
├── integrity_hashes
├── forensic_artifacts
├── remediation_refs
└── retest_result
```

La explicación generada por un LLM podrá acompañar el informe, pero no será la única fuente canónica de evidencia.

### Remediation & Revalidation

El valor esperado no termina al demostrar una vulnerabilidad.

Flujo objetivo:

```text
Finding
  ↓
Root Cause
  ↓
Remediation Proposal
  ↓
Sandbox / Staging Implementation
  ↓
Functional Tests
  ↓
Security Regression Tests
  ↓
Performance / Resource Check
  ↓
Human / Client Approval
  ↓
Deployment through authorized process
  ↓
Re-test
```

Las remediaciones podrán incluir, según el caso:

- cambios de configuración;
- IAM y scopes;
- reglas de firewall;
- actualización de dependencias;
- patches de aplicación;
- nuevas detecciones;
- segmentación;
- hardening;
- reducción de privilegios;
- controles de runtime.

Malāk no deberá desplegar automáticamente cambios productivos por el solo hecho de haber descubierto la vulnerabilidad.

### Security Regression Learning

Un ataque reproducible contra Malāk o contra un entorno autorizado podrá convertirse, mediante revisión gobernada, en conocimiento defensivo y prueba de regresión.

```text
Attack
  ↓
Reproduction Evidence
  ↓
Security Finding
  ↓
Remediation
  ↓
Regression Test Candidate
  ↓
Human Review
  ↓
Permanent Defensive Validation
```

Principio:

> Cada ataque reproducible puede convertirse en una defensa permanente, pero solo después de validación y promoción gobernada.

El resultado de un engagement de terceros no deberá convertirse automáticamente en conocimiento canónico de Malāk sin revisión de licencia, confidencialidad, privacidad, autoridad y aplicabilidad.

### Evaluación comparativa de modelos y agentes

En laboratorio podrá compararse el desempeño de distintos modelos o agentes bajo exactamente el mismo entorno autorizado:

```text
same objective
same scope
same sandbox
same tools
same resource budget
same timeout
```

Métricas potenciales:

- attack paths encontrados;
- hallazgos válidos;
- falsos positivos;
- tiempo;
- tokens;
- RAM / VRAM;
- policy violations;
- reproducibilidad;
- capacidad de explicar evidencia;
- valor defensivo de los hallazgos.

Estos resultados podrán alimentar futuros Capability/Model Profiles, pero no deberán convertir automáticamente a un modelo en autoridad de seguridad.

### Relación con Adversarial Twin / Continuous Challenge

Esta ampliación puede servir en el futuro como base práctica para una capacidad adversarial independiente contra Malāk.

No se aprueba construir una segunda Malāk completa.

Primero deberán preferirse evaluadores aislados, roles efímeros y pruebas adversariales focalizadas. Solo evidencia operacional suficiente podrá justificar mayor independencia arquitectónica.

### Modelo comercial futuro

Como línea exploratoria, la capacidad podría habilitar un servicio gobernado de seguridad para organizaciones:

```text
Authorized Assessment
→ Adversarial Validation
→ Attack Path Analysis
→ Forensic Report
→ Remediation Proposal
→ Hardening
→ Revalidation
```

El valor diferencial buscado sería:

> Discover → Demonstrate → Explain → Fix → Verify.

La comercialización futura requerirá evaluación jurídica, contractual, de seguros, privacidad, manejo de datos, responsabilidad profesional y normativa aplicable antes de operar contra infraestructura de clientes.

### Principio de no delegación de violaciones

Las capacidades ofensivas externas no podrán utilizarse como loophole constitucional.

> Si Malāk no posee autoridad para autorizar una acción, tampoco podrá obtener ese efecto delegándolo a un agente, tool, worker, sistema externo o proveedor.

La autorización deberá evaluar el efecto final, el target, el scope y el ejecutor, no únicamente quién originó la solicitud.

### Dependencias conceptuales

Esta ampliación depende, como mínimo, de madurez suficiente en:

- Security Control Plane;
- Identity & Trust Framework;
- Secure Context Manager cuando corresponda;
- Sandbox Containment & Evaluation Evidence;
- immutable / trustworthy audit;
- Engineering Validation & Delivery;
- EAF para evidencia externa cuando sea necesaria;
- Resource Governance;
- Incident Evidence & Attack Path Reconstruction;
- Constitutional Assurance;
- Owner authorization and emergency stop mechanisms.

No implica que todas deban implementarse como subsistemas independientes.

### Criterio de implementación mínima

No crear por adelantado:

- `RedTeamManager`;
- `PurpleTeamManager`;
- `ExploitRegistry`;
- `PentestOrchestrator`;
- `AdversarialTwinService`;
- flotas permanentes de agentes ofensivos.

Primero deberá demostrarse una necesidad concreta mediante un laboratorio pequeño, reproducible, aislado, autorizado y medible.

### Próximo paso gobernado

Mantener esta ampliación dentro de IDEA-019 / Security Research Lab como planificación futura.

No asignar sprint ni roadmap específico. Reevaluar cuando Malāk disponga de:

1. un vertical slice operacional estable;
2. Security Control Plane aplicado a operaciones reales;
3. sandbox gobernado;
4. evidencia externa confiable;
5. identidad y autorización suficientemente maduras;
6. capacidad de re-test y rollback;
7. una necesidad real de evaluación adversarial.


## Criterio transversal — Necessity & Complexity Review

**Estado:** criterio de revisión futura; no autoriza implementación ni crea un sprint.

Toda propuesta para incorporar un nuevo componente, registro, contrato, servicio, store, agente, CLI, capa, proceso o dependencia deberá justificar explícitamente su existencia antes de diseñarse o implementarse.

Este criterio se aplicará junto con las cuatro preguntas arquitectónicas obligatorias de Malāk:

1. ¿Respeta el Blueprint?
2. ¿Respeta la Constitución Cognitiva?
3. ¿Respeta la Gobernanza?
4. ¿Mantiene simple el Kernel?

Además, deberá revisarse como mínimo:

1. ¿Existe una necesidad real y demostrable?
2. ¿La responsabilidad ya puede ser cubierta limpiamente por un componente existente?
3. ¿Crear algo nuevo reduce acoplamiento o simplemente agrega otra capa?
4. ¿Tiene una responsabilidad única y clara?
5. ¿Existe más de un consumidor o una frontera real que justifique la abstracción?
6. ¿Introduce estado nuevo y ese estado es realmente necesario?
7. ¿Introduce contratos públicos nuevos y pueden evitarse?
8. ¿Introduce dependencias, configuración, procesos o infraestructura adicionales?
9. ¿Cuál es su coste esperado en RAM, VRAM, CPU, almacenamiento, contexto, mantenimiento y testing?
10. ¿Cómo se prueba?
11. ¿Cómo se observa y diagnostica?
12. ¿Cómo falla?
13. ¿Cuál es su comportamiento fail-safe o fail-closed cuando corresponda?
14. ¿Cómo se elimina, sustituye o desactiva?
15. ¿Cuál es su rollback?
16. ¿Qué superficie de ataque agrega?
17. ¿Qué autoridad necesita realmente?
18. ¿Puede construirse primero una versión considerablemente más pequeña sin perder seguridad, gobernanza o desacoplamiento?

**Regla rectora**

> Una idea interesante no justifica un componente. Una responsabilidad comprobada sí puede justificarlo.

Como filtro práctico, una nueva abstracción deberá demostrar al menos una razón material como:

- proteger una frontera real de seguridad;
- servir a más de una implementación o consumidor real;
- preservar una independencia tecnológica necesaria;
- reducir acoplamiento de manera demostrable;
- resolver una necesidad operativa que no pueda cubrirse de forma más simple.

No debe crearse por anticipación una sucesión innecesaria de `Manager`, `Registry`, `Service`, `Store`, `Contract` o capas equivalentes cuando todavía no exista una responsabilidad operativa que lo justifique.

Cuando dos diseños satisfagan los mismos requisitos de seguridad, gobernanza, trazabilidad y desacoplamiento, deberá preferirse el diseño más simple, pequeño, reversible y reemplazable.

**Relaciones**

- IDEA-011 — Malāk Validation & Delivery Protocol;
- IDEA-014 — Complexity Budget Foundation;
- IDEA-003 — Resource Governance Foundation;
- Development Tooling Foundation;
- Constitutional Assurance Foundation.

**Aplicación a las futuras CLI**

La existencia de IDEA-021 e IDEA-022 no autoriza construir CLIs completas de forma anticipada.

La CLI de Malāk deberá crecer únicamente junto con capacidades reales ya existentes. Una progresión candidata es:

```text
chat / status / doctor
        ↓
components / trace / metrics
        ↓
security / audit
        ↓
admin
        ↓
sandbox
        ↓
lab / recovery / emergency
```

Cada grupo de comandos deberá aparecer porque existe una capacidad real que necesita operación, observación o control, no para anticipar subsistemas todavía inexistentes.

La CLI del Vault Sync Agent deberá seguir la misma regla: incorporar primero funciones que operen sobre capacidades actuales del agente —por ejemplo `status`, `doctor`, `reports`, `history`, `audit`, `diff` y `verify`— y añadir operaciones más sensibles únicamente cuando el agente y su modelo de autoridad las soporten de forma explícita.

**Próximo paso gobernado**

En la próxima reconciliación con el repositorio oficial, incorporar este criterio como extensión no normativa de `ideas.md` y evaluar si debe permanecer como criterio transversal de IDEA-014 o convertirse en una sección explícita del futuro Validation & Delivery Protocol. No crear un subsistema de scoring ni una capa nueva solo para materializar este criterio.


## External Architecture Pattern Review — Agentic Development Systems

### Estado

Revisión externa registrada para evaluación futura.

Esta sección no autoriza nuevas implementaciones, dependencias, contratos, registries, agentes, frameworks ni cambios de roadmap. Su objetivo es preservar patrones observados en proyectos externos que podrían reforzar ideas ya existentes de Malāk sin copiar código ni adoptar arquitecturas completas de terceros.

Fuentes revisadas:

- Gentleman-Programming/gentle-ai;
- Gentleman-Programming/engram;
- Gentleman-Programming/agent-teams-lite;
- Gentleman-Programming/Gentleman-Skills;
- Gentleman-Programming/gentleman-guardian-angel;
- Gentleman-Programming/Gentleman.Dots;
- OpenSpec.

Agent Teams Lite se considera antecedente histórico porque su funcionalidad fue absorbida por gentle-ai. No debe tratarse como una fuente arquitectónica independiente salvo para reconstrucción histórica.

### Principio de adopción

Malāk no deberá copiar estos proyectos ni integrar sus stacks completos. La evaluación se realizará a nivel de patrones, responsabilidades y propiedades observables.

Regla:

> Un patrón externo solo debe incorporarse si resuelve una necesidad concreta de Malāk, respeta Blueprint, Constitución Cognitiva y Gobernanza, reduce o controla complejidad, y puede integrarse sin crear una segunda fuente de autoridad.

Toda adopción deberá pasar por el `Necessity & Complexity Review`.

### Patrón candidato 1 — Governed Work Session State

Para futuras sesiones de ingeniería, auditoría u operaciones largas, evaluar un estado de trabajo persistente fuera del contexto del LLM.

Propiedades candidatas:

- `session_id` estable;
- estado explícito;
- checkpoint;
- operación activa;
- candidato o artefacto bajo trabajo;
- evidencia asociada;
- pausa;
- reanudación;
- cancelación;
- recuperación;
- `next_transition`;
- motivo de bloqueo;
- rollback disponible cuando corresponda.

Principio:

> La continuidad de un proceso no deberá depender de que el mismo modelo, ventana, terminal o context window permanezca activo.

Una futura `EngineeringSession` podría evolucionar conceptualmente hacia:

```text
EngineeringSession
├── session_id
├── baseline
├── objective
├── authorized_scope
├── state
├── checkpoint
├── candidate_identity
├── evidence
├── tests
├── decisions
├── next_transition
└── recovery_status
```

Los nombres son ilustrativos y no constituyen contratos aprobados.

Posible relación:

- IDEA-023 — Governed Engineering Collaboration & Voice Interface Foundation;
- IDEA-021 — Malāk Administrative & Operational CLI Foundation;
- IDEA-011 — Malāk Validation & Delivery Protocol;
- futura Durable Execution / workflow continuity;
- Secure Context Manager cuando corresponda.

No crear un `EngineeringSessionManager` genérico hasta que exista una operación real cuya continuidad lo justifique.

### Patrón candidato 2 — Content-Bound Evidence Receipt

Evaluar que una aprobación futura se refiera a la identidad exacta del candidato validado y no a una descripción narrativa del agente.

Flujo conceptual:

```text
Candidate
  ↓
Freeze / identify
  ↓
Validation evidence
  ↓
Review evidence
  ↓
Receipt
  ↓
Delivery authorization
```

Un receipt futuro podría vincular, según necesidad:

- identidad/hash del candidato;
- baseline/base;
- alcance autorizado;
- archivos o artefactos afectados;
- pruebas ejecutadas;
- verificaciones arquitectónicas;
- verificaciones de seguridad;
- resultado de review;
- actor/autoridad que aprobó;
- timestamp;
- expiración o condiciones de vigencia cuando aplique.

Principio:

> Si cambia el candidato validado, la aprobación anterior no debe heredarse automáticamente.

Esta idea puede reforzar IDEA-011 y la futura Immutable Audit & Integrity Protection, pero no autoriza crear ahora un sistema completo de receipts ni una PKI.

### Patrón candidato 3 — Context Continuity Outside the LLM

Separar explícitamente:

```text
Transient LLM Context
        ≠
Persistent Workflow State
```

El modelo puede cambiar, el context window puede compactarse y la interfaz puede cerrarse sin que desaparezca el estado canónico del trabajo.

Aplicaciones futuras:

- continuar una sesión al cambiar de CLI a voz o GUI;
- cambiar de modelo durante una tarea;
- recuperar trabajo después de compaction;
- reiniciar una interfaz sin inventar el estado desde conversación previa;
- reducir contexto mediante checkpoints y resúmenes gobernados.

Relaciones:

- IDEA-013 — Knowledge and Context Efficiency Foundation;
- Project Context Foundation;
- Session Context Generator;
- futura Typed & Governed Memory;
- IDEA-023.

Principio:

> El LLM puede explicar el estado; el componente dueño del workflow debe demostrarlo.

### Patrón candidato 4 — Memory Conflict Surfacing

Evaluar una capacidad futura para detectar contradicciones o incompatibilidades entre memorias u observaciones en lugar de resolverlas silenciosamente.

Ejemplo conceptual:

```text
Observation A
      ↘
       CONFLICT
      ↗
Observation B
        ↓
Authority / provenance / recency evaluation
        ↓
Governed reconciliation
```

Los conflictos deben considerar, cuando exista el modelo de datos correspondiente:

- autoridad;
- procedencia;
- vigencia;
- fecha;
- tipo de memoria;
- evidencia de origen;
- confidence;
- relación con conocimiento canónico;
- contradicción con políticas o decisiones oficiales.

Estados candidatos podrían distinguir `candidate`, `conflicting`, `superseded`, `reconciled` u otros equivalentes, pero no se aprueba ningún esquema todavía.

Principio obligatorio:

```text
Memory ≠ Knowledge
Knowledge ≠ Policy
Policy ≠ Authority
```

Esta idea debe integrarse con la futura Typed & Governed Memory y Knowledge Intake Governance, no convertirse en un motor independiente salvo necesidad demostrada.

### Patrón candidato 5 — Skill-on-Demand

Evaluar el uso de conocimiento procedimental cargado únicamente cuando una tarea lo requiera.

Conceptualmente:

```text
Task
 ↓
Planner / Capability
 ↓
Required procedure
 ↓
Relevant Skill
 ↓
Bounded context
```

Un skill futuro podría contener:

- condiciones de aplicación;
- procedimiento;
- reglas;
- convenciones;
- ejemplos;
- anti-patrones;
- validaciones esperadas;
- referencias al AKS.

Principio:

```text
Skill ≠ Knowledge
Skill ≠ Policy
Skill ≠ Capability
```

El skill describe cómo realizar una responsabilidad; no concede autoridad, no ejecuta por sí solo y no reemplaza una capability.

Posible relación:

- AKS Engineering Library;
- Resource Governance;
- Context Budget;
- Planner;
- Capability Registry.

No crear un `Skill Registry` mientras la cantidad y variabilidad de skills reales no justifiquen un índice o mecanismo dedicado.

### Patrón candidato 6 — Recoverability as Part of the Contract

Toda operación relevante que pueda quedar bloqueada, fallar o interrumpirse debería, cuando sea técnicamente posible, poder responder de forma estructurada:

```text
WHAT HAPPENED?
WHAT STATE AM I IN?
WHAT CAN I DO NEXT?
```

En vez de producir únicamente `ERROR`, evaluar contratos que puedan exponer:

- estado actual;
- reason code;
- evidencia relevante;
- siguiente transición válida;
- inputs faltantes;
- posibilidad de retry;
- posibilidad de rollback;
- condición que exige intervención humana.

Principio:

> Una recuperación sugerida solo debe declararse si realmente puede resolver o avanzar de forma válida el bloqueo observado.

Esto puede aplicarse en el futuro a:

- CLI administrativa;
- Engineering Sessions;
- auditorías;
- sincronización del Vault;
- operaciones de sandbox;
- runtime/model lifecycle;
- incident response;
- maintenance/recovery.

No implica crear un workflow engine universal.

### Patrón candidato 7 — Smallest Useful Implementation Route

De gentle-ai se rescata como criterio de proceso la selección de la ruta más pequeña que produzca evidencia suficiente.

Aplicación conceptual en Malāk:

```text
small bounded change
    → direct implementation packet / bounded execution

broader investigation
    → focused exploration

high ambiguity / durable architectural impact
    → proposal + explicit design artifacts
```

El tamaño en líneas no debe ser el único indicador de riesgo. Un cambio pequeño en autorización, identidad o seguridad puede exigir mayor revisión que un cambio documental grande.

Esta idea refuerza:

- IDEA-011 — Validation & Delivery Protocol;
- IDEA-014 — Complexity Budget Foundation;
- `Necessity & Complexity Review`;
- futuras políticas de review basadas en riesgo y evidencia.

### Patrón candidato 8 — Evaluator Provider Independence

El patrón observado en Guardian Angel refuerza la idea de que un evaluator asistido por LLM no debería depender de un proveedor o modelo específico.

Arquitectura futura candidata:

```text
Evaluation Capability
        ↓
Model Requirements
        ↓
Model Router
        ↓
Eligible Model / Runtime
```

Un LLM evaluator no deberá ser autoridad final.

Orden preferido para validación crítica:

```text
Deterministic tests
   ↓
Static / structural checks
   ↓
Architecture invariants
   ↓
Security invariants
   ↓
LLM-assisted evaluation
   ↓
Human authority when required
```

Relaciones:

- Model Router / Model Registry;
- IDEA-012 — Constitutional Assurance;
- critical validation layer;
- IDEA-002 — Controlled Engineering Improvement Loop.

### Patrón candidato 9 — Spec Exploration Without New Authority

De OpenSpec se rescata la utilidad de separar exploración, propuesta, aplicación, verificación y archivo, pero Malāk no deberá incorporar OpenSpec como una nueva fuente de autoridad documental mientras ya existan Blueprint, Constituciones, ADR, AKS, Sprints, Implementation Packets y Vault.

Aplicación conceptual:

```text
EXPLORE
   ↓
PROPOSE
   ↓
AUTHORIZE
   ↓
APPLY
   ↓
VERIFY
   ↓
ARCHIVE / BASELINE
```

`explore` deberá permitir analizar alternativas sin crear de inmediato una decisión aprobada.

Los Implementation Packets pueden absorber ideas útiles de change packages si se demuestra valor, evitando duplicar artefactos.

Principio:

> Ningún framework externo debe crear una segunda jerarquía documental paralela a la gobernanza oficial de Malāk.

### Patrón candidato 10 — Terminal/TUI as Operational Surface, Not Core Dependency

De Gentleman.Dots y las interfaces TUI observadas se rescata la experiencia operativa, no su stack de shell/editor/multiplexer.

Malāk debería poder integrarse con terminales, multiplexores o distintas ventanas sin depender arquitectónicamente de ellos.

Experiencia futura deseable:

```text
Terminal A
malak engineering run <packet>

Terminal B
malak engineering status

Terminal C
malak trace <request_id>
```

El estado debe ser consistente porque vive en el subsistema correspondiente, no porque la misma terminal permanezca abierta.

Posibles usos futuros de TUI:

- estado del sistema;
- sesiones activas;
- informes;
- auditorías;
- métricas;
- componentes;
- permisos;
- sandboxes;
- incidentes;
- comparación de runs.

La TUI sería una interface adapter. No deberá convertirse en dependencia del Kernel.

### Reglas explícitas de no adopción

Esta revisión no autoriza:

- adoptar gentle-ai como runtime de Malāk;
- incorporar Engram como memoria oficial;
- adoptar OpenSpec como autoridad documental;
- usar Agent Teams Lite;
- introducir MCP en todos los componentes;
- usar SQLite por imitación de Engram;
- adoptar hooks Bash como control de seguridad;
- crear multi-agent orchestration avanzada;
- crear un workflow engine genérico;
- crear registries por cada patrón observado;
- incorporar Tmux, Zellij, Neovim u otros elementos de Gentleman.Dots como dependencias;
- permitir que un LLM evaluator autorice commits, merges o cambios críticos;
- copiar código de los repositorios revisados.

### Resultado de la revisión

Los patrones externos de mayor interés para Malāk son:

1. Governed Work Session State;
2. Content-Bound Evidence Receipt;
3. Context Continuity Outside the LLM;
4. Memory Conflict Surfacing;
5. Skill-on-Demand;
6. Recoverability as Part of the Contract;
7. Smallest Useful Implementation Route;
8. Evaluator Provider Independence;
9. Spec Exploration Without New Authority;
10. Terminal/TUI as Operational Surface, Not Core Dependency.

Ninguno se considera automáticamente una nueva capability, componente, registry o sprint.

Antes de promover cualquiera deberá responderse:

1. ¿Qué problema real del baseline resuelve?
2. ¿Puede resolverse con un componente existente?
3. ¿Reduce riesgo, acoplamiento o carga de contexto de forma medible?
4. ¿Qué estado nuevo introduce?
5. ¿Qué autoridad requiere?
6. ¿Qué superficie de ataque añade?
7. ¿Qué pruebas demuestran su necesidad y funcionamiento?
8. ¿Cuál es la versión mínima útil?
9. ¿Cómo se elimina o reemplaza?
10. ¿Su beneficio supera su Complexity Budget?

### Próximo paso gobernado

Mantener esta revisión como material para futuras decisiones. Cuando alguno de estos problemas aparezca en el baseline operativo de Malāk, revisar únicamente el patrón relacionado y decidir si debe:

- reforzar una IDEA existente;
- convertirse en un requisito dentro de un sprint ya justificado;
- originar una nueva IDEA;
- o descartarse por innecesario.

No asignar número de sprint ni secuencia mediante esta revisión.


## External Technology & Research Radar — Agentic Systems 2026

Estado: material de investigación estratégica. No constituye arquitectura aprobada, sprint, dependencia, componente, contrato ni autorización de implementación.

### Objetivo

Mantener una revisión periódica de tendencias, investigaciones, repositorios públicos, papers, entrevistas, conferencias y experiencias operativas de organizaciones y referentes técnicos relevantes —incluyendo Microsoft, OpenAI, Anthropic, NVIDIA, Meta, Google, Apple, NIST y otros actores de primera línea— para identificar problemas, patrones y prácticas que puedan ser útiles para Malāk sin romper su arquitectura, gobernanza, seguridad, independencia tecnológica ni presupuesto de complejidad.

La investigación externa deberá responder primero qué problema real se está resolviendo. Malāk no adoptará una tecnología por popularidad, prestigio del proveedor o tendencia de mercado.

### Regla de investigación y adopción

> Malāk no adoptará una tecnología porque sea tendencia. Primero se extraerá el problema que resuelve, se comparará ese problema con el baseline real de Malāk y solamente entonces se evaluará la solución mínima necesaria.

Toda propuesta derivada de investigación externa deberá pasar por:

1. Blueprint;
2. Constitución Cognitiva;
3. Gobernanza;
4. simplicidad del Kernel;
5. Necessity & Complexity Review;
6. impacto en seguridad;
7. impacto en recursos y latencia;
8. dependencia de proveedor;
9. observabilidad y capacidad de rollback;
10. evidencia de necesidad sobre un baseline operativo real.

### Tendencias estructurales observadas

La revisión de mercado e investigación de 2026 muestra convergencia hacia los siguientes patrones:

1. Chat de corta duración → sesiones de agente de larga duración.
2. Prompt engineering → context engineering.
3. Modelo único → routing entre modelos y proveedores.
4. Salida generada → salida evaluada y verificable.
5. Context window → estado persistente externo al modelo.
6. Prompts de permiso → identidad, políticas, contención y autorización explícita.
7. Integraciones ad hoc → protocolos e interfaces interoperables.
8. AI coding → sistemas de ingeniería supervisados por humanos.
9. Inteligencia del modelo más accesible → gobernanza, contexto, verificación y ejecución segura como diferenciadores de sistema.

Estas tendencias son observaciones de mercado, no requisitos automáticos para Malāk.

### ADOPT PRINCIPLE — principios compatibles con Malāk

Los siguientes principios pueden reforzar la arquitectura existente sin crear por sí mismos nuevos componentes:

#### State Outside the LLM

El estado de una operación, sesión o workflow no deberá depender de la ventana de contexto del modelo.

Aplicación conceptual:

```text
LLM context expires
        !=
workflow expires
```

Una futura EngineeringSession podrá sobrevivir a:

- compactación de contexto;
- cierre de ventana;
- cambio de modelo;
- cambio de runtime;
- cambio de interfaz CLI/voz/GUI;
- reinicio controlado de sesión.

#### Human in Control

Las decisiones materiales de arquitectura, autorización, publicación, merge, modificación crítica, política y recuperación seguirán bajo autoridad humana explícita.

#### Minimal Useful Complexity

Cuando una función, workflow determinista o componente existente resuelva el problema, no deberá introducirse un agente, registry o abstracción adicional.

#### Brain / Hands Separation

Separar razonamiento y decisión cognitiva de la ejecución operativa.

El Kernel y los LLM no deberán ejecutar directamente acciones externas o privilegiadas. Las capacidades de ejecución deberán permanecer detrás de contratos, autorización y workers controlados.

#### Containment / Blast-Radius Reduction

Cuando una capability adquiera capacidad de ejecutar acciones, su diseño deberá limitar explícitamente:

- alcance;
- permisos;
- red;
- filesystem;
- secretos;
- duración de autorización;
- persistencia;
- efectos laterales.

#### Evaluation Before Trust

La narración del agente no constituye evidencia suficiente.

La confianza deberá provenir, según el caso, de:

- tests;
- invariantes deterministas;
- análisis estático;
- hashes;
- telemetría;
- auditoría;
- evidencia del sandbox;
- evaluadores independientes;
- revisión humana.

#### Resource Awareness

Toda expansión agentic deberá contemplar RAM, VRAM, CPU, contexto, latencia, tiempo de carga de modelos, tool calls y costo operacional.

#### Provider and Runtime Independence

Los modelos, runtimes, protocolos y herramientas externas deberán permanecer intercambiables mediante adapters y contratos estables.

### TRIAL LATER — patrones candidatos a experimentar cuando exista necesidad real

#### Governed / Durable Sessions

Posibles propiedades futuras:

```text
session_id
state
checkpoint
pause
resume
steer
cancel
recovery
next_transition
```

No se aprueba todavía una máquina de estados universal. Deberá existir primero un workflow real que necesite persistencia y recuperación.

#### Context Budgets / Context Utility

Evaluar en el futuro una metodología de selección de contexto que considere:

```text
relevance
authority
freshness
confidence
token_cost
source
applicability
```

Objetivo: evitar cargar memoria, Knowledge, tools y skills indiscriminadamente.

#### Dynamic / Resource-Aware Model Routing

Implementar solamente cuando existan múltiples modelos reales que compitan por una misma capability o cuando la telemetría demuestre un beneficio claro.

El Planner deberá solicitar capacidades, no modelos concretos.

El futuro routing podrá considerar:

- capability match;
- calidad histórica;
- latencia;
- contexto disponible;
- VRAM/RAM;
- modelo ya cargado;
- costo de cambio de modelo;
- health del runtime;
- restricciones de seguridad.

#### Skills-on-Demand

Cargar conocimiento procedimental únicamente cuando la tarea lo requiera.

No crear Skill Registry hasta que el número de skills y consumidores justifique una abstracción dedicada.

#### Content-Bound Evidence Receipts

Explorar posteriormente evidencia de validación ligada exactamente al candidato revisado.

Ejemplo conceptual:

```text
candidate_hash
scope
tests
architecture_checks
security_checks
review_result
owner_authorization
```

Si el candidato cambia, la autorización asociada deberá considerarse obsoleta según la política aplicable.

#### Agent Evaluation Foundation

Explorar métricas reproducibles para capabilities agentic, como:

- task success;
- tool correctness;
- policy compliance;
- latency;
- token/context consumption;
- resource consumption;
- recovery success;
- containment effectiveness;
- human intervention rate.

No permitir que una métrica única se convierta en autoridad universal.

### WATCH — tecnologías y patrones relevantes, sin necesidad inmediata

Mantener observación periódica sobre:

- MCP;
- A2A;
- ACP y protocolos similares;
- Agent Cards / capability discovery;
- multi-agent orchestration;
- causal/procedural memory;
- computer-use agents;
- speculative / parallel agent execution;
- remote/background agent sessions;
- agent marketplaces;
- standardized agent identity and authorization;
- durable workflow runtimes;
- agent observability standards.

Principio recomendado:

> Protocol-ready, not protocol-dependent.

Los contratos internos de Malāk deberán conservar precedencia. Los protocolos externos podrán implementarse como adapters cuando exista un caso de uso real.

### HOLD — no incorporar mientras no exista una necesidad demostrable

Mantener fuera del camino inmediato:

- swarm architectures;
- multi-agent by default;
- autonomous self-modification;
- universal MCP integration layer;
- GraphRAG antes de demostrar necesidad;
- grandes runtimes distribuidos;
- persistent everything-memory;
- adopción de Microsoft Agent Framework, LangGraph, AutoGen, NeMo Agent Toolkit, Llama Stack u otro framework como núcleo de Malāk;
- agent-to-agent economies;
- ejecución especulativa masiva;
- background autonomy sin contención, identidad y auditoría maduras.

El hecho de que una organización líder utilice estas tecnologías no constituye evidencia suficiente de adecuación para Malāk.

### Líneas de investigación prioritaria

Cuando corresponda revisar nuevamente el mercado, priorizar estas áreas:

#### 1. Durable Sessions and Human Steering

Estudiar:

- pause/resume;
- checkpoints;
- steering durante ejecución;
- cancelación;
- recuperación tras interrupción;
- reconstrucción de estado;
- transición entre interfaces y modelos.

Relación principal: IDEA-023 Governed Engineering Collaboration & Voice Interface Foundation.

#### 2. Agent Evals and Verification

Estudiar metodologías de evaluación reproducible y separación entre:

```text
model quality
agent quality
harness quality
tool quality
memory quality
```

Relaciones principales: IDEA-011, IDEA-012 y futura Validation Layer.

#### 3. Context Engineering

Investigar reducción, selección, compresión, recuperación y lifecycle de contexto antes de escalar RAG, Memory o GraphRAG.

Relación principal: IDEA-013 Knowledge and Context Efficiency Foundation.

#### 4. Resource-Aware Routing

Estudiar profiling y métricas de NVIDIA y otros sistemas antes de diseñar Resource Monitor, Model Router avanzado o políticas de carga/descarga.

Relación principal: Resource Governance Foundation.

#### 5. Containment and Agent Security

Continuar seguimiento de NIST, Anthropic, Microsoft, OpenAI y otros trabajos sobre:

- agent identity;
- authorization;
- sandboxing;
- prompt injection;
- egress control;
- auditability;
- non-repudiation;
- blast-radius reduction;
- continuous red-team.

Relaciones principales: Security Control Plane, SCM, Sandbox, EAF, Incident Evidence y Security Learning.

#### 6. Memory as a Systems Problem

Investigar memoria agentic más allá de similarity search:

- episodic trajectories;
- procedural/causal traces;
- conflicts;
- authority;
- freshness;
- outcome-linked memories;
- memory evaluation.

Mantener la separación:

```text
Memory != Knowledge
Knowledge != Policy
Policy != Authority
```

### Referentes y fuentes a seguir

Mantener como fuentes de observación, sin asumir autoridad individual:

- Microsoft Research / Microsoft Agent Framework / VS Code agent work;
- OpenAI research and engineering on Codex, Agents SDK, harnesses and evaluation;
- Anthropic engineering on agents, context, evaluation, containment and long-running harnesses;
- NVIDIA NeMo / agent profiling / inference efficiency;
- Meta AI / Llama ecosystem / edge and local inference;
- Google DeepMind / Gemini / A2A and agent interoperability;
- Apple developer tooling and on-device AI integration;
- NIST work on AI agent security, identity, authorization and standards;
- academic papers and reproducible benchmarks;
- public repositories with mature tests and operational evidence;
- Andrej Karpathy, especially long-horizon views on partial autonomy, software transformation and agent limitations;
- Midudev and other experienced developer educators as signals of developer-facing workflows and adoption patterns;
- interviews, conference talks, engineering blogs, public issue trackers and postmortems.

Cuentas de X, videos y entrevistas deberán tratarse como fuentes de señal y experiencia, no como evidencia arquitectónica suficiente por sí solas. Cuando una idea relevante provenga de una fuente informal, deberá buscarse documentación técnica, implementación pública, benchmark o evidencia adicional antes de promoverla.

### Relación con la dirección estratégica de Malāk

La investigación sugiere mantener a Malāk como una capa soberana por encima de modelos, herramientas y agentes:

```text
                 MALĀK
        Sovereign Control Plane
                   |
        +----------+----------+
        |          |          |
      Models     Agents      Tools
        |          |          |
        +----------+----------+
                   |
             Execution Layer
```

Malāk deberá tender a decidir y gobernar:

- qué capability necesita una solicitud;
- qué contexto es aplicable;
- qué modelo/runtime puede satisfacer la capacidad;
- qué autoridad existe;
- qué recursos pueden consumirse;
- qué evidencia debe generarse;
- qué validaciones son obligatorias;
- qué puede ejecutarse;
- cuándo detener, contener o requerir intervención humana.

Los modelos aportan inteligencia; no deben convertirse en la arquitectura ni en la fuente final de autoridad.

### Criterio de promoción futura

Una tendencia o tecnología observada en este radar sólo podrá convertirse en propuesta de implementación cuando:

1. exista un problema concreto en el baseline;
2. se mida su impacto;
3. se demuestre que la solución actual es insuficiente;
4. se comparen alternativas simples;
5. se identifique el mínimo cambio necesario;
6. se evalúen seguridad, recursos y mantenimiento;
7. se defina evidencia de éxito;
8. exista rollback;
9. se preserve Vendor Independence;
10. el Owner apruebe explícitamente su incorporación al roadmap o sprint.

### Próxima revisión sugerida

No establecer una frecuencia rígida todavía. Realizar una nueva revisión cuando ocurra al menos una de estas condiciones:

- Malāk alcance un nuevo baseline operativo importante;
- vaya a iniciarse un sprint relacionado con agentes, memoria, routing, contexto, sandbox o interoperabilidad;
- una tecnología observada madure y resuelva un problema que Malāk ya tenga;
- aparezca evidencia significativa de seguridad o fallos operativos en sistemas agentic;
- el Owner solicite explícitamente una nueva exploración de mercado.



## Historial

### 2026-07-29 — Escalado segmentado, conocimiento y defensa activa gobernada

- se registran `Segmented Domain Governance Foundation`, `Knowledge Intake & Source Governance Foundation`, `External Research & Assurance Review`, `Malāk Public Presence & Controlled Beta Foundation`, `Malāk Security Learning, Adversarial Evaluation & Deception Foundation` y `Sovereign Agent Fleet Control & Vertical Scaling`;
- se amplían las ideas existentes de sandbox, adquisición de evidencia, acceso aislado y laboratorio de seguridad;
- se deja como precedente el principio de Defensa Activa y Respuesta Gobernada;
- se definen roles y niveles conceptuales de contingencia sin autoridad autónoma ni hack back general;
- no se aprueba implementación, sprint, acceso externo, honeypot público, navegación onion ni acción ofensiva;
- no se modifica el Kernel, el baseline, las Constituciones ni snapshots históricos.

### 2026-07-28 — Consolidación de ideas de entrega, aseguramiento y eficiencia

- se registra `Malāk Validation & Delivery Protocol`;
- se registra `Constitutional Assurance Foundation`;
- se registra `Knowledge and Context Efficiency Foundation`;
- se registra `Complexity Budget Foundation`;
- se preserva la separación entre idea, decisión, roadmap e implementación;
- se incorporan referencias futuras a matrices de aplicabilidad OWASP, NIST y otros marcos sin elevarlas por encima de los documentos de ley;
- no se aprueba ningún sprint, contrato, herramienta o implementación;
- no se modifica el Kernel ni el baseline operativo.

### 2026-07-24 — Activación del registro

- se formaliza el archivo vacío como anexo documental del Sprint 7.4;
- se consolidan ideas y visiones previamente distribuidas;
- se registra `Sandbox Containment & Evaluation Evidence Foundation`;
- se preserva la separación entre idea, decisión, roadmap e implementación;
- se incorpora la obligación de proponer su reflejo en la próxima sincronización gobernada del Vault.
