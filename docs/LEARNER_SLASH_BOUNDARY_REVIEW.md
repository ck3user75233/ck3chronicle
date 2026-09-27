# Slash boundaries and learner path ranges — 2026-09-21

The owner corrected the raw boundary: `/` is a standalone punctuation token,
even with no intervening whitespace. The learner recognizes a path from the
adjacent sequence; the parser does not turn that sequence into a semantic slot.

## Subsequent filename clarification

Windows permits ! in filename content, including at the beginning, internally,
and immediately before the extension. See [Microsoft's naming conventions](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file).
The prior per-segment split was a parser defect, not a special filename rule.

Parser v1.3 also corrects the bare-name case: !!0_TFE_chars.txt is one token,
just as fi!le.txt and file!.txt are. A slash remains a separate token; error!
still has sentence-final punctuation separated. A standalone ! is unchanged.
The reference records the owner's authority and the filename documentation.
The ten-log native evidence contains eleven occurrences of
history/characters/!!0_TFE_chars.txt and no observed bare ! filename. Explicit
owner filename probes therefore verify the bare form without presenting it as
a native emission. The same ten complete logs reconstruct exactly under v1.3, and all 8,249
prior path ranges plus 8,282 candidate captures pass. Candidate
d195b4944aeeb10cccfec51e retains ten ambiguous occurrences and zero unknowns.
It also includes the separately owner-approved wiki vocabulary update, so it
is not an isolated parser-only comparison. Current v1.3 verification is recorded in CURRENT_HANDOFF;
the v1.2 results below remain the completed slash-correction checkpoint.

## Delivered slash change (v1.2 checkpoint)

Selected parser: `ck3-lossless-v1.2`, SHA-256
`5f23b0c533ed1183f990b66156cd7b79dbb0f213d2d6a62e8415d2329ca47943`.

The raw pieces for an actual native dynasty path are:

```text
"common" | "/" | "dynasties" | "/" | "00_bgp_dynasties.txt:6"
```

The separators above mark piece boundaries, not added whitespace. Each piece
keeps its original byte span. The LOCATOR capture covers all five pieces.
The :6 suffix is present in this native example; it is neither required nor
appended to other paths. Separately labelled line values remain separate fields.

Splitting slashes preserves other internal punctuation. The native path
`history/characters/!!0_TFE_chars.txt` ends in one segment `!!0_TFE_chars.txt`.
Its leading exclamation marks do not become separate template literals merely
because a slash precedes that segment. Dotted keys and adjoining @ are preserved.

The learner identifies ranges from adjacent segments/slashes plus location
context or filename syntax. There is no folder or extension allowlist. Default
words inside recognized paths are excluded from literal anchors. LOCATOR now
uses `location_value` instead of `single_token`: it accepts a complete adjacent
path range or one labelled non-punctuation value. It cannot consume surrounding
quotes/brackets, spaces, or following trace fields.

Candidate retrieval, similarity and alignment use the same recognized location
ranges, so shared folder spellings and path depth do not drive formulation
grouping. The range refers back to existing pieces; no alternate tokenization,
rewritten message, or hidden word deletion is introduced. Source boundaries and
independent L1/L2 learning remain unchanged. `Div/0`, `tooltip/description`,
`yes/no` and `Invalid/missing` demonstrate why adjacent slashes alone do not
establish a filesystem location in every message context.

## Native verification

All ten previously selected complete logs were freshly parsed; old feature caches
were not reused. All 91,407,302 input bytes reconstruct exactly. Emission counts
remain 343,585 and recovered-message counts remain 352,317. Every slash is a
separate piece (1,092,019 body-piece occurrences); original ordered byte spans
and message counts passed checks on every log.

The final candidate is `21658012c3f44bbc5f09716b`, using the current 18 explicitly
owner-supplied symbol spellings. It contains 297 ordinary and 368 component
patterns. Outcomes:

| Outcome | Occurrences |
|---|---:|
| Full ordinary match | 140,442 |
| L1+L2 complete match | 211,865 |
| Ambiguous | 10 |
| Unknown / partial / L1-only | 0 |

Relative to the previous restricted-vocabulary ten-log build, 34 formerly
ambiguous occurrences become complete matches, five complete matches become
ambiguous, and five remain ambiguous. This is a net reduction from 39 to 10,
not an assertion that no regression occurred. The vocabulary also now contains
the explicitly supplied trait type, so this is not an isolated slash-only
accuracy experiment. The five newly ambiguous occurrences are script-system
L2 or trace overlaps; remaining examples and every competing template are saved.
No candidate was promoted and no registry selection was changed.

The final capture audit checks 8,282 matching-candidate path captures with zero
failures. An independent cross-version check preserves all 8,249 prior captured
path ranges, including complete filenames with punctuation. It also verifies
that default words inside locations are not literal anchors: 126,272 path
occurrences contain such words. These checks cover the saved native corpus;
they are not a claim that every possible CK3 path presentation is supported.

The first intermediate rebuild exposed path-depth influence on grouping and
increased ambiguities to 976. Range-based grouping corrected it. A subsequent
native review caught the !! filename boundary issue, corrected before the final
build. Intermediate bundles are research history, not versions to integrate.

## Evidence and handoff

Artifacts are under `.codex-tmp/learner-refactor/symbol-location-review/slash-final/`:
`raw-checks.json`, `path-capture-checks.json`, `comparison.json`, `summary.json`,
and the immutable revision bundle. `comparison.json` includes full native text,
actual raw pieces, captures, occurrences and the remaining competing templates.
Current source hashes match the final model's implementation snapshot.

Consumers must explicitly select the new parser and regenerate features. The
[model contract](LEARNER_NATIVE_MODEL_CONTRACT.md) and
[pipeline handoff](LEARNER_PARSER_PIPELINE_HANDOFF.md) describe range captures and
the new constraint. Pipeline caller refactoring remains with that team. No
73-log rerun was started. Broader symbol-type evidence and the requested valid
expanded-versus-restricted vocabulary comparison remain separate outstanding work.

## Spaced slash/list check — owner follow-up

The owner noted that provinces / baronies ordinarily denotes alternatives when
there are no other path signals. The current parser preserves the two spaces as
gaps around a separate slash token. Path range recognition stops at gaps and
also requires location context or filename syntax. It does not join that phrase
into a LOCATOR. Explicit probes of the owner's phrase, both one-sided spacing
variants, and provinces/baronies all remain literal formulations without a
location context. These probes are owner examples, not native log emissions.

The current ten-log candidate's 352,317 messages contain no whitespace-adjacent
slash. A read-only search of all 2,594,601 occurrences in the saved 73-log corpus
also found none. Therefore there is no native spaced-slash example to cite from
this corpus; no training was restarted to obtain that result.

Actual unspaced non-path expressions in the ten-log run are Div/0 (1,628),
tooltip/description (730), yes/no (18), Invalid/missing (9), else/else_if (8),
and ai_check_interval'/'ai_check_interval_by_tier (10). Every candidate capture
overlapping these non-location sequences was
checked: none was a LOCATOR. This confirms that slash occurrence alone is not
being used as path identity in these cases. No parser/inference change was
needed for the owner's spaced example.

Evidence: .codex-tmp/learner-refactor/symbol-location-review/slash-list-checks.json
and slash-list-corpus-checks.json. The latter is a read-only corpus search, not
a new 73-log training exercise.
