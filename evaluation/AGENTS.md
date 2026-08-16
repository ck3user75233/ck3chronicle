# Evaluation archive instructions

`evaluation/archive/` contains source-only historical snapshots of completed,
independently authored evaluator harnesses. It is not the workspace for the
next release attempt.

- Do not edit an archived harness in place.
- Do not add corpora, private holdouts, expected answers, runner outputs,
  scorer outputs, databases, logs, or generated result packages.
- Implementation agents may update public product contracts elsewhere in this
  repository, but they do not author the next executable exit harness or
  scorer.
- The next harness is commissioned in a fresh user-owned evaluator task, not a
  subagent of the implementation task. The blind runner uses a separate task.
- If an independently completed harness must be preserved, add it under a new
  immutable attempt/revision directory with a source manifest and provenance;
  never overwrite a prior archive.
