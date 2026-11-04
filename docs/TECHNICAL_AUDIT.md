# Technical Audit of the Original 12-Week LLM Fine-Tuning Syllabus

**Reviewed:** 5 November 2026  
**Source:** `hyperscaler_llm_fine_tuning_syllabus.md` (153 lines)  
**Classification:** High = may distort understanding or block execution; Medium = oversimplification or missing important qualification; Low = editorial / hygiene.

## Executive verdict

**Keep the structure's core ideas. Redesign sequencing and correct hardware and methodology claims.** The original is a strong technical *outline* but is not a sufficiently validated plan for full post-training engineering competence. The biggest gaps are (1) evaluation after training, (2) little reward modeling or executed online RL, (3) over-confident hardware claims, (4) fixed or incorrect memory/LoRA/ZeRO statements, and (5) too few controlled experiments. A 24-week core programme is recommended, with further study for research-grade or hyperscaler-level specialist skills.

## Finding register

| ID | Priority | Original location | Finding | Recommended change |
|---|---|---|---|---|
| F01 | High | Outcomes, line 13 | Predicting **exact** VRAM down to MB is not generally possible as a prior guarantee; allocator, temporary workspaces, other GPU processes, context overhead and backend decisions vary. | Predict lower bounds/ranges and **measure** peak allocated, reserved and system-used VRAM. |
| F02 | High | 1.1, line 26 | BF16 does not universally prevent underflow/overflow; it offers wider exponent range but fewer mantissa bits than FP16. | Teach range, precision, numerical stability, FP16 scaling and error cases. |
| F03 | High | 1.1, line 30 | AdamW's 8 bytes/parameter refers to two FP32 moments, not the total trained-parameter footprint; paged optimizers reduce peak spikes rather than making optimizer memory disappear. | Account separately for weights, trainable gradients, optimizer moments, possible master copies, activations and allocator overhead. |
| F04 | Medium | 1.2, line 35 | Saying FlashAttention achieves `O(N)` memory is incomplete; this is about **attention-intermediate** auxiliary storage, not total training memory or attention compute complexity. | Distinguish `O(N²)` attention FLOPs from IO-aware tiling and memory savings, with measured benchmark. |
| F05 | Medium | Lab 1, line 46 | The 99.6% trainable parameter reduction is configuration-specific. A checked box can be valid if actually finished but not as a universal target. | Compute ratio from actual `requires_grad` count; record model, target modules, rank. |
| F06 | High | Phase 2, lines 52, 73 | Training 8B on RTX 4060 8GB may fit only with 4-bit QLoRA, short sequences, tiny microbatches and memory optimizations, and can still OOM. | Make 1–3B the reliable local core; 7–8B a conditional stretch. |
| F07 | High | Phase 2, lines 52, 73; capstone line 153 | Treating 27B training on Colab Pro L4 or A100 as guaranteed is untenable; availability varies, model weight type matters, and DPO can be heavier than SFT. | Require a pilot memory budget; prefer A100 40/80 for larger QLoRA, 27B as optional. Do not assume Colab GPU type. |
| F08 | High | 2.1, line 57 | Forcing ChatML/ShareGPT can corrupt model-specific control tokens (including turn endings, tools and reasoning templates). | Store structured role messages and use the model's tokenizer's `apply_chat_template` and tests. |
| F09 | Medium | 2.1, line 58 | Assistant-only labels are common and important for instruction SFT, but not the only valid causal LM training objective; it also depends on proper template masks. | Compare assistant-only, completion-only and full-sequence learning; test masked token positions explicitly. |
| F10 | High | 2.2, line 61 | Teacher-generated data is not necessarily accurate, legally reusable or aligned with task goals. A single teacher grading its own synthetic answers causes circular evaluation. | Add provenance, licensing/usage checks, human calibration, quality gates and independent ground truth. |
| F11 | Medium | 2.2 + Lab 2, line 72 | 2,500 examples is arbitrary: quantity may inflate low-quality and near-duplicate data. | Start with 300–500 verified items, then scale; track quality/diversity and held-out gains per additional data. |
| F12 | High | 2.2, line 63 | Packing sequences with EOS alone does not always prevent attention crossing sample boundaries; token supervision, sequence slicing and truncation can be incorrect. | Test attention/label boundaries and effective packing behaviour of the chosen trainer; compare packed/unpacked. |
| F13 | Medium | 2.3, line 66 | All-linear LoRA often helps but is not proven to outperform attention-only targets for every domain, model and budget. | Treat it as a hypothesis; run controlled all-linear vs attention-only experiments. |
| F14 | Medium | 2.3, lines 67–68 | Fixed alpha-to-rank ratios and LR ranges are useful starting heuristics, not laws. Higher LoRA LR is not always optimal. | Tune rank, alpha, LR and dropout conditionally; control for data/steps and look at rsLoRA as extension. |
| F15 | High | Phase ordering, lines 51–99 | Evaluation is introduced after running SFT; this risks leakage, post-hoc metric selection and no baseline. | **Move task specification + frozen evaluation set before data generation and training.** |
| F16 | High | 3.2, line 89 | MMLU/GSM8K/HumanEval are neither universal task metrics nor complete tests for catastrophic forgetting; they are costly and can be contaminated. | Use task-specific test sets, selected general regression slices and balanced human/judge assessment. |
| F17 | Medium | 3.1, line 82 | `PPL=exp(loss)` only has an interpretable comparison when the loss is mean token cross-entropy with compatible tokenization/masking/normalization. | Document denominator and masking; avoid comparing perplexities from incompatible setups. |
| F18 | Medium | 3.1, lines 84–86 | Overfitting/underfitting and gradient norm are presented as single-cause diagnostics, when root causes can be data, optimizer, masking, schedule or measurement. | Include controlled fault-injection, failure taxonomy, tracing and hypotheses. |
| F19 | High | 4.1, line 104 | PPO-based RLHF does **not** necessarily keep four fully separate models in GPU memory simultaneously. Typical conceptual components are policy, reference, reward and value/critic (often a head), subject to sharding/offload. | Teach the conceptual architecture separately from actual memory layout; add small reward-model training lab. |
| F20 | High | 4.1, line 105 | DPO is not a universal closed-form **weight-update** algorithm; it derives a relationship between reward and KL-regularized optimal policy and optimizes a tractable logistic preference loss with gradient descent. | Re-derive the DPO loss and implement it from chosen/rejected sequence log-probabilities. |
| F21 | Medium | 4.1, line 107 | `beta` described simply as a KL penalty obscures its role as a temperature/regularization parameter in the DPO derivation and library implementation. | Relate beta to reference deviation and log-ratio scale, and inspect varying beta empirically. |
| F22 | High | 4.1, lines 107, 115 | Chosen/rejected reward margins are **implicit proxy telemetry**, not proof the model is more truthful, safer or useful. | Add external blind win-rate, length bias, task pass rate, refusal quality and safety regressions. |
| F23 | Medium | 4.2, line 110 | ORPO phrasing as a monolithic training step is imprecise; it combines supervised and odds-ratio preference terms without a separate reference model. | Explain the objective and when ORPO/IPO/SimPO may be preferable to DPO. |
| F24 | High | 4.2, line 111 | GRPO is only a reading topic; modern online RL competence requires rollout, verifier/reward, advantages, policy updates and failure investigations. | Add a real **small-model verifiable-reward online RL lab**, with reward hacking and held-out comparison. |
| F25 | High | Phase 5, lines 129–131 | ZeRO-1 ‘4×’ and ZeRO-2 ‘8×’ are not fixed universal memory reductions. Sharding savings vary with number of data-parallel ranks, model state composition, batch and communication buffers. | Use explicit state-size formulae and a scaling sweep across rank counts. |
| F26 | High | Phase 5, line 135 | Single-GPU Colab cannot prove multi-GPU sharding benefits. Multi-process on one GPU does not create extra aggregate VRAM. | Use CPU distributed process-group correctness lab; rent 2+ actual GPUs for optional DDP/FSDP experiment. |
| F27 | Medium | 6.1, line 144 | ‘Never merge directly into quantized weights’ is too absolute. Some PEFT quantized merge routes dequantize/add/requantize; roundoff differences are important. | Preserve original adapter, measure post-merge quality and use validated supported paths. |
| F28 | Medium | 6.1, line 145 | GGUF, AWQ and EXL2 are different quantization formats/techniques/runtime ecosystems, not interchangeable one-click export targets. | Teach per-format workflow, calibration, serving compatibility and accuracy/throughput trade-offs; optionally add GPTQ. |
| F29 | High | 6.2 + capstone, lines 147–153 | High-throughput vLLM and multi-LoRA on local 8GB 7/8B assume headroom that may not exist once KV cache and concurrency are counted. | Use 1–3B local serving as core; benchmark cloud for larger deployment; record context/concurrency/TTFT/TPOT. |
| F30 | Medium | 6.2, line 150 | Runtime hot-loading of arbitrary LoRA adapters can introduce a security risk. | Restrict admin adapter-management endpoints to trusted networks and processes. |
| F31 | High | Entire syllabus | No explicit data leakage, privacy, licensing, human label quality, model/dataset cards or problem-framing gate. | Add responsible data-engineering deliverables and distinguish fine-tuning from RAG/prompting. |
| F32 | High | Entire syllabus | Little scientific experiment design: no frozen comparison protocol, ablation matrix, repeated seeds, uncertainty or negative-results report. | Make controlled comparisons and reproducible reports mandatory in every phase. |
| F33 | High | Entire syllabus | ‘Complete expertise’ within 12 weeks is not a defensible competency target, especially for distributed training + online RL + production systems. | Expand to 24-week technical foundation with chosen specialty and continued replication/research thereafter. |
| F34 | Medium | Capstone, line 153 | ‘Raw open-weight model’ confuses an untuned checkpoint with an instruction-tuned open-weights model. | Explicitly specify base vs instruct vs post-trained checkpoint and model lineage. |
| F35 | Medium | Hardware intro, line 4 | 120 GB internal NVMe can be quickly consumed by multiple model revisions, optimizer checkpoints and large-model downloads; external SSD offload may have bandwidth limits. | Add storage budget, resumable cloud training and checkpoint retention policy. |

## Priority fix order

1. **First:** Freeze evaluation and choose a measurable target task (F15, F16, F31, F32).
2. **Next:** Revise hardware plan and model-size ladder (F06, F07, F26, F29, F35).
3. **Then:** Correct mathematical statements and add first-principles labs (F01–F05, F19–F25).
4. **Finally:** Extend data/reward/online RL and build a genuine experimental capstone (F08–F14, F22–F24, F33).

## What is already strong — preserve it

- The focus on GPU memory and attention primitives rather than only high-level APIs.
- LoRA/QLoRA mathematics and adapter merging.
- Synthetic data generation, deduplication, rejection sampling and packing as **techniques**.
- Loss/gradient debugging, deterministic evaluation and LLM-as-judge awareness.
- DPO formula and interest in GRPO/ORPO.
- Distributed-systems fundamentals and the attempt to connect training to serving.
- A working end-to-end capstone rather than only quizzes.

## Suggested five non-negotiable portfolio proofs

1. **Scratch LoRA + gradient test:** demonstrate theoretical shape math and a correct trained adapter.
2. **Memory budgeting notebook:** predict bounds; measure CUDA allocated/reserved and device VRAM; explain error margins.
3. **Frozen evaluator and controlled SFT ablation:** report baseline, experiment variants, paired outcomes, failure slices and leakage audit.
4. **DPO from scratch and one actual online RL experiment:** report independent improvements/failures, reward hacking and stability.
5. **Deployed artifact:** reproducible API, quantization/merging regression, latency and resource measurements, model/dataset cards.

## Grounding sources (current official docs and original papers)

- Google Colab resource caveats: https://research.google.com/colaboratory/faq.html
- Hugging Face SFT/packing/assistant-only masking: https://huggingface.co/docs/trl/sft_trainer
- Model-native chat templates: https://huggingface.co/docs/transformers/chat_templating
- PEFT quantization and adapter merge caveats: https://huggingface.co/docs/peft/developer_guides/quantization
- DPO trainer and beta/variants: https://huggingface.co/docs/trl/dpo_trainer
- GRPO trainer: https://huggingface.co/docs/trl/grpo_trainer
- Reward trainer: https://huggingface.co/docs/trl/reward_trainer
- QLoRA paper: https://arxiv.org/abs/2305.14314
- DPO paper: https://arxiv.org/abs/2305.18290
- DeepSpeed ZeRO: https://www.deepspeed.ai/tutorials/zero/
- PyTorch FSDP2: https://docs.pytorch.org/docs/stable/distributed.fsdp.fully_shard.html
- CUDA memory stats: https://docs.pytorch.org/docs/stable/generated/torch.cuda.memory.memory_stats.html
- vLLM multi-LoRA security: https://docs.vllm.ai/en/stable/features/lora/
- Qwen3.6-27B model card: https://huggingface.co/Qwen/Qwen3.6-27B

**Important:** These findings are a document-and-documentation audit. No actual training execution, VRAM measurement, or model quality test was performed for the user's environment. All practical feasibility statements must be confirmed by a pilot on the target GPU and pinned software stack.
