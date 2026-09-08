---
title: Constitutional Assurance — G1 Objective Architecture Invariants Design
status: gate_pass
authority: especificación operativa de diseño
as_of_date: 2026-09-08
unit: Objective Architecture Invariants Foundation
gate: G1
source_baseline: 5fa2ae2586aec3498710f6722407e371b3e58d1f
g0_candidate: e1b41e4087f572dd75a6a40d5870f01aaecbe0f8
issue: 68
pr: 69
risk_class: 3
implementation_authorized: false
rdd_stage_2_authorized: false
language: es
---

# Constitutional Assurance — G1 Objective Architecture Invariants Design

## 1. Estado de autoridad

El propietario autorizó G1 exclusivamente para diseñar las invariantes y sus
escenarios verificables.

Esta autorización permite:

- especificar comportamiento esperado;
- fijar algoritmo de inspección;
- definir escenarios RED/GREEN futuros;
- fijar archivos permitidos y prohibidos para una eventual implementación;
- definir stop conditions y rollback.

No autoriza:

- crear o modificar tests;
- tocar `src/malak/**`;
- modificar CI;
- modificar contratos públicos;
- modificar Kernel o Security behavior;
- introducir dependencias;
- asignar automáticamente número de Sprint;
- RDD Stage 2;
- merge.

La autoridad final permanece humana.

```text
Test result != Validation != Decision != Authority
```

---

# 2. Baseline y evidencia reutilizada

Baseline fuente congelado:

```text
Aranwill/jarvis
main
5fa2ae2586aec3498710f6722407e371b3e58d1f
```

G0:

```text
tracked discovered = 174
tracked classified = 174
silently omitted = 0
G0 = PASS
```

La pipeline vigente de Sprint 7.11 ya ejecuta la suite completa de `pytest`, por
lo que una futura prueba arquitectónica quedaría incorporada automáticamente sin
cambiar `.github/workflows/validation.yml`.

RDD Stage 1 ya demuestra de forma determinista:

```text
authority_effect = none
PASS | FAIL | INCONCLUSIVE only
```

Por tanto CA-I3 reutiliza evidencia existente y no genera cobertura duplicada.

---

# 3. Objetivo de G1

Diseñar el mínimo mecanismo determinista capaz de responder dos preguntas:

```text
CA-I1:
¿src/malak/kernel/** mantiene independencia directa de implementaciones
concretas de runtime/provider y ConversationService?

CA-I2:
¿src/malak/security/** mantiene independencia directa de runtimes/providers y
LLMRuntime?
```

El mecanismo propuesto inspecciona imports Python estáticos.

No interpreta Constitución, Blueprint ni ADRs en runtime.
No decide si un cambio es aceptable.
No concede permisos.
No modifica ningún componente.

Su salida futura será únicamente evidencia binaria de cumplimiento de una lista
de dependencias prohibidas previamente aprobada por gobernanza humana.

---

# 4. Artefacto futuro único permitido

Si una implementación posterior es autorizada, G1 propone un solo archivo nuevo:

```text
tests/test_architecture_invariants.py
```

No se crea helper en `src/`, `scripts/` ni un nuevo package de arquitectura.

Razón:

- la lógica es exclusivamente de test/assurance;
- no pertenece al runtime;
- no justifica un servicio reutilizable todavía;
- evita crear infraestructura prematura.

Presupuesto esperado:

```text
allowed new files       = 1
production files        = 0
public contract changes = 0
external dependencies   = 0
CI changes              = 0
Kernel changes          = 0
Security behavior       = 0
```

---

# 5. Algoritmo de inspección diseñado

## 5.1 Fuente de verdad del análisis

Usar exclusivamente Python stdlib:

```text
ast
pathlib
importlib.util
```

`pytest` ya existe como dependencia de desarrollo y ejecutor de tests; no se
añade ninguna dependencia nueva.

## 5.2 Archivos analizados

CA-I1:

```text
src/malak/kernel/**/*.py
```

CA-I2:

```text
src/malak/security/**/*.py
```

La búsqueda es recursiva y determinista.

## 5.3 Nodos AST relevantes

Se inspeccionan:

```text
ast.Import
ast.ImportFrom
```

No se usa grep textual para evitar falsos positivos en comentarios, strings o
docstrings.

## 5.4 Normalización de `import`

Ejemplo:

```python
import malak.runtime.mock_llm_runtime as runtime
```

produce candidato:

```text
malak.runtime.mock_llm_runtime
```

Cada alias de `ast.Import.names` se evalúa individualmente.

## 5.5 Normalización de `from ... import ...`

Ejemplo:

```python
from malak.providers.runtime_provider import RuntimeConversationProvider
```

produce al menos:

```text
malak.providers.runtime_provider
malak.providers.runtime_provider.RuntimeConversationProvider
```

Ejemplo importante para evitar bypass por package import:

```python
from malak.services import conversation_service
```

produce:

```text
malak.services
malak.services.conversation_service
```

Así CA-I1 detecta `ConversationService` aunque se importe desde el package padre.

## 5.6 Imports relativos

Los imports relativos también deben resolverse.

Ejemplo desde `malak.kernel`:

```python
from ..runtime import mock_llm_runtime
```

se normaliza conceptualmente a:

```text
malak.runtime
malak.runtime.mock_llm_runtime
```

La resolución propuesta utiliza `importlib.util.resolve_name` con el package
deducido de la ruta del archivo bajo `src/`.

Ejemplo desde `malak.security`:

```python
from ..core import llm_runtime
```

se normaliza a:

```text
malak.core
malak.core.llm_runtime
```

## 5.7 Match de frontera

Una dependencia está prohibida cuando el target normalizado:

```text
== forbidden target
OR
starts with forbidden target + "."
```

Esto evita falsos matches como:

```text
malak.runtime_tools
```

cuando la frontera prohibida es:

```text
malak.runtime
```

---

# 6. CA-I1 — Kernel Concrete Execution Isolation

## 6.1 Regla exacta

Para todo archivo Python trackeado bajo:

```text
src/malak/kernel/**
```

ningún import estático directo puede resolver a:

```text
malak.runtime
malak.providers
malak.services.conversation_service
```

ni a descendientes de esos namespaces.

## 6.2 Lo que CA-I1 protege

- Runtime Independence;
- frontera Kernel → Capability;
- ausencia de provider concreto en el Kernel;
- ausencia de `ConversationService` concreto dentro del Kernel.

## 6.3 Lo que CA-I1 NO afirma

CA-I1 no prohíbe automáticamente:

```text
malak.services.planner
malak.core.*
malak.kernel.*
malak.capabilities.*
```

Tampoco establece una prohibición general contra `malak.security`.

Una futura relación Kernel–policy/security deberá evaluarse contra Blueprint,
ADR y contratos aplicables en su propia admission review.

## 6.4 Baseline observado

`kernel.py` actualmente importa:

```text
malak.core.request
malak.core.response
malak.kernel.bootstrap
malak.kernel.registry
malak.services.planner
```

`bootstrap.py` importa:

```text
malak.capabilities.echo
malak.kernel.registry
```

Por tanto:

```text
baseline CA-I1 = PASS
```

---

# 7. CA-I2 — Security Runtime/Provider Independence

## 7.1 Regla exacta

Para todo archivo Python trackeado bajo:

```text
src/malak/security/**
```

ningún import estático directo puede resolver a:

```text
malak.runtime
malak.providers
malak.core.llm_runtime
```

ni a descendientes de esos namespaces.

## 7.2 Lo que CA-I2 protege

- decisiones y enforcement independientes de modelo/provider;
- determinismo del Security Control Plane;
- separación entre autorización y ejecución de inferencia.

## 7.3 Lo que CA-I2 NO afirma

No prohíbe dependencias legítimas hacia:

```text
malak.security.*
stdlib
contratos/core no relacionados con LLMRuntime
```

No cambia:

- PDP;
- PEP;
- `SecurityContext`;
- TTL/lifecycle;
- auditoría;
- permisos;
- reglas de autorización.

Por tanto:

```text
security behavior delta = 0
```

## 7.4 Baseline observado

La inspección del baseline no detectó imports desde `src/malak/security/**` hacia
runtimes, providers ni `malak.core.llm_runtime`.

Por tanto:

```text
baseline CA-I2 = PASS
```

---

# 8. CA-I3 — Evidence Carries Zero Authority

## 8.1 Disposición

```text
ADOPT EXISTING EVIDENCE
```

No se crea test nuevo.

## 8.2 Evidencia ya existente

`MALAK-EVIDENCE-MANIFEST/v1` exige:

```text
authority_effect = none
```

y el validator rechaza otros valores.

La suite actual ya cubre, entre otros:

```text
authority_effect = approved            → FAIL
campo approved agregado                → FAIL
resultado fuera de enum                → FAIL
FAIL ocultado como PASS                → FAIL
INCONCLUSIVE promovido a PASS          → FAIL
```

## 8.3 Regla anti-duplicación

No agregar otra prueba de CA-I3 salvo que una revisión futura identifique un gap
concreto no cubierto por `tests/test_malak_evidence.py`.

---

# 9. Escenarios RED/GREEN diseñados

Una eventual implementación deberá demostrar primero que el detector falla ante
violaciones sintéticas y luego que el baseline real cumple las invariantes.

No se requiere modificar producción para producir RED.

## CA-T1 — detecta import absoluto de runtime desde Kernel

Given:

```python
import malak.runtime.mock_llm_runtime
```

When:

se inspecciona como fuente perteneciente a `malak.kernel`.

Then:

```text
violation = YES
matched boundary = malak.runtime
```

RED inicial esperado antes del helper mínimo:

```text
detector inexistente / test falla
```

GREEN:

```text
detector AST mínimo identifica la violación
```

## CA-T2 — detecta provider mediante `from`

Given:

```python
from malak.providers.runtime_provider import RuntimeConversationProvider
```

Then:

```text
CA-I1 violation = YES
```

## CA-T3 — detecta ConversationService importado desde package padre

Given:

```python
from malak.services import conversation_service
```

Then:

```text
normalized candidate includes malak.services.conversation_service
CA-I1 violation = YES
```

Este escenario evita una implementación demasiado superficial que mire solo el
campo `module` de `ast.ImportFrom`.

## CA-T4 — detecta import relativo desde Kernel

Given archivo perteneciente a `malak.kernel`:

```python
from ..runtime import mock_llm_runtime
```

Then:

```text
resolved target includes malak.runtime
CA-I1 violation = YES
```

## CA-T5 — permite Planner en Kernel

Given:

```python
from malak.services.planner import Planner
```

Then:

```text
CA-I1 violation = NO
```

Este escenario protege contra una regla más amplia que la aprobada.

## CA-T6 — detecta runtime desde Security

Given:

```python
from malak.runtime.ollama_runtime import OllamaRuntime
```

Then:

```text
CA-I2 violation = YES
```

## CA-T7 — detecta LLMRuntime desde Security

Given:

```python
from malak.core.llm_runtime import LLMRuntime
```

Then:

```text
CA-I2 violation = YES
```

## CA-T8 — detecta LLMRuntime relativo desde Security

Given archivo perteneciente a `malak.security`:

```python
from ..core import llm_runtime
```

Then:

```text
normalized candidate includes malak.core.llm_runtime
CA-I2 violation = YES
```

## CA-T9 — no confunde namespace parecido

Given:

```python
import malak.runtime_tools
```

Then:

```text
CA-I1 violation = NO
CA-I2 violation = NO
```

## CA-T10 — baseline Kernel completo

Given:

```text
src/malak/kernel/**/*.py
```

When:

se inspeccionan todos los imports estáticos.

Then:

```text
violations = []
```

## CA-T11 — baseline Security completo

Given:

```text
src/malak/security/**/*.py
```

Then:

```text
violations = []
```

---

# 10. Forma de evidencia de fallo

Un fallo futuro debe identificar, como mínimo:

```text
invariant
file
line
observed_import
normalized_target
forbidden_boundary
```

Ejemplo conceptual:

```text
CA-I1 violation
file: src/malak/kernel/kernel.py
line: 7
observed_import: from malak.runtime.ollama_runtime import OllamaRuntime
normalized_target: malak.runtime.ollama_runtime
forbidden_boundary: malak.runtime
```

No se requiere JSON ni un nuevo evidence schema para este incremento.

El failure message de pytest es evidencia técnica, no receipt ni autoridad.

---

# 11. Casos deliberadamente fuera de alcance

G1 no intenta detectar:

```text
importlib.import_module("...")
__import__("...")
exec/eval
strings que nombren módulos
runtime monkeypatching
inyección mediante plugin discovery
transitive dependency graphs
semantic call graphs
constitutional natural-language interpretation
```

Razón:

La necesidad demostrada es asegurar imports estáticos directos en dos fronteras.
Agregar análisis dinámico o grafo transitivo sería una expansión no justificada.

Stop condition:

```text
si una futura implementación real usa mecanismos dinámicos dentro de estas
fronteras y afecta la utilidad de la invariante
→ NO ampliar silenciosamente el test
→ abrir nueva evaluation/admission
```

---

# 12. Falsos positivos y falsos negativos aceptados

## Falsos positivos

El diseño busca evitarlos mediante:

- AST en lugar de grep;
- match por namespace exacto o descendiente;
- escenario permitido para `malak.services.planner`;
- escenario permitido para namespace similar `malak.runtime_tools`.

## Falsos negativos conocidos

Mecanismos de import dinámico quedan fuera de alcance deliberadamente.

Esto no se oculta ni se interpreta como cobertura total de arquitectura.

La afirmación correcta es:

```text
static direct import invariant
```

no:

```text
complete dependency proof
```

---

# 13. Candidate Identity y TDD

Si implementación es autorizada posteriormente:

```text
G1 design candidate
→ implementation branch/head changes
→ candidate identity changes
→ G1 evidence remains historical design evidence
→ implementation requires new candidate-bound validation
```

Secuencia TDD propuesta:

```text
1. crear tests sintéticos CA-T1..CA-T9
2. verificar RED por ausencia del detector mínimo
3. implementar detector local dentro del mismo test module
4. verificar GREEN sintético
5. activar scans CA-T10 y CA-T11 sobre baseline
6. ejecutar suite completa
7. compileall
8. candidate-bound diff-check
9. FULL 4R
10. independent validation
11. human governance
```

No se modifica producción para fabricar un RED.

---

# 14. Correction Budget futuro

Si durante implementación aparece un finding corregible, presupuesto inicial
máximo propuesto:

```yaml
allowed_files:
  - tests/test_architecture_invariants.py
max_new_files: 1
max_production_delta_loc: 0
max_test_delta_loc: 180
new_dependencies: 0
public_contract_changes: 0
kernel_delta: 0
security_behavior_delta: 0
ci_delta: 0
max_fix_rounds: 1
```

`max_test_delta_loc` es guardrail, no objetivo.

Si la solución necesita exceder ese presupuesto:

```text
STOP → ESCALATE
```

No crear helper de producción ni script adicional por conveniencia.

---

# 15. Stop conditions

Detener y pedir nueva autorización si aparece cualquiera de estas necesidades:

- tocar `src/malak/**`;
- modificar Kernel;
- modificar Security behavior;
- cambiar un contrato público;
- modificar `.github/workflows/validation.yml`;
- agregar dependencia Python;
- crear un parser/framework externo;
- ampliar hacia import graph transitivo;
- inspeccionar dinámica/reflexión;
- convertir el test en policy engine;
- interpretar lenguaje natural constitucional;
- crear Constitutional Engine runtime;
- introducir RDD Stage 2;
- duplicar CA-I3 sin gap demostrado;
- ampliar lista de forbidden boundaries sin nueva justificación arquitectónica.

---

# 16. Rollback

Si una implementación futura no aporta señal útil o produce fragilidad:

```text
revert tests/test_architecture_invariants.py
```

No existirán:

- migraciones;
- cambios de datos;
- runtime state;
- contratos nuevos;
- dependencias que desinstalar;
- cambios de producción.

La documentación G0/G1 se conserva como trazabilidad histórica aunque la
implementación sea rechazada o revertida.

---

# 17. Cuatro preguntas obligatorias — G1

## Blueprint

```text
PASS
```

El diseño protege Runtime Independence y límites concretos existentes sin
redefinir arquitectura.

## Cognitive Constitution

```text
PASS
```

El mecanismo es proporcional, verificable, trazable y no pretende convertir
juicio contextual en falsa precisión mecánica.

## Governance

```text
PASS
```

Los tests solo producen evidencia. No aprueban, autorizan, mergean ni amplían
scope.

## Kernel simplicity

```text
PASS
planned Kernel delta = 0
```

---

# 18. Criterios de aceptación de G1

```text
[x] CA-I1 definida con forbidden boundaries exactas
[x] CA-I2 definida con forbidden boundaries exactas
[x] CA-I3 reutiliza evidencia existente
[x] imports absolutos cubiertos en diseño
[x] from-import package bypass cubierto
[x] imports relativos cubiertos
[x] namespace prefix matching definido sin falsos prefijos
[x] escenarios permitidos definidos
[x] baseline scan diseñado
[x] failure evidence mínima definida
[x] dynamic imports explícitamente fuera de alcance
[x] single future test file
[x] production delta = 0
[x] Kernel delta = 0
[x] Security behavior delta = 0
[x] external dependencies = 0
[x] CI delta = 0
[x] RDD Stage 2 = NOT AUTHORIZED
[x] rollback simple
[x] stop conditions explícitas
```

---

# 19. Decisión G1

```text
G1 RESULT = PASS
blocking findings = 0
```

G1 aprueba el diseño técnico mínimo para consideración humana posterior.

No autoriza implementación.

Siguiente gate candidato:

```text
G2 — TDD implementation of static architecture invariants
```

Estado:

```text
G2 = NOT AUTHORIZED
implementation = NOT AUTHORIZED
merge = HUMAN-ONLY
```
