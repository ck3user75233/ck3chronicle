# ck3chronicle workspace instructions

Use the repository-root `AGENTS.md` as the normative instruction source. Read
`docs/CURRENT_HANDOFF.md` and `docs/WORKSPACE_ROUTING.md` before planning work.

- Work only in this standalone ck3chronicle Git root.
- Never implement ck3chronicle in `ck3raven` or `.ck3raven/wip`.
- Reuse `tools/template_learning/` for learner, review, registry, and catalog
  work; do not construct another learner elsewhere.
- Keep runtime logs, databases, corpora, workbooks, private holdouts, and
  generated evaluation results out of Git.
- Preserve unknown and low-confidence assignments for review; do not force
  100% semantic attribution.
- Add verification only after mapping it to an active owner-directed
  requirement and representative real CK3 behavior. Historical test
  expectations do not create product scope.
- Run routine Python verification through `.\.venv\Scripts\python.exe` inside
  the agent. The optional owner environment being inaccessible to the sandbox
  is not a reason to defer compilation, imports, CLI checks, or tests to Nate.
