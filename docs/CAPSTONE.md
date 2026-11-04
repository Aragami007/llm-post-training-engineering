# Capstone: falsifiable B0/B1/B2/B3 comparison

## Question

For one tightly bounded text task, under a fixed budget and fixed held-out evaluation, **when does post-training measurably outperform strong prompting/constrained decoding (and RAG where relevant), and at what quality, safety, compute and serving cost?**

Recommended task: structured tool selection and schema-valid argument generation with refusal/abstention on unsupported or unsafe requests. Alternatives: unit-tested code transformation or verifiable arithmetic. Do not switch task after inspecting held-out scores without declaring a new experiment.

## Four methods

- **B0:** frozen prompted instruct-model baseline; record prompt search and constraints.
- **B1:** task SFT adapter with data audit and at least one ablation.
- **B2:** B1 plus preference optimization; report DPO implicit margin **separately** from external task quality.
- **B3:** separate small online RL with deterministic reward; report reward hacking and failures, including if it underperforms.

## Essential deliverables

| Area | Commit evidence |
|---|---|
| Task and benchmarks | `eval/eval_spec.md`, frozen checksums, `eval.py`, baseline report, per-item results |
| Dataset | `models_and_datasets/dataset_card.md`, generation provenance, privacy/license checks, data audit |
| Models | model/base revision and cards, adapters (or storage pointers), training scripts and config hashes |
| Scientific method | exact token budgets, run IDs, seeds, controlled ablations, error analysis and uncertainty |
| Preference/RL | preference rubric and audit, scratch DPO, B2 evaluation, small online RL experiment and verifier |
| Engineering | memory profiler report, checkpoints/resume, API smoke test, serving latency and cost |
| Communication | `REPORT.md` (6–10 pages), 5-minute technical walkthrough, reproducibility checklist |

## Research report outline

1. Task and falsifiable hypotheses.
2. Prior methods, evidence hierarchy and selected model lineage.
3. Data provenance, leakage prevention and evaluation design.
4. B0 baseline and B1/B2/B3 experimental controls.
5. Main results with per-slice and uncertainty metrics.
6. Failure analysis, unintended proxy optimization, adversarial tests and negative results.
7. Systems cost (VRAM, tokens/sec, GPU hours, storage and inference latency).
8. Limitations, environmental reproducibility and next experiments.

**Graduation:** reproducible evidence and defensible conclusions, *not* a requirement that each advanced method beats its predecessor. Optional 27B/multi-GPU experiments may be explicitly marked deferred.
