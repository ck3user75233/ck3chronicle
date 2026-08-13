"""Validation and immutable representation of reviewed classifier models."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .normalize import tokenize


MODEL_SCHEMA = "ck3chronicle-empirical-template-calibration"
MODEL_SCHEMA_VERSION = 3
NORMALIZER_VERSION = "ck3-empirical-template-normalizer-v4.6"
CLUSTERER_VERSION = "ordered-token-clusterer-v4-bounded-script-layers"


class ModelIntegrityError(ValueError):
    """The model is corrupt, incompatible, or not the approved artifact."""


@dataclass(frozen=True)
class LayerContracts:
    l1_outer_tokens: tuple[str, ...]
    l2_reason_tokens: tuple[str, ...]

    @property
    def l1_template(self) -> str:
        return " ".join(self.l1_outer_tokens)

    @property
    def l2_template(self) -> str:
        return " ".join(self.l2_reason_tokens)


@dataclass(frozen=True)
class ModelCluster:
    cluster_id: str
    source_family: str
    medoid: str
    medoid_tokens: tuple[str, ...]
    semantic_lead: tuple[str, ...]
    template_tokens: tuple[str, ...]
    layers: LayerContracts | None

    @property
    def template(self) -> str:
        return " ".join(self.template_tokens)


@dataclass(frozen=True)
class EmpiricalModel:
    path: Path
    sha256: str
    revision_id: str
    threshold: float
    clusters: tuple[ModelCluster, ...]


def _require_mapping(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ModelIntegrityError(f"{field} must be an object")
    return value


def _require_strings(value: Any, field: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value or not all(
        isinstance(item, str) and item for item in value
    ):
        raise ModelIntegrityError(f"{field} must be a non-empty string array")
    return tuple(value)


def _expected_cluster_id(source_family: str, template_tokens: tuple[str, ...]) -> str:
    material = source_family + "\0" + " ".join(template_tokens)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def _load_cluster(raw: Any, index: int) -> ModelCluster:
    item = _require_mapping(raw, f"clusters[{index}]")
    source_family = item.get("source_family")
    cluster_id = item.get("cluster_id")
    medoid = item.get("medoid")
    lead = _require_strings(item.get("semantic_lead"), f"clusters[{index}].semantic_lead")
    template_tokens = _require_strings(
        item.get("template_tokens"), f"clusters[{index}].template_tokens"
    )
    if not isinstance(source_family, str) or not source_family:
        raise ModelIntegrityError(f"clusters[{index}].source_family is invalid")
    if not isinstance(cluster_id, str) or len(cluster_id) != 16:
        raise ModelIntegrityError(f"clusters[{index}].cluster_id is invalid")
    if not isinstance(medoid, str) or not medoid:
        raise ModelIntegrityError(f"clusters[{index}].medoid is invalid")
    if cluster_id != _expected_cluster_id(source_family, template_tokens):
        raise ModelIntegrityError(
            f"clusters[{index}].cluster_id does not match its source/template contract"
        )

    layers: LayerContracts | None = None
    raw_layers = item.get("layer_contracts")
    if raw_layers is not None:
        layer_item = _require_mapping(raw_layers, f"clusters[{index}].layer_contracts")
        outer = _require_strings(
            layer_item.get("l1_outer_tokens"),
            f"clusters[{index}].layer_contracts.l1_outer_tokens",
        )
        reason = _require_strings(
            layer_item.get("l2_reason_tokens"),
            f"clusters[{index}].layer_contracts.l2_reason_tokens",
        )
        layers = LayerContracts(outer, reason)

    return ModelCluster(
        cluster_id=cluster_id,
        source_family=source_family,
        medoid=medoid,
        medoid_tokens=tokenize(medoid),
        semantic_lead=lead,
        template_tokens=template_tokens,
        layers=layers,
    )


def load_model(path: Path | str, *, expected_sha256: str) -> EmpiricalModel:
    """Load one exact reviewed model artifact after whole-file hash validation."""
    model_path = Path(path)
    payload = model_path.read_bytes()
    actual_sha256 = hashlib.sha256(payload).hexdigest()
    if actual_sha256.casefold() != expected_sha256.casefold():
        raise ModelIntegrityError(
            f"model SHA-256 mismatch: expected {expected_sha256}, got {actual_sha256}"
        )
    try:
        raw = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ModelIntegrityError(f"model is not valid UTF-8 JSON: {exc}") from exc
    document = _require_mapping(raw, "model")
    if document.get("schema") != MODEL_SCHEMA:
        raise ModelIntegrityError("unsupported model schema")
    if document.get("schema_version") != MODEL_SCHEMA_VERSION:
        raise ModelIntegrityError("unsupported model schema version")

    revision = _require_mapping(document.get("revision"), "revision")
    algorithm = _require_mapping(document.get("algorithm"), "algorithm")
    normalizer = revision.get("normalizer_version", algorithm.get("normalizer_version"))
    clusterer = revision.get("clusterer_version", algorithm.get("clusterer_version"))
    if normalizer != NORMALIZER_VERSION:
        raise ModelIntegrityError("model requires an unsupported normalizer")
    if clusterer != CLUSTERER_VERSION:
        raise ModelIntegrityError("model requires an unsupported clusterer")
    revision_id = revision.get("revision_id")
    if not isinstance(revision_id, str) or not revision_id:
        raise ModelIntegrityError("revision.revision_id is invalid")
    threshold = revision.get("threshold", algorithm.get("cluster_threshold"))
    if not isinstance(threshold, (int, float)) or not 0.0 < float(threshold) <= 1.0:
        raise ModelIntegrityError("model threshold is invalid")

    raw_clusters = document.get("clusters")
    if not isinstance(raw_clusters, list) or not raw_clusters:
        raise ModelIntegrityError("clusters must be a non-empty array")
    clusters = tuple(_load_cluster(item, index) for index, item in enumerate(raw_clusters))
    ids = [cluster.cluster_id for cluster in clusters]
    if len(ids) != len(set(ids)):
        raise ModelIntegrityError("cluster IDs are not unique")
    return EmpiricalModel(
        path=model_path,
        sha256=actual_sha256,
        revision_id=revision_id,
        threshold=float(threshold),
        clusters=clusters,
    )
