---
title: Malāk E3 Assessor Reason Semantics V0.1 — U07 Bounded Correction
status: candidate
authority: non-normative
date: 2026-10-11
authority_effect: none
---

# Malāk E3 Assessor Reason Semantics V0.1 — U07 Bounded Correction

## Purpose

This record documents a bounded correction to the E3 governed local Ollama assessor prompt after repaired-corpus qualification evidence showed a general ambiguity in reason-code semantics.

The original V0 design and prior live runs remain historical evidence and are not rewritten.

## Evidence trigger

The admitted `gemma4:12b` run on the repaired corpus:

- crossed the runtime and `thinking_enabled=false` boundary successfully;
- satisfied the complete safety floor;
- preserved binding-drift detection and equivalent-input stability;
- failed exact qualification only on reason-code classification/pairing cases;
- emitted one `OUTCOME_REASON_CONTRACT_INVALID` safe diagnostic.

The current V0 prompt enumerates allowed reason codes but does not define their semantics or required outcome pairing.

## Bounded correction

The prompt now defines generic semantics for every model-owned reason code:

```text
MATERIAL_SUPPORT_CONFIRMED              -> SUPPORTED
SUPPORTING_REFS_IRRELEVANT             -> INSUFFICIENT
SUPPORTING_REFS_INSUFFICIENT           -> INSUFFICIENT
COMPOUND_CLAIM_NOT_FULLY_SUPPORTED     -> INCONCLUSIVE
MATERIAL_COUNTEREVIDENCE_UNRESOLVED    -> INCONCLUSIVE
ASSESSMENT_SCOPE_EXCEEDED              -> INCONCLUSIVE
```

Specific compound, counterevidence and scope conditions take precedence over the generic `SUPPORTING_REFS_INSUFFICIENT` reason.

This is taxonomy clarification, not case-answer injection. No case IDs, expected outcomes, expected reason codes, hidden truth or corpus-specific text is added to the model prompt.

## Frozen surfaces

No change is authorized to:

- repaired case set or Ground-Truth Review B;
- response JSON schema;
- qualification runner or thresholds;
- safety floor;
- RuntimeGenerationContract;
- context/output token budgets;
- retry/fallback policy;
- provenance checks;
- deterministic-envelope ownership;
- model promotion;
- U08 continuity wiring;
- Kernel, Planner, Capability or persistence authority.

## Candidate identity

```text
prompt_template_digest =
6fb7fe90ee0113be0d91fc02b77bbabdd8eabd08903067249c8675de3d3e6a92

example:model config_digest =
8165a7bc50236fa2d4d6ea3ad01d416f1771e7a894c05df3b67aed6064fcf3d7
```

The mechanism remains `e3-blind-assessor-ollama-local / v0`; its candidate-bound config digest changes because the prompt bundle changed.

## Gate discipline

The correction requires:

```text
RED -> exact prompt contract fails against V0
GREEN -> full repository validation
Owner review
Owner merge only
post-merge rebaseline
new exact live model qualification
```

No prior FAIL is reinterpreted. A future PASS, if any, must come from a new post-merge run bound to the new prompt digest.

U08 remains blocked until G-01 produces valid PASS evidence.
