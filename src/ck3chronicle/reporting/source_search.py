"""Read-only inventories and batched ripgrep searches of explicit source scopes."""
from collections import defaultdict
from copy import deepcopy
import fnmatch
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tempfile
from time import perf_counter

from ..runtime_logging import event, get_logger
from ..decoder import HEADER_INSPECTION_BYTES, Decoder, inspect_source_header, normalize_newlines, physical_lines
from .analysis import DiagnosticAnalysis, SourceEvaluationError, identity_key
from .query import QueryError, evaluate_group, evaluate_text
from .source_query import normalize_source
from .source_references import source_references

LOGGER = get_logger('source_search')


def _physical(path):
    # Ordinary lexical path access; no link resolution or root discovery.
    return os.path.normcase(os.path.abspath(path))


def _relative(path):
    return str(path).replace('\\', '/').removeprefix('./')


def _issue(path, reason, error=None):
    return {'path': str(path) if path is not None else None, 'reason': reason,
            'error': str(error) if error is not None else None}


def _leaves(expression):
    if 'and' in expression or 'or' in expression:
        for child in next(iter(expression.values())):
            yield from _leaves(child)
    else:
        yield expression


def file_line_sources(candidates):
    """Apply the owner's last-load-order rule independently to each file/line.

    Pure analysis of resolved file associations; no presentation or disk access.
    Outside-playset files have no load order and cannot be ordered by this rule.
    """
    groups = {}
    for candidate in candidates:
        for ref in candidate['references']:
            key = (candidate['relative_path'], ref.get('line'))
            group = groups.setdefault(key, {})
            group[candidate['candidate_id']] = candidate
    result = []
    for (path, line), members in groups.items():
        choices = list(members.values())
        orders = [(c.get('member') or {}).get('load_order') for c in choices]
        reason, source = None, None
        if line is None:
            reason = 'No line supplied.'
        elif any(order is None for order in orders):
            reason = 'Load order unavailable.'
        else:
            last = [c for c, order in zip(choices, orders) if order == max(orders)]
            if len(last) == 1:
                c = last[0]
                source = {k: deepcopy(c[k]) for k in ('candidate_id', 'member', 'relative_path', 'physical_path')}
            else:
                reason = 'No unique last load order.'
        result.append({'relative_path': path, 'line': line, 'rule': 'last_load_order',
                       'candidate_ids': list(members), 'error_source': source, 'reason': reason})
    return result


class SourceSearch:
    """One in-memory source-search session, also an 08A.1 SourceResolver.

    Explicit roots work without client/run/playset. context supplies optional
    default source roots/search options for investigations. Required scope.source
    is separate. A new investigation clears caches; repeated standalone searches
    reuse inventories until clear(). No persistent index or source writes.

    Path-only filters select recorded references. candidate_context=True opts
    reports into optional disk candidates for them. Their default remains SQL-only. Disk coverage
    stays separate from completion of that stored-reference predicate.

    Default disk scope: every accessible member root in the selected Run's
    recorded playset, recursively. This is stored Run provenance, not today's
    active playset. Explicit roots/members narrow the root set before disk access;
    directories and recursive narrow traversal. Exact files/relative references
    further restrict enumeration to their parent directories, nonrecursively.
    Filename-only/basename searches traverse the requested directory scope because
    no parent path is known. Inventories contain paths, not all file contents;
    content reads occur only for requested content searches or excerpts.
    """
    def __init__(self, client=None, *, ripgrep='rg', context=None, excerpts=False, scratch_directory=None,
                 candidate_context=False, decoder=None):
        self.reader = DiagnosticAnalysis(client) if client is not None else None
        self.ripgrep = str(ripgrep)
        self.context = normalize_source(context) if context else {}
        self.excerpts = excerpts
        self.candidate_context = candidate_context
        self.scratch_directory = scratch_directory
        self.decoder = decoder if decoder is not None else Decoder()
        self.clear()

    def clear(self):
        self._inventories = {}
        self._playsets = {}
        self._contents = {}
        self._decoded_files = {}
        self._decoding_results = {}
        self._excerpt_cache = {}
        self._header_cache = {}
        self.metrics = {'inventory_builds': 0, 'inventory_cache_hits': 0, 'inventoried_files': 0,
                        'inventoried_folders': 0,
                        'inventory_scopes': [],
                        'inventory_seconds': 0.0, 'content_seconds': 0.0,
                        'ripgrep_invocations': [], 'reference_lookup_seconds': 0.0}

    def begin_investigation(self):
        self.clear()

    def _validate_candidate_header(self, candidate, run_id):
        """Header reads must belong to an actual recorded member, including links."""
        unavailable = {'status': 'unavailable', 'warnings': [], 'bytes_inspected': 0,
                       'scope': f'First {HEADER_INSPECTION_BYTES} bytes'}
        playset = self._stored_playset(run_id) or {}
        member = candidate.get('member')
        if not member or member not in playset.get('members', []):
            return {**unavailable, 'reason': 'Header validation requires a recorded playset member.'}
        try:
            root = Path(member['path']).resolve()
            selected_root = Path(candidate['root']).resolve()
            path = Path(candidate['physical_path']).resolve()
            if not path.is_relative_to(root) or not path.is_relative_to(selected_root):
                return {**unavailable, 'reason': 'Resolved file escapes its recorded or selected root.'}
            if str(path) in self._decoding_results:
                decoded, issue = self._read_source(path)
                return deepcopy(decoded.header) if decoded else {**unavailable, 'reason': issue['reason']}
            stat = path.stat()
            key = (str(path), stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns)
            if key not in self._header_cache:
                with path.open('rb') as stream:
                    raw = stream.read(HEADER_INSPECTION_BYTES + 1)
                after = path.stat()
                if (stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                    return {**unavailable, 'reason': 'File changed during header validation.'}
                self._header_cache[key] = inspect_source_header(
                    raw[:HEADER_INSPECTION_BYTES], end_of_file=len(raw) <= HEADER_INSPECTION_BYTES)
            return deepcopy(self._header_cache[key])
        except (OSError, ValueError, RuntimeError) as exc:
            return {**unavailable, 'reason': str(exc)}

    def validate_sources(self, selection, *, run_id):
        """Validate every matching file header through the existing source scope."""
        selection = normalize_source(selection)
        playset = self._stored_playset(run_id) or {}
        members = playset.get('members', [])
        if selection.get('roots'):
            for root in selection['roots']:
                if not any(m.get('path') and _physical(m['path']) == _physical(root) for m in members):
                    raise QueryError('Header validation roots must be recorded member roots; narrow them with directories/files.')
            selection.setdefault('members', [{'load_order': m['load_order']} for m in members
                                             if m.get('path') and any(_physical(m['path']) == _physical(r) for r in selection['roots'])])
        # Header validation establishes containment before any content search.
        # The search owner still applies all ordinary path/member predicates.
        content = selection.get('content')
        result = self.search({k: v for k, v in selection.items() if k != 'content'}, run_id=run_id)
        for candidate in result['files']:
            candidate['encoding_validation'] = self._validate_candidate_header(candidate, run_id)
        result['coverage']['encoding_validation'] = self._validation_coverage(result['files'])
        if content:
            eligible = [c for c in result['files'] if c['encoding_validation']['status'] != 'unavailable']
            matched, issues = self._content(eligible, content)
            for candidate in eligible:
                candidate['decoding'] = deepcopy(self._decoding_results[str(Path(candidate['physical_path']).resolve())])
            result['coverage']['decoding'] = [{'path': c['physical_path'], **c['decoding']}
                                             for c in {c['physical_path']: c for c in eligible}.values()]
            result['files'] = [{**c, 'matching_lines': matched[c['physical_path']]} for c in eligible if c['physical_path'] in matched]
            result['coverage']['issues'].extend(issues)
            result['coverage']['complete'] &= not issues and result['coverage']['encoding_validation']['unavailable_files'] == 0
            result['coverage']['search_counts'].update(
                content_files_requested=len({_physical(c['physical_path']) for c in eligible}),
                matching_files=len({_physical(c['physical_path']) for c in result['files']}))
            result['coverage']['matching_file_associations'] = len(result['files'])
            result['coverage']['unique_matching_files'] = result['coverage']['search_counts']['matching_files']
        result['effective_selection'] = deepcopy(selection)
        return result

    @staticmethod
    def _validation_coverage(candidates):
        values = {c['physical_path']: c['encoding_validation'] for c in candidates}
        return {'scope': f'First {HEADER_INSPECTION_BYTES} bytes of each requested file',
                'requested_files': len(values),
                'inspected_files': sum(v['status'] in {'checked', 'critical', 'undetermined'} for v in values.values()),
                'critical_files': sum(v['status'] == 'critical' for v in values.values()),
                'unavailable_files': sum(v['status'] == 'unavailable' for v in values.values()),
                'undetermined_files': sum(v['status'] == 'undetermined' for v in values.values()),
                'complete': all(v['status'] in {'checked', 'critical'} for v in values.values())}

    def validate_details(self, run_id, entries):
        """Attach warnings to requested detail only, after diagnostic ranking."""
        candidates = [c for e in entries for c in e['candidates']]
        for candidate in candidates:
            candidate['encoding_validation'] = self._validate_candidate_header(candidate, run_id)
            decoded = self._decoding_results.get(str(Path(candidate['physical_path']).resolve()))
            if decoded:
                candidate['decoding'] = deepcopy(decoded)
        for entry in entries:
            by_id = {c['candidate_id']: c for c in entry['candidates']}
            for reference in entry.get('reference_resolution', []):
                selected = [by_id[i] for i in reference['candidate_ids'] if i in by_id]
                reference['encoding_validation'] = {
                    **self._validation_coverage(selected),
                    'not_inspected_candidate_ids': [i for i in reference['candidate_ids'] if i not in by_id],
                    'warnings': [{**w, 'candidate_id': c['candidate_id'], 'physical_path': c['physical_path'],
                                  'member': c['member']} for c in selected
                                 for w in c['encoding_validation']['warnings']]}
                if reference['encoding_validation']['not_inspected_candidate_ids']:
                    reference['encoding_validation']['complete'] = False
        return self._validation_coverage(candidates)

    def _stored_playset(self, run_id):
        if self.reader is None:
            raise QueryError('a HandlerClient is required to read a recorded playset')
        if run_id not in self._playsets:
            run = self.reader._read('get_run', run_id=run_id)
            if run is None:
                raise QueryError(f'unknown Run: {run_id}')
            self._playsets[run_id] = self.reader._read('read_playset', run_id=run_id)
        return deepcopy(self._playsets[run_id])

    def read_playset(self, run_id):
        """Stored members, including repeats/nulls, plus current root availability."""
        stored = self._stored_playset(run_id)
        available = bool(stored and stored.get('playset_captured'))
        members = []
        for member in stored.get('members', []) if stored else []:
            members.append({'member': member, **self._availability(member['path'])})
        return {'run_id': run_id, 'available': available, 'stored': stored, 'members': members,
                'reason': None if available else 'Recorded playset is unavailable.'}

    @staticmethod
    def _availability(path):
        try:
            if not path or not Path(path).is_absolute():
                return {'available': False, 'reason': 'missing or non-absolute recorded root'}
            if Path(path).is_file():
                return {'available': False, 'reason': 'unsupported archive/file mount'}
            with os.scandir(path):
                pass
            return {'available': True, 'reason': None}
        except OSError as exc:
            return {'available': False, 'reason': str(exc)}

    def _roots(self, run_id, selection):
        explicit = selection.get('roots')
        member_filters = selection.get('members')
        issues, roots = [], []
        if explicit is not None and member_filters is None:
            for index, path in enumerate(explicit):
                if not Path(path).is_absolute():
                    raise QueryError('explicit source roots must be absolute directories')
                roots.append({'path': path, 'member': None, 'order': index})
        else:
            if run_id is None:
                return [], [_issue(None, 'No explicit roots or selected Run playset supplied.')]
            # Select stored members before probing disk. read_playset's public
            # availability listing intentionally checks every member; a scoped
            # search must not use that listing to probe unrelated mod roots.
            playset = self._stored_playset(run_id)
            if not playset or not playset.get('playset_captured'):
                return [], [_issue(None, 'Recorded playset is unavailable.')]
            selected = [m for m in playset['members'] if not member_filters or any(
                all(m[key] == value for key, value in selector.items()) for selector in member_filters)]
            if member_filters:
                for selector in member_filters:
                    if not any(all(m[key] == value for key, value in selector.items()) for m in selected):
                        issues.append(_issue(None, 'Requested member is absent from the stored playset.', json.dumps(selector)))
            for member in selected:
                if explicit is None or (member['path'] and any(_physical(member['path']) == _physical(p) for p in explicit)):
                    roots.append({'path': member['path'], 'member': member, 'order': member['load_order']})
        for root in roots:
            root.update(self._availability(root['path']))
            if not root['available']:
                issues.append(_issue(root['path'], root['reason']))
        return roots, issues

    def _inventory(self, root, directories, recursive):
        key = (_physical(root), tuple(directories), recursive)
        if key in self._inventories:
            self.metrics['inventory_cache_hits'] += 1
            return self._inventories[key], 'exact_scope'
        whole = self._inventories.get((_physical(root), ('.',), True))
        if whole is not None and not whole['issues']:
            prefixes = [os.path.normcase(_relative(d).strip('/').removeprefix('./')) for d in directories]
            def included(path):
                for prefix in prefixes:
                    normalized = os.path.normcase(path)
                    separator = os.path.normcase('/')
                    tail = path if prefix == '.' else path[len(prefix) + 1:] if normalized.startswith(prefix + separator) else None
                    if tail is not None and (recursive or '/' not in tail):
                        return True
                return False
            def included_folder(path):
                normalized = os.path.normcase(path)
                return any(normalized == prefix or (recursive and (
                    prefix == '.' or normalized.startswith(prefix + os.path.normcase('/')))) for prefix in prefixes)
            value = {'files': [p for p in whole['files'] if included(p)], 'issues': [],
                     'folders': [p for p in whole['folders'] if included_folder(p)]}
            self._inventories[key] = value
            self.metrics['inventory_cache_hits'] += 1
            return value, 'whole_root_subset'
        started = perf_counter()
        measurement = {'root': root, 'directories': list(directories), 'recursive': recursive}
        self.metrics['inventory_scopes'].append(measurement)
        files, folders, issues = set(), set(), []
        def error(exc):
            issues.append(_issue(exc.filename or root, 'Directory traversal failed.', exc))
        for directory in directories:
            base = Path(root).joinpath(*PurePosixPath(_relative(directory)).parts)
            try:
                # A directory absent under an otherwise available member is a
                # known empty scope, not an unreadable root.
                if not base.exists():
                    continue
                if recursive:
                    for parent, _, names in os.walk(base, onerror=error):
                        folders.add(Path(parent).relative_to(root).as_posix())
                        for name in names:
                            files.add(Path(parent, name).relative_to(root).as_posix())
                else:
                    with os.scandir(base) as entries:
                        folders.add(base.relative_to(root).as_posix())
                        for entry in entries:
                            if entry.is_file():
                                files.add(Path(entry.path).relative_to(root).as_posix())
            except OSError as exc:
                error(exc)
        value = {'files': sorted(files), 'folders': sorted(folders), 'issues': issues}
        measurement.update(files_searched=len(files), folders_searched=len(folders), complete=not issues)
        self._inventories[key] = value
        self.metrics['inventory_builds'] += 1
        self.metrics['inventoried_files'] += len(files)
        self.metrics['inventoried_folders'] += len(folders)
        self.metrics['inventory_seconds'] += perf_counter() - started
        return value, 'none'

    @staticmethod
    def _path_matches(relative, physical, selection):
        sensitive = selection.get('case_sensitive', False)
        norm = (lambda s: s) if sensitive else str.casefold
        relative = _relative(relative)
        name = PurePosixPath(relative).name
        if 'referenced_paths' in selection:
            refnorm = (lambda p: PurePosixPath(_relative(p)).name) if selection.get('reference_mode') == 'basename' else _relative
            if norm(refnorm(relative)) not in {norm(refnorm(p)) for p in selection['referenced_paths']}:
                return False
        if 'files' in selection and not any(
                norm(_relative(physical)) == norm(_relative(p)) if Path(p).is_absolute() else
                norm(relative) == norm(_relative(p)) for p in selection['files']):
            return False
        if 'extensions' in selection and norm(PurePosixPath(name).suffix) not in {
                norm('.' + e.lstrip('.')) for e in selection['extensions']}:
            return False
        for field, text in (('filename', name), ('relative_path', relative)):
            condition = selection.get(field, {})
            if 'exact' in condition and norm(text) not in {norm(_relative(p)) for p in condition['exact']}:
                return False
            if not evaluate_text(text, condition.get('text')):
                return False
        for field, text in (('filename_globs', name), ('path_globs', relative), ('include', relative)):
            if field in selection and not any(fnmatch.fnmatchcase(norm(text), norm(p)) for p in selection[field]):
                return False
        return not any(fnmatch.fnmatchcase(norm(relative), norm(p)) for p in selection.get('exclude', []))

    @staticmethod
    def _lookup_scope(root, selection, reference_paths):
        """Intersect known exact paths with explicit scope before enumeration.

        Each list of exact paths is an OR; independent constraints intersect.
        A missing named file is a nonmatch. Basenames have no implied
        parent. Directory inventory preserves actual filename spelling.
        """
        directories = selection.get('directories', ['.'])
        recursive = selection.get('recursive', True)
        norm = (lambda s: s) if selection.get('case_sensitive', False) else str.casefold
        groups = []
        if 'files' in selection:
            groups.append(selection['files'])
        if reference_paths is not None and selection.get('reference_mode') != 'basename':
            groups.append(reference_paths)
        if 'referenced_paths' in selection and selection.get('reference_mode') != 'basename':
            groups.append(selection['referenced_paths'])
        if 'exact' in selection.get('relative_path', {}):
            groups.append(selection['relative_path']['exact'])
        if not groups:
            return directories, recursive
        allowed = None
        for group in groups:
            paths = {}
            for value in group:
                path = Path(_relative(value))
                if path.is_absolute():
                    try:
                        path = path.relative_to(root)
                    except ValueError:
                        continue  # Outside this selected root.
                relative = PurePosixPath(path.as_posix())
                if relative.is_absolute() or '..' in relative.parts:
                    continue
                paths[norm(relative.as_posix())] = relative
            allowed = paths if allowed is None else {k: v for k, v in allowed.items() if k in paths}
        parents = set()
        for path in allowed.values():
            parent = path.parent.as_posix()
            for directory in directories:
                scope = PurePosixPath(_relative(directory)).as_posix()
                if norm(parent) == norm(scope) or (recursive and (
                        scope == '.' or norm(parent).startswith(norm(scope).rstrip('/') + '/'))):
                    parents.add(parent)
                    break
        return sorted(parents), False

    def _files(self, run_id, selection, reference_paths=None):
        """Apply root/member/directory/exact-path scope before enumeration.

        An unscoped search inventories all selected roots recursively. A known
        path inventories only its parent directory, intersected with explicit
        scope; a filename-only query searches within the selected directory
        scope. Reuse never widens traversal. Repeated members retain associations.
        """
        roots, issues = self._roots(run_id, selection)
        files = []
        scopes, searched_files, searched_folders = [], set(), set()
        sensitive = selection.get('case_sensitive', False)
        norm = (lambda s: s) if sensitive else str.casefold
        refnorm = (lambda p: PurePosixPath(_relative(p)).name) if selection.get('reference_mode') == 'basename' else _relative
        allowed = {norm(refnorm(p)) for p in reference_paths} if reference_paths is not None else None
        for root in roots:
            scope = {'root': root['path'], 'member': root['member'], 'root_order': root['order'],
                     'directories': [], 'recursive': selection.get('recursive', True),
                     'files_searched': 0, 'folders_searched': 0, 'cache': 'none',
                     'complete': root['available']}
            scopes.append(scope)
            if not root['available']:
                scope['skipped'] = root['reason']
                continue
            directories, recursive = self._lookup_scope(root['path'], selection, reference_paths)
            scope.update(directories=list(directories), recursive=recursive)
            if not directories:
                scope['skipped'] = 'No referenced path lies in this root/directory scope.'
                continue
            inventory, cache = self._inventory(root['path'], directories, recursive)
            issues.extend(inventory['issues'])
            scope.update(files_searched=len(inventory['files']), folders_searched=len(inventory['folders']),
                         cache=cache, complete=not inventory['issues'])
            searched_folders.update(_physical(Path(root['path']) / p) for p in inventory['folders'])
            for relative in inventory['files']:
                path = os.path.join(root['path'], relative.replace('/', os.sep))
                searched_files.add(_physical(path))
                if allowed is not None and norm(refnorm(relative)) not in allowed and norm(_relative(path)) not in allowed:
                    continue
                if self._path_matches(relative, path, selection):
                    files.append({'candidate_id': json.dumps([root['order'], _physical(root['path']), relative], ensure_ascii=False),
                                  'root': root['path'], 'root_order': root['order'], 'member': root['member'],
                                  'relative_path': relative, 'physical_path': path})
        return roots, files, issues, scopes, {'files_searched': len(searched_files),
                                            'folders_searched': len(searched_folders)}

    def _reference_roots(self, run_id, selection):
        """Lexical relative/absolute path projection from metadata, without disk access."""
        if selection.get('roots') and not selection.get('members'):
            return selection['roots']
        if self.reader is None:
            return []
        playset = self._stored_playset(run_id) or {}
        return [m['path'] for m in playset.get('members', []) if m.get('path')
                and (not selection.get('members') or any(
                    all(m[k] == v for k, v in selector.items()) for selector in selection['members']))
                and (not selection.get('roots') or any(_physical(m['path']) == _physical(p) for p in selection['roots']))]

    @classmethod
    def _reference_matches(cls, path, selection, roots):
        """A recorded path either satisfies the path predicates or is excluded."""
        variants = [(path, path)]
        for root in roots:
            if Path(path).is_absolute():
                try:
                    variants.append((Path(path).relative_to(root).as_posix(), path))
                except ValueError:
                    continue
            else:
                variants.append((path, str(Path(root) / path)))
        norm = (lambda s: s) if selection.get('case_sensitive') else str.casefold
        for relative, physical in variants:
            if not cls._path_matches(relative, physical, selection):
                continue
            parent = norm(PurePosixPath(_relative(relative)).parent.as_posix())
            directories = selection.get('directories', ['.'] if selection.get('recursive') is False else None)
            if directories is None or any(
                    parent == norm(_relative(d).rstrip('/') or '.') or
                    (selection.get('recursive', True) and (d == '.' or parent.startswith(norm(_relative(d).rstrip('/')) + '/')))
                    for d in directories):
                return True
        return False

    def _read_source(self, path):
        try:
            path = Path(path).resolve()
            stat = path.stat()
            stamp = (stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns)
            if path in self._decoded_files:
                previous, decoded = self._decoded_files[path]
                if previous != stamp:
                    raise OSError('Source changed after reading; start a new search session.')
            else:
                decoded = self.decoder.read(path)
                after = path.stat()
                if stamp != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                    raise OSError('Source changed while reading.')
                self._decoded_files[path] = stamp, decoded
            self._decoding_results[str(Path(path).resolve())] = decoded.metadata()
            issue = None if decoded.text is not None else {
                **_issue(path, decoded.reason), 'decoding': decoded.metadata(), 'content_searched': False}
            return decoded, issue
        except OSError as exc:
            self._decoding_results[str(Path(path).resolve())] = {'status': 'unavailable', 'reason': str(exc)}
            return None, {**_issue(path, str(exc)), 'content_searched': False}

    def _content(self, files, expression):
        expression = deepcopy(expression)
        for predicate in _leaves(expression):
            op = 'contains' if 'contains' in predicate else 'not_contains'
            predicate[op] = normalize_newlines(predicate[op])
        paths = list(dict.fromkeys(f['physical_path'] for f in files))
        cache_key = (tuple(paths), json.dumps(expression, sort_keys=True))
        executable = shutil.which(self.ripgrep)
        if executable is None:
            raise SourceEvaluationError('ripgrep is required for content search. Install ripgrep for Windows '
                                        '(for example winget install BurntSushi.ripgrep.MSVC), or pass '
                                        'SourceSearch(ripgrep=the_full_path_to_rg_exe).')
        started = perf_counter()
        issues, usable, decoded_files = [], [], {}
        for path in paths:
            decoded, issue = self._read_source(path)
            if issue:
                issues.append(issue)
            else:
                usable.append(path)
                decoded_files[path] = decoded
        if not issues and cache_key in self._contents:
            return self._contents[cache_key]
        predicates = list(_leaves(expression))
        patterns = list(dict.fromkeys(p.get('contains', p.get('not_contains')) for p in predicates))
        found = defaultdict(set)
        unavailable = set()
        lines = defaultdict(dict)
        # Use case-insensitive broad matching whenever any leaf needs it; the
        # shared literal evaluator applies each leaf's own case setting below.
        insensitive = any(not p.get('case_sensitive', False) for p in predicates)
        with tempfile.TemporaryDirectory(prefix='ck3-source-', dir=self.scratch_directory) as scratch:
            transport = {}
            for index, path in enumerate(usable):
                target = Path(scratch, f'source-{index}.txt')
                target.write_bytes(decoded_files[path].working_text.encode('utf-8', errors='strict'))
                transport[_physical(target)] = path
            pattern_file = Path(scratch, 'patterns.txt')
            pattern_file.write_bytes(('\n'.join(patterns) + '\n').encode('utf-8'))
            arguments = [executable, '--no-config', '--json', '--fixed-strings', '--text',
                         '--hidden', '--no-ignore', '--encoding', 'none', '--no-mmap',
                         '--color', 'never', '--line-number', '--with-filename',
                         '--ignore-case' if insensitive else '--case-sensitive']
            if any('\n' in p or '\r' in p for p in patterns):
                arguments.append('--multiline')
                for pattern in patterns:
                    arguments.extend(['-e', pattern])
            else:
                arguments.extend(['-f', str(pattern_file)])
            batches, batch, size = [], [], sum(len(a) + 3 for a in arguments)
            for path in transport:
                # Windows command lines are limited; batching is transport sizing,
                # never a result cap. All selected files are sent exactly once.
                if batch and size + len(path) + 3 > 24000:
                    batches.append(batch)
                    batch, size = [], sum(len(a) + 3 for a in arguments)
                batch.append(path)
                size += len(path) + 3
            if batch:
                batches.append(batch)
            for batch in batches:
                with tempfile.TemporaryFile(dir=scratch) as stderr:
                    command = [*arguments, '--', *batch]
                    try:
                        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=stderr,
                            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
                    except OSError as exc:
                        issues.append(_issue(None, 'Could not start ripgrep.', exc))
                        unavailable.update(_physical(transport[p]) for p in batch)
                        continue
                    try:
                        for raw in process.stdout:
                            message = json.loads(raw)
                            if message['type'] != 'match':
                                continue
                            data = message['data']
                            path = data['path'].get('text')
                            text = data['lines'].get('text')
                            if path is None or text is None:
                                issues.append(_issue(path, 'ripgrep returned non-UTF-8 path or match data.'))
                                unavailable.update(_physical(transport[p]) for p in batch)
                                continue
                            key = _physical(transport[_physical(path)])
                            positive = False
                            for predicate in predicates:
                                op = 'contains' if 'contains' in predicate else 'not_contains'
                                literal = predicate[op]
                                if evaluate_text(text, {'contains': literal, 'case_sensitive': predicate.get('case_sensitive', False)}):
                                    found[key].add((literal, predicate.get('case_sensitive', False)))
                                    positive |= op == 'contains'
                            if positive:
                                for offset, line in enumerate(physical_lines(text)):
                                    lines[key][data['line_number'] + offset] = line
                        code = process.wait()
                    finally:
                        process.stdout.close()
                        if process.poll() is None:
                            process.terminate()
                            process.wait()
                    stderr.seek(0)
                    errors = stderr.read().decode('utf-8', errors='replace')
                    self.metrics['ripgrep_invocations'].append({'files': len(batch), 'exit_code': code,
                                                               'stderr': errors, 'options': arguments[1:-1]})
                    if code not in (0, 1) or errors:
                        issues.append(_issue(None, f'ripgrep search incomplete (exit {code}).', errors))
                        unavailable.update(_physical(transport[p]) for p in batch)
        def qualifies(path):
            key = _physical(path)
            # Known positive branches can qualify even when another OR branch
            # needs unavailable absence evidence. Unknown never becomes False.
            return evaluate_group(expression, lambda literal, sensitive:
                (literal, sensitive) in found[key], complete=key not in unavailable) is True
        matches = {path: [{'line': n, 'text': text} for n, text in sorted(lines[_physical(path)].items())]
                   for path in usable if qualifies(path)}
        self.metrics['content_seconds'] += perf_counter() - started
        self._contents[cache_key] = (matches, issues)
        return matches, issues

    def search(self, selection: dict, *, run_id: str | None = None) -> dict:
        """All matching files, ordered associations and explicit coverage. No result cap."""
        return self._search(selection, run_id)

    def _search(self, selection, run_id, reference_paths=None):
        selection = normalize_source(selection)
        roots, files, issues, scopes, counts = self._files(run_id, selection, reference_paths)
        inventory_count = len(files)
        counts['candidate_files'] = len({_physical(f['physical_path']) for f in files})
        counts['content_files_requested'] = counts['candidate_files'] if 'content' in selection else 0
        # Resolution concerns whether a referenced file exists in this scope,
        # independently of a separate content predicate on those files.
        reference_files = files
        if 'content' in selection:
            matched, errors = self._content(files, selection['content'])
            issues.extend(errors)
            files = [{**f, 'matching_lines': matched[f['physical_path']],
                      'decoding': deepcopy(self._decoding_results[str(Path(f['physical_path']).resolve())])}
                     for f in files if f['physical_path'] in matched]
        else:
            files = [{**f, 'matching_lines': []} for f in files]
        counts['matching_files'] = len({_physical(f['physical_path']) for f in files})
        coverage = {'complete': not issues, 'issues': issues, 'roots': roots,
                    'search_scopes': scopes, 'search_counts': counts,
                    'count_meaning': 'Per-search unique physical paths. Files searched counts names/paths examined in the effective lookup directories, before path/content filters; cached inventories count as examined. Folders include each searched starting directory and empty folders. Per-root rows may overlap and are not additive. Content files requested is separate from names/paths searched; issues disclose incomplete work.',
                    'selected_file_associations': inventory_count,
                    'matching_file_associations': len(files),
                    'unique_matching_files': len({_physical(f['physical_path']) for f in files}),
                    'settings': {'ignore_files': False, 'hidden_files': True, 'binary': 'searched as text when content requested',
                                 'encoding': self.decoder.settings(),
                                 'glob': 'fnmatchcase; slash is ordinary, case controlled explicitly'},
                    'metrics': deepcopy(self.metrics)}
        if 'content' in selection:
            coverage['decoding'] = [{'path': f['physical_path'],
                **deepcopy(self._decoding_results[str(Path(f['physical_path']).resolve())])}
                for f in {c['physical_path']: c for c in reference_files}.values()]
        event(LOGGER, 'source_search_completed', run_id=run_id,
              matching_files=len(files), complete=coverage['complete'])
        return {'effective_selection': deepcopy(selection), 'files': files, 'coverage': coverage,
                'reference_files': reference_files}

    def excerpts_for(self, paths_and_lines: dict[str, set[int]]) -> dict:
        """Search and excerpts share the same captured, decoded source text."""
        result = {}
        for path, targets in paths_and_lines.items():
            decoded, issue = self._read_source(path)
            if issue:
                for n in targets:
                    result[path, n] = {'available': False, 'reason': issue['reason'], 'line': n,
                                      'decoding': decoded.metadata() if decoded else {'status': 'unavailable'}}
                continue
            pending = {n for n in targets if (path, n) not in self._excerpt_cache}
            if pending:
                lines = physical_lines(decoded.working_text)
                total = len(lines)
                for n in pending:
                    if not 1 <= n <= total:
                        value = {'available': False, 'reason': 'Referenced line is outside the current file.',
                                 'line': n, 'total_lines': total}
                    else:
                        value = {'available': True, 'line': n, 'total_lines': total,
                                 'lines': [{'line': i, 'text': lines[i - 1], 'target': i == n}
                                           for i in range(max(1, n - 10), min(total, n + 10) + 1)]}
                    self._excerpt_cache[path, n] = {**value, 'decoding': decoded.metadata()}
            for n in targets:
                result[path, n] = self._excerpt_cache[path, n]
        return result

    def resolve(self, run, records, scope):
        """Batch source association for the shared diagnostic investigation.

        Exact references constrain disk lookup to their actual parent scopes;
        explicitly requested basename mode retains the broader directory search.
        A stored-reference-only predicate below avoids disk lookup altogether.
        """
        if scope:
            scope = normalize_source(scope, diagnostic=True)
        resolution_filter = (scope or {}).get('resolution')
        selection = {**self.context, **{k: v for k, v in (scope or {}).items() if k != 'resolution'}}
        # With no explicit selection, use the selected Run's stored playset.
        if not selection:
            selection = {'recursive': True}
        extracted = {identity_key(r): source_references(r) for r in records}
        # A path predicate is an ordinary recorded-value filter. Pathless and
        # nonmatching records do not make the query incomplete. Only predicates
        # about a current root/member/file's contents require disk association.
        reference_only = scope is not None and not {'roots', 'members', 'content', 'resolution'} & scope.keys()
        selected_references = {k: v['references'] for k, v in extracted.items()}
        if scope:
            paths = [*scope.get('files', []), *scope.get('referenced_paths', []),
                     *scope.get('relative_path', {}).get('exact', []),
                     *(r['path'] for value in extracted.values() for r in value['references'])]
            # Optional candidate context must not alter stored-path membership.
            roots = self._reference_roots(run['run_id'], scope) if any(Path(p).is_absolute() for p in paths) else []
            selected_references = {k: [r for r in value['references']
                                       if self._reference_matches(r['path'], scope, roots)]
                                   for k, value in extracted.items()}
            extracted = {k: v for k, v in extracted.items() if selected_references[k]}
        # Pathless emissions have no source lookup to perform. Do not probe a
        # playset/root and manufacture a coverage problem for those emissions.
        searched = (any(selected_references[k] for k in extracted)
                    and not (reference_only and not self.candidate_context))
        try:
            search = ({'files': [], 'coverage': {'complete': True, 'issues': [], 'roots': [], 'metrics': {},
                       'search_scopes': [], 'search_counts': {'files_searched': 0, 'folders_searched': 0,
                           'candidate_files': 0, 'matching_files': 0, 'content_files_requested': 0}}}
                      if not searched
                      else self._search(selection, run['run_id'],
                          {r['path'] for key in extracted for r in selected_references[key]}))
        except SourceEvaluationError as exc:
            search = {'files': [], 'coverage': {'complete': False, 'issues': [_issue(None, str(exc))], 'roots': []}}
        started = perf_counter()
        sensitive = selection.get('case_sensitive', False)
        norm = (lambda s: s) if sensitive else str.casefold
        by_relative, by_basename, by_absolute = defaultdict(list), defaultdict(list), defaultdict(list)
        for candidate in search['files']:
            by_relative[norm(candidate['relative_path'])].append(candidate)
            by_basename[norm(PurePosixPath(candidate['relative_path']).name)].append(candidate)
            by_absolute[_physical(candidate['physical_path'])].append(candidate)
        path_relative, path_basename, path_absolute = defaultdict(list), defaultdict(list), defaultdict(list)
        for candidate in search.get('reference_files', search['files']):
            path_relative[norm(candidate['relative_path'])].append(candidate)
            path_basename[norm(PurePosixPath(candidate['relative_path']).name)].append(candidate)
            path_absolute[_physical(candidate['physical_path'])].append(candidate)

        def lookup(ref, relative, basename, absolute):
            path = ref['path']
            if Path(path).is_absolute():
                return absolute[_physical(path)]
            if selection.get('reference_mode', 'relative') == 'basename':
                return basename[norm(PurePosixPath(path).name)]
            return relative[norm(path)]

        references, candidates, details, statuses, matches = {}, {}, {}, {}, []
        resolutions, attributions = {}, {}
        excerpts = defaultdict(set)
        for key, evidence in extracted.items():
            refs = evidence['references']
            references[key] = list(dict.fromkeys(r['path'] for r in refs))
            details[key] = refs
            statuses[key] = evidence['status']
            selected_refs = selected_references[key]
            resolutions[key] = []
            resolved_files = {}
            for ref in refs:
                found_paths = lookup(ref, path_relative, path_basename, path_absolute) if ref in selected_refs else []
                status = ('outside_scope' if ref not in selected_refs else 'not_searched' if not searched else
                          'resolved' if found_paths else 'unresolved' if search['coverage']['complete'] else 'incomplete')
                resolutions[key].append({'reference': ref, 'status': status,
                                         'candidate_ids': [c['candidate_id'] for c in found_paths]})
                for candidate in found_paths:
                    item = resolved_files.setdefault(candidate['candidate_id'], {**candidate, 'references': []})
                    item['references'].append(ref)
            # File-content filtering must not turn an earlier copy into the source.
            attributions[key] = file_line_sources(list(resolved_files.values()))
            associated = {}
            for ref in selected_refs:
                found = lookup(ref, by_relative, by_basename, by_absolute)
                for candidate in found:
                    item = associated.setdefault(candidate['candidate_id'], {**candidate, 'references': []})
                    item['references'].append(ref)
                    if self.excerpts and ref['line'] is not None:
                        excerpts[candidate['physical_path']].add(ref['line'])
            candidates[key] = sorted(associated.values(), key=lambda c: (c['root_order'], c['relative_path']))
            if resolution_filter:
                qualifies = any(r['status'] == resolution_filter for r in resolutions[key])
                # Content, when required, still needs a positive matching file.
                # Another reference in the same diagnostic may supply that file.
                qualifies &= 'content' not in (scope or {}) or bool(candidates[key])
            else:
                qualifies = reference_only or bool(candidates[key])
            if selected_refs and qualifies:
                matches.append(key)
        if self.excerpts:
            contexts = self.excerpts_for(excerpts)
            for items in candidates.values():
                for candidate in items:
                    candidate['excerpts'] = [contexts[candidate['physical_path'], ref['line']] if ref['line'] is not None else
                                             {'available': False, 'reason': 'Stored reference supplies no line.', 'line': None}
                                             for ref in candidate['references']]
        self.metrics['reference_lookup_seconds'] += perf_counter() - started
        coverage = {**search['coverage'], 'effective_selection': deepcopy(selection),
                    'resolution_filter': resolution_filter, 'searched': bool(searched),
                    'reference_only_filter': reference_only,
                    'records_without_source_path': sum(s == 'no_path' for s in statuses.values()),
                    'metrics': deepcopy(self.metrics),
                    'reference_count': sum(len(v) for v in details.values()),
                    'candidate_associations': sum(len(v) for v in candidates.values()),
                    'interpretation': 'Resolved files in the effective source scope. For each file/line, the last matching playset member in load order is the error source (owner-directed rule). Contents are current at report generation.'}
        # Candidate context is optional for a stored-reference predicate. Its
        # disk coverage must not change SQL-only membership or filter completion.
        complete = reference_only or coverage['complete']
        return {'complete': complete, 'coverage': coverage, 'matches': matches,
                'references': references, 'reference_details': details, 'candidates': candidates,
                'reference_resolution': resolutions, 'reference_status': statuses,
                'file_line_sources': attributions}
