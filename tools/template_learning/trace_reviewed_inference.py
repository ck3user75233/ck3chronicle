"""Trace retained v54 decisions for owner cases 7–10; no model is built or published."""
import argparse
from collections import defaultdict
import inspect
import json
from pathlib import Path
import sys


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--release-file',type=Path,required=True)
    cli.add_argument('--bundle',type=Path,required=True)
    cli.add_argument('--output',type=Path,required=True)
    cli.add_argument('--expect-correction',action='store_true')
    args=cli.parse_args()
    from template_learning.learner_loader import authenticate
    release=json.loads(args.release_file.read_bytes());authenticate(release['folder'],release['manifest_sha256'])
    for name in list(sys.modules):
        if name=='template_learning' or name.startswith('template_learning.'):del sys.modules[name]
    sys.path.insert(0,release['folder'])
    from template_learning import clustering as c
    from template_learning.records import SequenceRecord,identity
    from template_learning.evidence_serialization import native_evidence_rows,write_json
    from template_learning.matching_primitives import display_pattern
    assert Path(c.__file__).resolve().is_relative_to(Path(release['folder']).resolve())
    model=json.loads((args.bundle/'empirical_template_model.json').read_bytes())
    ids=['796ad48a3e5e8f97332f4427','766cfec88e63687b63c5123d','f7a161abe24ee04e2cd78b76','afac2b20cf8aab9ca59f9a09']
    targets={t['template_id']:t for t in model['templates'] if t['template_id'] in ids};del model
    wanted=set().union(*(set(t['evidence_record_ids']) for t in targets.values()))
    sources={t['source_family'] for t in targets.values()};pools=defaultdict(dict)
    for row,n in native_evidence_rows(args.bundle/'native_evidence.json'):
        if row['source_family'] not in sources:continue
        record=SequenceRecord(row['source_family'],row['native'],tuple(map(tuple,row['pieces'])),
            context_kind=row['context_kind'],contexts=row['contexts'],native_occurrences=row['native_occurrences'],continuations=tuple(row['continuations']))
        pools[record.source_family][identity(record.key)]=record
    events=[];similarities=[]
    original_derive=c.derive_pattern;original_guard=c.reject_wording_loss;original_comparable=c.comparable
    def target_ids(records):
        member_ids={identity(r.key) for r in records}
        return [key for key,t in targets.items() if member_ids.intersection(t['evidence_record_ids'])]
    def trace_derive(records,*a,**kw):
        result=original_derive(records,*a,**kw);affected=target_ids(records)
        if affected:
            stack=[f.function for f in inspect.stack()[1:7]]
            events.append(dict(operation='derive_pattern',stack=stack,targets=affected,members=len(records),
                display=display_pattern(result[0]),slots=[dict(name=p['name'],type=p['type'],values=p['observed_values']) for p in result[0] if p['kind']=='slot' and p['type'] in ('KEY','PARAM')],failures=result[1]))
        return result
    def trace_guard(previous,proposed,**kw):
        value=original_guard(previous,proposed,**kw);affected=target_ids(proposed.records)
        if affected:events.append(dict(operation='reject_wording_loss',targets=affected,path=kw['path'],rejected=value,
            previous=[display_pattern(x.parts) for x in previous],proposed=display_pattern(proposed.parts)))
        return value
    def comparable(left,right,threshold):
        result=original_comparable(left,right,threshold)
        if ('token','Unknown') in left and ('token','Unknown') in right and {('token','effect'),('token','trigger')}<=set(left)|set(right):
            item=dict(left=left,right=right,score=c.sequence_similarity(left,right),threshold=threshold,accepted=result)
            if item not in similarities:similarities.append(item)
        return result
    c.derive_pattern=trace_derive;c.reject_wording_loss=trace_guard;c.comparable=comparable
    finals={};reviews=[];corrected=[]
    for source,records in sorted(pools.items()):
        print('Tracing',source,len(records),flush=True)
        clusters=c.cluster_source_records(source,list(records.values()),.72,review=reviews)
        for cluster in clusters:
            if cluster.template_id in targets:finals[cluster.template_id]=display_pattern(cluster.parts)
            affected=target_ids(cluster.records)
            if affected:
                corrected.append(dict(targets=affected,template_id=cluster.template_id,display=display_pattern(cluster.parts)))
                if args.expect_correction and 'afac2b20cf8aab9ca59f9a09' in affected:
                    assert display_pattern(cluster.parts).startswith(('Unknown effect:','Unknown trigger:'))
                    assert not any(p.get('type') in ('KEY','PARAM') and {'effect','trigger'}.intersection(p['observed_values']) for p in cluster.parts if p['kind']=='slot')
                if args.expect_correction and '796ad48a3e5e8f97332f4427' in affected:
                    assert 'has history <PARAM> birth' in display_pattern(cluster.parts)
    if not args.expect_correction:assert set(finals)==set(targets),(set(targets)-set(finals))
    result=dict(scope='Reproduction of the retained v54 source-pool learning decisions for the four reviewed outcomes; not a fresh-versus-incremental comparison.',release=release,
        identical_final_patterns=all(finals[k]==targets[k]['display'] for k in finals),events=events,unknown_similarity=similarities,
        final_patterns=finals,corrected_patterns=corrected,correction_checked=args.expect_correction,source_records={k:len(v) for k,v in pools.items()})
    if not args.expect_correction:assert result['identical_final_patterns']
    write_json(args.output,result);print(json.dumps(dict(events=len(events),unknown_similarity=similarities,exact_final_ids=list(finals)),ensure_ascii=True))


if __name__=='__main__':main()
