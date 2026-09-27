"""Select one pinned native release from source or installed package resources."""
from pathlib import Path
import re
import sys

from .classifier import Classifier
from .model import ModelCompatibilityError, ModelIntegrityError, load_model, read_json


def selected_models_root() -> Path:
    source = Path(__file__).resolve().parents[3] / 'models'
    if source.is_dir():
        return source
    return Path(sys.prefix) / 'share' / 'ck3chronicle' / 'models'


def load_selected_model(*, models_root: Path | None = None):
    root = selected_models_root() if models_root is None else Path(models_root)
    selection = read_json((root / 'selection.json').read_bytes())
    if (selection.get('schema'), selection.get('schema_version')) != (
            'ck3chronicle.native-model-selection', 1):
        raise ModelCompatibilityError('unsupported model selection')
    revision = selection.get('revision_id')
    if (not isinstance(revision, str) or not re.fullmatch(r'[0-9a-f]{24}', revision)
            or selection.get('artifact_directory') != revision):
        raise ModelIntegrityError('invalid selected revision directory')
    digest = selection.get('manifest_sha256')
    if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest):
        raise ModelIntegrityError('selection requires a manifest SHA-256')
    folder = (root / revision).resolve()
    if folder.parent != root.resolve():
        raise ModelIntegrityError('selected release lies outside models root')
    model = load_model(folder, expected_manifest_sha256=digest)
    if model.revision_id != revision:
        raise ModelIntegrityError('loaded revision disagrees with selection')
    return model


def load_selected_classifier(*, models_root: Path | None = None) -> Classifier:
    return Classifier(load_selected_model(models_root=models_root))
