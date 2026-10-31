---
title: "Malāk MEM-PDW-01 — G0 Reconciliation & G1 Critical Contract Hardening Candidate"
status: "G0_PARTIAL / G1_DESIGN_CANDIDATE / STOP_IMPLEMENTATION"
date: "2026-10-31"
repository: "Aranwill/jarvis"
source_baseline: "6bde76edf6b9953beb5019e48cfbf486ca785790"
work_unit: "MEM-PDW-01"
risk_class: 3
critical_contract: true
authority_effect: "none"
---

# Malāk — MEM-PDW-01: reconciliación del ledger y contrato de escritura protegida

## 0. Alcance y veredicto

**Entrada comprobada por el Owner:** `MALAK-MEM-PDW-01-STRUCTURAL-LEDGER/v0` en `D:\Ollama\malak-memory-ledger-20261031-135857`, 417 archivos trackeados y clasificados, 0 omitidos, `review_depth_actual=STRUCTURAL_ONLY`, `preflight_result=INCONCLUSIVE`, baseline exacto `6bde76edf6b9953beb5019e48cfbf486ca785790`.

**Resultado de este documento:** avance de análisis y diseño, **no** cierre de G0/G1 ni autorización RED/GREEN. El inventario estructural se admite como evidencia de cobertura de rutas, no de lectura exhaustiva por archivo. No se modifican código, corpus, CI ni PR #360. No se infiere ejecución de modelos ni persistencia real.

**Necesidad real:** crear un *protected durable write* episódico, manteniendo `storage != trust`, `permission to persist != permission to rely` y autoridad externa al LLM.

## 1. Reconciliación de superficies del baseline

| Superficie | Evidencia verificable | Disposición | Efecto propuesto |
|---|---|---|---|
| `InMemoryConversationContext` | 6 intercambios por sesión, memoria efímera, ningún write durable | REUSE para contexto; REJECT como DB | NO_CHANGE |
| `ConversationService`, `ConversationCapability`, CLI | Chat ejecutable con Ollama, sin autorización de memoria persistente ni identidad autenticada para esa operación | OBSERVE | NO_CHANGE |
| `EpisodicMemoryCandidate` | Incluye `origin`, `experience.user_content`, `experience.assistant_content`, `control` y `created_at` | REUSE con límite de datos | NO_CHANGE |
| `compute_episodic_candidate_content_identity` | SHA-256 sobre payload canónico que incluye **ambos textos** del intercambio | REUSE | NO_CHANGE |
| `evaluate_episodic_persistence_readiness` | READY / HOLD / DENIED; binding atado al candidato e intent | REUSE | NO_CHANGE |
| `compose_episodic_persistence_authorization_request` | `memory.episodic/persist` y exact operation binding; sin decision/enforcement | REUSE | NO_CHANGE |
| `StaticPolicyDecisionPoint` | Decide sobre SecurityContext, permiso y policy | REUSE | NO_CHANGE |
| `StrictPolicyEnforcementPoint` | Valida request, decisión, permiso y binding; audita antes del efecto | REUSE | NO_CHANGE |
| stores de métricas y eventos | Operaciones de observabilidad, no Memory | REJECT como Memory store | NO_CHANGE |
| Archivo/DB episódico durable | No hay efecto persistente implementado en el baseline | NEW, sujeto a justificación G1 | No crear todavía |

**Fuentes aplicables revisadas:** AGENTS.md, Construction Preflight, Construction Protocol §5.5, Engineering Method, Development Checklist, Blueprint, Kernel, Cognitive Constitution CC-010/CC-013, Governance Constitution, Architecture Quality Gates, SECURITY.md, ADR-002, ADR-003, ADR-006, roadmap/ideas/concepts, código y tests relacionados de Memory, Security, Conversation y Ollama. La revisión de todas las 417 entradas del ledger a la profundidad declarada por archivo aún no fue acreditada, por lo que G0 permanece inconcluso.

## 2. Dos gaps materiales que cambian la implementación

### G1-F01 — Exact payload vs. "recordar una palabra"

El candidato existente `EpisodicMemoryCandidate` contiene **texto completo del usuario y del asistente**, y ambos son parte de la identidad calculada. Persistir "solo la palabra" bajo la identidad del intercambio íntegro es una sustitución material inválida. Persistir el candidato íntegro sin consentimiento específico expone más contenido del necesario.

**Resolución propuesta:** MEM-PDW-01 sólo admitirá **fixtures sintéticos no sensibles** de candidato completo, generados fuera del chat normal. Ningún token de conversación real pasa al store. Para recordar preferencias/factos reales se requerirá una futura proyección que cree un *nuevo candidato* con provenance y una *nueva identidad* antes de pasar por admission/readiness/PDP/PEP; no se recorta el payload dentro del store ni se reutiliza el hash original.

**STOP:** si se solicita persistir chats reales, secretos, identidad personal o datos sensibles usando esta unidad, devolver `SCOPE_NOT_ADMITTED`, sin I/O.

### G1-F02 — Readiness y operation binding no son anti-replay/consent

`EpisodicPersistenceReadinessResult.READY` no es una autorización PDP. `AuthorizationRequest.request_id` existe, pero el binding de readiness no prueba por sí solo que una request no se haya usado antes. Tampoco el modelo de `EpisodicAdmissionContext` aporta, por sí mismo, evidencia formal de consentimiento del usuario.

**Resolución propuesta:** exigir precondición de consentimiento/retención verificable **en la capa de composición**, nunca deducida de una instrucción textual dirigida a Qwen. Para datos sintéticos, la operación de laboratorio será iniciada explícitamente por el Owner con SecurityContext válido, policy aplicable y auditoría. El efecto guardará un marcador durable único de request/operación en la **misma transacción** que el registro. Un segundo uso de la misma request devuelve `REPLAY_REJECTED` y no escribe. El resultado de una operación anterior no actúa como permiso para otra.

**STOP:** si falta evidencia de consentimiento o mecanismo anti-replay ligado a identidad, expiración y operación exactas, no existe implementación habilitable.

## 3. G1 — Contrato candidato, acotado y fail-closed

**D1. Fuente/consentimiento.** Permitidos en la primera unidad: datos sintéticos, explícitamente marcados como `lab_synthetic`, libres de secretos, sin PII y con propósito técnico cerrado. Rechazar otros datos antes de construir la operación. Una etiqueta suministrada por el modelo no prueba por sí sola que el material sea seguro.

**D2. Content identity.** Recalcular `EpisodicCandidateContentIdentity` inmediatamente antes del efecto. Confirmar igualdad exacta del candidato, intent, readiness, autorización y payload serializado canónico. No permitir cambios de canonicalización de forma silenciosa. SHA-256 demuestra consistencia de bytes, no autenticidad de fuente ni verdad semántica.

**D3. Autorización.** Usar la misma `AuthorizationRequest` de `compose_episodic_persistence_authorization_request`, una operación con `required_permission=PermissionScope('memory.episodic','persist')` y `authorization_binding` correspondiente, ejecutada exclusivamente mediante `StrictPolicyEnforcementPoint`. La operación no llama a PDP ni emite decisiones de autoridad. El resultado `PDP ALLOW` no es durable reliance.

**D4. Freshness y anti-replay.** Un request_id único, autenticado y vigente debe quedar consumido transaccionalmente junto con el efecto; reintentar la misma request rechaza el replay aunque el contenido coincida. No equiparar un SHA/digest a nonce ni a prueba temporal. La operación necesita conservar la identidad exacta del request que su PEP autorizó, sin alterar contratos públicos; si la composición existente no puede demostrar esa unión, detener G1 antes de RED.

**D5. At-most-once effect y fallo parcial.** SQLite `BEGIN IMMEDIATE`, constraints `UNIQUE` por request y por clave lógica de operación, `COMMIT` atómico. Si hay crash después de `COMMIT` y antes de informar receipt, una futura operación de *status* de solo lectura, autorizada de forma separada, podrá indicar `ALREADY_COMMITTED` solo tras verificar identidad exacta. No volver a efectuar el write utilizando una autorización anterior. No prometer exactly-once delivery.

**D6. Lifecycle.** Todo registro sintético se almacena inicialmente `QUARANTINED`, con `created_at`, `expires_at`, propósito y metadata de provenance. No hay transición a `TRUSTED/ACTIVE` ni lectura para prompts dentro de MEM-PDW-01. La revocación o vencimiento bloquea cualquier uso. Retención máxima candidata: 24 h para laboratorio, sujeta a aceptación de G1. TTL lógico/DELETE no implica borrado físico seguro.

**D7. Store.** `sqlite3` estándar, archivo fuera de worktree, ruta proporcionada por host y validada fail-closed. Se prohíbe crear DB si ruta, propietario/permisos, symlink/reparse point, schema o configuración de almacenamiento no son seguros o verificables. No reutilizar stores de logs/metricas. No afirmar que SQLite cifre datos; sin esquema de cifrado validado, ningún dato sensible se admite.

**D8. Integridad y auditoría.** El store conserva versión de schema, la identidad canónica del candidato y binding, request_id y provenance mínimos. No registrar full prompts, respuestas, secretos o payload completo en observabilidad. La auditoría del PEP conserva su ownership. Si DB falla/corrompe, fail closed, sin regeneración silenciosa.

**D9. Recuperación.** No hay API para inyectar memoria persistida en `ConversationRequest` ni volverla Knowledge. `MEM-RETRIEVE-01` posterior deberá definir acceso, identidad, taint/quarantine, purpose, freshness, disclosure, minimización y *reliance* con autorización distinta. `Storage != trust`.

**D10. No nuevo subsistema.** Una operación protegida Memory-local y un helper privado de almacenamiento son opciones, no aprobación automática de clases/archivos. Si se demuestra que un solo módulo cubre el efecto sin mezclar autoridad e I/O indebidamente, preferir un solo módulo. Ningún nuevo Kernel, MemoryManager, PDP, PEP o dependencia externa.

## 4. Contrato de estados candidato

```text
NOT_ADMITTED / CONSENT_MISSING / SENSITIVE_DATA / SUBJECT_MISMATCH
    → STOP, 0 I/O
READINESS_HOLD / READINESS_DENIED / AUTH_DENIED / STALE_AUTH
    → STOP, 0 write
BINDING_MISMATCH / PAYLOAD_MISMATCH / INVALID_STORE
    → STOP, 0 write
FIRST_AUTHORIZED_COMMIT
    → 1 stored QUARANTINED synthetic record + consumed request marker
REPLAY_SAME_REQUEST
    → REPLAY_REJECTED, 0 additional writes
DUPLICATE_LOGICAL_OPERATION_DIFFERENT_BYTES
    → CONFLICT, 0 overwrites
COMMIT_THEN_RECEIPT_FAILURE
    → UNKNOWN_TO_CALLER; authorized status lookup may reconcile; no blind retry
```

**Advertencia:** estos son resultados candidatos de dominio, no enum oficial aprobado ni RDD terminal. No se implementarán ni se presentarán como tests verdes hasta superar los gates.

## 5. Matriz RED acotada, sin repetir E3/Ollama

| ID | Precondición / inyección | Esperado |
|---|---|---|
| W01 | Readiness HOLD/DENIED | 0 writes; sin invocation de store |
| W02 | PDP DENY o SecurityContext inválido | 0 writes; audit conforme PEP |
| W03 | Permiso ≠ `memory.episodic/persist` | PEP rechaza, 0 writes |
| W04 | Payload/candidate alterado tras readiness | binding mismatch, 0 writes |
| W05 | Solicitud válida + candidato sintético | un `COMMIT` y un registro en quarantine |
| W06 | Repetición de request consumida | replay denegado; no segundo write |
| W07 | Mismo operation key, material distinto | conflict; no overwrite |
| W08 | Crash tras COMMIT antes del receipt | recuperación de status sin doble efecto; no reutilización de permiso |
| W09 | Sin consentimiento o TTL o datos sensibles | 0 writes |
| W10 | Revocado, expired, tainted, quarantined | no read/promoción a trust |
| W11 | Corrupción DB, ruta de escape o schema incompatible | fail-closed, ninguna autocorrección encubierta |
| W12 | Receipt de escritura | no habilita trust, inference, knowledge ni durable reliance |

Las pruebas W01–W12 son **especificación RED futura**; no se ejecutaron. En laboratorio no se usa un modelo de lenguaje.

## 6. Evaluación arquitectónica y 4R de diseño (no Candidate FULL 4R)

- **Blueprint:** el efecto de Memory queda downstream; Kernel/Runtime no asumen ownership del almacenamiento. Compatible **condicionalmente**.
- **Cognitive Constitution CC-010/CC-013:** la memoria persistida no constituye verdad, conocimiento, autorización ni reliance. Compatible **condicionalmente**.
- **Governance Constitution:** Human in Control, permisos por defecto denegados, clasificación de operación persistente y auditoría. Compatible **condicionalmente**.
- **Kernel simplicity:** Kernel permanece sin cambios; se aprovecha PEP/PDP existentes. Favorable.
- **Risk:** `risk_class=3` alto, envenenamiento de memoria, disclosure, replay y crash. **Pendiente** resolver procedimientos antes de RED.
- **Readability:** distinguir autorización, efecto, estado y futuras lecturas. Favorable sin managers adicionales.
- **Reliability:** propuesta transaccional `UNIQUE/COMMIT`, hash de material y binding. **Pendiente** tests causales.
- **Resilience:** fallo parcial, corrupción, taint, expiry y restore. **Pendiente** pruebas y contrato completo.

**No se declara Design 4R PASS.** Son disposiciones de diseño preliminar; RDD Stage 1 Design Check no realizado.

## 7. File Coverage y estados formales

| Requisito | Estado real | Evidencia / por qué no se promueve |
|---|---|---|
| P0 identidad del baseline | PASS focal | 417 rutas, SHA exacto del baseline |
| Ledger de cobertura de rutas | PASS estructural | 417/417, 0 omitidos |
| P1 lectura completa del set obligatorio | PARTIAL | hay fuentes focales leídas; `review_depth_actual=STRUCTURAL_ONLY` en ledger |
| P2 arquitectura, Seguridad, Memory | PARTIAL | gaps G1-F01/F02 identificados, no resueltos contractualmente |
| P3 direccionalidad | PRELIMINARY PASS | propuesta evita control ascendente; implementación no evaluada |
| P4 REUSE/COMPOSE/NEW | PARTIAL | responsabilidades identificadas; falta justificar módulo(s) nuevos conforme a AGENTS |
| P5 riesgo/criticidad | DECLARED | risk 3, critical contract YES, FULL 4R, independent validation y RDD Stage 1+2 |
| P6 scope e identidad de candidate | PROPOSED | sin freeze ni SHA de implementación |
| P7 preflight terminal | **INCONCLUSIVE / STOP** | no hay autorización de RED ni escritura durable |
| G0 / G1 | **NOT CLOSED** | faltan gate formal, decisiones finales y Design 4R |
| Runtime/DB escritura real | **ABSENT** | no se creó código ni se ejecutó DB |

## 8. Próximo acto material sin repetición de suite

**El inventario NO debe repetirse.** Usar su directorio exacto y registrar el digest de paths. Siguiente paso es reconciliar las entradas marcadas `FURTHER_REVIEW_PENDING` mediante lectura de las fuentes aplicables, validar G1-F01/F02 y completar la New Component Justification. El equipo no debe reabrir E3, SCD-01 ni ejecutar Qwen.

Antes de RED se requiere **decisión explícita del Owner** sobre este alcance de persistencia *sintética de laboratorio*, el límite de retención y el contrato de autorización/replay. Luego Design 4R/RDD Design; sólo después se puede crear una única Implementation PR Draft con RED trazable. La autorización de GREEN es un gate separado del Protocol §5.5.

**Conclusión:** ya existe un diseño preciso del delta que falta y de las dos condiciones que bloquean persistir información real. No es lícito confundir el ledger estructural con preflight aprobado ni el mecanismo de guardar bytes con Memory usable en conversaciones.

## Adenda de hardening actualizada para revisión PR-A (W15–W19)

**W15 — mismo candidato, nuevo binding temporal:** `compute_episodic_persistence_operation_binding` integra los timestamps de intent y readiness. La transacción debe exigir `UNIQUE(request_id)`, `UNIQUE(authorization_binding)` y `UNIQUE(candidate_id)`, sin sobrescribir un registro existente ni afirmar deduplicación semántica de distintos IDs. El laboratorio aislado confirmó el defecto del esquema anterior y la corrección en `2/2`; esto no constituye validación productiva de PEP.

**W16 — caducidad al instante de escritura:** antes de abrir la transacción SQLite, la operación protegida captura su request exacta y revalida `issued_at <= trusted_now < expires_at`. La comprobación anterior del PDP/PEP no permite inferir vigencia posterior al retraso de ejecución.

**W17 — concurrencia:** dos conexiones SQLite simultáneas que intenten confirmar el mismo candidato deben serializar el efecto mediante transacción y restricciones de unicidad DB, no mediante un mutex de proceso.

**W18 — integridad:** al obtener un registro o validar un efecto, el contenido material completo debe corresponder al digest y versión de canonicalización originalmente vinculados. Ante discrepancia, bloquear/quarantine; nunca convertir digest en verdad semántica ni entregar a la conversación.

**W19 — sustitución de AuthorizationRequest:** `StrictPolicyEnforcementPoint` no identifica request sustituida cuando su binding coincide con el capturado por una operación de otro contexto. La composición privada de Memory no admite request, policy, PEP ni operación proporcionados por el caller. Debe construir request y operación juntos y llamar al PEP con el objeto exacto. W19 valida que la entrada pública no permita inyección ni I/O en la variante negativa. No adjudicarle una garantía inexistente al PEP.

**Restricción adicional:** en esta primera unidad, fixtures sintéticos cerrados, persistencia cuarentenada, sin CLI/LLM, sin Memory retrieval, sin contenido real, sin cambio de Kernel/Security. El contrato de retención, consentimiento real, revocación/taint y filesystem security permanece requisito separado antes de memoria personal. Los resultados de laboratorio son factibilidad, no RED/GREEN ni G1/4R/RDD PASS. El Owner autorizó solo la PR-A documental Draft, no la implementación.
