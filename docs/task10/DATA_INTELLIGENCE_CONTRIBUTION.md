# Task 10D — Data Intelligence documentation contribution

2026-10-08. Producer **Data Intelligence**, **TREK-13**; receiver Launch &
Distribution / Docs, **TREK-11**. Authority: the owner-issued
[component prompt](../task10-deliverables/COMPONENT_DOCUMENTATION_INPUT.md),
[10D](../task10-deliverables/10D_PRODUCT_REFERENCE.md),
[10E](../task10-deliverables/10E_USER_WORKFLOWS.md) and
[working agreement](../task10-deliverables/WORKING_AGREEMENT.md).
Task 09 remains completed. This assignment supplies documentation only.

## Editorial boundary

Proposed canonical manual section: `docs/user/DATA_INTELLIGENCE_REFERENCE.md`,
linked from the CLI/configuration references. Placement coordination is TREK-11
CMT-94. Until Docs confirms placement, the ready-to-integrate reference below is
the technical contribution. Docs owns shared manual/index/coverage edits and
records receipt on TREK-13; final manual acceptance remains on 10C. Do not retain
two independently maintained versions of the reference after integration.

## Release and verification

Reference revision **data-intelligence-0.0.2-r1** describes the actual delivered
application **0.0.2**, wheel SHA-256
`2de516e02aae2e858f1b2f2d34a5ec89ba69306e7001477c29d1857d9ffbd594`.
The Task 09 source baseline is commit
`709ea7842a0202c420b43355b18be91d8ca196a3`, tag
`task09-baseline-2026-10-07`; Task 10 application changes are uncommitted and
identified by the wheel manifest, not by that baseline tag alone.
Model default: package `2b12932103f3a3111a4e1880`, manifest
`02c70654c3ffa9678df80108985206a12c92bb67b0c36311fbec393b329e1505`.
Reports use each Run's stored lineage, not the current processing default.

Fresh read-only inspection authenticated the wheel and all **14** relevant
source/wheel/manifest members: twelve Reporting files/resources and the shared
root CLI/configuration. No command that starts a handler, produces a report,
ingests, builds or changes application state was executed for this contribution.
No synthetic test was created. Local inspection evidence and exact hashes are in
ignored `.codex-tmp/task10d-data-intelligence/evidence-inspection.json`; the
inspection script is beside it. All twelve Reporting members also match the
prior received installed application used for E3; shared CLI/config changes are
covered by E1 instead. The four E1 command receipts have exit 0; their JSON totals
agree with both stored counters and the retained external SQL result. All twelve
local document links resolve and all three fenced JSON examples parse. These
are static document/receipt checks, not new product acceptance tests.
Prior runtime evidence remains outside Git.

| Evidence | What is reused and where to inspect it | Limit |
|---|---|---|
| E1: delivered 0.0.2 | `.codex-tmp/task10a1/release/{artifact.json,commands.json,verification.json,stored.json,report-text.stdout,report-json.stdout,report-html.stderr,data/report.html}`; [Pipeline handoff](PIPELINE_HANDOFF.md); TREK-9 CMT-81/83 | Genuine capture `20261003-D3N7ZQ`, SHA-256 `5a7b93d8ee374c60f767593631713eaf8719004ba4f9cf33e7eb5d812dbec629`; Run `20261008-VZP1CG`. Installed runs and frequent text/JSON/HTML commands exit 0. Report has 1,066 records / 1,838 occurrences, agreeing with stored read-only SQL evidence. This is reused execution, not a new run. |
| E2: external installation | `.codex-tmp/task10b/single-setup/{placement-receipt.json,verification.json}`; [distribution handoff](DISTRIBUTION_HANDOFF.md#external-candidate-4-receipt-and-gui-correction-in-progress) | Owner-executed candidate 4, same application, genuine Run `20261008-P8KHM4`, same capture hash; text/JSON/HTML exercised and repeat setup preservation passed. Candidate 9 reuses these unchanged application checks; it did not independently ingest/report. No clean-machine or full lifecycle claim. |
| E3: query/history/source semantics | `.codex-tmp/trek5-reporting-20261006/changed/receipt.json` and its named command/stdout files; `.codex-tmp/trek6-removal-20261007/{output-review.json,installed-receipt.json,installed-supplement.json}`; [08B handoff](../TASK08B_REPORTING_HANDOFF.md), [combined receiving](../learner-next-release/OBSERVER_FREE_PIPELINE_RECEIVING.md) | Received TREK-5 is completed. Ten genuine commands, nine exit 0 and the known syntax/package restriction exit 2; thirteen replacement-output comparisons, preserved-byte evidence, missing-time semantics and actual content search/cache evidence. Reporting bytes are unchanged in 0.0.2. Old config/bootstrap examples are superseded by 0.0.2. |
| E4: earlier advanced examples | [08B handoff](../TASK08B_REPORTING_HANDOFF.md#worked-trailing-five-investigation), [example definitions](../../examples/reporting/README.md) and their linked ignored receipts | Genuine historical query/preset/history results apply only to the recorded packages and Runs. They are not new 0.0.2 installed walkthroughs or evidence every flag combination was exercised. The owner-authorized fake-LOCATOR fixture remains separately labelled synthetic and is not used as genuine acceptance here. |

E1's exact command arrays, cwd and exits are in `commands.json`; stdout/stderr
are named by command. Its JSON result has `status: completed`, Run
`20261008-VZP1CG`, `totals: {occurrences: 1838, distinct_records: 1066,
historical_entries: 0}`. `records` contains 50 displayed records; those 50 are
not the total. This is a bounded genuine example, not a prediction for a user's
database. E2 supplies the installed CMD-launcher route. Public examples below
substitute paths and, where indicated, Run/template IDs; originals remain private.

## Discrepancies and limits for Docs

- Use the team name **Data Intelligence**. The Python package/legacy task name
  `reporting` still names the implementation and is not renamed by this task.
- Older 08B prose says cwd `config.toml`, timestamp-filtered Run listing and
  rejection of directly named Runs without timestamps. Those statements are
  superseded. The reference below follows delivered code and current owner rules.
- The `syntax` preset really is restricted to package
  `68f1ae5db205ab46afef9c4d` / model `f5cde2616f35d563118d3d32`; the current
  full-model default cannot use it. This is the existing R4 limitation, not a
  documentation-authorized repair or a new implementation assignment.
- Escaping process/transport/source/export failures, interrupted output and other
  absent fault cases remain unverified; their documented handling is source
  inspection, not manufactured execution. No new defect was demonstrated.
- Final installed manual walkthroughs and acceptance belong to Docs/10C.
  Changes to these interfaces must update the canonical reference and its example
  evidence with the owning implementation delivery.

---

## Ready-to-integrate user reference

# Data Intelligence reference

Applies to application **0.0.2**. Data Intelligence lists stored Runs, investigates
diagnostics, compares history and exports reports. Complete `template` and
`provisional` assignments are included. Native unresolved review evidence remains
separate and is not searched as diagnostic rows.

### Before running a command

Use the terminal in your installed Windows bundle directory. The examples use
PowerShell and `ck3chronicle.cmd`. An installation exposing the application console
entry point can use `ck3chronicle` with the same arguments. Complete setup first;
use its existing database containing genuine processed Runs. Commands use the
public database handler and may start its compatible process if none is running.
They do not ingest, reclassify, change model selection or edit game/mod sources.
They create invocation journals and may create output directories/files. Source
content search may use temporary decoding files and the configured ripgrep tool.

Global `--config PATH` goes **before** `runs` or `report`. Without it, the fixed
Windows `%LOCALAPPDATA%\ck3chronicle\paths.toml` is used; there is no cwd config
search. `--database PATH` overrides `watcher.database` for that invocation but
does not remove the configuration prerequisite. CLI paths are relative to the
invocation directory; TOML paths are relative to the selected TOML file.
See [application configuration](../user/PIPELINE_REFERENCE.md) and
[installation](../user/DISTRIBUTION_REFERENCE.md).

Query/context JSON changes take effect on the next report invocation. They do
not need a watcher restart. Persistent configuration changes follow the shared
configuration/handler maintenance rules in the application reference. Current
source-file changes affect subsequent searches; reports are not historical source
snapshots. Existing HTML/JSON/text exports do not update themselves.

### List Runs

```text
ck3chronicle [--config PATH] runs --package-id ID
  [--database PATH] [--format text|json] [--offset N] [--limit N]
  [--output PATH] [--log-dir PATH]
```

| Argument | Type, default and meaning |
|---|---|
| `--package-id` | Required nonempty stored processing package ID. Find it in Run lineage or a known processing receipt; the active processing selection is not implicitly used. |
| `--database` | Existing database path; default configured `watcher.database`. |
| `--format` | `text` (default) or `json`; no HTML listing. |
| `--offset`, `--limit` | Integers >=0; defaults 0 and 50. Pagination follows package selection and Run-ID ascending ordering. Zero limit returns no displayed rows. |
| `--output` | UTF-8 file path; omitted means stdout. |
| `--log-dir` | Invocation journal directory; omitted uses configured runtime logging. |

The listing includes Runs without usable source timestamps. Run-ID order is not
session chronology. JSON includes `runs`, `eligible_count`, `offset`, `limit`,
`ordering`, `package_id`, `chronology_exclusions`, `database` and `status`.
`eligible_count` is the whole package's Run count before pagination;
`chronology_exclusions` explains why some listed Runs cannot enter time windows.

Example: reused installed execution, with user-path substitutions. Select your
actual stored package; this ID is the delivered default model.

```powershell
.\ck3chronicle.cmd --config 'D:\Chronicle\paths.toml' runs --package-id 2b12932103f3a3111a4e1880 --format json
```

### Investigate and export

```text
ck3chronicle [--config PATH] report RUN_ID|latest
  (--preset hotspots|frequent|syntax|new|symbol | --custom)
  [--query PATH] [--database PATH] [--package-id ID]
  [--format text|json|html] [--output PATH]
  [--limit N] [--historical-limit N] [--no-history] [--verbose]
  [--source-context PATH] [--source-root ABSOLUTE_PATH ...]
  [--source-directory RELATIVE_PATH ...] [--no-recursive]
  [--ripgrep EXE] [--log-dir PATH]
```

Repeat the **flag** for each source root/directory. Choose exactly one preset or
`--custom`; custom requires `--query`. A named Run supplies its stored package;
an explicitly conflicting package fails. `latest` requires `--package-id` and
selects the greatest usable original error-log modification timestamp in that
package. Processing time, Run ID and current model selection do not choose latest.

| Option | Type, default and effect |
|---|---|
| `--query` | UTF-8 JSON object file; a UTF-8 BOM is accepted. Adds conditions to a preset or supplies the custom investigation. |
| `--format`, `--output` | Text default; JSON/text default to stdout. HTML requires an output path. Files are UTF-8. Existing destinations are overwritten and missing parent directories created. |
| `--limit` | Integer >=0; overrides `display.limit`; CLI effective default 50. Bounds selected and each comparison Run's detail list. |
| `--historical-limit` | Integer >=0; overrides `display.historical_limit`; CLI effective default 20. Separate previously observed detail bound. |
| `--no-history` | Switch, default off. Sets both history and absent-history display off; conflicts with trailing/newly-observed conditions. |
| `--verbose` | Switch, default off. Adds current source excerpts. HTML may create a linked `NAME-sources.html` beside `NAME.html`; keep both together. |
| `--source-context` | Optional source-selection JSON object file. Supplies context without restricting diagnostic membership. |
| `--source-root`, `--source-directory`, `--no-recursive` | Override optional context `roots`, `directories`, `recursive` respectively. Roots must be absolute. Directory values stay relative to each root. |
| `--ripgrep` | Explicit executable overrides configured `tools.ripgrep`. No configured executable means content search is unavailable; no ambient tool discovery. |
| `--database`, `--log-dir` | As for `runs`. |

Required `scope.source` fields override optional context of the same name, even
when that context came from CLI flags. Other optional context fields remain.
CLI display limits override query limits. Preset conditions are ANDed with user
conditions; they are not replaced by query JSON. `purpose` is explanatory text.

Text/HTML bound ranking tables too; JSON keeps complete rollups and identity maps,
so a low limit does not necessarily make a small JSON file. Totals are calculated
before display truncation. HTML is offline, with embedded CSS and no required
server, JavaScript or remote assets. Output must differ from database/query/context
inputs; use dedicated report paths. Main/appendix output is not an atomic pair.

Reused genuine frequent-report example, with paths substituted. Text and JSON
use the same arguments except `--format` and destination:

```powershell
.\ck3chronicle.cmd --config 'D:\Chronicle\paths.toml' report latest --package-id 2b12932103f3a3111a4e1880 --preset frequent --format html --output 'D:\Reports\frequent.html'
.\ck3chronicle.cmd --config 'D:\Chronicle\paths.toml' report latest --package-id 2b12932103f3a3111a4e1880 --preset frequent --format json
```

The genuine received 0.0.2 example returned exit 0 and this shortened JSON
excerpt (your results depend on your stored Runs):

```json
{"status":"completed","totals":{"occurrences":1838,"distinct_records":1066,"historical_entries":0}}
```

### Presets

| Preset | Actual condition |
|---|---|
| `frequent` | All exact diagnostic records in the effective scope, ordered by descending selected-Run occurrences then exact identity key. No minimum frequency or severity threshold. |
| `hotspots` | Requires an identifiable stored script/file reference. Current file existence is not required. Ranks emitters, referenced paths and candidate associations separately. |
| `new` | Present now and absent from every successfully read included predecessor. No predecessor means positive records are new within that window. Check comparison completeness. |
| `symbol` | Query must contain `templates`, `template_text`, `template_exact` or typed `bindings`, directly/in an AND clause, or in every OR-selector branch. Exact identities remain separate. |
| `syntax` | Nine verified template/family/model selectors for package `68f1ae5db205ab46afef9c4d`, model `f5cde2616f35d563118d3d32` only. Both match statuses are eligible. Other packages, including the delivered default, return exit 2. This is not a complete syntax-error taxonomy. |

Copyable variants below are **unexecuted as written**, with substituted Run IDs
and paths. Applicable earlier genuine preset/query receipts exist, but do not
prove these substitutions match a particular user's data. Replace `<Run ID>`
with a stored Run and create the JSON described below for `symbol.json`.

```powershell
.\ck3chronicle.cmd report '<Run ID>' --preset hotspots --format html --verbose --output 'D:\Reports\hotspots.html'
.\ck3chronicle.cmd report '<Run ID>' --preset new --format text
.\ck3chronicle.cmd report '<Run ID>' --preset symbol --query 'D:\Queries\symbol.json'
.\ck3chronicle.cmd report latest --package-id 68f1ae5db205ab46afef9c4d --preset syntax
```

These variants use the default setup config. Add global `--config` if needed.
The syntax command requires actual stored Runs in its named historical package.

### Editable query JSON

A query is an object with only `scope`, `refinement`, `analytics`, `display` and
`purpose`. All are optional; omitted filter fields impose no restriction. Unknown
keys, wrong types and empty selector/text-group lists are errors. An empty `{}`
is a valid unrestricted custom query. Opposing valid filters give an empty result.

| Section/field | Type and meaning |
|---|---|
| `scope.source_families` | Nonempty list of exact emitter family strings, ORed. These are engine emitters, not mod file paths. |
| `scope.has_source_reference` | Boolean; selects presence/absence of a usable stored script/file reference. |
| `scope.source` | Nonempty source-selection object, described below; required diagnostic filter. |
| `refinement` | Record predicates described below, ANDed with scope. Default `{}`. |
| `analytics.history` | Boolean, default true. |
| `analytics.trailing_runs` | Integer >=1; selected Run plus at most N-1 predecessors, no successors. Omitted means up to five predecessors and five successors. |
| `analytics.include_absent` | Boolean, default equal to history. Includes the separate preceding-window identities absent from selected Run. |
| `display.limit`, `display.historical_limit` | Integer >=0 or null. Omitted/null becomes 50/20 through the CLI. Zero hides that detail list, not its totals. |
| `purpose` | String, default empty; CLI supplies preset/custom explanation if empty. Never a filter. |

History false cannot be combined with `trailing_runs`, any `newly_observed`
condition (even false), or explicit `include_absent: true`.

Record predicates are allowed directly in refinement and in each
`refinement.all` clause. The `all` list is nonempty and ANDs its nonempty clauses;
clauses cannot themselves contain `all`.

| Record predicate | Type and matching rule |
|---|---|
| `source_families` | Nonempty exact-string list, OR. |
| `match_status` | Nonempty list containing `template` and/or `provisional`, OR. |
| `templates` | Nonempty OR list of objects with required nonempty `template_id`; optional exact `model_revision`, `contract_version`. |
| `identities` | Nonempty OR list of complete returned `identity` objects; copy them from a report. A digest, ordinal or template ID alone is insufficient. |
| `bindings` | Nonempty AND list. Each object requires nonempty `type` and exact `value`; optional `region`, `slot_id`, `present` (boolean, default true). A present value is a string (including empty); absent requires `present: false, value: null`. Each predicate must match a binding. |
| `message` | Literal text condition over the complete rendered diagnostic, including bound values. |
| `template_text` | Literal text condition over stored body template literals and `<TYPE>` placeholders, excluding instance binding values. Repeat layouts describe the template, not occurrence count. |
| `template_exact` | Nonempty OR list of exact case-sensitive returned template-text strings. |
| `selectors` | Nonempty OR list of nonempty objects containing only the eight predicate fields above (not `selectors`, counts, newness or `all`). Fields within a selector are ANDed. |
| `occurrences` | Object with optional inclusive `min`/`max`, integers >=0. Counts are anchored to the selected Run, including zero for historical entries. |
| `newly_observed` | Boolean relative to included successfully read predecessors; requires chronological history. |
| `has_source_reference` | Boolean as in scope. |

Literal text conditions use exactly one `contains` or `not_contains` nonempty
string, with optional boolean `case_sensitive` (default false). Or use a single
`and`/`or` key containing a nonempty list of nested conditions. These are literal
substrings, not token boundaries, regular expressions, SQL or Python expressions.
Case-insensitive matching uses Unicode case folding. A message match can come
from a template literal or populated slot; returned provenance identifies its
origin without assigning a new classification.

Save this illustrative query as `D:\Queries\context-switch.json`. **Unexecuted
as written here**; its emitter/phrase/trailing-five form has earlier genuine
history evidence. Counts are not promised for your package or Run.

```json
{
  "scope": {"source_families": ["jomini_script_system.cpp"]},
  "refinement": {"message": {"contains": "failed context switch"}},
  "analytics": {"trailing_runs": 5},
  "display": {"limit": 20, "historical_limit": 10},
  "purpose": "Compare context-switch diagnostics across recent Runs"
}
```

```powershell
.\ck3chronicle.cmd report '<Run ID>' --custom --query 'D:\Queries\context-switch.json' --format json --output 'D:\Reports\context-switch.json'
```

For `symbol.json`, copy a returned template ID into
`{"refinement":{"templates":[{"template_id":"<returned template ID>"}]}}`.
To select a single exact identity instead, use
`{"refinement":{"identities":[<complete returned identity object>]}}`.
These two inline forms are substitution instructions, not literal ready-to-parse
JSON files. Do not confuse whole-template selection with one exact diagnostic.

An identity contains `definition: {template_id, model_revision, contract_version}`
and `equality: {template_id, regions}`. Each region carries `name`, `layout`,
`component_index`, `bindings`; each binding carries `slot_id`, `type`, `value`,
`present`. Preserve the returned values/layouts instead of authoring or simplifying
them. Generated report envelopes, stored records, lineage, captured playsets and
model/contract payloads are not runtime-editable settings. Query files may embed
returned identity values; editing those values does not alter stored evidence.

### Source selection and context

Use the same source-selection fields in `scope.source` and optional
`--source-context` JSON, except `resolution` is permitted only in `scope.source`.
Without explicit roots/member restrictions, searches use the selected Run's
recorded playset. This is not today's launcher playset or automatic root discovery.

| Field | Type, default and meaning |
|---|---|
| `roots` | Nonempty list of absolute directories, in caller order. Without `members`, explicit roots work independently of captured membership. With `members`, restrict selected stored members to matching roots. |
| `members` | Nonempty OR list of stored-member selectors. Within an object fields are ANDed: `load_order` integer >=0; `name`, `path`, `root_ID`, `stable_id`, `descriptor_path` exact nonempty strings or null. At least one field required. |
| `directories` | Nonempty list relative to each selected root; default root itself. `.` is valid; no parent traversal, drive colon or absolute directory. Explicit relative fields accept a leading `/`. |
| `recursive` | Boolean, default true; false searches only the selected directories. |
| `files` | Nonempty list of exact physical absolute paths or root-relative paths. |
| `referenced_paths` | Nonempty list matching stored paths; default relative-path matching. |
| `filename`, `relative_path` | Nonempty object with `exact` (nonempty OR string list) and/or `text` (literal text condition). Both fields, if supplied, must match. Relative exact paths normalize slashes and may start with `/`. |
| `extensions` | Nonempty string list; dot optional, e.g. `txt` or `.txt`. |
| `filename_globs`, `path_globs`, `include`, `exclude` | Nonempty glob-string lists. Filename globs inspect basename; other globs inspect relative path. Each positive field requires any match; any exclude match vetoes. These use shell-style fnmatch matching, not regex or gitignore rules. |
| `case_sensitive` | Boolean, default false for path matching. Text/content leaves use their own case setting. |
| `content` | Literal text condition, evaluated per candidate file as a whole. Each AND term may occur on a different line. Requires readable current files and configured/explicit ripgrep. |
| `reference_mode` | `relative` (default) or explicit broader `basename`; basename can associate unrelated same-named files. |
| `resolution` | `resolved` or `unresolved`, only in required scope. At least one selected reference must have that result. Unresolved means a completed search found no candidate, not that search was unavailable. |

Fields are ANDed unless their list/group explicitly supplies alternatives.
Path-only required scope selects stored references independently of disk existence;
no-path/nonmatching records are ordinary nonmatches. Reports still offer optional
current candidate context for those records. Root/member/content/resolution filters
need current-source evaluation; incomplete required evaluation returns exit 3,
with partial evidence. Optional context problems leave stored membership intact
and appear in coverage. A pathless diagnostic is complete by design; source lookup
is not applicable, and an entirely pathless selection does no source traversal.

Unscoped inventories can inspect whole selected roots recursively. Member/root and
directory restrictions narrow traversal first; exact relative paths/references
narrow candidate lookup to their parent directories. Search counts include examined
names/paths before content filtering and include cached inventories; folder counts
include starting and empty folders. Per-root rows can overlap and are not additive.
New investigations clear caches; timing/counts are coverage facts, not a benchmark.

For each referenced file/line, the last matching recorded playset member in load
order is the report's assigned source when a line and unique last member are
available. Missing lines, unavailable load order and ties leave attribution
unassigned with a reason. Other matches remain visible. Explicit
outside-playset roots cannot establish recorded load order. Content filtering does
not promote an earlier copy to the assigned source. This rule does not prove a
mod caused the error. Excerpts show the current referenced line plus up to ten
lines on each side; unavailable/out-of-range lines and decoding/header findings
are labelled. A resolved path does not certify encoding or historical contents.

Example of a user-editable path-only query (unexecuted substitution; replace the
path with a stored reference):

```json
{"scope":{"source":{"relative_path":{"exact":["common/on_action/sea_minority_on_actions.txt"]}}}}
```

Add `"resolution": "unresolved"` inside `source` only when the question is
whether the current selected source scope lacks a candidate. This changes the
question from stored-path matching to current filesystem observation.

### Interpret totals, history and statuses

A distinct record is an exact, definition-scoped contract identity. Occurrences
count how often that identity occurred in the Run. Template and provisional are
stored assignment statuses, not severity or numerical confidence. A template
rollup can contain many exact identities. Review shard units/emissions are separate
unresolved evidence; do not add them to diagnostic-row counts or assume the database
reconstructs the original error.log.

JSON reports include `run`, `package_id`, `effective_query`, `filter_meaning`,
`chronology_exclusions`, `window`, `totals`, `records`, `historical`, `rollups`,
`review`, `coverage`, `status`, `presentation` and `explanation`. Each record carries
its full `identity`, `identity_key`, stored assignment, rendered message, template
text, selected count, history, references and candidate/source facts. Run-local
ordinals are provenance, not cross-Run identity. Generated output is evidence;
keep the editable query separately for rerunning.

`totals` describes the selected Run. `window.totals` sums successfully read included
Runs and counts distinct full identities across them. `historical` lists identities
seen in predecessors but absent now, separate from current records. Occurrence and
newness filters remain anchored to the selected Run even in per-Run views.
Referenced/candidate buckets can overlap: consult overlap and
`bucket_totals_are_additive` before summing. Engine `.cpp` emitters are not script
source paths. Row limits never change the complete computed totals.

History uses usable offset-bearing source-log modification timestamps within one
package. Equal timestamps do not trigger reporting deduplication. A named Run
without a usable timestamp is still reportable; chronological context and novelty
are unavailable. Novelty filters on it fail with exit 2. Missing window positions
are shown as unavailable, not invented zero-count Runs. A successful read with no
matching identity is zero; a failed/unavailable read has null counts and a reason.
Observation fractions use successful reads only. Newness and absence are relative
to this included window, not proof of first-ever occurrence or a confirmed fix.

`status: completed` and exit 0 mean the investigation completed, including a valid
empty result. They do not prove all optional source/history evidence is available.
Inspect `window.complete`, `coverage.comparison_errors`,
`coverage.comparison_unavailable`, per-Run source issues and filter completeness.
Source-reference presence (`present`/`no_path`) differs from each reference's
resolution (`resolved`, `unresolved`, `outside_scope`, `not_searched`, `incomplete`).

| Exit | Meaning at the reporting command boundary |
|---|---|
| 0 | Completed, including empty list/result; read the coverage fields. |
| 1 | Read unavailable or operation/output failure. Failure status is `read_unavailable` or `operation_failed`; an output failure can prevent writing the result. |
| 2 | Invalid query, unsupported syntax package or Run selection conflict/unavailability: `invalid_query` or `run_selection_error`. Parser/configuration errors also use 2 and may only print stderr. |
| 3 | `source_filter_incomplete`: required source filtering cannot be fully evaluated. Partial known matches are not a complete zero/result. |

Reporting errors print stderr and attempt the requested structured JSON or readable
text/HTML failure output. If output itself fails, stderr is the remaining result;
do not assume an export was saved. These mappings describe ordinary reporting
handling, not a guarantee for process termination or every bootstrap failure.
