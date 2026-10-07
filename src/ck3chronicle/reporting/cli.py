"""Root CLI adapters. Public handler reads only; no model selection or loading."""
from datetime import datetime, timezone
import json
import re
from pathlib import Path
import sys
import traceback

from ..pipeline.request_handler import COMPLETED, HandlerClient
from ..journal import get_journal
from ..runtime_logging import event, get_logger
from .analysis import DiagnosticAnalysis, QueryError, ReadError, RunSelectionError, SourceEvaluationError
from .presets import build_query, preset_description, validate_package
from .source_search import SourceSearch

LOGGER = get_logger('report_cli')
journal = get_journal('report_cli')


def serialize_json(payload):
    """UTF-8 JSON with reversible surrogate escapes and unchanged Unicode text."""
    native = json.dumps(payload, ensure_ascii=False, indent=2) + '\n'
    return re.sub(r'[\ud800-\udfff]', lambda m: f'\\u{ord(m[0]):04x}', native)


def _database(args):
    if args.database is not None:
        return args.database.resolve()
    from ..config import watcher_settings
    return watcher_settings().database


def _json_file(path):
    try:
        value = json.loads(path.read_text(encoding='utf-8-sig'))
    except (OSError, UnicodeError, ValueError) as exc:
        raise QueryError(f'cannot read JSON query/context {path}: {exc}') from exc
    if not isinstance(value, dict):
        raise QueryError(f'{path}: expected a JSON object')
    return value


def _package(client, run, supplied):
    if run == 'latest':
        if not supplied:
            raise QueryError('latest requires an explicit --package-id; active model selection is not consulted')
        return supplied
    try:
        result = client.result(client.submit('get_run', {'run_id': run}))
    except (LookupError, OSError, EOFError, RuntimeError) as exc:
        raise ReadError('get_run', run, str(exc), type(exc).__name__) from exc
    if result.status != COMPLETED:
        raise ReadError('get_run', run, result.error, result.exception_class)
    if result.value is None:
        raise RunSelectionError(f'unknown Run: {run}')
    stored = result.value['lineage']['package_id']
    if supplied is not None and supplied != stored:
        raise RunSelectionError(f'Run {run} belongs to package {stored}; supplied --package-id {supplied} conflicts')
    return stored


def _emit(args, payload, kind):
    with journal.call():
        from .explanation import explain
        from .presentation import render_html, render_text
        payload = {'explanation': explain(payload, requested_run=getattr(args, 'run', None)), **payload}
        output = args.output
        appendix = appendix_bytes = None
        if args.format == 'json':
            rendered = serialize_json(payload)
        elif args.format == 'html':
            appendix = output.with_name(output.stem + '-sources.html')
            rendered, appendix_html = render_html(payload, report_name=output.name, appendix_name=appendix.name)
            if appendix_html is not None:
                appendix_bytes = appendix_html.encode('utf-8')
        else:
            rendered = render_text(payload, kind=kind)
        # Finish encoding both documents before opening either destination. An
        # encoding error must not create/truncate the main output or its appendix.
        output_bytes = rendered.encode('utf-8')
        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
            if appendix_bytes is not None:
                appendix.write_bytes(appendix_bytes)
            output.write_bytes(output_bytes)
            print(f'{kind} written: {output.resolve()}', file=sys.stderr)
        else:
            # Python's redirected Windows console can otherwise use a lossy encoding.
            if hasattr(sys.stdout, 'reconfigure'):
                sys.stdout.reconfigure(encoding='utf-8', newline='\n')
            sys.stdout.write(rendered)


def _failure(args, exc, *, kind, stage=None):
    if isinstance(exc, SourceEvaluationError):
        state, code = 'source_filter_incomplete', 3
    elif isinstance(exc, RunSelectionError):
        state, code = 'run_selection_error', 2
    elif isinstance(exc, QueryError):
        state, code = 'invalid_query', 2
    elif isinstance(exc, ReadError):
        state, code = 'read_unavailable', 1
    else:
        state, code = 'operation_failed', 1
    unexpected = state == 'operation_failed' and not isinstance(exc, OSError)
    payload = {'status': state, 'error': str(exc), 'exception_class': type(exc).__name__,
               'request': {'operation': kind, **{
                   name: str(value) if name in {'database', 'query'} else value
                   for name in ('run', 'package_id', 'preset', 'database', 'query')
                   if (value := getattr(args, name, None)) is not None}}}
    if stage is not None:
        payload['failure_stage'] = stage
    if unexpected:
        payload['traceback'] = ''.join(traceback.format_exception(exc))
    if isinstance(exc, SourceEvaluationError):
        payload['partial'] = exc.partial
        if exc.partial is not None and 'chronology_exclusions' in exc.partial:
            payload['chronology_exclusions'] = exc.partial['chronology_exclusions']
    if isinstance(exc, RunSelectionError):
        payload['chronology_exclusions'] = exc.exclusions
    if isinstance(exc, ReadError):
        payload['read_error'] = exc.to_dict()
    payload['presentation'] = {'generated_at': datetime.now(timezone.utc).isoformat(),
                               'verbose': getattr(args, 'verbose', False)}
    event(LOGGER, 'report_failed', level='ERROR', exc_info=unexpected,
          operation=kind, failure_stage=stage, error=str(exc), exception_class=type(exc).__name__)
    print(f'ERROR [{state}] {kind}' + (f' at {stage}' if stage else '') +
          f': {type(exc).__name__}: {exc}', file=sys.stderr)
    # Argument/output errors still need a readable stderr even without a target.
    if args.format != 'html' or args.output is not None:
        try:
            _emit(args, payload, kind)
        except Exception as output_error:
            # This is the terminal caller boundary: a broken renderer/destination
            # must not hide the original error or recursively invoke rendering.
            payload['output_error'] = {'exception_class': type(output_error).__name__,
                                       'error': str(output_error)}
            event(LOGGER, 'report_error_output_failed', level='ERROR', exc_info=True,
                  operation=kind, error=str(output_error))
            print(f'ERROR [output_failed]: {type(output_error).__name__}: {output_error}', file=sys.stderr)
            print(json.dumps(payload, ensure_ascii=True), file=sys.stderr)
            code = 1
    return code


def _check_output(args, database):
    if args.output:
        targets = [args.output]
        if args.format == 'html' and getattr(args, 'verbose', False):
            targets.append(args.output.with_name(args.output.stem + '-sources.html'))
        inputs = [database, getattr(args, 'query', None), getattr(args, 'source_context', None)]
        if any(t.resolve() == p.resolve() for t in targets for p in inputs if p is not None):
            # Prevent _failure from writing over that same input.
            args.output = None
            raise QueryError('report destination must differ from the database and query/context inputs')


def cmd_runs(args):
    stage = 'input_validation'
    try:
        database = _database(args)
        _check_output(args, database)
        stage = 'run_selection'
        payload = DiagnosticAnalysis(HandlerClient(database)).list_runs(args.package_id, offset=args.offset, limit=args.limit)
        stage = 'export'
        _emit(args, dict(payload, status='completed', database=str(database)), 'runs')
        return 0
    except Exception as exc:
        return _failure(args, exc, kind='runs', stage=stage)


def cmd_report(args):
    stage = 'input_validation'
    try:
        if args.format == 'html' and args.output is None:
            raise QueryError('HTML requires an explicit --output destination')
        if args.custom and args.query is None:
            raise QueryError('--custom requires --query PATH')
        if args.run == 'latest' and not args.package_id:
            raise QueryError('latest requires an explicit --package-id')
        value = _json_file(args.query) if args.query else {}
        context = _json_file(args.source_context) if args.source_context else {}
        if args.source_root:
            context['roots'] = args.source_root
        if args.source_directory:
            context['directories'] = args.source_directory
        if args.no_recursive:
            context['recursive'] = False
        database = _database(args)
        _check_output(args, database)
        query = build_query(args.preset, value, limit=args.limit,
                            historical_limit=args.historical_limit, no_history=args.no_history)
        stage = 'run_selection'
        client = HandlerClient(database)
        package = _package(client, args.run, args.package_id)
        validate_package(args.preset, package)
        sources = SourceSearch(client, context=context, excerpts=args.verbose,
                               ripgrep=args.ripgrep, candidate_context=True)
        stage = 'investigation'
        payload = DiagnosticAnalysis(client, source_resolver=sources).investigate(
            args.run, package_id=package, query=query).to_dict()
        payload.update(status='completed', presentation={
            'preset': preset_description(args.preset), 'generated_at': datetime.now(timezone.utc).isoformat(),
            'verbose': args.verbose, 'source_context': context, 'database': str(database)})
        stage = 'export'
        _emit(args, payload, 'report')
        event(LOGGER, 'report_exported', run_id=payload['run']['run_id'], format=args.format,
              output=str(args.output) if args.output else 'stdout')
        return 0
    # Catch ordinary Python exceptions at the CLI boundary only. Library callers
    # keep their original exceptions; interrupts/SystemExit are not swallowed.
    except Exception as exc:
        return _failure(args, exc, kind='report', stage=stage)
