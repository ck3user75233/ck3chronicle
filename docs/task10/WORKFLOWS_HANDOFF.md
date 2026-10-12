# Task 10E — Workflow and external-data delivery

2026-10-08. **TREK-15**, Launch & Distribution / Docs. Edition **10E-r1** is
delivered for 10C to follow; receiving and the required installed lifecycle/stop
check remain open. No product code, schema, configuration authority or export
mechanism was added. Tracker status is not final product acceptance.

## Delivered files and editorial boundary

- [WORKFLOWS.md](../user/WORKFLOWS.md): first/repeat setup, observe/stop, captured
  input processing, Run investigation/comparison, report files, model choice,
  execution journals and bounded recovery guidance.
- [EXTERNAL_DATA.md](../user/EXTERNAL_DATA.md): configured schema-3 database,
  live read-only transaction, meaningful SQL/tool example, keys/JSON/timestamps/
  scope, and separate native-shard locating/viewing.
- [Genuine cropped setup screenshot](../user/images/setup-folders-c9-crop.png):
  existing 10B candidate-9 capture; crop `(0,0,900,415)` removes private user-path
  fields. No replacement pixels, generated screen, or outcome inference.
- [Root README](../../README.md): delegated orientation links and bounded updates
  to its obsolete command/bootstrap statements. 10D retained the manual index,
  references and shared assignment-index editor; CMT-112 delegates this README edit.
- [Assignment](../task10-deliverables/10E_USER_WORKFLOWS.md): native ID recorded.

TREK-11 CMT-107/108 requested shared-run/index coordination. TREK-15 CMT-112
confirms the shared C9 handler is stopped, authorizes reuse of the exact genuine
example, identifies original GUI images and delegates root README. 10D has linked
the two guides in its [manual index](../user/README.md) and recorded TREK-15 in the
assignment index. No parallel edits to its canonical references were made.

Final guide/asset hashes and commands are retained in
`.codex-tmp/task10e/delivery-manifest.json`. This pins a review revision for 10B
and 10C; it is not a source commit, rebuilt bundle or published manual. Runtime
evidence is ignored, outside Git. The prior root README is retained byte-for-byte
at `.codex-tmp/task10e/before/README.md`; the two guides, handoff and cropped asset
were absent before 10E. The only assignment-prompt change is its enrollment line.

## Product and technical inputs

| Input | Exact identity / receipt |
|---|---|
| Application | **0.0.2**, wheel SHA-256 `2de516e02aae2e858f1b2f2d34a5ec89ba69306e7001477c29d1857d9ffbd594`; TREK-9 CMT-81/82, actual receiving CMT-83 |
| Windows candidate | C9 manifest `066ae6f7378372074c575cd9c5c8e75257c809ec65575526a0fee7979f9f4aa5`; ZIP `db1ed81f050e13c93652681e829c18ef282a92965c116aee0fc59cea49eedfc1`; TREK-10 CMT-91 |
| Executed tool | C9 private CPython 3.12.14 / SQLite 3.53.1, Windows x64; actual tool-version stdout retained |
| Default package | `2b12932103f3a3111a4e1880`, manifest `02c70654c3ffa9678df80108985206a12c92bb67b0c36311fbec393b329e1505` |
| Source | Task09 baseline `709ea7842a0202c420b43355b18be91d8ca196a3` plus delivered uncommitted Task10 bytes; baseline tag alone does not identify this candidate |

Read and refreshed 10A/TREK-7, Pipeline/TREK-9, distribution/TREK-10,
reference/TREK-11, and Watcher/Reporting/Learner contributions TREK-12/13/14.
Actual later receipts supersede stale pending/dispatch prose in older handoffs.
Technical sources are [10A's journey](FIRST_USE_DESIGN.md),
[Pipeline delivery](PIPELINE_HANDOFF.md), [distribution delivery](DISTRIBUTION_HANDOFF.md),
[reference coverage](DOCUMENTATION_HANDOFF.md),
[Watcher contribution](WATCHER_DOCUMENTATION_HANDOFF.md),
[Reporting contribution](DATA_INTELLIGENCE_CONTRIBUTION.md) and
[Learner contribution](LEARNER_DOCUMENTATION_HANDOFF.md).

10D received the three component contributions on CMT-109/110/111. 10E uses those
technical meanings and owns the cross-component steps. Pipeline's documented
`mode=ro`/short-transaction route meets the basic external-access requirement;
no new snapshot or flattening request is necessary. Current C9 healthy-checkbox
defaults follow later Owner direction, not the superseded first-use proposal.

## Evidence and reproduction

Fresh 10E originals are in **`.codex-tmp/task10e/`**. `commands.json` and
`fresh-commands.json` retain exact argv, cwd, expected/actual exit and named
stdout/stderr files; `verify_guides.py` executes the guide's literal PowerShell/
SQL blocks with real path/Run substitutions. `verification.json`,
`inspection-queries.json`, `review-verification.json` and `history-reuse.json`
record inspected results. `reused-evidence-hashes.json` identifies the exact
shared originals consumed. It is a document-evidence recorder, not a new product
test framework or acceptance requirement.

The application bundle used is
`.codex-tmp/task10b/READY_TO_MOVE_C9/ck3chronicle/`. Fresh guide-block execution
uses that folder as cwd; preview/model/doctor commands use the ignored 10E
evidence directory. Neither depends on repository imports. Verify authenticates
all 1,492 bundle files. Config and databases remained byte-identical across
these fresh read-only operations; no handler or watcher was started by 10E.

### Shared installed genuine example

10D's exact original directory is **`.codex-tmp/task10d/evidence/`**, confirmed
for reuse by CMT-112. `commands.json`, `verification.json`, `stored.json`,
`inspect-command.json`, `inspect.stdout` and each named stdout/stderr/output are
the execution receipt, not merely screenshots or help output.

- Configuration: `settings/paths.toml`; data: `data/runtime/`.
- Database: `ck3chronicle-schema3-20261008T142121Z.sqlite3` in that runtime.
- Genuine input directory: `pending/20261003-D3N7ZQ`; error-log SHA-256
  `5a7b93d8ee374c60f767593631713eaf8719004ba4f9cf33e7eb5d812dbec629`.
- Stored Run: **`20261008-01PBM7`**, 1,066 diagnostic records / 1,838 occurrences.
  1,057 template records / 1,775 occurrences; 9 provisional / 63.
- Public-handler `get_run`, `read_diagnostics`, `read_playset`,
  `read_review_metadata` results establish stored facts and all 133 playset
  members. Native review is available and empty: zero bytes/emissions/units.
- Source modification `2026-10-03T02:34:42.700452600+00:00` differs from processing
  `2026-10-08T14:21:24.878287+00:00`. Identity basis is processing; no date invented.

### Journey receipts

| Guide journey | Prerequisite/input and exact command source | Expected / actual result and files | Status |
|---|---|---|---|
| First GUI setup | C9 actual external receipt `task10b/resume-20261008/{c9-placement-receipt.json,c9-verification.json,c9-command-evidence}`; local wizard screenshots/checks under `task10b/wizard-flow/checks/` | Saved config, private runtime/import/model/tool identity, 1492-file Verify and handler shutdown; Owner completed external GUI once. Local repeat is separate evidence. | Applicable 10B reuse; not new 10E installation |
| CLI setup / repeat | 10D `commands.json`: `setup-preview`, `setup-apply`, `setup-repeat`; `verification.json` repeat-confirm; same real CK3 paths and isolated storage | Preview creates nothing; Apply saves exact DB/model/tool; repeat preserves populated DB hash. Commands exit 0; saved config and public stored facts inspected. | Exact shared reuse |
| Inspect config/model/doctor | 10E `fresh-commands.json`: installed `setup --format json`, `setup --list-models --format json`, `doctor --format json` using shared config | Preview/database/model agree with saved config; inventory succeeds (0); doctor has expected unverified write findings (2). Config/DB unchanged. | Fresh 10E execution |
| Start / observe / stop | Watcher contribution's authenticated `pipeline-refresh-20261005/switch-verification.json`; 10B `verification-candidate3-final/watcher-check.json` | Actual earlier CK3 lifecycle and unchanged watcher delivery; installed Start attached to existing CK3 and observed startup duplicate. Managed-terminal graceful stop was unsuccessful; task cleanup is not stop acceptance. | Reused limited receipts; full C9 lifecycle and ordinary-console Ctrl+C open |
| Captured-input ingest | 10D `commands.json` `ingest`, `ingest.stdout`; genuine input above | `COMPLETED`, exit 0, Run 01PBM7; public handler and later independent SQL confirm stored result/lineage/counts and preserved playset. | Exact shared reuse; no repeated ingest |
| Runs/investigate/custom | 10D `runs`, `report-text`, `custom-report`, `report-hotspots`, `report-new` command entries | Exit 0; text shows 1066/1838 with 5 displayed; custom failed-context-switch query is successfully empty. Single-Run history explicitly unavailable outside selected position. | Exact shared reuse |
| Genuine multi-Run comparison | `trek5-reporting-20261006/changed/receipt.json` `history-json`/`history-text` and matching stdout; Reporting unchanged-byte correspondence in its contribution | Exit 0; selected BND9AS 3211/59313, predecessor OSPK8G 3315/12811, 541 earlier identities absent now. Fresh 10E SQL counts match both stored Runs; `history-reuse.json` retains positions/totals. | Earlier execution reused; fresh read-only corroboration, not new 0.0.2 history generation |
| Text/JSON/HTML outputs | 10D `report-{text,json,html}`; `report.text`, `report.json`, `report.html` | All exit 0 and actual files exist; JSON/public-handler totals agree; five displayed records do not truncate totals. External C4 receipt separately corroborates unchanged app. | Exact shared reuse; no fresh browser-navigation claim |
| Model change | Pipeline `task10a1/release/{commands.json,supplement.json,verification.json,stored.json}` | Actual select prior `4ac4e8...`, different genuine G2 ingest to QE9JN9, observed package/restore default and unchanged historical rows. | Applicable 0.0.2 reuse; no model build/replay |
| External SQLite | 10E `external-read-retry.stdout`, `commands.json`; literal guide block with shared config/Run | Exit 0, no stderr; SQLite 3.53.1/schema 3 and 1066/1838 equal Run counters plus handler/report evidence. All remaining guide SQL queries executed; binding values match stored evidence. | Fresh 10E |
| Empty and nonempty native shard | `review-verification.json`; literal guide PS blocks and `review-<Run>-retry1.stdout` | Both exit 0, no stderr after correction; size/hash/manifest/Run agree. Empty 01PBM7 separate from nonempty historical OSPK8G. Native bytes read as text, manifest as JSON. | Fresh read-only viewing of genuine files |
| Execution logs | `execution-logs.stdout`, `verification.json`; shared report and rotated handler JSONL files | Exact guide command prints actual event fields; 40 foreground accepted report request pairs match real handler terminal completions. Absence is not reconstructed. | Fresh read-only inspection |

### Separate nonempty review evidence

Existing genuine Run **`20261005-OSPK8G`**, package `4ac4e8ee92346e6d14eacfbf`,
is in the retained task database
`.codex-tmp/pipeline-receiving-20261005/context/runtime/disposable/ck3chronicle-schema3-20261005T060419Z.sqlite3`.
The genuine input is original capture `20261002-2PVVSE`, input SHA-256
`13b97a210172daf637ad77ecc83ae94463f492ed8d467493a3bd37b08a5527a6`.
Its [Pipeline receipt](../learner-next-release/PIPELINE_RECEIVING.md) explicitly
records the original capture, two unmatched plus one unresolved-recovery unit and
418 exact bytes; corresponding `20261002-2PVVSE-{ingest,review-metadata}.json`
originals remain beside that evidence tree. This is not the synthetic LOCATOR fixture.

Stored review reference:
`review/ck3chronicle-schema3-20261005T060419Z/20261005-OSPK8G/review.error.log`.
Actual SHA-256 **`6925e2c7d6c36f76af28eba6850804f022d0947d8fdb265570f27f79278729c7`**,
418 bytes, 3 emissions/3 units. Fresh file viewing and hash/manifest comparison
passed. The source database was opened only with `mode=ro` and a short transaction;
its bytes stayed unchanged. This receipt establishes viewing existing unresolved
native evidence, not reclassification under the new default model.

### Recorder and documentation corrections

All limits/failures remain visible:

- Enrollment succeeded as TREK-15, but the initial local response recorder used
  the request's absolute path in an output filename and failed. The canonical
  task-list was read before continuing; the create was **not retried**, no
  duplicate task was made, and native state was confirmed before update.
- Initial scratch `.ps1 -File` execution was rejected by local execution policy.
  The documented pasted command block then executed through `-Command`, without
  changing execution policy. Exact first failure and later stdout/stderr remain.
- The local Python evidence reader first used the Windows default text encoding
  for a genuine UTF-8 report, then misread an indented Markdown fence. UTF-8 mode
  and bounded fence extraction corrected the recorder; no product/data repair.
- Initial shard snippet used `Get-FileHash`, unavailable in this managed
  PowerShell session. It emitted a nonterminating error even though the shell
  returned 0. Earlier output formatting also hid unlike object fields. The final
  guide uses bundled Python SHA-256 plus explicit `Format-List`; both genuine
  shard examples now visibly show actual hash/metadata with **empty stderr**.
  Earlier failed/incomplete transcripts are retained and do not count as passes.

No synthetic history, mock client, injected fault, new requirement or code repair
was created. No source runtime changes occurred, so the runtime-logging ownership
checker is not required for this documentation-only change.

## Remaining receiving actions and limits

| Owner | Exact action / limit |
|---|---|
| **10C / Launch & Distribution** | Follow these guides against the final authenticated installed bundle and record internal receipt on **TREK-15**, separately from 10D/TREK-11 and 10B/TREK-10. The current candidate's ordinary-console Ctrl+C plus a full fresh CK3 lifecycle remain required unverified journey work. Use a genuinely authorized interactive session; do not treat managed-terminal cleanup as success. |
| **10B / Launch & Distribution** | Receive the agreed 10D/10E manual revision and include its exact hashes in a new final bundle; finish its existing upstream runtime/tool notice/provenance work. Current C9 does not already contain this final guide revision. |
| **10D / Docs** | Maintain canonical shared index/reference links and already-returned wording issues. Its CMT-106 on TREK-9 identifies stale ingest-help “catalog default”; CMT-92 on TREK-10 identifies stale external-installation prose. 10E states current delivered behavior and does not repair producer code. |
| **Pipeline / TREK-9** | Retains actual storage/config/application defects. None found in the basic read-only access route; no new mechanism requested. No documented complete app backup/restore is claimed. |
| **Watcher / component owner** | Retains any technical correction to lifecycle/stop semantics if the real 10C console check fails; current contribution accurately labels the unverified case. No new implementation dispatch from this handoff. |

No current source supports claims of a complete backup, concurrent-writer timing
test, clean-machine installation, fresh C9 full lifecycle, ordinary-console
graceful stop, genuine interrupted-setup recovery, absent-current-log setup case
or every flag variant. Unexecuted command shapes are identified in the guides.
These limits do not turn an empty SQL result or missing fact into a defect.

10E remains open for 10C receipt and its own documentation corrections. No
production state, live service, retained release, Git index/commit/tag, hosted
publication or unrelated source file was changed. Runtime originals remain
private and excluded from Git; public paths are substitutions, outputs are
labelled shortened, and the sole screenshot crop preserves genuine pixels.
