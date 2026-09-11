"""Extractor registry: ordered lists per log type, unclassified last.

Each extractor module exposes a module-level constant ``CATEGORY`` (str)
and two callables ``match(block) -> bool`` and ``extract(block) -> IssueDraft``.

Log-type dispatch
-----------------
``extract_block_for_log_type(block, log_type)`` selects the extractor list
appropriate for the log file origin:

- ``"error"``              → ``ERROR_EXTRACTORS``  (error.log patterns)
- ``"debug"``              → ``DEBUG_EXTRACTORS``  (debug.log; debug_log first)
- ``"game"``               → ``GAME_EXTRACTORS``   (game.log; unclassified only)
- ``"database_conflicts"`` → ``DB_CONFLICT_EXTRACTORS``
- ``"unknown"``            → ``ERROR_EXTRACTORS``  (safe default)

``extract_block()`` is retained as a legacy alias using ``ERROR_EXTRACTORS``.
"""
from __future__ import annotations

from ck3chronicle.parser.log_blocks import TimestampedLogBlock
from ck3chronicle.models.issue import IssueDraft

from . import (
    debug_log,
    script_system,
    localization,
    descriptor,
    persistent_reader,
    asset_graphics,
    gui_interface,
    event_system,
    database_reference,
    history_setup,
    culture_faith,
    script_hygiene,
    unclassified,
)

# ── Per-log-type extractor lists ──────────────────────────────────────────
# All lists MUST end with ``unclassified`` (its match() always returns True).

ERROR_EXTRACTORS = [
    script_system,
    localization,
    descriptor,
    persistent_reader,
    asset_graphics,
    gui_interface,
    event_system,
    database_reference,
    history_setup,
    culture_faith,
    script_hygiene,
    unclassified,
]

DEBUG_EXTRACTORS = [
    debug_log,          # pdx_localize.cpp / gamedatabase.h — must come first
    script_system,
    localization,
    descriptor,
    persistent_reader,
    asset_graphics,
    gui_interface,
    event_system,
    database_reference,
    history_setup,
    culture_faith,
    script_hygiene,
    unclassified,
]

GAME_EXTRACTORS = [
    # game.log is mostly informational; no specific extractors yet.
    unclassified,
]

DB_CONFLICT_EXTRACTORS = [
    database_reference,
    unclassified,
]

_LOG_TYPE_EXTRACTORS: dict[str, list] = {
    "error": ERROR_EXTRACTORS,
    "debug": DEBUG_EXTRACTORS,
    "game": GAME_EXTRACTORS,
    "database_conflicts": DB_CONFLICT_EXTRACTORS,
    "unknown": ERROR_EXTRACTORS,
}

# Legacy alias — kept for backwards compatibility.
EXTRACTORS = ERROR_EXTRACTORS


# ── Dispatch functions ────────────────────────────────────────────────────

def extract_block(block: TimestampedLogBlock) -> IssueDraft:
    """Legacy dispatch using error-log extractor list.

    The unclassified extractor always claims, so this function never
    returns ``None``.
    """
    for extractor in EXTRACTORS:
        if extractor.match(block):
            return extractor.extract(block)
    # Unreachable: unclassified.match() always returns True.
    return unclassified.extract(block)


def extract_block_for_log_type(block: TimestampedLogBlock, log_type: str) -> IssueDraft:
    """Dispatch to the extractor list appropriate for *log_type*.

    Falls back to ``ERROR_EXTRACTORS`` for unknown log types.
    """
    extractors = _LOG_TYPE_EXTRACTORS.get(log_type, ERROR_EXTRACTORS)
    for extractor in extractors:
        if extractor.match(block):
            return extractor.extract(block)
    # Unreachable: every list ends with unclassified.
    return unclassified.extract(block)
