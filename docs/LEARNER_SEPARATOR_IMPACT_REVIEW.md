# Fresh learner run with parser v1.6

2026-09-21. Candidate `e375ae7fb4cf74bcdef446ec`, not promoted.

The current learner was rebuilt from the same ten complete native logs as
candidate `255eecc2dd7965207c58b0da`, using freshly parsed v1.6 pieces throughout.
All ten logs entered the accumulated learning pool: 343,585 emissions,
352,317 recovered messages, 7,827 distinct source/message pairs and 93 sources.
Source partitioning, independent L1/L2 inference, literal guidance, range-based
locations, tighter grouping and parser-boundary matching were all active.

No synthetic inputs, prior feature caches or new inference rules were used.
The implementation hashes of the learner Python modules match the baseline.
Effective literal guidance is identical; the owner-rule reference changes only
its architectural-authority descriptions. This comparison therefore measures
the effect of the new raw tokenization on the current learner.

## Results on the same training evidence

| Outcome | Before, v1.5 | After, v1.6 |
| --- | ---: | ---: |
| One complete ordinary match | 140,442 | 140,443 |
| One complete L1/L2 composition | 211,865 | 211,872 |
| Ambiguous | 10 | 2 |
| Unknown | 0 | 0 |
| Partial / L1-only | 0 | 0 |

Eight formerly ambiguous occurrences now have one complete match: seven script
system errors and one character-history error. No previously complete outcome
became ambiguous, partial or unknown. Both remaining ambiguities already existed.
All evidence rows were compared by source, exact original message and exact
context text; context hashes were not assumed stable across tokenizations.

The capture check verified 34,476 nonempty ordinary/component captures against
the original bytes and new raw-piece boundaries. No capture check failed.
The native exports retain every occurrence; comparisons include 7,864 distinct
message/context rows. This is a same-training-corpus result, not unseen accuracy.

## Concrete effects

One script-system L2 previously captured complete `ONCLICK:` and `TOOLTIP:`
fields through KEY slots. Their colons and prefixes now remain literal, while
the variable values have their own captures. A redundant exact-message candidate
no longer overlaps the generalized candidate for that observed message.

Native negative localization hash values now occupy one signed VALUE capture;
the minus sign is no longer a separate template literal. Filenames, line ranges
and path separators retain their exact values and boundaries.

The remaining two ambiguous messages are in `characterhistory.cpp`: a parent
with the wrong gender, and a parent who has not been born. Both match a pattern
with literal `Lowborn` and another with a second KEY capturing that word.
These alternatives are preserved in the review. No preferred-match suppression
or new literal override was introduced.

## Generalization concern exposed by the corrected parse

More detailed boundaries do not automatically produce better grouping:

| Candidate kind | Before | After |
| --- | ---: | ---: |
| Ordinary templates | 300 | 374 |
| L1 | 188 | 188 |
| L2 | 134 | 130 |
| Trace tails | 47 | 97 |
| Other composition framing | 5 | 5 |

The learner requires matching punctuation-anchor signatures when forming a
group. Ordinary messages include their trace text in that signature. Newly
visible colon/bracket differences in the trace therefore split otherwise
similar diagnostic wording into smaller learning groups.

Concrete native case, source `jomini_scriptvalue.h`: the 18 distinct messages
beginning `Badly read script value` previously supported one template. They now
support four, separated by their trace punctuation:

- Fifteen natural-disaster messages still support a KEY in the script-value
  position and share one trace shape.
- The message containing `@cultural_maa_extra_ai_score` occurs ten times but is
  one distinct message in its new group. Its key and trace spelling become fixed
  text in that candidate. The raw parser still retains the complete @ symbol.
- Two messages containing `0.333333` have different trace depths and now produce
  two separate candidates with the number and trace text fixed.

The native traces include `persian_paighan:ai_quality:value`,
`natural_disaster_5001_effect:change_development_level`, and the two
`mlgdc_cap_value[args#4128741568]:value:add:multiply` traces, one followed by
`:subtract`. Their complete messages, raw pieces, anchor signatures and learned
captures are in `script-value-grouping-review.json` beside the comparison.

This confirms that trace punctuation affects ordinary diagnostic grouping. It
does not measure failure on an unseen log. The next learner work should examine
how to keep supported trace structure from unnecessarily fragmenting diagnostic
learning while preserving every delimiter and raw range. Do not undo the parser
boundaries, merge punctuation into KEY values, force an example-specific slot,
or reintroduce discarded preprocessing.

## Inspectable artifacts and next work

Results are under `.codex-tmp/learner-refactor/separator-learner-review/`:

- [48 before/after native cases](../.codex-tmp/learner-refactor/separator-learner-review/NATIVE_COMPARISON.md),
  including all changed outcomes and both remaining ambiguities.
- `comparison.json`: all 2,628 rows whose matching templates or captures changed,
  representing 161,135 occurrences; original pieces, captures and provenance.
- `visual-review.json`: refreshed top-20 ordinary/L1/L2 support rankings and both
  ambiguity groups, with 135 actual supporting examples. The older HTML viewer
  has not been replaced by this dataset export.
- `candidate/e375ae7fb4cf74bcdef446ec/`: immutable hash-verified bundle, exact
  parser, model, full native evidence and reproduction command.

The run and comparison are complete. No 73-log run, registry change, confirmation
or model promotion was performed. Remaining work is the trace/grouping concern,
the two Lowborn overlaps, and the separately requested broader-versus-restricted
symbol-literal comparison. Parser-provided lexical-category metadata remains a
separate proposed cleanup, not part of this run.
