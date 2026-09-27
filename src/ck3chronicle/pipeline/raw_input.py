"""Adapt the selected lossless parser without lexing or normalizing again."""
from pathlib import Path

from template_learning.parsers import ParserReference, load_parser, iter_recoveries

from .domain import ByteSpan
from .domain import NativeContinuation, NativeDiagnostic, NativeRegion, UnresolvedEmission


def read_raw_log(path: Path | str, *, parser_reference: dict):
    parser = load_parser(ParserReference.from_dict(parser_reference))
    return parser.parse_file(path)


def _region(message) -> NativeRegion:
    return NativeRegion(message.text, tuple((p.kind, p.text) for p in message.pieces),
                        ByteSpan(message.span.start, message.span.end))


def iter_diagnostics(raw):
    """Retain each complete recovered error once, including supporting entries."""
    for recovery in iter_recoveries(raw):
        emission = recovery.parent
        parents = getattr(recovery, 'parents', (emission,))
        span = ByteSpan(emission.span.start, parents[-1].span.end)
        if recovery.status != 'recovered':
            yield UnresolvedEmission(raw, emission.ordinal, emission.source_family, span,
                                     recovery.reason or recovery.status)
            continue
        context_kind, contexts = 'body', ()
        if recovery.structure == 'located-message-wrapper':
            context_kind = recovery.structure
            bounds = (
                ('prefix', emission.body_span.start, recovery.messages[0].span.start),
                ('suffix', recovery.messages[-1].span.end, emission.body_span.end),
            )
            contexts = tuple((name, _region(emission.select_messages(((a, b),))[0]))
                             for name, a, b in bounds)
        for message in recovery.messages:
            entries = tuple(NativeContinuation(_region(entry.message),
                ByteSpan(entry.prefix_span.start, entry.prefix_span.end),
                ByteSpan(entry.label_span.start, entry.label_span.end),
                ByteSpan(entry.value_span.start, entry.value_span.end),
                entry.message.parent.ordinal, entry.message.parent.source_tag)
                for entry in getattr(message, 'continuations', ()))
            yield NativeDiagnostic(raw, emission.source_family, emission.source_tag, emission.ordinal,
                                   message.ordinal, span, _region(message),
                                   'continuation:' + recovery.structure if entries else context_kind, contexts,
                                   entries, tuple(e.ordinal for e in parents), recovery.reason)
