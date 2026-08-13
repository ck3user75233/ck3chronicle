"""Classification service over canonical source blocks stored in SQLite."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import sqlite3

from ck3chronicle.db import repository

from .inference import ClassificationResult, Classifier


CLASSIFICATION_CONTRACT_VERSION = "1.0.0"


class ClassificationError(RuntimeError):
    """Base class for operator-facing classification failures."""


class ClassificationPreconditionError(ClassificationError):
    """The session does not have an accepted canonical source-block store."""


@dataclass(frozen=True)
class PreparedAssignment:
    source_block_id: str
    unit_ordinal: int
    result: ClassificationResult


@dataclass(frozen=True)
class ClassificationRunResult:
    run_id: int
    session_id: int
    model_revision_id: str
    model_sha256: str
    classification_contract_version: str
    counts: dict[str, int]
    mutated: bool


def _counts_from_row(row: sqlite3.Row) -> dict[str, int]:
    return {
        "source_blocks": int(row["source_block_count"]),
        "semantic_occurrences": int(row["semantic_occurrence_count"]),
        "full": int(row["full_count"]),
        "l1_l2": int(row["l1_l2_count"]),
        "l1": int(row["l1_count"]),
        "unknown": int(row["unknown_count"]),
    }


def classify_session(
    conn: sqlite3.Connection,
    session_id: int,
    classifier: Classifier,
    *,
    reclassify: bool = False,
) -> ClassificationRunResult:
    """Classify a session's stored source blocks and atomically persist them."""
    session = repository.get_session(conn, session_id)
    if session is None:
        raise ClassificationPreconditionError(f"session_id {session_id} not found")
    if session["capture_status"] != "finalized":
        raise ClassificationPreconditionError("session evidence is not finalized")
    if session["parse_status"] != "succeeded":
        raise ClassificationPreconditionError(
            "session must be successfully parsed before classification"
        )

    repository.ensure_classification_model(conn, classifier.model)

    existing = repository.get_classification_run(
        conn, session_id, classifier.model.sha256
    )
    if existing is not None and not reclassify:
        return ClassificationRunResult(
            run_id=int(existing["run_id"]),
            session_id=session_id,
            model_revision_id=classifier.model.revision_id,
            model_sha256=classifier.model.sha256,
            classification_contract_version=existing[
                "classification_contract_version"
            ],
            counts=_counts_from_row(existing),
            mutated=False,
        )

    blocks = repository.get_classification_source_blocks(conn, session_id)
    expected_blocks = int(session["parse_source_blocks"] or 0)
    if len(blocks) != expected_blocks:
        raise ClassificationPreconditionError(
            "stored source-block count disagrees with successful parse state"
        )

    assignments: list[PreparedAssignment] = []
    for block in blocks:
        results = classifier.classify_block(
            block["source_family"], block["raw_block"]
        )
        if not results:
            raise ClassificationError(
                f"source block {block['source_block_id']} produced no semantic occurrence"
            )
        assignments.extend(
            PreparedAssignment(block["source_block_id"], ordinal, result)
            for ordinal, result in enumerate(results)
        )

    levels = Counter(item.result.assignment_level for item in assignments)
    counts = {
        "source_blocks": len(blocks),
        "semantic_occurrences": len(assignments),
        "full": levels["full"],
        "l1_l2": levels["l1_l2"],
        "l1": levels["l1"],
        "unknown": levels["unknown"],
    }
    run_id = repository.replace_classification_run(
        conn,
        session_id=session_id,
        model=classifier.model,
        assignments=assignments,
        counts=counts,
        classification_contract_version=CLASSIFICATION_CONTRACT_VERSION,
    )
    return ClassificationRunResult(
        run_id=run_id,
        session_id=session_id,
        model_revision_id=classifier.model.revision_id,
        model_sha256=classifier.model.sha256,
        classification_contract_version=CLASSIFICATION_CONTRACT_VERSION,
        counts=counts,
        mutated=True,
    )
