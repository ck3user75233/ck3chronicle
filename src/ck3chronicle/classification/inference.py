"""Conservative, deterministic inference against a reviewed empirical model."""

from __future__ import annotations

import difflib
import hashlib
from dataclasses import dataclass
from typing import Sequence

from .contracts import TemplateValidation, validate_template_tokens
from .model import EmpiricalModel, ModelCluster
from .normalize import (
    LOCATOR,
    PUNCTUATION,
    TRUNCATED_REASON,
    diagnostic_lead,
    block_message,
    extract_structured_slots,
    legacy_diagnostic_lead,
    reason_lead,
    semantic_units,
    script_system_layers,
    split_location_evidence,
    tokenize,
)


@dataclass(frozen=True)
class ClassificationResult:
    source_family: str
    assignment_level: str
    contract_id: str | None
    model_revision_id: str
    model_sha256: str
    confidence: float
    semantic_text: str
    location_evidence: str | None
    normalized_tokens: tuple[str, ...]
    l1_template: str | None = None
    l2_template: str | None = None
    structured_slots: tuple[dict[str, object], ...] = ()


def _similarity(left: Sequence[str], right: Sequence[str]) -> float:
    if not left or not right:
        return 0.0
    matcher = difflib.SequenceMatcher(None, left, right, autojunk=False)
    matched = sum(block.size for block in matcher.get_matching_blocks())
    largest = max(len(left), len(right))
    smallest = min(len(left), len(right))
    return (
        0.55 * matched / largest
        + 0.35 * matched / smallest
        + 0.10 * smallest / largest
    )


def _ordered_anchor_overlap(left: Sequence[str], right: Sequence[str]) -> bool:
    left_words = [item.casefold() for item in left if item != LOCATOR and item not in PUNCTUATION]
    right_words = [item.casefold() for item in right if item != LOCATOR and item not in PUNCTUATION]
    if min(len(left_words), len(right_words)) <= 2:
        return bool(set(left_words) & set(right_words))
    return bool(set(zip(left_words, left_words[1:])) & set(zip(right_words, right_words[1:])))


def _composed_id(source: str, outer: Sequence[str], reason: Sequence[str]) -> str:
    material = source + "\0L1\0" + " ".join(outer) + "\0L2\0" + " ".join(reason)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


class Classifier:
    """Assign diagnostics without allowing an uncertain match to become fact."""

    def __init__(self, model: EmpiricalModel) -> None:
        self.model = model
        self._by_source: dict[str, tuple[ModelCluster, ...]] = {}
        for source in {cluster.source_family.casefold() for cluster in model.clusters}:
            self._by_source[source] = tuple(
                cluster
                for cluster in model.clusters
                if cluster.source_family.casefold() == source
            )

    def classify(self, source_family: str, message: str) -> ClassificationResult:
        semantic, location = split_location_evidence(message)
        slots = extract_structured_slots(semantic)
        tokens = tokenize(semantic)
        candidates = self._by_source.get(source_family.casefold(), ())
        leads = {diagnostic_lead(semantic), legacy_diagnostic_lead(semantic)}

        scored: list[tuple[float, ModelCluster, TemplateValidation]] = []
        for cluster in candidates:
            if tuple(item.casefold() for item in cluster.semantic_lead) not in leads:
                continue
            if not _ordered_anchor_overlap(tokens, cluster.medoid_tokens):
                continue
            score = _similarity(tokens, cluster.medoid_tokens)
            if score < self.model.threshold:
                continue
            # Candidate discovery uses empirical similarity, but acceptance is
            # a separate exact contract check. In particular, locator tokens
            # were identified before this point and can never be consumed by
            # a key/value slot.
            validation = validate_template_tokens(tokens, cluster.template_tokens)
            scored.append((score, cluster, validation))
        for score, cluster, validation in sorted(
            scored, key=lambda item: (-item[0], item[1].cluster_id)
        ):
            if not validation.valid:
                continue
            layers = cluster.layers
            validated_slots = tuple(item.as_dict() for item in validation.slots)
            return self._result(
                source_family,
                "full",
                cluster.cluster_id,
                score,
                semantic,
                location,
                tokens,
                layers.l1_template if layers else None,
                layers.l2_template if layers else None,
                slots or validated_slots,
            )

        layered = script_system_layers(tokens)
        if layered is not None:
            outer, reason = layered
            exact_outer = {
                cluster.layers.l1_outer_tokens: cluster.layers
                for cluster in candidates
                if cluster.layers is not None
            }.get(outer)
            if exact_outer is not None:
                if TRUNCATED_REASON in reason:
                    return self._result(
                        source_family,
                        "l1",
                        None,
                        1.0,
                        semantic,
                        location,
                        tokens,
                        " ".join(outer),
                        " ".join(reason),
                        slots,
                    )
                reason_candidates = [
                    (cluster.layers, validation)
                    for cluster in candidates
                    if cluster.layers is not None
                    and reason_lead(cluster.layers.l2_reason_tokens) == reason_lead(reason)
                    and _ordered_anchor_overlap(reason, cluster.layers.l2_reason_tokens)
                    and _similarity(reason, cluster.layers.l2_reason_tokens) >= self.model.threshold
                    and (
                        validation := validate_template_tokens(
                            reason, cluster.layers.l2_reason_tokens
                        )
                    ).valid
                ]
                if reason_candidates:
                    reason_layer, reason_validation = max(
                        reason_candidates,
                        key=lambda item: _similarity(
                            reason, item[0].l2_reason_tokens
                        ),
                    )
                    reason_contract = reason_layer.l2_reason_tokens
                    validated_slots = tuple(
                        item.as_dict() for item in reason_validation.slots
                    )
                    return self._result(
                        source_family,
                        "l1_l2",
                        _composed_id(source_family, outer, reason_contract),
                        min(1.0, _similarity(reason, reason_contract)),
                        semantic,
                        location,
                        tokens,
                        " ".join(outer),
                        " ".join(reason_contract),
                        slots or validated_slots,
                    )
                return self._result(
                    source_family,
                    "l1",
                    None,
                    1.0,
                    semantic,
                    location,
                    tokens,
                    " ".join(outer),
                    " ".join(reason),
                    slots,
                )

        return self._result(
            source_family,
            "unknown",
            None,
            0.0,
            semantic,
            location,
            tokens,
            None,
            None,
            slots,
        )

    def classify_block(
        self, source_family: str, raw_block: str
    ) -> tuple[ClassificationResult, ...]:
        """Classify every semantic occurrence represented by one stored block."""
        message = block_message(raw_block)
        units = semantic_units(source_family, message)
        if len(units) <= 1:
            if not message:
                return ()
            candidate = (
                units[0]
                if units
                and source_family.casefold() == "pdx_persistent_reader.cpp"
                and units[0] != message
                else message
            )
            return (self.classify(source_family, candidate),)
        return tuple(self.classify(source_family, unit) for unit in units)

    def _result(
        self,
        source: str,
        level: str,
        contract_id: str | None,
        confidence: float,
        semantic: str,
        location: str | None,
        tokens: tuple[str, ...],
        l1: str | None,
        l2: str | None,
        slots: tuple[dict[str, object], ...],
    ) -> ClassificationResult:
        return ClassificationResult(
            source_family=source,
            assignment_level=level,
            contract_id=contract_id,
            model_revision_id=self.model.revision_id,
            model_sha256=self.model.sha256,
            confidence=confidence,
            semantic_text=semantic,
            location_evidence=location,
            normalized_tokens=tokens,
            l1_template=l1,
            l2_template=l2,
            structured_slots=slots,
        )
