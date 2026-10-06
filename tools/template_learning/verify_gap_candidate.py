"""Verify implemented owner fields, native captures and residuals in a frozen candidate."""
import argparse
from collections import Counter,defaultdict
import json
from pathlib import Path
from template_learning.evidence_serialization import native_evidence_rows,write_json
from template_learning.audit_key_bindings import hits
from template_learning.inventory import sha256_file
from template_learning.matcher_example import load_verified
from ck3chronicle.pipeline.classifier import Classifier
from ck3chronicle.pipeline.contracts import materialize_definitions, prepare_record
from ck3chronicle.pipeline.domain import NativeReview


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--bundle',type=Path,required=True)
    cli.add_argument('--package',type=Path,required=True)
    cli.add_argument('--preflight',type=Path,required=True)
    cli.add_argument('--output',type=Path,required=True)
    cli.add_argument('--review-shard',type=Path,required=True,help='Original three-message IS3QON review shard; read only.')
    args=cli.parse_args()
    expected=json.loads(args.preflight.read_bytes());by_id={r['example_id']:r for r in expected['records']}
    model=json.loads((args.package/'empirical_template_model.json').read_bytes());templates={t['template_id']:t for t in model['templates']}
    required={
        'comparison_types':'comparison were of different types (<PARAM>)',
        'invalid_comparison':"Invalid <KEY> side during comparison '<KEY>'",
        'trigger_failures':'<KEY> trigger [ <REASON>',
        'unset_event_target':"Event target link '<KEY>' returned an unset scope",
        'untyped_trigger':'untyped trigger [ <REASON>',
        'invalid_province':'Invalid province',
        'history_after_death':"has history after death birth, won't execute.",
        'history_before_birth':"has history from before birth, won't execute.",
        'scope_mismatch':"Expected '<KEY>', but got '<KEY>'",
        'compare_expected_scope':"compare trigger '<KEY>': none, expected <KEY>",
        'previous_holders':"No previous holders for '<PARAM>'",
        'formatting_tag':"Unknown formatting tag '<PARAM>'",
    }
    owner_patterns={name:[t['template_id'] for t in templates.values() if snippet in t['display']] for name,snippet in required.items()}
    owner_patterns['history_phrase']=owner_patterns['history_after_death']+owner_patterns['history_before_birth']
    owner_patterns['emblem_category']=[t['template_id'] for t in templates.values() if 'emblem texture ' in t['display']]
    owner_patterns['flag_variable']=[t['template_id'] for t in templates.values() if 'is used but is never set.' in t['display']]
    owner_patterns['unknown_effect_trigger']=[t['template_id'] for t in templates.values() if t['source_family']=='pdx_persistent_reader.cpp' and t['display'].lstrip().startswith(('Unknown effect:', 'Unknown trigger:'))]
    rule_types={r['id']:r.get('slot_type','PARAM') for r in model['parameter_structures']} if 'parameter_structures' in model else {}
    # Runtime declarations retain the same owner rules in the model.
    if not rule_types:rule_types={r['id']:r.get('slot_type','PARAM') for r in model['owner_rules']['parameter_structures']}
    counts=Counter();occs=Counter();field_ids=defaultdict(set);seen=set();failures=[];examples=defaultdict(list);outcomes=Counter();ties=[];grammar=[];keyvalues=Counter();unknown=Counter();selected_templates=Counter();residual_messages=Counter();residual_occurrences=Counter()
    for row,n in native_evidence_rows(args.bundle/'native_evidence.json'):
        selected=row.get('selected_assignment');outcomes[selected['match_status'] if selected else 'no_match']+=n
        if selected:
            selected_templates[selected['template_id']]+=n
            flagged=any(c.get('type') in ('KEY','OPTIONAL_KEY') and c.get('value') and hits(c['value']) for c in selected['captures'])
            if flagged:
                if row['source_family']=='jomini_effect_impl.cpp' and 'Starting travel with incorrect receiver' in row['native']:
                    category='Format-constrained date (May is a month)'
                elif row['source_family'] in ('character.cpp','characterhistory.cpp'):
                    assert 'already has the trait ' in row['native'] or 'Failed to find any valid flavorization' in row['native']
                    category='Trait / display markup spelling coincidence'
                else:
                    category='Identifier, function/property name, type or reported offending token'
                residual_messages[category]+=1;residual_occurrences[category]+=n
            data=row['native'].encode('utf-8','surrogateescape')
            for c in selected['captures']:
                if c.get('span') is not None:
                    a,b=c['span'];assert data[a:b].decode('utf-8','surrogateescape')==c['value']
                if c['type'] in ('KEY','OPTIONAL_KEY') and c.get('value'):
                    for hit in hits(c['value']):keyvalues[hit['word']]+=1
                    if c['value'] in ("hasn't",'been','the') and row['source_family']=='characterhistory.cpp':grammar.append(dict(text=row['native'],capture=c))
            if selected.get('selection',{}).get('template_tie'):ties.append(dict(text=row['native'],occurrences=n,selection=selected['selection'],template_id=selected['template_id']))
            if row['source_family']=='pdx_persistent_reader.cpp' and row['native'].lstrip().startswith(('Unknown effect:','Unknown trigger:')):
                pattern=templates[selected['template_id']]['display'];assert pattern.lstrip().startswith(('Unknown effect:','Unknown trigger:'))
                unknown[pattern.split(':',1)[0].strip()]+=n
        if row['example_id'] not in by_id:continue
        seen.add(row['example_id']);witness=by_id[row['example_id']]
        assert (witness['native'],witness['occurrences'])==(row['native'],n)
        if not selected:
            failures.append(dict(example_id=row['example_id'],reason='no complete assignment',text=row['native']));continue
        template=templates[selected['template_id']];parts={p['name']:p for p in template['parts'] if p['kind']=='slot'}
        captured=defaultdict(list)
        for c in selected['captures']:
            part=parts.get(c['name'],{});definition=part.get('constraints',{}).get('parameter_structure',{}).get('definition')
            if definition:
                assert c['type']==rule_types[definition]
                captured[definition].append(c['value'])
        for definition,values in witness['fields'].items():
            if captured[definition]!=values:
                failures.append(dict(example_id=row['example_id'],definition=definition,expected=values,actual=captured[definition],text=row['native']))
            else:
                counts[definition]+=len(values);occs[definition]+=n*len(values);field_ids[definition].add(selected['template_id'])
                if len(examples[definition])<3 and not any(e['values']==values for e in examples[definition]):examples[definition].append(dict(values=values,text=row['native'],template_id=selected['template_id'],status=selected['match_status'],provenance=row['native_occurrences'][:1]))
    assert seen==set(by_id)
    package=load_verified(args.package,sha256_file(args.package/'manifest.json'))
    definitions=materialize_definitions(package);targets=[]
    original_hash=sha256_file(args.review_shard)
    for classified in Classifier(package).classify_raw(package.parse_file(args.review_shard)):
        assert not isinstance(classified,NativeReview) and classified.selected is not None
        record=prepare_record(definitions[classified.selected.template_id],classified)
        assert record['match_status']=='template'
        targets.append(dict(text=classified.diagnostic.unit['body']['text'],record=record))
    assert len(targets)==3 and sha256_file(args.review_shard)==original_hash
    result=dict(outcomes=dict(outcomes),field_counts=dict(counts),field_occurrences=dict(occs),field_templates={k:sorted(v) for k,v in field_ids.items()},
        field_examples=dict(examples),failures=failures,remaining_grammatical_key_captures=grammar,template_ties=ties,
        key_inventory_hits=dict(keyvalues),unknown_category_occurrences=dict(unknown),all_expected_messages_seen=True,owner_patterns=owner_patterns,
        selected_template_occurrences=dict(selected_templates),original_run_pipeline_records=targets,
        original_review_sha256=original_hash,original_review_unchanged=True,
        residual_function_words={key:dict(contextual_messages=count,occurrences=residual_occurrences[key]) for key,count in residual_messages.items()})
    write_json(args.output,result)
    print(json.dumps(dict(outcomes=dict(outcomes),fields=dict(counts),failures=len(failures),remaining_grammatical_key_captures=len(grammar),template_ties=len(ties),unknown_category_occurrences=dict(unknown)),indent=2))
    assert not failures and not grammar and all(owner_patterns.values())


if __name__=='__main__':main()
