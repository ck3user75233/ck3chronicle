"""Locate source references in stored contract regions, without rematching logs."""
from pathlib import PurePosixPath
import re

from ..pipeline.contracts import render_regions


# A path needs a directory or filename extension; a number, key or C++ emitter
# is not a source path. These patterns read stored rendered regions only.
_PATH = re.compile(r'(?<![\w@])(?:[A-Za-z]:[\\/])?(?:[\w.@+() -]+[\\/])+[\w.@+() -]+\.[A-Za-z0-9_]+')
_LINE_AFTER = re.compile(r'''^["']?\s*(?:,\s*)?(?:near\s+)?line\s*:?\s*(-?\d+)''', re.IGNORECASE)
_LINE_BEFORE = re.compile(r'\bline\s*:?\s*(-?\d+)(?:\s+and\s+column\s*:?\s*-?\d+)?\s+in\s*["\']?\s*$', re.IGNORECASE)


def _usable_path(value):
    value = value.strip().replace('\\', '/')
    path = PurePosixPath(value)
    if not path.suffix or path.suffix.casefold() in {'.cpp', '.h', '.hpp'}:
        return None
    if '\n' in value or '\r' in value or value.lstrip('-').isdigit():
        return None
    return value


def source_references(record: dict) -> dict:
    """Return ordered path/line references and their presence in one stored record.

    Exact LOCATOR values take priority. Literal paths visible in rendered regions
    supplement them. Line labels must be adjacent; numeric locators alone never
    produce a path. Original region/slot references accompany each association.
    """
    regions = dict(render_regions(record['definition'], record['values']))
    found, seen = [], set()
    for region in record['values']['regions']:
        text = regions[region['name']]
        located = []
        cursor = 0
        for binding in region['bindings']:
            if not binding['present']:
                continue
            value = binding['value']
            offset = text.find(value, cursor)
            if offset < 0:
                continue
            cursor = offset + len(value)
            if binding['type'] == 'LOCATOR':
                path = _usable_path(value)
                if path:
                    located.append((offset, offset + len(value), path, binding['slot_id'], 'binding'))
        for match in _PATH.finditer(text):
            if any(start < match.end() and match.start() < end for start, end, *_ in located):
                continue
            # Strip surrounding prose up to a known file/location label. Literal
            # candidates without a clean path boundary remain unassigned evidence.
            raw = match.group().strip()
            path = _usable_path(raw)
            if path and ' ' not in path.split('/')[0]:
                located.append((match.start(), match.end(), path, None, 'stored_text'))
        for start, end, path, slot, kind in sorted(located):
            after = _LINE_AFTER.search(text[end:])
            before = _LINE_BEFORE.search(text[:start]) if after is None else None
            line = int((after or before).group(1)) if after or before else None
            key = (path, line, region['name'])
            if key in seen:
                continue
            seen.add(key)
            found.append({'path': path, 'line': line, 'region': region['name'],
                          'slot_id': slot, 'evidence': kind,
                          'role': 'supporting' if region['component_index'] is not None or
                          text[:start].rsplit('\n', 1)[-1].strip() == 'file:' else 'location'})
    return {'references': found, 'status': 'present' if found else 'no_path'}
