"""Trace a locator-candidate inference regression using authenticated native evidence."""
import argparse
import json
import sys
import inspect
from pathlib import Path

from template_learning.location_candidate_experiment import save, sha
from template_learning.evidence_serialization import native_evidence_rows
from template_learning.records import SequenceRecord, identity
from template_learning import clustering
from template_learning.patterns import derive_pattern
from template_learning.matching_primitives import display_pattern


def model(folder):
    manifest = json.loads((folder/'manifest.json').read_text())
    path = folder/'empirical_template_model.json'
    assert sha(path)==manifest['hashes'][path.name]
    return json.loads(path.read_text())


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--before',type=Path,required=True)
    cli.add_argument('--after',type=Path,required=True)
    cli.add_argument('--output',type=Path,required=True)
    cli.add_argument('--source-ranking',action='store_true')
    args=cli.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    before=model(args.before)
    prior=next(t for t in before['templates'] if t['template_id']=='4992aa31ffdc6074f4b31ebd')
    expected=set(prior['evidence_record_ids'])
    after=model(args.after)
    evidence=args.after/'native_evidence.json'
    assert sha(evidence)==json.loads((args.after/'manifest.json').read_text())['hashes'][evidence.name]
    selected=[]
    source_records=[]
    for row,count in native_evidence_rows(evidence):
        if row['source_family']!='jomini_script_system.cpp':
            continue
        record=SequenceRecord(row['source_family'],row['native'],tuple(map(tuple,row['pieces'])),
            row['context_kind'],row['contexts'],row['native_occurrences'],tuple(row['continuations']))
        if args.source_ranking:
            source_records.append(record)
        if identity(record.key) in expected:
            selected.append((record,row,count))
    assert len(selected)==len(expected)==2
    rows=[]
    for record,native,count in selected:
        tokens=clustering.learning_tokens(record)
        rows.append(dict(record_id=identity(record.key),text=record.text,pieces=record.pieces,
            occurrences=count,provenance=native['native_occurrences'],tokens=tokens,
            anchors=sorted(clustering.anchors(tokens)),scope=clustering.grouping_scope(record)))
    records=[r for r,_,_ in selected]
    parts,failures=derive_pattern(records,clustering.choose_medoid(records))
    review=[]
    clusters=clustering.cluster_source_records('jomini_script_system.cpp',records,.72,review=review)
    relevant=[t for t in after['templates'] if expected.intersection(t['evidence_record_ids'])]
    events=[e for e in after['region_discovery']['decisions']
            if isinstance(e.get('records'),list) and expected.intersection(e['records'])]
    result=dict(before_template={k:prior[k] for k in ('template_id','display','learning_support','evidence_record_ids')},
        after_templates=[{k:t[k] for k in ('template_id','display','learning_support','evidence_record_ids','inference_refinements')} for t in relevant],
        native_examples=rows,raw_similarity=clustering.sequence_similarity(*(clustering.learning_tokens(r) for r in records)),
        discovery_comparable=clustering.comparable(*(clustering.learning_tokens(r) for r in records),.72),
        joint_inference=dict(display=display_pattern(parts),failures=failures,
            tokens=[clustering.learning_tokens(r,parts) for r in records]),
        pair_only_templates=[dict(display=display_pattern(c.parts),failures=c.failures) for c in clusters],
        pair_only_review=review,full_build_events=events)
    if 'refinement_history' in after:
        from template_learning.refinement_history import history_events
        result['refinement_history'] = list(history_events(after,
            [reference for t in relevant for reference in t['inference_refinements']]))
    save(args.output/'trace.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('full_build_events','pair_only_review','native_examples')},indent=2),flush=True)
    print('Native comparison',json.dumps([{k:r[k] for k in ('tokens','anchors','scope')} for r in rows]),flush=True)
    print('Full build events:',len(events),flush=True)
    if args.source_ranking:
        from template_learning.artifacts import _learn_pool
        rankings=[]
        watched=clustering.refine_region_groups.__code__
        lines,first=inspect.getsourcelines(clustering.refine_region_groups)
        stop_line=first+next(i for i,line in enumerate(lines) if 'limit=INFERENCE_POLICY' in line)
        def trace(frame,event,arg):
            if frame.f_code is not watched:
                return None
            if event=='line' and frame.f_lineno==stop_line:
                local=frame.f_locals
                left=local['left']
                left_members={identity(r.key) for r in left.records}
                if expected.intersection(left_members):
                    peers=local['possible']
                    rankings.append(dict(left=left.template_id,left_members=sorted(left_members),
                        display=display_pattern(left.parts),
                        candidates=[dict(rank=i+1,template_id=p.template_id,display=display_pattern(p.parts),
                            target=bool(expected.intersection(identity(r.key) for r in p.records)),
                            words=sorted(local['word_sets'][id(p)])) for i,p in enumerate(peers)]))
            return trace
        sys.settrace(trace)
        try:
            inferred=_learn_pool('jomini_script_system.cpp',source_records,.72,[])
        finally:
            sys.settrace(None)
        save(args.output/'ranking.json',dict(records=len(source_records),rankings=rankings,
            inferred_templates=len(inferred)))
        print('Rankings saved',flush=True)


if __name__=='__main__':
    main()
