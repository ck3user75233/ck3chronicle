"""Exercise the installed release using supplied genuine logs, outside checkout imports."""
import argparse
from collections import Counter
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import sys
import xml.etree.ElementTree as ET

from ck3chronicle import decoder
from ck3chronicle.pipeline.catalog import load_selected_classifier, selected_models_root
from ck3chronicle.pipeline.contracts import materialize_definitions, prepare_record, render_regions, run_lineage
from ck3chronicle.pipeline.domain import NativeReview
from ck3chronicle.reporting import presentation
from template_learning.learner_loader import resolve_release, authenticate, launch


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--package', required=True)
    cli.add_argument('--learner', required=True)
    cli.add_argument('--original-review', type=Path, required=True)
    cli.add_argument('--session55-receipt', type=Path, required=True)
    cli.add_argument('--source-survey', type=Path, required=True)
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args()
    prefix = Path(sys.prefix).resolve()
    assert Path(decoder.__file__).resolve().is_relative_to(prefix)
    assert selected_models_root().resolve() == prefix/'share/ck3chronicle/models'
    classifier = load_selected_classifier(package_id=args.package)
    definitions = materialize_definitions(classifier.package)
    output = args.output.resolve(); output.mkdir(parents=True, exist_ok=True)
    receipt = dict(status='running', scope='Installed ingestion, reconstruction and dependency closure; Data Intelligence export limitation reported separately.',
        python=platform.python_version(), prefix=str(prefix),
        sys_path=sys.path, application_modules={}, decoder_sha256=hashlib.sha256(Path(decoder.__file__).read_bytes()).hexdigest(),
        chardet_version=importlib.metadata.version('chardet'), logs=[])
    display_witness = None
    supplied = json.loads(args.session55_receipt.read_bytes())
    session55 = next(r for r in supplied['logs'] if r['sha256']=='cf3214a8186859223a9d3e5c36fafcd1d3d01c8ca715bcabcac986e3a2750740')
    for path, expected in [(args.original_review, '6695afb54d8924a1ce9dc033503328297ba3691907fa9694aac14448eccb0e74'),
                           (Path(session55['path']), session55['sha256'])]:
        data = path.read_bytes(); assert hashlib.sha256(data).hexdigest() == expected
        raw = classifier.read_log(path)
        assert b''.join(e.native_bytes() for e in raw.emissions) == data
        counts = Counter(); preserved = 0
        for result in classifier.classify_raw(raw):
            if isinstance(result, NativeReview):
                counts['unresolved'] += 1
                continue
            unit = result.diagnostic.unit
            if result.selected is None:
                counts['no_match'] += 1
                continue
            record = prepare_record(definitions[result.selected.template_id], result)
            counts[record['match_status']] += 1
            rendered = render_regions(definitions[result.selected.template_id], record['values'])
            native = [('body', unit['body']['text']), *[(k,v['text']) for k,v in unit['contexts'].items()],
                      *[('continuation:'+str(i),v['text']) for i,v in enumerate(unit['continuations'])]]
            assert dict(rendered) == dict(native)
            if any(0xDC80 <= ord(c) <= 0xDCFF for _, text in native for c in text):
                assert record['match_status']=='template'
                assert json.loads(json.dumps(record,ensure_ascii=True)) == record
                preserved += 1
                if display_witness is None:
                    display_witness = unit['body']['text']
        if path == args.original_review:
            assert counts == {'template': 3}
        else:
            assert preserved == 44
            assert sum(counts.values()) == session55['compared_native_units']
        receipt['logs'].append(dict(path=str(path),sha256=expected,counts=counts,
                                   preserved_byte_supported_messages=preserved,native_reconstruction=True))
    assert 'chardet' not in sys.modules, 'known UTF-8 ingestion unexpectedly imported detection'
    receipt['known_utf8_imported_detector'] = False
    # Track the pre-existing Data Intelligence limitation using actual native text.
    # This probes export helpers; it is not a fabricated stored Run or full CLI test.
    node = ET.Element('div'); presentation._el(node,'pre',display_witness)
    display = {}
    for label,text in [('json',json.dumps(display_witness,ensure_ascii=False)),
                       ('html',presentation._page('Genuine preserved-byte witness',node)),
                       ('text',presentation._plain(node))]:
        try:
            text.encode('utf-8',errors='strict')
            display[label] = dict(status='passed')
        except UnicodeEncodeError as exc:
            display[label] = dict(status='failed',exception=type(exc).__name__,reason=exc.reason)
    receipt['data_intelligence_display'] = dict(checks=display,
        scope='Installed export helpers on genuine session-55 text; not full stored-Run CLI acceptance.',
        disposition='Separate bounded Data Intelligence repair or owner disposition; native ingestion/storage preservation passes.')
    files = json.loads(args.source_survey.read_bytes())['files']
    witnesses = []
    for digest in ('3d93cf6154a309777d87fdb580430f69d125df54f42ae061b6cfe3cdfd0c58dc',
                   '89ef11bb8cb8a9ea70aab2fa022a1a5ad3622ae0c3790a08a09b0254c23341e7'):
        row = next(r for r in files if r['sha256']==digest)
        path = Path(row['path']); data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest()==digest
        result = decoder.read(path)
        if digest.startswith('3d93'):
            assert result.bom_bytes==3 and decoder.read(path,encoding='utf-8-sig').bom_bytes==3
            assert decoder.read(path,encoding='utf-8').bom_bytes==0
        else:
            assert result.text is None and result.status=='undetermined'
        witnesses.append(dict(path=str(path),sha256=digest,metadata=result.metadata()))
    receipt['source_witnesses'] = witnesses
    folder,pin=resolve_release(prefix/'share/ck3chronicle/learners',args.learner)
    manifest,payloads=authenticate(folder,pin)
    assert payloads['ck3chronicle/decoder.py']==Path(decoder.__file__).read_bytes()
    # A real retained operation on the genuine original three-emission shard;
    # fresh disposable output, never another release's learned state.
    launch(folder,pin,'learn',['--log',str(args.original_review),'--output-dir',str(output/'learner-probe')],
           receipt=str(output/'learner-execution.json'))
    receipt['learner'] = dict(release_id=args.learner,manifest_sha256=pin,parser=manifest['parser'])
    for name,module in list(sys.modules.items()):
        if name.startswith(('ck3chronicle','template_learning')) and getattr(module,'__file__',None):
            path=Path(module.__file__).resolve()
            assert path.is_relative_to(prefix),(name,path)
            if path.suffix=='.py':receipt['application_modules'][name]=dict(path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    source_hashes={name:row['sha256'] for name,row in receipt['application_modules'].items()}
    revision='sha256:'+hashlib.sha256(json.dumps(source_hashes,sort_keys=True).encode()).hexdigest()
    receipt['lineage']=run_lineage(classifier.package,application_revision=revision)
    receipt['status']='passed'
    (output/'receipt.json').write_text(json.dumps(receipt,ensure_ascii=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='passed',logs=receipt['logs'],learner=receipt['learner']),indent=2))


if __name__ == '__main__':
    main()
