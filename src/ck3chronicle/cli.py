"""ck3chronicle CLI entry point."""
from __future__ import annotations

import argparse
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
    """Capture and register evidence without parsing it."""
    return cmd_ingest(args)


def cmd_watch(args: argparse.Namespace) -> int:
    """Capture stable logs now and after each observed CK3 process exit."""
    from . import config
    from .watcher import (
        is_process_running,
        wait_for_stable_evidence,
        watch_sessions,
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
            wait_for_stable_evidence(
                logs_root,
                stable_seconds=args.stable_seconds,
                poll_seconds=min(args.poll_seconds, 0.5),
                timeout_seconds=args.timeout_seconds,
                abort_if=lambda: is_process_running(args.process_name),
            )
            result = _capture_once(args)
        except Exception as exc:
            return _capture_error(exc)
        _print_capture_result(result)
        return 0

    print(
        f"watching {args.process_name}; stable logs are captured on process exit "
        "(Ctrl+C to stop)"
    )

    def on_capture(result, trigger: str) -> None:
        print(f"capture trigger: {trigger}")
        _print_capture_result(result)

    def on_error(exc: Exception, trigger: str) -> None:
        print(f"WARNING: {trigger} capture deferred: {exc}", file=sys.stderr)

    try:
        watch_sessions(
            logs_root=logs_root,
            capture=lambda trigger: _capture_once(args, trigger),
            process_probe=lambda: is_process_running(args.process_name),
            on_capture=on_capture,
            on_error=on_error,
            poll_seconds=args.poll_seconds,
            stable_seconds=args.stable_seconds,
            timeout_seconds=args.timeout_seconds,
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

    try:
        summary = reconcile_archives(
            config.ROOT_CK3CHRONICLE,
            config.ROOT_CK3CHRONICLE / "ck3chronicle.db",
            full_verify=True,
        )
    except Exception as exc:
        return _capture_error(exc)
    print(
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ck3chronicle",
        description=(
            "CK3 log memory — preserve and triage "
            "Crusader Kings III runtime logs."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # capture / legacy ingest alias
    p_capture = sub.add_parser(
        "capture",
        help="Atomically preserve and register CK3 logs without parsing them.",
    )
    p_capture.add_argument("--logs", metavar="PATH", help="Path to CK3 logs folder.")
    p_capture.set_defaults(func=cmd_capture)

    p_ingest = sub.add_parser(
        "ingest",
        help="Alias for `capture` (preserves compatibility).",
    )
    p_ingest.add_argument("--logs", metavar="PATH", help="Path to CK3 logs folder.")
    p_ingest.set_defaults(func=cmd_ingest)

    p_watch = sub.add_parser(
        "watch",
        help="Capture existing logs and each future CK3 run in the foreground.",
    )
    p_watch.add_argument("--logs", metavar="PATH", help="Path to CK3 logs folder.")
    p_watch.add_argument(
        "--process-name", default="ck3.exe", help="Exact CK3 process name."
    )
    p_watch.add_argument("--poll-seconds", type=float, default=1.0, metavar="N")
    p_watch.add_argument("--stable-seconds", type=float, default=2.0, metavar="N")
    p_watch.add_argument("--timeout-seconds", type=float, default=30.0, metavar="N")
    p_watch.add_argument(
        "--once",
        action="store_true",
        help="Capture the current stable logs once, then exit.",
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

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
