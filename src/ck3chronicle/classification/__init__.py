"""Empirical CK3 error-template classification.

Training remains an offline, reviewed workflow. This package contains only
the deterministic model loader, normalizer, and inference runtime.
"""

from .inference import ClassificationResult, Classifier
from .model import EmpiricalModel, ModelIntegrityError, load_model

__all__ = [
    "ClassificationResult",
    "Classifier",
    "EmpiricalModel",
    "ModelIntegrityError",
    "load_model",
]
