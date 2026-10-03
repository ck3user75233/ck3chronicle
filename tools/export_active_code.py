"""Export current reachable application and supported learner source, without running it.

Modulegraph2 and AST imports plus explicit project entry-point/manifest boundaries.
Whole-file source exports: this is not a proof of function-level dead-code absence.
"""
from __future__ import annotations

import argparse
import ast
from collections import defaultdict, deque
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import tokenize
import tomllib


def digest(data):
    return hashlib.sha256(data).hexdigest()


def constant(path, name):
    for node in ast.parse(path.read_bytes(), filename=str(path)).body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError(f'missing literal declaration {name}: {path}')


class Sources:
    def __init__(self, root):
        self.root = root
        self.modules = {}
        self.packages = set()
        for base in (root / 'src', root / 'tools'):
            for path in base.rglob('*.py'):
                if '__pycache__' in path.parts:
                    continue
                parts = list(path.relative_to(base).with_suffix('').parts)
                if parts[0] not in ('ck3chronicle', 'template_learning'):
                    continue
                if parts[-1] == '__init__':
                    parts.pop()
                    self.packages.add('.'.join(parts))
                self.modules['.'.join(parts)] = path
        self.import_cache = {}

    def imports(self, module):
        if module in self.import_cache:
            return self.import_cache[module]
        path = self.modules[module]
        package = module if module in self.packages else module.rpartition('.')[0]
        edges = []
        missing = []
        external = set()

        def add(name, line, required=False):
            if not name:
                return
            if name in self.modules:
                edges.append((name, line))
            elif name.split('.')[0] in ('ck3chronicle', 'template_learning'):
                # A namespace directory is legal; attributes in from-imports
                # are not missing modules.
                namespace = any(n.startswith(name + '.') for n in self.modules)
                if required and not namespace:
                    missing.append((name, line))
            else:
                external.add(name.split('.')[0])

        for node in ast.walk(ast.parse(path.read_bytes(), filename=str(path))):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    add(alias.name, node.lineno, True)
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    parts = package.split('.')
                    if node.level > len(parts):
                        raise ValueError(f'bad relative import: {path}:{node.lineno}')
                    base = '.'.join(parts[:len(parts) - node.level + 1])
                    if node.module:
                        base += '.' + node.module
                else:
                    base = node.module or ''
                add(base, node.lineno, True)
                for alias in node.names:
                    if alias.name != '*':
                        add(base + '.' + alias.name, node.lineno)
        self.import_cache[module] = (edges, missing, sorted(external))
        return self.import_cache[module]

    def closure(self, seeds):
        reasons = defaultdict(set)
        pending = deque()
        seen = set()
        missing = []
        external = set()
        for module, reason in seeds.items():
            if module not in self.modules:
                raise ValueError(f'missing entry module: {module}')
            reasons[self.modules[module]].add(reason)
            pending.append(module)
        while pending:
            module = pending.popleft()
            if module in seen:
                continue
            seen.add(module)
            path = self.modules[module]
            parts = module.split('.')
            for size in range(1, len(parts)):
                parent = '.'.join(parts[:size])
                if parent in self.modules:
                    reasons[self.modules[parent]].add(f'Package initializer for {module}')
                    pending.append(parent)
            edges, absent, imports = self.imports(module)
            missing.extend((str(path.relative_to(self.root)), n, line) for n, line in absent)
            external.update(imports)
            for target, line in edges:
                reasons[self.modules[target]].add(
                    f'Import from {path.relative_to(self.root).as_posix()}:{line}')
                pending.append(target)
        if missing:
            raise ValueError(f'unresolved required project imports: {missing}')
        return reasons, sorted(seen), sorted(external)


def merge(target, other):
    for path, reasons in other.items():
        target[path].update(reasons)


def crosscheck_imports(root, seeds, expected, external):
    """Independently compare modulegraph2's static graph with our import closure."""
    import modulegraph2

    graph = modulegraph2.ModuleGraph(use_stdlib_implies=False, use_builtin_hooks=False)
    # Dependency implementations are outside this first-party source export.
    graph.add_excludes(external)
    previous_path = sys.path[:]
    try:
        sys.path[:0] = [str(root / 'src'), str(root / 'tools')]
        for name in seeds:
            graph.add_module(name)
    finally:
        sys.path[:] = previous_path
    actual = set()
    for node in graph.iter_graph():
        if not node.name.startswith(('ck3chronicle', 'template_learning')):
            continue
        if isinstance(node, (modulegraph2.MissingModule, modulegraph2.InvalidModule,
                             modulegraph2.InvalidRelativeImport)):
            raise ValueError(f'modulegraph2 unresolved project import: {node.name}')
        if node.filename is not None:
            actual.add(node.name)
    if actual != set(expected):
        raise ValueError(f'import graph disagreement: modulegraph2-only={sorted(actual-set(expected))}; '
                         f'AST-only={sorted(set(expected)-actual)}')
    return dict(library='modulegraph2', version=modulegraph2.__version__,
                entry_points=sorted(seeds), matched_modules=sorted(actual),
                external_roots_excluded=sorted(external))


def authenticated_files(folder, expected_pin):
    manifest_path = folder / 'manifest.json'
    payload = manifest_path.read_bytes()
    if digest(payload) != expected_pin:
        raise ValueError(f'catalog/selection manifest mismatch: {folder}')
    manifest = json.loads(payload)
    files = []
    for name, expected in manifest['hashes'].items():
        path = (folder / name).resolve()
        if not path.is_relative_to(folder.resolve()):
            raise ValueError('manifest path outside distribution')
        if digest(path.read_bytes()) != expected:
            raise ValueError(f'manifest payload mismatch: {path}')
        files.append(path)
    return manifest, files


def source_text(path, payload):
    if path.suffix == '.py':
        encoding, _ = tokenize.detect_encoding(io.BytesIO(payload).readline)
        return payload.decode(encoding)
    return payload.decode('utf-8-sig')


def directory_tree(paths):
    tree = {}
    for path in paths:
        node = tree
        for part in path.parts:
            node = node.setdefault(part, {})
    lines = ['ck3chronicle/']

    def walk(node, prefix):
        entries = sorted(node, key=lambda name: (not bool(node[name]), name))
        for index, name in enumerate(entries):
            last = index == len(entries) - 1
            lines.append(prefix + ('└── ' if last else '├── ') + name + ('/' if node[name] else ''))
            walk(node[name], prefix + ('    ' if last else '│   '))
    walk(tree, '')
    return '\n'.join(lines)


def write_export(root, output, title, scope, reasons, resources, excluded, external):
    paths = sorted(reasons, key=lambda p: p.relative_to(root).as_posix())
    entries = []
    blocks = []
    for path in paths:
        raw = path.read_bytes()
        text = source_text(path, raw)
        name = path.relative_to(root).as_posix()
        # A fence longer than any backtick run in the source cannot be closed
        # by an embedded Markdown example or template literal.
        fence = '`' * max(3, 1 + max((len(s) for s in re.findall(r'`+', text)), default=0))
        language = {'.py': 'python', '.json': 'json', '.html': 'html'}.get(path.suffix, 'text')
        body = f'### `{name}`\n\n{fence}{language}\n{text}'
        if not text.endswith('\n'):
            body += '\n'
        body += f'{fence}\n\n'
        blocks.append(body)
        entries.append(dict(path=name, bytes=len(raw), sha256=digest(raw),
                            reasons=sorted(reasons[path]), fence=fence))
    generated = datetime.now(timezone.utc).isoformat(timespec='seconds')
    introduction = [f'# {title}', '', f'**Generated:** {generated}', '',
                    f'**Root:** `{root}`', '', f'**Files included:** {len(paths)}', '',
                    '---', '', '## Scope and selection', '', *scope, '',
                    'Files are reproduced in full, including comments and any unused symbols inside a reachable file. '
                    'This is a source/module selection, not function-level dead-code elimination or proof of what '
                    'a currently running process has loaded. No product command, database handler, capture, '
                    'learning campaign or production ingestion was executed to generate this export.', '',
                    'Analysis: `modulegraph2` independently cross-checks the standard-library `ast` import '
                    'closure (including imports inside functions), supplemented by reviewed subprocess entry '
                    'points and immutable-package declarations. External/stdlib dependency implementations '
                    'are not embedded. The companion inclusion-audit.json records the graph agreement, '
                    'file hashes and inclusion reasons.', '',
                    'Private config.toml, logs, SQL databases, native evidence, tests, scratch work, retired '
                    'providers and historical/rejected design documents are excluded.', '',
                    '## Directory Structure', '', '```text',
                    directory_tree([p.relative_to(root) for p in paths]), '```', '',
                    '## Inclusion reasons', '', '| File | Reason |', '|---|---|']
    for entry in entries:
        introduction.append(f"| `{entry['path']}` | {entry['reasons'][0].replace('|', '/')} |")
    introduction += ['', '## Runtime data referenced, not source bodies', '',
                     'These artifacts are data, not executable source. Their role is explicit; this source '
                     'export is not a standalone installable distribution.', '',
                     '| Artifact | Bytes | Role |', '|---|---:|---|']
    for path, role in sorted(resources.items(), key=lambda item: str(item[0])):
        introduction.append(f'| `{path.relative_to(root).as_posix()}` | {path.stat().st_size} | {role} |')
    introduction += ['', '## Excluded from this scope', '', *['- ' + x for x in excluded], '',
                     'External/standard-library import roots: ' + ', '.join(f'`{x}`' for x in external), '',
                     '---', '', '## File Contents', '']
    result = '\n'.join(introduction) + '\n' + ''.join(blocks)
    output.write_text(result, encoding='utf-8', newline='')
    saved = output.read_bytes().decode('utf-8')
    if saved != result:
        raise ValueError('export readback mismatch')
    # Check every embedded section against the original source, without trimming
    # or rewriting source text. File-specific fences handle embedded code fences.
    for entry, block in zip(entries, blocks):
        if saved.count(f"### `{entry['path']}`\n") != 1 or block not in saved:
            raise ValueError('missing or duplicated source section: ' + entry['path'])
        if digest((root / entry['path']).read_bytes()) != entry['sha256']:
            raise ValueError('source changed during export: ' + entry['path'])
    return dict(output=str(output), files=entries, bytes=output.stat().st_size,
                resources=[dict(path=str(p.relative_to(root)), role=r) for p, r in resources.items()],
                excluded=excluded, external_import_roots=external)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-directory', type=Path, default=Path('output/source-code-export'))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = (root / args.output_directory).resolve()
    if not output.is_relative_to(root):
        raise ValueError('export output must be inside the repository workspace')
    output.mkdir(parents=True, exist_ok=True)
    sources = Sources(root)
    scripts = tomllib.loads((root / 'pyproject.toml').read_text(encoding='utf-8'))['project']['scripts']
    runtime_seeds = {scripts['ck3chronicle'].split(':')[0]: 'Installed ck3chronicle console entry point'}
    handler = 'ck3chronicle.pipeline.database_handler'
    if handler not in (root / 'src/ck3chronicle/pipeline/request_handler.py').read_text(encoding='utf-8'):
        raise ValueError('reinspect the handler subprocess entry point before exporting')
    runtime_seeds[handler] = 'Subprocess entry point launched by request_handler.py (python -m)'
    runtime_seeds['ck3chronicle.reporting'] = (
        'Supported public diagnostic-query and source-search APIs delivered by Tasks 08A.1/08A.2')
    runtime_seeds['ck3chronicle.command_envelope'] = (
        'Application response helper explicitly retained by Task 06B for Task 08 command integration; '
        'not currently called by the CLI')
    runtime, runtime_modules, runtime_external = sources.closure(runtime_seeds)
    runtime_check = crosscheck_imports(root, runtime_seeds, runtime_modules, runtime_external)
    runtime_resources = {}
    selection_path = root / 'models/selection.json'
    selection = json.loads(selection_path.read_bytes())
    folder = (root / 'models' / selection['artifact_directory']).resolve()
    if not folder.is_relative_to(root / 'models'):
        raise ValueError('selected package escapes models directory')
    manifest, package_files = authenticated_files(folder, selection['manifest_sha256'])
    if manifest['package_id'] != selection['package_id']:
        raise ValueError('selected package identity mismatch')
    runtime[selection_path].add('Current default runtime package selection')
    runtime[folder / 'manifest.json'].add('Current selected executable package manifest')
    for path in package_files:
        if path.suffix == '.py':
            runtime[path].add('Selected immutable parser/matcher executable authenticated by package manifest')
        else:
            runtime_resources[path] = 'Selected package data read/authenticated by matcher_loader.py'
    runtime_resources[root / 'models/catalog.json'] = 'Explicit opt-in package selection catalog'
    excluded_runtime = [f'`{p.relative_to(root).as_posix()}`: not reachable from runtime entry points.'
                        for n, p in sorted(sources.modules.items())
                        if n.startswith('ck3chronicle') and n not in runtime_modules]
    excluded_runtime += ['Learner authoring/release tools: exported separately.',
                         'Non-default model packages and retained historical snapshots: optional explicit selections, '
                         'not the default runtime exported here. This exclusion does not classify them as dead code.']

    learner_seeds = {scripts[name].split(':')[0]: f'Installed {name} console entry point'
                     for name in ('ck3chronicle-learner-release', 'ck3chronicle-model-release')}
    learner, learner_modules, learner_external = sources.closure(learner_seeds)
    author_root = root / 'tools/template_learning'
    loader = author_root / 'learner_loader.py'
    declared = constant(loader, 'FILES')
    operations = constant(loader, 'OPERATIONS')
    author_seeds = {'template_learning.' + module: f'Supported release operation: {operation}'
                    for operation, module in operations.items()}
    author_seeds['template_learning.evidence_serialization'] = 'Documented data-only inspection command'
    author_seeds['template_learning.evaluate_unseen_session'] = 'Documented explicit-release evaluation entry point'
    author_closure, author_modules, author_external = sources.closure(author_seeds)
    merge(learner, author_closure)
    learner_external = sorted(set(learner_external) | set(author_external))
    learner_check = crosscheck_imports(root, {**learner_seeds, **author_seeds},
                                     set(learner_modules) | set(author_modules), learner_external)
    for name in declared:
        path = author_root / name
        if not path.is_file():
            raise ValueError(f'missing current learner distribution source: {path}')
        learner[path].add('Current source explicitly required by learner_loader.FILES for release creation')
    catalog_path = root / 'learners/catalog.json'
    catalog = json.loads(catalog_path.read_bytes())
    available = [r for r in catalog['releases'] if r['availability'] == 'available'
                 and r['publication_status'] == 'production' and isinstance(r.get('production_order'), int)]
    selected = max(available, key=lambda r: r['production_order'])
    retained = (root / 'learners' / selected['retained_path']).resolve()
    if not retained.is_relative_to(root / 'learners/releases'):
        raise ValueError('learner catalog path outside releases')
    learner_manifest, learner_files = authenticated_files(retained, selected['manifest_sha256'])
    if learner_manifest.get('completeness') != 'complete':
        raise ValueError('latest available production learner is not complete')
    learner[retained / 'manifest.json'].add('Latest complete production learner release manifest')
    for path in learner_files:
        learner[path].add('Retained executable/source resource of the latest complete production learner release')
    learner_resources = {catalog_path: 'Learner availability/selection catalog',
                         root / 'models/catalog.json': 'Model package availability/selection catalog'}
    # Current selected model evaluation dynamically executes the same package as
    # runtime; include its source here too so each export is independently readable.
    learner[selection_path].add('Default runtime selection consumed by package tools')
    learner[folder / 'manifest.json'].add('Default model package evaluated by model-release tools')
    for path in package_files:
        if path.suffix == '.py':
            learner[path].add('Default package dynamic executable used by model-release evaluation')
        else:
            learner_resources[path] = 'Default package data; source bodies are exported, generated model data is not'
    excluded_learner = [f'`{p.relative_to(root).as_posix()}`: outside supported operation/import and release-source closure.'
                       for n, p in sorted(sources.modules.items())
                       if n.startswith('template_learning') and p not in learner]
    excluded_learner += ['Older retained learner/model releases: optional version-specific execution, not this current-source export.',
                         'Working authoring and retained learner source are both included and separately labeled; '
                         'the current authoring tree is not substituted for immutable execution bytes.']
    common = ['Active means current on-disk supported code for the stated entry points, not a trace of a '
              'running watcher. Export generation does not inspect live-process state and makes no '
              'assertion that a live process has loaded these exact bytes.']
    reports = []
    reports.append(write_export(root, output / 'ck3chronicle-runtime-code.md',
        'ck3chronicle Runtime Codebase Export', common + [
            f'Default package: `{selection["package_id"]}`. Roots: `ck3chronicle.cli` and '
            '`ck3chronicle.pipeline.database_handler`, plus the supported `ck3chronicle.reporting` '
            'public library APIs and retained `ck3chronicle.command_envelope` helper '
            '(reporting CLI integration remains Task 08B). Includes their transitive project imports and '
            'the selected package Python source.'], runtime, runtime_resources, excluded_runtime, runtime_external))
    reports.append(write_export(root, output / 'ck3chronicle-learner-release-code.md',
        'ck3chronicle Learner and Release Tools Codebase Export', common + [
            'Roots: the installed learner-release and model-release commands, documented current learner '
            'operations and declared release-creation source files.',
            f'Latest complete production learner: `{selected["release_id"]}`. There is no implicit active '
            'learner selection: this is the current complete release chosen explicitly for the export.',
            'Includes current authoring source, its required project imports, the retained complete learner '
            'closure, and default model evaluation source. Older opt-in snapshots are excluded.'],
        learner, learner_resources, excluded_learner, learner_external))
    reports[0]['import_crosscheck'] = runtime_check
    reports[1]['import_crosscheck'] = learner_check
    (output / 'inclusion-audit.json').write_text(json.dumps(reports, indent=2) + '\n', encoding='utf-8')
    for report in reports:
        print(json.dumps(dict(output=report['output'], files=len(report['files']), bytes=report['bytes'])))


if __name__ == '__main__':
    main()
