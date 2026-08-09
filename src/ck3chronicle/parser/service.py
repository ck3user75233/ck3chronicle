"""Shared C1 parse service: error.log evidence to atomic canonical rows."""
from __future__ import annotations

from collections import OrderedDict
import hashlib
from pathlib import Path
import sqlite3

from ck3chronicle.db import repository
from ck3chronicle.models.parse import (
    ClusterRecord,
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


PARSER_CONTRACT_VERSION = "1.0.0"


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

    Parsing and normalization finish before persistence begins.  The repository
    then replaces blocks, occurrences, clusters, counters, state, and version in
    one transaction, so either the whole candidate becomes visible or none of
    it does.
    """
    session = repository.get_session(conn, session_id)
    if session is None:
        raise SessionNotFoundError(f"session_id {session_id} not found")

    existing = repository.get_successful_parse_result(conn, session_id)
    if existing is not None and not reparse:
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

    blocks: list[SourceBlockRecord] = []
    occurrences: list[OccurrenceRecord] = []
    # Insertion order is deterministic: first semantic occurrence wins the
    # cluster's representative fields.
    clustered: OrderedDict[str, list[object]] = OrderedDict()
    preamble_blocks = 0
    unclassified_occurrences = 0
    multi_issue_blocks = 0

    for lexical_block in iter_log_blocks(log_path, log_relpath=log_relpath):
        if lexical_block.timestamp is None:
            preamble_blocks += 1
            continue

        extracted = extract_block(lexical_block)
        # C1 accepts the historical single-draft extractor API while C2
        # migrates individual families to multi-draft lists.
        drafts = [extracted] if isinstance(extracted, IssueDraft) else list(extracted)
        if not drafts:
            fallback = unclassified.extract(lexical_block)
            drafts = [fallback] if isinstance(fallback, IssueDraft) else list(fallback)
        if not drafts:
            raise CanonicalParseError(
                f"no fallback issue for source block {lexical_block.source_block_id}"
            )

        normalized = [normalize(draft) for draft in drafts]
        if len(normalized) > 1:
            multi_issue_blocks += 1

        blocks.append(
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
                issue_count=len(normalized),
            )
        )

        for issue_ordinal, issue in enumerate(normalized):
            occurrences.append(
                OccurrenceRecord(
                    source_block_id=lexical_block.source_block_id,
                    issue_ordinal=issue_ordinal,
                    issue=issue,
                )
            )
            if issue.category == "unclassified":
                unclassified_occurrences += 1
            cluster = clustered.get(issue.signature)
            if cluster is None:
                clustered[issue.signature] = [issue, 1]
            else:
                cluster[1] = int(cluster[1]) + 1

    clusters = [
        ClusterRecord(issue=value[0], occurrence_count=int(value[1]))
        for value in clustered.values()
    ]
    counters = ParseCounters(
        source_blocks=len(blocks),
        preamble_blocks=preamble_blocks,
        issue_occurrences=len(occurrences),
        issue_clusters=len(clusters),
        unclassified_occurrences=unclassified_occurrences,
        multi_issue_blocks=multi_issue_blocks,
        silently_dropped_blocks=0,
    )

    repository.replace_canonical_parse(
        conn,
        session_id,
        blocks,
        occurrences,
        clusters,
        counters,
        PARSER_CONTRACT_VERSION,
    )
    return ParseResult(
        session_id=session_id,
        parser_contract_version=PARSER_CONTRACT_VERSION,
        counters=counters,
        mutated=True,
    )
