"""Verify owner-approved discovery/consolidation behavior on genuine evidence."""
import argparse
import hashlib
import json
from pathlib import Path
from template_learning import clustering as c
from template_learning.records import SequenceRecord, identity
from template_learning.matching_defaults import match_pattern
from template_learning.matching_primitives import pattern_identity


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--probe',type=Path,required=True)
    p.add_argument('--trial',type=Path,required=True)
    p.add_argument('--inventory',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    probe=json.loads(a.probe.read_bytes());trial=json.loads(a.trial.read_bytes())
    inventory=json.loads(a.inventory.read_bytes())
    paths={r['sha256']:Path(r['snapshot']) for r in inventory['inputs']}
    native={};checks=[]
    for data in probe['sources'].values():
        for row in data['native_records']:
            o=row['native_occurrences'][0];sha=o['evidence_sha256']
            if sha not in native:
                raw=paths[sha].read_bytes();assert hashlib.sha256(raw).hexdigest()==sha;native[sha]=raw
            assert native[sha][slice(*o['span'])]==row['text'].encode('utf-8','surrogateescape')
    checks.append('all native record bytes verified against hashed logs')
    events=[SequenceRecord.from_dict(r) for r in probe['sources']['eventmanager.cpp']['native_records'][:2]]
    tokens=[c.learning_tokens(r) for r in events]
    assert tokens[0]==tokens[1] and c.sequence_similarity(*tokens)==1.0
    assert sum(k=='quoted-value' for k,v in tokens[0])==3
    # Declarations are not inferred from masking; real joint native inference is.
    joint=c.refine_literal_variants(c.TemplateCluster(events[0].source_family,'body',events,events[0]))
    assert len(joint)==1 and not joint[0].failures
    assert [p['type'] for p in joint[0].parts if p['kind']=='slot']==['KEY']*3
    checks.append('event values supply no discovery credit; complete joint inference yields three KEY fields')
    summaries={}
    for source,data in probe['sources'].items():
        records=[SequenceRecord.from_dict(r) for r in data['native_records']]
        review=[];groups=c.cluster_source_records(source,records,review=review)
        expected=trial['sources'][source]['quoted_contents_neutral']
        assert sorted(g.template_id for g in groups)==sorted(g['id'] for g in expected['final'])
        for r in records:
            matches=[g.template_id for g in groups if match_pattern(g.parts,r.text,pieces=r.pieces) is not None]
            assert matches==expected['body_matches'][identity(r.key)]
        summaries[source]=dict(records=len(records),templates=len(groups))
    checks.append('all 129 genuine final template identities and body assignments match reviewed quote trial')
    # Nine identical candidates produced by the genuine culture-name regrouping
    # pass must refresh all 18 members with exactly one derivation.
    data=probe['sources']['culture_name_equivalency.cpp']
    members={identity(r.key):r for r in [SequenceRecord.from_dict(x) for x in data['native_records']]}
    peers=[]
    for row in data['after']:
        records=[members[k] for k in row['record_ids']]
        peers.append(c.TemplateCluster(records[0].source_family,records[0].context_kind,
            records,records[0],parts=row['parts'],failures=row['failures']))
    assert len(peers)==9 and len({g.template_id for g in peers})==1
    actual=c.derive_pattern;calls=[]
    def observed(records,*args,**kwargs):
        calls.append(len(records));return actual(records,*args,**kwargs)
    c.derive_pattern=observed
    try:merged=c.consolidate_identical_templates(peers)
    finally:c.derive_pattern=actual
    assert calls==[18] and len(merged)==1 and not merged[0].failures
    assert merged[0].template_id==data['final'][0]['id']
    assert sorted(identity(r.key) for r in merged[0].records)==sorted(members)
    for r in merged[0].records:
        assert match_pattern(merged[0].parts,r.text,pieces=r.pieces) is not None
    for part in merged[0].parts:
        if part['kind']=='slot':
            assert {m['record_id'] for m in part['field_support']['members']}==set(members)
    checks.append('nine identical genuine candidates consolidated once; all 18 records and field-support members retained')
    # Each constituent's protected wording participates in the real guard.
    actual_guard=c.reject_wording_loss;guarded=[]
    def observed_guard(previous,proposed,**kwargs):
        guarded.append(len(previous));return actual_guard(previous,proposed,**kwargs)
    c.reject_wording_loss=observed_guard
    try:c.consolidate_identical_templates(peers)
    finally:c.reject_wording_loss=actual_guard
    assert guarded==[9]
    checks.append('wording guard receives every original constituent')
    result=dict(checks=checks,sources=summaries,logs_hash_verified=len(native),
        source_hashes={name:hashlib.sha256(Path(c.__file__).with_name(name).read_bytes()).hexdigest()
                      for name in ['clustering.py','regions.py']})
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
