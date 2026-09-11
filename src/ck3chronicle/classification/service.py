"""Classification service over canonical source blocks stored in SQLite."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import sqlite3
import time
from typing import Callable, TypeVar

from ck3chronicle.db import repository

from .inference import ClassificationResult, Classifier


CLASSIFICATION_CONTRACT_VERSION = "2.0.1"
T = TypeVar("T")
ClassificationEventSink = Callable[[str, dict[str, object]], None]


def _elapsed_ms(started_ns: int, monotonic_ns: Callable[[], int]) -> float:
    return round((monotonic_ns() - started_ns) / 1_000_000, 3)


def _timed_classification_stage(
    stage: str,
    operation: Callable[[], T],
    *,
    session_id: int,
    event_sink: ClassificationEventSink | None,
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


class ClassificationError(RuntimeError):
    """Base class for operator-facing classification failures."""


class ClassificationPreconditionError(ClassificationError):
    """The session does not have an accepted canonical source-block store."""


@dataclass(frozen=True)
class PreparedAssignment:
    source_block_pk: int
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
    event_sink: ClassificationEventSink | None = None,
    monotonic_ns: Callable[[], int] = time.perf_counter_ns,
) -> ClassificationRunResult:
    """Classify a session's stored source blocks and atomically persist them."""
    session = _timed_classification_stage(
        "classification_lookup_session",
        lambda: repository.get_session(conn, session_id),
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
    )
    if session is None:
        raise ClassificationPreconditionError(f"session_id {session_id} not found")
    if session["capture_status"] != "finalized":
        raise ClassificationPreconditionError("session evidence is not finalized")
    if session["parse_status"] != "succeeded":
        raise ClassificationPreconditionError(
            "session must be successfully parsed before classification"
        )

    _timed_classification_stage(
        "classification_ensure_model",
        lambda: repository.ensure_classification_model(conn, classifier.model),
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
    )

    existing = _timed_classification_stage(
        "classification_lookup_existing",
        lambda: repository.get_classification_run(
            conn, session_id, classifier.model.sha256
        ),
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
    )
    if (
        existing is not None
        and not reclassify
        and existing["classification_contract_version"]
        == CLASSIFICATION_CONTRACT_VERSION
    ):
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

    blocks = _timed_classification_stage(
        "classification_load_blocks",
        lambda: repository.get_classification_source_blocks(conn, session_id),
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
        completion_fields=lambda rows: {"block_count": len(rows)},
    )
    expected_blocks = int(session["parse_source_blocks"] or 0)
    if len(blocks) != expected_blocks:
        raise ClassificationPreconditionError(
            "stored source-block count disagrees with successful parse state"
        )

    assignments: list[PreparedAssignment] = []
    cached_results: dict[
        tuple[str, int], tuple[ClassificationResult, ...]
    ] = {}
    block_analysis_reuses = 0
    preparation_started_ns = monotonic_ns()
    next_progress_ns = preparation_started_ns + 5_000_000_000
    if event_sink is not None:
        event_sink(
            "stage_started",
            {"stage": "classification_prepare", "session_id": session_id},
        )
    completed_blocks = 0
    try:
        for index, block in enumerate(blocks, start=1):
            cache_key = (
                str(block["source_family"]),
                int(block["raw_block_pk"]),
            )
            results = cached_results.get(cache_key)
            if results is None:
                results = tuple(
                    classifier.classify_block(
                        block["source_family"], block["raw_block"]
                    )
                )
                cached_results[cache_key] = results
            else:
                block_analysis_reuses += 1
            if not results:
                raise ClassificationError(
                    f"source block {block['source_block_pk']} produced no semantic occurrence"
                )
            assignments.extend(
                PreparedAssignment(int(block["source_block_pk"]), ordinal, result)
                for ordinal, result in enumerate(results)
            )
            completed_blocks = index
            progress_ns = monotonic_ns() if index % 250 == 0 else None
            if (
                event_sink is not None
                and progress_ns is not None
                and (
                    progress_ns >= next_progress_ns
                    or index % 10_000 == 0
                )
            ):
                elapsed_ms = _elapsed_ms(preparation_started_ns, monotonic_ns)
                event_sink(
                    "stage_progress",
                    {
                        "stage": "classification_prepare",
                        "session_id": session_id,
                        "completed_blocks": index,
                        "total_blocks": len(blocks),
                        "assignments": len(assignments),
                        "unique_block_analyses": len(cached_results),
                        "block_analysis_reuses": block_analysis_reuses,
                        "current_raw_block_pk": int(block["raw_block_pk"]),
                        "duration_ms": elapsed_ms,
                        "blocks_per_second": round(
                            index / (elapsed_ms / 1000), 3
                        ) if elapsed_ms else None,
                    },
                )
                next_progress_ns = progress_ns + 5_000_000_000
    except BaseException as exc:
        if event_sink is not None:
            event_sink(
                "stage_failed",
                {
                    "stage": "classification_prepare",
                    "session_id": session_id,
                    "completed_blocks": completed_blocks,
                    "total_blocks": len(blocks),
                    "assignments": len(assignments),
                    "unique_block_analyses": len(cached_results),
                    "block_analysis_reuses": block_analysis_reuses,
                    "duration_ms": _elapsed_ms(
                        preparation_started_ns, monotonic_ns
                    ),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                },
            )
        raise
    if event_sink is not None:
        event_sink(
            "stage_completed",
            {
                "stage": "classification_prepare",
                "session_id": session_id,
                "completed_blocks": len(blocks),
                "assignments": len(assignments),
                "unique_block_analyses": len(cached_results),
                "block_analysis_reuses": block_analysis_reuses,
                "duration_ms": _elapsed_ms(preparation_started_ns, monotonic_ns),
            },
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
    run_id = _timed_classification_stage(
        "classification_persist",
        lambda: repository.replace_classification_run(
            conn,
            session_id=session_id,
            model=classifier.model,
            assignments=assignments,
            counts=counts,
            classification_contract_version=CLASSIFICATION_CONTRACT_VERSION,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        ),
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
        completion_fields=lambda value: {
            "classification_run_id": value,
            **counts,
        },
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
