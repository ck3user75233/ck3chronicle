"""Check new character/date fields and survey old captures on genuine evidence."""
import argparse
from bisect import bisect_right
from collections import Counter, defaultdict
import json
from pathlib import Path
import re

from template_learning.location_candidate_experiment import save, sha
from template_learning.matcher_example import load_verified
from template_learning.verify_location_candidate import region
from template_learning.matching_defaults import RULES
from template_learning.evidence_serialization import native_evidence_rows
from template_learning import formatted_literals


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--experiment',type=Path,required=True)
    cli.add_argument('--baseline',type=Path,required=True)
    args=cli.parse_args();out=args.experiment.resolve()
    manifest,=(args.baseline/'packages').glob('*/manifest.json')
    package=load_verified(manifest.parent,sha(manifest))
    corpus=json.loads((out/'corpus.json').read_text())
    requested=defaultdict(list)
    for kind in ('dates','plain_titled_candidates'):
        for row in corpus[kind]:requested[row['example']['path']].append((kind,row))
    fields=[];plain=[];name_counts=Counter();raw_name_counts=Counter();old_receiver=Counter()
    for path,rows in requested.items():
        raw=Path(path).read_bytes();assert sha(Path(path))==rows[0][1]['example']['sha256']
        segments=raw.split(b'\n')
        lines=[part+b'\n' for part in segments[:-1]]+[segments[-1]]
        # CK3 formatting controls are not physical line or emission boundaries.
        headers=[i for i,line in enumerate(lines) if re.match(rb'^\[[0-9:]+\]\[',line)]
        blocks={}
        for kind,row in rows:
            # Preserve the complete actual parent emission of every witness.
            index=row['example']['line']-1
            assert row['text'] in lines[index].decode('utf-8','surrogateescape'),(path,index)
            h=bisect_right(headers,index)-1;start=headers[h];end=headers[h+1] if h+1<len(headers) else len(lines)
            if start not in blocks:
                fragment=b''.join(lines[start:end]);parsed=package.parser.parse_bytes(fragment,source_name=path+':line'+str(start+1),parser_reference=package.manifest['parser'])
                blocks[start]=list(package.iter_units(parsed))
            units=blocks[start]
            if kind=='dates':
                unit=next(u for u in units if row['date'] in u['body']['text'])
                text=unit['body']['text'];pieces=tuple(map(tuple,unit['body']['pieces']))
                spans=RULES.parameter_piece_ranges(pieces,unit['source_family'])
                recognized={d:''.join(t for _,t in pieces[a:b]) for a,(b,d) in spans.items()}
                recognized.update({d:''.join(t for _,t in pieces[a:b]) for a,(b,d) in
                    formatted_literals.ranges(pieces,RULES.declarations.get('formatted_literals', ())).items()})
                short=re.search(re.escape(row['date'])+r' (?P<name>[^()\r\n]+) \((?P<id>[0-9]+), (?P<place>[^()\r\n]+)\):',text)
                assert short
                expected=short['name']+' ('+short['id']+', '+short['place']+')'
                receiver_match=re.search(r'receiver is (.+?), default location is ',text)
                receiver=receiver_match[1]
                receiver_span=[len(text[:position].encode('utf-8','surrogateescape')) for position in receiver_match.span(1)]
                assert recognized['game-date-prefix']==row['date'][:-1]
                assert recognized['character-id-short']==expected
                assert recognized['receiver-before-default-location']==receiver
                if 'default-location-name' in RULES.parameter_definitions:
                    assert recognized['default-location-name']==text.split('default location is ',1)[1].rstrip(' \t\r\n')
                name_counts[len(short['name'].split())]+=row['count']
                raw_name_counts[sum(k=='token' for k,t in region(package.parser,short['name'])['pieces'])]+=row['count']
                result=package.match(unit);assignment=result['assignment'];types=[]
                if assignment:
                    for r in assignment['regions']:
                        for c in r['captures']:
                            if r['name']=='body' and c.get('span') and c['span'][0]<=receiver_span[0] and receiver_span[1]<=c['span'][1]:types.append(c['type'])
                old_receiver['+'.join(sorted(set(types))) if types else ('literal' if assignment else 'no_match')]+=row['count']
                fields.append(dict(text=text,count=row['count'],name=short['name'],name_words=len(short['name'].split()),identity=expected,receiver=receiver,recognized=recognized,source=unit['source_family'],example=row['example'],baseline_status=assignment['match_status'] if assignment else 'no_match',baseline_receiver_types=types))
            else:
                value=row['value'];categories=set()
                for unit in units:
                    if value not in unit['body']['text']:continue
                    result=package.match(unit);assignment=result['assignment']
                    found=set()
                    if assignment:
                        for r in assignment['regions']:
                            found.update(c['type'] for c in r['captures'] if c.get('value') and value in c['value'])
                    categories.update(found or {('literal' if assignment else 'no_match')})
                plain.append(dict(**row,capture_categories=sorted(categories or {'no_recovered_body_containing_expression'})))
    # Compare every existing full identity in the same twenty-log evidence pool.
    native,=(args.baseline/'candidate').glob('*/native_evidence.json')
    expected=json.loads((native.parent/'manifest.json').read_text())['hashes']['native_evidence.json'];assert sha(native)==expected
    preserved=Counter();full_examples=[]
    for row,count in native_evidence_rows(native):
        if 'Internal ID' not in row['native']:continue
        pieces=tuple(map(tuple,row['pieces']));source=row['source_family']
        def full_fields(rules):
            return [(a,b,d) for a,(b,d) in rules.parameter_piece_ranges(pieces,source).items() if rules.parameter_definitions[d]['mechanic']=='full_id']
        before=full_fields(package.matcher.rules);after=full_fields(RULES)
        assert before==after,(source,row['record_id'])
        for a,b,d in before:preserved[d]+=count
        if before and len(full_examples)<5:full_examples.append(dict(source=source,text=row['native']))
    save(out/'field-verification.json',dict(genuine_date_short_occurrences=sum(r['count'] for r in fields),name_word_counts=name_counts,name_raw_token_counts=raw_name_counts,fields=fields,baseline_receiver_capture_counts=old_receiver,
        plain_titled_capture_counts=dict(Counter({k:sum(r['count'] for r in plain if k in r['capture_categories']) for k in {k for r in plain for k in r['capture_categories']}})),plain_titled_examples=plain,full_id_preserved_occurrences=preserved,full_id_examples=full_examples,
        limitations=['No short-identity/date family beyond the 75 travel examples was found in 104 complete logs.','Hyphenated day-month-year is owner-requested but has no genuine corpus witness.']+(['Undated short identities are permitted by the rule but have no genuine corpus witness.'] if 'default-location-name' in RULES.parameter_definitions else ['Multiword default-location display names remain ordinary inference; this trial does not declare a new location-name field.'])))
    print(json.dumps(dict(name_word_counts=name_counts,full_ids_preserved=preserved,baseline_receiver_capture_counts=old_receiver),indent=2))


if __name__=='__main__':main()
