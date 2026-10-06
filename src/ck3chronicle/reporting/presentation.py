"""Offline report views of plain analysis data, shared by HTML and text.

ElementTree owns escaping of every data-bearing text/attribute. The packaged
string.Template shell contains only trusted layout/CSS and serialized elements.
No diagnostic, filename, purpose or source code is interpreted as markup.
"""
from html import escape
from importlib.resources import files
import json
from string import Template
from urllib.parse import quote
import xml.etree.ElementTree as ET
from .query import refinement_clauses
from .source_search import file_line_sources
from .analysis import window_positions
from ..decoder import display_text


def _text(value):
    return 'unavailable' if value is None else str(value)


def _el(parent, tag, text=None, **attrs):
    node = ET.SubElement(parent, tag, {k.rstrip('_').replace('_', '-'): str(v) for k, v in attrs.items()})
    if text is not None:
        node.text = _text(text)
    return node


def _encoding_status(validation):
    if not validation:
        return 'Encoding header not inspected'
    warnings = validation.get('warnings', [])
    if warnings:
        return 'Critical Encoding issues (' + ', '.join(dict.fromkeys(w['label'] for w in warnings)) + ')'
    if validation.get('status') == 'unavailable' or validation.get('unavailable_files'):
        return 'Encoding header unavailable'
    if validation.get('status') == 'undetermined' or validation.get('undetermined_files'):
        return 'Encoding header undetermined'
    if validation.get('not_inspected_candidate_ids') or validation.get('requested_files') == 0:
        return 'Encoding header not fully inspected'
    return 'No critical header patterns detected'


def _resolution(parent, entry):
    values = entry.get('reference_resolution', [])
    if not values:
        return
    labels = {'resolved': 'Resolved',
              'unresolved': 'File not found',
              'incomplete': 'Unknown: source search incomplete',
              'not_searched': 'Not searched: stored-path selection only',
              'outside_scope': 'Outside the selected path scope'}
    _table(parent, ['Recorded path', 'Line', 'Status', 'Paths found'], [
        [v['reference']['path'], v['reference'].get('line'), labels[v['status']] +
         (' / ' + _encoding_status(v['encoding_validation']) if v.get('encoding_validation', {}).get('warnings') else ''),
         len(v['candidate_ids']) if v['status'] in {'resolved', 'unresolved'} else None] for v in values])


def _match_origin(origin):
    return f'<{origin["type"]}> slot' if origin['kind'] == 'slot' else 'Template literal text'


def _window_rows(payload, counts=None):
    window = payload.get('window') or (payload.get('partial') or {}).get('window')
    if not window:
        return [['—', rid, value] for rid, value in (counts or {}).items()]
    runs = {r['run_id']: r for r in window['runs']}
    if not window.get('chronology_available', True):
        return [['Selected (chronology unavailable)', r['run_id'],
                 counts[r['run_id']] if counts is not None else r['occurrences']]
                + ([] if counts is not None else [r['distinct_records']]) for r in window['runs']]
    positions = window_positions(window['runs'], window['requested'])
    rows = []
    for position in positions:
        offset, rid = position['offset'], position['run_id']
        label = 'Run 0 (selected)' if offset == 0 else f'Run {offset:+d}'
        if not position['available']:
            rows.append([label, 'Not available', 'Not available'] + ([] if counts is not None else ['Not available']))
        elif counts is not None:
            rows.append([label, rid, counts[rid]])
        else:
            run = runs[rid]
            rows.append([label, rid, run['occurrences'], run['distinct_records']])
    return rows


def _message_matches(parent, entry):
    _el(parent, 'p', 'Assigned template: ' + entry['identity']['definition']['template_id'], class_='meta')
    matches = entry.get('message_matches', [])
    if matches:
        _table(parent, ['Search term', 'Matched text', 'From', 'Stored location'], [
            [match['term'], origin['text'], _match_origin(origin),
             origin['region'] + (' / ' + origin['slot_id'] if origin['kind'] == 'slot' else '')]
            for match in matches for origin in match['origins']])


def _message_summary(parent, payload):
    buckets = payload['rollups'].get('message_matches', {}).get('buckets', [])
    if not buckets:
        return
    node = _el(parent, 'section', id='message-matches')
    _el(node, 'h3', 'Where the search matched')
    _el(node, 'p', 'The whole diagnostic is searched, including literal wording and populated slot values. '
        'These counts cover all selected-Run matches before display limits. A diagnostic may appear in more than one row; do not add these rows together.')
    _table(node, ['Search term', 'From', 'Diagnostics', 'Occurrences', 'Assigned templates'], [
        [b['message_match']['term'], _match_origin(b['message_match']), b['distinct_records'], b['occurrences'],
         len(b['templates'])] for b in buckets]).set('class', 'match-summary')
    references = _details(node, 'Assigned template IDs for these matches')
    for bucket in buckets:
        _el(references, 'p', bucket['message_match']['term'] + ' — ' + _match_origin(bucket['message_match'])
            + ': ' + ', '.join(t['template_id'] for t in bucket['templates']))


def _details(parent, title):
    node = _el(parent, 'details')
    _el(node, 'summary', title)
    return node


def _json(parent, title, value):
    node = _details(parent, title)
    # Keep copyable identities/query data reversible even in a human report.
    from .cli import serialize_json
    _el(node, 'pre', serialize_json(value).rstrip('\n'))
    return node


def _table(parent, headers, rows):
    wrapper = _el(parent, 'div', class_='table-wrap')
    table = _el(wrapper, 'table')
    head = _el(_el(table, 'thead'), 'tr')
    for header in headers:
        _el(head, 'th', header, scope='col')
    body = _el(table, 'tbody')
    for row in rows:
        node = _el(body, 'tr')
        for item in row:
            cell = _el(node, 'td')
            if isinstance(item, ET.Element):
                cell.append(item)
            else:
                cell.text = _text(item)
    return table


def _link(label, target):
    node = ET.Element('a', {'href': target})
    node.text = str(label)
    return node


def _member(candidate):
    member = candidate.get('member')
    if member is None:
        return 'Explicit root'
    return member.get('name') or '(unnamed member)'


def _file_columns(candidate, path, line):
    member = candidate.get('member') or {}
    return [member.get('load_order', '—'),
            member.get('name', '—') if member.get('root_ID') != 'ROOT_GAME' else '—', path, line]


def _file_label(candidate, path):
    member = candidate.get('member')
    if member and member.get('root_ID') == 'ROOT_GAME':
        return path
    return _member(candidate) + ' — ' + path


def _guide(parent, payload, evidence=None):
    from .explanation import explain
    value = payload.get('explanation') or explain(payload)
    section = _el(parent, 'section', id='explanation', class_='reading-guide')
    if payload.get('example', {}).get('outcomes_href'):
        review = _el(section, 'p', class_='review-status')
        review.text = 'Earlier failures and incomplete deliverables: '
        review.append(_link('case-by-case expected and actual outcomes', payload['example']['outcomes_href'] + '#query-outcomes'))
        review[-1].tail = ' · '
        review.append(_link('still-unverified checks', payload['example']['outcomes_href'] + '#unverified'))

    def content(node, items):
        if isinstance(items, str):
            _el(node, 'p', items)
        elif len(items) == 1:
            _el(node, 'p', items[0])
        elif items:
            listing = _el(node, 'ul')
            for item in items:
                _el(listing, 'li', item)

    _el(section, 'h2', 'What this report checks')
    if payload.get('example', {}).get('evidence_kind') == 'synthetic':
        _el(section, 'p', 'Synthetic verification fixture: two genuine emissions with only their file LOCATOR paths changed. The recorded playset membership is unchanged. This is not a genuine game Run or history example.', class_='notice')
    content(section, value['question'])
    request = payload.get('request') or payload.get('example', {}).get('request')
    if request:
        _el(section, 'p', ' · '.join(f'{label}: {request[field]}' for field, label in (
            ('run', 'Requested Run'), ('package_id', 'Package'), ('preset', 'Preset'))
            if request.get(field) is not None), class_='meta')
    # Keep the explanation and actual outcome adjacent. Command paths and long
    # filter dictionaries must not separate the question from its answer.
    panels = _el(section, 'div', class_='outcome-panels')
    for key, title in (('expected', 'What the result should show'), ('result', 'What this result shows')):
        panel = _el(panels, 'section', class_='outcome-panel')
        _el(panel, 'h2', title, **({'id': 'actual-result'} if key == 'result' else {}))
        content(panel, value[key])
        if key == 'result' and payload.get('example'):
            _el(panel, 'p', f'Recorded command exit code: {payload["example"]["cli_exit_code"]}.', class_='meta')
    if evidence is not None:
        evidence(_el(section, 'section', id='explanation-evidence', class_='explanation-evidence'))
    if payload.get('example', {}).get('attachments'):
        attachments = _details(section, 'Inputs and verification evidence')
        for item in payload['example']['attachments']:
            _el(attachments, 'p').append(_link(item['label'], item['href']))
    filters = _details(section, 'The query in plain English and exact command selection')
    content(filters, value['conditions'])
    if request:
        labels = {'operation': 'Command', 'run': 'Requested Run', 'package_id': 'Requested processing package',
                  'preset': 'Preset', 'database': 'Database', 'query': 'Query file'}
        _table(filters, ['Requested selection', 'Value'], [
            [label, request[field]] for field, label in labels.items() if request.get(field) is not None])
    if payload.get('example', {}).get('data_href'):
        _el(filters, 'p').append(_link('Open the saved structured result', payload['example']['data_href']))
    content(_details(section, 'How to read the entries'), value['reading_guide'])


def _visible_files(parent, entry, link=None):
    """Show resolved paths and the shared file/line attribution in ordinary columns."""
    sources = entry.get('file_line_sources')
    if sources is None:
        # Reading copies can derive the rule from retained resolved associations.
        # Do not infer a source from a saved content-filtered subset of the files.
        known = {c['candidate_id'] for c in entry['candidates']}
        complete = all(set(r['candidate_ids']) <= known for r in entry.get('reference_resolution', []))
        sources = file_line_sources(entry['candidates']) if complete else []
    winners = {(s['error_source']['candidate_id'], s['line']) for s in sources if s['error_source']}
    rows = []
    for candidate in entry['candidates']:
        for index, ref in enumerate(candidate['references']):
            path = link(candidate, ref, index) if link else candidate['relative_path']
            source = 'Yes' if (candidate['candidate_id'], ref.get('line')) in winners else '—'
            decoding = candidate.get('decoding', {})
            status = _encoding_status(candidate.get('encoding_validation'))
            if decoding.get('warnings'):
                status += ' / Encoding warning (' + str(decoding.get('encoding')) + ')'
            rows.append([*_file_columns(candidate, path, ref.get('line')), source,
                         status])
    if rows:
        _el(parent, 'h4', 'Matching files')
        _el(parent, 'p', 'Error source: last in load order for each file/line.', class_='meta')
        _table(parent, ['Load order', 'Mod name', 'File path', 'Line', 'Error source', 'Encoding validation'], rows)
        for candidate in entry['candidates']:
            for warning in candidate.get('decoding', {}).get('warnings', []):
                _el(parent, 'p', _file_label(candidate, candidate['relative_path']) + ': ' + warning['reason'], class_='notice')
            validation = candidate.get('encoding_validation')
            if validation and (validation.get('warnings') or validation.get('status') in {'unavailable', 'undetermined'}):
                node = _details(parent, _file_label(candidate, candidate['relative_path']) + ' — ' + _encoding_status(validation))
                _el(node, 'p', validation.get('scope'))
                for warning in validation.get('warnings', []):
                    _el(node, 'p', f"Critical Encoding issues ({warning['label']}) at byte {warning['byte_offset']}: {warning['reason']}", class_='notice')
                if validation.get('reason') or validation.get('decoding_issue'):
                    _el(node, 'p', validation.get('reason') or validation['decoding_issue'], class_='notice')
                if validation.get('prefix_hex'):
                    _el(node, 'pre', 'Header bytes: ' + validation['prefix_hex'] + '\nEscaped text: ' + validation['escaped_prefix'])
    displayed = {c['candidate_id'] for c in entry['candidates']}
    outside = [s for s in sources if s['error_source'] and s['error_source']['candidate_id'] not in displayed]
    if outside:
        _el(parent, 'h4', 'Error source')
        _el(parent, 'p', 'Load order is evaluated before the separate file-content filter.')
        _table(parent, ['Load order', 'Mod name', 'File path', 'Line'], [
            _file_columns(s['error_source'], s['relative_path'], s['line']) for s in outside])


def _fraction(value):
    return f'{value[0]}/{value[1]} successfully read Runs' if value is not None else 'unavailable (no successful reads)'


def _template_investigation(payload):
    refinement = payload['effective_query']['refinement']
    fields = {'templates', 'template_exact', 'template_text'}
    return (payload['presentation']['preset']['name'] == 'symbol'
            or any(fields & branch.keys() for clause in refinement_clauses(refinement)
                   for branch in [clause, *clause.get('selectors', [])]))


def _templates(parent, payload, limit):
    """Present complete analytical template buckets, never totals from displayed entries."""
    section = _el(parent, 'section', id='templates')
    _el(section, 'h2', 'Matching templates — patterns and combined counts')
    _el(section, 'p', 'A template is the shared message pattern with typed placeholders. '
        'Each diagnostic below is a specific stored instance with its own values and script location. '
        'Template counts combine the matching diagnostics; all effective query restrictions still apply.')
    buckets = payload['window']['rollups']['templates']['buckets']
    selected = {b['key']: b for b in payload['rollups']['templates']['buckets']}
    _el(section, 'p', f'Showing {min(limit, len(buckets))} of {len(buckets)} matching stored template definitions '
        f'across the included Runs; display limit {limit}. Counts include diagnostics beyond their display limits.')
    if not buckets:
        _el(section, 'p', 'No matching diagnostic supplies a stored template definition in the successfully read Runs.')
    for number, bucket in enumerate(buckets[:limit], 1):
        template = bucket['template']
        node = _el(section, 'section', id=f'T{number}', class_='diagnostic')
        _el(node, 'h3', 'Template ' + template['template_id'])
        _el(node, 'p', class_='meta').append(_link('Back to the explanation and evidence', '#explanation'))
        _el(node, 'pre', template['text'], class_='template-pattern')
        _el(node, 'p', 'Placeholders such as <KEY>, <REASON> and <LOCATOR> vary between diagnostics. '
            'The stored pattern above contains no values from an individual diagnostic.')
        _el(node, 'p', f'Model {template["model_revision"]} · contract {template["contract_version"]} · '
            f'emitter {template["source_family"]}', class_='meta')
        current = selected.get(bucket['key'], {})
        _el(node, 'p', f'Selected Run: {current.get("occurrences", 0)} occurrences across '
            f'{current.get("distinct_records", 0)} distinct diagnostics. Included-window total: '
            f'{bucket["occurrences"]} occurrences across {bucket["distinct_records"]} distinct diagnostics.')
        rows = []
        for run in payload['window']['runs']:
            match = next((b for b in run['rollups']['templates']['buckets'] if b['key'] == bucket['key']), {}) if run['rollups'] is not None else None
            rows.append([run['run_id'] + (' (selected Run)' if run['role'] == 'selected' else ''),
                         match.get('occurrences', 0) if match is not None else None,
                         match.get('distinct_records', 0) if match is not None else None,
                         'Read unavailable' if match is None else 'Observed' if match else 'Not observed'])
        _table(node, ['Run', 'Template occurrences', 'Distinct matching diagnostics', 'Observation'], rows)
        _el(node, 'p').append(_link('Individual diagnostics in the selected Run', '#diagnostics'))


def _exclusions(parent, exclusions):
    node = _details(parent, f'Chronology exclusions ({sum(len(e["run_ids"]) for e in exclusions)} Runs)')
    if not exclusions:
        _el(node, 'p', 'No timestamp exclusions in this package.')
    else:
        _table(node, ['Run IDs', 'Stored source timestamp', 'Reason'], [
            [', '.join(e['run_ids']), e['timestamp'], e['reason'] + (' ' + e['guidance'] if e.get('guidance') else '')]
            for e in exclusions])


def _rankings(parent, rollups, *, limit, links):
    if not rollups:
        return
    for key, title in (('emitters', 'Emitter groupings'), ('referenced_files', 'Referenced script/file paths'),
                       ('candidate_files', 'Matching files')):
        result = rollups.get(key)
        if result is None:
            continue
        buckets = result['buckets']
        node = _details(parent, f'{title} — {len(buckets)} groups')
        _el(node, 'p', f'Showing {min(limit, len(buckets))} of {len(buckets)} groups. '
            f'Overlapping exact records: {result["overlapping_records"]}; unassociated: {result["unassociated_records"]}. '
            'Bucket sums count associations and must not be substituted for unique diagnostic totals.')
        rows = []
        for bucket in buckets[:limit]:
            name = bucket['key']
            columns = [name]
            if 'candidate' in bucket:
                c = bucket['candidate']
                columns = _file_columns(c, c['relative_path'], 'All matching lines')
            contributors = ET.Element('span')
            visible = [k for k in bucket['identity_keys'] if k in links]
            for index, identity in enumerate(visible):
                link = _link(links[identity], '#' + links[identity])
                link.tail = ', ' if index < len(visible) - 1 else ''
                contributors.append(link)
            hidden = len(bucket['identity_keys']) - len(visible)
            if hidden:
                _el(contributors, 'span', f' ({hidden} contributors beyond diagnostic display limit)')
            rows.append([*columns, bucket['occurrences'], bucket['distinct_records'], contributors])
        headers = ['Load order', 'Mod name', 'File path', 'Line'] if key == 'candidate_files' else ['Group']
        _table(node, [*headers, 'Occurrences', 'Distinct records', 'Displayed contributors'], rows)


class _Document:
    def __init__(self, payload, appendix_name):
        self.payload = payload
        self.root = ET.Element('main')
        self.appendix = ET.Element('main')
        self.appendix_name = appendix_name
        self.verbose = payload.get('presentation', {}).get('verbose', False)
        self.excerpts = {}
        self.title = 'CK3 Chronicle'

    def guide_evidence(self, parent):
        """Put the evidence discussed by the explanation beside that explanation.

        These are labelled excerpts of the existing presentation data, never
        another query or a new set of totals. Detail links use the same entries.
        """
        p = self.payload
        _el(parent, 'h2', 'Evidence for this result')
        if 'eligible_count' in p:
            _table(parent, ['Eligible Run', 'Original source-log timestamp'], [
                [r['run_id'], r['facts'].get('error_log_source_modified_at')] for r in p['runs']])
            if p['exclusions']:
                _exclusions(parent, p['exclusions'])
            return
        if p['status'] != 'completed':
            partial = p.get('partial')
            if not partial:
                _el(parent, 'p', p['error'], class_='notice')
                _el(parent, 'p', 'This response is the outcome of the request. There is no diagnostic result to find elsewhere in the report.')
                return
            for index, entry in enumerate(partial.get('records', [])[:1], 1):
                self.evidence_entry(parent, entry, f'P{index}', 'Known matching diagnostic',
                                    history=partial.get('effective_query', {}).get('analytics', {}).get('history', True))
            _el(parent, 'p').append(_link('Source search scope and coverage', '#source-coverage'))
            return
        history = p['window']['history_available']
        limit = p['effective_query']['display']['limit']
        _message_summary(parent, p)
        if _template_investigation(p) and limit and p['window']['rollups']['templates']['buckets']:
            buckets = p['window']['rollups']['templates']['buckets']
            bucket = buckets[0]
            card = _el(parent, 'section', class_='evidence-card')
            _el(card, 'h3', f'Stored template pattern · first of {len(buckets)} matching patterns')
            _el(card, 'pre', bucket['template']['text'])
            _el(card, 'p', 'This is a shared pattern. Each matching diagnostic is a separate record with its own values.')
            _el(card, 'p').append(_link('This template and its combined counts in each Run', '#T1'))
        if history:
            _el(parent, 'h3', 'All matches by Run')
            _table(parent, ['Position', 'Run', 'Occurrences', 'Distinct diagnostics'], _window_rows(p))
            _el(parent, 'p', 'Not available means no eligible Run occupies that position. It is not a failed read or a diagnostic count of zero.')
            _el(parent, 'p').append(_link('Run-window details and contributing diagnostics', '#window'))
        if p['presentation']['preset']['name'] == 'hotspots':
            files = (p['rollups'].get('candidate_files') or {}).get('buckets', [])
            if files and limit:
                _el(parent, 'h3', 'Files with the most matching occurrences')
                _table(parent, ['Load order', 'Mod name', 'File path', 'Line', 'Occurrences', 'Distinct diagnostics'], [
                    [*_file_columns(b['candidate'], b['candidate']['relative_path'], 'All matching lines'), b['occurrences'], b['distinct_records']]
                    for b in files[:min(3, limit)]])
                _el(parent, 'p', 'These are candidate associations; overlapping files do not increase the unique diagnostic totals.')
        entries = [(e, f'D{i}', 'Selected-Run diagnostic') for i, e in enumerate(p['records'][:2], 1)]
        if p['historical'] and p['presentation']['preset']['name'] == 'frequent':
            entries = entries[:1] + [(p['historical'][0], 'H1', 'Previously observed; absent from the selected Run')]
        if entries:
            _el(parent, 'p', f'The entries below illustrate the result. The query matched {p["totals"]["distinct_records"]} selected-Run diagnostics in total; the complete displayed list and its limits remain below.')
            for entry, label, meaning in entries:
                self.evidence_entry(parent, entry, label, meaning, history=history)
        elif not p['totals']['distinct_records']:
            _el(parent, 'p', 'Zero selected-Run diagnostics satisfy all filters. There are no matching lines or diagnostic entries to locate.', class_='notice')
        else:
            _el(parent, 'p', 'The requested display limit omits individual diagnostics; the totals above still include every match.')

    def evidence_entry(self, parent, entry, label, meaning, *, history):
        card = _el(parent, 'section', class_='evidence-card')
        _el(card, 'h3', meaning + f' · {label} · {entry["selected_count"]} occurrence(s) in the selected Run')
        _el(card, 'pre', entry['message'], class_='message')
        _message_matches(card, entry)
        _resolution(card, entry)
        if history:
            _table(card, ['Position', 'Run', 'Occurrences of this exact diagnostic'], _window_rows(self.payload, entry['history']['counts']))
        self.file_table(card, entry, label)
        if not entry['candidates'] and entry['reference_details'] and not entry.get('reference_resolution'):
            _table(card, ['Stored file path', 'Line'], [[r['path'], r.get('line')] for r in entry['reference_details']])
        if not entry['candidates']:
            coverage = (self.payload.get('partial') or {}).get('coverage') or self.payload.get('coverage', {}).get('source', {}).get(entry['origin']['run_id'], {})
            if not entry['reference_details']:
                _el(card, 'p', 'Source lookup: not applicable. This emission supplies no file path.')
            elif entry.get('reference_resolution'):
                if any(v['status'] == 'resolved' for v in entry['reference_resolution']):
                    _el(card, 'p', 'Files were found, but none matches the separate source-content condition.')
                for reason in dict.fromkeys(i['reason'] for i in coverage.get('issues', [])):
                    _el(card, 'p', reason)
            elif coverage.get('complete'):
                _el(card, 'p', 'Complete search: no matching file on disk within the effective scope. The diagnostic and its stored path remain visible.', class_='notice')
            else:
                _el(card, 'p', 'Incomplete source coverage: a missing candidate does not establish that the file is absent.', class_='notice')
                for reason in dict.fromkeys(i['reason'] for i in coverage.get('issues', [])):
                    _el(card, 'p', reason)
        _el(card, 'p').append(_link('Read the complete evidence for diagnostic ' + label, '#' + label))

    def file_table(self, parent, entry, label):
        def location(candidate, ref, index):
            if not self.verbose:
                return candidate['relative_path']
            excerpts = candidate.get('excerpts', [])
            excerpt = excerpts[index] if index < len(excerpts) else {'available': False, 'reason': 'No excerpt returned.'}
            anchor = self._excerpt(candidate, ref, excerpt, quote(self.report_name) + '#' + label)
            return _link(candidate['relative_path'], quote(self.appendix_name) + '#' + anchor)
        _visible_files(parent, entry, location)

    def _excerpt(self, candidate, ref, excerpt, backlink):
        # Share repeated physical/reference/member associations without losing provenance.
        key = (candidate['candidate_id'], candidate['physical_path'], ref.get('line'))
        if key not in self.excerpts:
            anchor = f'source-{len(self.excerpts) + 1}'
            self.excerpts[key] = anchor
            node = _el(self.appendix, 'section', id=anchor, class_='diagnostic')
            _el(node, 'h2', anchor)
            _table(node, ['Load order', 'Mod name', 'File path', 'Line'], [
                _file_columns(candidate, candidate['relative_path'], ref.get('line'))])
            _el(node, 'p', candidate['physical_path'], class_='path')
            _json(node, 'Recorded member identity', candidate.get('member'))
            _el(node, 'p', 'Current file contents at report generation.')
            _el(node, 'p').append(_link('Back to diagnostic', backlink))
            if excerpt.get('available'):
                lines = excerpt['lines']
                _el(node, 'p', f'Lines {lines[0]["line"]}–{lines[-1]["line"]} of {excerpt["total_lines"]}; target line marked >.')
                pre = _el(node, 'pre', class_='source')
                for line in lines:
                    _el(pre, 'mark' if line['target'] else 'span',
                        f'{">" if line["target"] else " "} {line["line"]:6} | {line["text"]}\n')
            else:
                _el(node, 'p', 'Excerpt unavailable: ' + excerpt.get('reason', 'No excerpt returned.'), class_='notice')
        return self.excerpts[key]

    def entry(self, parent, entry, label, coverage, report_name, *, history=True, per_run=False):
        node = _el(parent, 'article', id=label, class_='diagnostic')
        row = entry['stored_record']
        count = entry.get('run_count') if per_run else entry['selected_count']
        count_scope = 'this Run' if per_run else 'the selected Run'
        _el(node, 'h3', f'Diagnostic {label} · {count} occurrence(s) in {count_scope}')
        _el(node, 'p', class_='meta').append(_link('Back to the explanation and evidence', '#explanation'))
        _el(node, 'p', f'Specific diagnostic recorded in Run {entry["origin"]["run_id"]} · engine emitter {row["definition"]["source_family"]}', class_='meta')
        if row['match_status'] == 'provisional':
            _el(node, 'p', 'This diagnostic has a provisional classification.', class_='notice')
        _el(node, 'h4', 'Recorded diagnostic message')
        _el(node, 'pre', entry['message'], class_='message')
        _message_matches(node, entry)
        _resolution(node, entry)
        self.file_table(node, entry, label)
        if count == 0:
            _el(node, 'p', 'Previously observed; not observed in the selected Run. This is absence, not a confirmed fix.', class_='notice')
        if history:
            h = entry['history']
            _el(node, 'h4', 'Occurrences by Run', id=label + '-runs')
            _table(node, ['Position', 'Run', 'Occurrences of this exact diagnostic'], _window_rows(self.payload, h['counts']))
            selected_run = self.payload.get('run', {}).get('run_id')
            previous = None
            counts = []
            for rid, value in h['counts'].items():
                change = value - previous if value is not None and previous is not None else None
                run_label = rid + (' (selected Run)' if rid == selected_run else '')
                counts.append([run_label, value, 'Read unavailable' if value is None else
                               'Not observed' if value == 0 else 'Observed',
                               f'{change:+d}' if change is not None else 'unavailable'])
                previous = value
            panel = _details(node, 'History notes and observation fractions')
            _table(panel, ['Run', 'Occurrences', 'Observation', 'Change from preceding included Run'], counts)
            _el(panel, 'p', 'Preceding observation fraction: ' + _fraction(h['preceding_fraction']) +
                '; subsequent: ' + _fraction(h['subsequent_fraction']) + '.')
            _el(panel, 'p', ('New within this included window.' if h['newly_observed'] else 'Not new within this included window.') +
                (' Comparison coverage incomplete.' if not h['comparison_complete'] else ''))
        _json(node, 'Exact diagnostic identity (copy into refinement.identities)', entry['identity'])
        classification = _details(node, 'How this diagnostic was classified')
        _el(classification, 'p', 'This is a specific diagnostic, with its values filled in. It was recognized using stored error pattern '
            + row['definition']['template_id'] + '. The error pattern itself is shown separately below.')
        _el(classification, 'p', 'Stored classification: ' + row['match_status'] +
            (' (recognized using a template).' if row['match_status'] == 'template' else ' (provisional assignment).'))
        _el(_details(node, 'Stored template text (independent of bound values)'), 'pre', entry['template_text'])
        bindings = [[r['name'], b['slot_id'], b['type'], b['value'] if b['present'] else '(absent)']
                    for r in row['values']['regions'] for b in r['bindings']]
        if bindings:
            _table(_details(node, 'Typed values'), ['Region', 'Slot', 'Type', 'Value'], bindings)
        refs = entry['reference_details']
        if refs:
            _table(_details(node, 'Stored reference details'), ['Stored reference', 'Line', 'Region / slot', 'Role'], [
                [r['path'], r.get('line'), f'{r["region"]} / {_text(r.get("slot_id"))}', r['role']] for r in refs])
        else:
            _el(node, 'p', 'Source lookup: not applicable. This emission supplies no file path.')
        candidates = entry['candidates']
        if refs and not coverage.get('complete', False):
            _el(node, 'p', 'Incomplete source coverage: absence of a candidate is not proof that no matching file exists. See source coverage.', class_='notice')
        elif refs and not candidates and not entry.get('reference_resolution'):
            _el(node, 'p', 'Complete search: no matching file on disk within the effective scope.', class_='notice')
        if candidates:
            details = _details(node, f'Physical paths and source excerpts ({len(candidates)} files)')
            for c in candidates:
                item = _el(details, 'section', class_='candidate')
                _table(item, ['Load order', 'Mod name', 'File path', 'Line'], [
                    _file_columns(c, c['relative_path'], r.get('line')) for r in c['references']])
                _el(item, 'p', c['physical_path'], class_='path')
                _json(item, 'Member identity', c.get('member'))
                for index, ref in enumerate(c['references']):
                    label_text = _file_label(c, ref['path']) + f' : line {_text(ref.get("line"))} ({ref["region"]}, {ref["role"]})'
                    p = _el(item, 'p')
                    if self.verbose:
                        excerpts = c.get('excerpts', [])
                        excerpt = excerpts[index] if index < len(excerpts) else {'available': False, 'reason': 'No excerpt returned.'}
                        target = self._excerpt(c, ref, excerpt, quote(report_name) + '#' + label)
                        p.append(_link(label_text + f' → {target}', quote(self.appendix_name) + '#' + target))
                    else:
                        p.text = label_text

    def coverage(self, parent, coverage):
        section = _el(parent, 'section', id='source-coverage')
        _el(section, 'h2', 'Effective source scope and coverage')
        _el(section, 'p', 'Default roots are each Run’s recorded playset. Explicit context/root/member/directory selections are shown below. Exact relative references narrow inventories to their parent directories within that scope.')
        for rid, value in coverage.items():
            if value.get('encoding_validation'):
                _json(section, f'{rid} — encoding header validation of requested detail', value['encoding_validation'])
            if not isinstance(value, dict):
                continue
            for decoded in value.get('decoding', []):
                for warning in decoded.get('warnings', []):
                    _el(section, 'p', str(decoded['path']) + ': ' + warning['reason'], class_='notice')
            counts = value.get('search_counts')
            if counts is not None:
                _el(section, 'h3', rid + ' · source search counts')
                _table(section, ['Files checked (names/paths)', 'Folders checked', 'Candidate files',
                                 'Files selected for content check', 'Matching files'], [[
                    counts['files_searched'], counts['folders_searched'], counts['candidate_files'],
                    counts['content_files_requested'], counts['matching_files']]])
                _el(section, 'p', 'Counts describe this search, including cached inventories. Folders include the starting directories and empty folders. '
                    'Physical paths are counted once across overlapping roots; per-root counts below may overlap. '
                    'These are the effective lookup directories, which can be narrower than the whole root.')
                if value.get('searched') is False:
                    _el(section, 'p', 'No filesystem search was needed for this stored-data selection.')
                if not value.get('complete'):
                    _el(section, 'p', 'Source coverage is incomplete; these counts describe only the work that could be evaluated.', class_='notice')
            node = _details(section, f'{rid} · {"complete" if value.get("complete") else "incomplete"} source coverage')
            _el(node, 'pre', json.dumps(value.get('effective_selection', {}), ensure_ascii=False, indent=2))
            for issue in value.get('issues', []):
                _el(node, 'p', f'{_text(issue.get("path"))}: {issue["reason"]} {_text(issue.get("error"))}', class_='notice')
            roots = value.get('roots', [])
            scopes = value.get('search_scopes', [])
            if scopes:
                _table(node, ['Load order', 'Mod name', 'Root', 'Lookup directories', 'Descend into subfolders',
                              'Files checked', 'Folders checked', 'Inventory source / coverage'], [
                    [*_file_columns(s, s['root'], None)[:3], '\n'.join(s['directories']), 'Yes' if s['recursive'] else 'No',
                     s['files_searched'], s['folders_searched'],
                     s.get('skipped') or ({'none': 'Read from disk', 'exact_scope': 'Cached scope',
                       'whole_root_subset': 'Selected from cached root'}[s['cache']] +
                       ('; complete' if s['complete'] else '; incomplete'))] for s in scopes])
            _table(_details(node, f'Selected roots / recorded member identities ({len(roots)})'),
                ['Load order', 'Mod name', 'Root', 'Available', 'Reason'], [
                    [*_file_columns(r, r.get('path'), None)[:3], r.get('available'), r.get('reason')] for r in roots])
            no_path = value.get('records_without_source_path', 0)
            if no_path:
                _el(node, 'p', f'{no_path} diagnostic(s) supply no file path; source lookup is not applicable to those emissions.')
            _json(node, 'Actual inventory scopes and search metrics', value.get('metrics', {}))

    def build(self, report_name):
        self.report_name = report_name
        p, root = self.payload, self.root
        navigation = _el(root, 'nav', aria_label='Investigation navigation', class_='investigation-nav')
        _el(navigation, 'span').append(_link('Explanation and evidence', '#explanation'))
        _el(navigation, 'span').append(_link('Actual result', '#actual-result'))
        example = p.get('example', {})
        if example.get('outcomes_href'):
            _el(navigation, 'span').append(_link('08B delivery status and remaining gaps', example['outcomes_href']))
        if example.get('guide_href'):
            _el(navigation, 'span').append(_link('Back to this example in the investigation list', example['guide_href']))
            _el(root, 'p', 'Example: ' + example['name'], class_='eyebrow')
        if p.get('status') != 'completed':
            self.title = 'Operation failed' if p['status'] in {'operation_failed', 'read_unavailable'} else 'Investigation unavailable'
            _el(root, 'h1', self.title)
            _guide(root, p, self.guide_evidence)
            _el(root, 'p', f'{p["status"]}: {p["error"]}', class_='notice')
            _json(root, 'Operation and exception details', {
                field: p[field] for field in ('request', 'failure_stage', 'exception_class', 'read_error', 'traceback')
                if field in p})
            if p.get('chronology_exclusions'):
                _exclusions(root, p['chronology_exclusions'])
            partial = p.get('partial')
            if partial:
                _el(root, 'h2', 'Partial source matches — incomplete evidence')
                metadata = partial.get('run', {})
                _el(root, 'p', f'Run {metadata.get("run_id", "unavailable")} · package {metadata.get("lineage", {}).get("package_id", "unavailable")} · '
                    f'original source timestamp {metadata.get("facts", {}).get("error_log_source_modified_at", "unavailable")}.')
                _el(root, 'p', 'Report generated / current source observation: ' + p['presentation']['generated_at'])
                _el(root, 'p', 'Unable to evaluate the required source filter completely. These known matches are not a complete report or an exact zero.')
                _el(root, 'p', f'Known matching records: {partial.get("known_matching_records", len(partial.get("matches", [])))}; showing {len(partial.get("records", []))}.')
                _json(root, 'Effective query', partial.get('effective_query'))
                history = partial.get('effective_query', {}).get('analytics', {}).get('history', True)
                for index, entry in enumerate(partial.get('records', []), 1):
                    self.entry(root, entry, f'P{index}', partial['coverage'], report_name, history=history)
                self.coverage(root, {partial.get('run', {}).get('run_id', 'partial'): partial['coverage']})
            return
        if 'eligible_count' in p:
            self.title = 'Eligible Runs'
            _el(root, 'h1', self.title)
            _guide(root, p, self.guide_evidence)
            _el(root, 'p', f'Package {p["package_id"]} · {p["eligible_count"]} eligible Runs · offset {p["offset"]} · limit {p["limit"]}. {p["ordering"]}; package membership precedes pagination.')
            if not p['eligible_count']:
                _el(root, 'p', 'No Run belongs to this processing package.')
            elif not p['runs']:
                _el(root, 'p', 'No Runs on this page; eligible Runs exist outside the requested offset/limit.')
            _table(root, ['Run ID', 'Original source-log modification timestamp', 'Package'], [
                [r['run_id'], r['facts'].get('error_log_source_modified_at'), r['lineage']['package_id']] for r in p['runs']])
            _exclusions(root, p['chronology_exclusions'])
            return
        meta = p['presentation']
        self.title = meta['preset']['title']
        _el(root, 'p', 'CK3 CHRONICLE · STORED RUN INVESTIGATION', class_='eyebrow')
        _el(root, 'h1', self.title)
        if p['effective_query']['purpose'] != meta['preset']['condition']:
            _el(root, 'p', p['effective_query']['purpose'], class_='purpose')
        _guide(root, p, self.guide_evidence)
        _el(_details(root, 'Preset definition'), 'p', meta['preset']['condition'])
        template_view = _template_investigation(p)
        nav = _el(root, 'nav', aria_label='Report sections')
        sections = [('Explanation', 'explanation'), ('Actual result', 'actual-result'), ('Summary', 'summary')]
        if template_view:
            sections.append(('Templates', 'templates'))
        sections.extend([('Individual diagnostics', 'diagnostics'), ('Previously observed', 'historical'), ('Run window', 'window'), ('Source coverage', 'source-coverage')])
        for text, anchor in sections:
            a = _link(text, '#' + anchor)
            a.tail = ' · '
            nav.append(a)
        if self.verbose:
            nav.append(_link('Source appendix', quote(self.appendix_name)))
        summary = _el(root, 'section', id='summary')
        _el(summary, 'h2', 'Selected Run')
        _table(summary, ['Field', 'Value'], [
            ['Run', p['run']['run_id']], ['Processing package', p['package_id']],
            ['Original source-log modification timestamp', p['run']['facts'].get('error_log_source_modified_at')],
            ['Report generated / current source observation', meta['generated_at']],
            ['Filtered occurrences', p['totals']['occurrences']], ['Distinct exact diagnostics', p['totals']['distinct_records']],
            ['Previously observed entries (separate)', p['totals']['historical_entries']]])
        _json(summary, 'Effective filters and analytics (authoritative structured query)', p['effective_query'])
        _json(summary, 'Filter semantics', p['filter_meaning'])
        _json(summary, 'Optional source context (required scope.source overrides the same fields)', meta['source_context'])
        source = p['coverage']['source']
        selected_source = source.get(p['run']['run_id'], {})
        selection = selected_source.get('effective_selection', {})
        _el(summary, 'p', f'Effective source scope: {len(selected_source.get("roots", []))} selected roots; '
            + ('explicit roots' if 'roots' in selection else 'recorded playset') + '; '
            + json.dumps(selection, ensure_ascii=False) + '. Actual inventory scopes and coverage are disclosed below.')
        if 'search_counts' in selected_source:
            counts = selected_source['search_counts']
            _el(summary, 'p', f'Source lookup checked {counts["files_searched"]:,} file names/paths in '
                f'{counts["folders_searched"]:,} folders within its effective lookup scope. ').append(
                    _link('See counts, directories and cache use', '#source-coverage'))
        if meta['preset']['name'] == 'syntax':
            _el(summary, 'p', meta['preset']['exclusions'])
            _json(summary, 'Syntax evidence, nine conditions and package/model boundary', meta['preset'])
        _el(summary, 'p', 'Review coverage: ' + str(p['run']['counters'].get('review_emissions', 'unavailable')) +
            ' routed emissions; ' + str(p['run']['counters'].get('review_units', 'unavailable')) + ' review units. Unassigned evidence is outside the diagnostic search.')
        _json(summary, 'Stored review counts and references (availability is recorded, not rechecked)', p['review'])
        _el(summary, 'p', 'Counts reflect frequency and session length, not severity. Review-routed evidence is not searched. '
            'For each file/line, the last matching playset member in load order is the error source. Source contents are current at report generation.', class_='notice')
        limit = p['effective_query']['display']['limit']
        selected_links = {e['identity_key']: f'D{i}' for i, e in enumerate(p['records'], 1)}
        _rankings(summary, p['rollups'], limit=limit, links=selected_links)
        if template_view:
            _templates(root, p, limit)
        history = p['window']['history_available']
        if p['window']['unavailable_reason']:
            _el(root, 'p', p['window']['unavailable_reason'], class_='notice')
        section = _el(root, 'section', id='diagnostics')
        _el(section, 'h2', 'Individual diagnostics in the selected Run')
        if template_view:
            _el(section, 'p', 'These are the specific diagnostics matching the template investigation. '
                'Each heading counts one exact diagnostic, not the whole template. Their combined counts appear above.')
        _el(section, 'p', f'Showing {len(p["records"])} of {p["totals"]["distinct_records"]} matching exact records; display limit {limit}. Totals and rankings were computed before display limits.')
        if not p['totals']['distinct_records']:
            _el(section, 'p', 'Successful empty result: no selected-Run records match these effective filters.')
        if p['records']:
            _table(section, ['Diagnostic', 'Occurrences', 'Assigned template', 'Search matched in'], [
                [_link(selected_links[e['identity_key']], '#' + selected_links[e['identity_key']]),
                 e['selected_count'], e['identity']['definition']['template_id'],
                 ', '.join(dict.fromkeys(_match_origin(o) for m in e.get('message_matches', []) for o in m['origins'])) or '—']
                for e in p['records']])
        for entry in p['records']:
            self.entry(section, entry, selected_links[entry['identity_key']], source.get(entry['origin']['run_id'], {}), report_name, history=history)
        historical = _el(root, 'section', id='historical')
        _el(historical, 'h2', 'Previously observed')
        if history:
            _el(historical, 'p', f'Showing {len(p["historical"])} of {p["totals"]["historical_entries"]} matching preceding-window identities absent from the selected Run; separate limit {p["effective_query"]["display"]["historical_limit"]}. Their selected-Run count is zero; they do not contribute to selected totals.')
        else:
            _el(historical, 'p', p['window']['unavailable_reason'])
        _el(historical, 'p', 'An explicit positive occurrence minimum excludes these zero-count entries. include_absent=false or history=false omits this view.')
        for index, entry in enumerate(p['historical'], 1):
            self.entry(historical, entry, f'H{index}', source.get(entry['origin']['run_id'], {}), report_name, history=history)
        window = _el(root, 'section', id='window')
        _el(window, 'h2', 'Run window and per-Run filtered totals')
        _table(window, ['Position', 'Run', 'Filtered occurrences', 'Distinct diagnostics'], _window_rows(p))
        _json(window, 'Requested window / actual obtained and successfully read sizes',
              {'requested': p['window']['requested'], 'obtained': p['window']['obtained']})
        if history:
            _el(window, 'p', 'New means present in the selected Run and absent from every successfully read included predecessor. '
                'With no such predecessors, positive records are new within this window and the preceding observation fraction is unavailable. '
                'Observation fractions are observed successful reads / all successful reads; absent identities contribute zero. '
                'Unavailable reads enter neither numerator nor denominator. New is not a first-ever claim.')
        else:
            _el(window, 'p', 'Recent-Run commentary omitted; only the selected Run was read.')
        _table(window, ['Run', 'Original source timestamp', 'Role', 'Filtered occurrences', 'Distinct records', 'Read'], [
            [r['run_id'], r['timestamp'], r['role'], r['occurrences'], r['distinct_records'],
             r['read_error'] or r.get('unavailable') or 'successful'] for r in p['window']['runs']])
        _el(window, 'p', 'Per-Run totals apply the effective filters. Occurrence/newness refinements stay anchored to the selected Run. Exact-identity history retains the actual raw counts.')
        totals = p['window']['totals']
        _el(window, 'p', f'Included-window sum: {totals["occurrences"]} occurrences; {totals["distinct_records"]} distinct exact identities across {totals["successful_reads"]} successful reads. '
            'These are separate from selected-Run totals. Unavailable reads do not contribute; see window completeness.')
        window_links = dict(selected_links)
        for index, entry in enumerate(p['historical'], 1):
            window_links.setdefault(entry['identity_key'], f'H{index}')
        for index, run in enumerate(p['window']['runs'], 1):
            if run['role'] != 'selected':
                for number, entry in enumerate(run.get('records') or [], 1):
                    window_links.setdefault(entry['identity_key'], f'W{index}D{number}')
        _rankings(_details(window, 'Rankings across the included window'), p['window']['rollups'], limit=limit, links=window_links)
        for index, run in enumerate(p['window']['runs'], 1):
            if run['role'] == 'selected' or run.get('records') is None:
                continue
            node = _details(window, f'{run["run_id"]} · contributing exact diagnostics and candidate rankings')
            rows = run['records']
            _el(node, 'p', f'Showing {len(rows)} of {run["distinct_records"]} matching records; per-Run display limit {limit}.')
            links = {e['identity_key']: f'W{index}D{i}' for i, e in enumerate(rows, 1)}
            _rankings(node, run['rollups'], limit=limit, links=links)
            for entry in rows:
                self.entry(node, entry, links[entry['identity_key']], source.get(run['run_id'], {}), report_name, history=history, per_run=True)
        _exclusions(window, p['chronology_exclusions'])
        if p['coverage']['comparison_errors']:
            _json(window, 'Unavailable comparison reads (not zero observations)', p['coverage']['comparison_errors'])
        self.coverage(root, source)


def _page(title, root):
    package = files('ck3chronicle.reporting').joinpath('templates')
    shell = Template(package.joinpath('report.html').read_text(encoding='utf-8'))
    return display_text(shell.substitute(title=escape(title), style=package.joinpath('report.css').read_text(encoding='utf-8'),
                            body=ET.tostring(root, encoding='unicode', method='html')))


def _build(payload, report_name, appendix_name):
    doc = _Document(payload, appendix_name)
    _el(doc.appendix, 'h1', 'Current source appendix')
    _el(doc.appendix, 'p', 'Report generated / current source observation: ' + payload.get('presentation', {}).get('generated_at', 'unavailable'))
    _el(doc.appendix, 'p').append(_link('Return to report', quote(report_name)))
    _el(doc.appendix, 'p', 'Referenced line plus ten lines above/below, clipped to current file boundaries. Target lines are marked >. Repeated references may share an entry; recorded member associations remain distinct.')
    doc.build(report_name)
    for node in (doc.root, doc.appendix):
        native = ET.tostring(node, encoding='unicode')
        if display_text(native) != native:
            notice = ET.Element('p', {'class': 'notice'})
            notice.text = ('Preserved undecodable bytes are represented as \\xHH in this view. '
                           'These display escapes are not replacement characters or native values. '
                           'JSON exports retain native values using reversible \\uDCxx escapes; '
                           'message offsets refer to native text before display escaping.')
            node.insert(0, notice)
    if not doc.excerpts:
        _el(doc.appendix, 'p', 'No candidate excerpts are available for the displayed diagnostics. See main-report reference and source coverage explanations.')
    return doc


def render_html(payload, *, report_name, appendix_name):
    doc = _build(payload, report_name, appendix_name)
    return _page(doc.title, doc.root), _page('Current source appendix', doc.appendix) if doc.verbose else None


def _plain(node):
    """Readable text from the exact same semantic document, including details."""
    if node.tag == 'table':
        rows = [[''.join(c.itertext()) for c in r] for part in node for r in part]
        return display_text('\n'.join(' | '.join(row) for row in rows) + '\n\n')
    if node.tag in {'pre', 'h1', 'h2', 'h3', 'h4', 'p', 'summary', 'nav', 'li'}:
        text = display_text(''.join(node.itertext()))
        if node.tag.startswith('h') and node.tag != 'html':
            return '\n' + text + '\n' + ('=' if node.tag == 'h1' else '-') * min(80, len(text)) + '\n\n'
        return ('- ' if node.tag == 'li' else '') + text + '\n\n'
    return ''.join(_plain(child) for child in node)


def render_text(payload, *, kind='report'):
    doc = _build(payload, 'report', 'source-appendix')
    return _plain(doc.root) + ('\n' + _plain(doc.appendix) if doc.verbose else '')
