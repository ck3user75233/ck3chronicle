"""Build a navigable review bundle from saved, evidence-labelled root-CLI results.

No database access or investigation rerun. The original exports stay unchanged;
reading copies add explicit check descriptions and links to their actual outcomes.
"""
import argparse
from copy import deepcopy
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
from urllib.parse import quote, unquote, urlsplit
import xml.etree.ElementTree as ET

from ck3chronicle.reporting.presentation import render_html, _page, _el, _link, _table
from ck3chronicle.reporting.explanation import explain


class Links(HTMLParser):
    def __init__(self, value):
        super().__init__()
        self.ids, self.links = set(), []
        self.feed(value)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'a':
            self.links.append(attrs.get('href', ''))


def _argument(command, flag):
    values = [command[index + 1] for index, part in enumerate(command[:-1]) if part == flag]
    return values[-1] if values else None


def _request(command):
    operation = 'report' if 'report' in command else 'runs'
    return {'operation': operation,
            'run': command[command.index('report') + 1] if operation == 'report' else None,
            **{name: _argument(command, '--' + name.replace('_', '-'))
               for name in ('package_id', 'preset', 'database', 'query')}}


def _actions(parent, href):
    node = _el(parent, 'div', class_='example-actions')
    node.append(_link('Read explanation and evidence →', href + '#explanation'))


def _outcomes(status, included, results, catalog):
    page = ET.Element('main')
    _el(page, 'nav').append(_link('Back to the investigations', 'examples.html'))
    _el(page, 'h1', '08B: what happened to the incomplete items?')
    sections = _el(page, 'nav', class_='investigation-nav')
    sections.append(_link('Earlier assessment: every item', '#earlier-assessment'))
    sections.append(_link('Failed / empty queries: expected and actual outcomes', '#query-outcomes'))
    sections.append(_link('Completed corrections', '#completed'))
    sections.append(_link('Still unverified', '#unverified'))
    _el(page, 'p', 'Reviewed ' + status['updated'], class_='meta')
    _el(page, 'p', status['summary'], class_='notice')
    _el(page, 'p', f'{len(status["unverified"])} specific runtime fault paths were not encountered in the available checks. '
        'A saved error response can be the expected result of a checked request; it does not by itself mean an unfinished deliverable. '
        'The rows below separate the query outcome from the state of the work. This page reuses saved CLI results and does not claim new execution of those queries.')

    def examples(names):
        node = ET.Element('div')
        for name in names:
            if name in included:
                _el(node, 'p').append(_link(name + ' — explanation and actual result',
                                         'investigations/' + quote(name) + '.html#explanation'))
            else:
                _el(node, 'p', name + ' (not included in this bundle)')
        if not names:
            _el(node, 'p', 'No individual diagnostic report for this item.')
        return node

    _el(page, 'h2', 'Earlier assessment — disposition of every review item', id='earlier-assessment')
    _table(page, ['Earlier item', 'Current status', 'What happened / what remains', 'Results'], [
        [row['id'] + '\n' + row['item'], row['status'], row['outcome'], examples(row['examples'])]
        for row in status['earlier_assessment']])
    _el(page, 'h2', 'Runtime fault paths not exercised', id='unverified')
    _el(page, 'p', 'These are limits on executed verification, not missing data or empty-query outcomes. The operations and inspected handling are identified below.', class_='notice')
    _table(page, ['Operation not exercised with a fault', 'What the available evidence establishes', 'Follow-up if encountered'], [
        [row['item'], row['available'], row['needed']] for row in status['unverified']])

    _el(page, 'h2', 'Failed / empty queries — expected behavior and actual saved outcomes', id='query-outcomes')
    _el(page, 'p', 'Each case name opens its explanation and result together. The old names are retained so earlier comments can be traced; '
        'for example, required-partial now completes successfully. Earlier incorrect expectations are explicitly identified below.')
    rows = []
    for row in status['query_outcomes']:
        name = row['case']
        assert name in included, ('missing query-outcome case', name)
        actual, definition = results[name], catalog[name]
        assert actual['status'] == row['expected_status'], (name, actual)
        assert actual['exit'] == row['expected_exit'], (name, actual)
        if 'expected_records' in row:
            assert actual['records'] == row['expected_records'], (name, actual)
        if 'expected_stage' in row:
            assert actual['stage'] == row['expected_stage'], (name, actual)
        case = ET.Element('div', id='outcome-' + name)
        case.append(_link(name, 'investigations/' + quote(name) + '.html#explanation'))
        if definition.get('evidence_kind') == 'synthetic':
            _el(case, 'p', 'Authorized synthetic fixture')
        expected = ET.Element('div')
        _el(expected, 'p', definition['question'])
        _el(expected, 'p', 'Expected: ' + definition['expected'])
        result = ET.Element('div')
        if actual['status'] == 'completed':
            _el(result, 'p', f'{actual["records"]} diagnostic(s), {actual["occurrences"]} occurrence(s).')
        else:
            _el(result, 'p', actual['error'])
        _el(result, 'p', f'CLI exit {actual["exit"]} · {actual["status"]}', class_='meta')
        if actual['stage']:
            _el(result, 'p', 'Stage: ' + actual['stage'], class_='meta')
        disposition = ET.Element('div')
        _el(disposition, 'strong', row['status'])
        _el(disposition, 'p', row['disposition'])
        rows.append([case, expected, result, disposition])
    _table(page, ['Case / open report', 'Query and expected behavior', 'Actual saved result', 'Work status'], rows)

    _el(page, 'h2', 'Completed corrections — supporting detail', id='completed')
    _table(page, ['Earlier incomplete item', 'What was completed', 'Where to see it'], [
        [row['item'], row['outcome'], examples(row['examples'])] for row in status['completed']])
    _el(page, 'p', status['boundary'])
    return _page('08B delivery status and remaining gaps', page)


def build(evidence, output, featured_commands=()):
    definitions = Path(__file__).resolve().parents[1] / 'examples/reporting'
    catalog = json.loads((definitions / 'checks.json').read_bytes())
    delivery = json.loads((definitions / 'delivery-status.json').read_bytes())
    destination = output / 'investigations'
    destination.mkdir(parents=True, exist_ok=True)
    pages, rows, expected_targets, results = {}, [], [], {}
    calls = json.loads((evidence / 'commands.json').read_bytes())
    for manifest in featured_commands:
        value = json.loads(manifest.read_bytes())
        calls.extend(value if isinstance(value, list) else [value])
    included = set()
    for call in calls:
        command = call['command']
        output_argument = _argument(command, '--output')
        if output_argument is None:
            continue
        path = Path(output_argument)
        if path.suffix != '.json':
            continue
        if path.stem in included:
            continue
        case = catalog[path.stem]
        if case.get('withdrawn'):
            page = ET.Element('main', id='explanation')
            _el(page, 'h1', 'Withdrawn example')
            _el(page, 'p', case['withdrawn'])
            _el(page, 'p').append(_link('Read the whole-message search and its actual result', 'message-context-switch.html#explanation'))
            _el(page, 'p').append(_link('Back to current investigations', '../examples.html'))
            retired = destination / (path.stem + '.html')
            retired.write_text(_page('Withdrawn example', page), encoding='utf-8')
            pages[retired] = Links(retired.read_text(encoding='utf-8'))
            continue
        included.add(path.stem)
        if (destination / path.name).resolve() == path.resolve():
            raise ValueError('reading copies must not overwrite original CLI exports')
        original = json.loads(path.read_bytes())
        results[path.stem] = {'status': original['status'], 'exit': call['returncode'],
            'records': original.get('totals', {}).get('distinct_records'),
            'occurrences': original.get('totals', {}).get('occurrences'),
            'stage': original.get('failure_stage'), 'error': original.get('error')}
        payload = deepcopy(original)
        payload['explanation'] = explain(payload, requested_run=_request(command)['run'])
        payload['explanation'].update(question=case['question'], expected=[case['expected']])
        payload['example'] = {'name': path.stem, 'source': str(path), 'cli_exit_code': call['returncode'],
                              'evidence_kind': case.get('evidence_kind', 'genuine'),
                              'guide_href': '../examples.html#case-' + quote(path.stem),
                              'outcomes_href': '../outcomes.html',
                              'data_href': quote(path.name), 'request': _request(command),
                              'note': 'Reading copy of root-CLI data; analytical fields unchanged.'}
        if call.get('attachments'):
            attachments = destination / 'attachments' / path.stem
            attachments.mkdir(parents=True, exist_ok=True)
            payload['example']['attachments'] = []
            for item in call['attachments']:
                source = Path(item['path'])
                target = attachments / source.name
                shutil.copyfile(source, target)
                assert target.read_bytes() == source.read_bytes()
                payload['example']['attachments'].append({'label': item['label'],
                    'href': target.relative_to(destination).as_posix()})
        main_name = path.stem + '.html'
        appendix_name = path.stem + '-sources.html'
        main, appendix = render_html(payload, report_name=main_name, appendix_name=appendix_name)
        (destination / main_name).write_text(main, encoding='utf-8', newline='\n')
        (destination / path.name).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8', newline='\n')
        pages[destination / main_name] = Links(main)
        if appendix is not None:
            (destination / appendix_name).write_text(appendix, encoding='utf-8', newline='\n')
            pages[destination / appendix_name] = Links(appendix)
        assert {k: v for k, v in payload.items() if k not in {'explanation', 'example'}} == {
            k: v for k, v in original.items() if k not in {'explanation', 'example'}}
        href = 'investigations/' + quote(main_name)
        title = ET.Element('div', {'id': 'case-' + path.stem})
        title.append(_link(path.stem, href + '#explanation'))
        if case.get('evidence_kind') == 'synthetic':
            _el(title, 'p', 'Synthetic fixture', class_='notice')
        result = ET.Element('div')
        _el(result, 'p', ' '.join(payload['explanation']['result']))
        _el(result, 'p', f'CLI exit {call["returncode"]} · {payload["status"]}', class_='meta')
        _actions(result, href)
        rows.append([title, case['question'], result])
        expected_targets.append((destination / main_name, 'explanation'))
        print('Prepared:', path.stem, flush=True)

    index = ET.Element('main')
    _el(index, 'h1', '08B investigations and their results')
    status_link = _el(index, 'section', class_='reading-guide')
    _el(status_link, 'h2', 'What happened to the earlier incomplete deliverables?')
    _el(status_link, 'p', 'Ordinary path filtering returns recorded matches. A separate resolution filter finds recorded paths with no current file in the chosen roots. The examples and status page show both behaviors and the remaining evidence gaps.')
    _el(status_link, 'p').append(_link('Read the item-by-item delivery status and remaining gaps', 'outcomes.html'))
    _el(index, 'p', 'These examples use genuine stored CK3 records and current source files, plus a separately labelled owner-authorized synthetic source-path fixture. '
        'Each page explains the query, what it checks and the actual CLI outcome. Some checks deliberately return an empty set or report unavailable evidence.', class_='notice')
    _el(index, 'p', 'Click an investigation to read its explanation, actual result and supporting evidence together. '
        'The report shows the relevant template, Run counts or diagnostics immediately below the explanation. '
        'Named evidence links take you directly to further details or the referenced source line.')
    _el(index, 'h2', 'Start here')
    for name, title in (('message-unrecognized', 'Search the whole diagnostic for unrecognized'),
                        ('message-context-switch', 'The same content search finds populated REASON values'),
                        ('history-positions', 'Every requested history position, including unavailable Runs'),
                        ('stored-data-io', 'Stored-data reporting: file-access trace'),
                        ('relative-path-all-members', 'One relative path across every recorded playset member'),
                        ('pathless-emission', 'A complete emission with no source path'),
                        ('recursion-scoped-report', 'Source recursion and actual file/folder counts'),
                        ('unresolved-genuine-paths', 'Recorded paths with no current file in the selected roots'),
                        ('synthetic-unresolved-paths', 'Unresolved-path selector: two-entry fixture (synthetic)'),
                        ('file-path-all', 'All diagnostics referencing one path'),
                        ('synthetic-missing-files', 'Two-entry missing-file fixture (synthetic)'),
                        ('worked-five-runs', 'Failed context switches across five genuine Runs'),
                        ('template-only', 'Whole trigger-error template'),
                        ('worked-full', 'Earlier four-Run context-switch example')):
        if name not in included:
            continue
        section = _el(index, 'section', class_='diagnostic')
        _el(section, 'h3', title)
        _el(section, 'p', catalog[name]['question'])
        _actions(section, 'investigations/' + name + '.html')
    _el(index, 'p', 'Short/full worked reports differ only in display limits. Text, JSON and HTML are formats of the same analysis.')
    _el(index, 'h2', 'Individual checks')
    _table(index, ['Investigation', 'What it checks', 'Actual outcome and report'], rows)
    _el(index, 'h2', 'Checks without a diagnostic report')
    _el(index, 'p', 'The CLI group also checks existing command help and rejection of HTML without an explicit destination. '
        'These exercise command integration and argument handling.')
    index_html = _page('08B investigations and results', index)
    (output / 'examples.html').write_text(index_html, encoding='utf-8', newline='\n')
    pages[output / 'examples.html'] = Links(index_html)
    outcomes_html = _outcomes(delivery, included, results, catalog)
    (output / 'outcomes.html').write_text(outcomes_html, encoding='utf-8', newline='\n')
    pages[output / 'outcomes.html'] = Links(outcomes_html)

    links = 0
    for path, parsed in list(pages.items()):
        for href in parsed.links:
            target = urlsplit(href)
            assert not target.scheme, href
            resolved = (path.parent / unquote(target.path)).resolve() if target.path else path.resolve()
            assert resolved.is_file(), resolved
            if target.fragment:
                if resolved not in pages:
                    pages[resolved] = Links(resolved.read_bytes().decode('utf-8'))
                assert target.fragment in pages[resolved].ids, (path, href)
            links += 1
    for path, anchor in expected_targets:
        assert anchor in pages[path].ids
        assert any(href.startswith('../examples.html#case-') for href in pages[path].links)
    result = {'status': 'passed', 'explained_cases': len(rows), 'links_checked': links,
              'earlier_assessment_items': len(delivery['earlier_assessment']),
              'query_outcomes_checked_against_saved_results': len(delivery['query_outcomes']),
              'still_unverified_groups': len(delivery['unverified']),
              'analytical_payloads_unchanged': True, 'integrated_explanation_and_return_links': len(expected_targets),
              'delivery_status': str(output / 'outcomes.html'),
              'guide': str(output / 'examples.html')}
    (output / 'example-guide-verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence-dir', type=Path, required=True, help='Directory containing genuine CLI commands.json and exports')
    parser.add_argument('--output-dir', type=Path, required=True, help='Review bundle directory; writes examples.html and investigations/')
    parser.add_argument('--featured-commands', type=Path, action='append', default=[], help='Additional recorded CLI command JSON containing featured JSON exports')
    args = parser.parse_args()
    print(json.dumps(build(args.evidence_dir.resolve(), args.output_dir.resolve(), args.featured_commands), indent=2))
