# Hyperscaler LLM Fine-Tuning & Post-Training Engineering
**Target Role:** Post-Training / Alignment / Fine-Tuning Engineer  
**Compute Architecture:** 
* **Local Bare-Metal Sandbox:** Ubuntu 26.04 LTS | NVIDIA RTX 4060 (8GB VRAM) | 120GB NVMe + 250GB External SSD
* **Cloud Compute Cluster:** Google Colab Pro (NVIDIA L4 24GB & A100 40GB/80GB)

---

## Course Philosophy & Learning Outcomes
Hyperscalers do not hire engineers who merely execute high-level library wrappers; they hire engineers who understand the **CUDA memory hierarchy**, **mathematical weight adaptations**, **automated data curation**, and **preference alignment dynamics**. 

By completing this syllabus, you will be able to:
1. **Calculate and Profile:** Predict exact VRAM consumption down to the megabyte across weights, gradients, optimizer states, and activations.
2. **Data Engineer:** Build automated synthetic data generation and rejection-sampling pipelines.
3. **Train & Align:** Execute Supervised Fine-Tuning (SFT) and Direct Preference Optimization (DPO) on models up to 27B+ parameters (e.g., Qwen, Llama).
4. **Evaluate Rigorously:** Construct deterministic and LLM-as-a-Judge evaluation harnesses to prove capability gains and diagnose overfitting or catastrophic forgetting.
5. **Optimize & Serve:** Quantize, merge, and deploy custom adapters into high-throughput production inference engines.

---

## Phase 1: Bare-Metal Primitives & The CUDA Memory Hierarchy (Weeks 1–2)
**Primary Compute:** Local RTX 4060 (8GB VRAM)  
**Objective:** Strip away Hugging Face abstractions. Understand the physical hardware limits, floating-point representations, and the raw PyTorch math behind Parameter-Efficient Fine-Tuning (PEFT).

### 1.1 The Anatomy of GPU Memory (VRAM)
* **Floating-Point Representations:** FP32 vs. FP16 vs. BF16 (Dynamic range vs. precision; why BF16 prevents underflow/overflow during gradient updates).
* **The Four VRAM Buckets:**
  * **Parameters (Weights):** Calculating static footprint ($\text{Params} \times \text{Bytes}$).
  * **Gradients:** Storage requirements during `loss.backward()`.
  * **Optimizer States:** Why standard `AdamW` requires $8\text{ bytes}$ per parameter (32-bit first and second moments: $m_t$ and $v_t$) and how 8-bit Paged Optimizers solve this.
  * **Activations:** How sequence length ($N$) and batch size ($B$) scale memory dynamically during the forward pass, and how **Gradient Checkpointing** trades compute for memory.

### 1.2 Attention & Complexity Mechanics
* **Scaled Dot-Product Attention:** Implementing $\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$ in raw PyTorch.
* **The $O(N^2)$ Memory Bottleneck:** Understanding why materializing the $N \times N$ attention matrix crashes VRAM on long contexts, and how **FlashAttention** uses GPU SRAM tiling to achieve $O(N)$ memory complexity.

### 1.3 Low-Rank Adaptation (LoRA) from First Principles
* **Intrinsic Rank Hypothesis:** Why weight updates during adaptation have a low "intrinsic rank."
* **The LoRA Formulation:** 
  $$h = W_0 x + \Delta W x = W_0 x + \frac{\alpha}{r} B A x$$
  Where $W_0 \in \mathbb{R}^{d \times k}$, $B \in \mathbb{R}^{d \times r}$, $A \in \mathbb{R}^{r \times k}$, and $r \ll \min(d, k)$.
* **Initialization Mechanics:** Why $A$ is initialized with Kaiming uniform/Gaussian noise and $B$ is initialized to $0$ ($\Delta W = 0$ at step $0$).
* **QLoRA & 4-Bit NormalFloat (NF4):** Quantization block sizes, double quantization, and dequantizing frozen base weights to BF16 on-the-fly during matrix multiplication.

* **Phase 1 Deliverables (Lab 1):**
  * [x] Write `lora_scratch.py` in pure PyTorch and verify the $99.6\%$ reduction in trainable parameters.
  * [ ] Write a PyTorch CUDA memory profiler script that logs exact VRAM allocation at every step of a forward and backward pass on your RTX 4060.

---

## Phase 2: Data Engineering & Supervised Fine-Tuning (Weeks 3–5)
**Primary Compute:** Local RTX 4060 (Data Prep & 3B–8B Testing) + Colab Pro L4 (14B–27B Training)  
**Objective:** Master the modern truth of AI: *Data is the code.* Transform raw domain knowledge into token-packed instruction datasets and execute stable SFT runs.

### 2.1 Tokenization & Chat Templates
* **Subword Tokenization (BPE):** Understanding token IDs, vocabulary matrices (`embed_tokens` and `lm_head`), and special tokens (`<|im_start|>`, `<|im_end|>`, `<|eot_id|>`).
* **Template Standardization:** Converting raw data into **ChatML** and **ShareGPT** formats.
* **Label Masking (Crucial):** Configuring the Cross-Entropy Loss function so that loss is calculated *only* on the assistant's completion tokens (setting user prompt token labels to `-100`), preventing the model from learning to mimic user prompts.

### 2.2 Synthetic Data Generation & Curation Pipelines
* **Teacher-Student Distillation:** Using frontier models to synthesize complex instruction-response pairs tailored to your target domain.
* **Data Filtering & Rejection Sampling:** Deduplication (MinHash), heuristic length filtering, and automated quality scoring.
* **Sequence Packing:** Concatenating multiple short training examples into a single context window separated by EOS tokens to eliminate padding waste and maximize GPU compute utilization.

### 2.3 Hyperparameter Dynamics & SFT Execution
* **LoRA Target Modules:** Why targeting all linear layers (`q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`) outperforms targeting only attention matrices.
* **The Rank ($r$) vs. Alpha ($\alpha$) Tradeoff:** Selecting $r \in \{8, 16, 32, 64, 128\}$ based on task complexity (formatting vs. domain knowledge injection) and maintaining the $\alpha = 2r$ or $\alpha = r$ scaling ratio.
* **Learning Rate Schedules:** Warmup ratios, Cosine Annealing vs. WSD (Warmup-Stable-Decay), and why LoRA requires a higher learning rate ($\sim 1\text{e-}4$ to $2\text{e-}4$) than full fine-tuning ($\sim 1\text{e-}5$).
* **Effective Batch Size:** Balancing `per_device_train_batch_size` and `gradient_accumulation_steps`.

* **Phase 2 Deliverables (Lab 2):**
  * [ ] Build an automated Python pipeline that generates, cleans, and formats 2,500 domain-specific instruction pairs into a ChatML `.jsonl` dataset.
  * [ ] Fine-tune an 8B model locally on your RTX 4060 using Unsloth, followed by scaling the exact pipeline to a **27B model** on a Colab Pro L4/A100 GPU.

---

## Phase 3: Diagnostics, Metrics & Evaluation Harnesses (Weeks 6–7)
**Primary Compute:** Hybrid (Local RTX 4060 + Colab Pro)  
**Objective:** Learn to read telemetry like a senior researcher. Prove mathematically that your fine-tuned model outperforms the base model without suffering from catastrophic forgetting.

### 3.1 Reading Telemetry (Weights & Biases)
* **Loss Curves:** Interpreting Cross-Entropy Loss, Perplexity ($\text{PPL} = e^{\text{Loss}}$), and token-level accuracy.
* **Diagnosing Pathologies:**
  * **Overfitting:** Training loss plummets while validation loss forms a U-shape and climbs.
  * **Underfitting:** Loss plateaus high; diagnosing insufficient rank or overly conservative learning rates.
  * **Gradient Explosions:** Reading `grad_norm` spikes and configuring gradient clipping (`max_grad_norm`).

### 3.2 Post-Training Evaluation Frameworks
* **General Capability Regressions (Catastrophic Forgetting):** Running **LM-Evaluation-Harness** on standard benchmarks (MMLU, GSM8K, HumanEval) before and after SFT to ensure domain tuning didn't lobotomize general reasoning.
* **Deterministic Task Eval:** Exact-match, JSON schema validation, and execution-based grading (for code/CAD scripts).
* **LLM-as-a-Judge:** Building pairwise comparison pipelines with rubric grading and mitigating positional bias (swapping response A and B order).

* **Phase 3 Deliverables (Lab 3):**
  * [ ] Deliberately induce overfitting and gradient explosion on a small model on your RTX 4060 to capture diagnostic telemetry in Weights & Biases.
  * [ ] Build an automated evaluation suite that benchmarks your Phase 2 model against its base model across both domain accuracy and formatting compliance.

---

## Phase 4: Preference Alignment & Post-Training (Weeks 8–9)
**Primary Compute:** Colab Pro (A100 40GB)  
**Objective:** SFT teaches a model *how* to speak; alignment teaches it *what* to prefer. Master the post-training algorithms used to eliminate hallucinations, enforce constraints, and boost reasoning.

### 4.1 From RLHF to Direct Preference Optimization (DPO)
* **The RLHF Bottleneck:** Why training a separate Reward Model and running PPO (Proximal Policy Optimization) requires 4 models in VRAM simultaneously.
* **The DPO Mathematical Breakthrough:** Deriving the closed-form policy update that uses the LLM itself as an implicit reward model:
  $$\mathcal{L}_{\text{DPO}}(\pi_\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x, y_w, y_l)}\left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)} \right) \right]$$
* **Key DPO Telemetry:** Tracking **Rewards/Chosen**, **Rewards/Rejected**, **Rewards/Margins**, and tuning the $\beta$ (KL-divergence penalty) parameter.

### 4.2 Advanced Alignment Variants
* **ORPO (Odds Ratio Preference Optimization):** Combining SFT and preference alignment into a single monolithic training step without a reference model.
* **GRPO (Group Relative Policy Optimization):** Understanding how modern reasoning models use verifiable rewards and group-normalized baselines to learn chain-of-thought reasoning.

* **Phase 4 Deliverables (Lab 4):**
  * [ ] Construct a preference dataset of `{prompt, chosen, rejected}` triplets by sampling outputs from your Phase 2 SFT model and grading them.
  * [ ] Run a DPO alignment pass on Colab Pro using `trl` and analyze the divergence of chosen vs. rejected reward margins.

---

## Phase 5: Distributed Training Systems (Week 10)
**Primary Compute:** Colab Pro + Multi-Process Simulation  
**Objective:** Understand how hyperscalers train models when a single GPU is no longer enough.

### 5.1 Parallelism Paradigms
* **Data Parallelism (DDP):** Replicating the model on each GPU and syncing gradients via `AllReduce`.
* **Tensor & Pipeline Parallelism:** Splitting individual weight matrices (Megatron-LM style) and layers across GPUs.

### 5.2 Sharding Architectures (DeepSpeed & FSDP)
* **DeepSpeed ZeRO (Zero Redundancy Optimizer):**
  * **ZeRO-1:** Partitioning optimizer states ($4\times$ memory reduction).
  * **ZeRO-2:** Partitioning optimizer states + gradients ($8\times$ memory reduction).
  * **ZeRO-3 / PyTorch FSDP:** Partitioning parameters, gradients, and optimizer states across devices, using `AllGather` dynamically during the forward/backward pass.
* **CPU / NVMe Offloading:** Paging optimizer states to system RAM when VRAM is exhausted.

* **Phase 5 Deliverables (Lab 5):**
  * [ ] Write an `accelerate` and `FSDP` / `DeepSpeed ZeRO-2/3` configuration file and execute a sharded training script.

---

## Phase 6: Inference Optimization & Capstone Deployment (Weeks 11–12)
**Primary Compute:** Local RTX 4060 (Local Edge Deployment) + Colab Pro (High-Throughput Server)  
**Objective:** Merge your adapters, quantize the weights for production, and serve the model behind an asynchronous, high-throughput API.

### 6.1 Weight Merging & Post-Training Quantization (PTQ)
* **Adapter Merging:** Mathematically folding the learned $\frac{\alpha}{r}BA$ matrices back into the base weights $W_0$ in 16-bit precision (warn: never merge directly into 4-bit quantized weights without dequantizing first).
* **Quantization Formats:** Exporting to **GGUF** (for local CPU/GPU hybrid execution), **AWQ** (Activation-aware Weight Quantization), and **EXL2**.

### 6.2 Production Serving Engines
* **The KV Cache Bottleneck:** Calculating how Key-Value cache grows linearly with batch size and context length during autoregressive decoding.
* **PagedAttention & vLLM:** How `vLLM` manages KV cache like OS virtual memory pages to eliminate fragmentation and enable **Continuous Batching**.
* **Multi-LoRA Serving:** Serving a single base model in VRAM while dynamically hot-swapping multiple lightweight LoRA adapters per user request.

* **Phase 6 Capstone Project:**
  * [ ] **End-to-End Production System:** Take a raw open-weight model (e.g., Qwen 27B for cloud or 7B/8B for local RTX 4060 execution), curate a custom dataset, run SFT + DPO, prove superior performance on a custom evaluation benchmark, quantize the final artifact, and deploy it via a `vLLM` OpenAI-compatible API endpoint.