"""Authenticate the package bootstrap; delegate model semantics to its loader."""
import hashlib
import json
from pathlib import Path
import re
import types


class ResourceIntegrityError(ValueError):
    """Selection, manifest or bootstrap bytes disagree."""


class SelectionCompatibilityError(ValueError):
    """The application cannot consume this selection format."""


def read_json(payload):
    def object_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ResourceIntegrityError('duplicate JSON key: ' + key)
            result[key] = value
        return result
    try:
        return json.loads(payload, object_pairs_hook=object_pairs)
    except (ValueError, UnicodeError) as exc:
        raise ResourceIntegrityError(str(exc)) from exc


def load_package(folder: Path, *, expected_manifest_sha256: str):
    """Execute authenticated bootstrap bytes, never an import from the learner."""
    folder = Path(folder).resolve()
    if not isinstance(expected_manifest_sha256, str) or not re.fullmatch(
            r'[0-9a-f]{64}', expected_manifest_sha256):
        raise ResourceIntegrityError('an external manifest SHA-256 is required')
    try:
        payload = (folder / 'manifest.json').read_bytes()
        if hashlib.sha256(payload).hexdigest() != expected_manifest_sha256:
            raise ResourceIntegrityError('manifest SHA-256 mismatch')
        manifest = read_json(payload)
        bootstrap = folder / 'matcher_loader.py'
        code = bootstrap.read_bytes()
        if hashlib.sha256(code).hexdigest() != manifest['hashes']['matcher_loader.py']:
            raise ResourceIntegrityError('bootstrap SHA-256 mismatch')
    except (OSError, KeyError, TypeError) as exc:
        raise ResourceIntegrityError(str(exc)) from exc
    module = types.ModuleType('_ck3_bootstrap_' + expected_manifest_sha256)
    module.__file__ = str(bootstrap)
    exec(compile(code, str(bootstrap), 'exec'), module.__dict__)
    return module.load_package(folder, expected_manifest_sha256=expected_manifest_sha256)
