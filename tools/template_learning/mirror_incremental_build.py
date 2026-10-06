"""Mirror a recorded batch schedule through an unchanged authenticated learner.

Only orchestration lives here. The retained registry operation owns recovery,
fresh/additive learning, serialization and subsequent publication.
"""
import argparse
import ctypes
from ctypes import wintypes
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

from template_learning.inventory import sha256_file
from template_learning.learner_loader import authenticate


def read(path):
    return json.loads(path.read_bytes())


def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')


class Memory(ctypes.Structure):
    _fields_ = [('cb', wintypes.DWORD), ('PageFaultCount', wintypes.DWORD)] + [
        (name, ctypes.c_size_t) for name in ('PeakWorkingSetSize', 'WorkingSetSize',
        'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage', 'QuotaPeakNonPagedPoolUsage',
        'QuotaNonPagedPoolUsage', 'PagefileUsage', 'PeakPagefileUsage', 'PrivateUsage')]


def process_memory(pid):
    kernel = ctypes.windll.kernel32
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    fn = ctypes.windll.psapi.GetProcessMemoryInfo
    fn.argtypes = [wintypes.HANDLE, ctypes.POINTER(Memory), wintypes.DWORD]
    handle = kernel.OpenProcess(0x410, False, pid)
    if not handle:
        return {}
    try:
        info = Memory(); info.cb = ctypes.sizeof(info)
        if not fn(handle, ctypes.byref(info), info.cb):
            return {}
        return {name: getattr(info, name) for name in ('WorkingSetSize','PrivateUsage','PeakWorkingSetSize')}
    finally:
        kernel.CloseHandle(handle)


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--fresh-evidence', type=Path)
    cli.add_argument('--production-build', type=Path)
    cli.add_argument('--basis', type=Path, help='Reuse the already-established corpus and incremental schedule.')
    cli.add_argument('--release-file', type=Path, help='New frozen learner release receipt for the retained basis.')
    cli.add_argument('--output', type=Path, required=True)
    cli.add_argument('--resume', action='store_true', help='Reuse completed, authenticated stages in this same build.')
    args = cli.parse_args()
    if args.basis or args.release_file:
        if not (args.basis and args.release_file) or args.fresh_evidence or args.production_build:
            cli.error('--basis and --release-file must be used together, without the older input-discovery arguments')
    elif not (args.fresh_evidence and args.production_build):
        cli.error('supply --basis/--release-file or --fresh-evidence/--production-build')
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=args.resume)
    fresh = args.fresh_evidence.resolve() if args.fresh_evidence else None
    historical = args.production_build.resolve() if args.production_build else None
    release = read(args.release_file if args.release_file else fresh/'release.json')
    folder = Path(release['folder'])
    manifest, _ = authenticate(folder, release['manifest_sha256'])
    retained = read(args.basis) if args.basis else None
    schedule = dict(inputs=retained['inputs'],batch_sizes=retained['batch_sizes']) if retained else read(historical/'additive/identity.json')
    original = retained['inputs'] if retained else read(historical/'inputs-all.json')
    snapshots = {r['sha256']: r for r in (retained['inputs'] if retained else read(fresh/'inputs.json'))}
    assert [r['sha256'] for r in schedule['inputs']] == [r['sha256'] for r in original]
    assert set(snapshots) == {r['sha256'] for r in original}
    assert len(original) == sum(schedule['batch_sizes']) == 73
    assert schedule['batch_sizes'] == [20,20,20,13]
    assert [r['sha256'] for r in original] == sorted(snapshots)
    for row in ([] if retained else original):
        item = snapshots[row['sha256']]
        path = Path(item['snapshot'])
        assert path.stat().st_size == row['bytes'] and sha256_file(path) == row['sha256']
    checkpoints = []; count = 0
    for size in schedule['batch_sizes']:
        count += size
        prior = next(p for p in retained['schedule'] if p['logs']==count) if retained else read(historical/f'additive/result-{count}.json')
        assert prior['logs'] == count
        checkpoints.append(dict(logs=count, historical_revision=prior.get('historical_revision',prior.get('revision_id')), historical_bundle=prior.get('historical_bundle',prior.get('bundle')),
            ordered_input_hashes=[r['sha256'] for r in original[:count]]))
    basis = dict(strategy='same-version-additive-v1', threshold=.72, release=release,
        schedule=checkpoints, batch_sizes=schedule['batch_sizes'], inputs=[snapshots[r['sha256']] for r in original],
        original_script_sha256=retained['original_script_sha256'] if retained else sha256_file(historical/'run_additive.py'),
        original_identity_sha256=retained['original_identity_sha256'] if retained else sha256_file(historical/'additive/identity.json'),
        retained_basis=str(args.basis.resolve()) if retained else None,
        collection_method='Retained registry sync parses staged exact log copies with the same parser; cumulative build calls the existing build_model(previous_model=...). Historical runner filtered a recovery snapshot then called the same core API.',
        code_changes=bool(retained and retained['release']!=release), cross_version_template_seed=False, production_mutations=False)
    if args.resume:
        assert read(out/'build-basis.json') == basis
    else:
        write(out/'build-basis.json', basis)
    write(out/'release.json', release)
    write(out/'inputs.json', basis['inputs'])
    print('Reused established 73-log inventory and 20/20/20/13 schedule; frozen release:', release['release_id'], flush=True)

    def execute(name, operation, arguments):
        log_path = out/(name+'.log'); receipt = out/(name+'-execution.json')
        if args.resume and receipt.exists() and read(receipt)['status']=='completed':
            saved = read(receipt)
            assert saved['release_id']==release['release_id'] and saved['manifest_sha256']==release['manifest_sha256']
            progress = read(out/'progress.json')
            print(name, 'reusing completed authenticated stage', flush=True)
            return progress['seconds'] if progress['phase']==name else None
        command = [sys.executable,'-I','-S','-B',str(folder/'launcher.py'),'_execute',str(folder),
                   release['manifest_sha256'],operation,str(receipt),*map(str,arguments)]
        started = time.monotonic()
        with log_path.open('wb') as output:
            child = subprocess.Popen(command, stdout=output, stderr=subprocess.STDOUT,
                creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            print(name, 'started; PID', child.pid, flush=True)
            while True:
                memory = process_memory(child.pid)
                state = dict(phase=name,pid=child.pid,seconds=round(time.monotonic()-started,3),
                             log=str(log_path),memory=memory,memory_scope='launcher PID only; not the descendant learner peak',returncode=child.poll())
                write(out/'progress.json', state)
                with (out/'memory.jsonl').open('a',encoding='utf-8') as stream:
                    stream.write(json.dumps(state)+'\n')
                if state['returncode'] is not None:
                    break
                time.sleep(15)
        if child.returncode:
            raise RuntimeError(name+' failed; see '+str(log_path))
        assert read(receipt)['status'] == 'completed'
        print(name, 'completed in', round(time.monotonic()-started,1), 'seconds', flush=True)
        return time.monotonic()-started

    previous = 0; results = read(out/'results.json') if args.resume and (out/'results.json').exists() else []
    state = out/'registry'; runtime = out/'inputs'
    for point in checkpoints:
        count = point['logs']
        if any(r['logs']==count for r in results):
            previous=count
            continue
        for row in original[previous:count]:
            dest = runtime/'sessions'/row['sha256']/'error.log'
            dest.parent.mkdir(parents=True,exist_ok=args.resume)
            if dest.exists():
                assert sha256_file(dest)==row['sha256']
            else:
                shutil.copyfile(snapshots[row['sha256']]['snapshot'], dest)
        execute(f'sync-{count}', 'registry', ['--state-root',state,'sync','--runtime-root',runtime,'--default-role','training'])
        registry = read(state/'registry.json')
        assert sorted(k for k,v in registry['evidence'].items() if v['role']=='training') == point['ordered_input_hashes']
        seconds = execute(f'build-{count}', 'registry', ['--state-root',state,'build','--threshold','.72'])
        registry = read(state/'registry.json')
        bundle = state/'revisions'/registry['current_revision']
        model = read(bundle/'empirical_template_model.json')
        assert set(model['evidence']) == set(point['ordered_input_hashes'])
        assert model['learner_release']['release_id'] == release['release_id']
        assert model['algorithm']['learner_identity'] == manifest['learner_identity']
        result = dict(logs=count,bundle=str(bundle),revision_id=model['revision_id'],seconds=seconds,
            summary=model['summary'],update=model.get('learning_update'),
            parent_revision=results[-1]['revision_id'] if results else None)
        write(out/f'result-{count}.json', result)
        results.append(result); write(out/'results.json',results)
        del model
        print('Checkpoint',count,'logs:',json.dumps(result['summary']),flush=True)
        previous=count
    execute('publish', 'publish', ['--bundle',results[-1]['bundle'],'--output-dir',out/'packages'])
    write(out/'completion.json',dict(status='completed',final_bundle=results[-1]['bundle'],
          checkpoints=[r['revision_id'] for r in results],release=release))


if __name__ == '__main__':
    main()
