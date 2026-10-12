---
title: Malāk E3 HVC-A — PR-B Execution / RED→GREEN Ledger
status: implementation_draft
authority: non_normative
language: es
date: 2026-10-12
baseline_commit: b5d2c39c32033e8df51b8101ec87606c2c0dcb59
baseline_tree: 6931188572dce6836bff5c388fd7a4d21fe0d5aa
trigger_issue: 282
risk_class: 3_HIGH
critical_contract: true
authority_effect: none
correction_round: 3
---

# HVC-A PR-B — Execution / RED→GREEN Ledger

## 1. Propósito

Materializar el contrato HVC-A integrado en PR #283 sin seleccionar verifier,
model/provider ni introducir settlement. Esta PR conserva candidates RED y GREEN
separados dentro de una única Draft PR conforme Construction Protocol §5.5.

## 2. Human authorization

La instrucción del Owner del 2026-10-12, “avancemos … quiero seguir avanzando
con Malāk”, queda registrada en issue #282 como autorización para iniciar PR-B y
transicionar RED→GREEN con evidencia candidate-bound separada.

No concede Ready/Merge ni amplía autoridad.

## 3. Preflight PR-B

```text
repository                    Aranwill/jarvis
baseline                      b5d2c39c32033e8df51b8101ec87606c2c0dcb59
tree                          6931188572dce6836bff5c388fd7a4d21fe0d5aa
tracked baseline files        391
recursive tree truncated      false
PR-A design                   INTEGRATED / PR #283
Research Horizon update       INTEGRATED / PR #284

P0 baseline                   PASS
P1 sources/hierarchy          PASS
P2 invariants                 PASS
P3 authority direction        PASS
P4 reuse/necessity            PASS / ADAPT existing E3 contract surface
P5 risk                       3_HIGH
critical_contract             YES
P6 scope                      FROZEN
P7 result                     PASS

Critical Contract Hardening   PASS / inherited design + no new semantics
law questions                 PASS / unchanged
Design 4R                     PASS / integrated PR-A
RDD Stage 1 Design Check      PASS / integrated PR-A
RED                           AUTHORIZED
GREEN                         AUTHORIZED after preserved RED evidence
Candidate FULL 4R             REQUIRED after GREEN
independent GT validation     REQUIRED
RDD Stage 1 Candidate         REQUIRED
RDD Stage 2 Receipt           REQUIRED
Ready / Merge                 OWNER ONLY
```

## 4. Reuse / complexity

```text
SemanticObservationV0             ADAPT existing _engineering_analysis.py
existing binding primitives       REUSE
blind projection pattern          REUSE / ADAPT
V0.4                              PRESERVE / REFERENCE
new Capability                    NO
new service/manager/layer         NO
Kernel/Planner                    NO_CHANGE
support_sufficient                NO_CHANGE
Protected Finalization            NO_CHANGE
U08                               BLOCKED
```

## 5. PR-B file budget

Allowed add:

- `docs/project/sprints/proposals/MALAK-E3-HVC-A-SEMANTIC-OBSERVATION-GROUND-TRUTH-CONTRACT-PR-B-EXECUTION-20261012.md`
- `docs/project/sprints/proposals/MALAK-E3-HVC-A-SEMANTIC-OBSERVATION-GROUND-TRUTH-CONTRACT-PR-B-FILE-COVERAGE-20261012.tsv`
- `evaluations/e3_hvc_a_semantic_observation_v0/visible_cases.json`
- `evaluations/e3_hvc_a_semantic_observation_v0/ground_truth.json`
- `tests/test_e3_hvc_a_semantic_observation_v0.py`

Allowed modify in GREEN only:

- `src/malak/capabilities/_engineering_analysis.py`

All other baseline files are forbidden for PR-B absent Bounded Correction and
explicit scope reopening.

## 6. RED contract

RED must demonstrate that the baseline lacks the HVC-A public contract while the
tests encode:

- exact enum domains;
- one observation ↔ one evidence_ref;
- authority_effect = none;
- NON_MATERIAL / UNKNOWN / PARTIAL fail-closed combinations;
- LIMITS != CONTRADICTS;
- scope NONE != sufficiency;
- EXTERNAL_REQUIRED and UNKNOWN remain non-positive;
- evidence_ref must resolve inside visible case material;
- hidden ground-truth keys cannot cross the visible projection;
- claim_part_id is accepted only when already supplied;
- list/multi-observation settlement is outside HVC-A;
- ground-truth discriminability pairs remain distinct.

Expected RED reason: missing HVC-A symbols on the exact RED candidate, not an
unrelated regression.

## 7. GREEN boundary

GREEN may only add the minimal contract and deterministic validation/projection
helpers required by RED. It may not add inference, model calls, scoring,
aggregation, settlement or finalization.

## 8. Independent Ground-Truth Review

The blind reviewer receives `evaluations/e3_hvc_a_semantic_observation_v0/visible_cases.json` only. The hidden file
`evaluations/e3_hvc_a_semantic_observation_v0/ground_truth.json` and model outputs/qualification results are prohibited inputs.

Independent validation remains PENDING until performed by an actor distinct from
the writer. This document does not self-certify that gate.

## 9. Stage 2

Risk 3 requires a valid external `MALAK-EVIDENCE-MANIFEST/v1`, terminal
RDD Stage 1 Candidate Conformance and
`MALAK-RDD-VALIDATION-RECEIPT/v1` before human Ready.

Receipt != Ready != Merge != Authority.

## 10. Candidate FULL 4R — preliminary review / Bounded Correction round 1

GREEN inicial:

```text
candidate       03c446cdfdeafb2a120fc0ba5998c9c2150acbb0
tree            0ed15f001351b4ecf817c6a4e4f456e5429fce0a
Ubuntu tests    2052 / 2052 PASS
compileall      PASS
diff validation PASS
```

FULL 4R preliminar encontró un finding bloqueante acotado:

```text
HVC-A-PRB-F01
type        evaluation-pack completeness
runtime     unaffected
problem     matrix items 6/7/9/10 existed as tests but were not frozen as
            explicit contract adversarial vectors in Ground Truth
disposition BOUNDED_CORRECTION
```

Corrección:

- freeze MISSING_EVIDENCE_MATERIAL_VS_SEMANTIC_UNKNOWN;
- freeze EXACT_BINDING_VS_BINDING_DRIFT;
- freeze ONE_VALID_OBSERVATION_VS_DUPLICATE_SET;
- freeze VALID_ABSTAINING_OBSERVATION_VS_UNKNOWN_ENUM;
- preserve all four as deterministic INVALID contract adversarials;
- no semantic labels are changed;
- no production behavior or authority is added.

El corrected candidate requiere affected revalidation y un nuevo Candidate FULL 4R.

## 11. Candidate pre-review / Bounded Correction round 2

Se detectó un segundo finding de fidelidad contractual antes de independent review:

```text
HVC-A-PRB-F02
type        contract fidelity / optional field
design      claim_part_id? is optional and only present when upstream supplies it
problem     visible projection required the key even for root-claim cases
impact      representation was stricter than integrated G1
disposition BOUNDED_CORRECTION
```

Corrección:

- root-claim visible cases omit claim_part_id;
- projection accepts absence and normalizes it internally to None;
- upstream-authorized claim part remains explicit when present;
- unknown extra keys still fail closed;
- no new semantics, component, authority or dependency.

Any review/evidence bound to candidate d3b6309646d3c672f9818d9f63be37b59bdc4a67 is superseded.

## 12. Independent FULL 4R FAIL / Bounded Correction round 3

Independent issue #288 reviewed candidate:

```text
candidate       0eb173d9b5cb1ae83ff119cdf54afee9f1cd1c64
tree            89c3ddd67100ce3c36a870bd53909c5a74a4f2f6
Risk            FAIL
Readability     PASS
Reliability     FAIL
Resilience      FAIL
FULL_4R_RESULT  FAIL
```

Blocking finding:

```text
HVC-A-PRB-4R-R2-F03
type        provenance / binding
severity    HIGH
blocking    YES
problem     free caller-visible material can be substituted while inherited
            evidence/finding identities remain unchanged
```

Bounded Correction round 3 remains inside the existing PR-B file/component budget.

Selected correction:

```text
caller dict provenance              REJECT
existing focused evidence identity  REUSE + RECOMPUTE
existing finding fingerprint        REUSE + RECOMPUTE
selected evidence_ref               RESOLVE from exact focused bundle
claim                               DERIVE from exact structured finding
claim_part_id                       FAIL CLOSED until an authorized upstream
                                    provider exists
new evidence identity               NO
new component/service/manager       NO
```

`project_hvc_a_visible_semantic_observation_case_v0` no longer accepts a free
mapping. A bound case must first be derived from the existing
`GovernedEngineeringEvidenceFocus`, `FocusedEngineeringEvidenceBundle` and
structured `_Finding` surfaces. The existing focused evidence digest is
recomputed from the exact bundle/focus material before projection. The existing
finding fingerprint is recomputed from the exact finding material.

F03-specific validation covers:

- free visible dict rejected as provenance;
- changed claim cannot preserve finding fingerprint;
- changed evidence material with old evidence_set_digest rejected;
- coordinated changed evidence material requires a new evidence_set_digest;
- caller-invented claim_part_id rejected because no upstream authorized provider
  exists in this baseline;
- projected claim/material are derived from the bound upstream objects.

Ground Truth labels and visible semantic cases were not changed by this correction.

The corrected candidate requires full affected revalidation, fresh independent
FULL 4R, and a fresh blind Ground-Truth review bound to the new candidate.
