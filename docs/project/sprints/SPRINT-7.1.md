---
title: Sprint 7.1 — CLI con OllamaRuntime
status: completado
authority: no normativa
as_of_commit: 58eee58
language: es
---

# Sprint 7.1 — CLI con `OllamaRuntime`

## Autoridad y dependencia

Documento derivado y no normativo.

Este sprint depende del cierre aprobado del Sprint 7.0 y de la ruta de composición arquitectónica validada para la CLI técnica de Malāk.

No modifica el Blueprint, la Constitución Cognitiva, la Gobernanza ni la arquitectura del Kernel.

## Objetivo

Conectar la CLI técnica validada en el Sprint 7.0 con `OllamaRuntime` para realizar conversaciones locales reales mediante configuración externa, sin acoplar el Kernel a Ollama ni convertir la CLI en el pipeline cognitivo completo de Malāk.

## Arquitectura implementada

La composición queda ubicada en la frontera de aplicación:

```text
Variables de entorno
        ↓
CLIConfiguration
        ↓
build_runtime()
        ↓
LLMRuntime
├── MockLLMRuntime
└── OllamaRuntime
        ↓
MockConversationProvider
        ↓
ConversationProviderRegistry
        ↓
ConversationService
        ↓
run_cli()