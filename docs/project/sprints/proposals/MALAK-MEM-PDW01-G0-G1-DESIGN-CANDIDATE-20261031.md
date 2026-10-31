---
title: "Malāk MEM-PDW-01 — Protected Episodic Durable Write, G0/G1 Design Candidate"
status: "G0_RECONCILIATION_PARTIAL / G1_PRE_REVIEW / STOP_RED"
repository: Aranwill/jarvis
baseline_commit: 6bde76edf6b9953beb5019e48cfbf486ca785790
baseline_tree: 70d5f289ed97e1f72ac85c09b7c4ee80adc00652
unit_id: MEM-PDW-01
work_type: CRITICAL_CONTRACT_DESIGN
operation_level: 2
risk_class: 3
critical_contract: "YES"
authority_effect: none
as_of_date: 2026-10-31
---

# MEM-PDW-01 — G0/G1: contrato de la primera escritura episódica protegida

## 0. Resultado y criterio de continuidad

**Propuesta lista para revisión de diseño, no aprobada para implementación.** Se ha delimitado una unidad de laboratorio para comprobar el primer efecto durable protegido sin convertir el almacenamiento en confianza, ni habilitar memoria de conversación real.

**No se declara `G0 PASS`, `G1 PASS`, `Design 4R PASS`, `RDD Design Check PASS` ni autorización RED.** Este registro consolida decisiones candidatas verificables y los pendientes explícitos. No sustituye al ledger individual del Owner ni transforma automáticamente la revisión estructural en lectura completa.

## 1. Baseline, evidencia y riesgo

- `Aranwill/jarvis/main@6bde76edf6b9953beb5019e48cfbf486ca785790`; tree `70d5f289ed97e1f72ac85c09b7c4ee80adc00652`.
- Ledger ejecutado en Windows por el Owner: `417/417` rutas clasificadas, omisiones `0`, `review_depth_actual=STRUCTURAL_ONLY`, `preflight_result=INCONCLUSIVE`. Digest de paths `36dd4401dfa5276d623ef04f53132f6e1ff963ecec029885b693903ada18c344`.
- Reconciliación de la clasificación exacta del inventariador: **17 FULL**, **52 TARGETED**, **348 STRUCTURAL**. Esta es la *profundidad prevista*, no una promoción retroactiva de `review_depth_actual`.
- Cobertura focal de fuentes primarias: constituciones, Blueprint, ADR-002/003/006, `SECURITY.md`, método/protocolo/preflight, roadmap, `ideas.md`, `concepts/**`, interfaces de Memory/Security, tests episódicos y PEP, y stores de observabilidad. Evidencia de lectura no equivale por sí sola a ledger individual de profundidades cerrado.
- Operación del producto: nivel 2 (`persistente`). Riesgo del cambio: clase 3, contrato crítico `YES`.

## 2. Necesidad y revisión de reutilización

**Necesidad demostrada:** `InMemoryConversationContext` es efímero. Memory implementa Admission → Content Identity → Projection/Consumption → Persistence Readiness → AuthorizationRequest composition, pero no efectúa un **protected durable write**. `StrictPolicyEnforcementPoint` ya impone binding y permission; solo falta el efecto de dominio y un backend transaccional.

| Responsabilidad | Estado / decisión |
|---|---|
| EpisodicAdmission / Projection / Readiness | `REUSE`; sin cambios |
| Content identity (candidato completo) | `REUSE`; sin reinterpretar digest ni recortar texto |
| AuthorizationRequest composer | `REUSE`, fija `memory.episodic/persist` |
| PDP / Strict PEP / Audit | `REUSE`, sin bypass ni modificaciones |
| Kernel, Planner, ConversationService, CLI/Ollama | `NO_CHANGE`, sin wiring de escritura |
| Métricas/eventos JSONL | `REJECT` como backend de Memory; distintos contratos y datos |
| Operación de escritura de dominio | `NEW`, responsabilidad no implementada |
| Adaptador SQLite de infraestructura | `NEW`, persistencia técnica no implementada |

**Justificación de componentes nuevos:** 1) La operación de Memory enlaza objeto, alcance y precondiciones; 2) el adaptador de Infrastructure ejecuta únicamente una transacción. No añadir `MemoryManager`, `PersistenceAuthorizationManager`, PDP/PEP nuevos, event bus o registro central.

## 3. Frontera de confianza y contrato G1

### D01 — Laboratorio sólo con fixtures inmutables

El primer candidate solo acepta un **conjunto cerrado de fixtures sintéticos exactos** (identidad/digest registrados fuera de entradas del LLM). El host confiable selecciona un fixture; ni texto libre de CLI ni una etiqueta `synthetic` suministrada por el modelo bastan. **Datos reales, personales o sensibles: STOP, sin I/O.** Esta restricción evita fingir que ya hay consentimiento, minimización, cifrado o lifecycle productivo; esos contratos se admitirán en unidades futuras.

### D02 — Sujeto material y serialización verificables

El sujeto es el **`EpisodicMemoryCandidate` íntegro**, incluidas `origin`, `experience.user_content`, `experience.assistant_content`, `control` y timestamps. Antes de cualquier escritura se recalcula la identidad pública con `compute_episodic_candidate_content_identity` y se compara con la identidad de `readiness`. La serialización persistida debe reconstruir exactamente ese sujeto para poder comprobar el mismo digest; versión de schema y canonicalización obligatorias. Un recordatorio de una sola palabra extraído de una conversación **no hereda** la identidad del intercambio completo.

### D03 — Solicitud exacta y PEP como única vía

La composición privada crea una sola `AuthorizationRequest` mediante `compose_episodic_persistence_authorization_request(readiness, security_context, created_at)`. **La misma instancia** se captura con la operación inmutable y se pasa a `StrictPolicyEnforcementPoint.execute(request)`; no hay API pública que acepte por separado un PEP y una request alternativa. La operación declara `required_permission=PermissionScope('memory.episodic','persist')` y `authorization_binding=readiness.authorization_operation_binding`. El PEP sigue obteniendo la decisión de su PDP confiable, nunca de Qwen, Memory, fixture ni caller.

**Riesgo acotado:** `ProtectedOperation.execute()` no recibe la request como argumento. La garantía contra sustitución depende de mantener la construcción y ejecución dentro de la misma función privada, sin exponer operación reusable a callers no confiables. Si una prueba de sustitución demuestra que una request diferente (incluso con binding igual) puede persistir un marker ajeno, **STOP**; no se cambia PEP silenciosamente.

### D04 — Freshness y anti-replay son independientes del binding

`SecurityContext` y PDP comprueban temporalidad de autorización; `operation_binding` comprueba el sujeto. Ninguno equivale por sí solo a **anti-replay durable**. Al escribir, la operación registra transaccionalmente y de forma única el `request_id` y la huella de la operación. Duplicados no conceden autorización renovada, no sobrescriben contenido y no convierten un error previo en éxito.

### D05 — Transacción y fallos parciales

En una transacción SQLite `BEGIN IMMEDIATE` se insertan **juntos** el registro en cuarentena y sus marcadores de consumo. Constraints `UNIQUE(request_id)` y `UNIQUE(operation_binding...)` se aplican en el propio archivo. El `COMMIT` es el punto de persistencia. Ante caída antes del commit: rollback y cero efectos; caída después del commit pero antes del recibo: `UNKNOWN_TO_CALLER`, nunca reintentar con la autorización consumida ni afirmar ausencia del registro. La verificación posterior de estado es otra operación, no lectura libre de contenido para el modelo.

### D06 — Almacenamiento sin escritura arbitraria

El **laboratorio** utiliza un directorio temporal recién creado y poseído por el host de pruebas, **fuera del worktree**, con base SQLite nueva y fija. No se acepta una ruta libre procedente de Qwen, CLI o caller externo. No se afirma protección general contra ataques de reparse point/ACL en Windows, ni cifrado de SQLite; esta es otra razón para impedir datos reales. En caso de schema desconocido, corrupción, ruta que no cumpla la restricción de entorno o imposibilidad de verificar el destino: falla cerrada y sin reparación silenciosa.

### D07 — Estado, retención y lifecycle

Cada registro nace `QUARANTINED`. El fixture posee un `expires_at` lógico con horizonte de laboratorio propuesto de **24 h**, que NO significa borrado físico ni borrado seguro de WAL/backups. El fixture se destruye al cerrar el entorno temporal. No existe promoción a TRUSTED/Knowledge, ni lectura/inyección a conversaciones. Revocación, retención real, consentimiento, acceso y purga productivos serán gates de otro alcance; no se inventan aquí.

### D08 — Audit sin autoridad

La auditoría existente del PEP precede a la ejecución. **Audit `ALLOWED` no significa `COMMITTED`** y `COMMITTED` no significa `TRUSTED`. El receipt técnico solo incluye identidad y estado mínimo no sensible, sin volcar prompts, respuestas ni secretos en logs. `authority_effect=none`.

## 4. Alcance y budget de implementación candidata (no autorización)

Ficheros **propuestos** para la futura PR-B de implementación, todos nuevos:

1. `src/malak/memory/episodic_protected_write.py` — composición fija / validaciones del sujeto y operación vinculada; no selecciona policy ni concede permisos.
2. `src/malak/infrastructure/episodic_sqlite_store.py` — schema/atomic write/anti-replay del fixture sintético.
3. `tests/test_episodic_protected_write.py` — tests causales PEP/admission/binding.
4. `tests/test_episodic_sqlite_store.py` — transacción, conflictos y fallo parcial.

`NO_CHANGE`: Kernel, `src/malak/security/**`, contratos públicos, `src/malak/app/**`, Conversation/LLM, `SECURITY.md`, constituciones, Blueprint, ADR, E3/SCD-01, corpus, prompts y ground truth. Si la necesidad obliga a ampliar archivos o authority, STOP y nueva admisión.

**Topología:** PR-A documental de diseño (Draft → revisión → Owner Merge) **antes** de PR-B implementación (Draft RED/autoridad GREEN/validaciones/4R/CI/RDD/Owner Ready-Merge). No abrir PR extra para cada test.

## 5. Escenarios TDD futuros (sintéticos; no ejecutados aquí)

| ID | Escenario | Resultado observable mínimo |
|---|---|---|
| W01 | Projection/Admission/Readiness HOLD o DENIED | 0 llamadas a PEP/store |
| W02 | PDP DENY / contexto inválido | 0 escrituras; auditoría de rechazo |
| W03 | Permission o binding distintos | PEP bloquea antes de I/O |
| W04 | Candidato modificado, digest diferente o canonicalización no válida | 0 escrituras |
| W05 | Fixture exacto, actor autenticado y PDP ALLOW | 1 commit `QUARANTINED` |
| W06 | Reutilización de `request_id` | `REPLAY_REJECTED`, 0 filas nuevas |
| W07 | Nueva request con operation binding consumido | `CONFLICT`, 0 overwrite |
| W08 | Fallo antes del COMMIT | rollback y cero marker/payload |
| W09 | Fallo después de COMMIT antes del recibo | efecto persiste; `UNKNOWN_TO_CALLER`; no retry con autorización previa |
| W10 | Fixture no incluido en allowlist, entrada real o ruta externa | 0 I/O |
| W11 | Schema/version corrupta o inesperada | fail closed; no auto-migración |
| W12 | Receipt válido / registro en cuarentena | no lectura a prompt, no reliance/Knowledge |
| W13 | Request diferente con igual binding inyectada entre compositor y PEP | imposible por API privada; rechazo si se viola el mismo objeto capturado |
| W14 | Expiración lógica de fixture, source revocado o tainted | sin lectura/promoción; no falso borrado físico |

**RED legítimo:** falla conductual por operación aún ausente, no solo `ImportError`, test skip o mock ornamental. Sin GREEN hasta autorización separada y evidencia causal de RED.

## 6. Cuatro preguntas de ley

1. **Blueprint:** Memory conserva lifecycle semántico; Infrastructure I/O; Kernel coordina sin asumir persistencia. Compatible como diseño, no runtime validado.
2. **Cognitive Constitution:** `storage != trust`; `permission to persist != permission to rely`, CC-010/CC-013 preservadas. Compatible como diseño.
3. **Governance Constitution:** operación persistente nivel 2; PDP/PEP confiables, audit y Human in Control. Compatible como diseño.
4. **Kernel simplicity:** cero modificaciones, cero ownership de memoria durable en Kernel. Compatible como diseño.

## 7. Design 4R preliminar — sin promoción indebida

| Lente | Evidencia / limitación | Resultado |
|---|---|---|
| Risk | Datos sintéticos exactos, no CLI; owner del efecto identificado; falta comprobar G0 y composición real | `INCONCLUSIVE` |
| Readability | Dos responsabilidades y cuatro archivos candidatos; no hay managers ni nuevas policies | `PASS` (de diseño solamente) |
| Reliability | Lab SQLite 7/7 para atomicidad, replay y fallo parcial; integración real no ejecutada | `INCONCLUSIVE` |
| Resilience | Corrupción de schema / rollback contemplados; seguridad Windows y estado post-commit aún sin contrato validado sobre Malāk | `INCONCLUSIVE` |

`Design 4R` agregado `INCONCLUSIVE`; `RDD Stage 1 Design Check` `INCONCLUSIVE` hasta completar gate anterior. Los siete tests SQLite previos son **factibilidad aislada**, no evidencia RED/GREEN o PEP.

## 8. Construction Preflight P0–P7

| Campo | Estado al 2026-10-31 | Evidencia / stop |
|---|---|---|
| P0: Identity | `PASS` | Exact main baseline/tree; Owner path digest |
| P1: Sources/Depth | `PARTIAL` | 417 rutas clas., 17/52/348 profundidad prevista, ledger conserva `STRUCTURAL_ONLY`; referencias focales leídas en Github |
| P2: Invariants | `PARTIAL` | Se proponen invariantes D01-D08, no verificados sobre integración real |
| P3: Authority flow | `PASS` como diseño | Sin control ascendente, no autoridad al LLM, PDP/PEP existente |
| P4: Reuse/Necessity | `PASS` como diseño | REUSE/COMPOSE y dos responsabilidades NEW justificadas |
| P5: Risk | `DECLARED` | Nivel 2, risk_class=3, critical_contract=YES, 4R full, RDD Stage1/2 |
| P6: Scope | `PROPOSED` | Cuatro rutas nuevas futuras, sin cambios de código ahora; freeze requiere aceptación |
| P7: Terminal | `INCONCLUSIVE / STOP_RED` | P1, Design 4R y gate humano pendientes |

No crear un ledger de 417 líneas con `FULL_READ` inventado. La revisión de alcance G0 puede adjuntar un suplemento de lectura individual sobre el ledger exacto sin repetir `git ls-tree`.

## 9. Gates próximos exactos

1. **Consolidar suplemento de profundidades G0** sobre el TSV existente; las 348 inspecciones estructurales siguen siendo estructurales, no completas. Resolver las fuentes prioritarias 17 FULL y 52 TARGETED con notas de lectura atribuibles. `INCONCLUSIVE` hasta evidencia suficiente.
2. Confirmar D01-D08, archivo budget y modelo de fixture cerrado en revisión G1; completar Critical Contract Hardening, cuatro preguntas, Design 4R y RDD Stage 1 Design Check.
3. Tras aprobación humana de diseño, **PR-A Design** en Draft, una sola PR documental.
4. Tras Owner Merge de PR-A y autorización material aplicable, iniciar **PR-B** con RED causal y autorización de transición GREEN. Seguir §5.5, sin mezclar experimentos E3/Ollama.
5. Candidate FULL 4R, E2E, CI, revisión independiente, RDD Stage1 Candidate Conformance + Receipt Stage2 y decisión humana Ready/Merge.

**STOP si:** contenido real/no consentido, sustitución de request, modificación del PEP/Kernel, rutas no controladas, hash de candidato recortado, side effects antes de PDP/PEP, replay no atomicamente consumido, o intento de promover quarantine a truth/authority.

## 10. Evidencia y límites de afirmación

Fuentes primarias `Aranwill/jarvis` en commit `6bde76edf6b9953beb5019e48cfbf486ca785790`, en particular `AGENTS.md`, `SECURITY.md`, `docs/development/*`, `docs/architecture/*`, constituciones y ADR-002/003/006, `docs/project/implementation_roadmap.md`, `documents/projects/jarvis/ideas.md`, `docs/project/concepts/**`, `src/malak/memory/**`, `src/malak/security/**`, `src/malak/services/conversation_context.py`, pruebas de Memory/PDP/PEP.

No se han ejecutado modelos, no se ha incorporado almacenamiento a `main` ni se ha emitido autorización de persistencia real. `authority_effect=none`.

## 11. Disposición posterior de admisión documental del Owner (2026-10-31)

**Autorización humana explícita:** el Owner aprobó la profundidad de revisión proporcional para esta PR-A exclusivamente documental y la creación de su rama, commits y Pull Request Draft. No aprobó RED/GREEN, escritura real, cambio de Kernel ni incorporación de conversaciones a Memory.

- El ledger original del Owner conserva su identidad (417/417, cero omisiones, revisión estructural). No se reescribe como lectura completa.
- Las 17 fuentes normativas reciben revisión material focalizada y trazable, no una etiqueta ficticia FULL_READ; 52 fuentes de implementación/concepto tienen revisión focalizada y 348 siguen como inspección estructural. Se aplica la proporcionalidad expresamente aprobada *solo para admitir el diseño en PR-A*, conforme a Construction Protocol §3.2.
- Preflight P0: PASS (main SHA exacto). P1: PASS para revisión proporcional documental. P2 y P3: PASS como compatibilidad de diseño, sin operación nueva. P4: PASS, reuse de Memory/PDP/PEP y responsabilidades nuevas estrictamente justificadas. P5: PASS, risk_class=3, critical_contract=YES, operación nivel 2. P6: PASS para dos rutas documentales exclusivamente, sin cambios productivos. P7: PASS **solo para crear PR-A Draft como instrumento de revisión**, con disposición del Owner.
- **NO se declara G0/G1 sustantivos PASS**. Critical Contract Hardening definitivo, cuatro preguntas, Design 4R y RDD Stage 1 Design Check aún requieren revisión en PR-A. La lectura proporcional aceptada no es certificación de FULL_READ. PR-B/RED sigue prohibida hasta sus propios gates.

## 12. Alineación, identidad e implicaciones de diseño consolidadas para PR-A

| Fuente | Autoridad | Invariante | Evidencia baseline | Disposición | Efecto futuro | Diferido/rechazado | Razón | Trazabilidad |
|---|---|---|---|---|---|---|---|---|
| Constitución Cognitiva CC-010/011/013 | Normativa | Persistencia y reliance son transiciones distintas | Texto constitucional vigente | ADOPT | No promover stored a trusted | REJECT memoria automática | La retención no aporta verdad ni autoridad | `docs/governance/cognitive_constitution.md` |
| Constitución Gobernanza GOV-001 y nivel 2 | Normativa | Usuario conserva autoridad; persistencia según policy | Texto constitucional vigente | ADOPT | Permiso fijo y autorización explícita | REJECT autopermiso de LLM | La clasificación no concede permiso | `docs/governance/governance_constitution.md` |
| Blueprint R-023 / Kernel | Arquitectura normativa | No bypass y Kernel mínimo | Blueprint y Kernel vigentes | ADOPT | Memory owns domain, Infrastructure I/O | REJECT nuevo manager de autoridad | Reducir complejidad | `docs/architecture/blueprint.md` |
| SECURITY.md | Política activa | Fail-closed, disclosure, taint y consentimiento | Riesgos documentados | ADOPT | Fixture cerrado sin datos reales | DEFERRED memoria personal | Consentimiento no inferible | `SECURITY.md` |
| ADR-002 / ADR-003 | ADR aceptados | Binding exacto y dirección de control | PEP/permission declarada | ADOPT | Reutilizar PDP/PEP sin modificaciones | REJECT bypass y request de caller | Seguridad mantiene enforcement | `docs/architecture/adr/ADR-002-policy-enforcement-boundary.md` |
| ADR-006 | ADR aceptado | Retención distinta del reliance | Gate y límites actuales | ADOPT | Guardar únicamente en quarantine | DEFERRED lectura conversacional | No crear confianza por storage | `docs/architecture/adr/ADR-006-protected-durable-reliance-preconditions.md` |
| Memory readiness/composition | Código implementado | Candidate digest y binding exacto | Código y tests de Memory | ADOPT | Reuse de readiness y request | REJECT identidad de palabra extraída | Hash original protege candidato completo | `src/malak/memory/**` |
| Ledger/roadmap/concepts | Derivado y conceptual | Plan no constituye autorización | Roadmap, ideas y concepts | OBSERVE | Evidencia de gap | REJECT sistema adicional de RAG/agents | Evita sobreingeniería | `docs/project/implementation_roadmap.md` |

G1-D03B: el PEP genérico compara binding y permiso, pero `ProtectedOperation.execute()` no recibe la request. La composición de Memory **debe** crear internamente una request única y su operación vinculada, sin aceptar sustitución de request/PEP/operación desde caller. W19 prueba ese entrypoint, no atribuye al PEP capacidad inexistente. Si esa frontera no puede demostrarse con el scope previsto, STOP.

La evidencia de diseño está abierta a revisión. `authority_effect=none`; solo el Owner puede decidir Ready/Merge.
