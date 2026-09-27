# Brace candidate and evidence strength — 2026-09-23

## v36 boundary verification — 2026-09-26

The thirty-log native message is `Failed to read key reference: }: }, near line:
23876606`. Its established template has **two** OPTIONAL_KEY fields separated by
the literal `: `. The first brace occupies message bytes [30,31), the second
[33,34), and the line locator [47,55). Each brace is already one raw parser piece;
the entire `}: }` sequence is not one identifier field.

Inspection retained the canonical template's literals and normal location
constraints, but examined expected identifier spans even when their contents
failed ordinary KEY validity. Among 1,306 native rows with this diagnostic prefix,
there were zero ambiguous boundary assignments. The sole malformed-value row is
the brace example, occurring three times. The ordinary typed matcher still
rejects it and the model retains its separate provisional literal candidate.

Recommended correction: bind each exact malformed value to the established
expected field with an unsupported-syntax/punctuation annotation. Keep raw pieces
and byte ranges intact; do not declare punctuation valid identifier grammar or
use it as PARAM evidence. Multiple pieces may occupy an anomalous field only
when the complete diagnostic template establishes its boundaries. Preserve
uncertainty where it does not. This runtime/model binding is **not implemented**;
the completed work is native boundary verification, not a production fallback.

Evidence: `.codex-tmp/learner-refactor/adjective-ablation-v36/brace-boundaries.json`
and its native-only inspection script. Earlier counts below concern the older
ten-log review, not this thirty-log inventory.

Owner questioned why an anomalous brace in the normal key position became a
template, whether repeated occurrences drive learning, and whether template
provenance distinguishes strong empirical support from repeated observations.

## Confirmed native evidence

Candidate 231197737b82bcf8386a3ac2, template 2d80f2a2be6286b818549847:

`Failed to read key reference: }: }, near line: <LOCATOR>`

Two occurrences in two of ten logs; one distinct message. Both report line
23876606 and an empty filename. Timestamps are 09:37:34 and 19:55:17, source
pdx_persistent_reader.cpp:216. Their input hashes begin 5d6fceb4 and a0d5354e.
Both are preceded by empty key-reference reports and followed by a continuation
of Malformed token reports. This supports a malformed-input interpretation but
does not establish the original cause or originating file. The raw parser
retains the actual braces correctly.

## Why it became a candidate

The saved refinement records a 506-member provisional group splitting when a
field cannot support any ordinary slot type. The brace spelling becomes its own
one-member group. Re-inference against that single observation retains all
non-location content literally; location syntax independently supplies LOCATOR.
No evidence gate distinguishes this retained observation from a generalized
candidate. It has status provisional, not confirmed, but it produces a unique
complete match and therefore enters the full-match total.

This is the relevant design gap: preservation of an observation is being
represented as a candidate template and counted alongside empirically supported
generalizations. Removing PARAM fallback prevented the brace from corrupting
the ordinary KEY fields; it did not solve evidence qualification for the
remaining one-example formulation. No inference/status change was made during
this investigation.

## Repetition and diversity

collect_records deduplicates by source family, context kind and exact native
message. Alignment uses the distinct records; occurrence_weighting is false.
The two identical brace messages therefore provide one learning example.

Different locator spellings still make different native records. Consequently,
distinct native count alone is not evidence of different KEY values or different
diagnostic wording. Repeated logs may also share exactly the same failure state;
log coverage is useful provenance, not a measure of independent testing.

| Candidate | Occurrences | Supporting logs | Distinct native messages | Forms excluding locators/declared traces | Nonempty KEY values |
| --- | ---: | ---: | ---: | ---: | --- |
| Brace spelling | 2 | 2 | 1 | 1 | No learned KEY field |
| Normal key reference | 8,343 | 9 | 505 | 32 | 31 in each of its two fields |
| Generic script-system KEY trigger | 191,055 | 10 | 1,959 | 441 | 68 |

The current native comparison measures training-corpus reconstruction, not
independent generalization testing. All current templates remain provisional.
The counts above describe evidence strength without asserting a confidence score.

## Recommended correction, not implemented as an inference rule

Use anomalous punctuation as a contextual field observation: where same-source
surrounding wording and positions strongly agree with a supported candidate,
an unbalanced brace occupying its ordinary KEY position is evidence of an
invalid reported value, not evidence that the brace is fixed template wording.

Unbalanced punctuation alone is insufficient: a diagnostic may intentionally
quote syntax. Preserve the exact raw value, link the anomaly to the supported
formulation for review, and exclude it from ordinary KEY/PARAM evidence. Do not
declare the brace a valid KEY or force a full typed match. Any future generic
policy belongs in the owner-rule registry with explicit authority and evidence.

Candidate reporting should distinguish retained observations, formulations
supported by actual variable-value evidence, and reviewed contracts. This is
not a universal minimum-log rule: a fixed-word error can be legitimate, and one
log can contain ample distinct variable values. Replay alone cannot determine
semantic correctness for either kind.

## Reporting correction completed

native_evidence_rows formerly exposed just one provenance example by default.
The new review had incorrectly used that sample to count supporting logs.
It now requests all occurrences, counts provenance first, and only then retains
compact examples. Occurrence totals were already correct; log counts could be
understated. Every template's per-log support totals now reconcile to its saved
support count; the brace is explicitly verified as 2 occurrences / 2 logs.

The interactive review now exposes supporting-log count, distinct native count,
diagnostic-form count after LOCATOR/declared-trace replacement, per-KEY spelling
diversity and provisional/training-corpus status. Ordinary PARAM/REASON contents
remain in the diagnostic-form diversity measure. This is report-only; neither
model identity nor learning behavior changed. Full per-log counts and both
brace occurrences are saved under the ignored typed-fields-diagnostics directory.
