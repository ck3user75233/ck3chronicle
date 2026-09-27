# Full-ID review follow-up — v34

**Follow-up:** the owner approved the one-sweep recommendation. v35 implements
it and the discussed TITLE_FULL_ID extension. See
[the v35 ledger](LEARNER_V35_IMPLEMENTATION.md). The measurements below remain the
historical v34 experiment, not new v35 measurements.

Updated 2026-09-26. Native validation and all-source ablation complete; owner review. No production publication.

## Owner feedback and scope

- `In history for` stays diagnostic wording. The actual v33 character captures
  start at the name, not that introduction. No boundary change is needed.
- `Lowborn of` remains inside the complete character reference. No name parsing
  or additional literal rule is needed.
- Athlone is a county. The same full-ID spelling occurs for multiple title
  ranks; the native inventory below distinguishes them. No new title slot type
  is introduced in this correction.
- Resolve the missing-parent diagnostic-wording defect before proceeding to the
  next outstanding learner item. No sentence-specific template overrides.

## Status ledger

| Step | Status | Evidence |
| --- | --- | --- |
| Inspect actual v33 captures and native examples | Complete | Parent evidence and characterhistory evidence saved under `.codex-tmp/learner-refactor/full-id-followup-v34/`. |
| Identify the damaging inference stage | Complete | Initial inference produces two correct literal formulations; the first region regrouping merges them into three KEYs. `before-stages.json` records the actual stages. |
| Implement general merge correction | Implemented, v34 | `diagnostic_wording.key_run_wording_loss`, consumed at existing merge-check call sites. Policy and engineering rationale are explicit in owner_rules.json. |
| Fresh same-ten/same-thirty complete native builds | Complete | Ten cd757f4a20bd6e9549bff77a; thirty 2b3c6d09c3b753b10cfaa417. No imported templates or manual model edits; production/parser pins unchanged. |
| Inspect improvements, regressions and actual captures | Complete for the correction | In both corpora, only 63 parent assignments change; their two diagnostic phrases remain literal. No other assignment or outcome changes. All 63 produce identical single matches in the active runtime and learner; 6,783 changed-ablation capture values reproduce native byte spans. |
| Complete all-source regrouping ablation | Complete | Same thirty logs, every source: disabled, one original-group sweep, ordinary repeated loop. Other acceptance rules are identical; coverage-absorption calls stay enabled and are instrumented. |
| Change the production regrouping policy | Recommendation only | Retain one original-group sweep; remove repeated reopening. Experiment overrides are not a production implementation of that recommendation. |

Readable evidence: `.codex-tmp/learner-refactor/full-id-followup-v34/REVIEW.html`.
It includes five complete native parent examples, selected ablation effects and
all 106 changed template/outcome groups, with captures and provenance. Every
changed row is retained in the sibling JSON. No synthetic messages were used.

## Results and recommendation

| Region-regrouping arm | Templates | Full outcomes | Provisional outcomes | Unknown |
| --- | ---: | ---: | ---: | ---: |
| Disabled | 537 | 674,619 | 468,445 | 0 |
| One original-group sweep | 458 | 697,334 | 445,730 | 0 |
| Repeated loop | 456 | 697,337 | 445,727 | 0 |

**Recommendation: retain one consolidation sweep, remove repeated reopening.**
This does not assert that every one-sweep generalization is correct. The data
shows useful consolidation, but little demonstrated reason to reopen newly
merged groups repeatedly. Production policy has not yet been switched.

One sweep changes 1,487 contextual rows representing 74,149 occurrences versus
disabled, across eleven sources. Of these, 22,715 become full outcomes. Concrete
effects explain why this is not simply an accuracy count:

- **Useful:** two queued-event identifiers become `Event <KEY> has been queued
  twice with the same data including delay` (538 occurrences).
- **Useful:** three native data-system formulations become `Could not find data
  system function '<KEY>' in '<PARAM>'.` (35 occurrences). Fixed failure wording
  stays intact; actual function identifiers and bounded expressions vary.
- **Supported absence:** 22,061 empty-field occurrences join identifier-bearing
  messages as `Failed to read key reference: <OPTIONAL_KEY>: <OPTIONAL_KEY>, near
  line: <LOCATOR>`. These have actual absence, not malformed braces coerced into
  PARAM. Occurrence totals do not supply independent learning support.
- **Remaining concern:** `Event target` and `List target` become `<KEY> target`
  across 266 occurrences. The values remain captured, but diagnostic category
  wording no longer remains literal. This already happens in one sweep.
- **Substantial type change to inspect:** 50,629 one-token localization-string
  occurrences change from KEY to PARAM when grouped with one native multi-token
  quoted string. The entire bounded value is preserved; the long witness and
  short witnesses are shown together. This has region evidence and is not a
  failed-KEY fallback, but it is not 50,629 additional correct classifications.
- Quoted title names generalize to PARAM without treating internal `of` as a
  template boundary. Rich-text character/name fragments still lack an opaque
  declared structure; new full-ID support does not claim to cover those forms.

**Repetition beyond one sweep changes only five rows / five occurrences**, all
from `jomini_effect_impl.cpp`. Three become full and two were already full.
All concern formatted `had_sex_with_effect` messages with Cheater/With references.
Two additional full outcomes generalize names such as `von Österreich` and
`de Sarvay` into separate KEY captures containing raw formatting suffixes.
Another union changes `root`/`target` from literal wording to KEY and accounts
for the other new full outcome plus the two already-full assignment changes.
There is some further name variation recognized, but no convincing clean
reference-field or diagnostic-quality gain from the repetition. The report
shows all five, rather than claiming repetition is uniformly harmful or useful.

The v34 guard itself changes only the 63 missing-parent assignments versus v33
in both ten and thirty logs: 310 → 311 and 455 → 456 templates respectively,
with every outcome unchanged. This closes the demonstrated three-KEY phrase
loss. Single-word diagnostic loss and coverage-only merge authority remain
open; this repair does not solve the whole merge architecture.

## Regrouping comparison scope

The earlier v32 experiment covered only five sources and found mixed benefit and
harm. It did not justify keeping or deleting regrouping across the full corpus.
The owner now directs the complete comparison before the next learner item.

All three new arms use v34, including the same full-ID declarations and new
wording-loss guard. The enabled arm is the ordinary fresh thirty-log build.
Disabled and single-sweep arms use the same complete raw evidence (38,584
distinct messages / 38,621 contextual rows / 1,143,064 occurrences, all 113
sources). They import no templates. Their overrides exist only in the research
process and cannot change production selection.

Both calls to the distinct complete-match coverage-absorption routine remain
enabled, and their before/after memberships are recorded. This is a controlled
test of region regrouping and its repetition, not a claim that every kind of
group consolidation has been disabled. Single-sweep permits disjoint original
groups to merge but never reopens a newly merged group within that sweep.

The acceptance criteria are actual native diagnostic wording, typed fields,
capture boundaries and competing matches. Fewer templates, more full matches,
or a shorter run are reported measurements, not automatic correctness judgments.

## Confirmed cause

The thirty-log v33 learner first discovers:

```text
Parent ((no character)) of <CHARACTER_FULL_ID> is hasn't been born at file: <LOCATOR> line: <LOCATOR>
Parent ((no character)) of <CHARACTER_FULL_ID> is the wrong gender at file: <LOCATOR> line: <LOCATOR>
```

The first has 42 distinct messages; the second 21. They remain separate through
same-wording consolidation and the first complete-coverage reconsideration.
`refine_region_groups` then replaces them with:

```text
Parent ((no character)) of <CHARACTER_FULL_ID> is <KEY> <KEY> <KEY> at file: <LOCATOR> line: <LOCATOR>
```

The inferred values are exactly `hasn't` / `the`, `been` / `wrong`, and
`born` / `gender`. Whitespace alignment divides the phrases into three variable
positions; each passes KEY syntax. Existing established-wording guards inspect
loss to PARAM, so this KEY route bypasses them. The bug is in inference/merging,
not raw tokenization or the new character-field boundaries. Sixty-three native
occurrences match the defective template; 61 changed outcome from provisional
to full in v33 and two were already full.

## Correction being evaluated

Before accepting a merge, check whether it replaces an independently established
literal word sequence with adjacent KEY/OPTIONAL_KEY slots separated only by
whitespace. Reject that proposed merge and retain the previous formulations.

The prior template must already have variation in a non-location field. Only
complete alphabetic raw tokens outside all prior captures count. At least two
words must be swallowed into different adjacent KEY slots. This minimum defines
a word sequence; it is an engineering choice under the repair authorization,
not an owner-prescribed threshold or proof of linguistic meaning.

The check does not use failure-word lists, force initially observed words to
remain literal, prohibit all adjacent KEYs, parse names, or change supported
PARAMs. Words already inside full-ID fields, locators, traces and other slots
cannot trigger it. The existing listed-wording PARAM check remains separate.

This is conservative evidence for retaining existing formulations, not permanent
freezing against future counterevidence. No new automatic counterevidence
mechanism or unrelated merge rewrite is claimed here.

## Native title-format inventory

Across the existing 73 complete native logs, the populated `Internal Key`
format occurs 337 times: 286 county keys, 36 barony keys, nine duchy keys and
six kingdom keys. These are observed key-prefix categories, not a whitelist of
title values. Sources:

| Source | County | Barony | Duchy | Kingdom |
| --- | ---: | ---: | ---: | ---: |
| `pdx_assert.cpp` | 2 | 0 | 0 | 0 |
| `succession_order.cpp` | 34 | 36 | 4 | 0 |
| `jomini_script_system.cpp` | 250 | 0 | 5 | 6 |

The two assertion examples are Athlone (`c_athlone`) and Lübeck (`c_lubeck`).
Other actual names include Ahnais (`b_ahnas`), Haute-Égypte (`d_al-said`),
Amorios Family (`d_nf_amorios`) and Arwastan (`k_jazira`). House records with an
empty Internal Key are the twelve separately recognized HOUSE_FULL_ID cases.

A general TITLE_FULL_ID would fit this common formatter more accurately than
calling all these objects COUNTY_FULL_ID. Recognition would still require
explicit emitter/start boundaries and the balanced ID ending, with the interior
opaque. That extension remains a recommendation for review; the implemented
change here addresses the diagnostic-wording defect.
