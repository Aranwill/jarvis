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
prompt_template_digest  d33b9d310e50d475c17e935ae7bcdd55cbdf123c6e3663a0d4050b47b2edd4b4
example_config_digest   51272bab0b799a16d28fbaad1f3f69dfd04eb5b2f853203ae4534455bec85524
```

## Digest verification

The prompt/config digest calculation was cross-checked against the previously integrated V0.1 prompt digest before binding this candidate. Candidate identity uses exact repository canonical JSON and raw case-set bytes.

## Frozen surfaces

No change to expected outcomes/reason labels, qualification thresholds, safety floor, RuntimeGenerationContract, retry/fallback, response schema, Kernel, Planner, Capability, persistence or authority.

## Required next gate

Full CI PASS is followed by a new independent Ground-Truth Review over the exact candidate case-set digest before Owner merge or any new live U06 qualification.

## Ground-Truth Review C and V0.4 relevance amendment

Independent Ground-Truth Review C (#276) returned `FAIL_AMBIGUOUS` only for the boundary between irrelevant and relevant-but-insufficient supporting references.

The visible contract is therefore clarified generically:

```text
SUPPORTING_REFS_IRRELEVANT:
use only when none of the supplied supporting references materially bear on the statement or its evidentiary sufficiency.

SUPPORTING_REFS_INSUFFICIENT:
use when at least one supplied supporting reference materially bears on the statement, including by directly describing a limitation or non-establishment, but the packet does not establish it.
```

If any supplied supporting reference materially bears on the statement, `SUPPORTING_REFS_IRRELEVANT` is forbidden. More specific compound/counterevidence/scope rules retain precedence.

This amendment changes no case-set bytes or expected labels.

V0.4 prompt identities:

```text
case_set_digest         4ec4d152af884b50d7bfa8c9d14eaaabb93b6e306ea5e7bd0361b326bb053bba
prompt_template_digest  5af5cc933925031c5e84ce4bca00cdc4df872f91fa710a7b8f97ae8ce7c3bff5
example_config_digest   94ab5a6b1bb6dd60097f2233834617daca0963a2443eec26e11387cc50b678c9
```

