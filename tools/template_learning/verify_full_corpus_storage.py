"""Verify storage changes against the preserved genuine 73-log v53 result."""
import argparse
from collections import Counter
import json
from pathlib import Path

from template_learning.evidence_serialization import write_json
from template_learning.inventory import sha256_file
from template_learning.refinement_history import validate_history


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--before', type=Path, required=True, help='Stopped v53 experiment directory.')
    cli.add_argument('--after', type=Path, required=True)
    args = cli.parse_args()
    old_release = args.before/'recovered-release'
    old_completion = json.loads((old_release/'completion.json').read_text())
    assert sha256_file(old_release/'manifest.json') == old_completion['manifest_sha256']
    old_manifest = json.loads((old_release/'manifest.json').read_text())
    old_path = old_release/'empirical_template_model.json'
    assert sha256_file(old_path) == old_manifest['hashes'][old_path.name]
    old = json.loads(old_path.read_text())
    package_manifest, = (args.after/'packages').glob('*/manifest.json')
    manifest = json.loads(package_manifest.read_text())
    path = package_manifest.parent/'empirical_template_model.json'
    assert sha256_file(path) == manifest['hashes'][path.name]
    current = json.loads(path.read_text())
    assert old['templates'] == current['templates'], 'storage changes altered executable definitions'
    assert old['summary'] == current['summary']
    assert old['training_evidence'] == current['training_evidence']
    bundle_manifest, = (args.after/'candidate').glob('*/manifest.json')
    bundle = bundle_manifest.parent
    old_bundle = args.before/'candidate'/old['source_candidate_revision']
    old_native = json.loads((old_bundle/'manifest.json').read_text())['hashes']['native_evidence.json']
    new_native = json.loads(bundle_manifest.read_text())['hashes']['native_evidence.json']
    assert old_native == new_native == sha256_file(bundle/'native_evidence.json')
    model_path = bundle/'empirical_template_model.json'
    assert sha256_file(model_path) == json.loads(bundle_manifest.read_text())['hashes'][model_path.name]
    with model_path.open(encoding='utf-8') as stream:
        model = json.load(stream)
    validate_history(model)
    table = model['refinement_history']
    references = Counter(parent for event in table.values() for parent in event['parents'])
    observations = sorted((dict(event_id=key, values=len(event['delta']['observed_values']),
                               child_references=references[key])
                           for key, event in table.items() if 'observed_values' in event['delta']),
                          key=lambda row: -row['values'])
    assert all('observed_values' not in event['delta'] and 'values' not in event['delta']
               for event in table.values() if 'retained_value' in event['delta'])
    journal = [json.loads(line) for line in (args.after/'learner-memory.jsonl').read_text().splitlines()]
    result = dict(executable_definitions_identical_to_v53=True, native_assignment_evidence_byte_identical=True,
        original_source_revision=old['source_candidate_revision'], candidate_source_revision=model['revision_id'],
        templates=len(current['templates']), native_evidence_sha256=new_native,
        original_research_model_bytes=(old_bundle/'empirical_template_model.json').stat().st_size,
        corrected_research_model_bytes=model_path.stat().st_size,
        history_events=len(table), largest_split_observations=observations[:5],
        sampled_peak_private_bytes=max(row['private_bytes'] for row in journal),
        process_peak_working_set_bytes=max(row['peak_working_set_bytes'] for row in journal),
        memory_scope='Learner process; 15-second sampling for private memory. Separate publication process excluded.',
        control='Same 73 genuine input hashes; history storage changes preserve executable definitions and complete native assignments.')
    write_json(args.after/'history-storage-verification.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
