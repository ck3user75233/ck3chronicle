"""Native lexer audit and research comparison; not a parser implementation.

Only complete native logs from an explicit saved selection are evaluation inputs.
Do not add constructed probes or fixtures. Outputs belong outside Git.
The selected backend audits the supplied parser artifact. Other backends are
research comparisons, never selected by the parser loader.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import ctypes
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import re
import sys
import time

from template_learning.parsers import load_parser, reference_from_manifest

CORE = ': / \\ { } [ ] ( )'.replace(' ', '')
EXTRA = '"<>=;|'
RECOMMENDED_EXTRA = '"<>='
MANIFEST = Path('tools/template_learning/parsers/v1/manifest.json')


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + '\n', encoding='utf-8')


def patterns(separators):
    boundary = re.escape(separators.replace('/', '').replace('\\', ''))
    chars = re.escape(separators)
    # Complete lexical policy: no edge-stripping pass runs after either lexer.
    # Other filename/symbol punctuation stays in WORD unless it is an explicit
    # contextual punctuation mark at the edge of a run.
    div = rf'''(?<![^\s{boundary}',])Div/0(?=$|[\s{boundary}]|[',.!?]+(?=$|[\s{boundary}]))'''
    dots = rf'(?<![^\s{chars}])\.{{1,2}}(?=$|[\s{chars}])'
    edge = rf'''(?<![^\s{chars}])[',]|[',.!?](?=[',.!?]*(?:$|[\s{chars}]))'''
    word = rf'''[^\s{chars}]+?(?=[',.!?]*(?:$|[\s{chars}]))'''
    return [('DIVZERO.10',div),('DOTS.5',dots),('EDGE.3',edge),
            ('SEP.2','['+chars+']'),('GAP.1',r'\s+'),('WORD',word)]


def grammar(separators):
    def terminal(name, pattern):
        return name + ': /' + pattern.replace('/', r'\/') + '/'
    rules=patterns(separators)
    return '\n'.join(['start: ('+' | '.join(n.split('.')[0] for n,_ in rules)+')*',
                      *(terminal(n,p) for n,p in rules), ''])


def build_backend(name, parser, separators, standalone_path=None):
    if name in {'control', 'selected'}:
        return parser.implementation.lexical_pieces
    if name == 'handwritten':
        scanner = re.compile('|'.join('(?:'+pattern+')' for _,pattern in patterns(separators)))
        def scan(text):
            for match in scanner.finditer(text):
                yield match.start(), match.end(), match.group()
    elif name in {'lark', 'lark-selective', 'standalone'}:
        if name == 'standalone':
            spec = importlib.util.spec_from_file_location('_evaluated_standalone', standalone_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            engine = module.Lark_StandAlone()
            # Generated LALR modules otherwise rebuild their BasicLexer on every
            # lex() call in 1.3.1. This is a pinned generated-code integration,
            # using its internal constructor once, not a new runtime fallback.
            engine.lexer = engine._build_lexer()
        else:
            from lark import Lark
            engine = Lark(grammar(separators), parser=None, lexer='basic',
                          keep_all_tokens=True, maybe_placeholders=False)
        if name == 'lark-selective':
            whitespace_runs = re.compile(r'\s+|\S+')
            separator_search = re.compile('[' + re.escape(separators) + ']')
            plain_scanner = re.compile('|'.join('(?:'+pattern+')' for _,pattern in patterns(separators)))
            def scan(text):
                for run in whitespace_runs.finditer(text):
                    value = run.group()
                    if value.isspace():
                        yield run.start(), run.end(), value
                    elif not separator_search.search(value):
                        for token in plain_scanner.finditer(value):
                            yield run.start()+token.start(), run.start()+token.end(), token.group()
                    else:
                        for token in engine.lex(value):
                            yield run.start()+token.start_pos, run.start()+token.end_pos, str(token)
        else:
            def scan(text):
                for token in engine.lex(text):
                    yield token.start_pos, token.end_pos, str(token)
    else:
        raise ValueError(name)
    Span, Piece = parser.implementation.Span, parser.implementation.Piece
    def lex(source, span):
        text = source.read_text(span)
        bytepos, charpos, result = span.start, 0, []
        for start, end, value in scan(text):
            if start != charpos or value != text[start:end]:
                raise AssertionError('scanner omitted or changed characters')
            charpos = end
            gap = value.isspace()
            byteend = bytepos + len(value.encode('utf-8', 'surrogateescape'))
            result.append(Piece(Span(bytepos, byteend), value, 'gap' if gap else 'token'))
            bytepos = byteend
        if charpos != len(text) or bytepos != span.end:
            raise AssertionError('scanner did not consume complete input')
        return tuple(result)
    return lex


def peak_memory():
    class PMC(ctypes.Structure):
        _fields_ = [('cb', ctypes.c_ulong), ('PageFaultCount', ctypes.c_ulong)] + [
            (name, ctypes.c_size_t) for name in ('PeakWorkingSetSize', 'WorkingSetSize',
            'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage', 'QuotaPeakNonPagedPoolUsage',
            'QuotaNonPagedPoolUsage', 'PagefileUsage', 'PeakPagefileUsage', 'PrivateUsage')]
    k32, psapi = ctypes.WinDLL('kernel32'), ctypes.WinDLL('psapi')
    k32.GetCurrentProcess.restype = ctypes.c_void_p
    psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(PMC), ctypes.c_ulong]
    counters = PMC()
    counters.cb = ctypes.sizeof(counters)
    if not psapi.GetProcessMemoryInfo(k32.GetCurrentProcess(), ctypes.byref(counters), counters.cb):
        raise ctypes.WinError()
    return {key: getattr(counters, key) for key in
            ('PeakWorkingSetSize', 'WorkingSetSize', 'PrivateUsage', 'PeakPagefileUsage')}


def compact(pieces):
    return [[p.kind, p.text, p.span.start, p.span.end] for p in pieces]


def verify(source, span, pieces, separators=None):
    at = span.start
    for piece in pieces:
        assert piece.span.start == at and piece.span.end > at
        assert source.read_bytes(piece.span) == piece.text.encode('utf-8', 'surrogateescape')
        assert piece.kind == ('gap' if piece.text.isspace() else 'token')
        if separators and piece.text != 'Div/0':
            assert not any(c in separators for c in piece.text) or len(piece.text) == 1
        at = piece.span.end
    assert at == span.end
    assert b''.join(p.text.encode('utf-8', 'surrogateescape') for p in pieces) == source.read_bytes(span)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--selection', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--mode', choices=['audit', 'benchmark', 'equivalence'], default='audit')
    ap.add_argument('--backend', choices=['control', 'selected', 'handwritten', 'lark', 'lark-selective', 'standalone'], default='selected')
    ap.add_argument('--parser-manifest', type=Path, default=MANIFEST)
    ap.add_argument('--control-manifest', type=Path,
                    help='Explicit baseline artifact for a native before/after audit')
    ap.add_argument('--standalone', type=Path)
    ap.add_argument('--separator-policy', choices=['core','recommended','expanded'], default='recommended')
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    separators = CORE + {'core':'','recommended':RECOMMENDED_EXTRA,'expanded':EXTRA}[args.separator_policy]
    reference = reference_from_manifest(args.parser_manifest)
    parser = load_parser(reference)
    control = load_parser(reference_from_manifest(args.control_manifest)) if args.control_manifest else parser
    if args.backend == 'selected':
        separators = ''.join(sorted(parser.implementation.ALWAYS_SEPARATORS))
    selection = json.loads(args.selection.read_text(encoding='utf-8'))
    start = time.perf_counter()
    backend = build_backend(args.backend, parser, separators, args.standalone)
    equivalent = build_backend('handwritten', parser, separators) if args.mode == 'equivalence' else None
    init_seconds = time.perf_counter() - start
    metadata = dict(mode=args.mode, backend=args.backend, separators=separators,
        selected_parser=reference.to_dict(), control_parser=control.reference.to_dict(),
        python=sys.version, platform=platform.platform(),
        experiment_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        init_seconds=init_seconds, selection_sha256=hashlib.sha256(args.selection.read_bytes()).hexdigest())
    if args.backend.startswith('lark'):
        import lark
        metadata['lark_version'] = lark.__version__
    if args.standalone:
        metadata['standalone_sha256'] = hashlib.sha256(args.standalone.read_bytes()).hexdigest()
    if args.backend != 'selected':
        (args.output / 'candidate.lark').write_text(grammar(separators), encoding='utf-8')
    reports, counts, contexts, examples = [], Counter(), defaultdict(dict), []
    changed_sources = Counter()
    for log in selection['logs']:
        data = Path(log['path']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == log['sha256']
        started = time.perf_counter()
        parsed = parser.parse_bytes(data, source_name=log['path'])
        framing_seconds = time.perf_counter() - started
        pieces_count, changed, recovered, unresolved = 0, 0, 0, 0
        token_digest = hashlib.sha256()
        lex_seconds = 0.0
        original_lex = parser.implementation.lexical_pieces
        baseline_lex = control.implementation.lexical_pieces
        for emission in parsed.emissions:
            started = time.perf_counter()
            pieces = backend(parsed.source, emission.body_span)
            lex_seconds += time.perf_counter() - started
            pieces_count += len(pieces)
            if args.mode == 'benchmark':
                continue
            if args.mode == 'equivalence':
                assert pieces == equivalent(parsed.source, emission.body_span)
                assert parsed.source.read_bytes(emission.header_span) + b''.join(
                    x.text.encode('utf-8','surrogateescape') for x in pieces) == emission.native_bytes()
                for piece in pieces:
                    token_digest.update(f'{piece.span.start}:{piece.span.end}:{piece.kind};'.encode('ascii'))
                continue
            verify(parsed.source, emission.body_span, pieces, None if args.backend == 'control' else separators)
            # Header + tokenized body reconstruct each complete emission.
            assert parsed.source.read_bytes(emission.header_span) + b''.join(
                p.text.encode('utf-8', 'surrogateescape') for p in pieces) == emission.native_bytes()
            control_pieces = baseline_lex(parsed.source, emission.body_span)
            verify(parsed.source, emission.body_span, control_pieces)
            is_changed = compact(control_pieces) != compact(pieces)
            changed += is_changed
            changed_sources[emission.source_family] += is_changed
            if is_changed and len(examples) < 100:
                # First distinct body examples, documented selection (not random).
                if not any(e['raw_body'] == emission.body_text for e in examples):
                    examples.append(dict(sha256=log['sha256'], source=emission.source_family,
                        emission_ordinal=emission.ordinal, emission_span=[emission.span.start, emission.span.end],
                        raw_body=emission.body_text, control=compact(control_pieces), proposed=compact(pieces)))
            for p in pieces:
                token_digest.update(f'{p.span.start}:{p.span.end}:{p.kind};'.encode('ascii'))
            body = emission.body_text
            for char in CORE + EXTRA:
                amount = body.count(char)
                if not amount:
                    continue
                counts[char] += amount
                counts[char + '_emissions'] += 1
                if len(contexts[char]) >= 35:
                    continue
                for match in re.finditer(re.escape(char), body):
                    i = match.start()
                    snippet = body[max(0, i-50):i+65]
                    interior = i > 0 and i+1 < len(body) and not body[i-1].isspace() and not body[i+1].isspace()
                    key = ('internal:' if interior else 'edge:') + snippet
                    if key not in contexts[char] and len(contexts[char]) < 35:
                        contexts[char][key] = dict(source=emission.source_family, sha256=log['sha256'],
                            emission_ordinal=emission.ordinal, body_span=[emission.body_span.start, emission.body_span.end],
                            snippet=snippet, char_index=i, internal=interior)
            recovery = emission.recovery
            parser.implementation.lexical_pieces = backend
            try:
                proposed_recovery = emission.recovery
            finally:
                parser.implementation.lexical_pieces = original_lex
            assert proposed_recovery == recovery
            recovered += len(recovery.messages)
            unresolved += len(recovery.unresolved_spans)
            assert b''.join(parsed.source.read_bytes(s) for s in recovery.ordered_spans) == emission.native_bytes()
        if args.mode != 'benchmark':
            assert b''.join(e.native_bytes() for e in parsed.emissions) == data
        reports.append(dict(sha256=log['sha256'], bytes=len(data), emissions=len(parsed.emissions),
            pieces=pieces_count, changed_emissions=changed, recovered_messages=recovered,
            unresolved_spans=unresolved, framing_seconds=framing_seconds, lex_seconds=lex_seconds,
            boundary_digest=token_digest.hexdigest(), memory=peak_memory()))
        print(json.dumps(reports[-1]), flush=True)
        del parsed, data
    metadata.update(logs=reports, total_bytes=sum(r['bytes'] for r in reports),
        total_lex_seconds=sum(r['lex_seconds'] for r in reports), memory=peak_memory())
    dump(args.output / 'summary.json', metadata)
    if args.mode == 'audit':
        dump(args.output / 'punctuation-evidence.json', dict(counts=dict(counts), contexts=contexts))
        dump(args.output / 'native-comparisons.json', dict(selection='First 100 distinct changed emission bodies in saved log order',
            changed_source_counts=dict(changed_sources), examples=examples))


if __name__ == '__main__':
    main()
