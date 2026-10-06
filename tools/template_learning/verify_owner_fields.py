"""Verify owner-approved whole fields on retained genuine training messages."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
from template_learning.evidence_serialization import native_evidence_rows, write_json
from template_learning.matching_defaults import RULES
from template_learning.matcher_example import load_verified

FIELDS={'character-parent-state-phrase','formatting-tag-content',
        'compare-trigger-identifier','compare-trigger-expected-scope','missing-localization-display','marked-character-line-reference',
        'invalid-comparison-side','invalid-comparison-identifier'}


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--bundle',type=Path,required=True)
    cli.add_argument('--baseline',type=Path,required=True)
    cli.add_argument('--pin',required=True)
    cli.add_argument('--output',type=Path,required=True)
    args=cli.parse_args();old=load_verified(args.baseline,args.pin)
    counts=Counter();occ=Counter();values=defaultdict(Counter);examples=defaultdict(list);records=[];full=0;rows=0
    for row,n in native_evidence_rows(args.bundle/'native_evidence.json'):
        rows+=1;pieces=tuple(map(tuple,row['pieces']));source=row['source_family']
        before=old.matcher.rules.parameter_piece_ranges(pieces,source)
        after=RULES.parameter_piece_ranges(pieces,source)
        def full_ids(ranges,rules):
            return [(a,b,d) for a,(b,d) in ranges.items() if rules.parameter_definitions[d]['mechanic']=='full_id']
        prior=full_ids(before,old.matcher.rules);assert prior==full_ids(after,RULES),(row['example_id'],'full ID changed')
        full+=len(prior)
        found={}
        for a,(b,identifier) in after.items():
            if identifier not in FIELDS:continue
            value=''.join(text for _,text in pieces[a:b]);found.setdefault(identifier,[]).append(value)
            counts[identifier]+=1;occ[identifier]+=n;values[identifier][value]+=n
            if len(examples[identifier])<3:examples[identifier].append(dict(value=value,text=row['native'],source=source,provenance=row['native_occurrences'][:1]))
        for identifier in FIELDS:
            rule=RULES.parameter_definitions[identifier]
            if rule.get('source',source)!=source:continue
            expected=[m.group() for prefix in re.finditer(rule['prefix'],row['native']) if (m:=re.compile(rule['content']).match(row['native'],prefix.end()))]
            assert expected==found.get(identifier,[]),(identifier,row['example_id'],expected,found)
        if found:records.append(dict(example_id=row['example_id'],source=source,native=row['native'],pieces=row['pieces'],context_kind=row['context_kind'],contexts=row['contexts'],continuations=row['continuations'],occurrences=n,fields=found,provenance=row['native_occurrences'][:1]))
        if rows%20000==0:print('Verified',rows,flush=True)
    assert counts.keys()==FIELDS
    result=dict(rows=rows,unchanged_full_id_captures=full,counts=dict(counts),occurrences=dict(occ),values={k:dict(v) for k,v in values.items()},examples=dict(examples),records=records)
    write_json(args.output,result)
    print(json.dumps(dict(rows=rows,unchanged_full_id_captures=full,counts=dict(counts),occurrences=dict(occ)),indent=2))


if __name__=='__main__':main()
