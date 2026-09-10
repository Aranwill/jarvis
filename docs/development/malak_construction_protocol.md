# Malāk Construction Protocol

Versión: 0.2.1

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
7. Architecture Quality Gates;
8. `SECURITY.md`.

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
security policy + roadmap + ideas + research horizon + concepts
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

Para todo sprint material, este flujo constituye una obligación de ejecución y evidencia, no una guía aspiracional ni un checklist que dependa de un recordatorio conversacional del Owner. El asistente o agente debe aplicar automáticamente cada etapa que corresponda, demostrar su resultado o detenerse si no puede hacerlo.

La existencia de una idea, concepto, research gap, roadmap o receipt no constituye autorización para implementar.

Un requisito de `SECURITY.md` define una restricción o condición de seguridad; no demuestra por sí mismo que la capability o control correspondiente ya esté implementado.

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

## 3.4 Contexto de decisión activo

Antes de determinar el próximo cambio, admitir un sprint o modificar documentación oficial, la revisión debe identificar si existen gates, proposals o packets activos materialmente relacionados con el trabajo actual y leer los que resulten aplicables.

No se requiere releer de forma indiscriminada todo `docs/project/sprints/proposals/**` en cada interacción. La selección debe ser explícita y basada en estado y relevancia.

Una proposal o gate record permanece activo mientras conserve una decisión, restricción, candidate, finding o condición de promoción todavía no cerrada, rechazada, superseded o promovida.

Cuando una proposal haya sido promovida correctamente:

```text
proposal / gate record
→ trazabilidad histórica de la decisión

fuente normativa, especificación o baseline promovido
→ dueño vigente de la verdad aplicable
```

Una proposal activa debe poder restringir el trabajo por su scope o findings, pero no adquiere por ello autoridad superior a las fuentes normativas.

```text
proposal != authority
promotion evidence != normative owner
historical record != current state
```

---

# 4. Incorporación progresiva de capacidades futuras

## 4.1 Fuentes de incubación y restricciones

Antes de diseñar desde cero una nueva capacidad, la revisión debe consultar explícitamente:

```text
SECURITY.md
docs/project/implementation_roadmap.md
documents/projects/jarvis/ideas.md
docs/project/concepts/README.md
docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md
docs/project/concepts/**
```

`SECURITY.md` aporta requisitos y límites de seguridad protegidos.

`ideas.md`, `MALAK_RESEARCH_HORIZON_MAP.md` y `docs/project/concepts/**` constituyen reservorios de intención, gaps y diseño futuro ya explorado, sin adquirir por ello autoridad de implementación.

En una revisión cuyo objetivo sea seleccionar la próxima implementación, `MALAK_RESEARCH_HORIZON_MAP.md` debe recibir lectura explícita; no basta con asumir que quedó cubierto por el glob `docs/project/concepts/**`.

## 4.2 Regla de revalidación

Una propuesta preservada solo puede incorporarse cuando una necesidad del baseline actual la haga relevante y después de revalidarla contra:

- Blueprint;
- Constitución Cognitiva;
- Gobernanza;
- `SECURITY.md`;
- Architecture Quality Gates;
- ADR vigentes;
- código real;
- tests;
- riesgos actuales;
- dependencias actuales;
- evidencia operacional disponible.

La revisión debe distinguir:

```text
security requirement != implemented control
research gap != roadmap
concept != baseline
proposal != authorization
```

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

No se debe rediseñar desde cero una capacidad futura sin comprobar primero si la intención ya está preservada en `ideas.md`, `MALAK_RESEARCH_HORIZON_MAP.md` o `docs/project/concepts/**`.

Tampoco se debe forzar una idea histórica o un gap de investigación sobre un baseline que todavía no la justifica.

## 4.5 Security Horizon Check

Antes de proponer una nueva superficie sensible —incluyendo Memory persistente, agentes, tools, red, interoperabilidad, ejecución externa, aprendizaje procedimental o manejo de datos sensibles— la admission review debe comprobar si activa requisitos o gaps ya preservados en `SECURITY.md` y `MALAK_RESEARCH_HORIZON_MAP.md`.

Como mínimo debe evaluar, según aplicabilidad:

- Prompt & Context Trust Boundary;
- identidad y delegación;
- compromise containment y trust revocation;
- Memory / Knowledge admission y poisoning;
- AI supply-chain trust;
- data classification / disclosure;
- Resource Governance;
- observabilidad, evidencia, recovery y Human in Control.

El resultado puede ser:

```text
ALREADY_COVERED
REQUIRES_REINFORCEMENT
BLOCKING_GAP
NOT_APPLICABLE
DEFERRED
```

Esta clasificación informa la admisión; no crea componentes ni autoriza implementación.

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

## 5.1 Envelope obligatorio de sprint material

Todo sprint se considera material por defecto salvo clasificación explícita y justificada como microcambio no material aprobada por el Owner.

Un sprint material no puede cerrarse únicamente porque el cambio exista o porque la suite esté verde. Debe ejecutar y dejar evidencia de este envelope, según aplicabilidad:

```text
Owner authorization
        ↓
baseline + scope freeze
        ↓
Candidate Identity
        ↓
candidate-bound evidence (RDD Stage 1)
        ↓
validación focalizada
        ↓
FULL 4R
        ↓
bounded correction
        ↓
validación independiente
        ↓
E2E del flujo o cadena afectada
        ↓
CI / evidencia candidate-bound
        ↓
revisión humana
        ↓
Ready humano
        ↓
merge humano
        ↓
validación post-merge
        ↓
reconciliación derivada cuando corresponda
```

No basta con mencionar RDD, 4R o E2E en una ficha o PR. Debe existir evidencia verificable de que las etapas aplicables fueron ejecutadas sobre el candidato correcto.

El E2E no puede omitirse silenciosamente. Cuando no exista un runtime E2E aplicable, el cierre debe registrar la razón y ejecutar la validación end-to-end equivalente de la cadena realmente afectada —por ejemplo coherencia entre documentos, contratos, estados o artefactos— en lugar de declarar simplemente `N/A` sin evidencia.

---

# 6. Cuatro lentes obligatorios

Los cuatro lentes definidos por el Engineering Method son:

```text
Risk
Readability
Reliability
Resilience
```

En todo sprint material, FULL 4R es obligatorio y cada lente debe producir evidencia separada.

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

Para un microcambio no material aprobado explícitamente, la profundidad puede ser proporcional, pero las cuatro lentes deben al menos recibir disposición explícita; una lente omitida requiere justificación.

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

Malāk ha adoptado **RDD Stage 1 — Structured Evidence Manifest** como parte de su disciplina de construcción.

Stage 1 utiliza `MALAK-EVIDENCE-MANIFEST/v1`, definido en `docs/development/evidence_manifest.md`, para ligar evidencia de construcción al candidato exacto evaluado.

Malāk no adopta Receipt-Driven Development como metodología externa completa ni concede autoridad a RDD. **RDD Stage 2 no está autorizado.**

El perfil activo conserva:

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

Un manifest o receipt describe evidencia relativa a un candidato exacto. No aprueba, autoriza, promueve, mergea ni modifica gobernanza.

## 8.3 Candidate-bound evidence

Regla:

```text
candidate changes
→ candidate identity changes
→ previous candidate-bound validation no longer certifies the new candidate
→ affected evidence must be revalidated
```

La identidad puede utilizar commit SHA, hash de contenido u otro identificador determinista aprobado.

## 8.4 Evidence Manifest v1

Para todo candidate material que alcance cierre de validación, la evidencia RDD Stage 1 debe representarse mediante `MALAK-EVIDENCE-MANIFEST/v1` o evidencia estructurada equivalente explícitamente aprobada que preserve las mismas invariantes.

El manifest debe, como mínimo:

```text
bind baseline exacto
bind candidate exacto
referenciar scope / specification / gate
registrar validaciones
registrar FULL 4R
preservar findings y correction rounds
identificar validator
registrar result
mantener authority_effect = none
```

No constituye un receipt de Stage 2.

Resultados permitidos:

```text
PASS
FAIL
INCONCLUSIVE
```

Resultados o efectos prohibidos:

```text
APPROVED
AUTHORIZED
MERGED
PROMOTED
RELEASED
authority_effect != none
```

## 8.5 Evolución por evidencia

Estado y ruta de maduración:

```text
Stage 0 — Candidate Identity + evidencia base          integrado históricamente
Stage 1 — Structured Evidence Manifest                 ADOPTED / ACTIVE
Stage 2 — Candidate-Bound Validation Receipt           NOT AUTHORIZED
Stage 3 — Candidate Evidence Package                   future candidate
Stage 4 — Integrity hardening                          future candidate
Stage 5 — agent-produced candidates + external validation
Stage 6 — governed multi-agent candidate evaluation
```

Ninguna etapa posterior se implementa por secuencia automática.

Cada promoción requiere necesidad demostrada, evidencia de utilidad y aprobación separada.

La adopción de Stage 1 no autoriza un servicio, base de datos, PKI, ledger, auto-finalización, auto-promoción ni auto-merge.

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

# 12. Frontera de modificación de documentos de ley

Los documentos de ley y promoción normativa de Malāk poseen una frontera de escritura más estricta que la documentación ordinaria.

Esta frontera aplica, como mínimo, a:

```text
docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
docs/architecture/blueprint.md
docs/architecture/adr/** cuando una ADR crea, acepta o modifica arquitectura normativa
docs/architecture/decisions/decision-index.md cuando forma parte de una promoción normativa
```

Para estos documentos:

```text
assistant / agent
→ puede leer
→ puede analizar
→ puede señalar conflictos
→ puede proponer un patch exacto
→ puede validar el diff y la evidencia

assistant / agent
→ NO puede materializar remotamente el cambio normativo
→ NO puede escribirlo mediante API, connector o automatización
→ NO puede crear unilateralmente una branch/PR normativa desde su propia edición
```

La materialización de la ley debe realizarla el Owner desde su consola local bajo supervisión directa y revisión hunk-by-hunk.

Secuencia mínima:

```text
mostrar contenido vigente
        ↓
justificar cada modificación
        ↓
Owner aplica el patch mínimo desde consola
        ↓
git diff -- <archivo>
        ↓
revisión conjunta hunk-by-hunk
        ↓
FULL 4R + E2E de coherencia normativa
        ↓
candidate-bound evidence
        ↓
commit / push / PR por acción humana
        ↓
Ready humano
        ↓
merge humano
```

La ausencia de una instrucción conversacional que repita esta frontera no la desactiva. Un asistente o agente que detecte que el target pertenece a esta categoría debe aplicar automáticamente la restricción y detener cualquier escritura remota.

Un proposal, candidate patch o research record no normativo puede preparar la decisión, pero no sustituye el acto humano de modificar la ley.

```text
proposal != law
candidate patch != activation
technical PASS != normative authority
```

---

# 13. Regla final

El cumplimiento de este protocolo es comportamiento por defecto del proceso de construcción de Malāk. No depende de que el Owner recuerde o reitere en cada sprint RDD, 4R, E2E, bounded correction, validación independiente, Human in Control o la frontera de documentos normativos.

Si una etapa obligatoria se omite, debe tratarse como finding de proceso y resolverse antes de declarar el sprint cerrado.

> **Malāk crece desde evidencia verificable, reusa y revalida su diseño futuro preservado, cambia mediante gates pequeños y solo convierte evidencia en baseline a través de gobernanza humana.**
