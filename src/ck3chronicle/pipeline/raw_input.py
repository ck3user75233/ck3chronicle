"""Project pinned parser units once; recovery remains wholly inside the package."""
from .domain import NativeDiagnostic, NativeReview


def iter_diagnostics(package, raw):
    for unit in package.iter_units(raw):
        if unit['recovery_status'] == 'unresolved':
            recovery = unit['recovery']
            yield NativeReview(raw, unit, recovery.reason or recovery.status)
        else:
            yield NativeDiagnostic(raw, unit)


def native_regions(unit):
    """API order, with each original region retaining its independent origin."""
    yield 'body', unit['body']
    for name in ('prefix', 'suffix'):
        if name in unit['contexts']:
            yield name, unit['contexts'][name]
    for index, region in enumerate(unit['continuations']):
        yield 'continuation:' + str(index), region


def matching_content(unit):
    """Complete cache input excluding only caller-owned occurrence provenance."""
    def region(value):
        return {key: item for key, item in value.items() if key != 'provenance'}
    return {**{k: v for k, v in unit.items()
               if k not in {'provenance', 'body', 'contexts', 'continuations'}},
            'body': region(unit['body']),
            'contexts': {name: region(value) for name, value in unit['contexts'].items()},
            'continuations': [region(value) for value in unit['continuations']]}
