"""Focused receiving repair checks on supplied retained genuine evidence only.

No ingestion, database access, detector tuning or generated diagnostic fixtures.
The disposable parser comparison is run separately by its existing harness.
"""
import argparse
import ast
import hashlib
import importlib.util
import inspect
import json
from pathlib import Path
import sys

from ck3chronicle import decoder


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--before-decoder', type=Path, required=True)
    cli.add_argument('--survey', type=Path, required=True)
    cli.add_argument('--log-receipt', type=Path, required=True)
    cli.add_argument('--source-receipt', type=Path, required=True)
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args()
    spec = importlib.util.spec_from_file_location('_reviewed_decoder_before_corrective', args.before_decoder)
    before = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = before
    spec.loader.exec_module(before)
    report = {'decoder_sha256': digest(Path(decoder.__file__).read_bytes()),
              'before_decoder_sha256': digest(args.before_decoder.read_bytes()),
              'logs': [], 'sources': [], 'checks': {}}
    assert inspect.getsource(before.inspect_source_header) == inspect.getsource(decoder.inspect_source_header)
    report['checks']['physical_header_inspector_unchanged'] = True

    # This structural check is explicitly inspection, not an invented double-BOM fixture.
    body = ast.parse(inspect.getsource(decoder.decode_fragment)).body[0]
    calls = [n for n in ast.walk(body) if isinstance(n, ast.Call)]
    assert len(calls) == 3
    assert {n.func.id for n in calls if isinstance(n.func, ast.Name)} == {'isinstance', 'TypeError'}
    byte_call = next(n for n in calls if isinstance(n.func, ast.Attribute))
    assert ast.unparse(byte_call) == "raw.decode('utf-8', errors='surrogateescape')"
    report['checks']['fragment_call_graph_no_header_detection_or_normalization'] = True
    assert 'chardet' not in sys.modules
    logs = json.loads(args.log_receipt.read_bytes())['logs']
    for row in logs:
        raw = Path(row['path']).read_bytes()
        assert digest(raw) == row['sha256']
        text = decoder.decode_fragment(raw)
        assert text == raw.decode('utf-8', 'surrogateescape')
        assert text.encode('utf-8', 'surrogateescape') == raw
        report['logs'].append({'path': row['path'], 'sha256': row['sha256'],
                              'bytes': len(raw), 'roundtrip': True,
                              'preserved_bytes': sum(0xdc80 <= ord(c) <= 0xdcff for c in text)})
    assert 'chardet' not in sys.modules
    report['checks']['genuine_known_utf8_checks_without_detector_import'] = True

    previous_sources = {r['path']: r for r in json.loads(args.source_receipt.read_bytes())}
    for row in json.loads(args.survey.read_bytes())['files']:
        raw = Path(row['path']).read_bytes()
        assert digest(raw) == row['sha256']
        old, new = before.decode(raw), decoder.decode(raw)
        assert old.text == new.text and old.metadata() == new.metadata(), row['path']
        assert new.metadata() == {k: v for k, v in previous_sources[row['path']].items() if k != 'path'}
        item = {'path': row['path'], 'sha256': row['sha256'], 'status': new.status,
                'automatic_text_and_metadata_unchanged': True}
        if raw.startswith(decoder.codecs.BOM_UTF8):
            old_sig = before.decode(raw, encoding='utf-8-sig')
            sig = decoder.decode(raw, encoding='utf-8-sig')
            native = decoder.decode(raw, encoding='utf-8')
            assert old_sig.text == sig.text == raw.decode('utf-8-sig')
            assert old_sig.bom_bytes == 0 and sig.bom_bytes == new.bom_bytes == 3
            assert native.bom_bytes == 0 and native.text == raw.decode('utf-8')
            assert sig.text.encode('utf-8') == raw[sig.bom_bytes:]
            assert decoder.decode_fragment(raw) == native.text
            assert decoder.decode_fragment(raw).encode('utf-8', 'surrogateescape') == raw
            item['bom_check'] = {'old_explicit_utf8_sig': 0, 'corrected_explicit_utf8_sig': 3,
                                 'automatic': 3, 'explicit_utf8': 0,
                                 'fragment_preserves_leading_bom': True}
        elif new.status == 'readable' and new.encoding == 'utf-8':
            sig = decoder.decode(raw, encoding='utf-8-sig')
            assert sig.bom_bytes == 0 and sig.text == new.text
            item['no_bom_explicit_utf8_sig'] = 0
        report['sources'].append(item)

    report['checks']['source_files_unchanged'] = len(report['sources'])
    report['checks']['genuine_utf8_bom_files_corrected'] = sum('bom_check' in r for r in report['sources'])
    report['checks']['undetermined_unchanged'] = sum(r['status'] == 'undetermined' for r in report['sources'])
    assert report['checks']['genuine_utf8_bom_files_corrected'] > 0
    assert report['checks']['undetermined_unchanged'] == 1
    report['limitations'] = [
        'No genuine internal double-BOM fragment or physical double-BOM positive example; separation verified by call-graph inspection.',
        'Explicit generic UTF-16/32 BOM consumption implemented by the same signature-length rule; no genuine positive examples tested.',
        'Existing source-search/report receipts reused: all sampled automatic text/metadata and caller bytes unchanged; no database checks run.',
    ]
    report['status'] = 'passed'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding='utf-8')
    print(json.dumps({'status': report['status'], 'checks': report['checks'], 'logs': report['logs']}, indent=2))


if __name__ == '__main__':
    main()
