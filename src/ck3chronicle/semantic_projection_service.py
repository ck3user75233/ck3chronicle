"""Atomic canonical projection from a persisted classification run."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass

from ck3chronicle.classification.inference import ClassificationResult
from ck3chronicle.classification.projection_catalog import ProjectionCatalog
from ck3chronicle.db import repository
from ck3chronicle.models.issue import NormalizedIssue
from ck3chronicle.parser.log_blocks import TimestampedLogBlock, source_block_id
from ck3chronicle.semantic_projection import project_normalized_issue


SEMANTIC_PROJECTION_CONTRACT_VERSION = "1.0.0"


class SemanticProjectionServiceError(RuntimeError):
    """Base class for stored semantic projection failures."""


class SemanticProjectionPreconditionError(SemanticProjectionServiceError):
    """Required parse, classification, or catalog lineage is unavailable."""


class StoredClassificationError(SemanticProjectionServiceError):
    """Persisted classification payloads are malformed or inconsistent."""


@dataclass(frozen=True)
class PreparedProjectionOccurrence:
    source_block_pk: int
    unit_ordinal: int
    issue: NormalizedIssue


@dataclass(frozen=True)
class SemanticProjectionRunResult:
    projection_run_id: int
    classification_run_id: int
    session_id: int
    model_revision_id: str
    model_sha256: str
    projection_catalog_revision_id: str
    projection_catalog_sha256: str
    projection_contract_version: str
    counts: dict[str, int]
    mutated: bool


def _lineage_counts(row: sqlite3.Row) -> dict[str, int]:
    return {
        "source_blocks": int(row["source_block_count"]),
        "semantic_occurrences": int(row["semantic_occurrence_count"]),
        "issue_clusters": int(row["issue_cluster_count"]),
        "unclassified_occurrences": int(row["unclassified_occurrence_count"]),
        "multi_issue_blocks": int(row["multi_issue_block_count"]),
    }


def _load_string_tuple(raw_json: str, field: str) -> tuple[str, ...]:
    try:
        value = json.loads(raw_json)
    except (TypeError, json.JSONDecodeError) as exc:
        raise StoredClassificationError(f"{field} is not valid JSON") from exc
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise StoredClassificationError(f"{field} is not a string array")
    return tuple(value)


def _load_slots(raw_json: str) -> tuple[dict[str, object], ...]:
    try:
        value = json.loads(raw_json)
    except (TypeError, json.JSONDecodeError) as exc:
        raise StoredClassificationError(
            "structured_slots_json is not valid JSON"
        ) from exc
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise StoredClassificationError("structured_slots_json is not an object array")
    return tuple(dict(item) for item in value)


def _display_lines(raw_block: str, start_line: int) -> tuple[str, list[str]]:
    lines = raw_block.splitlines()
    if not lines:
        return "", []
    header = lines[0]
    if start_line == 1 and header.startswith("\ufeff"):
        header = header[1:]
    return header, lines[1:]


def _reconstruct(
    row: sqlite3.Row,
) -> tuple[TimestampedLogBlock, ClassificationResult]:
    run_model_sha256 = str(row["run_model_sha256"])
    if str(row["payload_model_sha256"]) != run_model_sha256:
        raise StoredClassificationError(
            "classification payload model disagrees with classification run"
        )
    classified_family = str(row["classified_source_family"])
    block_family = str(row["block_source_family"])
    if classified_family.casefold() != block_family.casefold():
        raise StoredClassificationError(
            "classification source family disagrees with source block"
        )
    raw_block = str(row["raw_block"])
    start_line = int(row["start_line"])
    header, continuations = _display_lines(raw_block, start_line)
    raw_hash = str(row["raw_block_sha256"])
    log_relpath = str(row["log_relpath"])
    block = TimestampedLogBlock(
        timestamp=str(row["timestamp"]),
        level=str(row["level"]),
        source_tag=str(row["source_tag"]),
        source_family=block_family,
        header_line=header,
        continuation_lines=continuations,
        raw_block=raw_block,
        log_relpath=log_relpath,
        line_number=start_line,
        end_line=int(row["end_line"]),
        raw_block_sha256=raw_hash,
        raw_byte_length=int(row["raw_byte_length"]),
        source_block_id=source_block_id(log_relpath, start_line, raw_hash),
    )
    result = ClassificationResult(
        source_family=classified_family,
        assignment_level=str(row["assignment_level"]),
        contract_id=(
            str(row["contract_id"]) if row["contract_id"] is not None else None
        ),
        model_revision_id=str(row["model_revision_id"]),
        model_sha256=run_model_sha256,
        confidence=float(row["confidence"]),
        semantic_text=str(row["semantic_text"]),
        location_evidence=(
            str(row["location_evidence"])
            if row["location_evidence"] is not None
            else None
        ),
        normalized_tokens=_load_string_tuple(
            str(row["normalized_tokens_json"]), "normalized_tokens_json"
        ),
        l1_template=(
            str(row["l1_template"]) if row["l1_template"] is not None else None
        ),
        l2_template=(
            str(row["l2_template"]) if row["l2_template"] is not None else None
        ),
        structured_slots=_load_slots(str(row["structured_slots_json"])),
    )
    return block, result


def _lineage_matches(
    row: sqlite3.Row,
    *,
    classification_run_id: int,
    catalog: ProjectionCatalog,
    projection_contract_version: str,
) -> bool:
    return (
        int(row["classification_run_id"]) == classification_run_id
        and str(row["model_sha256"]) == catalog.model_sha256
        and str(row["projection_catalog_sha256"]) == catalog.sha256
        and str(row["projection_catalog_revision_id"]) == catalog.revision_id
        and int(row["projection_catalog_schema_version"]) == catalog.schema_version
        and str(row["projection_contract_version"]) == projection_contract_version
    )


def project_classification_run(
    conn: sqlite3.Connection,
    session_id: int,
    catalog: ProjectionCatalog,
    *,
    reproject: bool = False,
    projection_contract_version: str = SEMANTIC_PROJECTION_CONTRACT_VERSION,
) -> SemanticProjectionRunResult:
    """Rebuild canonical issues from stored classifications in one transaction."""
    session = repository.get_session(conn, session_id)
    if session is None:
        raise SemanticProjectionPreconditionError(f"session_id {session_id} not found")
    if session["parse_status"] != "succeeded":
        raise SemanticProjectionPreconditionError(
            "session must have accepted lexical source blocks before projection"
        )
    classification_run = repository.get_classification_run(
        conn, session_id, catalog.model_sha256
    )
    if classification_run is None:
        raise SemanticProjectionPreconditionError(
            "no stored classification run matches the projection catalog model"
        )
    model = repository.get_classification_model(conn, catalog.model_sha256)
    if model is None:
        raise SemanticProjectionPreconditionError(
            "projection catalog model is not registered"
        )
    if str(model["revision_id"]) != catalog.model_revision_id:
        raise SemanticProjectionPreconditionError(
            "projection catalog model revision disagrees with registered model"
        )
    classification_run_id = int(classification_run["run_id"])

    existing = repository.get_semantic_projection_run(conn, session_id)
    if (
        existing is not None
        and not reproject
        and _lineage_matches(
            existing,
            classification_run_id=classification_run_id,
            catalog=catalog,
            projection_contract_version=projection_contract_version,
        )
    ):
        repository.validate_semantic_projection(
            conn, int(existing["projection_run_id"])
        )
        return SemanticProjectionRunResult(
            projection_run_id=int(existing["projection_run_id"]),
            classification_run_id=classification_run_id,
            session_id=session_id,
            model_revision_id=catalog.model_revision_id,
            model_sha256=catalog.model_sha256,
            projection_catalog_revision_id=catalog.revision_id,
            projection_catalog_sha256=catalog.sha256,
            projection_contract_version=projection_contract_version,
            counts=_lineage_counts(existing),
            mutated=False,
        )

    inputs = repository.get_semantic_projection_inputs(
        conn, classification_run_id
    )
    if len(inputs) != int(classification_run["semantic_occurrence_count"]):
        raise StoredClassificationError(
            "stored classification assignment count disagrees with run lineage"
        )
    prepared: list[PreparedProjectionOccurrence] = []
    for row in inputs:
        block, result = _reconstruct(row)
        try:
            issue = project_normalized_issue(result, block, catalog)
        except ValueError as exc:
            raise StoredClassificationError(
                "stored classification cannot satisfy projection catalog"
            ) from exc
        prepared.append(
            PreparedProjectionOccurrence(
                source_block_pk=int(row["source_block_pk"]),
                unit_ordinal=int(row["unit_ordinal"]),
                issue=issue,
            )
        )

    projection_run_id = repository.replace_semantic_projection(
        conn,
        session_id=session_id,
        classification_run_id=classification_run_id,
        model_sha256=catalog.model_sha256,
        projection_catalog_sha256=catalog.sha256,
        projection_catalog_revision_id=catalog.revision_id,
        projection_catalog_schema_version=catalog.schema_version,
        projection_contract_version=projection_contract_version,
        occurrences=prepared,
    )
    stored = repository.get_semantic_projection_run(conn, session_id)
    if stored is None or int(stored["projection_run_id"]) != projection_run_id:
        raise StoredClassificationError("accepted semantic projection lineage is missing")
    return SemanticProjectionRunResult(
        projection_run_id=projection_run_id,
        classification_run_id=classification_run_id,
        session_id=session_id,
        model_revision_id=catalog.model_revision_id,
        model_sha256=catalog.model_sha256,
        projection_catalog_revision_id=catalog.revision_id,
        projection_catalog_sha256=catalog.sha256,
        projection_contract_version=projection_contract_version,
        counts=_lineage_counts(stored),
        mutated=True,
    )
