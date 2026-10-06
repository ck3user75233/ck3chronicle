# Pipeline receipt and cutover preparation — 2026-10-05

**DATABASE REPLACEMENT COMPLETE.** Production has 31 freshly ingested Runs, all
on the new model. The [replacement receipt](#database-replacement-complete--2026-10-05)
records the safe backup/switch, archived former store, current services and verified
natural lifecycle. Earlier staged/deferred/pending statements below are historical.

## Original Pipeline receiving record

**Receiving completed with Reporting defects; R1 remains an unresolved reporting
acceptance issue and live activation remains unauthorized. R2 is an owner-accepted
nonblocking limitation, not an activation gate.** The authenticated package is `4ac4e8ee92346e6d14eacfbf`,
learner v61 / parser v1.8. No production selection, configuration, database,
watcher or handler was changed. No historical refresh, reset, commit or push was
performed. The existing prohibition on a live restart remains in force.

This receipt supplements the [final Learner handoff](HANDOFF.md), whose exact
artifact identities remain authoritative. The consultant disposition is the
delivered 08C correctives, as confirmed by the owner; neither the consultant ZIP
nor `parser-substitution-simplified` was used.

**Owner clarification after receiving — single-Run timestamps:** missing captured
source time is permitted. All nonchronological operations must work normally,
including Run-ID listings, searches for all Runs with a given error message,
and single-Run reports. Only chronological placement is unavailable. The session-55 CLI rejection
recorded below is now tracked as Reporting defect **R5**, not an accepted reporting
prerequisite. The [fresh Data Intelligence repair prompt](REPORTING_RECEIVING_REPAIR_PROMPT.md)
covers R1, R2 and R5; R2 remains nonblocking. No repair or new verification is
claimed by this clarification; original receipts remain unchanged.

All receiving evidence is ignored under
`.codex-tmp/pipeline-receiving-20261005` (**P** below). It contains scripts,
receipts, disposable captures/database, report results and runtime logs. These
are actual genuine-input checks, not synthetic acceptance tests.

## Timestamp provenance inspection after owner clarification

Read-only source inspection found no runtime fallback that invents missing
`error_log_source_modified_at`. Capture obtains it from the original file's
validated stat; ingestion passes supplied metadata into `facts` unchanged and
storage serializes those facts unchanged. Manual protection records its actual
`captured_at` without adding an original source time. Processing/Run-ID basis and
report generation have their own explicitly named clocks. Retention skips
unavailable capture times rather than substituting filesystem dates.

The harvester, ingestion, repository, retention, Reporting analysis and Reporting
CLI files were byte-compared: current source, delivered corrected wheel and
`installed-corrected` match for all six modules. The retained session-55 witness
has no source-time key, while independently recording capture/processing times
and `identity_basis: processing`. This inspection is not a new live-process check
or an ingestion/report execution. No runtime code or stored facts were changed.

Older test-only timestamp manipulation exists: two cases in
`tests/test_capture_source_mtime_requirements.py` shift disposable filesystem
times, and `.codex-tmp/pipeline-source-mtime-receiving/verify.py` supplies a
conflicting 2001 date to check duplicate rejection without overwriting stored
facts. These do not fill missing production timestamps. They were inspected,
not executed, and historical evidence was preserved. R5's improper eligibility
filter remains the assigned Reporting repair.

## Authentication and installed execution

- All **318** paths in Learner's final delivery hash inventory matched at intake.
- All **556** installed code/resource files matched the corrected wheel, in
  `combined-release-20261005/installed-corrected`. The application wheel hash is
  `362b09b2d553f7610a1cf5e8b848000af610ef48f4c8c1b5bba739223586316b`.
- Running its Python with `-I -B` from **`C:\Windows`** loaded the selected
  package, parser, decoder and all 394 contract definitions from installed
  resources. Module paths exclude checkout development modules. See
  `P/outside-checkout.json`. Handler/report execution used a separate directory
  containing explicit `config.toml` and disposable evidence; the application's
  working-directory configuration requirement is preserved.
- Corrected decoder hash is
  `c31c8d6089850fb01d146b420e1c7364d86cb9287180f2e9f451861c21feb039`.
  The supplied, locally repacked chardet 7.6.0 dependency and installed `pip check`
  passed. Known-UTF-8 processing did not import chardet in the receiving client;
  the authenticated fragment call graph uses direct UTF-8/surrogateescape only.
- `decode_fragment` returns a plain `str`. It has no warning/status/header
  metadata to aggregate. The four genuine ingestion results returned no warnings.
  Preserved bytes survive as surrogate code points in native strings, ASCII JSON
  escapes in SQLite/IPC, and exact bytes on inverse encoding. They are not stored
  as display `\\xHH` strings. No warning table/schema or physical-file admission
  step was introduced.

The handler's successful new Runs report model `789219fdbd81c8dab950bc93`, package
manifest pin `839548e8c8143e01b63059848557dc94e9fe66f5e1924f6026442f7331a8ba9f`,
parser `ck3-lossless-v1.8` /
`0357b8d1c342c546452ed8f294405bfe41c86c7116eca51eddf8bc5b67984135`, matcher v3,
selector `complete-assignment-v2`, classifier v8 and contract v1. Actual ingestion
application lineage is
`application-source-sha256:6424a090a308f0870d880d38e368efa89358b750267943d15960ccd0e183c475`.
This is ingestion's existing whole-application source fingerprint, distinct from
Learner's narrower probe fingerprint. It is computed from disk, not a digest of
in-memory imported code: the same string in an old long-running handler does
**not** prove that process loaded the new renderer. The new disposable hosts were
launched by the authenticated installed interpreter on unchanged installed files;
stored lineage and correlated completed-ingest logs establish their package use.

## Genuine handler/storage results

Explicit disposable store:
`P/context/runtime/disposable/ck3chronicle-schema3-20261005T060419Z.sqlite3`.
Each log was ingested once; later checker corrections reused the accepted Run.

| Genuine input | Disposable Run | Package | Supported | Provisional | Native review |
|---|---|---|---:|---:|---|
| Session 55 | `20261005-XH88PI` | new | 99,991 | 12 | none; all 44 preserved-byte occurrences retained |
| Original `20261003-IS3QON` capture | `20261005-BND9AS` | new | 59,223 | 90 | none |
| Original `20261002-2PVVSE` capture | `20261005-OSPK8G` | new | 12,723 | 88 | 2 unmatched + 1 unresolved recovery; 418 exact bytes |
| Original `20261003-D3N7ZQ` capture | `20261005-DQT13M` | previous | 1,775 | 63 | none; mixed-package control |

The new-package scope is **171,805 emissions / 172,130 observed units**:
171,937 supported, 190 provisional, two unmatched and one unresolved. Counts
match Learner's retained comparison for the corresponding captures and installed
session-55 receipt. The valid 73-log parser/full-corpus comparison and 20-Run
comparison were authenticated and reused, not repeated as a Pipeline campaign.

Public `HandlerClient` reads returned **28,283** new-package compact records.
All **29,723** rendered representative regions and **58,091** present bindings
match their original byte slices exactly. Including the old-package control:
29,349 records, 31,427 regions and 61,548 bindings. These counts describe compact
representatives; occurrence totals are reconciled separately. Complete-file
hashes and source bytes are unchanged. Supplied genuine capture facts and ordered
playset members compare equal. Session 55 has no retained capture metadata or
producer playset, so ordinary manual protection correctly records unavailable
playset/source-mtime facts rather than inventing them.

Review manifests, routing/count totals, hashes and every original/shard emission
span agree. The 418-byte shard retains the three native units, including the
unresolved one. Requesting the already stored IS3QON hash with the other real
package returns `NOT_COMPLETED` with its original Run, without new processing.

Source inspection confirms the existing route: protected bytes → package parser
→ classifier/bindings/contracts → accumulator/review preparation → handler worker.
Parsing and classification precede `write_run`; the transaction starts after
record validation, complete accounting and review staging. Empty manual/captured
files are rejected by ingestion. A nonempty log without the expected initial CK3
header raises in the parser; its existing framing/BOM behavior was unchanged.
This is separate from fragment decoding, which adds no header admission.
Unresolved/native-input outcomes are routed to review; unexpected parser/binding/
integrity exceptions propagate to `NOT_COMPLETED`, before any prepared Run write.
Coverage/count reconciliation rejects missing emissions or inconsistent totals.
Unrepresented read/parse/commit/transport failures were inspected, not injected
or declared dynamically verified. No empty-log success or silent partial ingest
was observed on genuine evidence.

## Defects and receiving ownership

| ID | Demonstrated impact | Accountable receiving owner and disposition |
|---|---|---|
| R1 | `reporting.analysis.template_text` treats every non-literal part as a slot. Schema-6 `kind: repeat` lacks `prefix`, raising `KeyError: 'prefix'` before filtering/formatting. Ordinary frequent reports fail in JSON, HTML and text, exit 1, for both new genuine captured Runs. IS3QON has 1,012 affected stored records / 54,967 occurrences in 17 definitions; 2PVVSE has 1,136 / 8,003 in 19 definitions. These are overlapping template inventories, not additive distinct definitions. | **Data Intelligence / Reporting (08A.1/08B): open receiving repair.** Consume the delivered contract's repeat/formatted-literal layouts in template text and query/presentation paths; recheck these actual stored Runs and all report formats. Pipeline did not replace Learner/parser/matcher code or silently broaden into Reporting implementation. End-to-end acceptance is held. |
| R2 | Genuine session-55 text read back from SQL reconstructs exactly, but installed JSON (`ensure_ascii=False`), HTML and text helpers raise `UnicodeEncodeError: surrogates not allowed` at UTF-8 export. A failed write can leave a created/truncated output. | **Data Intelligence / Reporting (08B): open bounded display/export repair; owner-accepted nonblocking limitation.** Owner clarification permits this known limitation for the release/activation decision; do not hold activation solely for R2 or ask again for its disposition. Preserve native processing/storage strings when repairing the human export boundary; verify the genuine stored witness and output-failure handling. No ingestion-warning schema is requested. This is not a claim that affected exports pass. |
| R3 | The wheel bundles the previous selection's `candidates/68f1ae5db205ab46afef9c4d`, but only `releases/` distributions are installed. Default loading fails with missing `manifest.json`; explicit catalog loading of both packages succeeds. | **Learner/application packaging: recorded upstream defect. Pipeline: explicit deployment selections prepared.** The new proposed selection already uses `releases/`. `P/rollback-installed-selection.json` comes from the existing catalog API, authenticates the same previous package/pin and uses `releases/68f1ae5db205ab46afef9c4d`. Never use the checkout's previous selection verbatim as an installed rollback. No retained package or delivered wheel was edited. |
| R4 | `syntax` deliberately supports only the previous package/model. The new-package CLI correctly exits 2 with `invalid_query`; there is no new-model syntax count. | **Reporting selector receiver: explicit remaining work.** Receive and verify selectors against the new model and real evidence before advertising this preset. Keep old package-specific syntax reports scoped to old Runs. This is not a request for new diagnostic taxonomy. |
| R5 | The recorded session-55 named-Run CLI request exits 2 before export because source-log modification time is absent, including with `--no-history`. Source inspection also shows `DiagnosticAnalysis.list_runs` filtering ordinary listings through chronology before pagination; `investigate` selects explicit IDs from that filtered list. The underlying handler listing includes missing-time Runs. | **Data Intelligence / Reporting: owner-directed repair.** Only chronological operations require time. Run-ID listings, all-Runs message searches, ordinary queries/counts and exports must include otherwise matching Runs regardless of missing time. Repair discovery/selection/search, retain unavailable timestamps, and verify genuine session 55 through listing/search/public analysis/installed CLI. Original helper-only R2 evidence remains valid within its recorded scope. |

`P/report-layout-defects.json` contains exact definitions; `P/report-cli-results.json`
contains executed commands/exit statuses; `P/stored-surrogate-export.json` and
`P/surrogate-stored-witness.json` establish R2 from actual stored values.
At original receiving, full session-55 Run CLI reporting exited 2 earlier because
the source-log mtime was unavailable, including with `--no-history`; no timestamp
was backfilled. R2's stored helper check is therefore distinguished from full CLI
acceptance. The owner subsequently identified that selection restriction as R5:
repair the standalone report path and verify it without manufacturing metadata.

The old-package mixed-store control exports successfully in all three formats.
Package-scoped Run listing retains independent lineages, excludes the other
package from history and reports missing source chronology as unavailable.
Absent classifications across different packages are not presented as zero or as
a cross-package trend. New-model query/report acceptance is blocked by R1.

Verification-tool corrections are retained: the first setup omitted the parent
directory required by `create_database`; no database was created on that attempt.
The first byte checker zipped display order against API region order; it compared
`prefix` with `body`. Matching by region name fixes the checker, without changing
product code or repeating accepted ingestion. `receipt-harness-region-order-failure.json`
and its log preserve that failure. The subsequent R1 failure is a product defect,
not another checker issue. Source logging ownership check passed; runtime code and
logging configuration were unchanged. Only disposable handlers were stopped.

## Live observations and database recommendation

At **2026-10-05 06:23:52 UTC** (14:23 Hong Kong), a fresh heartbeat identified
watcher **30816**, observing CK3 **49852**, whose start was observed at
06:00:41 UTC. Existing handler **23252**, worker thread 19548, instance
`ca3faf45a4514e5cab542769c2a3c70f`, answered read-only public operations.
Watcher/handler launchers are 24968/9000; process start times are recorded in
`P/live-processes.json`. CIM was denied and psutil unavailable; the successful
fallback was ordinary `Get-Process`, heartbeat, existing hello and public reads.
No service was restarted to inspect it.

Latest completed genuine Run **`20261005-ZEHL9K`** was protected at 04:48:03 UTC
and ingestion completed at 04:48:13 UTC. The capture/request correlation is in
`P/live-observation.json`. Its loaded processing lineage is the previous package,
parser v1.7 and matcher v2. Read-only reporting with the final installed application
succeeds for **5,689 occurrences / 2,723 distinct records** (`P/live-report.json`).
This is fresh evidence that capture/ingestion has operated today, not evidence of
the new package's live activation. The current CK3 session remains running.

**Keep the existing database for new unique logs.** It has 29 stored Runs. All 29
have a readable matching original in configured pending storage, with playset
availability inventoried. No readable unstored complete capture was found.
Twenty-two older pending directories are inaccessible; their contents and hashes
remain unknown. Permissions were not changed. No crash-folder principal logs were
searched and no capture facts reconstructed. This is a bounded operational pending
inventory, not a newly commissioned archive/source-coverage campaign.

A reset would discard current Run identities, processing lineages, results and
review/playset relationships unless backed up; ordinary re-ingestion would produce
new results/identities. Even with 29 readable originals, equal reconstruction of
old processing history is not promised. Unknown older directories remain unknown.
No reset is needed. Global `runs.log_sha256` uniqueness still rejects old hashes
under another package; same-Run replacement is documented but undelivered.

Physical-source encoding/header coverage gaps and the one undetermined source
remain disclosed source-reading limits, not ingestion gates. No detector research
or source-completeness campaign was added. No new live capture was manufactured;
post-switch loaded lineage and a naturally completed new lifecycle remain pending.

## Cutover

Use [the concrete cutover runbook](PIPELINE_CUTOVER.md). The source of the approval
requirement is the owner's current assignment (no live pin switch or restart),
reinforced by the final handoff and CURRENT_HANDOFF's unresolved explicit restart
prohibition. The owner has clarified that R2 is a nonblocking known limitation;
that disposition neither resolves R1 nor authorizes operations.
Recommended decision: retain the database and repair/re-receive R1 before activation;
alternatively the owner can explicitly accept R1's impact and authorize the concrete
switch/restart. Do not ask again for R2's disposition. A repaired application
is a new artifact requiring its own installed receipt; do not relabel this wheel.

## Reporting repair delivered — 2026-10-05

**READY FOR PIPELINE RECEIVING for R1, R2 and R5.** Data Intelligence supplied a
new application wheel; this is not production acceptance or activation. R2's
owner-accepted nonblocking disposition remains unchanged. Evidence root **R** is
`.codex-tmp/reporting-repair-20261005/`; P and the original wheel/installation are
unchanged. Forty-nine original receiving evidence hashes were reauthenticated.

| Defect | Root cause and delivered correction | Genuine before/after result |
|---|---|---|
| R1 | Template presentation treated every non-literal as a simple slot. It now traverses declared repeat layouts and shows their minimum/alternatives without selecting a fixed count. Formatted literals retain declared display text; bound messages still use the unchanged contract renderer. | Original installed reports reproduced exit 1 for BND9AS/OSPK8G in all three formats; repaired installed reports exit 0. Exact affected inventories remain 17 definitions / 1,012 records / 54,967 occurrences and 19 / 1,136 / 8,003. Complete diagnostic totals are 59,313 / 3,211 records and 12,811 / 3,315 records. Template exact/partial, typed repeated-binding and native message filters pass, including 20-entry and 18-entry witnesses. All 394 delivered definitions render. |
| R2 | Native byte-preserving surrogates were written directly as UTF-8. JSON now uses reversible surrogate escapes while retaining valid Unicode. HTML/text reuse the decoder's existing display rule, extracted as `display_text`, and label `\\xHH` as representation; copyable identity JSON remains native/reversible. Both main and appendix are encoded before either file is opened. | Original stored-value helpers reproduced `UnicodeEncodeError` and created/truncated files. Repaired helpers and actual named-Run CLI JSON/HTML/text pass, including all 44 stored byte-bearing occurrences with/without optional history. JSON values equal handler-returned records; inverse encoding still matches original source bytes. Valid text such as `Agmánd` remains unchanged. |
| R5 | Ordinary discovery/selection used chronology as eligibility. Package membership is now separate; listing includes missing-time Runs before pagination, in explicitly nonchronological Run-ID order. `search_runs` queries every package Run before matching pagination. Named reports retain selected results when optional history cannot be placed. | XH88PI remains without source time and returns all 100,003 occurrences / 21,757 records. Ordinary lists and genuine all-Run message search include it. The stored `Invalid supported_version` message for `mod/ugc_2218867072.mod`, line 7, matches BND9AS, OSPK8G and XH88PI, independently established from handler records. Pagination/counts pass. No relative positions, novelty or zero historical observations are invented; chronological latest excludes the unplaceable Run. Wrong-package and unknown-Run errors remain explicit. |

The old-package DQT13M control retains 1,838 occurrences / 1,066 records and passes
all formats. History remains package-scoped. Native record digests and Run metadata
match before/after for all four Runs. No ingestion, registration, fabricated
history/timestamps, mock clients or injected failures were used. Existing storage,
review and full-corpus receipts are inherited, not rerun or newly claimed here.

Verification receipts and limits:

- `R/original/receipt.json`: reproduction through the unchanged original installed
  application, including original root-CLI failures and successful old control.
- `R/installed-first/receipt.json`: 35 genuine-data checks and 28 CLI invocations;
  final analytical/export modules are byte-identical to this first repair build.
  The final build additionally corrects the root `runs` help text.
- `R/installed-final/receipt.json`: final-wheel installed root CLI, 24 report
  exports, two listings and two syntax checks; output contents inspected. New syntax
  is the expected exit-2 rejection; other commands exit 0. Includes verbose
  HTML appendices, normal named reports, `--no-history`, and targeted byte exports.
- `R/focused-final/receipt.json`: final public analysis and six installed exports
  of genuine native-byte/repeated-binding filters, plus exact date-literal
  provenance and original session-55 hash checks. `R/installed-pins.json` verifies
  all 394 definitions, import isolation, package/parser pins and installed rollback.
- Session 55 has no recorded playset: its source appendix honestly has no source
  excerpts. No genuine byte-bearing current-source appendix excerpt was supplied.
  Both documents share the verified display/encoding boundary; protection against
  encoding-time truncation is also source-inspected, not fault-injected. General
  filesystem atomicity and broader 08C/source coverage are not claimed.
- Runtime logging ownership passes (`R/runtime-logging-check.txt`); installed
  dependency checking passes (`R/pip-check.txt`). Only disposable handlers were
  started/stopped. Production configuration, selection and services are unchanged.

Artifact and source identity:

- Wheel: `R/final/application/ck3chronicle-0.0.1-py3-none-any.whl`, 2,467,374 bytes;
  SHA-256 `3b4b20881233174a1858b4fc960b0318555d0ef9387909ca4584c53772e68890`.
- Source: HEAD `7b7208341469e0b5df8d739cb0fd6e805fc411ea` plus the preserved dirty
  checkout. `R/artifact.json` authenticates all 556 source/wheel/installed members
  in both directions; source inventory digest
  `347641dd2b9d5fa15ba6913998a853788bd898ad1357fff639757806f279a3f4`.
  Installed application source fingerprint is
  `application-source-sha256:64f8a970c935120be483b3b1d5272fc3abe9d581b3d9b9b81a267f6147eeef5d`;
  existing Runs retain their original ingestion lineage.
- Only six wheel members differ from the original: root CLI help, decoder display
  helper, and Reporting analysis/CLI/explanation/presentation. `R/repair.patch`
  isolates this task from pre-existing concurrent changes. Retained learner/model/
  parser distributions, catalogs and packaged selection are byte-identical.
- Fresh setuptools build/staging and installation: `R/final/`; build helper/log
  retained there. Dependency remains the supplied chardet wheel, SHA-256
  `99bdf02c44a943448e82196ea735bd057a3ecc3e0b9a82dbbeff8f563fd9ae64`.
  Installation uses `-I -B`, no ambient checkout modules/PYTHONPATH, and explicit
  disposable `R/context/config.toml` with the existing P database.

Receiving commands (choose a fresh label; these scripts only read existing Runs):

```powershell
$projectRoot = 'C:\Users\nateb\Documents\ck3chronicle'
$repair = Join-Path $projectRoot '.codex-tmp\reporting-repair-20261005'
$python = Join-Path $repair 'final\installed\Scripts\python.exe'
Push-Location (Join-Path $repair 'context')
& $python -I -B (Join-Path $repair 'check_genuine.py') --label pipeline-recheck --cli
Pop-Location
```

Every executed root command/argument/output is retained in the receipts. The
standalone focused checker uses a fresh `focused-final` directory and must not be
rerun over its receipt. To rebuild/reinstall, use the recorded fresh-directory
setuptools helper and offline dependency/wheel installation recipe from the final
handoff; do not overwrite either original installation or Pipeline's staged one.

For a separate receiving installation, choose a fresh `$receivingEnvironment` and
use these exact inputs (the verified installation used `R/final/installed`):

```powershell
$release = Join-Path $projectRoot '.codex-tmp\combined-release-20261005'
$receivingEnvironment = Join-Path $repair 'pipeline-receiving-install'
& "$projectRoot\.venv\Scripts\python.exe" -B -m venv $receivingEnvironment
$receivingPython = Join-Path $receivingEnvironment 'Scripts\python.exe'
& $receivingPython -I -m pip install --no-index --no-deps "$release\wheelhouse\chardet-7.6.0-cp312-cp312-win_amd64.whl" "$repair\final\application\ck3chronicle-0.0.1-py3-none-any.whl"
Copy-Item -LiteralPath "$release\proposed-selection.json" -Destination "$receivingEnvironment\share\ck3chronicle\models\selection.json"
& $receivingPython -I -m pip check
```

Remaining owners/actions: **Pipeline** receives this new installed artifact and
updates cutover; **owner** decides activation. **R3 remains Learner/application
packaging work**: the wheel still ships the old unshipped `candidates/` default.
Only `R/final/installed/share/ck3chronicle/models/selection.json` is overridden with
the authenticated combined release's `proposed-selection.json`. Installed rollback
uses P's `rollback-installed-selection.json`, verified against installed resources;
never copy the checkout's old selection. Packaging must supply/document the intended
installed default in its release arrangement. **R4 remains separately owned
Reporting selector work**, not received here; new-package syntax rejection stays
explicit. No other 08C work, live switch/restart, reset, reprocessing, commit or push
is included in this delivery.

## Pipeline repair receiving completed — 2026-10-05

**READY FOR OWNER ACTIVATION DECISION.** Pipeline independently received R1/R2/R5
against the repaired application. The final installation arrangement, including
R3 defaults and installed rollback, is complete. Keep the existing production
database. Activation and a naturally completed new-package lifecycle remain
separate; no live selection/configuration switch, service restart, production
ingestion, reset, historical processing, commit or push occurred.

New Pipeline evidence root **Q** is
`.codex-tmp/pipeline-reporting-receiving-20261005/`. Original P and producer R
installations/receipts are preserved. The inspected producer checker was executed
by Q's receiving interpreter from Q's explicit disposable context, with fresh
label `pipeline-independent-final`; its output is
`R/pipeline-independent-final/receipt.json`. It reads the existing database named
in `P/database.json`; no ingestion setup was executed or synthetic case created.

### Exact final application and installation

The final wheel remains the delivered
`R/final/application/ck3chronicle-0.0.1-py3-none-any.whl`, SHA-256
`3b4b20881233174a1858b4fc960b0318555d0ef9387909ca4584c53772e68890`.
Pipeline built no replacement wheel. Dependency remains the supplied chardet
7.6.0 wheel, SHA-256
`99bdf02c44a943448e82196ea735bd057a3ecc3e0b9a82dbbeff8f563fd9ae64`.
All **19 producer delivery hashes**, **556 wheel/source entries**, and the six
reported changed application members authenticated independently. No additional
wheel members were added/removed. Retained learner/model/parser distributions,
catalogs, ingestion, contracts, handler/storage and review code are byte-identical
to the previously received wheel.

The complete decoder AST is identical after undoing only the new `display_text`
extraction and delegation from `DecodedText.display_text`. Fragment/native and
physical-source decoding remain unchanged; display escaping does not enter native
processing. Original Pipeline ingestion/storage/native-review and Learner 73-log
receipts are therefore reused. No ingestion or full-corpus campaign was repeated.

Final staged environment: **`Q/deployment`**, CPython 3.12, installed offline into
a fresh venv. `Q/installed-receipt.json` proves installed default/package loading
from **`C:\Windows`**, application/report imports from Q's disposable config
context, module origins under the new prefix, all 394 rendered definitions,
learner authentication, package/parser pins and installed rollback. No ambient
checkout modules are used. Installed `pip check` and runtime logging ownership
pass. Actual new application source fingerprint:
`application-source-sha256:64f8a970c935120be483b3b1d5272fc3abe9d581b3d9b9b81a267f6147eeef5d`.
Stored Runs keep their original processing lineage; read-only reporting does not
rewrite it.

**R3 disposition — Pipeline owns the supported installation arrangement.** The
wheel still contains the old `candidates/` default. The documented mandatory
post-install copy of `OUT/proposed-selection.json` installs the correct new
`releases/4ac4e8ee92346e6d14eacfbf` default. All 556 installed members match the
wheel except that explicit, authenticated selection override. Rollback uses
`P/rollback-installed-selection.json` and authenticates old package
`68f1ae5db205ab46afef9c4d` under installed `releases/`, with its original pin.
Both selections load against this exact final installation. The deployment is
complete; a bare wheel installation without the selection step remains a known
Pipeline-owned packaging limitation. No unnamed or Learner packaging owner is
being asked to close this arrangement, and no additional owner waiver is needed.
The [cutover runbook](PIPELINE_CUTOVER.md) contains the exact install recipe,
final paths, selections, capture boundary, backup/rollback and post-switch checks.

### Independent genuine-data verification

The producer's first/final/focused receipts were authenticated and inspected,
not counted as Pipeline executions. Pipeline's own run passed **35 checks and
28 root CLI invocations**: 24 report exports, two listings, and two syntax checks.
Twenty-seven commands exit 0; new-model syntax correctly exits 2 with
`invalid_query`. Contents and native records were checked, not just exit codes.

| Boundary | Independent result |
|---|---|
| R1 repeated templates | BND9AS: 59,313 occurrences / 3,211 records; OSPK8G: 12,811 / 3,315. JSON/HTML/text pass. Meaningful declared repeat text, exact/partial template filters, actual typed repeated bindings, message filters and rollup totals agree with public handler records. Witnesses retain 20 and 18 repetitions. Affected subsets remain 54,967 / 1,012 records and 8,003 / 1,136 records. |
| R2 stored bytes and display | All 44 byte-bearing occurrences survive JSON deserialization as the exact native stored values and inverse-encode to the original session-55 bytes. Targeted CLI JSON/HTML/text work with and without optional history; display uses labeled `\\xHH` while valid Unicode remains intact. No storage normalization occurs. |
| R5 ordinary operations | Missing-time XH88PI appears in all-package listings before pagination and the all-Run message search. The genuine shared message matches BND9AS, OSPK8G and XH88PI; counts and pagination include all three. Named reports retain 100,003 occurrences / 21,757 records with and without optional history. Source time stays absent. |
| Chronology | Unplaceable history has no invented relative positions, newness or zero observations. Chronological latest/history excludes unplaceable dates; explicit novelty filtering remains unavailable for that Run. Ordinary queries remain available. |
| Old-package compatibility | DQT13M retains 1,838 occurrences / 1,066 records; all formats and its syntax preset pass. Package-scoped histories remain separate; no cross-package zero counts are inferred. |

Pipeline additionally inspected the producer's six focused exports against fresh
public-handler query results and inspected the independently generated targeted
byte JSON and three HTML appendices (`Q/export-content-receipt.json`). Actual
repeated-binding output and 37 native-byte-filter matches agree in all three
formats; `Agmánd` remains unchanged. The independent targeted exports contain
all 44 byte occurrences. Session 55's appendix correctly has no candidate excerpts
because no producer playset was captured. No genuine current-source appendix
excerpt containing preserved bytes was supplied; that remains an evidence limit,
not an activation gate or a commissioned new test. Both HTML documents are encoded
before either destination opens, as confirmed by source inspection. General file
I/O atomicity and broader source/08C coverage are not claimed.

The original disposable database's complete-file hash, native record digests and
Run metadata remain unchanged. Original producer receipts and all live
configuration/selection/catalog guards remain unchanged. No newly demonstrated
regression or failed receiving check remains. R1/R2/R5 are closed for this receipt.
R2's earlier nonblocking disposition stands; it was not re-requested.
**R4 remains separately owned Reporting selector work**; explicit unsupported
new-model syntax behavior is preserved, not represented as a zero count.

### Refreshed operations and owner decision

At **2026-10-05 09:27:19 UTC** (17:27 Hong Kong), the existing handler answered
read-only operations as PID **23252**, instance
`ca3faf45a4514e5cab542769c2a3c70f`; a fresh heartbeat identified watcher **30816**
in state **absent**. Process creation times match the October 2 services. These
are current receipt observations, not permission to act on stale PIDs later.

The previously running session ended naturally and the watcher protected
`pending/20261005T081833.826175Z-h0m4a9YR`. Its request
`141e696aa6aa4459a0b45fbf93f6ee5b` completed at **08:18:52 UTC** as genuine Run
**`20261005-0UM3HN`**, still on old package/parser v1.7/matcher v2. All 30 stored
Runs now have readable matching protected originals; 22 older pending directories
remain inaccessible. No readable unstored complete capture was found. This was
read-only inspection of configured pending/runtime evidence, not a historical
refresh, crash-principal search, or fabricated capture.

Recommended operational decision: authorize the prepared transition to **Q's
repaired installed application plus package `4ac4e8ee92346e6d14eacfbf`**, retaining
the existing database, after refreshing the absent-game/capture-drained boundary.
The current prompt explicitly reserves live pin/configuration switching and
watcher/handler restart for a separate owner decision. Until then services remain
unchanged. After an authorized switch, actual new loaded lineage and the next
naturally completed unique live capture/report must be verified; no such
post-switch lifecycle is claimed by this disposable receiving.

## R3 packaging closed — 2026-10-05

**Pipeline closes R3. READY FOR OWNER ACTIVATION DECISION; do not activate.**
The owner explicitly held cutover while requesting this application packaging
repair. No live selection/configuration switch, runtime restart, production ingest,
database reset, historical processing, commit or push was performed.

Evidence root **S**: `.codex-tmp/pipeline-r3-packaging-20261005/`.
Final newly built application: `.codex-tmp/pipeline-r3-packaging-20261005/application/ck3chronicle-0.0.1-py3-none-any.whl`, SHA-256
`7239a0c5b89e52f2df1d31028bdbf21b086e3600bf7c079347a1ee4f1d982959` (2,467,339 bytes).
Final dormant installation: `.codex-tmp/pipeline-r3-packaging-20261005/deployment`.
The accepted Reporting wheel `3b4b2088…68890` and all previous installations/receipts
are preserved. This is a fresh source build, not a patched or relabeled wheel.

### Packaging change and independent verification

`pyproject.toml` now ships `packaging/models/selection.json` under the existing
installed `share/ck3chronicle/models/selection.json` location. Its bytes equal the
authenticated proposed selection. The separate checkout live selection remains
unchanged. The wheel default names shipped `releases/4ac4e8ee92346e6d14eacfbf`,
manifest pin `839548e8c8143e01b63059848557dc94e9fe66f5e1924f6026442f7331a8ba9f`.

- `S/artifact.json` authenticates all 556 code/resource members against source.
  The only changed code/resource member against the accepted Reporting wheel is
  the bundled selection. Dist-info RECORD updates accordingly; METADATA also
  includes the concurrent root README's team-governance link (`S/metadata.diff`).
  All application code, native decoder, catalogs and immutable learner/model/parser
  distribution members are byte-identical to the accepted artifact.
- `S/build_application_clean.py` used fresh build/staging/output directories;
  `S/build.log` and `S/install.log` retain the commands' results. The clean CPython
  3.12 environment was installed offline with the same authenticated chardet 7.6.0
  wheel (SHA-256 `99bdf02c44a943448e82196ea735bd057a3ecc3e0b9a82dbbeff8f563fd9ae64`).
  No installed selection file was copied, rewritten or otherwise corrected.
- `S/installed-receipt.json`: default package and classifier loaded from
  `C:\Windows` using `-I -B`, without an explicit selection argument or ambient
  checkout modules. All 556 installed code/resource members exactly match the
  wheel, including selection. All 394 new-package definitions render. Installed
  Reporting/HandlerClient imports use the explicit disposable context; no new
  handler or ingestion was needed. Installed `pip check` passes.
- The same installation authenticates the learner release and parser v1.8 pin,
  and loads the previous package/classifier and its definitions using
  `P/rollback-installed-selection.json`. Rollback resolves shipped
  `releases/68f1ae5db205ab46afef9c4d`, manifest pin
  `2a84fe9c734a558e757df54649eac0812ea380a80ac8a2d0fe17129d50f24a5f`.
  The old checkout `candidates/` selection is not used as installed rollback.

### Reused evidence and limits

The application fingerprint remains
`application-source-sha256:64f8a970c935120be483b3b1d5272fc3abe9d581b3d9b81a267f6147eeef5d`.
The independent R1/R2/R5 receipt at `R/pipeline-independent-final/receipt.json`
(35 genuine-data checks, 28 root CLI invocations with their expected outcomes)
and Q's additional output-content checks remain applicable because executable
bytes are unchanged. Original P ingestion/storage/native reconstruction/review
checks and Learner's full-corpus comparison are reused. No reporting campaign,
ingestion setup, synthetic case or model build was repeated for this packaging change.
`S/final-checks.json` records guards and exact reused receipt identities.

R4 new-model syntax remains explicitly unsupported and separately owned by
Reporting. R2's nonblocking unrepresented source/appendix evidence limits remain
as previously accepted. No new warning schema or physical-source admission was added.

Read-only observation at **09:44:32 UTC** found watcher 30816 and handler 23252 /
instance `ca3faf45a4514e5cab542769c2a3c70f`, with game absent. Latest genuine Run
remains `20261005-0UM3HN` on the old package. Thirty readable pending originals
match 30 stored Runs; 22 older directories remain inaccessible. See
`S/live-observation.json`, `S/live-processes.json` and `S/live-latest-run.json`.
These observations must be refreshed at any authorized future cutover.

Keep the current production database. The [final runbook](PIPELINE_CUTOVER.md)
uses this exact new wheel and staged environment, provides authenticated package
rollback, and preserves the capture-safe stop/backup/start boundaries. Activation
is held by the owner's explicit instruction. New-package live ingestion and a
naturally completed live lifecycle remain pending.

## Production activated — 2026-10-05

**Production is on the new package. No rollback. New-package live ingestion and
a naturally completed lifecycle remain pending.** The owner explicitly assigned
the execution prompt, superseding the prior hold for this cutover. R1/R2/R3/R5
receiving remains closed; R4's unavailable new-model syntax preset remains
separately owned Reporting work.

Activation evidence **A**: `.codex-tmp/pipeline-activation-20261005/`.
The final wheel remains
`.codex-tmp/pipeline-r3-packaging-20261005/application/ck3chronicle-0.0.1-py3-none-any.whl`,
SHA-256 `7239a0c5b89e52f2df1d31028bdbf21b086e3600bf7c079347a1ee4f1d982959`.
The installed interpreter is
`.codex-tmp/pipeline-r3-packaging-20261005/deployment/Scripts/python.exe`.
Checkout and installed selections now both select learner v61/parser v1.8 package
`4ac4e8ee92346e6d14eacfbf`, manifest pin
`839548e8c8143e01b63059848557dc94e9fe66f5e1924f6026442f7331a8ba9f`.
The installed default was already correct and was not replaced.

| Operation / observation | Actual UTC time and result |
|---|---|
| Preflight | 09:55:24; final wheel, all 556 installed members, default and installed rollback authenticate; 63 recorded handler requests have 63 terminal events, with none outstanding. Game absent; no capture publication in progress. |
| Controlled stop | 09:56:40.521–09:56:41.084; verified watcher 30816 stopped, handler 23252 / `ca3faf45a4514e5cab542769c2a3c70f` shut down through HandlerClient; old processes and pipe gone. |
| Backup verified | 09:56:54; 187 files, 1,250,938,203 bytes, with source/copy hashes verified. |
| Selection switch / start | 09:57:58.533 / 09:57:58.560; checkout selection switched; installed watcher launched hidden from checkout working directory. |
| New runtime | Watcher launcher 64756 → watcher 64444; handler launcher 65896 → handler 47932; handler instance `88739409838c4e38936bebc72166ae33`, worker 24868. |
| Verification | 10:01:22; fresh absent-game heartbeat from watcher 64444, lease acquisition recorded, handler ready, 30 expected startup duplicates, no new Run or reprocessing. |

Verified backup:
`.codex-tmp/pipeline-activation-20261005/backup-20261005T095647Z/`.
It contains the closed production SQLite database, complete review files,
configuration, previous checkout and installed rollback selections, staged/new
selection, and accessible protected error/debug logs, capture metadata and playsets.
The 22 previously inaccessible capture directories remain untouched and enumerated
in `A/backup.json`; their unavailable originals were not reconstructed.

The existing database remains
`.ck3chronicle/wip/runtime/ck3chronicle-schema3-20260928T211854Z.sqlite3`, database ID
`ck3chronicle-schema3-20260928T211854Z`, schema 3. Configuration stays checkout
`config.toml`, SHA-256 `57f199ebad15840cdb95be6393aaabd3a2dfd1c9d8bc5a9acc03c6c2db66224b`.
Retention settings are unchanged; no manual expiry, reset, historical replacement,
model build, commit or push occurred. All 30 stored Run records remain identical
to pre-cutover public-handler reads; backup-source hashes, including the database,
review and accessible capture files, remain equal after verification (the
authorized checkout selection change is the sole expected source exception).

`A/preflight.json` records installed module origins and unchanged application
fingerprint `application-source-sha256:64f8a970c935120be483b3b1d5272fc3abe9d581b3d9b9b81a267f6147eeef5d`.
`A/process-command-lines.json` and `A/after/live-processes.json` record actual
launchers, process ancestry/command lines and creation times. Windows venv launchers
spawn the base Python executable; the verified ancestry ties both actual processes
to the installed environment. PYTHONPATH was removed and user-site loading disabled.
No competing watcher/handler was found. CIM inspection was unavailable; the
recorded command-line/parent inspection used read-only Windows process APIs.

`A/verification.json` records public-handler reads and three installed root CLI
exports for genuine existing Run `20261005-0UM3HN`. JSON/HTML/text all succeed;
JSON native values match stored records and rendering, with 34,351 occurrences
across 3,412 records. This Run retains its old-package ingestion lineage.
Watcher stderr and handler bootstrap are empty; runtime events show ordinary
startup duplicate outcomes and no new runtime failure. Logging ownership and
installed dependency checks pass. Prior genuine repeated-layout, preserved-byte,
missing-time and package-history receiving remains applicable; no broad campaign
or synthetic case was repeated.

**Live processing evidence is still pending.** No naturally completed new unique
capture occurred during cutover verification. Duplicate admission returns before
parser/classifier loading, so startup does not establish a new-package stored
processing lineage or a completed lifecycle. The installed target/pin and runtime
launch are authenticated; this distinction is not hidden by old Run lineage.

**Pipeline retains the follow-up:** after the next natural `game_started` →
`game_exited` → protected capture → `ingestion_completed`, correlate the new
capture hash and request to public `find_run_by_log_hash` / `get_run`. Verify package
`4ac4e8ee92346e6d14eacfbf`, the manifest pin above, parser v1.8 SHA-256
`0357b8d1c342c546452ed8f294405bfe41c86c7116eca51eddf8bc5b67984135`, matcher v3 and
the installed application fingerprint. Reconcile native diagnostics/counts,
capture facts and exact spans, playset and review metadata; run named JSON/HTML/text
reports through this installed interpreter. Confirm ordinary listing/search/reporting
retains a missing-time Run if that genuine case occurs; only chronological placement
may be unavailable. Record absent facts as absent. Append the result here and update
the status pointers. Do not generate a capture or resubmit an old hash to close it.

Execution notes: an initial stop guard refused before any process stop because
PowerShell's automatic JSON DateTime conversion was reparsed through a display
string. Comparing the original DateTime ticks resolved it with unchanged process
identities. The reporting checker initially referenced `count`; it was corrected
to the existing `occurrence_count` field, and all three real exports then passed.
Neither was a product failure; the initial report-check log is retained.

## Thirty-capture rebuild staged; switch deferred — 2026-10-05

**STAGED REBUILD VERIFIED. Production database switch remains deferred by the
owner.** The owner requested rebuilding the 30 readable protected captures under
the new model, then explicitly directed: leave CK3 running, finish staging, and
defer the switch. No active database was wiped, no configuration was switched,
and the existing watcher/handler were not stopped.

Evidence **F**: `.codex-tmp/pipeline-refresh-20261005/`.
The existing `create_database` API explicitly initialized the separate store:
`.ck3chronicle/wip/runtime/ck3chronicle-schema3-20261005T112504Z.sqlite3`.
All 30 exact retained capture directories were ingested through the installed
public HandlerClient, without modifying their logs/metadata/playsets. The fresh
store has 30 unique input hashes, all on package `4ac4e8ee92346e6d14eacfbf`,
manifest pin `839548e8c8143e01b63059848557dc94e9fe66f5e1924f6026442f7331a8ba9f`,
parser v1.8/hash `0357b8d1c342c546452ed8f294405bfe41c86c7116eca51eddf8bc5b67984135`,
matcher v3 and application fingerprint
`application-source-sha256:64f8a970c935120be483b3b1d5272fc3abe9d581b3d9b9b81a267f6147eeef5d`.
The installed final R3 wheel remains SHA-256
`7239a0c5b89e52f2df1d31028bdbf21b086e3600bf7c079347a1ee4f1d982959`.

At 11:36:45 UTC, independent readback/reconstruction verification passed:

- 948,135 classified occurrences in 76,510 stored records; per-Run totals
  reconcile with stored accounting. All 30 ingestions completed without warnings.
- 95,742 stored native regions reconstruct exactly against their original byte
  spans using UTF-8/surrogateescape. Original complete-file hashes remain unchanged.
- All 30 capture facts equal their protected metadata; playsets equal the
  previously accepted stored playsets. Review shards (2,353,660 bytes in total)
  match stored hashes and original emission spans; manifests carry the new lineage.
- Four installed root CLI reports passed: JSON/HTML/text without history, and JSON
  with optional history for a genuine missing-time Run. Counts remain correct and
  chronology is honestly unavailable. Fourteen staged Runs have no source timestamp;
  they remain present in ordinary public-handler listings.

`F/rebuild-completed.json` contains old-to-new Run ID mappings and per-Run receipts;
`F/rebuild-verification.json` records native/accounting/playset/review/report checks.
The separate staging handler was shut down after verification. The closed database
is 112,771,072 bytes, SHA-256
`cd437809e1c866818148d595e9f49c326f4d86807b85cc685628edcc4daaacaf`.
`F/staging-summary.json` records this completed state.

At 11:37:32 UTC, production still uses
`.ck3chronicle/wip/runtime/ck3chronicle-schema3-20260928T211854Z.sqlite3`, with its
30 existing Runs, watcher 64444, handler 47932 /
`88739409838c4e38936bebc72166ae33`, and CK3 PID 53004 running. Configuration and all
retained input hashes are unchanged. This genuine historical rebuild is distinct
from the still-pending natural production lifecycle verification.

The 22 inaccessible directories are legacy August 30–September 6 captures; all
30 newer retained directories inherit permissions and are readable. The installed
harvester contains the September 8 inherited-permissions correction. No ACL repair
or inaccessible-log recovery was attempted here; see `F/access-chronology.json`
and `F/readable-capture-acls.json`.

**Pipeline continuation, after the owner lifts the switch deferral:** wait for a
natural game exit and complete capture/ingestion; refresh the inventory and verify
any newly completed production lifecycle. At the safe idle boundary, stop only the
verified production watcher/handler, make and verify a fresh closed-store/evidence
backup, and switch the explicit configured database path to this already verified
store. Preserve any captures created since the 30-input inventory. The sole installed
watcher's ordinary startup scan will deduplicate these 30 hashes and ingest newly
protected unique captures. Reconcile all expected hashes/new Runs and reports before
archiving the previous active database/review namespace. Do not rerun the 30-capture
build or invent missing facts. Prepared helpers exist in F but the stop/configuration
helpers reject execution while `owner-disposition.json` records the current deferral.
R4's unavailable new-model syntax preset remains separately owned Reporting work.

## Database replacement complete — 2026-10-05

**Production now uses the fresh rebuilt database. All 31 Runs use the new model.
No rollback. The genuine new-package live lifecycle check is verified.** The owner
closed CK3 and resumed the authorized replacement after deferring the switch.
The active store was replaced; no old database rows were migrated or imported and
no legacy fallback was added. Each Run was created by ordinary ingestion of its
protected error.log and accompanying capture metadata/playset inputs.

Active database:
`.ck3chronicle/wip/runtime/ck3chronicle-schema3-20261005T112504Z.sqlite3`.
Its 31 Runs comprise the verified 30-input rebuild plus the session just closed.
All have package `4ac4e8ee92346e6d14eacfbf`, manifest pin
`839548e8c8143e01b63059848557dc94e9fe66f5e1924f6026442f7331a8ba9f`, parser v1.8
and the installed final R3 application lineage. Totals: **958,190 classified
occurrences across 79,508 stored records**. The 30 staged Runs were unchanged by
startup; the last capture was independently ingested from its original files.

| Step | Actual UTC time / evidence |
|---|---|
| Natural game lifecycle | Watcher 64444 observed CK3 53004 start at 11:16:27.512 and exit normally at 12:06:14.300. |
| Capture and live ingestion | Capture `20261005T120614.334116Z-ZxGo208o` published at 12:06:16.704; automatic new-model ingestion completed at 12:06:25.580 as `20261005-5VVDQZ` in the now-retired store. |
| Safe stop | 12:07:32.224–12:07:34.618; no game, publication or unfinished handler request. Verified watcher/handler stopped; staging handler was already closed. |
| Backup / database selection | Fresh backup verified: 291 files / 1,402,178,722 bytes. Configuration's database path changed at 12:07:47.241; other configuration bytes are unchanged. |
| Restart | 12:08:19.685; hidden installed watcher launcher 55312 → watcher 51024; handler launcher 60264 → handler 54908. |
| Startup accounting | 30 ordinary duplicate outcomes and one newly ingested capture, Run `20261005-UYSOEO`; no reprocessing of the staged 30. |
| Verification / retirement | Checks passed at 12:11:16; retired database/review namespace archived at 12:11:45. Final public read at 12:12:29 confirms 31 all-new-model Runs and a healthy absent-game heartbeat. |

New handler instance: `f474dbf7100a44399e2ae4a6a05f6375`, worker 8516.
The installed interpreter and immutable package/distributions are unchanged from
R3. Selection files were not replaced. Configuration remains checkout `config.toml`;
only its explicit database path changed. No competing watcher/handler remains.

Fresh verified backup:
`.codex-tmp/pipeline-refresh-20261005/backup-20261005T120734Z/`.
The former active database and its review namespace were moved out of runtime into
that backup's `retired-original/` directory after successful production checks;
63 moved files were hash-verified again. The September 28 database is no longer at
its old active path. It is retained only as backup, with no runtime fallback route.
All 31 readable protected capture directories and their bytes remain intact; the
22 inaccessible legacy directories remain untouched.

The last capture SHA-256 is
`9810212144c70b2eeaed1919ba8a14e296ca8801219df8cb1d13d51c9bfe3c4c`.
Its active Run `20261005-UYSOEO` has 10,055 classified occurrences / 2,998 records.
Native reconstruction matched 3,674 stored regions to original byte spans; capture
facts, playset, counters and review bytes passed. JSON, HTML and text reports with
history succeeded through the active public handler. The prior 30-Run verification,
including missing-time reports, remains valid. Handler bootstrap and watcher stderr
are empty; runtime logging ownership passes. This observed natural lifecycle
closes the earlier live-ingestion follow-up; startup alone was not used as proof.

Evidence F (`.codex-tmp/pipeline-refresh-20261005/`): `preflight.json`, `stopped.json`,
`backup.json`, `selected.json`, `started.json`, `process-command-lines.json`,
`switch-verification.json`, `archived.json`, `completion.json`, public snapshots
under `before/` and `after/`, and the exported production reports. Original staging
and activation receipts remain historical evidence. R4's unavailable new-model
syntax preset remains separately owned Reporting work; accepted source/appendix
limitations are unchanged. No commit, push, fake capture or model rebuild occurred.
