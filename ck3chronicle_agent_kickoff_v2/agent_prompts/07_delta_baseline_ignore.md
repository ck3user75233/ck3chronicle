# Agent Prompt 07: Delta, Baseline, Ignore

Implement session comparison, baselines, and ignored issues.

Commands:

- `ck3chronicle diff`
- `ck3chronicle baseline create <name>`
- `ck3chronicle baseline list`
- `ck3chronicle report --since <baseline>`
- `ck3chronicle ignore <issue_id>`
- `ck3chronicle unignore <issue_id>`
- `ck3chronicle ignored`

Acceptance criteria:

- Latest session can be compared to previous session.
- Issues are classified as new, fixed, worse, improved, or unchanged.
- Ignored issues are hidden from default reports but still stored.
- Baseline comparison works.
- Crash status is included in deltas.
- Delta logic operates on canonical issue records and normalized signatures.
