---
title: "Malāk — External Research Evidence Transfer for Governed Self-Review"
status: draft
authority: non_normative_research
baseline_commit: f638a2070ddd3b358bcc32f2827b2f3766497250
issue: 319
authority_effect: none
---

# External Evidence Transfer — Governed Self-Review

## Purpose and separation

This document records external research candidates for future evaluation, not proof that any technique works in Malāk. It is separate from #323 G0/G1 to avoid changing its predeclared hypotheses, cases, metrics or acceptance criteria. No runtime, model training, memory persistence or architecture changes are authorized.

## Baseline alignment

Malāk's Cognitive Constitution CC-010 requires controlled learning; its evidence/authority boundaries forbid promoting confidence, retrieval, consensus or model output to authority. AGENTS.md requires proportionality, source closure and REUSE→ADAPT→COMPOSE→NEW. The Blueprint anticipates episodic memory and governed learning but planned design is not proof of implementation. The Research Horizon already tracks governed self-improvement, evidence acquisition, procedural learning, memory trust and poisoning. E2/E3/E4 and the SelfReviewEvidencePacket provide a bounded read-only evaluation/proposal foundation.

## Evidence-transfer matrix

| Reference | Published mechanism / research claim | Existing Malāk overlap | Transfer decision | Missing Malāk evidence / admission |
| --- | --- | --- | --- | --- |
| Reflexion (Shinn et al., NeurIPS 2023) | Verbal reinforcement learning via feedback and episodic reflection | Controlled-learning principles; memory roadmap | OBSERVE → ADAPT | No measured local benefit or authorized persistent-learning path |
| Self-RAG (Asai et al., ICLR 2024) | Learned retrieval and critique decisions | Governed evidence focus; repository and knowledge readers | ADAPT evaluation only | Show material missed evidence or avoidable retrieval cost first; do not copy trained tokens |
| CRITIC (Gou et al., ICLR 2024) | Tool-interactive feedback for self-correction | E2/E3/E4 evidence and proposals, exact refs | REUSE + evaluation | Measure whether feedback improves grounded claims vs baseline; no new critic agent |
| Constitutional AI (Bai et al., 2022/2023) | Principle-guided model critique/revision and training | Cognitive/Governance Constitutions | RESEARCH | Model adherence is not external enforcement or authority |
| Deliberative Alignment (Guan et al., 2024/2025) | Training models to reason over policy specifications | Constitutional principles and future Cognitive Dataset concept | RESEARCH | Independent policy adherence and safety evaluation before training |
| Agent Lightning (Microsoft Research, 2025/2026) | Separate agent execution from training and use trajectories as learning data | Existing run traces/outcomes | OBSERVE | Training data validity, reward validity, authorization, rollback, costs |
| STATE-Bench (Microsoft Research, 2026) | Stateful agent/memory task evaluation and consistency | Existing artifacts, traces, test infrastructure | ADAPT evaluation methodology | Confirm benchmark scope, metrics and reproducibility; design Malāk-specific held-out tasks |
| SWE-bench Verified (OpenAI et al., 2024) | Real repository issue benchmark with test-grounded outcomes | Engineering inspect/analyze/propose | ADAPT task methodology | No equivalence between passing tests and correct governance |

## Priority and proposed gates

- G1 (#323): independently review predeclared TRUE_GAP / NO_CHANGE / AMBIGUOUS design. **No reference here may retroactively alter G1**.
- G2: Owner-authorized read-only pilot with existing E2/E3/E4; record all outcomes and counterevidence.
- G3: expand held-out evaluations informed by CRITIC and stateful-task benchmarks; compare to unchanged baseline and measure false support, unnecessary abstention, useful NO_CHANGE, cost and latency.
- G4: only after a demonstrated deficit, consider selective retrieval changes via REUSE→ADAPT.
- G5: only after memory trust, authorization, taint/revocation and persistence controls are proven, consider reversible episodic learning.
- G6: training/optimization research requires separate authorization and independent safety/effectiveness evaluation.

## Rejection boundaries

Do not introduce HVC, universal semantic verifiers, model self-authorization, swarm critics, extra memory databases, self-modifying weights, or a training framework without specific measured need. `paper result != Malāk result`; `research evidence != implementation authority`; `source availability != source consumption != evidence support`.

## Primary public references to verify when transferring

- Reflexion: https://arxiv.org/abs/2303.11366
- Self-RAG: https://arxiv.org/abs/2310.11511
- CRITIC: https://arxiv.org/abs/2305.11738
- Constitutional AI: https://arxiv.org/abs/2212.08073
- Deliberative Alignment: https://arxiv.org/abs/2412.16339
- Agent Lightning: https://arxiv.org/abs/2508.03680
- SWE-bench: https://www.swebench.com/
- STATE-Bench: https://opensource.microsoft.com/blog/2026/05/19/introducing-state-bench-a-benchmark-for-ai-agent-memory/ and https://github.com/microsoft/STATE-Bench ; **VERIFIED EXISTENCE AND DOCUMENTED PROTOCOL**, not independently reproduced. 450 tasks in travel, customer support and shopping; state assertions and Agent Learning Track. Its official evaluation uses a locked simulator/judge client (documented GPT-5.4), which introduces cost/dependency and prevents claiming zero-cost local replication. Transfer only evaluation concepts, not benchmark scores.

## Source verification and reproducibility limits (2026-10-14)

- CRITIC: ICLR 2024 primary proceedings https://proceedings.iclr.cc/paper_files/paper/2024/hash/fef126561bbf9d4467dbb8d27334b8fe-Abstract-Conference.html ; publication verified, no Malāk replication.
- Reflexion: NeurIPS 2023 proceedings https://proceedings.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html and implementation https://github.com/noahshinn/reflexion ; public code/logs verified, but GPT-4 cost/access caveat disclosed by authors.
- Self-RAG: authors' repository https://github.com/AkariAsai/self-rag ; public training/inference implementation verified, no claim that trained reflection tokens are portable to Malāk.
- STATE-Bench: Microsoft publication and official repo verified; 450 stateful enterprise tasks, Agent Learning Track; task domain and locked evaluation protocol differ materially from Malāk engineering self-review. **Benchmark suitability for Malāk remains UNTESTED**.
- All results above are source-verified at publication/documentation level only. Reproduction, statistical validity on Malāk tasks, implementation fit and performance remain UNTESTED.

## Current decision

Research-only. No code/tests/runtime modifications, no benchmark run, no model qualification, no production admission, no merge authority. Any further gate requires independent review, Owner decision and exact candidate evidence.

authority_effect=none.
