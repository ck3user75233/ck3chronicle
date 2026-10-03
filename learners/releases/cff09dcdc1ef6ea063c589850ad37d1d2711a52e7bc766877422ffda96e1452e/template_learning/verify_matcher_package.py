"""Independent native replay; run with -I -S to exclude all installed packages.

Only immutable package code executes. A trusted local baseline made by
verify_shared_matcher supplies pre-extraction results, never matching code.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import importlib.abc
import importlib.util
import json
from pathlib import Path
import pickle
import sys


class NoDevelopmentImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'template_learning', 'ck3chronicle'}:
            raise AssertionError('forbidden development import: ' + fullname)


def canonical(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'))


def strip_addition(value):
    if isinstance(value, dict):
        return {k: strip_addition(v) for k, v in value.items() if k != 'layout_index'}
    if isinstance(value, (tuple, list)):
        return [strip_addition(v) for v in value]
    return value


def key(source, kind, body, contexts, entries):
    def content(region):
        return {k: v for k, v in region.items() if k != 'provenance'}
    return canonical([source, kind, content(body),
                      {k: content(v) for k, v in contexts.items()},
                      [content(e) for e in entries]])


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--package', type=Path, required=True)
    cli.add_argument('--manifest-sha256', required=True)
    cli.add_argument('--baseline', type=Path, required=True)
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args()
    sys.meta_path.insert(0, NoDevelopmentImports())
    spec = importlib.util.spec_from_file_location('standalone_example',
        Path(__file__).with_name('matcher_example.py'))
    example = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(example)
    package = example.load_verified(args.package, args.manifest_sha256)
    baseline = json.loads((args.baseline / 'baseline.json').read_text())
    report = dict(package_id=package.manifest['package_id'],
        manifest_sha256=args.manifest_sha256, dependency_hashes=package.manifest['hashes'],
        counts=Counter(), coverage=Counter(), examples={}, logs=[],
        unavailable=baseline['unavailable'], comparison_differences=[],
        matching_unit='each distinct complete native input per log; every occurrence byte-verified',
        absolute_binding_calls=0, forbidden_development_imports=[])
    templates = {t['template_id']: t for t in package.data['templates']}
    materializations = []
    original_region = package.matcher._region
    def track_region(name, *values, **options):
        materializations.append(name)
        return original_region(name, *values, **options)
    package.matcher._region = track_region
    for item in baseline['logs']:
        with gzip.open(args.baseline / (item['sha256'] + '.pickle.gz'), 'rb') as stream:
            summary, rows, unresolved = pickle.load(stream)
        expected = {}
        for row in rows:
            contexts = next(iter(row['contexts'].values())) if row['contexts'] else {}
            k = key(row['source_family'], row['context_kind'],
                    dict(text=row['native'], pieces=row['pieces']), contexts, row['continuations'])
            assert k not in expected
            expected[k] = row
        raw = package.parse_file(item['path'])
        assert hashlib.sha256(raw.source.data).hexdigest() == item['sha256']
        cursor = 0
        for recovery in raw.iter_recoveries():
            for span in recovery.ordered_spans:
                assert span.start == cursor
                cursor = span.end
        assert cursor == len(raw.source.data)
        seen, outcomes, cache = Counter(), Counter(), {}
        for unit in package.iter_units(raw):
            if unit['recovery_status'] != 'recovered':
                report['counts']['unresolved'] += 1
                continue
            k = key(unit['source_family'], unit['context_kind'], unit['body'],
                    unit['contexts'], unit['continuations'])
            row = expected[k]
            if k not in cache:
                materializations.clear()
                result = package.match(unit, inspect=True)
                assert materializations == ([r['name'] for r in result['assignment']['regions']]
                                             if result['assignment'] else [])
                report['counts']['selected_region_materializations'] += len(materializations)
                assert len(materializations) == len(set(materializations))
                assert result['provenance'] is unit['provenance']
                inspection = result['inspection']
                # Context IDs are caller-owned associations, not layout identity.
                for match in [*inspection['matches'], *inspection['capture_ambiguities']]:
                    if match['context_matches']:
                        match['context_matches'] = {next(iter(row['contexts'])):
                                                  match['context_matches']['native']}
                for name in ('matches', 'capture_ambiguities', 'selected_assignment'):
                    assert strip_addition(inspection[name]) == strip_addition(row[name]), (item['path'], name, row['native'])
                cache[k] = result
                report['counts']['distinct_complete_inputs'] += 1
                if report['counts']['distinct_complete_inputs'] == 1:
                    ordinary = package.match(unit)
                    assert 'inspection' not in ordinary
                    assert ordinary == {k: v for k, v in result.items() if k != 'inspection'}
                    report['ordinary_result_check'] = 'same one selection; no alternatives or absolute bindings'
            else:
                result = cache[k]
            chosen = result['assignment']
            status = chosen['match_status'] if chosen else 'no_match'
            outcomes[status] += 1
            report['counts'][status] += 1
            seen[k] += 1
            categories = {status}
            if chosen:
                selection = chosen['selection']
                report['coverage']['selection:' + selection['reason']] += 1
                if selection['competing_templates'] > 1:
                    categories.add('competing_templates')
                if selection['template_tie'] or selection['capture_tie']:
                    categories.add('tie')
                native_regions = {'body': unit['body'], **unit['contexts'],
                                  **{'continuation:' + str(i): e for i, e in enumerate(unit['continuations'])}}
                assert len(native_regions) == len(chosen['regions'])
                for region in chosen['regions']:
                    native = native_regions[region['name']]
                    start, end = native['provenance']['span']
                    assert raw.source.data[start:end].decode('utf-8', 'surrogateescape') == native['text']
                    report['counts']['selected_regions'] += 1
                    for capture in region['captures']:
                        report['coverage']['slot:' + capture['type']] += 1
                        categories.add(capture['type'])
                        if capture['present']:
                            a, b = capture['span']
                            assert 0 <= a <= b <= end-start
                            assert raw.source.data[start+a:start+b].decode('utf-8', 'surrogateescape') == capture['value']
                            report['counts']['present_captures'] += 1
                            if a == b:
                                categories.add('present_empty')
                                report['coverage']['present_empty'] += 1
                        else:
                            assert capture['span'] is None and capture['value'] is None
                            categories.add('absent')
                            report['counts']['absent_captures'] += 1
                if unit['contexts']:
                    report['coverage']['wrapped'] += 1
                    categories.add('wrapped')
                if unit['continuations']:
                    report['coverage']['continuation_groups'] += 1
                    report['coverage']['continuation_entries'] += len(unit['continuations'])
                    categories.add('entries:' + str(len(unit['continuations'])))
            for category in categories - report['examples'].keys():
                report['examples'][category] = dict(log=item['path'], sha256=item['sha256'],
                    source=unit['source_family'], native=unit['body']['text'],
                    contexts=unit['contexts'], continuations=unit['continuations'],
                    template=templates[chosen['template_id']]['display'] if chosen else None,
                    result={k: v for k, v in result.items() if k != 'inspection'})
        assert seen == Counter({k: len(r['native_occurrences']) for k, r in expected.items()})
        assert outcomes == Counter(template=summary['counts']['full'],
                                   provisional=summary['counts']['provisional'],
                                   no_match=summary['counts']['unknown'])
        report['logs'].append(dict(sha256=item['sha256'], bytes=len(raw.source.data),
                                  distinct_complete_inputs=len(expected), counts=outcomes))
        report['forbidden_development_imports'] = [n for n in sys.modules
            if n.split('.')[0] in {'template_learning', 'ck3chronicle'}]
        assert not report['forbidden_development_imports']
        args.output.write_text(json.dumps(report, indent=2) + '\n')
        print(len(report['logs']), item['sha256'], dict(outcomes), flush=True)


if __name__ == '__main__':
    main()
