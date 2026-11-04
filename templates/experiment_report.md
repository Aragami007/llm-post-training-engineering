# Experiment report — RUN-ID

## Claim and preregistered hypothesis

**What is the test? What result would falsify the idea?**

## Identity and versions

| Field | Value |
|---|---|
| Run ID / UTC date | |
| Git commit | |
| Base / tokenizer / adapter model IDs and revisions | |
| Dataset revision, SHA-256, split hashes | |
| Training method (SFT/DPO/RL/etc.) | |
| Precision/quantization and exact package versions | |
| Seed(s) | |

## Training details

| Field | Value |
|---|---|
| Learning rate, warmup and schedule | |
| Rank/alpha/target modules | |
| Microbatch/accumulation/effective batch | |
| Context length and real tokens processed | |
| Optimizer and update count | |
| Checkpoint/restart plan | |

## Hardware and budget

| Field | Value |
|---|---|
| GPU model/total VRAM and supports | |
| Theory weight + optimizer + activations | |
| Measured CUDA allocated/reserved/peak | |
| Measured full-device VRAM | |
| Tokens/sec and wall clock | |
| Storage and spend (actual or estimated) | |

## Controlled comparison

**Baseline and intervention:**
**Single main variable changed:**
**What was held fixed:** evaluation set, decoding, token budget, model lineage, metrics and code revisions.

| Model/run | Primary task metric | Uncertainty | Failure slice | Cost |
|---|---|---|---|---|
| B0 | | | | |
| B1 | | | | |
| B2 | | | | |
| B3 | | | | |

## Failure analysis

Include at least three representative mistakes or explain why none occurred. Note leakage risks, judge bias, changes in output length and task regression.

## Conclusion and limitations

**Supported result:**
**Alternative interpretation:**
**Unresolved questions:**
**Exact command and evidence links:**
