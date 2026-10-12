# Task 10A.1 — Application interfaces and artifact

**Owner: Pipeline. Receiver: Launch & Distribution.** Issued 2026-10-08.
**Trekker ID: TREK-9.** Follow the [common instructions](WORKING_AGREEMENT.md)
and [scope/index](../TASK10_DELIVERABLES.md). This is the one technical producer
assignment supporting Launch & Distribution; it does not make Pipeline the setup
experience or outer distribution owner.

## Intake and outcome

Read current source, root instructions, the Task 09 baseline/actual TREK-6 receipt,
`config.py`, CLI bootstrap, database initialization/public handler, release selection
and shared logging interfaces. Retrieve [10A](10A_FIRST_USE_DESIGN.md)'s proposal;
review it and record receipt/corrections on 10A. Interface review, current-source
inventory and environment preflight may start before that design is final.

Implement the received central configuration and runtime interfaces, then deliver
an authenticated application wheel for [10B](10B_DISTRIBUTION.md). Deliver a usable
interface early; do not wait for the outer bundle to complete its own prerequisite.

## Bounded implementation

- Resolve explicit configuration or the fixed LocalAppData bootstrap consistently;
  remove reliance on caller cwd for the installed route. Propagate the selected
  authority to runtime consumers/children. No runtime root discovery or alternative
  config owner. Owner correction, 2026-10-08: setup may offer bounded candidates
  from Windows Known Folders and user-supplied Steam/library locations. Return
  editable full paths and actual validation findings; require per-field acceptance
  before saving. Runtime and doctor use saved paths without replacement searches.
  Preserve existing supported use or identify required transition explicitly.
- Provide reusable validation, initialization and selection operations for setup.
  Validate before database creation and return/persist its exact created path.
  Repeat setup preserves existing user choices, captures, database and review data.
  Help/setup can run before config exists; Watcher configuration does not require
  a current error.log. The logs directory itself is expected; diagnose its absence
  as a configuration problem. Missing optional evidence must not become a new hard gate.
- Implement the Owner's substantive config-doctor correction through the existing
  `doctor` command and shared setup validators. Diagnose missing/invalid config,
  CK3 identity/readability (not mere directory existence), workshop/local-mod/log
  paths and configured data/database/model/tool state. Each finding gives evidence,
  severity, practical impact and correction; unverified is not healthy. Diagnose
  absent config without failing at import. No automatic repair, external-file edits,
  database initialization or handler startup from diagnosis. Resolve the current
  write-probe behavior and proposed exit/output changes in the technical receipt.
  Follow [the revised 10A design](../task10/FIRST_USE_DESIGN.md#path-suggestions-and-meaningful-configuration-diagnosis).
- Keep read-only application resources separate from writable runtime/state/log
  paths. Use the sole runtime logging backend. Retained Learner execution remains
  configuration-independent; do not edit retained bytes to implement app setup.
- Authenticate the shipped production model/default and dependency closure. Reuse
  Task 09's model/Learner pins. Produce a fresh wheel for changed application bytes,
  with accurate version/artifact identity, resources and installed entry points.
- Supply [10E](10E_USER_WORKFLOWS.md) a concrete supported way to locate and read the
  SQLite database independently. Prefer an existing read-only or consistent-snapshot
  route. Document writer/connection conditions, schema version, tables/JSON fields,
  count semantics and external-file limits. If no existing route can satisfy basic
  access, this assignment permits a bounded read-only/snapshot command using existing
  SQLite facilities. It does not permit schema redesign, arbitrary remote SQL,
  new export frameworks, flattened CSV/XML outputs or review-shard merging.

Permitted surfaces: owning configuration/bootstrap and catalog APIs, database
initialization/reading interface, shared CLI composition, existing packaging/resource
manifests, owning checks and handoffs. Coordinate shared `cli.py`/`pyproject.toml`
before editing. Do not change Watcher lifecycle/capture/playset, Reporting query
semantics, Learner algorithms or retained distributions. If adapting a consumer
requires a component-owned change beyond shared configuration wiring, identify
the exact owner/scope for an owner-issued follow-up, while continuing other work.

## Evidence and receiving

Own and deliver the user-facing technical reference drafts for the Pipeline
interfaces in this assignment: CLI syntax/options/defaults, TOML/JSON controls,
configuration precedence/path rules, database initialization/access, model selection,
outputs/exit behavior and side effects. Explain supported use and limits, with
meaningful examples and actual applicable execution evidence. Write concise
reference sections or coordinated drafts for `docs/user/`; linking only to code
or a long implementation handoff does not satisfy this contribution.

Deliver those sections with the interface/artifact on this same record so 10D/10E
can edit them into the manual. Review any disputed semantic changes directly.
When a later code repair changes behavior, update the reference contribution and
identify affected examples in the same delivery. Docs owns presentation; Pipeline
remains accountable for technical correctness and maintenance of its content.

Verify real isolated first/repeat setup, selected identities, persisted database
path, actual configuration propagation and preserved outputs/journals. Use genuine
inputs through normal APIs for needed processing checks. Run the runtime logging
ownership checker. Account for unchanged evidence reused from Task 09 and behavior
that changed; help output alone is not functional receiving.
Verify suggestions and per-field acceptance against actual available locations,
and doctor findings against real setup evidence. The Owner's examples define
required behavior, not authorization to create synthetic directories or injected
failures; unavailable genuine cases remain explicitly unverified.

Write `docs/task10/PIPELINE_HANDOFF.md`: exact callable interface/commands, artifact
and dependency pins, source/resource correspondence, config path rules, actual
checks/limits, external data access instructions and rollback. Record a producer
delivery on this record for Launch & Distribution to receive. Refresh 10B/10D/10E
requests before declaring your delivery final. Keep current summaries short.

Complete when the technical delivery is received with no outstanding Pipeline
defect. Outer-distribution/clean-machine acceptance remains on 10B/10C, not an
artificially open Pipeline producer. Repairs that alter the wheel must issue a new
artifact and identify which consumer evidence is invalidated. No full corpus build,
production activation, Git/publication action or unapproved synthetic test.
