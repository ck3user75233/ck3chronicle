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
    if isinstance(exc, (UnstableCapture, ArchiveIntegrityError)):
        print(f"ERROR [rejected_unstable]: {exc}", file=sys.stderr)
        return 3
    if isinstance(exc, sqlite3.Error):
        print(f"ERROR [database_failed]: {exc}", file=sys.stderr)
        return 5
    print(f"ERROR: {exc}", file=sys.stderr)
    return 1


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
    from . import config
    from .watcher import (
        EventJournal,
        WatcherLease,
        ensure_existing_logs_receipted,
        find_process,
        is_process_running,
        watch_sessions,
        write_capture_receipt,
    )

    logs_root = Path(args.logs) if args.logs else config.ROOT_LOGS
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
        write_capture_receipt(
            config.ROOT_CK3CHRONICLE,
            result,
            trigger=trigger,
            process=process,
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
                event_sink=journal.emit,
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

    try:
        finalized = finalize_pending_captures(config.ROOT_CK3CHRONICLE)
        summary = reconcile_archives(
            config.ROOT_CK3CHRONICLE,
            config.ROOT_CK3CHRONICLE / "ck3chronicle.db",
            full_verify=True,
        )
    except Exception as exc:
        return _capture_error(exc)
    print(
        f"finalized {len(finalized)} pending; "
        f"scanned {summary.scanned} archives; "
        f"adopted {summary.adopted_legacy} legacy; "
        f"registered {summary.registered} orphaned"
    )
    for error in summary.errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if summary.errors else 0


def cmd_sessions(args: argparse.Namespace) -> int:
    from . import config
    from .db import repository

    db_path = config.ROOT_CK3CHRONICLE / "ck3chronicle.db"
    if not db_path.exists():
        print("No sessions yet. Run: ck3chronicle ingest")
        return 0

    conn = repository.open_db(db_path)
    rows = repository.list_sessions(conn, limit=args.limit)
    conn.close()

    if not rows:
        print("No sessions recorded.")
        return 0

    header = f"{'id':<4}  {'created_at':<26}  {'logs':<4}  {'crash':<5}  {'bytes'}"
    print(header)
    print("-" * len(header))
    for row in rows:
        print(
            f"{row['session_id']:<4}  {row['created_at']:<26}  "
            f"{row['log_count']:<4}  {row['crash_present']:<5}  {row['total_bytes']}"
        )
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    from .doctor import run_doctor

    run_doctor()
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
    """Classify one session from its stored canonical source blocks."""
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
        approved_model_path,
    )
    from .db import repository

    if args.model and not args.model_sha256:
        print("ERROR: --model requires --model-sha256", file=sys.stderr)
        return 2
    model_path = Path(args.model) if args.model else approved_model_path()
    model_sha256 = args.model_sha256 or APPROVED_MODEL_SHA256
    conn = None
    try:
        classifier = Classifier(
            load_model(model_path, expected_sha256=model_sha256)
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
    except (ClassificationError, ModelIntegrityError, FileNotFoundError) as exc:
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
        "schema_version": 1,
        "session_id": result.session_id,
        "run_id": result.run_id,
        "model_revision_id": result.model_revision_id,
        "model_sha256": result.model_sha256,
        "classification_contract_version": result.classification_contract_version,
        "counts": result.counts,
        "mutated": result.mutated,
    }
    if args.json:
        print(json.dumps(payload, sort_keys=True))
    else:
        counts = result.counts
        action = "classified" if result.mutated else "already classified"
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
        conn = repository.open_db(
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

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
