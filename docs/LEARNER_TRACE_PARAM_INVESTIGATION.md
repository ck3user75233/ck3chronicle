# Trace grouping and PARAM investigation

2026-09-21. Investigation of the completed ten-log candidate
`e375ae7fb4cf74bcdef446ec`; no inference implementation or model changes.

The learner currently prevents a multi-token trace from becoming a usable PARAM.
This is a learner restriction, not lost parser information. No new slot type is
needed merely to represent the observed trace ranges.

## Native evidence and causal check

Inspected all 18 distinct `Badly read script value` messages in source
`jomini_scriptvalue.h` from the complete ten-log comparison. Original protected
log SHA-256 hashes and exact message byte ranges were rechecked. Saved raw pieces
reconstruct each native message. No synthetic messages or recombined inputs.

Two actual messages (original leading space and CRLF retained in the JSON):

```text
Badly read script value 0.333333 at file: common/scripted_effects/mlgdc_shared_effects.txt line: 59 (mlgdc_cap_value[args#4128741568]:value:add:multiply)
Badly read script value 0.333333 at file: common/scripted_effects/mlgdc_shared_effects.txt line: 64 (mlgdc_cap_value[args#4128741568]:value:add:multiply:subtract)
```

Their current token similarity is 0.95, above the 0.72 grouping threshold.
Nevertheless their punctuation signatures differ, so the grouping code never
compares them. Calling current inference with both records raises
`literal punctuation/guidance boundaries differ within inference pool`.

For an isolated causal check, the observed terminal parenthesized interiors were
selected on actual parser boundaries. This selection is an inspection operation,
not a newly implemented universal trace detector. Given these exact ranges,
the existing `_slot` classifier selects PARAM. Current matching rejects all 18.
Changing only that candidate's `literal_punctuation` constraint to false, in
memory for this check, makes all 18 exact native ranges match. Parser boundaries
and default literal guidance remain enabled. This demonstrates the blocker; it
does not validate automatic trace detection or justify relaxing every slot.

## Exact code responsibilities

- `clustering.py::cluster_source_records` indexes candidates by an exact
  `literal_anchor_signature` as well as source context and wording anchors.
  Different colon/bracket counts therefore exclude a comparison. Similarity
  also counts punctuation tokens at the same weight as word tokens.
- `patterns.py::inference_units` represents recognized locations as ranges but
  leaves these ordinary-message traces in the diagnostic comparison sequence.
- `patterns.py::literal_anchor_indices` anchors every punctuation piece outside
  locations. `derive_pattern` demands matching signatures and aligns only
  between these anchors. A trace cannot reach slot inference as one range.
- `derive_pattern` also records a failure for punctuation inside any non-LOCATOR
  slot, including PARAM.
- `_slot` can classify a multi-token range as PARAM, but gives it
  `literal_punctuation=True`. `match_pattern` then stops that capture at its
  first internal punctuation token. PARAM thus cannot fulfill its intended
  role for these traces even if earlier grouping restrictions are bypassed.

Known L1/L2 processing already separates a tail component from the diagnostic
components. That does not exempt the tail's own grouping from the same
punctuation gate. The ordinary script-value messages above have no corresponding
trace range separation. Their formatting must not be assumed universal to all
sources, traces, or parenthesized diagnostic expressions.

## What happens when more logs arrive

`incremental_template_registry.py::build_revision` combines all selected training
evidence, deduplicates exact source/context/message records, retains occurrences,
and rebuilds provisional groups. Explicitly confirmed templates are matched
first; uncovered records enter discovery. It does not learn each new log from
zero evidence or count verbatim repeats as independent distinct formulations.

However, the grouping pass assigns records greedily against the first member
of each group. Later refinements update representatives and can split or merge
groups, but there is no general repeated reassignment against the updated
representatives. More evidence can change groups on a rebuild; it cannot cross
the still-mandatory punctuation signature restriction. The expected ability to
reconsider poorly assigned messages is therefore only partially implemented.

## Recommended correction scope

1. Compare case-sensitive diagnostic wording within its source and component.
   Remove exact punctuation-signature equality as a grouping prerequisite;
   punctuation must not veto otherwise similar wording. Keep punctuation and
   its positions available for boundary inference and exact matching.
2. Identify supported trace ranges before diagnostic similarity, retaining all
   original pieces and offsets. Use PARAM for the trace content, with the
   surrounding delimiters retained. Do not classify every parenthesis as a trace.
3. Let bounded PARAM ranges contain internal punctuation. Update alignment,
   candidate validation and matching together; changing only grouping or only
   the PARAM matcher leaves other blockers intact. KEY remains a complete
   non-punctuation parser token. LOCATOR remains independently range-based.
4. Reconsider provisional membership against updated diagnostic representatives;
   retain confirmed-template decisions and explicit ambiguity reporting.
5. Validate changes on the same complete ten logs, checking diagnostic wording,
   trace captures, exact boundaries, overlaps and fragmentation. The 18 cases
   establish the defect, not general accuracy of a replacement algorithm.

Do not add CK3_TRACE solely to work around the PARAM prohibition. A dedicated
type is worth considering only if a wider native trace review establishes useful
structural validation that PARAM cannot express. No claim that every trace in
the corpus has one format has been established here.

Reproducible inspection and all native provenance:
`.codex-tmp/learner-refactor/separator-learner-review/inspect_trace_blockers.py`
and `trace-blockers.json`. The 73-log run remains deferred; no model promotion.
