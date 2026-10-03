# Shared matcher — independent pipeline verification

## Historical verification checkpoint

The candidate below is now integrated and selected by
[Task 05](TASK05_ERROR_CONTRACT_IMPLEMENTATION_HANDOFF.md). This report and its
comparison command describe the predecessor pipeline interfaces. Use the Task 05
handoff for current native replay, rendering and installed verification commands.

2026-09-27. **Passed on the available native corpus; ready for pipeline
integration.** Candidate `44a0401b8adf0a2953d26705` loads independently and returns
complete selected assignments that the current pipeline binding helper accepts.
No candidate defect was found in this verification. Active selection and
application integration remain unchanged.

Manifest SHA-256:
`2a768c9d9729025da2874671dfc5952b703019f57a36a68e8437e1242122aca1`.
Model `76630685c4a341ca14bf9c7c`, parser `ck3-lossless-v1.7`, matcher API
`ck3-native-matcher-v1`, selector `complete-assignment-v2`.
The [delivery handoff](LEARNER_PARSER_PIPELINE_HANDOFF.md) and
[API specification](SHARED_MATCHER_API.md) describe the integration interface.

## Fresh execution results

Reparsed all 30 model-supporting complete logs and the additional handoff log.
Every input hash was verified; all training-evidence hashes are covered.

| Check | Independently observed result |
|---|---:|
| Complete native logs | 31 |
| Recovered occurrences | 1,167,165 |
| Selected template matches | 712,271 |
| Selected provisional matches | 445,741 |
| No match | 9,153 |
| Differences from current pipeline in selected IDs, statuses, wrapper choices or ordered captures | 0 |
| Present captures verified against original bytes | 4,447,658 |
| Absent captures verified separately | 59,054 |
| Selected regions reconstructed exactly from model layouts and values | 1,268,561 |
| Existing pipeline binding-helper calls accepting package captures | 1,268,561 |

Coverage includes all nine slot types, 55,268 wrapped occurrences, one present
empty REASON, opaque full identifiers, and 11 continuation groups containing
13 ordered entries. Component indices and selected layout references resolve
correctly. Unmatched evidence remains available in its original regions.
The resulting outcome and capture counts agree with the learner's delivery.

The package loaded with Python `-I -S -B`, with explicit import blocking for
`template_learning` and `ck3chronicle`. All twelve payload hashes passed. Model,
parser, parser manifest, owner rules, selector and source-validation bytes match
the active release. The seven packaged matching/bootstrap modules match the
current learner source bytes. Matching therefore does not require a mutable
learner checkout or the pipeline's separate matcher.

## Method and limits

A fresh verification script used prior evidence only to locate native logs and
their recorded hashes. It did not reuse saved classifications, the learner's
verification scripts, test fixtures or synthetic inputs.

The main replay matched 78,882 distinct complete inputs within logs, caching
relative results for exact repetitions. Its key includes parser identity,
source family/tag, context kind, complete text/pieces and ordered continuation
framing; occurrence provenance is excluded. Every occurrence independently passed
native-region, rendering and byte checks. A separate fresh pipeline replay
compared selected results on those same inputs and used the existing binding
helper on every occurrence. Parser artifact paths were normalized to the common
manifest reference after verifying the actual parser version and hash.

An additional **uncached** standalone replay called the public matcher for every
one of the additional log's 24,112 occurrences. Instrumentation observed exactly
24,112 selector calls and 17,781 selected-region materializations: one selection
per occurrence, one materialization per winning region, none for losing
candidates. Ordinary output omitted research alternatives, and native provenance
passed through by object identity.

This establishes selected-result compatibility, byte preservation and usable
layout references. It does not independently establish every internal candidate's
eligibility or the semantic correctness of learned templates. Ties, capture
ambiguity, alternative component layouts, groups exceeding two entries and
malformed/integrity failure paths remain outside this native coverage. No inputs
were manufactured to exercise them. SQL, installed packaging and application
cutover were not exercised.

## Evidence and reproduction

Fresh ignored evidence is under
[shared-matcher-pipeline-verification-20260927](../.codex-tmp/shared-matcher-pipeline-verification-20260927/):

- [Verification script](../.codex-tmp/shared-matcher-pipeline-verification-20260927/verify.py),
  [environment](../.codex-tmp/shared-matcher-pipeline-verification-20260927/environment.json)
  and [input inventory](../.codex-tmp/shared-matcher-pipeline-verification-20260927/inputs.json).
- [Standalone results](../.codex-tmp/shared-matcher-pipeline-verification-20260927/standalone.json),
  [pipeline comparison](../.codex-tmp/shared-matcher-pipeline-verification-20260927/comparison.json)
  and [uncached instrumentation](../.codex-tmp/shared-matcher-pipeline-verification-20260927/ordinary.json).
- [Readable native spot checks](../.codex-tmp/shared-matcher-pipeline-verification-20260927/NATIVE_EXAMPLES.md)
  and [scope verification](../.codex-tmp/shared-matcher-pipeline-verification-20260927/scope.json).

From the repository root:

```powershell
.\.venv\Scripts\python.exe -I -S -B -u .codex-tmp/shared-matcher-pipeline-verification-20260927/verify.py standalone
.\.venv\Scripts\python.exe -I -B -u .codex-tmp/shared-matcher-pipeline-verification-20260927/verify.py compare
.\.venv\Scripts\python.exe -I -S -B -u .codex-tmp/shared-matcher-pipeline-verification-20260927/verify.py ordinary
```

All 290 pre-existing tracked/untracked non-ignored file hashes remained unchanged.
This task adds this report and ignored verification artifacts only. Pipeline
reader/classifier integration, removal of the duplicate matcher, and activation
of the candidate are the remaining implementation steps.
