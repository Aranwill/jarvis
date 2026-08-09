---
title: Hoja de ruta de implementación
status: activo
authority: no normativa
as_of_date: 2026-08-09
as_of_commit: 62bdc11c3ce16cb2cb54bb61bddfab4e39d689a8
branch: main
language: es
---

# Hoja de ruta de implementación

## Clasificación y autoridad

Este documento es derivado, informativo y no normativo.

Organiza propuestas preliminares de implementación, pero:

- no aprueba arquitectura;
- no autoriza cambios;
- no reemplaza las fuentes normativas;
- no establece automáticamente el próximo sprint;
- no convierte una recomendación en una obligación.

Ante cualquier conflicto prevalecen, en este orden:

1. Constitución Cognitiva;
2. Constitución de Gobernanza;
3. Blueprint;
4. especificaciones aprobadas;
5. ADR aceptados;
6. contratos públicos vigentes;
7. documentación operativa aprobada.

## Regla de admisión de sprints

La existencia, numeración, posición, título o ficha de un sprint no constituye autorización para implementarlo.

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

Sin esa aprobación no se debe crear una rama, modificar archivos ni iniciar una implementación.

La aprobación de un sprint anterior no autoriza automáticamente el siguiente.

El propietario puede aprobar, redefinir, diferir, reemplazar o descartar cualquier propuesta.

## Estado de referencia

- Rama permanente: `main`.
- HEAD verificado antes de iniciar la revisión integral y cierre del Sprint 7.5:
  `b4d1d512fe953d593608391390f82ab500fdc9d6`.
- Baseline nominal: `v0.6.0-alpha`.
- Suite completa validada durante el cierre: 304 pruebas aprobadas.
- `compileall` validado sin errores.
- `git diff --check` validado sin errores.
- Sprint 7.4 cerrado: `Consolidación de logs, métricas y auditoría`.
- Sprint 7.5 cerrado: `Security Control Plane Foundation`.
- El Kernel permanece desacoplado de runtimes, proveedores y modelos concretos.
- La CLI y el pipeline Kernel–Planner–Capability continúan siendo rutas separadas.
- No existe todavía una integración formal validada entre `Kernel.receive` y `ConversationService`.
- `main` es la única rama permanente del repositorio.

## Sprints cerrados del bloque 7.x

| Sprint | Estado | Resultado |
|---|---|---|
| 7.0 | Cerrado | CLI mínima con `MockLLMRuntime` |
| 7.1 | Cerrado | Composición de CLI con `OllamaRuntime` mediante configuración externa |
| 7.2 | Cerrado | Contrato estructural `RuntimeMetricSink` de solo escritura |
| 7.3 | Cerrado | Estabilización de la frontera de `ConversationProvider` |
| 7.4 | Cerrado | Consolidación de logs, métricas y auditoría; sincronización gobernada del Vault completada |
| 7.5 | Cerrado | Security Control Plane Foundation; autorización, PDP, PEP, auditoría y revisión integral completados |

## Estado de autorización de nuevos sprints

No existe un sprint posterior autorizado automáticamente por el cierre del Sprint 7.5.

Cualquier nueva unidad deberá ser inspeccionada, propuesta y aprobada explícitamente por el propietario antes de su implementación.

El Sprint 7.5 fue aprobado explícitamente por el propietario y quedó
cerrado después de completar seis incrementos pequeños, revisables y
reversibles.

El cierre integral confirmó:

- contratos de autorización estables;
- Policy Decision Point mínimo, determinista y fail-closed;
- Policy Enforcement Point separado de la lógica de negocio del Kernel;
- evidencia de auditoría estructurada e integrada de forma fail-closed;
- separación entre decisión, enforcement, auditoría y operación protegida;
- control humano y denegación por defecto preservados;
- ausencia de rutas operativas reales habilitadas por este sprint;
- 183 pruebas específicas de seguridad aprobadas;
- 304 pruebas totales aprobadas;
- `compileall` y `git diff --check` validados sin errores;
- ningún defecto bloqueante detectado durante la revisión integral.

El cierre del Sprint 7.5 no autoriza automáticamente ningún sprint
posterior ni habilita Secure Context Manager, persistencia de auditoría,
identidad criptográfica, TTL, nonce, prevención persistente de replay,
agentes, navegación o rutas operativas reales.

El Incremento 1 incorporó los contratos fundamentales:

- `PermissionScope`;
- `SecurityContext`;
- `AuthorizationRequest`;
- `AuthorizationDecision`.

La PR #15 fue mergeada en `main` mediante:

```text
c0a4283b100609daeb4b3422dd28634df9d851b6
```

La validación confirmó 45 pruebas específicas, 166 pruebas totales,
`compileall` correcto y `git diff --check` limpio.

El Incremento 2 — Activación y reconciliación documental — fue
completado e integrado mediante la PR #16 y el merge commit
`4afeed440a3bf2096035d0d458d2ef75c71689fd`. Su alcance quedó limitado a:

- cerrar documentalmente el Sprint 7.4;
- activar y reconciliar la ficha del Sprint 7.5;
- actualizar esta hoja de ruta;
- mantener `ideas.md` como consulta no normativa y sin modificaciones.

El Incremento 3 implementa un Policy Decision Point mínimo, determinista
y sin LLM. Incluye reglas exactas, denegación por defecto, evidencia
inmutable de confirmación humana y una frontera inyectable de
verificación. La validación confirmó 104 pruebas específicas, 225 pruebas
totales, `compileall` correcto y `git diff --check` limpio.

La semántica aprobada deniega la solicitud original cuando requiere
confirmación humana. Una confirmación verificada habilita únicamente la
evaluación desde cero de una solicitud nueva; no modifica la decisión
original, no concede permisos permanentes y no introduce un tercer
estado.

El Incremento 4 incorpora un Policy Enforcement Point inicial,
determinista y fail-closed. El PEP consulta directamente al PDP
inyectado, no acepta decisiones aportadas por el llamador y exige la
asociación exacta entre solicitud y decisión mediante `request_id`.

La operación protegida se ejecuta exactamente una vez solo ante una
decisión válida y permitida. Las denegaciones, los fallos del PDP, los
tipos de respuesta inválidos y las decisiones incongruentes bloquean la
operación. La validación confirmó 19 pruebas específicas y 244 pruebas
totales.

La ADR-002 formaliza esta frontera. La implementación permanece aislada
de Kernel, Planner, CLI, runtimes, Capability Registry y operaciones
reales. Fue integrada en `main` mediante la PR #19 y el merge commit
`af64b062aa1395ba7f7bdd59e5c1099ded68b683`.

El Incremento 5 incorporó posteriormente la evidencia de auditoría de
autorización mediante dos paquetes independientes:

1. Packet 5.1 — contratos mínimos de auditoría, integrado mediante la
   PR #22 y el merge commit
   `418358cc5b543c59cf4b113f42e762f6c78eec59`;
2. Packet 5.2 — integración fail-closed con el PEP, integrado mediante
   la PR #23 y el merge commit
   `38b0917c5b8dba5c5a4ef4db157e78ac428ab4bc`.

La reconciliación documental posterior cierra el Incremento 5 sin
habilitar rutas operativas reales ni ampliar autoridad.

El Incremento 6 — revisión integral y cierre — fue completado y validado
durante el cierre del Sprint 7.5. Su finalización no autoriza ningún
sprint posterior ni amplía el alcance operativo de Malāk.

### Cierre verificado del Sprint 7.4

El Sprint 7.4 fue integrado en `main` mediante `7cd7fcc`. Su
sincronización gobernada posterior quedó registrada como
`VSYNC-20260726-005`, con resultado `completed/pass`, y el Vault quedó
actualizado en `b20482c`.

Se conserva la evidencia técnica de cierre: 94 pruebas específicas,
121 pruebas totales, `compileall` y `git diff --check` aprobados.

La separación arquitectónica establecida permanece vigente:

- Las métricas miden rendimiento y comportamiento cuantificable.
- Los logs o eventos operativos permiten reconstruir ejecuciones y diagnosticar resultados o fallos.
- La auditoría evidencia decisiones, autorizaciones o acciones sensibles.
- Los tres subsistemas permanecen separados y no comparten contratos, stores, políticas de error, retención ni autoridad.
- Solo pueden compartir convenciones mínimas de trazabilidad, como identificadores estables, fechas UTC y nombres de eventos o componentes.
- `RuntimeMetricSample` y los stores de métricas existentes no se reutilizan para logs ni auditoría.
- No se crea un envelope universal de observabilidad.
- Para cada intento conversacional válido, la CLI genera exclusivamente
  el `request_id` utilizado para correlación, sin modificar
  `ConversationRequest` ni los demás contratos conversacionales.
- La auditoría de seguridad no se implementa en el Sprint 7.4; su frontera se preserva para el futuro Security Control Plane Foundation.
- El Kernel y `ConversationService` permanecen fuera del alcance.
- No se almacenan por defecto prompts completos, respuestas completas, secretos, credenciales ni contenido sensible innecesario.
- La evidencia producida no concede autoridad para modificar el sistema ni aplicar recomendaciones automáticamente.

La ficha operativa aprobada y sus incrementos se encuentran en:

```text
docs/project/sprints/SPRINT-7.4.md
```

### Registro de ideas y visión futura

El documento:

```text
documents/projects/jarvis/ideas.md
```

mantiene un catálogo evolutivo y no normativo de ideas, capacidades e iniciativas futuras de Malāk.

Su incorporación no aprueba automáticamente arquitectura, sprints ni implementación. Cada iniciativa deberá atravesar la revisión de necesidad, alcance, riesgos, dependencias, gobernanza y aprobación humana correspondiente.

Durante el Sprint 7.4 se incorporó para planificación futura la iniciativa:

**Sandbox Containment & Evaluation Evidence Foundation**

Su ubicación lógica será posterior a `Security Control Plane Foundation` y anterior a simulaciones con agentes o al `Controlled Engineering Improvement Loop Foundation`.

La iniciativa deberá abordar, mediante un sprint independiente:

- aislamiento y entornos descartables;
- control de red, archivos, procesos y herramientas;
- límites de CPU, RAM, VRAM, disco, tiempo y procesos;
- manifiestos reproducibles;
- telemetría externa al agente;
- registro verificable de operaciones;
- snapshots y hashes anteriores y posteriores;
- kill switch, timeout, cuarentena y cierre seguro;
- artefactos detallados de evaluación en un store separado;
- trazas experimentales de razonamiento opcionales y no autoritativas;
- pruebas de contención y revisión humana obligatoria.

Estado:

```text
Incorporada a la planificación futura.
Diseño detallado no aprobado.
Implementación no aprobada.
Sin número de sprint asignado.
```

Esta incorporación fue reflejada durante la sincronización gobernada
posterior al Sprint 7.4.

### Fundaciones paraguas incorporadas a planificación futura

Las siguientes líneas quedan incorporadas como planificación futura aprobada, sin diseño detallado, sin número de sprint y sin autorización de implementación.

#### Segmented Domain Governance Foundation

Propósito:

- preservar a Malāk como control plane horizontal;
- permitir Domain Packs subordinados a los documentos de ley;
- definir precedencia entre políticas globales, dominio, jurisdicción, organización y workflow;
- impedir que una capa inferior amplíe autoridad o contamine el Kernel con lógica sectorial.

Estado:

```text
Planificación futura aprobada.
Diseño detallado no aprobado.
Implementación no aprobada.
Sin número de sprint asignado.
```

#### Knowledge Intake & External Evidence Governance

Propósito:

- gobernar libros, papers, informes, webs y fuentes internas;
- conservar originales, procedencia, autoridad, licencias y vigencia;
- tratar Markdown, embeddings, índices y grafos como proyecciones reconstruibles;
- integrar búsqueda externa mediante autorización, sandbox, saneamiento y validación;
- prevenir autocontaminación y promoción automática de conclusiones.

Estado:

```text
Planificación futura aprobada.
Diseño detallado no aprobado.
Implementación no aprobada.
Sin número de sprint asignado.
```

#### Security Learning, Adversarial Evaluation & Deception

Propósito:

- habilitar laboratorios locales, CTF autorizados y formación asistida;
- evaluar agentes mediante observación externa;
- crear en el futuro un gemelo adversarial de Malāk, honeypots y deception defensiva aislada;
- transformar evidencia validada en pruebas y propuestas defensivas;
- establecer defensa activa dentro de fronteras propias y respuesta externa únicamente bajo autoridad legal, atribución validada, alcance explícito y supervisión humana.

Estado:

```text
Planificación futura aprobada.
Diseño detallado no aprobado.
Implementación no aprobada.
Sin número de sprint asignado.
```

Estas fundaciones dependen de `Security Control Plane Foundation` y de la futura `Sandbox Containment & Evaluation Evidence Foundation`. No habilitan agentes, navegación, malware, Tor, honeypots públicos, pentesting real, beta pública ni respuesta ofensiva.

## Propuestas pendientes de revisión y aprobación

| Propuesta | Estado | Observación |
|---|---|---|
| Preparación del AKS para GraphRAG | No aprobada | No implica implementar GraphRAG |
| Validación de baseline y release interna | No aprobada | Solo corresponde después de cerrar y sincronizar los bloques previos |

La tabla anterior no establece secuencia obligatoria.

El próximo sprint debe seleccionarse únicamente después de una revisión completa del baseline y de la necesidad real de Malāk.

## Regla de admisión de Capabilities

Una Capability solo podrá incorporarse cuando añada una funcionalidad real, necesaria y permanente para Malāk.

No se deben crear Capabilities con el único propósito de:

- validar routing;
- demostrar que el Planner selecciona múltiples entradas;
- comprobar que el Registry admite varias Capabilities;
- aumentar cobertura artificialmente;
- ejercitar infraestructura interna;
- completar una secuencia prevista;
- incorporar ejemplos sin utilidad funcional.

La infraestructura interna debe validarse mediante pruebas, dobles, fixtures, contratos e integración controlada.

## Restricción estructural

Antes de introducir agentes, herramientas externas, automatización del sistema operativo, navegación, mensajería externa, memoria sensible o Capabilities de alto riesgo, deben aprobarse e implementarse los fundamentos de seguridad y gobernanza correspondientes.

Ninguna propuesta futura puede:

- ampliar el Kernel con lógica de negocio;
- acoplar el Kernel a un runtime, proveedor, modelo o infraestructura concreta;
- introducir dependencias no aprobadas;
- modificar contratos centrales sin revisión específica;
- asumir que el hardware actual define la arquitectura permanente de Malāk.

## Fichas relacionadas

- `docs/project/sprints/SPRINT-7.0.md`
- `docs/project/sprints/SPRINT-7.1.md`
- `docs/project/sprints/SPRINT-7.2.md`
- `docs/project/sprints/SPRINT-7.3.md`
- `docs/project/sprints/SPRINT-7.4.md`
- `docs/project/sprints/SPRINT-7.5.md`
- `docs/project/sprints/SPRINT-7.6.md`
- `docs/project/sprints/SPRINT-7.7.md`

La ficha del Sprint 7.4 documenta un sprint cerrado, integrado y
sincronizado de forma gobernada.

La ficha del Sprint 7.5 documenta el sprint vigente aprobado y su
secuencia incremental. Las fichas 7.6 y 7.7 permanecen como propuestas
y no constituyen autorización de implementación.

## Regla de actualización

Este documento debe revalidarse cuando ocurra cualquiera de estos eventos:

- cambio material de `HEAD`;
- cierre de un sprint;
- modificación de contratos públicos;
- aceptación de un ADR relacionado;
- cambio de rama permanente;
- certificación de un nuevo baseline;
- cambio material de las reglas de gobernanza o ejecución.

Los snapshots históricos y releases certificadas no deben reescribirse para coincidir con este documento.
