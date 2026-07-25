---
title: Sprint 7.4 — Consolidación de logs, métricas y auditoría
status: en progreso
authority: operativa del sprint
as_of_commit: 5b951918006c464745e1eb1e3816bde619fad8b1
baseline_commit: fd4da3d371d07b6aa91cc9f1c4d4bac3838ad627
branch: feature/sprint-7.4-logs-metrics-audit
language: es
---

# Sprint 7.4 — Consolidación de logs, métricas y auditoría

## Autoridad y dependencia

Este documento define el alcance operativo aprobado del Sprint 7.4.

El sprint parte del baseline oficial posterior al cierre del Sprint 7.3:

```text
fd4da3d371d07b6aa91cc9f1c4d4bac3838ad627
```

La implementación fue aprobada explícitamente por el propietario después de:

- verificar el baseline vigente;
- relevar el código, las pruebas y la documentación;
- confirmar una necesidad real;
- revisar las fronteras arquitectónicas;
- definir alcance, exclusiones, riesgos y rollback;
- resolver conceptualmente la separación entre logs, métricas y auditoría.

El sprint no modifica el Blueprint, la Constitución Cognitiva, la Constitución de Gobernanza, el Kernel, el Planner, `ConversationService`, los contratos conversacionales ni el plano de autorización.

## Objetivo

Establecer una frontera mínima y estable de observabilidad operativa, manteniendo separados:

- métricas de rendimiento;
- logs o eventos operativos;
- evidencia de auditoría.

Los tres subsistemas podrán compartir convenciones mínimas de trazabilidad, pero no compartirán contratos, stores, políticas de error, retención ni autoridad.

El sprint no implementa una plataforma general de observabilidad ni concede autoridad automática a la telemetría.

## Necesidad verificada del baseline inicial

Esta sección se conserva como evidencia histórica del baseline inicial
del Sprint 7.4. No describe el estado actual de la implementación.

El baseline ya dispone de:

- `RuntimeMetricSample`;
- `RuntimeMetricSink`;
- `InMemoryRuntimeMetricStore`;
- `JsonlRuntimeMetricStore`;
- generación de métricas desde `OllamaRuntime`;
- persistencia y lectura de métricas en JSONL;
- un logger heredado basado en `logging`.

Sin embargo:

- no existe un contrato formal para eventos operativos;
- el logger heredado no define una frontera estable;
- no existe una política común de privacidad para eventos operativos;
- no existe una estrategia explícita de correlación;
- no existe una implementación real de auditoría;
- todavía debe impedirse que métricas, logs y auditoría se mezclen por conveniencia.

## Decisión arquitectónica

### Métricas

Las métricas miden rendimiento y comportamiento cuantificable.

Sus contratos y stores actuales se mantienen separados y compatibles.

`RuntimeMetricSample` no será reutilizado como log operativo ni como evidencia de auditoría.

### Logs o eventos operativos

Los eventos operativos permitirán reconstruir qué ocurrió durante una ejecución y diagnosticar resultados o fallos.

No almacenarán por defecto:

- prompts completos;
- respuestas completas;
- secretos;
- credenciales;
- contenido sensible innecesario.

### Auditoría

La auditoría evidenciará decisiones, autorizaciones o acciones sensibles.

El Sprint 7.4 define y preserva su frontera, pero no implementa auditoría de seguridad.

La auditoría vinculada al plano de autorización corresponderá al Sprint 7.5 y requerirá su propio alcance aprobado.

### Trazabilidad compartida

Los subsistemas podrán compartir únicamente convenciones mínimas, como:

- identificadores estables;
- fechas UTC;
- nombres de eventos o componentes.

No se creará un envelope universal de observabilidad.

Para cada prompt válido que alcanza un intento conversacional, la CLI
genera exclusivamente un nuevo `request_id`.

El identificador se incorpora a los eventos operativos correlacionados,
pero no a `ConversationRequest` ni a los demás contratos
conversacionales, que permanecen intactos.

## Alcance aprobado

- formalizar la separación entre métricas, logs operativos y auditoría;
- mantener intactos y compatibles los contratos y stores de métricas existentes;
- crear un contrato mínimo e inmutable para eventos operativos;
- crear una interfaz de solo escritura para eventos operativos;
- crear un store en memoria para pruebas deterministas;
- incorporar persistencia JSONL local para eventos operativos;
- definir límites de almacenamiento o una política equivalente;
- definir y probar el comportamiento ante fallos de escritura;
- aplicar una allowlist estricta de campos;
- excluir contenido sensible;
- generar exclusivamente en la CLI el `request_id` utilizado para
  correlación conversacional, sin modificar los contratos
  conversacionales;
- evaluar una integración mínima únicamente en la frontera de aplicación o CLI;
- documentar la frontera que separa la observabilidad operativa de la auditoría de seguridad;
- validar privacidad, compatibilidad, reversibilidad y comportamiento ante errores.

## Fuera de alcance

- implementar auditoría de seguridad;
- implementar autorización;
- implementar PDP o PEP;
- modificar el Kernel;
- modificar el Planner;
- modificar `ConversationService`;
- integrar `Kernel.receive` con `ConversationService`;
- modificar contratos conversacionales;
- crear un envelope universal;
- unificar logs, métricas y auditoría;
- reutilizar el store JSONL de métricas para otros registros;
- persistir prompts o respuestas completas por defecto;
- almacenar secretos o credenciales;
- implementar automatizaciones basadas en telemetría;
- aplicar recomendaciones automáticamente;
- implementar el futuro ciclo de mejora controlada;
- reemplazar masivamente el logger heredado;
- incorporar una plataforma externa de observabilidad;
- incorporar dependencias externas;
- modificar el Vault durante la implementación del sprint.

## Incrementos aprobados

### Incremento 1 — Activación documental

- convertir la ficha preliminar en alcance operativo aprobado;
- actualizar el roadmap oficial;
- registrar la separación entre métricas, logs y auditoría;
- mantener el código sin cambios.

### Incremento 2 — Contrato de evento operativo

- definir un contrato mínimo e inmutable;
- aplicar una allowlist estricta de campos;
- excluir contenido sensible;
- añadir pruebas deterministas.

### Incremento 3 — Sink y store en memoria

- definir una interfaz de solo escritura;
- implementar un store en memoria;
- probar orden, escritura y recuperación necesaria para tests.

### Incremento 4 — Persistencia JSONL

- implementar persistencia separada de las métricas;
- definir límites de escritura o política equivalente;
- definir el comportamiento ante errores;
- probar líneas válidas, inválidas y fallos de persistencia.

### Incremento 5 — Integración mínima

- inspeccionar la frontera de aplicación o CLI;
- integrar únicamente eventos operativos justificados;
- generar el `request_id` exclusivamente en la CLI sin modificar
  `ConversationRequest` ni los demás contratos conversacionales;
- preservar el comportamiento observable existente;
- mantener intactos el Kernel y `ConversationService`.

### Incremento 6 — Privacidad y revisión arquitectónica

- verificar que no se persistan prompts, respuestas, secretos ni datos sensibles;
- confirmar la separación entre los tres subsistemas;
- revisar compatibilidad y crecimiento del almacenamiento.

### Incremento 7 — Validación y cierre

- ejecutar pruebas específicas;
- ejecutar la suite completa;
- validar `compileall`;
- validar `git diff --check`;
- completar la documentación;
- preparar PR y cierre gobernado.

### Incremento 8 — Sincronización gobernada del Vault

Después del merge aprobado en `main`:

- ejecutar manualmente el Vault Synchronization Agent;
- revisar la evidencia producida;
- proponer los documentos del Vault que deban actualizarse;
- esperar aprobación antes de escribir;
- crear un nuevo snapshot si cambió el baseline;
- preservar todos los snapshots históricos.

## Archivos previstos

La lista se confirmará antes de cada incremento:

```text
docs/project/sprints/SPRINT-7.4.md
docs/project/implementation_roadmap.md

src/malak/observability/__init__.py
src/malak/observability/operational_event.py
src/malak/observability/operational_event_sink.py
src/malak/observability/operational_event_store.py
src/malak/observability/operational_event_jsonl_store.py

tests/test_operational_event.py
tests/test_operational_event_sink.py
tests/test_operational_event_store.py
tests/test_operational_event_jsonl_store.py
```

Cualquier integración con:

```text
src/malak/app/cli.py
tests/test_cli.py
```

fue aprobada después de inspeccionar su frontera exacta y quedó
limitada a esos dos archivos durante el Incremento 5.

## Criterios de aceptación

- métricas, logs operativos y auditoría permanecen separados;
- los contratos y stores de métricas actuales conservan compatibilidad;
- los eventos operativos poseen un contrato mínimo e inmutable;
- el sink es de solo escritura;
- la persistencia operativa utiliza un store independiente;
- los fallos de persistencia tienen comportamiento explícito y probado;
- no se almacenan prompts, respuestas completas, secretos ni credenciales;
- la correlación utiliza el `request_id` generado exclusivamente en la
  CLI, sin modificar `ConversationRequest` ni los demás contratos
  conversacionales;
- el Kernel permanece sin cambios;
- `ConversationService` permanece sin cambios;
- no se implementa autorización ni auditoría de seguridad;
- no se incorporan dependencias externas;
- la suite completa queda en verde;
- el rollback permanece simple y trazable.

## Riesgos y controles

### Exposición de información sensible

Control:

- allowlist estricta;
- ausencia de campos de contenido libre;
- pruebas específicas de privacidad;
- exclusión explícita de prompts, respuestas, secretos y credenciales.

### Crecimiento del almacenamiento

Control:

- límites de escritura, rotación o política equivalente;
- archivos separados por subsistema;
- comportamiento documentado y probado.

### Mezcla entre telemetría y auditoría

Control:

- contratos separados;
- stores separados;
- propósitos separados;
- políticas de error y retención independientes.

### Fallos de persistencia

Control:

- comportamiento explícito;
- pruebas de fallo;
- la observabilidad no debe corromper silenciosamente la ejecución principal.

### Expansión de responsabilidades

Control:

- integración únicamente en fronteras justificadas;
- Kernel y `ConversationService` fuera de alcance;
- revisión y aprobación incremental.

## Rollback

Cada incremento se implementará mediante commits pequeños y reversibles.

El rollback podrá retirar:

- contratos de eventos operativos;
- sinks;
- stores;
- persistencia JSONL;
- integración mínima;
- pruebas y documentación asociadas.

El rollback no requerirá migrar ni modificar los archivos JSONL de métricas existentes.

Si el Sprint 7.4 se revierte completamente, el baseline del Sprint 7.3 continuará operativo.

## Validación de gobernanza

### ¿Respeta el Blueprint?

Sí. Añade observabilidad mediante fronteras desacopladas y preserva los contratos centrales.

### ¿Respeta la Constitución Cognitiva?

Sí. La telemetría produce evidencia, pero no adquiere autoridad para modificar el sistema.

### ¿Respeta la Constitución de Gobernanza?

Sí. Mantiene separación de responsabilidades, trazabilidad, privacidad, revisión humana y reversibilidad.

### ¿Simplifica o mantiene simple el Kernel?

Sí. El Kernel permanece completamente fuera del alcance y no recibe nuevas dependencias.

## Anexo documental posterior al Incremento 1

Durante la revisión previa al Incremento 2 se formalizó:

```text
documents/projects/jarvis/ideas.md
```

como registro evolutivo y no normativo de ideas y visión futura de Malāk.

El documento preserva iniciativas para su evaluación posterior, pero no posee autoridad para aprobar sprints, modificar el roadmap, definir arquitectura implementada ni autorizar cambios de código.

Entre las iniciativas registradas se encuentra `Sandbox Containment & Evaluation Evidence Foundation`, incorporada a la planificación futura para controlar, contener y producir evidencia externa de las ejecuciones realizadas en sandboxes.

Esta incorporación:

- no amplía la implementación técnica del Sprint 7.4;
- no implementa sandboxes, agentes ni simulaciones;
- no implementa el futuro ciclo de mejora controlada;
- no convierte trazas de razonamiento en evidencia autoritativa;
- no modifica el Kernel ni `ConversationService`;
- deberá reflejarse en la próxima sincronización gobernada del Vault.

## Estado actual

```text
Sprint 7.4 aprobado y en progreso.
Rama: feature/sprint-7.4-logs-metrics-audit.
Baseline inicial: fd4da3d371d07b6aa91cc9f1c4d4bac3838ad627.

Incremento 1 — Activación documental:
- cerrado en el commit ab586f4.

Incremento 2 — Contrato de evento operativo:
- cerrado en el commit 9759525;
- contrato mínimo e inmutable implementado;
- allowlist y validaciones deterministas incorporadas.

Incremento 3 — Sink y store en memoria:
- cerrado en el commit 3c0cf90;
- sink de solo escritura y store en memoria implementados;
- orden de inserción y copias defensivas validados.

Incremento 4 — Persistencia JSONL:
- cerrado en el commit 8f9ab23;
- persistencia append-only separada de las métricas;
- allowlist de seis campos;
- límite máximo de 4096 bytes por línea;
- errores de persistencia explícitos y probados.

Incremento 5 — Integración mínima:
- implementado y validado;
- alcance limitado a src/malak/app/cli.py y tests/test_cli.py;
- commit de implementación:
  f1452a109142b6e9186fe59de89a641651b38558;
- generación del request_id exclusivamente en la CLI;
- emisión correlacionada de conversation.started y
  conversation.succeeded para el intento exitoso;
- comportamiento ante fallos del servicio y del sink probado;
- compatibilidad sin sink preservada;
- sin persistencia implícita ni creación automática de stores.

Validaciones del Incremento 5:
- pruebas específicas de CLI: 23 passed;
- suite completa: 121 passed;
- compileall: PASS;
- git diff --check: PASS.

Evidencia preservada de la validación en sandbox:
- UUID generado por la CLI:
  b2077885-2956-418b-8721-62fd844fb091;
- primer evento: conversation.started;
- segundo evento: conversation.succeeded;
- ambos eventos contienen exactamente el mismo request_id;
- request_id validado como UUID;
- correlación: PASS;
- sandbox temporal y JSONL eliminados de forma controlada después de
  la revisión y aprobación humanas;
- UUID y resultado de correlación preservados en esta ficha.

El Kernel, el Planner, ConversationService y los contratos
conversacionales permanecieron intactos.

Incremento 6 — Privacidad y revisión arquitectónica:
- completado y validado mediante inspección de solo lectura;
- revisión ejecutada sobre el HEAD:
  7ef432d209eaba9d34828ebcbdb25b7d41797488;
- revisión humana aprobada;
- resultado general: APTO;
- no se identificaron hallazgos bloqueantes.

Resultados del Incremento 6:
- privacidad de los eventos persistidos: PASS;
- ausencia de prompts, respuestas del modelo, contenido
  conversacional, secretos y datos sensibles: PASS;
- minimización de metadatos: PASS;
- separación entre métricas, eventos operativos y auditoría: PASS;
- ausencia de semántica de autorización o seguridad: PASS;
- degradación controlada ante fallos del sink o del almacenamiento:
  PASS;
- compatibilidad con los contratos existentes: PASS;
- Kernel, Planner, ConversationService y contratos conversacionales
  permanecen intactos;
- no se incorporaron dependencias externas;
- rollback simple y trazable;
- suite completa: evidencia vigente de 121 passed, no reejecutada
  durante la inspección del Incremento 6.

Deuda futura no bloqueante, fuera del alcance del Sprint 7.4:
- validación adicional de identificadores;
- control de exposición de errores;
- rotación y límites de crecimiento;
- retención y eliminación;
- concurrencia;
- recuperación ante corrupción parcial;
- permisos del archivo persistido.

Estas observaciones no requieren correcciones dentro del Sprint 7.4
ni amplían su alcance aprobado.

Incremento 7 — Validación y cierre:
- completado y validado;
- revisión humana aprobada;
- conclusión general: APTO;
- validación integral ejecutada sobre el HEAD:
  5b951918006c464745e1eb1e3816bde619fad8b1;
- pruebas específicas: 94 passed;
- suite completa: 121 passed;
- compileall: PASS;
- git diff --check del working tree: PASS;
- git diff --check main...HEAD: PASS;
- alcance sometido a validación integral:
  14 archivos modificados respecto de main,
  2084 inserciones y 44 eliminaciones;
- privacidad: PASS;
- separación arquitectónica: PASS;
- compatibilidad con los contratos existentes: PASS;
- rollback simple y trazable: PASS;
- Kernel, Planner, ConversationService y contratos conversacionales
  permanecen intactos;
- no se incorporaron dependencias externas;
- no se identificaron hallazgos bloqueantes;
- la deuda futura del Incremento 6 se conserva como no bloqueante y
  fuera del alcance del Sprint 7.4;
- rama lista para preparar el PR.

Siguiente paso:
- preparar el PR mediante el flujo gobernado y la aprobación humana
  correspondiente;
- después del merge aprobado en `main`, ejecutar el Incremento 8
  exclusivamente como sincronización gobernada del Vault;
- el Incremento 8 no constituye implementación operativa dentro de
  Malāk.

El cierre técnico previo al PR quedó validado. El Sprint 7.4 permanece
en progreso porque el Incremento 8 continúa pendiente y sólo puede
ejecutarse después del merge aprobado en `main`.
```
