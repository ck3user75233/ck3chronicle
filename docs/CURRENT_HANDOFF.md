# Current handoff

## Database replaced; 31 new-model Runs active — 2026-10-05

**Complete.** Production now uses
`.ck3chronicle/wip/runtime/ck3chronicle-schema3-20261005T112504Z.sqlite3`: 31 Runs,
all package `4ac4e8ee92346e6d14eacfbf` / parser v1.8, totaling 958,190 classified
occurrences in 79,508 records. These are the 30 rebuilt retained captures plus the
session the owner just closed. No database rows were migrated or imported.

See the [replacement receipt](learner-next-release/PIPELINE_RECEIVING.md#database-replacement-complete--2026-10-05)
and [operational record](learner-next-release/PIPELINE_CUTOVER.md). After a verified
backup, config's database path switched at 12:07:47 UTC and the installed watcher
restarted at 12:08:19. Watcher 51024 (launcher 55312); handler 54908 (launcher 60264),
instance `f474dbf7100a44399e2ae4a6a05f6375`. Fresh heartbeat/public reads/reports pass.
The old database/review namespace exists only in the backup at
`.codex-tmp/pipeline-refresh-20261005/backup-20261005T120734Z/retired-original/`.
Protected captures and other configuration remain unchanged. No rollback needed.

The genuine CK3 lifecycle 11:16:27–12:06:14, capture and automatic new-model ingestion
are verified; its active Run is `20261005-UYSOEO`. The earlier live-lifecycle follow-up
is closed. R4 syntax remains separately owned Reporting work. Staging/deferral and
older pending statements below are historical; do not rerun the 30-input rebuild.

## Thirty-capture rebuild verified; switch deferred by owner — 2026-10-05

All 30 readable protected captures are rebuilt and verified under production package
`4ac4e8ee92346e6d14eacfbf` in the separate staged database
`.ck3chronicle/wip/runtime/ck3chronicle-schema3-20261005T112504Z.sqlite3`.
The [receipt](learner-next-release/PIPELINE_RECEIVING.md#thirty-capture-rebuild-staged-switch-deferred--2026-10-05)
records 948,135 classified occurrences, 76,510 records, exact native-region/review
checks, unchanged capture facts/playsets and passing genuine missing-time reports.
Evidence: `.codex-tmp/pipeline-refresh-20261005/`; staging handler is shut down.

**The owner explicitly deferred the database switch and asked to leave CK3 running.**
Production still uses the September 28 database; configuration, watcher 64444,
handler 47932 and protected originals remain unchanged. Do not execute stop/switch
helpers while this deferral applies. Pipeline's next action after it is lifted:
secure the naturally completed session, refresh inventory, back up the closed
production store/evidence at the safe boundary, switch to this existing staged
store, then reconcile startup duplicates and any newly protected unique captures.
Do not rebuild the same 30 captures again. Natural production lifecycle verification
remains distinct from the completed historical rebuild. R4 remains Reporting-owned.

## Owner-requested database refresh pending game exit — 2026-10-05

The owner requested clearing legacy-model results and ingesting protected originals
under production package `4ac4e8ee92346e6d14eacfbf`. This authorizes the historical
refresh, superseding the earlier no-reset/no-reprocessing restriction for this work.
No reset has occurred. At 11:18:55 UTC CK3 PID 53004 is running under watcher 64444;
leave capture observation intact until natural exit and completed publication/ingestion.
Read-only inventory: `.codex-tmp/pipeline-refresh-20261005/refresh-inventory.json`.
All 30 stored Runs have readable protected originals; 22 older directories still
deny contents/ACL reads. They are not proven missing stored Runs.

Pipeline continuation: verify the first naturally completed new-package lifecycle,
refresh capture/request accounting, stop the verified watcher/handler safely, make
and verify a fresh backup, explicitly initialize a new database through the existing
API and switch its configured path, then let the sole installed watcher's ordinary
startup ingestion rebuild the available genuine captures. Preserve original logs,
metadata/playsets and archived database/review evidence. Run IDs/processing times
may change; old classifications/lineage survive in backup. No permissions repair,
fake input or fabricated missing history is authorized by this inventory work.

## Production cutover complete; natural lifecycle follow-up pending — 2026-10-05

**Production is on package `4ac4e8ee92346e6d14eacfbf` (learner v61/parser v1.8).
No rollback.** The owner-authorized switch/restart superseded the prior hold.
See the [activation receipt](learner-next-release/PIPELINE_RECEIVING.md#production-activated--2026-10-05)
and [cutover record](learner-next-release/PIPELINE_CUTOVER.md). At 09:57:58 UTC the
final R3 installed runtime started: watcher 64444 (launcher 64756), handler 47932
(launcher 65896), instance `88739409838c4e38936bebc72166ae33`. Existing database,
configuration, 30 Runs and capture/review evidence were preserved; the verified
backup is `.codex-tmp/pipeline-activation-20261005/backup-20261005T095647Z/`.
Fresh heartbeat, startup duplicate accounting and genuine existing-Run reports pass.

No new unique capture occurred: **new-package stored ingestion lineage and live
lifecycle verification remain pending**, distinct from successful activation.
Pipeline retains the follow-up: correlate the next natural completed capture to
its new Run, verify actual package/parser/application lineage, facts/counts,
playset/review and reports, then append evidence. No fake capture or historical
reprocessing. R1/R2/R3/R5 remain closed; R4 syntax remains separately owned Reporting
work. Older holds and process observations below are historical where superseded.

## R3 packaging closed; activation held — 2026-10-05

**READY FOR OWNER ACTIVATION DECISION. R3 CLOSED.** The
[final receipt](learner-next-release/PIPELINE_RECEIVING.md#r3-packaging-closed--2026-10-05)
and [cutover](learner-next-release/PIPELINE_CUTOVER.md) supersede the earlier
post-install override arrangement. Final wheel SHA-256:
`7239a0c5b89e52f2df1d31028bdbf21b086e3600bf7c079347a1ee4f1d982959`; artifact and clean staged environment
are under `.codex-tmp/pipeline-r3-packaging-20261005/`. The wheel contains a valid
default referencing shipped package `4ac4e8ee92346e6d14eacfbf`. Outside-checkout
default loading, all 556 installed members and installed rollback authenticate
without a corrective file replacement. Application/distribution bytes are unchanged;
prior independent Reporting/ingestion evidence is reused. Live configuration and
immutable distributions remain untouched. The owner explicitly holds activation;
new-package live lifecycle verification remains pending. Older entries below are
historical where superseded.

## Pipeline repair receipt complete; activation decision next — 2026-10-05

**READY FOR OWNER ACTIVATION DECISION.** Continue from the
[independent receipt](learner-next-release/PIPELINE_RECEIVING.md#pipeline-repair-receiving-completed--2026-10-05)
and [final cutover](learner-next-release/PIPELINE_CUTOVER.md). Evidence Q:
`.codex-tmp/pipeline-reporting-receiving-20261005/`; final staged interpreter:
`Q/deployment/Scripts/python.exe`. Final wheel remains
`.codex-tmp/reporting-repair-20261005/final/application/ck3chronicle-0.0.1-py3-none-any.whl`,
SHA-256 `3b4b20881233174a1858b4fc960b0318555d0ef9387909ca4584c53772e68890`.
Pipeline owns the mandatory new-selection installation override and authenticated
installed rollback. The bare-wheel default limitation is disclosed; no wheel was
patched/relabelled, and learner/model/parser distributions remain immutable.

Independent `R/pipeline-independent-final/receipt.json` passes 35 genuine checks
and 28 CLI commands (new syntax is the one expected exit-2 result); Q additionally
verifies delivered/independent output contents. R1/R2/R5 receiving is closed.
Original P/producer receipts and installations are preserved; no ingestion setup
was rerun. Native decoder/processing code is unchanged, so original storage and
full-corpus evidence is reused. R4 stays Reporting-owned; R2's nonblocking
disposition is unchanged. No runtime product source was edited in this continuation.

Read-only observation at 09:27:19 UTC: watcher 30816, handler 23252 / instance
`ca3faf45a4514e5cab542769c2a3c70f`, CK3 absent. Latest Run `20261005-0UM3HN`
completed naturally on the old package; 30 readable pending originals match all
30 stored Runs, with 22 older inaccessible directories unchanged. Refresh these
observations before any later operation. Keep the current database. The owner must
separately authorize the concrete pin switch and watcher/handler restart; no live
config/pin switch, production write/reset, backlog processing, commit or push is
authorized or performed. New-package live lifecycle verification remains pending.

## Reporting R1/R2/R5 repair delivered — 2026-10-05

Continue with the [new Pipeline repair receipt](learner-next-release/PIPELINE_RECEIVING.md#reporting-repair-delivered--2026-10-05).
Evidence/artifact root: `.codex-tmp/reporting-repair-20261005/`; final wheel is
`final/application/ck3chronicle-0.0.1-py3-none-any.whl`, SHA-256
`3b4b20881233174a1858b4fc960b0318555d0ef9387909ca4584c53772e68890`.
`artifact.json`, installed receipts and `repair.patch` identify only this repair
against the original wheel; concurrent work and original receipts are preserved.
All 556 members authenticate, with six application members changed and retained
distributions unchanged. Genuine public-handler and installed CLI checks pass for
R1/R2/R5 and the old-package control; no source timestamp was invented or stored.

Pipeline receives the new installation and updates cutover. Owner activation is
still separate; no live pin switch/restart, production ingest/reset, historical
processing, commit or push occurred. R2's prior nonblocking disposition stands.
R3 remains packaging's default-path obligation (explicit new selection and installed
rollback verified); R4 remains separate Reporting selector work. Broader 08C is
not resumed. Original receiving and source lineage below remain historical evidence.

## Pipeline receiving complete with Reporting defects — 2026-10-05

Current continuation is [PIPELINE_RECEIVING.md](learner-next-release/PIPELINE_RECEIVING.md)
and the [concrete cutover](learner-next-release/PIPELINE_CUTOVER.md). Authenticated
318 delivery hashes and 556 installed files; exact final package passed genuine
HandlerClient ingestion/storage/review on three new-package logs (172,130 units)
and an old-package control. Default ingestion in a separate staged deployment also
passed. Evidence/scripts/storage are ignored under `.codex-tmp/pipeline-receiving-20261005`.
No runtime product source was edited and concurrent work remains intact.

Open receiving owners: Data Intelligence/Reporting owns repeat-part template
rendering (`KeyError: 'prefix'`), surrogate UTF-8 exports and new-model syntax
selectors. Owner clarification: the surrogate-export defect R2 is nonblocking;
do not require its repair or another disposition before activation. The
[fresh-chat repair prompt](learner-next-release/REPORTING_RECEIVING_REPAIR_PROMPT.md)
covers R1/R2 and R5, Reporting's use of chronology to exclude missing-time Runs
from ordinary listings/selection. Missing time limits chronological placement only;
Run-ID listings, all-Runs message searches and other nonchronological operations
must work normally with the available facts. Repairs remain pending; this is prompt
preparation. Learner/application packaging receives the wheel's
default pointing to an unshipped `candidates/` directory; Pipeline's staged new
default and catalog-derived installed rollback avoid that deployment path defect.
Do not modify/relabel the delivered wheel. Repaired applications need new receipts.

Production remains package `68f1ae5db205ab46afef9c4d`, watcher 30816, handler 23252 /
instance `ca3faf45a4514e5cab542769c2a3c70f` at the recorded observation. CK3 is running.
29 stored Runs have readable matching pending originals; 22 older pending folders
are inaccessible and unchanged. Latest genuine ZEHL9K's report passes. Keep the
database; no historical processing/reset is authorized. No live selection, config,
database, watcher or handler was changed. R1 remains the recommended repair before
activation; the owner can separately disposition it. R2 is not an activation gate.
The existing restart prohibition still requires an operational decision.
Recheck process identities and capture safety before any later authorized switch.

## Combined learner / decoder release delivered — 2026-10-05

The final [release packet](learner-next-release/README.md) records registered v61
learner/parser v1.8 and model package `4ac4e8ee92346e6d14eacfbf`, the verified
installed application, exact pins and proposed/previous selections. Same 20 Runs
gain 13,184 classifications with no losses/downgrades; full 73-log preservation
passes. Pipeline receiving and activation remain pending. Production selection
`68f1ae5db205ab46afef9c4d` and services are unchanged. The Data Intelligence
surrogate-bearing export defect remains disclosed for bounded repair or owner
disposition. The preparation entries below are historical where superseded by
this completed release; they do not change the remaining operational restrictions.


## Decoder handoff delivered to learner and pipeline documentation — 2026-10-05

The combined release HANDOFF.md now includes exact learner/parser substitutions
and a pipeline receiving/deployment section. Current 07D and pipeline action
documents link to it. Decoder delivery is ready; receiving, combined verification
and activation are separate pending team responsibilities. This documentation
update did not change code, production selection, stored data or runtime processes.

## Travel-field implementation rechecked for owner — 2026-10-05

The quoted fragmented travel pattern is production template
`b04e2561df19216e8c1e0a72`, not a v60 successor. The actual candidate successor is
`64c28a8317c5ddae687bfb54`: equivalent `{game date}` literal, complete
CHARACTER_ID_SHORT, contextual CHARACTER_ID_SUPER_SHORT receiver, and final PARAM.
Re-ran the exported-package check on all 63 retained date/travel messages, plus
the existing history/localization checks. Exact rendering and date retention in
identity pass. The genuine Maria / Count Momčilo of Kotor example captures
`Maria (58928, Aigaîon Pélagos)`, `Count Momčilo of Kotor`, and `Aigaîon Pélagos`
as the complete respective fields; `27 Nov 1076` is a literal choice, not a slot.
Evidence: `.codex-tmp/marked-references-v60-final/travel-owner-recheck.json`.
The report generator now explicitly labels production-before / candidate-after,
marks removed predecessors, and provides a jump past long predecessor lists.
The same CHANGES.html URL is regenerated. No learner rules or packages changed.

## Combined learner / decoder release preparation — 2026-10-05

Owner intends the next pinned release to include the incoming decoder API handoff.
The running release packet is now [learner-next-release/README.md](learner-next-release/README.md),
with an 18-item implemented change list, genuine v60 results and explicit open/
deferred items. Its [HANDOFF.md](learner-next-release/HANDOFF.md) records exact
baseline pins, integration dependencies, verification and coordinated activation.
Final combined identities/results are pending; v60 is the verified baseline,
not a decoder-integrated release. The subteam's concurrent 2026-10-05 update reports
four disposable parser checks passing, including the corrected session-55 case;
formal receiving and integrated classification remain pending. Parser-hash equality assumptions in
comparison tools need explicit receiving work for the new parser combination.
This turn changes documentation only. No build, registration, active pin, runtime
process or stored evidence changed. Continue updating this packet as integration
lands; production remains 68f1ae5db205ab46afef9c4d.

## Shared decoder simplified; known encodings approved — 2026-10-05

Owner explicitly approved using a known encoding when available and detection
otherwise through one API. `decode`/`read` use standard codecs with surrogateescape
for known encodings; automatic Unicode reading precedes chardet fallback using its
own minimum threshold. Candidate voting, directory override routing and decoder
caching were removed. Search owns its session snapshot; display renders preserved
bytes as \\xHH without changing processing text. Double-BOM stop remains.

Actual disposable parser substitutions now PASS on four genuine logs including
session 55: 186,704 emissions, 190,701 native matcher inputs and exact native byte
reconstruction agree. All 44 Invalid character messages pass search/excerpt display
checks. The 942-file random mod survey gives 941 identical readable text/search/
excerpt results and one low-confidence undetermined result. Public stored-query
comparison and runtime logging ownership checks pass. Production caller files,
selected artifacts and selection remain unchanged; no database ingest or package
publication. See TASK08C_ENCODING_RECOMMENDATION and TASK08C_HANDOFF. Earlier
fully automatic/failed-parser statements below are historical and superseded.

## Disposable parser decoder substitution exercised — 2026-10-04

The actual pinned parser was copied into ignored decoder evidence and only its
two byte-to-text decoding calls were routed through the shared API, with a small
failure wrapper/counter. Three genuine logs match across 86,704 emissions and
90,698 native matcher inputs. Session 55 fails at line 1618 when the decoder
rejects its first Invalid character message. Overall acceptance FAILED; decoder
correction remains outstanding. Production artifacts/selection are unchanged.
See TASK08C_HANDOFF and `.codex-tmp/task08c/decoder/parser-substitution/results.json`.

## Decoder candidates only; existing callers restored — 2026-10-04

Owner requires the decoder cutover with the coordinated pinned release, using
only disposable caller copies meanwhile. Source-search/report integration and
the dependency declaration have been restored; candidate copies are retained
under ignored task evidence. The new decoder API has no production callers.
Inconclusive or text-ambiguous decoding now fails explicitly; header repair is
out of scope. Earlier integration-delivery statements are superseded. See the
[current 08C handoff](TASK08C_HANDOFF.md) for restoration and staged checks.

## Parser decoder-call boundary — 2026-10-04

Owner clarified that the shared decoder should replace embedded decoding calls,
without parser-mechanics changes absent prior alignment. The experimental source-
reference replacement adapter was removed; parser integration is pending the
coordinated upgrade. Source search/excerpts retain the shared decoder. The
[08C handoff](TASK08C_HANDOFF.md) distinguishes current code from historical
prototype comparisons. Pinned parser artifacts and ingestion are unchanged.

## Shared decoder/API and genuine integration comparison — 2026-10-04

Owner-directed unpinned `Decoder` now serves source search/excerpts through one
automatic API. Genuine source and UTF-8 parser comparisons pass; one actual log
with an invalid UTF-8 byte exposes a detector/parser mismatch, recorded for the
coordinated package upgrade. Ingestion and pinned artifacts remain unchanged.
See [08C handoff](TASK08C_HANDOFF.md) for APIs, evidence, limits and failed checks.

## Formatted-reference PARAM correction verified — 2026-10-04

Latest executable learner: v60. The owner requests contextual special-character
markers as PARAM boundaries. `formatted-linked-reference` recognizes optional
ONCLICK, TOOLTIP metadata, L/semicolon display marker and text, with the complete
consecutive reset run (at least three for linked references and two for tooltip-only references). It preserves
all bytes as one PARAM. Earlier declared/full-ID fields retain precedence; an
inner reference defers within a larger paired quotation. Discovery quote behavior
was proved identical on all 91,925 corpus messages. Parser v1.7 is unchanged.

The 73-log preflight recognizes 127 new fields in 69 messages, preserves every
old declared boundary and checks two larger quoted PARAMs. v59 initially covered
only triple resets. It completed and verified package 79b70779b4b73bc2b15a7c72,
with zero assignment losses/downgrades and 13,184 formerly unmatched occurrences
classified in the 20 stored Runs. This is 1,689 more than v58, from one genuine
character-title message now selecting its formatted PARAM template. However,
report review found 14 additional ordinary two-reset tooltip fields. v59 is
superseded by the current v60 rebuild and must not be promoted as final.

Current frozen release:
`a9cb7ae7704cfd7e6c5acf84def50dfe74440e9b913c0bf9240720dd985ebb6f`, pin
`66d6bcd105ea60fcabada86f90827a646fc00f5d102a7d6ee4f77ffe68920b01`.
Workspace `.codex-tmp/marked-references-v60-final/build` completed the established
20/20/20/13 incremental schedule. Research bundle: `5317ab79a799897585647fb9`.
Exported package: `840957b2f8e16f1cf0f88ad2`, model `8e6eed125bebfbc8b4ced145`,
manifest pin `1873f5b6f83c11fdd232817554343d154c9735f34398058d4057db6a0f43d288`.
Its 394 templates comprise 296 supported and 98 provisional templates. It remains
in the ignored workspace; it has not been registered or selected for production.

All 71 focused messages / 126 occurrences pass exact PARAM capture checks and
native reconstruction; all six templates using the new declaration are supported.
Both larger quoted PARAMs remain whole. Full-corpus gap checks find zero field
failures, grammatical KEY captures or ties. All 16 history messages retain literal
wording; 63 date/short-character messages retain equivalent date literals and typed
character slots. All three original IS3QON errors pass Classifier/prepare_record
as supported, preserving the review shard.

The 20 stored Runs gain 13,184 formerly unmatched occurrences across 95 messages,
with no lost assignments or supported-to-provisional downgrades. Reconstruction,
identity and locator preservation pass. Full 73-log comparison: 2,476,548 supported,
118,038 provisional and two unmatched occurrences; no losses or downgrades relative
to production. These overlapping scopes must not be added. The production baseline
remains package 68f1ae5db205ab46afef9c4d, not the earlier one-shot candidate.

Human review: `.codex-tmp/marked-references-v60-final/CHANGES.html` contains the
executive assessment, 15 added templates, 15 removals grouped by successor, and
15 previously unmatched examples. Linked `FIXES.html` groups the six changed
families plus the preserved quoted family, with 14 globally numbered examples.
The main report now lists every selected predecessor before each sampled
successor, links repeated patterns/bodies instead of printing them again, and
numbers 35 unique genuine examples. Neither report has duplicate preformatted
blocks, broken anchors or missing local links; see report-verification.json.
Executive assessment: positive on reviewed evidence, with explicit remaining gaps;
coverage alone does not prove every semantic generalization. The 38 removed
production alternatives without selected witnesses remain a comparison limit.

Tools: verify_formatted_references.py,
report_formatted_references.py, compare_production_candidate.py. The comparison
now guards catalogs before/after its own read-only execution, recording earlier
catalog changes separately: v58 registration legitimately changed catalogs since
the retained v57 Run snapshot. Production selection stayed 68f1ae5db205ab46afef9c4d.
Actual retained Run documents are in `.codex-tmp/literal-v57-candidate`; later
stored-evidence files point there instead of duplicating those documents.

Two five-reset faith references occur inside surrounding faction formatting.
Their displayed labels are plain, so the complete reset run is now recognized;
reset count alone is not an exclusion. Internally nested labels, including a
character label in that same family, remain outside this simple rule.
The separate activity PARAM proposal below
also remains unimplemented. No production activation, runtime restart, source-log
or stored-Run mutation occurred. Prior runtime-restart prohibition is unresolved.

## 08C critical source-header warnings — 2026-10-04

The owner-directed `Critical Encoding issues (...)` source-validation results
and report labels are implemented. See [08C handoff](TASK08C_HANDOFF.md) for the
owning-component changes, genuine 18,837-file header scan, public API/CLI/browser
checks and evidence limits. Broader decoding/scope/beta work remains pending;
production services, package selection and unrelated learner work are unchanged.

## Adjacent-field report corrected; activity PARAM proposal tested — 2026-10-04

Owner challenged "member failure", repeated presentations and the activity count.
`review_adjacent_field_families.py` now owns the same ADJACENT-WORDS.html URL.
It scans the entire 73-log native evidence and classifies the four complete
families with the recorded production package and v58. Each family appears once;
connected predecessor/successor groups prevent repeated alternatives. Unchanged
patterns appear once, linked examples use global E01–E27 labels, and literal
examples identical to a displayed pattern link to that text instead of repeating it.
The earlier audit tool now writes INFERENCE-CHECKS.html and cannot overwrite this
family report. All links/IDs and absence of repeated preformatted blocks verified.

Corrected activity incidence: 10 distinct messages / 10 occurrences, not two.
Two was only the retained inference support of template ee7f96f3c3b501ac6180eed7;
that template actually selects four messages in the full corpus. Another template
selects three, one provisional selects one, two remain unmatched. Both production
and v58 have those same outcomes. Other family totals: flavorization 4 messages /
5 occurrences; trait 41 / 90; history 16 / 33. Counts are complete family selections,
not overlapping alternative compatibility or inference-support counts.

"Member failure" was report wording for the existing complete-match/capture-range
consistency check in patterns.py, not an owner diagnostic category. Zero does not
prove semantic slot correctness. A combined activity inference gives a genuine
example: repeated formatting markers permit two different divisions of the Feast
message into two PARAMs. The check rejects that ambiguous assignment.

Bounded proposal: preserve the full CHARACTER_FULL_ID and capture the entire
activity description between `participating in activity ` and the fixed following
`. Use `remove_from_activity` ...` sentence as one PARAM. Existing matcher gives
one complete assignment and the exact intended field for all 10 genuine messages,
including the two presently unmatched. No observed activity value contains an
internal period. Existing ordinary whole-span inference proposes PARAM but rejects
its unpaired boundaries; a contextual field declaration is the recommended fix.
This is a tested proposal, NOT an implemented learner rule or new candidate.
Core rules, immutable packages, runtime processes and production pin are unchanged.
Evidence, trace, exact examples and checks: adjacent-word-audit/families.json and
family-report-verification.json. Initial probe import used the wrong helper module;
corrected to matching_defaults before running the successful test. Restart approval
remains unanswered; do not activate v58 while treating this newly identified gap
as already fixed.

## Adjacent-word rule scope audit delivered — 2026-10-04

Owner requested all affected templates, two genuine examples each, the three
other adjacent-field patterns, and exact enclosure exclusions. Delivered
`.codex-tmp/coupled-words-v58-candidate/adjacent-word-audit/ADJACENT-WORDS.html`
with JSON evidence via `tools/template_learning/audit_coupled_word_inference.py`.
Scanned all 91,925 contextual rows / 2,594,588 occurrences; replayed the final
400 template member groups (37,123 distinct supporting records), with zero
member failures and zero coupled-word triggers in those already-separated groups.
The combined 16-message history pool triggers once, proposing and rejecting
PARAM values `after death`/`from before`. This focused pool is not an invocation
log of every temporary proposal from the historical incremental build.

Exact v57/v58 exported-template comparison: all 400 IDs and literal/slot layouts
are identical. 398 whole template entries are identical; only construction_id
changes on the two history templates, from specific construction names to null.
No other changed final formulation was found. All 97 PARAM and 31 REASON slots
in final body patterns, wrapper declarations and repeated layouts are unchanged.

The prior "three other adjacent-KEY patterns" inventory consists of flavorization
character names, displayed history trait names, and activity names. All remain
unchanged and fail the alphabetic-only gate because of hyphens, controls or
possessive text. That inventory was NOT three additional rule successes and does
not endorse their semantic KEY typing. Report includes two distinct genuine
examples of each of these three patterns and each history template (10 total).
All 10 independently select their displayed supported templates through the
retained package matcher. Initial audit lookup confused evidence example IDs with
record-key IDs and stopped at an assertion; corrected before report delivery.

The enclosure gate checks matched markers immediately around the whole proposed
span, ignoring gap pieces. It is not a blanket exemption for every substring
anywhere inside ()/[]/quotes. Declared/empirical/inference-owned fields and REASON
types are excluded earlier. No new core inference rule or immutable artifact was
changed by this audit. Activation remains pending the earlier restart question;
this owner follow-up did not authorize a restart.

## v58 replacement prepared; runtime activation pending — 2026-10-04

Owner authorized pinning the completed replacement with its parser/matcher.
Registered unchanged package `f23424ed8aa4d910bf4d3223` under `models/releases/`
(publication order 7) and its complete frozen learner release `2951fe80...`
under `learners/releases/` (order 8). Catalog registration does not activate it.
The exact proposed selection and old selection are preserved in
`.codex-tmp/v58-production-promotion/`; current active selection remains
`68f1ae5db205ab46afef9c4d`.

Ten release-selection checks passed, including public contract preparation on
genuine IS3QON evidence for all retained available packages. Runtime logging
ownership passed. Wheel build passed; verified 327 packaged files byte-for-byte,
including the application renderer. Code extracted from that wheel classifies
all three original errors as supported and prepares their exact native contracts.
No production Runs, protected logs, old packages or runtime processes changed.

The existing handler is PID 23252, instance ca3faf45a4514e5cab542769c2a3c70f;
its October 2 startup predates the required repeated-locator/date renderer.
The old application imports contracts at startup, so a pin-only switch is unsafe.
The owner was asked to resolve the earlier explicit no-runtime-restart restriction
for the final controlled watcher/handler restart and pin switch. Await the answer;
do not infer permission from elapsed time. This is the only activation blocker.
After activation, rebuild/verify the wheel with the new default selection and
update this status. Use the existing runtime activation procedure; do not replay
historical Runs. Full identities and publication evidence are in
`docs/LEARNER_PARSER_PIPELINE_HANDOFF.md`.

## Completed continuation — 2026-10-04, reusable history inference (v58)

Continuing the unresolved implementation, not stopping at the delivery recap.
Removed the two v57 history constructions. In patterns.py, adjacent alphabetic
KEY proposals that vary only together, outside an enclosing pair, are reconsidered
as a complete span. Existing field-boundary assessment rejects an unmarked phrase
and literal refinement preserves its variants. Explicit fields, identifier syntax,
optional values, line breaks and observed independent variation are excluded.
No phrase, emitter or function-word list is encoded by this correction.

The retained 16 history messages / 33 occurrences reproduce KEY KEY with frozen
v57 after ablating its two construction gates. Frozen v58 produces two supported
literal templates, both construction_id=null. The actual final build agrees.
Traces are history-inference-{baseline,correction}.json in the new workspace.

COMPLETE: .codex-tmp/coupled-words-v58-candidate contains the full 73-log
20+20+20+13 incremental build, authenticated export, production comparisons and
human reports. CHANGES.html has 15 added templates, 15 removed templates in
complete successor groups, and 15 previously unmatched-message examples.
LITERAL-CORRECTIONS.html explains the reusable history inference; FIXES.html,
REMOVALS.html, REMAINING-REMOVALS.html and FUNCTION-WORDS.html cover the remaining
verification and semantic crosswalk. Review this candidate before release/pinning.

Package f23424ed8aa4d910bf4d3223; model 0f4a012e91e6ffa253d9d858;
manifest SHA-256 504710350c8f87666f0358fbacc35f85e4e50045e1cee5d270d25e63ea377c21.
Research revision 6ea0b0b5157f318030756507. Release receipt:
.codex-tmp/coupled-words-v58-release.json; release
2951fe80c0dd31a83cd639562a427d2658daaeab30279dcd15d32069ea1f2d8a;
implementation 30400ed4c65b1101e705ce8a47fea86ef11cf22cd5be7d4f9610916487a1ee43.
Current implementation agrees with this frozen release.

Verification: 400 templates (300 supported, 100 provisional), 207 added IDs,
496 removed IDs and 193 unchanged versus production. The same 20 stored Runs
gain 11,495 assignments / 94 distinct messages; zero losses/downgrades, identity
collisions, reconstruction failures or changed existing LOCATOR captures.
All 73 training logs: 36,833 provisional occurrences become supported, two
unmatched occurrences become supported, zero losses/downgrades. Two occurrences
remain unmatched as in production. Export parity checks 371,538 captures over
91,925 contextual messages / 2,594,588 occurrences, with zero changes.
All original three IS3QON errors pass public Classifier/prepare_record as
supported; all 75 saved short-character/date cases pass; all history/date literal
and exact-rendering checks pass. Full function-word audit and field checks show
zero demonstrated grammatical KEYs or template ties. The seven residual removal
cases remain three families / 676 messages with identical production/candidate
captures; 31 other no-selected-witness removals were already addressed.

The obsolete report_removed_templates.py renderer failed its historical
location-only-difference assertion on construction_id changes; no report from
that invocation was delivered. Current report_gap_candidate.py owns the up-to-date
REMOVALS report. Its output and the other five pages pass sample/link/anchor
checks; no new visual screenshot verification is claimed. A probe initially used
the wrong implementation-identity dictionary key, then passed with its actual
sha256 field. These were tooling checks, not failed candidate classifications.
The last learning stage took 685 seconds versus 285 previously; CPU progressed
and artifact creation completed. No cause for the elapsed-time difference was
established. The resulting research model is about 104 MB, not the old 11 GB.

No assigned implementation/test/report deliverable remains open from this
continuation. Contextual effect/trigger cue, rare-message pass and adoption of a
sliding threshold remain deferred; the requested threshold experiment is already
complete. Production packages, processes, source logs and Runs remain untouched.

## Earlier v57 delivery status — superseded by completed v58 above

The current review/test deliverables are COMPLETE: disposable v57 candidate built
on the 73-log incremental schedule; production comparison and human-readable
samples; grouped many-to-one removals; complete-marker effect/trigger survey;
and the specified sliding-threshold experiments with their precise scope and
limitations. All three original IS3QON diagnostics have supported assignments.

The overall exercise is NOT CLOSED: the owner rejected the history-wording
implementation, and no replacement mechanism has been delivered. Do not describe
successful literal-output verification as resolving that objection or as making
the candidate ready for production release.

The additional contextual cue and rare-message pass are deferred. The marker
survey shows no demonstrated need for a broader exemption now. A sliding policy
was tested but not adopted; the requested experiment is complete. Broader catalog
retirement and the two unchanged unmatched training messages are disclosed
limitations, not newly commissioned deliverables. Production release/pinning
remains intentionally unperformed. No new implementation or build this turn.

Close future delivery updates explicitly with completed deliverables, unresolved
assigned work, and intentional deferrals. Do not leave the owner to infer whether
work is finished or require reminders to produce already-requested reports.

## Owner deferrals and marker evidence — 2026-10-04

The contextual effect/trigger cue is deferred: existing learner changes address
the demonstrated category-wording problem; absence of that particular proposed
cue is not itself outstanding required work. Rare-message pooling is explicitly
low priority and deferred. Do not keep either on an urgent implementation list.
The owner requested genuine evidence for effect/trigger inside ()/[] before
considering a broader marker exemption. No such exemption is implemented now.

Re-ran the owning survey against v57's full 73-log native evidence: 91,925
contextual rows / 2,594,588 occurrences. Found 4,494 standalone effect/trigger
token positions inside matched ()/[], across 4,218 distinct messages / 306,193
message occurrences. Nearest enclosing pair: ()→PARAM 3,674 positions,
()→REASON 102, []→REASON 718. No enclosed literal, KEY or unassigned hit.
There are 34 selected templates and 46 template/word/marker/role combinations;
each combination has a genuine witness replayed through the authenticated v57
matcher, with exact capture-byte checks. The 102 parenthetical REASON cases are
inside a larger opaque reason, not evidence requiring another PARAM boundary.
The survey excludes identifier substrings and unmatched delimiters. Report and
complete patterns/captures: .codex-tmp/literal-v57-candidate/
category-word-marker-review.html and .json. This confirms no demonstrated need
for the proposed broader exemption in the surveyed corpus, not all future logs.

Clarified the exact sliding test in .codex-tmp/short-threshold-review/REVIEW.html.
The baseline was the CURRENT policy, not plain .72 everywhere: equal-length
1–2-unit sequences without quoted-value positions use ≥.49 same-position
agreement with at least one equal position. This positional rule is not the
weighted similarity score; the quotation branch bypasses it. Both trials keep
it unchanged and vary weighted-score cutoffs for lengths 3–6 only:
gentle .68/.69/.70/.71; lower .60/.63/.66/.69 versus baseline .72. A .713333
five-unit comparison changes admission in both trials; the lower trial also
admits a .6725 audio pair, later kept separate by inference. Tests preserve
proposal retrieval, construction boundaries and guards. They cover initial
discovery/refinement on the short-message subset, not a full incremental model
or an expanded proposal-search strategy. No new learner policy or production
change this turn; survey/report tooling and guidance only.

## Current learner improvement inventory — 2026-10-04

Checked current source against frozen v57 implementation identity
e0f56450eb75fd156567dd643454dfceb16d59ba3096b04b40737a730173291f;
they still agree. Earlier dated recommendation tables describe older candidates
and must not be presented as the current missing-work list.

Outstanding implementation/proposal distinctions:

1. Contextual `_`/`.` identifier + effect/trigger cue: surveyed, not implemented.
   The intended cue makes the preceding identifier KEY and the following category
   literal, excluding enclosing PARAM/REASON regions. Existing behavior already
   leaves all 8,302 surveyed category positions literal; 14 predecessor positions
   remain literal. Their raw v57 examples are in LITERAL-IDENTIFIERS.html. Do not
   call all 14 misclassifications without considering their contexts.
2. General marker-aware exemption in the wording-loss safeguard: not extended to
   newly proposed PARAMs. Existing opaque fields are excluded; the enclosed
   identifier exception currently permits KEY/OPTIONAL_KEY only. This is an
   identified code limitation, not a demonstrated remaining v57 failed assignment.
3. History after-death/from-before implementation: v57 uses hard-coded separate
   constructions and passes literal-output checks; the owner rejects the
   implementation. No revised mechanism has been implemented. The separate
   Parent-state PARAM correction is implemented, not part of this missing item.
4. Sliding similarity: two isolated genuine-corpus experiments are complete.
   No curve was adopted, and no full incremental candidate with a sliding policy
   was built. Both curves simplify initial grouping of 15 messages already
   assigned to the same whole-expression template in production and v57. No
   demonstrated selected-classification gain; keep this distinct from untested.
5. Separate rare-message pooling/additive pass: proposed, not implemented as a
   rarity-selected workflow. Existing additive learning already pools cumulative
   provisional/unassigned evidence; inclusion of rare source logs was corrected
   and the candidate has completed the full 73-log incremental schedule.
6. Broader retirement of redundant overlapping templates: not implemented beyond
   existing exact-identity consolidation and fixed KEY specialization retirement.
   Three unselected narrow name templates and four GUI alternatives remain in
   v57. This is a proposed reusable catalog simplification, not an identity or
   occurrence-count defect and not an instruction to delete unwitnessed templates.

Untyped construction applicability is now explained with both genuine header
variants; no agreed code replacement is waiting. The three-family removal report
is corrected, with all predecessors before one shared replacement; it is not a
template approval queue. Two training messages (two occurrences) about activity
participants aborting travel remain unmatched in both production and v57; the
saved comparison demonstrates the residual coverage gap, not its cause or a
ready correction. Do not confuse them with the three original IS3QON cases,
all of which now receive supported assignments.

Implemented and verified in the disposable candidate: quoted-value-neutral
ordered similarity; bounded regrouping and identical-template consolidation;
variable-count ending locator handling with one presence unit and exact identity
retention; contextual Unknown/marker recognition; trace PARAMs; equivalent literal
game dates; short and marker-bounded super-short character identities; default
location PARAM through line end; Unknown effect/trigger category separation;
the scoped comparison/expected-scope/formatting-tag/name-field corrections and
Parent-state PARAM; full-corpus function-word audit; incremental 73-log build and
production comparison; refinement-history deltas and bounded bundle writing.
No production release/pin activation has occurred. This inventory review changes
documentation only, not learner behavior or model artifacts.

## Consolidation report layout — 2026-10-04

Owner explicitly requires all removed predecessor templates together, followed
by their one shared replacement. Implemented in `review_unselected_removals.py`
and regenerated REMAINING-REMOVALS.html: missing-name now shows all five full
production patterns, then the single retained supported PARAM template. The
other two families use the same grouped layout. Counts and examples follow the
consolidation; no learner/model behavior changes. The replacement's prior
existence in production is identified explicitly.

## Owner correction: review learner behavior, not template approval — 2026-10-04

The owner does not approve individual templates. The learner determines supported
and provisional status; owner review concerns learner/matcher code and outcomes.
Approval for production release remains separate. Say "disposable candidate
model" and show actual template and assignment status; do not use "candidate"
ambiguously for a rejected hypothesis or an unapproved template.

Corrected the misleading seven-removal report in place:
`.codex-tmp/literal-v57-candidate/REMAINING-REMOVALS.html`. The owning tool,
`review_unselected_removals.py`, now groups by message family and evaluates actual
selected production AND v57 assignments across the entire 73-log family. Counts
for an old alternative measure overlapping compatibility sets, not selections
or occurrences of the repeated sample. No learner identity/counting bug was
demonstrated. All family rows have distinct native identities and unchanged
selected capture types, contents and spans between the two authenticated models.

- Missing loc for name: 630 distinct messages / 1,116 occurrences, all selected
  as supported template 5093f36599ce2356a1e6433e by BOTH models. There are 574
  distinct name PARAM values. Five old alternatives have overlapping counts
  75/159, 53/133, 551/1005, 74/158 and 54/134 (messages/occurrences), with union
  572/1030 and common intersection 53/133. None was selected. The exact
  Abd al-Aziz / 1235023 message occurs three times and fits all five; the report
  repeated it, not the stored message identity. Noriko's trailing space explains
  the optional-versus-mandatory one-message difference. Twenty-one two-word-name
  cases have nonnumeric character IDs, explaining the KEY-versus-VALUE difference.
- Scope-dependent localization: five messages / 180,998 occurrences, four
  leading identifiers. Both models already select the same KEY pattern/captures.
- GUI Failed-parsing-data-statement: 41 messages / 63 occurrences, 35 distinct
  statement PARAMs and seven property values. Both models already select the
  whole-statement PARAM pattern. The old page displayed only one witness because
  it restricted sampling to one removed literal alternative. The new page shows
  12 diverse genuine messages and all 35 exact PARAM values.

The owner considers the displayed generalizations better; this is feedback on
learner output, not case-by-case template approval. Production already selected
those generalized patterns too: the actual change here is catalog simplification,
not improved selected classifications. Additional unselected narrow templates
remain in v57 (three name variants and four GUI variants). They are disclosed as
residual catalog redundancy, not duplicate stored messages. Do not delete them
solely because they lack selected witnesses in this finite corpus. A broader
retirement change needs a reusable containment proof. No core learner/matcher
policy, immutable release, production pin, Run or source log changed this turn.
Evidence: removal-family-evidence.json and removal-family-summary.json adjacent
to the corrected report. Earlier "seven remaining for approval" framing below
is superseded. The short-threshold report links the corrected family explanation.

## Active owner review — 2026-10-04, after v57

The owner rejects the current after-death/from-before implementation. Do not
equate verification of literal output with approval of the two hard-coded
constructions. Clarification is pending on whether the objection concerns that
mechanism while the literal wording requirement remains. No new history rule
has been implemented in response. The immutable v57 candidate remains unchanged.

Owner explicitly requests a variable similarity threshold experiment now; the
earlier conditional deferral no longer applies. `review_short_thresholds.py`
performs isolated short-message discovery/refinement experiments using genuine
73-log evidence, not a replacement incremental model or production coverage
claim. Results are retained in `.codex-tmp/short-threshold-review`.

Experiment completed: 46,393 underlying short messages from 46,419 contextual
rows (1,845,193 occurrences), drawn from all 91,925 rows in the 73 logs. Baseline
0.72 yields 223 inferred templates in this subset. Both tested curves yield
221, consolidating 15 Failed-converting-statement messages into an already
inferred whole-expression PARAM template; no new template identities. Gentler
thresholds at lengths 3/4/5/6 are .68/.69/.70/.71; the lower curve uses
.60/.63/.66/.69; other lengths retain .72 and existing <=2 special handling.
The decisive score is .713333 at length five. The lower curve also admits an
audio stop/check-isPlaying comparison, but later inference keeps those separate.
All members match their inferred body patterns. Untouched source pools are
reused only after tracing every baseline comparison and proving neither curve
changes an admission there. No incremental build or complete assignment claim
is made for this experiment. Crucially, authenticated production and v57 matchers
already select the supported whole-expression PARAM template on all 15 changed
messages. Thus there is no demonstrated current selected-classification gain.
Report: `.codex-tmp/short-threshold-review/REVIEW.html`; raw experiment results,
comparison, and 15-message runtime checks are adjacent. No learner policy changed.

The 38 removed production templates with no selected witnesses narrow to seven
templates in three families not already covered by accepted changes: five
missing-character-name localization variants, one house_equal scope-dependent
localization template, and one GUI data-statement template. The other 31 are
covered by owner-directed field corrections/accepted generalizations, not 31
separately approved IDs. Direct complete matching over all 73 logs found genuine
witnesses for every one of the 38; all have complete candidate assignments.
See `.codex-tmp/literal-v57-candidate/REMAINING-REMOVALS.html` and
`unselected-removals-review.json`. Do not call these missing-coverage cases.

Untyped clarification verified against v57: plain-header template
4ac751de53c2454d5094602a is applicable and complete; generic
acf0016a118519e25fc1557c is inapplicable by construction exclusion. A genuine
tooltip/description-header message instead uses generic
4ebf2338bc94781fc5627440; the exact dedicated rule does not recognize that header.
Both branch traces and source provenance are saved in
`.codex-tmp/literal-v57-candidate/untyped-applicability-review.json` and shown in
the new review report. Do not describe all untyped messages as dedicated-only.

## Latest owner correction implemented and verified — 2026-10-04, v57

The sample numbers refer to v56 CHANGES.html: removed sample 6 is production
template 0ebbfabd31d46b3ad046b464, removed sample 11 is the history formulation,
and newly classified sample 3 is the Wijayatunggadewi travel diagnostic.
Do not confuse them with the separate fourteen-case review numbering.

Owner explicitly changes history direction: after death birth / from before
birth remain literal, superseding the earlier relative-phrase PARAM rule.
Implemented separate construction applicability, preserving both phrases during
initial inference and later matching. The separate Parent-state PARAM remains.
The date KEY implementation was incorrect: formatted game dates now occupy an
equivalent literal position, with exact spelling retained in literal_choices,
rendering and identity. The ordinary dotted-date KEY and outer timestamp are
unchanged. This includes a backward-compatible contract-renderer extension;
future activation requires that application change as well as the new package.

Genuine preflight: 63 date messages / 63 occurrences, 16 history messages / 33
occurrences. Both history formulations remain literal; date values are not slots.
All eight other explicit fields and 2,643 full-ID captures are preserved across
91,925 contextual rows. Runtime logging ownership and diff whitespace checks pass.

Raw sample 6 evidence: Key is missing localization: Ymerodraeth Lân Rufeinig
(three occurrences), and Yr Ymerodraeth Rufeinig (four). The removed OPTIONAL_KEY
template completely matches both, but production selects a three-KEY template.
Candidate captures each whole value as PARAM. Owner accepts removing the flawed
template as an improvement. Absence of a selected predecessor witness does not
mean absence of raw supporting examples. These messages contain no character-ID
parentheses or markup; do not infer a character identity from names alone.

Frozen v57 receipt: .codex-tmp/literal-v57-release.json; release
823909dc65f3093911cc12cd8ff20574fd6267de623c22baf143144067761f72,
manifest a95b5e6670a17b4c3351c3f90e2affcdfa4e2eb392b638dab3fe786ba93d9e63.
Build workspace .codex-tmp/literal-v57-candidate, using the retained same 73
inputs and 20+20+20+13 schedule. All checkpoints and publication completed.
Research revision 434b4e66b2fb4c476fe13213; package 53c4fdd5e5d0265714016450;
model d52938cb774206d0e62ed4ca; package manifest pin
0c1964615955b292863f365a1c619398305638b48438c7c9d1c029164a6d8f15.
There are 400 templates (300 supported, 100 provisional). Production comparison
has 207 added IDs, 496 removed IDs and 193 unchanged IDs; counts alone do not
establish quality. Same 20 Runs: 11,495 newly classified occurrences, no losses
or downgrades, no reconstruction failures or identity collisions, and unchanged
LOCATOR captures. Same 73 training logs: 36,833 provisional-to-template upgrades,
two newly classified occurrences, no losses/downgrades, two remain unmatched.

Frozen package checks: all 75 genuine date/character messages use one supported
template, with exact date spellings in literal_choices and no date slot. All
16 history messages / 33 occurrences retain literal formulations. Both raw
localization values match complete PARAMs. All original three IS3QON diagnostics
pass public Classifier/prepare_record as supported templates. Full eight-field
verification has zero failures, zero demonstrated grammatical KEYs and zero ties.
Export parity checks 371,538 captures with zero changed matches/outcomes.
The 75-case date corpus includes examples beyond the 63 dates in training;
the Wijayatunggadewi example is in that broader corpus and the original review.

Human reports: .codex-tmp/literal-v57-candidate/CHANGES.html and
LITERAL-CORRECTIONS.html; detailed field and removal reports remain linked.
Report checks pass all 20 local links and 15/15/15 samples across five pages.
Optional screenshot verification could not complete: isolated headless Chrome
failed GPU initialization; the in-process-GPU retry timed out and its owned
process was stopped. Do not claim visual inspection passed. This does not affect
the completed learner/matcher, identity, rendering or production comparisons.
No production pin, Run, source log or runtime process is changed.
The earlier contextual effect/trigger cue remains a surveyed proposal, not a
new v57 implementation. Only the date/history corrections are added this turn.

## Contextual effect/trigger proposal: status clarification — 2026-10-04

Owner confirms the proposed cue means: a preceding identifier containing `_`
or `.` becomes KEY, while the following effect/trigger remains literal. This is
additional evidence for discovery, not a replacement for other discovery.
Exclude occurrences inside parameter/reason markers or existing opaque fields.
**This new cue and a new general marker exemption have not been implemented.**
The last two turns added/revised survey tooling only; v56 remains the candidate.

The original 8,302-position survey checked the following category word only.
The expanded predecessor audit finds 8,288 preceding KEY positions and 14
preceding literals, while all 8,302 following category words remain literal.
The 14 literals are eight add_domicile_building cases, one each of
equip_artifact_to_owner_replace, fire_councillor, trigger_situation_catalyst,
vassal_contract_set_obligation_level, can_recruit and is_shown. They have complete
assignments; do not claim 100% implementation of both halves of the proposed cue.
An intermediate progress note incorrectly described all twelve effect cases as
add_domicile_building based on the first three samples; the full predecessor
inventory above corrects it.

All surveyed effect/trigger tokens inside matched ()/[] are already PARAM or
REASON contents in v56. Genuine `start_war effect [ No valid titles found for
start_war effect ]` establishes why marker/opaque-field ownership must take
precedence over the proposed cue. Default literal guidance is still disabled.
The older revision safeguard's enclosed-evidence exception covers KEY/OPTIONAL_KEY
but not new PARAM proposals. This is a code-level limitation to investigate,
not a demonstrated remaining v56 misclassification or an implemented fix.
`if effect` was described as genuine emitted wording, not a claim that a script
was valid; citing Unknown effect as a limitation of an additive cue was misplaced.

Evidence: `category-word-contexts.json` and
`category-word-contexts-with-predecessor.json` in the v56 candidate workspace;
reusable survey: tools/template_learning/survey_category_word_contexts.py.
Older dated entries below record earlier states; completed v56 work supersedes
their pending implementation/build statements.

## Owner gaps implemented and verified — 2026-10-04, v56

Owner explicitly directed implementation, not another proposal. Executable
owner-rule declarations now cover nine reviewed fields: history relative PARAM,
Parent-message state PARAM, formatting-tag PARAM, comparison side/identifier KEYs,
compare-trigger identifier/expected-scope KEYs, complete missing-localization
display PARAM, and complete marked Cheater/With character-reference PARAMs.
All native values, controls and presentation whitespace are retained. Full
73-log preflight passed all 91,925 contextual rows, preserving 2,643 full-ID
captures. The larger missing-localization retyping affects 19,288 fields / 97,451
occurrences and must be disclosed separately from coverage gains.

Retained v54 code reproduced all four originally disputed case 7–10 templates.
Unknown effect/trigger enter the same initial group at similarity 0.83636 > 0.72;
the first derive_pattern assigns their categories KEY. No previous literals
exist yet for the revision guard. The later Unknown/Unexpected merge is rejected.
v56 adds two explicit category-preserving constructions; a replay of the same
genuine source pool verifies history PARAM and fixed effect/trigger categories
already at initial discovery. No fresh-versus-incremental outcome comparison.

A v55 attempt was stopped after its 20-log build when this cause was established;
its running session and child processes were terminated through exec Ctrl-C.
Do not resume it. Current build: `.codex-tmp/owner-gaps-v56-candidate`, same retained
20+20+20+13 schedule via mirror_incremental_build.py --basis. Frozen release:
f274b62cfeb1b0151944d5dd8f326cefe5134f220017947ce4433fc9d2245683, manifest pin
9809e62fc11f4ad111641239960f4adb22df6ea7e922cc5b8ac13df65ec1771f. Receipt:
`.codex-tmp/owner-gaps-v56-release.json`. All four checkpoints and publication
completed; build session 37790 exited successfully. No build remains active.

Candidate package `3f5e1736f30ca4a1c94cbe5e`, model
`e00251c9a5de51b76b8c7f22`, manifest pin
`cc3f36a2c0b2b24f9b9bc605f6d1235ea18e33f5eea9ced6df74b7a2b6d3546f` lives under
`.codex-tmp/owner-gaps-v56-candidate/packages/`. Research revision:
`9c19654e784f3b5fcc371aa8`. It has 399 templates: 299 supported and 100 provisional.
Production remains package `68f1ae5db205ab46afef9c4d`.

Production-only verification, using the retained same evidence and schedule:

- 20 stored Runs: 11,495 newly classified occurrences (94 distinct contextual
  messages); no lost assignments or template-to-provisional downgrades. Another
  72 provisional occurrences become template assignments. All original three
  IS3QON messages pass public Classifier/prepare_record as supported templates.
- 73 training logs: all 91,925 contextual rows / 2,594,588 occurrences joined
  against the existing production ledger. No lost assignments or downgrades;
  36,833 provisional occurrences become templates, two unmatched become templates,
  and two remain unmatched. These scopes overlap and must not be added.
- All nine declared field checks pass exact value/type/boundary assertions.
  No demonstrated grammatical KEY splits and no template ties remain. Every
  required owner-pattern check passes. Unknown effect/trigger stay literal over
  445 / 67,740 training occurrences. Native export parity checks 371,617 captures
  with no changed matches or outcomes. Existing locator captures, reconstruction,
  and message identities pass; no parser change.
- Full function-word audit: 378 contextual rows / 2,401 occurrences, 285 bindings
  across 25 templates remain flagged by spelling. Context review finds reported
  identifiers/functions/properties/types/tokens (368 / 2,390), trait/display
  markup spellings (3 / 4), and May within dates (7 / 7), not the corrected
  grammatical phrases or fragmented name fields. This is the stated vocabulary
  audit, not proof of every possible English grammatical case.
- Inventory: 206 added IDs, 496 removed, 193 unchanged. 458 removed IDs have
  observed successors; 31 many-to-one groups involve 315 removed IDs. The 651
  genuine public-matcher witnesses cover all 466 observed mapping pairs across
  the two scopes. Location-role changes and diagnostic slot/literal changes are
  reported separately. **38 removed IDs lack a selected witness**, so replacement
  equivalence remains unverified. Untyped construction acceptance remains pending
  owner review. Do not claim every removal is approved or uniformly beneficial.

Reports in the candidate workspace: CHANGES.html (15 added, 15 removed, 15 newly
classified examples), FIXES.html (all fourteen cases and exact field captures),
REMOVALS.html (many-to-one mappings and role changes), FUNCTION-WORDS.html
(complete residual contextual inventory). Both main pages rendered successfully
in isolated headless Chrome and were inspected. Report generators and reusable
checks live under tools/template_learning. The comparison joins native IDs/counts,
not hashes of assignment-bearing files whose assignments legitimately changed.

Assessment: positive on verified evidence; owner review is still required before
release/pinning. No production package, selection, catalog, Run, protected source
log or runtime process was changed. Preserve the reviewed production-capture
finding below: whole-name improvements fix inherited limitations, not a newly
introduced candidate regression.

## Name-field production comparison clarification — 2026-10-04

Owner challenged whether the 107 flagged multiword-name cases were introduced
by the candidate. All 107 messages / 332 occurrences were replayed through both
pinned public matchers. Every flagged name capture already exists in production
with identical type, value and native byte span. Across 106 rows / 331 occurrences
all capture roles are unchanged. The remaining of Suffolk case changes only
diagnostic `target` from literal to KEY; its name captures are unchanged too.
Production already splits Antiochia/in/Pisidien and The/Isles using exactly the
same template IDs as the candidate. The Hampshire/Suffolk names also already
split of and the place name in production. Earlier recommendations did not
distinguish inherited name-field handling from candidate regressions clearly
enough. Treat whole-name recognition as an inherited improvement opportunity,
not a newly caused regression. Evidence/report:
`.codex-tmp/production-incremental-v54-candidate/name-capture-production-comparison.json`
and `NAME-COMPARISON.html`. Reproducible tool: `inspect_name_capture_changes.py`.
No inference/model/production changes.

## Residual KEY survey and consolidated recommendations — 2026-10-04

Owner allows hard-coded handling of the demonstrated phrases but requires a
remaining-incidence survey and concrete recommendations for earlier concerns.
The survey/recommendations are now in
`.codex-tmp/production-incremental-v54-candidate/RECOMMENDATIONS.html` and
`owner-recommendations.json`, generated by `report_owner_recommendations.py`.
No new learner rule, model build, production activation or Run change this turn.

All 313 flagged template/slot/value bindings across 33 templates were reviewed
contextually; the same 91,925 native rows were scanned to count each message once.
The 720 flagged rows / 3,221 occurrences partition into:
- grammatical diagnostic phrases: 235 / 488, three templates;
- multiword name/display-field boundaries: 107 / 332, five templates;
- identifiers/reported values: 365 / 1,862, twenty templates;
- display/markup spelling coincidences: six / 532, four templates;
- month May inside the declared date field: seven / seven, one template.

The two phrases cover the grammatical diagnostic-wording defect detected by the
explicit inventory; they do not fix the remaining name-field fragmentation.
This is not a claim of universal English grammatical classification. Propose
context-bound whole PARAMs for hasn't been born / the wrong gender in the
observed Parent (…) of … is … at file: formulation, plus the already directed
has history PARAM between has history and birth, won't execute. Do not turn
function-word spellings into a global KEY prohibition.

The report lists all fourteen owner cases against production/current incremental
patterns. Do not claim all accepted generalizations are delivered: case 2 retains
a literal left/scope variant; case 7 still has two literal history phrases;
case 12 retains expected character/war literals; case 14 still has a KEY template
and a literal control-character template rather than one PARAM. Cases 8/9 remain
separate like production; optional consolidation need not be forced. Case 10
effect/trigger remains literal, but the requested causal trace of the earlier
rejected outcome is still outstanding. Case 5 remains pending owner acceptance.
Retain verified locator/date/identity gains and cases 1/3/4/11/13. Resolve the
two supported-template ties before promotion; 18 removed IDs have no selected
witness. Recommended follow-up is a frozen corrected learner, same incremental
schedule, production-only comparison, and semantic/field checks alongside coverage.

## Expanded function-word KEY audit — 2026-10-04

The owner reiterated the request to identify the grammatical categories and find
KEY assignments containing such wording, including `hasn't` / `has not`. The
earlier finite-word audit omitted contractions and articles; its results below
must not be presented as an exhaustive grammatical audit.

`audit_key_bindings.py` now searches categorized prepositions/connectives,
auxiliary forms, negation, contractions, pronouns/determiners/articles and related
adverbs. Whole-value and within-value hits are distinguished; exact values and
UTF-8 spans are preserved. All selected assignment regions are visited. The
73-log retained evidence contains 91,925 contextual rows / 2,594,588 occurrences
and 97,976 nonempty selected KEY captures, all in bodies. Every selected body
capture's native byte span was checked. Search hits: 720 contextual rows / 3,221
occurrences, 313 template/slot/value bindings across 33 templates. These include
identifier/name/date spelling coincidences, not 720 confirmed typing errors.

Confirmed grammatical phrase splitting: `hasn't been born` becomes three KEYs
in 154 messages / 371 occurrences; `the wrong gender` likewise in 81 / 117.
Three characterhistory.cpp templates contain these alternatives. Existing
production witnesses establish inherited grammatical KEYs. Historical v34
regrouping traced the same phrase-pair defect, but do not assert that branch
caused the current outcome without tracing today's decisions. No taxonomy
category called a parent diagnostic is introduced; Parent is game wording.

Full inventory and genuine phrase context:
`.codex-tmp/production-incremental-v54-candidate/function-word-audit.json` and
`FUNCTION-WORDS.html`, generated by `report_function_words.py`. Before/from/has
are absent from selected KEY captures; after occurs in reported identifiers.
Whole-field concerns also occur in multiword display names. Function-word use in
ordinary diagnostic grammar must not become independent KEYs. Identifier-position
spellings are distinct evidence. Trace the three affected templates and pursue
a reusable phrase-level correction, keeping the owner-requested history PARAM
case in scope. No learner inference, candidate or production package changed in
this audit. Do not resume the one-shot-versus-incremental comparison.

## Production-to-incremental semantic investigation — 2026-10-04

**Owner correction: compare production with the incremental candidate only.**
Matching the build schedule was a control for that comparison, not a request to
investigate the one-shot build. Do not resume the fresh-versus-incremental work
described in the historical section below. An unexecuted exploratory script for
that wrong scope was removed. Neither candidate nor production was changed.

Current review: `.codex-tmp/production-incremental-v54-candidate/SEMANTICS.html`;
`CHANGES.html` now uses the same production-only executive assessment and retains
the 15 added / 15 removed / 15 newly classified examples. The separate historical
BUILD-HISTORY report is no longer the active review direction.
All local report links, 17 new-match groups and sample counts passed checks;
SEMANTICS rendered in Chrome and was visually inspected. Receipt:
`semantic-report-verification.json`.

Every one of the 81 newly classified stored messages (6,063 occurrences) was
replayed through both pinned public matchers. **6,048 occurrences / 66 messages**
have the same displayed diagnostic in production; every corresponding production
layout fails the parameter-structure applicability gate solely because its count
of trailing `located-parenthetical` traces differs. Source/context/construction
agree. Candidate repeated-locator matching preserves the diagnostic and captures
every original location. Biggest group: 5,236 occurrences with three locations;
production has the same KEY diagnostic with one or two. The other gains are 13
travel identities, one original quoted scope mismatch, and one marked-up-name
message requiring typing review. Rejected history/effect-trigger KEY patterns do
not drive these gains. Exact evidence: `production-gain-traces.json`.

622 public-matcher witnesses cover 430 of 448 removed IDs, 438 pairs and 195
destinations; 18 removed IDs have no selected witness. Disjoint primary changes:
144 identical displayed patterns; 138 location/layout changes with unchanged
diagnostic word roles; 139 literal-to-slot; eight slot-to-literal; one type change.
27 many-to-one groups involve 263 removed IDs. The report shows every predecessor
in each group and genuine capture changes. `removed-template-analysis.json`.

Both training template-to-provisional occurrences were individually replayed:
`di Urbino` and `di Rienzo`. The same two supported templates tie at rank
`[0,0,0,-2]`: generic `32c2191f6fdd59776673222b` and literal-di
`dbbfc518e0d2d4ded54722fd`. Selected captures are unchanged; no capture ambiguity.
This is a template-overlap/selection issue, not lost support or data. The first
report had one witness for the pair; `production-downgrade-traces.json` now includes
both complete matcher inspections, production assignments and capture comparisons.

Full 73-log audit: 91,925 contextual messages / 2,594,588 occurrences. `after`
occurs as a KEY in four event/namespace messages (five slot bindings), not grammar;
`before`, `from`, `effect`, `trigger` absent from selected body KEY values. `been`
occurs in 154 CK3 messages beginning `Parent (…) of …` / 371 occurrences. Three exact public
production witnesses establish the same grammatical KEY capture already existed;
same displayed production patterns cover these families. Multiword localization
`in`/`do`/`of` also uses an unchanged production template. No stop-word ban.
`key-binding-audit.json`, `inherited-key-witnesses.json` retain counts and context.

Assessment: mostly positive **versus production**, with overlapping name templates,
inherited phrase/name typing limitations, and unobserved removed-ID successors
remaining. No inference changes or model activation in this investigation.
Recommended next investigation concerns the overlap's retention/selection history
and coherent name/phrase typing; keep the requested history PARAM work distinct
from claims about new regressions. Production preservation checks remain valid.

Terminology clarification: “parent diagnostic” was ambiguous report shorthand,
not an owner-taxonomy concept. `Parent` is literal CK3 message text referring to
a character's parent. Current report wording now spells that out. Searches of
product/learner source and governing docs found no separate category, schema field
or processing layer with that name. Historical full-ID and wording-preservation
requirements apply to those ordinary error messages; do not delete recognition
or general merge safeguards based on this reporting terminology error.

## Production-schedule v54 control completed — 2026-10-04

The unchanged frozen v54 learner completed production's retained 20+20+20+13
schedule. Corpus equality and order were already established; the owner directed
reuse of the saved hashes/inventory, without another input audit. Disposable
package `83df10b8cfb86d1573f8e510`, model `6024f47eace4750c605e0101`, manifest pin
`9b4baf8e93455ef247808bbc13aa73d841aa1fb271a781ec2a2e8df385d2d321`.
Workspace `.codex-tmp/production-incremental-v54-candidate`; research revision
`4bde423710ac0d140f898168`. Authenticated build/publication receipts completed.
The initial post-20-log orchestration check used a runtime field on a research
model; it was corrected and the completed checkpoint resumed without rebuilding.

Reports: `BUILD-HISTORY.html` compares production/fresh/incremental and all 14
owner cases; `CHANGES.html` contains 15 added, 15 removed and 15 newly classified
examples. Links/sample counts/production parity passed; BUILD-HISTORY rendered
and visually inspected. Inventory: 689 production / 496 fresh / 467 incremental.
On the same 20 stored Runs: 6,063 newly classified occurrences, no production
assignment losses or downgrades, 72 provisional-to-template upgrades. All three
IS3QON reviews are supported assignments. Across 73 training logs: no production
assignment losses, two template-to-provisional occurrences, two of four unmatched
occurrences classified. Exact captures reconstruct, no message-identity collisions;
production selection/catalogs, retained DB backup and review shards unchanged.

Controlled result is mixed. Examples 7–10 retain literal phrases/categories in
incremental v54: history has two separate literal phrases (the requested shared
PARAM remains absent); effect/trigger remain literal; colored/textured and
Flag/Variable remain separate. Thus fresh-build KEY outcomes are demonstrably
build-history-sensitive. Exact decision/safeguard traces are still outstanding.
Fresh-to-incremental loses 10,665 stored-Run assignments across 17 messages:
5,429 invalid-comparison-side and 5,236 failed-variable-fetch occurrences, both
tooltip constructions. These were also unmatched in production. Both candidates
must be retained as controls; do not promote or call the new result uniformly
positive. Next: owner-requested actual traces for 7–10 and these two families,
full 73-log contextual function-word KEY audit, then reusable corrections and
re-evaluation. No inference changes were made in this controlled-build step.

## Owner review received; production-schedule build setup — 2026-10-04

[The owner review](LEARNER_73_LOG_OWNER_REVIEW.md) supersedes the provisional
review judgments below. First reproduce production's 20+20+20+13 ordered input
batches using the unchanged frozen v54 release. Incremental candidate workspace:
`.codex-tmp/production-incremental-v54-candidate`. The retained registry operation
owns recovery/build/publication; `mirror_incremental_build.py` only orchestrates
exact input copies, checkpoint receipts and progress. Build basis records original
script/identity hashes and each ordered input prefix. No cross-version model seed.

After completion, compare with production and fresh v54 before attributing the
differences or changing inference. Examples 7 and 10 are rejected; 8 and 9 are
accepted with sensitivity concerns; 5 remains pending. The detailed trace/full
binding audit/fixes follow that controlled comparison. Source logs, production
packages, selected learner and Runs remain unchanged. Preserve both v54 controls.

## Owner-authorized obsolete research artifact cleanup — 2026-10-04

Removed 23 superseded generated model/native-evidence payloads from this task,
totaling 18,316,359,874 bytes (18.32 GB), including the 11,350,871,937-byte v53
research model. Earlier v46/locator/character experiments and the refinement
memory/control copies were included. Original source logs, manifests, review
reports, compact exports and unrelated earlier research remain intact.

Current candidate `.codex-tmp/production-73-v54-candidate` is preserved in full.
Its research bundle hashes and immutable package pin were verified before and
after cleanup; production package/selection and current review reports are
unchanged. Exact deletion inventory and verification receipt:
`obsolete-artifact-cleanup.json` in that candidate directory. Each affected old
bundle has `REMOVED-PAYLOADS.json`; those research bundles are no longer loadable.
Historical statements below that their large payloads remain on disk are now
superseded. The computed bulk deletion was blocked by execution policy; direct
explicitly named nonrecursive PowerShell file deletions succeeded.

## Removed-template thematic review — 2026-10-04

Owner follow-up: make many-old-to-one-new mapping the main review view.
`.codex-tmp/production-73-v54-candidate/CONSOLIDATIONS.html` now presents all
38 such groups involving 289 distinct removed predecessors, with every old
pattern, genuine witnesses, exact capture changes and links to all its outcomes.
Initial review judgments: 30 look like upgrades, seven need wording/category
review, one has mixed predecessor outcomes (marked-up-name support downgrades
outside the displayed successor). These judgments are not accuracy measurements
or release approval. Full removal analysis retains the separate one-to-one,
lost-match and unobserved cases. Main comparison links to the focused view.
All predecessor membership and local links verified; Chrome desktop rendering
captured. Evidence: `consolidation-review.json` and
`consolidation-report-verification.json`. No matcher/package changes.

Owner terminology correction: use **error templates**, including provisional
templates, in learner review prose; “definitions” is not an additional taxonomy.
Updated the main report and added
`.codex-tmp/production-73-v54-candidate/REMOVED-TEMPLATES.html`.

The complete existing coverage crosswalk identifies 442 of 465 removed templates
with selected witnesses, mapping to 218 candidate templates; 23 lack a selected
witness. Both pinned public matchers replayed 659 genuine witnesses across 475
distinct predecessor/successor pairs, including a no-match destination. Capture
analysis samples one witness per mapping/status/scope, not every message. All
exact byte-span transfers, selected IDs/statuses and crosswalk counts passed.
Source JSON and the human report include all 465 removed templates and every
observed successor, with scope counts kept separate.

Primary categories (exclusive priority documented in report): 135 identical
display patterns with only location numeric/line-reference constraints removed
(apart from IDs/support metadata); 128 location changes without diagnostic word
retyping in witnesses; 165 literal-to-slot broadening, including 35 travel
predecessors; 10 narrowing; one both directions; two slot-type changes; one with
lost coverage; 23 unobserved. The recursive executable comparison verifies the
135 constraint-only replacements rather than assuming display equality means
equivalence. Net reduction is 689 to 496: script-system 251 to 81, effect-impl 74
to 43, all other emitters together +8. Gross ID removal is not family loss.

Assessment remains mixed. Category wording now generalized into KEY includes
after death/from before, left/right, Flag/Variable, effect/trigger and
colored/textured. A parenthesized left-was/right-was clause becomes PARAM.
These require classification-granularity review; this analysis does not establish
false positives or authorize a new constrained grammar. Known loss/support
regressions remain as documented below. No inference/package/runtime changes.

Verification: report data/links/anchors and 15/15/15 main-report samples pass;
Chrome headless desktop rendering captured and visually reviewed. Evidence:
`removed-template-analysis.json`, `removed-template-summary.json`,
`removed-report-verification.json`. The first extra crosswalk check incorrectly
omitted status from its key; one genuine pair has both template and provisional
selected outcomes. The corrected check includes status and passes; original
crosswalk/replay already preserved it. Source helpers:
`analyze_removed_templates.py`, `report_removed_templates.py`, and updated
`report_production_comparison.py` under `tools/template_learning/`.

## Completed 73-log v54 comparison and human report — 2026-10-04

Delivered report: `.codex-tmp/production-73-v54-candidate/CHANGES.html`.
It contains 15 added definitions, 15 removed definitions stratified across both
evaluation scopes, 15 newly classified messages and destination templates, an
executive assessment, original-three/effect/locator/continuation checks, full
crosswalks, remaining unmatched examples and concrete regression explanations.

Assessment: mixed, with a large net coverage improvement. On the same 20 retained
Runs (811,103 total message/recovery occurrences), 16,727 previously unclassified
occurrences (97 distinct messages) now classify; one previously complete occurrence
is lost; no template-to-provisional changes occur in these Runs. Net gain 16,726.
All original three IS3QON diagnostics are supported assignments, all 75 short-ID
travel forms share one supported template, and all four earlier effect KEY checks
pass. Of the earlier 60 lost occurrences, 59 recover; all 317 earlier downgrades
regain template status. Production parity, exact reconstruction, identity and
existing LOCATOR preservation checks have zero discrepancies.

Both packages use exactly the same 73 training hashes; none of these 20 stored
Run hashes is in that set. The independent full-training-corpus check covers
91,925 contextual messages / 2,594,588 occurrences: no complete match losses,
63,749 provisional-to-template upgrades, four formerly unmatched occurrences
classified, and 115 template-to-provisional occurrences over 30 forms. These
scopes overlap in message content and must not be summed as independent totals.
Definition inventory: production 689, candidate 496, added 272, removed 465,
shared IDs 224. Across both scopes, removed IDs classify as 435 with preserved
selected coverage, six support-downgrade-only, one lost-match, 23 without a
selected witness. The latter are not proven harmless removals.

Remaining lost match: Run `20261001-3FCRIS`, stored ordinal 3196, one marked-up
`had_sex_with_effect` character-name message, formerly template
`0fa77cd8ed4f17791dbdcb4a`. The trace PARAM is recognized; 38 applicable candidates
(34 in the family) yield zero complete matches and zero ambiguous-capture
candidates. The exact message is outside training. Saved refinement lineage shows
unsupported broad PARAM proposals split the marked-up names (167 values) and
localization spellings (18,895 values), leaving literal singleton survivors.
Training downgrades are 12 marked-up name forms/occurrences and 18 apostrophe-name
forms/103 occurrences. Do not force PARAMs or infer a database failure. Attribution
between changed inference and fresh-versus-incremental order remains unisolated.
Recommendation: retain improvements, resolve/review these regressions and the
remaining unselected definitions before release/pin approval; use a bounded
ordered-incremental experiment for the two families if requested. Production
selection, catalogs, processes, Runs and protected evidence remain unchanged.

Fresh source `f4fa64dd7d104a82fad64812`; model `31488ccd43652c5bcd8f05cf`;
disposable package `c506869af1b6c97d0bafb11e`; manifest pin
`a1335cbb3957ca717e98d941e73f7f30dd6987319661861c558c923d6cd5d380`.
Learner release/pin are the verified v54 identifiers recorded below. Build and
publication receipts completed. Native assignment evidence is byte-identical to
the stopped v53 73-log result, and all 496 executable definitions are identical.
Research model fell from 11,350,871,937 to 245,544,316 bytes. The 18,895-value
observation is now one event referenced by 18,895 children. Build time 1000.734s;
observed peak working set 5,025,054,720 bytes (private memory sampled every 15s).
No learning or publication worker remains active.

Verification disclosures: the first comparison correctly stopped because copied
experiment metadata still named the earlier 20 training logs; corrected only that
research descriptor to the authenticated 73 hashes and reran comparison and
locator verification. Original descriptor and evidence-reuse provenance retained.
An initial HTML checker used the Windows default encoding; corrected to UTF-8
bytes and disabled redundant CRLF translation in HTML output. All final sample
contents, counts and links pass. Headless Edge produced no screenshot and Chrome
startup exited -2147483645; visual rendering remains unverified. See
report-verification.json for these limits and the one real coverage failure.

## Resumed through production comparison and human report — 2026-10-04

The owner clarified that stopping after engineering verification did not complete
the requested deliverable. The corrected v54 fresh build resumed at 01:06:23 local
in `.codex-tmp/production-73-v54-candidate`, worker PID 47300, exec session 97109.
The prior stopped-attempt log is preserved separately. Use the completed 20-log
parity and serializer-memory checks above/below as prerequisites already met.
Finish this build, its authenticated publication/native parity, comparison with
the unchanged production package, original-three and locator/character checks,
and the human-readable CHANGES.html report. Include 15 added definitions, up to
15 removed definitions with replacement/loss assessment, previously unclassified
messages and their destination templates, executive judgment and next steps.
Do not end merely with a build-start or engineering-status message.

The report uses the same retained 20-Run snapshot as the earlier v53 comparison.
An additional read-only production pass over all 91,925 contextual messages from
the 73-log corpus completed: 2,439,711 template, 154,873 provisional, four no_match
occurrences. Ledger/provenance is production-training-ledger.json in the fresh
directory. Once new candidate native-evidence byte equality is established,
compare that ledger with the independently replayed candidate to assess removed
definitions beyond the 20-Run sample. New compare_training_corpus.py owns this
genuine-data comparison. No production records change. Learner memory sampling
is in learner-memory.jsonl; the separate monitor exec session is 15386.

## Refinement duplication corrected; 73-log build stopped for memory verification — 2026-10-04

Latest owner instruction: do not restart until the memory/bundle-writer defects
are also fixed. Although those changes were already included in the successful
20-log control, the 73-log worker and its launcher were stopped at 01:02:40 local
on 2026-10-04 (verified process IDs/start times; exec session 46197 ended).
No 73-log model or completion receipt was produced. Keep this attempt's directory;
do not mistake its release.json for a successful build. Production processes were
not stopped. An isolated serializer allocation measurement passed against
the genuine completed 103,390,582-byte control model; it did not run learning.
Helper: measure_serialization_memory.py; output `.codex-tmp/refinement-writer-memory`.
Peak additional Python allocations: 6,747,518 bytes for writing and 8,587,838
for revision hashing; output bytes and revision hash exactly unchanged. These
measurements exclude the already-loaded model and inference, and do not claim
full 73-log peak memory. Producer reload removal is in artifacts.write_bundle;
the genuine 20-log learn/publish receipts prove that corrected path completed.
The 73-log build remains stopped after the measurement; no restart occurred.

Owner clarified that the observed content hashes proved duplicated parent data;
they were not a request for content-addressed deduplication. The stopped 73-log
v53 research build and diagnostic recovery remain preserved. No recovery export
is being activated or substituted for a fresh build.

The v54 candidate changes six child-split paths and three consolidation/regrouping
paths to parent-linked, local-delta refinement events. A rejected field's complete
value list is created once at the split. Child decisions contain retained values,
not the parent list. Sequential research event IDs require no content comparison.
Retirement history shares this lineage. Further duplication corrections: reuse
the already-computed field observation, pass executable definitions into the
matcher's defensive snapshot, avoid copying immutable prior retirement history,
stream research model JSON/revision hashing, avoid producer-side model reload,
and stream review rows with one definition file per template.

Changed owners: clustering.py, new refinement_history.py, artifacts.py,
evidence_serialization.py, patterns.py, research_matching.py, learner_loader.py,
build_review_pack.py. Research probes now preserve lineage references.
New verify_refinement_lineage.py compares genuine candidate inputs, executable
definitions, full native-evidence bytes and lineage integrity. Canonical streaming
encoding/hash already agree exactly with the retained genuine v53 model.

Controlled rebuild passed in `.codex-tmp/refinement-lineage-control` on the
same 20 inputs as `.codex-tmp/super-short-character-candidate`: 287 executable
definitions exactly equal; complete native-evidence file byte-identical across
731,529 occurrences (600,256 template, 131,273 provisional, zero unknown).
The 219-node lineage passed integrity checks; 76 retained-value children contain
only local deltas. A genuine 32-way split stores one 32-value observation and 32
child references. Control model size is 103,390,582 bytes versus 103,472,274;
this smaller corpus does not contain the pathological 18,895-value split.
Build took 182.954 seconds; independent publication/native replay also passed.
Control source revision `2f5800a8b8d02fd1b6eb47e9`, runtime model
`4bbd5353d39e4407847f9353`, disposable package `c95eae6233cfc49bfe23dedf`.
See `verification.json`, `learn-execution.json`, `publish-execution.json` there.

The now-stopped 73-log build started 2026-10-04 01:01:49 local in
`.codex-tmp/production-73-v54-candidate`; learner worker PID 28460, parent 45380,
exec session 46197. Release `16b038032b58d67fe95304da8edfdd0aa02ecc1663d874a70c7c9935dcc3cd28`,
pin `f8f024af577229c48306c31b32e5712bdaa5f42341766cc2f26e1076961ed8f3`,
same exact release as the successful 20-log control. All 73 input bytes/hashes
were rechecked against production's recorded training set before launch.
The build helper would write learn/publish receipts and a disposable package;
this stopped attempt did not reach those steps.
After completion, quantify the large split's lineage/size reduction, compare
compact definitions and native assignments with the preserved v53 73-log
diagnostic baseline, then complete the production comparison/report using the
unchanged 20-Run exports copied into the fresh directory. Re-run character/date
and original IS3QON/location checks for the new candidate. The final production
report must retain the incremental-versus-fresh caveat and investigate regressions.

The owner deferred an identical incremental-order experiment; do not substitute
one now. Production selections, catalogs, processes and protected inputs remain
unchanged. No new full-corpus result is yet claimed.

## Reporting content search and outcome corrections — 2026-10-04

Owner terminology correction: unreadable/unsupported source content is a per-file
result with a reason, not a search-process crash. Python checks encoding/reads
excerpts; ripgrep searches current source contents. A busy handler queues requests
and retries contention; broken transport is a runtime error handled by its existing
contract, not a new busy-queue rejection policy. The current review register now
separates file outcomes from the two unencountered process/handler fault groups.

Latest owner clarification: operational faults should surface through the caller's
exception boundary. `reporting.cli` now catches unexpected ordinary Python
exceptions for `runs`/`report`, preserves stage/type/message/traceback and exits
nonzero. If the error renderer/destination also fails, stderr retains the original
error envelope. Libraries/handler contracts are unchanged. Verification uses
genuine CLI paths and source inspection; no induced crash/failure claim.

08B implementation and owner-review corrections are complete. The authoritative
deliverable checklist and remaining verification limits are now the opening
section of [the reporting handoff](TASK08B_REPORTING_HANDOFF.md). No known assigned
feature or documentation work remains. Do not treat historical open-item entries
below as current work, or unencountered runtime faults as passed tests.

Read [08B](TASK08B_REPORTING_HANDOFF.md)'s opening sections for current evidence. Normal content
search spans template literals and populated slots; result annotations derive
from the shared stored renderer, with assigned templates and full-count summaries.
The misleading template-phrase acceptance case is withdrawn. Genuine CLI groups
11/04/02/12 verify searches, composition, history/formats and all requested
-5…+5 positions with missing Runs labelled. The seven-Run middle window has four
unavailable positions; eleven simultaneous Runs are not a gate. Python file-I/O
tracing covers both the cold CLI and worker without opening logs/model artifacts.
No synthetic history, injected failures, production changes, commits or pushes.

Current review manifest/browser receipts: `.codex-tmp/task08b/content-search/`.
The existing bundle's `outcomes.html` now describes two concrete unexercised
fault paths (handler operation/transport; source-search process launch/error exit),
separately from successful empty queries and ordinary absence. Handoff lists
all receipts, bounded library changes, checker corrections and trace limits.

## Earlier reporting duplicate-detection requirement removal — 2026-10-04

Owner explicitly deleted timestamp-based duplicate detection/rejection from
Reporting and Analysis. The chronology grouping/exclusion code and reporting
verification item are removed. Duplicate-ingestion handling stays in the pipeline;
no replacement check or pipeline change was made. Prompts, owning/receiving
handoffs and cross-team summaries are corrected. The review page has four remaining
evidence-gap groups. See [08B](TASK08B_REPORTING_HANDOFF.md) for checks and receipts.

## Task 08B earlier-outcome reconciliation — 2026-10-04

Owner could not trace the earlier incomplete-deliverable/bad-query list from the
file report. `outcomes.html` now gives all six original review IDs, 17 named query
cases with expected and actual saved results, and the four still-unverified groups.
Opening explanations link directly to the case table and open checks. The builder
validates the named outcomes against retained CLI exports; no query, failure or
database state was fabricated or rerun for this presentation change. Documentation
completion does not imply owner acceptance or passing unrepresented cases.
See [08B](TASK08B_REPORTING_HANDOFF.md) for the current review/navigation check.

## Task 08B file presentation and source rule — 2026-10-04

The owner's current rule identifies the last matching playset member in load
order as the error source for each file/line. It supersedes the earlier blanket
winning-file/ownership-unresolved report wording for this case. Tables now show
raw load order, mod name, path and line separately, with **Resolved** / **File not
found** status and an **Error source** column. JSON exports `file_line_sources`;
the owning source service evaluates load order before file-content filtering.
Three genuine CLI groups / 18 exports passed in 63.465 s under
`.codex-tmp/task08b/bf417ac7f10840d7be776e15f11a15aa/`. The reviewed example retains
both orders 114/115 and assigns 115. Focused browser checks pass. The full evidence
and exceptions for unavailable load order/line are in [08B](TASK08B_REPORTING_HANDOFF.md).
No production/package/process change, commit or push.

## Task 08B relative-path clarification — 2026-10-04

The owner clarified that paths normally mean game-relative paths shared by the
base game and mod folder structures. Use `scope.source.relative_path.exact`:
optional leading `/` and either separator now normalize in explicitly relative
fields, leaving physical paths and stored evidence unchanged. Reports look in the
same parent folder beneath every recorded member, retaining all mod candidates.
Genuine CLI results: two diagnostics / 64 occurrences, candidates at orders 114/115,
433 file names in 77 existing parent folders, no recursion. Wrong relative folder:
empty success. The handoff and review bundle include `relative-path-all-members`.
SQL-only path matching, explicit physical-file access and other operational limits
remain unchanged. Exact receipts are in [08B](TASK08B_REPORTING_HANDOFF.md).

## Task 08B no-path emission correction — 2026-10-04

An emission need not contain a path. Reports label source lookup not applicable;
the source library skips playset/root access when no references need lookup.
No-path records have `source_path_status: "no_path"`; misleading reference-
limitation/completeness fields are removed. Mixed reports keep lookup problems
on actual referenced records only. Genuine checks and current examples are in the
[08B handoff](TASK08B_REPORTING_HANDOFF.md). Production and unrelated work unchanged.

## Task 08B source recursion/count verification — 2026-10-04

Per-search counts and effective root/directory/recursion/cache detail are now
returned by SourceSearch and rendered by reports. Independent PowerShell counts
and returned-file-set comparisons pass 29 cases on genuine base-game/mod trees;
the root CLI exports consistent counts in JSON/text/HTML. The initial text-checker
newline issue was corrected and the full check rerun in fresh disposable storage.
Passing receipt: `.codex-tmp/task08b/recursion/769ceb6ed0434981b2744aab42faff3e/`.
See the [08B handoff](TASK08B_REPORTING_HANDOFF.md) for exact counts and reproduction.
No production/package/process change or commit/push; preserve unrelated learner work.

## Task 08B explicit path-resolution selection — 2026-10-04

Owner-requested `scope.source.resolution: "unresolved"` finds messages with at
least one recorded reference for which a completed current search finds no file
in the effective roots. `resolved` is also supported. Reports and analytical JSON
show per-reference status; no-path messages are nonmatches and incomplete searches
remain unknown. Ordinary path matching is unchanged. The genuine example returns
60 diagnostics / 386 occurrences; the two-entry authorized fixture verifies fake
paths separately. Current implementation, evidence and bundle pointers are in
[08B handoff](TASK08B_REPORTING_HANDOFF.md). No schema/production/package-selection
change; commits and pushes remain deferred. Preserve the unrelated learner work.

## Task 08B path-filter correction — 2026-10-04

Owner correction implemented in 08A.2: ordinary path-only predicates select stored
references; pathless/nonmatching records are excluded without an error, warning or
unidentified partial. A matching file need not exist on disk. Root/member/content
queries still use current candidates; missing individual files are nonmatches.
08A.1 consumes those matches before totals/history/limits. No schema/API-field or
production change. The prior required-file/pathless-failure semantics are obsolete.

Current broad example: `investigations/file-path-all.html` in the existing 08B
bundle, selecting all diagnostics for one recorded path with no other refinement.
It returns two identities / 64 occurrences. The existing `required-partial.html`
now succeeds with only the culture diagnostic (32 occurrences), silently excluding
the pathless localisation record. New path-only and missing-file examples and the
outcome page explain the correction. Original exports are retained separately.

Two genuine CLI groups, four focused source groups and expanded path-composition
check pass; the authorized fixture passes nine checks / nineteen exports; genuine
archive/path checks pass seven exports, plus three broad-query formats. Logging
and imports pass. Current manifests and commands are under
`.codex-tmp/task08b/path-filter-correction/`; [handoff](TASK08B_REPORTING_HANDOFF.md)
records exact locations. Commits/pushes deferred; unrelated learner work preserved.

## Earlier Task 08B verification follow-up — 2026-10-04

The owner's requested synthetic fixture is delivered and labelled: two complete
genuine emissions, only fake file LOCATOR paths changed, all 133 recorded playset
members/orders preserved by the normal writer. Five checks / eleven actual CLI
exports pass. Original evidence is unchanged. The integrated report links input
log, playset JSON, original emissions and the verification receipt.

Fresh unchanged genuine backup: seven eligible Runs and fourteen exclusions.
Full trailing-five, separate five-before/five-after sides and a three-per-side
window pass independent public-handler count/history checks. Five unchanged
archived logs in separate disposable single-Run databases now exercise all nine
syntax selectors (85 diagnostics; seventeen CLI exports) and missing-playset
optional/required behavior. They do not extend production history. A temporary
capture rename failed before ingestion; a fresh retry passed the two remaining
archive cases. Details and retained failure evidence are in
[the reporting handoff](TASK08B_REPORTING_HANDOFF.md).

Review bundle remains `.codex-tmp/task08b/c9e83ce2125a45c78c8db4b4ab70d18f/`.
Open `investigations/synthetic-missing-files.html`, `worked-five-runs.html` beside
it, or `outcomes.html` for completed items and four remaining evidence-gap groups.
The 54-example bundle passes 16,161 links; fifteen new Chrome routes and fixture
input navigation pass; representative screenshots inspected. Final two genuine
CLI groups pass (72.554 s), plus logging/imports. No production/process/config/
package selection change, commit or push; unrelated learner work preserved.

## Earlier Task 08B integrated explanation correction — 2026-10-04

Latest owner follow-up: the template example did not show what happened to the
earlier incomplete deliverables. The bundle now has `outcomes.html`, linked from
the index and all example reports. It gives completed corrections with direct
report links, plus the remaining genuine-evidence gap groups and their completion
conditions. Definitions are in `examples/reporting/delivery-status.json`; the
existing bundle builder renders them. No missing evidence case was newly closed.

The latest owner feedback reopened the reading/navigation issue: an outcome link
was insufficient when the explanation and evidence still had to be found. The
ordinary report renderer now places the question, expected/actual result and
relevant evidence together. All 38 example links land there. Named links open
the exact template, diagnostic, Run table or highlighted source excerpt.
The rebuilt bundle passes 12,077 local-link checks with unchanged analytical
payloads. Genuine CLI format/history/limit and partial-source groups passed;
Chrome checks exercise integrated explanations and direct evidence links.
Evidence: `.codex-tmp/task08b/browser-integrated/`; details and CLI evidence paths
are in [the reporting handoff](TASK08B_REPORTING_HANDOFF.md). Earlier closure
wording below predates this additional owner correction. No production state,
active package selection, commits or pushes changed.

### Earlier reporting implementation checks — 2026-10-04

The open 08B work has been completed: valid opposing preset filters return empty
results; missing symbol input fails before any database request; partial-source
reports visibly separate the pathless diagnostic from known matches. Reports
explain their question/filters/outcome, show template patterns and diagnostic Run
counts, and name recorded mods beside paths. A genuine DLC-file case is checked.

All eight CLI groups passed (161.987 seconds), six query checks (13.926 seconds),
nine source checks (260.071 seconds), final focused partial-source checks and
logging/imports/dependency checks. Actual Chrome clicks cover 13 report routes and
source appendix/return navigation. Desktop/narrow screenshots were inspected.
The 38-example bundle has 10,559 checked local links. See the current closure
register, evidence paths and reproduction commands in
[TASK08B_REPORTING_HANDOFF.md](TASK08B_REPORTING_HANDOFF.md).

The seven absent syntax selectors and genuine failure/duplicate/full-window gaps
remain explicitly unverified, as permitted by the assignment. No production data,
process/config/model selection, commit or push changed. Full live Trusted Run
acceptance remains separate. The earlier in-progress notes below are history.

### Earlier 08B review continuation (superseded by closure above)


Latest review: query/preset input validation now precedes database-client creation
and named-Run lookup; the missing symbol selector submits no investigation.
Focused genuine preset checks passed (14.855 seconds), plus logging/imports.
The examples distinguish stored paths, current mod-file candidates and the genuine
pathless localisation record. Contradiction-to-empty-set behavior is an open owner
policy clarification, not a database limitation; original rejection rules remain.
Use the handoff's updated review-bundle command and saved evidence manifest.

Owner correction: 08B is not complete. Existing implementation and passing CLI
checks do not close report usability and visual/end-to-end review. Continue from
the open-issue register at the start of [TASK08B_REPORTING_HANDOFF.md](TASK08B_REPORTING_HANDOFF.md).
It separates current UX/verification work from expected negative checks and real
evidence gaps. Full Trusted Run acceptance remains a separate milestone.

The current navigation fix gives every example an explicit outcome link, a full
report link and a return route. `no-eligible` links to its actual error and shows
the requested package. Explanations live inside the reports. A tracked generator,
`tools/build_reporting_examples.py`, rebuilds the index and reading copies in
the same review bundle's `investigations/` directory. Browser/owner review remains
open even after structural and CLI verification.

### Earlier implementation evidence — 2026-10-03

Latest owner refinement: all outputs now start with plain-English question,
filters, expected behavior, actual result and reading guide. Each consumer example
also has a specific question/expected outcome in `examples/reporting/checks.json`.
Individual diagnostics are labelled explicitly; classification details explain
template recognition. Mod names/load orders are visible beside candidate paths,
using the evidence Run's recorded playset. Base-game/DLC members keep plain paths.
All eight genuine CLI groups passed (276.954 seconds), plus recorded-playset name
verification and existing template/count/history checks. Current template/worked
files were refreshed; `examples.html` beside them indexes explained reading copies
of the latest `cc41d9c32c7843d0bb98f857ee5f88ea/` CLI results. Receive the 08B handoff
for exact changes and the unexercised DLC-candidate presentation case.

Latest template/instance correction: reports now lead template investigations with
the actual placeholder pattern and combined per-Run counts, then explicitly label
each individual diagnostic. Raw `template` status is shown as `Match status: matched
template`. Complete template aggregates live in 08A.1's `rollups.templates`, keyed
by full definition reference and computed before display limits. The current
template-only exports were regenerated; genuine raw-handler counts, HTML/text/JSON,
zero-display-limit invariance, focused CLI checks (14.960 seconds), logging and
imports passed. See the handoff for the corrected initial test-discovery invocation.

Latest example correction: `symbol-template.json` now selects only the broad
trigger-error template, removing the culture/message restrictions that had reduced
it to one selected identity. Genuine root-CLI `template-only.{html,json,txt}`
exports in the current `c9e83ce2125a45c78c8db4b4ab70d18f/` evidence directory
show all 202 selected identities / 396 occurrences with per-Run history; four-Run
totals are 263 identities / 1,415 occurrences. Export agreement and visible Run
tables passed. README/handoff distinguish template selection from optional
refinement and the separate worked message query. The handoff discloses an initial
XML-checker failure on preserved CK3 control characters, corrected with HTMLParser.

Latest owner usability correction: `Occurrences by Run` is now visible directly
below each diagnostic message instead of inside collapsed history details.
The current `c9e83ce2125a45c78c8db4b4ab70d18f/worked-full.html` was regenerated
with the actual root CLI; generated history tables/counts and logging ownership
were checked. No analysis or runtime-data change.

Receive [TASK08B_REPORTING_HANDOFF.md](TASK08B_REPORTING_HANDOFF.md). Reporting
implementation is present: root `runs`/`report`, five presets, structured query
refinements, text/JSON/offline HTML, candidate associations and verbose appendices.
README and `examples/reporting/` supply working commands/queries. The two 08A
handoffs describe bounded consumer additions in their owning libraries.

Final genuine CLI verification passed all eight groups (179.454 seconds); all six
retained diagnostic and nine source checks passed. Exact consumer commands and
reports are under ignored `.codex-tmp/task08b/e5e61184ea4a41bcb077858ce49966f6/`.
Use `worked-full.html` and its sibling appendix for the full available four-Run
context-switch example. Shared logging/import/dependency checks and packaged
HTML/CSS passed. A configured-database check used a disposable config/database.
The latest worked files are in `.codex-tmp/task08b/c9e83ce2125a45c78c8db4b4ab70d18f/`
after two focused CLI groups passed again (126.077 seconds), checking escaped
content and preservation of exclusions in partial-source failures.
The handoff discloses initial newline/incorrect-source-assumption failures,
unavailable dependency/browser tooling and remaining real-evidence gaps.

Changed files owned by this task: root CLI; reporting CLI/presets/presentation,
HTML/CSS resources and package-data declaration; query/analysis/source receiving
additions; genuine CLI tests and a source-test assertion adjusted to separate
unchanged SQL/history from new candidate data; three example queries; README,
08B/08A handoffs and current pointers/ledger. No synthetic histories, live process
changes, production writes, model selection, commits or pushes. Pre-existing
learner/advisory changes listed below remain untouched. Full Trusted Run acceptance
and any browser visual review are separate continuation items; no operational
activation is needed merely to run these ordinary reporting commands.

## Incoming advisory review delivered — 2026-10-03

Continue advisory work from [TRUSTED_RUN_COMPLETION_PATHWAY.md](TRUSTED_RUN_COMPLETION_PATHWAY.md).
08B and the canonical implementation plan remain undelivered at inspection.
Configuration/bootstrap/setup and read-only doctor have concrete gaps. Retained
October 3 normal/crash lifecycles include start, exit, capture, ingestion and saved
public Run reads; do not repeat the earlier blanket live-evidence gap. Candidate
applicability and milestone acceptance remain separate. The pathway names proposed
owners, scope decisions and next assignments; none is activated by this review.
Only advisory documentation/current pointers changed. Existing prompts, product
specifications, source, runtime state and unrelated work are preserved.

## Canonical logging planning handoff — 2026-10-03

The owner supplied an execution-journal design using actual code identities,
bare source-position checkpoints and optional caller-owned counts. Read
[CANONICAL_LOGGING_SYSTEM_V1.md](CANONICAL_LOGGING_SYSTEM_V1.md) and
[TASK09A_PROMPT.md](TASK09A_PROMPT.md). The latter commissions a plan only;
`CANONICAL_LOGGING_V1_IMPLEMENTATION_PLAN.md` is its future deliverable, not a
completed artifact. Earlier learner phase-logging prompts are superseded.

Advisor source inspection confirmed the shared logger's config import and existing
release-mapping seam. `derive_pattern` is defined in `patterns.py`; registry
`paths_seen` increments before processing, so placement must preserve honest
completed counts. No runtime code changed or campaign ran. Source-preservation,
immutable-candidate and bounded rollback guidance is in 09A. The
[incoming briefing](ADVISORY_HANDOFF_TRUSTED_RUN.md) proposes learner-first adoption
and separate consideration of runtime conversion; owner decisions remain open.
The agreed 08B prompt is untouched. Ongoing locator work below remains independent.

## Exact production-corpus rebuild stopped; lineage correction pending — 2026-10-04

Owner explicitly stopped the v53 research-candidate path and requested fixing
the provenance duplication / serialization-memory problems before a fresh build.
No candidate worker remains running. A bounded export recovery completed parity
but was NOT packaged or used for a new production comparison; that path is stopped.

The v53 fresh build did learn the exact 73 hashes: 2,594,588 messages / 90,506
distinct messages, 496 definitions (335 supported, 161 provisional), training
2,503,348 full / 91,240 provisional / zero unknown. It wrote source candidate
54573fdc09b35e2e37d9ef1a, then whole-file reload grew past 56 GB private memory.
Only its identified worker PID16016 was stopped. Production PIDs30816/23252 and
their Oct2 start times were unchanged. Original artifacts are preserved.

Research model: 11,350,871,937 bytes, including 10,468,162,891 bytes of
inference_refinements. Bounded recovery under recovered-release/ in the same
experiment authenticated source hashes, used unchanged owner compaction and
verified 91,925 contextual messages / all 2,594,588 occurrences / 367,957 captures,
zero changed matches/outcomes. Its control reproduced the prior 20-log published
model exactly. This recovered release is diagnostic evidence only after the
owner's stop instruction; do not continue packaging it.

Owner rejected content-hash deduplication as the primary fix: children should
reference parent history and store ONLY incremental evidence; consolidation should
reference input histories instead of flattening them. The unrun content-addressed
research_history.py experiment and its artifacts/loader changes were backed out;
clustering remains v53. No fresh replacement build has started. Next: implement
creation-time lineage/deltas, separate research history from executable definitions,
stream writing/hashing, and avoid reloading while retaining producer objects.
Preserve exact provenance, template inference, support statuses and captures.

Owner also asked why fresh rather than equivalent incremental: old learner state
is incompatible, but an empty new-version incremental replay in original order is
possible. No incremental rebuild is requested now; consider it after fresh results.

### Original 73-log preparation

Owner requires candidate training on production's exact 73 logs before comparing.
All 73 hashes and byte sizes were resolved and verified against production's
training_evidence (596,625,707 bytes). The now-stopped fresh build ran under ignored
`.codex-tmp/production-73-v53-candidate/`, using the identical frozen v53 release
as the prior 20-log candidate. No learner rule changes or old-model seed.
The original IS3QON capture is outside this training set; 63 of the 75 genuine
travel examples are present. Evaluation reuses the exact preceding 20-Run public
handler export/database backup and native review routes, preserving comparability.
Build output and immutable execution receipts belong in that candidate directory.
Production selection, data and runtime processes are not being changed.

The comparison/report helpers now derive training parity, counts and assessment
from results, rather than retaining the earlier 20-log report's fixed numbers.
Final production comparison and updated human-readable report await the corrected
fresh build; the stopped/recovered v53 output has not replaced the old report.

## Production v45 versus v53 comparison delivered — 2026-10-03

Owner requested a production comparison, 15 added/removed examples, genuine
previously unclassified examples and a short executive assessment. Delivered
`.codex-tmp/production-v53-comparison/CHANGES.html`. This is explicitly against
selected production package 68f1ae5db205ab46afef9c4d, not an earlier experiment.
Candidate remains v53 a113649d3a975d5b47018681; no model changes or further build.

Fresh consistent read-only backup plus public HandlerClient export found 20 Runs
(two newer than prior comparisons), 52,899 stored records / 792,675 assigned
occurrences. Authenticated native review shards contribute 18,427 no_matches and
one unresolved recovery: 811,103 total occurrences, 7,287 distinct recovered native
messages. All 20 Runs record the selected v45 package. Production replay agrees
with every stored template/status and every review no_match route; zero parity
mismatches. Review units are mapped to original emission ordinals and body spans;
shards/manifests and backup hashes checked unchanged. No production data writes.

Assessment: MIXED, substantial net coverage gain but not ready to replace
production. 6,056 production no_match occurrences / 77 distinct messages become
template assignments (13 target definitions), including the original three.
60 previously complete occurrences / 38 distinct messages lose assignments
(56 template, 4 provisional). 317 occurrences / 8 distinct messages become
provisional; these remain valid complete assignments, not lost matches. Another
72 provisional occurrences become templates. Net complete gain: 5,996 occurrences.
Final counts production -> candidate: template 784,904 -> 790,659; provisional
7,771 -> 8,012; no_match 18,427 -> 12,431; unresolved recovery stays 1.

Definition inventory: 689 production vs 287 candidate; 164 added IDs, 566 absent,
123 shared. Removed categories: 166 observed replacements without coverage/status
regression; 19 with losses; 7 with downgrades and no losses; 374 unobserved in these
Runs, so safe replacement is not established. Exact-ID changes are not counts of
new/lost semantic families. Production trained on 73 logs vs candidate's 20, so
this comparison combines implementation and training-breadth differences.

Concrete narrowing: generic entity-name KEY becomes literal unit_levant... and
loses unit_seljuks... messages; generic audio parenthetical PARAM becomes one
literal reason with only one independent example; candidate lacks Invalid province
definitions. Smaller training breadth is a plausible contributor, not proven as
the sole cause. Recommendations: retain fixes; build fresh compatible learner
state on the full approved genuine corpus including production coverage, repeat
comparison against all losses/downgrades and remaining unknowns, review semantics,
then seek release/pin approval. That next build/activation was NOT started.

Report has exactly 15 added, 15 removed and 15 gained-message examples (covering
all 13 gained target definitions), plus 8 lost-match and all 8 downgrade examples.
Sample selection, complete crosswalk, full assignments and executive summary are
in sibling JSON. All gained samples are actual native production review routes.
Exact reconstruction and identity uniqueness pass; no existing LOCATOR capture
loss on shared matches. 303 distinct messages change captures/types; complete
details retained. This is data-fidelity evidence, not exhaustive semantic approval.
HTML counts/links and totals verified; production selection/catalogs unchanged.

New owning empirical helpers: compare_production_candidate.py and
report_production_comparison.py. Earlier open report links prominently to this
production assessment and labels prior no-regression claims as versus v52 only.
Existing unrelated reporting/advisory work preserved; no commits or runtime restarts.

## Corrected line boundary and dedicated super-short receiver — v53, 2026-10-03

Owner corrected the earlier period instruction: evidence should have challenged
it instead of adding an unsupported alternative. All 75 genuine bodies end in
CRLF and their default-location values have no terminal period. Removed v52's
period terminator; default-location PARAM now extends to native line end only,
retaining the capitalized start and separating trailing presentation whitespace.

The owner also questioned the missing super-short type and literal receiver in
the open report. Inspection confirmed no dedicated type existed through v52:
the marker-bounded recognizer emitted PARAM. The open locator-presence report
was v49, whose actual template really did have literal receiver names; it was
incorrect to explain this solely as raw-message display. v50-v52 captured receiver
PARAMs correctly. v53 reuses that verified recognizer with CHARACTER_ID_SUPER_SHORT
between `receiver is ` and `, default location is `. This is bounded recognition,
not a global capitalization/Name of Place classifier. Existing numeric-parenthesis
CHARACTER_ID_SHORT and full IDs remain unchanged. Structural validation requires
the owner-declared boundary for the new type.

Frozen release `a1c6be7f5802c60a6afe3f500cbe840bea53a2565cd051117ecb30ca8f633ec9`,
source candidate `0f451b3b150162fecbeb14f1`, model `89b82329839c9bd6cce5bdd1`,
package `a113649d3a975d5b47018681`, pin
`3c9f74a7f4a813920fa7ee573c5d263dbd3121e4867709c67a5ee0a5a987ca1a`.
Report: `.codex-tmp/super-short-character-candidate/CHANGES.html`; the previously
open `.codex-tmp/locator-presence-candidate/CHANGES.html` now shows the current
template and real captures above a collapsed, explicitly historical v49 section.
Original v49 page is preserved as CHANGES.v49-history.html in that directory.

Same 20-log fresh build: 222.984 seconds, 731,529 messages, 600,256 template /
131,273 provisional / zero unknown, 287 definitions (204 supported / 83 provisional).
Export parity: 166,518 captures, zero changed assignments/outcomes. All 75 genuine
travel examples retain template status via `0e4e3302cde2fc5e07a2227f`; this replaces
the prior travel definition, with 286 others unchanged. Receiver type changes
PARAM -> CHARACTER_ID_SUPER_SHORT; all exact values, other capture types (including
trace PARAMs), and rendered text remain identical to v52. Distinct identity checks
pass. Full IDs remain identical: 1,128 character / 3 house / 12 title occurrences.

All 18 Runs / 48,772 records / 766,476 occurrences retain v52 statuses: 758,582
template / 7,842 provisional / 52 no_match; no losses, downgrades or failed checks.
Original three all template through public Classifier/prepare_record. Original
Run: 59,170 template / 143 provisional. Locator/continuation/wrapper and four earlier
effect regressions pass. Production selection/catalogs, input hashes and backup
unchanged; production process IDs/start times unchanged. No activation, database
writes, runtime restarts or synthetic acceptance examples.

Changed owning source: owner_rules, shared SLOT_TYPES, patterns definitions/gates,
matching_validation structural-type requirement, clustering v53 identity. Empirical
evaluate_character_dates now accepts an explicit expected receiver type; shared
report helper supports historical v52 and corrected v53, checks complete capture
conservation and shows actual original-message binding tables. Guidance and formal
pipeline handoff updated. See focused-inference.json, receiver-type-transition.json,
all-short-identities.json, verification.json and immutable execution receipts.

## Owner-directed receiver/location boundaries — v52, 2026-10-03

Implemented the latest directive in executable owner_rules: `default location is`
introduces a PARAM whose first character is uppercase; a period ends the capture
and remains literal. Native line end also terminates it: a fresh hash-verified
104-log search found exactly 75 values, all capitalized and all without a period.
The period-terminated/lowercase-start branches have no genuine witnesses and
remain empirically unverified. The complete receiver PARAM rule already captures
all 75 shortest character display names between `receiver is ` and the following
comma/default-location marker; its explicit owner authorization is now recorded.
Numeric-parenthesis CHARACTER_ID_SHORT is separate and unchanged; corrected its
stale exported description that still claimed a preceding date was required.

Fresh frozen release `5973a6a68069df1493b7a8b0631fa57776b6247ff0cbe5677f7c01255039bab9`,
source candidate `afe5c5ce2dbebe2c5e326034`, model `b78ac3969c51343bfc071958`,
package `ca3d41518921b4ac128d3721`, manifest pin
`c6c6293f2723d17b399e7f7235f486e79f755efe239cef062a10cebe1c577230`.
Report: `.codex-tmp/receiver-location-boundaries-candidate/CHANGES.html`; sibling
location-boundary-inventory.json, field-verification.json, all-short-identities.json,
verification.json and immutable execution receipts retain exact evidence.

Same 20 complete-log build (497.344 seconds): 731,529 messages, 600,256 template /
131,273 provisional / zero unknown. All 287 definitions are identical to v51;
the changed executable rules are saved in the new package. Export parity checks
166,518 captures with zero changed matches/outcomes. All 75 corpus travel messages
retain template status via d9d8bdd39db285c6d80d8d2f, with exact date/identity/receiver/
location values, reconstruction and distinct identities. Full-ID preservation:
1,128 character / 3 house / 12 title occurrences.

Same unchanged public-handler export of 18 Runs / 48,772 records / 766,476
occurrences: all statuses unchanged from v51 (758,582 template / 7,842 provisional /
52 no_match), no lost matches, downgrades or failed checks. Original three all
template through public Classifier/prepare_record; original Run totals 59,170
template / 143 provisional. Locator/continuation/wrapper checks and four prior
effect regressions pass. Production selection/catalogs, input hashes and backup
are unchanged; production process IDs/start times remain unchanged. No promotion,
candidate database writes, process restarts or synthetic acceptance examples.

Changed owning source: owner_rules.json, clustering version, patterns slot
description, new report_receiver_location_boundaries helper; guidance and pipeline
handoff updated. Existing unrelated work preserved. Earlier reports link forward.

## Executable short-ID/location correction — v51, 2026-10-03

Owner explicitly required an updated candidate, not documentation alone. Implemented
the corrected first-capitalized-name/place rule with unrestricted later words and
numeric-comma parentheses, removing the preceding-date prerequisite. Body-start or
colon field boundaries remain; genuine leading transliteration modifiers are
accepted. Complete final display names after `default location is ` are now PARAMs,
including multiword names. Date KEYs, full IDs, receiver PARAMs, raw parser and
locator behavior remain unchanged. No global plain-name-of-place classifier.

Fresh immutable v51 release
`dd4888c1c7ff795ac0118f9d4c1ad183e279b13909f08880ff77a28702344768`, source candidate
`44f20d059af7d22e7c2df702`, model `a57f2987314c6427873d1097`, package
`a43ff1bce0c141069431b9a6`, manifest pin
`0db556637a153dc1e20bb3dd65475ea4d23f84a559fc52244fe005e472757a8f`.
Report and all nineteen exact repaired examples:
`.codex-tmp/character-location-candidate/CHANGES.html`.
Same 20 complete-log build: 731,529 messages, 600,256 template / 131,273 provisional /
zero unknown; 287 definitions, 204 supported / 83 provisional. Learning took 261.985
seconds. Export parity checked 166,518 captures with zero changed matches/outcomes.

All 75 inventoried genuine travel messages now have template assignments through
`d9d8bdd39db285c6d80d8d2f`: 56 retain template status; all 19 former no_matches
improve. Exact date, complete short identity, receiver, final display location,
native rendering and distinct identity digests pass. One shared template replaces
two definitions (final KEY / literal Mgikuyu Sabaki); 286 definitions are unchanged.
Existing full-ID recognition is identical for 1,128 character, 3 house and 12 title
occurrences. No genuine undated short-ID emitter was found in the 104-log inventory;
broader applicability remains unverified, despite removing the unnecessary guard.

All 18 stored Runs / 48,772 records / 766,476 occurrences checked against v50 using
the unchanged public-handler export: one additional no_match becomes template,
all other statuses unchanged. Totals: 758,582 template / 7,842 provisional /
52 no_match. No lost matches, status downgrades or failed checks. All original
three are template via the public Classifier/prepare_record path. Original Run:
59,170 template / 143 provisional / zero no_match. Ordered LOCATOR values,
variable-count distinct identity, native continuation/wrapper examples and four
earlier effect-regression cases pass. Production selection/catalogs, original
inputs and the database backup hashes are unchanged; no candidate DB writes or
runtime restarts. CIM process inspection was denied; ordinary Get-Process confirmed
both production process IDs/start times unchanged. No install was needed.

Code: owner_rules declarations, shared matching_primitives capitalization guard,
matching_validation declaration checks, v51 clustering identity. Empirical helpers
check_character_dates/evaluate_character_dates/report_character_location verify and
report genuine evidence. The receiver-capture survey now uses the actual receiver
span rather than substring containment in another capture. Guidance and formal
pipeline handoff record implemented behavior; historical v49/v50 pages link forward.
Remaining repeated-entry line:/near line: equivalence gap is a separate limitation.

## Disposable date/short-character correction — v50, 2026-10-03

Owner reiterated the previously omitted word-month date and short-character
directives. Implemented in the existing parameter registry/shared matcher:
format-constrained date KEY, opaque CHARACTER_ID_SHORT following that date,
and a bounded PARAM between `receiver is ` and `, default location is `.
All are source/mod/name independent. Numeric short-ID parentheses and the date
signpost establish boundaries in v50. Owner subsequently corrected the rationale:
capitalizing only the first word, allowing unrestricted later words, does not
truncate Viviana de Torres or Akurat Misibsen of Nabel. The earlier analysis
mistakenly tested an all-words-capitalized rule. Name/place first-character uppercase
holds in 74/75; the other starts `ʾAmīr` (uppercase A after a transliteration modifier).
All 75 numeric-comma endings are this character formulation; no non-character
counterexample was found. Evidence supports the owner's shape in this emitter/context;
it does not establish that the current date guard is necessary. No model changed
as part of this explanatory correction.
Existing CHARACTER_FULL_ID is unchanged (28 declared contexts / 17 sources).

104 complete retained logs (815,801,334 bytes, hashes verified) contain 75 short
identities/date prefixes, all in the travel family; no other family was found.
All dates use spaces/three-letter months: 19 three-digit years, 56 four-digit.
Hyphenated spelling is explicitly owner-requested, declared but unwitnessed.
Complete name word counts: 1=8, 2=40, 3=10, 4=9, 5=3, 6=5. Raw parser token
counts differ: 1=8, 2=39, 3=11, 4=8, 5=4, 6=4, 7=1. Names can include titles,
`of`, lowercase particles, apostrophes and untranslated dynasty strings; display
locations can be multiword. Short/full distinction is the numeric-comma suffix,
not the absence of `of` words. Whole short identities remain opaque.

The receiver was never PARAM in the v49 corpus replay: 22 literal / 53 unmatched.
Date/short fields alone pass similarity but the existing unmarked-PARAM ban still
separates the two targets. Explicit field markers now bound the receiver. Broad
plain-name-of-place survey: 187 expression occurrences / 154 distinct witnesses,
48 already inside PARAM, 109 inside REASON, 26 literal, 4 unmatched; includes
non-character titles/artifacts/traits/wording. Do not infer characters globally.

Fresh same-20-log source candidate `939a84cf65c16602cccf868f`, model
`165e31d94dd1dd6343acab13`, package `86a00a396c0c051a811e2048`, manifest pin
`bb8b30c80b7cb0777392bcb758b1debc4fc790bf3f7ed10a2bdb05bb81371174`, frozen release
`ea355276733439647c1ad7b9a2797a355958baaf3d6758324bb13fcb2e1144b2`.
Artifacts/report: `.codex-tmp/character-date-candidate/CHANGES.html` and sibling
corpus/field-verification/all-short-identities/verification JSON and execution receipts.
Training: 731,529 messages, 600,256 template / 131,273 provisional / zero unknown;
288 definitions, 205 supported / 83 provisional. Export parity: 166,516 captures,
zero changed assignments/outcomes. Build took 198.64 seconds.

All three original diagnostics are template assignments. Both travel examples
share `825d520b4951f33d75e54545`, capturing date KEY, CHARACTER_ID_SHORT, receiver
PARAM and final location KEY. Original Run public pipeline: 59,170 template /
143 provisional / zero no_match. Same 18-Run public-handler export: 766,476
occurrences, 3 no_match -> template; all other statuses unchanged (758,581 template,
7,842 provisional, 53 no_match). No downgrades or lost matches. Exact reconstruction,
identity distinction, LOCATOR preservation, continuation and four prior effect
checks pass. Existing recognized full-ID fields in the 20-log evidence are unchanged:
1,128 character, 3 house, 12 title occurrences.

All 75 short identities/date/receivers are recognized exactly; candidate complete
assignments: 56 template / 19 no_match. Versus v49: 34 newly matched, 8 provisional
-> template, 14 template unchanged, 19 unchanged no_match. Those 19 have final
multiword location names outside the learned final KEY; default-location display
names remain an explicit separate limitation. Do not claim the entire travel
family is solved. No universal name recognizer or new location-name field added.

The first all-75 evaluation harness failed a list-of-tuples versus list-of-lists
assertion; corrected to the renderer API shape and reran all 75 with exact text
and field-value checks. Corpus scanning now uses physical LF boundaries so CK3
formatting controls do not distort source line references; counts unchanged.
Parser unchanged; production models/catalogs, source logs, existing Runs and live
watcher/handler untouched. No candidate database writes or production activation.
Existing repeated-entry line/near-line equivalence gap remains separate.

## Disposable combined locator experiment — 2026-10-03

Completed owner-authorized follow-up: v49 restores exactly ONE LOCATOR presence
unit for the recognized variable-count message-ending location sequence. This
does not collapse KEY counts or other fields. Code change is in learning_tokens;
matcher capture/layout semantics and threshold 0.72 remain unchanged. An immutable
fresh same-20-log build is retained in `.codex-tmp/locator-presence-candidate/`,
using the prior unchanged 18-Run HandlerClient export/backup for comparison.
Frozen learner release: `25a23fd9776991fe8138bcd318818bd11df0acc8e63e215ecdd1340afebfca54`.
Focused genuine checks pass for absent, Unknown, 1/2/3-entry presence, three
independent KEY positions and two non-trailing LOCATOR positions. The real effect
pair now scores 0.775 and forms one shared KEY-effect definition at 0.72.
Full-package/stored-data verification passed. Candidate `32437a5272a3cf7586d3e741`
exports model `30a80a06501b0ecb861a2c95`, package `34993f744952a813749b9ecb`,
manifest pin `2166296d28590f6d9666dea5c3a336051b1d382a800c70938a77d55d04cc8d6e`.
Training: 731,529 messages, 600,248 template / 131,281 provisional / zero unknown;
296 definitions (204 supported, 92 provisional). Export parity checked 166,507
captures with zero changed matches/outcomes. All 18 stored Runs: 48,772 records,
766,476 occurrences, 6,875 distinct native units. v48 -> v49 changes only four
provisional occurrences to template, repairing all four effect regressions with
shared KEY-effect definition `54a08a1f7dece3a16e343bfb`; no status downgrades or
lost complete matches. Totals: 758,578 template / 7,842 provisional / 56 no_match.
Exact reconstruction, locator captures, distinct identities and continuation
checks pass. No selected KEY becomes literal; 36 custom_tooltip occurrences gain
KEY captures. Inventory changes: 23 added / 10 removed / 273 unchanged IDs;
new literal-scope inventory entries do not displace selected KEY captures in
these stored Runs. This is not a universal unseen-accuracy claim.
Original Run public pipeline: 59,168 template / 145 provisional / zero no_match;
original scope target template, both travel targets provisional (unchanged).
Report: `.codex-tmp/locator-presence-candidate/CHANGES.html`; verification and
authenticated execution receipts are alongside it. Production selection/catalogs,
backup, training logs and watcher/handler processes remain unchanged.
The presence correction resolves the effect regression, so the conditional
variable-threshold trial was not run; threshold remains 0.72.
The 0.85 calculation below was illustrative; it is not the implemented one-unit
policy. The repeated-entry line/near-line equivalence gap remains separate.

Latest owner correction: the recorded `inference_policy.field_similarity` rule
requires each recognized present field to contribute one typed similarity unit,
independent of its contents. v48 incorrectly removed repeated-location and trace
field-presence credit while removing count dependence. The v46 score's field
contributions were legitimate presence credit, not leakage of slot contents.
Restore count-independent presence credit before attributing the failure solely
to neighbor retrieval. A diagnostic calculation on the real pair retaining one
file/line/trace presence signature scores 0.85 before effect-name KEY inference;
this is illustrative, not an implemented policy. The jointly inferred fields are
KEY, REASON, LOCATOR, LOCATOR, PARAM; all five corresponding fields are present.
Runtime matching uses complete structural assignments, not similarity scores.
There is no implemented general sliding threshold: current short-form admission
only covers equal-length comparisons of at most two units with 0.49 agreement;
the three-unit v48 view falls through to 0.72. See `slot-presence-check.json` and
the corrected DIAGNOSIS.html. No matcher/learner behavior changed in this review.

Subsequent owner review identified a confirmed v48 discovery regression in the
four template-to-provisional effect occurrences. Do not treat this candidate as
ready for promotion. The two original training members are both present: current
joint inference and pair-only ordinary clustering produce the supported shared
`<KEY> effect [<REASON>]` formulation with zero failed captures. Their native
inference views contain 27 aligned units differing only at the effect-name token.
The initial comparison fell from v46's 0.87142857 (shared location fields counted)
to v48's 0.70 (location fields excluded), below the unchanged 0.72 threshold.
Full-source tracing reproduced 329 pre-regrouping groups: the correct partner
ranked 18th among 42 remaining candidates, outside the 12-neighbor limit. Other
effect formulations tie under the coarse word-set score; template IDs decide
their order. The later iteration searches only forward and never retries this
pair. Its one-member provisional definitions are an effect of missed discovery,
not insufficient corpus evidence. The earlier status-only explanation was incomplete.

Authenticated v46 focused additive source-API verification retains the old
supported definition with two settled records and zero reopened records. That
does not authorize or enable a v46-to-v48 seed: additive learning requires the
same implementation/rules/parser/threshold, and changed implementation is
explicitly rejected. Fix proposal retrieval for structurally aligned field
variants; preserve full inference/wording guards. No new inference policy was
implemented during this troubleshooting request. The independently found
repeated-entry `line:` / `near line:` equivalence omission is also outstanding.
Evidence/report: `.codex-tmp/effect-regression-review/DIAGNOSIS.html`, `trace.json`,
`ranking.json`, `v46-comparison.json`, `v46-additive.json`. Research tools:
`investigate_effect_regression.py`, `report_effect_regression.py`. The linked
CHANGES.html now flags this confirmed regression. Production remains untouched.

The owner now explicitly authorizes implementing/testing BOTH marker/Unknown
recognition and count-independent trailing locators in a disposable candidate,
using genuine ingested data. This supersedes the review-only/design-paused
boundary below, but does not authorize production registration, pinning,
replacement of stored Runs or runtime restarts.

Completed disposable experiment: v48 adds a repeated location-entry part (schema 6 / matcher API
v3) inside the existing body. `location_sequences.py` recognizes complete trailing
Script location / Stack trace sections; actual entry layouts come from genuine
members. Marker literals remain outside the repeated part; all file/line LOCATORs
and trace PARAMs expand into individually named ordered captures. Selection,
rendering and exact identity retain per-occurrence layout choices and values.
The parser, source records, deduplication key and cross-emission recovery are
unchanged. `pipeline/contracts.py` renders the new declared layout without
performing recognition; existing production definitions still render normally.

Ignored experiment: `.codex-tmp/locator-marker-candidate/`. An unchanged database
backup was read through its own HandlerClient: 18 genuine Runs, 48,772 diagnostic
records / 766,476 occurrences. Seventeen logs match retained inventory hashes;
all 18 Runs can be tested from stored definitions and values. Build uses the
corrected 20-log set, including IS3QON and the rare house_head witness. Only
IS3QON among the stored Runs belongs to that training set.

The earlier marker-only build failed because model validation still demanded a
numeric LOCATOR for line-label alternatives; the failure log/release/receipt are
retained with `marker-only-` prefixes. The combined source removes that stale
condition. A second attempt was stopped to remove repeated deep copying of large
inference metadata; another failed on a stale fixed-field lookup for dynamic
trace captures. Their logs/releases are retained with `aborted-count-` and
`count-integration-failure-` prefixes. Both defects were corrected before the
successful immutable build. Do not describe the earlier attempts as successes.

Successful candidate `56d4dbeca2c0da99a25a0d85`, published model
`e36f6ce8aa9803738d5b6237`, disposable package `4c2069e688e0a62d82222838`;
manifest SHA-256 `60bf1616772fd49fbd83a7b383a8f1a75772fa515e1dbcebc033d3b2d3267fd3`.
Frozen learner release `77d04126bfa24d588ed49bc9a5c968a40dcd02115365958cab4e472d48cfb1dc`
has completed learn and publish execution receipts. Training/export replay covers
731,529 messages: 600,244 template, 131,285 provisional, zero unmatched. Export
checked 191,357 captures with zero changed assignments/outcomes. Runtime logging
ownership and scoped whitespace checks passed.

Stored-data comparison against the same-20-log v46 package: 766,476 occurrences,
1,376 no_match -> template, 171 provisional -> template, 4 template -> provisional,
56 still unmatched, and no complete match lost. All selected native regions
reconstruct exactly; existing locator captures and distinct message identities
are preserved. Thirty occurrences now capture explicit Unknown as LOCATOR.
The four status reductions use two one-example provisional effect definitions
instead of the old two-example generic KEY-effect definition; there are no
capture/selection ties. They are disclosed, not silently called an unqualified
improvement. Genuine wrappers and the hardcoded history continuation still
recover the same messages and captures.

Genuine 1/2/3-entry scope examples share template `0213bb363ad56f39d7e953a5`,
retain 2/4/6 individual LOCATOR captures, and have distinct identities. Full
original IS3QON capture replay yields 59,168 template + 145 provisional, zero
unmatched: scope mismatch now supported; both travel messages remain provisional
with literal bodies. Date equivalence / reusable short character identity are
not implemented by this locator experiment. Parser v1.7 remains unchanged,
including its numeric recovery predicates; no genuine nonnumeric near-line
example was available to verify that recovery path.

Owner requested a human-readable delta report: `CHANGES.html` includes 15 new
definitions, 15 removed definitions with observed replacements, 15 previously
unmatched stored-message examples and their new assignments, plus the three
original production no_match diagnostics. Inventory changes: 381 -> 283 total,
144 unchanged IDs, 139 new IDs, 237 removed IDs. These are definition identities,
not counts of wholly new/lost error families. `changes.json` retains observed
crosswalks; `RESULTS.html` / `verification.json` retain full verification and the
56 unmatched occurrences. Replacement observations cover stored Runs, not an
exhaustive semantic-equivalence proof for every removed definition.

Production selection/catalog hashes, all training logs and the read-only backup
are unchanged; no production package registration, activation or runtime restart.
Research drivers: `location_candidate_experiment.py`, `verify_location_candidate.py`,
`report_locator_candidate_changes.py`. Generated artifacts remain ignored.

Latest numeric-gate clarification: `line:` and `near line:` identify location
fields; numeric content is not a prerequisite for LOCATOR recognition. All
255,228 near-line mentions in the 104-log inventory have numeric values; no
nonnumeric counterexample was found. Do not present that observation as grounds
for retaining a numeric gate. Prior cautions below about not silently changing
recovery do not authorize treating the old numeric predicate as a requirement.
Preserve established message boundaries while correcting marker/value handling.
The actual locator contents continue to count toward exact message identity.

Latest owner identity clarification: exact locator contents and count DO count
toward error-message identity and deciding whether two instances are occurrences
of the same message. Only classification similarity ignores those values/counts.
Preserve all ordered values and do not use a locator-neutral comparison view as
a deduplication or occurrence-aggregation key. Different locations can share one
template while remaining distinct messages. Guidance and HTML review updated;
no executable behavior or stored identities changed.

Latest continuation double-check: Unknown normally remains literal; only its
immediate value position after a recognized location marker permits LOCATOR
typing (`line:` and `near line:` included). Do not change recovery boundaries
as a side effect. A complete 104-log audit using the recorded package's verified
parser is at `.codex-tmp/location-variability-review/continuation-overlap.json`;
the HTML review includes every existing structure and native examples. Current
parser bytes and continuation declarations equal the recorded package; the
corrected v46 candidate has the same parser/declaration too.

Only `history-colon-title-list-v1` joins separate timestamped emissions: 11 groups,
13 title entries, no inventoried location markers in any group. Existing local
recovery overlaps location-bearing messages: 1,837,757 script-error emissions
(including all 9,055 Script location: Unknown occurrences), 87,346 quoted reader
wrappers yielding 167,882 messages, 244 participant forms with file/line in the
opening and Cheater:/With: following it, ten From forms, and six Stack trace forms.
All except reader wrappers remain one message per emission. Other multiline
envelopes are scope context (15), formatted reason (13), and quoted multiline
value (7); no inventoried markers observed there. Single-line recovery and one
unresolved unit complete the inventory. Every one of 3,344,830 original emissions
was consumed exactly once, yielding 3,425,352 messages, matching the earlier census.

Current implementation: reader wrapper recovery requires numeric near-line values; file/line envelopes
also require a numeric line. Unknown is currently accepted specially only after
Script location in that envelope. These are implementation facts, not required
numeric recognition gates (superseded by the clarification above). No genuine
Unknown-after-line witness was found. Preserve shared wrapper context, ordered history title components,
and whole script-error bodies while designing repeated locator storage.
Research helper: `tools/template_learning/review_continuation_location_overlap.py`.
Only research tooling, guidance and ignored reports changed; no executable
parser/learner/matcher rules, model release or production state changed.

Latest owner clarification: retain location markers (e.g. `Script location:`) as
literals; following entry count contributes no dissimilarity or grouping veto.
Store all actual file/line LOCATORs and trace PARAMs in order. An explicit Unknown
in the location-value position is itself one present LOCATOR value, not literal
wording, an absent location section or SQL null. This supersedes the September 27
literal-Unknown rule. Current guidance/model-contract documentation records the
new requirement; executable rules and production packages still have the old
behavior. Continue the review before implementing the representation change.

The marker inventory is complete over the same 104 logs:
`.codex-tmp/location-variability-review/location-markers.json`. Among the probed
location labels and unavailable-value spellings, only `Script location: Unknown`
was observed as an explicit unavailable value (9,055 mentions). Other observed
section markers include `location:`, `From:`, `Stack trace:`, `New Location:` and
`Previous Location:`; file/line aliases and Database were also inventoried. These
are physical marker counts, not new recovered-message classifications or an
exhaustive grammar. Empty filenames are separate evidence, not Unknown values.
`unknown-current-behavior.json` confirms an actual recorded-package provisional
assignment with REASON only and no LOCATOR capture for Unknown. The HTML report
now distinguishes the new required typing from the older positive file/line-entry
census. Current implementation still requires correction; no model was released.

Follow-up: the owner emphasizes that fixed counts after an existing recovery split
do not establish fixed counts in original emissions. Continue using recovered
messages for the variability census, and reserve existing recovery forms for
manual comparison with the problem case. `recovery-examples.json` now retains
original and recovered examples: the 1/2/3-entry scope-mismatch witnesses each
remain one `script-error` message, with 2/4/6 body LOCATOR fields; a genuine reader
wrapper becomes two messages; a genuine history continuation combines three
emissions into one message with two attached title entries. The HTML review now
shows these distinctions. No additional full-corpus pass or model change was needed.

The owner paused the proposed repeated-location correction to first measure
variability within the **same diagnostic template wording/slot pattern**, allowing
slot values to vary. The final requested unit is **recovered error messages**,
not original emissions. Original emission provenance remains available for review.
Neither a repeated-entry representation nor splitting one message into several
has been approved by this investigation; do not implement either based on the
earlier proposal. Leading date-literal equivalence remains pending separately.

Read `.codex-tmp/location-variability-review/REVIEW.html` and `incidence.json`.
All 104 retained distinct logs were examined: 3,344,830 original emissions,
3,425,352 recovered message occurrences, one unresolved recovery unit. Comparing
exact existing literal/slot prefixes before complete trailing location lists
finds 66 overlapping variable-count patterns, all from
`jomini_script_system.cpp:303`. They cover 1,828,067 message occurrences counted
once, including 596,837 with multiple entries. They are measurement groups, not
66 independent error families or newly accepted complete templates. References
are the original recorded package and the isolated corrected v46 20-log candidate;
the latter supplies the general three-KEY scope-mismatch opening. The original
package's behavior is unchanged.

That scope-mismatch pattern has 77 occurrences across 29 logs: one with one
entry (story_owner), one with two (war), and 75 with three. A separate Stack trace
form from `jomini_effect_impl.cpp:495` occurs six times, always with two entries;
no count variability was demonstrated there. The reader supplement records
329 expanded-from annotations across Unexpected token / Unknown trigger /
Unknown effect, including 48 empty filenames. These add literal annotation wording
and are not silently equated with a freely repeating trailing list.

Research tools: `tools/template_learning/investigate_message_location_variability.py`
and `report_message_location_variability.py`. All output is ignored. Counting
agrees with the earlier 73-log detailed location inventory on 1,165,336 native
message occurrences / 1,807,351 entries, with zero differences. No learner/matcher
algorithm, parser, package selection, source log, stored Run or runtime process
was changed. The next step is owner review of the incidence and native examples,
before deciding whether or how to change message boundaries or representations.

## Corrected rare-case 20-log experiment — 2026-10-03

[Evidence-selection correction and results](LEARNER_V46_QUOTED_DISCOVERY_RESULTS.md).
The first v46 training set excluded the three original diagnostics and house_head;
IS3QON was only evaluated afterward. That was insufficient for the target question.
Execution receipts nevertheless confirm the changed v46 code ran.

Rebuilt frozen v45 and v46 on the same corrected 20 logs, explicitly including all
rare witnesses. Both yield complete provisional assignments for war and the two
travel errors, and a full shared assignment for house_head. All selected assignments
and captures agree on 731,529 messages. Travel identities/dates and war's scope text
remain singleton literals; these are not solved reusable formulations. Eight
alternative IDs differ. No additional learner implementation change was made.

Review artifacts: `.codex-tmp/learner-v46-targeted20/RESULTS.html`. The exported
candidate and read-only pipeline checks passed; production remains unchanged.
Continue from these corrected results, not the earlier missing-target experiment.
Keep the existing review boundary for further recognition/location-stack changes.

## Known-path source-scope repair delivered — 2026-10-03

[Latest receiving delta and evidence](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md):
unscoped default is all recorded-playset roots; supplied scope must narrow work.
SourceSearch now selects members before disk probes and derives nonrecursive
parent scopes for known paths. Explicit directory restrictions remain effective.
41 genuine scope comparisons and four multi-Run source investigations / 93
comparisons passed, preserving candidates and counts without a directory workaround.
08B receives this completed repair; do not repeat or replace it. Prior blanket
default-acceptance and open-repair notes below are historical. Prompts unchanged.

## Default inventory behavior accepted — 2026-10-03

Owner accepts default enumeration of all selected recorded-playset roots.
Code docstrings now explain that omitted directories mean whole roots; filenames
and references filter afterward; explicit roots/members/directories narrow scope;
inventories contain paths and are reused within the investigation. No runtime
change. [Receiving clarification](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md) supersedes
the automatic-narrowing defect/open-repair classification below. 08B should
document the accepted default and retain explicit controls. Prompts were not edited.

## Do not claim unconditional 08A completion — 2026-10-03

[Requirement-by-requirement reconciliation](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md)
separates delivered capabilities, owner-directed median/newness changes, genuine
verification limits and the open 08A.2 known-path traversal defect. Assigning that
defect to 08B does not fulfil the original source-scoping requirement. The latest
passing source queries explicitly supplied directory scope; automatic narrowing
is still outstanding. Prompt edits were restored and no prompt was changed by
this reconciliation. The prior blanket completion wording was too broad.

## Included-window newness correction complete — 2026-10-03

[API changes and checks](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md). Newness is
selected count positive and no observation in any included predecessor. Removed
the unavailable-read veto/`QueryEvidenceError`, median/baseline fields and derived
notability labels. Counts and fractions remain; no replacement formula was added.
Consumers must use `history.newly_observed` and actual `history.counts`.

Reverified the unchanged four-Run backup: 18 investigations, 359 comparisons,
zero mismatches, plus two genuine single-Run checks. Logging/imports/pip passed.
Current report: `.codex-tmp/task08-multirun/WINDOW_NEWNESS_REPORT.md`.
Evidence: `.codex-tmp/task08-multirun/2624478c0021411d861144eaff16e3c6/presence-review/`.
No synthetic checks, runtime failure special cases, added dependency, production
write or new requirement. The verification handoff lists the required 08B
consumer changes. Median/newness edits to task prompts were restored per owner
direction; future receiving changes belong in the handoff. The separate
automatic traversal-scope correction remains open.

## Genuine timestamped history validated — 2026-10-03

[Verification results](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md) supersede the
earlier blocked outcome: four eligible Runs in package `68f1ae5db205ab46afef9c4d`,
17 completed investigations, 340 actual-data comparisons, zero mismatches.
Unchanged backup/evidence: `.codex-tmp/task08-multirun/2624478c0021411d861144eaff16e3c6/`.
Readable queries/results: `.codex-tmp/task08-multirun/TIMESTAMPED_MULTIRUN_REPORT.md`.

Latest `20261003-74G2EB` has three eligible predecessors. Whole-message
`failed context switch` returns 51 diagnostics / 245 occurrences; the exact
sea_minority file scope returns 2 / 64 and selected EB+EC724 mod returns 15 / 84.
Each Run's filtered identity/count maps and recorded members were verified.
Stored template references select ingestion assignments with OR; no template
wording search substitutes for whole-message content including slot values.

No runtime changes or new requirements. No synthetic data or failures.
One premature report-generation command failed, then succeeded after the final
integrity evidence was written; data comparisons all passed. Logging/imports/pip
checks passed. Failed-read/unavailable-source cases remain
unexercised. Continue 08B separately; its known traversal-scope repair is still open.

## Learner v46: approved changes and fresh 20-log candidate — 2026-10-03

[Results and continuation boundary](LEARNER_V46_QUOTED_DISCOVERY_RESULTS.md).
Implemented quoted-content-neutral discovery and one batch per identical-template
identity after the existing regrouping sweep. Threshold .72 and inference/matching
guards remain. Fresh 20-log build completed in 211.85 seconds; all 671,898 selected
assignments and capture bindings match the same-input v45 baseline. Seven unused
alternative definitions change; review details are in the ignored HTML report.

Candidate/package and authenticated learner release live only under
`.codex-tmp/learner-v46-20logs/`. Export validation checked 153,431 captures and all
35,362 contextual messages. Production catalogs/pin/processes/Runs/logs are unchanged.
All three original IS3QON diagnostics remain unmatched in this limited 20-log model.
No 104-log rerun or production activation was performed. Review this candidate
before deciding the next corpus/classification step; preserve the prior investigation.

## Genuine multi-Run verification — timestamp prerequisite absent — 2026-10-02

[Latest verification handoff](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md).
Configured current database: 14 genuine Runs / package `68f1ae5db205ab46afef9c4d`,
38,269 record rows / 683,608 occurrences, but **no Run has the required source
timestamp**. All 14 exclusions and explicit/latest selection failures were
verified on an unchanged disposable backup through `HandlerClient`.

The requested chronological acceptance is incomplete. Do not use Run IDs,
processing times or capture times as an alternate order; do not backfill facts.
An existing database with eligible timestamped history is needed. The owner was
asked whether another database was intended. Readable report and precise queries:
`.codex-tmp/task08-multirun/MULTIRUN_VERIFICATION_REPORT.md`; full evidence/backup:
`.codex-tmp/task08-multirun/049e5d1d395f4ad6b31008f177e9edab/`.

Real source/identity components were independently checked across all 14 Runs,
using each recorded playset. Their expected/actual filtered counts agree and
exclude out-of-scope identities; raw exact counts remain separate. 253 actual
data comparisons had no mismatches. No runtime changes were needed by those
checks. No synthetic evidence or new requirements were added. The ignored report
generator had one string-literal error, corrected before producing the report.
Logging ownership/imports/pip check passed. Only documentation and ignored
verification artifacts changed; no production writes or live restarts.

## Advisor receiving review — 08B ready with first repair — 2026-10-02

[Receiving review](TASK08B_RECEIVING_REVIEW.md): inspected both 08A deliveries and
reran all 15 retained genuine-data checks successfully. A public-handler syntax
selector probe returned the two actually present matches, including provisional
status. Static logging ownership, isolated imports and pip check passed.

[08B's prompt](TASK08B_PROMPT.md) now receives the actual APIs, available syntax
research and owner-directed real-evidence verification policy. It explicitly
assigns the remaining source-scope correction as its first bounded receiving
repair: apply known exact path/directory constraints before enumeration, without
widening scope to populate a cache. The correction is not yet implemented.
Multi-Run and absent real failure scenarios remain unverified. The fresh broad
content search took 181.405 seconds; no fixed performance threshold is inferred.
See the review for evidence paths and limits. Runtime code and production state
were unchanged; only disposable verification handlers were used.

## Task 08A.2 implementation delivery — 2026-10-02

Latest owner review concerns inventory memory and actual traversal scope.
Measurements/recommendations are in the 08A.2 handoff and ignored
`.codex-tmp/task08a2/memory/MEMORY_REVIEW.md`: full path inventory 11.54 MiB;
single-reference parent scope 96 KiB; all-reference parent scopes 2.68 MiB.
Full and parent-scoped inventories find exactly the same real candidate pairs.
Direct file checks reach the same files with one recorded/on-disk case-spelling
difference, verified with `Path.samefile`. No runtime strategy changed, packages
installed or synthetic checks added. Automatic lookup still needs its directory
constraints pushed ahead of traversal; preserve the owner's prohibition on
widening a narrower requested scope to fill a cache. 08B itself remains unimplemented.

Owner follow-up: the readable report now shows all 133 stored members in a
load-order table and includes explicit load-order numbers beside candidate names
and excerpt headings. Outside-playset roots show recorded order unavailable.
The 08A.2 handoff, 08B prompt and reporting ledger preserve this display requirement.
Regenerated from saved genuine evidence; no runtime code or new tests needed.

Delivered [source search/context and its 08A.1 integration](TASK08A_2_SOURCE_SEARCH_HANDOFF.md).
Public API: `SourceSearch(client=None, ripgrep=..., context=..., excerpts=...)`
(options keyword-only), `read_playset`, `search`, `resolve`, `excerpts_for`,
`clear`, and `source_references(record)`. Pass it as `DiagnosticAnalysis`'s
`source_resolver`. Required source predicates now work; optional source context
leaves SQL totals usable. 08B receives both deliveries and owns presentation.

Added reporting `source_query.py`, `source_references.py`, `source_search.py`;
extended `query.py`, `analysis.py`, `__init__.py`; added only genuine-data checks
in `tests/test_source_search_genuine.py`; updated both handoffs and current docs.
No handler/watcher/learner/schema changes. Unrelated dirty work is preserved.

Nine new checks passed twice; final run 64.248 seconds. Six existing genuine
diagnostic checks passed in 31.454 seconds. No failures/skips, synthetic scenarios
or injected errors. Full evidence and disposable SQL backup:
`.codex-tmp/task08a2/7db8b47229564e748a47221366512b0b/`.
Readable filters/results/excerpts:
`.codex-tmp/task08a2/SOURCE_SEARCH_REAL_DATA_REPORT.md`.
The handoff names each precise check, measured scope/timings and genuine cases
not exercised. Initial inspection encountered a console Unicode print error and
found a reference-slot provenance overlap; both are documented. No requirements
beyond the task were introduced.

The 133-member playset supplied 105,603 inventory entries; large content search
covered 11,914 text files in 66 Windows ripgrep batches. The 2,475 diagnostics /
4,182 occurrences remain unchanged despite 2,651 candidate associations. No
dependency installation was needed: ripgrep 15.2.0 already exists on PATH.
Logging ownership, isolated imports and pip check passed. No live processes were
restarted or production state modified. Do not restore removed synthetic tests;
missing real evidence stays explicitly unverified. Earlier checkpoints follow.

## Task 08A.1 implementation continuation — 2026-10-02

Delivered [diagnostic query/analysis library and handoff](TASK08A_1_DIAGNOSTIC_QUERY_HANDOFF.md).
New files are `src/ck3chronicle/reporting/{__init__,query,analysis}.py`,
`tests/test_reporting_query_requirements.py` and that handoff. This task also
updates the opening status/plan/reporting-ledger sections; all unrelated dirty
changes remain. No existing pipeline/handler/watcher/learner code was changed.

Public entry point is `DiagnosticAnalysis(HandlerClient(database_file))` with
`investigate(run, package_id=..., query=...)` and eligibility-first `list_runs`.
Results include effective filters, exact totals/rollups, stored rendering,
historical zero-count entries, requested/obtained windows, unavailable evidence,
review metadata and chronology exclusions. A required source filter fails
explicitly until 08A.2 supplies `SourceResolver`; no temporary search engine exists.

Owner review removed all 12 synthetic/scalar reporting checks plus the injected
request-failure and file/import-guard checks. Six genuine-data checks remain and
passed with no failures or skips. No invented metadata, counts, mock clients or
failure injection remains in this reporting test file. Its misleading syntax-test
name is now `test_record_selector_and_positive_occurrence_filter`; it does not
claim to verify the syntax preset. Do not restore the removed checks or turn their
scenarios into owner requirements. Report failures and proposed scope additions.

Current evidence is `.codex-tmp/task08a1/verification-after-synthetic-removal.txt`
and `35906eab57f24c338148dddc4803eadc/baseline.json` beneath that directory. All six
checks passed again in 9.732 seconds, with no failures or skips; logging ownership,
isolated imports and dependency checks passed again too. The unchanged
SQL exercise contains one eligible Run, 2,475 records and 4,182 occurrences.
Multi-Run behavior, threshold boundaries and failed-read behavior remain unverified
by genuine data. Earlier synthetic passes are not acceptance evidence. The owner
subsequently directed removal of the pre-existing synthetic logging suite too:
`tests/test_runtime_logging_requirements.py` and all seven checks are deleted.
Do not restore it from older handoffs or ignored runners. The arbitrary 32-level
query nesting cap was removed. Source inspection found no reporting branches
keyed to mock clients or fabricated messages; handling of documented handler
errors and unavailable comparisons follows the original task. No logging, handler
or watcher runtime code was changed. Earlier execution logs remain historical.

Continue with 08A.2's prompt and this delivered source/query boundary. Implement
and verify reference extraction, explicit roots/optional members, all-candidate
search, incomplete-coverage errors, file rollups and excerpts before 08B. The syntax
research handoff is available; the shared OR-selector interface can express its
exact conditions. CLI/presets remain 08B's task. Production operation restrictions
remain in force; nothing was committed or pushed.

## Source-search and 08B receiving corrections — 2026-10-02

Updated [08A.1](TASK08A_1_PROMPT.md), [08A.2](TASK08A_2_PROMPT.md) and
[08B](TASK08B_PROMPT.md): source roots need not belong to a playset; content
conditions evaluate across a file; unavailable required source associations
produce explicit errors with partial coverage/results retained. Optional context
remains distinct from a required filter. Added ripgrep configuration isolation,
structured output, match/no-match/error handling, missing-executable guidance
and actual Windows invocation verification to 08A.2's assignment.

08B names both split prompts and `TASK08A_1_DIAGNOSTIC_QUERY_HANDOFF.md` /
`TASK08A_2_SOURCE_SEARCH_HANDOFF.md`. It starts after both deliveries and their
query/source integration are complete. Removed rejected timestamp and mandatory
playset recommendations from the separate review; the owner's session-end
wording is unchanged. Documentation edits only; checked ripgrep help/documentation
and document links, not runtime implementation or production behavior.


## 08A.1 / 08A.2 prompts finalized — 2026-10-02

[08A.1](TASK08A_1_PROMPT.md) now explicitly supports OR selection of multiple
stored matched-template references and uses diagnostic-record search terminology.
[08A.2](TASK08A_2_PROMPT.md) requires efficient disk search from the start:
ripgrep bulk search, reused in-memory filename/path inventory, batching, early
filters, bounded streaming, explicit coverage settings and representative large
real-playset timings. The remaining prompt policies were preserved. The template
representation recommendation is withdrawn; unrelated recommendations remain
unapplied in [the separate review](TASK08_SPLIT_REVIEW.md). No implementation,
installations or runtime actions were performed; 08B was unchanged in this pass.

## Owner-updated reporting split — 2026-10-02

The current sequence is [08A.1 diagnostic queries/analysis](TASK08A_1_PROMPT.md),
[08A.2 playset source search/context](TASK08A_2_PROMPT.md), then
[08B reports/CLI](TASK08B_PROMPT.md). The owner's supplied revisions are the
baseline; changes are limited to task division, receiving boundaries and requested
search-library guidance. They supersede conflicting older planning text below.
Prompts are prepared, not implemented. See [the split review](TASK08_SPLIT_REVIEW.md)
for the scope mapping and separate unapplied recommendations. Documentation only;
no runtime actions or installations.


## Syntax research ready for Reporting and Analysis — 2026-09-30

[CK3 syntax diagnostics research](CK3_SYNTAX_DIAGNOSTICS_RESEARCH.md#concrete-selector-handoff)
supplies nine explicit selectors over existing stored definitions/values for
package `68f1ae5db205ab46afef9c4d`, including the exact REASON condition needed
to distinguish assignment errors from semantic errors sharing a template.
It includes genuine excerpts, source hashes, citations, exclusions and limited
extent/cascade findings. Both stored match statuses remain eligible.

The owner requested verified findings only. Unverified brace-balance formulations
have been removed from the proposed list; the observed `Unexpected token: =`
and `Malformed token: {` remain with their precise meanings. Context-dependent
messages are research evidence, not syntax-preset selectors. The recorded
eight-Run research snapshot yields 16 records; this is not a new live query.

The [2026-10-01 brace follow-up](CK3_SYNTAX_DIAGNOSTICS_RESEARCH.md#brace-token-follow-up--2026-10-01)
searched 82 distinct retained logs. It verifies quoted `'}'` in event-ID,
namespace and missing-theme messages, but finds no `token: '}'` spelling.
Exact template IDs and native excerpts are recorded as contextual clues;
brace imbalance remains unproved and the nine proposed selectors are unchanged.

Research delivery only: Reporting and Analysis reviews this handoff when building
08A/08B. Updated the report and receiving-document links; no runtime code,
classification, ingestion, storage, model selection or reporting implementation
was changed. No production ingestion or service restart was performed.

## Reporting and Analysis prompt handoff — 2026-09-30

Prepared [08A](TASK08A_PROMPT.md) and [08B](TASK08B_PROMPT.md) together. Execute
08A's reusable investigation/history/search services first; 08B consumes its
actual handoff to deliver presets, CLI and HTML/text/JSON with linked excerpts.
The [reporting ledger](TASK08_SCOPE_REVIEW.md) records ownership, dependencies
and drafting rationale. Old Task 08 audit instructions are superseded.

The timestamp field is already confirmed by the receiving check below. Exact
recurrence stays within a selected package; missing timestamps exclude Runs,
and short history is valid. Disappearance analysis includes historical identities
with selected count zero without creating stored records. The syntax research
delivery above now supplies that preset's selectors for receiving review.

Updated the two prompts and planning pointers only. Inspected focused source and
handoffs; did not rerun runtime checks, open the live database, change processes,
ingest captures, alter selection, reset/expire data, commit or push. Rejected
handler design documents were not read. Implementation is not claimed.

## Pipeline source modification timestamp receiving check — 2026-09-30

The existing capture-metadata → handler-owned write → `runs.facts_json` →
public Run facts path preserves `error_log_source_modified_at` exactly.
Read it as `run["facts"]["error_log_source_modified_at"]` when present;
historical/manual absence remains unavailable. See the
[current pipeline handoff](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md#source-modification-timestamp-receiving-check--2026-09-30)
for the exact path and evidence distinction.

Reviewed the inherited watcher source-mtime suite's 43-check result; did not
rerun it. Ran two additional focused checks on disposable copies: all public
Run reads preserved the nine-digit string, and a duplicate with conflicting
capture metadata preserved the entire stored Run. Both passed without skips.
Evidence and reproducer are ignored under
`.codex-tmp/pipeline-source-mtime-receiving/`. No preservation gap or implementation
change was needed. This follow-up changes only that pipeline handoff and this
ledger, plus ignored verification artifacts. Existing unrelated work is preserved.
No production ingestion, live restart, historical mutation, commit or push.

## Watcher source modification time — 2026-09-30

`spool_logs` now records `error_log_source_modified_at` from the validated
original source stat in the existing capture metadata. The existing ingestion
path preserves it in SQL Run facts without a schema change. See the
[focused handoff](WATCHER_SOURCE_MTIME_HANDOFF.md) for the field, genuine-input
checks and ignored disposable evidence. Changed files for this follow-up are
`harvester.py`, the new `test_capture_source_mtime_requirements.py`, that handoff
and this ledger. Existing unrelated changes are preserved. No historical
captures/Runs, production configuration or live processes were modified;
activation remains separate. Nothing was committed or pushed.

## Task 07E live activation - 2026-09-30 08:28 Hong Kong

Following owner authorization, the updated watcher was started hidden at
00:27:53 UTC. The previous PID was absent, its heartbeat was stale, the runtime
lease was free, and no old handler was listening. The exact configured database
passed read-only schema-3 verification. CK3 was already running, so the new
watcher attached to that process without interrupting the game.

Watcher PID 34340 (launcher 9792) observed CK3 PID 44816; a fresh heartbeat at
00:28:23 UTC confirmed `running`. Handler PID 308 reported `handler_ready`, with
instance `71d783fe8dc34ea6b4b0f7140de130b2`. Startup ingestion found all five
readable retained captures already stored and returned ordinary duplicate
non-completion. Twenty-two older inaccessible captures remain unavailable;
permissions were not changed. No watcher/handler ERROR events were observed;
bootstrap stderr was empty. Configuration, model selection and database identity
were unchanged; no reset or forced expiry was performed.

Evidence: ignored `.codex-tmp/task07e/activation.json`. Logs now use the 07E
paths in [the handoff](TASK07E_RUNTIME_LOGGING_HANDOFF.md). The attached game's
exit was subsequently observed at 01:26:28 UTC and ingestion completed at
01:26:36 UTC as Run `20260930-BYVZUV`, request
`3f5002c984d94334b65205052b4916ed`. Its merged trace is retained under
`.codex-tmp/task07e/live-session-20260930-BYVZUV/`. Capture and ingestion took
7.657 seconds, with no warning/error/contention events for that request.
Attachment after game startup does not establish complete observed start-to-exit
Trusted Run acceptance. Task 08 and
Run-result replacement remain separate. The following implementation-delivery
checkpoint predates this separately authorized activation.

## Task 07E delivered — activation remains separate — 2026-09-30

[Task 07E's handoff](TASK07E_RUNTIME_LOGGING_HANDOFF.md) documents the shared
standard-library logging owner, bounded UTF-8 JSONL files, watcher/request-ID
correlation, preparation/database timing, compact contention episodes, tracebacks
and durable bootstrap stderr. EventJournal preserves lifecycle vocabulary and
the replaceable heartbeat. Runtime logging failures do not change Run outcomes.
Future runtime code uses `runtime_logging.py`; run `tools/check_runtime_logging.py`.

Fresh verification passed **66 checks, no failures, errors or skips**, in 86.156
seconds: the 59 receiving checks were rerun alongside seven focused logging
checks, using genuine retained CK3 inputs and disposable storage. Static ownership,
isolated imports and `pip check` passed. This is distinct from the inherited
September 30 07D handoff's 59-check result. Evidence is ignored under
`.codex-tmp/task07e/`; the handoff records coverage and limitations.

The [07D API contract](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md) is preserved:
one dedicated handler, one preparation thread, one database worker, exactly three
public states, all unfinished requests plus the latest 256 terminal outcomes,
`LookupError` for unavailable results, `exception_class`, and internal-only
`cleanup_unaccepted`. Watcher `ingestion_outcome_unavailable` still creates no
outcome or eviction retry. SQL/review/playset formats and ingestion/retention
semantics are unchanged. Logging does not recover outcomes after abrupt termination.

No production configuration, selection, storage, captures or live processes were
changed; nothing was committed or pushed. The unrelated dirty tree is preserved.
Next operational step: follow the 07E handoff's separate procedure to stop the
watcher at a quiet boundary, shut down the old handler for the configured file,
verify that file read-only, and start the updated watcher. Startup ingestion and
daily retention keep their existing behavior. Task 08 SQL reports, Run-result
replacement and complete Trusted Run acceptance remain separate assignments.

## Historical checkpoints and separately scoped proposals

## Task 08/09 look-ahead proposal — 2026-09-29

[TASK08_TASK09_SCOPE_PROPOSAL.md](TASK08_TASK09_SCOPE_PROPOSAL.md) recommends
rewriting 08 as complete SQL reports/bounded audit over delivered 07D APIs and
retiring the old 09 offline reconnection/deletion draft. The proposed command
surface and sequencing are recommendations, not owner-approved implementation
instructions. Existing storage read/render APIs and 07C learner operations were
source-inspected; no runtime/learner campaign was rerun. The rejected database
handler design was not opened. 07D remains the active implementation assignment;
Run-result replacement and final Trusted Run acceptance remain separate.

## Task 07 receiving review and separate 07D assignment — 2026-09-29

Use [TASK07D_PROMPT.md](TASK07D_PROMPT.md) for the new team's implementation
assignment and [TASK07_QUALITY_REVIEW_FOR_07D.md](TASK07_QUALITY_REVIEW_FOR_07D.md)
for independent source/verification findings. The rejected design/copies were not
opened for this receiving review and are prohibited reading for 07D. The owner's
new in-memory, three-state direction supersedes the old design-review/stop gates.

Five receiving checks passed with no skips in 102.916 seconds, including three
complete genuine inputs, both packages in one database, SQL/review/playset
agreement, native rendering and disposable retention/initialization. Evidence is
ignored under `.codex-tmp/task07d-advisory-review/`. No core ingest/storage rewrite
was identified. Assignments 07D-01 through 03 cover shared runtime routing,
caller outcome reconciliation and current API/handoff repairs.

07D code/integration/verification remain to be delivered; this pass prepared
instructions and reviewed existing code. No product code, production data,
configuration, selected package or live process was changed. Historical activation
does not establish current live status. Task 08 and Run-result replacement remain
separate. Older rejected-design continuation text below is historical only.

## Rejected database-handler design retired

The owner rejected the shared-database-request-handler design as materially
over-scoped. `PIPELINE_QUEUED_INGESTION_DESIGN.md` has been deleted. Its review,
continuation and implementation instructions are withdrawn; no replacement design
or implementation is authorized by this cleanup. A replacement instruction will
be issued separately. Earlier queue follow-up references below do not authorize
implementation of the deleted design.

Repository inspection found no implementation derived from it: no request handler,
named-pipe transport, owner-election/request-recovery machinery, expanded request
states, or related schema/runtime integration. Ingest still opens the repository
directly; the watcher uses its existing local executor. SQL/review version 3 and
existing capture locks predate the rejected design and remain unchanged.

Only documentation was changed. No production data, configuration, runtime code or
live process was changed; current live-process status was not checked. Cleanup is
complete; stop here pending the separate replacement instruction.

## Watcher live ingestion activated; database naming implemented — 2026-09-29

The owner directed completion rather than leaving operational setup outstanding.
See [WATCHER_LIVE_ACTIVATION_HANDOFF.md](WATCHER_LIVE_ACTIVATION_HANDOFF.md).
The watcher was restarted at 21:19:39 UTC with worker PID 5032 and launcher PID
51116. It now ingests completed captures into the explicitly configured database
`ck3chronicle-schema3-20260928T211854Z.sqlite3` in the existing runtime directory.
Startup ingestion accepted all five readable captures (12,449 diagnostic records);
SQL/playset/review agreement and the new heartbeat are verified. Daily retention is enabled, first due one
day after startup. Twenty-two inaccessible older capture directories were
reported and skipped; permissions and the old legacy DB were not changed.

The approved storage naming is implemented in its owning APIs: `create_database`,
`open_database`, `open_database_readonly`, `Database`, `database_info` and
`database_id`. Open/ingest/config now take an exact SQLite file path. Schema and
review manifest are version 3; playset format stays 1. No compatibility alias,
migration, replay or newest-file discovery was introduced. Forty-five checks
passed before activation. Shared pipeline queuing remains the separate pipeline
follow-up; the actual watcher caller and operational activation are delivered.

## Watcher-to-ingest caller implemented — 2026-09-29

See [WATCHER_INGESTION_WIRING_HANDOFF.md](WATCHER_INGESTION_WIRING_HANDOFF.md).
The actual `cmd_watch` -> published capture -> completion callback now invokes
the existing ingest API on a serial worker outside lifecycle polling. Startup
submission, daily maintenance/retention, journaled outcomes and config defaults
are implemented. Protected error logs publish even when debug capture or playset
extraction fails. A narrow pipeline correction accepts malformed/mismatched
playsets as unavailable, with explicit `IngestResult.warnings`; supplied JSON is
preserved. These changes were verified through the actual watcher caller using
genuine inputs and disposable SQL storage. The pipeline's shared request queue
remains separate work and no longer blocks the watcher caller's implementation.

The owner approved `ck3chronicle-schema<N>-YYYYMMDDTHHMMSSZ.sqlite3` naming;
the pipeline filename/API terminology change is not yet implemented. No existing
database was deleted or renamed. The ignored config now contains explicit watcher
defaults, but current-schema production storage has not been initialized. The
live watcher started earlier still runs the previously loaded capture-only code;
this delivery has not restarted it or activated production ingestion/retention.

## Owner ingestion/retention decisions and pipeline queue request — 2026-09-29

The owner approved processing otherwise valid new error logs with missing,
malformed or mismatched playsets: report the problem, preserve source JSON and
store the existing unavailable-playset representation. A debug-copy failure must
also not block publication/ingestion of an already protected error log; that
capture change belongs to the watcher. Extract playsets only from copied pairs.
All completed captures enter ingestion, with startup identification and another
attempt for captures not accepted into SQL. Retention cadence is DAILY, with
the already-approved 30-day expiry policy unchanged. Configuration must have
sensible defaults and require no routine interactive setup.

This checkpoint's queue follow-up was later covered by the now-rejected handler
design. The [former prompt](PIPELINE_QUEUED_INGESTION_FOLLOWUP_PROMPT.md) is retired;
its queue/durability review and implementation instructions no longer apply.
Replacement instructions will be issued separately. The existing watcher caller
and its contention handling are unchanged.

The owner also questions legacy generation terminology and wants a consistent
database filename incorporating schema and initialization date/hour. A precise
UTC naming convention is proposed in the prompt, pending confirmation. No database
deletion, reset, rename or migration is authorized by that naming discussion.
This checkpoint and the prompt are documentation only; no live watcher, pipeline
code, operational config or production data was changed. Earlier malformed-playset
rejection and hourly-retention proposals below are superseded by these decisions.

## Task 07 implementation and verification checkpoint — 2026-09-28

Continue from [TASK07_INGESTION_AND_RETENTION_HANDOFF.md](TASK07_INGESTION_AND_RETENTION_HANDOFF.md).
Working ingest/retention APIs and the manual command are implemented. SQL schema 2
and review manifest 2 store ordered playsets and per-Run processing lineage. Three
genuine complete inputs passed API/CLI ingestion, cross-package duplicates, both
packages in one DB, native rendering/review accounting, playset agreement, explicit
schema-reset refusal, failure cleanup and disposable retention. Two native requirement
checks passed; evidence and limitations are in the handoff.

Exact continuation: obtain the already-requested owner disposition for malformed or
mismatched completed playset JSON. The current reviewable proposal raises PlaysetError
and preserves the capture; missing JSON is allowed. Do not claim Task 07 fully closed
before that decision. After closure the watcher team wires both automatic triggers;
Task 08 reports and separate live activation remain outstanding. No watcher trigger
or production change was made. Explicit Run replacement is separate follow-up work.

Task 07 changed `pipeline/schema.py`, `repository.py`, `review.py`, added
`ingestion.py`, `playsets.py`, `capture_access.py`, `retention.py`, added the ingest
handler/arguments in `cli.py`, native requirement checks, and the handoff/status/plan/
execution-order/scope/README documentation. Preserve the substantial pre-existing
dirty tree. Harvester, watcher, models, learners, selection and live configuration
remain untouched by this task. Scratch evidence is under `.codex-tmp/task07/`.
The completed Script location-stack findings remain context, not a pending task.
This checkpoint supersedes earlier implementation-pending continuation points below.

## Task 07 advisory review after 07C — 2026-09-28

Reviewed current source and delivery documents; Task 07 remains unimplemented.
The [prompt](TASK07_PROMPT.md) now uses 07C package selection
and existing `contracts.run_lineage`, removes ingestion-side learner-provenance
follow-up and recognizes the completed location-stack investigation. The
[scope review](TASK07_SCOPE_REVIEW.md#current-task-ledger) holds the compact task
ledger: the owner chose expiry of all completed captures, including failed/unprocessed
ones, after 30 elapsed days from capture time; malformed-playset disposition remains
pending. Current selection remains unchanged. Next: settle that choice, execute Task 07, then watcher-team
wiring and Task 08 SQL reports. This pass changed documentation only; no runtime
checks, production operations or independent rerun of delivery verification.

## Advisory transfer — 2026-09-28

Use the [Task 07 onward advisory transfer prompt](ADVISORY_HANDOFF_TASK07_ONWARD.md)
for the new planning/advisory task. It incorporates the delivered 07C release
handoff and completed Script location-stack investigation, distinguishes them
from older open-item wording below, and records current owner decisions and
remaining team boundaries. This transfer is documentation work, not Task 07
implementation or independent re-execution of 07C verification.

## Task 06B cleanup completed — 2026-09-28

The deprecated CLI/provider stack and its exclusive research/test consumers have
been removed. See [the cleanup handoff](TASK06B_DEPRECATED_CODE_CLEANUP_HANDOFF.md)
for the exact inventory, portable rollback archive, verification and limits.
`watch`, `capture`, `doctor` and `observe-logging` remain; `watch --once` remains
error-only. `harvester.py` remains the capture owner. No processing command is
active. Task 07 delivers ingest and retention APIs, one manual `ingest` command,
playset SQL storage and a watcher-team integration handoff. The watcher team owns
automatic ingest after capture and periodic retention checks, including idle periods.
See the [current scope](TASK07_SCOPE_REVIEW.md)
and [revised draft](TASK07_PROMPT.md).
Task 07 must remove the current database-wide lineage
lock and record processing versions per Run; compatible selections share one
database. Schema changes require an explicit reset, without migration or fallback.
These are instructions for implementation, not completed code. Retention eligibility
and cadence remain open. Task 08 focuses on SQL reports/read operations.
The old provider retirement, C1/C2 capture relocation/deletion proposal, parser
comparison retirement and removed-API research checks are discharged/superseded;
do not repeat them or restore compatibility providers. Task 06/v45 storage and
the watcher producer contracts remain intact, as do learner policy limitations
and the separate Script location-stack investigation. The separately authorized
live watcher was not stopped, restarted, reconfigured or used for verification.
Older dated provider-retention and cleanup-pending statements below are historical.

## Next: Task 06B cleanup, then Task 07 — 2026-09-28

The owner authorized disabling unused old CLI paths and removing their deprecated
providers before Task 07. Execute [Task 06B](06B_DEPRECATED_CODE_CLEANUP.md), then
[Task 07](TASK07_PROMPT.md) against its completion handoff.
Keep the working watcher/playset producer and capture owner `harvester.py` in place;
the earlier plan to relocate capture into `pipeline/capture.py` is superseded.
The watcher review's Section B supplies specific retirement targets. This checkpoint
records the assignment and revised prompts, not completed deletion. The live
watcher's separate operating authorization and Task 06's selected baseline remain.
Older instructions to retain unused CLI providers until cutover are superseded for
the explicit 06B scope.

The owner additionally requires 06B to archive every pre-edit/deleted file through
PowerShell before cleanup, delivering a portable archive with `cleanup.ps1`,
standalone `rollback.ps1`, inventory and restore README. Keep the archive available
for the owner to zip and move outside the repo; rehearse rollback on disposable
copies from a relocated archive. The Task 06B prompt contains the full requirements.

## Live watcher started at owner request — 2026-09-28

Started the updated continuous watcher in a hidden background process at
06:55:46 UTC using `.venv/Scripts/python.exe -B -m ck3chronicle.cli watch`
from the repository root. Worker PID: 46516; virtual-environment launcher PID:
61708. The worker holds the runtime lease and its journal reports
`watcher_ready` / `awaiting_game_start`; CK3 was absent at startup.
The worker's heartbeat was verified at 06:56:17 UTC.
Journal: `.ck3chronicle/wip/runtime/watch/events-20260928T065546.589644Z-46516.jsonl`.
New observed exits will publish paired logs and playset templates to the
configured pending directory. Pipeline processing remains a separate task.
This operating checkpoint supersedes the earlier statements that the live
watcher had not yet been started; no autostart or scheduled task was installed.

## Watcher active-playset producer delivered — 2026-09-28

The owner approved implementation of the watcher plan. Continuous `cmd_watch`
now copies the full error/debug pair, extracts the emitted active playset,
resolves descriptor names, hashes both protected files and writes `playset.json`
before existing pending publication. The joined identifier is
`sha256:<error_log_sha256>:<debug_log_sha256>`. Outcomes and metadata problems
go to the watcher journal without continuous-watcher terminal messages.

Production changes are confined to new `src/ck3chronicle/playset.py`, capture
support in `harvester.py`, actual watcher wiring in `cli.py`, and a small
`EventJournal` option in `watcher.py` for safe startup-failure logging. No root
configuration changes were required. Manual commands keep their existing behavior.
Tests were added/extended in the two watcher/playset capture requirement files.

39 focused checks passed, including existing processing-recovery coverage.
An isolated demonstration on recent real log copies produced 133 members,
zero UNKNOWN names and zero resolution warnings; both copied files and their
serialized hashes verified. Generated evidence is ignored under
`.codex-tmp/watcher-playset-implementation/`.

See [WATCHER_ACTIVE_PLAYSET_HANDOFF.md](WATCHER_ACTIVE_PLAYSET_HANDOFF.md) for the
complete producer format, generated example and precise Task 07 receiving work.
Task 07 was held for this delivery and has not been started here. Its receiving
path must consume the watcher template and preserve pair provenance in Run-owned
SQL and the review manifest; the old pending inspector currently rejects the new
JSON artifact. No pipeline/schema implementation, live watcher startup, production
capture processing, production DB write, commit or push was performed. Existing
unrelated working-tree changes were preserved.

## Task 06 v45 integration complete; Task 07 next — 2026-09-28

Task 06 has integrated and selected learner v45 package
`68f1ae5db205ab46afef9c4d`, model `f5cde2616f35d563118d3d32`:
model schema 5 / matcher API v2, `error-contract-v1`, SQLite schema 1.
The normal source catalog and installed wheel now use the same package.
The existing SQL design stores the new literal choices correctly; no pipeline
source edit, extra processing stage or physical database migration was needed.

Seven complete native logs passed preparation, aggregation, SQLite write/readback,
review completion and separate-process database-only rendering:
418,168 recovered occurrences,
19,912 unique records and four native review emissions.
All original 122 cases / 9,153 emissions are record-eligible. Both line-label
choices retain their exact native spelling. Duplicate rejection, generation
isolation and actual read-only SQLite failure preserve accepted state.
The installed whole-log storage path also passed with checkout resources blocked.
See [the v45 integration handoff](TASK06_V45_STORAGE_INTEGRATION_HANDOFF.md)
for exact evidence, storage mappings, changed paths and remaining limits.

The learner assessment's remaining word-run policy issues, two lost matches
against the thirty-log predecessor, capture regressions and tie behavior remain
documented; storage does not reinterpret those outcomes. Development selection
is updated, while production processing and existing application providers remain
unchanged. Next is Task 07 protected-input/processing/replay composition, followed
by Task 08 SQL-only reporting/audit. The historical learner/research retirement
dependencies in the Task 05/06 handoffs remain. No production database writes,
watcher/capture operation, retained-input deletion, commit or push occurred.

The dated selection and "integration pending" statements below retain their
historical context and are superseded by this checkpoint.


## Learner v45 release delivered; Task 06 integration separate — 2026-09-28

The owner authorized the demonstrated additive applicability fix, a replacement
over the complete retained 73-log corpus in cumulative 20 + 20 + 20 + 13 batches,
native before/after assessment and immutable schema-5 / matcher-API-v2 delivery.
That replacement is package `68f1ae5db205ab46afef9c4d`, published model
`f5cde2616f35d563118d3d32`, from candidate `c4f174d947fbc531aba35fb7`.
Manifest SHA-256:
`2a84fe9c734a558e757df54649eac0812ea380a80ac8a2d0fe17129d50f24a5f`.
Task 06 integration and active selection remain separate. Earlier no-publication
statements describe earlier scope, not this delivery assignment.

Learner v45 extracts the existing source/context/construction/parameter applicability
gates into the shared matcher and uses them before additive wording protection.
Refinement partitions use complete retained matches. The same-structure wording
rules are unchanged. Native retained decisions demonstrate that the one-frame
comparison proposal survives while the travel/activity policy conflicts remain.
Fresh state and exact provenance are under
`.codex-tmp/learner-release-v45/`; this is a new build, not an import of v43/v44
learned definitions. Learner SHA-256:
`025c98f6ca84cab8b6ea3b81e76f9517d166ee2090a81ed4878313122ae6a088`.

The final model has 689 definitions (492 supported / 197 provisional), assigning
2,439,711 occurrences as template and 154,873 as provisional, with four unmatched.
It gains 43,624 complete assignments versus the prior 73-log additive build with
no additional lost matches. Versus the selected thirty-log model it gains 119,114
and loses two. All original 122 cases / 9,153 occurrences match through 28
definitions: 118 bodies / 267 occurrences template; four / 8,886 provisional.

The [release assessment](LEARNER_RELEASE_V45_RESULTS.md) records native examples,
28 contextual inputs / 63 occurrences with changed captures versus the prior
73-log build, four remaining wording-policy conflicts, grouping regressions and
representation-sensitive ties. Within v45, all earlier supported definitions
survive, 30 promote and 50 retire with recorded successors/reasons. No prior
match becomes unmatched, but competing complete assignments make 21 previously
supported occurrences provisional at the 60-log checkpoint. Coverage gains do
not establish uniform semantic improvement or model acceptance.

The [pipeline handoff](LEARNER_PARSER_PIPELINE_HANDOFF.md) supplies exact parser,
matcher/validator/selector identities, callable interfaces, native export evidence
and schema-5 literal-choice requirements. Proposed selection is
`models/candidates/selection.v45.proposed.json`; read-only catalog loading resolves
it successfully. Active package `44a0401b8adf0a2953d26705` remains unchanged.
Next: Task 06 isolated integration of this explicit package, including choice
indices in storage/rendering, both statuses and native review associations, before
separate selection/cutover. Production processing remains disabled. No commit/push.

The independent immutable-package replay completed all 73 original logs without
development imports: zero discrepancies against 91,925 complete build inspection
results, 10,285,082 capture-byte checks and every original 122-case ordinal
reconciled. Exact results are in
`.codex-tmp/learner-release-v45/delivery-replay.json`; native examples and public
case results are alongside it. Active selection and all frozen source/package
hashes were reverified. This delivery makes no universal accuracy or performance
improvement claim; remaining policy/capture issues stay explicit in the assessment.

## Formal Pipeline Team reply: original unmatched shard — 2026-09-28

The owner requested closure against the original 122-case / 9,153-emission task.
[Formal reply](LEARNER_TASK06_UNMATCHED_REVIEW_REPLY.md): investigation and
candidate-level coverage are resolved; production deployment is not performed.
Fresh whole-original-log replay of current v44 additive candidate
`39cb19ab0ea10a48ebb98a46` and fresh candidate `6afef6948c1535e6d96126f5`
gives 114 template / 8 provisional cases, weighted 263 / 8,890 emissions, zero
no-match, using 28 definitions. Every original case/ordinal association reconciles.
The actually selected package remains `44a0401b8adf0a2953d26705` and still gives
the original 9,153 no-matches. Do not describe this reply as a deployed fix.
The reply links the historical causes, current before/after ledger, two worked
cases, multi-log answer and remaining out-of-scope learner limitations.
No publication, selection change, production processing, commit or push.

## Line-label equivalence implementation — 2026-09-28

Owner challenged the initial report's reliance on agent-chosen checks. The report
now leads with a procedure-matched v43/v44 audit, native examples, complete template
ledgers and additive evolution. There is no observed native coverage gain or loss:
fresh builds both have 203 templates; additive builds both have 208. All paired
definitions preserve memberships, support and capture behavior apart from the
declared label alternatives. Fresh-versus-additive differences affect 116 native
occurrences in four families, including one supported-versus-provisional difference;
these predate v44. Passing implementation checks is not owner acceptance. No
learner/runtime code was changed during this report audit. See the report for
concrete evidence/limits.

Owner authorized interchangeability of `line:` and `near line:` before LOCATOR.
Learner v44 represents these as declared literal alternatives in one template,
including from one native observation. Model schema 5 / matcher API v2 carry the
selected literal choice through exact rendering and identity; opaque fields,
source/context checks, complete assignment and support thresholds remain in force.
File-label policy is unchanged. Fresh same-version learning state is required.
See [implementation and verification](LEARNER_LOCATION_LABEL_EQUIVALENCE_RESULTS.md).
All 19 focused/native regression checks pass. The isolated two-log candidate
`6afef6948c1535e6d96126f5` accounts for 100,621 recovered occurrences; explicit
spelling-swap controls preserve template identity across 100 selected definitions.
Learner SHA-256: `2988d6fb02b51f4226fd6e025a21496062a518227f81607c4f45cc72fa1313cf`.
This does not fix the separate additive applicability defect recorded below.
No package publication, active selection change or production processing.

## Learner same-version additive exercise — 2026-09-27

Owner directs batches of 10–20 complete logs, retaining supported templates with
complete unambiguous assignments and refining cumulative provisional/unmatched
evidence. Do not tune inference from the 73-log run's behavior. The all-at-once
v42 attempt was stopped with its partial timing/recovery evidence retained;
the fresh thirty-log baseline completed. The v43 experiment completed
20 + 20 + 20 + 13 native logs and one cumulative successor model per checkpoint.
See [the experiment report](LEARNER_ALL_LOGS_V42_RESULTS.md), ignored
`.codex-tmp/learner-all-logs-v42/additive/` and `additive.log` for results.

v43 adds same-identity continuation, explicit provisional promotion/retirement
history, protection of provisional literal wording, and streamed native-evidence
serialization. The owner confirmed separate complete untyped effect/trigger
Unknown-location constructions, with opaque REASON and literal Unknown. Different
slot values count as distinct examples; repeated bodies do not. Each recognized
field contributes one typed similarity position, never its internal words.
No unchanged-evidence shortcut remains. Eight native additive and four date checks
pass. Frozen learner SHA-256 is
`8a1d1b067008a3d776b4496209e4b36c6bb7523923b28a7081be8deae216cbcc`.

The prior date-build issues are resolved: balanced-pair metadata uses lists, and
learner-only inference_rule metadata is excluded from executable field identity.
Final candidate `28cac50bf1249077100d12d5` has 492 supported / 199 provisional
definitions and matches all original 122 review cases. Its overall 73-log outcomes
are 2,396,084 supported, 154,876 provisional and 43,628 unmatched occurrences.
Those unmatched occurrences are eight bodies; the largest family demonstrates an
additive-guard applicability defect (one-frame proposals judged against four-frame
reference structures despite complete-matcher incompatibility). The other two
families expose incidental-value wording protection. Do not promote this candidate
or tune rules to its coverage. The report records targeted follow-up recommendations
and native proof; no inference changes were made during the frozen experiment.

All previous supported definitions survived; 30 provisional definitions promoted
and 53 fixed observations retired with successors. No previously matched training
evidence became unmatched within the same-version chain. The final comparison,
checkpoint audit and rejection traces are complete in the ignored directory.
The native-evidence inspector now reads ordinary JSON independently of indentation,
verified against both compact and indented complete exports; learner identity is
unchanged by this viewer correction.

No selected package, production state or existing research evidence was changed;
no commit, push, watcher or publication. Earlier dated sections remain historical.

## Learner date-token inference — 2026-09-27

Owner requires native dates such as `1178.10.1` to be KEYs, never diagnostic
wording, without waiting for variation in sampled values. Learner v42 adds the
declaration in `owner_rules.json`, recognizes the existing complete parser token
before grouping/alignment, and preserves it as KEY during field coalescing.
Selection evidence recognizes that declared field even with one observed value;
template support rules are unchanged. Opaque fields remain intact. The owner's
possible long evaluation interval is an explanation to consider, not an established
game behavior or a rule prerequisite.

Verification and native inputs are under `.codex-tmp/learner-date-key/`; the
requirement checks are `tests/test_learner_date_requirements.py`. No package,
active selection, parser, production state or existing research artifact was
changed. The previously reported in-memory balance-pair validation defect is
separate and remains unresolved; no full model build/publication was attempted.

## Task 06 completed; Task 07 is next — 2026-09-27

Task 06 delivers exact-identity aggregation, current-generation SQLite Run storage,
and the native review log plus manifest for every successful Run, including zero
review. Template and provisional records remain filterable and render from stored
definitions/values. `write_run` owns staging, finalization, publication, rollback and
commit; Tasks 07/08 consume its [public APIs and detailed handoff](TASK06_RUN_STORAGE_AND_NATIVE_REVIEW_HANDOFF.md).

Three complete unmodified Task 05 inventory logs were verified in fresh ignored
generations: 199,545 recovered occurrences, 190,392 eligible occurrences, 9,396
aggregated records and 9,153 native review emissions. Verification covers exact
bytes/order/frequency, both empty-shard files, duplicate rejection, namespaces,
Run IDs/date basis, count reconciliation, real read-only SQLite rejection and
separate-process database-only rendering. The detailed handoff distinguishes
observed failures from unexercised crash/native branches and records scope proof.

Next: Task 07 protected-input preparation and processing/replay composition;
Task 08 database-only reporting/audit. Operator command choices remain for Task 07
owner review. Existing application providers remain connected until separately
commissioned cutover. Production processing remains disabled. No watcher operation,
live capture, production database write, retained-input deletion, commit or push.

Task 05's named retirement dependencies remain: the historical baseline in
`tools/template_learning/build_parser_comparison.py`, the removed-API consumer
in `inspect_cross_emission_recovery.py`, and opt-in
`test_raw_parser_requirements.py::test_independent_pipeline_replay`. Learner/model
coverage limitations remain unchanged; storage does not repair unmatched or
malformed native patterns. The current selection/package is unchanged.

All dated instructions and task orders below are historical where superseded by
this checkpoint, the approved Error Contract and the Task 06 handoff.


## Task 05 completed; storage is next — 2026-09-27

Task 05 is complete: the selected schema-2 package is
`44a0401b8adf0a2953d26705` (unchanged model `76630685c4a341ca14bf9c7c`).
The pipeline now executes pinned recovery and shared complete selection, binds
only selected regions once, and prepares serializable `error-contract-v1` data
with exact identity and standalone rendering. The duplicate pipeline matcher and
its bound-candidate alternatives are removed. All 31 native inventory logs and
the disposable installed path passed; see
[the implementation handoff](TASK05_ERROR_CONTRACT_IMPLEMENTATION_HANDOFF.md)
for APIs, resources, evidence, coverage limits and exact changes.

Next: Run aggregation, SQL/native-review persistence and stored reporting;
application/provider cutover remains separately commissioned. Historical
recovery/view retirement still depends on the learner comparison tool's old
baseline. Two additional research/test consumers of removed APIs are named in
the handoff. Production processing remains disabled; no watcher operation,
learner publication, commit or push occurred. Earlier sections below describe
historical checkpoints and do not supersede this completion.

## Next implementation: revised Task 05 — 2026-09-27

The owner assigned the verified shared matcher integration to
[Task 05](05_ERROR_CONTRACT_IMPLEMENTATION.md). Execute its ordered steps:
load the pinned package; replace local matching and bind only the selected result
once; implement Error Contract preparation/identity/rendering; verify complete
native inputs; then select the package and verify installed resources.
Delete the superseded pipeline matcher and its unused result machinery.
The earlier Task 05 review hold is superseded for this defined scope.

[Independent pipeline verification](SHARED_MATCHER_PIPELINE_VERIFICATION.md)
passed across 31 logs / 1,167,165 occurrences, including every selected capture's
original-byte check. Candidate `44a0401b8adf0a2953d26705` is ready for integration;
selection remains unchanged in this prompt-revision pass. No source, package or
model implementation was changed. SQL/review persistence and application cutover
remain later. Historical recovery/view retirement still requires retiring the
learner comparison tool's old-baseline path; carry that dependency forward.

The delivery and earlier checkpoints below retain their dated evidence. Use this
section and the revised prompt for current execution scope and order.

## Shared matcher candidate delivered — 2026-09-27

Owner-directed learner extraction is complete. Candidate package
`models/candidates/44a0401b8adf0a2953d26705/`, manifest
`2a768c9d9729025da2874671dfc5952b703019f57a36a68e8437e1242122aca1`, supplies
`ck3-native-matcher-v1` with the unchanged schema-4 model
`76630685c4a341ca14bf9c7c`, parser v1.7 and assignment policy v2. The old release
and active `models/selection.json` remain byte-identical. Proposed metadata is
`models/candidates/selection.proposed.json`; it is not activation.

Fresh before/after learner and independent package replay agree on all 31
complete logs: 1,167,165 diagnostics, 78,869 distinct complete inputs within logs,
712,271 template / 445,741 provisional / 9,153 no-match. All nine slot types,
present empty versus absent, wrappers and 11 groups/13 entries are exercised.
4,447,658 present captures and 59,054 absences retain exact original bytes.
Unpublished-model parity also passes. New layout indices are the sole additive
legacy-result difference; no definitions, IDs, support or policy were changed.

Matching bodies are extracted into `matching_primitives.py`; learner callers,
evaluation and publication use the shared mechanics. `native_matching.py`,
`matching_validation.py` and `matcher_loader.py` provide the standalone contract.
Publication now creates immutable packages. Full-ID dependencies are hashed.
Research assignment review no longer imports the pipeline matcher. Generated
evidence is ignored under `.codex-tmp/shared-matcher/`.

Next owner: pipeline team. Implement package/selection reading, call the shared
entry point, bind only the selected assignment once, preserve final status and
layout references, verify on native logs, then retire its duplicate matcher.
Pipeline source, active/wheel selection, SQL and production operation were not
changed. Pre-existing product/pipeline documentation edits are preserved; no
commit/push was requested. See the [formal delivery and exact invocation](LEARNER_PARSER_PIPELINE_HANDOFF.md)
and [API/error/offset contract](SHARED_MATCHER_API.md). Ties, capture ambiguity,
alternative component layouts, >2 entries and malformed/failure paths have no
genuine witnesses in this corpus and remain explicit verification limits.

## Historical Task 04 closeout before audit/shared-matcher review — 2026-09-27

Owner approved the [full Error Contract](ERROR_CONTRACT_SPECIFICATION.md), including
source/emitter stored with the template definition and exposed through each record.
[Task 04 completion handoff](TASK04_ERROR_CONTRACT_HANDOFF.md) supplies the current
pin/interfaces, native checks, coverage limits and exact continuation point.
At this checkpoint the owner commissioned [Task 04(B)](04B_PIPELINE_PROCESSING_AUDIT.md)
before deciding repairs or Task 05 amendments. That audit, subsequent review and
shared-matcher delivery are now complete. The current scope at the top of this
document supersedes the original hold and bounded-local-matcher repair proposal.
The historical recovery/view retirement dependency remains separate.

The learner assignment dependency is resolved in selected model
76630685c4a341ca14bf9c7c, schema 4 / parser v1.7 / assignment-v2 / classifier-v7.
Both full and provisional outcomes expose one selected complete assignment.
Fresh Task 04 replay: 100,621 results on two complete logs, 173,247 present bindings
checked against source bytes, 4,350 absences, 11 groups / 13 supporting entries.
No SQL persistence or application cutover was performed.

This closeout adds the approved specification, completion handoff and revised
prompt, and reconciles active guidance. Code, models, learner files and protected
evidence remain unchanged. Pre-existing LEARNER_PIPELINE_MATCHING_INVESTIGATION_PROMPT.md
is preserved. Task 04(B) was the next step at that checkpoint. Run aggregation,
SQL/review publication and stored reporting
remain later implementation work. No commit or push is part of this closeout.

## Published: continuation-aware learner v41 and parser v1.7

2026-09-26. Owner authorized completing continuation support then publishing.
Selected release **76630685c4a341ca14bf9c7c**, manifest
`364215904d0b167b94365cb6b666818db15cc1947778acf6511772b9e12943c0`.
Model schema4 / featurev4 / assignment-v2 / classifier-v7. Parser v1.7 bytes
unchanged. models/selection.json and wheel data paths reference this release.

One complete learning record contains an opening and its ordered supporting title
entries. Owner JSON declares the component reference/value types; opening wording
is inferred. CHARACTER_FULL_ID remains opaque and each displayed title is PARAM.
Hash-covered continuations.py validates every entry against the selected opening;
assignment.py selects one complete supported/provisional result. Runtime model
reader, selector, matcher and absolute bindings are implemented. Callers use
NativeClassification.selected/template_id/bindings while preserving outcome;
each entry is a continuation:N region with its own original source span.

Same thirty complete logs: 418 templates (232 supported /186 provisional),
1,143,053 diagnostics (697,671 full /445,382 provisional /zero unknown).
All 1,143,044 unaffected occurrences retain v40 assignments/captures. Twenty
old separate messages become nine complete groups with eleven entries; seven
old opening/title formulations become one contract. Full runtime replay matches
all learner results; 4,429,930 native bindings checked. Final model also matches
both groups in the additional affected log outside training. That log retains
9,153 unrelated unknowns (v40 had9,155, including the separate title entries).

See LEARNER_CONTINUATION_MODEL_STATUS.md and the UPDATED EXISTING formal handoff
LEARNER_PARSER_PIPELINE_HANDOFF.md. Native report/evidence is ignored under
continuations-v41/. No synthetic logs or production ingestion. Application/SQL
caller adoption remains pipeline work, as do unrelated unseen-message coverage
and previously documented inference limitations.

Git checkpoint requested by owner remains separately unresolved at last check:
HEAD1af79a4, old weekly changes staged. User's helper output stopped in the diff
pager; advised q and disabled pagination for later helper executions. Do not
claim a commit/push without verifying HEAD/remote. New v41 edits were not staged
by this task, preserving the owner's earlier checkpoint snapshot.

## Current learner correction: symbol-wording loss across slot types, v40

2026-09-26. Owner authorized extending the retained CK3 symbol-type loss check
from PARAM to KEY/OPTIONAL_KEY/PARAM. Implemented in owner_rules.json and the
existing diagnostic_wording.py guard; whole raw-token matching and exclusion of
existing captured contents remain intact. Default literals stay disabled.

The direct extension incorrectly blocked quoted event scope values, losing 317
supported assignments on ten logs. Corrected using the existing enclosing-pair
mechanism and native variation: the new KEY/OPTIONAL_KEY guard permits a field
with two distinct nonempty values and matching enclosure on every native member.
This evidence exception is declared in JSON, records its evidence, does not
alter ordinary OPTIONAL_KEY typing or PARAM protection, and has no word/emitter
exceptions. Symbol words such as trigger/effect remain protected in diagnostic
wording; quoted army/character values remain variable.

Final same-ten/thirty builds with parser1.6: 292/424 templates; 291,456/697,680
supported and 60,861/445,384 provisional assignments; zero unknown. Every selected
template/capture/outcome agrees with v39, and native-evidence exports have the
same hashes. Both corpora show six direct symbol-loss rejections and one
positive-field-evidence allowance. No new classification gain is claimed: v39's
general wording check already prevented these bad proposals. Ten-log compact
export replay and thirty-log complete capture/layout comparison passed.

Research revisions 0fee46ee8d04f9a7d3ef9386 / 56a5ae97d60f780bad24c28e;
production pin unchanged. See LEARNER_SYMBOL_SLOT_LOSS_V40.md and ignored
symbol-slot-loss-v40/bounded/ for evidence. The populated-KEY agreement bonus
remains research-only (zero observed benefit); adjective-specific resistance
remains unimplemented (tested losses already blocked, no validated added value).
No runtime NLP dependency or repeated/coverage-driven regrouping was restored.

## Follow-up experiments: KEY agreement and negative adjectives

2026-09-26. Owner proposed treating corresponding populated KEYs as one-word
agreement and revisiting negative-adjective resistance outside enclosures.
Research only: production v39 code/owner JSON unchanged. Same ten-log paired-KEY
trial yields zero selected-template/capture/outcome changes across 352,317
occurrences; final comparison already scores 1.0 with supported fields excluded.
OPTIONAL_KEY absence stays neutral. The earlier presence-only variant likewise
had no assignment effect but penalized optional absence, and is superseded.

Native thirty-log evidence review shows an adjective loss flag would catch
Malformed/Unexpected becoming KEY in the unguarded trial: 4,160 occurrences.
Current v39 wording guard already prevents these. Earlier v36 adjective trial
only covered loss into PARAM, so it did not test this KEY failure. Recommend
explicit, contextual negative evidence rather than default literals or a new
unvalidated numeric weight. Existing PARAM/REASON/LOCATOR contents remain opaque;
adjectives alone cannot protect the lost trigger/effect words when Unknown stays.
See LEARNER_KEY_STRUCTURE_ADJECTIVE_REVIEW.md and ignored key-word-evidence-v39/.

## Current review: accepted-field comparison and single-sweep evidence, v39

2026-09-26. Fixed post-inference similarity counting accepted KEY values as
diagnostic words. Every accepted slot is now opaque to comparison; inferred
group retrieval uses the same view. The first native check exposed a narrower
wording-loss safeguard gap; the revised check prevents any part of an already
supported multi-word literal run becoming KEY content. No vocabulary/default
literals or example-specific exceptions were added.

Same ten/thirty native builds with parser1.6: 292/424 candidates; full assignments
291,456/697,680; provisional 60,861/445,384; unknown zero. Corrected canary and
rhomaios share `Unrecognized loc key <KEY>. <KEY>`. Independently established
Unknown/Unexpected/Malformed wording survives. New generalizations involving
quoted title names and travel receiver names still have KEY-splitting limits.
Models e17e0e907a97e4e58fc7c468 / cd5e492ff4f1b9ec5a071d4e are research only;
production pin is unchanged.

Owner then requested proof of the remaining consolidation pass. Native ten-log
ablation bypasses only the single original-group sweep; 357 candidates without
it versus 292 with it, 8,853 provisional-to-supported occurrences, unknown zero
in both. Actual entering groups/native examples show compound localization
fields, absent/present key fields, quoted variable-length strings and event
scope variants benefiting. This does not establish every merge as correct.
The repeated loop and coverage-only absorption remain expunged; one sweep still
exists, which is regrouping and should be described candidly as such.

See LEARNER_DIAGNOSTIC_COMPARISON_V39.md and LEARNER_SINGLE_SWEEP_NATIVE_REVIEW.md.
Artifacts: `.codex-tmp/learner-refactor/diagnostic-wording-v39/guarded/`, including
review-10, review-30, and sweep-review-10. No pipeline source or SQL changes.

## Delivered for review: adjective removal and single assignment, v37/v38

2026-09-26. Owner clarified the suspected no-match count came from another file,
then authorized retirement/winner implementation and a native sample report.
The adjective/error-word vocabulary, loader and optional NLTK dependency are
removed; survey/ablation tools moved out of the production package into ignored
research archives. v37 ten/thirty native templates and assignments are identical
to v36. A misleading research unmatched flag was corrected separately.

v38 implements exact fixed-KEY specialization retirement, independent support
excluding declared traces/locations, and a standalone hash-covered selector.
Ten logs: 37 retirements, 355 templates, 290,694 full / 61,623 provisional.
Thirty logs: 100 retirements, 500 templates, 696,216 full / 446,848 provisional.
Unknown zero in both. Every eligible message gets one selected assignment;
four ten-log occurrences require an honest provisional tie-break. Thirty-log
106,869 competing occurrences resolve; 1,119 lose unsupported trace-only status.

All 7,864 / 38,621 contextual rows replayed with the existing runtime matcher
plus the frozen selector, exact body/wrapper reconstruction and candidate-order
independence. No synthetic messages. Same parser v1.6 used to isolate this change.
Evidence/reviews: `.codex-tmp/learner-refactor/single-assignment-v38/review-30/REVIEW.html`
and review-10. Twenty-five distinct native examples, before templates, after
winner, actual captures and provenance. See LEARNER_SINGLE_ASSIGNMENT_IMPLEMENTATION.md.

Candidate revisions 71adca09f2d7551287987976 / 8c188491a07bba594efa4159. Not published
or pinned. The existing formal handoff contains the new selector interface and
explicit pipeline adapter requirements; pipeline code/SQL were not modified.
Existing UI-format KEY typing and anomalous-brace binding remain separate gaps.
The separately delivered parser-v1.7 continuation integration remains outstanding.

## Historical v36 checkpoint: adjective trial and brace-boundary inspection

2026-09-26, v36 research only. Fresh same-ten/thirty complete-log comparison of
current error words, no error words and eleven adjective additions yields
identical templates and every saved assignment/capture. CK3 reference unchanged;
default literals disabled. Baselines exactly reproduce preceding v36 templates
and summaries. Recommend leaving adjective additions inactive. Native research
tool: tools/template_learning/compare_adjective_guidance.py; complete evidence:
.codex-tmp/learner-refactor/adjective-ablation-v36/REVIEW.md.

Brace boundary inspection verifies two separate `}` values in the canonical
OPTIONAL_KEY fields; literal `: ` remains between them. Among 1,306 native rows,
zero ambiguous boundary assignments; only this one row / three occurrences has
invalid identifier values. Proposed unsupported-syntax binding is not yet a
runtime/model feature. See LEARNER_BRACE_CANDIDATE_INVESTIGATION.md.

Redundant fixed-value template retirement remains unimplemented. Concrete
criteria recorded in LEARNER_SINGLE_ASSIGNMENT_REVIEW.md: preserve unchanged,
independently supported fields, require corresponding diagnostic structure,
retain evidence but retire redundant competitors. This is not restoration of
coverage-driven absorption. Both scope:recipient competitors currently carry
supported status; provisional-only pruning would miss them. Production winner
selection remains separate. No model publication or pin change in this trial.

## Historical checkpoint after v35 review — v36 development

Owner asked whether coverage merging should have been removed and directed
expunging regrouping rather than a disable switch. The existing proposal does
explicitly require deleting coverage-driven absorption and both calls; that
function/calls are now deleted. Clarification pending: does “regrouping” mean the
repeated loop already deleted, or the entire one-sweep stage? Do not silently
claim all consolidation is gone. Fresh native comparison of coverage deletion is complete with the single sweep
retained: v36 thirty-log candidate e63bc6c6f15f79d36ae234a1 has 600 templates,
590,466 full / 552,598 provisional occurrences. All 106,869 changed occurrences
retain old matches and gain competitors. Both routes agree on all affected rows;
63 missing-parent and 13 title matches remain correct. Candidate is not published.
See .codex-tmp/learner-refactor/no-coverage-v36/REVIEW.html and the v35–v36 ledger.
The completed v35 measurements below remain a prior checkpoint, not v36 results.
Concurrent edits to records.py / incremental_template_registry.py added deferred
continuation bookkeeping after those builds; preserve them and use fresh source
identity for the next build.


## Historical learner update — v35, 2026-09-26

Owner authorized implementation of the single-sweep recommendation and discussed
improvements. Source now has one original-group region-consolidation sweep,
retains the v34 missing-parent guard, and declares TITLE_FULL_ID in the existing
owner JSON with shared learner/runtime recognition. Raw parser and production
model pins are unchanged. Native 73-log recognition audit passed: 85 title,
3,666 character, 12 house captures; three truncated markers remain uncertain.
Same ten/thirty fresh builds are complete: candidates fbb8d94f894456ebe470c695
and 753006dab4348ab5c6601afd. v35 changes 18 thirty-log assignments: 13 complete
title fields plus the five expected effects of removing repeated reopening.
All 63 missing-parent cases remain correct; production pin unchanged. Detailed
validation and remaining steps are tracked in
[LEARNER_V35_IMPLEMENTATION.md](LEARNER_V35_IMPLEMENTATION.md). Generated evidence:
`.codex-tmp/learner-refactor/single-sweep-v35/`. The v34 review now labels its off
arm “No region regrouping”; it never discarded those messages.


Updated: 2026-09-26

## Delivered: simplified cross-header continuation parser v1.7

Learner-team continuation is now written in the existing formal handoff under
[Learner team handoff: adopt v1.7 and complete grouped-error support](LEARNER_PARSER_PIPELINE_HANDOFF.md#learner-team-handoff-adopt-v17-and-complete-grouped-error-support).
It specifies exact prefix semantics, the current deferred-evidence fields,
consumer APIs, remaining model/runtime work, parser repinning and native evidence.

Owner reviewed the proposal, rejected the character-recognizer dependency and
authorized simplification and republication. See
[the delivery ledger](LEARNER_CHARACTER_TITLE_CONTINUATION_STATUS.md) and existing
formal pipeline handoff. Published `parsers/v1_7/manifest.json`, version
ck3-lossless-v1.7, parser SHA-256
`a8005254df58daf20e000e454c9e3e9b40304be4cd0962e1fa88e90cea86baab`.

Emitter/colon opening plus adjacent entry framing and opaque prefix equality;
no character recognition or fixed failure sentence. Both consumers use the shared
log-level stream. All 73 complete inputs passed: 11 groups, 13 entries, 2,594,588
messages, exact reconstruction, no parser unresolved outcomes and unchanged
unaffected recovery/lexical boundaries. Nine existing native/parser checks, both
complete affected-log consumer replays, binding/debug/feature checks and wheel/
independent-import checks passed. Evidence is under
`.codex-tmp/character-title-continuation-review/v1_7/`.

Feature v3 retains complete groups in unresolved review evidence with
recovery_status=recovered; classifier v6 returns one unknown group. No opener-only
matching or independent title-line learning. The learner must supply a repeated-
component model and a new immutable v1.7 pin for full classification. Current model
selection stays on v1.6. No inference, training, production or SQL changes in this
task. Preserve concurrent learner work.

## Active: all-source regrouping comparison complete; owner review (v34)

Owner's full-ID review requested concrete missing-parent examples and a repair
before the next outstanding item, then explicitly prioritized proving the value
or harm of regrouping across the complete corpus. Read
docs/LEARNER_FULL_ID_FOLLOWUP.md. v34 adds a general merge-only guard against
replacing an independently established word sequence with adjacent KEY slots;
no failure phrases are hardcoded. Fresh ten-log candidate
cd757f4a20bd6e9549bff77a corrects all 63 affected parent messages, with no other
assignment changes or outcome changes. Same-thirty candidate
2b3c6d09c3b753b10cfaa417 also changes only those 63 assignments; all 63 now have
one identical runtime/learner match. No other outcome changes.

Research scripts in .codex-tmp/learner-refactor/full-id-followup-v34/ compare
region regrouping disabled, one original-group sweep, and the ordinary repeated
loop on all 113 sources in the same thirty complete logs. Results respectively:
537/458/456 templates; 674619/697334/697337 full outcomes, zero unknown. One sweep
has concrete native benefits; repetition changes only five formatted script-effect
messages, adds three full outcomes and retains fragmented rich-text/name KEYs.
Recommendation: retain one sweep, remove repeated reopening. This recommendation
has NOT been implemented in the production loop. The readable REVIEW.html in
that directory includes all five repeat-only changes and five parent examples.
Event/List diagnostic category loss already occurs in one sweep and remains open.
The coverage-absorption
calls remain enabled and separately instrumented; do not describe this as all
merging disabled. Full-ID recognition is unchanged. Owner clarified that
`In history for` should remain diagnostic wording and `Lowborn of` is already
captured correctly. Populated Internal Key formatter also occurs for baronies,
duchies and kingdoms; TITLE_FULL_ID is proposed for review, not implemented.
No production model/parser pin or ingestion changes.

## Active: full-ID implementation and native validation complete; owner review

Owner approved implementation after the inventory, specifying variable-length
**name** (not description), lowercase connecting words accepted, and adding
HOUSE_FULL_ID. v33 implements two JSON-defined opaque field types using shared
full_ids.py in learner/runtime matching. Raw parser unchanged. Same ten-log build
58d4a838c87f78ab2dfa26c1 completed: 310 templates, 167 supported, 143 provisional;
290864 full / 61453 provisional / zero unknown. Active pipeline replay passed
all 352317 native occurrences with identical alternatives and exact captures.
Same-thirty build c5e23dbdc604f575dfd932b3 completed: 455 templates, 257 supported,
198 provisional; 697337 full / 445727 provisional / zero unknown. All 38621
contextual rows passed the exact full-ID capture and opaque-grouping audit.
Thirty-log active runtime replay passed all 1143064 messages with identical
outcomes, alternatives and captures; exact input reconstruction and capture bytes
also passed. Readable before/after review:
.codex-tmp/learner-refactor/full-ids-v33/REVIEW.html. Do not publish automatically:
the known Parent ((no character)) diagnostic still becomes three KEYs even though
the complete child reference is now correct. Its 61 provisional-to-full changes
are not demonstrated diagnostic-quality gains. Current production selection stays.

### Inventory history

Owner supplied a new structural-character-reference directive after reviewing
the enclosed-ID regression. Initial native inventory is complete; read
docs/LEARNER_CHARACTER_FULL_ID_STATUS.md and the ignored readable report at
.codex-tmp/learner-refactor/character-full-id-inventory/REVIEW.html.
73 complete logs, 6,726 messages, 7,768 Internal ID markers; all input hashes and
4,761 distinct native witness/piece sequences verified. Two character-form ID
endings observed; titles/houses/provinces explicitly excluded. Complete starts
need source/context declarations. No recognition/model/matcher changes made.
Owner follow-up simplifies recognition: all 7,414 character-form occurrences
have terminal `of`, then zero raw tokens (4,743) or one (2,671), then `(Internal
ID…)`. ID-parenthesis contents should remain opaque; do not validate historical
or internal values. Capitalization is not universal: four native Parent records
start `_name Tián`; known emitter boundaries handle that without a name rule.
The empty house key was not an exclusion reason: that example lacks the `of`
formulation and comes from a different emitter. Updated proposal and native
check are in the character status document / simplified-structure-check.json.
The review checkpoint above has now been approved for implementation. Do not add
the earlier field-retention workaround or a name recognizer. Production pins unchanged.
The prior five-source regrouping ablation completed with mixed benefits/harms;
its broader follow-up remains separate from this inventory checkpoint.

## Active: step 1 PARAM boundaries — pause after native review

Owner approved the consolidated work list sequentially, with a pause after each
step to inspect real performance. Step 1 only is implemented in v32; fresh native
10/30 builds completed. Read docs/LEARNER_PARAM_BOUNDARY_REVIEW.md.
Revisions: cf7ad19059eaa77eb5c7e0e7 (ten), 0deaa13fdfc7a7e27fdc13c1
(thirty). Owner then requested proof of repeated-regrouping benefits and closer
inspection of script-effect PARAM loss. Declared traces survive; two enclosed ID
fields in the ten-log comparison and thirteen parenthesized travel-debug fields
in thirty lose PARAM when rejecting another field partitions the whole pool.
Focused native ablation/audit is active in param-boundaries-v32/. No rescue or
field-retention change has been added. Do not treat step 1 as accepted yet.
Owner clarified during implementation: eliminate broken unmarked-PARAM logic;
do not try to rescue its prior assignments. The attempted replacement width
witness rule was withdrawn before a completed build and removed from source.
Only actual paired-enclosure discovery and existing owner-declared structures
can support PARAM now. Items 2 onward remain pending. Do not start them before
reporting this step and pausing. Production v29/parser v1.6 remain unchanged.

Current consolidated open-work list: docs/LEARNER_OUTSTANDING_WORK.md. It separates
the implemented v31 blocker/scoped survey from unimplemented PARAM/merge mechanics,
confirmed remaining defects, separate matching integration and deferred learning
work. Compiling this list did not change inference or the production pin.

## Active: diagnostic-wording loss blocker — 2026-09-25

Owner explicitly directed implementation of a simple listed-wording loss guard.
Learner v31 now checks established literal spans against proposed PARAM spans in
the consolidation/refinement/merge paths; matching words block the generalization.
Default literals remain disabled; existing slot interiors are excluded. JSON
records the narrow purpose and retained CK3 type/failure-word references. Read
docs/LEARNER_DIAGNOSTIC_WORDING_LOSS.md. The broader proposal below is still pending.

Native frozen-proposal checks completed (five rejected formulations; 896 unchanged
member checks with no loss flag; full controls cover all 7,827 native members).
Fresh ten-log build completed: one new provisional overlap, all other assignments
unchanged. Thirty-log build completed under .codex-tmp/learner-refactor/wording-loss-v31/:
416 templates; broad two-PARAM candidate gone; 22,574 key-reference ambiguities
resolved; 112 full-to-provisional changes (109 reduced support, three exposed
overlap occurrences). Read RUN_REVIEW.md there and the tracked review above.
Revisions: ten 8973261d53bac90dfc6d6f9f; thirty 8fc7bfaae87d27f911852f08.
No production repin. Owner also asked for language-library discovery of adjectives
from native logs. Owner installed NLTK 3.10.3 and its English tagger; installation
is verified and the complete thirty-log survey has now run.
Latest clarification: seek individual NEGATIVE adjectives inside literals or
possibly PARAMs; nothing inside LOCATORs should be evaluated. Corrected
survey_adjectives.py excludes LOCATOR contents before NLTK, tags contiguous
literal/PARAM regions separately and keeps their observations separate. It never
joined Malformed and token; the earlier table confusingly displayed native context.
The corrected full pass excludes 271,500 LOCATOR tokens; common disappears.
Review .codex-tmp/learner-refactor/adjective-review/NEGATIVE_ADJECTIVES.md and
negative-scoped-survey/. Older RECOMMENDATIONS.md is superseded; neutral-adjective
suggestions are withdrawn. Eleven negative-adjective additions are proposed, not
activated. Seventeen ambiguous rows are counted but not tagged; REASON and other
slot types are outside this survey. No blocker vocabulary or inference changes.

## Proposal awaiting owner review: PARAM context and merge mechanics — 2026-09-25

Owner supplied seven requirements and explicitly requested the revised triggers
and acceptance mechanics before implementation. Read
docs/LEARNER_PARAM_CONTEXT_PROPOSAL.md. This checkpoint changes documentation only;
no new learner run or source/model/parser/matcher changes have been made.
Persistent hypotheses remain deferred.

Owner further clarified discovery priority: explicitly demarcated regions first;
do not routinely seek unmarked PARAMs. The proposal now documents the one-sided
punctuation acceptance and coalescing loopholes, requires actual boundary evidence
through every path, and limits unmarked proposals to concrete native deficiencies
in independently supported formulations. Repeated wording is not PARAM evidence
or a reason to preserve a prior assignment. These are proposal updates only.
Further clarification: isolated colons and sentence-ending punctuation cannot
trigger PARAM hypotheses or supply positive evidence; they can be discovered as
endpoints through independent field evidence. Merges require matching diagnostic
wording and prefer formulations retaining more supported matching diagnostic
wording, not punctuation scores or broader capture coverage.
Enclosure discovery is explicitly prioritized: matched parentheses, square
brackets and braces first; paired single/double quotes are weaker secondary cues.
Colons are not opening/closing delimiter pairs. This remains proposal-only.

Audit confirms one-sided punctuation can currently qualify PARAM; location-label
words can affect similarity; coverage-based absorption runs twice and bypasses
the wording guard; paired PARAM boundaries also bypass part of that guard. The
proposal uses independent diagnostic wording outside all proposed/accepted fields,
joint context-dependency validation, evidence-triggered reconsideration and one
acceptance path across initial inference, coalescing and every merge. Exact
duplicate aggregation remains separate from generalization. Empirical wrapper
fields must retain owning-message context.

Current location-label handling emits separate exact variants, not general runtime
equivalence. The proposed required structural-label alternative must preserve
native spelling/spans and explicitly account for model/matcher interface changes;
do not silently normalize or claim the existing code already implements it.

## Completed: learner v30 isolation and 10/30 comparison; inference regressions found — 2026-09-25

Owner directed removal of all template importing, a registry per learner version,
fresh inference and research into genuine incremental learning. Removed confirmed
template seeding, the registry confirmation command and the bypass that excluded
already-matched messages from discovery. Each build now infers all templates from
selected native evidence. Registry schema 4 pins learner version/source hashes;
cache schema 4 carries the same identity. Default registry root includes it;
foreign roots and parser mismatches fail rather than migrate. No prior conclusions
are read. This remains cumulative batch learning, explicitly not online updating.

Ledger: docs/LEARNER_VERSION_ISOLATION_REVIEW.md. Evidence and live build logs:
.codex-tmp/learner-refactor/version-isolation-v30/. Fresh ten-log candidate
7885c36206ddaf31a7ec9a3b has 297 templates (165 supported,132 provisional), zero
imports and identical templates/support and all 7,864 contextual assignments to
v29. Thirty-log candidate 7278879bde9161fd798abc6d has 406 templates (243 supported,
163 provisional), 1,143,064 messages. Same-corpus comparison completed and exposed
regressions: `<PARAM>: <PARAM>, near line: <LOCATOR>` absorbs diagnostic wording,
overlaps the proper OPTIONAL_KEY contract (22,574 provisional occurrences), and
absorbs the brace anomaly into a supported generalization. A two-space texture
path observation broadens the LOCATOR field to PARAM. Do not promote this model.
New observations do improve some formulations, but full-match totals conceal
wrong captures. Full native before/after HTML, changes and exact assignments are
in the evidence directory. Native checks: 32 pass, one unexercised ambiguity check.
Native one-log registry build/cache equivalence completed. No synthetic emissions.
Production remains selected v29
0a61f6c93657948e0ca20b35; no publication, parser change, SQL or pipeline changes.

Earlier single-assignment examples were historical v16 competing candidates,
not current v29 competitors. The obsolete PARAM fallback competitor is absent
from v29/v30. The brace-only spelling is still freshly inferred as a provisional
singleton in the ten-log model; the thirty-log regrouping now undoes that isolation.
Malformed-value interpretation remains unimplemented. The prior
ranking proposals are not implemented and do not justify retaining known-bad
competitors. Current same-corpus replay evidence is the basis for the next review.

## Owner correction: exactly one provisional winner — 2026-09-25

The owner rejected abstention as a response to competing provisional matches.
Unknown is no eligible complete match; competition must return one selected
template and its complete bindings, still provisional. Updated the existing
single-assignment prompt/review and formal handoff to remove the contrary policy.
Recommendation: ordered comparisons of location preservation, opaque-region
boundaries, positive slot evidence, then distinct complete diagnostic support;
stable template/binding identity only for final ties. These are proposed metrics,
not production code or calibrated confidence. Runtime does not learn rankings.
Historical trace case now explicitly selects the candidate preserving all ten
LOCATORs over the candidate swallowing eight, while retaining its trace-literal
weakness for later learner correction. No policy/model publication in this turn.

## Single-assignment selection review — 2026-09-25

Owner requested best-practice recommendation and real multi-match examples,
not immediate policy implementation. Added LEARNER_SINGLE_ASSIGNMENT_REVIEW.md
and updated the existing prompt with current pin/status. Selected v29 unchanged.
Fresh current-matcher replay of 91937 saved complete contextual inputs from the
73-log audit found zero competing templates/capture ambiguities. Occurrences:
1359947 full,761401 unique provisional,473253 unknown (2594601 total). Rechecked
message/context bytes against original witnesses and all 73 complete log hashes.
This was replay of retained raw pieces, not a fresh tokenizer or retraining.

Four real historical provisional multi-matches from v16 were verified against
native bytes and current-parser/current-model execution: expression PARAM versus
memorized literal; key-reference KEY versus fallback PARAM; incompatible trace
interpretations; character-history naming overlap. Historical outputs are evidence
only, not authority to restore code. Recommended evidence-backed preference with
explicit unassigned outcomes, no raw-frequency/most-literal/type-order winner.
Incremental preference must not bootstrap confidence from its own disputed choice.
No exact score thresholds or new optional-key evidence restriction introduced.

Evidence: .codex-tmp/learner-refactor/single-assignment-review/ includes
current-replay.json, input-hashes.json, historical-cases.json and EXAMPLES.md.
The character-history witness still has `is <KEY> <KEY> <KEY>` for `is the wrong
gender`, despite now recognizing the outer parenthesized PARAM; noted as existing
semantic concern, not repaired or claimed caused by this review. No production
source/model/parser/SQL changes. Single-assignment implementation still pending.

## Published location-label correction — 2026-09-24

Owner authorized refreshed publication, pin and existing formal handoff update.
Selected release is now 0a61f6c93657948e0ca20b35; manifest SHA-256
a0b4624795819c60e21462bf066fc793440b1d3a67535e7531e04cdfdb16e197.
Candidate 9ee807faa3ab6531dd6036bf, learner v29, unchanged raw parser v1.6.
JSON location_label_equivalences plus generic candidate refinement preserve
observed Near file:/file: and near line:/line: wording as exact generated forms.
No template overwrites, input normalization or OPTIONAL_KEY restriction.
The rejected v28 candidate remains rejected and was never published.

Same ten native logs: 297 templates (165 supported,132 provisional). Exactly one
old template replaced by two supported forms: 959e7fc883d82201a278e344 (Near file)
and 1edb00c1404c4dd6db2527dc (file). Other 295 templates unchanged. Exactly 25
contextual rows /217 occurrences change assignment, no outcome changes. Both
genuine OPTIONAL_KEY fields unchanged. All 352317 messages pass independent
pipeline replay, full byte reconstruction and capture checks; additional native
tribute-mission trace/location witness still passes. Export replay 7864 contextual
rows;38311 inferred-member ranges checked. No other behavior changes found in
this comparison; no claim that finite-log parity establishes universal accuracy.

Evidence: .codex-tmp/learner-refactor/location-label-release/ contains command,
candidate, comparison/REVIEW.html, delta.json, REVIEW.md, published.json and
pipeline-replay.json. Existing LEARNER_PARSER_PIPELINE_HANDOFF.md updated; no new
formal handoff. models/selection.json and pyproject.toml pin new release. No
pipeline source edits, SQL, ingestion or watcher work. Single-assignment and
matcher-unification tasks are separate and not claimed delivered here.
Selected loader and wheel checks passed; all six release files and selection
in the wheel are byte-identical. Wheel SHA-256:
39262e2cf3a326d74a6a0f12edfba94ef7c1c7b5cf03130f9829e2be778fb9fb.
Verification saved as wheel-verification.json. MODEL-004 marked closed with
native evidence in src/ck3chronicle/pipeline/MODEL_BUGS.md.

## Owner correction: preserve OPTIONAL_KEY — 2026-09-24

Owner rejected the attempted minimum-two-present-values rule. OPTIONAL_KEY means
a key or absence; a single observed present spelling does not invalidate it.
The v28 experiment completed before the interruption was handled, but was never
published or selected. Its clustering.py and owner_rules.json changes have been
reverted; learner remains v27. The ignored near-literal-review/rebuild directory
is explicitly marked REJECTED.md and must not supply a future baseline/model.
This supersedes the optional-key evidence recommendation below. MODEL-004 remains
open: address location-label wording through the learner, without weakening
OPTIONAL_KEY or manually overwriting generated templates.

73-log label survey found 143966 occurrences of `near line:`, all followed by
numeric line/range values, and 1255 of `Near file:`, all followed by recognized
location values. These are label mentions counted with native occurrence weights,
not independent learning examples. Survey saved in
.codex-tmp/learner-refactor/near-literal-review/label-survey.json. No equivalence
or normalization rule has been implemented; preserve original wording/bytes.

Owner follow-up supports considering a contextual Near-file/file modification:
recognize equivalent location introducers immediately before a LOCATOR within
otherwise comparable complete messages. This must not impose variation among
present OPTIONAL_KEY values. Pending design: JSON-declared label equivalence,
original labels retained, ordinary exact template variants under current schema;
no new optional-literal representation or blanket Near word rule. Not implemented.

## Near OPTIONAL_KEY investigation — 2026-09-24

Owner requested why location wording Near becomes OPTIONAL_KEY and an explanation
of matching. Confirmed learner/model bug MODEL-004, added to MODEL_BUGS.md.
Selected release unchanged a9fa27a85ccd066285b99fdb. Affected template
1332e889d727946cb5b53eb4 merges complete Unrecognized loc key messages from the same
source family: nine Near-file messages / 90 occurrences, all cpp:57; sixteen
plain-file messages / 127 occurrences, all cpp:66. No cross-source/global
sub-phrase pool. _slot continuous-token branch treats Near plus absence as
OPTIONAL_KEY; the one-spelling optional-PARAM refinement does not apply to it.
Paths/lines already have correct LOCATOR boundaries.

73-log census: Near form 616 distinct /1255 occurrences, plain form 928/2737;
588 versus 817 different keys, none shared. Explicit investigative partition of
the 25 training members with unchanged inference produces separate fixed-wording
templates, all members match uniquely. No production partition/rule added.
Recommend two literal formulations; evaluate general OPTIONAL_KEY evidence
quality instead of a global Near literal or new locator boundary rule. Owner's
earlier instruction to separately review blanket one-spelling-plus-absence
splitting remains in force. Current other two OPTIONAL_KEY fields each have 31
present values. Evidence: .codex-tmp/learner-refactor/near-literal-review/REVIEW.md
and evidence.json. No learner/parser/pipeline/model changes or publication.

## P3 decisions; learner assignment prompt prepared — 2026-09-24

Owner clarified that diagnostic record means refined unique content stored in
SQL. Store template literals/slot placements and bindings; aggregate identical
matched content within each Run with occurrence counts. Source applicability is
handled in matching. Both template and provisional matches belong in SQL with
a filterable status; unmatched messages go to review. SQL needs no competing
template lists. Lineage is Run metadata; individual occurrence timestamps are
unnecessary. Storage consumes the assignment without rematching raw messages.

Current provisional outcomes conflate unique provisional-template matches and
ambiguous assignments. There is no ranked #1 policy. Owner assigned that problem
to the learner team; prepared [LEARNER_SINGLE_ASSIGNMENT_PROMPT.md](LEARNER_SINGLE_ASSIGNMENT_PROMPT.md)
with native audit, deterministic selection contract, consumer output and published
handoff requirements. The latest six-log replay observed no competing assignments;
the prompt does not claim an observed model collision. No message was sent to
another team and no learner/pipeline/model/SQL code changed. Next: learner response
and completion of P3 around the clarified storage rules and assignment interface.

## MODEL_BUGS current-status verification — 2026-09-24

Owner requested an evidence-backed check of every existing MODEL/P issue, not
another model change. Updated src/ck3chronicle/pipeline/MODEL_BUGS.md with the
current status table, per-issue findings and readable native witnesses; clearly
separated the original historical investigation and superseded statuses.

Selected model remains a9fa27a85ccd066285b99fdb. Fresh selected-pipeline replay:
2314 distinct native text/source witnesses from 37 hash-verified original logs,
selected from the 73-log census. MODEL-001: all 45 namespace messages (334 census
occurrences) fully match a whole KEY. MODEL-002: all 2048 duplicate-localization
messages (7860 occurrences) match KEY + LOCATORs. MODEL-003 loading/literal/tail/
TYPE fixes verified, including 208 former TYPE-family messages; its cited named
artifact holderplace / ID 100667378 remains unknown (no candidate; absent from
the ten training logs). Empty artifact case matches. Actual stress_impact/proud
pair now fully matches with intact REASON. P-01/P-02 superseded; P-03/P-05/P-06/
P-07 closed in selected path. P-08 offending source branch removed; no native
malformed-branch witness was invented. P-04 partly resolved: parser/rules shared
and pinned, matching code still separate; no drift found in current evidence.

Evidence: .codex-tmp/learner-refactor/model-bugs-audit/REVIEW.md,
native-replay.json, source-and-model-checks.json, named-artifact-coverage.json.
Every prior full ten-log replay pipeline hash and pinned learner hash is unchanged.
No source/model edits, retraining, synthetic messages, SQL or ingestion. Audit
process completed. This is an audit, not authorization to restore old architecture.

## Trace PARAM boundary correction published — 2026-09-24

Owner rejected extracting nested locations from oversized PARAMs and directed
fixing trace identification itself, rebuilding and publishing. Removed the
incorrect script-location-frames declaration; existing located-parenthetical
rule now yields `file: <LOCATOR> line: <LOCATOR> (<PARAM>)` per frame. No new
extraction API, schema, parser version, slot type or pipeline source change.

Selected immutable model a9fa27a85ccd066285b99fdb; manifest SHA-256
072e4af61179d8f853ddbd4f2a169e34c2f28ed26e0286a03941c3ce2755fbdb.
Candidate 762e1b8d5772b08ca08f1440, learner v27, same ten native logs, parser v1.6.
Selection and distribution packaging updated. Existing formal handoff has the
supplement. Prior releases remain immutable; no fallback or production activation.
Wheel built without dependency downloads; selection and all six release artifacts
verified byte-for-byte. Wheel SHA-256:
46ad2027e20bc003bae73203f15b333b62e81ecafbfcf1f8cad8b120de8f85b0.

296 patterns: 164 supported / 132 provisional. 290888 full / 61429 provisional /
zero unknown or ambiguous occurrences. 553 formerly full occurrences become
provisional across 36 patterns because only location variation remains; the
unchanged support policy excludes it. No other outcome regressions. Trace frame
counts now can produce separate flat templates; trace interior words do not.

73-log boundary audit: 15563 distinct changed messages / 1165336 occurrences,
zero recognized location/trace-PARAM overlaps. Same-ten comparison: 38336 member
ranges and 37456 captures agree. Independent pipeline replay of all 352317
native messages matches every expected outcome and capture (including 821250
LOCATOR captures), with exact log reconstruction and original-byte binding checks.
Owner's two-location native example is outside training: full match to
6a187968e94c36b0acd622d5, four LOCATORs / two PARAMs, exact bytes verified.

Evidence and readable review: .codex-tmp/learner-refactor/empirical-regions/
trace-boundary-review/. All learning and replay processes completed. The earlier
twenty-log v26 experiment remains unpublished; no further learner run is pending.
Remaining separate issues: location-only support policy, name recognition,
flat-template duplication across frame counts, and pipeline SQL/application work.

## P1 accepted and closed; bounded P2 verification — 2026-09-24

Owner accepted P1. Reloaded selected v3 model a9fa27a85ccd066285b99fdb with
manifest 072e4af61179d8f853ddbd4f2a169e34c2f28ed26e0286a03941c3ce2755fbdb
and the same pinned v1.6 parser. Existing reader/catalog/matcher/bindings consume
the corrected declarations without source changes. Error type remains unknown.

Refreshed report: [.ck3chronicle/wip/reports/p1-spot-check-a9fa27-20260924/index.html](../.ck3chronicle/wip/reports/p1-spot-check-a9fa27-20260924/index.html).
72 samples / 120 native examples. M01 displays the reviewed tribute-mission
message with four LOCATORs and two trace PARAMs. Three complete logs yield 33,489
full / 75,142 provisional / 1,139 unknown. Browser review and controls passed.

P2 additionally checked six complete native logs (one overlaps the report):
310,306 messages / 302,245 emissions; 140,985 full / 142,694 provisional /
26,627 unknown. All input bytes and occurrences accounted for; 1,082,002 present
captures agree with original bytes, 18,582 optional absences retained, 310,995
candidate regions reconstructed, 13,658 wrapped messages checked. Zero declaration
errors or unresolved parents. Five earlier REASON-boundary witnesses and the
55-frame trace remain ordinary unknown; the zero-parenthetical-trace example is
full. No synthetic evidence, substitute models or test-file requirements used.

Native competing assignments, recovery failures and accepted empty REASON
captures were not observed, so those branches remain coverage gaps. Installed
wheel execution and corrupt-input rejection were not tested in this closeout.
The supplied ten-log replay remains corroborating evidence: all eleven recorded
pipeline source hashes agree with this checkout. It was not rerun here.

P1 has no outstanding implementation item; bounded P2 replay is complete with
those stated limits. Next: P3 minimal Error Contract specification for aggregation,
rendering and lineage; error typing is not a dependency. Learner follow-up stays
in its separate handoff. Details and exact evidence links:
[PIPELINE_ACTIONS_AND_EXECUTION_ORDER.md](PIPELINE_ACTIONS_AND_EXECUTION_ORDER.md).

This closeout changed these two status documents and ignored review artifacts
only. No pipeline/learner/model source changes, SQL, production processing or
commit. Earlier P1 source work remains in the working tree: model.py, catalog.py,
classifier.py, matching.py, bindings.py, domain.py and raw_input.py. Verification
processes have completed.

## Task 4 supplemental correction published — 2026-09-24

Owner directed fixing the native reason-boundary defect and supplemental delivery
to pipeline Task 4. New selected immutable model: 1d1d6e0389f7235f565b2504;
manifest 110ca10dc94bd9e2cdaebb0c0dfe5f9f4e1c0b86e1285dad82a8d909cb43e3b1.
Source candidate cca96d77f96382f7082a3f73, learner v26. Raw parser v1.6 and its
implementation hash are unchanged: the defect was model/learner-owned.

owner_rules.json explicitly permits empty REASON and captures complete whitespace
runs outside the reason. constructions.py enforces declared empty permission;
patterns.py emits a zero-length declared inference unit once and resumes at the
same raw piece. Present empty capture is value="", span=[p,p], not absence/null.
No example-specific cases, new tokenizer, slot type or threshold change.

Audit of the 73-log raw census: 15558 declared distinct messages / 1174352
occurrences; exactly five changed reason ranges (eight occurrences), zero boundary
errors. Native witnesses were checked against original log hashes/bytes and exact
reconstruction. Ten-log rebuild retains all 229 compact template records and
captures/outcomes exactly; 133 supported + 96 provisional. Previous release bytes
remain immutable. Distribution contains the new selection and six release files.

Existing docs/LEARNER_PARSER_PIPELINE_HANDOFF.md contains the Task 4 supplement,
new pin and consumer instructions. Task 4 has concurrently implemented native
schema-3 loading/matching. Read-only integration probe: all five affected native
messages now return ordinary unknown with no declaration exception; isolated
native-member inference also yields exact reason captures in its matcher. No
pipeline caller source was changed by this learner task; no ingestion was run.

Evidence: .codex-tmp/learner-refactor/empirical-regions/empty-reason-review/.
The twenty-log experiment completed successfully in 1439.973 seconds. Candidate
9b7b9c106a99cc32129e6e53 in empty-reason-twenty-02 has 196 supported / 126
provisional patterns, 618689 full / 194716 provisional occurrences across 813405
messages. compare_twenty.py completed: 20 previous provisional families now
fully supported, 76 remain provisional; on the original ten logs, 299 occurrences
improve from provisional to full, none regress in outcome. Capture assignments
change on 199 contextual rows / 926 occurrences and require semantic review.
This wider candidate is NOT selected or published; no support policy changed.
Results: empty-reason-review/twenty-log-comparison.json.

The owner's subsequent trace correction supersedes the initial diagnosis of an
interface gap: the whole-chain PARAM boundary itself was wrong. The owner rejected
extracting nested locations from it. That proposed implementation was removed
before building. The v27 work removes script-location-frames and uses the existing
file/line-introduced parenthetical trace rule so normal LOCATOR slots remain outside
PARAMs; see the newest checkpoint above. Name handling acceptable for now per
owner. Orphan-event formulation has no locator in 385 occurrences / seven event
IDs / 55 logs; other event errors do have locations. Native evidence:
empty-reason-review/owner-examples-audit.json and trace-boundary-review/.

## Follow-up: template counts, thresholds and ten more logs — 2026-09-23

Owner seeks explanation of count reduction (which may be good), incremental
benefit and provisional usability. Same-ten-log comparison: v23 231 patterns;
v24/v25 229, now split into 133 supported + 96 provisional. Thirteen provisional
patterns / 38487 occurrences have multiple native messages but only LOCATOR
variation, excluded by an implementation policy now explicitly flagged for review.
No thresholds changed. Provisional hypotheses already participate in reference
matching and expose captures, but do not yield full accepted outcomes.

Attempted cumulative twenty-log build, original ten plus seeded ten from remaining
63, v25 unchanged. FAILED on native empty reason `[  ]`: declaration requires
nonempty L2 and takes one space from a two-space raw gap; field_ranges raises.
One occurrence in the selected logs. Native bytes/hash verified. No twenty-log
model, promotion forecast, filtering workaround or new publication. Evidence at
.codex-tmp/learner-refactor/empirical-regions/additional-ten-01/. Existing formal
pipeline handoff updated with the integration caveat. Next work: correct empty
reason boundary handling/graceful unresolved behavior, then rerun unchanged
selection; separately resolve whether LOCATOR variation should count as evidence.
No process remains running.

## Published learner/parser delivery — 2026-09-23

Owner-authorized publication completed in models/b1965fa4408ca1bcf36763c9;
models/selection.json pins manifest ce2d0b29b0ff95a3074229aa09b7d31be48bc4f381bc4dc402c84f0ea594399a.
Source candidate 17583181d0289e7f2ad2cf00, algorithm v25, parser v1.6 unchanged.
133 supported / 96 provisional hypotheses; 291441 full / 60876 provisional
occurrences in the same ten complete native logs. No unknown/ambiguous outcomes
in that training corpus. Publication preserves all template statuses; zero
individually confirmed templates. No new inference changes versus reviewed v24.

The existing docs/LEARNER_PARSER_PIPELINE_HANDOFF.md is rewritten as the current
formal reply to LEARNER_MODEL_DEPENDENCIES.md, per explicit owner request. This is
the shared-repository notification, not a separate handoff. Pipeline owns reader,
matcher, diagnostic/SQL integration. Published model is not activated in ingestion.

Owner settled the compound survey questions: supported variable expression
fields remain PARAM even for one-token members; malformed colon-qualified
references may occupy KEY. No colon-count/game-validity gate, prefix whitelist,
expression parser or example-specific override was added. The rejected grammar
recommendation is withdrawn from current documentation. Native malformed-reference
pieces were rechecked directly against the original log. Presumed literals stay off.

Validation uses only real native logs: all 7864 contextual results and 20832
message captures preserved by compact export; 21712 inferred field ranges agree;
all ten packaged-parser input files reconstruct exactly. Same-ten-log comparison
shows zero template/capture/outcome changes. Source observations remain ignored
under .codex-tmp/learner-refactor/empirical-regions/publication-review/ and
publication-development-01/. Native checks now verify the owner-settled PARAM
field's actual variation and boundaries, instead of the obsolete short-value KEY
assertion. No synthetic emissions/probes were introduced.

Remaining limits: 60876 provisional occurrences, general word-bounded PARAM
inference, rich-text/name semantic review, wider model learning and actual
application/SQL verification. This release does not claim unseen accuracy or
supply deterministic error typing. No training/background process remains.

The 73-log compound survey remains descriptive evidence, not training for this
release (2594601 recovered messages / 2517940 emissions / 90518 distinct pairs).
Historical checkpoints below describe their then-current restrictions/results;
the publication and owner decisions above supersede them.

## Learner checkpoint — 2026-09-23: raw-span evidence and provisional support

Current algorithm v24; candidate 9b49f15041153abb1fc6789b at ignored
.codex-tmp/learner-refactor/empirical-regions/param-evidence-development-02/candidate/.
Parser unchanged v1.6. Removed whitespace, nested-content and alternating-token
requirements from PARAM evidence, including false owner attribution. Positive
raw-span evidence is separate from boundary validation; qualified KEY pieces
cannot themselves justify PARAM when mixed with an outlier.

Singleton/location-only-repeat candidates remain provisional. Status supported
means at least two distinct non-location examples, not semantic confirmation.
Provisional-only matches cannot produce full outcomes or be confirmed/seeded.
Same ten logs: 133 supported / 96 provisional candidates; 291441 full / 60876
provisional occurrences, zero unknown or ambiguous. No model promotion.

32/33 native requirements pass. Remaining explicit failure: quoted statement
references become PARAM after pooling six KEY-compatible values with one complex
function expression (seven distinct values / 51 occurrences; 39 change KEY type).
Do not silently weaken that check or introduce a case-specific guard. Next review
is whether this uncommon complex value warrants broadening the whole field.
Four rich-text messages also consolidate; their formatting boundaries need review.
Mesh/character captures are retained; new general raw evidence replaces the old
restrictions rather than introducing captures already present in v23.

Delivery: .codex-tmp/learner-refactor/empirical-regions/param-evidence-delivery/
FINDINGS.md + REVIEW.html contain exact native examples, raw pieces, region values,
lengths, prior/current templates and semantic issues. Native check output, source
snapshot, full comparison and commands are saved there. Implementation ledger,
model contract, rule registry, README and pipeline handoff updated. No pending
training process. Earlier v23/v22 notes below are historical, not current status.

## Separate learner/parser checkpoint — 2026-09-20

### Qualified references, bracket sequences and character descriptions — 2026-09-23

Owner-directed v23 changes implemented and verified. KEY can cover adjacent
colon-qualified identifiers over separate raw pieces, with key_joiners=[':']
declared in the registry and applied identically during inference/matching.
Bracket-region validation now admits variable-length token/separator sequences;
the native mesh pool already contained the needed variation. Character: name /
title / balanced ID-parentheses is an owner-declared PARAM for characterhistory.cpp.
No name, mesh or identifier-prefix whitelist; no raw-parser or runtime changes.

Candidate f9d422a0a044d4670b9c54fd at ignored
.codex-tmp/learner-refactor/empirical-regions/qualified-fields-development-01/candidate/.
Same ten logs: 352,317 full, zero ambiguity/unknown; templates 265 -> 231.
30 native checks pass. 19,392 occurrences change captures; all 40 formulation
transitions reviewed. 19,251 script errors generalize qualified KEYs, 100 mesh
occurrences capture bracket interiors as PARAM, and Basilia's complete description
is PARAM. All 205 parent-history outer PARAMs are unchanged. The prior spouse
ambiguity resolves; full matches are not semantic approval.

Remaining: one separate concubine formulation retains its second description
literally; three-KEY parent explanations, title fragmentation and brace singleton
qualification remain. Source/input hashes and exact capture reconstruction verify.
See qualified-fields-delivery/REVIEW.html and LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md.
Pipeline handoff documents key_joiners; no promotion or caller refactor performed.

### Brace candidate provenance — 2026-09-23

Investigated owner concern: brace candidate is two identical occurrences in two
logs, deduplicated to one learning record, not ten-log support. Saved refinement
splits a 506-member group and retains the one-member brace group literally.
There is no separate qualification gate for retained observations versus
empirically generalized candidates; provisional patterns can count as full
structural matches. Owner's contextual malformed-slot idea is documented as a
recommendation, not implemented inline or as a new rule. See
LEARNER_BRACE_CANDIDATE_INVESTIGATION.md for evidence and the proposed correction.

Fixed a reporting defect discovered here: the first-occurrence-only streaming
view cannot count supporting logs. It now has an explicit retain_occurrences
option; diagnostics consumes all provenance before retaining compact samples.
All 265 per-template log totals reconcile. Added supporting log counts, KEY-value
diversity and diagnostic-form counts excluding locators/declared traces. Exact
native variants can differ only in locations, so they are not interchangeable
with KEY diversity. Current results are training-corpus replay, not independent
generalization tests. No inference/model changes or retraining.

### Frequency/outlier and original-case review — 2026-09-23

Owner requested the same problem cases plus common-template and statistical
outlier views. Extended build_visual_review.py with a read-only diagnostics
export and template_review.html. Uses unchanged v22 candidate
231197737b82bcf8386a3ac2 and v21 baseline, same ten logs. Original outer-delivery
cases 01–17 retain their exact native record IDs; original, v21 and current
formulations can be inspected with current captures and raw pieces.

265 templates, 439 native examples. Unique-match frequencies reconcile to
352,316; ambiguous occurrences are separate. KEY proportion excludes PARAM,
REASON and LOCATOR contents/slots and punctuation; denominator is literal
alphanumeric raw tokens plus KEY/OPTIONAL_KEY/VALUE slots. Separate rankings
show adjacent KEY runs, single-message literal templates and undeclared
word-bounded PARAMs. Percentiles are descriptive review signals, not automatic
rejection rules, and same-source percentiles require at least five peers.
No inference, owner-rule or model changes; no training run or promotion.

Saved export and interactive fragment:
.codex-tmp/learner-refactor/empirical-regions/typed-fields-diagnostics/.
The leading recurring defect is the 165-occurrence parent reason captured as
three KEYs. Correct two-KEY templates also rank highly; density alone is not
semantic evidence. Previous cases 05/12/13/17 have the expected KEY captures;
06 has the correct outer parent PARAM but still the three-KEY reason; 04 is now
an exact literal expression; 08 captures Alvise of Salisbury of intact; 10 and
15 retain their preceding formulations. See FINDINGS.md in the export directory.

### Ordinary KEY/PARAM fallback removed — 2026-09-23 (verified; owner review)

Latest owner direction: fix the diagnosed fallback. Algorithm v22 no longer
assigns PARAM merely because KEY/numeric/location checks fail. Ordinary PARAM
requires observed phrase variation and boundary validation; explicit declared
and empirical balanced-region evidence paths remain. Unsupported aligned fields
partition by native raw syntax and re-infer; otherwise keep literal alternatives.
No scope-prefix rule, presumed literals, NAME type or parser/runtime change.

Candidate 231197737b82bcf8386a3ac2 under ignored
.codex-tmp/learner-refactor/empirical-regions/typed-fields-development-01/candidate/.
Same ten logs: 352,316 full / 1 ambiguous / 0 unknown; templates 244 -> 265.
8,984 occurrences change formulation/captures. Ordinary key references and
reported-token values become KEY/OPTIONAL_KEY; punctuation outliers remain
literal. Qualified references retain locally inferred prefix punctuation.
All 205 outer parent PARAMs remain unchanged. Twenty-seven native checks pass;
exact reconstruction, candidate-member spans and source/input hashes verify.

Generalization regressions remain: names split into two KEYs in 14 activity
messages; two spouse descriptions, one marriage-age description and 40 mesh
occurrences become overly literal; four rich-text messages fragment. Earlier
title fragmentation and word-bounded parent explanations remain. Full-match
counts do not establish semantic correctness. All 33 changed formulations are
reviewable in typed-fields-delivery/REVIEW.html under the same evidence root,
with source snapshot and verification. No promotion or 73-log run.
Detailed mechanics and counts: LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md.

### Region-first balanced PARAM — 2026-09-23 (verified; owner review)

Owner authorized fixing the execution order and rerunning. Algorithm v21 proposes
outer balanced asymmetric regions before initial wording comparison and interior
alignment. Candidate-local variation plus phrase/nested content validates ordinary
PARAM. Internal recurring words remain opaque; native boundaries are preserved.
No character-specific JSON envelope, NAME type or presumed-literal restoration.
Known declared fields/locations keep priority; symmetric quotes retain prior
handling. General word-bounded inference and ordinary slot fallback remain gaps.

Candidate 22b23eefbc90b3e8b6e69b11 under ignored
.codex-tmp/learner-refactor/empirical-regions/region-first-development-01/candidate/:
same ten logs / 352,317 occurrences, 352,316 full / 1 ambiguous / 0 unknown.
Templates 240 -> 244. All 205 parent-history occurrences capture the outer parent
description intact. All 22 newly resolved ambiguities were parent-history;
the Jiong_7085 spouse overlap remains. Twenty-two native checks pass; exact
capture/member reconstruction and source/input hashes verified.

Regressions: 11 title-report occurrences split into narrower formulations,
including 3 entirely literal rows and 4 titles captured as three KEYs. Existing
three-KEY parent explanations and reported-token PARAM fallback are not fixed.
Review and preserved source/evidence:
.codex-tmp/learner-refactor/empirical-regions/region-first-delivery/REVIEW.html.
Detailed status in LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md. No promotion,
confirmation, production/SQL change or deferred 73-log exercise.

### Presumed-literal guidance disabled — 2026-09-22 (verified; owner review)

Latest owner direction supersedes the contextual-relaxation proposal below:
presumed literal guidance is globally disabled through
`owner_rules.json.default_literals.enabled=false`. Reference words are inactive;
effective grouping/anchors/inference/matching guidance is empty. No replacement
word list, exception, parser change or new PARAM policy. Algorithm v20 prevents
silent reuse of earlier guided candidates.

Same ten logs: candidate `9070fd331e7cb810fa98b58c` at ignored
`.codex-tmp/learner-refactor/empirical-regions/no-guidance-development-01/candidate/`.
352,294 full / 23 ambiguous / 0 unknown out of 352,317 occurrences, unchanged
outcomes from v19; templates 257 -> 240. Culture/faith now join KEY trigger;
861 contextual rows / 154,528 occurrences change formulation/captures.
Regressions: 165 parent-history occurrences lose reason wording to three KEYs;
217 localization-error occurrences turn optional Near into OPTIONAL_KEY.
Guidance remains disabled. These expose remaining empirical wording/slot-evidence
weaknesses for review, not justification to restore example-specific rules.

19 native checks pass, exact reconstruction/member spans and source/input hashes
verified. Review and source snapshot:
`.codex-tmp/learner-refactor/empirical-regions/no-guidance-delivery/REVIEW.html`.
Detailed results/checklist in LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md.
No confirmation, promotion, runtime/SQL change or deferred 73-log exercise.

### Declared traces as ordinary PARAM — 2026-09-22 (verified; owner review)

Owner authorized the trace experiment and asked why culture trigger is literal.
Trace recognition is declared in `owner_rules.json.parameter_structures`, consumed
by `parameter_structures.py`: complete Script location file/line chains and located
balanced parenthetical interiors. These are atomic ordinary PARAM fields during
inference, including single-observation traces. Their contents do not affect
wording comparison or alignment. Complete-message selection respects declaration
presence/order; PARAM matching has no trace-specific constraints or slot type.
No source-specific examples, names, folder lists or vocabulary exceptions added.

Final v19 candidate `7416a879fac4bf86ef1df0b5` under ignored
`.codex-tmp/learner-refactor/empirical-regions/trace-development-02/candidate/`:
same 10 full native logs / 352,317 occurrences, 352,294 full / 23 ambiguous /
0 unknown; 257 eligible candidates, none confirmed. Previous run: 352,051 / 266 /
0 and 275 candidates. All 244 script-system ambiguities resolve. The 23 remaining
are character-history (22 old plus one new overlap). Build 62.172s versus 780.817s.
All 18 native checks pass; trace spans, exact reconstruction, candidate-local
field spans and source/input hashes verified. Raw parser remains v1.6.

Review: `.codex-tmp/learner-refactor/empirical-regions/trace-delivery/REVIEW.html`
(31 before/after examples; culture-trigger first). Ledger:
[LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md](LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md).
`culture` is blocked from KEY by presumed-literal grouping/slot veto, not short
message similarity: 409 distinct rows / 146,941 occurrences. Guidance vocabulary
was deliberately unchanged; next proposal is contextual, evidence-driven relaxation
for an identifier position, not globally unprotecting culture or a word exception.
No promotion, SQL changes or deferred 73-log run.

### Punctuation-boundary follow-up — 2026-09-22 (completed; owner review)

Owner authorized generic punctuation-preferred PARAM boundaries and a same-ten-log
rerun, explicitly banning example-specific fixes. Algorithm v17 now re-infers
weak one-word divisions beside punctuation, retains outer delimiter ranks despite
interior repetition, requires stronger variation for punctuation-free PARAMs,
counts all complete capture assignments, and reconsiders both subsets of partly
failing groups. Policy/authority are in owner_rules.json. Raw parser stays v1.6.

Candidate `b8706927a26d53a7c50efbfd` at ignored
`.codex-tmp/learner-refactor/empirical-regions/punctuation-development-01/candidate/`
has 275 templates (274 eligible / one unresolved), 352,051 full / 266 ambiguous /
zero unknown occurrences from the same 352,317 messages. Sixteen native checks
pass; all accepted member spans agree with inference and reconstruct exactly.
Elapsed build 780.817s, versus preceding 428.391s. Three word-only PARAM fields
remain flagged. 255 previously full occurrences become ambiguous, despite the
net gain of 218 full matches; broad trace overlaps and broadened character-ID
PARAMs remain material review concerns.

Review: `.codex-tmp/learner-refactor/empirical-regions/punctuation-delivery/REVIEW.html`
(35 examples; first three correspond to previous 04/08/10). Ledger:
[LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md](LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md).
The bundle/report/source snapshots preserve evidence. No promotion, confirmation,
runtime change or 73-log exercise. Old bundles are read only as saved comparison
evidence; current loading requires matching algorithm revision and owner rules.

### Outer-diagnostic implementation — 2026-09-22 (verified; model review remains)

Owner approved the eight recommendations and directed a stepwise Markdown
ledger: [LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md](LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md).
Schema 3 now learns/matches complete outer diagnostics. The established script
envelope is declared in `tools/template_learning/owner_rules.json`, consumed by
`constructions.py`; its bracketed reason is intact REASON content. No detached
L2/tail pools remain. Locations/traces participate in the complete candidate.
The raw parser remains v1.6. Short-form consideration, candidate-local slot
provenance, stronger PARAM assessment and field-local literal relaxation are
implemented. Both observed script envelope variants are declared in JSON;
construction identity is enforced in matching. Candidate acceptance also
requires exact replay of its members' inferred field spans.

Verified command/output: ignored
`.codex-tmp/learner-refactor/empirical-regions/outer-development-11/`, using the
same ten logs as `empirical-delivery/candidate/e0f2d9bfd621adf7176400aa`.
Candidate `a5f3ace2fd908c6250ac7edd` completed in 428.391 seconds. All 11 native
checks passed. Outcomes: 351,833 full / 323 ambiguous / 161 unknown across
352,317 messages. There are 292 candidates, including three unresolved name
boundary candidates. Baseline had 13 ambiguous and zero unknown: this is not
an overall matching-quality improvement yet. No accepted member capture differs
from its inferred spans; full byte reconstruction and source hashes pass.

The owner-readable comparison has 39 distinct formulation examples, actual
captures and candidate-local PARAM witnesses at ignored
`.codex-tmp/learner-refactor/empirical-regions/outer-delivery/REVIEW.html`.
JSON comparison, 69-example visual-review dataset, verification metadata and
the exact source snapshot are beside it. Remaining work: repeated wording in
name fields (65 character-history / 96 landed-title unknown occurrences),
broad/narrow overlaps (323 occurrences), and semantic review of PARAMs spanning
several trace lines. Details and per-recommendation status are in the ledger.
Do not promote this work or launch the deferred 73-log exercise. The earlier
entries below are historical checkpoints.

### L1/L2 architecture reconsideration — 2026-09-21

Owner questions independent L2 learning and favors capturing the known bracketed
reason intact as a dedicated outer/L1 field, with locators/trace belonging to the
outer diagnostic. No implementation change yet: requested precise association
review saved as L1_L2_ASSOCIATIONS.html and L1_L2_REVIEW.md under ignored
.codex-tmp/learner-refactor/empirical-regions/. Native evidence in L1_L2_EVIDENCE.json.

Current code learns prefix/L1/open/L2/close/tail separately. Tail belongs to neither
L1 nor L2, and pools across all source L1s. L1 matching sees only L1; complete
classification separately requires unique matches for all regions. It does not
currently treat L2 as PARAM. Owner's proposed raw reason field is a change to
that contract, not a new name for the current independent L2 matching.

Exact native review: 793 distinct L2 texts, 19 reused with multiple exact L1s.
Trying to unlearn native language occurs 396 times only with unlearn_language
effect. Trying to <PARAM> combines five distinct failures; this is overbroad
consensus/fallback inference, not demonstrated diagnostic equivalence.

95 native two-token L1s end in effect. Two such L1s share one word and score .55,
below .72; iterative regrouping also requires two shared words. These gates
block plausible <KEY> effect inference and need general short-form treatment.

A01's tail has 54 distinct training tails associated with 15 L1s, mixing effect
and trigger failures. All five PARAM positions have genuine multi-token witnesses
in that wider pool. But its ten unlearn_language tail variants each retain the
same one-token values, so this failure alone supplies no PARAM evidence.
No automatic parentheses-to-PARAM rule remains. The broader pool and permissive
multi-token fallback are the actual mechanisms. The earlier random A01/A03/A04
selection repeated one failure with different locations; use distinct failure/
template-change formulations for future owner review, not full-row uniqueness.

### Owner-readable PARAM review — 2026-09-21

Owner requested explanations and random before/after examples. No learner or
parser changes and no training in this follow-up. READABLE_REVIEW.html under
.codex-tmp/learner-refactor/empirical-regions/ shows full native messages above
side-by-side actual template renderings: ten uniformly sampled distinct rows
from the 18 resolved-ambiguity rows, ten from all 3,782 changed rows, and the ten
original region examples. Seeds 20260921 / 20260922 and selection provenance
are saved; Markdown companion and RULE_EXAMPLES.md explain safeguards plainly.

Correction: 1,934 changed rows / 94,307 occurrences have unchanged written
templates and captures; candidate identities/constraints changed. Only 1,848
rows / 27,819 occurrences have visibly changed templates. Random cases expose
additional quality concerns: Trying to <PARAM> pools different L2 failures;
Malformed/Unexpected become a leading KEY; Reason<PARAM> can absorb colon and
empty-explanation whitespace. Do not equate matching coverage with correctness.

Default-literal guidance is currently a hard barrier in grouping, alignment
and PARAM matching. Native trace interiors tribute_mission_decision_china:effect
and VIETmisc.5052:trigger retain guided effect/trigger as literals. Owner proposes
presumed literals that can become captured content inside an empirically
established field. Examples gathered; this change is not yet implemented.
The separate learned-wording safeguard preserves gene-error formulations but
overprotects Wet Fields. It is not the same mechanism as default guidance.

Verified native middle-of-message PARAM lengths of one and four raw tokens match
the same following literal. Matching is ordered and exact but not tied to fixed
token ordinals. Owner explicitly confirms backslash exclusion from PARAM marker
proposals based on prior path-use assessment; do not reopen it because this
ten-log subset has no examples. Raw separator/path handling remains unchanged.

### Empirical regions delivered and compared — 2026-09-21

The complete owner instruction packet removes the terminal-parenthesis shortcut
before replacement development. Required code edits were applied in descending
line order and source snapshots saved under
.codex-tmp/learner-refactor/empirical-regions/removal-source/.
Removal-only ten-log baseline 248aaaad5e39b1cd80ff0872 completed before replacement
development. Final candidate e0f2d9bfd621adf7176400aa is under empirical-delivery/.
Earlier shortcut-assisted checkpoints below are historical and are not evidence
for general inference. No active shortcut or compatibility path remains.

The replacement investigates interior literals and ordinary slot types, supports
arbitrary-position regions, iterates provisional unions only after empirical
support, and records accepted/rejected/narrowed/divided/insufficient hypotheses.
Supported PARAM contents have zero similarity weight and no placeholder bonus.
No parser change or new hard-coded PARAM format. Generic conservative wording
and evidence-sufficiency heuristics are explicitly identified in owner_rules.

Same ten complete logs / 352,317 messages: ambiguities 2,066 -> 13; full ordinary
140,443 -> 140,435; L1+L2 209,808 -> 211,869; zero unknown/partial/L1-only.
2,064 ambiguous occurrences resolve; 11 previously complete occurrences become
ambiguous (eight culture-history explanation overlaps, three Wet Fields building
overlaps), and two existing Lowborn ambiguities remain. Do not hide these with
preferred-match selection. Ordinary templates 321 -> 308; components 432 -> 354.

Seven native checks pass, including 21 independently inspected capture ranges.
Audit replayed 36,074 captures including wrappers, reconstructed 23,073 matches,
and verified 231,879 proposed byte/piece ranges. Implementation hashes agree.
Final build ~164 seconds versus ~81 for removal-only; audit-rich model ~140 MB.
All jobs completed; no promotion, SQL changes or confirmation decisions.

See LEARNER_EMPIRICAL_REGIONS_REVIEW.md for results, decisions and limitations;
ignored REGION_EXAMPLES.md has ten detailed native region examples and
NATIVE_COMPARISON.md has 46 before/after cases. Next review is broad/narrow
wording overlap and remaining short-message fragmentation. The 73-log run and
broader/restricted vocabulary comparison stay deferred.

### Historical, withdrawn shortcut: PARAM boundary rerun — 2026-09-21

Delivered candidate dbd987c8de8e65127a8acb08 under
.codex-tmp/learner-refactor/param-boundary-review/candidate-reviewed/.
Parser v1.6 unchanged. Wording similarity excludes punctuation, locations and
terminal bounded interiors, with no PARAM placeholder bonus. PARAM admits
internal punctuation; terminal_parentheses matching captures the complete
balanced interior. Constant contents stay literal; observed variation establishes
the slot. Boundary absence and optional literal punctuation produce separate
formulations. Joint native re-inference can merge fully covered provisional
groups, preserving fixed wording and reporting partial overlaps.

All 352,317 messages from the same ten full logs preserve their outcomes:
140,443 full; 211,872 L1+L2; same two characterhistory Lowborn ambiguities;
zero unknown/partial/L1-only. Ordinary candidates 374 -> 309; L1 188 unchanged;
L2 130 -> 147; tails 97 -> 41. All 18 Badly read script value variants (35
occurrences) now share KEY/file LOCATOR/line LOCATOR/terminal PARAM formulation.
33,835 nonempty captures verified; 21,196 matches replayed; 4,498 terminal
captures checked, including 1,176 nested cases. Five real-native tests pass.
Code hashes match the immutable bundle; final run ~129 seconds. Jobs completed.

Important remaining regression: some short/name-heavy L2 formulations fragment
under the unchanged .72 threshold after punctuation ceases boosting similarity.
Culture/innovation and legitimacy examples are documented; successful training
matches do not prove preserved generalization. This needs follow-up calibration
and discovery work, not sentence-specific overrides. See
LEARNER_PARAM_BOUNDARY_REVIEW.md and its native comparisons. Pipeline handoff,
model contract, rule ledger and owner_rules reference updated. No promotion or
SQL changes; 73-log run and broader/restricted vocabulary comparison deferred.

### Trace/PARAM mechanical investigation — 2026-09-21

Owner rejected punctuation-pattern equality as a grouping prerequisite and
requested the precise PARAM blocker. Confirmed on all 18 native script-value
cases, with original file hashes/message byte ranges checked: two trace-depth
variants score .95 against .72 threshold but the punctuation signature prevents
comparison. Alignment also rejects different signatures; candidate validation
forbids punctuation in non-LOCATOR slots; PARAM matching stops at punctuation.
The existing slot classifier already returns PARAM for the actual trace ranges.
All 18 fail current PARAM matching; all 18 match with only that candidate's
punctuation prohibition disabled in an isolated inspection. No production edits.

Incremental builds do combine all selected evidence and rebuild provisional
groups, retaining confirmed templates first. There is no general iterative
reassignment, and rebuilding cannot bypass the hard punctuation gate. See
LEARNER_TRACE_PARAM_INVESTIGATION.md for code paths, authentic examples,
recommended scope, and limitations. No CK3_TRACE type or universal parenthesis
recognizer was introduced. Next fix must address grouping, bounded trace ranges,
alignment/validation and PARAM matching together, then compare the same ten logs.

### Fresh ten-log learner run completed — 2026-09-21

Owner authorized running the current learner with all implemented improvements
and parser v1.6. Fresh ten-log candidate e375ae7fb4cf74bcdef446ec is under
.codex-tmp/learner-refactor/separator-learner-review/candidate/.
Compared with v1.5 candidate 255eecc2dd7965207c58b0da on identical native evidence:
352,317 messages; ambiguous 10 -> 2; full ordinary 140,442 -> 140,443;
L1+L2 211,865 -> 211,872; unknown/partial/L1-only all zero. No previously complete
outcome regressed. All 34,476 inspected nonempty captures match original bytes
and raw boundaries. Effective literal guidance and learner Python hashes match
the baseline; owner-rule differences are architectural descriptions only.

Important concern: more specific trace anchors fragment learning groups.
Ordinary templates 300 -> 374; L1 unchanged at 188; L2 134 -> 130; trace tails
47 -> 97. Same-source Badly read script value messages split into four groups
by trace punctuation, fixing @cultural_maa_extra_ai_score in a one-distinct-message
group. The parser correctly preserves the symbol; this is learner grouping.
The two remaining ambiguities are characterhistory.cpp formulations where
Lowborn is literal in one candidate and KEY in another. Do not hardcode a fix
or undo parser boundaries. See LEARNER_SEPARATOR_IMPACT_REVIEW.md for exact
native evidence and the distinction between improved training coverage and
unmeasured unseen generalization.

48 before/after cases, complete comparison JSON, script-value grouping evidence
and refreshed top-template/ambiguity visualization data are saved beside the
candidate. The old HTML visualization is still historical. All jobs completed;
no inference edits during the comparison, no registry write or model promotion.
Next: address trace-driven over-fragmentation and the two overlaps, then complete
the pending same-ten-log broader/restricted symbol-literal comparison. The full
73-log run remains deferred. Parser lexical-category metadata is still only a
proposed cleanup; it was not implemented or claimed as part of this run.

### Separator/punctuation fix delivered — 2026-09-21

Owner approved the stdlib scanner implementation. Current manifest selects
ck3-lossless-v1.6, SHA-256
a9ed06a6c141a184939518c0b64292b1b48fda7f09fccc9067b3ecd944bd96d6.
Only lexical_pieces changed among existing parser definitions; _scanner is new.
Colon, slash, backslash, braces, brackets, parentheses, double quote, equals,
semicolon and pipe are individual tokens everywhere. @ stays within symbols;
underscores, internal dots/hyphens, signed numbers and leading/internal filename
exclamation marks survive. Exact Div/0 remains the approved exception.

Ten complete native logs (91,407,302 bytes): all 19,623,700 pieces reconstruct
exactly, separators isolate correctly, and framing/recovery remain identical for
343,585 emissions / 352,317 messages. 177,905 emissions change token boundaries.
No changes to recognized location ranges across 7,827 distinct source/messages.
Nine focused native checks passed, including independent pipeline loading,
learner collection, debug replay and feature-cache roundtrip. No constructed
lexical checks ran; the old synthetic lexical-example test was deleted.
See LEARNER_SEPARATOR_FIX.md and the fourteen-category before/after native
examples under .codex-tmp/learner-refactor/separator-fix/.
Fresh-process timing on the same three complete logs (43.7 MB), two repeats:
v1.5 40.61–40.65 s; v1.6 28.52–28.54 s, about 30% less lexing time. Peak memory
is effectively unchanged at 168–170 MiB. All audit jobs are finished.

Parser spec, owner_rules.json and pipeline handoff now describe v1.6. Existing
candidate models retain their own selected artifacts; no training, promotion,
runtime registry or SQL writes occurred. Next learner comparison must regenerate
features and build its candidate using the v1.6 manifest. Do not reuse old token
indexes or resume the deferred 73-log run. The requested symbol-vocabulary
comparison remains a separate unfinished task.

Owner follow-up: assess how the corrected raw parse improves learning and whether
learner punctuation handling can use the parser directly. The active learner
already consumes selected-parser pieces for alignment, anchors and capture
boundaries; no second punctuation splitter was found in those paths.
patterns.punctuation_piece independently classifies existing pieces with ASCII
and Unicode punctuation categories. It controls literal anchors and capture
exclusions, with recognized location ranges exempted. This is not tokenization.
Potential cleanup is parser-supplied lexical category metadata, retained in
features, to avoid maintaining an independent character classification. It is a
design proposal, not a confirmed native defect or an implemented API change.
Do not re-lex message fragments or move slot/location inference into the parser.
First quantify grouping/capture effects with the v1.6 ten-log learner rebuild;
the current parser checks alone do not establish model-quality improvement.

### Earlier Lark lexer evaluation — 2026-09-21 (superseded by delivery above)

Completed the owner's requested evaluation; see LEARNER_LARK_EVALUATION.md.
Scope is replacement of raw tokenization inside the existing workflow, not a
new diagnostic parser or emission/recovery design. Production remains v1.5,
SHA-256 fd48e9c51acf7e77dbcc3ecb42c8178cc07f58fdecefb84ed9dbeaae2fe8cc16.
The owner installed Lark 1.3.1 for research; no dependency declaration changed
in this evaluation. No training, model promotion, registry or SQL writes.

Lark with parser=None/lexer=basic and the corrected stdlib candidate agree on
19,623,363 pieces over the same ten complete native logs: 91,407,302 bytes,
343,585 emissions and 352,317 recovered messages. Exact byte reconstruction,
offsets, mandatory separator isolation, and unchanged message recovery passed.
Existing LOCATOR ranges agree on all 7,827 distinct source/message pairs after
correcting two experimental policy regressions (numeric sentence-ending dots
and filename underscores). Partial-Lark and generated variants agree on three
complete logs, including the largest 39.7 MB log.

Repeated 43.7 MB timing: corrected stdlib 14.81–18.41 s; Lark 33.22–33.63 s;
partial Lark 32.86–33.59 s; generated 31.87–31.97 s. Peak process working sets
roughly 169–173 MiB. Recommendation is a single corrected stdlib scanner with
explicit terminal policy; Lark is viable but supplies no correctness advantage
under the same policy and requires dependency/version-contract changes.

Owner accepts the stdlib re scanner direction for tokenization. Semicolon and
pipe are always separators, as are the already directed slash and backslash.
The backslashes used to escape pipes in the report's Markdown table were not
native characters. @ stays within a continuous symbol at any position; ! is
valid filename content beyond the leading position. Correct the lexer only.
Saved benchmarks used the preceding policy, which retained internal pipes and
semicolons; rerun native verification for the corrected policy. Production v1.5
has not yet been changed by this evaluation.
Owner correction: use only complete native error logs for evaluation. Constructed
inputs, assertions, saved probe outputs and source snapshots containing them have
been deleted. Questions and proposed work originating from synthetic checks are
deleted, not deferred or retained for future review. Withdraw synthetic-only
claims and hypothetical consumer work;
unobserved cases are unverified, not new requirements. Retain the directed raw
backslash separator. Parser revision/cache identity and native model relearning are
implementation consequences, not additional owner decisions. Do not introduce
a folder whitelist or absorb separators into KEY values. The grammar/scanner
performs no semantic inference.
Research tool: tools/template_learning/evaluate_raw_lexers.py now accepts only
the saved native-log selection, with no probe harness. Grammar, generated lexer,
native comparisons, original measurement hashes and RESULTS.json are under ignored
.codex-tmp/learner-refactor/lark-evaluation/lexer-only/. Earlier broad-policy
experiments in its parent directory are comparison evidence, not the final run.
After removing the probe harness, reran Lark on one complete 105,978-byte native
log: 576 emissions, 579 recovered messages, exact reconstruction and unchanged
recovery. See lark-evaluation/native-only-verification/. No probe files remain
in the evaluation directory; production parser hash remains unchanged.

The pre-evaluation v1.5 candidate remains
symbol-location-review/filename-line-fields/revisions/255eecc2dd7965207c58b0da
under .codex-tmp/learner-refactor/: 300 ordinary and 374 component candidates,
140,442 full / 211,865 L1+L2 / ten ambiguous / zero unknown or partial outcomes.
It was not rebuilt or promoted for the Lark evaluation. The prior symbol-type
vocabulary comparison remains separate unfinished work, not an inferred result
of this lexer evaluation.

### Latest Div/0 lexical exception — 2026-09-21

Owner explicitly requested Div/0 remain one token; tooltip/description should
remain tooltip, /, description. Implemented exact whole-lexeme exception in raw
parser v1.4, with authority recorded in owner_rules.json. SHA-256:
980321008a339e4574ec4c73a8691c8c458c0e3d0fe7057744ee3c5cb765ccc4.
No substring, case-folding, path-name list or learner-side token repair.

Re-read and re-lexed original message ranges covering all 1,628 Div/0 and 730
tooltip/description occurrences in the ten-log evidence. Both remain non-path
expressions. One complete 3,860,922-byte / 25,332-emission protected log round
trips exactly. The entire affected jomini_scriptvalue.cpp source pool across
those ten logs (six distinct records / 1,641 occurrences) re-infers with three
candidates and zero ambiguous or unmatched records. Owner lexical checks also
cover punctuation wrappers, embedded strings and Div/00 without inventing native
emissions. Evidence: symbol-location-review/div-zero-lexeme-checks.json under
.codex-tmp/learner-refactor/. Full model not rebuilt for this bounded correction;
latest complete bundle d195b4944aeeb10cccfec51e still selects its v1.3 parser.
No registry or production model changes; new full learning needs v1.4 features.

### Spaced slash/list verification — 2026-09-21

Owner example provinces / baronies and both one-sided spacing variants produce
no LOCATOR without path context. Whitespace remains raw gaps; path recognition
does not bridge them. No spaced-slash native message was found in the ten-log
candidate or a read-only search of all 2,594,601 saved occurrences from 73 logs.
Do not present the owner example as a native emission. All 2,403 occurrences of
observed unspaced non-path expressions in the ten-log model also avoid LOCATOR
captures. Evidence and exact forms are recorded in LEARNER_SLASH_BOUNDARY_REVIEW.
No inference change or training run was needed for this check.

### Latest filename ! correction — 2026-09-21

Owner clarified that ! is legal filename content, including a leading run and
before the extension. Microsoft Windows naming documentation confirms this.
Parser v1.3 preserves leading ! with adjoining text even for a bare filename;
internal ! remains unchanged, slash stays separate, and sentence-final error!
still separates. SHA-256:
29673f59b674187c3bd33115bdd314b54f768472ad4ae7332cd1cf7e1a5bcb77.

The same ten complete native logs reconstruct exactly again: 91,407,302 bytes,
343,585 emissions, 352,317 messages. Explicit owner filename probes cover the
bare form (not present in these native logs). All 8,249 prior path ranges and
8,282 candidate path captures pass. Current source hashes match candidate
d195b4944aeeb10cccfec51e. Counts: 140,442 full, 211,865 L1+L2, ten ambiguous,
zero unknown/partial/L1-only; 300 ordinary and 374 component patterns.

This build also includes the separately owner-approved wiki-supported symbol
vocabulary update made in the side conversation and recorded in owner_rules.
It is therefore not an isolated parser-only comparison. That update has been
preserved; the earlier 18-word checkpoint below is historical. Evidence is under
.codex-tmp/learner-refactor/symbol-location-review/filename-exclamation/.
No registry/production selection changed. No 73-log run was started.

### Latest slash-boundary correction — 2026-09-21

Owner requires standalone `/` tokens and path recognition across adjacent raw
pieces. Implemented parser v1.2, SHA-256
5f23b0c533ed1183f990b66156cd7b79dbb0f213d2d6a62e8415d2329ca47943.
Learner v8 uses complete location ranges for grouping/inference and matching;
LOCATOR declares location_value rather than single_token. Default words within
paths do not become literal anchors. No folder-derived vocabulary is restored.
Native !! filename punctuation remains within its segment after slash splitting.

Final research candidate: 21658012c3f44bbc5f09716b. Same ten logs freshly parsed:
91,407,302 bytes reconstruct exactly; 343,585 emissions / 352,317 messages;
140,442 full, 211,865 L1+L2, ten ambiguous, zero unknown/partial/L1-only. Compared
with the previous restricted ten-log build, 34 ambiguities resolve and five
previously complete occurrences become ambiguous; five remain ambiguous.
8,282 candidate path captures and 8,249 prior path-range comparisons pass.
Current source hashes verified against the final bundle. No registry/production
change, no 73-log run. See [slash-boundary review](LEARNER_SLASH_BOUNDARY_REVIEW.md)
for native examples, remaining overlaps, constraints and handoff implications.
The current visualization still shows the older 6d230eb73f03d4b738630eb4 model.

### Latest owner correction: remove folder-derived symbol defaults — 2026-09-21

Owner rejected deriving symbol-type identity from directory names. Removed the
folder-derived vocabulary expansion, category/path inventory, and all/restricted
loader selector. Active reference retains the 18 explicitly owner-supplied
symbol spellings with first-letter case alternatives. The directory survey no
longer enumerates game folders. The experimental comparison runner tied to the
rejected expansion was removed. Do not restore that expansion from saved models.

The two-arm ten-log experiment completed before this correction, but its expanded
arm is rejected input and does not answer the requested comparison of genuine
symbol types. Its saved results remain historical evidence only. A valid expanded
vocabulary and new comparison remain outstanding; no full 73-log rerun or model
promotion is authorized by this checkpoint. The prior 73-log follow-up was stopped.

Generic location recognition is retained: explicit labels, colon/in/file context with slash
syntax, and slash-delimited filenames, using raw-token boundaries and no folder
or extension allowlist. Recognized paths remain LOCATOR even with one observed
spelling. Phrase guides now preserve Internal ID and related labels intact;
standalone to/for are unprotected; Event is a symbol type. See
[the corrected review](LEARNER_SYMBOL_LOCATION_REVIEW.md). Existing visualization
still depicts the earlier 6d230eb73f03d4b738630eb4 candidate. No registry selection
or production model changed. Follow-up native verification covered 99 in/file
path evidence rows (963 occurrences), preserving exact LOCATOR spans. Attached
:number is optional native content, never required or appended to paths.
Older entries below describe earlier checkpoints.

### Native evidence visualization — 2026-09-21

Owner requested inspection of top templates with their actual parsed learning
evidence and the most frequent ambiguities. `build_visual_review.py` now exports
a bounded review dataset from a hash-verified bundle without inference changes.
Current candidate remains `6d230eb73f03d4b738630eb4`. Ordinary/L1/L2 rankings use
training support, not all runtime matches; support totals and distinct variant
counts are verified against the complete native export. Examples are actual
inference supports. Ambiguity sets remain source-specific and count each row once.

Under `.codex-tmp/learner-refactor/tighter-wording-review/`: `visual-review.json`
and `learner-evidence.html` provide the inline evidence browser. Each category
has 20 ranked entries; 199 distinct native examples provide 216 selectable views.
Top 20 of 196 ambiguity sets cover 4,623 of 5,656 ambiguous occurrences.
Raw pieces, exact captures and byte spans, L1/L2 context, original paths and first
occurrence provenance remain inspectable. Whitespace glyphs and shortened picker
labels are display-only; exact native text is retained. Browser checks exercised
all 216 views, with no JavaScript errors or narrow-layout overflow. No model or
registry changes. This is a review sample, not a claim that 199 messages suffice
to assess the complete model.

### Latest 2026-09-21 follow-up: tighten native candidate grouping

Owner rejected the mixed groups. Completed generic inference corrections in
`clustering.py` / `patterns.py`; see [native grouping review](LEARNER_GROUPING_REVIEW.md).
Distinct interior wording supported by independent native groups now partitions
a mixed group only when every member selects one alternative. This separates
gene-template versus gene-accessory-group wording. Whitespace-only divisions
between PARAM and adjacent text slots are re-inferred together. Candidates with
the same fixed wording are re-inferred from joint support, accepting a merge
only when all members match and that wording is preserved. These are documented
heuristics, not new owner vocabulary or sentence-specific overrides.

Capture selection now searches raw-piece boundaries directly, fixing the
internal-apostrophe rejection. No parser/reference/source/L1-L2 policy changes.
Same 73 logs / 2,594,601 occurrences / 90,518 messages / 133 sources:
final candidate `6d230eb73f03d4b738630eb4`, full 1,610,797; L1+L2 978,148;
ambiguous 5,656 (was 101,827); unknown 0 (was 171); partial/L1-only 0.
No previously complete outcome regressed or became ambiguous. There are 2,578
distinct ambiguous rows. Registry and production model remain unchanged.

Output: `.codex-tmp/learner-refactor/tighter-wording-review/`, including
`summary.json`, `training-review.json`, `native-grouping-checks.json`,
`fresh-parse-checks.json` and the immutable revision bundle. All 339,119 nonempty
native message/component captures passed byte/boundary checks. Two original
logs freshly parsed (12,417 messages) reproduce cached matches and captures
for all 1,724 distinct combined message/context cases. Current code/bundle
hashes verified. Both builds and verification processes completed.

Remaining work is evidence-led reconciliation of broad/narrow gene candidates
(3,616 occurrences), localization name fragments (1,306), and smaller existing
overlaps (734). Do not hide alternatives by selecting a preferred match. No
promotion has been requested. The previous cumulative/default-word work below
is historical context; its 101,827 ambiguities and 171 unknowns are superseded
by this comparison.

### Active 2026-09-21 follow-up: default words and reference file

Owner approved default words outside the previously proposed specific phrases,
including an initial CK3 symbol-type vocabulary, with exact whole-token matching.
Implemented `tools/template_learning/owner_rules.json` as the directly consumed
reference; removed the narrower `literal_guidance.json` file. It declares 66
words plus `due to`, exact case/plural spellings, authority/evidence, and existing
L1/L2 and slot-position cues. The latter were moved without behavior changes.
Architectural invariants are recorded with their implementation locations.
Models snapshot `owner_rules` and effective guidance and hash the reference.
No generated Python, optional literals or example-specific slot types.

The `Event`/`link` issue is confirmed in complete ordinary script messages:
`Event target link 'scope' returned an unset scope` versus
`Undefined event target 'story'`, with identical wrapper/location. Similarity
0.835 exceeds 0.72; differing failure words become slots despite protected
`target`. Independent default words now prevent that grouping. This is not
evidence of a separate subphrase-template mechanism.

Boundary checks cover the owner's exact names and 1,700 distinct native embedded
strings, with 15 original emissions freshly reparsed. Embedded substring matches
are absent. L1/L2 spans remain unchanged on all 15,646 surveyed native units.
See [default-literal review](LEARNER_DEFAULT_LITERALS_REVIEW.md).

The fixed-corpus comparison completed as candidate `1fbe61bfc955c6773d6c6192`,
against `87b4eed8261625c4ba9ff05c`. Training ambiguities: 96,898 to 955 occurrences,
2,075 to 409 distinct cases; no training recognition loss or new ambiguity.
Additional-log ambiguities: 5,314 to 208 occurrences, 928 to 69 distinct cases.
However 98,736 complete occurrences lose L2 (all Scoped-object/culture), 25
complete occurrences become unknown, and 104 ambiguous occurrences become
unknown. The 48-log training set lacks the culture-specific formulation;
default `culture` now prevents its capture through a broad KEY. Other losses
include religion-scope wording, Unexpected-token/scripted_effect and five
state_faith Event-target messages. Verified `state_faith` stays intact, not an
embedded default match. These frozen losses must remain visible in the report.

An isolated cumulative build added the remaining 25 logs to the 48 through
the existing learner, without installing templates or changing declarations.
Runner: `inspect_accumulated_corpus`, output:
`.codex-tmp/learner-refactor/default-literals-73-log-review/`, with adjacent
`.log`. The run uses an explicit selected parser manifest with the same bytes
as the prior bundled parser, since registry cache identity includes the selected
reference. Do not interpret in-corpus recovery as unseen-log accuracy.
Registry and production are unchanged. Fixed-comparison artifacts are in
`.codex-tmp/learner-refactor/default-literals-review/`.

Cumulative candidate `9310e1af7379beb8f6cbcda4` completed: 73 logs / 2,594,601
occurrences / 90,518 distinct messages / 133 sources. Outcomes: full 1,514,455;
L1+L2 978,148; L1-only/partial zero; ambiguous 101,827; unknown 171. All 98,736
frozen culture losses and 129 new unknowns recover completely after learning
the added evidence. However 92,639 previously complete occurrences become
ambiguous; there are 21,606 distinct ambiguous cases and 31 unknown cases.

Remaining issues are concrete: pdx_locstring.cpp has 97,063 ambiguous occurrences
from overlapping missing-localization PARAM patterns; portraitcontext.cpp has
4,030 from broad/narrow gene-description patterns. One unsupported localization
candidate causes all 171 unknowns. Native `Mts'khet'` has a continuous `Mts'khet`
piece plus a trailing apostrophe, but the matcher regex chooses the internal
apostrophe. Raw-boundary validation rejects it without seeking the valid capture
alternative. `Qal'at al-Nisā'` is the other failing support. See cumulative
`remaining-issues.json` and `unsupported-native-boundaries.json`.

Next work: boundary-aware capture selection and evidence-based reconciliation
of overlapping PARAM/gene-description candidates. Preserve the current defaults;
do not install name-specific exceptions or choose one winner to conceal overlap.
Both builds and all replay processes finished. No model was promoted; registry
current remains `e6aee7eeb209c9e26abf72da`, with no confirmations.

### Latest follow-up: wording survey and separate punctuation

Owner clarified that literal guidance should omit the separate colon tokens.
The live declaration is now `target`, `Reason`, `due to`; parser punctuation
and case-sensitive matching are unchanged. On all 15,646 source/region/context
units in the 48-log bundle, this loses no existing anchors and newly protects
194 units / 38,310 occurrences containing colonless `due to`. This measures
guidance coverage, not classification gains. Prior candidate bundles retain
their exact declarations and have not been rewritten or rebuilt.

Completed [native wording survey](LEARNER_LITERAL_WORDING_SURVEY.md): all
48 training logs / 1,940,027 occurrences, with 298 selected original emissions
freshly reparsed. The `Wrong scope for <KEY>` category slot contains only
`trigger` and `effect`. Observed L2s comprise 18 trigger texts / 190,746
occurrences and 8 effect texts / 425 occurrences. Recommend supplying the two
full introductions as literals, letting scope values continue to vary.

Other directly evidenced literal-loss candidates are `Event target link`,
`Undefined event target`, `Failed to`, `Could not`, `Invalid`, `Near file`, and
`Internal ID`. The survey includes current captures and native provenance.
`expected`, `but got`, `Scope`, `Type`, `was null`, `not found`, `does not exist`,
`near line` and other boundary wording are useful further candidates but already
literal in the inspected candidates' supporting examples. No additions beyond
the colon correction were installed. Review the concrete shortlist before
expanding guidance; then rebuild/compare complete native records. Do not treat
inventory phrases as inferred subtemplates, optional literals or new L1/L2
conventions. No registry/confirmation/production state changed.

Artifacts: `.codex-tmp/learner-refactor/literal-wording-survey/`. Reproducible
read-only tool: `tools/template_learning/inspect_literal_wording.py`.

### Current owner correction: explicit literal guidance, no type override

Implemented `source-component-consensus-v5`. Removed the relationship-specific
PARAM override and its false attribution to owner authority. The relationship
token is inferred normally as KEY. `owner_overrides` is empty; there is no
`owner_rule_id` on new slots. The owner asked about PARAM inference, not for a
hardcoded relationship template or slot type.

At this earlier checkpoint, `tools/template_learning/literal_guidance.json`
(now replaced by `owner_rules.json`) explicitly supplied `target`,
`Reason`, and `due to` (colon omission corrected in the follow-up above).
Exact case-sensitive occurrences at complete raw-piece
boundaries anchor candidate grouping and alignment. Slot matching uses the
candidate's recorded `constraints.literal_guidance` and cannot capture that
wording. Embedded identifier substrings are untouched. Literal parts remain
mandatory; no optional-literal representation is introduced. Separate
formulations with/without supplied wording are acceptable.

The blanket v4 one-fixed-spelling-plus-absence split was broader than the owner
instruction and is removed for separate review. Optional variable slots remain
supported. Case-sensitive retrieval and case-only literal distinctions remain.

The authorized comparison against v4 selects the same 48 native logs and
evaluates the other 25 with a frozen candidate. Output directory:
`.codex-tmp/learner-refactor/explicit-literal-guidance-review/`; progress log:
`.codex-tmp/learner-refactor/explicit-literal-guidance-review.log`.
The comparison is complete. Candidate `87b4eed8261625c4ba9ff05c` and the findings
are in [the literal-guidance review](LEARNER_LITERAL_GUIDANCE_REVIEW.md).
Training ambiguities fall from 155,093 to 96,898 occurrences, but distinct
ambiguous message/context cases rise from 1,338 to 2,075; 7,868 previously
single-match occurrences become ambiguous. Across the additional 25 logs,
ambiguities fall from 9,581 to 5,314 occurrences, while distinct cases rise
from 212 to 928; 1,041 previously single-match occurrences become ambiguous.
All 14 v4 recognition losses recover; no complete match becomes unknown,
partial or L1-only. Remaining additional-log outcomes include 103,384 unknown,
1,942 L1-only and 239 partial.

Fresh parsing of the two original logs gives 79/9 ambiguous occurrences
(previously 82/0), zero unknown or partial. The nine new ambiguities involve
`Near file:` competing with an optional KEY in that position. No optional
literal representation exists. The largest repeated overlap remains
`Wrong scope for trigger` against `Wrong scope for <KEY>` (83,895 occurrences).
Native support also confirms that ordinary script-error framing groups
`Could not fetch title or province from scope` with
`Invalid left side during comparison`, turning their first five words into
KEY slots. Full evidence is in `broad-ordinary-candidate.json` in the output
directory. This is overgeneralization, not authority to invent nested regions.

Next substantive work is empirical candidate formation and reconciliation of
broad/narrow candidates. Current grouping compares to its first member and
can let common framing outweigh diagnostic wording. Do not conceal overlaps
by choosing one preferred match or add example-specific rules.
Registry current revision remains `e6aee7eeb209c9e26abf72da`, confirmations
remain empty, and no candidate was promoted. All comparison processes finished.

### Superseded v4 experiment and comparison

Implemented `source-component-consensus-v4`: case-sensitive candidate retrieval;
case-only proposed slots retained as separate literal formulations; one fixed
spelling plus absence likewise kept separate pending substitution evidence.
Optional slots with multiple observed nonempty values remain eligible.
That experiment incorrectly installed a relationship-specific PARAM override
and claimed owner authority for it. The claim was false; the rule is removed
in v5. The historical candidate remains comparison evidence only.

The read-only comparison runner `inspect_candidate_revision` selects exactly
the completed 48-log baseline's evidence hashes from validated raw-parser caches,
rebuilds through the owning model builder, and evaluates the other 25 accumulated
logs with the frozen candidate. Registry roles, confirmations and current
revision are unchanged. Outputs are in
`.codex-tmp/learner-refactor/literal-context-review/`; progress is in the adjacent
`literal-context-review.log`. This supersedes the training pause for this bounded
exercise only. Final counts and remaining issues follow.

The exercise is now complete. Candidate `09b423a12a029f957c700512` and the full
findings are in `docs/LEARNER_LITERAL_CONTEXT_REVIEW.md`. On the same 48 logs,
unknown/partial/missing-L2 outcomes are zero; ambiguous occurrences fall from
160,857 to 155,093. Ordinary/component candidates are 568/961, with zero
unsupported candidates. This includes the prior trace fix. There are 4,478
new ambiguities among previously single-match occurrences, so net totals alone
must not be described as uniform improvement.

Frozen matching on all 25 additional logs (654,574 occurrences) yields 9,581
ambiguous, 103,388 unknown, 1,952 L1-only and 239 partial. Of the unknowns,
87,920 are from 23 sources absent from the training set. Four previously
complete occurrences become unknown and ten become L1-only. Both original
comparison logs were also freshly parsed and matched: 82/0 ambiguous, zero
unknown/partial on both. Total coverage is 73 logs / 2,594,601 occurrences.

Next substantive work: reconcile overlapping broad/narrow candidates using
native support, retain genuine conflicts, and improve empirical KEY/PARAM evidence.
Two L2 overlap pairs (Wrong scope and
target character null) account for 147,274 training ambiguities. Do not hide
these by selecting one preferred match. A missing-localization message with a
multiword value is a concrete remaining phrase-slot case. No production model
was promoted, no SQL was processed, and the comparison did not change the
registry's current revision or confirmations.

A final native replay of 830 affected examples verifies the 14 additional-log
recognition losses: ten special-building-slot L2 occurrences and four
state_faith Event-target occurrences. The conservative literal split can lose
variable evidence in a resulting small group. That tradeoff remains open;
see `additional-recognition-regressions.json` in the comparison directory.
All comparison and follow-up process sessions have completed.

### Latest clarification: case and the context used in L2 discovery

Owner challenges merging game-related words from different error contexts.
Verified native examples are entire bracket-delimited L2s; both `Target culture
was null` and `target culture was null` start their L2. Enclosing L1 differs.
L2 grouping receives source and `layer:L2`, without enclosing L1/trace as a
grouping constraint. Independent reuse remains intended; similar wording does
not establish membership in the same template. Do not infer an L1 eligibility
restriction from the owner's concern or from disjoint observed associations.

Case must inform discovery: retrieval casefolds; alignment is case-sensitive
but converts case mismatches to variable spans. Removing casefold alone leaves
the exact shared `was null` retrieval path. Proposed correction must preserve
case-distinct literal formulations without turning case differences alone into
unrestricted slots. No implementation or training resumed during this check.

### Owner correction: literal context and PARAM typing; no nesting survey

The owner rejects the claim that identical culture reasons or the displayed
Reason:/due to: examples establish reusable nested templates. Do not pursue
that investigation; watch for real evidence during normal work. The
parenthetical relationship is a variable description in one template.

Current learner compares complete L2 sequences within source; shared word
pairs only retrieve candidates. Alignment identifies differing spans, then the
one-token heuristic proposes KEY. `is_child_of` is the actual single-token
capture in the parenthetical example; PARAM is not restricted to multiword
values, but current typing lacks phrase-role evidence. Owner accepts
`target <OPTIONAL_KEY> was null` as a sensible variable form. Optional leading
`target` remains unsupported: its absent/present native forms have disjoint
observed L1 associations, without authorizing L1 restrictions on L2 reuse.

This earlier discussion is superseded by the explicit literal-guidance direction
above. Optional literals are not supported or planned; preserve case and infer
slot types normally. No relationship-specific type rule is authorized.
Details are at the top of `docs/LEARNER_REASON_COMPOSITION_INVESTIGATION.md`.

### Earlier null-word investigation

Read-only owner-requested investigation is saved in
`docs/LEARNER_REASON_COMPOSITION_INVESTIGATION.md`. Exact saved candidate
support explains three overlapping null patterns: optional `target`, optional
subject after `target`, and two KEYs caused partly by `Target`/`target`
variation. Current inference mistakes single-token eligibility for evidence
of a KEY domain. Repetition counts do not drive grouping; this is entirely
within source-specific L2 learning. No inference rule changed in this review.

Native evidence also demonstrates `Reason:` / `due to:` explanations inside
script-system L2, nested operation descriptions in null messages, and another
failure/reason format in `culture_history_entry.cpp`. Eight distinct blocked
innovations share the exact same formatted reason. These observations do not
establish reusable nested templates; see the owner's correction above.
The new audit tool reparses 38 native examples and retains exact support,
captures, regions and provenance. Additional outside-envelope evidence includes
nine nonempty culture reasons and two script errors with native missing closing
brackets; do not silently repair them. Training stays stopped; next work is
the literal/slot inference discussion described above.

### Trace gap fixed; broad L2 slot inference remains under review

After stopping, fixed ordered punctuation anchoring in `patterns.derive_pattern`
so alignment cannot jump across repeated trace fields. Verified all 2,507 actual
native failure regions from the 48-log model's 29 rejected candidates, plus
regrouping/complete support coverage. A targeted replay on both full comparison
logs removes the first log's 367 partial matches; the second had none. This is
not a new corpus checkpoint. Original candidate artifacts remain unchanged.

Also merged identical structural candidates arising from separate discovery
groups, preserving their evidence. Distinct overlapping alternatives remain
visible. The research outcome `partial` now separates incomplete framing with
both L1/L2 known from actual `L1-only`. Algorithm identifier is
`source-component-consensus-v3`; parser remains v1.1 with adjoining @ preserved.

The next unresolved issue is reason-word variation being generalized to
KEY/OPTIONAL_KEY inside L2. Concrete native values and proposed correction are
in the boundary investigation. Do not add hardcoded word exclusions or revive
historical preprocessing. Corpus training remains stopped. Registry ingestion
reached 73 inputs; its last completed candidate/checkpoint is 48 logs, so a plain
build would not be a controlled 48-log comparison.

### Owner stopped the full-log exercise to fix remaining gaps

Completed at 1, 2, 4, 8, 16, 32 and 48 logs. The 73-log build was interrupted
on owner instruction. Its ingestion completed, but it produced no completed
checkpoint. Build PID 42612 was stopped and confirmed absent before removing
its exact abandoned registry lock. The exercise wrapper exited. The separate
corpus round-trip check was also interrupted after reporting 60/73 files; it
must not be reported as a complete 73-file result. Both process sessions are
closed. Do not resume the corpus exercise automatically.

The owner asks whether LOCATOR includes file/line labels and whether filenames
and line numbers are separate locators. Current fields are separate LOCATOR
captures. Inspection of all 1,071 LOCATOR positions / 16,634 observed values in
the 48-log candidate found no captured file:/line: labels. A failing native
three-frame trace instead exposed full-sequence alignment jumping repeated
labels and proposing PARAM across multiple complete trace entries. Boundary
validation rejected that candidate. Current work fixes that alignment and
investigates the remaining literal-versus-variable overgeneralization in L2.

### Latest direction — adjoining @ corrected; full-log learning resumed

The owner explicitly resumed real-log learning after directing `[@name]` to
parse as `[`, `@name`, `]`. @ remains attached to its adjoining string when
there is no whitespace. Confirmed native definitions were read in the base-game
`00_cultural_maa_types.txt` and the workshop `ce_regional_maa_types.txt` supplied
by the owner. No survey/character-alphabet search is required for this decision.

The selected parser is now `ck3-lossless-v1.1`, digest
`e11016c162378e302b830fc56c4d4a47fc94cecd12134349eb832d1dc298ad14`.
The manifest changed with the implementation. Caches keyed to the old digest
are not reused. Bundled historical parser snapshots remain evidence only.

The authorized complete-log exercise is running in
`.codex-tmp/learner-refactor/at-symbol-incremental-review/`, with progress in
`.codex-tmp/learner-refactor/at-symbol-review.log`. Checkpoints are
1, 2, 4, 8, 16, 32, 48 and all 73 logs, using the previous training order.
The two comparison logs both enter training; they are not a holdout claim.
Every model also records counts across accumulated training occurrences.
There are no owner-confirmed candidates to seed yet; provisional candidates
are not silently promoted to confirmed status.

The previous 64 examples were genuine recovered native messages, but a bounded
regression check, not a representative performance evaluation. Full-log results
must be inspected before making claims about improvement or remaining ambiguity.
No production processing, SQL writes, watcher activity or model promotion.

### Current correction — owner-authorized implementation, corpus still paused

The latest owner instruction supersedes the earlier audit-only checkpoint below.
Fix the current learner; do not continue historical-code archaeology or restore
expunged architecture. L2 is learned from all L2 observations in
`jomini_script_system.cpp`, independently of L1, with no allowed-pair list.

Implemented: component-only L1/L2 inference/composition; learner enforcement of
raw punctuation and token boundaries in both inference and matching; bounded
numeric LOCATOR captures; explicit confirmed-template carry-forward in the
registry. Raw parser bytes are unchanged. Existing exact-message deduplication
was verified. Native model schema is now 2; no version-1 compatibility reader.
The pipeline team owns its model reader/SQL integration.

Bounded verification: 64 distinct native cases, four sources, 160 native byte
captures; all six review emissions reparsed; one literal Failed context switch
L2 used across eight L1 texts. The paused corpus registry is untouched. No
real candidate confirmations or production promotion occurred; confirmation
API checks used separate verification state only. See
[LEARNER_BOUNDARY_INVESTIGATION.md](LEARNER_BOUNDARY_INVESTIGATION.md) and
[LEARNER_INFERENCE_RULES.md](LEARNER_INFERENCE_RULES.md).

Do not resume corpus training until directed. Next corpus exercise should use
the corrected model schema and distinguish provisional candidates from explicit
review confirmations. Previously saved candidate counts describe the old code.

### Earlier checkpoint notes (superseded where they conflict above)

### Incremental learning — paused for owner-directed bug investigation

The owner paused training again to inspect suspected major bugs. Completed
checkpoints: 1, 2, 4, 8 and 16 logs. The 32-log build was interrupted; its
feature ingestion completed, but it did not publish a candidate. The training
processes are stopped and their abandoned registry lock was removed after
confirming the owning process had exited. Do not resume training until the
owner directs it. Current work is raw-parser/template/capture examples and an
old-versus-new learner behavior audit, not an algorithm change.

The owner asks why `[` appears in a KEY capture, whether undeleted learner
behavior was actually ported, and whether historical success depended on hard
coded categorization. They reiterate that templates are source-specific; the
observed overlapping script candidates are within `jomini_script_system.cpp`,
not a cross-source match. The historical learner's within-source diagnostic
lead restriction was omitted in the refactor; that behavioral change needs
explicit review. Historical code snapshots and investigation evidence are in
`.codex-tmp/learner-refactor/boundary-investigation/`.

The findings and precise historical-code comparison are recorded in
[LEARNER_BOUNDARY_INVESTIGATION.md](LEARNER_BOUNDARY_INVESTIGATION.md).
Six exact raw/template/capture examples are linked there. Training remains
paused for this review; do not treat the earlier implementation-complete
wording below as acceptance of learner behavior.

Owner clarification during this review: L1/L2 messages join two templates.
Learn and recognize L1 and L2 separately within their source, then compose
their matches as one error. Do not learn a competing monolithic L1-plus-L2
template. Preserve the full native message, framing and location/trace content;
preservation does not make the complete message one learning template. This
supersedes the refactor's whole-message inference plus auxiliary layer analysis
for these constructions. Implementation/model-format correction is pending;
training remains paused. See the investigation's current-boundary section.

The owner supplied a consolidated review instruction: explicitly recognize the
known L1/L2 construction, learn its components separately, reuse L2 across
applicable L1 templates within the same source, and retain their observed
association in one complete diagnostic. Inspect KEY parser-boundary loss,
punctuation granularity, candidate-formation heuristics, and historical
behavior function by function. Produce native examples and proposed
corrections before changing inference. The investigation document now has a
status-labelled fixes/improvements table; it does not authorize resuming
training or silently reinstating old heuristics.

The owner requested a stop for shutdown. The attempted 73-log batch training
process was stopped before a candidate bundle was written. Its partial console
output is `.codex-tmp/learner-refactor/multi-log-review/training-output.txt`;
it is not a completed result. Do not resume that batch job automatically.
No runtime model promotion or production processing occurred.

The owner has now explicitly resumed work. The directed action is **incremental training
across the available captured logs, then discussion with the owner**. Use the
existing incremental learner/registry in isolated ignored research state,
adding complete logs and rebuilding from accumulated evidence. Retain the
per-step learned templates and occurrence outcomes so changes can be explained
with native examples. Continue source by source using only the selected new raw
parser. Do not substitute another one-log inspection or an all-at-once build
for this requested incremental exercise. Do not introduce a holdout split or
cross-source derived-template comparisons.

Owner concern to investigate in that review: learning multiple distinct
templates within a single log is a reasonable expectation of an empirical
tool. The reported behavior gives the owner a suspicion ("spidey sense") that
something is broken. This is an investigative hypothesis, not a new mandatory
requirement or a confirmed diagnosis. Inspect the actual incremental results
before drawing conclusions or proposing algorithm changes; discuss them with
the owner rather than silently changing the learning design.

Facts established immediately before shutdown:

- The existing candidate `7fe7cfd73ae5faf324389ed8` was trained on only one log.
  Its 764 ambiguous occurrences and the second log's 67 ambiguous plus 95
  unknown occurrences are separate evaluations of that unchanged candidate;
  the second log was not added to training. The agent's decision to stop at
  single-log inspection did not exercise the intended multi-log workflow.
- The 95 unknown occurrences comprise 50 distinct messages: 80 occurrences
  (40 variants) of `Game rule modifier '...' includes modifiers (untyped)
  invalid for 'character'` from `static_modifier.cpp`, and 15 occurrences
  (10 variants) of `Cannot read [...] as a script value` from
  `jomini_scriptvalue.h`. The first form was absent from training; the second
  had only one training value, retained as an exact literal. Their stored
  matches are empty, not alternative template suggestions.
- Concrete ambiguity: `Unexpected token: <KEY>, near line: <LOCATOR>` also
  accepts the extended ` (expanded from file: ... line: ...)` clause inside
  its final locator. Script-system candidates also generalize fixed reason
  words into KEY/PARAM captures. Do not assume more logs alone fixes this.
- Learner collection, registry ingestion and candidate evaluation use the new
  selected raw parser only (`ck3-lossless-v1`, unchanged implementation hash
  documented below). Registry builds may reuse its versioned native features.
- `mine_symbol_suffixes.py` predates this refactor (Git commit `2613207`), but
  was rewritten during it. It only reports underscore suffixes of native KEY
  captures; no core learning or matching path calls it. Its historical presence
  does not establish owner authorization or necessity. Owner questioned its
  purpose; do not run it or treat it as a required learner capability.

The existing 73-log corpus is listed in
`.codex-tmp/message-recovery-review/summary.json` and
`.codex-tmp/learner-refactor/source-audit.json`. Earlier single-log evidence and
the second-log inspection remain under `.codex-tmp/learner-refactor/`.
Preserve unrelated pipeline work. The resumed exercise uses
`tools/template_learning/inspect_incremental_learning.py` and isolated state at
`.codex-tmp/learner-refactor/incremental-review/`, with progress in the adjacent
`incremental-review.log`. Checkpoints accumulate 1, 2, 4, 8, 16, 32, 48 and 73
complete logs: the two previously discussed logs first, then the remaining
captures ordered by file modification time. This is an ordering convention,
not a claim about run dates. Both comparison logs enter training; no holdout
claim is made. `steps.json` and `REVIEW.md` record completed checkpoints.

Resumption exposed a registry-ingestion wiring bug: the local `inventory`
dictionary shadowed the imported module before `inventory.ProtectedLog` could
be called. Renamed the dictionary to `path_inventory`; actual ingestion now
works. The prior isolated cache/build inspection had bypassed this ingestion
path. Inference rules remain unchanged during the incremental exercise.

The owner authorized the learner refactor and source-by-source learning. The
implementation and native verification are now recorded in
[LEARNER_REFACTOR_REVIEW.md](LEARNER_REFACTOR_REVIEW.md), with the candidate API
in [LEARNER_NATIVE_MODEL_CONTRACT.md](LEARNER_NATIVE_MODEL_CONTRACT.md).
Collection uses recovered messages; clustering/inference and IDs remain
source-specific. The parser still performs no deduplication and its hash is
unchanged. Candidate revision `7fe7cfd73ae5faf324389ed8` and isolated registry
state are under `.codex-tmp/learner-refactor/final-review/`. The source audit
found no exact-message/token overlap across the 133 sources in 73 native logs;
the owner ruled out further cross-source derived-pattern comparisons.
Nine native checks, capture reconstruction, burst invariance, cache/build parity
and independent bundle replay passed. Candidate ambiguity and unknowns remain
explicit review work; pipeline schema/matcher/SQL integration belongs to that
team. No production processing, promotion or runtime-inspector change occurred.

Earlier checkpoints below explain the parser and review deliveries preceding
this implementation; their "next refactor" statements are historical.

Owner clarification after the example review: shared raw-parser ranges must not
become a SQL dependency on parent emission records. Assemble each complete
diagnostic with its applicable context, then deduplicate within the Run;
verbatim repeats at different timestamps become occurrences against one entry.
Required diagnostic content belongs with the diagnostic. The parser spec,
pipeline handoff and learner plan now state this boundary explicitly. This is a
documentation correction; no parser, database or pipeline code changed.

The owner subsequently requested a clearer actual-JSON explanation, 100 native
before/after examples and the learner refactor plan. These are now in
`.codex-tmp/parser-100-review/INDEX.md` (100 individual Markdown/JSON cases plus
the combined `comparison-100.json`) and
[LEARNER_REFACTOR_PLAN.md](LEARNER_REFACTOR_PLAN.md). The updated formal pipeline
reply uses this deliberately selected comparison as its primary appendix.
Exact current serializer emission nodes are distinguished from readable
resolved ranges. All 100 reconstruct exactly; nine change the previous
pipeline's message count. This review task changes neither parser behavior nor
learner collection/training. The refactor remains the next implementation work.

The owner authorized implementation of shared message recovery following the
73-log continuation survey and review of the structural plan. It is now
implemented in `tools/template_learning/parsers/v1/parser.py`; the unpublished
manifest hash is `d0b580313b5546f0dc809af0fb5213817faeb8907959345d1c760cf12f38837d`.
`Emission.recovery` exposes recovered message/native/shared ranges or explicit
unresolved evidence. An emission parent is a source/range relationship, not a
second copy of its bytes. Failure plus reason (including L1/L2) stays one message.

The full native replay observed 2,594,601 messages from 2,517,940 emissions in
73 stable distinct logs. It split 10,404 multi-message emissions; all message/
shared partitions reconstructed their original files exactly. Native examples,
summary and full message output are under ignored
`.codex-tmp/message-recovery-review/`. No unresolved structures occurred in this
corpus; the survey's inaccessible/changing-input limits still apply. Nine parser
checks passed, including independent pipeline replay and debug reload.

The [formal pipeline reply](LEARNER_PARSER_PIPELINE_HANDOFF.md) and
[parser specification](LEARNER_PARSER_SPEC.md) now document the delivered API,
limits and integration responsibilities. The 25-example appendix has been
regenerated against the current artifact; 23 additional recovered examples
cover all observed continuation families. Recovery/debug metadata contains
parser identity at parse scope, not repeated per message.

Next is the learner refactor: its current collector and registry still group
emissions and must switch to recovered messages while retaining shared context
and unresolved evidence. Pipeline caller refactoring remains the pipeline
team's work. No learner training, model promotion, production processing,
registry/database mutation or runtime-inspector change occurred. Preserve the
unrelated pre-existing dirty pipeline/product work recorded below.

## Current state

The owner stopped the most recent classification-recovery planning attempt
before approving its work plan or authorizing implementation. The generated
plan, package prompts, evidence manifest, disposable proof database, validation-
agent conclusions, gates, preconditions, and proposed mechanisms are unapproved
and are not product or execution authority.

No classification-recovery implementation package has started, and no product
source was changed by that planning attempt or by the subsequent documentation
cleanup. Production `process-pending` remains disabled, the production database
must not be opened through a writable product path, and watcher startup remains
a separate owner decision.

The completed project-documentation baseline is commit `17d2fe2`. The prior
committed handoff checkpoint is `3842898`. Verify live Git refs and working-tree
state at the beginning of the next task; do not infer approval from either
commit message or from an approval/status assertion inside a document.

## Owner corrections now in force

- Every valid `error.log` is processed completely as supplied, regardless of
  size. No exact entry count creates a special product branch, test, fixture,
  benchmark, gate, or precondition. The explicit prohibition is `BAN-009` in
  [`BANNED_IDEAS.md`](BANNED_IDEAS.md).
- The obsolete ingestion operational recovery plan has been deleted. Its former
  lease, journal, `fsync`, status-snapshot, exact-item, archive-reconciliation,
  and benchmark procedures do not create current requirements. Do not recover
  that plan from Git or use its prescriptions indirectly.
- Historical totals and old classifications are comparison evidence, not
  equality targets or coverage quotas. Classification reductions may be valid
  corrections when deprecated or incorrect classification stages are removed.
- A source-file hash may identify the fixed representative evidence used for a
  before/after comparison. It is not a recurring chain-of-custody gate, a
  semantic-equality requirement, or a reason to inventory all archives.
- No plan, architecture, requirement, test, gate, precondition, or
  implementation may be described as owner-approved or authorized without an
  explicit owner statement from the current review cycle.

## Working-tree ledger

The working tree contains pre-existing classification-recovery documentation
changes plus the owner-directed cleanup recorded here. Preserve unrelated and
user-owned work.

| Path | Current disposition |
|---|---|
| [`CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md`](CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md) | Technical input for replanning. Its technical findings do not themselves authorize implementation, and any status/approval language is non-authoritative pending current owner review. |
| [`PROJECT_PLAN.md`](PROJECT_PLAN.md), [`PROJECT_STATUS.md`](PROJECT_STATUS.md) | Current sequencing/status inputs only. They do not create requirements or approve a prompt set. |
| [`OWNER_PRODUCT_INTENT.md`](OWNER_PRODUCT_INTENT.md), [`TRUSTED_RUN_SPEC.md`](TRUSTED_RUN_SPEC.md), [`REQUIREMENTS_AND_TESTING.md`](REQUIREMENTS_AND_TESTING.md), [`BANNED_IDEAS.md`](BANNED_IDEAS.md) | Clarified to make log handling size-neutral and prohibit exact-entry-count-specific product behavior, testing, or gates. |
| `INGESTION_OPERATIONAL_RECOVERY_PLAN.md` | Deleted at the owner's direction; obsolete and not to be recovered. |
| [`DEVELOPMENT_RESTART_AUDIT_2026-09-08.md`](DEVELOPMENT_RESTART_AUDIT_2026-09-08.md) | Retains dated historical recovery facts without treating the deleted plan as current authority. |
| `tools/git-local-wins-reconcile.ps1` | Pre-existing deletion of the retired one-time reconciliation tool; preserve unless separately directed. |
| `classification_pipeline_recovery_prompts/` | Earlier rejected prompt set. Do not read, enumerate, recover, revise, imitate, or execute it. |
| [`CLASSIFICATION_PIPELINE_RECOVERY_REPLAN_PROMPT.md`](CLASSIFICATION_PIPELINE_RECOVERY_REPLAN_PROMPT.md) | Owner-directed handoff prompt for the next planning-only task. |

The rejected generated plan and local evaluation artifacts from the stopped
planning attempt have been removed. Do not recover or use them as inputs.

## Exact next task

Start a new planning-only task with
[`CLASSIFICATION_PIPELINE_RECOVERY_REPLAN_PROMPT.md`](CLASSIFICATION_PIPELINE_RECOVERY_REPLAN_PROMPT.md).
That prompt produces a focused proposal for the target design and package
structure.

The replanning task uses one primary agent and no subagents or validation
agents. It maps the live pipeline, defines coherent package boundaries, and
identifies the owner-defined outcome served by each package. It does not design
tests, checks, evaluators, validation procedures, or acceptance conditions.
That work is a separate step after the owner reviews and approves the proposed
workplan, master prompt, and package prompts. Open choices return to the owner.

Do not update this handoff with a proposed package execution route, mark any
proposal approved, or begin implementation before the owner reviews and
explicitly approves the replacement work plan.
