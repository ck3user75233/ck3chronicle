"""Recovered-message measurement of variable trailing locations under shared wording.

Uses recovered native message bodies and the recorded package's location recognizer.
Template prefixes are measurement groups only, never complete assignments. No
inference, model changes, parser changes, recovery splitting or production writes.
"""
import argparse
from collections import Counter, defaultdict
from dataclasses import replace
import json
from pathlib import Path
import re

from template_learning.matcher_example import load_verified
from template_learning.matching_primitives import display_pattern, pattern_identity
from template_learning.records import identity


# Inventory expression only: full native file/line entries, optionally with a
# parenthetical trace. Does not supply a matching or parser/recovery rule.
ENTRY = re.compile(r'(?:infile|file):[ \t]+[^\r\n]+?[ \t]+(?:near line:|line:)'
                   r'[ \t]+[0-9]+(?:-[0-9]+)?(?:[ \t]+\([^\r\n]*\))?[ \t]*$')
FILE_LABEL = re.compile(r'(?<!\w)(?:infile|file):')


def trailing_entries(text):
    lines = text.splitlines(keepends=True)
    offset, spans = len(text), []
    for line in reversed(lines):
        offset -= len(line)
        clean = line.rstrip('\r\n')
        if not clean.strip(' \t'):
            continue
        matches = [m for m in FILE_LABEL.finditer(clean) if ENTRY.fullmatch(clean[m.start():])]
        if not matches:
            break
        match = matches[0]
        spans.append((offset + match.start(), offset + len(clean)))
        if clean[:match.start()].strip(' \t'):
            break
    if not spans:
        return None
    spans.reverse()
    return dict(count=len(spans), prefix=text[:spans[0][0]], entry_spans=spans)


def projected_prefixes(models):
    patterns = {}
    for origin, model in models:
        for template in model['templates']:
            if template['status'] == 'unresolved':
                continue
            for index, part in enumerate(template['parts']):
                if part['kind'] != 'literal' or 'alternatives' in part:
                    continue
                for found in FILE_LABEL.finditer(part['text']):
                    parts = pattern_identity(template['parts'][:index])
                    if found.start():
                        parts.append(dict(kind='literal', text=part['text'][:found.start()]))
                    if not parts:
                        continue
                    for n, p in enumerate(p for p in parts if p['kind'] == 'slot'):
                        p['name'] = 's' + str(n)
                    key = identity([template['source_family'], template['context_kind'], parts])[:24]
                    row = patterns.setdefault(key, dict(id=key, source=template['source_family'],
                        context_kind=template['context_kind'], parts=parts,
                        display=display_pattern(parts), definitions=[]))
                    ref = dict(model=origin, template_id=template['template_id'], status=template['status'])
                    if ref not in row['definitions']:
                        row['definitions'].append(ref)
    return patterns


def literal_subsequence_possible(parts, text):
    """Necessary literal-order check only; acceptance stays in the shared matcher."""
    cursor = 0
    for part in parts:
        if part['kind'] != 'literal':
            continue
        ends = [at + len(value) for value in part.get('alternatives', [part['text']])
                if (at := text.find(value, cursor)) >= 0]
        if not ends:
            return False
        cursor = min(ends)
    return True


def reader_annotations(package, inventory, output):
    """Inspect another observed location form without equating its full templates."""
    source = 'pdx_persistent_reader.cpp'
    # The pinned stream parser delegates these emissions to local recovery.
    # Filtering is safe here only because its cross-emission rule cannot apply.
    assert package.parser.CROSS_EMISSION_RULES['source_family'] != source
    templates = [t for t in package.data['templates'] if t['source_family'] == source
                 and t['context_kind'] == 'located-message-wrapper'
                 and '(expanded from file:' not in t['display']]
    rows, cache, counts = {}, {}, Counter()
    for number, item in enumerate(inventory['inputs'], 1):
        raw = package.parse_file(item['snapshot'])
        selected = replace(raw, emissions=tuple(e for e in raw.emissions if e.source_family == source))
        for unit in package.iter_units(selected):
            if unit['recovery_status'] != 'recovered':
                counts['unresolved'] += 1
                continue
            text = unit['body']['text']
            counts['messages'] += 1
            marker = ' (expanded from file:'
            prefix = text.split(marker, 1)[0]
            category = 'expanded' if marker in text else 'plain'
            if category == 'expanded' and re.search(r'\(expanded from file:[ \t]+line:', text):
                category = 'expanded_missing_filename'
            wrapper = ''.join(r['text'] for r in unit['contexts'].values())
            wrapper_missing = 'in file: ""' in wrapper
            counts[category] += 1
            counts['missing_wrapper_filename' if wrapper_missing else 'present_wrapper_filename'] += 1
            if prefix not in cache:
                end = len(prefix.encode('utf-8', 'surrogateescape'))
                cursor, pieces = 0, []
                for kind, value in unit['body']['pieces']:
                    cursor += len(value.encode('utf-8', 'surrogateescape'))
                    if cursor <= end:
                        pieces.append((kind, value))
                assert ''.join(t for _, t in pieces) == prefix
                cache[prefix] = [t for t in templates if package.matcher.rules.analyze_match_pattern(
                    t['parts'], prefix, pieces=tuple(pieces))['count'] == 1]
            if not cache[prefix]:
                counts['ungrouped'] += 1
            for template in cache[prefix]:
                row = rows.setdefault(template['template_id'], dict(template_id=template['template_id'],
                    display=template['display'], counts=Counter(), wrapper_counts=Counter(), examples={}))
                row['counts'][category] += 1
                row['wrapper_counts']['missing_filename' if wrapper_missing else 'present_filename'] += 1
                example_key = category + ('/missing_wrapper_filename' if wrapper_missing else '/present_wrapper_filename')
                row['examples'].setdefault(example_key, dict(text=text, contexts=unit['contexts'],
                    provenance=unit['provenance'], log_sha256=item['sha256'], path=item['snapshot']))
        if number % 20 == 0:
            print('Reader annotation review:', number, 'logs;', counts['messages'], 'messages', flush=True)
    result = dict(counts=counts, patterns=list(rows.values()),
        interpretation='Plain and expanded forms are different complete templates with extra literal location-annotation wording. They share the listed core pattern before that annotation. No optional annotation or new template is inferred.',
        method='Pinned parser recovery, same-source emissions only; exact native prefix pieces matched by existing base-template constraints; original wrapper context retained.')
    (output / 'reader-annotations.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(counts), flush=True)


def recovery_examples(package, inventory, output):
    """Retain original framing beside a few measured messages for manual review."""
    incidence = json.loads((output / 'incidence.json').read_text(encoding='utf-8'))
    target = next(f for f in incidence['families'] if
                  "did not get a matching scope type. Expected '<KEY>'" in f['pattern']['display'])
    result = dict(scope='Selected genuine examples, not an additional corpus census.', examples=[])

    def describe(label, recovery):
        parents = recovery.parents or (recovery.parent,)
        messages = []
        for message in recovery.messages:
            pieces = tuple((p.kind, p.text) for p in message.pieces)
            fields = package.matcher.rules.location_piece_ranges(pieces)
            messages.append(dict(text=message.text, span=[message.span.start, message.span.end],
                recognized_body_locators=[''.join(t for _, t in pieces[a:b]) for a, b in fields],
                continuations=[dict(text=e.message.text,
                    emission_ordinal=e.message.parent.ordinal) for e in message.continuations]))
        return dict(label=label, structure=recovery.structure, status=recovery.status,
            original_emissions=[dict(ordinal=e.ordinal, text=e.decoded_text,
                source=e.original.name, span=[e.span.start, e.span.end]) for e in parents],
            recovered_messages=messages)

    wrapper_found = False
    for count, example in sorted(target['examples'].items(), key=lambda kv:int(kv[0])):
        raw = package.parse_file(example['path'])
        ordinal, = example['provenance']['emission_ordinals']
        emission = next(e for e in raw.emissions if e.ordinal == ordinal)
        recovery = emission.recovery
        assert recovery.structure == 'script-error' and len(recovery.messages) == 1
        assert recovery.messages[0].text == example['text']
        row = describe('scope mismatch: ' + count + ' trailing entries', recovery)
        assert len(row['recovered_messages'][0]['recognized_body_locators']) == 2 * int(count)
        result['examples'].append(row)
        if not wrapper_found:
            for emission in raw.emissions:
                if emission.source_family != 'pdx_persistent_reader.cpp':
                    continue
                recovery = emission.recovery
                if recovery.structure == 'located-message-wrapper' and len(recovery.messages) > 1:
                    result['examples'].append(describe('existing wrapper split', recovery))
                    wrapper_found = True
                    break
    witness = package.parser.CROSS_EMISSION_RULES['evidence'][0]['sha256']
    item = next(i for i in inventory['inputs'] if i['sha256'] == witness)
    raw = package.parse_file(item['snapshot'])
    for recovery in raw.iter_recoveries():
        if recovery.status == 'recovered' and recovery.structure == package.parser.CROSS_EMISSION_RULES['id']:
            result['examples'].append(describe('existing attached continuation list', recovery))
            break
    (output / 'recovery-examples.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps([dict(label=e['label'], structure=e['structure'],
        emissions=len(e['original_emissions']), messages=len(e['recovered_messages']),
        body_locator_counts=[len(m['recognized_body_locators']) for m in e['recovered_messages']],
        attached_entries=[len(m['continuations']) for m in e['recovered_messages']])
        for e in result['examples']]), flush=True)


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--inventory', type=Path, required=True)
    cli.add_argument('--package', type=Path, required=True)
    cli.add_argument('--manifest-sha256', required=True)
    cli.add_argument('--additional-model', type=Path)
    cli.add_argument('--reader-annotations-only', action='store_true')
    cli.add_argument('--recovery-examples-only', action='store_true')
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    inventory = json.loads(args.inventory.read_text())
    package = load_verified(args.package, args.manifest_sha256)
    if args.recovery_examples_only:
        recovery_examples(package, inventory, args.output)
        return
    if args.reader_annotations_only:
        reader_annotations(package, inventory, args.output)
        return
    models = [(package.manifest['model_revision_id'], package.data)]
    if args.additional_model:
        model = json.loads(args.additional_model.read_text())
        models.append((model['revision_id'], model))
    patterns = projected_prefixes(models)
    by_source = defaultdict(list)
    for row in patterns.values():
        by_source[row['source']].append(row)
    rules = package.matcher.rules
    totals = Counter()
    sources = defaultdict(lambda: dict(messages=0, locator_fields=Counter(), file_fields=Counter(),
                                      trailing_entries=Counter()))
    families = {}
    cache, prefix_cache, unmatched, other_examples = {}, {}, {}, {}
    unique_pattern_memberships = Counter()
    logs = []
    for number, item in enumerate(inventory['inputs'], 1):
        raw = package.parse_file(item['snapshot'])
        for unit in package.iter_units(raw):
            if unit['recovery_status'] != 'recovered':
                totals['unresolved_recovery_units'] += 1
                continue
            text = unit['body']['text']
            key = (unit['source_family'], unit['context_kind'], text,
                   tuple((k, r['text']) for k, r in unit['contexts'].items()),
                   tuple(r['text'] for r in unit['continuations']))
            if key not in cache:
                pieces = tuple(map(tuple, unit['body']['pieces']))
                values = []
                for region in [unit['body'], *unit['contexts'].values(), *unit['continuations']]:
                    region_pieces = tuple(map(tuple, region['pieces']))
                    locations = rules.location_piece_ranges(region_pieces)
                    values.extend(''.join(t for _, t in region_pieces[a:b]) for a, b in locations)
                file_count = sum(not re.fullmatch(r'[0-9]+(?:-[0-9]+)?', v) for v in values)
                tail = trailing_entries(text)
                matches = []
                if tail:
                    prefix = tail['prefix']
                    prefix_key = (unit['source_family'], unit['context_kind'], prefix)
                    end = len(prefix.encode('utf-8', 'surrogateescape'))
                    prefix_pieces, cursor = [], 0
                    for piece in pieces:
                        cursor += len(piece[1].encode('utf-8', 'surrogateescape'))
                        if cursor <= end:
                            prefix_pieces.append(piece)
                    prefix_pieces = tuple(prefix_pieces)
                    if ''.join(t for _, t in prefix_pieces) != prefix:
                        tail['boundary_error'] = True
                    elif prefix_key in prefix_cache:
                        matches = prefix_cache[prefix_key]
                    else:
                        for pattern in by_source[unit['source_family']]:
                            if pattern['context_kind'] != unit['context_kind']:
                                continue
                            if not literal_subsequence_possible(pattern['parts'], prefix):
                                continue
                            assessment = rules.analyze_match_pattern(pattern['parts'], prefix, pieces=prefix_pieces)
                            if assessment['count'] == 1:
                                matches.append(pattern['id'])
                        prefix_cache[prefix_key] = matches
                cache[key] = dict(fields=len(values), files=file_count, tail=tail, patterns=matches)
            measured = cache[key]
            source = sources[unit['source_tag']]
            totals['messages'] += 1
            source['messages'] += 1
            source['locator_fields'][measured['fields']] += 1
            source['file_fields'][measured['files']] += 1
            if measured['fields']:
                totals['messages_with_recognized_locator_fields'] += 1
            if measured['files'] > 1:
                totals['messages_with_multiple_file_fields'] += 1
            tail = measured['tail']
            count = tail['count'] if tail else 0
            source['trailing_entries'][count] += 1
            example = dict(log_sha256=item['sha256'], path=item['snapshot'],
                source_tag=unit['source_tag'], context_kind=unit['context_kind'],
                provenance=unit['provenance'], text=text, contexts=unit['contexts'],
                recognized_locator_fields=measured['fields'], recognized_file_fields=measured['files'])
            if tail:
                totals['messages_with_trailing_location_entries'] += 1
                if count > 1:
                    totals['messages_with_multiple_trailing_entries'] += 1
                if not measured['patterns']:
                    totals['trailing_messages_without_template_prefix_group'] += 1
                    unmatched.setdefault((unit['source_tag'], count), example)
                unique_pattern_memberships[(tuple(measured['patterns']), count, unit['source_tag'])] += 1
                for pattern_id in measured['patterns']:
                    row = families.setdefault(pattern_id, dict(pattern=patterns[pattern_id],
                        counts=Counter(), sources=Counter(), logs=set(), distinct_bodies=set(),
                        literal_prefixes=set(), examples={}))
                    row['counts'][count] += 1
                    row['sources'][unit['source_tag']] += 1
                    row['logs'].add(item['sha256'])
                    row['distinct_bodies'].add(identity(key))
                    row['literal_prefixes'].add(tail['prefix'])
                    row['examples'].setdefault(count, example)
            elif measured['files'] > 1 or measured['fields'] > 2:
                other_examples.setdefault((unit['source_tag'], measured['fields'], measured['files']), example)
        logs.append(dict(sha256=item['sha256'], emissions=len(raw.emissions), bytes=len(raw.source.data)))
        print(f'{number}/{len(inventory["inputs"])} logs; {totals["messages"]} messages; {len(cache)} distinct contextual observations', flush=True)
        (args.output / 'progress.json').write_text(json.dumps(dict(logs=len(logs), totals=totals)), encoding='utf-8')
    output_families = []
    variable_covered, variable_sources = Counter(), Counter()
    for row in families.values():
        row['variable_count'] = len(row['counts']) > 1
        row['logs'] = sorted(row['logs'])
        row['distinct_bodies'] = len(row['distinct_bodies'])
        row['distinct_literal_prefixes'] = len(row.pop('literal_prefixes'))
        output_families.append(row)
    variable_ids = {r['pattern']['id'] for r in output_families if r['variable_count']}
    for (memberships, count, source), occurrences in unique_pattern_memberships.items():
        if variable_ids.intersection(memberships):
            variable_covered[count] += occurrences
            variable_sources[source] += occurrences
    output = dict(scope=inventory['scope'], inaccessible=inventory.get('inaccessible', inventory.get('errors', [])),
        models=[m[0] for m in models], parser=package.manifest['parser'], logs=logs, totals=totals,
        unique_contextual_messages=len(cache), source_tags=sources,
        variable_family_message_counts=variable_covered, variable_family_sources=variable_sources,
        families=sorted(output_families, key=lambda r:(not r['variable_count'], -sum(r['counts'].values()))),
        variable_family_count=len(variable_ids), unmatched_prefix_examples=list(unmatched.values()),
        other_multilocation_examples=list(other_examples.values()),
        limitations=['Counts are parser-recovered error messages; original emission provenance remains attached.',
          'Family groups match exact literal/slot prefix parts projected from the named models; slot values may vary.',
          'Location counts are not part of prefix grouping. This is not complete template matching or new classification.',
          'Projected prefix groups can overlap; their occurrence totals must not be summed.',
          'Trailing entry census covers complete file:/infile: plus line:/near line: entry lines and optional parentheticals.',
          'Other locator layouts are inventoried separately; absent prefix matches and ambiguous prefix matches are not forced into families.'])
    (args.output / 'incidence.json').write_text(json.dumps(output, indent=2), encoding='utf-8')
    print(json.dumps(dict(totals=totals, variable_families=len(variable_ids))), flush=True)


if __name__ == '__main__':
    main()
