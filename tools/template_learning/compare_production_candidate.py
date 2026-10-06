"""Compare pinned packages with genuine stored assignments and native review routes."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

from ck3chronicle.pipeline.contracts import materialize_definitions, render_regions
from template_learning.location_candidate_experiment import save, sha
from template_learning.matcher_example import load_verified
from template_learning.verify_location_candidate import stored_unit, prepared, captures
from template_learning.verify_parser_correspondence import corresponding_units


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--root',type=Path,required=True)
    cli.add_argument('--evidence',type=Path,required=True)
    cli.add_argument('--candidate',type=Path,required=True)
    cli.add_argument('--candidate-pin',required=True)
    cli.add_argument('--stored-evidence',type=Path,help='Reuse an existing immutable Run snapshot directory without copying its documents.')
    args=cli.parse_args();root=args.root.resolve();out=args.evidence.resolve()
    snapshot=args.stored_evidence.resolve() if args.stored_evidence else out
    historical_guard=json.loads((snapshot/'production-before.json').read_text())
    operation_guard={p:sha(root/p) for p in historical_guard}
    # Catalogs can legitimately acquire retained candidates between reviews.
    # Guard this read-only operation against mutation, while exposing pre-existing
    # differences from the snapshot-era catalogs instead of silently ignoring them.
    historical_catalog_changes=[p for p,h in historical_guard.items() if operation_guard[p]!=h]
    selection=json.loads((root/'models/selection.json').read_text())
    packages=dict(production=load_verified(root/'models'/selection['artifact_directory'],selection['manifest_sha256']),
                  candidate=load_verified(args.candidate,args.candidate_pin))
    definitions={k:materialize_definitions(p) for k,p in packages.items()}
    training_hashes={k:{r['sha256'] for r in p.data['training_evidence']} for k,p in packages.items()}
    training_comparison=dict(exact_hash_set=training_hashes['production']==training_hashes['candidate'],
        production_only=sorted(training_hashes['production']-training_hashes['candidate']),
        candidate_only=sorted(training_hashes['candidate']-training_hashes['production']))
    evidence=json.loads((snapshot/'stored-evidence.json').read_text())
    if snapshot!=out:
        save(out/'stored-evidence.json',dict(evidence,snapshot_directory=str(snapshot)))
    assert set(evidence['training_hashes'])==training_hashes['candidate']
    cache={};counts={k:Counter() for k in packages};transitions=Counter();runs=[];parity=[];collisions={};checks=Counter();review_files=[]

    def evaluate(units):
        corresponding_units(units)
        unit=units['candidate']
        native=[('body',unit['body']['text']),*[(k,v['text']) for k,v in unit['contexts'].items()],
                *[('continuation:'+str(i),r['text']) for i,r in enumerate(unit['continuations'])]]
        key=hashlib.sha256(repr((unit['source_family'],unit['context_kind'],native)).encode('utf-8','surrogateescape')).hexdigest()
        if key not in cache:
            results={k:prepared(p,p.match(units[k]),definitions[k]) for k,p in packages.items()}
            for label,result in results.items():
                if result:
                    # Names for continuation regions come from the contract; native
                    # order and exact text must reproduce every original region.
                    assert dict(result['rendered'])==dict(native),(label,key)
                    prior=collisions.setdefault((label,result['identity']),key)
                    assert prior==key,'different native messages collapsed'
            cache[key]=dict(key=key,source=unit['source_family'],context=unit['context_kind'],text=unit['body']['text'],
                            native_regions=native,results=results,occurrences=0,stored_occurrences=0,review_occurrences=0,references=[])
        return cache[key]

    def account(item,n,reference,actual_status,actual_id=None):
        results=item['results'];statuses={k:r['status'] if r else 'no_match' for k,r in results.items()}
        old=results['production'];old_id=old['values']['template_id'] if old else None
        if statuses['production']!=actual_status or (actual_id is not None and old_id!=actual_id):
            parity.append(dict(reference=reference,actual_status=actual_status,replayed_status=statuses['production'],actual_id=actual_id,replayed_id=old_id))
        item['occurrences']+=n;item[reference['kind']+'_occurrences']+=n
        item['references'].append(dict(**reference,occurrences=n))
        for label,status in statuses.items():counts[label][status]+=n
        transition=statuses['production']+' -> '+statuses['candidate'];transitions[transition]+=n
        return statuses,transition

    for info in evidence['runs']:
        run_id=info['run_id'];document=json.loads((snapshot/(run_id+'.json')).read_text())
        assert document['run']['lineage']['package_id']==selection['package_id']
        local={k:Counter() for k in packages};local_transitions=Counter()
        for row in document['records']:
            item=evaluate({k:stored_unit(p,row) for k,p in packages.items()})
            statuses,transition=account(item,row['occurrence_count'],dict(kind='stored',run_id=run_id,ordinal=row['ordinal']),row['match_status'],row['values']['template_id'])
            for k,s in statuses.items():local[k][s]+=row['occurrence_count']
            local_transitions[transition]+=row['occurrence_count'];checks['stored_records']+=1
        metadata=document['review'];review_counts=Counter()
        if metadata and metadata['availability']=='available':
            base=Path(evidence['source_database']).parent
            path=base/metadata['log_reference'];manifest_path=base/metadata['manifest_reference']
            assert sha(path)==metadata['log_sha256'];manifest=json.loads(manifest_path.read_text());shard_bytes=path.read_bytes()
            assert manifest['lineage']['package_id']==selection['package_id']
            assert manifest['log_sha256']==metadata['log_sha256']
            review_files.append(dict(path=str(path),sha256=sha(path),manifest=str(manifest_path),manifest_sha256=sha(manifest_path)))
            emissions=manifest['emissions'];package_units={}
            for label,package in packages.items():
                raw=package.parse_file(path);units={}
                assert b''.join(e.native_bytes() for e in raw.emissions)==shard_bytes
                for unit in package.iter_units(raw):
                    prov=unit['provenance'];original=tuple(emissions[i]['ordinal'] for i in prov['emission_ordinals'])
                    key=(original,prov.get('message_ordinal'))
                    assert key not in units;units[key]=unit
                package_units[label]=units
            assert package_units['production'].keys()==package_units['candidate'].keys()
            for route in manifest['routes']:
                prov=route['provenance'];key=(tuple(prov['emission_ordinals']),prov.get('message_ordinal'))
                units={k:v[key] for k,v in package_units.items()}
                corresponding_units(units)
                unit=units['candidate'];review_counts[route['kind']]+=1
                if route['kind']=='unresolved_recovery':
                    assert unit['recovery_status']=='unresolved'
                    for k in packages:local[k]['unresolved_recovery']+=1;counts[k]['unresolved_recovery']+=1
                    local_transitions['unresolved_recovery -> unresolved_recovery']+=1;transitions['unresolved_recovery -> unresolved_recovery']+=1
                    checks['unresolved_recovery_units']+=1;continue
                assert route['kind']=='no_match' and unit['recovery_status']=='recovered'
                # Prove this recovered body is exactly the recorded original span.
                a,b=route['regions']['body']['span']
                containing=next(e for e in emissions if e['original_span'][0]<=a<=b<=e['original_span'][1])
                offset=containing['shard_span'][0]-containing['original_span'][0]
                assert shard_bytes[a+offset:b+offset].decode('utf-8','surrogateescape')==unit['body']['text']
                item=evaluate(units)
                statuses,transition=account(item,1,dict(kind='review',run_id=run_id,unit_index=route['unit_index'],emission_ordinals=list(key[0]),reason=route['reason']),route['kind'])
                for k,s in statuses.items():local[k][s]+=1
                local_transitions[transition]+=1;checks['review_no_match_occurrences']+=1
            assert dict(review_counts)==metadata['routing_counts']
        else:
            assert not metadata or metadata['unit_count']==0,'review evidence unavailable'
        runs.append(dict(run_id=run_id,in_candidate_training=info['log_sha256'] in evidence['training_hashes'],counts=local,transitions=local_transitions,review_routes=review_counts))
        print(run_id,json.dumps(local_transitions),flush=True)

    before={t['template_id']:t for t in packages['production'].data['templates']};after={t['template_id']:t for t in packages['candidate'].data['templates']}
    added=set(after)-set(before);removed=set(before)-set(after)
    edges={};removed_coverage={};capture_changes=[]
    for item in cache.values():
        old,new=item['results']['production'],item['results']['candidate'];n=item['occurrences']
        old_id=old['values']['template_id'] if old else None;new_id=new['values']['template_id'] if new else None
        pair=(old_id,new_id,old['status'] if old else 'no_match',new['status'] if new else 'no_match')
        edge=edges.setdefault(pair,dict(before=old_id,after=new_id,before_status=pair[2],after_status=pair[3],occurrences=0,distinct_messages=0,example_key=item['key']))
        edge['occurrences']+=n;edge['distinct_messages']+=1
        if old and new and captures(old)!=captures(new):
            old_locations=captures(old,'LOCATOR');new_locations=captures(new,'LOCATOR')
            capture_changes.append(dict(key=item['key'],occurrences=n,old= captures(old),new=captures(new),
                                       existing_locators_preserved=old_locations==[c for c in new_locations if c[2]!='Unknown'] or old_locations==new_locations))
    for identifier in sorted(removed):
        items=[e for e in edges.values() if e['before']==identifier]
        n=sum(e['occurrences'] for e in items);lost=sum(e['occurrences'] for e in items if e['after'] is None)
        downgraded=sum(e['occurrences'] for e in items if e['before_status']=='template' and e['after_status']=='provisional')
        category='not_observed' if not n else 'has_lost_matches' if lost else 'has_status_downgrades' if downgraded else 'covered_by_replacements'
        removed_coverage[identifier]=dict(category=category,occurrences=n,lost=lost,downgraded=downgraded,edges=items)
    checks['distinct_recovered_messages']=len(cache);checks['production_parity_mismatches']=len(parity)
    checks['reconstruction_failures']=0;checks['identity_collisions']=0
    checks['changed_capture_messages']=len(capture_changes)
    checks['messages_with_changed_locator_captures']=sum(not r['existing_locators_preserved'] for r in capture_changes)
    assert sha(Path(evidence['database']))==evidence['database_sha256']
    assert all(sha(root/p)==h for p,h in operation_guard.items())
    assert all(sha(Path(r['path']))==r['sha256'] and sha(Path(r['manifest']))==r['manifest_sha256'] for r in review_files)
    result=dict(production=selection,candidate=dict(package_id=packages['candidate'].manifest['package_id'],model=packages['candidate'].data['revision_id'],pin=args.candidate_pin),
                training={k:p.data['summary'] for k,p in packages.items()},training_comparison=training_comparison,
                counts=counts,transitions=transitions,checks=checks,runs=runs,
                inventory=dict(production=len(before),candidate=len(after),added=len(added),removed=len(removed),unchanged=len(set(before)&set(after))),
                added=sorted(added),removed=sorted(removed),removed_coverage=removed_coverage,edges=list(edges.values()),
                capture_changes=capture_changes,production_parity_mismatches=parity,review_files=review_files,
                database_backup_unchanged=True,production_selection_catalogs_unchanged=True,review_files_unchanged=True,
                historical_catalog_changes_before_comparison=historical_catalog_changes)
    result['parser_correspondence']=dict(parsers={k:p.manifest['parser'] for k,p in packages.items()},
        stored_regions='Each package lexed the genuine rendered stored regions; all native inputs equal.',
        review_shards='Each package parsed original authenticated shard bytes; recovery routes and native inputs equal.')
    if snapshot!=out:save(out/'production-before.json',operation_guard)
    save(out/'messages.json',list(cache.values()));save(out/'comparison.json',result)
    print(json.dumps({k:result[k] for k in ('counts','transitions','checks','inventory')},indent=2),flush=True)


if __name__=='__main__':main()
