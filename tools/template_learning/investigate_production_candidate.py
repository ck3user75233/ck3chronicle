"""Trace genuine coverage gains against production's authenticated matcher.

Inspection only: no alternative inference, patched patterns or manufactured logs.
"""
import argparse
from collections import Counter, defaultdict
import difflib
import json
from pathlib import Path
import sys
from types import SimpleNamespace

from template_learning.matcher_example import load_verified
from template_learning.verify_location_candidate import region
from template_learning.evidence_serialization import write_json


def read(path):
    return json.loads(Path(path).read_bytes())


def trace_pattern(rules, template, record):
    """Observe the actual matcher; retain the most advanced template position."""
    states=[]
    filename=rules.analyze_match_pattern.__func__.__code__.co_filename
    def trace(frame,event,arg):
        if frame.f_code.co_filename!=filename or frame.f_code.co_name!='visit':
            return None
        if event=='return':
            local=frame.f_locals
            states.append(dict(position=local['position'],index=local['index'],count=arg[0],
                next_part=local.get('part'),at_pattern_end=local['index']==len(local['plan'])))
        return trace
    sys.settrace(trace)
    try:
        result=rules.analyze_match_pattern(template['parts'],record.text,pieces=record.pieces)
    finally:
        sys.settrace(None)
    deepest=max(states,key=lambda s:(s['index'],s['position'])) if states else None
    if deepest:
        deepest['remaining_native']=record.text[deepest['position']:]
    return dict(count=result['count'],farthest_state=deepest,
        initial_literal_mismatch=not states and result['count']==0)


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--evidence',type=Path,required=True)
    cli.add_argument('--production',type=Path,required=True)
    cli.add_argument('--candidate',type=Path,required=True)
    args=cli.parse_args(); out=args.evidence
    comparison=read(out/'comparison.json')
    packages=dict(production=load_verified(args.production,comparison['production']['manifest_sha256']),
        candidate=load_verified(args.candidate,comparison['candidate']['pin']))
    templates={k:{t['template_id']:t for t in p.data['templates']} for k,p in packages.items()}
    groups=defaultdict(list); traces=[]
    messages=read(out/'messages.json')
    for message in messages:
        if message['results']['production'] is not None or not message['results']['candidate']:
            continue
        native=dict(message['native_regions']); parser=packages['candidate'].parser
        regions={k:region(parser,v) for k,v in native.items()}
        unit=dict(parser=packages['candidate'].manifest['parser'],recovery_status='recovered',
            source_family=message['source'],source_tag=message['source'],context_kind=message['context'],
            body=regions['body'],contexts={k:regions[k] for k in ('prefix','suffix') if k in regions},
            continuations=[v for k,v in regions.items() if k.startswith('continuation:')])
        results={k:p.match(unit,inspect=True) for k,p in packages.items()}
        assert results['production']['status']=='no_match'
        assignment=results['candidate']['assignment']
        selected=assignment['template_id']
        assert selected==message['results']['candidate']['values']['template_id']
        record=SimpleNamespace(source_family=unit['source_family'],context_kind=unit['context_kind'],
            text=unit['body']['text'],pieces=tuple(map(tuple,unit['body']['pieces'])),
            contexts={'native':unit['contexts']} if unit['contexts'] else {},continuations=unit['continuations'])
        rules=packages['production'].matcher.rules
        construction=rules.recognize(record.source_family,record.text)
        structures=[v[1] for _,v in sorted(rules.parameter_piece_ranges(record.pieces,record.source_family).items())]
        peers=[]
        for template in packages['production'].matcher.by_source[record.source_family]:
            gates=dict(context=template['context_kind']==record.context_kind,
                construction=template['construction_id']==(construction['id'] if construction else None),
                parameters=template['parameter_structures']==structures)
            if not gates['context']:continue
            diagnostic=template['display'].split('Script location:')[0]
            new_diagnostic=templates['candidate'][selected]['display'].split('Script location:')[0]
            rank=difflib.SequenceMatcher(None,diagnostic,new_diagnostic,autojunk=False).ratio()
            peers.append((rank,template,gates))
        # Display similarity orders the explanatory list only; public matching
        # above evaluated every production template using its actual contract.
        peers.sort(key=lambda x:(-x[0],x[1]['template_id']))
        peer_traces=[]
        chosen_peers=[item for i,item in enumerate(peers) if i<8 or
            item[1]['display'].split('Script location:')[0]==templates['candidate'][selected]['display'].split('Script location:')[0]]
        for rank,t,gates in chosen_peers:
            trace=trace_pattern(rules,t,record) if all(gates.values()) else None
            peer_traces.append(dict(template_id=t['template_id'],display=t['display'],status=t['status'],
                gates=gates,parameter_structures=t['parameter_structures'],construction_id=t['construction_id'],
                same_displayed_diagnostic=t['display'].split('Script location:')[0]==templates['candidate'][selected]['display'].split('Script location:')[0],
                pattern_trace=trace))
        row=dict(key=message['key'],source=record.source_family,native_regions=native,
            occurrences=message['occurrences'],references=message['references'],candidate_template=selected,
            candidate_assignment=assignment,production_recognition=construction,
            production_parameter_structures=structures,production_peers=peer_traces,
            production_complete_matches=len(results['production']['inspection']['matches']),
            production_ambiguous_captures=len(results['production']['inspection']['capture_ambiguities']))
        traces.append(row);groups[selected].append(row)
    summaries=[]
    for identifier,rows in sorted(groups.items(),key=lambda item:-sum(r['occurrences'] for r in item[1])):
        values=defaultdict(Counter)
        for row in rows:
            for region_row in row['candidate_assignment']['regions']:
                for cap in region_row['captures']:
                    if cap['present']:
                        values[(region_row['name'],cap['slot_id'],cap['type'])][cap['value']]+=row['occurrences']
        summaries.append(dict(template_id=identifier,display=templates['candidate'][identifier]['display'],
            messages=len(rows),occurrences=sum(r['occurrences'] for r in rows),
            captures=[dict(region=k[0],slot=k[1],type=k[2],values=dict(v)) for k,v in values.items()]))
    write_json(out/'production-gain-traces.json',dict(scope='Production versus controlled incremental candidate only',
        packages=comparison['production']|{'candidate':comparison['candidate']},
        method='All newly classified stored-Run messages replayed through both pinned public matchers; nearest displayed production patterns annotated with actual applicability gates and memoized matcher states. No inputs or templates modified.',
        groups=summaries,messages=traces))
    print(json.dumps(dict(messages=len(traces),occurrences=sum(r['occurrences'] for r in traces),templates=len(groups),
        group_counts=[{k:g[k] for k in ('template_id','messages','occurrences')} for g in summaries]),indent=2))


if __name__=='__main__':main()
