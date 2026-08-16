"""Explicit catalog of reviewed classification model revisions."""

from __future__ import annotations

from pathlib import Path

from .inference import Classifier
from .model import EmpiricalModel, load_model
from .projection_catalog import ProjectionCatalog, load_projection_catalog


APPROVED_MODEL_REVISION = "67303093ecda779d"
APPROVED_MODEL_SHA256 = (
    "0a508eb8056f37d586921bb4441099dcb71fcf89e4a9d1c0e764b1b86d4c1b89"
)
APPROVED_PROJECTION_CATALOG_REVISION = (
    "public-semantic-252-contract-evidence-v3"
)
APPROVED_PROJECTION_CATALOG_SHA256 = (
    "c287849b16447e7b154f067c918afb3e0d30563ce56a9c578b06c006f20032b4"
)


def approved_model_path() -> Path:
    return (
        Path(__file__).resolve().parents[3]
        / "models"
        / APPROVED_MODEL_REVISION
        / "empirical_template_model.json"
    )


def approved_projection_catalog_path() -> Path:
    return (
        Path(__file__).resolve().parents[3]
        / "models"
        / APPROVED_MODEL_REVISION
        / "semantic_projection_catalog.json"
    )


def load_approved_model() -> EmpiricalModel:
    return load_model(approved_model_path(), expected_sha256=APPROVED_MODEL_SHA256)


def load_approved_projection_catalog(
    model: EmpiricalModel | None = None,
) -> ProjectionCatalog:
    approved_model = model or load_approved_model()
    catalog = load_projection_catalog(
        approved_projection_catalog_path(),
        expected_sha256=APPROVED_PROJECTION_CATALOG_SHA256,
        model=approved_model,
    )
    if catalog.revision_id != APPROVED_PROJECTION_CATALOG_REVISION:
        raise ValueError(
            "approved semantic projection catalog revision disagrees with code"
        )
    return catalog


def load_approved_classifier() -> Classifier:
    return Classifier(load_approved_model())


def load_approved_semantic_runtime() -> tuple[Classifier, ProjectionCatalog]:
    model = load_approved_model()
    return Classifier(model), load_approved_projection_catalog(model)
