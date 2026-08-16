"""Shared C1 parse service: error.log evidence to atomic canonical rows."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sqlite3

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
) -> ParseResult:
    """Parse one ingested session under the C1 canonical contract.

    Evidence validation finishes before replacement begins. Blocks are then
    extracted, normalized, and persisted one at a time inside one transaction.
    Python memory is bounded by the largest lexical block rather than the whole
    log, while readers see either the prior accepted parse or the complete new
    parse—never a partial replacement.
    """
    session = repository.get_session(conn, session_id)
    if session is None:
        raise SessionNotFoundError(f"session_id {session_id} not found")
    if session["capture_status"] != "finalized":
        raise ErrorLogEvidenceError(
            "session evidence has not passed finalized capture verification"
        )

    existing = repository.get_successful_parse_result(conn, session_id)
    if (
        existing is not None
        and existing.parser_contract_version == PARSER_CONTRACT_VERSION
        and not reparse
    ):
        return existing

    manifest = repository.get_error_log_manifest_row(conn, session_id)
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
    digest = hashlib.sha256()
    with log_path.open("rb") as evidence:
        for chunk in iter(lambda: evidence.read(1024 * 1024), b""):
            digest.update(chunk)
    if digest.hexdigest() != manifest["sha256"]:
        raise ErrorLogEvidenceError(
            "captured error.log SHA-256 does not match its manifest row"
        )

    source_blocks = 0
    issue_occurrences = 0
    preamble_blocks = 0
    unclassified_occurrences = 0
    multi_issue_blocks = 0

    try:
        repository.begin_canonical_replacement(conn, session_id)
        for lexical_block in iter_log_blocks(
            log_path,
            log_relpath=log_relpath,
            retain_preamble=False,
        ):
            if lexical_block.timestamp is None:
                preamble_blocks += 1
                continue

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
            source_blocks += 1
            issue_occurrences += len(block_occurrences)
            unclassified_occurrences += sum(
                item.issue.category == "unclassified"
                for item in block_occurrences
            )

        counters = ParseCounters(
            source_blocks=source_blocks,
            preamble_blocks=preamble_blocks,
            issue_occurrences=issue_occurrences,
            issue_clusters=repository.count_canonical_clusters(conn, session_id),
            unclassified_occurrences=unclassified_occurrences,
            multi_issue_blocks=multi_issue_blocks,
            silently_dropped_blocks=0,
        )
        repository.finish_canonical_replacement(
            conn,
            session_id,
            counters,
            PARSER_CONTRACT_VERSION,
        )
    except Exception:
        conn.rollback()
        raise
    return ParseResult(
        session_id=session_id,
        parser_contract_version=PARSER_CONTRACT_VERSION,
        counters=counters,
        mutated=True,
    )
