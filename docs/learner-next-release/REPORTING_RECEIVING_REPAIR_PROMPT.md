# Data Intelligence — diagnose and repair combined-release Reporting failures

Prepared for owner assignment to a **fresh Data Intelligence chat**. This replaces
the earlier R1-only repair prompt. When assigned, diagnose and repair R1, R2 and R5
below, then deliver a verified application artifact for Pipeline receiving.
Proceed independently within scope. This does not resume all outstanding 08C work.

## Background and authority

Checkout: `C:\Users\nateb\Documents\ck3chronicle`. Paths below are relative to
this checkout; document links are relative to this prompt.

CK3Chronicle protects completed CK3 logs, classifies their diagnostics, preserves
native evidence in SQLite/review shards, and reports from stored records. Learner
has published package **`4ac4e8ee92346e6d14eacfbf`**, combining learner v61,
parser v1.8, matcher v3, model schema 6 and the corrected shared decoder. SQLite
remains schema 3. The new model supports richer literal and repeated layouts.

Pipeline has completed receiving: genuine ingestion/storage checks passed for
172,130 new-package units, including native reconstruction, captured values and
unresolved review preservation. Reporting failed on those stored results. The
combined application is not accepted end to end; production activation has not
occurred. Data Intelligence owns Reporting repairs; Pipeline retains integration
receiving and cutover coordination. Learner owns retained executable/model
packages. This repair does not require another model build.

**R2 is already owner-accepted as nonblocking for activation.** Its repair is now
assigned here; this does not reverse that acceptance. Track each repair separately:
deliver completed repairs if R2 needs further work, and retain its unfinished
obligation explicitly. Do not ask for its disposition again or claim all repairs
complete when only part of the assignment is complete.

## Focused orientation

Read these current sections first; follow history only as needed:

- [AGENTS.md](../../AGENTS.md), [development environment](../DEVELOPMENT_ENVIRONMENT.md),
  and current openings of [status](../PROJECT_STATUS.md), [plan](../PROJECT_PLAN.md)
  and [handoff](../CURRENT_HANDOFF.md).
- [Pipeline receiving](PIPELINE_RECEIVING.md), especially R1–R5 and evidence limits;
  [release README](README.md) and [final intake](HANDOFF.md#final-identities-and-pipeline-intake).
  [Cutover](PIPELINE_CUTOVER.md) provides installation context, not permission to
  execute its production commands.
- [08B Reporting handoff](../TASK08B_REPORTING_HANDOFF.md): current checklist,
  interfaces and CLI/export behavior; [08A.1 query handoff](../TASK08A_1_DIAGNOSTIC_QUERY_HANDOFF.md):
  current filtering, identity and rendering provenance.
- [Error Contract](../ERROR_CONTRACT_SPECIFICATION.md) and relevant repeat/literal
  sections of [native model contract](../LEARNER_NATIVE_MODEL_CONTRACT.md).
  Inspect actual delivered definitions rather than extrapolating from old examples.
- [08C corrective handoff](../TASK08C_HANDOFF.md#pre-integration-corrective-complete--2026-10-05)
  and API/display sections of [encoding recommendation](../TASK08C_ENCODING_RECOMMENDATION.md).
  Decoder implementation is delivered; this is context, not another encoding study.

Newer owner dispositions/receiving evidence supersede older pending statements,
particularly requests for R2 disposition and any timestamp prerequisite for
nonchronological Run listing, querying or reporting. Do not read the rejected shared-
database-handler design or its continuation files.

Owning code: `src/ck3chronicle/reporting/analysis.py`, `query.py`,
`presentation.py`, `cli.py`, `presets.py` and their callers/templates. Consult
`src/ck3chronicle/pipeline/contracts.py` for rendering/binding semantics and
`src/ck3chronicle/decoder.py` for native/display separation. Preserve concurrent
changes; do not revert whole files to older receipts or silently include unrelated
changes in the repair artifact.

## Exact evidence and baseline

Evidence root **P**: `.codex-tmp/pipeline-receiving-20261005/`.

| Files under P | Purpose |
|---|---|
| `receipt.json`, `database.json` | Completed receiving results and exact disposable database path |
| `report-layout-defects.json`, `receive-report-layout-failure.log` | Affected definitions/records and original R1 traceback |
| `report-cli-results.json` | Executed commands, arguments and exit statuses |
| `stored-surrogate-export.json`, `surrogate-stored-witness.json` | R2 failures and actual preserved SQL/handler values |
| `context/config.toml` | Disposable configuration; inspect before running commands |

Database:
`P/context/runtime/disposable/ck3chronicle-schema3-20261005T060419Z.sqlite3`.
Use its existing genuine Runs through `pipeline.request_handler.HandlerClient`.
Do not rerun ingestion/registration scripts merely to reproduce reports.

Tested installation:
`.codex-tmp/combined-release-20261005/installed-corrected/`.
Original application wheel:
`.codex-tmp/combined-release-20261005/application-corrected/ck3chronicle-0.0.1-py3-none-any.whl`.
SHA-256:
`362b09b2d553f7610a1cf5e8b848000af610ef48f4c8c1b5bba739223586316b`.
Keep these and original failure receipts unchanged. Write new checks/outputs under
a separate ignored repair directory and record its exact path.

## 1. Repair new-template reporting (R1)

`DiagnosticAnalysis.investigate` and root-CLI `frequent` reports raise
`KeyError: 'prefix'` in `reporting.analysis.template_text`. It assumes every
non-literal part has simple-slot `prefix/type/suffix`; delivered `kind: repeat`
parts violate that assumption. JSON, HTML and text reports all exit 1.

| Genuine input | Existing disposable Run | Affected definition/record/occurrence inventory |
|---|---|---|
| Original `20261003-IS3QON` | `20261005-BND9AS` | 17 definitions; 1,012 records; 54,967 occurrences |
| Original `20261002-2PVVSE` | `20261005-OSPK8G` | 19 definitions; 1,136 records; 8,003 occurrences |

These inventories can share definitions. Both complete reports fail, not just
display of the listed records.

Confirm all delivered structures implicated by the failure. Inspect their
Reporting consumers: template presentation/filtering, typed bindings, message
provenance, grouping and exports. Extend the existing implementation consistently
with the contract. This is a focused compatibility repair, not a Reporting
redesign or a missing-key-default patch.

Distinguish template definitions from bound diagnostic instances. Represent
repeatable sections meaningfully without inventing fixed repetition counts.
Preserve actual locator values/order, literal alternatives, dates, native captures,
identities, counts and filtering semantics. Do not suppress failures with empty
defaults, generic unknown text, dropped records or flattened repeated bindings.

## 2. Repair preserved-byte exports (R2)

Session 55 is Run **`20261005-XH88PI`**: 99,991 supported and 12 provisional
occurrences. All 44 occurrences containing preserved undecodable bytes survived
storage and exact reconstruction. Installed JSON/HTML/text export helpers raise
`UnicodeEncodeError: surrogates not allowed` on those actual stored values.

Repair serialization/presentation at the export boundary. Reuse existing display
facilities where appropriate. Preserve native processing/storage strings and
machine identities; display escapes must be clearly representational. Do not
silently discard/replace bytes or change valid Unicode. Keep filtering, counts
and provenance based on native values. Check main output and applicable appendix
paths, including the demonstrated possibility of created/truncated output from an
encoding failure; avoid expanding this into a general I/O redesign.

The retained session lacks original source-log modification time. Existing CLI
selection rejects it before export, even with history disabled. The owner has
confirmed that this is another Reporting defect, **R5 below**, not a permissible
restriction on a single-Run report. The original R2 receipt therefore establishes
stored-value helper failures only. Repair R5 and verify this genuine Run through
the actual CLI as well; retain the original timestamp as unavailable.

`decode_fragment` returns plain `str`; it supplies no warning/status metadata.
Keep parser framing/recovery, fragment decoding and physical-source decoding
semantics unchanged. No ingestion warnings, admission rules or new storage fields.

## 3. Remove timestamp prerequisites from all nonchronological operations (R5)

Owner clarification: ingestion is permitted without a captured timestamp.
**Only chronological reporting depends on that timestamp. Everything else must
function normally.** This includes ordinary lists of Run IDs, searches for all
Runs containing a given error message, single-Run queries/reports, filtering,
counts, grouping and exports. Apply legitimate query/package filters normally;
missing time must not silently remove an otherwise matching Run.

`DiagnosticAnalysis.list_runs` currently filters through `chronology` before
pagination. `investigate` selects even an explicit Run ID only from that eligible
list, before examining whether history is requested. The underlying public-handler
Run listing does include missing-time Runs. Repair Reporting's use of chronology
across discovery, selection and search, not just the single-Run exception.
Separate ordinary eligibility from chronological placement. Preserve unknown-Run
and wrong-package errors, correct totals and pagination over all matching Runs.

Ordinary Run listings and searches must include missing-time Runs without forcing
the caller to opt into a special workaround. Display their date as unavailable;
any presentation ordering must not claim an inferred session time. Cross-Run
message search must not accidentally search only the chronological history window.
Single-Run reports must work, including the normal named-Run command and
`--no-history`. When optional history cannot be placed, retain the ordinary query
or report results and disclose unavailable chronological context.
Do not fabricate preceding/subsequent positions, trends, newly-observed claims or
zero observations. Operations that require time ordering, including chronological
`latest` selection, must continue to disclose/exclude unplaceable Runs honestly.
Do not substitute ingestion time, Run-ID order or another timestamp, and do not
backfill the stored metadata.

Use genuine Run `20261005-XH88PI` to verify ordinary Run listing, a search for
all Runs containing an actual stored error message, public analysis and installed
root-CLI JSON/HTML/text reports with and without optional history. Establish
expected matching Run IDs from actual handler-returned records; do not invent an
error scenario. Confirm missing time remains missing, counts/values and pagination
are correct, and timestamped Runs retain chronological behavior. Track selection
repair separately from R2 if exports remain unfinished. No new ingestion,
synthetic missing-time fixture or metadata edit is needed.

## 4. Compatibility and separately accountable work

Old-package control: original `20261003-D3N7ZQ`, disposable Run
**`20261005-DQT13M`**, package `68f1ae5db205ab46afef9c4d`. It already reports
successfully in this database. Preserve package-scoped history and honest
unavailable outcomes; cross-package absence is not a zero or comparable trend.

The `syntax` preset supports only the old package/model (R4). Keep its explicit
new-package rejection unless retained genuine evidence establishes correct new
selectors and you verify them. Do not relabel old selectors, invent a taxonomy or
start another corpus campaign. State whether R4 is received or remains separately
owned Reporting work; repairing R1/R2/R5 does not automatically close it.

The original wheel's default points to an unshipped `candidates/` directory (R3).
Learner/application packaging owns this; Pipeline has verified explicit new and
rollback selections. Use that documented arrangement in your separate repair
installation, recording overrides. Read `P/deployment-receipt.json`,
`P/rollback-installed-selection.json` and cutover's input section. Do not use the
checkout's old selection verbatim as installed rollback, modify Pipeline's staged
environment or claim the delivered wheel's default is fixed. Identify remaining
packaging actions precisely for their owner.

## Verification and delivery

Reproduce from existing genuine evidence and compare before/after on the same Runs.
Check failed R1 commands in JSON/HTML/text, relevant template-text/typed-binding
filters, counts/grouping, repeated data and representative rendered output.
Verify R2 stored-value exports, R5's Run listing/message search/named-Run CLI and unchanged
inverse byte reconstruction; check old-package compatibility. A full CLI check
means invoking the installed root `report` command and inspecting its actual
output, not merely calling an export helper. Inspect contents, not just exit codes.
Unavailable cases remain explicit. Reuse passing storage/full-corpus receipts.

Creation **or** execution of each synthetic test requires specific owner approval;
this assignment provides none. No mock clients, injected failures, invented
histories/timestamps or new evidence campaigns. Run the required runtime logging
ownership check for runtime changes.

Build a **new application wheel** using existing packaging mechanics in
[RELEASES.md](../RELEASES.md) and the final handoff. Use fresh build/install
directories to avoid the stale-wheel problem already encountered in this release.
Authenticate changed source against the wheel/installation, retained package pins
and dependencies. Verify representative installed reports without ambient checkout
modules, using explicit disposable configuration. Record source identity, artifact
path/SHA-256, commands and selection arrangement. Preserve retained learner/model/
parser distributions and the original tested installation. If another owner must
finish packaging, deliver the exact dependency; do not claim installed completion.

Append one concise repair section to [Pipeline receiving](PIPELINE_RECEIVING.md):
root causes, changes, genuine before/after evidence, artifact identity, receiving
commands, each defect's disposition and remaining owner/action. Update the current
[08B handoff](../TASK08B_REPORTING_HANDOFF.md) and release README/HANDOFF with short
pointers/status corrections; preserve original receipts and historical identities.
Distinguish checks you performed from inherited receipts.

Pipeline receives the installed repair and updates cutover; the owner decides
activation. Finish with separate R1/R2/R5 results and **READY FOR PIPELINE RECEIVING**
only for delivered, verified scope, otherwise name the exact remaining repair or
packaging dependency. R2's nonblocking status never hides unfinished work.

No live selection switch, runtime service restart, production ingestion, database
reset, historical reprocessing, commits or pushes. Broader 08C folder filters,
source search/beta analytics and new learner/model work remain outside this task.
