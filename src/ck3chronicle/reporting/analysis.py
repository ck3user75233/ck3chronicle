"""Caller-side analysis over public handler reads. No filesystem or SQL access."""
from collections import defaultdict
from copy import deepcopy
from dataclasses import asdict, dataclass
from datetime import datetime
import json
from typing import Protocol

from ..pipeline.contracts import identity_data, render
from ..pipeline.request_handler import COMPLETED, HandlerClient
from ..runtime_logging import event, get_logger
from .query import InvestigationQuery, QueryError, SELECTOR_FIELDS, evaluate_text, _integer

LOGGER = get_logger('reporting')


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
    return ''.join(
        ('{' + '|'.join(p['alternatives']) + '}' if 'alternatives' in p else p['text'])
        if p['kind'] == 'literal' else p['prefix'] + '<' + p['type'] + '>' + p['suffix']
        for p in definition['parts'])


def chronology(runs: list[dict], package_id: str) -> dict:
    """All package eligibility before any pagination. Input order is irrelevant.

    Standard datetime orders usable aware ISO timestamps. Duplicate groups use
    the stored strings themselves, never precision-reduced datetime values.
    """
    if not isinstance(package_id, str) or not package_id:
        raise QueryError('an explicit nonempty processing package_id is required')
    groups = defaultdict(list)
    exclusions, times = [], {}
    for run in runs:
        if run['lineage'].get('package_id') != package_id:
            continue
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
        groups[stamp].append(run)
    eligible = []
    for stamp, members in groups.items():
        if len(members) > 1:
            exclusions.append({'run_ids': [r['run_id'] for r in members], 'timestamp': stamp,
                               'reason': 'duplicate source-log modification timestamp',
                               'guidance': 'Inspect duplicated session data or overwritten/corrupted timestamps.'})
        else:
            eligible.extend(members)
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
    selector = {k: v for k, v in refinement.items() if k in SELECTOR_FIELDS}
    return (_matches(record, {k: v for k, v in scope.items() if k == 'source_families'}, text, pattern)
            and _matches(record, selector, text, pattern)
            and ('selectors' not in refinement or any(
                _matches(record, part, text, pattern) for part in refinement['selectors'])))


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
        """Newest eligible first; exclusions concern the entire package, not the page."""
        _integer(offset, 'offset')
        if limit is not None:
            _integer(limit, 'limit')
        result = chronology(self._read('list_runs'), package_id)
        rows = list(reversed(result['runs']))
        return {**result, 'runs': rows[offset:None if limit is None else offset + limit],
                'eligible_count': len(rows), 'offset': offset, 'limit': limit}

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
        order = chronology(self._read('list_runs'), package_id)
        runs = order['runs']
        selected = next((r for r in runs if r['run_id'] == run), None)
        if run == 'latest':
            selected = runs[-1] if runs else None
            if selected is None:
                raise RunSelectionError('no eligible Run is available in this processing package', order['exclusions'])
        elif selected is None:
            excluded = [e for e in order['exclusions'] if run in e['run_ids']]
            if excluded:
                raise RunSelectionError(f'Run {run} excluded: {excluded[0]["reason"]}. '
                                        + excluded[0].get('guidance', ''), order['exclusions'])
            known = self._read('get_run', run_id=run)
            raise RunSelectionError(f'Run {run}: ' + ('unknown Run' if known is None else
                                    'does not belong to the selected processing package'))
        index = runs.index(selected)
        analytics = effective['analytics']
        history = analytics['history']
        trailing = analytics.get('trailing_runs')
        before = runs[max(0, index - (trailing - 1 if trailing else 5)):index] if history else []
        after = runs[index + 1:index + 6] if history and trailing is None else []
        chosen = [*before, selected, *after]
        selected_id = selected['run_id']
        event(LOGGER, 'investigation_started', run_id=selected_id, package_id=package_id)
        data, failures, sources = {}, {}, {}
        for metadata in chosen:
            run_id = metadata['run_id']
            try:
                # read_diagnostics returns [] for a missing Run; check existence so
                # a disappeared Run cannot masquerade as zero evidence.
                current = self._read('get_run', run_id=run_id)
                if current != metadata:
                    raise ReadError('get_run', run_id, 'Run unavailable or changed during investigation')
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
            observations[key] = observation
            count_filter = effective['refinement'].get('occurrences', {})
            if not count_filter.get('min', 0) <= counts[selected_id] <= count_filter.get('max', float('inf')):
                continue
            if 'newly_observed' in effective['refinement']:
                if observation['newly_observed'] != effective['refinement']['newly_observed']:
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
                    raise SourceEvaluationError('required source association coverage is incomplete', resolved)
                sources[rid] = resolved

        def matches(key, row, origin):
            return (key in qualifying and _record_matches(row, effective)
                    and (not source_scope or key in sources[origin]['matches']))

        def entry(key, row, origin):
            return {'identity': exact_identity(row), 'identity_key': key,
                    'origin': {'run_id': origin, 'definition_id': row['definition_id'], 'ordinal': row['ordinal']},
                    'stored_record': deepcopy(row), 'message': render(row['definition'], row['values']),
                    'template_text': template_text(row['definition']),
                    'selected_count': observations[key]['selected_count'], 'history': observations[key],
                    'references': sources.get(origin, {}).get('references', {}).get(key, []),
                    'reference_details': sources.get(origin, {}).get('reference_details', {}).get(key, []),
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
            per_run.append({'run_id': rid, 'timestamp': metadata['facts']['error_log_source_modified_at'],
                            'role': 'selected' if rid == selected_id else 'preceding' if metadata in before else 'subsequent',
                            'occurrences': sum(r['occurrence_count'] for r in matched.values()) if rid in data else None,
                            'distinct_records': len(matched) if rid in data else None,
                            'identity_counts': {k: r['occurrence_count'] for k, r in matched.items()} if rid in data else None,
                            'read_error': failures.get(rid)})
        emitter = {e['identity_key']: [e['stored_record']['definition']['source_family']] for e in present}
        references = {e['identity_key']: e['references'] for e in present}
        candidates = {e['identity_key']: [c['candidate_id'] for c in e['candidates']] for e in present}
        result = InvestigationResult(
            run=selected, package_id=package_id, effective_query=effective,
            filter_meaning={'composition': 'Scope AND refinement; selectors OR; templates OR; bindings AND.',
                            'occurrences': 'Counts in selected Run, including zero for historical entries.',
                            'template_text': 'Stored body literals and <TYPE> placeholders; case-insensitive partial predicates by default; exact text is case-sensitive.',
                            'history': 'Exact definition-scoped contract identity; frequency, not severity or proof of repair.',
                            'newly_observed': 'Present in selected Run and absent from every successfully read preceding Run in this window.',
                            'per_run': 'Same filters; occurrence and novelty refinements remain anchored to the selected Run.'},
            chronology_exclusions=order['exclusions'],
            window={'requested': {'trailing_runs': trailing} if trailing else {'preceding': 5 if history else 0, 'subsequent': 5 if history else 0},
                    'obtained': {'preceding': len(before), 'subsequent': len(after),
                                 'preceding_read': sum(r['run_id'] in data for r in before),
                                 'subsequent_read': sum(r['run_id'] in data for r in after)},
                    'runs': per_run, 'complete': not failures},
            totals={'occurrences': sum(e['selected_count'] for e in present), 'distinct_records': len(present),
                    'historical_entries': len(absent)},
            records=present[:effective['display']['limit']], historical=absent[:effective['display']['historical_limit']],
            rollups={'emitters': rollup(present, emitter),
                     'referenced_files': rollup(present, references) if self.source_resolver else None,
                     'candidate_files': rollup(present, candidates) if self.source_resolver else None},
            review=review,
            coverage={'diagnostics': 'Stored template and provisional records; native review payload is not searched.',
                      'comparison_errors': list(failures.values()),
                      'source': {rid: value['coverage'] for rid, value in sources.items()} if self.source_resolver else
                                {'available': False, 'reason': 'No optional source resolver supplied.'},
                      'filter_complete': True})
        event(LOGGER, 'investigation_completed', run_id=selected_id, package_id=package_id,
              distinct_records=result.totals['distinct_records'], occurrences=result.totals['occurrences'])
        return result
