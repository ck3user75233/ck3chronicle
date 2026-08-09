"""ck3chronicle CLI entry point."""
from __future__ import annotations

import argparse
import sys
import pathlib
from pathlib import Path


def cmd_ingest(args: argparse.Namespace) -> int:
    from .ingest import ingest

    logs_root = Path(args.logs) if args.logs else None
    result = ingest(logs_root=logs_root, force=args.force)

    if result.was_duplicate:
        print(f"already ingested; existing session_id: {result.session_id}")
    elif result.forced_duplicate_of is not None:
        print(f"forced duplicate of session_id: {result.forced_duplicate_of}")
        print(f"session_id: {result.session_id}")
    else:
        print(f"evidence_bundle_hash: {result.evidence_bundle_hash}")
        print(f"session_id: {result.session_id}")
        crash_str = ""
        if result.crash_count:
            noun = "artifact" if result.crash_count == 1 else "artifacts"
            crash_str = f", {result.crash_count} crash {noun}"
        print(
            f"copied {result.total_files} files "
            f"({result.log_count} logs{crash_str}) to durable storage"
        )
    return 0


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

    # ingest
    p_ingest = sub.add_parser("ingest", help="Ingest a CK3 evidence bundle.")
    p_ingest.add_argument("--logs", metavar="PATH", help="Path to CK3 logs folder.")
    p_ingest.add_argument(
        "--force",
        action="store_true",
        help="Force re-ingest even if already recorded.",
    )
    p_ingest.set_defaults(func=cmd_ingest)

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
