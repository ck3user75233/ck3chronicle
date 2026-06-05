"""Extractor registry: ordered list, unclassified last.

Each extractor module exposes a module-level constant ``CATEGORY`` (str)
and two callables ``match(block) -> bool`` and ``extract(block) -> IssueDraft``.
Dispatch order is module-static (the list literal below); the unclassified
extractor is always last and always claims.
"""
from __future__ import annotations

from ck3chronicle.parser.log_blocks import TimestampedLogBlock
from ck3chronicle.models.issue import IssueDraft

from . import (
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


# Deterministic dispatch order. ``unclassified`` MUST be last.
EXTRACTORS = [
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


def extract_block(block: TimestampedLogBlock) -> IssueDraft:
    """Return the first claiming extractor's IssueDraft.

    The unclassified extractor always claims, so this function never
    returns ``None``.
    """
    for extractor in EXTRACTORS:
        if extractor.match(block):
            return extractor.extract(block)
    # Unreachable: unclassified.match() always returns True.
    return unclassified.extract(block)
