"""Evaluate every genuine inventoried short-identity message with the candidate."""
import argparse
from collections import Counter
import json
from pathlib import Path

from ck3chronicle.pipeline.contracts import materialize_definitions
from template_learning.location_candidate_experiment import save,sha
from template_learning.matcher_example import load_verified
from template_learning.verify_location_candidate import region,prepared,captures
from template_learning import formatted_literals


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--experiment',type=Path,required=True)
    cli.add_argument('--require-one-template',action='store_true')
    cli.add_argument('--receiver-type',default='PARAM')
    args=cli.parse_args();out=args.experiment.resolve()
    path,=(out/'packages').glob('*/manifest.json');package=load_verified(path.parent,sha(path))
    definitions=materialize_definitions(package)
    survey=json.loads((out/'field-verification.json').read_text())
    rows=[];transitions=Counter();missing=[]
    for row in survey['fields']:
        body=region(package.parser,row['text'])
        unit=dict(parser=package.manifest['parser'],source_family=row['source'],source_tag=row['source'],context_kind='body',body=body,contexts={},continuations=[])
        match=package.match(unit);assignment=prepared(package,match,definitions)
        status=assignment['status'] if assignment else 'no_match'
        transitions[row['baseline_status']+' -> '+status]+=row['count']
        recognition={d:''.join(t for _,t in body['pieces'][a:b]) for a,(b,d) in package.matcher.rules.parameter_piece_ranges(tuple(map(tuple,body['pieces'])),row['source']).items()}
        formats=package.matcher.rules.declarations.get('formatted_literals', ())
        recognition.update({d:''.join(t for _,t in body['pieces'][a:b]) for a,(b,d) in
            formatted_literals.ranges(tuple(map(tuple,body['pieces'])),formats).items()})
        assert all(recognition[k]==v for k,v in row['recognized'].items())
        if assignment:
            assert assignment['rendered']==[('body',row['text'])]
            values=captures(assignment)
            assert any(v[1]=='CHARACTER_ID_SHORT' and v[2]==row['identity'] for v in values)
            assert any(v[1]==args.receiver_type and v[2]==row['receiver'] for v in values)
            date=row['recognized']['game-date-prefix']
            if formats:
                assert date in [v for r in assignment['values']['regions'] for _,v in r['layout'].get('literal_choices', [])]
                assert not any(v[2]==date for v in values)
            else:
                assert any(v[1]=='KEY' and v[2]==date for v in values)
            if 'default-location-name' in row['recognized']:
                assert any(v[1]=='PARAM' and v[2]==row['recognized']['default-location-name'] for v in values)
        else:missing.append(row['text'])
        rows.append(dict(text=row['text'],example=row['example'],before=row['baseline_status'],after=status,
                         assignment=assignment,definition=package.matcher.by_id[match['assignment']['template_id']]['display'] if assignment else None))
    if args.require_one_template:
        assert not missing and all(r['after']=='template' for r in rows)
        assert len({r['assignment']['values']['template_id'] for r in rows})==1
        assert len({r['assignment']['identity'] for r in rows})==len(rows)
    save(out/'all-short-identities.json',dict(messages=len(rows),transitions=transitions,all_fields_recognized=True,receiver_type=args.receiver_type,one_template_required=args.require_one_template,unmatched_messages=missing,rows=rows))
    print(json.dumps(dict(messages=len(rows),transitions=transitions,unmatched=len(missing)),indent=2))


if __name__=='__main__':main()
