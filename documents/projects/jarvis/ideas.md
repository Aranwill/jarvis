---
title: Registro de ideas y visión futura de Malāk
status: activo
authority: no normativa
document_role: anexo de captura y seguimiento
introduced_in: Sprint 7.4
as_of_date: 2026-07-28
as_of_commit: d1c90bf0bf55a7076d68c1f4830e89e0d843661c
branch: agent/record-high-value-evolution-ideas
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

Los presupuestos no deben depender del hardware actual ni transformar restricciones locales en arquitectura permanente.

## Historial

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