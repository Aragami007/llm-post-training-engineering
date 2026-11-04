# Roadmap, pacing, and graduation rules

The approved curriculum has **24 weeks and 12 phases**, where Phase 0 and Phase 10/11 take one week and the remaining phases take 2–3 weeks. The complete canonical descriptions are in `SYLLABUS.md`.

A sequential phase gate (`Pxx-NN`) checks readiness. Gate issues are mandatory, as are all non-optional topics unless the evidence requirements are explicitly replaced with an equivalent tested artifact and justified in the issue comments.

**Core issue effort estimate:** 414.5 hours / 24 weeks ≈ 17.3 focused hours/week. This is near the high end of the planned 12–18 hours/week, not a fixed promise. If you average 12 hours/week, extend the calendar rather than eliminate tests or audits. Cloud run waiting time, installations and paper-research depth may add further time.

## Exit gates

| Phase | Exit evidence |
|---|---|
| 00 | Fresh-environment recipe, hardware inventory, checkpoint resume test |
| 01 | Mini transformer, attention numerical tests, precision/attention scaling results |
| 02 | Scratch LoRA adapter, checked gradients, actual GPU memory sweep |
| 03 | Frozen independent evaluator and B0 baseline **before** any finetuning examples are generated |
| 04 | Dataset provenance, 100 manually audited random items, no unresolved split leakage |
| 05 | B1 fine-tuned model and at least one controlled ablation; unsuccessful improvement is honestly diagnosed |
| 06 | Deliberate overfit/unstable runs, controlled repairs and repeatability evidence |
| 07 | Scratch DPO, independent B2 evaluation, preference quality audit and bias checks |
| 08 | Reproducible small online RL update and reward/task divergence demonstration |
| 09 | Correct CPU collective and sharding cost model; real 2+ GPU measurement optional |
| 10 | Actual API smoke test and measured memory/quality/latency tradeoffs |
| 11 | Reproducible final B0–B3 comparative research report and evidence index |

## Dependencies and parallelism

Topic order is a recommended learning sequence. Some reading issues can run in parallel with code labs, but Phase 3 must **precede** Phase 4/5 and preference/online RL work must inherit a well-defined B1 baseline. Issues include both a suggested immediately preceding item and the previous phase gate; where a dependency is a recommended study order rather than a hard technical block, state the reason if proceeding out of order.

## What counts as 'completed'

A passing issue has: a brief conceptual explanation in your own words; the checked tasks; committed evidence; a reproducible command/configuration; the specific acceptance test; one limitation or failure note; and a completion comment linking a commit/PR. Keep a snapshot of environment and data/model revisions. **Do not close an issue merely because external documentation was read.**

Stretch issues `kind:stretch` can be deferred explicitly when compute is unavailable or beyond an approved budget. Deferred stretch work must not be described as executed research.
