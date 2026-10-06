# Task 08C — Source reading, playset scope and error-analysis beta

Prepared 2026-10-04 for the Data Intelligence team. This is the next assignment
prompt; preparation does not execute it. Receive ongoing 08B corrections before
editing shared files. Extend the owning services rather than creating another
parser, search implementation or standalone report generator.

## Outcome and starting point

Deliver flexible source-text reading, centrally enforced playset search scope,
configurable default folder exclusions, and a reusable error-analysis beta that
the owner can give to agents and rerun against later stored Runs.

Read root/applicable `AGENTS.md`, `docs/DEVELOPMENT_ENVIRONMENT.md`, current openings
of plan/status/handoff, and the current sections of
[08B's handoff](TASK08B_REPORTING_HANDOFF.md),
[08A.2's handoff](TASK08A_2_SOURCE_SEARCH_HANDOFF.md) and
[reporting decisions](TASK08_SCOPE_REVIEW.md). Inspect `reporting/source_search.py`,
`source_query.py`, `analysis.py`, `presets.py`, CLI and presentation callers.

Receiving review found:

- 08B's latest checklist reports **no known unfinished assigned feature or
  documentation work**. Its earlier open-item lists are historical, not a new
  backlog. This review inspected the handoff/source; it did not rerun its checks.
- Carry forward two unexercised fault groups: database-handler operation/transport
  failures and ripgrep launch/error exits. Separately retain inspection limits for
  disappearing/changing Runs, unexpected/double-error caller paths and unreadable
  files. These are not all the same outcome, nor instructions to fabricate failures
  or rebuild delivered handling.
- `_encoding` currently accepts UTF-8 and BOM-marked UTF-16; this describes an
  implementation limitation, not an owner instruction to restrict encodings.
  Content search independently uses ripgrep's automatic encoding.
- Caller-supplied roots (`--source-root`, source context or structured selection)
  can bypass the recorded playset. Default report scope still uses that playset.
  Earlier 08A.2/08B prompts expressly allowed the explicit-root feature; the owner's
  new playset-bound requirement supersedes it for the source operations in this task.
- Every normal `report` constructs a source resolver with candidate context enabled.
  It resolves references for all qualifying diagnostics in selected/comparison Runs
  before applying display limits. “Optional” means supplementary context, not a
  user opt-in. Correct this excess enrichment below. These are source observations,
  not an executed workload measurement or proof that all installed mods are scanned.
- Source inventories/resolutions are built during investigation and cached in memory,
  with caches cleared for a new investigation. Results can be included in exported
  reports, but there is no reusable persisted resolution cache or source-candidate
  SQL-population route in the inspected callers. Preserve the no-database-write
  boundary; this task does not commission a persistent source index.

## 1. Encoding: investigate, obtain direction, then implement

Determine practical support for commonly readable encodings in CK3/game/mod
`.txt` and `.yml` text. CK3 warnings or apparent parse failures do not define our
readability policy: the owner observes that CK3 warns about missing UTF-8 BOMs
while still reading those files. Do not reject otherwise readable text on that
basis or claim precise knowledge of CK3's encoding acceptance. Double-BOM and
suspected mojibake findings require their specifically directed treatment and
honest evidence limits; they are not a general license to reject warned-about
files. Do not turn the illustrative “90% of software” wording into a numerical
acceptance threshold or claim universal detection.

The subsequent approved decoder design and staged implementation are recorded in
[the current API document](TASK08C_ENCODING_RECOMMENDATION.md) and the opening of
[the handoff](TASK08C_HANDOFF.md). Those supersede the original encoding decision
request below; this wording correction does not reopen approved implementation.

Use current primary library documentation and representative genuine files inside
the relevant playset. Evaluate maintained libraries, including `charset-normalizer`,
instead of designing a detector. Address Unicode/BOM handling, common Windows and
Latin code pages, relevant East Asian encodings, ambiguous/short/ASCII-heavy input,
malformed or mixed bytes, performance and dependency/licensing implications.
Library codec support alone is not proof of reliable detection on every file.

Present a concise recommendation in `docs/TASK08C_ENCODING_RECOMMENDATION.md`:
supported behavior, library choice, detection/decoding policy, uncertainty/failure
presentation, and how searching and excerpts will read the **same text**. Explain
how the selected decoding reaches the content-search backend; changing only
`_encoding` while leaving ripgrep on incompatible auto-detection is insufficient.
Recommend treatment of ambiguous files and any explicit override, if needed.

**Obtain owner direction before implementing the encoding choice.** Continue
independent scope/filter/report work while that decision is pending. Then implement
the directed behavior in one reusable source-reading boundary. Do not rewrite
source files, silently discard undecodable bytes, or label an unsupported encoding
as corruption. Preserve useful per-file outcomes and identify unsearched content.

Starting references: [supported encodings](https://charset-normalizer.readthedocs.io/en/latest/user/support.html),
[detection guidance](https://charset-normalizer.readthedocs.io/en/latest/community/faq.html),
[result interpretation](https://charset-normalizer.readthedocs.io/en/latest/user/handling_result.html).
The documentation describes broad codec support but also absent/ambiguous results;
the recommendation must resolve their product treatment rather than conceal them.

## 2. One playset-bounded enumeration and filtering path

For every diagnostic source lookup, file/content search, source validation,
informational filename search and excerpt read, the maximum scope is the relevant
Run's recorded playset roots. An unfiltered search traverses every available member
recursively, subject to the configured exclusions below. Historical Runs use their
own recorded playsets, not today's active mods.

- Reuse/extend `SourceSearch`'s in-memory playset access and inventories into a
  straightforward reusable member/path enumerator. All callers use the same scope
  and filtering behavior. No parallel index, persistent source cache or new database.
- Explicit roots, directories and files may narrow that playset boundary; they
  must not expand it. Supersede older 08A/08B permissions and examples allowing
  outside-playset roots, including old verification expectations. Reject an attempted
  expansion clearly. Missing playsets
  or roots remain unavailable; never substitute all installed mods, workshop
  directories, sibling mods or filesystem discovery.
- Enforce containment for actual file access, including absolute references,
  traversal components and links/junctions that would escape the selected roots.
  A lexical prefix check alone does not establish containment. Keep legitimate
  recorded-member associations when roots overlap or repeat.
- Represent folder/file include/exclude policy as declarative rules and use one
  generic evaluator. No scattered `if gui`, `if gfx`, etc. branches. Apply directory
  pruning before traversal where possible, rather than scan everything then filter.
- Ensure inventory/content caches respect effective scope, exclusions and decoding
  policy. A prior broad search must not leak excluded paths into a later request.

## 3. Default folder exclusions

Add configuration toggles, applied independently beneath **every playset member's
root** when the caller has supplied no narrowing path scope. No NiceGUI work now.

| Member-relative folder | Default | Effect when SKIP |
|---|---|---|
| `gui` | INCLUDE | Exclude this folder and its descendants |
| `gfx` | SKIP | Exclude this folder and its descendants |
| `map_data` | SKIP | Exclude files directly in this folder; keep `map_data/geographical_regions` searchable |
| `tools` | SKIP | Exclude this folder and its descendants |
| `music` | SKIP | Exclude this folder and its descendants |
| `fonts` | SKIP | Exclude this folder and its descendants |
| `sound` | SKIP | Exclude this folder and its descendants |

The owner clarified that `geographical_regions` is the child folder at issue;
do not broaden the `map_data` rule into a blanket recursive exclusion.

Apply these defaults inside both search and source-validation services. A caller
must not remember to apply them. Selecting members, extensions or a bare filename
does not itself narrow the directory scope. A caller's explicit relative directory
or file-path selection takes precedence within that selected path; it still cannot
escape the playset. Internally deriving a parent directory from a diagnostic
LOCATOR does not count as a user-supplied override of the defaults.

Return the effective policy and excluded member-relative scopes in structured
results and human reports. Distinguish **excluded by configuration**, **not
requested**, **file not found after completed lookup**, and **unavailable/error**.
Exclusion must not silently become a missing-file finding. Required filters that
cannot be decided must retain honest coverage rather than manufacture a nonmatch.

## 4. Complete searches without unnecessary enrichment

All requested searches must complete over their effective scope and retain every
match; never stop at the first matching file/member. Display limits are not search
limits. Preserve existing search counts and coverage disclosures.

Separate optional source enrichment from selection/ranking:

- Compute ordinary diagnostic counts and rankings from stored records first.
  Resolve candidates and read excerpts only for the displayed/requested detail
  set. Do not follow every LOCATOR in every diagnostic/history record merely to
  produce a bounded standard report, or persist those resolutions to SQL.
- When a caller explicitly requests source-dependent filtering, resolution checks
  or source-association analytics, perform the complete source work necessary for
  that request. Do not apply top-N first and thereby alter membership or totals.
  State what was inspected versus left unenriched.
- Pathless emissions remain valid complete records; do not perform source lookup
  or invent a warning for absent LOCATORs.

For literal source-content searches, retain occurrences inside longer tokens and
label them as substring matches where relevant. Do not silently turn an exact-token
predicate into substring membership. Prefer existing literal/grouped predicates;
if additional informational matching is impractical, explain the concrete tradeoff
to the owner before omitting it. No fuzzy-search engine is requested.

## 5. Agent-ready error-analysis beta

Build on the existing query, analysis and report services. Deliver one documented
root-CLI route using a selected stored Run, repeatable on later Runs, with readable
offline HTML/text and equivalent structured JSON. Do not parse raw logs again.

Initial presentation follows the owner's supplied file-ranking example:

- **Top 20 script-system referenced files**, ranked by occurrence count, with the
  contributing distinct diagnostics, messages and referenced lines beneath each.
- **Top 5 non-script-system diagnostics**, ranked by occurrence count.
- **Top 5 syntax diagnostics**, using researched, package/model-appropriate selectors.

The first section's file-based grouping is a drafting assumption, not a settled
interpretation of “top errors”; receive any owner correction before implementing it.
Determine script-system selection from actual stored emitter/source-family values
and document it. Reuse the current syntax
research; do not silently apply old-package template IDs to a newer model. If the
selected lineage lacks established selectors, disclose that limit and present the
bounded work needed rather than invent syntax classifications or return false zeroes.

Show Run/playset identity, actual section predicates, occurrence/distinct-record
totals, display bounds, source exclusions/coverage and usable links to details.
Compute totals before display limits. File copies in different members must not
multiply diagnostic counts. Disclose overlapping categories or multi-path buckets;
retain pathless script diagnostics in totals with an explicit ungrouped count.

For requested source detail:

- List every exact relative-path candidate across the allowed playset scope, with
  member/mod name, numeric load order, path and line. Preserve the current owner's
  **last matching load-order member is the Error source for each file/line** rule,
  its stated unavailable cases and the complete list of copies. Content filtering
  must not promote an earlier copy into the source.
- Also list informational near-name files in the **same relative parent directory**
  across playset members: e.g. `foo.txt` may suggest `foo_upgraded.txt` and
  `fix_foo.txt`. Use a clear literal basename/stem relationship and preserve extension
  meaning; do not search unrelated directories or introduce fuzzy guesses. Label
  these separately from exact source candidates. They must not establish resolution,
  change Error source attribution, or acquire the diagnostic's occurrence counts.
- Reuse the existing optional excerpt support, with the selected decoding policy.
  State that files are current at reading time, not a historical source snapshot.

Reuse existing history comparisons so agents can inspect actual counts on subsequent
Runs; do not infer that a patch worked merely because a report changed. The historical
example expresses the desired usefulness. Automatic patch recommendations, file diffs,
and broader causal blame are not additional deliverables for this beta.

## Verification and delivery

Use genuine stored CK3 records through `HandlerClient`, current playset source files
and proportionate root-CLI checks. Observe scope/enrichment behavior for real queries,
including that excluded/outside paths are not searched and displayed detail does not
trigger whole-history enrichment. Verify relevant HTML/text/JSON and browser layout
using available tooling. Reuse valid 08B evidence; do not repeat unchanged campaigns.

**Creation or execution of each synthetic test requires explicit owner approval for
that specific test.** The 2026-10-04 exception covers only the specified two genuine
emissions with fake LOCATOR paths, normal captured playset and normal-writer hashes;
keep its results labelled synthetic and separate from genuine history acceptance.
It does not authorize fabricated encodings, fake folders, mock clients, fault
injection or synthetic histories for 08C. Unrepresented cases remain unverified.

Run the required runtime logging ownership check for runtime changes and relevant
dependency/package checks if a library is added. Report failed attempts, actual
checks, inherited evidence and limits separately. Preserve the public handler,
stored identities/counts, shared logging ownership and read-only sources.

Deliver the encoding recommendation/owner disposition, owning-component changes,
concise configuration/CLI examples, representative genuine beta exports outside Git,
and `docs/TASK08C_HANDOFF.md` listing delivered work and any open decisions/follow-ups.
Update only affected guidance/current pointers; keep the 08B evidence historical.
No NiceGUI, Trekker implementation, model retraining/promotion, database schema or
candidate-persistence work, service restart, production mutation, commit or push.
