"""One immutable empirical format, with no semantic contract fields.

Revision IDs hash canonical document content excluding revision_id. Cluster IDs
hash source_family and template_tokens. The external SHA-256 pin protects the
exact serialized bytes as well. Literal phrase atoms emitted by infer_slot are
expanded to ordered tokens during offline preparation, never by this reader.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re

from .normalization import NORMALIZER_REVISION, script_system_layers
from .diagnostics import RECOVERY_REVISION

MODEL_SCHEMA = "ck3chronicle.empirical-structures"
MODEL_SCHEMA_VERSION = 1
VARIABLES = frozenset({"<KEY>", "<OPTIONAL_KEY>", "<TYPE>", "<VALUE>",
                       "<PARAM>", "<LOCATOR>"})
_ALT = re.compile(r"<ALT:[a-z]{1,16}(?:\|[a-z]{1,16}){1,3}>")


class ModelIntegrityError(ValueError):
    """Corrupt, unsupported, or unselected empirical content."""


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def content_id(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()[:16]


def cluster_id(source_family: str, template_tokens) -> str:
    return content_id({"source_family": source_family, "template_tokens": list(template_tokens)})


def is_variable(token: str) -> bool:
    return token in VARIABLES or _ALT.fullmatch(token) is not None


@dataclass(frozen=True)
class Layers:
    l1: tuple[str, ...]
    l2: tuple[str, ...]


@dataclass(frozen=True)
class ModelCluster:
    cluster_id: str
    source_family: str
    template_tokens: tuple[str, ...]
    layers: Layers | None
    source_cluster_id: str
    support_occurrences: int
    support_evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class EmpiricalModel:
    path: Path
    sha256: str
    revision_id: str
    normalizer_revision: str
    recovery_revision: str
    clusters: tuple[ModelCluster, ...]


def _object(value, keys, field):
    if not isinstance(value, dict) or set(value) != set(keys.split()):
        raise ModelIntegrityError(f"{field} has unsupported or missing fields")
    return value


def _strings(value, field, *, empty=False):
    if (not isinstance(value, list) or (not value and not empty)
            or any(not isinstance(v, str) or not v for v in value)):
        raise ModelIntegrityError(f"{field} must be a string array")
    return tuple(value)


def _hex(value, length, field):
    if not isinstance(value, str) or re.fullmatch(rf"[0-9a-f]{{{length}}}", value) is None:
        raise ModelIntegrityError(f"{field} must be {length} lowercase hexadecimal characters")
    return value


def _tokens(value, field):
    tokens = _strings(value, field)
    for token in tokens:
        if any(c.isspace() for c in token):
            raise ModelIntegrityError(f"{field} contains an unexpanded literal phrase")
        if token.startswith("<") and token.endswith(">") and not is_variable(token):
            raise ModelIntegrityError(f"{field} contains an unsupported variable: {token}")
        if token.startswith("<ALT:"):
            options = token[5:-1].split("|")
            if options != sorted(set(options)):
                raise ModelIntegrityError(f"{field} alternatives must be sorted and unique")
    return tokens


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ModelIntegrityError(f"duplicate JSON field: {key}")
        result[key] = value
    return result


def load_model(path: Path | str, *, expected_sha256: str) -> EmpiricalModel:
    """Read one current artifact, requiring an explicit byte-integrity pin."""
    _hex(expected_sha256, 64, "expected_sha256")
    path = Path(path)
    payload = path.read_bytes()
    actual = hashlib.sha256(payload).hexdigest()
    if actual != expected_sha256:
        raise ModelIntegrityError("model SHA-256 mismatch")
    try:
        document = json.loads(payload.decode("utf-8"), object_pairs_hook=_unique_object)
    except (UnicodeError, ValueError) as exc:
        raise ModelIntegrityError(f"invalid model JSON: {exc}") from exc
    _object(document, "schema schema_version revision_id normalizer_revision recovery_revision provenance clusters", "model")
    if (document["schema"] != MODEL_SCHEMA or type(document["schema_version"]) is not int
            or document["schema_version"] != MODEL_SCHEMA_VERSION):
        raise ModelIntegrityError("unsupported empirical format")
    if document["normalizer_revision"] != NORMALIZER_REVISION:
        raise ModelIntegrityError("unsupported normalization identity")
    if document["recovery_revision"] != RECOVERY_REVISION:
        raise ModelIntegrityError("unsupported diagnostic recovery identity")
    revision = _hex(document["revision_id"], 16, "revision_id")
    try:
        computed = content_id({k: v for k, v in document.items() if k != "revision_id"})
    except (ValueError, TypeError) as exc:
        raise ModelIntegrityError("invalid canonical content") from exc
    if computed != revision:
        raise ModelIntegrityError("revision ID disagrees with empirical content")
    provenance = _object(document["provenance"],
        "source_revision source_model_sha256 learner_sha256 training_sha256 conversion excluded_source_clusters",
        "provenance")
    _hex(provenance["source_revision"], 16, "source_revision")
    for key in ("source_model_sha256", "learner_sha256"):
        _hex(provenance[key], 64, key)
    training = _strings(provenance["training_sha256"], "training_sha256")
    for value in training:
        _hex(value, 64, "training_sha256")
    if training != tuple(sorted(set(training))):
        raise ModelIntegrityError("training hashes must be sorted and unique")
    _strings(provenance["conversion"], "conversion")
    if not isinstance(provenance["excluded_source_clusters"], list):
        raise ModelIntegrityError("excluded_source_clusters must be an array")
    excluded = set()
    for item in provenance["excluded_source_clusters"]:
        _object(item, "cluster_id reason", "excluded source cluster")
        excluded.add(_hex(item["cluster_id"], 16, "excluded cluster_id"))
        if not isinstance(item["reason"], str) or not item["reason"]:
            raise ModelIntegrityError("excluded cluster reason is missing")
    rows = document["clusters"]
    if not isinstance(rows, list) or not rows:
        raise ModelIntegrityError("clusters must be a nonempty array")
    clusters = []
    ids = set()
    source_ids = set()
    for index, row in enumerate(rows):
        label = f"clusters[{index}]"
        _object(row, "cluster_id source_family template_tokens layers source_cluster_id support_occurrences support_evidence_ids", label)
        source = row["source_family"]
        if not isinstance(source, str) or not source or source.strip() != source:
            raise ModelIntegrityError(f"{label}.source_family is invalid")
        tokens = _tokens(row["template_tokens"], label)
        identity = _hex(row["cluster_id"], 16, label)
        if identity != cluster_id(source, tokens) or identity in ids:
            raise ModelIntegrityError(f"{label} has duplicate or incorrect structural identity")
        ids.add(identity)
        old_id = _hex(row["source_cluster_id"], 16, label)
        if old_id in excluded or old_id in source_ids:
            raise ModelIntegrityError(f"{label} has duplicate or excluded provenance")
        source_ids.add(old_id)
        count = row["support_occurrences"]
        if type(count) is not int or count < 1:
            raise ModelIntegrityError(f"{label} support must be a positive integer")
        evidence = _strings(row["support_evidence_ids"], label)
        if evidence != tuple(sorted(set(evidence))) or not set(evidence) <= set(training):
            raise ModelIntegrityError(f"{label} has invalid evidence references")
        layers = None
        if row["layers"] is not None:
            layer = _object(row["layers"], "l1 l2", label)
            layers = Layers(_tokens(layer["l1"], label), _tokens(layer["l2"], label))
            if script_system_layers(tokens) != (layers.l1, layers.l2) or tokens[-1] != "]":
                raise ModelIntegrityError(f"{label} layers disagree with complete bracketed structure")
        clusters.append(ModelCluster(identity, source, tokens, layers, old_id, count, evidence))
    return EmpiricalModel(path, actual, revision, NORMALIZER_REVISION,
                          RECOVERY_REVISION, tuple(clusters))
