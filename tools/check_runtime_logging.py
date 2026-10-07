"""Cheap runtime logging ownership check. Run with the repository Python.

Only runtime_logging.py may configure logging. The declared Learner hook sources
are included; other research/support utilities and tests are outside this check.
Retained copies require separate authentication. Import aliases are resolved; this
is a small AST check, not a general linter or a defense against deliberate evasion.
"""
import ast
from pathlib import Path
import sys

CONFIGURATION = {
    'basicConfig', 'dictConfig', 'fileConfig', 'FileHandler', 'RotatingFileHandler',
    'TimedRotatingFileHandler', 'StreamHandler', 'NullHandler', 'Formatter',
    'addHandler', 'removeHandler', 'setFormatter', 'setLevel',
}

LEARNER_HOOK_SOURCES = (
    'learner_loader.py', 'artifacts.py', 'records.py',
    'incremental_template_registry.py',
)


def violations(source):
    tree = ast.parse(source)
    aliases = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for item in node.names:
                aliases[item.asname or item.name] = (node.module or '') + '.' + item.name
        elif isinstance(node, ast.Import):
            for item in node.names:
                aliases[item.asname or item.name] = item.name
    failures = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = ast.unparse(node.func)
        head, _, tail = name.partition('.')
        resolved = aliases.get(head, head) + ('.' + tail if tail else '')
        if resolved.rsplit('.', 1)[-1] in CONFIGURATION:
            failures.append((node.lineno, name))
    return failures


def check(root):
    failures = []
    paths = list((root / 'src' / 'ck3chronicle').rglob('*.py'))
    paths.extend(root / 'tools' / 'template_learning' / name for name in LEARNER_HOOK_SOURCES)
    for path in sorted(paths):
        if path == root / 'src' / 'ck3chronicle' / 'runtime_logging.py':
            continue
        failures.extend(f'{path.relative_to(root)}:{line}: logging configuration outside runtime_logging.py: {name}'
                        for line, name in violations(path.read_text(encoding='utf-8')))
        if path == root / 'src' / 'ck3chronicle' / 'journal.py':
            # The retained adapter may depend only on stdlib and its backend.
            tree = ast.parse(path.read_text(encoding='utf-8'))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    allowed = all(item.name.split('.')[0] in sys.stdlib_module_names
                                  for item in node.names)
                elif isinstance(node, ast.ImportFrom):
                    allowed = (node.level == 1 and node.module is None
                               and all(item.name == 'runtime_logging' for item in node.names)
                               or node.level == 1 and node.module == 'runtime_logging'
                               or node.level == 0 and (node.module or '').split('.')[0]
                               in sys.stdlib_module_names)
                else:
                    continue
                if not allowed:
                    failures.append(f'{path.relative_to(root)}:{node.lineno}: '
                                    'journal imports outside stdlib/runtime_logging')
    return failures


if __name__ == '__main__':
    errors = check(Path(__file__).resolve().parents[1])
    print('\n'.join(errors) if errors else 'Runtime logging ownership check passed.')
    sys.exit(bool(errors))
