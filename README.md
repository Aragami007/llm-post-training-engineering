# LLM Post-Training Engineering — Kausthuba's Learning Lab

> A **24-week, experiment-first curriculum** for learning the mathematics, data engineering, evaluation, SFT, preference optimization, online RL, distributed training and inference systems behind post-training text LLMs.

**Status:** Published to the private GitHub repository. All **133 topic issues** have been created on GitHub and the course sources are committed. Phase milestone synchronization is managed by `.github/workflows/publish-course-tracker.yml`.

[Read the full syllabus](SYLLABUS.md) · [Start here](docs/START_HERE.md) · [All 133 topic issues](docs/ISSUE_INDEX.md) · [Evaluation protocol](docs/EVALUATION_PROTOCOL.md) · [Capstone](docs/CAPSTONE.md) · [GitHub publishing](docs/GITHUB_PUBLISHING.md)

## Mission

Progress from **understanding core tensors and gradients** to **running reproducible, honestly evaluated post-training experiments**. Build the habits required for a post-training engineering role: calculation, empirical validation, clean dataset lineage, independent evaluation, rigorous ablations, and reproducible serving. This is a technical foundation and portfolio, **not** a claim to acquire hyperscaler-level expertise in 24 weeks.

### The four checkpoints

| Checkpoint | What it proves | Model source |
|---|---|---|
| **B0** | Prompted instruction-tuned baseline, measured before training | Untuned *for this task* instruct model |
| **B1** | Supervised fine-tuning (LoRA/QLoRA) | B0-compatible training lineage |
| **B2** | Offline preference optimization (e.g., DPO) | B1 plus preference data |
| **B3** | Small online RL branch with verifiable rewards | Controlled branch, compared with B1 and B2 |

An underlying pretrained **base checkpoint** can be preserved as **B-1** when useful. B3 may underperform B2; learning requires evidence, not a forced success story.

## Your compute reality

- **Local:** NVIDIA RTX 4060 8 GB, Ubuntu, limited NVMe + external storage.
- **Cloud:** Google Colab Pro when suitable GPUs are available; **L4/A100 access is not guaranteed**.
- **Core lab model ladder:** toy/tens-of-millions → 0.5–1.5B → 1–3B with LoRA/QLoRA.
- **Optional:** 7–14B cloud pilots; 27B and actual multi-GPU runs are resource-gated stretch work, never required to graduate.

Do not measure success by the parameter count of a model that fit in VRAM. Read [the compute policy](docs/COMPUTE_AND_COST.md).

## Roadmap and workload

| Phase | Week(s) | Subject | Issues |
|---|---|---|---:|
| 00 | 1 | Environment and reproducibility | 9 |
| 01 | 2–3 | Transformers, optimization and GPU primitives | 12 |
| 02 | 4–5 | LoRA, QLoRA and memory accounting | 11 |
| 03 | 6–7 | Task framing and **evaluation before tuning** | 12 |
| 04 | 8–9 | Dataset creation and curation | 12 |
| 05 | 10–12 | Supervised fine-tuning and ablations | 11 |
| 06 | 13–14 | Training diagnostics and interpretation | 10 |
| 07 | 15–17 | Reward modeling and offline preferences | 13 |
| 08 | 18–20 | Online RL and verifiable rewards | 12 |
| 09 | 21–22 | Distributed training systems | 11 |
| 10 | 23 | Serving, artifact engineering and observability | 10 |
| 11 | 24 | Capstone and research portfolio | 10 |
| | | **Total** | **133** |

The estimated 414.5 focused hours for all **core** issues is near the high end of a 12–18 hr/week plan. Slow down rather than skip correctness gates. Three optional stretch issues add ~15 hours. See [pacing rules](docs/ROADMAP.md).

## How the GitHub issue tracker works

Each course subtopic is **one issue** with a stable topic ID (e.g., `P03-06`) and:

- Theory and concepts to be able to explain.
- Explicit study/lab/experiment checklist.
- Named output artifact to commit as proof.
- A measurable **acceptance test** and completion comment.
- Suggested dependencies, reading, phase/week and estimated hours.

Labels distinguish phase, issue kind, core/stretch and compute requirements. Twelve phase milestones are specified by the tracker publishing workflow; verify their live assignment in the GitHub Milestones view. Each phase ends with a **gate issue**; pass the gate before advancing. GitHub Issues remain the source of truth for open/closed status after publication; `docs/PROGRESS.md` begins as a local, not-live snapshot.

**Close issues on evidence, not on having watched a tutorial.** A rigorous negative result qualifies if it is reproducible and correctly interpreted.

**Destination account:** `Aragami007`. The publication scripts verify that GitHub CLI authentication matches this owner before pushing files or issues. Nothing should be published to another account.

## Quick start on your computer

1. Read [START_HERE](docs/START_HERE.md) and [EVALUATION_PROTOCOL](docs/EVALUATION_PROTOCOL.md).
2. Install Git, Python 3.10+ and, for publication, the [GitHub CLI (`gh`)](https://cli.github.com/). For local course tools, no GPU or third-party Python packages are needed.
3. Run `python3 scripts/validate_course.py` (or `make validate`).
4. Start with `P00-01`, then the environment and reproducibility issues.
5. When ready to create the **private** GitHub repo, follow [GITHUB_PUBLISHING](docs/GITHUB_PUBLISHING.md) or use the bootstrapping script below.

```bash
# After obtaining the folder on your own machine and logging in via `gh auth login`:
bash scripts/bootstrap_repo.sh Aragami007/llm-post-training-engineering
python3 scripts/publish_issues.py --repo Aragami007/llm-post-training-engineering --dry-run
python3 scripts/publish_issues.py --repo Aragami007/llm-post-training-engineering --apply
```

`publish_issues.py` uses stable markers to avoid creating duplicate issues on reruns. It creates phase milestones and labels, then publishes issues. The default operation without `--apply` is **dry-run**. See the full guide for privacy and rate-limit safeguards.

## Workspace structure

```text
SYLLABUS.md                   Approved revised full syllabus, v2
tracker/topics.json           Structured source of truth: 133 topics
tracker/issues/Pxx-yy.md      Human-readable complete issue bodies
tracker/issue_manifest.csv    Spreadsheet-friendly issue inventory
docs/ISSUE_INDEX.md           All phase/topic links
docs/TECHNICAL_AUDIT.md      Technical corrections from the original syllabus
docs/ORIGINAL_DRAFT.md        Original 12-week syllabus for provenance
docs/EVALUATION_PROTOCOL.md   Frozen data, baselines, judge validation, metrics
docs/COMPUTE_AND_COST.md      Memory lower bounds, resource gates, fallback policy
docs/CAPSTONE.md              B0/B1/B2/B3 evidence requirements
templates/                   Reusable lab log, data/model cards, research notes
scripts/                     Course validation, issue publishing, progress tools
.github/                     Issue templates and a validation workflow
data/, train/, eval/, serve/   Intended workspaces for your future implementations
```

## Operating principles

1. **Freeze evaluation before training.** Never expose hidden test cases to teacher generation, preference labeling or prompt selection.
2. **Record actual machine capabilities.** Not all software combinations support BF16, FlashAttention, quantized training or vLLM on a given GPU.
3. **Prefer small conclusive runs.** A repeatable 1B experiment can be more valuable than an anecdotal 27B outcome.
4. **Never commit secrets, personal data, proprietary datasets, checkpoints or model weights** without ensuring you have appropriate rights. See [SECURITY](SECURITY.md).
5. **Teach from failures.** Record OOMs, negative results, problematic reward functions and baselines as rigorously as improvements.

## Original draft, corrections and ownership

This repository preserves the original draft in `docs/ORIGINAL_DRAFT.md`, the reviewed curriculum in `SYLLABUS.md`, and the detailed rationale in `docs/TECHNICAL_AUDIT.md`. Software/documentation links are references, not vendored third-party code. **No public reuse license is granted by default**; see [LICENSE-NOTICE](LICENSE-NOTICE.md). The intended default GitHub visibility is private.

## Optional advanced tracking

Use a [GitHub Project board](docs/PROJECT_BOARD.md) if visual Backlog/In progress/Review/Done columns help; the course works without it. Maintain the [competency matrix](docs/SKILL_MATRIX.md) from actual evidence, not aspirational labels.