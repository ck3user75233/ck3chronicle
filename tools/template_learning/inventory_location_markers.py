"""Inventory location-label mentions in genuine logs; not a recognition rule.

Counts physical marker mentions, not messages or selected slot assignments.
Contextual examples are retained for review; no input or model is modified.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re


MARKER = re.compile(rb'(?<![A-Za-z0-9_])(?:Script location|Stack trace|New Location|Previous Location|'
                    rb'Location|From|Near file|In file|infile|file|Near line|lines|line|Database):[ \t]*', re.I)
SENTINEL = re.compile(rb'''["']?(?:unknown|none|null|n/a|<unknown>|<none>|<null>|\(unknown\)|\(none\)|\(null\)|\?)(?=[\s"']|$)''', re.I)


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--inventory', type=Path, required=True)
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args()
    inventory = json.loads(args.inventory.read_text(encoding='utf-8'))
    markers, sentinel_forms = {}, {}
    for number, item in enumerate(inventory['inputs'], 1):
        data = Path(item['snapshot']).read_bytes()
        for match in MARKER.finditer(data):
            label = match.group().rstrip(b' \t').decode('ascii')
            row = markers.setdefault(label, dict(count=0, shapes=Counter(), examples={}))
            row['count'] += 1
            end = data.find(b'\n', match.end())
            end = len(data) if end < 0 else end
            tail = data[match.end():end].rstrip(b'\r')
            if not tail:
                shape = 'no value on this physical line'
            elif re.match(rb'''(?:["']{2}|["'][ \t]*["'])(?:\s|$)''', tail):
                shape = 'empty quoted value'
            elif SENTINEL.match(tail):
                shape = 'unavailable-value candidate'
            elif re.match(rb'''["']?(?:file|infile):''', tail, re.I):
                shape = 'file/line entry follows'
            elif re.match(rb'[0-9]+(?:-[0-9]+)?(?:\s|[)"\']|$)', tail):
                shape = 'numeric value follows'
            else:
                shape = 'other nonempty value'
            row['shapes'][shape] += 1
            example = None
            if shape not in row['examples'] or shape == 'unavailable-value candidate':
                line_start = data.rfind(b'\n', 0, match.start()) + 1
                example = dict(log_sha256=item['sha256'], path=item['snapshot'],
                    marker_span=[match.start(), match.end()],
                    native_line=data[line_start:end].decode('utf-8', 'surrogateescape'),
                    value_tail=tail.decode('utf-8', 'surrogateescape'))
                row['examples'].setdefault(shape, example)
            if shape == 'unavailable-value candidate':
                key = label, tail.decode('utf-8', 'surrogateescape')
                found = sentinel_forms.setdefault(key, dict(marker=label, native_value_tail=key[1], count=0, example=example))
                found['count'] += 1
        if number % 20 == 0:
            print(number, 'logs inventoried', flush=True)
    result = dict(scope=inventory['scope'], log_count=len(inventory['inputs']),
        bytes=sum(i['bytes'] for i in inventory['inputs']), access_errors=len(inventory['errors']),
        markers=markers, unavailable_candidates=list(sentinel_forms.values()),
        limitations=['Raw marker mentions, not independently recovered-message counts.',
                    'The listed marker and unavailable-value expressions are inventory probes, not an exhaustive grammar or matcher implementation.',
                    'Blank labels and empty quoted values are distinct from an explicitly emitted Unknown value.',
                    'Examples require contextual review; diagnostic wording such as Unknown trigger is not classified as a locator by this inventory.'])
    args.output.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(dict(markers={k:dict(count=v['count'], shapes=v['shapes']) for k,v in markers.items()},
        unavailable=[dict(marker=r['marker'], value=r['native_value_tail'], count=r['count']) for r in sentinel_forms.values()]), indent=2))


if __name__ == '__main__':
    main()
