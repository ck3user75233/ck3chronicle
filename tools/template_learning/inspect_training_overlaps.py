"""Inspect every genuine template-to-provisional transition against production."""
import argparse
import json
from pathlib import Path
from template_learning.matcher_example import load_verified
from template_learning.evidence_serialization import native_evidence_rows, write_json
from template_learning.analyze_removed_templates import changes, native_regions


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--evidence',type=Path,required=True)
    cli.add_argument('--bundle',type=Path,required=True)
    cli.add_argument('--production',type=Path,required=True)
    cli.add_argument('--candidate',type=Path,required=True)
    args=cli.parse_args();out=args.evidence
    read=lambda p:json.loads(p.read_bytes())
    comparison=read(out/'comparison.json');training=read(out/'training-corpus-comparison.json')
    edges=[e for e in training['edges'] if e['before_status']=='template' and e['after_status']=='provisional']
    targets={e['after'] for e in edges};expected=sum(e['occurrences'] for e in edges)
    old=load_verified(args.production,comparison['production']['manifest_sha256'])
    new=load_verified(args.candidate,comparison['candidate']['pin']);rows=[]
    for row,count in native_evidence_rows(args.bundle/'native_evidence.json'):
        selected=row.get('selected_assignment')
        if not selected or selected['template_id'] not in targets:continue
        unit=dict(parser=new.manifest['parser'],source_family=row['source_family'],context_kind=row['context_kind'],
            body=dict(text=row['native'],pieces=row['pieces']),contexts=next(iter(row['contexts'].values()),{}),continuations=row['continuations'])
        before=old.match(unit,inspect=True);after=new.match(unit,inspect=True)
        a,b=before['assignment'],after['assignment']
        if not a or a['match_status']!='template' or not b or b['match_status']!='provisional':continue
        texts=native_regions(unit);diffs=changes(a,b,texts)
        rows.append(dict(witness=dict(source=row['source_family'],native_regions=texts,provenance=row['native_occurrences'],occurrences=count,
            before=a['template_id'],after=b['template_id'],changes=diffs),result=after,production_result=before))
    assert sum(r['witness']['occurrences'] for r in rows)==expected
    write_json(out/'production-downgrade-traces.json',rows)
    for r in rows:
        s=r['result']['inspection']['selected_assignment']['selection']
        print(json.dumps(dict(occurrences=r['witness']['occurrences'],changes=r['witness']['changes'],selection=s),ensure_ascii=True))


if __name__=='__main__':main()
