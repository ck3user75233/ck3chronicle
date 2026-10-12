"""Pipeline setup operations. Launchers collect inputs; this module owns state."""
from contextlib import ExitStack
from copy import deepcopy
from datetime import date, datetime, time
import json
import os
from pathlib import Path
import tempfile
import sqlite3

from . import config

EXTERNAL = ('root_game', 'root_steam', 'root_local_mods', 'root_logs', 'root_crashes')


def finding(check, severity, evidence, impact, action):
    return dict(check=check, severity=severity, evidence=evidence if isinstance(evidence, (dict, list)) else str(evidence), impact=impact, action=action)


def inspect_paths(roots):
    result = []
    for key in EXTERNAL:
        path = roots[key]
        required = key in ('root_game', 'root_logs')
        try:
            if not path.is_dir():
                result.append(finding(key, 'error' if required else 'warning', path,
                    'Required directory unavailable.' if required else 'Optional mod/crash context unavailable.',
                    'Choose the actual directory in setup; CK3Chronicle will not create it.'))
                continue
            next(path.iterdir(), None)
            result.append(finding(key, 'healthy', path, 'Directory readable.', 'None.'))
        except OSError as exc:
            result.append(finding(key, 'error' if required else 'warning', exc,
                'Directory cannot be read.', 'Correct path or read permissions.'))
    game = roots['root_game']
    markers = [game / name for name in ('common', 'events', 'map_data')]
    executable = game.parent / 'binaries' / 'ck3.exe'
    recognized = all(p.is_dir() for p in markers) and executable.is_file()
    result.append(finding('ck3_identity', 'healthy' if recognized else 'warning',
        {'game_content': [str(p) for p in markers if p.is_dir()],
         'ck3_executable': str(executable) if executable.is_file() else None},
        'Observed supported CK3 layout.' if recognized else 'CK3 identity unverified; source context may use wrong files.',
        'None.' if recognized else 'Confirm the CK3 game directory; an unfamiliar layout needs review.'))
    logs = roots['root_logs']
    result.append(finding('error_log', 'healthy', logs / 'error.log',
        'Current error.log exists.' if (logs / 'error.log').is_file() else
        'No current error.log; setup is allowed. Capture needs a genuine completed log.', 'None.'))
    if logs.is_dir() and logs.name.casefold() != 'logs':
        result.append(finding('logs_identity', 'warning', logs,
            'Unusual logs directory name; intended CK3 location is unverified.', 'Confirm this is CK3 live logs.'))
    return result


def model_choices():
    from .pipeline import catalog
    from .pipeline.model import read_json
    root = catalog.selected_models_root()
    default = read_json((root / 'selection.json').read_bytes())
    choices = []
    for row in catalog.list_releases(models_root=root):
        choice = dict(row)
        if row.get('availability') == 'available':
            try:
                catalog.load_selected_package(models_root=root, package_id=row['package_id'])
                choice['authenticated'] = True
            except Exception as exc:
                choice.update(authenticated=False, error=str(exc))
        choices.append(choice)
    return dict(default=default, choices=choices)


def _model(document):
    from .pipeline import catalog
    value = document.get('model')
    if not isinstance(value, dict) or not value.get('package_id') or not value.get('manifest_sha256'):
        raise config.ConfigurationError('model.package_id and model.manifest_sha256 required; run setup')
    selection = catalog.package_selection(value['package_id'])
    if selection['manifest_sha256'] != value['manifest_sha256']:
        raise config.ConfigurationError('configured model manifest does not match installed catalog')
    catalog.load_selected_package(package_id=value['package_id'])
    return deepcopy(value)


def diagnose(document, path, *, initializing=False):
    """Read-only diagnosis. Never starts a handler or probes by writing files."""
    checks = []
    roots = None
    try:
        roots = config.paths_for(document, path)
        checks.extend(inspect_paths(roots))
        for key in ('root_wip', 'root_ck3chronicle', 'root_learner_state'):
            p = roots[key]
            checks.append(finding(key, 'error' if p.exists() and not p.is_dir() else 'unverified', p,
                'Write access is not established by read-only diagnosis.',
                'Setup checks application-data writes when applying.'))
    except (ValueError, OSError, config.ConfigurationError) as exc:
        checks.append(finding('paths', 'error', exc, 'Runtime roots cannot be used.', 'Correct named path fields.'))
    try:
        from .runtime_logging import _validated_settings
        _validated_settings(document.get('logging', {}))
        watcher = document.get('watcher', {})
        if not isinstance(watcher, dict):
            raise ValueError('watcher must be a table')
        for key in ('ingest_enabled', 'retention_enabled'):
            if type(watcher.get(key, True)) is not bool:
                raise ValueError(f'watcher.{key} must be boolean')
        for key, default in (('maintenance_hours', 24), ('retention_days', 30)):
            value = watcher.get(key, default)
            if type(value) is not int or value <= 0:
                raise ValueError(f'watcher.{key} must be a positive integer')
        checks.append(finding('controls', 'healthy', 'watcher/logging values valid', 'Settings can be used.', 'None.'))
    except (ValueError, TypeError) as exc:
        checks.append(finding('controls', 'error', exc, 'Runtime settings invalid.', 'Correct the named value.'))
    try:
        _model(document)
        checks.append(finding('model', 'healthy', document['model'], 'Installed model authenticated.', 'None.'))
    except Exception as exc:
        checks.append(finding('model', 'error', exc, 'Processing model unavailable.', 'Run setup to select an authenticated package.'))
    tools = document.get('tools', {})
    if not isinstance(tools, dict):
        checks.append(finding('tools', 'error', 'tools must be a table',
            'Tool configuration cannot be used.', 'Correct the tools table.'))
    tool = tools.get('ripgrep') if isinstance(tools, dict) else None
    if tool and isinstance(tool, str):
        executable = (path.parent / tool).resolve()
        checks.append(finding('ripgrep', 'healthy' if executable.is_file() else 'warning', executable,
            'Configured source-search executable exists; execution/version is not checked here.' if executable.is_file()
            else 'Source-content search unavailable; database reports remain available.',
            'Use setup --ripgrep with the bundled executable; verify its version in distribution acceptance.'))
    elif not tool:
        checks.append(finding('ripgrep', 'unverified', 'tools.ripgrep not configured',
            'Source-content search needs an explicit --ripgrep executable; database reports remain available.',
            'Set the bundled executable using setup --ripgrep.'))
    else:
        checks.append(finding('ripgrep', 'error', 'tools.ripgrep must be a path string',
            'Source-search configuration cannot be used.', 'Set the executable path with setup --ripgrep.'))
    database = None
    try:
        raw = document.get('watcher', {}).get('database')
        if not raw and initializing:
            checks.append(finding('database', 'healthy', 'new database planned', 'Apply will create once.', 'None.'))
        else:
            if not isinstance(raw, str) or not raw.strip():
                raise ValueError('watcher.database must name an existing initialized file')
            database = (path.parent / raw).resolve()
            if roots and not database.is_relative_to(roots['root_ck3chronicle']):
                raise ValueError('database must be inside paths.root_ck3chronicle; setup does not relocate state')
            from .pipeline.repository import open_database_readonly
            with open_database_readonly(database) as storage:
                metadata = storage.metadata
            checks.append(finding('database', 'healthy', dict(path=str(database), **metadata),
                'Current SQLite schema available.', 'None.'))
    except (ValueError, OSError, TypeError, AttributeError, sqlite3.Error) as exc:
        checks.append(finding('database', 'error', exc, 'History cannot be opened; it has not been reset.',
            'Supply the exact existing compatible database or recover setup using --database.'))
    return dict(config=str(path), paths={k: str(v) for k, v in (roots or {}).items()},
                database=str(database) if database else None, model=document.get('model'), findings=checks)


def suggest_paths():
    """Bounded Windows Known Folder suggestions, never selected configuration."""
    import ctypes
    import uuid
    def known(identifier):
        value = ctypes.c_wchar_p()
        guid = (ctypes.c_byte * 16).from_buffer_copy(uuid.UUID(identifier).bytes_le)
        shell = ctypes.windll.shell32
        if shell.SHGetKnownFolderPath(ctypes.byref(guid), 0, None, ctypes.byref(value)) != 0:
            return None
        try:
            return Path(value.value)
        finally:
            ctypes.windll.ole32.CoTaskMemFree(value)
    if os.name != 'nt':
        return dict(candidates={}, findings=['Windows suggestions unavailable; supply explicit paths.'])
    documents = known('FDD39AD0-238F-46AF-ADB4-6C85480369C7')
    programs = known('7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E')
    candidates = {}
    if programs:
        steam = programs / 'Steam' / 'steamapps'
        candidates.update(root_game=str(steam / 'common/Crusader Kings III/game'),
                          root_steam=str(steam / 'workshop/content/1158310'))
    if documents:
        base = documents / 'Paradox Interactive/Crusader Kings III'
        candidates.update({key: str(base / name) for key, name in
            [('root_local_mods', 'mod'), ('root_logs', 'logs'), ('root_crashes', 'crashes')]})
    return dict(candidates=candidates, accepted=False,
                findings=inspect_paths({k: Path(v) for k, v in candidates.items()})
                if len(candidates) == len(EXTERNAL) else ['Some Known Folders unavailable; type actual paths.'])


def _toml_value(value):
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, (datetime, date, time)):
        return value.isoformat()
    if isinstance(value, list):
        return '[' + ', '.join(_toml_value(v) for v in value) + ']'
    if isinstance(value, dict):
        return '{' + ', '.join(json.dumps(k) + ' = ' + _toml_value(v) for k, v in value.items()) + '}'
    raise ValueError(f'unsupported TOML value {type(value).__name__}')


def _toml(document):
    lines = ['# CK3Chronicle paths and settings. Editable; relative paths use this file.']
    for key, value in document.items():
        if not isinstance(value, dict):
            lines.append(json.dumps(key) + ' = ' + _toml_value(value))
    for key, value in document.items():
        if isinstance(value, dict):
            lines.extend(['', '[' + json.dumps(key) + ']'])
            lines.extend(json.dumps(k) + ' = ' + _toml_value(v) for k, v in value.items())
    return '\n'.join(lines) + '\n'


def prepare(path, inputs, accepted=()):
    path = Path(path).resolve()
    previous = config.load_config(path) if path.exists() else {}
    document = deepcopy(previous)
    for table in ('paths', 'watcher', 'model'):
        if not isinstance(document.setdefault(table, {}), dict):
            raise config.ConfigurationError(f'{table} must be a table')
    paths = document['paths']
    data = inputs.get('data_root')
    if data:
        data = str(Path(data).resolve())
        old = previous.get('paths', {}).get('root_wip')
        if old and (path.parent / old).resolve() != Path(data):
            raise config.ConfigurationError('setup cannot relocate existing data; keep data root and preserve history')
        paths['root_wip'] = data
    if not paths.get('root_wip'):
        local = os.environ.get('LOCALAPPDATA')
        if not local:
            raise config.ConfigurationError('specify --data-root when LocalAppData is unavailable')
        paths['root_wip'] = str(Path(local) / 'ck3chronicle/data')
    data = (path.parent / paths['root_wip']).resolve()
    paths.setdefault('root_ck3chronicle', str(data / 'runtime'))
    paths.setdefault('root_learner_state', str(data / 'learner'))
    confirmations = []
    for key in EXTERNAL:
        if inputs.get(key) is not None:
            paths[key] = str(Path(inputs[key]).resolve())
        old = previous.get('paths', {}).get(key)
        if paths.get(key) and (old is None or (path.parent / old).resolve() != (path.parent / paths[key]).resolve()):
            if key not in accepted:
                confirmations.append(key)
    for key in config._REQUIRED_PATH_KEYS:
        if paths.get(key):
            paths[key] = str((path.parent / paths[key]).resolve())
    watcher = document['watcher']
    if inputs.get('ripgrep'):
        tools = document.setdefault('tools', {})
        if not isinstance(tools, dict):
            raise config.ConfigurationError('tools must be a table')
        tools['ripgrep'] = str(Path(inputs['ripgrep']).resolve())
    for key, default in dict(ingest_enabled=True, retention_enabled=True, maintenance_hours=24, retention_days=30).items():
        watcher.setdefault(key, default)
    if inputs.get('database'):
        selected = str(Path(inputs['database']).resolve())
        if watcher.get('database') and (path.parent / watcher['database']).resolve() != Path(selected):
            raise config.ConfigurationError('repeat setup cannot replace the configured database; history preserved')
        watcher['database'] = selected
    elif watcher.get('database'):
        watcher['database'] = str((path.parent / watcher['database']).resolve())
    from .pipeline import catalog
    if inputs.get('package_id') or not document['model']:
        package_id = inputs.get('package_id') or model_choices()['default']['package_id']
        selection = catalog.package_selection(package_id)
        document['model'].update(package_id=package_id, manifest_sha256=selection['manifest_sha256'])
    result = diagnose(document, path, initializing=not watcher.get('database'))
    runtime = Path(paths['root_ck3chronicle'])
    if not watcher.get('database') and runtime.is_dir() and next(runtime.iterdir(), None) is not None:
        result['findings'].append(finding('existing_data', 'error', runtime,
            'Existing data has no configured database; setup will not guess or initialize another history.',
            'Supply --database with the exact initialized file, or choose a new empty data root for a new installation.'))
    result.update(acceptance_required=confirmations, applied=False, effects=[], restart_required=False)
    for key in confirmations:
        result['findings'].append(finding(key, 'error', paths[key], 'Path not individually accepted.',
            f'Confirm this location then supply --accept-path {key}.'))
    return document, previous, result


def apply_setup(path, inputs, accepted=()):
    """Validate before creation; serialize setup and hold the Watcher lease on apply."""
    path = Path(path).resolve()
    document, previous, result = prepare(path, inputs, accepted)
    if any(f['severity'] == 'error' for f in result['findings']):
        return result, 2
    from .watcher import WatcherLease
    from .pipeline.request_handler import HandlerClient, _startup_lock
    from .pipeline.repository import create_database
    runtime = Path(document['paths']['root_ck3chronicle'])
    effects = result['effects']
    try:
        parent_existed = path.parent.exists()
        path.parent.mkdir(parents=True, exist_ok=True)
        effects.append(dict(path=str(path.parent), effect='preserved' if parent_existed else 'created'))
        # Exact config lock, exclusive creation; no stale-lock takeover.
        lock = path.with_name(path.name + '.setup-lock')
        with ExitStack() as stack:
            stream = lock.open('x')
            stack.callback(lambda: lock.unlink())
            stack.enter_context(stream)
            stream.write(str(os.getpid()))
            stream.flush()
            # Re-read under lock; refuse overwriting a concurrently changed file.
            current = config.load_config(path) if path.exists() else {}
            if current != previous:
                raise config.ConfigurationError('configuration changed during setup; review again')
            for key in ('root_wip', 'root_ck3chronicle', 'root_learner_state'):
                folder = Path(document['paths'][key])
                existed = folder.exists()
                folder.mkdir(parents=True, exist_ok=True)
                effects.append(dict(path=str(folder), effect='preserved' if existed else 'created'))
            stack.enter_context(WatcherLease(runtime))
            effects.append(dict(path=str(runtime / 'watch'), effect='lease acquired; lock file retained'))
            database = document['watcher'].get('database')
            if database:
                stack.enter_context(_startup_lock(Path(database)))
                if HandlerClient(Path(database)).probe() is not None:
                    raise config.ConfigurationError('runtime in use; stop observation and run runtime-stop, then apply')
            for key in ('root_wip', 'root_ck3chronicle', 'root_learner_state'):
                folder = Path(document['paths'][key])
                with tempfile.TemporaryFile(dir=folder) as probe:
                    probe.write(b'ck3chronicle setup')
                    probe.flush()
            if not database:
                storage = create_database(runtime)
                database = str(storage.path)
                storage.close()
                document['watcher']['database'] = database
                result['database'] = database
                effects.append(dict(path=database, effect='created', recovery='Use setup --database with this exact file if saving fails.'))
            else:
                effects.append(dict(path=database, effect='preserved'))
            content = _toml(document)
            # Round trip before replacing config, including unrelated TOML values.
            if config.tomllib.loads(content) != document:
                raise ValueError('configuration serialization did not preserve values')
            fd, name = tempfile.mkstemp(prefix=path.name + '.', suffix='.tmp', dir=path.parent)
            temporary = Path(name)
            try:
                with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as output:
                    output.write(content)
                    output.flush()
                    os.fsync(output.fileno())
                temporary.replace(path)
            finally:
                temporary.unlink(missing_ok=True)
            effects.append(dict(path=str(path), effect='saved'))
            # Setup shares the sole runtime logging backend after durable config save.
            from . import runtime_logging as backend
            from uuid import uuid4
            destination = backend.invocation_log_path(runtime / 'logging', 'setup', uuid4().hex)
            output = None
            try:
                output = backend.configure_runtime_logging(destination=destination,
                    settings=backend._validated_settings(document.get('logging', {})))
                backend.event(backend.get_logger('setup'), 'setup_completed', config=str(path),
                    database=database, package_id=document['model']['package_id'], effects=effects)
            except OSError as exc:
                result['findings'].append(finding('setup_journal', 'warning', exc,
                    'Configuration saved but journal unavailable.', 'Correct runtime log-directory access.'))
            finally:
                if output is not None:
                    backend.close_runtime_logging(output)
        result.update(applied=True, restart_required=document != previous)
        return result, 0
    except Exception as exc:
        if getattr(exc, 'created_database_path', None):
            result['database'] = exc.created_database_path
            effects.append(dict(path=exc.created_database_path, effect='partial database creation; initialization unverified'))
        result['findings'].append(finding('apply', 'error', exc,
            'Setup not completed; inspect effects, previous configuration is preserved unless marked saved.',
            'Stop active runtime or correct access; recover using the exact created database path.'))
        return result, 2 if isinstance(exc, (config.ConfigurationError, FileExistsError)) else 1


def emit(result, format):
    if format == 'json':
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        for key, value in result.items():
            if key == 'findings':
                for item in value:
                    print(f"{item['severity'].upper()} {item['check']}: {item['evidence']}\n  {item['impact']} {item['action']}")
            else:
                print(f'{key}: {value}')


def command(args):
    try:
        if args.suggest_paths:
            result, code = suggest_paths(), 0
        elif args.list_models:
            result, code = model_choices(), 0
        elif args.apply:
            result, code = apply_setup(config.default_config_path(), vars(args), args.accept_path)
        else:
            _, _, result = prepare(config.default_config_path(), vars(args), args.accept_path)
            code = 2 if any(f['severity'] == 'error' for f in result['findings']) else 0
    except (ValueError, OSError, config.ConfigurationError) as exc:
        result, code = dict(error=str(exc), applied=False), 2
    emit(result, args.format)
    return code
