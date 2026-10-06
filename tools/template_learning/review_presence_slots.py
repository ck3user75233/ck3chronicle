"""Inspect genuine changed assignments for KEY-to-literal selection changes."""
import argparse
import json
from pathlib import Path

from template_learning.location_candidate_experiment import save, sha
from template_learning.matcher_example import load_verified
from template_learning.verify_location_candidate import stored_unit


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--experiment', type=Path, required=True)
    cli.add_argument('--previous', type=Path, required=True)
    args = cli.parse_args()
    out = args.experiment.resolve()
    report = json.loads((out/'verification.json').read_text())
    manifest, = (out/'packages').glob('*/manifest.json')
    package = load_verified(manifest.parent, sha(manifest))
    old_path, = (args.previous/'packages').glob('*/empirical_template_model.json')
    old = {t['template_id']:t for t in json.loads(old_path.read_text())['templates']}
    new = package.matcher.by_id
    def key_count(t):
        return sum(p.get('type') == 'KEY' for p in t['parts'])
    rows = []
    for change in report['assignment_changes']:
        before, after = change['before'], change['after']
        if not before or not after or key_count(old[before]) <= key_count(new[after]):
            continue
        document = json.loads((out/(change['run_id']+'.json')).read_text())
        row = next(r for r in document['records'] if r['ordinal'] == change['ordinal'])
        unit = stored_unit(package, row)
        result = package.match(unit, inspect=True)
        assert result['assignment']['template_id'] == after
        alternatives = [dict(template_id=m['template_id'], display=new[m['template_id']]['display'],
                             status=new[m['template_id']]['status'])
                        for m in result['inspection']['matches']
                        if key_count(new[m['template_id']]) >= key_count(old[before])]
        rows.append(dict(**change, before_display=old[before]['display'],
                         after_display=new[after]['display'], complete_key_alternatives=alternatives,
                         selection=result['assignment']['selection']))
    result = dict(scope='All changed assignment pairs losing a body KEY; alternatives inspected on one genuine stored representative per pair.',
                  pairs=len(rows), occurrences=sum(r['occurrences'] for r in rows),
                  all_representatives_retain_complete_key_alternative=all(r['complete_key_alternatives'] for r in rows),
                  rows=rows)
    save(out/'slot-selection-review.json', result)
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}, indent=2))


if __name__ == '__main__':
    main()
