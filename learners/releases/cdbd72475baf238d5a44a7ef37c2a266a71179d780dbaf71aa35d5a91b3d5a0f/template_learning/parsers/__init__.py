"""Explicit loading of self-contained, versioned raw-parser artifacts.

Only the selected source artifact is executed. It depends on the Python standard
library, never on the learner, a model, application configuration, or SQL.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import sys
import types
from urllib.parse import urlparse
from urllib.request import url2pathname


def iter_recoveries(raw):
    """Dispatch the two published APIs without changing the selected parser.

    v1.6 intentionally retains its per-emission behavior for existing model pins.
    v1.7 consumers must use the artifact's complete-log stream.
    """
    version = raw.parser_reference['version']
    if version == 'ck3-lossless-v1.6':
        return (emission.recovery for emission in raw.emissions)
    if version == 'ck3-lossless-v1.7':
        return raw.iter_recoveries()
    raise ValueError(f'unsupported recovery API for selected parser: {version}')


@dataclass(frozen=True)
class ParserReference:
    version: str
    artifact: str
    sha256: str

    def to_dict(self) -> dict:
        return dict(version=self.version, artifact=self.artifact, sha256=self.sha256)

    @classmethod
    def from_dict(cls, value: dict) -> ParserReference:
        if set(value) != {"version", "artifact", "sha256"}:
            raise ValueError("parser reference requires version, artifact and sha256")
        return cls(**value)


def reference_from_manifest(path: Path | str) -> ParserReference:
    path = Path(path).resolve()
    value = json.loads(path.read_text(encoding="utf-8"))
    reference = ParserReference.from_dict(value)
    artifact = (path.parent / reference.artifact).resolve()
    return ParserReference(reference.version, artifact.as_uri(), reference.sha256)


@dataclass(frozen=True)
class SelectedParser:
    reference: ParserReference
    implementation: types.ModuleType

    def parse_file(self, path: Path | str):
        path = Path(path)
        return self.parse_bytes(path.read_bytes(), source_name=str(path.resolve()))

    def parse_bytes(self, data: bytes, *, source_name: str):
        return self.implementation.parse_bytes(
            data, source_name=source_name, parser_reference=self.reference.to_dict())

    def load_debug(self, path: Path | str):
        return self.implementation.load_debug(Path(path), self.reference.to_dict())


def load_parser(reference: ParserReference) -> SelectedParser:
    """Resolve a supplied local artifact, verify it, then execute those bytes.

    A published artifact can be copied to another machine with a new local URI;
    its version and implementation digest remain the same. No version fallback.
    """
    uri = urlparse(reference.artifact)
    if uri.scheme != "file" or uri.netloc:
        raise ValueError("parser artifact must be an explicit local file URI")
    path = Path(url2pathname(uri.path))
    payload = path.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != reference.sha256:
        raise ValueError("selected parser implementation SHA-256 mismatch")
    name = "_ck3_raw_parser_" + digest
    module = sys.modules.get(name)
    if module is None:
        module = types.ModuleType(name)
        module.__file__ = str(path)
        sys.modules[name] = module
        try:
            exec(compile(payload, str(path), "exec"), module.__dict__)
        except BaseException:
            del sys.modules[name]
            raise
    if module.VERSION != reference.version:
        raise ValueError("selected parser version disagrees with its implementation")
    return SelectedParser(reference, module)
