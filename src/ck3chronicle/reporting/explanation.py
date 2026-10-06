"""Plain-language reading guide derived from the effective query and result.

This explains an investigation; it does not declare an acceptance test passed.
The structured query and analytical data remain the authoritative inputs.
"""
import json
from .query import refinement_clauses


def _quoted(value):
    return json.dumps(value, ensure_ascii=False)


def _choices(values):
    return ' or '.join(_quoted(value) for value in values)


def _text(condition):
    for group, joiner in (('and', ' AND '), ('or', ' OR ')):
        if group in condition:
            return '(' + joiner.join(_text(part) for part in condition[group]) + ')'
    operation = 'contains' if 'contains' in condition else 'not_contains'
    return ('contains ' if operation == 'contains' else 'does not contain ') + _quoted(condition[operation]) + (
        ' (case-sensitive)' if condition.get('case_sensitive') else ' (ignoring letter case)')


def _selector(value):
    rows = []
    if 'source_families' in value:
        rows.append('Engine emitter is ' + _choices(value['source_families']) + '.')
    if 'templates' in value:
        refs = ['; '.join(k.replace('_', ' ') + ' ' + _quoted(v) for k, v in ref.items()) for ref in value['templates']]
        rows.append('Use the stored error pattern identified by ' + ' OR '.join(refs) + '.')
    if 'template_exact' in value:
        rows.append('The error pattern itself must exactly equal ' + _choices(value['template_exact']) + '.')
    if 'template_text' in value:
        rows.append('The error pattern itself ' + _text(value['template_text']) + '; values filled into the pattern do not count.')
    if 'message' in value:
        rows.append('The complete diagnostic message, including template literals and populated slot values, ' + _text(value['message']) + '.')
    if 'identities' in value:
        rows.append(f'Keep only the {len(value["identities"])} exact diagnostic record(s) specified in the query, including all their identifying values and locations.')
    for binding in value.get('bindings', []):
        location = ', '.join(f'{k.replace("_", " ")} {binding[k]}' for k in ('region', 'slot_id') if k in binding)
        rows.append(f'A {binding["type"]} value must ' + (
            'equal ' + _quoted(binding['value']) if binding.get('present', True) else 'be absent') +
            (f' at {location}' if location else '') + '.')
    if 'match_status' in value:
        rows.append('Stored classification must be ' + _choices(value['match_status']) +
                    '; this describes how a specific diagnostic was recognized.')
    if 'selectors' in value:
        rows.append(f'Also satisfy at least one of {len(value["selectors"])} alternative groups; all conditions within a group must hold. The full groups are listed in Effective filters.')
    if 'has_source_reference' in value:
        rows.append('The stored diagnostic must ' + ('identify' if value['has_source_reference'] else 'not identify') + ' a file path. Paths can come from a <LOCATOR> value or literal stored text; a line number alone does not identify a file. This does not require the file to exist today.')
    for name, bound in value.get('occurrences', {}).items():
        rows.append(f'Its count in the selected Run must be {"at least" if name == "min" else "at most"} {bound}.')
    if 'newly_observed' in value:
        rows.append('Keep ' + ('only newly observed diagnostics' if value['newly_observed'] else 'only diagnostics that are not newly observed') + ' within the included comparison window.')
    for clause in value.get('all', []):
        rows.extend(_selector(clause))
    return rows


def _source(value):
    if not value:
        return []
    rows = []
    if 'members' in value:
        members = [' AND '.join(k.replace('_', ' ') + ' = ' + _quoted(v) for k, v in m.items()) for m in value['members']]
        rows.append('Look for the diagnostic\'s referenced file inside the current source root of a recorded playset member with ' + ' OR '.join(members) +
                    ('. Test path resolution within that member scope.' if 'resolution' in value else '. Keep the diagnostic only when a matching file is found there.') +
                    ' For each file/line, the last matching member in load order is the error source.')
    labels = {'files': 'The diagnostic must reference file path', 'referenced_paths': 'The stored message must reference path',
              'roots': 'Search source roots', 'directories': 'Search directories', 'extensions': 'Keep file extensions',
              'filename_globs': 'File name must match wildcard', 'path_globs': 'File path must match wildcard',
              'include': 'File path must match wildcard', 'exclude': 'Exclude file paths matching wildcard'}
    for key, label in labels.items():
        if key in value:
            rows.append(label + ' ' + _choices(value[key]) + '.')
    for key, label in (('filename', 'File name'), ('relative_path', 'Relative file path')):
        if key in value:
            if 'exact' in value[key]:
                rows.append(label + ' equals ' + _choices(value[key]['exact']) + '.')
            if 'text' in value[key]:
                rows.append(label + ' ' + _text(value[key]['text']) + '.')
    if 'exact' in value.get('relative_path', {}):
        rows.append('This is a path relative to each source root; an optional leading / means the same relative location. '
                    'By default, check that location beneath every member of this Run\'s recorded playset. '
                    'Exact-path lookup examines only the parent folder in each selected root, without descending into other folders. '
                    'Show every matching candidate, including copies in different mods.')
    if 'content' in value:
        rows.append('Current file contents ' + _text(value['content']) + '.')
    if 'recursive' in value:
        rows.append('Include subdirectories.' if value['recursive'] else 'Do not descend into subdirectories.')
    if value.get('reference_mode') == 'basename':
        rows.append('Match stored file references by file name only, within the selected scope.')
    if 'resolution' in value:
        rows.append('Keep diagnostics with at least one recorded path for which ' +
                    ('a completed search finds no current file in this source scope.' if value['resolution'] == 'unresolved' else
                     'a current file is found in this source scope.'))
        rows.append('Messages with no usable path do not match. An incomplete search is not evidence that a file is missing. File existence is tested before any separate file-content condition.')
    if not {'roots', 'members', 'content', 'resolution'} & value.keys():
        rows.append('Match recorded file paths; files need not exist on disk. Diagnostics without a matching usable path are excluded normally.')
    return rows


QUESTIONS = {
    'frequent': 'Which specific diagnostic messages occur most often in the selected Run?',
    'hotspots': 'Which referenced files are associated with the largest numbers of diagnostics?',
    'syntax': 'Which diagnostics match the nine researched syntax-error conditions for this processing package?',
    'new': 'Which diagnostics appear in the selected Run but were absent from every successfully read earlier Run in this comparison?',
    'symbol': 'Which specific diagnostics match the selected error patterns or typed values?',
    'custom': 'Which diagnostics satisfy the combined conditions below, and in which Runs do they appear?',
}


def explain(payload, *, requested_run=None):
    if payload['status'] != 'completed':
        if payload.get('failure_stage') == 'input_validation' and payload['status'] == 'invalid_query':
            return {'question': 'Is the report request complete and valid before submitting it?',
                    'conditions': [],
                    'expected': ['Validate the required inputs before requesting Run metadata or processing an investigation.'],
                    'result': [payload['error'], 'The CLI rejected this request before any database request; no investigation was submitted.'],
                    'reading_guide': ['This is an input-validation response, not a diagnostic search result.']}
        if payload['status'] in {'operation_failed', 'read_unavailable'}:
            operation = payload.get('request', {}).get('operation', 'report')
            return {'question': f'Did the {operation} operation complete?', 'conditions': [],
                    'expected': ['Return an execution error with its operation, stage and exception details when the operation cannot complete.'],
                    'result': [f'{payload["exception_class"]}: {payload["error"]}',
                               'Stopped during ' + payload.get('failure_stage', 'execution') + '.'],
                    'reading_guide': ['This response reports an execution error. It makes no claim about how many diagnostics match the query.']}
        partial = payload.get('partial') or {}
        query = partial.get('effective_query') or {}
        results = [payload['error']]
        if partial:
            results.append(f'{partial.get("known_matching_records", 0)} known matching diagnostic(s) are retained; the complete answer is unavailable.')
            if 'resolution' in query.get('scope', {}).get('source', {}):
                reasons = ' '.join(dict.fromkeys(i['reason'] for i in partial.get('coverage', {}).get('issues', [])))
                results.append('Current path resolution is unknown for the unevaluated references. ' + reasons)
        return {'question': f'Can the requested investigation of Run {requested_run or "specified in the command"} be evaluated?',
                'conditions': _selector(query.get('refinement', {})) + _source(query.get('scope', {}).get('source', {})),
                'expected': ['An invalid selection or unavailable required evidence must produce a clear failure, not a successful report with zero matches.'],
                'result': results,
                'reading_guide': ['This is a failed or incomplete investigation. Any displayed diagnostics are partial evidence only.']}
    if 'eligible_count' in payload:
        return {'question': 'Which stored Runs belong to this processing package?',
                'conditions': [f'Processing package: {payload["package_id"]}.'],
                'expected': ['List every matching Run, including unavailable source timestamps. Apply pagination after package selection.'],
                'result': [f'{payload["eligible_count"]} eligible Runs; {len(payload["runs"])} shown on this page.'],
                'reading_guide': ['Each row is a Run, not a diagnostic. Run-ID ordering does not imply session chronology. Missing-time Runs remain queryable but cannot enter chronological windows.']}
    query = payload['effective_query']
    refinement, scope = query['refinement'], query['scope']
    preset = payload['presentation']['preset']['name']
    conditions = _selector(scope) + _selector(refinement) + _source(scope.get('source', {}))
    context = payload['presentation'].get('source_context', {})
    if context:
        conditions.append('Optional source lookup uses the following settings. These settings alone do not filter stored diagnostics; required source filters take precedence.')
        conditions.extend(_source(context))
    expected = ['Every listed diagnostic must satisfy all the combined filters. If the conditions cannot hold together, the result is successfully empty. Different messages and identifying values remain separate, with their own counts.']
    fields = {k for c in refinement_clauses(refinement) for s in [c, *c.get('selectors', [])] for k in s}
    if fields & {'templates', 'template_exact', 'template_text'}:
        expected.append('Show the shared error patterns first, then the specific diagnostics recognized using them. A template filter can return many different diagnostics; it does not select just one filled-in message.')
    if 'identities' in fields:
        expected.append('Exact-record selection keeps only the specified diagnostic identities, even when many other records use the same error pattern.')
    if 'message' in fields:
        expected.append('Search the whole diagnostic, including template literals and populated slot values. Show where each search term matched and the template already assigned to each record.')
    if scope.get('source') or preset == 'hotspots':
        expected.append('Show all matching files with load order, mod name, path and line in separate columns. For each file/line, mark the last matching member in load order as the error source. Resolved means one or more paths found; File not found means none found.')
    if 'resolution' in scope.get('source', {}):
        expected.append('Show the current resolution of each recorded reference, separately from the stored message. A message may contain both resolved and unresolved paths; one selected path with the requested status is sufficient. This describes sources at report generation time, not at the time of the original Run.')
    if preset == 'frequent':
        expected.append('List specific diagnostics in descending occurrence count; this ranks frequency, not severity.')
    if preset == 'syntax':
        expected.append('Keep the researched syntax conditions, including the exact assignment-error reason. Generic trigger errors and failed context switches alone are insufficient.')
    if preset == 'new':
        expected.append('New means absent from the successfully read predecessors in this window, not first seen in all history. With no included predecessors, every positive record is new within that window.')
    total, window = payload['totals'], payload['window']
    result = [f'Run {payload["run"]["run_id"]}: {total["distinct_records"]} different diagnostics, occurring {total["occurrences"]} times. '
              f'{len(payload["records"])} diagnostics are displayed; counts include every match.']
    if not total['distinct_records']:
        result.append('The query completed successfully and found no matching diagnostic in the selected Run.')
    source_coverage = payload.get('coverage', {}).get('source', {}).get(payload['run']['run_id'], {})
    no_path = source_coverage.get('records_without_source_path', 0)
    if no_path:
        result.append(f'{no_path} diagnostic emission' + (' supplies' if no_path == 1 else 's supply') +
                      ' no file path; source lookup is not applicable for ' + ('that emission.' if no_path == 1 else 'those emissions.'))
    counts = source_coverage.get('search_counts')
    if counts is not None:
        result.append(f'Source lookup for this Run checked {counts["files_searched"]:,} file names/paths in '
                      f'{counts["folders_searched"]:,} folders within the effective lookup scope. '
                      'Source coverage below lists the directories and cache use; this is separate from reading file contents.')
    if query['analytics']['history'] and not window['history_available']:
        result.append(window['unavailable_reason'])
        conditions.append('Return the selected-Run results without chronological comparisons.')
    elif query['analytics']['history']:
        n = query['analytics'].get('trailing_runs')
        conditions.append(f'Compare up to {n} eligible Runs ending at the selected Run (including that Run).' if n else
                          'Compare up to five eligible Runs before and five after the selected Run.')
        result.append(f'{len(window["runs"])} Runs are included; {window["totals"]["successful_reads"]} were successfully read. '
                      f'Together they contain {window["totals"]["distinct_records"]} matching distinct diagnostics and {window["totals"]["occurrences"]} occurrences.')
        result.append(f'{total["historical_entries"]} matching earlier diagnostics are absent from the selected Run and are counted separately.')
    else:
        conditions.append('Read only the selected Run; comparison history is turned off.')
    guide = ['D1, D2 and the other D entries are individual diagnostics. Their headings count repetitions of that exact diagnostic in the selected Run. '
             'An error template is a shared pattern containing placeholders such as <KEY> and <REASON>; the diagnostic fills those placeholders with specific values.',
             'The recorded message is preserved as written. Matching files show load order, mod name, path and line separately. '
             'Base-game and DLC files have no mod name. Multiple matches remain visible; the last in load order is the error source for each file/line.']
    if window['history_available']:
        guide.append('Occurrences by Run shows where each diagnostic was observed. Zero means it was not observed in that Run. '
                     'Previously observed entries have zero occurrences in the selected Run.')
    return {'question': QUESTIONS[preset], 'conditions': conditions, 'expected': expected,
            'result': result, 'reading_guide': guide}
