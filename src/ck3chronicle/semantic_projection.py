"""Pure canonical projection from accepted empirical template contracts.

This module deliberately analyzes the complete lexical block.  The classifier's
bounded token stream establishes template identity; it is not reused as a lossy
source of paths, lines, or concrete typed slot values.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache

from ck3chronicle.classification.inference import ClassificationResult
from ck3chronicle.classification.normalize import (
    KEY,
    LOCATOR,
    OPTIONAL_KEY,
    PARAM,
    PERSISTENT_UNEXPECTED_TOKEN_RE,
    SCRIPT_SYSTEM_ROLE_RE,
    TOKEN_RE,
    TYPE,
    VALUE,
    block_message,
    mask_locators,
    normalize_structured_slots,
)
from ck3chronicle.classification.projection_catalog import (
    ProjectionCatalog,
    ReferenceProjection,
    SemanticProjection,
)
from ck3chronicle.models.issue import IssueDraft, NormalizedIssue
from ck3chronicle.parser.log_blocks import TimestampedLogBlock
from ck3chronicle.parser.normalize import normalize


_PATH_EXTENSIONS = (
    "txt|yml|yaml|gui|dds|asset|mesh|mod|json|wav|ogg|bank|png|tga"
)
_RELATIVE_ROOTS = (
    "mod|common|events|history|localization|gfx|gui|interface|map_data|"
    "game|dlc|music|sound|launcher|workshop"
)
_PATH_VALUE = (
    rf"(?:[A-Za-z]:[\\/][^\s\]\[\(\),;]+|"
    rf"(?:{_RELATIVE_ROOTS})[\\/][^\s\]\[\(\),;]+|"
    rf"[^\s\]\[\(\),;:'\"]+\.(?:{_PATH_EXTENSIONS}))"
)
_QUOTED_PATH_VALUE = rf"(?P<quote>['\"])(?P<quoted>{_PATH_VALUE})(?P=quote)"
_PATH_CAPTURE = rf"(?:{_QUOTED_PATH_VALUE}|(?P<plain>{_PATH_VALUE}))"

_FILE_LABEL_RE = re.compile(
    rf"\b(?:at\s+)?file\s*:\s*(?P<value>{_PATH_CAPTURE})"
    rf"(?:\s+(?:near\s+)?line\s*:?\s*(?P<line>\d+))?",
    re.IGNORECASE,
)
_QUOTED_NEAR_LINE_RE = re.compile(
    rf"(?P<value>{_QUOTED_PATH_VALUE})\s+near\s+line\s*:?\s*(?P<line>\d+)",
    re.IGNORECASE,
)
_PATH_LINE_RE = re.compile(
    rf"(?P<value>{_PATH_CAPTURE}):(?P<line>\d+)\b",
    re.IGNORECASE,
)
_LINE_COLUMN_IN_PATH_RE = re.compile(
    rf"\b(?:at\s+)?line\s*:?\s*(?P<line>\d+)\s+and\s+column\s*:?\s*\d+"
    rf"\s+in\s+(?P<value>{_PATH_CAPTURE})",
    re.IGNORECASE,
)
_OPAQUE_FILE_LABEL_RE = re.compile(
    r"\b(?:Near\s+)?file\s*:\s*(?P<value>[A-Za-z_][A-Za-z0-9_#@.-]*)"
    r"\s+(?:near\s+)?line\s*:?\s*(?P<line>\d+)",
    re.IGNORECASE,
)
_BARE_PATH_RE = re.compile(rf"(?P<value>{_PATH_CAPTURE})", re.IGNORECASE)
_PLACEHOLDER_VALUES = frozenset({KEY, OPTIONAL_KEY, LOCATOR, TYPE, VALUE, PARAM})
_TEMPLATE_SLOTS = _PLACEHOLDER_VALUES
_EVENT_URI_RE = re.compile(r"\[\s*event\s*:\s*(?P<value>/[^\]]+)\]", re.IGNORECASE)
_QUOTED_ARGUMENT_RE = re.compile(r"(?P<quote>['\"])(?P<value>.*?)(?P=quote)")
_PERSISTENT_KEY_RE = re.compile(
    r"\b(?:Unknown\s+trigger|Failed\s+to\s+read\s+key\s+reference)\s*:\s*"
    r"(?P<value>[^,\"]+)",
    re.IGNORECASE,
)
_UNKNOWN_ARGUMENTS_RE = re.compile(
    r"\bfailed\s+for\s+unknown\s+arguments\s*:\s*(?P<value>.*?)"
    r"\.\s+At\s+file\s*:",
    re.IGNORECASE,
)


class SemanticProjectionError(ValueError):
    """Classification and its hash-bound projection catalog are incompatible."""


@dataclass(frozen=True)
class LocatorEvidence:
    path: str
    line: int | None
    form: str


@dataclass(frozen=True)
class SlotEvidence:
    role: str
    ordinal: int
    name: str
    value: str | None
    present: bool


@dataclass(frozen=True)
class CompleteMessageEvidence:
    """Lossless semantic evidence derived independently of bounded tokenization."""

    raw_block: str
    complete_message: str
    semantic_text: str
    location_evidence: str | None
    locators: tuple[LocatorEvidence, ...]
    slots: tuple[SlotEvidence, ...]


def _path_from_match(match: re.Match[str]) -> str:
    value = match.groupdict().get("quoted") or match.groupdict().get("plain")
    if value is None:
        raw = match.group("value").strip()
        value = raw[1:-1] if len(raw) > 1 and raw[0] == raw[-1] and raw[0] in "'\"" else raw
    return value.replace("\\", "/")


def _overlaps(span: tuple[int, int], occupied: list[tuple[int, int]]) -> bool:
    return any(span[0] < other[1] and other[0] < span[1] for other in occupied)


def _extract_locators(message: str) -> tuple[LocatorEvidence, ...]:
    matches: list[tuple[int, int, LocatorEvidence]] = []
    # Event URIs use slash-separated CK3 object names, but they are not source
    # paths. Reserve their spans before applying broad path grammar so they can
    # be projected only by an explicit event_uri contract selector.
    occupied: list[tuple[int, int]] = [
        match.span() for match in _EVENT_URI_RE.finditer(message)
    ]
    patterns = (
        ("file_line", _FILE_LABEL_RE),
        ("quoted_near_line", _QUOTED_NEAR_LINE_RE),
        ("path_line", _PATH_LINE_RE),
        ("line_column_in_path", _LINE_COLUMN_IN_PATH_RE),
        ("opaque_file_line", _OPAQUE_FILE_LABEL_RE),
        ("path", _BARE_PATH_RE),
    )
    for form, pattern in patterns:
        for match in pattern.finditer(message):
            span = match.span()
            if _overlaps(span, occupied):
                continue
            raw_line = match.groupdict().get("line")
            matches.append(
                (
                    span[0],
                    span[1],
                    LocatorEvidence(
                        path=_path_from_match(match),
                        line=int(raw_line) if raw_line is not None else None,
                        form=form,
                    ),
                )
            )
            occupied.append(span)
    return tuple(item[2] for item in sorted(matches, key=lambda item: item[:2]))


def _extract_slots(result: ClassificationResult) -> tuple[SlotEvidence, ...]:
    ordinals: dict[str, int] = {}
    slots: list[SlotEvidence] = []
    for raw in result.structured_slots:
        role_value = raw.get("role")
        if not isinstance(role_value, str) or not role_value:
            continue
        role = role_value.casefold()
        ordinal = ordinals.get(role, 0) + 1
        ordinals[role] = ordinal
        present = raw.get("present") is True
        raw_value = raw.get("value")
        value = raw_value.strip() if isinstance(raw_value, str) else None
        if value in _PLACEHOLDER_VALUES:
            value = None
        name_value = raw.get("name")
        name = (
            name_value
            if isinstance(name_value, str) and name_value
            else f"template_{role}_{ordinal}"
        )
        slots.append(
            SlotEvidence(
                role=role,
                ordinal=ordinal,
                name=name,
                value=value,
                present=present,
            )
        )
    return tuple(slots)


def analyze_complete_message(
    result: ClassificationResult,
    block: TimestampedLogBlock,
) -> CompleteMessageEvidence:
    """Analyze the full lexical message without the classifier's token cap."""
    if block.raw_block:
        complete = block_message(block.raw_block)
    else:
        complete = " ".join(
            item.strip()
            for item in (block.header_line, *block.continuation_lines)
            if item.strip()
        )
    return CompleteMessageEvidence(
        raw_block=block.raw_block,
        complete_message=complete,
        semantic_text=result.semantic_text,
        location_evidence=result.location_evidence,
        locators=_extract_locators(complete),
        slots=_extract_slots(result),
    )


def _severity(level: str | None) -> str:
    normalized_level = (level or "").strip().casefold()
    if normalized_level in {"e", "error", "f", "fatal"}:
        return "error"
    return "warning"


def _slot_value(
    evidence: CompleteMessageEvidence,
    *,
    role: str,
    ordinal: int,
) -> str | None:
    slot = next(
        (
            item
            for item in evidence.slots
            if item.role == role and item.ordinal == ordinal
        ),
        None,
    )
    if slot is None or not slot.present:
        return None
    return slot.value


def _closed_alternatives(token: str) -> tuple[str, ...] | None:
    if not token.startswith("<ALT:") or not token.endswith(">"):
        return None
    values = tuple(token[5:-1].split("|"))
    return values if values and all(values) else None


def _template_alignment(
    candidate: tuple[str, ...], template: tuple[str, ...]
) -> tuple[int, ...] | None:
    """Map candidate token positions to their exact contract token positions."""

    @lru_cache(maxsize=None)
    def match(template_index: int, candidate_index: int) -> tuple[tuple[int, ...], ...]:
        if template_index == len(template):
            return ((),) if candidate_index == len(candidate) else ()
        expected = template[template_index]
        alternatives = _closed_alternatives(expected)
        if alternatives is not None:
            if candidate_index >= len(candidate) or candidate[candidate_index] not in alternatives:
                return ()
            return tuple(
                (template_index, *tail)
                for tail in match(template_index + 1, candidate_index + 1)
            )
        if expected not in _TEMPLATE_SLOTS:
            if candidate_index >= len(candidate) or candidate[candidate_index] != expected:
                return ()
            return tuple(
                (template_index, *tail)
                for tail in match(template_index + 1, candidate_index + 1)
            )
        if expected == LOCATOR:
            if candidate_index >= len(candidate) or candidate[candidate_index] != LOCATOR:
                return ()
            return tuple(
                (template_index, *tail)
                for tail in match(template_index + 1, candidate_index + 1)
            )

        solutions: list[tuple[int, ...]] = []
        if expected == OPTIONAL_KEY:
            solutions.extend(match(template_index + 1, candidate_index))
            if len(solutions) >= 2:
                return tuple(solutions[:2])
        if candidate_index < len(candidate) and candidate[candidate_index] == expected:
            ends = (candidate_index + 1,)
        else:
            ends = tuple(
                end
                for end in range(candidate_index + 1, len(candidate) + 1)
                if not any(token in _TEMPLATE_SLOTS for token in candidate[candidate_index:end])
            )
        for end in ends:
            for tail in match(template_index + 1, end):
                solutions.append((*((template_index,) * (end - candidate_index)), *tail))
                if len(solutions) == 2:
                    return tuple(solutions)
        return tuple(solutions)

    solutions = match(0, 0)
    if len(solutions) != 1 or len(solutions[0]) != len(candidate):
        return None
    return solutions[0]


def _template_span_value(
    result: ClassificationResult,
    projection: SemanticProjection,
    reference: ReferenceProjection,
) -> str | None:
    assert reference.start_ordinal is not None
    assert reference.end_ordinal_exclusive is not None
    masked = mask_locators(normalize_structured_slots(result.semantic_text))
    raw_matches = tuple(TOKEN_RE.finditer(masked))
    collapsed: list[re.Match[str]] = []
    for match in raw_matches:
        if match.group(0) == LOCATOR and collapsed and collapsed[-1].group(0) == LOCATOR:
            continue
        collapsed.append(match)
        if len(collapsed) == 384:
            break
    matches = tuple(collapsed)
    tokens = tuple(match.group(0) for match in matches)
    if tokens != result.normalized_tokens:
        raise SemanticProjectionError(
            "classification token evidence cannot be reconstructed for projection: "
            f"contract={projection.contract_id} reconstructed={tokens!r} "
            f"classified={result.normalized_tokens!r}"
        )
    mapping = _template_alignment(tokens, projection.template_tokens)
    if mapping is None:
        raise SemanticProjectionError(
            "classification tokens no longer align with their semantic contract"
        )
    start = reference.start_ordinal - 1
    end = reference.end_ordinal_exclusive - 1
    indexes = [index for index, ordinal in enumerate(mapping) if start <= ordinal < end]
    if not indexes:
        return None
    value = masked[matches[indexes[0]].start() : matches[indexes[-1]].end()].strip()
    return None if value in _PLACEHOLDER_VALUES else value


def _reference_values(
    reference: ReferenceProjection,
    result: ClassificationResult,
    projection: SemanticProjection,
    evidence: CompleteMessageEvidence,
) -> tuple[str, ...]:
    capture = reference.capture
    if capture == "locator":
        assert reference.ordinal is not None
        index = reference.ordinal - 1
        return (evidence.locators[index].path,) if index < len(evidence.locators) else ()
    if capture == "template_span":
        value = _template_span_value(result, projection, reference)
        return (value,) if value is not None else ()
    if capture == "slot":
        assert reference.role is not None and reference.ordinal is not None
        value = _slot_value(evidence, role=reference.role, ordinal=reference.ordinal)
        return (value,) if value is not None else ()
    if capture == "slot_set":
        assert reference.role is not None
        return tuple(
            value
            for ordinal in reference.ordinals
            if (value := _slot_value(evidence, role=reference.role, ordinal=ordinal))
            is not None
        )
    if capture == "equivalent_slots":
        assert reference.role is not None
        values = tuple(
            _slot_value(evidence, role=reference.role, ordinal=ordinal)
            for ordinal in reference.ordinals
        )
        if any(value is None for value in values):
            return ()
        if len(set(values)) != 1:
            raise SemanticProjectionError("equivalent semantic slots disagree")
        value = values[0]
        assert value is not None
        return (value,)
    if capture == "slot_composition":
        pieces: list[str] = []
        index = 0
        while index < len(reference.parts):
            kind, value = reference.parts[index]
            if kind == "literal":
                pieces.append(str(value))
                index += 1
                continue
            if kind != "role" or index + 1 >= len(reference.parts):
                raise SemanticProjectionError("invalid slot-composition projection")
            ordinal_kind, ordinal = reference.parts[index + 1]
            if ordinal_kind != "ordinal" or not isinstance(ordinal, int):
                raise SemanticProjectionError("invalid slot-composition projection")
            slot = _slot_value(evidence, role=str(value), ordinal=ordinal)
            if slot is None:
                return ()
            pieces.append(slot)
            index += 2
        return ("".join(pieces),)
    if capture == "script_outer_expression":
        match = SCRIPT_SYSTEM_ROLE_RE.match(evidence.complete_message)
        if match is None:
            return ()
        value = re.sub(r"\s*([\.:])\s*", r"\1", match.group("expression").strip())
        return (value,) if value else ()
    if capture == "persistent_key":
        match = _PERSISTENT_KEY_RE.search(evidence.complete_message)
        return (match.group("value").strip(),) if match is not None else ()
    if capture == "unexpected_token":
        match = PERSISTENT_UNEXPECTED_TOKEN_RE.match(evidence.complete_message)
        return (match.group("token").strip(),) if match is not None else ()
    if capture == "event_uri":
        match = _EVENT_URI_RE.search(evidence.complete_message)
        return (match.group("value").strip(),) if match is not None else ()
    if capture == "quoted_argument":
        assert reference.ordinal is not None
        matches = tuple(_QUOTED_ARGUMENT_RE.finditer(evidence.complete_message))
        index = reference.ordinal - 1
        return (matches[index].group("value"),) if index < len(matches) else ()
    if capture == "unknown_arguments":
        match = _UNKNOWN_ARGUMENTS_RE.search(evidence.complete_message)
        if match is None:
            return ()
        return tuple(
            value
            for item in match.group("value").split(",")
            if (value := item.strip())
        )
    raise SemanticProjectionError(f"unsupported reference capture: {capture}")


def _unclassified_draft(
    result: ClassificationResult,
    block: TimestampedLogBlock,
    evidence: CompleteMessageEvidence,
) -> IssueDraft:
    return IssueDraft(
        category="unclassified",
        error_type="unknown",
        tags=[],
        engine_source=result.source_family or block.source_family or "<preamble>",
        sample_message=evidence.complete_message or result.semantic_text,
        primary_file=None,
        primary_line=None,
        referenced_symbols=[],
        referenced_objects=[],
        extra_json={},
        severity=_severity(block.level),
        confidence="low",
        raw_block=block.raw_block,
        log_relpath=block.log_relpath,
        line_number=block.line_number,
    )


def _validate_catalog_binding(
    result: ClassificationResult,
    catalog: ProjectionCatalog,
) -> None:
    if result.model_sha256.casefold() != catalog.model_sha256.casefold():
        raise SemanticProjectionError(
            "classification model SHA-256 does not match projection catalog"
        )
    if result.model_revision_id != catalog.model_revision_id:
        raise SemanticProjectionError(
            "classification model revision does not match projection catalog"
        )


def _resolve_projection(
    result: ClassificationResult,
    catalog: ProjectionCatalog,
) -> tuple[SemanticProjection, str] | None:
    if result.contract_id is None:
        return None
    projection = catalog.projection_for(result.contract_id)
    if projection is None:
        return None
    if projection.source_family.casefold() != result.source_family.casefold():
        raise SemanticProjectionError(
            "classification source family does not match semantic contract"
        )
    confidence = projection.confidence_for(result.assignment_level)
    if confidence is None:
        return None
    return projection, confidence


def project_issue(
    result: ClassificationResult,
    block: TimestampedLogBlock,
    catalog: ProjectionCatalog,
) -> IssueDraft:
    """Project one accepted classification into canonical issue fields.

    An unknown, unreviewed, or assignment-level-incompatible result is preserved
    conservatively.  A stale model/catalog binding is an integrity error rather
    than a silent fallback.
    """
    _validate_catalog_binding(result, catalog)
    evidence = analyze_complete_message(result, block)
    resolved = _resolve_projection(result, catalog)
    if resolved is None:
        return _unclassified_draft(result, block, evidence)

    projection, confidence = resolved
    primary_file: str | None = None
    primary_line: int | None = None
    if projection.primary_locator_ordinal is not None:
        locator_index = projection.primary_locator_ordinal - 1
        if locator_index < len(evidence.locators):
            locator = evidence.locators[locator_index]
            primary_file = locator.path
            primary_line = locator.line

    symbols: list[str] = []
    objects: list[str] = []
    for slot_projection in projection.slot_projections:
        value = _slot_value(
            evidence,
            role=slot_projection.role,
            ordinal=slot_projection.ordinal,
        )
        if value is None:
            continue
        if slot_projection.target == "referenced_symbol":
            symbols.append(value)
        else:
            objects.append(value)
    for reference in projection.reference_projections:
        values = _reference_values(reference, result, projection, evidence)
        if reference.target == "referenced_symbol":
            symbols.extend(values)
        else:
            objects.extend(values)

    return IssueDraft(
        category=projection.category,
        error_type=projection.error_type,
        tags=list(projection.tags),
        engine_source=result.source_family,
        sample_message=projection.message_template,
        primary_file=primary_file,
        primary_line=primary_line,
        referenced_symbols=sorted(set(symbols)),
        referenced_objects=sorted(set(objects)),
        extra_json={},
        severity=_severity(block.level),
        confidence=confidence,
        raw_block=block.raw_block,
        log_relpath=block.log_relpath,
        line_number=block.line_number,
    )


def project_normalized_issue(
    result: ClassificationResult,
    block: TimestampedLogBlock,
    catalog: ProjectionCatalog,
) -> NormalizedIssue:
    """Project and normalize without performing persistence or other I/O."""
    return normalize(project_issue(result, block, catalog))
