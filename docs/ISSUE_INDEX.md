# Issue index — complete learning tracker

**133 issues** across 12 phases. Local links preview each complete GitHub issue body. Published issues will appear in the repository’s **Issues** tab.

## Phase 00 — Environment and reproducibility (Week 1)

**Phase gate:** `P00-09` · **Learning objective:** Reproducible local environment, baseline training smoke test and verified resume.

- [P00-01 — Map the post-training lifecycle](../tracker/issues/P00-01.md) — concept
- [P00-02 — Establish Linux/Python/Git development environment](../tracker/issues/P00-02.md) — lab
- [P00-03 — Inventory RTX 4060 and storage](../tracker/issues/P00-03.md) — lab
- [P00-04 — Check model cards, dataset cards and licenses](../tracker/issues/P00-04.md) — concept
- [P00-05 — Build versioned experiment configuration](../tracker/issues/P00-05.md) — lab
- [P00-06 — Characterize deterministic vs nondeterministic execution](../tracker/issues/P00-06.md) — experiment
- [P00-07 — Run a tiny inference and backward pass](../tracker/issues/P00-07.md) — lab
- [P00-08 — Implement save-resume smoke test](../tracker/issues/P00-08.md) — lab
- [P00-09 — Phase 0 reproducibility review](../tracker/issues/P00-09.md) — gate

## Phase 01 — Transformers, optimization and GPU primitives (Weeks 2–3)

**Phase gate:** `P01-12` · **Learning objective:** Correct mini decoder, measured precision and attention behavior.

- [P01-01 — Causal language-model objective and teacher forcing](../tracker/issues/P01-01.md) — concept
- [P01-02 — Token embeddings, output heads and tokenization](../tracker/issues/P01-02.md) — concept
- [P01-03 — Positional representations and RoPE](../tracker/issues/P01-03.md) — concept
- [P01-04 — Implement masked scaled dot-product attention](../tracker/issues/P01-04.md) — lab
- [P01-05 — Multi-head attention, GQA and KV heads](../tracker/issues/P01-05.md) — concept
- [P01-06 — Residuals, LayerNorm/RMSNorm and MLP blocks](../tracker/issues/P01-06.md) — concept
- [P01-07 — Code a minimal decoder-only transformer](../tracker/issues/P01-07.md) — lab
- [P01-08 — AdamW, schedulers and optimizer state](../tracker/issues/P01-08.md) — concept
- [P01-09 — Gradient accumulation, clipping and true batch size](../tracker/issues/P01-09.md) — lab
- [P01-10 — FP32, FP16, BF16 and numerical stability](../tracker/issues/P01-10.md) — experiment
- [P01-11 — Fused SDPA, FlashAttention and sequence scaling](../tracker/issues/P01-11.md) — experiment
- [P01-12 — Phase 1 correctness and derivation gate](../tracker/issues/P01-12.md) — gate

## Phase 02 — LoRA, QLoRA and memory accounting (Weeks 4–5)

**Phase gate:** `P02-11` · **Learning objective:** Correct scratch LoRA and measured GPU budgets.

- [P02-01 — LoRA low-rank update derivation](../tracker/issues/P02-01.md) — concept
- [P02-02 — Build LoRA for nn.Linear from scratch](../tracker/issues/P02-02.md) — lab
- [P02-03 — Test LoRA gradients, save/load and merge](../tracker/issues/P02-03.md) — lab
- [P02-04 — Compare LoRA module coverage and rank/alpha](../tracker/issues/P02-04.md) — concept
- [P02-05 — Weight quantization and NF4](../tracker/issues/P02-05.md) — concept
- [P02-06 — QLoRA optimizer and backward memory path](../tracker/issues/P02-06.md) — concept
- [P02-07 — Implement truthful CUDA memory probe](../tracker/issues/P02-07.md) — lab
- [P02-08 — Sweep batch, context, checkpointing and precision](../tracker/issues/P02-08.md) — experiment
- [P02-09 — LoRA vs QLoRA comparison on 1–3B](../tracker/issues/P02-09.md) — experiment
- [P02-10 — Stretch: 7–8B short-context QLoRA pilot](../tracker/issues/P02-10.md) — stretch *(optional)*
- [P02-11 — Phase 2 adapter and memory gate](../tracker/issues/P02-11.md) — gate

## Phase 03 — Task framing and evaluation before tuning (Weeks 6–7)

**Phase gate:** `P03-12` · **Learning objective:** Frozen evaluator and baseline B0 with trustworthy metrics.

- [P03-01 — Choose prompting, RAG, CPT, SFT or RL](../tracker/issues/P03-01.md) — concept
- [P03-02 — Specify one bounded course evaluation task](../tracker/issues/P03-02.md) — lab
- [P03-03 — Construct a task failure taxonomy](../tracker/issues/P03-03.md) — concept
- [P03-04 — Build independent train/dev/test partitions](../tracker/issues/P03-04.md) — lab
- [P03-05 — Audit exact/semantic data leakage](../tracker/issues/P03-05.md) — experiment
- [P03-06 — Implement deterministic task grading](../tracker/issues/P03-06.md) — lab
- [P03-07 — Design an unbiased pairwise judge rubric](../tracker/issues/P03-07.md) — concept
- [P03-08 — Calibrate judge scores against humans](../tracker/issues/P03-08.md) — experiment
- [P03-09 — Paired experiment design and uncertainty](../tracker/issues/P03-09.md) — concept
- [P03-10 — Add selected general-regression and safety tests](../tracker/issues/P03-10.md) — lab
- [P03-11 — Run and document B0 prompt-only baseline](../tracker/issues/P03-11.md) — experiment
- [P03-12 — Phase 3 freeze-before-training gate](../tracker/issues/P03-12.md) — gate

## Phase 04 — Dataset creation and curation (Weeks 8–9)

**Phase gate:** `P04-12` · **Learning objective:** Audited supervised dataset with provenance and no leakage.

- [P04-01 — Understand dataset schemas and conversations](../tracker/issues/P04-01.md) — concept
- [P04-02 — Apply the selected model's native chat template](../tracker/issues/P04-02.md) — lab
- [P04-03 — Prove assistant-only and completion-only masks](../tracker/issues/P04-03.md) — lab
- [P04-04 — Validate packing, boundaries and truncation](../tracker/issues/P04-04.md) — experiment
- [P04-05 — Establish data provenance and usage permissions](../tracker/issues/P04-05.md) — concept
- [P04-06 — Redact privacy-sensitive data](../tracker/issues/P04-06.md) — lab
- [P04-07 — Curate first 300–500 verified examples](../tracker/issues/P04-07.md) — lab
- [P04-08 — Synthesize controlled additional training data](../tracker/issues/P04-08.md) — experiment
- [P04-09 — Deduplicate exact and semantic near duplicates](../tracker/issues/P04-09.md) — lab
- [P04-10 — Filter, reject-sample and audit data quality](../tracker/issues/P04-10.md) — experiment
- [P04-11 — Build dataset card and token coverage report](../tracker/issues/P04-11.md) — concept
- [P04-12 — Phase 4 dataset admission gate](../tracker/issues/P04-12.md) — gate

## Phase 05 — Supervised fine-tuning and ablations (Weeks 10–12)

**Phase gate:** `P05-11` · **Learning objective:** Reproducible B1 with fair ablation comparisons.

- [P05-01 — Derive masked SFT objective and training budgets](../tracker/issues/P05-01.md) — concept
- [P05-02 — Train a transparent small SFT reference model](../tracker/issues/P05-02.md) — lab
- [P05-03 — Train QLoRA/LoRA 1–3B B1 candidate](../tracker/issues/P05-03.md) — lab
- [P05-04 — Compare attention-only versus all-linear LoRA](../tracker/issues/P05-04.md) — experiment
- [P05-05 — Compare LoRA rank and alpha configurations](../tracker/issues/P05-05.md) — experiment
- [P05-06 — Test learning rate and schedule sensitivity](../tracker/issues/P05-06.md) — experiment
- [P05-07 — Data quantity and synthetic-mixture ablation](../tracker/issues/P05-07.md) — experiment
- [P05-08 — Interpret overfitting versus forgetting](../tracker/issues/P05-08.md) — concept
- [P05-09 — Capture checkpoints and resumable training](../tracker/issues/P05-09.md) — lab
- [P05-10 — Optional cloud scaling to 7–14B/27B](../tracker/issues/P05-10.md) — stretch *(optional)*
- [P05-11 — Phase 5 B1 acceptance and ablation gate](../tracker/issues/P05-11.md) — gate

## Phase 06 — Training diagnostics and interpretation (Weeks 13–14)

**Phase gate:** `P06-10` · **Learning objective:** Fault injections and measured root-cause investigations.

- [P06-01 — Interpret loss/perplexity and masking denominators](../tracker/issues/P06-01.md) — concept
- [P06-02 — Induce and diagnose overfitting safely](../tracker/issues/P06-02.md) — experiment
- [P06-03 — Create and resolve gradient instability](../tracker/issues/P06-03.md) — experiment
- [P06-04 — Diagnose vanishing gradients and underfitting](../tracker/issues/P06-04.md) — concept
- [P06-05 — Compare several random seeds](../tracker/issues/P06-05.md) — experiment
- [P06-06 — Monitor tokens/sec and GPU/CPU bottlenecks](../tracker/issues/P06-06.md) — lab
- [P06-07 — Test checkpoint and resume failure paths](../tracker/issues/P06-07.md) — lab
- [P06-08 — Build training configuration and data-integrity tests](../tracker/issues/P06-08.md) — lab
- [P06-09 — Explain one unexpected metric with a controlled test](../tracker/issues/P06-09.md) — experiment
- [P06-10 — Phase 6 diagnostics gate](../tracker/issues/P06-10.md) — gate

## Phase 07 — Reward modeling and offline preferences (Weeks 15–17)

**Phase gate:** `P07-13` · **Learning objective:** Scratch DPO, preference-quality audit and independent B2 evaluation.

- [P07-01 — Understand RLHF and preference pipeline](../tracker/issues/P07-01.md) — concept
- [P07-02 — Design preference rubric and candidate sampling](../tracker/issues/P07-02.md) — lab
- [P07-03 — Audit annotator disagreement and preference noise](../tracker/issues/P07-03.md) — experiment
- [P07-04 — Derive Bradley–Terry reward preference model](../tracker/issues/P07-04.md) — concept
- [P07-05 — Train/evaluate a tiny reward model](../tracker/issues/P07-05.md) — lab
- [P07-06 — Derive DPO from KL-regularized preference objective](../tracker/issues/P07-06.md) — concept
- [P07-07 — Implement chosen/rejected sequence log probabilities](../tracker/issues/P07-07.md) — lab
- [P07-08 — Implement DPO loss from scratch](../tracker/issues/P07-08.md) — lab
- [P07-09 — Analyze beta and reference-policy choice](../tracker/issues/P07-09.md) — concept
- [P07-10 — Run TRL DPO to create B2](../tracker/issues/P07-10.md) — experiment
- [P07-11 — Detect length bias and self-evaluation failure](../tracker/issues/P07-11.md) — experiment
- [P07-12 — Compare IPO, ORPO, SimPO and DPO tradeoffs](../tracker/issues/P07-12.md) — concept
- [P07-13 — Phase 7 independent B2 evaluation gate](../tracker/issues/P07-13.md) — gate

## Phase 08 — Online RL and verifiable rewards (Weeks 18–20)

**Phase gate:** `P08-12` · **Learning objective:** Small B3 RL experiment and reward-hacking control.

- [P08-01 — Formulate post-training as sequential policy optimization](../tracker/issues/P08-01.md) — concept
- [P08-02 — Implement REINFORCE on tiny verifiable task](../tracker/issues/P08-02.md) — lab
- [P08-03 — Understand value baselines, advantages and KL](../tracker/issues/P08-03.md) — concept
- [P08-04 — Compare PPO, GRPO and RLOO](../tracker/issues/P08-04.md) — concept
- [P08-05 — Build verifiable reward oracle](../tracker/issues/P08-05.md) — lab
- [P08-06 — Model rollout generation and off-policy mismatch](../tracker/issues/P08-06.md) — concept
- [P08-07 — Implement tiny GRPO-style group-relative objective](../tracker/issues/P08-07.md) — lab
- [P08-08 — Train a small B3 with deterministic verifier](../tracker/issues/P08-08.md) — experiment
- [P08-09 — Analyze reward hacking and mitigation](../tracker/issues/P08-09.md) — experiment
- [P08-10 — Evaluate B3 vs B1/B2 independently](../tracker/issues/P08-10.md) — experiment
- [P08-11 — Model online RL resource economics](../tracker/issues/P08-11.md) — concept
- [P08-12 — Phase 8 online RL competency gate](../tracker/issues/P08-12.md) — gate

## Phase 09 — Distributed training systems (Weeks 21–22)

**Phase gate:** `P09-11` · **Learning objective:** Correct collectives/sharding model with honest hardware claims.

- [P09-01 — Quantify GPU communication collectives](../tracker/issues/P09-01.md) — concept
- [P09-02 — Implement 2-rank CPU Gloo all-reduce demo](../tracker/issues/P09-02.md) — lab
- [P09-03 — Derive DDP and gradient accumulation behavior](../tracker/issues/P09-03.md) — concept
- [P09-04 — Map tensor, pipeline and sequence/context parallelism](../tracker/issues/P09-04.md) — concept
- [P09-05 — Derive ZeRO stages without fixed multipliers](../tracker/issues/P09-05.md) — concept
- [P09-06 — Understand FSDP2 and DTensor](../tracker/issues/P09-06.md) — concept
- [P09-07 — Write valid DDP/FSDP/DeepSpeed configurations](../tracker/issues/P09-07.md) — lab
- [P09-08 — Checkpointing and recovery in sharded systems](../tracker/issues/P09-08.md) — concept
- [P09-09 — CPU/NVMe offload and performance limitations](../tracker/issues/P09-09.md) — concept
- [P09-10 — Optional real 2+ GPU comparison](../tracker/issues/P09-10.md) — stretch *(optional)*
- [P09-11 — Phase 9 systems comprehension gate](../tracker/issues/P09-11.md) — gate

## Phase 10 — Serving, artifact engineering and observability (Week 23)

**Phase gate:** `P10-10` · **Learning objective:** Working inference API and quantified serving tradeoffs.

- [P10-01 — Understand adapter-only vs merged model artifacts](../tracker/issues/P10-01.md) — concept
- [P10-02 — Merge LoRA and check numerical equivalence](../tracker/issues/P10-02.md) — lab
- [P10-03 — Compare GGUF, AWQ, GPTQ and runtime compatibility](../tracker/issues/P10-03.md) — concept
- [P10-04 — Measure post-training quantization regression](../tracker/issues/P10-04.md) — experiment
- [P10-05 — Calculate KV cache with GQA and context](../tracker/issues/P10-05.md) — concept
- [P10-06 — Explain continuous batching and paged attention](../tracker/issues/P10-06.md) — concept
- [P10-07 — Deploy an OpenAI-compatible inference endpoint](../tracker/issues/P10-07.md) — lab
- [P10-08 — Benchmark TTFT, TPOT, throughput and concurrency](../tracker/issues/P10-08.md) — experiment
- [P10-09 — Secure LoRA adapters and serving management](../tracker/issues/P10-09.md) — concept
- [P10-10 — Phase 10 serving acceptance gate](../tracker/issues/P10-10.md) — gate

## Phase 11 — Capstone and research portfolio (Week 24)

**Phase gate:** `P11-10` · **Learning objective:** Reproducible B0–B3 comparative system and research report.

- [P11-01 — Finalize capstone hypothesis and success criteria](../tracker/issues/P11-01.md) — concept
- [P11-02 — Curate final model/data/license cards](../tracker/issues/P11-02.md) — lab
- [P11-03 — Reproduce B0 prompted baseline from clean state](../tracker/issues/P11-03.md) — experiment
- [P11-04 — Reproduce B1 SFT and matched ablations](../tracker/issues/P11-04.md) — experiment
- [P11-05 — Reproduce B2 offline preference alignment](../tracker/issues/P11-05.md) — experiment
- [P11-06 — Reproduce B3 bounded online RL branch](../tracker/issues/P11-06.md) — experiment
- [P11-07 — Consolidate independent evaluation and uncertainty](../tracker/issues/P11-07.md) — experiment
- [P11-08 — Package inference interface and artifact integrity](../tracker/issues/P11-08.md) — lab
- [P11-09 — Write research-style final technical report](../tracker/issues/P11-09.md) — concept
- [P11-10 — Final portfolio review and retrospective](../tracker/issues/P11-10.md) — gate

