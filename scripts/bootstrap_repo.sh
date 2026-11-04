#!/usr/bin/env bash
# Create a PRIVATE repository from this folder and push the prepared documents.
# Run on a machine with git + GitHub CLI authenticated via `gh auth login`.
set -euo pipefail
REPO="${1:-Aragami007/llm-post-training-engineering}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
if ! command -v git >/dev/null || ! command -v gh >/dev/null; then
  echo 'Install git and GitHub CLI (https://cli.github.com/) first.' >&2
  exit 1
fi
gh auth status >/dev/null
# Only write when authenticated as the requested repository owner.
REPO_OWNER="${REPO%%/*}"
ACTIVE_LOGIN="$(gh api user --jq .login)"
if [[ "${ACTIVE_LOGIN,,}" != "${REPO_OWNER,,}" ]]; then
  echo "Authenticated GitHub login '$ACTIVE_LOGIN' does not match target owner '$REPO_OWNER'. Switch account with gh auth login/gh auth switch before publishing." >&2
  exit 1
fi
python3 scripts/validate_course.py
if [[ ! -d .git ]]; then
  git init -b main
fi
# Git settings are inherited from the authenticated user's machine; no identity is guessed.
git add .
if ! git diff --cached --quiet; then
  git commit -m "Initialize 24-week LLM post-training learning curriculum and 133-topic tracker"
fi
if gh repo view "$REPO" --json nameWithOwner >/dev/null 2>&1; then
  echo "Using existing repository $REPO; not altering its visibility."
else
  echo "Creating PRIVATE GitHub repository $REPO."
  gh repo create "$REPO" --private --source . --remote origin --push
  echo 'Repository created and files pushed. Continue with publish_issues.py.'
  exit 0
fi
if ! git remote get-url origin >/dev/null 2>&1; then
  git remote add origin "https://github.com/$REPO.git"
fi
# Do not overwrite an existing remote: an unrelated origin could lead to accidental pushes.
CURRENT_REMOTE="$(git remote get-url origin)"
if [[ "$CURRENT_REMOTE" != *"$REPO"* && "$CURRENT_REMOTE" != *"$REPO.git"* ]]; then
  echo "Origin points somewhere else ($CURRENT_REMOTE). Resolve manually before pushing." >&2
  exit 1
fi
git push -u origin main
printf 'Files pushed: https://github.com/%s\n' "$REPO"
