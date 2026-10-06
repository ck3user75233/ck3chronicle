"""Owner-declared literal equivalence, preserving each native spelling.

These ranges are literal positions, never slot captures. Recognition requires
the declared prefix, suffix and original parser boundaries. Opaque fields win.
"""
import re


def ranges(pieces, declarations, excluded=()):
    text = ''.join(t for _, t in pieces)
    offsets = {0: 0}
    cursor = 0
    for index, (_, value) in enumerate(pieces):
        cursor += len(value)
        offsets[cursor] = index + 1
    result = {}
    for declaration in declarations:
        content = re.compile(declaration['pattern'])
        for prefix in re.finditer(declaration['prefix'], text):
            match = content.match(text, prefix.end())
            if not match or not text.startswith(declaration['suffix'], match.end()):
                continue
            a, b = offsets.get(match.start()), offsets.get(match.end())
            if a is None or b is None or any(x < b and a < y for x, y in excluded):
                continue
            result[a] = (b, declaration['id'])
    return result


def spelling(part, text, position=0):
    match = re.compile(part['format_pattern']).match(text, position)
    return match.group() if match else None
