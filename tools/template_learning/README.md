# Empirical template-learning tools

This directory is the source-controlled home of the empirical learner,
incremental evidence registry, review-pack tools, blind-review helpers, and the
semantic-projection catalog builder used by ck3chronicle development.

Only reusable source belongs here. Captured `error.log` files, parsed exports,
training/reference corpora, human workbooks, private holdouts, incremental
state, and generated evaluation results are deliberately excluded from Git.
Supply those inputs through command-line paths and keep them under one of the
ignored local-data directories or outside the checkout.

The approved runtime artifacts are versioned under `models/` and verified by
SHA-256 at load time. These development tools may produce a candidate model or
catalog, but do not silently promote one. Promotion requires review, a new
immutable revision directory, manifest hashes, regression testing, and a code
change selecting the approved revision.

Semantic quality is tracked, not forced to perfection. Reports must preserve
the counts and examples for full, L1+L2, L1-only, provisional/low-confidence,
and unknown outcomes. The invariant is that every occurrence is accounted for;
unknowns and lower-confidence assignments are review debt rather than dropped
evidence.

Several files originated as WIP calibration utilities and are preserved here
so a machine loss cannot erase the project method. Their input corpora are not
part of the repository, and release scoring must remain role-separated from
learner development.
