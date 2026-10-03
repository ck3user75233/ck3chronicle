# Task 07 Prompt

Task 07 implements the APIs and manual ingest command. The watcher team integrates
automatic calls after receiving the handoff. No watcher changes belong to Task 07.

## References

Follow repository instructions and current owner decisions. Use these interface references:

- [Task 06 storage APIs](TASK06_RUN_STORAGE_AND_NATIVE_REVIEW_HANDOFF.md) and [selected-model update](TASK06_V45_STORAGE_INTEGRATION_HANDOFF.md).
- [Watcher capture and playset format](WATCHER_ACTIVE_PLAYSET_HANDOFF.md).
- [Error Contract](ERROR_CONTRACT_SPECIFICATION.md).
- [Task 07C receiving contract](TASK07C_SELF_CONTAINED_RELEASES_HANDOFF.md#task-07-receiving-contract) and [release selection](RELEASES.md#production-package-selection).

Current per-Run version policy below supersedes the Task 06 handoffs' database-wide
lineage restriction. The [scope review](TASK07_SCOPE_REVIEW.md) records current
owner decisions and the remaining malformed-playset choice.

## Deliverable 1 — Expose the existing ingest path

Error-log classification through SQL/review persistence already works. Reuse the
Task 06 `store_validated_log` example and the exercised orchestration in
`.codex-tmp/task06-v45/verify.py`; expose that sequence through the application.
These demonstrate reuse, not new requirements or code to copy wholesale.

- Accept a completed capture directory or explicitly supplied manual error log, plus the database.
- Provide one `ingest` command; use arguments to distinguish inputs. The watcher will call the same underlying API.
- Accept an optional package ID through that operation/API using `catalog.load_selected_classifier(package_id=...)`; omission uses the existing default. Do not change active selection or select by model ID alone.
- Keep protected originals where captured. Protect an unprotected manual input once using existing capture support.
- Read `capture-metadata.json`; retain supplied lifecycle/crash facts without inventing missing values.
- Detect duplicates by full error-log hash before parsing; return the existing Run ID.
- Reuse the catalog, `read_log`, `classify_raw`, contract preparation, accumulator and Run writer. Verify the input hash describes the bytes parsed.
- Pass every classifier result to `ReviewWriter.observe`; accumulate record-eligible results through existing contracts. Error type remains unknown.
- Return success only after SQL and the [two-part review shard](ARCHITECTURE_AND_DATA_LINEAGE.md#native-review-shard) complete. Return failures distinctly and preserve the input.

## Deliverable 2 — New schema, playset storage and per-Run versions

- Issue a new SQL schema version for playset storage; extend the review-manifest version.
- Use explicit database reset for schema changes. **NO LEGACY FALLBACKS, NO BACKWARD COMPATIBILITY, NO MIGRATIONS.** Opening an incompatible database reports the required reset without deleting it.
- Escalate concerns that changes would break still-required functionality; identify the affected behavior and proposed resolution before making the breaking change.
- Remove the database-wide lineage equality restriction. Compatible processing versions may create different Runs in the same database.
- Obtain actual processing lineage from `contracts.run_lineage(package, application_revision=...)`; retain the package's model format and storage format versions alongside it. Preserve the helper's package/manifest, model, parser, matcher API, selector, classifier and contract identities.
- Learner-release provenance belongs to offline publication. No new ingestion-side learner ID, learner import or historical release recovery belongs to this task.
- Receive watcher-produced playsets; verify their association with the captured pair. Preserve member order, repeats, nulls and all six member fields from the watcher handoff.
- Store playset availability, format and pair provenance with the Run. Write the same accepted values to the review manifest; provide an ordered SQL-only read.
- **Missing playset data must not block otherwise valid ingestion.** Store `playset_captured=false` and no member rows. Report malformed/mismatched completed JSON separately; obtain a disposition for that case.
- Preserve existing per-Run definition checks, diagnostic rendering, accounting, transaction and failure/cleanup behavior.

## Deliverable 3 — Configurable raw-log retention API

- Implement a callable retention operation, configurable and initially 30 elapsed days from capture time.
- Operate on captured error/debug logs in their existing location; ingestion creates no extra archives or retention-clock resets.
- Keep SQL history, stored playsets, review shards, capture metadata and completed playset JSON outside raw-log expiry.
- Return eligible/removed/skipped files and failures; offer a preview and protect inputs currently being ingested.
- All completed captures are eligible by age, including failed/unprocessed captures; successful ingestion is not an expiry prerequisite. Incomplete capture staging is outside this policy.
- Supply configuration and a proposed check interval to the watcher team. The watcher triggers checks periodically, including when no logs are ingested. Do not make ingest responsible for scheduling or create another resident process.

## Deliverable 4 — Watcher-team integration handoff

Create `docs/TASK07_INGESTION_AND_RETENTION_HANDOFF.md` with:

- Exact import paths, function signatures, configuration, results/exceptions and runnable calls for both APIs.
- Ingest trigger: after publication of a completed capture.
- Retention trigger: periodic watcher maintenance, independent of capture/ingest activity; specify the proposed cadence.
- Call duration/blocking behavior, safe coordination of ingest and retention, and failure handling that preserves capture and allows watching to continue.
- Propose minimal startup/backlog/retry behavior for the watcher team; identify unresolved choices without introducing a queue or recovery framework.
- SQL/manifest versions, playset read API, explicit database initialization/reset instructions and manual command examples. Define whether the database argument denotes a file or storage directory.

Task 07 delivers this document and working APIs. The watcher team owns trigger
wiring and live activation; Task 07 completion does not claim automatic ingestion
or retention has been activated.

## Deliverable 5 — Verification and completion

- Use complete genuine retained CK3 inputs in disposable storage. No synthetic messages, mutated logs, fabricated records or tests defining requirements.
- Verify API and CLI ingestion, duplicates, inputs with and without playsets, ordered SQL/manifest agreement, diagnostic/review accounting and SQL-only rendering.
- Verify distinct genuine logs processed with packages `44a0401b8adf0a2953d26705` and `68f1ae5db205ab46afef9c4d` can add Runs to the same database, retain their actual lineage and render from SQL. Re-submitting an accepted log under another package still returns its existing Run ID without replacement.
- Verify retention behavior on disposable copies; document evidence gaps.
- Record changed paths, checks and limitations in the handoff.
- Update current status, plan, execution order, `CURRENT_HANDOFF.md` and README with the watcher-team dependency.
- Carry the [completed Script location-stack findings](LEARNER_SCRIPT_LOCATION_STACK_INVESTIGATION_RESULTS.md) as context, not a pending investigation or representation change. Historical release gaps remain separate learner-team work only if commissioned; raw-log retention does not prune executable releases.
- Keep changes within pipeline, necessary configuration/CLI and documentation. Preserve unrelated work; leave learner/model artifacts, the live watcher and production data untouched.
