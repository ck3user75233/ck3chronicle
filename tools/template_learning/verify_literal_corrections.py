"""Verify the owner's date/history correction on retained genuine messages."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re

from template_learning.evidence_serialization import native_evidence_rows, write_json
from template_learning import formatted_literals
from template_learning.owner_rules import OWNER_RULES
from template_learning.records import SequenceRecord
from template_learning.patterns import derive_pattern
from template_learning.clustering import grouping_scope, learning_tokens, cluster_source_records
from template_learning.matching_primitives import display_pattern
from template_learning.matcher_example import load_verified
from template_learning.inventory import sha256_file
from ck3chronicle.pipeline.contracts import materialize_definitions, identity_data
from template_learning.verify_location_candidate import prepared
from template_learning.verify_parser_correspondence import evidence_unit


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--bundle',type=Path)
    cli.add_argument('--evidence',type=Path,required=True)
    cli.add_argument('--package',type=Path)
    cli.add_argument('--output',type=Path,required=True)
    args=cli.parse_args()
    if args.bundle:
        records=[]
        for row,n in native_evidence_rows(args.bundle/'native_evidence.json'):
            text=row['native'];pieces=tuple(map(tuple,row['pieces']))
            dates=formatted_literals.ranges(pieces,OWNER_RULES['formatted_literals'])
            history=re.search(r" has history (?:after death|from before) birth, won't execute\.",text) if row['source_family']=='characterhistory.cpp' else None
            localization='Ymerodraeth' in text and 'Rufeinig' in text
            if not dates and not history and not localization:continue
            records.append(dict(source=row['source_family'],text=text,pieces=row['pieces'],
                context_kind=row['context_kind'],contexts=row['contexts'],continuations=row['continuations'],
                dates=[''.join(t for _,t in pieces[a:b]) for a,(b,_) in dates.items()],
                history=history.group() if history else None,localization=localization,
                occurrences=n,example_id=row['example_id'],provenance=row['native_occurrences']))
        write_json(args.evidence,records)
    else:records=json.loads(args.evidence.read_bytes())
    groups=defaultdict(list);counts=Counter();occurrences=Counter()
    for r in records:
        category='date' if r['dates'] else 'history' if r['history'] else 'localization'
        counts[category]+=1;occurrences[category]+=r['occurrences']
        if category=='localization':continue
        record=SequenceRecord(r['source'],r['text'],tuple(map(tuple,r['pieces'])),context_kind=r['context_kind'],contexts=r['contexts'],continuations=tuple(r['continuations']))
        groups[grouping_scope(record)].append(record)
    inferred=[]
    for pool in groups.values():
        if 'has history ' in pool[0].text:
            # Check the learner's actual refinement, not a construction gate
            # that pre-separates the two literal formulations.
            for cluster in cluster_source_records(pool[0].source_family,pool,.72):
                display=display_pattern(cluster.parts)
                assert not cluster.failures,cluster.failures
                assert all(r.text.split(' has history ',1)[1].split('. File location',1)[0]
                           in display for r in cluster.records),display
                inferred.append(dict(display=display,messages=len(cluster.records)))
            continue
        parts,failures=derive_pattern(pool,pool[0]);assert not failures,failures
        display=display_pattern(parts)
        assert sum('literal_format' in p for p in parts)==1,display
        assert len({learning_tokens(r) for r in pool})==1
        inferred.append(dict(display=display,messages=len(pool)))
    outcomes=Counter();checked=[]
    if args.package:
        package=load_verified(args.package,sha256_file(args.package/'manifest.json'))
        definitions=materialize_definitions(package)
        for r in records:
            assert r['context_kind']=='body' and not r['continuations'] and not r['contexts']
            unit=dict(parser=package.manifest['parser'],source_family=r['source'],source_tag=r['source'],
                      context_kind='body',body=dict(text=r['text'],pieces=r['pieces']),contexts={},continuations=[])
            match=package.match(evidence_unit(package,unit));assignment=prepared(package,match,definitions)
            assert assignment is not None,r['text']
            assert assignment['rendered']==[('body',r['text'])]
            values=assignment['values'];body=values['regions'][0];bindings=body['bindings']
            if r['dates']:
                assert [v for _,v in body['layout']['literal_choices'] if isinstance(v,str)]==r['dates']
                assert not any(b['value'] in r['dates'] for b in bindings)
                assert identity_data(values)['regions'][0]['layout']==body['layout']
                assert all(t in {b['type'] for b in bindings} for t in ('CHARACTER_ID_SHORT','CHARACTER_ID_SUPER_SHORT'))
            if r['history']:
                template=package.matcher.by_id[values['template_id']]
                assert r['history'] in template['display'],template['display']
            if r['localization']:
                expected=r['text'].split('Key is missing localization: ',1)[1].rstrip('\r\n')
                assert any(b['type']=='PARAM' and b['value']==expected for b in bindings)
            outcomes[assignment['status']]+=r['occurrences']
            checked.append(dict(example_id=r['example_id'],text=r['text'],occurrences=r['occurrences'],
                                template=package.matcher.by_id[values['template_id']]['display'],assignment=assignment))
    write_json(args.output,dict(counts=counts,occurrences=occurrences,inferred=inferred,
        outcomes=outcomes,checked=checked,limitations=['No genuine hyphenated date witness; space-separated dates verified.',
        'Same-template date equivalence and exact identity/rendering retention verified; no fabricated messages used.']))
    print(json.dumps(dict(counts=counts,occurrences=occurrences,inferred=inferred,outcomes=outcomes),indent=2))


if __name__=='__main__':main()
