---
title: Sprint 7.5 — Base del plano de control de seguridad
status: cerrado
authority: operativa del sprint
as_of_commit: 62bdc11c3ce16cb2cb54bb61bddfab4e39d689a8
baseline_commit: 7cd7fcc
branch: main
language: es
---

# Sprint 7.5 — Base del plano de control de seguridad

## Autoridad y criticidad

Este documento define el alcance operativo aprobado del Sprint 7.5.

El sprint fue aprobado explícitamente por el propietario y quedó
cerrado después de completar sus incrementos y validaciones. Cada incremento requirió revisión y aprobación humana antes
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

- completado e integrado mediante la PR #16;
- merge commit: `4afeed440a3bf2096035d0d458d2ef75c71689fd`;
- Sprint 7.4 declarado formalmente como cerrado;
- Sprint 7.5 activado como aprobado y en progreso;
- hoja de ruta reconciliada con el baseline vigente;
- `ideas.md` mantenido sin cambios y sin autoridad operativa;
- ningún cambio de código incluido.

### Incremento 3 — Policy Decision Point mínimo

- semántica de confirmación humana aprobada por el propietario;
- contrato y responsabilidad del PDP definidos;
- implementación determinista inicial basada en reglas exactas;
- denegación por defecto y comportamiento fail-closed;
- ningún LLM participa en la decisión;
- evidencia de confirmación inmutable y verificador inyectado;
- pruebas de permisos, denegaciones, entradas inválidas y fallos
  seguros completadas;
- Kernel, Planner, CLI y runtimes sin cambios;
- completado e integrado mediante la PR #17;
- merge commit: `78799deabba5009e66c219220349e8202f5464bb`.

### Incremento 4 — Policy Enforcement Point inicial

- diseño e implementación aprobados por el propietario;
- frontera PDP–PEP formalizada mediante ADR-002;
- decisión obtenida internamente desde un PDP inyectado;
- decisión y ejecución separadas sin lógica de negocio en el Kernel;
- bloqueo ante denegación, fallo o decisión incongruente;
- operación protegida determinista y en memoria;
- implementación y validación completadas;
- completado e integrado mediante la PR #19;
- merge commit: `af64b062aa1395ba7f7bdd59e5c1099ded68b683`.

### Incremento 5 — Evidencia de auditoría de autorización

- completado mediante paquetes pequeños, revisables y reversibles;
- Packet 5.1 integrado mediante la PR #22 y el merge commit `418358cc5b543c59cf4b113f42e762f6c78eec59`;
- Packet 5.2 integrado mediante la PR #23 y el merge commit `38b0917c5b8dba5c5a4ef4db157e78ac428ab4bc`;
- incorpora evidencia mínima, estructurada, inmutable y segura;
- excluye secretos, prompts, outputs y contenido sensible innecesario;
- mantiene auditoría separada de métricas y eventos operativos;
- el `AuthorizationAuditSink` es obligatorio para el PEP inicial;
- un fallo de auditoría antes de una operación permitida bloquea la ejecución de forma fail-closed;
- ninguna evidencia de auditoría concede autoridad ni modifica una decisión de autorización;
- Kernel, Planner, CLI, runtimes y Capability Registry permanecen sin cambios;
- la integración continúa aislada de rutas operativas reales;
- reconciliación y cierre documental realizados en el Incremento 5.3.

Validación previa al cierre documental del Incremento 5:

- suite completa: 304 passed;
- `compileall`: PASS;
- `git diff --check`: PASS;
- working tree limpio antes de iniciar la reconciliación.

El cierre del Incremento 5 no autoriza el Incremento 6 ni habilita persistencia de auditoría, Secure Context Manager, rutas operativas reales o capacidades adicionales.

### Incremento 6 — Revisión integral y cierre

- revisión integral de contratos, PDP, PEP y auditoría completada;
- amenazas, privacidad, compatibilidad, comportamiento ante fallos y rollback revisados;
- separación entre decisión, enforcement, auditoría y operación protegida verificada;
- comportamiento fail-closed y pruebas negativas revisados;
- no se identificaron defectos bloqueantes ni necesidad de cambios de código;
- pruebas específicas de seguridad: 183 passed;
- suite completa: 304 passed;
- `compileall`: PASS;
- `git diff --check`: PASS;
- Kernel, Planner, CLI, runtimes y Capability Registry sin cambios;
- documentación final reconciliada mediante flujo gobernado de PR;
- el cierre del sprint no autoriza automáticamente ningún sprint posterior.

## Decisión aprobada — confirmación humana

`AuthorizationDecision` representa actualmente una decisión binaria
mediante `allowed=True` o `allowed=False`.

El propietario aprobó la siguiente semántica para las operaciones que
requieran confirmación humana:

1. La solicitud original se deniega de forma segura con
   `allowed=False` y `reason="human_confirmation_required"`.
2. La confirmación humana no modifica ni revierte esa decisión.
3. Después de la confirmación se debe emitir una solicitud nueva, con
   un `request_id` diferente.
4. La evidencia debe quedar ligada a la solicitud original, la solicitud
   nueva, el mismo sujeto y el mismo permiso exacto.
5. El PDP evalúa nuevamente la solicitud nueva desde cero.
6. Solo una nueva `AuthorizationDecision(allowed=True)` permite que un
   futuro PEP continúe.

La confirmación no constituye un permiso permanente, no amplía alcance,
no habilita elevación implícita y no garantiza por sí sola la
autorización final. Si la evidencia o su verificador no son confiables,
el PDP deniega la solicitud.

No se incorpora un tercer estado. Tampoco se incorporan firmas, TTL,
nonce, sesiones o renovación de contexto, porque pertenecen al futuro
Secure Context Manager y continúan fuera del alcance del Sprint 7.5.

## Implementación del Incremento 3

El PDP mínimo se implementa en `malak.security` mediante:

- `PolicyDecisionPoint`, contrato estructural de decisión;
- `StaticPolicyDecisionPoint`, primera implementación determinista;
- `PolicyRule`, regla exacta por sujeto y permiso;
- `PolicyEffect`, con efectos internos `ALLOW`, `DENY` y
  `REQUIRE_HUMAN_CONFIRMATION`;
- `HumanConfirmationEvidence`, evidencia inmutable;
- `HumanConfirmationVerifier`, frontera inyectable de verificación.

Los tres efectos son internos al PDP. La salida pública continúa siendo
exclusivamente `AuthorizationDecision` con resultado binario.

La implementación no admite comodines, herencia implícita, heurísticas,
interpretación de texto ni participación de LLM. Las reglas ausentes,
los sujetos no autenticados, la evidencia incongruente, la ausencia del
verificador y sus fallos producen denegaciones seguras.

Validación del Incremento 3:

- pruebas específicas: 104 passed;
- suite completa: 225 passed;
- `compileall`: PASS;
- `git diff --check`: PASS;
- Kernel, Planner, CLI y runtimes sin cambios;
- PEP, ejecución y auditoría de autorización fuera de alcance.

La implementación del PDP no habilita ninguna ejecución. El Incremento 4
fue diseñado y aprobado de forma independiente.

## Implementación del Incremento 4

El PEP inicial se implementa en `malak.security` mediante:

- `PolicyEnforcementPoint`, contrato estructural de enforcement;
- `StrictPolicyEnforcementPoint`, implementación inicial fail-closed;
- `ProtectedOperation`, contrato mínimo de una operación protegida;
- `AuthorizationDeniedError`, denegación explícita emitida por el PDP;
- `AuthorizationEnforcementError`, fallo o inconsistencia de
  enforcement.

El PEP no acepta una `AuthorizationDecision` aportada por el llamador.
Consulta directamente al `PolicyDecisionPoint` inyectado, valida el tipo
de la decisión y exige la coincidencia exacta de `request_id`. Solo una
decisión válida con `allowed=True` permite una única ejecución.

Las denegaciones, los fallos del PDP, las respuestas de tipo incorrecto
y las decisiones asociadas a otra solicitud bloquean la operación. Si la
operación protegida falla, su excepción se propaga sin reintento
automático.

Validación del Incremento 4:

- pruebas específicas: 19 passed;
- suite completa: 244 passed;
- `compileall`: PASS;
- `git diff --check`: PASS;
- Kernel, Planner, CLI, runtimes y Capability Registry sin cambios;
- operaciones reales, auditoría, sesiones, firmas, TTL, nonce y
  prevención persistente de replay fuera de alcance.

La implementación del Incremento 4 permanece aislada de rutas operativas
reales. Fue integrada en `main` mediante la PR #19 y el merge commit
`af64b062aa1395ba7f7bdd59e5c1099ded68b683`.

Posteriormente, el Incremento 5 incorporó los contratos de auditoría y su
integración fail-closed con el PEP mediante las PR #22 y #23. Ese trabajo
permanece igualmente aislado de rutas operativas reales.

El Incremento 5 quedó cerrado después de su reconciliación documental.
Posteriormente, el Incremento 6 completó la revisión integral y el cierre
del Sprint 7.5 sin ampliar su alcance ni autorizar ningún sprint posterior.

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
Sprint 7.5 cerrado — Security Control Plane Foundation.
Baseline inicial: 7cd7fcc.
Baseline previo al Incremento 6:
62bdc11c3ce16cb2cb54bb61bddfab4e39d689a8.

Incremento 1 — Contratos de autorización: completado.
Incremento 2 — Activación y reconciliación documental: completado.
Incremento 3 — Policy Decision Point mínimo: completado.
Incremento 4 — Policy Enforcement Point inicial: completado.
Incremento 5 — Evidencia de auditoría de autorización: completado.
Incremento 6 — Revisión integral y cierre: completado.

Validación final del cierre:
- 183 pruebas específicas de seguridad aprobadas;
- 304 pruebas totales aprobadas;
- compileall: PASS;
- git diff --check: PASS;
- sin defectos bloqueantes detectados;
- sin cambios funcionales requeridos durante el Incremento 6;
- Kernel, Planner, CLI, runtimes y Capability Registry intactos.

El cierre del Sprint 7.5 no autoriza automáticamente ningún sprint posterior.
```
