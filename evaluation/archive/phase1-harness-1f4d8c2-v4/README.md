# Phase 1 evaluator harness source archive

This is a source-only archive of the independently authored public evaluator
harness used for candidate `1f4d8c2f5a6e3ec1c5dc7a5324b0bbe4c4b233ac`.
It is retained so the test infrastructure and machine-readable 35-gate plan
are not lost with a workstation or WIP directory.

Original frozen identities:

- full harness manifest SHA-256:
  `033a8e6ea0749386b7d157d98870308b44c047fe09261a1742b2442f6db1410c`;
- full harness source-set SHA-256:
  `ff72fbb17a555287312b8d6ae02884bc7a048d03dc4c5a3fe0fd7971527f62a1`;
- public plan SHA-256:
  `8ee8f194e6ff342680ba903f84d4f5ee23ba5aae4d03f9cb1531111b28a380b8`.

The archive contains evaluator source, the public run plan, and timeout table.
It contains no corpus files, CK3 logs, parsed log exports, private holdout,
expected answers, scorer logic, runner results, scorer results, or adjudication
results. Generated harness self-test and preflight outputs are also omitted;
their hashes remain in the historical project record but they are not reusable
source.

This harness is candidate-bound and contains historical machine-specific
defaults. It is not the next release harness and must not be silently reused or
edited into one. A future Phase 1 exit attempt still requires a fresh
independently authored/frozen harness against its fixed input authority. The
normative product interfaces and gate rules remain under `docs/`.
