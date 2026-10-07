"""Caller-side analysis over public handler reads. No filesystem or SQL access."""
from collections import defaultdict
from copy import deepcopy
from dataclasses import asdict, dataclass
from datetime import datetime
import json
from typing import Protocol

from ..pipeline.contracts import identity_data, render, render_segments
from ..pipeline.request_handler import COMPLETED, HandlerClient
from ..journal import get_journal
from ..runtime_logging import event, get_logger
from .query import InvestigationQuery, QueryError, SELECTOR_FIELDS, evaluate_text, _integer, refinement_clauses

LOGGER = get_logger('reporting')
journal = get_journal('reporting')


class ReadError(RuntimeError):
    """An ordinary handler failure; never a successful empty read."""
    def __init__(self, operation, run_id, error, exception_class=None):
        super().__init__(f'{operation} ({run_id}): {error}')
        self.operation, self.run_id = operation, run_id
        self.error, self.exception_class = error, exception_class

    def to_dict(self):
        return dict(operation=self.operation, run_id=self.run_id, error=self.error,
                    exception_class=self.exception_class)


class RunSelectionError(ValueError):
    def __init__(self, message, exclusions=()):
        super().__init__(message)
        self.exclusions = list(exclusions)


class SourceEvaluationError(RuntimeError):
    """08A.2 unavailable/incomplete required filter; partial evidence is not zero."""
    def __init__(self, message, partial=None):
        super().__init__(message)
        self.partial = partial


class SourceResolver(Protocol):
    def resolve(self, run: dict, records: list[dict], scope: dict | None) -> dict:
        """08A.2 batch boundary, outside the worker, once per successfully read Run.

        Return {complete: bool, coverage: dict, matches: list[identity_key],
                references: {identity_key: list[str]},
                reference_resolution: {identity_key: list[dict]},
                reference_status: {identity_key: str},
                file_line_sources: {identity_key: list[dict]},
                candidates: {identity_key: list[dict]}}.
        Each candidate has a stable candidate_id plus provenance/context fields.
        With required scope, matches expresses ALL its composed conditions;
        complete=False raises SourceEvaluationError retaining this partial value.
        Without scope, incomplete optional context does not remove diagnostics.
        """


def _encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def exact_identity(record: dict) -> dict:
    """Portable full equality selector, scoped to the stored definition revision."""
    return {'definition': {k: record['definition'][k] for k in (
        'model_revision', 'contract_version', 'template_id')},
        'equality': identity_data(record['values'])}


def identity_key(record: dict) -> str:
    """Lossless canonical equality key, NOT a digest or Run-local row identifier."""
    return _encode(exact_identity(record))


def template_text(definition: dict) -> str:
    """Stored body parts as literal/placeholder text, independent of bound values.

    Uses <TYPE> placeholders, slot prefix/suffix and declared literal alternatives
    as {a|b}. This is definition.parts (the matched error template), not optional
    wrapper/support layouts. Those remain available in the returned definition.
    """
    def parts_text(parts):
        result = []
        for part in parts:
            if part['kind'] == 'literal':
                # Formatted literals already declare their display text (for
                # example {game date}); the instance retains its exact spelling.
                result.append('{' + '|'.join(part['alternatives']) + '}'
                              if 'alternatives' in part else part['text'])
            elif part['kind'] == 'slot':
                result.append(part['prefix'] + '<' + part['type'] + '>' + part['suffix'])
            elif part['kind'] == 'repeat':
                layouts = ' | '.join(parts_text(layout) for layout in part['layouts'])
                result.append(f'{{repeat {part["name"]} ({part["structure"]}); '
                              f'minimum {part["minimum"]}; layouts: [{layouts}]}}')
            else:
                raise ValueError(f'unsupported template part kind: {part["kind"]}')
        return ''.join(result)

    return parts_text(definition['parts'])


def package_runs(runs: list[dict], package_id: str) -> list[dict]:
    """Ordinary eligibility is package membership, independent of source time."""
    if not isinstance(package_id, str) or not package_id:
        raise QueryError('an explicit nonempty processing package_id is required')
    return [run for run in runs if run['lineage'].get('package_id') == package_id]


def chronology(runs: list[dict], package_id: str) -> dict:
    """Chronological placement only; exclusions remain ordinary queryable Runs."""
    eligible, exclusions, times = [], [], {}
    for run in package_runs(runs, package_id):
        stamp = run['facts'].get('error_log_source_modified_at')
        try:
            if not isinstance(stamp, str) or 'T' not in stamp:
                raise ValueError('expected ISO timestamp')
            parsed = datetime.fromisoformat(stamp)
            if parsed.utcoffset() is None:
                raise ValueError('timestamp has no UTC offset')
        except (ValueError, OverflowError):
            exclusions.append({'run_ids': [run['run_id']], 'timestamp': stamp,
                               'reason': 'missing or unusable source-log modification timestamp'})
            continue
        times[run['run_id']] = parsed
        eligible.append(run)
    eligible.sort(key=lambda r: times[r['run_id']])
    return {'package_id': package_id, 'runs': eligible, 'exclusions': exclusions}


def frequency_observation(selected: int, preceding: list[int | None],
                          subsequent: list[int | None] = ()) -> dict:
    """Counts/presence in the included window; None is not an observation.

    New means present now and absent from every included predecessor. This is
    relative to this window, including a window with no preceding observations.
    """
    before = [c for c in preceding if c is not None]
    after = [c for c in subsequent if c is not None]
    return {'selected_count': selected,
            'preceding_observed': sum(c > 0 for c in before), 'preceding_read': len(before),
            'subsequent_observed': sum(c > 0 for c in after), 'subsequent_read': len(after),
            'preceding_fraction': [sum(c > 0 for c in before), len(before)] if before else None,
            'subsequent_fraction': [sum(c > 0 for c in after), len(after)] if after else None,
            'newly_observed': selected > 0 and not any(c > 0 for c in before),
            'comparison_complete': all(c is not None for c in preceding)
                                   and all(c is not None for c in subsequent)}


def window_positions(runs, requested):
    """Requested relative positions; an unavailable position is not a zero count."""
    selected = next(i for i, run in enumerate(runs) if run['role'] == 'selected')
    indexed = {i - selected: run for i, run in enumerate(runs)}
    preceding = requested.get('preceding', requested.get('trailing_runs', 1) - 1)
    subsequent = requested.get('subsequent', 0)
    return [{'offset': offset, 'run_id': indexed.get(offset, {}).get('run_id'),
             'available': offset in indexed} for offset in range(-preceding, subsequent + 1)]


def _matches(record, selector, text, pattern):
    definition = record['definition']
    if 'source_families' in selector and definition['source_family'] not in selector['source_families']:
        return False
    if 'match_status' in selector and record['match_status'] not in selector['match_status']:
        return False
    if 'templates' in selector and not any(
            all(definition[k] == v for k, v in ref.items()) for ref in selector['templates']):
        return False
    if 'identities' in selector and exact_identity(record) not in selector['identities']:
        return False
    if 'template_exact' in selector and pattern not in selector['template_exact']:
        return False
    if not evaluate_text(text, selector.get('message')) or not evaluate_text(pattern, selector.get('template_text')):
        return False
    for predicate in selector.get('bindings', []):
        if not any(
                ('region' not in predicate or region['name'] == predicate['region'])
                and all(binding[k] == v for k, v in predicate.items() if k != 'region')
                and binding['present'] == predicate.get('present', True)
                for region in record['values']['regions'] for binding in region['bindings']):
            return False
    return True


def _record_matches(record, query):
    text = render(record['definition'], record['values'])
    pattern = template_text(record['definition'])
    scope, refinement = query['scope'], query['refinement']
    if 'has_source_reference' in scope:
        from .source_references import source_references
        if bool(source_references(record)['references']) != scope['has_source_reference']:
            return False
    if not _matches(record, {k: v for k, v in scope.items() if k == 'source_families'}, text, pattern):
        return False
    for clause in refinement_clauses(refinement):
        if 'has_source_reference' in clause:
            from .source_references import source_references
            if bool(source_references(record)['references']) != clause['has_source_reference']:
                return False
        selector = {k: v for k, v in clause.items() if k in SELECTOR_FIELDS}
        if not _matches(record, selector, text, pattern) or ('selectors' in clause and not any(
                _matches(record, part, text, pattern) for part in clause['selectors'])):
            return False
    return True


def message_matches(record, query):
    """Locate positive content-search terms using the stored render assignment.

    Only satisfied message/selector branches contribute terms. Exclusions have
    no matching span. Offsets refer to the complete rendered diagnostic, including
    phrases crossing literal/slot boundaries; no classification is performed.
    """
    text = render(record['definition'], record['values'])
    pattern = template_text(record['definition'])
    terms = set()

    def collect(expression):
        if not expression or not evaluate_text(text, expression):
            return
        for group in ('and', 'or'):
            if group in expression:
                for part in expression[group]:
                    collect(part)
                return
        if 'contains' in expression:
            terms.add((expression['contains'], expression.get('case_sensitive', False)))

    for clause in refinement_clauses(query['refinement']):
        collect(clause.get('message'))
        for selector in clause.get('selectors', []):
            if _matches(record, selector, text, pattern):
                collect(selector.get('message'))
    if not terms:
        return []
    segments = render_segments(record['definition'], record['values'])
    # Unicode casefold can expand characters. Map folded offsets back to the
    # original message rather than treating them as original character indices.
    folded = text.casefold()
    offsets = [i for i, character in enumerate(text) for _ in character.casefold()]
    result = []
    for term, sensitive in sorted(terms):
        haystack, needle = (text, term) if sensitive else (folded, term.casefold())
        cursor = 0
        seen = set()
        while (found := haystack.find(needle, cursor)) >= 0:
            start = found if sensitive else offsets[found]
            end = found + len(needle) if sensitive else offsets[found + len(needle) - 1] + 1
            cursor = found + 1
            if (start, end) in seen:
                continue
            seen.add((start, end))
            origins = [{**{k: v for k, v in s.items() if k not in {'text', 'start', 'end'}},
                        'start': max(start, s['start']), 'end': min(end, s['end']),
                        'text': text[max(start, s['start']):min(end, s['end'])]}
                       for s in segments if s['start'] < end and start < s['end']]
            result.append(dict(term=term, case_sensitive=sensitive, start=start, end=end,
                               text=text[start:end], origins=origins))
    return result


def message_match_rollups(entries):
    """Where content matches occur; overlapping origins retain unique identities."""
    details, associations = {}, {}
    for entry in entries:
        keys = set()
        for match in entry['message_matches']:
            for origin in match['origins']:
                detail = {k: match[k] for k in ('term', 'case_sensitive')}
                detail.update(kind=origin['kind'])
                if origin['kind'] == 'slot':
                    detail['type'] = origin['type']
                key = _encode(detail)
                details[key] = detail
                keys.add(key)
        associations[entry['identity_key']] = keys
    result = rollup(entries, associations)
    definitions = {e['identity_key']: e['identity']['definition'] for e in entries}
    for bucket in result['buckets']:
        bucket['message_match'] = details[bucket['key']]
        bucket['templates'] = list({_encode(definitions[k]): definitions[k]
                                    for k in bucket['identity_keys']}.values())
    return result


def rollup(entries: list[dict], associations: dict[str, list[str]]) -> dict:
    """Distinct identity buckets; overlap is disclosed, never a unique grand sum."""
    buckets = defaultdict(list)
    overlap = unassociated = 0
    for entry in entries:
        keys = set(associations.get(entry['identity_key'], []))
        overlap += len(keys) > 1
        unassociated += not keys
        for key in keys:
            buckets[key].append(entry)
    rows = [{'key': key, 'occurrences': sum(e['selected_count'] for e in group),
             'distinct_records': len(group), 'identity_keys': [e['identity_key'] for e in group]}
            for key, group in buckets.items()]
    rows.sort(key=lambda row: (-row['occurrences'], row['key']))
    return {'buckets': rows, 'overlapping_records': overlap, 'unassociated_records': unassociated,
            'bucket_totals_are_additive': overlap == 0}


def template_rollups(entries):
    """Count exact diagnostics by stored definition, independent of source context."""
    definitions = {_encode(e['identity']['definition']): {
        **e['identity']['definition'], 'source_family': e['stored_record']['definition']['source_family'],
        'text': e['template_text']} for e in entries}
    templates = rollup(entries, {e['identity_key']: [_encode(e['identity']['definition'])] for e in entries})
    for bucket in templates['buckets']:
        bucket['template'] = definitions[bucket['key']]
    return templates


def source_rollups(entries):
    """Group full template definitions and source associations before display limits."""
    candidates = {e['identity_key']: [c['candidate_id'] for c in e['candidates']] for e in entries}
    details = {c['candidate_id']: c for e in entries for c in e['candidates']}
    files = rollup(entries, candidates)
    for bucket in files['buckets']:
        bucket['candidate'] = {k: v for k, v in details[bucket['key']].items()
                               if k not in {'references', 'excerpts', 'matching_lines'}}
    return {'emitters': rollup(entries, {e['identity_key']: [e['stored_record']['definition']['source_family']]
                                        for e in entries}),
            'referenced_files': rollup(entries, {e['identity_key']: e['references'] for e in entries}),
            'candidate_files': files, 'templates': template_rollups(entries),
            'message_matches': message_match_rollups(entries)}


def window_rollups(runs):
    """Combine actual per-Run association counts, with distinct full identities.

    Combining per-Run buckets preserves changing candidate membership: an
    identity's count is only added to candidates associated in that same Run.
    """
    identities = {k for run in runs for k in (run['identity_counts'] or {})}
    result = {}
    for kind in ('emitters', 'referenced_files', 'candidate_files', 'templates', 'message_matches'):
        buckets, associations = {}, defaultdict(set)
        for run in runs:
            if run['rollups'] is None:
                continue
            for row in run['rollups'][kind]['buckets']:
                bucket = buckets.setdefault(row['key'], {'key': row['key'], 'occurrences': 0,
                    'identity_keys': set(), 'run_ids': [],
                    **{field: row[field] for field in ('candidate', 'template', 'message_match') if field in row}})
                if kind == 'message_matches':
                    refs = bucket.setdefault('templates', {})
                    refs.update({_encode(ref): ref for ref in row['templates']})
                bucket['occurrences'] += row['occurrences']
                bucket['identity_keys'].update(row['identity_keys'])
                bucket['run_ids'].append(run['run_id'])
                for key in row['identity_keys']:
                    associations[key].add(row['key'])
        rows = [{**b, 'identity_keys': sorted(b['identity_keys']), 'distinct_records': len(b['identity_keys'])}
                for b in buckets.values()]
        if kind == 'message_matches':
            for row in rows:
                row['templates'] = list(row['templates'].values())
        rows.sort(key=lambda b: (-b['occurrences'], b['key']))
        overlap = sum(len(v) > 1 for v in associations.values())
        result[kind] = {'buckets': rows, 'overlapping_records': overlap,
                        'unassociated_records': len(identities - associations.keys()),
                        'bucket_totals_are_additive': overlap == 0}
    return result


@dataclass
class InvestigationResult:
    run: dict
    package_id: str
    effective_query: dict
    filter_meaning: dict
    chronology_exclusions: list
    window: dict
    totals: dict
    records: list
    historical: list
    rollups: dict
    review: dict | None
    coverage: dict

    def to_dict(self):
        return asdict(self)


class DiagnosticAnalysis:
    """Only HandlerClient performs reads. This class never owns a database worker."""
    def __init__(self, client: HandlerClient, *, source_resolver: SourceResolver | None = None):
        self.client, self.source_resolver = client, source_resolver

    def _read(self, operation, **arguments):
        try:
            outcome = self.client.result(self.client.submit(operation, arguments))
        except (LookupError, OSError, EOFError, RuntimeError) as exc:
            raise ReadError(operation, arguments.get('run_id'), str(exc), type(exc).__name__) from exc
        if outcome.status != COMPLETED:
            raise ReadError(operation, arguments.get('run_id'), outcome.error, outcome.exception_class)
        return outcome.value

    def list_runs(self, package_id: str, *, offset: int = 0, limit: int | None = None) -> dict:
        """All package Runs in Run-ID order, without implying session chronology."""
        _integer(offset, 'offset')
        if limit is not None:
            _integer(limit, 'limit')
        rows = sorted(package_runs(self._read('list_runs'), package_id), key=lambda r: r['run_id'])
        return {'package_id': package_id, 'exclusions': [],
                'chronology_exclusions': chronology(rows, package_id)['exclusions'],
                'ordering': 'Run ID ascending (not session chronology)',
                'runs': rows[offset:None if limit is None else offset + limit],
                'eligible_count': len(rows), 'offset': offset, 'limit': limit}

    def search_runs(self, *, package_id: str, query: InvestigationQuery | dict,
                    offset: int = 0, limit: int | None = None) -> dict:
        """Search every package Run, independently of the chronological window.

        Counts and refinements are evaluated in each Run. Pagination follows
        matching, and a failed read propagates rather than becoming a nonmatch.
        """
        with journal.call():
            _integer(offset, 'offset')
            if limit is not None:
                _integer(limit, 'limit')
            value = (query.to_dict() if isinstance(query, InvestigationQuery) else deepcopy(query))
            analytics = value.get('analytics', {})
            if 'trailing_runs' in analytics or any('newly_observed' in c for c in
                    refinement_clauses(value.get('refinement', {}))):
                raise QueryError('all-Run search does not supply chronological refinements')
            value['analytics'] = {'history': False, 'include_absent': False}
            effective = InvestigationQuery.from_dict(value)
            listing = self.list_runs(package_id)
            matched = []
            for metadata in listing['runs']:
                result = self.investigate(metadata['run_id'], package_id=package_id, query=effective)
                if result.totals['distinct_records']:
                    matched.append({'run': metadata, 'totals': result.totals})
            return {'package_id': package_id, 'ordering': listing['ordering'],
                    'searched_count': listing['eligible_count'], 'matching_count': len(matched),
                    'runs': matched[offset:None if limit is None else offset + limit],
                    'offset': offset, 'limit': limit, 'effective_query': effective.to_dict()}

    def investigate(self, run: str, *, package_id: str,
                    query: InvestigationQuery | dict | None = None) -> InvestigationResult:
        """Select Run/latest in one explicit package and investigate stored records."""
        effective = (query if isinstance(query, InvestigationQuery) else
                     InvestigationQuery.from_dict({} if query is None else query)).to_dict()
        if not isinstance(run, str) or not run:
            raise QueryError('Run ID or latest must be a nonempty string')
        source_scope = effective['scope'].get('source')
        if source_scope and self.source_resolver is None:
            raise SourceEvaluationError('source filtering requires a SourceSearch resolver on DiagnosticAnalysis')
        begin = getattr(self.source_resolver, 'begin_investigation', None)
        if begin is not None:
            begin()
        all_runs = package_runs(self._read('list_runs'), package_id)
        order = chronology(all_runs, package_id)
        runs = order['runs']
        selected = next((r for r in all_runs if r['run_id'] == run), None)
        if run == 'latest':
            selected = runs[-1] if runs else None
            if selected is None:
                raise RunSelectionError('no eligible Run is available in this processing package', order['exclusions'])
        elif selected is None:
            known = self._read('get_run', run_id=run)
            raise RunSelectionError(f'Run {run}: ' + ('unknown Run' if known is None else
                                    'does not belong to the selected processing package'))
        placed = selected in runs
        index = runs.index(selected) if placed else None
        analytics = effective['analytics']
        history = analytics['history']
        history_available = history and placed
        history_reason = (None if history_available else 'History was not requested.' if not history else
                          'Chronological context unavailable: selected Run has no usable source-log modification timestamp.')
        if not placed and any('newly_observed' in c for c in refinement_clauses(effective['refinement'])):
            raise RunSelectionError('Chronological novelty filtering is unavailable for this Run: '
                                    'missing or unusable source-log modification timestamp.', order['exclusions'])
        trailing = analytics.get('trailing_runs')
        before = runs[max(0, index - (trailing - 1 if trailing else 5)):index] if history_available else []
        after = runs[index + 1:index + 6] if history_available and trailing is None else []
        chosen = [*before, selected, *after]
        selected_id = selected['run_id']
        event(LOGGER, 'investigation_started', run_id=selected_id, package_id=package_id)
        data, failures, unavailable, sources = {}, {}, {}, {}
        for metadata in chosen:
            run_id = metadata['run_id']
            try:
                # read_diagnostics returns [] for a missing Run; check existence so
                # a disappeared Run cannot masquerade as zero evidence.
                current = self._read('get_run', run_id=run_id)
                if current != metadata:
                    reason = ('Run is no longer available' if current is None else
                              'Run metadata changed after window selection; repeat the query')
                    if run_id == selected_id:
                        raise RunSelectionError(f'Run {run_id}: {reason}')
                    unavailable[run_id] = {'run_id': run_id, 'reason': reason}
                    event(LOGGER, 'comparison_run_not_available', **unavailable[run_id])
                    continue
                rows = self._read('read_diagnostics', run_id=run_id)
            except ReadError as exc:
                if run_id == selected_id:
                    raise
                failures[run_id] = exc.to_dict()
                event(LOGGER, 'comparison_read_unavailable', level='WARNING', **exc.to_dict())
                continue
            data[run_id] = {identity_key(row): row for row in rows}
        review = self._read('read_review_metadata', run_id=selected_id)
        current = data[selected_id]
        # All window identities are needed for filtered per-Run totals. Only selected
        # and preceding identities enter the two displayed comparison views.
        representatives = dict(current)
        origins = {key: selected_id for key in current}
        for metadata in chosen:
            run_id = metadata['run_id']
            for key, row in data.get(run_id, {}).items():
                if key not in representatives:
                    representatives[key], origins[key] = row, run_id
        observations, qualifying = {}, set()
        for key, row in representatives.items():
            counts = {r['run_id']: (data[r['run_id']].get(key, {}).get('occurrence_count', 0)
                      if r['run_id'] in data else None) for r in chosen}
            observation = frequency_observation(counts[selected_id],
                [counts[r['run_id']] for r in before], [counts[r['run_id']] for r in after])
            observation['counts'] = counts
            if not history_available:
                observation.update(newly_observed=None, comparison_complete=False,
                                   preceding_observed=None, preceding_read=None,
                                   subsequent_observed=None, subsequent_read=None,
                                   unavailable_reason=history_reason)
            observations[key] = observation
            if not all(
                    clause.get('occurrences', {}).get('min', 0) <= counts[selected_id] <= clause.get('occurrences', {}).get('max', float('inf'))
                    and ('newly_observed' not in clause or observation['newly_observed'] == clause['newly_observed'])
                    for clause in refinement_clauses(effective['refinement'])):
                continue
            qualifying.add(key)

        if self.source_resolver:
            for metadata in chosen:
                rid = metadata['run_id']
                if rid not in data:
                    continue
                # SQL predicates and selected-Run count refinements precede source
                # association, so unrelated records cannot make its coverage fail.
                rows = [row for key, row in data[rid].items()
                        if key in qualifying and _record_matches(row, effective)]
                resolved = self.source_resolver.resolve(metadata, rows, source_scope)
                if source_scope and not resolved['complete']:
                    evidence_records = [
                        {'identity': exact_identity(row), 'identity_key': identity_key(row),
                         'stored_record': deepcopy(row), 'message': render(row['definition'], row['values']),
                         'message_matches': message_matches(row, effective),
                         'template_text': template_text(row['definition']),
                         'origin': {'run_id': rid, 'definition_id': row['definition_id'], 'ordinal': row['ordinal']},
                         'selected_count': observations[identity_key(row)]['selected_count'],
                         'history': observations[identity_key(row)],
                         'references': resolved['references'].get(identity_key(row), []),
                         'reference_details': resolved.get('reference_details', {}).get(identity_key(row), []),
                         'reference_resolution': resolved.get('reference_resolution', {}).get(identity_key(row), []),
                         'source_path_status': resolved.get('reference_status', {}).get(identity_key(row), 'not_evaluated'),
                         'file_line_sources': resolved.get('file_line_sources', {}).get(identity_key(row), []),
                         'candidates': resolved['candidates'].get(identity_key(row), [])}
                        for row in rows]
                    partial_records = [e for e in evidence_records if e['identity_key'] in resolved['matches']]
                    raise SourceEvaluationError('required source filter cannot be evaluated completely',
                        {**resolved, 'run': metadata, 'effective_query': effective,
                         'chronology_exclusions': order['exclusions'],
                         'records': partial_records[:effective['display']['limit']],
                         'known_matching_records': len(partial_records)})
                sources[rid] = resolved

        def matches(key, row, origin):
            return (key in qualifying and _record_matches(row, effective)
                    and (not source_scope or key in sources[origin]['matches']))

        match_annotations = {}

        def entry(key, row, origin):
            if key not in match_annotations:
                match_annotations[key] = message_matches(row, effective)
            return {'identity': exact_identity(row), 'identity_key': key,
                    'origin': {'run_id': origin, 'definition_id': row['definition_id'], 'ordinal': row['ordinal']},
                    'stored_record': deepcopy(row), 'message': render(row['definition'], row['values']),
                    'message_matches': match_annotations[key],
                    'template_text': template_text(row['definition']),
                    'selected_count': observations[key]['selected_count'], 'history': observations[key],
                    'references': sources.get(origin, {}).get('references', {}).get(key, []),
                    'reference_details': sources.get(origin, {}).get('reference_details', {}).get(key, []),
                    'reference_resolution': sources.get(origin, {}).get('reference_resolution', {}).get(key, []),
                    'source_path_status': sources.get(origin, {}).get('reference_status', {}).get(key, 'not_evaluated'),
                    'file_line_sources': sources.get(origin, {}).get('file_line_sources', {}).get(key, []),
                    'candidates': sources.get(origin, {}).get('candidates', {}).get(key, [])}

        present = [entry(k, row, selected_id) for k, row in current.items() if matches(k, row, selected_id)]
        preceding_keys = {k for r in before for k in data.get(r['run_id'], {})}
        absent = [entry(k, representatives[k], origins[k]) for k in preceding_keys - current.keys()
                  if analytics['include_absent'] and matches(k, representatives[k], origins[k])]
        present.sort(key=lambda e: (-e['selected_count'], e['identity_key']))
        absent.sort(key=lambda e: e['identity_key'])
        per_run = []
        for metadata in chosen:
            rid = metadata['run_id']
            matched = {k: row for k, row in data.get(rid, {}).items() if matches(k, row, rid)}
            contributing = [dict(entry(k, row, rid), run_count=row['occurrence_count'])
                            for k, row in matched.items()]
            contributing.sort(key=lambda e: (-e['run_count'], e['identity_key']))
            run_rollups = source_rollups([dict(e, selected_count=e['run_count']) for e in contributing])
            per_run.append({'run_id': rid, 'timestamp': metadata['facts'].get('error_log_source_modified_at'),
                            'role': 'selected' if rid == selected_id else 'preceding' if metadata in before else 'subsequent',
                            'occurrences': sum(r['occurrence_count'] for r in matched.values()) if rid in data else None,
                            'distinct_records': len(matched) if rid in data else None,
                            'identity_counts': {k: r['occurrence_count'] for k, r in matched.items()} if rid in data else None,
                            'records': contributing[:effective['display']['limit']] if rid in data else None,
                            'rollups': run_rollups if rid in data else None,
                            'read_error': failures.get(rid), 'unavailable': unavailable.get(rid)})
        emitter = {e['identity_key']: [e['stored_record']['definition']['source_family']] for e in present}
        requested_window = {'trailing_runs': trailing} if trailing else {
            'preceding': 5 if history else 0, 'subsequent': 5 if history else 0}
        result = InvestigationResult(
            run=selected, package_id=package_id, effective_query=effective,
            filter_meaning={'composition': 'Scope AND refinement AND each refinement.all condition; selectors OR within a condition; templates OR; bindings AND. Mutually exclusive filters return an empty result.',
                            'occurrences': 'Counts in selected Run, including zero for historical entries.',
                            'source': 'Path predicates match stored references; no matching usable path means exclusion. Resolution explicitly tests current file existence within the effective source scope. Unresolved requires a completed search with no candidate for at least one selected reference; no usable reference is a nonmatch. These are current observations, not stored facts about historical source contents.',
                            'template_text': 'Stored body literals and <TYPE> placeholders; repeat sections show declared minimum and alternative layouts, not an instance count. Formatted literals use their declared display text. Case-insensitive partial predicates by default; exact text is case-sensitive.',
                            'message': 'Search the complete diagnostic: template literals and populated slot values together. Match origins describe the existing stored assignment; they do not reclassify the record.',
                            'history': 'Exact definition-scoped contract identity; frequency, not severity or proof of repair.',
                            'newly_observed': 'Present in selected Run and absent from every successfully read preceding Run in this window.',
                            'per_run': 'Same filters; occurrence and novelty refinements remain anchored to the selected Run.'},
            chronology_exclusions=order['exclusions'],
            window={'requested': requested_window,
                    'chronology_available': placed, 'history_available': history_available,
                    'unavailable_reason': history_reason,
                    'positions': window_positions(per_run, requested_window) if placed else [],
                    'obtained': {'preceding': len(before), 'subsequent': len(after),
                                 'preceding_read': sum(r['run_id'] in data for r in before),
                                 'subsequent_read': sum(r['run_id'] in data for r in after)},
                    'runs': per_run, 'complete': not failures and not unavailable and (not history or placed),
                    'totals': {'occurrences': sum(r['occurrences'] or 0 for r in per_run),
                               'distinct_records': len({k for r in per_run for k in (r['identity_counts'] or {})}),
                               'successful_reads': len(data)},
                    'rollups': window_rollups(per_run)},
            totals={'occurrences': sum(e['selected_count'] for e in present), 'distinct_records': len(present),
                    'historical_entries': len(absent)},
            records=present[:effective['display']['limit']], historical=absent[:effective['display']['historical_limit']],
            rollups=source_rollups(present) if self.source_resolver else
                    {'emitters': rollup(present, emitter), 'referenced_files': None, 'candidate_files': None,
                     'templates': template_rollups(present), 'message_matches': message_match_rollups(present)},
            review=review,
            coverage={'diagnostics': 'Stored template and provisional records; native review payload is not searched.',
                      'comparison_errors': list(failures.values()),
                      'comparison_unavailable': list(unavailable.values()),
                      'source': {rid: value['coverage'] for rid, value in sources.items()} if self.source_resolver else
                                {'available': False, 'reason': 'No optional source resolver supplied.'},
                      'filter_complete': True})
        validate_details = getattr(self.source_resolver, 'validate_details', None)
        if history and not placed:
            result.window['obtained'] = {key: None for key in result.window['obtained']}
            result.totals['historical_entries'] = None
        if validate_details is not None:
            # Header warnings describe source files, not stored diagnostic
            # membership/counts. Only the returned detail set needs these reads.
            detail_sets = defaultdict(list)
            for item in [*result.records, *result.historical,
                         *(e for r in result.window['runs'] for e in (r['records'] or []))]:
                detail_sets[item['origin']['run_id']].append(item)
            for rid, entries in detail_sets.items():
                validation = validate_details(rid, entries)
                result.coverage['source'].setdefault(rid, {})['encoding_validation'] = validation
        event(LOGGER, 'investigation_completed', run_id=selected_id, package_id=package_id,
              distinct_records=result.totals['distinct_records'], occurrences=result.totals['occurrences'])
        return result
