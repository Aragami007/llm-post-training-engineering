# Reading ladder and documentation

Links here are study references, not evidence that a study/lab was done. Pin library versions in individual experiments and revisit online documentation when libraries change.

## Foundations
- Vaswani et al., *Attention Is All You Need* — https://arxiv.org/abs/1706.03762
- Dao et al., *FlashAttention* — https://arxiv.org/abs/2205.14135
- PyTorch SDPA — https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html
- PyTorch CUDA memory — https://docs.pytorch.org/docs/stable/torch_cuda_memory.html

## Adaptation and data
- Hu et al., *LoRA* — https://arxiv.org/abs/2106.09685
- Dettmers et al., *QLoRA* — https://arxiv.org/abs/2305.14314
- PEFT quantization — https://huggingface.co/docs/peft/developer_guides/quantization
- Transformers chat templates — https://huggingface.co/docs/transformers/chat_templating
- TRL SFT trainer — https://huggingface.co/docs/trl/sft_trainer
- Hugging Face dataset cards — https://huggingface.co/docs/hub/datasets-cards

## Evaluation and alignment
- EleutherAI lm-evaluation-harness — https://github.com/EleutherAI/lm-evaluation-harness
- Rafailov et al., *DPO* — https://arxiv.org/abs/2305.18290
- TRL DPO — https://huggingface.co/docs/trl/dpo_trainer
- TRL RewardTrainer — https://huggingface.co/docs/trl/reward_trainer
- DeepSeekMath / GRPO — https://arxiv.org/abs/2402.03300
- TRL GRPO — https://huggingface.co/docs/trl/grpo_trainer
- Ouyang et al., *InstructGPT* — https://arxiv.org/abs/2203.02155

## Systems and deployment
- PyTorch distributed — https://docs.pytorch.org/docs/stable/distributed.html
- PyTorch FSDP2 — https://docs.pytorch.org/docs/stable/distributed.fsdp.fully_shard.html
- DeepSpeed ZeRO — https://www.deepspeed.ai/tutorials/zero/
- vLLM LoRA — https://docs.vllm.ai/en/stable/features/lora/
- vLLM metrics — https://docs.vllm.ai/en/latest/usage/metrics/
- Google Colab FAQ (resource availability) — https://research.google.com/colaboratory/faq.html
