"""Empirical CK3 error-template classification.

Training remains an offline, reviewed workflow. This package contains only
the deterministic model loader, normalizer, and inference runtime.
"""

from .inference import ClassificationResult, Classifier
from .model import EmpiricalModel, ModelIntegrityError, load_model
from .service import (
    ClassificationError,
    ClassificationPreconditionError,
    ClassificationRunResult,
    classify_session,
)

__all__ = [
    "ClassificationResult",
    "Classifier",
    "EmpiricalModel",
    "ModelIntegrityError",
    "load_model",
    "ClassificationError",
    "ClassificationPreconditionError",
    "ClassificationRunResult",
    "classify_session",
]
