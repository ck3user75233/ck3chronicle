# Empirical region discovery: native comparison

Completed 2026-09-21. The terminal-parenthesis shortcut was removed first;
the replacement uses native variation and ordinary slot assessment. This is
a learner/model change. Raw parser v1.6, emission framing and recovery are
unchanged. No model was promoted and no SQL or runtime registry was changed.

## Baseline and provenance

The named removal edits were verified and applied in descending line order
within each file. The removal ledger and source snapshot are in
`.codex-tmp/learner-refactor/empirical-regions/removal-edits.json` and
`removal-source/`. No active `terminal_parameter_range`,
`terminal_parentheses` or `parameter_field` remains in learner code or tests.
Historical documentation is explicitly marked as withdrawn/superseded.

The principal comparison is:

| Implementation | Immutable candidate | Build seconds |
|---|---|---:|
| Shortcut removed, before replacement development | `248aaaad5e39b1cd80ff0872` | 80.69 |
| Empirical region discovery | `e0f2d9bfd621adf7176400aa` | 164.39 |

Both used the same ten complete native logs: 343,585 emissions, 352,317
messages, 7,827 distinct source/message pairs, 7,864 contextual evidence rows,
and 93 source families. Parser identity and effective literal vocabulary are
the same. There were no confirmed templates in this exercise. Build times
are single local observations, not a controlled performance benchmark.

Candidate directories are below
`.codex-tmp/learner-refactor/empirical-regions/removal-baseline/candidate/`
and `empirical-delivery/candidate/`. Input identities, selection, command and
run result are saved beside each build. Final source hashes were checked
against the candidate; `delivery-source/` preserves that implementation.
Earlier shortcut-assisted results are historical comparisons only.

## What changed

Comparable native messages are aligned within their source and component.
Stable wording, separator occurrence/rank and observed nesting supply possible
boundaries at any position. Repeated internal punctuation whose count or
positionch, not an unrestricted search for
a globally optimal partition.
 varies does not automatically remain a template boundary. Interior
literals and ordinary KEY, VALUE, LOCATOR and PARAM assessment determine
whether an envelope remains literal, narrows, divides or supports a field.
Delimiter presence alone neither assigns PARAM nor removes literal guidance.

The learner reconsiders provisional groups using these hypotheses. A union
must first infer a candidate from its actual native members. Only then are
supported PARAM captures excluded from wording similarity, with neither a
penalty nor a placeholder bonus. At least two shared wording tokens and the
existing .72 threshold are required. Accepted unions reduce group count;
changed pools are reconsidered until no further union qualifies. This is a
finite, conservative union/refinement sear
Two safeguards arose from native inspection and are recorded as engineering
heuristics, not owner-supplied CK3 formats:

- One nonempty spelling plus absence does not establish varying contents for
  a multi-token PARAM. Record insufficient evidence and retain the observed
  literal formulations separately. This is not a blanket rule for every
  fixed word plus absence and does not change OPTIONAL_KEY.
- A proposed PARAM must not erase independently supported literal word runs
  from a group with observed non-location variation. This preserves the
  distinct gene-error formulations, but can also overprotect repeated field
  values; the resulting ambiguities are reported below.

Matching retains exact raw boundaries, whitespace and punctuation. A PARAM
gets a balanced-pair constraint only when all observed values support it;
the matcher then prevents an internal closing delimiter from prematurely
ending that capture. Source partitioning, separate L1/L2 learning, location
recognition, complete-token KEY captures, case distinctions and literal
guidance remain. No optional-literal mechanism or new hardcoded PARAM format
was introduced. Confirmed-template review decisions remain separate from
provisional inference, and competing matches remain visible.

## Marker decision

Standalone period tokens occur 5,632 times and equals tokens 57 times in the
selected recovered messages. Native periods include sentence endings; equals
occurs both inside `Current Buildings = yurt { ... }` content and as the bad
value in `Missing participant definition for tag '='`. No standalone backslash
token occurs in these ten logs' recovered message content. This is not a claim
about all CK3 logs.

Period, equals and backslash do not seed automatic marker-envelope proposals.
They remain original raw evidence and can remain supported literal boundaries
under ordinary alignment. This does not change tokenization or location
recognition. The owner's follow-up confirms that prior backslash assessment
established its path role apart from already handled harmless cases, and
explicitly endorses excluding it from PARAM-envelope proposals. This ten-log
subset alone does not repeat that assessment; no marker-policy ablation was performed. The native
counts and examples are in `marker-evidence.json` beside the comparisons.

## Results on the same ten logs

| Outcome | Shortcut removed | Empirical discovery |
|---|---:|---:|
| Full ordinary diagnostic | 140,443 | 140,435 |
| L1+L2 diagnostic | 209,808 | 211,869 |
| Ambiguous occurrences | 2,066 | 13 |
| Unknown, partial or L1-only | 0 | 0 |
| Ordinary templates | 321 | 308 |
| Component templates | 432 | 354 |
| Unresolved emissions | 0 | 0 |

2,064 formerly ambiguous occurrences become L1+L2 matches. Eight previously
full ordinary occurrences and three previously L1+L2 occurrences become
ambiguous. Two existing Lowborn ambiguities remain. There are no new unknown
or partial outcomes. Template/capture assignments changed for 3,782 contextual
rows representing 122,126 occurrences; this is broader than outcome changes.

Follow-up clarification: 1,934 of those rows (94,307 occurrences) have identical
written templates and captures; their candidate identity/constraints changed.
The other 1,848 rows (27,819 occurrences) have changed written templates.
Do not interpret the aggregate as 3,782 visibly different formulations.

The grouping ledger records 98 accepted unions, 6,884 rejected proposals and
37 divided proposals. Final patterns retain 2,330 accepted, 3,873 rejected,
409 divided and 287 narrowed region investigations, plus 18 rejected boundary
anchors. Including unsuccessful grouping proposals, 27 insufficient-evidence
decisions remain inspectable. These are audit decisions, not independent
messages or confidence scores.

## Inspectable native examples

The reports below are generated evidence and intentionally remain outside Git:

- [Readable side-by-side review](../.codex-tmp/learner-refactor/empirical-regions/READABLE_REVIEW.html):
  ten random resolved-ambiguity cases, ten random assignment-change cases,
  and the ten original region examples rewritten without JSON. Exact sampling
  pools, seeds, native provenance and plain-English caveats are recorded.
- [Rule explanations and native literal-guidance examples](../.codex-tmp/learner-refactor/empirical-regions/RULE_EXAMPLES.md).

- [Ten detailed region examples](../.codex-tmp/learner-refactor/empirical-regions/REGION_EXAMPLES.md):
  original messages, source, actual raw pieces, proposed byte/piece ranges,
  observed variation, final templates and captures, plus grouping decisions.
- [46 before/after comparisons](../.codex-tmp/learner-refactor/empirical-regions/NATIVE_COMPARISON.md):
  removal-baseline and final candidates together, including regressions.
- [Complete comparison data](../.codex-tmp/learner-refactor/empirical-regions/comparison.json)
  and [region audit](../.codex-tmp/learner-refactor/empirical-regions/REGION_REVIEW.json).

Examples extend beyond terminal traces: a script-value trace followed by more
message wording; a name between unpaired wording boundaries; a square-marker
mesh field; an assertion field; and nested scoped-object content. The nested
object retains stable wording and infers VALUE for the changing number rather
than turning its whole interior into PARAM. Relationship variation remains
KEY. A constant dynasty interior is rejected as a new PARAM; presence/absence
of the single observed `(opinion)` spelling is insufficient for one. Distinct
`No gene with key ...` and `Trying to read gene ...` wording remains separate.

## Regressions and remaining limits

The 11 newly ambiguous occurrences are real regressions in match uniqueness:

- Eight `culture_history_entry.cpp` messages for swahili at 1178.1.1 have the
  same explanation but different innovation keys. A broad candidate ending
  `Reason<PARAM>` overlaps a narrower candidate preserving the repeated
  discovery/era explanation. Shared repeated explanation alone does not
  establish a new nested L1/L2 convention.
- Three `jomini_script_system.cpp` L2 messages for Amdo, Dāmina and Tado match
  both `Province '<KEY>' does not have building '<PARAM>'` and the formulation
  with literal `'Wet Fields'`. The wording safeguard overprotects the repeated
  building value in the narrow pool.

The original two `characterhistory.cpp` Lowborn alternatives also remain.
Neither old nor new overlaps are hidden by a preferred-match rule. These
examples require better evidence for distinguishing recurring field values
from fixed diagnostic wording; no phrase-specific fix was installed.

The subsequent random readable review also exposes semantic concerns despite
unchanged successful outcomes: `Trying to <PARAM>` pools several distinct L2
failures; `Malformed`/`Unexpected` become a leading KEY; and `Reason<PARAM>`
absorbs the colon/whitespace for an empty explanation. These were not additional
unknown outcomes, but should not be counted as confirmed formulation improvements.
The current default-literal mechanism is still a hard grouping/alignment/capture
constraint. The owner's proposed field-local presumed-literal interpretation
is investigated with native `:effect` and `:trigger` trace examples in the
follow-up report; it has not been implemented.

Some short culture/innovation formulations remain fragmented under the existing
wording-only similarity threshold. That fragmentation is also present in the
shortcut-removed baseline. The conservative search may miss useful regrouping;
successful coverage of its training messages is not evidence of unseen-log
accuracy or of every template's semantic correctness.

The final model JSON is 139,533,332 bytes, including extensive discovery audit
evidence. This is research overhead, not a proposed runtime loading requirement.
Build time increased from about 81 to 164 seconds. No memory benchmark or
unseen-log generalization claim is made for this change.

## Verification and continuation

Seven native-evidence requirement checks pass. They include 21 independently
inspected expected capture ranges/types rather than asking the production
boundary detector to produce its own expected answer. No synthetic or
recombined CK3 emissions were used.

The comprehensive audit replayed 36,074 captures including wrapper contexts,
reconstructed 23,073 matches exactly from literals and captures, and verified
231,879 proposed hypothesis ranges against original raw-piece and byte offsets.
The narrower before/after capture audit checked 34,692 nonempty ordinary and
component captures. No optional PARAM with only one observed nonempty value
remains in the final candidate. Candidate/source implementation hashes agree.

The next review should inspect the broad/narrow overlaps and short-message
fragmentation, using the saved examples before further inference changes.
The 73-log run, broader/restricted vocabulary comparison and runtime promotion
remain deferred. Model contract, pipeline handoff, inference rules and owner
reference were updated to describe the replacement and its limitations.
