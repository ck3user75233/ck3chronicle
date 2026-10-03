"""Cheap runtime logging ownership check. Run with the repository Python.

Only runtime_logging.py may configure logging. Research/support utilities and
tests are outside this runtime-source check. Import aliases are resolved; this
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
    for path in sorted((root / 'src' / 'ck3chronicle').rglob('*.py')):
        if path == root / 'src' / 'ck3chronicle' / 'runtime_logging.py':
            continue
        failures.extend(f'{path.relative_to(root)}:{line}: logging configuration outside runtime_logging.py: {name}'
                        for line, name in violations(path.read_text(encoding='utf-8')))
    return failures


if __name__ == '__main__':
    errors = check(Path(__file__).resolve().parents[1])
    print('\n'.join(errors) if errors else 'Runtime logging ownership check passed.')
    sys.exit(bool(errors))
