---
title: Sprint 7.5 — Base del plano de control de seguridad
status: en progreso
authority: operativa del sprint
as_of_commit: c0a4283b100609daeb4b3422dd28634df9d851b6
baseline_commit: 7cd7fcc
branch: main
language: es
---

# Sprint 7.5 — Base del plano de control de seguridad

## Autoridad y criticidad

Este documento define el alcance operativo aprobado del Sprint 7.5.

El sprint fue aprobado explícitamente por el propietario y se encuentra
en progreso. Cada incremento requiere revisión y aprobación humana antes
de implementarse. La aprobación del sprint no autoriza por sí sola los
incrementos pendientes ni amplía su alcance.

Es un sprint estructural de riesgo alto. Requiere trazabilidad en el AKS
y ADR cuando una decisión cambie o precise la arquitectura vigente.

## Objetivo

Establecer una base determinista para solicitar, decidir, aplicar y auditar autorizaciones, preservando el control humano y la denegación por defecto.

## Principios obligatorios

- El usuario conserva la máxima autoridad operativa.
- Solicitar, autorizar, ejecutar y auditar son responsabilidades separadas.
- Ningún LLM toma decisiones de autorización.
- Las operaciones sensibles se deniegan por defecto.
- Las decisiones son explícitas, trazables y reversibles cuando sea posible.
- Ningún componente puede elevar sus propios permisos.

## Contratos fundamentales implementados

- `AuthorizationRequest`.
- `AuthorizationDecision`.
- `SecurityContext`.
- `PermissionScope`.

Los cuatro contratos fueron aprobados, implementados y publicados en
`malak.security` mediante la PR #15.

La integración quedó incorporada en `main` mediante:

```text
c0a4283b100609daeb4b3422dd28634df9d851b6
```

Validación del primer incremento:

- pruebas específicas: 45 passed;
- suite completa: 166 passed;
- `compileall`: PASS;
- `git diff --check`: PASS;
- Kernel, Planner y runtimes sin cambios;
- ningún LLM participa en decisiones de autorización.

## Alcance aprobado

- formalizar el modelo de autoridad y la clasificación de operaciones;
- mantener contratos mínimos, inmutables y desacoplados;
- implementar un Policy Decision Point mínimo, determinista y sin LLM;
- implementar un Policy Enforcement Point inicial fuera de la lógica
  de negocio del Kernel;
- definir y probar decisiones permitidas, denegadas, inválidas y de
  fallo seguro;
- registrar evidencia mínima y segura de las decisiones;
- preservar la separación entre solicitar, decidir, ejecutar y auditar;
- documentar riesgos, rollback y límites de cada incremento;
- cerrar el sprint únicamente después de la revisión integral y la
  aprobación humana.

## Fuera de alcance

- Ejecutar herramientas externas.
- Agentes autónomos, navegación o automatización del sistema operativo.
- Memoria sensible con escritura.
- Autorización basada en prompts, modelos o heurísticas no deterministas.
- Debilitar controles existentes para facilitar pruebas.
- Implementar el Secure Context Manager.
- Incorporar identidad criptográfica, sesiones firmadas, TTL, nonce o
  elevación de confianza.
- Modificar el Kernel, el Planner o los runtimes.
- Usar `ideas.md` como fuente normativa o como autorización para ampliar
  este sprint.

## Secuencia incremental aprobada

### Incremento 1 — Contratos de autorización

- completado e integrado mediante la PR #15;
- merge commit: `c0a4283b100609daeb4b3422dd28634df9d851b6`;
- cuatro contratos fundamentales expuestos en `malak.security`;
- 45 pruebas específicas y 166 pruebas totales aprobadas.

### Incremento 2 — Activación y reconciliación documental

- declarar formalmente el Sprint 7.4 como cerrado;
- activar el Sprint 7.5 como aprobado y en progreso;
- reconciliar la hoja de ruta con el baseline vigente;
- registrar el Incremento 1 y la secuencia restante;
- mantener `ideas.md` sin cambios y sin autoridad operativa;
- no modificar código.

### Incremento 3 — Policy Decision Point mínimo

- definir su contrato y responsabilidad exacta;
- aplicar denegación por defecto;
- mantener comportamiento determinista y sin LLM;
- resolver previamente la semántica de confirmación humana;
- probar permisos, denegaciones, entradas inválidas y fallos seguros.

### Incremento 4 — Policy Enforcement Point inicial

- aplicar decisiones sin incorporar lógica de negocio al Kernel;
- separar decisión y ejecución;
- impedir bypass y elevación implícita;
- probar enforcement y comportamiento ante ausencia o invalidez de una
  decisión.

### Incremento 5 — Evidencia de auditoría de autorización

- registrar evidencia mínima, estructurada y segura;
- excluir secretos y contenido sensible;
- preservar la separación respecto de métricas y eventos operativos;
- definir comportamiento ante fallos de auditoría.

### Incremento 6 — Revisión integral y cierre

- revisar amenazas, privacidad, compatibilidad y rollback;
- ejecutar pruebas específicas y suite completa;
- validar `compileall` y `git diff --check`;
- completar la documentación y el flujo gobernado de PR;
- proponer la sincronización del Vault después del cierre aprobado.

## Decisión pendiente — confirmación humana

`AuthorizationDecision` representa actualmente una decisión binaria
mediante `allowed=True` o `allowed=False`.

Antes de implementar el PDP debe aprobarse la semántica exacta para las
operaciones que requieran confirmación humana. No se incorporará un tercer
estado ni se modificará el contrato por inferencia.

La recomendación provisional, todavía no aprobada como implementación,
es tratar la necesidad de confirmación como una denegación segura hasta
recibir confirmación explícita y emitir una nueva solicitud. Esta opción
mantiene el comportamiento fail-closed y evita convertir una decisión
pendiente en autorización implícita.

## Puertas de aceptación

- Modelo de autoridad y propietarios de contratos aprobados.
- ADR y Decision Index actualizados cuando corresponda.
- Denegación por defecto demostrada mediante pruebas.
- Separación entre decisión y ejecución verificada.
- Control humano y trazabilidad verificables.
- Revisión de amenazas, rollback y comportamiento ante fallos completados.
- Suite completa en verde.

## Restricción de secuencia

Este sprint debe completarse antes de agentes, herramientas externas, automatización del sistema operativo, navegación, mensajería externa, memoria sensible o Capabilities de alto riesgo.

## Riesgo y rollback

Riesgo: alto. El rollback debe preservar evidencia de decisiones y evitar dejar rutas de ejecución sin enforcement.

Cada incremento se implementará mediante cambios pequeños, trazables y
reversibles. Si un incremento no supera sus validaciones, no se avanzará
al siguiente.

## Estado actual

```text
Sprint 7.5 aprobado y en progreso.
Baseline inicial: 7cd7fcc.
HEAD de referencia: c0a4283b100609daeb4b3422dd28634df9d851b6.

Incremento 1 — Contratos de autorización:
- completado;
- PR #15 mergeada;
- 45 pruebas específicas aprobadas;
- 166 pruebas totales aprobadas.

Incremento 2 — Activación y reconciliación documental:
- aprobado;
- en progreso;
- limitado a SPRINT-7.4.md, SPRINT-7.5.md e
  implementation_roadmap.md;
- sin cambios de código;
- ideas.md consultado y mantenido intacto.

Incrementos 3 a 6:
- pendientes de diseño incremental, revisión y aprobación humana.

Decisión pendiente antes del PDP:
- semántica de confirmación humana.
```