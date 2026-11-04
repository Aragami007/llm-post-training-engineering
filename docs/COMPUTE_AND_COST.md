# Compute feasibility, memory and cost gates

**Hardware:** NVIDIA RTX 4060 **8 GB VRAM** local; local drive ~120 GB NVMe + ~250 GB external SSD per course planning assumptions. Confirm all physical details in P00 inventory. Cloud L4/A100 are opportunistic and **not guaranteed** by Colab Pro.

## Ideal weight-only lower bounds (dense model, not training memory)

| Model | BF16 weights | Ideal 4-bit weights | Default training setting |
|---|---:|---:|---|
| 1B | 1.86 GiB | 0.47 GiB | Local LoRA/QLoRA, tiny full-tuning controls |
| 3B | 5.59 GiB | 1.40 GiB | Local QLoRA under sequence/batch limits |
| 8B | 14.90 GiB | 3.73 GiB | Local stretch QLoRA only after memory pilot |
| 14B | 26.08 GiB | 6.52 GiB | Cloud L4-class QLoRA conditional |
| 27B | 50.29 GiB | 12.57 GiB | Cloud A100-class **elective** feasibility pilot |

Theoretical bound `parameters × bytes per parameter` omits quantization scales, embeddings not quantized, gradients, optimizer states, activations, CUDA context, memory fragmentation, temporary tensors, KV cache, communication buffers, allocator reservation and checkpoint copies. Prefer GiB for precise accounting. LoRA/QLoRA feasibility varies with model architecture and kernel.

## Must-fill resource gate before each major run

Copy [resource gate template](../templates/resource_gate.md) and state:

1. Model repo/revision/license/tokenizer and dense vs MoE/multimodal architecture.
2. Theoretical and **measured** model weight footprint, estimated adapter/activation/optimizer/temporary memory.
3. Actual GPU(s), supported precision and kernels, current free memory, expected max sequence length and microbatch.
4. Dataset hash, training token count, optimizer steps, planned tokens/sec, wall-time and spend cap.
5. Checkpoint frequency/retention/resume plan, required free SSD, and fallback if Colab disconnects.
6. Clear go/no-go threshold, e.g., memory pilot at representative sequence length and a 10–20% headroom target where feasible.

For 27B, record exact model card; a particular 27B variant may be vision-capable and not the text-only architecture assumed by smaller labs. DPO often needs policy and reference behavior; its memory budget is not interchangeable with QLoRA SFT.

## Resource priority

1. Small correctness test locally.
2. Controlled 1–3B experiment locally or modest cloud.
3. Quality/latency/VRAM measurement.
4. Optional cloud scale with budget and rollback.
5. Optional actual multi-GPU system experiment.

Never infer a runtime, availability or cost from paid Colab subscription alone. Avoid storing secrets or large checkpoints in Git. Only publish metadata, small sanitized examples and reproducible scripts.
