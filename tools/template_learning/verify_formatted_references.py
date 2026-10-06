"""Verify control-marked references on genuine evidence and a disposable export."""
import argparse
import copy
from collections import Counter, defaultdict
import json
from pathlib import Path

from template_learning.evidence_serialization import native_evidence_rows, write_json
from template_learning.matching_defaults import RULES
from template_learning.matching_primitives import Rules
from template_learning.matcher_example import load_verified
from template_learning.inventory import sha256_file
from template_learning.verify_parser_correspondence import evidence_unit


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--bundle',type=Path,required=True)
    cli.add_argument('--baseline',type=Path,required=True)
    cli.add_argument('--output',type=Path,required=True)
    cli.add_argument('--candidate',type=Path)
    cli.add_argument('--preflight',type=Path)
    args=cli.parse_args()
    old=load_verified(args.baseline,sha256_file(args.baseline/'manifest.json'))
    if args.candidate:
        candidate=load_verified(args.candidate,sha256_file(args.candidate/'manifest.json'))
        data=json.loads(args.preflight.read_bytes()); transitions=Counter(); matched=Counter();failures=[]
        for row in data['records']:
            unit=dict(parser=candidate.manifest['parser'],source_family=row['source'],source_tag=row['source'],
                context_kind=row['context_kind'],body=dict(text=row['text'],pieces=row['pieces']),
                contexts=next(iter(row['contexts'].values()),{}),continuations=row['continuations'])
            before=old.match(evidence_unit(old,unit))['assignment']
            after=candidate.match(evidence_unit(candidate,unit))['assignment']
            transitions[(before['match_status'] if before else 'no_match')+' -> '+(after['match_status'] if after else 'no_match')]+=row['occurrences']
            if after:
                captures=next(r['captures'] for r in after['regions'] if r['name']=='body')
                for field in row['fields']:
                    if not any(c['type']=='PARAM' and c['value']==field['value'] for c in captures):
                        failures.append(dict(example_id=row['example_id'],field=field,template_id=after['template_id']))
                matched[after['template_id']]+=row['occurrences']
            else:failures.append(dict(example_id=row['example_id'],reason='no complete assignment'))
        result=dict(package_id=candidate.manifest['package_id'],messages=len(data['records']),transitions=dict(transitions),templates=dict(matched),failures=failures)
    else:
        declarations=copy.deepcopy(RULES.declarations)
        next(d for d in declarations['parameter_structures'] if d['id']=='formatted-linked-reference').pop('defer_inside_quotes')
        unbounded=Rules(declarations)
        counts=Counter();weighted=Counter();prior_fields=Counter();records=[];rows=0;preserved=0
        for row,n in native_evidence_rows(args.bundle/'native_evidence.json'):
            rows+=1;pieces=tuple(map(tuple,row['pieces']));source=row['source_family']
            before=old.matcher.rules.parameter_piece_ranges(pieces,source)
            after=RULES.parameter_piece_ranges(pieces,source)
            for a,v in before.items():
                assert after.get(a)==v,(row['example_id'],'existing field changed',a,v,after.get(a))
                prior_fields[v[1]]+=1
            fields=[]
            for a,(b,identifier) in after.items():
                if identifier!='formatted-linked-reference':continue
                value=''.join(t for _,t in pieces[a:b])
                assert value.endswith('\x15!\x15!') and value.startswith(('\x15ONCLICK:','\x15TOOLTIP:'))
                fields.append(dict(pieces=[a,b],value=value));counts[source]+=1;weighted[source]+=n
            # Also verify genuine larger inferred PARAMs, not just declarations.
            proposed=unbounded.parameter_piece_ranges(pieces,source)
            deferred=[(a,b) for a,(b,d) in proposed.items() if d=='formatted-linked-reference' and a not in after]
            if deferred:
                unit=dict(parser=old.manifest['parser'],source_family=source,source_tag=source,
                    context_kind=row['context_kind'],body=dict(text=row['native'],pieces=row['pieces']),
                    contexts=next(iter(row['contexts'].values()),{}),continuations=row['continuations'])
                assignment=old.match(unit)['assignment']
                captures=next(r['captures'] for r in assignment['regions'] if r['name']=='body') if assignment else []
                for a,b in deferred:
                    value=''.join(t for _,t in pieces[a:b])
                    enclosing=[c for c in captures if c['type']=='PARAM' and value in c['value'] and value!=c['value']]
                    assert len(enclosing)==1,(row['example_id'],'deferred field without existing enclosing PARAM')
                    fields.append(dict(value=enclosing[0]['value'],preserved_enclosing=True));preserved+=1
            if fields:records.append(dict(example_id=row['example_id'],source=source,text=row['native'],pieces=row['pieces'],
                context_kind=row['context_kind'],contexts=row['contexts'],continuations=row['continuations'],
                occurrences=n,fields=fields,provenance=row['native_occurrences'][:1]))
            if rows%20000==0:print('Verified',rows,flush=True)
        result=dict(rows=rows,messages=len(records),counts=dict(counts),weighted_fields=dict(weighted),preserved_enclosing_params=preserved,
                    prior_fields_preserved=dict(prior_fields),records=records)
    args.output.parent.mkdir(parents=True,exist_ok=True);write_json(args.output,result)
    print(json.dumps({k:v for k,v in result.items() if k!='records'},ensure_ascii=True,indent=2),flush=True)
    if args.candidate:
        assert not result['failures'], result['failures']


if __name__=='__main__':main()
