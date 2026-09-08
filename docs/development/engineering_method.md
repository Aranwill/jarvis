# Malāk Engineering Method

Versión: 0.1.0

Estado: Activo

---

# 1. Objetivo

Este documento define la metodología de ingeniería de Malāk para diseñar, implementar, revisar y validar cambios de forma incremental, trazable, proporcional al riesgo y compatible con los principios arquitectónicos y de gobernanza del proyecto.

La metodología combina:

- Specification-Driven Development (SDD).
- Test-Driven Development (TDD).
- revisión basada en riesgo mediante las 4R.
- corrección acotada (Bounded Correction).
- validación independiente de correcciones.
- evidencia verificable asociada al candidato evaluado.
- validación E2E y métricas cuando corresponda.

Este documento no sustituye ni reinterpreta la Constitución Cognitiva, la Constitución de Gobernanza, el Blueprint, los ADR aceptados, los contratos públicos ni los Architecture Quality Gates.

En caso de conflicto, prevalece la jerarquía documental oficial del proyecto.

---

# 2. Principio rector

La metodología de ingeniería de Malāk sigue esta cadena:

```text
Evidencia / necesidad
        ↓
Especificación
        ↓
Pruebas
        ↓
Implementación
        ↓
Revisión proporcional al riesgo
        ↓
Corrección acotada cuando corresponda
        ↓
Validación independiente
        ↓
E2E / métricas / evidencia
        ↓
Gobernanza humana
        ↓
Baseline estable
```

Principio asociado:

> La evidencia origina la hipótesis. La especificación define el comportamiento esperado. Los tests verifican el comportamiento. La revisión identifica riesgos y defectos. La corrección permanece acotada. La validación demuestra el resultado. La gobernanza decide la aceptación.

---

# 3. Relación con la autoridad del proyecto

SDD, TDD, 4R y los mecanismos definidos en este documento son métodos de ingeniería.

No constituyen una autoridad superior a:

1. Constitución Cognitiva.
2. Constitución de Gobernanza.
3. Blueprint.
4. Especificaciones aprobadas.
5. ADR aceptados.
6. Contratos públicos y Capabilities.
7. Configuración y documentación de desarrollo aplicable.

Una especificación, test, review, receipt o informe de validación que contradiga una fuente de autoridad superior se considera inválido.

Ningún agente, reviewer, test, receipt o proceso automatizado puede aprobar por sí mismo un cambio crítico ni ampliar su propio alcance o autoridad.

---

# 4. Specification-Driven Development (SDD)

## 4.1 Propósito

SDD define el comportamiento esperado antes de la implementación.

Toda modificación significativa debe responder, como mínimo:

- qué problema o necesidad existe;
- qué comportamiento debe cambiar;
- qué queda fuera de alcance;
- cuáles son los criterios de aceptación;
- qué riesgos y dependencias existen;
- qué evidencia permitirá considerar el cambio correcto.

## 4.2 Estructura mínima de una especificación

Cuando corresponda, una especificación debe incluir:

```text
ID
Título
Problema / necesidad
Alcance
Fuera de alcance
Requisitos
Escenarios
Criterios de aceptación
Dependencias
Riesgos
Rollback
Relaciones con ADR / deuda técnica / sprint
```

## 4.3 Escenarios

Los requisitos importantes deben poder expresarse mediante escenarios verificables.

Ejemplo:

```text
Given:
un SecurityContext expirado

When:
intenta autorizar una operación protegida

Then:
la operación debe ser rechazada
la decisión debe ser fail-closed
debe existir evidencia de auditoría
```

## 4.4 Herramientas

SDD es la metodología adoptada.

OpenSpec u otras herramientas podrán evaluarse como soporte, pero ninguna herramienta concreta se considera obligatoria mientras no sea aprobada, documentada e integrada formalmente al baseline.

Malāk no deberá depender conceptualmente de una herramienta específica para interpretar sus especificaciones.

---

# 5. Test-Driven Development (TDD)

## 5.1 Ciclo

El ciclo preferido es:

```text
RED
↓
GREEN
↓
REFACTOR
```

1. RED: escribir primero una prueba que represente el comportamiento esperado y comprobar que falla por la razón prevista.
2. GREEN: implementar el cambio mínimo necesario para satisfacerla.
3. REFACTOR: mejorar la implementación sin alterar el comportamiento demostrado.

## 5.2 Aplicación obligatoria

TDD debe utilizarse con especial rigor en:

- seguridad;
- autorización;
- contratos públicos;
- límites del Kernel;
- lógica determinista crítica;
- lifecycle de contextos;
- permisos;
- políticas;
- persistencia sensible;
- regresiones de seguridad o arquitectura.

## 5.3 Aplicación recomendada

TDD es recomendado para:

- Services;
- Capabilities;
- routing;
- observabilidad;
- runtimes;
- persistencia ordinaria;
- transformaciones deterministas.

## 5.4 Excepciones

Puede utilizarse test-after en:

- tooling interno de bajo riesgo;
- exploración controlada;
- prototipos de sandbox;
- spike técnico desechable.

Una excepción no elimina la obligación de validación antes de aceptar el cambio en el baseline.

## 5.5 Tests negativos

Los componentes de seguridad deben probar también condiciones de rechazo.

Ejemplos:

```text
identidad ausente          → DENY
contexto expirado          → DENY
nonce reutilizado          → DENY
permiso insuficiente       → DENY
contexto superseded        → DENY
fallo de auditoría         → operación bloqueada
```

---

# 6. Revisión basada en riesgo — Modelo 4R

La revisión de ingeniería utiliza cuatro lentes:

- Risk / Riesgo.
- Readability / Legibilidad.
- Reliability / Confiabilidad.
- Resilience / Resiliencia.

El coste de revisión debe ser proporcional al riesgo del cambio, no al tamaño general del proyecto.

## 6.1 Risk — Riesgo

Evalúa:

- seguridad;
- permisos;
- exposición o pérdida de datos;
- autoridad;
- dependencias;
- cambios arquitectónicos;
- contratos públicos;
- superficies de ataque;
- comportamiento irreversible;
- impacto sobre governance y Human in Control.

Pregunta central:

> ¿Qué puede salir mal y qué daño produciría?

## 6.2 Readability — Legibilidad

Evalúa:

- claridad;
- cohesión;
- responsabilidades;
- mantenibilidad;
- complejidad accidental;
- duplicación;
- nombres y estructura;
- proporcionalidad de la solución;
- señales de sobreingeniería.

Pregunta central:

> ¿La solución es comprensible y más simple de mantener que las alternativas razonables?

## 6.3 Reliability — Confiabilidad

Evalúa:

- corrección funcional;
- invariantes;
- comportamiento determinista;
- pruebas;
- regresiones;
- manejo de estado;
- idempotencia cuando corresponda;
- consistencia entre inputs y outputs.

Pregunta central:

> ¿Hace de forma consistente lo que la especificación promete?

## 6.4 Resilience — Resiliencia

Evalúa:

- fallos parciales;
- timeouts;
- dependencias degradadas;
- reintentos;
- recuperación;
- consistencia tras errores;
- degradación controlada;
- rollback;
- comportamiento ante recursos insuficientes.

Pregunta central:

> ¿Qué ocurre cuando el entorno o una dependencia falla?

---

# 7. Selección proporcional de lentes

No todos los cambios requieren revisión 4R completa.

## Nivel 0 — Trivial

Ejemplos:

- typo;
- formato;
- comentario;
- cambio documental sin efecto normativo.

Revisión:

- validación normal;
- sin subagente 4R salvo señal de riesgo.

## Nivel 1 — Bajo

Ejemplos:

- helper local;
- refactor pequeño;
- documentación técnica;
- cambio acotado sin contratos públicos.

Revisión:

- un lente dominante.

## Nivel 2 — Estándar

Ejemplos:

- Service;
- Capability;
- runtime logic;
- persistencia simple;
- routing.

Revisión:

- uno o más lentes según impacto;
- posibilidad de escalamiento.

## Nivel 3 — Alto

Ejemplos:

- seguridad;
- autorización;
- contratos públicos;
- Kernel boundaries;
- ejecución externa;
- datos sensibles.

Revisión:

- FULL 4R.

## Nivel 4 — Crítico

Ejemplos:

- Governance;
- Constitución;
- Blueprint;
- autoridad de seguridad;
- operaciones privilegiadas;
- self-modification boundaries;
- cambios del Kernel.

Revisión:

- FULL 4R;
- revisión humana obligatoria;
- evaluación adversarial adicional cuando corresponda.

---

# 8. Escalamiento dinámico

Un review inicialmente limitado puede escalar si descubre una señal de mayor riesgo.

Ejemplos:

```text
Readability
→ detecta cambio en PermissionScope
→ escalar a Risk + Reliability + Resilience
```

```text
Reliability
→ detecta nuevo subprocess o dependencia externa
→ escalar a Risk + Resilience
```

El reviewer no amplía el alcance de implementación. Solo amplía el alcance de revisión.

---

# 9. Separación de responsabilidades

Regla fundamental:

```text
Writer != Reviewer != Validator != Authority
```

## Writer

Implementa únicamente el cambio autorizado.

## Reviewer

Inspecciona el candidato y genera findings.

Debe operar en modo de solo lectura siempre que sea técnicamente posible.

No puede:

- modificar código;
- modificar tests;
- cambiar la spec;
- hacer commit;
- ampliar el scope;
- conceder permisos;
- aprobar su propio trabajo.

## Validator

Comprueba objetivamente que una corrección resolvió el finding y respetó los límites definidos.

## Authority

La aceptación final pertenece a la gobernanza aplicable y, cuando corresponda, al propietario humano.

---

# 10. Bounded Correction — Corrección acotada

## 10.1 Objetivo

Una dificultad local no autoriza una expansión silenciosa del alcance.

Cuando un review detecta un finding corregible, la solución debe ejecutarse dentro de un Correction Budget explícito.

La corrección se realiza de forma acotada y no debe transformarse en un refactor general ni en una feature adicional.

## 10.2 Correction Scope

Toda corrección acotada debe indicar, cuando corresponda:

```text
finding_id
objetivo exacto
archivos autorizados
componentes autorizados
componentes prohibidos
presupuesto de cambio
dependencias permitidas
contratos que no pueden cambiar
número máximo de rondas
criterio de éxito
```

## 10.3 Correction Budget

El presupuesto no debe medirse exclusivamente en líneas de código.

Puede incluir:

```yaml
allowed_files: 2
max_production_delta_loc: 30
max_test_delta_loc: 60
allowed_components:
  - SecurityContextValidator
forbidden_components:
  - Kernel
  - Governance
  - Blueprint
new_dependencies: 0
public_contract_changes: 0
architecture_changes: 0
max_fix_rounds: 1
```

Las líneas de código son un guardrail de tamaño, no una medida absoluta de riesgo.

Un cambio pequeño en Governance puede tener mayor riesgo que una modificación mucho mayor en tests.

## 10.4 Regla anti-scope-creep

Si el finding no puede resolverse dentro del Correction Budget:

```text
NO ampliar automáticamente
NO refactorizar componentes adyacentes
NO cambiar arquitectura
NO introducir dependencias

→ ESCALATE
```

La expansión del alcance requiere una nueva evaluación y autorización.

---

# 11. Fix Actor

El Fix Actor recibe solamente la información necesaria para corregir el finding:

- finding;
- evidencia;
- archivos autorizados;
- Correction Budget;
- restricciones;
- criterios de aceptación.

No recibe autoridad para reinterpretar el sprint ni realizar mejoras laterales.

Ejemplo:

```text
Finding:
timeout de Ollama no está manejado de forma determinista.

Allowed:
src/malak/runtime/ollama_runtime.py
tests/runtime/test_ollama_runtime.py

Budget:
25 LOC producción
50 LOC tests

Forbidden:
Kernel
contratos públicos
nuevas dependencias

Goal:
manejar timeout de forma determinista y verificable.
```

---

# 12. Fix Validator

Después de una corrección, el sistema no acepta la afirmación del Fix Actor como evidencia suficiente.

El Fix Validator debe verificar:

- que solo se modificaron archivos autorizados;
- que no se excedió el budget;
- que el finding fue realmente resuelto;
- que no se introdujeron regresiones;
- que no cambiaron contratos o arquitectura fuera del alcance;
- que los tests relevantes pasan;
- que el candidato validado corresponde al candidato esperado.

## 12.1 Estados

El resultado debe ser uno de:

```text
PASS
FAIL
INCONCLUSIVE
```

### PASS

La evidencia disponible demuestra que el finding se resolvió dentro del alcance autorizado.

### FAIL

La evidencia demuestra que el finding permanece o que la corrección introdujo una violación.

Debe generarse evidencia explícita del fallo.

### INCONCLUSIVE

No existe evidencia suficiente o acceso suficiente para concluir PASS o FAIL.

INCONCLUSIVE nunca debe interpretarse como PASS.

Debe:

- detener la aceptación automática;
- solicitar nueva verificación;
- o escalar según política.

---

# 13. Evidencia de fallo

Un FAIL no debe reducirse a una etiqueta.

Debe registrar, cuando corresponda:

```yaml
status: FAIL
finding_id: R-017
candidate_id: CANDIDATE-004
reason: "contexto superseded todavía aceptado"
expected: DENY
actual: ALLOW
test: test_superseded_context_is_denied
affected_file: src/malak/security/context_validator.py
fix_round: 1
```

La evidencia de fallo puede alimentar:

- corrección posterior;
- Technical Debt Register;
- análisis de regresiones;
- Engineering Intelligence;
- revisión de arquitectura;
- conocimiento histórico.

---

# 14. Candidate Identity

Toda revisión debe referirse a un candidato identificable.

Un candidato puede quedar ligado mediante:

- commit SHA;
- hash de contenido;
- conjunto de archivos y hashes;
- identificador de propuesta;
- identificador de ejecución.

Si el candidato cambia después de ser revisado, la revisión anterior no debe reutilizarse ciegamente.

Principio:

```text
candidate changes
→ identity changes
→ previous approval/evidence must be revalidated
```

---

# 15. Receipts y Receipt-Driven Development

## 15.1 Estado en Malāk

Malāk adopta actualmente los principios de:

- revisión 4R basada en riesgo;
- candidate identity;
- bounded correction;
- correction budget;
- validación independiente;
- PASS / FAIL / INCONCLUSIVE;
- evidencia de fallo;
- separación Writer / Reviewer / Validator / Authority.

Receipt-Driven Development como metodología completa y cualquier implementación externa concreta permanecen en observación hasta que exista suficiente madurez y una decisión arquitectónica específica.

## 15.2 Candidate-Bound Receipt

Como evolución prevista, una validación con resultado `PASS` podrá producir un receipt ligado al candidato.

Ejemplo conceptual:

```yaml
receipt_id: RCP-7F19
result: PASS

candidate:
  id: CANDIDATE-004
  sha: c84e...

risk:
  level: 3

review:
  mode: 4R
  lenses:
    - risk
    - readability
    - reliability
    - resilience

fix:
  rounds: 1
  budget_used: 14

validation:
  tests: PASS
  architecture: PASS
  security: PASS

authority:
  reviewer: none
  acceptance: owner_required
```

## 15.3 Invalidez por cambio de candidato

Si el contenido cambia después del receipt:

```text
reviewed candidate hash != current candidate hash
```

el receipt no debe considerarse prueba suficiente del nuevo candidato.

Debe producirse una nueva verificación o una validación explícita del delta.

## 15.4 Evolución futura

Las siguientes técnicas quedan fuera del alcance actual y podrán evaluarse posteriormente:

- hash chaining;
- firmas criptográficas;
- receipts firmados;
- transparencia basada en Merkle;
- attestation externa;
- hardware-backed attestation;
- almacenamiento inmutable distribuido.

No deben incorporarse prematuramente.

---

# 16. Prevención de sobreingeniería

La metodología debe reducir complejidad, no producirla.

Reglas:

- no usar FULL 4R para cambios triviales;
- no crear una spec extensa para un cambio local obvio;
- no exigir TDD estricto a experimentos desechables;
- no introducir agentes cuando una validación determinista simple sea suficiente;
- no ampliar un fix fuera de su Correction Budget;
- no introducir una dependencia cuando una solución local es suficiente;
- no convertir findings locales en refactors generales;
- escalar solamente cuando la evidencia lo justifique.

Principio:

> La profundidad del proceso debe ser proporcional al riesgo, impacto e incertidumbre del cambio.

---

# 17. Relación con Technical Debt

Un finding puede:

```text
4R Finding
    ↓
Fix inmediato
```

o:

```text
4R Finding
    ↓
evaluación
    ↓
Technical Debt
```

La deuda aceptada debe conservar:

- origen;
- finding relacionado;
- evidencia;
- impacto;
- severidad;
- razón de aplazamiento;
- condición de cierre.

Una deuda no debe considerarse resuelta solamente mediante un cambio de estado documental.

Cuando sea razonable, su cierre debe estar respaldado por:

```text
spec
+
tests
+
validación
+
evidencia
```

---

# 18. Relación con agentes

Los futuros agentes de Malāk deben operar bajo separación de responsabilidades.

Modelo recomendado:

```text
Malāk / Orchestrator
        ↓
Candidate
        ↓
Risk Classifier
        ↓
4R Reviewer
        ↓
Findings
        ↓
Bounded Fix Planner
        ↓
Fix Actor
        ↓
Fix Validator
        ↓
Evidence / Receipt
        ↓
Governance
```

Ningún agente puede ser simultáneamente la única fuente de:

- implementación;
- revisión;
- validación;
- autorización.

Un agente puede generar una recomendación, pero no convertirla por sí mismo en autoridad.

---

# 19. Engineering Intelligence

Esta metodología debe servir como base futura para que Malāk evalúe propuestas de mejora mediante evidencia.

Cadena objetivo:

```text
Telemetría / incidentes / deuda
        ↓
observación
        ↓
hipótesis
        ↓
propuesta de mejora
        ↓
SDD
        ↓
TDD
        ↓
implementación experimental
        ↓
4R
        ↓
bounded correction
        ↓
fix validation
        ↓
E2E
        ↓
métricas before/after
        ↓
evidencia
        ↓
recomendación
        ↓
gobernanza humana
```

Malāk puede aprender de:

- propuestas aprobadas;
- propuestas rechazadas;
- errores de predicción;
- regresiones;
- findings recurrentes;
- componentes con mayor deuda;
- diferencias entre impacto esperado y real.

La mejora del conocimiento no concede autoridad para modificar el baseline.

---

# 20. E2E y métricas

Cuando el cambio lo justifique, la Definition of Done debe incluir validación de integración y métricas.

Ejemplos:

- latencia E2E;
- TTFT;
- tokens de entrada/salida;
- tokens/s;
- RAM;
- VRAM;
- tiempo de carga;
- overhead de seguridad;
- eventos de auditoría;
- fallos y denegaciones;
- comparación before/after.

La optimización debe basarse en evidencia real y no en suposiciones.

---

# 21. Definition of Done

Un cambio significativo no debe considerarse terminado solamente porque el código compile o los tests pasen.

Cuando corresponda, debe existir:

```text
Specification             PASS
TDD / tests               PASS
Architecture Gates        PASS
4R Review                 PASS
Bounded Fix Validation    PASS / N/A
Security Tests            PASS
Integration Tests         PASS
Controlled E2E            PASS / N/A
Metrics                   RECORDED / N/A
Documentation             UPDATED
Rollback                  DEFINED
Human Review              COMPLETE
```

Los elementos no aplicables deben registrarse como N/A con justificación cuando el riesgo del cambio lo permita.

---

# 22. Reglas para herramientas externas

No se incorpora automáticamente ninguna herramienta externa para implementar SDD, TDD, 4R o RDD.

Cualquier herramienta futura debe:

- ser evaluada;
- estar documentada;
- respetar Runtime Independence;
- no convertirse en autoridad;
- mantener Human in Control;
- respetar Zero Trust;
- permitir rollback;
- demostrar valor frente a su coste de complejidad.

Esto incluye, entre otras:

- OpenSpec;
- Gentle AI;
- frameworks de agentes;
- sistemas de receipts;
- validadores externos.

---

# 23. Validación arquitectónica obligatoria

Antes de aplicar cualquier cambio importante:

1. ¿Respeta el Blueprint?
2. ¿Respeta la Constitución Cognitiva?
3. ¿Respeta la Constitución de Gobernanza?
4. ¿Mantiene el Kernel simple?

Si una respuesta es negativa, dudosa o carece de evidencia, el cambio debe detenerse y rediseñarse antes de implementar.

---

# 24. Principios resumidos

Malāk adopta los siguientes principios de ingeniería:

> Specification defines intent.

> TDD proves behavior locally.

> 4R reviews the quality and risk of the implementation.

> Bounded Correction prevents uncontrolled scope expansion.

> Independent validation verifies the fix.

> Receipts may bind evidence to a specific candidate.

> E2E proves integration.

> Telemetry proves operational reality.

> Governance decides acceptance.

Y como regla transversal:

> La cognición puede proponer. La autoridad decide. La ejecución debe producir evidencia verificable cuando sea técnicamente razonable.