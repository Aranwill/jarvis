---
title: Sprint 7.4 — Consolidación de logs, métricas y auditoría
status: en progreso
authority: operativa del sprint
as_of_commit: fd4da3d371d07b6aa91cc9f1c4d4bac3838ad627
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

## Necesidad verificada

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

Cuando exista una solicitud conversacional se reutilizará su `request_id`.

Un identificador de ejecución separado solo se incorporará si un proceso no dispone de `request_id` y el incremento correspondiente demuestra su necesidad.

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
- reutilizar `request_id` para correlación conversacional;
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
- reutilizar `request_id`;
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
```

deberá aprobarse después de inspeccionar su frontera exacta.

## Criterios de aceptación

- métricas, logs operativos y auditoría permanecen separados;
- los contratos y stores de métricas actuales conservan compatibilidad;
- los eventos operativos poseen un contrato mínimo e inmutable;
- el sink es de solo escritura;
- la persistencia operativa utiliza un store independiente;
- los fallos de persistencia tienen comportamiento explícito y probado;
- no se almacenan prompts, respuestas completas, secretos ni credenciales;
- la correlación reutiliza `request_id` cuando corresponde;
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

## Estado actual

```text
Sprint aprobado.
Rama creada desde el baseline oficial.
Incremento 1 documental en progreso.
Implementación de código todavía no iniciada.
```