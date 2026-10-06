# Combined learner / decoder release

**Database replacement complete — 2026-10-05.** Production now has 31 freshly
ingested Runs under the new model: the 30 retained captures plus the session just
closed. The former database exists only in backup; no Run rows were migrated.
The natural live lifecycle and current reports are verified. See the
[replacement receipt](PIPELINE_RECEIVING.md#database-replacement-complete--2026-10-05)
and [current operational record](PIPELINE_CUTOVER.md). Older pending/held statements
below are historical.

**Production activated — 2026-10-05 09:57:58 UTC.** The owner-authorized cutover
uses the final R3 wheel and package `4ac4e8ee92346e6d14eacfbf`; no rollback.
See the [activation receipt](PIPELINE_RECEIVING.md#production-activated--2026-10-05)
and [cutover record](PIPELINE_CUTOVER.md). Existing database/Runs/evidence are
preserved. New-package live ingestion/lifecycle remains pending the next natural
unique capture; Pipeline retains the follow-up. R4 remains Reporting-owned.
Prior held/ready statements below are historical and superseded by this activation.

Updated 2026-10-05. **READY FOR OWNER ACTIVATION DECISION; activation held. R3 CLOSED.**
The new application wheel contains a valid shipped default; no corrective
post-install selection replacement is required. See the
[R3 packaging receipt](PIPELINE_RECEIVING.md#r3-packaging-closed--2026-10-05)
and [final cutover](PIPELINE_CUTOVER.md). Final wheel:
`.codex-tmp/pipeline-r3-packaging-20261005/application/ck3chronicle-0.0.1-py3-none-any.whl`, SHA-256
`7239a0c5b89e52f2df1d31028bdbf21b086e3600bf7c079347a1ee4f1d982959`; clean staged environment:
`.codex-tmp/pipeline-r3-packaging-20261005/deployment`.
Default loading from `C:\Windows` and installed rollback pass. Application bytes
are unchanged, so the independent R1/R2/R5 genuine receiving results are reused.
R4 syntax remains separately owned Reporting work. Keep the production database;
live configuration and retained distributions are unchanged. No activation occurred.
Earlier artifact/override statements below are historical where superseded.

The final reference model is the ordinary empirically learned model/runtime
package `4ac4e8ee92346e6d14eacfbf`, built fresh from the authenticated 73-log
inventory with the recorded **20 + 20 + 20 + 13** schedule. It includes learner
v61, parser v1.8, the corrected shared decoder and matcher API v3. No manual
template set or earlier registry seeded the build. It has 394 templates
(296 supported, 98 provisional); equality with v60's compact templates was
measured after building, while the new executable and package identities differ.

The same retained 20 Runs gain **13,184 classified occurrences across 95 messages**
over production, with zero assignment losses or supported-to-provisional
downgrades. All three original failures classify as supported. Full parser
correspondence passes for 73 genuine logs, 2,517,940 emissions and 2,594,588 native
inputs. Installed classification, contract reconstruction and isolated learner
execution pass, including session 55. Details, exact pins, commands and intake:
[final handoff](HANDOFF.md#combined-release-delivered--2026-10-05).

The original application's Data Intelligence JSON/HTML/text export helpers rejected
surrogate-bearing text from genuine session 55. This affects human exports of
affected records, not the verified native ingestion/reconstruction. It requires
a bounded Data Intelligence repair or explicit owner disposition during Pipeline
receiving. Decoder integration alone did not close it. This failure is superseded
by the independently received repair above. Pipeline's original
[receiving receipt](PIPELINE_RECEIVING.md) distinguishes passing handler/storage
checks from open Reporting repairs; this is not a blanket completion of 08C.

Concrete intake is in the [final release record](#final-release-record) below.
The [numbered production comparison](../../.codex-tmp/combined-release-20261005/CHANGES.html)
contains 15 added, 15 removed and 15 gained examples, linked to shared patterns.
The [marked-reference report](../../.codex-tmp/combined-release-20261005/FIXES.html)
contains 14 numbered examples. Their evidence and links are checked; no new
browser campaign is claimed. Existing release mechanics are in [RELEASES.md](../RELEASES.md).

## Receiving and operational boundary

The consultant's findings were delivered as the two 08C correctives; the owner
confirmed no separate assessment is needed. Accepted code/evidence hashes,
production package `68f1ae5db205ab46afef9c4d` and the v60 research package
`840957b2f8e16f1cf0f88ad2` were authenticated before integration. The old
parser-substitution-simplified adapter and consultant ZIP remain historical.
The corrected fragment API is used at Source.read_text, decoded header groups,
native continuation text and the existing formatted-literal byte tail. Parser
framing, recovery, byte spans, tokenization and inverse encoding are unchanged.
Physical source operations retain header policy and corrected BOM metadata.

The learner's authenticated ordinary manifest includes the same application
decoder source. Isolated `python -I -S -B` execution has no ambient application
fallback. The installed runtime uses the packaged application module. There is
no separate decoder catalog or pin. Automatic physical-source detection declares
`chardet>=7.6,<8`; the verified version is **7.6.0**. Known-UTF-8 processing does
not require or import a detector. Source-search/excerpt changes were received by
focused edits and match the accepted candidate text.

Publication used the existing learner/model registration owners: learner order
**9**, model order **8**. It did not change `models/selection.json`, ingest/reset
production, restart services, interrupt capture, commit, push or upload anything.
Retained v58 is not the proposed selection. All prior releases remain available.
Pipeline must use the final application artifact with its current contract
renderer, not only change a model pin. The existing restart restriction remains
until the owner resolves it for a concrete verified cutover.

Database recommendation remains to retain the existing store for new unique logs.
Full-log hashes are globally unique; changing packages does not provide the
undelivered same-Run result-replacement operation. No reset is required or
authorized here. Pipeline's [receiving assignment](PIPELINE_INTEGRATION_PROMPT.md)
owns runtime/capture checks and cutover preparation.

## Executive assessment of the combined release

The changes are positive on the reviewed evidence: the same 20 stored Runs gain
13,184 complete classifications across 95 previously unmatched messages, with no
assignment losses or supported-to-provisional downgrades. All three original
`20261003-IS3QON` diagnostics classify as supported templates. Exact reconstruction,
message identity and existing locator captures pass the comparison checks.

These are cumulative improvements over production, not gains attributable solely
to the last formatting fix. Remaining activity and internally nested-formatting
gaps are explicit below. Coverage and fewer templates do not establish universal
semantic correctness. The integrated decoder results are recorded below.

## Implemented improvements retained from v60 and integrated in v61

The IDs below are documentation references, not new diagnostic taxonomy. All
rows in this table are implemented in the delivered release; production is unchanged.

| ID | Change and resulting behavior | Owning implementation |
|---|---|---|
| L01 | Single-quoted values no longer contribute their spelling to initial similarity. Quote positions remain structural evidence; missing/misaligned positions incur a penalty. This proposes groups, not automatic KEY/PARAM typing. | [regions.py](../../tools/template_learning/regions.py), [matching_primitives.py](../../tools/template_learning/matching_primitives.py) |
| L02 | After the existing single regrouping sweep, identical-template groups are consolidated and their union inferred once. Original constituents still participate in wording protection and complete-match checks. | [clustering.py](../../tools/template_learning/clustering.py) |
| L03 | A recognized trailing location sequence contributes one presence unit when it contains one or more locators. Its values and entry count do not affect classification similarity. Literal section introducers remain significant. Every ordered file/line/trace value is retained. This does not collapse arbitrary KEY or PARAM sequences. | [location_sequences.py](../../tools/template_learning/location_sequences.py), [regions.py](../../tools/template_learning/regions.py) |
| L04 | `line:` / `near line:` field recognition no longer depends on a numeric value. `Unknown` is a LOCATOR in the recognized location-value position; elsewhere it normally remains literal. Parenthetical location traces, including `effect[args#…]`, are captured as PARAM interiors. | [owner_rules.json](../../tools/template_learning/owner_rules.json), [matching_primitives.py](../../tools/template_learning/matching_primitives.py) |
| L05 | In-game date prefixes such as `17 May 994:` are equivalent formatted literals at the same template position, displayed as `{game date}`. They are not KEYs. Exact spelling remains part of message identity and reconstruction; the outer log timestamp is separate. | [formatted_literals.py](../../tools/template_learning/formatted_literals.py), owner rules |
| L06 | `CHARACTER_ID_SHORT` captures the complete display name and `(numeric ID, display location)` at supported field boundaries. A date is not required. Subsequent lowercase words and leading transliteration modifiers are handled; existing full identities retain precedence. | Owner rules, shared field recognition |
| L07 | The complete receiver between `receiver is ` and `, default location is ` is `CHARACTER_ID_SUPER_SHORT`. This is contextual character recognition, not a global capitalization/name heuristic. | Owner rules, matcher validation |
| L08 | The capitalized display-location field after `default location is ` is one PARAM through its native line boundary. Multiword places are retained whole. A period is not a special terminator. | Owner rules |
| L09 | Contextual grammatical/name fields retain whole values: Parent-message state phrases, missing-localization display names, and demonstrated marked character line references. There is no global English stop-word ban. | Owner rules, shared field recognition |
| L10 | Invalid-comparison side/identifier and compare-trigger identifier/expected-scope fields have explicit contextual KEY boundaries. Surrounding diagnostic wording remains literal. | Owner rules |
| L11 | `Unknown effect:` and `Unknown trigger:` retain separate category wording during initial discovery. This addresses the case where a revision-only wording safeguard could not protect words already inferred as slots. Default literal guidance remains disabled. | Owner-directed constructions, [diagnostic_wording.py](../../tools/template_learning/diagnostic_wording.py) |
| L12 | Adjacent alphabetic KEY proposals that only vary together are reconsidered as one span. That span must satisfy existing field boundaries; otherwise literal variants remain. The two character-history phrases stay literal without history-specific construction gates. Existing opaque PARAM/REASON fields are protected. | [patterns.py](../../tools/template_learning/patterns.py), shared boundary checks |
| L13 | Quoted unknown-formatting-tag contents are complete PARAMs, preserving actual control characters and line endings. | Owner rules |
| L14 | Contextual ONCLICK/TOOLTIP/display/reset sequences become whole opaque PARAMs. Metadata, names and control bytes remain exact. The complete reset run is retained; larger existing quoted PARAMs are not split. No trait/name/mod/emitter whitelist is used. | Owner rules, shared field recognition |
| L15 | Refinement children store local decisions with parent references rather than copying the parent's complete evidence repeatedly. Consolidation and retirement share this lineage. Sequential event IDs do not require content-hash deduplication. | [refinement_history.py](../../tools/template_learning/refinement_history.py), clustering and retirement |
| L16 | Model JSON and revision hashing stream. Bundle validation uses the producer representation and checks written bytes without loading a second complete model. Field observations and executable matcher snapshots avoid additional copies; review output streams rows. | [artifacts.py](../../tools/template_learning/artifacts.py), [evidence_serialization.py](../../tools/template_learning/evidence_serialization.py), research/review tools |
| L17 | Schema-6 templates / matcher API v3 support repeated location layouts and exact formatted-literal choices. The application contract renderer reconstructs them without normalizing native message contents. | Matcher validation, [contracts.py](../../src/ck3chronicle/pipeline/contracts.py) |
| L18 | Human reports group production predecessors by actual candidate successor, distinguish selected counts from overlapping compatibility counts, number examples, and avoid repeated patterns. Retained genuine evidence supports reproducible comparisons. | [report_production_comparison.py](../../tools/template_learning/report_production_comparison.py), focused review tools |
| L19 | Fragment-safe UTF-8/surrogateescape processing in the new parser and native helpers preserves leading BOM characters and undecodable bytes without physical-file header admission. Physical source decoding retains its own header and detection policy. | [parser v1.8](../../tools/template_learning/parsers/v1_8/parser.py), [decoder.py](../../src/ck3chronicle/decoder.py), continuation and matcher owners |
| L20 | Explicit authenticated application dependency in isolated learner releases, declared detector dependency and packaged registered distributions close installed loading. Comparison tools prove genuine input correspondence under each package's actual parser identity. | [learner_loader.py](../../tools/template_learning/learner_loader.py), [pyproject.toml](../../pyproject.toml), parser/comparison verification owners |

For detailed boundaries and owner authority, use
[LEARNER_INFERENCE_RULES.md](../LEARNER_INFERENCE_RULES.md). Its older dated
mechanisms are historical where superseded: in particular, date-as-KEY,
history-as-PARAM and history-specific construction gates are not current behavior.

## Representative results

The scope-mismatch diagnostic now shares this formulation:

```text
Event target link '<KEY>' did not get a matching scope type. Expected '<KEY>', but got '<KEY>'
```

The travel diagnostic retains its native leading location/trace text, followed by:

```text
{game date}: <CHARACTER_ID_SHORT>: Starting travel with incorrect receiver, receiver is <CHARACTER_ID_SUPER_SHORT>, default location is <PARAM>
```

The complete formatted references around `Insightful Thinker`, `Misguided Warrior`
and character names now occupy PARAMs. Those names are examples, not rule constants.
In contrast, `has history after death birth` and `has history from before birth`
retain their literal wording. No template approvals are encoded in the learner.

Owner recheck on 2026-10-05 confirmed the genuine Maria / Count Momčilo of Kotor
message: `27 Nov 1076` is an exact literal choice; `Maria (58928, Aigaîon Pélagos)`
is CHARACTER_ID_SHORT; `Count Momčilo of Kotor` is CHARACTER_ID_SUPER_SHORT;
`Aigaîon Pélagos` is one PARAM. All 63 retained travel/date examples pass the
[exported-package recheck](../../.codex-tmp/marked-references-v60-final/travel-owner-recheck.json).
Fragmented VALUE/KEY patterns shown before the successor in the comparison are
production predecessors, explicitly labeled as removed from the candidate.

## Verification of the exact combined artifacts

The production comparison and new reference model use the established 73-log content-hash inventory. The candidate was
built with the recorded 20 + 20 + 20 + 13 incremental schedule, not a one-shot build.

| Scope | Result |
|---|---|
| Parser correspondence | All 73 logs / 2,517,940 emissions / 2,594,588 native units pass exact bytes, framing, text, lexical spans and recovery checks. Session 55 is included. |
| Same 20 stored Runs | 52,899 stored records; 7,287 distinct recovered contextual messages; 811,103 message/recovery occurrences. Gains: 13,184 occurrences / 95 messages. Losses and supported-to-provisional downgrades: zero. |
| Candidate outcomes in those Runs | 798,160 supported-template occurrences; 7,699 provisional; 5,243 unmatched; one unresolved recovery. Provisional assignments are complete pipeline outcomes. |
| Full 73-log training evidence | 91,925 contextual messages / 2,594,588 occurrences. Candidate: 2,476,548 supported, 118,038 provisional, two unmatched. No lost assignments or supported-to-provisional downgrades relative to production. |
| Original Run IS3QON | All three originally unmatched messages pass classification and record preparation as supported templates. |
| Marked references | 127 newly recognized fields in 69 messages; two additional messages verify preservation of enclosing PARAMs. All 71 messages / 126 occurrences pass exact captures and reconstruction. Six templates use the new declaration; all are supported. |
| Earlier field fixes | All 16 history messages / 33 occurrences retain literal phrases. All 63 date/short-character messages in the 73-log scope pass. Full-corpus field checks report zero failed captures, reviewed grammatical KEY captures or template ties. |
| Storage fidelity | Zero production replay mismatches, reconstruction failures, identity collisions or changed existing LOCATOR captures in the stored-Run comparison. |
| Installed artifact | CPython 3.12.14 / chardet 7.6.0, imports from the installed prefix; original three and all 100,003 session-55 messages reconstruct exactly. Session 55: 99,991 supported, 12 provisional; all 44 preserved-byte messages supported. Isolated retained learner executes with its authenticated decoder. |
| Learning history | 211 events, including 43 child delta events, retain valid parent-linked lineage; streamed producer/writer owners retained. No new peak-memory measurement is claimed. |
| Template inventory | Production 689; candidate 394 (296 supported, 98 provisional). By exact ID: 213 added, 508 removed, 181 unchanged. Replacements and layout consolidations contribute to these counts. |

The training and stored-Run scopes overlap; do not add their counts. Contextual
message counts also differ from the model's 90,506 distinct message records.
These checks establish observed behavior, not an independent accuracy estimate.

Readable evidence:

- [Production comparison, executive assessment and 15/15/15 samples](../../.codex-tmp/combined-release-20261005/CHANGES.html).
- [All marked-reference groups, with 14 numbered examples](../../.codex-tmp/combined-release-20261005/FIXES.html).
- [Full 73-log comparison](../../.codex-tmp/combined-release-20261005/training-corpus-comparison.json).
- [Exact field verification](../../.codex-tmp/combined-release-20261005/formatted-verification.json), [earlier fixes and original three](../../.codex-tmp/combined-release-20261005/gap-verification.json), [date/history checks](../../.codex-tmp/combined-release-20261005/literal-corrections-verification.json).

Evidence links are workstation-local ignored artifacts, not files shipped in a
release. Their SHA-256 inventory is in the final delivery receipt linked below.

## Open, deferred and unchanged items

| Item | Actual status |
|---|---|
| Decoder API integration | Delivered and verified in parser v1.8, learner v61 and the installed application. No physical-file calls enter internal parser spans. See the final handoff. |
| Activity description | Tested contextual PARAM proposal, not implemented. Two training messages remain unmatched; the observed family contains ten messages. |
| Formatting nested inside a display label | Outside the implemented simple-reference rule. Includes a character label in the faction family; its plain faith reference is captured correctly. |
| Removed templates without selected witnesses | 38 production alternatives have no selected witness across the two comparison scopes. This is not proof of a loss or a safe removal; earlier reviewed overlaps must not be presented as new independent defects. |
| Untyped construction | Existing dedicated applicability excludes it from the generic construction. Do not describe this as literal-preference selection or full owner approval of that design. |
| Sliding similarity scale | Tested, not adopted. Existing equal-length 1–2-unit positional rule was retained; experiments varied 3–6-unit weighted cutoffs to .68/.69/.70/.71 and .60/.63/.66/.69. No demonstrated selected-classification gain; no full incremental sliding-policy model was built. |
| Additional `_`/`.` effect/trigger cue and broader PARAM exemption | Surveyed and deferred; existing behavior addressed the demonstrated category cases. No blanket literal-word rule was added. |
| Separate rare-message pass | Deferred. Existing additive learning already pools cumulative unsettled evidence. |
| Parser mechanics / message splitting | Unchanged from v1.7 apart from fragment decoding and honest version metadata; full genuine-corpus correspondence passes. Locator recognition does not split emissions or alter continuation recovery. |
| Production activation | Not performed. The combined v61 package is registered, with an exact proposed selection and retained previous selection. Pipeline receiving and activation are pending; v58 is not the proposed cutover. |

## Final release record

Paths below are relative to the repository root. Full SHA-256 values are external
pins, not version nicknames. The final application wheel is under `application-corrected/`;
earlier wheels under `application/` and `wheelhouse/` are not intake artifacts.

| Artifact / identity | Location / SHA-256 |
|---|---|
| Learner v61 | `learners/releases/0dc8130a0740d2209e1da8e2cc7241d7d735df2c0252342075b7624bfad0e3de`; manifest `d5dffa6f9202bf6d386f27a2738ca8d0274b42971272bc8cd2550cddbbe42041` |
| Learner implementation identity | `77a3935070c561c2de830f6577f31c189991dd93d0bce7bf0106c626a083ced7` |
| Parser | `ck3-lossless-v1.8`; code `0357b8d1c342c546452ed8f294405bfe41c86c7116eca51eddf8bc5b67984135` |
| Research / runtime model | `59d8130aaad3a305b9c1ba42` / `789219fdbd81c8dab950bc93` |
| Model package | `models/releases/4ac4e8ee92346e6d14eacfbf`; manifest `839548e8c8143e01b63059848557dc94e9fe66f5e1924f6026442f7331a8ba9f` |
| Interfaces | Model schema 6; matcher `ck3-native-matcher-v3`; selector `complete-assignment-v2`; classifier `ck3-native-message-classifier-v8`; contract `error-contract-v1` |
| Final application wheel | `.codex-tmp/combined-release-20261005/application-corrected/ck3chronicle-0.0.1-py3-none-any.whl`; `362b09b2d553f7610a1cf5e8b848000af610ef48f4c8c1b5bba739223586316b` |
| Application source inventory | `application-source.json`; source digest `e47d8ed33c9301ad1b4a867d5862bf6ffdf9f7b4ac8832a08f2c352346a8020f`. Git HEAD `7b7208341469e0b5df8d739cb0fd6e805fc411ea` plus recorded dirty worktree, not a new committed revision. |
| Installed classifier application lineage | `sha256:34e0069e431a1c810265d655f7990e6c1c12d583f4d71f948111d59e1e477905` (classifier's narrower lineage identity) |
| Dependency wheel, CPython 3.12 Windows AMD64 | `.codex-tmp/combined-release-20261005/wheelhouse/chardet-7.6.0-cp312-cp312-win_amd64.whl`; `99bdf02c44a943448e82196ea735bd057a3ecc3e0b9a82dbbeff8f563fd9ae64` |
| Installed receipt | `.codex-tmp/combined-release-20261005/installed-check-corrected/receipt.json`; `a5ac3859af1746accfdddcf4dd0a43505c34bcc0a283edf10e06a91ef6205b86` |
| Registration / selections | [publication.json](../../.codex-tmp/combined-release-20261005/publication.json), [proposed selection](../../.codex-tmp/combined-release-20261005/proposed-selection.json), [previous selection](../../.codex-tmp/combined-release-20261005/previous-selection.json) |
| Final evidence inventory | [delivery-hashes.json](../../.codex-tmp/combined-release-20261005/delivery-hashes.json); receipt locations and reproduction commands in [HANDOFF](HANDOFF.md#reproduction-and-intake-commands) |

Final receiving repaired stale setuptools build contamination: 54 obsolete files
were removed by rebuilding in fresh build/staging directories. The corrected wheel
contains 556 source-corresponding code/resource files; its clean installed probe
passes. The rejected wheel/receipt remain evidence, not intake. See HANDOFF's
failed-check dispositions and `application-stale-build-failure.json`.

The dependency wheel was locally repacked from 65 installed files whose hashes
matched their original RECORD, after network/cache access was unavailable. It is
not claimed to be the original upstream wheel. Offline clean installation and
`pip check` pass. The installed check uses only a configuration working directory
and installed modules, with writable runtime paths confined to disposable evidence.

The reused genuine source campaign covers 942 files: 941 readable and one retained
low-confidence outcome. Corrective BOM metadata and two installed source witnesses
pass. Missing genuine UTF-16/32, East Asian encoding and double-BOM positive
examples remain disclosed source-reading limits, not release gates. No additional
encoding research or synthetic tests were performed. The separate Data
Intelligence export defect remains open as described above.
