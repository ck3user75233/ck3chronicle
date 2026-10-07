"""Recover an export from a hash-pinned, written research bundle with bounded memory.

This empirical adapter does not infer or edit templates. It projects away only
research fields which compact_model/compact_template/pattern_identity already
discard, verifies every input payload, and runs the owning full native export
parity check. The resulting native release is input to the established immutable
source-release packaging operation. Original research artifacts stay untouched.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import time
from types import SimpleNamespace

from template_learning.learner_loader import authenticate, source_payloads
from template_learning.location_candidate_experiment import save, sha
from template_learning.publish_native_model import (
    compact_model, compact_template, validate_native_export, canonical_bytes,
    ARTIFACTS, RELEASE_SCHEMA,
)
from template_learning.matching_primitives import pattern_identity


# These are research-only fields discarded by the owning compaction functions.
TEMPLATE_METADATA={'inference_refinements','region_hypotheses','unsupported_members'}
PART_METADATA={'observed_values','observed_absence','inference_basis','inference_rule',
               'field_support','rejection_reason','parameter_definition','empirical_region'}
ROOT_METADATA={'region_discovery','template_retirement'}
KEY=re.compile(rb'^( +)"([^"\\]+)": ')


def project(path, expected):
    """Read the existing canonical pretty JSON; discard no executable fields.

    Replaced research values become null in this private projection so commas
    remain exact. This projection is never a candidate or a published artifact.
    The actual owner compactor removes these fields after JSON decoding.
    """
    digest=hashlib.sha256();result=bytearray();removed=Counter()
    skip=None;root_key=None;prefix=None;field=None;lines=0;total=0
    with path.open('rb',buffering=8*1024*1024) as stream:
        for line in stream:
            digest.update(line);lines+=1;total+=len(line)
            if skip is not None:
                removed[field]+=len(line)
                indent=len(line)-len(line.lstrip(b' '))
                if indent==skip and line.lstrip().startswith((b'}',b']')):
                    result.extend(prefix+b'null'+(b',' if line.rstrip().endswith(b',') else b'')+b'\n')
                    skip=None
                continue
            match=KEY.match(line)
            if match:
                indent=len(match[1]);key=match[2].decode('ascii')
                if indent==2:root_key=key
                discard=(indent==2 and key in ROOT_METADATA) or (
                    root_key=='templates' and key in TEMPLATE_METADATA|PART_METADATA)
                if discard:
                    field=key;removed[field]+=len(line);prefix=line[:match.end()]
                    tail=line[match.end():].strip()
                    if tail in {b'[',b'{'}:skip=indent
                    else:result.extend(prefix+b'null'+(b',' if tail.endswith(b',') else b'')+b'\n')
                    continue
            result.extend(line)
    assert skip is None,'truncated research field'
    assert digest.hexdigest()==expected,'research payload hash mismatch'
    print(json.dumps(dict(input_bytes=total,projection_bytes=len(result),removed_bytes=removed)),flush=True)
    return json.loads(result),dict(input_bytes=total,projection_bytes=len(result),removed_bytes=removed,
                                  input_sha256=digest.hexdigest(),physical_lines=lines)


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--bundle',type=Path,required=True)
    cli.add_argument('--bundle-pin',required=True)
    cli.add_argument('--release',type=Path,required=True)
    cli.add_argument('--release-pin',required=True)
    cli.add_argument('--output',type=Path,required=True)
    cli.add_argument('--application-source',type=Path,required=True)
    args=cli.parse_args();start=time.monotonic();bundle=args.bundle.resolve();out=args.output.resolve()
    assert not out.exists();out.mkdir(parents=True)
    assert sha(bundle/'manifest.json')==args.bundle_pin
    manifest=json.loads((bundle/'manifest.json').read_bytes())
    release,payloads=authenticate(args.release,args.release_pin)
    # The adapter calls unchanged owning implementations, never ambient replacements.
    source=Path(__file__).parent
    for name, data in source_payloads(source, application_source=args.application_source).items():
        assert data==payloads[name],name
    expected_release=dict(release_id=release['release_id'],manifest_sha256=args.release_pin,
                          learner_identity=release['learner_identity']['sha256'])
    assert manifest['learner_release']==expected_release
    for name,expected in manifest['hashes'].items():
        assert (bundle/name).resolve().parent==bundle
        if name!='empirical_template_model.json':assert sha(bundle/name)==expected,name
    candidate,proof=project(bundle/'empirical_template_model.json',manifest['hashes']['empirical_template_model.json'])
    assert candidate['revision_id']==manifest['revision_id']
    assert candidate['learner_release']==expected_release
    assert candidate['algorithm']['learner_identity']==release['learner_identity']
    assert candidate['parser']==manifest['parser']
    # Verify the recovered metadata sets are truly absent from owner compaction.
    for template in candidate['templates']:
        assert not TEMPLATE_METADATA.intersection(compact_template(template))
        assert all(not PART_METADATA.intersection(part) for part in pattern_identity(template['parts']))
    model=compact_model(candidate)
    assert not ROOT_METADATA.intersection(model)
    proof.update(source_manifest_sha256=args.bundle_pin,source_bundle=str(bundle),
                 source_candidate_revision=candidate['revision_id'],learner_release=expected_release,
                 summary=model['summary'],adapter_sha256=sha(Path(__file__)),
                 method='Read-only research projection; unchanged owner compaction; complete native export parity required.')
    save(out/'projection-provenance.json',proof)
    print('Starting full native export parity',flush=True)
    validation=validate_native_export(model,bundle, execution_context=SimpleNamespace(
        manifest=release, folder=args.release.resolve()))
    payload={'empirical_template_model.json':canonical_bytes(model),
             'parser.py':(bundle/'parser.py').read_bytes(),
             'parser-manifest.json':canonical_bytes(model['parser']),
             'owner_rules.json':canonical_bytes(model['owner_rules']),
             'native-validation.json':canonical_bytes(validation),
             'assignment.py':(bundle/'assignment.py').read_bytes(),
             'continuations.py':(bundle/'continuations.py').read_bytes()}
    assert set(payload)==ARTIFACTS
    for name,data in payload.items():(out/name).write_bytes(data)
    compact_manifest=dict(schema=RELEASE_SCHEMA,schema_version=1,revision_id=model['revision_id'],
        parser=model['parser'],hashes={name:hashlib.sha256(data).hexdigest() for name,data in payload.items()},
        source_candidate_manifest_sha256=args.bundle_pin,source_candidate_revision=candidate['revision_id'],
        projection_provenance_sha256=sha(out/'projection-provenance.json'))
    (out/'manifest.json').write_bytes(canonical_bytes(compact_manifest))
    save(out/'completion.json',dict(seconds=time.monotonic()-start,manifest_sha256=sha(out/'manifest.json'),
                                  model_revision=model['revision_id'],validation=validation))
    print(json.dumps(dict(model_revision=model['revision_id'],validation=validation),indent=2),flush=True)


if __name__=='__main__':main()
