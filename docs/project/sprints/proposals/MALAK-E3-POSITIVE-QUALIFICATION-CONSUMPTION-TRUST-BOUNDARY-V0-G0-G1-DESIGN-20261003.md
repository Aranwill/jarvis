---
title: E3 Positive Qualification Consumption Trust Boundary V0 — G0/G1 Re-Admission Design
status: design_candidate_bounded_correction_2
authority: evidence_only
language: es
as_of_date: 2026-10-03
baseline_commit: 8236e14e07a02c9f10bfc438bb914300d541ce0f
previous_candidate: eb36b1a83797986bdcb032f0f84873c2be2d9b70
first_reviewed_candidate: caf67a4f4071e40c017ef3567a1aa17aec311a19
risk_class: HIGH
critical_contract: true
correction_round: 2
authority_effect: none
---

# E3 Positive Qualification Consumption Trust Boundary V0

## 1. Estado de autoridad

Este documento materializa Bounded Correction 2 de G0/G1.

Historia candidate-bound:
- caf67a4f4071e40c017ef3567a1aa17aec311a19 → PRE-RED DESIGN REVIEW = FAIL;
- eb36b1a83797986bdcb032f0f84873c2be2d9b70 → PRE-RED DESIGN RE-REVIEW = FAIL.

El bounded re-review sobre el candidate anterior cerró en diseño:
- F248-PRED-01 — composition seam / same-seam E2E;
- F248-PRED-04 — StrictPolicyEnforcementPoint reuse;
- F248-PRED-05 — Alignment Matrix / File Coverage Ledger.

Y mantuvo OPEN / blocking:
- F248-PRED-02 — runtime qualification ↔ admitted material join y múltiples matches;
- F248-PRED-03 — punto efectivo de consumption-time sampling.

Bounded Correction 2 modifica exclusivamente el contrato documental necesario para F248-PRED-02 y F248-PRED-03. No reabre por decisión del Writer los findings 01/04/05; su cierre pertenece a Evidence externa ligada al candidate anterior y el nuevo reviewer sólo debe comprobar ausencia de regresión.

Esta corrección NO declara F248-PRED-02 ni F248-PRED-03 CLOSED.

Estado máximo:
- correction materialized;
- independent bounded re-review 2: PENDING;
- PRE-RED ADMISSION: PENDING;
- RED: NOT AUTHORIZED;
- GREEN: NOT AUTHORIZED;
- implementation: NOT AUTHORIZED;
- Ready: OWNER ONLY;
- Merge: OWNER ONLY;
- RDD Stage 2: NOT AUTHORIZED;
- authority_effect: none.

## 2. Identidad y scope

Repository: Aranwill/jarvis.

Baseline exacto:

8236e14e07a02c9f10bfc438bb914300d541ce0f

Candidate Identity strategy:

la Candidate Identity es el commit SHA exacto de la rama Draft después de materializar esta corrección. Cualquier cambio posterior invalida Evidence candidate-bound afectada.

Scope de esta Bounded Correction:

- MODIFY este design record;
- MODIFY File Coverage Ledger;
- production delta: 0;
- runtime delta: 0;
- test delta: 0;
- dependency delta: 0;
- Security contract delta: 0;
- PDP/PEP semantic delta: 0;
- authority delta: 0.

## 3. Construction Preflight revalidado

P0 — repository-first:

- repository exacto: PASS;
- baseline exacto: PASS;
- branch/ref: Draft PR #248;
- work type: G0/G1 Bounded Correction;
- prior external Evidence: bound únicamente a caf67a4f4071e40c017ef3567a1aa17aec311a19.

P1 — fuentes:

Se reconciliaron las fuentes normativas, arquitectónicas, de Security, CURRENT_STATE, RDD Stage 1, E3, Qualification Bundle, PEP y precedentes de projection/consumption aplicables.

P2 — invariants:

- Human in Control: PRESERVED;
- Kernel First: PRESERVED;
- Capability First: PRESERVED;
- Runtime Independence: PRESERVED;
- Zero Trust: PRESERVED;
- Least Privilege: PRESERVED;
- no bypass: REQUIRED;
- fail-closed: REQUIRED;
- Evidence != Authority: PRESERVED.

P3 — ADR-003:

authority/control fluye upstream → downstream.
results/findings/Evidence pueden retornar downstream → upstream con authority_effect = none.

P4 — reuse:

Overall disposition = COMPOSE / ADAPT.

REUSE obligatorio ahora incluye explícitamente:

- PermissionScope;
- AuthorizationOperationBinding;
- AuthorizationRequest;
- AuthorizationDecision;
- SecurityContext;
- Clock;
- SecurityContextValidator;
- PolicyDecisionPoint / StaticPolicyDecisionPoint;
- StrictPolicyEnforcementPoint;
- ProtectedOperation;
- AuthorizationAuditSink / existing authorization audit semantics.

P5:

- risk_class = HIGH;
- critical_contract = YES;
- Design FULL 4R = REQUIRED;
- RDD Stage 1 Design Check = REQUIRED;
- RDD Stage 2 = NOT AUTHORIZED.

P6:

Scope frozen a dos documentos en esta corrección.
Future implementation envelope permanece separado y NOT AUTHORIZED.

P7:

Construction Preflight Writer result = CANDIDATE PASS.

Independent Construction Preflight result = PENDING.

## 4. File Coverage Ledger corregido

Baseline inventory:

- tracked files discovered = 363;
- tracked files classified = 363;
- silently omitted files = 0;
- FULL_READ = 5;
- TARGETED_READ = 76;
- STRUCTURAL_INSPECTION = 282.

Fuentes promovidas explícitamente respecto del ledger anterior:

- src/malak/security/pep.py → FULL_READ;
- docs/architecture/adr/ADR-002-policy-enforcement-boundary.md → FULL_READ;
- scripts/evaluate_e3_deterministic_oracle_qualification.py → FULL_READ;
- docs/project/project_context.md → TARGETED_READ;
- docs/development/evidence_manifest.md → TARGETED_READ;
- tests/test_policy_enforcement_point.py → TARGETED_READ;
- tests/test_e3_deterministic_oracle_qualification.py → TARGETED_READ.

El File Coverage Ledger inventaría el baseline de 363 blobs. Los dos archivos de esta PR no se cuentan como baseline preexistente.

PROJECT - MANIFIESTO MALAK (1).docx no está presente en el baseline y no fue leído.

Detalle: docs/project/sprints/proposals/MALAK-E3-POSITIVE-QUALIFICATION-CONSUMPTION-TRUST-BOUNDARY-V0-G0-G1-FILE-COVERAGE-20261003.tsv.

## 5. Necesidad CURRENT

El baseline conserva deliberadamente:

caller-controlled FULL qualification
→ INFERENTIAL

La razón está implementada en route_governed_support_evidence_v0: coherencia estructural caller-controlled no demuestra external provenance ni positive governed reliance.

La unidad sólo intenta habilitar:

exact FULL structurally eligible oracle
+ independently reviewed qualification material
+ governed composition admission
+ exact Security enforcement
+ fresh consumption-time validation
→ candidate DETERMINISTIC

No autoriza oracle execution, support_sufficient, Protected Finalization, Kernel wiring, InternalInteraction ni runtime side effects.

## 6. Historia #242 / #243 / #245

PR #242, #243 y #245:

CLOSED / NOT MERGED / HISTORICAL_REFERENCE.

No se heredan PASS, RED, authorization ni Candidate Identity.

Constraints históricas:

- F242-PRED-01 — composition admission seam / configured PDP enforcement;
- F242-PRED-02 — admission lifetime / temporal revalidation;
- F242-PRED-03 — catalog completeness causal coverage.

Estado Writer después de esta Bounded Correction:

- F242-PRED-01 — CORRECTION MATERIALIZED / PENDING INDEPENDENT RE-REVIEW;
- F242-PRED-02 — CORRECTION MATERIALIZED / PENDING INDEPENDENT RE-REVIEW;
- F242-PRED-03 — DESIGN PROPERTY PRESERVED / RUNTIME UNTESTED.

## 7. Component / Logic Reuse Review corregido

### 7.1 REUSE — StrictPolicyEnforcementPoint

ADR-002 y src/malak/security/pep.py ya materializan la frontera Security correcta para una operación protegida:

AuthorizationRequest
→ exact required PermissionScope
→ exact ProtectedOperation.authorization_binding
→ StrictPolicyEnforcementPoint
→ configured PolicyDecisionPoint.decide(...)
→ AuthorizationDecision type/request_id/binding checks
→ audit
→ execute protected operation exactly once only if allowed

Por tanto esta unidad NO implementará una segunda versión local de:

- configured PDP invocation;
- AuthorizationDecision acceptance/validation;
- request_id enforcement;
- request/decision operation-binding equality;
- request/ProtectedOperation binding equality;
- required_permission enforcement;
- authorization audit fail-closed.

Disposition:

StrictPolicyEnforcementPoint = REUSE.
ProtectedOperation = REUSE contract.
Domain admission logic = ADAPT behind ProtectedOperation.

### 7.2 ADAPT — qualification domain validation

El Qualification Bundle y Review Evidence actuales contienen domain-specific validation que Security no interpreta.

La future admission operation puede validar semántica de Qualification después de structural/canonical prevalidation, pero no puede reimplementar Security authority semantics.

### 7.3 ADAPT — governed projection/consumption pattern

Memory demuestra un patrón útil:

raw material
→ governed validation
→ READY | HOLD | DENIED
→ fresh consumption-time checks
→ bounded downstream evaluation

Se adapta la propiedad. Engineering no importa Memory domain contracts.

### 7.4 ADAPT — E3 routing

P01–P09 actuales no se copian.

La future implementation debe extraer/reutilizar una única primitive interna pura de structural routing evaluation si necesita compartir selección con la boundary. route_governed_support_evidence_v0 y la positive boundary deben depender de la misma primitive.

Si P01–P09 requieren duplicación material:

STOP → scope review.

### 7.5 REJECT dentro de V0

- QualificationTrustManager;
- reviewer registry;
- persistent trust store;
- second Permission Engine;
- PKI/signatures;
- network verifier;
- new authority service;
- RDD Stage 2 credential system.

## 8. Threat model congelado

Primary threat:

request/caller fabrica FULL qualification
+ fabrica review-shaped material
+ fabrica allowed=True o READY-shaped object
→ false DETERMINISTIC.

V0 debe bloquear:

- caller-supplied AuthorizationDecision;
- caller-supplied READY;
- caller-supplied SecurityContext for the request-facing route call;
- caller-supplied PDP/PEP/Clock/boundary replacement;
- partial material binding;
- wrong candidate;
- wrong bundle;
- wrong oracle;
- wrong question/contracts;
- wrong catalog;
- stale runner material;
- unresolved verification refs;
- FAIL/INCONCLUSIVE dimensions;
- expired authorization context;
- duplicate READY;
- ambiguous FULL;
- RDD/review references used as bearer credentials.

Threat-model limit:

same-process arbitrary code can instantiate public Python classes.
V0 proves API/ownership and governed composition separation, not cryptographic process isolation.
SecurityContext.authenticated != cryptographic identity proof.

## 9. Exact governed composition seam — F248-PRED-01 correction

Candidate composition-only factory:

compose_governed_qualification_consumption_boundary_v0(...)

Esta factory pertenece a app/composition o a una composition-owned helper interna. No es parte de la request-facing Engineering API.

Governed composition inputs:

- exact qualification_bundle material;
- exact qualification_review_evidence material;
- expected_repository;
- expected_candidate_commit;
- governed SecurityContext;
- configured PolicyDecisionPoint;
- AuthorizationAuditSink;
- one governed Clock instance;
- optional HumanConfirmationEvidence sólo si la configured policy lo requiere.

Prohibido en request-facing route:

- qualification_bundle;
- review_evidence;
- SecurityContext;
- AuthorizationRequest;
- AuthorizationDecision;
- HumanConfirmationEvidence;
- PDP;
- PEP;
- Clock;
- READY admission;
- boundary constructor/factory/configuration.

Composition ownership invariant:

governed composition
→ constructs exact boundary once from admitted material
→ passes already-composed boundary to the request consumer

request consumer
→ may call boundary.route(...)
→ cannot replace its admitted set through route arguments.

No claim criptográfico se deriva de object ownership.

## 10. ProtectedOperation + PEP chain — F248-PRED-04 correction

Candidate domain operation:

GovernedQualificationReviewAdmissionOperationV0
implements ProtectedOperation[GovernedQualificationReviewAdmissionV0].

It exposes:

required_permission =
PermissionScope(
  resource = engineering.qualification_review_consumption,
  action = admit
)

authorization_binding =
AuthorizationOperationBinding(
  namespace = engineering.qualification_review_consumption,
  binding_version = v0,
  digest_algorithm = sha256,
  digest_hex = derived exact admission binding digest
)

Positive admission chain:

1. composition validates the raw Qualification Bundle and Review Evidence shape/bounds/bindings;
2. composition derives the exact authorization binding;
3. composition samples governed Clock for AuthorizationRequest.created_at;
4. composition constructs AuthorizationRequest;
5. composition constructs the domain ProtectedOperation with the same required_permission and binding;
6. composition constructs StrictPolicyEnforcementPoint using the configured PDP and audit sink;
7. PEP.execute(request, confirmation?) invokes the configured PDP internally;
8. PEP verifies request/operation permission, request/operation binding, decision type, request_id and decision binding;
9. PEP writes authorization audit;
10. only after allowed enforcement, ProtectedOperation.execute() may materialize the positive domain admission;
11. composition performs the final temporal freeze check before exposing READY.

Caller-supplied AuthorizationDecision is not accepted anywhere in this seam.

Mapping of PEP outcomes:

- AuthorizationDeniedError → admission DENIED;
- AuthorizationEnforcementError or audit/enforcement infrastructure failure → admission HOLD;
- operation semantic FAIL → admission DENIED;
- operation semantic INCONCLUSIVE/missing material → admission HOLD;
- only exact positive chain → admission READY.

No DENIED/HOLD result can be promoted to READY later.

## 11. Exact Qualification material contracts — F248-PRED-02 correction

The admission design binds to the current integrated contracts from:

scripts/evaluate_e3_deterministic_oracle_qualification.py

Qualification Bundle schema:

MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-BUNDLE/v0

Review Evidence schema:

MALAK-E3-DETERMINISTIC-ORACLE-QUALIFICATION-REVIEW-EVIDENCE/v0

Current canonical serialization:

JSON UTF-8
sort_keys = true
separators = comma/colon without whitespace
ensure_ascii = false
digest = sha256(canonical_json)

The admission layer MUST NOT trust declared digest-shaped strings when corresponding material is available.
It must reuse or preserve equivalent validation of the current runner contract.

## 12. Exact binding payload v0

### 12.1 Admission material binding

Canonical domain payload before sha256:
QUALIFICATION_REVIEW_ADMISSION_BINDING/v0

Fields, exact and versioned:
1. schema = QUALIFICATION_REVIEW_ADMISSION_BINDING/v0
2. repository
3. evaluated_candidate_commit
4. qualification_bundle_schema_version
5. qualification_bundle_digest — recomputed from the exact Qualification Bundle
6. oracle_identity: oracle_id, oracle_version, oracle_content_digest, oracle_producer_subject_id
7. governed_question_material: relation_id, evaluation_question_identity, input_contract_identity, output_contract_identity
8. obligation_catalog_digest — recomputed from exact obligation_catalog material
9. verification_evidence_digest — recomputed from exact verification_evidence material
10. qualification_material_digest — recomputed from exact qualification_material
11. qualification_method
12. executing_runner_version
13. executing_runner_digest
14. review_evidence_schema_version
15. review_evidence_digest — recomputed from exact Review Evidence object
16. reviewed_relation_id
17. reviewed_evaluation_question_identity
18. reviewed_obligation_catalog_digest
19. structural_validator_result
20. catalog_completeness_result
21. independence_review_result
22. verification_material_review_result
23. qualification_review_result
24. implementation_actor_id
25. qualification_reviewer_id
26. qualification_validator_id
27. authority_effect

Derived, never caller-trusted when material exists:
- qualification_bundle_digest;
- obligation_catalog_digest;
- verification_evidence_digest;
- qualification_material_digest;
- review_evidence_digest;
- AuthorizationOperationBinding.digest_hex.

Expected, composition-owned:
- expected_repository;
- expected_candidate_commit.

Declared fields must match recomputed/expected values. Any mismatch: no READY.

### 12.2 Runtime Qualification Binding V0 — F248-PRED-02

The positive boundary MUST derive a second binding specifically for the qualification object that routing actually consumes.

Logical name: RuntimeQualificationBindingV0.

Exact fields:
- repository;
- evaluated_candidate_commit;
- oracle_id;
- oracle_version;
- oracle_content_digest;
- relation_id;
- evaluation_question_identity;
- input_contract_identity;
- output_contract_identity;
- coverage_claim;
- oracle_producer_subject_id;
- qualifier_subject_id;
- qualification_evidence_digest;
- qualification_identity;
- authority_effect.

For Positive Qualification Consumption V0 the mapping is frozen as:
- coverage_claim MUST equal FULL;
- qualifier_subject_id MUST equal Review Evidence.qualification_reviewer_id;
- qualification_evidence_digest MUST equal the recomputed qualification_bundle_digest;
- authority_effect MUST equal none;
- repository MUST equal composition-owned expected_repository;
- evaluated_candidate_commit MUST equal composition-owned expected_candidate_commit.

The expected qualification_identity is recomputed by composition using the exact same canonical material used by GovernedDeterministicOracleQualificationV0:
- coverage_claim;
- evaluation_question_identity;
- input_contract_identity;
- oracle_content_digest;
- oracle_id;
- oracle_producer_subject_id;
- oracle_version;
- output_contract_identity;
- qualification_evidence_digest;
- qualifier_subject_id;
- relation_id.

Serialization:
- JSON UTF-8;
- ensure_ascii = false;
- sort_keys = true;
- separators = comma/colon without whitespace;
- sha256(canonical_json).

The derived expected qualification_identity MUST equal both selected oracle.qualification.qualification_identity and selected oracle.qualification_identity.

Baseline evidence for this V0 bridge:
- current runtime qualification identity already binds qualification_evidence_digest and qualifier_subject_id;
- current deferred consumption tests bind Review Evidence.qualification_bundle_digest to qualification.qualification_evidence_digest.

This equality is a V0 contract decision. If a future version needs qualification_evidence_digest to mean a different artifact than Qualification Bundle digest, that requires a new version/scope review; it MUST NOT be silently reinterpreted.

Role strings remain provenance only: qualifier_subject_id == qualification_reviewer_id != cryptographic proof of human independence.

### 12.3 Routing candidate relation

For this V0 positive boundary:
route.baseline_commit MUST equal boundary.expected_candidate_commit and therefore MUST equal admitted evaluated_candidate_commit.

This is an explicit V0 contract, not an inferred universal equivalence between every field named baseline/candidate in Malāk.

If route.baseline_commit differs:
- existing P01–P09 structural result is preserved;
- positive admission lookup is not eligible;
- no DETERMINISTIC upgrade.

## 13. Mapping to current runner invariants

The future admission validation must preserve these current causal checks before positive reliance:

- exact BUNDLE_KEYS;
- artifact bound;
- exact bundle schema version;
- exact candidate SHA form;
- exact oracle identity schema;
- exact governed question material schema;
- obligation catalog material and recomputed digest;
- exact coverage set/cardinality;
- resolved verification evidence refs;
- verification evidence material and recomputed digest;
- candidate_binding on verification Evidence;
- qualification_method exact;
- executing_runner_version exact;
- executing_runner_digest validated against the executing evaluator contract when applicable;
- qualification_material_digest recomputed;
- governed binding repository/candidate/oracle/question/catalog/bundle equality;
- Review Evidence schema exact;
- Review Evidence repository/candidate/bundle/question/catalog equality;
- role IDs bounded and declared role separation;
- structural_validator_result matches structural evaluation;
- catalog_completeness_result is terminal causal input;
- authority_effect == none;
- terminal result aggregation remains PASS | FAIL | INCONCLUSIVE.

This design does NOT claim that role strings prove real-world identity independence.

## 14. Admission lookup, instance identity and ambiguity — F248-PRED-02

Two identities are intentionally separate.

### 14.1 RuntimeQualificationBindingKeyV0

Routing lookup is keyed ONLY by material derivable from composition-owned repository/candidate expectation plus the exact selected oracle and GovernedDeterministicOracleQualificationV0.

Key fields are exactly the RuntimeQualificationBindingV0 fields defined in §12.2.

review_evidence_digest is NOT part of this lookup key.

Reason: two different review artifacts about the same runtime qualification must not become two silently selectable positive routes.

### 14.2 AdmissionInstanceKeyV0

Each installed admission also has a provenance/instance identity:
RuntimeQualificationBindingKeyV0
+ qualification_bundle_digest
+ review_evidence_digest
+ authorization_context_id
+ authorization_request_id
+ AuthorizationOperationBinding.digest_hex.

This instance key is for provenance, duplicate detection and audit. It is not the request lookup selector.

### 14.3 Exact lookup algorithm

After existing routing reaches the exact-one-FULL residual point:
1. verify route.baseline_commit == boundary.expected_candidate_commit;
2. derive RuntimeQualificationBindingV0 from selected oracle/qualification and composition-owned expected repository/candidate;
3. recompute selected qualification_identity from its runtime fields;
4. require exact equality with oracle.qualification_identity and stored expected runtime binding;
5. collect every installed admission whose RuntimeQualificationBindingKeyV0 equals the derived key;
6. apply cardinality fail-closed.

Cardinality:
- 0 matching admissions → existing INFERENTIAL fallback;
- exactly 1 matching HOLD → no DETERMINISTIC;
- exactly 1 matching DENIED → no DETERMINISTIC;
- exactly 1 matching READY → eligible for temporal consumption check;
- more than 1 matching admission, regardless of review_evidence_digest or outcome → ADMISSION_AMBIGUOUS / no DETERMINISTIC.

Therefore changed qualification_evidence_digest, qualifier_subject_id, qualification_identity or candidate cannot match the prior admission. Two distinct PASS reviews for the same runtime qualification are ambiguous if both are installed. READY mixed with HOLD/DENIED across different review digests is also ambiguous.

V0 does not create durable anti-replay across processes or boundary lifetimes.

## 15. Admission outcome contract

GovernedQualificationReviewAdmissionV0:

READY | HOLD | DENIED.

READY requires all simultaneously:

- exact schemas and bounds;
- exact expected repository;
- exact expected candidate;
- all material digests recomputed and matching;
- exact governed binding;
- structural_validator_result PASS;
- catalog_completeness_result PASS;
- independence_review_result PASS;
- verification_material_review_result PASS;
- qualification_review_result PASS;
- authority_effect none;
- exact PermissionScope;
- exact AuthorizationOperationBinding;
- PEP allowed;
- request/decision/operation coherence;
- final temporal check PASS.

DENIED:

- explicit policy denial;
- material/binding/candidate mismatch;
- any required review dimension FAIL;
- authority_effect != none;
- invalid permission or exact binding mismatch.

HOLD:

- required material missing;
- any required review dimension INCONCLUSIVE;
- unsupported/malformed schema where positive trust cannot be established;
- clock invalid/unavailable;
- PEP enforcement/audit infrastructure failure;
- unresolved external validation requirement.

READY != DETERMINISTIC.
READY != semantic truth.
READY != Authority.
READY != Ready/Merge of the PR.

## 16. Temporal contract exact — F248-PRED-03 Bounded Correction 2

One governed Clock instance is composition-owned for the positive boundary. The same Clock object MUST construct the SecurityContextValidator used by the configured StaticPolicyDecisionPoint and be retained by the consumption boundary.

The request-facing route call receives no time input.

### 16.1 Admission timing

admission_started_at = clock.now()

Requirements:
- datetime;
- timezone-aware;
- context.issued_at <= admission_started_at < context.expires_at.

AuthorizationRequest.created_at MUST be set explicitly to admission_started_at. The default wall-clock factory is not used for this seam.

After PEP.execute returns a positive domain operation result:
admission_evaluated_at = clock.now()

Requirements:
- datetime;
- timezone-aware;
- admission_started_at <= admission_evaluated_at < context.expires_at.

If context expires between PDP/PEP enforcement and READY freeze: no READY.

READY retains the exact frozen SecurityContext object used by AuthorizationRequest, plus authorization_request_id, authorization_request_created_at, authorization_operation_binding and admission_evaluated_at. Consumption never accepts a replacement SecurityContext.

### 16.2 Effective consumption point

consume_at is NOT sampled at boundary.route entry.

Positive consumption order is frozen as:
boundary.route
→ shared P01–P09 structural evaluation
→ exact-one-FULL residual point
→ derive exact RuntimeQualificationBindingV0
→ bounded in-memory admission lookup/cardinality
→ require exactly one READY matching admission
→ consume_at = governed_clock.now() sampled exactly once
→ temporal validation against the exact retained SecurityContext
→ positive DETERMINISTIC upgrade.

This single sample is the effective point of positive reliance.

Requirements:
- consume_at is datetime;
- timezone-aware;
- admission_evaluated_at <= consume_at < authorization_context.expires_at;
- consume_at >= authorization_context.issued_at.

Edges:
- admission_started_at == context.issued_at → allowed if all other checks PASS;
- admission_evaluated_at == admission_started_at → allowed;
- consume_at == admission_evaluated_at → allowed;
- consume_at == context.expires_at → ADMISSION_STALE;
- consume_at > context.expires_at → ADMISSION_STALE;
- consume_at < admission_evaluated_at → CLOCK_REVERSED / no DETERMINISTIC;
- naive/non-datetime/exception from Clock → CLOCK_INVALID / no DETERMINISTIC.

If the context expires while P01–P09 or admission lookup are running, the post-lookup consume_at sample observes expiry and blocks the positive upgrade.

After consume_at, V0 permits only bounded pure in-memory comparisons and result construction before return: no I/O, network, user callback, second policy decision or second clock sample.

The guarantee is validity at the effective positive reliance sample. It is NOT a claim that the context remains valid indefinitely after the function returns.

No new monotonic clock service is introduced. V0 does not claim detection of every backward wall-clock movement across separate successful calls.

## 17. Exact request-facing API seam

Candidate request-facing object:

GovernedQualificationConsumptionBoundaryV0.

Its route method mirrors the existing structural routing request material:

route(
  policy_version,
  baseline_commit,
  focus_id,
  evidence_set_digest,
  relation_id,
  evaluation_question_identity,
  finding_fingerprint,
  resolved_evidence_material_digest,
  declared_evidence_complete,
  scope_expansion_required,
  oracles,
  expected_binding
) -> GovernedSupportEvidenceRoutingV0

It exposes NO argument for:

- review Evidence;
- admission;
- SecurityContext;
- AuthorizationRequest;
- AuthorizationDecision;
- confirmation;
- PDP;
- PEP;
- Clock;
- configuration/factory.

The free function route_governed_support_evidence_v0 remains public and fail-closed exactly as today.

A caller that only has the free function cannot obtain DETERMINISTIC from caller-controlled FULL qualification.

## 18. Routing integration without P01–P09 duplication

Future implementation rule:
1. extract or reuse one pure internal structural evaluation primitive from current route_governed_support_evidence_v0;
2. preserve current P01–P09 ordering, reason codes and free-function behavior;
3. free function maps exact-one-FULL residual eligibility to existing INFERENTIAL fallback;
4. boundary.route uses the SAME structural evaluation result;
5. only at exact-one-FULL residual may the boundary derive RuntimeQualificationBindingV0;
6. require route.baseline_commit == boundary.expected_candidate_commit;
7. compare runtime binding exactly with installed admission runtime binding;
8. perform bounded lookup by RuntimeQualificationBindingKeyV0;
9. require exactly one matching READY admission;
10. only then sample consume_at once and perform temporal validation;
11. only exact runtime join + exact single READY + fresh temporal validation may upgrade to DETERMINISTIC;
12. otherwise preserve INFERENTIAL or the earlier existing structural outcome.

The structural evaluator must expose enough selected-oracle information for the boundary to derive runtime binding without recomputing a second selection algorithm.

If one primitive cannot serve both paths without behavioral drift: STOP → scope review.

## 19. Same-seam Future E2E contract — preserved after Bounded Correction 2

Positive E2E-equivalent:
governed composition
→ exact raw Qualification Bundle + Review Evidence
→ recompute canonical material/digests
→ derive admission material binding
→ derive expected RuntimeQualificationBindingV0
   - qualification_evidence_digest := recomputed qualification_bundle_digest
   - qualifier_subject_id := qualification_reviewer_id
   - expected qualification_identity recomputed
→ derive exact AuthorizationOperationBinding
→ admission_started_at from governed Clock
→ AuthorizationRequest(created_at = admission_started_at)
→ ProtectedOperation
→ StrictPolicyEnforcementPoint
→ configured PDP
→ audit/enforcement
→ domain positive operation
→ admission_evaluated_at from governed Clock
→ final READY freeze with exact SecurityContext
→ immutable GovernedQualificationConsumptionBoundaryV0
→ request boundary.route with ordinary routing args only
→ same P01–P09 structural evaluator
→ selected exact-one-FULL oracle/qualification
→ route.baseline_commit == expected_candidate_commit
→ derive actual RuntimeQualificationBindingV0
→ exact bounded lookup by runtime binding
→ exactly one matching READY
→ consume_at = governed Clock.now() once at effective reliance point
→ temporal validation
→ DETERMINISTIC.

Negative E2E uses the same boundary.route seam.

Additional negatives:
- free route + caller-controlled FULL → INFERENTIAL;
- changed qualification_evidence_digest → no DETERMINISTIC;
- changed qualifier_subject_id / recomputed qualification_identity → no DETERMINISTIC;
- multiple installed reviews matching one runtime qualification → ADMISSION_AMBIGUOUS;
- context expires during structural evaluation/lookup → consume_at detects stale.

A fixture that directly instantiates AuthorizationDecision(allowed=True), READY admission or a pretrusted boundary does NOT satisfy the positive E2E.

## 20. Fail-closed precedence

Before any positive upgrade:
1. existing P01 schema/bounds;
2. existing P02–P05 policy/exact subject binding;
3. existing P06–P07 oracle/qualification/cardinality;
4. existing P08 material completeness;
5. require route.baseline_commit == boundary.expected_candidate_commit;
6. derive exact RuntimeQualificationBindingV0;
7. require qualification identity/evidence/reviewer mapping equality;
8. lookup all admissions by RuntimeQualificationBindingKeyV0;
9. require cardinality exactly one;
10. require that admission READY;
11. consume_at = governed Clock.now() exactly once;
12. validate exact retained SecurityContext freshness/time ordering;
13. positive upgrade.

No DETERMINISTIC on missing/HOLD/DENIED admission, multiple matches, stale/clock failure, baseline/candidate mismatch, qualification_evidence_digest/bundle mismatch, qualifier/reviewer mismatch, qualification_identity mismatch, candidate/material drift, or catalog/review non-PASS.

## 21. Future RED requirements — NOT AUTHORIZED

Existing PQCTB-R01..R42 remain required, with R34 interpreted as configured composition + exact runtime qualification join + exact fresh READY + exact FULL → DETERMINISTIC.

Bounded Correction 2 adds individual causal requirements:
- PQCTB-R43 selected qualification.qualification_evidence_digest != recomputed qualification_bundle_digest → no DETERMINISTIC;
- PQCTB-R44 selected qualification.qualifier_subject_id != admitted qualification_reviewer_id → no DETERMINISTIC;
- PQCTB-R45 selected qualification_identity != composition-derived expected qualification_identity → no DETERMINISTIC;
- PQCTB-R46 route.baseline_commit != boundary.expected_candidate_commit/evaluated_candidate_commit → no DETERMINISTIC;
- PQCTB-R47 two admissions with same RuntimeQualificationBindingKeyV0 but different review_evidence_digest → ADMISSION_AMBIGUOUS / no DETERMINISTIC;
- PQCTB-R48 admission_started_at == context.issued_at positive edge may proceed;
- PQCTB-R49 admission_evaluated_at == admission_started_at positive edge may proceed;
- PQCTB-R50 context expires during P01–P09 or admission lookup before consume_at sample → ADMISSION_STALE / no DETERMINISTIC;
- PQCTB-R51 consume_at is sampled only after exact-one-FULL structural result and exact-one-READY lookup, immediately before temporal reliance check;
- PQCTB-R52 consumption validates the exact frozen SecurityContext used by AuthorizationRequest; request cannot replace it.

R39 material invalidation MUST include runtime qualification_evidence_digest, qualifier_subject_id and derived qualification_identity.
R40 candidate invalidation MUST include route.baseline_commit versus boundary.expected_candidate_commit/evaluated_candidate_commit.

Negative domain tests must start from a valid positive composition and vary only the intended dimension where causal isolation requires it.

RED remains NOT AUTHORIZED.

## 22. Malāk Alignment Matrix — Construction Protocol §4.6 compliant

| source | source_authority_class | applicable_invariant_or_intent | baseline_evidence | alignment_disposition | implementation_effect | deferred_or_rejected_effect | rationale | traceability_reference |
|---|---|---|---|---|---|---|---|---|
| Cognitive Constitution | normative_protected | Evidence before material reliance; uncertainty explicit; no self-certification | current constitution + E3 fail-closed baseline | ADOPT | require exact Evidence binding and non-PASS preservation | cryptographic identity proof deferred | positive reliance cannot arise from caller assertion | docs/governance/cognitive_constitution.md |
| Governance Constitution | normative_protected | Human in Control; Evidence != Authority | authority_effect none; Owner gates remain human | ADOPT | no RED/Ready/Merge authority in component | autonomous promotion REJECTED | routing trust cannot promote project state | docs/governance/governance_constitution.md |
| Blueprint | architecture | Kernel First; Capability First; no bypass | current E3 lives in Engineering capability code; Kernel delta 0 | ADOPT | keep boundary outside Kernel | Kernel/Planner changes REJECTED | no new coordination responsibility | docs/architecture/blueprint.md |
| Kernel specification | architecture | Kernel remains coordination-only | current kernel contracts unchanged | ADOPT | Kernel delta 0 | business/security admission in Kernel REJECTED | preserve existing responsibility | docs/architecture/kernel.md |
| Architecture Quality Gates | architecture | contracts, dependencies, testability, reversibility | current architecture gates apply to critical contract | ADOPT | explicit seams, stop conditions and bounded scope | silent coupling REJECTED | pre-RED design must be testable | docs/architecture/architecture_quality_gates.md |
| SECURITY.md | protected_security_policy | Zero Trust, least privilege, fail-closed | current Security primitives + deny by default | ADOPT | exact PermissionScope + configured enforcement | caller-supplied trust REJECTED | positive trust must cross existing Security boundary | SECURITY.md |
| ADR-002 | accepted_architecture_decision | PDP decision obtained by PEP; exact binding and required permission | StrictPolicyEnforcementPoint already enforces request/decision/operation chain | ADOPT | REUSE PEP + ProtectedOperation + audit | local duplicate enforcement REJECTED | closes F248-PRED-04 and F242-PRED-01 | docs/architecture/adr/ADR-002-policy-enforcement-boundary.md; src/malak/security/pep.py |
| ADR-003 | accepted_architecture_decision | authority downstream; Evidence may return upstream with zero authority | design has authority_effect none | ADOPT | no upward control path | result-as-authority REJECTED | preserve directional authority | docs/architecture/adr/ADR-003-directional-communication-and-authority-flow.md |
| ADR-004 | accepted_architecture_decision | specification and verification before acceptance | current positive path remains blocked until pre-RED gates | ADOPT | freeze causal RED/E2E before implementation | implementation-first REJECTED | critical contract requires testable design | docs/architecture/adr/ADR-004-specification-and-verification-first.md |
| ADR-005 | accepted_architecture_decision | Protected Finalization remains separate | current finalization coupling not authorized | ADOPT | no finalization delta | coupling DEFERRED | trust boundary is not final response authority | docs/architecture/adr/ADR-005-evidence-bound-final-response-transition.md |
| ADR-006 | accepted_architecture_decision | durable reliance requires stronger preconditions | this V0 has no durable side effect/store | OBSERVE | no durable guarantee claimed | anti-replay/store/idempotency DEFERRED | avoid overclaiming V0 | docs/architecture/adr/ADR-006-protected-durable-reliance-preconditions.md |
| Engineering Method | development_contract | Writer != Reviewer != Validator != Authority; RDD Stage 1 | current correction requires bounded re-review | ADOPT | independent review remains separate | self-certification REJECTED | process Evidence remains candidate-bound | docs/development/engineering_method.md |
| Construction Protocol | development_contract | §4.6 matrix; §5.5 critical sequence | prior candidate failed matrix adequacy | ADOPT | complete matrix and ledger depth | informal traceability REJECTED | closes F248-PRED-05 | docs/development/malak_construction_protocol.md §4.6/§5.5 |
| Evidence Manifest v1 | development_contract | Candidate-bound Evidence; Stage 1 only | baseline/candidate SHA binding and authority_effect none | ADAPT | current external review bound only to old candidate | Receipt/Stage2 semantics REJECTED | candidate change invalidates affected Evidence | docs/development/evidence_manifest.md |
| project_context | derived_current_state | recover CURRENT state without authority elevation | as_of 2026-10-02; routing line and deferred scopes recorded | ADAPT | planning context only; revalidated against Git | treating derived snapshot as authority REJECTED | CURRENT_STATE source must be targeted-read | docs/project/project_context.md |
| implementation roadmap | derived_current_state | next implementation sequence and not-authorized scopes | current E3 direction and later boundaries | ADAPT | keep unit bounded before later wiring | Sprint 7.12/support_sufficient wiring DEFERRED | no implicit roadmap advancement | docs/project/implementation_roadmap.md |
| ideas.md | conceptual_non_normative | long-horizon evidence/reliance ideas | non-normative candidate concepts | OBSERVE | no direct implementation effect | speculative autonomy/store concepts DEFERRED | lower authority cannot drive current contract | documents/projects/jarvis/ideas.md |
| Research Horizon Map | conceptual_non_normative | track external research without importing authority | research candidates remain non-normative | OBSERVE | no direct implementation effect | unrelated horizon items DEFERRED | evidence source, not permission | docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md |
| Evidence Bound Cognition concept | conceptual_non_normative | exact Evidence before reliance | aligned with bounded positive trust | ADAPT | reinforce exact material/candidate binding | broader cognition promotion DEFERRED | use intent without expanding scope | docs/project/concepts/MALAK_EVIDENCE_BOUND_COGNITION_FOUNDATION.md |
| Swarm / ephemeral agent concepts | conceptual_non_normative | governed future execution | not part of E3 positive qualification consumption | REJECT | none | agents/swarm execution REJECTED for V0 | unrelated responsibility | docs/project/concepts/GOVERNED_SWARM_LONG_HORIZON_REFERENCE.md; GOVERNED_EPHEMERAL_AGENT_EXECUTION_EVIDENCE_REFERENCE.md |
| Current E3 routing | implementation | P01–P09 ordering and caller-only FULL fail-closed | route_governed_support_evidence_v0 exact baseline behavior | ADAPT | share one internal structural evaluator; free API unchanged | duplicated P01–P09 REJECTED | preserve regression-equivalence | src/malak/capabilities/_engineering_analysis.py; tests/test_e3_governed_support_evidence_routing_v0.py |
| Qualification Bundle runner | evaluation_tooling | exact schema, canonical JSON, material digests, external review aggregation | current runner recomputes catalog/evidence/material/bundle digests and runner identity | ADAPT | positive admission binds exact current material and derives RuntimeQualificationBindingV0 | digest-shaped declarations without material REJECTED | bundle material must join exactly to the runtime qualification consumed by routing | scripts/evaluate_e3_deterministic_oracle_qualification.py; tests/test_e3_deterministic_oracle_qualification.py |
| Routing qualification binding tests | verification_evidence | runtime qualification identity binds qualifier_subject_id + qualification_evidence_digest; deferred helper bridges bundle digest | current tests derive qualification_identity and use qualification_bundle_digest = qualification.qualification_evidence_digest while positive consumption remains deferred | ADAPT | freeze V0 bridge qualification_evidence_digest := bundle digest and qualifier_subject_id := qualification_reviewer_id; require exact identity join | caller-declared reviewer/digest without governed admission REJECTED | exposes current intended bridge without treating caller-controlled objects as trust | tests/test_e3_routing_qualification_binding_v0.py; tests/test_e3_governed_support_evidence_routing_v0.py |
| StrictPolicyEnforcementPoint tests | verification_evidence | caller cannot inject decision; exact binding/permission chain | existing tests exercise direct PDP acquisition and fail-closed mismatches | ADOPT | Future RED composes same primitive | bypass/duplicate enforcement REJECTED | reuse verified baseline behavior | tests/test_policy_enforcement_point.py |
| Governed projection/consumption precedent | implementation | immutable projection + fresh downstream consumption checks | Memory modules/test suites show READY/HOLD/DENIED and fresh temporal evaluation | ADAPT | pattern only; no Engineering→Memory import | domain coupling REJECTED | reuse architecture pattern, not domain contracts | src/malak/memory/governed_input_projection.py; src/malak/memory/governed_projection_consumption.py |

OBSERVE and DEFERRED items remain outside implementation scope.
REJECT items preserve their reason so they cannot silently reappear.

## 23. Necessity & Complexity Review

- need demonstrated by current fail-closed routing: YES;
- consumer contract exists: YES;
- positive runtime consumer wired today: NO / not required for G0/G1;
- simpler safe current behavior exists: keep INFERENTIAL;
- if positive route is pursued, Security PEP reuse is simpler than new enforcement: YES;
- new subsystem necessary: NO;
- new authority necessary: NO;
- Kernel complexity delta: 0.

Writer result:

PASS for continuing design admission only.

## 24. Critical Contract Hardening — Writer recheck

Bounded Correction 2 freezes the two residual ambiguities from the external re-review.

F248-PRED-02:
- exact RuntimeQualificationBindingV0;
- qualification_evidence_digest := recomputed Qualification Bundle digest;
- qualifier_subject_id := qualification_reviewer_id;
- expected qualification_identity recomputed with current runtime semantics;
- route.baseline_commit == expected/evaluated candidate for this V0;
- runtime lookup key distinct from admission instance key;
- all admissions matching one runtime qualification considered together;
- more than one match fails closed regardless review digest/outcome.

F248-PRED-03:
- consume_at removed from route entry;
- P01–P09 and bounded lookup happen first;
- exactly-one-READY identified before sampling;
- consume_at sampled once immediately before positive temporal reliance check;
- exact frozen SecurityContext retained from AuthorizationRequest;
- expiry during structural evaluation/lookup observed by later sample;
- guarantee bounded to effective reliance sample, not indefinitely after return.

Previously frozen contracts remain unchanged: composition-only factory, trust-free request API, PEP/ProtectedOperation reuse, PermissionScope, canonical material binding, same-seam E2E, shared P01–P09 evaluator, no durable anti-replay/cryptographic identity/Stage2.

Writer result: CANDIDATE PASS.
Independent bounded re-review 2: PENDING.

## 25. Four Law Questions — Writer recheck

Blueprint — CANDIDATE PASS.
Reason: Kernel delta 0, Engineering responsibility remains bounded, no bypass.

Cognitive Constitution — CANDIDATE PASS.
Reason: exact material and uncertainty are preserved; role strings/authenticated context are not treated as semantic truth or cryptographic identity.

Governance Constitution — CANDIDATE PASS.
Reason: PEP decides operational authorization within existing Security; Owner retains RED/Ready/Merge authority.

Kernel complexity — CANDIDATE PASS.
Reason: no Kernel/Planner delta and no new manager/framework.

Independent results remain PENDING.

## 26. Design FULL 4R — Writer recheck

Risk — CANDIDATE PASS.
Runtime qualification substitution and multiple matching reviews now fail closed; stale-use is checked at the effective positive reliance point.

Readability — CANDIDATE PASS.
Admission material binding, runtime qualification binding, admission instance identity, routing lookup key and consumption sample are now distinct.

Reliability — CANDIDATE PASS.
Candidate, bundle digest, reviewer/qualifier, qualification identity and cardinality have deterministic rules.

Resilience — CANDIDATE PASS.
Expiry during structural work/lookup, clock failure/reversal, multiple matches and runtime/admission drift fail closed.

DESIGN FULL 4R Writer result: CANDIDATE PASS.
Independent FULL 4R: PENDING.

## 27. RDD Stage 1 Design Check — Writer recheck

Preserved:
- exact baseline;
- Candidate Identity strategy;
- Evidence provenance;
- first external FAIL bound to caf67a4f4071e40c017ef3567a1aa17aec311a19;
- first bounded re-review FAIL bound to eb36b1a83797986bdcb032f0f84873c2be2d9b70;
- F248-PRED-01/04/05 closure Evidence belongs to the previous candidate and requires only no-regression confirmation on the corrected SHA;
- F248-PRED-02/03 require new independent closure Evidence;
- Writer != Reviewer != Validator != Authority;
- PASS | FAIL | INCONCLUSIVE;
- INCONCLUSIVE != PASS;
- Bounded Correction;
- affected Evidence invalidation;
- authority_effect = none;
- RDD Stage 2 NOT AUTHORIZED.

Writer result: CANDIDATE PASS.
Independent result: PENDING.

## 28. Finding correction ledger

F248-PRED-01: EXTERNAL CLOSED IN DESIGN on eb36b1a83797986bdcb032f0f84873c2be2d9b70. Current candidate: PENDING NO-REGRESSION CONFIRMATION only.

F248-PRED-02: BOUNDED CORRECTION 2 MATERIALIZED. Evidence: §§12.2–12.3, 14, 18–21, 22, 24, 26. Closure: PENDING INDEPENDENT BOUNDED RE-REVIEW 2.

F248-PRED-03: BOUNDED CORRECTION 2 MATERIALIZED. Evidence: §16, §§18–21, 24, 26. Closure: PENDING INDEPENDENT BOUNDED RE-REVIEW 2.

F248-PRED-04: EXTERNAL CLOSED IN DESIGN on eb36b1a83797986bdcb032f0f84873c2be2d9b70. PEP/ProtectedOperation reuse unchanged. Current candidate: PENDING NO-REGRESSION CONFIRMATION only.

F248-PRED-05: EXTERNAL CLOSED IN DESIGN on eb36b1a83797986bdcb032f0f84873c2be2d9b70. §4.6 matrix/ledger preserved with added runtime-join traceability. Current candidate: PENDING NO-REGRESSION CONFIRMATION only.

F242-PRED-01: EXTERNAL CLOSED IN DESIGN on eb36b1a83797986bdcb032f0f84873c2be2d9b70; runtime UNTESTED.
F242-PRED-02: Bounded Correction 2 materialized through §16; closure PENDING.
F242-PRED-03: PASS de diseño preserved / runtime UNTESTED.

No finding is declared newly CLOSED by the Writer.

## 29. Future implementation envelope — NOT AUTHORIZED

If and only if independent pre-RED review PASS and Owner later authorizes RED:

Possible production files:

- src/malak/capabilities/_engineering_analysis.py;
- one bounded internal E3 admission module only if cohesion requires it;
- src/malak/app/composition.py only if causally required for composition ownership.

Possible Security usage:

- import/reuse existing contracts, PEP, PDP protocol, Clock and audit interfaces;
- NO edits to Security contracts;
- NO edits to PEP semantics;
- NO edits to PDP semantics.

Possible tests:

- one focused PQCTB V0 module;
- existing E3 routing tests for regression;
- PEP tests only if a regression gap is discovered, not to change semantics.

Hard zero delta:

- Kernel;
- Planner;
- runtime/provider/model;
- Conversation;
- support_sufficient;
- Protected Finalization;
- InternalInteraction;
- network;
- store;
- registry;
- new dependencies;
- RDD Stage 2.

If any hard-zero item becomes necessary:

STOP → scope review.

## 30. Gate state after Bounded Correction 2

Construction Preflight — WRITER CANDIDATE PASS.
G0 / admission — WRITER CANDIDATE PASS.
Component / Logic Reuse Review — COMPOSE / ADAPT with explicit PEP REUSE.
Necessity & Complexity Review — WRITER CANDIDATE PASS.
Malāk Alignment Matrix — MATERIALIZED / §4.6-equivalent.
Critical Contract Hardening — WRITER CANDIDATE PASS after runtime join + consumption point correction.
Four Law Questions — WRITER CANDIDATE PASS.
Design FULL 4R — WRITER CANDIDATE PASS.
RDD Stage 1 Design Check — WRITER CANDIDATE PASS.

External PRE-RED review on caf67a4f4071e40c017ef3567a1aa17aec311a19 — FAIL / HISTORICAL CANDIDATE-BOUND EVIDENCE.
External bounded re-review on eb36b1a83797986bdcb032f0f84873c2be2d9b70 — FAIL / HISTORICAL CANDIDATE-BOUND EVIDENCE.

Previous external dispositions:
- F248-PRED-01 CLOSED in design;
- F248-PRED-04 CLOSED in design;
- F248-PRED-05 CLOSED in design;
- F248-PRED-02 OPEN;
- F248-PRED-03 OPEN.

Current corrected candidate:
- F248-PRED-02 correction materialized / independent closure PENDING;
- F248-PRED-03 correction materialized / independent closure PENDING;
- F248-PRED-01/04/05 no-regression confirmation PENDING;
- PRE-RED ADMISSION PENDING.

RED — NOT AUTHORIZED.
GREEN — NOT AUTHORIZED.
implementation — NOT AUTHORIZED.
Ready — OWNER ONLY.
Merge — OWNER ONLY.
RDD Stage 2 — NOT AUTHORIZED.
authority_effect — none.

## 31. Next lawful transition

Independent bounded read-only re-review 2 must focus on:
- F248-PRED-02 runtime qualification ↔ admission join;
- F248-PRED-03 effective consumption-time sampling;
- Future RED adequacy for R43–R52 and affected prior tests;
- Future E2E-equivalent adequacy;
- Critical Contract Hardening;
- Risk / Readability / Reliability / Resilience;
- F242-PRED-02;
- no-regression confirmation only for F248-PRED-01/04/05 and F242-PRED-01.

It must not repeat the full audit from zero unless a new blocker or scope drift is discovered.

No RED may be materialized before an independent terminal PASS and explicit Owner authorization.
