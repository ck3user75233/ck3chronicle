"""ck3chronicle CLI entry point."""
from __future__ import annotations

import argparse
import json
import sys
import pathlib
from pathlib import Path


def _capture_once(args: argparse.Namespace, observation_trigger: str | None = None):
    from .ingest import ingest

    logs_root = Path(args.logs) if args.logs else None
    return ingest(
        logs_root=logs_root,
        observation_trigger=observation_trigger,
        process_name=getattr(args, "process_name", None),
    )


def _spool_once(args: argparse.Namespace, abort_if=None):
    from . import config
    from .harvester import spool_logs

    logs_root = Path(args.logs) if args.logs else config.ROOT_LOGS
    return spool_logs(logs_root, config.ROOT_CK3CHRONICLE, abort_if=abort_if)


def _print_pending_result(result) -> None:
    print(f"protected pending capture: {result.dest_dir}")
    print(f"copied {result.files_copied} logs; hashing and SQLite deferred")


def _print_capture_result(result) -> None:
    if result.was_duplicate:
        print(f"already captured; existing session_id: {result.session_id}")
    else:
        action = "registered existing archive" if result.archive_was_existing else "finalized"
        print(f"{action} evidence_bundle_hash: {result.evidence_bundle_hash}")
        print(f"session_id: {result.session_id}")
        crash_str = ""
        if result.crash_count:
            noun = "artifact" if result.crash_count == 1 else "artifacts"
            crash_str = f", {result.crash_count} crash {noun}"
        print(
            f"preserved {result.total_files} files "
            f"({result.log_count} logs{crash_str}) in durable storage"
        )
    if result.missing_principal_logs:
        print(
            "WARNING: missing principal logs: "
            + ", ".join(result.missing_principal_logs),
            file=sys.stderr,
        )
    for warning in result.reconciliation_errors:
        print(f"WARNING: archive reconciliation failed: {warning}", file=sys.stderr)


def _capture_error(exc: Exception) -> int:
    import sqlite3
    from .harvester import (
        ArchiveIntegrityError,
        InvalidCaptureInput,
        UnstableCapture,
    )

    if isinstance(exc, InvalidCaptureInput):
        print(f"ERROR [invalid_input]: {exc}", file=sys.stderr)
        return 2
    if isinstance(exc, UnstableCapture):
        print(f"ERROR [rejected_unstable]: {exc}", file=sys.stderr)
        return 3
    if isinstance(exc, ArchiveIntegrityError):
        print(f"ERROR [archive_integrity]: {exc}", file=sys.stderr)
        return 3
    if isinstance(exc, sqlite3.Error):
        print(f"ERROR [database_failed]: {exc}", file=sys.stderr)
        return 5
    print(f"ERROR: {exc}", file=sys.stderr)
    return 1


def _emit_command_json(
    command: str,
    *,
    status: str,
    exit_code: int,
    result: dict[str, object] | None = None,
    error_code: str | None = None,
    message: str | None = None,
    stage: str | None = None,
    retryable: bool = False,
) -> None:
    from .command_envelope import command_envelope

    print(
        json.dumps(
            command_envelope(
                command,
                status=status,
                exit_code=exit_code,
                result=result,
                error_code=error_code,
                message=message,
                stage=stage,
                retryable=retryable,
            ),
            sort_keys=True,
        )
    )


def cmd_ingest(args: argparse.Namespace) -> int:
    """Backward-compatible name for finalized evidence capture."""
    try:
        result = _capture_once(args)
    except Exception as exc:
        return _capture_error(exc)
    _print_capture_result(result)
    return 0


def cmd_capture(args: argparse.Namespace) -> int:
    """Immediately protect logs without hashing, parsing, or SQLite."""
    from . import config
    from .watcher import is_process_running, write_capture_receipt

    try:
        if is_process_running("ck3.exe"):
            print(
                "ERROR: ck3.exe is running; refusing to copy a live session",
                file=sys.stderr,
            )
            return 3
        result = _spool_once(args, abort_if=lambda: is_process_running("ck3.exe"))
        write_capture_receipt(
            config.ROOT_CK3CHRONICLE,
            result,
            trigger="manual_capture",
        )
    except Exception as exc:
        return _capture_error(exc)
    _print_pending_result(result)
    return 0


def cmd_watch(args: argparse.Namespace) -> int:
    """Observe exact CK3 lifecycles and protect logs after process exit."""
    from datetime import datetime, timezone

    from . import config
    from .watcher import (
        EventJournal,
        WatcherLease,
        ensure_existing_logs_receipted,
        find_process,
        infer_termination_from_crashes,
        is_process_running,
        scan_crash_inventory,
        watch_sessions,
        write_capture_receipt,
    )

    logs_root = Path(args.logs) if args.logs else config.ROOT_LOGS
    crashes_root = logs_root.parent / "crashes"
    crash_baseline = None
    observed_started_at = None
    observed_ended_at = None
    inferred_termination = "unknown"
    inferred_crash = None
    if args.once:
        try:
            if is_process_running(args.process_name):
                print(
                    f"ERROR: {args.process_name} is running; close CK3 before one-shot capture",
                    file=sys.stderr,
                )
                return 3
            result = _spool_once(
                args,
                abort_if=lambda: is_process_running(args.process_name),
            )
            write_capture_receipt(
                config.ROOT_CK3CHRONICLE,
                result,
                trigger="manual_capture",
            )
        except Exception as exc:
            return _capture_error(exc)
        _print_pending_result(result)
        return 0

    def perform_capture(trigger: str, process):
        result = _spool_once(
            args,
            abort_if=lambda: find_process(args.process_name) is not None,
        )
        termination = inferred_termination
        crash = inferred_crash
        if trigger == "process_exit":
            # Copy first. A second directory-only inventory catches a crash
            # folder that appeared while the live logs were being protected.
            termination, crash = infer_termination_from_crashes(
                crash_baseline,
                scan_crash_inventory(crashes_root),
            )
        write_capture_receipt(
            config.ROOT_CK3CHRONICLE,
            result,
            trigger=trigger,
            process=process,
            observed_started_at=(
                observed_started_at if trigger == "process_exit" else None
            ),
            observed_ended_at=(
                observed_ended_at if trigger == "process_exit" else None
            ),
            termination_kind=(
                termination if trigger == "process_exit" else "unknown"
            ),
            crash=crash if trigger == "process_exit" else None,
        )
        return result

    def on_capture(result, trigger: str) -> None:
        print(f"capture trigger: {trigger}", flush=True)
        _print_pending_result(result)

    def on_error(exc: Exception, trigger: str) -> None:
        print(f"WARNING: {trigger} capture deferred: {exc}", file=sys.stderr)

    try:
        with WatcherLease(config.ROOT_CK3CHRONICLE), EventJournal(
            config.ROOT_CK3CHRONICLE
        ) as journal:
            def lifecycle_event(event: str, fields: dict) -> None:
                nonlocal crash_baseline
                nonlocal observed_started_at, observed_ended_at
                nonlocal inferred_termination, inferred_crash
                if event == "game_started" or (
                    event == "watcher_started"
                    and fields.get("state") == "attached_to_existing_process"
                ):
                    observed_started_at = datetime.now(timezone.utc).isoformat()
                    observed_ended_at = None
                    crash_baseline = scan_crash_inventory(crashes_root)
                    inferred_termination = "unknown"
                    inferred_crash = None
                elif event == "game_exited":
                    observed_ended_at = datetime.now(timezone.utc).isoformat()
                    inferred_termination, inferred_crash = (
                        infer_termination_from_crashes(
                            crash_baseline,
                            scan_crash_inventory(crashes_root),
                        )
                    )
                elif event == "process_replaced":
                    observed_started_at = datetime.now(timezone.utc).isoformat()
                    observed_ended_at = None
                    crash_baseline = scan_crash_inventory(crashes_root)
                    inferred_termination = "unknown"
                    inferred_crash = None
                journal.emit(event, fields)

            print(
                f"watching {args.process_name}; event journal: {journal.path} "
                "(Ctrl+C to stop)",
                flush=True,
            )
            watch_sessions(
                logs_root=logs_root,
                capture=perform_capture,
                process_probe=lambda: find_process(args.process_name),
                startup_recovery_needed=lambda: not ensure_existing_logs_receipted(
                    logs_root,
                    config.ROOT_CK3CHRONICLE,
                ),
                event_sink=lifecycle_event,
                on_capture=on_capture,
                on_error=on_error,
                poll_seconds=args.poll_seconds,
                heartbeat_seconds=args.heartbeat_seconds,
            )
    except KeyboardInterrupt:
        print("watch stopped")
    except Exception as exc:
        return _capture_error(exc)
    return 0


def cmd_reconcile(args: argparse.Namespace) -> int:
    """Register complete orphan archives and verify/adopt legacy bundles."""
    from . import config
    from .archive_registry import reconcile_archives
    from .harvester import finalize_pending_captures
    from .run_registry import reconcile_run_receipts

    try:
        finalized = finalize_pending_captures(config.ROOT_CK3CHRONICLE)
        summary = reconcile_archives(
            config.ROOT_CK3CHRONICLE,
            config.ROOT_CK3CHRONICLE / "ck3chronicle.db",
            full_verify=True,
            strict_integrity=True,
        )
        run_summary = reconcile_run_receipts(
            config.ROOT_CK3CHRONICLE,
            config.ROOT_CK3CHRONICLE / "ck3chronicle.db",
            strict_integrity=True,
        )
    except Exception as exc:
        return _capture_error(exc)
    print(
        f"finalized {len(finalized)} pending; "
        f"scanned {summary.scanned} archives; "
        f"adopted {summary.adopted_legacy} legacy; "
        f"registered {summary.registered} orphaned; "
        f"registered {run_summary.registered} runs"
    )
    errors = summary.errors + run_summary.errors
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


def cmd_sessions(args: argparse.Namespace) -> int:
    from . import config
    from .db import repository

    db_path = config.ROOT_CK3CHRONICLE / "ck3chronicle.db"
    if not db_path.exists():
        print("No sessions yet. Run: ck3chronicle ingest")
        return 0

    conn = repository.open_db_readonly(db_path)
    rows = repository.list_sessions(conn, limit=args.limit)
    conn.close()

    if not rows:
        print("No sessions recorded.")
        return 0

    header = (
        f"{'id':<4}  {'created_at':<26}  {'logs':<4}  "
        f"{'legacy crash files':<18}  {'bytes'}"
    )
    print(header)
    print("-" * len(header))
    for row in rows:
        print(
            f"{row['session_id']:<4}  {row['created_at']:<26}  "
            f"{row['log_count']:<4}  {row['crash_present']:<18}  "
            f"{row['total_bytes']}"
        )
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    from .doctor import run_doctor

    run_doctor()
    return 0


def cmd_audit_db(args: argparse.Namespace) -> int:
    """Audit the archive/index/canonical database contract without mutation."""
    import sqlite3

    from . import config
    from .database_audit import DatabaseAuditError, audit_database

    try:
        result = audit_database(config.ROOT_CK3CHRONICLE, deep=bool(args.deep))
    except DatabaseAuditError as exc:
        print(f"ERROR [database_audit]: {exc}", file=sys.stderr)
        return 2
    except (sqlite3.Error, ValueError, RuntimeError) as exc:
        print(f"ERROR [database_failed]: {exc}", file=sys.stderr)
        return 5
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        summary = result["summary"]
        print(
            f"Database audit: {result['status'].upper()} - "
            f"sessions={summary.get('registered_sessions', 0)}; "
            f"archives={summary.get('archive_directories', 0)}; "
            f"pending={summary.get('pending_directories', 0)}"
        )
        print(
            f"blocks={summary.get('source_blocks', 0):,}; "
            f"raw-headers={summary.get('raw_timestamp_headers', 0):,}; "
            f"occurrences={summary.get('occurrences', 0):,}; "
            f"assignments={summary.get('classification_assignments', 0):,}"
        )
        print(
            f"errors={summary['errors']}; warnings={summary['warnings']}; "
            f"read-only=yes; depth={result['audit_depth']}"
        )
        for item in result["findings"]:
            sessions = (
                f" sessions={','.join(str(value) for value in item['session_ids'])}"
                if item["session_ids"]
                else ""
            )
            print(
                f"[{item['severity'].upper()}] {item['code']} "
                f"{item['message']}{sessions}"
            )
    return 2 if result["status"] == "fail" else 0


def cmd_observe_logging(args: argparse.Namespace) -> int:
    """Journal incremental error/game timestamp progress for one CK3 run."""
    from . import config
    from .logging_observer import observe_logging_progress
    from .watcher import ProcessProbeError, find_process

    logs_root = Path(args.logs) if args.logs else config.ROOT_LOGS
    try:
        journal, observed = observe_logging_progress(
            logs_root=logs_root,
            runtime_root=config.ROOT_CK3CHRONICLE,
            process_probe=lambda: find_process(args.process_name),
            poll_seconds=float(args.poll_seconds),
            heartbeat_seconds=float(args.heartbeat_seconds),
            stall_seconds=float(args.stall_seconds),
        )
    except ProcessProbeError as exc:
        print(f"ERROR [process_probe]: {exc}", file=sys.stderr)
        return 2
    except (OSError, ValueError) as exc:
        print(f"ERROR [logging_observer]: {exc}", file=sys.stderr)
        return 2
    print(f"logging observation journal: {journal}")
    if observed:
        print(
            "OBSERVED: error.log remained at exactly 100,000 timestamp headers "
            "while game.log continued advancing."
        )
    else:
        print("No exact-100,000 boundary with continuing game.log progress observed.")
    return 0


def _log_type_from_relpath(rel_path: str) -> str:
    """Detect log type from filename. Returns 'error', 'debug', 'game', 'database_conflicts', or 'unknown'."""
    name = pathlib.Path(rel_path).name.lower()
    if name.startswith("error"):
        return "error"
    if name.startswith("debug"):
        return "debug"
    if name.startswith("game"):
        return "game"
    if name.startswith("database_conflicts") or name.startswith("database"):
        return "database_conflicts"
    return "unknown"


def cmd_parse(args: argparse.Namespace) -> int:
    """Parse one session's captured error.log into canonical stored records."""
    from . import config
    from .db import repository
    from .parser.service import CanonicalParseError, parse_session

    session_id = int(args.session)
    db_path = config.ROOT_CK3CHRONICLE / "ck3chronicle.db"
    conn = repository.open_db(db_path)
    try:
        result = parse_session(
            conn,
            config.ROOT_CK3CHRONICLE,
            session_id,
            reparse=bool(args.reparse),
        )
    except CanonicalParseError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"ERROR: parse failed: {exc}", file=sys.stderr)
        return 1
    finally:
        conn.close()

    if not result.mutated:
        print(
            f"session_id={session_id}: already parsed "
            f"({result.counters.issue_clusters} issue clusters); "
            "use --reparse to replace"
        )
        return 0

    counters = result.counters
    print(
        f"session_id={session_id}: parsed {counters.source_blocks} source blocks, "
        f"{counters.issue_occurrences} occurrences, "
        f"{counters.issue_clusters} issue clusters"
    )
    return 0


def cmd_classify(args: argparse.Namespace) -> int:
    """Classify and canonically project one stored parsed session."""
    import sqlite3

    from . import config
    from .classification import (
        ClassificationError,
        Classifier,
        ModelIntegrityError,
        classify_session,
        load_model,
    )
    from .classification.catalog import (
        APPROVED_MODEL_SHA256,
        load_approved_semantic_runtime,
        approved_model_path,
    )
    from .classification.projection_catalog import (
        ProjectionCatalogIntegrityError,
        load_projection_catalog,
    )
    from .db import repository
    from .semantic_projection_service import (
        SemanticProjectionServiceError,
        project_classification_run,
    )

    if args.model and not args.model_sha256:
        print("ERROR: --model requires --model-sha256", file=sys.stderr)
        return 2
    if bool(args.projection_catalog) != bool(args.projection_catalog_sha256):
        print(
            "ERROR: --projection-catalog and --projection-catalog-sha256 "
            "must be supplied together",
            file=sys.stderr,
        )
        return 2
    if args.model and not args.projection_catalog:
        print(
            "ERROR: a custom --model requires a hash-pinned "
            "--projection-catalog",
            file=sys.stderr,
        )
        return 2
    conn = None
    try:
        if args.model:
            model_path = Path(args.model)
            model_sha256 = args.model_sha256
            classifier = Classifier(
                load_model(model_path, expected_sha256=model_sha256)
            )
        elif args.projection_catalog:
            classifier = Classifier(
                load_model(
                    approved_model_path(), expected_sha256=APPROVED_MODEL_SHA256
                )
            )
        else:
            classifier, projection_catalog = load_approved_semantic_runtime()
        if args.projection_catalog:
            projection_catalog = load_projection_catalog(
                Path(args.projection_catalog),
                expected_sha256=args.projection_catalog_sha256,
                model=classifier.model,
            )
        conn = repository.open_db(
            config.ROOT_CK3CHRONICLE / "ck3chronicle.db"
        )
        result = classify_session(
            conn,
            int(args.session),
            classifier,
            reclassify=bool(args.reclassify),
        )
        projection = project_classification_run(
            conn, int(args.session), projection_catalog
        )
    except (
        ClassificationError,
        ModelIntegrityError,
        ProjectionCatalogIntegrityError,
        SemanticProjectionServiceError,
        FileNotFoundError,
    ) as exc:
        print(f"ERROR: classification rejected: {exc}", file=sys.stderr)
        return 2
    except sqlite3.Error as exc:
        print(f"ERROR [database_failed]: {exc}", file=sys.stderr)
        return 5
    except Exception as exc:
        print(f"ERROR: classification failed: {exc}", file=sys.stderr)
        return 1
    finally:
        if conn is not None:
            conn.close()

    payload = {
        "schema": "ck3chronicle.classification-run",
        "schema_version": 2,
        "session_id": result.session_id,
        "run_id": result.run_id,
        "model_revision_id": result.model_revision_id,
        "model_sha256": result.model_sha256,
        "classification_contract_version": result.classification_contract_version,
        "counts": result.counts,
        "classification_mutated": result.mutated,
        "semantic_projection": {
            "run_id": projection.projection_run_id,
            "catalog_revision_id": projection.projection_catalog_revision_id,
            "catalog_sha256": projection.projection_catalog_sha256,
            "contract_version": projection.projection_contract_version,
            "counts": projection.counts,
            "mutated": projection.mutated,
        },
        "mutated": result.mutated or projection.mutated,
    }
    if args.json:
        print(json.dumps(payload, sort_keys=True))
    else:
        counts = result.counts
        action = (
            "classified and projected"
            if result.mutated or projection.mutated
            else "already classified and projected"
        )
        print(
            f"session_id={result.session_id}: {action} "
            f"{counts['semantic_occurrences']} semantic occurrences from "
            f"{counts['source_blocks']} blocks "
            f"(full={counts['full']}, l1_l2={counts['l1_l2']}, "
            f"l1={counts['l1']}, unknown={counts['unknown']}); "
            f"model={result.model_revision_id}"
        )
    return 0


def cmd_review_queue(args: argparse.Namespace) -> int:
    """Show stored L1-only and unknown assignments for human adjudication."""
    import sqlite3

    from . import config
    from .classification.catalog import APPROVED_MODEL_SHA256
    from .db import repository

    model_sha256 = args.model_sha256 or APPROVED_MODEL_SHA256
    conn = None
    try:
        conn = repository.open_db_readonly(
            config.ROOT_CK3CHRONICLE / "ck3chronicle.db"
        )
        run = repository.get_classification_run(
            conn, int(args.session), model_sha256
        )
        model = repository.get_classification_model(conn, model_sha256)
        if run is None or model is None:
            print(
                "ERROR: no stored classification run for this session/model",
                file=sys.stderr,
            )
            return 2
        rows = repository.list_classification_review_items(
            conn,
            session_id=int(args.session),
            model_sha256=model_sha256,
            level=args.level,
            limit=int(args.limit),
        )
    except sqlite3.Error as exc:
        print(f"ERROR [database_failed]: {exc}", file=sys.stderr)
        return 5
    finally:
        if conn is not None:
            conn.close()

    items = [
        {
            "assignment_level": row["assignment_level"],
            "source_family": row["source_family"],
            "occurrences": int(row["occurrences"]),
            "first_line": int(row["first_line"]),
            "l1_template": row["l1_template"],
            "l2_template": row["l2_template"],
            "sample": row["sample"],
        }
        for row in rows
    ]
    payload = {
        "schema": "ck3chronicle.classification-review-queue",
        "schema_version": 1,
        "session_id": int(args.session),
        "model_revision_id": model["revision_id"],
        "model_sha256": model_sha256,
        "level": args.level,
        "returned": len(items),
        "items": items,
    }
    if args.json:
        print(json.dumps(payload, sort_keys=True))
    else:
        print(
            f"session_id={args.session}: {len(items)} review patterns "
            f"(model={model['revision_id']})"
        )
        for item in items:
            print(
                f"{item['occurrences']:>7}  {item['assignment_level']:<7}  "
                f"{item['source_family']}:{item['first_line']}  {item['sample']}"
            )
    return 0


def _report_for_args(args: argparse.Namespace, *, latest: bool = False):
    import sqlite3

    from . import config
    from .db import repository
    from .reporting import ReportError, build_session_report, latest_report_target

    conn = None
    try:
        conn = repository.open_db_readonly(
            config.ROOT_CK3CHRONICLE / "ck3chronicle.db"
        )
        observed_run_id = None
        if latest:
            target = latest_report_target(conn)
            if target is None:
                raise ReportError("no reportable runs exist")
            session_id, observed_run_id = target
        elif getattr(args, "run", None) is not None:
            observed_run = repository.get_run(conn, int(args.run))
            if observed_run is None:
                raise ReportError(f"run_id {args.run} not found")
            session_id = int(observed_run["session_id"])
            observed_run_id = int(observed_run["observation_id"])
        else:
            session_id = int(args.session)
        if session_id is None:
            raise ReportError("no captured sessions exist")
        return build_session_report(
            conn,
            session_id,
            model_sha256=getattr(args, "model_sha256", None),
            observed_run_id=observed_run_id,
            limit=int(args.limit),
        )
    finally:
        if conn is not None:
            conn.close()


def _print_executive_report(report: dict[str, object]) -> None:
    observed_run = report["run"]
    session = report["session"]
    classification = report["classification"]
    parse = report["parse"]
    counts = classification["counts"]
    print(
        f"Session {session['session_id']} — captured {session['captured_at']} — "
        f"{session['total_bytes']:,} bytes"
    )
    if observed_run is not None:
        print(
            f"Run {observed_run['run_id']} - ended "
            f"{observed_run['observed_ended_at']} - "
            f"termination={observed_run['termination_kind']}"
        )
        crash = observed_run.get("crash")
        if isinstance(crash, dict):
            exception = crash["exception"]
            retained = exception["retained_path"]
            suffix = f"; retained={retained}" if retained else ""
            print(f"Crash exception: {exception['status']}{suffix}")
    print(
        f"Evidence: {session['log_count']} logs; completeness="
        f"{session['evidence_completeness']}; legacy crash artifacts="
        f"{session['legacy_crash_artifact_present']}"
    )
    print(
        f"Parsed: {parse['source_blocks']:,} blocks; "
        f"{parse['canonical_occurrences']:,} canonical occurrences"
    )
    print(
        f"Classified: {classification['semantic_occurrences']:,} semantic occurrences; "
        f"full={counts['full']:,}, l1+l2={counts['l1_l2']:,}, "
        f"l1={counts['l1']:,}, unknown={counts['unknown']:,}; "
        f"model={classification['model_revision_id']}"
    )
    runtime = report["runtime_context"]
    if runtime is None:
        print("Runtime context: not processed")
    else:
        print(
            f"Runtime context: {runtime['status']}; {runtime['dlc_count']} DLCs; "
            f"{runtime['mod_count']} active mods; "
            f"unknown mounts={runtime['unknown_mount_count']}"
        )
    print("\nTop patterns")
    for pattern in report["top_patterns"]:
        label = pattern["template"] or pattern["sample"]
        print(
            f"{pattern['occurrences']:>8,}  {pattern['assignment_level']:<7}  "
            f"{pattern['source_family']}  {label}"
        )
    print(f"\nReview required: {classification['review_required']:,} occurrences")
    for item in report["review_queue"]:
        print(
            f"{item['occurrences']:>8,}  {item['assignment_level']:<7}  "
            f"{item['source_family']}:{item['first_line']}  {item['sample']}"
        )


def _cmd_report(args: argparse.Namespace, *, latest: bool) -> int:
    import sqlite3

    from .reporting import ReportError
    from .session_intelligence import ComparisonError, compare_sessions

    command = "latest" if latest else "report"
    try:
        if getattr(args, "run", None) is not None and args.since is not None:
            raise ReportError(
                "--since is session-based and cannot be combined with exact --run"
            )
        report = _report_for_args(args, latest=latest)
        comparison = None
        if args.since is not None:
            from . import config
            from .db import repository

            conn = repository.open_db_readonly(
                config.ROOT_CK3CHRONICLE / "ck3chronicle.db"
            )
            try:
                comparison = compare_sessions(
                    conn,
                    int(report["session"]["session_id"]),
                    args.since,
                    model_sha256=str(report["classification"]["model_sha256"]),
                    limit=int(args.limit),
                )
            finally:
                conn.close()
    except (ReportError, ComparisonError, ValueError) as exc:
        if args.json:
            _emit_command_json(
                command,
                status="failed",
                exit_code=2,
                error_code="report_unavailable",
                message=str(exc) or "report unavailable",
                stage="report",
            )
        else:
            print(f"ERROR: report unavailable: {exc}", file=sys.stderr)
        return 2
    except sqlite3.Error as exc:
        if args.json:
            _emit_command_json(
                command,
                status="failed",
                exit_code=5,
                error_code="database_failed",
                message=str(exc) or "database failed",
                stage="database",
            )
        else:
            print(f"ERROR [database_failed]: {exc}", file=sys.stderr)
        return 5
    except Exception as exc:
        if args.json:
            _emit_command_json(
                command,
                status="failed",
                exit_code=1,
                error_code="report_failed",
                message=str(exc) or "report failed",
                stage="report",
            )
        else:
            print(f"ERROR: report failed: {exc}", file=sys.stderr)
        return 1
    if args.json:
        payload = (
            {
                "schema": "ck3chronicle.report-with-comparison",
                "schema_version": 2,
                "report": report,
                "comparison": comparison,
            }
            if comparison is not None
            else report
        )
        _emit_command_json(
            command,
            status="succeeded",
            exit_code=0,
            result=payload,
        )
    else:
        _print_executive_report(report)
        if comparison is not None:
            print()
            _print_session_comparison(comparison)
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    return _cmd_report(args, latest=False)


def cmd_latest(args: argparse.Namespace) -> int:
    return _cmd_report(args, latest=True)


def cmd_errors(args: argparse.Namespace) -> int:
    import sqlite3

    from .reporting import ReportError

    try:
        report = _report_for_args(
            args,
            latest=not bool(args.session or args.run),
        )
    except ReportError as exc:
        if args.json:
            _emit_command_json(
                "errors",
                status="failed",
                exit_code=2,
                error_code="errors_unavailable",
                message=str(exc) or "errors unavailable",
                stage="report",
            )
        else:
            print(f"ERROR: errors unavailable: {exc}", file=sys.stderr)
        return 2
    except sqlite3.Error as exc:
        if args.json:
            _emit_command_json(
                "errors",
                status="failed",
                exit_code=5,
                error_code="database_failed",
                message=str(exc) or "database failed",
                stage="database",
            )
        else:
            print(f"ERROR [database_failed]: {exc}", file=sys.stderr)
        return 5
    except Exception as exc:
        if args.json:
            _emit_command_json(
                "errors",
                status="failed",
                exit_code=1,
                error_code="errors_failed",
                message=str(exc) or "errors failed",
                stage="report",
            )
        else:
            print(f"ERROR: errors failed: {exc}", file=sys.stderr)
        return 1
    payload = {
        "schema": "ck3chronicle.errors",
        "schema_version": 2,
        "run": report["run"],
        "session_id": report["session"]["session_id"],
        "captured_at": report["session"]["captured_at"],
        "model_revision_id": report["classification"]["model_revision_id"],
        "total_occurrences": report["classification"]["semantic_occurrences"],
        "patterns": report["top_patterns"],
    }
    if args.json:
        _emit_command_json(
            "errors",
            status="succeeded",
            exit_code=0,
            result=payload,
        )
    else:
        print(
            f"Session {payload['session_id']} errors — "
            f"{payload['total_occurrences']:,} semantic occurrences"
        )
        if payload["run"] is not None:
            print(
                f"Run {payload['run']['run_id']} - ended "
                f"{payload['run']['observed_ended_at']} - "
                f"termination={payload['run']['termination_kind']}"
            )
        for pattern in payload["patterns"]:
            label = pattern["template"] or pattern["sample"]
            print(
                f"{pattern['occurrences']:>8,}  {pattern['source_family']}  {label}"
            )
    return 0


def cmd_process_pending(args: argparse.Namespace) -> int:
    """Finalize protected copies and bring every session to report-ready state."""
    import sqlite3

    from . import config
    from .classification.catalog import load_approved_semantic_runtime
    from .classification.model import ModelIntegrityError
    from .harvester import ArchiveIntegrityError
    from .processing import process_pending

    def fail(
        exit_code: int,
        code: str,
        message: str,
        stage: str,
        *,
        retryable: bool = False,
    ) -> int:
        message = message or code
        if args.json:
            _emit_command_json(
                "process-pending",
                status="failed",
                exit_code=exit_code,
                error_code=code,
                message=message,
                stage=stage,
                retryable=retryable,
            )
        else:
            print(f"ERROR [{code}]: {message}", file=sys.stderr)
        return exit_code

    try:
        classifier, projection_catalog = load_approved_semantic_runtime()
        result = process_pending(
            config.ROOT_CK3CHRONICLE, classifier, projection_catalog
        )
    except ArchiveIntegrityError as exc:
        return fail(3, "archive_integrity", str(exc), "archive")
    except ModelIntegrityError as exc:
        return fail(4, "model_invalid", str(exc), "classifier")
    except sqlite3.Error as exc:
        return fail(5, "database_failed", str(exc), "database")
    except Exception as exc:
        return fail(1, "processing_failed", str(exc), "pipeline")

    payload = {
        "schema": "ck3chronicle.processing-result",
        "schema_version": 4,
        "finalized_pending": result.finalized_pending,
        "registered_archives": result.registered_archives,
        "registered_runs": result.registered_runs,
        "context_sessions": result.context_sessions,
        "parsed_sessions": result.parsed_sessions,
        "classified_sessions": result.classified_sessions,
        "projected_sessions": result.projected_sessions,
        "reconciliation_errors": list(result.reconciliation_errors),
        "latest_report": result.latest_report,
    }
    if args.json:
        if result.reconciliation_errors:
            _emit_command_json(
                "process-pending",
                status="warning",
                exit_code=1,
                result=payload,
                error_code="reconciliation_incomplete",
                message=(
                    f"{len(result.reconciliation_errors)} archive/run "
                    "reconciliation error(s) remain"
                ),
                stage="reconcile",
                retryable=True,
            )
        else:
            _emit_command_json(
                "process-pending",
                status="succeeded",
                exit_code=0,
                result=payload,
            )
    else:
        print(
            f"finalized={result.finalized_pending}; "
            f"registered={result.registered_archives}; "
            f"runs={result.registered_runs}; "
            f"context={result.context_sessions}; "
            f"parsed={result.parsed_sessions}; "
            f"classified={result.classified_sessions}"
            f"; projected={result.projected_sessions}"
        )
        for error in result.reconciliation_errors:
            print(f"WARNING: {error}", file=sys.stderr)
        if result.latest_report is not None:
            print()
            _print_executive_report(result.latest_report)
    return 1 if result.reconciliation_errors else 0


def _print_session_comparison(comparison: dict[str, object]) -> None:
    previous = comparison["previous_session"]
    current = comparison["current_session"]
    summary = comparison["summary"]
    pattern_counts = summary["pattern_counts"]
    movement = summary["occurrence_movement"]
    policy = summary["policy"]
    print(
        f"Session {current['session_id']} ({current['captured_at']}) vs "
        f"session {previous['session_id']} ({previous['captured_at']})"
    )
    print(
        f"Observed semantic occurrences: {summary['previous_occurrences']:,} -> "
        f"{summary['current_occurrences']:,} "
        f"(net {summary['net_change']:+,})"
    )
    if summary["previous_rate_per_observed_hour"] is not None:
        print(
            "Rate per observed error hour: "
            f"{summary['previous_rate_per_observed_hour']:,.1f} -> "
            f"{summary['current_rate_per_observed_hour']:,.1f} "
            f"(net {summary['rate_delta_per_observed_hour']:+,.1f})"
        )
    print(
        "Patterns: "
        f"new={pattern_counts['new']}, fixed={pattern_counts['fixed']}, "
        f"worse={pattern_counts['worse']}, improved={pattern_counts['improved']}, "
        f"unchanged={pattern_counts['unchanged']}"
    )
    print(
        "Occurrence movement: "
        f"introduced={movement['introduced']:,}, eliminated={movement['eliminated']:,}, "
        f"increased={movement['increased']:,}, reduced={movement['reduced']:,}"
    )
    print(
        f"Actionable changed patterns={policy['actionable_changed_patterns']}; "
        f"ignored annotations={policy['ignored_changed_patterns']}"
    )
    for warning in comparison["evidence_quality"]["warnings"]:
        print(f"WARNING: {warning}")
    runtime_delta = comparison["runtime_context_delta"]
    if not runtime_delta["available"]:
        print(f"Runtime mount comparison unavailable: {runtime_delta['reason']}")
    elif not runtime_delta["runtime_changed"]:
        print(
            "Runtime mounts unchanged: "
            f"{runtime_delta['dlcs']['current_count']} DLCs; "
            f"{runtime_delta['active_mods']['current_count']} active mods"
        )
    else:
        mods = runtime_delta["active_mods"]
        dlcs = runtime_delta["dlcs"]
        print(
            "Runtime mounts changed: "
            f"mods +{len(mods['added'])}/-{len(mods['removed'])}/"
            f"moved {len(mods['moved'])}; "
            f"DLCs +{len(dlcs['added'])}/-{len(dlcs['removed'])}/"
            f"moved {len(dlcs['moved'])}"
        )
        for item in mods["added"]:
            print(f"  added mod: {item['display_name'] or item['key']}")
        for item in mods["removed"]:
            print(f"  removed mod: {item['display_name'] or item['key']}")
    print("\nLargest observed changes")
    for item in comparison["changed_patterns"]:
        label = item["template"] or item["sample"]
        ignored = (
            f" [ignored: {item['ignore_reason']}]" if item["ignored"] else ""
        )
        print(
            f"{item['status']:<8} {item['previous_occurrences']:>8,} -> "
            f"{item['current_occurrences']:<8,} {item['source_family']}  "
            f"{label}{ignored}"
        )


def cmd_compare(args: argparse.Namespace) -> int:
    import sqlite3

    from . import config
    from .db import repository
    from .session_intelligence import (
        ComparisonError,
        compare_against_baseline,
        compare_latest,
        compare_sessions,
    )

    conn = None
    try:
        if args.baseline is not None and args.model_sha256 is not None:
            raise ComparisonError(
                "--model-sha256 cannot override a baseline's pinned model"
            )
        conn = repository.open_db_readonly(
            config.ROOT_CK3CHRONICLE / "ck3chronicle.db"
        )
        if args.baseline is not None:
            comparison = compare_against_baseline(
                conn,
                args.baseline,
                current_session_id=args.session,
                limit=args.limit,
            )
        elif args.session is None:
            comparison = compare_latest(
                conn,
                against_session_id=args.against,
                model_sha256=args.model_sha256,
                limit=args.limit,
            )
        else:
            comparison = compare_sessions(
                conn,
                args.session,
                args.against,
                model_sha256=args.model_sha256,
                limit=args.limit,
            )
    except (ComparisonError, ValueError) as exc:
        print(f"ERROR: comparison unavailable: {exc}", file=sys.stderr)
        return 2
    except sqlite3.Error as exc:
        print(f"ERROR [database_failed]: {exc}", file=sys.stderr)
        return 5
    finally:
        if conn is not None:
            conn.close()
    if args.json:
        print(json.dumps(comparison, sort_keys=True))
    else:
        _print_session_comparison(comparison)
    return 0


def _latest_session_and_model(conn) -> tuple[int, str]:
    from .reporting import latest_session_id

    session_id = latest_session_id(conn)
    if session_id is None:
        raise ValueError("no captured sessions exist")
    run = conn.execute(
        """
        SELECT model_sha256
        FROM classification_runs
        WHERE session_id = ?
        ORDER BY classified_at DESC, run_id DESC
        LIMIT 1
        """,
        (session_id,),
    ).fetchone()
    if run is None:
        raise ValueError(f"latest session {session_id} has not been classified")
    return session_id, str(run["model_sha256"])


def cmd_baseline_create(args: argparse.Namespace) -> int:
    import sqlite3

    from . import config
    from .db import repository
    from .session_intelligence import PolicyError, create_baseline

    conn = None
    try:
        conn = repository.open_db(
            config.ROOT_CK3CHRONICLE / "ck3chronicle.db"
        )
        session_id = args.session
        if session_id is None:
            session_id, _latest_model = _latest_session_and_model(conn)
        baseline = create_baseline(
            conn,
            args.name,
            session_id,
            model_sha256=args.model_sha256,
            note=args.note,
        )
    except (PolicyError, ValueError) as exc:
        print(f"ERROR: baseline unavailable: {exc}", file=sys.stderr)
        return 2
    except sqlite3.Error as exc:
        print(f"ERROR [database_failed]: {exc}", file=sys.stderr)
        return 5
    finally:
        if conn is not None:
            conn.close()
    payload = {
        "schema": "ck3chronicle.baseline",
        "schema_version": 1,
        **baseline,
    }
    if args.json:
        print(json.dumps(payload, sort_keys=True))
    else:
        print(
            f"created baseline {baseline['baseline_name']}: "
            f"session {baseline['session_id']}"
        )
    return 0


def cmd_baseline_list(args: argparse.Namespace) -> int:
    import sqlite3

    from . import config
    from .db import repository
    from .session_intelligence import list_baselines

    conn = None
    try:
        conn = repository.open_db_readonly(
            config.ROOT_CK3CHRONICLE / "ck3chronicle.db"
        )
        baselines = list_baselines(conn)
    except sqlite3.Error as exc:
        print(f"ERROR [database_failed]: {exc}", file=sys.stderr)
        return 5
    finally:
        if conn is not None:
            conn.close()
    if args.json:
        print(
            json.dumps(
                {
                    "schema": "ck3chronicle.baseline-list",
                    "schema_version": 1,
                    "baselines": baselines,
                },
                sort_keys=True,
            )
        )
    else:
        for baseline in baselines:
            note = f" — {baseline['note']}" if baseline["note"] else ""
            print(
                f"{baseline['baseline_name']}: session {baseline['session_id']} "
                f"({baseline['captured_at']}){note}"
            )
    return 0


def cmd_baseline_delete(args: argparse.Namespace) -> int:
    import sqlite3

    from . import config
    from .db import repository
    from .session_intelligence import delete_baseline

    conn = None
    try:
        conn = repository.open_db(
            config.ROOT_CK3CHRONICLE / "ck3chronicle.db"
        )
        deleted = delete_baseline(conn, args.name)
    except sqlite3.Error as exc:
        print(f"ERROR [database_failed]: {exc}", file=sys.stderr)
        return 5
    finally:
        if conn is not None:
            conn.close()
    if not deleted:
        print(f"ERROR: baseline not found: {args.name}", file=sys.stderr)
        return 2
    if args.json:
        print(
            json.dumps(
                {
                    "schema": "ck3chronicle.baseline-deletion",
                    "schema_version": 1,
                    "baseline_name": args.name,
                    "deleted": True,
                },
                sort_keys=True,
            )
        )
    else:
        print(f"deleted baseline: {args.name}")
    return 0


def _policy_model(conn, requested: str | None) -> str:
    if requested is not None:
        return requested
    _session_id, model_sha256 = _latest_session_and_model(conn)
    return model_sha256


def cmd_ignore_add(args: argparse.Namespace) -> int:
    import sqlite3

    from . import config
    from .db import repository
    from .session_intelligence import PolicyError, ignore_pattern

    conn = None
    try:
        conn = repository.open_db(config.ROOT_CK3CHRONICLE / "ck3chronicle.db")
        ignored = ignore_pattern(
            conn,
            _policy_model(conn, args.model_sha256),
            args.pattern_id,
            args.reason,
        )
    except (PolicyError, ValueError) as exc:
        print(f"ERROR: ignore unavailable: {exc}", file=sys.stderr)
        return 2
    except sqlite3.Error as exc:
        print(f"ERROR [database_failed]: {exc}", file=sys.stderr)
        return 5
    finally:
        if conn is not None:
            conn.close()
    payload = {
        "schema": "ck3chronicle.pattern-ignore",
        "schema_version": 1,
        **ignored,
    }
    if args.json:
        print(json.dumps(payload, sort_keys=True))
    else:
        print(f"ignored {ignored['pattern_id']}: {ignored['reason']}")
    return 0


def cmd_ignore_list(args: argparse.Namespace) -> int:
    import sqlite3

    from . import config
    from .db import repository
    from .session_intelligence import list_ignored_patterns

    conn = None
    try:
        conn = repository.open_db_readonly(
            config.ROOT_CK3CHRONICLE / "ck3chronicle.db"
        )
        ignored = list_ignored_patterns(conn, model_sha256=args.model_sha256)
    except sqlite3.Error as exc:
        print(f"ERROR [database_failed]: {exc}", file=sys.stderr)
        return 5
    finally:
        if conn is not None:
            conn.close()
    if args.json:
        print(
            json.dumps(
                {
                    "schema": "ck3chronicle.pattern-ignore-list",
                    "schema_version": 1,
                    "ignored_patterns": ignored,
                },
                sort_keys=True,
            )
        )
    else:
        for item in ignored:
            print(f"{item['pattern_id']}: {item['reason']}")
    return 0


def cmd_ignore_remove(args: argparse.Namespace) -> int:
    import sqlite3

    from . import config
    from .db import repository
    from .session_intelligence import unignore_pattern

    conn = None
    try:
        conn = repository.open_db(config.ROOT_CK3CHRONICLE / "ck3chronicle.db")
        model_sha256 = _policy_model(conn, args.model_sha256)
        deleted = unignore_pattern(conn, model_sha256, args.pattern_id)
    except ValueError as exc:
        print(f"ERROR: ignore unavailable: {exc}", file=sys.stderr)
        return 2
    except sqlite3.Error as exc:
        print(f"ERROR [database_failed]: {exc}", file=sys.stderr)
        return 5
    finally:
        if conn is not None:
            conn.close()
    if not deleted:
        print(f"ERROR: ignored pattern not found: {args.pattern_id}", file=sys.stderr)
        return 2
    if args.json:
        print(
            json.dumps(
                {
                    "schema": "ck3chronicle.pattern-ignore-deletion",
                    "schema_version": 1,
                    "model_sha256": model_sha256,
                    "pattern_id": args.pattern_id,
                    "deleted": True,
                },
                sort_keys=True,
            )
        )
    else:
        print(f"removed ignore: {args.pattern_id}")
    return 0


def cmd_context(args: argparse.Namespace) -> int:
    import sqlite3

    from . import config
    from .db import repository
    from .runtime_context import RuntimeContextError, parse_runtime_context

    conn = None
    try:
        conn = repository.open_db(config.ROOT_CK3CHRONICLE / "ck3chronicle.db")
        result = parse_runtime_context(
            conn,
            config.ROOT_CK3CHRONICLE,
            args.session,
            reparse=args.reparse,
        )
    except RuntimeContextError as exc:
        print(f"ERROR [runtime_context]: {exc}", file=sys.stderr)
        return 3
    except sqlite3.Error as exc:
        print(f"ERROR [database_failed]: {exc}", file=sys.stderr)
        return 5
    finally:
        if conn is not None:
            conn.close()
    payload = {
        "schema": "ck3chronicle.runtime-context",
        "schema_version": 2,
        "session_id": result.session_id,
        "contract_version": result.context_contract_version,
        "status": result.status,
        "debug_log_sha256": result.debug_log_sha256,
        "provenance": {
            "source_session_file_id": result.source_session_file_id,
            "start_line": result.block_start_line,
            "end_line": result.block_end_line,
            "start_byte": result.block_start_byte,
            "end_byte": result.block_end_byte,
            "block_sha256": result.block_sha256,
            "candidate_count": result.block_candidate_count,
            "valid_mount_count": result.valid_mount_count,
            "malformed_mount_count": result.malformed_mount_count,
            "termination_evidence": result.termination_evidence,
            "absence_reason": result.absence_reason,
        },
        "mutated": result.mutated,
        "unknown_mount_count": result.unknown_mount_count,
        "warnings": list(result.warnings),
        "dlcs": [
            {
                "mount_ordinal": item.mount_ordinal,
                "dlc_order": item.dlc_order,
                "dlc_key": item.dlc_key,
                "mount_path": item.mount_path,
            }
            for item in result.dlcs
        ],
        "active_mods": [
            {
                "mount_ordinal": item.mount_ordinal,
                "load_order": item.load_order,
                "mod_key": item.mod_key,
                "mount_path": item.mount_path,
                "source_kind": item.source_kind,
            }
            for item in result.mods
        ],
        "inventory_enrichment": {
            "dlc_count": result.inventory_dlc_count,
            "enabled_mod_count": result.inventory_enabled_mod_count,
            "warnings": list(result.inventory_warnings),
            "dlcs": [
                {
                    "dlc_key": item.dlc_key,
                    "display_name": item.display_name,
                    "descriptor_path": item.descriptor_path,
                }
                for item in result.dlcs
                if item.display_name is not None or item.descriptor_path is not None
            ],
            "mods": [
                {
                    "mod_key": item.mod_key,
                    "display_name": item.display_name,
                    "descriptor_path": item.descriptor_path,
                }
                for item in result.mods
                if item.display_name is not None or item.descriptor_path is not None
            ],
        },
    }
    if args.json:
        print(json.dumps(payload, sort_keys=True))
    else:
        print(
            f"Session {result.session_id} runtime context: {result.status}; "
            f"{len(result.dlcs)} DLCs; {len(result.mods)} active mods"
        )
        for warning in result.warnings:
            print(f"WARNING: {warning}")
        for warning in result.inventory_warnings:
            print(f"INVENTORY: {warning}")
        print("\nMounted DLCs")
        for item in result.dlcs:
            print(
                f"{item.dlc_order:>3}  {item.dlc_key}  "
                f"{item.mount_path}"
            )
        print("\nActive mod load order")
        for item in result.mods:
            print(
                f"{item.load_order:>3}  {item.source_kind:<8}  {item.mod_key}  "
                f"{item.mount_path}"
            )
    return 0


def cmd_resolve_file(args: argparse.Namespace) -> int:
    import sqlite3

    from . import config
    from .db import repository
    from .source_resolution import SourceResolutionError, resolve_file_instances

    conn = None
    try:
        conn = repository.open_db_readonly(
            config.ROOT_CK3CHRONICLE / "ck3chronicle.db"
        )
        resolution = resolve_file_instances(conn, args.session, args.path)
    except SourceResolutionError as exc:
        print(f"ERROR [source_resolution]: {exc}", file=sys.stderr)
        return 2
    except sqlite3.Error as exc:
        print(f"ERROR [database_failed]: {exc}", file=sys.stderr)
        return 5
    finally:
        if conn is not None:
            conn.close()
    if args.json:
        print(json.dumps(resolution, sort_keys=True))
    else:
        print(
            f"Session {resolution['session_id']} — {resolution['relative_path']} — "
            f"{resolution['status']}"
        )
        scope = resolution["scope"]
        print(
            f"Recorded roots={scope['recorded_roots']}; "
            f"missing now={scope['missing_current_roots']}; inactive searched=0"
        )
        for item in resolution["instances"]:
            print(
                f"{item['mount_order']:>3}  {item['source_kind']:<9}  "
                f"{item['display_name'] or item['source_key']}  {item['path']}"
            )
        if resolution["file_layer"]["winner"] is not None:
            winner = resolution["file_layer"]["winner"]
            print(
                "Exact-path file winner: "
                f"{winner['display_name'] or winner['source_key']}"
            )
        print(
            "Domain policy: "
            f"{resolution['domain_layer']['policy']} "
            f"({resolution['domain_layer']['status']})"
        )
        print(f"Caveat: {resolution['caveat']}")
    return 0


def cmd_triage(args: argparse.Namespace) -> int:
    import sqlite3

    from . import config
    from .db import repository
    from .triage import TriageError, build_triage

    conn = None
    try:
        conn = repository.open_db_readonly(
            config.ROOT_CK3CHRONICLE / "ck3chronicle.db"
        )
        triage = build_triage(
            conn,
            session_id=args.session,
            against_session_id=args.against,
            limit=args.limit,
        )
    except (TriageError, ValueError) as exc:
        print(f"ERROR [triage]: {exc}", file=sys.stderr)
        return 2
    except sqlite3.Error as exc:
        print(f"ERROR [database_failed]: {exc}", file=sys.stderr)
        return 5
    finally:
        if conn is not None:
            conn.close()
    if args.json:
        print(json.dumps(triage, sort_keys=True))
    else:
        current = triage["current_session"]
        previous = triage["previous_session"]
        summary = triage["summary"]
        print(
            f"Action triage: session {current['session_id']} vs "
            f"{previous['session_id']} — {summary['regression_patterns_total']} "
            "new/worse patterns"
        )
        print(
            f"Returned={summary['returned_regressions']}; "
            f"source-resolved={summary['source_resolved_regressions']}; "
            f"classification-review={summary['classification_review_occurrences']}"
        )
        for index, item in enumerate(triage["regressions"], 1):
            label = item["template"] or item["sample"]
            print(
                f"\n{index}. {item['status']} {item['previous_occurrences']:,} -> "
                f"{item['current_occurrences']:,}: {label}"
            )
            location = item["location_evidence"]
            if location["dominant_file"]:
                print(
                    f"   dominant file ({location['dominant_file_occurrences']:,}): "
                    f"{location['dominant_file']}"
                )
            resolution = item["source_resolution"]
            if resolution and resolution["file_layer"]["winner"]:
                winner = resolution["file_layer"]["winner"]
                print(
                    "   exact-path file winner: "
                    f"{winner['display_name'] or winner['source_key']}"
                )
                print(
                    "   domain policy: "
                    f"{resolution['domain_layer']['policy']} "
                    f"({resolution['domain_layer']['status']})"
                )
            source_delta = item["source_observation_delta"]
            if source_delta is not None:
                changed = [
                    change
                    for change in source_delta["instances"]
                    if change["status"] != "unchanged"
                ]
                print(
                    "   stored source change: "
                    f"{'yes' if source_delta['changed'] else 'no'}; "
                    f"changed instances={len(changed)}"
                )
                for change in changed[:3]:
                    print(
                        f"      {change['status']}: "
                        f"{change['source_kind']}:{change['source_key']}"
                    )
        if triage["classification_review"]:
            print("\nClassification review remains")
            for item in triage["classification_review"]:
                print(
                    f"{item['occurrences']:>8,} {item['assignment_level']} "
                    f"{item['source_family']}:{item['first_line']} {item['sample']}"
                )
        print(f"\nCaveat: {triage['caveat']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ck3chronicle",
        description=(
            "CK3 log memory — preserve and triage "
            "Crusader Kings III runtime logs."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # urgent copy / legacy archive-and-register command
    p_capture = sub.add_parser(
        "capture",
        help="Immediately copy CK3 logs to the pending queue; defer hashing and SQLite.",
    )
    p_capture.add_argument("--logs", metavar="PATH", help="Path to CK3 logs folder.")
    p_capture.set_defaults(func=cmd_capture)

    p_ingest = sub.add_parser(
        "ingest",
        help="Legacy command: finalize and register logs immediately.",
    )
    p_ingest.add_argument("--logs", metavar="PATH", help="Path to CK3 logs folder.")
    p_ingest.set_defaults(func=cmd_ingest)

    p_watch = sub.add_parser(
        "watch",
        help="Immediately copy logs after each CK3 exit; defer hashing and SQLite.",
    )
    p_watch.add_argument("--logs", metavar="PATH", help="Path to CK3 logs folder.")
    p_watch.add_argument(
        "--process-name", default="ck3.exe", help="Exact CK3 process name."
    )
    p_watch.add_argument("--poll-seconds", type=float, default=0.5, metavar="N")
    p_watch.add_argument(
        "--heartbeat-seconds",
        type=float,
        default=30.0,
        metavar="N",
        help="Write an auditable watcher heartbeat every N seconds.",
    )
    p_watch.add_argument(
        "--once",
        action="store_true",
        help="Copy the current completed-session logs once, then exit.",
    )
    p_watch.set_defaults(func=cmd_watch)

    p_reconcile = sub.add_parser(
        "reconcile",
        help="Verify/adopt archives and repair missing registry rows.",
    )
    p_reconcile.set_defaults(func=cmd_reconcile)

    # sessions
    p_sessions = sub.add_parser("sessions", help="List ingested sessions.")
    p_sessions.add_argument("--limit", type=int, default=50, metavar="N")
    p_sessions.set_defaults(func=cmd_sessions)

    # doctor
    p_doctor = sub.add_parser("doctor", help="Health check.")
    p_doctor.set_defaults(func=cmd_doctor)

    p_audit_db = sub.add_parser(
        "audit-db",
        help="Read-only audit of archives, SQLite rows, and canonical invariants.",
    )
    p_audit_db.add_argument("--json", action="store_true")
    p_audit_db.add_argument(
        "--deep",
        action="store_true",
        help="Also reconcile every block/signature distribution; may take minutes.",
    )
    p_audit_db.set_defaults(func=cmd_audit_db)

    p_observe_logging = sub.add_parser(
        "observe-logging",
        help="Journal error.log/game.log timestamp progress for one CK3 lifecycle.",
    )
    p_observe_logging.add_argument("--logs", metavar="PATH")
    p_observe_logging.add_argument("--process-name", default="ck3.exe")
    p_observe_logging.add_argument("--poll-seconds", type=float, default=2.0)
    p_observe_logging.add_argument("--heartbeat-seconds", type=float, default=30.0)
    p_observe_logging.add_argument(
        "--stall-seconds",
        type=float,
        default=60.0,
        help="Required stable error boundary while game.log advances.",
    )
    p_observe_logging.set_defaults(func=cmd_observe_logging)

    # parse
    p_parse = sub.add_parser(
        "parse",
        help="Extract structured issues from an ingested session's logs.",
    )
    p_parse.add_argument(
        "--session",
        type=int,
        required=True,
        metavar="SESSION_ID",
        help="session_id (from `ck3chronicle sessions`) to parse.",
    )
    p_parse.add_argument(
        "--reparse",
        action="store_true",
        help="Atomically replace the session's prior canonical parse.",
    )
    p_parse.set_defaults(func=cmd_parse)

    p_classify = sub.add_parser(
        "classify",
        help="Classify one parsed session with a hash-pinned empirical model.",
    )
    p_classify.add_argument("--session", type=int, required=True, metavar="SESSION_ID")
    p_classify.add_argument("--model", metavar="PATH")
    p_classify.add_argument("--model-sha256", metavar="SHA256")
    p_classify.add_argument("--projection-catalog", metavar="PATH")
    p_classify.add_argument("--projection-catalog-sha256", metavar="SHA256")
    p_classify.add_argument(
        "--reclassify",
        action="store_true",
        help="Atomically replace this session/model classification run.",
    )
    p_classify.add_argument("--json", action="store_true")
    p_classify.set_defaults(func=cmd_classify)

    p_review = sub.add_parser(
        "review-queue",
        help="List stored L1-only and unknown patterns for human review.",
    )
    p_review.add_argument("--session", type=int, required=True, metavar="SESSION_ID")
    p_review.add_argument(
        "--level", choices=("all", "l1", "unknown"), default="all"
    )
    p_review.add_argument("--limit", type=int, default=100, metavar="N")
    p_review.add_argument("--model-sha256", metavar="SHA256")
    p_review.add_argument("--json", action="store_true")
    p_review.set_defaults(func=cmd_review_queue)

    p_report = sub.add_parser(
        "report", help="Executive report for one stored classified session."
    )
    report_target = p_report.add_mutually_exclusive_group(required=True)
    report_target.add_argument("--session", type=int, metavar="SESSION_ID")
    report_target.add_argument(
        "--run",
        type=int,
        metavar="RUN_ID",
        help="Exact observed run ID; selects chronology even when evidence is reused.",
    )
    p_report.add_argument("--limit", type=int, default=20, metavar="N")
    p_report.add_argument(
        "--since",
        type=int,
        metavar="SESSION_ID",
        help="Append a comparison against this earlier session.",
    )
    p_report.add_argument("--model-sha256", metavar="SHA256")
    p_report.add_argument("--json", action="store_true")
    p_report.set_defaults(func=cmd_report)

    p_latest = sub.add_parser(
        "latest", help="Executive report for the latest captured session."
    )
    p_latest.add_argument("--limit", type=int, default=20, metavar="N")
    p_latest.add_argument(
        "--since",
        type=int,
        metavar="SESSION_ID",
        help="Append a comparison against this earlier session.",
    )
    p_latest.add_argument("--model-sha256", metavar="SHA256")
    p_latest.add_argument("--json", action="store_true")
    p_latest.set_defaults(func=cmd_latest)

    p_errors = sub.add_parser(
        "errors", help="List the most frequent stored semantic error patterns."
    )
    errors_target = p_errors.add_mutually_exclusive_group()
    errors_target.add_argument("--session", type=int, metavar="SESSION_ID")
    errors_target.add_argument(
        "--run",
        type=int,
        metavar="RUN_ID",
        help="Exact observed run ID; defaults to the latest reportable run.",
    )
    p_errors.add_argument("--limit", type=int, default=20, metavar="N")
    p_errors.add_argument("--model-sha256", metavar="SHA256")
    p_errors.add_argument("--json", action="store_true")
    p_errors.set_defaults(func=cmd_errors)

    p_process = sub.add_parser(
        "process-pending",
        help="Finalize, register, parse, classify, and report protected captures.",
    )
    p_process.add_argument("--json", action="store_true")
    p_process.set_defaults(func=cmd_process_pending)

    p_compare = sub.add_parser(
        "compare",
        help="Compare semantic error patterns between classified sessions.",
    )
    p_compare.add_argument(
        "--session",
        type=int,
        metavar="SESSION_ID",
        help="Current session; defaults to the latest captured session.",
    )
    compare_target = p_compare.add_mutually_exclusive_group()
    compare_target.add_argument(
        "--against",
        type=int,
        metavar="SESSION_ID",
        help="Prior session; defaults to the preceding compatible capture.",
    )
    compare_target.add_argument(
        "--baseline",
        metavar="NAME",
        help="Compare against a named baseline and its pinned model.",
    )
    p_compare.add_argument("--limit", type=int, default=50, metavar="N")
    p_compare.add_argument("--model-sha256", metavar="SHA256")
    p_compare.add_argument("--json", action="store_true")
    p_compare.set_defaults(func=cmd_compare)

    p_baseline = sub.add_parser(
        "baseline",
        help="Create, list, or delete named session baselines.",
    )
    baseline_sub = p_baseline.add_subparsers(dest="baseline_command", required=True)
    p_baseline_create = baseline_sub.add_parser(
        "create", help="Create an immutable named session/model baseline."
    )
    p_baseline_create.add_argument("name", metavar="NAME")
    p_baseline_create.add_argument("--session", type=int, metavar="SESSION_ID")
    p_baseline_create.add_argument("--model-sha256", metavar="SHA256")
    p_baseline_create.add_argument("--note")
    p_baseline_create.add_argument("--json", action="store_true")
    p_baseline_create.set_defaults(func=cmd_baseline_create)
    p_baseline_list = baseline_sub.add_parser("list", help="List named baselines.")
    p_baseline_list.add_argument("--json", action="store_true")
    p_baseline_list.set_defaults(func=cmd_baseline_list)
    p_baseline_delete = baseline_sub.add_parser(
        "delete", help="Delete a named baseline pointer; evidence is untouched."
    )
    p_baseline_delete.add_argument("name", metavar="NAME")
    p_baseline_delete.add_argument("--json", action="store_true")
    p_baseline_delete.set_defaults(func=cmd_baseline_delete)

    p_ignore = sub.add_parser(
        "ignore",
        help="Add, list, or remove reasoned model-bound pattern annotations.",
    )
    ignore_sub = p_ignore.add_subparsers(dest="ignore_command", required=True)
    p_ignore_add = ignore_sub.add_parser(
        "add", help="Mark a known pattern ignored while retaining it in reports."
    )
    p_ignore_add.add_argument("pattern_id", metavar="PATTERN_ID")
    p_ignore_add.add_argument("--reason", required=True)
    p_ignore_add.add_argument("--model-sha256", metavar="SHA256")
    p_ignore_add.add_argument("--json", action="store_true")
    p_ignore_add.set_defaults(func=cmd_ignore_add)
    p_ignore_list = ignore_sub.add_parser("list", help="List ignored patterns.")
    p_ignore_list.add_argument("--model-sha256", metavar="SHA256")
    p_ignore_list.add_argument("--json", action="store_true")
    p_ignore_list.set_defaults(func=cmd_ignore_list)
    p_ignore_remove = ignore_sub.add_parser(
        "remove", help="Remove an ignore annotation."
    )
    p_ignore_remove.add_argument("pattern_id", metavar="PATTERN_ID")
    p_ignore_remove.add_argument("--model-sha256", metavar="SHA256")
    p_ignore_remove.add_argument("--json", action="store_true")
    p_ignore_remove.set_defaults(func=cmd_ignore_remove)

    p_context = sub.add_parser(
        "context",
        help="Parse and show same-run mounted DLC and active-mod order.",
    )
    p_context.add_argument("--session", type=int, required=True, metavar="SESSION_ID")
    p_context.add_argument(
        "--reparse",
        action="store_true",
        help="Atomically replace the stored interpretation from archived debug.log.",
    )
    p_context.add_argument("--json", action="store_true")
    p_context.set_defaults(func=cmd_context)

    p_resolve = sub.add_parser(
        "resolve-file",
        help="Find a relative file only in one session's recorded active roots.",
    )
    p_resolve.add_argument("--session", type=int, required=True, metavar="SESSION_ID")
    p_resolve.add_argument("--path", required=True, metavar="RELATIVE_PATH")
    p_resolve.add_argument("--json", action="store_true")
    p_resolve.set_defaults(func=cmd_resolve_file)

    p_triage = sub.add_parser(
        "triage",
        help="Rank new/worse patterns and attach current active-source evidence.",
    )
    p_triage.add_argument("--session", type=int, metavar="SESSION_ID")
    p_triage.add_argument("--against", type=int, metavar="SESSION_ID")
    p_triage.add_argument("--limit", type=int, default=20, metavar="N")
    p_triage.add_argument("--json", action="store_true")
    p_triage.set_defaults(func=cmd_triage)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
