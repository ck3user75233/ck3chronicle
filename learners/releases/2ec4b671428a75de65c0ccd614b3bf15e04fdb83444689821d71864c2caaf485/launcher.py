"""Authenticate immutable learner distributions; launch only selected code.

Standard library only. No inference, matching, or ambient learner imports.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import importlib.abc
import importlib.util
import json
from pathlib import Path, PurePosixPath
import platform
import runpy
import subprocess
import sys
import types
import unicodedata
import copy
import uuid

SCHEMA = 'ck3chronicle.learner-release'
FILES = (
    'records.py', 'clustering.py', 'patterns.py', 'regions.py', 'literal_guidance.py',
    'diagnostic_wording.py', 'owner_rules.py', 'owner_rules.json', 'constructions.py',
    'parameter_structures.py', 'full_ids.py', 'artifacts.py', 'inventory.py', 'evidence.py',
    'research_matching.py', 'incremental_template_registry.py', 'learn_error_templates.py',
    'assignment.py', 'selection_evidence.py', 'template_retirement.py', 'continuations.py',
    'matching_primitives.py', 'matching_defaults.py', 'native_matching.py', 'location_sequences.py', 'formatted_literals.py',
    'matching_validation.py', 'matcher_loader.py', 'additive_learning.py',
    'evidence_serialization.py', 'refinement_history.py', 'learner_loader.py', 'publish_native_model.py',
    'evaluate_unseen_session.py', 'release_evaluation.py', 'build_review_pack.py', 'build_visual_review.py',
    'inspect_outer_diagnostics.py', 'review_assignment_changes.py', 'template_review.html',
    'parsers/__init__.py', 'parsers/v1_8/parser.py', 'parsers/v1_8/manifest.json',
    'parsers/v1_8/recovery_rules.json',
)
OPERATIONS = {
    'learn': 'learn_error_templates', 'registry': 'incremental_template_registry',
    'evaluate': 'release_evaluation', 'publish': 'publish_native_model',
    'review': 'build_review_pack', 'visual-review': 'build_visual_review',
    'compare': 'review_assignment_changes',
}
SHARED_FILES = ('ck3chronicle/runtime_logging.py', 'ck3chronicle/journal.py')


class ReleaseError(ValueError):
    """Missing, corrupt, incompatible or unselected learner release."""


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(',', ':')).encode()


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def read_json(payload):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ReleaseError('duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=unique)


def constant(path, name):
    for node in ast.parse(path.read_bytes()).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise ReleaseError('missing source constant: ' + name)


def source_payloads(source, *, application_source):
    """The authoritative authoring-source to retained-payload map."""
    if application_source is None:
        raise ReleaseError('explicit application source is required')
    source, application_source = Path(source), Path(application_source)
    payloads = {'template_learning/' + name: (source / name).read_bytes() for name in FILES}
    payloads['launcher.py'] = Path(__file__).read_bytes()
    for name in ('ck3chronicle/decoder.py', *SHARED_FILES):
        payloads[name] = (application_source / PurePosixPath(name).name).read_bytes()
    return payloads


def _identity_fingerprint(identity):
    values = (identity['version'], identity['implementation_hashes'])
    if 'shared_implementation_hashes' in identity:
        values += (identity['shared_implementation_hashes'],)
    return digest(canonical(values))


def implementation_identity(source=None, *, application_source=None):
    context = sys.modules.get('_ck3_learner_execution')
    if context is not None:
        return copy.deepcopy(context.manifest['learner_identity'])
    payloads = source_payloads(source, application_source=application_source)
    return _mapped_identity(Path(source), payloads)


def _mapped_identity(source, payloads):
    hashes = {name: digest(payloads['template_learning/' + name]) for name in FILES}
    version = constant(source / 'clustering.py', 'CLUSTERER_VERSION')
    identity = dict(version=version, implementation_hashes=hashes,
                    shared_implementation_hashes={name: digest(payloads[name]) for name in SHARED_FILES})
    identity['sha256'] = _identity_fingerprint(identity)
    return identity


def verify_implementation_reference(identity, *, execution_context):
    """Check authenticated identity equality and actual mapped retained disk bytes."""
    if execution_context is None or identity != execution_context.manifest['learner_identity']:
        raise ReleaseError('reference learner identity differs')
    mapped = {'template_learning/' + name: value
              for name, value in identity['implementation_hashes'].items()}
    mapped.update(identity.get('shared_implementation_hashes', {}))
    for name, expected in mapped.items():
        if digest(safe_path(execution_context.folder, name).read_bytes()) != expected:
            raise ReleaseError('reference implementation differs: ' + name)


def safe_path(root, name):
    relative = PurePosixPath(name)
    if not name or '\\' in name or ':' in name or relative.is_absolute() or '..' in relative.parts:
        raise ReleaseError('invalid release path: ' + name)
    path = root / name
    if not path.resolve().is_relative_to(root.resolve()) or path.is_symlink():
        raise ReleaseError('release path escapes retained directory: ' + name)
    return path


def authenticate(folder, expected_manifest_sha256):
    folder = Path(folder).resolve()
    try:
        raw = (folder / 'manifest.json').read_bytes()
        if digest(raw) != expected_manifest_sha256:
            raise ReleaseError('learner manifest SHA-256 mismatch')
        manifest = read_json(raw)
        if (manifest['schema'], manifest['schema_version']) != (SCHEMA, 1):
            raise ReleaseError('unsupported learner release format')
        if sys.version_info < tuple(manifest['python_minimum']):
            raise ReleaseError('unsupported Python platform')
        if manifest['release_id'] != digest(canonical({k:v for k,v in manifest.items() if k != 'release_id'})):
            raise ReleaseError('learner release identity mismatch')
        if not manifest['operations'] or not set(manifest['operations']) <= set(OPERATIONS):
            raise ReleaseError('unsupported learner operation set')
        for op, module in manifest['operations'].items():
            if module != OPERATIONS[op] or 'template_learning/' + module + '.py' not in manifest['hashes']:
                raise ReleaseError('unretained operation: ' + op)
        payloads = {}
        for name, expected in manifest['hashes'].items():
            data = safe_path(folder, name).read_bytes()
            if digest(data) != expected:
                raise ReleaseError('learner payload SHA-256 mismatch: ' + name)
            payloads[name] = data
        if 'launcher.py' not in payloads:
            raise ReleaseError('missing authenticated launcher')
        learner = manifest['learner_identity']
        if learner['sha256'] != _identity_fingerprint(learner):
            raise ReleaseError('learner implementation identity disagreement')
        for name, expected in learner['implementation_hashes'].items():
            if digest(payloads['template_learning/' + name]) != expected:
                raise ReleaseError('learner identity/payload disagreement: ' + name)
        if 'journal_api' in manifest:
            if type(manifest['journal_api']) is not int or manifest['journal_api'] != 1:
                raise ReleaseError('unsupported journal API')
            if set(learner.get('shared_implementation_hashes', {})) != set(SHARED_FILES):
                raise ReleaseError('journal capability requires shared implementation identity')
            if payloads['launcher.py'] != payloads['template_learning/learner_loader.py']:
                raise ReleaseError('journal launcher and loader must be identical')
        elif 'shared_implementation_hashes' in learner:
            raise ReleaseError('shared journal identity requires capability')
        for name, expected in learner.get('shared_implementation_hashes', {}).items():
            if digest(payloads[name]) != expected:
                raise ReleaseError('shared identity/payload disagreement: ' + name)
        parser = manifest['parser']
        parser_directory = {'ck3-lossless-v1.7': 'v1_7', 'ck3-lossless-v1.8': 'v1_8'}[parser['version']]
        parser_root = 'template_learning/parsers/' + parser_directory
        if digest(payloads[parser_root + '/parser.py']) != parser['sha256']:
            raise ReleaseError('learner parser identity mismatch')
        if read_json(payloads[parser_root + '/manifest.json']) != parser:
            raise ReleaseError('learner parser manifest disagreement')
        if parser['version'] == 'ck3-lossless-v1.8' and 'ck3chronicle/decoder.py' not in payloads:
            raise ReleaseError('shared application decoder absent from learner distribution')
        return manifest, payloads
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ReleaseError('incomplete learner release: ' + str(exc)) from exc


def create_release(source, output, *, historical_identity=None, application_source=None):
    """Copy source bytes, never infer or rebuild a model. Historical code is unchanged."""
    source, output = Path(source).resolve(), Path(output).resolve()
    if historical_identity is None:
        payloads = source_payloads(source, application_source=application_source)
        learner = _mapped_identity(source, payloads)
        names = FILES
        operations = OPERATIONS
    else:
        learner = read_json(Path(historical_identity).read_bytes())
        for name, expected in learner['implementation_hashes'].items():
            if digest((source / name).read_bytes()) != expected:
                raise ReleaseError('historical source differs: ' + name)
        # Retain the genuine source copy. Only historical candidate evaluation is
        # supported: no new candidate is created without release provenance.
        names = sorted(p.relative_to(source).as_posix() for p in source.rglob('*')
                       if p.is_file() and p.suffix in {'.py', '.json', '.html'})
        operations = {'evaluate': OPERATIONS['evaluate']}
    if historical_identity is not None:
        payloads = {'template_learning/' + name: (source / name).read_bytes() for name in names}
        # A new distribution envelope, not a claim that these adapters belonged
        # to the historical learner fingerprint. Retained historical files stay byte-identical.
        payloads['template_learning/release_evaluation.py'] = Path(__file__).with_name('release_evaluation.py').read_bytes()
        payloads['launcher.py'] = Path(__file__).read_bytes()
    parser_directory = 'v1_7' if historical_identity else 'v1_8'
    parser = read_json((source / 'parsers' / parser_directory / 'manifest.json').read_bytes())
    manifest = dict(schema=SCHEMA, schema_version=1, learner_identity=learner,
        parser=parser, python_minimum=[3, 11], operations=operations,
        completeness='historical-evaluation-only' if historical_identity else 'complete',
        hashes={name:digest(data) for name,data in sorted(payloads.items())})
    if historical_identity is None:
        manifest['journal_api'] = 1
    manifest['release_id'] = digest(canonical(manifest))
    payloads['manifest.json'] = canonical(manifest) + b'\n'
    folder = output / manifest['release_id']
    if folder.exists():
        if any(not (folder/n).is_file() or (folder/n).read_bytes()!=data for n,data in payloads.items()):
            raise ReleaseError('immutable learner release differs')
    else:
        folder.mkdir(parents=True)
        for name, data in payloads.items():
            path = safe_path(folder, name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    pin = digest(payloads['manifest.json'])
    authenticate(folder, pin)
    return dict(release_id=manifest['release_id'], manifest_sha256=pin,
                folder=str(folder), learner_identity=learner['sha256'], completeness=manifest['completeness'])


def selected_release():
    context = sys.modules.get('_ck3_learner_execution')
    if context is None:
        raise ReleaseError('select an authenticated learner release with learner_loader run')
    return dict(release_id=context.manifest['release_id'], manifest_sha256=context.pin,
                learner_identity=context.manifest['learner_identity']['sha256'])


def require_candidate(model):
    reference = selected_release()
    if model.get('learner_release') != reference:
        raise ReleaseError('candidate requires a different learner release')
    return reference


class RetainedImports(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    """Only authenticated bytes supply project modules; no filesystem fallback."""
    def __init__(self, folder, payloads):
        self.folder, self.payloads = folder, payloads
        self.loaded = {}

    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] not in {'template_learning', 'ck3chronicle'}:
            return None
        stem = fullname.replace('.', '/')
        for name, is_package in ((stem + '/__init__.py', True), (stem + '.py', False)):
            if name in self.payloads:
                return importlib.util.spec_from_loader(fullname, self, origin=str(self.folder/name), is_package=is_package)
        if fullname in {'template_learning', 'ck3chronicle'}:
            return importlib.util.spec_from_loader(fullname, self, origin='<retained namespace>', is_package=True)
        raise ImportError('dependency absent from selected learner release: ' + fullname)

    def create_module(self, spec):
        return None

    def get_code(self, fullname):
        stem = fullname.replace('.', '/')
        name = next((n for n in (stem + '/__init__.py', stem + '.py') if n in self.payloads), None)
        if name is None:
            if fullname in {'template_learning', 'ck3chronicle'}:
                return compile('', '<retained namespace>', 'exec')
            raise ImportError(fullname)
        self.loaded[fullname] = dict(path=name, sha256=digest(self.payloads[name]))
        return compile(self.payloads[name], str(self.folder/name), 'exec')

    def get_filename(self, fullname):
        stem=fullname.replace('.', '/')
        return str(self.folder/next(n for n in (stem+'/__init__.py',stem+'.py') if n in self.payloads))

    def exec_module(self, module):
        if module.__name__ not in {'template_learning', 'ck3chronicle'}:
            module.__file__ = self.get_filename(module.__name__)
        if module.__spec__.submodule_search_locations is not None:
            module.__path__ = []
        exec(self.get_code(module.__name__), module.__dict__)


def _terminal_observation(error):
    if error is None:
        return dict(outcome='success')
    if isinstance(error, SystemExit):
        return dict(outcome='nonzero_exit', exit_code=error.code)
    if isinstance(error, KeyboardInterrupt):
        return dict(outcome='interrupted', exception_class=type(error).__name__)
    return dict(outcome='failed', exception_class=type(error).__name__)


def _journal_options(options, manifest):
    if (manifest.get('journal_api') != 1 or not isinstance(options, dict)
            or type(options.get('api')) is not int or options['api'] != 1):
        raise ReleaseError('invalid journal transport capability')
    if set(options) != {'api', 'destination', 'invocation_id'}:
        raise ReleaseError('invalid journal transport fields')
    invocation_id = options['invocation_id']
    if not isinstance(invocation_id, str) or uuid.UUID(invocation_id).hex != invocation_id:
        raise ReleaseError('invalid journal invocation ID')
    destination = Path(options['destination'])
    if not destination.is_absolute() or destination.name != 'learner-' + invocation_id + '.jsonl':
        raise ReleaseError('invalid journal destination')
    return destination, invocation_id


def execute(folder, pin, operation, arguments, receipt, *, journal_options=None):
    """Private worker entered only in a clean isolated Python process."""
    folder=Path(folder).resolve()
    manifest,payloads=authenticate(folder,pin)
    if Path(__file__).read_bytes()!=payloads['launcher.py']:
        raise ReleaseError('worker launcher differs from selected release')
    if operation not in manifest['operations']:
        raise ReleaseError('operation unavailable in selected learner release: '+operation)
    if manifest.get('journal_api') == 1 and journal_options is None:
        raise ReleaseError('journal-capable worker requires journal transport')
    if any(n=='template_learning' or n.startswith('template_learning.') for n in sys.modules):
        raise ReleaseError('worker already contains learner imports')
    context=types.ModuleType('_ck3_learner_execution')
    context.manifest,context.pin,context.folder=manifest,pin,folder
    sys.modules[context.__name__]=context
    finder=RetainedImports(folder,payloads)
    sys.meta_path.insert(0,finder)
    compiled_sources = {}
    derived_executables = {}
    retained_code = {digest(data):name for name,data in payloads.items() if name.endswith('.py')}
    def audit(event, args):
        if event == 'compile' and isinstance(args[1], str) and args[1].endswith('.py'):
            path = Path(args[1]).resolve()
            if path.is_relative_to(folder):
                relative = path.relative_to(folder).as_posix()
                if relative not in payloads:
                    raise ReleaseError('unlisted executable: ' + relative)
                data = args[0].encode() if isinstance(args[0], str) else args[0]
                if digest(data) != digest(payloads[relative]):
                    raise ReleaseError('compiled bytes differ from retained source: ' + relative)
                compiled_sources[relative] = digest(data)
            elif not path.is_relative_to(Path(sys.base_prefix).resolve()):
                data = args[0].encode() if isinstance(args[0], str) else args[0]
                selected_source = retained_code.get(digest(data))
                if operation != 'publish' or selected_source is None:
                    raise ReleaseError('executable outside selected release/platform: ' + str(path))
                # Publication verifies its new runtime distribution. Its code
                # must be byte-identical to authenticated retained source.
                derived_executables[str(path)] = dict(source=selected_source,sha256=digest(data))
    sys.addaudithook(audit)
    backend = handler = logger = log_context = None
    journal_path = invocation_id = None
    if journal_options is not None:
        journal_path, invocation_id = _journal_options(journal_options, manifest)
        from ck3chronicle import runtime_logging as backend
        from ck3chronicle import journal  # Import authenticated adapter under audit too.
        handler = backend.configure_runtime_logging(destination=journal_path)
        logger = backend.get_logger('learner')
    result = 'failed'
    pending = receipt_error = None
    receipt_written = False
    observed = dict(outcome='unavailable')
    try:
        if handler is not None:
            log_context = backend.log_context(invocation_id=invocation_id, release_id=manifest['release_id'])
            log_context.__enter__()
            print('Learner journal: ' + str(journal_path), file=sys.stderr)
            backend.event(logger, 'invocation_started', operation=operation,
                          manifest_sha256=pin, learner_identity=manifest['learner_identity']['sha256'],
                          parser=manifest['parser'], journal_path=str(journal_path))
        try:
            # Direct parser loads must also select retained bytes. Core fresh commands
            # accept this manifest path, never an ambient checkout parser.
            parser_directory = {'ck3-lossless-v1.7': 'v1_7', 'ck3-lossless-v1.8': 'v1_8'}[manifest['parser']['version']]
            parser_path=folder/'template_learning/parsers'/parser_directory/'manifest.json'
            if operation in {'learn','registry'} and (operation=='learn' or any(a in {'sync','build'} for a in arguments)):
                if '--parser-manifest' in arguments:
                    index=arguments.index('--parser-manifest')
                    if Path(arguments[index+1]).resolve()!=parser_path:
                        raise ReleaseError('parser must come from selected learner release')
                else:
                    arguments=[*arguments,'--parser-manifest',str(parser_path)]
            if manifest['completeness']=='historical-evaluation-only':
                if '--bundle' not in arguments:
                    raise ReleaseError('historical evaluation requires an explicit candidate')
                bundle=Path(arguments[arguments.index('--bundle')+1])
                model=read_json((bundle/'empirical_template_model.json').read_bytes())
                if model['algorithm'].get('learner_identity')!=manifest['learner_identity']:
                    raise ReleaseError('historical candidate belongs to another learner')
            sys.argv=[manifest['operations'][operation],*arguments]
            try:
                runpy.run_module('template_learning.'+manifest['operations'][operation],run_name='__main__')
            except SystemExit as exc:
                if exc.code not in (None,0):raise
            result = 'completed'
            observed = _terminal_observation(None)
        except BaseException as error:
            pending = error
            observed = _terminal_observation(error)
            raise
        finally:
            try:
                if receipt:
                    detail = dict(status=result,operation=operation,release_id=manifest['release_id'],
                        manifest_sha256=pin,learner_identity=manifest['learner_identity']['sha256'],parser=manifest['parser'],
                        python=platform.python_version(),python_implementation=platform.python_implementation(),
                        unicode_version=unicodedata.unidata_version,modules=finder.loaded,
                        compiled_sources=compiled_sources,rule_hashes={n:h for n,h in manifest['hashes'].items() if n.endswith('.json')},
                        derived_executables=derived_executables,arguments=arguments)
                    if handler is not None:
                        detail.update(invocation_id=invocation_id, journal_path=str(journal_path),
                                      rotation=dict(max_bytes=handler.maxBytes, backup_count=handler.backupCount),
                                      terminal_observation=observed, receipt_written=True)
                    path=Path(receipt);path.parent.mkdir(parents=True,exist_ok=True)
                    path.write_bytes(canonical(detail)+b'\n')
                    receipt_written = True
            except BaseException as error:
                receipt_error = error
                if pending is None:
                    raise
            finally:
                if handler is not None:
                    boundary_error = pending if pending is not None else receipt_error
                    terminal = observed if pending is not None or receipt_error is None else _terminal_observation(receipt_error)
                    trace = ((type(boundary_error), boundary_error, boundary_error.__traceback__)
                             if boundary_error is not None and not isinstance(boundary_error, (SystemExit, KeyboardInterrupt)) else False)
                    backend.event(logger, 'invocation_finished', **terminal, dispatch_outcome=observed['outcome'],
                                  receipt_requested=bool(receipt), receipt_written=receipt_written,
                                  receipt_error=type(receipt_error).__name__ if receipt_error is not None else None,
                                  exc_info=trace)
                    del boundary_error, trace
    finally:
        # Cleanup is observational, including while a dispatch/receipt exception
        # is pending. It cannot replace the already observed execution outcome.
        try:
            if log_context is not None:
                log_context.__exit__(None, None, None)
        except BaseException:
            pass
        try:
            if handler is not None:
                backend.close_runtime_logging(handler)
        except BaseException:
            pass
        pending = receipt_error = None


def launch(folder, pin, operation, arguments, *, receipt=None, log_dir=None):
    manifest,_=authenticate(folder,pin)
    if operation not in manifest['operations']:
        raise ReleaseError('operation unavailable: '+operation)
    prefix = [sys.executable,'-I','-S','-B',str(Path(folder).resolve()/'launcher.py')]
    if manifest.get('journal_api') == 1:
        resolved_receipt = str(Path(receipt).expanduser().resolve()) if receipt else ''
        directory = (Path(log_dir).expanduser().resolve() if log_dir is not None else
                     Path(resolved_receipt).parent/'learner-logs' if receipt else
                     Path.cwd()/'.ck3chronicle/wip/learner-logs')
        invocation_id = uuid.uuid4().hex
        options = dict(api=1, destination=str(directory/('learner-'+invocation_id+'.jsonl')),
                       invocation_id=invocation_id)
        command = [*prefix, '_execute_journal_v1', str(Path(folder).resolve()), pin, operation,
                   resolved_receipt, canonical(options).decode(), *arguments]
    else:
        if log_dir is not None:
            raise ReleaseError('selected release does not support --log-dir')
        command = [*prefix, '_execute', str(Path(folder).resolve()), pin, operation, receipt or '', *arguments]
    return subprocess.run(command, check=True)


def catalog_root():
    root=Path(__file__).resolve().parents[2]/'learners'
    return root if root.is_dir() else Path(sys.prefix)/'share/ck3chronicle/learners'


def resolve_release(root, release_id):
    root=Path(root)
    catalog=read_json((root/'catalog.json').read_bytes())
    if (catalog.get('schema'),catalog.get('schema_version')) != ('ck3chronicle.learner-release-catalog',1):
        raise ReleaseError('unsupported learner release catalog')
    rows=[r for r in catalog['releases'] if r['release_id']==release_id]
    if len(rows)!=1 or rows[0]['availability'] not in {'available','partial'}:
        raise ReleaseError('learner release unavailable: '+release_id)
    row=rows[0]
    folder=safe_path(root,row['retained_path'])
    manifest,_=authenticate(folder,row['manifest_sha256'])
    if manifest['release_id']!=release_id:
        raise ReleaseError('catalog learner identity disagreement')
    return folder,row['manifest_sha256']


def register_release(source, pin, root, *, production_order=None, publication_evidence=None):
    """Register retained bytes. Publication order is an explicit decision, never activation order."""
    source,root=Path(source).resolve(),Path(root).resolve()
    manifest,payloads=authenticate(source,pin)
    if production_order is not None and (type(production_order) is not int or production_order<1 or not publication_evidence):
        raise ReleaseError('production registration requires order and evidence')
    path=root/'catalog.json'
    catalog=read_json(path.read_bytes()) if path.exists() else dict(
        schema='ck3chronicle.learner-release-catalog',schema_version=1,
        retention_floor_production_learners=10,releases=[])
    if (catalog.get('schema'),catalog.get('schema_version')) != ('ck3chronicle.learner-release-catalog',1):
        raise ReleaseError('unsupported learner release catalog')
    for old in catalog['releases']:
        if production_order is not None and old.get('production_order')==production_order and old.get('learner_identity')!=manifest['learner_identity']['sha256']:
            raise ReleaseError('production order already belongs to another learner')
        if old.get('learner_identity')==manifest['learner_identity']['sha256'] and old.get('production_order')!=production_order:
            raise ReleaseError('existing learner publication order cannot change')
    relative='releases/'+manifest['release_id']
    destination=root/relative
    payloads={**payloads,'manifest.json':(source/'manifest.json').read_bytes()}
    if destination.exists():
        if any(not (destination/n).is_file() or (destination/n).read_bytes()!=data for n,data in payloads.items()):
            raise ReleaseError('immutable registered learner differs')
    else:
        destination.mkdir(parents=True)
        for name,data in payloads.items():
            target=safe_path(destination,name);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    row=dict(family='learner',release_id=manifest['release_id'],learner_identity=manifest['learner_identity']['sha256'],
        learner_version=manifest['learner_identity']['version'],retained_path=relative,manifest_sha256=pin,
        availability='available' if manifest['completeness']=='complete' else 'partial',
        operations=list(manifest['operations']),publication_status='production' if production_order is not None else 'research',
        production_order=production_order,publication_evidence=publication_evidence)
    prior=next((r for r in catalog['releases'] if r['release_id']==row['release_id']),None)
    if prior is not None and prior!=row:raise ReleaseError('existing learner registration differs')
    if prior is None:
        catalog['releases'].append(row)
        root.mkdir(parents=True,exist_ok=True)
        temporary=path.with_suffix('.json.tmp');temporary.write_bytes(canonical(catalog)+b'\n');temporary.replace(path)
    return row


def main():
    if len(sys.argv)>1 and sys.argv[1]=='_execute_journal_v1':
        execute(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[7:],sys.argv[5] or None,
                journal_options=read_json(sys.argv[6]))
        return
    if len(sys.argv)>1 and sys.argv[1]=='_execute':
        execute(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[6:],sys.argv[5] or None)
        return
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    create=sub.add_parser('create');create.add_argument('--source',type=Path,required=True)
    create.add_argument('--output',type=Path,required=True);create.add_argument('--historical-identity',type=Path)
    create.add_argument('--application-source',type=Path,help='Explicit application source directory providing decoder and shared logging.')
    listing=sub.add_parser('list');listing.add_argument('--root',type=Path,default=catalog_root())
    register=sub.add_parser('register');register.add_argument('--root',type=Path,default=catalog_root())
    register.add_argument('--source',type=Path,required=True);register.add_argument('--manifest-sha256',required=True)
    register.add_argument('--production-order',type=int);register.add_argument('--publication-evidence')
    run=sub.add_parser('run');run.add_argument('--root',type=Path,default=catalog_root())
    run.add_argument('--release',required=True);run.add_argument('--receipt')
    run.add_argument('--log-dir',type=Path)
    for command in (create, listing, register):
        command.add_argument('--log-dir',type=Path)
    run.add_argument('operation',choices=OPERATIONS);run.add_argument('arguments',nargs=argparse.REMAINDER)
    a=p.parse_args()
    if a.command in {'create', 'list', 'register'}:
        from ck3chronicle import runtime_logging as backend
        invocation_id = uuid.uuid4().hex
        directory = (a.log_dir.expanduser().resolve() if a.log_dir is not None else
                     Path.cwd()/'.ck3chronicle/wip/learner-logs')
        destination = backend.invocation_log_path(directory, 'learner-admin', invocation_id)
        handler = backend.configure_runtime_logging(destination=destination)
        logger = backend.get_logger('learner-admin')
        try:
            print('Learner journal: ' + str(destination), file=sys.stderr)
            with backend.log_context(invocation_id=invocation_id):
                backend.event(logger, 'invocation_started', operation=a.command,
                              source_file=__file__, journal_path=str(destination),
                              source_identity='mutable source; no immutable application identity supplied')
                try:
                    if a.command=='create':
                        print(json.dumps(create_release(a.source,a.output,historical_identity=a.historical_identity,application_source=a.application_source),indent=2))
                    elif a.command=='list':print((a.root/'catalog.json').read_text())
                    else:print(json.dumps(register_release(a.source,a.manifest_sha256,a.root,
                        production_order=a.production_order,publication_evidence=a.publication_evidence),indent=2))
                except BaseException as error:
                    backend.event(logger, 'invocation_finished', **_terminal_observation(error),
                                  exc_info=not isinstance(error, (SystemExit, KeyboardInterrupt)))
                    raise
                else:
                    backend.event(logger, 'invocation_finished', outcome='success')
        finally:
            try:
                backend.close_runtime_logging(handler)
            except BaseException:
                pass
    else:
        args=a.arguments[1:] if a.arguments[:1]==['--'] else a.arguments
        # Convenience defaults belong to the outer application command only.
        if a.operation=='registry' and ('--state-root' not in args or ('sync' in args and '--runtime-root' not in args)):
            from ck3chronicle import config
            folder,pin=resolve_release(a.root,a.release)
            if '--state-root' not in args:args=['--state-root',str(config.ROOT_LEARNER_STATE/a.release),*args]
            if 'sync' in args and '--runtime-root' not in args:args += ['--runtime-root',str(config.ROOT_CK3CHRONICLE)]
        folder,pin=resolve_release(a.root,a.release)
        launch(folder,pin,a.operation,args,receipt=a.receipt,log_dir=a.log_dir)


if __name__=='__main__':
    main()
