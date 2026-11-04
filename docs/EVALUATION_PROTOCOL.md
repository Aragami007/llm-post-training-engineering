# Frozen evaluation and scientific comparison protocol

**Before training**, create a stable unseen test set for a narrow measurable task. Prefer structured tool calling, programmatically graded code transformations or verifiable mathematics. Document a task specification and failure taxonomy.

## Data boundaries

- `train`: model updates and data generation, not final scoring.
- `dev`: prompt selection, hyperparameter tuning and early stopping; report the amount of search performed.
- `test`: **frozen** final measurement. Never show hidden examples to synthetic-data teacher generation or tune prompts/hyperparameters after seeing test responses.
- Preference train/dev/test: separate from supervised examples where practical; preserve prompt-level lineage and deduplicate semantically, not just by file hash.
- Preserve split IDs, SHA-256 checksums, collection metadata, licenses and versioned grader definition.

## Score and report

For each B0/B1/B2/B3 model under an unchanged test protocol record the same prompt, chat template, max token count, sampling settings, exact checkpoint/adapter, structured-output constraints, and metric code revision. Suggested task metrics: schema validity, executable success, correct tool choice/arguments, abstention correctness, unsupported-claim rate and latency/cost. Select one primary metric before training.

For paired model comparisons store **per-item records** (not aggregate wins only) and compute a confidence interval or a justified alternative uncertainty statement. Report total item count, slice counts, average and failure cases. Use deterministic programmatic grading wherever possible.

## LLM judge discipline

- Use a written rubric and independent judge where possible.
- Blind model identity and randomize/swapped A/B order; count ties.
- Calibrate against a human-scored sample and report judge–human disagreements.
- Detect verbosity/length/position preference and whether the same teacher/judge generated preferred examples.
- Never claim DPO implicit reward margins alone show better truthfulness or task accuracy.

## Regression and safety

Create slices for catastrophic-forgetting-relevant functions, malformed tool calls, unsafe actions, hallucinations, abstention, long/short prompts and distribution shifts. A smaller but relevant regression suite can be more informative than downloading a giant unrelated benchmark. Academic benchmarks are supplementary, not substitutes for task-level tests.

## Baseline ledger

| Checkpoint | Training source | Primary metric | Confidence/variation | Regressions | Compute/cost |
|---|---|---|---|---|---|
| B0 | Untuned instruct | To measure before tuning | | | |
| B1 | SFT adapter | | | | |
| B2 | DPO / offline preference | | | | |
| B3 | Small verifiable online RL | | | | |

Use [experiment report template](../templates/experiment_report.md) and [capstone specification](CAPSTONE.md). Negative results count as legitimate findings when they are independently evaluated.
