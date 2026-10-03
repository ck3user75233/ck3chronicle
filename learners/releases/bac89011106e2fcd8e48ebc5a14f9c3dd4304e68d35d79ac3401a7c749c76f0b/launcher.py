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

SCHEMA = 'ck3chronicle.learner-release'
FILES = (
    'records.py', 'clustering.py', 'patterns.py', 'regions.py', 'literal_guidance.py',
    'diagnostic_wording.py', 'owner_rules.py', 'owner_rules.json', 'constructions.py',
    'parameter_structures.py', 'full_ids.py', 'artifacts.py', 'inventory.py', 'evidence.py',
    'research_matching.py', 'incremental_template_registry.py', 'learn_error_templates.py',
    'assignment.py', 'selection_evidence.py', 'template_retirement.py', 'continuations.py',
    'matching_primitives.py', 'matching_defaults.py', 'native_matching.py',
    'matching_validation.py', 'matcher_loader.py', 'additive_learning.py',
    'evidence_serialization.py', 'learner_loader.py', 'publish_native_model.py',
    'evaluate_unseen_session.py', 'release_evaluation.py', 'build_review_pack.py', 'build_visual_review.py',
    'inspect_outer_diagnostics.py', 'review_assignment_changes.py', 'template_review.html',
    'parsers/__init__.py', 'parsers/v1_7/parser.py', 'parsers/v1_7/manifest.json',
    'parsers/v1_7/recovery_rules.json',
)
OPERATIONS = {
    'learn': 'learn_error_templates', 'registry': 'incremental_template_registry',
    'evaluate': 'release_evaluation', 'publish': 'publish_native_model',
    'review': 'build_review_pack', 'visual-review': 'build_visual_review',
    'compare': 'review_assignment_changes',
}


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


def implementation_identity(source):
    source = Path(source)
    hashes = {name: digest((source / name).read_bytes()) for name in FILES}
    version = constant(source / 'clustering.py', 'CLUSTERER_VERSION')
    return dict(version=version, implementation_hashes=hashes,
                sha256=digest(canonical((version, hashes))))


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
        if learner['sha256'] != digest(canonical((learner['version'], learner['implementation_hashes']))):
            raise ReleaseError('learner implementation identity disagreement')
        for name, expected in learner['implementation_hashes'].items():
            if digest(payloads['template_learning/' + name]) != expected:
                raise ReleaseError('learner identity/payload disagreement: ' + name)
        parser = manifest['parser']
        if digest(payloads['template_learning/parsers/v1_7/parser.py']) != parser['sha256']:
            raise ReleaseError('learner parser identity mismatch')
        if read_json(payloads['template_learning/parsers/v1_7/manifest.json']) != parser:
            raise ReleaseError('learner parser manifest disagreement')
        return manifest, payloads
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ReleaseError('incomplete learner release: ' + str(exc)) from exc


def create_release(source, output, *, historical_identity=None):
    """Copy source bytes, never infer or rebuild a model. Historical code is unchanged."""
    source, output = Path(source).resolve(), Path(output).resolve()
    if historical_identity is None:
        learner = implementation_identity(source)
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
    payloads = {'template_learning/' + name: (source / name).read_bytes() for name in names}
    if historical_identity is not None:
        # A new distribution envelope, not a claim that these adapters belonged
        # to the historical learner fingerprint. Retained historical files stay byte-identical.
        payloads['template_learning/release_evaluation.py'] = Path(__file__).with_name('release_evaluation.py').read_bytes()
    payloads['launcher.py'] = Path(__file__).read_bytes()
    parser = read_json((source / 'parsers/v1_7/manifest.json').read_bytes())
    manifest = dict(schema=SCHEMA, schema_version=1, learner_identity=learner,
        parser=parser, python_minimum=[3, 11], operations=operations,
        completeness='historical-evaluation-only' if historical_identity else 'complete',
        hashes={name:digest(data) for name,data in sorted(payloads.items())})
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
        if fullname.split('.')[0] == 'ck3chronicle':
            raise ImportError('application imports unavailable in a learner release')
        if fullname.split('.')[0] != 'template_learning':
            return None
        stem = fullname.replace('.', '/')
        for name, is_package in ((stem + '/__init__.py', True), (stem + '.py', False)):
            if name in self.payloads:
                return importlib.util.spec_from_loader(fullname, self, origin=str(self.folder/name), is_package=is_package)
        if fullname == 'template_learning':
            return importlib.util.spec_from_loader(fullname, self, origin='<retained namespace>', is_package=True)
        raise ImportError('dependency absent from selected learner release: ' + fullname)

    def create_module(self, spec):
        return None

    def get_code(self, fullname):
        stem = fullname.replace('.', '/')
        name = next((n for n in (stem + '/__init__.py', stem + '.py') if n in self.payloads), None)
        if name is None:
            if fullname == 'template_learning':
                return compile('', '<retained namespace>', 'exec')
            raise ImportError(fullname)
        self.loaded[fullname] = dict(path=name, sha256=digest(self.payloads[name]))
        return compile(self.payloads[name], str(self.folder/name), 'exec')

    def get_filename(self, fullname):
        stem=fullname.replace('.', '/')
        return str(self.folder/next(n for n in (stem+'/__init__.py',stem+'.py') if n in self.payloads))

    def exec_module(self, module):
        if module.__name__ != 'template_learning':
            module.__file__ = self.get_filename(module.__name__)
        if module.__spec__.submodule_search_locations is not None:
            module.__path__ = []
        exec(self.get_code(module.__name__), module.__dict__)


def execute(folder, pin, operation, arguments, receipt):
    """Private worker entered only in a clean isolated Python process."""
    folder=Path(folder).resolve()
    manifest,payloads=authenticate(folder,pin)
    if Path(__file__).read_bytes()!=payloads['launcher.py']:
        raise ReleaseError('worker launcher differs from selected release')
    if operation not in manifest['operations']:
        raise ReleaseError('operation unavailable in selected learner release: '+operation)
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
    # Direct parser loads must also select retained bytes. Core fresh commands
    # accept this manifest path, never an ambient checkout parser.
    parser_path=folder/'template_learning/parsers/v1_7/manifest.json'
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
    result='failed'
    try:
        try:
            runpy.run_module('template_learning.'+manifest['operations'][operation],run_name='__main__')
        except SystemExit as exc:
            if exc.code not in (None,0):raise
        result='completed'
    finally:
        if receipt:
            path=Path(receipt);path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(canonical(dict(status=result,operation=operation,release_id=manifest['release_id'],
                manifest_sha256=pin,learner_identity=manifest['learner_identity']['sha256'],parser=manifest['parser'],
                python=platform.python_version(),python_implementation=platform.python_implementation(),
                unicode_version=unicodedata.unidata_version,modules=finder.loaded,
                compiled_sources=compiled_sources,rule_hashes={n:h for n,h in manifest['hashes'].items() if n.endswith('.json')},
                derived_executables=derived_executables,
                arguments=arguments))+b'\n')


def launch(folder, pin, operation, arguments, *, receipt=None):
    manifest,_=authenticate(folder,pin)
    if operation not in manifest['operations']:
        raise ReleaseError('operation unavailable: '+operation)
    return subprocess.run([sys.executable,'-I','-S','-B',str(Path(folder).resolve()/'launcher.py'),
        '_execute',str(Path(folder).resolve()),pin,operation,receipt or '',*arguments],check=True)


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
    if len(sys.argv)>1 and sys.argv[1]=='_execute':
        execute(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[6:],sys.argv[5] or None)
        return
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    create=sub.add_parser('create');create.add_argument('--source',type=Path,required=True)
    create.add_argument('--output',type=Path,required=True);create.add_argument('--historical-identity',type=Path)
    listing=sub.add_parser('list');listing.add_argument('--root',type=Path,default=catalog_root())
    register=sub.add_parser('register');register.add_argument('--root',type=Path,default=catalog_root())
    register.add_argument('--source',type=Path,required=True);register.add_argument('--manifest-sha256',required=True)
    register.add_argument('--production-order',type=int);register.add_argument('--publication-evidence')
    run=sub.add_parser('run');run.add_argument('--root',type=Path,default=catalog_root())
    run.add_argument('--release',required=True);run.add_argument('--receipt')
    run.add_argument('operation',choices=OPERATIONS);run.add_argument('arguments',nargs=argparse.REMAINDER)
    a=p.parse_args()
    if a.command=='create':
        print(json.dumps(create_release(a.source,a.output,historical_identity=a.historical_identity),indent=2))
    elif a.command=='list':print((a.root/'catalog.json').read_text())
    elif a.command=='register':print(json.dumps(register_release(a.source,a.manifest_sha256,a.root,
        production_order=a.production_order,publication_evidence=a.publication_evidence),indent=2))
    else:
        args=a.arguments[1:] if a.arguments[:1]==['--'] else a.arguments
        # Convenience defaults belong to the outer application command only.
        if a.operation=='registry' and ('--state-root' not in args or ('sync' in args and '--runtime-root' not in args)):
            from ck3chronicle import config
            folder,pin=resolve_release(a.root,a.release)
            if '--state-root' not in args:args=['--state-root',str(config.ROOT_LEARNER_STATE/a.release),*args]
            if 'sync' in args and '--runtime-root' not in args:args += ['--runtime-root',str(config.ROOT_CK3CHRONICLE)]
        folder,pin=resolve_release(a.root,a.release)
        launch(folder,pin,a.operation,args,receipt=a.receipt)


if __name__=='__main__':
    main()
