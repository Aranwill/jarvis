---
title: Malak E3 Ground-Truth Discriminability V0.3 — U07 Bounded Correction
status: candidate
authority: non-normative
date: 2026-10-12
authority_effect: none
---

# Malak E3 Ground-Truth Discriminability V0.3 — U07 Bounded Correction

## Trigger

Independent blind review #274 returned `FAIL_AMBIGUOUS`.

The visible V0.1 contract could not uniquely discriminate the rationale-overclaim and compound-partial packets, and its scope reason overlapped ordinary insufficient support.

## Bounded correction

### C09 — RATIONALE_OVERCLAIM

The visible statement is narrowed to:

```text
Kernel owns durable persistence authority.
```

The rationale still performs the unsupported inference from orchestration to durable persistence authority.

Expected disposition remains unchanged:

```text
INSUFFICIENT / SUPPORTING_REFS_INSUFFICIENT
```

### Scope semantics

`ASSESSMENT_SCOPE_EXCEEDED` now requires the packet to explicitly identify a named evidence dependency outside the bounded packet or stated scope.

Ordinary relevant-but-insufficient support remains `SUPPORTING_REFS_INSUFFICIENT`.

C18 already materializes the strict scope condition with production deployment logs / telemetry outside the packet.

## Hidden-label prohibition

Synthetic evaluation `uncertainty_basis` values are not used as oracle labels or deterministic discriminators.

## Candidate identities

```text
case_set_digest         4ec4d152af884b50d7bfa8c9d14eaaabb93b6e306ea5e7bd0361b326bb053bba
prompt_template_digest  8a5916bba52f7c71a0e0bc0ca854f95a7e74fd222b5354d1a9b60142b7aa98dd
example_config_digest   70bef63de4997ea4f95453e1aa0bc05235a638770d83bd86488ebe7fccc2973e
```

## Frozen surfaces

No change to expected outcomes/reason labels, qualification thresholds, safety floor, RuntimeGenerationContract, retry/fallback, response schema, Kernel, Planner, Capability, persistence or authority.

## Required next gate

Full CI PASS is followed by a new independent Ground-Truth Review over the exact candidate case-set digest before Owner merge or any new live U06 qualification.
