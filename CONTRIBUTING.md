# Personal contribution workflow

1. Pick the next GitHub Issue (stable ID `Pxx-yy`); read its prerequisites and acceptance check.
2. Create a short branch such as `study/P03-06-deterministic-eval` if useful.
3. Add reproducible code/notes and use [learning log](templates/learning_log.md).
4. Run tests and `python3 scripts/validate_course.py`.
5. Link your commit or pull request in the issue; state the exact command, measured result, unexpected finding and limitations.
6. Close only after the acceptance criteria are verified. The phase gate should be reviewed before moving to the next phase.

The syllabus is an approved plan, but can evolve with a *versioned* change note; do not quietly alter a frozen evaluation set or erase previous experiment results. Open a separate `curriculum-change` issue for substantive syllabus modifications.
