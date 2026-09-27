# Continuation-aware model integration — v41

Owner authorized completing parser v1.7 continuation support before publishing
the next model. v40 with parser v1.6 remains the comparison baseline.

- [x] Read parser delivery and current learner/runtime interfaces.
- [x] Preserve complete ordered groups in versioned learner records.
- [x] Declare the repeated title component in owner JSON; learn opening wording.
- [x] Carry component structure through schema, export, selection and runtime.
- [x] Inspect every native affected group on complete logs, including both list lengths.
- [x] Rebuild the same thirty-log corpus and compare unaffected messages with v40.
- [x] Verify compact export and independent runtime loading/matching/binding.
- [x] Publish/pin the new immutable release and update the existing formal handoff.

The entry grammar is one repeated reference to the opening CHARACTER_FULL_ID,
the native label, and a displayed-title PARAM. The parser supplies component
ranges; neither matcher repeats parser recovery nor infers names. Actual entry
presentation literals are retained. Unknown structural variants remain explicit.
An opening-only match cannot classify a complete group. Supporting entries are
not independent diagnostics or templates. Complete ordered contents determine
learning-record identity; headers and absolute ranges belong to occurrence
provenance. The new contract must work in both matching routes before publication.

No SQL migration, watcher activation, synthetic logs, name dictionary or new
regrouping pass is part of this work.

## Implemented contract

Feature v4 keeps opening text/pieces plus ordered continuation bodies and their
relative prefix/label/value ranges. Complete record identity includes the entries;
absolute component spans and every contributing emission ordinal are retained on
each occurrence. The parser artifact remains unchanged.

Model schema 4 adds `continuation` (null for ordinary templates). A declared
component contract references the opening CHARACTER_FULL_ID slot, retains native
leading/label/trailing literals, and accepts one or more ordered entries. Each
entry captures the matching reference and the displayed title as PARAM. The
declaration is in owner_rules.json; list length and title words are not diagnostic
grouping evidence. The parser's label excludes preceding possessive framing;
the model retains that framing as part of the literal between captures.

The release includes hash-covered standalone assignment.py and continuations.py.
Assignment policy v2 carries component captures alongside body/wrapper captures.
The runtime reader validates schema/declarations/artifacts; classifier v7 uses the
release selector and component matcher, exposes one selected assignment for both
supported and provisional outcomes, and binds each component to its own body.
All complete capture alternatives are supplied to selection. Earlier schema
releases are not silently adapted by the updated reader.

## Demonstrated on both affected complete native logs

Two-log research build: 206 templates, 133 supported / 73 provisional. All 100,621
complete diagnostic occurrences replay through the independent runtime route:
64,143 supported, 36,478 provisional, zero unknown. Learner and runtime agree on
every selected template and capture; 192,850 bound values were compared against
original bytes. All 11 groups / 13 title entries are represented, including the
repeated complete error in the second log and both two-entry groups. All groups
use one supported opening-plus-repeatable-entry formulation:

```text
<CHARACTER_FULL_ID> should hold at least one landed title (barony or county) but doesn't has any:
    <same CHARACTER_FULL_ID>'s title: <PARAM>   [one or more entries]
```

The indentation and repeat annotation above explain the model; they are not
inserted into native text. Character references, title spelling, leading spacing
and CRLF bytes remain intact. This confirms the delivered component mechanism,
not correctness of all other inferred templates. Native malformed/missing-list
variants remain unobserved in the census.

## Thirty-log comparison

Candidate `007d011659a02de3c965a9cd`, rebuilt from the same thirty logs without
template imports. All 1,143,044 unaffected occurrences / 38,601 contextual rows
retain their v40 selected template, support outcome and captures. The affected
twenty formerly separate messages are nine complete groups with eleven entries.
Seven old formulations (one opening and six title-line variants) become one
opening-plus-entry contract; supporting title words no longer fragment templates.

| Measure | v40 / parser 1.6 | v41 / parser 1.7 |
| --- | ---: | ---: |
| Templates | 424 | 418 |
| Supported / provisional templates | 236 / 188 | 232 / 186 |
| Complete diagnostic occurrences | 1,143,064 | 1,143,053 |
| Supported assignments | 697,680 | 697,671 |
| Provisional assignments | 445,384 | 445,382 |
| Unknown | 0 | 0 |

The smaller message/assignment counts reflect correct grouping, not discarded
evidence or losses of matches. All nine groups use supported template
`0875e8c46afb0b47271a8341`. Compact export passes full native replay and the
independent schema-4 reader loads research release `76630685c4a341ca14bf9c7c`.
The complete runtime replay subsequently passed and publication is complete below.

## Published delivery

Published/pinned **76630685c4a341ca14bf9c7c**, parser **ck3-lossless-v1.7**.
Manifest SHA-256: `364215904d0b167b94365cb6b666818db15cc1947778acf6511772b9e12943c0`.
The existing formal handoff contains schema-4, assignment-v2 and classifier-v7
interfaces. No production ingestion was run.

Independent runtime replay matches every learner assignment across 1,143,053
occurrences / 38,610 contextual rows, checking 4,429,930 absolute bindings.
The final thirty-log model also matches the two repeated groups in the second
affected log, which was not trained on. That entire log has 14,600 supported,
359 provisional and 9,153 unknown occurrences. The v40 template/parser/selector
comparison (unchanged pattern mechanics) has the same supported/provisional
counts and 9,155 unknowns: the two extra unknowns were separate supporting-title
entries. No broadened accuracy claim is made. The largest pre-existing unknown
is the `untyped effect` formulation with `Script location: Unknown` (8,880
occurrences); this remains a separate coverage issue.

Evidence under `.codex-tmp/learner-refactor/continuations-v41/`: comparison-30.json,
30-runtime.json, affected-runtime.json, additional-affected-log.json,
additional-affected-v40.json, and readable REVIEW.html. All existing opening and
entry bytes remain available; component-relative captures bind to their original
bodies and never to concatenated display offsets.

Wheel packaging also passed: all release hashes agree with packaged bytes, and
an isolated Python process loaded the wheel's runtime/model/parser/helpers and
classified all eleven native groups/thirteen entries with exact bindings. The
published selected route also exposes complete components on research candidate
alternatives, alongside its single selected assignment. No SQL processing or
application lifecycle was invoked for these checks.
