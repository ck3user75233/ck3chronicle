"""Compare disposable candidates on exact genuine records read through the handler.

Reconstruct native regions from stored definitions/values, never fabricate logs.
Use each package's public matcher and the pipeline's rendering/identity contract.
"""
import argparse
from collections import Counter
import hashlib
import html
import json
from pathlib import Path

from ck3chronicle.pipeline.contracts import render_regions, identity_digest, materialize_definitions
from ck3chronicle.pipeline.contracts import prepare_record
from ck3chronicle.pipeline.classifier import Classifier
from ck3chronicle.pipeline.domain import NativeReview
from template_learning.location_candidate_experiment import save, sha
from template_learning.matcher_example import load_verified


def region(parser, text):
    raw = text.encode('utf-8', 'surrogateescape')
    source = parser.Source('stored-native-region', raw)
    return dict(text=text, pieces=[(p.kind, p.text) for p in parser.lexical_pieces(source, parser.Span(0, len(raw)))])


def stored_unit(package, row):
    rendered = dict(render_regions(row['definition'], row['values']))
    regions = {name: region(package.parser, text) for name, text in rendered.items()}
    entries = []
    for value_region in row['values']['regions']:
        if value_region['component_index'] is None:
            continue
        name = value_region['name']
        entry = regions[name]
        source = next(r for r in row['provenance']['regions'] if r['name'] == name)
        reference, value = [[a-source['span'][0], b-source['span'][0]] for a,b in source['binding_spans']]
        native = entry['text'].encode('utf-8', 'surrogateescape')
        middle = native[reference[1]:value[0]]
        assert b'title:' in middle
        entry.update(prefix_span=reference, value_span=value,
            label_span=[reference[1]+middle.index(b'title:'), value[0]])
        entries.append(entry)
    return dict(parser=package.manifest['parser'], recovery_status='recovered',
        source_family=row['source_family'], source_tag=row['provenance']['source_tag'],
        context_kind=row['definition']['context_kind'], body=regions['body'],
        contexts={n:regions[n] for n in ('prefix','suffix') if n in regions},
        continuations=entries, provenance=row['provenance'])


def prepared(package, result, definitions):
    assignment = result['assignment']
    if assignment is None:
        return None
    values = dict(contract_version='error-contract-v1', template_id=assignment['template_id'], regions=[
        dict(name=r['name'], layout=r['layout'], component_index=r.get('component_index'),
             bindings=[{k:b[k] for k in ('slot_id','type','value','present')} for b in r['captures']])
        for r in assignment['regions']])
    rendered = render_regions(definitions[assignment['template_id']], values)
    return dict(status=assignment['match_status'], values=values, rendered=rendered,
                identity=identity_digest(values))


def captures(prep, kind=None):
    if prep is None:
        return None
    return [(r['name'], b['type'], b['value'], b['present'])
            for r in prep['values']['regions'] for b in r['bindings'] if kind is None or b['type']==kind]


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--root', type=Path, required=True)
    cli.add_argument('--experiment', type=Path, required=True)
    cli.add_argument('--baseline', type=Path, required=True)
    cli.add_argument('--baseline-pin', required=True)
    cli.add_argument('--baseline-label', default='v46')
    cli.add_argument('--regression-evidence',type=Path)
    args = cli.parse_args()
    root, out = args.root.resolve(), args.experiment.resolve()
    manifest_path, = (out/'packages').glob('*/manifest.json')
    packages = dict(baseline=load_verified(args.baseline, args.baseline_pin),
                    candidate=load_verified(manifest_path.parent, sha(manifest_path)))
    definitions = {k:materialize_definitions(p) for k,p in packages.items()}
    assert packages['baseline'].manifest['parser'] == packages['candidate'].manifest['parser']
    report = dict(scope='All stored diagnostics from an unchanged genuine database backup, via public handler reads. No ingestion or production activation.',
        candidate_package=packages['candidate'].manifest['package_id'],
        candidate_pin=sha(manifest_path), baseline_package=packages['baseline'].manifest['package_id'],
        totals=Counter(), transitions=Counter(), runs=[], changes=[], failures=[], targets=[],
        status_downgrades=[], remaining_unmatched=[], assignment_changes=[], regression_checks=[])
    report['baseline_label']=args.baseline_label
    regressions = {}
    if args.regression_evidence:
        prior=json.loads(args.regression_evidence.read_text())
        regressions={(r['run_id'],r['ordinal']):r for r in prior['status_downgrades']}
    changed_pairs={}
    report['training_summary'] = packages['candidate'].data['summary']
    report['export_validation'] = json.loads((manifest_path.parent/'native-validation.json').read_text())
    cache = {}
    locator_only_pairs = {}
    evidence = json.loads((out/'stored-evidence.json').read_text())
    for run in evidence['runs']:
        document = json.loads((out/(run['run_id']+'.json')).read_text())
        counts = {k:Counter() for k in packages}
        identities = {}
        for row in document['records']:
            unit = stored_unit(packages['candidate'], row)
            text_key = (row['source_family'], unit['context_kind'], tuple(render_regions(row['definition'],row['values'])))
            key = hashlib.sha256(repr(text_key).encode('utf-8','surrogateescape')).hexdigest()
            if key not in cache:
                results = {label:prepared(p, p.match(unit), definitions[label]) for label,p in packages.items()}
                for label, prep in results.items():
                    if prep is not None:
                        assert prep['rendered'] == list(text_key[2]), (label, row['run_id'], row['ordinal'])
                cache[key] = results
            results = cache[key]
            before, after = results['baseline'], results['candidate']
            n = row['occurrence_count']
            report['totals']['stored_records'] += 1
            report['totals']['occurrences'] += n
            for label, prep in results.items():
                counts[label][prep['status'] if prep else 'no_match'] += n
            transition = (before['status'] if before else 'no_match') + ' -> ' + (after['status'] if after else 'no_match')
            report['transitions'][transition] += n
            if (row['run_id'],row['ordinal']) in regressions:
                passed=bool(after and after['status']=='template' and any(
                    v[1]=='KEY' and v[2] in {'add_title_law','activate_struggle_catalyst'} for v in captures(after)))
                report['regression_checks'].append(dict(run_id=row['run_id'],ordinal=row['ordinal'],passed=passed,
                    occurrences=n,text=unit['body']['text'],assignment=after))
                if not passed:
                    report['failures'].append(dict(run_id=row['run_id'],ordinal=row['ordinal'],reason='effect-name KEY regression remains'))
            old_id=before['values']['template_id'] if before else None
            new_id=after['values']['template_id'] if after else None
            if old_id!=new_id or transition not in {'template -> template','provisional -> provisional','no_match -> no_match'}:
                pair=(old_id,new_id,transition)
                change=changed_pairs.setdefault(pair,dict(before=old_id,after=new_id,transition=transition,occurrences=0,records=0,
                    source_family=row['source_family'],run_id=row['run_id'],ordinal=row['ordinal'],text=unit['body']['text']))
                change['occurrences']+=n
                change['records']+=1
            if transition == 'template -> provisional':
                detail = {label:p.match(unit) for label,p in packages.items()}
                report['status_downgrades'].append(dict(run_id=row['run_id'],ordinal=row['ordinal'],
                    occurrences=n, text=unit['body']['text'], results=detail))
            if after is None:
                report['remaining_unmatched'].append(dict(run_id=row['run_id'],ordinal=row['ordinal'],
                    occurrences=n,source_family=row['source_family'],text=unit['body']['text']))
            if before is not None and after is None:
                report['failures'].append(dict(run_id=row['run_id'], ordinal=row['ordinal'], reason='lost complete match'))
            if after:
                existing = identities.setdefault(after['identity'], key)
                assert existing == key, 'different native messages collapsed to one identity'
                report['totals']['reconstructed_occurrences'] += n
                unknowns = sum(b[2]=='Unknown' for b in captures(after,'LOCATOR'))
                report['totals']['unknown_locator_occurrences'] += unknowns*n
                layout_key = repr([(r['name'],r['layout']) for r in after['values']['regions']])
                other_values = tuple(v for v in captures(after) if v[1]!='LOCATOR')
                comparison_key = (after['values']['template_id'],layout_key,other_values)
                witness = dict(run_id=row['run_id'],ordinal=row['ordinal'],identity=after['identity'],locators=captures(after,'LOCATOR'))
                prior = locator_only_pairs.setdefault(comparison_key,witness)
                if prior['locators']!=witness['locators']:
                    assert prior['identity']!=witness['identity']
                    report.setdefault('locator_only_identity_witness',[prior,witness])
            if before and after and captures(before) != captures(after):
                report['totals']['changed_capture_records'] += 1
                report['totals']['changed_capture_occurrences'] += n
                old_locations = captures(before, 'LOCATOR')
                new_locations = captures(after, 'LOCATOR')
                if new_locations != old_locations and [v for v in new_locations if v[2]!='Unknown'] != old_locations:
                    report['failures'].append(dict(run_id=row['run_id'], ordinal=row['ordinal'], reason='existing locator captures changed'))
                if len(report['changes']) < 12:
                    report['changes'].append(dict(run_id=row['run_id'], ordinal=row['ordinal'],
                        text=dict(text_key[2])['body'], before=captures(before), after=captures(after)))
        report['runs'].append(dict(run_id=run['run_id'], counts=counts,
            in_training=run['log_sha256'] in evidence['training_hashes']))
        print(run['run_id'], json.dumps(counts), flush=True)
    report['totals']['distinct_native_units'] = len(cache)
    report['assignment_changes']=list(changed_pairs.values())
    assert len(report['regression_checks'])==len(regressions)
    # The original three were in native review, not stored assigned diagnostics.
    original = next(r for r in evidence['runs'] if r['run_id']=='20261003-IS3QON')
    package = packages['candidate']
    raw = package.parse_file(original['input']['snapshot'])
    wanted = {4019,56914,57093}
    pipeline_counts = Counter()
    for classified in Classifier(package).classify_raw(raw):
        if isinstance(classified,NativeReview):
            pipeline_counts['unresolved'] += 1
            continue
        unit = classified.diagnostic.unit
        if classified.selected is None:
            pipeline_counts['no_match'] += 1
            native_record = None
        else:
            native_record = prepare_record(definitions['candidate'][classified.selected.template_id], classified)
            pipeline_counts[native_record['match_status']] += 1
        if wanted.intersection(unit['provenance']['emission_ordinals']):
            result = package.match(unit)
            prep = prepared(package,result,definitions['candidate'])
            report['targets'].append(dict(provenance=unit['provenance'],text=unit['body']['text'],
                assignment=prep, pipeline_record=native_record,
                template=package.matcher.by_id[result['assignment']['template_id']]['display'] if prep else None))
    report['original_run_pipeline_counts']=pipeline_counts
    assert len(report['targets']) == 3
    model = package.data
    parts = [part for t in model['templates'] for p in [t,*[v for rows in t['context_patterns'].values() for v in rows]] for part in p['parts']]
    repeated_parts = [p for p in parts if p['kind']=='repeat']
    parts.extend(p for repeated in repeated_parts for layout in repeated['layouts'] for p in layout)
    locator_parts = [p for p in parts if p.get('type')=='LOCATOR']
    assert not any(p['constraints'].get('numeric_text') or p['constraints'].get('line_reference') for p in locator_parts)
    report['locator_slots_without_numeric_gate'] = len(locator_parts)
    report['repeated_location_definitions'] = len(repeated_parts)
    # Exercise real 1/2/3-entry witnesses without synthesizing new messages.
    examples = json.loads((root/'.codex-tmp/location-variability-review/recovery-examples.json').read_text())
    witnesses = []
    for example in examples['examples']:
        if not example['label'].startswith('scope mismatch'):
            continue
        text = example['recovered_messages'][0]['text']
        unit = dict(parser=package.manifest['parser'],source_family='jomini_script_system.cpp',
            source_tag='jomini_script_system.cpp:303', context_kind='body', body=region(package.parser,text),
            contexts={},continuations=[])
        result = package.match(unit)
        prep = prepared(package,result,definitions['candidate'])
        assert prep is not None
        witnesses.append(dict(label=example['label'],template_id=prep['values']['template_id'],
            status=prep['status'],locators=captures(prep,'LOCATOR'),identity=prep['identity'],
            layout=prep['values']['regions'][0]['layout']))
    assert len(witnesses)==3 and len({w['template_id'] for w in witnesses})==1
    assert [len(w['locators']) for w in witnesses]==[2,4,6]
    assert len({w['identity'] for w in witnesses})==3
    report['variable_count_witnesses']=witnesses
    continuation_checks = []
    for example in examples['examples']:
        if example['label'] not in {'existing wrapper split','existing attached continuation list'}:
            continue
        parent = example['original_emissions'][0]
        native = package.parse_file(parent['source'])
        units = [u for u in package.iter_units(native)
                 if parent['ordinal'] in u['provenance']['emission_ordinals']]
        assert len(units)==len(example['recovered_messages'])
        for unit in units:
            results = {label:prepared(p,p.match(unit),definitions[label]) for label,p in packages.items()}
            assert results['baseline'] and results['candidate']
            assert captures(results['baseline'])==captures(results['candidate'])
        continuation_checks.append(dict(label=example['label'],messages=len(units),
            attached_entries=sum(len(u['continuations']) for u in units),captures_preserved=True))
    assert len(continuation_checks)==2
    report['continuation_checks']=continuation_checks
    report['database_unchanged'] = sha(Path(evidence['database'])) == evidence['database_sha256']
    report['training_inputs_unchanged'] = all(sha(Path(row['snapshot']))==row['sha256']
        for row in json.loads((out/'inputs.json').read_text()))
    before_hashes = json.loads((out/'production-before.json').read_text())
    report['production_unchanged'] = all(sha(root/name)==value for name,value in before_hashes.items())
    assert report['database_unchanged'] and report['production_unchanged'] and report['training_inputs_unchanged']
    report['limitations'] = ['Repeated locations apply to complete trailing Script location and Stack trace sections; other recovery structures remain unchanged.',
        'Parser numeric recovery checks are unchanged; no genuine nonnumeric near-line example exists in the examined corpus.',
        f"The candidate training set contains {len(evidence['training_hashes'])} logs; original Run in training: {original['log_sha256'] in evidence['training_hashes']}. Target checks do not establish general accuracy.",
        'The other stored Runs test coverage on ingested evidence outside that training set; absence of a baseline match is reported explicitly.']
    save(out/'verification.json', report)
    esc = lambda value: html.escape(str(value))
    bits = ['<!doctype html><meta charset="utf-8"><title>Disposable locator candidate test</title>',
        '<style>body{font:16px/1.5 system-ui;max-width:1100px;margin:36px auto;padding:0 24px}table{border-collapse:collapse;width:100%}td,th{padding:9px;border-bottom:1px solid #ccc;text-align:left}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f5f7;padding:14px}</style>',
        '<h1>Disposable locator candidate: genuine ingested data</h1>',
        '<p><a href="CHANGES.html">Human-readable template changes and previously unmatched examples</a></p>',
        '<p>Candidate '+esc(report['candidate_package'])+'. Production selection and the database backup are unchanged.</p>',
        '<p>This experiment tests marker/Unknown recognition, removes numeric-only LOCATOR constraints, and learns repeated trailing location entries independently of their count. '
        'The parser and message boundaries are unchanged. All inputs are genuine stored records or protected captures.</p>',
        '<h2>Fresh build and export</h2><pre>'+esc(json.dumps(report['training_summary'],indent=2))+'</pre>',
        '<p>Export replay checks every training assignment and capture against the candidate. See the complete evidence for the export validation receipt.</p>',
        '<h2>Stored-data comparison with the same-20-log '+esc(args.baseline_label)+' candidate</h2><pre>'+esc(json.dumps(report['totals'],indent=2))+'</pre>',
        '<p>All selected assignments reconstruct their complete native regions. Distinct native messages were checked against candidate identity keys for accidental merging.</p>',
        '<pre>'+esc(json.dumps(report['transitions'],indent=2))+'</pre>',
        '<p>Failed checks: '+str(len(report['failures']))+'. Candidate LOCATOR slots without numeric gates: '+str(report['locator_slots_without_numeric_gate'])+'.</p>',
        '<table><tr><th>Run</th><th>In training</th><th>'+esc(args.baseline_label)+' baseline</th><th>Candidate</th></tr>']
    for row in report['runs']:
        bits.append('<tr><td>'+esc(row['run_id'])+'</td><td>'+str(row['in_training'])+'</td><td>'+esc(dict(row['counts']['baseline']))+'</td><td>'+esc(dict(row['counts']['candidate']))+'</td></tr>')
    bits.append('</table><h2>Native changes</h2>')
    bits.append('<p>Template-to-provisional changes: '+str(sum(r['occurrences'] for r in report['status_downgrades']))+
                ' occurrences. Complete assignment details and all remaining unmatched records are included in verification.json.</p>')
    bits.append('<h2>One template, distinct exact messages</h2><pre>'+esc(json.dumps(witnesses,indent=2))+'</pre>')
    for change in report['changes']:
        bits.append('<details><summary>'+esc(change['run_id'])+' record '+str(change['ordinal'])+'</summary><pre>'+esc(change['text'])+'</pre><pre>'+esc(json.dumps({k:change[k] for k in ('before','after')},indent=2))+'</pre></details>')
    bits.append('<h2>Original three review diagnostics</h2>')
    for target in report['targets']:
        bits.append('<p>'+esc(target['assignment']['status'] if target['assignment'] else 'no_match')+'</p><pre>'+esc(target['template'])+'</pre>')
    bits.append('<h2>Limits</h2><ul>'+''.join('<li>'+esc(t)+'</li>' for t in report['limitations'])+'</ul>')
    if report['failures']:
        bits.append('<h2>Failures requiring review</h2><pre>'+esc(json.dumps(report['failures'],indent=2))+'</pre>')
    bits.append('<p><a href="verification.json">Complete verification evidence</a> · <a href="stored-evidence.json">Stored Run/input membership</a> · <a href="learn-execution.json">Build execution receipt</a></p>')
    (out/'RESULTS.html').write_text('\n'.join(bits),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k in ('totals','transitions','failures','production_unchanged','database_unchanged')},indent=2),flush=True)


if __name__ == '__main__':
    main()
