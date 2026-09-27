"""Publish a compact, immutable native model after replaying its real evidence.

No learner inference, log normalization or application/SQL activation occurs here.
The reference matcher is the existing matcher, never an export-specific copy.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from template_learning.artifacts import canonical_bytes, load_bundle, MODEL_SCHEMA, MODEL_VERSION
from template_learning.inventory import sha256_file
from template_learning.parsers import load_parser, reference_from_manifest
from template_learning.patterns import pattern_identity
from template_learning.records import SequenceRecord, identity
from template_learning.research_matching import match_record, assignment_candidates
from template_learning.assignment import select_assignment
from template_learning.inspect_incremental_learning import native_evidence_rows

RELEASE_SCHEMA = 'ck3chronicle.native-model-release'
ARTIFACTS = {'empirical_template_model.json', 'parser.py', 'parser-manifest.json',
             'owner_rules.json', 'native-validation.json', 'assignment.py', 'continuations.py'}


def compact_template(template):
    keys = ('template_id', 'source_family', 'context_kind', 'construction_id',
            'parameter_structures', 'status', 'learning_support', 'display',
            'unique_messages', 'support_occurrences', 'selection_evidence', 'continuation')
    result = {k: template[k] for k in keys if k in template}
    result['parts'] = pattern_identity(template['parts'])
    result['context_patterns'] = {
        name: [compact_template(p) for p in patterns]
        for name, patterns in template['context_patterns'].items()}
    return result


def compact_model(candidate):
    keys = ('schema', 'schema_version', 'record_scope', 'parser', 'algorithm',
            'slot_definitions', 'owner_rules', 'literal_guidance', 'constructions',
            'diagnostic_policy', 'summary', 'by_source', 'assignment_policy')
    result = {k: candidate[k] for k in keys}
    result.update(status='published', source_candidate_revision=candidate['revision_id'],
                  templates=[compact_template(t) for t in candidate['templates']],
                  training_evidence=[{'sha256': sha, **{k: value[k] for k in
                      ('bytes', 'timestamped_blocks', 'recovered_messages')}}
                      for sha, value in sorted(candidate['evidence'].items())])
    result['publication'] = dict(
        authority='Owner-authorized model delivery. This export preserves the reviewed candidate templates, statuses, JSON-declared policy and complete assignment interface. Publication alone does not activate the pipeline or change its selection.',
        template_statuses_preserved=True,
        integration='Pipeline migration required; publication does not activate ingestion.',
        review='docs/LEARNER_PARSER_PIPELINE_HANDOFF.md')
    result['revision_id'] = identity(result)[:24]
    return result


def verify_reference_implementation(model):
    """Guard replay against silently using different mutable learner code/rules."""
    root = Path(__file__).parent
    for name, digest in model['algorithm']['implementation_hashes'].items():
        path = (root / name).resolve()
        if path.parent != root.resolve() or sha256_file(path) != digest:
            raise ValueError(f'reference implementation differs: {name}')


def validate_native_export(model, bundle):
    """Replay every complete contextual message, preserving all alternatives."""
    verify_reference_implementation(model)
    by_source = {}
    for template in model['templates']:
        by_source.setdefault(template['source_family'], []).append(template)
    counts = Counter(full=0, provisional=0, unknown=0)
    rows = captures = 0
    for row, occurrences in native_evidence_rows(bundle / 'native_evidence.json'):
        record = SequenceRecord(row['source_family'], row['native'],
            tuple(map(tuple, row['pieces'])), row['context_kind'], row['contexts'],
            continuations=tuple(row['continuations']))
        if ''.join(t for _, t in record.pieces) != record.text:
            raise ValueError('native piece reconstruction differs')
        ambiguities = []
        matches = [m for t in by_source.get(record.source_family, [])
                   if (m := match_record(t, record, capture_ambiguities=ambiguities)) is not None]
        # Includes exact captures, wrapper alternatives, template IDs and statuses.
        if matches != row['matches'] or ambiguities != row['capture_ambiguities']:
            raise ValueError(f'compact export changes matching: {row["record_id"]}')
        selected = select_assignment(model,assignment_candidates(matches,ambiguities))
        if selected != row['selected_assignment']:
            raise ValueError('compact export changes selected assignment')
        outcome = ('full' if selected and selected['match_status']=='template' else
                   'provisional' if selected else 'unknown')
        if outcome != row['outcome']:
            raise ValueError('compact export changes outcome')
        native = record.text.encode('utf-8', errors='surrogateescape')
        for match in matches:
            for capture in match['captures']:
                if capture['span'] is not None:
                    a, b = capture['span']
                    if native[a:b].decode('utf-8', errors='surrogateescape') != capture['value']:
                        raise ValueError('capture differs from native bytes')
                    captures += 1
            for components in match['component_witnesses']:
                for component in components:
                    original = record.continuations[component['index']]['text'].encode('utf-8','surrogateescape')
                    for capture in component['captures']:
                        a,b=capture['span']
                        if original[a:b].decode('utf-8','surrogateescape') != capture['value']:
                            raise ValueError('component capture differs from native bytes')
                        captures += 1
        counts[outcome] += occurrences
        rows += 1
    if dict(counts) != model['summary']['training_outcomes']:
        raise ValueError('native replay counts differ')
    return dict(schema='ck3chronicle.native-release-validation', version=1,
        contextual_messages=rows, occurrences=sum(counts.values()), outcomes=dict(counts),
        captures_checked=captures, changed_matches=0, changed_outcomes=0,
        native_evidence_sha256=sha256_file(bundle / 'native_evidence.json'),
        scope='All actual messages from the complete training logs; export parity is not unseen accuracy.',
        source_candidate_revision=model['source_candidate_revision'])


def load_release(folder, *, expected_manifest_sha256):
    """Explicit new release format; validates hashes/identity before loading code.

    The expected manifest digest is supplied by selection/configuration, not
    accepted from an unverified manifest. No current-rule dependency for loading.
    Call verify_reference_implementation before using the research matcher.
    """
    folder = Path(folder).resolve()
    if sha256_file(folder / 'manifest.json') != expected_manifest_sha256:
        raise ValueError('release manifest hash mismatch')
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    if (manifest.get('schema'), manifest.get('schema_version')) != (RELEASE_SCHEMA, 1):
        raise ValueError('unsupported native release')
    if set(manifest['hashes']) != ARTIFACTS:
        raise ValueError('incomplete release artifact manifest')
    for name, digest in manifest['hashes'].items():
        if sha256_file(folder / name) != digest:
            raise ValueError(f'release artifact hash mismatch: {name}')
    model = json.loads((folder / 'empirical_template_model.json').read_text(encoding='utf-8'))
    if (model.get('schema'), model.get('schema_version'), model.get('status')) != (MODEL_SCHEMA, MODEL_VERSION, 'published'):
        raise ValueError('unsupported published native model')
    revision = identity({k: v for k, v in model.items() if k != 'revision_id'})[:24]
    if revision != model['revision_id'] or revision != manifest['revision_id']:
        raise ValueError('release revision identity disagreement')
    parser_ref = json.loads((folder / 'parser-manifest.json').read_text(encoding='utf-8'))
    if model['parser'] != parser_ref or manifest['parser'] != parser_ref or parser_ref['artifact'] != 'parser.py':
        raise ValueError('release parser disagreement')
    if model['owner_rules'] != json.loads((folder / 'owner_rules.json').read_text(encoding='utf-8')):
        raise ValueError('release rule disagreement')
    return model, load_parser(reference_from_manifest(folder / 'parser-manifest.json'))


def publish(bundle, output):
    bundle, output = Path(bundle).resolve(), Path(output).resolve()
    candidate, parser = load_bundle(bundle)
    model = compact_model(candidate)
    verification = validate_native_export(model, bundle)
    payloads = {'empirical_template_model.json': canonical_bytes(model),
                'parser.py': Path(parser.implementation.__file__).read_bytes(),
                'parser-manifest.json': canonical_bytes(model['parser']),
                'owner_rules.json': canonical_bytes(model['owner_rules']),
                'native-validation.json': canonical_bytes(verification),
                'assignment.py': (bundle/'assignment.py').read_bytes(),
                'continuations.py': (bundle/'continuations.py').read_bytes()}
    import hashlib
    manifest = dict(schema=RELEASE_SCHEMA, schema_version=1, revision_id=model['revision_id'],
        parser=model['parser'], source_candidate_revision=candidate['revision_id'],
        source_candidate_manifest_sha256=sha256_file(bundle / 'manifest.json'),
        build_command='python -B -m template_learning.publish_native_model --bundle <source-candidate-bundle> --output-dir models',
        publisher_sha256=sha256_file(Path(__file__)),
        hashes={name: hashlib.sha256(data).hexdigest() for name, data in payloads.items()})
    payloads['manifest.json'] = canonical_bytes(manifest)
    folder = output / model['revision_id']
    if folder.exists():
        if any(not (folder / name).is_file() or (folder / name).read_bytes() != data
               for name, data in payloads.items()):
            raise ValueError(f'immutable release already differs: {folder}')
    else:
        folder.mkdir(parents=True)
        for name, data in payloads.items():
            (folder / name).write_bytes(data)
    digest = sha256_file(folder / 'manifest.json')
    load_release(folder, expected_manifest_sha256=digest)
    return dict(revision_id=model['revision_id'], folder=str(folder), manifest_sha256=digest,
                summary=model['summary'], validation=verification)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(publish(args.bundle, args.output_dir), indent=2))


if __name__ == '__main__':
    main()
