"""Compare a history-only learner change using two genuine candidate bundles."""
import argparse
from collections import Counter
import json
from pathlib import Path

from template_learning.evidence_serialization import inspect_bundle, json_identity, write_json
from template_learning.publish_native_model import compact_template
from template_learning.refinement_history import validate_history


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--baseline', type=Path, required=True)
    cli.add_argument('--candidate', type=Path, required=True)
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args()
    old, new = inspect_bundle(args.baseline), inspect_bundle(args.candidate)
    before, after = old['model'], new['model']
    assert before['evidence'] == after['evidence'], 'control training inputs differ'
    assert before['summary'] == after['summary'], 'learning outcomes changed'
    assert [compact_template(t) for t in before['templates']] == [compact_template(t) for t in after['templates']], 'executable definitions changed'
    assert old['manifest']['hashes']['native_evidence.json'] == new['manifest']['hashes']['native_evidence.json'], 'native assignments/captures/provenance changed'
    assert after['revision_id'] == json_identity({k: v for k, v in after.items() if k != 'revision_id'})[:24]
    validate_history(after)
    table = after['refinement_history']
    children = Counter(parent for event in table.values() for parent in event['parents'])
    observations = [dict(event_id=key, values=len(event['delta'].get('observed_values', event['delta'].get('values', []))),
                         children=children[key]) for key, event in table.items()
                    if 'observed_values' in event['delta'] or 'values' in event['delta']]
    # A split's alternatives belong to its parent observation, never its child.
    retained = [event for event in table.values() if 'retained_value' in event['delta']]
    assert all('values' not in event['delta'] and 'observed_values' not in event['delta'] for event in retained)
    result = dict(baseline_revision=before['revision_id'], candidate_revision=after['revision_id'],
        genuine_logs=len(after['evidence']), summary=after['summary'],
        executable_templates_equal=True, native_evidence_byte_identical=True,
        native_evidence_sha256=new['manifest']['hashes']['native_evidence.json'],
        valid_lineage=True, history_events=len(table), child_delta_events=len(retained),
        shared_observations=sorted(observations, key=lambda row: -row['values']),
        baseline_model_bytes=(args.baseline/'empirical_template_model.json').stat().st_size,
        candidate_model_bytes=(args.candidate/'empirical_template_model.json').stat().st_size)
    write_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
