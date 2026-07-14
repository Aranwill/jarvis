---
title: Sprint 7.5 — Base del plano de control de seguridad
status: borrador estructural
authority: no normativa
as_of_commit: 71d13fc0ee431b9574fcfb5dbc52baf8cb6e4c4c
language: es
---

# Sprint 7.5 — Base del plano de control de seguridad

## Autoridad y criticidad

Documento derivado y no normativo. No autoriza implementación. Es un sprint estructural de riesgo alto que requiere diseño aprobado, trazabilidad en el AKS y ADR cuando la solución cambie o precise la arquitectura vigente.

## Objetivo preliminar

Establecer una base determinista para solicitar, decidir, aplicar y auditar autorizaciones, preservando el control humano y la denegación por defecto.

## Principios obligatorios

- El usuario conserva la máxima autoridad operativa.
- Solicitar, autorizar, ejecutar y auditar son responsabilidades separadas.
- Ningún LLM toma decisiones de autorización.
- Las operaciones sensibles se deniegan por defecto.
- Las decisiones son explícitas, trazables y reversibles cuando sea posible.
- Ningún componente puede elevar sus propios permisos.

## Contratos candidatos sujetos a aprobación

- `AuthorizationRequest`.
- `AuthorizationDecision`.
- `SecurityContext`.
- `PermissionScope`.

Los nombres, propietarios, ubicación y semántica son preliminares hasta su aprobación arquitectónica.

## Alcance preliminar

- Formalizar el modelo de autoridad y la clasificación de operaciones.
- Diseñar un Policy Decision Point mínimo, determinista y sin LLM.
- Diseñar un Policy Enforcement Point inicial fuera de la lógica de negocio del Kernel.
- Definir decisiones permitidas, denegadas y condicionadas a confirmación humana.
- Registrar evidencia suficiente de cada decisión sin filtrar secretos.
- Probar caminos permitidos, denegados, inválidos y de fallo seguro.
- Preparar la base conceptual del futuro Secure Context Manager sin implementarlo por adelantado.

## Fuera de alcance

- Ejecutar herramientas externas.
- Agentes autónomos, navegación o automatización del sistema operativo.
- Memoria sensible con escritura.
- Autorización basada en prompts, modelos o heurísticas no deterministas.
- Debilitar controles existentes para facilitar pruebas.

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
