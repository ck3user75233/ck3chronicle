# Trusted Run completion pathway

Prepared 2026-10-03. **Advisory assessment and proposed sequence, not an
implementation assignment, operational authorization or milestone acceptance.**
This is the receiving document for [the transfer briefing](ADVISORY_HANDOFF_TRUSTED_RUN.md).
Owning specifications and the agreed 08B/09A prompts have not been rewritten.

**Current-direction update, 2026-10-05:** the assessment below is historical.
08B, combined-release receiving, production cutover and the new-package live
lifecycle are delivered; use the current project status and release receipt.
The owner now requires Learner-led planning for logging throughout the application
([09A](TASK09A_PROMPT.md)), and configuration/selection setup enabling a user to
download CK3Chronicle cold and start using it ([proposed Task 10](TASK10_PROMPT.md)).
The earlier learner-only adoption option and Task 10 readiness-only recommendation
are superseded. Installer format and a separate doctor command remain undecided.
Trekker is independent work tracking, not part of the logging architecture.

**1. Outcome and current assessment**

Trusted Run means that an explicitly configured user can have one complete CK3
start-to-exit lifecycle observed, its live-root error evidence protected and
processed into the operational SQLite database, one native review shard finalized,
and human/structured reports produced from stored records without the original log.
Acceptance applies to an identified application/configuration/database/parser/
package/contract/output revision combination. It is not clean-machine installation
or public-release certification. Provisional and unresolved results are valid;
complete accounting and honest evidence matter, not 100% classification.

The capture, ingest, storage and reporting-library foundations are delivered.
**08B is still outstanding, configuration/setup/doctor have concrete remaining
gaps, and milestone scope needs explicit reconciliation. Complete live lifecycle
evidence already exists.** Do not commission another live session simply because
the September 30 activation attached after CK3 had started.

Authority is the current owner direction, [Owner Product Intent](OWNER_PRODUCT_INTENT.md),
[Trusted Run specification](TRUSTED_RUN_SPEC.md), approved
[Error Contract](ERROR_CONTRACT_SPECIFICATION.md), and later boundary decisions.
The [architecture](ARCHITECTURE_AND_DATA_LINEAGE.md) remains the component/data
reference; its historical implementation and retention statements are not all current.
Code establishes behavior; handoffs establish reported delivery/checks; neither
withdraws an owner requirement. Recommendations below remain proposals.

Inspection found no `TASK08B_REPORTING_HANDOFF.md`, reporting renderer delivery,
or `CANONICAL_LOGGING_V1_IMPLEMENTATION_PLAN.md`. Root CLI help still lists only
`ingest`, `capture`, `watch`, `doctor`, and `observe-logging`. The source-scope repair
is delivered; assigning it again would duplicate completed work. Selection still
names package `68f1ae5db205ab46afef9c4d`, model `f5cde2616f35d563118d3d32`, parser
`ck3-lossless-v1.7`; SQL/review schema is 3. Selection is not proof of what any
currently running process has loaded.

The configuration findings are directly inspectable in
[`config.py`](../src/ck3chronicle/config.py) (`CONFIG_FILE_PATH`, module-level loading),
[`doctor.py`](../src/ck3chronicle/doctor.py) (`run_doctor` write probe),
[`cli.py`](../src/ck3chronicle/cli.py) (`build_parser`, `cmd_doctor`), and
[`repository.py`](../src/ck3chronicle/pipeline/repository.py) (`create_database`).
The last API exclusively creates a new schema/timestamp-named file; supported
idempotent setup must compose it with the explicitly configured existing file.

**2. Requirement, delivery and remaining work**

“Reported” below means inherited evidence, not checks rerun by this advisor.
Receiving responsibilities are proposed where no current assignment exists.

| Requirement/outcome | Current authority | Delivered behavior | Evidence and limit | Remaining action | Delivery / receiving team |
|---|---|---|---|---|---|
| Explicit configuration and setup | Intent; spec `REQ-CONFIG-001..007`, `REQ-DATABASE-001`; README still identifies the target | Central roots and containment; exact database-file configuration; low-level `create_database` | Source inspection: fixed current-directory `config.toml`; no root `--config` or setup command. Database initialization API exists, but is not idempotent user setup | Bounded target-bootstrap, validation and setup delivery; reuse storage API, retain explicit file selection | Watcher as proposed existing root-CLI/configuration lead; Pipeline receives database/handler setup, Reporting receives CLI use |
| Read-only readiness and fail-closed operation | Spec `REQ-CONFIG-004/005`, `TRUSTED-RUN-READ-01` | `doctor` lists roots and probes writable storage | Source inspection: it creates directories and writes/deletes a probe file; missing roots are printed and `cmd_doctor` returns 0 after normal return. Full target readiness is absent | Repair in `doctor.py` and central configuration; no live log required for base/watch readiness | Same configuration lead; Pipeline and Reporting receive relevant readiness behavior |
| Complete observed lifecycle and protected live-root capture | Intent/spec capture rules; current Watcher deliveries | Lifecycle detector, stable error-first copy, pending publication and automatic submission | Later genuine normal/crash start/exit evidence personally inspected below. Activation/attachment alone is insufficient | Receive existing evidence and determine applicability to the final candidate; repeat live work only for a concrete uncovered change | Watcher delivers; Pipeline receives protected publication; Pipeline proposed integration lead |
| Crash facts and root exception attachment | Spec `REQ-CRASH-001..004`; Watcher delivery | New-folder association; optional root `exception.txt`; normal/unknown states | Genuine crash Run and retained attachment inspected below. No crash-folder principal logs opened by this review | Receive crash evidence; preserve distinction between observed facts and inference; attachment expiry decision remains separate | Watcher; Pipeline receives facts |
| Valid input, manual facts and ordinary duplicates | Spec input/identity rules as amended by [07D](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md) and [database policy](TASK07_SCOPE_REVIEW.md#database-policy) | Manual ingest/protected copies, pre-parse hash lookup, existing Run returned as `NOT_COMPLETED` on duplicate | Reported genuine ingest/duplicate/manual checks; genuine nonempty zero-diagnostic witness not established | Carry the zero-diagnostic evidence gap to Learner/Pipeline; do not confuse zero review or zero matched records with zero diagnostic emissions | Pipeline; Learner owns parser support, Watcher supplies capture evidence |
| Complete selected assignments, exact aggregation, no silent loss | Error Contract; [Task 06](TASK06_RUN_STORAGE_AND_NATIVE_REVIEW_HANDOFF.md), [v45 integration](TASK06_V45_STORAGE_INTEGRATION_HANDOFF.md); latest owner locator clarification | Pinned parser/matcher selection; template/provisional SQL records; exact ordered values/layout/count identity | Reported native storage/rendering/accounting checks, including seven-log v45 evidence. Not universal parser/model coverage | Receive current evidence; preserve all actual locations and their order/count. No rematching, semantic layer or classification-coverage gate | Learner supplies package; Pipeline owns receiving/contracts/storage; Reporting consumes exact identity |
| Operational SQLite, per-Run lineage and native review | Error Contract and current 07D | Schema 3; one handler/DB worker; two-part finalized shard even when empty; per-Run versions | Reported current-handler/disposable verification; saved public reads and actual finalized manifests inspected below. Not a new power-loss proof | Bounded receiving checks on final candidate, including reopen and reports; no replacement database engine or durable request queue | Pipeline; Watcher and Reporting receive public APIs |
| Raw error/debug retention | Latest [07 policy](TASK07_SCOPE_REVIEW.md#retention-and-preparation), 07D | Daily watcher maintenance; initially 30 elapsed days; completed failed/unprocessed captures eligible; active-input protection | Reported disposable expiry checks and activation history. No production expiry was invoked here | Verify affected integration only; preserve metadata/playsets, SQL and native review. Supersede old one-week/processed-only wording | Pipeline owns retention API; Watcher owns triggers |
| Playset and source context | Later Watcher/07/08A assignments supersede old exclusions | Same-Run debug capture, ordered playset storage; optional unavailable state; all-candidate source search | Reported producer/storage and genuine 08A evidence; known-path scope-before-traversal repair delivered | 08B receives existing service, preserves every candidate/order association and honest missing context | Watcher producer → Pipeline storage → Reporting and Analysis |
| History/query services | Latest [08 decisions](TASK08_SCOPE_REVIEW.md) and [multi-Run handoff](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md) | Same-package source-mtime chronology; exact history; counts/fractions/included-window newness | Reported 18 investigations/359 comparisons + two single-Run checks; 41 scope comparisons, four source investigations/93 comparisons, nine source tests. Four eligible Runs; fourteen missing-time exclusions in that backup | Receive results without rerunning the campaign. Unrepresented failed-read/full-window cases remain unverified; no fallback clocks or medians. Duplicate-ingestion handling belongs to the pipeline | Reporting and Analysis |
| Human/structured/offline reports and CLI | Current [08B prompt](TASK08B_PROMPT.md); spec `REQ-REPORT-001..004` | Libraries available; root report commands/renderers not delivered | CLI help personally run; no delivery handoff found | Complete unchanged 08B: five presets, `runs`/`report`, text/JSON/offline HTML, source candidates and linked verbose appendix; receive remaining milestone metadata obligations in readiness | Reporting and Analysis; Pipeline receives handler use; integration lead receives whole result |
| Audit/reconstruction | Owner's explicit deferral and briefing supersede old task-audit assignments | Historical investigations exist; no further audit commissioned | Owner reports reconstruction of the content of interest, discounting timestamps/order. Not independently rerun here | Record that deferral in milestone reconciliation; no occurrence-history requirement or new reconstruction investigation | Advisory records decision; no audit implementation owner needed now |
| SQL/review/exception expiry, pruning, backup/restore | Old spec still lists acceptance checks; later raw policy preserves SQL/review; Intent treats Run pruning as future authorized work | Current raw retention does not deliver these old managed-lifecycle capabilities | Missing scope reconciliation, not authority to revive removed providers or declare old checks passed | Obtain explicit milestone disposition recommended below; no numeric review/exception defaults activated | Owner decides; Advisory reconciles; Pipeline/Watcher receive only if separately commissioned |
| Candidate, packaging and performance | Spec candidate acceptance, model promotion and performance checks; 07C/07D/08B boundaries | Immutable packages; prior source/installed checks; no final reporting candidate yet | Earlier installed evidence predates final CLI/templates/dependencies; measured timings are not budgets | Identify final revision set; inspect affected packaging and run proportionate checks. Resolve old unratified performance-gate wording | Pipeline proposed readiness lead; Reporting owns its resources; Learner receives package questions |

There is an intentional later capture amendment to preserve in reconciliation:
the approved playset producer copies error/debug bytes, then extracts/hashes their
protected copies before the final pending-directory rename. Deferred ingestion
still begins after publication. Do not reinstate older “all enrichment after
pending publication” wording as a reason to relocate capture or rebuild this path.

**3. Later live evidence personally inspected**

These are read-only observations of retained records, not a new live exercise,
fresh public-handler query, or assertion that the recorded PIDs are running now.
The October 2 source-timestamp activation attached to CK3 PID 8204. Later
`game_started` events distinguish subsequent full lifecycles from that attachment.

| Run | Recorded lifecycle events (UTC) | Capture → ingestion | Stored/review evidence inspected |
|---|---|---|---|
| `20261003-IS3QON` | Start Oct 2 12:58:42.900887; exit Oct 3 00:11:08.724216; CK3 PID 42076 | `20261003T001108.738327Z-Fbp4xgDg`; completed 00:11:30.605021 | Saved handler read: 3,208 records, 59,310 SQL occurrences, three review emissions; normal termination |
| `20261003-D3N7ZQ` | Start Oct 3 02:18:06.777299; exit 02:34:57.135117; CK3 PID 39308 | `20261003T023457.146855Z-CbdYHNZ2`; completed 02:35:00.942723 | Saved handler read: 1,066 records, 1,838 SQL occurrences; new crash-folder association and captured root exception; actual two-part empty shard, manifest `finalization=complete` |
| `20261003-74G2EB` | Start Oct 3 02:50:18.682057; exit 05:06:14.952440; CK3 PID 41556 | `20261003T050614.976714Z-_gldnNph`; completed 05:06:23.292304 | Saved handler read: 2,921 records, 8,916 SQL occurrences, four review emissions; actual two-part shard, manifest `finalization=complete` |

All three use the same watcher PID 30816 in the retained journal; each start/exit
pair has matching process identity, including `started_ns`. For D3N7ZQ and 74G2EB,
the actual capture metadata equals the saved public Run `facts`; the referenced
review files exist, and D3N7ZQ's retained exception exists. No content rehash/audit
or diagnostic reprocessing was performed. Observed lifecycle facts and log-event
emission timestamps differ slightly; the table uses event timestamps and does not
substitute them for stored facts or reporting's source-mtime clock.

Evidence locations, relative to the checkout:

- `.ck3chronicle/wip/runtime/watch/events-watcher.jsonl`: lifecycle, publication,
  request and terminal ingestion records. A further full start/exit and completion
  for `20261003-IUYE99` is present at 11:03–11:15 UTC; its SQL data was not inspected.
- `.ck3chronicle/wip/runtime/pending/<capture_id>/capture-metadata.json`.
- `.codex-tmp/task08-multirun/2624478c0021411d861144eaff16e3c6/<run_id>.json`:
  retained public-handler reads associated with the unchanged 06:06 UTC backup.
- `.ck3chronicle/wip/runtime/review/ck3chronicle-schema3-20260928T211854Z/<run_id>/`:
  inspected native review files and manifests for D3N7ZQ and 74G2EB.

This closes the briefing's uncertainty about whether **any** later complete
lifecycle evidence exists. It does not complete reports, establish current live
state, or show every boundary on the eventual candidate. The recorded processing
application revision is `application-source-sha256:e6ed1eb8f3417e56ef5fadc87ec63531fc561a017be46e878879a894a1d54ab1`;
future configuration/reporting/common-logger changes require an applicability
review, not automatic reuse of the whole acceptance claim.

**4. Scope decisions and recommendations**

These are the material decisions for pathway review. Existing requirements need
no fresh approval merely to remain requirements. A missing implementation is
not a missing product decision.

| Item | What is settled / what remains open | Recommendation and effect |
|---|---|---|
| Configuration/setup | Target bootstrap, explicit roots and read-only doctor remain stated requirements; no later withdrawal found. Current project-local operation is an implementation fact | Retain the target and commission a bounded delivery before acceptance. Defer only wider installation/release UX. Choosing to accept repository-local setup instead would require an explicit milestone amendment; this review does not recommend silently doing so |
| Deferred audit | Owner has already excluded further audit/reconstruction work | Carry that exclusion into the ratified Trusted Run checks. Only its formal milestone disposition needs recording; do not reopen the investigation or ask whether to build an audit |
| Old managed retention/backup checks | Raw 30-day daily expiry is settled. SQL/review preservation is settled for that operation. Old bounded-history, shard/exception expiry, prune and backup acceptance obligations are not explicitly reconciled | Explicitly defer `TRUSTED-RUN-DATABASE-RETENTION-01`, `REVIEW-RETENTION-01`'s expiry portion, `EXCEPTION-RETENTION-01`, and `BACKUP-01` to separately commissioned data-lifecycle work. Keep finalized-shard requirements active. Preserve current attachments pending policy; do not activate 90-day/2-GiB or other candidate defaults. This is a proposed scope amendment, not a pass |
| Performance and evidence methods | No current ratified budgets were located. Current owner instructions prohibit synthetic reporting histories/mock clients/injected failures; absent genuine cases stay unverified | Replace old synthetic/instrumented campaign prescriptions with current genuine-evidence rules. Recommend explicit deferral of the comprehensive numeric-budget gate (`PERFORMANCE-01`); record actual candidate observations and concrete usability failures. Do not invent thresholds or certify every old interruption/power-loss check |
| Genuine nonempty zero-diagnostic case | `REQ-INPUT-003` remains; no qualifying witness established by the reviewed handoffs | Keep a named Learner/Pipeline evidence follow-up. Inspect existing retained inventories first; verify a genuine witness if available. If none exists, return this specific acceptance gap for an explicit deferral/limitation decision. Do not fabricate a log, mistake an empty review shard for this case, or label unsupported input handling complete |
| Candidate and canonical logging timing | Canonical architecture is approved; 09A plans only. Locator experiment is authorized only in disposable storage | Recommend the currently selected package as the initial acceptance baseline, with disclosed learner limits, unless the owner chooses a new release. Keep canonical implementation independent of milestone completion. If shared runtime changes are chosen before candidate selection, include them in readiness; after selection, defer them or deliberately requalify affected evidence |

The last recommendation does not waive newer locator requirements. Learner remains
the receiving owner for their implementation and eventual production-release
proposal. The combined v48 experiment supports explicit Unknown locators and
variable trailing-entry counts, but is not a production parser/model/API release.
**A later handoff update received during this review confirms a discovery
regression in its four template-to-provisional effect occurrences; v48 is not
ready for promotion.** Both training members exist and joint inference succeeds;
candidate-pair discovery missed them. Learner owns the proposal-retrieval repair
and the separately found repeated-entry `line:`/`near line:` equivalence omission.
Cross-version additive seeding is not a permitted workaround. The experiment's
reported 56 still-unmatched occurrences and no complete match lost do not erase
the confirmed regression. Actual locations/order/count still define exact identity.
Reusable travel formulations/date equivalence remain separate. The corrected
same-corpus v45/v46 results showed no changed selected assignments across 731,529
messages; coverage gains must not be attributed to v46 without evidence.

Explicit Run-result replacement also remains an owner requirement. Name
**Pipeline** as the proposed delivery owner, with Watcher and Reporting receiving
preserved facts/read behavior. Its assignment and timing remain separate: same
Run ID, entire result/review replacement, preserved capture/playset and other Runs,
old accepted result preserved on failure. It is not a prerequisite for this
milestone without an owner decision; generation replay remains banned.

**5. Minimal sequence and acceptance deliverables**

**A — Finish the already prepared 08B assignment.** Reporting and Analysis owns
delivery and bounded repairs in its libraries. The next executable product
assignment is the existing [TASK08B_PROMPT.md](TASK08B_PROMPT.md), unchanged.

- Deliver `TASK08B_REPORTING_HANDOFF.md`, documented root commands and all five
  presets, text/JSON/offline HTML, every displayed diagnostic's candidate context,
  and working linked verbose excerpts.
- Demonstrate agreement of identities/counts/history/effective query across
  formats through the actual CLI and public handler on disposable genuine data.
  Preserve raw/model independence, optional-context degradation, explicit
  required-source errors, short-window disclosure and successful empty results.
- Receive the existing scoped traversal repair and current newness semantics;
  do not add logging implementation or another statistical baseline. Maintain
  current usage/handoff pointers and list absent genuine cases without invention.

**B — Close the known configuration/setup/doctor gaps.** Proposed bounded
follow-up, led by Watcher as root CLI/configuration maintainer. Pipeline receives
initialization and handler launch/configuration; Reporting receives CLI selection.
Prepare this assignment while 08B runs, then coordinate shared `cli.py` edits.

- Deliver exact `--config`/fixed-known-folder bootstrap through the one central
  authority, explicit path validation and roles, and a supported setup operation
  that writes/validates configuration before storage initialization. Repeated
  setup uses the explicitly selected existing database; no database discovery,
  silent reset, automatic relocation or parallel initialization engine.
- Make `doctor` read-only with useful readiness/failure results, including valid
  roots with no current error log. Propagate the selected configuration through
  watcher/handler/logger consumers. Reconcile existing project-containment checks
  with explicit target roots without silently removing their safety purpose.
- Deliver focused disposable checks against the requirement and a receiving
  handoff naming actual commands/configuration and changed consumers. No production
  file move, configuration replacement, process restart or initialization occurs
  merely to complete implementation. No clean-machine installer is required.

**C — Bounded integration and acceptance-readiness review.** Replace original
Task 10; proposed lead **Pipeline**, receiving Watcher and Reporting deliveries.
Advisory supports requirement reconciliation; it is not a new mandatory approval
layer. Repairs stay with their component owner, and this lead retains closure
responsibility until the receiving owner accepts them.

- Deliver `docs/TRUSTED_RUN_READINESS_HANDOFF.md`: identified candidate/revisions,
  requirement dispositions, applicable evidence, concrete defects/owners and a
  short acceptance procedure. Only ratified amendments change acceptance scope.
- Trace actual publication → `HandlerClient` ingest → SQL/finalized review → Run
  selection → report CLI. Use the existing owners; no new queue, scheduler,
  provider, interpretation service or broad rewrite. Check reporting metadata
  against `REQ-REPORT-002/004`, including application/output/database revisions,
  represented package/contracts, review availability and completeness limits.
- Use targeted disposable genuine-data checks for changed boundaries, storage
  reopen and database-only reporting. Inspect packaging of actual CLI code,
  templates/assets/dependencies; make no installed-execution claim without running
  it. Run the existing logging ownership check if runtime changes are included.
  Do not repeat the large inherited campaigns just to create new totals.
- Receive the complete normal/crash evidence above. Distinguish an attached
  `observed_started_at` from proof of observed startup; journal transition matters.
  Assess candidate applicability and name any remaining live evidence precisely.
- Close concrete defects through bounded owning-component repairs and focused
  rechecks. Resolve the zero-diagnostic witness and any other still-ratified
  unverified acceptance case explicitly; a passing subset cannot silently accept
  the whole milestone.

**D — Final candidate acceptance, with live action only if required and authorized.**
Proposed operational lead **Watcher**; Pipeline receives SQL/review, Reporting
produces reports, and the owner accepts the milestone.

- Existing authorized live records are usable evidence. Disposable verification
  proves implementation boundaries. Neither alone proves that a changed candidate
  is loaded in the operational processes.
- If readiness requires activation or a fresh lifecycle, present the exact
  candidate, configured database, changed processes and short procedure first.
  Obtain authorization for those new actions. Start observation before the owner's
  next ordinary CK3 session; do not manufacture crashes, expire evidence, reset
  production or reprocess accepted Runs for the exercise.
- Acceptance connects the identified observed start/exit to protected capture,
  successful operational ingestion, one finalized native shard and agreeing human/
  structured stored-record reports. Record remaining limitations and the
  disposition of every ratified check. If a required check remains unverified,
  report it as outstanding rather than declaring acceptance.

**E — Reconcile current documentation to decisions and delivered facts.** Advisory
leads document preparation; each component team receives its operational claims.
Record scope decisions before treating the old spec as an acceptance checklist;
final delivery/acceptance wording follows evidence. Update the spec, Intent where
the owner amendment requires it, architecture, operating guide, README and current
plan/status/handoff pointers through a separately approved reconciliation scope.
Preserve historical handoffs as dated evidence. Every preceding task maintains
its own handoff; documentation is not postponed wholesale to the end.

**6. Tasks 09–12 and canonical logging**

| Draft/task | Disposition recommended after inspection |
|---|---|
| Original 09, offline learner reconnection | Retire as superseded. It targets absent `pipeline.emissions` and deletes tools now used by 07C, including `build_review_pack.py` and `evaluate_unseen_session.py`. Current retained execution supplies learning/registry/evaluation/publication/review. No generic reconnection or deletion task remains justified |
| New 09A planning | Proceed independently alongside 08B. Learner is proposed planning lead; the existing shared logger maintainer (07E/Pipeline receiving role) receives common-owner effects. Deliver only `CANONICAL_LOGGING_V1_IMPLEMENTATION_PLAN.md` under its existing prompt; architecture approval does not authorize implementation |
| Canonical implementation after plan review | One bounded learner-first assignment, separately authorized; no need to invent a permanent team or a chain of task numbers. Shared-owner extension → authenticated immutable distribution → selected actual-function/checkpoint hooks. Keep implementation number provisional until scope is reviewed |
| Original 10, cutover manifest | Replace with C above. Old provider closure, capture relocation and `rebuild-db`/generation instructions no longer match the product. Preserve only justified integration/resource/evidence review |
| Original 11, application cutover | Retire the broad source switch/deletion exercise; 06B and 07D/Watcher already did its relevant work, and 08B registers its own commands. Any concrete repair belongs to its actual owner. A separately authorized activation/acceptance procedure is D, not execution of the old manifest |
| Original 12, documentation reconciliation | Retain the purpose, replace stale inputs/prescriptions. Its absent modules, indefinite-raw retention and fresh-generation wording conflict with current direction. Reconcile ratified scope and actual delivery; never rewrite requirements to whatever code passes |

Canonical implementation must retain `runtime_logging.py` as the single editable
backend owner. 09A should define real-code call identities, immediate bare and
throttled caller-count checkpoints, invocation outcomes, explicit log destinations
and release authentication/receipts. Its existing preservation plan is appropriate:
verified exact affected working-source copies, including uncommitted files;
coordinated overlapping edits; small diffs; immutable candidates; rollback limited
to this task. Git HEAD or Markdown source exports alone are insufficient.

Receive any common change with current watcher/handler behavior, request
correlations, destinations, bootstrap diagnostics and operator instructions
accounted for. Broader consumer conversion needs a concrete benefit and explicit
replacement mapping; do not add aliases, duplicate streams or silently remove
visibility. Configuration work and logging's config-import extension overlap and
must be coordinated. No canonical implementation is needed merely to prove the
already observed lifecycle. Learner locator adoption and production Run-result
replacement also remain independent unless deliberately included in the candidate.

**Inspection and verification record for this advisory delivery**

Read current authority/handoffs, the original 09–12 drafts, canonical architecture/
09A prompt and focused owning source. Rejected handler designs were not read.
Personally ran only root CLI `--help` with the repository Python and read-only
JSON/source inspections described above, plus document link/whitespace checks.
No upstream campaign was rerun; no `doctor`, handler launch, database operation,
capture, expiry, installation, model activation, commit or push was performed.
The entry Git status showed two unrelated untracked files, rather than the
briefing's older extensive tracked delta; both were preserved. Historical pending
directories denied enumeration access; permissions were not changed and the
assessment uses the accessible later evidence identified above.
Concurrent learner documentation/research changes appeared before completion;
they were preserved, and the new effect-regression finding was incorporated above.

The [working-practices review](AGENT_WORKING_PRACTICES_REVIEW.md) remains a proposal.
This pathway names delivery/receiving responsibilities for review, without
activating that proposal or new Skills. Only this pathway and short current
document pointers are changed by this assignment.
