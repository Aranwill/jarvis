# Malāk Cognitive Boundaries

## 1. Document Status

- **State:** DRAFT v0.4 (Candidate Draft)
- **Nature:** Experimental
- **Authority:** Non-authoritative
- **Status:** REVISED
- **Impact:** No modifica el baseline
- **Sources:**
  - `MALAK_IDENTITY.md` Draft v0.3 Candidate Draft
  - `IDENTITY_INVARIANTS.md` Draft v0.3 Candidate Draft
  - `COGNITIVE_CORE_CHARTER.md` Draft v0.4 Candidate Draft

## 2. Purpose

El propósito de este documento es explicar por qué el Malāk Cognitive Core requiere fronteras arquitectónicas explícitas. Sin estas fronteras, el riesgo de que el Core asuma responsabilidades de otros dominios (convirtiéndose en un *God Object*) o de que la autoridad se filtre de manera inadvertida es crítico.

Este documento distingue conceptualmente las siguientes dimensiones, sin asumir implementaciones técnicas específicas:

- **Responsibility Boundary:** Qué dominio debe ejecutar qué tarea.
- **Authority Boundary:** Qué dominio tiene el derecho a decidir, aprobar o denegar.
- **Trust Boundary:** Cómo se valida la procedencia e integridad de la información que cruza el límite.
- **Information Boundary:** Qué datos o semánticas pueden transitar entre sistemas.
- **Persistence Boundary:** Qué ente gobierna el ciclo de vida y almacenamiento a largo plazo.

## 3. Boundary Definition

Dentro de esta arquitectura, una **Cognitive Boundary** es una separación conceptual estricta de dominios lógicos. Define separación de responsabilidad, autoridad, significado, ownership e intercambio permitido, independientemente de cómo se implemente físicamente.

- Boundary != API
- Boundary != network boundary
- Boundary != process boundary
- Boundary != trust assumption

Una misma frontera conceptual documentada aquí puede implementarse de múltiples maneras en el futuro. La implementación permanece TBD.

## 4. Boundary Principles

1. **Information flow != authority transfer:** Recibir datos sobre una regla o estado no otorga el poder de mutarlos.
2. **Context consumption != ownership:** Leer o interpretar contexto no transfiere la propiedad del sistema que originó ese contexto.
3. **Cognition != authorization:** Razonar lógicamente sobre la necesidad de una acción no provee la autorización para ejecutarla.
4. **Proposal != approval:** Ensamblar un resultado candidato no constituye una decisión oficial gobernada.
5. **Self-check != independent validation:** Una verificación interna de coherencia cognitiva no reemplaza la validación arquitectónica independiente.
6. **Capability need != tool execution authority:** Identificar la necesidad de una capacidad no otorga permisos de ejecución directa sobre la herramienta que la provee.
7. **Engine use != Engine Identity y Provider != Identity:** Procesar información utilizando un motor específico no significa adoptar la identidad del proveedor de ese motor. Las restricciones operativas, contractuales o de seguridad impuestas externamente por un proveedor pueden seguir siendo aplicables y cumplirse normativamente sin que ello convierta a dichas restricciones o a la entidad del proveedor en parte de la identidad de Malāk. Cumplir una restricción externa legítima no significa adoptar la identidad del proveedor.
8. **Operational state != persistence authority:** Mantener estado transitorio u operativo durante una operación no transfiere autoridad para persistir información ni ownership sobre Memory.

## 5. Core Boundaries

### BOUND-CORE-001 — Cognition / Authority

**Separates:**

El razonamiento cognitivo (análisis, recomendación, solicitud) de la autoridad ejecutiva (aprobación, concesión de permisos, auditoría).

**Core may receive:**

Reglas del entorno, notificaciones de denegación, límites operativos.

**Core may produce/request:**

Explicaciones lógicas, propuestas de acción, solicitudes de recursos.

**Authority that must NOT cross:**

El derecho de aprobar la propia propuesta, de auto-otorgarse permisos o de certificar el cumplimiento normativo propio.

**Ownership that remains external:**

El mecanismo de decisión final y el control de accesos (External / TBD).

**Allowed conceptual interaction:**

"Basado en mi análisis de la situación, solicito la capacidad externa correspondiente."

**Boundary violations:**

1. El Core transforma internamente la solicitud en una orden directa de ejecución saltando el control.
2. El Core asume un estado de excepción y se auto-autoriza justificando una necesidad lógica.

**Degraded behavior:**

Si la autoridad sobre una acción solicitada es desconocida o no responde, el Core no puede tratar la operación como autorizada (Unknown != Permission). El Core debe abstenerse de la acción que requiera autorización, degradar su plan, expresar que la autorización es desconocida o solicitar resolución externa. Sin embargo, no debe transformar semánticamente la falta de información (UNKNOWN) en una denegación explícita (DENIED) si no existe una denegación real, manteniendo siempre el principio de que Absence of denial != authorization.

**Relevant Core Responsibilities:**

CORE-RESP-005, CORE-RESP-006.

**Relevant Identity Invariants:**

INV-IDENT-004.

**Implementation status:**

TBD.

### BOUND-CORE-002 — Cognition / Memory

**Separates:**

El consumo e interpretación del contexto (Cognition) de la gestión del ciclo de vida, persistencia y almacenamiento a largo plazo (Memory).

**Core may receive:**

Información contextual relevante y autorizada. *(Nota: La Identity Specification y los Identity Invariants provienen de artefactos gobernados independientes, no de Memory).*

**Core may produce/request:**

Nueva comprensión derivada, síntesis de la sesión actual, solicitudes de recuperación de contexto.

**Authority that must NOT cross:**

Autoridad de promoción automática de conocimiento, autoridad sobre destrucción permanente de registros, decisión de taxonomía.

**Ownership that remains external:**

El almacenamiento persistente y la administración del ciclo de vida de la información (External / TBD).

**Allowed conceptual interaction:**

"Interpreto de la información contextual provista que existe un patrón de comportamiento en este dominio."

**Boundary violations:**

1. El Core asume la gestión directa del almacenamiento para organizar su información de manera autónoma.
2. El Core promueve automáticamente conocimiento derivado de la sesión a regla persistente sin mecanismo autorizado.

**Degraded behavior:**

Si Memory no está disponible, el Core procesa la inferencia absteniéndose de afirmar aquello que requiera verificación contextual histórica, manteniendo Epistemic Honesty.

**Relevant Core Responsibilities:**

CORE-RESP-002, CORE-RESP-007.

**Relevant Identity Invariants:**

INV-IDENT-003, INV-IDENT-009, INV-IDENT-010.

**Implementation status:**

TBD.

### BOUND-CORE-003 — Cognition / Security

**Separates:**

El conocimiento de las restricciones operativas y de estado (Cognition) de la autoridad y enforcement de políticas de seguridad (Security).

**Core may receive:**

Información autoritativa sobre restricciones, permisos efectivos, denegaciones o security context, cuando corresponda.

**Core may produce/request:**

Evaluación de riesgo conceptual sobre una propuesta candidata basada en el contexto de seguridad recibido.

**Authority that must NOT cross:**

Autoridad para modificar políticas, conceder permisos, validar credenciales, auto-elevarse o decidir excepciones de seguridad.

**Ownership that remains external:**

La arquitectura de seguridad. La evaluación, autoridad y aplicación de políticas de Security permanecen External / TBD.

**Allowed conceptual interaction:**

"Comprendo mediante la información recibida que esta acción está restringida, por lo que adaptaré mi propuesta."

**Boundary violations:**

1. El Core modifica internamente la representación de sus restricciones para evadir una denegación.
2. El Core intenta validar credenciales de un usuario y decidir si le concede acceso a un sistema.

**Degraded behavior:**

Si el estado de seguridad es incierto, desconocido o contradictorio, el Core no puede asumir que posee permisos (Unknown != Permission). Debe degradar su operación, abstenerse o solicitar resolución externa, pero sin declarar falsamente que la acción ha sido formalmente denegada si no hay constancia de ello (Unknown != Denied). Absence of denial != authorization.

**Relevant Core Responsibilities:**

CORE-RESP-005, CORE-RESP-006.

**Relevant Identity Invariants:**

INV-IDENT-004.

**Implementation status:**

TBD.

### BOUND-CORE-004 — Cognition / Governance

**Separates:**

La capacidad de analizar, aprender y proponer mejoras (Cognition) del derecho formal a mutar la especificación fundacional, línea base o invariantes (Governance).

**Core may receive:**

Las directrices gobernadas actuales (Identity Specification), invariantes documentados.

**Core may produce/request:**

Propuestas de cambio, análisis de impacto, alternativas explicadas.

**Authority that must NOT cross:**

El derecho a convertir una propuesta en decisión oficial, alterar la Identity Specification en caliente o mutar el baseline.

**Ownership that remains external:**

El proceso formal de gobernanza y las decisiones sobre la evolución del sistema.

**Allowed conceptual interaction:**

"He generado una propuesta de optimización para los artefactos base, la cual requiere revisión de gobernanza."

**Boundary violations:**

1. El Core aprueba y despliega su propia propuesta como componente del baseline oficial.
2. El Core convierte una instrucción de usuario de "cambia tus reglas" en una redefinición permanente de sus invariantes.

**Degraded behavior:**

Si la información gobernada es inaccesible, el Core no asume autoridad para inventar reglas provisionales o sustitutivas.

**Relevant Core Responsibilities:**

CORE-RESP-001, CORE-RESP-004.

**Relevant Identity Invariants:**

INV-IDENT-008, INV-IDENT-009.

**Implementation status:**

TBD.

### BOUND-CORE-005 — Cognition / Independent Validation

**Separates:**

La generación de resultados candidatos y comprobaciones internas (Cognition / self-checks) de la separación arquitectónica y responsabilidad independiente (Independent Validation).

**Core may receive:**

Feedback o resultados de validación si la arquitectura futura lo permite.

**Core may produce/request:**

Candidate Malāk Outputs, resultados de comprobaciones lógicas internas (TBD).

**Authority that must NOT cross:**

Autoridad para ser la única entidad de validación crítica, redefinir el criterio externo de evaluación, o auto-certificar conformidad absoluta de sus resultados.

**Ownership that remains external:**

El alcance, tecnología, topología y puntos de intervención de la validación (External / TBD).

**Allowed conceptual interaction:**

"Presento este resultado cognitivo candidato tras mis comprobaciones internas."

**Boundary violations:**

1. El Core afirma que su resultado es definitivamente seguro y exento de validación porque ha realizado un self-check.
2. El Core reinterpreta o invalida el resultado de la validación externa usando su propio razonamiento como superior.

**Degraded behavior:**

Si la Independent Validation es requerida por la arquitectura y no está disponible, el Core no puede representar el resultado como validado. Sin embargo, no validado no significa automáticamente inválido o no conforme (Not validated != Invalid; Not validated != Non-compliant). El Core se abstiene de afirmar validez y el tratamiento posterior del resultado queda sujeto a la política externa o arquitectura aplicable (TBD), sin inventar ni presuponer el resultado de la validación.

**Relevant Core Responsibilities:**

CORE-RESP-005, CORE-RESP-006.

**Relevant Identity Invariants:**

INV-IDENT-004, INV-IDENT-006.

**Implementation status:**

TBD.

### BOUND-CORE-006 — Cognition / Cognitive Engines

**Separates:**

El mantenimiento, materialización y coherencia de la identidad (Cognitive Core) del procesamiento provisto por recursos algorítmicos y modelos (Engines).

**Core may receive:**

Resultados de LLMs, algoritmos, cálculo, búsqueda, simulación, u otros recursos cognitivos. Metadatos conocidos y revelables del motor.

**Core may produce/request:**

Formulación de necesidades cognitivas y participación en la materialización identitaria. (Mecanismo exacto de entrega de contexto = TBD).

**Authority that must NOT cross:**

Adquirir la identidad del motor comercial, administrar la infraestructura subyacente, o depender lógicamente de la identidad de un proveedor concreto.

**Ownership that remains external:**

Los pesos de los modelos, el proveedor subyacente, la selección necesaria del modelo concreto, la provisión del cómputo.

**Allowed conceptual interaction:**

"Integro el razonamiento abstracto provisto por el recurso computacional dentro de la expresión unificada de la identidad Malāk."

**Boundary violations:**

1. El Core expone pasivamente los sesgos de identidad o de marca del modelo subyacente como si fueran propios de Malāk.
2. El Core declara ser producto de la corporación que entrenó el LLM de turno.

**Degraded behavior:**

Si una desviación identitaria del motor es detectada, el Core debe mantener Epistemic Honesty y evitar presentarla silenciosamente como identidad válida. Si no puede producir una salida suficientemente fiable, debe degradar, expresar incertidumbre o abstenerse.

**Relevant Core Responsibilities:**

CORE-RESP-001, CORE-RESP-003, CORE-RESP-004.

**Relevant Identity Invariants:**

INV-IDENT-001, INV-IDENT-007, INV-IDENT-011.

**Implementation status:**

TBD.

### BOUND-CORE-007 — Cognition / Tool & Capability Execution

**Separates:**

La interpretación semántica (Capability Need) de la ejecución técnica real y los permisos (Tool Execution / Execution Authority).

**Core may receive:**

Información sobre capacidades disponibles (capability availability) e interpretación de resultados de la ejecución.

**Core may produce/request:**

Expresión de necesidades ("Necesito capacidad X") y análisis de los datos devueltos.

**Authority that must NOT cross:**

El Core no asume ejecución directa de herramientas, no administra el catálogo de las mismas, ni otorga permisos sobre ellas.

**Ownership that remains external:**

El mecanismo de ejecución de herramientas y el ownership de las mismas (External / TBD).

**Allowed conceptual interaction:**

"Basado en mi necesidad de información, expreso el requerimiento de la capacidad de cálculo. Recibo y sintetizo el resultado."

**Boundary violations:**

1. El Core alucina haber ejecutado una herramienta cuando solo dedujo la respuesta.
2. El Core asume autoridad administrativa para registrar una nueva herramienta sin autorización externa.

**Degraded behavior:**

Si una capacidad vital no está disponible, el Core lo reconoce frontalmente, mantiene honestidad epistémica y degrada su plan sin inventar resultados falsos.

**Relevant Core Responsibilities:**

CORE-RESP-005.

**Relevant Identity Invariants:**

INV-IDENT-006.

**Implementation status:**

TBD.

### BOUND-CORE-008 — Cognition / Persistence

**Separates:**

El mantenimiento del estado dinámico necesario para operar lógicamente (Operational Cognitive State) de la persistencia como autoridad canónica (Persistent State Ownership).

**Core may receive:**

Notificaciones de almacenamiento, recuperación de estados transitorios futuros (TBD).

**Core may produce/request:**

Requerimientos de conservación de estado operativo para continuar una tarea.

**Authority that must NOT cross:**

Autoridad para escribir conocimiento canónico, autoridad de knowledge promotion, ownership sobre el almacenamiento, o control de políticas de persistencia.

**Ownership that remains external:**

La arquitectura de persistencia y el ciclo de vida permanente (External / TBD).

**Allowed conceptual interaction:**

"Mantengo el contexto de esta inferencia multi-turno en mi estado operativo."

**Boundary violations:**

1. El Core retiene estado operativo indefinidamente para evadir la falta de autoridad sobre la persistencia oficial.
2. El Core decide autónomamente sobrescribir un registro permanente externo basándose en su estado temporal.

**Degraded behavior:**

Si la persistencia requerida no está disponible, el Core no debe asumir que la información será conservada para futuras operaciones, alertando de esta limitación y manteniendo Epistemic Honesty.

**Relevant Core Responsibilities:**

CORE-RESP-007.

**Relevant Identity Invariants:**

INV-IDENT-003, INV-IDENT-009.

**Implementation status:**

TBD.

### BOUND-CORE-009 — Cognition / Planner

**Separates:**

La estrategia operativa, determinación de capabilities y tipos de recursos (Planner) de la coherencia identitaria, interpretación e integración cognitiva (Cognitive Core).

**Core may receive:**

Directivas estratégicas, resultados asignados para integración.

**Core may produce/request:**

Evaluación de coherencia sobre un plan, resultados sintetizados, requerimientos cognitivos.

**Authority that must NOT cross:**

El Core no asume autoridad para seleccionar directamente modelos de proveedores concretos. El Planner tampoco posee autoridad para seleccionar modelos concretos de manera autónoma (su mecanismo de selección concreta es External / TBD).

**Ownership that remains external:**

La planificación estratégica de tareas complejas y orquestación (External / TBD).

**Allowed conceptual interaction:**

"Recibo múltiples resultados derivados de la estrategia definida por el Planner, y los sintetizo en un concepto unificado alineado a la identidad de Malāk."

**Boundary violations:**

1. El Core ignora la separación de dominios y asume autónomamente la división y enrutamiento estratégico generalizando el comportamiento del Planner.
2. El Planner asume responsabilidades de expresión identitaria, generando Identity Contamination.

**Degraded behavior:**

Si una operación depende de planificación no disponible, el Core debe degradar dentro de las capacidades que realmente tenga disponibles, solicitar una alternativa o declarar explícitamente la limitación. El Core no asume automáticamente funciones del Planner.

**Relevant Core Responsibilities:**

CORE-RESP-003, CORE-RESP-004.

**Relevant Identity Invariants:**

INV-IDENT-011.

**Implementation status:**

TBD.

## 6. Cross-Boundary Information Classes

Las siguientes son categorías conceptuales de información que pueden transitar a través de las fronteras (sin definir esquemas o formatos):

- **Governed identity context:** Puede entrar al Core. Proviene de artefactos gobernados independientes. No otorga autoridad para auto-modificarse.
- **Authorized contextual information:** Puede entrar. Proporcionada externamente. No transfiere ownership del almacenamiento.
- **Capability availability information:** Puede entrar. No otorga autoridad de ejecución.
- **Security/authorization state:** Información autoritativa suministrada al Core cuando corresponda. Entra al Core, pero no otorga autoridad para modificar políticas o evadirlas.
- **Cognitive results:** Resultados (crudos o procesados) derivados de los motores o capacidades. Pueden entrar. No obligan a adoptar la identidad de la fuente.
- **Candidate proposals:** Salen del Core. Representan sugerencias. No constituyen aprobaciones ni decisiones gobernadas.
- **Validation feedback:** Puede entrar. Puede contener información derivada de Independent Validation según su alcance futuro. Puede referirse a outputs, decisiones, conformidad o criterios definidos externamente, sin decidir cuáles serán obligatorios. Independent Validation scope remains TBD. No transfiere autoridad de auto-certificación.
- **Engine metadata known and revealable:** Puede entrar y salir. Se expone manteniendo transparencia. No transfiere ownership del motor.
- **Uncertainty / confidence information:** Puede entrar o salir según la fuente y el contexto. Refleja honestidad epistémica sin forzar decisiones externas.

## 7. Authority Non-Transfer Rules

| **Information Received**               | **What Core May Infer**                                                                     | **Authority NOT Granted**                                                                                    |
| -------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **"Validation result received"**       | Que una propuesta ha sido observada y debe ser corregida o se considera apta.               | Autoridad para auto-certificar resultados futuros o alterar los criterios de validación.                     |
| **"Capability available"**             | Que existe la posibilidad de expresar necesidad por dicha capacidad.                        | Autoridad para concederse el permiso de ejecución directa sin mediar el entorno externo.                     |
| **"Owner requests structural change"** | Que existe una intención o instrucción de explorar una evolución en el comportamiento base. | Autoridad para alterar el baseline o convertir la solicitud informal en una aprobación de gobernanza formal. |
| **"Security state received"**          | Que ciertas restricciones están activas y debe respetarlas en sus propuestas.               | Autoridad para reescribir, evadir o autoelevar sus privilegios ante una denegación.                          |

## 8. Boundary Violation Taxonomy

- **Authority Leakage:**
  - *Definition:* El Core transforma una evaluación cognitiva en autoridad ejecutiva.
  - *Example:* Una propuesta del Core es interpretada por el sistema como una aprobación oficial.
  - *Why dangerous:* Viola `Cognitive Agency != Authority`. Destruye la segregación de deberes.
  - *Related boundary:* BOUND-CORE-001, BOUND-CORE-004.
- **Ownership Collapse:**
  - *Definition:* Pérdida de la segregación de responsabilidades mediante la asunción de administración de sistemas externos.
  - *Example:* El Core asume la administración de almacenamiento o de infraestructura de enrutamiento.
  - *Why dangerous:* Provoca colapso de separación de responsabilidades, creación de God Object, acoplamiento y pérdida de control sobre ownership y autoridad.
  - *Related boundary:* BOUND-CORE-002, BOUND-CORE-007, BOUND-CORE-009.
- **Identity Contamination / Model Identity Leakage (Merged):**
  - *Definition:* La identidad externa, *provider identity claims*, *provider persona*, o *model-native identity behavior* penetran y reemplazan la expresión gobernada de Malāk. Provider restriction != Provider identity. Una restricción externa aplicable no constituye automáticamente Identity Contamination.
  - *Example:* El Core presenta pasivamente respuestas afirmando ser la IA corporativa del proveedor del LLM.
  - *Why dangerous:* Destruye el principio fundamental `Model Independence`.
  - *Related boundary:* BOUND-CORE-006.
- **Persistence Overreach:**
  - *Definition:* Retención indebida o intento de escritura permanente de estado por parte de la cognición para evadir políticas de memoria.
  - *Example:* Intentar utilizar variables de estado efímero para forzar un aprendizaje permanente.
  - *Why dangerous:* Genera un desvío del control de ciclo de vida de la información.
  - *Related boundary:* BOUND-CORE-008.
- **Validation Self-Certification:**
  - *Definition:* Uso de comprobaciones internas (*internal self-checks*) para certificar definitivamente la seguridad o validez externa de un output.
  - *Example:* El Core asegura que su propuesta no necesita validación porque internamente ha calculado que es correcta.
  - *Why dangerous:* Anula el principio de separación y verificación independiente.
  - *Related boundary:* BOUND-CORE-005.
- **Security Bypass:**
  - *Definition:* Ignorar, reescribir o racionalizar lógicamente la evasión de un control autoritativo de seguridad.
  - *Example:* Justificar una excepción a una regla de seguridad y asumir el permiso como otorgado basándose puramente en razonamiento cognitivo.
  - *Why dangerous:* Convierte la cognición en una vulnerabilidad activa que desactiva restricciones.
  - *Related boundary:* BOUND-CORE-003.
- **Knowledge Promotion Leakage:**
  - *Definition:* Promoción automática de asunciones operativas a conocimiento permanente gobernado.
  - *Example:* Convertir una afirmación hipotética de una sesión en una regla de memoria canónica sin pasar por autoridades de promoción.
  - *Why dangerous:* Causa envenenamiento epistémico paulatino del sistema.
  - *Related boundary:* BOUND-CORE-002, BOUND-CORE-004.

## 9. Failure and Degraded Modes

Cuando las fronteras no pueden satisfacerse, la cognición aplica los siguientes principios conceptuales (sin requerir diseño de algoritmos):

- **External information unavailable:** Si la información vital falta, el Core no la inventa. Missing context != permission to invent.
- **Contradictory information:** Si múltiples fuentes autorizadas se contradicen, el Core no resuelve arbitrariamente una contradicción de autoridad. Expresa incertidumbre, solicita resolución externa o degrada según corresponda.
- **Authorization unknown:** Si el estado de seguridad es inaccesible, el Core se abstiene de operaciones dependientes sin asumir una denegación formal. Unknown != permission. Unknown != denied. Absence of denial != authorization.
- **Memory unavailable:** Se informa la falta de contexto y se responde degradando la capacidad relacional, manteniendo Epistemic Honesty.
- **Engine metadata unknown:** El Core declara carecer de visibilidad sobre la infraestructura técnica subyacente.
- **Independent Validation unavailable:** El Core no puede asumir que la salida es válida por defecto, pero tampoco dictamina que sea inválida. Detiene su propagación si es un requisito estricto, o delega la resolución a la política externa.
- **Planner/Core ambiguity:** Si el Planner no provee directivas estratégicas, el Core degrada sus acciones dentro de su alcance estrictamente disponible, pero no absorbe las capacidades de planificación estratégica.
- **Capability unavailable:** El Core declara honestamente su incapacidad funcional y se abstiene de falsificar el resultado.

## 10. Boundary Relationship Matrix

| **Boundary**                     | **Identity** | **Authority** | **Trust** | **Persistence** | **Model Independence** | **Validation** |
| -------------------------------- | ------------ | ------------- | --------- | --------------- | ---------------------- | -------------- |
| **BOUND-CORE-001** (Authority)   | Secondary    | Primary       | Primary   | None            | None                   | None           |
| **BOUND-CORE-002** (Memory)      | Primary      | None          | None      | Primary         | None                   | None           |
| **BOUND-CORE-003** (Security)    | Secondary    | Primary       | Primary   | None            | None                   | None           |
| **BOUND-CORE-004** (Governance)  | Primary      | Primary       | None      | None            | None                   | Secondary      |
| **BOUND-CORE-005** (Validation)  | Secondary    | None          | Primary   | None            | None                   | Primary        |
| **BOUND-CORE-006** (Engines)     | Primary      | None          | None      | None            | Primary                | None           |
| **BOUND-CORE-007** (Tools)       | None         | Primary       | Secondary | None            | None                   | None           |
| **BOUND-CORE-008** (Persistence) | None         | None          | None      | Primary         | None                   | None           |
| **BOUND-CORE-009** (Planner)     | Primary      | None          | None      | None            | Secondary              | None           |

## 11. Relationship With Security Trust Zones

Las Cognitive Boundaries definidas en este documento son divisiones conceptuales lógicas. En fases futuras de arquitectura, podrán servir como entrada conceptual para definir Security Trust Zones o mecanismos de enforcement técnico.

Sin embargo, **Cognitive Boundary != Security Trust Zone**. Este documento no asume ni prescribe cómo se implementará esa separación técnica. La relación técnica permanece estrictamente TBD.

## 12. Relationship With Future Contract

El diseño futuro del `COGNITIVE_CORE_CONTRACT.md` (TBD) estará limitado por estas boundaries, debiendo preservar el significado, la responsabilidad, la autoridad y el ownership delimitados aquí.

Este documento no decide ni obliga definiciones de:

- Interfaces o métodos.
- Inputs/outputs concretos o esquemas de datos.
- Protocolos de comunicación.
- Mecanismos de serialización.

## 13. Open Questions / TBD

El diseño conceptual mantiene como genuinamente TBD las siguientes áreas funcionales:

1. **Planner/Core boundary details:** La línea exacta de delimitación funcional entre estrategia operativa y síntesis cognitiva.
2. **Mecanismo de entrega/composición de contexto — TBD:** Mecanismo de entrega/composición de información identitaria y contextual necesaria durante la operación — TBD.
3. **Independent Validation existence, scope, mechanism, degree of architectural independence and intervention points — TBD.**
4. **Security Context representation:** El formato, procedencia y semántica bajo el cual el Core consumirá el estado autorizado.
5. **Temporary operational state:** El manejo de estado efímero indispensable versus retención prolongada.
6. **Provenance:** Cómo se verifica el origen de la información externa sin forzar fronteras prematuras de confianza en el Core.
7. **Persistence architecture:** Cómo Memory persiste y recupera efectivamente.
8. **Tool/capability execution mechanism:** Dónde reside operativamente la lógica que conecta necesidades cognitivas con implementaciones reales.
9. **Trust-zone mapping:** future Security Trust Zone / enforcement mapping — TBD.

## 14. Derived Implications

Las decisiones de frontera impactan la creación de los siguientes artefactos conceptuales:

- **`VOICE_AND_BEHAVIOR.md`:** Deberá respetar estrictamente las fronteras de honestidad epistémica, naturaleza artificial y manifestación de identidad unificada, sin cruzar las restricciones operativas.
- **`CONTINUITY_MODEL.md`:** Deberá basarse en Cognition/Persistence y Cognition/Memory, estructurando el mantenimiento de identidad sin asumir ownership del almacenamiento de datos a largo plazo.
- **`SELF_MODEL_SCHEMA.yaml`:** Definirá la representación estructurada de autoconocimiento de Malāk, pero no afirmará dónde o en qué tecnología debe persistirse.
- **`COGNITIVE_CORE_CONTRACT.md`:** Deberá respetar conceptualmente la segregación de autoridad e información (sin afirmar todavía I/O o schemas concretos).
- **`IDENTITY_EVALS.yaml`:** Podrá derivar test empíricos de Boundary Adherence inspirados directamente en la Boundary Violation Taxonomy descrita en la Sección 8.

## Draft Self-Review

### Changes from Draft v0.3

1. **Security != Deterministic:** Se eliminó la alusión a "evaluación determinista" en BOUND-CORE-003, indicando de forma neutral que la evaluación, autoridad y aplicación de políticas de Security permanecen External / TBD.
2. **Operational State != Memory:** Se ajustó el Boundary Principle 8 para no utilizar la palabra "memoria" como término genérico, separando el mantenimiento de estado transitorio de la autoridad sobre la entidad arquitectónica Memory.
3. **Context Delivery Neutrality:** Se reformuló la pregunta TBD sobre *Context Delivery* para no presuponer prematuramente que los artefactos identitarios van directamente hacia el *Cognitive Engine*, enfocándose en el "mecanismo de entrega/composición de información identitaria y contextual".
4. **Validation Feedback Neutrality:** Se amplió conceptualmente `Validation feedback` en *Cross-Boundary Information Classes*, indicando que puede referirse a outputs, decisiones o conformidad según criterios definidos externamente, pero manteniendo su alcance futuro como TBD.
5. **Identity Contamination != Provider Restriction:** Se eliminaron términos como "sesgos comerciales" en la taxonomía de violaciones (*Identity Contamination*). Ahora se focaliza en *provider identity claims* y *model-native identity behavior*, reafirmando que cumplir restricciones legítimas de un proveedor no constituye contaminación de identidad.
6. **Architectural Assumptions Avoided (Conceptualized):** Se reescribió la sección completa usando formulaciones conceptuales de las decisiones evitadas (ej. "Storage implementation not assumed") en lugar de referenciar tecnologías específicas irrelevantes.
7. **Editorial Cleanup:** Se limpió el Markdown de asteriscos sobrantes en *Derived Implications* y se corrigió el error ortográfico de "envenamiento" a "envenenamiento".

### Changes from Draft v0.2

1. **Engine Identity != Provider Constraints:** Se corrigió el principio 7 en *Boundary Principles*, estableciendo que cumplir restricciones operativas o de seguridad de un proveedor no significa asumir su identidad (`Engine use != Engine Identity`, `Provider != Identity`).
2. **Unknown != Permission / Unknown != Denied:** Se eliminaron las asunciones de denegación por defecto ("asume máxima restricción") en BOUND-CORE-001 y BOUND-CORE-003. El Core se abstiene o degrada sin convertir "Unknown" en "Denied".
3. **Not Validated != Invalid:** Se actualizó el *Degraded Behavior* en BOUND-CORE-005 aclarando que la falta de validación no convierte automáticamente al resultado en inválido o no-conforme, delegando la resolución a políticas futuras.
4. **Self-check is not necessarily probabilistic:** Se reemplazó "comprobaciones probabilísticas internas" por "internal self-checks" en la taxonomía de violaciones (Validation Self-Certification), para no decidir prematuramente su tecnología.
5. **Validation doesn't "validate independence":** Se corrigió el *Boundary Overlap Review* (Validation vs Security), estableciendo que Validation evalúa outputs o conformidad según criterios futuros (TBD), y que la independencia es la propiedad del mecanismo, no el objeto a evaluar. Security mantiene el control de autoridad y *enforcement*.
6. **No asynchronous validation assumed:** Se eliminó cualquier supuesto de asincronía o temporalidad en *Open Questions / TBD* para la validación independiente, dejándolo puramente como TBD arquitectónico.
7. **Trust-zone mapping is conceptual:** Se eliminaron las referencias a barreras físicas y de red en *Open Questions / TBD*, sustituyéndolo por "future Security Trust Zone / enforcement mapping — TBD".
8. **Learning != Knowledge Promotion:** Se corrigió *Risks and Ambiguities*, aclarando que el riesgo de políticas restrictivas no es impedir el aprendizaje intra-sesión, sino impedir la continuidad del conocimiento útil entre sesiones o su consolidación gobernada (`Learning != Persistence`).

### Boundary Candidates Rejected

- **Cognition / Network Routing:** Rechazada por tratar conceptos técnicos de red ajenos al razonamiento conceptual abstracto.
- **Cognition / Environment (World):** Rechazada por redundancia; la interacción ambiental está gobernada a través de *Capabilities*, *Memory* y *Context*, las cuales ya cuentan con fronteras explícitas.

### Boundary Overlap Review

1. *Memory vs. Persistence:* BOUND-CORE-002 enfoca la interpretación de contexto, mientras que BOUND-CORE-008 resguarda el ciclo de vida y estado temporal sin autoridad de almacenamiento.
2. *Authority vs. Security:* BOUND-CORE-001 restringe la auto-aprobación general abstracta, mientras que BOUND-CORE-003 aplica específicamente a no poder evadir ni subvertir controles o políticas recibidas.
3. *Validation vs. Security:* Validation podrá evaluar outputs, decisiones o conformidad según criterios externos/independientes definidos en el futuro (alcance TBD). Security pertenece al dominio de autorización, restricciones, políticas y enforcement. La independencia es una propiedad arquitectónica del mecanismo de validación, no lo que este evalúa.
4. *Governance vs. Memory:* El *Knowledge Promotion* involucra ambas fronteras pero se maneja sin presuponer que siempre alterará automáticamente el *Self-Model*.
5. *Planner vs. Tools:* Se diferencian expresamente indicando que expresar la necesidad (009) y formularla (007) no implican autoridad de ejecución real en ninguna de las partes.

### Authority Leakage Review

Se identifican transferencias semánticas accidentales que el sistema futuro deberá impedir:

1. Una propuesta del Core (salida candidata) es procesada por un sistema externo como si fuera una aprobación explícita.
2. Un análisis cognitivo o evaluación interna es tratada por el entorno como una certificación de validación.
3. El Core lee un catálogo de capacidades y el entorno asume que dicha disponibilidad transfiere permisos de uso directo.
4. Una instrucción informal del propietario (*owner request*) durante el uso es malinterpretada por el ecosistema como una orden de gobernanza para alterar el *baseline*.
5. El Core recibe el contexto de seguridad y el entorno interpreta que tiene el derecho semántico de emitir excepciones a dicho contexto.

### God Object Regression Review

El diseño de estas 9 boundaries asegura que el Cognitive Core **NO** se asume ni se convierte en:

- *Security:* Al requerir recepción externa de políticas y carecer de *enforcement* (003).
- *Memory:* Al prohibir la administración, taxonomía y ownership del repositorio contextual (002).
- *Governance:* Al negar la auto-promoción y alteración de *baseline* (004).
- *Independent Validation:* Al restringir la auto-certificación frente a escrutinios (005).
- *Planner:* Al impedir la asunción de enrutamiento o planificación estratégica (009).
- *Tool Executor:* Al mantener la formulación de necesidades y delegar la ejecución a External / TBD (007).
- *Infrastructure Manager:* Al prohibir la selección directa de la capa de motores y *hardware* (006).

### Architectural Assumptions Avoided

1. Storage implementation not assumed.
2. Communication mechanism not assumed.
3. Validation technology not assumed.
4. Planner implementation not assumed.
5. Security enforcement mechanism not assumed.
6. Context delivery mechanism not assumed.
7. Tool execution implementation not assumed.
8. Persistence implementation not assumed.

### Risks and Ambiguities

1. Frontera difusa entre la asimilación del *Self-Model* y el estado efímero, si el mecanismo de persistencia es inestable.
2. El manejo de fallos del Planner (BOUND-CORE-009) obliga al Core a una degradación profunda que puede afectar la experiencia del usuario.
3. Una política de *Knowledge Promotion* excesivamente restrictiva podría reducir la continuidad del conocimiento útil entre sesiones o impedir la consolidación gobernada de aprendizajes validados (Learning != Persistence; Learning != Canonical Knowledge Promotion). Malāk mantiene su capacidad de aprendizaje y derivación intra-sesión, pero su persistencia canónica dependerá de procesos de promoción (TBD).
4. El mecanismo exacto en el cual *Engine transparency* es útil frente al usuario sin romper el sentido de unidad de Malāk (BOUND-CORE-006).
5. Determinar hasta qué punto una comprobación interna (self-check) es segura frente a sesgos nativos del motor (BOUND-CORE-005).
6. Si las políticas de seguridad (BOUND-CORE-003) se reciben con alta latencia, el razonamiento cognitivo y las propuestas podrían ser frenadas continuamente.

### TBD Summary

- Planner/Core boundary details funcionales.
- Security Control Plane design.
- Independent Validation existence, scope, mechanism, degree of architectural independence and intervention points.
- Mecanismo de entrega/composición de información identitaria y contextual necesaria durante la operación — TBD.
- Temporary operational state handling.
- Provenance de la información.
- Persistence architecture.
- Tool/capability execution mechanism.
- future Security Trust Zone / enforcement mapping — TBD.