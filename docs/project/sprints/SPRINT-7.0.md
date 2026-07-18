---
title: Sprint 7.0 - CLI mínima con MockLLMRuntime
status: implementación validada
authority: operativa del sprint
language: es
---

# Sprint 7.0 — CLI mínima con `MockLLMRuntime`

## Autoridad

Este documento define el alcance operativo del Sprint 7.0.

No modifica el Blueprint, la Constitución Cognitiva, el Kernel, los contratos centrales ni la gobernanza general del proyecto.

La implementación descrita corresponde a una interfaz técnica de validación del subsistema conversacional.

---

## Objetivo

Implementar y validar una interfaz mínima por terminal que permita:

- recibir texto ingresado por el usuario;
- construir un `ConversationRequest`;
- delegar la solicitud al subsistema conversacional existente;
- mostrar el contenido de un `ConversationResponse`;
- finalizar la sesión de forma controlada;
- validar manualmente la integración entre servicio, provider y runtime.

---

## Decisión arquitectónica adoptada

La CLI del Sprint 7.0 utiliza la siguiente ruta:

```text
CLI de validación
    ↓
ConversationRequest
    ↓
ConversationService
    ↓
ConversationProviderRegistry
    ↓
MockConversationProvider
    ↓
MockLLMRuntime
    ↓
ConversationResponse