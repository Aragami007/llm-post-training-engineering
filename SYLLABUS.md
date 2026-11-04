# LLM Post-Training Engineering — From First Principles to Research-Grade Practice

**Revised syllabus v2.0 | 5 November 2026**  
**Career direction:** LLM Post-Training / Fine-Tuning / Alignment Engineer; preparation for research-engineering and scalable training-systems work  
**Core duration:** 24 weeks, approximately 12–18 focused hours/week (adjust to prior experience)  
**Hardware:** Local NVIDIA RTX 4060 8 GB; opportunistic Google Colab Pro, with GPU availability **not guaranteed**; rent a specific GPU or multi-GPU instance only for experiments that need one.  
**Scope:** Text LLMs first; multimodal post-training and large-scale clusters as extension tracks.  
**Expectation:** Completion provides evidence of substantial practical competence, **not** a guarantee of mastery or a hyperscaler role. Depth follows from repeated projects, debugging, and research replication.

---

## A. Training philosophy

1. **Establish a falsifiable baseline before training.** Compare prompting/RAG/structured decoding against fine-tuning; do not fine-tune merely because it is available.
2. **Implement a small version from scratch, then use production libraries.** Understand derivatives and tensors; use PyTorch, Transformers, PEFT, TRL, and vLLM pragmatically.
3. **Separate independent concepts:** supervised fine-tuning (SFT), continued pretraining (CPT/DAPT), offline preference optimization (DPO/IPO/ORPO), learned reward models, and online RL (PPO/GRPO/RLOO).
4. **Treat datasets and evaluation as products.** Preserve provenance, labels, licenses, leakage checks, and versioned evaluation sets. Do not let the same LLM generator exclusively judge its own examples.
5. **Learn hardware through measurements.** Record theoretical parameter footprints, estimated allocations, measured allocated/reserved memory, total device usage, peak memory, throughput, and wall-clock cost.
6. **Prefer conclusive small experiments over unconstrained large-model attempts.** A reproducible 1–3B experiment with a causal explanation is more educational than one unverified 27B run.
7. **Use experiments to advance:** each phase has an artifact, a baseline, a test, and a short written engineering analysis.

### Required entry knowledge

Python, command line/Linux, Git, environments, NumPy, core PyTorch, differentiation and chain rule, matrices, probability/log probabilities, cross-entropy, gradient descent. If missing, allocate 2–4 additional foundation weeks before Week 1.

### Core evaluation project, selected by Week 6

Choose one narrow **measurable** domain for the entire course. Recommended: structured technical-support/tool-calling assistant that must choose a valid tool, produce schema-conforming arguments, and refrain from unsupported claims. Alternative: code-transformation assistant evaluated by unit tests; arithmetic / math assistant with verifiable final answers. Keep datasets and evaluation separate. Build four checkpoints:

- **B0 — Prompted baseline:** an off-the-shelf instruct model using carefully designed prompting and, where relevant, RAG or constrained decoding.
- **B1 — SFT model:** supervised adapter, tested against B0 with unchanged evaluation prompts.
- **B2 — Preference model:** B1 further trained with DPO or a comparable offline preference objective.
- **B3 — Online RL model (small):** a separate experimental branch trained on verifiable rewards, compared to B1/B2. B3 need not beat B2; explain why if it does not.

Also retain a **B-1 — untuned/base checkpoint** where useful for understanding pretrained vs instruction-tuned behavior. Do not treat an instruct model and its underlying base model as interchangeable.

---

## B. Hardware feasibility and budgeting

The table is a **weight-only theoretical lower bound** for dense models, excluding extra unquantized tensors, quantization metadata, LoRA parameters, activations, optimizer state, fragmentation, CUDA context, KV cache, and temporary tensors. Use **GiB**, not decimal GB, for memory planning.

| Parameter count | BF16 weight-only | Ideal 4-bit weight-only | Sensible first experiment |
|---|---:|---:|---|
| 1B | 1.86 GiB | 0.47 GiB | LoRA/QLoRA on RTX 4060; full tuning requires a much smaller model |
| 3B | 5.59 GiB | 1.40 GiB | RTX 4060 QLoRA with modest context |
| 8B | 14.90 GiB | 3.73 GiB | RTX 4060 **stretch** QLoRA, tight limits; better on L4/A100 |
| 14B | 26.08 GiB | 6.52 GiB | L4 24 GB QLoRA, subject to sequence and model architecture |
| 27B | 50.29 GiB | 12.57 GiB | A100 40/80 GB **stretch** QLoRA; require feasibility pilot |

**Important:** 27B model variants differ; Qwen3.6-27B is a vision-capable, post-trained architecture, not a generic text-only base. Verify model card, license, architecture, tokenizer, and supported kernels before selecting it. A 27B DPO run can require substantially more than a 27B QLoRA SFT run. Colab Pro does **not** guarantee L4 or A100 availability, uninterrupted execution, or a particular runtime lifetime. Preserve resumable checkpoints and maintain a smaller-model fallback.

**Storage:** 120 GB internal NVMe is restrictive when maintaining original weights, quantized models, optimizer/checkpoint snapshots, datasets and logs. Prefer larger fast SSD where available; store only selected checkpoints; avoid relying on slow external storage for heavy offload. Document download sizes and costs **before** running.

**Resource gates:** Before each training experiment, write a memory budget, sequence-length/batch assumptions, tokens-to-train estimate, estimated runtime/cost, dataset checksum, checkpoint plan, and an OOM fallback.

---

## Phase 0 — Environment, baseline ML engineering (Week 1)

**Knowledge:** CUDA toolkit/driver compatibility, `nvidia-smi`, PyTorch CUDA availability, pinned library versions, Python virtual environments, Git, configuration files, deterministic seeds and remaining nondeterminism, experiment metadata, licensing and model card inspection.

**Deliverables:**
- `environment.md` with versions, available GPUs and memory, `torch.cuda.is_bf16_supported()` result, and storage information.
- Reproducible training template: config, requirements/lockfile, data checksums, logging, checkpoint/save/resume test, README.
- Run one tiny model inference and a few gradient steps on synthetic data; commit executable results.

**Gate:** Another person can reproduce the same model, data revision, command and metric calculation.

## Phase 1 — Transformers, optimization and GPU primitives (Weeks 2–3)

**Theory:** causal language modeling; embeddings; positional encoding and RoPE; masked self-attention; multi-head attention and GQA; MLP; RMSNorm/LayerNorm; residual paths; pretraining vs post-training. Cross-entropy and teacher forcing, log likelihood, gradient accumulation, AdamW moments/weight decay, schedulers, clipping, regularization, precision.

**Hands-on:**
1. Implement a mini decoder-only transformer and causal cross-entropy training loop in PyTorch. Validate tensor shapes and gradient paths.
2. Write scaled dot-product attention and compare against PyTorch SDPA / fused attention as supported by the actual hardware. Understand the difference between **O(N²) compute** and the reduction of attention-intermediate memory through tiling; FlashAttention does not make total transformer memory O(N).
3. Compare FP32, FP16, BF16 (exponent vs mantissa, over/underflow risk, dynamic loss scaling where relevant) using a controlled test. Full-parameter training on the local 8 GB GPU should use a very small model (e.g., tens to a few hundreds of millions of parameters) unless memory-reduction techniques change the budget.

**Gate:** Explain every tensor shape and show a small correct backward pass; document numerical differences.

## Phase 2 — LoRA, quantization and real GPU accounting (Weeks 4–5)

**Theory:** frozen base vs trainable adapters; LoRA as `W = W0 + (alpha/r)BA`; shapes and gradients; zero-update initialization; intrinsic low-rank intuition as an empirical hypothesis; target modules; rank, alpha and dropout; rsLoRA/DoRA as optional extensions; quantization error; NF4, double quantization, QLoRA; optimizer state and activation tradeoffs; gradient checkpointing; fused attention; paged optimizers for spikes, not free memory.

**Hands-on:**
1. Implement LoRA on `nn.Linear` without PEFT; verify forward equivalence at initialization, trainability, adapter save/load, finite-difference gradient sanity checks.
2. Compute **actual** trainable-parameter reduction for each architecture/configuration (never assume 99.6% universally).
3. Build a memory experiment that records theory, `memory_allocated`, `memory_reserved`, peak allocated, full-device `nvidia-smi` usage and throughput for a controlled sweep of batch size, sequence length, checkpointing and precision.
4. On a 1–3B model, benchmark LoRA vs QLoRA with equal tokens/batch size. Optionally attempt 7–8B at short context after a successful memory pilot.

**Gate:** Explain peak-memory discrepancies and produce a working adapter with a unit test.

## Phase 3 — Problem framing, baseline design and evaluation **before tuning** (Weeks 6–7)

**Theory:** when to use prompting, RAG, tool use, constrained decoding, CPT/domain-adaptive pretraining, SFT and preference optimization; distinguish factual knowledge retrieval from behavior adaptation. Measurement validity, evaluation splits, contamination, calibration, rubric design, paired evaluation, confidence intervals, regression slices, judge biases and human calibration.

**Hands-on:**
1. Define task specification, failure taxonomy, baseline model, prompt protocol, sampling settings, acceptable actions, unsafe/unsupported behaviors, and cost limits.
2. Create a **frozen** unseen test set (suggest 150–300 diverse examples where feasible; quality matters more than count). Create separate dev/validation sets and a separate train pool. Deduplicate across splits by meaning as well as exact strings.
3. Build a deterministic evaluator (schema pass, unit tests, numerical answers) plus a rubric-based blind paired judge. Randomize ordering and calibrate a sample against independent human labels.
4. Record baseline success/error rate and slice-level failure analysis. Add a small general-capability regression suite where relevant; academic benchmarks alone are insufficient.

**Gate:** Publish `eval_spec.md`, `baseline_report.md`, versioned test set and runnable `eval.py` **before** generating fine-tuning data.

## Phase 4 — Dataset creation and scientific data curation (Weeks 8–9)

**Theory:** instruction vs completion vs conversational datasets; tokenizer-specific `apply_chat_template`, BOS/EOS/EOT and role turns; assistant-only/completion-only labels and `-100`; masking tests; packed sequence boundaries and cross-example attention; truncation; near duplicates, semantic leakage and distribution coverage; dataset licensing, PII removal, provenance and teacher-generation usage rights.

**Hands-on:**
1. Construct a high-quality training corpus (2,500 examples is **an optional scale target**, not a quality requirement). Start from 300–500 verified examples; extend only after quality review.
2. Generate synthetic data in controlled strata; record prompt, seed, generator/model/version, provenance, quality criteria and reason for acceptance/rejection. Include explicit abstention and failure cases.
3. Create tests proving exactly which tokens are supervised. Compare `assistant_only_loss` vs `completion_only_loss` where appropriate, using a compatible chat template.
4. Demonstrate packing with no unintended training on other conversations and no silent truncation of necessary answer tokens; test packed vs unpacked results.
5. Write a dataset card and a coverage table by domain, difficulty, length and error class.

**Gate:** `data_audit.json` includes leakage, dedup, token statistics, provenance and 100 manually audited random items.

## Phase 5 — SFT experiments and ablations (Weeks 10–12)

**Theory:** SFT objective, learning-rate schedules, microbatch vs effective batch, total tokens vs number of epochs, adapter capacity, regularization, early stopping, overfitting, scaling behaviors, full fine-tuning vs adapter fine-tuning, QLoRA pitfalls, catastrophic forgetting vs task tradeoffs.

**Hands-on:**
1. Train a 0.5–1.5B instruct model end to end with transparent PyTorch/Transformers; optionally full fine-tune a sufficiently small model as a control.
2. Train a 1–3B LoRA/QLoRA model on the same task; compare all-linear vs attention-only targets, at least two ranks and two learning rates. Keep data, evaluated tokens, inference and metric protocol fixed.
3. Conduct an **ablation study**: e.g. 500 vs 2,000 examples; real-only vs mixed synthetic; LoRA vs QLoRA; vary **one main factor at a time**.
4. Use a 7–14B model as a cloud-scale extension **only after** a small-model experiment is reproducible. Treat 27B as an elective, not a completion requirement.

**Gate:** B1 beats at least one clearly defined B0 metric on a held-out test without unacceptable regression in selected safety or general capability checks; if not, the failure diagnosis itself is documented.

## Phase 6 — Debugging, optimization and rigorous interpretation (Weeks 13–14)

**Theory:** train/validation loss, masked-token denominators, perplexity limitations, optimizer-state dynamics, gradient norm, exploding and vanishing gradients, learning-rate instability, sequence-length pathologies, label leakage, template misalignment, evaluation-induced false positives, reproducibility across seeds.

**Hands-on:**
1. Deliberately create overfitting and a numerically unstable training run with a **tiny** model, then fix them. Include before/after run logs.
2. Run three seeds for a **small** experiment where feasible; show confidence intervals/variation, not only the best run.
3. Instrument tokens/sec, peak allocated/reserved GPU memory, data throughput, checkpoint overhead and approximate run cost.
4. Add unit tests for model loading, expected trainable parameters, tokenizer-template compatibility, completion masks and resumed training.

**Gate:** Deliver `training_diagnostics.md` with causes supported by measurements, not loss-curve storytelling alone.

## Phase 7 — Human/AI preferences, reward models and offline alignment (Weeks 15–17)

**Theory:** RLHF pipeline (SFT, human comparisons, reward model, policy optimization), Bradley–Terry preference modeling, reward-model calibration, inter-annotator disagreement, on-policy vs off-policy preference distributions, DPO derivation and implicit rewards, choice of reference policy, beta/regularization, length bias; ORPO, IPO and SimPO as comparisons; distinction between an optimization proxy and actual real-world helpfulness/truthfulness.

**Hands-on:**
1. Build independent `{prompt, chosen, rejected}` pairs with rubric, grader source, difficulty and confidence; audit preference consistency and cases where both candidates are bad.
2. Implement DPO loss **from sequence log-probabilities** on a tiny toy model. Check gradient direction and numerical agreement with a library implementation.
3. Optionally fit a tiny reward model, measure held-out preference accuracy and inspect biases. This is a core conceptual competence even if full PPO is not run.
4. Apply TRL DPO (or a comparable method) to B1. Compare B1 vs B2 blind win rate, format accuracy, response length, chosen/rejected margins, regression rate and robustness on independent held-out prompts.
5. Demonstrate how biased pair labels or repeated self-judging can give improved training margins while worsening external evaluation.

**Gate:** `preference_eval.md` reports **both optimization telemetry and independent outcome metrics**.

## Phase 8 — Online reinforcement learning and reasoning adaptation (Weeks 18–20)

**Theory:** Markov/policy-gradient intuition, REINFORCE, baseline/advantage, likelihood ratios, clipping, reference-policy KL, reward shaping, reward models vs verifiable rewards, PPO vs GRPO/RLOO, group-relative standardization, zero-variance groups, reward hacking, response-length bias, training/inference rollout mismatch, generated-token budgets and systems cost.

**Hands-on:**
1. Implement a policy-gradient or GRPO-style objective on a tiny synthetic task where reward is fully verifiable.
2. Train a 0.5–1.5B model (or smaller if necessary) on a math/code/structured-output task with a deterministic verifier; use TRL GRPO when compatible with available resources, with a transparent fallback training loop.
3. Compare B3 vs B1/B2 on held-out tasks; report reward curve **and** actual final-answer/task success, length, diversity, failure cases, KL and compute cost.
4. Perform a reward-hacking demonstration safely in a controlled sandbox; modify the reward to resist the exploit and rerun a small experiment.

**Gate:** Explain why online rollouts change data distribution; demonstrate a case in which optimizing a reward metric is **not** the same as improving held-out task performance.

## Phase 9 — Distributed training and production training systems (Weeks 21–22)

**Theory:** data vs tensor vs pipeline vs sequence/context parallelism; collective operations and communication cost; gradient accumulation vs synchronization; DDP; FSDP2/DTensor; ZeRO 1/2/3; parameter/optimizer/gradient sharding; CPU/NVMe offload; model checkpoints, failure recovery, throughput and cost. Learn memory savings as functions of sharded state sizes and **GPU count**; do **not** memorize fixed 4× / 8× savings.

**Hands-on:**
1. Build a 2-rank CPU process-group demo using Gloo for all-reduce and a toy sharding experiment; verify aggregation numerically. Understand this is **not evidence of multi-GPU performance**.
2. Write and explain Accelerate/DDP/FSDP2/DeepSpeed configurations. Inspect parameter/device partitions, collectives and checkpoints.
3. **Conditional lab:** rent two or more GPUs briefly and run a measured DDP vs FSDP/ZeRO experiment. If unavailable, label configurations and simulations as conceptual; do not claim an executed sharded GPU experiment.

**Gate:** Produce a memory and communication cost model and a working demo with clearly stated hardware limitations.

## Phase 10 — Model artifact engineering, serving and observability (Week 23)

**Theory:** adapter-only vs merged artifacts; dequantize–merge–requantize and approximation error; GGUF, AWQ, GPTQ, etc. as **distinct** formats/workflows rather than interchangeable exports; KV cache and GQA; continuous batching, paged KV management, prefix caching, quantization accuracy tradeoffs; requests/sec, output tokens/sec, TTFT, TPOT, p50/p95 latency; basic production security and model-card/license compliance.

**Hands-on:**
1. Compare adapter-loaded vs merged model quality on the frozen task set. Record quantization-induced changes.
2. Deploy a realistically sized local model (ideally 1–3B on 8 GB) behind an OpenAI-compatible interface with vLLM **if the model/hardware/quantization format is supported**; otherwise use an alternative locally and run a separate cloud vLLM lab.
3. Benchmark concurrency, context length, GPU usage and TTFT/latency. Include at least one serving failure mode, checkpoint rollback and a simple access-control plan.
4. Explore multi-LoRA serving on cloud if memory permits; **never** expose administrative dynamic-LoRA-loading endpoints to untrusted users.

**Gate:** `serving_report.md` compares throughput/cost/quality for two serving configurations and shows an actual API smoke test.

## Phase 11 — Capstone and research-style write-up (Week 24; prepared from Week 6)

**Project:** A measurable, end-to-end post-training system for a bounded task.

**Required final artifacts:**
1. `README.md`: problem, target metric, environment, reproducible command sequence.
2. `model_and_dataset_cards/`: origins, license, consent/provenance, limitations and risks.
3. `data_pipeline/`: cleansing, split leakage checks, label masks, preference-data audit.
4. `train/`: scratch LoRA, SFT and DPO code; optional verifiable-reward GRPO branch.
5. `eval/`: frozen data, deterministic grader, judge rubric, human calibration samples, regression suite.
6. `experiments/`: config/seed ledger; baseline and ablations; charts with uncertainty; GPU and financial cost.
7. `serve/`: adapter artifact, inference API, load/latency smoke tests.
8. `REPORT.md` (6–10 pages): hypotheses; design; controlled comparisons; statistical uncertainty; negative results; limitations; lessons; research next steps.

**Minimal success criterion:** Reproducible technical demonstration and an evidence-backed analysis of what improved and what did not. A published win without baselines, leakage checks, and comparable evaluations **does not pass**.

---

## C. Mandatory experiment scorecard

Maintain this table for **every significant run**:

| Category | Log |
|---|---|
| Identity | Run ID, date, Git commit, model ID/revision, tokenizer, adapter ID |
| Data | Dataset version/hash, provenance, train/dev/test sizes, effective training tokens, packing/masking |
| Training | Method, rank/alpha/targets, precision/quantization, LR/schedule, warmup, optimizer, seed, steps, effective batch, sequence length |
| Systems | GPU, peak allocated/reserved/device VRAM, tokens/sec, wall clock, checkpoints, cost |
| Evaluation | Prompt/template, decoding, number of items, B0/B1/B2/B3 with paired comparisons, confidence interval where practical |
| Safety/quality | Unfounded assertions, abstention, unsafe outputs, invalid actions, general-regression slices, human error analysis |
| Interpretation | Hypothesis, outcome, alternative explanation, next experiment |

Suggested experiment discipline: run an unmodified baseline; change a single factor; hold test data and decoding constant; run more than one seed for consequential conclusions; report failures. Use loss/perplexity as diagnostic signals, not stand-ins for domain competence.

---

## D. Required reading and reference ladder

Read each method's original paper for assumptions and failure modes; cross-check against **version-pinned** implementation docs:

1. Transformer fundamentals — *Attention Is All You Need* (2017), plus a hands-on minimal decoder implementation.
2. LoRA — Hu et al., *LoRA: Low-Rank Adaptation of Large Language Models* (2021), https://arxiv.org/abs/2106.09685
3. FlashAttention — Dao et al., *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness* (2022), https://arxiv.org/abs/2205.14135
4. QLoRA — Dettmers et al. (2023), https://arxiv.org/abs/2305.14314
5. DPO — Rafailov et al. (2023), https://arxiv.org/abs/2305.18290
6. GRPO — DeepSeekMath (2024) plus current TRL GRPO documentation (implementation variants matter), https://huggingface.co/docs/trl/grpo_trainer
7. Tokenization/templates — https://huggingface.co/docs/transformers/chat_templating
8. Training/assistant-only masks/packing — https://huggingface.co/docs/trl/sft_trainer
9. Quantized adapters — https://huggingface.co/docs/peft/developer_guides/quantization
10. Offline preference methods — https://huggingface.co/docs/trl/dpo_trainer
11. Reward model training — https://huggingface.co/docs/trl/reward_trainer
12. General benchmarks/custom eval — https://github.com/EleutherAI/lm-evaluation-harness
13. Memory accounting — https://docs.pytorch.org/docs/stable/generated/torch.cuda.memory.memory_stats.html
14. ZeRO — https://www.deepspeed.ai/tutorials/zero/ and FSDP2 — https://docs.pytorch.org/docs/stable/distributed.fsdp.fully_shard.html
15. Production inference / LoRA / performance — https://docs.vllm.ai/en/stable/features/lora/ and https://docs.vllm.ai/en/latest/usage/metrics/
16. Colab constraints — https://research.google.com/colaboratory/faq.html

*Optional specialization after Week 24*: (a) large-scale training infrastructure and CUDA/Triton kernel profiling; (b) advanced online RL and reward-model training; (c) multimodal/VLM post-training; (d) continued pretraining and domain-adaptive training; (e) tooling/agent trajectories and multi-turn reinforcement learning. Choose a track and reproduce two recent papers with controls before claiming research-level depth.

---

## E. Explicit corrections applied to the original draft

- Removed the promise of predicting VRAM **exactly to the megabyte**: measure allocator stats and non-PyTorch overhead instead.
- Clarified BF16's **exponent range versus precision**, rather than saying BF16 eliminates numerical issues.
- Clarified AdamW's 8 bytes per trainable parameter cover **two FP32 moments only**, not total training state.
- Clarified FlashAttention's memory property and unchanged quadratic attention arithmetic.
- Made LoRA parameter savings and rank/alpha/LR settings **measured and task-dependent**, not universal.
- Replaced forced ChatML/ShareGPT normalization with **model-native chat templates** and supervised-token-mask tests.
- Moved evaluation **ahead of** synthetic data and SFT, reducing leakage and post-hoc metric selection.
- Distinguished continual-domain-pretraining, behavior SFT, preference optimization and online RL.
- Added provenance, human calibration, dataset cards, preference-label quality, and safe data use.
- Corrected DPO framing (closed-form reward–policy relationship and tractable preference loss; **not** a closed-form gradient-update rule).
- Expanded reward modeling, policy gradients and GRPO into testable experiments.
- Corrected ZeRO ratios: savings depend on sharding degree and state composition, requiring **multiple** data-parallel ranks.
- Replaced mandatory 27B L4/Colab training with a feasible local-first ladder and conditional cloud stretch.
- Qualified 4-bit adapter merging: dequantize/add/requantize may be supported but introduces quantization error.
- Added post-deployment latency, quantization regression, reproducibility, security, and costs.

**Design principle:** Strong engineers do not just know how to run a method; they can select it, derive its objective, implement its key part, measure resource use, establish a fair comparison, debug a failed run, and communicate whether the result is trustworthy.
