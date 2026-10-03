"""Standalone bootstrap for an immutable matcher/model/parser package.

Only standard-library imports. Verify the externally supplied manifest digest
and every payload before executing any package module. No checkout imports.
"""
import hashlib
import json
from pathlib import Path
import sys
import types

SCHEMA = 'ck3chronicle.native-matcher-package'
API_VERSION = 'ck3-native-matcher-v3'
MODULES = ('full_ids', 'continuations', 'assignment', 'location_sequences', 'matching_primitives',
           'matching_validation', 'native_matching', 'parser')
RUNTIME_FILES = tuple(name + '.py' for name in MODULES if name != 'parser') + ('matcher_loader.py',)
ARTIFACTS = set(RUNTIME_FILES) | {'empirical_template_model.json', 'parser.py',
    'parser-manifest.json', 'owner_rules.json', 'native-validation.json'}


class PackageIntegrityError(ValueError):
    """Selected bytes or mutually pinned identities disagree."""


class PackageCompatibilityError(ValueError):
    """Unsupported package, parser, model or matcher/selector API."""


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(',', ':')).encode()


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise PackageIntegrityError('duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(payload):
    return json.loads(payload, object_pairs_hook=_object)


class LoadedPackage:
    def __init__(self, manifest, manifest_sha256, matcher, parser, api):
        self.manifest = manifest
        self.manifest_sha256 = manifest_sha256
        self.matcher = matcher
        self.parser = parser
        self.api = api

    @property
    def data(self):
        return self.matcher.data

    def parse_file(self, path):
        path = Path(path).resolve()
        return self.parser.parse_bytes(path.read_bytes(), source_name=str(path),
                                       parser_reference=dict(self.manifest['parser']))

    def iter_units(self, raw):
        reference = self.manifest['parser']
        if any(raw.parser_reference.get(k) != reference[k] for k in ('version', 'sha256')):
            raise PackageCompatibilityError('raw parse is not from the package parser')
        return self.api.iter_native_units(raw)

    def match(self, unit, *, inspect=False):
        return self.matcher.match(unit, inspect=inspect)


def load_package(folder, *, expected_manifest_sha256):
    """Execute exactly the bytes authenticated by an external manifest digest."""
    folder = Path(folder).resolve()
    try:
        manifest_bytes = (folder / 'manifest.json').read_bytes()
        if hashlib.sha256(manifest_bytes).hexdigest() != expected_manifest_sha256:
            raise PackageIntegrityError('manifest SHA-256 mismatch')
        manifest = read_json(manifest_bytes)
        if (manifest['schema'], manifest['schema_version'], manifest['matcher_api_version'],
            manifest['model_schema_version'], manifest['selector_version']) != (
                SCHEMA, 1, API_VERSION, 6, 'complete-assignment-v2'):
            raise PackageCompatibilityError('unsupported package compatibility contract')
        if set(manifest['hashes']) != ARTIFACTS:
            raise PackageCompatibilityError('incomplete or unsupported package artifact set')
        package_id = hashlib.sha256(canonical({k: v for k, v in manifest.items()
                                              if k != 'package_id'})).hexdigest()[:24]
        if manifest['package_id'] != package_id:
            raise PackageIntegrityError('package identity disagreement')
        payloads = {}
        for name, digest in manifest['hashes'].items():
            payload = (folder / name).read_bytes()
            if hashlib.sha256(payload).hexdigest() != digest:
                raise PackageIntegrityError('artifact SHA-256 mismatch: ' + name)
            payloads[name] = payload
        # The bootstrap itself is part of the release, not an unpinned helper.
        if Path(__file__).read_bytes() != payloads['matcher_loader.py']:
            raise PackageCompatibilityError('bootstrap differs from the selected package')
        model = read_json(payloads['empirical_template_model.json'])
        revision = hashlib.sha256(canonical({k: v for k, v in model.items()
                                            if k != 'revision_id'})).hexdigest()[:24]
        if revision != model['revision_id'] or revision != manifest['model_revision_id']:
            raise PackageIntegrityError('model revision disagreement')
        reference = read_json(payloads['parser-manifest.json'])
        if (reference != manifest['parser'] or reference != model['parser'] or
            reference['artifact'] != 'parser.py' or reference['sha256'] != manifest['hashes']['parser.py']):
            raise PackageIntegrityError('parser pin disagreement')
        if reference['version'] != 'ck3-lossless-v1.7':
            raise PackageCompatibilityError('unsupported recovery API')
        if read_json(payloads['owner_rules.json']) != model['owner_rules']:
            raise PackageIntegrityError('model declaration disagreement')
        # An empty package search path prevents Python from consulting any
        # learner checkout or unlisted sibling file for executable dependencies.
        namespace = '_ck3_matcher_' + expected_manifest_sha256
        package = types.ModuleType(namespace)
        package.__path__ = []
        sys.modules[namespace] = package
        loaded = {}
        try:
            for name in MODULES:
                qualified = namespace + '.' + name
                module = types.ModuleType(qualified)
                module.__package__ = namespace
                module.__file__ = str(folder / (name + '.py'))
                sys.modules[qualified] = module
                loaded[name] = module
                exec(compile(payloads[name + '.py'], module.__file__, 'exec'), module.__dict__)
                setattr(package, name, module)
            if (loaded['native_matching'].API_VERSION != API_VERSION or
                loaded['assignment'].POLICY_VERSION != manifest['selector_version'] or
                loaded['parser'].VERSION != reference['version']):
                raise PackageCompatibilityError('executable version disagreement')
            matcher = loaded['native_matching'].Matcher(model)
        except BaseException:
            for name in loaded:
                sys.modules.pop(namespace + '.' + name, None)
            sys.modules.pop(namespace, None)
            raise
        return LoadedPackage(manifest, expected_manifest_sha256, matcher,
                             loaded['parser'], loaded['native_matching'])
    except (OSError, json.JSONDecodeError) as exc:
        raise PackageIntegrityError(str(exc)) from exc
    except (KeyError, TypeError) as exc:
        raise PackageCompatibilityError(f'invalid package contract: {exc}') from exc
