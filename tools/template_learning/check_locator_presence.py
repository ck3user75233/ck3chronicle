"""Verify locator-presence similarity on genuine retained messages only."""
import argparse
import json
from pathlib import Path

from template_learning.clustering import learning_tokens, sequence_similarity, comparable, cluster_source_records
from template_learning.location_sequences import sequence
from template_learning.records import SequenceRecord
from template_learning.matcher_example import load_verified
from template_learning.verify_location_candidate import region
from template_learning.location_candidate_experiment import save,sha
from ck3chronicle.pipeline.contracts import render_regions


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--root',type=Path,required=True)
    cli.add_argument('--output',type=Path,required=True)
    args=cli.parse_args()
    root=args.root.resolve(); output=args.output.resolve()
    previous=root/'.codex-tmp/locator-marker-candidate'
    package_path,=(previous/'packages').glob('*/manifest.json')
    package=load_verified(package_path.parent,sha(package_path))
    def native(text,source):
        return SequenceRecord(source,text,tuple(map(tuple,region(package.parser,text)['pieces'])))
    def present_units(record,parts=None):
        units=learning_tokens(record,parts)
        return units,sum(u==('field','LOCATOR') for u in units)
    trace=json.loads((root/'.codex-tmp/effect-regression-review/trace.json').read_text())
    effects=[native(row['text'],'jomini_script_system.cpp') for row in trace['native_examples']]
    initial=[learning_tokens(r) for r in effects]
    assert sequence_similarity(*initial)==.775
    assert comparable(*initial,.72)
    assert all(units[-1]==('field','LOCATOR') and units.count(('field','LOCATOR'))==1 for units in initial)
    clusters=cluster_source_records('jomini_script_system.cpp',effects,.72)
    assert len(clusters)==1 and not clusters[0].failures
    assert sum(p.get('type')=='KEY' for p in clusters[0].parts)==1
    examples=json.loads((root/'.codex-tmp/location-variability-review/recovery-examples.json').read_text())
    witnesses=[]
    for row in examples['examples']:
        if not row['label'].startswith('scope mismatch'):
            continue
        record=native(row['recovered_messages'][0]['text'],'jomini_script_system.cpp')
        parts=package.matcher.by_id['0213bb363ad56f39d7e953a5']['parts']
        initial_units,count=present_units(record)
        accepted_units,accepted_count=present_units(record,parts)
        assert count==accepted_count==1
        assert accepted_units.count(('field','KEY'))==3
        witnesses.append(dict(label=row['label'],entries=len(sequence(record.pieces)['entries']),
            initial_units=initial_units,accepted_units=accepted_units))
    assert len(witnesses)==3 and len({repr(w['accepted_units']) for w in witnesses})==1
    verification=json.loads((previous/'verification.json').read_text())
    travel=verification['targets'][1]
    record=native(travel['text'],'jomini_effect_impl.cpp')
    assert sequence(record.pieces) is None
    parts=package.matcher.by_id[travel['assignment']['values']['template_id']]['parts']
    assert present_units(record,parts)[1]==2  # Non-trailing LOCATORs stay individual.
    controls={}
    for run in json.loads((previous/'stored-evidence.json').read_text())['runs']:
        if len(controls)==2:
            break
        for row in json.loads((previous/(run['run_id']+'.json')).read_text())['records']:
            text=dict(render_regions(row['definition'],row['values']))['body']
            if 'unknown' not in controls and text.rstrip().endswith('Script location: Unknown'):
                record=native(text,row['source_family'])
                assert sequence(record.pieces) and present_units(record)[1]==1
                controls['unknown']=dict(run_id=run['run_id'],ordinal=row['ordinal'],units=learning_tokens(record))
            if 'absent' not in controls and 'location' not in text.lower() and 'file:' not in text.lower():
                record=native(text,row['source_family'])
                if present_units(record)[1]==0:
                    assert sequence(record.pieces) is None
                    controls['absent']=dict(run_id=run['run_id'],ordinal=row['ordinal'],text=text,units=learning_tokens(record))
            if len(controls)==2:
                break
    assert len(controls)==2
    save(output/'presence-check.json',dict(effect_initial_units=initial,effect_score=sequence_similarity(*initial),
        effect_pair_clusters=len(clusters),count_witnesses=witnesses,controls=controls,
        three_key_positions_preserved=True,non_trailing_locator_positions=2,
        threshold=.72,variable_threshold_used=False))
    print('Genuine presence checks passed: 0 versus 1/2/3 entries, Unknown, three separate KEY positions, two non-trailing LOCATOR positions. Effect pair score:',sequence_similarity(*initial),flush=True)


if __name__=='__main__':
    main()
