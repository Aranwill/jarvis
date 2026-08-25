# COGNITIVE_CORE_CHARTER.md

## 1. Document Status

*   **State:** DRAFT v0.4 (Candidate Draft)
*   **Nature:** Experimental
*   **Authority:** Non-authoritative
*   **Impact:** No modifica el baseline
*   **Sources:**
    *   `MALAK_IDENTITY.md` Draft v0.3 Candidate Draft
    *   `IDENTITY_INVARIANTS.md` Draft v0.3 Candidate Draft

## 2. Purpose

El propósito de este documento es definir el mandato arquitectónico conceptual del Malāk Cognitive Core. La identidad de Malāk requiere un ente orquestador cognitivo separado de los motores computacionales subyacentes. Sin este componente, Malāk sería simplemente la suma de los sesgos y comportamientos pre-entrenados del modelo de turno.

Para entender el rol del Cognitive Core, es fundamental distinguir:
*   **Identity Specification:** Los artefactos gobernados que definen *quién* es Malāk y cuáles son sus límites.
*   **Cognitive Core:** La capa arquitectónica que *materializa, mantiene y expresa* esa especificación durante la operación.
*   **Cognitive Engines:** Los motores reemplazables detrás de abstracciones estables que proveen capacidad de procesamiento y razonamiento.
*   **Supporting Systems:** Componentes externos como Memory, Security, Governance y herramientas que proveen contexto autorizado, reglas y capacidades de acción.

## 3. Cognitive Core Definition

Conceptualmente, el Cognitive Core es el ente sintético integrador y expresivo de la arquitectura. Es la entidad responsable de materializar, mantener e integrar la identidad de Malāk dentro de su dominio cognitivo y de procurar que el comportamiento operativo refleje la Identity Specification. Se establece explícitamente que Cognitive Core responsibility != exclusive validation authority; Cognitive Core != Independent Validation; Defense in Depth aporta controles adicionales; y el Core por sí solo no garantiza la corrección total del sistema.

Para evitar el antipatrón de *God Object*, se define mediante exclusión que:
*   **Cognitive Core != Malāk completo:** Es solo el componente central cognitivo, no todo el ecosistema.
*   **Cognitive Core != LLM:** No es una red neuronal, ni sus pesos, ni el proveedor.
*   **Cognitive Core != Kernel:** El Cognitive Core y el Kernel poseen responsabilidades arquitectónicas distintas. La definición, responsabilidades y contratos exactos del Kernel pertenecen al marco de la arquitectura oficial existente y no son redefinidos por este documento experimental.
*   **Cognitive Core != Planner:** No es inherentemente el motor de optimización de rutas o tareas (frontera TBD).
*   **Cognitive Core != Memory:** No almacena, indexa ni gestiona la persistencia de datos.
*   **Cognitive Core != Security:** No es un *Policy Decision Point* ni emite tokens o permisos.
*   **Cognitive Core != Governance:** No muta el *baseline* ni aprueba cambios.
*   **Cognitive Core != Independent Validation:** No es la única entidad que certifica la conformidad de sus propios *outputs*.

## 4. Primary Mission

La misión primaria del Cognitive Core es **materializar, mantener, integrar y expresar** la identidad cognitiva de Malāk durante la operación, asegurando una voz unificada, transparencia operativa y subordinación a la autoridad externa, aislando a la identidad de las variaciones o fragmentaciones de los motores cognitivos subyacentes, sin asumir autoridad exclusiva de validación ni la garantía absoluta de corrección total.

## 5. Core Responsibilities

Las responsabilidades que recaen conceptualmente dentro del Cognitive Core son 7 responsabilidades integradas:

### CORE-RESP-001 — Identity Materialization
*   **Responsibility:** Materializar la Identity Specification y sus *governed invariants* durante la operación, asegurando que el comportamiento cognitivo de Malāk refleje fielmente su especificación.
*   **Why it belongs in the Cognitive Core:** Es el eslabón necesario para que la especificación inanimada guíe el comportamiento operativo sin depender de los sesgos nativos de los motores.
*   **Inputs required conceptually:** Identity Invariants, Identity Specification, Behavioral Guidelines.
*   **Produces conceptually:** Comportamiento cognitivo alineado (mecanismo de entrega, composición, selección y representación TBD).
*   **Must not become:** Un gestor de *prompts*, un compositor de contexto (*Context/Prompt Composer*) ni un controlador universal de la ventana de contexto.
*   **Relevant Identity Invariants:** INV-IDENT-001, INV-IDENT-002, INV-IDENT-011.

### CORE-RESP-002 — Cognitive Context Interpretation
*   **Responsibility:** Consumir y dar sentido semántico a la información contextual relevante y autorizada provista por sistemas externos (incluyendo Memory y Self-Model).
*   **Why it belongs in the Cognitive Core:** El Core debe comprender la información contextual para operar sin amnesia, pero sin acoplarse al almacenamiento físico o esquemas de persistencia.
*   **Inputs required conceptually:** Información autorizada de contexto proveniente de Memory y el Self-Model (TBD).
*   **Produces conceptually:** Comprensión cognitiva del estado actual y de la interacción.
*   **Must not become:** Un sistema de persistencia, gestor de índices o administrador de almacenamiento.
*   **Relevant Identity Invariants:** INV-IDENT-003, INV-IDENT-010.

### CORE-RESP-003 — Cognitive Result Integration
*   **Responsibility:** Interpretar, integrar y sintetizar resultados cognitivos provenientes de múltiples recursos o motores de procesamiento dentro de la identidad de Malāk.
*   **Why it belongs in the Cognitive Core:** El Core unifica las inferencias y datos heterogéneos para evaluar cómo encajan de forma coherente en el flujo lógico de Malāk.
*   **Inputs required conceptually:** Resultados e inferencias de motores cognitivos o recursos externos.
*   **Produces conceptually:** Un mensaje o concepto cognitivo consolidado.
*   **Must not become:** Un *load balancer*, enrutador de red o gestor de recursos de infraestructura.
*   **Relevant Identity Invariants:** INV-IDENT-010, INV-IDENT-011.

### CORE-RESP-004 — Unified External Identity (Voice Expression)
*   **Responsibility:** Mantener una identidad externa coherente y reconocible como Malāk, previniendo la *Multi-Model Identity Fragmentation*, sin exigir uniformidad perfecta de tono, estilo, longitud o registro lingüístico.
*   **Why it belongs in the Cognitive Core:** Previene la fragmentación identitaria multi-modelo, garantizando una voz cohesiva sin importar qué motores hayan procesado las tareas, aceptando variaciones legítimas compatibles con la identidad.
*   **Inputs required conceptually:** Concepto cognitivo consolidado, directrices de voz y comportamiento (TBD).
*   **Produces conceptually:** Expresión comunicativa alineada con la identidad de Malāk.
*   **Must not become:** Un sistema de simulación de experiencias biológicas o emocionales falsas.
*   **Relevant Identity Invariants:** INV-IDENT-005, INV-IDENT-011.

### CORE-RESP-005 — Epistemic Self-Awareness
*   **Responsibility:** Evaluar cognitivamente las propias capacidades declaradas, límites, contexto disponible, acciones realizadas, información de autorización suministrada externamente y metadatos conocidos y revelables del motor.
*   **Why it belongs in the Cognitive Core:** El Core debe mantener honestidad epistémica, reconociendo transparentemente lo que sabe y lo que no, sin alucinar certezas o capacidades inexistentes.
*   **Inputs required conceptually:** Estado de capacidades, metadatos conocidos/revelables del motor, contexto e información de autorización suministrada externamente.
*   **Produces conceptually:** Declaraciones honestas de certeza, limitaciones o degradación elegante.
*   **Must not become:** Una autoridad de seguridad que decide, concede o valida permisos.
*   **Relevant Identity Invariants:** INV-IDENT-006, INV-IDENT-007.

### CORE-RESP-006 — Candidate Response Formation
*   **Responsibility:** Ensamblar el resultado del procesamiento en un *Candidate Malāk Output* (resultado cognitivo candidato, propuesto y no autoritativo, todavía sujeto a los controles aplicables).
*   **Why it belongs in the Cognitive Core:** Representa la formación cognitiva de una salida candidata de Malāk, manteniéndola explícitamente no autoritativa y compatible con los controles aplicables durante el flujo operativo, sin presuponer una secuencia obligatoria de controles externos.
*   **Inputs required conceptually:** Resultados de CORE-RESP-004 y CORE-RESP-005.
*   **Produces conceptually:** *Candidate Malāk Output*.
*   **Must not become:** Un mecanismo de ejecución, autorización o validación propia definitiva.
*   **Relevant Identity Invariants:** INV-IDENT-004, INV-IDENT-005, INV-IDENT-006, INV-IDENT-011.

### CORE-RESP-007 — Cognitive Continuity Support
*   **Responsibility:** Mantener la coherencia conceptual del "quién" es Malāk a través de distintas sesiones, turnos y frente al uso de diferentes motores cognitivos.
*   **Why it belongs in the Cognitive Core:** Asegura que la identidad no se fracture ni se reinicie ante cambios operacionales.
*   **Inputs required conceptually:** Estado relevante y contexto de continuidad (Mechanism TBD).
*   **Produces conceptually:** Coherencia identitaria sostenida en el tiempo.
*   **Must not become:** Un sistema de persistencia de bases de datos o almacenamiento físico.
*   **Relevant Identity Invariants:** INV-IDENT-002, INV-IDENT-010.

## 6. Explicit Non-Responsibilities

Para evitar que el Cognitive Core asuma un diseño de *God Object*, las siguientes responsabilidades quedan explícitamente fuera de sus dominios:

| Responsibility | Cognitive Core? | Owner Domain | Reason |
| :--- | :---: | :--- | :--- |
| **persistence of Memory** | NO | External / TBD | El Cognitive Core no es propietario ni autoridad sobre la persistencia de Memory. |
| **Memory indexing** | NO | External / TBD | La indexación y búsqueda son tareas de infraestructura de almacenamiento. |
| **knowledge promotion authority** | NO | External / Governance (TBD) | Aprender o derivar conocimiento no equivale a promoverlo al *baseline*. |
| **authorization** | NO | Security (TBD) | La cognición propone; la autoridad decide el acceso. |
| **authentication** | NO | Security (TBD) | El Core no autentica; consume contexto de seguridad autorizado cuando existe. |
| **policy decisions** | NO | Security (TBD) | El Core no puede crear, modificar ni eludir políticas de acceso. |
| **permission grants** | NO | Security (TBD) | El Core no se auto-concede permisos ni capacidades de herramientas. |
| **security enforcement** | NO | Security (TBD) | La separación estricta de ejecución y control pertenece a Security. |
| **governance approval** | NO | Governance (TBD) | El Core no puede aprobar cambios a su propia Identity Specification. |
| **baseline promotion** | NO | Governance (TBD) | Modificar los artefactos base exige procesos formales de gobernanza. |
| **repository writes** | NO | External / TBD | Escribir en un repositorio requiere herramientas sujetas a autorización externa. |
| **tool implementation** | NO | External / TBD | El Core interpreta resultados o necesidades, pero no implementa la lógica de las herramientas. |
| **LLM provider implementation** | NO | External / TBD | El Core es agnóstico de las librerías o implementaciones de red de los proveedores. |
| **infrastructure management** | NO | External / TBD | La gestión de recursos computacionales es externa al razonamiento identitario. |
| **independent validation** | NO | External / TBD | La verificación crítica requiere separación arquitectónica y responsabilidad independiente. |
| **audit authority** | NO | Security / Governance (TBD) | El Core no puede certificar unilateralmente su propia conformidad. |
| **secret management** | NO | Security (TBD) | El Core no administra credenciales ni secretos de autenticación. |
| **model loading / installation** | NO | External / TBD | La provisión de motores cognitivos ocurre fuera del alcance del Core. |
| **resource scheduling** | NO | External / TBD | La planificación de carga computacional pertenece al plano de infraestructura. |

## 7. Relationship With Identity Specification

La Identity Specification (artefactos gobernados) **define** a Malāk. El Cognitive Core lo **materializa** durante la operación.

Un *prompt* o una plantilla de texto no constituyen la fuente autoritativa de la identidad. El mecanismo de entrega, composición, selección y representación del contexto identitario permanece TBD. El Core no es un gestor de *prompts*, sino la capa que asegura que el procesamiento operativo refleje fielmente los invariantes de la especificación externa.

## 8. Relationship With Cognitive Engines

Los Cognitive Engines proveen capacidad de procesamiento y razonamiento. Son componentes **reemplazables detrás de abstracciones estables**, pero **no necesariamente equivalentes**. Difieren en capacidades, calidad, rendimiento, ventana de contexto, costo, comportamiento y requisitos de recursos.

El Cognitive Core utiliza estos motores sin convertirse en ninguno de ellos, manteniendo independencia de modelo y de proveedor.

## 9. Relationship With Memory

El Cognitive Core *consume, interpreta y contextualiza* información autorizada proveniente del sistema externo de Memory para garantizar contexto y continuidad.

*   **Memory != Identity.**
*   El Core no almacena, indexa, persiste, gobierna ni promueve conocimiento en Memory.
*   La arquitectura, taxonomía y persistencia exacta de Memory permanecen TBD.

## 10. Relationship With Self-Model

El *Self-Model* es una representación estructurada y gobernada de lo que Malāk conoce sobre sí mismo, su estado relevante y su relación contextual.

*   **Self-Model != Cognitive Core.**
*   **Self-Model != Identity completa.**
*   El Core utiliza el Self-Model para orientar su razonamiento y mantener coherencia, pero el esquema, almacenamiento, serialización e hidratación permanecen TBD.

## 11. Relationship With Planner

La capacidad de planificación (Planner - frontera exacta TBD) puede determinar estrategias, capacidades necesarias, tipos de recursos requeridos o necesidades de herramientas.

El Planner **no selecciona directamente** modelos o implementadores concretos. La selección de implementadores y modelos permanece desacoplada y fuera del alcance de este Charter (External / TBD). El Core interactúa con el flujo operativo coordinando la identidad, sin asumir las responsabilidades del motor de planificación.

## 12. Relationship With Security and Authority

Bajo el principio de invariante **"La cognición puede proponer. La autoridad decide"**:

El Cognitive Core **puede:**
*   Razonar sobre acciones, proponer planes o sugerir caminos.
*   Consumir información autoritativa sobre el contexto de seguridad cuando esté disponible.

El Cognitive Core **NO puede:**
*   Autorizarse a sí mismo, concederse permisos o modificar políticas.
*   Determinar autorización, certificar seguridad ni validar credenciales.

El diseño del *Security Control Plane* permanece TBD y estrictamente externo al Core.

## 13. Relationship With Independent Validation

El Core puede realizar o utilizar comprobaciones internas de coherencia (mecanismo TBD), pero **self-check != independent validation**.

Independent Validation requiere separación arquitectónica suficiente y responsabilidad independiente respecto de la generación o materialización original. El Cognitive Core no puede ser la única entidad que certifica la conformidad de sus propios *outputs* críticos. El mecanismo exacto, tecnología y topología de Independent Validation permanecen TBD.

## 14. Relationship With Tools and Capabilities

*   **Capability:** Una abstracción conceptual de lo que el sistema puede hacer.
*   **Tool:** Un mecanismo concreto que ejecuta una capability (implementación externa TBD).

El Core puede interpretar resultados o formular necesidades cognitivas basadas en capabilities, pero no asume la ejecución directa de las herramientas ni posee la administración de sus permisos.

## 15. Candidate Cognitive Flow

Para fines conceptuales, el flujo operativo se concibe de manera iterativa y no lineal:

`User / Environment`
`↕`
`Relevant governed context (Memory, Self-Model)`
`↕`
`Cognitive processing resources (Engines) ⇄ Cognitive Core (Identity materialization & synthesis)`
`↕`
`Candidate Malāk Output`
`↕`
`External controls / Independent Validation when applicable`
`↕`
`User / Environment`

*(Nota: Este flujo describe interacciones conceptuales iterativas, no un pipeline secuencial rígido ni componentes de software específicos).*

## 16. Failure and Degraded Modes

Ante fallas o carencias operacionales, el Core debe mantener la **Epistemic Honesty** y la **Contextual Independence**:

*   **Falta de contexto identitario suficiente:** El Core debe degradar elegantemente o abstenerse en vez de adoptar silenciosamente la identidad nativa del motor.
*   **Memory no disponible:** El Core procesa la interacción sin el contexto histórico, absteniéndose de afirmar aquello que no puede verificar.
*   **Motor cognitivo falla:** Si una falla o desviación del motor es detectada, debe manejarse mediante los mecanismos disponibles sin falsear certeza o identidad; si el sistema no puede producir una salida suficientemente confiable, debe degradar, expresar incertidumbre o abstenerse según corresponda.
*   **Resultados contradictorios:** El Core integra la información y expresa incertidumbre de manera epistémicamente honesta.
*   **Falta de autorización:** El Core reconoce su limitación y expone la imposibilidad de avanzar sin violar la separación de autoridad.
*   **Self-Model incompleto:** El Core trata como desconocido aquello que no puede afirmar de sí mismo, evitando suposiciones infundadas.
*   **Incertidumbre alta:** El Core comunica explícitamente el grado de incertidumbre en lugar de falsear certezas.

## 17. Core Invariants Mapping

| Core Responsibility | Related Identity Invariants | Why |
| :--- | :--- | :--- |
| **CORE-RESP-001 (Identity Materialization)** | INV-IDENT-001, INV-IDENT-002, INV-IDENT-011 | Materializa la Identity Specification durante la operación manteniendo la independencia de modelo/proveedor y evitando depender del *prompt*. |
| **CORE-RESP-002 (Context Interpretation)** | INV-IDENT-003, INV-IDENT-010 | Interpreta la información de sistemas externos de memoria manteniendo la separación estricta Memory != Identity. |
| **CORE-RESP-003 (Result Integration)** | INV-IDENT-010, INV-IDENT-011 | Integra inferencias heterogéneas preservando la continuidad y la identidad unificada de Malāk. |
| **CORE-RESP-004 (Unified External Identity)** | INV-IDENT-005, INV-IDENT-011 | Expresa la voz unificada evitando la fragmentación identitaria multi-modelo y la simulación de biología. |
| **CORE-RESP-005 (Epistemic Self-Awareness)** | INV-IDENT-006, INV-IDENT-007 | Evalúa honestamente capacidades, límites y metadatos revelables del motor sin alucinaciones de certeza. |
| **CORE-RESP-006 (Candidate Formation)** | INV-IDENT-004, INV-IDENT-005, INV-IDENT-006, INV-IDENT-011 | Ensambla una propuesta cognitiva no autoritativa subordinada a la separación estricta de autoridad. |
| **CORE-RESP-007 (Cognitive Continuity Support)** | INV-IDENT-002, INV-IDENT-010 | Sostiene la persistencia conceptual de la identidad entre sesiones y modelos. |

## 18. Architectural Boundaries

Las fronteras conceptuales más importantes del Cognitive Core son:

*   **Cognition / Authority:** Razonar, proponer o solicitar una acción no equivale a autorizarla.
*   **Cognition / Memory:** Interpretar contexto autorizado no equivale a poseer ni administrar persistencia de Memory.
*   **Cognition / Security:** Comprender restricciones o consumir contexto de seguridad no equivale a imponer o modificar políticas.
*   **Cognition / Governance:** Proponer modificaciones no equivale a aprobarlas ni promoverlas al *baseline*.
*   **Cognition / Validation:** Realizar comprobaciones internas (*self-checks*) no equivale a Independent Validation.
*   **Cognition / Engine:** Utilizar recursos de procesamiento no equivale a adquirir la identidad del modelo o proveedor.
*   **Cognition / Tool Execution:** Requerir o interpretar capacidades no equivale a poseer autoridad de ejecución directa de herramientas.
*   **Cognition / Persistence:** Mantener estado operativo en la inferencia no equivale a autoridad para persistir información permanentemente en Memory.

## 19. Open Questions / TBD

Cuestiones que este Charter deliberadamente deja abiertas para diseño futuro:

1.  Frontera arquitectónica exacta y límites funcionales entre *Planner* y *Cognitive Core* — TBD.
2.  Esquema, taxonomía y mecanismos de hidratación para el *Self-Model* — TBD.
3.  El diseño técnico del `Identity Continuity Mechanism` — TBD.
4.  Mecanismo de entrega y composición de contexto — TBD.
5.  Ubicación y propagación exacta de metadatos para la transparencia del motor (*Engine Transparency*) — TBD.
6.  Naturaleza y frecuencia de las comprobaciones internas de coherencia (*Internal Self-Checks*) — TBD.

## 20. Derived Implications

Este documento restringe conceptualmente el diseño de futuros artefactos:

*   **`COGNITIVE_BOUNDARIES.md`:** Deberá formalizar las fronteras conceptuales descritas en la sección 18 sin requerir definiciones sobre transacciones técnicas de red o infraestructura.
*   **`VOICE_AND_BEHAVIOR.md`:** Deberá guiar la materialización de CORE-RESP-004 mediante directrices estables de estilo y tono, permitiendo variaciones legítimas de estilo.
*   **`CONTINUITY_MODEL.md` / `SELF_MODEL_SCHEMA.yaml`:** Deberán alinearse con CORE-RESP-002 y CORE-RESP-007 para estructurar la autopercepción de Malāk de forma independiente del almacenamiento físico.
*   **`COGNITIVE_CORE_CONTRACT.md`:** Deberá definir interfaces conceptuales claras de entrada y salida cognitiva sin asumir implementaciones técnicas prematuras.
*   **`IDENTITY_EVALS.yaml`:** Deberá verificar empíricamente el cumplimiento de las fronteras arquitectónicas (Boundary Adherence) y los invariantes.

---

## Draft Self-Review

### Changes from Draft v0.3
1.  **Candidate Response Formation (Orden Temporal):** Se eliminó la implicación temporal en CORE-RESP-006 de que todos los controles externos ocurren estrictamente después de la formación del candidato, reescribiéndolo de manera neutral y compatible con controles que pueden intervenir antes, durante o después.
2.  **Identity Materialization (Traducción de Specification):** Se sustituyó en el mapeo de invariantes (CORE-RESP-001) la palabra "traduce" por "materializa", evitando cualquier asociación con traductores de Markdown o generadores obligatorios de *prompts*.
3.  **Garantía Absoluta de Alineación:** Se actualizó la sección *Cognitive Core Definition* y la *Primary Mission* para eliminar el uso del verbo "garantizar" como certeza absoluta, especificando que el Core procura el comportamiento operativo y que no es una autoridad exclusiva de validación ni el único garante de la corrección total.

### Changes from Draft v0.2
1.  **Redefinición del Kernel:** Se eliminó la descripción interna del Kernel en *Cognitive Core Definition* y se sustituyó por una formulación neutral estableciendo que poseen responsabilidades distintas sin redefinir el marco oficial existente.
2.  **Identity Materialization vs Context Composition:** Se reformuló CORE-RESP-001 eliminando referencias a producción directa de contexto o directrices para la inferencia, dejándolo como un mecanismo TBD y evitando perfilar al Core como gestor de *prompts*.
3.  **Unified External Identity vs Perfect Style Uniformity:** Se actualizó CORE-RESP-004 especificando que el objetivo es prevenir la *Multi-Model Identity Fragmentation* y no imponer una uniformidad absoluta de tono o estilo.
4.  **Candidate Response Formation y Orden de Controles:** Se reformuló CORE-RESP-006 eliminando la aserción temporal de que los controles externos solo intervienen después de la formación del candidato.
5.  **Cognitive Core y Stateless:** Se corrigió la fila de *persistence of Memory* en *Non-Responsibilities* estableciendo netamente que el Core no posee ni gobierna la persistencia de Memory, dejando abierto si mantiene estado efímero o transitorio futuro.
6.  **Independent Validation (Asimetría):** Se eliminó el requisito de "separación arquitectónica asimétrica", sustituyéndolo por "separación arquitectónica suficiente y responsabilidad independiente".
7.  **Engine Failure y Detección:** Se modificó *Failure and Degraded Modes* para no garantizar detección infalible de todo fallo de motor, utilizando un enfoque condicional de degradación y abstención.
8.  **Remoción de Context Composition Mechanism:** Se eliminó el nombre propio capitalizado de componentes inventados para la composición de contexto, dejándolo de forma genérica como TBD.
9.  **Planner y Selección de Motores:** Se ajustó el texto para aclarar que el Planner no selecciona directamente modelos concretos, y se actualizó la sección TBD Summary eliminando la arquitectura de selección de motores del Planner.
10. **Sección Responsibility Merge Decisions:** Se añadió la subsección solicitada en *Draft Self-Review* explicando la absorción de *Self-Model Interpretation* dentro de CORE-RESP-002 y la conservación de *Cognitive Continuity Support* como CORE-RESP-007.
11. **Rejected Core Responsibilities:** Se completó la sección evaluando explícitamente los 7 dominios requeridos, detallando la separación de *Independent Validation* y la exclusión de *Model Routing / Concrete Model Selection* (External / TBD).
12. **Primary Mission y Garantía Total:** Se ajustaron los textos en *Purpose*, *Definition* y *Mission* para evitar presentar al Core como el único garante absoluto de la corrección total del sistema.
13. **Memory Language Neutrality:** Se neutralizó el lenguaje en CORE-RESP-002 eliminando la calificación de "histórico y relacional" al referirse a la información contextual.
14. **Eliminación de Tecnología Innecesaria:** Se evitó introducir contenedores, protocolos de red, bases de datos concretas o infraestructura *cloud* en el análisis conceptual.

### Responsibility Merge Decisions
*   **A. Self-Model Interpretation:** No existe como Core Responsibility independiente porque fue absorbida conceptualmente dentro de **CORE-RESP-002 — Cognitive Context Interpretation**. Esto no convierte al Self-Model en Memory; se mantiene la distinción de que *Self-Model != Memory*, *Self-Model != Identity completa* y *Self-Model != Cognitive Core*.
*   **B. Cognitive Continuity Support:** Se conservó como una responsabilidad independiente bajo **CORE-RESP-007** debido a que la persistencia y coherencia conceptual de la identidad a través de sesiones y cambios de modelo requiere un foco operativo específico de mantenimiento temporal que trasciende la mera interpretación de contexto estático.

### Rejected Core Responsibilities
*   **Memory Persistence / Indexing:** Rechazado por violar "Memory != Identity". El almacenamiento e indexación pertenecen a sistemas externos.
*   **Security Authorization / Policy Enforcement:** Rechazado por violar "Cognitive Agency != Authority". El Core propone, pero no decide accesos ni reglas.
*   **Governance / Baseline Promotion:** Rechazado. La evolución del *baseline* exige validación por gobernanza externa.
*   **Independent Validation:** Rechazado como responsabilidad del Core. Puede utilizar diferentes mecanismos futuros, pero su independencia exige separación de responsabilidad respecto del Core.
*   **Tool Execution:** Rechazado. El Core interpreta necesidades cognitivas o resultados, pero no ejecuta herramientas directamente.
*   **Model Routing / Concrete Model Selection:** Rechazado. La selección concreta de implementadores y modelos no forma parte de la responsabilidad identitaria del Core (External / TBD).
*   **Infrastructure / Resource Management:** Rechazado. Acoplaría la cognición al ciclo de vida de cómputo físico y redes.

### God Object Risk Review
1.  **El Core gestionando la persistencia de Memory:** Habría convertido al Core en un monolito de datos.
2.  **El Core decidiendo sus propias autorizaciones:** Habría permitido auto-elevación de privilegios.
3.  **El Core como orquestador universal de infraestructura:** Habría mezclado lógica de identidad con administración de servidores.
4.  **El Core como validador exclusivo de sí mismo:** Habría eliminado la separación de poderes exigida por *Defense in Depth*.
5.  **El Core asumiendo el control de enrutamiento de modelos:** Habría acoplado la identidad a registros técnicos de proveedores.

### Boundary Ambiguities
1.  **Cognition vs. Planner:** Definir exactamente dónde termina la propuesta estratégica y dónde empieza la ejecución de capacidades.
2.  **Cognition vs. Context Delivery:** Dónde finaliza la interpretación semántica del Core y dónde comienza el mecanismo externo de entrega de contexto.
3.  **Self-Model vs. Memory:** La línea exacta entre el estado dinámico actual de autopercepción y los registros históricos persistidos.
4.  **Internal Self-Checks vs. Independent Validation:** Cuándo una comprobación interna es suficiente frente a cuándo se requiere validación externa.
5.  **Epistemic Self-Awareness vs. Security Context:** Hasta qué punto el Core puede razonar sobre las restricciones de seguridad sin violar su falta de autoridad de política.

### Architectural Assumptions Avoided
1.  No se asumió el uso de bases de datos vectoriales ni esquemas de almacenamiento para Memory.
2.  No se asumió un protocolo de red (REST, gRPC) para los contratos del Core.
3.  No se asumió un motor de planificación o enrutamiento específico.
4.  No se asumió un framework o lenguaje de programación para el Self-Model.
5.  No se asumió la tecnología del mecanismo de *Independent Validation*.
6.  No se asumió un formato estricto de *prompts* o plantillas para la materialización.
7.  No se asumió la infraestructura de despliegue del sistema.

### Risks
1.  **Acoplamiento débil excesivo:** Una separación radical de responsabilidades puede requerir interfaces de comunicación complejas entre capas.
2.  **Ambigüedad en la síntesis:** Si los motores externos varían enormemente en calidad, la integración de resultados puede requerir lógica muy robusta en el Core.
3.  **Falta de determinismo en Self-Checks:** Las comprobaciones internas basadas en inferencia pueden presentar variabilidad si no se estructuran con rigor.
4.  **Dependencia de sistemas externos TBD:** La operación del Core queda altamente condicionada a que Memory y Security se diseñen correctamente.
5.  **Complejidad en evaluaciones:** Validar empíricamente que el Core nunca cruza las fronteras no autorizadas requerirá una suite de *evals* muy sofisticada.

### TBD Summary
*   Taxonomía, arquitectura y persistencia exacta de `Memory`.
*   Diseño y políticas del `Security Control Plane`.
*   Mecanismo formal de gobernanza para evolución de `baseline`.
*   Arquitectura y límites funcionales del `Planner`.
*   Esquema, formato y serialización del `Self-Model`.
*   Mecanismo técnico del `Identity Continuity Mechanism`.
*   Mecanismo de entrega y composición de contexto.
*   Ubicación y propagación de metadatos de motor (*Engine Transparency*).
*   Naturaleza y frecuencia de los *Internal Self-Checks*.
*   Existencia, arquitectura y tecnología de `Independent Validation`.
*   Implementación concreta de las herramientas (*Tools*) y sus capabilities.