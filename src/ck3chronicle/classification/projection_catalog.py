"""Hash-bound semantic projections for accepted empirical contracts.

The empirical classifier answers which ordered template matched.  This catalog
answers what that reviewed template means to canonical storage.  Keeping the
projection metadata in a separately hash-verified artifact lets a model be
reprojected without returning to broad source-name heuristics.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any

from ck3chronicle.models.issue import ConfidenceValue, KNOWN_CATEGORIES

from .model import EmpiricalModel, ModelCluster


PROJECTION_SCHEMA = "ck3chronicle-semantic-projection-catalog"
PROJECTION_SCHEMA_VERSION = 2

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_IDENTIFIER_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_ASSIGNMENT_LEVELS = frozenset({"full", "l1_l2", "l1"})
_CONFIDENCE_VALUES = frozenset({"high", "medium", "low"})
_ACCOUNTING_VALUES = frozenset({"classified", "preserved_unclassified"})
_SLOT_ROLES = frozenset({"key", "optional_key", "value", "param", "type"})
_SLOT_TARGETS = frozenset({"referenced_symbol", "referenced_object"})
_CONTRACT_KINDS = frozenset({"model_full", "composed_l1_l2"})
_REFERENCE_CAPTURES = frozenset(
    {
        "event_uri",
        "equivalent_slots",
        "locator",
        "persistent_key",
        "quoted_argument",
        "script_outer_expression",
        "slot",
        "slot_composition",
        "slot_set",
        "template_span",
        "unexpected_token",
        "unknown_arguments",
    }
)


class ProjectionCatalogIntegrityError(ValueError):
    """The semantic projection artifact is corrupt or incompatible."""


@dataclass(frozen=True)
class SlotProjection:
    """Project one typed template slot into one canonical reference list."""

    role: str
    ordinal: int
    target: str


@dataclass(frozen=True)
class ReferenceProjection:
    """Contract-bound extraction from complete, non-lossy message evidence."""

    capture: str
    target: str
    ordinal: int | None = None
    start_ordinal: int | None = None
    end_ordinal_exclusive: int | None = None
    role: str | None = None
    ordinals: tuple[int, ...] = ()
    parts: tuple[tuple[str, str | int], ...] = ()


@dataclass(frozen=True)
class SemanticProjection:
    """Total canonical meaning for one exact empirical template contract."""

    contract_id: str
    contract_kind: str
    source_family: str
    template_tokens: tuple[str, ...]
    accounting: str
    category: str
    error_type: str
    tags: tuple[str, ...]
    confidence_by_assignment: tuple[tuple[str, ConfidenceValue], ...]
    primary_locator_ordinal: int | None
    slot_projections: tuple[SlotProjection, ...]
    reference_projections: tuple[ReferenceProjection, ...]

    @property
    def message_template(self) -> str:
        return " ".join(self.template_tokens)

    def confidence_for(self, assignment_level: str) -> ConfidenceValue | None:
        return dict(self.confidence_by_assignment).get(assignment_level)


@dataclass(frozen=True)
class ProjectionCatalog:
    path: Path
    sha256: str
    revision_id: str
    schema_version: int
    model_revision_id: str
    model_sha256: str
    projections: tuple[SemanticProjection, ...]
    _by_contract: Mapping[str, SemanticProjection] = field(
        repr=False, compare=False
    )

    def projection_for(self, contract_id: str) -> SemanticProjection | None:
        return self._by_contract.get(contract_id)


def contract_id_for(source_family: str, template_tokens: tuple[str, ...]) -> str:
    """Return the empirical model's stable source/template identity."""
    material = source_family + "\0" + " ".join(template_tokens)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def composed_contract_id_for(
    source_family: str,
    l1_outer_tokens: tuple[str, ...],
    l2_reason_tokens: tuple[str, ...],
) -> str:
    """Return the classifier's stable identity for one reviewed L1/L2 pair."""
    material = (
        source_family
        + "\0L1\0"
        + " ".join(l1_outer_tokens)
        + "\0L2\0"
        + " ".join(l2_reason_tokens)
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def _mapping(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ProjectionCatalogIntegrityError(f"{field} must be an object")
    return value


def _nonempty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise ProjectionCatalogIntegrityError(f"{field} must be a non-empty string")
    return value


def _string_array(value: Any, field: str, *, allow_empty: bool) -> tuple[str, ...]:
    if not isinstance(value, list) or (not allow_empty and not value):
        qualifier = "a string array" if allow_empty else "a non-empty string array"
        raise ProjectionCatalogIntegrityError(f"{field} must be {qualifier}")
    if not all(isinstance(item, str) and item for item in value):
        raise ProjectionCatalogIntegrityError(f"{field} contains an invalid value")
    return tuple(value)


def _load_slot_projection(raw: Any, field: str) -> SlotProjection:
    item = _mapping(raw, field)
    role = item.get("role")
    ordinal = item.get("ordinal")
    target = item.get("target")
    if role not in _SLOT_ROLES:
        raise ProjectionCatalogIntegrityError(f"{field}.role is invalid")
    if not isinstance(ordinal, int) or isinstance(ordinal, bool) or ordinal < 1:
        raise ProjectionCatalogIntegrityError(f"{field}.ordinal is invalid")
    if target not in _SLOT_TARGETS:
        raise ProjectionCatalogIntegrityError(f"{field}.target is invalid")
    return SlotProjection(role=role, ordinal=ordinal, target=target)


def _positive_integer(value: Any, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ProjectionCatalogIntegrityError(f"{field} is invalid")
    return value


def _load_reference_projection(raw: Any, field: str) -> ReferenceProjection:
    item = _mapping(raw, field)
    capture = item.get("capture")
    target = item.get("target")
    if capture not in _REFERENCE_CAPTURES:
        raise ProjectionCatalogIntegrityError(f"{field}.capture is invalid")
    if target not in _SLOT_TARGETS:
        raise ProjectionCatalogIntegrityError(f"{field}.target is invalid")

    ordinal: int | None = None
    start_ordinal: int | None = None
    end_ordinal: int | None = None
    role: str | None = None
    ordinals: tuple[int, ...] = ()
    parts: tuple[tuple[str, str | int], ...] = ()

    if capture in {"locator", "quoted_argument"}:
        ordinal = _positive_integer(item.get("ordinal"), f"{field}.ordinal")
    elif capture == "template_span":
        start_ordinal = _positive_integer(
            item.get("start_ordinal"), f"{field}.start_ordinal"
        )
        end_ordinal = _positive_integer(
            item.get("end_ordinal_exclusive"),
            f"{field}.end_ordinal_exclusive",
        )
        if end_ordinal <= start_ordinal:
            raise ProjectionCatalogIntegrityError(
                f"{field}.end_ordinal_exclusive must exceed start_ordinal"
            )
    elif capture == "slot":
        role = item.get("role")
        if role not in _SLOT_ROLES:
            raise ProjectionCatalogIntegrityError(f"{field}.role is invalid")
        ordinal = _positive_integer(item.get("ordinal"), f"{field}.ordinal")
    elif capture in {"slot_set", "equivalent_slots"}:
        role = item.get("role")
        if role not in _SLOT_ROLES:
            raise ProjectionCatalogIntegrityError(f"{field}.role is invalid")
        raw_ordinals = item.get("ordinals")
        if not isinstance(raw_ordinals, list) or len(raw_ordinals) < 2:
            raise ProjectionCatalogIntegrityError(
                f"{field}.ordinals must contain at least two ordinals"
            )
        ordinals = tuple(
            _positive_integer(value, f"{field}.ordinals[{index}]")
            for index, value in enumerate(raw_ordinals)
        )
        if len(ordinals) != len(set(ordinals)):
            raise ProjectionCatalogIntegrityError(
                f"{field}.ordinals contains duplicates"
            )
    elif capture == "slot_composition":
        raw_parts = item.get("parts")
        if not isinstance(raw_parts, list) or not raw_parts:
            raise ProjectionCatalogIntegrityError(
                f"{field}.parts must be a non-empty array"
            )
        parsed_parts: list[tuple[str, str | int]] = []
        for index, raw_part in enumerate(raw_parts):
            part_field = f"{field}.parts[{index}]"
            part = _mapping(raw_part, part_field)
            if set(part) == {"literal"}:
                literal = _nonempty_string(part["literal"], f"{part_field}.literal")
                parsed_parts.append(("literal", literal))
                continue
            if set(part) != {"role", "ordinal"} or part["role"] not in _SLOT_ROLES:
                raise ProjectionCatalogIntegrityError(f"{part_field} is invalid")
            parsed_parts.extend(
                (
                    ("role", part["role"]),
                    (
                        "ordinal",
                        _positive_integer(
                            part["ordinal"], f"{part_field}.ordinal"
                        ),
                    ),
                )
            )
        parts = tuple(parsed_parts)

    return ReferenceProjection(
        capture=capture,
        target=target,
        ordinal=ordinal,
        start_ordinal=start_ordinal,
        end_ordinal_exclusive=end_ordinal,
        role=role,
        ordinals=ordinals,
        parts=parts,
    )


def _load_projection(
    raw: Any,
    index: int,
    model_contracts: Mapping[str, ModelCluster],
) -> SemanticProjection:
    field = f"projections[{index}]"
    item = _mapping(raw, field)
    contract_id = _nonempty_string(item.get("contract_id"), f"{field}.contract_id")
    contract_kind = item.get("contract_kind")
    if contract_kind not in _CONTRACT_KINDS:
        raise ProjectionCatalogIntegrityError(f"{field}.contract_kind is invalid")
    source_family = _nonempty_string(
        item.get("source_family"), f"{field}.source_family"
    )
    if contract_kind == "model_full":
        cluster = model_contracts.get(contract_id)
        if cluster is None or cluster.source_family != source_family:
            raise ProjectionCatalogIntegrityError(
                f"{field} does not match an approved model contract"
            )
        template_tokens = cluster.template_tokens
    else:
        l1_outer_tokens = _string_array(
            item.get("l1_outer_tokens"),
            f"{field}.l1_outer_tokens",
            allow_empty=False,
        )
        l2_reason_tokens = _string_array(
            item.get("l2_reason_tokens"),
            f"{field}.l2_reason_tokens",
            allow_empty=False,
        )
        if contract_id != composed_contract_id_for(
            source_family, l1_outer_tokens, l2_reason_tokens
        ):
            raise ProjectionCatalogIntegrityError(
                f"{field}.contract_id does not match its composed L1/L2 contract"
            )
        template_tokens = (*l1_outer_tokens, "[", *l2_reason_tokens, "]")

    accounting = item.get("accounting")
    if accounting not in _ACCOUNTING_VALUES:
        raise ProjectionCatalogIntegrityError(f"{field}.accounting is invalid")
    category = item.get("category")
    if category not in KNOWN_CATEGORIES:
        raise ProjectionCatalogIntegrityError(f"{field}.category is invalid")
    error_type = item.get("error_type")
    if not isinstance(error_type, str) or not _IDENTIFIER_RE.fullmatch(error_type):
        raise ProjectionCatalogIntegrityError(f"{field}.error_type is invalid")
    if accounting == "preserved_unclassified":
        if category != "unclassified" or error_type != "unknown":
            raise ProjectionCatalogIntegrityError(
                f"{field} preserved-unclassified projection is inconsistent"
            )
    elif category == "unclassified":
        raise ProjectionCatalogIntegrityError(
            f"{field} classified projection cannot use the unclassified category"
        )
    tags = _string_array(item.get("tags", []), f"{field}.tags", allow_empty=True)
    if len(tags) != len(set(tags)):
        raise ProjectionCatalogIntegrityError(f"{field}.tags contains duplicates")

    raw_confidence = _mapping(
        item.get("confidence_by_assignment"),
        f"{field}.confidence_by_assignment",
    )
    if not raw_confidence:
        raise ProjectionCatalogIntegrityError(
            f"{field}.confidence_by_assignment must not be empty"
        )
    if not set(raw_confidence).issubset(_ASSIGNMENT_LEVELS):
        raise ProjectionCatalogIntegrityError(
            f"{field}.confidence_by_assignment has an invalid assignment level"
        )
    if not all(value in _CONFIDENCE_VALUES for value in raw_confidence.values()):
        raise ProjectionCatalogIntegrityError(
            f"{field}.confidence_by_assignment has an invalid confidence"
        )
    confidence = tuple(
        (level, raw_confidence[level])
        for level in ("full", "l1_l2", "l1")
        if level in raw_confidence
    )

    locator_ordinal = item.get("primary_locator_ordinal")
    if locator_ordinal is not None and (
        not isinstance(locator_ordinal, int)
        or isinstance(locator_ordinal, bool)
        or locator_ordinal < 1
    ):
        raise ProjectionCatalogIntegrityError(
            f"{field}.primary_locator_ordinal is invalid"
        )

    raw_slots = item.get("slot_projections", [])
    if not isinstance(raw_slots, list):
        raise ProjectionCatalogIntegrityError(
            f"{field}.slot_projections must be an array"
        )
    slots = tuple(
        _load_slot_projection(slot, f"{field}.slot_projections[{slot_index}]")
        for slot_index, slot in enumerate(raw_slots)
    )
    identities = [(slot.role, slot.ordinal, slot.target) for slot in slots]
    if len(identities) != len(set(identities)):
        raise ProjectionCatalogIntegrityError(
            f"{field}.slot_projections contains duplicates"
        )

    raw_references = item.get("reference_projections", [])
    if not isinstance(raw_references, list):
        raise ProjectionCatalogIntegrityError(
            f"{field}.reference_projections must be an array"
        )
    references = tuple(
        _load_reference_projection(
            reference,
            f"{field}.reference_projections[{reference_index}]",
        )
        for reference_index, reference in enumerate(raw_references)
    )
    if len(references) != len(set(references)):
        raise ProjectionCatalogIntegrityError(
            f"{field}.reference_projections contains duplicates"
        )

    return SemanticProjection(
        contract_id=contract_id,
        contract_kind=contract_kind,
        source_family=source_family,
        template_tokens=template_tokens,
        accounting=accounting,
        category=category,
        error_type=error_type,
        tags=tags,
        confidence_by_assignment=confidence,
        primary_locator_ordinal=locator_ordinal,
        slot_projections=slots,
        reference_projections=references,
    )


def load_projection_catalog(
    path: Path | str,
    *,
    expected_sha256: str,
    model: EmpiricalModel,
) -> ProjectionCatalog:
    """Load one exact projection artifact after whole-file hash validation."""
    catalog_path = Path(path)
    payload = catalog_path.read_bytes()
    actual_sha256 = hashlib.sha256(payload).hexdigest()
    if actual_sha256.casefold() != expected_sha256.casefold():
        raise ProjectionCatalogIntegrityError(
            "projection catalog SHA-256 mismatch: "
            f"expected {expected_sha256}, got {actual_sha256}"
        )
    try:
        raw = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProjectionCatalogIntegrityError(
            f"projection catalog is not valid UTF-8 JSON: {exc}"
        ) from exc
    document = _mapping(raw, "catalog")
    if document.get("schema") != PROJECTION_SCHEMA:
        raise ProjectionCatalogIntegrityError("unsupported projection catalog schema")
    if document.get("schema_version") != PROJECTION_SCHEMA_VERSION:
        raise ProjectionCatalogIntegrityError(
            "unsupported projection catalog schema version"
        )

    revision_id = _nonempty_string(document.get("revision_id"), "revision_id")
    model_revision_id = _nonempty_string(
        document.get("model_revision_id"), "model_revision_id"
    )
    model_sha256 = document.get("model_sha256")
    if not isinstance(model_sha256, str) or not _SHA256_RE.fullmatch(
        model_sha256.casefold()
    ):
        raise ProjectionCatalogIntegrityError("model_sha256 is invalid")
    model_sha256 = model_sha256.casefold()
    if model_sha256 != model.sha256.casefold():
        raise ProjectionCatalogIntegrityError(
            "projection catalog model SHA-256 mismatch: "
            f"expected {model.sha256}, got {model_sha256}"
        )
    if model_revision_id != model.revision_id:
        raise ProjectionCatalogIntegrityError(
            "projection catalog model revision mismatch: "
            f"expected {model.revision_id}, got {model_revision_id}"
        )

    raw_projections = document.get("projections")
    if not isinstance(raw_projections, list) or not raw_projections:
        raise ProjectionCatalogIntegrityError(
            "projections must be a non-empty array"
        )
    model_contracts = {cluster.cluster_id: cluster for cluster in model.clusters}
    projections = tuple(
        _load_projection(item, index, model_contracts)
        for index, item in enumerate(raw_projections)
    )
    ids = [projection.contract_id for projection in projections]
    if len(ids) != len(set(ids)):
        raise ProjectionCatalogIntegrityError("projection contract IDs are not unique")
    full_ids = {
        projection.contract_id
        for projection in projections
        if projection.contract_kind == "model_full"
    }
    if full_ids != set(model_contracts):
        missing = len(set(model_contracts) - full_ids)
        unexpected = len(full_ids - set(model_contracts))
        raise ProjectionCatalogIntegrityError(
            "projection catalog does not cover the approved model exactly: "
            f"missing={missing}, unexpected={unexpected}"
        )

    return ProjectionCatalog(
        path=catalog_path,
        sha256=actual_sha256,
        revision_id=revision_id,
        schema_version=PROJECTION_SCHEMA_VERSION,
        model_revision_id=model_revision_id,
        model_sha256=model_sha256,
        projections=projections,
        _by_contract=MappingProxyType(
            {projection.contract_id: projection for projection in projections}
        ),
    )
