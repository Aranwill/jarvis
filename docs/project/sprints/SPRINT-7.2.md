---
title: Sprint 7.2 — Runtime Metric Sink Contract
status: implementación en validación
authority: operativa del sprint
as_of_commit: 920ac9ed908f72d599a308aa60afc91aa50a9e49
language: es
---

# Sprint 7.2 — Runtime Metric Sink Contract

## Autoridad y dependencia

Este documento define el alcance operativo del Sprint 7.2.

El sprint depende del baseline aceptado posterior al cierre del Sprint 7.1 y de la infraestructura de métricas de runtime ya existente.

No modifica el Blueprint, la Constitución Cognitiva, la Gobernanza, el Kernel ni los contratos conversacionales centrales.

## Objetivo

Desacoplar `OllamaRuntime` de una implementación concreta de almacenamiento de métricas mediante un contrato mínimo de escritura.

La dependencia objetivo es:

    OllamaRuntime
            ↓
    RuntimeMetricSink
            ├── InMemoryRuntimeMetricStore
            └── JsonlRuntimeMetricStore

## Decisión arquitectónica

`RuntimeMetricSink` se define como un `Protocol` estructural y expone únicamente:

    append(sample: RuntimeMetricSample) -> None

El contrato es intencionalmente de solo escritura.

No expone:

- lectura de muestras;
- filtrado;
- persistencia específica;
- perfilado;
- recomendaciones;
- configuración del runtime.

`OllamaRuntime` depende del contrato `RuntimeMetricSink` y no de `InMemoryRuntimeMetricStore`.

## Alcance implementado

- incorporación de `RuntimeMetricSink`;
- sustitución del tipo concreto en `OllamaRuntime`;
- preservación de la inyección opcional del sink;
- compatibilidad estructural con:
  - `InMemoryRuntimeMetricStore`;
  - `JsonlRuntimeMetricStore`;
- pruebas deterministas de composición;
- mantenimiento del comportamiento existente;
- ausencia de cambios en el Kernel y los contratos centrales.

## Fuera de alcance

- configuración de persistencia desde la CLI;
- nuevas variables de entorno;
- campañas de calibración;
- comparación de modelos;
- formatter o generación de informes;
- cambios de timeout;
- cambios de `keep_alive`;
- autoajuste;
- aplicación automática de recomendaciones;
- cambios en el Kernel;
- cambios en contratos conversacionales;
- nuevas dependencias.

## Criterios de aceptación

- `RuntimeMetricSink` expone únicamente `append(...)`;
- `OllamaRuntime` depende del contrato y no de un store concreto;
- ambos stores existentes pueden utilizarse como sinks;
- no cambia el comportamiento del runtime;
- suite completa en verde;
- compilación sin errores;
- diff sin errores de formato;
- documentación sincronizada;
- rollback simple y documentado.

## Validación

Estado validado durante el sprint:

    69 passed

Validaciones ejecutadas:

    python -m pytest -q
    python -m compileall src tests
    git diff --check

## Riesgo

Riesgo bajo.

La modificación afecta exclusivamente al contrato de dependencia de escritura de métricas.

No cambia persistencia, ejecución, configuración ni comportamiento observable.

## Rollback

El rollback consiste en:

1. restaurar el tipo `InMemoryRuntimeMetricStore` en `OllamaRuntime`;
2. eliminar `RuntimeMetricSink`;
3. eliminar las pruebas específicas del contrato;
4. revertir esta ficha documental.

El rollback no debe afectar stores, profiler, CLI, Kernel ni contratos conversacionales.