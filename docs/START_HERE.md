# Start here: the first 90 minutes

This is a learning operating system, not merely a reading list. Begin with tiny, verifiable actions.

## In order

1. Read the objectives and compute limitations in `SYLLABUS.md`.
2. Run `python3 scripts/validate_course.py` to confirm all 133 topic files and IDs are present.
3. Open [P00-01](../tracker/issues/P00-01.md). Write your own map of base pretraining → CPT/DAPT → SFT → preferences → online RL; preserve base vs instruct terminology.
4. Open [P00-02](../tracker/issues/P00-02.md). Record OS, CUDA driver, PyTorch/Transformers version and `git status`.
5. Open [P00-03](../tracker/issues/P00-03.md). Measure RTX 4060 VRAM and available storage. Do not guess support for BF16.
6. Duplicate [the lab log](../templates/learning_log.md) for each meaningful topic, e.g. `experiments/P00/P00-02.md`.
7. Close a published issue only when its checklist, acceptance check and evidence are complete.

## Study rhythm (12–18 focused hours per week)

- **Understanding:** derive equations and explain mechanisms without copying.
- **Building:** implement at toy scale and test invariants.
- **Measurement:** run an instrumented comparison with written assumptions.
- **Review:** document failures, limitations, next experiment and evidence links.

Time estimates in topics are optimistic, focused hours; include extra time for installations and failed runs. Do not bypass a phase gate to meet the calendar.

## What to avoid in Week 1

Do not download multiple 27B checkpoints, rent multi-GPU clusters, or start creating SFT examples without a frozen evaluation design. The substantive B0/B1/B2/B3 experiment begins in Phase 3, after hardware and foundational mathematics are understood.

## Core toolchain

Python 3.10+; Git; PyTorch; Transformers; Datasets; PEFT; TRL; optional bitsandbytes/Unsloth/vLLM based on verified hardware support; optional W&B or other experiment logger. **Do not pin a universal GPU package list here**: capture tested package versions in `environment.md` or a lockfile for each environment.
