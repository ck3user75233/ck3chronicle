"""Bind each selected region once against this occurrence's original bytes."""
from .domain import ByteSpan, NativeBinding, ResultIntegrityError


def bind_captures(original, region: dict, captures: list) -> tuple[NativeBinding, ...]:
    try:
        origin = ByteSpan(*region['provenance']['span'])
        if original.read_bytes(origin) != region['text'].encode('utf-8', 'surrogateescape'):
            raise ResultIntegrityError('selected region differs from original source bytes')
        bindings = []
        for capture in captures:
            present, value, relative = capture['present'], capture['value'], capture['span']
            if type(present) is not bool:
                raise ResultIntegrityError('capture presence must be explicit')
            if not present:
                if value is not None or relative is not None:
                    raise ResultIntegrityError('absent field has a value or span')
                span = None
            else:
                if not isinstance(value, str) or relative is None:
                    raise ResultIntegrityError('present capture requires value and span')
                local = ByteSpan(*relative)
                span = ByteSpan(origin.start + local.start, origin.start + local.end)
                if not origin.contains(span):
                    raise ResultIntegrityError('capture lies outside its native region')
                if original.read_bytes(span) != value.encode('utf-8', 'surrogateescape'):
                    raise ResultIntegrityError('capture differs from original source bytes')
            bindings.append(NativeBinding(capture['slot_id'], capture['type'], value, present, span))
        return tuple(bindings)
    except (KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, ResultIntegrityError):
            raise
        raise ResultIntegrityError('inconsistent selected capture: ' + str(exc)) from exc
