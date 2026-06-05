"""ck3chronicle CLI entry point."""
from __future__ import annotations

import argparse
import sys
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


def cmd_parse(args: argparse.Namespace) -> int:
    """Parse a previously-ingested session: extract issues + normalize + persist."""
    import json
    from . import config
    from .db import repository
    from .parser.extractors import extract_block
    from .parser.log_blocks import iter_log_blocks
    from .parser.normalize import normalize

    session_id = int(args.session)
    db_path = config.ROOT_CK3CHRONICLE / "ck3chronicle.db"
    conn = repository.open_db(db_path)

    session_row = conn.execute(
        "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
    ).fetchone()
    if session_row is None:
        conn.close()
        print(f"ERROR: session_id {session_id} not found", file=sys.stderr)
        return 2

    snapshot_dir = (
        config.ROOT_CK3CHRONICLE / "sessions" / session_row["evidence_bundle_hash"]
    )

    if args.reparse:
        conn.execute("DELETE FROM issues WHERE session_id = ?", (session_id,))
        conn.execute(
            "DELETE FROM issue_occurrences WHERE session_id = ?", (session_id,)
        )
        conn.commit()

    log_rows = conn.execute(
        "SELECT rel_path FROM session_files WHERE session_id = ? AND kind = 'log'",
        (session_id,),
    ).fetchall()

    issues_written = 0
    occurrences_written = 0

    for log_row in log_rows:
        rel_path = log_row["rel_path"]
        log_path = snapshot_dir / rel_path
        if not log_path.exists():
            continue
        for block in iter_log_blocks(log_path):
            block.log_relpath = rel_path
            draft = extract_block(block)
            if draft is None:
                continue
            result = normalize(draft)

            existing = conn.execute(
                "SELECT issue_id, occurrence_count FROM issues "
                "WHERE session_id = ? AND signature = ?",
                (session_id, result.signature),
            ).fetchone()
            if existing is None:
                conn.execute(
                    """
                    INSERT INTO issues (
                        session_id, signature, category, error_type,
                        tags_json, engine_source, severity, confidence,
                        message_template, sample_message, primary_file, primary_line,
                        referenced_symbols_json, referenced_objects_json,
                        extra_json, occurrence_count
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        session_id,
                        result.signature,
                        result.category,
                        result.error_type,
                        json.dumps(result.tags),
                        result.engine_source,
                        result.severity,
                        float(result.confidence),
                        result.message_template,
                        result.sample_message,
                        result.primary_file,
                        result.primary_line,
                        json.dumps(result.referenced_symbols),
                        json.dumps(result.referenced_objects),
                        json.dumps(result.extra_json),
                        1,
                    ),
                )
                issues_written += 1
            else:
                conn.execute(
                    "UPDATE issues SET occurrence_count = occurrence_count + 1 "
                    "WHERE issue_id = ?",
                    (existing["issue_id"],),
                )

            conn.execute(
                """
                INSERT INTO issue_occurrences (
                    session_id, signature, log_relpath, line_number,
                    raw_block, referenced_symbols_json, extra_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    result.signature,
                    result.log_relpath,
                    result.line_number,
                    result.raw_block,
                    json.dumps(result.referenced_symbols),
                    json.dumps(result.extra_json),
                ),
            )
            occurrences_written += 1

    conn.commit()
    conn.close()
    print(
        f"session_id={session_id}: wrote {issues_written} new issues, "
        f"{occurrences_written} occurrences"
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
        help="Delete existing issues for the session before re-parsing.",
    )
    p_parse.set_defaults(func=cmd_parse)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
