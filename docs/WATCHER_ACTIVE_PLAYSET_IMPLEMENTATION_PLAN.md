# Watcher active-playset implementation plan

Approved and implemented, 2026-09-28. The approved plan is retained below;
[the delivery handoff](WATCHER_ACTIVE_PLAYSET_HANDOFF.md) records the actual
implementation, verification and Task 07 receiving contract. The only additional
support change was an `EventJournal` option to log startup failures without
removing another watcher's heartbeat. No lifecycle detector rewrite was needed.

## Delivery and ownership

Deliver a working production watcher that, after an observed CK3 exit:

1. Copies `error.log` and the entire `debug.log` into protected storage.
2. Immediately extracts the active playset from the copied debug log's mount emissions.
3. Resolves human-readable member names from descriptors.
4. Computes the SHA-256 content hash of **each copied log**.
5. Writes `playset.json` containing both hashes, their joined identifier and the ordered members.
6. Records outcomes and problems in the watcher journal.

The extractor is part of this delivery. It is production code called by the watcher. The pipeline consumes the completed JSON; it does not need a playset extractor.

Task 07 is on hold and will run afterward. There is no Task 07 implementation or coordination dependency. Receiving requirements will be documented in the handoff delivered with the completed watcher.

## Output and provenance

Extend the existing capture directory:

```text
ROOT_CK3CHRONICLE/pending/<capture_id>/
  error.log
  debug.log
  capture-metadata.json
  playset.json
  crash/exception.txt          # when existing crash handling supplies it
```

| Template field | Meaning |
|---|---|
| `schema_version` | Format version, initially 1. |
| `error_log_sha256` | Lowercase, 64-character SHA-256 of the entire protected error log. |
| `debug_log_sha256` | Lowercase, 64-character SHA-256 of the entire protected debug log. |
| `log_pair_id` | Joined identifier defined below, usable before a Run ID exists. |
| `captured_at` | Existing capture timestamp. |
| `members` | Ordered array of member records. |

Define the joined identifier precisely:

```python
log_pair_id = f"sha256:{error_log_sha256}:{debug_log_sha256}"
```

Error hash first, debug hash second. This is their literal join, not a third hash calculation. It identifies the captured byte pair independently of filenames, capture time and the later Run ID. Both constituent hashes remain individually available. Derive the joined value during serialization from those two fields.

Hash each protected file once during template production. Retain both complete original files. No recurring rehashing or monitoring of protected directories is added.

Each member contains exactly:

```text
load_order       integer: base game 0; explicit mounts 1 onward
name             descriptor name, "CK3 Game Files", or "UNKNOWN"
path             mounted path; configured base-game path for member 0
root_ID          ROOT_GAME / ROOT_STEAM / ROOT_LOCAL_MODS / null
stable_id        existing namespaced publisher identifier, when available
descriptor_path  descriptor used, when available
```

Both the base game and its DLC directories use `ROOT_GAME`. An external mounted path has null `root_ID` and remains in the list. Keep the emitted path. Do not add type, source-line, association, confidence, metadata-status, replacement-declaration or separate raw-mount-line fields.

## Production files and functions

Paths below are relative to the repository. New symbol names are proposed interfaces.

| File | Functions/types to add or edit | Outcome |
|---|---|---|
| `src/ck3chronicle/playset.py` — new production module | `PlaysetMember`, `PlaysetTemplate`, `iter_mounted_paths`, `extract_playset`, descriptor helpers, `to_dict` | Watcher-owned extraction, name resolution and the fixed output model. |
| `src/ck3chronicle/harvester.py` | Extend `spool_logs`; add `write_playset_template`; reuse `hash_file` and existing copy/staging helpers | Protect both full logs, hash their protected contents and write the template. |
| `src/ck3chronicle/cli.py` | `_spool_once`, `cmd_watch.perform_capture`, new nested `create_captured_playset`, watcher logging paths, watch help in `build_parser` | Connect the production extractor to the actual watcher and journal results. |

The lifecycle detector in `watcher.py` already supplies the required start/exit trigger and journal. Its process-detection algorithm needs no rewrite. Existing roots require no configuration changes.

## Stage 1 — Implement the production extractor

Create `src/ck3chronicle/playset.py`, outside the pipeline package. This module is fully within the Watcher Team's implementation scope.

Define immutable `PlaysetMember` and `PlaysetTemplate` dataclasses using the agreed fields. `PlaysetTemplate.to_dict()` emits `log_pair_id` from its two stored hashes and serializes members in their existing order. Define `PLAYSET_FILENAME = "playset.json"` and `PLAYSET_SCHEMA_VERSION = 1` here.

Add:

```python
def iter_mounted_paths(lines): ...

def extract_playset(debug_path, *, roots, on_warning): ...
# Returns tuple[PlaysetMember, ...]
```

`iter_mounted_paths` yields VFS Mounted Data paths in file order. Reuse the applicable emission grammar from `runtime_context.py`. Do not copy its database service, separate DLC/mod ordering, name-derived IDs or multiple-session inference. Existing historical-provider retirement is a handoff note, not another implementation task here.

`extract_playset` streams the copied debug log, prepends `CK3 Game Files` at order 0, resolves the remaining members and returns the ordered tuple. Mount emissions are the final authority for membership and order. Descriptor checks supply metadata; they do not verify the engine's use of a member. No launcher-derived membership, sorting or deduplication.

Add these private helpers in the same module:

| Function | Behavior |
|---|---|
| `_root_id(path, roots)` | Determine configured root category while preserving the emitted path. |
| `_read_descriptor_fields(path)` | Read top-level name/path/remote_file_id/pops_id fields, handling normal whitespace, comments, UTF-8/BOM and quoted strings. |
| `_find_descriptor(mount_path, root_id, roots)` | Find the matching packaged .dlc, root descriptor.mod, or associated local .mod. |
| `_resolve_member(path, load_order, roots, on_warning)` | Construct the member and report metadata failures without dropping it. |

Resolution rules:

- Base game: fixed name, configured game path, order 0 and ID `ck3:1158310`.
- DLC: use matching packaged `.dlc` metadata; prefer its `pops_id` for the namespaced identifier.
- Workshop: use root `descriptor.mod`, then associated `ROOT_LOCAL_MODS/ugc_<id>.mod` where necessary. Use the existing Workshop identifier, never its numeric directory name as a substitute display name.
- Development mod: use root descriptor, then a matching associated `.mod`; stable ID remains null when none exists.
- Other mount: preserve its path/order and use any available descriptor metadata.

A missing/unreadable path or descriptor, missing name or conflicting metadata invokes `on_warning` with member order, mounted path, attempted descriptor and concrete reason. Keep the member and use `UNKNOWN` where the name cannot be resolved. A valid associated descriptor can supply the name when the root descriptor is missing. No persistent descriptor registry or later path rechecking is introduced.

Stage result: complete production code that constructs the actual ordered playset from a supplied protected debug log.

## Stage 2 — Protect the pair, hash it and write the template

### Edit `harvester.spool_logs`

Add keyword-only parameters:

```python
include_debug: bool = False
on_logs_copied: Callable[[Path, str, str], None] | None = None
# callback: staging directory, capture_id, captured_at
```

The observed-lifecycle watcher supplies `include_debug=True`. This internal option avoids changing manual/archive commands through shared global log-name constants. Keep the current defaults of `LOG_NAMES`, `PRINCIPAL_LOG_NAMES` and `discover_logs` for those existing callers.

Inside `spool_logs`:

1. Copy error.log first through the existing protection mechanics.
2. When requested, copy the complete regular debug.log through `_copy_stable_without_hash`; include it in returned file names, statistics and count after success.
3. If either copy fails, annotate the source/staging path in the existing failure context and do not invoke extraction. Preserve already-copied evidence through the current incomplete-staging behavior.
4. After successful copies, existing copy checks and crash handling, prepare the normal capture ID, timestamp and metadata.
5. Immediately invoke `on_logs_copied` while the copies are in the existing `.copying-*` directory.
6. Publish the completed capture through the existing directory rename.

This uses the existing staging mechanism to expose the completed file set together. Extraction and hashing operate on the copied files. No new publication state machine, background enrichment worker or protected-file monitoring is needed.

### Add `harvester.write_playset_template`

```python
def write_playset_template(directory, *, captured_at, members) -> PlaysetTemplate: ...
```

Reuse `hash_file(directory / "error.log")` and `hash_file(directory / "debug.log")`, once each. Construct `PlaysetTemplate` with both hashes, the existing timestamp and extracted members. Serialize through `to_dict()` and write completed `playset.json` using a temporary file and rename in that directory. Return the written template object so the callback can journal its hashes and joined identifier without rereading or rehashing the logs.

The generated template is not another captured CK3 log. A template-writing failure must not delete the copied logs.

Stage result: production capture support for both raw logs and a playset template with provenance for their exact byte pair.

## Stage 3 — Connect the actual watcher and journal outcomes

Edit `cli._spool_once` to accept and forward `include_debug` and `on_logs_copied` to its existing configured `spool_logs` call.

In `cli.cmd_watch`, add nested `create_captured_playset(directory, capture_id, captured_at)`:

1. Call `playset.extract_playset` on the copied debug log, supplying the configured roots.
2. Route resolution warnings to the existing journal with capture/member/path details.
3. Call `harvester.write_playset_template` to hash both copies and write their associated template.
4. Journal template success or the concrete failure.

Edit `perform_capture` to request paired copying and pass this callback. Keep existing lifecycle/crash observations. After publication, record the final template location rather than the staging location.

Member-name failures still produce a template containing that member. Expected debug-read/hash/template-write I/O failures are logged and leave the raw pair protected without a false template-success claim. Unexpected programming errors remain errors.

Use existing `EventJournal.emit` with `playset_metadata_warning`, `playset_template_created` and `playset_template_failed`; existing `capture_failed` covers log-copy failures. Template-created events include both hashes and `log_pair_id`.

Remove continuous-watcher terminal messages from `on_capture`, `on_error` and its startup/stop/failure paths. Journal outcomes while the journal is open, retaining meaningful process exit codes. Update watch help text. Explicit manual commands retain their present behavior.

Stage result: the actual observed CK3 exit path calls the finished production extractor and delivers both original logs plus the identified playset template.

## Verification and delivery

Production code lives under `src/ck3chronicle/`. Files named `tests/test_...` are automated checks of that code. They are not the implementation, a prototype or a parallel scope.

Update `tests/test_watcher_capture_requirements.py` for paired copying and the callback. Add `tests/test_playset_capture_requirements.py` to exercise the production extractor/writer. Verify:

- Complete error/debug retention and extraction after both copies succeed.
- Base order 0 and exact emitted order across DLC/mod members.
- Descriptor and associated-descriptor names, including Unicode.
- Missing metadata logs a problem while retaining the member/UNKNOWN name.
- Both hashes identify their respective copied contents and the joined identifier uses the specified order.
- Failed copying does not initiate extraction; failed template writing preserves the pair and logs failure.
- The real `cmd_watch` call path invokes this production code and journals outcomes without terminal chatter.

Use genuine recent log copies for the demonstration and isolated destinations for automated failure checks. Run focused checks through the repository `.venv`. Verification does not require starting the live watcher, processing production captures or changing CK3/mod files.

Deliver the implemented watcher, verification results, an example generated by the production code and `docs/WATCHER_ACTIVE_PLAYSET_HANDOFF.md`. Update README/current handoff with the actual delivery. The watcher assignment is complete independently of Task 07.

## Contents of the later pipeline handoff

Task 07 receives the finished producer contract and example. The handoff will state:

- Consume watcher-produced playset.json; do not add another extractor or reconstruct membership.
- Preserve both source-log hashes and log_pair_id as the playset's provenance when attaching it to a Run ID. Keep the existing error-log content hash as the existing Run duplicate key.
- Store the supplied ordered members in Run-owned SQL and derive the review manifest from those stored values.
- Permit historical error logs with no template using playset_captured=false.
- Recognize the artifact during input preparation and preserve the raw pair/template for replay. The old pending processor rejects extra files; it must not silently discard this template.
- Refer to the delivered watcher implementation if later reorganizing capture code. A separate extractor port is unnecessary.

This is communication for the subsequent task. Pipeline schema changes, provider cutover and concurrent Task 07 work are not part of this delivery.
