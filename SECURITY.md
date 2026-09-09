# Security Policy

**Versión:** 2.0  
**Estado:** Activo  
**Clasificación:** Política de seguridad protegida  
**Actualizado:** 2026-09-09

---

## 1. Propósito y autoridad

Este documento define la postura de seguridad obligatoria de Malāk.

Debe interpretarse junto con, y subordinado a:

1. `docs/governance/cognitive_constitution.md`;
2. `docs/governance/governance_constitution.md`;
3. `docs/architecture/blueprint.md`;
4. especificaciones, ADR y contratos públicos aprobados aplicables.

`SECURITY.md` establece requisitos y límites de seguridad. No convierte una capacidad futura en arquitectura implementada ni autoriza por sí mismo nuevos sprints, componentes, agentes, herramientas, Memory persistente, navegación, sandboxes o integraciones externas.

Las referencias conceptuales y de investigación pueden reforzar esta política, pero no poseen autoridad superior a las fuentes normativas.

---

## 2. Principio rector

Malāk adopta una arquitectura **Zero Trust**, **Defense in Depth** y **Human in Control**.

Ningún componente, modelo, runtime, provider, agente, tool, skill, fuente de conocimiento, memoria, protocolo o servicio externo recibe confianza o autoridad implícita por el hecho de existir, responder correctamente o haber sido utilizado anteriormente.

Reglas fundamentales:

```text
Model != System
Intelligence != Authority
Capability != Permission
Decision != Execution
Execution != Evidence
Evidence != Authority
```

Toda autoridad debe poder demostrarse mediante los mecanismos deterministas y gobernados correspondientes.

---

## 3. Invariantes de seguridad

### 3.1 Zero Trust interno

- Ningún componente debe asumir confianza implícita sobre otro componente.
- Toda interacción sensible debe atravesar contratos, validación y políticas aplicables.
- Compartir proceso, host, runtime, modelo o infraestructura no implica compartir confianza.

### 3.2 Denegación por defecto y fail-closed

- Una operación sensible no autorizada debe ser denegada.
- Una decisión ausente, inválida, inconsistente o no verificable no puede interpretarse como permiso.
- Los errores en enforcement o evidencia crítica de autorización deben producir comportamiento fail-closed cuando corresponda.

### 3.3 Least Privilege y Least Context

- Cada componente recibe únicamente los permisos necesarios para su responsabilidad autorizada.
- Toda futura ejecución agentic o tool-enabled deberá recibir únicamente el contexto necesario para la tarea.
- Acceso a información no implica permiso para persistirla, divulgarla, reutilizarla o transmitirla.

### 3.4 Human in Control

- Las acciones sensibles deben respetar la autorización definida por la Constitución de Gobernanza.
- Las operaciones críticas requieren siempre autoridad humana explícita.
- Un modelo, agente, tool, evaluator, receipt, score o mecanismo de evidencia no puede sustituir la autoridad humana cuando ésta sea requerida.

### 3.5 Separación de responsabilidades

La ruta de seguridad debe preservar, según aplicabilidad:

```text
request
  ↓
authorization decision
  ↓
enforcement
  ↓
protected operation
  ↓
evidence / audit
```

Debe mantenerse la separación entre:

```text
request != decision != enforcement != execution != evidence
```

### 3.6 Auditabilidad

- Las decisiones y acciones sensibles deben dejar evidencia estructurada suficiente para reconstrucción posterior.
- La auditoría no concede autoridad ni reemplaza la decisión que registra.
- Métricas, eventos operativos y auditoría de seguridad permanecen conceptualmente separados.

### 3.7 Reemplazabilidad y contención

Los componentes externos al núcleo de autoridad deben diseñarse, cuando corresponda, para poder ser detenidos, revocados, aislados, reemplazados o reconstruidos sin convertir su estado interno en requisito de supervivencia de Malāk.

---

## 4. Controles implementados en el baseline actual

Esta sección describe controles verificados en el baseline vigente; no amplía su alcance.

### 4.1 Security Control Plane Foundation

Sprint 7.5 incorporó y validó:

- `PermissionScope`;
- `SecurityContext`;
- `AuthorizationRequest`;
- `AuthorizationDecision`;
- Policy Decision Point determinista;
- Policy Enforcement Point separado;
- denegación por defecto;
- comportamiento fail-closed;
- confirmación humana cuando la política aplicable la requiere;
- evidencia estructurada de autorización separada de métricas y eventos operativos.

El LLM no participa en la decisión de autorización.

### 4.2 Secure Context Lifecycle Foundation

Sprint 7.6 incorporó y validó:

- identidad contextual mediante `SecurityContext`;
- `context_id`, `session_id`, `subject_id` y estado de autenticación;
- `issued_at` y `expires_at`;
- `parent_context_id` para lineage;
- `Clock` / `SystemClock`;
- `SecurityContextValidator`;
- `SecurityContextIssuer`;
- `SecurityContextRenewer`;
- `SecurityContextEnvelope`;
- enforcement temporal en el PDP;
- semántica `issued_at <= now < expires_at`.

Validator, Issuer, Renewer y Envelope no conceden permisos.

### 4.3 Frontera conversacional vigente

La integración conversacional actual no concede autoridad a la conversación ni al LLM.

Queda preservado:

```text
conversation != authorization
LLM output != authorization
session context != SecurityContext
```

La continuidad conversacional y `session_id` no constituyen Memory persistente, identidad criptográfica ni autoridad operacional.

---

## 5. Riesgo residual aceptado y límites actuales

El baseline actual conserva riesgo residual conocido: `SecurityContext` todavía no posee una raíz criptográfica fuerte de identidad y provenance.

Permanecen sin implementar y requieren diseño, threat modeling, validación y autorización independientes:

- identidad y firmas criptográficas fuertes;
- PKI;
- nonce y replay protection;
- MFA;
- Secure Context Manager criptográfico completo;
- Secure Message Bus;
- IPC seguro;
- gestión avanzada de secretos;
- Sandbox gobernado;
- agentes operativos;
- tools externas operativas;
- navegación;
- Memory persistente;
- rutas operativas reales de alto riesgo;
- automatización defensiva avanzada.

La existencia de estos gaps no autoriza su implementación automática.

Antes de habilitar agentes, tools, red, mensajería, Memory persistente o integraciones externas de mayor riesgo, estos límites deben volver a evaluarse explícitamente.

---

## 6. Prompt & Context Trust Boundary

La regla histórica:

```text
External information = DATA
External information != INSTRUCTIONS
```

se aplica como requisito transversal a toda futura superficie que introduzca contenido no confiable.

Debe preservarse:

```text
USER INTENT
!=
EXTERNAL CONTENT
!=
TOOL OUTPUT
!=
RETRIEVED MEMORY
!=
KNOWLEDGE CANDIDATE
!=
AUTHORITY
```

Por lo tanto:

- contenido web, archivos, emails, documentos, tool output, resultados de retrieval y payloads de protocolos externos deben tratarse como datos con trust explícito;
- ningún texto procesado puede conceder permisos, modificar políticas, ampliar scope o saltar PDP/PEP;
- una tool description, skill, prompt template, MCP/A2A payload o recurso externo no constituye autoridad;
- indirect prompt injection debe tratarse como amenaza de sistema, no únicamente como problema de prompting;
- las instrucciones efectivas para operaciones protegidas deben derivarse de canales, contratos, identidad, contexto y autorización verificables fuera del LLM.

---

## 7. Memory y Knowledge: confianza y poisoning

Antes de introducir Memory persistente o recuperación que pueda influir durablemente en Malāk, su diseño deberá contemplar una frontera de admisión gobernada.

Como mínimo deberán evaluarse, según el tipo de información:

- provenance;
- tipo, dominio y scope;
- autoridad de la fuente;
- confidence;
- vigencia temporal;
- contradicciones;
- indicadores de contaminación o compromiso;
- elegibilidad de recuperación;
- revocación, supersession o quarantine cuando corresponda.

Principios obligatorios:

```text
Conversation != Memory
Memory != Knowledge
Knowledge != Policy
Policy != Authority
```

Similarity search por sí sola no constituye una política suficiente de confianza.

La evidencia de un agente, tool o incidente no debe promoverse automáticamente a conocimiento canónico.

---

## 8. AI Supply-Chain Trust

La cadena de suministro de Malāk puede incluir más que paquetes de software.

Las futuras políticas de admisión deberán considerar, proporcionalmente al riesgo:

- paquetes y dependencias;
- modelos, weights y archivos GGUF;
- LoRA y adapters;
- embedding models;
- datasets;
- prompt templates;
- skills y definiciones de agentes;
- MCP servers y adapters de interoperabilidad;
- plugins y tools externas;
- containers e imágenes;
- fuentes de conocimiento.

Antes de admitir un artefacto relevante deberán poder evaluarse, cuando corresponda:

- origen y provenance;
- versión;
- integridad y hash;
- firma cuando sea aplicable;
- licencia;
- vulnerabilidades conocidas;
- dependencias transitivas;
- permisos o capacidades requeridos;
- política de actualización;
- rollback;
- cuarentena o retiro.

Reglas:

```text
Artifact integrity != Artifact trust
Artifact trust != Execution authorization
```

Un artefacto auténtico y criptográficamente íntegro todavía puede ser inseguro o incompatible con la política de Malāk.

---

## 9. Identidad, delegación y no elevación

Ningún agente, tool o componente podrá ampliar por delegación la autoridad de quien origina una tarea.

Toda futura delegación debe respetar conceptualmente:

```text
Effective delegated authority
=
Delegator authority
∩ applicable policy
∩ task scope
∩ capability scope
∩ resource limits
∩ TTL
```

La delegación nunca podrá producir expansión de autoridad.

La revocación de un contexto o autoridad superior deberá poder invalidar autoridad derivada cuando la política aplicable lo requiera.

Las cadenas de delegación verificables, identidad criptográfica, firmas y protección contra replay requieren diseño y aprobación propios antes de uso operacional.

---

## 10. Compromise Containment & Trust Revocation

Ante sospecha razonable de compromiso, la postura objetivo es reducir autoridad y radio de impacto antes de confiar en el componente investigado.

Principio obligatorio para futuras capacidades de respuesta:

> **Compromise must reduce authority, never expand investigation privileges.**

La arquitectura futura deberá permitir, proporcionalmente al riesgo y dentro de las capacidades aprobadas:

```text
SUSPECT
  ↓
FREEZE / REVOKE AUTHORITY
  ↓
CUT OR RESTRICT COMMUNICATION
  ↓
ISOLATE / QUARANTINE
  ↓
PRESERVE EVIDENCE
  ↓
ASSESS BLAST RADIUS
  ↓
MARK RELATED STATE / CREDENTIALS / ARTIFACTS AS SUSPECT
  ↓
ROTATE / REVOKE / REVALIDATE
  ↓
REBUILD FROM KNOWN-GOOD
  ↓
RESTORE ONLY TRUSTED STATE
  ↓
VERIFY BEFORE REINTRODUCTION
```

La detección, revocación, aislamiento y preservación de evidencia crítica no deben depender de la cooperación del componente sospechado.

Cuando un componente comprometido haya utilizado credenciales, escrito artefactos, producido estado o interactuado con otros componentes, esos activos pueden requerir revalidación. La relación no demuestra automáticamente compromiso; reduce el trust hasta recuperar evidencia suficiente.

Cuando sea posible, debe preferirse reconstruir desde un estado conocido y confiable antes que confiar en la autorreparación de un componente comprometido.

La destrucción definitiva no debe preceder a la preservación de evidencia forense necesaria.

---

## 11. Defensa activa, deception y respuesta a incidentes

La visión defensiva de Malāk permite, cuando existan las capacidades aprobadas y exclusivamente dentro de infraestructura propia o expresamente autorizada:

- detectar;
- bloquear;
- revocar;
- contener;
- aislar;
- degradar defensivamente;
- activar kill switches;
- utilizar deception, honeypots, honeynets, honeytokens y canary resources;
- observar comportamiento adversarial dentro de entornos contenidos;
- preservar evidencia;
- reconstruir attack paths;
- recuperar desde estado conocido;
- producir findings y propuestas de hardening;
- convertir incidentes reproducibles en candidatos de pruebas de regresión.

Los entornos de deception no deben contener secretos reales, credenciales válidas, datos personales reales, acceso al Kernel, Vault, repositorios productivos o redes no autorizadas.

El egress debe permanecer denegado por defecto cuando corresponda.

### 11.1 Atribución técnica limitada

Una IP, ASN, dominio, hash, fingerprint, user-agent u otro indicador representa evidencia técnica observada; no prueba por sí solo la identidad de una persona, organización, grupo o Estado.

Los informes deben distinguir, cuando corresponda:

```text
source_indicator
confidence
attribution_status
```

### 11.2 Límite de respuesta externa

Un ataque recibido no concede autoridad automática para acceder, alterar, inutilizar o comprometer infraestructura externa.

Malāk no realizará `hack back` autónomo.

Toda evaluación o acción fuera de infraestructura propia requiere autorización legal y técnica explícita, alcance definido, Rules of Engagement cuando corresponda y supervisión humana competente.

---

## 12. Datos, secretos y disclosure

Toda futura superficie que maneje datos persistentes, externos o sensibles deberá aplicar minimización y finalidad explícita.

El diseño deberá poder distinguir, según necesidad:

- sensibilidad;
- propietario u origen;
- finalidad permitida;
- dominio y scope;
- retención;
- exportación;
- uso por modelos remotos;
- persistencia en Memory;
- inclusión en evidencia o reportes;
- redaction;
- requisitos de consentimiento o revisión humana.

Regla:

```text
Having access to data
!=
permission to disclose, persist or reuse it
```

Los secretos y credenciales no deben registrarse íntegramente en logs, métricas, evidencia o reportes salvo que exista un protocolo forense expresamente aprobado que lo justifique.

---

## 13. Resource Governance y consumo acotado

Las futuras capacidades agentic, de retrieval, navegación, herramientas o investigación deberán operar bajo presupuestos y límites proporcionales.

Deberán poder limitar, cuando corresponda:

- tiempo;
- iteraciones;
- tool calls;
- CPU;
- RAM;
- VRAM;
- almacenamiento;
- red y egress;
- procesos;
- contexto;
- paralelismo;
- costos externos.

El agotamiento de recursos no debe interpretarse como permiso para ampliar cuotas o evadir controles.

---

## 14. Interoperabilidad externa

Malāk deberá mantenerse:

> **Protocol-ready, not protocol-dependent.**

MCP, A2A o protocolos equivalentes sólo podrán incorporarse mediante adapters gobernados cuando exista necesidad demostrada.

Reglas:

- un protocolo externo no constituye autoridad interna;
- identidad de protocolo no implica identidad o trust interno;
- metadata, schemas y tool descriptions no conceden permisos;
- cada operación protegida continúa subordinada al Security Control Plane;
- egress, secretos, recursos y scopes siguen gobernados por Malāk;
- los contratos internos de Malāk mantienen precedencia arquitectónica.

---

## 15. Mejora y aprendizaje bajo seguridad

Malāk puede observar su propio comportamiento, investigar, experimentar en entornos autorizados, generar evidencia y proponer mejoras.

No puede utilizar una mejora, incidente, emergencia o ventaja técnica como justificación para concederse autoridad adicional.

```text
Observation
  ↓
Evidence
  ↓
Finding
  ↓
Proposal
  ↓
Human / applicable governance
```

Queda prohibido:

```text
Observation or Incident
  ↓
autonomous authority expansion
  ↓
autonomous production modification
```

Las leyes fundacionales, políticas de seguridad, PDP/PEP y controles de integridad no pueden ser modificados por un componente para ampliar su propia autoridad.

---

## 16. Referencias de seguridad y assurance

Las revisiones podrán utilizar, por aplicabilidad, marcos reconocidos como:

- OWASP Top 10;
- OWASP para LLM/GenAI y aplicaciones agentic;
- NIST AI RMF y perfiles de ciberseguridad aplicables;
- NIST SSDF;
- MITRE ATLAS;
- OpenSSF/SLSA y referencias de supply chain;
- investigación académica y postmortems verificables.

Estos marcos son referencias de evaluación y no fuentes de autoridad superiores a las Constituciones, Blueprint o Gobernanza de Malāk.

No debe declararse cumplimiento total cuando sólo se evaluó un alcance parcial.

---

## 17. Documentos relacionados

### Fuentes normativas y estado implementado

- `docs/governance/cognitive_constitution.md`;
- `docs/governance/governance_constitution.md`;
- `docs/architecture/blueprint.md`;
- `docs/architecture/architecture_quality_gates.md`;
- `docs/project/project_context.md`;
- `docs/project/implementation_roadmap.md`;
- `docs/project/sprints/SPRINT-7.5.md`;
- `docs/project/sprints/SPRINT-7.6.md`;
- `docs/project/sprints/SPRINT-7.7.md`.

### Referencias conceptuales no normativas

- `documents/projects/jarvis/ideas.md`;
- `docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md`;
- `docs/project/concepts/GOVERNED_SWARM_LONG_HORIZON_REFERENCE.md`;
- `docs/project/concepts/GOVERNED_EPHEMERAL_AGENT_EXECUTION_EVIDENCE_REFERENCE.md`.

Las referencias conceptuales pueden orientar revisiones futuras, pero no autorizan implementación.

---

## 18. Reporte de vulnerabilidades

Malāk se encuentra en fase Alpha.

Las vulnerabilidades identificadas deberán documentarse de forma trazable y tratarse proporcionalmente a su severidad.

Cuando la información del finding pueda facilitar abuso antes de una corrección, debe evitarse publicar detalles operativos innecesarios en canales abiertos.

Toda corrección de seguridad deberá, cuando sea técnicamente viable:

- identificar causa raíz;
- preservar evidencia suficiente;
- incluir prueba negativa o de regresión;
- validar comportamiento fail-closed;
- revisar impacto en arquitectura y autoridad;
- documentar riesgo residual;
- preservar rollback.

---

## 19. Regla de cierre

La postura de seguridad de Malāk debe evolucionar con su superficie real de ataque.

No se deben construir controles para capacidades inexistentes sólo para completar una taxonomía externa; tampoco se debe habilitar una nueva superficie sensible sin revisar antes los límites de seguridad que la hacen aceptable.

Principio final:

> **Authority before autonomy. Identity before delegation. Governance before tools. Evidence before trust. Security boundary before agency.**
