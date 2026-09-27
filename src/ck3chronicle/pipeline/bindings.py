"""Bind model captures directly to the pinned parser's native byte ranges."""
from .domain import ByteSpan, Capture, NativeBinding, NativeRegion, OriginalAccess


def bind_captures(original: OriginalAccess, region: NativeRegion, captures: tuple[Capture, ...],
                  *, template_id: str, region_name: str) -> tuple[NativeBinding, ...]:
    bindings = []
    for capture in captures:
        if capture.span is None:
            if capture.value is not None:
                raise ValueError('an absent declared optional field has no value or range')
            span = None
        else:
            if capture.value is None:
                raise ValueError('a present capture requires a value')
            span = ByteSpan(region.span.start + capture.span.start, region.span.start + capture.span.end)
            if not region.span.contains(span):
                raise ValueError('capture lies outside its native region')
            if original.read_bytes(span) != capture.value.encode('utf-8', 'surrogateescape'):
                raise ValueError('capture differs from original source bytes')
        bindings.append(NativeBinding(template_id, region_name, capture.name, capture.type, capture.value, span))
    return tuple(bindings)
