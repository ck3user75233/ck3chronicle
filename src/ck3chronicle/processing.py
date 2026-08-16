"""Deferred archive finalization, parsing, classification, and reporting."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .archive_registry import reconcile_archives
from .classification import Classifier, classify_session
from .db import repository
from .harvester import finalize_pending_captures
from .parser.service import parse_session
from .reporting import build_session_report, latest_report_target
from .runtime_context import parse_runtime_context
from .run_registry import reconcile_run_receipts


@dataclass(frozen=True)
class ProcessingResult:
    finalized_pending: int
    registered_archives: int
    registered_runs: int
    context_sessions: int
    parsed_sessions: int
    classified_sessions: int
    reconciliation_errors: tuple[str, ...]
    latest_report: dict[str, object] | None


def process_pending(root: Path, classifier: Classifier) -> ProcessingResult:
    """Process every finalized session to the current approved derived state.

    The watcher never calls this function. It operates only on protected
    pending copies and immutable archives after the time-critical exit path.
    """
    evidence_root = Path(root)
    finalized = finalize_pending_captures(evidence_root)
    db_path = evidence_root / "ck3chronicle.db"
    reconciliation = reconcile_archives(
        evidence_root,
        db_path,
        strict_integrity=True,
    )
    run_reconciliation = reconcile_run_receipts(
        evidence_root,
        db_path,
        strict_integrity=True,
    )

    parsed = 0
    classified = 0
    context_sessions = 0
    conn = repository.open_db(db_path)
    try:
        # Chronology controls presentation, not processing correctness. Every
        # registered finalized archive is brought to the same derived state.
        for session in repository.list_sessions(conn, limit=1_000_000):
            if session["capture_status"] != "finalized":
                continue
            context = parse_runtime_context(
                conn, evidence_root, int(session["session_id"])
            )
            context_sessions += int(context.mutated)
            if session["parse_status"] != "succeeded":
                parse_result = parse_session(
                    conn, evidence_root, int(session["session_id"])
                )
                parsed += int(parse_result.mutated)
            classification = classify_session(
                conn, int(session["session_id"]), classifier
            )
            classified += int(classification.mutated)

        latest_target = latest_report_target(conn)
        latest_report = (
            build_session_report(
                conn,
                latest_target[0],
                model_sha256=classifier.model.sha256,
                observed_run_id=latest_target[1],
            )
            if latest_target is not None
            else None
        )
    finally:
        conn.close()

    return ProcessingResult(
        finalized_pending=len(finalized),
        registered_archives=reconciliation.registered,
        registered_runs=run_reconciliation.registered,
        context_sessions=context_sessions,
        parsed_sessions=parsed,
        classified_sessions=classified,
        reconciliation_errors=(
            reconciliation.errors + run_reconciliation.errors
        ),
        latest_report=latest_report,
    )
