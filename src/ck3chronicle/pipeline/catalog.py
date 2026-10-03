"""Select one pinned matcher package from source or installed resources."""
from pathlib import Path, PurePosixPath
import re
import sys

from .classifier import Classifier
from .model import (ResourceIntegrityError, SelectionCompatibilityError,
                    load_package, read_json)


def selected_models_root() -> Path:
    source = Path(__file__).resolve().parents[3] / 'models'
    if source.is_dir():
        return source
    return Path(sys.prefix) / 'share' / 'ck3chronicle' / 'models'


def load_selected_package(*, models_root: Path | None = None,
                          selection_path: Path | None = None, package_id: str | None = None):
    """An explicit selection_path permits verification before active selection."""
    root = (selected_models_root() if models_root is None else Path(models_root)).resolve()
    if package_id is not None and selection_path is not None:
        raise SelectionCompatibilityError('select a catalog package or a selection file, not both')
    path = root / 'selection.json' if selection_path is None else Path(selection_path)
    selection = package_selection(package_id, models_root=root) if package_id is not None else read_json(path.read_bytes())
    if not isinstance(selection, dict) or (selection.get('schema'), selection.get('schema_version')) != (
            'ck3chronicle.native-model-selection', 2):
        raise SelectionCompatibilityError('unsupported model selection; schema 2 required')
    for key in ('revision_id', 'package_id'):
        if not isinstance(selection.get(key), str) or not re.fullmatch(r'[0-9a-f]{24}', selection[key]):
            raise ResourceIntegrityError('invalid selection ' + key)
    directory = selection.get('artifact_directory')
    if not isinstance(directory, str) or chr(92) in directory:
        raise ResourceIntegrityError('invalid selected package directory')
    relative = PurePosixPath(directory)
    if relative.is_absolute() or '..' in relative.parts or ':' in directory:
        raise ResourceIntegrityError('selected package must lie within models root')
    folder = (root / directory).resolve()
    if not folder.is_relative_to(root) or folder.name != selection['package_id']:
        raise ResourceIntegrityError('selected package directory disagrees with identity/root')
    package = load_package(folder, expected_manifest_sha256=selection.get('manifest_sha256'))
    for key, manifest_key in (('revision_id', 'model_revision_id'), ('package_id', 'package_id'),
                              ('matcher_api_version', 'matcher_api_version')):
        if selection.get(key) != package.manifest[manifest_key]:
            raise ResourceIntegrityError('loaded package disagrees with selection ' + key)
    return package


def load_selected_classifier(*, models_root: Path | None = None,
                             selection_path: Path | None = None, package_id: str | None = None,
                             cache_size: int = 4096) -> Classifier:
    return Classifier(load_selected_package(models_root=models_root, selection_path=selection_path, package_id=package_id),
                      cache_size=cache_size)


def list_releases(*, models_root: Path | None = None):
    """Includes unavailable historical publications; never infer order from directories."""
    root = selected_models_root() if models_root is None else Path(models_root)
    catalog = read_json((root / 'catalog.json').read_bytes())
    if (catalog.get('schema'), catalog.get('schema_version')) != ('ck3chronicle.model-release-catalog', 1):
        raise SelectionCompatibilityError('unsupported model release catalog')
    rows = catalog['releases']
    identities = [r['release_id'] for r in rows]
    if len(set(identities)) != len(identities):
        raise ResourceIntegrityError('duplicate catalog release identity')
    return rows


def package_selection(package_id, *, models_root: Path | None = None):
    """Resolve an exact executable package, never an implicit package for a model."""
    rows = [r for r in list_releases(models_root=models_root) if r.get('package_id') == package_id]
    if len(rows) != 1 or rows[0]['availability'] != 'available':
        raise SelectionCompatibilityError('model package unavailable: ' + str(package_id))
    row = rows[0]
    return dict(schema='ck3chronicle.native-model-selection', schema_version=2,
        revision_id=row['model_revision_id'], package_id=package_id,
        artifact_directory=row['retained_path'], manifest_sha256=row['manifest_sha256'],
        matcher_api_version=row['matcher_api_version'])


def register_package(source, *, expected_manifest_sha256, models_root,
                     production_order=None, publication_evidence=None):
    """Retain verified existing package bytes; no learning, rewriting or activation."""
    import json
    source, root = Path(source).resolve(), Path(models_root).resolve()
    package = load_package(source, expected_manifest_sha256=expected_manifest_sha256)
    manifest = package.manifest
    if production_order is not None and (type(production_order) is not int or production_order < 1 or not publication_evidence):
        raise ValueError('production registration requires explicit order and publication evidence')
    path = root / 'catalog.json'
    if path.exists():
        rows = list_releases(models_root=root)
    else:
        rows = []
    for row in rows:
        if row.get('production_order') is not None:
            if row.get('model_revision_id') == manifest['model_revision_id'] and row['production_order'] != production_order:
                raise ValueError('publication order of an existing model cannot change')
            if row['production_order'] == production_order and row.get('model_revision_id') != manifest['model_revision_id']:
                raise ValueError('publication order already belongs to another model')
    relative = 'releases/' + manifest['package_id']
    destination = root / relative
    payloads = {n:(source/n).read_bytes() for n in ['manifest.json', *manifest['hashes']]}
    if destination.exists():
        if any(not (destination/n).is_file() or (destination/n).read_bytes()!=data for n,data in payloads.items()):
            raise ResourceIntegrityError('immutable retained package differs')
    else:
        destination.mkdir(parents=True)
        for name,data in payloads.items():
            (destination/name).write_bytes(data)
    row = dict(family='model', release_id=manifest['package_id'], package_id=manifest['package_id'],
        model_revision_id=manifest['model_revision_id'], retained_path=relative,
        manifest_sha256=expected_manifest_sha256, matcher_api_version=manifest['matcher_api_version'],
        parser=manifest['parser'], selector_version=manifest['selector_version'], availability='available',
        publication_status='production' if production_order is not None else 'research',
        production_order=production_order, publication_evidence=publication_evidence)
    prior = next((r for r in rows if r['release_id']==row['release_id']),None)
    if prior is not None and prior != row:
        raise ResourceIntegrityError('existing catalog registration differs')
    if prior is None:
        rows.append(row)
        root.mkdir(parents=True,exist_ok=True)
        temporary=path.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(dict(schema='ck3chronicle.model-release-catalog',schema_version=1,
            retention_floor_distinct_production_models=10,releases=rows),indent=2)+'\n',encoding='utf-8')
        temporary.replace(path)
    return row


def evaluate_package(package_id, log, *, models_root=None):
    """Published-model evaluation uses retained runtime code and public contract preparation."""
    import hashlib
    from collections import Counter
    from .contracts import prepare_record, materialize_definitions, run_lineage
    from .domain import NativeReview
    classifier=load_selected_classifier(models_root=models_root,package_id=package_id,cache_size=0)
    raw=classifier.read_log(log)
    definitions=materialize_definitions(classifier.package)
    counts=Counter()
    records=[]
    for result in classifier.classify_raw(raw):
        if isinstance(result, NativeReview):
            counts['unresolved'] += 1
            records.append(dict(status='unresolved',reason=result.reason,provenance=result.unit['provenance']))
            continue
        if result.selected is None:
            counts['no_match'] += 1
            records.append(dict(status='no_match',reason=result.review_reason,provenance=result.diagnostic.provenance))
            continue
        prepared=prepare_record(definitions[result.selected.template_id],result)
        counts[prepared['match_status']] += 1
        records.append(prepared)
    application_hashes={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
        for name in ('catalog.py','model.py','classifier.py','raw_input.py','bindings.py','contracts.py','domain.py')}
    import json, platform, unicodedata
    application_revision='sha256:'+hashlib.sha256(json.dumps(application_hashes,sort_keys=True).encode()).hexdigest()
    return dict(package_id=package_id, lineage=run_lineage(classifier.package,application_revision=application_revision),
                application_hashes=application_hashes,python=platform.python_version(),unicode=unicodedata.unidata_version,
                input_sha256=hashlib.sha256(Path(log).read_bytes()).hexdigest(),counts=dict(counts),records=records)


def main():
    import argparse
    import json
    p=argparse.ArgumentParser(description='List and select retained model packages; never changes the active default.')
    p.add_argument('--models-root',type=Path)
    commands=p.add_subparsers(dest='command',required=True)
    commands.add_parser('list')
    select=commands.add_parser('selection');select.add_argument('--package',required=True)
    evaluate=commands.add_parser('evaluate');evaluate.add_argument('--package',required=True)
    evaluate.add_argument('--log',type=Path,required=True);evaluate.add_argument('--output',type=Path,required=True)
    register=commands.add_parser('register');register.add_argument('--source',type=Path,required=True)
    register.add_argument('--manifest-sha256',required=True);register.add_argument('--production-order',type=int)
    register.add_argument('--publication-evidence')
    a=p.parse_args()
    if a.command=='list':result=list_releases(models_root=a.models_root)
    elif a.command=='selection':result=package_selection(a.package,models_root=a.models_root)
    elif a.command=='register':result=register_package(a.source,expected_manifest_sha256=a.manifest_sha256,
        models_root=a.models_root or selected_models_root(),production_order=a.production_order,
        publication_evidence=a.publication_evidence)
    else:
        result=evaluate_package(a.package,a.log,models_root=a.models_root)
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        result={k:v for k,v in result.items() if k!='records'}
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
