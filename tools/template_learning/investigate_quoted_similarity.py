"""Isolated, non-publishing comparison of owner-proposed discovery scoring.

Consumes the genuine record slices saved by the regrouping investigation. The
selected frozen learner supplies inference and matching. Experimental overrides
exist only in this process; no model, release or learner rules are written.
"""
from __future__ import annotations

import argparse
from collections import Counter
from difflib import SequenceMatcher
import hashlib
import json
from pathlib import Path
import sys
import time


def quote_ranges(pieces):
    """Conservative single-quote proposals over existing native parser pieces.

    Apostrophes inside words are not delimiters. Ambiguous/nested quote syntax
    abstains for the whole message; this is an experimental boundary policy,
    not a new lexer or an assertion that every quoted interior is a KEY.
    """
    from template_learning.matching_primitives import punctuation_piece

    ranges, opened = [], None
    for i, (kind, value) in enumerate(pieces):
        if (kind, value) != ('token', "'"):
            continue
        left = pieces[i-1] if i else None
        right = pieces[i+1] if i+1 < len(pieces) else None
        can_open = left is None or left[0] == 'gap' or punctuation_piece(*left)
        can_close = right is None or right[0] == 'gap' or punctuation_piece(*right)
        if opened is None:
            if not can_open or (can_close and right != ('token', "'")):
                return (), 'ambiguous_quote_boundaries'
            opened = i
        elif can_close:
            if can_open and i != opened + 1:
                return (), 'ambiguous_quote_boundaries'
            if any('\n' in text or '\r' in text for _,text in pieces[opened+1:i]):
                return (), 'multiline_quote_boundaries'
            ranges.append((opened, i+1))
            opened = None
        elif can_open:
            return (), 'nested_quote_boundaries'
        # A word-internal apostrophe within an open quotation is interior data.
    if opened is not None:
        return (), 'unclosed_quote'
    return tuple(ranges), None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release-root', type=Path, required=True)
    parser.add_argument('--probe', type=Path, required=True)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.release_root.resolve()))
    from template_learning import clustering as c
    from template_learning.records import SequenceRecord, identity
    from template_learning.matching_defaults import match_pattern
    from template_learning.matching_primitives import pattern_identity

    original_tokens, original_score, original_comparable = c.learning_tokens,c.sequence_similarity,c.comparable
    original_regroup = c.refine_region_groups
    probe = json.loads(args.probe.read_bytes())
    inventory = json.loads(args.inventory.read_bytes())
    inputs = {r['sha256']:Path(r['snapshot']) for r in inventory['inputs']}
    verified = {}
    for d in probe['sources'].values():
        for row in d['native_records']:
            o=row['native_occurrences'][0];sha=o['evidence_sha256']
            if sha not in verified:
                raw=inputs[sha].read_bytes()
                assert hashlib.sha256(raw).hexdigest()==sha
                verified[sha]=raw
            a,b=o['span']
            assert verified[sha][a:b]==row['text'].encode('utf-8','surrogateescape')

    def projected(record, parts=None):
        if parts is not None:
            return original_tokens(record,parts)
        ranges,reason=quote_ranges(record.pieces)
        if not ranges:
            return original_tokens(record)
        units,spans=c.inference_units(record,region_first=True)
        offsets=[0]
        for _,value in record.pieces:
            offsets.append(offsets[-1]+len(value.encode('utf-8','surrogateescape')))
        diagnostic=c.constructions.comparison_ranges(record.source_family,record.text)
        # Do not look inside existing opaque fields or probable bracket regions.
        opaque=[(a,b) for unit,(a,b) in zip(units,spans) if unit[0] not in {'token','gap'}]
        ranges=[(a,b) for a,b in ranges if not any(x<b and a<y for x,y in opaque)
                and any(x<=offsets[a] and offsets[b]<=y for x,y in diagnostic)]
        if not ranges:
            return original_tokens(record)
        result=[(a,('quoted-value','present' if ''.join(t for _,t in record.pieces[a+1:b-1]).strip() else 'empty'))
                for a,b in ranges]
        for unit,(a,b) in zip(units,spans):
            if any(x<=a and b<=y for x,y in ranges):
                continue
            if unit[0]=='location-label':
                result.append((a,unit))
            elif unit[0]=='token' and any(v.isalnum() for v in unit[1]):
                if any(x<=offsets[a] and offsets[b]<=y for x,y in diagnostic):
                    result.append((a,unit))
            else:
                kind=None
                if unit[0]=='declared':kind=unit[3]
                elif unit[0]=='parameter':kind=c.parameter_structures.BY_ID[unit[1]].get('slot_type','PARAM')
                elif unit[0]=='location':kind='LOCATOR'
                elif unit[0]=='date-key':kind='KEY'
                if kind is not None:result.append((a,('field',kind)))
        return tuple(unit for _,unit in sorted(result))

    def quote_score(left,right):
        if not any(u[0]=='quoted-value' for u in (*left,*right)):
            return original_score(left,right)
        blocks=SequenceMatcher(None,left,right,autojunk=False).get_matching_blocks()
        matched=sum(left[b.a+i][0]!='quoted-value' for b in blocks for i in range(b.size))
        qmatched=sum(left[b.a+i][0]=='quoted-value' for b in blocks for i in range(b.size))
        qa,qb=[sum(u[0]=='quoted-value' for u in seq) for seq in (left,right)]
        short,long=sorted((len(left)-qa,len(right)-qb))
        missing=max(qa,qb)-qmatched
        if not short:return 0.0
        return .55*matched/(long+missing)+.35*matched/(short+missing)+.10*short/(long+missing)

    def quote_comparable(left,right,threshold):
        if any(u[0]=='quoted-value' for u in (*left,*right)):
            return quote_score(left,right)>=threshold
        return original_comparable(left,right,threshold)

    def view(cluster):
        return dict(id=cluster.template_id,pattern=pattern_identity(cluster.parts),
                    display=''.join(p.get('text','') if p['kind']=='literal' else '<'+p['type']+'>' for p in cluster.parts),
                    record_ids=[identity(r.key) for r in cluster.records],failures=cluster.failures)

    result=dict(experimental=True,scope='Bounded genuine source slices; no candidate publication or runtime classification',
        probe_sha256=hashlib.sha256(args.probe.read_bytes()).hexdigest(),release_root=str(args.release_root.resolve()),
        verified_logs=len(verified),sources={},quote_boundary_abstentions={})
    for source,d in probe['sources'].items():
        result['sources'][source]={}
        for mode in ['baseline','threshold_060','quoted_contents_neutral']:
            records=[SequenceRecord.from_dict(row) for row in d['native_records']]
            c.learning_tokens=projected if mode=='quoted_contents_neutral' else original_tokens
            c.sequence_similarity=quote_score if mode=='quoted_contents_neutral' else original_score
            c.comparable=quote_comparable if mode=='quoted_contents_neutral' else original_comparable
            captured={}
            def observe(groups,threshold,review):
                captured['before_regrouping']=[view(g) for g in groups]
                return original_regroup(groups,threshold,review)
            c.refine_region_groups=observe
            review=[];start=time.perf_counter()
            groups=c.cluster_source_records(source,records,.60 if mode=='threshold_060' else .72,review=review)
            # Restore for output; native pattern matching was never patched.
            c.refine_region_groups=original_regroup
            coverage={identity(r.key):[g.template_id for g in groups if match_pattern(g.parts,r.text,pieces=r.pieces) is not None] for r in records}
            value=dict(seconds=time.perf_counter()-start,**captured,final=[view(g) for g in groups],body_matches=coverage,
                accepted_regroupings=sum(e.get('decision')=='accepted' for e in review),review=review)
            result['sources'][source][mode]=value
            print(json.dumps(dict(source=source,mode=mode,before=len(captured['before_regrouping']),final=len(groups),
                accepted=value['accepted_regroupings'],unmatched=sum(not v for v in coverage.values()),seconds=value['seconds'])),flush=True)
        result['quote_boundary_abstentions'][source]=dict(Counter(quote_ranges(r.pieces)[1] or 'recognized_or_no_quote' for r in records))
        args.output.write_text(json.dumps(result,indent=2,ensure_ascii=True))
    c.learning_tokens,c.sequence_similarity,c.comparable=original_tokens,original_score,original_comparable
    event=[SequenceRecord.from_dict(r) for r in probe['sources']['eventmanager.cpp']['native_records'][:2]]
    before=[original_tokens(r) for r in event];after=[projected(r) for r in event]
    result['event_example']=dict(before=before,after=after,original_score=original_score(*before),quoted_score=quote_score(*after),
        original_matching_blocks=[list(b) for b in SequenceMatcher(None,*before,autojunk=False).get_matching_blocks()])
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=True))


if __name__=='__main__':
    main()
