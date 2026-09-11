"""Shared C1 parse service: error.log evidence to atomic canonical rows."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sqlite3
import time
from typing import Callable, TypeVar

from ck3chronicle.db import repository
from ck3chronicle.models.parse import (
    OccurrenceRecord,
    ParseCounters,
    ParseResult,
    SourceBlockRecord,
)
from ck3chronicle.models.issue import IssueDraft
from ck3chronicle.parser.extractors import extract_block
from ck3chronicle.parser.extractors import unclassified
from ck3chronicle.parser.log_blocks import iter_log_blocks
from ck3chronicle.parser.normalize import normalize


PARSER_CONTRACT_VERSION = "1.0.2"
T = TypeVar("T")
ParseEventSink = Callable[[str, dict[str, object]], None]


def _elapsed_ms(started_ns: int, monotonic_ns: Callable[[], int]) -> float:
    return round((monotonic_ns() - started_ns) / 1_000_000, 3)


def _timed_parse_stage(
    stage: str,
    operation: Callable[[], T],
    *,
    session_id: int,
    event_sink: ParseEventSink | None,
    monotonic_ns: Callable[[], int],
    completion_fields: Callable[[T], dict[str, object]] | None = None,
) -> T:
    context: dict[str, object] = {"stage": stage, "session_id": session_id}
    if event_sink is not None:
        event_sink("stage_started", dict(context))
    started_ns = monotonic_ns()
    try:
        result = operation()
    except BaseException as exc:
        if event_sink is not None:
            event_sink(
                "stage_failed",
                {
                    **context,
                    "duration_ms": _elapsed_ms(started_ns, monotonic_ns),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                },
            )
        raise
    fields = {
        **context,
        "duration_ms": _elapsed_ms(started_ns, monotonic_ns),
    }
    if completion_fields is not None:
        fields.update(completion_fields(result))
    if event_sink is not None:
        event_sink("stage_completed", fields)
    return result


class CanonicalParseError(RuntimeError):
    """Base class for operator-facing C1 parse failures."""


class SessionNotFoundError(CanonicalParseError):
    pass


class ErrorLogEvidenceError(CanonicalParseError):
    pass


def parse_session(
    conn: sqlite3.Connection,
    evidence_root: Path,
    session_id: int,
    *,
    reparse: bool = False,
    event_sink: ParseEventSink | None = None,
    monotonic_ns: Callable[[], int] = time.perf_counter_ns,
) -> ParseResult:
    """Parse one ingested session under the C1 canonical contract.

    Evidence validation finishes before replacement begins. Blocks are then
    extracted, normalized, and persisted one at a time inside one transaction.
    Python memory is bounded by the largest lexical block rather than the whole
    log, while readers see either the prior accepted parse or the complete new
    parse—never a partial replacement.
    """
    session = _timed_parse_stage(
        "parse_lookup_session",
        lambda: repository.get_session(conn, session_id),
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
    )
    if session is None:
        raise SessionNotFoundError(f"session_id {session_id} not found")
    if session["capture_status"] != "finalized":
        raise ErrorLogEvidenceError(
            "session evidence has not passed finalized capture verification"
        )

    existing = _timed_parse_stage(
        "parse_lookup_existing",
        lambda: repository.get_successful_parse_result(conn, session_id),
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
    )
    if (
        existing is not None
        and existing.parser_contract_version == PARSER_CONTRACT_VERSION
        and not reparse
    ):
        return existing

    manifest = _timed_parse_stage(
        "parse_lookup_error_log",
        lambda: repository.get_error_log_manifest_row(conn, session_id),
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
    )
    if manifest is None:
        raise ErrorLogEvidenceError(
            "session must contain exactly one captured error.log manifest row"
        )

    log_relpath = manifest["rel_path"]
    log_path = (
        Path(evidence_root)
        / "sessions"
        / session["evidence_bundle_hash"]
        / log_relpath
    )
    if not log_path.is_file():
        raise ErrorLogEvidenceError(
            f"captured error.log is missing from the session snapshot: {log_path}"
        )
    archived_bytes = log_path.stat().st_size
    if archived_bytes != manifest["bytes"]:
        raise ErrorLogEvidenceError(
            "captured error.log byte length does not match its manifest row"
        )
    def hash_evidence() -> str:
        digest = hashlib.sha256()
        with log_path.open("rb") as evidence:
            for chunk in iter(lambda: evidence.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    evidence_sha256 = _timed_parse_stage(
        "parse_verify_error_log",
        hash_evidence,
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
        completion_fields=lambda _digest: {"input_bytes": archived_bytes},
    )
    if evidence_sha256 != manifest["sha256"]:
        raise ErrorLogEvidenceError(
            "captured error.log SHA-256 does not match its manifest row"
        )

    source_blocks = 0
    issue_occurrences = 0
    preamble_blocks = 0
    unclassified_occurrences = 0
    multi_issue_blocks = 0

    transaction_started_ns = monotonic_ns()
    stream_ns = 0
    transform_ns = 0
    database_append_ns = 0
    if event_sink is not None:
        event_sink(
            "stage_started",
            {"stage": "parse_transaction", "session_id": session_id},
        )
    try:
        _timed_parse_stage(
            "parse_begin_replacement",
            lambda: repository.begin_canonical_replacement(
                conn,
                session_id,
                event_sink=event_sink,
                monotonic_ns=monotonic_ns,
            ),
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
        iterator = iter(
            iter_log_blocks(
                log_path,
                log_relpath=log_relpath,
                retain_preamble=False,
            )
        )
        loop_started_ns = monotonic_ns()
        if event_sink is not None:
            event_sink(
                "stage_started",
                {"stage": "parse_stream_loop", "session_id": session_id},
            )
        while True:
            started_ns = monotonic_ns()
            try:
                lexical_block = next(iterator)
            except StopIteration:
                stream_ns += monotonic_ns() - started_ns
                break
            stream_ns += monotonic_ns() - started_ns
            if lexical_block.timestamp is None:
                preamble_blocks += 1
                continue

            started_ns = monotonic_ns()
            extracted = extract_block(lexical_block)
            # C1 accepts the historical single-draft extractor API while C2
            # migrates individual families to multi-draft lists.
            drafts = (
                [extracted]
                if isinstance(extracted, IssueDraft)
                else list(extracted)
            )
            if not drafts:
                fallback = unclassified.extract(lexical_block)
                drafts = (
                    [fallback]
                    if isinstance(fallback, IssueDraft)
                    else list(fallback)
                )
            if not drafts:
                raise CanonicalParseError(
                    "no fallback issue for source block "
                    f"{lexical_block.source_block_id}"
                )

            normalized = [normalize(draft) for draft in drafts]
            if len(normalized) > 1:
                multi_issue_blocks += 1
            block_occurrences = tuple(
                OccurrenceRecord(
                    source_block_id=lexical_block.source_block_id,
                    issue_ordinal=issue_ordinal,
                    issue=issue,
                )
                for issue_ordinal, issue in enumerate(normalized)
            )
            transform_ns += monotonic_ns() - started_ns
            started_ns = monotonic_ns()
            repository.append_canonical_block(
                conn,
                session_id,
                SourceBlockRecord(
                    source_block_id=lexical_block.source_block_id,
                    log_relpath=log_relpath,
                    start_line=lexical_block.line_number,
                    end_line=lexical_block.end_line,
                    timestamp=lexical_block.timestamp,
                    level=lexical_block.level or "",
                    source_tag=lexical_block.source_tag,
                    source_family=lexical_block.source_family,
                    raw_block_sha256=lexical_block.raw_block_sha256,
                    raw_byte_length=lexical_block.raw_byte_length,
                    raw_block=lexical_block.raw_block,
                    issue_count=len(block_occurrences),
                ),
                block_occurrences,
            )
            database_append_ns += monotonic_ns() - started_ns
            source_blocks += 1
            issue_occurrences += len(block_occurrences)
            unclassified_occurrences += sum(
                item.issue.category == "unclassified"
                for item in block_occurrences
            )
            if event_sink is not None and source_blocks % 5_000 == 0:
                elapsed_ms = _elapsed_ms(loop_started_ns, monotonic_ns)
                event_sink(
                    "stage_progress",
                    {
                        "stage": "parse_stream_loop",
                        "session_id": session_id,
                        "completed_blocks": source_blocks,
                        "occurrences": issue_occurrences,
                        "duration_ms": elapsed_ms,
                        "stream_ms": round(stream_ns / 1_000_000, 3),
                        "transform_ms": round(transform_ns / 1_000_000, 3),
                        "database_append_ms": round(
                            database_append_ns / 1_000_000, 3
                        ),
                        "blocks_per_second": round(
                            source_blocks / (elapsed_ms / 1000), 3
                        ) if elapsed_ms else None,
                    },
                )

        if event_sink is not None:
            event_sink(
                "stage_completed",
                {
                    "stage": "parse_stream_loop",
                    "session_id": session_id,
                    "completed_blocks": source_blocks,
                    "occurrences": issue_occurrences,
                    "preamble_blocks": preamble_blocks,
                    "duration_ms": _elapsed_ms(loop_started_ns, monotonic_ns),
                    "stream_ms": round(stream_ns / 1_000_000, 3),
                    "transform_ms": round(transform_ns / 1_000_000, 3),
                    "database_append_ms": round(
                        database_append_ns / 1_000_000, 3
                    ),
                },
            )

        issue_clusters = _timed_parse_stage(
            "parse_count_clusters",
            lambda: repository.count_canonical_clusters(conn, session_id),
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
        counters = ParseCounters(
            source_blocks=source_blocks,
            preamble_blocks=preamble_blocks,
            issue_occurrences=issue_occurrences,
            issue_clusters=issue_clusters,
            unclassified_occurrences=unclassified_occurrences,
            multi_issue_blocks=multi_issue_blocks,
            silently_dropped_blocks=0,
        )
        repository.finish_canonical_replacement(
            conn,
            session_id,
            counters,
            PARSER_CONTRACT_VERSION,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
        if event_sink is not None:
            event_sink(
                "stage_completed",
                {
                    "stage": "parse_transaction",
                    "session_id": session_id,
                    "duration_ms": _elapsed_ms(
                        transaction_started_ns, monotonic_ns
                    ),
                    "source_blocks": source_blocks,
                    "issue_occurrences": issue_occurrences,
                    "issue_clusters": issue_clusters,
                },
            )
    except BaseException as exc:
        rollback_started_ns = monotonic_ns()
        was_in_transaction = conn.in_transaction
        try:
            conn.rollback()
        finally:
            if event_sink is not None:
                try:
                    event_sink(
                        "transaction_rolled_back",
                        {
                            "stage": "parse_rollback",
                            "session_id": session_id,
                            "was_in_transaction": was_in_transaction,
                            "duration_ms": _elapsed_ms(
                                rollback_started_ns, monotonic_ns
                            ),
                            "completed_blocks": source_blocks,
                            "error_type": type(exc).__name__,
                            "error": str(exc),
                        },
                    )
                    event_sink(
                        "stage_failed",
                        {
                            "stage": "parse_transaction",
                            "session_id": session_id,
                            "duration_ms": _elapsed_ms(
                                transaction_started_ns, monotonic_ns
                            ),
                            "completed_blocks": source_blocks,
                            "error_type": type(exc).__name__,
                            "error": str(exc),
                        },
                    )
                except Exception:
                    pass
        raise
    return ParseResult(
        session_id=session_id,
        parser_contract_version=PARSER_CONTRACT_VERSION,
        counters=counters,
        mutated=True,
    )
