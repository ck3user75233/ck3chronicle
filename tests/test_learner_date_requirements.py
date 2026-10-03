"""Owner's 2026-09-27 date-as-KEY requirement, using complete native logs.

CK3_DATE_NATIVE_INPUTS names a JSON inventory of complete logs with path/sha256.
No generated messages or artificial Runs are used.
"""
import json
import os
from pathlib import Path
import unittest

from template_learning import artifacts, clustering, inventory, records
from template_learning.parsers import load_parser, reference_from_manifest
from template_learning.patterns import inference_units
from template_learning.matching_defaults import RULES


@unittest.skipUnless(os.environ.get('CK3_DATE_NATIVE_INPUTS'), 'requires complete native logs')
class NativeDateRequirements(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        inputs = json.loads(Path(os.environ['CK3_DATE_NATIVE_INPUTS']).read_text())
        logs = []
        for row in inputs:
            path = Path(row['path']); stat = path.stat()
            logs.append(inventory.ProtectedLog(row['sha256'], 'protected', path,
                        row['sha256'], stat.st_size, stat.st_mtime_ns))
        parser = load_parser(reference_from_manifest(
            Path(__file__).resolve().parents[1] / 'tools/template_learning/parsers/v1_7/manifest.json'))
        cls.parser = parser
        cls.grouped, cls.stats = records.collect_records(logs, parser=parser)

    def test_complete_native_candidate_build_accepts_inferred_fields(self):
        from template_learning.native_matching import Matcher
        model, evidence = artifacts.build_model(self.grouped, self.stats, parser=self.parser)
        loaded = Matcher(json.loads(artifacts.canonical_bytes(model)))
        self.assertTrue(any(p.get('constraints', {}).get('balanced_pairs')
                            for t in model['templates'] for p in t['parts']))
        for row in evidence['records']:
            if row['source_family'] == 'landed_title_manager.cpp':
                record = next(r for r in self.grouped[row['source_family']] if r.text == row['native'])
                self.assertEqual(loaded.inspect_record(record)[2], row['selected_assignment'])

    def test_one_observed_date_learns_key_and_matches_other_native_date(self):
        pool = self.grouped['landed_title_manager.cpp']
        training = [r for r in pool if ' Date 1178.10.1. Title ' in r.text]
        unseen = [r for r in pool if ' Date 1066.9.15. Title ' in r.text]
        self.assertTrue(training); self.assertTrue(unseen)
        templates = artifacts._learn_pool('landed_title_manager.cpp', training, .72, [])
        self.assertEqual(len(templates), 1)
        template = templates[0]
        self.assertTrue(template['display'].startswith(' Date <KEY>. Title '))
        for record in [*training, *unseen]:
            result = RULES.match_record(template, record)
            self.assertIsNotNone(result, record.text)
            date = next(c for c in result['captures'] if c['name'] == 's0')
            self.assertEqual(date['type'], 'KEY')
            self.assertEqual(record.text.encode('utf-8')[slice(*date['span'])], date['value'].encode())
            self.assertEqual(sum(k == 'token' and t == date['value'] for k, t in record.pieces), 1)
            self.assertNotIn(('token', date['value']), clustering.learning_tokens(record))
            self.assertEqual(sum(c['type'] == 'CHARACTER_FULL_ID' for c in result['captures']), 1)

    def test_single_native_date_observation_stays_provisional(self):
        record = next(r for r in self.grouped['landed_title_manager.cpp']
                      if ' Date 1178.10.1. Title ' in r.text)
        template, = artifacts._learn_pool(record.source_family, [record], .72, [])
        self.assertEqual(template['status'], 'provisional')
        self.assertEqual(template['learning_support']['distinct_diagnostic_examples'], 1)
        self.assertEqual(template['selection_evidence']['unsubstantiated_fields'], 0)
        self.assertTrue(template['display'].startswith(' Date <KEY>. Title '))

    def test_every_exposed_native_date_is_a_complete_key_capture(self):
        examined = 0
        for source, pool in self.grouped.items():
            dated = []
            for record in pool:
                units, spans = inference_units(record)
                dates = [span for unit, span in zip(units, spans) if unit == ('date-key',)]
                if dates:
                    dated.append((record, dates))
            if not dated:
                continue
            templates = artifacts._learn_pool(source, pool, .72, [])
            for record, dates in dated:
                matches = [m for t in templates if (m := RULES.match_record(t, record)) is not None]
                self.assertTrue(matches, record.text)
                offsets = [0]
                for _, value in record.pieces:
                    offsets.append(offsets[-1] + len(value.encode('utf-8', 'surrogateescape')))
                for a, b in dates:
                    self.assertTrue(any(any(c['type'] == 'KEY' and c['span'] == [offsets[a], offsets[b]]
                                            for c in match['captures']) for match in matches), record.text)
                    examined += 1
        self.assertGreater(examined, 0)


if __name__ == '__main__':
    unittest.main()
