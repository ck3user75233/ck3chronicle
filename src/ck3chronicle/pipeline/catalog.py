"""Explicit selection for the disconnected empirical pipeline only.

Application selection and installed package resources change at cutover.
Missing or corrupt selected resources fail; no old revision is substituted.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

from .classifier import Classifier
from .model import EmpiricalModel, ModelIntegrityError, load_model
from .normalization import NORMALIZER_REVISION
from .diagnostics import RECOVERY_REVISION

SELECTED_MODEL_REVISION = "43634d23e619ecb4"
SELECTED_MODEL_SHA256 = "791b37be8fd3de65b613d7d34d5dadcdb7acb275cdac5c25d0fa5e50ba25a5b7"
SELECTED_MANIFEST_SHA256 = "b0b755c1f23038f78f26d5ca05d59bf272bef7dd2599845793e63a80eb021b67"


def selected_revision_root() -> Path:
    source = Path(__file__).resolve().parents[3] / "models" / SELECTED_MODEL_REVISION
    if source.is_dir():
        return source
    installed = Path(sys.prefix) / "share" / "ck3chronicle" / "models" / SELECTED_MODEL_REVISION
    if installed.is_dir():
        return installed
    raise FileNotFoundError("selected empirical revision is absent from source and installed resources")


def selected_model_path() -> Path:
    return selected_revision_root() / "empirical_template_model.json"


def load_selected_model() -> EmpiricalModel:
    root = selected_revision_root()
    payload = (root / "manifest.json").read_bytes()
    if hashlib.sha256(payload).hexdigest() != SELECTED_MANIFEST_SHA256:
        raise ModelIntegrityError("selected manifest SHA-256 mismatch")
    manifest = json.loads(payload)
    if (manifest.get("schema") != "ck3chronicle.empirical-model-revision"
            or manifest.get("schema_version") != 1
            or manifest.get("revision_id") != SELECTED_MODEL_REVISION
            or manifest.get("model_sha256") != SELECTED_MODEL_SHA256
            or manifest.get("normalizer_revision") != NORMALIZER_REVISION
            or manifest.get("recovery_revision") != RECOVERY_REVISION):
        raise ModelIntegrityError("selected manifest disagrees with catalog/grammar identities")
    model = load_model(root / "empirical_template_model.json", expected_sha256=SELECTED_MODEL_SHA256)
    if model.revision_id != SELECTED_MODEL_REVISION:
        raise ModelIntegrityError("selected model revision disagrees with catalog")
    return model


def load_selected_classifier() -> Classifier:
    return Classifier(load_selected_model())
