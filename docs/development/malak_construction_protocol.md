# Malāk Construction Protocol

Versión: 0.1.0

Estado: Activo

---

# 1. Propósito

Este documento define la disciplina transversal utilizada para revisar el estado de Malāk, seleccionar trabajo futuro, ejecutar cambios por gates y producir evidencia verificable sin ampliar autoridad ni alcance de forma implícita.

Complementa `docs/development/engineering_method.md` y `docs/development/development_checklist.md`.

No reemplaza ni reinterpreta:

1. Constitución Cognitiva;
2. Constitución de Gobernanza;
3. Blueprint;
4. especificaciones aprobadas;
5. ADR aceptados;
6. contratos públicos;
7. Architecture Quality Gates.

En caso de conflicto prevalece la jerarquía documental oficial del proyecto.

---

# 2. Principio de construcción

Malāk debe crecer desde evidencia y necesidad real, reutilizando y revalidando la intención arquitectónica ya preservada antes de inventar una línea nueva.

Flujo rector:

```text
baseline verificable
        ↓
necesidad real
        ↓
inventario exhaustivo de fuentes
        ↓
roadmap + ideas + concepts
        ↓
ADOPT / ADAPT / OBSERVE / REJECT
        ↓
admission review
        ↓
especificación
        ↓
gates pequeños y reversibles
        ↓
TDD / implementación
        ↓
4R
        ↓
bounded correction cuando corresponda
        ↓
validación independiente
        ↓
E2E / métricas / evidencia
        ↓
gobernanza humana
        ↓
baseline estable
        ↓
reconciliación derivada
```

La existencia de una idea, concepto, roadmap o receipt no constituye autorización para implementar.

---

# 3. Cobertura exhaustiva de repositorio

## 3.1 Regla de inventario

Toda revisión declarada `integral`, `completa`, `transversal`, de admisión de sprint, certificación, reconciliación o auditoría debe comenzar por un inventario recursivo de todos los archivos trackeados de los repositorios incluidos en el alcance.

La revisión debe poder demostrar:

```text
tracked files discovered = N
tracked files classified = N
silently omitted files   = 0
```

Ningún archivo puede desaparecer del proceso por no haber coincidido con una búsqueda textual.

## 3.2 File Coverage Ledger

Cada archivo debe recibir una disposición explícita, como mínimo equivalente a:

```text
path
repository
artifact_type
authority_class
review_relevance
review_depth
disposition
related_findings
```

Disposiciones candidatas:

```text
FULL_READ
TARGETED_READ
STRUCTURAL_INSPECTION
HISTORICAL_REFERENCE
GENERATED_OR_DERIVED
NOT_APPLICABLE_WITH_REASON
PROTECTED
REJECTED_DO_NOT_READ
```

La profundidad de lectura puede ser proporcional al rol y al problema, pero la clasificación no puede omitirse.

Un archivo expresamente prohibido por las instrucciones vigentes debe aparecer en el inventario con `REJECTED_DO_NOT_READ` y no debe abrirse ni procesarse.

## 3.3 Revisión transversal

Cuando el estado global de Malāk forme parte de la decisión, el inventario debe abarcar, según disponibilidad:

```text
Aranwill/jarvis
Aranwill/malak-project-vault
Aranwill/malak-vault-sync-agent
```

La fuente oficial continúa siendo `Aranwill/jarvis/main`.

El Vault es una proyección derivada y el Sync Agent un mecanismo determinista de observación y propuesta.

---

# 4. Incorporación progresiva de capacidades futuras

## 4.1 Fuentes de incubación

Antes de diseñar desde cero una nueva capacidad, la revisión debe consultar explícitamente:

```text
docs/project/implementation_roadmap.md
documents/projects/jarvis/ideas.md
docs/project/concepts/**
```

`ideas.md` y `docs/project/concepts/**` constituyen el principal reservorio de intención y diseño futuro ya explorado, sin adquirir por ello autoridad de implementación.

## 4.2 Regla de revalidación

Una propuesta preservada solo puede incorporarse cuando una necesidad del baseline actual la haga relevante y después de revalidarla contra:

- Blueprint;
- Constitución Cognitiva;
- Gobernanza;
- Architecture Quality Gates;
- ADR vigentes;
- código real;
- tests;
- riesgos actuales;
- dependencias actuales;
- evidencia operacional disponible.

## 4.3 Clasificación de disposición

Toda idea o concepto candidato debe clasificarse explícitamente:

```text
ADOPT
→ encaja sin cambios materiales con la necesidad y el baseline actual.

ADAPT
→ conserva la intención, pero requiere ajuste al baseline o a evidencia nueva.

OBSERVE
→ sigue siendo valioso, pero la necesidad o madurez todavía no justifican implementación.

REJECT
→ contradice principios, evidencia o necesidad actual, o introduce complejidad injustificada.
```

La clasificación no equivale a autorización.

## 4.4 Regla anti-rediseño

No se debe rediseñar desde cero una capacidad futura sin comprobar primero si la intención ya está preservada en `ideas.md` o `docs/project/concepts/**`.

Tampoco se debe forzar una idea histórica sobre un baseline que ya no la justifica.

---

# 5. Planificación por gates

Todo cambio material debe poder dividirse en gates verificables.

Cada gate debe declarar, cuando corresponda:

```text
gate_id
objective
preconditions
candidate_identity
risk_class
allowed_files
allowed_components
forbidden_components
out_of_scope
expected_delta
validation
metrics
4R_lenses
stop_conditions
rollback
result
```

Estados de gate:

```text
PASS
FAIL
INCONCLUSIVE
```

`INCONCLUSIVE` nunca equivale a `PASS`.

No se avanza al gate siguiente si existe un `FAIL` bloqueante o un `INCONCLUSIVE` no resuelto.

---

# 6. Cuatro lentes obligatorios

Los cuatro lentes definidos por el Engineering Method son:

```text
Risk
Readability
Reliability
Resilience
```

Cuando corresponda FULL 4R, cada lente debe producir evidencia separada.

Formato mínimo recomendado:

```text
lens
status: PASS | FAIL | INCONCLUSIVE
questions_evaluated
findings
evidence
residual_risk
```

No debe utilizarse `4R PASS` como única evidencia cuando el riesgo requiera demostrar qué fue revisado por cada lente.

El escalamiento dinámico de revisión continúa regido por `engineering_method.md`.

---

# 7. Métricas mínimas de ejecución

Cada gate debe medir las variables aplicables en lugar de limitarse a una afirmación cualitativa.

Perfil recomendado:

```text
gate
candidate_sha
baseline_sha
risk_class
changed_files
production_delta
test_delta
dependencies_added
public_contract_changes
kernel_delta
targeted_tests
full_tests
duration
risk_status
readability_status
reliability_status
resilience_status
findings
correction_rounds
final_status
```

Los campos no aplicables deben registrarse como `N/A` cuando el artefacto de evidencia los utilice.

Las métricas son evidencia; no son autoridad.

---

# 8. Perfil RDD progresivo de Malāk

## 8.1 Estado

Malāk no adopta todavía Receipt-Driven Development como metodología completa ni autoriza infraestructura específica de receipts.

Sí adopta de forma progresiva los patrones maduros que ya convergen con su Engineering Method:

- Candidate Identity;
- evidencia ligada al candidato;
- separación Writer / Reviewer / Validator / Authority;
- 4R;
- Bounded Correction;
- validación independiente;
- trazabilidad de findings;
- revalidación cuando cambia el candidato.

## 8.2 Separaciones obligatorias

```text
Evidence
!= Receipt
!= Validation
!= Decision
!= Authority
```

Un receipt describe evidencia relativa a un candidato exacto. No aprueba, autoriza, promueve, mergea ni modifica gobernanza.

## 8.3 Candidate-bound evidence

Regla:

```text
candidate changes
→ candidate identity changes
→ previous candidate-bound validation no longer certifies the new candidate
→ affected evidence must be revalidated
```

La identidad puede utilizar commit SHA, hash de contenido u otro identificador determinista aprobado.

## 8.4 Evidence Receipt mínimo experimental

Antes de implementar un subsistema RDD, los sprints pueden probar un perfil documental mínimo:

```text
receipt_id
receipt_type
baseline_identity
candidate_identity
specification_reference
gate
risk_class
validations
4R_results
findings
correction_round
metrics
evidence_references
validator
result
generated_at
```

Resultados permitidos:

```text
PASS
FAIL
INCONCLUSIVE
```

Resultados prohibidos para un receipt:

```text
APPROVED
AUTHORIZED
MERGED
```

## 8.5 Evolución por evidencia

Ruta de maduración candidata:

```text
Stage 0 — Candidate Identity + evidencia actual
Stage 1 — Structured Evidence Manifest
Stage 2 — Candidate-Bound Validation Receipt
Stage 3 — Candidate Evidence Package
Stage 4 — Integrity hardening
Stage 5 — agent-produced candidates + external validation
Stage 6 — governed multi-agent candidate evaluation
```

Ninguna etapa se implementa por secuencia automática.

Cada promoción requiere necesidad demostrada, evidencia de utilidad y aprobación separada.

Se debe preferir primero usar el perfil documental en uno o más sprints y medir su utilidad antes de crear un contrato, servicio, base de datos, PKI o ledger.

---

# 9. Bounded Correction y receipts

Un finding no se elimina porque exista una corrección posterior.

Secuencia preservada:

```text
candidate A
→ finding / FAIL evidence
→ authorized Correction Budget
→ candidate B
→ independent validation
→ new evidence / receipt
```

La evidencia histórica del fallo se conserva cuando sea necesaria para trazabilidad.

Una corrección que exceda su budget debe escalar en lugar de ampliar silenciosamente scope o arquitectura.

---

# 10. Reconciliación derivada post-merge

## 10.1 Trigger

Después de integrar un cambio en `Aranwill/jarvis/main`, debe evaluarse si las rutas modificadas están observadas o mapeadas por el Malāk Vault Synchronization Agent.

Cuando corresponda, la reconciliación del Project Vault debe ejecutarse mediante el flujo gobernado del Sync Agent.

## 10.2 Autoridad

La reconciliación del Vault:

```text
NO reabre un Sprint ya cerrado
NO modifica la autoridad de jarvis/main
NO convierte el Vault en source of truth
NO permite al Sync Agent aprobar cambios
```

Si el Sync Agent falla, `jarvis/main` continúa siendo la fuente oficial y el drift debe permanecer visible.

## 10.3 Gate antes de la siguiente admisión

No debe iniciarse la admisión formal de una nueva unidad de trabajo mientras exista `BASELINE_DRIFT`, `PROJECTION_DRIFT`, `STATE_DRIFT` o drift semántico downstream relevante conocido sin:

1. reconciliación;
2. resolución explícita;
3. o aceptación humana documentada del riesgo y su impacto sobre la decisión.

Esto protege la calidad del contexto usado para planificar sin convertir al Vault en autoridad de cierre del Sprint anterior.

---

# 11. Revisión de cierre cross-repository

Cuando el cambio afecte estado proyectado, el cierre debe comprobar:

```text
jarvis/main
        ↓
source candidate exacto

Sync Agent
        ↓
observación / estado reconciliado

Project Vault
        ↓
proyección coherente con la fuente
```

Findings relevantes deben clasificarse mediante la taxonomía de drift vigente.

---

# 12. Regla final

> **Malāk crece desde evidencia verificable, reusa y revalida su diseño futuro preservado, cambia mediante gates pequeños y solo convierte evidencia en baseline a través de gobernanza humana.**
