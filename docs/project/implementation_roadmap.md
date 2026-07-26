---
title: Hoja de ruta de implementaciÃ³n
status: activo
authority: no normativa
as_of_date: 2026-07-26
as_of_commit: c0a4283b100609daeb4b3422dd28634df9d851b6
branch: main
language: es
---

# Hoja de ruta de implementaciÃ³n

## ClasificaciÃ³n y autoridad

Este documento es derivado, informativo y no normativo.

Organiza propuestas preliminares de implementaciÃ³n, pero:

- no aprueba arquitectura;
- no autoriza cambios;
- no reemplaza las fuentes normativas;
- no establece automÃ¡ticamente el prÃ³ximo sprint;
- no convierte una recomendaciÃ³n en una obligaciÃ³n.

Ante cualquier conflicto prevalecen, en este orden:

1. ConstituciÃ³n Cognitiva;
2. ConstituciÃ³n de Gobernanza;
3. Blueprint;
4. especificaciones aprobadas;
5. ADR aceptados;
6. contratos pÃºblicos vigentes;
7. documentaciÃ³n operativa aprobada.

## Regla de admisiÃ³n de sprints

La existencia, numeraciÃ³n, posiciÃ³n, tÃ­tulo o ficha de un sprint no constituye autorizaciÃ³n para implementarlo.

Cada propuesta debe someterse, como mÃ­nimo, a:

1. inspecciÃ³n completa del baseline vigente;
2. revisiÃ³n del cÃ³digo, pruebas y documentaciÃ³n aplicables;
3. identificaciÃ³n de una necesidad real y comprobada de MalÄk;
4. justificaciÃ³n de su utilidad cognitiva, arquitectÃ³nica, operativa o de gobernanza;
5. definiciÃ³n explÃ­cita del alcance y fuera de alcance;
6. evaluaciÃ³n de riesgos, dependencias, impacto y rollback;
7. validaciÃ³n mediante las cuatro preguntas obligatorias;
8. presentaciÃ³n y debate del plan de ejecuciÃ³n;
9. aprobaciÃ³n explÃ­cita e inequÃ­voca del propietario.

Sin esa aprobaciÃ³n no se debe crear una rama, modificar archivos ni iniciar una implementaciÃ³n.

La aprobaciÃ³n de un sprint anterior no autoriza automÃ¡ticamente el siguiente.

El propietario puede aprobar, redefinir, diferir, reemplazar o descartar cualquier propuesta.

## Estado de referencia

- Rama permanente: `main`.
- Commit de referencia: `c0a4283b100609daeb4b3422dd28634df9d851b6`.
- Baseline nominal: `v0.6.0-alpha`.
- Suite validada: 166 pruebas aprobadas.
- `compileall` validado sin errores.
- `git diff --check` validado sin errores.
- Sprint 7.4 cerrado: `ConsolidaciÃ³n de logs, mÃ©tricas y auditorÃ­a`.
- Sprint 7.5 aprobado y en progreso: `Base del plano de control de seguridad`.
- El Kernel permanece desacoplado de runtimes, proveedores y modelos concretos.
- La CLI y el pipeline Kernelâ€“Plannerâ€“Capability continÃºan siendo rutas separadas.
- No existe todavÃ­a una integraciÃ³n formal validada entre `Kernel.receive` y `ConversationService`.
- `main` es la Ãºnica rama permanente del repositorio.

## Sprints cerrados del bloque 7.x

| Sprint | Estado | Resultado |
|---|---|---|
| 7.0 | Cerrado | CLI mÃ­nima con `MockLLMRuntime` |
| 7.1 | Cerrado | ComposiciÃ³n de CLI con `OllamaRuntime` mediante configuraciÃ³n externa |
| 7.2 | Cerrado | Contrato estructural `RuntimeMetricSink` de solo escritura |
| 7.3 | Cerrado | EstabilizaciÃ³n de la frontera de `ConversationProvider` |
| 7.4 | Cerrado | ConsolidaciÃ³n de logs, mÃ©tricas y auditorÃ­a; sincronizaciÃ³n gobernada del Vault completada |

## Sprint vigente aprobado

| Sprint | Estado | Objetivo |
|---|---|---|
| 7.5 | En progreso | Establecer la base determinista del plano de control de seguridad |

El Sprint 7.5 fue aprobado explÃ­citamente por el propietario. Su
implementaciÃ³n se organiza mediante incrementos pequeÃ±os, revisables y
reversibles. La aprobaciÃ³n del sprint no autoriza automÃ¡ticamente cada
incremento pendiente.

El Incremento 1 incorporÃ³ los contratos fundamentales:

- `PermissionScope`;
- `SecurityContext`;
- `AuthorizationRequest`;
- `AuthorizationDecision`.

La PR #15 fue mergeada en `main` mediante:

```text
c0a4283b100609daeb4b3422dd28634df9d851b6
```

La validaciÃ³n confirmÃ³ 45 pruebas especÃ­ficas, 166 pruebas totales,
`compileall` correcto y `git diff --check` limpio.

El Incremento 2 â€” ActivaciÃ³n y reconciliaciÃ³n documental â€” estÃ¡
aprobado y en progreso. Queda limitado a:

- cerrar documentalmente el Sprint 7.4;
- activar y reconciliar la ficha del Sprint 7.5;
- actualizar esta hoja de ruta;
- mantener `ideas.md` como consulta no normativa y sin modificaciones.

La secuencia restante contempla, sujeta a revisiÃ³n y aprobaciÃ³n por
incremento:

1. Policy Decision Point mÃ­nimo, determinista y sin LLM;
2. Policy Enforcement Point inicial fuera de la lÃ³gica del Kernel;
3. evidencia de auditorÃ­a de autorizaciÃ³n;
4. revisiÃ³n integral y cierre.

Antes del PDP permanece pendiente resolver la semÃ¡ntica exacta de la
confirmaciÃ³n humana. No se modificarÃ¡ `AuthorizationDecision` ni se
introducirÃ¡ un tercer estado por inferencia.

### Cierre verificado del Sprint 7.4

El Sprint 7.4 fue integrado en `main` mediante `7cd7fcc`. Su
sincronizaciÃ³n gobernada posterior quedÃ³ registrada como
`VSYNC-20260726-005`, con resultado `completed/pass`, y el Vault quedÃ³
actualizado en `b20482c`.

Se conserva la evidencia tÃ©cnica de cierre: 94 pruebas especÃ­ficas,
121 pruebas totales, `compileall` y `git diff --check` aprobados.

La separaciÃ³n arquitectÃ³nica establecida permanece vigente:

- Las mÃ©tricas miden rendimiento y comportamiento cuantificable.
- Los logs o eventos operativos permiten reconstruir ejecuciones y diagnosticar resultados o fallos.
- La auditorÃ­a evidencia decisiones, autorizaciones o acciones sensibles.
- Los tres subsistemas permanecen separados y no comparten contratos, stores, polÃ­ticas de error, retenciÃ³n ni autoridad.
- Solo pueden compartir convenciones mÃ­nimas de trazabilidad, como identificadores estables, fechas UTC y nombres de eventos o componentes.
- `RuntimeMetricSample` y los stores de mÃ©tricas existentes no se reutilizan para logs ni auditorÃ­a.
- No se crea un envelope universal de observabilidad.
- Para cada intento conversacional vÃ¡lido, la CLI genera exclusivamente
  el `request_id` utilizado para correlaciÃ³n, sin modificar
  `ConversationRequest` ni los demÃ¡s contratos conversacionales.
- La auditorÃ­a de seguridad no se implementa en el Sprint 7.4; su frontera se preserva para el futuro Security Control Plane Foundation.
- El Kernel y `ConversationService` permanecen fuera del alcance.
- No se almacenan por defecto prompts completos, respuestas completas, secretos, credenciales ni contenido sensible innecesario.
- La evidencia producida no concede autoridad para modificar el sistema ni aplicar recomendaciones automÃ¡ticamente.

La ficha operativa aprobada y sus incrementos se encuentran en:

```text
docs/project/sprints/SPRINT-7.4.md
```

### Registro de ideas y visiÃ³n futura

El documento:

```text
documents/projects/jarvis/ideas.md
```

mantiene un catÃ¡logo evolutivo y no normativo de ideas, capacidades e iniciativas futuras de MalÄk.

Su incorporaciÃ³n no aprueba automÃ¡ticamente arquitectura, sprints ni implementaciÃ³n. Cada iniciativa deberÃ¡ atravesar la revisiÃ³n de necesidad, alcance, riesgos, dependencias, gobernanza y aprobaciÃ³n humana correspondiente.

Durante el Sprint 7.4 se incorporÃ³ para planificaciÃ³n futura la iniciativa:

**Sandbox Containment & Evaluation Evidence Foundation**

Su ubicaciÃ³n lÃ³gica serÃ¡ posterior a `Security Control Plane Foundation` y anterior a simulaciones con agentes o al `Controlled Engineering Improvement Loop Foundation`.

La iniciativa deberÃ¡ abordar, mediante un sprint independiente:

- aislamiento y entornos descartables;
- control de red, archivos, procesos y herramientas;
- lÃ­mites de CPU, RAM, VRAM, disco, tiempo y procesos;
- manifiestos reproducibles;
- telemetrÃ­a externa al agente;
- registro verificable de operaciones;
- snapshots y hashes anteriores y posteriores;
- kill switch, timeout, cuarentena y cierre seguro;
- artefactos detallados de evaluaciÃ³n en un store separado;
- trazas experimentales de razonamiento opcionales y no autoritativas;
- pruebas de contenciÃ³n y revisiÃ³n humana obligatoria.

Estado:

```text
Incorporada a la planificaciÃ³n futura.
DiseÃ±o detallado no aprobado.
ImplementaciÃ³n no aprobada.
Sin nÃºmero de sprint asignado.
```

Esta incorporaciÃ³n fue reflejada durante la sincronizaciÃ³n gobernada
posterior al Sprint 7.4.

## Propuestas pendientes de revisiÃ³n y aprobaciÃ³n

| Propuesta | Estado | ObservaciÃ³n |
|---|---|---|
| PreparaciÃ³n del AKS para GraphRAG | No aprobada | No implica implementar GraphRAG |
| ValidaciÃ³n de baseline y release interna | No aprobada | Solo corresponde despuÃ©s de cerrar y sincronizar los bloques previos |

La tabla anterior no establece secuencia obligatoria.

El prÃ³ximo sprint debe seleccionarse Ãºnicamente despuÃ©s de una revisiÃ³n completa del baseline y de la necesidad real de MalÄk.

## Regla de admisiÃ³n de Capabilities

Una Capability solo podrÃ¡ incorporarse cuando aÃ±ada una funcionalidad real, necesaria y permanente para MalÄk.

No se deben crear Capabilities con el Ãºnico propÃ³sito de:

- validar routing;
- demostrar que el Planner selecciona mÃºltiples entradas;
- comprobar que el Registry admite varias Capabilities;
- aumentar cobertura artificialmente;
- ejercitar infraestructura interna;
- completar una secuencia prevista;
- incorporar ejemplos sin utilidad funcional.

La infraestructura interna debe validarse mediante pruebas, dobles, fixtures, contratos e integraciÃ³n controlada.

## RestricciÃ³n estructural

Antes de introducir agentes, herramientas externas, automatizaciÃ³n del sistema operativo, navegaciÃ³n, mensajerÃ­a externa, memoria sensible o Capabilities de alto riesgo, deben aprobarse e implementarse los fundamentos de seguridad y gobernanza correspondientes.

Ninguna propuesta futura puede:

- ampliar el Kernel con lÃ³gica de negocio;
- acoplar el Kernel a un runtime, proveedor, modelo o infraestructura concreta;
- introducir dependencias no aprobadas;
- modificar contratos centrales sin revisiÃ³n especÃ­fica;
- asumir que el hardware actual define la arquitectura permanente de MalÄk.

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
y no constituyen autorizaciÃ³n de implementaciÃ³n.

## Regla de actualizaciÃ³n

Este documento debe revalidarse cuando ocurra cualquiera de estos eventos:

- cambio material de `HEAD`;
- cierre de un sprint;
- modificaciÃ³n de contratos pÃºblicos;
- aceptaciÃ³n de un ADR relacionado;
- cambio de rama permanente;
- certificaciÃ³n de un nuevo baseline;
- cambio material de las reglas de gobernanza o ejecuciÃ³n.

Los snapshots histÃ³ricos y releases certificadas no deben reescribirse para coincidir con este documento.