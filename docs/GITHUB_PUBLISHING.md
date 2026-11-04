# Publish this course to GitHub (private by default)

## Why this step exists

The supplied workspace contains **all files and all 133 issue bodies**. It was prepared without modifying existing unrelated repositories. The connected GitHub integration in the originating chat does **not** expose an API action to create a new repository, so the package includes a self-service publishing route through the **GitHub CLI**. Files and issues should not be described as live on GitHub until these commands succeed.

## Prerequisites

1. Authenticate as **`Aragami007`** (not a second GitHub account). Verify with `gh api user --jq .login`.
2. Git installed and configured with your preferred identity (`git config --global user.name ...` and `git config --global user.email ...` if required).
3. Python 3.10+ and [GitHub CLI](https://cli.github.com/).
4. Authenticate interactively on your computer: `gh auth login`, select `Aragami007`, and verify with `gh api user --jq .login`. **Do not paste your access token into an issue, this chat, screenshots, or the repository.**

## Recommended: bootstrap a private repository

From the unzipped course directory:

```bash
python3 scripts/validate_course.py
bash scripts/bootstrap_repo.sh Aragami007/llm-post-training-engineering
```

The bootstrap script validates the tracker, initializes Git, creates a local commit, creates a **private** GitHub repository only if one does not already exist, and pushes the workspace. Existing repo visibility is not changed. It refuses to push to an unrelated configured remote. It does **not** automatically publish 133 issues.

Alternatively create an empty private GitHub repository manually in your browser, then run the same script. Do not initialize the remote repository with a separate README if you want the simplest push.

## Preview and publish issues

```bash
# Read-only preview: doesn't need gh authentication
python3 scripts/publish_issues.py --repo Aragami007/llm-post-training-engineering --dry-run

# Small first batch for visual inspection; phase 00 has 9 items
python3 scripts/publish_issues.py --repo Aragami007/llm-post-training-engineering --phase 0 --limit 2 --apply

# When satisfied, continue all 133; existing topics are safely skipped
python3 scripts/publish_issues.py --repo Aragami007/llm-post-training-engineering --apply
```

The script ensures **12 phase milestones**, phase/type/scope/compute labels, and one issue per stable `Pxx-yy` ID. It checks the hidden marker `<!-- course-topic-id: Pxx-yy -->` across all issue states and **skips** already published topics; rerun after an API failure or rate limit. It waits briefly between requests and retries certain temporary failures. It does not modify the contents of existing issues by default, so your later learning notes are preserved.

A subsequent optional status snapshot:

```bash
python3 scripts/progress.py --repo Aragami007/llm-post-training-engineering
git add docs/PROGRESS.md && git commit -m "Refresh issue progress snapshot" && git push
```

## GitHub UX

- **Issues:** filter by `phase:03`, `kind:lab`, `scope:core`, etc.
- **Milestones:** Phase 00 through Phase 11, each with its designated phase gate.
- **Issue checklist:** click to check tasks as completed; link PRs/commits as evidence.
- **Issue close:** add a final comment with commands, test results, evidence and caveat; then close.
- **Progress:** GitHub Milestones provide live phase counts; `docs/PROGRESS.md` is only a snapshot after refreshing.

## Safety and limitations

- Default create mode is **private**; owner decides if/when to release publicly.
- No due dates were invented: the 24-week plan is relative to your actual start date.
- GitHub API writes require authentication with appropriate repository/issue permissions; the script cannot bypass account/org restrictions.
- If you encounter a secondary rate limit, stop and retry later; don't dramatically increase the request rate.
- The `--dry-run` option previews the manifest, not existing remote state. `--apply` queries live issues and then creates missing ones.
- Keep model weights, large datasets, cloud credentials, proprietary material and private logs out of source control.

## If publishing through an assistant later

Once the **empty repository** exists in your account, an assistant with GitHub file and issue write access can also populate it from the prepared Markdown manifest. Creation of a *new* repository is distinct from writing files/issues into an existing one.

## Optional project board

Once issues exist, follow [PROJECT_BOARD](PROJECT_BOARD.md) to create a visual Kanban board. Board creation/addition requires additional GitHub Project permissions and is intentionally not bundled into the automatic issue publication step.
