"""Recover native child boundaries before any matching normalization."""

from __future__ import annotations

import re

from .domain import ByteSpan, Emission, RecoveredDiagnostic
from .emissions import _Text, _collapse, _decode_text, _message

RECOVERY_REVISION = "ck3-diagnostic-recovery-v1"
_PERSISTENT_WRAPPER_RE = re.compile(
    r'^\s*Error\s*:\s*"(?P<inner>.*)"\s+in\s+file\s*:', re.IGNORECASE
)
_PERSISTENT_CLAUSE_START_RE = re.compile(
    r"(?=(?:Unknown\s+trigger|Failed\s+to\s+read\s+key\s+reference)\s*:)", re.IGNORECASE
)


class RecoveryError(ValueError):
    """Original evidence cannot be composed into the requested child."""


def _diagnostic_text(diagnostic: RecoveredDiagnostic) -> _Text:
    pieces = []
    for span in diagnostic.local_spans:
        raw = diagnostic.parent.original.read_bytes(span)
        if len(raw) != span.end - span.start:
            raise RecoveryError("incomplete original child read")
        piece = _decode_text(raw, span.start)
        if pieces:
            pieces.append(piece.literal(" "))
        pieces.append(piece)
    result = _collapse(pieces[0].join(pieces))
    if result.text != diagnostic.decoded_text:
        raise RecoveryError("recovered child text disagrees with original boundaries")
    return result


def recover_diagnostics(emission: Emission) -> tuple[RecoveredDiagnostic, ...]:
    """Return at least one accounted child, including an empty-message child.

    Recognized persistent clauses own disjoint byte ranges. The complement
    (header, wrapper, prefix and suffix) is explicitly shared native evidence.
    Unrecognized wrappers/messages remain one intact child for later review.
    """
    message = _message(emission)
    wrapper = (_PERSISTENT_WRAPPER_RE.match(message.text)
               if emission.source_family.casefold() == "pdx_persistent_reader.cpp" else None)
    if wrapper is not None:
        starts = list(_PERSISTENT_CLAUSE_START_RE.finditer(wrapper.group("inner")))
        if starts:
            base, end = wrapper.span("inner")
            boundaries = [base + match.start() for match in starts] + [end]
            children = []
            first_byte = message.origins[boundaries[0]][0].span.start
            last_byte = message.origins[end - 1][-1].span.end
            shared = (ByteSpan(emission.span.start, first_byte), ByteSpan(last_byte, emission.span.end))
            for ordinal, (left, right) in enumerate(zip(boundaries, boundaries[1:])):
                local = ByteSpan(message.origins[left][0].span.start,
                                 message.origins[right - 1][-1].span.end)
                children.append(RecoveredDiagnostic(
                    emission, ordinal, (local,), shared, message.cut(left, right).strip().text,
                    RECOVERY_REVISION,
                ))
            return tuple(children)
    if message.text:
        local = ByteSpan(message.origins[0][0].span.start, message.origins[-1][-1].span.end)
    else:
        local = ByteSpan(emission.span.end, emission.span.end)
    shared = (ByteSpan(emission.span.start, local.start), ByteSpan(local.end, emission.span.end))
    return (RecoveredDiagnostic(emission, 0, (local,), shared, message.text, RECOVERY_REVISION),)
