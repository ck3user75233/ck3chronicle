"""Owner 2026-09-28: line:/near line: are literal choices, never slots.

Complete native logs supply discovery and replay. Explicitly marked in-memory
controls change only an approved label; they are not logs or training evidence.
"""
from copy import deepcopy
from dataclasses import replace
import json
import os
from pathlib import Path
from types import SimpleNamespace
import unittest

from template_learning import artifacts, inventory, records
from template_learning.additive_learning import contextual_records
from template_learning.native_matching import Matcher
from template_learning.native_matching import API_VERSION, iter_native_units
from template_learning.matching_primitives import MatcherDeclarationError
from template_learning.matching_defaults import RULES
from template_learning.parsers import load_parser, reference_from_manifest
from template_learning.patterns import inference_units
from ck3chronicle.pipeline import contracts
from ck3chronicle.pipeline.domain import ResultIntegrityError
from ck3chronicle.pipeline.classifier import Classifier
from ck3chronicle.pipeline.raw_input import iter_diagnostics, native_regions


def unit(record, parser):
    return dict(parser=parser.reference.to_dict(), recovery_status='recovered',
        source_family=record.source_family, context_kind=record.context_kind,
        body=dict(text=record.text, pieces=record.pieces),
        contexts=next(iter(record.contexts.values()), {}), continuations=record.continuations)


def values(assignment):
    return dict(contract_version=contracts.CONTRACT_VERSION, template_id=assignment['template_id'],
        regions=[dict(name=r['name'], layout=r['layout'], component_index=r.get('component_index'),
            bindings=[{k: c[k] for k in ('slot_id', 'type', 'value', 'present')}
                      for c in r['captures']]) for r in assignment['regions']])


@unittest.skipUnless(os.environ.get('CK3_LOCATION_NATIVE_INPUTS'), 'requires complete native logs')
class NativeLocationLabels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        inputs = json.loads(Path(os.environ['CK3_LOCATION_NATIVE_INPUTS']).read_text())
        logs = []
        for row in inputs:
            path = Path(row['path']); stat = path.stat()
            if inventory.sha256_file(path) != row['sha256']:
                raise ValueError('native input digest differs')
            logs.append(inventory.ProtectedLog(row['sha256'], 'protected', path,
                row['sha256'], stat.st_size, stat.st_mtime_ns))
        cls.parser = load_parser(reference_from_manifest(
            Path(__file__).resolve().parents[1]/'tools/template_learning/parsers/v1_7/manifest.json'))
        cls.grouped, cls.stats = records.collect_records(logs, parser=cls.parser)
        cls.logs = logs
        cls.model, cls.evidence = artifacts.build_model(cls.grouped, cls.stats, parser=cls.parser)
        cls.matcher = Matcher(cls.model)
        cls.definitions = contracts.materialize_definitions(SimpleNamespace(data=cls.model,
            manifest={'model_revision_id': cls.model['revision_id']}))
        cls.package = SimpleNamespace(data=cls.model, match=cls.matcher.match,
            iter_units=iter_native_units, parse_file=cls.parser.parse_file,
            manifest={'model_revision_id': cls.model['revision_id'], 'matcher_api_version': API_VERSION})
        cls.choice_records = []
        for pool in cls.grouped.values():
            for record in pool:
                if any(k[0] == 'location-label' for k in inference_units(record)[0]):
                    cls.choice_records.append(record)

    def test_native_complete_replay_and_exact_serializable_rendering(self):
        choices = set()
        for pool in self.grouped.values():
            for record in pool:
                for contextual in contextual_records(record):
                    incoming = unit(contextual, self.parser)
                    result = self.matcher.match(incoming)
                    self.assertEqual(result['status'], 'matched', record.text)
                    assignment = result['assignment']
                    stored = json.loads(json.dumps(values(assignment)))
                    rendered = dict(contracts.render_regions(self.definitions[assignment['template_id']], stored))
                    self.assertEqual(rendered['body'], record.text)
                    for name, region in incoming['contexts'].items():
                        self.assertEqual(rendered[name], region['text'])
                    for i, region in enumerate(incoming['continuations']):
                        self.assertEqual(rendered['continuation:'+str(i)], region['text'])
                    for region in assignment['regions']:
                        choices.update(choice for _, choice in region['layout'].get('literal_choices', []))
        self.assertEqual(choices, {0, 1})

    def test_single_observation_declares_both_labels_without_inventing_support(self):
        forms = set()
        for original in self.choice_records:
            record = contextual_records(original)[0]
            spelling = 'near line:' if 'near line:' in record.text else 'line:'
            if spelling in forms:
                continue
            template, = artifacts._learn_pool(record.source_family, [record], .72, [])
            self.assertEqual(template['status'], 'provisional')
            self.assertEqual(template['learning_support']['distinct_messages'], 1)
            label = next(p for p in template['parts'] if 'alternatives' in p)
            self.assertEqual(label['alternatives'], ['line:', 'near line:'])
            self.assertIsNotNone(RULES.match_record(template, record))
            forms.add(spelling)
        self.assertEqual(forms, {'line:', 'near line:'})

    def test_native_classifier_binding_preparation_and_rendering(self):
        classifier = Classifier(self.package)
        seen = set()
        for log in self.logs:
            raw = self.parser.parse_file(log.path)
            for diagnostic in iter_diagnostics(self.package, raw):
                if diagnostic.unit['recovery_status'] != 'recovered':
                    continue
                text = diagnostic.unit['body']['text']
                if 'line:' not in text:
                    continue
                form = 'near' if 'near line:' in text else 'line'
                if form in seen:
                    continue
                classified = classifier.classify(diagnostic)
                if classified.selected is None or not any(
                        'literal_choices' in r.layout for r in classified.selected.regions):
                    continue
                definition = self.definitions[classified.selected.template_id]
                prepared = contracts.prepare_record(definition, classified)
                rendered = dict(contracts.render_regions(definition, json.loads(json.dumps(prepared['values']))))
                self.assertEqual(rendered, {name: r['text'] for name,r in native_regions(diagnostic.unit)})
                seen.add(form)
                if seen == {'near', 'line'}:
                    break
            if seen == {'near', 'line'}:
                break
        self.assertEqual(seen, {'near', 'line'})

    def test_controlled_spelling_swap_keeps_template_fields_and_exact_rendering(self):
        # In-memory lexical controls only. No manufactured logs/Run IDs, and
        # these controls never enter collect_records, build_model or support.
        exercised = set()
        for original in self.choice_records:
            record = contextual_records(original)[0]
            incoming = unit(record, self.parser)
            before = self.matcher.match(incoming)['assignment']
            if before is None or before['template_id'] in exercised:
                continue
            units, spans = inference_units(record)
            a, b = next(span for key, span in zip(units, spans) if key[0] == 'location-label')
            spelling = ''.join(t for _, t in record.pieces[a:b])
            alternate = (('token', 'line'), ('token', ':')) if spelling == 'near line:' else (
                ('token', 'near'), ('gap', ' '), ('token', 'line'), ('token', ':'))
            pieces = (*record.pieces[:a], *alternate, *record.pieces[b:])
            control = deepcopy(incoming)
            control['body'] = dict(text=''.join(t for _, t in pieces), pieces=pieces)
            after = self.matcher.match(control)['assignment']
            self.assertIsNotNone(after, control['body']['text'])
            self.assertEqual(after['template_id'], before['template_id'])
            self.assertEqual(after['match_status'], before['match_status'])
            for old, new in zip(before['regions'], after['regions']):
                self.assertEqual([(c['type'], c['value']) for c in old['captures']],
                                 [(c['type'], c['value']) for c in new['captures']])
            self.assertNotEqual(values(before), values(after))
            rendered = dict(contracts.render_regions(self.definitions[after['template_id']], values(after)))
            self.assertEqual(rendered['body'], control['body']['text'])
            self.assertNotEqual(contracts.identity_digest(values(before)), contracts.identity_digest(values(after)))
            exercised.add(before['template_id'])
        self.assertGreater(len(exercised), 5)
        self.__class__.controlled_templates = sorted(exercised)

    def test_opaque_reason_and_unknown_remain_untouched(self):
        templates = [t for t in self.model['templates']
                     if t['construction_id'] in {'untyped-effect-location-unknown', 'untyped-trigger-location-unknown'}]
        self.assertTrue(templates)
        for template in templates:
            self.assertFalse(any('alternatives' in p for p in template['parts']))
            self.assertEqual([p['type'] for p in template['parts'] if p['kind'] == 'slot'], ['REASON'])
            self.assertIn('Script location: Unknown', template['display'])
        for pool in self.grouped.values():
            for record in pool:
                captures = RULES.field_ranges(record.source_family, record.text, record.pieces)
                captures.update({a:(b,) for a,(b,_) in RULES.parameter_piece_ranges(record.pieces, record.source_family).items()})
                units, spans = inference_units(record)
                for key, (a,b) in zip(units,spans):
                    if key[0] == 'location-label':
                        self.assertFalse(any(x < b and a < field[0] for x,field in captures.items()))

    def test_invalid_choices_and_missing_render_choice_are_rejected(self):
        model = deepcopy(self.model)
        part = next(p for t in model['templates'] for p in t['parts'] if 'alternatives' in p)
        part['alternatives'].append('lines:')
        with self.assertRaises(MatcherDeclarationError):
            Matcher(model)
        record = contextual_records(self.choice_records[0])[0]
        assignment = self.matcher.match(unit(record, self.parser))['assignment']
        stored = values(assignment)
        chosen = next(r for r in stored['regions'] if 'literal_choices' in r['layout'])
        chosen['layout'] = {k:v for k,v in chosen['layout'].items() if k != 'literal_choices'}
        with self.assertRaises(ResultIntegrityError):
            contracts.render(self.definitions[assignment['template_id']], stored)

    def test_equivalence_does_not_relax_other_wording_or_source(self):
        record = contextual_records(self.choice_records[0])[0]
        template, = artifacts._learn_pool(record.source_family, [record], .72, [])
        self.assertIsNone(RULES.match_record(template, replace(record, source_family='not-the-emitter.cpp')))
        pieces = (('token', 'Unrelated'), ('gap', ' '), *record.pieces)
        self.assertIsNone(RULES.match_record(template, replace(record,
            text=''.join(t for _,t in pieces), pieces=pieces)))

    @classmethod
    def tearDownClass(cls):
        destination = os.environ.get('CK3_LOCATION_OUTPUT')
        if not destination:
            return
        output = Path(destination)
        output.mkdir(parents=True, exist_ok=True)
        bundle = artifacts.write_bundle(output/'candidate', cls.model, cls.evidence,
            parser=cls.parser, build_command=['python', '-m', 'unittest', 'test_learner_location_label_requirements'])
        report = dict(learner=artifacts.learner_identity(), model_revision=cls.model['revision_id'],
            model_schema=cls.model['schema_version'], matcher_api=API_VERSION, bundle=str(bundle.resolve()),
            inputs=[dict(path=str(log.path),sha256=log.sha256) for log in cls.logs],
            summary=cls.model['summary'],
            native_body_label_examples=len(cls.choice_records),
            controlled_template_ids=getattr(cls, 'controlled_templates', []),
            controls='In-memory spelling swaps only; excluded from training and native occurrence counts')
        (output/'verification.json').write_bytes(artifacts.canonical_bytes(report))


if __name__ == '__main__':
    unittest.main()
