# Watcher active-playset delivery and Task 07 receiving contract

2026-10-07 implementation follow-up: the [Observer removal handoff](WATCHER_OBSERVER_REMOVAL_HANDOFF.md)
records deletion of the independent module and byte-identical preservation of the
required Watcher path. Pipeline owns the remaining CLI/backend cleanup and actual
replacement-candidate receipt on TREK-3 for TREK-6. Observer-only checks are removed
requirements, not passed tests. The dependency-review paragraph below is historical.

2026-10-07 dependency review: the [Observer deletion handoff](WATCHER_OBSERVER_DEPENDENCY_REVIEW.md)
traces the current lifecycle, capture, source timestamp, playset and handler path.
These functions are independent of Observer code/output. Findings are delivered
on existing TREK-3 for Pipeline's TREK-6; no deletion or release change is claimed.

Delivered 2026-09-28 following owner approval. The watcher producer is implemented.
Task 07 remains a subsequent task; no pipeline storage or application cutover was
performed as part of this delivery.

Receiving instructions are incorporated into the
[revised Task 07 prompt](TASK07_PROMPT.md), including its
explicit schema/repository/review scope and execution order. This handoff remains
the producer format and delivery reference. The
[integration review](TASK07_PROMPT_REVISION_REVIEW.md#watcher-handoff-quality-check-and-sequencing)
records the quality check, resolved scope conflicts and remaining operator choices.
Later live activation is recorded in `CURRENT_HANDOFF.md`; the no-live-operation
statements below describe the delivery's verification pass.

## Delivered execution path

`cli.cmd_watch` -> `watcher.watch_sessions` observes process exit ->
`cmd_watch.perform_capture` -> `_spool_once` -> `harvester.spool_logs` copies both
logs -> `cmd_watch.create_captured_playset` -> `playset.extract_playset` ->
`harvester.write_playset_template` -> existing pending-directory publication.

The continuous watcher copies the entire `error.log` first and `debug.log` second,
using the existing stable-copy helper. It then parses the protected debug copy,
reads descriptors, hashes each protected log once, and writes the completed
template before publishing the directory. Existing process/copy checks remain;
there is no subsequent monitoring of protected files. CK3 mount emissions alone
determine membership and order. Descriptors supply names and publisher IDs.

Output:

```text
ROOT_CK3CHRONICLE/pending/<capture_id>/
  error.log
  debug.log
  capture-metadata.json
  playset.json
  crash/exception.txt          # optional existing crash attachment
```

The callback runs after both copies and normal capture metadata are complete,
inside the existing `.copying-*` directory. The directory is renamed only after
the callback returns. The captured-file count covers the copied CK3 evidence;
generated JSON is not counted as another captured log.

The current lifecycle detector, crash selection and manual commands are retained.
`capture`, `watch --once`, and default `spool_logs` remain error-only operations.
The existing rejection of an empty error log remains. This delivery applies to
new observed-lifecycle pairs, not historical captures.

## Production ownership and interfaces

| File | Delivered responsibility |
|---|---|
| `src/ck3chronicle/playset.py` | Immutable `PlaysetMember` / `PlaysetTemplate`, `iter_mounted_paths`, `extract_playset`, descriptor resolution and serialization. |
| `src/ck3chronicle/harvester.py` | `spool_logs(..., include_debug=True, on_logs_copied=...)` and `write_playset_template(directory, captured_at=..., members=...)`. |
| `src/ck3chronicle/cli.py` | Actual watcher orchestration, configured roots, resolution warnings, template/failure journal events and continuous-watcher silence. |
| `src/ck3chronicle/watcher.py` | Small `EventJournal(cleanup_heartbeat=False)` option for recording startup failures without deleting another watcher's heartbeat. Lifecycle detection is unchanged. |

The production extractor belongs to the watcher. Pipeline callers receive its
completed JSON; they do not need another extractor or descriptor lookup.

## Format version 1

`PlaysetTemplate.to_dict()` defines the producer format. The JSON is UTF-8.

| Field | Meaning |
|---|---|
| `schema_version` | Integer `1`. |
| `error_log_sha256` | Lowercase 64-character SHA-256 of the complete protected error log. |
| `debug_log_sha256` | Lowercase 64-character SHA-256 of the complete protected debug log. |
| `log_pair_id` | Literal `sha256:<error_log_sha256>:<debug_log_sha256>`, derived during serialization. |
| `captured_at` | Same UTC ISO timestamp as `capture-metadata.json`. |
| `members` | Ordered member array; base at 0, emissions at 1 onward. |

There is no Run ID at capture time. The joined ID identifies the exact byte pair
before the pipeline assigns its Run ID. It is not another hash calculation, a
replacement error-log deduplication key, or a mutable current-playset ID.

Each member has exactly these fields:

| Field | Meaning |
|---|---|
| `load_order` | Integer: `0` for base game, then consecutive emission order. |
| `name` | Descriptor name; fixed `CK3 Game Files` for base; `UNKNOWN` if unavailable. |
| `path` | Path as emitted by CK3; configured game path for base. |
| `root_ID` | `ROOT_GAME`, `ROOT_STEAM`, `ROOT_LOCAL_MODS`, or JSON null. |
| `stable_id` | `ck3:1158310`, `pops:<pops_id>`, `steam_workshop:<id>`, or null. |
| `descriptor_path` | Descriptor used to supply metadata, or null. |

`ROOT_LOCAL_MODS` is the existing configured development/user-mod root; no duplicate
`ROOT_DEVMODS` root was added. Base and DLC both use `ROOT_GAME`. External mounts
are retained with null `root_ID`. Paths remain historical values; query-time
filesystem availability is a future consumer's responsibility.

Packaged DLC uses its matching `.dlc` metadata. Mods use root `descriptor.mod`,
then an associated local `.mod` with a matching declared path. Workshop fallback
tries `ugc_<id>.mod` first. A relative associated path is interpreted from the
CK3 user directory containing the configured `mod` root. The descriptor reader
handles UTF-8/BOM, comments, quoted/escaped strings and nested script blocks;
only top-level scalar metadata is used. No display name is fabricated from a
directory name. The Workshop path ID takes precedence over a conflicting
descriptor remote ID, with a journal warning.

## Failure and journal behavior

- If either source copy fails, extraction never starts. Existing `.copying-*`
  staging retains any copied evidence; `capture_failed` identifies the failing
  source and staging location. These directories are not completed inputs.
- Missing/unreadable paths, missing/malformed descriptors, missing names and
  conflicting metadata produce `playset_metadata_warning` with capture ID,
  member order, mounted path, attempted descriptor and reason. The member stays
  in the template. A usable associated descriptor can supply the name.
- No mount emissions yields the base member and an explicit
  `no_mount_emissions` warning; additional membership is never invented.
- Expected protected-debug read, hashing or template-write I/O failures produce
  `playset_template_failed`. The raw pair is still published and retained, with
  no completed template. A failed write can leave `.playset.json.tmp`; that file
  is incomplete and must never be consumed as the template.
- `playset_template_created` is emitted only after successful directory
  publication and names the final path, both hashes, joined ID and member count.
- Unexpected programming errors retain staging evidence, emit failure events
  and exit nonzero. Continuous watcher startup, completion, warning, interruption
  and failure reporting use the event journal, without terminal chatter. If the
  journal itself is unavailable, a nonzero exit code remains the failure signal.

Events use the existing `ROOT_CK3CHRONICLE/watch/events-*.jsonl` mechanism. Normal
capture completion means raw evidence is protected; template availability is
reported by the separate template-created or template-failed event.

## Verification and generated example

39 checks passed: 23 playset producer/integration checks, 8 watcher capture checks
and 8 existing processing-recovery checks. They cover actual `cmd_watch`
orchestration with a simulated lifecycle, exact-byte copying, hash/join provenance,
descriptor resolution, missing files, read/hash/write failures, preservation of
raw evidence, journal-only reporting, and the existing NTFS ACL check.

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p '*capture_requirements.py' -v
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p test_processing_recovery_requirements.py -v
```

The production extractor and writer also processed isolated copies of the recent
real logs with read-only access to real descriptors. Results: 133 members,
132 explicit mounts plus base, zero UNKNOWN names and zero warnings. All three
Workshop associated-descriptor fallbacks resolved correctly. Full protected
copies were checked byte-for-byte and both serialized hashes independently
verified. This was an isolated native-input demonstration, not a real lifecycle
observation or production pending capture.

Generated artifacts remain ignored, outside Git:

- [Complete production-generated playset.json](../.codex-tmp/watcher-playset-implementation/runtime/pending/20260928T044454.938004Z-OLveBBJL/playset.json)
- [Native verification details](../.codex-tmp/watcher-playset-implementation/native-verification.json)

Example provenance from that generated template:

```json
{
  "schema_version": 1,
  "error_log_sha256": "42d27e6896d2a349fc64ecbfae0bc025cb83b7501c2e374844d615767d0fab56",
  "debug_log_sha256": "1f5b07a4acd739d6214a1a267930fd84f57416de83c08f70ef0c781474b56ab0",
  "log_pair_id": "sha256:42d27e6896d2a349fc64ecbfae0bc025cb83b7501c2e374844d615767d0fab56:1f5b07a4acd739d6214a1a267930fd84f57416de83c08f70ef0c781474b56ab0",
  "captured_at": "2026-09-28T04:44:54.938004+00:00"
}
```

The complete example adds all 133 `members` records. The copied error log is
783,537 bytes and debug log 21,741,082 bytes. The live watcher was not started,
no production captures were processed and no production database was modified.

## Task 07 receiving work

1. **Consume this artifact.** Extend protected-input preparation to recognize
   completed `playset.json` beside its pair and carry its ordered fields forward.
   Validate the version, field shapes, consecutive order and two-hash association
   at input preparation. Do not reconstruct membership, consult the launcher,
   repeat descriptor resolution or add engine-use verification.
2. **Attach to the existing Run write boundary.** Current
   `pipeline.repository.Generation.write_run` takes `log_sha256` and `facts`;
   `pipeline.schema.runs` already persists `run_id`, unique `log_sha256` and
   `facts_json`. The error hash identifies the error log for a Run today. Match
   the supplied error hash to that existing input identity. Preserve the debug
   hash, joined ID and capture time when accepting the playset; keep error-log
   duplicate semantics intact.
3. **Persist Run-owned members.** Add normalized member rows keyed by
   `(run_id, load_order)` with the six delivered member fields. Store pair
   provenance and a `playset_captured` flag with the Run. Extend the existing
   repository read boundary (for example `Generation.read_playset(run_id)`) to
   retrieve the ordered records. SQL is canonical after ingestion; no independent
   authoritative playset registry or repeated JSON parsing in individual callers.
4. **Derive the review manifest.** `Generation.write_run` owns the transaction and
   review-shard publication; `ReviewWriter.stage` builds native review details.
   Serialize the playset into the manifest from the same accepted Run/member
   values stored in SQL, under that existing publication boundary. Do not make
   the watcher template or manifest a separately mutable second Run model.
5. **Accept historical error-only inputs.** A missing template must not reject
   an otherwise valid Run. Use `playset_captured=false`; consumers must not
   interpret missing capture as proof that no mods were active. The pipeline
   owns the exact absent-template representation and policy, including raw pairs
   retained after template failure. Do not fabricate historical descriptors.
6. **Retain replay provenance.** Preserve both raw logs and the watcher artifact
   when preparing/retaining new inputs. The old `harvester._inspect_pending`
   rejects `playset.json` as an unsupported file. Updating that receiving path
   or its commissioned replacement belongs to Task 07; do not work around the
   rejection by deleting the template. `.copying-*` and partial `.tmp` outputs
   are not completed templates. Full debug retention remains required.

Task 07 owns schema-version/generation implications and repository/review tests.
Future search/reporting projects consume its canonical ordered member read API
for selection, name/ID/path lookup, path iteration and load-order reasoning.
They must report missing historical filesystem paths accurately. No filesystem
search service, replacement declarations or winner-resolution algorithm was
added to this watcher delivery.
