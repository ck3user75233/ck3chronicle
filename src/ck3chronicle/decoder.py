"""Physical-source decoding/validation and lossless UTF-8 fragments; no release pin."""
from __future__ import annotations

import codecs
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
import re

HEADER_INSPECTION_BYTES = 4096
_SIGNATURES = ((codecs.BOM_UTF32_LE, 'utf-32-le'), (codecs.BOM_UTF32_BE, 'utf-32-be'),
               (codecs.BOM_UTF8, 'utf-8'), (codecs.BOM_UTF16_LE, 'utf-16-le'),
               (codecs.BOM_UTF16_BE, 'utf-16-be'))


def inspect_source_header(raw, *, end_of_file, encoding=None):
    """Inspect actual prefix bytes; decoding success does not mean a clean header.

    This bounded validation neither chooses a legacy codec nor repairs text.
    Warning codes describe observed patterns, not proof that CK3 rejected a file.
    """
    warnings = []
    def warn(code, label, offset, reason):
        if not any(w['code'] == code and w['byte_offset'] == offset for w in warnings):
            warnings.append({'severity': 'critical', 'code': code, 'label': label,
                             'byte_offset': offset, 'reason': reason})
    initial = next(((bom, codec) for bom, codec in _SIGNATURES if raw.startswith(bom)), None)
    skip = len(initial[0]) if initial else 0
    codec = initial[1] if initial else encoding or 'utf-8'
    signatures = []
    for bom, enc in _SIGNATURES:
        start = skip
        while (position := raw.find(bom, start)) != -1:
            signatures.append((position, bom, enc))
            start = position + len(bom)
    consumed = skip
    for position, bom, enc in sorted(signatures, key=lambda s: (s[0], -len(s[1]))):
        if position < consumed:
            continue  # UTF-32 signatures also contain shorter signatures.
        signature = (bom, enc)
        if initial and position == skip and signature == initial:
            warn('double_bom', 'double BOM', position, 'A second identical BOM immediately follows the initial signature.')
        elif initial and signature != initial:
            warn('conflicting_bom', 'conflicting BOM', position, 'A different encoding signature occurs inside the inspected header.')
        else:
            warn('displaced_bom', 'displaced BOM', position, 'A signature sequence occurs after preceding bytes; those bytes are preserved.')
        consumed = position + len(bom)
    decoding_issue = None
    try:
        decoder = codecs.getincrementaldecoder(codec)(errors='strict')
        text = decoder.decode(raw[skip:], final=end_of_file)
    except UnicodeError as exc:
        # Still report known prefix evidence. A non-UTF-8 unmarked file is not
        # automatically corrupt; deciding its legacy encoding is a separate step.
        text = raw[skip:skip + exc.start].decode(codec, errors='strict')
        decoding_issue = str(exc)
        if initial:
            warn('bom_byte_mismatch', 'BOM/byte mismatch', skip + exc.start,
                 'Header bytes do not decode strictly under their initial Unicode signature.')
    # Recognizable BOM mojibake forms, including repeated Western re-encoding.
    marker = '\u00ef\u00bb\u00bf'
    for _ in range(3):
        start = 0
        while (found := text.find(marker, start)) != -1:
            warn('mojibake', 'mojibake', skip + len(text[:found].encode(codec)),
                 'Literal BOM mojibake pattern found; suspected earlier mis-decoding, not automatically repaired.')
            start = found + len(marker)
        marker = marker.encode('utf-8').decode('cp1252')
    start = 0
    while (found := text.find('\ufffd', start)) != -1:
        warn('replacement_character', 'replacement character', skip + len(text[:found].encode(codec)),
             'Literal U+FFFD is already present; its origin and any lost character are unknown.')
        start = found + 1
    return {'status': 'critical' if warnings else 'undetermined' if decoding_issue else 'checked',
            'warnings': warnings, 'bytes_inspected': len(raw), 'end_of_file': end_of_file,
            'scope': f'First {HEADER_INSPECTION_BYTES} bytes; known BOM/mojibake/replacement patterns only. Not a whole-file encoding certificate.',
            'signature_encoding': initial[1] if initial else None,
            'decoding_issue': decoding_issue, 'prefix_hex': raw[:64].hex(' '),
            'escaped_prefix': text[:128].encode('unicode_escape').decode('ascii')}


def display_text(text: str) -> str:
    """Represent preserved bytes as \\xHH without changing valid Unicode."""
    return re.sub(r'[\udc80-\udcff]', lambda m: f'\\x{ord(m[0]) - 0xdc00:02X}', text)


def normalize_newlines(text: str) -> str:
    """Only physical CRLF/CR/LF endings; never Unicode/whitespace normalization."""
    return text.replace('\r\n', '\n').replace('\r', '\n')


def physical_lines(text: str) -> list[str]:
    """Return physical lines, preserving blanks and an unterminated final line."""
    if not text:
        return []
    lines = normalize_newlines(text).split('\n')
    return lines[:-1] if lines[-1] == '' else lines


def _newline_metadata(text):
    pairs = text.count('\r\n')
    counts = {'CRLF': pairs, 'LF': text.count('\n') - pairs, 'CR': text.count('\r') - pairs}
    styles = [name for name, count in counts.items() if count]
    return {'counts': counts, 'style': 'mixed' if len(styles) > 1 else styles[0] if styles else 'none',
            'terminal_newline': text.endswith(('\r', '\n'))}


def _text_codec(name):
    """Reject binary transforms and unknown codecs as configuration errors."""
    codec = codecs.lookup(name).name
    b''.decode(codec, errors='strict')
    return codec


@dataclass(frozen=True)
class DecodedText:
    """Physical-file result; bom_bytes counts leading BOM bytes omitted from text.

    This includes explicit BOM-consuming codecs. It is zero when no BOM was
    consumed, or when no processing text was returned. It is not a character
    offset map. Parser fragments return plain text via decode_fragment instead.
    """
    raw: bytes
    text: str | None
    status: str
    encoding: str | None
    method: str | None
    reason: str | None
    header: dict
    newlines: dict | None
    warnings: tuple[dict, ...] = ()
    bom_bytes: int = 0

    @property
    def display_text(self) -> str:
        """Render preserved bytes explicitly without changing processing text."""
        if self.text is None:
            raise ValueError(self.reason or self.status)
        return display_text(self.text)

    @property
    def working_text(self) -> str:
        return normalize_newlines(self.display_text)

    def metadata(self) -> dict:
        """Serializable outcomes without copying source bytes/text into reports."""
        return {'status': self.status, 'encoding': self.encoding, 'method': self.method,
                'reason': self.reason,
                'bytes': len(self.raw), 'bom_bytes': self.bom_bytes,
                'newlines': deepcopy(self.newlines), 'header': deepcopy(self.header),
                'warnings': deepcopy(list(self.warnings))}


def decode_fragment(raw: bytes) -> str:
    """Decode a native parser span as UTF-8/surrogateescape, without admission.

    A fragment has no physical-file header. Preserve BOM characters, undecodable
    bytes and newlines verbatim; no detection, inspection or normalization runs.
    The result encodes back to raw with UTF-8/surrogateescape.
    """
    if not isinstance(raw, bytes):
        raise TypeError('parser fragment decoding requires bytes')
    return raw.decode('utf-8', errors='surrogateescape')


def decode(raw: bytes, *, encoding=None) -> DecodedText:
    """Decode complete physical-source bytes, including header admission.

    Known encodings use surrogateescape to retain undecodable bytes. Automatic
    detection uses chardet's recommendation and its own minimum threshold, not
    agreement between alternative codecs. Neither certifies author intent.
    Internal parser spans must use decode_fragment, even with known UTF-8.
    """
    if not isinstance(raw, bytes):
        raise TypeError('source decoding requires bytes')
    override = _text_codec(encoding) if encoding is not None else None
    header = inspect_source_header(raw[:HEADER_INSPECTION_BYTES], end_of_file=len(raw) <= HEADER_INSPECTION_BYTES)
    initial = next(((mark, codec) for mark, codec in _SIGNATURES if raw.startswith(mark)), None)
    # An explicit codec retains its standard BOM semantics (utf-8 keeps it;
    # utf-8-sig consumes it). Automatic selection consumes the signature.
    skip = len(initial[0]) if initial and override is None else 0

    def result(text=None, *, status='readable', codec=None, method=None, reason=None, warnings=()):
        if text is not None:
            count = len(re.findall(r'[\udc80-\udcff]', text))
            if count:
                warnings = (*warnings, {'severity': 'warning', 'code': 'preserved_bytes',
                    'count': count, 'reason': 'Undecodable bytes preserved for processing; displayed as \\xHH.'})
        inspected = (inspect_source_header(raw[:HEADER_INSPECTION_BYTES],
                     end_of_file=len(raw) <= HEADER_INSPECTION_BYTES, encoding=codec)
                     if text is not None and codec not in {None, 'utf-8'} and initial is None else header)
        consumed_bom = 0
        if text is not None and initial and (skip or codec in {'utf-8-sig', 'utf-16', 'utf-32'}):
            consumed_bom = len(initial[0])
        return DecodedText(raw, text, status, codec, method, reason, inspected,
                             _newline_metadata(text) if text is not None else None, warnings, consumed_bom)

    if any(w['code'] == 'double_bom' for w in header['warnings']):
        return result(status='invalid_header', method='bom',
                      reason='Double BOM: content was not decoded for parsing or search. Header repair is not enabled.')

    if initial or override:
        codec = override or initial[1]
        if initial and override:
            signature_codec = initial[1]
            allowed = {signature_codec, 'utf-8-sig' if signature_codec == 'utf-8' else signature_codec[:-3]}
            if override not in allowed:
                return result(status='decode_error', codec=codec, method='bom', reason='Explicit encoding conflicts with the initial BOM.')
        method = 'known' if override else 'bom'
        try:
            return result(raw[skip:].decode(codec, errors='surrogateescape'), codec=codec, method=method)
        except UnicodeError as exc:
            return result(status='decode_error', codec=codec, method=method, reason=str(exc))
    if b'\x00' not in raw:
        try:
            return result(raw.decode('utf-8', errors='strict'), codec='utf-8',
                          method='ascii_compatible' if raw.isascii() else 'utf8')
        except UnicodeError:
            pass
    # UTF-8/Unicode fast paths above do not need heuristic detection.
    from chardet import detect, MINIMUM_THRESHOLD
    detected = detect(raw, max_bytes=len(raw), prefer_superset=True)
    if not detected['encoding'] or detected['confidence'] <= MINIMUM_THRESHOLD:
        return result(status='undetermined', method='detected',
                      reason=f"Detector did not support a reading above its minimum threshold ({detected['confidence']:.3f} <= {MINIMUM_THRESHOLD}).")
    codec = _text_codec(detected['encoding'])
    try:
        text = raw.decode(codec, errors='strict')
    except UnicodeError as exc:
        return result(status='decode_error', codec=codec, method='detected', reason=str(exc))
    warnings = [{'severity': 'warning', 'code': 'encoding_inferred',
                 'confidence': detected['confidence'],
                 'reason': f'Encoding inferred as {codec} by chardet; this is a heuristic interpretation.'}]
    return result(text, codec=codec, method='detected', warnings=tuple(warnings))


def read(path: str | Path, *, encoding=None) -> DecodedText:
    """Read a complete physical source file, then apply decode's admission rules."""
    return decode(Path(path).read_bytes(), encoding=encoding)


class Decoder:
    """Physical-source convenience object; parser spans use decode_fragment."""
    def __init__(self, *, encoding: str | None = None):
        self.encoding = _text_codec(encoding) if encoding is not None else None

    def settings(self):
        return {'encoding': self.encoding, 'policy': 'Python codecs; chardet for unknown encodings; no header repair.',
                'working_newlines': 'LF', 'preserved_bytes_display': '\\xHH'}

    def decode(self, raw: bytes) -> DecodedText:
        return decode(raw, encoding=self.encoding)

    def read(self, path: str | Path) -> DecodedText:
        return read(path, encoding=self.encoding)


def main(argv=None):
    """Read-only source inspection: python -m ck3chronicle.decoder PATH."""
    import argparse
    import json
    parser = argparse.ArgumentParser(description='Decode a source file without rewriting it.')
    parser.add_argument('path', type=Path)
    parser.add_argument('--encoding', help='Explicit source-text codec; never an automatic repair.')
    args = parser.parse_args(argv)
    try:
        result = Decoder(encoding=args.encoding).read(args.path)
    except (OSError, LookupError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result.metadata(), ensure_ascii=True, indent=2))
    return 0 if result.text is not None else 1


if __name__ == '__main__':
    raise SystemExit(main())

