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
