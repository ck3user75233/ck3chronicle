"""Trace file access in the actual reporting CLI and its disposable DB worker.

No missing-file simulation: retained input is copied with SQLite's read-only
backup API, then all runtime database operations go through HandlerClient.
Python audit hooks observe opens, directory scans, SQLite opens and subprocess
arguments. This is not an operating-system trace of arbitrary native code.
"""
import argparse
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import uuid

from ck3chronicle.pipeline.request_handler import HandlerClient


HOOK = '''import json, os, sys
from pathlib import Path
trace = Path(__file__).resolve().parent / ('io-' + str(os.getpid()) + '.jsonl')
descriptor = os.open(trace, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
def record(event, arguments):
    if event not in {'open', 'os.scandir', 'sqlite3.connect', 'subprocess.Popen'}:
        return
    if event == 'subprocess.Popen':
        arguments = arguments[:2]
    os.write(descriptor, (json.dumps({'pid': os.getpid(), 'event': event,
        'arguments': arguments}, default=str) + '\\n').encode('utf-8'))
sys.addaudithook(record)
'''


def check(evidence):
    config = json.loads(evidence.read_bytes())
    output = Path(config['output_root']) / 'io-trace' / uuid.uuid4().hex
    output.mkdir(parents=True)
    database = output / 'genuine.sqlite3'
    with sqlite3.connect(Path(config['database']).as_uri() + '?mode=ro', uri=True) as source:
        with sqlite3.connect(database) as target:
            source.backup(target)
    (output / 'sitecustomize.py').write_text(HOOK, encoding='utf-8')
    wrapper = output / 'trace_cli.py'
    wrapper.write_text("from pathlib import Path\nimport runpy\n"
        "hook = Path(__file__).with_name('sitecustomize.py')\n"
        "exec(compile(hook.read_text(encoding='utf-8'), str(hook), 'exec'), {'__file__': str(hook)})\n"
        "runpy.run_module('ck3chronicle.cli', run_name='__main__')\n", encoding='utf-8')
    query = output / 'query.json'
    query.write_text(json.dumps({'refinement': {'message': {'contains': 'unrecognized'}},
                                 'analytics': {'history': False}}), encoding='utf-8')
    destination = output / 'stored-data-io.json'
    command = [sys.executable, '-I', '-B', str(wrapper), 'report', 'latest',
               '--database', str(database), '--package-id', config['package_id'],
               '--custom', '--query', str(query), '--format', 'json', '--limit', '4',
               '--output', str(destination)]
    # -I ignores PYTHONPATH for the CLI wrapper; it installs the hook explicitly.
    # The normal worker launcher inherits PYTHONPATH and imports sitecustomize.
    environment = dict(os.environ, PYTHONPATH=str(output))
    try:
        result = subprocess.run(command, env=environment, capture_output=True, text=True, timeout=240)
    finally:
        HandlerClient(database).shutdown()
    (output / 'commands.json').write_text(json.dumps([dict(command=command,
        returncode=result.returncode, stderr=result.stderr)], indent=2), encoding='utf-8')
    assert result.returncode == 0, result.stderr
    payload = json.loads(destination.read_bytes())
    assert payload['status'] == 'completed' and payload['totals']['distinct_records'] > 0
    logs = sorted(output.glob('io-*.jsonl'))
    events = [json.loads(line) for path in logs for line in path.read_text(encoding='utf-8').splitlines()]
    pids = {e['pid'] for e in events}
    assert len(pids) == 2, ('CLI and one cold database worker must both be traced', pids)
    database_opens = [e for e in events if e['event'] == 'sqlite3.connect']
    assert database_opens, 'Worker database access was not observed'
    allowed = {str(database), database.as_uri(), ':memory:'}
    assert all(e['arguments'][0].split('?', 1)[0] in allowed for e in database_opens)
    assert any(e['arguments'][0].split('?', 1)[0] != ':memory:' for e in database_opens)
    accessed = [str(e['arguments'][0]).replace('\\', '/').casefold()
                for e in events if e['event'] in {'open', 'os.scandir'}]
    forbidden = [name for name in accessed if name.endswith('/error.log') or '/models/' in name]
    assert not forbidden, forbidden
    project_config = Path(__file__).resolve().parents[1] / 'config.toml'
    data_files = sorted({str(e['arguments'][0]) for e in events if e['event'] == 'open'
                        and isinstance(e['arguments'][0], str)
                        and not e['arguments'][0].endswith(('.py', '.pyc', '.pyd', '.dll'))})
    for name in data_files:
        path = Path(name).resolve()
        assert name.casefold() == 'nul' or path == project_config or path.is_relative_to(output), name
    children = [e['arguments'][1] for e in events if e['event'] == 'subprocess.Popen']
    for child in children:
        # The only additional native reader is rg, confined to source inventories.
        command_text = child if isinstance(child, str) else ' '.join(map(str, child))
        assert 'ck3chronicle.pipeline.database_handler' in command_text or 'rg.exe' in command_text.casefold(), child
        normalized = command_text.replace('\\', '/').casefold()
        assert '/models/' not in normalized and '/error.log' not in normalized
    receipt = dict(status='passed', output=str(output), traced_processes=len(pids),
                   audit_events=len(events), database_opens=len(database_opens),
                   raw_log_or_model_artifact_accesses=forbidden, subprocesses=len(children),
                   non_code_file_opens=data_files,
                   totals=payload['totals'], limit='Python file/directory/SQLite I/O and child command arguments; not a system-wide native trace')
    (output / 'io-verification.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, required=True)
    print(json.dumps(check(parser.parse_args().evidence), indent=2))
