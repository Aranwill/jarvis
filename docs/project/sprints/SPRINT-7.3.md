---
title: Sprint 7.3 — Conversation Provider Boundary Stabilization
status: implementación validada
authority: operativa del sprint
as_of_commit: 739924f
baseline_commit: fdb3ee922efc796e53ade1fc3abe4125f4072bd0
branch: feature/sprint-7.3-conversation-provider-boundary
language: es
---

# Sprint 7.3 — Conversation Provider Boundary Stabilization

## Autoridad y dependencia

Este documento define el alcance operativo aprobado del Sprint 7.3.

El sprint parte del baseline oficial posterior al cierre del Sprint 7.2:

```text
fdb3ee922efc796e53ade1fc3abe4125f4072bd0
```

No modifica el Blueprint, la Constitución Cognitiva, la Constitución de Gobernanza, el Kernel, el Planner, el contrato `Capability`, los contratos conversacionales ni los runtimes implementados.

## Objetivo

Estabilizar la frontera del subsistema conversacional entre:

```text
ConversationService
→ ConversationProviderRegistry
→ ConversationProvider
→ LLMRuntime
```

El sprint elimina ambigüedades de nombres y comportamiento sin integrar el subsistema conversacional con el Kernel ni incorporar nuevas capacidades.

## Problema verificado

La clase `MockConversationProvider` actuaba como adaptador genérico sobre cualquier implementación de `LLMRuntime`, incluido `OllamaRuntime`.

El nombre no representaba su responsabilidad real.

Además, `ConversationProviderRegistry`:

- no normalizaba nombres;
- permitía sobrescrituras silenciosas;
- exponía un `KeyError` interno cuando el provider no existía;
- no rechazaba nombres vacíos;
- no definía explícitamente el comportamiento ante duplicados.

El docstring de `ConversationService` también presentaba logging, métricas, retries y selección de providers como extensiones futuras, aunque esas responsabilidades no estaban aprobadas.

## Decisión arquitectónica

### `RuntimeConversationProvider`

`RuntimeConversationProvider` actúa como adaptador lógico entre el dominio conversacional y un `LLMRuntime` inyectado.

Su responsabilidad es:

1. recibir un `ConversationRequest`;
2. delegar la ejecución al runtime;
3. devolver un `ConversationResponse`;
4. mantener al servicio desacoplado de runtimes concretos.

No selecciona modelos, no configura runtimes, no aplica retries, no persiste conversaciones y no incorpora políticas de gobernanza.

### `ConversationProviderRegistry`

El registry:

- normaliza nombres mediante `strip().lower()`;
- rechaza nombres vacíos;
- rechaza providers duplicados;
- mantiene el listado ordenado;
- expone `ConversationProviderNotFoundError` cuando un provider no está registrado;
- encapsula el `KeyError` interno del diccionario.

### `ConversationService`

`ConversationService` conserva una responsabilidad mínima:

1. resolver el provider solicitado;
2. delegar la solicitud;
3. devolver la respuesta resultante.

No selecciona runtimes, modelos, retries, logging, métricas, persistencia ni políticas de gobernanza.

## Alcance implementado

- renombrado de `MockConversationProvider` a `RuntimeConversationProvider`;
- renombrado del módulo `mock_provider.py` a `runtime_provider.py`;
- actualización de imports y pruebas;
- normalización de nombres en `ConversationProviderRegistry`;
- rechazo de nombres vacíos;
- rechazo de registros duplicados;
- incorporación de `ConversationProviderNotFoundError`;
- listado ordenado de providers;
- aclaración de la responsabilidad mínima de `ConversationService`;
- prueba de propagación del error de provider inexistente;
- preservación del comportamiento de la CLI;
- preservación de compatibilidad con `MockLLMRuntime` y `OllamaRuntime`.

## Fuera de alcance

- cambios en el Kernel;
- cambios en el Planner;
- cambios en `Capability`;
- integración entre `Kernel.receive` y `ConversationService`;
- nuevos providers específicos;
- nuevos runtimes;
- retries;
- fallback;
- logging;
- nuevas métricas;
- persistencia conversacional;
- memoria;
- auditoría;
- autorización;
- Security Control Plane;
- selección automática de modelos;
- cambios en `timeout`;
- cambios en `keep_alive`;
- cambios en el Vault.

## Archivos de código modificados

```text
src/malak/app/cli.py
src/malak/core/conversation_registry.py
src/malak/providers/runtime_provider.py
src/malak/services/conversation_service.py
```

Archivo retirado mediante renombrado:

```text
src/malak/providers/mock_provider.py
```

## Pruebas modificadas

```text
tests/test_cli.py
tests/test_conversation_registry.py
tests/test_conversation_service.py
tests/test_runtime_integration.py
tests/test_runtime_provider.py
```

Archivo retirado mediante renombrado:

```text
tests/test_mock_provider.py
```

## Commits de implementación

```text
50c34af refactor(conversation): clarify runtime provider role
dcd580e refactor(conversation): stabilize provider registry
d7eb1aa refactor(conversation): define minimal service boundary
739924f docs(sprints): archive superseded Sprint 7.3 draft
e354e7b docs(sprint): document Sprint 7.3 provider boundary
```

## Validación

Suite completa:

```text
74 passed in 0.17s
```

Comandos ejecutados:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m compileall src tests
git diff --check
git status
```

Resultado:

- suite completa en verde;
- compilación sin errores;
- diff sin errores de formato;
- working tree limpio;
- rama local sincronizada con su referencia remota.

## Criterios de aceptación

- el provider representa correctamente su responsabilidad;
- un mismo provider puede envolver runtimes mock o reales;
- los nombres se normalizan;
- los nombres vacíos se rechazan;
- los duplicados se rechazan;
- la ausencia de provider produce un error explícito;
- el servicio conserva una responsabilidad mínima;
- la CLI mantiene su comportamiento observable;
- el Kernel permanece sin cambios;
- los contratos conversacionales permanecen sin cambios;
- la suite completa queda en verde;
- el rollback es simple.

## Riesgos controlados

### Refactor puramente cosmético

Mitigado mediante la estabilización del comportamiento público del registry y su cobertura de pruebas.

### Expansión de responsabilidades

Mitigada mediante límites explícitos en `RuntimeConversationProvider` y `ConversationService`.

### Regresión de la CLI

Mitigada mediante pruebas de composición, integración y CLI.

### Exposición de errores internos

Mitigada mediante `ConversationProviderNotFoundError`.

## Rollback

El rollback consiste en:

1. restaurar `MockConversationProvider`;
2. restaurar `mock_provider.py`;
3. restaurar el comportamiento previo de `ConversationProviderRegistry`;
4. retirar `ConversationProviderNotFoundError`;
5. restaurar el docstring anterior de `ConversationService`;
6. revertir las pruebas y referencias actualizadas.

El rollback no afecta:

- Kernel;
- Planner;
- Capability Registry;
- runtimes;
- métricas;
- configuración externa;
- contratos conversacionales.

## Validación de gobernanza

### ¿Respeta el Blueprint?

Sí. Clarifica contratos públicos entre módulos y preserva la independencia del Kernel.

### ¿Respeta la Constitución Cognitiva?

Sí. Aplica una solución mínima, proporcional, verificable y reversible sobre una ambigüedad comprobada.

### ¿Respeta la Constitución de Gobernanza?

Sí. Refuerza separación de responsabilidades, trazabilidad, consistencia y rollback.

### ¿Simplifica o mantiene simple el Kernel?

Sí. El Kernel no fue modificado y no recibió nuevas dependencias.

## Estado de cierre

La implementación y validación local están completas.

El cierre operativo definitivo queda condicionado a:

- revisión del diff documental;
- commit documental;
- revisión del pull request;
- merge aprobado en `main`;
- verificación del nuevo HEAD y de la suite posterior al merge.