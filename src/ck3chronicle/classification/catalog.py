"""Explicit catalog of reviewed classification model revisions."""

from __future__ import annotations

from pathlib import Path

from .inference import Classifier
from .model import load_model


APPROVED_MODEL_REVISION = "93196794a7e0115d"
APPROVED_MODEL_SHA256 = (
    "3bd189b4c93ad260e925d1a1ac3ece7c79cc63217480b79a939f6f7f5d034db3"
)


def approved_model_path() -> Path:
    return (
        Path(__file__).resolve().parents[3]
        / "models"
        / APPROVED_MODEL_REVISION
        / "empirical_template_model.json"
    )


def load_approved_classifier() -> Classifier:
    return Classifier(
        load_model(approved_model_path(), expected_sha256=APPROVED_MODEL_SHA256)
    )
