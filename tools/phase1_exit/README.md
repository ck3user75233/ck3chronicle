# Phase 1 exit tools

These tools keep candidate execution separate from oracle scoring.

## `run_lexical_candidate.py`

Runner-side tool for the `P1-PAR-01-LEXICAL` component. It receives only a candidate checkout and an
`error.log`. It emits the candidate's lexical observations and input/candidate
identity. It fails if the imported lexer is outside the declared Git root and,
by default, if the candidate worktree is dirty. `--allow-dirty` exists only for
development calibration. The runner contains no expected values and accepts no
oracle argument.

## `score_lexical.py`

Scorer-side tool for the `P1-PAR-01-LEXICAL` component. It imports no ck3chronicle package and never
executes the candidate. It compares a sealed runner result with the independent
lexical oracle and emits a bounded gate result.

For a release run these commands execute under separate identities according
to `docs/PHASE1_EXIT_PROTOCOL.md`. Running both in one checkout is development
calibration only and must not be called a blind release evaluation.
