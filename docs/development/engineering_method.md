# Malāk Engineering Method

Versión: 0.1.2

Estado: Activo

---

# 1. Objetivo

Este documento define la metodología de ingeniería de Malāk para diseñar, implementar, revisar y validar cambios de forma incremental, trazable, proporcional al riesgo y compatible con los principios arquitectónicos y de gobernanza del proyecto.

La metodología combina:

- Specification-Driven Development (SDD).
- Test-Driven Development (TDD).
- RDD Stage 1 adaptado a Malāk como control explícito de conformidad de diseño y de Evidence ligada al candidate, cuando aplique.\n- RDD Stage 2 adaptado a Malāk como `Candidate-Bound Validation Receipt` para riesgo 3/4 y por admisión explícita en riesgo 2.
- revisión basada en riesgo mediante las 4R.
- Bounded Correction.
- validación independiente de correcciones.
- evidencia verificable asociada al candidato evaluado.
- validación E2E y métricas cuando corresponda.

Este documento no sustituye ni reinterpreta la Constitución Cognitiva, la Constitución de Gobernanza, el Blueprint, los ADR aceptados, los contratos públicos ni los Architecture Quality Gates.

En caso de conflicto, prevalece la jerarquía documental oficial del proyecto.

Para toda unidad material, la aplicación de este método comienza sólo después de
superar `docs/development/malak_construction_preflight.md`. El preflight no agrega
una autoridad nueva: operacionaliza la obligación de recuperar y reconciliar el
baseline, las fuentes aplicables y los límites del trabajo antes de entrar al
ciclo de ingeniería.

---

# 2. Principio rector

La metodología de ingeniería de Malāk sigue esta cadena:

```text
Evidencia / necesidad
        ↓
Especificación + gates de diseño aplicables
        ↓
RDD Stage 1 Design Check cuando aplique
        ↓
Pruebas
        ↓
Implementación
        ↓
Revisión proporcional al riesgo
        ↓
Bounded Correction cuando corresponda
        ↓
Validación independiente
        ↓
E2E / métricas / evidencia candidate-bound
        ↓
RDD Stage 1 Candidate Conformance cuando aplique
        ↓
Gobernanza humana
        ↓
Baseline estable
```

Principio asociado:

> La evidencia origina la hipótesis. La especificación define el comportamiento esperado. RDD Stage 1 comprueba, cuando aplica, que el diseño y el paquete de evidencia preservan identidad, procedencia, separación de roles y vínculo con el candidato. Los tests verifican el comportamiento. La revisión identifica riesgos y defectos. La corrección permanece acotada. La validación demuestra el resultado. La gobernanza decide la aceptación.

---

# 3. Relación con la autoridad del proyecto

SDD, TDD, 4R, RDD Stage 1 adaptado a Malāk y los demás mecanismos definidos en este documento son métodos de ingeniería.

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

La proporcionalidad modifica la **profundidad** de revisión, no permite que una
lente desaparezca silenciosamente.

Toda unidad de cambio debe considerar explícitamente las cuatro lentes:

```text
Risk
Readability
Reliability
Resilience
```

Existen dos perfiles:

```text
PROPORTIONAL 4R
→ las cuatro lentes reciben disposición explícita;
→ se profundizan únicamente las materialmente aplicables;
→ una lente no profundizada debe quedar como NOT_APPLICABLE_WITH_REASON
  o con una justificación equivalente.

FULL 4R
→ las cuatro lentes se revisan en profundidad;
→ cada una produce evidencia separada;
→ cada una concluye PASS | FAIL | INCONCLUSIVE.
```

Una selección proporcional válida debe poder demostrar, como mínimo:

```text
risk_class
lens
disposition
rationale
evidence cuando aplique
escalation_trigger cuando aplique
```

## Nivel 0 — Trivial

Ejemplos:

- typo;
- formato;
- comentario;
- cambio documental sin efecto normativo.

Revisión:

- PROPORTIONAL 4R mínima;
- las cuatro lentes reciben disposición explícita;
- no se exige subagente 4R salvo señal de riesgo.

## Nivel 1 — Bajo

Ejemplos:

- helper local;
- refactor pequeño;
- documentación técnica;
- cambio acotado sin contratos públicos.

Revisión:

- PROPORTIONAL 4R;
- una o más lentes pueden ser dominantes;
- las lentes restantes no pueden omitirse: requieren disposición y razón.

## Nivel 2 — Estándar

Ejemplos:

- Service;
- Capability;
- runtime logic;
- persistencia simple;
- routing.

Revisión:

- PROPORTIONAL 4R con profundidad por impacto;
- posibilidad de escalamiento dinámico;
- FULL 4R si aparece una señal material que eleva el riesgo.

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

Reglas adicionales:

- un contrato crítico conserva los checkpoints Design 4R pre-RED y Candidate
  FULL 4R post-GREEN definidos por el Construction Protocol, con independencia
  de que el delta de código sea pequeño;
- una lente marcada como no aplicable no equivale a no revisada: debe conservar
  razón verificable;
- si una lente detecta una señal de mayor riesgo, se aplica el escalamiento
  dinámico de la sección siguiente.

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

# 10. Bounded Correction

## 10.1 Objetivo

Una dificultad local no autoriza una expansión silenciosa del alcance.

Cuando un review detecta un finding corregible, la solución debe ejecutarse dentro de un Correction Budget explícito.

La corrección se realiza de forma acotada y no debe transformarse en un refactor general ni en una feature adicional.

## 10.2 Correction Scope

Toda `Bounded Correction` debe indicar, cuando corresponda:

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

# 15. RDD adaptado a Malāk y Receipts

## 15.1 Estado de RDD en Malāk

Malāk adopta un **RDD Stage 1 adaptado a su propia lógica de ingeniería y gobernanza**
como parte activa de su método. Esta adopción se inspira en Receipt-Driven
Development (RDD), pero no equivale a copiar ni incorporar automáticamente una
implementación externa concreta.

RDD Stage 1 es un control de Evidence separado de SDD, TDD, 4R, E2E y aprobación
humana. Su definición canónica y su orden operativo se encuentran en
`docs/development/malak_construction_protocol.md`, especialmente §§5.4–5.5.
Esta sección resume el método y no sustituye ese protocolo.

Para cambios materiales, cuando corresponda, existen dos checkpoints distintos:

```text
pre-RED:
RDD Stage 1 Design Check

post-GREEN / after required candidate validation / pre-human-review:
RDD Stage 1 Candidate Conformance
```

El **Design Check** comprueba antes de RED que el diseño preserve, según
aplicabilidad:

- Candidate Identity strategy;
- baseline/candidate binding;
- Evidence provenance;
- separación Writer / Reviewer / Validator / Authority;
- resultados terminales `PASS | FAIL | INCONCLUSIVE`;
- `INCONCLUSIVE != PASS`;
- invalidación de Evidence afectada cuando cambia el candidate;
- Bounded Correction y Correction Budget cuando existan findings;
- independent fix validation cuando corresponda;
- `authority_effect = none`;
- aplicabilidad de RDD Stage 2 declarada sin convertir Receipt en Authority.

El **Candidate Conformance** comprueba sobre el candidate material exacto,
después de las validaciones requeridas y antes de human review, que el paquete
de Evidence sea coherente, candidate-bound y trazable.

Separación obligatoria:

```text
Evidence
!= Receipt
!= Validation
!= Decision
!= Authority

RDD Stage 1 Design Check PASS
!= RDD Stage 1 Candidate Conformance PASS

RDD Stage 1 Candidate Conformance PASS
!= FULL 4R PASS
!= E2E PASS
!= Owner approval

candidate changes
→ affected RDD evidence must be regenerated/revalidated

authority_effect = none
RDD Stage 2 = NOT AUTHORIZED
Stage 3+ = NOT AUTHORIZED
```

El perfil activo integra y endurece mecanismos que Malāk ya utilizaba:

- Candidate Identity y candidate binding;
- candidate-bound Evidence;
- Evidence provenance;
- revisión 4R basada en riesgo;
- Bounded Correction y Correction Budget;
- independent validation;
- `PASS | FAIL | INCONCLUSIVE`;
- failure evidence;
- separación Writer / Reviewer / Validator / Authority;
- invalidación y revalidación de Evidence cuando cambia el candidate;
- `MALAK-EVIDENCE-MANIFEST/v1`.

La ausencia de Evidence requerida produce `INCONCLUSIVE`; nunca puede
degradarse silenciosamente a `PASS`.

La metodología externa completa y las implementaciones concretas de terceros
permanecen como referencias de investigación `OBSERVE` hasta que una necesidad,
Evidence y decisión arquitectónica específicas justifiquen evaluar alguna parte.

## 15.2 Candidate-bound Evidence de Stage 1

Stage 1 utiliza `MALAK-EVIDENCE-MANIFEST/v1`, definido en
`docs/development/evidence_manifest.md`, o Evidence estructurada equivalente
explícitamente aprobada que preserve las mismas invariantes.

La Evidence debe ligar, como mínimo:

```text
baseline exacto
candidate exacto
scope / specification / gate
validations aplicables
4R aplicable
findings
correction rounds
producer / validator provenance
terminal result
authority_effect = none
```

Este manifest **no es** un Receipt de Stage 2.

## 15.3 Invalidación por cambio de candidate

Si cambia el candidate después de producir Evidence ligada a él:

```text
reviewed candidate identity != current candidate identity
```

la Evidence anterior no debe considerarse prueba suficiente del nuevo candidate.

Debe producirse una nueva verificación o una revalidación explícita de la
Evidence afectada.

La misma regla alcanzaría a un Receipt candidate-bound si Stage 2 fuera
autorizado en el futuro: un Receipt nunca debe reinterpretarse como Validation ni
como Authority.

## 15.4 RDD Stage 2 — Candidate-Bound Validation Receipt

RDD Stage 2 está **ADOPTED / ACTIVE** mediante
`MALAK-RDD-VALIDATION-RECEIPT/v1`, definido en
`docs/development/rdd_validation_receipt.md`.

Aplicabilidad:

```text
risk_class 0  → NOT_APPLICABLE
risk_class 1  → NOT_APPLICABLE
risk_class 2  → OPTIONAL / explicit admission only
risk_class 3  → REQUIRED
risk_class 4  → REQUIRED
```

Stage 2 ocurre después de RDD Stage 1 Candidate Conformance. Para riesgo 3/4 exige
un `MALAK-EVIDENCE-MANIFEST/v1` real y válido; una colección informal de comments
o un structured equivalent no materializado no constituye input de Stage 2 V1.

El Receipt preserva:

```text
exact baseline/candidate/tree
Manifest canonical digest
Manifest terminal result
Candidate Conformance terminal result
correction/findings context
provenance references
authority_effect = none
```

```text
Receipt validator PASS
!= Candidate Conformance PASS
!= Owner approval
!= Ready
!= Merge
```

Cambio de candidate invalida la aplicabilidad del Receipt anterior y obliga a
revalidar la Evidence afectada antes de emitir otro Receipt cuando Stage 2 aplique.

Continúan fuera del alcance activo y requieren admisión separada:

- hash chaining;
- firmas criptográficas / signed Receipts;
- transparencia basada en Merkle;
- external/hardware-backed attestation;
- registry/store/database;
- network publication;
- runtime consumption;
- Cognitive Receipt;
- Protected Finalization;
- Persistence Authorization;
- RDD Stage 3+.

Ninguna etapa posterior se incorpora por secuencia automática.

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
RDD Stage 1 Design Check cuando aplique
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
evidencia candidate-bound
        ↓
RDD Stage 1 Candidate Conformance cuando aplique
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
Specification                    PASS
RDD Stage 1 Design Check          PASS / N/A JUSTIFIED
TDD / tests                       PASS
Architecture Gates                PASS
4R Review                         PASS
Bounded Fix Validation            PASS / N/A
Security Tests                    PASS
Integration Tests                 PASS
Controlled E2E                    PASS / N/A
Metrics                           RECORDED / N/A
RDD Stage 1 Candidate Conformance PASS / N/A JUSTIFIED
Documentation                     UPDATED
Rollback                          DEFINED
Human Review                      COMPLETE
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

> RDD Stage 1 verifies design and candidate-bound evidence without granting authority.

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