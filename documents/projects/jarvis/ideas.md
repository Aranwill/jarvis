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

> Ante una agresión maliciosa o destructiva contra Malāk, sus componentes, sus datos o su infraestructura autorizada, Malāk podrá detectar, contener, aislar, bloquear, engañar, degradar dentro de fronteras propias, revocar credenciales, cerrar sesiones, activar kill switches, desplegar señuelos, preservar evidencia y coordinar una respuesta defensiva proporcional.

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

Diseñar primero laboratorios locales y un Adversarial Twin sin acceso externo. Honeypots públicos, bug bounty, Tor, malware o interacción activa requieren decisiones y readiness reviews independientes.

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
Malāk se gobierna y valida a sí misma
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
