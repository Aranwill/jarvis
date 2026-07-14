---
title: Sprint 7.4 — Consolidación de logs, métricas y auditoría
status: borrador preliminar
authority: no normativa
as_of_commit: 71d13fc0ee431b9574fcfb5dbc52baf8cb6e4c4c
language: es
---

# Sprint 7.4 — Consolidación de logs, métricas y auditoría

## Autoridad y dependencia

Documento derivado y no normativo. No autoriza implementación. La estructura de eventos y la política de datos requieren revisión de arquitectura y gobernanza.

## Objetivo preliminar

Separar y estabilizar observabilidad operativa, métricas de rendimiento y evidencia de auditoría sin almacenar contenido sensible innecesario.

## Alcance preliminar

- Definir una estructura estable para eventos operativos.
- Separar logs, métricas y auditoría por propósito y retención.
- Introducir identificadores de ejecución trazables.
- Definir límites, rotación o políticas equivalentes para almacenamiento local.
- Gestionar fallos de escritura sin ocultar errores ni corromper la ejecución.
- Revisar qué campos son necesarios y cuáles deben excluirse o redactarse.
- Mantener compatibilidad explícita con los stores de métricas existentes.

## Fuera de alcance

- Plataforma externa de observabilidad.
- Persistencia de prompts completos por defecto.
- Automatización de acciones a partir de métricas.
- Cambios al Kernel o a contratos públicos sin decisión aprobada.
- Implementar el plano de autorización del Sprint 7.5.

## Criterios preliminares de aceptación

- Cada tipo de registro tiene propósito, esquema, propietario y política de error.
- Los identificadores permiten reconstruir una ejecución sin exponer datos innecesarios.
- Los fallos de persistencia tienen comportamiento probado.
- La retrocompatibilidad o migración está documentada.
- Suite completa en verde y revisión específica de datos sensibles.

## Riesgo

Riesgo: medio por privacidad, crecimiento de almacenamiento y posible mezcla entre telemetría y auditoría.
