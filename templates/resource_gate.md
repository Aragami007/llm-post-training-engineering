# Resource admission gate — run/model

- [ ] Actual model name, architecture, model card, revision, tokenizer and license recorded.
- [ ] Weight-only BF16 / 4-bit theoretical lower bound computed in GiB; unquantized tensors and metadata called out.
- [ ] Memory model includes trainable gradients, optimizer states, activations, temporary buffers and CUDA context.
- [ ] Representative batch/context pilot executed or explicitly marked unverified.
- [ ] GPU and precision/kernels measured, not guessed.
- [ ] Dataset hash, estimated training tokens, tokens/sec, steps and effective batch specified.
- [ ] Estimated GPU hours, cloud spend, free storage and checkpoint retention within personal budget.
- [ ] Restore plan for cloud disconnection or OOM documented.
- [ ] Fallback identified (e.g., 3B QLoRA or toy CPU model).

**Go/no-go rationale:**
**Observed pilot measurements:**
**Maximum acceptable spend/time:**
**Rollback/fallback plan:**
