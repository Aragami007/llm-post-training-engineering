# Optional visual GitHub Project board

The default tracking system is **GitHub Issues + phase milestones + labels**; it works without GitHub Projects. For a visual Kanban board, a GitHub Project v2 can provide:

- **Status:** Backlog, In progress, Review, Done.
- **Phase:** use `phase:00` through `phase:11` issue labels or create a single-select phase field.
- **Issue type:** concept, lab, experiment, gate, stretch.
- **Learning evidence:** link to commit/PR, not a superficial checked box.
- **Pacing:** use the milestone/phase week ranges; avoid invented due dates.

### Manual setup (recommended)

After publishing the repository's course issues:

1. Open GitHub account **Projects → New project → Board**.
2. Name it **LLM Post-Training — 24-Week Learning Tracker**.
3. Add a GitHub issue view filtered to the course repository.
4. Group columns by Status and optionally create another table view grouped by Milestone.
5. Add the 133 course issues (select the repository's issues in bulk where supported); keep the GitHub Issues tab as the canonical open/closed record.
6. Change a card to Done only after its issue's acceptance tests have actually passed.

GitHub Projects may require an additional account authorization scope beyond ordinary GitHub Issues access. This project board is optional and **has not been created by the package**. Do not let project management overhead displace study time.
